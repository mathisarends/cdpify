import asyncio
from collections import deque


class EventQueue[T]:
    """A non-blocking event buffer that drops the oldest item on overflow.

    Use from one asyncio event loop. Zero means unlimited buffering. Items must
    not be None, which get() returns once a closed queue is fully drained.
    Closing wakes readers without consuming capacity or evicting queued events.
    """

    __slots__ = ("_items", "_ready", "_closed", "_max_size", "dropped_events")

    def __init__(self, max_queue_size: int = 0) -> None:
        if not isinstance(max_queue_size, int):
            raise TypeError("max_queue_size must be an integer")
        if max_queue_size < 0:
            raise ValueError("max_queue_size must be non-negative")
        self._items: deque[T] = deque()
        self._ready = asyncio.Event()
        self._closed = False
        self._max_size = max_queue_size
        self.dropped_events = 0

    def push(self, item: T) -> None:
        """Append an event, evicting the oldest if full; ignore events after close."""
        if self._closed:
            return
        if self._max_size and len(self._items) >= self._max_size:
            self._items.popleft()
            self.dropped_events += 1
        self._items.append(item)
        self._ready.set()

    def finish(self, *, discard: bool = False) -> None:
        """Close and wake all readers, optionally releasing buffered events."""
        self._closed = True
        if discard:
            self._items.clear()
        self._ready.set()

    async def get(self, timeout: float | None = None) -> T | None:
        """Read the next event, or None after closure; raise TimeoutError on timeout."""
        if timeout is None:
            return await self._receive()
        return await asyncio.wait_for(self._receive(), timeout=timeout)

    async def _receive(self) -> T | None:
        while not self._items:
            if self._closed:
                return None
            await self._ready.wait()
        item = self._items.popleft()
        if not self._items and not self._closed:
            self._ready.clear()
        return item
