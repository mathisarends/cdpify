from enum import Enum


class UnsetType(Enum):
    """The singleton marker for an omitted, potentially null-valued CDP field."""

    UNSET = 0

    def __repr__(self) -> str:
        return "UNSET"


UNSET = UnsetType.UNSET
