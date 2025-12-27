"""Generated command models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class ClearParams(CDPModel):
    storage_id: StorageId

class GetDOMStorageItemsParams(CDPModel):
    storage_id: StorageId

class GetDOMStorageItemsResult(CDPModel):
    entries: list[Item]

class RemoveDOMStorageItemParams(CDPModel):
    storage_id: StorageId
    key: str

class SetDOMStorageItemParams(CDPModel):
    storage_id: StorageId
    key: str
    value: str
