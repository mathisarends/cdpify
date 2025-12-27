from pydantic_cpd.generator.models import Command, Domain
from pydantic_cpd.generator.type_mapper import to_pascal_case, to_snake_case


class LibraryGenerator:
    def generate(self, domain: Domain) -> str:
        sections = [
            self._header(domain),
            self._imports(domain),
            self._client_class(domain),
        ]

        return "\n\n".join(sections)

    def _header(self, domain: Domain) -> str:
        return '"""Generated client library from CDP specification"""'

    def _imports(self, domain: Domain) -> str:
        lines = [
            "from __future__ import annotations",
            "",
            "from typing import TYPE_CHECKING, Any",
            "",
            "if TYPE_CHECKING:",
            "    from pydantic_cpd.client import CDPClient",
            "",
        ]

        if domain.commands:
            param_classes = {
                f"{to_pascal_case(cmd.name)}Params"
                for cmd in domain.commands
                if cmd.parameters
            }
            return_classes = {
                f"{to_pascal_case(cmd.name)}Result"
                for cmd in domain.commands
                if cmd.returns
            }

            all_classes = sorted(param_classes | return_classes)

            if all_classes:
                lines.append("from .commands import (")
                for cls in all_classes:
                    lines.append(f"    {cls},")
                lines.append(")")

        return "\n".join(lines)

    def _client_class(self, domain: Domain) -> str:
        class_name = f"{domain.domain}Client"

        lines = [f"class {class_name}:"]

        lines.append("    def __init__(self, client: CDPClient) -> None:")
        lines.append("        self._client = client")

        for command in domain.commands:
            lines.append("")
            lines.append(self._generate_method(command, domain.domain))

        return "\n".join(lines)

    def _generate_method(self, command: Command, domain_name: str) -> str:
        method_name = to_snake_case(command.name)
        cdp_method = f"{domain_name}.{command.name}"

        params = self._build_params(command)
        return_type = self._get_return_type(command)

        lines = [
            f"    async def {method_name}(",
            f"        {', '.join(params)}",
            f"    ) -> {return_type}:",
        ]

        if command.parameters:
            lines.extend(
                [
                    "        result = await self._client.send_raw(",
                    f'            method="{cdp_method}",',
                    "            params=params.to_cdp_params() if params else None,",
                    "            session_id=session_id,",
                    "        )",
                ]
            )
        else:
            lines.extend(
                [
                    "        result = await self._client.send_raw(",
                    f'            method="{cdp_method}",',
                    "            params=None,",
                    "            session_id=session_id,",
                    "        )",
                ]
            )

        if command.returns:
            result_class = f"{to_pascal_case(command.name)}Result"
            lines.append(f"        return {result_class}.model_validate(result)")
        else:
            lines.append("        return result")

        return "\n".join(lines)

    def _build_params(self, command: Command) -> list[str]:
        params = ["self"]

        if command.parameters:
            all_optional = all(p.optional for p in command.parameters)
            param_class = f"{to_pascal_case(command.name)}Params"

            if all_optional:
                params.append(f"params: {param_class} | None = None")
            else:
                params.append(f"params: {param_class}")

        params.append("session_id: str | None = None")
        return params

    def _get_return_type(self, command: Command) -> str:
        if command.returns:
            return f"{to_pascal_case(command.name)}Result"
        return "dict[str, Any]"
