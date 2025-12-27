"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    DeliverPushMessageParams,
    DispatchPeriodicSyncEventParams,
    DispatchSyncEventParams,
    SetForceUpdateOnPageLoadParams,
    SkipWaitingParams,
    StartWorkerParams,
    StopWorkerParams,
    UnregisterParams,
    UpdateRegistrationParams,
)

class ServiceWorkerClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def deliver_push_message(
        self, params: DeliverPushMessageParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="ServiceWorker.deliverPushMessage",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="ServiceWorker.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def dispatch_sync_event(
        self, params: DispatchSyncEventParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="ServiceWorker.dispatchSyncEvent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def dispatch_periodic_sync_event(
        self, params: DispatchPeriodicSyncEventParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="ServiceWorker.dispatchPeriodicSyncEvent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="ServiceWorker.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_force_update_on_page_load(
        self, params: SetForceUpdateOnPageLoadParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="ServiceWorker.setForceUpdateOnPageLoad",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def skip_waiting(
        self, params: SkipWaitingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="ServiceWorker.skipWaiting",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def start_worker(
        self, params: StartWorkerParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="ServiceWorker.startWorker",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def stop_all_workers(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="ServiceWorker.stopAllWorkers",
            params=None,
            session_id=session_id,
        )
        return result

    async def stop_worker(
        self, params: StopWorkerParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="ServiceWorker.stopWorker",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def unregister(
        self, params: UnregisterParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="ServiceWorker.unregister",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def update_registration(
        self, params: UpdateRegistrationParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="ServiceWorker.updateRegistration",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
