"""Reproducible codec/dispatch benchmarks, with optional real CDP round trips."""

import argparse
import asyncio
import base64
import json
import platform
import random
import statistics
import time
import timeit

from cdpify import CdpClient, decode_cdp, encode_cdp
from cdpify.domains.runtime import EvaluateParams, EvaluateResult
from cdpify.domains.runtime.domain import Runtime
from cdpify.events import EventRouter
from cdpify.executor import BoundCommandExecutor
from cdpify.transport import TransportEvent

RESULT = {"result": {"type": "number", "value": 2}}


class Executor:
    async def execute(self, **kwargs):
        return RESULT


def sync_benchmark(fn, iterations, samples):
    fn()  # Compile the model plan outside the steady-state measurement.
    values = timeit.repeat(fn, number=iterations, repeat=samples)
    return {"median_us": statistics.median(values) * 1e6 / iterations}


async def async_benchmark(fn, iterations, samples):
    await fn()
    values = []
    for _ in range(samples):
        start = time.perf_counter_ns()
        for _ in range(iterations):
            await fn()
        values.append((time.perf_counter_ns() - start) / iterations / 1000)
    return {"median_us": statistics.median(values)}


async def main(args):
    output = {
        "metadata": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "iterations": args.iterations,
            "samples": args.samples,
        },
        "measurements": {},
    }
    measurements = output["measurements"]
    params = EvaluateParams(expression="1 + 1", return_by_value=True)
    measurements["encode_evaluate_params"] = sync_benchmark(
        lambda: encode_cdp(params), args.iterations, args.samples
    )
    measurements["decode_evaluate_result"] = sync_benchmark(
        lambda: decode_cdp(EvaluateResult, RESULT), args.iterations, args.samples
    )
    runtime = Runtime(Executor())
    measurements["typed_evaluate_mock"] = await async_benchmark(
        lambda: runtime.evaluate(expression="1 + 1", return_by_value=True),
        args.iterations,
        args.samples,
    )
    client_runtime = Runtime(BoundCommandExecutor(Executor()))
    measurements["typed_evaluate_with_client_deadline"] = await async_benchmark(
        lambda: client_runtime.evaluate(expression="1 + 1", return_by_value=True),
        args.iterations,
        args.samples,
    )
    for count in (0, 1, 10, 100):
        router = EventRouter(max_queue_size=1, overflow="drop_oldest")
        subscriptions = [router.listen_raw(session_id=None) for _ in range(count)]
        event = TransportEvent("Benchmark.event", {"value": 1})
        measurements[f"dispatch_{count}_listeners"] = await async_benchmark(
            lambda: router.dispatch(event), args.iterations, args.samples
        )
        for subscription in subscriptions:
            await subscription.aclose()
    if args.page_url:
        async with CdpClient(args.page_url, compression=args.compression) as client:
            for _ in range(20):
                await client.runtime.evaluate(expression="1 + 1", return_by_value=True)
            measurements["chrome_small_rtt"] = await round_trips(client, "1 + 1", 200)
            # A seeded Base64 payload approximates already-compressed CDP data
            # better than a repeated character. This measures 1 MiB both ways.
            payload = base64.b64encode(random.Random(42).randbytes(786432)).decode(
                "ascii"
            )
            measurements["chrome_1mib_rtt"] = await round_trips(
                client, json.dumps(payload), 30
            )
            output["metadata"]["browser"] = (await client.browser.get_version()).product
            output["metadata"]["compression"] = args.compression
    print(json.dumps(output, indent=2))


async def round_trips(client, expression, count):
    values = []
    for _ in range(count):
        start = time.perf_counter_ns()
        await client.runtime.evaluate(expression=expression, return_by_value=True)
        values.append((time.perf_counter_ns() - start) / 1000)
    return {
        "p50_us": statistics.median(values),
        "p95_us": sorted(values)[int(0.95 * count)],
        "count": count,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=10000)
    parser.add_argument("--samples", type=int, default=7)
    parser.add_argument("--page-url", help="Optional page webSocketDebuggerUrl")
    parser.add_argument("--compression", choices=["deflate"], default=None)
    options = parser.parse_args()
    if options.iterations <= 0 or options.samples <= 0:
        parser.error("iterations and samples must be positive")
    asyncio.run(main(options))
