Pick the 1 or 2 benchmark YAMLs most structurally relevant to the paper
described in the user message. Prefer matching `porting_strategy` first, then
`domain`, then `primary_region`.

The user message contains:
- A compact manifest of available reference YAMLs (one line per file).
- Key attributes of the paper being synthesized (stated domain, apparent
  porting_strategy, primary region).

Return a JSON array of filenames. Examples:

```
["afrimedqa.yaml"]
["helm.yaml", "seahelm.yaml"]
```

Return ONLY the JSON array. No prose, no code fences, no explanation.
