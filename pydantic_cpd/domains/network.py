"""Generated from CDP specification"""

from pydantic_cpd.domains.base import CDPModel
from typing import Literal, Any

from pydantic_cpd.domains import debugger
from pydantic_cpd.domains import emulation
from pydantic_cpd.domains import io
from pydantic_cpd.domains import network
from pydantic_cpd.domains import page
from pydantic_cpd.domains import runtime
from pydantic_cpd.domains import security

# Alias for cross-domain type references
Debugger = debugger
Emulation = emulation
IO = io
Network = network
Page = page
Runtime = runtime
Security = security


ResourceType = Literal[
    "Document",
    "Stylesheet",
    "Image",
    "Media",
    "Font",
    "Script",
    "TextTrack",
    "XHR",
    "Fetch",
    "Prefetch",
    "EventSource",
    "WebSocket",
    "Manifest",
    "SignedExchange",
    "Ping",
    "CSPViolationReport",
    "Preflight",
    "FedCM",
    "Other",
]
LoaderId = str
RequestId = str
InterceptionId = str
ErrorReason = Literal[
    "Failed",
    "Aborted",
    "TimedOut",
    "AccessDenied",
    "ConnectionClosed",
    "ConnectionReset",
    "ConnectionRefused",
    "ConnectionAborted",
    "ConnectionFailed",
    "NameNotResolved",
    "InternetDisconnected",
    "AddressUnreachable",
    "BlockedByClient",
    "BlockedByResponse",
]
TimeSinceEpoch = float
MonotonicTime = float
Headers = dict[str, Any]
ConnectionType = Literal[
    "none",
    "cellular2g",
    "cellular3g",
    "cellular4g",
    "bluetooth",
    "ethernet",
    "wifi",
    "wimax",
    "other",
]
CookieSameSite = Literal["Strict", "Lax", "None"]
CookiePriority = Literal["Low", "Medium", "High"]
CookieSourceScheme = Literal["Unset", "NonSecure", "Secure"]


class ResourceTiming(CDPModel):
    """Timing information for the request."""

    request_time: float
    proxy_start: float
    proxy_end: float
    dns_start: float
    dns_end: float
    connect_start: float
    connect_end: float
    ssl_start: float
    ssl_end: float
    worker_start: float
    worker_ready: float
    worker_fetch_start: float
    worker_respond_with_settled: float
    worker_router_evaluation_start: float | None = None
    worker_cache_lookup_start: float | None = None
    send_start: float
    send_end: float
    push_start: float
    push_end: float
    receive_headers_start: float
    receive_headers_end: float


ResourcePriority = Literal["VeryLow", "Low", "Medium", "High", "VeryHigh"]
RenderBlockingBehavior = Literal[
    "Blocking",
    "InBodyParserBlocking",
    "NonBlocking",
    "NonBlockingDynamic",
    "PotentiallyBlocking",
]


class PostDataEntry(CDPModel):
    """Post data entry for HTTP request"""

    bytes: str | None = None


class Request(CDPModel):
    """HTTP request data."""

    url: str
    url_fragment: str | None = None
    method: str
    headers: Headers
    post_data: str | None = None
    has_post_data: bool | None = None
    post_data_entries: list[PostDataEntry] | None = None
    mixed_content_type: Security.MixedContentType | None = None
    initial_priority: ResourcePriority
    referrer_policy: Literal[
        "unsafe-url",
        "no-referrer-when-downgrade",
        "no-referrer",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
    ]
    is_link_preload: bool | None = None
    trust_token_params: TrustTokenParams | None = None
    is_same_site: bool | None = None
    is_ad_related: bool | None = None


class SignedCertificateTimestamp(CDPModel):
    """Details of a signed certificate timestamp (SCT)."""

    status: str
    origin: str
    log_description: str
    log_id: str
    timestamp: float
    hash_algorithm: str
    signature_algorithm: str
    signature_data: str


class SecurityDetails(CDPModel):
    """Security details about a request."""

    protocol: str
    key_exchange: str
    key_exchange_group: str | None = None
    cipher: str
    mac: str | None = None
    certificate_id: Security.CertificateId
    subject_name: str
    san_list: list[str]
    issuer: str
    valid_from: TimeSinceEpoch
    valid_to: TimeSinceEpoch
    signed_certificate_timestamp_list: list[SignedCertificateTimestamp]
    certificate_transparency_compliance: CertificateTransparencyCompliance
    server_signature_algorithm: int | None = None
    encrypted_client_hello: bool


CertificateTransparencyCompliance = Literal["unknown", "not-compliant", "compliant"]
BlockedReason = Literal[
    "other",
    "csp",
    "mixed-content",
    "origin",
    "inspector",
    "integrity",
    "subresource-filter",
    "content-type",
    "coep-frame-resource-needs-coep-header",
    "coop-sandboxed-iframe-cannot-navigate-to-coop-page",
    "corp-not-same-origin",
    "corp-not-same-origin-after-defaulted-to-same-origin-by-coep",
    "corp-not-same-origin-after-defaulted-to-same-origin-by-dip",
    "corp-not-same-origin-after-defaulted-to-same-origin-by-coep-and-dip",
    "corp-not-same-site",
    "sri-message-signature-mismatch",
]
CorsError = Literal[
    "DisallowedByMode",
    "InvalidResponse",
    "WildcardOriginNotAllowed",
    "MissingAllowOriginHeader",
    "MultipleAllowOriginValues",
    "InvalidAllowOriginValue",
    "AllowOriginMismatch",
    "InvalidAllowCredentials",
    "CorsDisabledScheme",
    "PreflightInvalidStatus",
    "PreflightDisallowedRedirect",
    "PreflightWildcardOriginNotAllowed",
    "PreflightMissingAllowOriginHeader",
    "PreflightMultipleAllowOriginValues",
    "PreflightInvalidAllowOriginValue",
    "PreflightAllowOriginMismatch",
    "PreflightInvalidAllowCredentials",
    "PreflightMissingAllowExternal",
    "PreflightInvalidAllowExternal",
    "PreflightMissingAllowPrivateNetwork",
    "PreflightInvalidAllowPrivateNetwork",
    "InvalidAllowMethodsPreflightResponse",
    "InvalidAllowHeadersPreflightResponse",
    "MethodDisallowedByPreflightResponse",
    "HeaderDisallowedByPreflightResponse",
    "RedirectContainsCredentials",
    "InsecurePrivateNetwork",
    "InvalidPrivateNetworkAccess",
    "UnexpectedPrivateNetworkAccess",
    "NoCorsRedirectModeNotFollow",
    "PreflightMissingPrivateNetworkAccessId",
    "PreflightMissingPrivateNetworkAccessName",
    "PrivateNetworkAccessPermissionUnavailable",
    "PrivateNetworkAccessPermissionDenied",
    "LocalNetworkAccessPermissionDenied",
]


class CorsErrorStatus(CDPModel):
    cors_error: CorsError
    failed_parameter: str


ServiceWorkerResponseSource = Literal[
    "cache-storage", "http-cache", "fallback-code", "network"
]


class TrustTokenParams(CDPModel):
    """
    Determines what type of Trust Token operation is executed and depending on the type,
    some additional parameters. The values are specified in
    third_party/blink/renderer/core/fetch/trust_token.idl.
    """

    operation: TrustTokenOperationType
    refresh_policy: Literal["UseCached", "Refresh"]
    issuers: list[str] | None = None


TrustTokenOperationType = Literal["Issuance", "Redemption", "Signing"]
AlternateProtocolUsage = Literal[
    "alternativeJobWonWithoutRace",
    "alternativeJobWonRace",
    "mainJobWonRace",
    "mappingMissing",
    "broken",
    "dnsAlpnH3JobWonWithoutRace",
    "dnsAlpnH3JobWonRace",
    "unspecifiedReason",
]
ServiceWorkerRouterSource = Literal[
    "network",
    "cache",
    "fetch-event",
    "race-network-and-fetch-handler",
    "race-network-and-cache",
]


class ServiceWorkerRouterInfo(CDPModel):
    rule_id_matched: int | None = None
    matched_source_type: ServiceWorkerRouterSource | None = None
    actual_source_type: ServiceWorkerRouterSource | None = None


class Response(CDPModel):
    """HTTP response data."""

    url: str
    status: int
    status_text: str
    headers: Headers
    headers_text: str | None = None
    mime_type: str
    charset: str
    request_headers: Headers | None = None
    request_headers_text: str | None = None
    connection_reused: bool
    connection_id: float
    remote_i_p_address: str | None = None
    remote_port: int | None = None
    from_disk_cache: bool | None = None
    from_service_worker: bool | None = None
    from_prefetch_cache: bool | None = None
    from_early_hints: bool | None = None
    service_worker_router_info: ServiceWorkerRouterInfo | None = None
    encoded_data_length: float
    timing: ResourceTiming | None = None
    service_worker_response_source: ServiceWorkerResponseSource | None = None
    response_time: TimeSinceEpoch | None = None
    cache_storage_cache_name: str | None = None
    protocol: str | None = None
    alternate_protocol_usage: AlternateProtocolUsage | None = None
    security_state: Security.SecurityState
    security_details: SecurityDetails | None = None


class WebSocketRequest(CDPModel):
    """WebSocket request data."""

    headers: Headers


class WebSocketResponse(CDPModel):
    """WebSocket response data."""

    status: int
    status_text: str
    headers: Headers
    headers_text: str | None = None
    request_headers: Headers | None = None
    request_headers_text: str | None = None


class WebSocketFrame(CDPModel):
    """
    WebSocket message data. This represents an entire WebSocket message, not just a
    fragmented frame as the name suggests.
    """

    opcode: float
    mask: bool
    payload_data: str


class CachedResource(CDPModel):
    """Information about the cached resource."""

    url: str
    type: ResourceType
    response: Response | None = None
    body_size: float


class Initiator(CDPModel):
    """Information about the request initiator."""

    type: Literal[
        "parser", "script", "preload", "SignedExchange", "preflight", "FedCM", "other"
    ]
    stack: Runtime.StackTrace | None = None
    url: str | None = None
    line_number: float | None = None
    column_number: float | None = None
    request_id: RequestId | None = None


class CookiePartitionKey(CDPModel):
    """
    cookiePartitionKey object The representation of the components of the key that are
    created by the cookiePartitionKey class contained in
    net/cookies/cookie_partition_key.h.
    """

    top_level_site: str
    has_cross_site_ancestor: bool


class Cookie(CDPModel):
    """Cookie object"""

    name: str
    value: str
    domain: str
    path: str
    expires: float
    size: int
    http_only: bool
    secure: bool
    session: bool
    same_site: CookieSameSite | None = None
    priority: CookiePriority
    same_party: bool
    source_scheme: CookieSourceScheme
    source_port: int
    partition_key: CookiePartitionKey | None = None
    partition_key_opaque: bool | None = None


SetCookieBlockedReason = Literal[
    "SecureOnly",
    "SameSiteStrict",
    "SameSiteLax",
    "SameSiteUnspecifiedTreatedAsLax",
    "SameSiteNoneInsecure",
    "UserPreferences",
    "ThirdPartyPhaseout",
    "ThirdPartyBlockedInFirstPartySet",
    "SyntaxError",
    "SchemeNotSupported",
    "OverwriteSecure",
    "InvalidDomain",
    "InvalidPrefix",
    "UnknownError",
    "SchemefulSameSiteStrict",
    "SchemefulSameSiteLax",
    "SchemefulSameSiteUnspecifiedTreatedAsLax",
    "SamePartyFromCrossPartyContext",
    "SamePartyConflictsWithOtherAttributes",
    "NameValuePairExceedsMaxSize",
    "DisallowedCharacter",
    "NoCookieContent",
]
CookieBlockedReason = Literal[
    "SecureOnly",
    "NotOnPath",
    "DomainMismatch",
    "SameSiteStrict",
    "SameSiteLax",
    "SameSiteUnspecifiedTreatedAsLax",
    "SameSiteNoneInsecure",
    "UserPreferences",
    "ThirdPartyPhaseout",
    "ThirdPartyBlockedInFirstPartySet",
    "UnknownError",
    "SchemefulSameSiteStrict",
    "SchemefulSameSiteLax",
    "SchemefulSameSiteUnspecifiedTreatedAsLax",
    "SamePartyFromCrossPartyContext",
    "NameValuePairExceedsMaxSize",
    "PortMismatch",
    "SchemeMismatch",
    "AnonymousContext",
]
CookieExemptionReason = Literal[
    "None",
    "UserSetting",
    "TPCDMetadata",
    "TPCDDeprecationTrial",
    "TopLevelTPCDDeprecationTrial",
    "TPCDHeuristics",
    "EnterprisePolicy",
    "StorageAccess",
    "TopLevelStorageAccess",
    "Scheme",
    "SameSiteNoneCookiesInSandbox",
]


class BlockedSetCookieWithReason(CDPModel):
    """A cookie which was not stored from a response with the corresponding reason."""

    blocked_reasons: list[SetCookieBlockedReason]
    cookie_line: str
    cookie: Cookie | None = None


class ExemptedSetCookieWithReason(CDPModel):
    """
    A cookie should have been blocked by 3PCD but is exempted and stored from a response
    with the corresponding reason. A cookie could only have at most one exemption
    reason.
    """

    exemption_reason: CookieExemptionReason
    cookie_line: str
    cookie: Cookie


class AssociatedCookie(CDPModel):
    """
    A cookie associated with the request which may or may not be sent with it. Includes
    the cookies itself and reasons for blocking or exemption.
    """

    cookie: Cookie
    blocked_reasons: list[CookieBlockedReason]
    exemption_reason: CookieExemptionReason | None = None


class CookieParam(CDPModel):
    """Cookie parameter object"""

    name: str
    value: str
    url: str | None = None
    domain: str | None = None
    path: str | None = None
    secure: bool | None = None
    http_only: bool | None = None
    same_site: CookieSameSite | None = None
    expires: TimeSinceEpoch | None = None
    priority: CookiePriority | None = None
    same_party: bool | None = None
    source_scheme: CookieSourceScheme | None = None
    source_port: int | None = None
    partition_key: CookiePartitionKey | None = None


class AuthChallenge(CDPModel):
    """Authorization challenge for HTTP status code 401 or 407."""

    source: Literal["Server", "Proxy"] | None = None
    origin: str
    scheme: str
    realm: str


class AuthChallengeResponse(CDPModel):
    """Response to an AuthChallenge."""

    response: Literal["Default", "CancelAuth", "ProvideCredentials"]
    username: str | None = None
    password: str | None = None


InterceptionStage = Literal["Request", "HeadersReceived"]


class RequestPattern(CDPModel):
    """Request pattern for interception."""

    url_pattern: str | None = None
    resource_type: ResourceType | None = None
    interception_stage: InterceptionStage | None = None


class SignedExchangeSignature(CDPModel):
    """
    Information about a signed exchange signature.
    https://wicg.github.io/webpackage/draft-yasskin-httpbis-origin-signed-exchanges-
    impl.html#rfc.section.3.1
    """

    label: str
    signature: str
    integrity: str
    cert_url: str | None = None
    cert_sha256: str | None = None
    validity_url: str
    date: int
    expires: int
    certificates: list[str] | None = None


class SignedExchangeHeader(CDPModel):
    """
    Information about a signed exchange header. https://wicg.github.io/webpackage/draft-
    yasskin-httpbis-origin-signed-exchanges-impl.html#cbor-representation
    """

    request_url: str
    response_code: int
    response_headers: Headers
    signatures: list[SignedExchangeSignature]
    header_integrity: str


SignedExchangeErrorField = Literal[
    "signatureSig",
    "signatureIntegrity",
    "signatureCertUrl",
    "signatureCertSha256",
    "signatureValidityUrl",
    "signatureTimestamps",
]


class SignedExchangeError(CDPModel):
    """Information about a signed exchange response."""

    message: str
    signature_index: int | None = None
    error_field: SignedExchangeErrorField | None = None


class SignedExchangeInfo(CDPModel):
    """Information about a signed exchange response."""

    outer_response: Response
    has_extra_info: bool
    header: SignedExchangeHeader | None = None
    security_details: SecurityDetails | None = None
    errors: list[SignedExchangeError] | None = None


ContentEncoding = Literal["deflate", "gzip", "br", "zstd"]


class NetworkConditions(CDPModel):
    url_pattern: str
    latency: float
    download_throughput: float
    upload_throughput: float
    connection_type: ConnectionType | None = None
    packet_loss: float | None = None
    packet_queue_length: int | None = None
    packet_reordering: bool | None = None


class BlockPattern(CDPModel):
    url_pattern: str
    block: bool


DirectSocketDnsQueryType = Literal["ipv4", "ipv6"]


class DirectTCPSocketOptions(CDPModel):
    no_delay: bool
    keep_alive_delay: float | None = None
    send_buffer_size: float | None = None
    receive_buffer_size: float | None = None
    dns_query_type: DirectSocketDnsQueryType | None = None


class DirectUDPSocketOptions(CDPModel):
    remote_addr: str | None = None
    remote_port: int | None = None
    local_addr: str | None = None
    local_port: int | None = None
    dns_query_type: DirectSocketDnsQueryType | None = None
    send_buffer_size: float | None = None
    receive_buffer_size: float | None = None
    multicast_loopback: bool | None = None
    multicast_time_to_live: int | None = None
    multicast_allow_address_sharing: bool | None = None


class DirectUDPMessage(CDPModel):
    data: str
    remote_addr: str | None = None
    remote_port: int | None = None


PrivateNetworkRequestPolicy = Literal[
    "Allow",
    "BlockFromInsecureToMorePrivate",
    "WarnFromInsecureToMorePrivate",
    "PermissionBlock",
    "PermissionWarn",
]
IPAddressSpace = Literal["Loopback", "Local", "Public", "Unknown"]


class ConnectTiming(CDPModel):
    request_time: float


class ClientSecurityState(CDPModel):
    initiator_is_secure_context: bool
    initiator_i_p_address_space: IPAddressSpace
    private_network_request_policy: PrivateNetworkRequestPolicy


CrossOriginOpenerPolicyValue = Literal[
    "SameOrigin",
    "SameOriginAllowPopups",
    "RestrictProperties",
    "UnsafeNone",
    "SameOriginPlusCoep",
    "RestrictPropertiesPlusCoep",
    "NoopenerAllowPopups",
]


class CrossOriginOpenerPolicyStatus(CDPModel):
    value: CrossOriginOpenerPolicyValue
    report_only_value: CrossOriginOpenerPolicyValue
    reporting_endpoint: str | None = None
    report_only_reporting_endpoint: str | None = None


CrossOriginEmbedderPolicyValue = Literal["None", "Credentialless", "RequireCorp"]


class CrossOriginEmbedderPolicyStatus(CDPModel):
    value: CrossOriginEmbedderPolicyValue
    report_only_value: CrossOriginEmbedderPolicyValue
    reporting_endpoint: str | None = None
    report_only_reporting_endpoint: str | None = None


ContentSecurityPolicySource = Literal["HTTP", "Meta"]


class ContentSecurityPolicyStatus(CDPModel):
    effective_directives: str
    is_enforced: bool
    source: ContentSecurityPolicySource


class SecurityIsolationStatus(CDPModel):
    coop: CrossOriginOpenerPolicyStatus | None = None
    coep: CrossOriginEmbedderPolicyStatus | None = None
    csp: list[ContentSecurityPolicyStatus] | None = None


ReportStatus = Literal["Queued", "Pending", "MarkedForRemoval", "Success"]
ReportId = str


class ReportingApiReport(CDPModel):
    """An object representing a report generated by the Reporting API."""

    id: ReportId
    initiator_url: str
    destination: str
    type: str
    timestamp: Network.TimeSinceEpoch
    depth: int
    completed_attempts: int
    body: dict[str, Any]
    status: ReportStatus


class ReportingApiEndpoint(CDPModel):
    url: str
    group_name: str


class LoadNetworkResourcePageResult(CDPModel):
    """An object providing the result of a network resource load."""

    success: bool
    net_error: float | None = None
    net_error_name: str | None = None
    http_status_code: float | None = None
    stream: IO.StreamHandle | None = None
    headers: Network.Headers | None = None


class LoadNetworkResourceOptions(CDPModel):
    """
    An options object that may be extended later to better support CORS, CORB and
    streaming.
    """

    disable_cache: bool
    include_credentials: bool


class SetacceptedencodingsParams(CDPModel):
    """
    Sets a list of content encodings that will be accepted. Empty list means no encoding
    is accepted.
    """

    encodings: list[ContentEncoding]


class CanclearbrowsercacheResult(CDPModel):
    result: bool


class CanclearbrowsercookiesResult(CDPModel):
    result: bool


class CanemulatenetworkconditionsResult(CDPModel):
    result: bool


class ContinueinterceptedrequestParams(CDPModel):
    """
    Response to Network.requestIntercepted which either modifies the request to continue
    with any modifications, or blocks it, or completes it with the provided response
    bytes. If a network fetch occurs as a result which encounters a redirect an
    additional Network.requestIntercepted event will be sent with the same
    InterceptionId. Deprecated, use Fetch.continueRequest, Fetch.fulfillRequest and
    Fetch.failRequest instead.
    """

    interception_id: InterceptionId
    error_reason: ErrorReason | None = None
    raw_response: str | None = None
    url: str | None = None
    method: str | None = None
    post_data: str | None = None
    headers: Headers | None = None
    auth_challenge_response: AuthChallengeResponse | None = None


class DeletecookiesParams(CDPModel):
    """
    Deletes browser cookies with matching name and url or domain/path/partitionKey pair.
    """

    name: str
    url: str | None = None
    domain: str | None = None
    path: str | None = None
    partition_key: CookiePartitionKey | None = None


class EmulatenetworkconditionsParams(CDPModel):
    """
    Activates emulation of network conditions. This command is deprecated in favor of
    the emulateNetworkConditionsByRule and overrideNetworkState commands, which can be
    used together to the same effect.
    """

    offline: bool
    latency: float
    download_throughput: float
    upload_throughput: float
    connection_type: ConnectionType | None = None
    packet_loss: float | None = None
    packet_queue_length: int | None = None
    packet_reordering: bool | None = None


class EmulatenetworkconditionsbyruleParams(CDPModel):
    """
    Activates emulation of network conditions for individual requests using URL match
    patterns. Unlike the deprecated Network.emulateNetworkConditions this method does
    not affect `navigator` state. Use Network.overrideNetworkState to explicitly modify
    `navigator` behavior.
    """

    offline: bool
    matched_network_conditions: list[NetworkConditions]


class EmulatenetworkconditionsbyruleResult(CDPModel):
    rule_ids: list[str]


class OverridenetworkstateParams(CDPModel):
    """Override the state of navigator.onLine and navigator.connection."""

    offline: bool
    latency: float
    download_throughput: float
    upload_throughput: float
    connection_type: ConnectionType | None = None


class EnableParams(CDPModel):
    """Enables network tracking, network events will now be delivered to the client."""

    max_total_buffer_size: int | None = None
    max_resource_buffer_size: int | None = None
    max_post_data_size: int | None = None
    report_direct_socket_traffic: bool | None = None
    enable_durable_messages: bool | None = None


class ConfiguredurablemessagesParams(CDPModel):
    """
    Configures storing response bodies outside of renderer, so that these survive a
    cross-process navigation. If maxTotalBufferSize is not set, durable messages are
    disabled.
    """

    max_total_buffer_size: int | None = None
    max_resource_buffer_size: int | None = None


class GetallcookiesResult(CDPModel):
    cookies: list[Cookie]


class GetcertificateParams(CDPModel):
    """Returns the DER-encoded certificate."""

    origin: str


class GetcertificateResult(CDPModel):
    table_names: list[str]


class GetcookiesParams(CDPModel):
    """
    Returns all browser cookies for the current URL. Depending on the backend support,
    will return detailed cookie information in the `cookies` field.
    """

    urls: list[str] | None = None


class GetcookiesResult(CDPModel):
    cookies: list[Cookie]


class GetresponsebodyParams(CDPModel):
    """Returns content served for the given request."""

    request_id: RequestId


class GetresponsebodyResult(CDPModel):
    body: str
    base64_encoded: bool


class GetrequestpostdataParams(CDPModel):
    """
    Returns post data sent with the request. Returns an error when no data was sent with
    the request.
    """

    request_id: RequestId


class GetrequestpostdataResult(CDPModel):
    post_data: str


class GetresponsebodyforinterceptionParams(CDPModel):
    """Returns content served for the given currently intercepted request."""

    interception_id: InterceptionId


class GetresponsebodyforinterceptionResult(CDPModel):
    body: str
    base64_encoded: bool


class TakeresponsebodyforinterceptionasstreamParams(CDPModel):
    """
    Returns a handle to the stream representing the response body. Note that after this
    command, the intercepted request can't be continued as is -- you either need to
    cancel it or to provide the response body. The stream only supports sequential read,
    IO.read will fail if the position is specified.
    """

    interception_id: InterceptionId


class TakeresponsebodyforinterceptionasstreamResult(CDPModel):
    stream: IO.StreamHandle


class ReplayxhrParams(CDPModel):
    """
    This method sends a new XMLHttpRequest which is identical to the original one. The
    following parameters should be identical: method, url, async, request body, extra
    headers, withCredentials attribute, user, password.
    """

    request_id: RequestId


class SearchinresponsebodyParams(CDPModel):
    """Searches for given string in response content."""

    request_id: RequestId
    query: str
    case_sensitive: bool | None = None
    is_regex: bool | None = None


class SearchinresponsebodyResult(CDPModel):
    result: list[Debugger.SearchMatch]


class SetblockedurlsParams(CDPModel):
    """Blocks URLs from loading."""

    url_patterns: list[BlockPattern] | None = None
    urls: list[str] | None = None


class SetbypassserviceworkerParams(CDPModel):
    """Toggles ignoring of service worker for each request."""

    bypass: bool


class SetcachedisabledParams(CDPModel):
    """Toggles ignoring cache for each request. If `true`, cache will not be used."""

    cache_disabled: bool


class SetcookieParams(CDPModel):
    """
    Sets a cookie with the given cookie data; may overwrite equivalent cookies if they
    exist.
    """

    name: str
    value: str
    url: str | None = None
    domain: str | None = None
    path: str | None = None
    secure: bool | None = None
    http_only: bool | None = None
    same_site: CookieSameSite | None = None
    expires: TimeSinceEpoch | None = None
    priority: CookiePriority | None = None
    same_party: bool | None = None
    source_scheme: CookieSourceScheme | None = None
    source_port: int | None = None
    partition_key: CookiePartitionKey | None = None


class SetcookieResult(CDPModel):
    success: bool


class SetcookiesParams(CDPModel):
    """Sets given cookies."""

    cookies: list[CookieParam]


class SetextrahttpheadersParams(CDPModel):
    """
    Specifies whether to always send extra HTTP headers with the requests from this
    page.
    """

    headers: Headers


class SetattachdebugstackParams(CDPModel):
    """Specifies whether to attach a page script stack id in requests"""

    enabled: bool


class SetrequestinterceptionParams(CDPModel):
    """
    Sets the requests to intercept that match the provided patterns and optionally
    resource types. Deprecated, please use Fetch.enable instead.
    """

    patterns: list[RequestPattern]


class SetuseragentoverrideParams(CDPModel):
    """Allows overriding user agent with the given string."""

    user_agent: str
    accept_language: str | None = None
    platform: str | None = None
    user_agent_metadata: Emulation.UserAgentMetadata | None = None


class StreamresourcecontentParams(CDPModel):
    """
    Enables streaming of the response for the given requestId. If enabled, the
    dataReceived event contains the data that was received during streaming.
    """

    request_id: RequestId


class StreamresourcecontentResult(CDPModel):
    buffered_data: str


class GetsecurityisolationstatusParams(CDPModel):
    """Returns information about the COEP/COOP isolation status."""

    frame_id: Page.FrameId | None = None


class GetsecurityisolationstatusResult(CDPModel):
    status: SecurityIsolationStatus


class EnablereportingapiParams(CDPModel):
    """
    Enables tracking for the Reporting API, events generated by the Reporting API will
    now be delivered to the client. Enabling triggers 'reportingApiReportAdded' for all
    existing reports.
    """

    enable: bool


class LoadnetworkresourceParams(CDPModel):
    """Fetches the resource and returns the content."""

    frame_id: Page.FrameId | None = None
    url: str
    options: LoadNetworkResourceOptions


class LoadnetworkresourceResult(CDPModel):
    resource: LoadNetworkResourcePageResult


class SetcookiecontrolsParams(CDPModel):
    """
    Sets Controls for third-party cookie access Page reload is required before the new
    cookie behavior will be observed
    """

    enable_third_party_cookie_restriction: bool
    disable_third_party_cookie_metadata: bool
    disable_third_party_cookie_heuristics: bool


class NetworkClient:
    """
    Network domain allows tracking network activities of the page. It exposes
    information about http, file, data and other requests and responses, their headers,
    bodies, timing, etc.
    """

    def __init__(self, cdp_client: Any) -> None:
        self._cdp = cdp_client

    async def set_accepted_encodings(self, encodings: list[ContentEncoding]) -> None:
        """
        Sets a list of content encodings that will be accepted. Empty list means no
        encoding is accepted.
        """
        params = SetacceptedencodingsParams(
            encodings=encodings,
        )
        result = await self._cdp.call(
            "Network.setAcceptedEncodings",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def clear_accepted_encodings_override(self) -> None:
        """Clears accepted encodings set by setAcceptedEncodings"""
        result = await self._cdp.call("Network.clearAcceptedEncodingsOverride", {})
        return None

    async def can_clear_browser_cache(self) -> CanclearbrowsercacheResult:
        """Tells whether clearing browser cache is supported."""
        result = await self._cdp.call("Network.canClearBrowserCache", {})
        return CanclearbrowsercacheResult(**result)

    async def can_clear_browser_cookies(self) -> CanclearbrowsercookiesResult:
        """Tells whether clearing browser cookies is supported."""
        result = await self._cdp.call("Network.canClearBrowserCookies", {})
        return CanclearbrowsercookiesResult(**result)

    async def can_emulate_network_conditions(self) -> CanemulatenetworkconditionsResult:
        """Tells whether emulation of network conditions is supported."""
        result = await self._cdp.call("Network.canEmulateNetworkConditions", {})
        return CanemulatenetworkconditionsResult(**result)

    async def clear_browser_cache(self) -> None:
        """Clears browser cache."""
        result = await self._cdp.call("Network.clearBrowserCache", {})
        return None

    async def clear_browser_cookies(self) -> None:
        """Clears browser cookies."""
        result = await self._cdp.call("Network.clearBrowserCookies", {})
        return None

    async def continue_intercepted_request(
        self,
        interception_id: InterceptionId,
        error_reason: ErrorReason | None = None,
        raw_response: str | None = None,
        url: str | None = None,
        method: str | None = None,
        post_data: str | None = None,
        headers: Headers | None = None,
        auth_challenge_response: AuthChallengeResponse | None = None,
    ) -> None:
        """
        Response to Network.requestIntercepted which either modifies the request to
        continue with any modifications, or blocks it, or completes it with the provided
        response bytes. If a network fetch occurs as a result which encounters a
        redirect an additional Network.requestIntercepted event will be sent with the
        same InterceptionId. Deprecated, use Fetch.continueRequest, Fetch.fulfillRequest
        and Fetch.failRequest instead.
        """
        params = ContinueinterceptedrequestParams(
            interception_id=interception_id,
            error_reason=error_reason,
            raw_response=raw_response,
            url=url,
            method=method,
            post_data=post_data,
            headers=headers,
            auth_challenge_response=auth_challenge_response,
        )
        result = await self._cdp.call(
            "Network.continueInterceptedRequest",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def delete_cookies(
        self,
        name: str,
        url: str | None = None,
        domain: str | None = None,
        path: str | None = None,
        partition_key: CookiePartitionKey | None = None,
    ) -> None:
        """
        Deletes browser cookies with matching name and url or domain/path/partitionKey
        pair.
        """
        params = DeletecookiesParams(
            name=name,
            url=url,
            domain=domain,
            path=path,
            partition_key=partition_key,
        )
        result = await self._cdp.call(
            "Network.deleteCookies", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def disable(self) -> None:
        """
        Disables network tracking, prevents network events from being sent to the
        client.
        """
        result = await self._cdp.call("Network.disable", {})
        return None

    async def emulate_network_conditions(
        self,
        offline: bool,
        latency: float,
        download_throughput: float,
        upload_throughput: float,
        connection_type: ConnectionType | None = None,
        packet_loss: float | None = None,
        packet_queue_length: int | None = None,
        packet_reordering: bool | None = None,
    ) -> None:
        """
        Activates emulation of network conditions. This command is deprecated in favor
        of the emulateNetworkConditionsByRule and overrideNetworkState commands, which
        can be used together to the same effect.
        """
        params = EmulatenetworkconditionsParams(
            offline=offline,
            latency=latency,
            download_throughput=download_throughput,
            upload_throughput=upload_throughput,
            connection_type=connection_type,
            packet_loss=packet_loss,
            packet_queue_length=packet_queue_length,
            packet_reordering=packet_reordering,
        )
        result = await self._cdp.call(
            "Network.emulateNetworkConditions",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def emulate_network_conditions_by_rule(
        self, offline: bool, matched_network_conditions: list[NetworkConditions]
    ) -> EmulatenetworkconditionsbyruleResult:
        """
        Activates emulation of network conditions for individual requests using URL
        match patterns. Unlike the deprecated Network.emulateNetworkConditions this
        method does not affect `navigator` state. Use Network.overrideNetworkState to
        explicitly modify `navigator` behavior.
        """
        params = EmulatenetworkconditionsbyruleParams(
            offline=offline,
            matched_network_conditions=matched_network_conditions,
        )
        result = await self._cdp.call(
            "Network.emulateNetworkConditionsByRule",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return EmulatenetworkconditionsbyruleResult(**result)

    async def override_network_state(
        self,
        offline: bool,
        latency: float,
        download_throughput: float,
        upload_throughput: float,
        connection_type: ConnectionType | None = None,
    ) -> None:
        """Override the state of navigator.onLine and navigator.connection."""
        params = OverridenetworkstateParams(
            offline=offline,
            latency=latency,
            download_throughput=download_throughput,
            upload_throughput=upload_throughput,
            connection_type=connection_type,
        )
        result = await self._cdp.call(
            "Network.overrideNetworkState",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def enable(
        self,
        max_total_buffer_size: int | None = None,
        max_resource_buffer_size: int | None = None,
        max_post_data_size: int | None = None,
        report_direct_socket_traffic: bool | None = None,
        enable_durable_messages: bool | None = None,
    ) -> None:
        """
        Enables network tracking, network events will now be delivered to the client.
        """
        params = EnableParams(
            max_total_buffer_size=max_total_buffer_size,
            max_resource_buffer_size=max_resource_buffer_size,
            max_post_data_size=max_post_data_size,
            report_direct_socket_traffic=report_direct_socket_traffic,
            enable_durable_messages=enable_durable_messages,
        )
        result = await self._cdp.call(
            "Network.enable", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def configure_durable_messages(
        self,
        max_total_buffer_size: int | None = None,
        max_resource_buffer_size: int | None = None,
    ) -> None:
        """
        Configures storing response bodies outside of renderer, so that these survive a
        cross-process navigation. If maxTotalBufferSize is not set, durable messages are
        disabled.
        """
        params = ConfiguredurablemessagesParams(
            max_total_buffer_size=max_total_buffer_size,
            max_resource_buffer_size=max_resource_buffer_size,
        )
        result = await self._cdp.call(
            "Network.configureDurableMessages",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def get_all_cookies(self) -> GetallcookiesResult:
        """
        Returns all browser cookies. Depending on the backend support, will return
        detailed cookie information in the `cookies` field. Deprecated. Use
        Storage.getCookies instead.
        """
        result = await self._cdp.call("Network.getAllCookies", {})
        return GetallcookiesResult(**result)

    async def get_certificate(self, origin: str) -> GetcertificateResult:
        """Returns the DER-encoded certificate."""
        params = GetcertificateParams(
            origin=origin,
        )
        result = await self._cdp.call(
            "Network.getCertificate",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetcertificateResult(**result)

    async def get_cookies(self, urls: list[str] | None = None) -> GetcookiesResult:
        """
        Returns all browser cookies for the current URL. Depending on the backend
        support, will return detailed cookie information in the `cookies` field.
        """
        params = GetcookiesParams(
            urls=urls,
        )
        result = await self._cdp.call(
            "Network.getCookies", params.model_dump(by_alias=True, exclude_none=True)
        )
        return GetcookiesResult(**result)

    async def get_response_body(self, request_id: RequestId) -> GetresponsebodyResult:
        """Returns content served for the given request."""
        params = GetresponsebodyParams(
            request_id=request_id,
        )
        result = await self._cdp.call(
            "Network.getResponseBody",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetresponsebodyResult(**result)

    async def get_request_post_data(
        self, request_id: RequestId
    ) -> GetrequestpostdataResult:
        """
        Returns post data sent with the request. Returns an error when no data was sent
        with the request.
        """
        params = GetrequestpostdataParams(
            request_id=request_id,
        )
        result = await self._cdp.call(
            "Network.getRequestPostData",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetrequestpostdataResult(**result)

    async def get_response_body_for_interception(
        self, interception_id: InterceptionId
    ) -> GetresponsebodyforinterceptionResult:
        """Returns content served for the given currently intercepted request."""
        params = GetresponsebodyforinterceptionParams(
            interception_id=interception_id,
        )
        result = await self._cdp.call(
            "Network.getResponseBodyForInterception",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetresponsebodyforinterceptionResult(**result)

    async def take_response_body_for_interception_as_stream(
        self, interception_id: InterceptionId
    ) -> TakeresponsebodyforinterceptionasstreamResult:
        """
        Returns a handle to the stream representing the response body. Note that after
        this command, the intercepted request can't be continued as is -- you either
        need to cancel it or to provide the response body. The stream only supports
        sequential read, IO.read will fail if the position is specified.
        """
        params = TakeresponsebodyforinterceptionasstreamParams(
            interception_id=interception_id,
        )
        result = await self._cdp.call(
            "Network.takeResponseBodyForInterceptionAsStream",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return TakeresponsebodyforinterceptionasstreamResult(**result)

    async def replay_x_h_r(self, request_id: RequestId) -> None:
        """
        This method sends a new XMLHttpRequest which is identical to the original one.
        The following parameters should be identical: method, url, async, request body,
        extra headers, withCredentials attribute, user, password.
        """
        params = ReplayxhrParams(
            request_id=request_id,
        )
        result = await self._cdp.call(
            "Network.replayXHR", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def search_in_response_body(
        self,
        request_id: RequestId,
        query: str,
        case_sensitive: bool | None = None,
        is_regex: bool | None = None,
    ) -> SearchinresponsebodyResult:
        """Searches for given string in response content."""
        params = SearchinresponsebodyParams(
            request_id=request_id,
            query=query,
            case_sensitive=case_sensitive,
            is_regex=is_regex,
        )
        result = await self._cdp.call(
            "Network.searchInResponseBody",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return SearchinresponsebodyResult(**result)

    async def set_blocked_u_r_ls(
        self,
        url_patterns: list[BlockPattern] | None = None,
        urls: list[str] | None = None,
    ) -> None:
        """Blocks URLs from loading."""
        params = SetblockedurlsParams(
            url_patterns=url_patterns,
            urls=urls,
        )
        result = await self._cdp.call(
            "Network.setBlockedURLs",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_bypass_service_worker(self, bypass: bool) -> None:
        """Toggles ignoring of service worker for each request."""
        params = SetbypassserviceworkerParams(
            bypass=bypass,
        )
        result = await self._cdp.call(
            "Network.setBypassServiceWorker",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_cache_disabled(self, cache_disabled: bool) -> None:
        """
        Toggles ignoring cache for each request. If `true`, cache will not be used.
        """
        params = SetcachedisabledParams(
            cache_disabled=cache_disabled,
        )
        result = await self._cdp.call(
            "Network.setCacheDisabled",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_cookie(
        self,
        name: str,
        value: str,
        url: str | None = None,
        domain: str | None = None,
        path: str | None = None,
        secure: bool | None = None,
        http_only: bool | None = None,
        same_site: CookieSameSite | None = None,
        expires: TimeSinceEpoch | None = None,
        priority: CookiePriority | None = None,
        same_party: bool | None = None,
        source_scheme: CookieSourceScheme | None = None,
        source_port: int | None = None,
        partition_key: CookiePartitionKey | None = None,
    ) -> SetcookieResult:
        """
        Sets a cookie with the given cookie data; may overwrite equivalent cookies if
        they exist.
        """
        params = SetcookieParams(
            name=name,
            value=value,
            url=url,
            domain=domain,
            path=path,
            secure=secure,
            http_only=http_only,
            same_site=same_site,
            expires=expires,
            priority=priority,
            same_party=same_party,
            source_scheme=source_scheme,
            source_port=source_port,
            partition_key=partition_key,
        )
        result = await self._cdp.call(
            "Network.setCookie", params.model_dump(by_alias=True, exclude_none=True)
        )
        return SetcookieResult(**result)

    async def set_cookies(self, cookies: list[CookieParam]) -> None:
        """Sets given cookies."""
        params = SetcookiesParams(
            cookies=cookies,
        )
        result = await self._cdp.call(
            "Network.setCookies", params.model_dump(by_alias=True, exclude_none=True)
        )
        return None

    async def set_extra_h_t_t_p_headers(self, headers: Headers) -> None:
        """
        Specifies whether to always send extra HTTP headers with the requests from this
        page.
        """
        params = SetextrahttpheadersParams(
            headers=headers,
        )
        result = await self._cdp.call(
            "Network.setExtraHTTPHeaders",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_attach_debug_stack(self, enabled: bool) -> None:
        """Specifies whether to attach a page script stack id in requests"""
        params = SetattachdebugstackParams(
            enabled=enabled,
        )
        result = await self._cdp.call(
            "Network.setAttachDebugStack",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_request_interception(self, patterns: list[RequestPattern]) -> None:
        """
        Sets the requests to intercept that match the provided patterns and optionally
        resource types. Deprecated, please use Fetch.enable instead.
        """
        params = SetrequestinterceptionParams(
            patterns=patterns,
        )
        result = await self._cdp.call(
            "Network.setRequestInterception",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def set_user_agent_override(
        self,
        user_agent: str,
        accept_language: str | None = None,
        platform: str | None = None,
        user_agent_metadata: Emulation.UserAgentMetadata | None = None,
    ) -> None:
        """Allows overriding user agent with the given string."""
        params = SetuseragentoverrideParams(
            user_agent=user_agent,
            accept_language=accept_language,
            platform=platform,
            user_agent_metadata=user_agent_metadata,
        )
        result = await self._cdp.call(
            "Network.setUserAgentOverride",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def stream_resource_content(
        self, request_id: RequestId
    ) -> StreamresourcecontentResult:
        """
        Enables streaming of the response for the given requestId. If enabled, the
        dataReceived event contains the data that was received during streaming.
        """
        params = StreamresourcecontentParams(
            request_id=request_id,
        )
        result = await self._cdp.call(
            "Network.streamResourceContent",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return StreamresourcecontentResult(**result)

    async def get_security_isolation_status(
        self, frame_id: Page.FrameId | None = None
    ) -> GetsecurityisolationstatusResult:
        """Returns information about the COEP/COOP isolation status."""
        params = GetsecurityisolationstatusParams(
            frame_id=frame_id,
        )
        result = await self._cdp.call(
            "Network.getSecurityIsolationStatus",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return GetsecurityisolationstatusResult(**result)

    async def enable_reporting_api(self, enable: bool) -> None:
        """
        Enables tracking for the Reporting API, events generated by the Reporting API
        will now be delivered to the client. Enabling triggers 'reportingApiReportAdded'
        for all existing reports.
        """
        params = EnablereportingapiParams(
            enable=enable,
        )
        result = await self._cdp.call(
            "Network.enableReportingApi",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None

    async def load_network_resource(
        self,
        url: str,
        options: LoadNetworkResourceOptions,
        frame_id: Page.FrameId | None = None,
    ) -> LoadnetworkresourceResult:
        """Fetches the resource and returns the content."""
        params = LoadnetworkresourceParams(
            frame_id=frame_id,
            url=url,
            options=options,
        )
        result = await self._cdp.call(
            "Network.loadNetworkResource",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return LoadnetworkresourceResult(**result)

    async def set_cookie_controls(
        self,
        enable_third_party_cookie_restriction: bool,
        disable_third_party_cookie_metadata: bool,
        disable_third_party_cookie_heuristics: bool,
    ) -> None:
        """
        Sets Controls for third-party cookie access Page reload is required before the
        new cookie behavior will be observed
        """
        params = SetcookiecontrolsParams(
            enable_third_party_cookie_restriction=enable_third_party_cookie_restriction,
            disable_third_party_cookie_metadata=disable_third_party_cookie_metadata,
            disable_third_party_cookie_heuristics=disable_third_party_cookie_heuristics,
        )
        result = await self._cdp.call(
            "Network.setCookieControls",
            params.model_dump(by_alias=True, exclude_none=True),
        )
        return None
