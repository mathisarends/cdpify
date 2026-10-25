import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RawCDPEvent:
    params: dict[str, Any]
    session_id: str | None = None


_EventHandler = Callable[[RawCDPEvent], Awaitable[None]]


class EventDispatcher:
    def __init__(self) -> None:
        self._session_handlers: dict[
            tuple[str | None, str | None], list[_EventHandler]
        ] = {}
        self._all_session_handlers: dict[str | None, list[_EventHandler]] = {}

    def add_handler(
        self,
        event_name: str | None,
        handler: _EventHandler,
        *,
        session_id: str | None = None,
        all_sessions: bool = False,
    ) -> None:
        handlers = self._handlers_for(
            event_name,
            session_id=session_id,
            all_sessions=all_sessions,
        )
        handlers.append(handler)

    def remove_handler(
        self,
        event_name: str | None,
        handler: _EventHandler,
        *,
        session_id: str | None = None,
        all_sessions: bool = False,
    ) -> None:
        if all_sessions:
            handlers = self._all_session_handlers.get(event_name, [])
        else:
            handlers = self._session_handlers.get((event_name, session_id), [])

        if handler in handlers:
            handlers.remove(handler)
        if handlers:
            return

        if all_sessions:
            self._all_session_handlers.pop(event_name, None)
        else:
            self._session_handlers.pop((event_name, session_id), None)

    async def dispatch(self, method: str, event: RawCDPEvent) -> bool:
        any_handled = False

        handler_groups = (
            self._session_handlers.get((method, event.session_id), []),
            self._session_handlers.get((None, event.session_id), []),
            self._all_session_handlers.get(method, []),
            self._all_session_handlers.get(None, []),
        )
        for handlers in handler_groups:
            for handler in tuple(handlers):
                if await _invoke_handler(handler, event):
                    any_handled = True

        return any_handled

    def _handlers_for(
        self,
        event_name: str | None,
        *,
        session_id: str | None,
        all_sessions: bool,
    ) -> list[_EventHandler]:
        if all_sessions:
            return self._all_session_handlers.setdefault(event_name, [])
        return self._session_handlers.setdefault((event_name, session_id), [])


async def _invoke_handler(handler: _EventHandler, event: RawCDPEvent) -> bool:
    try:
        await handler(event)
        return True
    except Exception:
        logger.exception("Event handler %r failed", handler)
        return False
