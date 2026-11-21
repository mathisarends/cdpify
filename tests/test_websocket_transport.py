import asyncio
import gc
import json
from unittest.mock import AsyncMock

import pytest
from websockets.asyncio.server import ServerConnection, serve
from websockets.exceptions import ConnectionClosedOK

from cdpify.error import (
    CDPCommandError,
    CDPConnectionError,
    CDPTimeoutError,
)
from cdpify.transport import TransportEvent
from cdpify.transports import websocket as websocket_module
from cdpify.transports.websocket import WebSocketTransport


class _FakeWebSocket:
    def __init__(self) -> None:
        self.sent: asyncio.Queue[tuple[str | bytes, bool | None]] = asyncio.Queue()
        self.incoming: asyncio.Queue[bytes] = asyncio.Queue()
        self.closed = False

    async def send(self, payload: str | bytes, *, text: bool | None = None) -> None:
        self.sent.put_nowait((payload, text))

    async def recv(self, decode=None) -> bytes:
        assert decode is False
        return await self.incoming.get()

    async def close(self) -> None:
        self.closed = True

    def receive(self, message: dict) -> None:
        self.incoming.put_nowait(json.dumps(message).encode())


class _ScriptedWebSocket(_FakeWebSocket):
    def __init__(self, messages: list[str]) -> None:
        super().__init__()
        self._messages = iter(messages)
        self.exhausted = asyncio.Event()

    async def recv(self, decode=None) -> bytes:
        assert decode is False
        message = next(self._messages, None)
        if message is None:
            self.exhausted.set()
            raise ConnectionClosedOK(None, None)
        return message.encode()


@pytest.fixture
def socket(monkeypatch: pytest.MonkeyPatch) -> _FakeWebSocket:
    connection = _FakeWebSocket()
    monkeypatch.setattr(websocket_module, "connect", AsyncMock(return_value=connection))
    return connection


@pytest.mark.asyncio
async def test_execute_timeout_includes_sending_and_can_recover(
    socket: _FakeWebSocket,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_send = socket.send
    cancelled = asyncio.Event()

    async def blocked_send(payload, *, text=None) -> None:
        await original_send(payload, text=text)
        try:
            await asyncio.Event().wait()
        finally:
            cancelled.set()

    async with WebSocketTransport("ws://example") as transport:
        with monkeypatch.context() as patch:
            patch.setattr(socket, "send", blocked_send)
            with pytest.raises(CDPTimeoutError):
                await transport.execute("Runtime.enable", timeout_seconds=0.02)
        assert cancelled.is_set()

        expired_payload, _ = socket.sent.get_nowait()
        expired_id = json.loads(expired_payload)["id"]
        command = asyncio.create_task(transport.execute("Page.enable"))
        payload, _ = await asyncio.wait_for(socket.sent.get(), timeout=1.0)
        active_id = json.loads(payload)["id"]

        socket.receive({"id": expired_id, "result": {"expired": True}})
        socket.receive({"id": active_id, "result": {"ok": True}})
        assert await asyncio.wait_for(command, timeout=1.0) == {"ok": True}


@pytest.mark.asyncio
async def test_execute_requires_connection() -> None:
    transport = WebSocketTransport("ws://example")

    with pytest.raises(CDPConnectionError):
        await transport.execute("Runtime.enable")


@pytest.mark.asyncio
async def test_execute_raises_command_error_and_connection_stays_usable(
    socket: _FakeWebSocket,
) -> None:
    async with WebSocketTransport("ws://example") as transport:
        command = asyncio.create_task(transport.execute("Page.enable"))
        payload, _ = await asyncio.wait_for(socket.sent.get(), timeout=1.0)
        request = json.loads(payload)
        assert request["params"] == {}
        socket.receive(
            {
                "id": request["id"],
                "error": {"code": 9, "message": "failed"},
            }
        )

        with pytest.raises(CDPCommandError) as error:
            await asyncio.wait_for(command, timeout=1.0)
        assert error.value.method == "Page.enable"
        assert error.value.code == 9
        assert str(error.value) == "Page.enable failed with CDP error 9: failed"

        following = asyncio.create_task(transport.execute("Page.enable"))
        payload, _ = await asyncio.wait_for(socket.sent.get(), timeout=1.0)
        socket.receive({"id": json.loads(payload)["id"], "result": {"ok": True}})
        assert await asyncio.wait_for(following, timeout=1.0) == {"ok": True}


@pytest.mark.asyncio
async def test_disconnect_fails_waiting_commands_and_closes_socket(
    socket: _FakeWebSocket,
) -> None:
    async with WebSocketTransport("ws://example") as transport:
        command = asyncio.create_task(transport.execute("Page.enable"))
        await asyncio.wait_for(socket.sent.get(), timeout=1.0)

        await transport.disconnect()

        assert socket.closed
        assert not transport.is_connected
        with pytest.raises(CDPConnectionError, match="Disconnected"):
            await asyncio.wait_for(command, timeout=1.0)


@pytest.mark.asyncio
async def test_client_forwards_explicit_connection_options(monkeypatch) -> None:
    from cdpify import CdpClient

    dial = AsyncMock(return_value=_ScriptedWebSocket([]))
    monkeypatch.setattr(websocket_module, "connect", dial)
    client = CdpClient(
        "ws://example",
        compression="deflate",
        open_timeout_seconds=4,
        close_timeout_seconds=3,
    )
    await client.connect()
    dial.assert_awaited_once_with(
        "ws://example",
        max_size=100 * 1024 * 1024,
        additional_headers=None,
        compression="deflate",
        open_timeout=4,
        close_timeout=3,
    )
    await client.disconnect()


@pytest.mark.asyncio
@pytest.mark.parametrize("backend", ["json", "orjson"])
async def test_message_loop_skips_malformed_messages(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    backend: str,
) -> None:
    monkeypatch.setattr(
        websocket_module,
        "orjson",
        None if backend == "json" else pytest.importorskip("orjson"),
    )
    socket = _ScriptedWebSocket(
        [
            "not json",
            "null",
            '{"foo": "bar"}',
            '{"method": "Page.loadEventFired", "params": {}}',
        ]
    )
    monkeypatch.setattr(websocket_module, "connect", AsyncMock(return_value=socket))

    with caplog.at_level("WARNING"):
        async with WebSocketTransport("ws://example") as transport:
            async with asyncio.timeout(2):
                events = [event async for event in transport.events()]

    assert [event.method for event in events] == ["Page.loadEventFired"]
    assert "Dropping malformed CDP message" in caplog.text
    assert "Unknown CDP message format" in caplog.text


@pytest.mark.asyncio
@pytest.mark.parametrize("backend", ["json", "orjson"])
async def test_websocket_response_preserves_lone_surrogates(
    monkeypatch: pytest.MonkeyPatch, backend: str
) -> None:
    monkeypatch.setattr(
        websocket_module,
        "orjson",
        None if backend == "json" else pytest.importorskip("orjson"),
    )
    value = chr(0xD800)

    async def respond(socket: ServerConnection) -> None:
        command = json.loads(await socket.recv())
        await socket.send(json.dumps({"id": command["id"], "result": {"value": value}}))
        await socket.wait_closed()

    async with serve(respond, "127.0.0.1", 0) as server:
        port = server.sockets[0].getsockname()[1]
        async with WebSocketTransport(f"ws://127.0.0.1:{port}") as transport:
            assert await transport.execute("Runtime.evaluate", timeout_seconds=2.0) == {
                "value": value
            }


@pytest.mark.asyncio
async def test_event_without_params_has_empty_params(monkeypatch) -> None:
    socket = _ScriptedWebSocket(
        [
            '{"method": "Page.loadEventFired", "params": null}',
            '{"method": "Page.domContentEventFired"}',
        ]
    )
    monkeypatch.setattr(websocket_module, "connect", AsyncMock(return_value=socket))
    async with WebSocketTransport("ws://example") as transport:
        async with asyncio.timeout(2):
            events = [event async for event in transport.events()]

    assert [event.params for event in events] == [{}, {}]


@pytest.mark.asyncio
async def test_bounded_transport_drains_latest_events_on_disconnect(
    monkeypatch,
) -> None:
    socket = _ScriptedWebSocket(
        [
            json.dumps({"method": "Test.event", "params": {"value": value}})
            for value in range(5)
        ]
    )
    monkeypatch.setattr(websocket_module, "connect", AsyncMock(return_value=socket))
    async with WebSocketTransport(
        "ws://example", max_queue_size=2, overflow="drop_oldest"
    ) as transport:
        await asyncio.wait_for(socket.exhausted.wait(), timeout=1.0)
        await transport.disconnect()
        await transport.disconnect()

        async with asyncio.timeout(2):
            assert [event.params["value"] async for event in transport.events()] == [
                3,
                4,
            ]
        assert transport.dropped_events == 3


@pytest.mark.asyncio
async def test_disconnect_wakes_transport_reader() -> None:
    transport = WebSocketTransport("ws://example", max_queue_size=1)
    reader = asyncio.create_task(anext(transport.events(), None))
    await asyncio.sleep(0)

    await transport.disconnect()

    assert await asyncio.wait_for(reader, timeout=1.0) is None


@pytest.mark.asyncio
@pytest.mark.parametrize("backend", ["json", "orjson"])
async def test_json_backends_send_text_and_decode_events_and_responses(
    monkeypatch: pytest.MonkeyPatch,
    backend: str,
    socket: _FakeWebSocket,
) -> None:
    monkeypatch.setattr(
        websocket_module,
        "orjson",
        None if backend == "json" else pytest.importorskip("orjson"),
    )
    value = "Grüße 🌍"
    async with WebSocketTransport("ws://example") as transport:
        task = asyncio.create_task(
            transport.execute("Test.command", {"text": value}, session_id="S1")
        )
        payload, text = await asyncio.wait_for(socket.sent.get(), timeout=1.0)
        assert isinstance(payload, bytes if backend == "orjson" else str)
        assert text is True
        request = json.loads(payload)
        assert isinstance(request["id"], int)
        assert request == {
            "id": request["id"],
            "method": "Test.command",
            "params": {"text": value},
            "sessionId": "S1",
        }
        socket.receive({"id": request["id"], "result": {"ok": True}})
        socket.receive(
            {
                "method": "Test.event",
                "sessionId": "S1",
                "params": {"text": value},
            }
        )

        assert await asyncio.wait_for(task, timeout=1.0) == {"ok": True}
        event = await asyncio.wait_for(anext(transport.events()), timeout=1.0)
        assert event == TransportEvent("Test.event", {"text": value}, "S1")


@pytest.mark.asyncio
async def test_callback_stream_closes_once_and_excludes_iterator(monkeypatch) -> None:
    socket = _ScriptedWebSocket(['{"method":"Test.event"}'])
    monkeypatch.setattr(websocket_module, "connect", AsyncMock(return_value=socket))
    transport = WebSocketTransport("ws://example")
    handler = AsyncMock()
    transport.set_event_handler(handler)

    async with transport:
        with pytest.raises(RuntimeError, match="event handler"):
            await anext(transport.events())

        await asyncio.wait_for(socket.exhausted.wait(), timeout=1.0)
        await transport.disconnect()

    assert [call.args[0] for call in handler.await_args_list] == [
        TransportEvent("Test.event", {}),
        None,
    ]


def test_websocket_transport_rejects_negative_queue_limit() -> None:
    with pytest.raises(ValueError, match="max_queue_size"):
        WebSocketTransport("ws://example", max_queue_size=-1)


@pytest.mark.asyncio
async def test_reconnect_resets_buffer_without_migrating_old_readers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def messages(values: list[int]) -> _ScriptedWebSocket:
        return _ScriptedWebSocket(
            [
                json.dumps({"method": "Test.event", "params": {"value": value}})
                for value in values
            ]
        )

    monkeypatch.setattr(
        websocket_module,
        "connect",
        AsyncMock(side_effect=[messages([1, 2, 3]), messages([4])]),
    )
    transport = WebSocketTransport(
        "ws://example", max_queue_size=2, overflow="drop_oldest"
    )
    await transport.connect()
    old_events = transport.events()
    assert (await anext(old_events)).params == {"value": 2}
    assert transport.dropped_events == 1

    await transport.disconnect()
    await transport.connect()

    assert transport.dropped_events == 0
    assert [event.params["value"] async for event in old_events] == [3]
    assert [event.params["value"] async for event in transport.events()] == [4]
    await transport.disconnect()


@pytest.mark.asyncio
async def test_disconnect_during_send_handles_error_without_future_leak(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class SendingSocket(_FakeWebSocket):
        def __init__(self) -> None:
            super().__init__()
            self.sending = asyncio.Event()
            self.finished = asyncio.Event()

        async def send(self, payload: str | bytes, *, text=None) -> None:
            self.sending.set()
            await self.finished.wait()
            raise ConnectionClosedOK(None, None)

        async def close(self) -> None:
            self.finished.set()

    loop = asyncio.get_running_loop()
    previous_handler = loop.get_exception_handler()
    errors = []
    loop.set_exception_handler(lambda loop, context: errors.append(context))
    transport = WebSocketTransport("ws://example")
    socket = SendingSocket()
    monkeypatch.setattr(websocket_module, "connect", AsyncMock(return_value=socket))
    await transport.connect()
    command = asyncio.create_task(transport.execute("Runtime.evaluate"))
    try:
        await asyncio.wait_for(socket.sending.wait(), timeout=1.0)
        await transport.disconnect()
        with pytest.raises(CDPConnectionError):
            await asyncio.wait_for(command, timeout=1.0)
        del command
        gc.collect()
        await asyncio.sleep(0)
        assert not transport.is_connected
        assert errors == []
    finally:
        loop.set_exception_handler(previous_handler)
