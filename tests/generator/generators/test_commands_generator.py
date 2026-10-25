from cdpify.generator.generators import commands
from cdpify.generator.schemas import Command, Domain, Parameter


def test_renders_header_and_imports(simple_domain: Domain) -> None:
    output = commands.generate(simple_domain)

    assert "auto-generated" in output
    assert "from dataclasses import dataclass, field" in output
    assert "from enum import StrEnum" in output
    assert "cdpify.shared.models" not in output


def test_renders_command_enum(simple_domain: Domain) -> None:
    output = commands.generate(simple_domain)

    assert "class SampleCommand(StrEnum):" in output
    assert 'GET_NODE = "Sample.getNode"' in output
    assert 'CLEAR = "Sample.clear"' in output
    assert 'LEGACY_OP = "Sample.legacyOp"' in output


def test_renders_params_model(simple_domain: Domain) -> None:
    output = commands.generate(simple_domain)

    assert "@dataclass(kw_only=True, slots=True)" in output
    assert "class GetNodeParams:" in output
    assert 'node_id: NodeId = field(metadata={"cdp_name": "nodeId"})' in output
    assert "Fetches a node by id." in output


def test_renders_result_model(simple_domain: Domain) -> None:
    output = commands.generate(simple_domain)
    assert "@dataclass(kw_only=True, slots=True)" in output
    assert "class GetNodeResult:" in output
    assert "box: Box\n" in output


def test_command_without_params_omits_params_class(simple_domain: Domain) -> None:
    output = commands.generate(simple_domain)
    assert "class ClearParams" not in output


def test_command_without_returns_omits_result_class(simple_domain: Domain) -> None:
    output = commands.generate(simple_domain)
    assert "class ClearResult" not in output
    assert "class LegacyOpResult" not in output


def test_local_type_imports_are_collected(simple_domain: Domain) -> None:
    output = commands.generate(simple_domain)
    assert "from .types import (" in output
    assert "    NodeId," in output
    assert "    Box," in output


def test_empty_domain_marker(empty_domain: Domain) -> None:
    output = commands.generate(empty_domain)
    assert "# No commands defined" in output


def test_cross_domain_imports_are_not_type_checked() -> None:
    domain = Domain(
        domain="Animation",
        commands=[
            Command(
                name="play",
                parameters=[Parameter(name="target", ref="DOM.NodeId")],
            )
        ],
    )

    output = commands.generate(domain)

    assert "from cdpify.domains import dom" in output
    assert "if TYPE_CHECKING:" not in output
    assert "target: dom.NodeId" in output


def test_optional_param_renders_with_none_default() -> None:
    domain = Domain(
        domain="Sample",
        commands=[
            Command(
                name="op",
                parameters=[Parameter(name="extra", type="string", optional=True)],
            )
        ],
    )

    output = commands.generate(domain)
    assert "extra: str | None = None" in output
    assert "from dataclasses import dataclass\n" in output
