# Benchmark Caliper — Website

A public-facing interface to two evaluation workflows at <https://aimslab.stanford.edu/benchmark-caliper/>. The starting page lets users choose Benchmark Caliper or goal-conditioned item review. See [SECURITY.md](SECURITY.md) for how each flow handles data and keys.

## Routes

- `/` — workflow selection.
- `/caliper` — the existing benchmark-paper analysis, using an Anthropic key.
- `/items` — the new item-review demo, using an OpenAI key.
- `/run/{run_id}` — existing Caliper report links, preserved.

All routes work under the production `/benchmark-caliper` prefix.

## Goal-conditioned item review

The new flow asks for an OpenAI key, collects six concrete deployment questions,
shows the catalog and fixed sample size before paid calls, and displays ranked items with all six
validity judgments, per-dimension confidence and explanations, evidence,
information gaps, and pinned source provenance. It
uses the shared `bayesian_auditing` loader, rubric, schema, and arithmetic with
GPT-6 Luna, high reasoning effort, and a 25,000-token ceiling. The initial
questions are fixed and editable; they do not require an additional model call.

Scoring version 2 keeps every valid assessment in the ranking, including items
with partial evidence. High/medium/low confidence weights (1, 0.6, 0.3) pull
scores toward a neutral baseline of 3; missing dimensions contribute that
baseline without receiving an invented dimension score. Results show the
adjusted ranking score, unadjusted mean, dimensions scored, and evidence gaps.
The confidence labels and weights are not calibrated probabilities. See the
[scoring policy](../bayesian_auditing/README.md#process-and-scoring) for details.
The JSON download includes the policy and confidence explanations. Old reports
have no recorded confidence; they require a new paid review to obtain it.

The catalog includes every available formatted `items.parquet` table from both
measurement-db branches, pinned to the revisions in the inventory. The current
snapshot has **113 benchmark collections, 119 tables, and 1,804,733 source rows**.
The demo selects up to **50 distinct items per benchmark collection**, for at most
**5,407 selected items** in this snapshot. A fixed seed makes selection independent
of row order and deployment description. Duplicate evidence gets one selection
opportunity, and all provenance is retained. When a benchmark has branch-exclusive
evidence in both branches, at least one selected item comes from each. Rankings
describe the selected sample. The text judge does not inspect referenced media assets.
The mathematics tutor is an optional form example, not a restriction on deployment.

The gated dataset requires Hugging Face access. Configure an authorized
`HF_TOKEN` or Hub login on the server. Dataset access is managed by the server;
visitors supply only their OpenAI API key. If the server credential is missing,
the UI disables new reviews and asks visitors to contact the site maintainer.
The server never uses its own OpenAI key: each review requires the user's key.

`server/item_review.py` prepares the complete sample before making model calls,
then runs one sequential, cancellable assessment stream. The first preparation
scans all source rows without model calls, using a temporary SQLite index of hashes
and source locations, keeping only the best 50 selection candidates in memory.
Additional branch representatives are fetched through Parquet HTTP ranges if
needed. `bayesian_auditing/sampling.py` caches selected dataset evidence under
`WEBSITE_DATA_DIR/item-review-samples/`, keyed by pinned inventory, seed, sample
size, and loader/sampling versions. Later reviews reuse that sample. The cache
contains no deployment answers or provider keys. Source metadata may also be cached.
`server/item_review_store.py` stores assessments, evidence, and source references
in a private temporary SQLite file, with indexes for deduplication and ranking.
The deployment answers and OpenAI key remain in process memory. Raw provider
responses are not retained. This keeps dataset loading and ranking independent
of the available RAM, without adding a worker queue or persistent job service.

The browser polls 20 results at a time; these are display pages, not review limits.
The authenticated `/api/item-review/runs/{id}/export` route streams every assessment
available when the download begins. A read failure stops preparation or assessment
and preserves completed results; it does not silently skip a table or claim a
complete sample. Exports include the sampling policy and pinned source revisions.
Three reviews can run simultaneously, one per OpenAI key. Up to 30 jobs are retained.
Completed/failed/cancelled jobs and their result files expire after one hour
(checked each minute). A normal shutdown cancels jobs and deletes these files.
An abrupt process kill can leave orphaned temporary files until the host cleans
them up. The demo does not resume after server restarts; the [CLI](../bayesian_auditing/README.md)
supports durable resume. Refreshing the same browser tab resumes polling a live
job. Cancelling prevents further model calls; a request already sent may be billed.

The router and UI live in `server/item_review.py` and `client/src/itemReview/`;
`client/src/EvaluationSite.tsx` chooses the workflow. The catalog inventory is
`server/item_review_inventory.json`. To refresh it deliberately, run:

```bash
python -m website.server.item_review_catalog
```

The refresh command discovers both branches and reads Parquet footers to validate
the required columns and record source-row counts. It saves only paths, revisions,
and counts after all tables are inspected successfully. No item content or
credentials are committed. Prepare the reusable sample without an OpenAI key with:

```bash
python -m website.server.item_review_sample
```

Preparation can take time on a cold cache. The cache is private to the server and
can be regenerated; it survives normal shutdown. Temporary assessment files still
expire after each review. Completion depends on provider quota, disk space, and
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
changing deployment answers uses the same selected evidence with new judgments.

---

## What it does

A user pastes their Anthropic API key, uploads a benchmark paper PDF, and describes a deployment context. The site walks them through:

1. **Slug** — derive a short identifier (Haiku)
2. **Metadata** — extract benchmark metadata from pages 1–2 (Haiku)
3. **Elicitation questions** — generate 3–5 deployment-context questions (Sonnet)
4. **User answers** the questions in the browser
5. **Elicitation summary** — synthesize a structured summary (Sonnet)
6. **Email + mode** — user provides an email address and chooses auto (default) or step-by-step. By default the rest of the pipeline runs unattended and the user is emailed when the report is ready.
7. **Paper extraction** — per-page parallel Haiku fan-out + Sonnet consolidation
8. **Benchmark YAML** — Haiku picks ICL examples, Sonnet writes a per-paper YAML
9. **Region YAML** — Haiku picks templates, Sonnet writes a regional scaffold, Sonnet+web search enriches it
10. **Validity scoring** — single Opus call across the 6 dimensions
11. **Email delivery** — Resend sends the user a link to `/run/{run_id}` with the rendered Markdown report and raw JSON attached.

The final output is a 6-dimension validity report with per-dimension scores, reasoning, and evidence.

A typical end-to-end run for a 20-page paper costs roughly $1.50–$2.50 of Anthropic API spend at current rates (Haiku 4.5 / Sonnet 4.6 / Opus 4.7). Web search adds $10 per 1,000 searches on top of tokens.

---

## Running it locally

Requirements: Python 3.11+, Node 24+, and the API key for the selected workflow.

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

For UI work and click-through testing without paying for API calls, set `MOCK_ANTHROPIC=1`. Every `call_text_async()` short-circuits to canned fixtures pulled from one already-paid assessment under `anthropic_api_package_release/assessments/`. Paste any string (e.g. `sk-ant-FAKE`) into the API-key field — the value is ignored.

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

Run the shared item judge tests with `python -m pytest bayesian_auditing/tests/`.
Backend tests mock provider calls, including success, failures, cancellation,
credential handling, retention, and per-run access control. Frontend tests cover
both routing and the guided item-review flow.

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
