# Reading Guide

## Suggested order

### 1. Infrastructure (read first — everything depends on these)

| File | What to look for |
|------|-----------------|
| `client.py` | API call mechanics, cost tracking, rate limiting, dry-run mode |
| `prompts.py` | How `.md` prompt templates get loaded and rendered |

### 2. Core pipeline (read top-down, following data flow)

| File | Steps | What to look for |
|------|-------|-----------------|
| `run_pipeline.py` | 0-8 | Main orchestrator. Read `_run_single_step()` and `main()` last — start with the step functions in order (0, 1, 2, 3a, 3b, 3c, 4a, 4b, 5, 5b, 6, 7, 8) |
| `personas.py` | used by 7 | Persona definitions and expected scores (useful to read alongside the Opus scoring prompt) |

### 3. Helper scripts (read alongside the step that calls them)

| File | Called by | Notes |
|------|----------|-------|
| `scripts/parse_llm_output.py` | many steps | Fence stripping + JSON/YAML extraction. Read early — you'll see `_run_script("parse_llm_output.py", ...)` everywhere |
| `scripts/parse_elicitation_questions.py` | step 2-questions | |
| `scripts/assemble_elicitation_answers.py` | step 2-summary | Pairs questions with expert answers |
| `scripts/verify_quotes.py` | step 3c | Quote verification against PDF pages |
| `scripts/compose_prompt.py` | step 6 | Assembles the final Opus prompt from all artifacts. Worth reading carefully — it's where everything converges |
| `scripts/format_results.py` | step 8 | Scoring JSON to markdown report |

### 4. Dataset analysis (read as a group — step 5b)

| File | Role |
|------|------|
| `scripts/dataset_analysis/hf_metadata.py` | HF API metadata fetch |
| `scripts/dataset_analysis/content_sample.py` | Stratified example sampling |
| `scripts/dataset_analysis/audio_stats.py` | Audio-specific stats (conditional) |

### 5. Expert validation wrappers (read last — they wrap the core pipeline)

| File | Role |
|------|------|
| `run_expert_stage1.py` | CSV ingestion, runs steps 0/1/2-questions per tuple |
| `run_expert_stage2.py` | Parses answer CSV, runs steps 2-summary through 8 per tuple |
| `generate_expert_forms.py` | Generates Google Forms for expert elicitation |

## Cross-referencing tips

- **Prompts live in `prompts/`** — when a step calls `prompts.load("X")`, read `prompts/X.md` alongside the step function
- **`compose_prompt.py` + `prompts/opus_scoring_framing.md`** are the two halves of what Opus sees in step 7
- **`run_pipeline.py` step functions** reference assessment directories under `assessments/<paper_stem>/<slug>/` — knowing the directory layout helps when reading artifact I/O
- **`active_slug.txt`** is the mechanism that connects the expert wrappers to the core pipeline — grep for it if the indirection is confusing
