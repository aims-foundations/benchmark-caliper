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


class ModelResponseError(ModelRequestError):
    """An unusable response whose billable usage still needs to be recorded."""

    def __init__(self, message: str, result: CallResult):
        super().__init__(message)
        self.result = result


def _options(*, model, reasoning_effort, system, user, max_tokens):
    return {
        "model": model,
        "instructions": system,
        "input": user,
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
        raise ModelResponseError("OpenAI did not complete the response. Retry or increase the output token limit.", result)
    refused = any(
        part.type == "refusal"
        for item in response.output if item.type == "message"
        for part in item.content
    )
    if refused or not result.text.strip():
        raise ModelResponseError("OpenAI did not return classification JSON for this request.", result)
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
    except Exception:
        raise ModelRequestError("OpenAI request failed. Check key access, quota, and model availability.") from None
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
    except Exception:
        raise ModelRequestError("OpenAI request failed. Check key access, quota, and model availability.") from None
    return _result(response, api_key=api_key, started=started)
