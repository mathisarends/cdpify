"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    CollectClassNamesFromSubtreeParams,
    CollectClassNamesFromSubtreeResult,
    CopyToParams,
    CopyToResult,
    DescribeNodeParams,
    DescribeNodeResult,
    DiscardSearchResultsParams,
    EnableParams,
    FocusParams,
    ForceShowPopoverParams,
    ForceShowPopoverResult,
    GetAnchorElementParams,
    GetAnchorElementResult,
    GetAttributesParams,
    GetAttributesResult,
    GetBoxModelParams,
    GetBoxModelResult,
    GetContainerForNodeParams,
    GetContainerForNodeResult,
    GetContentQuadsParams,
    GetContentQuadsResult,
    GetDetachedDomNodesResult,
    GetDocumentParams,
    GetDocumentResult,
    GetElementByRelationParams,
    GetElementByRelationResult,
    GetFileInfoParams,
    GetFileInfoResult,
    GetFlattenedDocumentParams,
    GetFlattenedDocumentResult,
    GetFrameOwnerParams,
    GetFrameOwnerResult,
    GetNodeForLocationParams,
    GetNodeForLocationResult,
    GetNodeStackTracesParams,
    GetNodeStackTracesResult,
    GetNodesForSubtreeByStyleParams,
    GetNodesForSubtreeByStyleResult,
    GetOuterHTMLParams,
    GetOuterHTMLResult,
    GetQueryingDescendantsForContainerParams,
    GetQueryingDescendantsForContainerResult,
    GetRelayoutBoundaryParams,
    GetRelayoutBoundaryResult,
    GetSearchResultsParams,
    GetSearchResultsResult,
    GetTopLayerElementsResult,
    MoveToParams,
    MoveToResult,
    PerformSearchParams,
    PerformSearchResult,
    PushNodeByPathToFrontendParams,
    PushNodeByPathToFrontendResult,
    PushNodesByBackendIdsToFrontendParams,
    PushNodesByBackendIdsToFrontendResult,
    QuerySelectorAllParams,
    QuerySelectorAllResult,
    QuerySelectorParams,
    QuerySelectorResult,
    RemoveAttributeParams,
    RemoveNodeParams,
    RequestChildNodesParams,
    RequestNodeParams,
    RequestNodeResult,
    ResolveNodeParams,
    ResolveNodeResult,
    ScrollIntoViewIfNeededParams,
    SetAttributeValueParams,
    SetAttributesAsTextParams,
    SetFileInputFilesParams,
    SetInspectedNodeParams,
    SetNodeNameParams,
    SetNodeNameResult,
    SetNodeStackTracesEnabledParams,
    SetNodeValueParams,
    SetOuterHTMLParams,
)

class DOMClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def collect_class_names_from_subtree(
        self, params: CollectClassNamesFromSubtreeParams, session_id: str | None = None
    ) -> CollectClassNamesFromSubtreeResult:
        result = await self._client.send_raw(
            method="DOM.collectClassNamesFromSubtree",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CollectClassNamesFromSubtreeResult.model_validate(result)

    async def copy_to(
        self, params: CopyToParams, session_id: str | None = None
    ) -> CopyToResult:
        result = await self._client.send_raw(
            method="DOM.copyTo",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CopyToResult.model_validate(result)

    async def describe_node(
        self, params: DescribeNodeParams | None = None, session_id: str | None = None
    ) -> DescribeNodeResult:
        result = await self._client.send_raw(
            method="DOM.describeNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return DescribeNodeResult.model_validate(result)

    async def scroll_into_view_if_needed(
        self, params: ScrollIntoViewIfNeededParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.scrollIntoViewIfNeeded",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def discard_search_results(
        self, params: DiscardSearchResultsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.discardSearchResults",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, params: EnableParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.enable",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def focus(
        self, params: FocusParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.focus",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_attributes(
        self, params: GetAttributesParams, session_id: str | None = None
    ) -> GetAttributesResult:
        result = await self._client.send_raw(
            method="DOM.getAttributes",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetAttributesResult.model_validate(result)

    async def get_box_model(
        self, params: GetBoxModelParams | None = None, session_id: str | None = None
    ) -> GetBoxModelResult:
        result = await self._client.send_raw(
            method="DOM.getBoxModel",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetBoxModelResult.model_validate(result)

    async def get_content_quads(
        self, params: GetContentQuadsParams | None = None, session_id: str | None = None
    ) -> GetContentQuadsResult:
        result = await self._client.send_raw(
            method="DOM.getContentQuads",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetContentQuadsResult.model_validate(result)

    async def get_document(
        self, params: GetDocumentParams | None = None, session_id: str | None = None
    ) -> GetDocumentResult:
        result = await self._client.send_raw(
            method="DOM.getDocument",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetDocumentResult.model_validate(result)

    async def get_flattened_document(
        self, params: GetFlattenedDocumentParams | None = None, session_id: str | None = None
    ) -> GetFlattenedDocumentResult:
        result = await self._client.send_raw(
            method="DOM.getFlattenedDocument",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetFlattenedDocumentResult.model_validate(result)

    async def get_nodes_for_subtree_by_style(
        self, params: GetNodesForSubtreeByStyleParams, session_id: str | None = None
    ) -> GetNodesForSubtreeByStyleResult:
        result = await self._client.send_raw(
            method="DOM.getNodesForSubtreeByStyle",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetNodesForSubtreeByStyleResult.model_validate(result)

    async def get_node_for_location(
        self, params: GetNodeForLocationParams, session_id: str | None = None
    ) -> GetNodeForLocationResult:
        result = await self._client.send_raw(
            method="DOM.getNodeForLocation",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetNodeForLocationResult.model_validate(result)

    async def get_outer_h_t_m_l(
        self, params: GetOuterHTMLParams | None = None, session_id: str | None = None
    ) -> GetOuterHTMLResult:
        result = await self._client.send_raw(
            method="DOM.getOuterHTML",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetOuterHTMLResult.model_validate(result)

    async def get_relayout_boundary(
        self, params: GetRelayoutBoundaryParams, session_id: str | None = None
    ) -> GetRelayoutBoundaryResult:
        result = await self._client.send_raw(
            method="DOM.getRelayoutBoundary",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetRelayoutBoundaryResult.model_validate(result)

    async def get_search_results(
        self, params: GetSearchResultsParams, session_id: str | None = None
    ) -> GetSearchResultsResult:
        result = await self._client.send_raw(
            method="DOM.getSearchResults",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetSearchResultsResult.model_validate(result)

    async def hide_highlight(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.hideHighlight",
            params=None,
            session_id=session_id,
        )
        return result

    async def highlight_node(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.highlightNode",
            params=None,
            session_id=session_id,
        )
        return result

    async def highlight_rect(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.highlightRect",
            params=None,
            session_id=session_id,
        )
        return result

    async def mark_undoable_state(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.markUndoableState",
            params=None,
            session_id=session_id,
        )
        return result

    async def move_to(
        self, params: MoveToParams, session_id: str | None = None
    ) -> MoveToResult:
        result = await self._client.send_raw(
            method="DOM.moveTo",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return MoveToResult.model_validate(result)

    async def perform_search(
        self, params: PerformSearchParams, session_id: str | None = None
    ) -> PerformSearchResult:
        result = await self._client.send_raw(
            method="DOM.performSearch",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return PerformSearchResult.model_validate(result)

    async def push_node_by_path_to_frontend(
        self, params: PushNodeByPathToFrontendParams, session_id: str | None = None
    ) -> PushNodeByPathToFrontendResult:
        result = await self._client.send_raw(
            method="DOM.pushNodeByPathToFrontend",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return PushNodeByPathToFrontendResult.model_validate(result)

    async def push_nodes_by_backend_ids_to_frontend(
        self, params: PushNodesByBackendIdsToFrontendParams, session_id: str | None = None
    ) -> PushNodesByBackendIdsToFrontendResult:
        result = await self._client.send_raw(
            method="DOM.pushNodesByBackendIdsToFrontend",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return PushNodesByBackendIdsToFrontendResult.model_validate(result)

    async def query_selector(
        self, params: QuerySelectorParams, session_id: str | None = None
    ) -> QuerySelectorResult:
        result = await self._client.send_raw(
            method="DOM.querySelector",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return QuerySelectorResult.model_validate(result)

    async def query_selector_all(
        self, params: QuerySelectorAllParams, session_id: str | None = None
    ) -> QuerySelectorAllResult:
        result = await self._client.send_raw(
            method="DOM.querySelectorAll",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return QuerySelectorAllResult.model_validate(result)

    async def get_top_layer_elements(
        self, session_id: str | None = None
    ) -> GetTopLayerElementsResult:
        result = await self._client.send_raw(
            method="DOM.getTopLayerElements",
            params=None,
            session_id=session_id,
        )
        return GetTopLayerElementsResult.model_validate(result)

    async def get_element_by_relation(
        self, params: GetElementByRelationParams, session_id: str | None = None
    ) -> GetElementByRelationResult:
        result = await self._client.send_raw(
            method="DOM.getElementByRelation",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetElementByRelationResult.model_validate(result)

    async def redo(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.redo",
            params=None,
            session_id=session_id,
        )
        return result

    async def remove_attribute(
        self, params: RemoveAttributeParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.removeAttribute",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def remove_node(
        self, params: RemoveNodeParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.removeNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def request_child_nodes(
        self, params: RequestChildNodesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.requestChildNodes",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def request_node(
        self, params: RequestNodeParams, session_id: str | None = None
    ) -> RequestNodeResult:
        result = await self._client.send_raw(
            method="DOM.requestNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return RequestNodeResult.model_validate(result)

    async def resolve_node(
        self, params: ResolveNodeParams | None = None, session_id: str | None = None
    ) -> ResolveNodeResult:
        result = await self._client.send_raw(
            method="DOM.resolveNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return ResolveNodeResult.model_validate(result)

    async def set_attribute_value(
        self, params: SetAttributeValueParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.setAttributeValue",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_attributes_as_text(
        self, params: SetAttributesAsTextParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.setAttributesAsText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_file_input_files(
        self, params: SetFileInputFilesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.setFileInputFiles",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_node_stack_traces_enabled(
        self, params: SetNodeStackTracesEnabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.setNodeStackTracesEnabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_node_stack_traces(
        self, params: GetNodeStackTracesParams, session_id: str | None = None
    ) -> GetNodeStackTracesResult:
        result = await self._client.send_raw(
            method="DOM.getNodeStackTraces",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetNodeStackTracesResult.model_validate(result)

    async def get_file_info(
        self, params: GetFileInfoParams, session_id: str | None = None
    ) -> GetFileInfoResult:
        result = await self._client.send_raw(
            method="DOM.getFileInfo",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetFileInfoResult.model_validate(result)

    async def get_detached_dom_nodes(
        self, session_id: str | None = None
    ) -> GetDetachedDomNodesResult:
        result = await self._client.send_raw(
            method="DOM.getDetachedDomNodes",
            params=None,
            session_id=session_id,
        )
        return GetDetachedDomNodesResult.model_validate(result)

    async def set_inspected_node(
        self, params: SetInspectedNodeParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.setInspectedNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_node_name(
        self, params: SetNodeNameParams, session_id: str | None = None
    ) -> SetNodeNameResult:
        result = await self._client.send_raw(
            method="DOM.setNodeName",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetNodeNameResult.model_validate(result)

    async def set_node_value(
        self, params: SetNodeValueParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.setNodeValue",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_outer_h_t_m_l(
        self, params: SetOuterHTMLParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.setOuterHTML",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def undo(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="DOM.undo",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_frame_owner(
        self, params: GetFrameOwnerParams, session_id: str | None = None
    ) -> GetFrameOwnerResult:
        result = await self._client.send_raw(
            method="DOM.getFrameOwner",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetFrameOwnerResult.model_validate(result)

    async def get_container_for_node(
        self, params: GetContainerForNodeParams, session_id: str | None = None
    ) -> GetContainerForNodeResult:
        result = await self._client.send_raw(
            method="DOM.getContainerForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetContainerForNodeResult.model_validate(result)

    async def get_querying_descendants_for_container(
        self, params: GetQueryingDescendantsForContainerParams, session_id: str | None = None
    ) -> GetQueryingDescendantsForContainerResult:
        result = await self._client.send_raw(
            method="DOM.getQueryingDescendantsForContainer",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetQueryingDescendantsForContainerResult.model_validate(result)

    async def get_anchor_element(
        self, params: GetAnchorElementParams, session_id: str | None = None
    ) -> GetAnchorElementResult:
        result = await self._client.send_raw(
            method="DOM.getAnchorElement",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetAnchorElementResult.model_validate(result)

    async def force_show_popover(
        self, params: ForceShowPopoverParams, session_id: str | None = None
    ) -> ForceShowPopoverResult:
        result = await self._client.send_raw(
            method="DOM.forceShowPopover",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return ForceShowPopoverResult.model_validate(result)
