import asyncio
import logging

from _chrome import get_ws_url

from cdpify import CdpClient
from cdpify.domains.network.events import (
    LoadingFailedEvent,
    LoadingFinishedEvent,
    RequestWillBeSentEvent,
    ResponseReceivedEvent,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def monitor_requests(client: CdpClient) -> None:
    async for event in client.listen(RequestWillBeSentEvent):
        url = event.request.url
        method = event.request.method
        print(f"📤 Request: {method} {url}")


async def monitor_responses(client: CdpClient) -> None:
    async for event in client.listen(ResponseReceivedEvent):
        url = event.response.url
        status = event.response.status
        mime_type = event.response.mime_type
        print(f"📥 Response: {status} {url} ({mime_type})")


async def monitor_loading_finished(client: CdpClient) -> None:
    async for event in client.listen(LoadingFinishedEvent):
        request_id = event.request_id
        print(f"✓ Loading finished: {request_id}")


async def monitor_loading_failed(client: CdpClient) -> None:
    async for event in client.listen(LoadingFailedEvent):
        request_id = event.request_id
        error_text = event.error_text
        print(f"✗ Loading failed: {request_id} - {error_text}")


async def main() -> None:
    ws_url = get_ws_url()
    print(f"Connecting to: {ws_url}\n")

    async with CdpClient(ws_url) as client:
        await client.network.enable()

        print("🌐 Network monitoring started...")
        print("Press Ctrl+C to stop\n")

        tasks = [
            asyncio.create_task(monitor_requests(client)),
            asyncio.create_task(monitor_responses(client)),
            asyncio.create_task(monitor_loading_finished(client)),
            asyncio.create_task(monitor_loading_failed(client)),
        ]

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            # Ctrl+C cancels the main task; KeyboardInterrupt only reaches
            # the caller of asyncio.run().
            print("\n⏹️  Stopping...")
            raise
        finally:
            for task in tasks:
                task.cancel()
            print("✅ Network monitoring stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Done!")
