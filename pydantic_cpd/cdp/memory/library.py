"""Generated client library from CDP specification"""
# Domain: Memory Client

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
    """CDP Memory domain client."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def get_d_o_m_counters(
        self, session_id: str | None = None
    ) -> GetDOMCountersResult:
        """Retruns current DOM object counters."""
        result = await self._client.send_raw(
            method="Memory.getDOMCounters",
            params=None,
            session_id=session_id,
        )
        return GetDOMCountersResult.model_validate(result)

    async def get_d_o_m_counters_for_leak_detection(
        self, session_id: str | None = None
    ) -> GetDOMCountersForLeakDetectionResult:
        """Retruns DOM object counters after preparing renderer for leak detection."""
        result = await self._client.send_raw(
            method="Memory.getDOMCountersForLeakDetection",
            params=None,
            session_id=session_id,
        )
        return GetDOMCountersForLeakDetectionResult.model_validate(result)

    async def prepare_for_leak_detection(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        """Prepares for leak detection by terminating workers, stopping spellcheckers,
        dropping non-essential internal caches, running garbage collections, etc."""
        result = await self._client.send_raw(
            method="Memory.prepareForLeakDetection",
            params=None,
            session_id=session_id,
        )
        return result

    async def forcibly_purge_java_script_memory(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        """Simulate OomIntervention by purging V8 memory."""
        result = await self._client.send_raw(
            method="Memory.forciblyPurgeJavaScriptMemory",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_pressure_notifications_suppressed(
        self,
        params: SetPressureNotificationsSuppressedParams,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Enable/disable suppressing memory pressure notifications in all processes."""
        result = await self._client.send_raw(
            method="Memory.setPressureNotificationsSuppressed",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def simulate_pressure_notification(
        self, params: SimulatePressureNotificationParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Simulate a memory pressure notification in all processes."""
        result = await self._client.send_raw(
            method="Memory.simulatePressureNotification",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def start_sampling(
        self, params: StartSamplingParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Start collecting native memory profile."""
        result = await self._client.send_raw(
            method="Memory.startSampling",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def stop_sampling(self, session_id: str | None = None) -> dict[str, Any]:
        """Stop collecting native memory profile."""
        result = await self._client.send_raw(
            method="Memory.stopSampling",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_all_time_sampling_profile(
        self, session_id: str | None = None
    ) -> GetAllTimeSamplingProfileResult:
        """Retrieve native memory allocations profile
        collected since renderer process startup."""
        result = await self._client.send_raw(
            method="Memory.getAllTimeSamplingProfile",
            params=None,
            session_id=session_id,
        )
        return GetAllTimeSamplingProfileResult.model_validate(result)

    async def get_browser_sampling_profile(
        self, session_id: str | None = None
    ) -> GetBrowserSamplingProfileResult:
        """Retrieve native memory allocations profile
        collected since browser process startup."""
        result = await self._client.send_raw(
            method="Memory.getBrowserSamplingProfile",
            params=None,
            session_id=session_id,
        )
        return GetBrowserSamplingProfileResult.model_validate(result)

    async def get_sampling_profile(
        self, session_id: str | None = None
    ) -> GetSamplingProfileResult:
        """Retrieve native memory allocations profile collected since last
        `startSampling` call."""
        result = await self._client.send_raw(
            method="Memory.getSamplingProfile",
            params=None,
            session_id=session_id,
        )
        return GetSamplingProfileResult.model_validate(result)
