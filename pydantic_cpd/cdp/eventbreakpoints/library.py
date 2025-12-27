"""Generated client library from CDP specification"""
# Domain: EventBreakpoints Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    RemoveInstrumentationBreakpointParams,
    SetInstrumentationBreakpointParams,
)


class EventBreakpointsClient:
    """EventBreakpoints permits setting JavaScript breakpoints on operations and events
    occurring in native code invoked from JavaScript. Once breakpoint is hit, it is
    reported through Debugger domain, similarly to regular breakpoints being hit."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def set_instrumentation_breakpoint(
        self, params: SetInstrumentationBreakpointParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Sets breakpoint on particular native event."""
        result = await self._client.send_raw(
            method="EventBreakpoints.setInstrumentationBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def remove_instrumentation_breakpoint(
        self,
        params: RemoveInstrumentationBreakpointParams,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Removes breakpoint on particular native event."""
        result = await self._client.send_raw(
            method="EventBreakpoints.removeInstrumentationBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Removes all breakpoints"""
        result = await self._client.send_raw(
            method="EventBreakpoints.disable",
            params=None,
            session_id=session_id,
        )
        return result
