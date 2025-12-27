"""Generated event models from CDP specification"""
# Domain: DOM Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *

from pydantic_cpd.cdp import dom


class AttributemodifiedEvent(CDPModel):
    """Fired when `Element`'s attribute is modified."""

    node_id: NodeId
    name: str
    value: str


class AdoptedstylesheetsmodifiedEvent(CDPModel):
    """Fired when `Element`'s adoptedStyleSheets are modified."""

    node_id: NodeId
    adopted_style_sheets: list[StyleSheetId]


class AttributeremovedEvent(CDPModel):
    """Fired when `Element`'s attribute is removed."""

    node_id: NodeId
    name: str


class CharacterdatamodifiedEvent(CDPModel):
    """Mirrors `DOMCharacterDataModified` event."""

    node_id: NodeId
    character_data: str


class ChildnodecountupdatedEvent(CDPModel):
    """Fired when `Container`'s child node count has changed."""

    node_id: NodeId
    child_node_count: int


class ChildnodeinsertedEvent(CDPModel):
    """Mirrors `DOMNodeInserted` event."""

    parent_node_id: NodeId
    previous_node_id: NodeId
    node: Node


class ChildnoderemovedEvent(CDPModel):
    """Mirrors `DOMNodeRemoved` event."""

    parent_node_id: NodeId
    node_id: NodeId


class DistributednodesupdatedEvent(CDPModel):
    """Called when distribution is changed."""

    insertion_point_id: NodeId
    distributed_nodes: list[BackendNode]


class DocumentupdatedEvent(CDPModel):
    """Fired when `Document` has been totally updated. Node ids are no longer valid."""

    pass


class InlinestyleinvalidatedEvent(CDPModel):
    """Fired when `Element`'s inline style is modified via a CSS property modification."""

    node_ids: list[NodeId]


class PseudoelementaddedEvent(CDPModel):
    """Called when a pseudo element is added to an element."""

    parent_id: NodeId
    pseudo_element: Node


class ToplayerelementsupdatedEvent(CDPModel):
    """Called when top layer elements are changed."""

    pass


class ScrollableflagupdatedEvent(CDPModel):
    """Fired when a node's scrollability state changes."""

    node_id: dom.NodeId
    is_scrollable: bool


class AffectedbystartingstylesflagupdatedEvent(CDPModel):
    """Fired when a node's starting styles changes."""

    node_id: dom.NodeId
    affected_by_starting_styles: bool


class PseudoelementremovedEvent(CDPModel):
    """Called when a pseudo element is removed from an element."""

    parent_id: NodeId
    pseudo_element_id: NodeId


class SetchildnodesEvent(CDPModel):
    """Fired when backend wants to provide client with the missing DOM structure. This happens upon
    most of the calls requesting node ids."""

    parent_id: NodeId
    nodes: list[Node]


class ShadowrootpoppedEvent(CDPModel):
    """Called when shadow root is popped from the element."""

    host_id: NodeId
    root_id: NodeId


class ShadowrootpushedEvent(CDPModel):
    """Called when shadow root is pushed into the element."""

    host_id: NodeId
    root: Node
