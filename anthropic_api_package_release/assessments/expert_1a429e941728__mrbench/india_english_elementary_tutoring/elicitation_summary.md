## Use Case
A GPT-4 model augmented by human tutors is deployed as a one-on-one tutoring assistant via mobile application or enterprise software for students in grades 1–8 in metropolitan Indian cities. The primary evaluation goal is to assess whether students are satisfied with GPT-4's tutoring responses within the mathematics domain, with responses co-authored by human tutors.

## Target Population
- **Geography:** Metropolitan cities in India (no specific sub-national region specified beyond "metropolitan")
- **Language:** English (fluent)
- **Grade cohort:** Grades 1–8 (ages approximately 6–14)
- **Curriculum alignment:** Indian national curriculum (NCERT-aligned, including conventions such as lakhs/crores, rupees, local contextual word problems)
- **Role:** Students as primary end-users; human tutors as co-authors and secondary evaluators of response quality

## Elicitation Responses

Q1 [IO]: Your students are in grades 1–8 in metropolitan India. Should the tutoring system handle content tied to the Indian school curriculum (e.g., NCERT-aligned topics, Indian numeral naming conventions like lakhs and crores, word problems referencing rupees or local contexts like train timetables)? Or is the math content entirely curriculum-agnostic in your deployment?
A1: The system must be tied to the Indian school curriculum. NCERT-aligned content, Indian numeral naming conventions, and locally grounded word problems are all required — the deployment is not curriculum-agnostic.

Q2 [IC]: Word problems and tutoring examples in Western benchmarks often use culturally specific contexts (e.g., baseball statistics, US grocery prices, American school scenarios). In your deployment, would students encounter these kinds of culture-distant examples, or would the system generate problems grounded in familiar Indian everyday contexts — like cricket scores, local market transactions, or school fee calculations?
A2: The system should generate problems grounded in familiar Indian everyday contexts (e.g., cricket, local markets, school fees). Culture-distant Western examples are not appropriate for this deployment.

Q3 [OC]: The benchmark's pedagogical quality labels were annotated by human raters — but the actual measure of success is student satisfaction. Who in the deployment context are the right judges of a "good" tutor response, and would their judgments align with the benchmark's annotators?
A3: The appropriate judges are human tutors (co-authors) and student engagement signals. Satisfaction judgments from a metropolitan Indian child are expected to largely align with benchmark annotators, though some divergence may occur due to cultural and educational context differences.

Q4 [OO]: The benchmark scores responses on pedagogical dimensions (guidance, tone, mistake identification), but the deployment goal is student satisfaction — which may depend on culturally specific warmth or communication style. Would a pedagogically correct but culturally distant or overly formal response still count as satisfying?
A4: No. A response must be both pedagogically sound and culturally appropriate to count as satisfying. Overly formal or culturally distant responses, even if pedagogically correct, would not meet the deployment's success criterion.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | MRBench derives from Western/general-context math datasets (MathDial, Bridge), and the deployment explicitly requires NCERT-aligned Indian curriculum categories — a clear ontological mismatch in topic coverage and numeral conventions. |
| IC | HIGH | Benchmark instances likely embed Western cultural contexts (US school scenarios, dollar-denominated problems), while the deployment requires Indian everyday contexts (cricket, rupees, local markets); this is a confirmed gap from A2. |
| IF | LOWER | Both benchmark and deployment are text-only in English, and the target population is fluent English-speaking; no modality or script mismatch exists. |
| OO | HIGH | The benchmark's eight pedagogical dimensions do not map cleanly onto student satisfaction as the deployment's success criterion; A4 confirms that cultural appropriateness and warmth are necessary conditions for a "good" response that the benchmark's output taxonomy does not capture. |
| OC | MODERATE | Human tutors and student engagement are the intended judges, and A3 indicates partial alignment with benchmark annotators — but cultural and educational context differences mean ground-truth labels from non-Indian raters may diverge on tone and style judgments for this population. |
| OF | LOWER | The benchmark outputs labels and scores which serve as intermediate evaluation signals; the deployment's output is free-form tutor text, but this mismatch is partially bridged by the human tutor co-authorship layer and is not the primary validity risk. |

## Flagged Gaps

1. **NCERT curriculum coverage:** MRBench is derived from MathDial and Bridge datasets, neither of which is aligned to the Indian national curriculum. Downstream search should investigate whether any math tutoring benchmark covers NCERT Grade 1–8 topics, including lakhs/crores notation, Indian standard algorithm conventions, and rupee-based word problems.

2. **Indian cultural context in benchmark instances:** The source datasets are likely populated with Western contextual framings. Web search should check whether MathDial or Bridge contain any India-specific word problems or whether their student-error typologies reflect Indian classroom pedagogy.

3. **Satisfaction vs. pedagogical quality as a construct:** MRBench measures pedagogical correctness, not student satisfaction or engagement. Downstream search should identify whether any validation study links MRBench scores to learner-reported satisfaction, particularly for non-Western student populations.

4. **Metropolitan India sub-national variation:** The target population is defined only as "metropolitan India," which spans vastly different linguistic, socioeconomic, and pedagogical contexts (e.g., Mumbai vs. Delhi vs. Bengaluru). No sub-national granularity was specified; downstream search should flag whether any benchmark or validation study distinguishes between Indian metropolitan cohorts in terms of math tutoring expectations or communication style norms.

5. **Annotator pool for MRBench:** It is unknown whether MRBench's human annotators included any Indian educators or students. Downstream search should investigate the annotator demographics to assess how representative they are of the target population, particularly for the tone and human-likeness dimensions that bear most directly on satisfaction.

6. **Cultural norms around tutor communication style:** A4 confirms that warmth, encouragement, and culturally appropriate register are required for satisfaction — dimensions that vary between Indian classroom norms and the likely Western or generic academic context assumed by the benchmark's annotators. Search should investigate empirical work on Indian pedagogical communication expectations in primary/middle school settings.