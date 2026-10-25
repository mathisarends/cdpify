from cdpify.generator.generators.constants import FUTURE_ANNOTATIONS, HEADER
from cdpify.generator.generators.context import GenerationContext
from cdpify.generator.generators.utils import (
    format_docstring,
    resolve_type,
    to_enum_name,
    to_identifier,
    to_pascal_case,
)
from cdpify.generator.generators.views import (
    EnumMemberView,
    FieldView,
    ModelView,
    dataclass_import,
)
from cdpify.generator.rendering import render_template
from cdpify.generator.schemas import Domain, Event, Parameter

_OPTIONAL_OVERRIDES: dict[str, set[str]] = {
    "Network.requestWillBeSent": {"documentURL"},
}


def generate(domain: Domain) -> str:
    ctx = GenerationContext()
    for event in domain.events:
        for param in event.parameters:
            ctx.scan_param(param)

    aliases = _aliases_for(domain, ctx)
    models = tuple(_build_models(domain, aliases, ctx))

    return render_template(
        "events.py.jinja2",
        header=HEADER,
        future_annotations=FUTURE_ANNOTATIONS,
        typing_names=tuple(sorted({*ctx.sorted_typing_names, "ClassVar"})),
        local_type_names=tuple(
            f"{name} as {alias}" if alias else name
            for name, alias in ctx.sorted_local_types(aliases)
        ),
        cross_domain_modules=ctx.cross_domain_modules,
        domain_name=domain.domain,
        event_members=tuple(
            EnumMemberView(
                name=to_enum_name(event.name),
                value=f"{domain.domain}.{event.name}",
            )
            for event in domain.events
        ),
        models=models,
        dataclass_import=dataclass_import(models),
    )


def _aliases_for(domain: Domain, ctx: GenerationContext) -> dict[str, str]:
    enum_name = f"{domain.domain}Event"
    if enum_name in ctx.local_type_refs:
        return {enum_name: f"{enum_name}Type"}
    return {}


def _build_models(
    domain: Domain,
    aliases: dict[str, str],
    ctx: GenerationContext,
) -> list[ModelView]:
    return [
        _build_event_model(event, domain.domain, aliases, ctx)
        for event in domain.events
    ]


def _build_event_model(
    event: Event,
    domain_name: str,
    aliases: dict[str, str],
    ctx: GenerationContext,
) -> ModelView:
    event_fqn = f"{domain_name}.{event.name}"
    class_name = f"{to_pascal_case(event.name)}Event"
    return ModelView(
        name=class_name,
        docstring=(
            format_docstring(event.description, indent=4) if event.description else None
        ),
        fields=tuple(
            _build_field_view(param, event_fqn, aliases, ctx)
            for param in event.parameters
        ),
        event_name=event_fqn,
    )


def _build_field_view(
    param: Parameter,
    event_fqn: str,
    aliases: dict[str, str],
    ctx: GenerationContext,
) -> FieldView:
    field_name = to_identifier(param.name)
    py_type = aliases.get(resolve_type(param), resolve_type(param))
    ctx.track_type_string(py_type)

    is_optional = param.optional or param.name in _OPTIONAL_OVERRIDES.get(
        event_fqn, set()
    )
    return FieldView(
        field_name,
        py_type,
        optional=is_optional,
        cdp_name=param.name,
    )
