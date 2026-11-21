import asyncio
import gc
import weakref
from copy import deepcopy
from dataclasses import dataclass
from typing import ClassVar
from unittest.mock import Mock, create_autospec

import pytest

from cdpify.error import CDPStreamClosedError
from cdpify.events import EventRouter
from cdpify.transport import TransportEvent


@dataclass
class _Event:
    __cdp_event__: ClassVar[str] = "Test.event"

    value: int


def _event(value: int, session_id: str | None = None) -> TransportEvent:
    return TransportEvent("Test.event", {"value": value}, session_id=session_id)


@pytest.mark.asyncio
async def test_generated_enum_event_marker_routes_wire_strings() -> None:
    from cdpify.domains.network import LoadingFailedEvent, ResourceType

    router = EventRouter()
    async with router.listen(LoadingFailedEvent, session_id=None) as events:
        assert (
            await router.dispatch(
                TransportEvent(
                    "Network.loadingFailed",
                    {
                        "requestId": "R1",
                        "timestamp": 1.0,
                        "type": "Fetch",
                        "errorText": "Failed",
                    },
                )
            )
            is True
        )

        event = await events.next(timeout_seconds=1.0)
        assert event.type is ResourceType.FETCH


@pytest.mark.asyncio
async def test_events_before_first_read_are_buffered() -> None:
    router = EventRouter()
    events = router.listen(_Event, session_id=None)

    await router.dispatch(_event(1))

    assert await events.next(timeout_seconds=1.0) == _Event(value=1)


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
        await events.next(timeout_seconds=0.01)


@pytest.mark.asyncio
async def test_zero_timeout_reads_buffered_events_or_reports_empty_queue() -> None:
    router = EventRouter()
    events = router.listen(_Event, session_id=None)
    with pytest.raises(TimeoutError):
        await events.next(timeout_seconds=0)

    await router.dispatch(_event(1))
    assert await events.next(timeout_seconds=0) == _Event(1)
    with pytest.raises(TimeoutError):
        await events.next(timeout_seconds=0)

    await router.dispatch(_event(2))
    router.close()
    assert await events.next(timeout_seconds=0) == _Event(2)
    with pytest.raises(CDPStreamClosedError):
        await events.next(timeout_seconds=0)


@pytest.mark.asyncio
async def test_next_uses_listen_timeout_by_default() -> None:
    router = EventRouter()
    events = router.listen(_Event, session_id=None, timeout_seconds=0.01)

    with pytest.raises(TimeoutError):
        await events.next()


@pytest.mark.asyncio
async def test_router_close_drains_buffered_events_then_ends() -> None:
    router = EventRouter()
    events = router.listen(_Event, session_id=None)
    await router.dispatch(_event(1))

    router.close()

    assert not events.closed
    assert await events.next() == _Event(value=1)
    assert events.closed
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
    received = await events.next(timeout_seconds=1.0)

    assert received.value == _Event(value=1)
    assert received.session_id == "S1"


@pytest.mark.asyncio
async def test_detaching_session_ends_only_its_subscriptions_after_drain() -> None:
    router = EventRouter()
    detached = router.listen(_Event, session_id="child")
    waiting = router.listen_raw("Test.waiting", session_id="child")
    parent = router.listen_raw("Target.detachedFromTarget", session_id="parent")
    parent_events = router.listen(_Event, session_id="parent")
    root = router.listen(_Event, session_id=None)
    all_events = router.listen_all(_Event)
    await router.dispatch(_event(1, session_id="child"))
    reader = asyncio.create_task(anext(waiting, None))
    await asyncio.sleep(0)

    notification = TransportEvent(
        "Target.detachedFromTarget", {"sessionId": "child"}, session_id="parent"
    )
    await router.dispatch(notification)

    assert await parent.next(timeout_seconds=1.0) == notification
    assert await asyncio.wait_for(reader, timeout=1.0) is None
    assert await detached.next(timeout_seconds=1.0) == _Event(1)
    with pytest.raises(CDPStreamClosedError):
        await detached.next(timeout_seconds=1.0)

    await router.dispatch(_event(2))
    await router.dispatch(_event(3, session_id="parent"))
    assert await root.next(timeout_seconds=1.0) == _Event(2)
    assert await parent_events.next(timeout_seconds=1.0) == _Event(3)
    assert (await all_events.next(timeout_seconds=1.0)).session_id == "child"
    assert (await all_events.next(timeout_seconds=1.0)).value == _Event(2)


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

    assert await events.next(timeout_seconds=1.0) == _UnnamedEvent(value=5)


@pytest.mark.asyncio
async def test_bounded_listeners_drop_oldest_independently_and_drain_on_close() -> None:
    router = EventRouter(max_queue_size=2, overflow="drop_oldest")
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
        await events.next(timeout_seconds=0.01)
    reader = asyncio.create_task(events.next())
    await asyncio.sleep(0)
    reader.cancel()
    with pytest.raises(asyncio.CancelledError):
        await asyncio.wait_for(reader, timeout=1.0)

    await router.dispatch(_event(3))

    assert await events.next(timeout_seconds=1.0) == _Event(3)
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


def _observe_construction(monkeypatch: pytest.MonkeyPatch, event_type: type) -> Mock:
    original_init = event_type.__init__
    construct = create_autospec(original_init, side_effect=original_init)
    monkeypatch.setattr(event_type, "__init__", construct)
    return construct


@pytest.mark.asyncio
@pytest.mark.parametrize("session_id", [None, "S1"])
async def test_matching_listeners_decode_once_and_share_model(
    monkeypatch: pytest.MonkeyPatch, session_id: str | None
) -> None:
    construct = _observe_construction(monkeypatch, _Event)
    router = EventRouter()
    first = router.listen(_Event, session_id=session_id)
    second = router.listen(_Event, session_id=session_id)
    all_events = router.listen_all(_Event)
    await router.dispatch(_event(1, session_id=session_id))
    construct.assert_not_called()

    shared = await first.next(timeout_seconds=1.0)
    assert await second.next(timeout_seconds=1.0) is shared
    received = await all_events.next(timeout_seconds=1.0)
    assert received.value is shared
    assert received.session_id == session_id
    construct.assert_called_once_with(shared, value=1)

    owned = deepcopy(shared)
    owned.value = 99
    assert shared.value == 1
    await first.aclose()
    await second.aclose()
    await all_events.aclose()


@pytest.mark.asyncio
async def test_decode_cache_is_scoped_to_each_event_and_target_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    construct = _observe_construction(monkeypatch, _Event)
    construct_custom = _observe_construction(monkeypatch, _UnnamedEvent)
    router = EventRouter()
    events = router.listen(_Event, session_id=None)
    duplicates = router.listen(_Event, session_id=None)
    custom = router.listen(_UnnamedEvent, session_id=None, event_name="Test.event")
    for value in (1, 2):
        await router.dispatch(_event(value))
    router.close()

    first, second = [event async for event in events]
    copies = [event async for event in duplicates]
    other_types = [event async for event in custom]

    assert first is copies[0]
    assert second is copies[1]
    assert first is not second
    assert construct.call_count == 2
    assert construct_custom.call_count == 2
    assert [first, second] == [_Event(1), _Event(2)]
    assert other_types == [_UnnamedEvent(1), _UnnamedEvent(2)]


@pytest.mark.asyncio
async def test_shared_event_mutations_are_visible_to_other_listeners() -> None:
    router = EventRouter()
    first = router.listen(_Event, session_id=None)
    second = router.listen(_Event, session_id=None)
    await router.dispatch(_event(1))

    shared = await first.next(timeout_seconds=1.0)
    shared.value = 99

    assert (await second.next(timeout_seconds=1.0)).value == 99
    await first.aclose()
    await second.aclose()


@pytest.mark.asyncio
async def test_decode_cache_is_released_when_remaining_listener_closes() -> None:
    router = EventRouter()
    first = router.listen(_Event, session_id=None)
    slow = router.listen(_Event, session_id=None)
    await router.dispatch(_event(1))
    model = await first.next(timeout_seconds=1.0)
    reference = weakref.ref(model)
    del model
    await first.aclose()
    assert reference() is not None

    await slow.aclose()
    gc.collect()

    assert reference() is None


@pytest.mark.parametrize("max_queue_size", [-1, 1.5])
def test_rejects_invalid_queue_limits(max_queue_size: int) -> None:
    with pytest.raises((ValueError, TypeError), match="max_queue_size"):
        EventRouter(max_queue_size=max_queue_size)
    with pytest.raises((ValueError, TypeError), match="max_queue_size"):
        EventRouter().listen(_Event, session_id=None, max_queue_size=max_queue_size)
