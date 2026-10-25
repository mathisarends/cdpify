import asyncio
import gc
from dataclasses import dataclass
from typing import ClassVar

import pytest

from cdpify.events import EventRouter
from cdpify.exceptions import CDPStreamClosedError
from cdpify.transport import TransportEvent


@dataclass
class _Event:
    __cdp_event__: ClassVar[str] = "Test.event"

    value: int


def _event(value: int, session_id: str | None = None) -> TransportEvent:
    return TransportEvent("Test.event", {"value": value}, session_id=session_id)


@pytest.mark.asyncio
async def test_events_before_first_read_are_buffered() -> None:
    router = EventRouter()
    events = router.listen(_Event, session_id=None)

    await router.dispatch(_event(1))

    assert await events.next(timeout=1.0) == _Event(value=1)


@pytest.mark.asyncio
async def test_async_with_unsubscribes_on_exit() -> None:
    router = EventRouter()

    async with router.listen(_Event, session_id=None) as events:
        assert await router.dispatch(_event(1)) is True

    assert events.closed is True
    assert await router.dispatch(_event(2)) is False


@pytest.mark.asyncio
async def test_next_raises_timeout_error_without_events() -> None:
    router = EventRouter()
    events = router.listen(_Event, session_id=None)

    with pytest.raises(TimeoutError):
        await events.next(timeout=0.01)


@pytest.mark.asyncio
async def test_next_uses_listen_timeout_by_default() -> None:
    router = EventRouter()
    events = router.listen(_Event, session_id=None, timeout=0.01)

    with pytest.raises(TimeoutError):
        await events.next()


@pytest.mark.asyncio
async def test_router_close_drains_buffered_events_then_ends() -> None:
    router = EventRouter()
    events = router.listen(_Event, session_id=None)
    await router.dispatch(_event(1))

    router.close()

    assert [event async for event in events] == [_Event(value=1)]
    with pytest.raises(CDPStreamClosedError):
        await events.next()


@pytest.mark.asyncio
async def test_aclose_drops_buffered_events() -> None:
    router = EventRouter()
    events = router.listen(_Event, session_id=None)
    await router.dispatch(_event(1))

    await events.aclose()

    assert [event async for event in events] == []


@pytest.mark.asyncio
async def test_aclose_wakes_a_waiting_reader() -> None:
    router = EventRouter()
    events = router.listen(_Event, session_id=None)
    reader = asyncio.create_task(anext(events, None))
    await asyncio.sleep(0)

    await events.aclose()

    assert await asyncio.wait_for(reader, timeout=1.0) is None


@pytest.mark.asyncio
async def test_unreferenced_subscription_unsubscribes() -> None:
    router = EventRouter()
    router.listen(_Event, session_id=None)
    gc.collect()

    assert await router.dispatch(_event(1)) is False


@pytest.mark.asyncio
async def test_listen_all_wraps_events_with_session_id() -> None:
    router = EventRouter()
    events = router.listen_all(_Event)

    await router.dispatch(_event(1, session_id="S1"))
    received = await events.next(timeout=1.0)

    assert received.value == _Event(value=1)
    assert received.session_id == "S1"


@dataclass
class _UnnamedEvent:
    value: int


def test_listen_requires_event_name_for_classes_without_cdp_event() -> None:
    router = EventRouter()

    with pytest.raises(TypeError, match="pass event_name="):
        router.listen(_UnnamedEvent, session_id=None)


@pytest.mark.asyncio
async def test_event_name_overrides_cdp_event() -> None:
    router = EventRouter()
    events = router.listen(_UnnamedEvent, session_id=None, event_name="Custom.event")

    await router.dispatch(TransportEvent("Custom.event", {"value": 5}))

    assert await events.next(timeout=1.0) == _UnnamedEvent(value=5)


@pytest.mark.asyncio
async def test_bounded_listeners_drop_oldest_independently_and_drain_on_close() -> None:
    router = EventRouter(max_queue_size=2)
    bounded = router.listen(_Event, session_id=None)
    unlimited = router.listen(_Event, session_id=None, max_queue_size=0)
    global_events = router.listen_all(_Event, max_queue_size=1)

    for value in range(5):
        await router.dispatch(_event(value))
    router.close()
    router.close()

    assert [event.value async for event in bounded] == [3, 4]
    assert bounded.dropped_events == 3
    assert [event.value async for event in unlimited] == [0, 1, 2, 3, 4]
    assert unlimited.dropped_events == 0
    assert [event.value.value async for event in global_events] == [4]
    assert global_events.dropped_events == 4


@pytest.mark.asyncio
async def test_full_buffer_can_be_closed_without_reading() -> None:
    router = EventRouter(max_queue_size=1)
    events = router.listen(_Event, session_id=None)
    await router.dispatch(_event(1))

    await asyncio.wait_for(events.aclose(), timeout=1.0)

    assert [event async for event in events] == []
    assert events.dropped_events == 0
    assert await router.dispatch(_event(2)) is False


@pytest.mark.asyncio
async def test_timed_out_or_cancelled_read_does_not_lose_next_event() -> None:
    router = EventRouter(max_queue_size=1)
    events = router.listen(_Event, session_id=None)
    with pytest.raises(TimeoutError):
        await events.next(timeout=0.01)
    reader = asyncio.create_task(events.next())
    await asyncio.sleep(0)
    reader.cancel()
    with pytest.raises(asyncio.CancelledError):
        await reader

    await router.dispatch(_event(3))

    assert await events.next(timeout=1.0) == _Event(3)
    await events.aclose()


@pytest.mark.asyncio
async def test_reopening_router_keeps_old_subscriptions_closed() -> None:
    router = EventRouter(max_queue_size=1)
    old_events = router.listen(_Event, session_id=None)
    await router.dispatch(_event(1))
    router.close()
    assert await router.dispatch(_event(2)) is False
    router.open()
    new_events = router.listen(_Event, session_id=None)
    await router.dispatch(_event(3))
    router.close()

    assert [event.value async for event in old_events] == [1]
    assert [event.value async for event in new_events] == [3]


@pytest.mark.asyncio
async def test_listeners_receive_independent_mutable_models() -> None:
    router = EventRouter()
    first = router.listen(_Event, session_id=None)
    second = router.listen(_Event, session_id=None)
    await router.dispatch(_event(1))

    changed = await first.next(timeout=1.0)
    changed.value = 99

    assert await second.next(timeout=1.0) == _Event(1)
    await first.aclose()
    await second.aclose()


@pytest.mark.parametrize("max_queue_size", [-1, 1.5])
def test_rejects_invalid_queue_limits(max_queue_size: int) -> None:
    with pytest.raises((ValueError, TypeError), match="max_queue_size"):
        EventRouter(max_queue_size=max_queue_size)
    with pytest.raises((ValueError, TypeError), match="max_queue_size"):
        EventRouter().listen(_Event, session_id=None, max_queue_size=max_queue_size)
