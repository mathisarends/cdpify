# Changelog

All notable changes to this project are documented here.
Breaking changes are listed first in each release.

## [Unreleased]

### Fixed

- Event listeners (`listen()`, `listen_all()`, `CDPSession.listen()`) now end
  when the transport event stream ends or the client disconnects. Previously
  they waited forever unless a `timeout` was set. Events that were already
  received are still delivered before the stream ends.
- Generated fields and parameters whose CDP name is a Python keyword get a
  trailing underscore (`or` → `or_`), so the generated code is valid again.

### Added

- `FindInPage` domain (`client.find_in_page`) from the latest CDP spec.

### Performance

- `import cdpify` loads CDP domains lazily on first access. Import time drops
  from ~790 ms to ~85 ms.
