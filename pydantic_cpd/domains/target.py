"""Generated from CDP specification"""

from pydantic_cpd.domains.base import CDPModel
from typing import Literal, Any

from pydantic_cpd.domains import browser
from pydantic_cpd.domains import page

# Alias for cross-domain type references
Browser = browser
Page = page


TargetID = str
SessionID = str


class TargetInfo(CDPModel):
    target_id: TargetID
    type: str
    title: str
    url: str
    attached: bool
    opener_id: TargetID | None = None
    can_access_opener: bool
    opener_frame_id: Page.FrameId | None = None
    parent_frame_id: Page.FrameId | None = None
    browser_context_id: Browser.BrowserContextID | None = None
    subtype: str | None = None


class FilterEntry(CDPModel):
    """A filter used by target query/discovery/auto-attach operations."""

    exclude: bool | None = None
    type: str | None = None


TargetFilter = list[Any]


class RemoteLocation(CDPModel):
    host: str
    port: int


WindowState = Literal["normal", "minimized", "maximized", "fullscreen"]


class ActivatetargetParams(CDPModel):
    """Activates (focuses) the target."""

    target_id: TargetID


class AttachtotargetParams(CDPModel):
    """Attaches to the target with given id."""

    target_id: TargetID
    flatten: bool | None = None


class AttachtotargetResult(CDPModel):
    session_id: SessionID


class AttachtobrowsertargetResult(CDPModel):
    session_id: SessionID


class ClosetargetParams(CDPModel):
    """Closes the target. If the target is a page that gets closed too."""

    target_id: TargetID


class ClosetargetResult(CDPModel):
    success: bool


class ExposedevtoolsprotocolParams(CDPModel):
    """
    Inject object to the target's main frame that provides a communication channel with
    browser target.  Injected object will be available as `window[bindingName]`.  The
    object has the following API: - `binding.send(json)` - a method to send messages
    over the remote debugging protocol - `binding.onmessage = json =>
    handleMessage(json)` - a callback that will be called for the protocol notifications
    and command responses.
    """

    target_id: TargetID
    binding_name: str | None = None
    inherit_permissions: bool | None = None


class CreatebrowsercontextParams(CDPModel):
    """
    Creates a new empty BrowserContext. Similar to an incognito profile but you can have
    more than one.
    """

    dispose_on_detach: bool | None = None
    proxy_server: str | None = None
    proxy_bypass_list: str | None = None
    origins_with_universal_network_access: list[str] | None = None


class CreatebrowsercontextResult(CDPModel):
    browser_context_id: Browser.BrowserContextID


class GetbrowsercontextsResult(CDPModel):
    browser_context_ids: list[Browser.BrowserContextID]
    default_browser_context_id: Browser.BrowserContextID | None = None


class CreatetargetParams(CDPModel):
    """Creates a new page."""

    url: str
    left: int | None = None
    top: int | None = None
    width: int | None = None
    height: int | None = None
    window_state: WindowState | None = None
    browser_context_id: Browser.BrowserContextID | None = None
    enable_begin_frame_control: bool | None = None
    new_window: bool | None = None
    background: bool | None = None
    for_tab: bool | None = None
    hidden: bool | None = None


class CreatetargetResult(CDPModel):
    target_id: TargetID


class DetachfromtargetParams(CDPModel):
    """Detaches session with given id."""

    session_id: SessionID | None = None
    target_id: TargetID | None = None


class DisposebrowsercontextParams(CDPModel):
    """
    Deletes a BrowserContext. All the belonging pages will be closed without calling
    their beforeunload hooks.
    """

    browser_context_id: Browser.BrowserContextID


class GettargetinfoParams(CDPModel):
    """Returns information about a target."""

    target_id: TargetID | None = None


class GettargetinfoResult(CDPModel):
    target_info: TargetInfo


class GettargetsParams(CDPModel):
    """Retrieves a list of available targets."""

    filter: TargetFilter | None = None


class GettargetsResult(CDPModel):
    target_infos: list[TargetInfo]


class SendmessagetotargetParams(CDPModel):
    """
    Sends protocol message over session with given id. Consider using flat mode instead;
    see commands attachToTarget, setAutoAttach, and crbug.com/991325.
    """

    message: str
    session_id: SessionID | None = None
    target_id: TargetID | None = None


class SetautoattachParams(CDPModel):
    """
    Controls whether to automatically attach to new targets which are considered to be
    directly related to this one (for example, iframes or workers). When turned on,
    attaches to all existing related targets as well. When turned off, automatically
    detaches from all currently attached targets. This also clears all targets added by
    `autoAttachRelated` from the list of targets to watch for creation of related
    targets. You might want to call this recursively for auto-attached targets to attach
    to all available targets.
    """

    auto_attach: bool
    wait_for_debugger_on_start: bool
    flatten: bool | None = None
    filter: TargetFilter | None = None


class AutoattachrelatedParams(CDPModel):
    """
    Adds the specified target to the list of targets that will be monitored for any
    related target creation (such as child frames, child workers and new versions of
    service worker) and reported through `attachedToTarget`. The specified target is
    also auto-attached. This cancels the effect of any previous `setAutoAttach` and is
    also cancelled by subsequent `setAutoAttach`. Only available at the Browser target.
    """

    target_id: TargetID
    wait_for_debugger_on_start: bool
    filter: TargetFilter | None = None


class SetdiscovertargetsParams(CDPModel):
    """
    Controls whether to discover available targets and notify via
    `targetCreated/targetInfoChanged/targetDestroyed` events.
    """

    discover: bool
    filter: TargetFilter | None = None


class SetremotelocationsParams(CDPModel):
    """
    Enables target discovery for the specified locations, when `setDiscoverTargets` was
    set to `true`.
    """

    locations: list[RemoteLocation]


class GetdevtoolstargetParams(CDPModel):
    """
    Gets the targetId of the DevTools page target opened for the given target (if any).
    """

    target_id: TargetID


class GetdevtoolstargetResult(CDPModel):
    target_id: TargetID | None = None


class OpendevtoolsParams(CDPModel):
    """Opens a DevTools window for the target."""

    target_id: TargetID
    panel_id: str | None = None


class OpendevtoolsResult(CDPModel):
    target_id: TargetID


class TargetClient:
    """Supports additional targets discovery and allows to attach to them."""

    def __init__(self, cdp_client: Any) -> None:
        self._cdp = cdp_client

    async def activate_target(self, target_id: TargetID) -> None:
        """Activates (focuses) the target."""
        params = ActivatetargetParams(
            target_id=target_id,
        )
        result = await self._cdp.call(
            "Target.activateTarget", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def attach_to_target(
        self, target_id: TargetID, flatten: bool | None = None
    ) -> AttachtotargetResult:
        """Attaches to the target with given id."""
        params = AttachtotargetParams(
            target_id=target_id,
            flatten=flatten,
        )
        result = await self._cdp.call(
            "Target.attachToTarget", params.model_dump(by_alias=True, exclude_none=True)
        )
        return AttachtotargetResult(**result)

    async def attach_to_browser_target(self) -> AttachtobrowsertargetResult:
        """Attaches to the browser target, only uses flat sessionId mode."""
        result = await self._cdp.call("Target.attachToBrowserTarget", {})
        return AttachtobrowsertargetResult(**result)

    async def close_target(self, target_id: TargetID) -> ClosetargetResult:
        """Closes the target. If the target is a page that gets closed too."""
        params = ClosetargetParams(
            target_id=target_id,
        )
        result = await self._cdp.call(
            "Target.closeTarget", params.model_dump(by_alias=True, exclude_none=True)
        )
        return ClosetargetResult(**result)

    async def expose_dev_tools_protocol(
        self,
        target_id: TargetID,
        binding_name: str | None = None,
        inherit_permissions: bool | None = None,
    ) -> None:
        """
        Inject object to the target's main frame that provides a communication channel
        with browser target.  Injected object will be available as
        `window[bindingName]`.  The object has the following API: - `binding.send(json)`
        - a method to send messages over the remote debugging protocol -
        `binding.onmessage = json => handleMessage(json)` - a callback that will be
        called for the protocol notifications and command responses.
        """
        params = ExposedevtoolsprotocolParams(
            target_id=target_id,
            binding_name=binding_name,
            inherit_permissions=inherit_permissions,
        )
        result = await self._cdp.call(
            "Target.exposeDevToolsProtocol",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def create_browser_context(
        self,
        dispose_on_detach: bool | None = None,
        proxy_server: str | None = None,
        proxy_bypass_list: str | None = None,
        origins_with_universal_network_access: list[str] | None = None,
    ) -> CreatebrowsercontextResult:
        """
        Creates a new empty BrowserContext. Similar to an incognito profile but you can
        have more than one.
        """
        params = CreatebrowsercontextParams(
            dispose_on_detach=dispose_on_detach,
            proxy_server=proxy_server,
            proxy_bypass_list=proxy_bypass_list,
            origins_with_universal_network_access=origins_with_universal_network_access,
        )
        result = await self._cdp.call(
            "Target.createBrowserContext",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return CreatebrowsercontextResult(**result)

    async def get_browser_contexts(self) -> GetbrowsercontextsResult:
        """
        Returns all browser contexts created with `Target.createBrowserContext` method.
        """
        result = await self._cdp.call("Target.getBrowserContexts", {})
        return GetbrowsercontextsResult(**result)

    async def create_target(
        self,
        url: str,
        left: int | None = None,
        top: int | None = None,
        width: int | None = None,
        height: int | None = None,
        window_state: WindowState | None = None,
        browser_context_id: Browser.BrowserContextID | None = None,
        enable_begin_frame_control: bool | None = None,
        new_window: bool | None = None,
        background: bool | None = None,
        for_tab: bool | None = None,
        hidden: bool | None = None,
    ) -> CreatetargetResult:
        """Creates a new page."""
        params = CreatetargetParams(
            url=url,
            left=left,
            top=top,
            width=width,
            height=height,
            window_state=window_state,
            browser_context_id=browser_context_id,
            enable_begin_frame_control=enable_begin_frame_control,
            new_window=new_window,
            background=background,
            for_tab=for_tab,
            hidden=hidden,
        )
        result = await self._cdp.call(
            "Target.createTarget", params.model_dump(by_alias=True, exclude_none=True)
        )
        return CreatetargetResult(**result)

    async def detach_from_target(
        self, session_id: SessionID | None = None, target_id: TargetID | None = None
    ) -> None:
        """Detaches session with given id."""
        params = DetachfromtargetParams(
            session_id=session_id,
            target_id=target_id,
        )
        result = await self._cdp.call(
            "Target.detachFromTarget",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def dispose_browser_context(
        self, browser_context_id: Browser.BrowserContextID
    ) -> None:
        """
        Deletes a BrowserContext. All the belonging pages will be closed without calling
        their beforeunload hooks.
        """
        params = DisposebrowsercontextParams(
            browser_context_id=browser_context_id,
        )
        result = await self._cdp.call(
            "Target.disposeBrowserContext",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def get_target_info(
        self, target_id: TargetID | None = None
    ) -> GettargetinfoResult:
        """Returns information about a target."""
        params = GettargetinfoParams(
            target_id=target_id,
        )
        result = await self._cdp.call(
            "Target.getTargetInfo", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GettargetinfoResult(**result)

    async def get_targets(self, filter: TargetFilter | None = None) -> GettargetsResult:
        """Retrieves a list of available targets."""
        params = GettargetsParams(
            filter=filter,
        )
        result = await self._cdp.call(
            "Target.getTargets", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GettargetsResult(**result)

    async def send_message_to_target(
        self,
        message: str,
        session_id: SessionID | None = None,
        target_id: TargetID | None = None,
    ) -> None:
        """
        Sends protocol message over session with given id. Consider using flat mode
        instead; see commands attachToTarget, setAutoAttach, and crbug.com/991325.
        """
        params = SendmessagetotargetParams(
            message=message,
            session_id=session_id,
            target_id=target_id,
        )
        result = await self._cdp.call(
            "Target.sendMessageToTarget",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_auto_attach(
        self,
        auto_attach: bool,
        wait_for_debugger_on_start: bool,
        flatten: bool | None = None,
        filter: TargetFilter | None = None,
    ) -> None:
        """
        Controls whether to automatically attach to new targets which are considered to
        be directly related to this one (for example, iframes or workers). When turned
        on, attaches to all existing related targets as well. When turned off,
        automatically detaches from all currently attached targets. This also clears all
        targets added by `autoAttachRelated` from the list of targets to watch for
        creation of related targets. You might want to call this recursively for auto-
        attached targets to attach to all available targets.
        """
        params = SetautoattachParams(
            auto_attach=auto_attach,
            wait_for_debugger_on_start=wait_for_debugger_on_start,
            flatten=flatten,
            filter=filter,
        )
        result = await self._cdp.call(
            "Target.setAutoAttach", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def auto_attach_related(
        self,
        target_id: TargetID,
        wait_for_debugger_on_start: bool,
        filter: TargetFilter | None = None,
    ) -> None:
        """
        Adds the specified target to the list of targets that will be monitored for any
        related target creation (such as child frames, child workers and new versions of
        service worker) and reported through `attachedToTarget`. The specified target is
        also auto-attached. This cancels the effect of any previous `setAutoAttach` and
        is also cancelled by subsequent `setAutoAttach`. Only available at the Browser
        target.
        """
        params = AutoattachrelatedParams(
            target_id=target_id,
            wait_for_debugger_on_start=wait_for_debugger_on_start,
            filter=filter,
        )
        result = await self._cdp.call(
            "Target.autoAttachRelated",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_discover_targets(
        self, discover: bool, filter: TargetFilter | None = None
    ) -> None:
        """
        Controls whether to discover available targets and notify via
        `targetCreated/targetInfoChanged/targetDestroyed` events.
        """
        params = SetdiscovertargetsParams(
            discover=discover,
            filter=filter,
        )
        result = await self._cdp.call(
            "Target.setDiscoverTargets",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_remote_locations(self, locations: list[RemoteLocation]) -> None:
        """
        Enables target discovery for the specified locations, when `setDiscoverTargets`
        was set to `true`.
        """
        params = SetremotelocationsParams(
            locations=locations,
        )
        result = await self._cdp.call(
            "Target.setRemoteLocations",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def get_dev_tools_target(
        self, target_id: TargetID
    ) -> GetdevtoolstargetResult:
        """
        Gets the targetId of the DevTools page target opened for the given target (if
        any).
        """
        params = GetdevtoolstargetParams(
            target_id=target_id,
        )
        result = await self._cdp.call(
            "Target.getDevToolsTarget",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetdevtoolstargetResult(**result)

    async def open_dev_tools(
        self, target_id: TargetID, panel_id: str | None = None
    ) -> OpendevtoolsResult:
        """Opens a DevTools window for the target."""
        params = OpendevtoolsParams(
            target_id=target_id,
            panel_id=panel_id,
        )
        result = await self._cdp.call(
            "Target.openDevTools", params.model_dump(by_alias=True, exclude_none=True)
        )
        return OpendevtoolsResult(**result)
