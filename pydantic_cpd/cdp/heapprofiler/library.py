"""Generated client library from CDP specification"""
# Domain: HeapProfiler Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    AddInspectedHeapObjectParams,
    GetHeapObjectIdParams,
    GetHeapObjectIdResult,
    GetObjectByHeapObjectIdParams,
    GetObjectByHeapObjectIdResult,
    GetSamplingProfileResult,
    StartSamplingParams,
    StartTrackingHeapObjectsParams,
    StopSamplingResult,
    StopTrackingHeapObjectsParams,
    TakeHeapSnapshotParams,
)


class HeapProfilerClient:
    """CDP HeapProfiler domain client."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def add_inspected_heap_object(
        self, params: AddInspectedHeapObjectParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enables console to refer to the node with given id via $x (see Command Line API for more details
        $x functions)."""
        result = await self._client.send_raw(
            method="HeapProfiler.addInspectedHeapObject",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def collect_garbage(self, session_id: str | None = None) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="HeapProfiler.collectGarbage",
            params=None,
            session_id=session_id,
        )
        return result

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="HeapProfiler.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="HeapProfiler.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_heap_object_id(
        self, params: GetHeapObjectIdParams, session_id: str | None = None
    ) -> GetHeapObjectIdResult:
        result = await self._client.send_raw(
            method="HeapProfiler.getHeapObjectId",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetHeapObjectIdResult.model_validate(result)

    async def get_object_by_heap_object_id(
        self, params: GetObjectByHeapObjectIdParams, session_id: str | None = None
    ) -> GetObjectByHeapObjectIdResult:
        result = await self._client.send_raw(
            method="HeapProfiler.getObjectByHeapObjectId",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetObjectByHeapObjectIdResult.model_validate(result)

    async def get_sampling_profile(
        self, session_id: str | None = None
    ) -> GetSamplingProfileResult:
        result = await self._client.send_raw(
            method="HeapProfiler.getSamplingProfile",
            params=None,
            session_id=session_id,
        )
        return GetSamplingProfileResult.model_validate(result)

    async def start_sampling(
        self, params: StartSamplingParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="HeapProfiler.startSampling",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def start_tracking_heap_objects(
        self,
        params: StartTrackingHeapObjectsParams | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="HeapProfiler.startTrackingHeapObjects",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def stop_sampling(self, session_id: str | None = None) -> StopSamplingResult:
        result = await self._client.send_raw(
            method="HeapProfiler.stopSampling",
            params=None,
            session_id=session_id,
        )
        return StopSamplingResult.model_validate(result)

    async def stop_tracking_heap_objects(
        self,
        params: StopTrackingHeapObjectsParams | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="HeapProfiler.stopTrackingHeapObjects",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def take_heap_snapshot(
        self,
        params: TakeHeapSnapshotParams | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="HeapProfiler.takeHeapSnapshot",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
