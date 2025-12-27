"""Generated client library from CDP specification"""
# Domain: Tracing Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    GetCategoriesResult,
    GetTrackEventDescriptorResult,
    RecordClockSyncMarkerParams,
    RequestMemoryDumpParams,
    RequestMemoryDumpResult,
    StartParams,
)


class TracingClient:
    """CDP Tracing domain client."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def end(self, session_id: str | None = None) -> dict[str, Any]:
        """Stop trace events collection."""
        result = await self._client.send_raw(
            method="Tracing.end",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_categories(
        self, session_id: str | None = None
    ) -> GetCategoriesResult:
        """Gets supported tracing categories."""
        result = await self._client.send_raw(
            method="Tracing.getCategories",
            params=None,
            session_id=session_id,
        )
        return GetCategoriesResult.model_validate(result)

    async def get_track_event_descriptor(
        self, session_id: str | None = None
    ) -> GetTrackEventDescriptorResult:
        """Return a descriptor for all available tracing categories."""
        result = await self._client.send_raw(
            method="Tracing.getTrackEventDescriptor",
            params=None,
            session_id=session_id,
        )
        return GetTrackEventDescriptorResult.model_validate(result)

    async def record_clock_sync_marker(
        self, params: RecordClockSyncMarkerParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Record a clock sync marker in the trace."""
        result = await self._client.send_raw(
            method="Tracing.recordClockSyncMarker",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def request_memory_dump(
        self,
        params: RequestMemoryDumpParams | None = None,
        session_id: str | None = None,
    ) -> RequestMemoryDumpResult:
        """Request a global memory dump."""
        result = await self._client.send_raw(
            method="Tracing.requestMemoryDump",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return RequestMemoryDumpResult.model_validate(result)

    async def start(
        self, params: StartParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Start trace events collection."""
        result = await self._client.send_raw(
            method="Tracing.start",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
