from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FieldView:
    name: str
    annotation: str
    optional: bool = False
    cdp_name: str | None = None

    @property
    def needs_field(self) -> bool:
        """Whether the declaration needs ``field()`` to keep the CDP wire name."""
        return self.cdp_name is not None and self.cdp_name != self.name

    @property
    def declaration(self) -> str:
        annotation = f"{self.annotation} | None" if self.optional else self.annotation
        if not self.needs_field:
            default = " = None" if self.optional else ""
            return f"{self.name}: {annotation}{default}"

        arguments = []
        if self.optional:
            arguments.append("default=None")
        arguments.append(f'metadata={{"cdp_name": "{self.cdp_name}"}}')
        declaration = f"{self.name}: {annotation}"
        if len(declaration) + len(" = field(") + 4 > 88:
            indented_arguments = ",\n        ".join(arguments)
            return (
                f"{declaration} = field(  # noqa: E501\n"
                f"        {indented_arguments},\n"
                "    )"
            )
        return f"{declaration} = field({', '.join(arguments)})"


@dataclass(frozen=True, slots=True)
class EnumMemberView:
    name: str
    value: str

    @property
    def assignment(self) -> str:
        return f'{self.name} = "{self.value}"'


@dataclass(frozen=True, slots=True)
class TypeDefinitionView:
    kind: str
    name: str
    docstring: str | None = None
    annotation: str | None = None
    fields: tuple[FieldView, ...] = ()


@dataclass(frozen=True, slots=True)
class ModelView:
    name: str
    docstring: str | None = None
    fields: tuple[FieldView, ...] = ()
    event_name: str | None = None


@dataclass(frozen=True, slots=True)
class MethodView:
    name: str
    parameters: tuple[FieldView, ...]
    return_type: str
    command_member: str
    docstring: str | None = None
    deprecated: bool = False
    params_model: str | None = None
    constructor_args: str = ""
    result_model: str | None = None


@dataclass(frozen=True, slots=True)
class DomainView:
    name: str
    module: str
    property_name: str

    @property
    def import_statement(self) -> str:
        return f"from .{self.module} import {self.name}"

    @property
    def export(self) -> str:
        return f'"{self.name}",'


@dataclass(frozen=True, slots=True)
class ImportBlockView:
    module: str
    names: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LazyExportView:
    name: str
    module: str
    attribute: str


def dataclass_import(models: Iterable[ModelView | TypeDefinitionView]) -> str:
    """Import ``field`` only when a generated declaration uses it."""
    uses_field = any(f.needs_field for model in models for f in model.fields)
    return f"from dataclasses import dataclass{', field' if uses_field else ''}"
