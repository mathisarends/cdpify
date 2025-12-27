"""Generated event models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class DomStorageItemAddedEvent(CDPModel):
    storage_id: StorageId
    key: str
    new_value: str

class DomStorageItemRemovedEvent(CDPModel):
    storage_id: StorageId
    key: str

class DomStorageItemUpdatedEvent(CDPModel):
    storage_id: StorageId
    key: str
    old_value: str
    new_value: str

class DomStorageItemsClearedEvent(CDPModel):
    storage_id: StorageId
