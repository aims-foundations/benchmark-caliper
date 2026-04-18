"""Flow-only smoke tests for the api_package pipeline.

Every `client.call` is replaced with a `FakeClient` that returns canned strings
keyed by the system prompt's first line. This exercises:

  - prompt loading (prompts/*.md resolve correctly)
  - ThreadPoolExecutor fan-out for per-page Haiku extraction
  - script subprocess contracts (split_pdf, verify_quotes, parse_llm_output,
    parse_elicitation_questions, assemble_elicitation_answers, compose_prompt,
    format_results)
  - Q/A round-trip through the elicitation assembler
  - full chain of file writes (papers/<name>/, benchmarks/, and the unified
    assessments/<name>/<slug>/ tree)

No network, no API key required.
"""

from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).parent / "fixtures"
FAKE_RESPONSES = FIXTURES / "fake_responses"
sys.path.insert(0, str(ROOT))

import client  # noqa: E402
import run_pipeline  # noqa: E402


# ===================================================================
# FakeClient — routes calls by matching the system prompt's first line
# to a canned fixture file.
# ===================================================================

# Elicitation calls are routed via USER_ROUTES (by user-message content) since
# the question and summary prompts share overlapping system-prompt text.
ROUTES = [
    ("You are extracting validity-relevant quotes from page",
     "pdf_extract_page.txt"),
    ("You will consolidate per-page JSON extractions",
     "pdf_extract_consolidate.md"),
    ("Pick the 1 or 2 benchmark YAMLs",
     "benchmark_example_selection.txt"),
    ("Synthesize a benchmark YAML from a paper summary",
     "benchmark_synthesis.txt"),
    ("role-playing as a practitioner",
     "persona_system.txt"),
    ("Produce a short slug",
     "slug_from_description.txt"),
    ("Pick the 1 or 2 base region template",
     "region_template_selection.txt"),
    ("Produce an assessment-specific region YAML",
     "region_synthesis.txt"),
    ("Web Search Guide for Cultural Validity",
     "web_search_guide.txt"),
    ("You are the validity analysis scorer",
     "opus_scoring_framing.txt"),
]


class FakeClient:
    """Signature-routing stand-in for `client.call`.

    Matches fixtures by (a) a unique substring in the system prompt, or (b) a
    unique substring in the user message (used to route elicitation calls
    whose system prompts overlap in structure).
    """

    # (where, signature, fixture). `where` is "system" or "user".
    USER_ROUTES = [
        # Elicitation: "Questions & answers:" only appears in the summary call.
        ("user", "Questions & answers:", "elicitation_summary.md"),
        # Remaining elicitation call (questions) keys on "Deployment description:".
        ("user", "Deployment description:", "elicitation_questions.txt"),
    ]

    def __init__(self) -> None:
        self.calls: list[dict] = []

    def __call__(self, model: str, system: str, user: str,
                 pdf_path: str | None = None,
                 tools: list | None = None,
                 max_tokens: int = 4096,
                 step: str = "") -> str:
        self.calls.append({
            "model": model,
            "step": step,
            "system_head": system[:160],
            "pdf": bool(pdf_path),
            "tools": tools,
        })
        # Resolve the canned response.
        response: str | None = None
        for where, signature, fixture_name in self.USER_ROUTES:
            target = user if where == "user" else system
            if signature in target:
                response = (FAKE_RESPONSES / fixture_name).read_text()
                break
        if response is None:
            for signature, fixture_name in ROUTES:
                if signature in system:
                    response = (FAKE_RESPONSES / fixture_name).read_text()
                    break
        if response is None:
            raise AssertionError(
                f"FakeClient: no route matched.\n"
                f"  len(system)={len(system)}\n"
                f"  head={system[:200]!r}\n"
                f"  tail={system[-400:]!r}\n"
                f"  user_head={user[:200]!r}"
            )
        # Mirror client.call's ledger write so persistence assertions can fire.
        # Token counts are rough proxies of the real prompt so cost-report math
        # stays recognizable without pretending to be accurate.
        web_searches = 0
        if tools and any(t.get("type", "").startswith("web_search") for t in tools):
            web_searches = 2  # canned: 2 searches per web-search call
        usage = _FakeUsage(
            input_tokens=max(1, len(system) // 4 + len(user) // 4),
            output_tokens=max(1, len(response) // 4),
            web_search_requests=web_searches,
        )
        client._record_usage(step=step, model=model, usage=usage)
        return response


# ===================================================================
# Fixtures / cleanup
# ===================================================================

@pytest.fixture
def clean_outputs():
    """Remove any pipeline outputs from prior runs so each test starts fresh."""
    import shutil
    # Top-level (non-assessment) outputs.
    (ROOT / "benchmarks" / "dummy.yaml").unlink(missing_ok=True)
    # Paper-scoped derived artifacts.
    paper_dir = ROOT / "papers" / "dummy"
    if paper_dir.exists():
        shutil.rmtree(paper_dir)
    # Every deployment-scoped artifact lives under assessments/<name>/...
    assessments_dir = ROOT / "assessments" / "dummy"
    if assessments_dir.exists():
        shutil.rmtree(assessments_dir)
    # Scrub the per-page Haiku cache so fan-out actually dispatches on each run.
    cache_dir = ROOT / "page_caches" / "dummy"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    yield


# ===================================================================
# Test 1 — persona mode: pipeline pauses after 1d-questions, then resumes
# via --step invocations once a CC Opus subagent answers file is supplied.
# ===================================================================

def test_flow_persona_mode(clean_outputs, capsys):
    fake = FakeClient()
    dummy_pdf = FIXTURES / "dummy.pdf"

    # === Phase 1: full run in persona mode — should pause after 1d-questions ===
    with patch.object(client, "call", side_effect=fake), \
         patch.object(sys, "argv",
                      ["run_pipeline.py", str(dummy_pdf),
                       "--persona", "helm-b",
                       "--no-web-search"]):
        run_pipeline.main()

    slug = (ROOT / "assessments" / "dummy" / "active_slug.txt").read_text().strip()
    assessment_dir = ROOT / "assessments" / "dummy" / slug
    persona_prompt = assessment_dir / "persona_prompt.md"
    questions = assessment_dir / "elicitation_questions.json"
    elicitation = assessment_dir / "elicitation_summary.md"

    assert persona_prompt.exists(), "persona handoff prompt not written"
    assert questions.exists(), "elicitation questions not written"
    assert not elicitation.exists(), "summary should NOT be written before CC Opus answers"
    # Persona system prompt must NOT have been invoked via API — the handoff
    # replaces it. No call should match the persona signature.
    persona_sig = "role-playing as a practitioner"
    persona_api_calls = [c for c in fake.calls if persona_sig in c["system_head"]]
    assert not persona_api_calls, "persona call fired via API (should be CC subagent handoff)"

    prompt_body = persona_prompt.read_text()
    assert "helm-b" in prompt_body
    assert "Claude Code Opus subagent" in prompt_body
    assert "## System prompt" in prompt_body
    assert "## User message" in prompt_body
    # Persona block content must be substituted into the system prompt section.
    assert "Kisumu" in prompt_body, "persona_block not rendered into the handoff prompt"

    # === Phase 2: CC Opus subagent produces an answers file (simulated here) ===
    qs = json.loads(questions.read_text())
    canned = {q["id"]: f"Simulated persona reply for {q['id']}" for q in qs}
    answers_path = assessment_dir / "elicitation_answers.json"
    answers_path.write_text(json.dumps(canned))

    # === Phase 3: drive the remaining steps via --step invocations ===
    for step in ("1d-summary", "2a-template", "2b-synthesize", "4", "5", "6"):
        extra = ["--answers", str(answers_path)] if step == "1d-summary" else []
        with patch.object(client, "call", side_effect=fake), \
             patch.object(sys, "argv",
                          ["run_pipeline.py", str(dummy_pdf),
                           "--step", step, *extra]):
            run_pipeline.main()

    # === File-level assertions ===
    summary = ROOT / "papers" / "dummy" / "paper_summary.md"
    benchmark = ROOT / "benchmarks" / "dummy.yaml"
    region_yaml = assessment_dir / "region.yaml"
    composed = assessment_dir / "composed_prompt.md"
    scoring = assessment_dir / "scoring.json"

    assert summary.exists(), "paper summary not written"
    assert benchmark.exists(), "benchmark YAML not written"
    assert elicitation.exists(), "elicitation summary not written"
    assert region_yaml.exists(), f"region YAML missing at {region_yaml}"
    assert composed.exists(), f"composed prompt missing at {composed}"
    assert scoring.exists(), f"scoring JSON missing at {scoring}"

    # === Benchmark YAML covers all 6 dimensions ===
    bm = yaml.safe_load(benchmark.read_text())
    assert bm["name"] == "dummybench"
    dims_seen = {q["dimension"] for q in bm["verbatim_quotes"]}
    assert dims_seen == {
        "input_ontology", "input_content", "input_form",
        "output_ontology", "output_content", "output_form",
    }

    # === Scoring JSON has all 6 dimensions + risk assessment ===
    results = json.loads(scoring.read_text())
    assert set(results["dimensions"].keys()) == {
        "input_ontology", "input_content", "input_form",
        "output_ontology", "output_content", "output_form",
    }
    assert results["risk_assessment"] in {"low", "medium", "high"}

    # === Model routing: at least one Opus + Sonnet + Haiku call, exactly one Opus ===
    models_used = {c["model"] for c in fake.calls}
    assert {"haiku", "sonnet", "opus"}.issubset(models_used), models_used
    opus_calls = [c for c in fake.calls if c["model"] == "opus"]
    assert len(opus_calls) == 1, "should be exactly one Opus call (scoring)"

    # === Every call is tagged; 1d_persona is gone (CC subagent, not API) ===
    untagged = [c for c in fake.calls if not c["step"]]
    assert not untagged, f"calls missing step= label: {untagged}"
    expected_steps = {
        "0_slug",
        "1a_extract", "1a_consolidate",
        "1b_select", "1b_synthesize",
        "1d_questions", "1d_summary",
        "2a_template", "2b_synthesize",
        "5_score",
    }
    steps_seen = {c["step"] for c in fake.calls}
    assert "1d_persona" not in steps_seen, "persona API call must not fire"
    assert expected_steps == steps_seen, (
        f"unexpected step set. missing={expected_steps - steps_seen}, "
        f"extra={steps_seen - expected_steps}"
    )

    # === Persistent cost ledger survived across --step invocations ===
    cost_ledger = assessment_dir / "cost_ledger.json"
    assert cost_ledger.exists(), f"persistent cost ledger not written at {cost_ledger}"
    persisted = json.loads(cost_ledger.read_text())
    # Every step label that fired should appear in the persisted ledger.
    persisted_steps = set(persisted.keys())
    assert expected_steps.issubset(persisted_steps), (
        f"ledger missing steps: {expected_steps - persisted_steps}"
    )

    # === Report printed to stdout ===
    captured = capsys.readouterr().out
    assert "Validity Analysis" in captured
    assert "Dimension Scores" in captured


# ===================================================================
# Test 2 — full flow, interactive (stdin) mode via --use-case
# ===================================================================

def test_flow_interactive_mode(clean_outputs, monkeypatch):
    fake = FakeClient()
    dummy_pdf = FIXTURES / "dummy.pdf"
    use_case = FIXTURES / "use_case.txt"

    # Pipe 3 answers for the 3 elicitation questions. Deployment description
    # comes from --use-case so stdin isn't consumed for it.
    answers = "swahili and english\nfive triage categories\nshort voice-to-text\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(answers))

    with patch.object(client, "call", side_effect=fake), \
         patch.object(sys, "argv",
                      ["run_pipeline.py", str(dummy_pdf),
                       "--use-case", str(use_case),
                       "--no-web-search"]):
        run_pipeline.main()

    # Persona system prompt must NOT have been invoked in this mode.
    persona_sig = "role-playing as a practitioner"
    persona_calls = [c for c in fake.calls if persona_sig in c["system_head"]]
    assert not persona_calls, "persona call fired in interactive mode"

    # Elicitation summary written and reflects the interactive answers.
    slug = (ROOT / "assessments" / "dummy" / "active_slug.txt").read_text().strip()
    assessment_dir = ROOT / "assessments" / "dummy" / slug
    elicitation = assessment_dir / "elicitation_summary.md"
    assert elicitation.exists()
    # Answers file written by step_1d_collect_stdin.
    answers_path = assessment_dir / "elicitation_answers.json"
    assert answers_path.exists()
    assert json.loads(answers_path.read_text()) == {
        "Q1": "swahili and english",
        "Q2": "five triage categories",
        "Q3": "short voice-to-text",
    }


# ===================================================================
# Test 3 — parse_llm_output.py, JSON fence stripping
# ===================================================================

def test_parse_llm_output_json():
    raw = 'Here you go:\n```json\n{"name": "dummybench", "year": 2026}\n```\nEnd.'
    result = subprocess.run(
        ["python3", str(ROOT / "scripts" / "parse_llm_output.py"),
         "--format", "json", "-"],
        input=raw, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    parsed = json.loads(result.stdout)
    assert parsed == {"name": "dummybench", "year": 2026}


# ===================================================================
# Test 4 — parse_llm_output.py, YAML fence stripping
# ===================================================================

def test_parse_llm_output_yaml():
    raw = "Sure thing:\n```yaml\nname: dummybench\nyear: 2026\n```\nCheers."
    result = subprocess.run(
        ["python3", str(ROOT / "scripts" / "parse_llm_output.py"),
         "--format", "yaml", "-"],
        input=raw, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    parsed = yaml.safe_load(result.stdout)
    assert parsed == {"name": "dummybench", "year": 2026}


# ===================================================================
# Test 5 — parse_elicitation_questions.py
# ===================================================================

def test_parse_elicitation_questions_valid():
    raw = (FAKE_RESPONSES / "elicitation_questions.txt").read_text()
    result = subprocess.run(
        ["python3", str(ROOT / "scripts" / "parse_elicitation_questions.py"), "-"],
        input=raw, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    qs = json.loads(result.stdout)
    assert len(qs) == 3
    assert {q["dimension"] for q in qs} == {"IC", "OO", "IF"}


def test_parse_elicitation_questions_malformed():
    result = subprocess.run(
        ["python3", str(ROOT / "scripts" / "parse_elicitation_questions.py"), "-"],
        input='[{"id": "Q1"}]',  # missing dimension + question
        capture_output=True, text=True,
    )
    assert result.returncode == 1


# ===================================================================
# Test 6 — assemble_elicitation_answers.py
# ===================================================================

def test_assemble_elicitation_answers(tmp_path):
    q_path = tmp_path / "q.json"
    a_path = tmp_path / "a.json"
    q_path.write_text(json.dumps([
        {"id": "Q1", "dimension": "IC", "question": "Languages?"},
        {"id": "Q2", "dimension": "OO", "question": "Label set?"},
    ]))
    a_path.write_text(json.dumps({"Q1": "swahili", "Q2": "triage"}))

    result = subprocess.run(
        ["python3", str(ROOT / "scripts" / "assemble_elicitation_answers.py"),
         "--questions", str(q_path), "--answers", str(a_path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    body = result.stdout
    assert "Q1 [IC]: Languages?" in body
    assert "A1: swahili" in body
    assert "Q2 [OO]: Label set?" in body
    assert "A2: triage" in body


# ===================================================================
# Test 7 — verify_quotes.py pass + fail
# ===================================================================

def test_verify_quotes_pass(tmp_path):
    # Copy the canned paper summary and a valid benchmark YAML.
    summary = tmp_path / "summary.md"
    summary.write_text((FAKE_RESPONSES / "pdf_extract_consolidate.md").read_text())

    # The benchmark_synthesis fixture is fenced YAML; strip the fence for a
    # direct copy.
    bench_raw = (FAKE_RESPONSES / "benchmark_synthesis.txt").read_text()
    bench_yaml = bench_raw.split("```yaml\n", 1)[1].split("\n```", 1)[0]
    bench = tmp_path / "bench.yaml"
    bench.write_text(bench_yaml)

    result = subprocess.run(
        ["python3", str(ROOT / "scripts" / "verify_quotes.py"),
         str(bench), str(summary)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr + "\n" + result.stdout


def test_verify_quotes_fail_on_missing_dimension(tmp_path):
    summary = tmp_path / "summary.md"
    summary.write_text(
        "| ID | Page | Dimension | Text |\n"
        "|----|------|-----------|------|\n"
        "| Q1 | 1 | input_ontology | \"x\" |\n"
    )
    bench = tmp_path / "bench.yaml"
    bench.write_text(yaml.safe_dump({
        "verbatim_quotes": [
            {"id": "Q1", "page": 1, "dimension": "input_ontology", "text": "x"},
        ],
    }))
    result = subprocess.run(
        ["python3", str(ROOT / "scripts" / "verify_quotes.py"),
         str(bench), str(summary)],
        capture_output=True, text=True,
    )
    # Only 1 dimension covered → must fail
    assert result.returncode == 1


# ===================================================================
# Test 8 — client.py cost ledger: record → snapshot → format round-trip
# ===================================================================

class _FakeUsage:
    """Duck-typed stand-in for anthropic's Usage response object."""
    def __init__(self, input_tokens: int, output_tokens: int,
                 web_search_requests: int = 0) -> None:
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_creation_input_tokens = 0
        self.cache_read_input_tokens = 0
        if web_search_requests:
            class _STU:
                pass
            stu = _STU()
            stu.web_search_requests = web_search_requests
            self.server_tool_use = stu
        else:
            self.server_tool_use = None


def test_cost_ledger_records_and_prices():
    client.reset_ledger()
    # Two Haiku calls in the same step → should aggregate.
    client._record_usage("1a_extract_page", "haiku", _FakeUsage(1000, 500))
    client._record_usage("1a_extract_page", "haiku", _FakeUsage(2000, 300))
    # One Sonnet call with web search.
    client._record_usage("3_web_search", "sonnet", _FakeUsage(5000, 2000, web_search_requests=4))
    # One Opus call.
    client._record_usage("5_score", "opus", _FakeUsage(45000, 15000))

    snap = client.ledger_snapshot()
    assert snap["1a_extract_page"]["haiku"]["calls"] == 2
    assert snap["1a_extract_page"]["haiku"]["input_tokens"] == 3000
    assert snap["1a_extract_page"]["haiku"]["output_tokens"] == 800
    assert snap["3_web_search"]["sonnet"]["web_search_requests"] == 4

    rollup = client.cost_report()
    # Spot-check pricing: Opus @ $15/M in + $75/M out for (45000, 15000):
    # = 45000/1e6 * 15 + 15000/1e6 * 75 = 0.675 + 1.125 = 1.80
    assert abs(rollup["steps"]["5_score"]["cost_usd"] - 1.80) < 1e-6
    # Input/output split for the same Opus row.
    assert abs(rollup["steps"]["5_score"]["input_usd"] - 0.675) < 1e-6
    assert abs(rollup["steps"]["5_score"]["output_usd"] - 1.125) < 1e-6
    assert rollup["steps"]["5_score"]["web_search_usd"] == 0.0
    # Web search: 4 searches at $10/1000 = $0.04, plus the Sonnet token charge
    # 5000/1e6 * 3 + 2000/1e6 * 15 = 0.015 + 0.030 = 0.045, total = 0.085.
    assert abs(rollup["steps"]["3_web_search"]["cost_usd"] - 0.085) < 1e-6
    assert abs(rollup["steps"]["3_web_search"]["web_search_usd"] - 0.04) < 1e-6
    assert abs(rollup["steps"]["3_web_search"]["input_usd"] - 0.015) < 1e-6
    assert abs(rollup["steps"]["3_web_search"]["output_usd"] - 0.030) < 1e-6
    # Top-level totals match the sum of parts.
    assert abs(
        rollup["input_usd"] + rollup["output_usd"] + rollup["web_search_usd"]
        - rollup["total_usd"]
    ) < 1e-6

    report = client.format_cost_report()
    assert "1a_extract_page" in report
    assert "5_score" in report
    assert "TOTAL" in report
    assert "In$" in report and "Out$" in report and "Tools$" in report

    client.reset_ledger()
    assert client.ledger_snapshot() == {}


def test_ledger_persistence_round_trip(tmp_path):
    """save_ledger → reset → load_ledger should reproduce the original snapshot."""
    client.reset_ledger()
    client._record_usage("1a_extract_page", "haiku", _FakeUsage(1000, 500))
    client._record_usage("3_web_search", "sonnet", _FakeUsage(5000, 2000, web_search_requests=4))
    original = client.ledger_snapshot()

    path = client.save_ledger(tmp_path / "cost_ledger.json")
    assert path.exists()

    client.reset_ledger()
    assert client.ledger_snapshot() == {}
    client.load_ledger(path)
    assert client.ledger_snapshot() == original

    # load_ledger on a missing file is a no-op, not an error.
    client.reset_ledger()
    client.load_ledger(tmp_path / "does_not_exist.json")
    assert client.ledger_snapshot() == {}


def test_clear_steps_overwrites_on_rerun(tmp_path):
    """clear_steps drops prior entries so re-running a step 'overwrites' cost."""
    client.reset_ledger()
    # Simulate a first (expensive) attempt at step 1a.
    client._record_usage("1a_extract_page", "haiku", _FakeUsage(10000, 5000))
    client.save_ledger(tmp_path / "ledger.json")

    # Second invocation of the pipeline step: load prior ledger, clear this
    # step, record the final run's usage, save.
    client.reset_ledger()
    client.load_ledger(tmp_path / "ledger.json")
    client.clear_steps("1a_extract_page")
    client._record_usage("1a_extract_page", "haiku", _FakeUsage(1000, 500))
    client.save_ledger(tmp_path / "ledger.json")

    client.reset_ledger()
    client.load_ledger(tmp_path / "ledger.json")
    snap = client.ledger_snapshot()
    # Counters reflect only the final run, not the sum of both attempts.
    assert snap["1a_extract_page"]["haiku"]["input_tokens"] == 1000
    assert snap["1a_extract_page"]["haiku"]["output_tokens"] == 500
    assert snap["1a_extract_page"]["haiku"]["calls"] == 1
    client.reset_ledger()
