"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    BindParams,
    UnbindParams,
)

class TetheringClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def bind(
        self, params: BindParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Tethering.bind",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def unbind(
        self, params: UnbindParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Tethering.unbind",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
