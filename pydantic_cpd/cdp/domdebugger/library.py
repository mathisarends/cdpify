"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    GetEventListenersParams,
    GetEventListenersResult,
    RemoveDOMBreakpointParams,
    RemoveEventListenerBreakpointParams,
    RemoveInstrumentationBreakpointParams,
    RemoveXHRBreakpointParams,
    SetBreakOnCSPViolationParams,
    SetDOMBreakpointParams,
    SetEventListenerBreakpointParams,
    SetInstrumentationBreakpointParams,
    SetXHRBreakpointParams,
)

class DOMDebuggerClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def get_event_listeners(
        self, params: GetEventListenersParams, session_id: str | None = None
    ) -> GetEventListenersResult:
        result = await self._client.send_raw(
            method="DOMDebugger.getEventListeners",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetEventListenersResult.model_validate(result)

    async def remove_d_o_m_breakpoint(
        self, params: RemoveDOMBreakpointParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMDebugger.removeDOMBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def remove_event_listener_breakpoint(
        self, params: RemoveEventListenerBreakpointParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMDebugger.removeEventListenerBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def remove_instrumentation_breakpoint(
        self, params: RemoveInstrumentationBreakpointParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMDebugger.removeInstrumentationBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def remove_x_h_r_breakpoint(
        self, params: RemoveXHRBreakpointParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMDebugger.removeXHRBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_break_on_c_s_p_violation(
        self, params: SetBreakOnCSPViolationParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMDebugger.setBreakOnCSPViolation",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_d_o_m_breakpoint(
        self, params: SetDOMBreakpointParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMDebugger.setDOMBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_event_listener_breakpoint(
        self, params: SetEventListenerBreakpointParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMDebugger.setEventListenerBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_instrumentation_breakpoint(
        self, params: SetInstrumentationBreakpointParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMDebugger.setInstrumentationBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_x_h_r_breakpoint(
        self, params: SetXHRBreakpointParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMDebugger.setXHRBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
