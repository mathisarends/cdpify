"""Generated client library from CDP specification"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic_cpd.client import CDPClient

from .commands import (
    DispatchDragEventParams,
    DispatchKeyEventParams,
    DispatchMouseEventParams,
    DispatchTouchEventParams,
    EmulateTouchFromMouseEventParams,
    ImeSetCompositionParams,
    InsertTextParams,
    SetIgnoreInputEventsParams,
    SetInterceptDragsParams,
    SynthesizePinchGestureParams,
    SynthesizeScrollGestureParams,
    SynthesizeTapGestureParams,
)

class InputClient:
    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def dispatch_drag_event(
        self, params: DispatchDragEventParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.dispatchDragEvent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def dispatch_key_event(
        self, params: DispatchKeyEventParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.dispatchKeyEvent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def insert_text(
        self, params: InsertTextParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.insertText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def ime_set_composition(
        self, params: ImeSetCompositionParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.imeSetComposition",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def dispatch_mouse_event(
        self, params: DispatchMouseEventParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.dispatchMouseEvent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def dispatch_touch_event(
        self, params: DispatchTouchEventParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.dispatchTouchEvent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def cancel_dragging(
        self, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.cancelDragging",
            params=None,
            session_id=session_id,
        )
        return result

    async def emulate_touch_from_mouse_event(
        self, params: EmulateTouchFromMouseEventParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.emulateTouchFromMouseEvent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_ignore_input_events(
        self, params: SetIgnoreInputEventsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.setIgnoreInputEvents",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_intercept_drags(
        self, params: SetInterceptDragsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.setInterceptDrags",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def synthesize_pinch_gesture(
        self, params: SynthesizePinchGestureParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.synthesizePinchGesture",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def synthesize_scroll_gesture(
        self, params: SynthesizeScrollGestureParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.synthesizeScrollGesture",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def synthesize_tap_gesture(
        self, params: SynthesizeTapGestureParams, session_id: str | None = None
    ) -> dict[str, Any]:
        result = await self._client.send_raw(
            method="Input.synthesizeTapGesture",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
