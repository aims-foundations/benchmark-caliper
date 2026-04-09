# Web Client Prompts for Validity Analysis

These prompts let you run the benchmark validity analysis framework using only a
web-based LLM chat interface (ChatGPT, Claude web, Gemini, etc.) — no coding,
no API keys, no setup required.

## What You Need

1. A benchmark paper PDF
2. Access to a capable LLM chat interface (Claude, ChatGPT, etc.)
3. (Optional) A region YAML file from `regions/` for richer regional context

## Which Version to Use

### Single-Prompt Version (`single_prompt.md`)
- **Best for**: Quick assessments, users who want simplicity
- **How it works**: Upload PDF + paste one prompt. Get results in one turn.
- **Trade-off**: No separate quote provenance verification step. The LLM
  extracts quotes and scores in a single pass, which means paraphrasing can
  creep in unnoticed.
- **Quality**: ~80% of the full pipeline

### Two-Prompt Version (`two_prompt_step1.md` + `two_prompt_step2.md`)
- **Best for**: Higher-quality assessments, when accuracy matters
- **How it works**: Upload PDF + paste Step 1 prompt. Copy the output, then
  paste Step 2 prompt. Get results.
- **Advantage**: Quote extraction and scoring are separated, preserving the
  provenance chain that prevents "evidence laundering."
- **Quality**: ~90% of the full pipeline

## What's NOT Included (vs. Full Pipeline)

These web client prompts omit:
- **Web search enrichment** (Step 3): The LLM relies on parametric knowledge for regional context. You can partially compensate by pasting regional context
  from a `regions/*.yaml` file.
- **Mechanical verification** (Step 1c scripts): No quote count or ID checks.
- **Multiple runs for robustness**: The full pipeline supports prompt variants (A/B/C). You can manually re-run with variant instructions if desired.

## Usage

### Single Prompt
1. Open your LLM chat
2. Upload the benchmark paper PDF
3. Copy the contents of `single_prompt.md`
4. Replace `{REGION}` with your target region name
5. (Optional) Replace `{REGIONAL_CONTEXT}` with content from a region YAML
6. Paste and send

### Two Prompts
1. Open your LLM chat
2. Upload the benchmark paper PDF
3. Paste `two_prompt_step1.md` — this extracts quotes and structures data
4. Wait for the response (the extracted summary)
5. Paste `two_prompt_step2.md` with your target region filled in
6. Wait for the JSON results
