"""Generated command models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class GetRealtimeDataParams(CDPModel):
    """
    Fetch the realtime data from the registered contexts.
    """
    context_id: GraphObjectId

class GetRealtimeDataResult(CDPModel):
    realtime_data: ContextRealtimeData
