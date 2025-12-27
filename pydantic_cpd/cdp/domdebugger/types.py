"""Generated from CDP specification"""
# Domain: DOMDebugger
# DOM debugging allows setting breakpoints on particular DOM operations and events.
# JavaScript execution will stop on these operations as if there was a regular
# breakpoint set.

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

# DOM breakpoint type.
DOMBreakpointType = Literal["subtree-modified", "attribute-modified", "node-removed"]

# CSP Violation type.
CSPViolationType = Literal["trustedtype-sink-violation", "trustedtype-policy-violation"]


class EventListener(CDPModel):
    """Object event listener."""

    type: str
    use_capture: bool
    passive: bool
    once: bool
    script_id: runtime.ScriptId
    line_number: int
    column_number: int
    handler: runtime.RemoteObject | None = None
    original_handler: runtime.RemoteObject | None = None
    backend_node_id: dom.BackendNodeId | None = None
