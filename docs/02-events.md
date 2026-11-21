# Level 2: Events

CDP pushes events such as `Network.requestWillBeSent` or `Page.loadEventFired`
to the client. `cdpify` exposes them as typed async streams.

## Subscribing

Pass a generated event class to `listen()`. The returned `EventSubscription` is
an async iterator of typed events:

```python
from cdpify.domains.network import RequestWillBeSentEvent

await client.network.enable()  # most domains only emit events once enabled

async for event in client.listen(RequestWillBeSentEvent):
    print(event.request.method, event.request.url)
```

An `EventSubscription` supports three ways of reading:

| Usage | Behavior |
| --- | --- |
| `async for event in sub` | Yields events until the stream ends, then stops normally. |
| `await sub.next(timeout=...)` | Returns one event. Raises `TimeoutError` if none arrives in time, `CDPStreamClosedError` if the stream has ended. |
| `async with sub:` | Unsubscribes when the block exits. Combine with either of the above. |

Further members:

- `await sub.aclose()` unsubscribes immediately and drops buffered events.
- `sub.closed` is `True` once no further events will be returned.
- `sub.dropped_events` counts events discarded by the
  [overflow policy](#limiting-buffered-events).

## Subscribe first, then trigger

A subscription is registered **as soon as `listen()` returns**, and events are
buffered until you read them. So when you wait for an event that your own
command causes, subscribe before sending the command:

```python
from cdpify.domains.page import LoadEventFiredEvent

await client.page.enable()
async with client.listen(LoadEventFiredEvent) as loaded:
    await client.page.navigate(url="https://example.com")
    await loaded.next(timeout=10)
```

Subscribing after `navigate()` returns would race the browser and could miss
the event.

## Timeouts

`listen(..., timeout=seconds)` sets a default deadline for every read from that
subscription. `next(timeout=...)` overrides it for a single read:

| `next()` argument | Meaning |
| --- | --- |
| omitted | Use the `timeout` given to `listen()` (default: wait forever). |
| `None` | Wait forever. |
| `0` | Return an already buffered event, or raise `TimeoutError` immediately. |
| `seconds` | Wait up to that long. |

An `async for` loop uses the `listen()` timeout for each iteration and raises
`TimeoutError` when it expires.

## When streams end

A stream ends when:

- you leave its `async with` block or call `aclose()`;
- the client disconnects (buffered events are still delivered first);
- Chrome detaches the target session a [session-scoped](03-sessions.md)
  subscription belongs to (buffered events are delivered first);
- its buffer overflows under `overflow="error"` (see below).

After that, `async for` stops and `next()` raises `CDPStreamClosedError`, or
`CDPEventOverflowError` for an overflow.

## Scopes: root, session, all

Every event arrives either on the root connection or on a target session.
Choose the scope with the object you call `listen()` on:

| Call | Receives |
| --- | --- |
| `client.listen(Event)` | Events from the root connection only |
| `session.listen(Event)` | Events from that session only |
| `client.listen_all(Event)` | Events from the root and every session |

```python
tab = await client.attach(target_id)

async for event in tab.listen(RequestWillBeSentEvent):
    print(event.request.url)  # this tab's requests only
```

`listen_all()` wraps each event in a `ReceivedEvent` so the routing metadata
stays separate from the CDP model:

```python
async for received in client.listen_all(RequestWillBeSentEvent):
    print(received.session_id, received.value.request.url)
```

`received.session_id` is `None` for root events.

## Running several listeners

Each subscription is independent. To process several event types at once, run
one task per stream:

```python
from cdpify.domains.network import LoadingFailedEvent, ResponseReceivedEvent


async def log_responses() -> None:
    async for event in client.listen(ResponseReceivedEvent):
        print(event.response.status, event.response.url)


async def log_failures() -> None:
    async for event in client.listen(LoadingFailedEvent):
        print("failed:", event.error_text)


async with asyncio.TaskGroup() as group:
    group.create_task(log_responses())
    group.create_task(log_failures())
```

See [`examples/network_monitoring.py`](../examples/network_monitoring.py) for a
complete script.

## Event models are shared and read-only

An incoming event is decoded once per event class, when the first listener
reads it. All matching `listen()`, `CdpSession.listen()` and `listen_all()`
subscriptions receive **the same object**. Treat events as read-only; changing
one changes what the other listeners see. Copy it if you need a private,
mutable instance:

```python
from copy import deepcopy

owned = deepcopy(event)
```

Unread events are never decoded, and the cached model is released once every
subscription has read or discarded the event.

## Limiting buffered events

By default every subscription buffers without limit. Set `max_queue_size` on
the client to cap each listener's buffer, and override it per subscription.
`0` means unlimited.

What happens when a buffer is full depends on the overflow policy:

| `overflow=` | Behavior |
| --- | --- |
| `"error"` (default) | The affected subscription ends; its next read raises `CDPEventOverflowError`. |
| `"drop_oldest"` | The oldest buffered event is discarded and `dropped_events` is incremented. |

`"error"` makes loss explicit. That matters for events that need a reply, such
as `Fetch.requestPaused`, where silently dropping one would stall a request.
Choose `"drop_oldest"` for streams where loss is acceptable:

```python
client = CdpClient(ws_url, max_queue_size=256, overflow="drop_oldest")

async with client:
    async with client.listen(RequestWillBeSentEvent, max_queue_size=32) as events:
        event = await events.next(timeout=10)
        print(events.dropped_events)
```

Overflow never blocks command responses or other subscriptions. The same
options apply to `listen()`, `listen_all()`, session listeners and raw streams.

`CDPEventOverflowError` carries `max_queue_size` and `dropped_events` for
diagnostics.

## Raw events

Raw subscriptions skip decoding and yield `TransportEvent` objects with the wire
`method`, the `camelCase` `params` dictionary and the `session_id`. Use them for
events missing from the generated spec, or to inspect the wire data:

```python
async with tab.listen_raw("Future.event") as events:
    event = await events.next(timeout=5)
    print(event.method, event.session_id, event.params)
```

| Call | Scope |
| --- | --- |
| `client.listen_raw(method)` | Root connection |
| `session.listen_raw(method)` | One session |
| `client.listen_all_raw(method)` | Root and every session |

Omit `method` to receive every event in the scope. Raw streams follow the same
lifetime, buffering and read-only rules as typed ones.

## Custom event classes

Generated event classes carry their wire name in `__cdp_event__`. To decode an
event into your own dataclass, pass the name explicitly:

```python
from dataclasses import dataclass


@dataclass
class LoadFired:
    timestamp: float


async for event in client.listen(LoadFired, event_name="Page.loadEventFired"):
    print(event.timestamp)
```

Generated event dataclasses contain only fields defined by the CDP
specification; routing data such as the session ID is never mixed in.

## Next

**Level 3: [Multiple targets](03-sessions.md).** Attach to several tabs and
route commands and events per target. Event-driven recipes are in the
[cookbook](cookbook.md#level-2-events).
