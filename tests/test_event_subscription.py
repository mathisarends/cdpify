import asyncio
import gc
from dataclasses import dataclass

import pytest

from cdpify.events import EventRouter
from cdpify.exceptions import CDPStreamClosedError
from cdpify.transport import TransportEvent


@dataclass
class _Event:
    value: int


def _event(value: int, session_id: str | None = None) -> TransportEvent:
    return TransportEvent("Test.event", {"value": value}, session_id=session_id)


@pytest.mark.asyncio
async def test_events_before_first_read_are_buffered() -> None:
    router = EventRouter()
    events = router.listen("Test.event", _Event, session_id=None)

    await router.dispatch(_event(1))

    assert await events.next(timeout=1.0) == _Event(value=1)


@pytest.mark.asyncio
async def test_async_with_unsubscribes_on_exit() -> None:
    router = EventRouter()

    async with router.listen("Test.event", _Event, session_id=None) as events:
        assert await router.dispatch(_event(1)) is True

    assert events.closed is True
    assert await router.dispatch(_event(2)) is False


@pytest.mark.asyncio
async def test_next_raises_timeout_error_without_events() -> None:
    router = EventRouter()
    events = router.listen("Test.event", _Event, session_id=None)

    with pytest.raises(TimeoutError):
        await events.next(timeout=0.01)


@pytest.mark.asyncio
async def test_next_uses_listen_timeout_by_default() -> None:
    router = EventRouter()
    events = router.listen("Test.event", _Event, session_id=None, timeout=0.01)

    with pytest.raises(TimeoutError):
        await events.next()


@pytest.mark.asyncio
async def test_router_close_drains_buffered_events_then_ends() -> None:
    router = EventRouter()
    events = router.listen("Test.event", _Event, session_id=None)
    await router.dispatch(_event(1))

    router.close()

    assert [event async for event in events] == [_Event(value=1)]
    with pytest.raises(CDPStreamClosedError):
        await events.next()


@pytest.mark.asyncio
async def test_aclose_drops_buffered_events() -> None:
    router = EventRouter()
    events = router.listen("Test.event", _Event, session_id=None)
    await router.dispatch(_event(1))

    await events.aclose()

    assert [event async for event in events] == []


@pytest.mark.asyncio
async def test_aclose_wakes_a_waiting_reader() -> None:
    router = EventRouter()
    events = router.listen("Test.event", _Event, session_id=None)
    reader = asyncio.create_task(anext(events, None))
    await asyncio.sleep(0)

    await events.aclose()

    assert await asyncio.wait_for(reader, timeout=1.0) is None


@pytest.mark.asyncio
async def test_unreferenced_subscription_unsubscribes() -> None:
    router = EventRouter()
    router.listen("Test.event", _Event, session_id=None)
    gc.collect()

    assert await router.dispatch(_event(1)) is False


@pytest.mark.asyncio
async def test_listen_all_wraps_events_with_session_id() -> None:
    router = EventRouter()
    events = router.listen_all("Test.event", _Event)

    await router.dispatch(_event(1, session_id="S1"))
    received = await events.next(timeout=1.0)

    assert received.value == _Event(value=1)
    assert received.session_id == "S1"
