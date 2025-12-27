from pydantic_cpd.generator.models import Domain, Command, Parameter
from pydantic_cpd.generator.type_mapper import (
    map_cdp_type,
    to_snake_case,
    to_pascal_case,
)


class CommandsGenerator:
    def __init__(self):
        self.cross_domain_refs: set[str] = set()

    def generate(self, domain: Domain) -> str:
        self.cross_domain_refs.clear()

        command_models = self._generate_command_models(domain)

        sections = [
            self._header(domain),
            self._imports(bool(command_models)),
        ]

        if self.cross_domain_refs:
            sections.append(self._cross_domain_imports())

        sections.append(command_models if command_models else "# No commands defined")

        return "\n\n".join(sections)

    def _header(self, domain: Domain) -> str:
        return f'''"""Generated command models from CDP specification"""
# Domain: {domain.domain} Commands'''

    def _imports(self, has_models: bool) -> str:
        lines = [
            "from typing import Any, Literal",
            "from pydantic_cpd.cdp.base import CDPModel",
        ]

        if has_models:
            lines.append("")
            lines.append("from .types import *")

        return "\n".join(lines)

    def _cross_domain_imports(self) -> str:
        lines = []
        for ref in sorted(self.cross_domain_refs):
            domain_name = ref.split(".")[0].lower()
            lines.append(f"from pydantic_cpd.cdp import {domain_name}")
        return "\n".join(lines)

    def _generate_command_models(self, domain: Domain) -> str:
        if not domain.commands:
            return ""

        models = []
        for command in domain.commands:
            if command.parameters:
                models.append(self._create_params_model(command))
            if command.returns:
                models.append(self._create_returns_model(command))

        return "\n\n".join(models)

    def _create_params_model(self, command: Command) -> str:
        class_name = f"{to_pascal_case(command.name)}Params"

        lines = [f"class {class_name}(CDPModel):"]

        if command.description:
            lines.append(f'    """{command.description}"""')

        for param in command.parameters:
            lines.append(f"    {self._create_field(param)}")

        return "\n".join(lines)

    def _create_returns_model(self, command: Command) -> str:
        class_name = f"{to_pascal_case(command.name)}Result"

        lines = [f"class {class_name}(CDPModel):"]

        for param in command.returns:
            lines.append(f"    {self._create_field(param)}")

        return "\n".join(lines)

    def _create_field(self, param: Parameter) -> str:
        field_name = to_snake_case(param.name)
        py_type = self._resolve_type(param)

        if param.ref and "." in param.ref:
            self.cross_domain_refs.add(param.ref)

        return f"{field_name}: {py_type}" + (" = None" if param.optional else "")

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
