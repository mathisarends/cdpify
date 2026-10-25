from cdpify.generator.generators import domain as domain_generator
from cdpify.generator.schemas import Command, Domain, Parameter


def test_renders_domain_class(simple_domain: Domain) -> None:
    output = domain_generator.generate(simple_domain)

    assert "class Sample:" in output
    assert "def __init__(self, executor: CommandExecutor) -> None:" in output
    assert "self._executor = executor" in output


def test_depends_on_command_executor_abstraction(simple_domain: Domain) -> None:
    output = domain_generator.generate(simple_domain)

    assert "from cdpify.executor import CommandExecutor" in output
    assert "from cdpify.client import" not in output


def test_method_with_params(simple_domain: Domain) -> None:
    output = domain_generator.generate(simple_domain)

    assert "async def get_node(" in output
    assert "node_id: NodeId," in output
    assert "session_id: str | None = None," not in output
    assert "-> GetNodeResult:" in output
    assert "params = GetNodeParams(node_id=node_id)" in output
    assert "method=SampleCommand.GET_NODE" in output
    assert "result = await self._executor.execute(" in output
    assert "from cdpify.codec import decode_cdp, encode_cdp" in output
    assert "params=encode_cdp(params)" in output
    assert "return decode_cdp(GetNodeResult, result)" in output


def test_method_without_params_or_returns(simple_domain: Domain) -> None:
    output = domain_generator.generate(simple_domain)

    assert "async def clear(" in output
    assert "-> None:" in output
    assert "params=None" in output
    clear_block = output.split("async def clear(")[1].split("async def")[0]
    assert "await self._executor.execute(" in clear_block
    assert "result =" not in clear_block
    assert "return" not in clear_block


def test_deprecated_command_gets_decorator(simple_domain: Domain) -> None:
    output = domain_generator.generate(simple_domain)

    assert "from cdpify.shared.decorators import deprecated" in output
    legacy_block = output.split("async def legacy_op")[0]
    # The decorator must appear directly above the deprecated method
    assert legacy_block.rstrip().endswith(
        '@deprecated("Sample.legacyOp is deprecated")'
    )


def test_no_deprecated_import_when_no_deprecated_commands() -> None:
    domain = Domain(
        domain="Sample",
        commands=[Command(name="op", parameters=[Parameter(name="x", type="string")])],
    )

    output = domain_generator.generate(domain)
    assert "from cdpify.shared.decorators import deprecated" not in output


def test_protocol_session_id_keeps_its_natural_name() -> None:
    domain = Domain(
        domain="Target",
        commands=[
            Command(
                name="attachToTarget",
                parameters=[Parameter(name="sessionId", type="string")],
            )
        ],
    )

    output = domain_generator.generate(domain)

    assert "session_id: str," in output
    assert "AttachToTargetParams(session_id=session_id)" in output


def test_cross_domain_param_resolved_via_type_checking() -> None:
    domain = Domain(
        domain="Animation",
        commands=[
            Command(
                name="play",
                parameters=[Parameter(name="target", ref="DOM.NodeId")],
            )
        ],
    )

    output = domain_generator.generate(domain)

    assert "if TYPE_CHECKING:" in output
    assert "from cdpify.domains import dom" in output
    assert "target: dom.NodeId" in output


def test_command_imports_include_enum_and_classes(simple_domain: Domain) -> None:
    output = domain_generator.generate(simple_domain)

    imports_section = output.split("from .commands import (")[1].split(")")[0]
    assert "SampleCommand" in imports_section
    assert "GetNodeParams" in imports_section
    assert "GetNodeResult" in imports_section
    assert "LegacyOpParams" in imports_section


def test_kw_only_marker_appears_when_command_has_params(simple_domain: Domain) -> None:
    output = domain_generator.generate(simple_domain)

    # Methods with params should have the `*` separator
    get_node_block = output.split("async def get_node(")[1].split(") ->")[0]
    assert "*," in get_node_block
