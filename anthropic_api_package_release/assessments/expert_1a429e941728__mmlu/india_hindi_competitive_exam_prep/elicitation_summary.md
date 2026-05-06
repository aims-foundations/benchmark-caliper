## Use Case
A Hindi-speaking graduate student in North India uses a mobile/enterprise AI application to prepare for central competitive examinations (e.g., UPSC, SSC, banking exams). The AI evaluates the student's responses and provides correct/incorrect labels plus explanatory feedback in Hindi. The goal is to assess whether MMLU — an English-language, US-designed benchmark — is a valid instrument for measuring the LLM's fitness in this deployment.

## Target Population
Geography: North India (states such as UP, Bihar, Rajasthan, MP), with focus on aspirants for centrally conducted examinations.
Language: Hindi (primary); limited English exposure; up to ~10% English code-mixing acceptable.
Role: Graduate-level student engaged in competitive exam preparation.
Demographic note: Hindi-medium educated background; curriculum shaped by Indian national and regional history, polity, and administrative traditions rather than US/Western academic conventions.

## Elicitation Responses

Q1 [IO]: For a graduate student in North India preparing for competitive job exams (e.g., UPSC, SSC, state PSC, banking exams), which subject areas are most critical — General Knowledge, Current Affairs, Indian Polity & Constitution, Hindi language proficiency, regional history of North Indian states (UP, Bihar, Rajasthan, MP), or Mathematics/Reasoning? Are there specific exam types (Central vs. state-level) that your deployment must prioritize?
A1: The most critical subject areas are General Knowledge, Current Affairs, History, and Mathematics/Reasoning, with supplementary coverage of Indian Polity & Constitution and Hindi language proficiency. The deployment focuses specifically on central government examinations (UPSC, SSC, etc.) rather than state-level PSCs.

Q2 [IC]: Competitive exam questions for North Indian students often draw on culturally specific knowledge — e.g., festivals like Chhath Puja, regional administrative units like tehsils or mandals, state-specific historical figures, or North Indian legal and land-revenue traditions. Does your deployment expect the AI to handle this kind of regionally grounded content, or is the focus on pan-India general knowledge content?
A2: Central competitive examinations require both regionally grounded Indian content (including North India–specific elements) and pan-India general knowledge; the AI must handle both dimensions.

Q3 [OO]: When the AI provides feedback on a student's response, what should that feedback look like — a simple correct/incorrect label, an explanation of why an answer is right or wrong, a hint toward the correct answer, or an encouragement message in Hindi? If the benchmark only scores label accuracy, there may be a mismatch with deployment needs.
A3: The AI must produce both a correct/incorrect label and a substantive explanation of why the answer is right or wrong, and this feedback must be delivered in Hindi. A label-only benchmark output is insufficient for this deployment.

Q4 [IC]: Since the target student has limited English exposure, would it be a problem if some benchmark questions contain English technical terms, code-mixed phrasing, or assume familiarity with English-medium textbook conventions?
A4: Moderate code-mixing with English technical terms is acceptable provided it does not exceed approximately 10% of the content. Fully English-medium question phrasing or heavy reliance on English-medium academic conventions would be a problem.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | MMLU's 57 subjects are anchored in a US academic curriculum and contain no coverage of Indian Polity, Indian History, Current Affairs relevant to India, or Hindi language proficiency — the exact domains that central competitive exams prioritise. |
| IC | HIGH | Individual MMLU items embed US-default factual and cultural assumptions (US law, US history, Western civic norms) that are directly irrelevant or misleading for an Indian competitive-exam context requiring both pan-India and North India–specific knowledge. |
| IF | HIGH | MMLU is entirely in English, while the deployment requires Hindi-medium interaction with at most ~10% English code-mixing; the script and language distribution of benchmark inputs do not match deployment reality. |
| OO | HIGH | MMLU scores label accuracy only (A/B/C/D MCQ), whereas the deployment requires the model to produce a correct/incorrect verdict plus a Hindi-language explanatory rationale — a fundamentally different output taxonomy. |
| OC | HIGH | MMLU ground-truth labels were validated by English-speaking, US-educated annotators; for Indian GK, Polity, and regional history items that MMLU does not contain, there is no representative Indian annotator pool, making label correctness for an India-centric use case unverifiable. |
| OF | MODERATE | Both MMLU and the deployment use text-based MCQ as the input vehicle, which is a partial match; however, MMLU's label-only output form diverges from the required Hindi explanatory-feedback output, raising external validity concerns at the output side. |

## Flagged Gaps

1. **Indian curriculum coverage absence**: MMLU contains no subject track for Indian Polity & Constitution, Indian History (ancient/medieval/modern), Indian Geography, or Hindi language proficiency — all core components of UPSC/SSC syllabi. Downstream search should verify whether any MMLU subject can be mapped even partially to these domains.

2. **Hindi-language availability**: MMLU has no official Hindi-language version and no ported variant with verified Hindi translations as of its 2021 release. Search should check whether community-translated Hindi MMLU datasets exist and whether their quality has been independently evaluated.

3. **North India–specific and pan-India regional content**: Central exam GK sections include content on Indian administrative structures (tehsils, districts, panchayati raj), Indian festivals, state-wise demographic data, land-revenue history, and contemporary Indian current affairs. MMLU has no analogue for this content; search should identify whether any Indian-origin benchmark (e.g., IndicMMLU, IndiGO, or exam-specific question banks) covers these sub-domains.

4. **Explanatory feedback in Hindi**: MMLU's design produces only a predicted label; the deployment requires Hindi-language rationale generation. Search should investigate whether LLMs evaluated on MMLU have been tested for Hindi explanation quality, and whether any rubric or benchmark exists for evaluating Hindi-language exam-prep feedback.

5. **Code-mixing threshold and script handling**: The student tolerates up to ~10% English code-mixing in Devanagari-dominant text. Search should look for evidence on how leading LLMs handle Hinglish or lightly code-mixed Hindi in educational contexts, and whether MMLU-derived prompts translated into Hindi preserve acceptable code-mix ratios.

6. **Annotator representativeness for Indian GK labels**: For any India-adapted version of MMLU or related benchmark, downstream search should check whether Indian subject-matter experts (particularly those familiar with UPSC/SSC exam standards) participated in label validation, or whether labels were generated/verified by non-Indian annotators or LLMs.