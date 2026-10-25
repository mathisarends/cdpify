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
    ) -> EventSubscription[T]:
        """Subscribe to events from this connection or bound session only.

        Pass a generated event class such as ``RequestWillBeSentEvent`` or a
        custom dataclass with ``event_name``. ``timeout`` limits each read.
        ``max_queue_size`` overrides the client's default for this subscription;
        zero is unlimited. Full buffers discard the oldest event without
        blocking command responses. See ``EventSubscription.dropped_events``.
        """
        return self._event_router.listen(
            event_type,
            session_id=self._session_id,
            timeout=timeout,
            event_name=event_name,
            max_queue_size=max_queue_size,
        )
