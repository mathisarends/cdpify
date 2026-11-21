from pathlib import Path

import pytest

from cdpify.generator import formatting, generator
from cdpify.generator.schemas import Domain


def test_render_domain_includes_available_modules(simple_domain: Domain) -> None:
    files = generator._render_domain(simple_domain)
    directory = Path("sample")

    assert set(files) == {
        directory / "__init__.py",
        directory / "domain.py",
        directory / "commands.py",
        directory / "events.py",
        directory / "types.py",
    }


def test_render_domain_omits_empty_optional_modules(empty_domain: Domain) -> None:
    files = generator._render_domain(empty_domain)
    directory = Path("empty")

    assert set(files) == {
        directory / "__init__.py",
        directory / "domain.py",
    }


def test_missing_ruff_has_actionable_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def raise_missing(*args: object, **kwargs: object) -> None:
        raise FileNotFoundError

    monkeypatch.setattr(formatting.subprocess, "run", raise_missing)

    with pytest.raises(RuntimeError, match=r"install cdpify\[generator\]"):
        formatting.format_python_tree(Path("generated"))


def test_domain_packages_cannot_overwrite_each_other() -> None:
    domains = [Domain(domain="IndexedDB"), Domain(domain="IndexedDb")]
    with pytest.raises(ValueError, match="Duplicate domain module names: indexed_db"):
        generator._render_files(domains)
