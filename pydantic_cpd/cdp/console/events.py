"""Generated event models from CDP specification"""
# Domain: Console Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class MessageaddedEvent(CDPModel):
    """Issued when new console message is added."""

    message: ConsoleMessage
