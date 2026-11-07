"""Check generated modules against bundled specs, or regenerate with --write."""

import argparse
import tempfile
from pathlib import Path

from cdpify.generator.generator import generate_domains
from cdpify.generator.schemas import CDPSpecs, ProtocolSpec


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    committed = (root / "cdpify/domains").resolve()
    if not committed.is_relative_to(root) or committed.name != "domains":
        raise ValueError("Generated output must stay inside the repository")
    specs = CDPSpecs(
        **{
            kind: ProtocolSpec.model_validate_json(
                (root / "specs" / filename).read_text(encoding="utf-8")
            )
            for kind, filename in (
                ("browser", "browser_protocol.json"),
                ("js", "js_protocol.json"),
            )
        }
    )
    if args.write:
        generate_domains(specs.all_domains, committed)
        return
    with tempfile.TemporaryDirectory(prefix="cdpify-generated-") as directory:
        temporary = Path(directory).resolve()
        generated = (temporary / "domains").resolve()
        assert generated.is_relative_to(temporary)
        generate_domains(specs.all_domains, generated)
        expected = _sources(generated)
        actual = _sources(committed)
        changed = sorted(
            p
            for p in expected.keys() | actual.keys()
            if expected.get(p) != actual.get(p)
        )
        if changed:
            raise SystemExit("Generated code drift: " + ", ".join(map(str, changed)))
    print("Generated code matches the bundled specs.")


def _sources(directory: Path) -> dict[Path, bytes]:
    return {
        p.relative_to(directory): p.read_bytes().replace(b"\r\n", b"\n")
        for p in directory.rglob("*.py")
    }


if __name__ == "__main__":
    main()
