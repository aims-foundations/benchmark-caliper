## Use Case
An AI system assists Arab-country high school (G10–12) Arabic teachers in grading student essays written in Modern Standard Arabic (MSA), using a seven-trait rubric (relevance, organization, vocabulary, style, development, mechanics, grammar). The benchmark dataset (LAILA) was collected in Qatar but targets MSA writing, which is standardized across the Arab world, although grading conventions and rubric structures vary by country.

## Target Population
Geography: Arab countries broadly (Qatar as benchmark source; deployment extends to Egypt, Saudi Arabia, Jordan, Lebanon, Morocco, and others). Sub-national/country variation is explicitly relevant. Language: Modern Standard Arabic (written). Occupation: High school Arabic teachers (G10–12). Demographic notes: Teachers operate under diverse national curricula; some (e.g., Egypt) use holistic, rubric-free grading rather than trait-based scoring.

## Elicitation Responses

Q1 [OC]: The benchmark essays were scored by annotators in Qatar. For teachers in other Arab countries — such as Egypt, Saudi Arabia, Jordan, Lebanon, or Morocco — would you expect grading standards to differ meaningfully on traits like style, vocabulary, or development? For instance, would a Lebanese teacher apply different expectations for formal register or rhetorical organization than a Qatari one, and should the system's scoring reflect each country's local norms or a pan-Arab standard?
A1: Cross-country grading standards for MSA writing are not expected to differ significantly; the shared goal is well-formed MSA prose and the end product is indistinguishable by nationality. A pan-Arab standard is considered appropriate rather than country-specific norms.

Q2 [IO]: In your deployment, are teachers expected to grade essays on all seven trait dimensions, or do different countries or curricula emphasize a subset? Are there grading criteria important to teachers in target countries that might not be captured by these seven traits?
A2: Different countries may apply different grading criteria. Notably, Egypt does not use a structured rubric — grading is holistic and evaluator-dependent — meaning the seven-trait ontology may not map onto Egyptian classroom practice. Other countries may similarly de-emphasize or re-weight specific traits.

Q3 [OO]: Should the system produce a single score per trait or express uncertainty and provide justification when an essay falls between levels?
A3: The system should express confidence and provide explanatory justification alongside each score so teachers can intervene when essays fall between levels, rather than presenting a single authoritative label. Pure label output is insufficient for the deployment need.

Q4 [IC]: Could essay prompts and expected content knowledge differ enough across Arab countries — e.g., Egyptian history, Gulf social norms, Levantine literary traditions — that a model trained on Qatari prompts might misjudge relevance or development for locally grounded content?
A4: Yes, if the model is unfamiliar with locally grounded content knowledge (history, social norms, literary traditions specific to a non-Qatari context), it may misjudge relevance and development scores for essays written in response to prompts from other national curricula.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The seven-trait rubric ontology does not universally match national curricula — Egypt uses holistic, rubric-free grading — so the benchmark's trait structure may be irrelevant or incomplete for large segments of the target deployment population. |
| IC | HIGH | Benchmark essays use Qatari prompts and cultural/educational contexts; for teachers in Egypt, the Levant, or North Africa, locally grounded content (history, literary canon, social norms) may fall outside the model's training distribution, risking systematic misjudgment of relevance and development. |
| IF | LOWER | Deployment is text-only in MSA, matching the benchmark's modality and script; no infrastructure mismatch is anticipated. |
| OO | HIGH | The benchmark produces discrete trait scores/labels, but the deployment requires confidence estimates and explanatory justification alongside each score; the scoring output ontology as designed does not satisfy the teacher-facing use case. |
| OC | MODERATE | The user considers pan-Arab MSA standards sufficiently uniform to reduce annotator-population mismatch concerns, but Qatari annotators may still embed implicit Gulf-curriculum expectations in holistic judgments; this warrants verification rather than dismissal. |
| OF | HIGH | The benchmark outputs labels/scores, but teachers need uncertainty flagging and score-range or rationale output; the output form mismatch between benchmark and deployment is a direct validity threat for practical use. |

## Flagged Gaps

1. **Egypt (holistic grading)**: Egypt is a major Arab education system where essay grading is rubric-free and evaluator-dependent. The benchmark's seven-trait structure has no direct equivalent; downstream search should investigate whether any Arabic AES work has been validated against Egyptian national curriculum grading practices.

2. **Non-Qatari prompt topics and content domains**: The benchmark's essay prompts are set in a Qatari educational context. Downstream search should look for evidence on whether LAILA-trained models have been tested on essays responding to prompts about Egyptian, Levantine, or North African history, literature, or social topics — and whether relevance/development scoring degrades for such content.

3. **Confidence/uncertainty output**: The benchmark provides point-score labels, not confidence intervals or justification text. Downstream search should investigate whether any Arabic AES systems built on LAILA (or comparable datasets) have been augmented with uncertainty quantification or rationale generation, and how such outputs have been evaluated by teachers.

4. **Country-level rubric variation**: Saudi Arabia, Jordan, Lebanon, and Morocco each have distinct national Arabic language curricula. Downstream search should identify whether any of these countries' official rubric structures have been documented and compared against LAILA's seven-trait schema, to flag specific trait mismatches (e.g., whether "style" or "development" are assessed differently or absent).

5. **Annotator pool composition within Qatar**: The benchmark is described as designed by the target population, but the specific annotator profiles (teachers, curriculum specialists, nationalities) within Qatar are not detailed. Downstream search should verify whether annotators reflected diverse Arab-country backgrounds or were exclusively Qatari-curriculum aligned, which would affect the generalizability of ground-truth labels.

6. **Dialectal influence on MSA scoring**: While the user affirms MSA is uniform, students in some countries (e.g., Morocco, where Darija and French influence written Arabic) may produce MSA with distinct interference patterns. Downstream search should investigate whether LAILA's mechanics and vocabulary scoring handles non-Gulf MSA writing patterns without systematic bias.