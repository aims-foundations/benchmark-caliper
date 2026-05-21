"""Per-request Anthropic client for the website backend.

This is intentionally separate from `anthropic_api_package_release/client.py`, which
reads keys from the environment, holds a module-level singleton, and writes
trace files to disk. None of those behaviours are safe for a multi-user
backend running BYOK — so this module:

  - takes the API key as an argument (from the per-request HTTP header),
  - constructs a fresh `anthropic.AsyncAnthropic` per call,
  - exposes a single async helper that returns text + token usage,
  - never persists anything itself (the redaction gate is the only writer).

The model family names ("haiku", "sonnet", "opus") match the routing the
existing pipeline uses, so prompts and step labels stay portable.
"""

from __future__ import annotations

import base64
import time
from dataclasses import dataclass
from typing import Optional

import anthropic

from . import mock_anthropic

# Mirrors anthropic_api_package_release/client.py:MODELS so the website and the
# pipeline call the same models. Update both together.
MODELS: dict[str, str] = {
    "haiku":  "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus":   "claude-opus-4-7",
}


@dataclass(frozen=True)
class CallResult:
    """The minimum we need from a Claude call to log a step."""
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: int


WEB_SEARCH_TOOL = {
    "type": "web_search_20250305",
    "name": "web_search",
}


async def call_text_async(
    api_key: str,
    family: str,
    system: str,
    user: str,
    pdf_bytes: Optional[bytes] = None,
    tools: Optional[list[dict]] = None,
    max_tokens: int = 1024,
) -> CallResult:
    """One Anthropic message, returning text + usage.

    The `api_key` is used to construct a per-call client and goes out of
    scope when this coroutine returns. No globals, no caches.

    If `pdf_bytes` is provided, it is attached as a document block before
    the user text. Anthropic's PDF support accepts up to 32 MB and ~100
    pages per document.

    If `tools` is provided (e.g. `[WEB_SEARCH_TOOL]`), the model can use
    the named server tools. Server-tool invocations and results are
    interleaved with text in the response; we extract only the final text
    content. Web search is billed by Anthropic at $10/1000 searches in
    addition to normal token costs — that surcharge is not modelled in
    `prices.py`.
    """
    if family not in MODELS:
        raise ValueError(f"unknown model family: {family!r}")

    # DEV-ONLY: short-circuit to fixtures when MOCK_ANTHROPIC=1. The app's
    # lifespan guard ensures this is never active in production.
    if mock_anthropic.is_mock_enabled():
        return CallResult(
            text=mock_anthropic.replay(family=family, system=system),
            model=MODELS[family],
            input_tokens=0,
            output_tokens=0,
            latency_ms=50,
        )

    client = anthropic.AsyncAnthropic(api_key=api_key)
    model_id = MODELS[family]

    user_content: list[dict] = []
    if pdf_bytes is not None:
        user_content.append(
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": base64.standard_b64encode(pdf_bytes).decode("ascii"),
                },
            }
        )
    user_content.append({"type": "text", "text": user})

    kwargs: dict = {
        "model": model_id,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user_content}],
    }
    if tools:
        kwargs["tools"] = tools

    # Stream every call: the SDK refuses non-streaming requests whose
    # worst-case completion time exceeds 10 minutes (Opus + large prompts
    # + high max_tokens trips this). Streaming is also what the CLI
    # pipeline uses, so behaviour stays aligned.
    started = time.monotonic()
    async with client.messages.stream(**kwargs) as stream_resp:
        final = await stream_resp.get_final_message()
    latency_ms = int((time.monotonic() - started) * 1000)

    return CallResult(
        text=_extract_text(final),
        model=model_id,
        input_tokens=final.usage.input_tokens,
        output_tokens=final.usage.output_tokens,
        latency_ms=latency_ms,
    )


def _extract_text(resp: anthropic.types.Message) -> str:
    """Concatenate text blocks from a Claude response."""
    parts: list[str] = []
    for block in resp.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    return "".join(parts)
