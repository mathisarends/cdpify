from .client import CdpClient
from .codec import decode_cdp, encode_cdp
from .error import (
    CDPCommandError,
    CDPConnectionError,
    CDPDecodeError,
    CDPError,
    CDPEventOverflowError,
    CDPStreamClosedError,
    CDPTimeoutError,
    deprecated_exception,
)
from .event_queue import OverflowPolicy
from .events import EventSubscription, ReceivedEvent
from .executor import CommandExecutor
from .session import CdpSession
from .transport import Transport, TransportEvent
from .unset import UNSET, UnsetType

__all__ = [
    "CdpClient",
    "CdpSession",
    "CommandExecutor",
    "EventSubscription",
    "ReceivedEvent",
    "decode_cdp",
    "encode_cdp",
    "Transport",
    "TransportEvent",
    "CDPError",
    "CDPConnectionError",
    "CDPCommandError",
    "CDPTimeoutError",
    "CDPStreamClosedError",
    "CDPDecodeError",
    "CDPEventOverflowError",
    "OverflowPolicy",
    "UNSET",
    "UnsetType",
]


def __getattr__(name: str) -> type[CDPError]:
    replacement = deprecated_exception(name)
    if replacement is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return replacement
