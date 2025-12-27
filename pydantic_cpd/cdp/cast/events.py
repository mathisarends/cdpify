"""Generated event models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class SinksUpdatedEvent(CDPModel):
    """
    This is fired whenever the list of available sinks changes. A sink is a device or a
    software surface that you can cast to.
    """
    sinks: list[Sink]

class IssueUpdatedEvent(CDPModel):
    """
    This is fired whenever the outstanding issue/error message changes. |issueMessage|
    is empty if there is no issue.
    """
    issue_message: str
