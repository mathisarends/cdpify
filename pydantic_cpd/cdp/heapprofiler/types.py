"""Generated from CDP specification"""

from typing import TYPE_CHECKING
from pydantic_cpd.cdp.base import CDPModel

if TYPE_CHECKING:
    from pydantic_cpd.cdp import runtime

"""
Heap snapshot object id.
"""
HeapSnapshotObjectId = str

class SamplingHeapProfileNode(CDPModel):
    """
    Sampling Heap Profile node. Holds callsite information, allocation statistics and
    child nodes.
    """
    call_frame: runtime.CallFrame
    self_size: float
    id: int
    children: list[SamplingHeapProfileNode]

class SamplingHeapProfileSample(CDPModel):
    """
    A single sample from a sampling profile.
    """
    size: float
    node_id: int
    ordinal: float

class SamplingHeapProfile(CDPModel):
    """
    Sampling profile.
    """
    head: SamplingHeapProfileNode
    samples: list[SamplingHeapProfileSample]
