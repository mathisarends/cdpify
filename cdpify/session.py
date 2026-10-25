from typing import Any

from cdpify.domains import DomainAccessors
from cdpify.events import EventRouter, EventSubscription
from cdpify.executor import BoundCommandExecutor
from cdpify.transport import Transport


class CDPSession(DomainAccessors):
    """An immutable view of the CDP domains bound to one target session."""

    def __init__(
        self,
        transport: Transport,
        event_router: EventRouter,
        session_id: str,
    ) -> None:
        if not session_id:
            raise ValueError("session_id must not be empty")

        self._session_id = session_id
        self._event_router = event_router
        self._executor = BoundCommandExecutor(transport, session_id)

    @property
    def session_id(self) -> str:
        return self._session_id

    async def execute(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        return await self._executor.execute(
            method=method,
            params=params,
            timeout=timeout,
        )

    def listen[T](
        self,
        event_name: str,
        event_type: type[T],
        timeout: float | None = None,
    ) -> EventSubscription[T]:
        """Subscribe to events emitted by this session only."""
        return self._event_router.listen(
            event_name,
            event_type,
            session_id=self._session_id,
            timeout=timeout,
        )
