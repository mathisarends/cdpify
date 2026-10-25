import subprocess
import sys
import types
from pathlib import Path

import pytest

from cdpify.shared.lazy import lazy_exports

_PROJECT_ROOT = Path(__file__).parents[1]


def _run_isolated(code: str) -> str:
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=_PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def test_importing_cdpify_does_not_load_domain_modules() -> None:
    output = _run_isolated(
        "import sys, cdpify; "
        "print(sorted(m for m in sys.modules if m.startswith('cdpify.domains.')))"
    )

    assert output == "['cdpify.domains.accessors']"


def test_domain_accessor_loads_only_its_domain_on_demand() -> None:
    output = _run_isolated(
        "import sys; from cdpify import CdpClient; "
        "client = CdpClient(transport=object()); client.page; "
        "print('cdpify.domains.page.domain' in sys.modules, "
        "'cdpify.domains.webaudio.domain' in sys.modules)"
    )

    assert output == "True False"


def test_lazy_names_resolve_through_public_package_paths() -> None:
    from cdpify.domains import Page
    from cdpify.domains.animation import AnimationType
    from cdpify.domains.animation.types import Animation
    from cdpify.domains.page import NavigateParams
    from cdpify.domains.page.commands import NavigateParams as DirectNavigateParams
    from cdpify.domains.page.domain import Page as DirectPage

    assert Page is DirectPage
    assert NavigateParams is DirectNavigateParams
    assert AnimationType is Animation


def test_lazy_exports_caches_value_and_lists_names() -> None:
    package = types.ModuleType("fake_lazy_package")
    sys.modules[package.__name__] = package
    submodule = types.ModuleType("fake_lazy_package.values")
    submodule.Value = object()
    sys.modules[submodule.__name__] = submodule
    try:
        getattr_hook, dir_hook = lazy_exports(
            package.__name__, {"Exported": (".values", "Value")}
        )

        assert getattr_hook("Exported") is submodule.Value
        assert package.__dict__["Exported"] is submodule.Value
        assert "Exported" in dir_hook()
        with pytest.raises(AttributeError, match="Missing"):
            getattr_hook("Missing")
    finally:
        del sys.modules[package.__name__]
        del sys.modules[submodule.__name__]
