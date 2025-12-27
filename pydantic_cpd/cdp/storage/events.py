"""Generated event models from CDP specification"""
# Domain: Storage Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *

from pydantic_cpd.cdp import network
from pydantic_cpd.cdp import page
from pydantic_cpd.cdp import target


class CachestoragecontentupdatedEvent(CDPModel):
    """A cache's contents have been modified."""

    origin: str
    storage_key: str
    bucket_id: str
    cache_name: str


class CachestoragelistupdatedEvent(CDPModel):
    """A cache has been added/deleted."""

    origin: str
    storage_key: str
    bucket_id: str


class IndexeddbcontentupdatedEvent(CDPModel):
    """The origin's IndexedDB object store has been modified."""

    origin: str
    storage_key: str
    bucket_id: str
    database_name: str
    object_store_name: str


class IndexeddblistupdatedEvent(CDPModel):
    """The origin's IndexedDB database list has been modified."""

    origin: str
    storage_key: str
    bucket_id: str


class InterestgroupaccessedEvent(CDPModel):
    """One of the interest groups was accessed. Note that these events are global
    to all targets sharing an interest group store."""

    access_time: network.TimeSinceEpoch
    type: InterestGroupAccessType
    owner_origin: str
    name: str
    component_seller_origin: str | None = None
    bid: float | None = None
    bid_currency: str | None = None
    unique_auction_id: InterestGroupAuctionId | None = None


class InterestgroupauctioneventoccurredEvent(CDPModel):
    """An auction involving interest groups is taking place. These events are
    target-specific."""

    event_time: network.TimeSinceEpoch
    type: InterestGroupAuctionEventType
    unique_auction_id: InterestGroupAuctionId
    parent_auction_id: InterestGroupAuctionId | None = None
    auction_config: dict[str, Any] | None = None


class InterestgroupauctionnetworkrequestcreatedEvent(CDPModel):
    """Specifies which auctions a particular network fetch may be related to, and
    in what role. Note that it is not ordered with respect to
    Network.requestWillBeSent (but will happen before loadingFinished
    loadingFailed)."""

    type: InterestGroupAuctionFetchType
    request_id: network.RequestId
    auctions: list[InterestGroupAuctionId]


class SharedstorageaccessedEvent(CDPModel):
    """Shared storage was accessed by the associated page.
    The following parameters are included in all events."""

    access_time: network.TimeSinceEpoch
    scope: SharedStorageAccessScope
    method: SharedStorageAccessMethod
    main_frame_id: page.FrameId
    owner_origin: str
    owner_site: str
    params: SharedStorageAccessParams


class SharedstorageworkletoperationexecutionfinishedEvent(CDPModel):
    """A shared storage run or selectURL operation finished its execution.
    The following parameters are included in all events."""

    finished_time: network.TimeSinceEpoch
    execution_time: int
    method: SharedStorageAccessMethod
    operation_id: str
    worklet_target_id: target.TargetID
    main_frame_id: page.FrameId
    owner_origin: str


class StoragebucketcreatedorupdatedEvent(CDPModel):
    bucket_info: StorageBucketInfo


class StoragebucketdeletedEvent(CDPModel):
    bucket_id: str


class AttributionreportingsourceregisteredEvent(CDPModel):
    registration: AttributionReportingSourceRegistration
    result: AttributionReportingSourceRegistrationResult


class AttributionreportingtriggerregisteredEvent(CDPModel):
    registration: AttributionReportingTriggerRegistration
    event_level: AttributionReportingEventLevelResult
    aggregatable: AttributionReportingAggregatableResult


class AttributionreportingreportsentEvent(CDPModel):
    url: str
    body: dict[str, Any]
    result: AttributionReportingReportResult
    net_error: int | None = None
    net_error_name: str | None = None
    http_status_code: int | None = None


class AttributionreportingverbosedebugreportsentEvent(CDPModel):
    url: str
    body: list[dict[str, Any]] | None = None
    net_error: int | None = None
    net_error_name: str | None = None
    http_status_code: int | None = None
