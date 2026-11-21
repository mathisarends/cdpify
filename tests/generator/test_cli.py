from pathlib import Path

import pytest

from cdpify.generator import __main__ as cli
from cdpify.generator.schemas import CDPSpecs, Domain


@pytest.fixture
def downloaded_specs(monkeypatch, sample_protocol_spec) -> CDPSpecs:
    js = sample_protocol_spec.model_copy(update={"domains": [Domain(domain="Other")]})
    specs = CDPSpecs(browser=sample_protocol_spec, js=js)
    monkeypatch.setattr(cli, "download_specs", lambda _: specs)
    return specs


@pytest.mark.parametrize(
    ("selection", "expected"),
    [
        ([], ["Sample", "Other"]),
        (
            ["--domain", "Other", "--domain", "Sample", "--domain", "Other"],
            ["Other", "Sample"],
        ),
    ],
)
def test_cli_selects_domains(
    monkeypatch, downloaded_specs, tmp_path, selection, expected
):
    selected = []
    monkeypatch.setattr(
        cli, "generate_domains", lambda domains, _: selected.extend(domains)
    )

    cli.main(["--spec-dir", str(tmp_path), *selection])

    assert [domain.domain for domain in selected] == expected


def test_cli_rejects_unknown_domains(downloaded_specs, tmp_path, capsys):
    with pytest.raises(SystemExit) as error:
        cli.main(
            [
                "--domain",
                "Missing",
                "--spec-dir",
                str(tmp_path),
                "--output-dir",
                str(tmp_path / "output"),
            ]
        )

    assert error.value.code == 2
    assert "Unknown CDP domain(s): Missing" in capsys.readouterr().err
    assert not (tmp_path / "output").exists()


def test_main_passes_explicit_paths_and_selection(
    monkeypatch: pytest.MonkeyPatch,
    sample_protocol_spec,
    tmp_path: Path,
) -> None:
    specs = CDPSpecs(browser=sample_protocol_spec, js=sample_protocol_spec)
    spec_dir = tmp_path / "specs"
    output_dir = tmp_path / "domains"
    downloaded: list[Path] = []
    generated: list[tuple[list[Domain], Path]] = []

    def download(destination: Path) -> CDPSpecs:
        downloaded.append(destination)
        return specs

    monkeypatch.setattr(cli, "download_specs", download)
    monkeypatch.setattr(
        cli,
        "generate_domains",
        lambda domains, destination: generated.append((domains, destination)),
    )

    cli.main(
        [
            "--domain",
            "Sample",
            "--spec-dir",
            str(spec_dir),
            "--output-dir",
            str(output_dir),
        ]
    )

    assert downloaded == [spec_dir]
    assert generated == [([sample_protocol_spec.domains[0]], output_dir)]
