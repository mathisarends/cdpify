"""Generated event models from CDP specification"""
# Domain: Tracing Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *

from pydantic_cpd.cdp import io


class BufferusageEvent(CDPModel):
    percent_full: float | None = None
    event_count: float | None = None
    value: float | None = None


class DatacollectedEvent(CDPModel):
    """Contains a bucket of collected trace events. When tracing is stopped collected events will be
    sent as a sequence of dataCollected events followed by tracingComplete event."""

    value: list[dict[str, Any]]


class TracingcompleteEvent(CDPModel):
    """Signals that tracing is stopped and there is no trace buffers pending flush, all data were
    delivered via dataCollected events."""

    data_loss_occurred: bool
    stream: io.StreamHandle | None = None
    trace_format: StreamFormat | None = None
    stream_compression: StreamCompression | None = None
