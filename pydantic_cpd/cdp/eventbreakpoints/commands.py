"""Generated command models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class SetInstrumentationBreakpointParams(CDPModel):
    """
    Sets breakpoint on particular native event.
    """
    event_name: str

class RemoveInstrumentationBreakpointParams(CDPModel):
    """
    Removes breakpoint on particular native event.
    """
    event_name: str
