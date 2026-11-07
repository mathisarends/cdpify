from dataclasses import dataclass, field
from typing import Any

import pytest

from cdpify import UNSET, CDPDecodeError, UnsetType
from cdpify import decode_cdp as public_decode_cdp
from cdpify import encode_cdp as public_encode_cdp
from cdpify.codec import _compile_model, decode_cdp, encode_cdp


@dataclass
class _Child:
    child_value: int = field(metadata={"cdp_name": "childValue"})


@dataclass
class _Parent:
    child: _Child | None = field(metadata={"cdp_name": "child"})
    values: list[int] | None = field(
        default=None,
        metadata={"cdp_name": "values"},
    )


@dataclass
class _StringHintsModel:
    value: "int" = field(metadata={"cdp_name": "value"})
    known: "int" = field(metadata={"cdp_name": "known"})


def test_codec_is_available_from_the_public_package() -> None:
    assert public_decode_cdp is decode_cdp
    assert public_encode_cdp is encode_cdp


def test_deserializes_nested_models_and_optional_lists() -> None:
    model = decode_cdp(
        _Parent,
        {"child": {"childValue": 3}, "values": [1, 2, 3]},
    )

    assert model.child is not None
    assert model.child.child_value == 3
    assert model.values == [1, 2, 3]


def test_serializes_nested_models_with_their_own_aliases() -> None:
    model = _Parent(child=_Child(child_value=3), values=[1, 2, 3])

    assert encode_cdp(model) == {
        "child": {"childValue": 3},
        "values": [1, 2, 3],
    }


def test_construct_handles_missing_required_fields_with_none(caplog) -> None:
    model = decode_cdp(_Parent, {}, strict=False)

    assert model.child is None
    assert "CDP spec mismatch for _Parent" in caplog.text


def test_missing_required_fields_raise_structured_decode_error() -> None:
    with pytest.raises(CDPDecodeError) as error:
        decode_cdp(_Parent, {})
    assert error.value.model_type is _Parent
    assert error.value.missing_fields == ("child",)


def test_strictness_propagates_to_nested_models_and_does_not_leak() -> None:
    assert decode_cdp(_Parent, {"child": {}}, strict=False).child.child_value is None
    with pytest.raises(CDPDecodeError) as error:
        decode_cdp(_Parent, {"child": {}})
    assert error.value.path == ("child",)
    assert error.value.missing_fields == ("child_value",)


def test_any_preserves_null_and_unset_omits_the_field() -> None:
    from cdpify.domains.runtime import CallArgument

    assert encode_cdp(CallArgument()) == {}
    assert encode_cdp(CallArgument(value=None)) == {"value": None}
    assert decode_cdp(CallArgument, {}).value is UNSET
    assert decode_cdp(CallArgument, {"value": None}).value is None


def test_required_any_accepts_explicit_null() -> None:
    @dataclass
    class Required:
        value: Any

    assert encode_cdp(Required(value=None)) == {"value": None}
    assert decode_cdp(Required, {"value": None}).value is None
    with pytest.raises(CDPDecodeError):
        decode_cdp(Required, {})


def test_unset_survives_copy_and_pickle() -> None:
    import copy
    import pickle

    assert isinstance(UNSET, UnsetType)
    assert copy.deepcopy(UNSET) is UNSET
    assert pickle.loads(pickle.dumps(UNSET)) is UNSET


def test_ignores_unknown_wire_fields() -> None:
    model = decode_cdp(
        _Parent,
        {"child": {"childValue": 3}, "futureField": True},
    )

    assert model.child == _Child(child_value=3)


def test_model_plan_is_cached_per_type() -> None:
    _compile_model.cache_clear()

    decode_cdp(_Parent, {"child": {"childValue": 1}})
    first = _compile_model.cache_info()
    decode_cdp(_Parent, {"child": {"childValue": 2}})
    second = _compile_model.cache_info()

    assert second.misses == first.misses
    assert second.hits > first.hits


def test_deserialization_falls_back_when_get_type_hints_fails(monkeypatch) -> None:
    def _raise_type_hints(_: type) -> dict[str, Any]:
        raise RuntimeError("boom")

    _compile_model.cache_clear()
    monkeypatch.setattr("cdpify.codec.get_type_hints", _raise_type_hints)

    model = decode_cdp(_StringHintsModel, {"value": 1, "known": 2})

    assert model.value == 1
    assert model.known == 2


def test_deserialization_keeps_raw_values_when_annotations_cannot_resolve(
    monkeypatch,
) -> None:
    def _raise_type_hints(_: type) -> dict[str, Any]:
        raise RuntimeError("boom")

    def _raise_eval(_: str, __: dict[str, Any]) -> Any:
        raise NameError("unknown")

    _compile_model.cache_clear()
    monkeypatch.setattr("cdpify.codec.get_type_hints", _raise_type_hints)
    monkeypatch.setattr("builtins.eval", _raise_eval)

    model = decode_cdp(_StringHintsModel, {"value": 1, "known": 2})

    assert model.value == 1
    assert model.known == 2


def test_rejects_non_dataclass_types() -> None:
    with pytest.raises(TypeError, match="Expected a dataclass type"):
        decode_cdp(dict, {})


type _ChildList = list[_Child]


@dataclass
class _Container:
    aliased: _ChildList = field(metadata={"cdp_name": "aliased"})
    by_key: dict[str, _Child] | None = field(
        default=None, metadata={"cdp_name": "byKey"}
    )


@dataclass
class _Recursive:
    name: str
    parent: "_Recursive | None" = None


def test_decodes_models_behind_type_alias_statements() -> None:
    model = decode_cdp(_Container, {"aliased": [{"childValue": 1}, None]})

    assert model.aliased == [_Child(child_value=1), None]


def test_decodes_dict_values_into_models() -> None:
    model = decode_cdp(_Container, {"aliased": [], "byKey": {"a": {"childValue": 2}}})

    assert model.by_key == {"a": _Child(child_value=2)}


def test_decodes_recursive_models() -> None:
    model = decode_cdp(_Recursive, {"name": "a", "parent": {"name": "b"}})

    assert model == _Recursive(name="a", parent=_Recursive(name="b"))


def test_primitive_fields_need_no_decoder() -> None:
    plan = _compile_model(_Parent)

    decoders = {field_plan.name: field_plan.decoder for field_plan in plan.fields}
    assert decoders["values"] is None
    assert decoders["child"] is not None


@dataclass
class _UnresolvableHint:
    value: "DoesNotExist" = field(metadata={"cdp_name": "value"})  # noqa: F821


def test_warns_when_a_field_type_cannot_be_resolved(
    caplog: pytest.LogCaptureFixture,
) -> None:
    model = decode_cdp(_UnresolvableHint, {"value": {"raw": True}})

    assert model.value == {"raw": True}
    assert "Cannot resolve type 'DoesNotExist' of _UnresolvableHint.value" in (
        caplog.text
    )
