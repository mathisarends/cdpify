# pydantic_cpd/client.py
from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any

import websockets
from websockets.asyncio.client import ClientConnection, connect

logger = logging.getLogger(__name__)


class CDPError(Exception):
    """Base exception for CDP errors"""


class CDPConnectionError(CDPError):
    """WebSocket connection error"""


class CDPCommandError(CDPError):
    """CDP command execution error"""

    def __init__(self, error_data: dict[str, Any]) -> None:
        self.code: int = error_data.get("code", -1)
        self.message: str = error_data.get("message", "Unknown error")
        self.data: Any = error_data.get("data")
        super().__init__(f"CDP Error {self.code}: {self.message}")


class CDPTimeoutError(CDPError):
    """Request timeout error"""


EventHandler = Callable[[dict[str, Any], str | None], Awaitable[None]]


class EventRegistry:
    """Registry for CDP event handlers"""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}
        self._wildcard_handlers: list[EventHandler] = []

    def register(self, event_name: str | None, handler: EventHandler) -> None:
        """Register handler for specific event or all events (wildcard if None)"""
        if event_name is None:
            self._wildcard_handlers.append(handler)
        else:
            self._handlers.setdefault(event_name, []).append(handler)

    def unregister(self, event_name: str | None, handler: EventHandler) -> None:
        """Unregister a specific handler"""
        if event_name is None:
            if handler in self._wildcard_handlers:
                self._wildcard_handlers.remove(handler)
        else:
            handlers = self._handlers.get(event_name, [])
            if handler in handlers:
                handlers.remove(handler)

    async def handle_event(
        self, method: str, params: dict[str, Any], session_id: str | None
    ) -> bool:
        """Dispatch event to registered handlers. Returns True if any handler was called."""
        handled = False

        # Call specific handlers
        for handler in self._handlers.get(method, []):
            try:
                await handler(params, session_id)
                handled = True
            except Exception as e:
                logger.exception(f"Error in event handler for {method}: {e}")

        # Call wildcard handlers
        for handler in self._wildcard_handlers:
            try:
                await handler(params, session_id)
                handled = True
            except Exception as e:
                logger.exception(f"Error in wildcard event handler: {e}")

        return handled


class CDPClient:
    """Chrome DevTools Protocol WebSocket client"""

    def __init__(
        self,
        url: str,
        *,
        additional_headers: dict[str, str] | None = None,
        max_frame_size: int = 100 * 1024 * 1024,  # 100MB default
        default_timeout: float = 30.0,
    ) -> None:
        """
        Initialize CDP client.

        Args:
            url: WebSocket URL (e.g., ws://localhost:9222/devtools/page/...)
            additional_headers: Optional additional WebSocket headers
            max_frame_size: Maximum WebSocket frame size in bytes
            default_timeout: Default timeout for CDP commands in seconds
        """
        self.url: str = url
        self.additional_headers: dict[str, str] | None = additional_headers
        self.max_frame_size: int = max_frame_size
        self.default_timeout: float = default_timeout

        self._ws: ClientConnection | None = None
        self._msg_id: int = 0
        self._pending_requests: dict[int, asyncio.Future[dict[str, Any]]] = {}
        self._message_handler_task: asyncio.Task[None] | None = None
        self._event_registry: EventRegistry = EventRegistry()
        self._is_stopping: bool = False

    async def __aenter__(self) -> CDPClient:
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit"""
        await self.disconnect()

    @property
    def is_connected(self) -> bool:
        """Check if WebSocket is connected"""
        return self._ws is not None

    async def connect(self) -> None:
        """Establish WebSocket connection"""
        if self._ws is not None:
            raise CDPConnectionError("Client is already connected")

        logger.info(f"Connecting to {self.url}")

        try:
            self._ws = await connect(
                self.url,
                max_size=self.max_frame_size,
                additional_headers=self.additional_headers,
            )
            self._is_stopping = False
            self._message_handler_task = asyncio.create_task(self._handle_messages())
            logger.info("Connected successfully")

        except Exception as e:
            raise CDPConnectionError(f"Failed to connect: {e}") from e

    async def disconnect(self) -> None:
        """Close WebSocket connection and cleanup resources"""
        if self._is_stopping:
            return

        self._is_stopping = True
        logger.info("Disconnecting...")

        # Cancel message handler task
        if self._message_handler_task and not self._message_handler_task.done():
            self._message_handler_task.cancel()
            try:
                await self._message_handler_task
            except asyncio.CancelledError:
                logger.debug("Message handler cancelled")

        # Fail all pending requests
        error = CDPConnectionError("Client disconnected")
        for request_id, future in list(self._pending_requests.items()):
            if not future.done():
                future.set_exception(error)
        self._pending_requests.clear()

        # Close WebSocket
        if self._ws:
            try:
                await self._ws.close()
            except Exception as e:
                logger.debug(f"Error closing websocket: {e}")

        self._ws = None
        logger.info("Disconnected")

    def on_event(
        self, event_name: str | None = None
    ) -> Callable[[EventHandler], EventHandler]:
        """
        Decorator to register event handler.

        Args:
            event_name: Specific event name (e.g., "Page.loadEventFired") or None for all events

        Example:
            @client.on_event("Page.loadEventFired")
            async def on_load(params, session_id):
                print("Page loaded!")
        """

        def decorator(func: EventHandler) -> EventHandler:
            self._event_registry.register(event_name, func)
            return func

        return decorator

    def register_event_handler(
        self, event_name: str | None, handler: EventHandler
    ) -> None:
        """Register an event handler programmatically"""
        self._event_registry.register(event_name, handler)

    def unregister_event_handler(
        self, event_name: str | None, handler: EventHandler
    ) -> None:
        """Unregister an event handler"""
        self._event_registry.unregister(event_name, handler)

    async def send_raw(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        session_id: str | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """
        Send a CDP command and wait for response.

        Args:
            method: CDP method name (e.g., "Page.navigate")
            params: Command parameters
            session_id: Optional session ID for commands
            timeout: Command timeout (uses default_timeout if None)

        Returns:
            Response result dictionary

        Raises:
            CDPConnectionError: If not connected
            CDPCommandError: If command returns an error
            CDPTimeoutError: If command times out
        """
        if not self.is_connected:
            raise CDPConnectionError("Client is not connected")

        if timeout is None:
            timeout = self.default_timeout

        self._msg_id += 1
        msg_id = self._msg_id

        message = {
            "id": msg_id,
            "method": method,
            "params": params or {},
        }

        if session_id:
            message["sessionId"] = session_id

        # Create future for this request
        future: asyncio.Future[dict[str, Any]] = asyncio.Future()
        self._pending_requests[msg_id] = future

        try:
            logger.debug(f"Sending #{msg_id}: {method}")
            await self._ws.send(json.dumps(message))

            # Wait for response with timeout
            try:
                result = await asyncio.wait_for(future, timeout=timeout)
                logger.debug(f"Received #{msg_id}: OK")
                return result
            except asyncio.TimeoutError:
                raise CDPTimeoutError(
                    f"Command {method} timed out after {timeout}s"
                ) from None

        except (CDPTimeoutError, CDPCommandError):
            # Re-raise CDP-specific errors as-is
            raise
        except Exception as e:
            # Wrap other exceptions
            raise CDPConnectionError(f"Failed to send command: {e}") from e
        finally:
            # Always cleanup pending request
            self._pending_requests.pop(msg_id, None)

    async def _handle_messages(self) -> None:
        """Main message handling loop"""
        try:
            async for message in self._ws:
                if self._is_stopping:
                    break

                try:
                    data = json.loads(message)

                    # Handle response messages (with id)
                    if "id" in data:
                        await self._handle_response(data)

                    # Handle event messages (with method)
                    elif "method" in data:
                        await self._handle_event(data)

                    # Unexpected message format
                    else:
                        logger.warning(f"Unexpected message format: {data}")

                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode message: {e}")

        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")
        except asyncio.CancelledError:
            logger.debug("Message handler cancelled")
            raise
        except Exception as e:
            logger.exception(f"Error in message handler: {e}")
        finally:
            # Cleanup on exit
            if not self._is_stopping:
                await self.disconnect()

    async def _handle_response(self, data: dict[str, Any]) -> None:
        """Handle CDP response message"""
        msg_id = data["id"]
        future = self._pending_requests.get(msg_id)

        if not future:
            logger.warning(f"Received response for unknown request #{msg_id}")
            return

        if future.done():
            logger.warning(f"Received duplicate response for request #{msg_id}")
            return

        if "error" in data:
            error = CDPCommandError(data["error"])
            logger.error(f"Command #{msg_id} failed: {error}")
            future.set_exception(error)
        else:
            future.set_result(data.get("result", {}))

    async def _handle_event(self, data: dict[str, Any]) -> None:
        """Handle CDP event message"""
        method = data["method"]
        params = data.get("params", {})
        session_id = data.get("sessionId")

        logger.debug(f"Event: {method}")

        handled = await self._event_registry.handle_event(method, params, session_id)

        if not handled:
            logger.debug(f"No handler registered for event: {method}")
