"""Step 5b — HuggingFace dataset analysis.

Imports the deterministic helpers from the release pipeline
(`_resolve_hf_info`, `_profile_single_dataset`, `_resolve_org_datasets`,
`_validate_content_sample`, `_resolve_cited_evidence`,
`_requires_remote_code`) so the data-fetching half is byte-identical to
the CLI. The Sonnet interpretation half is rewritten on top of
`call_text_async` so each call uses the per-request user API key,
matching the website's BYOK contract.

Output: a markdown blob the caller passes to Step 7 as
`## Dataset Analysis Findings`, the same wrapper the CLI uses in
run_pipeline.py:1922 (org mode) / :1981 (single mode).
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Awaitable, Callable, Optional

from .anthropic_client import call_text_async

# Make the release package importable for the helper functions we lift
# from run_pipeline. pipeline_runner already does this, but we run on the
# import path so re-doing it here is cheap and keeps this module
# importable standalone (tests, etc).
_PACKAGE_ROOT = (
    Path(__file__).resolve().parent.parent.parent / "anthropic_api_package_release"
)
if str(_PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(_PACKAGE_ROOT))


# The Sonnet prompts ship with the package, same dir we already point at
# for every other step.
PROMPTS_DIR = _PACKAGE_ROOT / "prompts"


# ---------- pipeline helpers we borrow unchanged ----------


def _pipeline_helpers():
    """Lazy import so `pip install datasets` is only enforced when DA runs."""
    from run_pipeline import (
        HF_LINKS_FILE,
        _profile_single_dataset,
        _requires_remote_code,
        _resolve_cited_evidence,
        _resolve_org_datasets,
        _validate_content_sample,
    )
    return SimpleNamespace(
        HF_LINKS_FILE=HF_LINKS_FILE,
        profile_single_dataset=_profile_single_dataset,
        requires_remote_code=_requires_remote_code,
        resolve_cited_evidence=_resolve_cited_evidence,
        resolve_org_datasets=_resolve_org_datasets,
        validate_content_sample=_validate_content_sample,
    )


# ---------- resolution ----------


def resolve_target(
    *,
    hf_dataset_id: Optional[str],
    hf_config: Optional[str],
    benchmark_name: Optional[str],
) -> Optional[dict]:
    """Mirror of `run_pipeline._resolve_hf_info` but driven by request args
    instead of argparse + on-disk slug.

    Returns one of:
        {"mode": "single", "hf_dataset_id": "...", "hf_config": ...}
        {"mode": "org",    "hf_org": "..."}
        None — no DA available (skip the step)
    """
    h = _pipeline_helpers()

    if hf_dataset_id:
        if h.requires_remote_code(hf_dataset_id):
            return None
        return {
            "mode": "single",
            "hf_dataset_id": hf_dataset_id,
            "hf_config": hf_config,
        }

    if not benchmark_name:
        return None
    if not h.HF_LINKS_FILE.exists():
        return None

    links = json.loads(h.HF_LINKS_FILE.read_text())
    # The CLI tries both the full name and the part after "__" (used for
    # expert-namespaced entries). Replicate that.
    for key in [benchmark_name, benchmark_name.split("__", 1)[-1]]:
        entry = links.get(key)
        if not entry:
            continue
        if entry.get("hf_org"):
            return {"mode": "org", "hf_org": entry["hf_org"]}
        if entry.get("hf_dataset_id"):
            ds_id = entry["hf_dataset_id"]
            if h.requires_remote_code(ds_id):
                return None
            return {
                "mode": "single",
                "hf_dataset_id": ds_id,
                "hf_config": entry.get("hf_config"),
            }
    return None


# ---------- Sonnet calls (BYOK) ----------


def _build_data_block(script_outputs: dict) -> str:
    """Format DA script outputs the same way the CLI does.

    Mirrors run_pipeline.py:1961-1972 (single) and :1644-1656 (per-dataset).
    """
    sections: list[str] = [
        f"### HF Metadata\n```json\n{script_outputs.get('hf_metadata', '{}')}\n```"
    ]
    content_json = script_outputs.get("content_sample", "{}")
    try:
        content_md = json.loads(content_json).get("markdown", content_json)
    except (json.JSONDecodeError, AttributeError):
        content_md = content_json
    sections.append(f"### Sampled Examples\n\n{content_md}")
    if "audio_stats" in script_outputs:
        sections.append(
            f"### Audio Stats\n```json\n{script_outputs['audio_stats']}\n```"
        )
    return "\n\n".join(sections)


def _load_da_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text()


async def _sonnet_single_interpret(
    *,
    api_key: str,
    benchmark_yaml: str,
    elicitation_summary: str,
    web_search_text: str,
    data_block: str,
) -> str:
    user = (
        f"## Benchmark YAML\n\n```yaml\n{benchmark_yaml}\n```\n\n"
        f"## Deployment Context (Elicitation Summary)\n\n{elicitation_summary}\n\n"
        f"## Web Search Findings\n\n{web_search_text}\n\n"
        f"## Dataset Content\n\n{data_block}"
    )
    result = await call_text_async(
        api_key=api_key,
        family="sonnet",
        system=_load_da_prompt("da_interpret"),
        user=user,
        max_tokens=16384,
    )
    return result.text


async def _sonnet_per_dataset(
    *,
    api_key: str,
    hf_dataset_id: str,
    script_outputs: dict,
    benchmark_yaml: str,
    elicitation_summary: str,
) -> str:
    data_block = _build_data_block(script_outputs)
    user = (
        f"## Dataset: {hf_dataset_id}\n\n"
        f"## Benchmark YAML\n\n```yaml\n{benchmark_yaml}\n```\n\n"
        f"## Deployment Context (Elicitation Summary)\n\n{elicitation_summary}\n\n"
        f"## Dataset Content\n\n{data_block}"
    )
    result = await call_text_async(
        api_key=api_key,
        family="sonnet",
        system=_load_da_prompt("da_per_dataset"),
        user=user,
        max_tokens=8192,
    )
    return result.text


async def _sonnet_aggregate(
    *,
    api_key: str,
    benchmark_yaml: str,
    elicitation_summary: str,
    web_search_text: str,
    per_dataset_summaries: dict[str, str],
) -> str:
    summaries_block = "\n\n".join(
        f"### {ds_id}\n\n{summary}"
        for ds_id, summary in per_dataset_summaries.items()
    )
    user = (
        f"## Benchmark YAML\n\n```yaml\n{benchmark_yaml}\n```\n\n"
        f"## Deployment Context (Elicitation Summary)\n\n{elicitation_summary}\n\n"
        f"## Web Search Findings\n\n{web_search_text}\n\n"
        f"## Per-Dataset Analysis Reports\n\n{summaries_block}"
    )
    result = await call_text_async(
        api_key=api_key,
        family="sonnet",
        system=_load_da_prompt("da_aggregate"),
        user=user,
        max_tokens=16384,
    )
    return result.text


# ---------- public drivers ----------


EmitFn = Callable[[str, dict], Awaitable[None]]


async def _noop_emit(_name: str, _payload: dict) -> None:
    return None


async def run_single(
    *,
    api_key: str,
    hf_dataset_id: str,
    hf_config: Optional[str],
    benchmark_yaml: str,
    elicitation_summary: str,
    web_search_text: str,
    emit: EmitFn = _noop_emit,
) -> str:
    """Single-dataset DA: profile + one Sonnet `da_interpret` call.

    Returns the Sonnet markdown report. Raises on script errors that the
    pipeline treats as fatal (empty content_sample), matching the CLI's
    behaviour at run_pipeline.py:1958.
    """
    h = _pipeline_helpers()
    await emit("step-progress", {"step": "5b-profile", "hf_dataset_id": hf_dataset_id})
    # Profiling does subprocess I/O — run off the event loop.
    script_outputs = await asyncio.to_thread(
        h.profile_single_dataset, hf_dataset_id, hf_config
    )
    # Mirrors the CLI's hard-fail when no examples were sampled.
    h.validate_content_sample(
        script_outputs,
        hf_dataset_id,
        Path(""),  # cache_path unused in our flow (no cache invalidation)
    )

    await emit("step-started", {"step": "5b-interpret"})
    data_block = _build_data_block(script_outputs)
    report = await _sonnet_single_interpret(
        api_key=api_key,
        benchmark_yaml=benchmark_yaml,
        elicitation_summary=elicitation_summary,
        web_search_text=web_search_text,
        data_block=data_block,
    )
    await emit("step-completed", {"step": "5b-interpret"})
    return report


async def run_org(
    *,
    api_key: str,
    hf_org: str,
    benchmark_yaml: str,
    elicitation_summary: str,
    web_search_text: str,
    emit: EmitFn = _noop_emit,
) -> str:
    """Org-mode DA: profile each dataset, per-dataset Sonnet summaries,
    then one aggregate Sonnet call + citation resolution.

    Mirrors run_pipeline.py:1849-1932 minus the trace-based resume.
    """
    h = _pipeline_helpers()
    dataset_ids = await asyncio.to_thread(h.resolve_org_datasets, hf_org)
    await emit(
        "step-progress",
        {"step": "5b-org-resolved", "hf_org": hf_org, "count": len(dataset_ids)},
    )

    per_dataset_summaries: dict[str, str] = {}
    for i, ds_id in enumerate(dataset_ids, 1):
        await emit(
            "step-progress",
            {
                "step": "5b-profile",
                "hf_dataset_id": ds_id,
                "completed": i - 1,
                "total": len(dataset_ids),
            },
        )
        script_outputs = await asyncio.to_thread(
            h.profile_single_dataset, ds_id, None
        )
        # Org mode tolerates per-dataset content_sample errors (the CLI
        # silently keeps going via try/except around the validator).
        summary = await _sonnet_per_dataset(
            api_key=api_key,
            hf_dataset_id=ds_id,
            script_outputs=script_outputs,
            benchmark_yaml=benchmark_yaml,
            elicitation_summary=elicitation_summary,
        )
        per_dataset_summaries[ds_id] = summary

    await emit(
        "step-started",
        {"step": "5b-aggregate", "count": len(dataset_ids)},
    )
    report = await _sonnet_aggregate(
        api_key=api_key,
        benchmark_yaml=benchmark_yaml,
        elicitation_summary=elicitation_summary,
        web_search_text=web_search_text,
        per_dataset_summaries=per_dataset_summaries,
    )
    # Replaces bare citation IDs with full excerpts so the report stands
    # on its own. Same function the CLI calls at run_pipeline.py:1932.
    report = h.resolve_cited_evidence(report, per_dataset_summaries)
    await emit("step-completed", {"step": "5b-aggregate"})
    return report
