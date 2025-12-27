"""Generated from CDP specification"""
# Domain: IO
# Input/Output operations for streams produced by DevTools.

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

# This is either obtained from another method or specified as `blob:<uuid>` where
# `<uuid>` is an UUID of a Blob.
StreamHandle = str
