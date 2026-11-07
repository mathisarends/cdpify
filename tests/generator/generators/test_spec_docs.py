import ast

from cdpify.generator.generators import commands, events, types
from cdpify.generator.generators.domain import generate
from cdpify.generator.schemas import Command, Domain, Event, Parameter, TypeDefinition


def test_method_docs_include_parameter_units_and_lifecycle() -> None:
    domain = Domain(
        domain="Sample",
        commands=[
            Command(
                name="evaluate",
                description="Evaluates an expression.",
                experimental=True,
                parameters=[
                    Parameter(
                        name="timeout",
                        type="number",
                        optional=True,
                        description="Execution limit in milliseconds.",
                        deprecated=True,
                    )
                ],
            )
        ],
    )
    source = generate(domain)
    ast.parse(source)
    assert "Args:" in source
    assert "timeout: Execution limit in milliseconds." in source
    assert "Deprecated in the Chrome DevTools Protocol." in " ".join(source.split())
    assert "Experimental: this API may change or be removed." in source


def test_model_fields_and_type_lifecycle_keep_spec_documentation() -> None:
    domain = Domain(
        domain="Sample",
        types=[
            TypeDefinition(
                id="Data",
                type="object",
                deprecated=True,
                properties=[
                    Parameter(
                        name="byteCount",
                        type="integer",
                        description="Size in bytes.",
                        experimental=True,
                    )
                ],
            )
        ],
        events=[
            Event(
                name="changed",
                experimental=True,
                parameters=[
                    Parameter(
                        name="value", type="string", description="The changed value."
                    )
                ],
            )
        ],
        commands=[
            Command(
                name="put",
                parameters=[
                    Parameter(
                        name="value", type="string", description="The value to store."
                    )
                ],
            )
        ],
    )
    for source in (
        types.generate(domain),
        events.generate(domain),
        commands.generate(domain),
    ):
        ast.parse(source)
    assert "Size in bytes." in types.generate(domain)
    assert "Deprecated in the Chrome DevTools Protocol." in types.generate(domain)
    assert "The changed value." in events.generate(domain)
    assert "The value to store." in commands.generate(domain)


def test_spec_descriptions_cannot_break_generated_python_literals() -> None:
    text = 'A """quoted""" value under C:\\path.'
    domain = Domain(
        domain="Sample",
        types=[TypeDefinition(id="Value", type="string", description=text)],
        commands=[
            Command(
                name="put",
                description=text,
                parameters=[Parameter(name="value", type="string", description=text)],
            )
        ],
    )
    for source in (types.generate(domain), commands.generate(domain), generate(domain)):
        ast.parse(source)
