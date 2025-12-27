"""Generated event models from CDP specification"""
# Domain: DOMStorage Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class DomstorageitemaddedEvent(CDPModel):
    storage_id: StorageId
    key: str
    new_value: str


class DomstorageitemremovedEvent(CDPModel):
    storage_id: StorageId
    key: str


class DomstorageitemupdatedEvent(CDPModel):
    storage_id: StorageId
    key: str
    old_value: str
    new_value: str


class DomstorageitemsclearedEvent(CDPModel):
    storage_id: StorageId
