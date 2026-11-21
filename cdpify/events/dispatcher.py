import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from cdpify.codec import decode_cdp

logger = logging.getLogger(__name__)
_NOT_DECODED = object()


@dataclass(frozen=True, slots=True)
class RawCDPEvent:
    params: dict[str, Any]  # smelt: ignore[MOD011] -- Original wire payload by API.
    session_id: str | None = None
    method: str = ""
    _decoded: dict[type, Any] = field(  # smelt: ignore[MOD011] -- Lazy decode cache.
        default_factory=dict, init=False, repr=False, compare=False
    )

    def decode[T](self, event_type: type[T]) -> T:
        """Decode lazily once per type; listeners share the cached model.

        Treat the result as read-only, or copy it before making changes. The
        cache lives only as long as this received event remains referenced.
        """
        model = self._decoded.get(event_type, _NOT_DECODED)
        if model is _NOT_DECODED:
            model = decode_cdp(event_type, self.params)
            self._decoded[event_type] = model
        return model


_EventHandler = Callable[[RawCDPEvent], Awaitable[None]]
type _HandlersByEvent = dict[str | None, list[_EventHandler]]


class EventDispatcher:
    def __init__(self) -> None:
        self._handlers_by_session: dict[str | None, _HandlersByEvent] = {}
        self._all_session_handlers: _HandlersByEvent = {}

    def add_handler(
        self,
        event_name: str | None,
        handler: _EventHandler,
        *,
        session_id: str | None = None,
        all_sessions: bool = False,
    ) -> None:
        if all_sessions:
            handlers_by_event = self._all_session_handlers
        else:
            handlers_by_event = self._handlers_by_session.setdefault(session_id, {})
        handlers_by_event.setdefault(event_name, []).append(handler)

    def remove_handler(
        self,
        event_name: str | None,
        handler: _EventHandler,
        *,
        session_id: str | None = None,
        all_sessions: bool = False,
    ) -> None:
        handlers_by_event = (
            self._all_session_handlers
            if all_sessions
            else self._handlers_by_session.get(session_id)
        )
        if handlers_by_event is None:
            return

        handlers = handlers_by_event.get(event_name)
        if handlers is None:
            return

        if handler in handlers:
            handlers.remove(handler)
        if not handlers:
            del handlers_by_event[event_name]
            if not all_sessions and not handlers_by_event:
                del self._handlers_by_session[session_id]

    def remove_session_handlers(self, session_id: str) -> None:
        self._handlers_by_session.pop(session_id, None)

    async def dispatch(self, method: str, event: RawCDPEvent) -> bool:
        any_handled = False

        session_handlers = self._handlers_by_session.get(event.session_id)
        handler_groups = (
            self._all_session_handlers.get(method, ()),
            self._all_session_handlers.get(None, ()),
        )
        if session_handlers is not None:
            handler_groups = (
                session_handlers.get(method, ()),
                session_handlers.get(None, ()),
                *handler_groups,
            )
        for handlers in handler_groups:
            for handler in tuple(handlers):
                if await _invoke_handler(handler, event):
                    any_handled = True

        return any_handled


async def _invoke_handler(handler: _EventHandler, event: RawCDPEvent) -> bool:
    try:
        await handler(event)
        return True
    except Exception:
        # A failing user handler must not block delivery to other listeners.
        logger.exception("Event handler %r failed", handler)
        return False
