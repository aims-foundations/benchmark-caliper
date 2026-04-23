"""Anthropic API wrapper for the validity pipeline.

One unified `call()` for serial steps and a `call_parallel()` fan-out for the
per-page Haiku extraction. All step-specific prompts live in `prompts/*.md` and
are loaded by `prompts.py` — no prompt text belongs here.

Reads ANTHROPIC_API_KEY from the environment (or a .env file if python-dotenv
is available).

Every API call also updates a per-step, per-model ledger of token usage so the
pipeline can print a cost breakdown at the end of each run. Override `PRICES`
at runtime (e.g. `client.PRICES["sonnet"]["output"] = 18.0`) if Anthropic's
pricing changes before you update this file.
"""

from __future__ import annotations

import base64
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import anthropic

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MODELS = {
    "haiku":  "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus":   "claude-opus-4-7",
}

# Pricing in USD per 1M tokens. Source: https://www.anthropic.com/pricing
# These are point-in-time values — reconcile against the pricing page for the
# authoritative number before quoting costs externally.
PRICES: dict[str, dict[str, float]] = {
    "haiku":  {"input": 1.00,  "output": 5.00},
    "sonnet": {"input": 3.00,  "output": 15.00},
    "opus":   {"input": 15.00, "output": 75.00},
}
# Web search is billed separately as a server tool: $10 per 1000 requests.
WEB_SEARCH_PRICE_PER_1K = 10.00

_client: anthropic.Anthropic | None = None

# Dry-run mode: when enabled, `call()` / `call_parallel()` print each prompt
# to stdout and return a placeholder instead of hitting the API. Lets you
# inspect the exact system + user content a step would send before paying for
# the real call. Toggle via `client.set_dry_run(True)`.
DRY_RUN: bool = False
DRY_RUN_PLACEHOLDER = "<dry-run: skipped API call>"


def set_dry_run(enabled: bool) -> None:
    global DRY_RUN
    DRY_RUN = enabled


# Streaming override. `None` (default) streams all models. Set to False via
# run_pipeline's --no-streaming flag to disable.
STREAM_DEFAULT: bool | None = None


def set_stream_default(mode: bool | None) -> None:
    global STREAM_DEFAULT
    STREAM_DEFAULT = mode


# Per-call trace log: one JSONL file per step label in `_TRACE_DIR`. Each file
# holds every call that step fired (typically 1, except 1a_extract which has
# one entry per page). Disabled unless set via `set_trace_dir`. Thread-safe:
# parallel Haiku fan-out serializes appends through `_TRACE_LOCK`.
_TRACE_DIR: Path | None = None
_TRACE_LOCK = threading.Lock()


def set_trace_dir(path: Path | str | None) -> None:
    global _TRACE_DIR
    _TRACE_DIR = Path(path) if path is not None else None


def clear_trace_steps(*step_names: str) -> None:
    """Delete the per-step trace file(s); overwrite-on-rerun semantics."""
    if _TRACE_DIR is None:
        return
    with _TRACE_LOCK:
        for step in step_names:
            (_TRACE_DIR / f"{step}.jsonl").unlink(missing_ok=True)


def _cost_for_usage(model: str, usage) -> float:
    """Point-estimate USD cost for one call, mirroring `_model_cost_breakdown`."""
    price = PRICES.get(model)
    if not price:
        return 0.0
    in_tok = getattr(usage, "input_tokens", 0) or 0
    out_tok = getattr(usage, "output_tokens", 0) or 0
    stu = getattr(usage, "server_tool_use", None)
    web_req = getattr(stu, "web_search_requests", 0) or 0 if stu else 0
    return (
        in_tok * price["input"] / 1_000_000
        + out_tok * price["output"] / 1_000_000
        + web_req * WEB_SEARCH_PRICE_PER_1K / 1000
    )


def _extract_tool_trace(content_blocks) -> list[dict]:
    """Pull server_tool_use + web_search_tool_result blocks out of the
    response's content list, preserving in-order interleaving. The opaque
    `encrypted_content` field on individual result items is dropped (large
    and not useful for post-hoc analysis); title / url / page_age are kept
    so the trace is enough to reconstruct what the model searched and what
    it got back."""
    trace: list[dict] = []
    for b in content_blocks:
        btype = getattr(b, "type", None)
        if btype == "server_tool_use":
            trace.append({
                "type": "server_tool_use",
                "id": getattr(b, "id", None),
                "name": getattr(b, "name", None),
                "input": getattr(b, "input", None),
            })
        elif btype == "web_search_tool_result":
            entry: dict = {
                "type": "web_search_tool_result",
                "tool_use_id": getattr(b, "tool_use_id", None),
            }
            content = getattr(b, "content", None)
            if isinstance(content, list):
                entry["results"] = [
                    {
                        "title": getattr(r, "title", None),
                        "url": getattr(r, "url", None),
                        "page_age": getattr(r, "page_age", None),
                    }
                    for r in content
                ]
            else:
                entry["error"] = {
                    "error_code": getattr(content, "error_code", None),
                }
            trace.append(entry)
    return trace


def _write_trace(
    *,
    step: str,
    model: str,
    system: str,
    user: str,
    output: str,
    usage,
    duration_s: float,
    pdf_path: str | None,
    tools: list | None,
    max_tokens: int,
    temperature: float | None = None,
    top_p: float | None = None,
    top_k: int | None = None,
    tool_trace: list[dict] | None = None,
) -> None:
    if _TRACE_DIR is None:
        return
    step_label = step or "_unattributed"
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "step": step_label,
        "model": model,
        "model_id": MODELS.get(model, model),
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "sampling_note": "explicit" if temperature is not None else "API defaults (not explicitly set)",
        "pdf_path": pdf_path,
        "tools": tools,
        "duration_seconds": round(duration_s, 3),
        "system": system,
        "user": user,
        "output": output,
        "tool_trace": tool_trace or [],
        "usage": {
            "input_tokens": getattr(usage, "input_tokens", 0) or 0,
            "output_tokens": getattr(usage, "output_tokens", 0) or 0,
            "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0) or 0,
            "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0) or 0,
            "web_search_requests": (
                getattr(getattr(usage, "server_tool_use", None), "web_search_requests", 0) or 0
            ),
        },
        "cost_usd": round(_cost_for_usage(model, usage), 6),
    }
    line = json.dumps(entry, ensure_ascii=False)
    path = _TRACE_DIR / f"{step_label}.jsonl"
    with _TRACE_LOCK:
        _TRACE_DIR.mkdir(parents=True, exist_ok=True)
        with path.open("a") as f:
            f.write(line + "\n")

# === Per-run cost ledger ===
# Structure: {step_label: {model_key: {calls, input_tokens, output_tokens,
#                                      cache_read_input_tokens,
#                                      cache_creation_input_tokens,
#                                      web_search_requests}}}
_LEDGER: dict[str, dict[str, dict[str, int]]] = {}
_LEDGER_LOCK = threading.Lock()


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        # Use the SDK default (max_retries=2). Higher values multiply cost
        # on persistent failures (e.g. middlebox-closed TLS streams) without
        # fixing the root cause — each retry re-bills the full input.
        _client = anthropic.Anthropic()
    return _client


def _pdf_block(pdf_path: str) -> dict:
    with open(pdf_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("ascii")
    return {
        "type": "document",
        "source": {"type": "base64", "media_type": "application/pdf", "data": data},
    }


def _new_counters() -> dict:
    return {
        "model_id": "",
        "calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0,
        "web_search_requests": 0,
    }


def _print_dry_run(
    step: str,
    model: str,
    system: str,
    user: str,
    pdf_path: str | None,
    tools: list | None,
    max_tokens: int,
) -> None:
    """Emit the exact prompt that `call()` would send, then return (no API hit)."""
    label = step or "(unattributed)"
    bar = "=" * 78
    print(bar)
    print(f"[dry-run] step={label}  model={model} ({MODELS[model]})  max_tokens={max_tokens}")
    if pdf_path:
        print(f"[dry-run] pdf_path={pdf_path}")
    if tools:
        print(f"[dry-run] tools={tools}")
    print("-" * 78)
    print("--- SYSTEM ---")
    print(system)
    print("--- USER ---")
    print(user)
    print(bar)


def _record_usage(step: str, model: str, usage) -> None:
    """Fold an Anthropic Usage object into the per-step/per-model ledger."""
    if not step:
        step = "(unattributed)"
    with _LEDGER_LOCK:
        counters = _LEDGER.setdefault(step, {}).setdefault(model, _new_counters())
        counters["model_id"] = MODELS.get(model, model)
        counters["calls"] += 1
        counters["input_tokens"] += getattr(usage, "input_tokens", 0) or 0
        counters["output_tokens"] += getattr(usage, "output_tokens", 0) or 0
        counters["cache_read_input_tokens"] += (
            getattr(usage, "cache_read_input_tokens", 0) or 0
        )
        counters["cache_creation_input_tokens"] += (
            getattr(usage, "cache_creation_input_tokens", 0) or 0
        )
        # server_tool_use may be present on responses that invoked web_search.
        stu = getattr(usage, "server_tool_use", None)
        if stu is not None:
            counters["web_search_requests"] += (
                getattr(stu, "web_search_requests", 0) or 0
            )


def reset_ledger() -> None:
    with _LEDGER_LOCK:
        _LEDGER.clear()


def ledger_snapshot() -> dict:
    """Deep-copy of the ledger for external inspection / JSON dump."""
    with _LEDGER_LOCK:
        return {
            step: {m: dict(c) for m, c in models.items()}
            for step, models in _LEDGER.items()
        }


def _model_cost_breakdown(model: str, counters: dict) -> dict[str, float]:
    """Return input / output / web-search / total USD for a step+model row.

    Cache-read and cache-creation tokens are tracked in the ledger but not
    priced here — the pipeline doesn't use prompt caching yet, and Anthropic
    bills them at different rates. When caching is turned on, extend PRICES
    with cache_read / cache_creation fields and update this function.
    """
    price = PRICES.get(model)
    if not price:
        return {"input_usd": 0.0, "output_usd": 0.0, "web_search_usd": 0.0, "total_usd": 0.0}
    in_usd = counters["input_tokens"] / 1_000_000 * price["input"]
    out_usd = counters["output_tokens"] / 1_000_000 * price["output"]
    ws_usd = counters["web_search_requests"] / 1000 * WEB_SEARCH_PRICE_PER_1K
    return {
        "input_usd": in_usd,
        "output_usd": out_usd,
        "web_search_usd": ws_usd,
        "total_usd": in_usd + out_usd + ws_usd,
    }


def cost_report() -> dict:
    """Structured per-step cost rollup. Handy for JSON dumps."""
    snap = ledger_snapshot()
    rollup: dict = {
        "steps": {},
        "input_usd": 0.0,
        "output_usd": 0.0,
        "web_search_usd": 0.0,
        "total_usd": 0.0,
    }
    for step in sorted(snap):
        step_in = step_out = step_ws = 0.0
        per_model = {}
        for model, counters in snap[step].items():
            bd = _model_cost_breakdown(model, counters)
            step_in += bd["input_usd"]
            step_out += bd["output_usd"]
            step_ws += bd["web_search_usd"]
            per_model[model] = {
                **counters,
                "input_usd": round(bd["input_usd"], 6),
                "output_usd": round(bd["output_usd"], 6),
                "web_search_usd": round(bd["web_search_usd"], 6),
                "cost_usd": round(bd["total_usd"], 6),
            }
        step_total = step_in + step_out + step_ws
        rollup["steps"][step] = {
            "models": per_model,
            "input_usd": round(step_in, 6),
            "output_usd": round(step_out, 6),
            "web_search_usd": round(step_ws, 6),
            "cost_usd": round(step_total, 6),
        }
        rollup["input_usd"] += step_in
        rollup["output_usd"] += step_out
        rollup["web_search_usd"] += step_ws
        rollup["total_usd"] += step_total
    rollup["input_usd"] = round(rollup["input_usd"], 6)
    rollup["output_usd"] = round(rollup["output_usd"], 6)
    rollup["web_search_usd"] = round(rollup["web_search_usd"], 6)
    rollup["total_usd"] = round(rollup["total_usd"], 6)
    return rollup


def format_cost_report() -> str:
    """Human-readable per-step cost table with In$ / Out$ / Tools$ / Total$."""
    rollup = cost_report()
    if not rollup["steps"]:
        return "(no API calls recorded)"
    header = (
        f"{'Step':<24}{'Model':<8}{'Calls':>6}"
        f"{'In':>11}{'Out':>11}"
        f"{'In$':>9}{'Out$':>9}{'Tools$':>9}{'Total$':>10}"
    )
    sep = "-" * len(header)
    lines = [sep, header, sep]
    for step, step_data in rollup["steps"].items():
        for model, c in step_data["models"].items():
            lines.append(
                f"{step:<24}{model:<8}{c['calls']:>6}"
                f"{c['input_tokens']:>11,}{c['output_tokens']:>11,}"
                f"{c['input_usd']:>9.4f}{c['output_usd']:>9.4f}"
                f"{c['web_search_usd']:>9.4f}{c['cost_usd']:>10.4f}"
            )
        lines.append(
            f"{'  subtotal':<24}{'':<8}{'':>6}{'':>11}{'':>11}"
            f"{step_data['input_usd']:>9.4f}{step_data['output_usd']:>9.4f}"
            f"{step_data['web_search_usd']:>9.4f}{step_data['cost_usd']:>10.4f}"
        )
    lines.append(sep)
    lines.append(
        f"{'TOTAL':<24}{'':<8}{'':>6}{'':>11}{'':>11}"
        f"{rollup['input_usd']:>9.4f}{rollup['output_usd']:>9.4f}"
        f"{rollup['web_search_usd']:>9.4f}{rollup['total_usd']:>10.4f}"
    )
    lines.append(sep)
    return "\n".join(lines)


def dump_cost_ledger(path: str | Path) -> Path:
    """Write the structured cost report to a JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cost_report(), indent=2))
    return path


# === Persistent ledger helpers ===
# The in-memory ledger is per-process. When the pipeline runs step-by-step
# across separate CLI invocations, we persist raw counters (not the rolled-up
# report) to disk so prices can be re-derived after later edits to PRICES.

def save_ledger(path: str | Path) -> Path:
    """Write raw ledger counters to JSON. Re-runs re-derive cost at read time."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger_snapshot(), indent=2))
    return path


def load_ledger(path: str | Path, *, replace: bool = True) -> None:
    """Load raw ledger counters from JSON into the in-memory ledger.

    `replace=True` (default) clears the current ledger first — the on-disk file
    is the single source of truth for a step-by-step run. Pass `replace=False`
    to merge (rare; useful for combining counters across parallel runs).
    """
    path = Path(path)
    if not path.exists():
        return
    raw = json.loads(path.read_text())
    with _LEDGER_LOCK:
        if replace:
            _LEDGER.clear()
        for step, models in raw.items():
            for model, counters in models.items():
                existing = _LEDGER.setdefault(step, {}).setdefault(model, _new_counters())
                for k, v in counters.items():
                    if k == "model_id":
                        existing[k] = v
                    else:
                        existing[k] = existing.get(k, 0) + int(v) if not replace else int(v)


def clear_steps(*step_names: str) -> None:
    """Drop the given step entries from the in-memory ledger.

    Called before re-running a step so the 'final run' cost overwrites the
    prior attempt instead of accumulating.
    """
    with _LEDGER_LOCK:
        for name in step_names:
            _LEDGER.pop(name, None)


def graft_snapshot(snap: dict) -> None:
    """Graft a snapshot (step -> model -> counters) into the in-memory ledger,
    overwriting any matching step entries. Used to re-inject a step's usage
    after a load_ledger round-trip (e.g. step 0 of the pipeline records its
    0_slug counters in memory before the slug is known — which means the disk
    ledger can't be loaded yet — and this helper re-plants them after the
    disk load."""
    with _LEDGER_LOCK:
        for step, models in snap.items():
            _LEDGER[step] = {m: dict(c) for m, c in models.items()}


def call(
    model: str,
    system: str,
    user: str,
    pdf_path: str | None = None,
    tools: list | None = None,
    max_tokens: int = 4096,
    step: str = "",
    stream: bool | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
    top_k: int | None = None,
) -> str:
    """One API call. Returns the joined assistant text across all text blocks.

    - `model` is a key of MODELS: "haiku" | "sonnet" | "opus".
    - `pdf_path`, if given, attaches the PDF as a document block (used for the
      Haiku per-page fan-out and the Sonnet quote spot-check).
    - `tools` is passed through for server-side tools like
      `{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}`.
      No client-side tool loop is needed — web_search is fully server-handled.
    - `step` labels this call in the cost ledger for the end-of-run report.
    - `stream`: if True, stream tokens to stderr as they arrive (so you can
      tell a long call is still alive). If None (default), consult the
      module-level `STREAM_DEFAULT` override; if that's also None, stream is
      enabled for all models. Use --no-streaming to disable.
    - `temperature`, `top_p`, `top_k`: sampling parameters. When None (default),
      the API's built-in defaults are used (temperature=1.0). All values are
      recorded in the per-call trace for reproducibility.
    """
    if DRY_RUN:
        _print_dry_run(step=step, model=model, system=system, user=user,
                       pdf_path=pdf_path, tools=tools, max_tokens=max_tokens)
        return DRY_RUN_PLACEHOLDER

    content: list[dict] = []
    if pdf_path:
        content.append(_pdf_block(pdf_path))
    content.append({"type": "text", "text": user})

    kwargs = {
        "model": MODELS[model],
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": content}],
    }
    if tools:
        kwargs["tools"] = tools
    if temperature is not None:
        kwargs["temperature"] = temperature
    if top_p is not None:
        kwargs["top_p"] = top_p
    if top_k is not None:
        kwargs["top_k"] = top_k

    trace_sampling = dict(temperature=temperature, top_p=top_p, top_k=top_k)

    if stream is None:
        stream = STREAM_DEFAULT if STREAM_DEFAULT is not None else True

    if not stream:
        t0 = time.monotonic()
        resp = _get_client().messages.create(**kwargs)
        duration = time.monotonic() - t0
        _record_usage(step=step, model=model, usage=resp.usage)
        output = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
        tool_trace = _extract_tool_trace(resp.content)
        _write_trace(step=step, model=model, system=system, user=user,
                     output=output, usage=resp.usage, duration_s=duration,
                     pdf_path=pdf_path, tools=tools, max_tokens=max_tokens,
                     tool_trace=tool_trace, **trace_sampling)
        return output

    # Streaming path: emit tokens to stderr as they arrive, then collect the
    # final message for accurate usage accounting.
    label = step or model
    print(f"\n  [{label}] streaming ▶ ", file=sys.stderr, end="", flush=True)
    t0 = time.monotonic()
    with _get_client().messages.stream(**kwargs) as stream_resp:
        for text in stream_resp.text_stream:
            print(text, file=sys.stderr, end="", flush=True)
        final = stream_resp.get_final_message()
    duration = time.monotonic() - t0
    print(file=sys.stderr)  # newline after the stream
    _record_usage(step=step, model=model, usage=final.usage)
    # Prefer the final message's text blocks as source of truth (covers
    # non-text blocks like server-tool-use interleaved with text).
    output = "".join(
        b.text for b in final.content if getattr(b, "type", None) == "text"
    )
    tool_trace = _extract_tool_trace(final.content)
    _write_trace(step=step, model=model, system=system, user=user,
                 output=output, usage=final.usage, duration_s=duration,
                 pdf_path=pdf_path, tools=tools, max_tokens=max_tokens,
                 tool_trace=tool_trace, **trace_sampling)
    return output


def call_parallel(jobs: list[dict], max_workers: int = 6) -> list[str]:
    """Run a list of `call()` kwargs dicts in parallel. Results are in input order."""
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(lambda j: call(**j), jobs))
