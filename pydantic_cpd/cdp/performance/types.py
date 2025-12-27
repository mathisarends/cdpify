"""Generated from CDP specification"""
# Domain: Performance

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel


class Metric(CDPModel):
    """Run-time execution metric."""

    name: str
    value: float
