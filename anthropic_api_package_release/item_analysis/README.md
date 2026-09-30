# Item-level validity analysis

This module measures how often specific validity properties appear in one
benchmark for an existing Caliper deployment assessment. It runs after stage 7:

```text
scoring.json + deployment + dataset profile + dataset-analysis findings
  → Sonnet generates a classifier specification
  → Haiku labels each item using the frozen specification
  → Python counts labels and exports an HTML report and item-level CSV
```

The five classifier slots cover Input/Output Ontology and Content. Input Form
and Output Form retain their original benchmark-level assessments. This module
does not produce six new item-level 1–5 scores or convert prevalence into new
benchmark scores. It is independent of `bayesian_auditing` and does not change
the original assessment or require rerunning stages 0–7.

## Prepare one benchmark

Run all commands **from the repository root**, using the full module name shown
below. Install the pipeline dependencies if needed:

```bash
python -m pip install -r anthropic_api_package_release/requirements.txt
```

Obtain a local `items.parquet` from a pinned measurement-db revision using your
authorized Hugging Face access. Provide the source revision and repository table
path when the file is outside the Hub snapshot cache:

```bash
python -m anthropic_api_package_release.item_analysis prepare \
  --assessment-dir anthropic_api_package_release/assessments/expert_1a429e941728__mmlu/india_hindi_competitive_exam_prep \
  --items /path/to/mmlu/items.parquet \
  --source-revision SOURCE_COMMIT \
  --source-table mmlu/items.parquet \
  --output-dir results/item_analysis/mmlu \
  --seed 42
```

`prepare` requires `scoring.json`, `deployment_description.txt`,
`elicitation_summary.md`, and `dataset_analysis_report.md` in the assessment
directory. It snapshots those inputs and the framework. The Parquet reader
preserves full content, answers/grading criteria, item features, verifiers, and
asset references. Verifiers are never executed; media references are retained
but their contents are not loaded. Missing answers stay missing.

The profiler records actual columns/types, all observed categorical item-feature
values and counts, reference availability, and observed format/media evidence.
It does not enumerate the values of free-text questions. The entire source
population is shuffled once with the saved seed. The first 100 prepared items
are therefore a reproducible random sample, not the first 100 source rows.
Different item IDs remain separate observations even when content is identical.
Duplicate item IDs and contradictory named benchmark identities are rejected.

Source files are checksummed; HF cache paths also supply the original revision
and table path. Opaque benchmark IDs are recorded as unverified. A cached snapshot
can be used even when no longer downloadable, but results describe **that exact
snapshot**, not a current release or the full dataset described in a paper.
If a source revision is unknown, the manifest says so; the checksum still pins
the local file. Do not assign a guessed revision.

## Generate or import the specification

Preview the full Sonnet request without API calls:

```bash
python -m anthropic_api_package_release.item_analysis generate-spec \
  --run-dir results/item_analysis/mmlu --dry-run
```

Then generate it with Sonnet. Live generation and classification require
`ANTHROPIC_API_KEY` in the environment (or a local `.env`):

```bash
python -m anthropic_api_package_release.item_analysis generate-spec \
  --run-dir results/item_analysis/mmlu
```

The generator receives the fixed roster/schema, full deterministic profile,
source registry, deployment requirements, stage-7 findings, and eight actual
items. It must preserve deployment text, cite existing source IDs, and write
positive/negative/unknown decision rules. Stage-7 findings are hypotheses to
test, not conclusions each item must reproduce. New category labels must be
grounded in deployment requirements; the classifier slots remain fixed.
Structural validation failures receive at most one repair call. API failures
stop the command and preserve attempt details. Code replaces any generated
profile with the authoritative profile and records that adjustment.

For the demo, importing the supplied pilot JSON is an alternative entry path:

```bash
python -m anthropic_api_package_release.item_analysis generate-spec \
  --run-dir results/item_analysis/mmlu \
  --spec mmlu_classifier_spec.json
```

Choose either generation or import for one run directory. The original JSON is
preserved next to the effective specification. Imported free-text citations and
deployment paraphrases require human review; both original and specification
deployments appear in the report. The first implementation uses Haiku for every
applicable classifier; legacy `data_then_haiku`/valid `data_column` hints are
normalized to `haiku` with an explicit adjustment record.

The fixed-MCQ rule follows `SPEC.md`: when every item has explicit choices,
`OO.output_category` is N/A because answer representation is uniform. This
differs from the supplied pilot's semantic-answer interpretation. The gate and
reason are recorded; `OO.value_encoding` still assesses output conventions.
N/A means a classifier does not apply; `null` means an individual judgment lacks
evidence. Those states are never counted as negative labels.

## Inspect 100 items, then complete every item

First save the exact Haiku requests without scoring:

```bash
python -m anthropic_api_package_release.item_analysis classify \
  --run-dir results/item_analysis/mmlu --dry-run --limit 100
```

Run the initial review checkpoint:

```bash
python -m anthropic_api_package_release.item_analysis classify \
  --run-dir results/item_analysis/mmlu --limit 100
```

One request per item applies all applicable classifiers. Responses must contain
the specified labels, evidence, and a justification. An invalid response gets
one structural repair attempt, then becomes an error. Errors are never validity
judgments. API exceptions stop the run instead of repeatedly consuming calls
after an authentication, quota, or service failure. Successful results are
flushed immediately; model usage and raw call traces are saved.

Inspect `report.html` and `items.csv`. **The program does not rewrite its own
criteria after inspecting these results.** If the instructions or data adapter
need changing, prepare a new directory and rerun the checkpoint. If the criteria
are suitable, continue with unchanged settings:

```bash
python -m anthropic_api_package_release.item_analysis classify \
  --run-dir results/item_analysis/mmlu --all --resume
```

This scores all remaining items and retries previous errors without repeating
completed items. The default `--limit 100` is the review checkpoint; `--all` is
the full-benchmark demo target. Only the limit can grow during continuation:
changed data, assessment, criteria, prompt, model ID, or token settings require
a new run directory. Use one process per directory; concurrent writers are
rejected. A truncated final JSONL append is recoverable; other corruption fails.
An interruption after an API response but before saving can repeat that call.

The run is sequential. Use the checkpoint's actual elapsed time and recorded
token usage to estimate a full run. The shared client's monetary estimates use
its configured pricing table; token counts and call traces are the primary
usage record.

## Report and human review

Classification automatically refreshes the report. It can also be rebuilt
offline, including before any model labels exist:

```bash
python -m anthropic_api_package_release.item_analysis report \
  --run-dir results/item_analysis/mmlu
```

The report keeps known labels, unknown judgments, invalid results, failed calls,
and pending items separate. Percentages use known valid labels as denominator;
the denominator and missingness are explicit. Counts are model classifications,
not established regional stakeholder judgments. A full run removes sampling
uncertainty for that snapshot, but classification error still requires review.
Overlapping flags are never summed as independent problematic items. Required
categories with no classified items are reported as **not observed**, not proof
that the original benchmark lacks the category.

`review.csv` is a blind worksheet containing the next 50 items after the initial
100 (or a clearly marked debugging sample for datasets of at most 100 items).
It is created once and never overwritten. Enter independent labels using the
specification; leave unreviewed cells empty and use `unknown` for insufficient
evidence. The file intentionally excludes model predictions. Review should be
done by someone qualified for the deployment, particularly for label
contestability. Keep the held-out review separate from prompt tuning.

```bash
python -m anthropic_api_package_release.item_analysis validate \
  --run-dir results/item_analysis/mmlu \
  --review results/item_analysis/mmlu/review.csv
```

This exports per-classifier agreement, Cohen's kappa where defined, confusion
counts, and human/model-unknown counts. It does not treat unknown human labels
as ground truth or agreement. A small reviewed subset is preliminary evidence,
not proof of validity. Revalidate when model results or review labels change.

## Artifacts and maintenance

| Artifact | Purpose |
| --- | --- |
| `dataset.json`, `profile.json`, `items.jsonl` | Source provenance, full-table facts, saved random item order |
| `evidence.json` | Original assessment, deployment, and source registry |
| `generation_request.json`, `generation_attempts.json` | Exact generation inputs and model/repair outputs |
| `classifier_spec.original.json`, `classifier_spec.json`, `specification.json` | Original/effective criteria, adjustments, hashes, and review notes |
| `preview_requests.jsonl` | Exact classification requests; previews contain no labels |
| `run.json`, `results.jsonl`, `execution.json` | Frozen settings, append-only results, progress/errors |
| `traces/`, `usage_ledger.json`, `usage.json` | API call traces and accumulated usage |
| `report.html`, `summary.json`, `items.csv` | Human and machine-readable analysis |
| `review.csv`, `review_selection.json`, `review_comparison.json` | Independent review and agreement |

`data.py` owns source normalization/profiling. `prepare.py` snapshots the original
assessment. `schema.py` owns the fixed roster and contracts. `generate.py` and
`classify.py` own the two model stages; their readable prompts are in `prompts/`.
`report.py` performs deterministic aggregation and review comparison.
`storage.py` provides hashes, atomic JSON writes, and the run lock. The CLI is
in `__main__.py`. Model calls reuse the pipeline's existing `client.py`.

Run the offline tests from the repository root:

```bash
python -m pytest anthropic_api_package_release/tests/test_item_analysis_*.py -q
```

Tests use local Parquet fixtures and injected model responses. They cover
generation/repair, imported specifications, evidence preservation, label
validation, random sampling, 100-to-all continuation, failures, unknowns,
reporting, human review, and frozen-run integrity. They establish program
behavior, not the quality of live Sonnet or Haiku judgments.
