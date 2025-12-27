# main.py
import asyncio
import httpx
from pydantic_cpd.cdp.page.commands import NavigateParams
from pydantic_cpd.cdp.page.library import PageClient
from pydantic_cpd.client import CDPClient


async def get_ws_url() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:9222/json")
        pages = response.json()

        if not pages:
            raise RuntimeError(
                "No pages found. Is Chrome running with --remote-debugging-port=9222?"
            )

        return pages[0]["webSocketDebuggerUrl"]


async def test_basic():
    print("=== Test 1: Basic send_raw ===")

    ws_url = await get_ws_url()
    print(f"Connecting to: {ws_url}")

    async with CDPClient(ws_url) as client:
        page_client = PageClient(client)
        result = await page_client.navigate(NavigateParams(url="https://example.com"))


async def main():
    try:
        await test_basic()
        print("\n✅ All tests passed!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


# WICHTIG: Das hier fehlt wahrscheinlich!
if __name__ == "__main__":
    asyncio.run(main())
