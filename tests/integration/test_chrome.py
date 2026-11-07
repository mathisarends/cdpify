"""Run with pytest -m integration; CHROME_PATH can select the browser."""

import asyncio
import json
import os
import shutil
import subprocess
import time

import pytest
import pytest_asyncio

from cdpify import CdpClient, CDPTimeoutError
from cdpify.domains.page import LoadEventFiredEvent
from cdpify.domains.runtime import CallArgument
from cdpify.transports import websocket as websocket_module

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def browser_url(tmp_path_factory):
    candidates = [
        os.environ.get("CHROME_PATH"),
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    executable = next((p for p in candidates if p and os.path.isfile(p)), None)
    if executable is None:
        pytest.skip("Chrome not found; set CHROME_PATH")
    profile = tmp_path_factory.mktemp("cdpify-chrome")
    process = subprocess.Popen(
        [
            executable,
            "--headless=new",
            "--remote-debugging-port=0",
            "--user-data-dir=" + str(profile),
            "--no-first-run",
            "--no-default-browser-check",
            "--no-sandbox",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    try:
        port_file = profile / "DevToolsActivePort"
        deadline = time.monotonic() + 20
        while True:
            if port_file.exists():
                lines = port_file.read_text().splitlines()
                if len(lines) >= 2:
                    port, path = lines[:2]
                    break
            if process.poll() is not None or time.monotonic() >= deadline:
                pytest.fail("Chrome did not expose its debugger endpoint")
            time.sleep(0.05)
        yield f"ws://127.0.0.1:{port}{path}"
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


@pytest_asyncio.fixture
async def browser(browser_url):
    async with CdpClient(browser_url) as client:
        yield client


async def page(client):
    target = await client.target.create_target(url="about:blank")
    attached = await client.target.attach_to_target(
        target_id=target.target_id, flatten=True
    )
    return client.session(attached.session_id)


@pytest.mark.asyncio
async def test_typed_null_and_undefined_remain_distinct(browser) -> None:
    tab = await page(browser)
    root = await tab.runtime.evaluate(expression="globalThis")
    for arguments, expected in [
        ([CallArgument(value=None)], "null"),
        ([CallArgument()], "undefined"),
    ]:
        result = await tab.runtime.call_function_on(
            function_declaration="function(v){return v === null ? 'null' : typeof v}",
            object_id=root.result.object_id,
            arguments=arguments,
            return_by_value=True,
        )
        assert result.result.value == expected


@pytest.mark.asyncio
async def test_event_subscription_is_active_before_navigation(browser) -> None:
    tab = await page(browser)
    await tab.page.enable()
    async with (
        tab.listen(LoadEventFiredEvent) as typed,
        browser.listen_all_raw("Page.loadEventFired") as raw,
    ):
        result = await tab.page.navigate(url="data:text/html,<title>cdpify</title>")
        assert result.frame_id
        assert (await typed.next(timeout=5)).timestamp > 0
        wire = await raw.next(timeout=5)
        assert wire.session_id == tab.session_id
        assert wire.params["timestamp"] > 0


@pytest.mark.asyncio
async def test_outer_timeout_releases_pending_request_and_connection_stays_usable(
    browser,
) -> None:
    tab = await page(browser)
    with pytest.raises(TimeoutError) as error:
        async with asyncio.timeout(0.05):
            await tab.runtime.evaluate(
                expression="new Promise(() => {})", await_promise=True
            )
    assert not isinstance(error.value, CDPTimeoutError)
    assert browser.transport._pending_requests == {}
    assert (
        await tab.runtime.evaluate(expression="2 + 2", return_by_value=True)
    ).result.value == 4


@pytest.mark.asyncio
@pytest.mark.parametrize("backend", ["json", "orjson"])
@pytest.mark.parametrize("compression", [None, "deflate"])
async def test_large_payload_backends_and_compression(
    browser_url, monkeypatch, backend, compression
) -> None:
    monkeypatch.setattr(
        websocket_module,
        "orjson",
        None if backend == "json" else pytest.importorskip("orjson"),
    )
    async with CdpClient(browser_url, compression=compression) as client:
        assert bool(client.transport._ws.protocol.extensions) == (
            compression == "deflate"
        )
        tab = await page(client)
        value = "Grüße 🌍" * 20000
        result = await tab.runtime.evaluate(
            expression=json.dumps(value), return_by_value=True
        )
        assert result.result.value == value
