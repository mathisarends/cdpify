import json
import pickle
from copy import deepcopy
from dataclasses import dataclass
from enum import StrEnum

import pytest

from cdpify.codec import decode_cdp, encode_cdp
from cdpify.shared.enums import CDPStrEnum


class _Reason(CDPStrEnum):
    KNOWN = "known"
    EMPTY = ""


class _StrictReason(StrEnum):
    KNOWN = "known"


type _Reasons = list[_Reason]


@dataclass
class _EnumFields:
    reason: _Reason
    optional: _Reason | None
    reasons: _Reasons
    by_key: dict[str, _Reason]


@dataclass
class _Nested:
    fields: _EnumFields


def test_known_values_return_canonical_members() -> None:
    assert _Reason("known") is _Reason.KNOWN
    assert _Reason("") is _Reason.EMPTY
    assert issubclass(_Reason, StrEnum)


def test_unknown_strings_remain_enum_members_without_growing_member_maps() -> None:
    members = dict(_Reason.__members__)
    unknown = _Reason("future-value")

    assert isinstance(unknown, _Reason)
    assert unknown.value == "future-value"
    assert str(unknown) == "future-value"
    assert unknown == "future-value"
    assert _Reason.__members__ == members
    assert list(_Reason) == [_Reason.KNOWN, _Reason.EMPTY]
    assert _Reason("future-value") is not unknown


@pytest.mark.parametrize("value", [None, 1, b"known"])
def test_unknown_non_strings_are_rejected(value: object) -> None:
    with pytest.raises(ValueError):
        _Reason(value)


def test_unknown_values_survive_copying_and_pickling() -> None:
    unknown = _Reason("future-value")

    for restored in (deepcopy(unknown), pickle.loads(pickle.dumps(unknown))):
        assert isinstance(restored, _Reason)
        assert restored.value == unknown.value


def test_decodes_enums_in_nested_models_aliases_lists_and_dicts() -> None:
    payload = {
        "fields": {
            "reason": "known",
            "optional": "",
            "reasons": ["known", "future-value"],
            "by_key": {"a": "known", "b": "future-value"},
        }
    }

    model = decode_cdp(_Nested, payload)

    assert model.fields.reason is _Reason.KNOWN
    assert model.fields.optional is _Reason.EMPTY
    assert model.fields.reasons[0] is _Reason.KNOWN
    assert isinstance(model.fields.reasons[1], _Reason)
    assert model.fields.reasons[1].value == "future-value"
    assert model.fields.by_key["a"] is _Reason.KNOWN
    assert isinstance(model.fields.by_key["b"], _Reason)
    assert json.loads(json.dumps(encode_cdp(model))) == payload


def test_optional_enum_can_be_missing_or_null() -> None:
    @dataclass
    class OptionalEnum:
        reason: _Reason | None = None

    assert decode_cdp(OptionalEnum, {}).reason is None
    assert decode_cdp(OptionalEnum, {"reason": None}).reason is None


def test_codec_also_supports_standard_str_enums() -> None:
    @dataclass
    class StrictEnum:
        reason: _StrictReason

    assert decode_cdp(StrictEnum, {"reason": "known"}).reason is _StrictReason.KNOWN
    with pytest.raises(ValueError):
        decode_cdp(StrictEnum, {"reason": "future-value"})


def test_orjson_encodes_known_and_unknown_enum_values() -> None:
    orjson = pytest.importorskip("orjson")

    payload = [_Reason.KNOWN, _Reason("future-value")]

    assert orjson.loads(orjson.dumps(payload)) == ["known", "future-value"]
