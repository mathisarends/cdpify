"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    GetRealtimeDataParams,
    GetRealtimeDataResult,
)

class WebAudioClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def enable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="WebAudio.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="WebAudio.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_realtime_data(
        self, params: GetRealtimeDataParams, session_id: str | None = None
    ) -> GetRealtimeDataResult:
        result = await self._client.send_raw(
            method="WebAudio.getRealtimeData",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetRealtimeDataResult.model_validate(result)
