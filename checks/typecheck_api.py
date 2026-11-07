"""Static regression checks for the installed, public developer API."""

from typing import assert_type

from cdpify import CdpClient, EventSubscription, ReceivedEvent, TransportEvent
from cdpify.domains.network import RequestWillBeSentEvent
from cdpify.domains.runtime import CallArgument, EvaluateResult


async def usage(client: CdpClient) -> None:
    result = await client.runtime.evaluate(expression="1 + 1", return_by_value=True)
    assert_type(result, EvaluateResult)
    assert_type(
        client.listen(RequestWillBeSentEvent), EventSubscription[RequestWillBeSentEvent]
    )
    async with client.listen_all(RequestWillBeSentEvent) as events:
        received = await events.next(timeout=1)
        assert_type(received, ReceivedEvent[RequestWillBeSentEvent])
        assert_type(received.value.request.url, str)
    assert_type(
        await client.session("S1").runtime.evaluate(expression="1"), EvaluateResult
    )
    assert_type(client.listen_raw(), EventSubscription[TransportEvent])
    assert_type(client.listen_all_raw(), EventSubscription[TransportEvent])
    await client.runtime.call_function_on(
        function_declaration="function(x) {}", arguments=[CallArgument(value=None)]
    )
