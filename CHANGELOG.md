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

### Added

- `EventSubscription` registers its handler as soon as `listen()` is called, so
  events emitted before the first read are no longer lost. It supports
  `async with` for deterministic cleanup and `await events.next(timeout=...)`
  for waiting on a single event. `next()` raises `CDPStreamClosedError` once
  the stream has ended.
- `FindInPage` domain (`client.find_in_page`) from the latest CDP spec.

### Changed

- `CDPTimeoutError` also inherits from the built-in `TimeoutError`, so
  `except TimeoutError` catches command timeouts.

### Fixed

- Event listeners (`listen()`, `listen_all()`, `CDPSession.listen()`) now end
  when the transport event stream ends or the client disconnects. Previously
  they waited forever unless a `timeout` was set. Events that were already
  received are still delivered before the stream ends.
- Generated fields and parameters whose CDP name is a Python keyword get a
  trailing underscore (`or` → `or_`), so the generated code is valid again.

### Performance

- `import cdpify` loads CDP domains lazily on first access. Import time drops
  from ~790 ms to ~85 ms.
