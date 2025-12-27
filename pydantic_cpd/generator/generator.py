from pathlib import Path

from pydantic_cpd.generator.generators import (
    CommandsGenerator,
    EventsGenerator,
    LibraryGenerator,
    TypesGenerator,
)
from pydantic_cpd.generator.models import Domain

CDP_DIR = Path(__file__).parent.parent / "cdp"


class DomainGenerator:
    def __init__(self):
        self.types_gen = TypesGenerator()
        self.commands_gen = CommandsGenerator()
        self.events_gen = EventsGenerator()
        self.library_gen = LibraryGenerator()

    def generate_all(self, domains: list[Domain]) -> None:
        self._prepare_output_dir()
        print(f"\n📝 Generating {len(domains)} domains...")

        for domain in domains:
            self._generate_domain(domain)

        self._generate_base_file()
        self._generate_init_file(domains)

        print("\n✅ Domain generation complete!")

    def _prepare_output_dir(self) -> None:
        if CDP_DIR.exists():
            import shutil

            shutil.rmtree(CDP_DIR)

        CDP_DIR.mkdir(parents=True, exist_ok=True)

    def _generate_domain(self, domain: Domain) -> None:
        domain_dir = CDP_DIR / domain.domain.lower()
        domain_dir.mkdir(exist_ok=True)

        print(f"  ✓ {domain.domain}")
        print(f"    - {len(domain.types)} types")
        print(f"    - {len(domain.commands)} commands")
        print(f"    - {len(domain.events)} events")

        (domain_dir / "types.py").write_text(self.types_gen.generate(domain))
        (domain_dir / "commands.py").write_text(self.commands_gen.generate(domain))
        (domain_dir / "events.py").write_text(self.events_gen.generate(domain))
        (domain_dir / "library.py").write_text(self.library_gen.generate(domain))
        (domain_dir / "__init__.py").write_text(self._generate_domain_init(domain))

    def _generate_domain_init(self, domain: Domain) -> str:
        return f'''"""CDP {domain.domain} Domain"""

from .types import *
from .commands import *
from .events import *
from .library import {domain.domain}Client

__all__ = ["{domain.domain}Client"]
'''

    def _generate_base_file(self) -> None:
        content = '''"""Base Pydantic models for CDP."""

from typing import Any
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CDPModel(BaseModel):
    """Base model for CDP with automatic camelCase alias generation."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )

    def to_cdp_params(self) -> dict[str, Any]:
        """Convert model to CDP parameters format."""
        return self.model_dump(by_alias=True, exclude_none=True)
'''
        (CDP_DIR / "base.py").write_text(content)
        print("  ✓ base.py")

    def _generate_init_file(self, domains: list[Domain]) -> None:
        lines = ['"""Generated CDP domains"""', ""]

        for domain in domains:
            domain_lower = domain.domain.lower()
            lines.append(f"from .{domain_lower} import {domain.domain}Client")

        lines.append("")
        lines.append("__all__ = [")
        for domain in domains:
            lines.append(f'    "{domain.domain}Client",')
        lines.append("]")

        (CDP_DIR / "__init__.py").write_text("\n".join(lines))
        print("  ✓ __init__.py")


def generate_all_domains(domains: list[Domain]) -> None:
    generator = DomainGenerator()
    generator.generate_all(domains)
