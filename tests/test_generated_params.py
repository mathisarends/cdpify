from dataclasses import fields

import pytest

from cdpify import encode_cdp
from cdpify.domains.runtime import CallArgument, CallFunctionOnParams, EvaluateParams
from cdpify.domains.runtime.domain import Runtime


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
    class Executor:
        async def execute(self, *, method, params):
            assert params == encode_cdp(expected)
            return {"result": {"type": "undefined"}}

    expected = params
    await getattr(Runtime(Executor()), method)(
        **{f.name: getattr(params, f.name) for f in fields(params)}
    )
