#!/usr/bin/env bash
# ============================================================================
# run_manual_comparison.sh
#
# Drive the validity pipeline on the manual-study deployment tuples, WITHOUT
# the elicitation stage. For each row we pre-author a synthetic
# `elicitation_summary.md` (verbatim Use Case + Target Population from the
# expert's tuple, with the Q&A / priority-weight sections filled by explicit
# "skipped" notes). That file carries the tuple downstream so the automated
# arm is conditioned on exactly what the manual expert works from — no more,
# no less.
#
# Pipeline steps 1, 2-questions, and 2-summary are NEVER invoked. We run:
#   0  -> derive slug (Haiku, ~$0.01)
#   (inject synthetic elicitation_summary.md)
#   3a-extract .. 4b-synthesize -> paper + benchmark + region YAMLs
#   5          -> web search enrichment
#   5b-da      -> dataset analysis (only if the row declares an HF dataset)
#   6..9       -> compose prompt, Opus scoring, report, review PDF
#
# Run from the anthropic_api_package_release/ directory with the
# `validity-global-south` conda env active and ANTHROPIC_API_KEY set
# (via .env or the environment).
#
# Usage:
#   ./manual_comparison/run_manual_comparison.sh                 # all ready rows
#   ./manual_comparison/run_manual_comparison.sh mrbench         # one row
#   STOP_AFTER=4b-synthesize ./manual_comparison/run_manual_comparison.sh mrbench
#   DRY=1 ./manual_comparison/run_manual_comparison.sh           # print plan only
# ============================================================================
set -euo pipefail

# === Row registry ==========================================================
# One entry per tuple, pipe-delimited:
#   name | pdf_path | seed_dir | hf_dataset | hf_config
# - name       : pipeline name = PDF stem; also the assessments/<name>/ dir.
# - pdf_path   : benchmark paper PDF (must already exist locally).
# - seed_dir   : holds deployment_description.txt + elicitation_summary.md.
# - hf_dataset : HF id for Step 5b dataset analysis, or "-" to skip 5b.
# - hf_config  : HF config/subset, or "-".
ROWS=(
  "mrbench|papers/mrbench.pdf|manual_comparison/row1_mrbench|-|-"
  # DA disabled: deepset/germanquad ships a custom loading script that datasets 4.x
  # can't load, so Step 5b can never run for it — assess on paper + web search only,
  # exactly like MRBench (keeps the two rows comparable).
  "germanquad|papers/germanquad.pdf|manual_comparison/row2_germanquad|-|-"
  # Rows 3 & 4 (2026-08 batch).
  # DailyDilemmas: DA enabled. kellycyy/daily_dilemmas loads cleanly (no remote-code
  # loader, datasets-server viewer live). Config pinned to the actual dilemmas subset
  # — leaving it blank auto-samples all 4 configs and burns most of the char budget on
  # the 14.6K-row Action_to_party_to_value mapping table instead of the 2.7K dilemmas.
  "dailydilemmas|papers/dailydilemmas.pdf|manual_comparison/row3_dailydilemmas|kellycyy/daily_dilemmas|Dilemmas_with_values_aggregated"
  # AraDiCE: DA left off. The cited repo QCRI/AraDiCE is an 8-row stub; the real
  # benchmark is fragmented across ~10 QCRI/AraDiCE-* sub-repos (dialect MMLU, BoolQ,
  # Culture, …) — DAing those would be multiple extra calls, so assess on paper + web.
  "aradice|papers/aradice.pdf|manual_comparison/row4_aradice|-|-"
  # Row 5 (2026-08 batch, tuple sent directly by the expert).
  # DisasterVQA: DA enabled. QCRI/DisasterVQA loads cleanly — single "default"/"train"
  # config, datasets-server viewer live, no remote-code loader — so 5b-da runs with no
  # modification (config left "-" since there's only one). It's a multimodal VQA set;
  # the lone `image` column comes back as a small ref (URL + dims), not raw bytes, so it
  # won't eat the char budget. DA profiles the rich text metadata (question, question_type,
  # disaster_type, region, groundtruth_answer, crisis_info_*) — directly on-point for the
  # flood / Argentina fit question (whether the benchmark's disaster + region coverage
  # matches the deployment).
  "disastervqa|papers/disastervqa.pdf|manual_comparison/row5_disastervqa|QCRI/DisasterVQA|-"
)

# === Step sequence (elicitation stages 1 / 2-questions / 2-summary omitted) =
STEPS_BUILD=(3a-extract 3a-assemble 3a-consolidate 3b-select 3b-synthesize \
             3c-verify 4a-template 4b-synthesize 5)   # 5b-da inserted after 5 if HF
STEPS_SCORE=(6 7 8 9)

# === Knobs =================================================================
ONLY_ROW="${1:-}"              # run just this row name (optional)
STOP_AFTER="${STOP_AFTER:-}"   # stop each row after this step (checkpointing)
DRY="${DRY:-0}"                # 1 = print the command plan, run nothing

# === Helpers ===============================================================
say() { printf '%s\n' "$*"; }

# Run a pipeline step (or just print it under DRY=1).
run_step() {
  local pdf="$1"; shift
  local step="$1"; shift
  if [[ "$DRY" == "1" ]]; then
    say "    + python run_pipeline.py $pdf --step $step $*"
  else
    say "  [$step]"
    python run_pipeline.py "$pdf" --step "$step" "$@"
  fi
}

# === Preflight =============================================================
[[ -f run_pipeline.py ]] || { say "ERROR: run from the anthropic_api_package_release/ dir."; exit 1; }
command -v qpdf >/dev/null 2>&1 || command -v pdftk >/dev/null 2>&1 \
  || { say "ERROR: need qpdf or pdftk on PATH for PDF splitting."; exit 1; }
if [[ "$DRY" != "1" ]]; then
  [[ -f .env || -n "${ANTHROPIC_API_KEY:-}" ]] \
    || { say "ERROR: ANTHROPIC_API_KEY not set (create .env or export it)."; exit 1; }
fi

# === Main loop =============================================================
for entry in "${ROWS[@]}"; do
  IFS='|' read -r name pdf seed_dir hf_dataset hf_config <<< "$entry"
  [[ -n "$ONLY_ROW" && "$ONLY_ROW" != "$name" ]] && continue

  say "=== ROW: $name ==="

  # --- Validate inputs; skip (or fail, if explicitly selected) when missing ---
  missing=""
  [[ -f "$pdf" ]] || missing="$missing $pdf"
  [[ -f "$seed_dir/deployment_description.txt" ]] || missing="$missing $seed_dir/deployment_description.txt"
  [[ -f "$seed_dir/elicitation_summary.md" ]] || missing="$missing $seed_dir/elicitation_summary.md"
  if [[ -n "$missing" ]]; then
    if [[ -n "$ONLY_ROW" ]]; then say "ERROR: missing inputs:$missing"; exit 1; fi
    say "  [skip] missing inputs:$missing"; continue
  fi

  # --- Step 0: derive slug (idempotent: reuses slug when the desc is unchanged) ---
  run_step "$pdf" 0 --use-case "$seed_dir/deployment_description.txt"

  if [[ "$DRY" == "1" ]]; then
    slug="<derived-slug>"
  else
    slug="$(cat "assessments/$name/active_slug.txt")"
  fi
  say "  slug: $slug"

  # --- Inject the synthetic (elicitation-skipped) summary ---
  if [[ "$DRY" == "1" ]]; then
    say "    + cp $seed_dir/elicitation_summary.md assessments/$name/$slug/elicitation_summary.md"
  else
    cp "$seed_dir/elicitation_summary.md" "assessments/$name/$slug/elicitation_summary.md"
    say "  injected elicitation_summary.md (elicitation stage skipped)"
  fi
  [[ "$STOP_AFTER" == "0" ]] && { say "  [stop-after 0]"; continue; }

  # --- Assemble the per-row step list (dataset analysis only when HF is set) ---
  steps=("${STEPS_BUILD[@]}")
  [[ "$hf_dataset" != "-" ]] && steps+=("5b-da")
  steps+=("${STEPS_SCORE[@]}")

  # --- Execute ---
  for step in "${steps[@]}"; do
    if [[ "$step" == "5b-da" ]]; then
      if [[ "$hf_config" != "-" ]]; then
        run_step "$pdf" 5b-da --hf-dataset "$hf_dataset" --hf-config "$hf_config"
      else
        run_step "$pdf" 5b-da --hf-dataset "$hf_dataset"
      fi
    else
      run_step "$pdf" "$step"
    fi
    [[ "$STOP_AFTER" == "$step" ]] && { say "  [stop-after $step]"; break; }
  done

  say "  -> assessments/$name/$slug/pdfs/review.pdf"
done

say "done."
