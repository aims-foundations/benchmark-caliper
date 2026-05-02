## Use Case
An AI system assists high school students (Grades 10–12) in Arab countries — primarily Qatar — to edit and revise Arabic essay drafts before formal grading. The system provides formative feedback on writing quality, ideally including natural-language revision suggestions rather than numeric scores alone.

## Target Population
Primary geography: Qatar (G10–12 high school students); secondary reach across Arab countries (e.g., Egypt, Saudi Arabia, Jordan, Lebanon). Language: Modern Standard Arabic (MSA), with regional dialect influence possible. Role: student writers preparing academic essays. Curriculum context: Qatar national curriculum is the primary anchor, though the system may serve students under different Arab national curricula with partially divergent norms.

## Elicitation Responses

Q1 [IO]: Does your deployment target students across multiple Arab countries or is it focused on Qatar, and do essay prompts, curricula, and writing conventions differ meaningfully across those countries?
A1: The system can support students in other Arab countries but is most reliable for Qatar, since essay prompts and curricula differ across countries. Sub-national and cross-country curricular variation exists and limits generalizability beyond Qatar.

Q2 [OC]: Whose standards should define quality on traits like style, vocabulary, and development — are local curriculum bodies' scoring conventions in different Arab countries meaningfully different from Qatar's?
A2: Local curriculum bodies and teacher communities exist in each country, but how much their scoring conventions diverge from Qatar's is uncertain and would need further research. In principle, MSA norms are shared across the Arab world, but practical rubric differences may exist.

Q3 [OO]: Does the system need to produce actionable natural-language revision suggestions, or are numeric trait scores sufficient for students?
A3: Actionable revision suggestions with natural-language explanations of why points were lost on each trait are more useful; a scored rubric alone is insufficient for the target student population.

Q4 [IC]: Do student essay prompts resemble those in the benchmark, or do they extend to genres like literary analysis, religious texts, or cultural commentary?
A4: The benchmark covers only 8 explanatory/persuasive prompts, which is too narrow — Qatari and other Arab high school students are also assigned literary analysis, religious-text engagement, and cultural commentary essays that require different evaluative knowledge.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark covers only 2 essay types (explanatory/persuasive) drawn from a US middle-school context; the deployment requires coverage of literary analysis, religious texts, and cultural commentary genres that are absent from the benchmark's category inventory. |
| IC | HIGH | Benchmark essays are English-language US student writing from grades 7–10; the deployment targets Arabic-language Qatari/Arab students writing to culturally embedded prompts, creating strong construct-irrelevant variance in individual datapoints. |
| IF | HIGH | The benchmark is English-only; the deployment operates entirely in Arabic (MSA with potential dialectal influence), a different script, morphological structure, and orthographic system — a fundamental signal-distribution mismatch. |
| OO | HIGH | The benchmark scores with a holistic+attribute rubric designed for English writing; the deployment requires natural-language revision suggestions, not numeric labels, and the scoring taxonomy was not designed for Arabic rhetorical or curricular norms. |
| OC | HIGH | Ground-truth labels were produced by annotators judging English essays by US curriculum standards; Qatar/Arab curriculum teachers may apply different quality standards for MSA conventions, organization, and style, making label transfer highly unreliable. |
| OF | HIGH | The benchmark outputs numeric trait scores and labels; the deployment explicitly requires free-text, actionable revision suggestions with explanatory rationale — a direct mismatch in output form that the benchmark cannot validate. |

## Flagged Gaps

1. **Arabic-language essay corpora**: No benchmark data exists in Arabic in ASAP++. Downstream search should investigate whether any Arabic automated essay scoring (AES) datasets exist (e.g., Arabic IELTS writing, Gulf/Qatar national exam corpora) that could serve as a more valid proxy.

2. **Qatar national curriculum writing standards**: The Qatar Ministry of Education's Arabic-language writing rubrics and grading criteria are the operative ground truth for this deployment. Web search should locate published rubric documentation or curriculum frameworks from Qatar's national curriculum (e.g., ADEC/MOE Qatar Arabic language standards, Grades 10–12).

3. **Cross-Arab rubric divergence**: The uncertainty about how Saudi, Egyptian, Jordanian, and Lebanese scoring conventions differ from Qatar's is a concrete gap. Search should look for comparative studies of Arabic writing instruction norms or pan-Arab exam rubrics (e.g., Arabic Tawjihi, Egyptian Thanaweya Amma writing components).

4. **Genre coverage gap — literary analysis, religious text commentary**: The benchmark has zero coverage of these genres. Search should identify whether any AES benchmarks or Arabic NLP resources cover literary/Quranic text analysis essays, which are common in Arab high school curricula.

5. **MSA vs. dialectal influence in student writing**: Qatari students may blend Gulf Arabic features into MSA writing. Search should investigate whether any NLP tools or datasets account for this code-mixing in formal student writing, as the benchmark assumes monolingual English with no dialectal variation.

6. **Actionable feedback generation validation**: Since the deployment output is natural-language revision suggestions (not scores), search should identify any Arabic writing feedback generation systems or human-in-the-loop evaluation frameworks that have been validated with Arab student populations, as the ASAP++ label-based evaluation framework is entirely misaligned with this output requirement.