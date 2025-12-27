"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    EnableParams,
    SetSinkToUseParams,
    StartDesktopMirroringParams,
    StartTabMirroringParams,
    StopCastingParams,
)

class CastClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def enable(
        self, params: EnableParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Cast.enable",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Cast.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_sink_to_use(
        self, params: SetSinkToUseParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Cast.setSinkToUse",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def start_desktop_mirroring(
        self, params: StartDesktopMirroringParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Cast.startDesktopMirroring",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def start_tab_mirroring(
        self, params: StartTabMirroringParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Cast.startTabMirroring",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def stop_casting(
        self, params: StopCastingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Cast.stopCasting",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
