"""Runtime behavior shared by generated CDP models and events."""

import importlib
import pkgutil
from dataclasses import dataclass, field, is_dataclass

import pytest

from cdpify import domains
from cdpify.codec import _compile_model, decode_cdp, encode_cdp
from cdpify.domains.accessibility import AXNode
from cdpify.domains.dom.commands import GetOuterHTMLParams
from cdpify.domains.page.events import LifecycleEventEvent


@dataclass(kw_only=True, slots=True)
class _Sample:
    value: int = field(metadata={"cdp_name": "value"})


class TestGeneratedModels:
    def test_command_models_do_not_carry_session_metadata(self) -> None:
        params = GetOuterHTMLParams(backend_node_id=7)

        assert not hasattr(params, "cdp_session_id")

    def test_event_models_do_not_carry_session_metadata(self) -> None:
        event = decode_cdp(
            LifecycleEventEvent,
            {
                "frameId": "F1",
                "loaderId": "L1",
                "name": "networkIdle",
                "timestamp": 12.5,
            },
        )

        assert event.name == "networkIdle"
        assert not hasattr(event, "cdp_session_id")

    def test_models_are_mutable_and_slotted(self) -> None:
        model = _Sample(value=1)

        assert not hasattr(model, "__dict__")
        model.value = 2
        assert model.value == 2


class TestAcronymFieldNames:
    """Field names come from the generator's snake case; from_cdp has to use
    the same one. A mismatch is silent — the field just stays None."""

    def test_fills_field_behind_an_acronym_wire_key(self) -> None:
        node = decode_cdp(
            AXNode, {"nodeId": "1", "ignored": False, "backendDOMNodeId": 42}
        )
        assert node.backend_dom_node_id == 42

    def test_round_trips_acronym_field_back_to_the_wire_name(self) -> None:
        params = GetOuterHTMLParams(backend_node_id=7, include_shadow_dom=True)
        assert encode_cdp(params) == {
            "backendNodeId": 7,
            "includeShadowDOM": True,
        }


def _generated_models() -> list[type]:
    models = []
    for module_info in pkgutil.walk_packages(domains.__path__, "cdpify.domains."):
        module = importlib.import_module(module_info.name)
        models.extend(
            value
            for value in vars(module).values()
            if isinstance(value, type)
            and is_dataclass(value)
            and value.__module__ == module.__name__
        )
    return models


def test_every_generated_model_has_resolvable_field_types(
    caplog: pytest.LogCaptureFixture,
) -> None:
    models = _generated_models()

    for model in models:
        _compile_model(model)

    assert len(models) > 1000
    assert "Cannot resolve type" not in caplog.text
