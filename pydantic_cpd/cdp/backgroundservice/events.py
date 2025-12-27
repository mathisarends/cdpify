"""Generated event models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class RecordingStateChangedEvent(CDPModel):
    """
    Called when the recording state for the service has been updated.
    """
    is_recording: bool
    service: ServiceName

class BackgroundServiceEventReceivedEvent(CDPModel):
    """
    Called with all existing backgroundServiceEvents when enabled, and all new events
    afterwards if enabled and recording.
    """
    background_service_event: BackgroundServiceEvent
