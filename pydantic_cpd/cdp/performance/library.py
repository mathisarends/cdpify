"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    EnableParams,
    GetMetricsResult,
    SetTimeDomainParams,
)

class PerformanceClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Performance.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, params: EnableParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Performance.enable",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_time_domain(
        self, params: SetTimeDomainParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Performance.setTimeDomain",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_metrics(
        self, session_id: str | None = None
    ) -> GetMetricsResult:
        result = await self._client.send_raw(
            method="Performance.getMetrics",
            params=None,
            session_id=session_id,
        )
        return GetMetricsResult.model_validate(result)
