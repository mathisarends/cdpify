import asyncio
import json
from dataclasses import dataclass
from typing import ClassVar

import pytest
from websockets.asyncio.server import ServerConnection, serve

from cdpify import CdpClient
from cdpify.exceptions import CDPConnectionError, CDPStreamClosedError


@dataclass
class _Event:
    __cdp_event__: ClassVar[str] = "Test.event"

    value: int


@pytest.mark.asyncio
async def test_websocket_client_routes_bursts_without_blocking_responses() -> None:
    async def respond(socket: ServerConnection) -> None:
        command = json.loads(await socket.recv())
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
        async with CdpClient(f"ws://127.0.0.1:{port}", max_queue_size=2) as client:
            root_events = client.listen(_Event)
            session_events = client.session("S1").listen(_Event, max_queue_size=1)
            all_events = client.listen_all(_Event, max_queue_size=0)

            result = await client.execute("Test.command", timeout=2.0)

            assert result == {"ok": True}
            assert client._event_loop_task is None
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
                await client.execute("Test.command", timeout=2.0)
                assert await events.next(timeout=2.0) == _Event(expected)
                with pytest.raises(CDPStreamClosedError):
                    await events.next(timeout=2.0)
            assert [event async for event in events] == []


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
        await events.next(timeout=1.0)
    await asyncio.wait_for(client.disconnect(), timeout=1.0)
