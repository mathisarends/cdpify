"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    GetAXNodeAndAncestorsParams,
    GetAXNodeAndAncestorsResult,
    GetChildAXNodesParams,
    GetChildAXNodesResult,
    GetFullAXTreeParams,
    GetFullAXTreeResult,
    GetPartialAXTreeParams,
    GetPartialAXTreeResult,
    GetRootAXNodeParams,
    GetRootAXNodeResult,
    QueryAXTreeParams,
    QueryAXTreeResult,
)

class AccessibilityClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Accessibility.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Accessibility.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_partial_a_x_tree(
        self, params: GetPartialAXTreeParams | None = None, session_id: str | None = None
    ) -> GetPartialAXTreeResult:
        result = await self._client.send_raw(
            method="Accessibility.getPartialAXTree",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetPartialAXTreeResult.model_validate(result)

    async def get_full_a_x_tree(
        self, params: GetFullAXTreeParams | None = None, session_id: str | None = None
    ) -> GetFullAXTreeResult:
        result = await self._client.send_raw(
            method="Accessibility.getFullAXTree",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetFullAXTreeResult.model_validate(result)

    async def get_root_a_x_node(
        self, params: GetRootAXNodeParams | None = None, session_id: str | None = None
    ) -> GetRootAXNodeResult:
        result = await self._client.send_raw(
            method="Accessibility.getRootAXNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetRootAXNodeResult.model_validate(result)

    async def get_a_x_node_and_ancestors(
        self, params: GetAXNodeAndAncestorsParams | None = None, session_id: str | None = None
    ) -> GetAXNodeAndAncestorsResult:
        result = await self._client.send_raw(
            method="Accessibility.getAXNodeAndAncestors",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetAXNodeAndAncestorsResult.model_validate(result)

    async def get_child_a_x_nodes(
        self, params: GetChildAXNodesParams, session_id: str | None = None
    ) -> GetChildAXNodesResult:
        result = await self._client.send_raw(
            method="Accessibility.getChildAXNodes",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetChildAXNodesResult.model_validate(result)

    async def query_a_x_tree(
        self, params: QueryAXTreeParams | None = None, session_id: str | None = None
    ) -> QueryAXTreeResult:
        result = await self._client.send_raw(
            method="Accessibility.queryAXTree",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return QueryAXTreeResult.model_validate(result)
