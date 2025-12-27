"""Generated event models from CDP specification"""
# Domain: LayerTree Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *

from pydantic_cpd.cdp import dom


class LayerpaintedEvent(CDPModel):
    layer_id: LayerId
    clip: dom.Rect


class LayertreedidchangeEvent(CDPModel):
    layers: list[Layer] | None = None
