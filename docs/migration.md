# Migration guide

This page lists the changes you have to make in your code when upgrading. For
everything else that changed, see the [changelog](../CHANGELOG.md).

## 0.5.x → 0.6.0

| Area | What to change |
| --- | --- |
| Domain packages | Use the client accessor's spelling in imports. For example, `cdpify.domains.indexeddb` becomes `cdpify.domains.indexed_db` and `cdpify.domains.layertree` becomes `cdpify.domains.layer_tree`. See [all domains](01-first-steps.md#all-domains) for the current spellings. |
| Generated names | Rename `network.set_blocked_ur_ls()` and `NetworkCommand.SET_BLOCKED_UR_LS` to `network.set_blocked_urls()` and `NetworkCommand.SET_BLOCKED_URLS`. Import `LifecycleEvent` from `cdpify.domains.page` in place of `LifecycleEventEvent`. |
| Binding sessions | Replace `client.session(session_id)` with `client.bind_session(session_id)` to bind an existing session ID locally. Use `await client.attach(target_id)` to create a session for a target ID. |
| Session lifetime | Catch `CDPSessionClosedError` for new commands or subscriptions on a detached session. It inherits from `CDPConnectionError`. After a reconnect, attach or bind a fresh session and reacquire any cached domain objects. |
| Timeout keywords | Rename library keywords `timeout`, `default_timeout`, `open_timeout` and `close_timeout` to `timeout_seconds`, `default_timeout_seconds`, `open_timeout_seconds` and `close_timeout_seconds`. Update custom `Transport.execute()` signatures as well. |
| Raw `execute()` | Change `client.execute(m, p, sid, t)` to `client.execute(m, p, session_id=sid, timeout_seconds=t)`. Change `session.execute(m, p, t)` to `session.execute(m, p, timeout_seconds=t)`. |

### Timeouts in detail

Generated methods accept only CDP parameters. A CDP parameter named `timeout`
keeps its protocol meaning and units, often milliseconds. Client-side deadlines
work like this:

```python
client = CdpClient(ws_url, default_timeout_seconds=30.0)   # default for every command

async with asyncio.timeout(2):                     # one call or a group of calls
    await client.page.navigate(url="https://example.com")

await client.execute("Page.reload", timeout_seconds=5)     # raw call, seconds
await client.execute("Page.reload", timeout_seconds=None)  # raw call, no deadline
```

### Bundled protocol changes

- Remove calls to `browser.add_privacy_sandbox_enrollment_override()` and
  imports of its generated command or parameter types. Chromium removed the
  underlying `Browser.addPrivacySandboxEnrollmentOverride` command.
- Remove references to `browser.PermissionType.TOP_LEVEL_STORAGE_ACCESS`,
  `dom.PseudoType.OVERSCROLL_BACKDROP`, and
  `page.PermissionsPolicyFeature.BROWSING_TOPICS` and `.INTEREST_COHORT`.
- In WebMCP, use the `tool_id` reported by the browser when constructing `Tool`
  and `RemovedTool` values. Supply exactly one of `tool_id` and `tool_name`
  to `web_mcp.invoke_tool()`. `tool_name` is deprecated and optional on that
  command, and `ToolInvokedEvent` may omit the name or ID. With strict decoding,
  older Chrome builds that omit the newly required `toolId` on a `Tool` or
  `RemovedTool` payload raise `CDPDecodeError`.

## 0.4.x → 0.5.0

| Area | What to change |
| --- | --- |
| Error imports | `cdpify.exceptions` is removed. Import from `cdpify.error` or from `cdpify` directly. |
| Optional `Any` fields | Use `UNSET` to omit a value. `None` now sends JSON `null`. Ordinary optional scalar fields still treat `None` as omitted. See [`UNSET` vs. `None`](04-timeouts-and-errors.md#unset-vs-none). |
| Missing required fields | Responses and events lacking required fields now raise `CDPDecodeError`. For the old tolerant behavior, decode manually with `decode_cdp(Model, payload, strict=False)`. |
| Command deadlines | Configure `default_timeout` on `CdpClient`; it now applies to every transport and covers sending as well as receiving. `WebSocketTransport` no longer accepts `default_timeout`. Use `asyncio.timeout()` for individual calls. |
| Bounded event buffers | Overflow now raises `CDPEventOverflowError` by default. Pass `overflow="drop_oldest"` to keep lossy buffering. Unbounded buffers (the default) are unaffected. |
| WebSocket compression | Off by default. Pass `compression="deflate"` to enable it. |

## 0.3.x → 0.4.0

0.4.0 renamed `Client` to `CdpClient` and `CDPSession` to `CdpSession`, made
named enums `StrEnum`s, switched type aliases to `type` statements, renamed
exceptions to `*Error` and changed `listen()` to take only the event class. The
[0.4.0 changelog](../CHANGELOG.md#040---2026-10-25) has before/after examples for
each change.
