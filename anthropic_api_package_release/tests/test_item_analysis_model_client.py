"""Exercise the real OpenAI adapter with SDK responses, without paid calls."""

import asyncio
import json
from types import SimpleNamespace

import httpx
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


def install_transport(monkeypatch, asynchronous, status, body):
    """Exercise SDK serialization, HTTP exception parsing, and client cleanup."""
    name = "AsyncOpenAI" if asynchronous else "OpenAI"
    sdk_client = getattr(openai, name)
    requests, transports = [], []

    def respond(request):
        requests.append(request)
        return httpx.Response(status, json=body)

    def factory(**kwargs):
        transport = httpx.MockTransport(respond)
        client = (httpx.AsyncClient(transport=transport) if asynchronous
                  else httpx.Client(transport=transport))
        transports.append(client)
        return sdk_client(**kwargs, http_client=client)

    monkeypatch.setattr(openai, name, factory)
    return requests, transports


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("status,code,parameter,expected", [
    (401, "invalid_api_key", None, "authentication"),
    (404, "model_not_found", "model", "model_unavailable"),
    (429, "insufficient_quota", None, "quota"),
    (429, "rate_limit_exceeded", None, "rate_limit"),
    (400, "unsupported_parameter", "reasoning.effort", "invalid_request"),
    (400, "invalid_value", "service_tier", "invalid_request"),
])
def test_real_sdk_errors_keep_actionable_reason_without_provider_text(
        monkeypatch, asynchronous, status, code, parameter, expected):
    requests, transports = install_transport(monkeypatch, asynchronous, status, {
        "error": {"message": "Sensitive upstream text private-test-key",
                  "type": "invalid_request_error", "code": code, "param": parameter},
    })
    with pytest.raises(model_client.ModelRequestError) as raised:
        call(asynchronous)
    error = raised.value
    assert error.code == expected
    assert error.status_code == status
    assert error.parameter == parameter
    assert "private-test-key" not in str(error)
    assert "Sensitive upstream text" not in str(error)
    if expected == "invalid_request":
        assert f"Rejected setting: {parameter}." in str(error)
    assert len(requests) == 1  # No hidden SDK retry charges.
    assert str(requests[0].url) == "https://api.openai.com/v1/responses"
    payload = json.loads(requests[0].content)
    assert payload["model"] == "gpt-6-luna"
    assert payload["reasoning"] == {"effort": "low"}
    assert payload["text"] == {"format": {"type": "json_object"}}
    assert all(client.is_closed for client in transports)


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("parameter", [
    "private-test-key", {"private-test-key": "secret"}, ["private-test-key"],
])
def test_real_sdk_untrusted_error_parameter_is_omitted(monkeypatch, asynchronous, parameter):
    install_transport(monkeypatch, asynchronous, 400, {
        "error": {"message": "private-test-key", "type": "invalid_request_error",
                  "code": "unsupported_parameter", "param": parameter},
    })
    with pytest.raises(model_client.ModelRequestError) as raised:
        call(asynchronous)
    assert raised.value.code == "invalid_request"
    assert raised.value.parameter is None
    assert str(raised.value) == model_client.ERROR_MESSAGES["invalid_request"]
    assert "private-test-key" not in str(raised.value)


@pytest.mark.parametrize("asynchronous", [False, True])
def test_real_sdk_output_limit_retains_usage_and_specific_error(monkeypatch, asynchronous):
    requests, transports = install_transport(monkeypatch, asynchronous, 200, {
        "id": "resp_test", "object": "response", "created_at": 1,
        "status": "incomplete", "model": "gpt-6-luna", "output": [],
        "incomplete_details": {"reason": "max_output_tokens"},
        "usage": {"input_tokens": 120, "output_tokens": 4096, "total_tokens": 4216,
                  "input_tokens_details": {"cached_tokens": 100},
                  "output_tokens_details": {"reasoning_tokens": 4096}},
    })
    with pytest.raises(model_client.ModelResponseError) as raised:
        call(asynchronous)
    assert raised.value.code == "output_limit"
    assert raised.value.result.input_tokens == 120
    assert raised.value.result.output_tokens == 4096
    assert raised.value.result.reasoning_tokens == 4096
    assert "output token limit" in str(raised.value)
    assert len(requests) == 1
    assert all(client.is_closed for client in transports)
