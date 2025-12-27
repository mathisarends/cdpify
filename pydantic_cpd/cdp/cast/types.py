"""Generated from CDP specification"""
# Domain: Cast
# A domain for interacting with Cast, Presentation API, and Remote Playback API
# functionalities.

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel


class Sink(CDPModel):
    name: str
    id: str
    session: str | None = None
