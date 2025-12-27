"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    AddPrivacySandboxCoordinatorKeyConfigParams,
    AddPrivacySandboxEnrollmentOverrideParams,
    CancelDownloadParams,
    ExecuteBrowserCommandParams,
    GetBrowserCommandLineResult,
    GetHistogramParams,
    GetHistogramResult,
    GetHistogramsParams,
    GetHistogramsResult,
    GetVersionResult,
    GetWindowBoundsParams,
    GetWindowBoundsResult,
    GetWindowForTargetParams,
    GetWindowForTargetResult,
    GrantPermissionsParams,
    ResetPermissionsParams,
    SetContentsSizeParams,
    SetDockTileParams,
    SetDownloadBehaviorParams,
    SetPermissionParams,
    SetWindowBoundsParams,
)

class BrowserClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def set_permission(
        self, params: SetPermissionParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.setPermission",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def grant_permissions(
        self, params: GrantPermissionsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.grantPermissions",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def reset_permissions(
        self, params: ResetPermissionsParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.resetPermissions",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_download_behavior(
        self, params: SetDownloadBehaviorParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.setDownloadBehavior",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def cancel_download(
        self, params: CancelDownloadParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.cancelDownload",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def close(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.close",
            params=None,
            session_id=session_id,
        )
        return result

    async def crash(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.crash",
            params=None,
            session_id=session_id,
        )
        return result

    async def crash_gpu_process(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.crashGpuProcess",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_version(
        self, session_id: str | None = None
    ) -> GetVersionResult:
        result = await self._client.send_raw(
            method="Browser.getVersion",
            params=None,
            session_id=session_id,
        )
        return GetVersionResult.model_validate(result)

    async def get_browser_command_line(
        self, session_id: str | None = None
    ) -> GetBrowserCommandLineResult:
        result = await self._client.send_raw(
            method="Browser.getBrowserCommandLine",
            params=None,
            session_id=session_id,
        )
        return GetBrowserCommandLineResult.model_validate(result)

    async def get_histograms(
        self, params: GetHistogramsParams | None = None, session_id: str | None = None
    ) -> GetHistogramsResult:
        result = await self._client.send_raw(
            method="Browser.getHistograms",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetHistogramsResult.model_validate(result)

    async def get_histogram(
        self, params: GetHistogramParams, session_id: str | None = None
    ) -> GetHistogramResult:
        result = await self._client.send_raw(
            method="Browser.getHistogram",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetHistogramResult.model_validate(result)

    async def get_window_bounds(
        self, params: GetWindowBoundsParams, session_id: str | None = None
    ) -> GetWindowBoundsResult:
        result = await self._client.send_raw(
            method="Browser.getWindowBounds",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetWindowBoundsResult.model_validate(result)

    async def get_window_for_target(
        self, params: GetWindowForTargetParams | None = None, session_id: str | None = None
    ) -> GetWindowForTargetResult:
        result = await self._client.send_raw(
            method="Browser.getWindowForTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetWindowForTargetResult.model_validate(result)

    async def set_window_bounds(
        self, params: SetWindowBoundsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.setWindowBounds",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_contents_size(
        self, params: SetContentsSizeParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.setContentsSize",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_dock_tile(
        self, params: SetDockTileParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.setDockTile",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def execute_browser_command(
        self, params: ExecuteBrowserCommandParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.executeBrowserCommand",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def add_privacy_sandbox_enrollment_override(
        self, params: AddPrivacySandboxEnrollmentOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.addPrivacySandboxEnrollmentOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def add_privacy_sandbox_coordinator_key_config(
        self, params: AddPrivacySandboxCoordinatorKeyConfigParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Browser.addPrivacySandboxCoordinatorKeyConfig",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
