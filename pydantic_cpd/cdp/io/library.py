"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    CloseParams,
    ReadParams,
    ReadResult,
    ResolveBlobParams,
    ResolveBlobResult,
)

class IOClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def close(
        self, params: CloseParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="IO.close",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def read(
        self, params: ReadParams, session_id: str | None = None
    ) -> ReadResult:
        result = await self._client.send_raw(
            method="IO.read",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return ReadResult.model_validate(result)

    async def resolve_blob(
        self, params: ResolveBlobParams, session_id: str | None = None
    ) -> ResolveBlobResult:
        result = await self._client.send_raw(
            method="IO.resolveBlob",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return ResolveBlobResult.model_validate(result)
