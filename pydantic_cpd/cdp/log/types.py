"""Generated from CDP specification"""
# Domain: Log
# Provides access to log entries.

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel


class LogEntry(CDPModel):
    """Log entry."""

    source: Literal[
        "xml",
        "javascript",
        "network",
        "storage",
        "appcache",
        "rendering",
        "security",
        "deprecation",
        "worker",
        "violation",
        "intervention",
        "recommendation",
        "other",
    ]
    level: Literal["verbose", "info", "warning", "error"]
    text: str
    category: Literal["cors"] | None = None
    timestamp: runtime.Timestamp
    url: str | None = None
    line_number: int | None = None
    stack_trace: runtime.StackTrace | None = None
    network_request_id: network.RequestId | None = None
    worker_id: str | None = None
    args: list[Runtime.RemoteObject] | None = None


class ViolationSetting(CDPModel):
    """Violation configuration setting."""

    name: Literal[
        "longTask",
        "longLayout",
        "blockedEvent",
        "blockedParser",
        "discouragedAPIUse",
        "handler",
        "recurringHandler",
    ]
    threshold: float
