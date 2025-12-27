"""Generated event models from CDP specification"""
# Domain: Security Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class CertificateerrorEvent(CDPModel):
    """There is a certificate error. If overriding certificate errors is enabled, then it should be
    handled with the `handleCertificateError` command. Note: this event does not fire if the
    certificate error has been allowed internally. Only one client per target should override
    certificate errors at the same time."""

    event_id: int
    error_type: str
    request_u_r_l: str


class VisiblesecuritystatechangedEvent(CDPModel):
    """The security state of the page changed."""

    visible_security_state: VisibleSecurityState


class SecuritystatechangedEvent(CDPModel):
    """The security state of the page changed. No longer being sent."""

    security_state: SecurityState
    scheme_is_cryptographic: bool
    explanations: list[SecurityStateExplanation]
    insecure_content_status: InsecureContentStatus
    summary: str | None = None
