# Security and privacy

How the Validity Analyzer website handles user data and credentials.

This file documents the website's security posture **as actually implemented in the code**. Every statement below is a property of the code or schema in this repo, with a one-line description of how anyone can independently verify it.

Items that depend on the deployed infrastructure (TLS, DNS, hosting accounts, monitoring) live in [Pre-launch verification](#pre-launch-verification) at the bottom — these must be checked off before a public domain is pointed at the service.

This file is paired with [DESIGN.md](DESIGN.md). Every privacy claim in DESIGN.md should map to a statement here.

---

## 1. API key handling

The website uses a "bring your own key" (BYOK) model: the Anthropic API key is supplied by the user on each request and never persisted on our side.

- **The API key is never written to disk on the server.** The redaction gate in `server/logging_gate.py` strips `sk-ant-...` patterns from every blob write.
  *How to verify:* run a real test request, then `grep -r "sk-ant-"` against the database file, the blob store, and any log files — zero matches.

- **The API key is never included in any log output.** The structured logger redacts the `X-Anthropic-Key` header.
  *How to verify:* trigger a deliberately failing request and inspect logs — no `sk-ant-` prefix anywhere.

- **The API key is sent in an HTTP header, not a URL parameter or a cookie.** `client/src/api.ts` uses `headers: { 'X-Anthropic-Key': ... }`. CORS sets `allow_credentials=False`, so no cookie auth is possible.
  *How to verify:* inspect frontend network calls; confirm no `Set-Cookie` response includes the key.

- **The API key is stored in `sessionStorage` by default; `localStorage` only when the user explicitly opts in to "remember on this device".** Implemented in `client/src/keyStorage.ts`.
  *How to verify:* open browser devtools → Application → Storage. Toggling "remember" moves the key between the two stores.

- **The API key input is masked and never echoed back in any UI element or response body.** `client/src/components/KeyForm.tsx` uses `type="password"`.
  *How to verify:* trigger an auth failure — error message says "auth failed" without echoing any portion of the key.

- **No global mutable state stores keys across requests.** The Anthropic client is constructed per-request inside the handler scope. The one exception is `active_runs.store`, which holds the BYOK key in memory for the duration of a single auto-run so background tasks can outlive the request that started them; that entry is dropped on run completion and never touches disk.
  *How to verify:* code review of `server/app.py` handlers + `server/active_runs.py`. Behavior pinned by `test_active_runs.py`.

- **The in-memory `active_runs` entry is dropped on every run-completion path, and a sweeper culls stale entries after one hour.**
  *How to verify:* `pytest server/tests/test_active_runs.py` — see `test_end_drops_entry` and `test_sweeper_drops_stale_entries`.

## 2. Browser-side attack surface

- **A strict Content-Security-Policy is active on every page**: `default-src 'self'`, `script-src 'self'`, no `unsafe-inline`, no `unsafe-eval`, no wildcards. Configured in `server/app.py` (`SECURITY_HEADERS`).
  *How to verify:* `curl -I http://<host>/` shows the `Content-Security-Policy` header.

- **No third-party scripts on any page** — no analytics, no chat, no ad SDKs.
  *How to verify:* `grep "<script" client/index.html` shows only the bundled app script (self-origin).

- **`X-Frame-Options: DENY` and CSP `frame-ancestors 'none'` prevent clickjacking.**
  *How to verify:* `curl -I` shows both headers; embedding the site in an `<iframe>` is refused by the browser.

- **No `dangerouslySetInnerHTML` or unsafe DOM injection.**
  *How to verify:* `grep -r "dangerouslySetInnerHTML\|innerHTML\|document.write" client/src` returns zero results.

- **Model-generated content (LLM responses, scoring outputs) is rendered as escaped text, never as HTML.**
  *How to verify:* paste `<script>alert(1)</script>` into a deployment description, run the pipeline, view the scoring report — script does not execute, literal text is displayed.

- **CORS allowlist contains only configured frontend origin(s).** The allowlist is controlled by the `WEBSITE_ALLOWED_ORIGINS` env var; the default is `http://localhost:5173`.
  *How to verify:* `curl -H "Origin: https://evil.com"` to an API endpoint — response does not include that origin in `Access-Control-Allow-Origin`.

- **Defense-in-depth headers are set:** `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` denies camera / microphone / geolocation.
  *How to verify:* `curl -I` confirms each header. Set in `server/app.py:SECURITY_HEADERS`.

## 3. Server hardening

- **Upload size is capped at 50 MB** (`MAX_BODY_BYTES` in `server/app.py`). Enforced by middleware before any handler runs.
  *How to verify:* send a 51 MB POST — server rejects with 413.

- **PDF uploads are processed in memory and never written to a persistent temp directory.** During a run, the PDF bytes live in `active_runs.store` (memory only). At scoring time the PDF is written to the per-run workspace at `data/tuples/<run_id>/paper.pdf` so the verifier can re-check quotes against it; it is removed when the run is deleted, when the workspace is reset, or by the retention cron after 90 days.
  *How to verify:* trigger an upload, check `/tmp` during and after the request — no leftover files. `pytest -k "verify or pdf"` pins the workspace lifecycle.

- **No backdoor admin endpoints reachable without authentication.** The one admin endpoint, `POST /api/runs/{run_id}/verify`, requires an `X-Admin-Token` header matching the `WEBSITE_ADMIN_TOKEN` env var. The env var being unset returns 503, so a forgotten config does not leave admin routes open.
  *How to verify:* `pytest server/tests/test_app.py -k verify` covers env-unset, wrong-token, and correct-token cases.

- **The Docker image runs as a non-root user.** `Dockerfile` includes a `USER` directive (UID 10001).
  *How to verify:* `docker inspect` the running container — `Config.User` is set.

## 4. Logging and redaction (the four-tier model)

The website classifies every piece of data into one of four tiers. All persistence routes through a single gate.

- **All log writes go through `server/logging_gate.py`.** `start_run()` and `log_step()` are the only entry points; no other module writes to the database or the blob store.
  *How to verify:* `grep -n "db.execute" server/*.py | grep -v logging_gate` shows no direct writes outside the gate.

- **The redaction gate has unit tests** covering API key stripping, email and phone PII patterns, opt-out routing, and tier classification.
  *How to verify:* `pytest server/tests/test_logging_gate.py` — all tests pass.

- **Tier 0 (API keys, auth headers): never written to any log, store, or trace.** Stripped by `API_KEY_PATTERN` in `server/logging_gate.py` before any persistence.
  *How to verify:* after a full pipeline run, `grep -r "sk-ant-"` against the database file, blob store, and logs returns zero matches.

- **Tier 1 (operational metadata): always written to the `runs` and `steps` tables with no PII.** Schema in `server/db.py`: only IDs, timestamps, model names, token counts, costs, status, error classes. No content fields, no email, no IP-tied identifier.
  *How to verify:* schema review of `server/db.py`.

- **Tier 2 (fingerprints): SHA-256 hex hashes only, never raw inputs.** `input_hash` and `output_hash` columns store exactly 64-character hex strings.
  *How to verify:* `SELECT length(input_hash), length(output_hash) FROM steps WHERE input_hash IS NOT NULL LIMIT 5;` — always 64.

- **Tier 3 (full content) is retained 90 days, then auto-deleted.** `server/retention.py` runs daily and prunes:
  - Tier-3 blob files older than 90 days, and
  - Per-run tuple workspaces (`data/tuples/<run_id>/`, which contain `paper.pdf`, `scoring.json`, `report.md`, `review.pdf`) older than 90 days, using the *newest* file mtime as the cutoff so an active re-score isn't prematurely wiped.

  *How to verify:* `pytest server/tests/test_retention.py` — 17 tests pin the cron behavior, including the workspace prune.

- **The opt-out checkbox routes runs to skip tier-3 writes.** Tier 1 + 2 are still populated; `blob_key` is NULL and no objects are written to the blob store.
  *How to verify:* end-to-end test with `opted_in_full=False` — confirm `blob_key IS NULL` for every step.

- **A daily aggregation job rolls `steps` rows into `daily_aggregates` before any pruning** (`aggregate_yesterday()` in `server/retention.py`). Idempotent via `INSERT OR REPLACE` on the composite primary key.
  *How to verify:* inspect `daily_aggregates` for yesterday's date — totals match an ad-hoc SQL sum over the previous day's `steps`.

## 5. Privacy and user data

- **A per-run opt-in toggle is present; default is unchecked.** Submitting the form without checking it produces a run whose `blob_key` columns are NULL everywhere.
  *How to verify:* open the form, inspect the checkbox default; submit without it, then query `steps` for the run.

- **A consent gate is shown before the user can use the tool the first time**, explaining what is and isn't logged. The decision is persisted in `localStorage` (`consent_v1`) so it doesn't reappear on the next visit.
  *How to verify:* open the site in a fresh browser profile — modal appears before the key-entry form. Clear browser data and reload — modal reappears.

- **The export-my-data endpoint (`GET /api/runs/{run_id}/export`)** returns the full trace for one run as JSON: the run row, all step rows, and the contents of any tier-3 blobs still on disk.
  *How to verify:* integration test in `server/tests/test_app.py`.

- **The delete-my-data endpoint (`DELETE /api/runs/{run_id}`)** removes the database row, cascades to delete all `steps` rows, removes the per-run blob directory, and removes the per-run tuple workspace (including the source PDF).
  *How to verify:* integration test confirms rows and files are gone. After the call returns, no record of the run remains.

- **No third-party analytics, advertising, or tracking SDKs anywhere on the site.**
  *How to verify:* open the network tab on every page — only requests to our own origin and `api.anthropic.com`.

- **The user's email address (provided for the report-ready notification) is stored only on the `runs` row and is removed by delete-my-data.** Schema in `server/db.py`: `runs.email` and `runs.email_sent_at` are the only columns for it; no email column exists on `steps`. The redaction gate's `EMAIL_PATTERN` strips emails from tier-3 blob writes.
  *How to verify:* schema review. End-to-end test: provide an email, run a pipeline, verify the row contains the address, then call delete-my-data and confirm the row is gone. Grep tier-3 blobs for the address — zero matches.

- **Email delivery uses Resend only.** No other module references `runs.email`. If `RESEND_API_KEY` is unset, the dry-run fallback logs to stderr instead of contacting any third party.
  *How to verify:* `grep -r "runs\.email" server/` shows only `email_notify.py` and `db.py`.

## 6. Supply chain

- **Lockfiles are committed and pinned to exact versions.** `requirements.txt` uses `==`; `package-lock.json` is committed.
  *How to verify:* read both files — no `^`, `~`, `>=` ranges in pinned production deps.

- **A pre-commit secret scanner blocks commits containing API key patterns.** Configured via `.pre-commit-config.yaml` + `.gitleaks.toml` at the repo root, with a custom rule for `sk-ant-` and an allowlist for known-safe test fixtures.
  *How to verify:* attempt to commit a file containing `sk-ant-realkey123` — gitleaks blocks it.

- **No `.env` files are committed.**
  *How to verify:* `git log --all --full-history -- '*.env'` returns no results.

---

## Pre-launch verification

These items genuinely depend on deployed infrastructure, hosting accounts, or written documents — they are not properties of the codebase. Tick each one before pointing a public domain at this service.

### Transport security (depends on hosting)

- [ ] TLS 1.2+ with valid cert (SSL Labs grade A or higher).
- [ ] HSTS header with `max-age >= 31536000; includeSubDomains; preload`.
- [ ] HTTP redirects to HTTPS at the edge.
- [ ] No mixed content on any page.
- [ ] CAA DNS records pin acceptable CAs.

### Rate limiting (depends on edge)

- [ ] Per-IP rate limiting at the hosting edge (Cloudflare / Fly built-in). Documented in deploy config.

### Operational accounts

- [ ] 2FA enforced on GitHub org, hosting provider, DNS registrar.
- [ ] Deploy credentials follow least privilege (can deploy and roll back; cannot delete the project, change billing, or read user data).
- [ ] Production secrets stored in hosting provider's secret manager, not in env files in the repo.

### Monitoring

- [ ] Uptime monitor pings the site every minute; alert fires within 2 minutes of simulated outage.
- [ ] Error tracking (Sentry or equivalent) is configured with PII scrubbing for keys and request bodies.

### Public-facing docs and addresses

- [ ] A privacy policy page is live, linked from the footer of every page, and every claim maps to a statement above. (Copy still needs writing — see README.md "Known gaps for v0".)
- [ ] Security contact email is published in `SECURITY.md` and on the website; the address auto-forwards to a monitored inbox.

### Review cadence

- [ ] Quarterly review of this entire file; the date and reviewer are recorded below.

---

## Review log

| Date | Reviewer | Notes |
|------|----------|-------|
| 2026-05-21 | trim | Dropped four pre-launch items judged non-essential for v0: Dependabot config, incident runbook, quarterly secret rotation, cost dashboard. GDPR Art. 33 breach-notification duty still applies to EU users independent of the removed runbook line. Also removed a duplicated "no `.env` committed" claim in §6. |
| 2026-05-19 | rewrite | Restructured into declarative claims (what the code guarantees) and a pre-launch checklist (what hosting / process / docs need to add before a public deploy). All declarative items audited against the codebase at this date. Workspace retention added to `retention.py` to cover the now-persisted source PDF. Incident runbook + Dependabot config tracked as pre-launch items (not yet written). |
| 2026-05-10 | follow-up fixes | Closed 4 of 5 fail items from the pre-deploy audit. Schema default for `user_opted_in_full` flipped to `0`. Rate limiting intentionally not added in-app — handled at the hosting edge during deploy. |
| 2026-05-10 | pre-deploy audit | First end-to-end walk-through against the running Docker stack. |
| 2026-05-04 | initial draft | First version, paired with DESIGN.md. |
