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
- Calling a deprecated CDP command emits a `DeprecationWarning` instead of
  logging a warning on every call. Python's default filters show it once per
  call site; use `warnings.filterwarnings` or `-W` to change that. The
  decorator is now `warnings.deprecated` (PEP 702) on Python 3.13+, so IDEs and
  type checkers mark deprecated commands. `cdpify.shared.decorators.deprecated`
  requires a message: `@deprecated("...")` instead of `@deprecated()`.

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
- Docstrings of generated type aliases follow the alias, so IDEs and Sphinx
  show them on hover.
- Generated fields only carry `metadata={"cdp_name": ...}` when the CDP name
  differs from the Python name. Code that reads `field.metadata["cdp_name"]`
  directly should fall back to `field.name`.

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
- Array type aliases keep their element type instead of `list[Any]`, e.g.
  `DOM.Quad = list[float]` and `Target.TargetFilter = list[FilterEntry]`.
  Fields typed as `TargetFilter` now decode to `FilterEntry` objects instead
  of plain dicts.
- Generated fields and parameters whose CDP name is a Python keyword get a
  trailing underscore (`or` → `or_`), so the generated code is valid again.

### Performance

- `decode_cdp` builds a converter per field once per model instead of
  inspecting type annotations for every value. Decoding typical Network
  events is 4–7× faster (`ResponseReceivedEvent`: 56 µs → 7 µs).
- `import cdpify` loads CDP domains lazily on first access. Import time drops
  from ~790 ms to ~85 ms.
