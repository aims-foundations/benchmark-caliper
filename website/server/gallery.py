"""Curated benchmark gallery — read-only views of expert assessments.

Surfaces the completed assessments under
`anthropic_api_package_release/assessments/<expert>__<benchmark>/<slug>/`
as a public, read-only gallery. These are runs experts already paid for
and completed; the website just displays them.

This module never writes anything and never calls the Anthropic API. An
entry `id` is always an existing assessment directory name — callers must
pass an `id` from `list_entries()`, never a user-constructed path, so
directory traversal is structurally impossible.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import yaml

_ASSESSMENTS_ROOT = (
    Path(__file__).resolve().parent.parent.parent
    / "anthropic_api_package_release"
    / "assessments"
)


def _slug_dir(assessment_dir: Path) -> Path | None:
    """Return the deployment-slug subdirectory that holds a scored run."""
    if not assessment_dir.is_dir():
        return None
    for sub in sorted(assessment_dir.iterdir()):
        if sub.is_dir() and (sub / "scoring.json").is_file():
            return sub
    return None


def _benchmark_name(slug_dir: Path, fallback: str) -> str:
    """Display name for a benchmark — prefer benchmark.yaml, else the slug."""
    yaml_path = slug_dir / "benchmark.yaml"
    if yaml_path.is_file():
        try:
            data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            data = None
        if isinstance(data, dict):
            name = data.get("full_name") or data.get("name")
            if isinstance(name, str) and name.strip():
                return name.strip()
    return fallback


@lru_cache(maxsize=1)
def list_entries() -> list[dict]:
    """All curated gallery entries, sorted by benchmark display name.

    Dedup rule: if two assessments share both the benchmark name and the
    deployment slug, only the first is kept (per spec). In the current
    data set this removes nothing — every (benchmark, slug) pair is
    unique — but the rule guards against future collisions.

    Cached: the assessments directory is static at runtime.
    """
    if not _ASSESSMENTS_ROOT.is_dir():
        return []

    entries: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for assessment_dir in sorted(_ASSESSMENTS_ROOT.iterdir()):
        if not assessment_dir.is_dir():
            continue
        slug_dir = _slug_dir(assessment_dir)
        if slug_dir is None:
            continue

        dir_id = assessment_dir.name
        # Directory names are `expert_<hash>__<benchmark>`; the suffix is a
        # readable fallback if benchmark.yaml is missing or unparseable.
        suffix = dir_id.split("__", 1)[-1]
        name = _benchmark_name(slug_dir, suffix)
        slug = slug_dir.name

        key = (name.lower(), slug.lower())
        if key in seen:
            continue
        seen.add(key)

        dep_path = slug_dir / "deployment_description.txt"
        deployment = (
            dep_path.read_text(encoding="utf-8").strip()
            if dep_path.is_file()
            else ""
        )

        entries.append(
            {
                "id": dir_id,
                "benchmark_name": name,
                "slug": slug,
                "deployment_description": deployment,
            }
        )

    entries.sort(key=lambda e: e["benchmark_name"].lower())
    return entries


def _entry_ids() -> set[str]:
    return {e["id"] for e in list_entries()}


def get_report(entry_id: str) -> dict | None:
    """Scoring data + raw Opus text for one curated benchmark.

    Returns None if `entry_id` is not a known gallery entry — callers
    should treat that as a 404. The whitelist check means `entry_id`
    cannot escape the assessments directory.
    """
    if entry_id not in _entry_ids():
        return None
    slug_dir = _slug_dir(_ASSESSMENTS_ROOT / entry_id)
    if slug_dir is None:
        return None

    scoring_path = slug_dir / "scoring.json"
    try:
        scoring = json.loads(scoring_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    # Raw Opus output lives in the step-7 trace; fall back to a pretty
    # dump of the parsed scoring if the trace is absent.
    raw = ""
    trace_path = slug_dir / "traces" / "7_score.jsonl"
    if trace_path.is_file():
        try:
            first = json.loads(trace_path.read_text(encoding="utf-8").splitlines()[0])
            if isinstance(first.get("output"), str):
                raw = first["output"]
        except (OSError, json.JSONDecodeError, IndexError):
            raw = ""
    if not raw:
        raw = json.dumps(scoring, indent=2, ensure_ascii=False)

    entry = next(e for e in list_entries() if e["id"] == entry_id)
    return {
        "id": entry_id,
        "benchmark_name": entry["benchmark_name"],
        "slug": entry["slug"],
        "deployment_description": entry["deployment_description"],
        "scoring": scoring,
        "raw": raw,
    }


def review_pdf_path(entry_id: str) -> Path | None:
    """Filesystem path to a curated benchmark's review.pdf, or None."""
    if entry_id not in _entry_ids():
        return None
    slug_dir = _slug_dir(_ASSESSMENTS_ROOT / entry_id)
    if slug_dir is None:
        return None
    pdf = slug_dir / "pdfs" / "review.pdf"
    return pdf if pdf.is_file() else None
