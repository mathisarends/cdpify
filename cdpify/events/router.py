import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass

from cdpify.codec import decode_cdp
from cdpify.transport import TransportEvent

from .dispatcher import EventDispatcher, RawCDPEvent


@dataclass(frozen=True, slots=True)
class ReceivedEvent[T]:
    """A typed CDP event together with its transport routing metadata."""

    value: T
    session_id: str | None


_STREAM_CLOSED = object()


class EventRouter:
    """Decode and route transport events to root, session, or global listeners."""

    def __init__(self) -> None:
        self._dispatcher = EventDispatcher()
        self._queues: set[asyncio.Queue[RawCDPEvent | object]] = set()
        self._closed = False

    @property
    def is_closed(self) -> bool:
        return self._closed

    def open(self) -> None:
        """Accept new listeners again, e.g. after a reconnect."""
        self._closed = False

    def close(self) -> None:
        """End every active listener once its buffered events are consumed."""
        if self._closed:
            return
        self._closed = True
        for queue in self._queues:
            queue.put_nowait(_STREAM_CLOSED)

    async def dispatch(self, event: TransportEvent) -> bool:
        return await self._dispatcher.dispatch(
            event.method,
            RawCDPEvent(params=event.params, session_id=event.session_id),
        )

    async def listen[T](
        self,
        event_name: str,
        event_type: type[T],
        *,
        session_id: str | None,
        timeout: float | None = None,
    ) -> AsyncIterator[T]:
        async for event in self._listen_raw(
            event_name,
            session_id=session_id,
            timeout=timeout,
        ):
            yield decode_cdp(event_type, event.params)

    async def listen_all[T](
        self,
        event_name: str,
        event_type: type[T],
        *,
        timeout: float | None = None,
    ) -> AsyncIterator[ReceivedEvent[T]]:
        async for event in self._listen_raw(
            event_name,
            all_sessions=True,
            timeout=timeout,
        ):
            yield ReceivedEvent(
                value=decode_cdp(event_type, event.params),
                session_id=event.session_id,
            )

    async def _listen_raw(
        self,
        event_name: str,
        *,
        session_id: str | None = None,
        all_sessions: bool = False,
        timeout: float | None = None,
    ) -> AsyncIterator[RawCDPEvent]:
        if self._closed:
            return

        queue: asyncio.Queue[RawCDPEvent | object] = asyncio.Queue()

        async def handler(event: RawCDPEvent) -> None:
            queue.put_nowait(event)

        self._queues.add(queue)
        try:
            self._dispatcher.add_handler(
                event_name,
                handler,
                session_id=session_id,
                all_sessions=all_sessions,
            )
            while True:
                if timeout is None:
                    item = await queue.get()
                else:
                    item = await asyncio.wait_for(queue.get(), timeout=timeout)
                if not isinstance(item, RawCDPEvent):
                    return
                yield item
        finally:
            self._queues.discard(queue)
            self._dispatcher.remove_handler(
                event_name,
                handler,
                session_id=session_id,
                all_sessions=all_sessions,
            )
