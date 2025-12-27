"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    GetBestEffortCoverageResult,
    SetSamplingIntervalParams,
    StartPreciseCoverageParams,
    StartPreciseCoverageResult,
    StopResult,
    TakePreciseCoverageResult,
)

class ProfilerClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Profiler.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Profiler.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_best_effort_coverage(
        self, session_id: str | None = None
    ) -> GetBestEffortCoverageResult:
        result = await self._client.send_raw(
            method="Profiler.getBestEffortCoverage",
            params=None,
            session_id=session_id,
        )
        return GetBestEffortCoverageResult.model_validate(result)

    async def set_sampling_interval(
        self, params: SetSamplingIntervalParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Profiler.setSamplingInterval",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def start(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Profiler.start",
            params=None,
            session_id=session_id,
        )
        return result

    async def start_precise_coverage(
        self, params: StartPreciseCoverageParams | None = None, session_id: str | None = None
    ) -> StartPreciseCoverageResult:
        result = await self._client.send_raw(
            method="Profiler.startPreciseCoverage",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return StartPreciseCoverageResult.model_validate(result)

    async def stop(
        self, session_id: str | None = None
    ) -> StopResult:
        result = await self._client.send_raw(
            method="Profiler.stop",
            params=None,
            session_id=session_id,
        )
        return StopResult.model_validate(result)

    async def stop_precise_coverage(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Profiler.stopPreciseCoverage",
            params=None,
            session_id=session_id,
        )
        return result

    async def take_precise_coverage(
        self, session_id: str | None = None
    ) -> TakePreciseCoverageResult:
        result = await self._client.send_raw(
            method="Profiler.takePreciseCoverage",
            params=None,
            session_id=session_id,
        )
        return TakePreciseCoverageResult.model_validate(result)
