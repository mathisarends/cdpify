import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import ClassVar
from unittest.mock import AsyncMock, call

import pytest

from cdpify import CdpClient, CdpSession, CDPSessionClosedError
from cdpify.error import CDPStreamClosedError
from cdpify.transport import TransportEvent


@dataclass(kw_only=True, slots=True)
class _Event:
    __cdp_event__: ClassVar[str] = "Test.event"

    value: int = field(metadata={"cdp_name": "value"})


class _Transport:
    def __init__(self) -> None:
        self.is_connected = False
        self.execute = AsyncMock(return_value={})
        self._events: asyncio.Queue[TransportEvent | None] = asyncio.Queue()

    async def connect(self) -> None:
        self.is_connected = True

    async def disconnect(self) -> None:
        self.is_connected = False
        self._events.put_nowait(None)

    async def events(self) -> AsyncIterator[TransportEvent]:
        while True:
            event = await self._events.get()
            if event is None:
                return
            yield event

    def emit(self, event: TransportEvent) -> None:
        self._events.put_nowait(event)


@pytest.mark.asyncio
async def test_attach_requests_flat_session_and_routes_commands() -> None:
    transport = _Transport()
    transport.execute.return_value = {"sessionId": "session-1"}
    client = CdpClient(transport=transport)  # type: ignore[arg-type]

    session = await client.attach("target-1")
    await session.page.enable()

    assert transport.execute.await_args_list == [
        call(
            method="Target.attachToTarget",
            params={"targetId": "target-1", "flatten": True},
            session_id=None,
            timeout_seconds=None,
        ),
        call(
            method="Page.enable",
            params={},
            session_id="session-1",
            timeout_seconds=None,
        ),
    ]


def test_client_creates_immutable_session_view() -> None:
    transport = _Transport()
    client = CdpClient(transport=transport)  # type: ignore[arg-type]

    session = client.bind_session("session-1")
    transport.execute.assert_not_called()

    assert isinstance(session, CdpSession)
    assert session.session_id == "session-1"
    assert not hasattr(session, "switch_to")
    with pytest.raises(AttributeError):
        session.session_id = "session-2"  # type: ignore[misc]


def test_rejects_empty_session_id() -> None:
    client = CdpClient(transport=_Transport())  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="must not be empty"):
        client.bind_session("")


@pytest.mark.asyncio
async def test_generated_commands_are_bound_to_session() -> None:
    transport = _Transport()
    session = CdpClient(transport=transport).bind_session("session-2")  # type: ignore[arg-type]

    await session.page.enable()

    assert transport.execute.await_args_list == [
        call(
            method="Page.enable",
            params={},
            session_id="session-2",
            timeout_seconds=None,
        )
    ]


@pytest.mark.asyncio
async def test_low_level_execute_cannot_override_bound_session() -> None:
    transport = _Transport()
    session = CdpClient(transport=transport).bind_session("session-2")  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        await session.execute("Page.enable", {}, None)  # type: ignore[call-arg]
    transport.execute.assert_not_called()

    await session.execute(
        "Runtime.evaluate", {"expression": "1 + 1"}, timeout_seconds=None
    )

    transport.execute.assert_awaited_once_with(
        method="Runtime.evaluate",
        params={"expression": "1 + 1"},
        session_id="session-2",
        timeout_seconds=None,
    )
    with pytest.raises(TypeError):
        await session.execute(  # type: ignore[call-arg]
            "Runtime.evaluate",
            session_id="another-session",
        )


@pytest.mark.asyncio
async def test_sessions_are_safe_to_use_concurrently() -> None:
    transport = _Transport()
    client = CdpClient(transport=transport)  # type: ignore[arg-type]
    session_a = client.bind_session("A")
    session_b = client.bind_session("B")

    await asyncio.gather(
        session_a.page.enable(),
        session_b.page.enable(),
    )

    assert transport.execute.await_count == 2
    transport.execute.assert_has_awaits(
        [
            call(
                method="Page.enable",
                params={},
                session_id="A",
                timeout_seconds=None,
            ),
            call(
                method="Page.enable",
                params={},
                session_id="B",
                timeout_seconds=None,
            ),
        ],
        any_order=True,
    )


@pytest.mark.asyncio
async def test_session_listener_filters_other_sessions() -> None:
    transport = _Transport()
    client = CdpClient(transport=transport)  # type: ignore[arg-type]
    await client.connect()
    stream = client.bind_session("A").listen(_Event, timeout_seconds=1.0)
    next_event = asyncio.create_task(anext(stream))
    await asyncio.sleep(0)

    transport.emit(TransportEvent("Test.event", {"value": 2}, session_id="B"))
    transport.emit(TransportEvent("Test.event", {"value": 1}, session_id="A"))

    assert await asyncio.wait_for(next_event, timeout=1.0) == _Event(value=1)
    await stream.aclose()
    await client.disconnect()


@pytest.mark.asyncio
async def test_detached_session_cannot_send_or_subscribe_again() -> None:
    transport = _Transport()
    client = CdpClient(transport=transport)
    async with client:
        tab = client.bind_session("A")
        domain = tab.page
        events = tab.listen_raw()
        transport.emit(TransportEvent("Target.detachedFromTarget", {"sessionId": "A"}))
        with pytest.raises(CDPStreamClosedError):
            await events.next(timeout_seconds=1.0)

        with pytest.raises(CDPSessionClosedError) as error:
            tab.listen(_Event)
        assert error.value.session_id == "A"
        with pytest.raises(CDPSessionClosedError):
            client.bind_session("A").listen_raw()
        with pytest.raises(CDPSessionClosedError):
            await domain.enable()
        with pytest.raises(CDPSessionClosedError):
            await tab.execute("Page.enable")
        with pytest.raises(CDPSessionClosedError):
            await client.execute("Page.enable", session_id="A")
        transport.execute.assert_not_awaited()
        await client.bind_session("B").page.enable()

    async with client:
        with pytest.raises(CDPSessionClosedError):
            tab.listen_raw()
        with pytest.raises(CDPSessionClosedError):
            await domain.enable()
        await client.bind_session("A").page.enable()
