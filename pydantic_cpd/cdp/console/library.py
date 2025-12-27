"""Generated client library from CDP specification"""
# Domain: Console Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient


class ConsoleClient:
    """This domain is deprecated - use Runtime or Log instead."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def clear_messages(self, session_id: str | None = None) -> dict[str, Any]:
        """Does nothing."""
        result = await self._client.send_raw(
            method="Console.clearMessages",
            params=None,
            session_id=session_id,
        )
        return result

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables console domain, prevents further console messages from being reported to the client."""
        result = await self._client.send_raw(
            method="Console.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        """Enables console domain, sends the messages collected so far to the client by means of the
        `messageAdded` notification."""
        result = await self._client.send_raw(
            method="Console.enable",
            params=None,
            session_id=session_id,
        )
        return result
