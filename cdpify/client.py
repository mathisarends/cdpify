import asyncio
import logging
from typing import Any, Self

from cdpify.domains import DomainAccessors
from cdpify.events import EventRouter, EventSubscription, ReceivedEvent
from cdpify.events.source import EventSource
from cdpify.exceptions import CDPConnectionError
from cdpify.executor import BoundCommandExecutor
from cdpify.session import CdpSession
from cdpify.transport import CallbackTransport, Transport, TransportEvent

logger = logging.getLogger(__name__)


class CdpClient(DomainAccessors, EventSource):
    def __init__(
        self,
        url: str | None = None,
        *,
        transport: Transport | None = None,
        additional_headers: dict[str, str] | None = None,
        max_frame_size: int = 100 * 1024 * 1024,
        default_timeout: float = 30.0,
        max_queue_size: int = 0,
    ) -> None:
        if transport is not None and url is not None:
            raise TypeError("Pass either url or transport, not both")
        if transport is None:
            if url is None:
                raise TypeError("CdpClient requires either url or transport")
            transport = _create_websocket_transport(
                url,
                additional_headers=additional_headers,
                max_frame_size=max_frame_size,
                default_timeout=default_timeout,
                max_queue_size=max_queue_size,
            )

        self._transport = transport
        self._executor = BoundCommandExecutor(transport)
        EventSource.__init__(self, EventRouter(max_queue_size=max_queue_size), None)
        self._event_loop_task: asyncio.Task[None] | None = None
        self._disconnect_task: asyncio.Task[None] | None = None

    @property
    def transport(self) -> Transport:
        return self._transport

    @property
    def is_connected(self) -> bool:
        return self._transport.is_connected

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()

    async def connect(self) -> None:
        if self.is_connected:
            raise CDPConnectionError("Already connected")
        if self._disconnect_task is not None:
            await asyncio.shield(self._disconnect_task)
        self._disconnect_task = None
        self._event_router.open()
        callback_transport = (
            self._transport if isinstance(self._transport, CallbackTransport) else None
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
        if self._disconnect_task is None:
            self._disconnect_task = asyncio.create_task(self._disconnect())
        await asyncio.shield(self._disconnect_task)

    async def _disconnect(self) -> None:
        await self._stop_event_loop()
        try:
            await self._transport.disconnect()
        finally:
            self._event_router.close()
            if isinstance(self._transport, CallbackTransport):
                self._transport.set_event_handler(None)

    def session(self, session_id: str) -> CdpSession:
        """Create an immutable domain view bound to ``session_id``."""
        return CdpSession(self._transport, self._event_router, session_id)

    async def execute(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        session_id: str | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Execute a low-level command, optionally routed to a target session."""
        return await self._transport.execute(
            method=method,
            params=params,
            session_id=session_id,
            timeout=timeout,
        )

    def listen_all[T](
        self,
        event_type: type[T],
        *,
        timeout: float | None = None,
        event_name: str | None = None,
        max_queue_size: int | None = None,
    ) -> EventSubscription[ReceivedEvent[T]]:
        """Subscribe to matching events from the root and every target session.

        Accepts the same arguments as :meth:`listen`.
        """
        return self._event_router.listen_all(
            event_type,
            timeout=timeout,
            event_name=event_name,
            max_queue_size=max_queue_size,
        )

    async def _run_event_loop(self) -> None:
        try:
            async for event in self._transport.events():
                await self._dispatch_event(event)
        except asyncio.CancelledError:
            raise
        except Exception:
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


def _create_websocket_transport(
    url: str,
    *,
    additional_headers: dict[str, str] | None,
    max_frame_size: int,
    default_timeout: float,
    max_queue_size: int,
) -> Transport:
    try:
        from cdpify.transports.websocket import WebSocketTransport
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
        default_timeout=default_timeout,
        max_queue_size=max_queue_size,
    )
