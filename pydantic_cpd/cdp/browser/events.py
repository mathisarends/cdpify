"""Generated event models from CDP specification"""
# Domain: Browser Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *

from pydantic_cpd.cdp import page


class DownloadwillbeginEvent(CDPModel):
    """Fired when page is about to start a download."""

    frame_id: page.FrameId
    guid: str
    url: str
    suggested_filename: str


class DownloadprogressEvent(CDPModel):
    """Fired when download makes progress. Last call has |done| == true."""

    guid: str
    total_bytes: float
    received_bytes: float
    state: Literal["inProgress", "completed", "canceled"]
    file_path: str | None = None
