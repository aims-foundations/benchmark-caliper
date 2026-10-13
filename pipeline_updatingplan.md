# Pipeline update: measurement-db data bank integration

## 1. What changes and why

The pipeline currently analyzes a benchmark's actual data only if the user happens to supply a HuggingFace dataset ID. We now have a curated data bank on HuggingFace (aims-foundations/measurement-db, gated): 200+ folders, one per benchmark, each with

- benchmarks.parquet: one row of benchmark info (columns include name, paper_url, dataset_source, n_items, n_subjects, has_ground_truth, response_type, ...)
- items.parquet: every test item (content = question text, correct_answer)
- response.parquet: every (model, item, trial, score) observation
- subjects.parquet: the models that were evaluated

The new flow: the user provides a paper URL along with the PDF. The pipeline checks whether the benchmark is already in the data bank. If yes, it analyzes the bank's items and responses as the dataset evidence. If no, it asks the user for a dataset link (mandatory), analyzes whatever that link points to, and records the benchmark in an internal list of uncurated-but-requested benchmarks.

## 2. User inputs

1. Benchmark paper (PDF) - same as today
2. Paper URL - new (e.g. https://arxiv.org/abs/2411.15640)
3. Deployment description - same as today
4. Dataset link - asked only when the benchmark is not found in the data bank (mandatory at that point; any host: HuggingFace, GitHub, Zenodo, Kaggle, OSF, Dataverse, personal website, ...)

## 3. The pipeline, step by step

Step 0 - Slug (Haiku, unchanged)
Derives a short folder name from the deployment description. All outputs for this assessment live under assessments/<paper>/<slug>/.

Step 1 - Metadata (Haiku, unchanged)
Reads PDF pages 1-2, writes metadata.md containing the benchmark name, full name, domain, languages, region. The prompt already emits structured "- name:" and "- full_name:" lines, so the benchmark name for matching comes for free.

Step 2 - Elicitation (Sonnet + user, unchanged)
Sonnet asks 6-10 questions about the deployment context; the user answers; Sonnet writes elicitation_summary.md with priority weights for the six validity dimensions.

Step 2.5 - Data-bank lookup (NEW - deterministic code, no LLM)
Runs right after Step 2.

a. Load a cached index of every folder's benchmarks.parquet from measurement-db.
Built once (downloads ~200 tiny files), cached keyed to the dataset's commit sha, so it refreshes only when the data bank actually changes. Requires HF_TOKEN (the repo is gated). If the token is missing or unauthorized, this step silently skips and the whole pipeline behaves exactly as today.
b. Match two things, both normalized:
    - the paper URL against the paper_url column (arxiv abs/pdf/version variants
    all treated as equal)
    - the benchmark name against the name column ("AfriMed-QA" matches "afrimedqa")
c. FOUND: record which folder matched. No further questions. Continue.
d. NOT FOUND: silently append {name, paper_url, timestamp} to the internal request log (benchmarks/mdb_missing.jsonl on the CLI; a missing_benchmarks SQLite table on the website). Then ask for the dataset link. This is mandatory:
- CLI: input() re-prompts until a valid http(s) URL is given; non-interactive runs must pass --dataset-link or the run exits with a clear error.
- Website: the run pauses with a link form; there is no skip button. If the user walks away the run is eventually swept as abandoned, same as an unanswered elicitation today. The provided link is first checked against the bank's dataset_source column (a match there means we do have the benchmark, so treat as FOUND). Otherwise a huggingface.co/datasets link is parsed into org/name; any other link is kept for the agentic explorer. The link is also added to the request log.
e. The outcome is persisted to dataset_source.json in the assessment folder.

Steps 3-5 (unchanged)
Step 3: per-page Haiku extraction, Sonnet consolidation, benchmark YAML synthesis.
Step 4: deterministic quote verification, region scaffold with placeholders.
Step 5: Sonnet with web search fills the region YAML gaps (up to 10 searches).

Step 5b - Dataset analysis (existing step, gains two new modes)
Produces dataset_analysis_report.md either way. The mode was decided in Step 2.5:

Mode 1 - data-bank mode (new, the FOUND branch):

A deterministic script (scripts/dataset_analysis/mdb_profile.py, no LLM) downloads the matched folder's items.parquet and response.parquet and computes:
- per-item difficulty: fraction of models answering each item correctly; distribution, plus share of items at ceiling (>90% correct, useless for separating strong models) and at floor
- per-item discrimination: does success on this item correlate with a model's overall score (corrected item-total point-biserial)
- overall reliability (KR-20 / Cronbach's alpha)
- a sample of actual item texts, stratified by difficulty, within a char budget
- the benchmarks.parquet registry row (domain, response type, counts, ...)
Then one Sonnet call reads those numbers + sampled items + the elicitation summary and writes the report: are the items relevant to this deployment, is there headroom for the models being deployed, can the benchmark distinguish ability - every claim citing specific items (D1, D2, ...).

Mode 2 - HF-link mode (existing machinery, NOT-FOUND branch with an HF link):

The dataset at the parsed org/name is downloaded, sampled within a char budget, and interpreted by Sonnet against the deployment context. This is exactly today's --hf-dataset behavior, triggered by the pasted link.

Mode 3 - explorer mode (new, NOT-FOUND branch with any other link):

An Opus agent gets three read-only tools - fetch a URL, list an archive's contents, preview a data file (jsonl/csv/tsv/parquet/json) - and up to 12 turns to locate and sample the actual data files behind the link. Size caps on every download, GET-only, never executes fetched content. On success, a Sonnet call interprets the sampled data (same report format). On failure the pipeline warns, records the link in the request log, and continues without dataset analysis - the mandate is on providing the link, not on it being crackable.

Step 6 - Prompt composition (script, unchanged)
Assembles the Opus evaluation prompt: rubric + benchmark YAML + region YAML + elicitation summary + verified quotes + the dataset analysis report (whatever mode produced it), with DATASET-D{n} citation format.

Step 7 - Validity scoring (Opus, unchanged)
One Opus call scores the six dimensions (Input/Output x Ontology/Content/Form, 1-5), now able to cite real data evidence, e.g. "IC = 2: 84% of sampled items are US-clinical questions with no Indonesian coverage [DATASET-D4], and 61% of items are at ceiling for frontier models [DATASET-D7]".

Steps 8-9 (unchanged)
Format the report and build the 7-section review PDF.

## 4. Model assignment

- Deterministic code (no LLM): data-bank index + all matching, all psychometric statistics, quote verification, prompt assembly. The numerically hard parts are deliberately not model tasks.
- Haiku: existing duties only (page extraction, metadata). The bank match uses Haiku's extracted name only as the secondary key; the paper URL is exact-match and model-independent, and a false name miss just costs one extra question.
- Sonnet: the interpretation calls (mdb_interpret, link_interpret) - reading precomputed stats and samples against the deployment summary, the same class of task as today's da_interpret which already runs Sonnet in production.
- Opus: Step 7 scoring, plus the link explorer. The explorer is the hardest new LLM task and its worst failure (confidently sampling the wrong files) is silent downstream; Opus is only ~1.7x Sonnet's price on this bounded step, and the step only fires on bank-miss runs. The docs' "Opus: exactly one call" claim gets updated to name both call sites.

## 5. Website flow

Same logic, browser plumbing:
- The run form gains a Paper URL field (recommended, prominent). The existing HF dataset ID field moves into a collapsed "Advanced" section as a manual override.
- After Step 1, a new progress step "1b - checking measurement data bank" appears, using the server's own HF_TOKEN (never the user's Anthropic key). Found / not-found / skipped is shown live via SSE.
- On FOUND, the dataset-analysis phase runs the psychometric analysis automatically; the user never supplies a dataset ID.
- On NOT FOUND, the run pauses right after the databank check - in the same phase where the user is answering elicitation questions, before any expensive steps - and shows a form: paste a dataset link (any host). No skip button. Submitting resumes the run via a new POST /api/runs/{id}/dataset-link endpoint and a new awaiting-dataset-link SSE event/phase.
- Not-found benchmarks land in a new missing_benchmarks SQLite table (benchmark name, paper URL, link, run id, timestamp) written through logging_gate (the single privacy chokepoint), tier 1, redact() applied, run linkage severed on delete-my-data, included in /export. Never shown in any UI. DESIGN.md, SECURITY.md and the privacy notice get updated to document this collection.

## 6. Implementation plan

New files (pipeline, anthropic_api_package_release/):
- measurement_db.py: get_hf_token, normalize_name, normalize_paper_url, build_index (sha-keyed cache under benchmarks/mdb_cache/), lookup (priority: paper_url > name > dataset_source), log_missing (JSONL).
- scripts/dataset_analysis/mdb_profile.py: loads the four parquets (with --local_dir test hook), computes difficulty/discrimination/reliability, samples items stratified by difficulty, emits JSON on stdout like the sibling scripts.
- link_explorer.py: the three tools (fetch_url, list_archive, preview_data_file) with size/scheme caps, plus explore() driving the Opus tool loop.
- prompts/mdb_interpret.md, prompts/link_explore.md, prompts/link_interpret.md: each with a unique first line (the test FakeClient routes on prompt prefixes); the interpret prompts keep da_interpret.md's Datapoint Citations Registry format so compose_prompt.py and the DATASET-D{n} contract work unchanged.

Modified files (pipeline):
- run_pipeline.py: _parse_metadata_fields (regex the "- key: value" lines);
  _resolve_dataset_evidence (the Step 2.5 logic above, persisted to
  dataset_source.json); new CLI flags --paper-url, --dataset-link,
  --no-measurement-db; the resolution call moves from before Step 1 (current
  _resolve_hf_info at ~L2479) to right after step_2_summary (~L2595); Step 5b
  gains the mdb and link branches ahead of the existing org/single logic, with a
  profile cache at benchmarks/mdb_cache/<folder>/script_outputs.json and an
  exploration cache at benchmarks/mdb_cache/links/<urlhash>/; STEP_LABELS gains
  5b_link_explore.
- client.py: new call_tool_loop(model, system, user, tool_specs, tool_handler,
  max_turns=12, step) - client-executed tool loop reusing the existing usage
  recording, rate limiting, tracing, and dry-run printing.
- requirements.txt: add explicit pandas>=2.0 and pyarrow>=14.0 (currently only
  transitive via datasets).

Modified files (website):
- client/src/components/RunForm.tsx: paperUrl input; HF fieldset demoted to a
  collapsed details element.
- client/src/api.ts and App.tsx: paper_url in the form data; the new
  awaiting-dataset-link event and submitDatasetLink(); new DatasetLinkForm.tsx.
- server/app.py: paper_url form param; the 1b-databank step after metadata; the
  dataset-link pause/resume in both step-by-step and auto modes; the new
  POST /api/runs/{id}/dataset-link endpoint; status awaiting_dataset_link must
  return to a scorable status on every exit path or /compose-prompt and /score
  will 409.
- server/dataset_analysis.py: wrappers check_measurement_db, resolve_link,
  run_databank, run_agentic - thin adapters over the pipeline modules, so
  pipeline drift is contained to one file.
- server/db.py + server/logging_gate.py: missing_benchmarks table (run_id
  REFERENCES runs ON DELETE SET NULL) and the two writer functions.
- server/mock_anthropic.py: replay routes for the new prompts; a
  measurement_db.json fixture so MOCK_ANTHROPIC=1 stays fully offline.
- DESIGN.md, SECURITY.md, PrivacyNotice.tsx, DEPLOYMENT.md (HF_TOKEN secret).

Tests:
- Pipeline: fixture parquets with hand-computed difficulty/discrimination/alpha;
  test_measurement_db.py (normalizers, lookup priority, sha-keyed cache, auth
  error -> graceful skip, JSONL log); test_mdb_profile.py (stats match hand
  values, char budget respected); test_link_explorer.py (monkeypatched requests:
  size caps, scheme rejection, previews; stubbed SDK client for the tool loop);
  extend test_pipeline_flow.py (no-token silent skip, --no-measurement-db
  reproduces today's behavior, dataset_source.json short-circuit, non-tty never
  prompts).
- Website: 1b branches (found / not-found / skipped) with the missing-row written
  only on not-found; dataset-link endpoint (404/409/validation/redaction); pause
  and resume in both modes; status restoration; export/delete of
  missing_benchmarks rows; frontend vitest for the form, the event, and
  DatasetLinkForm.

Build order:
1. measurement_db.py + tests (pure logic, no pipeline coupling)
2. mdb_profile.py + fixture parquets + tests
3. run_pipeline.py rewiring + mdb branch + mdb_interpret.md
4. client.call_tool_loop + link_explorer.py + link prompts + link branch
5. Website: form + 1b check + databank driver, then the link pause, then
   recording + docs, tests alongside

Verification:
- cd anthropic_api_package_release && python -m pytest tests/ (offline suite
  stays green, including the new tests)
- dry run: python run_pipeline.py paper.pdf --use-case ctx.txt --paper-url <url>
  --dry-run shows the data-bank resolution in the banner
- real FOUND run against a known bank entry (e.g. AfriMed-QA,
  arxiv.org/abs/2411.15640) with the local HF token: expect mode mdb, a
  psychometric dataset_analysis_report.md, DATASET-D{n} citations in scoring.json
- real NOT-FOUND run: link prompt re-asks until a valid URL; non-tty without
  --dataset-link exits with a clear error; mdb_missing.jsonl gets the entry; an
  uncrackable link still completes the run without dataset analysis
- website: python3 -m pytest website/server/tests/; npm test; a manual
  MOCK_ANTHROPIC=1 run exercising both the found and not-found fixtures,
  including the mid-run link form

Known risks:
- response.parquet size for the largest bank entries is unverified; mdb_profile.py
  needs a pyarrow batch-accumulation fallback, exercised early against a real
  large folder.
- schema drift across the 200+ benchmarks.parquet files; the index build uses
  union-of-columns concat and logs folders missing name/paper_url.
- a data-bank hit overrides an explicit --hf-dataset (per the decision that the
  found case uses measurement-db only); --no-measurement-db is the escape hatch.
- the awaiting_dataset_link status must return to a scorable status on every exit
  path on the website, or later steps 409 - covered by tests.
