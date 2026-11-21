"""Preserve protocol documentation in generated Python docstrings."""

import textwrap

from cdpify.generator.generators.names import to_identifier
from cdpify.generator.schemas import Command


def method_docstring(command: Command) -> str:
    """Preserve parameter descriptions and units in IDE method documentation."""
    description = api_description(
        command.description,
        experimental=command.experimental,
        deprecated=command.deprecated,
    )
    lines = format_docstring(description, indent=8).splitlines()
    documented = []
    for param in command.parameters:
        text = api_description(
            param.description,
            experimental=param.experimental,
            deprecated=param.deprecated,
        )
        if text:
            documented.append((param, _escape_docstring(text)))
    if not documented:
        return "\n".join(lines)
    if not lines:
        lines = ['        """', '        """']
    lines.pop()
    if description:
        lines.append("")
    lines.append("        Args:")
    for param, text in documented:
        prefix = f"            {to_identifier(param.name)}: "
        lines.extend(
            textwrap.wrap(
                text,
                width=88,
                initial_indent=prefix,
                subsequent_indent="                ",
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
    lines.append('        """')
    return "\n".join(lines)


def format_docstring(text: str, indent: int = 4) -> str:
    if not text:
        return ""

    indent_str = " " * indent
    max_length = 88 - indent

    words = _escape_docstring(text).split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1
        if current_length + word_length > max_length and current_line:
            lines.append(indent_str + " ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += word_length

    if current_line:
        lines.append(indent_str + " ".join(current_line))

    result = [f'{indent_str}"""']
    result.extend(lines)
    result.append(f'{indent_str}"""')

    return "\n".join(result)


def api_description(
    description: str | None, *, experimental: bool = False, deprecated: bool = False
) -> str:
    parts = [description] if description else []
    if experimental:
        parts.append("Experimental: this API may change or be removed.")
    if deprecated:
        parts.append("Deprecated in the Chrome DevTools Protocol.")
    return " ".join(parts)


def _escape_docstring(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
