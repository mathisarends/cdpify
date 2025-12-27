"""Generated client library from CDP specification"""
# Domain: Overlay Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    GetGridHighlightObjectsForTestParams,
    GetGridHighlightObjectsForTestResult,
    GetHighlightObjectForTestParams,
    GetHighlightObjectForTestResult,
    GetSourceOrderHighlightObjectForTestParams,
    GetSourceOrderHighlightObjectForTestResult,
    HighlightFrameParams,
    HighlightNodeParams,
    HighlightQuadParams,
    HighlightRectParams,
    HighlightSourceOrderParams,
    SetInspectModeParams,
    SetPausedInDebuggerMessageParams,
    SetShowAdHighlightsParams,
    SetShowContainerQueryOverlaysParams,
    SetShowDebugBordersParams,
    SetShowFPSCounterParams,
    SetShowFlexOverlaysParams,
    SetShowGridOverlaysParams,
    SetShowHingeParams,
    SetShowHitTestBordersParams,
    SetShowIsolatedElementsParams,
    SetShowLayoutShiftRegionsParams,
    SetShowPaintRectsParams,
    SetShowScrollBottleneckRectsParams,
    SetShowScrollSnapOverlaysParams,
    SetShowViewportSizeOnResizeParams,
    SetShowWebVitalsParams,
    SetShowWindowControlsOverlayParams,
)


class OverlayClient:
    """This domain provides various functionality related to drawing atop the inspected page."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables domain notifications."""
        result = await self._client.send_raw(
            method="Overlay.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        """Enables domain notifications."""
        result = await self._client.send_raw(
            method="Overlay.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_highlight_object_for_test(
        self, params: GetHighlightObjectForTestParams, session_id: str | None = None
    ) -> GetHighlightObjectForTestResult:
        """For testing."""
        result = await self._client.send_raw(
            method="Overlay.getHighlightObjectForTest",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetHighlightObjectForTestResult.model_validate(result)

    async def get_grid_highlight_objects_for_test(
        self,
        params: GetGridHighlightObjectsForTestParams,
        session_id: str | None = None,
    ) -> GetGridHighlightObjectsForTestResult:
        """For Persistent Grid testing."""
        result = await self._client.send_raw(
            method="Overlay.getGridHighlightObjectsForTest",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetGridHighlightObjectsForTestResult.model_validate(result)

    async def get_source_order_highlight_object_for_test(
        self,
        params: GetSourceOrderHighlightObjectForTestParams,
        session_id: str | None = None,
    ) -> GetSourceOrderHighlightObjectForTestResult:
        """For Source Order Viewer testing."""
        result = await self._client.send_raw(
            method="Overlay.getSourceOrderHighlightObjectForTest",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetSourceOrderHighlightObjectForTestResult.model_validate(result)

    async def hide_highlight(self, session_id: str | None = None) -> dict[str, Any]:
        """Hides any highlight."""
        result = await self._client.send_raw(
            method="Overlay.hideHighlight",
            params=None,
            session_id=session_id,
        )
        return result

    async def highlight_frame(
        self, params: HighlightFrameParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Highlights owner element of the frame with given id.
        Deprecated: Doesn't work reliably and cannot be fixed due to process
        separation (the owner node might be in a different process). Determine
        the owner node in the client and use highlightNode."""
        result = await self._client.send_raw(
            method="Overlay.highlightFrame",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def highlight_node(
        self, params: HighlightNodeParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Highlights DOM node with given id or with the given JavaScript object wrapper. Either nodeId or
        objectId must be specified."""
        result = await self._client.send_raw(
            method="Overlay.highlightNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def highlight_quad(
        self, params: HighlightQuadParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Highlights given quad. Coordinates are absolute with respect to the main frame viewport."""
        result = await self._client.send_raw(
            method="Overlay.highlightQuad",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def highlight_rect(
        self, params: HighlightRectParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Highlights given rectangle. Coordinates are absolute with respect to the main frame viewport.
        Issue: the method does not handle device pixel ratio (DPR) correctly.
        The coordinates currently have to be adjusted by the client
        if DPR is not 1 (see crbug.com/437807128)."""
        result = await self._client.send_raw(
            method="Overlay.highlightRect",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def highlight_source_order(
        self, params: HighlightSourceOrderParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Highlights the source order of the children of the DOM node with given id or with the given
        JavaScript object wrapper. Either nodeId or objectId must be specified."""
        result = await self._client.send_raw(
            method="Overlay.highlightSourceOrder",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_inspect_mode(
        self, params: SetInspectModeParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enters the 'inspect' mode. In this mode, elements that user is hovering over are highlighted.
        Backend then generates 'inspectNodeRequested' event upon element selection."""
        result = await self._client.send_raw(
            method="Overlay.setInspectMode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_ad_highlights(
        self, params: SetShowAdHighlightsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Highlights owner element of all frames detected to be ads."""
        result = await self._client.send_raw(
            method="Overlay.setShowAdHighlights",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_paused_in_debugger_message(
        self,
        params: SetPausedInDebuggerMessageParams | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Overlay.setPausedInDebuggerMessage",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_debug_borders(
        self, params: SetShowDebugBordersParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Requests that backend shows debug borders on layers"""
        result = await self._client.send_raw(
            method="Overlay.setShowDebugBorders",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_f_p_s_counter(
        self, params: SetShowFPSCounterParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Requests that backend shows the FPS counter"""
        result = await self._client.send_raw(
            method="Overlay.setShowFPSCounter",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_grid_overlays(
        self, params: SetShowGridOverlaysParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Highlight multiple elements with the CSS Grid overlay."""
        result = await self._client.send_raw(
            method="Overlay.setShowGridOverlays",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_flex_overlays(
        self, params: SetShowFlexOverlaysParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Overlay.setShowFlexOverlays",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_scroll_snap_overlays(
        self, params: SetShowScrollSnapOverlaysParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Overlay.setShowScrollSnapOverlays",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_container_query_overlays(
        self, params: SetShowContainerQueryOverlaysParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Overlay.setShowContainerQueryOverlays",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_paint_rects(
        self, params: SetShowPaintRectsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Requests that backend shows paint rectangles"""
        result = await self._client.send_raw(
            method="Overlay.setShowPaintRects",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_layout_shift_regions(
        self, params: SetShowLayoutShiftRegionsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Requests that backend shows layout shift regions"""
        result = await self._client.send_raw(
            method="Overlay.setShowLayoutShiftRegions",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_scroll_bottleneck_rects(
        self, params: SetShowScrollBottleneckRectsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Requests that backend shows scroll bottleneck rects"""
        result = await self._client.send_raw(
            method="Overlay.setShowScrollBottleneckRects",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_hit_test_borders(
        self, params: SetShowHitTestBordersParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Deprecated, no longer has any effect."""
        result = await self._client.send_raw(
            method="Overlay.setShowHitTestBorders",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_web_vitals(
        self, params: SetShowWebVitalsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Deprecated, no longer has any effect."""
        result = await self._client.send_raw(
            method="Overlay.setShowWebVitals",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_viewport_size_on_resize(
        self, params: SetShowViewportSizeOnResizeParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Paints viewport size upon main frame resize."""
        result = await self._client.send_raw(
            method="Overlay.setShowViewportSizeOnResize",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_hinge(
        self, params: SetShowHingeParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Add a dual screen device hinge"""
        result = await self._client.send_raw(
            method="Overlay.setShowHinge",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_isolated_elements(
        self, params: SetShowIsolatedElementsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Show elements in isolation mode with overlays."""
        result = await self._client.send_raw(
            method="Overlay.setShowIsolatedElements",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_show_window_controls_overlay(
        self,
        params: SetShowWindowControlsOverlayParams | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Show Window Controls Overlay for PWA"""
        result = await self._client.send_raw(
            method="Overlay.setShowWindowControlsOverlay",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
