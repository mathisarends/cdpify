import asyncio
import json
from dataclasses import dataclass
from typing import ClassVar
from unittest.mock import AsyncMock

import pytest
from websockets.asyncio.server import ServerConnection, serve
from websockets.exceptions import ConnectionClosedOK
from websockets.http11 import Request

from cdpify import CdpClient
from cdpify.error import CDPConnectionError, CDPStreamClosedError
from cdpify.transports import websocket as websocket_module


@dataclass
class _Event:
    __cdp_event__: ClassVar[str] = "Test.event"

    value: int


@pytest.mark.asyncio
@pytest.mark.parametrize("compression", [None, "deflate"])
async def test_websocket_client_routes_bursts_without_blocking_responses(
    compression,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    unexpected_iterator = AsyncMock(
        side_effect=AssertionError("Expected callback delivery")
    )
    monkeypatch.setattr(
        websocket_module.WebSocketTransport, "events", unexpected_iterator
    )
    negotiated = []

    async def respond(socket: ServerConnection) -> None:
        negotiated.append(socket.response.headers.get("Sec-WebSocket-Extensions"))
        raw_command = await socket.recv()
        assert isinstance(raw_command, str)
        command = json.loads(raw_command)
        for session_id in (None, "S1"):
            for value in range(5):
                await socket.send(
                    json.dumps(
                        {
                            "method": "Test.event",
                            "params": {"value": value},
                            "sessionId": session_id,
                        }
                    )
                )
        await socket.send(json.dumps({"id": command["id"], "result": {"ok": True}}))
        await socket.wait_closed()

    async with serve(respond, "127.0.0.1", 0) as server:
        port = server.sockets[0].getsockname()[1]
        async with CdpClient(
            f"ws://127.0.0.1:{port}",
            max_queue_size=2,
            overflow="drop_oldest",
            compression=compression,
        ) as client:
            root_events = client.listen(_Event)
            session_events = client.bind_session("S1").listen(_Event, max_queue_size=1)
            all_events = client.listen_all(_Event, max_queue_size=0)

            result = await client.execute("Test.command", timeout_seconds=2.0)

            assert result == {"ok": True}
            unexpected_iterator.assert_not_called()
            if compression is None:
                assert negotiated == [None]
            else:
                assert negotiated[0].startswith("permessage-deflate")
            assert root_events.dropped_events == 3
            assert session_events.dropped_events == 4
            assert all_events.dropped_events == 0

        assert [event.value async for event in root_events] == [3, 4]
        assert [event.value async for event in session_events] == [4]
        assert [
            (event.session_id, event.value.value) async for event in all_events
        ] == [(session_id, value) for session_id in (None, "S1") for value in range(5)]


@pytest.mark.asyncio
async def test_browser_closure_ends_listeners_and_client_can_reconnect() -> None:
    connection_number = 0

    async def respond_and_close(socket: ServerConnection) -> None:
        nonlocal connection_number
        connection_number += 1
        value = connection_number
        command = json.loads(await socket.recv())
        await socket.send(
            json.dumps({"method": "Test.event", "params": {"value": value}})
        )
        await socket.send(json.dumps({"id": command["id"], "result": {}}))
        await socket.close()

    async with serve(respond_and_close, "127.0.0.1", 0) as server:
        port = server.sockets[0].getsockname()[1]
        client = CdpClient(f"ws://127.0.0.1:{port}", max_queue_size=1)
        for expected in (1, 2):
            async with client:
                events = client.listen(_Event)
                await client.execute("Test.command", timeout_seconds=2.0)
                assert await events.next(timeout_seconds=2.0) == _Event(expected)
                with pytest.raises(CDPStreamClosedError):
                    await events.next(timeout_seconds=2.0)
            assert [event async for event in events] == []


@pytest.mark.asyncio
@pytest.mark.parametrize("direct_transport", [False, True])
async def test_overlapping_connects_open_only_one_socket(
    direct_transport: bool,
) -> None:
    handshake_started = asyncio.Event()
    finish_handshake = asyncio.Event()
    second_started = asyncio.Event()
    sockets: list[ServerConnection] = []

    async def hold_handshake(socket: ServerConnection, request: Request) -> None:
        handshake_started.set()
        await finish_handshake.wait()

    async def hold_connection(socket: ServerConnection) -> None:
        sockets.append(socket)
        await socket.wait_closed()

    async with serve(
        hold_connection, "127.0.0.1", 0, process_request=hold_handshake
    ) as server:
        port = server.sockets[0].getsockname()[1]
        client = CdpClient(f"ws://127.0.0.1:{port}")
        connection = client.transport if direct_transport else client

        async def connect_again() -> None:
            second_started.set()
            await connection.connect()

        first = asyncio.create_task(connection.connect())
        try:
            await asyncio.wait_for(handshake_started.wait(), timeout=5.0)
            second = asyncio.create_task(connect_again())
            await asyncio.wait_for(second_started.wait(), timeout=5.0)
        finally:
            finish_handshake.set()

        first_result, second_result = await asyncio.gather(
            first, second, return_exceptions=True
        )
        await connection.disconnect()

        assert first_result is None
        assert isinstance(second_result, CDPConnectionError)
        assert str(second_result) == "Already connected"
        assert len(sockets) == 1
        await asyncio.wait_for(sockets[0].wait_closed(), timeout=5.0)
        assert not server.connections


@pytest.mark.asyncio
async def test_failed_callback_connection_closes_existing_subscriptions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from cdpify.transports import websocket

    async def fail(*args: object, **kwargs: object) -> None:
        raise OSError("Connection refused")

    monkeypatch.setattr(websocket, "connect", fail)
    client = CdpClient("ws://example", max_queue_size=1)
    events = client.listen(_Event)

    with pytest.raises(CDPConnectionError, match="Connection refused"):
        await client.connect()

    with pytest.raises(CDPStreamClosedError):
        await events.next(timeout_seconds=1.0)
    await asyncio.wait_for(client.disconnect(), timeout=1.0)


class _ClosingWebSocket:
    def __init__(self) -> None:
        self.peer_closed = asyncio.Event()
        self.closing = asyncio.Event()
        self.finish_close = asyncio.Event()
        self.close_calls = 0

    async def recv(self, decode=None):
        await self.peer_closed.wait()
        raise ConnectionClosedOK(None, None)

    async def close(self) -> None:
        self.close_calls += 1
        self.closing.set()
        await self.finish_close.wait()


@pytest.mark.asyncio
@pytest.mark.parametrize("browser_closes", [False, True])
@pytest.mark.parametrize("cancel_waiter", [False, True])
async def test_disconnect_waits_for_shared_cleanup(
    monkeypatch: pytest.MonkeyPatch, browser_closes: bool, cancel_waiter: bool
) -> None:
    socket = _ClosingWebSocket()
    monkeypatch.setattr(websocket_module, "connect", AsyncMock(return_value=socket))
    client = CdpClient("ws://example")
    await client.connect()
    events = client.listen(_Event)
    if browser_closes:
        socket.peer_closed.set()
        await asyncio.wait_for(socket.closing.wait(), timeout=1.0)

    first = asyncio.create_task(client.disconnect())
    await asyncio.wait_for(socket.closing.wait(), timeout=1.0)
    second = asyncio.create_task(client.disconnect())
    await asyncio.sleep(0)

    try:
        assert not first.done()
        assert not second.done()
        with pytest.raises(CDPConnectionError):
            await client.execute("Runtime.evaluate", timeout_seconds=0.01)
        if cancel_waiter:
            first.cancel()
            with pytest.raises(asyncio.CancelledError):
                await asyncio.wait_for(first, timeout=1.0)
            assert not second.done()
    finally:
        socket.finish_close.set()
        await asyncio.wait_for(
            asyncio.gather(first, second, return_exceptions=True), timeout=5.0
        )

    await asyncio.wait_for(second, timeout=1.0)
    assert not client.is_connected
    assert socket.close_calls == 1
    with pytest.raises(CDPStreamClosedError):
        await events.next(timeout_seconds=1.0)
    await client.disconnect()
