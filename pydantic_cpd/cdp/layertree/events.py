"""Generated event models from CDP specification"""

from typing import TYPE_CHECKING
from pydantic_cpd.cdp.base import CDPModel

from .types import *

if TYPE_CHECKING:
    from pydantic_cpd.cdp import dom

class LayerPaintedEvent(CDPModel):
    layer_id: LayerId
    clip: dom.Rect

class LayerTreeDidChangeEvent(CDPModel):
    layers: list[Layer] | None = None
