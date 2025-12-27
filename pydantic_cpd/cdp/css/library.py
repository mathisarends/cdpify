"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    AddRuleParams,
    AddRuleResult,
    CollectClassNamesParams,
    CollectClassNamesResult,
    CreateStyleSheetParams,
    CreateStyleSheetResult,
    ForcePseudoStateParams,
    ForceStartingStyleParams,
    GetAnimatedStylesForNodeParams,
    GetAnimatedStylesForNodeResult,
    GetBackgroundColorsParams,
    GetBackgroundColorsResult,
    GetComputedStyleForNodeParams,
    GetComputedStyleForNodeResult,
    GetEnvironmentVariablesResult,
    GetInlineStylesForNodeParams,
    GetInlineStylesForNodeResult,
    GetLayersForNodeParams,
    GetLayersForNodeResult,
    GetLocationForSelectorParams,
    GetLocationForSelectorResult,
    GetLonghandPropertiesParams,
    GetLonghandPropertiesResult,
    GetMatchedStylesForNodeParams,
    GetMatchedStylesForNodeResult,
    GetMediaQueriesResult,
    GetPlatformFontsForNodeParams,
    GetPlatformFontsForNodeResult,
    GetStyleSheetTextParams,
    GetStyleSheetTextResult,
    ResolveValuesParams,
    ResolveValuesResult,
    SetContainerQueryTextParams,
    SetContainerQueryTextResult,
    SetEffectivePropertyValueForNodeParams,
    SetKeyframeKeyParams,
    SetKeyframeKeyResult,
    SetLocalFontsEnabledParams,
    SetMediaTextParams,
    SetMediaTextResult,
    SetPropertyRulePropertyNameParams,
    SetPropertyRulePropertyNameResult,
    SetRuleSelectorParams,
    SetRuleSelectorResult,
    SetScopeTextParams,
    SetScopeTextResult,
    SetStyleSheetTextParams,
    SetStyleSheetTextResult,
    SetStyleTextsParams,
    SetStyleTextsResult,
    SetSupportsTextParams,
    SetSupportsTextResult,
    StopRuleUsageTrackingResult,
    TakeComputedStyleUpdatesResult,
    TakeCoverageDeltaResult,
    TrackComputedStyleUpdatesForNodeParams,
    TrackComputedStyleUpdatesParams,
)

class CSSClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def add_rule(
        self, params: AddRuleParams, session_id: str | None = None
    ) -> AddRuleResult:
        result = await self._client.send_raw(
            method="CSS.addRule",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return AddRuleResult.model_validate(result)

    async def collect_class_names(
        self, params: CollectClassNamesParams, session_id: str | None = None
    ) -> CollectClassNamesResult:
        result = await self._client.send_raw(
            method="CSS.collectClassNames",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CollectClassNamesResult.model_validate(result)

    async def create_style_sheet(
        self, params: CreateStyleSheetParams, session_id: str | None = None
    ) -> CreateStyleSheetResult:
        result = await self._client.send_raw(
            method="CSS.createStyleSheet",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CreateStyleSheetResult.model_validate(result)

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="CSS.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="CSS.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def force_pseudo_state(
        self, params: ForcePseudoStateParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="CSS.forcePseudoState",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def force_starting_style(
        self, params: ForceStartingStyleParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="CSS.forceStartingStyle",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_background_colors(
        self, params: GetBackgroundColorsParams, session_id: str | None = None
    ) -> GetBackgroundColorsResult:
        result = await self._client.send_raw(
            method="CSS.getBackgroundColors",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetBackgroundColorsResult.model_validate(result)

    async def get_computed_style_for_node(
        self, params: GetComputedStyleForNodeParams, session_id: str | None = None
    ) -> GetComputedStyleForNodeResult:
        result = await self._client.send_raw(
            method="CSS.getComputedStyleForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetComputedStyleForNodeResult.model_validate(result)

    async def resolve_values(
        self, params: ResolveValuesParams, session_id: str | None = None
    ) -> ResolveValuesResult:
        result = await self._client.send_raw(
            method="CSS.resolveValues",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return ResolveValuesResult.model_validate(result)

    async def get_longhand_properties(
        self, params: GetLonghandPropertiesParams, session_id: str | None = None
    ) -> GetLonghandPropertiesResult:
        result = await self._client.send_raw(
            method="CSS.getLonghandProperties",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetLonghandPropertiesResult.model_validate(result)

    async def get_inline_styles_for_node(
        self, params: GetInlineStylesForNodeParams, session_id: str | None = None
    ) -> GetInlineStylesForNodeResult:
        result = await self._client.send_raw(
            method="CSS.getInlineStylesForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetInlineStylesForNodeResult.model_validate(result)

    async def get_animated_styles_for_node(
        self, params: GetAnimatedStylesForNodeParams, session_id: str | None = None
    ) -> GetAnimatedStylesForNodeResult:
        result = await self._client.send_raw(
            method="CSS.getAnimatedStylesForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetAnimatedStylesForNodeResult.model_validate(result)

    async def get_matched_styles_for_node(
        self, params: GetMatchedStylesForNodeParams, session_id: str | None = None
    ) -> GetMatchedStylesForNodeResult:
        result = await self._client.send_raw(
            method="CSS.getMatchedStylesForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetMatchedStylesForNodeResult.model_validate(result)

    async def get_environment_variables(
        self, session_id: str | None = None
    ) -> GetEnvironmentVariablesResult:
        result = await self._client.send_raw(
            method="CSS.getEnvironmentVariables",
            params=None,
            session_id=session_id,
        )
        return GetEnvironmentVariablesResult.model_validate(result)

    async def get_media_queries(
        self, session_id: str | None = None
    ) -> GetMediaQueriesResult:
        result = await self._client.send_raw(
            method="CSS.getMediaQueries",
            params=None,
            session_id=session_id,
        )
        return GetMediaQueriesResult.model_validate(result)

    async def get_platform_fonts_for_node(
        self, params: GetPlatformFontsForNodeParams, session_id: str | None = None
    ) -> GetPlatformFontsForNodeResult:
        result = await self._client.send_raw(
            method="CSS.getPlatformFontsForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetPlatformFontsForNodeResult.model_validate(result)

    async def get_style_sheet_text(
        self, params: GetStyleSheetTextParams, session_id: str | None = None
    ) -> GetStyleSheetTextResult:
        result = await self._client.send_raw(
            method="CSS.getStyleSheetText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetStyleSheetTextResult.model_validate(result)

    async def get_layers_for_node(
        self, params: GetLayersForNodeParams, session_id: str | None = None
    ) -> GetLayersForNodeResult:
        result = await self._client.send_raw(
            method="CSS.getLayersForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetLayersForNodeResult.model_validate(result)

    async def get_location_for_selector(
        self, params: GetLocationForSelectorParams, session_id: str | None = None
    ) -> GetLocationForSelectorResult:
        result = await self._client.send_raw(
            method="CSS.getLocationForSelector",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetLocationForSelectorResult.model_validate(result)

    async def track_computed_style_updates_for_node(
        self, params: TrackComputedStyleUpdatesForNodeParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="CSS.trackComputedStyleUpdatesForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def track_computed_style_updates(
        self, params: TrackComputedStyleUpdatesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="CSS.trackComputedStyleUpdates",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def take_computed_style_updates(
        self, session_id: str | None = None
    ) -> TakeComputedStyleUpdatesResult:
        result = await self._client.send_raw(
            method="CSS.takeComputedStyleUpdates",
            params=None,
            session_id=session_id,
        )
        return TakeComputedStyleUpdatesResult.model_validate(result)

    async def set_effective_property_value_for_node(
        self, params: SetEffectivePropertyValueForNodeParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="CSS.setEffectivePropertyValueForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_property_rule_property_name(
        self, params: SetPropertyRulePropertyNameParams, session_id: str | None = None
    ) -> SetPropertyRulePropertyNameResult:
        result = await self._client.send_raw(
            method="CSS.setPropertyRulePropertyName",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetPropertyRulePropertyNameResult.model_validate(result)

    async def set_keyframe_key(
        self, params: SetKeyframeKeyParams, session_id: str | None = None
    ) -> SetKeyframeKeyResult:
        result = await self._client.send_raw(
            method="CSS.setKeyframeKey",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetKeyframeKeyResult.model_validate(result)

    async def set_media_text(
        self, params: SetMediaTextParams, session_id: str | None = None
    ) -> SetMediaTextResult:
        result = await self._client.send_raw(
            method="CSS.setMediaText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetMediaTextResult.model_validate(result)

    async def set_container_query_text(
        self, params: SetContainerQueryTextParams, session_id: str | None = None
    ) -> SetContainerQueryTextResult:
        result = await self._client.send_raw(
            method="CSS.setContainerQueryText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetContainerQueryTextResult.model_validate(result)

    async def set_supports_text(
        self, params: SetSupportsTextParams, session_id: str | None = None
    ) -> SetSupportsTextResult:
        result = await self._client.send_raw(
            method="CSS.setSupportsText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetSupportsTextResult.model_validate(result)

    async def set_scope_text(
        self, params: SetScopeTextParams, session_id: str | None = None
    ) -> SetScopeTextResult:
        result = await self._client.send_raw(
            method="CSS.setScopeText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetScopeTextResult.model_validate(result)

    async def set_rule_selector(
        self, params: SetRuleSelectorParams, session_id: str | None = None
    ) -> SetRuleSelectorResult:
        result = await self._client.send_raw(
            method="CSS.setRuleSelector",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetRuleSelectorResult.model_validate(result)

    async def set_style_sheet_text(
        self, params: SetStyleSheetTextParams, session_id: str | None = None
    ) -> SetStyleSheetTextResult:
        result = await self._client.send_raw(
            method="CSS.setStyleSheetText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetStyleSheetTextResult.model_validate(result)

    async def set_style_texts(
        self, params: SetStyleTextsParams, session_id: str | None = None
    ) -> SetStyleTextsResult:
        result = await self._client.send_raw(
            method="CSS.setStyleTexts",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetStyleTextsResult.model_validate(result)

    async def start_rule_usage_tracking(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="CSS.startRuleUsageTracking",
            params=None,
            session_id=session_id,
        )
        return result

    async def stop_rule_usage_tracking(
        self, session_id: str | None = None
    ) -> StopRuleUsageTrackingResult:
        result = await self._client.send_raw(
            method="CSS.stopRuleUsageTracking",
            params=None,
            session_id=session_id,
        )
        return StopRuleUsageTrackingResult.model_validate(result)

    async def take_coverage_delta(
        self, session_id: str | None = None
    ) -> TakeCoverageDeltaResult:
        result = await self._client.send_raw(
            method="CSS.takeCoverageDelta",
            params=None,
            session_id=session_id,
        )
        return TakeCoverageDeltaResult.model_validate(result)

    async def set_local_fonts_enabled(
        self, params: SetLocalFontsEnabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="CSS.setLocalFontsEnabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
