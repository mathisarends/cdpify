# Level 4: Timeouts and errors

Browsers hang, targets crash and specs drift. This guide shows how to bound
every call and what `cdpify` raises when something goes wrong.

## Timeouts

### The client default

Every command has a total time budget, covering sending the request and
waiting for its response. It comes from `CdpClient(default_timeout_seconds=...)`, which
defaults to **30 seconds** and applies to the root client and all sessions,
whatever the transport:

```python
client = CdpClient(ws_url, default_timeout_seconds=10.0)  # None disables it
```

When it expires, `cdpify` raises `CDPTimeoutError`.

### Per call: `asyncio.timeout`

Generated methods accept only CDP parameters, so a per-call deadline uses
Python's standard tool. It can cover one call or a whole sequence:

```python
import asyncio

async with asyncio.timeout(5):
    await client.page.navigate(url="https://example.com")
    await client.runtime.evaluate(expression="document.title")
```

An outer `asyncio.timeout()` that fires first raises the built-in
`TimeoutError`. `CDPTimeoutError` subclasses `TimeoutError`, so
`except TimeoutError` catches both.

Either way the pending request is released locally. Cancelling the wait does
**not** cancel work already started inside Chrome.

### Raw commands

`execute()` takes a client-side `timeout_seconds` as a keyword argument:

```python
await client.execute("Page.reload", timeout_seconds=5)
await client.execute("Page.reload", timeout_seconds=None)  # no deadline for this call
await client.execute("Page.reload")                # inherit default_timeout_seconds
```

### CDP `timeout` parameters are different

Some CDP commands have their own parameter named `timeout`. It keeps the
protocol's meaning and units. `Runtime.evaluate(timeout=...)`, for example,
limits script execution inside Chrome in **milliseconds**:

```python
# Chrome aborts the script after 500 ms; the client still waits up to its default.
await client.runtime.evaluate(expression="heavyWork()", timeout=500)
```

### Event reads

Subscriptions have their own timeouts; see
[Events](02-events.md#timeouts).

## Errors

All library errors derive from `CDPError` and are importable from `cdpify` or
`cdpify.error`:

| Error | Raised when |
| --- | --- |
| `CDPError` | Base class of everything below |
| `CDPConnectionError` | The connection can't be used: not connected, already connected, or closed |
| `CDPSessionClosedError` | A target session detached or its connection ended. Subclass of `CDPConnectionError`. |
| `CDPCommandError` | Chrome rejected a command. Has `method`, `code`, `message` and `data`. |
| `CDPTimeoutError` | A command exceeded its client deadline. Also a `TimeoutError`. |
| `CDPStreamClosedError` | `next()` was called on an event stream that has ended |
| `CDPEventOverflowError` | An event buffer overflowed under `overflow="error"`. Has `max_queue_size` and `dropped_events`. |
| `CDPDecodeError` | A response or event lacks fields its model requires. Has `model_type`, `missing_fields` and `path`. |

### Handling command errors

```python
from cdpify import CDPCommandError, CDPTimeoutError


async def outer_html(client, selector: str) -> str | None:
    document = await client.dom.get_document()
    try:
        found = await client.dom.query_selector(
            node_id=document.root.node_id, selector=selector
        )
        if not found.node_id:  # CDP reports "no match" as node ID 0
            return None
        html = await client.dom.get_outer_html(node_id=found.node_id)
    except CDPCommandError as error:
        print(f"{error.method} failed ({error.code}): {error.message}")
        return None
    except CDPTimeoutError:
        print("Chrome did not answer in time")
        return None
    return html.outer_html
```

Not every failure is an exception: some commands report problems in their
result. `Page.navigate` sets `error_text` when navigation fails, and
`Runtime.evaluate` sets `exception_details` when the script throws:

```python
result = await client.runtime.evaluate(expression="undefinedVariable")
if details := result.exception_details:
    print(details.exception.description if details.exception else details.text)
    # ReferenceError: undefinedVariable is not defined
```

## Decoding

### Strict by default

Responses and events are decoded into their generated models. A payload that
lacks a field the spec marks as required raises `CDPDecodeError`, which
names the model, the missing fields and the wire path to the nested object:

```text
Cannot decode cdpify.domains.network.types.Response at response:
missing required fields status, status_text, headers, ...
```

Decoding is deliberately forgiving elsewhere: unknown fields are ignored, and
enum values from newer Chrome versions are kept. It checks the presence of
required fields; it does not validate primitive values against the schema.

### Decoding raw payloads

`decode_cdp` and `encode_cdp` convert between models and wire dictionaries.
Combine them with `execute()` when a browser deviates from the spec, and
choose a tolerant decode explicitly:

```python
from cdpify import decode_cdp
from cdpify.domains.runtime import EvaluateResult

raw = await client.execute("Runtime.evaluate", {"expression": "1 + 1"})
result = decode_cdp(EvaluateResult, raw, strict=False)
```

With `strict=False`, missing required fields, including nested ones, become
`None` and a warning is logged.

### `UNSET` vs. `None`

For most optional parameters `None` means "omit". Fields typed as `Any` are
different: JSON `null` is a valid value for them, so omission is spelled
`UNSET`:

```python
from cdpify import UNSET, encode_cdp
from cdpify.domains.runtime import CallArgument

assert encode_cdp(CallArgument()) == {}                             # omitted
assert encode_cdp(CallArgument(value=None)) == {"value": None}      # JSON null
assert CallArgument().value is UNSET
```

## Deprecated commands

Deprecated CDP commands still work but emit a `DeprecationWarning`. Use the
standard warning filters to silence them, or turn them into errors in tests:

```python
import warnings

warnings.filterwarnings(
    "ignore", category=DeprecationWarning, message=r"\w+\.\w+ is deprecated"
)
```

## Next

**Level 5: [Configuration and transports](05-configuration-and-transports.md).**
Every client option, and how to connect over something other than the built-in
WebSocket transport.
