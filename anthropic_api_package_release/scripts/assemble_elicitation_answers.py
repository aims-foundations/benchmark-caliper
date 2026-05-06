#!/usr/bin/env python3
"""Combine elicitation questions and answers into a Q/A text block.

The same assembler serves both stdin-interactive mode (answers collected
locally in run_pipeline.py) and the future web UI (answers posted per-question
and written to a JSON file).

Inputs:
    --questions questions.json  — [{"id": "Q1", "dimension": "IC", "question": "..."}, ...]
    --answers   answers.json    — {"Q1": "...", "Q2": "...", ...}

Output on stdout:
    Q1 [IC]: <question>
    A1: <answer>

    Q2 [OO]: ...
    A2: ...
"""

import argparse
import json
import sys


# Entry point: loads questions + answers from disk, validates completeness,
# then serializes them into a numbered Q/A text block for the step-2 summary prompt.
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", required=True)
    ap.add_argument("--answers", required=True)
    args = ap.parse_args()

    # === Load inputs ===
    # questions is an ordered list (preserves question numbering for the output block)
    # answers is a flat dict keyed by question ID for O(1) lookup
    with open(args.questions) as f:
        questions = json.load(f)
    with open(args.answers) as f:
        answers = json.load(f)

    # === Validate completeness ===
    # Every question must have a matching answer before we emit anything —
    # a partial Q/A block would silently mislead the downstream LLM summarizer.
    missing = [q["id"] for q in questions if q["id"] not in answers]
    if missing:
        print(f"ERROR: missing answers for: {missing}", file=sys.stderr)
        sys.exit(1)

    # === Build Q/A blocks ===
    # Output format mirrors the expected structure in the step-2 summary prompt:
    #   Q1 [IC]: <question text>
    #   A1: <answer text>
    # Blocks are separated by a blank line so the LLM sees discrete Q/A pairs.
    blocks = []
    for q in questions:
        qid = q["id"]
        # Strip the leading "Q" to get the bare numeral used in the A-line label
        # (e.g., "Q3" -> "3" so we can write "A3:")
        n = qid.lstrip("Q")
        blocks.append(f"{qid} [{q['dimension']}]: {q['question']}\nA{n}: {answers[qid]}")
    print("\n\n".join(blocks))


if __name__ == "__main__":
    main()
