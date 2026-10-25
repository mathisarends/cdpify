from collections.abc import Callable

import pytest

from cdpify.generator.generators import commands, domain, events, init, types
from cdpify.generator.schemas import Command, Domain, Parameter, TypeDefinition


@pytest.mark.parametrize(
    ("filename", "render"),
    [
        ("types.py", types.generate),
        ("commands.py", commands.generate),
        ("events.py", events.generate),
        ("domain.py", domain.generate),
        ("__init__.py", init.generate),
    ],
)
def test_generated_domain_modules_compile(
    filename: str,
    render: Callable[[Domain], str],
    simple_domain: Domain,
) -> None:
    source = render(simple_domain)

    compile(source, filename, "exec")


@pytest.mark.parametrize("render", [types.generate, commands.generate, domain.generate])
def test_keyword_field_names_generate_valid_code(
    render: Callable[[Domain], str],
) -> None:
    keyword_parameter = Parameter(name="or", type="boolean", optional=True)
    keyword_domain = Domain(
        domain="Keywords",
        types=[
            TypeDefinition(
                id="Condition", type="object", properties=[keyword_parameter]
            )
        ],
        commands=[Command(name="match", parameters=[keyword_parameter])],
    )

    source = render(keyword_domain)

    compile(source, "generated.py", "exec")
    assert "or_" in source
