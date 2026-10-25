import logging
import sys
from collections.abc import Callable
from dataclasses import MISSING, dataclass, fields, is_dataclass
from enum import StrEnum
from functools import cache
from types import UnionType
from typing import Any, TypeAliasType, Union, get_args, get_origin, get_type_hints

logger = logging.getLogger(__name__)

_CDP_ENABLED_METADATA_KEY = "cdp"
_CDP_NAME_METADATA_KEY = "cdp_name"


# Converts a non-None wire value; ``None`` means the value is used as is.
_Decoder = Callable[[Any], Any] | None


@dataclass(frozen=True, slots=True)
class _FieldPlan:
    name: str
    cdp_name: str
    decoder: _Decoder
    init: bool
    required: bool
    wire_enabled: bool


@dataclass(frozen=True, slots=True)
class _ModelPlan:
    fields: tuple[_FieldPlan, ...]
    decodable_fields: dict[str, _FieldPlan]
    required_names: frozenset[str]


def encode_cdp(model: Any) -> dict[str, Any]:
    """Serialize a generated CDP dataclass to its wire representation."""
    plan = _compile_model(type(model))
    encoded: dict[str, Any] = {}

    for model_field in plan.fields:
        if not model_field.wire_enabled:
            continue

        value = getattr(model, model_field.name)
        if value is not None:
            encoded[model_field.cdp_name] = _encode_value(value)

    return encoded


def decode_cdp[T](
    model_type: type[T],
    data: dict[str, Any],
) -> T:
    """Construct a generated CDP dataclass from its wire representation."""
    plan = _compile_model(model_type)
    values: dict[str, Any] = {}

    for cdp_name, value in data.items():
        model_field = plan.decodable_fields.get(cdp_name)
        if model_field is None:
            continue
        if value is not None and model_field.decoder is not None:
            value = model_field.decoder(value)
        values[model_field.name] = value

    if not values.keys() >= plan.required_names:
        missing = [
            model_field.name
            for model_field in plan.fields
            if model_field.name in plan.required_names
            and model_field.name not in values
        ]
        logger.warning(
            "CDP spec mismatch for %s. Missing fields: %s. Data keys: %s",
            model_type.__name__,
            missing,
            list(data.keys()),
        )
        values.update(dict.fromkeys(missing))

    return model_type(**values)


@cache
def _compile_model(model_type: type) -> _ModelPlan:
    if not is_dataclass(model_type):
        raise TypeError(f"Expected a dataclass type, got {model_type!r}")

    resolved_types = _resolve_field_types(model_type)
    field_plans = tuple(
        _FieldPlan(
            name=model_field.name,
            cdp_name=model_field.metadata.get(_CDP_NAME_METADATA_KEY, model_field.name),
            decoder=_build_decoder(resolved_types.get(model_field.name, Any)),
            init=model_field.init,
            required=(
                model_field.default is MISSING
                and model_field.default_factory is MISSING
            ),
            wire_enabled=model_field.metadata.get(_CDP_ENABLED_METADATA_KEY, True),
        )
        for model_field in fields(model_type)
    )
    return _ModelPlan(
        fields=field_plans,
        decodable_fields={
            field_plan.cdp_name: field_plan
            for field_plan in field_plans
            if field_plan.wire_enabled and field_plan.init
        },
        required_names=frozenset(
            field_plan.name
            for field_plan in field_plans
            if field_plan.init and field_plan.required
        ),
    )


def _resolve_field_types(model_type: type) -> dict[str, Any]:
    try:
        return get_type_hints(model_type)
    except Exception:
        pass

    module = sys.modules.get(model_type.__module__)
    globalns = getattr(module, "__dict__", {}) if module else {}
    resolved: dict[str, Any] = {}

    for model_field in fields(model_type):
        annotation = model_type.__annotations__.get(model_field.name, model_field.type)
        if not isinstance(annotation, str):
            resolved[model_field.name] = annotation
            continue
        try:
            resolved[model_field.name] = eval(annotation, globalns)
        except Exception as error:
            logger.warning(
                "Cannot resolve type %r of %s.%s (%s); nested values stay raw",
                annotation,
                model_type.__qualname__,
                model_field.name,
                error,
            )
            resolved[model_field.name] = Any

    return resolved


def _encode_value(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return encode_cdp(value)
    if isinstance(value, (list, tuple)):
        return [_encode_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _encode_value(item) for key, item in value.items()}
    return value


def _build_decoder(field_type: Any) -> _Decoder:
    """Build a converter for one annotation once, instead of per value."""
    if field_type is Any:
        return None
    if isinstance(field_type, TypeAliasType):
        return _build_decoder(field_type.__value__)

    origin = get_origin(field_type)
    args = get_args(field_type)

    if origin in (Union, UnionType):
        candidates = [arg for arg in args if arg is not type(None)]
        if len(candidates) == 1:
            return _build_decoder(candidates[0])
        model_type = next(filter(_is_dataclass_type, candidates), None)
        return None if model_type is None else _model_decoder(model_type)

    if origin is list and args:
        item_decoder = _build_decoder(args[0])
        if item_decoder is None:
            return None
        return lambda value: [
            None if item is None else item_decoder(item) for item in value
        ]

    if origin is dict and len(args) == 2:
        item_decoder = _build_decoder(args[1])
        if item_decoder is None:
            return None
        return lambda value: {
            key: None if item is None else item_decoder(item)
            for key, item in value.items()
        }

    if _is_dataclass_type(field_type):
        return _model_decoder(field_type)

    if isinstance(field_type, type) and issubclass(field_type, StrEnum):
        return _enum_decoder(field_type)

    return None


class _EnumValues(dict[str, StrEnum]):
    """Resolve known values in dict's C path and construct unknowns on demand."""

    def __init__(self, enum_type: type[StrEnum]) -> None:
        super().__init__(
            (member.value, member) for member in enum_type.__members__.values()
        )
        self._enum_type = enum_type

    def __missing__(self, value: str) -> StrEnum:
        # Do not retain unknown browser values in this process-wide lookup.
        return self._enum_type(value)


@cache
def _enum_decoder(enum_type: type[StrEnum]) -> Callable[[str], StrEnum]:
    return _EnumValues(enum_type).__getitem__


def _model_decoder(model_type: type) -> Callable[[Any], Any]:
    # Resolved lazily so recursive models (e.g. a StackTrace parent) work.
    def decode(value: Any) -> Any:
        return decode_cdp(model_type, value) if isinstance(value, dict) else value

    return decode


def _is_dataclass_type(field_type: Any) -> bool:
    try:
        return isinstance(field_type, type) and is_dataclass(field_type)
    except TypeError:
        return False
