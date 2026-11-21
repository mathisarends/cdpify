# cdpify documentation

`cdpify` gives you fully typed, Pythonic access to the Chrome DevTools
Protocol. These guides form a learning path: each level builds on the one
before it, and every concept comes with a runnable example.

## Learning path

| Level | Guide | After reading it you can… |
| --- | --- | --- |
| 1 | [First steps](01-first-steps.md) | connect to Chrome, send commands and read typed results |
| 2 | [Events](02-events.md) | wait for and stream browser events without races |
| 3 | [Multiple targets](03-sessions.md) | open, attach to and drive several tabs concurrently |
| 4 | [Timeouts and errors](04-timeouts-and-errors.md) | bound every call, handle failures and decode raw payloads |
| 5 | [Configuration and transports](05-configuration-and-transports.md) | tune the connection and plug in your own transport |

## Cookbook

The [cookbook](cookbook.md) collects complete recipes, sorted by difficulty:
screenshots, scraping the DOM, console capture, device emulation, waiting for
navigation, request blocking and mocking, and multi-tab crawling.

## Reference material

- The [migration guide](migration.md) covers breaking changes by version.
- [Changelog](../CHANGELOG.md): full release notes.
- [Chrome DevTools Protocol reference](https://chromedevtools.github.io/devtools-protocol/):
  the upstream description of every domain, command and event. Every CDP name
  maps to `cdpify` by switching to `snake_case`, as explained in
  [First steps](01-first-steps.md#domains-and-commands).

## Contributing

- [Development](development.md): setup, tests, code generation, benchmarks.
- [Releasing](../RELEASING.md): the release checklist.
