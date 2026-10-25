from cdpify.generator.generators import types
from cdpify.generator.schemas import Domain, Parameter, TypeDefinition


def test_generates_header_and_dataclass_imports(simple_domain: Domain) -> None:
    output = types.generate(simple_domain)

    assert "auto-generated" in output
    assert "from __future__ import annotations" in output
    assert "from dataclasses import dataclass\n" in output
    assert "cdpify.shared.models" not in output


def test_renders_alias_for_primitive_type(simple_domain: Domain) -> None:
    output = types.generate(simple_domain)
    assert "NodeId = int" in output


def test_array_alias_keeps_item_type() -> None:
    domain = Domain(
        domain="Target",
        types=[
            TypeDefinition(id="FilterEntry", type="object", properties=[]),
            TypeDefinition(
                id="TargetFilter", type="array", items={"$ref": "FilterEntry"}
            ),
            TypeDefinition(id="Quad", type="array", items={"type": "number"}),
            TypeDefinition(id="Frames", type="array", items={"$ref": "Page.FrameId"}),
        ],
    )

    output = types.generate(domain)

    assert "TargetFilter = list[FilterEntry]" in output
    assert "Quad = list[float]" in output
    assert "Frames = list[page.FrameId]" in output
    assert "from cdpify.domains import page" in output


def test_renders_enum_as_literal(simple_domain: Domain) -> None:
    output = types.generate(simple_domain)
    assert 'type Color = Literal["red", "green", "blue"]' in output
    assert "from typing import" in output and "Literal" in output


def test_renders_object_as_dataclass(simple_domain: Domain) -> None:
    output = types.generate(simple_domain)

    assert "@dataclass(kw_only=True, slots=True)" in output
    assert "class Box:" in output
    assert "width: int\n" in output
    assert "height: int\n" in output
    assert "label: str | None = None" in output
    assert "metadata=" not in output


def test_alias_docstring_follows_the_assignment() -> None:
    domain = Domain(
        domain="Page",
        types=[
            TypeDefinition(
                id="FrameId", type="string", description="Unique frame identifier."
            ),
            TypeDefinition(
                id="Kind", type="string", enum=["a", "b"], description="Frame kind."
            ),
        ],
    )

    output = types.generate(domain)

    assert 'FrameId = str\n"""\nUnique frame identifier.\n"""' in output
    assert 'type Kind = Literal["a", "b"]\n"""\nFrame kind.\n"""' in output


def test_includes_descriptions_as_docstrings(simple_domain: Domain) -> None:
    output = types.generate(simple_domain)
    assert "A bounding box." in output


def test_empty_domain_emits_marker(empty_domain: Domain) -> None:
    output = types.generate(empty_domain)
    assert "# No types defined" in output


def test_cross_domain_ref_uses_runtime_import() -> None:
    domain = Domain(
        domain="Animation",
        types=[
            TypeDefinition(
                id="Track",
                type="object",
                properties=[Parameter(name="target", ref="DOM.NodeId")],
            )
        ],
    )

    output = types.generate(domain)

    assert "from cdpify.domains import dom" in output
    assert "target: dom.NodeId" in output
    assert "if TYPE_CHECKING:" not in output
    assert "TYPE_CHECKING" not in output


def test_optional_override_makes_field_optional() -> None:
    domain = Domain(
        domain="DOMSnapshot",
        types=[
            TypeDefinition(
                id="DocumentSnapshot",
                type="object",
                properties=[
                    Parameter(name="documentURL", type="string"),
                    Parameter(name="title", type="string"),
                ],
            )
        ],
    )

    output = types.generate(domain)

    assert (
        "document_url: str | None = field("
        'default=None, metadata={"cdp_name": "documentURL"})'
    ) in output
    assert "title: str\n" in output


def test_long_aliased_field_declaration_is_lint_safe() -> None:
    domain = Domain(
        domain="Sample",
        types=[
            TypeDefinition(
                id="Container",
                type="object",
                properties=[
                    Parameter(
                        name="federatedAuthUserInfoRequestIssueReason",
                        ref="FederatedAuthUserInfoRequestIssueReason",
                    )
                ],
            )
        ],
    )

    output = types.generate(domain)

    assert "field(  # noqa: E501" in output
