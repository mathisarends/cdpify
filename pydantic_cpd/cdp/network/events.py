"""Generated event models from CDP specification"""
# Domain: Network Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *

from pydantic_cpd.cdp import page


class DatareceivedEvent(CDPModel):
    """Fired when data chunk was received over the network."""

    request_id: RequestId
    timestamp: MonotonicTime
    data_length: int
    encoded_data_length: int
    data: str | None = None


class EventsourcemessagereceivedEvent(CDPModel):
    """Fired when EventSource message is received."""

    request_id: RequestId
    timestamp: MonotonicTime
    event_name: str
    event_id: str
    data: str


class LoadingfailedEvent(CDPModel):
    """Fired when HTTP request has failed to load."""

    request_id: RequestId
    timestamp: MonotonicTime
    type: ResourceType
    error_text: str
    canceled: bool | None = None
    blocked_reason: BlockedReason | None = None
    cors_error_status: CorsErrorStatus | None = None


class LoadingfinishedEvent(CDPModel):
    """Fired when HTTP request has finished loading."""

    request_id: RequestId
    timestamp: MonotonicTime
    encoded_data_length: float


class RequestinterceptedEvent(CDPModel):
    """Details of an intercepted HTTP request, which must be either allowed, blocked, modified or
    mocked.
    Deprecated, use Fetch.requestPaused instead."""

    interception_id: InterceptionId
    request: Request
    frame_id: page.FrameId
    resource_type: ResourceType
    is_navigation_request: bool
    is_download: bool | None = None
    redirect_url: str | None = None
    auth_challenge: AuthChallenge | None = None
    response_error_reason: ErrorReason | None = None
    response_status_code: int | None = None
    response_headers: Headers | None = None
    request_id: RequestId | None = None


class RequestservedfromcacheEvent(CDPModel):
    """Fired if request ended up loading from cache."""

    request_id: RequestId


class RequestwillbesentEvent(CDPModel):
    """Fired when page is about to send HTTP request."""

    request_id: RequestId
    loader_id: LoaderId
    document_u_r_l: str
    request: Request
    timestamp: MonotonicTime
    wall_time: TimeSinceEpoch
    initiator: Initiator
    redirect_has_extra_info: bool
    redirect_response: Response | None = None
    type: ResourceType | None = None
    frame_id: page.FrameId | None = None
    has_user_gesture: bool | None = None
    render_blocking_behavior: RenderBlockingBehavior | None = None


class ResourcechangedpriorityEvent(CDPModel):
    """Fired when resource loading priority is changed"""

    request_id: RequestId
    new_priority: ResourcePriority
    timestamp: MonotonicTime


class SignedexchangereceivedEvent(CDPModel):
    """Fired when a signed exchange was received over the network"""

    request_id: RequestId
    info: SignedExchangeInfo


class ResponsereceivedEvent(CDPModel):
    """Fired when HTTP response is available."""

    request_id: RequestId
    loader_id: LoaderId
    timestamp: MonotonicTime
    type: ResourceType
    response: Response
    has_extra_info: bool
    frame_id: page.FrameId | None = None


class WebsocketclosedEvent(CDPModel):
    """Fired when WebSocket is closed."""

    request_id: RequestId
    timestamp: MonotonicTime


class WebsocketcreatedEvent(CDPModel):
    """Fired upon WebSocket creation."""

    request_id: RequestId
    url: str
    initiator: Initiator | None = None


class WebsocketframeerrorEvent(CDPModel):
    """Fired when WebSocket message error occurs."""

    request_id: RequestId
    timestamp: MonotonicTime
    error_message: str


class WebsocketframereceivedEvent(CDPModel):
    """Fired when WebSocket message is received."""

    request_id: RequestId
    timestamp: MonotonicTime
    response: WebSocketFrame


class WebsocketframesentEvent(CDPModel):
    """Fired when WebSocket message is sent."""

    request_id: RequestId
    timestamp: MonotonicTime
    response: WebSocketFrame


class WebsockethandshakeresponsereceivedEvent(CDPModel):
    """Fired when WebSocket handshake response becomes available."""

    request_id: RequestId
    timestamp: MonotonicTime
    response: WebSocketResponse


class WebsocketwillsendhandshakerequestEvent(CDPModel):
    """Fired when WebSocket is about to initiate handshake."""

    request_id: RequestId
    timestamp: MonotonicTime
    wall_time: TimeSinceEpoch
    request: WebSocketRequest


class WebtransportcreatedEvent(CDPModel):
    """Fired upon WebTransport creation."""

    transport_id: RequestId
    url: str
    timestamp: MonotonicTime
    initiator: Initiator | None = None


class WebtransportconnectionestablishedEvent(CDPModel):
    """Fired when WebTransport handshake is finished."""

    transport_id: RequestId
    timestamp: MonotonicTime


class WebtransportclosedEvent(CDPModel):
    """Fired when WebTransport is disposed."""

    transport_id: RequestId
    timestamp: MonotonicTime


class DirecttcpsocketcreatedEvent(CDPModel):
    """Fired upon direct_socket.TCPSocket creation."""

    identifier: RequestId
    remote_addr: str
    remote_port: int
    options: DirectTCPSocketOptions
    timestamp: MonotonicTime
    initiator: Initiator | None = None


class DirecttcpsocketopenedEvent(CDPModel):
    """Fired when direct_socket.TCPSocket connection is opened."""

    identifier: RequestId
    remote_addr: str
    remote_port: int
    timestamp: MonotonicTime
    local_addr: str | None = None
    local_port: int | None = None


class DirecttcpsocketabortedEvent(CDPModel):
    """Fired when direct_socket.TCPSocket is aborted."""

    identifier: RequestId
    error_message: str
    timestamp: MonotonicTime


class DirecttcpsocketclosedEvent(CDPModel):
    """Fired when direct_socket.TCPSocket is closed."""

    identifier: RequestId
    timestamp: MonotonicTime


class DirecttcpsocketchunksentEvent(CDPModel):
    """Fired when data is sent to tcp direct socket stream."""

    identifier: RequestId
    data: str
    timestamp: MonotonicTime


class DirecttcpsocketchunkreceivedEvent(CDPModel):
    """Fired when data is received from tcp direct socket stream."""

    identifier: RequestId
    data: str
    timestamp: MonotonicTime


class DirectudpsocketjoinedmulticastgroupEvent(CDPModel):
    identifier: RequestId
    i_p_address: str


class DirectudpsocketleftmulticastgroupEvent(CDPModel):
    identifier: RequestId
    i_p_address: str


class DirectudpsocketcreatedEvent(CDPModel):
    """Fired upon direct_socket.UDPSocket creation."""

    identifier: RequestId
    options: DirectUDPSocketOptions
    timestamp: MonotonicTime
    initiator: Initiator | None = None


class DirectudpsocketopenedEvent(CDPModel):
    """Fired when direct_socket.UDPSocket connection is opened."""

    identifier: RequestId
    local_addr: str
    local_port: int
    timestamp: MonotonicTime
    remote_addr: str | None = None
    remote_port: int | None = None


class DirectudpsocketabortedEvent(CDPModel):
    """Fired when direct_socket.UDPSocket is aborted."""

    identifier: RequestId
    error_message: str
    timestamp: MonotonicTime


class DirectudpsocketclosedEvent(CDPModel):
    """Fired when direct_socket.UDPSocket is closed."""

    identifier: RequestId
    timestamp: MonotonicTime


class DirectudpsocketchunksentEvent(CDPModel):
    """Fired when message is sent to udp direct socket stream."""

    identifier: RequestId
    message: DirectUDPMessage
    timestamp: MonotonicTime


class DirectudpsocketchunkreceivedEvent(CDPModel):
    """Fired when message is received from udp direct socket stream."""

    identifier: RequestId
    message: DirectUDPMessage
    timestamp: MonotonicTime


class RequestwillbesentextrainfoEvent(CDPModel):
    """Fired when additional information about a requestWillBeSent event is available from the
    network stack. Not every requestWillBeSent event will have an additional
    requestWillBeSentExtraInfo fired for it, and there is no guarantee whether requestWillBeSent
    or requestWillBeSentExtraInfo will be fired first for the same request."""

    request_id: RequestId
    associated_cookies: list[AssociatedCookie]
    headers: Headers
    connect_timing: ConnectTiming
    client_security_state: ClientSecurityState | None = None
    site_has_cookie_in_other_partition: bool | None = None
    applied_network_conditions_id: str | None = None


class ResponsereceivedextrainfoEvent(CDPModel):
    """Fired when additional information about a responseReceived event is available from the network
    stack. Not every responseReceived event will have an additional responseReceivedExtraInfo for
    it, and responseReceivedExtraInfo may be fired before or after responseReceived."""

    request_id: RequestId
    blocked_cookies: list[BlockedSetCookieWithReason]
    headers: Headers
    resource_i_p_address_space: IPAddressSpace
    status_code: int
    headers_text: str | None = None
    cookie_partition_key: CookiePartitionKey | None = None
    cookie_partition_key_opaque: bool | None = None
    exempted_cookies: list[ExemptedSetCookieWithReason] | None = None


class ResponsereceivedearlyhintsEvent(CDPModel):
    """Fired when 103 Early Hints headers is received in addition to the common response.
    Not every responseReceived event will have an responseReceivedEarlyHints fired.
    Only one responseReceivedEarlyHints may be fired for eached responseReceived event."""

    request_id: RequestId
    headers: Headers


class TrusttokenoperationdoneEvent(CDPModel):
    """Fired exactly once for each Trust Token operation. Depending on
    the type of the operation and whether the operation succeeded or
    failed, the event is fired before the corresponding request was sent
    or after the response was received."""

    status: Literal[
        "Ok",
        "InvalidArgument",
        "MissingIssuerKeys",
        "FailedPrecondition",
        "ResourceExhausted",
        "AlreadyExists",
        "ResourceLimited",
        "Unauthorized",
        "BadResponse",
        "InternalError",
        "UnknownError",
        "FulfilledLocally",
        "SiteIssuerLimit",
    ]
    type: TrustTokenOperationType
    request_id: RequestId
    top_level_origin: str | None = None
    issuer_origin: str | None = None
    issued_token_count: int | None = None


class PolicyupdatedEvent(CDPModel):
    """Fired once security policy has been updated."""

    pass


class ReportingapireportaddedEvent(CDPModel):
    """Is sent whenever a new report is added.
    And after 'enableReportingApi' for all existing reports."""

    report: ReportingApiReport


class ReportingapireportupdatedEvent(CDPModel):
    report: ReportingApiReport


class ReportingapiendpointschangedfororiginEvent(CDPModel):
    origin: str
    endpoints: list[ReportingApiEndpoint]
