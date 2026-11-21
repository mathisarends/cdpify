"""Translate CDP names to Python identifiers and check for collisions."""

import keyword
import re
from collections import Counter
from collections.abc import Iterable

from cdpify.shared.naming import to_snake_case


def event_class_name(name: str) -> str:
    return to_pascal_case(name).removesuffix("Event") + "Event"


def to_pascal_case(name: str) -> str:
    if not name:
        return name

    return name[0].upper() + name[1:]


def require_unique_names(names: Iterable[str], scope: str) -> None:
    duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
    if duplicates:
        raise ValueError(f"Duplicate {scope}: {', '.join(duplicates)}")


def to_identifier(name: str) -> str:
    """Convert a CDP name to a snake_case identifier that is never a keyword.

    Keywords such as ``or``/``not`` get a trailing underscore (PEP 8); the wire
    name is preserved separately via ``cdp_name`` metadata.
    """
    identifier = to_snake_case(name)
    return f"{identifier}_" if keyword.iskeyword(identifier) else identifier


def to_enum_name(name: str) -> str:
    identifier = re.sub(r"\W+", "_", to_snake_case(name)).strip("_").upper()
    if not identifier:
        return "EMPTY"
    return f"VALUE_{identifier}" if identifier[0].isdigit() else identifier
