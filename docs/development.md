# Development

How to work on `cdpify` itself.

## Project layout

```text
cdpify/
  client.py, session.py      CdpClient and CdpSession
  executor.py                command execution and deadlines
  events/                    subscriptions, routing and dispatch
  codec.py                   dataclass <-> wire-format conversion
  transport.py               Transport protocol
  transports/websocket.py    built-in WebSocket transport
  generator/                 code generator (spec -> Python)
  domains/                   GENERATED: one package per CDP domain
specs/                       bundled CDP specification (JSON)
scripts/check_generated.py   regenerate / check for drift
benchmarks/runtime.py        microbenchmarks
checks/typecheck_api.py      public API sample checked by Pyright
examples/                    runnable example scripts
tests/                       unit tests; tests/integration needs Chrome
```

`cdpify/domains/` is generated from the spec and templates. Its dataclasses
use keyword-only constructors and slots, and their fields are mutable. Event
listeners can share a decoded model, so copy it before editing. Smelt requires
frozen, slotted dataclasses in the hand-written code it checks.

## Setup

The project uses [uv](https://docs.astral.sh/uv/):

```bash
uv sync --dev                  # core + dev dependencies
uv sync --dev --extra orjson   # also test the orjson backend
```

## Checks

```bash
uv run pytest                                          # unit tests
uv run ruff check . --exclude cdpify/domains           # lint
uv run ruff format --check . --exclude cdpify/domains  # formatting
uv run pyright                                         # type checks
uv run smelt check --fail-on warning --show-hints       # architecture and code quality
uv run python scripts/check_generated.py               # generated-code drift
```

Run `uv run --extra orjson pytest` to exercise both JSON backends.

### Integration tests

Integration tests launch an isolated headless Chrome and are excluded from the
default run:

```bash
uv run --extra orjson pytest -m integration
```

Set `CHROME_PATH` if Chrome or Chromium is not found automatically.

### CI

CI runs the unit tests with both JSON backends on Ubuntu, Windows and macOS
with Python 3.12, 3.13 and 3.14, plus Pyright on the library and the public API
sample, Smelt on hand-written code and tests, the generated-code drift check
and the integration suite against Chrome.

Use a single-dot relative import within a package, such as
`from .schemas import Domain` in the generator. Imports outside the current
package use an absolute path. Repository YAML files use the `.yaml` extension.

## Code generation

`cdpify.generator` turns the CDP JSON specification into the packages under
`cdpify/domains/`.

Regenerate from the **bundled** specs in `specs/`, which is reproducible and
works offline:

```bash
uv run python scripts/check_generated.py --write
```

Download the **latest upstream** specs and regenerate everything:

```bash
uv run python -m cdpify.generator
```

Generator options:

| Option | Purpose |
| --- | --- |
| `--domain NAME` | Generate only this domain; repeat for several |
| `--spec-dir PATH` | Where downloaded specifications are written |
| `--output-dir PATH` | Where generated modules are written |

The output directory is **replaced** entirely, even for partial generation.
Use a separate `--output-dir` when generating selected domains so the bundled
client stays intact:

```bash
uv run python -m cdpify.generator --domain Page --domain Runtime \
  --output-dir build/selected-domains
```

Selected domains may reference types from other domains.

A scheduled workflow refreshes the upstream specification weekly and opens a
pull request when the generated code changes.

## Benchmarks

```bash
uv run python benchmarks/runtime.py
uv run --extra orjson python benchmarks/runtime.py \
  --page-url ws://localhost:9222/devtools/page/...
```

The output is JSON with environment metadata and timings for encoding,
decoding, typed calls and event dispatch at several listener counts. With
`--page-url`, it adds real round trips for small messages and a 1 MiB
payload, including p50 and p95 latency. Add `--compression deflate` to compare
compression; installing or omitting `orjson` selects the JSON backend.

Timings are diagnostic and are not used as CI pass/fail thresholds.

## Releasing

See [RELEASING.md](../RELEASING.md).
