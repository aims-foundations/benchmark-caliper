# Six-score item analysis

Each benchmark item receives six deployment-specific assessments: Input
Ontology, Input Content, Input Form, Output Ontology, Output Content, and Output
Form. Shared deployment and benchmark evidence is assembled once, then one
primary model request assesses all six dimensions for each item.

```text
Saved deployment requirements + benchmark documentation + dataset evidence
  → assemble shared context and the fixed six-dimension item rubric once
  → one scoring request per item, returning six assessments
  → validate, save, resume, report, and independently review
```

Context assembly requires no model call and does not generate classifiers.
The six questions and scoring anchors are fixed in `scoring.py` and
[prompts/assess_item.md](prompts/assess_item.md). The deployment supplies the
requirements against which they are applied.

| Dimension | Item-level question |
| --- | --- |
| Input Ontology | Does this item test a deployment-relevant task or capability? |
| Input Content | Does this particular question or scenario fit the deployment's users, language, and domain? |
| Input Form | Do the item's input modality and representation match deployment inputs? |
| Output Ontology | Do its expected decisions and grading criteria capture deployment success? |
| Output Content | Is its reference answer or expected judgment appropriate for deployment? |
| Output Form | Does its expected response format or modality match deployment needs? |

Each dimension returns `score` (an integer 1–5 or `null`), `justification`,
`evidence`, and `information_gaps`. Scores mean 1 = fundamental mismatch,
2 = substantial mismatch, 3 = partial alignment, 4 = strong alignment with minor
limitations, and 5 = strong alignment supported by evidence. Numerical scores
require evidence; Unknown (`null`) requires an information gap. All six dimensions
always appear. Unknown is a valid completed judgment, not a processing error or
a low score. An item can therefore be complete while some scores are Unknown.

Input Ontology assesses the relevance of the individual item, not coverage of
all deployment tasks. Prior benchmark scores and model-written hypotheses do
not ground item judgments. The original benchmark assessment remains separate;
item scores never overwrite it. No combined item rank or benchmark score is
computed from the six scores.

## Prepare a run

Run commands from the repository root:

```bash
python -m pip install -r anthropic_api_package_release/requirements.txt

python -m anthropic_api_package_release.item_analysis prepare \
  --assessment-dir /path/to/existing/assessment \
  --items /path/to/items.parquet \
  --source-revision SOURCE_COMMIT \
  --source-table benchmark/items.parquet \
  --output-dir results/item_analysis/example \
  --seed 42
```

Preparation freezes the dataset, source evidence, deterministic profile, and
shared scoring context. Available deployment answers, benchmark instructions,
label definitions, scoring rules, and regional/domain evidence retain their
source IDs and roles. Missing evidence stays explicit. The fixed context is
saved as `classifier_spec.json` for compatibility with existing artifact paths.
Original elicitation questions remain paired with user answers so references
such as "both" retain their meaning. Questions have a separate context role;
their assumptions do not establish deployment requirements.
The website also supports starting directly from deployment requirements
without running a benchmark assessment first.

To assemble six-score context for an existing prepared directory that has no
specification or scoring configuration:

```bash
python -m anthropic_api_package_release.item_analysis prepare-context \
  --run-dir results/item_analysis/example --dry-run

python -m anthropic_api_package_release.item_analysis prepare-context \
  --run-dir results/item_analysis/example
```

Inspect the context before interpreting judgments. Source and structural checks
do not establish semantic correctness. `specification.json` records context
assembly and retains `semantic_validation: "unreviewed"`.

The item adapter preserves questions, references, answer choices, grading rules,
metadata, features, verifiers, and media references when available. Verifiers
are never executed. A path or URL alone does not mean an image or audio asset
was inspected. Missing references and unavailable modalities can leave a
dimension Unknown. Items retain unique IDs and a deterministic shuffled order;
source checksums identify the prepared snapshot.

## Score items and resume

Preview complete requests without making model calls:

```bash
python -m anthropic_api_package_release.item_analysis classify \
  --run-dir results/item_analysis/example --dry-run --limit 100
```

Score a selected prefix with the configured model and API credentials:

```bash
python -m anthropic_api_package_release.item_analysis classify \
  --run-dir results/item_analysis/example --limit 100
```

For 100 items, the normal workload is 100 primary requests producing 600
dimension assessments. Each request includes the same shared source context,
the full item evidence, and the fixed rubric. The response is validated as a
single six-dimension assessment. A structurally invalid response receives at
most one repair attempt; unrecoverable failures are operational errors without
fabricated dimension scores. API failures stop further calls and preserve saved
progress. Repairs and retries add calls.

Completed items are saved immediately and are skipped on resume. Failed or
pending items are retried; the selected prefix may grow:

```bash
python -m anthropic_api_package_release.item_analysis classify \
  --run-dir results/item_analysis/example --limit 100 --resume

python -m anthropic_api_package_release.item_analysis classify \
  --run-dir results/item_analysis/example --all --resume
```

The dataset, context, rubric, prompt, and model settings remain frozen. Changed
inputs require a new run directory. Run locks reject concurrent writers; an
interrupted final append can be recovered on resume, while other corruption
fails validation. A call received but not saved before interruption may need
to be repeated.

## Results and independent human review

Rebuild reports offline:

```bash
python -m anthropic_api_package_release.item_analysis report \
  --run-dir results/item_analysis/example
```

`report.html` shows one row per prepared item and six score columns. Expand a
score to inspect its explanation, evidence, and information gaps. `items.csv`
contains the same assessments, full item evidence, selection flags, and distinct
Unknown/error/pending states. `summary.json` records six score distributions for
the selected items, selected progress, and the full prepared-population counts.
Completed pilots remain distinct from completion of the entire prepared dataset.
The original benchmark report appears separately when available.

`review.csv` is a blind worksheet for the actual selected items, created once a
selection exists. It omits model predictions. Existing annotations are preserved
when reports regenerate; expanding a run does not change an existing worksheet's
selection. Give each reviewer a separate copy and the fixed rubric/shared
context before showing predictions.

Enter 1–5 or `unknown` for each reviewed dimension. A blank score means
unreviewed. Provide a justification and supporting evidence for a numerical
score; Unknown requires a justification and missing-information explanation in
`<dimension>.information_gaps`. Additional gaps may accompany numerical scores.

```bash
python -m anthropic_api_package_release.item_analysis validate \
  --run-dir results/item_analysis/example \
  --review /path/to/independent-review.csv
```

Comparison reports exact agreement, Cohen's kappa where defined, confusion
counts, and mean absolute error separately for each dimension. Unknown
participates in exact agreement; numerical error uses paired numerical scores
only. Pending and failed model results are excluded and counted separately.
A saved comparison becomes visibly stale if its results, context, or review
file changes. Completion and agreement alone do not establish validity.

The website can export a ZIP containing the offline report, CSVs, shared context,
raw results, exact saved requests/responses, frozen prompts, available usage,
and a manifest of file checksums and missing artifacts. Original benchmark
scores/PDFs remain separate. The package preserves existing annotations and
also creates `review/blank_review.csv` without predictions or reviewer answers.
Partial packages clearly retain saved progress and outstanding work.

## Artifacts and compatibility

| Artifact | Purpose |
| --- | --- |
| `dataset.json`, `profile.json`, `items.jsonl` | Dataset provenance, deterministic facts, saved item order |
| `evidence.json`, optional `direct_context.json` | Original evidence and deployment requirements |
| `classifier_spec.json`, `specification.json` | Frozen shared source context, six-dimension rubric, hashes and preparation notes |
| `preview_requests.jsonl` | Exact scoring request previews without model calls |
| `run.json`, `results.jsonl`, `execution.json` | Frozen settings, append-only cumulative attempt history and assessments, actual selection/progress |
| `classification_requests.jsonl`, optional `requests.jsonl` | Exact core scoring requests and website request/usage records |
| `usage_ledger.json`, `usage_ledger.jsonl`, `usage.json` | Available call/usage records and token totals |
| `report.html`, `summary.json`, `items.csv` | Six-score reports and supporting evidence |
| `review.csv`, `review_selection.json`, `review_comparison.json` | Independent judgments, preserved selection, agreement |

New context uses `caliper_item_context_v1`; the fixed rubric is
`caliper_item_rubric_v1`; results use `caliper_item_result_v4`.
Historical four-classifier and earlier induced-classifier reports keep their
original labels and semantics. They are not reinterpreted as six scores. The
legacy `generate-spec` command remains available for existing categorical
workflows. New six-score runs should use a fresh directory; historical
specifications are never silently migrated.

`scoring.py` owns context assembly, the fixed six-dimension contract, scoring,
and continuation. `score_report.py` handles six-score reports and human review;
`report.py` dispatches by specification version while retaining historical
readers. `package.py` exports allowlisted artifacts. `prepare.py`, `data.py`,
and `storage.py` provide dataset/evidence snapshots, hashes, atomic writes,
and locks. `__main__.py` exposes the CLI.

Run offline tests:

```bash
python -m pytest anthropic_api_package_release/tests/test_item_analysis_*.py -q
```

Tests use local fixtures and injected model responses. They verify contracts,
state transitions, provenance, and compatibility; they do not establish the
accuracy of live model judgments.
