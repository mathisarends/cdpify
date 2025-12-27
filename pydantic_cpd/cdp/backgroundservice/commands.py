"""Generated command models from CDP specification"""
# Domain: BackgroundService Commands

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class StartObservingParams(CDPModel):
    """Enables event updates for the service."""

    service: ServiceName


class StopObservingParams(CDPModel):
    """Disables event updates for the service."""

    service: ServiceName


class SetRecordingParams(CDPModel):
    """Set the recording state for the service."""

    should_record: bool
    service: ServiceName


class ClearEventsParams(CDPModel):
    """Clears all stored data for the service."""

    service: ServiceName
