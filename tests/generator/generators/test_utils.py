import pytest

from cdpify.generator.generators.utils import (
    format_docstring,
    map_cdp_type,
    resolve_type,
    to_enum_name,
    to_identifier,
    to_pascal_case,
    to_snake_case,
)
from cdpify.generator.schemas import Parameter


class TestToSnakeCase:
    @pytest.mark.parametrize(
        "name, expected",
        [
            ("simple", "simple"),
            ("camelCase", "camel_case"),
            ("PascalCase", "pascal_case"),
            ("setSPCTransactionMode", "set_spc_transaction_mode"),
            ("getDOMNode", "get_dom_node"),
            ("parseHTML", "parse_html"),
            ("AXTree", "ax_tree"),
            ("getSSLCertificate", "get_ssl_certificate"),
            ("X", "x"),
        ],
    )
    def test_handles_acronyms(self, name: str, expected: str) -> None:
        assert to_snake_case(name) == expected


class TestToPascalCase:
    @pytest.mark.parametrize(
        "name, expected",
        [
            ("foo", "Foo"),
            ("fooBar", "FooBar"),
            ("AlreadyPascal", "AlreadyPascal"),
            ("a", "A"),
        ],
    )
    def test_capitalizes_first_only(self, name: str, expected: str) -> None:
        assert to_pascal_case(name) == expected

    def test_empty_input(self) -> None:
        assert to_pascal_case("") == ""


class TestToEnumName:
    def test_combines_snake_case_and_upper(self) -> None:
        assert to_enum_name("getDOMNode") == "GET_DOM_NODE"
        assert to_enum_name("clear") == "CLEAR"


class TestMapCdpType:
    @pytest.mark.parametrize(
        "cdp_type, expected",
        [
            ("string", "str"),
            ("integer", "int"),
            ("number", "float"),
            ("boolean", "bool"),
            ("any", "Any"),
            ("object", "dict[str, Any]"),
        ],
    )
    def test_basic_types(self, cdp_type: str, expected: str) -> None:
        assert map_cdp_type(Parameter(name="p", type=cdp_type)) == expected

    def test_unknown_type_falls_back_to_any(self) -> None:
        assert map_cdp_type(Parameter(name="p", type="weirdtype")) == "Any"

    def test_local_ref_returns_ref_name(self) -> None:
        assert map_cdp_type(Parameter(name="p", ref="NodeId")) == "NodeId"

    def test_array_of_basic_type(self) -> None:
        param = Parameter(name="p", type="array", items={"type": "string"})
        assert map_cdp_type(param) == "list[str]"

    def test_array_of_local_ref(self) -> None:
        param = Parameter(name="p", type="array", items={"$ref": "NodeId"})
        assert map_cdp_type(param) == "list[NodeId]"

    def test_array_of_cross_domain_ref(self) -> None:
        param = Parameter(name="p", type="array", items={"$ref": "DOM.NodeId"})
        assert map_cdp_type(param) == "list[dom.NodeId]"

    def test_array_with_no_items(self) -> None:
        param = Parameter(name="p", type="array")
        assert map_cdp_type(param) == "list[Any]"

    def test_enum_produces_literal(self) -> None:
        param = Parameter(name="p", type="string", enum=["a", "b", "c"])
        assert map_cdp_type(param) == 'Literal["a", "b", "c"]'


class TestResolveType:
    def test_cross_domain_ref_lowercases_domain(self) -> None:
        param = Parameter(name="p", ref="DOM.NodeId")
        assert resolve_type(param) == "dom.NodeId"

    def test_local_ref_unchanged(self) -> None:
        param = Parameter(name="p", ref="NodeId")
        assert resolve_type(param) == "NodeId"

    def test_falls_through_to_map_cdp_type(self) -> None:
        param = Parameter(name="p", type="string")
        assert resolve_type(param) == "str"


class TestFormatDocstring:
    def test_empty_returns_empty(self) -> None:
        assert format_docstring("") == ""

    def test_wraps_with_triple_quotes(self) -> None:
        result = format_docstring("Hello world.", indent=0)
        assert result.startswith('"""')
        assert result.endswith('"""')
        assert "Hello world." in result

    def test_respects_indent(self) -> None:
        result = format_docstring("Hi.", indent=4)
        for line in result.splitlines():
            assert line.startswith("    ")

    def test_wraps_long_text(self) -> None:
        text = " ".join(["word"] * 50)
        result = format_docstring(text, indent=4)
        body_lines = [
            line for line in result.splitlines() if line.strip() and '"""' not in line
        ]
        assert len(body_lines) > 1
        assert all(len(line) <= 88 for line in body_lines)


@pytest.mark.parametrize(
    ("cdp_name", "expected"),
    [("or", "or_"), ("not", "not_"), ("from", "from_"), ("urlPattern", "url_pattern")],
)
def test_to_identifier_escapes_python_keywords(cdp_name: str, expected: str) -> None:
    assert to_identifier(cdp_name) == expected
