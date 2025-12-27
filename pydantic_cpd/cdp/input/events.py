"""Generated event models from CDP specification"""
# Domain: Input Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class DraginterceptedEvent(CDPModel):
    """Emitted only when `Input.setInterceptDrags` is enabled. Use this data with `Input.dispatchDragEvent` to
    restore normal drag and drop behavior."""

    data: DragData
