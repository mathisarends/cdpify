"""Generated client library from CDP specification"""
# Domain: WebAuthn Client

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
    """This domain allows configuring virtual authenticators to test the WebAuthn
    API."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def enable(
        self, params: EnableParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enable the WebAuthn domain and start intercepting credential storage and
        retrieval with a virtual authenticator."""
        result = await self._client.send_raw(
            method="WebAuthn.enable",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disable the WebAuthn domain."""
        result = await self._client.send_raw(
            method="WebAuthn.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def add_virtual_authenticator(
        self, params: AddVirtualAuthenticatorParams, session_id: str | None = None
    ) -> AddVirtualAuthenticatorResult:
        """Creates and adds a virtual authenticator."""
        result = await self._client.send_raw(
            method="WebAuthn.addVirtualAuthenticator",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return AddVirtualAuthenticatorResult.model_validate(result)

    async def set_response_override_bits(
        self, params: SetResponseOverrideBitsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Resets parameters isBogusSignature, isBadUV, isBadUP to false if they are not present."""
        result = await self._client.send_raw(
            method="WebAuthn.setResponseOverrideBits",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def remove_virtual_authenticator(
        self, params: RemoveVirtualAuthenticatorParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Removes the given authenticator."""
        result = await self._client.send_raw(
            method="WebAuthn.removeVirtualAuthenticator",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def add_credential(
        self, params: AddCredentialParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Adds the credential to the specified authenticator."""
        result = await self._client.send_raw(
            method="WebAuthn.addCredential",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_credential(
        self, params: GetCredentialParams, session_id: str | None = None
    ) -> GetCredentialResult:
        """Returns a single credential stored in the given virtual authenticator that
        matches the credential ID."""
        result = await self._client.send_raw(
            method="WebAuthn.getCredential",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetCredentialResult.model_validate(result)

    async def get_credentials(
        self, params: GetCredentialsParams, session_id: str | None = None
    ) -> GetCredentialsResult:
        """Returns all the credentials stored in the given virtual authenticator."""
        result = await self._client.send_raw(
            method="WebAuthn.getCredentials",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetCredentialsResult.model_validate(result)

    async def remove_credential(
        self, params: RemoveCredentialParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Removes a credential from the authenticator."""
        result = await self._client.send_raw(
            method="WebAuthn.removeCredential",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def clear_credentials(
        self, params: ClearCredentialsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Clears all the credentials from the specified device."""
        result = await self._client.send_raw(
            method="WebAuthn.clearCredentials",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_user_verified(
        self, params: SetUserVerifiedParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Sets whether User Verification succeeds or fails for an authenticator.
        The default is true."""
        result = await self._client.send_raw(
            method="WebAuthn.setUserVerified",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_automatic_presence_simulation(
        self,
        params: SetAutomaticPresenceSimulationParams,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Sets whether tests of user presence will succeed immediately (if true) or fail to resolve (if false) for an authenticator.
        The default is true."""
        result = await self._client.send_raw(
            method="WebAuthn.setAutomaticPresenceSimulation",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_credential_properties(
        self, params: SetCredentialPropertiesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Allows setting credential properties.
        https://w3c.github.io/webauthn/#sctn-automation-set-credential-properties"""
        result = await self._client.send_raw(
            method="WebAuthn.setCredentialProperties",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
