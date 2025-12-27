"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    GetAllTimeSamplingProfileResult,
    GetBrowserSamplingProfileResult,
    GetDOMCountersForLeakDetectionResult,
    GetDOMCountersResult,
    GetSamplingProfileResult,
    SetPressureNotificationsSuppressedParams,
    SimulatePressureNotificationParams,
    StartSamplingParams,
)

class MemoryClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def get_d_o_m_counters(
        self, session_id: str | None = None
    ) -> GetDOMCountersResult:
        result = await self._client.send_raw(
            method="Memory.getDOMCounters",
            params=None,
            session_id=session_id,
        )
        return GetDOMCountersResult.model_validate(result)

    async def get_d_o_m_counters_for_leak_detection(
        self, session_id: str | None = None
    ) -> GetDOMCountersForLeakDetectionResult:
        result = await self._client.send_raw(
            method="Memory.getDOMCountersForLeakDetection",
            params=None,
            session_id=session_id,
        )
        return GetDOMCountersForLeakDetectionResult.model_validate(result)

    async def prepare_for_leak_detection(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Memory.prepareForLeakDetection",
            params=None,
            session_id=session_id,
        )
        return result

    async def forcibly_purge_java_script_memory(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Memory.forciblyPurgeJavaScriptMemory",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_pressure_notifications_suppressed(
        self, params: SetPressureNotificationsSuppressedParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Memory.setPressureNotificationsSuppressed",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def simulate_pressure_notification(
        self, params: SimulatePressureNotificationParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Memory.simulatePressureNotification",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def start_sampling(
        self, params: StartSamplingParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Memory.startSampling",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def stop_sampling(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Memory.stopSampling",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_all_time_sampling_profile(
        self, session_id: str | None = None
    ) -> GetAllTimeSamplingProfileResult:
        result = await self._client.send_raw(
            method="Memory.getAllTimeSamplingProfile",
            params=None,
            session_id=session_id,
        )
        return GetAllTimeSamplingProfileResult.model_validate(result)

    async def get_browser_sampling_profile(
        self, session_id: str | None = None
    ) -> GetBrowserSamplingProfileResult:
        result = await self._client.send_raw(
            method="Memory.getBrowserSamplingProfile",
            params=None,
            session_id=session_id,
        )
        return GetBrowserSamplingProfileResult.model_validate(result)

    async def get_sampling_profile(
        self, session_id: str | None = None
    ) -> GetSamplingProfileResult:
        result = await self._client.send_raw(
            method="Memory.getSamplingProfile",
            params=None,
            session_id=session_id,
        )
        return GetSamplingProfileResult.model_validate(result)
