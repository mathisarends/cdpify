"""Generated event models from CDP specification"""
# Domain: Audits Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class IssueaddedEvent(CDPModel):
    issue: InspectorIssue
