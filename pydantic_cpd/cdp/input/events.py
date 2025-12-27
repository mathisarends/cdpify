"""Generated event models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class DragInterceptedEvent(CDPModel):
    """
    Emitted only when `Input.setInterceptDrags` is enabled. Use this data with
    `Input.dispatchDragEvent` to restore normal drag and drop behavior.
    """
    data: DragData
