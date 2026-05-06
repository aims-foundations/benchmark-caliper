You are extracting validity-relevant quotes from page {page_num} of a benchmark
paper. A single-page PDF is attached to this message as a document block — read
it and extract from that attached page only.

Extract ALL factual claims relevant to these categories:

1. Task taxonomy / test case categories
2. Data sources and collection
3. Data format and preprocessing
4. Label categories and output types
5. Annotation process (annotators, demographics, agreement)
6. Evaluation metrics and output modality
7. Stated limitations
8. Authors and affiliations

Output a single JSON object with this shape:

{{
  "quotes": [
    {{
      "text": "<EXACT verbatim text from the PDF - complete sentences>",
      "page": {page_num},
      "category": "<one of: task_taxonomy, data_sources, data_format, label_categories, annotation_process, evaluation_metrics, stated_limitations, authors_affiliations>"
    }}
  ],
  "page_summary": "<1-2 sentence summary of what this page covers>",
  "continues_from_previous": <true|false>,
  "continues_to_next": <true|false>
}}

Continuity flags:
- `continues_from_previous`: true if the page opens mid-sentence or mid-paragraph — i.e. the first visible line starts with a lowercase word, a dangling clause, or clearly references material not on this page. False if it starts a new section, heading, or self-contained sentence.
- `continues_to_next`: true if the page ends mid-sentence or mid-paragraph — last visible line breaks off without a terminal period/punctuation, or ends on an em-dash/colon that demands a follow-up. False if it ends cleanly (end of section, end of paragraph, or closing punctuation).

Rules:
- Quote COMPLETE sentences only — never truncate mid-sentence.
- If a sentence spans from the previous page, include the full sentence visible on this page.
- If a claim spans multiple sentences, quote all of them together.
- Include statistical facts, methodological claims, design decisions, and limitations.
- Skip: related-work citations, model performance tables, and figure captions unless they contain methodological claims.
- If this page has no relevant content (references, full-page figures, etc.), return
  {{"quotes": [], "page_summary": "...", "continues_from_previous": false, "continues_to_next": false}}.

Output ONLY the JSON object, with no surrounding prose or code fences.
