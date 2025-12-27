"""Generated command models from CDP specification"""
# Domain: DeviceOrientation Commands

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class SetDeviceOrientationOverrideParams(CDPModel):
    """Overrides the Device Orientation."""

    alpha: float
    beta: float
    gamma: float
