"""Generated from CDP specification"""

from typing import Any
from pydantic_cpd.cdp.base import CDPModel

SerializedStorageKey = str

class StorageId(CDPModel):
    """
    DOM Storage identifier.
    """
    security_origin: str | None = None
    storage_key: SerializedStorageKey | None = None
    is_local_storage: bool

"""
DOM Storage item.
"""
Item = list[Any]
