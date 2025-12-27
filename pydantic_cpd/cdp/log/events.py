"""Generated event models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class EntryAddedEvent(CDPModel):
    """
    Issued when new message was logged.
    """
    entry: LogEntry
