# Manual vs. Automated Comparison Study

A head-to-head study comparing an expert's **manual** benchmark-validity assessment
against the **automated** pipeline's assessment of the *same* deployment tuple.

## The question

For a given `(benchmark, use case, target population)` triplet, does the automated
validity pipeline produce an assessment that an expert finds useful, accurate, and
decision-relevant — measured against the expert's own manual assessment as the
reference point?

## Two arms

Each expert contributes to both arms for their own triplet:

1. **Manual arm** — the expert performs their own validity assessment directly from
   the deployment tuple (benchmark + use case + target population), with **no
   elicitation dialogue** and **no pre-assigned dimension priority weights**. They
   form their own view of dimension severity.

2. **Automated arm** — the pipeline is run on the *same* tuple, also with the
   elicitation stage skipped, so both arms are conditioned on exactly the same
   inputs — no more, no less. Output is a scored `review.pdf`.

The expert completes their manual assessment **first**, is then sent the automated
`review.pdf`, and finally fills out a short comparison form. Independence (manual
before automated) is enforced by a checkbox in the form.

## Directory layout

```
manual_comparison/
├── README.md                        # this file
├── run_manual_comparison.sh         # driver for the AUTOMATED arm
├── create_comparison_form.py        # builds the Google comparison form (user-run)
├── comparison_form_url.json         # saved responder + edit URLs for that form
├── deployment_context_responses.csv # expert intake form responses (the raw triplets)
├── rowN_<name>/                     # one per expert/tuple — the pipeline inputs
│   ├── deployment_description.txt   #   use case + target population (for Step 0)
│   └── elicitation_summary.md       #   synthetic, elicitation-skipped summary
├── reports/                         # generated automated-arm review PDFs, per row
│   ├── mrbench_review.pdf
│   └── germanquad_review.pdf
└── superseded_assessments/          # earlier assessment runs kept for provenance
```

Benchmark paper PDFs live outside this dir at `papers/<name>.pdf`.
Pipeline outputs land in `assessments/<name>/<slug>/`.

## The automated arm: `run_manual_comparison.sh`

Runs the validity pipeline on each study tuple, **skipping the elicitation stages**
(steps 1, 2-questions, 2-summary are never invoked). For each row it:

1. **Step 0** — derives the slug from `deployment_description.txt` (Haiku, ~$0.01;
   idempotent — reuses the slug when the description is unchanged).
2. **Injects** the pre-authored synthetic `elicitation_summary.md` into
   `assessments/<name>/<slug>/`, carrying the tuple downstream in place of an
   elicited summary.
3. **Steps 3a–4b** — extract / synthesize paper + benchmark + region YAMLs.
4. **Step 5** — web-search enrichment.
5. **Step 5b-da** — dataset analysis, *only* when the row declares an HF dataset.
6. **Steps 6–9** — compose prompt, Opus scoring, report, and the final `review.pdf`.

### Row registry

Rows are declared in the `ROWS` array near the top of the script, pipe-delimited:

```
name | pdf_path | seed_dir | hf_dataset | hf_config
```

| field        | meaning                                                              |
|--------------|----------------------------------------------------------------------|
| `name`       | pipeline name = PDF stem; also the `assessments/<name>/` dir         |
| `pdf_path`   | benchmark paper PDF (must already exist locally)                     |
| `seed_dir`   | holds `deployment_description.txt` + `elicitation_summary.md`        |
| `hf_dataset` | HF dataset id for Step 5b dataset analysis, or `-` to skip 5b        |
| `hf_config`  | HF config/subset, or `-`                                             |

Whether dataset analysis (5b) is enabled per row is a deliberate, documented choice
— see the inline comments in the registry (e.g. GermanQuAD's custom loader can't
load under `datasets` 4.x, so it's assessed on paper + web only to stay comparable
with MRBench).

### Running it

Run from the `anthropic_api_package_release/` directory, with the
`validity-global-south` conda env active and `ANTHROPIC_API_KEY` set (via `.env` or
the environment). `qpdf` or `pdftk` must be on `PATH` for PDF splitting.

```bash
./manual_comparison/run_manual_comparison.sh              # all ready rows
./manual_comparison/run_manual_comparison.sh mrbench      # a single row
DRY=1 ./manual_comparison/run_manual_comparison.sh        # print the plan, run nothing
STOP_AFTER=4b-synthesize ./manual_comparison/run_manual_comparison.sh mrbench  # checkpoint
```

Rows with missing inputs are skipped (or, if named explicitly, fail loudly).
The final artifact per row is `assessments/<name>/<slug>/pdfs/review.pdf`.

## The comparison form: `create_comparison_form.py`

Builds the single Google Form experts fill out after receiving the automated
assessment (~10 min, ~one form for all experts). **User-run** (Google OAuth;
reuses `.secrets/{credentials,token.json}` with the `forms.body` scope).

The form is structured around two **independent** axes so a "useful but imperfect"
result can't hide under one averaged score:

- **§3 Signal** — valid / useful content the pipeline *added*.
- **§4 Noise** — incorrect / irrelevant content requiring expert discernment
  (split into hallucination frequency vs. over-flagging frequency).

Both are positive-direction, so an assessment can rate high on both. The
ground-truth anchor is **§5 Decision outcome**: did the automated assessment change
and/or improve the expert's final deploy + remediation call. Sections: (1) identity
+ independence check, (2) overall agreement, (3) signal, (4) noise, (5) decision
impact, (6) efficiency / trust / summary profile.

```bash
python manual_comparison/create_comparison_form.py            # create it
python manual_comparison/create_comparison_form.py --dry-run  # print the item plan
python manual_comparison/create_comparison_form.py --force    # recreate
```

Responder + edit URLs are printed and saved to `comparison_form_url.json`
(re-runs are skipped unless `--force`).

## Adding a new row (new expert deployment context)

1. Place the benchmark paper PDF at `papers/<name>.pdf`.
2. Create `rowN_<name>/deployment_description.txt` — two labeled blocks:
   `Use case and domain:` and `Target population:` (see any existing row).
3. Create `rowN_<name>/elicitation_summary.md` — the synthetic, elicitation-skipped
   summary (Use Case + Target Population verbatim, with the Q&A and priority-weight
   sections marked "skipped"; copy an existing row's file and edit the two content
   blocks).
4. Add a registry line to `ROWS` in `run_manual_comparison.sh`, deciding whether to
   enable Step 5b dataset analysis (`hf_dataset`/`hf_config`) or leave both `-`.
5. Run the driver for that row (see above).
