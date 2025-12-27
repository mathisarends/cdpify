"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    ClearEventsParams,
    SetRecordingParams,
    StartObservingParams,
    StopObservingParams,
)

class BackgroundServiceClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def start_observing(
        self, params: StartObservingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="BackgroundService.startObserving",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def stop_observing(
        self, params: StopObservingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="BackgroundService.stopObserving",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_recording(
        self, params: SetRecordingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="BackgroundService.setRecording",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def clear_events(
        self, params: ClearEventsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="BackgroundService.clearEvents",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
