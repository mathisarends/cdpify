# Migration guide

This page lists the changes you have to make in your code when upgrading. For
everything else that changed, see the [changelog](../CHANGELOG.md).

## Unreleased (after 0.5.0)

| Area | What to change |
| --- | --- |
| Domain packages | Multiword domain packages match their accessors, e.g. `cdpify.domains.indexed_db` and `cdpify.domains.layer_tree`. |
| Renamed members | `Network.setBlockedURLs` is `network.set_blocked_urls(...)` and `NetworkCommand.SET_BLOCKED_URLS`. Import `LifecycleEvent` from `cdpify.domains.page` for `Page.lifecycleEvent`. |
| Detached sessions | Commands and new subscriptions on a detached session raise `CDPSessionClosedError`. Sessions do not survive a reconnect; attach or bind again. |
| Binding sessions | `client.session(session_id)` is now `client.bind_session(session_id)`. It still only binds locally. To attach to a target ID, use `await client.attach(target_id)`. |
| Raw `execute()` | Arguments after `method` and `params` are keyword-only. `client.execute(m, p, sid, t)` becomes `client.execute(m, p, session_id=sid, timeout=t)`; `session.execute(m, p, t)` becomes `session.execute(m, p, timeout=t)`. |

## 0.4.x → 0.5.0

| Area | What to change |
| --- | --- |
| Error imports | `cdpify.exceptions` is removed. Import from `cdpify.error` or from `cdpify` directly. |
| Optional `Any` fields | Use `UNSET` to omit a value. `None` now sends JSON `null`. Ordinary optional scalar fields still treat `None` as omitted. See [`UNSET` vs. `None`](04-timeouts-and-errors.md#unset-vs-none). |
| Missing required fields | Responses and events lacking required fields now raise `CDPDecodeError`. For the old tolerant behavior, decode manually with `decode_cdp(Model, payload, strict=False)`. |
| Command deadlines | Configure `default_timeout` on `CdpClient`; it now applies to every transport and covers sending as well as receiving. `WebSocketTransport` no longer accepts `default_timeout`. Use `asyncio.timeout()` for individual calls. |
| Bounded event buffers | Overflow now raises `CDPEventOverflowError` by default. Pass `overflow="drop_oldest"` to keep lossy buffering. Unbounded buffers (the default) are unaffected. |
| WebSocket compression | Off by default. Pass `compression="deflate"` to enable it. |

### Timeouts in detail

Generated methods accept only CDP parameters. A CDP parameter named `timeout`
keeps its protocol meaning and units, often milliseconds. Client-side deadlines
work like this:

```python
client = CdpClient(ws_url, default_timeout=30.0)   # default for every command

async with asyncio.timeout(2):                     # one call or a group of calls
    await client.page.navigate(url="https://example.com")

await client.execute("Page.reload", timeout=5)     # raw call, seconds
await client.execute("Page.reload", timeout=None)  # raw call, no deadline
```

## 0.3.x → 0.4.0

0.4.0 renamed `Client` to `CdpClient` and `CDPSession` to `CdpSession`, made
named enums `StrEnum`s, switched type aliases to `type` statements, renamed
exceptions to `*Error` and changed `listen()` to take only the event class. The
[0.4.0 changelog](../CHANGELOG.md#040---2026-10-25) has before/after examples for
each change.
