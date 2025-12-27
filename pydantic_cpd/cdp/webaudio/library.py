"""Generated client library from CDP specification"""
# Domain: WebAudio Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    GetRealtimeDataParams,
    GetRealtimeDataResult,
)


class WebAudioClient:
    """This domain allows inspection of Web Audio API.
    https://webaudio.github.io/web-audio-api/"""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        """Enables the WebAudio domain and starts sending context lifetime events."""
        result = await self._client.send_raw(
            method="WebAudio.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables the WebAudio domain."""
        result = await self._client.send_raw(
            method="WebAudio.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_realtime_data(
        self, params: GetRealtimeDataParams, session_id: str | None = None
    ) -> GetRealtimeDataResult:
        """Fetch the realtime data from the registered contexts."""
        result = await self._client.send_raw(
            method="WebAudio.getRealtimeData",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetRealtimeDataResult.model_validate(result)
