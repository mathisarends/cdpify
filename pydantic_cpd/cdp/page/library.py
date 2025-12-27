"""Generated client library from CDP specification"""
# Domain: Page Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    AddCompilationCacheParams,
    AddScriptToEvaluateOnLoadParams,
    AddScriptToEvaluateOnLoadResult,
    AddScriptToEvaluateOnNewDocumentParams,
    AddScriptToEvaluateOnNewDocumentResult,
    CaptureScreenshotParams,
    CaptureScreenshotResult,
    CaptureSnapshotParams,
    CaptureSnapshotResult,
    CreateIsolatedWorldParams,
    CreateIsolatedWorldResult,
    DeleteCookieParams,
    EnableParams,
    GenerateTestReportParams,
    GetAdScriptAncestryParams,
    GetAdScriptAncestryResult,
    GetAnnotatedPageContentParams,
    GetAnnotatedPageContentResult,
    GetAppIdResult,
    GetAppManifestParams,
    GetAppManifestResult,
    GetFrameTreeResult,
    GetInstallabilityErrorsResult,
    GetLayoutMetricsResult,
    GetManifestIconsResult,
    GetNavigationHistoryResult,
    GetOriginTrialsParams,
    GetOriginTrialsResult,
    GetPermissionsPolicyStateParams,
    GetPermissionsPolicyStateResult,
    GetResourceContentParams,
    GetResourceContentResult,
    GetResourceTreeResult,
    HandleJavaScriptDialogParams,
    NavigateParams,
    NavigateResult,
    NavigateToHistoryEntryParams,
    PrintToPDFParams,
    PrintToPDFResult,
    ProduceCompilationCacheParams,
    ReloadParams,
    RemoveScriptToEvaluateOnLoadParams,
    RemoveScriptToEvaluateOnNewDocumentParams,
    ScreencastFrameAckParams,
    SearchInResourceParams,
    SearchInResourceResult,
    SetAdBlockingEnabledParams,
    SetBypassCSPParams,
    SetDeviceMetricsOverrideParams,
    SetDeviceOrientationOverrideParams,
    SetDocumentContentParams,
    SetDownloadBehaviorParams,
    SetFontFamiliesParams,
    SetFontSizesParams,
    SetGeolocationOverrideParams,
    SetInterceptFileChooserDialogParams,
    SetLifecycleEventsEnabledParams,
    SetPrerenderingAllowedParams,
    SetRPHRegistrationModeParams,
    SetSPCTransactionModeParams,
    SetTouchEmulationEnabledParams,
    SetWebLifecycleStateParams,
    StartScreencastParams,
)


class PageClient:
    """Actions and events related to the inspected page belong to the page domain."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def add_script_to_evaluate_on_load(
        self, params: AddScriptToEvaluateOnLoadParams, session_id: str | None = None
    ) -> AddScriptToEvaluateOnLoadResult:
        """Deprecated, please use addScriptToEvaluateOnNewDocument instead."""
        result = await self._client.send_raw(
            method="Page.addScriptToEvaluateOnLoad",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return AddScriptToEvaluateOnLoadResult.model_validate(result)

    async def add_script_to_evaluate_on_new_document(
        self,
        params: AddScriptToEvaluateOnNewDocumentParams,
        session_id: str | None = None,
    ) -> AddScriptToEvaluateOnNewDocumentResult:
        """Evaluates given script in every frame upon creation (before loading frame's scripts)."""
        result = await self._client.send_raw(
            method="Page.addScriptToEvaluateOnNewDocument",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return AddScriptToEvaluateOnNewDocumentResult.model_validate(result)

    async def bring_to_front(self, session_id: str | None = None) -> dict[str, Any]:
        """Brings page to front (activates tab)."""
        result = await self._client.send_raw(
            method="Page.bringToFront",
            params=None,
            session_id=session_id,
        )
        return result

    async def capture_screenshot(
        self,
        params: CaptureScreenshotParams | None = None,
        session_id: str | None = None,
    ) -> CaptureScreenshotResult:
        """Capture page screenshot."""
        result = await self._client.send_raw(
            method="Page.captureScreenshot",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CaptureScreenshotResult.model_validate(result)

    async def capture_snapshot(
        self, params: CaptureSnapshotParams | None = None, session_id: str | None = None
    ) -> CaptureSnapshotResult:
        """Returns a snapshot of the page as a string. For MHTML format, the serialization includes
        iframes, shadow DOM, external resources, and element-inline styles."""
        result = await self._client.send_raw(
            method="Page.captureSnapshot",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CaptureSnapshotResult.model_validate(result)

    async def clear_device_metrics_override(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        """Clears the overridden device metrics."""
        result = await self._client.send_raw(
            method="Page.clearDeviceMetricsOverride",
            params=None,
            session_id=session_id,
        )
        return result

    async def clear_device_orientation_override(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        """Clears the overridden Device Orientation."""
        result = await self._client.send_raw(
            method="Page.clearDeviceOrientationOverride",
            params=None,
            session_id=session_id,
        )
        return result

    async def clear_geolocation_override(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        """Clears the overridden Geolocation Position and Error."""
        result = await self._client.send_raw(
            method="Page.clearGeolocationOverride",
            params=None,
            session_id=session_id,
        )
        return result

    async def create_isolated_world(
        self, params: CreateIsolatedWorldParams, session_id: str | None = None
    ) -> CreateIsolatedWorldResult:
        """Creates an isolated world for the given frame."""
        result = await self._client.send_raw(
            method="Page.createIsolatedWorld",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CreateIsolatedWorldResult.model_validate(result)

    async def delete_cookie(
        self, params: DeleteCookieParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Deletes browser cookie with given name, domain and path."""
        result = await self._client.send_raw(
            method="Page.deleteCookie",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables page domain notifications."""
        result = await self._client.send_raw(
            method="Page.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, params: EnableParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enables page domain notifications."""
        result = await self._client.send_raw(
            method="Page.enable",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_app_manifest(
        self, params: GetAppManifestParams | None = None, session_id: str | None = None
    ) -> GetAppManifestResult:
        """Gets the processed manifest for this current document.
        This API always waits for the manifest to be loaded.
        If manifestId is provided, and it does not match the manifest of the
          current document, this API errors out.
        If there is not a loaded page, this API errors out immediately."""
        result = await self._client.send_raw(
            method="Page.getAppManifest",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetAppManifestResult.model_validate(result)

    async def get_installability_errors(
        self, session_id: str | None = None
    ) -> GetInstallabilityErrorsResult:
        result = await self._client.send_raw(
            method="Page.getInstallabilityErrors",
            params=None,
            session_id=session_id,
        )
        return GetInstallabilityErrorsResult.model_validate(result)

    async def get_manifest_icons(
        self, session_id: str | None = None
    ) -> GetManifestIconsResult:
        """Deprecated because it's not guaranteed that the returned icon is in fact the one used for PWA installation."""
        result = await self._client.send_raw(
            method="Page.getManifestIcons",
            params=None,
            session_id=session_id,
        )
        return GetManifestIconsResult.model_validate(result)

    async def get_app_id(self, session_id: str | None = None) -> GetAppIdResult:
        """Returns the unique (PWA) app id.
        Only returns values if the feature flag 'WebAppEnableManifestId' is enabled"""
        result = await self._client.send_raw(
            method="Page.getAppId",
            params=None,
            session_id=session_id,
        )
        return GetAppIdResult.model_validate(result)

    async def get_ad_script_ancestry(
        self, params: GetAdScriptAncestryParams, session_id: str | None = None
    ) -> GetAdScriptAncestryResult:
        result = await self._client.send_raw(
            method="Page.getAdScriptAncestry",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetAdScriptAncestryResult.model_validate(result)

    async def get_frame_tree(self, session_id: str | None = None) -> GetFrameTreeResult:
        """Returns present frame tree structure."""
        result = await self._client.send_raw(
            method="Page.getFrameTree",
            params=None,
            session_id=session_id,
        )
        return GetFrameTreeResult.model_validate(result)

    async def get_layout_metrics(
        self, session_id: str | None = None
    ) -> GetLayoutMetricsResult:
        """Returns metrics relating to the layouting of the page, such as viewport bounds/scale."""
        result = await self._client.send_raw(
            method="Page.getLayoutMetrics",
            params=None,
            session_id=session_id,
        )
        return GetLayoutMetricsResult.model_validate(result)

    async def get_navigation_history(
        self, session_id: str | None = None
    ) -> GetNavigationHistoryResult:
        """Returns navigation history for the current page."""
        result = await self._client.send_raw(
            method="Page.getNavigationHistory",
            params=None,
            session_id=session_id,
        )
        return GetNavigationHistoryResult.model_validate(result)

    async def reset_navigation_history(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        """Resets navigation history for the current page."""
        result = await self._client.send_raw(
            method="Page.resetNavigationHistory",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_resource_content(
        self, params: GetResourceContentParams, session_id: str | None = None
    ) -> GetResourceContentResult:
        """Returns content of the given resource."""
        result = await self._client.send_raw(
            method="Page.getResourceContent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetResourceContentResult.model_validate(result)

    async def get_resource_tree(
        self, session_id: str | None = None
    ) -> GetResourceTreeResult:
        """Returns present frame / resource tree structure."""
        result = await self._client.send_raw(
            method="Page.getResourceTree",
            params=None,
            session_id=session_id,
        )
        return GetResourceTreeResult.model_validate(result)

    async def handle_java_script_dialog(
        self, params: HandleJavaScriptDialogParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Accepts or dismisses a JavaScript initiated dialog (alert, confirm, prompt, or onbeforeunload)."""
        result = await self._client.send_raw(
            method="Page.handleJavaScriptDialog",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def navigate(
        self, params: NavigateParams, session_id: str | None = None
    ) -> NavigateResult:
        """Navigates current page to the given URL."""
        result = await self._client.send_raw(
            method="Page.navigate",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return NavigateResult.model_validate(result)

    async def navigate_to_history_entry(
        self, params: NavigateToHistoryEntryParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Navigates current page to the given history entry."""
        result = await self._client.send_raw(
            method="Page.navigateToHistoryEntry",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def print_to_p_d_f(
        self, params: PrintToPDFParams | None = None, session_id: str | None = None
    ) -> PrintToPDFResult:
        """Print page as PDF."""
        result = await self._client.send_raw(
            method="Page.printToPDF",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return PrintToPDFResult.model_validate(result)

    async def reload(
        self, params: ReloadParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Reloads given page optionally ignoring the cache."""
        result = await self._client.send_raw(
            method="Page.reload",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def remove_script_to_evaluate_on_load(
        self, params: RemoveScriptToEvaluateOnLoadParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Deprecated, please use removeScriptToEvaluateOnNewDocument instead."""
        result = await self._client.send_raw(
            method="Page.removeScriptToEvaluateOnLoad",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def remove_script_to_evaluate_on_new_document(
        self,
        params: RemoveScriptToEvaluateOnNewDocumentParams,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Removes given script from the list."""
        result = await self._client.send_raw(
            method="Page.removeScriptToEvaluateOnNewDocument",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def screencast_frame_ack(
        self, params: ScreencastFrameAckParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Acknowledges that a screencast frame has been received by the frontend."""
        result = await self._client.send_raw(
            method="Page.screencastFrameAck",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def search_in_resource(
        self, params: SearchInResourceParams, session_id: str | None = None
    ) -> SearchInResourceResult:
        """Searches for given string in resource content."""
        result = await self._client.send_raw(
            method="Page.searchInResource",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SearchInResourceResult.model_validate(result)

    async def set_ad_blocking_enabled(
        self, params: SetAdBlockingEnabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enable Chrome's experimental ad filter on all sites."""
        result = await self._client.send_raw(
            method="Page.setAdBlockingEnabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_bypass_c_s_p(
        self, params: SetBypassCSPParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enable page Content Security Policy by-passing."""
        result = await self._client.send_raw(
            method="Page.setBypassCSP",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_permissions_policy_state(
        self, params: GetPermissionsPolicyStateParams, session_id: str | None = None
    ) -> GetPermissionsPolicyStateResult:
        """Get Permissions Policy state on given frame."""
        result = await self._client.send_raw(
            method="Page.getPermissionsPolicyState",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetPermissionsPolicyStateResult.model_validate(result)

    async def get_origin_trials(
        self, params: GetOriginTrialsParams, session_id: str | None = None
    ) -> GetOriginTrialsResult:
        """Get Origin Trials on given frame."""
        result = await self._client.send_raw(
            method="Page.getOriginTrials",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetOriginTrialsResult.model_validate(result)

    async def set_device_metrics_override(
        self, params: SetDeviceMetricsOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Overrides the values of device screen dimensions (window.screen.width, window.screen.height,
        window.innerWidth, window.innerHeight, and "device-width"/"device-height"-related CSS media
        query results)."""
        result = await self._client.send_raw(
            method="Page.setDeviceMetricsOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_device_orientation_override(
        self, params: SetDeviceOrientationOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Overrides the Device Orientation."""
        result = await self._client.send_raw(
            method="Page.setDeviceOrientationOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_font_families(
        self, params: SetFontFamiliesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Set generic font families."""
        result = await self._client.send_raw(
            method="Page.setFontFamilies",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_font_sizes(
        self, params: SetFontSizesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Set default font sizes."""
        result = await self._client.send_raw(
            method="Page.setFontSizes",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_document_content(
        self, params: SetDocumentContentParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Sets given markup as the document's HTML."""
        result = await self._client.send_raw(
            method="Page.setDocumentContent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_download_behavior(
        self, params: SetDownloadBehaviorParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Set the behavior when downloading a file."""
        result = await self._client.send_raw(
            method="Page.setDownloadBehavior",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_geolocation_override(
        self,
        params: SetGeolocationOverrideParams | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Overrides the Geolocation Position or Error. Omitting any of the parameters emulates position
        unavailable."""
        result = await self._client.send_raw(
            method="Page.setGeolocationOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_lifecycle_events_enabled(
        self, params: SetLifecycleEventsEnabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Controls whether page will emit lifecycle events."""
        result = await self._client.send_raw(
            method="Page.setLifecycleEventsEnabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_touch_emulation_enabled(
        self, params: SetTouchEmulationEnabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Toggles mouse event-based touch event emulation."""
        result = await self._client.send_raw(
            method="Page.setTouchEmulationEnabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def start_screencast(
        self, params: StartScreencastParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Starts sending each frame using the `screencastFrame` event."""
        result = await self._client.send_raw(
            method="Page.startScreencast",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def stop_loading(self, session_id: str | None = None) -> dict[str, Any]:
        """Force the page stop all navigations and pending resource fetches."""
        result = await self._client.send_raw(
            method="Page.stopLoading",
            params=None,
            session_id=session_id,
        )
        return result

    async def crash(self, session_id: str | None = None) -> dict[str, Any]:
        """Crashes renderer on the IO thread, generates minidumps."""
        result = await self._client.send_raw(
            method="Page.crash",
            params=None,
            session_id=session_id,
        )
        return result

    async def close(self, session_id: str | None = None) -> dict[str, Any]:
        """Tries to close page, running its beforeunload hooks, if any."""
        result = await self._client.send_raw(
            method="Page.close",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_web_lifecycle_state(
        self, params: SetWebLifecycleStateParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Tries to update the web lifecycle state of the page.
        It will transition the page to the given state according to:
        https://github.com/WICG/web-lifecycle/"""
        result = await self._client.send_raw(
            method="Page.setWebLifecycleState",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def stop_screencast(self, session_id: str | None = None) -> dict[str, Any]:
        """Stops sending each frame in the `screencastFrame`."""
        result = await self._client.send_raw(
            method="Page.stopScreencast",
            params=None,
            session_id=session_id,
        )
        return result

    async def produce_compilation_cache(
        self, params: ProduceCompilationCacheParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Requests backend to produce compilation cache for the specified scripts.
        `scripts` are appended to the list of scripts for which the cache
        would be produced. The list may be reset during page navigation.
        When script with a matching URL is encountered, the cache is optionally
        produced upon backend discretion, based on internal heuristics.
        See also: `Page.compilationCacheProduced`."""
        result = await self._client.send_raw(
            method="Page.produceCompilationCache",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def add_compilation_cache(
        self, params: AddCompilationCacheParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Seeds compilation cache for given url. Compilation cache does not survive
        cross-process navigation."""
        result = await self._client.send_raw(
            method="Page.addCompilationCache",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def clear_compilation_cache(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        """Clears seeded compilation cache."""
        result = await self._client.send_raw(
            method="Page.clearCompilationCache",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_s_p_c_transaction_mode(
        self, params: SetSPCTransactionModeParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Sets the Secure Payment Confirmation transaction mode.
        https://w3c.github.io/secure-payment-confirmation/#sctn-automation-set-spc-transaction-mode"""
        result = await self._client.send_raw(
            method="Page.setSPCTransactionMode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_r_p_h_registration_mode(
        self, params: SetRPHRegistrationModeParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Extensions for Custom Handlers API:
        https://html.spec.whatwg.org/multipage/system-state.html#rph-automation"""
        result = await self._client.send_raw(
            method="Page.setRPHRegistrationMode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def generate_test_report(
        self, params: GenerateTestReportParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Generates a report for testing."""
        result = await self._client.send_raw(
            method="Page.generateTestReport",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def wait_for_debugger(self, session_id: str | None = None) -> dict[str, Any]:
        """Pauses page execution. Can be resumed using generic Runtime.runIfWaitingForDebugger."""
        result = await self._client.send_raw(
            method="Page.waitForDebugger",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_intercept_file_chooser_dialog(
        self, params: SetInterceptFileChooserDialogParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Intercept file chooser requests and transfer control to protocol clients.
        When file chooser interception is enabled, native file chooser dialog is not shown.
        Instead, a protocol event `Page.fileChooserOpened` is emitted."""
        result = await self._client.send_raw(
            method="Page.setInterceptFileChooserDialog",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_prerendering_allowed(
        self, params: SetPrerenderingAllowedParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enable/disable prerendering manually.

        This command is a short-term solution for https://crbug.com/1440085.
        See https://docs.google.com/document/d/12HVmFxYj5Jc-eJr5OmWsa2bqTJsbgGLKI6ZIyx0_wpA
        for more details.

        TODO(https://crbug.com/1440085): Remove this once Puppeteer supports tab targets."""
        result = await self._client.send_raw(
            method="Page.setPrerenderingAllowed",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_annotated_page_content(
        self,
        params: GetAnnotatedPageContentParams | None = None,
        session_id: str | None = None,
    ) -> GetAnnotatedPageContentResult:
        """Get the annotated page content for the main frame.
        This is an experimental command that is subject to change."""
        result = await self._client.send_raw(
            method="Page.getAnnotatedPageContent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetAnnotatedPageContentResult.model_validate(result)
