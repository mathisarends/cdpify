import asyncio
import builtins
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any

import pytest

from cdpify.client import Client
from cdpify.transport import TransportEvent


class _FakeTransport:
    def __init__(self) -> None:
        self.is_connected = False
        self.executions: list[dict[str, Any]] = []
        self.result: dict[str, Any] = {}
        self._events: asyncio.Queue[TransportEvent | None] = asyncio.Queue()

    async def connect(self) -> None:
        self.is_connected = True

    async def disconnect(self) -> None:
        self.is_connected = False
        self._events.put_nowait(None)

    async def execute(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        session_id: str | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        self.executions.append(
            {
                "method": method,
                "params": params,
                "session_id": session_id,
                "timeout": timeout,
            }
        )
        return self.result

    async def events(self) -> AsyncIterator[TransportEvent]:
        while True:
            event = await self._events.get()
            if event is None:
                return
            yield event

    def emit(self, event: TransportEvent) -> None:
        self._events.put_nowait(event)


@dataclass
class _EventModel:
    value: int = field(metadata={"cdp_name": "value"})


def test_requires_url_or_transport() -> None:
    with pytest.raises(TypeError, match="requires either url or transport"):
        Client()


def test_rejects_url_and_transport_together() -> None:
    with pytest.raises(TypeError, match="either url or transport"):
        Client("ws://example", transport=_FakeTransport())


def test_default_transport_has_actionable_optional_dependency_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_import = builtins.__import__

    def blocked_import(name: str, *args: object, **kwargs: object):
        if name == "cdpify.transports.websocket":
            raise ModuleNotFoundError(name="websockets")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)

    with pytest.raises(RuntimeError, match=r"cdpify\[websocket\]"):
        Client("ws://example")


def test_domain_clients_are_cached() -> None:
    client = Client(transport=_FakeTransport())
    properties = [
        "accessibility",
        "animation",
        "audits",
        "browser",
        "cache_storage",
        "cast",
        "console",
        "css",
        "debugger",
        "device_orientation",
        "dom",
        "dom_debugger",
        "dom_snapshot",
        "dom_storage",
        "emulation",
        "event_breakpoints",
        "fetch",
        "heap_profiler",
        "indexed_db",
        "input",
        "io",
        "layer_tree",
        "log",
        "media",
        "memory",
        "network",
        "overlay",
        "page",
        "performance",
        "profiler",
        "runtime",
        "schema",
        "security",
        "service_worker",
        "storage",
        "system_info",
        "target",
        "tethering",
        "tracing",
        "web_audio",
        "web_authn",
    ]

    for name in properties:
        first = getattr(client, name)
        second = getattr(client, name)
        assert first is second


@pytest.mark.asyncio
async def test_execute_delegates_to_transport() -> None:
    transport = _FakeTransport()
    transport.result = {"value": 42}
    client = Client(transport=transport)

    result = await client.execute(
        "Runtime.evaluate",
        {"expression": "6 * 7"},
        session_id="S1",
        timeout=2.0,
    )

    assert result == {"value": 42}
    assert transport.executions == [
        {
            "method": "Runtime.evaluate",
            "params": {"expression": "6 * 7"},
            "session_id": "S1",
            "timeout": 2.0,
        }
    ]


@pytest.mark.asyncio
async def test_generated_domain_uses_transport_execute() -> None:
    transport = _FakeTransport()
    client = Client(transport=transport)

    await client.tracing.end()

    assert transport.executions == [
        {
            "method": "Tracing.end",
            "params": None,
            "session_id": None,
            "timeout": None,
        }
    ]


@pytest.mark.asyncio
async def test_connect_and_disconnect_manage_transport() -> None:
    transport = _FakeTransport()
    client = Client(transport=transport)

    await client.connect()
    assert client.is_connected is True

    await client.disconnect()
    assert client.is_connected is False
    assert client._event_loop_task is None


@pytest.mark.asyncio
async def test_listen_yields_only_typed_root_events() -> None:
    transport = _FakeTransport()
    client = Client(transport=transport)
    await client.connect()
    stream = client.listen("Test.event", _EventModel, timeout=1.0)

    next_event_task = asyncio.create_task(anext(stream))
    await asyncio.sleep(0)
    transport.emit(
        TransportEvent(
            method="Test.event",
            params={"value": 8},
            session_id="S1",
        )
    )
    transport.emit(TransportEvent(method="Test.event", params={"value": 7}))
    event = await next_event_task

    assert event.value == 7

    await stream.aclose()
    await client.disconnect()


@pytest.mark.asyncio
async def test_listen_all_preserves_session_metadata_in_envelope() -> None:
    transport = _FakeTransport()
    client = Client(transport=transport)
    await client.connect()
    stream = client.listen_all("Test.event", _EventModel, timeout=1.0)

    next_event_task = asyncio.create_task(anext(stream))
    await asyncio.sleep(0)
    transport.emit(
        TransportEvent(
            method="Test.event",
            params={"value": 7},
            session_id="S1",
        )
    )
    received = await next_event_task

    assert received.value == _EventModel(value=7)
    assert received.session_id == "S1"

    await stream.aclose()
    await client.disconnect()


@pytest.mark.asyncio
async def test_listen_ends_when_transport_stream_ends() -> None:
    transport = _FakeTransport()
    client = Client(transport=transport)
    await client.connect()
    stream = client.listen("Test.event", _EventModel)
    next_event_task = asyncio.create_task(anext(stream, None))
    await asyncio.sleep(0)

    transport.emit(TransportEvent(method="Test.event", params={"value": 1}))
    first = await next_event_task
    await transport.disconnect()
    remaining = [event async for event in stream]

    assert first == _EventModel(value=1)
    assert remaining == []
    await client.disconnect()


@pytest.mark.asyncio
async def test_listen_ends_on_client_disconnect() -> None:
    transport = _FakeTransport()
    client = Client(transport=transport)
    await client.connect()

    async def consume() -> list[_EventModel]:
        return [event async for event in client.listen("Test.event", _EventModel)]

    consumer = asyncio.create_task(consume())
    await asyncio.sleep(0)
    await client.disconnect()

    assert await asyncio.wait_for(consumer, timeout=1.0) == []


@pytest.mark.asyncio
async def test_listen_after_disconnect_ends_immediately() -> None:
    transport = _FakeTransport()
    client = Client(transport=transport)
    await client.connect()
    await client.disconnect()

    events = [event async for event in client.listen("Test.event", _EventModel)]

    assert events == []
