"""Generated event models from CDP specification"""
# Domain: Emulation Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class VirtualtimebudgetexpiredEvent(CDPModel):
    """Notification sent after the virtual time budget for the current VirtualTimePolicy has run out."""

    pass
