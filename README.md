# cdpify

🚀 **An async, typed Python client for the Chrome DevTools Protocol.**

`cdpify` turns the Chrome DevTools Protocol (CDP) into a Pythonic, IDE-friendly
API. Commands, results, events, and protocol types are generated from the
official CDP specifications, so you get autocomplete and typed responses
without working with raw JSON messages.

## Contents

- [Why cdpify?](#why-cdpify)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Supported domains](#supported-domains)
- [Listening for events](#listening-for-events)
- [Working with target sessions](#working-with-target-sessions)
- [Configuration](#configuration)
- [Development](#development)
- [Resources](#resources)

## Why cdpify?

- **Typed by default** — generated models for commands, results, events, and
  shared protocol types
- **Complete domain coverage** — access all 59 generated CDP domains through
  properties such as `client.page`, `client.network`, and `client.runtime`
- **Async throughout** — transport-neutral core with an optional WebSocket
  implementation
- **Typed event streams** — consume CDP events with async iterators
- **Multi-target support** — use immutable, concurrency-safe session views
- **Low-level protocol access** — execute any CDP method through `execute()`
  when needed

## Installation

```bash
pip install "cdpify[websocket]"
```

Requires Python 3.12 or newer. The WebSocket extra provides the recommended
default transport used by `CdpClient(url)`. Install `cdpify` without an extra when
supplying your own `Transport` implementation.

Install the generator dependencies only when regenerating protocol modules:

```bash
pip install "cdpify[generator]"
```

## Quick start

Start Chrome or Chromium with remote debugging enabled, then obtain a page's
`webSocketDebuggerUrl` from `http://localhost:9222/json`.

```python
import asyncio
import json
from urllib.request import urlopen

from cdpify import CdpClient


def get_websocket_url() -> str:
    with urlopen("http://localhost:9222/json", timeout=5) as response:
        return json.load(response)[0]["webSocketDebuggerUrl"]


async def main() -> None:
    ws_url = get_websocket_url()

    async with CdpClient(ws_url) as client:
        await client.page.navigate(url="https://example.com")

        result = await client.runtime.evaluate(
            expression="document.title",
            return_by_value=True,
        )
        print(result.result.value)


asyncio.run(main())
```

Domains are available as lazy properties on `CdpClient`. Parameters use
Python's `snake_case`; `cdpify` handles conversion to and from CDP's wire format.

## Supported domains

The generated client currently includes all 59 domains from the bundled CDP
specifications. Each domain is available as a lazy property on `CdpClient` and
`CdpSession`:

| CDP domain | Python accessor | CDP domain | Python accessor |
| --- | --- | --- | --- |
| `Accessibility` | `client.accessibility` | `IndexedDB` | `client.indexed_db` |
| `Ads` | `client.ads` | `Input` | `client.input` |
| `Animation` | `client.animation` | `Inspector` | `client.inspector` |
| `Audits` | `client.audits` | `IO` | `client.io` |
| `Autofill` | `client.autofill` | `LayerTree` | `client.layer_tree` |
| `BackgroundService` | `client.background_service` | `Log` | `client.log` |
| `BluetoothEmulation` | `client.bluetooth_emulation` | `Media` | `client.media` |
| `Browser` | `client.browser` | `Memory` | `client.memory` |
| `CacheStorage` | `client.cache_storage` | `Network` | `client.network` |
| `Cast` | `client.cast` | `Overlay` | `client.overlay` |
| `Console` | `client.console` | `Page` | `client.page` |
| `CrashReportContext` | `client.crash_report_context` | `Performance` | `client.performance` |
| `CSS` | `client.css` | `PerformanceTimeline` | `client.performance_timeline` |
| `Debugger` | `client.debugger` | `Preload` | `client.preload` |
| `DeviceAccess` | `client.device_access` | `Profiler` | `client.profiler` |
| `DeviceOrientation` | `client.device_orientation` | `PWA` | `client.pwa` |
| `DigitalCredentials` | `client.digital_credentials` | `Runtime` | `client.runtime` |
| `DOM` | `client.dom` | `Schema` | `client.schema` |
| `DOMDebugger` | `client.dom_debugger` | `Security` | `client.security` |
| `DOMSnapshot` | `client.dom_snapshot` | `ServiceWorker` | `client.service_worker` |
| `DOMStorage` | `client.dom_storage` | `SmartCardEmulation` | `client.smart_card_emulation` |
| `Emulation` | `client.emulation` | `Storage` | `client.storage` |
| `EventBreakpoints` | `client.event_breakpoints` | `SystemInfo` | `client.system_info` |
| `Extensions` | `client.extensions` | `Target` | `client.target` |
| `FedCm` | `client.fed_cm` | `Tethering` | `client.tethering` |
| `Fetch` | `client.fetch` | `Tracing` | `client.tracing` |
| `FileSystem` | `client.file_system` | `WebAudio` | `client.web_audio` |
| `FindInPage` | `client.find_in_page` | `WebAuthn` | `client.web_authn` |
| `HeadlessExperimental` | `client.headless_experimental` | `WebMCP` | `client.web_mcp` |
| `HeapProfiler` | `client.heap_profiler` |  |  |

## Listening for events

Pass a generated event class to `listen()`. The returned subscription is an
async iterator of typed events:

```python
from cdpify.domains.network.events import RequestWillBeSentEvent


await client.network.enable()

async for event in client.listen(RequestWillBeSentEvent):
    print(event.request.method, event.request.url)
```

The subscription is registered as soon as `listen()` is called, and events are
buffered until you read them. To wait for an event that your own command
triggers, subscribe first and then send the command:

```python
from cdpify.domains.page.events import LoadEventFiredEvent


async with client.listen(LoadEventFiredEvent) as events:
    await client.page.navigate(url="https://example.com")
    await events.next(timeout=10)
```

Leaving the `async with` block unsubscribes. A stream also ends when the client
disconnects; `events.next()` then raises `CDPStreamClosedError`. The optional
`timeout` on `listen()` limits how long each read waits and raises
`TimeoutError` when it expires.

`client.listen()` yields only events from the root connection. A session view
applies the same rule to its bound target:

```python
tab = client.session("session-id")

async for event in tab.listen(RequestWillBeSentEvent):
    # This stream contains events from this session only.
    print(event.request.url)
```

To observe the root connection and all attached sessions together, use
`listen_all()`. Routing metadata is returned separately from the generated CDP
event model:

```python
async for received in client.listen_all(RequestWillBeSentEvent):
    print(received.session_id, received.value.request.url)
```

`received.session_id` is `None` for a root event. Generated event dataclasses
contain only fields defined by the CDP specification, plus their CDP name in
`__cdp_event__`. To listen with your own dataclass, pass the name explicitly:
`client.listen(MyEvent, event_name="Page.loadEventFired")`.

## Working with target sessions

Attach to a target in flat mode and create an immutable session view with
`client.session()`. Every generated command on that view is routed to the bound
session:

```python
from cdpify import CdpClient


async with CdpClient(browser_ws_url) as root_client:
    attached = await root_client.target.attach_to_target(
        target_id="target-id",
        flatten=True,
    )
    tab = root_client.session(attached.session_id)

    await tab.page.enable()
    await tab.runtime.evaluate(expression="console.log('Hello from CDP')")
```

There is no mutable "active session". Create one view per attached target and
use them safely from concurrent tasks:

```python
import asyncio


tab_a = root_client.session(session_a)
tab_b = root_client.session(session_b)

await asyncio.gather(
    tab_a.runtime.evaluate(expression="document.title"),
    tab_b.runtime.evaluate(expression="document.title"),
)
```

Session routing is transport metadata, not a generated command parameter.
Generated methods therefore never accept an additional routing `session_id`.
A real `sessionId` declared by the CDP specification remains a normal typed
parameter. For low-level access, `root_client.execute()` optionally accepts a
session ID, while `tab.execute()` is always bound and cannot be overridden:

```python
await root_client.execute("Page.enable", session_id=session_a)
await tab.execute("Runtime.evaluate", {"expression": "1 + 1"})
```

## Configuration

```python
client = CdpClient(
    url="ws://localhost:9222/devtools/browser/...",
    additional_headers={"Authorization": "Bearer token"},
    max_frame_size=100 * 1024 * 1024,
    default_timeout=30.0,
)
```

For another transport protocol, implement the exported `Transport` protocol
and inject it directly:

```python
from cdpify import CdpClient

client = CdpClient(transport=my_transport)
```

For methods not covered by the generated API, use the low-level escape hatch:

```python
result = await client.execute(
    "Runtime.evaluate",
    {"expression": "1 + 1", "returnByValue": True},
)
```

### When Chrome deviates from the spec

Chrome does not always send every field the protocol marks as required.
Instead of failing, cdpify logs a warning on the `cdpify.codec` logger and
sets the missing field to `None`, even if its type says otherwise. Unknown
fields from newer Chrome versions are ignored.

Deprecated CDP commands still work but emit a `DeprecationWarning`. Use
Python's warning filters to silence them or turn them into errors:

```python
import warnings

warnings.filterwarnings(
    "ignore", category=DeprecationWarning, message=r"\w+\.\w+ is deprecated"
)
```

## Development

Install the project and its development dependencies with
[uv](https://docs.astral.sh/uv/):

```bash
uv sync --dev
uv run pytest
uv run ruff check . --exclude cdpify/domains
```

To download the latest protocol definitions and regenerate all domain clients:

```bash
uv run python -m cdpify.generator
```

Generate only selected domains by repeating `--domain`:

```bash
uv run python -m cdpify.generator --domain Page --domain Runtime
```

Use `--spec-dir` and `--output-dir` to override where downloaded specifications
and generated modules are written.

The generated output lives in `cdpify/domains/` and should not be edited by
hand. The repository also refreshes the upstream specification automatically
once a week and opens a pull request when generated code changes.

## Resources

- [Chrome DevTools Protocol documentation](https://chromedevtools.github.io/devtools-protocol/)
- [Chrome DevTools Protocol repository](https://github.com/ChromeDevTools/devtools-protocol)
- [Examples](examples)

The code-generation approach was inspired by
[`cdp-use`](https://github.com/browser-use/cdp-use).
