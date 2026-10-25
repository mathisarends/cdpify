import asyncio
import weakref
from collections.abc import Callable
from types import TracebackType
from typing import Final, Self

from cdpify.exceptions import CDPStreamClosedError

from .dispatcher import RawCDPEvent

_STREAM_END: Final = object()
_UNSET: Final = object()


class EventBuffer:
    """Queue between the dispatcher and one subscription.

    The router holds the buffer, not the subscription, so a subscription that is
    garbage collected without being closed can still unsubscribe itself.
    """

    __slots__ = ("_queue",)

    def __init__(self) -> None:
        self._queue: asyncio.Queue[RawCDPEvent | object] = asyncio.Queue()

    def push(self, event: RawCDPEvent) -> None:
        self._queue.put_nowait(event)

    def finish(self) -> None:
        self._queue.put_nowait(_STREAM_END)

    async def get(self, timeout: float | None) -> RawCDPEvent | None:
        if timeout is None:
            item = await self._queue.get()
        else:
            item = await asyncio.wait_for(self._queue.get(), timeout=timeout)
        return item if isinstance(item, RawCDPEvent) else None


class EventSubscription[T]:
    """A stream of events that is registered as soon as it is created.

    Events that arrive between creating the subscription and reading from it are
    buffered, so it is safe to subscribe first and then trigger the event::

        async with client.listen(LoadEventFiredEvent) as events:
            await client.page.navigate(url="https://example.com")
            event = await events.next(timeout=10)

    Iterating with ``async for`` yields events until the subscription is closed or
    the client disconnects. Leaving the ``async with`` block or calling
    :meth:`aclose` unsubscribes immediately.
    """

    def __init__(
        self,
        buffer: EventBuffer,
        convert: Callable[[RawCDPEvent], T],
        *,
        timeout: float | None,
        unsubscribe: Callable[[], None],
    ) -> None:
        self._buffer = buffer
        self._convert = convert
        self._timeout = timeout
        self._ended = False
        self._unsubscribe = weakref.finalize(self, unsubscribe)

    @property
    def closed(self) -> bool:
        """Whether the stream has ended and no further events will be returned."""
        return self._ended

    async def next(self, timeout: float | None | object = _UNSET) -> T:
        """Wait for the next event.

        ``timeout`` defaults to the timeout passed to ``listen()``; ``None`` waits
        forever.

        Raises:
            TimeoutError: No event arrived within ``timeout`` seconds.
            CDPStreamClosedError: The stream ended before another event arrived.
        """
        event = await self._receive(self._timeout if timeout is _UNSET else timeout)
        if event is None:
            raise CDPStreamClosedError("Event stream is closed")
        return self._convert(event)

    async def aclose(self) -> None:
        """Unsubscribe and end the stream, dropping buffered events."""
        if self._ended:
            return
        self._ended = True
        self._unsubscribe()
        self._buffer.finish()

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> T:
        event = await self._receive(self._timeout)
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

    async def _receive(self, timeout: float | None) -> RawCDPEvent | None:
        if self._ended:
            return None
        event = await self._buffer.get(timeout)
        if event is None:
            self._ended = True
            self._unsubscribe()
        return event
