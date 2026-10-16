# Website design and operations

This document describes the website implementation in this checkout, its user flows, data handling, and operating requirements. Deployment verification is separate; source changes do not establish what is currently live.

It is the single source of truth for the team. It is paired with [SECURITY.md](SECURITY.md), which is the concrete checklist we audit before each deploy. Every claim in this document should map to a verifiable item in SECURITY.md.

If you only have ten minutes, read sections **1 (Overview)**, **4 (Security)**, and **5 (Logging)**.

---

## 1. Overview

### What the website does

The homepage offers two tools. **Benchmark validity analysis** (`/caliper`) starts with a benchmark paper PDF and deployment context, produces a structured six-dimension assessment, and continues into the required item-analysis stage within the same report. Users confirm matching items from the Measurement Data Bank or an upload, generate criteria from that assessment, inspect a pilot, and classify the full snapshot before the analysis is marked complete. **Goal-conditioned item assessment** (`/items`) independently ranks a reproducible sample from the Measurement Data Bank against a deployment description.

Saved `/run/{run_id}` reports and gallery assessments provide the same item-analysis continuation. `/item-analysis` remains a compatibility entry into the main Caliper flow; it does not present a third top-level tool.

### Who it is for

Researchers, practitioners, designers, and policymakers who need to know whether an AI benchmark developed in one cultural context will produce valid signal in a different one. The intended user base spans academia, NGOs, industry, and government, including users in regions with strong data-protection norms.

### What the website does not do

- It does not host an LLM. Users supply an Anthropic key for benchmark assessment and an OpenAI key for item analysis or goal-conditioned item assessment.
- It does not persist provider keys on the server. Anthropic browser storage and the memory-only OpenAI key policy are described separately below.
- It does not require an account in v0.
- Item prevalence does not automatically revise the original benchmark scores or validate model judgments against human labels.

### Relationship to the existing pipeline

The benchmark and item-analysis stages reuse [anthropic_api_package_release/](../anthropic_api_package_release/), while the separate item-review tool reuses [bayesian_auditing/](../bayesian_auditing/). FastAPI adds browser job lifecycles, report resolution, dataset selection and upload, access control, and exports. Shared code does not guarantee identical model outputs across runs.

---

## 2. Stack

### Backend: FastAPI (Python)

Chosen because the pipeline is already Python. FastAPI imports the existing pipeline modules directly — no porting, no dual-implementation maintenance burden, no risk of behavior drift between the website and the paper. FastAPI also has native async support, which we need for streaming progress while the per-page Haiku fan-out runs.

Alternatives considered and rejected:
- **Next.js / TypeScript backend:** would require porting every prompt loader, every script, every YAML synthesis path. Two implementations, double the maintenance, real risk of drift.
- **Streamlit / Gradio:** server-side session state makes BYOK harder to do safely; UX is constrained.
- **Flask:** works, but no native async, no Pydantic validation. FastAPI is strictly better for this shape of app.

### Frontend: Vite + React

Chosen for a multi-step interactive flow: dynamic elicitation question rendering, live progress streaming, file upload, structured result display. SSR is unnecessary because every page is user-specific and behind interaction. Vite is simpler than Next.js without sacrificing the React ecosystem.

Alternatives considered and rejected:
- **Plain HTML + HTMX:** works for static forms, but the dynamic-question UX is awkward.
- **Next.js:** SSR adds complexity without benefit for our use case.

### Streaming: Server-Sent Events (SSE)

The pipeline interaction is one-way: the server emits step-completion events while the user waits. SSE is plain HTTP, simpler than WebSockets, no sticky-session requirements at the load balancer.

### Storage

- **SQLite** for the structured event log (tier 1 + tier 2 in the four-tier model below).
- **Local filesystem** for blob storage (tier 3 full content), with TTL via cron.
- **Benchmark tuple workspaces** retain the report's deployment and assessment artifacts for saved-report continuation, independently of optional trace logging, under the existing workspace retention policy.
- **Private temporary item-run directories** hold the connected dataset, copied assessment, generated criteria, classifications, and exports. Their in-memory access registry and one-hour expiry are separate from benchmark retention.
- For v1+: migrate to Postgres + Cloudflare R2 once we have multiple concurrent users or want a real dashboard.

---

## 3. How the website works (user flow)

```
USER                     FRONTEND                  BACKEND                 ANTHROPIC API
 │                          │                         │                         │
 │  paste API key           │                         │                         │
 ├─────────────────────────►│                         │                         │
 │                          │                         │                         │
 │  upload paper PDF        │                         │                         │
 │  + deployment desc       │                         │                         │
 ├─────────────────────────►│                         │                         │
 │                          │  POST /run              │                         │
 │                          │  X-Anthropic-Key: ...   │                         │
 │                          ├────────────────────────►│                         │
 │                          │                         │  Steps 0-2 (slug,       │
 │                          │                         │  metadata, elicit Qs)   │
 │                          │                         ├────────────────────────►│
 │                          │                         │◄────────────────────────┤
 │                          │  SSE: questions ready   │                         │
 │                          │◄────────────────────────┤                         │
 │  answer questions        │                         │                         │
 ├─────────────────────────►│  POST /run/{id}/answers │                         │
 │                          ├────────────────────────►│                         │
 │                          │  SSE: step 3a, 3b, ...  │  Steps 3-7 (PDF extract,│
 │                          │◄────────────────────────┤  YAML synth, web search,│
 │                          │  (live progress)        │  scoring) — async tail  │
 │                          │                         ├────────────────────────►│
 │                          │                         │◄────────────────────────┤
 │                          │  SSE: scoring complete  │                         │
 │  view + download report  │◄────────────────────────┤                         │
 │◄─────────────────────────┤                         │                         │
```

The sequence above covers the benchmark-assessment stage. Its report leads
directly into item analysis before the full workflow is complete.

### Stage by stage

1. **Key entry.** User pastes their Anthropic API key. The browser stores it in `sessionStorage` (cleared when the tab closes). An optional "remember on this device" toggle moves it to `localStorage`. The key is masked on input.

2. **Pre-flight validation.** Browser sends a single 1-token "ping" request through our backend to confirm the key works. No prompt or response body is logged for this call beyond status (success / auth-failed).

3. **PDF upload + deployment description.** User uploads a paper (capped at 50 MB) and types a free-form description of the deployment they are considering.

4. **Steps 0–2 run on the server.** The server proxies three pipeline calls to Anthropic: derive a slug, extract metadata from pages 1–2, and generate elicitation questions. Roughly 30 seconds. Progress streams to the browser via SSE.

5. **User answers elicitation questions.** Generated questions are rendered as a form. User types answers; the client posts them back. The server runs Step 2-summary and shows the result.

6. **User chooses benchmark run mode.** Below the summary, the user chooses automatic processing (default) or step-by-step review. The current UI has no report-notification email field. Optional email API support remains for compatible clients and does not gate progress.

7. **Steps 3–7 run on the server.** PDF fan-out across pages (Haiku), consolidation (Sonnet), benchmark YAML synthesis, region YAML synthesis, optional web search, prompt assembly, and Opus scoring. Roughly 3–7 minutes total.
   - **Auto mode (default):** A `POST /api/runs/{id}/auto-run` enqueues a background task that drives the benchmark phases using the API key + PDF bytes already stashed in the per-run in-memory store. Progress events flow into a ring buffer that the browser can tail via SSE (`GET /api/runs/{id}/events`). Closing the tab does not stop the background benchmark job. Item-analysis model calls still require separate actions after the benchmark report is ready.
   - **Step-by-step mode:** Same per-phase SSE endpoints as before (`/extract`, `/region`, `/score`), but the user is not asked to re-upload the PDF — the server reuses the bytes from step 3. The email, if provided, is still sent when scoring completes.

8. **Benchmark report and dataset connection.** The report appears inline with downloads and the next required item-analysis stage. `/run/{run_id}` fetches the saved benchmark report and offers the same continuation. The run ID remains the bearer credential for the original report and its assessment setup, matching `/export`; public gallery reports use allowlisted gallery IDs. The server searches the Measurement Data Bank using the saved paper metadata: paper and dataset identifiers, names and aliases, then fuzzy name matches. Deployment descriptions do not influence identity matching. The user reviews the candidate’s match reasons, version, scope, item count, and source, then explicitly confirms the benchmark and snapshot. Search supports correcting a suggestion; CSV/JSON upload remains available when no usable source is found. Changing the source clears confirmation. Uploads allow up to 10 MiB and 50,000 rows; nonempty `content` is required, `item_id` is generated when omitted, and `reference_answer` is optional.

9. **Criteria, pilot, and full item analysis.** The server copies the report's exact deployment, scores, elicitation summary, and available dataset report into a new private item run. Connecting a dataset never selects its historical assessment or supplied criteria. An explicit action with an OpenAI key generates fresh criteria using GPT-6 Luna. Users review those criteria, explicitly classify the first 100 items (or all items for a smaller dataset), inspect the checkpoint, and explicitly continue through the remaining items. Full classification marks the workflow complete. Distributions and per-item evidence supplement the unchanged six-dimension scores; criteria, labels, summary, HTML report, and a blind human-review worksheet can be downloaded.

10. **Cleanup.** The benchmark job drops its in-memory API key and PDF bytes when it ends; a safety-net sweeper removes stale entries after one hour. Existing 90-day benchmark workspace and trace retention remain separate. Item runs expire one hour after their last phase ends and do not survive a server restart; their input copies and outputs are removed on normal shutdown. Users must download item outputs before expiry.

### Starting at the item stage

`/caliper?start=items` offers existing gallery/saved-report reuse and direct
entry with new deployment requirements. Both are starting points within the
same validity-analysis workflow. Existing assessments retain their original
context and findings. Direct context is separately validated and frozen; its
identifier hashes all normalized user requirement fields.

Direct generation uses an evidence registry of explicit requirements and the
framework, plus the actual dataset profile and sample items. It does not run
paper analysis, elicitation synthesis, regional research, or benchmark scoring.
The item generator uses the same fixed classifier roster and structural checks,
including an explicit task-requirements reference for task coverage. Reports
mark the benchmark assessment as not run; Input Form and Output Form remain
unassessed and no six-dimension scores are generated. Both paths use confirmed
dataset selection, reviewed criteria, a pilot, and full-snapshot classification.

### Free walkthrough

`/caliper?demo=mathdial` replays the cached MathDial benchmark assessment and
continues into a browser-only item walkthrough. The direct
`/caliper?demo=mathdial&stage=items` URL reconstructs the cached report on refresh
and restores the separate demo item-stage state. Both stages share the original
MathDial deployment context. A ten-dialogue public source sample with authored
example judgments illustrates confirmation, criteria, a four-item pilot,
review, and completion of the remaining sample. The demo never creates a live
item job, requests provider keys, or claims to analyze the entire benchmark.
Real gallery links continue to use Data Bank discovery and paid model actions.

### Assessment-to-item boundary

`GET /api/item-analysis/assessment?kind=run&id={run_id}` (or `kind=gallery`)
resolves an existing assessment and returns its context, benchmark identity,
suggested Data Bank sources, catalog status, and upload limits without model
calls. `GET /api/item-analysis/sources` accepts the same assessment reference
and a `q` search string for finding another candidate. `POST /api/item-analysis/runs/from-assessment`
accepts multipart `assessment_kind`, `assessment_id`, `benchmark_confirmed=true`,
and exactly one of `source_id` or `items_file`, with `X-OpenAI-Key`. Data Bank
selections require the displayed `source_revision`. The backend resolves
assessment artifacts itself, rejects unconfirmed or stale sources, validates uploads, and
starts fresh criteria generation. Subsequent item endpoints require an independent
`X-Review-Token`, stored in the tab alongside the item run ID and scoped to its
original assessment.

The older prepared-example `/api/item-analysis/catalog` and
`POST /api/item-analysis/runs` API remains for compatibility, including
supplied-criteria previews. It is not a
standalone homepage tool and does not provide the context for report continuation.

---

## 4. Security

This section is the *narrative*. The verifiable checklist is in [SECURITY.md](SECURITY.md). Both must be kept in sync.

### Threat model

We worry, in priority order, about:
1. **API key theft** — the single biggest blast radius if it happens.
2. **User content leakage** — unpublished benchmarks, internal deployment plans.
3. **Cross-user contamination** — one user's data appearing in another user's session.
4. **Service availability** — denial-of-service or runaway cost from abuse.
5. **Supply-chain compromise** — a bad npm/pypi update introducing exfiltration.

We do not currently defend against:
- A user's own machine being compromised (out of scope).
- Anthropic's own systems being breached (out of our hands).
- A targeted nation-state actor (proportional to risk; we are not that target).

### How we keep API keys safe

The principle: **the server never writes the key to disk, ever, and only holds it in memory while it is actively needed for a run.**

The bullets below describe the Anthropic benchmark stage. Item-stage OpenAI keys
travel in `X-OpenAI-Key` and stay in frontend memory and the active server phase;
they are never put in browser storage. Only the independent item-run access
token is saved in session storage. Criteria generation and each classification
phase require explicit actions; a required product stage does not imply consent
to start paid calls. See [SECURITY.md](SECURITY.md) for item-run boundaries.

- The key lives in the user's browser only (`sessionStorage` by default, `localStorage` opt-in).
- The key is sent in an `X-Anthropic-Key` header on each request.
- For step-by-step mode the key is captured in the request handler's closure and goes out of scope when the SSE response completes — same posture as v0.2.
- For auto mode the key is additionally placed in a per-run in-memory entry (`active_runs.store`) so a background task can keep making Anthropic calls after the user's tab closes. The entry is keyed by run_id, holds the key + PDF bytes only, and is dropped on run completion (success or failure) by the orchestrator. A safety-net sweeper drops any stale entries older than one hour.
- The active-runs store is process-local memory only — nothing it holds is written to the database, the blob store, or any log. The redaction gate remains the only path to disk; grep for `log_step` / `start_run` / `end_run` to audit.
- Logging is configured to redact the `X-Anthropic-Key` header. Pipeline traces strip it before any persistence.
- The key is never put in a URL, a cookie, an analytics payload, or any other channel.
- Strict CSP prevents third-party scripts from reading `localStorage`.

### How we keep user content safe

User content (PDFs, deployment descriptions, elicitation answers, scoring outputs) is:
- Held in a per-request temp directory for the duration of the run.
- Streamed to the user's browser as it's produced.
- Persisted server-side only as far as the four-tier logging model allows (section 5).
- Never combined with cross-user data; every storage key includes the run ID.

### Browser-side hardening

- Strict `Content-Security-Policy: script-src 'self'; default-src 'self'`. No inline scripts, no eval.
- `X-Frame-Options: DENY` and `frame-ancestors 'none'` to block clickjacking.
- `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`.
- No third-party scripts on any page that handles keys or user content.
- Subresource Integrity hashes if any external script is ever introduced.
- Model-generated content (LLM responses, scoring) is rendered as escaped text, never as HTML.

### Network security

- TLS 1.2+ only, modern cipher suites.
- HSTS with preload.
- HTTP redirects to HTTPS at the edge.
- CAA DNS records pin certificate authorities.

### Server hardening

- The process runs as a non-root user with restricted filesystem permissions.
- 50 MB upload cap; per-IP rate limiting.
- No backdoor admin endpoints reachable without auth.
- Per-request temp directories; deleted on completion regardless of success.

### Supply chain

- Pinned lockfiles committed.
- Dependabot/Renovate proposes updates; never auto-merged.
- A pre-commit secret scanner blocks commits containing `sk-ant-` patterns.
- Frontend dependencies on key-handling pages are minimized and audited per release.

---

## 5. Logging and observability

The following model describes benchmark-stage trace logging. Report artifacts
in benchmark workspaces and temporary item-run inputs and outputs have the
separate lifecycles described above; they are not opt-in trace blobs. API keys
are excluded from all server persistence.

### The four-tier model

| Tier | Content | Retention | Where stored |
|------|---------|-----------|--------------|
| **0 — never logged** | API keys, auth headers | Never | Nowhere |
| **1 — operational metadata** | Run ID, step name, timestamps, model, token counts, cost, latency, error class | Forever | SQLite (`runs`, `steps` tables) |
| **2 — fingerprints** | SHA-256 hashes of inputs, page count, language, region | ~1 year | SQLite (`steps.input_hash` etc.) |
| **3 — full content** | Full prompts, full LLM responses, PDF text, deployment description, elicitation Q&A | 90 days, then auto-deleted | Filesystem blobs (`assessments/<run_id>/`) |

Tier 1 and 2 also feed a `daily_aggregates` table (cost per model per day, error rates, run counts) which is kept forever. It is small, safe, and the basis for long-term trend analysis after tier-3 data is purged.

### The redaction gate

A single Python module is the only path to disk. Every log write — every step completion, every error, every blob save — goes through it. It:
1. Strips API keys (regex on `sk-ant-` patterns) and `Authorization` headers.
2. Computes SHA-256 fingerprints of inputs.
3. Classifies the event as tier 1, 2, or 3 and routes it to the correct store.
4. Strips known PII patterns (email, phone) from tier-3 prompts before persistence.
5. Honors the user's opt-out flag — if set, only tiers 1 and 2 are written.

Because there is exactly one chokepoint, the privacy guarantee is *auditable*: grep the codebase for "writes to disk," confirm the gate is the only path. This is item 5 in `SECURITY.md`.

### Cost tracking

The Anthropic API returns `usage.input_tokens` and `usage.output_tokens` on every response. These are tier 1, always logged. Per-run cost = sum across steps of `tokens × price_per_million`. A `model_prices.py` file holds the per-model rates, updated when Anthropic changes prices.

This gives us, for free:
- Cost per run (mean, p50, p95)
- Cost per step per model — confirms the Haiku/Sonnet/Opus routing is paying off
- Daily, weekly, monthly spend, broken down by step or model
- Failed-run rate per step (where we are wasting money)
- Step latency distributions

### Schema

```sql
CREATE TABLE runs (
  run_id              TEXT PRIMARY KEY,
  started_at          TIMESTAMP,
  ended_at            TIMESTAMP,
  status              TEXT,        -- success | failed | abandoned
  total_input_tokens  INTEGER,
  total_output_tokens INTEGER,
  total_cost_usd      REAL,
  pipeline_version    TEXT,
  -- INTEGER (0/1) since SQLite has no native BOOLEAN. Default 0 enforces
  -- the opt-out policy; logging_gate.start_run always sets it explicitly.
  user_opted_in_full  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE steps (
  run_id        TEXT,
  step_name     TEXT,             -- "3a-extract", "7-score", etc.
  model         TEXT,
  started_at    TIMESTAMP,
  latency_ms    INTEGER,
  input_tokens  INTEGER,
  output_tokens INTEGER,
  cost_usd      REAL,
  status        TEXT,
  error_class   TEXT,
  input_hash    TEXT,             -- tier 2
  output_hash   TEXT,             -- tier 2
  blob_key      TEXT              -- tier 3 pointer; NULL if user opted out
);

CREATE TABLE daily_aggregates (
  date           DATE,
  model          TEXT,
  step_name      TEXT,
  run_count      INTEGER,
  total_tokens   INTEGER,
  total_cost_usd REAL,
  error_count    INTEGER
);
```

### Retention enforcement

A nightly cron job:
1. Deletes blob objects older than 90 days.
2. Sets the corresponding `steps.blob_key` to NULL.
3. Rolls up the previous day's `steps` rows into `daily_aggregates`.

The cron's correctness is a checklist item in `SECURITY.md` (test by inserting a 91-day-old blob and confirming removal).

---

## 6. Privacy and legal

### What we collect, plainly

- **Always:** which steps ran, when, on which model, with how many tokens, at what cost, and whether they succeeded. Hashed fingerprints of your inputs (so we can tell two runs are on the same paper without storing the paper). No name, no IP-tied identity.
- **If an API client requests a report email:** the supplied email address and delivery timestamp are stored on the run's row and removed when the run is deleted. The current browser flow does not collect this address.
- **For report continuation:** the benchmark workspace retains deployment and assessment artifacts under its existing retention policy. An item run separately holds a copy of those artifacts, the connected or uploaded dataset, criteria, and classifications until its temporary expiry.
- **Only if you explicitly opt in (per run):** the full text of your deployment description, elicitation answers, and the LLM prompts and responses for that run. Stored for 90 days then automatically deleted. Default is **off**.
- **Never:** your Anthropic API key. Your authentication credentials.

### How users control it

- **Default is no tier-3 storage.** On every run we log operational metadata (which steps ran, tokens, cost, hashes) by default. We do **not** log prompts or responses unless the user explicitly opts in for that run via a per-run checkbox.
- **Consent gate before first use.** The first time a user visits, a modal explains what we log on every run, what we would only log with explicit opt-in, and the user's data-subject rights. They acknowledge before accessing the tool. The acknowledgment is stored in their browser's localStorage; clearing browser data resets it.
- **Per-run opt-in checkbox.** A "Allow storing my prompts and responses for 90 days" checkbox on the run page. Default: unchecked. If checked, full content is stored for 90 days then auto-deleted.
- **Export-my-data endpoint.** Given a run ID, returns the full trace as JSON.
- **Delete-my-data endpoint.** Given a run ID, removes both database rows and blob objects. We treat this as a hard delete, not a soft delete.

This default — "operational metadata yes, content no" — was decided 2026-05-04 with Sang and Rudy. The reasoning: the public-facing tool should not be optimised for our research data collection; that is a separate workstream with its own consent flow.

### Legal frameworks we follow

We do not have legal counsel as of writing. The commitments below are best-effort alignment with common privacy frameworks; they should be reviewed by counsel before public launch.

- **GDPR (EU users).** We provide:
  - A privacy policy in plain language stating what we collect and why.
  - A lawful basis for processing: legitimate interest for tier 1 and tier 2 operational data; consent (the opt-in default, plus opt-out toggle) for tier 3.
  - Right to access (export-my-data), right to erasure (delete-my-data), right to data portability (JSON export).
  - Data minimization: per-purpose retention, with tier-3 capped at 90 days.
- **CCPA (California).** Privacy policy meets disclosure requirements. We do not sell user data.
- **University context.** If the data is used in any publication, we will obtain explicit per-user consent at run time, separate from the operational logging consent. IRB review is sought before any such publication.

### What users see

A short privacy notice linked from the footer of every page, in plain language. Each claim in the notice maps to a verifiable item in `SECURITY.md`.

---

## 7. Operations

### Hosting

A reputable provider. Current candidates: Fly.io, Render, Vercel (frontend) + Fly/Render (backend). Specifically not a self-managed VM, because their security teams are larger than ours.

### Accounts and access

- **2FA enforced** on every account that can deploy, push code, change DNS, or access hosting.
- **Least privilege** for deploy credentials: deploy and rollback only; cannot delete the project or read user data.
- **Production secrets** stored in the hosting provider's secret manager. No production secrets in the repo, ever (verified by the pre-commit secret scanner).
- **Quarterly secret rotation** with a calendar reminder.

### Monitoring

- **Uptime ping** every minute; alert fires within 2 minutes of an outage.
- **Error tracking** (Sentry-style) with PII scrubbing. Trigger an intentional error during setup to confirm scrubbing works.
- **Cost dashboard** showing daily/weekly spend per model, derived from `daily_aggregates`.
- **Anomaly alerts** for cost spikes, error-rate spikes, and unusual traffic patterns.

### Deploy

- All changes go through a pull request with at least one reviewer.
- CI runs lint, typecheck, unit tests, and the redaction-gate test suite before merge.
- Deploys are pushed from `main`; manual deploys are off.
- Every deploy re-checks the `SECURITY.md` checklist.

### Incident response

A short runbook in this repo describes:
1. **Discovery** — alerts, user reports, security@ email.
2. **Triage** — severity classification (key leak = sev-1, content leak = sev-2, availability = sev-3).
3. **Containment** — how to take the service offline if needed; how to revoke credentials.
4. **User notification** — within 72 hours of confirmed user-data breach, per GDPR.
5. **Postmortem** — root cause, timeline, action items.

### Quarterly review

Every 90 days the team reviews `SECURITY.md` end-to-end, confirms each item is still verifiable, updates the review log at the bottom of that file, and rotates any production secrets.

---

## 8. Roadmap

### v0 — minimum viable, locked-down

- BYOK only; no accounts.
- SQLite + local filesystem.
- FastAPI backend + Vite/React frontend.
- The redaction gate, the four-tier schema, the 90-day cron.
- The codebase items in `SECURITY.md` are green; deploy-dependent items (custom domain, hosting accounts, edge rate limiting, monitoring) remain pending until a public host is chosen.
- Deployed behind HTTPS on a single hosting provider.

### v1 — observability and growth

- Migrate SQLite → Postgres.
- Migrate local filesystem → Cloudflare R2 (or equivalent object store with lifecycle rules).
- Add self-hosted Langfuse for the dashboard layer.
- Add cost dashboards visible to admins.
- Consider OpenTelemetry GenAI semantic conventions for portability.

### v1+ — optional features

- Optional capped-key tier (we hold a small budget, give users a $3 daily limit). Requires accounts; introduces JOSE-style signed session tokens.
- Optional "preserve indefinitely" opt-in for users who want to cite their runs.
- User-research collection: with explicit per-run consent, opt-in to share specific runs for paper improvement.
- Free-tier integration (Google Gemini's free tier, if added) to lower the barrier for first-time users.

### Things we do not plan to build

- An "admin views all user content" UI. There is no such role; if we need to debug, we use redacted traces.
- A multi-tenant accounts system in v0. Once we add it, we redo this design doc with the new threat model.
- A "bring your own database" feature. Out of scope.

---

## 9. Glossary

- **BYOK** — bring your own key. The user supplies their own Anthropic API credential.
- **Tier 0–3** — sensitivity classification of logged data; see section 5.
- **Redaction gate** — the single Python module that is the only path to disk; see section 5.
- **SSE** — Server-Sent Events; one-way HTTP streaming from server to browser.
- **CSP** — Content-Security-Policy; HTTP header that restricts what scripts and resources a page can load.
- **HSTS** — HTTP Strict Transport Security; HTTP header that forces TLS.
- **JOSE** — JSON Object Signing and Encryption; the spec underneath signed/encrypted JWTs. Not used in v0.
- **SRI** — Subresource Integrity; pinned hashes for externally loaded scripts.
- **CAA** — Certification Authority Authorization; DNS record that pins which CAs can issue certs for our domain.
