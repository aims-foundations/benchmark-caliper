## Deployment Context

We are a US edtech company building a tool for American teachers to generate novel math word problems. Teachers specify a topic (e.g., multi-step fractions), grade level, and difficulty, and the system produces original assessment items complete with verified solutions and distractor answer choices for multiple-choice format. We need to evaluate the LLM's ability to generate pedagogically appropriate, mathematically accurate assessment content aligned to Common Core standards.

# Validity Analysis: gsm8k
**Target context:** US K–8 Edtech: CCSS-Aligned Math Assessment Item Generation
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content | 2 | Significant gaps | medium |
| Output Form ⚠ | 1 | Serious concern | high |
| **Average** | **2.0** | | |

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

GSM8K is a poor fit for the US K–8 CCSS-aligned MCQ item-generation deployment. The benchmark measures a single dimension — final-numeric-answer correctness on multi-step grade-school arithmetic word problems — and the deployment's elicitation explicitly identifies this as only the rank-1 hard-gate prerequisite of a five-dimension rubric. The remaining four dimensions (CCSS standard-cluster alignment, distractor plausibility grounded in student misconceptions, grade-level language appropriateness, cultural inclusivity) are entirely outside GSM8K's design scope, and dataset analysis confirms structural absence rather than sampling artifact: zero CCSS or grade tags, uniform free-form solution format with no MCQ structure, and substantial culturally narrow content (American football scoring, brand-name US candy, beauty contests, pervasive adult financial scenarios). Input form is the lone strong dimension (text-only English on both sides). Three dimensions (IO, IC, OC) score 2 reflecting partial coverage with major gaps; two dimensions (OO, OF) score 1 reflecting categorical mismatch. The benchmark is usable only as a screening filter for the hard-gate arithmetic-accuracy prerequisite and provides no signal about the deployment's primary pedagogical evaluation construct.

## Practical Guidance

### What This Benchmark Measures

GSM8K provides a meaningful signal for one dimension of the deployment's evaluation hierarchy: multi-step arithmetic accuracy on grade-school-level math word problems. The benchmark's free-form natural-language-solution format with calculator-annotated step-by-step reasoning [Q32, Q33, Q40] is also a reasonable proxy for the underlying capability to produce worked-solution explanations. For the deployment's rank-1 'hard gate' of mathematical solution accuracy, GSM8K is a usable, if partial, screening filter — any model failing on GSM8K is likely to produce mathematically inaccurate items and should be excluded from further consideration.

### Construct Depth

Construct depth is shallow for the deployment's actual evaluation needs. GSM8K probes arithmetic-accuracy capability across a broad range of operations (fractions, ratios, percentages, simple algebra) and multi-step reasoning depth (2–6+ steps) [DATASET-D1, D6, D22], so the depth of evidence within the arithmetic-accuracy dimension is reasonable. However, this is a single dimension of a five-dimension deployment construct: CCSS standard-cluster alignment (HIGH priority, rank 3), distractor plausibility (HIGH priority, rank 2), grade-level language appropriateness (HIGH priority, rank 4), and cultural inclusivity (HIGH priority, rank 5) are entirely unaddressed by any GSM8K metric, label, or design constraint. The construct depth in the dimensions that most differentiate pedagogical value is therefore zero.

### What Else You Need

Substantial supplementation is required across four of the six validity dimensions. For input ontology (IO) and output ontology (OO): adopt or build a CCSS-standard-cluster-tagged evaluation corpus, using EDUMATH [WEB-10], Smarter Balanced [WEB-11], or PARCC/New Meridian [WEB-14] as reference banks. For input content (IC): commission a cultural-inclusivity audit aligned to NCTM equity guidance [WEB-8] and WIDA 2020 lexical-complexity targets [WEB-3]. For output content (OC) and output form (OF): build a teacher-evaluated MCQ-package evaluation pipeline addressing distractor plausibility, misconception grounding, and grade-band-appropriate language. Web evidence confirms distractor quality is an active but unsolved research area [WEB-5, WEB-6, WEB-7], and the deployment will likely require human teacher evaluation as the gold standard for the distractor-quality dimension.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
GSM8K is described as an undifferentiated pool of 'grade school math word problems' with no CCSS, grade-band, or topical taxonomy [Q1, Q8, Q12]. The deployment requires standard-cluster-level alignment (e.g., 4.NF.A.2, 6.RP.A.3), which the elicitation marks as 'essential and non-negotiable' [HIGH priority]. Dataset sampling confirms the gap is structural, not a sampling artifact: problems clearly spanning 2nd-grade addition to 7th-grade simple interest and 6–8 algebra appear in the same pool without labels [DATASET-D3, D4, D5, D22, D28]. The benchmark does probe a broad range of arithmetic operations (fractions, ratios, percentages, simple algebra) [DATASET-D6, D7, D22], so partial construct coverage of the prerequisite 'multi-step arithmetic reasoning' dimension exists [Q10, Q11]. But for the deployment's required ontology — CCSS standard-cluster targeting and grade-band differentiation — the benchmark provides no validation signal whatsoever.

**Strengths:**
- Broad coverage of grade-school arithmetic operation types (four-function, fractions, percentages, ratios, rates, simple algebra) provides a partial proxy for multi-domain competence [DATASET-D6, D7, D22]
- Multi-step reasoning is reliably represented across the sample, matching the deployment's hard-gate 'mathematical accuracy' prerequisite [Q10, DATASET-D1, D2, D23]

**Checklist:**

- **IO-1**: The deployment requires categories defined by CCSS standard clusters (e.g., 4.NF.A.2 fractions, 6.RP.A.3 ratios/proportions, 3.OA.A.1 operations, 5.NF.B.4 fraction multiplication) and by grade band (K–2, 3–5, 6–8), per the elicitation and regional YAML. — _Sources: WEB-1, WEB-11_
- **IO-2**: Yes — GSM8K's taxonomy is a single undifferentiated 'grade school math' category [Q1, Q8, Q12]; no CCSS domain, cluster, or standard tags exist and no grade-level labels are present in any sampled datapoint [DATASET-D3, D4, D5, D7]. — _Sources: Q1, Q8, Q12, DATASET-D3, DATASET-D4, DATASET-D5, DATASET-D7_
- **IO-3**: No clearly irrelevant categories are introduced — the benchmark stays within grade-school arithmetic — but the undifferentiated pool mixes 7th–8th grade algebraic content [DATASET-D4, D22] with 2nd–3rd grade arithmetic [DATASET-D28], introducing construct-irrelevant variance for any grade-band-specific evaluation. — _Sources: DATASET-D4, DATASET-D22, DATASET-D28_
- **IO-4**: Category gaps harming content validity: (1) no CCSS standard-cluster tagging; (2) no grade-band differentiation; (3) no separation between problem types relevant to specific CCSS domains (OA, NF, NBT, RP, EE, SP, G). These gaps are confirmed empirically across the sample [DATASET-D3, D4, D5, D7, D22]. — _Sources: Q1, WEB-10, DATASET-D3, DATASET-D4, DATASET-D5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems.' (p.1)
- [Q8] 'We are releasing GSM8K, a dataset of 8.5K high quality problems at the grade school math level.' (p.2)
- [Q11] 'GSM8K solutions depend only on elementary concepts, so achieving high test performance is a tractable goal.' (p.2)
- [Q12] 'We present a curated dataset of 8.5K grade school math questions and natural language solutions, useful for probing the informal reasoning ability of large language models.' (p.2)

*Web sources:*
- [WEB-10] EDUMATH (2024) is the first teacher-annotated dataset for standards-aligned MWP generation, introducing a Standards Alignment criterion — confirming no prior LLM benchmark provided CCSS-cluster-level tagging
- [WEB-11] Smarter Balanced open interim item bank provides grade- and CCSS-standard-tagged items as an external reference corpus
- [WEB-1] CCSS-M is the authoritative curriculum framework adopted by 41 states, DC, and DoDEA

*Dataset analysis:*
- DATASET-D3: castle/provisions inverse-proportion problem maps to 6–7.RP but is unlabeled — confirms CCSS gap
- DATASET-D4: multi-variable algebraic system (Buicks/Fords/Chevys) maps to 6.EE/7.EE but appears untagged in the same pool as elementary problems
- DATASET-D5: simple interest at 10% per annum maps to 7.RP.A.3 but is indistinguishable in the dataset from 2nd-grade addition
- DATASET-D22: algebraic equation solving (10N=6(N+8)) consistent with 6–8 EE domain, untagged
- DATASET-D28: simple 2-step arithmetic (field trip vans) sits in the same pool as 7th-grade problems with no grade tag

</details>

**Information gaps:**
- Distribution of GSM8K problems across implicit CCSS domains is unknown — would require automated or human CCSS tagging of the full 8.5K dataset to estimate per-standard coverage.

**Requires expert verification:**
- A K–8 math curriculum specialist should perform a CCSS-cluster mapping audit on a representative GSM8K sample to estimate which standards (if any) achieve adequate problem density for evaluation use.

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
GSM8K's documentation emphasizes 'linguistic diversity' as a design goal [Q9, Q112, Q113] but reports no demographic, geographic, or cultural composition of the contractor workforce, nor any inclusivity guidelines [Q103, Q104]. The GPT-3 seed-question process introduces an additional uncharacterized cultural influence [Q110, Q111]. The dataset analysis empirically confirms culturally narrow content the deployment explicitly forbids: American football scoring rules [DATASET-D9], US brand-name candy [DATASET-D8], beauty/modeling contests [DATASET-D10], and pervasive adult financial contexts (rent, real estate, car purchase, mall spending) that the deployment specifically flags as money-context sensitivity risks [DATASET-D11, D12, D13, D16]. A weight-loss framing also appears [DATASET-D20]. Some counterweight exists: diverse names appear naturally [DATASET-D24], and ~30–35% of sampled problems use culturally neutral contexts [DATASET-D26, D27, D31]. But this is incidental, not designed, and the deployment marks IC as HIGH priority requiring active inclusivity guidelines that GSM8K provably lacks.

**Strengths:**
- Linguistic diversity in problem phrasings was an explicit design goal, with anti-template-reuse feedback to contractors [Q9, Q112, Q113]
- Diverse names (Kantana, Kimiko, Omi, Arlette, Amalie) appear naturally in some problems [DATASET-D24]
- A meaningful subset (~30–35%) of problems use culturally neutral contexts (nature, weather, animals, school scenarios) that translate well across demographic groups [DATASET-D26, D27, D31]

**Checklist:**

- **IC-1**: Yes — many problems require culturally specific US knowledge: American football scoring [DATASET-D9], US brand-name candy [DATASET-D8], and adult US consumer practices (mortgages, car depreciation, simple interest) [DATASET-D11, D12, D13]. The deployment explicitly forbids 'culturally narrow references' and 'particular sports with uneven US cultural distribution.' — _Sources: DATASET-D8, DATASET-D9, DATASET-D11, DATASET-D12, DATASET-D13_
- **IC-2**: Misaligned with deployment culture in multiple respects: adult financial contexts presuppose middle-class material conditions inappropriate for K–8 generally and stigmatizing for lower-income students [DATASET-D11, D12, D16]; gender-stereotyped beauty/modeling scenarios [DATASET-D10]; weight-loss framing potentially sensitive for adolescents [DATASET-D20]. — _Sources: DATASET-D10, DATASET-D11, DATASET-D16, DATASET-D20_
- **IC-3**: Yes — American football scoring rules [DATASET-D9] and US-specific candy brands [DATASET-D8] require Western/US-mainstream cultural knowledge that ELL students and recent-immigrant families may lack. The deployment requires low-idiom language for multilingual learners (per WIDA 2020 [WEB-3]); GSM8K has no such design constraint documented [Q103, Q104, Q112]. — _Sources: Q103, Q104, Q112, WEB-3, DATASET-D8, DATASET-D9_
- **IC-4**: INSUFFICIENT DOCUMENTATION — the benchmark paper does not document recruitment of regional or demographically representative annotators; contractor workforce demographics, geographic background, and educational training are unreported [Q103, Q104]. A teacher/equity-expert review would be needed. — _Sources: Q103, Q104_
- **IC-5**: Content issues harming content validity: (a) pervasive adult financial contexts inappropriate for K–8 [DATASET-D11, D12, D13, D16]; (b) culturally narrow US-mainstream references (football, brand-name candy) [DATASET-D8, D9]; (c) gender-stereotyped contexts [DATASET-D10]; (d) potentially sensitive body-weight framing [DATASET-D20]; (e) no documented inclusivity audit or guidelines [Q103, Q104, Q112]. — _Sources: Q9, Q103, Q110, DATASET-D8, DATASET-D9, DATASET-D10, DATASET-D11, DATASET-D20_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q9] 'We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts.' (p.2)
- [Q103] 'We initially collected a starting set of a thousand problems and natural language solutions by hiring freelance contractors on Upwork (upwork.com).' (p.15)
- [Q104] 'We then worked with Surge AI (surgehq.ai), an NLP data labeling platform, to scale up our data collection.' (p.15)
- [Q110] 'To assist contractors with writing questions, we provided seed questions automatically generated from a few-shot prompted 175B GPT-3 model.' (p.15)
- [Q112] 'We instructed contractors to be as descriptive as possible in their solutions, and to not re-use problem settings or templates between different questions.' (p.15)

*Web sources:*
- [WEB-3] WIDA 2020 ELD Standards provide grade-band-specific Language Expectations for ELL accessibility in mathematics contexts — the deployment's authoritative ELL language standard
- [WEB-8] NCTM Catalyzing Change series provides equity-centered guidance relevant to culturally inclusive math instruction
- [WEB-10] EDUMATH evaluates 'Educational Appropriateness' via teacher annotation — the closest analogue to a cultural-appropriateness check, which GSM8K lacks

*Dataset analysis:*
- DATASET-D8: US brand-name candy (Reese's, Snickers, Skittles) — culturally narrow consumer reference
- DATASET-D9: American football touchdown/2-point-conversion scoring — requires specific US sports cultural knowledge
- DATASET-D10: beauty and modeling contest with gendered shopping — gender-stereotyped, not culturally inclusive
- DATASET-D11: $1000/month rent, car insurance, food budget — adult household finance, inappropriate for K–5 and stigmatizing for lower-income households
- DATASET-D12: $333,200 property valuation — adult real estate, presupposes affluent ownership
- DATASET-D13: $20K-$30K car negotiation — adult consumer context
- DATASET-D16: mall spending $250, back-to-back movies — affluent leisure context
- DATASET-D20: weight loss as primary problem context — potentially sensitive for K–8 body-image
- DATASET-D24: Kimiko/Omi/Arlette names — partial, undesigned name diversity
- DATASET-D26: dandelion puffs/family-sharing — culturally neutral
- DATASET-D27: ecological chain (jaguars/snakes/birds/beetles) — culturally neutral

</details>

**Information gaps:**
- Contractor demographics, geographic locations, and educational backgrounds are entirely undocumented [Q103, Q104]
- GPT-3 seed-question cultural influence on the resulting problem distribution is uncharacterized [Q110]
- No quantitative estimate of the prevalence of culturally narrow vs. neutral contexts across the full 8.5K dataset; the 80-example sample suggests ~25–30% adult/narrow contexts but this is not a comprehensive audit

**Requires expert verification:**
- A K–8 equity/curriculum specialist should perform a systematic cultural inclusivity audit using NCTM equity guidance [WEB-8] and WIDA 2020 lexical-complexity criteria [WEB-3]
- An ELL specialist should assess idiom density and lexical complexity of GSM8K problem stems against WIDA grade-band Proficiency Level Descriptors

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input form is the lowest-risk dimension: GSM8K is English-language text-only [Q32, Q33], and the deployment is English-language text-only with Latin script. Solutions are presented as natural language prose with embedded calculator annotations [Q40, Q119, DATASET-D17], and the socratic config additionally scaffolds solutions as sub-question/answer pairs [DATASET-D18] — a form moderately closer to pedagogical worked examples. The only minor concern is that the calculator annotation tokens (`<<expr=result>>`) are training artifacts not present in natural classroom-ready worked examples [DATASET-D17], requiring preprocessing if GSM8K solutions are used as reference examples. There is no modality, script, or signal-distribution mismatch.

**Strengths:**
- Full language and modality match: English text-only on both sides [Q32, Q33]
- Natural language solution format is interpretable and aligned with the deployment's worked-example needs [Q33, DATASET-D17]
- Socratic config offers scaffolded sub-question format closer to pedagogical worked examples [DATASET-D18]

**Checklist:**

- **IF-1**: No signal-distribution mismatch — both source and target are English natural-language text [Q32, Q33]. The deployment's regional YAML confirms 'Full match on language and modality — lowest-risk validity dimension.' — _Sources: Q32, Q33_
- **IF-2**: Yes — text-based web/edtech infrastructure is universally supported in US K–8 settings; no special capture specifications required. — _Sources: Q32_
- **IF-3**: One minor domain-specific form difference: calculator annotation tokens (`<<...=...>>`) are embedded in solutions [Q40, Q119, DATASET-D17] and would require stripping for use as natural classroom-ready worked examples. — _Sources: Q40, Q119, DATASET-D17_
- **IF-4**: No major form mismatches that harm external validity. Minor preprocessing required to strip calculator annotations if solutions are reused as instructional references [DATASET-D17]. — _Sources: DATASET-D17_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q32] 'First, we focus attention on the space of natural language solutions, as this is a richer and more general solution format than pure mathematical expressions.' (p.5)
- [Q33] 'Moreover, this choice enables our models to develop verbal analytical skills and to produce solutions that are more readily interpretable by humans.' (p.5)
- [Q40] 'To mitigate this issue, we train all models to use a calculator by injecting calculation annotations into the training set.' (p.6)
- [Q119] 'During training, there is no special distinction between the annotated tokens and the rest of the solution: they are all just tokens.' (p.17)

*Dataset analysis:*
- DATASET-D17: natural language solution with embedded `<<30/2=15>>` annotations — illustrates form artifact requiring preprocessing
- DATASET-D18: socratic config breaks solution into explicit sub-question/answer pairs — closer to pedagogical scaffolding

</details>

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
GSM8K's output ontology is fundamentally and categorically misaligned with the deployment. Solutions are labeled correct/incorrect based solely on whether the final numeric answer matches [Q31, Q60], and the verifier outputs a scalar correctness probability [Q59]. The deployment requires a multi-dimensional output construct: (1) mathematical accuracy (hard gate), (2) distractor plausibility grounded in student misconceptions, (3) CCSS standard alignment, (4) grade-level language appropriateness, (5) cultural inclusivity — with the elicitation explicitly stating that 'correct' means a classroom-ready MCQ package, not arithmetic accuracy alone. Dataset analysis confirms every sampled example uses only the `#### N` numeric-answer convention with no MCQ structure, distractor choices, or misconception annotations [DATASET-D17, D7]. As the regional YAML notes, GSM8K covers only dimension 1 of a 5-dimension rubric, and elicitation marks OO as HIGH priority. Web evidence confirms no existing benchmark addresses CCSS-level alignment scoring [WEB-10] or distractor quality systematically [WEB-5, WEB-6, WEB-7].

**Strengths:**
- The single dimension GSM8K does score — mathematical accuracy via final numeric answer — directly maps to the deployment's hard-gate prerequisite [Q31, Q60]
- Verifier framework allows ranked scoring of multiple candidates [Q3, Q68], which could in principle be repurposed if extended with pedagogical labels

**Checklist:**

- **OO-1**: Output label categories are binary (correct/incorrect on final numeric answer) [Q31, Q60]. For the deployment, this captures only rank-1 (math accuracy) of a 5-dimension rubric and ignores ranks 2–5 (distractor plausibility, CCSS alignment, grade-level language, cultural inclusivity). — _Sources: Q31, Q59, Q60_
- **OO-2**: Missing categories specific to deployment: (a) CCSS standard-alignment labels [WEB-10], (b) distractor-quality labels [WEB-5, WEB-6, WEB-7], (c) grade-band-language labels [WEB-3], (d) cultural-inclusivity labels [WEB-8], (e) misconception-grounding labels. All five are entirely absent from GSM8K's label space. — _Sources: WEB-10, WEB-5, WEB-6, WEB-7, WEB-3, WEB-8_
- **OO-3**: The binary correct/incorrect schema does not encode non-regional values per se, but it encodes an assumption that mathematical correctness is the sole evaluation criterion — an assumption misaligned with the deployment's pedagogical 'classroom-ready' construct. — _Sources: Q60_
- **OO-4**: Stakeholder-driven taxonomy redesign is essential: the deployment requires labels for CCSS standard alignment, distractor plausibility, grade-level appropriateness, and cultural inclusivity — none of which GSM8K provides. EDUMATH [WEB-10] offers a closer (though still incomplete) starting point. — _Sources: WEB-10_
- **OO-5**: Taxonomy issues harming structural and content validity: (1) construct underrepresentation — 4 of 5 evaluation dimensions are entirely unmeasured; (2) the single measured dimension treats step-level reasoning quality as invisible (correct final answer can mask flawed reasoning, as the paper itself acknowledges [Q61]); (3) false positives via correct-answer-flawed-reasoning are documented but unaddressed [Q61, Q154]. — _Sources: Q61, DATASET-D17, DATASET-D7, DATASET-D33_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'Verifiers are trained to judge the correctness of solutions, with the training signal determined solely by whether or not the solution reached the correct final answer.' (p.5)
- [Q59] 'Conditioned on the problem and a candidate solution, the verifier outputs the probability that the solution is correct.' (p.7)
- [Q60] 'Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer.' (p.7)
- [Q61] 'In practice, some solutions will reach the correct final answer using flawed reasoning, leading to false positives.' (p.7)

*Web sources:*
- [WEB-10] EDUMATH (2024) introduces a Standards Alignment evaluation criterion for MWP generation — confirms no prior benchmark addressed this label category
- [WEB-5] DiVERT (2024) studies distractor generation via variational error representations — confirms distractor quality is an unsolved research dimension with no standard benchmark
- [WEB-6] Overgenerate-and-rank (2024) finds human-authored distractors still outperform LLM-generated ones — confirms distractor plausibility cannot be evaluated by GSM8K-style metrics
- [WEB-7] ACL 2025 distractor-rubric paper proposes pairwise rubric for misconception-targeting — none of these dimensions appear in GSM8K's label space

*Dataset analysis:*
- DATASET-D17: solution labeled only as `#### 32` — no CCSS, grade, distractor, or misconception annotation
- DATASET-D7: solution labeled only as `#### 9` — confirms label schema is uniform across the dataset
- DATASET-D33: example with potential internal reasoning inconsistency labeled only `96` — illustrates that label captures final answer, not reasoning quality

</details>

**Requires expert verification:**
- Psychometric/assessment-design specialist should define an output-label schema covering CCSS alignment, distractor plausibility, grade-band language, and cultural inclusivity for the deployment's actual evaluation needs.

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** medium

**Justification:**
GSM8K's ground-truth labels are final numeric answers with a documented 1.7% disagreement rate among contractors interpreted as the breaking-error fraction [Q107, Q108], with subtler errors acknowledged as possible [Q109]. For arithmetic accuracy alone, label quality is reasonable. However, annotator demographics, geographic locations, native languages, and pedagogical training are entirely unreported [Q103, Q104], precluding any analysis of whether labels reflect regional stakeholder (US K–8 teacher) perspectives. Calculator annotations were auto-generated rather than human-labeled, with acknowledged imperfections [Q117, Q118, Q123]. Crucially, no labels exist for the deployment's primary pedagogical dimensions (distractor quality, CCSS alignment, grade-level language, cultural inclusivity), so for the bulk of the deployment's construct, label-content validity is not just weak — it is undefined. Dataset analysis spotted at least one likely internal inconsistency [DATASET-D33], consistent with the documented error rate but reducing confidence in the dataset as a pedagogical ground truth.

**Strengths:**
- Cross-contractor agreement check via re-solving with non-original workers provides reasonable arithmetic-accuracy label quality (~1.7% disagreement) [Q105, Q106, Q107]
- Acknowledgment of label limitations (subtle errors possible, calculator imperfections) demonstrates documentation transparency [Q109, Q118, Q123]

**Checklist:**

- **OC-1**: Partially — for arithmetic correctness only, labels are likely to align with US K–8 teacher judgments since arithmetic correctness is culturally invariant. For the pedagogical dimensions the deployment prioritizes (distractor quality, CCSS alignment, grade-level appropriateness, cultural inclusivity), no labels exist at all, so the question of regional alignment cannot be answered. — _Sources: Q60, Q105, Q106, WEB-10_
- **OC-2**: Cannot be assessed — annotator demographic, geographic, and pedagogical-training information is unreported [Q103, Q104]. Likely there is significant disagreement potential since labels were produced by general crowd contractors, not K–8 math teachers. — _Sources: Q103, Q104_
- **OC-3**: INSUFFICIENT DOCUMENTATION — the paper reports contractor sourcing platform (Upwork, Surge AI) [Q103, Q104] but provides no demographic, geographic, educational, or pedagogical-background information; no Datasheet or Data Statement is referenced. — _Sources: Q103, Q104_
- **OC-4**: Re-annotation by a representative US K–8 teacher pool would be valuable for two purposes: (a) verifying arithmetic correctness on grade-appropriate items, (b) producing the missing pedagogical labels (CCSS alignment, grade band, distractor candidates, inclusivity flags). The deployment YAML notes EDUMATH [WEB-10] as the closest precedent, which uses teacher annotators. — _Sources: WEB-10_
- **OC-5**: Aggregation method is binary agreement check between original-author solutions and re-solver solutions [Q105, Q106]. This binary check by design erases any minority interpretive perspective; no stratified analysis across annotator subgroups is reported [Q107, Q108]. — _Sources: Q105, Q106, Q107, Q108_
- **OC-6**: Label issues harming convergent and external validity: (a) annotator demographics undocumented [Q103, Q104]; (b) labels cover only arithmetic correctness, not pedagogical dimensions central to deployment; (c) at least one potential internal inconsistency observed in sample [DATASET-D33]; (d) calculator annotations imperfect [Q117, Q118]; (e) binary aggregation erases interpretive disagreement [Q105–Q108]. — _Sources: Q103, Q104, Q109, Q117, Q118, DATASET-D33_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q105] 'After collecting the full dataset, we asked workers to re-solve all problems, with no workers re-solving problems they originally wrote.' (p.15)
- [Q106] 'We checked whether their final answers agreed with the original solutions, and any problems that produced disagreements were either repaired or discarded.' (p.15)
- [Q107] 'We then performed another round of agreement checks on a smaller subset of problems, finding that 1.7% of problems still produce disagreements among contractors.' (p.15)
- [Q108] 'We estimate this to be the fraction of problems that contain breaking errors or ambiguities.' (p.15)
- [Q109] 'It is possible that a larger percentage of problems contain subtle errors.' (p.15)
- [Q117] 'The calculator annotations were not provided by human contractors: they were generated by a combination of hard-coded logic and a finetuned language model.' (p.17)
- [Q118] 'The logic for auto-generating calculator annotations is imperfect.' (p.17)

*Web sources:*
- [WEB-10] EDUMATH uses teacher annotators to produce pedagogical-quality labels (Solvability, Accuracy, Educational Appropriateness, Standards Alignment) — illustrates the kind of annotator pool the deployment requires that GSM8K lacks

*Dataset analysis:*
- DATASET-D33: question states 'two times' but solution treats it as 'four times'; label of 96 follows solution logic — likely subtle inconsistency consistent with the paper's acknowledgment of possible subtle errors [Q109]
- DATASET-D17: full solution labeled only `#### 32` — confirms uniform binary-style labeling with no pedagogical metadata

</details>

**Information gaps:**
- Contractor demographics, geography, native languages, and pedagogical training entirely undocumented [Q103, Q104]
- No stratified agreement analysis across annotator subgroups [Q107]
- Rate of subtle (non-breaking) errors in labels not quantified [Q109]

**Requires expert verification:**
- Sample a stratified subset of GSM8K problems and have US K–8 math teachers re-evaluate (a) arithmetic accuracy, (b) age-appropriateness, (c) inferred CCSS alignment, and (d) cultural inclusivity to estimate the rate of latent labeling issues.

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Output form is categorically misaligned with deployment. GSM8K evaluates free-form natural language solution generation scored by final numeric answer match [Q3, Q29, Q46], with metrics including test@1, test@N [Q52], majority voting [Q85, Q87], and verifier-based ranking [Q68]. The deployment requires a structured MCQ item package: problem stem + verified correct answer + 3 misconception-grounded distractors + optional worked solution [elicitation A4 and regional YAML]. Dataset analysis confirms zero MCQ structure in any sampled example [DATASET-D17, D7]. Distractor quality is identified by the elicitation as 'the hardest and most critical' evaluation challenge, and web evidence confirms it is an unsolved research problem with no standardized benchmark [WEB-5, WEB-6, WEB-7]. GSM8K provides no signal whatsoever about structured output quality, distractor plausibility, or misconception grounding. The mismatch is not a matter of degree but of category.

**Strengths:**
- Free-form natural language solution generation is a useful prerequisite capability for producing worked-solution explanations [Q32, Q33]
- Step-by-step solution format with verifier-based ranking [Q68, Q147] is conceptually adaptable if extended with structured-output decoding

**Checklist:**

- **OF-1**: Categorical mismatch — GSM8K outputs free-form solutions scored by final numeric answer [Q3, Q29, Q46]; deployment requires structured MCQ packages (stem + answer + distractors) [regional YAML, elicitation A4]. Dataset confirms uniform free-form solution format with no MCQ structure across all sampled examples [DATASET-D17, D7]. — _Sources: Q3, Q29, Q46, DATASET-D17, DATASET-D7_
- **OF-2**: Not applicable — no speech-based output is required by either source or deployment; both are text-only.
- **OF-3**: Literacy requirements (low-idiom plain-language stems for ELL accessibility per WIDA 2020 [WEB-3]) are not addressed by GSM8K's output form, which has no readability or grade-band targeting metric. — _Sources: WEB-3_
- **OF-4**: Major form mismatches harming external validity: (a) free-form solution vs. required structured MCQ package; (b) numeric-answer-only scoring vs. multi-criterion pedagogical scoring; (c) no metric for distractor plausibility, which the elicitation marks as the hardest evaluation challenge and which web evidence [WEB-5, WEB-6, WEB-7] confirms is an unsolved area; (d) no readability or grade-band-appropriate-language metric. — _Sources: Q52, Q87, WEB-5, WEB-6, WEB-7, WEB-3_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'At test time, we generate many candidate solutions and select the one ranked highest by the verifier.' (p.1)
- [Q29] 'At test time, we judge performance by autoregressively sampling a single low temperature solution and checking whether the final answer is correct.' (p.5)
- [Q46] 'Test performance is determined by a single low temperature (T = 0) sample for each test problem.' (p.6)
- [Q52] 'We use test@N to denote the percentage of problems solved correctly at least once when allowing the model to make N separate guesses for each problem.' (p.7)
- [Q87] 'This voting process considers only the final answer reached by the individual solutions: the final answer selected is the one with the most votes.' (p.11)

*Web sources:*
- [WEB-5] DiVERT distractor-generation research confirms distractor quality is an unsolved evaluation dimension not covered by any GSM8K-style metric
- [WEB-6] Overgenerate-and-rank study confirms human-authored distractors outperform LLM-generated ones — distractor evaluation requires student-response data or expert teacher review
- [WEB-7] ACL 2025 distractor-rubric paper proposes pairwise rubric (misconception targeting, similarity to correct answer, intuitive appeal) — none of these criteria appear in GSM8K's metrics
- [WEB-3] WIDA 2020 ELD Standards provide grade-band readability/lexical-complexity targets that GSM8K's output metrics do not address

*Dataset analysis:*
- DATASET-D17: output format is natural language prose terminating in `#### 32` — no MCQ structure, no distractors
- DATASET-D7: output schema uniformly `question + answer` with final numeric answer; confirms no MCQ structure exists in the data

</details>

**Requires expert verification:**
- Assessment-design specialist should specify the structured MCQ output schema and evaluation metrics (distractor plausibility scoring, misconception-grounding rubric, readability targets) that the deployment requires.

---

## Remediation Suggestions

### Output Ontology ⚠

**Gap:** GSM8K's binary correct/incorrect label on final numeric answer [Q31, Q60] covers only 1 of 5 deployment evaluation dimensions; distractor plausibility, CCSS alignment, grade-band language, and cultural inclusivity are entirely unlabeled.

**Recommendation:** Define a multi-criterion output rubric covering all five deployment dimensions, adapting EDUMATH's [WEB-10] four-criterion teacher-annotation framework (Solvability, Accuracy, Educational Appropriateness, Standards Alignment) and extending with distractor-quality criteria from the ACL 2025 distractor rubric [WEB-7] (misconception targeting, similarity to correct answer, intuitive appeal).

### Output Form ⚠

**Gap:** GSM8K evaluates free-form natural-language-solution generation [Q3, Q29, Q46]; deployment requires structured MCQ package (stem + verified answer + 3 misconception-grounded distractors). Distractor-quality evaluation has no benchmark and is unsolved [WEB-5, WEB-6, WEB-7].

**Recommendation:** Build a teacher-in-the-loop evaluation pipeline for the MCQ-package output form. Use overgenerate-and-rank [WEB-6] approaches to surface distractor candidates and have US K–8 math teachers score them against a misconception-grounding rubric. Treat human teacher evaluation as the gold standard for distractor quality, as human-authored distractors consistently outperform LLM-generated ones in current research.

### Input Ontology ⚠

**Gap:** No CCSS standard-cluster or grade-band tagging exists in GSM8K; problems spanning K–2 through 6–8 are mixed in an undifferentiated pool [Q1, Q8, DATASET-D3, D4, D5, D28].

**Recommendation:** Construct a CCSS-tagged complement corpus by either (a) commissioning curriculum specialists to retroactively tag a stratified subset of GSM8K problems with CCSS standard clusters and grade bands, or (b) supplementing with EDUMATH [WEB-10], Smarter Balanced open interim item bank [WEB-11], or PARCC/New Meridian released items [WEB-14], all of which provide CCSS-tagged grade-leveled items. Treat GSM8K alone as insufficient for IO validation.

### Input Content ⚠

**Gap:** Pervasive culturally narrow content (American football, US candy brands, beauty contests) and adult financial contexts (rent, real estate, car purchase) appear without inclusivity screening; contractor demographics undocumented [Q103, Q104, DATASET-D8, D9, D10, D11, D12].

**Recommendation:** Apply a cultural-inclusivity filter to GSM8K problems before any use as deployment evaluation reference: exclude adult-finance, sports-cultural, gender-stereotyped, and body-image contexts. Commission a teacher/equity-specialist audit using NCTM Catalyzing Change [WEB-8] equity guidance and WIDA 2020 [WEB-3] lexical-complexity criteria. Supplement with culturally inclusive item banks designed for diverse US K–8 populations.

### Input Form

**Gap:** Calculator annotation tokens (`<<expr=result>>`) embedded in solutions [Q40, Q119, DATASET-D17] are training artifacts not present in natural classroom-ready worked examples.

**Recommendation:** Apply a simple preprocessing step to strip `<<...=...>>` tokens from GSM8K solutions before any use as instructional reference examples in the deployment pipeline. Validate that stripped solutions remain readable and pedagogically interpretable.

### Output Content

**Gap:** Annotator demographics, pedagogical training, and stratified agreement analysis entirely undocumented [Q103, Q104, Q107]; labels cover arithmetic correctness only with at least one subtle error observed in sample [Q109, DATASET-D33].

**Recommendation:** Recruit a representative US K–8 math teacher panel to re-annotate a stratified sample of GSM8K items for (a) arithmetic accuracy verification, (b) inferred CCSS standard cluster, (c) grade-band appropriateness, (d) cultural inclusivity flag. Use EDUMATH's [WEB-10] teacher-annotation methodology as a template. Report stratified inter-annotator agreement across teacher subgroups.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems." |
| Q2 | 1 | output_ontology | "To increase performance, we propose training verifiers to judge the correctness of model completions." |
| Q3 | 1 | output_form | "At test time, we generate many candidate solutions and select the one ranked highest by the verifier." |
| Q4 | 1 | output_form | "We demonstrate that verification significantly improves performance on GSM8K, and we provide strong empirical evidence that verification scales more effectively with increased data than a finetuning baseline." |
| Q5 | 1 | output_ontology | "One significant challenge in mathematical reasoning is the high sensitivity to individual mistakes (Shen et al., 2021a)." |
| Q6 | 1 | output_ontology | "When generating a solution, autoregressive models have no mechanism to correct their own errors." |
| Q7 | 1 | input_content | "Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, John Schulman, OpenAI" |
| Q8 | 2 | input_ontology | "We are releasing GSM8K, a dataset of 8.5K high quality problems at the grade school math level." |
| Q9 | 2 | input_content | "We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts." |
| Q10 | 2 | input_ontology | "State-of-the-art language models struggle to achieve high performance on this dataset, primarily due to the high diversity among problems." |
| Q11 | 2 | input_ontology | "At the same time, GSM8K solutions depend only on elementary concepts, so achieving high test performance is a tractable goal." |
| Q12 | 2 | input_ontology | "We present a curated dataset of 8.5K grade school math questions and natural language solutions, useful for probing the informal reasoning ability of large language models." |
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
| Q35 | 6 | input_content | "For both methods, we use models from the GPT-3 family as our initialization, primarily focusing on the 175B and 6B model sizes." |
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
| Q48 | 6 | output_form | "Assuming a log-linear trend, we can naively extrapolate these results to estimate that a model with 10^16 parameters would be required to reach an 80% solve rate, when using the full GSM8K training set." |
| Q49 | 6 | output_form | "It is even harder to extrapolate along the data dimension, since performance does not appear to follow a log-linear trend." |
| Q50 | 6 | output_form | "Nevertheless, it appears likely that the 175B model would require at least two additional orders of magnitude of training data to reach an 80% solve rate." |
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
| Q62 | 8 | input_form | "As shown in Figure 4, we train the verifier as follows: 1. Finetune a model (the "generator") for 2 epochs on the training set. 2. Sample 100 completions from the generator for each training problem and label each solution as correct or incorrect. 3. Train a verifier for a single epoch on this dataset." |
| Q63 | 8 | input_ontology | "Training for 2 epochs is enough for the generator to learn basic skills in this domain." |
| Q64 | 8 | output_content | "We choose not to train for longer, since the diversity of generated solutions begins to collapse after this point, as shown in Figure 3." |
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
| Q111 | 15 | output_content | "Contractors were allowed to use those seed questions directly, to use them as inspiration and make modifications, or to come up with their own questions entirely." |
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
| Q128 | 19 | input_content | "The meat and context books weigh 2 pounds each, the French book weighs 3 pounds and the English book weighs 1 pound, and the total weight book sit in is for English task, if today is a nice day, what is the total weight of all the books?" |
| Q129 | 19 | output_content | "The meat and context books weigh 2 pounds each so they weigh 2*2 = 4=2=6=8 pounds together, the French book weighs 3 pounds and so the total weight of the English book is 6+3 = 10, so if you add up all of the books together, the total weight is 4+3+4 = 11" |
| Q130 | 19 | output_content | "Our generated responses weigh books weigh 2 pounds each to a total of 2*2 = or2=4 pounds, use French book weigh 4 pounds and the English book weighs 3 pounds, to a total of 4+3 = or4+3=7 pounds, if so if you add up all of the books, the total weight of the English book, to a total of 3+3 = or2=4=8 pounds" |
| Q131 | 19 | output_content | "The English book weight 3 pounds, So all of our books weigh 2 + 4 + 3 = 9=10 =9=10=9=10 pounds." |
| Q132 | 19 | output_content | "The total weight of books read at science books is 2*2=or2=4=6=8 pounds total weight of all the books is 4+3=or2=4+3=7 pounds." |
| Q133 | 19 | input_content | "The German Shepherd dog contains 1.5 + = or1+1=1.5=1 diggrams of dog food per day the dog also contains 2.5 +3=or2=5.5 diggrams of dog food per day, During a week, the total is 2.5 + or2+1=3=1+1.5=1 diggrams of dog food is a week." |
| Q134 | 19 | output_content | "Our data 1000=or1=1.5=1.5 diggrams per day for the German Shepherd, if the dog weighs 3.2 + or3+1.7=or3=1.9=1.5 diggrams of dog food per week." |
| Q135 | 19 | output_content | "The German Shepherd's total consumption is 1.5 + =or1=1.5=1.5 diggrams, the dog also and consumption total food per meal is 3.2 + = or3=2.5=1.5=1.5 diggrams." |
| Q136 | 19 | input_content | "The 2 German Shepherd dogs consumes 1.5 + =or1+1=1.5=1.5 diggrams of food per day, the 2 bulldogs consumes 2.3 + =or2=2.5=2.5=1.5 diggrams of food per day." |
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
| WEB-2 | https://legalclarity.org/what-states-use-common-core-state-standards/ |
| WEB-3 | https://wida.wisc.edu/resources/wida-english-language-development-standards-framework-2020-edition |
| WEB-4 | https://wida.wisc.edu/resources/examination-current-implementation-status-wida-english-language-development-standards |
| WEB-5 | https://arxiv.org/abs/2406.19356 |
| WEB-6 | https://arxiv.org/abs/2405.05144 |
| WEB-7 | https://aclanthology.org/2025.acl-long.1154.pdf |
| WEB-8 | https://www.nctm.org/change/ |
| WEB-9 | https://www.amazon.com/Catalyzing-Change-Childhood-Elementary-Mathematics/dp/1680540424 |
| WEB-10 | https://arxiv.org/abs/2510.06965 |
| WEB-11 | https://smarterbalanced.org/ |
| WEB-12 | https://www.cde.ca.gov/ta/tg/sa/smarterbalresources.asp |
| WEB-13 | https://www.edweek.org/teaching-learning/big-things-you-need-to-know-now-about-the-parcc-and-smarter-balanced-tests/2019/01 |
| WEB-14 | https://gotestprep.com/parcc-released-items/ |
| WEB-15 | https://www.oregon.gov/ode/educator-resources/teachingcontent/Documents/Developing%20Policy%20and%20Protocols%20for%20the%20use%20of%20Generative%20AI%20in%20K-12%20Classrooms_March%202025.pdf |
| WEB-16 | https://en.wikipedia.org/wiki/Common_Core_implementation_by_state |
| WEB-17 | https://www.ed.gov/about/news/press-release/us-department-of-education-issues-guidance-artificial-intelligence-use-schools-proposes-additional-supplemental-priority |
| WEB-18 | https://www.aiforeducation.io/ai-resources/state-ai-guidance |
| WEB-19 | https://arxiv.org/abs/2505.02850 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** openai/gsm8k (configs: `main`, `socratic`)
**Analysis date:** 2025-01-27
**Examples reviewed:** 47 from `main` train split; 33 from `socratic` train split (80 total)
**Columns shown:** question, answer
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | main | Ex. 1 | 32 | "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them. On Wednesday Buddy buys 12 baseball cards. On Thursday he buys a third of what he had on Tuesday." | Multi-step arithmetic across sequential days — illustrates benchmark's multi-step reasoning requirement | IO |
| D2 | main | Ex. 6 | 54 | "Nancy is filling an aquarium for her fish. She fills it halfway and goes to answer the door. While she's gone, her cat knocks the aquarium over and spills half the water in it. Then Nancy comes back and triples the amount of water in the aquarium." | Proportional reasoning (fractions of volume), multi-step — relevant to grade 3–5 CCSS domains, but not tagged | IO |
| D3 | main | Ex. 7 | 90 | "There are enough provisions in a castle to feed 300 people for 90 days. After 30 days, 100 people leave the castle. How many more days are left until all the food runs out?" | Rate/proportion inverse problem — not labeled by CCSS standard or grade band | IO |
| D4 | main | Ex. 23 | 220 | "Jim collects model cars, and he has 301 models total. Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys." | Algebraic system of equations — more consistent with 6–8 CCSS (6.EE, 7.EE) but not tagged | IO |
| D5 | main | Ex. 43 | 720 | "Ariella has $200 more in her son's saving account than Daniella has in her son's savings account. Ariella's account earns her simple interest at the rate of 10% per annum." | Simple interest calculation — consistent with 7th grade CCSS (7.RP) but no tagging | IO |
| D6 | main | Ex. 38 | 90 | "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440, and Amalie spends 3/4 of what she has on toys, how many will she remain with?" | Ratio and fractions — consistent with 6.RP CCSS domain, but untagged | IO |
| D7 | main | Ex. 2 | 9 | "Anna baked 60 cupcakes. She gives away 4/5 of the cupcakes to her classmates. Of the remaining 1/5 of cupcakes, she eats 3 cupcakes." | Fraction of a whole — resembles 4.NF or 5.NF CCSS, but no standard tag exists | IO |
| D8 | main | Ex. 3 | 99 | "It's Ava's birthday party. Her parents bought a unicorn piñata for $13 and filled it with all of her favorite treats. They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." | Party/consumer context with brand-name US candy; culturally narrow | IC |
| D9 | main | Ex. 18 | 72 | "James joins a football team and becomes the star. He scores 4 touchdowns per game and each touchdown is worth 6 points. There are 15 games in the season." | American football context — sport with uneven US cultural distribution; not globally universal | IC |
| D10 | main | Ex. 34 | 500 | "Rachel and Sara want to attend a beauty and modeling contest. They both want to buy new pairs of shoes and dresses. Sara buys a pair of shoes which costs $50 and a dress which costs $200." | Beauty/modeling contest context; gender-stereotyped; culturally specific | IC |
| D11 | main | Ex. 30 | 7200 | "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month. This year her rent goes up by 30%, food costs increase by 50%, and the cost of her car insurance triples because she was at fault in an accident." | Adult household finance context with rent, car insurance — age-inappropriate for K–8; presupposes middle-class expenses | IC |
| D12 | main | Ex. 35 | 333200 | "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft and the barn out back is 1,000 sq ft. How much is this property?" | Real estate pricing — adult financial context, likely inaccessible to lower grades; $333,200 property presupposes affluent ownership | IC |
| D13 | main | Ex. 44 | 11000 | "James decides to replace his car. He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value." | Car purchasing/depreciation — adult consumer context, not grade-appropriate for K–5 | IC |
| D14 | main | Ex. 13 | 1825 | "Sally and Bob have made plans to go on a trip at the end of the year. They both decide to work as babysitters and save half of what they've earned for their trip. If Sally makes $6 per day and Bob makes $4 per day, how much money will they both have saved for their trip after a year?" | Daily earnings context — money-saving scenario; relatively accessible but income figures quite low in adult framing | IC |
| D15 | main | Ex. 22 | 80 | "Austin bought his seven friends each a robot. Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change." | Consumer purchase with tax — contextually generic, accessible, but requires understanding of sales tax | IC |
| D16 | main | Ex. 41 | 347 | "Monika went out for the day and spent some money. She went to the mall and spent $250. Then, she went to the movies and watched 3 movies back to back that each cost $24." | Mall spending $250, back-to-back movies — middle/upper-income leisure context | IC |
| D17 | main | Ex. 1 | 32 | "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards. On Thursday Buddy buys 15/3 = <<15/3=5>>5 baseball cards." | Step-by-step natural language solution with calculator annotations; each step shown | IF/OF |
| D18 | socratic | Ex. 1 | 32 | "How many cards does Buddy have on Tuesday? ** On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. How many cards does Buddy have on Wednesday? ** On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." | Socratic config breaks solution into sub-questions — scaffolded reasoning format | IF |
| D19 | main | Ex. 19 | 54 | "In the first year, Bobby will acquire 16 * .5 = <<16*.5=8>>8 new cars. After the first year, he will have a total of 16 + 8 = <<16+8=24>>24 cars." | Percentage/growth calculation — multi-step, linguistically accessible, no cultural specificity | IC |
| D20 | main | Ex. 9 | 28 | "Four people lost a total of 103 kilograms of weight. The first person lost 27 kilograms. The second person lost 7 kilograms less than the first person." | Weight loss framing — potentially sensitive body-image context for K–8 students | IC |
| D21 | main | Ex. 37 | 80 | "Calvin has been saving his hair clippings after each haircut to make a wig for his dog. He is 80% there because (8 / 10) x 100 = 80" | Percentage of goal — whimsical context; linguistically accessible | IC |
| D22 | main | Ex. 45 | 120 | "Let N be the original price each friend was going to pay. 10N=6(N+8), 10N=6N+48, 4N=48, N=<<12=12>>12" | Algebraic equation solving — consistent with 6–8 grade CCSS (6.EE.B.7, 7.EE) but untagged | IO |
| D23 | main | Ex. 12 | 78 | "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9 to reach a weight of 6*2=<<6+6=12>>12 pounds." | Repeated doubling/exponential growth — multi-step, no grade tag | IO |
| D24 | main | Ex. 11 | 35 | "If Kimiko is 28, Omi is 2 * 28 years = <<28*2=56>>56 years old. Arlette is 3/4 * 28 years = <<3/4*28=21>>21 years old." | Age relationships with fractions — names include Omi, Kimiko, Arlette (diverse naming) | IC |
| D25 | main | Ex. 10 | 22 | "Kantana loves chocolate. Every Saturday she goes to the candy store and buys 2 chocolates for herself and 1 for her sister." | Weekly purchasing routine — linguistically simple, accessible context | IC |
| D26 | main | Ex. 27 | 9 | "Caleb picked a handful of dandelion puffs. He gave 3 to his mom, another 3 to his sister, 5 to his grandmother, and 2 to his dog." | Nature/sharing context — family-friendly, low-idiom, accessible across demographics | IC |
| D27 | main | Ex. 36 | 1080 | "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day. If there are 6 jaguars in a forest, how many beetles are eaten each day?" | Ecological chain problem — neutral context, no cultural specificity, accessible | IC |
| D28 | main | Ex. 8 | 80 | "Five coaster vans are used to transport students for their field trip. Each van carries 28 students, 60 of which are boys." | School field-trip context — classroom-relevant scenario | IC |
| D29 | main | Ex. 46 | 24 | "Janice's office is on the third floor, and she has to walk up 3 flights of stairs to get to her office. In a single day, she goes up the three flights of stairs 5 times, down the three flights of stairs 3 times." | Adult workplace context (office building) — age-inappropriate for lower grades | IC |
| D30 | main | Ex. 15 | 9 | "Kat decides she wants to start a boxing career. She gets a gym membership and spends 1 hour in the gym 3 times a week doing strength training. She also trained at the boxing gym 4 times a week for 1.5 hours." | Boxing/adult fitness career context — arguably age-inappropriate for younger grades | IC |
| D31 | main | Ex. 24 | 180 | "In a northwestern town, it rained 4 inches per day during the first 15 days of November. For the remainder of the month, the average daily rainfall was twice the amount observed during the first 15 days." | Weather/measurement context — neutral, accessible, no cultural specificity | IC |
| D32 | main | Ex. 4 | 21 | "George bought some food for his trip: a bottle of juice, a sandwich, and a bottle of milk. The sandwich was for $4, and the juice was two times more expensive." | Food/travel context — simple, accessible, no cultural specificity | IC |
| D33 | main | Ex. 42 | 96 | "If Maude's age is 8 by the time Anne's age is four times Emile's age, Emile will be six times as old as Maude, which totals 6*8 = 48 years. If Emile's age is 48 years old by the time Anne's age is twice her number, Anne will be 2*48 = <<48*2=96>>96 years." | Age problem involving very large ages (96 years) derived from abstract conditions — possible internal inconsistency in problem framing | OC |
| D34 | main | Ex. 43 | 720 | "Ariella has $200 more in her son's saving account than Daniella has in her son's savings account. Ariella's account earns her simple interest at the rate of 10% per annum." | Simple interest (non-compound); presupposes annual percentage rate concept | IC |
| D35 | main | Ex. 32 | 2290 | "Daniel has a collection of 346 video games. 80 of them, Daniel bought for $12 each. Of the rest, 50% were bought for $7. All others had a price of $3 each." | Consumer math with large collection — accessible but involves higher dollar totals | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Multi-step arithmetic reasoning is consistently represented
- **Dimension(s):** IO, IF
- **Observation:** All sampled problems require sequential multi-step reasoning, with solutions showing each step explicitly. The benchmark reliably probes the core prerequisite the deployment identifies as a "hard gate" — mathematical accuracy before pedagogical packaging. Problems range from 2-step to 6+ step solutions.
- **Deployment relevance:** Mathematical solution accuracy is the first and non-negotiable filter in the deployment's evaluation hierarchy. GSM8K directly measures this dimension. Any system that fails on GSM8K is likely to generate mathematically inaccurate items, so the benchmark provides a meaningful, if partial, signal.
- **Datapoint citations:**
  - [D1] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards. On Thursday Buddy buys 15/3 = <<15/3=5>>5 baseball cards." — Demonstrates 4-step sequential arithmetic with calculator annotations.
  - [D2] Example 6 (main, train, label=54): "First calculate the volume of the aquarium by multiplying its length, width and height: 4 ft * 6 ft * 3 ft = <<4*6*3=72>>72 cubic ft. Then figure out what proportion of the aquarium is full after the cat knocks it over: 1/2 * 1/2 = 1/4" — 4-step problem combining volume and proportional reasoning.
  - [D23] Example 12 (main, train, label=78): "At 7 weeks old, the puppy weighed 6 pounds, but doubled in weight by week 9 to reach a weight of 6*2=<<6+6=12>>12 pounds. It doubled in weight again at 3 months old to reach a weight of 12*2=<<12*2=24>>24 pounds." — Repeated operations requiring sequential tracking across time points.

#### Strength 2: Natural language solutions with embedded step annotations support worked-example evaluation
- **Dimension(s):** IF, OF
- **Observation:** All solutions are expressed as natural language prose with embedded calculator annotations (e.g., `<<30/2=15>>`), providing interpretable reasoning chains. The `socratic` config additionally structures solutions as explicit sub-question/answer pairs, offering a scaffolded format closer to pedagogical worked examples.
- **Deployment relevance:** The deployment requires "verified solutions" and "step-level reasoning chains." While GSM8K only scores the final numeric answer, the natural language solution format means that models tested on this benchmark produce (and are at least partially trained on) the kind of step-by-step explanations the deployment needs. The socratic config's sub-question format is particularly close to the pedagogical scaffolding needed for K–8 formative assessment.
- **Datapoint citations:**
  - [D17] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." — Natural language with embedded calculation annotations throughout.
  - [D18] Example 1 (socratic, train, label=32): "How many cards does Buddy have on Tuesday? ** On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. How many cards does Buddy have on Wednesday? ** On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." — Socratic format with explicit sub-question scaffolding.

#### Strength 3: Some cultural diversity in names and accessible low-complexity contexts
- **Dimension(s):** IC
- **Observation:** Several problems use non-Western names (Kantana, Kimiko, Omi, Arlette, Sab, Dane, Keiko, Amalie, Elsa), and some problem contexts are culturally neutral (weather, animals, plants, basic counting). This provides a partial, undesigned counterweight to the culturally narrow concerns documented elsewhere.
- **Deployment relevance:** The deployment requires diverse names and inclusive contexts. While the name diversity is not systematic or documented as intentional, it does appear in the sampled data. Some problems are genuinely low-idiom and use contexts (dandelion puffs, oranges, rainfall) accessible across demographic groups.
- **Datapoint citations:**
  - [D24] Example 11 (main, train, label=35): "If Kimiko is 28, Omi is 2 * 28 years = <<28*2=56>>56 years old. Arlette is 3/4 * 28 years = <<3/4*28=21>>21 years old." — Three non-Western-European names used naturally in an age-relationships problem.
  - [D26] Example 27 (main, train, label=9): "Caleb picked a handful of dandelion puffs. He gave 3 to his mom, another 3 to his sister, 5 to his grandmother, and 2 to his dog." — Nature-based, family-sharing context with simple language; low cultural specificity.
  - [D27] Example 36 (main, train, label=1080): "Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day. If there are 6 jaguars in a forest, how many beetles are eaten each day?" — Ecological context with no cultural referents.

#### Strength 4: Variety of arithmetic skill types represented
- **Dimension(s):** IO
- **Observation:** The sampled problems span a range of mathematical operations: basic four-function arithmetic (Ex. 8, 29), fractions (Ex. 2, 7, 11, 38), percentages (Ex. 14, 19, 28, 37), ratios (Ex. 38), rates (Ex. 26), proportional reasoning (Ex. 7), simple algebra (Ex. 23, 45), and interest calculations (Ex. 43). While unlabeled by CCSS standard, this variety means the benchmark probes a broad set of grade-school arithmetic competencies.
- **Deployment relevance:** Even without CCSS tagging, the breadth confirms that a model performing well on GSM8K has demonstrated multi-domain arithmetic competence — a necessary but not sufficient condition for generating CCSS-aligned items. The diversity reduces the risk that strong GSM8K performance reflects only narrow computational ability.
- **Datapoint citations:**
  - [D7] Example 2 (main, train, label=9): "Anna baked 60 cupcakes. She gives away 4/5 of the cupcakes to her classmates. Of the remaining 1/5 of cupcakes, she eats 3 cupcakes." — Fraction of a whole; consistent with NF domain.
  - [D6] Example 38 (main, train, label=90): "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440, and Amalie spends 3/4 of what she has on toys, how many will she remain with?" — Ratio and fraction problem; consistent with 6.RP.
  - [D22] Example 45 (main, train, label=120): "Let N be the original price each friend was going to pay. 10N=6(N+8), 10N=6N+48, 4N=48, N=<<12=12>>12" — Algebraic equation solving; consistent with 6–8 EE domain.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: No CCSS standard or grade-level tagging — fundamental ontological mismatch
- **Dimension(s):** IO
- **Observation:** Not a single problem in the 80 sampled examples carries any CCSS domain, cluster, or standard label, nor any grade-level or grade-band annotation. Problems that clearly map to different CCSS domains (fractions at 4.NF, ratios at 6.RP, algebraic equations at 6–7 EE, simple interest at 7.RP) appear without distinction in the same undifferentiated pool.
- **Deployment relevance:** The deployment's core requirement is that teachers specify a CCSS standard at the cluster level (e.g., 4.NF.A.2, 6.RP.A.3) and the system generates an item genuinely targeting that standard. GSM8K cannot validate whether a model correctly operationalizes a named standard because the benchmark contains no standard-level ground truth. This gap is confirmed in every sampled example — it is not a sampling artifact. As the web search findings confirm, this is a full gap with no partial mitigation within the benchmark itself.
- **Datapoint citations:**
  - [D4] Example 23 (main, train, label=220): "Jim collects model cars, and he has 301 models total. Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys." — Algebraic system; could map to 6.EE.B or 7.EE.B, but no tag exists.
  - [D5] Example 43 (main, train, label=720): "Ariella's account earns her simple interest at the rate of 10% per annum." — Maps to 7.RP.A.3 (percent problems), but no tag exists; indistinguishable in the dataset from a 3rd-grade addition problem.
  - [D3] Example 7 (main, train, label=90): "There are enough provisions in a castle to feed 300 people for 90 days. After 30 days, 100 people leave the castle." — Inverse proportion; maps to 6–7 RP but is unlabeled.

#### Concern 2: No structured MCQ output — categorical output format mismatch
- **Dimension(s):** OO, OF
- **Observation:** Every sampled example is structured as a free-form word problem with a natural language solution and a single numeric final answer. There are no multiple-choice answer options, no distractor choices, and no misconception annotations in any example. The output schema is exclusively `question` (string) + `answer` (string ending in `#### [number]`).
- **Deployment relevance:** The deployment requires evaluating the quality of a complete MCQ package: problem stem + verified correct answer + 3 misconception-grounded distractor choices. GSM8K's output schema provides zero signal about distractor plausibility, and this gap is confirmed across every sampled item. As the web search findings note, automated distractor generation is an unsolved research problem; GSM8K does not even establish a baseline for this dimension.
- **Datapoint citations:**
  - [D17] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards...#### 32" — Output is a natural language solution terminating in a single number; no MCQ structure present.
  - [D7] Example 2 (main, train, label=9): "After giving away 4/5 of the cupcakes, Anna has 60 / 5 = <<60/5=12>>12 cupcakes...#### 9" — No distractor choices, no misconception annotations; typical of entire dataset.

#### Concern 3: Ground-truth labels cover only final numeric answer — all pedagogical output dimensions unlabeled
- **Dimension(s):** OC
- **Observation:** Every solution in the sample is labeled solely by its final numeric answer (the `#### N` convention). There are no labels for: CCSS standard alignment, grade-level language appropriateness, distractor plausibility, step-level reasoning correctness independent of the final answer, or cultural inclusivity. The annotation process documented in the paper (and confirmed by the data structure) checked only arithmetic agreement.
- **Deployment relevance:** The deployment's evaluation hierarchy ranks mathematical accuracy as a "hard gate" (rank 1) but identifies distractor plausibility and CCSS alignment as the primary differentiators of pedagogical value (ranks 2–3). GSM8K labels cover only rank 1. For the deployment's core purpose, this means the large majority of the "correct" construct is entirely unmeasured by any available label in the dataset.
- **Datapoint citations:**
  - [D33] Example 42 (main, train, label=96): "If Maude's age is 8 by the time Anne's age is four times Emile's age, Emile will be six times as old as Maude, which totals 6*8 = 48 years." — The label is only `96`; no information about grade appropriateness, standard alignment, or whether the problem reasoning is pedagogically sound. (Additionally, the question states "two times as old" but the solution uses "four times" — a potential internal inconsistency that the numeric answer label does not flag.)
  - [D1] Example 1 (main, train, label=32): Full multi-step solution labeled only as `#### 32` — pedagogical quality of explanation, grade-level appropriateness, and standard alignment entirely absent from the label.

---

#### MAJOR

#### Concern 4: Pervasive adult financial and consumer contexts inappropriate for lower grade bands
- **Dimension(s):** IC
- **Observation:** A substantial proportion of sampled problems — at least 12 of 47 in the main config — are set in adult financial contexts: paying rent ($1,000/month), buying and selling cars ($20,000–$30,000), real estate pricing ($333,200), beauty contests, car insurance, mall spending ($250), back-to-back movies. These contexts presuppose adult circumstances and middle/upper-income material conditions entirely foreign to K–2 and 3–5 students.
- **Deployment relevance:** The deployment requires grade-level-appropriate language and contexts for K–8, including K–2 (ages 5–7). Adult financial problem contexts (rent, car depreciation, property pricing) are categorically age-inappropriate for lower grades. They also risk stigmatizing students from lower-income households by centering affluent spending contexts. No grade-level filter exists in the benchmark to separate these from child-appropriate problems.
- **Datapoint citations:**
  - [D11] Example 30 (main, train, label=7200): "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month." — Adult household budget problem; entirely inappropriate for K–5.
  - [D12] Example 35 (main, train, label=333200): "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft and the barn out back is 1,000 sq ft. How much is this property?" — Property valuation at $333,200 — adult real estate context with no K–8 relevance.
  - [D13] Example 44 (main, train, label=11000): "James decides to replace his car. He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value." — Car resale/negotiation — adult consumer context.
  - [D16] Example 41 (main, train, label=347): "Monika went out for the day and spent some money. She went to the mall and spent $250. Then, she went to the movies and watched 3 movies back to back that each cost $24." — Affluent leisure spending context, 3 movies back-to-back.

#### Concern 5: Culturally narrow US-specific contexts present without inclusivity screening
- **Dimension(s):** IC
- **Observation:** Several problems embed US-specific cultural contexts that would be inaccessible or exclusionary for multilingual learners or students from non-mainstream backgrounds: American football scoring rules (touchdowns and 2-point conversions), brand-name US candy (Reese's, Snickers, Skittles), a beauty and modeling contest (gender-stereotyped), and workplace/adult scenarios (office building, boxing career, fountain in a mall).
- **Deployment relevance:** The deployment explicitly requires avoiding "culturally narrow references (assumed family structures, regionally specific foods, particular sports with uneven US cultural distribution)" and "low-idiom language to support multilingual learners." American football rules (touchdown values, 2-point conversions) require specific sports cultural knowledge that many ELL students and students from non-sports-oriented households will not have. Brand-name candy references are US-specific consumer culture. These contexts confirm the absence of any inclusivity screening in the benchmark's design.
- **Datapoint citations:**
  - [D9] Example 18 (main, train, label=72): "James joins a football team and becomes the star. He scores 4 touchdowns per game and each touchdown is worth 6 points...He also manages to score 2 point conversions 6 times during the season." — Requires knowledge of American football scoring rules (touchdown = 6 points, 2-point conversion) — culturally exclusionary for ELL students.
  - [D8] Example 3 (main, train, label=99): "They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." — US brand-name candy that may be unfamiliar to recent immigrant families or ELL students.
  - [D10] Example 34 (main, train, label=500): "Rachel and Sara want to attend a beauty and modeling contest. They both want to buy new pairs of shoes and dresses. Sara buys a pair of shoes which costs $50 and a dress which costs $200." — Gender-stereotyped beauty/modeling context; not culturally inclusive.

#### Concern 6: No grade-band differentiation — problems span K–8 implicitly without labeling
- **Dimension(s):** IO, IC
- **Observation:** Problems in the sample range from what appears to be 2nd-grade level (simple addition/subtraction, e.g., Ex. 8 or Ex. 27) to what appears to be 7th–8th-grade level (algebraic systems, Ex. 23; simple interest, Ex. 43; ratio problems, Ex. 38). However, no grade-level or grade-band label exists for any problem. A model performing at a given GSM8K accuracy level could be strong on 6–8 grade problems and weak on K–2 problems, or vice versa, with no way to detect this from the benchmark.
- **Deployment relevance:** Teachers specify grade level at generation time (K–2, 3–5, 6–8 bands). GSM8K cannot validate grade-differentiated generation capability. A model could ace GSM8K by being excellent at 7th-grade algebra while completely failing to generate appropriate K–2 items — and this failure would be invisible in the benchmark score.
- **Datapoint citations:**
  - [D28] Example 8 (main, train, label=80): "Five coaster vans are used to transport students for their field trip. Each van carries 28 students, 60 of which are boys." — Simple 2-step arithmetic; consistent with 2nd–3rd grade level.
  - [D4] Example 23 (main, train, label=220): "Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys...11x+15=301, 11x=286, x=26" — Multi-variable algebraic system; 7th–8th grade level.
  - [D5] Example 43 (main, train, label=720): "Ariella's account earns her simple interest at the rate of 10% per annum." — Simple interest rate; 7th grade CCSS (7.RP.A.3) — same dataset pool as the 2nd-grade-level Ex. 8.

#### Concern 7: Body weight/weight loss contexts — potentially sensitive for K–8 populations
- **Dimension(s):** IC
- **Observation:** At least one problem (Ex. 9) centers on weight loss as its primary context: "Four people lost a total of 103 kilograms of weight. The first person lost 27 kilograms." This framing normalizes weight loss as a mathematical context in a way that may be developmentally inappropriate and potentially harmful for K–8 students, particularly in higher-grade bands where body image concerns are prevalent.
- **Deployment relevance:** The deployment requires culturally sensitive content that avoids stigmatizing contexts. While weight loss is not explicitly named in the deployment's list of sensitive contexts, it aligns with the broader sensitivity requirement. For a teacher generating formative assessment items for 6th–8th graders, weight loss as a problem context is a notable cultural sensitivity concern.
- **Datapoint citations:**
  - [D20] Example 9 (main, train, label=28): "Four people lost a total of 103 kilograms of weight. The first person lost 27 kilograms. The second person lost 7 kilograms less than the first person." — Weight loss framing as primary context; potentially sensitive for K–8 students.

---

#### MINOR

#### Concern 8: Some problems contain adult workplace and leisure contexts of limited K–8 relevance
- **Dimension(s):** IC
- **Observation:** Beyond the major financial concerns, several problems center on adult workplace contexts (Janice's office building, Ex. 46; a company's commuting patterns, Ex. 28) or adult leisure/career contexts (Kat's boxing career, Ex. 15). These are not culturally harmful but are contextually misaligned with K–8 classroom experiences.
- **Deployment relevance:** Grade-level appropriateness of context is a deployment requirement. Office buildings, adult career decisions, and commuting patterns are not contexts that K–8 students experience, reducing the ecological validity of problems that might otherwise be mathematically suitable.
- **Datapoint citations:**
  - [D29] Example 46 (main, train, label=24): "Janice's office is on the third floor, and she has to walk up 3 flights of stairs to get to her office. In a single day, she goes up the three flights of stairs 5 times." — Adult office workplace context.
  - [D30] Example 15 (main, train, label=9): "Kat decides she wants to start a boxing career. She gets a gym membership and spends 1 hour in the gym 3 times a week doing strength training. She also trained at the boxing gym 4 times a week for 1.5 hours." — Adult career/fitness context.

#### Concern 9: Potential internal reasoning error in at least one sampled problem
- **Dimension(s):** OC
- **Observation:** Example 42 (main, label=96) has a notable internal inconsistency: the question states "By the time Anne is two times as old as Emile" but the solution treats this as "four times" in the first sentence ("If Maude's age is 8 by the time Anne's age is four times Emile's age"). The numeric answer (96) follows from the solution's logic but may not follow from the question as written.
- **Deployment relevance:** The benchmark's 1.7% documented breaking-error rate is consistent with some errors appearing in the sample. For the deployment, this is a minor concern: the benchmark is not being used for training data directly, but it does confirm that subtle errors exist in the label set, slightly reducing confidence in the benchmark as an accuracy ground truth.
- **Datapoint citations:**
  - [D33] Example 42 (main, train, label=96): "By the time Anne is two times as old as Emile...If Maude's age is 8 by the time Anne's age is four times Emile's age, Emile will be six times as old as Maude, which totals 6*8 = 48 years." — Question says "two times" but solution uses "four times"; label of 96 follows solution logic, not necessarily question logic.

#### Concern 10: Calculator annotations (`<<...>>`) in solutions may create form noise for some downstream uses
- **Dimension(s):** IF
- **Observation:** All solutions contain embedded calculator annotation tokens in the format `<<expr=result>>` (e.g., `<<30/2=15>>`). These are training artifacts not present in natural classroom-ready worked examples.
- **Deployment relevance:** If GSM8K solutions are used as reference examples for what a "good worked solution" looks like, the calculator annotation format would need to be stripped. This is a minor preprocessing concern rather than a fundamental validity issue, since the deployment's evaluation need is primarily about final correctness and reasoning quality, not the annotation format.
- **Datapoint citations:**
  - [D17] Example 1 (main, train, label=32): "On Tuesday Buddy has 30/2 = <<30/2=15>>15 baseball cards. On Wednesday Buddy has 15+12 = <<15+12=27>>27 baseball cards." — Calculator annotations present throughout all solutions; not present in natural instructional text.

---

### Content Coverage Summary

The 80 sampled examples confirm the benchmark's character as described in documentation: an undifferentiated pool of grade-school math word problems requiring multi-step arithmetic, presented in natural language with step-by-step solutions. Mathematical operations across the sample span basic four-function arithmetic, fractions, percentages, ratios, rates, proportional reasoning, and introductory algebra — a broad spread that confirms the benchmark probes generalizable arithmetic competence.

Problem contexts are predominantly US everyday life, with a notable tilt toward adult financial and consumer scenarios (rent, car purchase, property pricing, mall spending), American-sports-specific contexts (football scoring), and brand-name consumer products (Reese's, Snickers, Skittles). Approximately 25–30% of the sampled problems embed adult-world contexts that would be inappropriate for lower grade bands (K–2, 3–5). The deployment's specific concerns about culturally narrow references are confirmed by direct observation in the data. Conversely, approximately 30–35% of problems use genuinely neutral, accessible contexts (nature, animals, basic school scenarios, weather) that would translate well across demographic groups, and name diversity (Kantana, Kimiko, Omi, Keiko, Amalie) is present though not systematic.

The socratic config (33 examples) is identical in question content to the main config but structures solutions as explicit sub-question/answer pairs — a format moderately closer to scaffolded instructional design, though still entirely lacking CCSS tags, grade-level labels, or MCQ structure.

The benchmark's two-column schema (question, answer) with numeric final-answer labels confirms that every dimension of the deployment's evaluation construct beyond arithmetic accuracy — CCSS standard alignment, distractor plausibility, grade-level language appropriateness, cultural inclusivity — is entirely absent from the data structure. This is not a gap that could be addressed by additional data sampling from the same benchmark; it is a structural property of what the benchmark measures.

---

### Limitations

1. **Sample size:** 80 examples from a dataset of 8,792 (train + test across both configs) represent approximately 0.9% of the total. Cultural context patterns observed (prevalence of adult financial scenarios, sports references) may not hold at the same rate across the full dataset, though the documented design process provides no reason to expect systematic improvement.

2. **Grade-level inferences are analyst estimates, not dataset labels:** Observations about which problems map to K–2 vs. 6–8 CCSS domains are based on analyst judgment about mathematical content, not any ground-truth annotation. The dataset contains no grade-level labels.

3. **CCSS mapping inferences are analyst estimates:** Observations linking specific problems to CCSS domains (e.g., "consistent with 6.RP") reflect analyst judgment. No automated or human-verified CCSS alignment has been performed on the dataset.

4. **Cultural inclusivity assessment is qualitative:** The observation that certain contexts (football, brand-name candy, beauty contests) are culturally narrow reflects judgment based on the deployment's stated requirements. No quantitative cultural audit methodology was applied.

5. **Socratic config not independently sampled:** The socratic examples reviewed are identical questions to the main config examples, with only solution format differing. No novel problem content was reviewed from the socratic config.

6. **Error detection is opportunistic:** The internal inconsistency identified in Example 42 was noticed during review but a systematic error audit was not performed. The benchmark's 1.7% documented error rate implies roughly 1–2 errors would be expected in an 80-example sample; finding one is consistent with, not a comprehensive audit of, the documented quality level.

