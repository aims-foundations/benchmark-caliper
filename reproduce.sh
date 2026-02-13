#!/usr/bin/env bash
#
# reproduce.sh — Reproduce validity analysis results
#
# Usage:
#   bash reproduce.sh                          # Generate reports + heatmap from existing results
#   bash reproduce.sh --evaluate BENCHMARK REGION  # Run a new LLM evaluation, then generate reports
#
# Prerequisites:
#   pip install pyyaml numpy matplotlib
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="$SCRIPT_DIR/results"
BENCHMARKS_DIR="$SCRIPT_DIR/benchmarks"
REGIONS_DIR="$SCRIPT_DIR/regions"

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

usage() {
    cat <<EOF
Usage:
  bash reproduce.sh                                Generate reports + heatmap from existing results
  bash reproduce.sh --evaluate BENCHMARK REGION    Evaluate a benchmark for a target region via LLM
  bash reproduce.sh --report RESULT_NAME           Generate report for a single result (no .json)
  bash reproduce.sh --validate                     Compare LLM scores against ground-truth
  bash reproduce.sh --csv                          Export results to CSV for human review

Examples:
  bash reproduce.sh --evaluate helm southeast_asia
  bash reproduce.sh --evaluate afrimedqa sub_saharan_africa
  bash reproduce.sh --report helm_sea
  bash reproduce.sh --validate

Available benchmarks:  $(ls "$BENCHMARKS_DIR"/*.yaml 2>/dev/null | xargs -I{} basename {} .yaml | tr '\n' ' ')
Available regions:     $(ls "$REGIONS_DIR"/*.yaml 2>/dev/null | xargs -I{} basename {} .yaml | tr '\n' ' ')
EOF
    exit 0
}

check_deps() {
    python3 -c "import yaml, numpy, matplotlib" 2>/dev/null || {
        echo "Missing dependencies. Install with:"
        echo "  pip install pyyaml numpy matplotlib"
        exit 1
    }
}

# ──────────────────────────────────────────────
# Evaluate a benchmark-region pair using an LLM
# ──────────────────────────────────────────────

run_evaluation() {
    local benchmark="$1"
    local region="$2"
    local bench_file="$BENCHMARKS_DIR/${benchmark}.yaml"
    local region_file="$REGIONS_DIR/${region}.yaml"
    local result_file="$RESULTS_DIR/${benchmark}_${region}.json"

    if [[ ! -f "$bench_file" ]]; then
        echo "Error: Benchmark file not found: $bench_file"
        echo "Available benchmarks:"
        ls "$BENCHMARKS_DIR"/*.yaml 2>/dev/null | xargs -I{} basename {} .yaml | sed 's/^/  /'
        exit 1
    fi
    if [[ ! -f "$region_file" ]]; then
        echo "Error: Region file not found: $region_file"
        echo "Available regions:"
        ls "$REGIONS_DIR"/*.yaml 2>/dev/null | xargs -I{} basename {} .yaml | sed 's/^/  /'
        exit 1
    fi

    mkdir -p "$RESULTS_DIR"

    echo "======================================================================"
    echo "  Evaluating: ${benchmark} -> ${region}"
    echo "======================================================================"
    echo ""
    echo "Benchmark: $bench_file"
    echo "Region:    $region_file"
    echo "Output:    $result_file"
    echo ""

    # Build the evaluation prompt from the template, benchmark, region, and framework
    local prompt
    prompt=$(cat <<PROMPT_EOF
I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Benchmark Information
$(cat "$bench_file")

## Target Region
$(cat "$region_file")

## Validity Framework
$(cat "$SCRIPT_DIR/framework.yaml")

## Instructions

Analyze this benchmark's validity for the target region across all 6 dimensions
(input_ontology, input_content, input_form, output_ontology, output_content, output_form).

For each dimension, follow the checklist in the framework and provide a score from 1-5.

Return ONLY a single JSON object (no markdown fences) with this structure:
{
  "benchmark": "${benchmark}",
  "region": "${region}",
  "dimensions": {
    "<dimension_key>": {
      "score": <1-5>,
      "justification": "<2-4 sentences>",
      "checklist_responses": {"<id>": "<response>"},
      "evidence_quotes": ["<quote from benchmark docs>"],
      "confidence": "<high|medium|low>",
      "information_gaps": ["<what info was missing>"],
      "requires_expert_verification": ["<findings needing expert input>"]
    }
  },
  "overall_summary": "<3-5 sentence summary>",
  "risk_assessment": "<high|medium|low>",
  "remediation_suggestions": "<key actions>",
  "highest_concern_dimensions": ["<dim keys>"],
  "strongest_dimensions": ["<dim keys>"]
}
PROMPT_EOF
    )

    # Try Claude CLI first, fall back to Anthropic API
    if command -v claude &>/dev/null; then
        echo "Using Claude CLI..."
        echo "$prompt" | claude --output-format json -p - > "$result_file"
    elif [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
        echo "Using Anthropic API..."
        local escaped_prompt
        escaped_prompt=$(echo "$prompt" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

        curl -s https://api.anthropic.com/v1/messages \
            -H "content-type: application/json" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: 2023-06-01" \
            -d "{
                \"model\": \"claude-sonnet-4-5-20250929\",
                \"max_tokens\": 8192,
                \"messages\": [{\"role\": \"user\", \"content\": $escaped_prompt}]
            }" | python3 -c "
import sys, json
resp = json.load(sys.stdin)
text = resp['content'][0]['text']
# Extract JSON from response (handle possible markdown fences)
if '\`\`\`json' in text:
    text = text.split('\`\`\`json')[1].split('\`\`\`')[0]
elif '\`\`\`' in text:
    text = text.split('\`\`\`')[1].split('\`\`\`')[0]
parsed = json.loads(text.strip())
print(json.dumps(parsed, indent=2))
" > "$result_file"
    else
        echo "No LLM backend available. To run evaluations, either:"
        echo "  1. Install Claude CLI:    npm install -g @anthropic-ai/claude-code"
        echo "  2. Set API key:           export ANTHROPIC_API_KEY=sk-ant-..."
        echo ""
        echo "Alternatively, manually fill in prompt_template.md and save the JSON to:"
        echo "  $result_file"
        exit 1
    fi

    echo ""
    echo "Evaluation saved to: $result_file"
    echo ""

    # Generate report for this result
    local result_name="${benchmark}_${region}"
    echo "Generating report..."
    python3 "$SCRIPT_DIR/generate_report.py" --result "$result_name"
    echo ""
}

# ──────────────────────────────────────────────
# Generate all reports from existing results
# ──────────────────────────────────────────────

generate_all() {
    echo "======================================================================"
    echo "  Generating reports and visualizations"
    echo "======================================================================"
    echo ""

    if [[ ! -d "$RESULTS_DIR" ]] || [[ -z "$(ls "$RESULTS_DIR"/*.json 2>/dev/null)" ]]; then
        echo "No results found in $RESULTS_DIR."
        echo "Run an evaluation first:"
        echo "  bash reproduce.sh --evaluate <benchmark> <region>"
        exit 1
    fi

    local count
    count=$(ls "$RESULTS_DIR"/*.json 2>/dev/null | wc -l)
    echo "Found $count result files."
    echo ""

    echo "[1/3] Generating markdown reports and radar charts..."
    python3 "$SCRIPT_DIR/generate_report.py"
    echo ""

    echo "[2/3] Generating heatmap..."
    python3 "$SCRIPT_DIR/generate_heatmap.py"
    echo ""

    echo "[3/3] Validating against ground truth..."
    python3 "$SCRIPT_DIR/validate.py"
    echo ""

    echo "======================================================================"
    echo "  Done. Outputs in: $RESULTS_DIR"
    echo "======================================================================"
    echo ""
    echo "Generated files:"
    echo "  - results/*_report.md       Per-benchmark markdown reports"
    echo "  - results/all_radar.png     Combined radar chart"
    echo "  - results/validity_heatmap.png/pdf   Heatmap visualization"
    echo ""
}

# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

if [[ $# -eq 0 ]]; then
    check_deps
    generate_all
    exit 0
fi

case "${1:-}" in
    --help|-h)
        usage
        ;;
    --evaluate)
        if [[ $# -lt 3 ]]; then
            echo "Usage: bash reproduce.sh --evaluate BENCHMARK REGION"
            echo "Example: bash reproduce.sh --evaluate helm southeast_asia"
            exit 1
        fi
        check_deps
        run_evaluation "$2" "$3"
        ;;
    --report)
        if [[ $# -lt 2 ]]; then
            echo "Usage: bash reproduce.sh --report RESULT_NAME"
            exit 1
        fi
        check_deps
        python3 "$SCRIPT_DIR/generate_report.py" --result "$2"
        ;;
    --validate)
        check_deps
        python3 "$SCRIPT_DIR/validate.py"
        ;;
    --csv)
        check_deps
        python3 "$SCRIPT_DIR/validate.py" --csv
        ;;
    *)
        echo "Unknown option: $1"
        usage
        ;;
esac
