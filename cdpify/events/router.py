from collections.abc import Callable
from dataclasses import dataclass

from cdpify.error import CDPSessionClosedError
from cdpify.event_queue import EventQueue, OverflowPolicy
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

    def __init__(
        self, *, max_queue_size: int = 0, overflow: OverflowPolicy = "error"
    ) -> None:
        # Validate the default even when no listeners are registered yet.
        EventQueue(max_queue_size, overflow=overflow)
        self._max_queue_size = max_queue_size
        self._overflow: OverflowPolicy = overflow
        self._dispatcher = EventDispatcher()
        self._detached_sessions: set[str] = set()
        self._buffers: dict[str | None, set[EventQueue[RawCDPEvent]]] = {}
        self._closed = False

    @property
    def is_closed(self) -> bool:
        return self._closed

    def open(self) -> None:
        """Accept new listeners again, e.g. after a reconnect."""
        self._closed = False

    def ensure_session_open(self, session_id: str) -> None:
        if self._closed or session_id in self._detached_sessions:
            raise CDPSessionClosedError(session_id)

    def close(self) -> None:
        """End every active listener once its buffered events are consumed."""
        if self._closed:
            return
        self._closed = True
        self._detached_sessions.clear()
        for buffers in self._buffers.values():
            for buffer in buffers:
                buffer.finish()
        self._buffers.clear()
        self._dispatcher = EventDispatcher()

    async def dispatch(self, event: TransportEvent) -> bool:
        if self._closed:
            return False
        handled = await self._dispatcher.dispatch(
            event.method,
            RawCDPEvent(
                params=event.params, session_id=event.session_id, method=event.method
            ),
        )
        if event.method == "Target.detachedFromTarget":
            # The envelope identifies the parent session, if there is one.
            detached_id = event.params.get("sessionId")
            if isinstance(detached_id, str):
                self._detached_sessions.add(detached_id)
                for buffer in self._buffers.pop(detached_id, ()):
                    buffer.finish()
                self._dispatcher.remove_session_handlers(detached_id)
        return handled

    def listen[T](
        self,
        event_type: type[T],
        *,
        session_id: str | None,
        timeout: float | None = None,
        event_name: str | None = None,
        max_queue_size: int | None = None,
        overflow: OverflowPolicy | None = None,
    ) -> EventSubscription[T]:
        return self._subscribe(
            _resolve_event_name(event_type, event_name),
            lambda event: event.decode(event_type),
            session_id=session_id,
            timeout=timeout,
            max_queue_size=max_queue_size,
            overflow=overflow,
        )

    def listen_all[T](
        self,
        event_type: type[T],
        *,
        timeout: float | None = None,
        event_name: str | None = None,
        max_queue_size: int | None = None,
        overflow: OverflowPolicy | None = None,
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
            overflow=overflow,
        )

    def listen_raw(
        self,
        method: str | None = None,
        *,
        session_id: str | None,
        all_sessions: bool = False,
        timeout: float | None = None,
        max_queue_size: int | None = None,
        overflow: OverflowPolicy | None = None,
    ) -> EventSubscription[TransportEvent]:
        """Subscribe to wire dictionaries; None matches every method in scope."""
        return self._subscribe(
            method,
            lambda event: TransportEvent(event.method, event.params, event.session_id),
            session_id=session_id,
            all_sessions=all_sessions,
            timeout=timeout,
            max_queue_size=max_queue_size,
            overflow=overflow,
        )

    def _subscribe[T](
        self,
        event_name: str | None,
        convert: Callable[[RawCDPEvent], T],
        *,
        session_id: str | None = None,
        all_sessions: bool = False,
        timeout: float | None,
        max_queue_size: int | None,
        overflow: OverflowPolicy | None,
    ) -> EventSubscription[T]:
        if session_id is not None:
            self.ensure_session_open(session_id)
        buffer = EventQueue[RawCDPEvent](
            self._max_queue_size if max_queue_size is None else max_queue_size,
            overflow=self._overflow if overflow is None else overflow,
        )
        if self._closed:
            buffer.finish()
            return EventSubscription(
                buffer, convert, timeout=timeout, unsubscribe=_do_nothing
            )

        scope = None if all_sessions else session_id

        async def handler(event: RawCDPEvent) -> None:
            buffer.push(event)
            if buffer.failed:
                unsubscribe()

        def unsubscribe() -> None:
            buffer.finish(discard=True)
            buffers = self._buffers.get(scope)
            if buffers is not None:
                buffers.discard(buffer)
                if not buffers:
                    del self._buffers[scope]
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
        self._buffers.setdefault(scope, set()).add(buffer)
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
