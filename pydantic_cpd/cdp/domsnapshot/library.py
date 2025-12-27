"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    CaptureSnapshotParams,
    CaptureSnapshotResult,
    GetSnapshotParams,
    GetSnapshotResult,
)

class DOMSnapshotClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMSnapshot.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMSnapshot.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_snapshot(
        self, params: GetSnapshotParams, session_id: str | None = None
    ) -> GetSnapshotResult:
        result = await self._client.send_raw(
            method="DOMSnapshot.getSnapshot",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetSnapshotResult.model_validate(result)

    async def capture_snapshot(
        self, params: CaptureSnapshotParams, session_id: str | None = None
    ) -> CaptureSnapshotResult:
        result = await self._client.send_raw(
            method="DOMSnapshot.captureSnapshot",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CaptureSnapshotResult.model_validate(result)
