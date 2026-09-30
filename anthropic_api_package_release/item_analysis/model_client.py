"""Request-scoped OpenAI calls for the CLI and website item analysis.

Credentials are passed explicitly, never cached or written to disk. JSON mode
handles serialization; the shared pipeline validates the full rubric schema and
allows one structural repair. The schema uses conditions that cannot be passed
unchanged to OpenAI's strict Structured Outputs format.
"""

from dataclasses import dataclass
import time

MODEL_ID = "gpt-6-luna"
PROVIDER = "openai"
REASONING_EFFORT = "low"

# Only these messages and parameter names may leave the provider adapter.
# SDK exception text can contain credentials, prompts, or account identifiers.
ERROR_MESSAGES = {
    "authentication": "OpenAI rejected authentication (401). Check that the API key is active and has permission to create Responses in its project.",
    "model_unavailable": "OpenAI could not find GPT-6 Luna or this key's project cannot access it. A valid API key does not guarantee access to this model.",
    "permission": "OpenAI denied this request (403). Check the key's project permissions, model access, and organization restrictions.",
    "quota": "OpenAI reports insufficient API credits or an API spending/usage limit. Check billing and limits for the key's project before retrying.",
    "rate_limit": "OpenAI temporarily rate-limited the request (429). Wait before retrying; completed items will be reused.",
    "invalid_request": "OpenAI rejected the demo's request settings. This needs a configuration check; re-entering the same key will not fix it.",
    "context_limit": "The request exceeds the model's input limit. The demo's prompt needs to be shortened before retrying.",
    "not_found": "OpenAI could not find the requested model or endpoint (404). The demo's model configuration or project access needs checking.",
    "timeout": "The OpenAI request timed out. Retry to resume from saved progress.",
    "connection": "The website server could not connect to OpenAI. Retry shortly; this does not establish that your key is invalid.",
    "server_error": "OpenAI is temporarily unable to process the request. Retry shortly to resume saved progress.",
    "output_limit": "GPT-6 Luna reached the output token limit before finishing its JSON. The demo's token limit or reasoning settings need adjustment.",
    "refusal": "OpenAI declined to return a classification for this request. No label was saved for the item.",
    "incomplete_response": "OpenAI returned an incomplete response. No label was saved; retry to resume saved progress.",
    "empty_response": "OpenAI returned no classification text. No label was saved; retry to resume saved progress.",
    "internal_error": "The demo could not process the model request. Share this message with the maintainer; this does not establish a problem with your API key.",
    "request_failed": "The OpenAI request failed for an unclassified reason. Share this message with the demo maintainer.",
}
SAFE_PARAMETERS = {"model", "reasoning", "reasoning.effort", "max_output_tokens",
                   "text", "text.format", "text.format.type", "service_tier", "store", "input", "instructions"}


@dataclass(frozen=True)
class CallResult:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    cached_input_tokens: int = 0
    reasoning_tokens: int = 0


class ModelRequestError(RuntimeError):
    """A safe error message without SDK request details or credentials."""

    def __init__(self, message=None, *, code="request_failed", status_code=None, parameter=None):
        # Accept the old message argument for callers, but never trust its text.
        self.code = code if isinstance(code, str) and code in ERROR_MESSAGES else "request_failed"
        self.status_code = status_code if isinstance(status_code, int) else None
        self.parameter = parameter if isinstance(parameter, str) and parameter in SAFE_PARAMETERS else None
        self.public_message = ERROR_MESSAGES[self.code]
        if self.parameter and self.code == "invalid_request":
            self.public_message += f" Rejected setting: {self.parameter}."
        super().__init__(self.public_message)


class ModelResponseError(ModelRequestError):
    """An unusable response whose billable usage still needs to be recorded."""

    def __init__(self, message: str, result: CallResult, *, code="incomplete_response"):
        super().__init__(message, code=code)
        self.result = result


def _request_error(error):
    """Classify errors using status/code fields, never a provider's free text."""
    from openai import APIConnectionError, APIStatusError, APITimeoutError

    if isinstance(error, APITimeoutError):
        return ModelRequestError(code="timeout")
    if isinstance(error, APIConnectionError):
        return ModelRequestError(code="connection")
    if not isinstance(error, APIStatusError):
        return ModelRequestError(code="internal_error")
    status = error.status_code
    body = error.body if isinstance(error.body, dict) else {}
    body = body.get("error", body)
    body = body if isinstance(body, dict) else {}
    code, kind, parameter = body.get("code"), body.get("type"), body.get("param")
    if code == "model_not_found":
        category = "model_unavailable"
    elif code in ("insufficient_quota", "credit_balance_exhausted", "organization_spend_limit_exceeded",
                  "project_spend_limit_exceeded", "organization_usage_limit_exceeded") or kind == "insufficient_quota":
        category = "quota"
    elif code == "context_length_exceeded":
        category = "context_limit"
    else:
        category = {401: "authentication", 403: "permission", 404: "not_found",
                    429: "rate_limit", 400: "invalid_request", 422: "invalid_request"}.get(
                        status, "server_error" if status >= 500 else "request_failed")
    return ModelRequestError(code=category, status_code=status, parameter=parameter)


def _options(*, model, reasoning_effort, system, user, max_tokens):
    return {
        "model": model,
        "instructions": system,
        # JSON mode checks input messages separately from `instructions`.
        # The serialized item/spec payload need not itself contain this word.
        "input": "Return a JSON object.\n\n" + user,
        "reasoning": {"effort": reasoning_effort},
        "max_output_tokens": max_tokens,
        "text": {"format": {"type": "json_object"}},
        "service_tier": "default",
        "store": False,
    }


def _result(response, *, api_key, started):
    usage = response.usage
    result = CallResult(
        text=(response.output_text or "").replace(api_key, "[redacted]"),
        model=response.model,
        input_tokens=usage.input_tokens if usage else 0,
        output_tokens=usage.output_tokens if usage else 0,
        latency_ms=int((time.monotonic() - started) * 1000),
        cached_input_tokens=getattr(getattr(usage, "input_tokens_details", None), "cached_tokens", 0) or 0,
        reasoning_tokens=getattr(getattr(usage, "output_tokens_details", None), "reasoning_tokens", 0) or 0,
    )
    if response.status != "completed":
        reason = getattr(getattr(response, "incomplete_details", None), "reason", None)
        code = "output_limit" if reason == "max_output_tokens" else "incomplete_response"
        raise ModelResponseError("", result, code=code)
    refused = any(
        part.type == "refusal"
        for item in response.output if item.type == "message"
        for part in item.content
    )
    if refused or not result.text.strip():
        raise ModelResponseError("", result, code="refusal" if refused else "empty_response")
    return result


def call_text(*, api_key, system, user, max_tokens,
              model=MODEL_ID, reasoning_effort=REASONING_EFFORT):
    """Make one synchronous call, with no hidden SDK retries or trace files."""
    from openai import OpenAI

    options = _options(model=model, reasoning_effort=reasoning_effort,
                       system=system, user=user, max_tokens=max_tokens)
    started = time.monotonic()
    try:
        with OpenAI(api_key=api_key, base_url="https://api.openai.com/v1",
                    timeout=180.0, max_retries=0) as client:
            response = client.responses.create(**options)
    except Exception as error:
        raise _request_error(error) from None
    return _result(response, api_key=api_key, started=started)


async def call_text_async(*, api_key, system, user, max_tokens,
                          model=MODEL_ID, reasoning_effort=REASONING_EFFORT):
    """Make one async call and release its client on completion or cancellation."""
    from openai import AsyncOpenAI

    options = _options(model=model, reasoning_effort=reasoning_effort,
                       system=system, user=user, max_tokens=max_tokens)
    started = time.monotonic()
    try:
        async with AsyncOpenAI(api_key=api_key, base_url="https://api.openai.com/v1",
                               timeout=180.0, max_retries=0) as client:
            response = await client.responses.create(**options)
    except Exception as error:
        raise _request_error(error) from None
    return _result(response, api_key=api_key, started=started)
