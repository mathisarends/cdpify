"""Generated client library from CDP specification"""
# Domain: IndexedDB Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    ClearObjectStoreParams,
    DeleteDatabaseParams,
    DeleteObjectStoreEntriesParams,
    GetMetadataParams,
    GetMetadataResult,
    RequestDataParams,
    RequestDataResult,
    RequestDatabaseNamesParams,
    RequestDatabaseNamesResult,
    RequestDatabaseParams,
    RequestDatabaseResult,
)


class IndexedDBClient:
    """CDP IndexedDB domain client."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def clear_object_store(
        self, params: ClearObjectStoreParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Clears all entries from an object store."""
        result = await self._client.send_raw(
            method="IndexedDB.clearObjectStore",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def delete_database(
        self, params: DeleteDatabaseParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Deletes a database."""
        result = await self._client.send_raw(
            method="IndexedDB.deleteDatabase",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def delete_object_store_entries(
        self, params: DeleteObjectStoreEntriesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Delete a range of entries from an object store"""
        result = await self._client.send_raw(
            method="IndexedDB.deleteObjectStoreEntries",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables events from backend."""
        result = await self._client.send_raw(
            method="IndexedDB.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        """Enables events from backend."""
        result = await self._client.send_raw(
            method="IndexedDB.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def request_data(
        self, params: RequestDataParams, session_id: str | None = None
    ) -> RequestDataResult:
        """Requests data from object store or index."""
        result = await self._client.send_raw(
            method="IndexedDB.requestData",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return RequestDataResult.model_validate(result)

    async def get_metadata(
        self, params: GetMetadataParams, session_id: str | None = None
    ) -> GetMetadataResult:
        """Gets metadata of an object store."""
        result = await self._client.send_raw(
            method="IndexedDB.getMetadata",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetMetadataResult.model_validate(result)

    async def request_database(
        self, params: RequestDatabaseParams, session_id: str | None = None
    ) -> RequestDatabaseResult:
        """Requests database with given name in given frame."""
        result = await self._client.send_raw(
            method="IndexedDB.requestDatabase",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return RequestDatabaseResult.model_validate(result)

    async def request_database_names(
        self,
        params: RequestDatabaseNamesParams | None = None,
        session_id: str | None = None,
    ) -> RequestDatabaseNamesResult:
        """Requests database names for given security origin."""
        result = await self._client.send_raw(
            method="IndexedDB.requestDatabaseNames",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return RequestDatabaseNamesResult.model_validate(result)
