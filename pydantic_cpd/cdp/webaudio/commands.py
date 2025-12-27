"""Generated command models from CDP specification"""
# Domain: WebAudio Commands

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class GetRealtimeDataParams(CDPModel):
    """Fetch the realtime data from the registered contexts."""

    context_id: GraphObjectId


class GetRealtimeDataResult(CDPModel):
    realtime_data: ContextRealtimeData
