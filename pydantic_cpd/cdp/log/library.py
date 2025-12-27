"""Generated client library from CDP specification"""
# Domain: Log Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    StartViolationsReportParams,
)


class LogClient:
    """Provides access to log entries."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def clear(self, session_id: str | None = None) -> dict[str, Any]:
        """Clears the log."""
        result = await self._client.send_raw(
            method="Log.clear",
            params=None,
            session_id=session_id,
        )
        return result

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables log domain, prevents further log entries from being reported to the client."""
        result = await self._client.send_raw(
            method="Log.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        """Enables log domain, sends the entries collected so far to the client by means of the
        `entryAdded` notification."""
        result = await self._client.send_raw(
            method="Log.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def start_violations_report(
        self, params: StartViolationsReportParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """start violation reporting."""
        result = await self._client.send_raw(
            method="Log.startViolationsReport",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def stop_violations_report(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        """Stop violation reporting."""
        result = await self._client.send_raw(
            method="Log.stopViolationsReport",
            params=None,
            session_id=session_id,
        )
        return result
