import weakref
from collections.abc import Callable
from types import TracebackType
from typing import Self

from cdpify.error import CDPEventOverflowError, CDPStreamClosedError
from cdpify.event_queue import EventQueue
from cdpify.unset import UNSET, UnsetType

from .dispatcher import RawCDPEvent


class EventSubscription[T]:
    """A stream of events that is registered as soon as it is created.

    Events that arrive between creating the subscription and reading from it are
    buffered, so it is safe to subscribe first and then trigger the event::

        async with client.listen(LoadEventFiredEvent) as events:
            await client.page.navigate(url="https://example.com")
            event = await events.next(timeout_seconds=10)

    Iterating with ``async for`` drains buffered events and ends when the client
    disconnects or Chrome detaches the subscribed session. Leaving the
    ``async with`` block or calling :meth:`aclose` unsubscribes immediately.

    Listeners for the same incoming event and event type share one decoded
    model. Treat it as read-only, or use ``copy.deepcopy`` before changing it.
    """

    def __init__(
        self,
        buffer: EventQueue[RawCDPEvent],
        convert: Callable[[RawCDPEvent], T],
        *,
        timeout_seconds: float | None,
        unsubscribe: Callable[[], None],
    ) -> None:
        self._buffer = buffer
        self._convert = convert
        self._timeout_seconds = timeout_seconds
        self._ended = False
        self._unsubscribe = weakref.finalize(self, unsubscribe)

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> T:
        event = await self._receive(self._timeout_seconds)
        if event is None:
            raise StopAsyncIteration
        return self._convert(event)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    @property
    def closed(self) -> bool:
        """Whether the stream has ended and no further events will be returned."""
        return self._ended or self._buffer.drained

    @property
    def dropped_events(self) -> int:
        """Number of events discarded by the configured overflow policy."""
        return self._buffer.dropped_events

    async def next(self, timeout_seconds: float | None | UnsetType = UNSET) -> T:
        """Wait for the next event.

        Omit ``timeout_seconds`` to use the subscription's default. Pass ``None``
        to wait forever or ``0`` to read only an already buffered event.

        Raises:
            TimeoutError: No event arrived within ``timeout_seconds`` seconds.
            CDPStreamClosedError: The stream ended before another event arrived.
        """
        event = await self._receive(
            self._timeout_seconds if timeout_seconds is UNSET else timeout_seconds
        )
        if event is None:
            raise CDPStreamClosedError("Event stream is closed")
        return self._convert(event)

    async def aclose(self) -> None:
        """Unsubscribe and end the stream, dropping buffered events."""
        if self._ended:
            return
        self._ended = True
        self._unsubscribe()
        self._buffer.finish(discard=True)

    async def _receive(self, timeout_seconds: float | None) -> RawCDPEvent | None:
        if self._ended:
            return None
        try:
            event = await self._buffer.get(timeout_seconds)
        except CDPEventOverflowError:
            await self.aclose()
            raise
        if event is None:
            self._ended = True
            self._unsubscribe()
        return event
