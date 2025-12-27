"""Generated from CDP specification"""
# Domain: DOMStorage
# Query and modify DOM storage.

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

SerializedStorageKey = str


class StorageId(CDPModel):
    """DOM Storage identifier."""

    security_origin: str | None = None
    storage_key: SerializedStorageKey | None = None
    is_local_storage: bool


# DOM Storage item.
Item = list[Any]
