from enum import StrEnum
from typing import Self


class CDPStrEnum(StrEnum):
    """A protocol enum that also preserves values from newer CDP versions."""

    @classmethod
    def _missing_(cls, value: object) -> Self | None:
        if not isinstance(value, str):
            return None

        member = str.__new__(cls, value)
        # Unknown values deliberately have no declared member name. Enum's
        # annotation only describes declared members, whose names are strings.
        member._name_ = None  # pyright: ignore[reportAttributeAccessIssue]
        member._value_ = value
        # Do not cache arbitrary browser values in the enum's member maps.
        return member
