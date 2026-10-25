from cdpify.generator.generators.constants import FUTURE_ANNOTATIONS, HEADER
from cdpify.generator.generators.context import GenerationContext
from cdpify.generator.generators.utils import (
    format_docstring,
    resolve_type,
    to_enum_name,
    to_identifier,
    to_pascal_case,
)
from cdpify.generator.generators.views import EnumMemberView, FieldView, ModelView
from cdpify.generator.rendering import render_template
from cdpify.generator.schemas import Command, Domain, Parameter


def generate(domain: Domain) -> str:
    ctx = GenerationContext()
    for command in domain.commands:
        _scan_command(command, ctx)

    models = tuple(_build_models(domain.commands, ctx))
    # Cross-domain imports must remain runtime imports so that
    # `get_type_hints()` (used by decode_cdp) can resolve forward
    # references like `dom.Rect`. `from __future__ import annotations`
    # defers annotation evaluation, avoiding the circular-import problem
    # until first deserialization.
    return render_template(
        "commands.py.jinja2",
        header=HEADER,
        future_annotations=FUTURE_ANNOTATIONS,
        typing_names=ctx.sorted_typing_names,
        local_type_names=tuple(name for name, _ in ctx.sorted_local_types()),
        cross_domain_modules=ctx.cross_domain_modules,
        domain_name=domain.domain,
        command_members=tuple(
            EnumMemberView(
                name=to_enum_name(command.name),
                value=f"{domain.domain}.{command.name}",
            )
            for command in domain.commands
        ),
        models=models,
    )


def _scan_command(command: Command, ctx: GenerationContext) -> None:
    for param in command.parameters:
        ctx.scan_param(param)
    for param in command.returns:
        ctx.scan_param(param)


def _build_models(commands: list[Command], ctx: GenerationContext) -> list[ModelView]:
    models: list[ModelView] = []
    for command in commands:
        if command.parameters:
            models.append(_build_params_model(command, ctx))
        if command.returns:
            models.append(_build_result_model(command, ctx))
    return models


def _build_params_model(command: Command, ctx: GenerationContext) -> ModelView:
    return ModelView(
        name=f"{to_pascal_case(command.name)}Params",
        docstring=(
            format_docstring(command.description, indent=4)
            if command.description
            else None
        ),
        fields=tuple(_build_field_view(param, ctx) for param in command.parameters),
    )


def _build_result_model(command: Command, ctx: GenerationContext) -> ModelView:
    return ModelView(
        name=f"{to_pascal_case(command.name)}Result",
        fields=tuple(_build_field_view(param, ctx) for param in command.returns),
    )


def _build_field_view(param: Parameter, ctx: GenerationContext) -> FieldView:
    field_name = to_identifier(param.name)
    py_type = resolve_type(param)
    ctx.track_type_string(py_type)
    return FieldView(
        field_name,
        py_type,
        optional=param.optional,
        cdp_name=param.name,
    )
