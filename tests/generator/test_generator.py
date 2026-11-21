from pathlib import Path

import pytest

from cdpify.generator import formatting, generator
from cdpify.generator.schemas import Domain


def test_generates_available_domain_modules(
    simple_domain: Domain, tmp_path: Path
) -> None:
    generator.generate_domains([simple_domain], tmp_path)
    directory = tmp_path / "sample"

    assert set(directory.glob("*.py")) == {
        directory / "__init__.py",
        directory / "domain.py",
        directory / "commands.py",
        directory / "events.py",
        directory / "types.py",
    }


def test_omits_empty_optional_modules(empty_domain: Domain, tmp_path: Path) -> None:
    generator.generate_domains([empty_domain], tmp_path)
    directory = tmp_path / "empty"

    assert set(directory.glob("*.py")) == {
        directory / "__init__.py",
        directory / "domain.py",
    }


def test_missing_ruff_has_actionable_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def raise_missing(*args: object, **kwargs: object) -> None:
        raise FileNotFoundError

    monkeypatch.setattr(formatting.subprocess, "run", raise_missing)

    with pytest.raises(RuntimeError, match=r"install cdpify\[generator\]"):
        formatting.format_python_tree(Path("generated"))


def test_domain_packages_cannot_overwrite_each_other(tmp_path: Path) -> None:
    domains = [Domain(domain="IndexedDB"), Domain(domain="IndexedDb")]
    with pytest.raises(ValueError, match="Duplicate domain module names: indexed_db"):
        generator.generate_domains(domains, tmp_path)

    assert list(tmp_path.iterdir()) == []
