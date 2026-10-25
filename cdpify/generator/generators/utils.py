import keyword

from cdpify.generator.schemas import Parameter
from cdpify.shared.naming import to_snake_case


def map_cdp_type(param: Parameter) -> str:
    base_type = _get_base_type(param)

    if param.enum:
        base_type = _create_enum_literal(param.enum)

    return base_type


def to_pascal_case(name: str) -> str:
    if not name:
        return name

    return name[0].upper() + name[1:]


def to_identifier(name: str) -> str:
    """Convert a CDP name to a snake_case identifier that is never a keyword.

    Keywords such as ``or``/``not`` get a trailing underscore (PEP 8); the wire
    name is preserved separately via ``cdp_name`` metadata.
    """
    identifier = to_snake_case(name)
    return f"{identifier}_" if keyword.iskeyword(identifier) else identifier


def to_enum_name(name: str) -> str:
    return to_snake_case(name).upper()


def resolve_type(param: Parameter) -> str:
    if param.ref and "." in param.ref:
        domain, type_name = param.ref.split(".", 1)
        return f"{domain.lower()}.{type_name}"
    return map_cdp_type(param)


def format_docstring(text: str, indent: int = 4) -> str:
    if not text:
        return ""

    indent_str = " " * indent
    max_length = 88 - indent

    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1
        if current_length + word_length > max_length and current_line:
            lines.append(indent_str + " ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += word_length

    if current_line:
        lines.append(indent_str + " ".join(current_line))

    result = [f'{indent_str}"""']
    result.extend(lines)
    result.append(f'{indent_str}"""')

    return "\n".join(result)


def _get_base_type(param: Parameter) -> str:
    if param.ref:
        return param.ref

    if param.type in _BASIC_TYPE_MAPPING:
        return _BASIC_TYPE_MAPPING[param.type]

    if param.type == "array":
        return _create_array_type(param.items)

    return "Any"


def _create_enum_literal(enum_values: list[str]) -> str:
    quoted_values = ", ".join(f'"{value}"' for value in enum_values)
    return f"Literal[{quoted_values}]"


def _create_array_type(items: dict | None) -> str:
    if not items:
        return "list[Any]"

    item_type = _get_array_item_type(items)
    return f"list[{item_type}]"


def _get_array_item_type(item_spec: dict) -> str:
    if "$ref" in item_spec:
        ref = item_spec["$ref"]
        if "." in ref:
            parts = ref.split(".")
            return f"{parts[0].lower()}.{parts[1]}"
        return ref

    if "type" in item_spec:
        return _BASIC_TYPE_MAPPING.get(item_spec["type"], "Any")

    return "Any"


_BASIC_TYPE_MAPPING = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "object": "dict[str, Any]",
    "any": "Any",
}
