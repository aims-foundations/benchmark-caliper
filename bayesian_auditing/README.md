# Goal-conditioned item review

## Step 2: extract deployment requirements

The website's **Extract requirements** action implements Step 2 of *Goal-Conditioned
Adaptive Composite Benchmarks* (§1.1 and §2.2). It sends the six original answers
to GPT-6 Luna in one structured extraction request and stops at a reviewable
requirements preview. It does not load the item bank, retrieve items, or assess
their compatibility. No Hugging Face access is needed for this action.

[`requirements.py`](requirements.py) defines the output and validates references;
[`extract_requirements.md`](prompts/extract_requirements.md) is the complete prompt.
The output contains the workflow, primary user, input/output types, authority,
task facets, explicit collection coverage requirements, and unresolved details.
Each known text field includes its supporting answer identifiers and verbatim
quotations. Unknown text stays `null` with no fabricated evidence. Facets retain
required inputs, required output behavior, and essential status; an ambiguous
essential status stays `null`.

Source identifiers match the existing form: `task`, `users`, `inputs`, `outputs`,
`success`, and `constraints` correspond to the paper's answers 1–6. Pydantic
validates the structure, unique facet identifiers, and coverage references;
Python checks each quotation against its named original answer. These checks
establish literal provenance, not semantic correctness. Review the interpretation
alongside the original answers.

Collection targets are separate from individual response requirements. For
example, the [paper's medical study goal](examples/medical_study_goal.json) asks
for at least three medication-constrained management cases; this becomes a
coverage requirement linked to `initial_management` with `minimum_items: 3`.
Other explicit quota forms are preserved as supported text with a null minimum
and an unresolved enforcement detail. No default quotas are invented.

`RequirementExtractor` and `AsyncRequirementExtractor` reuse the existing OpenAI
Responses settings (GPT-6 Luna, high reasoning effort, 25,000 maximum output
tokens, `store=False`). Incomplete responses, refusals, invalid schemas, and
invalid quotations produce an error with no accepted requirements. Invalid output
is not automatically re-prompted; the website retains the SDK's existing two
transport retries. Provider errors are sanitized and cancellation is supported.

The existing run/export mechanism saves the original answers, validated
requirements, prompt, schema, model/settings, response identifier, and available
token usage in downloadable JSON. Website runs remain temporary; export before
they expire. The preview can continue to O*NET grounding below. Tests use
mocked model responses, including a human-authored
extraction of the paper's worked example; they do not measure live LLM quality.

## Step 3: ground task vocabulary with O*NET

After a successful extraction, choose **Ground with O*NET** in the requirements
preview. Enter an OpenAI key again because the extraction key has been cleared.
This creates a separate run using a copy of the accepted requirements and exact
original answers; it does not repeat extraction. The original run stays available
until its normal expiry. Grounding uses local reference search followed by one
paid GPT-6 Luna mapping request per task facet with candidates, and stops at an
inspectable mapping preview. It does not retrieve or judge benchmark questions.

[`onet.py`](onet.py) reads `materials/ONET_index.csv` and
`materials/ONET_embeddings.npz`. The supplied table contains 3,197 records from
a healthcare-focused O*NET catalog, including occupations, skills/abilities,
knowledge, and work activities. The companion `skill_bank.json` supplies the
richer source catalog; its metadata identifies O*NET 30.3, retrieved 2026-08-22,
with attribution to the U.S. Department of Labor/ETA and the National Center for
O*NET Development under CC BY 4.0. These materials are a healthcare subset, not
the entire O*NET database. `deployment_goal.txt` supplies 15 six-answer scenarios
for manual pipeline review, without expected extracted or mapped outputs.

Local retrieval uses:

- **Meaning-based search:** `BAAI/bge-small-en-v1.5`, pinned to revision
  `5c38ec7c405ec4b44b94cc5a9bb96e735b38267a`, with CLS pooling, L2 normalization,
  and right truncation at 512 tokens. Documents use the CSV `text` field;
  queries use BGE's documented retrieval instruction. Before its first dense
  search, the index re-encodes eight evenly spaced records and requires a cosine
  match of at least 0.9999 with their saved vectors. Incompatible vectors fail
  explicitly. This is a sampled compatibility check, not a complete reconstruction
  of the original index-generation process.
- **Keyword search:** `rank-bm25` BM25Okapi, with Unicode word tokens after
  casefolding, `k1=1.5`, `b=0.75`, and `epsilon=0.25`.
- **Combined ranking:** up to 50 candidates from each method, reciprocal-rank
  fusion with `k=60`, and the top 20 unique records per facet. Record IDs break
  ties deterministically. These depths and Step 3 fusion settings are implementation
  choices; the paper specifies the two search methods but not these parameters.

Install `requirements-retrieval.txt` for NumPy, Torch, Transformers, and BM25.
The first dense search downloads the pinned model if it is not cached. Subsequent
searches reuse the local reference index and encoder; user queries and mappings
remain with their individual runs. `ITEM_REVIEW_ONET_DIR` can point the website
to another directory containing the two prepared files. Restart the server when
replacing the reference files, since the index is cached for the process lifetime.

[`onet_mapping.py`](onet_mapping.py) uses each facet's task text as its O*NET
search query. Shared answer-format and educational wording is kept out of this
query so it does not overwhelm the task vocabulary. The mapper still receives
the full deployment context when assessing applicability.
[`map_onet.md`](prompts/map_onet.md) contains the
complete mapping instructions. The mapper receives the original answers,
requirements, facet, and shortlisted record text. For every record it assesses,
it returns an exact supporting passage, applicability (`applicable`,
`partially_applicable`, or `not_applicable`), a rationale, and supported search
phrases. Applicable and partially applicable records are adopted; rejected
records contribute no phrases. It may also return up to three refinements with
literal evidence from the original deployment answers. The original tasks,
authority, answer formats, and collection targets stay unchanged.

Pydantic and Python reject unknown/duplicate IDs, changed facet references,
nonliteral passages or search phrases, and invalid goal-source quotations. An
empty mapping with an explanation is valid: the task remains unchanged without
added O*NET vocabulary. These checks establish provenance, while the preview
lets a human assess semantic applicability. Invalid output fails without another
model attempt; transport retries retain the existing SDK policy. Cancellation or
a provider failure preserves completed facet mappings.

The JSON export includes the original answers and extraction snapshot, source run
ID, local search queries and shortlisted records/ranks, validated mappings,
reference-file checksums, retrieval settings, sampled embedding compatibility
result, mapping prompt/schema, response metadata, and available token usage for
the grounding run. Results use the existing one-hour temporary retention policy.
Tests cover local search and mocked LLM responses. Real local BGE searches have
also been checked against the supplied vectors; no live mapping quality is
claimed by these checks.

## Step 4: retrieve benchmark items

After a completed O*NET grounding run, choose **Retrieve benchmark items**.
This step searches the whole Measurement Data Bank on a pinned `main` commit:
every row of every discovered `items.parquet` table, across all benchmark
collections and releases. There is no collection selector or release filter.
It makes no paid model calls and needs no OpenAI key. The output is a set of
candidate queues for later screening, without validity judgments or a final
benchmark selection.

The hosted inventory pins `main` at
`54074453da7b9911be0f48e4c560be547bc84d21`, with **281 benchmark collections,
281 item tables, and 8,471,422 source rows**. Refreshing this inventory reads
table metadata; it does not build the full retrieval index. The complete bank
has not yet been indexed and searched end to end.

[`benchmark_queries.py`](benchmark_queries.py) creates one deterministic query
per extracted task. The query combines the task, required input/output behavior,
deployment context, adopted O*NET phrases, and validated goal-supported
refinements. Rejected O*NET records contribute no phrases. A completed mapping
with no adopted record is valid and searches using the existing task context.
The exact query, adopted record IDs, and refinement evidence remain inspectable.
There is no additional LLM query-generation request.

[`benchmark_index.py`](benchmark_index.py) streams the whole item bank into a
local SQLite index. Every column of each `items.parquet` row is preserved under
`evidence.item`, and the complete row is serialized as `search_text` for both
search methods using sorted field labels and original string values, including
literal whitespace. Canonical JSON is used separately for exact-row identity;
JSON stored inside a string cell is preserved without parsing or normalizing it.
This includes identifiers, questions, answers, grading criteria,
and any other fields present in the source row. A row without a conventional
question field is still searchable. Rows are duplicates only when their complete
contents match, including identifiers; matching question text alone does not
combine them. Every distinct source reference is retained. The separate
`question_text` field is only a convenient display preview.

Each task uses two searches:

- **Dense:** up to 600 items using the same pinned BGE model as Step 3. Each
  complete row is split into nonoverlapping token chunks that fit the model's
  512-token window, including special tokens. Each chunk uses CLS pooling and
  L2 normalization; their mean is normalized again to produce one row vector.
  This includes the full row instead of dropping fields beyond one model
  window. Queries use the same chunking and pooling, with the BGE retrieval
  instruction prefixed once to the complete query. Documents have no instruction
  prefix. Disk vectors are scanned in bounded batches.
- **BM25:** up to 600 matching items through SQLite FTS5, with its built-in
  `k1=1.2`, `b=0.75`, and `unicode61` tokenizer with diacritic removal. Quoted
  query words are joined with OR; user text cannot become FTS query operators.
  This disk-backed implementation differs from Step 3's `rank-bm25` settings.
- **Fusion:** reciprocal-rank fusion with `k=60`, preserving the complete union
  of both lists (up to 1,200 distinct items per task). Evidence hashes resolve
  score ties. There is no additional truncation of the fused ranking.

The task's complete ranking becomes its all-source queue. Filtering that same
order by benchmark collection produces one queue per source collection. An item
may occur in several queues, with the same stable evidence identifier. The
`ScreeningQueues` helper supports later selection of the next unseen items using
a shared set of successfully screened IDs; retrieving or stopping a run does not
mark candidates as screened. Step 4 ends at retrieval; the completed preview
offers a separate action to start the initial screening below.

The first index build reads the complete bank and computes local BGE
vectors, so it can require substantial time and disk. Evidence, source references,
and vectors remain on disk instead of materializing the full corpus in memory.
The website caches completed indexes under
`WEBSITE_DATA_DIR/benchmark-retrieval-index/`; direct Python use defaults to
`~/.cache/benchmark-caliper/benchmark-index/`. Cache identity includes the complete
pinned main-branch inventory, loader version, and indexing/encoding policy.
Updated source commits or policies create a separate cache. Interrupted or
failed builds are not published and must be restarted. Cached indexes contain
dataset evidence and vectors, not
user deployment answers, query vectors, or provider keys.

Install the existing retrieval dependencies and configure authorized Hugging
Face dataset access on the server. The pinned BGE model is downloaded once if
absent from the local Hugging Face cache. The index needs SQLite with FTS5.
The preview shows task queries, queue membership, complete searchable row text,
original source fields, source provenance, dense/BM25 ranks, and RRF scores.
The JSON export preserves the original answers, requirements, grounding, pinned
inventory, policies, queries, candidates, and queues. Stopping a run preserves
completed task results. Runs retain the existing
temporary expiry policy; download the export to keep the result.

Tests cover retrieval, complete-row identity and field preservation,
cache/cancellation behavior, query assembly, queue ordering, and website
integration with offline fixtures. A real BGE smoke check retrieved all nine
EngiBench rows with every source column preserved and verified cache reuse.
Long-row checks also confirmed that text beyond token 512 affects the embedding.
These checks do not establish performance or
retrieval quality across the whole bank, which has not been run end to end.

## Step 5: screen the initial 50 candidates

After completed retrieval, choose **Screen initial candidates**. This step
assesses at most **50 distinct items** using GPT-6 Luna. The fixed budget of 50
is the agreed implementation choice; the paper's worked example uses 48 items
across three tasks. This stage does not perform adaptive allocation, assemble a
collection, or implement Step 7. Collection selection follows separately in
Step 6.

[`screening_queue.py`](screening_queue.py) allocates the budget deterministically
across the tasks' all-source queues. Each pass takes the next unseen item from
each task in the existing task order, preserving retrieval rank within each
queue. Three queues with enough distinct items receive 17, 17, and 16 items.
An overlapping item counts once globally; the next queue skips it and continues
to its next unseen candidate. When a queue is exhausted, the remaining queues
use the available budget. If their combined union has fewer than 50 items, the
allocation records the shortfall. Per-collection queues do not receive separate
initial allocations, and the original queues are unchanged.

[`screening.py`](screening.py) sends one request per allocated item using the
[`screen_item.md`](prompts/screen_item.md) prompt and a strict structured-output
schema. Inputs are the six original answers, validated extracted requirements,
and the complete original row under `item`. Retrieval queries, queue labels,
and retrieval scores are not model inputs. The model identifies the decision
actually requested by the question and matches it against any extracted task
facet, independently of which queue supplied it. It returns:

- A task finding: matched facet IDs, no match, or unresolved, with supporting
  item excerpts, justification, and information gaps.
- Separate 1–5 or null ratings for input ontology, input content, input form,
  output ontology, output content, and output form, each with the same evidence
  and explanation fields. There is no numerical confidence or aggregate score.
- One true, false, or null coverage finding for each explicit coverage
  requirement, identified by its zero-based `requirement_index`. This describes
  an item's contribution; collection-wide numerical minimums are not imposed
  on a single item.

The prompt defines score anchors from fundamental mismatch (1) to strong
alignment supported by positive evidence (5), and uses null when the supplied
evidence cannot support a rating. These anchors and explicit unknown handling
are implementation choices that make the paper's ratings operational. The
default model settings are `gpt-6-luna`, high reasoning effort, and a 25,000-token
output ceiling. Calls use the Responses API with `store=False` and no tools.

Python validates task references, coverage indices and scope, and literal
evidence excerpts against original string values in the item, including nested
values. It does not verify whether an excerpt semantically supports a judgment.
A resolved task, numerical rating, or true/false coverage finding needs an item
excerpt; an unknown finding needs a stated information gap. Invalid responses
remain errors without an accepted assessment or an automatic model repair.
Reference answers are evidence to inspect, not proof of correctness, and the
output-content rating is not expert validation of clinical answers.

The construction gate is computed by Python. It passes only with a matched task
and ratings of at least 3 for **input ontology, input content, input form, and
output ontology**. A clear task mismatch or any known score below 3 in these
four dimensions fails, even if other findings are unknown. Otherwise an
unresolved task or a null gated rating leaves the gate unresolved. Output
content, output form, and coverage findings remain inspectable but do not
change this gate. A passing gate is eligibility for later construction, not
final selection or a performance result.

The website uses the existing run token and a fresh OpenAI key for each
screening run. No dataset fetch or retrieval rerun is needed. Cancellation or a
provider failure retains completed assessments. **Continue screening** reuses
the same allocation and its original prompt/settings snapshot, retaining all
valid pass, fail, and unresolved assessments and retrying only pending or errored
items. Incompatible saved schema versions require a new run from retrieval.
Run-level token totals cover only new calls; each item keeps its own usage,
response metadata, and originating `screened_run_id`.

The export includes the complete screening allocation and results alongside the
original answers, extraction, grounding, retrieval inventory, candidates, and
queues. The prompt, schema, model settings, and gate policy are inspectable.
Temporary run expiry still applies. The allocator and synchronous/asynchronous
screener are also available as Python library functions/classes; there is no
new Step 5 CLI command.

Tests exercise allocation, strict response/evidence validation, gate behavior,
mocked provider requests, and website continuation, cancellation, and export.
Live provider judgment quality has not been validated, and these tests do not
constitute an end-to-end run over the complete bank.

## Step 6: select a collection under coverage constraints

After screening finishes, **Select up to 30 items** builds a collection from the
valid assessments already available. This is a local calculation with no new
LLM request or dataset fetch. A stopped or failed screening run can still
provide its completed assessments; pending and errored items are reported
separately and cannot be selected. This stage does not start adaptive screening
or freeze the collection for expert validation.

[`selection.py`](selection.py) revalidates the original item identities and
screening assessments, recomputes the four-dimension gate, and considers only
passing items. Exact full-row duplicates count once; conflicting assessments
for the same row are rejected. Neither retrieval scores nor the saved gate
label determine eligibility. For each eligible item, its construction-fit score
`Q` is the mean of input ontology, input content, input form, and output
ontology. Output content and output form remain reported separately. This score
does not use confidence or establish clinical answer correctness.

The selected collection contains **at most 30 distinct items in total**, across
all tasks. Every extracted task has a default minimum of one selected item;
the `essential` flag does not remove a task from this policy. There is no
automatic equal split or larger per-task minimum. Each explicit positive
`minimum_items` coverage requirement supplies an additional constraint. An item
counts for a task only when its screened question requests that decision, and
counts toward a conditional quota only when its corresponding coverage finding
is true. One item may contribute to multiple supported tasks or conditions
while occupying one place. False and unknown coverage findings do not satisfy
a quota. Requirements with `minimum_items: null` remain visible as unresolved
rules rather than receiving an invented numerical minimum.

Selection uses SciPy's mixed-integer optimizer with the HiGHS solver. One binary
variable represents each eligible item. Constraints enforce the size limit and
coverage minimums, and the objective maximizes the sum of the four gated
ratings, exactly equivalent to maximizing total `Q`. Scores are positive, so
available places are filled when enough eligible items exist; smaller pools
produce smaller collections. Among equally rated feasible collections, repeated
solver checks choose the lexicographically smallest sorted item-ID list. This
handles overlapping tasks and quotas without relying on a greedy per-task
selection or an approximate ID-rank tie breaker.

When the current screened pool cannot satisfy every constraint, the original
targets remain unchanged and gaps remain explicit. The documented fallback
first maximizes the number of represented tasks, then minimizes the sum of
shortfalls across explicit numerical quotas, then maximizes the same rating
total, followed by the item-ID tie break. The quota-shortfall ordering is an
implementation choice for otherwise unspecified infeasible cases. Missing
candidates and coverage that cannot fit within 30 are reported, without lowering
rating thresholds or treating unknown findings as successes.

The selector can reconsider all eligible items as more screening results become
available. Its optional `previous_selected_ids` preserves achieved task coverage
and numerical-quota counts up to their stated minimums, while allowing higher
rated items to replace earlier ones. It does not lock individual items or
preserve excess counts beyond a minimum. A solver timeout or cancellation does
not prove infeasibility: an interrupted computation produces no new accepted
collection, and the website retains the preceding accepted selection when one
exists.

The website's **Select up to 30 items** action requires the existing run token, not
an OpenAI key. It saves a separate selection run with the input artifacts,
selected IDs, item quality values, coverage counts, gaps, exclusions, policy,
and solver outcome. `selection_input` distinguishes allocated, completed,
errored, and pending screening items; `selection_run_id` identifies the run
that produced the accepted collection, including one retained after a retry.
Its export retains the original answers, requirements,
grounding, retrieval, and screening. **Continue screening** from a selection
can finish pending or errored items from the original 50-item allocation;
reselect afterward to incorporate the new results. It does not add adaptive
batches. Step 7 reuses the same Python `select_collection` function after each
adaptive batch; there is no new CLI command.

Tests compare small random problems with an independent exhaustive enumeration
of every possible collection, alongside overlapping task/quota cases, exact-ID
ties, partial results, preserved coverage, cancellation, and solver limits.
These checks establish implementation behavior, not the validity of model
ratings or performance across the complete item bank.

## Step 7: adapt screening and freeze the collection

After all candidates in the initial allocation have valid screening results and
Step 6 has accepted a collection, **Start adaptive screening** continues through
the saved Step 4 task/source queues. It does not retrieve more candidates, alter
their ranks, or repeat the initial 50 screening calls. The total candidate limit
is **160 distinct items, including the initial allocation**; each subsequent
batch contains at most eight unseen items. The selected collection still holds
at most 30 items in total.

[`adaptive_screening.py`](adaptive_screening.py) maintains queue counters and
makes the next queue decision locally. Each queue starts with `Beta(1, 1)`. A
candidate is a success if it belongs to the accepted collection immediately
after its batch; every other validly screened candidate is a failure for this
selection signal. This is a retention signal, not the probability of passing
the gate or answering the question correctly. The initial Step 6 collection
supplies batch zero's outcomes. Each outcome is recorded once, including when a
later collection replaces an item that was previously successful.

For a queue with `s` successes and `f` failures, its estimated yield is
`(1 + s) / (2 + s + f)`. Two retained candidates out of a first batch of eight
therefore produce `Beta(3, 7)` and yield `0.3`. Credit applies to the acquisition
task's all-source queue and each source queue containing that exact original
row, once per queue. Overlapping retrieval under a different task does not
receive an outcome from that acquisition.

Queue priority is estimated yield multiplied by a coverage weight. The default
task minimum gives weight 2 to an uncovered task and 1 to a covered task. For
explicit numerical requirements, the controller uses the largest applicable
fractional shortfall, `(minimum - selected_count) / minimum`, capped below at
zero, and adds 1. Conditional requirements count only selected items whose
screening finding satisfies that condition. Requirements with no numerical
minimum remain unresolved and do not acquire an invented target. Extending the
paper's task shortfall to conditional quotas this way is an implementation
choice; Step 6 remains responsible for actual collection coverage constraints.

At each decision, exhausted queues are excluded. With probability 0.8, the
controller picks the highest-priority available queue, breaking ties by queue
ID. With probability 0.2, it picks uniformly among all available queues. A saved
seed and decision index reproduce each choice. The chosen queue supplies
the next highest-ranked unseen items; full-row duplicates already acquired
anywhere are skipped. Queue choices, priority components, acquisition IDs, and
exploration decisions are retained in batch history.

Screening reuses Step 5's saved model, prompt, schema, and six-dimensional
assessment, then Step 6 reconsiders all eligible results accumulated so far.
Previously achieved task coverage and quota counts up to their targets are
preserved, while individual items can be replaced. Only a fully screened batch
and a successfully completed selection commit new outcomes and queue counters.
A provider error, invalid response, cancellation, or solver interruption keeps
the last accepted collection and the pending batch. Continuation retries only
unfinished or invalid assessments from that batch before choosing another
queue. It never treats an operational failure as a selection failure.

If the cost budget cannot fund retries of a pending batch, the controller may
instead select from that batch's valid assessments and freeze the collection.
It records outcomes only for those valid assessments and lists the remaining
item IDs as unresolved. This final partial batch cannot be resumed; errors and
unanswered requests never become negative retention outcomes.

The loop freezes the last accepted collection at the candidate limit, queue
exhaustion, or configured cost limit. Filling all task minima does not stop it:
later items may still improve quality. A frozen result cannot continue adaptive
screening; its gaps remain visible for expert review. Freezing does not establish
model performance or validate the screening judgments.

An optional dollar ceiling is set before starting, together with explicit input,
cached-input, and output prices per million tokens. Prices are supplied by the
caller, never inferred from a model name. The ceiling covers **new Step 7
screening calls only**, excluding the earlier extraction, grounding, and initial
screening costs. Request admission reserves a conservative estimate from the
serialized request size and maximum output tokens; provider-reported usage then
settles that reservation, counting cached input separately and output reasoning
tokens within output tokens. This is an admission estimate, not a guaranteed
provider bill. Unknown usage remains explicitly recorded with its reservation;
it is never silently assigned zero cost. SDK retries are disabled so retries are
explicit attempts in this ledger. Without configured prices, dollar amounts
remain unknown while token usage is still reported.

The website's `POST /api/item-review/runs/{run_id}/adapt` action requires the
source run token and a fresh OpenAI key. It starts from a completed selection or
resumes an interrupted adaptive run with unchanged settings. Each continuation
creates a separate run and copies the earlier artifacts, batch history, request
attempts with their usage, and accepted collection. The source stays unchanged.
Export includes settings,
queue statistics, batch outcomes and collection changes, attempt-level usage,
cost scope, remaining gaps, and the stopping reason. Ordinary `/screen` and
`/select` continuations reject adaptive runs so they cannot discard this history.
Hosted runs retain the existing temporary expiry and do not survive a server
restart.

## Existing Qwen retrieval and six-dimension assessment

Describe an AI deployment, retrieve a bounded shortlist of evaluation questions
with local **Qwen3-Embedding-0.6B** embeddings, then assess only that shortlist with
**GPT-6 Luna**. The existing six validity judgments, evidence, confidence, and final
ranking remain unchanged. Retrieval reduces the number of paid judgments; live
assessment still requires an OpenAI API key.

This is a retrieval-augmented assessment workflow. Embedding inference runs on
local hardware without paid embedding API calls. It does not use Qwen to generate
answers. Embedding similarity selects candidates; it is not a validity score,
calibrated confidence, or a guarantee of deployment compatibility.

The [website](../website/README.md) retains this separate assessment option at
`/benchmark-caliper/items`. This option retrieves from a fixed, reproducible sample of up
to 50 distinct items per benchmark collection from the hosted main-branch
inventory, currently at most **13,602 sampled items**. The CLI still defaults to
discovering both `main` and the historical migration branch; `--branches main`
restricts CLI inventory discovery to main. It can index the full saved inventory
or use explicit source-row limits. The
website and CLI keep retrieval relevance separate from the original
[six-dimensional framework](../anthropic_api_package_release/framework.yaml).

## Quick start

Run these commands from the repository root:

```bash
python -m pip install -r bayesian_auditing/requirements.txt -r bayesian_auditing/requirements-retrieval.txt
```

Access to the gated
[measurement-db dataset](https://huggingface.co/datasets/aims-foundations/measurement-db)
requires an authorized Hugging Face account. The loader uses the existing Hub
login or `HF_TOKEN`. Use `hf auth login` if a login is needed. Live judging also
requires `OPENAI_API_KEY` in the environment and access to `gpt-6-luna`.

Start with two benchmark directories to inspect a small example from both
branches:

```bash
python -m bayesian_auditing inventory \
  --benchmarks matharena afrimedqa \
  --output bayesian_auditing/results/demo_inventory.json

python -m bayesian_auditing run \
  --inventory bayesian_auditing/results/demo_inventory.json \
  --deployment bayesian_auditing/examples/deployment.txt \
  --output-dir bayesian_auditing/results/demo_preview \
  --limit-per-table 2 --dry-run
```

The included deployment is an example text mathematics tutor. Replace it with a
description of your intended users, tasks, input format, expected outputs,
success criteria, and constraints. Unspecified requirements remain unspecified;
the judge is instructed to report information gaps.

`--dry-run` downloads data/model files as needed, computes local embeddings,
retrieves the shortlist, and saves its actual judge inputs without making OpenAI
calls or producing validity scores. The pinned sample inventory currently contains
three tables: matharena in both branches and afrimedqa in the migration branch.
The limit applies to source rows in **each table**, before duplicate detection.

Once the inputs look appropriate, run a small paid assessment in a new folder:

```bash
python -m bayesian_auditing run \
  --inventory bayesian_auditing/results/demo_inventory.json \
  --deployment bayesian_auditing/examples/deployment.txt \
  --output-dir bayesian_auditing/results/demo_scores \
  --limit-per-table 2 --retrieve-k 5 --top-k 5
```

`--retrieve-k` limits the number of distinct items sent to the judge (default
20). `--top-k` independently limits the final validity-ranked output (default
10). Use `--retrieval-query path/to/question.txt` to retrieve using a specific
reference question; otherwise the deployment description is the retrieval query.
The judge always receives the full deployment description and original item
evidence, regardless of which retrieval query you choose.

The first local embedding pass downloads the pinned Qwen3 model and tokenizer through the standard Hugging
Face cache (`HF_HOME` can relocate it) and computes question vectors. Later runs reuse item vectors from the private
cache at `~/.cache/benchmark-caliper/question-embeddings/`;
`--embedding-cache-dir PATH` selects another location. User queries are not
written to that reusable embedding cache, though the run configuration records
the query for reproducibility. This removes embedding API charges, not hardware,
download, storage, or judge costs. Qwen3's 0.6B weights and runtime need substantially
more memory than lexical search: approximately 2.4 GB for FP32 weights on CPU
or 1.2 GB for FP16 weights on CUDA, plus framework and activation memory. CUDA
is used when available; otherwise inference runs on CPU. Measure peak RAM with
representative question lengths before a large run. The
full-corpus CLI index retains normalized records and vectors in memory.

The model defaults to `gpt-6-luna` with `--reasoning-effort high`; `--model` and
`--reasoning-effort` are available for later comparisons. The default
`--max-output-tokens 25000` includes internal reasoning and the final assessment.
This ceiling follows [OpenAI's initial reasoning-token guidance](https://developers.openai.com/api/docs/guides/reasoning#allocating-space-for-reasoning)
and does not force each item to consume that many tokens. High effort may use
more time and tokens; its effect on scoring quality needs human-reviewed
evaluation. The request timeout is 600 seconds to accommodate longer responses.
An incomplete or invalid response is recorded as an error, never as a low
validity score.

## Process and scoring

1. **Discover and pin the data.** `inventory` reads `main` and
   `migration/tabular-builders-20260924`, saving their commit IDs and item-table
   paths. It checks benchmark roots and `formatted_tables/`, avoiding raw data
   and model-response traces. `--branches` can explicitly select other branches.
   Missing item tables are reported in the inventory.
2. **Read each item.** The loader streams Parquet rows and combines the full item
   text, grading criterion/reference answer, verifier description, item features,
   asset references, and available benchmark metadata. Verifiers are never
   executed. Metadata about historical model performance is excluded.
3. **Deduplicate evidence.** An exact hash of all supplied item evidence and
   benchmark context identifies duplicates, including copies across branches.
   Identical evidence is assessed once per deployment/run; every source remains
   traceable. Different grading criteria or context produce separate assessments.
4. **Retrieve a shortlist locally.** Embed only the item question/content using
   `Qwen/Qwen3-Embedding-0.6B`, pinned to revision
   `97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3`. Both query and questions use the same
   plain-text encoding, an 8,192-token maximum with truncation, last-token
   pooling, and unit normalization. Rank by dot product, with exact question
   matches first. Grading answers and benchmark metadata remain available to
   the judge but are excluded from the retrieval text. Long question tails can
   therefore be absent from retrieval even though full evidence is preserved.
   Items without retrievable question content are counted separately.
5. **Assess all six dimensions in one call per retrieved item.** The deployment description and
   evidence are sent with the readable [judging prompt](prompts/assess_item.md).
   Every dimension returns a score (or an explicit unknown), confidence and its
   rationale, a short justification, evidence references, and information gaps.
6. **Validate and rank the assessed shortlist.** Python validates the structured response and computes
   a confidence-adjusted ranking score and the original compatibility mean.
   Partial assessments remain ranked with their dimension coverage shown;
   assessments with no scores are retained without a rank. Results retain the
   original numerical confidence, rationales, gaps, and source provenance.

| Dimension | Item-level question |
| --- | --- |
| Input ontology | Does this task or capability belong to the deployment workload or test a stated constraint? |
| Input content | Does the particular scenario fit the domain, users, language, and operating conditions? |
| Input form | Does the input modality, representation, and interaction format match? |
| Output ontology | Do the expected decisions and grading criteria measure deployment success? |
| Output content | Is the particular reference answer or expected judgment appropriate and supported? |
| Output form | Does the expected response format, modality, and language match? |

Scores range from **1 (fundamental mismatch)** to **5 (strong, evidence-supported
alignment)**, with dimension-specific anchors in the prompt. Compatibility and
confidence are separate judgments. The judge should make a defensible tentative
estimate when possible, with low confidence and explicit assumptions. When no
estimate is defensible, both score and confidence stay `null`, and
an information gap is required. A missing dimension no longer discards the item.

Scoring version 5 requests numerical confidence from 0 to 1 directly from the
model. It describes how strongly the supplied evidence supports the particular
compatibility score. Higher values indicate direct, applicable, consistent
evidence with little material uncertainty; lower values indicate tentative
support involving indirect evidence, conflicts, assumptions, or consequential
gaps. The prompt asks the model to consider evidence relevance, completeness,
consistency, and the importance of uncertainty for each dimension. It does not
frame confidence as agreement with a reviewer, and does not assign numerical
values to categorical labels. A null score has null confidence, distinct from
a numerical confidence of zero. The UI shows numbers directly, without buckets.

The prompt and schema request evidence, dimension-specific information gaps,
and a concise justification identifying material assumptions before the score
and confidence. Each confidence rationale must link the number to that evidence
and explain what could change the rating. A missing reference answer need not
lower confidence in an independently assessable input format.

`overall_score` is a conservative ranking score on a 1–5 scale. Each scored
dimension contributes `1 + confidence * (score - 1)`, and each missing dimension
contributes 1. Average these contributions over all six dimensions:

```text
overall_score = 1 + sum(confidence * (score - 1) for scored dimensions) / 6
```

The floor of 1 represents no positive ranking support. It does not assign a
compatibility judgment to missing dimensions: their original score and confidence
remain `null`. If all dimensions are unknown, `overall_score` is also `null`,
and the item is unranked. A scored item with zero confidence receives a ranking
score of 1. Lower confidence never increases a contribution, and removing a
score cannot improve the ranking score. All six dimensions retain equal weight;
the denominator is not the sum of confidence values. Full confidence on all six
dimensions recovers the original compatibility mean.

`compatibility_score` is the unadjusted mean of available compatibility scores,
shown alongside the ranking score. It excludes missing dimensions and is
independent of confidence. `scored_dimensions` records coverage. `needs_review`
flags any missing score or explicit information gap, including unverified material
assumptions. It uses no confidence cutoff. The CLI and website share this arithmetic.

For example, five scores of 4 at confidence 0.8 and one unknown yield a ranking
score of 3.0, a compatibility mean of 4, and coverage of 5/6. A score of 5 at
confidence 0.2 contributes 1.8, while a score of 4 at confidence 0.9 contributes
3.7. A mismatch scored 1 contributes 1 at any confidence, so uncertainty never
erases that weakness from the average.

Six unknowns yield `null` for both scores and no rank. These assessments remain
in the CLI assessment log and the website's `unranked_items` list, including its
JSON download. `complete` counts all valid assessments; `ranked` and `unranked`
distinguish score availability. Compare coverage and individual dimensions when
interpreting the unadjusted mean.

Confidence is the judge's evidence-support assessment, not a calibrated
probability or measured reliability. The linear discount toward 1 is an explicit
conservative ranking policy, not an expected compatibility score, statistical
lower bound, or validated validity measure. An average can still hide individual
mismatches. Ties use evidence hashes for deterministic ordering. Human-reviewed
calibration and comparison of ranking policies are later steps.

Existing report files are not rewritten. Version 2 used confidence weights and
neutral placeholders; version 3 kept categorical confidence separate from the
mean; version 4 used numerical confidence separate from the mean. The website
preserves those reports' original scoring explanations. Resuming with a different
scoring policy or prompt is rejected to prevent mixing methods. Use a new output
directory for version 5.

## Traverse the full inventory

Omit the benchmark filter when discovering tables, and omit the row limit to
retrieve from the full inventory. The shortlist limit still bounds judging:

```bash
python -m bayesian_auditing inventory \
  --output bayesian_auditing/results/inventory.json

python -m bayesian_auditing run \
  --inventory bayesian_auditing/results/inventory.json \
  --deployment bayesian_auditing/examples/deployment.txt \
  --output-dir bayesian_auditing/results/full_run \
  --retrieve-k 20 --top-k 10
```

This indexes the saved inventory locally and makes paid judgment requests only
for the retrieved shortlist. First-time embedding and loading can take substantial
time, RAM, and disk for a large inventory. `--limit-per-table` limits retrieval's
source rows, not just the number of paid calls. `--retrieve-k` bounds paid item
judgments, but each judgment can consume different tokens and provider retries
can add requests; it is not a fixed dollar budget.

Use the same command with `--resume` after an interruption. Resume requires the
same inventory, deployment, retrieval query/policy/limit and exact selected
evidence, prompt, schema, judge model, reasoning settings, token limit, and row
limit. Changing `--top-k` is allowed and rebuilds the ranked output
without repeating completed judgments. Resume reuses the frozen shortlist and
does not re-embed or rerank the corpus. Changed retrieval or scoring settings
need a new output folder. A preview cannot be resumed as a live run.

Old full-inventory CLI runs cannot be resumed as retrieval-shortlist runs.
Scoring-version-1 runs also cannot be resumed under this schema. Keep their exported
files and use a new output folder for version 5; old results have no recorded
confidence, so it must not be invented or silently backfilled. New judgments
require new API calls.

Completed assessments, including partial-evidence ones, are reused. Failed responses are retried
on resume. An invalid judgment is attempted only once per distinct evidence hash
in an invocation, even when multiple source rows reference it. After the SDK's
two retries, an API exception stops the run and saves
partial results, avoiding repeated requests during an authentication or quota
failure. Dataset read errors also stop the run. A partially written final JSONL
record can be recovered on resume; corruption in a complete line is reported.
An interruption after a request succeeds but before its result is saved can
cause that request to be repeated. Use one process per output directory.

## Output files

| File | Contents |
| --- | --- |
| `run.json` | Deployment, pinned inventory, retrieval query/policy and exact shortlist evidence, judge settings, rubric, and output-schema snapshot. |
| `assessments.jsonl` | Append-only assessments with confidence, errors, and duplicate source references. Previews include the exact request input. |
| `ranked_items.json` | Up to `--top-k` assessments with at least one score, ordered by confidence-adjusted ranking score, with the original compatibility mean, coverage, confidence, evidence, all source references, and the separate retrieval rank, similarity, and exact-match flag. |
| `summary.json` | Indexed corpus counts, retrieved/assessed shortlist counts, scope, errors, retrieval and scoring policies, token usage across attempts, and any fatal error. |

`full_inventory_indexed` describes retrieval's source coverage. It does not mean
that every item was judged. `corpus_items` counts distinct evidence records;
`indexed_items` counts those with retrievable question content. The retrieval
metadata also reports `contentless_items`. `retrieved_candidates` and
`shortlist_assessed` distinguish selection from completed judgments. `configured_scope_traversed`
means the shortlist was processed. `full_inventory_scored` remains false when
items were omitted by retrieval, row limits, missing tables, failures, or preview
mode. “Full inventory” means the saved inventory, which may already be filtered
by branch or benchmark. Final rankings describe the assessed shortlist only.

Partial and unknown assessments remain in `assessments.jsonl`; inspect
`unranked`, `needs_review`, and individual information gaps. Reported output tokens
already include reasoning tokens. Usage can be unavailable for failed requests.
Referenced images, audio, and linked documents are not inspected. Retrieval
truncates question inputs at its token limit; the judge's evidence is not silently
truncated and can still exceed provider limits.

## Maintainer guide

| File | Responsibility |
| --- | --- |
| `data.py` | Discover tables, pin revisions, normalize evidence, and preserve provenance. |
| `prompts/assess_item.md` | Six-dimensional rubric and evidence requirements. |
| `scoring.py` | Typed output schema, validation, and aggregate arithmetic. |
| `judge.py` | One structured OpenAI Responses request. |
| `retrieval.py` | Local Qwen3 embeddings, question cache, exact-match priority, and shortlist selection. |
| `runner.py` | Sequential shortlisted judgments, duplicate detection, checkpoint log, and validity ranking. |
| `__main__.py` | CLI arguments and client setup. |

The modules are independent of the existing website and Anthropic pipeline. The
rubric is deliberately an item-level adaptation: a single item cannot establish
the coverage or validity of an entire benchmark. The retrieval index retains
normalized item records and question vectors in memory. The judge loop reuses completed evidence hashes and retains only the
requested top validity-ranked items when writing its report. Increase `DATA_VERSION` or
`SCORING_VERSION` when changes would make previous runs incompatible.

```bash
python -m pip install -r bayesian_auditing/requirements-dev.txt
python -m pytest bayesian_auditing/tests -q
```

Tests use local Parquet fixtures for both branch layouts and mock HTTP responses
through the real OpenAI SDK. They cover validation, ranking, duplicate handling,
resume, incomplete/refused responses, and failure reporting without paid calls.
They do not establish retrieval recall or judge quality. Human review is needed
before relying on a shortlisted ranking, and omitted items may be relevant.

API references: [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)
and [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).
