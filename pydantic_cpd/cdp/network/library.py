"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    CanClearBrowserCacheResult,
    CanClearBrowserCookiesResult,
    CanEmulateNetworkConditionsResult,
    ConfigureDurableMessagesParams,
    ContinueInterceptedRequestParams,
    DeleteCookiesParams,
    EmulateNetworkConditionsByRuleParams,
    EmulateNetworkConditionsByRuleResult,
    EmulateNetworkConditionsParams,
    EnableParams,
    EnableReportingApiParams,
    GetAllCookiesResult,
    GetCertificateParams,
    GetCertificateResult,
    GetCookiesParams,
    GetCookiesResult,
    GetRequestPostDataParams,
    GetRequestPostDataResult,
    GetResponseBodyForInterceptionParams,
    GetResponseBodyForInterceptionResult,
    GetResponseBodyParams,
    GetResponseBodyResult,
    GetSecurityIsolationStatusParams,
    GetSecurityIsolationStatusResult,
    LoadNetworkResourceParams,
    LoadNetworkResourceResult,
    OverrideNetworkStateParams,
    ReplayXHRParams,
    SearchInResponseBodyParams,
    SearchInResponseBodyResult,
    SetAcceptedEncodingsParams,
    SetAttachDebugStackParams,
    SetBlockedURLsParams,
    SetBypassServiceWorkerParams,
    SetCacheDisabledParams,
    SetCookieControlsParams,
    SetCookieParams,
    SetCookieResult,
    SetCookiesParams,
    SetExtraHTTPHeadersParams,
    SetRequestInterceptionParams,
    SetUserAgentOverrideParams,
    StreamResourceContentParams,
    StreamResourceContentResult,
    TakeResponseBodyForInterceptionAsStreamParams,
    TakeResponseBodyForInterceptionAsStreamResult,
)

class NetworkClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def set_accepted_encodings(
        self, params: SetAcceptedEncodingsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.setAcceptedEncodings",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def clear_accepted_encodings_override(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.clearAcceptedEncodingsOverride",
            params=None,
            session_id=session_id,
        )
        return result

    async def can_clear_browser_cache(
        self, session_id: str | None = None
    ) -> CanClearBrowserCacheResult:
        result = await self._client.send_raw(
            method="Network.canClearBrowserCache",
            params=None,
            session_id=session_id,
        )
        return CanClearBrowserCacheResult.model_validate(result)

    async def can_clear_browser_cookies(
        self, session_id: str | None = None
    ) -> CanClearBrowserCookiesResult:
        result = await self._client.send_raw(
            method="Network.canClearBrowserCookies",
            params=None,
            session_id=session_id,
        )
        return CanClearBrowserCookiesResult.model_validate(result)

    async def can_emulate_network_conditions(
        self, session_id: str | None = None
    ) -> CanEmulateNetworkConditionsResult:
        result = await self._client.send_raw(
            method="Network.canEmulateNetworkConditions",
            params=None,
            session_id=session_id,
        )
        return CanEmulateNetworkConditionsResult.model_validate(result)

    async def clear_browser_cache(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.clearBrowserCache",
            params=None,
            session_id=session_id,
        )
        return result

    async def clear_browser_cookies(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.clearBrowserCookies",
            params=None,
            session_id=session_id,
        )
        return result

    async def continue_intercepted_request(
        self, params: ContinueInterceptedRequestParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.continueInterceptedRequest",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def delete_cookies(
        self, params: DeleteCookiesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.deleteCookies",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def emulate_network_conditions(
        self, params: EmulateNetworkConditionsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.emulateNetworkConditions",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def emulate_network_conditions_by_rule(
        self, params: EmulateNetworkConditionsByRuleParams, session_id: str | None = None
    ) -> EmulateNetworkConditionsByRuleResult:
        result = await self._client.send_raw(
            method="Network.emulateNetworkConditionsByRule",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return EmulateNetworkConditionsByRuleResult.model_validate(result)

    async def override_network_state(
        self, params: OverrideNetworkStateParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.overrideNetworkState",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, params: EnableParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.enable",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def configure_durable_messages(
        self, params: ConfigureDurableMessagesParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.configureDurableMessages",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_all_cookies(
        self, session_id: str | None = None
    ) -> GetAllCookiesResult:
        result = await self._client.send_raw(
            method="Network.getAllCookies",
            params=None,
            session_id=session_id,
        )
        return GetAllCookiesResult.model_validate(result)

    async def get_certificate(
        self, params: GetCertificateParams, session_id: str | None = None
    ) -> GetCertificateResult:
        result = await self._client.send_raw(
            method="Network.getCertificate",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetCertificateResult.model_validate(result)

    async def get_cookies(
        self, params: GetCookiesParams | None = None, session_id: str | None = None
    ) -> GetCookiesResult:
        result = await self._client.send_raw(
            method="Network.getCookies",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetCookiesResult.model_validate(result)

    async def get_response_body(
        self, params: GetResponseBodyParams, session_id: str | None = None
    ) -> GetResponseBodyResult:
        result = await self._client.send_raw(
            method="Network.getResponseBody",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetResponseBodyResult.model_validate(result)

    async def get_request_post_data(
        self, params: GetRequestPostDataParams, session_id: str | None = None
    ) -> GetRequestPostDataResult:
        result = await self._client.send_raw(
            method="Network.getRequestPostData",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetRequestPostDataResult.model_validate(result)

    async def get_response_body_for_interception(
        self, params: GetResponseBodyForInterceptionParams, session_id: str | None = None
    ) -> GetResponseBodyForInterceptionResult:
        result = await self._client.send_raw(
            method="Network.getResponseBodyForInterception",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetResponseBodyForInterceptionResult.model_validate(result)

    async def take_response_body_for_interception_as_stream(
        self, params: TakeResponseBodyForInterceptionAsStreamParams, session_id: str | None = None
    ) -> TakeResponseBodyForInterceptionAsStreamResult:
        result = await self._client.send_raw(
            method="Network.takeResponseBodyForInterceptionAsStream",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return TakeResponseBodyForInterceptionAsStreamResult.model_validate(result)

    async def replay_x_h_r(
        self, params: ReplayXHRParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.replayXHR",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def search_in_response_body(
        self, params: SearchInResponseBodyParams, session_id: str | None = None
    ) -> SearchInResponseBodyResult:
        result = await self._client.send_raw(
            method="Network.searchInResponseBody",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SearchInResponseBodyResult.model_validate(result)

    async def set_blocked_u_r_ls(
        self, params: SetBlockedURLsParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.setBlockedURLs",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_bypass_service_worker(
        self, params: SetBypassServiceWorkerParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.setBypassServiceWorker",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_cache_disabled(
        self, params: SetCacheDisabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.setCacheDisabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_cookie(
        self, params: SetCookieParams, session_id: str | None = None
    ) -> SetCookieResult:
        result = await self._client.send_raw(
            method="Network.setCookie",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetCookieResult.model_validate(result)

    async def set_cookies(
        self, params: SetCookiesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.setCookies",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_extra_h_t_t_p_headers(
        self, params: SetExtraHTTPHeadersParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.setExtraHTTPHeaders",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_attach_debug_stack(
        self, params: SetAttachDebugStackParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.setAttachDebugStack",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_request_interception(
        self, params: SetRequestInterceptionParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.setRequestInterception",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_user_agent_override(
        self, params: SetUserAgentOverrideParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.setUserAgentOverride",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def stream_resource_content(
        self, params: StreamResourceContentParams, session_id: str | None = None
    ) -> StreamResourceContentResult:
        result = await self._client.send_raw(
            method="Network.streamResourceContent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return StreamResourceContentResult.model_validate(result)

    async def get_security_isolation_status(
        self, params: GetSecurityIsolationStatusParams | None = None, session_id: str | None = None
    ) -> GetSecurityIsolationStatusResult:
        result = await self._client.send_raw(
            method="Network.getSecurityIsolationStatus",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetSecurityIsolationStatusResult.model_validate(result)

    async def enable_reporting_api(
        self, params: EnableReportingApiParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.enableReportingApi",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def load_network_resource(
        self, params: LoadNetworkResourceParams, session_id: str | None = None
    ) -> LoadNetworkResourceResult:
        result = await self._client.send_raw(
            method="Network.loadNetworkResource",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return LoadNetworkResourceResult.model_validate(result)

    async def set_cookie_controls(
        self, params: SetCookieControlsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Network.setCookieControls",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
