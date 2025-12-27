"""Generated from CDP specification"""
# Domain: Fetch
# A domain for letting clients substitute browser's network layer with client code.

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

# Unique request identifier. Note that this does not identify individual HTTP requests
# that are part of a network request.
RequestId = str

# Stages of the request to handle. Request will intercept before the request is sent.
# Response will intercept after the response is received (but before response body is
# received).
RequestStage = Literal["Request", "Response"]


class RequestPattern(CDPModel):
    url_pattern: str | None = None
    resource_type: network.ResourceType | None = None
    request_stage: RequestStage | None = None


class HeaderEntry(CDPModel):
    """Response HTTP header entry"""

    name: str
    value: str


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
