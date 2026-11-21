import asyncio
import logging
from functools import partial
from typing import Any, Literal, Self

from .domains import DomainAccessors
from .error import CDPConnectionError
from .event_queue import OverflowPolicy
from .events import EventRouter, EventSource, EventSubscription, ReceivedEvent
from .executor import BoundCommandExecutor
from .session import CdpSession
from .transport import CallbackTransport, Transport, TransportEvent
from .unset import UNSET, UnsetType

logger = logging.getLogger(__name__)


class CdpClient(DomainAccessors, EventSource):
    def __init__(
        self,
        url: str | None = None,
        *,
        transport: Transport | None = None,
        additional_headers: dict[str, str] | None = None,
        max_frame_size: int = 100 * 1024 * 1024,
        default_timeout_seconds: float | None = 30.0,
        max_queue_size: int = 0,
        overflow: OverflowPolicy = "error",
        compression: Literal["deflate"] | None = None,
        open_timeout_seconds: float | None = 10.0,
        close_timeout_seconds: float | None = 10.0,
    ) -> None:
        transport = _resolve_transport(
            url,
            transport=transport,
            additional_headers=additional_headers,
            max_frame_size=max_frame_size,
            max_queue_size=max_queue_size,
            overflow=overflow,
            compression=compression,
            open_timeout_seconds=open_timeout_seconds,
            close_timeout_seconds=close_timeout_seconds,
        )

        self._transport = transport
        self._default_timeout_seconds = default_timeout_seconds
        self._executor: BoundCommandExecutor = BoundCommandExecutor(
            transport, default_timeout_seconds=default_timeout_seconds
        )
        self._new_router = partial(
            EventRouter, max_queue_size=max_queue_size, overflow=overflow
        )
        EventSource.__init__(self, self._new_router(), None)
        self._connection_lock = asyncio.Lock()
        self._event_loop_task: asyncio.Task[None] | None = None
        self._disconnect_task: asyncio.Task[None] | None = None

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()

    @property
    def transport(self) -> Transport:
        return self._transport

    @property
    def is_connected(self) -> bool:
        return self._transport.is_connected

    async def connect(self) -> None:
        async with self._connection_lock:
            if self.is_connected:
                raise CDPConnectionError("Already connected")
            if self._disconnect_task is not None:
                await asyncio.shield(self._disconnect_task)
            self._disconnect_task = None
            if self._event_router.is_closed:
                self._event_router = self._new_router()
            callback_transport = (
                self._transport
                if isinstance(self._transport, CallbackTransport)
                else None
            )
            if callback_transport is not None:
                callback_transport.set_event_handler(self._dispatch_event)
            try:
                await self._transport.connect()
            except BaseException:
                self._event_router.close()
                if callback_transport is not None:
                    callback_transport.set_event_handler(None)
                raise
            if callback_transport is None:
                self._event_loop_task = asyncio.create_task(self._run_event_loop())

    async def disconnect(self) -> None:
        """Close once; cancellation of a waiter does not interrupt cleanup."""
        async with self._connection_lock:
            if self._disconnect_task is None:
                self._disconnect_task = asyncio.create_task(self._disconnect())
            task = self._disconnect_task
        await asyncio.shield(task)

    async def attach(self, target_id: str) -> CdpSession:
        """Attach to a target in flat mode and return its bound session."""
        attached = await self.target.attach_to_target(target_id=target_id, flatten=True)
        return self.bind_session(attached.session_id)

    def bind_session(self, session_id: str) -> CdpSession:
        """Bind to an existing session ID locally, without sending a command."""
        return CdpSession(
            self._transport,
            self._event_router,
            session_id,
            default_timeout_seconds=self._default_timeout_seconds,
        )

    async def execute(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        *,
        session_id: str | None = None,
        timeout_seconds: float | None | UnsetType = UNSET,
    ) -> dict[str, Any]:
        """Execute a low-level command, optionally routed to a target session."""
        executor = (
            self._executor if session_id is None else self.bind_session(session_id)
        )
        return await executor.execute(
            method=method,
            params=params,
            timeout_seconds=timeout_seconds,
        )

    def listen_all[T](
        self,
        event_type: type[T],
        *,
        timeout_seconds: float | None = None,
        event_name: str | None = None,
        max_queue_size: int | None = None,
        overflow: OverflowPolicy | None = None,
    ) -> EventSubscription[ReceivedEvent[T]]:
        """Subscribe to matching events from the root and every target session.

        Accepts the same arguments as :meth:`listen`.
        """
        return self._event_router.listen_all(
            event_type,
            timeout_seconds=timeout_seconds,
            event_name=event_name,
            max_queue_size=max_queue_size,
            overflow=overflow,
        )

    def listen_all_raw(
        self,
        method: str | None = None,
        *,
        timeout_seconds: float | None = None,
        max_queue_size: int | None = None,
        overflow: OverflowPolicy | None = None,
    ) -> EventSubscription[TransportEvent]:
        """Listen to wire dictionaries from the root and every target session."""
        return self._event_router.listen_raw(
            method,
            session_id=None,
            all_sessions=True,
            timeout_seconds=timeout_seconds,
            max_queue_size=max_queue_size,
            overflow=overflow,
        )

    async def _disconnect(self) -> None:
        await self._stop_event_loop()
        try:
            await self._transport.disconnect()
        finally:
            self._event_router.close()
            if isinstance(self._transport, CallbackTransport):
                self._transport.set_event_handler(None)

    async def _run_event_loop(self) -> None:
        try:
            async for event in self._transport.events():
                await self._dispatch_event(event)
        except asyncio.CancelledError:
            raise
        except Exception:
            # Custom transports can raise arbitrary errors while iterating.
            logger.exception("Transport event loop error")
        finally:
            self._event_router.close()

    async def _dispatch_event(self, event: TransportEvent | None) -> None:
        if event is None:
            self._event_router.close()
            return
        logger.debug("Event: %s", event.method)
        handled = await self._event_router.dispatch(event)
        if not handled:
            logger.debug("Unhandled event: %s", event.method)

    async def _stop_event_loop(self) -> None:
        task = self._event_loop_task
        if task and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        self._event_loop_task = None


def _resolve_transport(
    url: str | None,
    *,
    transport: Transport | None,
    additional_headers: dict[str, str] | None,
    max_frame_size: int,
    max_queue_size: int,
    overflow: OverflowPolicy,
    compression: Literal["deflate"] | None,
    open_timeout_seconds: float | None,
    close_timeout_seconds: float | None,
) -> Transport:
    if transport is not None:
        if url is not None:
            raise TypeError("Pass either url or transport, not both")
        return transport
    if url is None:
        raise TypeError("CdpClient requires either url or transport")

    try:
        from .transports.websocket import WebSocketTransport
    except ModuleNotFoundError as error:
        if error.name == "websockets":
            raise RuntimeError(
                "The default WebSocket transport requires cdpify[websocket]"
            ) from error
        raise

    return WebSocketTransport(
        url,
        additional_headers=additional_headers,
        max_frame_size=max_frame_size,
        max_queue_size=max_queue_size,
        overflow=overflow,
        compression=compression,
        open_timeout_seconds=open_timeout_seconds,
        close_timeout_seconds=close_timeout_seconds,
    )
