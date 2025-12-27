"""Generated from CDP specification"""

from typing import Literal
from pydantic_cpd.cdp.base import CDPModel

"""
Memory pressure level.
"""
PressureLevel = Literal["moderate", "critical"]

class SamplingProfileNode(CDPModel):
    """
    Heap profile sample.
    """
    size: float
    total: float
    stack: list[str]

class SamplingProfile(CDPModel):
    """
    Array of heap profile samples.
    """
    samples: list[SamplingProfileNode]
    modules: list[Module]

class Module(CDPModel):
    """
    Executable module information
    """
    name: str
    uuid: str
    base_address: str
    size: float

class DOMCounter(CDPModel):
    """
    DOM object counter data.
    """
    name: str
    count: int
