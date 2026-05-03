#!/usr/bin/env python3
"""Debug script to diagnose scoring JSON parse failure."""
import json
import re

TRACE = ("assessments/expert_c799688856da__afridoc_mt_document_level_mt_corpus"
         "_for_african_languages/ethiopia_amharic_rural_finance/traces/7_score.jsonl")

with open(TRACE) as f:
    obj = json.loads(f.read())

raw = obj["output"]
first_nl = raw.index("\n") + 1
last_fence = raw.rindex("\n```")
body = raw[first_nl:last_fence]
lines = body.split("\n")


# Test json_repair on this output
import re
fence = re.search(r'```(?:json)?\s*\n(.*?)\n```', raw, re.DOTALL)
cleaned = fence.group(1).strip()
cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)

from json_repair import repair_json
repaired = repair_json(cleaned, return_objects=True)
print(f"json_repair result type: {type(repaired).__name__}")
if isinstance(repaired, dict):
    print(f"Top-level keys: {list(repaired.keys())}")
    dims = repaired.get("dimensions", {})
    print(f"Dimensions: {list(dims.keys())}")
    pg = repaired.get("practical_guidance")
    print(f"practical_guidance type: {type(pg).__name__}")
    if isinstance(pg, dict):
        print(f"  keys: {list(pg.keys())}")
    rs = repaired.get("remediation_suggestions")
    print(f"remediation_suggestions type: {type(rs).__name__ if rs else 'MISSING'}")
    if rs is None and isinstance(pg, dict):
        rs_nested = pg.get("remediation_suggestions")
        print(f"  nested in practical_guidance? {rs_nested is not None}")
