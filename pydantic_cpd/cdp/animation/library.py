"""Generated client library from CDP specification"""
# Domain: Animation Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    GetCurrentTimeParams,
    GetCurrentTimeResult,
    GetPlaybackRateResult,
    ReleaseAnimationsParams,
    ResolveAnimationParams,
    ResolveAnimationResult,
    SeekAnimationsParams,
    SetPausedParams,
    SetPlaybackRateParams,
    SetTimingParams,
)


class AnimationClient:
    """CDP Animation domain client."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables animation domain notifications."""
        result = await self._client.send_raw(
            method="Animation.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        """Enables animation domain notifications."""
        result = await self._client.send_raw(
            method="Animation.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def get_current_time(
        self, params: GetCurrentTimeParams, session_id: str | None = None
    ) -> GetCurrentTimeResult:
        """Returns the current time of the an animation."""
        result = await self._client.send_raw(
            method="Animation.getCurrentTime",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetCurrentTimeResult.model_validate(result)

    async def get_playback_rate(
        self, session_id: str | None = None
    ) -> GetPlaybackRateResult:
        """Gets the playback rate of the document timeline."""
        result = await self._client.send_raw(
            method="Animation.getPlaybackRate",
            params=None,
            session_id=session_id,
        )
        return GetPlaybackRateResult.model_validate(result)

    async def release_animations(
        self, params: ReleaseAnimationsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Releases a set of animations to no longer be manipulated."""
        result = await self._client.send_raw(
            method="Animation.releaseAnimations",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def resolve_animation(
        self, params: ResolveAnimationParams, session_id: str | None = None
    ) -> ResolveAnimationResult:
        """Gets the remote object of the Animation."""
        result = await self._client.send_raw(
            method="Animation.resolveAnimation",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return ResolveAnimationResult.model_validate(result)

    async def seek_animations(
        self, params: SeekAnimationsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Seek a set of animations to a particular time within each animation."""
        result = await self._client.send_raw(
            method="Animation.seekAnimations",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_paused(
        self, params: SetPausedParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Sets the paused state of a set of animations."""
        result = await self._client.send_raw(
            method="Animation.setPaused",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_playback_rate(
        self, params: SetPlaybackRateParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Sets the playback rate of the document timeline."""
        result = await self._client.send_raw(
            method="Animation.setPlaybackRate",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_timing(
        self, params: SetTimingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Sets the timing of an animation node."""
        result = await self._client.send_raw(
            method="Animation.setTiming",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
