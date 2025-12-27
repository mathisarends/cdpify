"""Generated client library from CDP specification"""
# Domain: Input Client

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
    """CDP Input domain client."""

    def __init__(self, client: CDPClient) -> None:
        self._client = client

    async def dispatch_drag_event(
        self, params: DispatchDragEventParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Dispatches a drag event into the page."""
        result = await self._client.send_raw(
            method="Input.dispatchDragEvent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def dispatch_key_event(
        self, params: DispatchKeyEventParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Dispatches a key event to the page."""
        result = await self._client.send_raw(
            method="Input.dispatchKeyEvent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def insert_text(
        self, params: InsertTextParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """This method emulates inserting text that doesn't come from a key press,
        for example an emoji keyboard or an IME."""
        result = await self._client.send_raw(
            method="Input.insertText",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def ime_set_composition(
        self, params: ImeSetCompositionParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """This method sets the current candidate text for IME.
        Use imeCommitComposition to commit the final text.
        Use imeSetComposition with empty string as text to cancel composition."""
        result = await self._client.send_raw(
            method="Input.imeSetComposition",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def dispatch_mouse_event(
        self, params: DispatchMouseEventParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Dispatches a mouse event to the page."""
        result = await self._client.send_raw(
            method="Input.dispatchMouseEvent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def dispatch_touch_event(
        self, params: DispatchTouchEventParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Dispatches a touch event to the page."""
        result = await self._client.send_raw(
            method="Input.dispatchTouchEvent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def cancel_dragging(self, session_id: str | None = None) -> dict[str, Any]:
        """Cancels any active dragging in the page."""
        result = await self._client.send_raw(
            method="Input.cancelDragging",
            params=None,
            session_id=session_id,
        )
        return result

    async def emulate_touch_from_mouse_event(
        self, params: EmulateTouchFromMouseEventParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Emulates touch event from the mouse event parameters."""
        result = await self._client.send_raw(
            method="Input.emulateTouchFromMouseEvent",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_ignore_input_events(
        self, params: SetIgnoreInputEventsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Ignores input events (useful while auditing page)."""
        result = await self._client.send_raw(
            method="Input.setIgnoreInputEvents",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def set_intercept_drags(
        self, params: SetInterceptDragsParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Prevents default drag and drop behavior and instead emits `Input.dragIntercepted` events.
        Drag and drop behavior can be directly controlled via `Input.dispatchDragEvent`."""
        result = await self._client.send_raw(
            method="Input.setInterceptDrags",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def synthesize_pinch_gesture(
        self, params: SynthesizePinchGestureParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Synthesizes a pinch gesture over a time period by issuing appropriate touch events."""
        result = await self._client.send_raw(
            method="Input.synthesizePinchGesture",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def synthesize_scroll_gesture(
        self, params: SynthesizeScrollGestureParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Synthesizes a scroll gesture over a time period by issuing appropriate touch events."""
        result = await self._client.send_raw(
            method="Input.synthesizeScrollGesture",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result

    async def synthesize_tap_gesture(
        self, params: SynthesizeTapGestureParams, session_id: str | None = None
    ) -> dict[str, Any]:
        """Synthesizes a tap gesture over a time period by issuing appropriate touch events."""
        result = await self._client.send_raw(
            method="Input.synthesizeTapGesture",
            params=params.to_cdp_params() if params else None,
            session_id=session_id,
        )
        return result
