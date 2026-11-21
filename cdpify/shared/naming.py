import re
from functools import lru_cache

# A trailing plural s belongs to the acronym, as in URLs or IDs.
_CAMEL_PATTERN_1 = re.compile(r"(.)([A-Z](?!s(?:$|[A-Z_]))[a-z]+)")
_CAMEL_PATTERN_2 = re.compile(r"([a-z0-9])([A-Z])")


@lru_cache(maxsize=512)
def to_snake_case(name: str) -> str:
    """Convert camelCase/PascalCase to snake_case, keeping acronyms intact."""
    partly_split = _CAMEL_PATTERN_1.sub(r"\1_\2", name)
    return _CAMEL_PATTERN_2.sub(r"\1_\2", partly_split).lower()
