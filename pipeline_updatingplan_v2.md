# Pipeline update v2: measurement-db data bank integration

Revision of `pipeline_updatingplan.md`. Structural changes from v1: the data-bank
lookup moves earlier (URL match at submission, name match after Step 1) so the
dataset-link request rides inside the existing elicitation round-trip instead of
adding a second pause; a fuzzy near-miss confirmation replaces silent NOT_FOUND;
Mode 1 gains a Haiku fan-out relevance-tagging stage (coverage, not a bigger
model, is where extra spend buys performance); an explicit "dataset not publicly
available" declaration replaces the garbage-link workaround; and the link
explorer gets an SSRF hardening section, which is a must-fix for the website.

## 1. What changes and why

The pipeline currently analyzes a benchmark's actual data only if the user
happens to supply a HuggingFace dataset ID. We now have a curated data bank on
HuggingFace (aims-foundations/measurement-db, gated): ~230 folders, one per
benchmark, each with

- benchmarks.parquet: one row of benchmark info (columns include name,
  paper_url, dataset_source, n_items, n_subjects, has_ground_truth,
  response_type, ...)
- items.parquet: every test item (content = question text, correct_answer)
- response.parquet: every (model, item, trial, score) observation
- subjects.parquet: the models that were evaluated
- traces.parquet: present in some folders; **ignored in v1** (decided, not an
  oversight). Revisit when we know what's in it.
- DATA_FORMAT.md at the repo root documents the schema; pull it once the token
  is provisioned and treat it as the authority over the column list above.

The new flow: the user provides a paper URL along with the PDF. The pipeline
checks whether the benchmark is already in the data bank. If yes, it analyzes
the bank's items and responses as the dataset evidence. If no, it asks for a
dataset link (or an explicit "not publicly available" declaration) inside the
elicitation round, analyzes whatever the link points to, and records the
benchmark in an internal list of uncurated-but-requested benchmarks.

Day-one prerequisite: an HF_TOKEN with access to the gated repo. None exists in
the dev environment today; nothing on the FOUND path can be tested without it.

## 2. User inputs

1. Benchmark paper (PDF) - same as today
2. Paper URL - new (e.g. https://arxiv.org/abs/2411.15640)
3. Deployment description - same as today
4. Dataset link OR a "dataset is not publicly available" declaration - asked
   only when the benchmark is not found in the data bank, bundled into the
   elicitation round (any host: HuggingFace, GitHub, Zenodo, Kaggle, OSF,
   Dataverse, personal website, ...)

## 3. The pipeline, step by step

Step -0 - Paper-URL match (NEW - deterministic code, no LLM, at submission)
The paper URL needs no LLM output, so it is matched the moment the run is
created, before Step 0. Normalized comparison against the cached index's
paper_url column (arxiv abs/pdf/version variants all treated as equal; host
aliases hf.co = huggingface.co; scheme/trailing-slash insensitive). A hit here
resolves the whole lookup: FOUND, folder recorded, no further questions ever.

Step 0 - Slug (Haiku, unchanged)
Derives a short folder name from the deployment description. All outputs for
this assessment live under assessments/<paper>/<slug>/.

Step 1 - Metadata (Haiku, unchanged)
Reads PDF pages 1-2, writes metadata.md with benchmark name, full name, domain,
languages, region. The structured "- name:" line feeds the name match below.

Step 1b - Data-bank name match (NEW - deterministic code, no LLM)
Only runs if Step -0 missed.

a. Load the cached index of every folder's benchmarks.parquet. Built once
   (~230 tiny downloads), cached keyed to the dataset's commit sha, so it
   refreshes only when the bank actually changes. Requires HF_TOKEN (repo is
   gated). Token missing or unauthorized: silently skip, pipeline behaves
   exactly as today.
b. Exact-normalized name match ("AfriMed-QA" matches "afrimedqa"): FOUND,
   folder recorded, done.
c. Exact miss but strong fuzzy candidate (deterministic scoring - rapidfuzz or
   token overlap - above a conservative threshold): NEAR_MISS. Do not decide;
   queue a confirmation question for the elicitation round ("Is this the same
   benchmark as 'afrimedqa' in our records?"). A silent wrong answer here costs
   double: redundant explorer work AND a bank benchmark polluting the
   missing-benchmarks log.
d. No candidate: NOT_FOUND. Queue the dataset-link request for the elicitation
   round.
e. The outcome (found | near_miss | not_found | skipped, matched folder,
   match key) is persisted to dataset_source.json in the assessment folder.

Step 2 - Elicitation (Sonnet + user, extended)
Sonnet asks 6-10 deployment questions as today. The same interaction now also
carries, when applicable:
- the NEAR_MISS confirmation (yes -> FOUND; no -> falls through to the link
  request in the same round), and
- the NOT_FOUND dataset-link request. The user pastes a link or explicitly
  declares the dataset not publicly available. There is no skip, but the
  declaration is a truthful escape: v1's no-escape design just laundered the
  skip through a garbage link, paying for a doomed Opus exploration and
  polluting the request log.
  - A pasted link is first checked against the bank's dataset_source column
    (match -> FOUND after all). Otherwise a huggingface.co/hf.co dataset link
    parses to org/name (Mode 2); anything else goes to the explorer (Mode 3).
  - CLI: prompted together with the elicitation answers; re-prompts until a
    valid http(s) URL or the literal declaration is given. Non-interactive runs
    must pass --dataset-link or --dataset-unavailable or exit with a clear
    error.
  - NOT_FOUND outcomes (name, paper_url, link or unavailable-declaration,
    timestamp) are appended to the internal request log
    (benchmarks/mdb_missing.jsonl on the CLI; missing_benchmarks SQLite table
    on the website). FOUND hits are logged too (folder, timestamp) - usage
    analytics for curation priorities. Neither log is ever shown to users.
Sonnet then writes elicitation_summary.md with priority weights, as today.

One interaction round total. The v1 draft was inconsistent here (S3 paused
after Step 2b, S5 paused during elicitation); this resolves toward the single
bundled round everywhere. Every extra pause multiplies abandonment.

Steps 3-5 (one addition)
Step 3: per-page Haiku extraction, Sonnet consolidation, benchmark YAML
synthesis. NEW: on FOUND, the matched benchmarks.parquet registry row is
injected into the Step 3b synthesis context - the bank's n_items,
response_type, has_ground_truth are authoritative over the paper's prose.
Step 4: deterministic quote verification, region scaffold with placeholders.
Step 5: Sonnet with web search fills the region YAML gaps (up to 10 searches).

Step 5b - Dataset analysis (existing step, gains two new modes)
Produces dataset_analysis_report.md either way. Mode was decided by Steps
-0/1b/2. The report header states its evidence strength (see below) so Step 7
weighs it appropriately.

Mode 1 - data-bank mode (FOUND branch). Three stages:

(i) Deterministic profile (scripts/dataset_analysis/mdb_profile.py, no LLM):
downloads the folder's items.parquet and response.parquet and computes
- per-item difficulty: fraction of models answering each item correctly;
  distribution, plus share of items at ceiling (>90% correct) and floor
- per-item discrimination: corrected item-total point-biserial
- overall reliability: KR-20 for dichotomous scores, Cronbach's alpha otherwise
  (branch on response_type / observed score domain - not every bank entry is
  0/1)
- guardrails: with < 10 subjects, discrimination and reliability are emitted as
  "insufficient subjects (n=K)" rather than numbers Step 7 would happily cite;
  same for items with too few observations
- a sample of item texts stratified by difficulty x category/subject (when
  items.parquet has a category column - relevance clusters by topic, so
  difficulty-only strata undersample it), within a char budget
- the benchmarks.parquet registry row

(ii) Relevance fan-out (Haiku, NEW): the deployment-specific question - are
these items relevant to this context - is the weak link if it rests on one
model reading a 30-item sample. Instead, a few hundred stratified items are
tagged in Haiku batches (each call: elicitation summary + a batch of items ->
per-item relevant / irrelevant / culture-bound + one-line reason). Same tiered
idiom as per-page PDF extraction; costs cents; turns the report's claims from
impressions into rates ("84% of sampled items are US-clinical").

(iii) Interpret (Sonnet, mdb_interpret): reads the profile stats, the tag
rates, sampled items, and the elicitation summary; writes the report - item
relevance, headroom for the models being deployed, ability to discriminate -
every claim citing specific items (D1, D2, ...) or tag rates.

Mode 2 - HF-link mode (existing machinery, NOT-FOUND branch with an HF link):
the dataset at the parsed org/name is downloaded, sampled within a char budget,
and interpreted by Sonnet against the deployment context. Today's --hf-dataset
behavior, triggered by the pasted link. The Haiku relevance fan-out from Mode 1
runs here too when items are extractable.

Mode 3 - explorer mode (NOT-FOUND branch with any other link):
an Opus agent gets three read-only tools - fetch a URL, list an archive's
contents, preview a data file (jsonl/csv/tsv/parquet/json) - and up to 12 turns
to locate and sample the actual data files behind the link. On success, Sonnet
interprets the sample (same report format). The explorer additionally emits a
short provenance note - which files it chose, why, what it rejected - appended
to the report. Its worst failure (confidently sampling the wrong files) is
otherwise silent; the note gives Step 7 and the human expert a way to catch it.
On failure the pipeline warns, records the link in the request log, and
continues without dataset analysis.

Unavailable-declaration: no analysis; the report is a stub stating the dataset
is not public, and the declaration is recorded in the request log.

Evidence strength header: Mode 1 = "full psychometric profile"; Modes 2/3 =
"qualitative sample only - no model-response data exists outside the bank, so
difficulty/discrimination/reliability are not computable"; declaration = "no
dataset evidence". This distinction can also feed the calibrated-confidence
column in the score table.

Step 6 - Prompt composition (script, unchanged)
Assembles the Opus evaluation prompt: rubric + benchmark YAML + region YAML +
elicitation summary + verified quotes + the dataset analysis report (whatever
mode produced it), with DATASET-D{n} citation format.

Step 7 - Validity scoring (Opus, unchanged)
One Opus call scores the six dimensions (Input/Output x Ontology/Content/Form,
1-5), now able to cite real data evidence, e.g. "IC = 2: 84% of sampled items
are US-clinical questions with no Indonesian coverage [DATASET-D4], and 61% of
items are at ceiling for frontier models [DATASET-D7]".

Steps 8-9 (unchanged)
Format the report and build the 7-section review PDF.

## 4. Model assignment

- Deterministic code (no LLM): URL/name/fuzzy matching, data-bank index, all
  psychometric statistics, quote verification, prompt assembly. The numerically
  hard parts are deliberately not model tasks.
- Haiku: existing duties (page extraction, metadata) plus the NEW relevance
  fan-out in Step 5b. Where extra quality is wanted, it is bought as coverage
  (hundreds of items actually read) rather than as a bigger summarizer - one
  Opus call reading 30 items cannot beat Haiku reading 400.
- Sonnet: the interpretation calls (mdb_interpret, link_interpret) - reading
  precomputed stats, tag rates, and samples against the deployment summary;
  same class of task as today's da_interpret. Deliberately NOT Opus: the hard
  numbers are script output, and the Step 7 Opus scorer re-reads the entire
  report anyway - an Opus interpreter would pay twice for the same judgment.
- Opus: Step 7 scoring, plus the link explorer. The explorer is the hardest new
  LLM task, its worst failure is silent downstream, and it only fires on
  bank-miss runs, so the marginal cost is bounded. The docs' "Opus: exactly one
  call" claim gets updated to name both call sites.

## 5. Website flow

Same logic, browser plumbing:
- The run form gains a Paper URL field (recommended, prominent). The existing
  HF dataset ID field moves into a collapsed "Advanced" section as a manual
  override.
- Step -0 (URL match) runs on submission; "1b - checking measurement data bank"
  appears as a progress step after metadata for the name/fuzzy match, using the
  server's own HF_TOKEN (never the user's Anthropic key). Found / near-miss /
  not-found / skipped is shown live via SSE.
- On FOUND, the dataset-analysis phase runs the psychometric profile + fan-out
  automatically; the user never supplies a dataset ID.
- On NEAR_MISS / NOT_FOUND, the confirmation and/or link form render inside the
  existing elicitation screen - one pause total, before any expensive steps.
  The link form offers the "dataset is not publicly available" declaration as
  an explicit choice; there is no skip. Submitting resumes via POST
  /api/runs/{id}/dataset-link (link or declaration) - reuse the elicitation
  submit path where possible; if a separate awaiting-dataset-link status
  exists, it must return to a scorable status on every exit path or
  /compose-prompt and /score will 409.
- Not-found benchmarks land in a new missing_benchmarks SQLite table (benchmark
  name, paper URL, link or declaration, run id, timestamp) written through
  logging_gate (the single privacy chokepoint), tier 1, redact() applied, query
  strings stripped from logged links (user-pasted URLs can embed presigned-URL
  secrets), run linkage severed on delete-my-data, included in /export. FOUND
  hits land in a bank_hits table with the same handling. Never shown in any UI.
  DESIGN.md, SECURITY.md and the privacy notice get updated to document both.

## 6. Explorer security (must-fix before the website ships Mode 3)

fetch_url executes server-side against arbitrary user-supplied URLs - the
textbook SSRF vector. Size caps and GET-only do not cover it. Required:

- Block private/reserved IP ranges, localhost, and cloud metadata endpoints
  (169.254.169.254), enforced on the resolved IP (pin DNS resolution, connect
  to the pinned IP) and re-validated after every redirect hop.
- http(s) schemes only; no credentials in URLs; response size caps on every
  download; never execute or render fetched content.
- The server's HF_TOKEN is attached ONLY to huggingface.co/hf.co requests -
  never to explorer fetches of arbitrary hosts, or the explorer becomes a
  token-exfiltration oracle. Same rule for any future secret.
- Per-run byte ceiling and fetch count logged to the trace.
- Each of these becomes a SECURITY.md checklist item mapped to a DESIGN.md
  claim, per the existing convention.

The CLI explorer shares the same code path and caps (a local user can already
fetch anything, but the shared implementation keeps the website safe by
default).

## 7. Implementation plan

New files (pipeline, anthropic_api_package_release/):
- measurement_db.py: get_hf_token, normalize_name, normalize_paper_url (arxiv
  variants, host aliases, scheme/slash), normalize_dataset_url, fuzzy_candidates
  (deterministic, thresholded), build_index (sha-keyed cache under
  benchmarks/mdb_cache/), lookup (priority: paper_url > exact name > fuzzy
  confirm > dataset_source), log_missing + log_hit (JSONL).
- scripts/dataset_analysis/mdb_profile.py: loads the parquets (with
  --local_dir test hook), computes difficulty/discrimination/reliability with
  the response_type branch and small-n guards, samples items stratified by
  difficulty x category, emits JSON on stdout like the sibling scripts.
- relevance_tagger.py: batches items, drives the Haiku fan-out, aggregates tag
  rates; shared by Modes 1 and 2.
- link_explorer.py: the three tools (fetch_url, list_archive,
  preview_data_file) with the Section 6 hardening, plus explore() driving the
  Opus tool loop and emitting the provenance note.
- prompts/mdb_interpret.md, prompts/relevance_tag.md, prompts/link_explore.md,
  prompts/link_interpret.md: each with a unique first line (the test FakeClient
  routes on prompt prefixes); the interpret prompts keep da_interpret.md's
  Datapoint Citations Registry format so compose_prompt.py and the
  DATASET-D{n} contract work unchanged.

Modified files (pipeline):
- run_pipeline.py: _parse_metadata_fields (regex the "- key: value" lines);
  _resolve_dataset_evidence split into the submission-time URL match and the
  post-Step-1 name/fuzzy match (replacing the current _resolve_hf_info call
  site at ~L2479), persisted to dataset_source.json; elicitation gains the
  bundled confirmation/link questions; new CLI flags --paper-url,
  --dataset-link, --dataset-unavailable, --no-measurement-db; Step 5b gains
  the mdb and link branches ahead of the existing org/single logic, with a
  profile cache at benchmarks/mdb_cache/<folder>/script_outputs.json and an
  exploration cache at benchmarks/mdb_cache/links/<urlhash>/; STEP_LABELS
  gains 5b_link_explore and 5b_relevance_tags.
- client.py: new call_tool_loop(model, system, user, tool_specs, tool_handler,
  max_turns=12, step) - client-executed tool loop reusing the existing usage
  recording, rate limiting, tracing, and dry-run printing.
- requirements.txt: add explicit pandas>=2.0, pyarrow>=14.0, rapidfuzz.

Modified files (website):
- client/src/components/RunForm.tsx: paperUrl input; HF fieldset demoted to a
  collapsed details element.
- client/src/api.ts and App.tsx: paper_url in the form data; the near-miss
  confirmation and DatasetLinkForm.tsx (link + unavailable declaration)
  rendered in the elicitation phase; submitDatasetLink().
- server/app.py: paper_url form param; submission-time URL match; the
  1b-databank step after metadata; the bundled pause/resume in both
  step-by-step and auto modes; POST /api/runs/{id}/dataset-link; every exit
  path returns to a scorable status.
- server/dataset_analysis.py: wrappers check_measurement_db, resolve_link,
  run_databank (profile + fan-out + interpret), run_agentic - thin adapters
  over the pipeline modules, so pipeline drift is contained to one file.
- server/db.py + server/logging_gate.py: missing_benchmarks and bank_hits
  tables (run_id REFERENCES runs ON DELETE SET NULL), query-string stripping,
  the writer functions.
- server/mock_anthropic.py: replay routes for the new prompts; a
  measurement_db.json fixture so MOCK_ANTHROPIC=1 stays fully offline.
- DESIGN.md, SECURITY.md (incl. Section 6 items), PrivacyNotice.tsx,
  DEPLOYMENT.md (HF_TOKEN secret + scoping rule).

Tests:
- Pipeline: fixture parquets with hand-computed difficulty/discrimination/
  alpha, including a continuous-score fixture (alpha branch) and a 3-subject
  fixture (insufficient-n guard); test_measurement_db.py (normalizers, lookup
  priority, fuzzy thresholds - near-miss fires / random names don't, sha-keyed
  cache, auth error -> graceful skip, JSONL logs incl. hits);
  test_mdb_profile.py (stats match hand values, strata cover difficulty x
  category, char budget respected); test_relevance_tagger.py (batching, rate
  aggregation, FakeClient routing); test_link_explorer.py (monkeypatched
  requests: SSRF blocks - private IPs, metadata endpoint, redirect-hop
  re-validation, token never sent off-HF; size caps, scheme rejection,
  previews; stubbed SDK client for the tool loop); extend test_pipeline_flow.py
  (no-token silent skip, --no-measurement-db reproduces today's behavior,
  dataset_source.json short-circuit, --dataset-unavailable path, non-tty never
  prompts).
- Website: URL-match-at-submission; 1b branches (found / near-miss confirmed /
  near-miss rejected / not-found / skipped) with rows written correctly;
  dataset-link endpoint (404/409/validation/redaction/query-string stripping/
  declaration); single-pause bundling in both modes; status restoration;
  export/delete of both tables; frontend vitest for the form, the events,
  DatasetLinkForm, and the confirmation.

Build order:
1. Token + data probe FIRST: provision HF_TOKEN, pull DATA_FORMAT.md, download
   the largest folder's response.parquet. Schema truth and the size question
   (batch-accumulation vs load-all) shape mdb_profile.py; do not write it
   blind. (Promoted from v1's "known risks" to step 1.)
2. measurement_db.py + tests (pure logic, no pipeline coupling)
3. mdb_profile.py + fixture parquets + tests
4. relevance_tagger.py + mdb_interpret.md + run_pipeline.py rewiring (mdb
   branch)
5. client.call_tool_loop + link_explorer.py (with Section 6 hardening from the
   first commit, not retrofitted) + link prompts + link branch
6. Website: form + submission URL match + 1b check + databank driver, then the
   bundled elicitation pause, then recording + docs, tests alongside

Verification:
- cd anthropic_api_package_release && python -m pytest tests/ (offline suite
  stays green, including the new tests)
- dry run: python run_pipeline.py paper.pdf --use-case ctx.txt --paper-url
  <url> --dry-run shows the data-bank resolution in the banner
- real FOUND run against a known bank entry (e.g. AfriMed-QA,
  arxiv.org/abs/2411.15640) with the local HF token: expect mode mdb, a
  psychometric dataset_analysis_report.md with tag rates, DATASET-D{n}
  citations in scoring.json
- real NEAR_MISS run (mangle the name, keep a bank-adjacent paper): the
  confirmation question appears in elicitation; yes -> mdb mode
- real NOT-FOUND run: link request appears bundled with elicitation; non-tty
  without --dataset-link/--dataset-unavailable exits with a clear error;
  mdb_missing.jsonl gets the entry; an uncrackable link still completes the
  run without dataset analysis; --dataset-unavailable produces the stub report
- website: python3 -m pytest website/server/tests/; npm test; a manual
  MOCK_ANTHROPIC=1 run exercising found, near-miss, and not-found fixtures,
  including the in-elicitation link form

Known risks:
- schema drift across the ~230 benchmarks.parquet files; the index build uses
  union-of-columns concat and logs folders missing name/paper_url.
- fuzzy threshold tuning: too low spams confirmations, too high defeats the
  purpose. Start conservative (confirm only strong candidates); the miss cost
  is one wasted exploration, not a wrong answer.
- category columns may not exist uniformly in items.parquet; the stratifier
  falls back to difficulty-only strata and says so in the report.
- a data-bank hit overrides an explicit --hf-dataset (the found case uses
  measurement-db only); --no-measurement-db is the escape hatch.
- Haiku tag quality: spot-check tag samples against Sonnet on 2-3 benchmarks
  during build step 4; if disagreement is high, batch size shrinks or the
  tagger moves to Sonnet (still cheap - it is the coverage that matters).
- the bundled elicitation pause touches the website's most stateful path;
  every exit must land on a scorable status or later steps 409 - covered by
  tests.
