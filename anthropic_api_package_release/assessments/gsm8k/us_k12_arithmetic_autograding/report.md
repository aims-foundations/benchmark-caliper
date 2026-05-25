## Deployment Context

We are a US edtech company building an auto-grading system for American schools. Teachers assign arithmetic word problems and students submit numerical answers through our text-based platform. Our LLM independently solves the same problem and compares its answer to the student's submission. We need to evaluate whether the LLM reliably produces correct final numerical answers to arithmetic word problems.

# Validity Analysis: gsm8k
**Target context:** US K-8 Arithmetic Auto-Grading Platform (Grades 3–8)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ✓ | 4 | Minor gaps | high |
| Input Form ✓ | 5 | Strong alignment | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content | 3 | Moderate gaps | medium |
| Output Form | 3 | Moderate gaps | high |
| **Average** | **3.2** | | |

> ⚠ = highest concern &nbsp; ✓ = strongest dimension

### Dimension Key

| Abbr. | Dimension | Definition |
|:-----:|-----------|------------|
| IO | Input Ontology | Whether the benchmark's test case categories cover the query types expected in deployment. |
| IC | Input Content | Whether individual datapoint content is culturally and contextually appropriate for the target region. |
| IF | Input Form | Whether the input signal encoding (text, audio, image parameters) matches deployment conditions. |
| OO | Output Ontology | Whether the benchmark's output categories and scoring criteria reflect regionally valid decision boundaries. |
| OC | Output Content | Whether ground-truth labels align with the judgments of regional stakeholders. |
| OF | Output Form | Whether the expected output modality matches regional deployment needs and accessibility. |

## Overall Summary

GSM8K is a partially valid evaluation for the US K-8 Arithmetic Auto-Grading Platform's deployment context. It is strongly aligned on input form, input content, and the basic chain-of-thought output pattern, all of which match the platform's text-only English, US-contextualized infrastructure. However, the two HIGH-priority dimensions (input ontology, output ontology) both show significant gaps: (1) GSM8K's problem-type coverage omits user-confirmed essential categories — standalone unit conversion, basic geometry (perimeter/area), and tabular/chart data interpretation — and under-represents grade 3–4 single-step difficulty; (2) GSM8K's exact-match scoring does not stress-test the answer-equivalence and tolerance-based normalization the platform's grading logic must handle. The benchmark provides a useful but incomplete reliability signal — necessary for assessing multi-step arithmetic reasoning in grades 5–8 but insufficient for the platform's full problem distribution and grading requirements. Saturation on frontier LLMs further reduces its discriminative value.

## Practical Guidance

### What This Benchmark Measures

GSM8K can reliably evaluate an LLM's ability to solve US-contextualized multi-step arithmetic word problems requiring 2–8 reasoning steps, particularly in the grades 5–8 difficulty range. Its strongest dimensions (input_form: 5, input_content: 4) make it well-suited as a baseline reliability signal for the platform's English, text-only, US-dollar-and-imperial-unit problem profile. For multi-step ratio, percent, rate, and proportional reasoning problems (DATASET-D15, D16, D18, D20), GSM8K provides a representative evaluation.

### Construct Depth

The benchmark probes final-answer correctness on multi-step arithmetic but does not probe at depth: (a) problem-type coverage is bounded to narrative arithmetic — omitting geometry, standalone unit conversion, and data interpretation (input_ontology: 2); (b) scoring is exact-match without equivalence normalization, so it does not probe whether the LLM handles representational variants the platform must grade (output_ontology: 2); (c) saturation on frontier models means a high score reflects coverage of a solved sub-problem rather than evidence of full reliability. The benchmark provides surface-level coverage of multi-step reasoning rather than a comprehensive reliability probe.

### What Else You Need

To complete the assessment, the platform should supplement GSM8K with: (1) ASDiv-W [WEB-7] for explicit Geometry and UnitTrans problem-type coverage, addressing the input_ontology gap; (2) GSM-Plus integer-decimal-fraction conversion subset [WEB-9] for stress-testing answer-equivalence handling, addressing the output_ontology gap; (3) bespoke evaluation items authored by US K-8 educators for data interpretation from tables/bar charts, which no existing benchmark covers (input_ontology / input_form gap); (4) GSM1K [WEB-15] for contamination-controlled multi-step arithmetic evaluation given GSM8K saturation; (5) Easy2Hard-Bench / E2H-GSM8K [WEB-10] for difficulty-stratified evaluation approximating grade-band breakdown, addressing the grade 3–4 calibration gap; (6) sample re-annotation by US K-8 educators on edge cases to address output_content demographic uncertainty.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Input ontology is the HIGH-priority dimension for this deployment, and GSM8K shows significant gaps. The benchmark's scope is explicitly limited to multi-step grade-school arithmetic word problems [Q9, Q11], with no systematic subtask taxonomy by problem type. Three user-confirmed essential problem types — measurement/unit conversion, basic geometry (perimeter/area), and data interpretation from tables/bar charts — are absent or only incidentally present. The dataset analysis confirms zero standalone unit conversion problems (conversion appears only as embedded sub-steps in D7, D8) and zero geometry formula problems (D9 uses area as input, D10 computes prism volume incidentally). Data interpretation from tables/charts is structurally impossible in this text-only benchmark. Additionally, the difficulty distribution skews to 2–8 step problems [WEB-4, WEB-5], under-representing grade 3–4 single-step arithmetic (DATASET-D17, D18, D19 show the lower-bound complexity is still upper-grade-band).

**Strengths:**
- Strong coverage of multi-step ratio, percent, rate, and proportional reasoning aligned to grades 6–8 (DATASET-D15, D16, D18, D20)
- Linguistic diversity within the arithmetic domain is an explicit design goal [Q9], reducing template-driven overfitting risk
- Explicit positioning as grade-school level with elementary concepts [Q11] aligns with the broad deployment domain

**Checklist:**

- **IO-1**: Required categories per elicitation: single-step multiplication/division (grades 3–4), multi-step arithmetic, ratio/proportion, percent, rate, measurement/unit conversion, time, basic geometry (perimeter/area), and simple data interpretation from tables/bar charts. — _Sources: WEB-1, WEB-3_
- **IO-2**: Confirmed omissions: (a) standalone unit conversion — only embedded incidentally (DATASET-D7, D8); (b) geometry formula application — absent (DATASET-D9, D10 nearest, neither computes perimeter/area); (c) tabular/chart data interpretation — structurally impossible in text-only format; (d) single-step grade 3–4 calibration — paper acknowledges 175B model needs 2 orders of magnitude more data to reach 80% [Q50], and minimum sampled complexity is 2-step (DATASET-D29, D30). — _Sources: Q9, WEB-7, WEB-8, DATASET-D7, DATASET-D8, DATASET-D9, DATASET-D10_
- **IO-3**: No clearly irrelevant categories identified; all problem types in GSM8K (multi-step arithmetic, ratio, percent, rate) are within the platform's stated scope. — _Sources: Q9, Q11_
- **IO-4**: Documented gaps: unit conversion (HIGH), geometry (HIGH), data interpretation (HIGH/structural), grade 3–4 single-step calibration (MODERATE). These harm content validity because the benchmark systematically under-represents categories the platform actually serves. — _Sources: Q50, WEB-4, DATASET-D17, DATASET-D29_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q9] 'We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts.' (p.2)
- [Q11] 'GSM8K solutions depend only on elementary concepts, so achieving high test performance is a tractable goal.' (p.2)
- [Q19] 'GSM8K is larger, provides natural language solutions, and consists of problems that on average require more steps to solve.' (p.4)
- [Q50] 'It appears likely that the 175B model would require at least two additional orders of magnitude of training data to reach an 80% solve rate.' (p.6)

*Web sources:*
- [WEB-4] GSM8K problems each require between 2 and 8 solution steps; calibrated toward bright middle-school student
- [WEB-7] ASDiv explicitly includes 'Geometry' and 'UnitTrans' problem categories that GSM8K lacks
- [WEB-8] No K-8-calibrated benchmark combining arithmetic word problems with table/chart inputs exists; TAT-QA is finance-domain

*Dataset analysis:*
- DATASET-D7, D8: Unit conversion appears only as incidental embedded sub-step, never as primary task
- DATASET-D9, D10: No problem applies perimeter/area formulas; closest is rectangular prism volume as intermediate step
- DATASET-D17, D18, D19, D20: Lower-end sampled problems still require algebra or compound percent — well above grades 3–4
- DATASET-D29, D30: Simplest sampled problems are 2-step, not single-step

</details>

**Information gaps:**
- Statistical frequency of unit-conversion-like and geometry-adjacent problems in the full 8,500-item dataset (only 47 main examples sampled)
- Whether any test-split problems differ in type distribution from the train split observed

**Requires expert verification:**
- Mapping of confirmed essential problem types to specific CCSS-M codes (e.g., 3.OA, 4.MD, 6.RP) for precise gap accounting
- Platform-internal data interpretation modality (text-serialized vs. image-rendered tables)

---

### Input Content — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input content is a LOWER-priority dimension and is one of GSM8K's stronger fits. Dataset analysis confirms US dollar amounts, imperial units (pounds, feet, inches, cubic feet), American names, and familiar US school/sports/consumer scenarios across the sample (DATASET-D1, D2, D3, D4, D5). One metric instance (DATASET-D11, kilograms) appears, broadly matching the elicitation's description of a 'small minority' of metric problems. Minor concerns: annotator demographics are not documented [Q103, Q104], and GPT-3-generated seed questions [Q110] partly shaped problem framing rather than curated by US educators. Cherry-picking for diversity in appendix samples [Q127] limits confidence about systematic representativeness, but the empirical evidence strongly supports cultural alignment.

**Strengths:**
- US monetary contextualization is pervasive — dollars, cents, tax, savings scenarios (DATASET-D1, D4, D6, D27)
- Imperial units dominate with occasional metric, matching platform distribution (DATASET-D2, D3, D11)
- Linguistic diversity is an explicit design principle with template-reuse detection [Q9, Q113]
- American school, sports, and consumer scenarios match deployment profile (DATASET-D5, D1, D32)

**Checklist:**

- **IC-1**: Inputs require US-typical cultural knowledge — dollar pricing, American school scenarios, US sports (football scoring in DATASET-D5). This aligns with the deployment target. — _Sources: DATASET-D1, DATASET-D5_
- **IC-2**: Cultural alignment is strong: dataset analysis confirms predominantly US contextualization (DATASET-D1, D2, D4, D5) matching the elicitation's description of platform problems as 'almost entirely US-contextualized.' — _Sources: DATASET-D1, DATASET-D2, DATASET-D4, DATASET-D5_
- **IC-3**: Minimal Western-non-US content. Metric units appear sporadically (DATASET-D11) but do not constitute a systematic mismatch given the elicitation acknowledges some metric problems exist in science-adjacent platform content. — _Sources: DATASET-D11_
- **IC-4**: INSUFFICIENT DOCUMENTATION — annotator demographics are not reported beyond identifying Upwork and Surge AI [Q103, Q104]. Would need demographic data on contractor pool to confirm US-schooled framing.
- **IC-5**: Content issues are limited: undocumented annotator demographics and GPT-3-seeded generation [Q110, Q111] introduce mild risk that some problem framings were not curated by US K-8 educators, but empirical evidence does not surface concrete misalignments. — _Sources: Q103, Q104, Q110_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q9] 'We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts.' (p.2)
- [Q103] 'We initially collected a starting set of a thousand problems and natural language solutions by hiring freelance contractors on Upwork (upwork.com).' (p.15)
- [Q104] 'We then worked with Surge AI (surgehq.ai), an NLP data labeling platform, to scale up our data collection.' (p.15)
- [Q110] 'To assist contractors with writing questions, we provided seed questions automatically generated from a few-shot prompted 175B GPT-3 model.' (p.15)
- [Q113] 'To ensure contractors were not re-using problem templates, we computed pairwise similarity scores between problems and used this to provide feedback to contractors.' (p.15)

*Dataset analysis:*
- DATASET-D1: US birthday party with brand-name candies and dollar prices
- DATASET-D2: Imperial weight (pounds) in pet scenario
- DATASET-D5: American football scoring — culturally US-specific
- DATASET-D11: Single metric (kilogram) example — matches elicitation's 'small minority'
- DATASET-D32: Linguistic diversity across domains (sports, food, finance, ecology)

</details>

**Information gaps:**
- Annotator demographics (geographic location, native language, US-schooled status)
- Frequency of metric vs. imperial unit problems across the full 8,500-item dataset

---

### Input Form — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
Input form is a LOWER-priority dimension and aligns nearly perfectly. Both benchmark and platform are text-only, English-language, US-standard mathematical notation (DATASET-D33 shows the consistent calculator-annotation format). No script, modality, or language mismatch exists. The calculator-annotation training format [Q40] and natural-language chain-of-thought solutions [Q32, Q33] are structurally congruent with the LLM-as-solver deployment pattern. The only minor caveat is that the socratic config (DATASET-D31) provides sub-question scaffolding that doesn't match deployment problem format, but this is a configuration choice the platform can avoid.

**Strengths:**
- Text-only English format exactly matches platform infrastructure [Q9]
- Natural-language chain-of-thought solutions match LLM-as-solver deployment pattern [Q32, Q33]
- Calculator-annotation format provides clean step-by-step computation (DATASET-D33)
- No script or notation mismatch — Arabic numerals, standard US math notation throughout

**Checklist:**

- **IF-1**: Signal distributions match exactly: both are text-only English prose with US-standard mathematical notation (DATASET-D33). — _Sources: Q9, Q32, DATASET-D33_
- **IF-2**: Regional infrastructure (US edtech platform) fully supports text-only LLM I/O; no capture-specification differences apply. — _Sources: Q32_
- **IF-3**: Domain-specific form: chain-of-thought reasoning with calculator annotations [Q40, Q119] matches the platform's expected LLM solving pattern. One caveat: data interpretation problems may involve image-rendered tables in deployment, which GSM8K cannot represent — but this is captured under input ontology rather than form. — _Sources: Q40, Q119, DATASET-D33, DATASET-D31_
- **IF-4**: No material form mismatches for the text-only problem subset. Modality gap for table/chart inputs is real but more appropriately categorized as an ontology gap (table reading is a problem type GSM8K lacks). — _Sources: DATASET-D31_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q9] 'We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts.' (p.2)
- [Q32] 'First, we focus attention on the space of natural language solutions, as this is a richer and more general solution format than pure mathematical expressions.' (p.5)
- [Q33] 'This choice enables our models to develop verbal analytical skills and to produce solutions that are more readily interpretable by humans.' (p.5)
- [Q40] 'To mitigate this issue, we train all models to use a calculator by injecting calculation annotations into the training set.' (p.6)
- [Q119] 'During training, there is no special distinction between the annotated tokens and the rest of the solution: they are all just tokens.' (p.17)

*Dataset analysis:*
- DATASET-D33: Calculator annotation format `<<expr=result>>` visible throughout solutions
- DATASET-D31: Socratic config adds sub-question scaffolding — diverges from deployment format; main config should be used

</details>

**Information gaps:**
- Platform's exact rendering of data-interpretation problems (text-serialized vs. image-rendered tables) — affects whether any IF gap exists for that subset

**Requires expert verification:**
- Platform team confirmation of chain-of-thought surfacing to students/teachers and table-rendering modality

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Output ontology is the second HIGH-priority dimension and shows significant misalignment. GSM8K's correctness criterion reduces to a single extracted numerical string with binary correct/incorrect judgment based solely on final answer match [Q31, Q60]. The standard scoring pipeline strips currency symbols and units [WEB-6] but does not implement fraction-decimal equivalence, rounding tolerance, or mixed-number normalization — a structural mismatch with the platform's partial normalization logic that must handle representational equivalences (e.g., '1/2' vs. '0.5', '$2.50' vs. '2.50'). GSM-Plus's findings [WEB-9] confirm this is a real LLM failure mode: all 25 tested models showed significant drops on integer-decimal-fraction perturbations. The dataset analysis surfaces conditions that generate these equivalences (decimal currency in DATASET-D6, D27; fractions in DATASET-D23, D24, D25; comma-formatted answers in DATASET-D21, D22), but the scoring schema doesn't stress-test them.

**Strengths:**
- Decision rule is mathematically objective — final answer correctness is unambiguous for integer answers [Q31, Q60]
- Token-level verifier provides interpretable per-token judgment (DATASET-D33) [Q72, Q73, Q147]
- Clean `#### N` answer format makes extraction unambiguous (DATASET-D13, D30)

**Checklist:**

- **OO-1**: Output label is a single numerical string with binary correct/incorrect judgment [Q31, Q60]. Categories are mathematically universal and regionally relevant. — _Sources: Q31, Q60_
- **OO-2**: Missing categories for the deployment: no representation of answer equivalence forms (fraction↔decimal, mixed↔improper, currency formatting, rounding tolerance, unit-stripped vs. unit-included). The platform's grading logic needs these; the benchmark schema does not encode them. — _Sources: WEB-6, WEB-9, DATASET-D6, DATASET-D23, DATASET-D21_
- **OO-3**: No categories encode non-regional values. The gap is structural (missing equivalence handling) rather than value-laden. — _Sources: Q31_
- **OO-4**: Stakeholder-driven redesign would mean augmenting evaluation with equivalence-class scoring (e.g., GSM-Plus integer-decimal-fraction subset [WEB-9]) rather than redesigning core categories. — _Sources: WEB-9_
- **OO-5**: Documented taxonomy issue: exact-match scoring [Q29, Q46] without equivalence normalization is a structural validity gap — the benchmark's construct (final answer correctness) is operationalized more narrowly than the deployment requires. Confidence is high because both verbatim quotes and web sources confirm the scoring pipeline lacks equivalence logic. — _Sources: Q29, Q46, WEB-6_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q29] 'At test time, we judge performance by autoregressively sampling a single low temperature solution and checking whether the final answer is correct.' (p.5)
- [Q31] 'Verifiers are trained to judge the correctness of solutions, with the training signal determined solely by whether or not the solution reached the correct final answer.' (p.5)
- [Q46] 'Test performance is determined by a single low temperature (T = 0) sample for each test problem.' (p.6)
- [Q60] 'Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer.' (p.7)

*Web sources:*
- [WEB-6] GSM8K standard pipeline strips currency symbols and units but does not implement fraction-decimal equivalence, rounding tolerance, or mixed-number normalization
- [WEB-9] GSM-Plus integer-decimal-fraction conversion perturbation causes significant performance drops in all 25 tested LLMs — confirms equivalence handling is a real failure mode

*Dataset analysis:*
- DATASET-D6, D27: Decimal dollar amounts in inputs but final answers are integers, masking equivalence-handling requirement
- DATASET-D23, D24, D25: Fractional multipliers in reasoning but integer final answers
- DATASET-D21, D22: Comma-formatted answer strings in annotations ('2,250'; '333,200.00') require format normalization not exercised by exact-match scoring

</details>

**Information gaps:**
- Frequency of non-integer final answers (fractions, mixed numbers) in the full test split — sample shows nearly all integers, suggesting low frequency

**Requires expert verification:**
- Platform's exact tolerance thresholds and normalization logic for cross-comparison with GSM-Plus-style evaluation

---

### Output Content — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Output content is MODERATE priority. Label quality is reasonable for the core arithmetic types: dedicated re-solving QC found 1.7% disagreement [Q107], which authors estimate as the breaking-error rate, while acknowledging subtle errors may be more frequent [Q109]. The dataset analysis confirms clean integer labels with consistent `#### N` extraction (DATASET-D13, D30). However, several concerns: (a) annotator demographics are not documented [Q103, Q104], so subtle convention mismatches (US currency formatting, imperial unit naming) cannot be ruled out; (b) calculator annotations are auto-generated, not human-validated, and have known imperfections [Q117, Q118] — DATASET-D2 shows a minor annotation inconsistency ('6+6' instead of '6*2'); (c) verifier-based scoring introduces additional label risk via false positives from flawed reasoning [Q61, Q155] and false negatives from ambiguous language [Q153, Q154]. For the platform's grading use case (LLM-as-solver, not verifier-as-grader), risk (c) is less directly relevant.

**Strengths:**
- Dedicated re-solving QC pass with disagreement-driven repair/discard [Q105, Q106]
- Quantified residual error rate of 1.7% [Q107] provides a published quality floor
- Clean integer ground-truth labels for the large majority of problems (DATASET-D13, D30)
- Anti-template-reuse pairwise similarity check [Q113] improves label diversity

**Checklist:**

- **OC-1**: Ground-truth labels for arithmetic problems are mathematically determined and reflect universal regional perspectives on numerical correctness. Risk concentrates at edge cases involving conventions (currency formatting, unit naming) where annotator demographics matter. — _Sources: Q60_
- **OC-2**: Potential disagreement with US-schooled annotators is bounded by the documented 1.7% rate [Q107]; subtle errors may be higher [Q109]. No regional-population-specific re-annotation evidence available. — _Sources: Q107, Q109_
- **OC-3**: INSUFFICIENT DOCUMENTATION — annotator demographics (age, geography, native language, educational background) are not reported beyond identifying Upwork and Surge AI as platforms [Q103, Q104]. Would need a Datasheets/Data Statements entry on contractor demographics. — _Sources: Q103, Q104_
- **OC-4**: Re-annotation by US K-8 educators on a sample of problems would be a reasonable remediation, especially for any problems involving fractions, mixed numbers, or unit-stripped answers where convention matters. — _Sources: Q109_
- **OC-5**: Aggregation: labels were validated via two-stage re-solving with disagreement repair/discard [Q105, Q106, Q107]. This conservative aggregation likely under-erases minority perspectives for objective math but could not surface culturally-specific convention disputes. — _Sources: Q105, Q106, Q107_
- **OC-6**: Documented label issues: 1.7% breaking-error rate, plus potentially larger subtle-error rate [Q108, Q109]; calculator-annotation auto-generation imperfections [Q117, Q118] confirmed in DATASET-D2. — _Sources: Q108, Q109, Q117, Q118, DATASET-D2_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q105] 'After collecting the full dataset, we asked workers to re-solve all problems, with no workers re-solving problems they originally wrote.' (p.15)
- [Q107] 'We then performed another round of agreement checks on a smaller subset of problems, finding that 1.7% of problems still produce disagreements among contractors.' (p.15)
- [Q109] 'It is possible that a larger percentage of problems contain subtle errors.' (p.15)
- [Q117] 'The calculator annotations were not provided by human contractors: they were generated by a combination of hard-coded logic and a finetuned language model.' (p.17)
- [Q118] 'The logic for auto-generating calculator annotations is imperfect.' (p.17)

*Dataset analysis:*
- DATASET-D13, D30: Clean integer labels with consistent `#### N` extraction
- DATASET-D2: Minor annotation inconsistency ('6+6' in annotation vs. 'doubled'/'6*2' in narrative) — confirms documented annotation imperfection [Q118]

</details>

**Information gaps:**
- Annotator demographics (geographic, educational, linguistic)
- Subtle-error rate (beyond the 1.7% breaking-error figure)

**Requires expert verification:**
- Sample re-annotation by US K-8 educators on edge-case problems (fractions, mixed numbers, unit-stripped answers)

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
Output form is MODERATE priority. The benchmark produces a final numerical answer extracted from a natural-language chain-of-thought solution [Q29, Q46], which structurally matches the deployment's LLM-as-solver pattern. The calculator-override mechanism [Q41, Q120] further aligns with reliable computation. However, two concerns: (1) the standard scoring pipeline does single-sample exact-match evaluation [Q29] without testing tolerance-based or equivalence-aware grading that the platform requires; (2) GSM8K saturation (>90% on frontier LLMs per [WEB-13]) reduces discriminative power for selecting among current models. The output format itself is well-matched; the gap is in what the scoring procedure evaluates rather than what the model produces.

**Strengths:**
- Final numerical answer format matches deployment grading-pipeline input [Q29]
- Calculator-override mechanism reduces arithmetic-error noise in produced answers [Q41, Q120]
- Natural language chain-of-thought output matches LLM-as-solver deployment pattern (DATASET-D33)
- Clean `#### N` answer extraction convention is unambiguous (DATASET-D13, D30)

**Checklist:**

- **OF-1**: Expected output modality (text with embedded final numerical answer) matches deployment exactly — both produce a numerical answer that the platform's grading logic then compares to student submission. — _Sources: Q29, DATASET-D33_
- **OF-2**: Not applicable — no speech-based output requirement.
- **OF-3**: Not applicable — platform users (grades 3–8 students) interact via text; LLM output is consumed by the grading pipeline, not the student.
- **OF-4**: Form mismatches are minor: (a) exact-match scoring [Q29] doesn't exercise equivalence-aware grading the platform requires (overlaps with OO finding); (b) saturation [WEB-13] limits the benchmark's ability to discriminate among frontier models; (c) socratic config (DATASET-D31) would inflate scores if used — should use main config. — _Sources: Q29, WEB-13, WEB-9, DATASET-D31_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q29] 'At test time, we judge performance by autoregressively sampling a single low temperature solution and checking whether the final answer is correct.' (p.5)
- [Q41] 'At test time, a calculator will override sampling when the model chooses to use these annotations.' (p.6)
- [Q46] 'Test performance is determined by a single low temperature (T = 0) sample for each test problem.' (p.6)
- [Q120] 'During testing, we override model sampling when a well-formatted annotation exists, specifically overwriting the token(s) directly following "=" and within <<. . . >>.' (p.17)

*Web sources:*
- [WEB-13] Most frontier LLMs achieve >90% accuracy on GSM8K — discriminative power for frontier-model selection is reduced
- [WEB-9] GSM-Plus tests robustness to answer-format perturbations not covered by GSM8K's exact-match scoring

*Dataset analysis:*
- DATASET-D33: Final answer extracted as `#### 28` from chain-of-thought — matches deployment pattern
- DATASET-D13, D30: Clean unambiguous final answer extraction
- DATASET-D31: Socratic config provides scaffolding that doesn't match deployment problem format

</details>

**Information gaps:**
- Whether the platform's grading pipeline expects only the final number or full chain-of-thought; affects whether output-form match extends to intermediate reasoning

**Requires expert verification:**
- Platform team confirmation of chain-of-thought consumption (final answer only vs. full reasoning surfaced to teachers/students)

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** Standalone unit conversion and basic geometry (perimeter/area) problem types are absent or only incidentally present, despite being confirmed essential for grades 3–8.

**Recommendation:** Supplement GSM8K with ASDiv-W [WEB-7], which provides explicit 'UnitTrans' and 'Geometry' problem categories with grade-level annotations; use grade-level metadata to filter for the platform's 3–8 range.

### Input Ontology ⚠

**Gap:** Data interpretation from tables/bar charts is structurally impossible to cover with any existing text-only K-8 arithmetic benchmark.

**Recommendation:** Author a bespoke evaluation set of 100–200 data-interpretation items matching actual teacher-assigned content (text-serialized tables or image-rendered charts depending on platform modality), validated by US K-8 educators.

### Input Ontology ⚠

**Gap:** Grade 3–4 single-step arithmetic is underrepresented; the minimum sampled complexity is 2 steps and many problems require algebraic or compound reasoning.

**Recommendation:** Use E2H-GSM8K [WEB-10] difficulty stratification to report accuracy by tier separately, and supplement with single-step problem sets from MAWPS or ASDiv-A subset filtered for grades 3–4.

### Output Ontology ⚠

**Gap:** Exact-match scoring does not stress-test answer-equivalence (fractions↔decimals, currency formatting, mixed numbers, rounding tolerance) that the platform's grading logic must handle.

**Recommendation:** Add the GSM-Plus integer-decimal-fraction conversion perturbation subset [WEB-9] to the evaluation suite; additionally implement a custom equivalence-class scoring harness aligned to the platform's tolerance thresholds.

### Output Content

**Gap:** Annotator demographics are undocumented, so subtle convention mismatches (US currency formatting, imperial unit naming) cannot be ruled out; residual subtle-error rate may exceed the documented 1.7% [Q107, Q109].

**Recommendation:** Conduct a focused re-annotation pass with US K-8 educators on a stratified sample of 200–500 problems, prioritizing problems with fractions, mixed numbers, or unit-stripped answers; quantify residual disagreement rate.

### Output Form

**Gap:** GSM8K saturation on frontier LLMs (>90% accuracy per [WEB-13]) limits discriminative power for selecting among current models the platform might deploy.

**Recommendation:** Use GSM1K [WEB-15] as a contamination-controlled complement to GSM8K, and rely on the supplementary benchmarks above for the differentiation that GSM8K alone cannot provide at the frontier.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems." |
| Q2 | 1 | input_ontology | "To increase performance, we propose training verifiers to judge the correctness of model completions." |
| Q3 | 1 | output_form | "At test time, we generate many candidate solutions and select the one ranked highest by the verifier." |
| Q4 | 1 | output_form | "We demonstrate that verification significantly improves performance on GSM8K, and we provide strong empirical evidence that verification scales more effectively with increased data than a finetuning baseline." |
| Q5 | 1 | output_content | "One significant challenge in mathematical reasoning is the high sensitivity to individual mistakes (Shen et al., 2021a)." |
| Q6 | 1 | output_content | "When generating a solution, autoregressive models have no mechanism to correct their own errors." |
| Q7 | 1 | input_content | "Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, John Schulman, OpenAI" |
| Q8 | 2 | input_content | "We are releasing GSM8K, a dataset of 8.5K high quality problems at the grade school math level." |
| Q9 | 2 | input_form | "We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts." |
| Q10 | 2 | input_form | "State-of-the-art language models struggle to achieve high performance on this dataset, primarily due to the high diversity among problems." |
| Q11 | 2 | input_ontology | "At the same time, GSM8K solutions depend only on elementary concepts, so achieving high test performance is a tractable goal." |
| Q12 | 2 | input_content | "We present a curated dataset of 8.5K grade school math questions and natural language solutions, useful for probing the informal reasoning ability of large language models." |
| Q13 | 2 | output_form | "We show that, compared to a finetuning baseline, the use of verifiers results in approximately the same performance boost as a 30x model size increase, and that verifiers scale significantly better with increased data." |
| Q14 | 2 | output_form | "We show that dropout acts as a strong regularizer, significantly improving performance for both finetuning and verification." |
| Q15 | 3 | input_content | "Early math word problem datasets (Kushman et al., 2014; Roy and Roth, 2015) are relatively small and are not well suited for testing the limits of modern language models." |
| Q16 | 3 | input_content | "Dolphin18K (Huang et al., 2016) is a larger dataset containing" |
| Q17 | 4 | input_content | "The recently developed ASDiv dataset (Miao et al., 2021), which contains 2.3K math word problems, addresses common flaws in prior datasets by ensuring problems have both high diversity and high quality." |
| Q18 | 4 | input_ontology | "We share those design principles in the creation of GSM8K." |
| Q19 | 4 | input_form | "However, we note that GSM8K is larger, provides natural language solutions, and consists of problems that on average require more steps to solve." |
| Q20 | 4 | input_ontology | "The MATH dataset (Hendrycks et al., 2021) is larger and significantly more complex than GSM8K, but the high difficulty makes it challenging to accurately measure progress given the current capabilities of state-of-the-art language models." |
| Q21 | 4 | input_ontology | "Similar to CommonsenseQA, GSM8K includes questions that require basic background knowledge, like the number of days in a week." |
| Q22 | 4 | input_ontology | "Similar to LogiQA, which requires a mix of reading comprehension and logical reasoning, GSM8K's main difficulty lies in both properly interpreting a question and reasoning through the steps to solve it." |
| Q23 | 4 | output_form | "Previous work has attempted to solve classic math word problem benchmarks with recurrent seq2seq models (Sutskever et al., 2014) and closely related variants (Wang et al., 2017; Huang et al., 2018)." |
| Q24 | 4 | output_form | "More recent work has improved performance by designing specialized encoder-decoder architectures (Amini et al., 2019; Chiang and Chen, 2018; Xie and Sun, 2019; Chen et al., 2020; Li et al., 2020), with the strongest results often relying on large pretrained encoders from the BERT family (Chen et al., 2019; Kim et al., 2020; Liang et al., 2021)." |
| Q25 | 4 | input_content | "Hendrycks et al. (2021) propose pretraining models on a new AMPS corpus, derived from Khan Academy problems and Mathematica scripts." |
| Q26 | 4 | input_content | "Similarly, Shen et al. (2021b) propose a pretrained a corpus of pre-K to college level curricula extracted from the internet, and Peng et al. (2021) propose pretraining by predicting masked subexpressions from expression trees." |
| Q27 | 5 | input_ontology | "We investigate two methods to solve problems in GSM8K: finetuning and verification." |
| Q28 | 5 | input_ontology | "Finetuning, our baseline method, uses the same language modeling objective as the generative pretraining in GPT-3 (Brown et al., 2020)." |
| Q29 | 5 | output_form | "At test time, we judge performance by autoregressively sampling a single low temperature solution and checking whether the final answer is correct." |
| Q30 | 5 | input_ontology | "In contrast, verification consists of sampling multiple high temperature solutions, assigning each solution a score, and outputting the highest ranked solution." |
| Q31 | 5 | output_ontology | "Verifiers are trained to judge the correctness of solutions, with the training signal determined solely by whether or not the solution reached the correct final answer." |
| Q32 | 5 | input_form | "First, we focus attention on the space of natural language solutions, as this is a richer and more general solution format than pure mathematical expressions." |
| Q33 | 5 | input_form | "Moreover, this choice enables our models to develop verbal analytical skills and to produce solutions that are more readily interpretable by humans." |
| Q34 | 5 | output_form | "Finally, we use separate generator and verifier networks, in order to prevent the generator from overfitting." |
| Q35 | 6 | input_ontology | "For both methods, we use models from the GPT-3 family as our initialization, primarily focusing on the 175B and 6B model sizes." |
| Q36 | 6 | input_ontology | "The 175B model is the largest and produces the most impressive results, while the 6B model is significantly more convenient for research purposes." |
| Q37 | 6 | input_form | "We discuss hyperparameter choices in Appendix B." |
| Q38 | 6 | output_content | "Our models frequently fail to accurately perform calculations." |
| Q39 | 6 | output_content | "Although larger models make fewer arithmetic mistakes than smaller models, this remains a common source of errors." |
| Q40 | 6 | input_form | "To mitigate this issue, we train all models to use a calculator by injecting calculation annotations into the training set." |
| Q41 | 6 | output_form | "At test time, a calculator will override sampling when the model chooses to use these annotations." |
| Q42 | 6 | input_form | "Details can be found in Appendix C." |
| Q43 | 6 | output_form | "We perform finetuning by updating model parameters to minimize the cross-entropy loss over all training tokens." |
| Q44 | 6 | input_ontology | "Figure 2 shows test performance after finetuning on training sets of varying sizes for 20 epochs." |
| Q45 | 6 | output_form | "We visualize the same data both as a function of training set size and as a function of model size." |
| Q46 | 6 | output_form | "Test performance is determined by a single low temperature (T = 0) sample for each test problem." |
| Q47 | 6 | input_ontology | "Unsurprisingly, we see that the 175B model significantly outperforms the smaller models." |
| Q48 | 6 | input_ontology | "Assuming a log-linear trend, we can naively extrapolate these results to estimate that a model with 10^16 parameters would be required to reach an 80% solve rate, when using the full GSM8K training set." |
| Q49 | 6 | input_ontology | "It is even harder to extrapolate along the data dimension, since performance does not appear to follow a log-linear trend." |
| Q50 | 6 | input_ontology | "Nevertheless, it appears likely that the 175B model would require at least two additional orders of magnitude of training data to reach an 80% solve rate." |
| Q51 | 6 | output_form | "In Figure 3, we show how 6B test performance varies over the course of 100" |
| Q52 | 7 | output_form | "We use test@N to denote the percentage of problems solved correctly at least once when allowing the model to make N separate guesses for each problem." |
| Q53 | 7 | output_form | "We use a low temperature (T = 0) to generate test@1 samples and we use a higher temperature (T = 0.7) to generate test@100 samples." |
| Q54 | 7 | output_form | "Both temperature values were chosen empirically to produce the best results." |
| Q55 | 7 | input_content | "For this reason, we use models trained for 2 epochs to generate samples for training verifiers." |
| Q56 | 7 | input_form | "We also note that it is important to allow the model to generate the full natural language solution before outputting a final answer." |
| Q57 | 7 | output_form | "If we instead finetune a 6B model to directly output the final answer without any intermediate steps, performance drops drastically from 20.6% to 5.2%." |
| Q58 | 7 | input_ontology | "To improve upon the finetuning baseline, we train verifiers to judge the correctness of model-generated solutions and search against these verifiers at test time." |
| Q59 | 7 | output_ontology | "Conditioned on the problem and a candidate solution, the verifier outputs the probability that the solution is correct." |
| Q60 | 7 | output_ontology | "Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer." |
| Q61 | 7 | output_content | "In practice, some solutions will reach the correct final answer using flawed reasoning, leading to false positives." |
| Q62 | 8 | output_form | "As shown in Figure 4, we train the verifier as follows: 1. Finetune a model (the "generator") for 2 epochs on the training set. 2. Sample 100 completions from the generator for each training problem and label each solution as correct or incorrect. 3. Train a verifier for a single epoch on this dataset." |
| Q63 | 8 | input_ontology | "Training for 2 epochs is enough for the generator to learn basic skills in this domain." |
| Q64 | 8 | output_content | "We choose not to train for longer, since the diversity of generated solutions begins to collapse after this point, as shown in Figure 3." |
| Q65 | 8 | output_form | "We train separate generator and verifier models to limit the generator's training and prevent overfitting, but in principle, it should be possible to combine these models." |
| Q66 | 8 | output_form | "Unless otherwise specified, we use the same model size for the generator and the verifier." |
| Q67 | 8 | output_ontology | "In addition to predicting solution correctness, we also train the verifier with the same language modeling objective as the generator." |
| Q68 | 8 | output_form | "At test time, we sample 100 completions to each test problem, rank them with the verifier, and then return the one with the highest verifier score." |
| Q69 | 8 | output_form | "We find that it is not beneficial to use verification at low dataset sizes." |
| Q70 | 8 | output_content | "We believe this is due to the pressure to overfit to the correct answer: with small datasets, overfitting to the correct answer happens faster than learning more generalizable properties of correct reasoning." |
| Q71 | 8 | output_form | "However, once we use a sufficiently large dataset, we see a strong boost from verifiers." |
| Q72 | 9 | input_ontology | "We can either train verifiers to make a single scalar prediction conditioned on the entire generated solution, or to make a scalar prediction after each token in the solution." |
| Q73 | 9 | input_ontology | "By default, we choose the latter, training verifiers to make predictions after each token." |
| Q74 | 9 | input_ontology | "This can be viewed as a token-level value function." |
| Q75 | 9 | output_ontology | "Predicting the value function at every token is a more challenging and noisier task than judging only the full completion." |
| Q76 | 9 | output_form | "However, despite the initially slower training, the token-level verifier ultimately outperforms the solution-level verifier." |
| Q77 | 9 | output_form | "Moreover, the token-level verifier is still improving late in training, whereas the solution-level verifier quickly shows signs of overfitting." |
| Q78 | 9 | output_ontology | "We hypothesize that the full value function provides a useful auxiliary signal that encourages the model to judge the reasoning throughout solutions, rather than merely memorizing the correct final answer." |
| Q79 | 9 | output_ontology | "As discussed in Section 4.2, we can optionally include a language modeling objective alongside the verification objective." |
| Q80 | 9 | output_form | "Although both are reasonable choices, including the language modeling objective is a strict improvement." |
| Q81 | 10 | output_form | "At test time, we can choose to generate arbitrarily many solutions to be judged by the verifier before selecting the highest ranked completion." |
| Q82 | 10 | output_form | "At this scale, performance improves as we increase the number of completions up to 400." |
| Q83 | 10 | output_content | "Beyond this point, performance start to decrease. This suggests that the benefits of search are eventually outweighed by the risk of finding adversarial solutions that fool the verifier." |
| Q84 | 10 | output_form | "In general, we evaluate verifier test performance using 100 completions, since this captures most of the benefits of verification with a relatively modest compute cost." |
| Q85 | 10 | output_form | "To further increase performance, we can take a majority vote among the top verifier-ranked solutions instead of selecting only the single top solution." |
| Q86 | 10 | output_content | "This suggests that the verifier may often be relying on relatively coarse heuristics to discriminate between solutions from a given generator, rather than attempting a more thorough form of verification." |
| Q87 | 11 | output_form | "This voting process considers only the final answer reached by the individual solutions: the final answer selected is the one with the most votes." |
| Q88 | 11 | output_form | "When we have only 100 samples, it is optimal to allow only the top 3-5 samples to cast a vote. When we have 3200 samples, it is approximately optimal to allow the top 30 to cast a vote." |
| Q89 | 11 | output_form | "We find that both finetuning and verification strongly benefit from the use of dropout as a regularizer." |
| Q90 | 11 | input_form | "Specifically, we apply residual dropout (Vaswani et al., 2017) along the residual paths of each layer in the network." |
| Q91 | 11 | input_form | "We use 20% dropout for all dropout experiments, chosen based on the results of a hyperparameters sweep." |
| Q92 | 11 | output_form | "We note that GPT-3 models are not pretrained with dropout. For experiments involving dropout, we therefore perform additional pretraining with dropout before subsequently finetuning the models. This mitigates the distribution shift the model experiences during finetuning." |
| Q93 | 11 | output_form | "Figure 8a shows that dropout leads to a significant improvement over baseline." |
| Q94 | 11 | output_form | "In Figure 8b, we see that dropout significantly improves solution-level verifiers, mitigating the overfitting that occurs in the unregularized baseline." |
| Q95 | 11 | output_form | "Notably, using dropout with solution-level verifiers reaches a similar level of performance as token-level verifiers." |
| Q96 | 11 | output_form | "In Figure 8c, we apply dropout to token-level verifiers. Since token-level verifiers are already less susceptible to overfitting, it is no surprise that the impact of dropout is less significant." |
| Q97 | 11 | input_form | "Note that we increase the batch size for token-level verifiers by a factor of 4, to better handle the more difficult objective and the noise from dropout." |
| Q98 | 12 | output_form | "We have seen that verification provides a significant performance boost relative to a finetuning baseline." |
| Q99 | 12 | output_form | "On the full dataset, 6B verification slightly outperforms a finetuned 175B model, thereby offering a boost approximately equivalent to a 30x model size increase." |
| Q100 | 12 | output_form | "We have also seen that token-level verifiers are less prone to overfitting than solution-level verifiers, and that all methods benefit from regularization with residual dropout." |
| Q101 | 12 | input_ontology | "We expect verification to scale well to problem distributions that require more complex mathematical reasoning, and we hope GSM8K supports the development of new methods that scale even better." |
| Q102 | 12 | input_content | "We thank Dan Hendrycks, Leo Gao, Alec Radford, and Giambattista Parascandolo for their valuable feedback on this paper; Harri Edwards, Yura Burda, Michael Wu, and Nick Ryder for many insightful conversations; Michael Petrov, Alethea Power, and Jacob Jackson for their technical assistance; the OpenAI Supercomputing team for the infrastructure that made these experiments possible; and the team at Surge AI for performing the GSM8K data collection." |
| Q103 | 15 | input_content | "We initially collected a starting set of a thousand problems and natural language solutions by hiring freelance contractors on Upwork (upwork.com)." |
| Q104 | 15 | input_content | "We then worked with Surge AI (surgehq.ai), an NLP data labeling platform, to scale up our data collection." |
| Q105 | 15 | output_content | "After collecting the full dataset, we asked workers to re-solve all problems, with no workers re-solving problems they originally wrote." |
| Q106 | 15 | output_content | "We checked whether their final answers agreed with the original solutions, and any problems that produced disagreements were either repaired or discarded." |
| Q107 | 15 | output_content | "We then performed another round of agreement checks on a smaller subset of problems, finding that 1.7% of problems still produce disagreements among contractors." |
| Q108 | 15 | output_content | "We estimate this to be the fraction of problems that contain breaking errors or ambiguities." |
| Q109 | 15 | output_content | "It is possible that a larger percentage of problems contain subtle errors." |
| Q110 | 15 | input_content | "To assist contractors with writing questions, we provided seed questions automatically generated from a few-shot prompted 175B GPT-3 model." |
| Q111 | 15 | output_content | "Contractors were allowed to use those seed questions directly, to use them as inspiration and make modifications, or to come up with their own questions entirely." |
| Q112 | 15 | output_content | "We instructed contractors to be as descriptive as possible in their solutions, and to not re-use problem settings or templates between different questions." |
| Q113 | 15 | input_content | "To ensure contractors were not re-using problem templates, we computed pairwise similarity scores between problems and used this to provide feedback to contractors." |
| Q114 | 16 | output_form | "We performed sweeps of the learning rate and batch size by an order of magnitude in both directions from the values in the table and were unable to find any significant improvements." |
| Q115 | 16 | output_form | "Other reasonable choices for both the verifier temperature (eg: 1.0 instead of 0.7) and objective (cross-entropy instead of mean squared error) also had negligible effect in our ablations." |
| Q116 | 16 | output_form | "Hyperparameters used for all experiments, unless explicitly said otherwise. Notable exceptions include Figure 8c, which uses 4x more tokens per batch and 300 completions at both training and test time. All dropout experiments in Figure 8 use 20% dropout. Figure 7a uses verifiers trained on 100 completions, but searching over more completions at test time." |
| Q117 | 17 | output_content | "The calculator annotations were not provided by human contractors: they were generated by a combination of hard-coded logic and a finetuned language model." |
| Q118 | 17 | output_content | "The logic for auto-generating calculator annotations is imperfect. It is highly unlikely to generate any incorrect annotations, but it is not uncommon for it to ignore some lines that could be annotated." |
| Q119 | 17 | input_form | "During training, there is no special distinction between the annotated tokens and the rest of the solution: they are all just tokens." |
| Q120 | 17 | output_form | "During testing, we override model sampling when a well-formatted annotation exists, specifically overwriting the token(s) directly following "=" and within <<. . . >>." |
| Q121 | 17 | output_form | "To simulate the calculator, we simply use the python eval function to evaluate the tokens in the expression (Figure 9)." |
| Q122 | 17 | output_form | "Evaluations that time out or throw an error result in the annotations being skipped and the model being sampled from as usual." |
| Q123 | 17 | output_form | "We note that the original version of our calculator, used for all results in this paper, had some minor implementation bugs." |
| Q124 | 17 | output_form | "Our reported test performance is therefore a slight underestimate, though the magnitude of this discrepancy is less than 1% in most experiments." |
| Q125 | 17 | output_form | "Fixing the calculator improves verification test performance by about 1% when using the full GSM8K training set." |
| Q126 | 18 | input_ontology | "We showcase a handful of samples comparing finetuning and verification at both 6B and 175B scale." |
| Q127 | 18 | input_content | "Samples were slightly cherry-picked for diversity." |
| Q128 | 19 | input_ontology | "The meat and context books weigh 2 pounds each, the French book weighs 3 pounds and the English book weighs 1 pound, and the total weight book sit in is for English task, if today is a nice day, what is the total weight of all the books?" |
| Q129 | 19 | input_ontology | "The meat and context books weigh 2 pounds each so they weigh 2*2 = 4=2=6=8 pounds together, the French book weighs 3 pounds and so the total weight of the English book is 6+3 = 10, so if you add up all of the books together, the total weight is 4+3+4 = 11" |
| Q130 | 19 | input_ontology | "Our generated responses weigh books weigh 2 pounds each to a total of 2*2 = or2=4 pounds, use French book weigh 4 pounds and the English book weighs 3 pounds, to a total of 4+3 = or4+3=7 pounds, if so if you add up all of the books, the total weight of the English book, to a total of 3+3 = or2=4=8 pounds" |
| Q131 | 19 | input_ontology | "The English book weight 3 pounds, So all of our books weigh 2 + 4 + 3 = 9=10 =9=10=9=10 pounds." |
| Q132 | 19 | input_ontology | "The total weight of books read at science books is 2*2=or2=4=6=8 pounds total weight of all the books is 4+3=or2=4+3=7 pounds." |
| Q133 | 19 | input_ontology | "The German Shepherd dog contains 1.5 + = or1+1=1.5=1 diggrams of dog food per day the dog also contains 2.5 +3=or2=5.5 diggrams of dog food per day, During a week, the total is 2.5 + or2+1=3=1+1.5=1 diggrams of dog food is a week." |
| Q134 | 19 | input_ontology | "Our data 1000=or1=1.5=1.5 diggrams per day for the German Shepherd, if the dog weighs 3.2 + or3+1.7=or3=1.9=1.5 diggrams of dog food per week." |
| Q135 | 19 | input_ontology | "The German Shepherd's total consumption is 1.5 + =or1=1.5=1.5 diggrams, the dog also and consumption total food per meal is 3.2 + = or3=2.5=1.5=1.5 diggrams." |
| Q136 | 19 | input_ontology | "The 2 German Shepherd dogs consumes 1.5 + =or1+1=1.5=1.5 diggrams of food per day, the 2 bulldogs consumes 2.3 + =or2=2.5=2.5=1.5 diggrams of food per day." |
| Q137 | 20 | output_ontology | "As noted in section 4.2, we train verifiers with a joint objective where the model learns to label a model completion as correct or incorrect, in addition to the original language modeling objective." |
| Q138 | 20 | output_form | "Architecturally, this means our verifiers are language models, with a small scalar head that outputs predictions on a per-token basis." |
| Q139 | 20 | output_form | "We implement this scalar head as a single bias parameter and single gain parameter that operate on the logits outputted by the language model's final unembedding layer." |
| Q140 | 20 | output_form | "We can choose to initialize the verifier from the same pretrained language model the generator was finetuned from, or from the generator itself." |
| Q141 | 20 | output_form | "In our ablations the latter performed slightly better; we suspect this is because better understanding the language distribution that the generator learned should only aid the verifier in scoring samples from that distribution." |
| Q142 | 20 | output_form | "Unless otherwise explicitly stated, we initialize our verifiers from their corresponding generators in all experiments." |
| Q143 | 20 | input_content | "When training verifiers with the joint objective, we use an equal mix of language data and verifier data." |
| Q144 | 20 | input_content | "Because we sample 100 completions for each original training example to generate the verifier data, using an equal mix means we effectively upsample the original language data by a factor of 100." |
| Q145 | 20 | output_form | "To form the joint objective, we simply add the verifier loss and language modeling loss unweighted, and define an epoch of this joint objective as having seen each verifier example once." |
| Q146 | 20 | input_form | "With both objectives, we mask out tokens in the question and only train on tokens in the solutions, as visualized in Figure 12." |
| Q147 | 21 | output_form | "One benefit of the token-level verifiers is that these models become immediately interpretable: we can visualize the predicted value for each token and better understand how the verifier makes decisions on judging samples." |
| Q148 | 21 | output_form | "Above we present a visualization of the predicted values for five different cherry-picked questions and model completions, verified by a 175B token-level verifier that was trained on the full training set." |
| Q149 | 21 | output_form | "In the visualization, the background color of the text corresponds to the verifier score for that token, where red is low value (predicted incorrect) and green" |
| Q150 | 22 | output_form | "The second column of the table summarizes the verifier's prediction, and the third column indicates whether the generated model completion was actually correct or incorrect." |
| Q151 | 22 | output_form | "Any disagreement between the second and third columns indicates that the verifier made an error." |
| Q152 | 22 | output_content | "Note that the model is initially unsure about whether the solution is correct and gradually gains certainty as the solution progresses: this is likely a property of the verifier training procedure, where it trains on a large fraction of incorrect model-generated samples." |
| Q153 | 22 | output_content | "The second row contains a problem where the solution is correct, but the verifier has rated it as incorrect. This is potentially due to the ambiguity between the "4 times" and the "4 potatoes" in the problem description." |
| Q154 | 22 | output_content | "The third row consists of another false negative example. However, unlike the previous example, here the model completion contains some faulty reasoning. As such, even though the final answer in the model completion was correct, the natural language explanation was incorrect, and so the verifier correctly assigned a low score." |
| Q155 | 22 | output_content | "The final row contains a false positive, where the model makes a mistake on the second step, where it subtracts 400 from the price of a diamond jewel instead of a gold one. Verifiers occasionally make mistakes with performing this variable binding of quantities to their relationships." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.thecorestandards.org/standards-in-your-state/ |
| WEB-2 | https://worldpopulationreview.com/state-rankings/common-core-states |
| WEB-3 | https://goblinsapp.com/standards/math |
| WEB-4 | https://www.emergentmind.com/topics/gsm8k-dataset |
| WEB-5 | https://klu.ai/glossary/GSM8K-eval |
| WEB-6 | https://mbrenndoerfer.com/writing/gsm8k-evaluating-mathematical-reasoning-language-models |
| WEB-7 | https://arxiv.org/abs/2106.15772 |
| WEB-8 | https://aclanthology.org/2021.acl-long.254/ |
| WEB-9 | https://arxiv.org/abs/2402.19255 |
| WEB-10 | https://arxiv.org/pdf/2510.18147 |
| WEB-11 | https://github.com/chaochun/nlu-asdiv-dataset |
| WEB-12 | https://github.com/arkilpatel/SVAMP |
| WEB-13 | https://www.emergentmind.com/topics/gsm8k |
| WEB-14 | https://github.com/qtli/GSM-Plus |
| WEB-15 | https://arxiv.org/pdf/2405.00332 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** openai/gsm8k (configs: `main`, `socratic`)
**Analysis date:** 2025-01-31
**Examples reviewed:** 47 from `main` train split; 33 from `socratic` train split (80 total; socratic examples are structurally identical to main with sub-question scaffolding added)
**Columns shown:** question, answer
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | main | 3 | 99 | "Her parents bought a unicorn piñata for $13 and filled it with all of her favorite treats. They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." | US consumer goods, dollar amounts — typical birthday party scenario | IC |
| D2 | main | 12 | 78 | "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9." | Imperial weight units (pounds), US-style pet scenario | IC |
| D3 | main | 6 | 54 | "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" | Imperial length units; volume calculation (length × width × height) | IC, IO |
| D4 | main | 13 | 1825 | "If Sally makes $6 per day and Bob makes $4 per day, how much money will they both have saved for their trip after a year?" | Dollar amounts, annual savings rate problem | IC |
| D5 | main | 18 | 72 | "He scores 4 touchdowns per game and each touchdown is worth 6 points. There are 15 games in the season." | American football scoring scenario — culturally specific to US | IC |
| D6 | main | 22 | 80 | "Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change. How much did Austin start with?" | Dollar amounts with cents (decimal currency), tax scenario | IC, OO |
| D7 | main | 26 | 2,250 | "Roberto can skip 4,200 times an hour. Valerie can skip 80 times a minute. If they jump rope for fifteen minutes straight, how many skips will they total?" | Implicit unit conversion (hours-to-minutes) embedded within a rate problem | IO |
| D8 | main | 47 | 72 | "Larry spends half an hour twice a day walking and playing with his dog. He also spends a fifth of an hour every day feeding his dog. How many minutes does Larry spend on his dog each day?" | Explicit hours-to-minutes conversion embedded in problem | IO |
| D9 | main | 35 | 333200 | "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft and the barn out back is 1,000 sq ft. How much is this property?" | Area used as input quantity, but no geometry formula required — pure multiplication | IO |
| D10 | main | 6 | 54 | "First calculate the volume of the aquarium by multiplying its length, width and height: 4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft" | Volume of rectangular prism computed — closest geometry-adjacent example in sample | IO |
| D11 | main | 9 | 28 | "Four people lost a total of 103 kilograms of weight." | Metric units (kilograms) appear in at least one problem | IC |
| D12 | main | 24 | 180 | "In a northwestern town, it rained 4 inches per day during the first 15 days of November." | Imperial measurement (inches of rain); multi-step rate × time | IC |
| D13 | main | 1 | 32 | "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them. On Wednesday Buddy buys 12 baseball cards. On Thursday he buys a third of what he had on Tuesday." | 4-step sequential problem; straightforward multi-step arithmetic | IO |
| D14 | main | 7 | 90 | "There are enough provisions in a castle to feed 300 people for 90 days. After 30 days, 100 people leave the castle. How many more days are left until all the food runs out?" | Multi-step proportional reasoning with division | IO |
| D15 | main | 19 | 54 | "Bobby has 16 toy cars, and the number of cars he has increases by 50% every year. How many toy cars will Bobby have in three years?" | Compound percentage growth over multiple years — grades 6–8 level | IO |
| D16 | main | 30 | 7200 | "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month. This year her rent goes up by 30%, food costs increase by 50%..." | Multi-step percent change problem — upper grade band | IO |
| D17 | main | 23 | 220 | "Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys." | Algebraic system-of-equations approach — above typical grade 3–4 | IO |
| D18 | main | 43 | 720 | "Ariella's account earns her simple interest at the rate of 10% per annum." | Simple interest calculation — finance context, grades 7–8 | IO |
| D19 | main | 45 | 120 | "Ten friends decide to get an end-of-year gift for their teacher. They plan to split the cost of the gift equally. But four of the group drop out." | Algebraic equation set-up (10N = 6(N+8)) | IO |
| D20 | main | 38 | 90 | "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440, and Amalie spends 3/4 of what she has on toys, how many will she remain with?" | Ratio + fraction multi-step — upper grade band difficulty | IO |
| D21 | main | 26 | 2,250 | "They will skip 2,250 times because 150 x 15 = <<150*15=2250>>2,250" | Final answer formatted as "2,250" (comma-formatted integer) — not a plain integer string | OO |
| D22 | main | 35 | 333200 | "98*3400 = $<<98*3400=333200.00>>333,200.00" | Answer annotation contains "333200.00" (trailing decimal zeros); extracted answer "333200" — format normalization in scoring | OO |
| D23 | main | 4 | 21 | "So the cost of one bottle of milk was 75/100 * 12 = $<<75/100*12=9>>9." | Percent expressed as fraction (75/100) in reasoning — answer is integer | OO |
| D24 | main | 11 | 35 | "Arlette is 3/4 * 28 years = <<3/4*28=21>>21 years old." | Fraction used in intermediate step; final answer is integer | OO |
| D25 | main | 2 | 9 | "After giving away 4/5 of the cupcakes, Anna has 60 / 5 = <<60/5=12>>12 cupcakes" | Fraction used in problem setup; intermediate and final answers are integers | OO |
| D26 | main | 5 | 36 | "Caleb spent $40 − $4 = $36 more on ice cream than on frozen yogurt." | Answer is plain integer $36; no dollar sign in extracted answer | OO |
| D27 | main | 22 | 80 | "$68.47 total spent in-store + $11.53 in change = $<<68.47+11.53=80>>80 to start." | Decimal dollar amounts in intermediate steps; final answer is integer | OO |
| D28 | main | 41 | 347 | "Monika spent 20*1.25 = <<20*1.25=25>>25 dollars at the farmers market." | Decimal multiplication ($1.25/bag × 20) yields integer answer | OO |
| D29 | main | 15 | 9 | "Kat decides she wants to start a boxing career. She gets a gym membership and spends 1 hour in the gym 3 times a week... She also trained at the boxing gym 4 times a week for 1.5 hours." | Simple 2-step problem — among the lower-complexity examples in sample | IO |
| D30 | main | 8 | 80 | "Five coaster vans are used to transport students for their field trip. Each van carries 28 students, 60 of which are boys. How many are girls?" | 2-step problem; simple subtraction after multiplication | IO |
| D31 | socratic | 6 | 54 | "How many cubic feet are in the aquarium? ** First calculate the volume of the aquarium by multiplying its length, width and height" | Socratic decomposition scaffolds sub-questions for each step | IF, OF |
| D32 | main | 36 | 1080 | "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day. If there are 6 jaguars in a forest, how many beetles are eaten each day?" | Multi-step chain multiplication (rate problem); no cultural specificity | IO |
| D33 | main | 9 | 28 | "Second person = 27 - 7 = <<27-7=20>>20 kg\n103 - 27 - 20 = <<103-27-20=56>>56 kg\n56/2 = <<56/2=28>>28 kg" | Answer annotations show calculator-injection format `<<expr=result>>` | IF |
| D34 | main | 44 | 11000 | "He sold his car for 20000*.8=$<<20000*.8=16000>>16,000\nHe bought the new car for 30,000*.9=$<<30000*.9=27000>>27,000" | Comma-formatted intermediate values; final answer 11000 is plain integer | OO |

---

### Deployment-Relevant Strengths

#### Strength 1: Strong US cultural and monetary contextualization
- **Dimension(s):** IC
- **Observation:** The overwhelming majority of sampled problems use US dollars, American consumer goods, and familiar US school/social scenarios. Dollar amounts appear in at least 20 of 47 main examples, and settings include birthday parties, sports, babysitting, candy stores, and mall fountains — all squarely matching the platform's profile.
- **Deployment relevance:** The user confirmed that platform problems are "almost entirely US-contextualized — dollars, imperial units, American names, typical school scenarios." GSM8K's content closely mirrors this, minimizing construct-irrelevant cultural variance.
- **Datapoint citations:**
  - [D1] Example 3 (main, train, label=99): "Her parents bought a unicorn piñata for $13 and filled it with all of her favorite treats. They bought 4 bags of Reese's for $9 per bag..." — US birthday party scenario with named US brand candies and dollar prices
  - [D4] Example 13 (main, train, label=1825): "If Sally makes $6 per day and Bob makes $4 per day, how much money will they both have saved for their trip after a year?" — dollar-based savings rate problem with American names
  - [D5] Example 18 (main, train, label=72): "He scores 4 touchdowns per game and each touchdown is worth 6 points. There are 15 games in the season." — American football scoring, a culturally US-specific scenario

#### Strength 2: Imperial units dominate, with occasional metric, matching the platform's distribution
- **Dimension(s):** IC
- **Observation:** Imperial units (pounds, feet, inches, cubic feet) appear throughout the sample. One metric instance (kilograms) appears, matching the user's description that "a small minority of teachers include metric units in science-adjacent problems."
- **Deployment relevance:** The platform's stated distribution — predominantly imperial, small metric minority — is reflected in the data without over-representing metric units that would misalign with actual classroom problem profiles.
- **Datapoint citations:**
  - [D2] Example 12 (main, train, label=78): "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9." — pounds used naturally in consumer/pet context
  - [D3] Example 6 (main, train, label=54): "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" — feet and cubic feet; imperial volumetric units
  - [D11] Example 9 (main, train, label=28): "Four people lost a total of 103 kilograms of weight." — one of the rare metric instances, plausibly representing science-adjacent problems

#### Strength 3: Multi-step arithmetic reasoning across the upper grade band (grades 5–8)
- **Dimension(s):** IO
- **Observation:** The sample contains strong coverage of multi-step ratio, percent, rate, proportional reasoning, and algebraic problems that align with grades 6–8 curriculum. Multiple examples require 4–6 distinct calculation steps with correctly tracked intermediate quantities.
- **Deployment relevance:** The platform serves grades 3–8, and the upper half of this range (grades 6–8) is where the most analytically demanding problems appear. GSM8K provides substantive coverage of this upper tier.
- **Datapoint citations:**
  - [D16] Example 30 (main, train, label=7200): "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month. This year her rent goes up by 30%, food costs increase by 50%..." — multi-step percentage change with annual scaling
  - [D18] Example 43 (main, train, label=720): "Ariella's account earns her simple interest at the rate of 10% per annum." — simple interest over two years, finance-adjacent
  - [D20] Example 38 (main, train, label=90): "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440, and Amalie spends 3/4 of what she has on toys..." — ratio + fraction multi-step problem

#### Strength 4: Chain-of-thought solution format with calculator annotations matches LLM deployment pattern
- **Dimension(s):** IF, OF
- **Observation:** Every answer in the sample uses natural language step-by-step reasoning with embedded calculator annotation tokens (`<<expr=result>>`), terminating in a `#### N` final answer. This exactly matches the chain-of-thought output format the deployment LLM would produce, and the final answer extraction convention is unambiguous.
- **Deployment relevance:** The LLM's role in the platform is to independently solve problems and produce a numerical answer. GSM8K's solution format — prose reasoning → annotated computation → final number — is structurally congruent with this deployment pattern, supporting reliable evaluation of the generation quality.
- **Datapoint citations:**
  - [D33] Example 9 (main, train, label=28): "Second person = 27 - 7 = <<27-7=20>>20 kg\n103 - 27 - 20 = <<103-27-20=56>>56 kg\n56/2 = <<56/2=28>>28 kg" — calculator annotation format visible; final `#### 28`
  - [D31] Socratic Example 6 (socratic, train, label=54): "How many cubic feet are in the aquarium? ** First calculate the volume of the aquarium by multiplying its length, width and height" — socratic config adds sub-question scaffolding, offering an additional evaluation format for step-by-step reasoning

#### Strength 5: Reliable integer-answer problems with clean ground-truth labels for core arithmetic
- **Dimension(s):** OC
- **Observation:** The large majority of sampled problems have clean integer final answers, making ground-truth extraction unambiguous. The answer annotation format (`#### N`) is consistent across all examples. The re-solving QC process documented in the paper is evidenced in the data quality — no ambiguous or missing final answers appear in the sample.
- **Deployment relevance:** For the platform's grading pipeline, clean integer answers reduce the normalization burden and make benchmark scoring most directly comparable to the operational grading logic for straightforward problem types.
- **Datapoint citations:**
  - [D13] Example 1 (main, train, label=32): "On Thursday Buddy has a total of 27+5 = <<27+5=32>>32 baseball cards.\n#### 32" — clean integer, unambiguous label
  - [D30] Example 8 (main, train, label=80): "If 60 are boys, then 140 - 60 = <<140-60=80>>80 of these students are girls.\n#### 80" — simple 2-step integer answer

#### Strength 6: Linguistic diversity within US-contextualized problems
- **Dimension(s):** IC
- **Observation:** Problem contexts span a wide range of US-familiar domains: sports (baseball cards, football, boxing), food (cupcakes, peanuts, ice cream, pie), pets (dog weight, dog food), school (field trips, gift-splitting), finance (rent, car insurance, savings), and commerce (ice cream shop, video game collection). This variety reduces the risk of the benchmark overfitting to a single domain register.
- **Deployment relevance:** Teachers on the platform assign problems across diverse real-world contexts. The contextual variety in GSM8K helps ensure that LLM reliability is tested across different problem framings rather than a single narrow topic.
- **Datapoint citations:**
  - [D32] Example 36 (main, train, label=1080): "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day." — ecological chain-rate problem; unusual context
  - [D5] Example 18 (main, train, label=72): "James joins a football team and becomes the star. He scores 4 touchdowns per game..." — sports scoring context
  - [D1] Example 3 (main, train, label=99): "It's Ava's birthday party. Her parents bought a unicorn piñata for $13..." — consumer/celebration context

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Measurement/unit conversion as standalone problem type is absent — only incidentally embedded
- **Dimension(s):** IO
- **Observation:** No sampled problem requires standalone unit conversion as its primary task (e.g., "convert 3.5 feet to inches," "how many minutes are in 4 hours 15 minutes," "convert 2.5 pounds to ounces"). Unit conversion appears only as an incidental embedded step within rate or time problems. Example 26 (D7) requires dividing 4,200 per hour by 60 to get per-minute rate, and Example 47 (D8) converts "half an hour" to 30 minutes as an unstated assumption — but neither problem presents unit conversion as its stated goal or tests the conversion relationship explicitly.
- **Deployment relevance:** The user explicitly confirmed measurement and unit conversion problems (hours-to-minutes, feet-to-inches, pounds-to-ounces) are "frequently assigned and essential" for grades 3–8. The complete absence of conversion-primary problems means GSM8K cannot assess LLM reliability on this problem type as teachers assign it.
- **Datapoint citations:**
  - [D7] Example 26 (main, train, label=2250): "Roberto can skip 4,200 times an hour. Valerie can skip 80 times a minute. If they jump rope for fifteen minutes straight, how many skips will they total?" — conversion from hours to minutes is embedded incidentally (dividing by 60), not the problem's stated goal
  - [D8] Example 47 (main, train, label=72): "Larry spends half an hour twice a day walking and playing with his dog. He also spends a fifth of an hour every day feeding his dog. How many minutes does Larry spend on his dog each day?" — minutes-to-hours conversion required but framed as a time arithmetic problem, not a unit conversion exercise

#### CRITICAL Concern 2: No geometry word problems (perimeter, area) appear in any sampled example
- **Dimension(s):** IO
- **Observation:** Zero sampled problems require computing the perimeter or area of a geometric shape as the primary task. Example 6 (D3, D10) computes a rectangular prism volume as an intermediate step within a water-filling scenario, and Example 35 (D9) multiplies area (sq ft) by price — but the area is given as an input value, not computed from dimensions using a formula. No problem asks students to find the perimeter or area of a rectangle, triangle, or polygon.
- **Deployment relevance:** The user confirmed basic geometry word problems (perimeter, area) are "frequently assigned" and "considered essential coverage for any trustworthy reliability evaluation" across grades 4–8. This is a total gap in the sampled data, consistent with the benchmark's documented arithmetic-only scope.
- **Datapoint citations:**
  - [D9] Example 35 (main, train, label=333200): "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft and the barn out back is 1,000 sq ft. How much is this property?" — area values are given as inputs; no geometric formula applied
  - [D10] Example 6 (main, train, label=54): "First calculate the volume of the aquarium by multiplying its length, width and height: 4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft" — closest geometry-adjacent computation in sample; volume of rectangular prism, not perimeter or area

#### CRITICAL Concern 3: Data interpretation from tables or bar charts is structurally impossible — total modality gap
- **Dimension(s):** IO, IF
- **Observation:** All 80 sampled problems are pure text narrative. No problem requires reading values from a table, bar chart, number line, or any structured data representation. This is an expected property of GSM8K's design (text-only) but constitutes a total gap relative to the deployment.
- **Deployment relevance:** The user confirmed teachers "frequently assign" simple data interpretation problems requiring students to read values from tables or bar charts before computing. No existing text-only benchmark can close this gap; the web search confirmed no K-8-calibrated arithmetic benchmark with text-serialized table inputs exists.
- **Datapoint citations:** No positive evidence possible from the sample — all 80 examples confirm absence of any tabular or chart-based data. The structural evidence is the text-narrative format itself: every problem encodes all numerical values as prose.

---

#### MAJOR

#### MAJOR Concern 4: Answer equivalence edge cases (decimal/fraction, currency formatting) are not stress-tested by the scoring pipeline
- **Dimension(s):** OO, OC
- **Observation:** The data contains problems where intermediate steps use decimal dollar amounts (D6: $8.75, $7.22, $11.53; D27: $68.47, $11.53), fractional multipliers (D24: 3/4 × 28; D25: 4/5 of 60; D23: 75/100 × 12), and comma-formatted answer strings (D21: "2,250"; D22: "333,200.00"). In all cases, the final extracted answer is a plain integer or simple decimal. However, the benchmark's scoring pipeline uses exact-match extraction and does not test whether a model that outputs "1/2" instead of "0.5," or "$2.50" instead of "2.50," would be correctly credited. The GSM8K scoring infrastructure (per web search findings) strips currency symbols but does not implement fraction-decimal equivalence.
- **Deployment relevance:** The user identified answer equivalence across representations as "a genuine operational requirement" — students may submit "0.5" when the LLM produces "1/2." GSM8K's problems generate the conditions for these equivalences (fractions in intermediate steps, decimal currency in inputs) but the scoring pipeline does not evaluate whether the LLM handles them correctly. The benchmark will not surface LLM failures of the type documented in GSM-Plus's integer-decimal-fraction perturbation experiments.
- **Datapoint citations:**
  - [D21] Example 26 (main, train, label=2250): "They will skip 2,250 times because 150 x 15 = <<150*15=2250>>2,250" — final answer formatted "2,250" with comma; scoring must handle comma normalization
  - [D22] Example 35 (main, train, label=333200): "98*3400 = $<<98*3400=333200.00>>333,200.00" — annotation contains "333200.00" with trailing decimal zero; label is 333200
  - [D6] Example 22 (main, train, label=80): "Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change." — decimal dollar amounts throughout; final answer happens to be integer 80, masking the decimal handling requirement

#### MAJOR Concern 5: Lower grade-band difficulty (grades 3–4, single-step problems) is underrepresented
- **Dimension(s):** IO
- **Observation:** Among the 47 main examples, the simplest problems require at least 2 calculation steps (e.g., D29: 2 multiplications + 1 subtraction; D30: 1 multiplication + 1 subtraction). The majority require 3–6 steps. No single-step multiplication ("If apples cost $0.30 each, how much do 7 apples cost?") or single-step division problem appears. Problems involving algebraic equation setup (D17, D19), compound growth (D15), simple interest (D18), and multi-variable ratio systems (D20) suggest the lower end of the sample still calibrates well above grades 3–4.
- **Deployment relevance:** The platform spans grades 3–8, and a substantial fraction of its users are grades 3–4 students assigned single-step or two-step multiplication/division problems. Over-estimating LLM reliability on these simpler problems (because GSM8K provides no grade 3–4 calibrated examples) is a real risk for the platform's grading accuracy at the lower end.
- **Datapoint citations:**
  - [D17] Example 23 (main, train, label=220): "Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys." — requires algebraic system of equations; well above grades 3–4
  - [D19] Example 45 (main, train, label=120): "Let N be the original price each friend was going to pay. 10N=6(N+8)" — formal algebraic equation; not grade 3–4 content
  - [D29] Example 15 (main, train, label=9): "She strength trains 3*1=<<3*1=3>>3 hours a week. She does boxing training 4*1.5=<<4*1.5=6>>6 hours a week." — among the simplest in sample; still requires 2 multiplications + addition

#### MAJOR Concern 6: GSM8K saturation reduces discriminative power for current frontier LLMs
- **Dimension(s):** OO, OF
- **Observation:** Per web search findings, most frontier LLMs achieve >90% accuracy on GSM8K as of early 2026. The sampled problems, while linguistically varied, are structured arithmetic scenarios that strong LLMs now solve near-perfectly. The benchmark can still detect failures in weaker or smaller models, but cannot meaningfully differentiate among the frontier models the platform would likely deploy.
- **Deployment relevance:** If the platform is evaluating frontier LLMs (GPT-4 class or similar), a near-ceiling GSM8K score provides very limited signal about which model is more reliable for its specific use case. The benchmark is necessary but not sufficient as a reliability signal.
- **Datapoint citations:**
  - [D13] Example 1 (main, train, label=32): "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them..." — straightforward 4-step sequential problem that near-any capable LLM solves correctly, providing no differentiation signal
  - [D30] Example 8 (main, train, label=80): "Five coaster vans are used to transport students for their field trip. Each van carries 28 students, 60 of which are boys. How many are girls?" — trivially simple 2-step problem for frontier models

---

#### MINOR

#### MINOR Concern 7: A small number of problems use metric units, creating minor distribution mismatch
- **Dimension(s):** IC
- **Observation:** Example 9 uses kilograms (D11). The user confirmed metric units appear in "a small minority" of teacher-assigned problems, primarily in science contexts. The benchmark's sporadic metric usage is not a systematic mismatch but may slightly inflate the apparent US-contextualization of the benchmark if metric problems cluster disproportionately in evaluation splits.
- **Deployment relevance:** Minor — the mismatch is acknowledged and small. Platform teachers do assign some metric problems, so metric instances are not entirely irrelevant; they just represent a minority of actual assignments.
- **Datapoint citations:**
  - [D11] Example 9 (main, train, label=28): "Four people lost a total of 103 kilograms of weight." — metric weight unit (kilograms) rather than pounds; only metric example identified in 47-example sample

#### MINOR Concern 8: Socratic config adds sub-question scaffolding not present in deployment problems
- **Dimension(s):** IF
- **Observation:** The `socratic` configuration provides the same problems as `main` but with intermediate sub-questions decomposing the solution ("How many cards does Buddy have on Tuesday? **"). This format does not correspond to how teacher-assigned problems are written, and if used for evaluation, would artificially guide LLM reasoning in a way that inflates performance estimates.
- **Deployment relevance:** If the platform uses the socratic config for evaluation (rather than main), this would overestimate LLM performance by providing guided scaffolding. However, this is a configuration choice issue — using `main` avoids the concern entirely.
- **Datapoint citations:**
  - [D31] Socratic Example 6 (socratic, train, label=54): "How many cubic feet are in the aquarium? ** First calculate the volume of the aquarium by multiplying its length, width and height: 4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft" — sub-question header makes the intermediate step explicit, reducing the reasoning challenge compared to the main config

#### MINOR Concern 9: Some intermediate calculation annotations contain minor format inconsistencies
- **Dimension(s):** OC
- **Observation:** In Example 12's answer (D2), the calculator annotation reads `6*2=<<6+6=12>>` — the annotation expression uses `6+6` while the narrative says "doubled" (i.e., `6*2`). This is a known annotation imperfection documented in the paper (Q118: "The logic for auto-generating calculator annotations is imperfect... not uncommon for it to ignore some lines"). The final answer is correct (12), so label quality is not affected, but the annotation contains a minor logical inconsistency that could confuse models trained on these annotations.
- **Deployment relevance:** Minor for the evaluation use case (correctness label is unaffected), but relevant if the platform were to use GSM8K training data to fine-tune the LLM it deploys.
- **Datapoint citations:**
  - [D2] Example 12 (main, train, label=78): "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9 to reach a weight of 6*2=<<6+6=12>>12 pounds." — narrative says "6*2" but annotation expression is "6+6"; both yield 12, so label is correct, but annotation expression is inconsistent

---

### Content Coverage Summary

The 80 sampled examples (47 main + 33 socratic, where socratic mirrors main problems) present a consistent profile: all problems are text-only English prose in US-contextualized settings, using predominantly dollar amounts and imperial units, with names like Bobby, Kantana, Ariella, and James appearing in typical American school, home, and commercial scenarios. Problem difficulty clusters firmly in the multi-step range — the simplest examples require 2 arithmetic operations; the most complex involve compound percentage change, simple interest, algebraic equation systems, and multi-level ratio chains. All answers in the sample are integers or simple decimals, with final answers extracted unambiguously via the `#### N` convention.

The data exhibits strong coverage of: rate and unit-rate problems, percent and percentage change, ratio and proportion, multi-step spending/budgeting scenarios, and sequential counting problems. It does not contain any examples of: standalone unit conversion (as the problem's primary task), geometric formula application (perimeter, area), or data interpretation from structured representations (tables, charts). The closest geometry-adjacent problem (Example 6) computes rectangular prism volume as an intermediate step within a water-filling scenario, and the closest unit-conversion-adjacent problems (Examples 26 and 47) embed conversion as an unstated intermediate step rather than as the stated goal.

The solution format is consistent: natural language reasoning with calculator annotation tokens (`<<expr=result>>`), culminating in `#### N`. The socratic config adds sub-question headers to each step but uses the same underlying problems. Both configs are text-only with no multimedia.

---

### Limitations

1. **Sample size and split coverage**: Only 47 examples from the `main` train split were inspected (out of 7,473 train + 1,319 test). The test split — which is the operationally relevant set for benchmark scoring — was not directly sampled. Problem type distribution observations are indicative, not statistically representative of the full benchmark.

2. **Problem type frequency unknown**: Without a systematic taxonomy of all 8,500 problems, it is impossible to determine whether geometry, unit conversion, or data interpretation problems appear at very low frequency in the full dataset. The sample provides no positive evidence for these types, but cannot rule out rare instances.

3. **Answer format edge cases require test-split inspection**: The scoring behavior for non-integer answers (fractions, mixed numbers, large comma-formatted integers) depends on the test-split distribution and the evaluation pipeline implementation, neither of which was directly inspected. The concern about answer equivalence is grounded in intermediate-step formatting observed in the training sample and documented external findings, not in direct observation of evaluation failures.

4. **Annotator demographics unverifiable from data**: The cultural specificity of problem settings can be observed (US-contextualized), but whether any problems reflect non-US annotator assumptions (e.g., metric units, non-US school scenarios) cannot be confirmed from content alone without knowing annotator demographics, which the paper does not report.

5. **GSM8K saturation claim unverifiable from data**: The claim that frontier LLMs achieve >90% accuracy is based on web search findings; no model performance data was directly inspected. The content of the sampled problems is consistent with this claim (many are straightforward for strong models) but cannot confirm the specific accuracy figures.

