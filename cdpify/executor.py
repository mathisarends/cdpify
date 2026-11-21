import asyncio
from collections.abc import Awaitable, Callable
from typing import Any, Protocol

from cdpify.error import CDPTimeoutError
from cdpify.transport import Transport
from cdpify.unset import UNSET, UnsetType


class CommandExecutor(Protocol):
    """Execute CDP commands within an already selected routing context."""

    async def execute(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Send a command with a deadline in seconds and return its wire result."""
        ...


class BoundCommandExecutor:
    """Bind command execution to the root connection or one CDP session."""

    def __init__(
        self,
        transport: Transport,
        session_id: str | None = None,
        *,
        default_timeout: float | None = 30.0,
        check_session: Callable[[str], None] | None = None,
    ) -> None:
        self._transport = transport
        self._session_id = session_id
        self._check_session = check_session
        self._default_timeout = default_timeout

    @property
    def session_id(self) -> str | None:
        return self._session_id

    async def execute(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        timeout: float | None | UnsetType = UNSET,
    ) -> dict[str, Any]:
        if self._check_session is not None and self._session_id is not None:
            self._check_session(self._session_id)
        request_timeout = self._default_timeout if timeout is UNSET else timeout
        return await with_command_timeout(
            method,
            request_timeout,
            self._transport.execute(
                method=method,
                params=params,
                session_id=self._session_id,
                # The client owns this deadline. Disable a second transport
                # timer; standalone transport callers can still set a budget.
                timeout=None,
            ),
        )


async def with_command_timeout[T](
    method: str, timeout: float | None, operation: Awaitable[T]
) -> T:
    """Translate expiry of this command's deadline to CDPTimeoutError."""
    if timeout is None:
        return await operation
    deadline = asyncio.timeout(timeout)
    try:
        async with deadline:
            return await operation
    except TimeoutError:
        # Preserve errors from the transport and timeouts owned by an outer
        # caller. Only translate expiration of this particular deadline.
        if not deadline.expired():
            raise
        raise CDPTimeoutError(f"{method} timed out after {timeout}s") from None
