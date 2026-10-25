from collections.abc import Callable
from dataclasses import dataclass

from cdpify.event_queue import EventQueue
from cdpify.transport import TransportEvent

from .dispatcher import EventDispatcher, RawCDPEvent
from .subscription import EventSubscription


@dataclass(frozen=True, slots=True)
class ReceivedEvent[T]:
    """A typed CDP event together with its transport routing metadata."""

    value: T
    session_id: str | None


class EventRouter:
    """Decode and route transport events to root, session, or global listeners."""

    def __init__(self, *, max_queue_size: int = 0) -> None:
        # Validate the default even when no listeners are registered yet.
        EventQueue(max_queue_size)
        self._max_queue_size = max_queue_size
        self._dispatcher = EventDispatcher()
        self._buffers: set[EventQueue[RawCDPEvent]] = set()
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
        for buffer in self._buffers:
            buffer.finish()
        self._buffers.clear()
        self._dispatcher = EventDispatcher()

    async def dispatch(self, event: TransportEvent) -> bool:
        if self._closed:
            return False
        return await self._dispatcher.dispatch(
            event.method,
            RawCDPEvent(params=event.params, session_id=event.session_id),
        )

    def listen[T](
        self,
        event_type: type[T],
        *,
        session_id: str | None,
        timeout: float | None = None,
        event_name: str | None = None,
        max_queue_size: int | None = None,
    ) -> EventSubscription[T]:
        return self._subscribe(
            _resolve_event_name(event_type, event_name),
            lambda event: event.decode(event_type),
            session_id=session_id,
            timeout=timeout,
            max_queue_size=max_queue_size,
        )

    def listen_all[T](
        self,
        event_type: type[T],
        *,
        timeout: float | None = None,
        event_name: str | None = None,
        max_queue_size: int | None = None,
    ) -> EventSubscription[ReceivedEvent[T]]:
        return self._subscribe(
            _resolve_event_name(event_type, event_name),
            lambda event: ReceivedEvent(
                value=event.decode(event_type),
                session_id=event.session_id,
            ),
            all_sessions=True,
            timeout=timeout,
            max_queue_size=max_queue_size,
        )

    def _subscribe[T](
        self,
        event_name: str,
        convert: Callable[[RawCDPEvent], T],
        *,
        session_id: str | None = None,
        all_sessions: bool = False,
        timeout: float | None,
        max_queue_size: int | None,
    ) -> EventSubscription[T]:
        buffer = EventQueue[RawCDPEvent](
            self._max_queue_size if max_queue_size is None else max_queue_size
        )
        if self._closed:
            buffer.finish()
            return EventSubscription(
                buffer, convert, timeout=timeout, unsubscribe=_do_nothing
            )

        async def handler(event: RawCDPEvent) -> None:
            buffer.push(event)

        def unsubscribe() -> None:
            buffer.finish(discard=True)
            self._buffers.discard(buffer)
            self._dispatcher.remove_handler(
                event_name,
                handler,
                session_id=session_id,
                all_sessions=all_sessions,
            )

        self._dispatcher.add_handler(
            event_name,
            handler,
            session_id=session_id,
            all_sessions=all_sessions,
        )
        self._buffers.add(buffer)
        return EventSubscription(
            buffer, convert, timeout=timeout, unsubscribe=unsubscribe
        )


def _resolve_event_name(event_type: type, event_name: str | None) -> str:
    if event_name is not None:
        return event_name
    name = getattr(event_type, "__cdp_event__", None)
    if not isinstance(name, str):
        raise TypeError(
            f"{event_type.__qualname__} does not define __cdp_event__; "
            "pass event_name= to listen for it"
        )
    return name


def _do_nothing() -> None:
    pass
