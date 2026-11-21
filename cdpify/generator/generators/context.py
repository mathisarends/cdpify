import re
from dataclasses import dataclass, field

from cdpify.generator.schemas import Parameter
from cdpify.shared.naming import to_snake_case

_CROSS_DOMAIN_PATTERN = re.compile(r"\b([a-z][a-z0-9_]*)\.([A-Z][a-zA-Z0-9]*)\b")


@dataclass
class GenerationContext:
    """Tracks imports and type references discovered while generating one file.

    A fresh context is created per `generate()` call, so generators stay
    effectively stateless across domains.
    """

    cross_domain_refs: set[str] = field(default_factory=set)
    local_type_refs: set[str] = field(default_factory=set)
    typing_names: set[str] = field(default_factory=set)

    def use_typing(self, name: str) -> None:
        self.typing_names.add(name)

    def track_type_string(self, type_str: str) -> None:
        if "Any" in type_str:
            self.use_typing("Any")
        if "Literal" in type_str:
            self.use_typing("Literal")
        for domain, type_name in _CROSS_DOMAIN_PATTERN.findall(type_str):
            self.cross_domain_refs.add(f"{domain}.{type_name}")

    def scan_param(self, param: Parameter) -> None:
        self._add_ref(param.ref)
        if param.type == "array" and param.items:
            self._add_ref(param.items.get("$ref"))

    def _add_ref(self, ref: str | None) -> None:
        if not ref:
            return
        if "." in ref:
            self.cross_domain_refs.add(ref)
        else:
            self.local_type_refs.add(ref)

    @property
    def sorted_typing_names(self) -> tuple[str, ...]:
        return tuple(sorted(self.typing_names))

    def sorted_local_types(
        self, aliases: dict[str, str] | None = None
    ) -> tuple[tuple[str, str | None], ...]:
        aliases = aliases or {}
        return tuple((name, aliases.get(name)) for name in sorted(self.local_type_refs))

    @property
    def cross_domain_modules(self) -> tuple[str, ...]:
        return tuple(
            sorted({to_snake_case(ref.split(".")[0]) for ref in self.cross_domain_refs})
        )
