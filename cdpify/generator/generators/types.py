from cdpify.generator.generators.constants import FUTURE_ANNOTATIONS, HEADER
from cdpify.generator.generators.context import GenerationContext
from cdpify.generator.generators.utils import (
    api_description,
    format_docstring,
    map_cdp_type,
    resolve_type,
    to_enum_name,
)
from cdpify.generator.generators.views import (
    EnumMemberView,
    FieldView,
    TypeDefinitionView,
    dataclass_import,
    model_fields,
)
from cdpify.generator.rendering import render_template
from cdpify.generator.schemas import Domain, Parameter, TypeDefinition

_OPTIONAL_OVERRIDES: dict[str, set[str]] = {
    "DocumentSnapshot": {"documentURL", "baseURL"},
    "AXRelatedNode": {"backendDOMNodeId"},
}


def generate(domain: Domain) -> str:
    ctx = GenerationContext()
    definitions = tuple(_build_type_view(type_def, ctx) for type_def in domain.types)
    uses_unset = any(field.uses_unset for field in model_fields(definitions))
    has_enums = any(definition.kind == "enum" for definition in definitions)
    return render_template(
        "types.py.jinja2",
        header=HEADER,
        future_annotations=FUTURE_ANNOTATIONS,
        typing_names=ctx.sorted_typing_names,
        cross_domain_modules=ctx.cross_domain_modules,
        definitions=definitions,
        has_enums=has_enums,
        uses_unset=uses_unset,
        dataclass_import=dataclass_import(definitions),
    )


def _build_type_view(
    type_def: TypeDefinition, ctx: GenerationContext
) -> TypeDefinitionView:
    if type_def.enum:
        return _build_enum_view(type_def)
    if type_def.properties:
        return _build_object_view(type_def, ctx)
    return _build_alias_view(type_def, ctx)


def _build_enum_view(type_def: TypeDefinition) -> TypeDefinitionView:
    members = []
    used_names = set()
    for value in type_def.enum or ():
        base_name = to_enum_name(value)
        name = base_name
        suffix = 2
        while name in used_names:
            name = f"{base_name}_{suffix}"
            suffix += 1
        used_names.add(name)
        members.append(EnumMemberView(name=name, value=value))
    return TypeDefinitionView(
        kind="enum",
        name=type_def.id,
        members=tuple(members),
        docstring=_type_docstring(type_def, indent=4),
    )


def _build_object_view(
    type_def: TypeDefinition, ctx: GenerationContext
) -> TypeDefinitionView:
    return TypeDefinitionView(
        kind="object",
        name=type_def.id,
        docstring=_type_docstring(type_def, indent=4),
        fields=tuple(
            _build_field_view(prop, type_def.id, ctx) for prop in type_def.properties
        ),
    )


def _build_alias_view(
    type_def: TypeDefinition, ctx: GenerationContext
) -> TypeDefinitionView:
    py_type = map_cdp_type(
        Parameter(
            name=type_def.id,
            type=type_def.type,
            items=type_def.items,
            optional=False,
        )
    )
    ctx.track_type_string(py_type)
    return TypeDefinitionView(
        kind="alias",
        name=type_def.id,
        annotation=py_type,
        docstring=_type_docstring(type_def, indent=0),
    )


def _build_field_view(
    param: Parameter, type_id: str, ctx: GenerationContext
) -> FieldView:
    py_type = resolve_type(param)

    ctx.scan_ref(param.ref)
    ctx.track_type_string(py_type)

    return FieldView.from_parameter(
        param,
        py_type,
        force_optional=param.name in _OPTIONAL_OVERRIDES.get(type_id, ()),
    )


def _type_docstring(type_def: TypeDefinition, *, indent: int) -> str | None:
    text = api_description(
        type_def.description,
        experimental=type_def.experimental,
        deprecated=type_def.deprecated,
    )
    return format_docstring(text, indent=indent) if text else None
