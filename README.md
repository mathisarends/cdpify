# cdpify

**Fully typed, Pythonic access to the Chrome DevTools Protocol.**

The Chrome DevTools Protocol (CDP) is a JSON-over-WebSocket API with hundreds
of commands and events. Speaking it by hand means stringly-typed method names,
`camelCase` dictionaries and digging through docs for every field.

`cdpify` generates a typed Python API from the official CDP specification.
Every command is a method, every parameter a keyword argument, every result
and event a dataclass, and your editor knows all of them.

<table>
<tr><th>Raw CDP</th><th>cdpify</th></tr>
<tr>
<td>

```python
await ws.send(json.dumps({
    "id": 1,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.title",
        "returnByValue": True,
    },
}))
reply = json.loads(await ws.recv())
# hope it's the right id, hope the
# keys are spelled right…
title = reply["result"]["result"]["value"]
```

</td>
<td>

```python
result = await client.runtime.evaluate(
    expression="document.title",
    return_by_value=True,
)
title = result.result.value
```

</td>
</tr>
</table>

- **Typed end to end.** Arguments, results, events and nested protocol types
  are generated dataclasses, enums and aliases. Autocomplete, hover docs and
  Pyright/mypy checks work out of the box.
- **Pythonic.** `snake_case` names, keyword arguments, `async with`,
  `async for`, `StrEnum`s and regular exceptions. `cdpify` converts to and from
  the `camelCase` wire format for you.
- **Complete.** All 59 CDP domains, regenerated weekly from upstream Chrome.
  The spec's descriptions, units and deprecation markers land in the
  docstrings.
- **Lean.** No required dependencies; the WebSocket transport and `orjson`
  speedups are optional extras.

## Installation

```bash
pip install "cdpify[websocket]"
```

Requires Python 3.12+. Add the `orjson` extra for faster JSON
(`pip install "cdpify[websocket,orjson]"`).

## Quick start

Start Chrome with remote debugging enabled:

```bash
chrome --remote-debugging-port=9222 --user-data-dir=/tmp/cdpify-profile
```

Then connect to a tab and drive it:

```python
import asyncio
import json
from urllib.request import urlopen

from cdpify import CdpClient


def page_url() -> str:
    with urlopen("http://localhost:9222/json") as response:
        targets = json.load(response)
    return next(t["webSocketDebuggerUrl"] for t in targets if t["type"] == "page")


async def main() -> None:
    async with CdpClient(page_url()) as client:
        await client.page.navigate(url="https://example.com")

        result = await client.runtime.evaluate(
            expression="document.title",
            return_by_value=True,
        )
        print(result.result.value)


asyncio.run(main())
```

## Core API at a glance

Almost everything you do with `cdpify` uses these few building blocks:

| You want to… | API |
| --- | --- |
| Connect | `async with CdpClient(ws_url) as client:` |
| Send a command | `await client.<domain>.<command>(**params)`, e.g. `client.page.navigate(url=...)` |
| Wait for one event | `async with client.listen(Event) as sub:` … `await sub.next(timeout=10)` |
| Stream events | `async for event in client.listen(Event):` |
| Control another tab | `tab = await client.attach(target_id)`, then `tab.page`, `tab.listen(...)` |
| Limit how long a call may take | `async with asyncio.timeout(5):` |
| Call something not in the spec | `await client.execute("Domain.method", {...})` |

### Commands

Domains are properties, commands are methods, results are dataclasses:

```python
document = await client.dom.get_document()
heading = await client.dom.query_selector(node_id=document.root.node_id, selector="h1")
html = await client.dom.get_outer_html(node_id=heading.node_id)
print(html.outer_html)
```

### Events

Subscribe with a generated event class and iterate. Subscriptions buffer from
the moment they are created, so subscribe first and then trigger the event:

```python
from cdpify.domains.page import LoadEventFiredEvent

await client.page.enable()
async with client.listen(LoadEventFiredEvent) as loaded:
    await client.page.navigate(url="https://example.com")
    await loaded.next(timeout=10)
```

```python
from cdpify.domains.network import ResponseReceivedEvent

await client.network.enable()
async for event in client.listen(ResponseReceivedEvent):
    print(event.response.status, event.response.url)
```

### Sessions

Connect to the browser once and drive many targets concurrently:

```python
target = await client.target.create_target(url="https://example.org")
tab = await client.attach(target.target_id)

await tab.page.enable()
shot = await tab.page.capture_screenshot(format="png")
```

### Errors

Failures are ordinary exceptions:

```python
from cdpify import CDPCommandError

try:
    await client.dom.query_selector(node_id=-1, selector="h1")
except CDPCommandError as error:
    print(error.method, error.code, error.message)
```

## Documentation

The docs are a learning path: each level builds on the previous one.

| Level | Guide | You learn |
| --- | --- | --- |
| 1 | [First steps](docs/01-first-steps.md) | Connecting, commands, naming, enums, types |
| 2 | [Events](docs/02-events.md) | Subscriptions, timeouts, scopes, buffering |
| 3 | [Multiple targets](docs/03-sessions.md) | Attaching to tabs, sessions, concurrency |
| 4 | [Timeouts and errors](docs/04-timeouts-and-errors.md) | Deadlines, error types, decoding, `UNSET` |
| 5 | [Configuration and transports](docs/05-configuration-and-transports.md) | All client options, custom transports |
| ★ | [Cookbook](docs/cookbook.md) | Complete recipes, from screenshots to request interception |

Also: the [migration guide](docs/migration.md), the
[development guide](docs/development.md), runnable [examples](examples) and the
[changelog](CHANGELOG.md).

## Resources

- [Chrome DevTools Protocol reference](https://chromedevtools.github.io/devtools-protocol/)
- [CDP specification repository](https://github.com/ChromeDevTools/devtools-protocol)

The code-generation approach was inspired by
[`cdp-use`](https://github.com/browser-use/cdp-use).
