# Cookbook

Complete recipes, sorted by difficulty. Each recipe is a self-contained
function that takes a connected client, so you can paste it into your own
code. The levels match the [learning path](README.md#learning-path).

| Level | Recipe |
| --- | --- |
| 1 · Commands | [Take a screenshot](#1-take-a-screenshot) |
| 1 · Commands | [Extract data with JavaScript](#2-extract-data-with-javascript) |
| 1 · Commands | [Emulate a phone](#3-emulate-a-phone) |
| 2 · Events | [Navigate and wait for the page to load](#4-navigate-and-wait-for-the-page-to-load) |
| 2 · Events | [Capture console output](#5-capture-console-output) |
| 2 · Events | [Record network traffic](#6-record-network-traffic) |
| 3 · Multiple targets | [Crawl several pages in parallel](#7-crawl-several-pages-in-parallel) |
| 4 · Advanced | [Block images and mock an API](#8-block-images-and-mock-an-api) |
| 4 · Advanced | [Test your code without a browser](#9-test-your-code-without-a-browser) |

## Setup

All recipes assume Chrome is running with remote debugging enabled (see
[First steps](01-first-steps.md#start-a-browser)) and use these helpers:

```python
import asyncio
import json
from urllib.request import urlopen

from cdpify import CdpClient


def page_url() -> str:
    """WebSocket URL of the first open tab."""
    with urlopen("http://localhost:9222/json") as response:
        targets = json.load(response)
    return next(t["webSocketDebuggerUrl"] for t in targets if t["type"] == "page")


def browser_url() -> str:
    """WebSocket URL of the browser itself, for multi-target work."""
    with urlopen("http://localhost:9222/json/version") as response:
        return json.load(response)["webSocketDebuggerUrl"]


async def run(recipe, *args) -> None:
    async with CdpClient(page_url()) as client:
        await recipe(client, *args)
```

For example: `asyncio.run(run(screenshot, "https://example.com", "page.png"))`.

## Level 1: Commands

### 1. Take a screenshot

Screenshots arrive as Base64 strings. Ask for the full scrollable page with
`capture_beyond_viewport`:

```python
import base64
from pathlib import Path

from cdpify.domains.page import LoadEventFiredEvent


async def screenshot(client: CdpClient, url: str, path: str) -> None:
    await client.page.enable()
    async with client.listen(LoadEventFiredEvent) as loaded:
        await client.page.navigate(url=url)
        await loaded.next(timeout=15)

    shot = await client.page.capture_screenshot(
        format="png",
        capture_beyond_viewport=True,
    )
    Path(path).write_bytes(base64.b64decode(shot.data))
```

`format` is typed as `Literal["jpeg", "png", "webp"]`, so a typo is caught by
your type checker before it reaches Chrome.

### 2. Extract data with JavaScript

`Runtime.evaluate` with `return_by_value=True` returns JSON-serializable
results directly as Python values:

```python
from cdpify import UNSET


async def extract_links(client: CdpClient) -> list[dict[str, str]]:
    result = await client.runtime.evaluate(
        expression="""
            [...document.querySelectorAll('a[href]')].map(a => ({
                text: a.textContent.trim(),
                href: a.href,
            }))
        """,
        return_by_value=True,
    )
    if details := result.exception_details:
        error = details.exception.description if details.exception else details.text
        raise RuntimeError(error)

    links = result.result.value
    if links is UNSET:  # e.g. the expression evaluated to `undefined`
        raise RuntimeError("Expected a JSON value")
    return links
```

`RemoteObject.value` is typed `Any | UnsetType`: JSON `null` is a valid value,
so "no value" is the `UNSET` marker, and your type checker makes you handle it.

Add `await_promise=True` to wait for an `async` expression, for example
`fetch('/api').then(r => r.json())`.

### 3. Emulate a phone

Device metrics, user agent and touch support are separate commands of the
`Emulation` domain:

```python
async def emulate_phone(client: CdpClient) -> None:
    await client.emulation.set_device_metrics_override(
        width=390,
        height=844,
        device_scale_factor=3,
        mobile=True,
    )
    await client.emulation.set_user_agent_override(
        user_agent=(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        ),
    )
    await client.emulation.set_touch_emulation_enabled(enabled=True)
```

Undo the metrics with `await client.emulation.clear_device_metrics_override()`.

## Level 2: Events

### 4. Navigate and wait for the page to load

A reusable helper that subscribes before navigating, checks the navigation
result and bounds the whole operation:

```python
from cdpify.domains.page import LoadEventFiredEvent


async def goto(client: CdpClient, url: str, timeout: float = 30) -> None:
    await client.page.enable()
    async with asyncio.timeout(timeout):
        async with client.listen(LoadEventFiredEvent) as loaded:
            navigation = await client.page.navigate(url=url)
            if navigation.error_text:
                raise RuntimeError(f"Navigation to {url} failed: {navigation.error_text}")
            await loaded.next()
```

Wait for `DomContentEventFiredEvent` instead if you do not need images and
other subresources.

### 5. Capture console output

Collect `console.*` calls while a block of code runs:

```python
from cdpify import UNSET
from cdpify.domains.runtime import ConsoleAPICalledEvent


async def console_messages(client: CdpClient, expression: str) -> list[str]:
    await client.runtime.enable()
    messages: list[str] = []

    async with client.listen(ConsoleAPICalledEvent) as events:
        await client.runtime.evaluate(expression=expression)
        while True:
            try:
                event = await events.next(timeout=0.5)
            except TimeoutError:
                break
            text = " ".join(
                str(arg.value if arg.value is not UNSET else arg.description)
                for arg in event.args
            )
            messages.append(f"[{event.type}] {text}")

    return messages
```

`await console_messages(client, "console.warn('low disk', 42)")` returns
`["[warning] low disk 42"]`.

`RemoteObject.value` can legitimately be JSON `null`, so an absent value is
`UNSET` rather than `None`; objects without a JSON value fall back to their
`description`. See [`UNSET` vs. `None`](04-timeouts-and-errors.md#unset-vs-none).

### 6. Record network traffic

Run several listeners concurrently and stop them together when the page has
loaded. Each response is matched with its final size via the request ID:

```python
from dataclasses import dataclass

from cdpify.domains.network import LoadingFinishedEvent, ResponseReceivedEvent
from cdpify.domains.page import LoadEventFiredEvent


@dataclass
class Entry:
    url: str
    status: int
    mime_type: str
    size: float = 0


async def record_traffic(client: CdpClient, url: str) -> list[Entry]:
    entries: dict[str, Entry] = {}

    async def on_response() -> None:
        async for event in client.listen(ResponseReceivedEvent):
            response = event.response
            entries[event.request_id] = Entry(
                response.url, response.status, response.mime_type
            )

    async def on_finished() -> None:
        async for event in client.listen(LoadingFinishedEvent):
            if entry := entries.get(event.request_id):
                entry.size = event.encoded_data_length

    await client.network.enable()
    await client.page.enable()
    tasks = [asyncio.create_task(on_response()), asyncio.create_task(on_finished())]
    try:
        async with client.listen(LoadEventFiredEvent) as loaded:
            await client.page.navigate(url=url)
            await loaded.next(timeout=30)
        await asyncio.sleep(1)  # give late requests a moment
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    return list(entries.values())
```

## Level 3: Multiple targets

### 7. Crawl several pages in parallel

Connect to the **browser** endpoint, open one tab per URL, and drive all tabs
concurrently through their sessions. A semaphore caps the number of open tabs:

```python
from cdpify import CdpSession
from cdpify.domains.page import LoadEventFiredEvent


async def page_title(tab: CdpSession, url: str) -> str:
    await tab.page.enable()
    async with tab.listen(LoadEventFiredEvent) as loaded:
        await tab.page.navigate(url=url)
        await loaded.next(timeout=30)
    result = await tab.runtime.evaluate(
        expression="document.title", return_by_value=True
    )
    title = result.result.value
    return title if isinstance(title, str) else ""


async def crawl(urls: list[str], max_tabs: int = 4) -> dict[str, str]:
    limit = asyncio.Semaphore(max_tabs)

    async with CdpClient(browser_url()) as browser:

        async def visit(url: str) -> tuple[str, str]:
            async with limit:
                target = await browser.target.create_target(url="about:blank")
                try:
                    tab = await browser.attach(target.target_id)
                    return url, await page_title(tab, url)
                finally:
                    await browser.target.close_target(target_id=target.target_id)

        return dict(await asyncio.gather(*(visit(url) for url in urls)))
```

```python
titles = asyncio.run(crawl(["https://example.com", "https://example.org"]))
```

Every `tab.listen()` only sees its own tab's events, so the concurrent loads
never get mixed up.

## Level 4: Advanced

### 8. Block images and mock an API

The `Fetch` domain pauses matching requests until you decide what happens to
them. Each paused request **must** be answered: continue it, fail it or
fulfill it yourself. That is why event subscriptions default to
`overflow="error"`; a silently dropped `requestPaused` event would leave a
request hanging forever.

```python
import base64
import json

from cdpify.domains.fetch import HeaderEntry, RequestPattern, RequestPausedEvent
from cdpify.domains.network import ErrorReason, ResourceType


async def intercept(client: CdpClient) -> None:
    """Handle paused requests until the subscription is cancelled."""
    async with client.listen(RequestPausedEvent) as paused:
        await client.fetch.enable(patterns=[RequestPattern(url_pattern="*")])

        async for event in paused:
            if event.resource_type is ResourceType.IMAGE:
                await client.fetch.fail_request(
                    request_id=event.request_id,
                    error_reason=ErrorReason.BLOCKED_BY_CLIENT,
                )
            elif event.request.url.endswith("/api/user"):
                body = json.dumps({"name": "Test User"}).encode()
                await client.fetch.fulfill_request(
                    request_id=event.request_id,
                    response_code=200,
                    response_headers=[
                        HeaderEntry(name="Content-Type", value="application/json")
                    ],
                    body=base64.b64encode(body).decode(),
                )
            else:
                await client.fetch.continue_request(request_id=event.request_id)
```

Run it as a background task while you navigate, and cancel it when done:

```python
interceptor = asyncio.create_task(intercept(client))
await goto(client, "https://example.com")  # from recipe 4
interceptor.cancel()
await client.fetch.disable()
```

Narrow `RequestPattern` by `resource_type` or `request_stage` to pause only the
requests you care about; every paused request costs a round trip.

Resources Chrome already holds in its in-memory cache are served without a
network request and are never paused. Intercept before the first load, or use
a fresh tab, when every request must pass through your handler.

### 9. Test your code without a browser

`CdpClient` accepts any object implementing the `Transport` protocol, so unit
tests can replace Chrome with a scripted fake. Typed results are decoded from
the fake's dictionaries exactly as from real responses:

```python
import asyncio
from collections.abc import AsyncIterator
from typing import Any

from cdpify import CdpClient, TransportEvent


class FakeTransport:
    def __init__(self, responses: dict[str, dict[str, Any]]) -> None:
        self.responses = responses
        self.sent: list[tuple[str, dict[str, Any] | None]] = []
        self._connected = False
        self._closed = asyncio.Event()

    @property
    def is_connected(self) -> bool:
        return self._connected

    async def connect(self) -> None:
        self._connected = True

    async def disconnect(self) -> None:
        self._connected = False
        self._closed.set()

    async def execute(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        session_id: str | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        self.sent.append((method, params))
        return self.responses.get(method, {})

    async def events(self) -> AsyncIterator[TransportEvent]:
        await self._closed.wait()
        return
        yield


async def test_reads_title() -> None:
    transport = FakeTransport({
        "Runtime.evaluate": {"result": {"type": "string", "value": "Hello"}},
    })
    async with CdpClient(transport=transport) as client:
        result = await client.runtime.evaluate(
            expression="document.title", return_by_value=True
        )

    assert result.result.value == "Hello"
    assert transport.sent == [
        ("Runtime.evaluate", {"expression": "document.title", "returnByValue": True})
    ]
```

The assertion on `transport.sent` also shows the wire format `cdpify`
produces from your `snake_case` call. To test event handling, have `events()`
yield `TransportEvent("Page.loadEventFired", {"timestamp": 1.0})` values. See
[Configuration and transports](05-configuration-and-transports.md#custom-transports)
for the full contract.
