"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    ActivateTargetParams,
    AttachToBrowserTargetResult,
    AttachToTargetParams,
    AttachToTargetResult,
    AutoAttachRelatedParams,
    CloseTargetParams,
    CloseTargetResult,
    CreateBrowserContextParams,
    CreateBrowserContextResult,
    CreateTargetParams,
    CreateTargetResult,
    DetachFromTargetParams,
    DisposeBrowserContextParams,
    ExposeDevToolsProtocolParams,
    GetBrowserContextsResult,
    GetDevToolsTargetParams,
    GetDevToolsTargetResult,
    GetTargetInfoParams,
    GetTargetInfoResult,
    GetTargetsParams,
    GetTargetsResult,
    OpenDevToolsParams,
    OpenDevToolsResult,
    SendMessageToTargetParams,
    SetAutoAttachParams,
    SetDiscoverTargetsParams,
    SetRemoteLocationsParams,
)

class TargetClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def activate_target(
        self, params: ActivateTargetParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Target.activateTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def attach_to_target(
        self, params: AttachToTargetParams, session_id: str | None = None
    ) -> AttachToTargetResult:
        result = await self._client.send_raw(
            method="Target.attachToTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return AttachToTargetResult.model_validate(result)

    async def attach_to_browser_target(
        self, session_id: str | None = None
    ) -> AttachToBrowserTargetResult:
        result = await self._client.send_raw(
            method="Target.attachToBrowserTarget",
            params=None,
            session_id=session_id,
        )
        return AttachToBrowserTargetResult.model_validate(result)

    async def close_target(
        self, params: CloseTargetParams, session_id: str | None = None
    ) -> CloseTargetResult:
        result = await self._client.send_raw(
            method="Target.closeTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CloseTargetResult.model_validate(result)

    async def expose_dev_tools_protocol(
        self, params: ExposeDevToolsProtocolParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Target.exposeDevToolsProtocol",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def create_browser_context(
        self, params: CreateBrowserContextParams | None = None, session_id: str | None = None
    ) -> CreateBrowserContextResult:
        result = await self._client.send_raw(
            method="Target.createBrowserContext",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CreateBrowserContextResult.model_validate(result)

    async def get_browser_contexts(
        self, session_id: str | None = None
    ) -> GetBrowserContextsResult:
        result = await self._client.send_raw(
            method="Target.getBrowserContexts",
            params=None,
            session_id=session_id,
        )
        return GetBrowserContextsResult.model_validate(result)

    async def create_target(
        self, params: CreateTargetParams, session_id: str | None = None
    ) -> CreateTargetResult:
        result = await self._client.send_raw(
            method="Target.createTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CreateTargetResult.model_validate(result)

    async def detach_from_target(
        self, params: DetachFromTargetParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Target.detachFromTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def dispose_browser_context(
        self, params: DisposeBrowserContextParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Target.disposeBrowserContext",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_target_info(
        self, params: GetTargetInfoParams | None = None, session_id: str | None = None
    ) -> GetTargetInfoResult:
        result = await self._client.send_raw(
            method="Target.getTargetInfo",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetTargetInfoResult.model_validate(result)

    async def get_targets(
        self, params: GetTargetsParams | None = None, session_id: str | None = None
    ) -> GetTargetsResult:
        result = await self._client.send_raw(
            method="Target.getTargets",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetTargetsResult.model_validate(result)

    async def send_message_to_target(
        self, params: SendMessageToTargetParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Target.sendMessageToTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_auto_attach(
        self, params: SetAutoAttachParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Target.setAutoAttach",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def auto_attach_related(
        self, params: AutoAttachRelatedParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Target.autoAttachRelated",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_discover_targets(
        self, params: SetDiscoverTargetsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Target.setDiscoverTargets",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_remote_locations(
        self, params: SetRemoteLocationsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Target.setRemoteLocations",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_dev_tools_target(
        self, params: GetDevToolsTargetParams, session_id: str | None = None
    ) -> GetDevToolsTargetResult:
        result = await self._client.send_raw(
            method="Target.getDevToolsTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetDevToolsTargetResult.model_validate(result)

    async def open_dev_tools(
        self, params: OpenDevToolsParams, session_id: str | None = None
    ) -> OpenDevToolsResult:
        result = await self._client.send_raw(
            method="Target.openDevTools",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return OpenDevToolsResult.model_validate(result)
