"""Generated client library from CDP specification"""
# Domain: CacheStorage Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    DeleteCacheParams,
    DeleteEntryParams,
    RequestCacheNamesParams,
    RequestCacheNamesResult,
    RequestCachedResponseParams,
    RequestCachedResponseResult,
    RequestEntriesParams,
    RequestEntriesResult,
)


class CacheStorageClient:
    """CDP CacheStorage domain client."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def delete_cache(
        self, params: DeleteCacheParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Deletes a cache."""
        result = await self._client.send_raw(
            method="CacheStorage.deleteCache",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def delete_entry(
        self, params: DeleteEntryParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Deletes a cache entry."""
        result = await self._client.send_raw(
            method="CacheStorage.deleteEntry",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def request_cache_names(
        self,
        params: RequestCacheNamesParams | None = None,
        session_id: str | None = None,
    ) -> RequestCacheNamesResult:
        """Requests cache names."""
        result = await self._client.send_raw(
            method="CacheStorage.requestCacheNames",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return RequestCacheNamesResult.model_validate(result)

    async def request_cached_response(
        self, params: RequestCachedResponseParams, session_id: str | None = None
    ) -> RequestCachedResponseResult:
        """Fetches cache entry."""
        result = await self._client.send_raw(
            method="CacheStorage.requestCachedResponse",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return RequestCachedResponseResult.model_validate(result)

    async def request_entries(
        self, params: RequestEntriesParams, session_id: str | None = None
    ) -> RequestEntriesResult:
        """Requests data from cache."""
        result = await self._client.send_raw(
            method="CacheStorage.requestEntries",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return RequestEntriesResult.model_validate(result)
