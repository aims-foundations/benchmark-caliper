# Validity Analyzer — Website

A public-facing interface to the validity-analysis pipeline from the paper *"Validity Analysis when Porting Benchmarks Across Cultures and Regions."*

> **Status:** v0 draft. The full 7-step flow works end-to-end. Privacy infrastructure (consent gate, retention cron, export/delete) is in place. Not yet deployed to a public host. **Do not share publicly until pre-launch checklist in [SECURITY.md](SECURITY.md) is completed.**

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

---

## How to run it

Requirements: Python 3.10+, Node 20+, an Anthropic API key.

```bash
# Terminal 1 — backend
cd website/server
python3 -m venv ../../.venv && source ../../.venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app:app --reload --port 8000

# Terminal 2 — frontend
cd website/client
npm install
npm run dev
```

Open <http://localhost:5173>. Vite proxies `/api/*` to <http://localhost:8000>.

---

## How to test it 

### Click-through

1. Open the site. You'll see a one-time consent screen — read it, click "I understand."
2. Paste your Anthropic API key (the page never sends it to our server).
3. Upload a short benchmark paper PDF. Anthropic supports up to 32 MB and ~100 pages per call.
4. Type a deployment description like "Indonesian government chatbot answering KTP queries."
5. Wait ~30 seconds for Steps 0–2 to stream.
6. Answer the elicitation questions. Short answers are fine.
7. Wait for the elicitation summary (~30 seconds).
8. Click **Extract paper →**, re-upload the same PDF (we don't keep it). Watch live page-by-page progress.
9. Click **Build region context →**. Web search enrichment can take 30–60 seconds.
10. Click **Score validity →**. The Opus call typically takes 30–90 seconds.

A typical end-to-end run for a 20-page paper costs roughly $1.50–$2.50 of Anthropic API spend at current rates (Haiku 4.5 / Sonnet 4.6 / Opus 4.7). Web search adds $10 per 1,000 searches on top of tokens.

### Run the test suite

```bash
# backend (run from the repository root)
python3 -m pytest website/server/tests/

# frontend
cd website/client
npm test
```

All tests should pass (101 backend + 51 frontend = 152 total).

---

## What to review

Most useful first reads:

- [DESIGN.md](DESIGN.md) — narrative architecture, security posture, four-tier logging model, roadmap
- [SECURITY.md](SECURITY.md) — verifiable checklist for everything we claim
- [server/app.py](server/app.py) — every endpoint
- [server/active_runs.py](server/active_runs.py) — the process-local store that holds the BYOK key + PDF for an auto-run; the only place key bytes live server-side
- [server/email_notify.py](server/email_notify.py) — Resend wrapper used for the report-ready email, with a dry-run fallback when `RESEND_API_KEY` is unset
- [server/logging_gate.py](server/logging_gate.py) — the single chokepoint to disk; everything privacy-related funnels through it
- [client/src/App.tsx](client/src/App.tsx) — the state machine for the whole user flow

For a faster skim, the slice-by-slice journey is in `MEMORY.md` and the project memory files.

---

## Known gaps for v0

- **Web search cost** isn't modeled in the cost ledger ($10 per 1k searches Anthropic charges separately).
- **MVP deploy target is Render.** See [DEPLOYMENT.md](DEPLOYMENT.md) for the one-service Docker setup and the AIMS Vercel proxy.
- **Privacy policy and ToS** copy still needs writing — the policy is described in DESIGN.md section 6 but the user-facing page doesn't exist yet.
- **Pre-launch security checklist** in SECURITY.md hasn't been ticked off; do not point a public domain at this until it has.

---

## Layout

```
website/
├── DESIGN.md              # Narrative spec
├── SECURITY.md            # Verifiable checklist
├── README.md              # This file
├── server/                # FastAPI backend
│   ├── app.py             # All HTTP endpoints
│   ├── logging_gate.py    # The privacy chokepoint
│   ├── retention.py       # 90-day cron
│   ├── pipeline_assets.py # Reads ICL YAMLs from anthropic_api_package/
│   ├── anthropic_client.py
│   ├── pdf_utils.py
│   ├── elicitation.py
│   ├── quote_registry.py
│   ├── prices.py
│   ├── sse.py
│   ├── db.py
│   ├── requirements.txt
│   └── tests/             # 101 backend tests
└── client/                # Vite + React + TypeScript
    ├── src/
    │   ├── App.tsx
    │   ├── api.ts
    │   ├── consentStorage.ts
    │   ├── keyStorage.ts
    │   └── components/    # Per-phase views
    └── (vitest tests, 48 of them)
```

---

## License

TBD.
