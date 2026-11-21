from dataclasses import fields
from typing import get_type_hints

import pytest

from cdpify import encode_cdp
from cdpify.domains.network import LoaderId
from cdpify.domains.page import Page
from cdpify.domains.runtime import CallArgument, CallFunctionOnParams, EvaluateParams
from cdpify.domains.runtime.domain import Runtime


def test_generated_method_type_hints_resolve_cross_domain_types() -> None:
    assert get_type_hints(Page.reload)["loader_id"] == LoaderId | None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params,method",
    [
        (
            EvaluateParams(expression="1", return_by_value=False, context_id=0),
            "evaluate",
        ),
        (
            CallFunctionOnParams(
                function_declaration="function(x) { return x; }",
                arguments=[CallArgument(value=None)],
            ),
            "call_function_on",
        ),
        (
            CallFunctionOnParams(function_declaration="function() {}", arguments=[]),
            "call_function_on",
        ),
    ],
)
async def test_generated_wire_params_match_public_params_models(params, method) -> None:
    sent = []

    class Executor:
        async def execute(self, *, method, params):
            sent.append(params)
            return {"result": {"type": "undefined"}}

    await getattr(Runtime(Executor()), method)(
        **{f.name: getattr(params, f.name) for f in fields(params)}
    )

    assert sent == [encode_cdp(params)]
