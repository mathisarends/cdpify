"""Generated command models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class StartViolationsReportParams(CDPModel):
    """
    start violation reporting.
    """
    config: list[ViolationSetting]
