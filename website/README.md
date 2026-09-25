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
shows the sample size before paid calls, and displays ranked items with all six
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

For this first hosted demo, the catalog contains **MathArena and AfriMed-QA**,
using three pinned item tables across both measurement-db branches. The user
chooses 1–10 initial rows per table (2 by default), for at most 30 source rows.
Identical evidence is assessed once, and the UI requests all ranked items in
this bounded sample (up to 30). This is a deterministic sample, not a
full-corpus search or a representative selection. Full traversal remains
available through the [CLI](../bayesian_auditing/README.md).

The gated dataset requires Hugging Face access. Configure `HF_TOKEN` on the
server, or enter an authorized read token in the demo's masked access field.
The server never uses its own OpenAI key: each review requires the user's key.

`server/item_review.py` provides a small in-memory background runner. The browser
polls progress using a separate run secret and can stop a run or download its
JSON results. This avoids keeping one HTTP request open across every item.
Three active reviews are allowed per process, one per OpenAI key; each has a
one-hour maximum duration. Completed/failed/cancelled results expire after one
hour (checked each minute). Up to 30 runs are retained in memory. Keys and user
content are not written to the Caliper database or CLI result files. Source
Parquet files are cached by Hugging Face. Refreshing the same tab resumes polling;
server restarts discard jobs and results. Cancelling stops further requests but
cannot guarantee that a request already submitted to OpenAI is unbilled.

The router and UI live in `server/item_review.py` and `client/src/itemReview/`;
`client/src/EvaluationSite.tsx` chooses the workflow. The catalog inventory is
`server/item_review_inventory.json`. To refresh it deliberately, run:

```bash
python -m bayesian_auditing inventory --benchmarks matharena afrimedqa \
  --output website/server/item_review_inventory.json
```

The committed inventory contains paths and revisions only, not dataset items or
credentials. Do not add arbitrary large benchmarks to this hosted sample without
reviewing memory and cache-disk requirements.

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
