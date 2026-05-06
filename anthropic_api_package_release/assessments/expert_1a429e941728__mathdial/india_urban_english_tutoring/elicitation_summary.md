## Use Case
A GPT-4 model assists one-on-one tutoring sessions in which its outputs are augmented with a human tutor's input; a professional teacher then evaluates the pedagogical quality of the combined response, specifically whether it provides adequate guidance to the student. The system is assessed using the MATHDIAL benchmark to determine whether augmented GPT-4 responses meet teacher-acceptable standards.

## Target Population
High-end professional teachers working in Grades 1–8 in major Indian metropolitan cities (Delhi, Mumbai). English-fluent, operating within the Indian educational system (NCERT/CBSE context). Demographically: likely experienced, formally credentialed educators accustomed to exam-oriented, teacher-directed pedagogical norms. Single-language deployment (English text only).

## Elicitation Responses

Q1 [IO]: For your Grade 1–8 teachers in Delhi and Mumbai, do the student mistake scenarios covered by the benchmark need to reflect the Indian curriculum (e.g., NCERT/CBSE topics, Indian arithmetic conventions like the Indian place-value system with lakhs and crores, or standard algorithms taught differently in Indian textbooks)? Or would curriculum-agnostic math errors be sufficient for evaluating pedagogical quality?
A1: Curriculum-agnostic math errors are considered sufficient for evaluating pedagogical quality; alignment with Indian curriculum specifics is not required.

Q2 [IC]: The benchmark's student-tutor conversations are drawn from a particular linguistic and cultural context that may not reflect Indian classroom dynamics. For your professional teachers in Indian metros, would the depicted student mistakes, student communication styles, or classroom interaction norms feel realistic and recognisable — or do you expect meaningful differences?
A2: The mathematical content feels broadly familiar, but the interaction dynamics are meaningfully mismatched. Indian students tend to be brief, deferential, and less likely to verbalize reasoning; teachers tend toward direct, exam-oriented correction rather than extended Socratic dialogue. Procedure-heavy learning patterns and language-related misunderstandings common in Indian classrooms are underrepresented in the benchmark's Western-origin dialogues.

Q3 [OO]: The benchmark scores pedagogical quality along multiple dimensions. For your teachers evaluating acceptability of an augmented response, which dimensions matter most — and are there missing dimensions your teachers would actually judge on?
A3: The eight benchmark dimensions are considered necessary and sufficient for the evaluation task. The single most critical dimension is "providing guidance"; no additional dimensions are required.

Q4 [OC]: The benchmark's ground-truth annotations were produced by a likely non-Indian annotator pool. Do you expect your professional Indian teachers' judgments of good guidance to systematically differ from Western educator norms?
A4: Yes, meaningful differences are expected due to Indian cultural context, teaching style, and pedagogy — particularly around preferences for direct correction versus Socratic probing and the weighting of exam-readiness relative to conceptual exploration.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | LOWER | The user confirmed curriculum-agnostic errors suffice and the benchmark's eight pedagogical categories are accepted as necessary and sufficient, removing the main source of ontological misalignment. |
| IC | HIGH | The user explicitly identified that Indian classroom interaction norms — deferential student style, direct teacher correction, procedure-heavy patterns — diverge from the Western-origin dialogue instances in the benchmark, creating construct-irrelevant variance in individual datapoints. |
| IF | LOWER | Both deployment and benchmark are English text-only on mobile/enterprise platforms; no modality or script mismatch exists. |
| OO | MODERATE | The benchmark's eight output dimensions are accepted as sufficient, but the primacy of "providing guidance" in the Indian context may not be weighted commensurately in the benchmark's scoring rubric, creating potential scoring emphasis misalignment. |
| OC | HIGH | The user expects systematic divergence between Indian professional teachers' quality judgments and those of the benchmark's likely non-Indian annotators, particularly on direct-correction vs. Socratic probing and exam-readiness weighting. |
| OF | LOWER | Both benchmark and deployment operate in text-based, open-ended tutoring dialogue format; no output-form mismatch is present. |

## Flagged Gaps

1. **Indian classroom interaction norms in benchmark dialogues**: The benchmark's student-simulating LLM was prompted on Western tutoring conventions. Downstream search should investigate whether MATHDIAL's student simulation captures deferential, brief, low-verbalization student behavior typical of Indian metro classrooms, or whether it defaults to the more expressive, reasoning-out-loud style common in US/UK tutoring datasets.

2. **Annotator provenance**: MATHDIAL annotations were produced by crowdsourced or institutional annotators whose regional/cultural background is undisclosed. Search should establish whether any Indian educators were involved in annotation, particularly for the "guidance quality" dimension, given the user's expectation of systematic divergence.

3. **Guidance dimension operationalization**: The user identifies "providing guidance" as the dominant evaluation criterion, but the benchmark treats it as one of eight co-equal dimensions. Search should investigate how MATHDIAL defines and weights its guidance-related annotations (e.g., scaffolding vs. direct correction) and whether that definition aligns with exam-oriented direct correction styles valued by Indian professional teachers.

4. **Socratic vs. directive pedagogy weighting**: The benchmark is explicitly designed around scaffolding and avoidance of premature solution revelation — a constructivist, Socratic orientation. Indian metro teachers may systematically rate more directive responses higher. Search should look for evidence of how MATHDIAL's pedagogical stance interacts with non-Western, exam-driven teaching philosophies.

5. **Sub-national variation within Indian metros**: Delhi and Mumbai represent distinct linguistic and socioeconomic teaching environments. The user did not differentiate between these cities; search should investigate whether pedagogical norms or teacher expectations differ meaningfully between these metros and whether any India-specific tutoring benchmarks exist that capture this variation.