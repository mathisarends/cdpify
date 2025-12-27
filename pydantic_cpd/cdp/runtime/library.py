"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    AddBindingParams,
    AwaitPromiseParams,
    AwaitPromiseResult,
    CallFunctionOnParams,
    CallFunctionOnResult,
    CompileScriptParams,
    CompileScriptResult,
    EvaluateParams,
    EvaluateResult,
    GetExceptionDetailsParams,
    GetExceptionDetailsResult,
    GetHeapUsageResult,
    GetIsolateIdResult,
    GetPropertiesParams,
    GetPropertiesResult,
    GlobalLexicalScopeNamesParams,
    GlobalLexicalScopeNamesResult,
    QueryObjectsParams,
    QueryObjectsResult,
    ReleaseObjectGroupParams,
    ReleaseObjectParams,
    RemoveBindingParams,
    RunScriptParams,
    RunScriptResult,
    SetAsyncCallStackDepthParams,
    SetCustomObjectFormatterEnabledParams,
    SetMaxCallStackSizeToCaptureParams,
)

class RuntimeClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def await_promise(
        self, params: AwaitPromiseParams, session_id: str | None = None
    ) -> AwaitPromiseResult:
        result = await self._client.send_raw(
            method="Runtime.awaitPromise",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return AwaitPromiseResult.model_validate(result)

    async def call_function_on(
        self, params: CallFunctionOnParams, session_id: str | None = None
    ) -> CallFunctionOnResult:
        result = await self._client.send_raw(
            method="Runtime.callFunctionOn",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CallFunctionOnResult.model_validate(result)

    async def compile_script(
        self, params: CompileScriptParams, session_id: str | None = None
    ) -> CompileScriptResult:
        result = await self._client.send_raw(
            method="Runtime.compileScript",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return CompileScriptResult.model_validate(result)

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Runtime.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def discard_console_entries(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Runtime.discardConsoleEntries",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Runtime.enable",
            params=None,
            session_id=session_id,
        )
        return result

    async def evaluate(
        self, params: EvaluateParams, session_id: str | None = None
    ) -> EvaluateResult:
        result = await self._client.send_raw(
            method="Runtime.evaluate",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return EvaluateResult.model_validate(result)

    async def get_isolate_id(
        self, session_id: str | None = None
    ) -> GetIsolateIdResult:
        result = await self._client.send_raw(
            method="Runtime.getIsolateId",
            params=None,
            session_id=session_id,
        )
        return GetIsolateIdResult.model_validate(result)

    async def get_heap_usage(
        self, session_id: str | None = None
    ) -> GetHeapUsageResult:
        result = await self._client.send_raw(
            method="Runtime.getHeapUsage",
            params=None,
            session_id=session_id,
        )
        return GetHeapUsageResult.model_validate(result)

    async def get_properties(
        self, params: GetPropertiesParams, session_id: str | None = None
    ) -> GetPropertiesResult:
        result = await self._client.send_raw(
            method="Runtime.getProperties",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetPropertiesResult.model_validate(result)

    async def global_lexical_scope_names(
        self, params: GlobalLexicalScopeNamesParams | None = None, session_id: str | None = None
    ) -> GlobalLexicalScopeNamesResult:
        result = await self._client.send_raw(
            method="Runtime.globalLexicalScopeNames",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GlobalLexicalScopeNamesResult.model_validate(result)

    async def query_objects(
        self, params: QueryObjectsParams, session_id: str | None = None
    ) -> QueryObjectsResult:
        result = await self._client.send_raw(
            method="Runtime.queryObjects",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return QueryObjectsResult.model_validate(result)

    async def release_object(
        self, params: ReleaseObjectParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Runtime.releaseObject",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def release_object_group(
        self, params: ReleaseObjectGroupParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Runtime.releaseObjectGroup",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def run_if_waiting_for_debugger(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Runtime.runIfWaitingForDebugger",
            params=None,
            session_id=session_id,
        )
        return result

    async def run_script(
        self, params: RunScriptParams, session_id: str | None = None
    ) -> RunScriptResult:
        result = await self._client.send_raw(
            method="Runtime.runScript",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return RunScriptResult.model_validate(result)

    async def set_async_call_stack_depth(
        self, params: SetAsyncCallStackDepthParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Runtime.setAsyncCallStackDepth",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_custom_object_formatter_enabled(
        self, params: SetCustomObjectFormatterEnabledParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Runtime.setCustomObjectFormatterEnabled",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_max_call_stack_size_to_capture(
        self, params: SetMaxCallStackSizeToCaptureParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Runtime.setMaxCallStackSizeToCapture",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def terminate_execution(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Runtime.terminateExecution",
            params=None,
            session_id=session_id,
        )
        return result

    async def add_binding(
        self, params: AddBindingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Runtime.addBinding",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def remove_binding(
        self, params: RemoveBindingParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Runtime.removeBinding",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def get_exception_details(
        self, params: GetExceptionDetailsParams, session_id: str | None = None
    ) -> GetExceptionDetailsResult:
        result = await self._client.send_raw(
            method="Runtime.getExceptionDetails",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetExceptionDetailsResult.model_validate(result)
