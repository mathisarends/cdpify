import pytest

from cdpify.events.dispatcher import EventDispatcher, RawCDPEvent


@pytest.mark.asyncio
async def test_dispatch_invokes_specific_and_wildcard_handlers() -> None:
    dispatcher = EventDispatcher()
    calls: list[tuple[str, RawCDPEvent]] = []

    async def specific(event: RawCDPEvent) -> None:
        calls.append(("specific", event))

    async def wildcard(event: RawCDPEvent) -> None:
        calls.append(("wildcard", event))

    dispatcher.add_handler("Page.frameNavigated", specific, session_id="S1")
    dispatcher.add_handler(None, wildcard, all_sessions=True)

    event = RawCDPEvent(params={"id": 1}, session_id="S1")
    handled = await dispatcher.dispatch("Page.frameNavigated", event)

    assert handled is True
    assert calls == [("specific", event), ("wildcard", event)]


@pytest.mark.asyncio
async def test_dispatch_returns_false_for_unhandled_event() -> None:
    dispatcher = EventDispatcher()

    handled = await dispatcher.dispatch(
        "Page.frameNavigated", RawCDPEvent(params={"id": 1})
    )

    assert handled is False


@pytest.mark.asyncio
async def test_dispatch_does_not_cross_session_boundaries() -> None:
    dispatcher = EventDispatcher()
    calls: list[RawCDPEvent] = []

    async def handler(event: RawCDPEvent) -> None:
        calls.append(event)

    dispatcher.add_handler("Network.requestWillBeSent", handler, session_id="A")

    handled = await dispatcher.dispatch(
        "Network.requestWillBeSent",
        RawCDPEvent(params={}, session_id="B"),
    )

    assert handled is False
    assert calls == []


@pytest.mark.asyncio
async def test_remove_handler_stops_future_dispatches() -> None:
    dispatcher = EventDispatcher()
    calls: list[RawCDPEvent] = []

    async def handler(event: RawCDPEvent) -> None:
        calls.append(event)

    dispatcher.add_handler("Runtime.consoleAPICalled", handler)
    dispatcher.remove_handler("Runtime.consoleAPICalled", handler)

    handled = await dispatcher.dispatch(
        "Runtime.consoleAPICalled", RawCDPEvent(params={"id": 7})
    )

    assert handled is False
    assert calls == []


@pytest.mark.asyncio
async def test_dispatch_continues_when_handler_raises(
    caplog: pytest.LogCaptureFixture,
) -> None:
    dispatcher = EventDispatcher()
    calls: list[str] = []

    async def broken(_: RawCDPEvent) -> None:
        raise RuntimeError("boom")

    async def healthy(_: RawCDPEvent) -> None:
        calls.append("healthy")

    dispatcher.add_handler("Runtime.exceptionThrown", broken)
    dispatcher.add_handler("Runtime.exceptionThrown", healthy)

    with caplog.at_level("ERROR"):
        handled = await dispatcher.dispatch(
            "Runtime.exceptionThrown", RawCDPEvent(params={"id": 1})
        )

    assert handled is True
    assert calls == ["healthy"]
    assert "failed" in caplog.text
    assert "RuntimeError: boom" in caplog.text
