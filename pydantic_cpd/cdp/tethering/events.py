"""Generated event models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class AcceptedEvent(CDPModel):
    """
    Informs that port was successfully bound and got a specified connection id.
    """
    port: int
    connection_id: str
