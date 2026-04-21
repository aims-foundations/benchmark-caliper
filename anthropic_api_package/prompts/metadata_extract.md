You are extracting lightweight metadata from the first 1-2 pages of a benchmark
paper (title page, abstract, introduction). A PDF containing only these pages is
attached to this message as a document block.

The goal is to gather just enough context for elicitation — not to perform full
extraction. Downstream steps will process the entire paper later.

Extract these fields. If a field cannot be determined from the available pages,
write "UNKNOWN".

Output as a structured text block with exactly this format:

- name: [short lowercase identifier, no spaces — e.g. "sea-helm", "afriqa", "culturebench"]
- full_name: [full benchmark title as written in the paper]
- year: [publication year]
- domain: [what the benchmark evaluates, 1-2 sentences]
- languages: [comma-separated list of languages mentioned]
- primary_region: [the geographic/cultural region the benchmark targets]
- porting_strategy: [one of: ground_up, adapted, mixed, translation, parallel, regional_exams, none]
- brief_description: [2-3 sentence summary of what this benchmark does and how it was built]
- source_culture: [one of: designed by target population, transferred from Western context, mixed, unclear]

Porting strategy definitions:
- ground_up: benchmark was built from scratch for the target region/culture
- adapted: an existing benchmark was modified for a new region (not just translated)
- mixed: some tasks are original, others are adapted or translated
- translation: an existing benchmark was directly translated
- parallel: parallel versions were created for multiple regions simultaneously
- regional_exams: benchmark draws from region-specific exams (e.g. university entrance exams)
- none: no cross-cultural porting involved (single-region benchmark)

Output ONLY the structured text block, with no surrounding prose or code fences.
