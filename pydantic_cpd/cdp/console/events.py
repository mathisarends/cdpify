"""Generated event models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class MessageAddedEvent(CDPModel):
    """
    Issued when new console message is added.
    """
    message: ConsoleMessage
