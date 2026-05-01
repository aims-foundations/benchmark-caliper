## Use Case
A Hindi-speaking postgraduate/PhD-qualified teacher in North India uses an LLM-powered mobile or enterprise application to evaluate student multiple-choice responses, assign scores (positive for correct, negative for incorrect), and provide feedback. The AI must handle MCQ content drawn from Hindi-medium and translated English-medium syllabi across CBSE and multiple state boards (UP, MP, Rajasthan, Bihar, etc.).

## Target Population
Geography: North India (Hindi belt states — UP, MP, Rajasthan, Bihar, and surrounding regions); sub-national variation across state board curricula is relevant.
Language: Hindi (Devanagari script, standard Khari Boli register expected in professional assessment contexts).
Occupation/role: Postgraduate- or PhD-qualified Hindi-medium teacher with 0–20+ years of teaching experience.
Demographic notes: Evaluation norms are broadly shared across boards, but curricular content references (canonical texts, historical figures, regional knowledge) diverge across state and central board syllabi.

## Elicitation Responses

Q1 [IO]: Your deployment involves evaluating student responses and assigning scores — tasks that require the AI to judge partial credit, borderline answers, and reasoning quality, not just match a correct label. Does your assessment context involve open-ended or long-form student answers (e.g., essay-style, analytical responses), structured short answers, or primarily factual single-item questions? Understanding the mix will clarify whether the benchmark under assessment covers the response types your teacher actually encounters.
A1: The deployment is exclusively MCQ-based. Each question has exactly one correct answer; scoring uses a positive-mark / negative-mark (penalty) scheme. No open-ended, partial-credit, or rubric-based evaluation is involved.

Q2 [OO]: Should the AI system support graded scoring, binary correct/incorrect judgments, or qualitative rubric-based feedback? And would the teacher expect the AI's scoring rationale to be expressed in standard Hindi or would informal/regional Hindi be acceptable?
A2: All questions are MCQ-type in Hindi with a single correct answer; scoring is binary (correct/incorrect with corresponding positive/negative marks). No gradations or rubric language are required.

Q3 [IC]: Does your deployment target a specific board or institution type, or must the AI handle content across multiple curricula? Would student responses reference canonical Hindi literary or regional historical figures that the benchmark's content might frame differently?
A3: The deployment must cover all Hindi state and central board syllabi (CBSE plus UP, MP, Rajasthan, Bihar, etc.). Questions may also be sourced from English-medium boards, provided they are translated into Hindi and aligned with Hindi-board content norms. Curricular breadth across boards is required.

Q4 [OC]: Are the kinds of answers students produce and the mark schemes teachers use likely to reflect North Indian academic norms that might diverge from the benchmark annotators' keying of correct answers?
A4: No significant divergence is expected; evaluation schemas across Indian boards and states are broadly similar. North Indian academic norms are unlikely to produce systematically different ground-truth judgments from the benchmark's answer keys for factual MCQ content.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | MMLU's 57 subject taxonomy was designed for a US academic context; it lacks subject categories central to Hindi-medium Indian curricula (e.g., Hindi literature, Indian classical studies, state-board history/civics, regional language arts), while including many US-specific professional domains (US law, US history) irrelevant to this deployment. |
| IC | HIGH | Individual question items assume US cultural defaults, US historical referents, and English-language canonical texts; translated or ported Hindi-board content (Tulsidas, Premchand, Indian constitutional history, regional geography) is absent, creating substantial construct-irrelevant variance for North Indian students and teachers. |
| IF | HIGH | MMLU is English-only with no Hindi-language items; the deployment requires Devanagari-script Hindi input and output throughout, meaning the benchmark's input signal distribution fundamentally mismatches the deployment's language and script requirements. |
| OO | MODERATE | The MCQ binary-scoring requirement (correct/incorrect) aligns structurally with MMLU's label-based output ontology; however, MMLU's answer keys were designed for US-context correct answers, and some subject-domain categories carry different "correct" interpretations in an Indian educational context. |
| OC | MODERATE | The user confirms that evaluation schemas across Indian boards are broadly similar, reducing annotator-population mismatch risk for factual content; however, MMLU annotators were not drawn from the Hindi-medium North Indian teacher community, and any culturally loaded items (ethics, social sciences, history) remain at risk of label misalignment. |
| OF | LOWER | Both MMLU and the deployment use MCQ with a single correct-answer label as output; the output form matches structurally, though the language of presentation (Hindi vs. English) remains a separate concern captured under IF. |

## Flagged Gaps

1. **Hindi-language coverage**: MMLU contains no Hindi-language items. Downstream search should investigate whether any Hindi-adapted or Hindi-translated version of MMLU exists (e.g., IndicMMLU, Anudesh, or similar Hindi NLP benchmarks) and how faithfully such translations preserve item intent and cultural referents.

2. **Indian curricular subject taxonomy**: MMLU's 57 subjects do not map to CBSE or state-board subject taxonomies. Search should identify what subject categories appear in Class 10–12 and postgraduate Hindi-medium syllabi across CBSE, UP Board, MP Board, Rajasthan Board, and Bihar Board, and which of these are absent or only partially covered by MMLU.

3. **Canonical Hindi literary and cultural content**: Items referencing Tulsidas, Kabir, Premchand, Mirabai, Indian constitutional history, or regional historical figures are structurally absent from MMLU. Search should probe whether any existing LLM benchmark covers this content and how state-board exam question banks frame such items.

4. **Translation quality and construct fidelity**: If MMLU items are translated into Hindi for this deployment, the translation process introduces its own validity risks (idiomatic distortion, register mismatch, Devanagari rendering of technical terms). Search should find any published work on MMLU Hindi translation quality or known failure modes.

5. **Negative marking (penalty scoring) alignment**: MMLU was designed for zero-shot and few-shot accuracy measurement, not penalty-based scoring. Search should assess whether the benchmark's item difficulty distribution and distractor design are appropriate for a negative-marking regime, where guessing behavior and distractor plausibility carry higher stakes.

6. **Sub-national board variation in content norms**: Despite the user's indication that evaluation schemas are broadly similar, state boards (particularly UP and Bihar) have distinct prescribed text lists and historical framings. Search should surface any documented divergence in correct-answer expectations for history, civics, and Hindi literature items across these boards.