"""Generated event models from CDP specification"""
# Domain: Log Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class EntryaddedEvent(CDPModel):
    """Issued when new message was logged."""

    entry: LogEntry
