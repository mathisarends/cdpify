"""Generated event models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class IssueAddedEvent(CDPModel):
    issue: InspectorIssue
