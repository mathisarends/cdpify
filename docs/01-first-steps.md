# Level 1: First steps

This guide walks you from a fresh install to a working script and explains the
conventions the generated API follows.

## Install

```bash
pip install "cdpify[websocket]"
# optional: faster JSON
pip install "cdpify[websocket,orjson]"
```

`cdpify` requires Python 3.12 or newer.

## Start a browser

`cdpify` talks to a running Chrome or Chromium instance. Start it with remote
debugging enabled and a dedicated profile directory (Chrome refuses remote
debugging on your default profile):

```bash
# Linux
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/cdpify-profile

# macOS
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 --user-data-dir=/tmp/cdpify-profile

# Windows (PowerShell)
& "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  --remote-debugging-port=9222 --user-data-dir="$env:TEMP\cdpify-profile"
```

Add `--headless=new` to run without a window.

> [!TIP]
> The scripts in [`examples/`](../examples) launch Chrome with these options
> automatically. From a development checkout, run for example
> `uv run python examples/navigate.py`.

## Find a WebSocket URL

Chrome lists its debuggable targets over HTTP:

| Endpoint | Returns |
| --- | --- |
| `http://localhost:9222/json` | One entry per target (tabs, workers, …), each with a `webSocketDebuggerUrl` |
| `http://localhost:9222/json/version` | Browser info, including the browser-level `webSocketDebuggerUrl` |

- Connect to a **page URL** to control a single tab directly.
- Connect to the **browser URL** to manage many targets through
  [sessions](03-sessions.md).

```python
import json
from urllib.request import urlopen


def find_page_websocket_url() -> str:
    with urlopen("http://localhost:9222/json", timeout=5) as response:
        return next(
            target["webSocketDebuggerUrl"]
            for target in json.load(response)
            if target.get("type") == "page"
        )
```

## Your first script

```python
import asyncio

from cdpify import CdpClient
from cdpify.domains.page import LoadEventFiredEvent


async def main() -> None:
    async with CdpClient(find_page_websocket_url()) as client:
        await client.page.enable()

        async with client.listen(LoadEventFiredEvent) as loaded:
            navigation = await client.page.navigate(url="https://example.com")
            if navigation.error_text:
                raise RuntimeError(navigation.error_text)
            await loaded.next(timeout_seconds=10)

        result = await client.runtime.evaluate(
            expression="document.title",
            return_by_value=True,
        )
        print(result.result.value)


asyncio.run(main())
```

`async with CdpClient(...)` connects on entry and disconnects on exit. You can
also call `await client.connect()` and `await client.disconnect()` yourself.

## Domains and commands

Every CDP domain is a lazy property on `CdpClient` (and on
[`CdpSession`](03-sessions.md)). Domain names become `snake_case`:

| CDP | Python |
| --- | --- |
| `Page.navigate` | `client.page.navigate(...)` |
| `Runtime.evaluate` | `client.runtime.evaluate(...)` |
| `DOM.getDocument` | `client.dom.get_document(...)` |
| `IndexedDB.requestData` | `client.indexed_db.request_data(...)` |
| `LayerTree.enable` | `client.layer_tree.enable()` |

Parameters are keyword arguments in `snake_case`, and results are typed
dataclasses whose fields are `snake_case` too. `cdpify` converts to and from
CDP's `camelCase` wire format for you:

```python
# Wire: {"method": "Runtime.evaluate",
#        "params": {"expression": "1 + 1", "returnByValue": true}}
result = await client.runtime.evaluate(expression="1 + 1", return_by_value=True)
print(result.result.value)       # 2
print(result.exception_details)  # None
```

Generated methods accept only the parameters defined by CDP. Their docstrings
carry the spec's descriptions, units, defaults and experimental or deprecated
markers, so your editor's hover is often all the reference you need.

### Imports

Each domain is a package under `cdpify.domains`, named like its accessor
(`cdpify.domains.indexed_db` for `client.indexed_db`), exporting its events,
types and result models:

```python
from cdpify.domains.network import RequestWillBeSentEvent, ResourceType
from cdpify.domains.page import FrameId, LoadEventFiredEvent
```

The submodules `commands`, `events` and `types` hold the same names if you
prefer explicit paths, for example `cdpify.domains.network.events`.

### All domains

All 59 domains of the bundled specification are available:

| CDP domain | Python accessor | CDP domain | Python accessor |
| --- | --- | --- | --- |
| `Accessibility` | `accessibility` | `IndexedDB` | `indexed_db` |
| `Ads` | `ads` | `Input` | `input` |
| `Animation` | `animation` | `Inspector` | `inspector` |
| `Audits` | `audits` | `IO` | `io` |
| `Autofill` | `autofill` | `LayerTree` | `layer_tree` |
| `BackgroundService` | `background_service` | `Log` | `log` |
| `BluetoothEmulation` | `bluetooth_emulation` | `Media` | `media` |
| `Browser` | `browser` | `Memory` | `memory` |
| `CacheStorage` | `cache_storage` | `Network` | `network` |
| `Cast` | `cast` | `Overlay` | `overlay` |
| `Console` | `console` | `Page` | `page` |
| `CrashReportContext` | `crash_report_context` | `Performance` | `performance` |
| `CSS` | `css` | `PerformanceTimeline` | `performance_timeline` |
| `Debugger` | `debugger` | `Preload` | `preload` |
| `DeviceAccess` | `device_access` | `Profiler` | `profiler` |
| `DeviceOrientation` | `device_orientation` | `PWA` | `pwa` |
| `DigitalCredentials` | `digital_credentials` | `Runtime` | `runtime` |
| `DOM` | `dom` | `Schema` | `schema` |
| `DOMDebugger` | `dom_debugger` | `Security` | `security` |
| `DOMSnapshot` | `dom_snapshot` | `ServiceWorker` | `service_worker` |
| `DOMStorage` | `dom_storage` | `SmartCardEmulation` | `smart_card_emulation` |
| `Emulation` | `emulation` | `Storage` | `storage` |
| `EventBreakpoints` | `event_breakpoints` | `SystemInfo` | `system_info` |
| `Extensions` | `extensions` | `Target` | `target` |
| `FedCm` | `fed_cm` | `Tethering` | `tethering` |
| `Fetch` | `fetch` | `Tracing` | `tracing` |
| `FileSystem` | `file_system` | `WebAudio` | `web_audio` |
| `FindInPage` | `find_in_page` | `WebAuthn` | `web_authn` |
| `HeadlessExperimental` | `headless_experimental` | `WebMCP` | `web_mcp` |
| `HeapProfiler` | `heap_profiler` |  |  |

The bundled specification is refreshed weekly by CI, so this list follows
upstream Chrome.

## Enums

Named protocol enums are `StrEnum` classes. Decoded responses and events
contain enum members, including inside nested models and lists:

```python
from cdpify.domains.network import LoadingFailedEvent, NetworkEvent, ResourceType

async for event in client.listen(LoadingFailedEvent):
    assert event.__cdp_event__ is NetworkEvent.LOADING_FAILED
    if event.type is ResourceType.FETCH:
        print(event.error_text)
```

- Members behave like strings; `.value` is the original protocol value.
- Values unknown to the bundled spec (from newer Chrome versions) are
  preserved as members of the same enum, without changing its declared
  constants or iteration order.
- Anonymous enums are typed as `Literal[...]`, for example
  `Literal["jpeg", "png"]`, and accept plain strings.
- Open string fields such as EventSource's server-defined `event_name` stay
  plain `str`.

## Type aliases

Aliases such as `FrameId`, `NodeId` or `TargetFilter` are declared with
Python's `type` statement. Use them in annotations and pass ordinary values:

```python
from cdpify.domains.page import FrameId

frame_id: FrameId = "F1"
```

Aliases are not constructors or runtime classes: write `"F1"`, not
`FrameId("F1")`, and use `isinstance(frame_id, str)` for runtime checks.

## Calling commands by name

For commands that are missing from the generated API, for example
brand-new experimental ones, use `execute()` with the wire name and a
`camelCase` parameter dictionary. The result is the raw response dictionary:

```python
result = await client.execute(
    "Runtime.evaluate",
    {"expression": "1 + 1", "returnByValue": True},
)
print(result["result"]["value"])
```

To turn a raw dictionary into a typed model, see
[`decode_cdp`](04-timeouts-and-errors.md#decoding-raw-payloads).

## Next

**Level 2: [Events](02-events.md).** Wait for page loads, watch network
traffic and stream anything the browser reports.

Want to see more complete programs first? Try recipes 1 to 3 of the
[cookbook](cookbook.md).
