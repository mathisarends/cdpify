import importlib
from collections.abc import Callable, Mapping
from typing import Any

LazyExports = Mapping[str, tuple[str, str]]


def lazy_exports(
    package: str,
    exports: LazyExports,
) -> tuple[Callable[[str], Any], Callable[[], list[str]]]:
    """Build PEP 562 ``__getattr__``/``__dir__`` hooks for a package.

    ``exports`` maps each public name to ``(relative_module, attribute)``. The
    submodule is imported on first access and the value is cached in the
    package namespace, so later lookups bypass ``__getattr__`` entirely.
    """
    namespace = importlib.import_module(package).__dict__

    def __getattr__(name: str) -> Any:
        try:
            module_name, attribute = exports[name]
        except KeyError:
            raise AttributeError(
                f"module {package!r} has no attribute {name!r}"
            ) from None

        value = getattr(importlib.import_module(module_name, package), attribute)
        namespace[name] = value
        return value

    def __dir__() -> list[str]:
        return sorted({*namespace, *exports})

    return __getattr__, __dir__
