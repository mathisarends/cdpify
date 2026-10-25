# Changelog

All notable changes to this project are documented here.
Breaking changes are listed first in each release.

## [Unreleased]

### Breaking changes

- Exceptions follow Python naming: `CDPException` → `CDPError`,
  `CDPConnectionException` → `CDPConnectionError`, `CDPCommandException` →
  `CDPCommandError`, `CDPTimeoutException` → `CDPTimeoutError`. The old names
  still work but emit a `DeprecationWarning` and will be removed in a future
  release.
- `CDPCommandError` takes `(method, code, message, data=None)` instead of the
  raw error dict. Use `CDPCommandError.from_response(method, error)` to build
  one from a CDP error payload. The message now names the failed method, e.g.
  `Page.navigate failed with CDP error -32000: Cannot navigate to invalid URL`.
- `listen()`, `listen_all()` and `CDPSession.listen()` are now regular methods
  that return an `EventSubscription` instead of async generators. `async for`
  and `aclose()` keep working. Code that relied on the generator type itself
  (e.g. `inspect.isasyncgen`) or on `asend()`/`athrow()` must be updated.
- `listen()`, `listen_all()` and `CDPSession.listen()` take the event class
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

### Added

- `EventSubscription` registers its handler as soon as `listen()` is called, so
  events emitted before the first read are no longer lost. It supports
  `async with` for deterministic cleanup and `await events.next(timeout=...)`
  for waiting on a single event. `next()` raises `CDPStreamClosedError` once
  the stream has ended.
- Generated event classes expose their CDP method name as `__cdp_event__`,
  e.g. `LoadEventFiredEvent.__cdp_event__ == "Page.loadEventFired"`.
- `FindInPage` domain (`client.find_in_page`) from the latest CDP spec.

### Changed

- `CDPTimeoutError` also inherits from the built-in `TimeoutError`, so
  `except TimeoutError` catches command timeouts.

### Fixed

- `decode_cdp` now decodes nested models behind `type X = ...` aliases instead
  of leaving them as plain dicts.
- `decode_cdp` logs a warning when a field annotation cannot be resolved,
  instead of silently leaving nested values as plain dicts.
- A malformed message from the browser no longer closes the WebSocket
  connection. The message is logged and skipped.
- Event listeners (`listen()`, `listen_all()`, `CDPSession.listen()`) now end
  when the transport event stream ends or the client disconnects. Previously
  they waited forever unless a `timeout` was set. Events that were already
  received are still delivered before the stream ends.
- Generated fields and parameters whose CDP name is a Python keyword get a
  trailing underscore (`or` → `or_`), so the generated code is valid again.

### Performance

- `decode_cdp` builds a converter per field once per model instead of
  inspecting type annotations for every value. Decoding typical Network
  events is 4–7× faster (`ResponseReceivedEvent`: 56 µs → 7 µs).
- `import cdpify` loads CDP domains lazily on first access. Import time drops
  from ~790 ms to ~85 ms.
