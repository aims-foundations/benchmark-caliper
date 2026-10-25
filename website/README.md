# Benchmark Caliper — Website

The website source provides two tools: **benchmark validity analysis** and **goal-conditioned item assessment**. Benchmark validity analysis is one continuous workflow: assess the benchmark documentation, then analyze its items using the same deployment context. This document describes the checkout; check the hosted service at <https://aimslab.stanford.edu/benchmark-caliper/> separately before assuming a change is deployed. See [SECURITY.md](SECURITY.md) for data and key handling.

## Routes

- `/` — selection between the two tools.
- `/caliper` — benchmark assessment with an Anthropic key, followed by required item analysis with an OpenAI key.
- `/caliper?start=items` — enter the item stage using an existing assessment or a new deployment context; no new benchmark assessment or Anthropic key required.
- `/caliper?start=items&mode=new` — direct item analysis from explicit deployment, task, and answer requirements.
- `/caliper?demo=mathdial` — free walkthrough of benchmark and item analysis.
- `/caliper?demo=mathdial&stage=items` — direct entry to the free item walkthrough.
- `/items` — the separate goal-conditioned item-review demo, using an OpenAI key.
- `/item-analysis` — compatibility entry into the main Caliper workflow; no standalone item-analysis chooser.
- `/run/{run_id}` — saved benchmark report with the same item-analysis continuation.

All routes work under the production `/benchmark-caliper` prefix.

## Start at item analysis

**Start at item analysis** is another starting point within Benchmark Caliper.
Users can select a gallery assessment or reopen a saved report and retain its
original deployment and findings. Links jump to the report's item stage; no
benchmark model calls are made to open the report.

For a new deployment, users supply the benchmark name, deployment context,
required tasks/topics, expected answers, and optional validity concerns. The
website searches the same Measurement Data Bank catalog and requires explicit
benchmark/snapshot confirmation, or confirmation of an uploaded CSV/JSON file.
Neither entering context nor searching/confirming requires a key or model call.
Preparing classifier context and classifying items require explicit actions and an
OpenAI key. The full-snapshot continuation also requires pilot review.

Direct criteria use the frozen user requirements, framework, deterministic
dataset profile, and actual sample items. No benchmark scores or elicitation
summary are invented. UI and exported artifacts identify the basis as
deployment requirements and the benchmark assessment as **Not run**. Input Form
and Output Form remain unassessed. Completing an item snapshot does not claim
a completed six-dimension benchmark assessment.

Direct context and run access are restored in the same browser tab, separately
from gallery/run-linked analyses and the free demo. Provider keys are never
stored by the item workflow. Editing the context starts fresh criteria and
requires dataset confirmation again; active model phases must finish or stop
first. The normal full pipeline and free walkthrough remain available.

## Free pipeline walkthrough

The homepage and Caliper screen offer **Try the free demo**. The MathDial
walkthrough replays the existing benchmark assessment, then continues through
mandatory sample confirmation, criterion review, a four-dialogue pilot,
a human-review checkpoint, and all ten bundled sample dialogues. No Anthropic
or OpenAI key is required, and the walkthrough makes no model calls or creates
server analysis jobs. The optional gallery listing remains a read-only request.
The intro also provides **Preview item analysis** for returning visitors.

The item sample contains the first ten complete dialogues from the public
`eth-nlped/mathdial` test split, pinned to a repository revision. Original source
records, source identifiers, attribution, license, and selection scope ship with
the fixture. Item criteria and judgments are authored walkthrough examples,
clearly distinguished from the prerecorded benchmark scores and source data.
Counts describe the ten-dialogue convenience sample, not all 599 test dialogues
or the full MathDial benchmark. Missing local-teacher acceptance evidence stays
unknown. This supplied sample does not claim to be a Data Bank search result.

The item-stage state is stored under a demo-only session-storage key. Refreshing
its demo URL restores the walkthrough without opening a paid gallery
continuation. Restarting the item demo requires confirming the sample again.
Downloads are generated locally and retain demo/source provenance. Opening an
ordinary gallery report or starting a new assessment uses the live pipeline.

## Item-level validity analysis

The benchmark report embeds the shared
[`item_analysis` pipeline](../anthropic_api_package_release/item_analysis/README.md)
as the next required stage, including reports opened from the gallery or a saved
`/run/{run_id}` link. The report remains marked as awaiting item analysis until
the full connected item snapshot is classified. This product requirement does
not authorize automatic paid calls: each model phase requires a user action.

1. Find and confirm the benchmark's items. Caliper searches the Measurement Data
   Bank using the paper identity saved with the assessment. Review the matching
   evidence, version, scope, item count, and source before explicitly confirming
   the benchmark and snapshot. Search for another candidate or upload its items
   as CSV or a JSON array of objects when needed. Uploads require confirmation too.
   Uploads accept 1–50,000 items and at most 10 MiB. Each item needs nonempty
   `content`; `item_id` is generated from its row number when omitted and must
   be unique when supplied. Include `reference_answer` when available.
2. Prepare sourced context for the four fixed rubric classifiers with GPT-6 Luna. The server carries
   forward the exact report's deployment description, scoring, elicitation
   summary, and available dataset evidence. Selecting a dataset does not select
   another deployment or reuse that source's supplied criteria. Review the
   decision rules, labels, and applicability before classification.
3. Classify the first 100 items with GPT-6 Luna (all items for smaller datasets),
   inspect the evidence, then explicitly continue through the full snapshot.
   Completed items are reused on continuation or retry.

The results show counts, percentages among known labels, unknowns, failures, and
pending items. Expand individual items to inspect justifications and evidence.
Download the specification, item CSV, summary JSON, HTML report, or blind human
review worksheet. The original six-dimensional assessment remains visible;
the demo does not turn item prevalence into new 1–5 scores. Criteria changes
require a new run. The website does not automatically revise criteria or import
completed human reviews; the CLI supports comparison with a completed worksheet.

An OpenAI key is required for generation and classification. Both steps use
`gpt-6-luna` with low reasoning effort; each run records this model configuration.
Opening the report and dataset setup makes no model calls. Preparing classifier context,
classifying the pilot, and continuing through the remaining items are separate
paid actions. The key stays in memory; the item run's ID and separate access
secret are kept in browser session storage, scoped to the source assessment.
Initialization failures identify dataset/evidence preparation, criteria
validation, provider access, or report preparation separately. The displayed
error reference contains a stage and fixed code; raw model replies and private
source text are not included. Validation permits one structural repair and does
not start item classification when the criteria are invalid.
Refresh restores the active run, but a later phase may require entering the key
again. Runs expire one hour after the last phase ends and do not survive a server
restart. Download outputs before they expire. Stop cancels the current awaited
request and prevents new calls; a request already submitted may still be billed.

### Assessment-continuation API

- `GET /api/item-analysis/assessment?kind=run&id={run_id}` (or `kind=gallery`)
  resolves the existing report, returns its context, extracted benchmark identity,
  suggested Data Bank sources, catalog status, and upload limits. It makes no
  model call. A run ID uses the existing report access model; gallery IDs must identify an allowlisted report.
- `GET /api/item-analysis/sources?kind=run&id={run_id}&q={query}` searches the
  catalog for another candidate while retaining the original assessment identity.
- `POST /api/item-analysis/runs/from-assessment` accepts multipart fields
  `assessment_kind` (`run` or `gallery`), `assessment_id`, and exactly one of
  `source_id` or `items_file`, plus explicit `benchmark_confirmed=true` and
  `X-OpenAI-Key`. Remote sources also require the displayed `source_revision`.
  It validates confirmation, the assessment, and source or upload before starting
  fresh context preparation. Clients cannot submit replacement assessment text
  or arbitrary source URLs. Stale revisions must be reviewed and confirmed again.
- Polling, classification, cancellation, and downloads use the existing item-run
  endpoints with `X-Review-Token`. Classification pauses at the 100-item review
  checkpoint before full-snapshot continuation.

The older `/api/item-analysis/catalog` and `POST /api/item-analysis/runs` prepared
example API remains available for compatibility and tests. It retains generated
or supplied criteria modes and the ten-item illustrative example. These presets
are not a separate homepage tool and do not replace the current report's context.

### Configure Data Bank access

Set the server's `HF_TOKEN` to a Hugging Face credential with read access to
`aims-foundations/measurement-db-pp` for merged and direct item analysis. The
browser never receives this credential.
Visitors supply only their OpenAI key for the item stage. Catalog search and
benchmark confirmation make no model calls and do not require an OpenAI key.

`server/item_analysis_databank_catalog.json` ships a metadata-only catalog for
fast initial search. `server/item_analysis_databank.py` discovers the Data Bank's
main branch, pins its commit, and refreshes the cached catalog in the background.
Discovery reads benchmark descriptors from `benchmarks.parquet` and optional
`metadata.yaml` files in `measurement-db-pp`, plus item-table metadata, without
downloading every item population. Discovery includes benchmarks regardless of
their release metadata, using the server's configured Hugging Face access.
Historical migration branches are not silently combined. Sources that exceed
the hosted reader's size or schema capabilities remain visible with an
explanation and an upload alternative.
The hosted reader currently accepts text/code item tables with at most 50,000
items, 32 MiB compressed data, and 96 MiB decoded Parquet data. These are full
snapshot limits; the server never silently samples down an oversized benchmark.

Matching uses canonical paper identifiers and dataset URLs, normalized names and
aliases, then fuzzy name matching. Match reasons and version/scope differences
are shown instead of numeric confidence claims. The deployment context never
participates in benchmark identity matching. Every proposed source requires
confirmation, including exact identifier matches; changing the candidate or
uploaded file clears that confirmation. A revision-bound source ID prevents a
catalog refresh from silently switching the selected snapshot.

Refresh the bundled catalog deliberately with:

```bash
python -m website.server.item_analysis_databank --refresh --output website/server/item_analysis_databank_catalog.json
```

The selected item table is downloaded only when context preparation is started,
then checked for integrity, expected row count, schema, and benchmark identity
before any model call. The complete supported snapshot is prepared; the first
100 items form the review checkpoint, not the population for the final report.
Repository, revision, table, and checksum remain recorded with the run. Raw
items are cached privately and are excluded from Git and the container image.
An access or validation failure never substitutes another benchmark.

The older prepared-example API retains `server/item_analysis_sources.json`,
its pinned MMLU/TOXIGEN sources in `measurement-db-pp`, public GSM8K/HumanEval
sources, and the illustrative example. `ITEM_ANALYSIS_PREPARED_DIR` applies only
to that legacy API. These sources and historical assessment contexts do not
replace Data Bank discovery or the current report's context in the merged flow.

Implementation: `server/item_analysis_assessment.py` resolves existing reports,
extracts paper identity, validates uploads, and freezes the original context;
`server/item_analysis_databank.py` owns discovery, matching, and selected-source
validation; `server/item_analysis.py` owns jobs, access control, and the async
OpenAI bridge. `client/src/itemAnalysis/` owns the stage embedded by
`client/src/components/ScoringView.tsx`. Preparation, the OpenAI client,
specification validation, classification, aggregation, and exports reuse
`anthropic_api_package_release/item_analysis/`. The separate `bayesian_auditing`
review workflow keeps its own sample and catalog.

## Goal-conditioned item review

The six-answer form also offers **Extract requirements**, an independent paid
GPT-6 Luna request implementing Step 2 of *Goal-Conditioned Adaptive Composite
Benchmarks*. It shows the extracted deployment summary, task facets, essential
status, supporting quotations, explicit collection coverage requirements, and
unresolved details beside the original answers. This action works without dataset
access and stops at the preview; it does not run retrieval or item assessments.

The action uses `POST /api/item-review/runs` with
`{"mode": "requirements", "deployment": {"task": "...", "users": "...", "inputs": "...", "outputs": "...", "success": "...", "constraints": ""}}`.
It shares the existing run-secret polling, cancellation, expiry, and export
endpoints. Its export contains the original answers, validated requirements,
prompt/schema, model/settings, and available usage. Invalid extraction produces a
failed run without accepted requirements or downstream calls. Source-quotation
checks establish traceability; human review still assesses the interpretation.
The schema and prompt live in `bayesian_auditing/requirements.py` and
`bayesian_auditing/prompts/extract_requirements.md`.

The requirements preview offers **Ground with O*NET**. It searches the supplied
local healthcare catalog using BGE embeddings and BM25, then asks GPT-6 Luna to
map shortlisted records to each existing task. The preview shows adopted record
IDs, exact supporting passages, applicability, rationale, search vocabulary,
goal-supported refinements, and unresolved details. Retrieved rankings and
rejected mappings are expandable. Original requirements remain unchanged, and a
task may have no applicable O*NET record. This stage stops before benchmark-item
retrieval or assessment.

`POST /api/item-review/runs/{run_id}/ground` takes `X-Review-Token` for a finished
requirements or grounding run and a fresh `X-OpenAI-Key`. It creates a separate
`mode: "grounding"` run without repeating extraction. The key stays in memory
only. Polling, cancellation, JSON export, and expiry use the existing endpoints;
completed mappings survive cancellation or later failures. The export includes
the original extraction, candidates/ranks, mapping evidence, prompts, settings,
reference-file checksums, and grounding token usage. A failed or stopped mapping
can be retried as a new run, which maps all facets again.

The default reference directory is the repository's `materials/`; override it
with `ITEM_REVIEW_ONET_DIR`. Keep `ONET_index.csv` and `ONET_embeddings.npz`
together and restart the server after replacing them. The retrieval dependencies
are included by `website/server/requirements.txt`. The first local search loads
the pinned `BAAI/bge-small-en-v1.5` model (downloading it if needed) and verifies
sampled vectors against the supplied index. Dataset authorization is not needed
for extraction or O*NET grounding. See
[`bayesian_auditing/README.md`](../bayesian_auditing/README.md) for the exact search
settings, data scope, mapping contract, and source attribution.

A completed O*NET grounding preview now offers **Retrieve benchmark items**
(Step 4). This searches the whole Measurement Data Bank at a pinned `main`
commit: every row from every discovered `items.parquet` table, including every
benchmark collection and release. There are no collection or release filters.
The preview displays the complete bank's collection and source-row counts.
The first index build can be expensive: the server reads the whole bank,
computes BGE vectors locally, and stores the index on disk. Later searches reuse
the completed cache for that pinned inventory. Dataset access and the existing
BGE retrieval dependencies are required; this action needs no OpenAI key and
makes no paid model calls.

For each extracted task, a deterministic query combines its required behavior,
deployment context, adopted O*NET vocabulary, and goal-supported refinements.
Local BGE and SQLite FTS5 BM25 each return up to 600 items. Reciprocal-rank fusion
retains their complete union, up to 1,200 distinct candidates per task. Every
source-row field is preserved in `evidence.item` and serialized into
`search_text`, including identifiers, questions, answers, grading criteria, and
other source columns. Both searches use this complete row text. BGE encodes all
nonoverlapping token chunks and combines their normalized CLS vectors into one
normalized mean vector; BM25 indexes the full text. Only identical complete
rows are deduplicated, including their identifiers, while preserving every
source reference. The preview shows the exact queries, ranks, supporting O*NET
IDs, complete searchable text, original row evidence, and provenance. A separate
question field is optional and used only as a convenient display preview.
These candidates are not validity assessments or final benchmark selections.

Each task has a fixed all-source queue and per-collection queues that preserve
the same retrieval order. Browse candidates by task and collection, or download
the complete retrieval JSON. The export contains the original answers,
requirements and grounding snapshots, pinned scope, retrieval settings, queries,
candidates, and queue memberships. Stopping a run preserves completed task
results. The next screening/adaptive-selection stages are not invoked.

`POST /api/item-review/runs/{run_id}/retrieve` accepts an empty JSON object `{}`
and requires only the source run's `X-Review-Token`. Scope overrides such as
`benchmarks` are rejected. It creates a separate `mode: "retrieval"` run.
Polling returns a compact summary;
`GET /api/item-review/runs/{run_id}/candidates?queue_id=...&page=1` returns
20 candidates per display page, and the existing export route returns the full
retrieval artifact. The existing run-token authorization, cancellation, and
temporary expiry policy apply.

Completed indexes live under `WEBSITE_DATA_DIR/benchmark-retrieval-index/`,
keyed by the complete pinned main-branch inventory and loader/encoding policy.
Failed or cancelled builds never become reusable caches; a retry starts that
build again.
The cache contains dataset evidence and document vectors, but no deployment
answers or query vectors. SQLite FTS5 and bounded embedding/vector-scan batches
keep the full corpus off the Python heap. Budget for substantial disk and local
inference time for the complete bank. Full-bank performance and retrieval
quality have not been measured end to end.

The existing **Review catalog** assessment option collects six deployment answers, retrieves relevant questions
locally, and uses the visitor's OpenAI key to assess only the selected shortlist.
It defaults to 20 retrieved items, with a maximum of 100 per web review. A
reference question can guide retrieval; otherwise it uses the deployment answers.
Retrieval uses `Qwen/Qwen3-Embedding-0.6B` on local hardware with question-only
inputs, 8,192-token truncation, unit-normalized vectors and dot-product ranking.
Exact question matches appear first. The pinned model/policy and source revisions
are recorded with the results.

This retrieval-augmented assessment makes no paid embedding API calls. GPT-6 Luna
still performs the existing six validity judgments, using full item evidence and
the deployment description. Its high reasoning effort and 25,000-token ceiling
are unchanged. Retrieval similarity and order stay separate from final validity
scores, per-dimension confidence, evidence, information gaps, and provenance.
Similarity identifies candidates; it does not establish compatibility. The initial
deployment questions are fixed and editable, without an extra model call.

The first five deployment answers must contain non-whitespace text; constraints
is optional. There are no minimum or maximum answer-length limits. Submitted
answers remain fixed for each run and are included verbatim in its JSON export.
Submitting revised answers creates a separate run.

Scoring version 5 ranks items by a confidence-adjusted score. Each scored
dimension contributes `1 + confidence * (compatibility - 1)`, and missing
dimensions contribute 1 to ranking only; the result averages all six contributions.
This discounts uncertain positive support without raising low scores or dropping
potential weaknesses from the average. The UI also shows the original mean of
available compatibility scores, excluding missing dimensions.
The model directly reports numerical confidence from 0 to 1 for each
scored dimension, with a rationale. Confidence describes how strongly the
supplied evidence supports that score, based on relevance, completeness,
consistency, and remaining uncertainty. The prompt asks for evidence, specific
information gaps, and material assumptions first, without referring to an
independent reviewer. Confidence is displayed directly. A dimension with no
defensible score keeps null score and confidence; the ranking floor is not an
imputed compatibility score.
The evidence-gap flag uses missing scores or listed gaps, not a confidence cutoff.
Partial assessments remain ranked with coverage shown (for example, 5/6), and
items with no scores remain available without a rank. Compare coverage when
interpreting the compatibility mean. Confidence describes evidence support and
is not a calibrated probability; the adjustment is a conservative ranking
heuristic, not a statistical lower bound. See the
[scoring policy](../bayesian_auditing/README.md#process-and-scoring) for details.
The JSON download includes the policy, confidence explanations, and separate
`ranked_items`, `unranked_items`, and `failed_items` lists. `complete` counts all
valid assessments; `ranked` and `unranked` distinguish score availability.
Existing version-2 and version-3 reports retain their categorical confidence
labels and scoring explanations. Version-4 reports retain their numerical
confidence and unadjusted ranking. Version-1
reports have no recorded confidence and require a new review to obtain it.

The catalog includes every available formatted `items.parquet` table from
measurement-db's `main` branch, pinned to
`54074453da7b9911be0f48e4c560be547bc84d21`. The current snapshot has **281 benchmark
collections, 281 tables, and 8,471,422 source rows**, without a release filter.
The inventory refresh reads table metadata; the complete Step 4 retrieval index
has not yet been built or searched end to end.
The existing Qwen assessment demo selects up to **50 distinct items per benchmark collection**, for at most
**13,602 selected items** in this snapshot. A fixed seed makes selection independent
of row order and deployment description. Duplicate evidence gets one selection
opportunity, and all provenance is retained. Retrieval
searches only the selected sample; validity rankings describe the retrieved and
assessed shortlist, not all sample items or the full catalog. The text judge does
not inspect referenced media assets.
The mathematics tutor is an optional form example, not a restriction on deployment.

The gated dataset requires Hugging Face access. Configure an authorized
`HF_TOKEN` or Hub login on the server. Dataset access is managed by the server;
visitors supply only their OpenAI API key. If the server credential is missing,
the UI disables new reviews and asks visitors to contact the site maintainer.
The server never uses its own OpenAI key: each review requires the user's key.

`server/item_review.py` prepares the complete sample and retrieves a shortlist
before making paid calls, then assesses up to four shortlisted items concurrently.
Set `ITEM_REVIEW_CONCURRENCY` (1–16, default 4) to tune the judge worker limit;
1 restores sequential assessment. A fixed worker pool bounds in-flight requests,
deduplicates evidence before calls, and cancels workers on stop or provider failure
while retaining completed judgments. The first preparation
scans all source rows without model calls, using a temporary SQLite index of hashes
and source locations, keeping only the best 50 selection candidates in memory.
Additional branch representatives are fetched through Parquet HTTP ranges if
needed. `bayesian_auditing/sampling.py` caches selected dataset evidence under
`WEBSITE_DATA_DIR/item-review-samples/`, keyed by pinned inventory, seed, sample
size, and loader/sampling versions. Later reviews reuse that sample. Question
vectors are cached separately under
`WEBSITE_DATA_DIR/item-review-embeddings/`; query vectors are not written to this
reusable cache. Qwen model files use the standard Hugging Face cache. First-time
model download and embedding can take substantial time, memory, and disk. The cache
contains no deployment answers or provider keys. Source metadata may also be cached.
`server/item_review_store.py` stores assessments, evidence, and source references
in a private temporary SQLite file, with indexes for deduplication and ranking.
The deployment answers and OpenAI key remain in process memory. Raw provider
responses are not retained. Retrieval holds the selected records and vectors in
memory; provision enough RAM for this index and the local Qwen runtime.

The browser polls 20 results at a time; these are display pages, not shortlist limits.
The authenticated `/api/item-review/runs/{id}/export` route streams every assessment
available when the download begins. A read failure stops preparation or assessment
and preserves completed results; it does not silently skip a table or claim a
complete sample. Exports include retrieval and sampling policies, separate
indexed, retrieved, and assessed counts, and pinned source revisions. Completion means the retrieved
shortlist was processed, not that the entire sample was judged.
Three reviews can run simultaneously, one per OpenAI key. Up to 30 jobs are retained.
Completed/failed/cancelled jobs and their result files expire after one hour
(checked each minute). A normal shutdown cancels jobs and deletes these files.
An abrupt process kill can leave orphaned temporary files until the host cleans
them up. The demo does not resume after server restarts; the [CLI](../bayesian_auditing/README.md)
supports durable resume. Refreshing the same browser tab resumes polling a live
job. Cancelling prevents further model calls; requests already sent may be billed.

The router and UI live in `server/item_review.py` and `client/src/itemReview/`;
`client/src/EvaluationSite.tsx` chooses the workflow. The catalog inventory is
`server/item_review_inventory.json`. To refresh it deliberately, run:

```bash
python -m website.server.item_review_catalog
```

The refresh command discovers all item tables on `main` and reads Parquet footers to validate
the required columns and record source-row counts. It saves only paths, revisions,
and counts after all tables are inspected successfully. No item content or
credentials are committed. Prepare the reusable sample without an OpenAI key with:

```bash
python -m website.server.item_review_sample --build-index
```

Omit `--build-index` to prepare only the sample. With it, preparation also caches
Qwen question vectors, without making paid calls. Preparation can take time on a
cold cache. The caches are private to the server, can be regenerated, and survive
normal shutdown. Temporary assessment files still expire after each review. Completion depends on provider quota, disk space, and
the server staying alive.

The sampling implementation is `bayesian_auditing/sampling.py`. It combines each
collection's branches, deduplicates by the existing evidence fingerprint, and
assigns each distinct input a SHA-256 priority derived from seed `20260925`, the
collection name, and its fingerprint. It reserves one randomly chosen exclusive
item per branch when available (otherwise a shared item), then fills to 50 by
priority. Small collections contribute every distinct item. This balances
collection coverage for the demo; it is not a sample proportional to catalog size
or deployment workload. Source order and duplicate frequency do not affect selection.
Changing a pinned revision or the sampling policy creates a new cache entry;
changing deployment answers reuses the sampled evidence and question vectors,
retrieves a new shortlist, and makes new judgments. Similarity, truncation, and
shortlist limits can omit relevant items. Evaluate retrieval recall separately
from judge quality.

---

## What it does

A user pastes their Anthropic API key, uploads a benchmark paper PDF, and describes a deployment context. The site walks them through:

1. **Slug** — derive a short identifier (Haiku)
2. **Metadata** — extract benchmark metadata from pages 1–2 (Haiku)
3. **Elicitation questions** — generate 3–5 deployment-context questions (Sonnet)
4. **User answers** the questions in the browser
5. **Elicitation summary** — synthesize a structured summary (Sonnet)
6. **Run mode** — user chooses automatic benchmark processing (default) or step-by-step review. The current browser UI does not collect a report-notification email address.
7. **Paper extraction** — per-page parallel Haiku fan-out + Sonnet consolidation
8. **Benchmark YAML** — Haiku picks ICL examples, Sonnet writes a per-paper YAML
9. **Region YAML** — Haiku picks templates, Sonnet writes a regional scaffold, Sonnet+web search enriches it
10. **Validity scoring** — single Opus call across the 6 dimensions
11. **Benchmark report** — the six-dimension report is displayed with downloads and the required item-analysis stage below it. Saved `/run/{run_id}` reports offer the same continuation. Optional notification endpoints remain available to compatible clients when email delivery is configured.
12. **Item analysis** — connect matching benchmark items, prepare and review sourced classifier context, classify the first 100 items, inspect the pilot, then continue through the full snapshot. These explicit paid actions use a separately supplied OpenAI key.

The complete output combines the six-dimension validity report with item-level
judgments, prevalence summaries, and exportable evidence. Item prevalence does
not change the original benchmark scores.

Benchmark-stage cost depends on paper length, model usage, and web search.
Item context preparation and classification incur separate OpenAI charges;
classification volume depends on the connected dataset's size.

---

## Running it locally

Requirements: Python 3.11+, Node 24+, and the API key for the selected workflow.
Goal-conditioned review also downloads a local Qwen embedding model and needs
sufficient RAM and disk for its weights, runtime, sample, and vector cache. See
[deployment sizing](DEPLOYMENT.md#item-review-configuration) before hosting it.

```bash
# Terminal 1 — backend (run from the repository root)
python3 -m venv .venv && source .venv/bin/activate
pip install -r website/server/requirements.txt
python3 -m uvicorn website.server.app:app --reload --port 8000

# Terminal 2 — frontend
cd website/client
npm install
npm run dev
```

Open <http://localhost:5173>. Vite proxies `/api/*` to <http://localhost:8000>.

> The backend uses package-relative imports, so it must be run as `website.server.app:app` from the **repository root** — not `app:app` from inside `website/server/`.

### Free local dev (no Anthropic spend)

For the benchmark-assessment stage of `/caliper`, UI work and click-through testing without paying for API calls can use `MOCK_ANTHROPIC=1`. Every `call_text_async()` short-circuits to canned fixtures pulled from one already-paid assessment under `anthropic_api_package_release/assessments/`. Paste any string (e.g. `sk-ant-FAKE`) into the API-key field — the value is ignored. This flag does not mock the subsequent OpenAI item-analysis stage. Inspect its setup without starting a model phase, or use offline tests for the complete workflow.

```bash
MOCK_ANTHROPIC=1 python3 -m uvicorn website.server.app:app --reload --port 8000
```

The server prints a loud `⚠️  MOCK_ANTHROPIC=1` banner on startup and refuses to boot if any production signal is set (`ENV=production`, non-localhost `WEBSITE_ALLOWED_ORIGINS`). Override the fixture source with `MOCK_ANTHROPIC_FIXTURE=/abs/path/to/<expert>__<benchmark>/<slug>`. **Never set `MOCK_ANTHROPIC` in production** — leaving the variable unset (the default) is real mode. See [server/mock_anthropic.py](server/mock_anthropic.py).

---

## Testing

```bash
# backend (run from the repository root)
python3 -m pytest website/server/tests/

# frontend
cd website/client
npm test
```

Run the shared retrieval and item judge tests with `python -m pytest bayesian_auditing/tests/`.
Backend tests mock provider calls, including success, failures, cancellation,
credential handling, retention, and per-run access control. Frontend tests cover
both routing and the guided item-review flow.

The item-analysis tests exercise generated and supplied criteria, checkpoint
continuation, cancellation, exports, and authentication without paid model calls:

```bash
python -m pytest website/server/tests/test_item_analysis*.py anthropic_api_package_release/tests/test_item_analysis_*.py
cd website/client
npm test -- src/itemAnalysis src/EvaluationSite.test.tsx
```

---

## Deployment

The site deploys as a single Docker service on Render. See [DEPLOYMENT.md](DEPLOYMENT.md) for the one-service setup and the AIMS proxy.

---

## AIMS theme and navigation sync

The client is styled to match the AIMS redesign (`web/app/redesign.css` in
`aims-foundations/aimslab`): warm `#f3efec` bands, light-weight Google Sans
Flex display type, cardinal accents, mono pill buttons, flat 1px-rule cards.
Fonts are self-hosted (Roboto Mono via `@fontsource`, Google Sans Flex
vendored in `client/src/fonts/`) so the strict CSP needs no third-party
origins.

The header's nav items are **not** hard-coded: the main site publishes its
`primaryNavigation` at `https://aimslab.stanford.edu/nav.json` for exactly
this purpose, and `SiteHeader.tsx` fetches it at runtime (same-origin under
the proxy). When the main site's nav changes, this app's header follows
automatically — the `NAV_FALLBACK` snapshot in `SiteHeader.tsx` only covers
first paint, local dev, and direct-origin access, so refreshing it is nice to
have, not required. The footer is a static port of the main site's `RdFooter`
plus the in-app privacy-notice link required by [SECURITY.md](SECURITY.md).

---

## Layout

```
website/
├── DESIGN.md              # Narrative architecture and security posture
├── SECURITY.md            # Verifiable security checklist
├── DEPLOYMENT.md          # Hosted setup
├── README.md              # This file
├── server/                # FastAPI backend
│   ├── app.py             # All HTTP endpoints
│   ├── logging_gate.py    # The privacy chokepoint
│   ├── retention.py       # 90-day cron
│   ├── pipeline_assets.py # Reads ICL YAMLs from anthropic_api_package_release/
│   ├── anthropic_client.py
│   ├── pdf_utils.py
│   ├── elicitation.py
│   ├── quote_registry.py
│   ├── prices.py
│   ├── sse.py
│   ├── db.py
│   ├── requirements.txt
│   └── tests/             # 130 backend tests
└── client/                # Vite + React + TypeScript
    ├── src/
    │   ├── App.tsx
    │   ├── api.ts
    │   ├── consentStorage.ts
    │   ├── keyStorage.ts
    │   └── components/    # Per-phase views
    └── (vitest tests, 46 of them)
```

---

## License

TBD.


Item-analysis catalog and result contracts now use `caliper_generic_items_v1`
and `caliper_item_spec_v2`. The judge receives the catalog's actual fixed rules,
sourced context, category inventory, and source registry on every item request.
Input Ontology records a judgment plus multiple matched required-category IDs;
Input Content, Output Ontology, and Output Content use `issue_identified`,
`no_issue_identified`, and `insufficient_evidence`. Multiple-choice items retain
Output Ontology. Input Form and Output Form remain benchmark-level dimensions.

The website displays source contents, prior hypotheses, inventory completeness,
and evidence gaps for review. Prepared context is semantically unreviewed even
when structure and source references pass validation. Distribution percentages
include all valid judgments, including insufficient evidence; operational errors
and pending items remain separate. Counts come from selected items and saved
judgments, with one primary request per item covering every classifier.

Historical induced specifications retain explicit legacy schema/catalog markers
and their original label meanings. The old MMLU supplied specification is retained
as a historical artifact, but is unavailable for new runs. The bundled exam demo
and free MathDial walkthrough use the fixed generic catalog. The walkthrough's
judgments are authored illustrations with explicit evidence gaps, not a study.
Its catalog copy is checked against the Python catalog by the server tests.
