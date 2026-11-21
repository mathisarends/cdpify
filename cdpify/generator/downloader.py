import json
from pathlib import Path
from typing import Any, cast
from urllib.request import urlopen

from cdpify.generator.schemas import CDPSpecs, ProtocolSpec


def download_specs(destination: Path) -> CDPSpecs:
    """Download the protocol specifications and save them to ``destination``."""
    destination.mkdir(parents=True, exist_ok=True)

    browser = _fetch("browser_protocol.json", destination)
    js = _fetch("js_protocol.json", destination)

    return CDPSpecs(
        browser=ProtocolSpec.model_validate(browser),
        js=ProtocolSpec.model_validate(js),
    )


_BASE_URL = (
    "https://raw.githubusercontent.com/"
    "ChromeDevTools/devtools-protocol/refs/heads/master/json"
)


def _fetch(filename: str, destination: Path) -> dict[str, Any]:
    with urlopen(f"{_BASE_URL}/{filename}", timeout=30) as response:
        data = cast(dict[str, Any], json.load(response))

    (destination / filename).write_text(
        f"{json.dumps(data, indent=2)}\n", encoding="utf-8"
    )
    return data
