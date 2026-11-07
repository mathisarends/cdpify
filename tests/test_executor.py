import asyncio

import pytest

from cdpify import CdpClient, CDPTimeoutError
from cdpify.executor import BoundCommandExecutor


class SlowTransport:
    def __init__(self) -> None:
        self.cancelled = False
        self.timeout = None

    async def execute(self, method, params=None, session_id=None, timeout=None):
        self.timeout = timeout
        try:
            await asyncio.Event().wait()
        finally:
            self.cancelled = True


@pytest.mark.asyncio
@pytest.mark.parametrize("scope", ["root", "session", "raw", "raw_session"])
async def test_client_deadline_enforces_custom_transports(scope) -> None:
    transport = SlowTransport()
    client = CdpClient(transport=transport, default_timeout=0.01)
    with pytest.raises(CDPTimeoutError):
        if scope == "root":
            await client.runtime.enable()
        elif scope == "session":
            await client.session("S1").runtime.enable()
        else:
            await client.execute(
                "Runtime.enable", session_id="S1" if scope == "raw_session" else None
            )
    assert transport.cancelled
    assert transport.timeout == 0.01


@pytest.mark.asyncio
async def test_outer_timeout_preserves_builtin_exception_and_cleans_request() -> None:
    transport = SlowTransport()
    executor = BoundCommandExecutor(transport, default_timeout=30)
    with pytest.raises(TimeoutError) as error:
        async with asyncio.timeout(0.01):
            await executor.execute("Runtime.enable")
    assert not isinstance(error.value, CDPTimeoutError)
    assert transport.cancelled


@pytest.mark.asyncio
async def test_none_explicitly_disables_default_and_cancellation_is_preserved() -> None:
    transport = SlowTransport()
    executor = BoundCommandExecutor(transport, default_timeout=0.001)
    task = asyncio.create_task(executor.execute("Runtime.enable", timeout=None))
    await asyncio.sleep(0.01)
    assert not task.done()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert transport.cancelled
    assert transport.timeout is None


@pytest.mark.asyncio
async def test_transport_timeout_error_is_not_relabelled_as_own_deadline() -> None:
    class FailingTransport:
        async def execute(self, **kwargs):
            raise TimeoutError("transport-specific failure")

    executor = BoundCommandExecutor(FailingTransport())
    with pytest.raises(TimeoutError, match="transport-specific failure") as error:
        await executor.execute("Runtime.enable")
    assert not isinstance(error.value, CDPTimeoutError)
