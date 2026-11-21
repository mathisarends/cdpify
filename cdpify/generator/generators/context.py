import re

from cdpify.generator.schemas import Parameter
from cdpify.shared.naming import to_snake_case

_CROSS_DOMAIN_PATTERN = re.compile(r"\b([a-z][a-z0-9_]*)\.([A-Z][a-zA-Z0-9]*)\b")


class GenerationContext:
    """Tracks imports and type references discovered while generating one file.

    A fresh context is created per `generate()` call, so generators stay
    effectively stateless across domains.
    """

    def __init__(self) -> None:
        self._cross_domain_refs: set[str] = set()
        self._local_type_refs: set[str] = set()
        self._typing_names: set[str] = set()

    def track_type_string(self, type_str: str) -> None:
        if "Any" in type_str:
            self.use_typing("Any")
        if "Literal" in type_str:
            self.use_typing("Literal")
        for domain, type_name in _CROSS_DOMAIN_PATTERN.findall(type_str):
            self._cross_domain_refs.add(f"{domain}.{type_name}")

    def use_typing(self, name: str) -> None:
        self._typing_names.add(name)

    def scan_param(self, param: Parameter) -> None:
        self.scan_ref(param.ref)
        if param.type == "array" and param.items:
            self.scan_ref(param.items.get("$ref"))

    def references_local_type(self, name: str) -> bool:
        return name in self._local_type_refs

    def scan_ref(self, ref: str | None) -> None:
        if not ref:
            return
        if "." in ref:
            self._cross_domain_refs.add(ref)
        else:
            self._local_type_refs.add(ref)

    @property
    def sorted_typing_names(self) -> tuple[str, ...]:
        return tuple(sorted(self._typing_names))

    def local_import_names(
        self, aliases: dict[str, str] | None = None
    ) -> tuple[str, ...]:
        aliases = aliases or {}
        names = []
        for name in sorted(self._local_type_refs):
            alias = aliases.get(name)
            names.append(f"{name} as {alias}" if alias else name)
        return tuple(names)

    @property
    def cross_domain_modules(self) -> tuple[str, ...]:
        modules = {
            to_snake_case(ref.split(".", 1)[0]) for ref in self._cross_domain_refs
        }
        return tuple(sorted(modules))
