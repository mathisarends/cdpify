from cdpify.generator.generators.constants import HEADER
from cdpify.generator.generators.utils import to_pascal_case, to_snake_case
from cdpify.generator.generators.views import (
    DomainView,
    ImportBlockView,
    LazyExportView,
)
from cdpify.generator.rendering import render_template
from cdpify.generator.schemas import Domain


def generate(domain: Domain) -> str:
    type_names = [type_def.id for type_def in domain.types]
    imported_type_names = [
        f"{name} as {name}Type" if name == domain.domain else name
        for name in type_names
    ]
    command_names = _command_names(domain)
    event_names = _event_names(domain, type_names)
    domain_class = domain.domain

    type_exports = [_exported_name(name) for name in imported_type_names]
    event_exports = [_exported_name(name) for name in event_names]
    all_names = sorted([*type_exports, *command_names, *event_exports, domain_class])

    lazy_exports = [
        *_lazy_exports("types", imported_type_names),
        *_lazy_exports("commands", command_names),
        *_lazy_exports("events", event_names),
        LazyExportView(domain_class, "domain", domain_class),
    ]

    return render_template(
        "domain_init.py.jinja2",
        header=HEADER,
        domain_name=domain.domain,
        import_blocks=tuple(
            ImportBlockView(module, tuple(names))
            for module, names in (
                ("types", imported_type_names),
                ("commands", command_names),
                ("events", event_names),
            )
            if names
        ),
        domain_class=domain_class,
        exports=tuple(all_names),
        lazy_exports=tuple(sorted(lazy_exports, key=lambda export: export.name)),
    )


def generate_root(domains: list[Domain]) -> str:
    return render_template(
        "root_init.py.jinja2",
        header=HEADER,
        domains=tuple(
            DomainView(
                name=domain.domain,
                module=domain.domain.lower(),
                property_name=to_snake_case(domain.domain),
            )
            for domain in domains
        ),
    )


def _command_names(domain: Domain) -> list[str]:
    if not domain.commands:
        return []

    names = [f"{domain.domain}Command"]
    for command in domain.commands:
        pascal = to_pascal_case(command.name)
        if command.parameters:
            names.append(f"{pascal}Params")
        if command.returns:
            names.append(f"{pascal}Result")
    return sorted(names)


def _event_names(domain: Domain, type_names: list[str]) -> list[str]:
    if not domain.events:
        return []

    enum_name = f"{domain.domain}Event"
    if enum_name in type_names:
        enum_name = f"{enum_name} as {enum_name}Name"

    names = [enum_name]
    names.extend(f"{to_pascal_case(event.name)}Event" for event in domain.events)
    return sorted(names)


def _exported_name(imported_name: str) -> str:
    return imported_name.rsplit(" as ", maxsplit=1)[-1]


def _lazy_exports(module: str, imported_names: list[str]) -> list[LazyExportView]:
    exports = []
    for imported_name in imported_names:
        attribute, _, alias = imported_name.partition(" as ")
        exports.append(LazyExportView(alias or attribute, module, attribute))
    return exports
