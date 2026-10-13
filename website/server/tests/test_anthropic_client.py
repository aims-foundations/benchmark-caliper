"""A per-call provider client must release connections on every exit path."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from website.server import anthropic_client


@pytest.mark.parametrize("failure", [None, RuntimeError("provider unavailable"), asyncio.CancelledError()])
def test_stream_client_is_closed_on_success_failure_and_cancellation(monkeypatch, failure):
    async def final_message():
        if failure is not None:
            raise failure
        return SimpleNamespace(content=[SimpleNamespace(type="text", text="response")],
                               usage=SimpleNamespace(input_tokens=3, output_tokens=1))

    class Stream:
        async def __aenter__(self):
            return SimpleNamespace(get_final_message=final_message)

        async def __aexit__(self, *args):
            return False

    client = SimpleNamespace(messages=SimpleNamespace(stream=lambda **kwargs: Stream()), close=AsyncMock())
    monkeypatch.setattr(anthropic_client.anthropic, "AsyncAnthropic", lambda **kwargs: client)
    monkeypatch.setattr(anthropic_client.mock_anthropic, "is_mock_enabled", lambda: False)
    request = anthropic_client.call_text_async("test-key", "haiku", "system", "user")
    if failure is None:
        assert asyncio.run(request).text == "response"
    else:
        with pytest.raises(type(failure)):
            asyncio.run(request)
    client.close.assert_awaited_once()
