"""Generated client library from CDP specification"""
# Domain: Profiler Client

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
    """CDP Profiler domain client."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Profiler.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Profiler.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_best_effort_coverage(
        self, session_id: str | None = None
    ) -> GetBestEffortCoverageResult:
        """Collect coverage data for the current isolate. The coverage data may be incomplete due to
        garbage collection."""
        result = await self._client.send_raw(
            method="Profiler.getBestEffortCoverage",
            params=None,
            session_id=session_id,
        )
        return GetBestEffortCoverageResult.model_validate(result)

    async def set_sampling_interval(
        self, params: SetSamplingIntervalParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Changes CPU profiler sampling interval. Must be called before CPU profiles recording started."""
        result = await self._client.send_raw(
            method="Profiler.setSamplingInterval",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def start(self, session_id: str | None = None) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Profiler.start",
            params=None,
            session_id=session_id,
        )
        return result

    async def start_precise_coverage(
        self,
        params: StartPreciseCoverageParams | None = None,
        session_id: str | None = None,
    ) -> StartPreciseCoverageResult:
        """Enable precise code coverage. Coverage data for JavaScript executed before enabling precise code
        coverage may be incomplete. Enabling prevents running optimized code and resets execution
        counters."""
        result = await self._client.send_raw(
            method="Profiler.startPreciseCoverage",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return StartPreciseCoverageResult.model_validate(result)

    async def stop(self, session_id: str | None = None) -> StopResult:
        result = await self._client.send_raw(
            method="Profiler.stop",
            params=None,
            session_id=session_id,
        )
        return StopResult.model_validate(result)

    async def stop_precise_coverage(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        """Disable precise code coverage. Disabling releases unnecessary execution count records and allows
        executing optimized code."""
        result = await self._client.send_raw(
            method="Profiler.stopPreciseCoverage",
            params=None,
            session_id=session_id,
        )
        return result

    async def take_precise_coverage(
        self, session_id: str | None = None
    ) -> TakePreciseCoverageResult:
        """Collect coverage data for the current isolate, and resets execution counters. Precise code
        coverage needs to have started."""
        result = await self._client.send_raw(
            method="Profiler.takePreciseCoverage",
            params=None,
            session_id=session_id,
        )
        return TakePreciseCoverageResult.model_validate(result)
