"""Shared helper to launch Chrome with remote debugging for the examples."""

import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

DEBUG_PORT = 9222
_DEBUG_PORT_POLL_SECONDS = 0.2
PROFILE_DIR = Path(tempfile.gettempdir()) / "cdpify-chrome-profile"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "google-chrome",
    "chromium",
]


def _find_chrome() -> str:
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists() or shutil.which(candidate):
            return candidate
    raise RuntimeError(
        "Chrome executable not found. Set CHROME_CANDIDATES in _chrome.py."
    )


def _is_debug_port_open() -> bool:
    try:
        with urlopen(f"http://localhost:{DEBUG_PORT}/json/version", timeout=1):
            return True
    except URLError:
        return False


def ensure_chrome_running(
    timeout_seconds: float = 10.0, start_url: str = "about:blank"
) -> None:
    """Start Chrome with remote debugging enabled, unless it's already running.

    The tab is opened directly on `start_url` rather than navigated there via
    CDP afterwards: navigating away from about:blank/new-tab-page triggers a
    renderer process swap (Site Isolation), which detaches the CDP session
    that was attached to the old target.
    """
    if _is_debug_port_open():
        return

    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    chrome = _find_chrome()

    subprocess.Popen(
        [
            chrome,
            f"--remote-debugging-port={DEBUG_PORT}",
            f"--user-data-dir={PROFILE_DIR}",
            "--no-first-run",
            "--no-default-browser-check",
            start_url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if _is_debug_port_open():
            return
        time.sleep(_DEBUG_PORT_POLL_SECONDS)

    raise RuntimeError(f"Chrome did not open the debug port within {timeout_seconds}s")


def get_ws_url(start_url: str = "about:blank") -> str:
    ensure_chrome_running(start_url=start_url)

    with urlopen(f"http://localhost:{DEBUG_PORT}/json") as response:
        pages = json.load(response)

    if not pages:
        raise RuntimeError("No pages found even though Chrome is running.")

    return pages[0]["webSocketDebuggerUrl"]
