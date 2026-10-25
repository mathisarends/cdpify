from cdpify.generator.generators import accessors
from cdpify.generator.schemas import Domain


def test_generates_typed_cached_domain_accessors() -> None:
    output = accessors.generate([Domain(domain="Page"), Domain(domain="DOMStorage")])

    assert "    from cdpify.executor import CommandExecutor" in output
    assert "class DomainAccessors:" in output
    assert "_executor: CommandExecutor" in output
    assert "def __init__" not in output
    assert "from .page import Page" in output
    assert "from .domstorage import DOMStorage" in output
    assert "@cached_property" in output
    assert "def page(self) -> Page:" in output
    assert "def dom_storage(self) -> DOMStorage:" in output
    assert "return Page(self._executor)" in output


def test_accessors_import_domains_on_first_access() -> None:
    output = accessors.generate([Domain(domain="Page")])

    type_checking_block, class_body = output.split("class DomainAccessors:")
    assert "if TYPE_CHECKING:" in type_checking_block
    assert "    from .page import Page" in type_checking_block
    assert "        from .page import Page\n" in class_body
