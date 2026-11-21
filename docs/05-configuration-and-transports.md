# Level 5: Configuration and transports

This guide covers every `CdpClient` option and the transport layer underneath
it.

## Client options

```python
client = CdpClient(
    "ws://localhost:9222/devtools/browser/...",
    # Commands and events
    default_timeout=30.0,       # total budget per command in seconds; None disables
    max_queue_size=0,           # per-listener event buffer; 0 = unlimited
    overflow="error",           # or "drop_oldest"
    # WebSocket transport
    additional_headers={"Authorization": "Bearer token"},
    max_frame_size=100 * 1024 * 1024,
    compression=None,           # or "deflate"
    open_timeout=10.0,
    close_timeout=10.0,
)
```

| Option | Default | Meaning |
| --- | --- | --- |
| `url` | (required unless `transport`) | WebSocket URL of a page or the browser |
| `transport` | `None` | A custom [`Transport`](#custom-transports). Mutually exclusive with `url`. |
| `default_timeout` | `30.0` | Total budget per command in seconds, for every transport. See [Timeouts](04-timeouts-and-errors.md#timeouts). |
| `max_queue_size` | `0` | Buffer limit per event listener. `0` is unlimited. See [Events](02-events.md#limiting-buffered-events). |
| `overflow` | `"error"` | What a full buffer does: end that stream with an error, or `"drop_oldest"` |
| `additional_headers` | `None` | Extra HTTP headers for the WebSocket handshake |
| `max_frame_size` | 100 MiB | Largest accepted incoming frame, in bytes. Raise it for large screenshots or response bodies. |
| `compression` | `None` | `"deflate"` enables WebSocket compression |
| `open_timeout` | `10.0` | Seconds allowed for the opening handshake |
| `close_timeout` | `10.0` | Seconds allowed for the closing handshake |

The last five options configure the built-in WebSocket transport and only
apply when you pass `url`. A custom transport manages its own connection
settings.

### Compression

Compression is off by default: on a local connection it costs CPU and adds
latency. Turn it on when Chrome runs on another machine and bandwidth matters
more:

```python
client = CdpClient(remote_url, compression="deflate")
```

### JSON backend

With the `orjson` extra installed, the WebSocket transport uses `orjson` for
encoding and decoding automatically, and falls back to the standard library
otherwise. Outgoing messages stay text frames either way.

```bash
pip install "cdpify[websocket,orjson]"
```

### Logging

`cdpify` logs through the standard `logging` module under the `cdpify`
namespace. Enable debug output to see every event method as it arrives:

```python
import logging

logging.getLogger("cdpify").setLevel(logging.DEBUG)
```

## Connection lifecycle

```python
client = CdpClient(ws_url)

await client.connect()      # raises CDPConnectionError if already connected
print(client.is_connected)
await client.disconnect()   # idempotent and safe to call concurrently
```

`async with CdpClient(...)` does the same. A client can be reconnected after
it has disconnected. On disconnect, event streams deliver what they have
buffered and then end. Subscriptions and session views do not carry over to a
new connection: subscribe and attach again after reconnecting.

## Transports

A transport moves CDP messages; `CdpClient` adds typing, timeouts, sessions and
event routing on top. `CdpClient(url)` creates the built-in
`WebSocketTransport`, which needs the `websocket` extra. `client.transport`
returns the transport in use.

### Using `WebSocketTransport` directly

The transport is usable on its own, for example in low-level tooling. It takes
the same connection options as the client, but has no default command timeout:

```python
from cdpify.transports.websocket import WebSocketTransport

transport = WebSocketTransport(ws_url, compression="deflate")
await transport.connect()
try:
    result = await transport.execute(
        "Runtime.evaluate", {"expression": "1 + 1"}, timeout=5
    )
finally:
    await transport.disconnect()
```

Its `max_queue_size` and `overflow` options bound the buffer of its own
`events()` stream with the same policies as client subscriptions.

### Custom transports

To speak CDP over something else, such as a pipe, a proxy or an in-memory
fake for tests, implement the `Transport` protocol and pass it to the client:

```python
from collections.abc import AsyncIterator
from typing import Any

from cdpify import CdpClient, TransportEvent


class MyTransport:
    @property
    def is_connected(self) -> bool: ...

    async def connect(self) -> None: ...

    async def disconnect(self) -> None: ...

    async def execute(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        session_id: str | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]: ...

    def events(self) -> AsyncIterator[TransportEvent]: ...


client = CdpClient(transport=MyTransport())
```

The contract:

- `execute()` sends one command, routed to `session_id` if given, and returns
  the response's `result` dictionary. Raise `CDPCommandError` for CDP error
  responses.
- `timeout` is a total budget in seconds; `None` means no deadline.
  `CdpClient` enforces its own deadline and passes `None`, so your transport
  must let the outer cancellation propagate and release that request's
  resources when cancelled.
- `events()` yields a `TransportEvent(method, params, session_id)` for every
  incoming event until the connection closes. `CdpClient` is its only
  consumer.
- `disconnect()` releases outstanding requests and ends the event stream.

### Callback delivery

For lower latency, a transport can additionally implement
`CallbackTransport` from `cdpify.transport` and push events straight into the
client instead of through `events()`; the built-in WebSocket transport does
this. The client calls `set_event_handler(handler)` before connecting. Await
the handler for each event in order, and once with `None` when the stream
closes. The handler runs inside your receive loop, so it must never wait for a
command response on the same transport.

Transports that implement only `events()` keep working.
