"""Generated client library from CDP specification"""
# Domain: SystemInfo Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    GetFeatureStateParams,
    GetFeatureStateResult,
    GetInfoResult,
    GetProcessInfoResult,
)


class SystemInfoClient:
    """The SystemInfo domain defines methods and events for querying low-level system information."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def get_info(self, session_id: str | None = None) -> GetInfoResult:
        """Returns information about the system."""
        result = await self._client.send_raw(
            method="SystemInfo.getInfo",
            params=None,
            session_id=session_id,
        )
        return GetInfoResult.model_validate(result)

    async def get_feature_state(
        self, params: GetFeatureStateParams, session_id: str | None = None
    ) -> GetFeatureStateResult:
        """Returns information about the feature state."""
        result = await self._client.send_raw(
            method="SystemInfo.getFeatureState",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetFeatureStateResult.model_validate(result)

    async def get_process_info(
        self, session_id: str | None = None
    ) -> GetProcessInfoResult:
        """Returns information about all running processes."""
        result = await self._client.send_raw(
            method="SystemInfo.getProcessInfo",
            params=None,
            session_id=session_id,
        )
        return GetProcessInfoResult.model_validate(result)
