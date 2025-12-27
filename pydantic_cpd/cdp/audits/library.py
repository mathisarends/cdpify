"""Generated client library from CDP specification"""
# Domain: Audits Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    CheckContrastParams,
    CheckFormsIssuesResult,
    GetEncodedResponseParams,
    GetEncodedResponseResult,
)


class AuditsClient:
    """Audits domain allows investigation of page violations and possible improvements."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def get_encoded_response(
        self, params: GetEncodedResponseParams, session_id: str | None = None
    ) -> GetEncodedResponseResult:
        """Returns the response body and size if it were re-encoded with the specified settings. Only
        applies to images."""
        result = await self._client.send_raw(
            method="Audits.getEncodedResponse",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetEncodedResponseResult.model_validate(result)

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables issues domain, prevents further issues from being reported to the client."""
        result = await self._client.send_raw(
            method="Audits.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        """Enables issues domain, sends the issues collected so far to the client by means of the
        `issueAdded` event."""
        result = await self._client.send_raw(
            method="Audits.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def check_contrast(
        self, params: CheckContrastParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Runs the contrast check for the target page. Found issues are reported
        using Audits.issueAdded event."""
        result = await self._client.send_raw(
            method="Audits.checkContrast",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def check_forms_issues(
        self, session_id: str | None = None
    ) -> CheckFormsIssuesResult:
        """Runs the form issues check for the target page. Found issues are reported
        using Audits.issueAdded event."""
        result = await self._client.send_raw(
            method="Audits.checkFormsIssues",
            params=None,
            session_id=session_id,
        )
        return CheckFormsIssuesResult.model_validate(result)
