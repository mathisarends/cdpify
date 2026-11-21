from cdpify.generator.generators.constants import HEADER
from cdpify.generator.generators.utils import to_snake_case
from cdpify.generator.generators.views import DomainView
from cdpify.generator.rendering import render_template
from cdpify.generator.schemas import Domain


def generate(domains: list[Domain]) -> str:
    return render_template(
        "accessors.py.jinja2",
        header=HEADER,
        domains=tuple(
            DomainView(
                name=domain.domain,
                module=to_snake_case(domain.domain),
                property_name=to_snake_case(domain.domain),
            )
            for domain in domains
        ),
    )
