## Deployment Context

We are building an automated logic-checking tool for undergraduate formal reasoning courses at a US university. The tool receives a set of premises and a conclusion expressed in controlled natural language and determines whether the argument is logically valid, invalid, or indeterminate. Our users are American undergraduates taking introductory logic courses. We need to evaluate the LLM's deductive reasoning capabilities.

# Validity Analysis: folio
**Target context:** US Undergraduate Introductory Logic Course — Automated Validity Checker
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ✓ | 4 | Minor gaps | high |
| Output Content | 3 | Moderate gaps | high |
| Output Form ✓ | 4 | Minor gaps | high |
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

FOLIO is a partially valid benchmark for a US undergraduate introductory logic course's automated validity checker. Its three-way label schema (True/False/Unknown) cleanly maps to the course rubric (valid/invalid/indeterminate) — including the course's strict 'invalid = premises entail the negation' definition, which is operationally satisfied by FOLIO's resolution-based inference engine [WEB-3, WEB-4]. The expert-annotated, FOL-engine-verified labels [Q2, Q16, Q57] provide strong ground-truth quality on the FOL portion of the course. However, two structural issues limit overall validity: (1) FOLIO contains no propositional-only subset, leaving the entire first half of the course uncovered (every sampled example uses ∀ or ∃ — DATASET-D1, D2, D4); and (2) the dominant FOLIO input register is naturalistic, Wikipedia-seeded prose with embedded real-world domain knowledge [Q35, DATASET-D7, D9, D14, D25], substantially different from the course's syntactically controlled Hurley-style templates. Reasoning depth also skews deeper than typical course problems [Q60]. Additional concerns include observable annotation errors in the HuggingFace data (DATASET-D27, D28, D29) and a paper-vs-data label-string mismatch ('Unknown' vs 'Uncertain', DATASET-D3). For a tool intended to cover the full course, FOLIO must be supplemented with a propositional-logic benchmark (LogicBench [WEB-1]) and ideally a small course-packet-aligned probe set to bridge the register gap.

## Practical Guidance

### What This Benchmark Measures

FOLIO measures a model's ability to determine, from naturalistic English prose containing first-order logical structure, whether a conclusion is entailed (True), its negation is entailed (False), or neither follows (Unknown). The output ontology (Output Ontology, strong) maps directly to the course's three-way valid/invalid/indeterminate rubric. The output content (Output Content, moderate) is generally high-quality due to expert annotation and FOL-engine verification, though some annotation errors are observable in the public release. For the FOL/second-half portion of the course (covered by Input Ontology and observable in DATASET-D21, D8, D38), FOLIO provides meaningful signal at the higher end of difficulty.

### Construct Depth

FOLIO probes reasoning across deep chains (mode 4 steps, 28.7% at 5+ [Q60]) and a wide AST variety [Q61], so a model scoring well on FOLIO has been tested on combinations of quantifiers, connectives, and chained inferences. However, it does not probe propositional-only reasoning at all (DATASET-D1, D2 confirm universal quantifier presence in every example) and does not probe the syntactically controlled Hurley-style register that dominates the course packet (Input Content is the weakest dimension after Input Ontology). Per-class accuracy is essential because models exhibit systematic bias toward True predictions [Q155, Q156]; overall accuracy can mask poor invalid/indeterminate performance.

### What Else You Need

Three supplementation steps are necessary: (1) Add LogicBench [WEB-1] to cover propositional inference rules (MP, MT, HS, DS, etc.) for the course's first half — this directly addresses the IO gap. (2) Construct a small course-packet-aligned probe set in Hurley-style templates to address the IC register mismatch and validate model performance on the deployment's dominant register. (3) Prefer the 2026 Vampire-cleaned FOLIO split [WEB-6] over the raw HuggingFace release to mitigate the annotation errors observed in OC. Reporting per-class accuracy (especially for False and Unknown) is essential given documented model bias [Q155, Q156, Q157].

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
FOLIO's logical scope aligns with the second half of the deployment course (predicate/first-order logic with quantifiers, connectives, and combinations [Q43, Q138]), and the operator inventory comprehensively covers the FOL portion of the curriculum (DATASET-D21, D8, D38). However, the benchmark contains no quantifier-free or propositional-only subset — every sampled example uses ∀ or ∃ (DATASET-D1, D2, D4), and the documentation treats FOL with quantifiers as the inherent design [Q15, Q63]. Since the course's first half is entirely propositional, FOLIO alone gives zero coverage of roughly half the course's logical scope. Reasoning depth also skews deeper than introductory problems: the mode is 4 steps with 28.7% requiring 5+ [Q60], whereas course-packet problems typically span 1–3 steps. Modal and temporal logic are explicitly excluded from FOLIO [Q139, Q140], which matches the deployment's classical-deductive-only constraint.

**Strengths:**
- FOL operator coverage (∀, ∃, ¬, ∧, ∨, →, =, ⊕) comprehensively matches the second-half course scope [Q138, DATASET-D21, D8]
- Explicit exclusion of modal and temporal logic [Q139, Q140] matches the course's classical-deductive-only scope
- Contains some minimal syllogistic forms structurally close to Hurley templates (e.g., 'No A are B' / 'All C are B') usable for the predicate-logic half (DATASET-D1, D2, D5)

**Checklist:**

- **IO-1**: Deployment requires two categories: (a) propositional-logic problems (truth tables, MP, MT, HS, DS, CD, etc.) for the first half and (b) first-order predicate logic problems with quantifiers and basic syllogistic forms for the second half. The Hurley-style register is dominant across both halves. — _Sources: Q15, Q43_
- **IO-2**: FOLIO omits the entire propositional-only category. Every sampled example contains at least one quantifier (DATASET-D1, D2, D4), and the documentation treats FOL with quantifiers as foundational [Q15, Q63]. LogicBench [WEB-1] is identified as a complementary benchmark covering nine propositional inference rules. — _Sources: Q15, Q63, WEB-2, WEB-1, DATASET-D1, DATASET-D2, DATASET-D4_
- **IO-3**: FOLIO includes very deep reasoning chains (mode 4 steps, 28.7% requiring 5+ [Q60]; DATASET-D7, D10, D21 show 6–7 premise chains) that exceed typical introductory difficulty and may introduce construct-irrelevant variance for the deployment's 1–3 step target. — _Sources: Q60, DATASET-D7, DATASET-D10, DATASET-D21_
- **IO-4**: Two documented gaps harm content validity: (a) total absence of propositional-only subset undertests the first half of the course; (b) reasoning depth distribution skews well above the typical course-packet 1–3 step range. — _Sources: Q60, WEB-2, DATASET-D1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q15] 'a natural language reasoning dataset, FOLIO, with first-order logic reasoning problems which require the models to decide the correctness of conclusions given a world defined by the premises' (p.1)
- [Q43] 'There are 256 logically distinct types of syllogisms and 24 of them are valid... We use various combinations of 24 valid syllogisms. We also add in conjunction, disjunction, and implication.' (p.4)
- [Q60] '28.7% of the examples need five or more depths of reasoning to infer the conclusions' (p.5)
- [Q138] 'We include the following operators: negation ¬, conjunction ∧, disjunction ∨, implication →, universal quantifier ∀, existential quantifier ∃, equal =' (p.13)
- [Q139] 'we consider temporal logic and modal logic as special-purpose logics' (p.13)
- [Q140] 'they are beyond the scope of the definition of first-order logic used in our dataset' (p.13)

*Web sources:*
- [WEB-2] FOL2NS characterizes quantifiers as the key feature distinguishing FOL from propositional logics; FOLIO has no propositional-only subset
- [WEB-1] LogicBench (ACL 2024) covers nine propositional inference rules (MP, MT, HS, DS, CD, DD, BD, CT, MI) as complementary benchmark

*Dataset analysis:*
- DATASET-D1: simplest two-premise FOLIO example still uses ∀ for both premises — confirms no propositional-only examples
- DATASET-D4: shortest sampled example also quantified — '∀x (Building(x) → Tall(x))'
- DATASET-D21: 6-premise chained reasoning across multiple universal rules — exceeds introductory depth
- DATASET-D7: 7-premise tech-company narrative with nested XOR — substantially deeper than course-packet target

</details>

**Information gaps:**
- Exact proportion of FOLIO examples that fall in the 1–3 step depth range usable as proxy for course-packet difficulty

**Requires expert verification:**
- Course instructor confirmation of typical reasoning depth distribution in actual course packets

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The deployment's dominant input register is heavily templated Hurley-style prose ('All A are B', 'If P then Q'), explicitly confirmed in elicitation A3. FOLIO's WikiLogic pipeline deliberately avoided template-style generation [Q35] and produces naturalistic, Wikipedia-seeded prose; HybLogic uses syllogistic templates instantiated with naturalistic NL fillers [Q42, Q44]. Sampled data confirms predominance of complex naturalistic narratives — tech companies (DATASET-D7), branded products (DATASET-D9), economics with geopolitical content (DATASET-D14), astronomy with technical nomenclature (DATASET-D25). Only a minority of examples (DATASET-D1, D2, D3, D5) approach Hurley-template form. FOLIO also added epistemic qualifiers to generalizations [Q129] and used naturalistic disjunction phrasings [Q130, Q131, Q132, Q133] that depart from bare templates. WikiLogic content may overlap with LLM training data [Q104], further confounding deployment performance prediction. The benchmark does explicitly avoid identity-linked biases and stereotypes [Q47, Q127], which is appropriate for a US academic context.

**Strengths:**
- Subset of HybLogic examples uses minimal syllogistic forms structurally close to Hurley templates (DATASET-D1, D2, D5)
- Explicit exclusion of identity stereotypes and opinionated language [Q47, Q127] matches academic deployment norms
- Topic diversity and AST variety [Q38, Q61] reduce risk of narrow-domain overfit

**Checklist:**

- **IC-1**: Deployment requires syntactically constrained, domain-neutral pedagogical templates. FOLIO inputs frequently embed real-world domain knowledge (Russia/embargo D14, Rouge Dior products D9, PSO J318.5−22 D25) that introduces construct-irrelevant variance not present in Hurley-style problems. — _Sources: Q35, Q104, DATASET-D7, DATASET-D9, DATASET-D14, DATASET-D25_
- **IC-2**: Cultural content is broadly US/Western academic (Wikipedia-seeded). Aligns with US undergraduate deployment population. No identity-linked biases were retained [Q47, Q127]. — _Sources: Q47, Q127_
- **IC-3**: Western-specific knowledge appears (Yale references in D11, US tech companies in D23, US film industry in D12) but the deployment is itself US-based, so this is not a transfer problem. The greater concern is construct-irrelevant domain knowledge load. — _Sources: DATASET-D14, DATASET-D25_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional annotator recruitment was performed for this assessment; concern is based on register/style mismatch, not cultural sensitivity.
- **IC-5**: Register mismatch (naturalistic prose vs. Hurley-style bare templates) is the primary content-validity concern; LLM training-data contamination for WikiLogic [Q104] adds a secondary concern. — _Sources: Q35, Q104, Q129, DATASET-D7, WEB-1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q33] 'collected our dataset using two different methods in order to obtain examples that are both logically diverse and complex and have abundant abstract syntax tree (AST) variations' (p.4)
- [Q35] 'We ask the annotators to create new stories from scratch without using templates based on real-world knowledge' (p.4)
- [Q44] 'we then ask human annotators to assign nouns, phrases, or clauses to the abstract entities or categories that reflect real-life scenarios to each template' (p.4)
- [Q47] 'Our dataset prioritizes realism and factual accuracy, steering clear of biases and stereotypes' (p.4)
- [Q104] 'since the examples in WikiLogic are created from scratch by humans, it is possible that LLMs have seen similar texts with similar logical patterns in the training data' (p.8)
- [Q127] 'We took out stories that had strongly opinionated language and contained gender, racial, and classist biases' (p.13)
- [Q129] 'For stories that pertain to generalization, such as "All As are Bs," we have added specifiers like "all Dan knows"' (p.13)

*Web sources:*
- [WEB-1] LogicBench uses heuristic single-rule templates but does not replicate Hurley-style bare templates
- No benchmark explicitly replicating Hurley-style bare-template register was identified after ACL Anthology and arXiv search

*Dataset analysis:*
- DATASET-D7: 7-premise tech-company narrative with embedded relative clauses — maximally different from Hurley bare templates
- DATASET-D9: branded Rouge Dior lipstick product line — domain-specific NP terminology
- DATASET-D14: Russia embargo economics scenario — geopolitical content alien to introductory course packets
- DATASET-D25: 'PSO J318.5−22 is a rogue planet' — technical astronomical designation adds parsing load
- DATASET-D1, D2, D3, D5: short syllogistic examples that do approach Hurley register — minority subset

</details>

**Information gaps:**
- Proportion of HybLogic examples that match Hurley templates closely enough to use as a focused subset
- Quantitative measure of LLM training-data contamination risk for WikiLogic examples

**Requires expert verification:**
- Course-instructor sampling of representative course-packet problems to compare against FOLIO subsets for register match

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Modality, script, and language match the deployment cleanly: both are English text in standard Latin script [Q27, Q64]. FOLIO's premises-and-conclusions structural format is directly compatible with the deployment's input style. Grammar was checked with Grammarly and reviewed by English Literature annotators [Q49, Q50], and ambiguity was minimized [Q51]. The 70/15/15 train/val/test split by story [Q78, Q79] avoids cross-split leakage. The only form-level wrinkles are: (a) FOLIO uses naturalistic disjunction conventions [Q130, Q131] and adds epistemic qualifiers [Q129] rather than bare connective phrasings — but these are register-level (input content) rather than modality-level concerns; (b) the HuggingFace dataset's mean Dale-Chall readability score could not be retrieved [WEB-7]. No infrastructure or signal-distribution mismatch.

**Strengths:**
- Text-only English in standard Latin script matches deployment exactly [Q27, Q64]
- Grammar-checked, ambiguity-minimized prose [Q49, Q50, Q51]
- Story-level train/val/test split prevents leakage [Q78, Q79]

**Checklist:**

- **IF-1**: No signal-distribution mismatch — both benchmark and deployment use English text. Dale-Chall readability distribution is reported in FOLIO Figure 3 [Q154] but no mean is accessible; Hurley templates likely score lower (simpler) than FOLIO's naturalistic prose [WEB-7]. — _Sources: Q27, Q64, WEB-7_
- **IF-2**: Deployment infrastructure is standard US-university NLP tooling; full compatibility with FOLIO's text format. NLI tooling availability is strong for English. — _Sources: Q27_
- **IF-3**: Sentence-level conventions (e.g., 'Some A is B' over '∃x...' [Q132], 'All A are B' over 'If A then B' [Q133]) approach Hurley forms; 'either-or' for XOR [Q130] is also a textbook convention. Where FOLIO diverges is in qualifier addition [Q129] and richer naturalistic prose. — _Sources: Q130, Q132, Q133, Q129_
- **IF-4**: No modality or infrastructure mismatch identified. Residual readability concern flagged but low-priority. — _Sources: Q49, Q50_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q27] 'Our annotators are either college or graduate students who are native English speakers or possess near-native proficiency in English' (p.3)
- [Q49] 'All the sentences are first checked with a grammar checking tool, Grammarly' (p.4)
- [Q50] 'Our annotators who have graduated from or are senior students studying English Literature conducted a thorough round of review' (p.4)
- [Q51] 'We also eliminate natural language ambiguity when it is possible' (p.4)
- [Q64] 'Each natural language (NL) story S in FOLIO consists of n premises... and m conclusions' (p.6)
- [Q78] 'We split FOLIO by 70%/15%/15% split for the train/validation/test sets' (p.6)
- [Q79] 'We split by story so that models are evaluated on unseen stories' (p.6)

*Web sources:*
- [WEB-7] FOLIO GitHub repository — Figure 3 readability distribution not retrievable from text passages; mean Dale-Chall not reported

</details>

**Information gaps:**
- Mean Dale-Chall readability score for FOLIO vs. typical course packet

---

### Output Ontology — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
FOLIO uses a three-way True/False/Unknown label schema [Q36, Q66] that maps onto the deployment's valid/invalid/indeterminate rubric. The label-mapping concern flagged in elicitation (whether 'False' = entailment of negation, as the course requires for 'invalid') is resolved as aligned: the proving pipeline returns a definite truth value via theorem-prover execution [Q153], and the resolution-based Stanford CS221 engine returns False only when the negation is provably entailed [WEB-3, WEB-4]. The Unknown label is formally defined as the case where the inference engine returns neither True nor False [Q70], which matches the course's indeterminate definition (S ⊭ H and S ⊭ ¬H). Undecidable formulas are excluded by construction [Q70], matching the course rubric's exclusion. Empirical inspection confirms False labels are assigned only with provable counterexamples (DATASET-D11, D12, D13). Two residual concerns: (a) the HuggingFace dataset uses the label string 'Uncertain' rather than the paper's 'Unknown' (DATASET-D3, D15, D37), a practical-implementation hazard; (b) label imbalance (Unknown = 27% of test set [Q94]) combined with model bias toward True predictions [Q155, Q156, Q157] means accuracy may not equally reflect performance on the invalid and indeterminate categories the rubric distinguishes.

**Strengths:**
- Three-way schema [Q36, Q66] structurally matches deployment rubric
- False label formally equivalent to S ⊨ ¬H via resolution prover [WEB-3, WEB-4], matching course's strict 'invalid' definition
- Unknown excludes undecidable formulas by construction [Q70], matching course's exclusion
- Empirical False examples reflect provable negation entailment (DATASET-D11, D12, D13)

**Checklist:**

- **OO-1**: All three FOLIO categories are deployment-relevant: True↔valid, False↔invalid (both = entailment of negation), Unknown↔indeterminate [Q36, Q66, Q70, WEB-3, WEB-4]. — _Sources: Q36, Q66, Q70, WEB-3, WEB-4, DATASET-D11, DATASET-D17_
- **OO-2**: No regionally-specific category missing — the deployment's three-way scheme is fully represented. — _Sources: Q36_
- **OO-3**: No non-regional values encoded; FOL semantics are universal. — _Sources: Q138_
- **OO-4**: No taxonomy redesign required. However, evaluation code must use the actual label string 'Uncertain' (HuggingFace) rather than 'Unknown' (paper) [DATASET-D3, D15, D37]. — _Sources: DATASET-D3, DATASET-D15_
- **OO-5**: Residual issues: label-string inconsistency between paper and HuggingFace data; label imbalance (Unknown 27%) combined with documented model bias toward True [Q155, Q156] reduces accuracy's informativeness for the indeterminate category. — _Sources: Q94, Q155, Q156, DATASET-D3_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q36] 'Each of the stories is composed of several premises and conclusions with truth values of True, False, or Unknown' (p.4)
- [Q66] 'Given P and H, the goal is to determine the truth values of the conclusions: "True", "False" or "Unknown", based on FOL reasoning' (p.6)
- [Q70] 'the premises and conclusions are set up in such a way to ensure that the inference engine always returns an answer given enough resources such as time and memory' (p.6)
- [Q94] 'in our test set, there are 87, 78 and 61 examples with labels of true, false and unknown respectively' (p.7)
- [Q153] 'the FOL statements... are converted to Python code... the theorem prover outputs whether the conclusions are True / False / Unknown' (p.14)
- [Q155] 'LLMs are significantly better at making the correct predictions for conclusions with labels of True than the conclusions with labels of False or Unknown' (p.15)
- [Q156] 'The accuracy on examples with False or Unknown conclusions is 61.9% with fine-tuning and 54.0% with few-shot prompting' (p.15)

*Web sources:*
- [WEB-3] CGD-PD paper formalizes FOLIO labels as True = S ⊨ H, False = S ⊨ ¬H, Unknown = S ⊭ H and S ⊭ ¬H
- [WEB-4] Stanford CS221 resolution-based inference engine semantics confirm False is returned only when negation is provably entailed
- [WEB-5] FOLIO paper Q70 confirmation: undecidables excluded by construction

*Dataset analysis:*
- DATASET-D11, D12, D13: False labels assigned with clear provable counterexamples — confirms S ⊨ ¬H semantics empirically
- DATASET-D17, D26: Unknown labels assigned where premises are silent on conclusion topic — confirms indeterminate semantics empirically
- DATASET-D3, D15, D37: HuggingFace data uses label string 'Uncertain' rather than paper's 'Unknown' — practical implementation gap

</details>

**Information gaps:**
- Whether FOLIO's 27% Unknown share matches the course packet's indeterminate problem frequency

**Requires expert verification:**
- Course-instructor elicitation of typical course-packet indeterminate problem rate

---

### Output Content — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
Ground-truth label generation is rigorous: expert annotators (CS undergraduates/graduates and senior researchers with formal FOL training and native or near-native English [Q16, Q27, Q28, Q31, Q122, Q123]) executed a six-stage 980-person-hour annotation pipeline [Q32] with separate NL and FOL expert quality checks [Q29, Q124, Q125]. All FOL annotations are verified by an inference engine [Q2, Q57], and expert human accuracy reaches 95.98% [Q111] — strong convergent evidence for label correctness on clear cases. Premise ordering does not yield spurious labels [Q158, Q159, Q160]. However, empirical inspection of the HuggingFace data reveals multiple concrete annotation errors: free variables in FOL conditionals (DATASET-D27), name inconsistencies between premises and conclusions (DATASET-D24, D28), missing closing parentheses (DATASET-D29, D30, D35), and a potential NL-FOL alignment gap on inclusive disjunction (DATASET-D36). The 2026 Vampire-prover cleaning study confirms these are systemic [WEB-6]. The annotator population (expert FOL-trained academics) is appropriate for producing reliable ground-truth labels but is not representative of novice-student production norms — this is acceptable for ground-truth quality and not a concern for the deployment's use of FOLIO as a label oracle.

**Strengths:**
- Expert annotator population with formal FOL training [Q16, Q27, Q28, Q123]
- Six-stage 980-person-hour annotation pipeline with separate NL and FOL quality checks [Q29, Q32, Q124, Q125]
- FOL-engine verification of all label annotations [Q2, Q57]
- Expert human accuracy 95.98% [Q111] — strong convergent evidence
- No premise-ordering spurious correlations [Q158, Q159, Q160]

**Checklist:**

- **OC-1**: Ground-truth labels reflect formal FOL semantics, which is the deployment's normative standard for valid/invalid/indeterminate. Regional stakeholder perspective is replaced by formal logical correctness — appropriate for this deployment. — _Sources: Q2, Q57_
- **OC-2**: Disagreement between annotators and regional population is not a meaningful axis here, since the rubric is formal-logical. Novice students would disagree with expert labels but only because the experts are correct. — _Sources: Q111_
- **OC-3**: Annotator demographics documented: native/near-native English speakers, college and graduate CS students with formal FOL training, NLP and FOL domain experts assigned to quality-check stages [Q27, Q28, Q31, Q122, Q123, Q124, Q125]. — _Sources: Q27, Q28, Q31, Q122, Q123, Q124, Q125_
- **OC-4**: Re-annotation by regional pool not necessary — formal-logical labels are the target. However, the 2026 Vampire-prover cleaned split [WEB-6] should be preferred if available, given the annotation errors observed in the raw HuggingFace data (DATASET-D27, D28, D29, D30, D35). — _Sources: WEB-6, DATASET-D27, DATASET-D28, DATASET-D29_
- **OC-5**: Aggregation method (FOL-engine verification) does not erase minority perspectives; it enforces formal correctness. — _Sources: Q2_
- **OC-6**: Concrete annotation errors observable in sampled data (free variables, name mismatches, unmatched parentheses) confirm the 2026 cleaning study's findings — undermines label reliability for some portion of the dataset and warrants using the cleaned split. — _Sources: WEB-6, DATASET-D24, DATASET-D27, DATASET-D29, DATASET-D35, DATASET-D36_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'The logical correctness of the premises and conclusions is ensured by their FOL annotations, which are automatically verified by an FOL inference engine' (p.1)
- [Q16] 'FOLIO is a high-quality and manually curated dataset, written by CS undergraduate and graduate students and researchers in academia and industry' (p.2)
- [Q28] 'They possess formal education in first-order logic' (p.3)
- [Q29] 'At the NL quality check stage, only annotators who are experts in natural language processing or computational linguistics are involved. For the FOL quality check, only annotators who are experts in first-order logic are involved.' (p.4)
- [Q32] 'We develop our dataset in six stages... spending 980 man-hours in total' (p.4)
- [Q57] 'we verify the syntactic validity and label consistency of FOL formula annotations with an FOL inference engine' (p.5)
- [Q111] 'Expert annotations achieve an accuracy of 95.98% while non-expert annotations achieves 61.82%' (p.9)
- [Q160] 'the ordering of premises in FOLIO examples does not yield significant information about the label' (p.15)

*Web sources:*
- [WEB-6] 2026 Agentified Assessment paper using Vampire theorem prover identified label errors and NL-FOL misalignments in original FOLIO; auto-formalization reached 86.70% on validation set after cleaning

*Dataset analysis:*
- DATASET-D27: free variable x in FOL conditional antecedent — annotation error
- DATASET-D24: name inconsistency between premises (John) and conclusion (Jim)
- DATASET-D28: name inconsistency between premises (Matt) and conclusion (Mike)
- DATASET-D29: missing closing parenthesis in FOL formula
- DATASET-D30: trailing unmatched parenthesis in conclusion-FOL
- DATASET-D35: unmatched trailing parenthesis in FOL premise
- DATASET-D36: NL 'either...or both' (inclusive) rendered as bare ∨ without verification

</details>

**Information gaps:**
- Total proportion of FOLIO examples affected by annotation errors observable only via systematic prover verification
- Whether the 2026 cleaned split is publicly accessible at time of deployment

**Requires expert verification:**
- Logic-instructor spot-check of FOLIO labels against course rubric on a sample of HybLogic examples that match Hurley register

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
The deployment produces a single categorical label from a fixed three-item set (valid/invalid/indeterminate), and FOLIO's primary reasoning task evaluates a categorical label from True/False/Unknown with accuracy as the primary metric [Q80, Q66]. Output modality and form are well-matched. The NL-FOL translation metrics (SynV, ExcAcc [Q73–Q76]) are not deployment-relevant. Two minor wrinkles: (a) the public HuggingFace dataset does not expose the `test` split that published baselines [Q93, Q94] are computed on, limiting direct comparison; (b) accuracy alone (without per-class breakdown) is insufficient given documented model bias toward True predictions [Q155, Q156, Q157] — per-class accuracy should be reported. Literacy and accessibility are non-issues: the deployment population is US undergraduates in an English-language course.

**Strengths:**
- Categorical label from fixed small set matches deployment exactly [Q66, Q80]
- Accuracy is a transparent, deployment-aligned metric
- No modality mismatch — text in, label out

**Checklist:**

- **OF-1**: Output modality (single categorical label) matches deployment need exactly [Q66, Q80]. — _Sources: Q66, Q80_
- **OF-2**: Text-to-speech not relevant; deployment is a text-based tool used by literate undergraduates.
- **OF-3**: Literacy assumed (US undergraduate population); accessibility-of-output not a concern at this stage.
- **OF-4**: Practical concerns: (a) test split unavailable on HuggingFace (DATASET limitation) — published baselines [Q93, Q94] cannot be directly replicated; (b) overall accuracy hides class-imbalance effects, so per-class accuracy should be reported [Q155, Q156]. — _Sources: Q93, Q155, Q156_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q66] 'Given P and H, the goal is to determine the truth values of the conclusions: "True", "False" or "Unknown"' (p.6)
- [Q80] 'We use accuracy for evaluating logical reasoning performance' (p.6)
- [Q93] 'We run experiments on five randomly sampled sets of examples from the training set and report the average accuracy' (p.7)
- [Q155] 'LLMs are significantly better at making the correct predictions for conclusions with labels of True than the conclusions with labels of False or Unknown' (p.15)
- [Q156] 'The accuracy on examples with False or Unknown conclusions is 61.9% with fine-tuning and 54.0% with few-shot prompting' (p.15)

*Dataset analysis:*
- Dataset analysis limitation: HuggingFace exposes only train (1001) and validation (203) splits; the test split (226 examples) used for published baselines is not publicly accessible

</details>

**Information gaps:**
- Whether the public release of FOLIO test split has been updated since dataset analysis

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** Complete absence of propositional-only (quantifier-free) examples leaves the course's first half uncovered.

**Recommendation:** Supplement FOLIO with LogicBench [WEB-1], which explicitly covers nine propositional inference rules (MP, MT, HS, DS, CD, DD, BD, CT, MI) directly relevant to the propositional half of the course.

### Input Ontology ⚠

**Gap:** Reasoning depth distribution (mode 4 steps, 28.7% at 5+) substantially exceeds typical introductory course-packet problems (1–3 steps).

**Recommendation:** Stratify FOLIO evaluation by reasoning depth and report 1–3 step accuracy separately as the course-aligned metric; treat 5+ step performance as informative but not deployment-critical.

### Input Content ⚠

**Gap:** FOLIO's dominant naturalistic prose register (with Wikipedia-seeded content and real-world domain knowledge) does not match the course's Hurley-style syntactically controlled templates.

**Recommendation:** Construct a small course-packet-aligned probe set (50–100 problems) in bare Hurley-template form ('All A are B', 'If P then Q', etc.) for register-matched validation. Optionally filter FOLIO to the HybLogic subset that approaches template form (e.g., DATASET-D1, D2, D5) for a closer FOLIO-internal proxy.

### Output Content

**Gap:** Observable annotation errors in the public HuggingFace release (free variables, name mismatches, unmatched parentheses) confirm a known systemic issue identified by the 2026 Vampire-prover cleaning study.

**Recommendation:** Prefer the 2026 cleaned FOLIO split [WEB-6] when available; if using the original release, run a syntactic check on all FOL formulas and manually verify a sample of False and Uncertain labels before reporting performance.

### Output Form

**Gap:** Public HuggingFace release does not expose the test split that published baselines are computed on, limiting direct replication of GPT-4 64.16% / expert 95.98% comparisons.

**Recommendation:** Use the validation split (203 examples) for deployment-aligned benchmarking and document the split used; treat published test-set baselines as approximate references rather than exact targets.

### Output Ontology

**Gap:** Label string in HuggingFace data ('Uncertain') differs from paper documentation ('Unknown'); label imbalance plus documented model bias toward True predictions reduces informativeness of overall accuracy.

**Recommendation:** Use the actual label strings as released ('Uncertain') in evaluation pipelines, and report per-class accuracy (True/False/Uncertain separately) in addition to overall accuracy. Track invalid- and indeterminate-class accuracy specifically as the deployment-critical metrics.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "FOLIO consists of 1,430 examples (unique conclusions), each paired with one of 487 sets of premises used to deductively reason for the validity of each conclusion." |
| Q2 | 1 | output_content | "The logical correctness of the premises and conclusions is ensured by their FOL annotations, which are automatically verified by an FOL inference engine." |
| Q3 | 1 | input_ontology | "In addition to the main NL reasoning task, NL-FOL pairs in FOLIO constitute a new NL-FOL translation dataset." |
| Q4 | 1 | output_form | "Our experiments on FOLIO systematically evaluate the FOL reasoning ability of supervised fine-tuning on medium-sized language models." |
| Q5 | 1 | output_form | "For both NL reasoning and NL-FOL translation, we benchmark multiple state-of-the-art language models." |
| Q6 | 1 | output_form | "Our results show that a subset of FOLIO presents a challenge for one of the most capable Large Language Model (LLM) publicly available, GPT-4." |
| Q7 | 1 | input_ontology | "Logical reasoning is a central component for intelligent systems and should be sufficiently and independently evaluated (Russell and Norvig, 2010)." |
| Q8 | 1 | input_ontology | "However, existing natural language tasks are inadequate in measuring the complex logical reasoning capability of a model (Srivastava et al., 2023; Saparov and He, 2023; Tian et al., 2021)." |
| Q9 | 1 | input_ontology | "Some of these common benchmarks do not specifically evaluate logical reasoning independently of other forms of reasoning (Yu et al., 2020; Liu et al., 2021)." |
| Q10 | 1 | input_ontology | "Those specifically designed for measuring logical reasoning are insufficient in terms of logical reasoning complexity and natural language variety." |
| Q11 | 1 | input_ontology | "Examples in RuleTaker (Clark et al., 2020) and LogicNLI (Tian et al., 2021) need at most five depths of reasoning." |
| Q12 | 1 | input_ontology | "The entire corpus of RuleTaker or LogicNLI has fewer than 50 distinct abstract syntax trees." |
| Q13 | 1 | input_ontology | "RuleTaker has only 101 words in its vocabulary and LogicNLI has 1077 words in the vocabulary." |
| Q14 | 1 | input_content | "Moreover, none of them are written by humans with information drawn from real-world knowledge, making them less applicable to real-world reasoning scenarios." |
| Q15 | 1 | input_ontology | "We present a natural language reasoning dataset, FOLIO, with first-order logic reasoning problems which require the models to decide the correctness of conclusions given a world defined by the premises." |
| Q16 | 2 | output_content | "FOLIO is a high-quality and manually curated dataset, written by CS undergraduate and graduate students and researchers in academia and industry." |
| Q17 | 2 | output_content | "To ensure the conclusions of our examples follow the premises logically, we annotated all reasoning examples with first-order logic (FOL) formulas." |
| Q18 | 2 | input_ontology | "Based on our annotations, we propose a new NL-FOL translation task where an NL reasoning example is translated into its FOL counterpart." |
| Q19 | 2 | output_form | "Finally, we benchmark the performance of strong LMs in both fully supervised and few-shot settings to understand their capabilities in logical reasoning (i.e., deriving the truth value of a logical conclusion from NL premises)." |
| Q20 | 2 | output_content | "Under the few-shot setting, the most capable publicly available LLM so far achieves only 53.1% on the stories written in a hybrid manner, which is slightly better than random." |
| Q21 | 2 | output_content | "We release a natural language reasoning dataset written by expert annotators, FOLIO, with first-order logical reasoning problems." |
| Q22 | 2 | input_form | "We use formal logic, i.e., FOL to ensure the logical validity of the examples written in NL and propose a new NL-FOL translation task." |
| Q23 | 2 | output_form | "We benchmark the performance of LMs by fine-tuning models and prompting LLMs with few-shot examples, on the FOLIO reasoning task." |
| Q24 | 3 | output_content | "We collected FOLIO through a carefully designed manual annotation process to achieve high-quality examples that necessitate complex logical reasoning." |
| Q25 | 3 | output_content | "Writing natural language reasoning stories with FOL requires sufficient knowledge in both semantic parsing and first-order logic, as well as strong analytical skills." |
| Q26 | 3 | output_content | "Given the complexities of such annotations, we selected annotators based on a few important criteria to ensures that our dataset is annotated with the highest level of precision and expertise, reflecting the complexity and nuance required for first-order logical reasoning." |
| Q27 | 3 | input_form | "Our annotators are either college or graduate students who are native English speakers or possess near-native proficiency in English." |
| Q28 | 3 | output_content | "They possess formal education in first-order logic, having either completed relevant coursework or undertaken self-directed studies in first-order logic or seman-" |
| Q29 | 4 | output_content | "At the NL quality check stage, only annotators who are experts in natural language processing or computational linguistics are involved. For the FOL quality check, only annotators who are experts in first-order logic are involved." |
| Q30 | 4 | output_content | "We also give the annotators several training sessions on how to write a story, by providing them with detailed annotation guidelines." |
| Q31 | 4 | output_content | "All stories and FOL annotations in FOLIO are written and reviewed by expert annotators, including CS undergraduate and graduate students, and senior researchers, who met the aforementioned criteria." |
| Q32 | 4 | input_content | "We develop our dataset in six stages: WikiLogic collection, HybLogic collection, NL quality control, FOL quality control, NL-FOL alignment and FOL verification, spending 980 man-hours in total." |
| Q33 | 4 | input_content | "We collected our dataset using two different methods in order to obtain examples that are both logically diverse and complex and have abundant abstract syntax tree (AST) variations." |
| Q34 | 4 | input_content | "WikiLogic: annotation from scratch using Wikipedia articles as seeds. At this annotation stage, the annotators are asked to select random Wikipedia pages by repeatedly using the Wikipedia Special Random link. The Wikipedia articles are used to develop ideas for topics to write new stories." |
| Q35 | 4 | input_content | "We ask the annotators to create new stories from scratch without using templates based on real-world knowledge, which should be plausible in general." |
| Q36 | 4 | output_ontology | "Each of the stories is composed of several premises and conclusions with truth values of True, False, or Unknown (see Table 2 for an example)." |
| Q37 | 4 | output_ontology | "We also ask the annotators to write parallel FOL sentences for both the premises and conclusions." |
| Q38 | 4 | input_content | "This results in a wide range of topics, abundant AST variations, and a wide vocabulary for FOLIO." |
| Q39 | 4 | input_content | "HybLogic: hybrid annotation The task of generating logically sound stories from scratch for a set of facts is very time-consuming for human writers, where the main challenge is to create complex and varied logical patterns to arrive at a conclusion." |
| Q40 | 4 | input_content | "To address the problems of solely using manual annotation, we also consider a hybrid approach to facilitate the process. Our hybrid method is based on a common form of logical stories: syllogisms." |
| Q41 | 4 | input_ontology | "A syllogism consists of two premises and a single conclusion, and the conclusion states some facts about the entities and categories in the premises." |
| Q42 | 4 | input_content | "In this approach, we first generate logically valid stories, which are templates containing abstract categories and entities, by combining multiple syllogisms into a single story template: the conclusion of one syllogism is used as a premise for the next syllogism." |
| Q43 | 4 | input_ontology | "There are 256 logically distinct types of syllogisms and 24 of them are valid (Lehman, 1973). We use various combinations of 24 valid syllogisms. We also add in conjunction, disjunction, and implication." |
| Q44 | 4 | input_content | "We then ask human annotators to assign nouns, phrases, or clauses to the abstract entities or categories that reflect real-life scenarios to each template and write logically-valid stories in natural language." |
| Q45 | 4 | input_content | "The usage of the template is to ensure that we have a set of varied and complex logical stories with multiple conclusions. There are many ways of expressing the same logic template in natural language, and so the generated templates augment, rather than limit, the creativity of humans." |
| Q46 | 4 | output_content | "To ensure the highest quality of the dataset, we dedicated considerable attention to the following key aspects of the natural language sentences during the quality control process." |
| Q47 | 4 | input_content | "Our dataset prioritizes realism and factual accuracy, steering clear of biases and stereotypes linked to identity markers like race, ethnicity, gender, sexuality, nationality, class, and religion." |
| Q48 | 4 | output_content | "Toward these objectives, we manually screened all stories and found that 39.2% of the stories suffer from at least one of these issues. We implemented a detailed protocol to rewrite these stories." |
| Q49 | 4 | input_form | "Apart from grammar, we make sure the sentences in our dataset are highly natural. All the sentences are first checked with a grammar checking tool, Grammarly." |
| Q50 | 4 | input_form | "Our annotators who have graduated from or are senior students studying English Literature conducted a thorough round of review for grammatical correctness and language naturalness." |
| Q51 | 4 | input_form | "We also eliminate natural language ambiguity when it is possible." |
| Q52 | 5 | input_form | "We adopt the FOL definitions and syntax most widely used in the AI community (Russell and Norvig, 2010)." |
| Q53 | 5 | output_content | "In preliminary investigations, we found that the human-written FOL formulas suffer from FOL consistency issues, which necessitates an additional round of quality control for FOL formulas." |
| Q54 | 5 | output_content | "One NL sentence can be translated into FOL through multiple non-equivalent ways. For example, sometimes additional information inferred from a sentence can be represented in FOL, leading to multiple representations. We therefore design an annotation protocol for FOL translation in order to ensure that our FOL translations are as consistent as possible across all examples in our dataset." |
| Q55 | 5 | output_content | "Apart from checking whether NL and FOL express equivalent meanings, we also add necessary commonsense knowledge in both the NL and FOL premises. Sometimes humans do not write certain commonsense knowledge in the premises that is required in the FOL reasoning process, which is based solely on the premises given. We add such knowledge as additional premises at this stage." |
| Q56 | 5 | input_form | "In particular, intrinsic properties of some predicates are required in the FOL reasoning process. For example, "LocatedIn(x,y)" should be transitive and "BeFamily(x,y)" should be symmetric." |
| Q57 | 5 | output_content | "Recognizing that the FOL formula annotations can be error-prone, we verify the syntactic validity and label consistency of FOL formula annotations with an FOL inference engine." |
| Q58 | 5 | input_content | "Table 3 shows that examples based on Wikipedia make up the largest portion of FOLIO, with 304 stories, 1,353 NL and FOL premise pairs, and 753 NL and FOL conclusion pairs. Hybrid annotations consist of 183 stories with 1,054 NL and FOL premise pairs, and 682 NL and FOL conclusion pairs in total." |
| Q59 | 5 | output_form | "We use the Dale-Chall Readability Formula (Dale and Chall, 1948, 1995) to show the text complexity of FOLIO following (Singh et al., 2023; Arps et al., 2022; Wei et al., 2021)." |
| Q60 | 5 | input_ontology | "As shown in Figure 1, the mode of reasoning depths is four in FOLIO. 28.7% of the examples need five or more depths of reasoning to infer the conclusions, while the previous datasets needed at most five reasoning depths as shown in Table 1." |
| Q61 | 5 | input_ontology | "Table 1 shows that FOLIO also has a much larger number of distinct ASTs than the previous datasets, indicating that FOLIO is much more logically diverse." |
| Q62 | 5 | input_content | "Table 3 shows that our dataset has a vocabulary of 4,351 words, and the examples based on Wikipedia account for 74% of the total vocabulary even though the WikiLogic stories take up only 63% of the total number of stories." |
| Q63 | 6 | input_ontology | "We define two new tasks based on FOLIO, natural language reasoning with first-order logic and NL-FOL translation." |
| Q64 | 6 | input_form | "Each natural language (NL) story S in FOLIO consists of n premises: P = {p1, p2, ..., pn} and m conclusions: H = {h1, h2, ..., hm}." |
| Q65 | 6 | input_form | "All NL stories are annotated with parallel FOL stories SF, which are sets of FOL formulas consisting of n premises PF = {pf1, pf2, ..., pfn} and m conclusions HF = {hf1, hf2, ..., hfm}." |
| Q66 | 6 | output_ontology | "Given P and H, the goal is to determine the truth values of the conclusions: "True", "False" or "Unknown", based on FOL reasoning." |
| Q67 | 6 | input_ontology | "We propose a new natural language to first-order logic translation (NL-FOL translation) task alongside our reasoning dataset." |
| Q68 | 6 | output_ontology | "In particular, each of the NL sentence pi or hi and the parallel FOL formula pfi or hfi should be logically and semantically equivalent." |
| Q69 | 6 | output_ontology | "Moreover, the truth values for the conclusions should be the same based on the NL story S and the parallel FOL story FS." |
| Q70 | 6 | output_ontology | "In our dataset, the premises and conclusions are set up in such a way to ensure that the inference engine always returns an answer given enough resources such as time and memory." |
| Q71 | 6 | input_ontology | "Unlike previous work (Singh et al., 2020) which translates problems with a single premise and a single hypothesis, our task is on translating examples of various lengths with a focus on stories with multiple premises." |
| Q72 | 6 | input_ontology | "Thus, it also requires the models to consider discourse-level consistencies as opposed to translation at the sentence level." |
| Q73 | 6 | output_form | "Two metrics are adopted to evaluate NL-FOL translation to capture different aspects of the generation results: 1). Syntactic validity (SynV)." |
| Q74 | 6 | output_form | "The Syntactic Validity score measures whether the FOL formulas are syntactically valid. The score will be 1 if all FOL formulas of an example can pass the syntactic check and 0 otherwise 2)." |
| Q75 | 6 | output_form | "Inference Engine execution accuracy (ExcAcc). The group of translated FOL for premises and conclusions in one story is fed into our inference engine to output the truth value for each conclusion." |
| Q76 | 6 | output_form | "We define the accuracy of the output labels as the execution accuracy." |
| Q77 | 6 | output_form | "We leave for future work the design of a more reliable metric of NL-FOL translation." |
| Q78 | 6 | input_form | "We split FOLIO by 70%/15%/15% split for the train/validation/test sets with 1,001/203/226 examples respectively." |
| Q79 | 6 | input_form | "We split by story so that models are evaluated on unseen stories." |
| Q80 | 6 | output_form | "We use accuracy for evaluating logical reasoning performance." |
| Q81 | 6 | output_form | "For NL-FOL translation, we use the metrics in Section 4.2." |
| Q82 | 6 | input_ontology | "We test the logical reasoning capabilities of LMs using fully supervised fine-tuning and few-shot prompting." |
| Q83 | 6 | input_ontology | "We also test NL-FOL translation with few-shot prompting." |
| Q84 | 7 | input_ontology | "As fine-tuning baselines, we experiment with BERT (Devlin et al., 2019), and RoBERTa (Liu et al., 2020)." |
| Q85 | 7 | output_form | "We fine-tune the base and large versions of both BERT and RoBERTa, with an additional two-layer classification layer to predict the truth values." |
| Q86 | 7 | input_ontology | "For the second task, i.e., NL-FOL translation, we only report few-shot prompting methods." |
| Q87 | 7 | input_ontology | "We conduct zero-shot and few-shot prompting experiments on larger LMs with few-shot capabilities." |
| Q88 | 7 | input_ontology | "For open-source models, we test LLaMA-13B and LLaMA-70B (Touvron et al., 2023), GPT-NeoX-20B (Black et al., 2022); for proprietary models we test GPT-3 (Brown et al., 2020), GPT-3.5-Turbo and GPT-4 (OpenAI et al., 2023) using prompts with 8 examples." |
| Q89 | 7 | input_ontology | "We experiment with incorporating recent prompting strategies into GPT-4 as they have shown improvements in the general reasoning performance of LLMs." |
| Q90 | 7 | input_ontology | "The prompting strategies include chain-of-thought (CoT) prompting (Wei et al., 2022b), chain-of-thought prompting with self-consistency (Wang et al., 2023) and tree-of-thought prompting (Yao et al., 2023)." |
| Q91 | 7 | input_ontology | "We also test recent methods specifically designed for logical reasoning: Logic-LM (2023), LINC (Olausson et al., 2023) and DetermLR(Sun et al., 2023), using GPT-4 as the base model." |
| Q92 | 7 | input_form | "For the second task (NL-FOL translation), we use the same examples as in the Few-Shot NL experiments except that all the conclusions are included in each example." |
| Q93 | 7 | output_form | "We run experiments on five randomly sampled sets of examples from the training set and report the average accuracy." |
| Q94 | 7 | output_ontology | "The majority baseline of our dataset is 38.5% since in our test set, there are 87, 78 and 61 examples with labels of true, false and unknown respectively." |
| Q95 | 7 | input_form | "In experimenting with different prompts, we found 8 shot examples to perform slightly better. It is also the maximum number of examples that fits in the text-davinci-002 context." |
| Q96 | 8 | output_form | "Table 5 shows the results of NL-FOL translation. The syntactic validity scores are around 93% with both GPT-3.5-Turbo and GPT-4. This indicates that language models with sufficient scales are good at picking up the patterns for FOL formulas and generating syntactically valid FOL formulas." |
| Q97 | 8 | output_form | "However, GPT-3.5-Turbo and GPT-4 are not yet good at translating an NL story to a logically or semantically similar FOL counterpart, as indicated by the low inference engine execution accuracy score." |
| Q98 | 8 | output_form | "Below we provide analysis of our results and key findings, providing additional insights into our dataset FOLIO and the current capabilities of LLMs in logical reasoning." |
| Q99 | 8 | output_form | "With few-shot prompting, GPT-3.5 and GPT-4 both perform much better on examples with a 0 ∼ 3 reasoning depth, indicating that examples with a 4 ∼ 7 reasoning depth pose a challenge to the SoTA LMs." |
| Q100 | 8 | output_form | "This indicates that fine-tuning on longer and more difficult reasoning chains in the training set can improve model performance on equally-long test example chains." |
| Q101 | 8 | input_ontology | "FOLIO's unique complexity reveals that current LMs are limited in their ability to extrapolate to longer and more complex reasoning chains, and suggests an avenue for further study." |
| Q102 | 8 | output_form | "As shown in Table 6, in logical reasoning, GPT-3.5 and GPT-4 achieve substantially lower results on HybLogic than on WikiLogic and the result is slightly higher than chance." |
| Q103 | 8 | input_content | "We hypothesize that this is because HybLogic has high logical complexity that the SoTA LLMs like GPT-4 cannot solve yet while WikiLogic examples require shorter reasoning chains which the model is already capable of solving." |
| Q104 | 8 | input_content | "Moreover, since the examples in WikiLogic are created from scratch by humans, it is possible that LLMs have seen similar texts with similar logical patterns in the training data." |
| Q105 | 8 | input_content | "However, fine-tuning RoBERTa-large achieves higher performance on HybLogic than on WikiLogic. This is likely because HybLogic is created from templates and some of the logical patterns can be learned during fine-tuning." |
| Q106 | 8 | input_content | "In NL-FOL translation, performs 10 points better on HybLogic than WikiLogic. This could be because WikiLogic has more distinct and diverse sentence-level logical and language patterns and FOL annotations. WikiLogic has 53 ASTs while HybLogic has 33." |
| Q107 | 9 | output_content | "We collected truth value annotations of logical reasoning for FOLIO test set from expert and non-expert annotators." |
| Q108 | 9 | output_content | "Our expert annotators are computer science college students familiar with FOL." |
| Q109 | 9 | output_content | "Non-expert annotators are community college or high school students who have not taken the SAT." |
| Q110 | 9 | output_content | "Both expert and non-expert annotators are native English speakers." |
| Q111 | 9 | output_content | "Expert annotations achieve an accuracy of 95.98% while non-expert annotations achieves 61.82%, with a gap of 34.16%." |
| Q112 | 9 | input_ontology | "This shows that sufficient domain knowledge of FOL is necessary for good performance on FOLIO." |
| Q113 | 9 | output_content | "The expert and GPT-4 gap is 31.82%, suggesting significant room for model improvement." |
| Q114 | 9 | input_content | "We focus on collecting a very high-quality dataset in evaluating logical reasoning rather than merely a large dataset." |
| Q115 | 9 | output_content | "Optimizing for quality required us to adopt a rigorous annotation process with domain experts selected based on a few important criteria as mentioned in Appendix A: Annotator Selection." |
| Q116 | 9 | input_content | "Significantly scaling up this process would have required resources beyond our current means and we are unable further expand our dataset for investigating how the size of training data affects the performance of fine-tuning experiments." |
| Q117 | 9 | input_content | "We encourage the community to apply our annotation protocol to expand this realistic and complex FOL reasoning story set." |
| Q118 | 9 | output_form | "Approximately 65% of the time, the model struggles to construct accurate reasoning chains for complex problems with intricate steps, leading to faulty reasoning paths and indicating a limited ability to solve problems with long reasoning chains." |
| Q119 | 9 | output_form | "In 25% of cases, erroneous derivations occur within certain reasoning steps, highlighting potential inaccuracies and flaws in logical deductions." |
| Q120 | 9 | output_ontology | "5% of conclusions in FOLIO have a complex syntactic structure, posing comprehension challenges for GPT-4." |
| Q121 | 9 | output_content | "5% of outputs show that GPT-4 leverage commonsense reasoning to employ spurious shortcuts that lead to the wrong truth value for the conclusion." |
| Q122 | 12 | output_content | "Given the complexities of our annotations, we selected annotators based on a few important criteria 1). Our annotators are either college or graduate students who are native English speakers or possess near-native proficiency in English." |
| Q123 | 12 | output_content | "They possess formal education in first-order logic, having either completed relevant coursework or undertaken self-directed studies in first-order logic or semantic parsing." |
| Q124 | 12 | output_content | "At the NL quality check stage, only annotators who are experts in natural language processing or computational linguistics are involved." |
| Q125 | 12 | output_content | "For the FOL quality check, only annotators who are experts in first-order logic are involved." |
| Q126 | 13 | input_content | "We rewrote those that are not reflective of well-established scientific, historical, or legal facts." |
| Q127 | 13 | input_content | "We took out stories that had strongly opinionated language and contained gender, racial, and classist biases." |
| Q128 | 13 | input_content | "We accept certain classes of "psychologically fundamental generalizations" (Leslie, 2008), however, such as "Covid is transmitted through the air" or "Tigers eat other animals," that may not be factually invariant but add logical and semantic nuances to the stories." |
| Q129 | 13 | input_form | "For stories that pertain to generalization, such as "All As are Bs," we have added specifiers like "all Dan knows" to give a degree of reasonable factuality." |
| Q130 | 13 | input_form | "We always use "either-or" to express exclusive disjunction." |
| Q131 | 13 | input_form | "We use either "A or B" or "A or B, or both" to express inclusive disjunction." |
| Q132 | 13 | input_form | "It is more natural to say "Some A is B" rather than "there exists an A such that A is B."" |
| Q133 | 13 | input_form | ""All A are B" can be more natural than "If A then B"." |
| Q134 | 13 | input_form | "Other common issues in NL quality include singular/plural issues, especially in statements that deal with both categories and individual members of those categories; as well as ambiguities resulting from improper introduction of, or failure to introduce, proper nouns." |
| Q135 | 13 | output_ontology | "FOL enables deriving facts from other facts (Russell and Norvig, 2010)." |
| Q136 | 13 | output_ontology | "FOL, as a logical form, is a more explicit logical representation than its NL counterpart and can be used as input to an FOL prover in order to obtain the exact truth values for the conclusions." |
| Q137 | 13 | output_ontology | "FOL has no ambiguity while ambiguity can occur at various levels of NLP." |
| Q138 | 13 | output_ontology | "We include the following operators: negation ¬, conjunction ∧, disjunction ∨, implication →, universal quantifier ∀, existential quantifier ∃, equal =." |
| Q139 | 13 | input_ontology | "Following (Russell and Norvig, 2010), we consider temporal logic and modal logic as special-purpose logics." |
| Q140 | 13 | input_ontology | "Consequently, they are beyond the scope of the definition of first-order logic used in our dataset." |
| Q141 | 13 | output_ontology | "We use n-place predicates when applicable for the expressivity of the FOL formulas." |
| Q142 | 13 | output_ontology | "However, we do not use the Davidsonian (Davidson, 2001) or neo-Davidsonian semantics (Parsons, 1990) because translating the majority of the FOL formulas in our dataset only requires one-place and two-place predicates." |
| Q143 | 14 | output_content | "We therefore design an annotation protocol for first-order logic translation in order to ensure that our FOL translations are as consistent as possible across all examples in our dataset." |
| Q144 | 14 | output_content | "First-order logic formulas need to preserve as much as possible the semantics of natural language sentences." |
| Q145 | 14 | output_content | "First-order logic formulas should stay as faithful to the structure of the original NL sentence as possible." |
| Q146 | 14 | output_content | "Semantic decomposition is not needed unless necessary for maintaining the NL expressivity." |
| Q147 | 14 | output_content | "In terms of abstraction, we neglect tense and remove all the plural forms of verbs." |
| Q148 | 14 | output_form | "Although there are many provers widely used in the community (McCune, 2005–2010; Sutcliffe, 2017; Nipkow et al., 2002), we adopt the inference engine provided in the Stanford CS221 course page, which is a compact module designed specifically for procesing first-order logic statements." |
| Q149 | 14 | output_form | "The inference engine does not support input in the FOL syntax adopted by standard education material (Russell and Norvig, 2010), which is used in our dataset." |
| Q150 | 14 | output_form | "We therefore developed a FOL parser in order to convert the FOL formulas written by humans to the input format of the inference engine." |
| Q151 | 14 | output_form | "The converter is a semantic parser tool written in Python." |
| Q152 | 14 | output_form | "Although LLMs such as GPT-4 can be utilized to conduct the conversion, it is hard to ensure the GPT-4 outputs are always correct." |
| Q153 | 14 | output_form | "Proving a story requires three steps. First, the FOL statements of the premises and conclusions of a story annotated by humans are converted to Python code. Then, the code snippets are used as input to the theorem prover. Finally, the theorem prover outputs whether the conclusions are True / False / Unknown, based on the premises." |
| Q154 | 14 | input_form | "We show the distribution of readability in Figure 3." |
| Q155 | 15 | output_form | "Confusion matrices in Figure 4 for the fine-tuning and 8-shot NL prompt results both show that LLMs are significantly better at making the correct predictions for conclusions with labels of True than the conclusions with labels of False or Unknown." |
| Q156 | 15 | output_form | "The accuracy on examples with False or Unknown conclusions is 61.9% with fine-tuning and 54.0% with few-shot prompting." |
| Q157 | 15 | output_form | "They also tend to make more predictions of True than the other labels." |
| Q158 | 15 | output_content | "To test if the premise ordering in FOLIO has spurious correlations with the conclusion label which a model can exploit, we shuffle the input premises to evaluate models." |
| Q159 | 15 | output_content | "We find that accuracy increases or decreases by roughly 1% in most settings compared to our unshuffled premises." |
| Q160 | 15 | output_content | "This indicates that the ordering of premises in FOLIO examples does not yield significant information about the label, and thus models will not be able to use the premise ordering as a strong heuristic or statistical feature for its predictions." |
| Q161 | 15 | output_ontology | "FOL formulas have a clearer and more straightforward logical structure than NL sentences." |
| Q162 | 15 | output_form | "As shown in Table 11, the performance slightly increases in the NL+FOL setting for GPT-4 while GPT-3.5 performs worse in both the NL+FOL and the FOL-only settings." |
| Q163 | 15 | output_form | "FOL always serves as additional useful information for GPT-4, but not for GPT-3.5 regardless of whether FOL is concatenated with NL." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://aclanthology.org/2024.acl-long.739/ |
| WEB-2 | https://arxiv.org/abs/2605.18155 |
| WEB-3 | https://arxiv.org/abs/2604.06196 |
| WEB-4 | https://stanford-cs221.github.io/autumn2022-extra/modules/logic/first-order-resolution.pdf |
| WEB-5 | https://arxiv.org/abs/2209.00840 |
| WEB-6 | https://arxiv.org/abs/2603.02788 |
| WEB-7 | https://github.com/Yale-LILY/FOLIO |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (default config)
**Analysis date:** 2025-01-31
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | FOLIO train | Ex 1 (story 271) | True | "No plants are fungi. Mushrooms are fungi." / conclusion: "No plants are mushrooms." | Two-premise syllogism with "No A are B" / "All C are B" form — structurally close to Hurley-style templates | IC, IO |
| D2 | FOLIO train | Ex 12 (story 257) | True | "Some cats are not pets. All cats are mammals." / conclusion: "Some mammals are not pets." | Minimal two-premise syllogism using Hurley-canonical forms ("Some A is not B", "All A are B") | IC, IO |
| D3 | FOLIO train | Ex 20 (story 269) | Uncertain | "All proteins are organic compounds. All enzymes are organic compounds." / conclusion: "All enzymes are proteins." | Two-premise syllogism illustrating classic undistributed-middle fallacy — directly analogous to Hurley course problems | IC, OO |
| D4 | FOLIO train | Ex 50 (story 284) | Uncertain | "Each building is tall. Everything tall has height." / conclusion: "All buildings are magnificent." | Minimal two-premise syllogism with irrelevant conclusion — indeterminate case, pedagogically transparent | IC, OO |
| D5 | FOLIO train | Ex 9 (story 264) | Uncertain | "No television stars are certified public accountants. All certified public accountants have good business sense." / conclusion: "All television stars have good business sense." | Two-premise syllogism, "No A are B" / "All B are C" form — near-Hurley template register | IC |
| D6 | FOLIO train | Ex 53 (story 37) | True | "Heptalogyy is a compound literary or narrative work that is made up of seven distinct works. The Harry Potter series consists of 7 distinct works." / conclusion: "The Harry Potter series of books is Heptalogy." | Simple two-premise syllogism with named entities; close to textbook form | IC |
| D7 | FOLIO train | Ex 2 (story 376) | Uncertain | "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises. People in this tech company who wear the same flannel shirts every day are consistent..." | Long naturalistic prose narrative with 7 premises and XOR embedded in premise — substantially more complex than Hurley problems | IC, IO |
| D8 | FOLIO train | Ex 3 (story 180) | Uncertain | "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac. Sam is using a Mac. If Sam uses a Mac, he will play a song." | 6-premise narrative scenario with chained conditionals and exclusive disjunction | IC, IO |
| D9 | FOLIO train | Ex 13 (story 395) | False | "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable...ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." | Complex branded-product scenario with 5 premises and compound conclusion | IC |
| D10 | FOLIO train | Ex 21 (story 381) | False | "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing...If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up..." | 6-premise Wikipedia-seeded narrative; convoluted tautological final premise | IC |
| D11 | FOLIO train | Ex 4 (story 408) | False | "No trick-shot artist in Yale's varsity team struggles with half court shots...Jack is on Yale's varsity team, and he is either a trick-shot artist or he successfully shoots a high percentage of 3-pointers." | Sports-domain narrative, 5 premises, label=False — tests invalid-conclusion case | OO, OC |
| D12 | FOLIO train | Ex 17 (story 70) | False | "Michael O'Donnell is a British physician, journalist, author, and broadcaster...Michael O'Donnell was born in Yorkshire as the son of a general practitioner." / conclusion: "There are no journalists that were born in Yorkshire." | WikiLogic biographical narrative; False label from clear counterexample in premises | OO, OC |
| D13 | FOLIO train | Ex 29 (story 210) | False | "The only types of mammals that lay eggs are either platypuses or echidnas...Grebes are not platypuses and also not echidnas." / conclusion: "Hyraxes lay eggs." | Biology-domain story; False conclusion via FOL entailment of negation | OO |
| D14 | FOLIO train | Ex 28 (story 252) | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency...There is an embargo on Russian foreign trade goods." / conclusion: "In Russia, an effective monetary policy is possible." | Economics-domain story; False via chain of conditionals; requires domain knowledge about Russia | IC |
| D15 | FOLIO train | Ex 6 (story 423) | Uncertain | "Everyone at the business conference is either an investor or an entrepreneur...Ho is at the business conference and prefers state ownership of the means of production." / conclusion: "Ho is not an ardent communist." | Unknown because ardent communist status is underdetermined given premises | OO |
| D16 | FOLIO train | Ex 22 (story 475) | Uncertain | "All PRC nationals are entitled to national social insurance coverage...Mei is at the Franco-China diplomatic conference." / conclusion: "Mei is a PRC national." | Diplomatic conference scenario; Uncertain because Mei's nationality not determinable | OO |
| D17 | FOLIO train | Ex 23 (story 108) | Uncertain | "The world's only major large passenger aircraft manufacturers are Boeing and Airbus...Airbus made more revenue than Boeing last year." / conclusion: "There exists a SpaceX commercial aircraft." | Conclusion about SpaceX is irrelevant to premises — clear indeterminate case | OO |
| D18 | FOLIO train | Ex 43 (story 393) | True | "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning...Modus Ponens is a component of a major part of reasoning rule." | Logic-domain story mentioning Modus Ponens — meta-logical content | IC |
| D19 | FOLIO train | Ex 7 (story 30) | Uncertain | "EndGame is a movie released in 2006...Andy Chang is from Hong Kong." / conclusion: "All of Andy Chang's movies are filmed outside of Washington." | WikiLogic film-domain story with insufficient premises to determine universal conclusion | IO, OO |
| D20 | FOLIO train | Ex 11 (story 486) | False | "Everything in Size Town is big or small...The bird is in Size Town and it is not both heavy and still." / conclusion: "If the bird is small or still, then it is either unpredictable or changing." | Abstract "Size Town" scenario; complex conditional conclusion with XOR | IC, OO |
| D21 | FOLIO train | Ex 16 (story 346) | True | "All professional athletes spend most of their time on sports...If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." / conclusion: "Amy is neither a full-time scientist nor an Olympic gold medal winner." | 6-premise chained syllogism with conditional; multi-step reasoning | IO |
| D22 | FOLIO train | Ex 33 (story 341) | Uncertain | "No battery-powered watch is automatic...Moonwatch is either a digital watch and an automatic, or it is neither." / conclusion: "Moonwatch is a mechanical watch." | Watch-domain story; mechanical watch status underdetermined from premises | OO |
| D23 | FOLIO train | Ex 38 (story 425) | False | "Everyone working at Meta has a high income...James has a car or works at Meta." / conclusion: "James is a student." | Modern tech-company scenario; False conclusion derivable via short chain | IC |
| D24 | FOLIO train | Ex 52 (story 337) | True | "No athletes never exercise...Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." (Note: conclusion uses "Jim" while premises use "John/Jim" inconsistently) | Name inconsistency between premises (John) and conclusion (Jim) — annotation quality issue | OC |
| D25 | FOLIO train | Ex 34 (story 377) | True | "All orphan planets are rogue planets...PSO J318.5−22 is a rogue planet." / conclusion: "PSO J318.5−22 is an orphan planet or it does not have the Sun as its star, or both." | Astronomy domain; complex disjunctive conclusion | IC |
| D26 | FOLIO train | Ex 56 (story 27) | Uncertain | "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin...Yangshuo is not a district in Guilin." / conclusion: "Kowloon District is in Hong Kong." | Irrelevant conclusion — Unknown because premises have nothing to say about Hong Kong | OO |
| D27 | FOLIO train | Ex 2 (story 376) | Uncertain | FOL premise: "¬(∃y (flannelShirt(y) ∧ WearEveryday(x, y)) ∧ Have(mike, highEnergy) ∧ Impulsive(mike)) → (Consistent(mike) ∧ StickTo(mike, theirRegularRoutine)) ⊕ ¬Like(mike, surprise)" | Malformed FOL — free variable `x` in antecedent of conditional; annotation error | OC |
| D28 | FOLIO train | Ex 57 (story 362) | False | "Matt does not invest in the public stock market regularly. Matt likes financial risks." / conclusion: "Matt is not at risk of a gambling addiction and Mike does not both read..." | Conclusion mentions "Mike" but premises are about "Matt" — name inconsistency in annotation | OC |
| D29 | FOLIO train | Ex 36 (story 422) | True | "Lily is in James' family; she watches TV series in cinemas." FOL: "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" | Missing closing parenthesis in FOL formula — syntactic annotation error | OC |
| D30 | FOLIO train | Ex 55 (story 477) | False | "TikTok is a social media application, and it is not ideal for preteens." / conclusion-FOL: "Contain(tikTok, chatFeature) ⊕ ComputerProgram(tikTok))" | Trailing unmatched parenthesis in conclusion-FOL | OC |
| D31 | FOLIO train | Ex 39 (story 243) | False | "If a person can distinguish the taste of different condiments, then they can also use different condiments for cooking...John can make meals which are popular at the party." / conclusion: "John cannot use different condiments for cooking." | 5-premise story; False conclusion derivable via clear chain | IO |
| D32 | FOLIO train | Ex 44 (story 474) | False | "All humans are capable of abstract thoughts. Plants are not capable of abstract thoughts...Hulu is a goat or a human." / conclusion: "If Hulu is either an animal or dirt, then Hulu is capable of abstract thoughts and is dirt." | XOR used in third premise in FOL but not NL; complex conditional conclusion | OC |
| D33 | FOLIO train | Ex 48 (story 92) | True | "Adventures of Rusty is a drama film and children's film. Columbia Pictures produced Adventures of Rusty." / conclusion: "Columbia pictures produced some drama film." | Simple existential conclusion from two-premise story | IO |
| D34 | FOLIO train | Ex 31 (story 60) | True | "All buildings in New Haven are not high...Tower A is managed by Yale Housing." / conclusion: "Tower A is low." (conclusion-FOL: ¬High(tower-a)) | Simple two-step chain; low premise count, close to textbook syllogistic form | IC |
| D35 | FOLIO train | Ex 10 (story 391) | Uncertain | "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" | Unmatched parenthesis in FOL formula — additional annotation error instance | OC |
| D36 | FOLIO train | Ex 46 (story 448) | Uncertain | "Someone is either a seasoned software engineer interviewer at Google, has human rights, or both." / premises-FOL: "∀x ((Seasoned(x) ∧ SoftwareEngineerInterviewer(x) ∧ At(x, google)) ∨ Have(x, humanRights))" | NL says "or both" (inclusive disjunction) but FOL uses ∨ — potential NL-FOL alignment gap | OC |
| D37 | FOLIO train | Ex 5 (story 348) | Uncertain | "All young adults at the event like independence...If Susan is a Yale student, then she does not like independence." / conclusion: "Susan is a college student." | 7-premise story with competing conditional chains; classic indeterminate case | OO |
| D38 | FOLIO train | Ex 8 (story 482) | Uncertain | "Harry, who lives in Potterville either yells or flies. Potter, who lives in Potterville, is a wizard and flies." / conclusion: "Harry is cool." | Fantasy-domain story; multiple conclusions from same story_id test same premises | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Three-way label schema maps directly onto the deployment rubric for FOL cases
- **Dimension(s):** OO, OC
- **Observation:** Across all 57 sampled examples, the three labels (True, False, Uncertain) appear in clear logical patterns consistent with the formally verified schema: False is assigned when the negation of the conclusion is provably entailed by the premises (not merely when the conclusion fails to follow), and Uncertain is assigned when premises are consistent with both the conclusion and its negation. The False examples in the sample (D11, D12, D13, D29, D38) all involve clear counterexamples entailed by premises, not merely absent entailment, aligning with the deployment's strict "invalid = premises entail negation" definition.
- **Deployment relevance:** The course's most exacting rubric requirement — that "invalid" requires positive entailment of the negation, not just failure to entail — is confirmed as operationally satisfied in the data examined. Annotators and the FOL prover jointly enforce this distinction.
- **Datapoint citations:**
  - [D12] Ex 17 (FOLIO train, label=False): "Michael O'Donnell is a British physician, journalist, author, and broadcaster...Michael O'Donnell was born in Yorkshire as the son of a general practitioner." / conclusion: "There are no journalists that were born in Yorkshire." — False because premises explicitly establish a counterexample (Michael O'Donnell is both a journalist and born in Yorkshire), confirming provable negation entailment rather than mere absence of entailment.
  - [D13] Ex 29 (FOLIO train, label=False): "Grebes are not platypuses and also not echidnas." / conclusion: "Hyraxes lay eggs." — False derivable via clear FOL chain through the exclusive mammal egg-laying premise; provable negation entailment confirmed.
  - [D11] Ex 4 (FOLIO train, label=False): "No trick-shot artist...struggles with half court shots...Jack is on Yale's varsity team, and he is either a trick-shot artist or he successfully shoots a high percentage of 3-pointers." / conclusion: "Jack is bad at mid-range shots." — False because either branch of the disjunction entails the negation.

#### Strength 2: Presence of minimal syllogistic examples close to Hurley-style template forms
- **Dimension(s):** IC
- **Observation:** A subset of examples — especially from the HybLogic pipeline and simpler WikiLogic stories — exhibit the short, template-like premise structures ("No A are B", "All C are B", "Some A is not B") that characterize Hurley-style course-packet problems, with low premise counts (2–3 premises) and clear categorical conclusions.
- **Deployment relevance:** These examples partially bridge the register gap between FOLIO's naturalistic prose and the course's Hurley-style templates. Models tested on FOLIO that perform well on this subset would demonstrate some relevant capability on the deployment's dominant input register.
- **Datapoint citations:**
  - [D1] Ex 1 (FOLIO train, label=True): "No plants are fungi. Mushrooms are fungi." / conclusion: "No plants are mushrooms." — Two-premise syllogism with canonical "No A are B" / "All C are B" structure directly paralleling Hurley examples.
  - [D2] Ex 12 (FOLIO train, label=True): "Some cats are not pets. All cats are mammals." / conclusion: "Some mammals are not pets." — Uses both "Some A is not B" and "All A are B" forms, core Hurley template patterns.
  - [D3] Ex 20 (FOLIO train, label=Uncertain): "All proteins are organic compounds. All enzymes are organic compounds." / conclusion: "All enzymes are proteins." — Classic undistributed-middle fallacy in bare "All A are B" form, highly representative of introductory logic course problems.
  - [D5] Ex 9 (FOLIO train, label=Uncertain): "No television stars are certified public accountants. All certified public accountants have good business sense." / conclusion: "All television stars have good business sense." — "No A are B" / "All B are C" form nearly identical to Hurley syllogism templates.
  - [D4] Ex 50 (FOLIO train, label=Uncertain): "Each building is tall. Everything tall has height." / conclusion: "All buildings are magnificent." — Minimal two-premise story with pedagogically transparent irrelevant-conclusion indeterminate case.

#### Strength 3: FOL operator coverage matches the deployment's second-half logical scope
- **Dimension(s):** IO
- **Observation:** The sampled examples contain all FOL operators the course requires for its second half: universal quantifier (∀), existential quantifier (∃), negation (¬), conjunction (∧), disjunction (∨), implication (→), exclusive disjunction (⊕), and equality (=). Examples span basic universal syllogisms, existential conclusions, chained conditionals, and combinations of quantifiers with connectives.
- **Deployment relevance:** The course's second-half FOL scope is comprehensively covered by the operator set observable in the data. A model scoring well on FOLIO would have been tested on all structural patterns relevant to the predicate-logic half of the course.
- **Datapoint citations:**
  - [D21] Ex 16 (FOLIO train, label=True): "All professional athletes spend most of their time on sports...If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." — Uses ∀, ∃ (via "all"), ¬, →, ∨ in combination across 6 premises.
  - [D8] Ex 3 (FOLIO train, label=Uncertain): "A project is written either in C++ or Python" → FOL uses ⊕ (exclusive disjunction) alongside ∀, ∃, →, ¬ — full operator set in a single story.
  - [D38] Ex 8 (FOLIO train, label=Uncertain): "All wizards in Potterville know magic...Harry, who lives in Potterville either yells or flies." — ∀, →, ¬, ⊕ in a chained multi-step reasoning structure.

#### Strength 4: Indeterminate (Unknown) label cases are clearly defined and pedagogically recognizable
- **Dimension(s):** OO
- **Observation:** The Uncertain/Unknown examples in the sample exhibit clearly recognizable patterns of logical underspecification: premises that are silent on a dimension needed to determine the conclusion (D15, D16, D17, D26), or premises that are consistent with both the conclusion and its negation due to insufficient information (D3, D22, D37). The course rubric's definition of indeterminate — "premises consistent with both the conclusion and its negation" — matches these cases precisely.
- **Deployment relevance:** The Unknown label's formal alignment with the course rubric is confirmed in the data. Students using the tool would receive "indeterminate" classifications on exactly the cases where neither entailment nor contradiction is provable, matching the intended pedagogical behavior.
- **Datapoint citations:**
  - [D17] Ex 23 (FOLIO train, label=Uncertain): "The world's only major large passenger aircraft manufacturers are Boeing and Airbus...Airbus made more revenue than Boeing last year." / conclusion: "There exists a SpaceX commercial aircraft." — Premises are entirely silent on SpaceX; neither conclusion nor its negation follows. Exemplary indeterminate case.
  - [D26] Ex 56 (FOLIO train, label=Uncertain): "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin...Yangshuo is not a district in Guilin." / conclusion: "Kowloon District is in Hong Kong." — Conclusion about Hong Kong is logically disconnected from premises about Guilin — paradigmatic indeterminate.
  - [D3] Ex 20 (FOLIO train, label=Uncertain): "All proteins are organic compounds. All enzymes are organic compounds." / conclusion: "All enzymes are proteins." — Undistributed middle; premises consistent with enzymes being or not being proteins.

#### Strength 5: Multi-step reasoning chains test the higher end of the course's FOL difficulty range
- **Dimension(s):** IO
- **Observation:** Many examples require 3–6 chained reasoning steps across multiple premises, with conclusions that can only be reached by tracing through multiple universal rules applied to specific individuals. This covers the deeper end of the reasoning depth distribution that the course's FOL section targets.
- **Deployment relevance:** While some FOLIO examples may be harder than typical course-packet problems, the presence of 3–5 step chains ensures the benchmark is not trivially solvable for the second-half FOL content and provides meaningful signal about model capability at the difficulty level instructors care about.
- **Datapoint citations:**
  - [D21] Ex 16 (FOLIO train, label=True): "All professional athletes spend most of their time on sports. All Olympic gold medal winners are professional athletes. No full-time scientists spend the majority of their time on sports. All Nobel physics laureates are full-time scientists. Amy spends the most time on sports, or Amy is an Olympic gold medal winner. If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." — 6-premise chain requiring case analysis.
  - [D38] Ex 8 (FOLIO train, label=Uncertain): Potterville scenario — 7 premises with chained wizard→magic→fly→cool chain; conclusion requires tracing through 4 steps.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete absence of propositional-logic (quantifier-free) examples
- **Dimension(s):** IO
- **Observation:** Every single example in the 57-item sample contains at least one universal (∀) or existential (∃) quantifier in the premises-FOL field. No quantifier-free example was observed. The YAML gap analysis and web search confirm this is a structural property of FOLIO, not a sampling artifact — the benchmark was designed around FOL predicate structures, and the FOL2NS paper explicitly characterizes quantifiers as the defining feature of FOLIO's logical scope.
- **Deployment relevance:** The course's first half is entirely propositional (connectives, truth tables, modus ponens, modus tollens, hypothetical syllogism, disjunctive syllogism, etc. — no quantifiers). If a model is assessed using FOLIO alone, there is zero coverage of approximately half the course's logical scope. A system that fails on propositional logic but succeeds on FOL would receive a misleadingly favorable evaluation. This is a deployment-critical gap for any tool intended to cover the full course.
- **Datapoint citations:**
  - [D1] Ex 1 (FOLIO train, label=True): "∀x (Plant(x) → ¬Fungi(x)) / ∀x (Mushroom(x) → Fungi(x))" — Even the simplest two-premise example uses universal quantifiers throughout; no quantifier-free propositional version exists in FOLIO.
  - [D4] Ex 50 (FOLIO train, label=Uncertain): "∀x (Building(x) → Tall(x)) / ∀x (Tall(x) → Height(x))" — The two shortest examples in the sample still use ∀; confirming no propositional subset.
  - [D2] Ex 12 (FOLIO train, label=True): "∃x (Cat(x) ∧ ¬Pet(x)) / ∀x (Cat(x) → Mammal(x))" — Minimal example uses both ∃ and ∀; no propositional-only FOLIO examples observed.

---

#### MAJOR

#### MAJOR Concern 1: Register mismatch — dominant FOLIO style is naturalistic prose, not Hurley-style templates
- **Dimension(s):** IC
- **Observation:** The majority of examples in the sample are naturalistic, topic-rich narratives substantially different from the bare template forms of Hurley-style course problems. Examples involve tech companies (D7), film directors (D19), diplomacy (D16), economics with Russia (D14), lipstick product lines (D9), and social media platforms (D23). The register is annotator-composed prose with epistemic qualifiers, complex noun phrases, and embedded real-world knowledge — the opposite of the syntactically constrained "All A are B" / "If P then Q" forms that dominate the course packet. While some simpler examples (D1, D2, D3, D5) approach Hurley register, they are a minority.
- **Deployment relevance:** Model performance on FOLIO's naturalistic prose may not predict performance on the course's dominant templated inputs. A model that successfully classifies "People in this tech company who wear the same flannel shirts every day are consistent" may still fail on "All A are B. Some B are not C. Therefore some A are not C." — and vice versa. Benchmark results may inflate or deflate apparent capability relative to the actual deployment inputs.
- **Datapoint citations:**
  - [D7] Ex 2 (FOLIO train, label=Uncertain): "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises. People in this tech company who wear the same flannel shirts every day are consistent and enjoy sticking to their regular routines." — Naturalistic narrative with embedded relative clauses and real-world scenario; maximally different from Hurley-style bare templates.
  - [D9] Ex 13 (FOLIO train, label=False): "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable...ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." — Branded-product prose with complex noun phrases; requires parsing product line terminology.
  - [D14] Ex 28 (FOLIO train, label=False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency...There is an embargo on Russian foreign trade goods." — Economics domain with contemporary geopolitical content; no structural equivalent in Hurley-style templates.
  - [D25] Ex 34 (FOLIO train, label=True): "All orphan planets are rogue planets...PSO J318.5−22 is a rogue planet." — Astronomy technical nomenclature ("PSO J318.5−22") requiring domain knowledge entirely absent from introductory logic course packets.

#### MAJOR Concern 2: Multiple annotation errors visible in the sampled data
- **Dimension(s):** OC
- **Observation:** The 57-item sample contains at least five distinct annotation errors or quality issues: (1) a free variable `x` in a FOL conditional antecedent (D27, story 376); (2) a name inconsistency between premises ("John") and conclusion ("Jim") (D24, story 337); (3) a name inconsistency between premises ("Matt") and conclusion ("Mike") in the conclusion text (D28, story 362); (4) a missing closing parenthesis in a FOL formula (D29, story 422; D30, story 477; D35, story 391); (5) a potential NL-FOL alignment gap where "either...or both" (inclusive disjunction) in NL is rendered as ∨ rather than explicitly verified (D36, story 448). These occur across different story IDs, suggesting this is not an isolated issue.
- **Deployment relevance:** A 2026 cleaning study cited in the web search found label errors and NL-FOL misalignments in the original FOLIO dataset. The sampled data confirms this concern is real and observable. For a deployment assessing model logic-checking capability, annotation noise in the ground truth directly undermines the validity of benchmark scores — a model might classify a mislabeled example "incorrectly" while reasoning correctly from the NL premises. The original (uncleaned) HuggingFace dataset should be used with caution.
- **Datapoint citations:**
  - [D27] Ex 2 (FOLIO train, story 376, label=Uncertain): FOL premise contains "¬(∃y (flannelShirt(y) ∧ WearEveryday(x, y)) ∧ Have(mike, highEnergy) ∧ Impulsive(mike)) → (Consistent(mike) ∧ StickTo(mike, theirRegularRoutine)) ⊕ ¬Like(mike, surprise)" — `x` is a free variable in the antecedent; this is a syntactic/semantic annotation error in the FOL.
  - [D24] Ex 52 (FOLIO train, story 337, label=True): Premises use "John" throughout; conclusion states "Jim is not a Knicks player." — Name inconsistency suggests a copy-paste or editing error in annotation.
  - [D28] Ex 57 (FOLIO train, story 362, label=False): Conclusion text reads "Matt is not at risk of a gambling addiction and Mike does not both read the Wall Street Journal..." — "Mike" appears in the conclusion while all premises discuss "Matt."
  - [D29] Ex 36 (FOLIO train, story 422, label=True): FOL premises contain "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" — missing closing parenthesis after `jameSFamily`.
  - [D35] Ex 10 (FOLIO train, story 391, label=Uncertain): FOL premises contain "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" — unmatched trailing parenthesis.

#### MAJOR Concern 3: Reasoning depth substantially exceeds typical introductory course-packet complexity
- **Dimension(s):** IO, IC
- **Observation:** Many examples in the sample require 4–7 chained reasoning steps and involve 5–8 premises with complex interactions among universal rules, conditional chains, and disjunctions. The course's introductory context involves 1–3 step arguments drawn from a structured textbook. FOLIO's documented mode reasoning depth is 4 steps with 28.7% requiring 5+, and the data confirms this — numerous examples involve extended chains not representative of introductory course problems.
- **Deployment relevance:** If a model struggles on deep FOLIO examples but would succeed on the 1–3 step problems in the course packet, FOLIO accuracy scores would underestimate actual deployment performance. Conversely, a model that performs adequately on FOLIO may be assessed as adequate when it could still fail on pedagogically simpler but register-distinct Hurley-style problems. The depth distribution mismatch distorts the benchmark's predictive validity for the deployment.
- **Datapoint citations:**
  - [D7] Ex 2 (FOLIO train, label=Uncertain): 7 premises with chained rules about tech company employees; final premise has an XOR embedded in a nested conditional structure — far beyond a first-semester logic student's typical 2–3 premise problem.
  - [D10] Ex 21 (FOLIO train, label=False): "All people who attend Renaissance fairs regularly enjoy dressing up...If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up in old-fashioned and historical period clothing." — 6 premises; convoluted tautological final premise requires 4–5 step reasoning.
  - [D21] Ex 16 (FOLIO train, label=True): 6-premise problem about Amy's professional status requiring complete case analysis across two disjuncts, spanning 4 distinct predicate categories.

#### MAJOR Concern 4: Label field uses "Uncertain" in HuggingFace data vs. "Unknown" in paper documentation
- **Dimension(s):** OO, OF
- **Observation:** The FOLIO paper and all citations consistently use "Unknown" as the third label category. However, in the actual HuggingFace dataset sampled, the third label appears as "Uncertain" (e.g., D3, D5, D15, D16, D22, D37). This is an inconsistency between the paper's documented label schema and the dataset schema in the deployed HuggingFace version. All 57 examples with a non-True/False label use "Uncertain," not "Unknown."
- **Deployment relevance:** For any automated pipeline that relies on the label strings from the HuggingFace dataset for evaluation, using "Unknown" (from the paper) as the target class label would cause a mismatch. This is a practical implementation concern that could invalidate accuracy calculations if not caught. The deployment tool's evaluation code must use "Uncertain" to match the actual data labels.
- **Datapoint citations:**
  - [D3] Ex 20 (FOLIO train, label=Uncertain): "All proteins are organic compounds. All enzymes are organic compounds." / label field value: "Uncertain" — paper documentation calls this "Unknown."
  - [D15] Ex 6 (FOLIO train, label=Uncertain): "Ho is at the business conference and prefers state ownership of the means of production." / conclusion: "Ho is not an ardent communist." — label field: "Uncertain."
  - [D37] Ex 5 (FOLIO train, label=Uncertain): Susan/Yale/Harvard event story — label field: "Uncertain."

---

#### MINOR

#### MINOR Concern 1: Test split not available in the HuggingFace dataset
- **Dimension(s):** OF
- **Observation:** The HuggingFace metadata shows only `train` (1,001 examples) and `validation` (203 examples) splits. The `test` split (226 examples, on which FOLIO's published results and majority baseline of 38.5% are computed) is not accessible in the public HuggingFace dataset. The analysis is based entirely on the training split.
- **Deployment relevance:** Benchmark comparisons to published model performance (GPT-4 64.16%, expert human 95.98%) are based on the test set. Users deploying FOLIO for assessment will need to use the validation set (203 examples) or the training set as a proxy, which may not precisely replicate published distributional statistics. This does not affect content validity observations but limits direct comparison to published baselines.
- **Datapoint citations:** (structural observation; no specific datapoint required)

#### MINOR Concern 2: Topic diversity includes content that may introduce construct-irrelevant domain knowledge requirements
- **Dimension(s):** IC
- **Observation:** Several WikiLogic examples presuppose domain-specific real-world knowledge that is not included in the premises and whose absence could affect whether a naive reader (or model without that knowledge) correctly identifies a classification. The economics-Russia example (D14) presupposes knowledge of what an embargo does; the lipstick example (D9) requires parsing branded product terminology; the astronomy example (D25) involves a technical astronomical designation.
- **Deployment relevance:** The deployment's course-packet problems are designed to be self-contained and domain-neutral, relying only on formal structure and explicitly stated premises. FOLIO's Wikipedia-seeded stories may introduce construct-irrelevant difficulty for models that lack the relevant world knowledge to parse the semantic content of the premises, creating a conflation between logical-reasoning ability and domain knowledge.
- **Datapoint citations:**
  - [D14] Ex 28 (FOLIO train, label=False): "The introduction of an embargo on foreign trade goods in a country leads to a sharp decrease in exports...There is an embargo on Russian foreign trade goods." — The logical chain depends on understanding what an embargo causes, which is given as a premise; however, the contemporary geopolitical context adds semantic load absent from Hurley-style problems.
  - [D25] Ex 34 (FOLIO train, label=True): "PSO J318.5−22 is a rogue planet" — Technical astronomical object name; while the premises are formally stated, the vocabulary creates parsing difficulty for readers unfamiliar with the domain.

#### MINOR Concern 3: Multiple conclusions drawn from a single story may create non-independence between test examples
- **Dimension(s):** IO, OF
- **Observation:** Several story_ids appear multiple times in the sample with different conclusions tested against the same premise set (story 408 appears as Ex 4, Ex 18, Ex 32; story 482 as Ex 8, Ex 19, Ex 30; story 70 as Ex 17, Ex 41; story 474 as Ex 44, Ex 49; story 436 as Ex 14, Ex 42; story 448 as Ex 46, Ex 47). This is by design (the benchmark is split by story, not by conclusion), but it means that per-example accuracy metrics treat correlated items as independent.
- **Deployment relevance:** If a model systematically misrepresents one story's premises, it will fail on all conclusions derived from that story, creating correlated errors that inflate apparent variance in model performance estimates. For deployment purposes, per-story accuracy may be a more informative metric than per-example accuracy, but this is not the primary reported metric.
- **Datapoint citations:**
  - [D11] and [D18] (both story 408): Same 5 premises about Yale varsity team; one tests "Jack is bad at mid-range shots" (False), the other tests a compound conditional conclusion (Uncertain) — shared premise set makes these non-independent.
  - [D38] Ex 8 and Ex 19 and Ex 30 (all story 482): Same Potterville premises tested with three different conclusions ("Harry is cool" / "Harry is not cool" / "Harry is a wizard or angry") — three dependent test items from one story.

---

### Content Coverage Summary

The 57 sampled examples span a wide range of topics: sports (basketball, basketball shooting), technology (software engineering, social media, computer science), biology (mammals, plants, fish), film, astronomy, economics, everyday scenarios (travel planning, family streaming subscriptions), and abstract fictional domains ("Size Town," "Potterville"). Approximately one-third of examples (estimated from the sample) come from short 2–4 premise stories that are structurally close to Hurley-style syllogistic forms; the remaining two-thirds involve 5–8 premise naturalistic narratives with complex logical interactions.

All examples use FOL predicate structures — universal and existential quantifiers are present in every example examined. No quantifier-free propositional example was found. The label distribution in the sample is approximately: True (~25%), False (~28%), Uncertain (~47%) — somewhat more Uncertain-heavy than the documented test set (27% Unknown), though this may reflect training set distribution differences.

The FOL annotations are generally well-formed but the sample reveals at least five distinct annotation errors (free variables, name inconsistencies, parenthesis mismatches) across different story IDs. The label field uses "Uncertain" rather than the paper-documented "Unknown." The register ranges from simple two-premise syllogisms in bare categorical form to complex multi-clause narratives with embedded real-world knowledge, with the naturalistic prose register predominating.

---

### Limitations

1. **Test split inaccessible**: All 57 examples are from the training split. The published performance baselines (GPT-4 64.16%, majority baseline 38.5%) are computed on the test split (226 examples), which is not available in the public HuggingFace repository. The training set may have a different label distribution or difficulty profile.

2. **Sample size**: 57 examples represent ~5.7% of the training set (1,001 examples) and ~4.7% of the combined train+validation set (1,204 examples). Topic and difficulty distributions observed may not fully represent the broader dataset.

3. **FOL annotation quality**: The FOL formulas (premises-FOL, conclusion-FOL fields) were inspected visually but not computationally verified against a theorem prover. The annotation errors noted (free variables, parenthesis mismatches, name inconsistencies) were identified by human inspection; there may be additional errors not visible through manual review of 57 examples.

4. **HybLogic vs. WikiLogic split**: The sample does not identify which pipeline produced each example. Conclusions about register (naturalistic vs. template-like) are inferred from content, not from a verified pipeline tag. The HybLogic subset (which would be most relevant to Hurley-style comparisons) cannot be isolated from this sample.

5. **Readability complexity**: The Dale-Chall readability distribution referenced in the paper (Figure 3) was not inspectable from the HuggingFace data. The claim that FOLIO examples are more complex than Hurley-style templates is inferred from content inspection, not from a computed readability comparison.

6. **Cleaned dataset**: The 2026 cleaning pipeline (using Vampire theorem prover) mentioned in the web search findings is not reflected in the current HuggingFace dataset. The label reliability concerns observed in the sample may be partially addressed by that cleaned version, which was not available for inspection.

