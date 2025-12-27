"""Generated client library from CDP specification"""
# Domain: DOMStorage Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    ClearParams,
    GetDOMStorageItemsParams,
    GetDOMStorageItemsResult,
    RemoveDOMStorageItemParams,
    SetDOMStorageItemParams,
)


class DOMStorageClient:
    """Query and modify DOM storage."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def clear(
        self, params: ClearParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMStorage.clear",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables storage tracking, prevents storage events from being sent to the client."""
        result = await self._client.send_raw(
            method="DOMStorage.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        """Enables storage tracking, storage events will now be delivered to the client."""
        result = await self._client.send_raw(
            method="DOMStorage.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_d_o_m_storage_items(
        self, params: GetDOMStorageItemsParams, session_id: str | None = None
    ) -> GetDOMStorageItemsResult:
        result = await self._client.send_raw(
            method="DOMStorage.getDOMStorageItems",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetDOMStorageItemsResult.model_validate(result)

    async def remove_d_o_m_storage_item(
        self, params: RemoveDOMStorageItemParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMStorage.removeDOMStorageItem",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_d_o_m_storage_item(
        self, params: SetDOMStorageItemParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOMStorage.setDOMStorageItem",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
