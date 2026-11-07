import warnings
from typing import Any, Self


class CDPError(Exception):
    """Base class for all cdpify errors."""


class CDPConnectionError(CDPError):
    """The connection to the browser could not be used or was closed."""


class CDPCommandError(CDPError):
    """The browser rejected a command."""

    def __init__(
        self,
        method: str,
        code: int,
        message: str,
        data: Any = None,
    ) -> None:
        self.method = method
        self.code = code
        self.message = message
        self.data = data
        detail = f"{method} failed with CDP error {code}: {message}"
        if data:
            detail = f"{detail} ({data})"
        super().__init__(detail)

    @classmethod
    def from_response(cls, method: str, error: dict[str, Any]) -> Self:
        return cls(
            method,
            code=error.get("code", -1),
            message=error.get("message", "Unknown error"),
            data=error.get("data"),
        )


class CDPTimeoutError(CDPError, TimeoutError):
    """A command did not receive a response in time."""


class CDPStreamClosedError(CDPError):
    """An event subscription ended before the next event arrived."""


class CDPDecodeError(CDPError):
    """A CDP payload is missing fields required by its generated model."""

    def __init__(
        self,
        model_type: type,
        missing_fields: tuple[str, ...],
        *,
        path: tuple[str, ...] = (),
    ) -> None:
        self.model_type = model_type
        self.missing_fields = missing_fields
        self.path = path
        location = ".".join(path) or "<root>"
        super().__init__(
            f"Cannot decode {model_type.__module__}.{model_type.__qualname__} "
            f"at {location}: missing required fields {', '.join(missing_fields)}"
        )

    def _prepend(self, name: str) -> "CDPDecodeError":
        return type(self)(self.model_type, self.missing_fields, path=(name, *self.path))


_DEPRECATED_NAMES = {
    "CDPException": CDPError,
    "CDPConnectionException": CDPConnectionError,
    "CDPCommandException": CDPCommandError,
    "CDPTimeoutException": CDPTimeoutError,
}


def deprecated_exception(name: str) -> type[CDPError] | None:
    """Return the replacement for a deprecated exception name, with a warning."""
    replacement = _DEPRECATED_NAMES.get(name)
    if replacement is not None:
        warnings.warn(
            f"{name} is deprecated, use {replacement.__name__} instead",
            DeprecationWarning,
            stacklevel=3,
        )
    return replacement


def __getattr__(name: str) -> type[CDPError]:
    replacement = deprecated_exception(name)
    if replacement is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return replacement
