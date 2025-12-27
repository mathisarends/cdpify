"""Generated event models from CDP specification"""
# Domain: BackgroundService Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class RecordingstatechangedEvent(CDPModel):
    """Called when the recording state for the service has been updated."""

    is_recording: bool
    service: ServiceName


class BackgroundserviceeventreceivedEvent(CDPModel):
    """Called with all existing backgroundServiceEvents when enabled, and all new
    events afterwards if enabled and recording."""

    background_service_event: BackgroundServiceEvent
