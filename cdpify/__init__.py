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
)
from .error import (
    deprecated_exception as deprecated_exception,
)
from .error import (
    exception_getattr as _exception_getattr,
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


__getattr__ = _exception_getattr(__name__)
