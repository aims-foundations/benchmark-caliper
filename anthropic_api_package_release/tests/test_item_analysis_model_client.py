"""Exercise the real OpenAI adapter with SDK responses, without paid calls."""

import asyncio
from types import SimpleNamespace

import openai
import pytest

from item_analysis import model_client


def response(*, status="completed", text='{"labels": []}', refusal=False):
    return SimpleNamespace(
        status=status, output_text=text, model="gpt-6-luna",
        output=[SimpleNamespace(type="message", content=[
            SimpleNamespace(type="refusal" if refusal else "output_text")])],
        usage=SimpleNamespace(
            input_tokens=120, output_tokens=40,
            input_tokens_details=SimpleNamespace(cached_tokens=100),
            output_tokens_details=SimpleNamespace(reasoning_tokens=30),
        ),
    )


class FakeClient:
    def __init__(self, result, failure=None):
        self.result, self.failure = result, failure
        self.options = None
        self.closed = False
        self.responses = SimpleNamespace(create=self.create)

    def create(self, **kwargs):
        self.options = kwargs
        if self.failure is not None:
            raise self.failure
        return self.result

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.closed = True

    async def __aenter__(self):
        async def create(**kwargs):
            return self.create(**kwargs)
        self.responses = SimpleNamespace(create=create)
        return self

    async def __aexit__(self, *args):
        self.closed = True


def install(monkeypatch, client, asynchronous):
    constructed = []

    def factory(**kwargs):
        constructed.append(kwargs)
        return client

    monkeypatch.setattr(openai, "AsyncOpenAI" if asynchronous else "OpenAI", factory)
    return constructed


def call(asynchronous, api_key="private-test-key"):
    kwargs = dict(api_key=api_key, system="Return rubric JSON.", user="An item.", max_tokens=4096)
    return (asyncio.run(model_client.call_text_async(**kwargs)) if asynchronous
            else model_client.call_text(**kwargs))


@pytest.mark.parametrize("asynchronous", [False, True])
def test_luna_request_usage_and_client_cleanup(monkeypatch, asynchronous):
    client = FakeClient(response())
    constructed = install(monkeypatch, client, asynchronous)
    result = call(asynchronous)
    assert client.closed
    assert constructed == [{"api_key": "private-test-key", "base_url": "https://api.openai.com/v1",
                            "timeout": 180.0, "max_retries": 0}]
    assert client.options == {
        "model": "gpt-6-luna", "instructions": "Return rubric JSON.", "input": "An item.",
        "reasoning": {"effort": "low"}, "max_output_tokens": 4096,
        "text": {"format": {"type": "json_object"}}, "service_tier": "default", "store": False,
    }
    assert result.input_tokens == 120
    assert result.output_tokens == 40  # reasoning is already included
    assert result.cached_input_tokens == 100
    assert result.reasoning_tokens == 30
    assert result.model == "gpt-6-luna"


@pytest.mark.parametrize("asynchronous", [False, True])
def test_provider_failure_closes_client_and_discards_sensitive_error(monkeypatch, asynchronous):
    client = FakeClient(None, RuntimeError("upstream echoed private-test-key"))
    install(monkeypatch, client, asynchronous)
    with pytest.raises(model_client.ModelRequestError) as error:
        call(asynchronous)
    assert client.closed
    assert "private-test-key" not in str(error.value)


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("output", [response(status="incomplete"), response(refusal=True), response(text="")])
def test_unusable_responses_retain_billable_usage(monkeypatch, asynchronous, output):
    client = FakeClient(output)
    install(monkeypatch, client, asynchronous)
    with pytest.raises(model_client.ModelResponseError) as error:
        call(asynchronous)
    assert client.closed
    assert error.value.result.input_tokens == 120
    assert error.value.result.output_tokens == 40


@pytest.mark.parametrize("asynchronous", [False, True])
def test_model_output_cannot_echo_the_credential(monkeypatch, asynchronous):
    client = FakeClient(response(text='{"evidence":"private-test-key"}'))
    install(monkeypatch, client, asynchronous)
    assert call(asynchronous).text == '{"evidence":"[redacted]"}'


def test_cancellation_closes_async_client(monkeypatch):
    client = FakeClient(None, asyncio.CancelledError())
    install(monkeypatch, client, True)
    with pytest.raises(asyncio.CancelledError):
        call(True)
    assert client.closed
