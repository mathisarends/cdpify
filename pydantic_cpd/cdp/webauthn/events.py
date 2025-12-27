"""Generated event models from CDP specification"""
# Domain: WebAuthn Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class CredentialaddedEvent(CDPModel):
    """Triggered when a credential is added to an authenticator."""

    authenticator_id: AuthenticatorId
    credential: Credential


class CredentialdeletedEvent(CDPModel):
    """Triggered when a credential is deleted, e.g. through
    PublicKeyCredential.signalUnknownCredential()."""

    authenticator_id: AuthenticatorId
    credential_id: str


class CredentialupdatedEvent(CDPModel):
    """Triggered when a credential is updated, e.g. through
    PublicKeyCredential.signalCurrentUserDetails()."""

    authenticator_id: AuthenticatorId
    credential: Credential


class CredentialassertedEvent(CDPModel):
    """Triggered when a credential is used in a webauthn assertion."""

    authenticator_id: AuthenticatorId
    credential: Credential
