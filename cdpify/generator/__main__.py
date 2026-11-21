import argparse
from collections.abc import Sequence
from pathlib import Path

from .downloader import download_specs
from .generator import generate_domains
from .schemas import CDPSpecs, Domain

__all__ = ["main"]

_PROJECT_ROOT = Path(__file__).parents[2]
_DEFAULT_SPEC_DIR = _PROJECT_ROOT / "specs"
_DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent / "domains"


def main(argv: Sequence[str] | None = None) -> None:
    parser = _create_parser()
    args = parser.parse_args(argv)

    print(f"Downloading CDP specifications to {args.spec_dir}...")
    specs = download_specs(args.spec_dir)

    try:
        domains = _select_domains(specs, args.domain_names)
    except ValueError as error:
        parser.error(str(error))

    print(f"Generating {len(domains)} CDP domains in {args.output_dir}...")
    generate_domains(domains, args.output_dir)
    print("Generation complete.")


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate the typed CDP client.")
    parser.add_argument(
        "--domain",
        action="append",
        dest="domain_names",
        metavar="NAME",
        help="generate only this CDP domain; may be specified multiple times",
    )
    parser.add_argument(
        "--spec-dir",
        type=Path,
        default=_DEFAULT_SPEC_DIR,
        help=f"directory for downloaded specifications (default: {_DEFAULT_SPEC_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_DEFAULT_OUTPUT_DIR,
        help=f"directory for generated modules (default: {_DEFAULT_OUTPUT_DIR})",
    )
    return parser


def _select_domains(specs: CDPSpecs, requested_names: list[str] | None) -> list[Domain]:
    if requested_names is None:
        return specs.all_domains

    domains: list[Domain] = []
    unknown_names: list[str] = []

    for name in dict.fromkeys(requested_names):
        domain = specs.get_domain(name)
        if domain is None:
            unknown_names.append(name)
        else:
            domains.append(domain)

    if unknown_names:
        joined_names = ", ".join(unknown_names)
        raise ValueError(f"Unknown CDP domain(s): {joined_names}")

    return domains


if __name__ == "__main__":
    main()
