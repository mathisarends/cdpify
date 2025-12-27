"""Generated event models from CDP specification"""
# Domain: Target Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class AttachedtotargetEvent(CDPModel):
    """Issued when attached to target because of auto-attach or `attachToTarget` command."""

    session_id: SessionID
    target_info: TargetInfo
    waiting_for_debugger: bool


class DetachedfromtargetEvent(CDPModel):
    """Issued when detached from target for any reason (including `detachFromTarget` command). Can be
    issued multiple times per target if multiple sessions have been attached to it."""

    session_id: SessionID
    target_id: TargetID | None = None


class ReceivedmessagefromtargetEvent(CDPModel):
    """Notifies about a new protocol message received from the session (as reported in
    `attachedToTarget` event)."""

    session_id: SessionID
    message: str
    target_id: TargetID | None = None


class TargetcreatedEvent(CDPModel):
    """Issued when a possible inspection target is created."""

    target_info: TargetInfo


class TargetdestroyedEvent(CDPModel):
    """Issued when a target is destroyed."""

    target_id: TargetID


class TargetcrashedEvent(CDPModel):
    """Issued when a target has crashed."""

    target_id: TargetID
    status: str
    error_code: int


class TargetinfochangedEvent(CDPModel):
    """Issued when some information about a target has changed. This only happens between
    `targetCreated` and `targetDestroyed`."""

    target_info: TargetInfo
