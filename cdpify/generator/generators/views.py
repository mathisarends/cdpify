from collections.abc import Iterable
from dataclasses import dataclass, replace

from cdpify.generator.generators.utils import api_description, format_docstring


@dataclass(frozen=True, slots=True)
class FieldView:
    name: str
    annotation: str
    optional: bool = False
    cdp_name: str | None = None
    encode_value: bool = False
    description: str | None = None
    experimental: bool = False
    deprecated: bool = False

    @property
    def docstring(self) -> str:
        description = api_description(
            self.description, experimental=self.experimental, deprecated=self.deprecated
        )
        if self.uses_unset:
            description += " Omit with UNSET; None encodes JSON null."
        return format_docstring(description.strip(), indent=4)

    @property
    def uses_unset(self) -> bool:
        return self.optional and self.annotation == "Any"

    @property
    def encoded_value(self) -> str:
        return f"_encode_value({self.name})" if self.encode_value else self.name

    @property
    def parameter_declaration(self) -> str:
        return replace(self, cdp_name=None).declaration

    @property
    def needs_field(self) -> bool:
        """Whether the declaration needs ``field()`` to keep the CDP wire name."""
        return self.cdp_name is not None and self.cdp_name != self.name

    @property
    def declaration(self) -> str:
        annotation = self.annotation
        default_value = "UNSET" if self.uses_unset else "None"
        if self.optional:
            annotation += " | UnsetType" if self.uses_unset else " | None"
        if not self.needs_field:
            default = f" = {default_value}" if self.optional else ""
            return f"{self.name}: {annotation}{default}"

        arguments = []
        if self.optional:
            arguments.append(f"default={default_value}")
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
    members: tuple[EnumMemberView, ...] = ()


@dataclass(frozen=True, slots=True)
class ModelView:
    name: str
    docstring: str | None = None
    fields: tuple[FieldView, ...] = ()
    event_member: str | None = None


@dataclass(frozen=True, slots=True)
class MethodView:
    name: str
    parameters: tuple[FieldView, ...]
    return_type: str
    command_member: str
    docstring: str | None = None
    deprecation: str | None = None
    params_model: str | None = None
    constructor_args: str = ""
    result_model: str | None = None

    @property
    def wire_params_name(self) -> str:
        name = "_params"
        names = {p.name for p in self.parameters}
        while name in names:
            name += "_"
        return name


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
