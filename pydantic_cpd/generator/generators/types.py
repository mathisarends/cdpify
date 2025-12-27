from pydantic_cpd.generator.models import Domain, Parameter, TypeDefinition
from pydantic_cpd.generator.type_mapper import map_cdp_type, to_snake_case

from .utils import format_docstring


class TypesGenerator:
    def __init__(self):
        self.cross_domain_refs: set[str] = set()
        self.uses_any: bool = False
        self.uses_literal: bool = False

    def generate(self, domain: Domain) -> str:
        self.cross_domain_refs.clear()
        self.uses_any = False
        self.uses_literal = False

        sections = [
            self._header(domain),
        ]

        # Erst alle Type Defs generieren (sammelt verwendete Types)
        type_defs = self._generate_type_definitions(domain)

        # Dann Imports basierend auf Verwendung
        sections.append(self._imports())

        # Dann cross-domain imports hinzufügen
        if self.cross_domain_refs:
            sections.append(self._cross_domain_imports())

        if type_defs:
            sections.append(type_defs)
        else:
            sections.append("# No types defined")

        return "\n\n".join(sections)

    def _header(self, domain: Domain) -> str:
        return '"""Generated from CDP specification"""'

    def _imports(self) -> str:
        typing_imports = []

        if self.uses_any:
            typing_imports.append("Any")
        if self.uses_literal:
            typing_imports.append("Literal")
        if self.cross_domain_refs:
            typing_imports.append("TYPE_CHECKING")

        lines = []
        if typing_imports:
            lines.append(f"from typing import {', '.join(typing_imports)}")

        lines.append("from pydantic_cpd.cdp.base import CDPModel")

        return "\n".join(lines)

    def _cross_domain_imports(self) -> str:
        # Dedupliziere domains
        unique_domains = set()
        for ref in self.cross_domain_refs:
            domain_name = ref.split(".")[0].lower()
            unique_domains.add(domain_name)

        if not unique_domains:
            return ""

        domains_list = ", ".join(sorted(unique_domains))
        return f"if TYPE_CHECKING:\n    from pydantic_cpd.cdp import {domains_list}"

    def _generate_type_definitions(self, domain: Domain) -> str:
        if not domain.types:
            return ""

        type_defs = []
        for type_def in domain.types:
            code = self._generate_single_type(type_def)
            if code:
                type_defs.append(code)

        return "\n\n".join(type_defs)

    def _generate_single_type(self, type_def: TypeDefinition) -> str:
        if type_def.enum:
            return self._create_enum_type(type_def)

        if type_def.properties:
            return self._create_object_model(type_def)

        return self._create_type_alias(type_def)

    def _create_enum_type(self, type_def: TypeDefinition) -> str:
        lines = []

        if type_def.description:
            # Module-level docstring for the enum/type alias
            lines.append(format_docstring(type_def.description, indent=0))

        values = ", ".join(f'"{v}"' for v in type_def.enum)
        literal_type = f"Literal[{values}]"

        # Track Literal usage
        self.uses_literal = True

        lines.append(f"{type_def.id} = {literal_type}")

        return "\n".join(lines)

    def _create_object_model(self, type_def: TypeDefinition) -> str:
        lines = [f"class {type_def.id}(CDPModel):"]

        if type_def.description:
            doc = format_docstring(type_def.description, indent=4)
            lines.extend(doc.rstrip().splitlines())

        for prop in type_def.properties:
            lines.append(f"    {self._create_field(prop)}")

        return "\n".join(lines)

    def _create_field(self, param: Parameter) -> str:
        field_name = to_snake_case(param.name)
        py_type = self._resolve_type(param)

        # Track cross-domain refs
        if param.ref and "." in param.ref:
            self.cross_domain_refs.add(param.ref)

        # Track type usage
        self._track_type_usage(py_type)

        return f"{field_name}: {py_type}" + (" = None" if param.optional else "")

    def _track_type_usage(self, type_str: str) -> None:
        """Track which typing imports are used"""
        if "Any" in type_str:
            self.uses_any = True
        if "Literal" in type_str:
            self.uses_literal = True

        # Track cross-domain refs
        import re

        pattern = r"\b([a-z]+)\.([A-Z][a-zA-Z0-9]*)\b"
        matches = re.findall(pattern, type_str)

        for domain, type_name in matches:
            ref = f"{domain}.{type_name}"
            self.cross_domain_refs.add(ref)

    def _resolve_type(self, param: Parameter) -> str:
        if param.ref and "." in param.ref:
            parts = param.ref.split(".")
            domain_lower = parts[0].lower()
            type_name = parts[1]
            base_type = f"{domain_lower}.{type_name}"
        else:
            base_type = map_cdp_type(param)

        if param.optional and " | None" not in base_type:
            return f"{base_type} | None"

        return base_type

    def _create_type_alias(self, type_def: TypeDefinition) -> str:
        lines = []

        if type_def.description:
            # Module-level docstring for the type alias
            lines.append(format_docstring(type_def.description, indent=0))

        py_type = map_cdp_type(
            Parameter(name=type_def.id, type=type_def.type, optional=False)
        )

        # Track type usage in type alias
        self._track_type_usage(py_type)

        lines.append(f"{type_def.id} = {py_type}")

        return "\n".join(lines)
