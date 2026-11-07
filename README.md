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

For faster JSON encoding and decoding in the WebSocket transport, install the
optional `orjson` extra as well:

```bash
pip install "cdpify[websocket,orjson]"
```

The transport automatically uses `orjson` when available and otherwise uses
Python's standard `json` module. Outgoing WebSocket messages remain text frames.

Generated methods expose only CDP parameters. Parameter docstrings preserve
the spec's units, defaults and experimental/deprecated markers.

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

Named protocol enums use `StrEnum`, so typed code can use constants such as
`ResourceType.FETCH` or `CookieOperation.SET_COOKIE`. Decoded responses and
events contain enum members, including in nested models and lists:

```python
from cdpify.domains.network import LoadingFailedEvent, NetworkEvent, ResourceType

async for event in client.listen(LoadingFailedEvent):
    assert event.__cdp_event__ is NetworkEvent.LOADING_FAILED
    if event.type is ResourceType.FETCH:
        print(event.error_text)
```

Enum members work as strings and expose the original protocol value through
`.value`. Unknown values from newer Chrome versions are preserved as members
of the same enum without changing its declared constants or iteration.
Anonymous enum annotations such as `Literal["jpeg", "png"]` still accept direct
strings. Open string fields, including EventSource's server-defined
`event_name`, remain strings.

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

An incoming event is decoded once per event class, when the first listener
reads it. Matching `listen()`, `CdpSession.listen()`, and `listen_all()`
subscriptions share that model (`received.value` for `listen_all()`). Treat
event data as read-only: changing a shared model also changes what other
listeners see. Make a deep copy when you need your own mutable instance:

```python
from copy import deepcopy

owned_event = deepcopy(event)
```

Different incoming messages and different event classes have separate cached
models. Unread events are not decoded. A cache is released when the last
subscription has read or discarded the incoming event.

### Limiting buffered events

Set `max_queue_size` on `CdpClient` to limit each listener's buffer. The default,
`0`, is unlimited. A bounded buffer defaults to `overflow="error"`: if it fills,
that subscription ends and its next read raises `CDPEventOverflowError`. Other
subscriptions and command responses continue normally. This makes event loss
explicit for protocols such as `Fetch.requestPaused` that require a response.

For a stream where loss is acceptable, select `overflow="drop_oldest"`:

```python
client = CdpClient(ws_url, max_queue_size=256, overflow="drop_oldest")

async with client:
    async with client.listen(RequestWillBeSentEvent, max_queue_size=32) as events:
        event = await events.next(timeout=10)
        print(events.dropped_events)
```

The same options apply to `listen_all()`, `CdpSession.listen()` and raw streams.
Each listener can override both the limit and overflow policy. Passing `0`
disables its limit. `events.dropped_events` counts discarded events. Disconnect
drains healthy buffers; explicit closure and overflow errors release them.

### Raw events

Use raw subscriptions for events outside the generated spec, or to inspect wire
parameter dictionaries without constructing typed models:

```python
async with tab.listen_raw("Future.event") as events:
    event = await events.next(timeout=5)
    print(event.method, event.session_id, event.params)
```

`client.listen_raw()` covers the root, `tab.listen_raw()` one session, and
`client.listen_all_raw()` every scope. Omitting the method matches every event
in that scope. Subscriptions register immediately and share the same lifetime,
buffering and read-only data rules as typed streams.

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
    max_queue_size=256,
    overflow="error",
    compression=None,
    open_timeout=10.0,
    close_timeout=10.0,
)
```

WebSocket compression is off by default to reduce local CPU work and latency.
Set `compression="deflate"` when saving network bandwidth is preferable.
`additional_headers`, `max_frame_size`, `compression`, `open_timeout` and
`close_timeout` configure the URL-based WebSocket transport. Supplied custom
transports own their connection settings.

### Timeouts

`default_timeout` is a total command budget in seconds, including sending and
waiting for the response. It applies to root commands and session commands,
including custom transports. `None` disables the default.

For one call, or a group of calls, use Python's normal timeout context:

```python
async with asyncio.timeout(2):
    result = await client.runtime.evaluate(expression="1 + 1")
```

A client deadline raises `CDPTimeoutError`; a shorter outer `asyncio.timeout()`
raises the built-in `TimeoutError`. Both release the pending local request.
Cancelling the wait does not automatically cancel work in Chrome.

CDP parameters retain the spec's units. For example, `Runtime.evaluate(timeout=...)`
limits execution inside Chrome in **milliseconds**; it is not the client budget.
The raw `execute()` escape hatch also accepts `timeout=seconds`: omit it to
inherit the client default or pass `None` to disable the deadline for that call.

### Custom transports

For another transport protocol, implement the exported `Transport` protocol
and inject it directly:

```python
from cdpify import CdpClient

client = CdpClient(transport=my_transport)
```

Custom transports can optionally implement `CallbackTransport` from
`cdpify.transport` to deliver events directly to the client. The default
WebSocket transport uses this path to avoid an intermediate event queue.
Transports that implement only `Transport.events()` continue to work.

When using `WebSocketTransport.events()` directly, its `max_queue_size` option
sets the limit on its transport buffer with the same overflow policies. A
client-supplied custom transport manages its own transport buffer limits.
`WebSocketTransport` has no default command timeout; standalone calls can pass
`execute(timeout=seconds)`. In the `Transport` contract, `timeout=None` means no
deadline and cancellation releases resources associated with that request.

For methods not covered by the generated API, use the low-level escape hatch:

```python
result = await client.execute(
    "Runtime.evaluate",
    {"expression": "1 + 1", "returnByValue": True},
)
```

### Generated type aliases

Generated aliases such as `FrameId`, `NodeId`, and `TargetFilter` use Python's
`type` statement. Use them in annotations and pass ordinary Python values:

```python
from cdpify.domains.page import FrameId

frame_id: FrameId = "F1"
```

Aliases are not constructors or runtime classes. Use `"F1"` directly rather
than `FrameId("F1")`, and `isinstance(frame_id, str)` for a runtime check.

### When Chrome deviates from the spec

Missing required fields raise `CDPDecodeError` with `model_type`,
`missing_fields` and the enclosing wire-field `path`. Unknown fields are ignored
and future enum values remain supported. Decoding checks required field
presence; it does not perform full schema validation of primitive values.

For a deliberately tolerant decode, use `decode_cdp(Model, payload, strict=False)`.
This fills missing required fields with `None` and logs a warning, including
nested models. When necessary, fetch the raw result with `execute()` and decode
it explicitly with this policy.

### Omitted values and JSON null

Optional scalar parameters still use `None` to mean omitted. Optional `Any`
fields use `UNSET` because JSON null is itself a valid value:

```python
from cdpify import UNSET, encode_cdp
from cdpify.domains.runtime import CallArgument

assert encode_cdp(CallArgument()) == {}
assert encode_cdp(CallArgument(value=None)) == {"value": None}
assert CallArgument().value is UNSET
```

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
uv run pyright
uv run python scripts/check_generated.py
```

Use `uv sync --dev --extra orjson` and `uv run --extra orjson pytest` to include
the optional backend. CI installs this extra and tests both JSON backends on
Ubuntu, Windows, and macOS with Python 3.12, 3.13, and 3.14.

Run real Chrome coverage with `uv run --extra orjson pytest -m integration`.
These tests launch an isolated headless browser. Set `CHROME_PATH` to select its
executable. Integration tests are excluded from the default unit-test run.

CI also checks the complete library and a public API sample with Pyright,
verifies generated-code drift, and runs the integration suite against Chrome.
Regenerate from the bundled specs with `uv run python scripts/check_generated.py --write`.

Run reproducible microbenchmarks with:

```bash
uv run python benchmarks/runtime.py
uv run --extra orjson python benchmarks/runtime.py --page-url ws://localhost:9222/devtools/page/...
```

Output is JSON with environment metadata and timings for encoding, decoding,
typed calls and dispatch to several listener counts. An optional page endpoint
adds real small-message and 1-MiB round trips, including p50 and p95 latency.
The large case sends and receives a seeded Base64 payload. Add
`--compression deflate` to compare compression on the same machine; installing
or omitting the `orjson` extra selects the JSON backend. Timings are diagnostic
and are not used as flaky CI pass/fail thresholds.

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
