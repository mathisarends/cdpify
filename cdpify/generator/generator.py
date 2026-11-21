import shutil
from pathlib import Path

from cdpify.generator.formatting import format_python_tree
from cdpify.generator.generators import (
    accessors,
    commands,
    events,
    init,
    types,
)
from cdpify.generator.generators import (
    domain as domain_generator,
)
from cdpify.generator.generators.utils import require_unique_names
from cdpify.generator.schemas import Domain
from cdpify.shared.naming import to_snake_case


def generate_domains(domains: list[Domain], output_dir: Path) -> None:
    generated_files = _render_files(domains)
    _replace_output(generated_files, output_dir)
    format_python_tree(output_dir)


def _render_files(domains: list[Domain]) -> dict[Path, str]:
    require_unique_names(
        (to_snake_case(d.domain) for d in domains), "domain module names"
    )
    files = {
        Path("accessors.py"): accessors.generate(domains),
        Path("__init__.py"): init.generate_root(domains),
    }

    for domain in domains:
        files.update(_render_domain(domain))

    return files


def _render_domain(domain: Domain) -> dict[Path, str]:
    directory = Path(to_snake_case(domain.domain))
    files = {
        directory / "domain.py": domain_generator.generate(domain),
        directory / "__init__.py": init.generate(domain),
    }

    if domain.types:
        files[directory / "types.py"] = types.generate(domain)
    if domain.commands:
        files[directory / "commands.py"] = commands.generate(domain)
    if domain.events:
        files[directory / "events.py"] = events.generate(domain)

    return files


def _replace_output(files: dict[Path, str], output_dir: Path) -> None:
    shutil.rmtree(output_dir, ignore_errors=True)

    for relative_path, source in files.items():
        output_path = output_dir / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(source, encoding="utf-8")
