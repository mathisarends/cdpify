from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class CDPEvent(Generic[T]):
    name: str
    data: T
