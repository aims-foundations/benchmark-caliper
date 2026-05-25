## Deployment Context

We are building a homework-checking feature for a US K-8 math tutoring platform. Students type in or receive arithmetic word problems through the platform's text interface, and our LLM checks whether their final numerical answer is correct. We want to evaluate the LLM's ability to solve multi-step arithmetic word problems (addition, subtraction, multiplication, division, fractions, percentages) before deploying this feature to American elementary and middle school students.

# Validity Analysis: gsm8k
**Target context:** US K-8 Math Tutoring Platform — Homework Checker Deployment
**Overall risk:** MEDIUM

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 3 | Moderate gaps | high |
| Input Content ⚠ | 4 | Minor gaps | high |
| Input Form ✓ | 5 | Strong alignment | high |
| Output Ontology ✓ | 5 | Strong alignment | high |
| Output Content | 4 | Minor gaps | high |
| Output Form ✓ | 5 | Strong alignment | high |
| **Average** | **4.3** | | |

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

GSM8K is well-suited as a screening-tier benchmark for the platform's core use case — multi-step arithmetic word problem checking for grades 3-6 students using US conventions — but has confirmed coverage gaps for several content types the platform serves regularly. The strongest alignment is on output structure (binary final-answer checking is structurally identical), input form (text-only English), and cultural framing (USD currency and American settings dominate empirically). The weakest alignment is in input ontology: US customary unit conversion problems were not observed in 80 sampled examples and are not documented in the paper; basic statistics (mean/median) is confirmed absent by multiple web sources and the sample; area/perimeter problems are confirmed absent (volume and area-as-pricing present but no perimeter); K-2 single-step arithmetic is excluded by the 2-step minimum design floor. These four gaps mean that strong GSM8K performance does not guarantee competence on roughly the lower-grade (K-2) and upper-grade-supplementary (statistics, perimeter, conversion) portions of the platform's content inventory. Additionally, benchmark saturation at ~95%+ for frontier models [WEB-4] further limits discrimination at the top end. For the platform's dominant grade 3-6 multi-step four-operations use case, GSM8K provides solid evaluation evidence; for the documented gap areas, supplementary evaluation is required.

## Practical Guidance

### What This Benchmark Measures

GSM8K validly measures an LLM's ability to read American English arithmetic word problems and produce correct final numerical answers via multi-step reasoning involving the four operations, fractions, decimals, percentages, ratios, and rates — the platform's highest-volume grade 3-6 content (input_ontology, input_content, output_ontology, output_form all score 3-5). It also confirms baseline cultural framing (USD, US customary units, American settings) appropriate for the target population.

### Construct Depth

Depth is high for multi-step four-operations arithmetic but shallow or absent for several CCSS-M content types the platform requires: US customary unit conversion (in↔ft, oz↔lb, cups↔gallons), basic statistics (mean/median from datasets), perimeter geometry, and K-2 single-step arithmetic. The benchmark provides strong signal on the platform's dominant use case (~60-70% of platform volume by elicited grade band) but limited signal on the remaining sub-domains. Saturation at ~95%+ further reduces discrimination among frontier models [WEB-4].

### What Else You Need

(1) A CCSS-M-aligned measurement conversion test set to fill the input_ontology gap on US customary unit conversion. (2) A grades 6-8 statistics word problem set (mean/median/mode/range from small datasets) — fully absent per [WEB-5, WEB-7] and sample. (3) A perimeter-focused geometry word problem set to complement GSM8K's area/volume coverage. (4) A K-2 single-step arithmetic test set, as GSM8K's 2-step minimum excludes this band by design. (5) An ambiguity audit on the deployment-relevant subset to mitigate the documented 1.7% label-error rate impact on user-facing scoring.

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
GSM8K's core taxonomy — multi-step arithmetic word problems using the four operations with fractions, percentages, and ratios — directly matches the platform's highest-volume grade 3-6 use case [Q1, Q11, Q19] and is empirically confirmed across the dataset sample (DATASET-D13, D17, D18, D21, D24). However, three platform-relevant categories are documented as absent or sparse: (a) US customary unit conversion problems are not documented in the paper and no conversion problem appeared in 80 sampled examples (DATASET-D31, D32 show only time/rate conversions, not in↔ft or oz↔lb); (b) basic statistics (mean/median from datasets) is confirmed absent in web research [WEB-5, WEB-7] and only a single embedded mean problem appeared in the sample (DATASET-D10); (c) area/perimeter geometry is confirmed absent per [WEB-5, WEB-7], with the sample showing volume and area-as-pricing (DATASET-D11, D12) but no perimeter problems. Additionally, the benchmark's 2–8 step difficulty floor [WEB-5, WEB-6] excludes true K-2 single-step arithmetic by design, leaving the platform's K-2 cohort untested. The benchmark also includes some algebra-required problems (DATASET-D16, D22) that exceed the platform's K-6 arithmetic scope, introducing minor construct-irrelevant variance. Given MODERATE priority and confirmed gaps on 3 of the user's explicitly flagged content types, partial alignment is the most defensible score.

**Strengths:**
- Core multi-step four-operations arithmetic at grades 3-6 difficulty is well represented (DATASET-D13, D24; Q19)
- Fractions and percentages are present and match grades 4-6 content (DATASET-D17, D18, D21, D26)
- Ratio and proportional reasoning problems cover grades 6-8 content (DATASET-D14, D15)
- High linguistic diversity in problem framing reduces template-overfitting risk [Q9, Q10, Q113]

**Checklist:**

- **IO-1**: Required categories per elicitation: multi-step four-operations arithmetic (grades 3-6), fractions/decimals/percentages/ratios (grades 4-8), US customary unit conversion, basic statistics (mean/median), area/perimeter word problems, and K-2 single-step arithmetic. — _Sources: Q1, Q11_
- **IO-2**: Yes. Three categories are omitted or sparsely represented: (a) US customary unit conversion — not documented in paper; absent from 80-example sample (DATASET-D31, D32 only show time conversions); (b) basic statistics (mean/median) — confirmed absent per [WEB-5, WEB-7]; only one embedded mean problem in sample (DATASET-D10); (c) area/perimeter — confirmed absent per [WEB-5, WEB-7]; sample shows volume/area-as-pricing only (DATASET-D11, D12), no perimeter. Additionally, K-2 single-step arithmetic is excluded by the 2-step minimum design floor [WEB-5, WEB-6]. — _Sources: WEB-5, WEB-7, WEB-6, DATASET-D10, DATASET-D11, DATASET-D12, DATASET-D31, DATASET-D32_
- **IO-3**: Minor inclusion of algebra-required variable-equation problems (DATASET-D16, D22) that exceed the platform's stated K-8 arithmetic scope. Low-frequency but introduces some construct-irrelevant variance. — _Sources: DATASET-D16, DATASET-D22_
- **IO-4**: Documented gaps that harm content validity: K-2 single-step problems (full gap, by design [WEB-5, WEB-6]); statistics word problems (full gap [WEB-5, WEB-7]); perimeter problems (full gap [WEB-5, WEB-7]); US customary unit conversion (likely partial gap, unconfirmed at full-dataset scale). Strong coverage on core multi-step four-operations and fractions/percentages/ratios. — _Sources: WEB-5, WEB-6, WEB-7, Q48_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems.' (p.1)
- [Q11] 'GSM8K solutions depend only on elementary concepts, so achieving high test performance is a tractable goal.' (p.2)
- [Q19] 'GSM8K is larger, provides natural language solutions, and consists of problems that on average require more steps to solve.' (p.4)
- [Q48] 'a model with 10^16 parameters would be required to reach an 80% solve rate' (p.6)

*Web sources:*
- [WEB-5] GSM8K content scope: 'percentages, fractions, ratios, work rates, and basic measurement conversions' with no geometry or statistics
- [WEB-7] 'no advanced mathematics (no geometry, quadratics, combinatorics)'; no statistics mentioned
- [WEB-6] Solutions 'primarily involve performing a sequence of elementary calculations using basic arithmetic operations'
- [WEB-5] Difficulty segmentation: 2-8 steps with approximately equal thirds easy/medium/hard; minimum 2-step floor excludes K-2 single-step

*Dataset analysis:*
- DATASET-D13: 4-step multi-operation problem confirms grades 3-6 core coverage
- DATASET-D10: only one mean/average problem in 80 examples; no median observed — confirms statistics gap
- DATASET-D11, D12: volume and area-as-pricing present but no perimeter problems observed
- DATASET-D31, D32: time conversions present but no US customary unit-to-unit conversions (in↔ft, oz↔lb)
- DATASET-D16, D22: algebra-required variable problems exceed stated K-8 arithmetic scope

</details>

**Information gaps:**
- Frequency of US customary unit conversion problems in the full 8,500-problem corpus (sample of 80 found none, but small sample limits inference)
- Whether any median/range/mode problems exist anywhere in the full dataset
- Whether GSM8K problems have any incidental alignment to specific CCSS-M grade-level standards

**Requires expert verification:**
- Full-dataset frequency audit of measurement conversion, statistics, and geometry sub-skills via keyword/semantic search
- Mapping of GSM8K items to CCSS-M grade bands by a curriculum specialist

---

### Input Content — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Empirical sampling provides strong evidence that GSM8K's content predominantly matches the platform's US cultural context. Currency is consistently USD with decimal cents across the sample (DATASET-D1, D2, D3, D28, D29), including American-specific features like sales tax (DATASET-D3) and brand-name US candy (DATASET-D1). US customary units (feet, pounds, square feet) appear regularly (DATASET-D5, D6, D7, D12). American cultural settings dominate — football, malls, farmer's markets (DATASET-D4, D28). [WEB-5] confirms 'the standard version is US-centric, using names, currencies, and scenarios typical of Western grade-school curricula.' However, three concerns persist: (a) the paper does not document contractor nationality [Q103, Q104] and the YAML notes a 'transferred from different cultural context' metadata flag (GAP-4); (b) at least one observed problem uses kilograms exclusively (DATASET-D8), conflicting with the platform's US-customary-primary requirement; (c) occasional non-US names and settings appear (DATASET-D14 'castle provisions'; DATASET-D27 British names; DATASET-D15 Scandinavian names). Given MODERATE priority and that the dominant evidence supports US alignment with only minor inconsistencies, score 4 is appropriate.

**Strengths:**
- USD currency with decimal cents consistent throughout the sample (DATASET-D1, D2, D3, D28)
- American retail and cultural settings dominate (mall, farmer's market, US football, brand-name candy) (DATASET-D1, D4, D28)
- US customary units (feet, pounds, square feet) used in measurement problems (DATASET-D5, D6, D7, D12)
- [WEB-5] independently confirms US-centric framing as the standard convention

**Checklist:**

- **IC-1**: Yes — problems contain American cultural references (US football scoring, brand-name candy, mall/farmer's market settings) that benefit from US student familiarity (DATASET-D1, D4, D28). These are deployment-aligned rather than misaligned. — _Sources: DATASET-D1, DATASET-D4, DATASET-D28_
- **IC-2**: Yes, predominantly. [WEB-5] confirms US-centric framing; empirical sample shows USD throughout (DATASET-D1-D3, D28-D29) and US customary units (DATASET-D5-D7, D12). Minor inconsistencies: one kilogram problem (DATASET-D8) and occasional non-US names (DATASET-D27, D15). — _Sources: WEB-5, DATASET-D1, DATASET-D2, DATASET-D3, DATASET-D5, DATASET-D8, DATASET-D27_
- **IC-3**: No problematic Western-specific knowledge for a US deployment — Western framing IS the target context. Minor non-US-flavored items (castle setting DATASET-D14, British names DATASET-D27) may slightly reduce cultural familiarity but do not impede arithmetic skill assessment. — _Sources: DATASET-D14, DATASET-D27_
- **IC-4**: INSUFFICIENT DOCUMENTATION — contractor demographics not disclosed in the paper [Q103, Q104]; no published audit of US-conventions enforcement across the full 8,500 problems. Would require systematic regional annotator review. — _Sources: Q103, Q104_
- **IC-5**: Minor content issues: ~5-10% of sampled problems show non-US-flavored framing (kilograms, non-US names, non-American settings). The cumulative impact on construct validity is low given that arithmetic skill is unit-agnostic, but reduces 'culturally familiar American settings' fidelity claim modestly. — _Sources: DATASET-D8, DATASET-D15, DATASET-D27_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q7] 'Karl Cobbe... OpenAI' — US-based authoring organization (p.1)
- [Q103] 'we initially collected a starting set of a thousand problems and natural language solutions by hiring freelance contractors on Upwork' (p.15)
- [Q104] 'We then worked with Surge AI, an NLP data labeling platform, to scale up our data collection.' (p.15)
- [Q110] 'we provided seed questions automatically generated from a few-shot prompted 175B GPT-3 model' (p.15)

*Web sources:*
- [WEB-5] 'the standard version is US-centric, using names, currencies, and scenarios typical of Western grade-school curricula'
- [WEB-5] Recent cultural adaptation work (Tomar et al. 2025) created non-US variants, confirming original is implicitly US/Western-anchored

*Dataset analysis:*
- DATASET-D1: USD pricing with US brand-name candy (Reese's, Snickers, Skittles) at birthday party
- DATASET-D3: USD with sales tax — characteristic American retail
- DATASET-D4: American football scoring (touchdowns, 2-point conversions)
- DATASET-D5, D6, D7, D12: US customary units (feet, pounds, sq ft) used consistently
- DATASET-D8: kilograms used exclusively — inconsistent with platform's US-customary requirement
- DATASET-D27: British names (Colin, Helen, Benedict) suggest possible non-US authorship
- DATASET-D14: castle/provisions setting — not characteristically American
- DATASET-D15: Scandinavian names, no currency denomination specified

</details>

**Information gaps:**
- Full-dataset frequency of non-US-flavored problems (sample suggests ~5-10% but n=80 too small for precision)
- Whether kilogram or other metric-only problems appear in problem types not sampled
- Contractor nationality and Common Core familiarity

**Requires expert verification:**
- Systematic audit by US elementary curriculum specialist of cultural setting and unit-system consistency across the full 8,500-problem corpus
- Confirmation that no benchmark problems use non-USD currency

---

### Input Form — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
Full alignment on input form. Both benchmark and deployment are text-only English prose word problems [Q9, Q32], using the Latin alphabet, with no audio, image, or structured-data modality. The empirical sample confirms every problem is plain prose in American English. The platform's input channel (text string submitted via API) matches the benchmark format exactly. No infrastructure constraints, signal distribution differences, or script mismatches exist. This dimension was correctly marked LOWER priority in elicitation.

**Strengths:**
- Text-only English prose matches deployment input channel exactly (Q9, Q32)
- Latin alphabet, US English register match platform requirements
- No modality conversion or preprocessing needed
- Calculator annotations are training-only and transparent to evaluation [Q117, Q119]

**Checklist:**

- **IF-1**: Both source and target are plain English text strings [Q9, Q32]. No signal-distribution differences. — _Sources: Q9, Q32_
- **IF-2**: Yes — text-based web/mobile API channel requires no specialized infrastructure beyond standard internet access, which the deployment assumes. — _Sources: Q9_
- **IF-3**: No domain-specific form differences. The platform requires text-in/binary-out; the benchmark provides text-in with a clearly delimited final numerical answer. — _Sources: Q32, DATASET-D13_
- **IF-4**: No form mismatches identified.

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q9] 'We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts.' (p.2)
- [Q32] 'we focus attention on the space of natural language solutions, as this is a richer and more general solution format than pure mathematical expressions.' (p.5)
- [Q56] 'it is important to allow the model to generate the full natural language solution before outputting a final answer' (p.7)

*Dataset analysis:*
- DATASET-D13, D21, D22: all sampled problems are plain English prose with no embedded media or structured data

</details>

---

### Output Ontology — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
GSM8K's output ontology — binary correct/incorrect judgment determined solely by whether the final numerical answer matches ground truth [Q31, Q60] — maps directly onto the deployment's stated requirement of 'binary correct/incorrect judgment on submitted final numerical answer only.' The decision rule is objective and culturally invariant: numerical equality. No categorical labels with cultural value-dependence are involved [Q60]. The elicitation explicitly confirms 'an unconventional solution method that yields the correct number is scored as correct,' which matches the benchmark's final-answer-only scoring [Q60, Q87]. No taxonomy redesign needed.

**Strengths:**
- Binary correct/incorrect decision rule is structurally identical to deployment requirement [Q31, Q60]
- Decision boundary is objective numerical equality — culturally invariant
- Sample confirms clean '#### N' final-answer delimiter format (DATASET-D13, D21, D22)
- No partial-credit or step-scoring assumptions that would need to be stripped out

**Checklist:**

- **OO-1**: Single binary label (correct/incorrect on final numerical answer) directly matches platform requirement [Q31, Q60]. — _Sources: Q31, Q60_
- **OO-2**: No missing regional categories — the output space is a number, not a label set requiring regional taxonomy. — _Sources: Q60_
- **OO-3**: No culturally encoded categories — numerical equality is the sole decision rule [Q60]. — _Sources: Q60_
- **OO-4**: No taxonomy redesign needed; benchmark structure already matches deployment. — _Sources: Q60_
- **OO-5**: No taxonomy issues identified. — _Sources: Q31, DATASET-D13_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'Verifiers are trained to judge the correctness of solutions, with the training signal determined solely by whether or not the solution reached the correct final answer.' (p.5)
- [Q60] 'Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer.' (p.7)
- [Q87] 'This voting process considers only the final answer reached by the individual solutions' (p.11)

*Dataset analysis:*
- DATASET-D13, D21, D22: '#### N' delimiter cleanly isolates the final numerical answer for binary matching

</details>

---

### Output Content — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Ground-truth labels are numerical answers verified by contractor re-solving with a documented 1.7% disagreement rate [Q107, Q108], which the authors acknowledge may understate the true subtle-error rate [Q109]. Because correctness is arithmetically verifiable, regional stakeholder disagreement is structurally minimal — a correct sum is correct regardless of cultural perspective. The dataset sample confirms label cleanliness in most cases (DATASET-D13, D21, D22), but DATASET-D23 illustrates the documented error pattern: 'every sixth customer' in the problem text, while the solution divides by 5 to reach label=10, an ambiguity that could cause a correctly-reasoning model to be marked wrong. This is consistent with the paper's documented 1.7% rate. The calculator annotation imperfection [Q118, Q123] is acknowledged but affects training/evaluation infrastructure rather than ground-truth labels. Contractor nationality remains undocumented [Q105], but for a numerical-equality decision rule, this matters less than for subjective tasks. Score 4 reflects strong label quality with documented minor error rate and no cultural-disagreement risk.

**Strengths:**
- Labels are arithmetically verifiable; correctness is objective [Q60]
- Two-pass contractor re-solving validation with documented agreement rate [Q105, Q106, Q107]
- Sample confirms clean numerical labels in most examples (DATASET-D13, D21, D22)
- 1.7% disagreement rate is low enough for a screening-tier benchmark [Q107]

**Checklist:**

- **OC-1**: Ground-truth labels are numerical and arithmetically verifiable, so regional stakeholder agreement is essentially structural rather than perspectival. — _Sources: Q60, Q108_
- **OC-2**: Minimal potential disagreement — US Common Core teachers would converge on the same numerical answers as the original annotators for well-formed problems. Disagreement risk is concentrated in the ~1.7% of problems with breaking errors or ambiguities [Q107, Q108]. — _Sources: Q107, Q108, DATASET-D23_
- **OC-3**: INSUFFICIENT DOCUMENTATION — contractor demographics (nationality, native language, CCSS-M familiarity) not disclosed [Q103, Q104, Q105]. For a numerical-equality task this is lower-stakes than for subjective labeling. — _Sources: Q103, Q104, Q105_
- **OC-4**: Re-annotation by US K-8 teachers would likely affect <2% of items; not necessary for the deployment but useful for high-stakes use. — _Sources: Q109_
- **OC-5**: No aggregation method that could erase minority perspectives — labels are single numerical values, not aggregated judgments. — _Sources: Q60_
- **OC-6**: Documented 1.7% disagreement rate [Q107] and acknowledged 'larger percentage may contain subtle errors' [Q109]; one such ambiguity observed empirically (DATASET-D23). Acceptable for screening-tier evaluation; users should be aware that 1-2% of failures may reflect label issues rather than model errors. — _Sources: Q107, Q109, DATASET-D23_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q105] 'After collecting the full dataset, we asked workers to re-solve all problems, with no workers re-solving problems they originally wrote.' (p.15)
- [Q107] '1.7% of problems still produce disagreements among contractors.' (p.15)
- [Q108] 'We estimate this to be the fraction of problems that contain breaking errors or ambiguities.' (p.15)
- [Q109] 'It is possible that a larger percentage of problems contain subtle errors.' (p.15)
- [Q123] 'the original version of our calculator, used for all results in this paper, had some minor implementation bugs.' (p.17)

*Dataset analysis:*
- DATASET-D23: 'every sixth customer' but solution divides by 5 — illustrates documented ambiguity pattern
- DATASET-D13, D21, D22: clean numerical labels in typical cases

</details>

**Information gaps:**
- True subtle-error rate beyond the documented 1.7% breaking-error rate
- Contractor demographics and CCSS-M familiarity

**Requires expert verification:**
- Targeted re-annotation of a sample by US elementary teachers to estimate CCSS-M-aligned label disagreement rate

---

### Output Form — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
Full alignment. GSM8K's output form is a final numerical answer string evaluated via exact-match correctness [Q29, Q46], which maps directly onto the deployment's stated output_channel ('binary correct/incorrect label returned to platform UI') and answer_format ('single numerical value — integer, decimal, or fraction'). The dataset sample confirms clean '#### N' final-answer delimiters across all examined examples (DATASET-D13, D21, D22). No text-to-speech, multi-modal output, or accessibility transformations are needed. Literacy is presumed in the target K-8 student population reading word problems in English. No format mismatch exists.

**Strengths:**
- Final numerical answer with exact-match scoring matches deployment output schema exactly [Q29, Q46]
- Clean '#### N' delimiter format across the sample (DATASET-D13, D21, D22)
- No partial-credit or step-scoring that would need to be discarded
- Text output channel matches platform UI requirement

**Checklist:**

- **OF-1**: Text-based numerical output matches platform UI requirement (binary label returned via API). — _Sources: Q29, Q46, DATASET-D13_
- **OF-2**: Not applicable — deployment is text-based, not speech-based.
- **OF-3**: Target population (K-8 students using English-language platform) is assumed literate in US English; no accessibility transformation needed for benchmark evaluation purposes.
- **OF-4**: No form mismatches identified.

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q29] 'we judge performance by autoregressively sampling a single low temperature solution and checking whether the final answer is correct.' (p.5)
- [Q46] 'Test performance is determined by a single low temperature (T = 0) sample for each test problem.' (p.6)

*Dataset analysis:*
- DATASET-D13, D21, D22: '#### N' delimiter cleanly maps to binary final-answer comparison

</details>

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** US customary unit conversion problems (feet↔inches, cups↔gallons, pounds↔ounces) not observed in 80-example sample and not documented in the paper; CCSS-M-mandated for grades 4-5+

**Recommendation:** Construct a 100-200 problem supplementary test set of US customary unit conversion word problems aligned to CCSS-M grades 4-5 measurement standards. Evaluate the LLM on this set alongside GSM8K.

### Input Ontology ⚠

**Gap:** Basic statistics word problems (mean, median, mode, range from small datasets) are confirmed absent from GSM8K's documented content scope [WEB-5, WEB-7]; only one embedded mean problem in 80-example sample

**Recommendation:** Add a grades 6-8 statistics word problem evaluation set covering mean/median/mode/range from named small datasets to fill this full coverage gap before deploying for upper-grade students.

### Input Ontology ⚠

**Gap:** Perimeter word problems absent from sample; geometry confirmed not in GSM8K scope [WEB-5, WEB-7]

**Recommendation:** Supplement with a perimeter-focused word problem set for rectangles, composite shapes, and real-world contexts. GSM8K's volume/area-as-pricing problems do not substitute for perimeter reasoning.

### Input Ontology ⚠

**Gap:** K-2 single-step arithmetic is excluded by GSM8K's 2-step minimum design floor [WEB-5, WEB-6]; deployment serves K-2 students

**Recommendation:** Evaluate K-2 capability with a single-step single-operation word problem set if the platform applies the homework-checker to early-grade student submissions. GSM8K provides zero test coverage for this band.

### Input Content ⚠

**Gap:** Occasional non-US-flavored problems (kilograms only, non-US names, non-American settings) in roughly 5-10% of sample (DATASET-D8, D14, D15, D27); contractor nationality undocumented

**Recommendation:** Filter or flag benchmark items using metric-only units or non-US settings if strict US-context fidelity is required for reporting. Consider using one of the published cultural adaptations or running an automated keyword/unit filter.

### Output Content

**Gap:** Documented 1.7% label-disagreement rate [Q107] and acknowledged subtle-error possibility [Q109]; one ambiguity observed empirically (DATASET-D23)

**Recommendation:** Have US K-8 math teachers re-validate a sample of GSM8K items used in user-facing accuracy reporting, or restrict reported metrics to a curated subset where label quality has been re-confirmed.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems." |
| Q2 | 1 | output_ontology | "To increase performance, we propose training verifiers to judge the correctness of model completions." |
| Q3 | 1 | output_form | "At test time, we generate many candidate solutions and select the one ranked highest by the verifier." |
| Q4 | 1 | output_form | "We demonstrate that verification significantly improves performance on GSM8K, and we provide strong empirical evidence that verification scales more effectively with increased data than a finetuning baseline." |
| Q5 | 1 | input_ontology | "One significant challenge in mathematical reasoning is the high sensitivity to individual mistakes (Shen et al., 2021a)." |
| Q6 | 1 | input_ontology | "When generating a solution, autoregressive models have no mechanism to correct their own errors." |
| Q7 | 1 | input_content | "Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, John Schulman, OpenAI" |
| Q8 | 2 | input_content | "We are releasing GSM8K, a dataset of 8.5K high quality problems at the grade school math level." |
| Q9 | 2 | input_form | "We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts." |
| Q10 | 2 | input_ontology | "State-of-the-art language models struggle to achieve high performance on this dataset, primarily due to the high diversity among problems." |
| Q11 | 2 | input_ontology | "At the same time, GSM8K solutions depend only on elementary concepts, so achieving high test performance is a tractable goal." |
| Q12 | 2 | input_content | "We present a curated dataset of 8.5K grade school math questions and natural language solutions, useful for probing the informal reasoning ability of large language models." |
| Q13 | 2 | output_form | "We show that, compared to a finetuning baseline, the use of verifiers results in approximately the same performance boost as a 30x model size increase, and that verifiers scale significantly better with increased data." |
| Q14 | 2 | output_form | "We show that dropout acts as a strong regularizer, significantly improving performance for both finetuning and verification." |
| Q15 | 3 | input_content | "Early math word problem datasets (Kushman et al., 2014; Roy and Roth, 2015) are relatively small and are not well suited for testing the limits of modern language models." |
| Q16 | 3 | input_content | "Dolphin18K (Huang et al., 2016) is a larger dataset containing" |
| Q17 | 4 | input_content | "The recently developed ASDiv dataset (Miao et al., 2021), which contains 2.3K math word problems, addresses common flaws in prior datasets by ensuring problems have both high diversity and high quality." |
| Q18 | 4 | input_content | "We share those design principles in the creation of GSM8K." |
| Q19 | 4 | input_ontology | "However, we note that GSM8K is larger, provides natural language solutions, and consists of problems that on average require more steps to solve." |
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
| Q34 | 5 | output_ontology | "Finally, we use separate generator and verifier networks, in order to prevent the generator from overfitting." |
| Q35 | 6 | input_form | "For both methods, we use models from the GPT-3 family as our initialization, primarily focusing on the 175B and 6B model sizes." |
| Q36 | 6 | input_ontology | "The 175B model is the largest and produces the most impressive results, while the 6B model is significantly more convenient for research purposes." |
| Q37 | 6 | input_form | "We discuss hyperparameter choices in Appendix B." |
| Q38 | 6 | output_content | "Our models frequently fail to accurately perform calculations." |
| Q39 | 6 | output_content | "Although larger models make fewer arithmetic mistakes than smaller models, this remains a common source of errors." |
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
| Q57 | 7 | output_form | "If we instead finetune a 6B model to directly output the final answer without any intermediate steps, performance drops drastically from 20.6% to 5.2%." |
| Q58 | 7 | output_ontology | "To improve upon the finetuning baseline, we train verifiers to judge the correctness of model-generated solutions and search against these verifiers at test time." |
| Q59 | 7 | output_ontology | "Conditioned on the problem and a candidate solution, the verifier outputs the probability that the solution is correct." |
| Q60 | 7 | output_ontology | "Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer." |
| Q61 | 7 | output_content | "In practice, some solutions will reach the correct final answer using flawed reasoning, leading to false positives." |
| Q62 | 8 | input_form | "As shown in Figure 4, we train the verifier as follows: 1. Finetune a model (the "generator") for 2 epochs on the training set. 2. Sample 100 completions from the generator for each training problem and label each solution as correct or incorrect. 3. Train a verifier for a single epoch on this dataset." |
| Q63 | 8 | input_ontology | "Training for 2 epochs is enough for the generator to learn basic skills in this domain." |
| Q64 | 8 | input_content | "We choose not to train for longer, since the diversity of generated solutions begins to collapse after this point, as shown in Figure 3." |
| Q65 | 8 | input_form | "We train separate generator and verifier models to limit the generator's training and prevent overfitting, but in principle, it should be possible to combine these models." |
| Q66 | 8 | input_form | "Unless otherwise specified, we use the same model size for the generator and the verifier." |
| Q67 | 8 | output_ontology | "In addition to predicting solution correctness, we also train the verifier with the same language modeling objective as the generator." |
| Q68 | 8 | output_form | "At test time, we sample 100 completions to each test problem, rank them with the verifier, and then return the one with the highest verifier score." |
| Q69 | 8 | output_form | "We find that it is not beneficial to use verification at low dataset sizes." |
| Q70 | 8 | output_content | "We believe this is due to the pressure to overfit to the correct answer: with small datasets, overfitting to the correct answer happens faster than learning more generalizable properties of correct reasoning." |
| Q71 | 8 | output_form | "However, once we use a sufficiently large dataset, we see a strong boost from verifiers." |
| Q72 | 9 | output_ontology | "We can either train verifiers to make a single scalar prediction conditioned on the entire generated solution, or to make a scalar prediction after each token in the solution." |
| Q73 | 9 | output_ontology | "By default, we choose the latter, training verifiers to make predictions after each token." |
| Q74 | 9 | output_ontology | "This can be viewed as a token-level value function." |
| Q75 | 9 | output_ontology | "Predicting the value function at every token is a more challenging and noisier task than judging only the full completion." |
| Q76 | 9 | output_form | "However, despite the initially slower training, the token-level verifier ultimately outperforms the solution-level verifier." |
| Q77 | 9 | output_content | "Moreover, the token-level verifier is still improving late in training, whereas the solution-level verifier quickly shows signs of overfitting." |
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
| Q89 | 11 | input_ontology | "We find that both finetuning and verification strongly benefit from the use of dropout as a regularizer." |
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
| Q112 | 15 | input_content | "We instructed contractors to be as descriptive as possible in their solutions, and to not re-use problem settings or templates between different questions." |
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
| Q123 | 17 | output_content | "We note that the original version of our calculator, used for all results in this paper, had some minor implementation bugs." |
| Q124 | 17 | output_content | "Our reported test performance is therefore a slight underestimate, though the magnitude of this discrepancy is less than 1% in most experiments." |
| Q125 | 17 | output_content | "Fixing the calculator improves verification test performance by about 1% when using the full GSM8K training set." |
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
| Q138 | 20 | output_ontology | "Architecturally, this means our verifiers are language models, with a small scalar head that outputs predictions on a per-token basis." |
| Q139 | 20 | output_ontology | "We implement this scalar head as a single bias parameter and single gain parameter that operate on the logits outputted by the language model's final unembedding layer." |
| Q140 | 20 | input_form | "We can choose to initialize the verifier from the same pretrained language model the generator was finetuned from, or from the generator itself." |
| Q141 | 20 | output_form | "In our ablations the latter performed slightly better; we suspect this is because better understanding the language distribution that the generator learned should only aid the verifier in scoring samples from that distribution." |
| Q142 | 20 | input_form | "Unless otherwise explicitly stated, we initialize our verifiers from their corresponding generators in all experiments." |
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
| WEB-4 | https://arxiv.org/pdf/2509.25160 |
| WEB-5 | https://www.emergentmind.com/topics/gsm8k-dataset-95a37205-4213-4591-900f-09ce82d0a123 |
| WEB-6 | https://huggingface.co/datasets/openai/gsm8k |
| WEB-7 | https://mbrenndoerfer.com/writing/gsm8k-evaluating-mathematical-reasoning-language-models |
| WEB-8 | https://www.mcdermottlaw.com/insights/edtech-and-privacy-navigating-a-shifting-regulatory-landscape/ |
| WEB-9 | https://studentdpa.com/blog/understanding-ferpa-coppa-state-privacy-laws-03202025 |
| WEB-10 | https://publicinterestprivacy.org/resources/state-student-privacy/ |
| WEB-11 | https://ikeepsafe.org/content/uploads/2017/01/FERPA-101-for-EdTech-iKeepSafe.pdf |
| WEB-12 | https://studentprivacycompass.org/ptac1/ |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** openai/gsm8k (configs: `main`, `socratic`)
**Analysis date:** 2025-01-31
**Examples reviewed:** 47 (`main` train), 33 (`socratic` train) = 80 total
**Columns shown:** question, answer
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | main | 3 | 99 | "Her parents bought a unicorn piñata for $13 and filled it with all of her favorite treats. They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." | US dollar pricing, brand-name American candy — strongly US cultural context | IC |
| D2 | main | 17 | 11 | "Linda bought two coloring books at $4 each, 4 packs of peanuts at $1.50 each pack, and one stuffed animal. She gave the cashier $25 and got no change." | USD transactions with decimal cents; cashier context | IC |
| D3 | main | 22 | 80 | "Austin bought his seven friends each a robot. Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change." | USD with tax — American retail context including sales tax | IC |
| D4 | main | 18 | 72 | "James joins a football team and becomes the star. He scores 4 touchdowns per game and each touchdown is worth 6 points. There are 15 games in the season. He also manages to score 2 point conversions 6 times during the season." | American football scoring system — distinctly US cultural setting | IC |
| D5 | main | 6 | 54 | "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" | US customary units (feet), volume calculation — matches deployment's unit system | IC, IO |
| D6 | main | 12 | 78 | "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9… the dog reached its final adult weight by adding another 30 pounds" | US customary weight (pounds) throughout | IC |
| D7 | main | 25 | 16 | "he poured into the box enough jelly beans to bring the weight to 2 pounds… he added enough brownies to cause the weight to triple… he added another 2 pounds of jelly beans" | US customary weight (pounds) used consistently | IC |
| D8 | main | 9 | 28 | "Four people lost a total of 103 kilograms of weight. The first person lost 27 kilograms." | Metric weight (kilograms) — not US customary | IC |
| D9 | main | 24 | 180 | "it rained 4 inches per day during the first 15 days of November… the average daily rainfall was twice the amount observed during the first 15 days" | Rainfall in inches (US customary), no conversion required | IC |
| D10 | main | 11 | 35 | "calculate the average age of the three?" — solved as "105 years / 3 people = <<105/3=35>>35 years/person" | Mean/average calculation embedded in a word problem — statistical reasoning present | IO |
| D11 | main | 6 | 54 | "4 feet long, 6 feet wide, and 3 feet high… 4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft… 72 cubic ft * 3/4 = <<72*3/4=54>>54 cubic ft" | Volume calculation using length × width × height — geometry-adjacent area/volume | IO |
| D12 | main | 35 | 333200 | "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft and the barn out back is 1,000 sq ft. How much is this property?" | Area (sq ft) applied to pricing — geometry-adjacent; uses sq ft (US customary) | IO, IC |
| D13 | main | 1 | 32 | "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them. On Wednesday Buddy buys 12 baseball cards. On Thursday he buys a third of what he had on Tuesday." | Multi-step four-operations problem across sequential days | IO |
| D14 | main | 7 | 90 | "There are enough provisions in a castle to feed 300 people for 90 days. After 30 days, 100 people leave the castle. How many more days are left until all the food runs out?" | Multi-step proportional reasoning (rates/ratios) — castle setting, not US-specific | IC |
| D15 | main | 38 | 90 | "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440, and Amalie spends 3/4 of what she has on toys" | Ratio problem with non-US names; no currency denomination specified | IC |
| D16 | main | 23 | 220 | "Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys" | Algebraic reasoning with US car brands — requires variable setup | IO |
| D17 | main | 4 | 21 | "The bottle of milk cost was 75% of the total cost of the sandwich and juice" — "75/100 * 12 = $<<75/100*12=9>>9" | Percentage calculation embedded in word problem | IO |
| D18 | main | 30 | 7200 | "her rent goes up by 30%, food costs increase by 50%, and the cost of her car insurance triples" | Multi-step percentage increase problem with monthly/annual scaling | IO |
| D19 | main | 43 | 720 | "Ariella's account earns her simple interest at the rate of 10% per annum. If Daniella has $400, how much money will Arialla have after two years?" | Simple interest calculation — financial math, USD | IO, IC |
| D20 | main | 19 | 54 | "Bobby has 16 toy cars, and the number of cars he has increases by 50% every year. How many toy cars will Bobby have in three years?" | Repeated percentage growth — compound-style reasoning over years | IO |
| D21 | main | 2 | 9 | "She gives away 4/5 of the cupcakes to her classmates. Of the remaining 1/5 of cupcakes, she eats 3 cupcakes." | Fraction operations on a whole — grades 4-5 fraction content | IO |
| D22 | main | 45 | 120 | "Ten friends decide to get an end-of-year gift for their teacher… four of the group drop out. The remaining friends split the cost equally… each share is now $8 more" | Algebraic reasoning with cost-splitting | IO |
| D23 | main | 31 | 10 | "Dan owns an ice cream shop and every sixth customer gets a free ice cream cone. Cones cost $2 each. If he sold $100 worth of cones, how many free ones did he give away?" | Division with a logical twist — note: answer logic has arithmetic error in solution (50/5=10, but every 6th, not 5th) | OC |
| D24 | main | 36 | 1080 | "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day. If there are 6 jaguars in a forest" | Multi-step chained multiplication — nature/ecology context | IO |
| D25 | main | 13 | 1825 | "If Sally makes $6 per day and Bob makes $4 per day, how much money will they both have saved for their trip after a year?" | USD daily earnings, year-long accumulation — simple interest-like structure | IC |
| D26 | main | 37 | 80 | "He has gotten 8 haircuts and knows that he needs 2 more to reach his goal. What percentage towards his goal is he?" | Percentage of goal completion — straightforward percentage | IO |
| D27 | main | 39 | 20 | "Ian won $100 in the lottery. He decided to use the money to pay off debts. He paid $20 to Colin." | USD lottery/debt context — British names (Colin, Helen, Benedict) suggest possible non-US authorship | IC |
| D28 | main | 41 | 347 | "She went to the mall and spent $250. Then, she went to the movies and watched 3 movies back to back that each cost $24. Then she stopped by the farmer's market on her way home and got 20 bags of beans at $1.25/bag." | USD across multiple retail settings; farmer's market — culturally American context | IC |
| D29 | main | 44 | 11000 | "He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value." | Large-dollar USD transactions, car-buying in American context | IC |
| D30 | socratic | 6 | 54 | "How many cubic feet are in the aquarium? ** First calculate the volume of the aquarium by multiplying its length, width and height: 4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft" | Socratic decomposition explicitly scaffolds volume step — same problem as D11 | IO |
| D31 | main | 47 | 72 | "Larry spends half an hour twice a day walking and playing with his dog. He also spends a fifth of an hour every day feeding his dog. How many minutes does Larry spend on his dog each day?" | Unit conversion (hours to minutes) within problem — time measurement conversion | IO |
| D32 | main | 26 | 2250 | "Roberto can skip 4,200 times an hour. Valerie can skip 80 times a minute. If they jump rope for fifteen minutes straight" | Rate conversion (hours to minutes) required for solution | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Consistent USD currency throughout the dataset
- **Dimension(s):** IC
- **Observation:** The overwhelming majority of problems involving monetary amounts use US dollars and cents, including decimal-cent amounts ($1.50, $8.75, $7.22), retail tax scenarios, and large-dollar purchases. No non-US currency (£, €, AUD) was observed in any of the 80 sampled examples.
- **Deployment relevance:** The platform specifies that problems use dollars/cents; this benchmark directly matches that convention, supporting IC validity for the currency dimension.
- **Datapoint citations:**
  - [D1] Example 3 (main, train, label=99): "Her parents bought a unicorn piñata for $13… 4 bags of Reese's for $9 per bag" — USD pricing with American brand names
  - [D2] Example 17 (main, train, label=11): "Linda bought two coloring books at $4 each, 4 packs of peanuts at $1.50 each pack… She gave the cashier $25 and got no change." — USD with decimal cents and cashier transaction
  - [D3] Example 22 (main, train, label=80): "Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change." — USD with sales tax, characteristic of American retail
  - [D28] Example 41 (main, train, label=347): "She went to the mall and spent $250… 3 movies back to back that each cost $24… 20 bags of beans at $1.25/bag." — USD across multiple everyday American contexts

#### Strength 2: Strong coverage of multi-step four-operations arithmetic at grades 3-6 difficulty
- **Dimension(s):** IO
- **Observation:** The sample contains numerous problems requiring 3-6 sequential arithmetic operations across addition, subtraction, multiplication, and division on multi-digit numbers, directly matching the platform's highest-volume grade 3-6 cohort.
- **Deployment relevance:** This is the platform's core use case — the benchmark provides ample examples of the problem type the homework-checker most frequently encounters.
- **Datapoint citations:**
  - [D13] Example 1 (main, train, label=32): "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half… On Wednesday Buddy buys 12… On Thursday he buys a third of what he had on Tuesday." — four sequential steps with division, subtraction, and addition
  - [D24] Example 36 (main, train, label=1080): "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day. If there are 6 jaguars in a forest" — chained multiplication across three steps
  - [D18] Example 30 (main, train, label=7200): "her rent goes up by 30%, food costs increase by 50%, and the cost of her car insurance triples… multiply the increase per month by the number of months in a year" — multi-step percentage and scaling over time

#### Strength 3: US customary units (feet, pounds, inches) present in a meaningful share of problems
- **Dimension(s):** IC
- **Observation:** Several sampled problems use US customary measurement units (feet, pounds, square feet) without any metric equivalent, confirming that at least a portion of the benchmark uses the unit system the platform requires.
- **Deployment relevance:** The platform specifies that problems use US customary units; these examples confirm partial alignment. The question is whether coverage is systematic enough (see Concern 1).
- **Datapoint citations:**
  - [D5] Example 6 (main, train, label=54): "If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" — feet/cubic feet throughout
  - [D6] Example 12 (main, train, label=78): "the puppy weighed 6 pounds, but doubled in weight by week 9… adding another 30 pounds" — pounds as the only weight unit
  - [D12] Example 35 (main, train, label=333200): "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft and the barn out back is 1,000 sq ft." — square feet used naturally

#### Strength 4: Binary final-answer grading structure perfectly matches deployment output requirements
- **Dimension(s):** OO, OF
- **Observation:** Every example terminates with a clearly delimited final numerical answer (`#### N`), and intermediate computation is shown only in the `answer` field. The question field contains only the word problem. This structure maps directly to a binary correct/incorrect check on the student's submitted number.
- **Deployment relevance:** The platform does not score intermediate steps; the `#### N` convention means the benchmark's evaluation protocol matches the deployment's exact output comparison task with no adaptation needed.
- **Datapoint citations:**
  - [D13] Example 1 (main, train, label=32): "#### 32" — clean numerical delimiter
  - [D21] Example 2 (main, train, label=9): "#### 9" — fraction operations resolve to a clean integer
  - [D22] Example 45 (main, train, label=120): "#### 120" — algebraic problem terminates in final numerical answer

#### Strength 5: Fraction and percentage problems represented across the sample
- **Dimension(s):** IO
- **Observation:** The sample contains multiple problems requiring fraction arithmetic (4/5, 3/4, 1/3) and percentage calculations (30%, 50%, 75%, 80%), covering the grades 4-6 content the platform serves.
- **Deployment relevance:** These sub-skills are explicitly listed in the deployment's problem inventory; their presence in the benchmark supports evaluation coverage for these content types.
- **Datapoint citations:**
  - [D21] Example 2 (main, train, label=9): "She gives away 4/5 of the cupcakes to her classmates. Of the remaining 1/5 of cupcakes, she eats 3 cupcakes." — explicit fraction-of-a-whole operation
  - [D17] Example 4 (main, train, label=21): "The bottle of milk cost was 75% of the total cost of the sandwich and juice… 75/100 * 12 = $<<75/100*12=9>>9" — percentage as fraction applied to cost
  - [D18] Example 30 (main, train, label=7200): "her rent goes up by 30%, food costs increase by 50%, and the cost of her car insurance triples" — percentage increase across multiple items
  - [D26] Example 37 (main, train, label=80): "What percentage towards his goal is he? … (8 / 10) x 100 = <<(8/10)*100=80>>80" — percentage of a goal

#### Strength 6: American cultural settings dominate the sample
- **Dimension(s):** IC
- **Observation:** Problem settings are predominantly American: American football, birthday parties with brand-name US candy, shopping at malls and farmer's markets, school field trips, and babysitting. These settings match the platform's stated requirement for "culturally familiar American settings."
- **Deployment relevance:** IC alignment on cultural setting reduces construct-irrelevant variance — students encounter familiar contextual framing rather than unfamiliar cultural scenarios that might introduce reading comprehension burden beyond the math task.
- **Datapoint citations:**
  - [D4] Example 18 (main, train, label=72): "James joins a football team… He scores 4 touchdowns per game and each touchdown is worth 6 points… 2 point conversions" — American football terminology and scoring
  - [D1] Example 3 (main, train, label=99): "4 bags of Reese's… 3 bags of Snickers… 5 bags of Skittles" — US brand-name candy at a birthday party
  - [D28] Example 41 (main, train, label=347): "She went to the mall and spent $250… she stopped by the farmer's market on her way home" — mall + farmer's market are recognizable American contexts

#### Strength 7: Average/mean calculation appears as an embedded skill in the sample
- **Dimension(s):** IO
- **Observation:** At least one problem explicitly requires computing a mean (average) as the final answer, suggesting that basic statistics operations are not entirely absent from the benchmark.
- **Deployment relevance:** The platform includes mean/median problems; finding at least one mean problem in the 47-example sample is mildly positive evidence, though median problems were not observed.
- **Datapoint citations:**
  - [D10] Example 11 (main, train, label=35): "calculate the average age of the three? … 105 years / 3 people = <<105/3=35>>35 years/person" — explicit mean calculation as the primary question

#### Strength 8: Geometry-adjacent area/volume problems present
- **Dimension(s):** IO
- **Observation:** Two distinct problems in the sample require computing area or volume as a sub-step or primary goal, demonstrating that the benchmark is not entirely devoid of geometry-adjacent measurement content.
- **Deployment relevance:** The platform regularly includes area and perimeter problems. While the sample does not show perimeter problems, area/volume problems are present, partially addressing the documented gap.
- **Datapoint citations:**
  - [D11] Example 6 (main, train, label=54): "4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft" — volume of a rectangular prism
  - [D12] Example 35 (main, train, label=333200): "The house is 2,400 sq ft and the barn out back is 1,000 sq ft… 2400+1000 = <<2400+1000=3400>>3,400 sq ft" — area addition applied to real estate pricing

#### Strength 9: Ratio and rate problems represented
- **Dimension(s):** IO
- **Observation:** Several problems require working with ratios, rates, or proportional reasoning, covering the grades 6-8 content listed in the deployment.
- **Deployment relevance:** Ratios/percentages are explicitly listed as part of the platform's problem inventory for upper grades; these examples confirm benchmark coverage extends to that difficulty band.
- **Datapoint citations:**
  - [D15] Example 38 (main, train, label=90): "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440…" — explicit ratio-to-quantity conversion
  - [D14] Example 7 (main, train, label=90): "The 200 people will eat 200/300 = 2/3 as much food as the original group… 60 days / (2/3) = <<60/(2/3)=90>>90 more days." — proportional rate reasoning

---

### Potential Concerns

#### CRITICAL

*(No findings at CRITICAL severity were identified in the sampled data.)*

---

#### MAJOR

#### Concern 1: Metric units appear alongside US customary units without conversion context
- **Dimension(s):** IC
- **Observation:** While many problems use US customary units (feet, pounds), at least one sampled problem uses kilograms as its sole measurement unit with no US customary equivalent provided. This creates a mixed unit environment rather than the consistently US-customary setting the platform uses.
- **Deployment relevance:** The platform states problems "consistently use… US customary units" and that metric "appears only where Common Core mandates some exposure in upper grades." A benchmark that intermixes kilograms without flagging grade-level context reduces IC alignment for the dominant use case (grades 3-6 where metric exposure is minimal).
- **Datapoint citations:**
  - [D8] Example 9 (main, train, label=28): "Four people lost a total of 103 kilograms of weight. The first person lost 27 kilograms. The second person lost 7 kilograms less than the first person." — kilograms used exclusively, no US customary equivalent

#### Concern 2: No explicit measurement conversion problems (feet↔inches, cups↔gallons, pounds↔ounces) observed in 80-example sample
- **Dimension(s):** IO
- **Observation:** The deployment's highest-priority flagged gap was US customary unit conversion problems. Across 80 sampled examples, no problem required converting between US customary units (e.g., 12 inches = 1 foot, 16 ounces = 1 pound, 4 cups = 1 quart). The measurement problems observed use a single unit throughout or involve time conversions (hours↔minutes), not unit-system conversions within the US customary framework.
- **Deployment relevance:** Measurement conversion is a standard Common Core skill from grades 4-5 onward that the platform includes regularly. Its apparent absence from the sample suggests either low frequency in the full dataset or complete absence — either way, the benchmark may under-test this specific sub-skill.
- **Datapoint citations:**
  - [D31] Example 47 (main, train, label=72): "Larry spends half an hour twice a day… a fifth of an hour every day feeding his dog. How many minutes does Larry spend on his dog each day?" — time conversion (hours to minutes) but not US customary physical unit conversion
  - [D32] Example 26 (main, train, label=2250): "Roberto can skip 4,200 times an hour. Valerie can skip 80 times a minute." — rate conversion hours→minutes, not physical unit conversion (in↔ft, oz↔lb, etc.)
  - [D5] Example 6 (main, train, label=54): "4 feet long, 6 feet wide, and 3 feet high" — feet used but no conversion between feet and inches required

#### Concern 3: Basic statistics problems (mean from small datasets, median) extremely sparse; no median problem observed
- **Dimension(s):** IO
- **Observation:** Only a single mean/average calculation was found in 80 sampled examples, and it appeared as an embedded sub-skill (average age of three people), not as a standalone data/statistics word problem involving a named dataset. No problem asked students to find the median, range, or mode of a set of values, nor did any problem present a table or list of data values to summarize.
- **Deployment relevance:** The platform explicitly lists "basic data/statistics problems (mean/median from small datasets)" as a regular content type and Common Core grades 6-8 content. The near-absence of such problems in a large sample is consistent with the documented gap in the benchmark YAML and represents a meaningful coverage limitation for the upper-grade portion of the platform's student population.
- **Datapoint citations:**
  - [D10] Example 11 (main, train, label=35): "calculate the average age of the three? … 105 years / 3 people = <<105/3=35>>35 years/person" — the only mean calculation observed; embedded in an age problem, not a data-summary context

#### Concern 4: Area and perimeter problems present but perimeter-specifically absent; volume appears instead
- **Dimension(s):** IO
- **Observation:** Two geometry-adjacent problems appeared in the sample, but both involved volume or area-as-pricing rather than the perimeter calculations that are a standard K-8 Common Core skill. No problem asked students to find the perimeter of a shape or use perimeter in a word problem context.
- **Deployment relevance:** The platform "regularly includes area and perimeter word problems" as a paired skill; finding area-type problems but no perimeter problems suggests the benchmark may cover only part of this sub-domain.
- **Datapoint citations:**
  - [D11] Example 6 (main, train, label=54): "4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft" — volume, not perimeter
  - [D12] Example 35 (main, train, label=333200): "2,400 sq ft… 1,000 sq ft… 2400+1000 = 3,400 sq ft" — area addition for pricing, not a geometric perimeter task

#### Concern 5: K-2 and lower-elementary single-step arithmetic absent from sample
- **Dimension(s):** IO
- **Observation:** The simplest problems in the 80-example sample still require 2-3 sequential operations and assume competence with multi-digit arithmetic. No single-operation problems (e.g., "Maria has 7 apples and gets 3 more. How many does she have?") appear in the sample, suggesting the benchmark skews toward grades 3-6 difficulty and above.
- **Deployment relevance:** The platform serves K-8, including students in grades K-2 where single-step problems are the norm. If the homework-checker is applied to early-grade submissions, GSM8K provides no test coverage for that difficulty band.
- **Datapoint citations:**
  - [D13] Example 1 (main, train, label=32): "On Monday… On Tuesday Buddy loses half… On Wednesday Buddy buys 12… On Thursday he buys a third of what he had on Tuesday." — minimum of 4 sequential operations; not accessible at K-2 difficulty
  - [D27] Example 27 (main, train, label=9): "He gave 3 to his mom, another 3 to his sister, 5 to his grandmother, and 2 to his dog. Then, he divided the remaining dandelion puffs equally among his 3 friends." — even the simpler-seeming problems require 2+ steps and division

---

#### MINOR

#### Concern 6: Occasional non-US personal names and settings suggest some non-US authorship
- **Dimension(s):** IC
- **Observation:** A small number of problems feature names that are more common in non-US English-speaking contexts (Colin, Helen, Benedict from the UK; Sab and Dane; Elsa and Amalie) and one setting ("castle provisions") that is not characteristically American. This is consistent with the benchmark YAML's note that contractor nationality was undocumented.
- **Deployment relevance:** For the platform's goal of "culturally familiar American settings," these occasional non-US-flavored problems are a minor inconsistency. The arithmetic skills tested remain equivalent, but the cultural framing may not match what students encounter on the platform.
- **Datapoint citations:**
  - [D27] Example 39 (main, train, label=20): "Ian won $100 in the lottery. He decided to use the money to pay off debts. He paid $20 to Colin… paid twice as much to Helen… paid half as much to Benedict" — British names; lottery winnings context
  - [D14] Example 7 (main, train, label=90): "There are enough provisions in a castle to feed 300 people for 90 days." — medieval castle setting, not an American school or everyday context
  - [D15] Example 38 (main, train, label=90): "The ratio of coins that Elsa has to that which Amalie has is 10:45." — Scandinavian names; "coins" without denomination specified

#### Concern 7: One solution contains a potential logical error in problem setup
- **Dimension(s):** OC
- **Observation:** Example 31 states "every sixth customer gets a free ice cream cone" but the solution divides by 5 rather than 6 to find free cones (50/5=10), suggesting either a problem statement error or an interpretation inconsistency. The ground-truth label is 10, which corresponds to the solution's arithmetic (dividing by 5), not the problem's stated rule (every 6th).
- **Deployment relevance:** This is consistent with the paper's documented 1.7% error/ambiguity rate. For a binary-correct homework-checker, a problem where the stated rule and the computed answer do not match could cause the LLM to answer differently from the ground truth — not due to reasoning failure but due to problem ambiguity. The rate is low but worth noting.
- **Datapoint citations:**
  - [D23] Example 31 (main, train, label=10): "Dan owns an ice cream shop and every sixth customer gets a free ice cream cone. Cones cost $2 each. If he sold $100 worth of cones, how many free ones did he give away? … He gave away 10 cones because 50 / 5 = <<50/5=10>>10" — problem says "sixth" but solution divides by 5

#### Concern 8: Algebra-required problems (variable setup) may exceed typical K-8 arithmetic scope
- **Dimension(s):** IO
- **Observation:** Two problems in the sample require setting up and solving a linear equation with a variable, which is more characteristic of grades 7-8 pre-algebra than the four-operations arithmetic that dominates the deployment's K-6 use case. If an LLM is evaluated primarily on arithmetic problems and these algebraic problems are present, they test a somewhat different skill.
- **Deployment relevance:** The platform's stated problem inventory is "multi-step problems with four operations… fractions, decimals/percentages/ratios." Formal variable-based algebra is not listed. These problems are valid for grades 7-8 but their presence means the benchmark includes a small proportion of problems that may not map to the platform's content standards.
- **Datapoint citations:**
  - [D16] Example 23 (main, train, label=220): "Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys… Let x represent the number of Chevys… 11x+15=301… x=26" — requires symbolic variable and equation solving
  - [D22] Example 45 (main, train, label=120): "Ten friends decide to get an end-of-year gift… four of the group drop out… If each share is now $8 more, how much does the gift cost? … Let N be the original price… 10N=6(N+8)… N=12" — explicit variable equation required

---

### Content Coverage Summary

The 80 sampled examples (47 `main`, 33 `socratic`) are natural-language arithmetic word problems in American English, almost entirely set in everyday US contexts: shopping, school activities, sports (American football, recess, boxing), pets, home improvement, and financial scenarios. Currency is uniformly USD with decimal cents. US customary units (feet, pounds, square feet) appear in roughly 3-4 of 47 `main` examples; metric units appear in at least 1 example (kilograms). The difficulty range spans approximately grades 3-7: problems consistently require 2-6 sequential operations, with fractions, percentages, ratios, and proportional reasoning well represented. Formal algebra (variable-based equations) appears in 2 examples. 

The `socratic` config contains the identical problem text but with step-by-step sub-questions decomposing each solution step, which is not directly relevant to the deployment's binary answer-checking use case but could be useful for reasoning evaluation.

Key topic observations from the sample:
- **Well represented:** Four operations, fractions, percentages, ratios, time/rate calculations, USD financial math
- **Partially represented:** Area/volume (2 examples), mean/average (1 example embedded), US customary measurement usage (but not conversion)
- **Not observed:** Perimeter problems, median/mode/range statistics problems, US customary unit-to-unit conversion (inches↔feet, ounces↔pounds, cups↔quarts), decimal place value problems, K-2 single-step arithmetic

The socratic config provides the same problems with Socratic sub-question scaffolding added to answers, but questions are identical to `main`, so it does not add new content coverage.

---

### Limitations

1. **Sample size:** 47 `main` + 33 `socratic` examples represent approximately 1.1% of the full 7,473 train + 1,319 test = 8,792 examples. Rare sub-topics (e.g., measurement conversion problems that appear in 2-5% of the dataset) could be entirely absent from this sample by chance. The absence of perimeter problems or unit conversion problems in the sample does not definitively confirm their absence from the full dataset.

2. **No topic labels:** The dataset has no subtopic taxonomy or difficulty tags in its schema (`question` and `answer` only), so the sample cannot be stratified by skill type. A systematic frequency analysis of measurement conversion, statistics, or geometry problems would require processing the full dataset with keyword or semantic search.

3. **Full dataset not inspectable:** Only 80 examples were reviewed. The coverage observations (particularly for statistics, perimeter, and conversion problems) are based on the sample and should be validated against the full 8,500-problem corpus before drawing definitive conclusions.

4. **No difficulty metadata:** Grade-level difficulty cannot be formally assessed from the text alone. The characterization of K-2 absence is based on the observed minimum complexity in the sample, not a systematic difficulty annotation.

5. **Socratic config overlap:** The `socratic` config examples reviewed were identical in question text to `main` examples; no new content coverage information was gained from those 33 examples beyond confirming the step-decomposition format.

