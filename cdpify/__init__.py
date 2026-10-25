from .client import Client
from .codec import decode_cdp, encode_cdp
from .events import ReceivedEvent
from .exceptions import (
    CDPCommandError,
    CDPConnectionError,
    CDPError,
    CDPTimeoutError,
    deprecated_exception,
)
from .executor import CommandExecutor
from .session import CDPSession
from .transport import Transport, TransportEvent

__all__ = [
    "Client",
    "CDPSession",
    "CommandExecutor",
    "ReceivedEvent",
    "decode_cdp",
    "encode_cdp",
    "Transport",
    "TransportEvent",
    "CDPError",
    "CDPConnectionError",
    "CDPCommandError",
    "CDPTimeoutError",
]


def __getattr__(name: str) -> type[CDPError]:
    replacement = deprecated_exception(name)
    if replacement is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return replacement
