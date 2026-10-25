import asyncio
import itertools
import json
import logging
from collections.abc import AsyncIterator
from typing import Any, Self

import websockets
from websockets.asyncio.client import ClientConnection, connect

from cdpify.event_queue import EventQueue
from cdpify.exceptions import CDPCommandError, CDPConnectionError, CDPTimeoutError
from cdpify.transport import TransportEvent

logger = logging.getLogger(__name__)


class WebSocketTransport:
    def __init__(
        self,
        url: str,
        *,
        additional_headers: dict[str, str] | None = None,
        max_frame_size: int = 100 * 1024 * 1024,
        default_timeout: float = 30.0,
        max_queue_size: int = 0,
    ) -> None:
        self.url = url
        self._additional_headers = additional_headers
        self._max_frame_size = max_frame_size
        self._default_timeout = default_timeout
        self._max_queue_size = max_queue_size

        self._ws: ClientConnection | None = None
        self._message_ids = itertools.count()
        self._pending_requests: dict[int, asyncio.Future[dict[str, Any]]] = {}
        self._message_loop_task: asyncio.Task[None] | None = None
        self._event_queue = EventQueue[TransportEvent](max_queue_size)
        self._event_stream_closed = False
        self._is_shutting_down = False

    @property
    def is_connected(self) -> bool:
        return self._ws is not None

    @property
    def dropped_events(self) -> int:
        """Oldest events discarded by events(); reset on each connection."""
        return self._event_queue.dropped_events

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()

    async def connect(self) -> None:
        if self.is_connected:
            raise CDPConnectionError("Already connected")

        logger.info("Connecting to %s", self.url)
        try:
            self._ws = await connect(
                self.url,
                max_size=self._max_frame_size,
                additional_headers=self._additional_headers,
            )
        except Exception as error:
            raise CDPConnectionError(f"Connection failed: {error}") from error

        self._is_shutting_down = False
        self._event_queue = EventQueue(self._max_queue_size)
        self._event_stream_closed = False
        self._message_loop_task = asyncio.create_task(self._run_message_loop())
        logger.info("Connected")

    async def disconnect(self) -> None:
        if self._is_shutting_down:
            return

        self._is_shutting_down = True
        logger.info("Disconnecting...")

        await self._stop_message_loop()
        self._cancel_pending_requests()
        await self._close_websocket()
        self._finish_event_stream()

        logger.info("Disconnected")

    async def execute(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        session_id: str | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        if not self.is_connected:
            raise CDPConnectionError("Not connected")

        request_timeout = self._default_timeout if timeout is None else timeout
        message_id = next(self._message_ids)

        message = _build_message(message_id, method, params, session_id)
        future = _create_pending_request(self._pending_requests, message_id)

        try:
            await self._send(message_id, method, message)
            return await self._await_response(
                message_id,
                method,
                future,
                request_timeout,
            )
        finally:
            self._pending_requests.pop(message_id, None)

    async def events(self) -> AsyncIterator[TransportEvent]:
        queue = self._event_queue
        while True:
            event = await queue.get()
            if event is None:
                return
            yield event

    async def _run_message_loop(self) -> None:
        connection = self._ws
        if connection is None:
            return

        try:
            async for raw_message in connection:
                if self._is_shutting_down:
                    break
                try:
                    self._process_message(raw_message)
                except Exception:
                    logger.exception(
                        "Dropping malformed CDP message: %.200r", raw_message
                    )
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection closed")
        except asyncio.CancelledError:
            logger.debug("Message loop cancelled")
            raise
        except Exception:
            logger.exception("Message loop error")
        finally:
            if not self._is_shutting_down:
                self._is_shutting_down = True
                self._cancel_pending_requests()
                await self._close_websocket()
                self._finish_event_stream()

    def _process_message(self, raw: str | bytes) -> None:
        message = json.loads(raw)

        if "id" in message:
            self._handle_response(message)
        elif "method" in message:
            self._handle_event(message)
        else:
            logger.warning("Unknown CDP message format: %s", message)

    def _handle_response(self, message: dict[str, Any]) -> None:
        message_id = message["id"]
        future = self._pending_requests.get(message_id)
        if not future or future.done():
            return

        future.set_result(message)

    def _handle_event(self, message: dict[str, Any]) -> None:
        event = TransportEvent(
            method=message["method"],
            params=message.get("params") or {},
            session_id=message.get("sessionId"),
        )
        self._event_queue.push(event)

    async def _stop_message_loop(self) -> None:
        task = self._message_loop_task
        if task and not task.done() and task is not asyncio.current_task():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        self._message_loop_task = None

    def _cancel_pending_requests(self) -> None:
        error = CDPConnectionError("Disconnected")
        for future in self._pending_requests.values():
            if not future.done():
                future.set_exception(error)
        self._pending_requests.clear()

    async def _close_websocket(self) -> None:
        if self._ws:
            try:
                await self._ws.close()
            except Exception as error:
                logger.debug("Websocket close error: %s", error)
            finally:
                self._ws = None

    def _finish_event_stream(self) -> None:
        if not self._event_stream_closed:
            self._event_stream_closed = True
            self._event_queue.finish()

    async def _send(
        self,
        message_id: int,
        method: str,
        message: dict[str, Any],
    ) -> None:
        connection = self._ws
        if connection is None:
            raise CDPConnectionError("Not connected")
        logger.debug("-> #%s: %s", message_id, method)
        await connection.send(json.dumps(message))

    async def _await_response(
        self,
        message_id: int,
        method: str,
        future: asyncio.Future[dict[str, Any]],
        timeout: float,
    ) -> dict[str, Any]:
        try:
            response = await asyncio.wait_for(future, timeout=timeout)
        except TimeoutError:
            raise CDPTimeoutError(f"{method} timed out after {timeout}s") from None

        if "error" in response:
            logger.debug("<- #%s: error", message_id)
            raise CDPCommandError.from_response(method, response["error"])
        logger.debug("<- #%s: OK", message_id)
        return response.get("result", {})


def _build_message(
    message_id: int,
    method: str,
    params: dict[str, Any] | None,
    session_id: str | None,
) -> dict[str, Any]:
    message = {
        "id": message_id,
        "method": method,
        "params": params or {},
    }
    if session_id:
        message["sessionId"] = session_id
    return message


def _create_pending_request(
    pending_requests: dict[int, asyncio.Future[dict[str, Any]]],
    message_id: int,
) -> asyncio.Future[dict[str, Any]]:
    future = asyncio.get_running_loop().create_future()
    pending_requests[message_id] = future
    return future
