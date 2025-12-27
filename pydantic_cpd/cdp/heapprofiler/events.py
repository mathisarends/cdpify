"""Generated event models from CDP specification"""
# Domain: HeapProfiler Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class AddheapsnapshotchunkEvent(CDPModel):
    chunk: str


class HeapstatsupdateEvent(CDPModel):
    """If heap objects tracking has been started then backend may send update for one or more fragments"""

    stats_update: list[int]


class LastseenobjectidEvent(CDPModel):
    """If heap objects tracking has been started then backend regularly sends a current value for last
    seen object id and corresponding timestamp. If the were changes in the heap since last event
    then one or more heapStatsUpdate events will be sent before a new lastSeenObjectId event."""

    last_seen_object_id: int
    timestamp: float


class ReportheapsnapshotprogressEvent(CDPModel):
    done: int
    total: int
    finished: bool | None = None


class ResetprofilesEvent(CDPModel):
    pass
