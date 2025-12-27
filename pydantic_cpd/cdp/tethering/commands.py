"""Generated command models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class BindParams(CDPModel):
    """
    Request browser port binding.
    """
    port: int

class UnbindParams(CDPModel):
    """
    Request browser port unbinding.
    """
    port: int
