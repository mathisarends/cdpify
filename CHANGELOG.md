# Changelog

All notable changes to this project are documented here.
Breaking changes are listed first in each release.

## [Unreleased]

### Breaking changes

- Named protocol enums are now `StrEnum` subclasses instead of `Literal`
  aliases. Use constants such as `ResourceType.FETCH` and
  `CookieOperation.SET_COOKIE` in typed code. `decode_cdp` returns enum members,
  including in nested models and collections. Unknown strings from newer CDP
  versions remain instances of the corresponding enum with their original
  `.value`; they are not added to its declared members. Inline enums remain
  `Literal` annotations.
- Matching event listeners now share one decoded model per incoming event and
  event class, including `listen_all()`'s `ReceivedEvent.value`. Mutations are
  visible to other listeners. Treat event data as read-only or make a
  `copy.deepcopy(event)` before changing it privately.
- All generated type aliases use `type` statements, including primitives and
  arrays, e.g. `type FrameId = str` and `type Quad = list[float]`. Use them in
  annotations; pass plain values such as `frame_id: FrameId = "F1"` instead of
  calling `FrameId("F1")`. For runtime checks use `isinstance(value, str)` rather
  than `isinstance(value, FrameId)`.
- `Client` and `CDPSession` are renamed to `CdpClient` and `CdpSession`.
  Update imports to `from cdpify import CdpClient, CdpSession` and calls to
  `CdpClient(...)`. `client.session(...)` now returns `CdpSession`.
- Exceptions follow Python naming: `CDPException` → `CDPError`,
  `CDPConnectionException` → `CDPConnectionError`, `CDPCommandException` →
  `CDPCommandError`, `CDPTimeoutException` → `CDPTimeoutError`. The old names
  still work but emit a `DeprecationWarning` and will be removed in a future
  release.
- `CDPCommandError` takes `(method, code, message, data=None)` instead of the
  raw error dict. Use `CDPCommandError.from_response(method, error)` to build
  one from a CDP error payload. The message now names the failed method, e.g.
  `Page.navigate failed with CDP error -32000: Cannot navigate to invalid URL`.
- `listen()`, `listen_all()` and `CdpSession.listen()` are now regular methods
  that return an `EventSubscription` instead of async generators. `async for`
  and `aclose()` keep working. Code that relied on the generator type itself
  (e.g. `inspect.isasyncgen`) or on `asend()`/`athrow()` must be updated.
- `listen()`, `listen_all()` and `CdpSession.listen()` take the event class
  instead of an event name plus class, and `timeout` is keyword-only:

  ```python
  # Before
  client.listen(NetworkEvent.REQUEST_WILL_BE_SENT, RequestWillBeSentEvent)
  client.listen(
      event_name=NetworkEvent.REQUEST_WILL_BE_SENT,
      event_type=RequestWillBeSentEvent,
  )

  # After
  client.listen(RequestWillBeSentEvent)
  ```

  The CDP name comes from the new `__cdp_event__` class variable on generated
  event classes. For custom dataclasses pass `event_name="Domain.event"`.
- Calling a deprecated CDP command emits a `DeprecationWarning` instead of
  logging a warning on every call. Python's default filters show it once per
  call site; use `warnings.filterwarnings` or `-W` to change that. The
  decorator is now `warnings.deprecated` (PEP 702) on Python 3.13+, so IDEs and
  type checkers mark deprecated commands. `cdpify.shared.decorators.deprecated`
  requires a message: `@deprecated("...")` instead of `@deprecated()`.

### Added

- Optional `max_queue_size` on `CdpClient`, `WebSocketTransport`, `listen()`,
  `listen_all()`, and `CdpSession.listen()`. Zero keeps unlimited buffering;
  bounded queues drop their oldest event instead of blocking command responses.
  Subscriptions inherit the client limit unless overridden. Both subscriptions
  and the standalone WebSocket transport expose `dropped_events` counters.
- `cdpify[orjson]` enables optional `orjson` encoding and decoding in the WebSocket
  transport, with automatic fallback to `json` and outgoing text frames.
- Optional `CallbackTransport` protocol in `cdpify.transport` for direct event
  delivery without a transport queue. Existing `Transport` implementations work
  through their event iterator.
- `EventSubscription` registers its handler as soon as `listen()` is called, so
  events emitted before the first read are no longer lost. It supports
  `async with` for deterministic cleanup and `await events.next(timeout=...)`
  for waiting on a single event. `next()` raises `CDPStreamClosedError` once
  the stream has ended.
- Generated event classes expose their CDP method name as `__cdp_event__`,
  e.g. `LoadEventFiredEvent.__cdp_event__ == "Page.loadEventFired"`.
- `FindInPage` domain (`client.find_in_page`) from the latest CDP spec.

### Changed

- Generated `__cdp_event__` class variables refer to the domain's event enum,
  e.g. `LoadingFailedEvent.__cdp_event__ is NetworkEvent.LOADING_FAILED`.
- The root client and session views share the implementation of `listen()`.
- CI runs tests on Ubuntu, Windows, and macOS with Python 3.12, 3.13, and 3.14,
  including both JSON backends.
- `CDPTimeoutError` also inherits from the built-in `TimeoutError`, so
  `except TimeoutError` catches command timeouts.
- Docstrings of generated type aliases follow the alias, so IDEs and Sphinx
  show them on hover.
- Generated fields only carry `metadata={"cdp_name": ...}` when the CDP name
  differs from the Python name. Code that reads `field.metadata["cdp_name"]`
  directly should fall back to `field.name`.

### Fixed

- Concurrent disconnects and browser-initiated closure now wait for the same
  cleanup. Cancelling a disconnect waiter no longer interrupts socket cleanup
  or masks cancellation with an error when detaching the event callback.
- Bounded event streams close even when their buffers are full, preserving
  buffered events on disconnect. Explicit subscription closure releases pending
  events immediately. Subscriptions from an earlier connection stay closed
  after reconnecting.
- `decode_cdp` now decodes nested models behind `type X = ...` aliases instead
  of leaving them as plain dicts.
- `decode_cdp` logs a warning when a field annotation cannot be resolved,
  instead of silently leaving nested values as plain dicts.
- A malformed message from the browser no longer closes the WebSocket
  connection. The message is logged and skipped.
- Events sent with `"params": null` are delivered with empty params instead of
  being dropped as malformed.
- Event listeners (`listen()`, `listen_all()`, `CdpSession.listen()`) now end
  when the transport event stream ends or the client disconnects. Previously
  they waited forever unless a `timeout` was set. Events that were already
  received are still delivered before the stream ends.
- Array type aliases keep their element type instead of `list[Any]`, e.g.
  `DOM.Quad = list[float]` and `Target.TargetFilter = list[FilterEntry]`.
  Fields typed as `TargetFilter` now decode to `FilterEntry` objects instead
  of plain dicts.
- Generated fields and parameters whose CDP name is a Python keyword get a
  trailing underscore (`or` → `or_`), so the generated code is valid again.

### Performance

- The default WebSocket transport delivers events directly to the router,
  removing the intermediate queue and client event-loop task.
- Event models are decoded lazily once per incoming event and target class,
  then reused by matching listeners. Unread events are not decoded; caches are
  released together with the buffered event instead of being retained globally.
- `decode_cdp` builds a converter per field once per model instead of
  inspecting type annotations for every value. Decoding typical Network
  events is 4–7× faster (`ResponseReceivedEvent`: 56 µs → 7 µs).
- `import cdpify` loads CDP domains lazily on first access. Import time drops
  from ~790 ms to ~85 ms.
