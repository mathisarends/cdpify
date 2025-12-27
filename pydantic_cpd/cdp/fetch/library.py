"""Generated client library from CDP specification"""
# Domain: Fetch Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    ContinueRequestParams,
    ContinueResponseParams,
    ContinueWithAuthParams,
    EnableParams,
    FailRequestParams,
    FulfillRequestParams,
    GetResponseBodyParams,
    GetResponseBodyResult,
    TakeResponseBodyAsStreamParams,
    TakeResponseBodyAsStreamResult,
)


class FetchClient:
    """A domain for letting clients substitute browser's network layer with client code."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables the fetch domain."""
        result = await self._client.send_raw(
            method="Fetch.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, params: EnableParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enables issuing of requestPaused events. A request will be paused until client
        calls one of failRequest, fulfillRequest or continueRequest/continueWithAuth."""
        result = await self._client.send_raw(
            method="Fetch.enable",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def fail_request(
        self, params: FailRequestParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Causes the request to fail with specified reason."""
        result = await self._client.send_raw(
            method="Fetch.failRequest",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def fulfill_request(
        self, params: FulfillRequestParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Provides response to the request."""
        result = await self._client.send_raw(
            method="Fetch.fulfillRequest",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def continue_request(
        self, params: ContinueRequestParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Continues the request, optionally modifying some of its parameters."""
        result = await self._client.send_raw(
            method="Fetch.continueRequest",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def continue_with_auth(
        self, params: ContinueWithAuthParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Continues a request supplying authChallengeResponse following authRequired event."""
        result = await self._client.send_raw(
            method="Fetch.continueWithAuth",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def continue_response(
        self, params: ContinueResponseParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Continues loading of the paused response, optionally modifying the
        response headers. If either responseCode or headers are modified, all of them
        must be present."""
        result = await self._client.send_raw(
            method="Fetch.continueResponse",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_response_body(
        self, params: GetResponseBodyParams, session_id: str | None = None
    ) -> GetResponseBodyResult:
        """Causes the body of the response to be received from the server and
        returned as a single string. May only be issued for a request that
        is paused in the Response stage and is mutually exclusive with
        takeResponseBodyForInterceptionAsStream. Calling other methods that
        affect the request or disabling fetch domain before body is received
        results in an undefined behavior.
        Note that the response body is not available for redirects. Requests
        paused in the _redirect received_ state may be differentiated by
        `responseCode` and presence of `location` response header, see
        comments to `requestPaused` for details."""
        result = await self._client.send_raw(
            method="Fetch.getResponseBody",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetResponseBodyResult.model_validate(result)

    async def take_response_body_as_stream(
        self, params: TakeResponseBodyAsStreamParams, session_id: str | None = None
    ) -> TakeResponseBodyAsStreamResult:
        """Returns a handle to the stream representing the response body.
        The request must be paused in the HeadersReceived stage.
        Note that after this command the request can't be continued
        as is -- client either needs to cancel it or to provide the
        response body.
        The stream only supports sequential read, IO.read will fail if the position
        is specified.
        This method is mutually exclusive with getResponseBody.
        Calling other methods that affect the request or disabling fetch
        domain before body is received results in an undefined behavior."""
        result = await self._client.send_raw(
            method="Fetch.takeResponseBodyAsStream",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return TakeResponseBodyAsStreamResult.model_validate(result)
