"""Generated from CDP specification"""
# Domain: Console
# This domain is deprecated - use Runtime or Log instead.

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel


class ConsoleMessage(CDPModel):
    """Console message."""

    source: Literal[
        "xml",
        "javascript",
        "network",
        "console-api",
        "storage",
        "appcache",
        "rendering",
        "security",
        "other",
        "deprecation",
        "worker",
    ]
    level: Literal["log", "warning", "error", "debug", "info"]
    text: str
    url: str | None = None
    line: int | None = None
    column: int | None = None
