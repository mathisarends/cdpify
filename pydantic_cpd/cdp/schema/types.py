"""Generated from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

class Domain(CDPModel):
    """
    Description of the protocol domain.
    """
    name: str
    version: str
