"""Generated from CDP specification"""
# Domain: WebAuthn
# This domain allows configuring virtual authenticators to test the WebAuthn API.

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

AuthenticatorId = str

AuthenticatorProtocol = Literal["u2f", "ctap2"]

Ctap2Version = Literal["ctap2_0", "ctap2_1"]

AuthenticatorTransport = Literal["usb", "nfc", "ble", "cable", "internal"]


class VirtualAuthenticatorOptions(CDPModel):
    protocol: AuthenticatorProtocol
    ctap2_version: Ctap2Version | None = None
    transport: AuthenticatorTransport
    has_resident_key: bool | None = None
    has_user_verification: bool | None = None
    has_large_blob: bool | None = None
    has_cred_blob: bool | None = None
    has_min_pin_length: bool | None = None
    has_prf: bool | None = None
    automatic_presence_simulation: bool | None = None
    is_user_verified: bool | None = None
    default_backup_eligibility: bool | None = None
    default_backup_state: bool | None = None


class Credential(CDPModel):
    credential_id: str
    is_resident_credential: bool
    rp_id: str | None = None
    private_key: str
    user_handle: str | None = None
    sign_count: int
    large_blob: str | None = None
    backup_eligibility: bool | None = None
    backup_state: bool | None = None
    user_name: str | None = None
    user_display_name: str | None = None
