import asyncio
from dataclasses import dataclass
from typing import ClassVar

import pytest

from cdpify import (
    CdpClient,
    CDPEventOverflowError,
    CDPStreamClosedError,
    TransportEvent,
)
from cdpify.events import EventRouter


@dataclass
class Event:
    __cdp_event__: ClassVar[str] = "Test.event"
    value: int


@pytest.mark.asyncio
async def test_overflow_fails_only_affected_stream_and_unregisters_immediately() -> (
    None
):
    router = EventRouter(max_queue_size=1)
    bounded = router.listen(Event, session_id=None)
    unlimited = router.listen(Event, session_id=None, max_queue_size=0)
    for i in range(3):
        await router.dispatch(TransportEvent("Test.event", {"value": i}))
    assert bounded.closed
    assert len(router._buffers) == 1
    with pytest.raises(CDPEventOverflowError) as error:
        await bounded.next()
    assert error.value.max_queue_size == 1
    assert error.value.dropped_events == 2
    with pytest.raises(CDPStreamClosedError):
        await bounded.next()
    router.close()
    assert [e.value async for e in unlimited] == [0, 1, 2]


@pytest.mark.asyncio
async def test_subscription_can_override_client_overflow_policy() -> None:
    router = EventRouter(max_queue_size=1)
    events = router.listen(Event, session_id=None, overflow="drop_oldest")
    await router.dispatch(TransportEvent("Test.event", {"value": 1}))
    await router.dispatch(TransportEvent("Test.event", {"value": 2}))
    assert (await events.next()).value == 2
    assert events.dropped_events == 1
    await events.aclose()


@pytest.mark.asyncio
async def test_raw_listeners_preserve_scope_method_and_wire_names() -> None:
    client = CdpClient("ws://unused")
    root = client.listen_raw("Future.event")
    tab = client.session("S1").listen_raw()
    all_events = client.listen_all_raw()
    messages = [
        TransportEvent("Future.event", {"wireName": 1}),
        TransportEvent("Another.event", {"wireName": 2}, "S1"),
        TransportEvent("Future.event", {"wireName": 3}, "S2"),
    ]
    for event in messages:
        await client._dispatch_event(event)
    client._event_router.close()
    assert [e async for e in root] == messages[:1]
    assert [e async for e in tab] == messages[1:2]
    assert [e async for e in all_events] == messages


@pytest.mark.asyncio
async def test_overflow_does_not_block_websocket_command_response() -> None:
    import json

    from websockets.asyncio.server import serve

    async def respond(socket):
        command = json.loads(await socket.recv())
        for i in range(3):
            await socket.send(
                json.dumps({"method": "Test.event", "params": {"value": i}})
            )
        await socket.send(json.dumps({"id": command["id"], "result": {}}))
        await socket.wait_closed()

    async with serve(respond, "127.0.0.1", 0) as server:
        url = f"ws://127.0.0.1:{server.sockets[0].getsockname()[1]}"
        async with CdpClient(url, max_queue_size=1) as client:
            events = client.listen_raw()
            assert await client.execute("Test.command", timeout=1) == {}
            with pytest.raises(CDPEventOverflowError):
                await events.next()


@pytest.mark.asyncio
async def test_raw_subscription_close_wakes_waiting_reader() -> None:
    router = EventRouter()
    events = router.listen_raw(session_id=None)
    task = asyncio.create_task(anext(events, None))
    await asyncio.sleep(0)
    await events.aclose()
    assert await task is None


def test_invalid_overflow_policy_is_rejected() -> None:
    with pytest.raises(ValueError, match="overflow"):
        EventRouter(overflow="block")
