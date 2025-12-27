"""Generated event models from CDP specification"""
# Domain: Overlay Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *

from pydantic_cpd.cdp import dom
from pydantic_cpd.cdp import page


class InspectnoderequestedEvent(CDPModel):
    """Fired when the node should be inspected. This happens after call to `setInspectMode` or when
    user manually inspects an element."""

    backend_node_id: dom.BackendNodeId


class NodehighlightrequestedEvent(CDPModel):
    """Fired when the node should be highlighted. This happens after call to `setInspectMode`."""

    node_id: dom.NodeId


class ScreenshotrequestedEvent(CDPModel):
    """Fired when user asks to capture screenshot of some area on the page."""

    viewport: page.Viewport


class InspectmodecanceledEvent(CDPModel):
    """Fired when user cancels the inspect mode."""

    pass
