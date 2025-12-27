"""Generated event models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class LoadCompleteEvent(CDPModel):
    """
    The loadComplete event mirrors the load complete event sent by the browser to
    assistive technology when the web page has finished loading.
    """
    root: AXNode

class NodesUpdatedEvent(CDPModel):
    """
    The nodesUpdated event is sent every time a previously requested node has changed
    the in tree.
    """
    nodes: list[AXNode]
