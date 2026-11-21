# Level 3: Multiple targets

A Chrome instance hosts many *targets*: tabs, iframes, service workers and
more. With a browser-level connection you can control all of them over one
WebSocket using CDP's flat session mode. In `cdpify` each attached target is a
`CdpSession`.

## Connect to the browser

Use the browser-level URL from `http://localhost:9222/json/version`:

```python
import json
from urllib.request import urlopen

with urlopen("http://localhost:9222/json/version", timeout=5) as response:
    browser_ws_url = json.load(response)["webSocketDebuggerUrl"]
```

## Attach to a target

`await client.attach(target_id)` sends `Target.attachToTarget` with
`flatten=True` and returns a `CdpSession` bound to the new session ID:

```python
from cdpify import CdpClient

async with CdpClient(browser_ws_url) as client:
    created = await client.target.create_target(url="about:blank")
    tab = await client.attach(created.target_id)

    await tab.page.enable()
    await tab.page.navigate(url="https://example.com")
    await tab.runtime.evaluate(expression="console.log('Hello from cdpify')")
```

A `CdpSession` has the same domain properties as `CdpClient` (`tab.page`,
`tab.network`, …), plus `listen()`, `listen_raw()`, `execute()` and the
read-only `session_id` property. Everything it sends is routed to its target.

## Bind an existing session

If you already know a session ID, for example from a
`Target.attachedToTarget` event or auto-attach, create a view without sending
any command:

```python
tab = client.bind_session(session_id)
```

`bind_session()` is purely local and cheap; call it as often as you like.

## Concurrency

Session views are immutable and safe to use from concurrent tasks. Commands on
different sessions run in parallel over the same connection:

```python
tab_a = client.bind_session(session_a)
tab_b = client.bind_session(session_b)

title_a, title_b = await asyncio.gather(
    tab_a.runtime.evaluate(expression="document.title", return_by_value=True),
    tab_b.runtime.evaluate(expression="document.title", return_by_value=True),
)
```

## Session events

`tab.listen(Event)` yields only that session's events, and
`client.listen_all(Event)` yields events from every scope together with their
session ID. When Chrome detaches a session, its subscriptions end. See
[Events](02-events.md#scopes-root-session-all) for details.

## When a session ends

When Chrome reports that a session detached (the tab closed, or you called
`Target.detachFromTarget`):

- existing subscriptions of that session deliver their buffered events and then
  end;
- new subscriptions and commands on that session raise
  `CDPSessionClosedError` locally, without a round trip to Chrome.

Session views belong to one connection. After the client reconnects, attach
or bind the session again on the new connection.

```python
from cdpify import CDPSessionClosedError

try:
    await tab.page.reload()
except CDPSessionClosedError:
    tab = await client.attach(target_id)  # re-attach if the target still exists
```

## Routing vs. `sessionId` parameters

Session routing is transport metadata, not a command parameter, so generated
methods never accept an extra routing `session_id`. Parameters that the CDP
specification itself calls `sessionId`, such as on
`Target.detachFromTarget`, stay regular typed parameters.

For raw commands, the root client takes an optional routing session ID, while a
session's `execute()` is always bound to its own session:

```python
await client.execute("Page.enable", session_id=session_a)
await tab.execute("Runtime.evaluate", {"expression": "1 + 1"})
```

## Timeouts

Sessions inherit the client's `default_timeout`. See
[Timeouts and errors](04-timeouts-and-errors.md#timeouts).

## Next

**Level 4: [Timeouts and errors](04-timeouts-and-errors.md).** Put deadlines
on calls and handle everything that can go wrong. A complete multi-tab crawler
is in the [cookbook](cookbook.md#level-3-multiple-targets).
