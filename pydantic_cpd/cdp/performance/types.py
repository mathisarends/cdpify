"""Generated from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

class Metric(CDPModel):
    """
    Run-time execution metric.
    """
    name: str
    value: float
