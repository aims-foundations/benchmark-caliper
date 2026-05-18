# SECURITY.md

A checklist of concrete, verifiable security commitments for the validity-analyzer website. Every item has a verification method. **If you can't verify an item, it isn't done.** Re-check the full list before any production deploy.

This file is paired with [DESIGN.md](DESIGN.md), which describes how the website is built. The two must be kept in sync — every claim in DESIGN.md should map to a verifiable item here.

---

## How to use this file

- Each item is a single, verifiable claim — not an aspiration.
- Each item has a `Verify by:` line describing how to confirm it.
- Re-check the full list before every production deploy.
- The team reviews the entire file once per quarter; record the date and reviewer in the log at the bottom.

---

## 1. API key handling

- [ ] **The API key is never written to disk on the server, ever.**
  - Verify by: grep the codebase for any path that writes `api_key`, `Authorization`, or related env-var references to a file. After a real test request, run `grep -r "sk-ant-"` against logs, the database file, and the blob store — must return zero matches.

- [ ] **The API key is never included in any log output.**
  - Verify by: configure the structured logger to redact the `X-Anthropic-Key` header. Submit a deliberately failing request; inspect access.log, error.log, and any APM trace — must contain no `sk-ant-` prefix and no full key.

- [ ] **The API key is sent in an HTTP header, not a URL parameter or a cookie.**
  - Verify by: inspect frontend network calls — `fetch` uses `headers: { 'X-Anthropic-Key': ... }`, never a query param. Confirm no `Set-Cookie` response includes the key.

- [ ] **The API key is stored in `sessionStorage` by default; `localStorage` only with explicit user opt-in.**
  - Verify by: open browser devtools → Application → Storage. Default flow uses sessionStorage. The "remember on this device" toggle moves it to localStorage and back.

- [ ] **The API key input is masked and never echoed back in any UI element or response body.**
  - Verify by: input field is `type="password"`. Trigger an auth failure — error message says "auth failed" without echoing any portion of the key.

- [ ] **Pre-flight key validation does not log or persist the validation request or response body.**
  - Verify by: trace the validation endpoint — confirm only operational metadata (status, latency) is written, no input/output bodies.

- [ ] **No global mutable state stores keys across requests.**
  - Verify by: code review — the Anthropic client is constructed per-request inside the handler scope. No module-level dicts keyed by user or key. The one exception is `active_runs.store`, which holds the BYOK key in memory for the duration of a single run so auto-mode tasks can outlive the request that started them; that entry is dropped on run completion and never touches disk (covered by item 1.8).

- [ ] **The in-memory `active_runs` entry is dropped on every run-completion path and a sweeper culls stale entries.**
  - Verify by: trigger an auto-run, observe the entry exists during the run, observe it is gone after `run-complete` or `error`. Force-stale a test entry (backdate `created_at`) and confirm `store.sweep()` drops it. Tests in `test_active_runs.py` pin this behaviour.

## 2. Transport security

- [ ] **All connections use TLS 1.2+ with a valid certificate.**
  - Verify by: `openssl s_client -connect <domain>:443` confirms cert validity and protocol version. SSL Labs scan returns A or higher.

- [ ] **HSTS header is set with `max-age >= 31536000` and `includeSubDomains; preload`.**
  - Verify by: `curl -I https://<domain>` confirms the `Strict-Transport-Security` header.

- [ ] **HTTP redirects to HTTPS at the edge.**
  - Verify by: `curl -I http://<domain>` returns 301 or 308 to https.

- [ ] **No mixed content (no `http://` references on HTTPS pages).**
  - Verify by: browser console on every page shows no mixed-content warnings. Run an automated mixed-content scanner once per release.

- [ ] **CAA DNS records pin which certificate authorities can issue for our domain.**
  - Verify by: `dig CAA <domain>` lists only intended CAs.

## 3. Browser-side attack surface

- [ ] **Strict Content-Security-Policy is active on every page.**
  - Verify by: `curl -I` shows a `Content-Security-Policy` header with `script-src 'self'`, `default-src 'self'`, no `unsafe-inline`, no `unsafe-eval`, no wildcard.

- [ ] **No third-party scripts on pages that handle the API key or user content.**
  - Verify by: view source on the key-entry page, the upload page, and the run page — every `<script>` tag points to our own origin. No analytics, no chat, no ad SDKs.

- [ ] **Subresource Integrity (SRI) hashes are pinned for any external script (if any are ever introduced).**
  - Verify by: every `<script src="..."` from a non-self origin has an `integrity="sha384-..."` attribute.

- [ ] **`X-Frame-Options: DENY` and CSP `frame-ancestors 'none'` prevent clickjacking.**
  - Verify by: `curl -I` shows both headers. Manually attempt to embed the site in an `<iframe>` — browser refuses.

- [ ] **No `dangerouslySetInnerHTML` or equivalent unsafe DOM injection.**
  - Verify by: grep frontend codebase for `dangerouslySetInnerHTML`, `innerHTML =`, `document.write` — must return zero results outside of audited and documented exceptions.

- [ ] **Model-generated content (LLM responses, scoring outputs) is rendered as escaped text, never as HTML.**
  - Verify by: paste `<script>alert(1)</script>` into a deployment description, run pipeline, view scoring report — script does not execute.

- [ ] **CORS allowlist contains only our own frontend origin(s).**
  - Verify by: `curl -H "Origin: https://evil.com"` to an API endpoint — response does not include `Access-Control-Allow-Origin: *` or our origin.

- [ ] **`X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` set to deny sensitive APIs.**
  - Verify by: `curl -I` confirms each header.

## 4. Server hardening

- [ ] **Per-request temp directories for uploads; deleted on request completion.**
  - Verify by: trigger an upload, check `/tmp` during the request (file present), check after response (file absent). Confirm crashed-request cleanup by killing a worker mid-run.

- [ ] **Upload size capped at 50 MB.**
  - Verify by: send a 51 MB POST — server rejects with 413. Check FastAPI/uvicorn config for the relevant limit.

- [ ] **Rate limiting per IP enforced at the edge.**
  - Verify by: scripted burst of 100 requests/sec from one IP — confirm 429 responses kick in. Rate limit values are documented in the deploy config.

- [ ] **No write access to anything except the temp dir, the database, and the blob store.**
  - Verify by: process runs as a non-root user with restricted FS perms. Attempt to write outside allowed paths fails.

- [ ] **No backdoor admin endpoints reachable without authentication.**
  - Verify by: full route enumeration (`fastapi routes` or equivalent); every admin/debug route requires authenticated access.

## 5. Logging and redaction (the four-tier model)

- [ ] **All log writes go through the single redaction-gate function.**
  - Verify by: grep for direct calls to log/write/print of pipeline I/O. Every write must go through `log_step()` (or equivalent). No direct writes to the database or blob store from any other code path.

- [ ] **The redaction gate has unit tests covering: API key stripping, PII patterns (email, phone), opt-out routing, and tier classification.**
  - Verify by: `pytest tests/test_redaction.py` — all tests pass. A regression test is added for any reported leak.

- [ ] **Tier 0 (API keys, auth headers): never written to any log, store, or trace.**
  - Verify by: end-to-end test runs a full pipeline, then greps the database, blob store, and logs for `sk-ant-` — must return zero matches.

- [ ] **Tier 1 (operational metadata): always written to the structured store with no PII.**
  - Verify by: schema review — `runs` and `steps` tables contain only IDs, timestamps, model names, token counts, costs, status, error classes. No content fields, no email, no IP-tied identifier.

- [ ] **Tier 2 (fingerprints): SHA-256 hashes only, never raw inputs.**
  - Verify by: schema review — `input_hash` and `output_hash` columns store exactly 64-character hex strings.

- [ ] **Tier 3 (full content): retained 90 days by default, then auto-deleted.**
  - Verify by: nightly cleanup job exists and is scheduled. Test by inserting a 91-day-old blob and confirming it is removed on the next cron run.

- [ ] **The opt-out checkbox routes runs to skip tier-3 writes.**
  - Verify by: end-to-end test with the opt-out flag set — `blob_key` column is NULL, no objects are written to the blob store. Tier 1 + 2 are still populated.

- [ ] **Daily aggregation job rolls up `steps` rows into `daily_aggregates` before any pruning.**
  - Verify by: nightly job exists. Inspect `daily_aggregates` for yesterday's date — totals match what an ad-hoc SQL sum over the previous day's `steps` would produce.

## 6. Privacy and user data

- [ ] **A privacy policy is live, linked from the footer of every page, and matches actual practice.**
  - Verify by: page exists. Each claim in the policy maps to a line in this checklist.

- [ ] **A per-run opt-in toggle is present on the run page; default is unchecked (no tier-3 storage).**
  - Verify by: UI test — checkbox visible and unchecked by default; submitting the form without checking it produces a run whose `blob_key` columns are NULL.

- [ ] **A consent gate is shown before the user can use the tool the first time, explaining what we do and do not log.**
  - Verify by: visit the site in a fresh browser profile — modal appears before the key-entry form. Decision is persisted in localStorage so it does not reappear on the next visit. Clearing browser data brings the modal back.

- [ ] **The export-my-data endpoint returns a single run's full trace.**
  - Verify by: integration test — given a run ID, returns JSON containing all tier 1, 2, and 3 data for that run.

- [ ] **The delete-my-data endpoint removes both database rows and blob objects.**
  - Verify by: integration test — call delete on a run, confirm rows are removed and blob objects are deleted (not just unlinked).

- [ ] **No third-party analytics, advertising, or tracking SDKs anywhere on the site.**
  - Verify by: network tab on every page — only requests to our own origin and the Anthropic API. Re-check after every dependency update.

- [ ] **The user's email address (when provided for the report-ready notification) is stored only on the run's row and is removed by delete-my-data.**
  - Verify by: schema review — `runs.email` and `runs.email_sent_at` are the only columns for it; no `email` column on `steps`. End-to-end test: provide an email, run a pipeline, verify the row contains the address, then call delete-my-data and confirm the row is gone. Grep tier-3 blobs for the address — must return zero matches (the redaction gate's `EMAIL_PATTERN` strips email patterns from blob writes).

- [ ] **Email delivery uses a transactional-only provider; the recipient address is sent to Resend and nowhere else.**
  - Verify by: code review — only `email_notify.send_report_ready` sends mail; it only calls Resend; no other module references `runs.email`. If `RESEND_API_KEY` is unset, the dry-run fallback logs to stderr instead of contacting a third party.

## 7. Supply chain and dependencies

- [ ] **Lockfiles (`package-lock.json`, `requirements.txt` or `uv.lock`) are committed and pinned to exact versions.**
  - Verify by: lockfile is present in the repo; no version ranges (`^`, `~`, `>=`).

- [ ] **Dependabot/Renovate configured with security-update auto-PRs but no auto-merge.**
  - Verify by: `.github/dependabot.yml` exists; PR history shows reviewed/approved updates, never auto-merged.

- [ ] **A pre-commit secret scanner (e.g., gitleaks, trufflehog) blocks commits containing API key patterns.**
  - Verify by: pre-commit hook installed; attempt to commit a file containing `sk-ant-test123` — commit is blocked.

- [ ] **No `.env` files committed; only `.env.example`.**
  - Verify by: `git log --all --full-history -- '*.env'` returns no results. `.gitignore` includes `.env`.

- [ ] **Frontend dependencies on the key-entry page are minimized and audited.**
  - Verify by: `npm ls` for the key-handling route — every dep reviewed for maintainer reputation, age, recent activity, and necessity.

## 8. Operational accounts

- [ ] **2FA is enforced on every account that can deploy, push code, change DNS, or access hosting.**
  - Verify by: admin review on GitHub org settings, hosting provider, DNS registrar — 2FA enforced for all members.

- [ ] **Deploy credentials follow least privilege.**
  - Verify by: deploy token can deploy and roll back, but cannot delete the project, change billing, or read user data.

- [ ] **Production secrets are stored in the hosting provider's secret manager, never in env files in the repo.**
  - Verify by: `git grep` returns no production secrets. The hosting dashboard confirms secret scope and access.

- [ ] **Quarterly rotation of all production secrets (DB password, blob-store credentials, signing keys).**
  - Verify by: a rotation log or calendar entry. Last rotation date is less than 90 days from current.

## 9. Monitoring and incident response

- [ ] **Uptime monitor pings the site every minute.**
  - Verify by: monitoring dashboard exists. Test by simulating an outage — alert fires within 2 minutes.

- [ ] **Error tracking (Sentry or equivalent) is configured with PII scrubbing for keys and request bodies.**
  - Verify by: trigger a deliberate error — confirm the captured event contains no key, no PDF content, no deployment description.

- [ ] **Cost dashboard shows daily/weekly spend per model.**
  - Verify by: dashboard exists. Live data matches the result of a manual SQL query against `daily_aggregates`.

- [ ] **`SECURITY.md` (this file) and a public security-contact email are visible in the repo and on the website.**
  - Verify by: file exists. The email auto-forwards to a real human and is monitored.

- [ ] **An incident response runbook documents: discovery → triage → containment → user notification → postmortem.**
  - Verify by: runbook exists in the repo. Every team member has read it once.

- [ ] **Quarterly review of this entire checklist; the date and reviewer are recorded below.**
  - Verify by: review log entry less than 90 days from current.

---

## Review log

| Date | Reviewer | Notes |
|------|----------|-------|
| 2026-05-04 | _initial draft_ | First version, paired with DESIGN.md. No build yet — items will become checkable as the build proceeds. |
| 2026-05-10 | pre-deploy audit | First end-to-end walk-through against the running Docker stack. **Pass: 25 items.** **Fail: 5 items** that are addressable now (4.3 rate limiting, 4.4 non-root container, 7.2 dependabot, 7.3 secret scanner, 9.5 incident runbook). **Deferred: 12 items** that genuinely require a deployed public domain + hosting accounts (sections 2, 8, parts of 9). One minor finding: `runs.user_opted_in_full` schema default is `1` while project policy is opt-out — code always sets it explicitly so no behaviour bug, but the schema default is misleading. |
| 2026-05-10 | follow-up fixes | Closed 4 of the 5 fail items: 4.4 non-root container (Dockerfile USER directive, verified running as UID 10001), 7.2 dependabot config (`.github/dependabot.yml`), 7.3 pre-commit + gitleaks (`.pre-commit-config.yaml` + `.gitleaks.toml` with custom `sk-ant-` rule and test-fixture allowlist), 9.5 incident runbook (`website/INCIDENT_RUNBOOK.md`). Schema default for `user_opted_in_full` flipped to `0`. **4.3 rate limiting intentionally not added in-app** — the team decision is to handle it at the hosting edge during deploy instead (Cloudflare / Fly built-in), so this item remains pending against the future deploy rather than the codebase. **101 backend + 48 frontend tests still pass.** |
