"""Generated client library from CDP specification"""
# Domain: Media Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient


class MediaClient:
    """This domain allows detailed inspection of media elements."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        """Enables the Media domain"""
        result = await self._client.send_raw(
            method="Media.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables the Media domain."""
        result = await self._client.send_raw(
            method="Media.disable",
            params=None,
            session_id=session_id,
        )
        return result
