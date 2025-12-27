"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    ClearCookiesParams,
    ClearDataForOriginParams,
    ClearDataForStorageKeyParams,
    ClearSharedStorageEntriesParams,
    ClearTrustTokensParams,
    ClearTrustTokensResult,
    DeleteSharedStorageEntryParams,
    DeleteStorageBucketParams,
    GetAffectedUrlsForThirdPartyCookieMetadataParams,
    GetAffectedUrlsForThirdPartyCookieMetadataResult,
    GetCookiesParams,
    GetCookiesResult,
    GetInterestGroupDetailsParams,
    GetInterestGroupDetailsResult,
    GetRelatedWebsiteSetsResult,
    GetSharedStorageEntriesParams,
    GetSharedStorageEntriesResult,
    GetSharedStorageMetadataParams,
    GetSharedStorageMetadataResult,
    GetStorageKeyForFrameParams,
    GetStorageKeyForFrameResult,
    GetStorageKeyParams,
    GetStorageKeyResult,
    GetTrustTokensResult,
    GetUsageAndQuotaParams,
    GetUsageAndQuotaResult,
    OverrideQuotaForOriginParams,
    ResetSharedStorageBudgetParams,
    RunBounceTrackingMitigationsResult,
    SendPendingAttributionReportsResult,
    SetAttributionReportingLocalTestingModeParams,
    SetAttributionReportingTrackingParams,
    SetCookiesParams,
    SetInterestGroupAuctionTrackingParams,
    SetInterestGroupTrackingParams,
    SetProtectedAudienceKAnonymityParams,
    SetSharedStorageEntryParams,
    SetSharedStorageTrackingParams,
    SetStorageBucketTrackingParams,
    TrackCacheStorageForOriginParams,
    TrackCacheStorageForStorageKeyParams,
    TrackIndexedDBForOriginParams,
    TrackIndexedDBForStorageKeyParams,
    UntrackCacheStorageForOriginParams,
    UntrackCacheStorageForStorageKeyParams,
    UntrackIndexedDBForOriginParams,
    UntrackIndexedDBForStorageKeyParams,
)

class StorageClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def get_storage_key_for_frame(
        self, params: GetStorageKeyForFrameParams, session_id: str | None = None
    ) -> GetStorageKeyForFrameResult:
        result = await self._client.send_raw(
            method="Storage.getStorageKeyForFrame",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetStorageKeyForFrameResult.model_validate(result)

    async def get_storage_key(
        self, params: GetStorageKeyParams | None = None, session_id: str | None = None
    ) -> GetStorageKeyResult:
        result = await self._client.send_raw(
            method="Storage.getStorageKey",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetStorageKeyResult.model_validate(result)

    async def clear_data_for_origin(
        self, params: ClearDataForOriginParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.clearDataForOrigin",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def clear_data_for_storage_key(
        self, params: ClearDataForStorageKeyParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.clearDataForStorageKey",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_cookies(
        self, params: GetCookiesParams | None = None, session_id: str | None = None
    ) -> GetCookiesResult:
        result = await self._client.send_raw(
            method="Storage.getCookies",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetCookiesResult.model_validate(result)

    async def set_cookies(
        self, params: SetCookiesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.setCookies",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def clear_cookies(
        self, params: ClearCookiesParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.clearCookies",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_usage_and_quota(
        self, params: GetUsageAndQuotaParams, session_id: str | None = None
    ) -> GetUsageAndQuotaResult:
        result = await self._client.send_raw(
            method="Storage.getUsageAndQuota",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetUsageAndQuotaResult.model_validate(result)

    async def override_quota_for_origin(
        self, params: OverrideQuotaForOriginParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.overrideQuotaForOrigin",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def track_cache_storage_for_origin(
        self, params: TrackCacheStorageForOriginParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.trackCacheStorageForOrigin",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def track_cache_storage_for_storage_key(
        self, params: TrackCacheStorageForStorageKeyParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.trackCacheStorageForStorageKey",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def track_indexed_d_b_for_origin(
        self, params: TrackIndexedDBForOriginParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.trackIndexedDBForOrigin",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def track_indexed_d_b_for_storage_key(
        self, params: TrackIndexedDBForStorageKeyParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.trackIndexedDBForStorageKey",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def untrack_cache_storage_for_origin(
        self, params: UntrackCacheStorageForOriginParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.untrackCacheStorageForOrigin",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def untrack_cache_storage_for_storage_key(
        self, params: UntrackCacheStorageForStorageKeyParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.untrackCacheStorageForStorageKey",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def untrack_indexed_d_b_for_origin(
        self, params: UntrackIndexedDBForOriginParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.untrackIndexedDBForOrigin",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def untrack_indexed_d_b_for_storage_key(
        self, params: UntrackIndexedDBForStorageKeyParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.untrackIndexedDBForStorageKey",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_trust_tokens(
        self, session_id: str | None = None
    ) -> GetTrustTokensResult:
        result = await self._client.send_raw(
            method="Storage.getTrustTokens",
            params=None,
            session_id=session_id,
        )
        return GetTrustTokensResult.model_validate(result)

    async def clear_trust_tokens(
        self, params: ClearTrustTokensParams, session_id: str | None = None
    ) -> ClearTrustTokensResult:
        result = await self._client.send_raw(
            method="Storage.clearTrustTokens",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return ClearTrustTokensResult.model_validate(result)

    async def get_interest_group_details(
        self, params: GetInterestGroupDetailsParams, session_id: str | None = None
    ) -> GetInterestGroupDetailsResult:
        result = await self._client.send_raw(
            method="Storage.getInterestGroupDetails",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetInterestGroupDetailsResult.model_validate(result)

    async def set_interest_group_tracking(
        self, params: SetInterestGroupTrackingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.setInterestGroupTracking",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_interest_group_auction_tracking(
        self, params: SetInterestGroupAuctionTrackingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.setInterestGroupAuctionTracking",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_shared_storage_metadata(
        self, params: GetSharedStorageMetadataParams, session_id: str | None = None
    ) -> GetSharedStorageMetadataResult:
        result = await self._client.send_raw(
            method="Storage.getSharedStorageMetadata",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetSharedStorageMetadataResult.model_validate(result)

    async def get_shared_storage_entries(
        self, params: GetSharedStorageEntriesParams, session_id: str | None = None
    ) -> GetSharedStorageEntriesResult:
        result = await self._client.send_raw(
            method="Storage.getSharedStorageEntries",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetSharedStorageEntriesResult.model_validate(result)

    async def set_shared_storage_entry(
        self, params: SetSharedStorageEntryParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.setSharedStorageEntry",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def delete_shared_storage_entry(
        self, params: DeleteSharedStorageEntryParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.deleteSharedStorageEntry",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def clear_shared_storage_entries(
        self, params: ClearSharedStorageEntriesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.clearSharedStorageEntries",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def reset_shared_storage_budget(
        self, params: ResetSharedStorageBudgetParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.resetSharedStorageBudget",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_shared_storage_tracking(
        self, params: SetSharedStorageTrackingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.setSharedStorageTracking",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_storage_bucket_tracking(
        self, params: SetStorageBucketTrackingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.setStorageBucketTracking",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def delete_storage_bucket(
        self, params: DeleteStorageBucketParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.deleteStorageBucket",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def run_bounce_tracking_mitigations(
        self, session_id: str | None = None
    ) -> RunBounceTrackingMitigationsResult:
        result = await self._client.send_raw(
            method="Storage.runBounceTrackingMitigations",
            params=None,
            session_id=session_id,
        )
        return RunBounceTrackingMitigationsResult.model_validate(result)

    async def set_attribution_reporting_local_testing_mode(
        self, params: SetAttributionReportingLocalTestingModeParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.setAttributionReportingLocalTestingMode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_attribution_reporting_tracking(
        self, params: SetAttributionReportingTrackingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.setAttributionReportingTracking",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def send_pending_attribution_reports(
        self, session_id: str | None = None
    ) -> SendPendingAttributionReportsResult:
        result = await self._client.send_raw(
            method="Storage.sendPendingAttributionReports",
            params=None,
            session_id=session_id,
        )
        return SendPendingAttributionReportsResult.model_validate(result)

    async def get_related_website_sets(
        self, session_id: str | None = None
    ) -> GetRelatedWebsiteSetsResult:
        result = await self._client.send_raw(
            method="Storage.getRelatedWebsiteSets",
            params=None,
            session_id=session_id,
        )
        return GetRelatedWebsiteSetsResult.model_validate(result)

    async def get_affected_urls_for_third_party_cookie_metadata(
        self, params: GetAffectedUrlsForThirdPartyCookieMetadataParams, session_id: str | None = None
    ) -> GetAffectedUrlsForThirdPartyCookieMetadataResult:
        result = await self._client.send_raw(
            method="Storage.getAffectedUrlsForThirdPartyCookieMetadata",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetAffectedUrlsForThirdPartyCookieMetadataResult.model_validate(result)

    async def set_protected_audience_k_anonymity(
        self, params: SetProtectedAudienceKAnonymityParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Storage.setProtectedAudienceKAnonymity",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
