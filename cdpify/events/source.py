from cdpify.event_queue import OverflowPolicy
from cdpify.transport import TransportEvent

from .router import EventRouter
from .subscription import EventSubscription


class EventSource:
    """Shared subscription API for the root client and bound session views."""

    def __init__(self, event_router: EventRouter, session_id: str | None) -> None:
        self._event_router = event_router
        self._session_id = session_id

    def listen[T](
        self,
        event_type: type[T],
        *,
        timeout: float | None = None,
        event_name: str | None = None,
        max_queue_size: int | None = None,
        overflow: OverflowPolicy | None = None,
    ) -> EventSubscription[T]:
        """Subscribe to events from this connection or bound session only.

        Pass a generated event class such as ``RequestWillBeSentEvent`` or a
        custom dataclass with ``event_name``. ``timeout`` limits each read.
        ``max_queue_size`` overrides the client's default for this subscription;
        zero is unlimited. Full buffers terminate the stream with
        CDPEventOverflowError by default. Explicit overflow="drop_oldest"
        discards older events instead. Neither policy blocks command responses.
        See EventSubscription.dropped_events for the count of discarded events.
        Matching listeners share the same decoded model; copy it before making
        changes that should be private to this listener.
        """
        return self._event_router.listen(
            event_type,
            session_id=self._session_id,
            timeout=timeout,
            event_name=event_name,
            max_queue_size=max_queue_size,
            overflow=overflow,
        )

    def listen_raw(
        self,
        method: str | None = None,
        *,
        timeout: float | None = None,
        max_queue_size: int | None = None,
        overflow: OverflowPolicy | None = None,
    ) -> EventSubscription[TransportEvent]:
        """Listen to undecoded events in this root/session scope.

        None matches all methods. Values carry the wire method, raw parameter
        dictionary and session ID. Subscribe before sending a triggering command.
        The lifetime, overflow and read-only data rules match listen().
        """
        return self._event_router.listen_raw(
            method,
            session_id=self._session_id,
            timeout=timeout,
            max_queue_size=max_queue_size,
            overflow=overflow,
        )
