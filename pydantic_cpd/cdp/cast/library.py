"""Generated client library from CDP specification"""
# Domain: Cast Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    EnableParams,
    SetSinkToUseParams,
    StartDesktopMirroringParams,
    StartTabMirroringParams,
    StopCastingParams,
)


class CastClient:
    """A domain for interacting with Cast, Presentation API, and Remote Playback API
    functionalities."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def enable(
        self, params: EnableParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Starts observing for sinks that can be used for tab mirroring, and if set,
        sinks compatible with |presentationUrl| as well. When sinks are found, a
        |sinksUpdated| event is fired.
        Also starts observing for issue messages. When an issue is added or removed,
        an |issueUpdated| event is fired."""
        result = await self._client.send_raw(
            method="Cast.enable",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Stops observing for sinks and issues."""
        result = await self._client.send_raw(
            method="Cast.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_sink_to_use(
        self, params: SetSinkToUseParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Sets a sink to be used when the web page requests the browser to choose a
        sink via Presentation API, Remote Playback API, or Cast SDK."""
        result = await self._client.send_raw(
            method="Cast.setSinkToUse",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def start_desktop_mirroring(
        self, params: StartDesktopMirroringParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Starts mirroring the desktop to the sink."""
        result = await self._client.send_raw(
            method="Cast.startDesktopMirroring",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def start_tab_mirroring(
        self, params: StartTabMirroringParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Starts mirroring the tab to the sink."""
        result = await self._client.send_raw(
            method="Cast.startTabMirroring",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def stop_casting(
        self, params: StopCastingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Stops the active Cast session on the sink."""
        result = await self._client.send_raw(
            method="Cast.stopCasting",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
