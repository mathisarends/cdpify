import functools
import inspect
import sys
import warnings
from collections.abc import Callable
from typing import Any


class _Deprecated:
    """Minimal ``warnings.deprecated`` (PEP 702) for Python 3.12.

    Emits a ``DeprecationWarning`` each time the decorated function is called.
    Type checkers only flag usages on Python 3.13+, where the standard library
    version is used instead.
    """

    def __init__(
        self,
        message: str,
        /,
        *,
        category: type[Warning] | None = DeprecationWarning,
        stacklevel: int = 1,
    ) -> None:
        if not isinstance(message, str):
            raise TypeError(f"Expected a message string, not {type(message).__name__}")
        self.message = message
        self.category = category
        self.stacklevel = stacklevel

    def __call__[F: Callable[..., Any]](self, func: F) -> F:
        message, category, stacklevel = self.message, self.category, self.stacklevel
        if category is None:
            func.__deprecated__ = message  # type: ignore[attr-defined]
            return func

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(message, category, stacklevel=stacklevel + 1)
            return func(*args, **kwargs)

        if inspect.iscoroutinefunction(func):
            wrapper = inspect.markcoroutinefunction(wrapper)
        func.__deprecated__ = wrapper.__deprecated__ = message  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]


if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    deprecated = _Deprecated

__all__ = ["deprecated"]
