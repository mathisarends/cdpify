from pydantic_cpd.generator.models import Domain, Event, Parameter
from pydantic_cpd.generator.type_mapper import (
    map_cdp_type,
    to_pascal_case,
    to_snake_case,
)

from .utils import format_docstring


class EventsGenerator:
    def __init__(self):
        self.cross_domain_refs: set[str] = set()
        self.uses_any: bool = False
        self.uses_literal: bool = False

    def generate(self, domain: Domain) -> str:
        self.cross_domain_refs.clear()
        self.uses_any = False
        self.uses_literal = False

        event_models = self._generate_event_models(domain)

        sections = [
            self._header(domain),
            self._imports(bool(event_models)),
        ]

        if self.cross_domain_refs:
            sections.append(self._cross_domain_imports())

        sections.append(event_models if event_models else "# No events defined")

        return "\n\n".join(sections)

    def _header(self, domain: Domain) -> str:
        return '"""Generated event models from CDP specification"""'

    def _imports(self, has_models: bool) -> str:
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

        if has_models:
            lines.append("")
            lines.append("from .types import *")

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

    def _generate_event_models(self, domain: Domain) -> str:
        if not domain.events:
            return ""

        return "\n\n".join(self._create_event_model(event) for event in domain.events)

    def _create_event_model(self, event: Event) -> str:
        class_name = f"{to_pascal_case(event.name)}Event"

        lines = [f"class {class_name}(CDPModel):"]

        if event.description:
            doc = format_docstring(event.description, indent=4)
            lines.extend(doc.rstrip().splitlines())

        if event.parameters:
            for param in event.parameters:
                lines.append(f"    {self._create_field(param)}")
        else:
            lines.append("    pass")

        return "\n".join(lines)

    def _create_field(self, param: Parameter) -> str:
        field_name = to_snake_case(param.name)
        py_type = self._resolve_type(param)

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
