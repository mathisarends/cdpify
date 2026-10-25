from typing import Any

from cdpify.domains import DomainAccessors
from cdpify.events import EventRouter
from cdpify.events.source import EventSource
from cdpify.executor import BoundCommandExecutor
from cdpify.transport import Transport


class CdpSession(DomainAccessors, EventSource):
    """An immutable view of the CDP domains bound to one target session."""

    def __init__(
        self,
        transport: Transport,
        event_router: EventRouter,
        session_id: str,
    ) -> None:
        if not session_id:
            raise ValueError("session_id must not be empty")

        EventSource.__init__(self, event_router, session_id)
        self._session_id: str = session_id
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
