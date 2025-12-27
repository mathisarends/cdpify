"""Generated event models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class VirtualTimeBudgetExpiredEvent(CDPModel):
    """
    Notification sent after the virtual time budget for the current VirtualTimePolicy
    has run out.
    """
    pass
