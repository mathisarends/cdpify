"""Generated command models from CDP specification"""
# Domain: Schema Commands

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class GetDomainsResult(CDPModel):
    domains: list[Domain]
