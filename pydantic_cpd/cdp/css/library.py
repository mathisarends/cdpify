"""Generated client library from CDP specification"""
# Domain: CSS Client

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
    """This domain exposes CSS read/write operations. All CSS objects (stylesheets, rules, and styles)
    have an associated `id` used in subsequent operations on the related object. Each object type has
    a specific `id` structure, and those are not interchangeable between objects of different kinds.
    CSS objects can be loaded using the `get*ForNode()` calls (which accept a DOM node id). A client
    can also keep track of stylesheets via the `styleSheetAdded`/`styleSheetRemoved` events and
    subsequently load the required stylesheet contents using the `getStyleSheet[Text]()` methods."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def add_rule(
        self, params: AddRuleParams, session_id: str | None = None
    ) -> AddRuleResult:
        """Inserts a new rule with the given `ruleText` in a stylesheet with given `styleSheetId`, at the
        position specified by `location`."""
        result = await self._client.send_raw(
            method="CSS.addRule",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return AddRuleResult.model_validate(result)

    async def collect_class_names(
        self, params: CollectClassNamesParams, session_id: str | None = None
    ) -> CollectClassNamesResult:
        """Returns all class names from specified stylesheet."""
        result = await self._client.send_raw(
            method="CSS.collectClassNames",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CollectClassNamesResult.model_validate(result)

    async def create_style_sheet(
        self, params: CreateStyleSheetParams, session_id: str | None = None
    ) -> CreateStyleSheetResult:
        """Creates a new special "via-inspector" stylesheet in the frame with given `frameId`."""
        result = await self._client.send_raw(
            method="CSS.createStyleSheet",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CreateStyleSheetResult.model_validate(result)

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables the CSS agent for the given page."""
        result = await self._client.send_raw(
            method="CSS.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        """Enables the CSS agent for the given page. Clients should not assume that the CSS agent has been
        enabled until the result of this command is received."""
        result = await self._client.send_raw(
            method="CSS.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def force_pseudo_state(
        self, params: ForcePseudoStateParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Ensures that the given node will have specified pseudo-classes whenever its style is computed by
        the browser."""
        result = await self._client.send_raw(
            method="CSS.forcePseudoState",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def force_starting_style(
        self, params: ForceStartingStyleParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Ensures that the given node is in its starting-style state."""
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
        """Returns the computed style for a DOM node identified by `nodeId`."""
        result = await self._client.send_raw(
            method="CSS.getComputedStyleForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetComputedStyleForNodeResult.model_validate(result)

    async def resolve_values(
        self, params: ResolveValuesParams, session_id: str | None = None
    ) -> ResolveValuesResult:
        """Resolve the specified values in the context of the provided element.
        For example, a value of '1em' is evaluated according to the computed
        'font-size' of the element and a value 'calc(1px + 2px)' will be
        resolved to '3px'.
        If the `propertyName` was specified the `values` are resolved as if
        they were property's declaration. If a value cannot be parsed according
        to the provided property syntax, the value is parsed using combined
        syntax as if null `propertyName` was provided. If the value cannot be
        resolved even then, return the provided value without any changes."""
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
        """Returns the styles defined inline (explicitly in the "style" attribute and implicitly, using DOM
        attributes) for a DOM node identified by `nodeId`."""
        result = await self._client.send_raw(
            method="CSS.getInlineStylesForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetInlineStylesForNodeResult.model_validate(result)

    async def get_animated_styles_for_node(
        self, params: GetAnimatedStylesForNodeParams, session_id: str | None = None
    ) -> GetAnimatedStylesForNodeResult:
        """Returns the styles coming from animations & transitions
        including the animation & transition styles coming from inheritance chain."""
        result = await self._client.send_raw(
            method="CSS.getAnimatedStylesForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetAnimatedStylesForNodeResult.model_validate(result)

    async def get_matched_styles_for_node(
        self, params: GetMatchedStylesForNodeParams, session_id: str | None = None
    ) -> GetMatchedStylesForNodeResult:
        """Returns requested styles for a DOM node identified by `nodeId`."""
        result = await self._client.send_raw(
            method="CSS.getMatchedStylesForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetMatchedStylesForNodeResult.model_validate(result)

    async def get_environment_variables(
        self, session_id: str | None = None
    ) -> GetEnvironmentVariablesResult:
        """Returns the values of the default UA-defined environment variables used in env()"""
        result = await self._client.send_raw(
            method="CSS.getEnvironmentVariables",
            params=None,
            session_id=session_id,
        )
        return GetEnvironmentVariablesResult.model_validate(result)

    async def get_media_queries(
        self, session_id: str | None = None
    ) -> GetMediaQueriesResult:
        """Returns all media queries parsed by the rendering engine."""
        result = await self._client.send_raw(
            method="CSS.getMediaQueries",
            params=None,
            session_id=session_id,
        )
        return GetMediaQueriesResult.model_validate(result)

    async def get_platform_fonts_for_node(
        self, params: GetPlatformFontsForNodeParams, session_id: str | None = None
    ) -> GetPlatformFontsForNodeResult:
        """Requests information about platform fonts which we used to render child TextNodes in the given
        node."""
        result = await self._client.send_raw(
            method="CSS.getPlatformFontsForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetPlatformFontsForNodeResult.model_validate(result)

    async def get_style_sheet_text(
        self, params: GetStyleSheetTextParams, session_id: str | None = None
    ) -> GetStyleSheetTextResult:
        """Returns the current textual content for a stylesheet."""
        result = await self._client.send_raw(
            method="CSS.getStyleSheetText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetStyleSheetTextResult.model_validate(result)

    async def get_layers_for_node(
        self, params: GetLayersForNodeParams, session_id: str | None = None
    ) -> GetLayersForNodeResult:
        """Returns all layers parsed by the rendering engine for the tree scope of a node.
        Given a DOM element identified by nodeId, getLayersForNode returns the root
        layer for the nearest ancestor document or shadow root. The layer root contains
        the full layer tree for the tree scope and their ordering."""
        result = await self._client.send_raw(
            method="CSS.getLayersForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetLayersForNodeResult.model_validate(result)

    async def get_location_for_selector(
        self, params: GetLocationForSelectorParams, session_id: str | None = None
    ) -> GetLocationForSelectorResult:
        """Given a CSS selector text and a style sheet ID, getLocationForSelector
        returns an array of locations of the CSS selector in the style sheet."""
        result = await self._client.send_raw(
            method="CSS.getLocationForSelector",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetLocationForSelectorResult.model_validate(result)

    async def track_computed_style_updates_for_node(
        self,
        params: TrackComputedStyleUpdatesForNodeParams | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Starts tracking the given node for the computed style updates
        and whenever the computed style is updated for node, it queues
        a `computedStyleUpdated` event with throttling.
        There can only be 1 node tracked for computed style updates
        so passing a new node id removes tracking from the previous node.
        Pass `undefined` to disable tracking."""
        result = await self._client.send_raw(
            method="CSS.trackComputedStyleUpdatesForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def track_computed_style_updates(
        self, params: TrackComputedStyleUpdatesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Starts tracking the given computed styles for updates. The specified array of properties
        replaces the one previously specified. Pass empty array to disable tracking.
        Use takeComputedStyleUpdates to retrieve the list of nodes that had properties modified.
        The changes to computed style properties are only tracked for nodes pushed to the front-end
        by the DOM agent. If no changes to the tracked properties occur after the node has been pushed
        to the front-end, no updates will be issued for the node."""
        result = await self._client.send_raw(
            method="CSS.trackComputedStyleUpdates",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def take_computed_style_updates(
        self, session_id: str | None = None
    ) -> TakeComputedStyleUpdatesResult:
        """Polls the next batch of computed style updates."""
        result = await self._client.send_raw(
            method="CSS.takeComputedStyleUpdates",
            params=None,
            session_id=session_id,
        )
        return TakeComputedStyleUpdatesResult.model_validate(result)

    async def set_effective_property_value_for_node(
        self,
        params: SetEffectivePropertyValueForNodeParams,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Find a rule with the given active property for the given node and set the new value for this
        property"""
        result = await self._client.send_raw(
            method="CSS.setEffectivePropertyValueForNode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_property_rule_property_name(
        self, params: SetPropertyRulePropertyNameParams, session_id: str | None = None
    ) -> SetPropertyRulePropertyNameResult:
        """Modifies the property rule property name."""
        result = await self._client.send_raw(
            method="CSS.setPropertyRulePropertyName",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetPropertyRulePropertyNameResult.model_validate(result)

    async def set_keyframe_key(
        self, params: SetKeyframeKeyParams, session_id: str | None = None
    ) -> SetKeyframeKeyResult:
        """Modifies the keyframe rule key text."""
        result = await self._client.send_raw(
            method="CSS.setKeyframeKey",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetKeyframeKeyResult.model_validate(result)

    async def set_media_text(
        self, params: SetMediaTextParams, session_id: str | None = None
    ) -> SetMediaTextResult:
        """Modifies the rule selector."""
        result = await self._client.send_raw(
            method="CSS.setMediaText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetMediaTextResult.model_validate(result)

    async def set_container_query_text(
        self, params: SetContainerQueryTextParams, session_id: str | None = None
    ) -> SetContainerQueryTextResult:
        """Modifies the expression of a container query."""
        result = await self._client.send_raw(
            method="CSS.setContainerQueryText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetContainerQueryTextResult.model_validate(result)

    async def set_supports_text(
        self, params: SetSupportsTextParams, session_id: str | None = None
    ) -> SetSupportsTextResult:
        """Modifies the expression of a supports at-rule."""
        result = await self._client.send_raw(
            method="CSS.setSupportsText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetSupportsTextResult.model_validate(result)

    async def set_scope_text(
        self, params: SetScopeTextParams, session_id: str | None = None
    ) -> SetScopeTextResult:
        """Modifies the expression of a scope at-rule."""
        result = await self._client.send_raw(
            method="CSS.setScopeText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetScopeTextResult.model_validate(result)

    async def set_rule_selector(
        self, params: SetRuleSelectorParams, session_id: str | None = None
    ) -> SetRuleSelectorResult:
        """Modifies the rule selector."""
        result = await self._client.send_raw(
            method="CSS.setRuleSelector",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetRuleSelectorResult.model_validate(result)

    async def set_style_sheet_text(
        self, params: SetStyleSheetTextParams, session_id: str | None = None
    ) -> SetStyleSheetTextResult:
        """Sets the new stylesheet text."""
        result = await self._client.send_raw(
            method="CSS.setStyleSheetText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetStyleSheetTextResult.model_validate(result)

    async def set_style_texts(
        self, params: SetStyleTextsParams, session_id: str | None = None
    ) -> SetStyleTextsResult:
        """Applies specified style edits one after another in the given order."""
        result = await self._client.send_raw(
            method="CSS.setStyleTexts",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetStyleTextsResult.model_validate(result)

    async def start_rule_usage_tracking(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enables the selector recording."""
        result = await self._client.send_raw(
            method="CSS.startRuleUsageTracking",
            params=None,
            session_id=session_id,
        )
        return result

    async def stop_rule_usage_tracking(
        self, session_id: str | None = None
    ) -> StopRuleUsageTrackingResult:
        """Stop tracking rule usage and return the list of rules that were used since last call to
        `takeCoverageDelta` (or since start of coverage instrumentation)."""
        result = await self._client.send_raw(
            method="CSS.stopRuleUsageTracking",
            params=None,
            session_id=session_id,
        )
        return StopRuleUsageTrackingResult.model_validate(result)

    async def take_coverage_delta(
        self, session_id: str | None = None
    ) -> TakeCoverageDeltaResult:
        """Obtain list of rules that became used since last call to this method (or since start of coverage
        instrumentation)."""
        result = await self._client.send_raw(
            method="CSS.takeCoverageDelta",
            params=None,
            session_id=session_id,
        )
        return TakeCoverageDeltaResult.model_validate(result)

    async def set_local_fonts_enabled(
        self, params: SetLocalFontsEnabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enables/disables rendering of local CSS fonts (enabled by default)."""
        result = await self._client.send_raw(
            method="CSS.setLocalFontsEnabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
