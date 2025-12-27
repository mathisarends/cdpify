"""Generated client library from CDP specification"""
# Domain: Security Client

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    HandleCertificateErrorParams,
    SetIgnoreCertificateErrorsParams,
    SetOverrideCertificateErrorsParams,
)


class SecurityClient:
    """CDP Security domain client."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables tracking security state changes."""
        result = await self._client.send_raw(
            method="Security.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(self, session_id: str | None = None) -> dict[str, Any]:
        """Enables tracking security state changes."""
        result = await self._client.send_raw(
            method="Security.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def set_ignore_certificate_errors(
        self, params: SetIgnoreCertificateErrorsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enable/disable whether all certificate errors should be ignored."""
        result = await self._client.send_raw(
            method="Security.setIgnoreCertificateErrors",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def handle_certificate_error(
        self, params: HandleCertificateErrorParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Handles a certificate error that fired a certificateError event."""
        result = await self._client.send_raw(
            method="Security.handleCertificateError",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_override_certificate_errors(
        self, params: SetOverrideCertificateErrorsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enable/disable overriding certificate errors. If enabled, all certificate error events need to
        be handled by the DevTools client and should be answered with `handleCertificateError` commands."""
        result = await self._client.send_raw(
            method="Security.setOverrideCertificateErrors",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
