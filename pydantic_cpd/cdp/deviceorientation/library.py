"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    SetDeviceOrientationOverrideParams,
)

class DeviceOrientationClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def clear_device_orientation_override(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DeviceOrientation.clearDeviceOrientationOverride",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_device_orientation_override(
        self, params: SetDeviceOrientationOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DeviceOrientation.setDeviceOrientationOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
