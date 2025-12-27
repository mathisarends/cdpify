"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    AddCredentialParams,
    AddVirtualAuthenticatorParams,
    AddVirtualAuthenticatorResult,
    ClearCredentialsParams,
    EnableParams,
    GetCredentialParams,
    GetCredentialResult,
    GetCredentialsParams,
    GetCredentialsResult,
    RemoveCredentialParams,
    RemoveVirtualAuthenticatorParams,
    SetAutomaticPresenceSimulationParams,
    SetCredentialPropertiesParams,
    SetResponseOverrideBitsParams,
    SetUserVerifiedParams,
)

class WebAuthnClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def enable(
        self, params: EnableParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="WebAuthn.enable",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="WebAuthn.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def add_virtual_authenticator(
        self, params: AddVirtualAuthenticatorParams, session_id: str | None = None
    ) -> AddVirtualAuthenticatorResult:
        result = await self._client.send_raw(
            method="WebAuthn.addVirtualAuthenticator",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return AddVirtualAuthenticatorResult.model_validate(result)

    async def set_response_override_bits(
        self, params: SetResponseOverrideBitsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="WebAuthn.setResponseOverrideBits",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def remove_virtual_authenticator(
        self, params: RemoveVirtualAuthenticatorParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="WebAuthn.removeVirtualAuthenticator",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def add_credential(
        self, params: AddCredentialParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="WebAuthn.addCredential",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_credential(
        self, params: GetCredentialParams, session_id: str | None = None
    ) -> GetCredentialResult:
        result = await self._client.send_raw(
            method="WebAuthn.getCredential",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetCredentialResult.model_validate(result)

    async def get_credentials(
        self, params: GetCredentialsParams, session_id: str | None = None
    ) -> GetCredentialsResult:
        result = await self._client.send_raw(
            method="WebAuthn.getCredentials",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetCredentialsResult.model_validate(result)

    async def remove_credential(
        self, params: RemoveCredentialParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="WebAuthn.removeCredential",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def clear_credentials(
        self, params: ClearCredentialsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="WebAuthn.clearCredentials",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_user_verified(
        self, params: SetUserVerifiedParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="WebAuthn.setUserVerified",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_automatic_presence_simulation(
        self, params: SetAutomaticPresenceSimulationParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="WebAuthn.setAutomaticPresenceSimulation",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_credential_properties(
        self, params: SetCredentialPropertiesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="WebAuthn.setCredentialProperties",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
