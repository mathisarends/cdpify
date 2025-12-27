"""Generated command models from CDP specification"""
# Domain: Memory Commands

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class GetDOMCountersResult(CDPModel):
    documents: int
    nodes: int
    js_event_listeners: int


class GetDOMCountersForLeakDetectionResult(CDPModel):
    counters: list[DOMCounter]


class SetPressureNotificationsSuppressedParams(CDPModel):
    """Enable/disable suppressing memory pressure notifications in all processes."""

    suppressed: bool


class SimulatePressureNotificationParams(CDPModel):
    """Simulate a memory pressure notification in all processes."""

    level: PressureLevel


class StartSamplingParams(CDPModel):
    """Start collecting native memory profile."""

    sampling_interval: int | None = None
    suppress_randomness: bool | None = None


class GetAllTimeSamplingProfileResult(CDPModel):
    profile: SamplingProfile


class GetBrowserSamplingProfileResult(CDPModel):
    profile: SamplingProfile


class GetSamplingProfileResult(CDPModel):
    profile: SamplingProfile
