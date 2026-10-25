import asyncio
import gc
import json
from unittest.mock import AsyncMock

import pytest
from websockets.exceptions import ConnectionClosedOK

from cdpify.exceptions import (
    CDPCommandError,
    CDPConnectionError,
    CDPTimeoutError,
)
from cdpify.transports import websocket as websocket_module
from cdpify.transports.websocket import (
    WebSocketTransport,
    _build_message,
    _create_pending_request,
)


class _FakeWebSocket:
    def __init__(self) -> None:
        self.sent_messages: list[str] = []
        self.closed = False

    async def send(self, payload: str) -> None:
        self.sent_messages.append(payload)

    async def close(self) -> None:
        self.closed = True


def test_builds_cdp_message() -> None:
    assert _build_message(3, "Page.enable", None, "S1") == {
        "id": 3,
        "method": "Page.enable",
        "params": {},
        "sessionId": "S1",
    }


@pytest.mark.asyncio
async def test_creates_and_registers_pending_request() -> None:
    pending: dict[int, asyncio.Future[dict[str, object]]] = {}

    future = _create_pending_request(pending, 3)

    assert pending == {3: future}


@pytest.mark.asyncio
async def test_await_response_returns_result() -> None:
    transport = WebSocketTransport("ws://example")
    future = _create_pending_request(transport._pending_requests, 1)

    transport._handle_response({"id": 1, "result": {"ok": True}})
    result = await transport._await_response(1, "Page.enable", future, timeout=1.0)

    assert result == {"ok": True}


@pytest.mark.asyncio
async def test_await_response_raises_command_error_with_method() -> None:
    transport = WebSocketTransport("ws://example")
    future = _create_pending_request(transport._pending_requests, 2)

    transport._handle_response({"id": 2, "error": {"code": 9, "message": "failed"}})

    with pytest.raises(CDPCommandError) as error_info:
        await transport._await_response(2, "Page.enable", future, timeout=1.0)

    assert error_info.value.method == "Page.enable"
    assert error_info.value.code == 9
    assert str(error_info.value) == "Page.enable failed with CDP error 9: failed"


@pytest.mark.asyncio
async def test_process_message_exposes_transport_event() -> None:
    transport = WebSocketTransport("ws://example")

    await transport._process_message(
        json.dumps(
            {
                "method": "Runtime.consoleAPICalled",
                "params": {"value": 1},
                "sessionId": "S1",
            }
        )
    )
    event = await anext(transport.events())

    assert event.method == "Runtime.consoleAPICalled"
    assert event.params == {"value": 1}
    assert event.session_id == "S1"


@pytest.mark.asyncio
async def test_send_serializes_payload_as_json() -> None:
    transport = WebSocketTransport("ws://example")
    transport._ws = _FakeWebSocket()  # type: ignore[assignment]

    await transport._send(
        3,
        "Page.enable",
        {"id": 3, "method": "Page.enable", "params": {}},
    )

    payload = transport._ws.sent_messages[0]  # type: ignore[union-attr]
    assert isinstance(payload, str)
    assert json.loads(payload) == {"id": 3, "method": "Page.enable", "params": {}}


@pytest.mark.asyncio
async def test_await_response_raises_timeout() -> None:
    transport = WebSocketTransport("ws://example")
    unresolved: asyncio.Future[dict[str, object]] = asyncio.Future()

    with pytest.raises(CDPTimeoutError):
        await transport._await_response(
            1,
            "Page.enable",
            unresolved,  # type: ignore[arg-type]
            timeout=0.001,
        )


@pytest.mark.asyncio
async def test_execute_requires_connection() -> None:
    transport = WebSocketTransport("ws://example")

    with pytest.raises(CDPConnectionError):
        await transport.execute("Runtime.enable")


@pytest.mark.asyncio
async def test_execute_removes_pending_request_after_failure() -> None:
    transport = WebSocketTransport("ws://example")
    transport._ws = _FakeWebSocket()  # type: ignore[assignment]
    transport._send = AsyncMock()  # type: ignore[method-assign]
    transport._await_response = AsyncMock(  # type: ignore[method-assign]
        side_effect=CDPTimeoutError("timeout")
    )

    with pytest.raises(CDPTimeoutError):
        await transport.execute("Runtime.enable")

    assert transport._pending_requests == {}


@pytest.mark.asyncio
async def test_disconnect_cancels_pending_requests_and_closes_websocket() -> None:
    transport = WebSocketTransport("ws://example")
    websocket = _FakeWebSocket()
    transport._ws = websocket  # type: ignore[assignment]
    pending = _create_pending_request(transport._pending_requests, 1)
    transport._message_loop_task = asyncio.create_task(asyncio.sleep(10))

    await transport.disconnect()

    assert websocket.closed is True
    assert transport.is_connected is False
    with pytest.raises(CDPConnectionError):
        await pending


@pytest.mark.asyncio
async def test_process_message_warns_for_unknown_payload(
    caplog: pytest.LogCaptureFixture,
) -> None:
    transport = WebSocketTransport("ws://example")

    with caplog.at_level("WARNING"):
        await transport._process_message(json.dumps({"foo": "bar"}))

    assert "Unknown CDP message format" in caplog.text


class _ScriptedWebSocket(_FakeWebSocket):
    def __init__(self, messages: list[str]) -> None:
        super().__init__()
        self._messages = messages

    async def __aiter__(self):
        for message in self._messages:
            yield message


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
    transport = WebSocketTransport("ws://example")
    transport._ws = _ScriptedWebSocket(  # type: ignore[assignment]
        [
            "not json",
            "null",
            json.dumps({"method": "Page.loadEventFired", "params": {}}),
        ]
    )

    with caplog.at_level("ERROR"):
        await transport._run_message_loop()
    events = [event async for event in transport.events()]

    assert [event.method for event in events] == ["Page.loadEventFired"]
    assert "Dropping malformed CDP message" in caplog.text


@pytest.mark.asyncio
async def test_event_without_params_has_empty_params() -> None:
    transport = WebSocketTransport("ws://example")
    transport._ws = _ScriptedWebSocket(  # type: ignore[assignment]
        [
            json.dumps({"method": "Page.loadEventFired", "params": None}),
            json.dumps({"method": "Page.domContentEventFired"}),
        ]
    )

    await transport._run_message_loop()
    events = [event async for event in transport.events()]

    assert [event.params for event in events] == [{}, {}]


@pytest.mark.asyncio
async def test_bounded_transport_drains_latest_events_on_disconnect() -> None:
    transport = WebSocketTransport("ws://example", max_queue_size=2)
    for value in range(5):
        await transport._process_message(
            json.dumps({"method": "Test.event", "params": {"value": value}})
        )

    await transport.disconnect()
    await transport.disconnect()

    assert [event.params["value"] async for event in transport.events()] == [3, 4]
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
    monkeypatch: pytest.MonkeyPatch, backend: str
) -> None:
    monkeypatch.setattr(
        websocket_module,
        "orjson",
        None if backend == "json" else pytest.importorskip("orjson"),
    )
    transport = WebSocketTransport("ws://example")
    socket = _FakeWebSocket()
    transport._ws = socket  # type: ignore[assignment]
    payload = {"id": 1, "method": "Test.command", "params": {"text": "Grüße 🌍"}}

    await transport._send(1, "Test.command", payload)
    assert isinstance(socket.sent_messages[0], str)
    assert json.loads(socket.sent_messages[0]) == payload
    pending = _create_pending_request(transport._pending_requests, 1)
    await transport._process_message(b'{"id":1,"result":{"ok":true}}')
    assert await transport._await_response(1, "Test.command", pending, 1.0) == {
        "ok": True
    }
    await transport._process_message(
        json.dumps({"method": "Test.event", "params": {"text": "Grüße 🌍"}}).encode()
    )
    assert (await anext(transport.events())).params == {"text": "Grüße 🌍"}
    await transport.disconnect()


@pytest.mark.asyncio
async def test_callback_stream_closes_once_and_excludes_iterator() -> None:
    transport = WebSocketTransport("ws://example")
    handler = AsyncMock()
    transport.set_event_handler(handler)
    await transport._process_message('{"method":"Test.event"}')
    with pytest.raises(RuntimeError, match="event handler"):
        await anext(transport.events())

    await transport.disconnect()
    await transport.disconnect()

    assert [call.args[0] for call in handler.await_args_list] == [
        websocket_module.TransportEvent("Test.event", {}),
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
    transport = WebSocketTransport("ws://example", max_queue_size=2)
    await transport.connect()
    old_events = transport.events()
    assert (await anext(old_events)).params == {"value": 2}
    assert transport.dropped_events == 1

    await transport.connect()

    assert transport.dropped_events == 0
    assert [event.params["value"] async for event in old_events] == [3]
    assert [event.params["value"] async for event in transport.events()] == [4]
    await transport.disconnect()


@pytest.mark.asyncio
async def test_disconnect_during_send_handles_error_without_future_leak() -> None:
    class SendingSocket(_FakeWebSocket):
        def __init__(self) -> None:
            super().__init__()
            self.sending = asyncio.Event()
            self.finished = asyncio.Event()

        async def send(self, payload: str) -> None:
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
    transport._ws = socket  # type: ignore[assignment]
    command = asyncio.create_task(transport.execute("Runtime.evaluate"))
    try:
        await asyncio.wait_for(socket.sending.wait(), timeout=1.0)
        await transport.disconnect()
        with pytest.raises(CDPConnectionError):
            await command
        del command
        gc.collect()
        await asyncio.sleep(0)
        assert transport._pending_requests == {}
        assert errors == []
    finally:
        loop.set_exception_handler(previous_handler)
