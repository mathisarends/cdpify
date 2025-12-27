"""Generated client library from CDP specification"""
# Domain: Tethering Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    BindParams,
    UnbindParams,
)


class TetheringClient:
    """The Tethering domain defines methods and events for browser port binding."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def bind(
        self, params: BindParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Request browser port binding."""
        result = await self._client.send_raw(
            method="Tethering.bind",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def unbind(
        self, params: UnbindParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Request browser port unbinding."""
        result = await self._client.send_raw(
            method="Tethering.unbind",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
