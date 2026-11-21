from cdpify.generator.generators.annotations import resolve_type
from cdpify.generator.generators.constants import FUTURE_ANNOTATIONS, HEADER
from cdpify.generator.generators.context import GenerationContext
from cdpify.generator.generators.docstrings import api_description, format_docstring
from cdpify.generator.generators.names import event_class_name, to_enum_name
from cdpify.generator.generators.views import (
    EnumMemberView,
    FieldView,
    ModelView,
    dataclass_import,
    model_fields,
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

    uses_unset = any(field.uses_unset for field in model_fields(models))
    return render_template(
        "events.py.jinja2",
        header=HEADER,
        future_annotations=FUTURE_ANNOTATIONS,
        typing_names=tuple(sorted({*ctx.sorted_typing_names, "ClassVar"})),
        local_type_names=ctx.local_import_names(aliases),
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
        uses_unset=uses_unset,
        dataclass_import=dataclass_import(models),
    )


def _aliases_for(domain: Domain, ctx: GenerationContext) -> dict[str, str]:
    enum_name = f"{domain.domain}Event"
    if ctx.references_local_type(enum_name):
        return {enum_name: f"{enum_name}Type"}
    return {}


def _build_models(
    domain: Domain,
    aliases: dict[str, str],
    ctx: GenerationContext,
) -> list[ModelView]:
    return [
        _build_event_model(event, domain.domain, aliases=aliases, ctx=ctx)
        for event in domain.events
    ]


def _build_event_model(
    event: Event,
    domain_name: str,
    *,
    aliases: dict[str, str],
    ctx: GenerationContext,
) -> ModelView:
    event_fqn = f"{domain_name}.{event.name}"
    class_name = event_class_name(event.name)
    return ModelView(
        name=class_name,
        docstring=(
            format_docstring(
                api_description(
                    event.description,
                    experimental=event.experimental,
                    deprecated=event.deprecated,
                ),
                indent=4,
            )
            or None
        ),
        fields=tuple(
            _build_field_view(param, event_fqn, aliases=aliases, ctx=ctx)
            for param in event.parameters
        ),
        event_member=to_enum_name(event.name),
    )


def _build_field_view(
    param: Parameter,
    event_fqn: str,
    *,
    aliases: dict[str, str],
    ctx: GenerationContext,
) -> FieldView:
    annotation = resolve_type(param)
    py_type = aliases.get(annotation, annotation)
    ctx.track_type_string(py_type)

    return FieldView.from_parameter(
        param,
        py_type,
        force_optional=param.name in _OPTIONAL_OVERRIDES.get(event_fqn, ()),
    )
