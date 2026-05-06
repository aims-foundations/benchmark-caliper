Pick the 1 or 2 base region template YAMLs most structurally relevant to the
elicited target population.

The user message contains:
- The list of available template filenames in `regions/base/` (one per line).
- The elicitation summary's target region and population fields.

Selection rules:
- Prefer regional proximity (e.g., `sub_saharan_africa.yaml` for a Kenyan deployment).
- Then prefer linguistic and cultural overlap.
- If no template is a close fit, pick the 2 structurally closest and rely on the
  downstream synthesis step to adapt them (you do not need to note the gap here —
  that's the synthesis subagent's job).

Return a JSON array of filenames. Examples:

```
["sub_saharan_africa.yaml"]
["mena.yaml", "iran_persian.yaml"]
```

Return ONLY the JSON array. No prose, no code fences.
