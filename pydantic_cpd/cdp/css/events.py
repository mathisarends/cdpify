"""Generated event models from CDP specification"""
# Domain: CSS Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *

from pydantic_cpd.cdp import dom


class FontsupdatedEvent(CDPModel):
    """Fires whenever a web font is updated.  A non-empty font parameter indicates a successfully loaded
    web font."""

    font: FontFace | None = None


class MediaqueryresultchangedEvent(CDPModel):
    """Fires whenever a MediaQuery result changes (for example, after a browser window has been
    resized.) The current implementation considers only viewport-dependent media features."""

    pass


class StylesheetaddedEvent(CDPModel):
    """Fired whenever an active document stylesheet is added."""

    header: CSSStyleSheetHeader


class StylesheetchangedEvent(CDPModel):
    """Fired whenever a stylesheet is changed as a result of the client operation."""

    style_sheet_id: dom.StyleSheetId


class StylesheetremovedEvent(CDPModel):
    """Fired whenever an active document stylesheet is removed."""

    style_sheet_id: dom.StyleSheetId


class ComputedstyleupdatedEvent(CDPModel):
    node_id: dom.NodeId
