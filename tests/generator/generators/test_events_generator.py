from cdpify.generator.generators import events
from cdpify.generator.schemas import Domain, Event, Parameter, TypeDefinition


def test_renders_event_enum(simple_domain: Domain) -> None:
    output = events.generate(simple_domain)

    assert "class SampleEvent(StrEnum):" in output
    assert 'NODE_ADDED = "Sample.nodeAdded"' in output
    assert 'CLEARED = "Sample.cleared"' in output


def test_renders_event_models(simple_domain: Domain) -> None:
    output = events.generate(simple_domain)

    assert "@dataclass(kw_only=True, slots=True)" in output
    assert "cdpify.shared.models" not in output
    assert "class NodeAddedEvent:" in output
    assert 'node_id: NodeId = field(metadata={"cdp_name": "nodeId"})' in output
    assert (
        "parent_id: NodeId | None = field("
        'default=None, metadata={"cdp_name": "parentId"})'
    ) in output
    assert "cdp_session_id" not in output


def test_event_without_parameters_only_has_cdp_event_name(
    simple_domain: Domain,
) -> None:
    output = events.generate(simple_domain)

    cleared_section = output.split("class ClearedEvent:")[1].strip().splitlines()
    assert cleared_section == ['__cdp_event__: ClassVar[str] = "Sample.cleared"']


def test_event_models_declare_cdp_event_name(simple_domain: Domain) -> None:
    output = events.generate(simple_domain)

    assert "from typing import ClassVar" in output
    assert '__cdp_event__: ClassVar[str] = "Sample.nodeAdded"' in output


def test_includes_event_descriptions(simple_domain: Domain) -> None:
    output = events.generate(simple_domain)
    assert "Fired when a node is added." in output


def test_empty_domain_marker(empty_domain: Domain) -> None:
    output = events.generate(empty_domain)
    assert "# No events defined" in output


def test_aliases_local_type_when_name_collides_with_event_enum() -> None:
    """If a domain has a type whose name matches `{domain}Event`, the import
    must be aliased to avoid shadowing the event enum class."""
    domain = Domain(
        domain="Page",
        types=[
            TypeDefinition(id="PageEvent", type="string"),
        ],
        events=[
            Event(
                name="something",
                parameters=[Parameter(name="kind", ref="PageEvent")],
            )
        ],
    )

    output = events.generate(domain)

    assert "PageEvent as PageEventType" in output
    assert "kind: PageEventType" in output
    assert "class PageEvent(StrEnum):" in output


def test_cross_domain_ref_uses_runtime_import() -> None:
    domain = Domain(
        domain="Animation",
        events=[
            Event(
                name="started",
                parameters=[Parameter(name="target", ref="DOM.NodeId")],
            )
        ],
    )

    output = events.generate(domain)

    assert "from cdpify.domains import dom" in output
    assert "target: dom.NodeId" in output
    assert "if TYPE_CHECKING:" not in output
    assert "TYPE_CHECKING" not in output
    assert "from __future__ import annotations" in output


def test_optional_override_for_request_will_be_sent() -> None:
    domain = Domain(
        domain="Network",
        events=[
            Event(
                name="requestWillBeSent",
                parameters=[
                    Parameter(name="documentURL", type="string"),
                    Parameter(name="requestId", type="string"),
                ],
            )
        ],
    )

    output = events.generate(domain)

    assert (
        "document_url: str | None = field("
        'default=None, metadata={"cdp_name": "documentURL"})'
    ) in output
    assert 'request_id: str = field(metadata={"cdp_name": "requestId"})' in output
