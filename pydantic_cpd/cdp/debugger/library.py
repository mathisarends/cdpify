"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    ContinueToLocationParams,
    DisassembleWasmModuleParams,
    DisassembleWasmModuleResult,
    EnableParams,
    EnableResult,
    EvaluateOnCallFrameParams,
    EvaluateOnCallFrameResult,
    GetPossibleBreakpointsParams,
    GetPossibleBreakpointsResult,
    GetScriptSourceParams,
    GetScriptSourceResult,
    GetStackTraceParams,
    GetStackTraceResult,
    GetWasmBytecodeParams,
    GetWasmBytecodeResult,
    NextWasmDisassemblyChunkParams,
    NextWasmDisassemblyChunkResult,
    PauseOnAsyncCallParams,
    RemoveBreakpointParams,
    RestartFrameParams,
    RestartFrameResult,
    ResumeParams,
    SearchInContentParams,
    SearchInContentResult,
    SetAsyncCallStackDepthParams,
    SetBlackboxExecutionContextsParams,
    SetBlackboxPatternsParams,
    SetBlackboxedRangesParams,
    SetBreakpointByUrlParams,
    SetBreakpointByUrlResult,
    SetBreakpointOnFunctionCallParams,
    SetBreakpointOnFunctionCallResult,
    SetBreakpointParams,
    SetBreakpointResult,
    SetBreakpointsActiveParams,
    SetInstrumentationBreakpointParams,
    SetInstrumentationBreakpointResult,
    SetPauseOnExceptionsParams,
    SetReturnValueParams,
    SetScriptSourceParams,
    SetScriptSourceResult,
    SetSkipAllPausesParams,
    SetVariableValueParams,
    StepIntoParams,
    StepOverParams,
)

class DebuggerClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def continue_to_location(
        self, params: ContinueToLocationParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.continueToLocation",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, params: EnableParams | None = None, session_id: str | None = None
    ) -> EnableResult:
        result = await self._client.send_raw(
            method="Debugger.enable",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return EnableResult.model_validate(result)

    async def evaluate_on_call_frame(
        self, params: EvaluateOnCallFrameParams, session_id: str | None = None
    ) -> EvaluateOnCallFrameResult:
        result = await self._client.send_raw(
            method="Debugger.evaluateOnCallFrame",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return EvaluateOnCallFrameResult.model_validate(result)

    async def get_possible_breakpoints(
        self, params: GetPossibleBreakpointsParams, session_id: str | None = None
    ) -> GetPossibleBreakpointsResult:
        result = await self._client.send_raw(
            method="Debugger.getPossibleBreakpoints",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetPossibleBreakpointsResult.model_validate(result)

    async def get_script_source(
        self, params: GetScriptSourceParams, session_id: str | None = None
    ) -> GetScriptSourceResult:
        result = await self._client.send_raw(
            method="Debugger.getScriptSource",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetScriptSourceResult.model_validate(result)

    async def disassemble_wasm_module(
        self, params: DisassembleWasmModuleParams, session_id: str | None = None
    ) -> DisassembleWasmModuleResult:
        result = await self._client.send_raw(
            method="Debugger.disassembleWasmModule",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return DisassembleWasmModuleResult.model_validate(result)

    async def next_wasm_disassembly_chunk(
        self, params: NextWasmDisassemblyChunkParams, session_id: str | None = None
    ) -> NextWasmDisassemblyChunkResult:
        result = await self._client.send_raw(
            method="Debugger.nextWasmDisassemblyChunk",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return NextWasmDisassemblyChunkResult.model_validate(result)

    async def get_wasm_bytecode(
        self, params: GetWasmBytecodeParams, session_id: str | None = None
    ) -> GetWasmBytecodeResult:
        result = await self._client.send_raw(
            method="Debugger.getWasmBytecode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetWasmBytecodeResult.model_validate(result)

    async def get_stack_trace(
        self, params: GetStackTraceParams, session_id: str | None = None
    ) -> GetStackTraceResult:
        result = await self._client.send_raw(
            method="Debugger.getStackTrace",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetStackTraceResult.model_validate(result)

    async def pause(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.pause",
            params=None,
            session_id=session_id,
        )
        return result

    async def pause_on_async_call(
        self, params: PauseOnAsyncCallParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.pauseOnAsyncCall",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def remove_breakpoint(
        self, params: RemoveBreakpointParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.removeBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def restart_frame(
        self, params: RestartFrameParams, session_id: str | None = None
    ) -> RestartFrameResult:
        result = await self._client.send_raw(
            method="Debugger.restartFrame",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return RestartFrameResult.model_validate(result)

    async def resume(
        self, params: ResumeParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.resume",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def search_in_content(
        self, params: SearchInContentParams, session_id: str | None = None
    ) -> SearchInContentResult:
        result = await self._client.send_raw(
            method="Debugger.searchInContent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SearchInContentResult.model_validate(result)

    async def set_async_call_stack_depth(
        self, params: SetAsyncCallStackDepthParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.setAsyncCallStackDepth",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_blackbox_execution_contexts(
        self, params: SetBlackboxExecutionContextsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.setBlackboxExecutionContexts",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_blackbox_patterns(
        self, params: SetBlackboxPatternsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.setBlackboxPatterns",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_blackboxed_ranges(
        self, params: SetBlackboxedRangesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.setBlackboxedRanges",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_breakpoint(
        self, params: SetBreakpointParams, session_id: str | None = None
    ) -> SetBreakpointResult:
        result = await self._client.send_raw(
            method="Debugger.setBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetBreakpointResult.model_validate(result)

    async def set_instrumentation_breakpoint(
        self, params: SetInstrumentationBreakpointParams, session_id: str | None = None
    ) -> SetInstrumentationBreakpointResult:
        result = await self._client.send_raw(
            method="Debugger.setInstrumentationBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetInstrumentationBreakpointResult.model_validate(result)

    async def set_breakpoint_by_url(
        self, params: SetBreakpointByUrlParams, session_id: str | None = None
    ) -> SetBreakpointByUrlResult:
        result = await self._client.send_raw(
            method="Debugger.setBreakpointByUrl",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetBreakpointByUrlResult.model_validate(result)

    async def set_breakpoint_on_function_call(
        self, params: SetBreakpointOnFunctionCallParams, session_id: str | None = None
    ) -> SetBreakpointOnFunctionCallResult:
        result = await self._client.send_raw(
            method="Debugger.setBreakpointOnFunctionCall",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetBreakpointOnFunctionCallResult.model_validate(result)

    async def set_breakpoints_active(
        self, params: SetBreakpointsActiveParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.setBreakpointsActive",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_pause_on_exceptions(
        self, params: SetPauseOnExceptionsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.setPauseOnExceptions",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_return_value(
        self, params: SetReturnValueParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.setReturnValue",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_script_source(
        self, params: SetScriptSourceParams, session_id: str | None = None
    ) -> SetScriptSourceResult:
        result = await self._client.send_raw(
            method="Debugger.setScriptSource",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetScriptSourceResult.model_validate(result)

    async def set_skip_all_pauses(
        self, params: SetSkipAllPausesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.setSkipAllPauses",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_variable_value(
        self, params: SetVariableValueParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.setVariableValue",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def step_into(
        self, params: StepIntoParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.stepInto",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def step_out(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.stepOut",
            params=None,
            session_id=session_id,
        )
        return result

    async def step_over(
        self, params: StepOverParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Debugger.stepOver",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
