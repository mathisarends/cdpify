from cdpify.generator.generators.constants import FUTURE_ANNOTATIONS, HEADER
from cdpify.generator.generators.context import GenerationContext
from cdpify.generator.generators.utils import (
    format_docstring,
    resolve_type,
    to_enum_name,
    to_identifier,
    to_pascal_case,
    to_snake_case,
)
from cdpify.generator.generators.views import FieldView, MethodView
from cdpify.generator.rendering import render_template
from cdpify.generator.schemas import Command, Domain, Parameter


def generate(domain: Domain) -> str:
    ctx = GenerationContext()
    methods = tuple(
        _build_method(command, domain.domain, ctx) for command in domain.commands
    )

    if ctx.cross_domain_modules:
        ctx.use_typing("TYPE_CHECKING")

    return render_template(
        "domain.py.jinja2",
        header=HEADER,
        future_annotations=FUTURE_ANNOTATIONS,
        typing_names=ctx.sorted_typing_names,
        has_deprecated=any(command.deprecated for command in domain.commands),
        command_imports=_command_imports(domain),
        local_type_names=tuple(name for name, _ in ctx.sorted_local_types()),
        cross_domain_modules=ctx.cross_domain_modules,
        domain_name=domain.domain,
        methods=methods,
    )


def _command_imports(domain: Domain) -> tuple[str, ...]:
    if not domain.commands:
        return ()

    model_names = {
        f"{to_pascal_case(command.name)}Params"
        for command in domain.commands
        if command.parameters
    }
    model_names.update(
        f"{to_pascal_case(command.name)}Result"
        for command in domain.commands
        if command.returns
    )
    return (f"{domain.domain}Command", *sorted(model_names))


def _build_method(
    command: Command, domain_name: str, ctx: GenerationContext
) -> MethodView:
    parameters = tuple(
        _build_parameter_view(parameter, ctx) for parameter in command.parameters
    )
    pascal_name = to_pascal_case(command.name)

    if command.returns:
        return_type = f"{pascal_name}Result"
        result_model = return_type
    else:
        return_type = "None"
        result_model = None

    params_model = f"{pascal_name}Params" if command.parameters else None
    constructor_args = ", ".join(
        f"{to_identifier(parameter.name)}={to_identifier(parameter.name)}"
        for parameter in command.parameters
    )

    return MethodView(
        name=to_snake_case(command.name),
        parameters=parameters,
        return_type=return_type,
        command_member=to_enum_name(command.name),
        docstring=(
            format_docstring(command.description, indent=8)
            if command.description
            else None
        ),
        deprecation=(
            f"{domain_name}.{command.name} is deprecated"
            if command.deprecated
            else None
        ),
        params_model=params_model,
        constructor_args=constructor_args,
        result_model=result_model,
    )


def _build_parameter_view(parameter: Parameter, ctx: GenerationContext) -> FieldView:
    ctx.scan_param(parameter)
    annotation = resolve_type(parameter)
    ctx.track_type_string(annotation)
    return FieldView(
        name=to_identifier(parameter.name),
        annotation=annotation,
        optional=parameter.optional,
    )
