from pathlib import Path
import subprocess
import textwrap

from pydantic_cpd.generator.models import Domain, Command, Parameter, TypeDefinition
from pydantic_cpd.generator.type_mapper import map_cdp_type, to_snake_case

_DOMAINS_DIR = Path(__file__).parent.parent / "domains"

_IMPORTS_TEMPLATE = '''"""Generated from CDP specification"""
from pydantic_cpd.domains.base import CDPModel
from typing import Literal, Any
'''

_BASE_FILE_TEMPLATE = '''"""Generated CDP base models"""
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CDPModel(BaseModel):
    """Base model for CDP with automatic camelCase alias generation."""
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
'''


def _extract_referenced_domains(domain: Domain) -> set[str]:
    """Extract all external domain references from types and commands."""
    referenced = set()

    def check_type(type_str: str) -> None:
        type_str = type_str.replace("list[", "").replace("dict[", "").replace("]", "")
        if "." in type_str:
            domain_name = type_str.split(".")[0].strip()
            if domain_name and domain_name[0].isupper():
                referenced.add(domain_name)

    if domain.types:
        for type_def in domain.types:
            if type_def.properties:
                for prop in type_def.properties:
                    type_str = map_cdp_type(prop)
                    check_type(type_str)
                    if prop.ref:
                        check_type(prop.ref)

    for command in domain.commands:
        if command.parameters:
            for param in command.parameters:
                type_str = map_cdp_type(param)
                check_type(type_str)
                if param.ref:
                    check_type(param.ref)
        if command.returns:
            for ret in command.returns:
                type_str = map_cdp_type(ret)
                check_type(type_str)
                if ret.ref:
                    check_type(ret.ref)

    return referenced


def _generate_imports(domain: Domain) -> str:
    code = _IMPORTS_TEMPLATE

    referenced_domains = _extract_referenced_domains(domain)
    if referenced_domains:
        code += "\n"
        for domain_name in sorted(referenced_domains):
            code += f"from pydantic_cpd.domains import {domain_name.lower()}\n"
        code += "\n# Alias for cross-domain type references\n"
        for domain_name in sorted(referenced_domains):
            code += f"{domain_name} = {domain_name.lower()}\n"
        code += "\n"

    return code


def _create_enum_type_alias(type_def: TypeDefinition) -> str:
    enum_values = ", ".join(f'"{v}"' for v in type_def.enum)
    return f"{type_def.id} = Literal[{enum_values}]\n"


def _format_docstring(description: str, indent: str = "    ") -> str:
    """Format docstring - single-line if short, multi-line if long."""
    max_width = 88 - len(indent) - 6

    if len(description) <= max_width and "\n" not in description:
        return f'{indent}"""{description}"""'

    wrapped = textwrap.fill(description, width=88 - len(indent))
    lines = wrapped.split("\n")

    result = [f'{indent}"""']
    for line in lines:
        result.append(f"{indent}{line}")
    result.append(f'{indent}"""')

    return "\n".join(result)


def _create_object_model(type_def: TypeDefinition) -> str:
    lines = [f"class {type_def.id}(CDPModel):"]

    if type_def.description:
        lines.append(_format_docstring(type_def.description))

    for prop in type_def.properties:
        py_type = map_cdp_type(prop)
        field_name = to_snake_case(prop.name)
        default = " = None" if prop.optional else ""
        lines.append(f"    {field_name}: {py_type}{default}")

    return "\n".join(lines) + "\n\n"


def _create_simple_type_alias(type_def: TypeDefinition) -> str:
    py_type = map_cdp_type(Parameter(name=type_def.id, type=type_def.type))
    return f"{type_def.id} = {py_type}\n"


def _generate_type_definitions(domain: Domain) -> str:
    if not domain.types:
        return ""

    code = ""
    for type_def in domain.types:
        if type_def.enum:
            code += _create_enum_type_alias(type_def)
        elif type_def.properties:
            code += _create_object_model(type_def)
        else:
            code += _create_simple_type_alias(type_def)

    return code


def _create_pydantic_field(param: Parameter, py_type: str, field_name: str) -> str:
    default = " = None" if param.optional else ""
    return f"    {field_name}: {py_type}{default}"


def _create_pydantic_model(
    class_name: str, description: str | None, parameters: list[Parameter]
) -> str:
    lines = [f"class {class_name}(CDPModel):"]

    if description:
        lines.append(_format_docstring(description))

    for param in parameters:
        py_type = map_cdp_type(param)
        field_name = to_snake_case(param.name)
        lines.append(_create_pydantic_field(param, py_type, field_name))

    return "\n".join(lines) + "\n\n"


def _generate_command_params(command: Command) -> str:
    if not command.parameters:
        return ""

    class_name = f"{command.name.capitalize()}Params"
    return _create_pydantic_model(class_name, command.description, command.parameters)


def _generate_command_result(command: Command) -> str:
    if not command.returns:
        return ""

    class_name = f"{command.name.capitalize()}Result"
    return _create_pydantic_model(class_name, None, command.returns)


def _generate_command_models(commands: list[Command]) -> str:
    if not commands:
        return ""

    code = ""
    for command in commands:
        code += _generate_command_params(command)
        code += _generate_command_result(command)

    return code


def _build_method_parameters(command: Command) -> str:
    required_params = []
    optional_params = []

    for param in command.parameters:
        py_type = map_cdp_type(param)
        field_name = to_snake_case(param.name)

        if param.optional:
            optional_params.append(f"{field_name}: {py_type} = None")
        else:
            required_params.append(f"{field_name}: {py_type}")

    all_params = required_params + optional_params
    return ", ".join(all_params)


def _get_method_return_type(command: Command) -> str:
    if command.returns:
        return f"{command.name.capitalize()}Result"
    return "None"


def _build_params_initialization(command: Command) -> str:
    if not command.parameters:
        return "{}"

    lines = [f"        params = {command.name.capitalize()}Params("]
    for param in command.parameters:
        field_name = to_snake_case(param.name)
        lines.append(f"            {field_name}={field_name},")
    lines.append("        )")
    return "\n".join(lines)


def _build_method_call(domain: Domain, command: Command) -> str:
    method_path = f"{domain.domain}.{command.name}"
    if command.parameters:
        params_dict = "params.model_dump(by_alias=True, exclude_none=True)"
    else:
        params_dict = "{}"
    return f'        result = await self._cdp.call("{method_path}", {params_dict})'


def _build_return_statement(command: Command) -> str:
    if command.returns:
        result_class = f"{command.name.capitalize()}Result"
        return f"        return {result_class}(**result)"
    return "        return None"


def _generate_client_method(domain: Domain, command: Command) -> str:
    method_name = to_snake_case(command.name)
    params_str = _build_method_parameters(command)
    return_type = _get_method_return_type(command)

    lines = []
    signature_params = f", {params_str}" if params_str else ""
    lines.append(
        f"    async def {method_name}(self{signature_params}) -> {return_type}:"
    )

    if command.description:
        lines.append(_format_docstring(command.description, indent="        "))

    if command.parameters:
        lines.append(_build_params_initialization(command))

    lines.append(_build_method_call(domain, command))
    lines.append(_build_return_statement(command))

    return "\n".join(lines) + "\n"


def _generate_client_class(domain: Domain) -> str:
    description = domain.description or f"{domain.domain} domain client"

    lines = [
        f"class {domain.domain}Client:",
        _format_docstring(description),
        "    def __init__(self, cdp_client: Any) -> None:",
        "        self._cdp = cdp_client",
    ]

    code = "\n".join(lines) + "\n"

    for command in domain.commands:
        code += _generate_client_method(domain, command)

    return code


def _should_skip_blank_line(lines: list[str], index: int) -> bool:
    """Check if the line after current index is a blank line that should be removed."""
    if index + 2 >= len(lines):
        return False

    current = lines[index].strip()
    next_line = lines[index + 1].strip()
    line_after_next = lines[index + 2]

    if next_line != "":
        return False

    if ":" not in line_after_next:
        return False

    is_single_line_docstring = current.startswith('"""') and current.endswith('"""')
    is_multi_line_docstring_end = current.endswith('"""') and not current.startswith(
        '"""'
    )

    return is_single_line_docstring or is_multi_line_docstring_end


def _remove_blank_lines_after_docstrings(file_path: Path) -> None:
    """Remove blank lines between class docstrings and their first attribute."""
    content = file_path.read_text()
    lines = content.split("\n")
    cleaned_lines = []

    i = 0
    while i < len(lines):
        current_line = lines[i]
        cleaned_lines.append(current_line)

        if _should_skip_blank_line(lines, i):
            i += 1

        i += 1

    file_path.write_text("\n".join(cleaned_lines))


def _format_file(file_path: Path) -> None:
    """Format generated file using ruff and clean up blank lines."""
    try:
        subprocess.run(
            ["ruff", "format", str(file_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        _remove_blank_lines_after_docstrings(file_path)

    except subprocess.CalledProcessError as e:
        print(f"  ⚠ Warning: Could not format {file_path.name}")
        print(f"    Error: {e.stderr}")
    except FileNotFoundError:
        print("  ⚠ Warning: ruff not found, skipping formatting")


def _generate_base_file() -> None:
    """Generate the base.py file with CDPModel."""
    base_path = _DOMAINS_DIR / "base.py"
    base_path.write_text(_BASE_FILE_TEMPLATE)
    _format_file(base_path)
    print("  ✓ Generated base.py")


def _generate_domain(domain: Domain) -> None:
    sections = []
    sections.append(_generate_imports(domain))

    types_code = _generate_type_definitions(domain)
    if types_code:
        sections.append(types_code)

    models_code = _generate_command_models(domain.commands)
    if models_code:
        sections.append(models_code)

    sections.append(_generate_client_class(domain))

    code = "\n".join(sections)
    output_path = _DOMAINS_DIR / f"{domain.domain.lower()}.py"
    output_path.write_text(code)
    _format_file(output_path)

    print(f"  ✓ Generated {output_path.name}")


def _create_domain_imports(domains: list[Domain]) -> str:
    imports = [
        f"from pydantic_cpd.domains.{d.domain.lower()} import {d.domain}Client"
        for d in domains
    ]
    return "\n".join(imports)


def _create_all_exports(domains: list[Domain]) -> str:
    exports = [f'"{d.domain}Client"' for d in domains]
    return "__all__ = [" + ", ".join(exports) + "]"


def _generate_init_file(domains: list[Domain]) -> None:
    sections = [
        '"""Generated CDP domains"""',
        "",
        _create_domain_imports(domains),
        "",
        _create_all_exports(domains),
        "",
    ]

    code = "\n".join(sections)
    init_path = _DOMAINS_DIR / "__init__.py"
    init_path.write_text(code)
    _format_file(init_path)

    print("  ✓ Generated __init__.py")


def generate_all_domains(domains: list[Domain]) -> None:
    _DOMAINS_DIR.mkdir(exist_ok=True)
    print("\n📝 Generating domain modules...")

    _generate_base_file()

    for domain in domains:
        _generate_domain(domain)

    _generate_init_file(domains)
