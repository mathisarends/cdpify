"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    AddScreenParams,
    AddScreenResult,
    CanEmulateResult,
    GetOverriddenSensorInformationParams,
    GetOverriddenSensorInformationResult,
    GetScreenInfosResult,
    RemoveScreenParams,
    SetAutoDarkModeOverrideParams,
    SetAutomationOverrideParams,
    SetCPUThrottlingRateParams,
    SetDataSaverOverrideParams,
    SetDefaultBackgroundColorOverrideParams,
    SetDeviceMetricsOverrideParams,
    SetDevicePostureOverrideParams,
    SetDisabledImageTypesParams,
    SetDisplayFeaturesOverrideParams,
    SetDocumentCookieDisabledParams,
    SetEmitTouchEventsForMouseParams,
    SetEmulatedMediaParams,
    SetEmulatedOSTextScaleParams,
    SetEmulatedVisionDeficiencyParams,
    SetFocusEmulationEnabledParams,
    SetGeolocationOverrideParams,
    SetHardwareConcurrencyOverrideParams,
    SetIdleOverrideParams,
    SetLocaleOverrideParams,
    SetNavigatorOverridesParams,
    SetPageScaleFactorParams,
    SetPressureDataOverrideParams,
    SetPressureSourceOverrideEnabledParams,
    SetPressureStateOverrideParams,
    SetSafeAreaInsetsOverrideParams,
    SetScriptExecutionDisabledParams,
    SetScrollbarsHiddenParams,
    SetSensorOverrideEnabledParams,
    SetSensorOverrideReadingsParams,
    SetSmallViewportHeightDifferenceOverrideParams,
    SetTimezoneOverrideParams,
    SetTouchEmulationEnabledParams,
    SetUserAgentOverrideParams,
    SetVirtualTimePolicyParams,
    SetVirtualTimePolicyResult,
    SetVisibleSizeParams,
)

class EmulationClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def can_emulate(
        self, session_id: str | None = None
    ) -> CanEmulateResult:
        result = await self._client.send_raw(
            method="Emulation.canEmulate",
            params=None,
            session_id=session_id,
        )
        return CanEmulateResult.model_validate(result)

    async def clear_device_metrics_override(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.clearDeviceMetricsOverride",
            params=None,
            session_id=session_id,
        )
        return result

    async def clear_geolocation_override(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.clearGeolocationOverride",
            params=None,
            session_id=session_id,
        )
        return result

    async def reset_page_scale_factor(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.resetPageScaleFactor",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_focus_emulation_enabled(
        self, params: SetFocusEmulationEnabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setFocusEmulationEnabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_auto_dark_mode_override(
        self, params: SetAutoDarkModeOverrideParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setAutoDarkModeOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_c_p_u_throttling_rate(
        self, params: SetCPUThrottlingRateParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setCPUThrottlingRate",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_default_background_color_override(
        self, params: SetDefaultBackgroundColorOverrideParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setDefaultBackgroundColorOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_safe_area_insets_override(
        self, params: SetSafeAreaInsetsOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setSafeAreaInsetsOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_device_metrics_override(
        self, params: SetDeviceMetricsOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setDeviceMetricsOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_device_posture_override(
        self, params: SetDevicePostureOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setDevicePostureOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def clear_device_posture_override(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.clearDevicePostureOverride",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_display_features_override(
        self, params: SetDisplayFeaturesOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setDisplayFeaturesOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def clear_display_features_override(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.clearDisplayFeaturesOverride",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_scrollbars_hidden(
        self, params: SetScrollbarsHiddenParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setScrollbarsHidden",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_document_cookie_disabled(
        self, params: SetDocumentCookieDisabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setDocumentCookieDisabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_emit_touch_events_for_mouse(
        self, params: SetEmitTouchEventsForMouseParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setEmitTouchEventsForMouse",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_emulated_media(
        self, params: SetEmulatedMediaParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setEmulatedMedia",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_emulated_vision_deficiency(
        self, params: SetEmulatedVisionDeficiencyParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setEmulatedVisionDeficiency",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_emulated_o_s_text_scale(
        self, params: SetEmulatedOSTextScaleParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setEmulatedOSTextScale",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_geolocation_override(
        self, params: SetGeolocationOverrideParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setGeolocationOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_overridden_sensor_information(
        self, params: GetOverriddenSensorInformationParams, session_id: str | None = None
    ) -> GetOverriddenSensorInformationResult:
        result = await self._client.send_raw(
            method="Emulation.getOverriddenSensorInformation",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetOverriddenSensorInformationResult.model_validate(result)

    async def set_sensor_override_enabled(
        self, params: SetSensorOverrideEnabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setSensorOverrideEnabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_sensor_override_readings(
        self, params: SetSensorOverrideReadingsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setSensorOverrideReadings",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_pressure_source_override_enabled(
        self, params: SetPressureSourceOverrideEnabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setPressureSourceOverrideEnabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_pressure_state_override(
        self, params: SetPressureStateOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setPressureStateOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_pressure_data_override(
        self, params: SetPressureDataOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setPressureDataOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_idle_override(
        self, params: SetIdleOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setIdleOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def clear_idle_override(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.clearIdleOverride",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_navigator_overrides(
        self, params: SetNavigatorOverridesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setNavigatorOverrides",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_page_scale_factor(
        self, params: SetPageScaleFactorParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setPageScaleFactor",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_script_execution_disabled(
        self, params: SetScriptExecutionDisabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setScriptExecutionDisabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_touch_emulation_enabled(
        self, params: SetTouchEmulationEnabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setTouchEmulationEnabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_virtual_time_policy(
        self, params: SetVirtualTimePolicyParams, session_id: str | None = None
    ) -> SetVirtualTimePolicyResult:
        result = await self._client.send_raw(
            method="Emulation.setVirtualTimePolicy",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetVirtualTimePolicyResult.model_validate(result)

    async def set_locale_override(
        self, params: SetLocaleOverrideParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setLocaleOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_timezone_override(
        self, params: SetTimezoneOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setTimezoneOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_visible_size(
        self, params: SetVisibleSizeParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setVisibleSize",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_disabled_image_types(
        self, params: SetDisabledImageTypesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setDisabledImageTypes",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_data_saver_override(
        self, params: SetDataSaverOverrideParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setDataSaverOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_hardware_concurrency_override(
        self, params: SetHardwareConcurrencyOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setHardwareConcurrencyOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_user_agent_override(
        self, params: SetUserAgentOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setUserAgentOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_automation_override(
        self, params: SetAutomationOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setAutomationOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_small_viewport_height_difference_override(
        self, params: SetSmallViewportHeightDifferenceOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.setSmallViewportHeightDifferenceOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_screen_infos(
        self, session_id: str | None = None
    ) -> GetScreenInfosResult:
        result = await self._client.send_raw(
            method="Emulation.getScreenInfos",
            params=None,
            session_id=session_id,
        )
        return GetScreenInfosResult.model_validate(result)

    async def add_screen(
        self, params: AddScreenParams, session_id: str | None = None
    ) -> AddScreenResult:
        result = await self._client.send_raw(
            method="Emulation.addScreen",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return AddScreenResult.model_validate(result)

    async def remove_screen(
        self, params: RemoveScreenParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Emulation.removeScreen",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
