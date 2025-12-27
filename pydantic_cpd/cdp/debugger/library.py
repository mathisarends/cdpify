"""Generated client library from CDP specification"""
# Domain: Debugger Client

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
    """Debugger domain exposes JavaScript debugging capabilities. It allows setting and removing
    breakpoints, stepping through execution, exploring stack traces, etc."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def continue_to_location(
        self, params: ContinueToLocationParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Continues execution until specific location is reached."""
        result = await self._client.send_raw(
            method="Debugger.continueToLocation",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def disable(self, session_id: str | None = None) -> dict[str, Any]:
        """Disables debugger for given page."""
        result = await self._client.send_raw(
            method="Debugger.disable",
            params=None,
            session_id=session_id,
        )
        return result

    async def enable(
        self, params: EnableParams | None = None, session_id: str | None = None
    ) -> EnableResult:
        """Enables debugger for the given page. Clients should not assume that the debugging has been
        enabled until the result for this command is received."""
        result = await self._client.send_raw(
            method="Debugger.enable",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return EnableResult.model_validate(result)

    async def evaluate_on_call_frame(
        self, params: EvaluateOnCallFrameParams, session_id: str | None = None
    ) -> EvaluateOnCallFrameResult:
        """Evaluates expression on a given call frame."""
        result = await self._client.send_raw(
            method="Debugger.evaluateOnCallFrame",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return EvaluateOnCallFrameResult.model_validate(result)

    async def get_possible_breakpoints(
        self, params: GetPossibleBreakpointsParams, session_id: str | None = None
    ) -> GetPossibleBreakpointsResult:
        """Returns possible locations for breakpoint. scriptId in start and end range locations should be
        the same."""
        result = await self._client.send_raw(
            method="Debugger.getPossibleBreakpoints",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetPossibleBreakpointsResult.model_validate(result)

    async def get_script_source(
        self, params: GetScriptSourceParams, session_id: str | None = None
    ) -> GetScriptSourceResult:
        """Returns source for the script with given id."""
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
        """Disassemble the next chunk of lines for the module corresponding to the
        stream. If disassembly is complete, this API will invalidate the streamId
        and return an empty chunk. Any subsequent calls for the now invalid stream
        will return errors."""
        result = await self._client.send_raw(
            method="Debugger.nextWasmDisassemblyChunk",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return NextWasmDisassemblyChunkResult.model_validate(result)

    async def get_wasm_bytecode(
        self, params: GetWasmBytecodeParams, session_id: str | None = None
    ) -> GetWasmBytecodeResult:
        """This command is deprecated. Use getScriptSource instead."""
        result = await self._client.send_raw(
            method="Debugger.getWasmBytecode",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetWasmBytecodeResult.model_validate(result)

    async def get_stack_trace(
        self, params: GetStackTraceParams, session_id: str | None = None
    ) -> GetStackTraceResult:
        """Returns stack trace with given `stackTraceId`."""
        result = await self._client.send_raw(
            method="Debugger.getStackTrace",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return GetStackTraceResult.model_validate(result)

    async def pause(self, session_id: str | None = None) -> dict[str, Any]:
        """Stops on the next JavaScript statement."""
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
        """Removes JavaScript breakpoint."""
        result = await self._client.send_raw(
            method="Debugger.removeBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def restart_frame(
        self, params: RestartFrameParams, session_id: str | None = None
    ) -> RestartFrameResult:
        """Restarts particular call frame from the beginning. The old, deprecated
        behavior of `restartFrame` is to stay paused and allow further CDP commands
        after a restart was scheduled. This can cause problems with restarting, so
        we now continue execution immediatly after it has been scheduled until we
        reach the beginning of the restarted frame.

        To stay back-wards compatible, `restartFrame` now expects a `mode`
        parameter to be present. If the `mode` parameter is missing, `restartFrame`
        errors out.

        The various return values are deprecated and `callFrames` is always empty.
        Use the call frames from the `Debugger#paused` events instead, that fires
        once V8 pauses at the beginning of the restarted function."""
        result = await self._client.send_raw(
            method="Debugger.restartFrame",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return RestartFrameResult.model_validate(result)

    async def resume(
        self, params: ResumeParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Resumes JavaScript execution."""
        result = await self._client.send_raw(
            method="Debugger.resume",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def search_in_content(
        self, params: SearchInContentParams, session_id: str | None = None
    ) -> SearchInContentResult:
        """Searches for given string in script content."""
        result = await self._client.send_raw(
            method="Debugger.searchInContent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SearchInContentResult.model_validate(result)

    async def set_async_call_stack_depth(
        self, params: SetAsyncCallStackDepthParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Enables or disables async call stacks tracking."""
        result = await self._client.send_raw(
            method="Debugger.setAsyncCallStackDepth",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_blackbox_execution_contexts(
        self, params: SetBlackboxExecutionContextsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Replace previous blackbox execution contexts with passed ones. Forces backend to skip
        stepping/pausing in scripts in these execution contexts. VM will try to leave blackboxed script by
        performing 'step in' several times, finally resorting to 'step out' if unsuccessful."""
        result = await self._client.send_raw(
            method="Debugger.setBlackboxExecutionContexts",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_blackbox_patterns(
        self, params: SetBlackboxPatternsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Replace previous blackbox patterns with passed ones. Forces backend to skip stepping/pausing in
        scripts with url matching one of the patterns. VM will try to leave blackboxed script by
        performing 'step in' several times, finally resorting to 'step out' if unsuccessful."""
        result = await self._client.send_raw(
            method="Debugger.setBlackboxPatterns",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_blackboxed_ranges(
        self, params: SetBlackboxedRangesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Makes backend skip steps in the script in blackboxed ranges. VM will try leave blacklisted
        scripts by performing 'step in' several times, finally resorting to 'step out' if unsuccessful.
        Positions array contains positions where blackbox state is changed. First interval isn't
        blackboxed. Array should be sorted."""
        result = await self._client.send_raw(
            method="Debugger.setBlackboxedRanges",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_breakpoint(
        self, params: SetBreakpointParams, session_id: str | None = None
    ) -> SetBreakpointResult:
        """Sets JavaScript breakpoint at a given location."""
        result = await self._client.send_raw(
            method="Debugger.setBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetBreakpointResult.model_validate(result)

    async def set_instrumentation_breakpoint(
        self, params: SetInstrumentationBreakpointParams, session_id: str | None = None
    ) -> SetInstrumentationBreakpointResult:
        """Sets instrumentation breakpoint."""
        result = await self._client.send_raw(
            method="Debugger.setInstrumentationBreakpoint",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetInstrumentationBreakpointResult.model_validate(result)

    async def set_breakpoint_by_url(
        self, params: SetBreakpointByUrlParams, session_id: str | None = None
    ) -> SetBreakpointByUrlResult:
        """Sets JavaScript breakpoint at given location specified either by URL or URL regex. Once this
        command is issued, all existing parsed scripts will have breakpoints resolved and returned in
        `locations` property. Further matching script parsing will result in subsequent
        `breakpointResolved` events issued. This logical breakpoint will survive page reloads."""
        result = await self._client.send_raw(
            method="Debugger.setBreakpointByUrl",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetBreakpointByUrlResult.model_validate(result)

    async def set_breakpoint_on_function_call(
        self, params: SetBreakpointOnFunctionCallParams, session_id: str | None = None
    ) -> SetBreakpointOnFunctionCallResult:
        """Sets JavaScript breakpoint before each call to the given function.
        If another function was created from the same source as a given one,
        calling it will also trigger the breakpoint."""
        result = await self._client.send_raw(
            method="Debugger.setBreakpointOnFunctionCall",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetBreakpointOnFunctionCallResult.model_validate(result)

    async def set_breakpoints_active(
        self, params: SetBreakpointsActiveParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Activates / deactivates all breakpoints on the page."""
        result = await self._client.send_raw(
            method="Debugger.setBreakpointsActive",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_pause_on_exceptions(
        self, params: SetPauseOnExceptionsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Defines pause on exceptions state. Can be set to stop on all exceptions, uncaught exceptions,
        or caught exceptions, no exceptions. Initial pause on exceptions state is `none`."""
        result = await self._client.send_raw(
            method="Debugger.setPauseOnExceptions",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_return_value(
        self, params: SetReturnValueParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Changes return value in top frame. Available only at return break position."""
        result = await self._client.send_raw(
            method="Debugger.setReturnValue",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_script_source(
        self, params: SetScriptSourceParams, session_id: str | None = None
    ) -> SetScriptSourceResult:
        """Edits JavaScript source live.

        In general, functions that are currently on the stack can not be edited with
        a single exception: If the edited function is the top-most stack frame and
        that is the only activation of that function on the stack. In this case
        the live edit will be successful and a `Debugger.restartFrame` for the
        top-most function is automatically triggered."""
        result = await self._client.send_raw(
            method="Debugger.setScriptSource",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return SetScriptSourceResult.model_validate(result)

    async def set_skip_all_pauses(
        self, params: SetSkipAllPausesParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Makes page not interrupt on any pauses (breakpoint, exception, dom exception etc)."""
        result = await self._client.send_raw(
            method="Debugger.setSkipAllPauses",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_variable_value(
        self, params: SetVariableValueParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Changes value of variable in a callframe. Object-based scopes are not supported and must be
        mutated manually."""
        result = await self._client.send_raw(
            method="Debugger.setVariableValue",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def step_into(
        self, params: StepIntoParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Steps into the function call."""
        result = await self._client.send_raw(
            method="Debugger.stepInto",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def step_out(self, session_id: str | None = None) -> dict[str, Any]:
        """Steps out of the function call."""
        result = await self._client.send_raw(
            method="Debugger.stepOut",
            params=None,
            session_id=session_id,
        )
        return result

    async def step_over(
        self, params: StepOverParams | None = None, session_id: str | None = None
    ) -> dict[str, Any]:
        """Steps over the statement."""
        result = await self._client.send_raw(
            method="Debugger.stepOver",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
