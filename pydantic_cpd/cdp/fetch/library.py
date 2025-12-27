"""Generated client library from CDP specification"""

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
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Fetch.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, params: EnableParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Fetch.enable",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def fail_request(
        self, params: FailRequestParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Fetch.failRequest",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def fulfill_request(
        self, params: FulfillRequestParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Fetch.fulfillRequest",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def continue_request(
        self, params: ContinueRequestParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Fetch.continueRequest",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def continue_with_auth(
        self, params: ContinueWithAuthParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Fetch.continueWithAuth",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def continue_response(
        self, params: ContinueResponseParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Fetch.continueResponse",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_response_body(
        self, params: GetResponseBodyParams, session_id: str | None = None
    ) -> GetResponseBodyResult:
        result = await self._client.send_raw(
            method="Fetch.getResponseBody",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetResponseBodyResult.model_validate(result)

    async def take_response_body_as_stream(
        self, params: TakeResponseBodyAsStreamParams, session_id: str | None = None
    ) -> TakeResponseBodyAsStreamResult:
        result = await self._client.send_raw(
            method="Fetch.takeResponseBodyAsStream",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return TakeResponseBodyAsStreamResult.model_validate(result)
