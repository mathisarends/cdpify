from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class TransportEvent:
    method: str
    params: dict[str, Any]
    session_id: str | None = None


class Transport(Protocol):
    @property
    def is_connected(self) -> bool: ...

    async def connect(self) -> None: ...

    async def disconnect(self) -> None: ...

    async def execute(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        session_id: str | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]: ...

    def events(self) -> AsyncIterator[TransportEvent]:
        """Yield incoming events until the connection closes.

        The stream has a single consumer: ``CdpClient`` reads it to route events
        to listeners. Use ``CdpClient.listen()`` instead of iterating it directly.
        """
        ...


type EventHandler = Callable[[TransportEvent | None], Awaitable[None]]


@runtime_checkable
class CallbackTransport(Transport, Protocol):
    """Optional transport capability for delivering events without a queue."""

    def set_event_handler(self, handler: EventHandler | None) -> None:
        """Select callback delivery before connecting; None selects events().

        Await the handler for each event, in order, and once with None on
        stream closure. Handlers must not wait for commands on this transport:
        they run inside its receive loop. CdpClient only enqueues listener data.
        """
        ...
