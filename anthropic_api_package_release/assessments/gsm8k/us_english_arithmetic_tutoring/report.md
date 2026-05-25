## Deployment Context

We are a US edtech company building a tutoring module for American students. When a student gets an arithmetic word problem wrong, our system should identify where in their worked solution the error occurred and explain the mistake. The system receives the original word problem plus the student's step-by-step work (which may contain errors), and produces a diagnostic explanation. We want to evaluate the LLM's ability to analyze and diagnose errors in arithmetic reasoning.

# Validity Analysis: gsm8k
**Target context:** US Elementary/Middle School Arithmetic Tutoring — Grade 3–6 Diagnostic Module
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 3 | Moderate gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ✓ | 2 | Significant gaps | high |
| **Average** | **1.8** | | |

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

GSM8K is a problem-solving benchmark — it tests whether models can produce correct grade-school math word problem solutions, scored by binary final-answer correctness. The deployment is a diagnostic system that must analyze student-authored solutions, locate the earliest error and downstream errors, classify error types according to a five-plus-category US-curriculum taxonomy, and generate teacher-register explanations differentiated by grade level. The directional mismatch is severe on every HIGH-priority dimension: input ontology lacks an error taxonomy and grade-level metadata; input content is professionally authored clean prose with none of the student-register notation the deployment must parse; output ontology is binary final-answer correctness with no error-location, error-type, or pedagogical-acceptability label space; output content is annotated by freelance contractors with no domain-educator involvement. The MR-GSM8K empirical result that top GSM8K solvers (>80% accuracy) collapse to MR-Scores <0.02 on error localization quantifies the gap as not merely structural but operationally severe. Partial alignments — shared text/English modality, USD currency, US-customary unit incidence, and the multi-step chain-of-thought solution format — are real but secondary. GSM8K is at best a final-answer sanity check; it cannot serve as the primary evaluation instrument for a diagnostic deployment.

## Practical Guidance

### What This Benchmark Measures

GSM8K measures a model's ability to *produce* a correct final numerical answer to a clean, professionally authored grade-school-level word problem when given the problem alone. It exercises multi-step chain-of-thought arithmetic reasoning (a strength for input_ontology) and verifies the final number against contractor-agreed ground truth. For the deployment, this provides only a baseline competency check: 'can this model do the underlying arithmetic if it had to?'

### Construct Depth

Shallow with respect to the deployment's construct. The construct of interest is *diagnostic meta-reasoning over student work*, which has at least four sub-constructs: (1) parsing non-standard student notation, (2) localizing the earliest error, (3) classifying error type against a curriculum-aligned taxonomy, and (4) generating teacher-register explanation. GSM8K touches sub-construct (0) — does the model know the arithmetic at all — and none of (1)–(4). The MR-GSM8K finding of near-zero error-localization performance from GSM8K-strong models [WEB-7, WEB-25] is direct empirical evidence that depth on the deployment construct is essentially absent.

### What Else You Need

Substantial supplementation required across all six dimensions. For IO/OO: ProcessBench [WEB-14] for earliest-error-step identification, MR-GSM8K [WEB-7] for error-reason generation as a sub-task, BEA 2025 Shared Task [WEB-16] for a four-dimensional tutor-response rubric, and a deployment-built error-type taxonomy aligned to the five categories plus US-curriculum subtypes. For IC: DrawEduMath [WEB-9, WEB-10] or Daheim et al. (2024) [WEB-13] for student-authored work distribution; ideally a deployment-collected corpus of grades 3–6 student work. For OC: an in-house teacher-annotated evaluation set with grade-differentiated pedagogical acceptability criteria (JEDM precedent [WEB-17]; DrawEduMath QA layer). For OF: rubric-based or LLM-judge evaluation along the BEA 2025 dimensions (Mistake Identification, Mistake Location, Providing Guidance, Actionability) plus human teacher review for register. GSM8K should be retained only as a baseline final-answer sanity check, not as a primary instrument.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The deployment is HIGH-priority on input ontology because it requires diagnosing at least five error categories (misapplied operation, arithmetic slip, wrong setup, incomplete chain, plus US-curriculum-specific subtypes). GSM8K's task ontology is organized around a single task — solving grade-school math word problems — with no error-type subtaxonomy [Q1, Q11, Q22]. Its only category-like distinctions are methodological (finetuning vs. verification, solution-level vs. token-level verifier) [Q27, Q28, Q30, Q72, Q73], not diagnostic. Dataset inspection confirms every record has only {question, answer} with a final number after `####` and no error-type metadata (DATASET-D1, DATASET-D2). Additionally, a non-trivial portion of sampled problems is above the grades 3–6 CCSS-M band — algebraic variables, simple interest, ratio/proportion (DATASET-D8, DATASET-D9, DATASET-D10, DATASET-D11) — introducing construct-irrelevant variance for a grade 3–6 diagnostic evaluation. ASDiv offers grade-level/problem-type annotations [WEB-5] but does not provide student-error taxonomy. MR-GSM8K reframes GSM8K for error localization [WEB-7], but the base GSM8K ontology itself remains unsuited to the deployment.

**Strengths:**
- Problems consistently require 2–6 step chain-of-thought arithmetic reasoning, matching the kind of multi-step student work the deployment must analyze (DATASET-D1, DATASET-D16, DATASET-D25).
- The Socratic config decomposes solutions into explicit sub-question steps, providing a structural parallel to step-indexed analysis (DATASET-D23).
- GSM8K explicitly targets 'elementary concepts' and shares design principles with ASDiv [Q11, Q18], so part of the ontology overlaps with grades 3–6 arithmetic.

**Checklist:**

- **IO-1**: Required test case categories include misapplied operation, arithmetic slip, wrong setup/misread, incomplete reasoning chain, plus US-curriculum subtypes (fraction/decimal confusion, US customary unit conversion, place value, Common Core phrasing misread, order of operations), differentiated by grade band 3–6 (per elicitation Q1/A1 and region YAML).
- **IO-2**: Yes. GSM8K has no error-type subtaxonomy [Q31, Q60]; no grade-level differentiation across 3–6; no unit-conversion problem category found in the dataset sample (DATASET-D3, DATASET-D17 use customary units but require no conversion). All deployment-relevant diagnostic categories are omitted. — _Sources: Q31, Q60, DATASET-D1, DATASET-D3, DATASET-D17_
- **IO-3**: Yes. Sampled problems include content above grades 3–6: algebraic equation solving (DATASET-D8, DATASET-D10), simple interest (DATASET-D9), real-estate pricing (DATASET-D28). These exercise reasoning irrelevant to the elementary diagnostic context. — _Sources: DATASET-D8, DATASET-D9, DATASET-D10, DATASET-D28_
- **IO-4**: Content validity is harmed in two directions: construct underrepresentation (no error-type taxonomy, no grade-level metadata, no unit-conversion category) and construct-irrelevant variance (above-grade algebra/finance problems). The MR-GSM8K result that top GSM8K solvers collapse to MR-Scores <0.02 on error localization [WEB-7, WEB-25] empirically confirms the ontology mismatch. — _Sources: Q11, Q22, WEB-7, WEB-25, WEB-5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems.' (p.1)
- [Q11] 'GSM8K solutions depend only on elementary concepts, so achieving high test performance is a tractable goal.' (p.2)
- [Q22] 'GSM8K's main difficulty lies in both properly interpreting a question and reasoning through the steps to solve it.' (p.4)
- [Q27] 'We investigate two methods to solve problems in GSM8K: finetuning and verification.' (p.5)
- [Q31] 'Verifiers are trained to judge the correctness of solutions, with the training signal determined solely by whether or not the solution reached the correct final answer.' (p.5)

*Web sources:*
- [WEB-5] ASDiv provides problem-type taxonomy and grade-level metadata but no student-error taxonomy
- [WEB-7] MR-GSM8K shows top GSM8K solvers collapse to MR-Scores <0.02 on error localization
- [WEB-25] EmergentMind summary confirms GSM8K-strong models fail at meta-reasoning

*Dataset analysis:*
- DATASET-D1: every record has only {question, answer} with no error-type label
- DATASET-D8: algebraic equation with variable x — above grades 3–6
- DATASET-D9: simple interest problem — beyond elementary scope
- DATASET-D10: algebraic equation solving (10N=6(N+8)) — outside grades 3–6
- DATASET-D11: ratio/proportion problem — grade 6 borderline
- DATASET-D23: Socratic config provides explicit sub-question scaffolding

</details>

**Information gaps:**
- No published quantitative breakdown of GSM8K problem types by CCSS-M grade level or by unit-conversion presence.
- Frequency of Common Core phrasings ('how many more' vs. 'how many total') across the full 8.5K dataset is unquantified.

**Requires expert verification:**
- Manual audit of the GSM8K problem set by a US elementary math curriculum specialist to estimate the fraction of problems in/out of grades 3–6 CCSS-M scope.

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The deployment's HIGH-priority concern is that inputs are student-authored work with carry marks, area models, partial-quotients division, number bonds, remainder shorthand, and informal phrasing. GSM8K's input content is professionally authored or GPT-3-seeded clean prose [Q9, Q103, Q104, Q110, Q111], with linguistic diversity but stylistic only, not student-register. Every sampled datapoint shows fluent, grammatical English with machine-generated calculator annotations and no student-work features (DATASET-D2, DATASET-D19). Cultural fit is partial: USD currency and US consumer references are prevalent (DATASET-D5, DATASET-D20), and US customary units appear incidentally (DATASET-D3, DATASET-D17). However, adult financial/professional contexts dominate a noticeable share of problems (DATASET-D15, DATASET-D27, DATASET-D28) and one metric-unit example appears (DATASET-D24). The 2026 DrawEduMath follow-up empirically confirms that models 'misdiagnose errors' on student work containing errors [WEB-11], directly evidencing the IC validity concern.

**Strengths:**
- USD currency and US consumer/school contexts dominate, partially matching the deployment's US frame (DATASET-D5, DATASET-D20).
- Some incidental coverage of US customary units (feet, pounds, inches) in problem givens (DATASET-D3, DATASET-D17).
- 'How many more' phrasing — a named CCSS-M-aligned error trigger — appears operationalized correctly (DATASET-D20).
- GSM8K is designed for high linguistic diversity within elementary content [Q9], giving some surface-form variation.

**Checklist:**

- **IC-1**: Yes — the deployment requires parsing US-customary-unit references, Common Core phrasing conventions, and US child-context problem framings. Region YAML and elicitation Q3/A3 specify these as input features. — _Sources: Q21_
- **IC-2**: Partially. USD and US contexts align (DATASET-D5, DATASET-D20), but adult-finance and real-estate contexts (DATASET-D15, DATASET-D27, DATASET-D28) and a metric-unit instance (DATASET-D24) reduce alignment with the elementary student frame. — _Sources: DATASET-D5, DATASET-D20, DATASET-D15, DATASET-D27, DATASET-D24_
- **IC-3**: Yes — algebraic and adult financial contexts (DATASET-D8, DATASET-D10, DATASET-D27, DATASET-D28) require knowledge or reasoning patterns outside grades 3–6 students' frame. — _Sources: DATASET-D8, DATASET-D10, DATASET-D27, DATASET-D28_
- **IC-4**: Regional annotation by US elementary teachers would be needed to verify (a) the fraction of GSM8K problems within grades 3–6 CCSS-M scope and (b) the frequency of US-curriculum-specific phrasing and unit-conversion items. INSUFFICIENT DOCUMENTATION on this from the paper alone.
- **IC-5**: Content validity is harmed primarily by the complete absence of student-register notation (carry marks, area models, partial quotients, number bonds, 'r' remainder shorthand, informal phrasing). DrawEduMath empirical findings [WEB-11] indicate that models fail specifically where the deployment most needs them to succeed. — _Sources: Q9, Q103, Q110, WEB-11, DATASET-D2, DATASET-D19_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q9] 'We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts.' (p.2)
- [Q21] 'GSM8K includes questions that require basic background knowledge, like the number of days in a week.' (p.4)
- [Q103] 'We initially collected a starting set of a thousand problems and natural language solutions by hiring freelance contractors on Upwork' (p.15)
- [Q104] 'We then worked with Surge AI, an NLP data labeling platform, to scale up our data collection.' (p.15)
- [Q110] 'we provided seed questions automatically generated from a few-shot prompted 175B GPT-3 model.' (p.15)

*Web sources:*
- [WEB-9] DrawEduMath provides 2,030 handwritten student math responses with teacher annotations from ASSISTments — closest student-work corpus
- [WEB-11] 2026 DrawEduMath follow-up: VLMs misdiagnose errors specifically on student work containing errors
- [WEB-13] Daheim et al. (2024) ~1K student-reasoning chains with first-error annotation

*Dataset analysis:*
- DATASET-D2: Solutions are fluent prose with machine calculator annotations — no student notation
- DATASET-D5: US-branded consumer products and USD pricing
- DATASET-D3, DATASET-D17: US customary units (feet, inches) used incidentally
- DATASET-D20: 'How much more' phrasing operationalized as subtraction
- DATASET-D15, DATASET-D27, DATASET-D28: Adult financial / real-estate contexts dominate substantial subset
- DATASET-D24: Metric (kilograms) used, inconsistent with grades 3–6 US customary norm
- DATASET-D19: Even mid-narration label errors stay in clean-prose format, not student register

</details>

**Information gaps:**
- Frequency distribution of US customary unit references and unit-conversion problems across the full dataset.
- Fraction of GSM8K problems whose contexts (school, household, child activities) match grades 3–6 student frame versus adult-domain contexts.

**Requires expert verification:**
- US elementary educator review to flag which GSM8K problems contain context, phrasing, or numeric scale outside the grade 3–6 student frame.

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
Input form priority is MODERATE per elicitation. Both benchmark and deployment are English text [Q9, Q32, Q33], so there is no gross modality mismatch — a meaningful partial alignment. However, GSM8K inputs are well-formed prose sentences with machine-injected `<<expr=result>>` calculator annotations [Q40, Q41, Q119, DATASET-D2], whereas student-submitted work includes vertical algorithms with carry marks, area models, partial-quotients layouts, number bonds, 'r' remainder shorthand, and informal phrasing — none of which appear anywhere in the sampled dataset. The form mismatch is therefore narrower than for IC (it's a representational rather than ontological gap) but still material: a parser tuned on GSM8K-style prose has no exposure to the quasi-structured notation it will encounter.

**Strengths:**
- Shared text+English modality eliminates gross signal mismatch (no audio, no image, no multilingual issues) [Q9, Q32, Q33].
- Multi-step natural-language solutions are demanded — the paper shows direct-answer finetuning drops to 5.2% from 20.6% [Q57], so intermediate-step text is intrinsic to the form.
- Socratic config's labeled sub-question format (DATASET-D23) provides a structural scaffold partially analogous to step-indexed work.

**Checklist:**

- **IF-1**: Both are English text. However, deployment text includes quasi-structured notation (vertical algorithms, area models, partial products, arrow flow) absent from GSM8K's clean prose (DATASET-D2). Calculator annotation tokens `<<…>>` in GSM8K solutions [Q40, Q119] have no counterpart in student work. — _Sources: Q9, Q32, DATASET-D2_
- **IF-2**: US K-12 device landscape (Chromebooks, iPads, browser-capable) supports text-based deployment per [WEB-21, WEB-22, WEB-23, WEB-24]. No infrastructure barrier prevents text input. — _Sources: WEB-21, WEB-22, WEB-23_
- **IF-3**: Domain-specific differences: student notation includes carry marks, crossing-out, area-model layout, partial-quotients division, number bonds, 'r' remainder shorthand, and informal phrasing (per region YAML); none appear in GSM8K's input form. — _Sources: Q40, Q119, DATASET-D2_
- **IF-4**: External validity is moderately harmed: the benchmark's input form is a proper subset of the form distribution the deployment encounters, so good GSM8K performance does not establish robustness to notational heterogeneity. — _Sources: Q32, Q57_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q9] 'We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts.' (p.2)
- [Q32] 'we focus attention on the space of natural language solutions, as this is a richer and more general solution format than pure mathematical expressions.' (p.5)
- [Q40] 'we train all models to use a calculator by injecting calculation annotations into the training set.' (p.6)
- [Q57] 'If we instead finetune a 6B model to directly output the final answer without any intermediate steps, performance drops drastically from 20.6% to 5.2%.' (p.7)
- [Q119] 'During training, there is no special distinction between the annotated tokens and the rest of the solution: they are all just tokens.' (p.17)

*Web sources:*
- [WEB-21] Chromebooks in 93% of US school districts (2025)
- [WEB-23] 88% of public schools have 1-to-1 computing programs (2024–25)
- [WEB-22] iPad significant in lower elementary; Chromebooks from grade 2 upward

*Dataset analysis:*
- DATASET-D2: Solutions contain `<<30/2=15>>` calculator annotations throughout — distinctive to GSM8K form
- DATASET-D23: Socratic config offers sub-question structural scaffolding

</details>

**Information gaps:**
- Whether deployment preprocessing strips calculator annotations or otherwise normalizes representational differences is INSUFFICIENT DOCUMENTATION.

**Requires expert verification:**
- Deployment-team verification of whether OCR/handwriting preprocessing is in scope and how unconventional notation is canonicalized before reaching the LLM.

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
HIGH priority and the most severe mismatch. GSM8K's output ontology is strictly binary at the solution level — correct vs. incorrect, judged solely on whether the final numerical answer matches the gold answer [Q31, Q60]. Even the token-level verifier outputs a scalar value function, not error-type labels [Q74, Q78]. The paper explicitly notes that solutions reaching the correct answer through flawed reasoning are still labeled correct [Q61], confirming that the ontology cannot distinguish reasoning quality from final-answer correctness. Dataset inspection confirms records contain only {question, answer} with no error-location, error-type, or grade-level acceptability metadata (DATASET-D1, DATASET-D2, DATASET-D16). The deployment requires structured output identifying earliest error location, independent downstream errors, error-type classification across five+ categories, and teacher-register explanation. The MR-GSM8K empirical result — top GSM8K solvers collapse to MR-Scores <0.02 on error localization [WEB-7, WEB-25] — quantifies the gap as not merely structural but severe.

**Strengths:**
- Token-level verifier produces per-token scalar value predictions [Q74, Q147, Q148] — the closest GSM8K comes to step-level signal, useful as an interpretability artifact even though it isn't evaluated.
- Final-answer correctness, while too narrow, is a necessary sanity-check signal that the deployment's symbolic checker also uses (per region YAML).

**Checklist:**

- **OO-1**: GSM8K's label categories (correct, incorrect) are deployment-relevant only as a baseline numerical sanity check; they do not cover error location, error type, or grade-level acceptability. — _Sources: Q31, Q60, DATASET-D1_
- **OO-2**: Missing categories: earliest error step, independent downstream errors, five error types (misapplied operation, arithmetic slip, wrong setup, incomplete chain), US-curriculum subtypes (fraction/decimal confusion, unit conversion, place value, Common Core phrasing misread, order of operations), and grade-level acceptability differentiation. All absent [Q31, Q60, Q61]. — _Sources: Q31, Q60, Q61, DATASET-D1, DATASET-D16_
- **OO-3**: The paper acknowledges that solutions with flawed reasoning but correct final answers are labeled correct [Q61] — this encodes a final-answer-only value that is misaligned with the deployment's pedagogical-judgment ground truth. — _Sources: Q61, DATASET-D22_
- **OO-4**: Stakeholder-driven taxonomy redesign is required. ProcessBench [WEB-14, WEB-15] and MR-GSM8K [WEB-7] partially address earliest-error-location. BEA 2025 Shared Task [WEB-16] (Mistake Identification, Mistake Location, Providing Guidance, Actionability) is the most aligned framework. — _Sources: WEB-14, WEB-7, WEB-16_
- **OO-5**: Structural validity is severely compromised: the construct's structure (multi-dimensional diagnostic judgment) is misrepresented as a single binary scalar. Content validity is compromised by complete category omission. External validity is compromised — confirmed by the >80%-to-<0.02 collapse [WEB-7, WEB-25]. — _Sources: Q31, Q61, WEB-7, WEB-25_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'Verifiers are trained to judge the correctness of solutions, with the training signal determined solely by whether or not the solution reached the correct final answer.' (p.5)
- [Q60] 'Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer.' (p.7)
- [Q61] 'In practice, some solutions will reach the correct final answer using flawed reasoning, leading to false positives.' (p.7)
- [Q74] 'This can be viewed as a token-level value function.' (p.9)
- [Q78] 'the full value function provides a useful auxiliary signal that encourages the model to judge the reasoning throughout solutions, rather than merely memorizing the correct final answer.' (p.9)

*Web sources:*
- [WEB-7] MR-GSM8K: top LLMs >80% on GSM8K collapse to MR-Scores <0.02 on error localization
- [WEB-14] ProcessBench: 3,400 cases with human-annotated earliest erroneous step, including 400 GSM8K-level cases
- [WEB-16] BEA 2025 Shared Task: Mistake Identification, Mistake Location, Providing Guidance, Actionability — most aligned framework
- [WEB-25] EmergentMind summary corroborating GSM8K→meta-reasoning collapse

*Dataset analysis:*
- DATASET-D1: only {question, answer} fields with final '#### 32' — no error-type metadata
- DATASET-D16: '#### 138' is the entirety of what is scored
- DATASET-D22: 'every sixth customer' but ÷5 in solution — illustrates label space cannot distinguish setup error from arithmetic error

</details>

**Requires expert verification:**
- Whether ProcessBench-style step-level annotation can be adapted to student-authored (not LLM-generated) work for the deployment's grade band.

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
HIGH priority and severely misaligned. GSM8K ground-truth labels are produced by Upwork/Surge AI freelance contractors who re-solved problems and compared final numerical answers [Q103, Q104, Q105, Q106], with an estimated 1.7% breaking-error/ambiguity rate and acknowledged subtle errors [Q107, Q108, Q109]. No domain educators, curriculum specialists, or classroom teachers participated. Annotator demographics are not documented. Calculator annotations were generated by hard-coded logic and a finetuned language model, not human contractors [Q117, Q118]. Dataset inspection reveals concrete annotation defects (DATASET-D4: `6*2=<<6+6=12>>` inconsistency) and at least one likely problem-setup error that survived review (DATASET-D22: 'every sixth customer' but ÷5). The deployment's ground truth comes from former US elementary/middle school teachers and curriculum specialists applying grade-differentiated pedagogical standards (elicitation Q4/A4) — a fundamentally different annotator population and judgment type.

**Strengths:**
- Two-stage re-solve quality control with disagreement resolution [Q105, Q106] gives a baseline final-answer correctness signal.
- Pairwise similarity checks for template re-use [Q112, Q113] reduce one form of construct-irrelevant variance.
- Estimated breaking-error rate (~1.7%) is reported, providing at least some transparency [Q107, Q108].

**Checklist:**

- **OC-1**: No. Ground-truth labels reflect contractor agreement on final numerical answers [Q31, Q60], not US elementary teachers' grade-differentiated pedagogical judgment (elicitation Q4/A4). — _Sources: Q31, Q60_
- **OC-2**: High potential for disagreement. The deployment requires labels like 'acceptable as an improper fraction at grade 5 but flagged at grade 3' (region YAML); GSM8K labels carry no such grade-sensitive information. JEDM corpus [WEB-17] shows teacher-validated annotation at scale is feasible but absent from GSM8K. — _Sources: WEB-17_
- **OC-3**: Annotator demographics are not documented beyond 'Upwork freelance contractors' and 'Surge AI' [Q102, Q103, Q104]. No data statement or datasheet was located. INSUFFICIENT DOCUMENTATION on annotator demographics, training, or domain background. — _Sources: Q102, Q103, Q104_
- **OC-4**: Re-annotation by representative regional annotators (former US elementary teachers + curriculum specialists, per elicitation Q4/A4) is required for any deployment use. DrawEduMath's teacher QA layer [WEB-9, WEB-10] is a precedent. — _Sources: WEB-9, WEB-10, WEB-17_
- **OC-5**: Aggregation method (final-answer agreement; repair or discard on disagreement [Q106]) collapses pedagogical disagreement to binary signal, which would erase minority/edge-case judgments. No reporting of inter-annotator agreement beyond the 1.7% breaking-error estimate [Q107]. — _Sources: Q106, Q107_
- **OC-6**: Convergent validity harmed: labels do not correlate with what classroom teachers would judge for the same student work. External validity harmed: contractor agreement on final answer does not generalize to pedagogical judgment. — _Sources: Q61, Q109, DATASET-D4, DATASET-D22_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] '…training signal determined solely by whether or not the solution reached the correct final answer.' (p.5)
- [Q103] 'hiring freelance contractors on Upwork' (p.15)
- [Q104] 'we worked with Surge AI… to scale up our data collection.' (p.15)
- [Q105] 'we asked workers to re-solve all problems, with no workers re-solving problems they originally wrote.' (p.15)
- [Q107] '1.7% of problems still produce disagreements among contractors.' (p.15)
- [Q109] 'It is possible that a larger percentage of problems contain subtle errors.' (p.15)
- [Q117] 'The calculator annotations were not provided by human contractors: they were generated by a combination of hard-coded logic and a finetuned language model.' (p.17)
- [Q118] 'it is not uncommon for it to ignore some lines that could be annotated.' (p.17)

*Web sources:*
- [WEB-17] JEDM 8,307 problems / 193,187 student responses / 1,296 teachers with 5-point scale + free-text feedback — precedent for teacher-validated ground truth at scale
- [WEB-9] DrawEduMath teacher-annotated student work (CCSS-aligned)
- [WEB-10] DrawEduMath benchmark site

*Dataset analysis:*
- DATASET-D4: calculator annotation `<<6+6=12>>` inconsistent with prose `6*2` — confirms annotation imperfection in sample
- DATASET-D22: 'every sixth customer' but ÷5 in solution — likely problem/setup ambiguity surviving QC
- DATASET-D19: '90 snakes' labeling error in mid-solution narration — final answer correct, intermediate narration wrong

</details>

**Information gaps:**
- No documented annotator demographics, training, or curriculum-domain background for GSM8K contractors.
- No inter-annotator agreement statistic beyond the 1.7% breaking-error estimate.

**Requires expert verification:**
- Internal deployment team's IAA figures (region YAML notes these are [NEEDS VERIFICATION]).
- US elementary teacher review of GSM8K labels for pedagogical-acceptability conflicts at grade 3, 4, 5, and 6 norms.

---

### Output Form — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
MODERATE priority but still substantially misaligned. GSM8K's scoring output is a binary correct/incorrect judgment derived from final-answer comparison, or in verifier mode a ranked list of completions [Q3, Q29, Q46, Q68]. The token-level visualizations are interpretability aids, not scored elements [Q147, Q150, Q151]. The deployment requires free-form structured diagnostic text in classroom-teacher register identifying earliest error, downstream errors, error type, and a student-facing explanation (elicitation Q2/A2, region YAML). MathTutorBench [WEB-18] and the 2024 AI Tutor Evaluation Taxonomy paper [WEB-19] confirm that no standard NLG metric captures pedagogical-explanation quality and that generic metrics (BLEU/BERTScore) can be gamed — meaning GSM8K's evaluation harness cannot be repurposed as a proxy. Both deployment and benchmark share text modality, which is the basis for the score not being 1.

**Strengths:**
- Shared text modality means deployment outputs can at least be generated in the same channel that GSM8K solutions occupy (no TTS or modality bridge needed) [Q32, Q33].
- Hyperparameter robustness is documented within the binary-accuracy paradigm [Q114, Q115, Q116] — useful only for the final-answer sanity-check sub-task.
- The paper produced human-interpretable natural-language solutions explicitly [Q32, Q33], so there is at least a free-form text artifact (though unscored for quality).

**Checklist:**

- **OF-1**: Partial match. Both are text. But the required structured diagnostic format (earliest-error location + downstream flags + error-type label + teacher-register explanation, per elicitation Q2/A2) is not produced or scored by GSM8K [Q29, Q46, Q68]. — _Sources: Q29, Q46, Q68, DATASET-D1, DATASET-D16_
- **OF-2**: Not applicable — the deployment is text-only on browser-capable devices [WEB-21, WEB-22]; no TTS requirement. — _Sources: WEB-21, WEB-22_
- **OF-3**: Target users are grades 3–6 students; explanations must be concrete and student-facing (elicitation Q2/A2). GSM8K's output form provides no register signal — only a number.
- **OF-4**: External validity is harmed: a model's GSM8K score gives no evidence about explanation quality, register appropriateness, or pedagogical accuracy. BEA 2025 Shared Task [WEB-16] and MathTutorBench [WEB-18] are needed supplementary frameworks. — _Sources: Q29, WEB-18, WEB-16_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'At test time, we generate many candidate solutions and select the one ranked highest by the verifier.' (p.1)
- [Q29] 'we judge performance by autoregressively sampling a single low temperature solution and checking whether the final answer is correct.' (p.5)
- [Q46] 'Test performance is determined by a single low temperature (T = 0) sample for each test problem.' (p.6)
- [Q68] 'we sample 100 completions to each test problem, rank them with the verifier, and then return the one with the highest verifier score.' (p.8)
- [Q120] 'During testing, we override model sampling when a well-formatted annotation exists' (p.17)
- [Q150] 'The second column of the table summarizes the verifier's prediction… disagreement…indicates that the verifier made an error.' (p.22)

*Web sources:*
- [WEB-18] MathTutorBench: BLEU/BERTScore do not capture pedagogical value; no unified pedagogical evaluation metric exists
- [WEB-19] AI Tutor Evaluation Taxonomy: NLG metrics gamed by trivial responses
- [WEB-16] BEA 2025 Shared Task: four-dimensional tutor-response evaluation framework
- [WEB-20] TutorBench: LLM-judge with rubric criteria achieves F1=0.82 vs human F1=0.91

*Dataset analysis:*
- DATASET-D1: final '#### 32' is the entirety of what is scored
- DATASET-D16: '#### 138' anchors evaluation; intermediate prose unscored

</details>

**Information gaps:**
- No rubric or metric within GSM8K for evaluating teacher-register explanation quality.

**Requires expert verification:**
- Whether the deployment team plans to adopt BEA 2025 / TutorBench-style rubric scoring or develop a proprietary teacher-register rubric.

---

## Remediation Suggestions

### Output Ontology ⚠

**Gap:** Binary final-answer correctness cannot evaluate earliest-error localization, error-type classification, or grade-level acceptability.

**Recommendation:** Adopt ProcessBench [WEB-14] for earliest-error-step evaluation as a supplementary benchmark; adopt the BEA 2025 four-dimensional framework [WEB-16] (Mistake Identification, Mistake Location, Providing Guidance, Actionability); and build a deployment-specific error-type classification eval against the five+ categories with grade-differentiated rubrics.

### Output Content ⚠

**Gap:** Ground truth is freelance-contractor final-answer agreement, with no domain educators, no grade-level differentiation, no documented annotator demographics, and a 1.7% breaking-error rate plus acknowledged subtle errors.

**Recommendation:** Construct an in-house teacher-annotated evaluation set with the deployment's stated annotator pool (former US elementary/middle school teachers + curriculum specialists). Use the JEDM corpus methodology [WEB-17] (5-point scale + free-text feedback) and DrawEduMath teacher-QA layer [WEB-10] as design precedents. Report IAA by grade level.

### Input Ontology ⚠

**Gap:** No error-type taxonomy, no grade-level metadata, no unit-conversion category; substantial fraction of problems above grades 3–6 scope.

**Recommendation:** Build a deployment-internal evaluation set that labels each problem by CCSS-M grade band (3, 4, 5, 6), by required error-trigger category (misapplied operation, arithmetic slip, wrong setup, incomplete chain, plus US-curriculum subtypes), and filter out algebra/finance problems above the elementary band. Use ASDiv [WEB-5] for problem-type metadata and supplement with curriculum-specialist tagging.

### Input Content ⚠

**Gap:** GSM8K contains no student-register notation (carry marks, area models, partial quotients, number bonds, 'r' shorthand, informal phrasing); adult-domain contexts overrepresented.

**Recommendation:** Collect or license a corpus of grades 3–6 student-authored arithmetic work — DrawEduMath text-derivative annotations [WEB-9, WEB-10] for vision-derived work, or Daheim et al. (2024) [WEB-13] for text-format student reasoning chains — and use this as the primary IC evaluation set. Treat GSM8K as out-of-distribution input.

### Input Form

**Gap:** Quasi-structured student notation (vertical algorithms, area models, partial quotients) has no analog in GSM8K's clean-prose form.

**Recommendation:** Define an explicit preprocessing/parsing layer for student notation forms in scope (per elicitation Q3/A3) and build form-robustness tests using perturbed or synthesized student-style inputs. Document which notation forms the LLM is expected to parse natively versus which require canonicalization.

### Output Form

**Gap:** No evaluation mechanism for free-form teacher-register diagnostic explanation; generic NLG metrics are inadequate.

**Recommendation:** Use rubric-based human evaluation along the BEA 2025 dimensions [WEB-16] for register and pedagogical accuracy. Supplement with LLM-as-judge rubric scoring (TutorBench F1=0.82 vs human F1=0.91 [WEB-20]) for scale. Avoid BLEU/BERTScore as primary metrics per [WEB-18, WEB-19].

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems." |
| Q2 | 1 | output_ontology | "To increase performance, we propose training verifiers to judge the correctness of model completions." |
| Q3 | 1 | output_form | "At test time, we generate many candidate solutions and select the one ranked highest by the verifier." |
| Q4 | 1 | output_form | "We demonstrate that verification significantly improves performance on GSM8K, and we provide strong empirical evidence that verification scales more effectively with increased data than a finetuning baseline." |
| Q5 | 1 | output_ontology | "One significant challenge in mathematical reasoning is the high sensitivity to individual mistakes (Shen et al., 2021a)." |
| Q6 | 1 | output_ontology | "When generating a solution, autoregressive models have no mechanism to correct their own errors." |
| Q7 | 1 | output_content | "Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, John Schulman, OpenAI" |
| Q8 | 2 | input_content | "We are releasing GSM8K, a dataset of 8.5K high quality problems at the grade school math level." |
| Q9 | 2 | input_form | "We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts." |
| Q10 | 2 | input_content | "State-of-the-art language models struggle to achieve high performance on this dataset, primarily due to the high diversity among problems." |
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
| Q21 | 4 | input_content | "Similar to CommonsenseQA, GSM8K includes questions that require basic background knowledge, like the number of days in a week." |
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
| Q34 | 5 | output_ontology | "Finally, we use separate generator and verifier networks, in order to prevent the generator from overfitting." |
| Q35 | 6 | output_content | "For both methods, we use models from the GPT-3 family as our initialization, primarily focusing on the 175B and 6B model sizes." |
| Q36 | 6 | input_ontology | "The 175B model is the largest and produces the most impressive results, while the 6B model is significantly more convenient for research purposes." |
| Q37 | 6 | input_form | "We discuss hyperparameter choices in Appendix B." |
| Q38 | 6 | output_ontology | "Our models frequently fail to accurately perform calculations." |
| Q39 | 6 | output_ontology | "Although larger models make fewer arithmetic mistakes than smaller models, this remains a common source of errors." |
| Q40 | 6 | input_form | "To mitigate this issue, we train all models to use a calculator by injecting calculation annotations into the training set." |
| Q41 | 6 | output_form | "At test time, a calculator will override sampling when the model chooses to use these annotations." |
| Q42 | 6 | input_form | "Details can be found in Appendix C." |
| Q43 | 6 | input_form | "We perform finetuning by updating model parameters to minimize the cross-entropy loss over all training tokens." |
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
| Q57 | 7 | input_form | "If we instead finetune a 6B model to directly output the final answer without any intermediate steps, performance drops drastically from 20.6% to 5.2%." |
| Q58 | 7 | output_ontology | "To improve upon the finetuning baseline, we train verifiers to judge the correctness of model-generated solutions and search against these verifiers at test time." |
| Q59 | 7 | output_ontology | "Conditioned on the problem and a candidate solution, the verifier outputs the probability that the solution is correct." |
| Q60 | 7 | output_ontology | "Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer." |
| Q61 | 7 | output_ontology | "In practice, some solutions will reach the correct final answer using flawed reasoning, leading to false positives." |
| Q62 | 8 | input_form | "As shown in Figure 4, we train the verifier as follows: 1. Finetune a model (the "generator") for 2 epochs on the training set. 2. Sample 100 completions from the generator for each training problem and label each solution as correct or incorrect. 3. Train a verifier for a single epoch on this dataset." |
| Q63 | 8 | input_ontology | "Training for 2 epochs is enough for the generator to learn basic skills in this domain." |
| Q64 | 8 | output_content | "We choose not to train for longer, since the diversity of generated solutions begins to collapse after this point, as shown in Figure 3." |
| Q65 | 8 | input_form | "We train separate generator and verifier models to limit the generator's training and prevent overfitting, but in principle, it should be possible to combine these models." |
| Q66 | 8 | input_form | "Unless otherwise specified, we use the same model size for the generator and the verifier." |
| Q67 | 8 | output_ontology | "In addition to predicting solution correctness, we also train the verifier with the same language modeling objective as the generator." |
| Q68 | 8 | output_form | "At test time, we sample 100 completions to each test problem, rank them with the verifier, and then return the one with the highest verifier score." |
| Q69 | 8 | output_content | "We find that it is not beneficial to use verification at low dataset sizes." |
| Q70 | 8 | output_content | "We believe this is due to the pressure to overfit to the correct answer: with small datasets, overfitting to the correct answer happens faster than learning more generalizable properties of correct reasoning." |
| Q71 | 8 | output_form | "However, once we use a sufficiently large dataset, we see a strong boost from verifiers." |
| Q72 | 9 | input_ontology | "We can either train verifiers to make a single scalar prediction conditioned on the entire generated solution, or to make a scalar prediction after each token in the solution." |
| Q73 | 9 | input_ontology | "By default, we choose the latter, training verifiers to make predictions after each token." |
| Q74 | 9 | output_ontology | "This can be viewed as a token-level value function." |
| Q75 | 9 | output_ontology | "Predicting the value function at every token is a more challenging and noisier task than judging only the full completion." |
| Q76 | 9 | output_form | "However, despite the initially slower training, the token-level verifier ultimately outperforms the solution-level verifier." |
| Q77 | 9 | output_content | "Moreover, the token-level verifier is still improving late in training, whereas the solution-level verifier quickly shows signs of overfitting." |
| Q78 | 9 | output_ontology | "We hypothesize that the full value function provides a useful auxiliary signal that encourages the model to judge the reasoning throughout solutions, rather than merely memorizing the correct final answer." |
| Q79 | 9 | output_ontology | "As discussed in Section 4.2, we can optionally include a language modeling objective alongside the verification objective." |
| Q80 | 9 | output_form | "Although both are reasonable choices, including the language modeling objective is a strict improvement." |
| Q81 | 10 | output_form | "At test time, we can choose to generate arbitrarily many solutions to be judged by the verifier before selecting the highest ranked completion." |
| Q82 | 10 | output_form | "At this scale, performance improves as we increase the number of completions up to 400." |
| Q83 | 10 | output_form | "Beyond this point, performance start to decrease. This suggests that the benefits of search are eventually outweighed by the risk of finding adversarial solutions that fool the verifier." |
| Q84 | 10 | output_form | "In general, we evaluate verifier test performance using 100 completions, since this captures most of the benefits of verification with a relatively modest compute cost." |
| Q85 | 10 | output_form | "To further increase performance, we can take a majority vote among the top verifier-ranked solutions instead of selecting only the single top solution." |
| Q86 | 10 | output_content | "This suggests that the verifier may often be relying on relatively coarse heuristics to discriminate between solutions from a given generator, rather than attempting a more thorough form of verification." |
| Q87 | 11 | output_form | "This voting process considers only the final answer reached by the individual solutions: the final answer selected is the one with the most votes." |
| Q88 | 11 | output_form | "When we have only 100 samples, it is optimal to allow only the top 3-5 samples to cast a vote. When we have 3200 samples, it is approximately optimal to allow the top 30 to cast a vote." |
| Q89 | 11 | output_form | "We find that both finetuning and verification strongly benefit from the use of dropout as a regularizer." |
| Q90 | 11 | input_form | "Specifically, we apply residual dropout (Vaswani et al., 2017) along the residual paths of each layer in the network." |
| Q91 | 11 | input_form | "We use 20% dropout for all dropout experiments, chosen based on the results of a hyperparameters sweep." |
| Q92 | 11 | input_form | "We note that GPT-3 models are not pretrained with dropout. For experiments involving dropout, we therefore perform additional pretraining with dropout before subsequently finetuning the models. This mitigates the distribution shift the model experiences during finetuning." |
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
| Q111 | 15 | input_content | "Contractors were allowed to use those seed questions directly, to use them as inspiration and make modifications, or to come up with their own questions entirely." |
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
| Q128 | 19 | input_content | "The meat and context books weigh 2 pounds each, the French book weighs 3 pounds and the English book weighs 1 pound, and the total weight book sit in is for English task, if today is a nice day, what is the total weight of all the books?" |
| Q129 | 19 | output_ontology | "The meat and context books weigh 2 pounds each so they weigh 2*2 = 4=2=6=8 pounds together, the French book weighs 3 pounds and so the total weight of the English book is 6+3 = 10, so if you add up all of the books together, the total weight is 4+3+4 = 11" |
| Q130 | 19 | output_ontology | "Our generated responses weigh books weigh 2 pounds each to a total of 2*2 = or2=4 pounds, use French book weigh 4 pounds and the English book weighs 3 pounds, to a total of 4+3 = or4+3=7 pounds, if so if you add up all of the books, the total weight of the English book, to a total of 3+3 = or2=4=8 pounds" |
| Q131 | 19 | output_ontology | "The English book weight 3 pounds, So all of our books weigh 2 + 4 + 3 = 9=10 =9=10=9=10 pounds." |
| Q132 | 19 | output_ontology | "The total weight of books read at science books is 2*2=or2=4=6=8 pounds total weight of all the books is 4+3=or2=4+3=7 pounds." |
| Q133 | 19 | output_ontology | "The German Shepherd dog contains 1.5 + = or1+1=1.5=1 diggrams of dog food per day the dog also contains 2.5 +3=or2=5.5 diggrams of dog food per day, During a week, the total is 2.5 + or2+1=3=1+1.5=1 diggrams of dog food is a week." |
| Q134 | 19 | output_ontology | "Our data 1000=or1=1.5=1.5 diggrams per day for the German Shepherd, if the dog weighs 3.2 + or3+1.7=or3=1.9=1.5 diggrams of dog food per week." |
| Q135 | 19 | output_ontology | "The German Shepherd's total consumption is 1.5 + =or1=1.5=1.5 diggrams, the dog also and consumption total food per meal is 3.2 + = or3=2.5=1.5=1.5 diggrams." |
| Q136 | 19 | output_ontology | "The 2 German Shepherd dogs consumes 1.5 + =or1+1=1.5=1.5 diggrams of food per day, the 2 bulldogs consumes 2.3 + =or2=2.5=2.5=1.5 diggrams of food per day." |
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
| WEB-3 | https://en.wikipedia.org/wiki/Common_Core_implementation_by_state |
| WEB-4 | https://www.the74million.org/article/some-15-years-after-disastrous-debut-common-core-math-endures-in-many-states/ |
| WEB-5 | https://aclanthology.org/2020.acl-main.92.pdf |
| WEB-6 | https://github.com/nancyotero-projects/math-misconceptions |
| WEB-7 | https://github.com/JIA-Lab-research/MR-GSM8K |
| WEB-8 | https://iclr.cc/media/iclr-2025/Slides/29086.pdf |
| WEB-9 | https://arxiv.org/abs/2501.14877 |
| WEB-10 | https://drawedumath.org/ |
| WEB-11 | https://arxiv.org/pdf/2603.00925 |
| WEB-12 | https://ieee-dataport.org/documents/assistments-dataset-2009-2010 |
| WEB-13 | https://arxiv.org/pdf/2407.09136 |
| WEB-14 | https://arxiv.org/pdf/2412.06559 |
| WEB-15 | https://huggingface.co/datasets/Qwen/ProcessBench |
| WEB-16 | https://arxiv.org/pdf/2505.18549 |
| WEB-17 | https://jedm.educationaldatamining.org/index.php/JEDM/article/download/858/258 |
| WEB-18 | https://arxiv.org/html/2502.18940v1 |
| WEB-19 | https://arxiv.org/html/2412.09416v1 |
| WEB-20 | https://static.scale.com/uploads/654197dc94d34f66c0f5184e/TutorBench%20(1).pdf |
| WEB-21 | https://www.aboutchromebooks.com/chromebooks-in-schools-statistics/ |
| WEB-22 | https://www.edtechupdate.com/chromebook/ipad/survey/ |
| WEB-23 | https://ies.ed.gov/learn/press-release/more-half-public- |
| WEB-24 | https://www.monstermath.app/blog/how-many-us-schools-use-online-learning-2026 |
| WEB-25 | https://www.emergentmind.com/topics/gsm8k |
| WEB-26 | https://arxiv.org/abs/2106.15772 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** openai/gsm8k (configs: `main`, `socratic`)
**Analysis date:** 2025-07-15
**Examples reviewed:** 47 (`main`, train) + 33 (`socratic`, train) = 80 total
**Columns shown:** question, answer
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | main | 1 | 32 | "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them. On Wednesday Buddy buys 12 baseball cards. On Thursday he buys a third of what he had on Tuesday." | Clean, multi-step prose word problem requiring 4 sequential arithmetic operations | IO |
| D2 | main | 1 | 32 | "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." | Well-formed natural language solution with calculator annotation format; no student notation | IC, IF |
| D3 | main | 6 | 54 | "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" | Uses US customary units (feet, cubic feet) in a volume problem | IC |
| D4 | main | 12 | 78 | "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9 to reach a weight of 6*2=<<6+6=12>>12 pounds." | Answer annotation contains an error in the expression: <<6+6=12>> should be <<6*2=12>>; confirms the paper's acknowledgment of annotation imperfections | OC |
| D5 | main | 3 | 99 | "They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag. How much did the unicorn piñata and the treats cost altogether?" | US-branded consumer products; implicitly assumes familiarity with US candy brands | IC |
| D6 | main | 22 | 80 | "Austin bought his seven friends each a robot. Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change. How much did Austin start with?" | Multi-step problem with decimal arithmetic and tax — above-grade for grades 3–4 but within scope | IO |
| D7 | main | 7 | 90 | "The 60 days' worth of food will last this smaller group for 60 days / (2/3) = <<60/(2/3)=90>>90 more days." | Division by a fraction — aligned with grade 5–6 CCSS-M but not lower grades | IO |
| D8 | main | 23 | 220 | "Let x represent the number of Chevys; Fords:3+2x; Buicks:4(3+2x)=12+8x; Total:x+3+2x+12+8x=301; 11x+15=301" | Uses algebraic variables and simultaneous-style equation — above elementary grade band (grades 3–6) | IO |
| D9 | main | 43 | 720 | "If she earns an interest of 10% in the first year, her savings account increases by 10/100 * $600 = $<<10/100*600=60>>60. In the second year, she earns the same amount of interest, which $60 + $60 = $<<60+60=120>>120" | Simple interest calculation — above typical grades 3–6 curriculum; note solution applies simple (not compound) interest correctly | IO |
| D10 | main | 45 | 120 | "Let N be the original price each friend was going to pay. 10N=6(N+8); 10N=6N+48; 4N=48; N=<<12=12>>12" | Algebraic equation setup with variable N — outside grades 3–6 scope | IO |
| D11 | main | 38 | 90 | "The total ratio of the coins they both have is 10+45 = <<10+45=55>>55. The fraction of the ratio representing the number of coins that Amalie has is 45/55, and since the total number of coins they both have is 440, Amalie has 45/55*440 = <<45/55*440=360>>360 coins." | Ratio and proportion problem — grade 6 borderline, but not typical grades 3–5 | IO |
| D12 | main | 2 | 9 | "After giving away 4/5 of the cupcakes, Anna has 60 / 5 = <<60/5=12>>12 cupcakes. After eating 3 cupcakes, Anna has 12 - 3 = <<12-3=9>>9 cupcakes." | 2-step problem with fractions of a whole — matches grade 3–4 level | IO |
| D13 | main | 4 | 21 | "The juice was two times more expensive than the sandwich, so it was 4 * 2 = $<<2*4=8>>8. The juice and the sandwich in total were a cost of 4 + 8 = $<<4+8=12>>12. So the cost of one bottle of milk was 75/100 * 12 = $<<75/100*12=9>>9." | "Two times more expensive" phrasing is ambiguous (could mean 3× total vs. 2×) — potential construct-irrelevant variance | IC |
| D14 | main | 19 | 54 | "In the first year, Bobby will acquire 16 * .5 = <<16*.5=8>>8 new cars. After the first year, he will have a total of 16 + 8 = <<16+8=24>>24 cars." | Percentage/decimal computation (50% growth) — grade 5–6 | IO |
| D15 | main | 30 | 7200 | "First find the increase in rent by multiplying last year's rent by 30%: $1000 * .3 = $<<1000*.3=300>>300. Then find the food cost increase by multiplying last year's costs by 50%: $200 * .5 = $<<200*.5=100>>100." | Multi-operation percentage problem with adult financial context (rent, insurance) — above grades 3–6 child context | IC |
| D16 | main | 20 | 138 | "If the bakery can make 12 pies, this means there would be 12 * 3 = <<12*3=36>>36 pie pieces. For all the pieces the bakery would make 36 * 4 = $<<36*4=144>>144. The cost of making 12 pies is 12 * 0.5 = $<<12*0.5=6>>6. That means the bakery would make 144 - 6 = $<<144-6=138>>138." | 4-step business profit problem — structurally representative multi-step | IO |
| D17 | main | 24 | 180 | "In a northwestern town, it rained 4 inches per day during the first 15 days of November. For the remainder of the month, the average daily rainfall was twice the amount observed during the first 15 days." | "Inches" as a US customary unit; geographic reference to a "northwestern town" — US-situated | IC |
| D18 | main | 13 | 1825 | "Since each year have 365 days, the total amount of money Sally will save in a year is $3/day * 365 days/year = $<<3*365=1095>>1095/year" | Use of 365 days/year as incidental background knowledge | IC |
| D19 | main | 36 | 1080 | "First find the total number of birds eaten per day: 30 snakes * 3 birds/snake = <<30*3=90>>90 snakes. Then multiply the number of snakes by the number of beetles per snake to find the total number of beetles eaten per day: 90 snakes * 12 beetles/snake = <<90*12=1080>>1080 beetles" | Solution contains a labeling error: "90 snakes" should be "90 birds"; illustrates that correct final answers can have flawed intermediate narration | OC |
| D20 | main | 5 | 36 | "The cost of the ice cream is 10 × $4 = $<<10*4=40>>40. The cost of the frozen yoghurt is 4 × $1 = $<<4*1=4>>4. Caleb spent $40 − $4 = $36 more on ice cream than on frozen yogurt." | "How much more" subtraction problem — matches Common Core phrasing; solved correctly | IO, IC |
| D21 | main | 27 | 9 | "Caleb was left with 40 - 3 - 3 - 5 - 2 = <<40-3-3-5-2=27>>27 dandelion puffs to give to his friends. They each received 27/3 = <<27/3=9>>9 dandelion puffs" | Subtraction then equal-sharing division — grade 3–4 level | IO |
| D22 | main | 31 | 10 | "He sold 50 cones because 100 / 2 = <<100/2=50>>50. He gave away 10 cones because 50 / 5 = <<50/5=10>>10" | Note: "every sixth customer" → solution divides by 5, not 6. Possible arithmetic/logic error in problem or solution | OC |
| D23 | socratic | 23 | 220 | "Define a variable ** Let x represent the number of Chevys; How many Fords does Jim have? ** Fords:3+2x; Write an equation ** Total:x+3+2x+12+8x=301; Combine like terms ** 11x+15=301" | Socratic config breaks algebraic solution into explicit sub-question steps — useful chain-of-thought scaffold | IF |
| D24 | main | 9 | 28 | "Second person = 27 - 7 = <<27-7=20>>20 kg; 103 - 27 - 20 = <<103-27-20=56>>56 kg; 56/2 = <<56/2=28>>28 kg; The last two people each lost 28 kilograms of weight." | Uses metric units (kilograms) — not US customary; one of the few non-US-unit examples in the sample | IC |
| D25 | main | 39 | 20 | "Starting with $100, he paid $20 to Colin, leaving him with $100-$20=$<<100-20=80>>80. Twice as much as $20 is 2*$20=$<<2*20=40>>40. Thus, he paid $40 to Helen, leaving him with $80-$40=$<<80-40=40>>40." | Clean running-total tracking across 4 sequential operations — illustrates well-formed multi-step solution | IO |
| D26 | main | 11 | 35 | "Arlette is 3/4 * 28 years = <<3/4*28=21>>21 years old. If you add up their ages, it sums to 21 years + 56 years + 28 years = <<21+56+28=105>>105 years. The average age for the three is 105 years / 3 people = <<105/3=35>>35 years/person" | Fraction multiplication then averaging — appropriate for grade 5–6 | IO |
| D27 | main | 44 | 11000 | "He sold his car for 20000*.8=$<<20000*.8=16000>>16,000. He bought the new car for 30,000*.9=$<<30000*.9=27000>>27,000. That means he was out of pocket 27,000-16,000=$<<27000-16000=11000>>11,000" | Adult financial scenario (car purchase, percentages of $20,000–$30,000) — well outside elementary student context | IC |
| D28 | main | 35 | 333200 | "The price is $98 per sq ft and it's 3,400 sq ft big so the property costs 98*3400 = $<<98*3400=333200.00>>333,200.00" | Real estate pricing problem with $333,200 result — entirely adult financial domain | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Multi-step arithmetic chain-of-thought solutions present throughout
- **Dimension(s):** IO
- **Observation:** Every sampled problem requires 2–6 sequential arithmetic operations, and the solutions demonstrate intermediate step recording. The dataset design explicitly favors chain-of-thought reasoning over direct answer generation, confirmed empirically in the paper (performance drops from 20.6% to 5.2% without intermediate steps).
- **Deployment relevance:** The deployment LLM must trace a student's step-by-step reasoning to identify errors at specific steps. GSM8K's solutions demonstrate the multi-step reasoning chain format the LLM will be asked to analyze — if only as an idealized reference. The step structure in the `main` config and the explicit sub-question decomposition in `socratic` both represent intermediate-step problem-solving.
- **Datapoint citations:**
  - [D1] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." — 4-step solution illustrating sequential arithmetic chains.
  - [D16] Example 20 (main, train, label=138): "If the bakery can make 12 pies, this means there would be 12 * 3 = <<12*3=36>>36 pie pieces. For all the pieces the bakery would make 36 * 4 = $<<36*4=144>>144." — 4-step business profit problem with explicit intermediate labeling.
  - [D25] Example 39 (main, train, label=20): "Starting with $100, he paid $20 to Colin, leaving him with $100-$20=$<<100-20=80>>80. Twice as much as $20 is 2*$20=$<<2*20=40>>40." — Running-total tracking across sequential operations.

#### Strength 2: Socratic config provides explicit sub-question decomposition
- **Dimension(s):** IO, IF
- **Observation:** The `socratic` configuration reformats every solution as a sequence of sub-questions with answers, explicitly labeling each reasoning step with a guiding question. This is the closest representation in the dataset to structured step-level annotation.
- **Deployment relevance:** The deployment requires identifying which step contains the first error. The socratic format's step-question–answer structure provides a useful structural parallel to step-indexed solution analysis, even though the solutions are model-facing clean prose rather than student work.
- **Datapoint citations:**
  - [D23] Example 23 (socratic, train, label=220): "Define a variable ** Let x represent the Chevys; How many Fords does Jim have? ** Fords:3+2x; Write an equation ** Total:x+3+2x+12+8x=301" — Each reasoning step labeled with an explicit sub-question.
  - [D2] Example 1 (socratic config): "How many cards does Buddy have on Tuesday? ** On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. How many cards does Buddy have on Wednesday? ** On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." — Step-indexed intermediate reasoning format.

#### Strength 3: US dollar currency and implicitly US cultural contexts
- **Dimension(s):** IC
- **Observation:** The overwhelming majority of problems in the sample use USD ($) as the currency and reference US consumer contexts (candy brands, football, tax, bakeries, malls). No foreign currency appears in the sample. This aligns with the deployment's US elementary school context.
- **Deployment relevance:** The deployment population is US-based; US dollar problems at least partially match the cultural reference frame. Problems involving "how much more" (subtraction) and equal-sharing (division) mirror Common Core phrasing.
- **Datapoint citations:**
  - [D5] Example 3 (main, train, label=99): "They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." — US-branded consumer products, USD pricing.
  - [D20] Example 5 (main, train, label=36): "The cost of the ice cream is 10 × $4 = $<<10*4=40>>40…Caleb spent $40 − $4 = $36 more on ice cream than on frozen yogurt." — "How much more" subtraction phrasing in a USD context.

#### Strength 4: Incidental coverage of US customary length and weight units
- **Dimension(s):** IC
- **Observation:** Several problems use feet, pounds, and inches — US customary units relevant to the deployment's grades 3–6 curriculum (where unit conversion in the customary system is a CCSS-M standard). The sample includes at least cubic feet (Example 6), feet (Example 35), pounds (Examples 9, 12, 25).
- **Deployment relevance:** US customary units are a high-frequency error source in the deployment. GSM8K at least incidentally uses these units in problem contexts, which means some problems exercise the arithmetic operations that underlie unit-conversion errors, even if no problem explicitly requires a unit conversion computation.
- **Datapoint citations:**
  - [D3] Example 6 (main, train, label=54): "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" — Volume problem using US customary units (feet).
  - [D17] Example 24 (main, train, label=180): "In a northwestern town, it rained 4 inches per day during the first 15 days of November." — Inches as measurement unit in a US-located context.

#### Strength 5: Problems cover the "how many more" subtraction phrasing
- **Dimension(s):** IC, IO
- **Observation:** Multiple sampled problems use "how many more" as the operative question, which is explicitly flagged as a high-frequency Common Core phrasing that triggers student confusion between subtraction and addition. The problems correctly operationalize this as subtraction.
- **Deployment relevance:** Common Core phrasing misread ("how many more" vs. "how many total") is one of the five named error categories in the deployment's taxonomy. GSM8K's linguistic diversity does appear to include this phrasing, confirming at least partial coverage of this error trigger.
- **Datapoint citations:**
  - [D20] Example 5 (main, train, label=36): "How much more did Caleb spend on ice cream than on frozen yoghurt?" — "How much more" operationalized as subtraction.
  - [D28] Example 28 (main, train, label=40): "How many more employees drive to work than take public transportation?" with solution "80-40=<<80-40=40>>40 employees" — "How many more" correctly solved via subtraction.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: No error-type taxonomy — binary correct/incorrect label only
- **Dimension(s):** IO, OO
- **Observation:** Every sampled problem has exactly two fields: `question` (prose) and `answer` (final numeric value preceded by natural language steps). There is no label for error type, error location, misapplied operation, arithmetic slip, or any other diagnostic category. The label is entirely determined by the final number after `####`. No metadata field encodes step-level correctness.
- **Deployment relevance:** The deployment requires classifying every error into one of five categories (misapplied operation, arithmetic slip, wrong setup, incomplete chain, plus US-curriculum subtypes). GSM8K provides zero support for this. An LLM evaluated on GSM8K accuracy cannot be assessed for its ability to diagnose which *kind* of error occurred — the benchmark's entire label space is orthogonal to the deployment's output ontology.
- **Datapoint citations:**
  - [D1] Example 1 (main, train, label=32): Answer field ends "#### 32" with no error-type annotation anywhere in the record. The problem is labeled only by its correct final answer.
  - [D2] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards." — Calculator annotation encodes computational expression but carries no information about what error type a student might commit here.
  - [D22] Example 31 (main, train, label=10): "He gave away 10 cones because 50 / 5 = <<50/5=10>>10" — The problem states "every sixth customer" but the solution divides by 5; if this is an error in the dataset, it goes uncategorized; if intentional, the taxonomy for distinguishing problem-setup errors from arithmetic errors is absent.

#### Concern 2: Input distribution is professionally authored clean prose — no student-work features
- **Dimension(s):** IC, IF
- **Observation:** Every sampled problem and solution is fluent, grammatically complete English prose with no carry marks, partial products, crossing-out, abbreviations ("r" for remainder, "b/c"), informal phrasing ("I did 5 times 3"), area model notation, number bonds, or partial-quotients division. All solutions flow linearly with standard calculator annotations (`<<expr=result>>`).
- **Deployment relevance:** The deployment system must correctly parse noisy student-authored work containing precisely these features. GSM8K provides no training signal or evaluation surface for parsing unconventional student notation. An LLM that performs well on GSM8K-format clean prose has never been tested on the input distribution it will actually encounter. The 2026 DrawEduMath follow-up study (web search findings) directly confirms models misdiagnose errors specifically when student work is non-standard.
- **Datapoint citations:**
  - [D2] Example 1 (main, train): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." — Perfectly formatted prose with machine-generated calculator annotations; no student register elements.
  - [D19] Example 36 (main, train, label=1080): "First find the total number of birds eaten per day: 30 snakes * 3 birds/snake = <<30*3=90>>90 snakes" — Even where a narration label error appears ("90 snakes" instead of "90 birds"), the format is clean annotated prose, not student informal work.

#### Concern 3: Output evaluation is final-answer correctness only — no diagnostic explanation mechanism
- **Dimension(s):** OO, OF
- **Observation:** The dataset schema has two string fields: `question` and `answer`. The `answer` field contains natural language steps followed by `#### [number]`. Benchmark evaluation parses only the number after `####` and checks it against the gold answer. There is no field, rubric, or scoring mechanism for evaluating whether a generated explanation identifies the error location, names the error type correctly, or uses classroom-teacher register.
- **Deployment relevance:** The deployment requires evaluating three distinct output dimensions: (1) correct identification of the earliest error step, (2) correct error-type classification, and (3) teacher-register explanation quality. GSM8K's scoring function evaluates none of these. A model that generates "you multiplied when you needed to divide because the problem is asking how many groups" cannot be distinguished from one that generates "the answer is wrong" using GSM8K's evaluation apparatus.
- **Datapoint citations:**
  - [D1] Example 1 (main, train, label=32): The answer field "#### 32" is the entirety of what the benchmark scores; the preceding natural language steps are not evaluated for register, pedagogical clarity, or error diagnosis.
  - [D16] Example 20 (main, train, label=138): "That means the bakery would make 144 - 6 = $<<144-6=138>>138. #### 138" — Evaluation anchors entirely on 138; the quality or register of the intermediate explanation receives no score.

#### Concern 4: Ground truth generated by freelance contractors with no pedagogical expertise or grade-level differentiation
- **Dimension(s):** OC
- **Observation:** The benchmark uses final numerical answer agreement among Upwork/Surge AI contractors as its correctness criterion. No domain educators, curriculum specialists, or classroom teachers participated. No grade-level acceptability criteria are applied (e.g., whether an improper fraction is acceptable at grade 3 vs. grade 5). The estimated error rate is 1.7% with an acknowledged possibility of more subtle errors.
- **Deployment relevance:** The deployment's ground truth is defined by former elementary teachers and curriculum specialists applying grade-differentiated pedagogical standards. These annotator populations and judgment criteria are entirely different from GSM8K's. A label agreement on GSM8K does not constitute evidence that the model's diagnostic output would match teacher judgment on the same problem.
- **Datapoint citations:**
  - [D4] Example 12 (main, train, label=78): "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9 to reach a weight of 6*2=<<6+6=12>>12 pounds." — The calculator annotation `<<6+6=12>>` is inconsistent with the surrounding text `6*2`; the final answer is correct but the annotation contains a notation error that contractor review missed, confirming annotation limitations.
  - [D22] Example 31 (main, train, label=10): "He gave away 10 cones because 50 / 5 = <<50/5=10>>10" — The problem says "every sixth customer" yet the solution uses ÷5 rather than ÷6. If this is a genuine error that survived contractor review, it illustrates the quality control gap. The label is '10' regardless.

---

#### MAJOR

#### Concern 5: Substantial proportion of problems are above grades 3–6 CCSS-M scope
- **Dimension(s):** IO
- **Observation:** Among the 47 sampled `main` examples, at least 6 clearly involve content beyond grades 3–6 CCSS-M: algebraic variable introduction (Examples 23, 45), ratio/proportion problems (Example 38), percentage of large adult-scale financial quantities (Examples 30, 44, 35), and compound/simple interest over years (Example 43). Grade-band coverage is uneven; the benchmark has no grade-level metadata.
- **Deployment relevance:** The deployment targets grades 3–6. If an LLM's diagnostic capability is being evaluated using GSM8K, problems above this grade band would assess reasoning abilities not relevant to the deployment, and good performance on algebra-level problems would not indicate fitness for grade-3 arithmetic diagnosis.
- **Datapoint citations:**
  - [D8] Example 23 (main, train, label=220): "Let x represent the number of Chevys; Fords:3+2x; Buicks:4(3+2x)=12+8x; Total:x+3+2x+12+8x=301; 11x+15=301" — Formal algebraic variable introduction and linear equation, beyond grades 3–6.
  - [D10] Example 45 (main, train, label=120): "Let N be the original price each friend was going to pay. 10N=6(N+8); 10N=6N+48; 4N=48" — Algebraic equation solving, outside grades 3–6 scope.
  - [D9] Example 43 (main, train, label=720): "If she earns an interest of 10% in the first year, her savings account increases by 10/100 * $600 = $<<10/100*600=60>>60." — Simple interest computation, typically a middle school or high school topic.
  - [D27] Example 44 (main, train, label=11000): "He sold his car for 20000*.8=$<<20000*.8=16000>>16,000. He bought the new car for 30,000*.9=$<<30000*.9=27000>>27,000." — Adult financial scenario with $20,000–$30,000 values, outside elementary context.

#### Concern 6: Adult financial and professional contexts dominate, mismatching elementary student frame of reference
- **Dimension(s):** IC
- **Observation:** A sizeable fraction of the sampled problems involve adult contexts: car purchases ($20,000–$30,000 — Example 44), real estate ($98/sq ft property — Example 35), annual savings and interest calculations (Examples 13, 43), business profit (Example 20), and professional workplace scenarios (Example 46). While not technically preventing arithmetic evaluation, these contexts differ meaningfully from the school, playground, and household contexts that appear in grades 3–6 CCSS-M problem sets.
- **Deployment relevance:** The deployment serves grades 3–6 students whose problems involve familiar child-accessible contexts. GSM8K's adult-domain problems would not represent the phrasing and contextual reasoning patterns that elementary students encounter, reducing the alignment between benchmark and deployment input distributions.
- **Datapoint citations:**
  - [D28] Example 35 (main, train, label=333200): "The price is $98 per sq ft and it's 3,400 sq ft big so the property costs 98*3400 = $<<98*3400=333200.00>>333,200.00" — Real estate problem with $333,200 total; entirely outside elementary student frame.
  - [D15] Example 30 (main, train, label=7200): "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month." — Adult budget management problem.
  - [D27] Example 44 (main, train, label=11000): "James decides to replace his car. He sold his $20,000 car for 80% of its value." — Adult vehicle transaction context.

#### Concern 7: No unit conversion problems found in sample; coverage of high-frequency US curriculum error type unknown
- **Dimension(s):** IO, IC
- **Observation:** None of the 80 sampled examples involves an explicit unit conversion computation (e.g., converting inches to feet, cups to quarts, ounces to pounds). The problems use US customary units incidentally (as given quantities) but never require students to convert between units within the same measurement system — a documented CCSS-M grade 4 standard and a high-frequency error source in the deployment.
- **Deployment relevance:** Unit conversion slips (inches/feet, cups/quarts) are explicitly named as a high-frequency error type in the deployment's taxonomy. If this problem type is underrepresented or absent from GSM8K (which the sample suggests), the benchmark would fail to assess the LLM's diagnostic capability for this specific error category.
- **Datapoint citations:**
  - [D3] Example 6 (main, train, label=54): "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high" — Uses feet as given quantities but requires no conversion computation.
  - [D17] Example 24 (main, train, label=180): "it rained 4 inches per day during the first 15 days of November" — Inches used as given unit; no conversion to feet or other unit required.

#### Concern 8: Metric units appear in the sample alongside US customary, inconsistent with deployment population
- **Dimension(s):** IC
- **Observation:** At least one sampled problem uses kilograms as the primary unit (Example 9: "Four people lost a total of 103 kilograms of weight"). The deployment population operates under US customary units exclusively in grades 3–6 CCSS-M; metric units are not introduced as a standard until later grades.
- **Deployment relevance:** Problems using metric units would not represent the unit conventions of the deployment's target curriculum and could introduce confounds in evaluating unit-related reasoning.
- **Datapoint citations:**
  - [D24] Example 9 (main, train, label=28): "Four people lost a total of 103 kilograms of weight. The first person lost 27 kilograms. The second person lost 7 kilograms less than the first person." — Metric units throughout; inconsistent with grades 3–6 US customary curriculum.

---

#### MINOR

#### Concern 9: Calculator annotation format (`<<expr=result>>`) is invisible to human readers and irrelevant to deployment evaluation
- **Dimension(s):** IF
- **Observation:** All solutions embed calculator annotations in the form `<<expression=result>>` (e.g., `<<30/2=15>>`). These are present in every sampled answer. They serve GSM8K's evaluation mechanism (Python `eval` override) but have no counterpart in student-submitted work or in the deployment's evaluation.
- **Deployment relevance:** Minor formatting noise for any system that processes GSM8K answers; a system trained on or evaluated with GSM8K solutions would need to strip these annotations to avoid learning the annotation format as a feature. Not a fundamental validity concern, but worth noting.
- **Datapoint citations:**
  - [D2] Example 1 (main, train): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards." — Calculator annotation present in every solution line.

#### Concern 10: Annotation inconsistency confirmed in sample (expression label mismatch)
- **Dimension(s):** OC
- **Observation:** Example 12 contains `6*2=<<6+6=12>>12`, where the left side of the annotation uses multiplication (`6*2`) but the expression inside the annotation uses addition (`6+6`). Both yield 12, so the final answer is unaffected, but the annotation itself is internally inconsistent. The paper acknowledges that calculator annotation logic is imperfect [Q117, Q118].
- **Deployment relevance:** Minor issue that does not affect the final-answer label but confirms the paper's caveat about annotation quality. For a deployment that examines intermediate steps, inconsistent intermediate annotations would be problematic; for GSM8K's binary evaluation, it is a minor defect.
- **Datapoint citations:**
  - [D4] Example 12 (main, train, label=78): "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9 to reach a weight of 6*2=<<6+6=12>>12 pounds." — Multiplication stated in prose but addition used inside the calculator annotation.

#### Concern 11: Potential logic/arithmetic error in one sampled problem (every-sixth-customer)
- **Dimension(s):** OC
- **Observation:** Example 31 states "every sixth customer gets a free ice cream cone" but the solution divides paying customers by 5 (not 6) to reach the giveaway count: "He sold 50 cones because 100 / 2 = 50; He gave away 10 cones because 50 / 5 = 10." If the problem means 1 in every 6 customers (1 free + 5 paid), dividing by 5 may be intentional; if "every sixth" means one out of every six total customers, the answer should be ≈8. The ambiguity is unresolved and the solution is internally inconsistent with the stated problem.
- **Deployment relevance:** The paper estimates ~1.7% of problems contain breaking errors or ambiguities [Q107, Q108]. This example illustrates that such errors are real and present in the sample. For a deployment that requires reliable ground truth, problem ambiguities of this kind undermine the trustworthiness of the benchmark as a reference.
- **Datapoint citations:**
  - [D22] Example 31 (main, train, label=10): "Dan owns an ice cream shop and every sixth customer gets a free ice cream cone. Cones cost $2 each. If he sold $100 worth of cones, how many free ones did he give away? … He gave away 10 cones because 50 / 5 = <<50/5=10>>10" — "Sixth customer" but ÷5 in solution.

---

### Content Coverage Summary

The 80 sampled examples are uniformly English-prose arithmetic word problems requiring 2–6 sequential operations. The register is professional and fluent throughout — no informal, abbreviated, or student-register language appears anywhere. Problems span a wide range of contexts: childhood activities (candy, toys, pets — Examples 1, 2, 3, 25, 27), sports (Examples 15, 18, 26), adult financial transactions (rent, real estate, car sales — Examples 30, 35, 44), and abstract quantity reasoning (Examples 7, 9, 38). Currency is overwhelmingly USD. Units include feet, pounds, inches (US customary), and one instance of kilograms (metric). The mathematical content ranges from grade-3-appropriate two-step problems (Examples 2, 8, 21, 27) up to algebraic equation solving and simple interest that are outside the grades 3–6 band (Examples 23, 43, 45). No problem requires a unit conversion computation. No solution exhibits informal notation, carry marks, area models, remainder notation, or any student-register feature. Solutions are clean annotated natural language prose with `<<expr=result>>` annotations. The `socratic` config provides the same content with sub-question scaffolding.

---

### Limitations

1. **Sample size.** 80 examples drawn from 7,473 train examples (~1.1%) are insufficient to quantify the frequency of any specific problem type (e.g., unit conversion problems, specific grade-level topics). Absence of a problem type in the sample does not establish its absence in the full dataset.

2. **No test-split sampling.** All examples come from the training split. The test split (1,319 examples) may have different topic or difficulty distributions; the benchmark documentation provides no breakdown by sub-type.

3. **No grade-level metadata.** Without grade-level labels in the data, it is impossible to measure from the sample what fraction of problems falls within grades 3–6 CCSS-M scope. The above-grade-band examples were identified by content inspection, not by a data field.

4. **Common Core phrasing frequency unquantifiable from sample.** Whether "how many more," "how many total," or other flagged CCSS-M phrasings appear at representative rates in the full dataset cannot be determined from 80 examples.

5. **No error-type annotation to inspect.** Because GSM8K contains no error-type labels, it is impossible to evaluate coverage of the deployment's diagnostic taxonomy from the data itself — this gap is structural and cannot be assessed by inspecting more examples.

6. **Calculator annotation correctness not systematically verified.** Only one annotation inconsistency was identified by inspection (D4); a systematic audit of all 8,500 problems' calculator annotations would be needed to quantify the annotation error rate beyond the paper's 1.7% estimate.

