import asyncio
import logging
from collections.abc import AsyncIterator
from typing import Any, Self

from cdpify.domains import DomainAccessors
from cdpify.events import EventRouter, ReceivedEvent
from cdpify.executor import BoundCommandExecutor
from cdpify.session import CDPSession
from cdpify.transport import Transport, TransportEvent

logger = logging.getLogger(__name__)


class Client(DomainAccessors):
    def __init__(
        self,
        url: str | None = None,
        *,
        transport: Transport | None = None,
        additional_headers: dict[str, str] | None = None,
        max_frame_size: int = 100 * 1024 * 1024,
        default_timeout: float = 30.0,
    ) -> None:
        if transport is not None and url is not None:
            raise TypeError("Pass either url or transport, not both")
        if transport is None:
            if url is None:
                raise TypeError("Client requires either url or transport")
            transport = _create_websocket_transport(
                url,
                additional_headers=additional_headers,
                max_frame_size=max_frame_size,
                default_timeout=default_timeout,
            )

        self._transport = transport
        self._executor = BoundCommandExecutor(transport)
        self._event_router = EventRouter()
        self._event_loop_task: asyncio.Task[None] | None = None

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
        await self._transport.connect()
        self._event_router.open()
        self._event_loop_task = asyncio.create_task(self._run_event_loop())

    async def disconnect(self) -> None:
        await self._stop_event_loop()
        self._event_router.close()
        await self._transport.disconnect()

    def session(self, session_id: str) -> CDPSession:
        """Create an immutable domain view bound to ``session_id``."""
        return CDPSession(self._transport, self._event_router, session_id)

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

    async def listen[T](
        self,
        event_name: str,
        event_type: type[T],
        timeout: float | None = None,
    ) -> AsyncIterator[T]:
        """Listen for events emitted by the root CDP connection only."""
        async for event in self._event_router.listen(
            event_name,
            event_type,
            session_id=None,
            timeout=timeout,
        ):
            yield event

    async def listen_all[T](
        self,
        event_name: str,
        event_type: type[T],
        timeout: float | None = None,
    ) -> AsyncIterator[ReceivedEvent[T]]:
        """Listen for matching events from the root and every target session."""
        async for event in self._event_router.listen_all(
            event_name,
            event_type,
            timeout=timeout,
        ):
            yield event

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

    async def _dispatch_event(self, event: TransportEvent) -> None:
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
    )
