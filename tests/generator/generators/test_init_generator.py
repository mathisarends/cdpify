from cdpify.generator.generators import init
from cdpify.generator.schemas import Domain, Event, TypeDefinition


def test_renders_module_docstring(simple_domain: Domain) -> None:
    output = init.generate(simple_domain)
    assert '"""CDP Sample Domain."""' in output


def test_imports_types(simple_domain: Domain) -> None:
    output = init.generate(simple_domain)

    types_block = output.split("from .types import")[1].split("from .commands")[0]
    assert "NodeId" in types_block
    assert "Color" in types_block
    assert "Box" in types_block


def test_imports_commands_and_events(simple_domain: Domain) -> None:
    output = init.generate(simple_domain)

    assert "from .commands import" in output
    assert "SampleCommand" in output
    assert "GetNodeParams" in output
    assert "GetNodeResult" in output

    assert "from .events import" in output
    assert "SampleEvent" in output
    assert "NodeAddedEvent" in output
    assert "ClearedEvent" in output


def test_imports_domain_class(simple_domain: Domain) -> None:
    output = init.generate(simple_domain)
    assert "from .domain import Sample" in output


def test_all_exports_sorted_and_complete(simple_domain: Domain) -> None:
    output = init.generate(simple_domain)

    all_block = output.split("__all__ = [")[1].split("]")[0]
    exports = [line.strip().strip(",").strip('"') for line in all_block.splitlines()]
    exports = [e for e in exports if e]

    assert exports == sorted(exports)
    assert "Sample" in exports
    assert "NodeId" in exports
    assert "SampleCommand" in exports
    assert "SampleEvent" in exports


def test_short_import_uses_inline_form(simple_domain: Domain) -> None:
    """Three or fewer names import inline, not as a block."""
    output = init.generate(simple_domain)

    # types has 3 entries → should use inline form
    types_line = next(
        line.strip()
        for line in output.splitlines()
        if line.strip().startswith("from .types import")
    )
    assert "(" not in types_line


def test_block_import_for_many_names(simple_domain: Domain) -> None:
    """Four or more names should use the multi-line block form."""
    output = init.generate(simple_domain)

    # types has 3 entries → inline; commands has 4+ entries → block
    commands_section = output.split("from .commands import")[1].split("from .events")[0]
    assert "(" in commands_section
    assert ")" in commands_section


def test_empty_domain_only_imports_domain_class(empty_domain: Domain) -> None:
    output = init.generate(empty_domain)

    assert "from .domain import Empty" in output
    assert "from .types import" not in output
    assert "from .commands import" not in output
    assert "from .events import" not in output
    assert '"Empty"' in output


def test_aliases_type_that_collides_with_domain_class() -> None:
    domain = Domain(
        domain="Animation",
        types=[TypeDefinition(id="Animation", type="object")],
    )

    output = init.generate(domain)

    assert "from .types import Animation as AnimationType" in output
    assert "from .domain import Animation" in output
    assert '"Animation"' in output
    assert '"AnimationType"' in output


def test_aliases_event_enum_when_it_collides_with_a_type() -> None:
    domain = Domain(
        domain="BackgroundService",
        types=[TypeDefinition(id="BackgroundServiceEvent", type="object")],
        events=[Event(name="eventReceived")],
    )

    output = init.generate(domain)

    assert "BackgroundServiceEvent as BackgroundServiceEventName" in output
    assert '"BackgroundServiceEvent",' in output
    assert '"BackgroundServiceEventName",' in output


def test_exports_are_resolved_lazily(simple_domain: Domain) -> None:
    output = init.generate(simple_domain)

    assert "if TYPE_CHECKING:" in output
    assert "__getattr__, __dir__ = lazy_exports(" in output
    assert '"Sample": (".domain", "Sample"),' in output
    assert '"GetNodeParams": (".commands", "GetNodeParams"),' in output
    assert '"NodeAddedEvent": (".events", "NodeAddedEvent"),' in output


def test_lazy_exports_follow_import_aliases() -> None:
    domain = Domain(
        domain="Animation",
        types=[TypeDefinition(id="Animation", type="object")],
    )

    output = init.generate(domain)

    assert '"AnimationType": (".types", "Animation"),' in output
    assert '"Animation": (".domain", "Animation"),' in output


def test_root_init_resolves_domains_lazily() -> None:
    output = init.generate_root([Domain(domain="Page"), Domain(domain="DOMStorage")])

    assert "from .accessors import DomainAccessors" in output
    assert "    from .page import Page" in output
    assert '"Page": (".page", "Page"),' in output
    assert '"DOMStorage": (".domstorage", "DOMStorage"),' in output
