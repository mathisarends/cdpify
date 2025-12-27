"""Generated from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

class Sink(CDPModel):
    name: str
    id: str
    session: str | None = None
