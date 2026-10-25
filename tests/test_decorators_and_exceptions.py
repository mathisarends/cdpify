import pytest

import cdpify
from cdpify import exceptions
from cdpify.exceptions import CDPCommandError, CDPTimeoutError
from cdpify.shared.decorators import deprecated


def test_command_error_from_empty_response_uses_defaults() -> None:
    error = CDPCommandError.from_response("Page.enable", {})

    assert error.code == -1
    assert error.message == "Unknown error"
    assert error.data is None
    assert str(error) == "Page.enable failed with CDP error -1: Unknown error"


def test_command_error_includes_data_in_message() -> None:
    error = CDPCommandError.from_response(
        "DOM.getDocument",
        {"code": -32602, "message": "Invalid parameters", "data": "depth: int"},
    )

    assert str(error) == (
        "DOM.getDocument failed with CDP error -32602: Invalid parameters (depth: int)"
    )


def test_timeout_error_is_builtin_timeout_error() -> None:
    assert issubclass(CDPTimeoutError, TimeoutError)


@pytest.mark.parametrize("module", [cdpify, exceptions])
@pytest.mark.parametrize(
    ("old_name", "new_name"),
    [
        ("CDPException", "CDPError"),
        ("CDPConnectionException", "CDPConnectionError"),
        ("CDPCommandException", "CDPCommandError"),
        ("CDPTimeoutException", "CDPTimeoutError"),
    ],
)
def test_old_exception_names_are_deprecated_aliases(
    module: object, old_name: str, new_name: str
) -> None:
    with pytest.deprecated_call(match=new_name):
        alias = getattr(module, old_name)

    assert alias is getattr(exceptions, new_name)


def test_deprecated_sync_function_logs_warning(
    caplog: pytest.LogCaptureFixture,
) -> None:
    @deprecated()
    def old_fn(value: int) -> int:
        return value + 1

    with caplog.at_level("WARNING"):
        result = old_fn(1)

    assert result == 2
    assert "old_fn is deprecated" in caplog.text


@pytest.mark.asyncio
async def test_deprecated_async_function_logs_warning(
    caplog: pytest.LogCaptureFixture,
) -> None:
    @deprecated()
    async def old_async_fn(value: int) -> int:
        return value + 2

    with caplog.at_level("WARNING"):
        result = await old_async_fn(1)

    assert result == 3
    assert "old_async_fn is deprecated" in caplog.text
