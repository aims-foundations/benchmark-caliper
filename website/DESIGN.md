# Website design and operations

This document describes how the validity-analyzer website is built, how it works, how user data and credentials are handled, the legal and ethical commitments we make, and how we operate it day to day.

It is the single source of truth for the team. It is paired with [SECURITY.md](SECURITY.md), which is the concrete checklist we audit before each deploy. Every claim in this document should map to a verifiable item in SECURITY.md.

If you only have ten minutes, read sections **1 (Overview)**, **4 (Security)**, and **5 (Logging)**.

---

## 1. Overview

### What the website does

The website is a public-facing interface to the validity-analysis pipeline described in the paper *"Validity Analysis when Porting Benchmarks Across Cultures and Regions."* A user uploads a benchmark paper PDF, describes the deployment context they are considering, answers a small set of elicitation questions, and receives a structured 6-dimension validity assessment with citations and remediation suggestions.

### Who it is for

Researchers, practitioners, designers, and policymakers who need to know whether an AI benchmark developed in one cultural context will produce valid signal in a different one. The intended user base spans academia, NGOs, industry, and government, including users in regions with strong data-protection norms.

### What the website does not do

- It does not host an LLM. The user supplies their own Anthropic API key (BYOK).
- It does not store the user's API key.
- It does not require an account in v0.
- It does not provide a database of pre-computed assessments. Each run is one user's deployment.

### Relationship to the existing pipeline

The website is a thin web wrapper over [anthropic_api_package/](../anthropic_api_package/). The pipeline itself — prompts, model routing, scripts, ICL templates — is unchanged. The website orchestrates the existing pipeline through a FastAPI backend; it does not reimplement any pipeline logic. This means **the website and the paper give identical answers for identical inputs**.

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

### Stage by stage

1. **Key entry.** User pastes their Anthropic API key. The browser stores it in `sessionStorage` (cleared when the tab closes). An optional "remember on this device" toggle moves it to `localStorage`. The key is masked on input.

2. **Pre-flight validation.** Browser sends a single 1-token "ping" request through our backend to confirm the key works. No prompt or response body is logged for this call beyond status (success / auth-failed).

3. **PDF upload + deployment description.** User uploads a paper (capped at 50 MB) and types a free-form description of the deployment they are considering.

4. **Steps 0–2 run on the server.** The server proxies three pipeline calls to Anthropic: derive a slug, extract metadata from pages 1–2, and generate elicitation questions. Roughly 30 seconds. Progress streams to the browser via SSE.

5. **User answers elicitation questions.** Generated questions are rendered as a form. User types answers; the client posts them back. This is the user-interaction point.

6. **Steps 3–7 run on the server.** PDF fan-out across pages (Haiku), consolidation (Sonnet), benchmark YAML synthesis, region YAML synthesis, optional web search, prompt assembly, and Opus scoring. Roughly 3–7 minutes total. Each step emits an SSE progress event.

7. **Result delivery.** The scoring JSON and a rendered markdown report stream to the browser. The user can download both. Their browser is the canonical copy; we keep a server-side copy under the retention policy in section 5.

8. **Cleanup.** The per-request temp directory holding the uploaded PDF is deleted as soon as the run finishes (success or failure).

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

The principle: **the server never sees, stores, or remembers the key. It is a transparent proxy for credentials.**

- The key lives in the user's browser only (`sessionStorage` by default, `localStorage` opt-in).
- The key is sent in an `X-Anthropic-Key` header on each request and discarded server-side as soon as the call completes.
- Server-side, an Anthropic client is instantiated per-request inside the handler scope. No global state, no caches, no in-memory dicts holding keys.
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

We log a lot — but in tiers, with one chokepoint, and with strict retention rules. The principle: **the API key is the only thing we never log; everything else is sorted by sensitivity.**

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
  user_opted_in_full  BOOLEAN
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

- **Always:** which steps ran, when, on which model, with how many tokens, at what cost, and whether they succeeded. Hashed fingerprints of your inputs (so we can tell two runs are on the same paper without storing the paper). No name, no email, no IP-tied identity.
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
- The `SECURITY.md` checklist green.
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
