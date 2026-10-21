# Item-level validity analysis

This experiment inspects benchmark questions, references, and metadata against
sourced deployment requirements. It supplements an existing Caliper assessment;
Input Form and Output Form remain benchmark-level dimensions. No item judgments
are converted into the rubric's 1–5 scores or used to overwrite an assessment.

```text
Deployment/elicitation evidence + benchmark/domain documentation + dataset profile
  → model prepares sourced context for the code-owned classifier catalog
  → code validates references and joins context to the catalog
  → one model request per item judges all four classifiers
  → deterministic reporting and independent human review
```

The catalog is `caliper_generic_items_v1`, in `catalog.json`. Its questions,
decision rules, labels, and response contracts are fixed across benchmarks.
The context generator cannot change those rules or add classifiers.

| Classifier | Item-level judgment |
| --- | --- |
| Input Ontology | `match`, `no_match`, `insufficient_evidence`, plus a set of matched required-category IDs |
| Input Content | `issue_identified`, `no_issue_identified`, `insufficient_evidence` |
| Output Ontology | `issue_identified`, `no_issue_identified`, `insufficient_evidence` |
| Output Content | `issue_identified`, `no_issue_identified`, `insufficient_evidence` |

Input Ontology can match several categories. Deployment evidence establishes the
category inventory; benchmark examples do not establish deployment requirements.
An inventory is `complete` only with explicit supporting evidence. With a
`partial` or `unknown` inventory, failure to match a listed category does not
justify `no_match`; an explicit sourced deployment-scope exclusion is required.
Every ontology response includes `matched_category_ids` and
`scope_exclusion_source_ids` (empty arrays when appropriate).

The three issue classifiers require an applicable comparison standard and item
evidence. `no_issue_identified` is a bounded finding, not proof of validity or
stakeholder agreement. Missing information remains `insufficient_evidence`.
Operational errors are separate from all judgments. Output Ontology examines
semantic categories and scoring rules, including for multiple-choice items.

## Prepare one benchmark

Run commands from the repository root. Install dependencies if necessary:

```bash
python -m pip install -r anthropic_api_package_release/requirements.txt
```

Provide a local dataset and its pinned source revision when available:

```bash
python -m anthropic_api_package_release.item_analysis prepare \
  --assessment-dir anthropic_api_package_release/assessments/expert_1a429e941728__mmlu/india_hindi_competitive_exam_prep \
  --items /path/to/mmlu/items.parquet \
  --source-revision SOURCE_COMMIT \
  --source-table mmlu/items.parquet \
  --output-dir results/item_analysis/mmlu \
  --seed 42
```

Preparation snapshots the assessment artifacts, deployment statement, rubric,
and deterministic dataset profile. Its source registry retains actual contents
and exact source IDs, including the deployment statement and profile. Available
elicitation answers, benchmark taxonomy/scoring documentation, and domain or
stakeholder evidence are registered with source roles. Earlier assessment
findings belong in `prior_hypotheses`, not normative requirements. Missing
sources or comparison standards must remain explicit evidence gaps.

The adapter preserves content, reference answers, grading criteria, item
features, verifiers, and media references. Verifiers are never executed; an
asset path is not evidence that its image or audio content was inspected.
Missing references remain missing. The deterministic profiler records actual
columns, categorical values/counts, reference availability, and observed
format/media evidence. It does not infer unavailable data.

The saved item order is a seeded shuffle of the source population. A prefix is
therefore reproducible. Distinct IDs remain distinct observations even when
content is identical; duplicate IDs are rejected. Source checksums pin the
local snapshot, and unknown source revisions remain unknown.

## Prepare and inspect the contextual specification

Preview the complete request without API calls:

```bash
python -m anthropic_api_package_release.item_analysis generate-spec \
  --run-dir results/item_analysis/mmlu --dry-run
```

Generate context with the configured model (`OPENAI_API_KEY` is required):

```bash
python -m anthropic_api_package_release.item_analysis generate-spec \
  --run-dir results/item_analysis/mmlu
```

The readable system prompt and user-message template are in `prompts/`. The
request includes the original rubric, source registry, deterministic profile,
and actual example items. The generated JSON contains the required-category
inventory and four `context_by_classifier` entries, each separating deployment
requirements, benchmark evidence, prior hypotheses, and evidence gaps.

Code validates the exact benchmark/deployment text, catalog version, classifier
IDs, source references and permitted source roles, then joins the unchanged
catalog to context. The item judge receives the actual fixed rules and source
contents, not just a catalog version string. Structural/reference validation
is not semantic validation: inspect the extracted requirements, category
boundaries, completeness claims, and faithful use of evidence before relying
on results. Specifications retain `semantic_validation: "unreviewed"`.

A previously prepared generic context/specification can be supplied with
`generate-spec --spec /path/to/context.json`. Historical induced-classifier
specifications cannot start new runs; retain their original directories for
historical reporting. Imported context receives the same structural and source
checks. A structural failure receives at most one repair call; API failures
stop the command and preserve attempt details.

## Run the small experiment

Preview the first selected items and their exact classification requests:

```bash
python -m anthropic_api_package_release.item_analysis classify \
  --run-dir results/item_analysis/mmlu --dry-run --limit 100
```

Then classify the selected prefix:

```bash
python -m anthropic_api_package_release.item_analysis classify \
  --run-dir results/item_analysis/mmlu --limit 100
```

Each primary request covers all configured classifiers for one item. Responses
must contain fixed judgment labels, nonempty item evidence, explanations, and
consistent ontology category/source IDs. Invalid responses receive one repair
attempt, then become operational errors. API exceptions stop further calls;
successful results are flushed immediately, with raw attempts and token usage.

Repeat for each benchmark in a separate run directory. Workload totals are
computed from actual selected IDs, configured classifiers, and valid completed
results. Benchmark–classifier combinations are not request counts; repairs and
retries add requests. Reports retain selected-item counts separately from the
full prepared dataset.

Continuation is optional and requires unchanged inputs:

```bash
python -m anthropic_api_package_release.item_analysis classify \
  --run-dir results/item_analysis/mmlu --limit 100 --resume
```

A larger limit or `--all --resume` expands the experiment without repeating saved
completions. A changed catalog, context, prompt, source data, or execution
configuration requires a new run directory. Results cannot be resumed across
incompatible versions. Use one writer per directory; run locks reject concurrent
writers. An interrupted final append can be recovered; other corruption fails.
An interruption between receiving an API response and saving it can repeat that
call on resume.

## Reporting and human review

Classification refreshes reports automatically; rebuild them offline with:

```bash
python -m anthropic_api_package_release.item_analysis report \
  --run-dir results/item_analysis/mmlu
```

Reports and CSVs identify schema/catalog versions. Generic reports count each
fixed judgment, with `insufficient_evidence`, invalid responses, operational
errors, and pending items separately visible. Judgment percentages use all valid
judgments; any determinate-only percentage states its denominator. Category
counts allow overlapping matches. A required category not observed in selected
items is not established absent from the benchmark, and an incomplete inventory
cannot establish complete deployment coverage.

The new generic `review.csv` is a blind worksheet for the actual selected items.
It excludes model predictions and is created once after an actual experiment
selection exists; reports generated before classification defer the worksheet.
Existing human work is never overwritten. Its selection file records the IDs and purpose. If the experiment
later expands, the original review sample remains fixed. This worksheet is an
independent review sample, not an automatic prompt-tuning holdout.

For every reviewed classifier, enter its fixed label, item evidence, and an
explanation. Blank labels mean unreviewed; use `insufficient_evidence` for an
actual evidence-gap judgment. For Input Ontology, also enter a JSON array in
`input_ontology.matched_category_ids` (for example `["required_001"]` or `[]`).
A `no_match` judgment with a partial/unknown inventory requires deployment-scope
source IDs in `input_ontology.scope_exclusion_source_ids`. Reviewers should
consult the catalog and sourced context independently before viewing predictions.

```bash
python -m anthropic_api_package_release.item_analysis validate \
  --run-dir results/item_analysis/mmlu \
  --review results/item_analysis/mmlu/review.csv
```

Comparison reports per-classifier judgment agreement, Cohen's kappa where
defined, confusion counts, pooled overall judgment agreement, pooled agreement
including Input Ontology category sets, and exact agreement across
all classifiers for fully reviewed items. `insufficient_evidence` participates
as an explicit judgment. Input Ontology additionally reports exact category-set
agreement on paired determinate judgments, excluding pairs where either side
has insufficient evidence, and joint judgment/category agreement. Category-set
order does not matter. Model errors, missing results, and invalid judgments are
excluded from agreement and counted separately. Human evidence/explanations are
required for entered judgments.

Historical reports preserve their old numeric labels and legacy unknown/N/A
semantics under explicit legacy versions. They are not reinterpreted as generic
judgments. Human-review comparisons become visibly stale when predictions,
specifications, or review files change. Revalidate to refresh them. Neither full
item coverage nor high agreement alone establishes benchmark validity.

## Artifacts and maintenance

| Artifact | Purpose |
| --- | --- |
| `dataset.json`, `profile.json`, `items.jsonl` | Dataset provenance, deterministic facts, saved random order |
| `evidence.json` | Original assessment, deployment, and source registry |
| `generation_request.json`, `generation_attempts.json` | Exact context request and model/repair outputs |
| `classifier_spec.original.json`, `classifier_spec.json`, `specification.json` | Original context, joined catalog/context, frozen hashes and validation notes |
| `preview_requests.jsonl` | Exact classification requests without judgments |
| `run.json`, `results.jsonl`, `execution.json` | Frozen configuration, append-only versioned results, actual selection/progress |
| `usage_ledger.json`, `usage.json` | Actual calls and token totals |
| `report.html`, `summary.json`, `items.csv` | Versioned analysis and item evidence |
| `review.csv`, `review_selection.json`, `review_comparison.json` | Independent judgments, fixed review selection, agreement |

`catalog.py`/`catalog.json` own immutable generic rules. `schema.py` validates
context and current contracts; `legacy_schema.py` retains historical readers.
`prepare.py` and `data.py` snapshot source evidence and datasets. `generate.py`
prepares context; `classify.py` sends the combined rules/context to the judge.
`report.py` aggregates results and compares human review. `storage.py` provides
hashes, atomic JSON writes, and locks. `__main__.py` exposes the CLI.

Run offline tests from the repository root:

```bash
python -m pytest anthropic_api_package_release/tests/test_item_analysis_*.py -q
```

Tests use local fixtures and injected model responses. They check program
behavior and compatibility, not semantic faithfulness of generated context or
the accuracy of live model judgments.
