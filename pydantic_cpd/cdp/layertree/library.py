"""Generated client library from CDP specification"""
# Domain: LayerTree Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    CompositingReasonsParams,
    CompositingReasonsResult,
    LoadSnapshotParams,
    LoadSnapshotResult,
    MakeSnapshotParams,
    MakeSnapshotResult,
    ProfileSnapshotParams,
    ProfileSnapshotResult,
    ReleaseSnapshotParams,
    ReplaySnapshotParams,
    ReplaySnapshotResult,
    SnapshotCommandLogParams,
    SnapshotCommandLogResult,
)


class LayerTreeClient:
    """CDP LayerTree domain client."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def compositing_reasons(
        self, params: CompositingReasonsParams, session_id: str | None = None
    ) -> CompositingReasonsResult:
        """Provides the reasons why the given layer was composited."""
        result = await self._client.send_raw(
            method="LayerTree.compositingReasons",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CompositingReasonsResult.model_validate(result)

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables compositing tree inspection."""
        result = await self._client.send_raw(
            method="LayerTree.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        """Enables compositing tree inspection."""
        result = await self._client.send_raw(
            method="LayerTree.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def load_snapshot(
        self, params: LoadSnapshotParams, session_id: str | None = None
    ) -> LoadSnapshotResult:
        """Returns the snapshot identifier."""
        result = await self._client.send_raw(
            method="LayerTree.loadSnapshot",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return LoadSnapshotResult.model_validate(result)

    async def make_snapshot(
        self, params: MakeSnapshotParams, session_id: str | None = None
    ) -> MakeSnapshotResult:
        """Returns the layer snapshot identifier."""
        result = await self._client.send_raw(
            method="LayerTree.makeSnapshot",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return MakeSnapshotResult.model_validate(result)

    async def profile_snapshot(
        self, params: ProfileSnapshotParams, session_id: str | None = None
    ) -> ProfileSnapshotResult:
        result = await self._client.send_raw(
            method="LayerTree.profileSnapshot",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return ProfileSnapshotResult.model_validate(result)

    async def release_snapshot(
        self, params: ReleaseSnapshotParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Releases layer snapshot captured by the back-end."""
        result = await self._client.send_raw(
            method="LayerTree.releaseSnapshot",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def replay_snapshot(
        self, params: ReplaySnapshotParams, session_id: str | None = None
    ) -> ReplaySnapshotResult:
        """Replays the layer snapshot and returns the resulting bitmap."""
        result = await self._client.send_raw(
            method="LayerTree.replaySnapshot",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return ReplaySnapshotResult.model_validate(result)

    async def snapshot_command_log(
        self, params: SnapshotCommandLogParams, session_id: str | None = None
    ) -> SnapshotCommandLogResult:
        """Replays the layer snapshot and returns canvas log."""
        result = await self._client.send_raw(
            method="LayerTree.snapshotCommandLog",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SnapshotCommandLogResult.model_validate(result)
