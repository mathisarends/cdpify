"""Generated client library from CDP specification"""
# Domain: Schema Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    GetDomainsResult,
)


class SchemaClient:
    """This domain is deprecated."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def get_domains(self, session_id: str | None = None) -> GetDomainsResult:
        """Returns supported domains."""
        result = await self._client.send_raw(
            method="Schema.getDomains",
            params=None,
            session_id=session_id,
        )
        return GetDomainsResult.model_validate(result)
