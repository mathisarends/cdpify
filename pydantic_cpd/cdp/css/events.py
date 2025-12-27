"""Generated event models from CDP specification"""

from typing import TYPE_CHECKING
from pydantic_cpd.cdp.base import CDPModel

from .types import *

if TYPE_CHECKING:
    from pydantic_cpd.cdp import dom

class FontsUpdatedEvent(CDPModel):
    """
    Fires whenever a web font is updated. A non-empty font parameter indicates a
    successfully loaded web font.
    """
    font: FontFace | None = None

class MediaQueryResultChangedEvent(CDPModel):
    """
    Fires whenever a MediaQuery result changes (for example, after a browser window has
    been resized.) The current implementation considers only viewport-dependent media
    features.
    """
    pass

class StyleSheetAddedEvent(CDPModel):
    """
    Fired whenever an active document stylesheet is added.
    """
    header: CSSStyleSheetHeader

class StyleSheetChangedEvent(CDPModel):
    """
    Fired whenever a stylesheet is changed as a result of the client operation.
    """
    style_sheet_id: dom.StyleSheetId

class StyleSheetRemovedEvent(CDPModel):
    """
    Fired whenever an active document stylesheet is removed.
    """
    style_sheet_id: dom.StyleSheetId

class ComputedStyleUpdatedEvent(CDPModel):
    node_id: dom.NodeId
