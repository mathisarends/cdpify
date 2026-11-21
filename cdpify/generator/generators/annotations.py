"""Render Python type annotations from CDP parameter definitions."""

from cdpify.generator.schemas import Parameter
from cdpify.shared.naming import to_snake_case


def resolve_type(param: Parameter) -> str:
    if param.ref and "." in param.ref:
        domain, type_name = param.ref.split(".", 1)
        return f"{to_snake_case(domain)}.{type_name}"
    return map_cdp_type(param)


def map_cdp_type(param: Parameter) -> str:
    base_type = _get_base_type(param)

    if param.enum:
        base_type = _create_enum_literal(param.enum)

    return base_type


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
            return f"{to_snake_case(parts[0])}.{parts[1]}"
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
