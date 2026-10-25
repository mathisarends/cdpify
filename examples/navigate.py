import asyncio

from _chrome import get_ws_url

from cdpify import CdpClient


async def test_basic():
    print("=== Test 1: Basic Navigation ===")

    ws_url = get_ws_url()
    print(f"Connecting to: {ws_url}")

    async with CdpClient(ws_url) as client:
        result = await client.page.navigate(url="https://example.com")

        print(f"Navigation Result: {result}")


if __name__ == "__main__":
    asyncio.run(test_basic())
