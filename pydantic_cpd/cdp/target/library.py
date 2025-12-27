"""Generated client library from CDP specification"""
# Domain: Target Client

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
    """Supports additional targets discovery and allows to attach to them."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def activate_target(
        self, params: ActivateTargetParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Activates (focuses) the target."""
        result = await self._client.send_raw(
            method="Target.activateTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def attach_to_target(
        self, params: AttachToTargetParams, session_id: str | None = None
    ) -> AttachToTargetResult:
        """Attaches to the target with given id."""
        result = await self._client.send_raw(
            method="Target.attachToTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return AttachToTargetResult.model_validate(result)

    async def attach_to_browser_target(
        self, session_id: str | None = None
    ) -> AttachToBrowserTargetResult:
        """Attaches to the browser target, only uses flat sessionId mode."""
        result = await self._client.send_raw(
            method="Target.attachToBrowserTarget",
            params=None,
            session_id=session_id,
        )
        return AttachToBrowserTargetResult.model_validate(result)

    async def close_target(
        self, params: CloseTargetParams, session_id: str | None = None
    ) -> CloseTargetResult:
        """Closes the target. If the target is a page that gets closed too."""
        result = await self._client.send_raw(
            method="Target.closeTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CloseTargetResult.model_validate(result)

    async def expose_dev_tools_protocol(
        self, params: ExposeDevToolsProtocolParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Inject object to the target's main frame that provides a communication
        channel with browser target.

        Injected object will be available as `window[bindingName]`.

        The object has the following API:
        - `binding.send(json)` - a method to send messages over the remote debugging protocol
        - `binding.onmessage = json => handleMessage(json)` - a callback that will be called for the protocol notifications and command responses."""
        result = await self._client.send_raw(
            method="Target.exposeDevToolsProtocol",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def create_browser_context(
        self,
        params: CreateBrowserContextParams | None = None,
        session_id: str | None = None,
    ) -> CreateBrowserContextResult:
        """Creates a new empty BrowserContext. Similar to an incognito profile but you can have more than
        one."""
        result = await self._client.send_raw(
            method="Target.createBrowserContext",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CreateBrowserContextResult.model_validate(result)

    async def get_browser_contexts(
        self, session_id: str | None = None
    ) -> GetBrowserContextsResult:
        """Returns all browser contexts created with `Target.createBrowserContext` method."""
        result = await self._client.send_raw(
            method="Target.getBrowserContexts",
            params=None,
            session_id=session_id,
        )
        return GetBrowserContextsResult.model_validate(result)

    async def create_target(
        self, params: CreateTargetParams, session_id: str | None = None
    ) -> CreateTargetResult:
        """Creates a new page."""
        result = await self._client.send_raw(
            method="Target.createTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CreateTargetResult.model_validate(result)

    async def detach_from_target(
        self,
        params: DetachFromTargetParams | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Detaches session with given id."""
        result = await self._client.send_raw(
            method="Target.detachFromTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def dispose_browser_context(
        self, params: DisposeBrowserContextParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Deletes a BrowserContext. All the belonging pages will be closed without calling their
        beforeunload hooks."""
        result = await self._client.send_raw(
            method="Target.disposeBrowserContext",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_target_info(
        self, params: GetTargetInfoParams | None = None, session_id: str | None = None
    ) -> GetTargetInfoResult:
        """Returns information about a target."""
        result = await self._client.send_raw(
            method="Target.getTargetInfo",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetTargetInfoResult.model_validate(result)

    async def get_targets(
        self, params: GetTargetsParams | None = None, session_id: str | None = None
    ) -> GetTargetsResult:
        """Retrieves a list of available targets."""
        result = await self._client.send_raw(
            method="Target.getTargets",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetTargetsResult.model_validate(result)

    async def send_message_to_target(
        self, params: SendMessageToTargetParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Sends protocol message over session with given id.
        Consider using flat mode instead; see commands attachToTarget, setAutoAttach,
        and crbug.com/991325."""
        result = await self._client.send_raw(
            method="Target.sendMessageToTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_auto_attach(
        self, params: SetAutoAttachParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Controls whether to automatically attach to new targets which are considered
        to be directly related to this one (for example, iframes or workers).
        When turned on, attaches to all existing related targets as well. When turned off,
        automatically detaches from all currently attached targets.
        This also clears all targets added by `autoAttachRelated` from the list of targets to watch
        for creation of related targets.
        You might want to call this recursively for auto-attached targets to attach
        to all available targets."""
        result = await self._client.send_raw(
            method="Target.setAutoAttach",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def auto_attach_related(
        self, params: AutoAttachRelatedParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Adds the specified target to the list of targets that will be monitored for any related target
        creation (such as child frames, child workers and new versions of service worker) and reported
        through `attachedToTarget`. The specified target is also auto-attached.
        This cancels the effect of any previous `setAutoAttach` and is also cancelled by subsequent
        `setAutoAttach`. Only available at the Browser target."""
        result = await self._client.send_raw(
            method="Target.autoAttachRelated",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_discover_targets(
        self, params: SetDiscoverTargetsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Controls whether to discover available targets and notify via
        `targetCreated/targetInfoChanged/targetDestroyed` events."""
        result = await self._client.send_raw(
            method="Target.setDiscoverTargets",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_remote_locations(
        self, params: SetRemoteLocationsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enables target discovery for the specified locations, when `setDiscoverTargets` was set to
        `true`."""
        result = await self._client.send_raw(
            method="Target.setRemoteLocations",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_dev_tools_target(
        self, params: GetDevToolsTargetParams, session_id: str | None = None
    ) -> GetDevToolsTargetResult:
        """Gets the targetId of the DevTools page target opened for the given target
        (if any)."""
        result = await self._client.send_raw(
            method="Target.getDevToolsTarget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetDevToolsTargetResult.model_validate(result)

    async def open_dev_tools(
        self, params: OpenDevToolsParams, session_id: str | None = None
    ) -> OpenDevToolsResult:
        """Opens a DevTools window for the target."""
        result = await self._client.send_raw(
            method="Target.openDevTools",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return OpenDevToolsResult.model_validate(result)
