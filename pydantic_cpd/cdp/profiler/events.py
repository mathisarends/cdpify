"""Generated event models from CDP specification"""
# Domain: Profiler Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *

from pydantic_cpd.cdp import debugger


class ConsoleprofilefinishedEvent(CDPModel):
    id: str
    location: debugger.Location
    profile: Profile
    title: str | None = None


class ConsoleprofilestartedEvent(CDPModel):
    """Sent when new profile recording is started using console.profile() call."""

    id: str
    location: debugger.Location
    title: str | None = None


class PrecisecoveragedeltaupdateEvent(CDPModel):
    """Reports coverage delta since the last poll (either from an event like this, or from
    `takePreciseCoverage` for the current isolate. May only be sent if precise code
    coverage has been started. This event can be trigged by the embedder to, for example,
    trigger collection of coverage data immediately at a certain point in time."""

    timestamp: float
    occasion: str
    result: list[ScriptCoverage]
