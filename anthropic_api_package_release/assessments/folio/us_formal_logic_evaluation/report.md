## Deployment Context

We are a US AI research lab evaluating LLM reasoning capabilities. We want to test whether the model can correctly classify the logical relationship (entailment, contradiction, or neutral) between a set of premises and a conclusion expressed in formal logical statements. Input is structured premise-conclusion pairs. Output is a categorical label. Our evaluation metric is classification accuracy.

# Validity Analysis: folio
**Target context:** US AI Research Lab — FOLIO FOL Reasoning Evaluation
**Overall risk:** LOW

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ✓ | 5 | Strong alignment | high |
| Input Content | 4 | Minor gaps | high |
| Input Form ⚠ | 3 | Moderate gaps | high |
| Output Ontology ✓ | 5 | Strong alignment | high |
| Output Content ✓ | 4 | Minor gaps | high |
| Output Form | 4 | Minor gaps | high |
| **Average** | **4.2** | | |

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

FOLIO is a strongly aligned benchmark for the US AI research lab's classical FOL reasoning evaluation, with five of six validity dimensions scoring 4–5. Input ontology and output ontology are exact matches: FOLIO's classical FOL operator coverage [Q138] and explicit temporal/modal exclusions [Q139, Q140] correspond precisely to the lab's in-scope and out-of-scope reasoning types, and the True/False/Unknown taxonomy maps cleanly onto entailment/contradiction/neutral per elicitation Q1. Output content is anchored in objective FOL-inference-derived labels [Q2, Q153], sidestepping most annotator-subjectivity concerns. The primary live concern, consistent with the lab's HIGH priority on input form, is the unresolved choice between pure-symbolic and hybrid NL+FOL presentation — FOLIO was designed and validated for NL-first presentation, and the paper itself documents that input format materially affects model scores [Q162, Q163]. Dataset analysis surfaces concrete annotation quality concerns: a direct NL/FOL semantic contradiction (Example 57, negation dropped) [DATASET-D17], multiple syntactic errors in FOL formulas, entity-name inconsistencies, and FOL over-specification patterns — corroborated by an independent 2025 study using the Vampire prover that established a cleaned validation set [WEB-5]. Output-form concerns are moderate: the HuggingFace dataset lacks the documented test split, the original GPT-4 ceiling has been substantially closed by neuro-symbolic pipelines (88.32% SotA) [WEB-4], and systematic label-class asymmetry [Q155-Q157] means aggregate accuracy can mislead without per-class reporting.

## Practical Guidance

### What This Benchmark Measures

For this lab's deployment, FOLIO provides a high-fidelity evaluation of classical first-order logic reasoning capability — specifically deductive entailment over premise-conclusion pairs with quantifiers, negation, conditionals, conjunction/disjunction, and multi-step chains (mode-4 depth, 28.7% at depth ≥5). The input_ontology (score 5) and output_ontology (score 5) dimensions show exact construct alignment, and output_content (score 4) confirms labels are anchored in objective FOL inference rather than subjective judgment. The benchmark cleanly supports the lab's three-way accuracy metric.

### Construct Depth

Construct depth is strong for the primary classification task and weaker for the symbolic-input regime. The NL-first design [Q64-Q68], NL-FOL alignment conventions [Q130-Q133], and per-sentence parallel annotation [DATASET-D1, D2] provide rich signal for hybrid evaluation. However, three depth limitations apply: (1) per-depth statistical power is limited at depth 6–7 (likely single-digit test examples) [WEB-6], (2) WikiLogic real-world entity references create a documented shortcut-reasoning confound [Q104, DATASET-D8, D10] — subcorpus-stratified analysis is needed, and (3) approximately 1–5% of sampled examples show NL/FOL annotation defects that may corrupt training signal for the secondary translation task [DATASET-D14-D17, D20-D21].

### What Else You Need

For the lab's specific use case: (1) If pursuing pure-symbolic evaluation (the input_form score-3 concern), supplement FOLIO with ProverQA [WEB-2] or LogicGraph [WEB-3], which are designed for symbolic-input regimes with depth stratification. (2) Verify whether to use the original or 2025-cleaned FOLIO annotations [WEB-5] — this directly affects output_content reliability. (3) Source the 226-example test split from FOLIO GitHub rather than HuggingFace (test split missing from HF). (4) Run subcorpus-stratified analysis (WikiLogic vs. HybLogic) to disentangle contamination effects from genuine deductive capability. (5) For frontier-model discriminability (output_form), supplement with LogiConBench [WEB-9] if FOLIO appears saturated under neuro-symbolic pipelines.

## Dimension Details

### Input Ontology — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
FOLIO's taxonomy aligns precisely with the lab's stated scope of classical deductive FOL. The benchmark covers all standard FOL operators (negation, conjunction, disjunction, implication, universal and existential quantifiers, equality) [Q138], uses n-place predicates for expressivity [Q141], explicitly excludes temporal and modal logic as out-of-scope [Q139, Q140] — matching the lab's out-of-scope list exactly — and emphasizes multi-step reasoning depth (mode=4, 28.7% at depth ≥5) [Q60]. The two-task structure (NL reasoning + NL-FOL translation) [Q63, Q67] covers both the lab's primary classification task and a documented secondary interest. Dataset analysis confirms all core operators are present in actual data, including exclusive disjunction (⊕) and quantifiers [DATASET-D3, D9, D13]. One minor caveat: per-depth example counts at depth 6–7 are likely too small for reliable per-depth statistical inference [WEB-6], but this affects statistical power, not taxonomic coverage.

**Strengths:**
- Full classical FOL operator coverage verified in both documentation and sampled data
- Explicit exclusion of out-of-scope sub-types (temporal, modal) matches the lab's scope precisely
- Substantially deeper reasoning-chain coverage (28.7% at depth ≥5) than prior FOL benchmarks (RuleTaker, LogicNLI)
- Multi-conclusion-per-premise design tests world-model consistency, not just isolated inference

**Checklist:**

- **IO-1**: Lab requires classical deductive FOL: quantifiers, negation, conditionals, conjunction/disjunction, multi-step deduction. All confirmed present in FOLIO documentation [Q138] and sampled data [DATASET-D3, D9, D13]. — _Sources: Q138, DATASET-D3, DATASET-D9, DATASET-D13_
- **IO-2**: No regionally-relevant categories omitted. The lab's in-scope list (classical deductive FOL) is precisely what FOLIO covers; out-of-scope items (temporal, modal, arithmetic, probabilistic) are explicitly excluded by FOLIO [Q139, Q140] and confirmed out-of-scope by the lab. — _Sources: Q139, Q140_
- **IO-3**: FOLIO does not include irrelevant categories beyond its declared scope; the NL-FOL translation secondary task is documented as a separate task with its own metrics [Q63, Q67, Q73-Q76], so it does not contaminate the primary classification metric. — _Sources: Q63, Q73-Q76_
- **IO-4**: No content-validity gaps in the taxonomy. Statistical-power concern at depth 6–7 is documented but is a sample-size issue, not a taxonomic gap [WEB-6]. — _Sources: WEB-6_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q138] 'We include the following operators: negation ¬, conjunction ∧, disjunction ∨, implication →, universal quantifier ∀, existential quantifier ∃, equal =.' (p.13)
- [Q139] 'Following (Russell and Norvig, 2010), we consider temporal logic and modal logic as special-purpose logics.' (p.13)
- [Q140] 'Consequently, they are beyond the scope of the definition of first-order logic used in our dataset.' (p.13)
- [Q60] '28.7% of the examples need five or more depths of reasoning to infer the conclusions' (p.5)
- [Q63] 'We define two new tasks based on FOLIO, natural language reasoning with first-order logic and NL-FOL translation.' (p.6)
- [Q141] 'We use n-place predicates when applicable for the expressivity of the FOL formulas.' (p.13)

*Web sources:*
- [WEB-6] FOLIO depth range 0–7, mode=4, 28.7% at depth ≥5 confirmed in EMNLP 2024 version

*Dataset analysis:*
- DATASET-D3: Exclusive disjunction (⊕) with universal quantifier observed in actual data
- DATASET-D9: Multi-step chain with negation, implication, and disjunction confirms operator diversity
- DATASET-D13: Negated conjunction in antecedent of implication; n-place predicate (BoundBy) confirmed
- DATASET-D24: 9-premise multi-step chain confirms high-depth examples are present

</details>

**Information gaps:**
- Per-depth example counts at depth 6–7 in the test set not published; depth 6–7 subsets likely single-digit counts

---

### Input Content — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input content is well-aligned for the lab's expert evaluator population in a US research lab context. FOLIO content consists of logically structured fictional stories with no consumer-facing cultural-loading concerns, expert-annotated by CS students/researchers [Q16, Q31] with explicit bias-screening (race, ethnicity, gender, sexuality, nationality, class, religion excluded) [Q47, Q127] and factual accuracy review [Q126]. The 4,351-word vocabulary spans diverse real-world topics [Q62], confirmed empirically across astronomy, geography, biology, economics, and media in the sample [DATASET-D13, D26, D28]. The primary concerns are (1) WikiLogic real-world entity references may overlap with LLM pretraining data, creating a shortcut-reasoning confound [Q104, DATASET-D8, D10] — explicitly flagged in the paper; and (2) NL-layer typos and grammar issues observed in training data despite documented quality control [DATASET-D7, D27]. Neither concern is fatal for an expert evaluator population that can perform subcorpus-stratified analysis (HybLogic vs. WikiLogic) [Q102].

**Strengths:**
- Identity-based bias screening was performed and 39.2% of stories rewritten [Q48, Q127]
- Broad topical coverage in sampled data confirms documented vocabulary breadth [DATASET-D13, D26, D28]
- Expert annotation with FOL training reduces semantic-content noise [Q31]
- Cultural loading is irrelevant to this expert US AI lab deployment per elicitation

**Checklist:**

- **IC-1**: Lab deployment is a US AI research lab with English-only content and expert evaluators; no region-specific cultural/geographic/dialectal knowledge requirements [elicitation cultural_norms_notes]. FOLIO's Wikipedia-seeded content spans diverse topics but does not require non-Western knowledge. — _Sources: Q47_
- **IC-2**: FOLIO explicitly excludes identity-based biases [Q47, Q127]; content is logical-structure-focused rather than culturally normative. Alignment with US research lab context is strong. — _Sources: Q47, Q127, Q126_
- **IC-3**: WikiLogic references real-world entities (Oxford Circus, Michael O'Donnell, John Nash) [DATASET-D8, D10] — these are Western-centric but the deployment is US-based, so this is a population match. However, real-world entity references create a documented contamination/shortcut-reasoning confound [Q104]. — _Sources: Q104, DATASET-D8, DATASET-D10_
- **IC-4**: Not applicable — expert AI researcher population in target context; regional annotator recruitment irrelevant per elicitation.
- **IC-5**: Content issues identified: (a) WikiLogic contamination risk [Q104], (b) typos and grammar issues in training data observed in sample [DATASET-D7, D27], (c) tautological premise in Example 13 [DATASET-D27]. None are fatal but introduce construct-irrelevant variance. — _Sources: Q104, DATASET-D7, DATASET-D27, WEB-5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q47] 'Our dataset prioritizes realism and factual accuracy, steering clear of biases and stereotypes linked to identity markers like race, ethnicity, gender, sexuality, nationality, class, and religion.' (p.4)
- [Q127] 'We took out stories that had strongly opinionated language and contained gender, racial, and classist biases.' (p.13)
- [Q126] 'We rewrote those that are not reflective of well-established scientific, historical, or legal facts.' (p.13)
- [Q62] 'our dataset has a vocabulary of 4,351 words, and the examples based on Wikipedia account for 74% of the total vocabulary' (p.5)
- [Q104] 'since the examples in WikiLogic are created from scratch by humans, it is possible that LLMs have seen similar texts with similar logical patterns in the training data.' (p.8)
- [Q48] 'we manually screened all stories and found that 39.2% of the stories suffer from at least one of these issues. We implemented a detailed protocol to rewrite these stories.' (p.4)

*Web sources:*
- [WEB-5] 2025 study found annotation errors in FOLIO requiring a cleaned validation set

*Dataset analysis:*
- DATASET-D7: Double-negative NL premise with two typos ('offical', 'Lipstcks') — NL quality issue in training data
- DATASET-D8: Real Wikipedia entity (Oxford Circus, John Nash) — WikiLogic contamination/shortcut risk
- DATASET-D10: Real Wikipedia person (Michael O'Donnell) with falsifiable world-knowledge conclusion
- DATASET-D13: Astronomy topic (PSO J318.5−22) — broad topical coverage confirmed
- DATASET-D26: Non-Western name ('Ho') and ideologically loaded content used as logical material — within deductive scope
- DATASET-D27: Tautological premise (p ∨ ¬p) with typos in NL

</details>

**Information gaps:**
- Rate of NL quality issues across the full corpus cannot be estimated from 57-example sample
- Whether lab uses cleaned (2025) or original FOLIO annotation set not specified

**Requires expert verification:**
- Whether contamination from Wikipedia-seeded stories materially affects model rankings for the lab's specific model set

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
This is the lab's highest-priority dimension and the analysis surfaces real concerns despite strong native-format alignment. FOLIO is fundamentally NL-first with parallel FOL annotations [Q64, Q65, Q37]; NL and FOL are designed to be logically and semantically equivalent [Q68], grammar-reviewed [Q49, Q50], and follow standard AI/education FOL syntax [Q52]. The parallel structure is empirically confirmed at sentence-level granularity [DATASET-D1, D2], and documented NL conventions (exclusive vs. inclusive disjunction, quantifier phrasing) are followed [DATASET-D3, D11]. This strongly supports NL-only and hybrid NL+FOL evaluation modes. However, three concerns reduce the score: (1) The paper explicitly documents that input format materially affects performance — adding FOL helps GPT-4 but hurts GPT-3.5 [Q162, Q163] — meaning a pure-symbolic regime is poorly matched to FOLIO's documented score distributions; this is the live unresolved decision flagged by the lab. (2) Dataset analysis reveals concrete NL-FOL alignment failures: a direct negation drop creating semantic contradiction [DATASET-D17], an entity-name mismatch (John/Jim) [DATASET-D16], unbalanced parentheses in multiple FOL formulas [DATASET-D14, D15, D20, D21], and FOL over-specification (double existential where single suffices) [DATASET-D6]. (3) Subcorpus AST diversity differs (WikiLogic: 53; HybLogic: 33) [Q106], affecting structural variety in the symbolic layer.

**Strengths:**
- Complete NL/FOL parallel annotation enables both NL-only and hybrid input modes out-of-the-box [DATASET-D1, D2]
- Documented NL conventions (⊕ for exclusive disjunction, ∨ for inclusive) consistently applied [DATASET-D3, D11]
- Standard AI/education FOL syntax (Russell & Norvig) used [Q52], aligning with lab researcher familiarity
- Grammar-reviewed NL with explicit ambiguity reduction protocols [Q49, Q50, Q51]

**Checklist:**

- **IF-1**: Signal-distribution mismatch is the central concern. FOLIO's documented scores derive from NL-first presentation [Q64]; paper explicitly shows FOL-only and NL+FOL settings produce different results across models [Q162, Q163]. Pure-symbolic regime will not generalize to/from FOLIO's documented score distributions; hybrid NL+FOL is well-supported. — _Sources: Q64, Q162, Q163, DATASET-D1_
- **IF-2**: Lab infrastructure (Python tooling, OpenAI API, standard NLP stack) fully supports all input formats; no infrastructure mismatch [elicitation infrastructure_notes].
- **IF-3**: Domain-specific form differences relevant to the lab's pipeline: (a) NL/FOL semantic alignment failures observed in sample [DATASET-D17], (b) syntactic errors in FOL [DATASET-D14, D15, D20, D21], (c) entity-name inconsistencies [DATASET-D16], (d) FOL over-specification of existentials [DATASET-D6]. These corrupt any FOL-only or hybrid presentation that relies on FOL fidelity. — _Sources: DATASET-D14, DATASET-D15, DATASET-D16, DATASET-D17, DATASET-D20, DATASET-D21, DATASET-D6_
- **IF-4**: Form mismatches that would harm external validity: (1) pure-symbolic regime is weakly aligned with FOLIO's NL-first design and validation; (2) NL/FOL annotation errors in the data create input-signal noise that may differentially affect hybrid vs. NL-only conditions; (3) AST diversity differs between subcorpora [Q106]. — _Sources: Q162, Q163, Q106, WEB-5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q64] 'Each natural language (NL) story S in FOLIO consists of n premises... and m conclusions' (p.6)
- [Q65] 'All NL stories are annotated with parallel FOL stories SF' (p.6)
- [Q68] 'each of the NL sentence pi or hi and the parallel FOL formula pfi or hfi should be logically and semantically equivalent.' (p.6)
- [Q52] 'We adopt the FOL definitions and syntax most widely used in the AI community (Russell and Norvig, 2010).' (p.5)
- [Q162] 'the performance slightly increases in the NL+FOL setting for GPT-4 while GPT-3.5 performs worse in both the NL+FOL and the FOL-only settings.' (p.15)
- [Q163] 'FOL always serves as additional useful information for GPT-4, but not for GPT-3.5 regardless of whether FOL is concatenated with NL.' (p.15)
- [Q106] 'WikiLogic has 53 ASTs while HybLogic has 33.' (p.8)
- [Q49] 'All the sentences are first checked with a grammar checking tool, Grammarly.' (p.4)

*Web sources:*
- [WEB-2] ProverQA (ICLR 2025) — pure-symbolic-compatible alternative if lab pursues that regime
- [WEB-1] ProntoQA — symbolic ontology-based alternative
- [WEB-3] LogicGraph — depth-stratified symbolic FOL benchmark
- [WEB-5] 2025 study identified annotation errors using Vampire prover, established cleaned set

*Dataset analysis:*
- DATASET-D1: Clean NL/FOL parallel at sentence level confirmed in actual data
- DATASET-D2: Multi-premise per-sentence FOL granularity confirmed
- DATASET-D3: NL 'either-or' → ⊕ convention applied correctly
- DATASET-D11: NL 'but not both' → ⊕ confirmed
- DATASET-D14: Missing closing parenthesis in FOL — syntactic error
- DATASET-D15: Missing closing parenthesis in FOL — syntactic error
- DATASET-D16: NL 'John' / FOL 'jim' name inconsistency
- DATASET-D17: CRITICAL — NL negation 'does not invest' dropped in FOL; direct semantic contradiction
- DATASET-D20: Unbalanced parenthesis in premises-FOL
- DATASET-D21: Extra closing parenthesis in conclusion-FOL
- DATASET-D6: FOL over-specifies existential (double ∃ where single suffices)

</details>

**Information gaps:**
- Rate of NL/FOL annotation errors across full corpus not quantified
- Whether the Stanford CS221 inference engine successfully resolved FOL syntactic errors via the Python parser bridge, or whether they propagated to label errors
- How pure-symbolic FOL-only presentation would interact with the observed FOL annotation errors

**Requires expert verification:**
- Whether the lab should use the original FOLIO dataset or the 2025 cleaned validation set
- Whether observed FOL annotation errors are present in the test split (not accessible via HuggingFace)

---

### Output Ontology — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
Output ontology is an exact match for the lab's deployment. FOLIO's three-way labels (True, False, Unknown) [Q36, Q66] map cleanly to the lab's three categories (entailment, contradiction, neutral) per elicitation Q1, with no sub-distinctions needed. The taxonomy is grounded in objective FOL inference rather than annotator subjectivity [Q2, Q70]. The label distribution in the test set is near-balanced (87 True / 78 False / 61 Unknown, 38.5% majority baseline) [Q94]. Dataset analysis confirms the Unknown label is used with logical precision rather than as a catch-all — complementary conclusions ('Harry is cool' and 'Harry is not cool') are both correctly labeled Uncertain when premises underdetermine them [DATASET-D19]. The only minor concern is the HuggingFace dataset uses the string 'Uncertain' rather than 'Unknown' [DATASET-D2], requiring a trivial string normalization. Temporal/modal exclusions [Q139, Q140] match the lab's out-of-scope list exactly.

**Strengths:**
- Three-way label maps directly to lab's entailment/contradiction/neutral with no residual ambiguity (confirmed by elicitation Q1)
- Ground truth determined by automated FOL inference engine, not annotator agreement [Q2, Q70]
- Near-balanced label distribution in test set [Q94]
- Empirical verification that Unknown reflects logical underdetermination [DATASET-D19]

**Checklist:**

- **OO-1**: Output categories (True/False/Unknown) are precisely relevant to the lab's three-way classification regime; elicitation Q1 confirmed clean mapping. — _Sources: Q36, Q66_
- **OO-2**: No missing regional categories. The lab confirmed no finer-grained distinctions within Unknown are needed. — _Sources: Q66_
- **OO-3**: No categories encode non-regional or value-laden assumptions; labels are anchored in formal logical validity [Q2, Q137]. — _Sources: Q2, Q137_
- **OO-4**: No stakeholder-driven redesign needed; taxonomy is formally objective. — _Sources: Q70_
- **OO-5**: No taxonomy issues. Minor implementation note: HF label string is 'Uncertain' not 'Unknown' [DATASET-D2] — string normalization only. 5% of conclusions have complex syntactic structure posing comprehension challenges [Q120] but this is a difficulty property, not a taxonomy issue. — _Sources: Q120, DATASET-D2_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q36] 'Each of the stories is composed of several premises and conclusions with truth values of True, False, or Unknown' (p.4)
- [Q66] 'Given P and H, the goal is to determine the truth values of the conclusions: "True", "False" or "Unknown", based on FOL reasoning.' (p.6)
- [Q70] 'the premises and conclusions are set up in such a way to ensure that the inference engine always returns an answer given enough resources' (p.6)
- [Q2] 'The logical correctness of the premises and conclusions is ensured by their FOL annotations, which are automatically verified by an FOL inference engine.' (p.1)
- [Q94] 'The majority baseline of our dataset is 38.5% since in our test set, there are 87, 78 and 61 examples with labels of true, false and unknown respectively.' (p.7)
- [Q137] 'FOL has no ambiguity while ambiguity can occur at various levels of NLP.' (p.13)

*Dataset analysis:*
- DATASET-D19: Complementary conclusions both labeled Uncertain confirms Unknown reflects logical underdetermination, not difficulty
- DATASET-D23: Conclusion introducing predicate absent from premises correctly labeled Uncertain
- DATASET-D28: Unrelated conclusion correctly labeled Uncertain — exemplifies Unknown semantics
- DATASET-D2: HF dataset uses 'Uncertain' label string vs. paper's 'Unknown' — implementation note

</details>

---

### Output Content — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output content (label correctness) is anchored in objective formal logical validity rather than annotator subjectivity, eliminating most convergent-validity concerns for the primary task [Q2, Q57, Q153]. A rigorous multi-stage QA process was used: NL quality review separated from FOL quality review [Q29, Q124, Q125], standardized FOL annotation protocol [Q54, Q143-Q146], commonsense premises explicitly added at alignment stage [Q55], and 39.2% of stories rewritten in QA [Q48]. Expert/non-expert accuracy gap (95.98% vs. 61.82%) [Q111] confirms the task genuinely requires FOL expertise and the labels are not noise. However, dataset analysis surfaces concrete label-correctness concerns: (1) a direct NL/FOL semantic contradiction in Example 57 (negation dropped) [DATASET-D17] means the label may be computed from incorrect FOL; (2) syntactic errors in FOL formulas [DATASET-D14, D15, D20, D21] could corrupt inference engine output; (3) FOL over-specification (double existential) [DATASET-D6] and atypical formulations [DATASET-D25] suggest annotation-protocol inconsistencies. A 2025 study using the Vampire prover identified errors requiring a cleaned validation set [WEB-5]. Annotator demographics beyond English proficiency and FOL training are not documented [Q122, Q123] — relevant if this were a subjective task, but largely moot here since labels are inference-engine-derived.

**Strengths:**
- Labels objectively determined by automated FOL inference engine, not subjective judgment [Q2, Q153]
- Rigorous multi-stage QA pipeline with role-separated expert review [Q29, Q124, Q125]
- Standardized FOL annotation protocol to minimize translation inconsistencies [Q54, Q143-Q146]
- Expert human ceiling (95.98%) provides meaningful upper bound [Q111]

**Checklist:**

- **OC-1**: Ground truth reflects formal logical validity rather than stakeholder perspective; the lab's expert population is precisely the population whose judgments the FOL-engine-derived labels approximate [Q2, Q111]. — _Sources: Q2, Q111_
- **OC-2**: Minimal disagreement risk: ground truth is mechanically derived from FOL premises, and the lab's expert population shares the source culture (FOL-trained CS researchers). Expert annotators achieved 95.98% on FOLIO [Q111]. — _Sources: Q2, Q111_
- **OC-3**: Annotator demographics partially documented: native/near-native English, CS students/researchers with formal FOL education [Q27, Q28, Q122, Q123]. Gender, racial, and institutional diversity NOT documented — INSUFFICIENT DOCUMENTATION, but largely moot given objective grounding. — _Sources: Q27, Q28, Q122, Q123_
- **OC-4**: Not needed — labels are inference-engine-derived; regional annotator pool re-annotation would not change formal-logical ground truth. — _Sources: Q2, Q153_
- **OC-5**: Aggregation methods not relevant — single ground-truth label per conclusion derived from FOL prover, not majority vote. — _Sources: Q70_
- **OC-6**: Label issues identified: (1) NL/FOL semantic mismatch in Example 57 [DATASET-D17] — if label was computed from FOL, it may not match what NL premises imply; (2) syntactic errors in FOL [DATASET-D14, D15, D20, D21] may have corrupted inference engine output or required manual override; (3) 2025 study found errors warranting cleaning [WEB-5]. — _Sources: DATASET-D17, DATASET-D14, DATASET-D15, DATASET-D20, DATASET-D21, WEB-5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'The logical correctness of the premises and conclusions is ensured by their FOL annotations, which are automatically verified by an FOL inference engine.' (p.1)
- [Q29] 'At the NL quality check stage, only annotators who are experts in natural language processing or computational linguistics are involved. For the FOL quality check, only annotators who are experts in first-order logic are involved.' (p.4)
- [Q54] 'we design an annotation protocol for FOL translation in order to ensure that our FOL translations are as consistent as possible across all examples in our dataset.' (p.5)
- [Q53] 'In preliminary investigations, we found that the human-written FOL formulas suffer from FOL consistency issues, which necessitates an additional round of quality control for FOL formulas.' (p.5)
- [Q48] '39.2% of the stories suffer from at least one of these issues. We implemented a detailed protocol to rewrite these stories.' (p.4)
- [Q111] 'Expert annotations achieve an accuracy of 95.98% while non-expert annotations achieves 61.82%, with a gap of 34.16%.' (p.9)
- [Q122] 'Our annotators are either college or graduate students who are native English speakers or possess near-native proficiency in English.' (p.12)
- [Q153] 'the theorem prover outputs whether the conclusions are True / False / Unknown, based on the premises.' (p.14)

*Web sources:*
- [WEB-5] 2025 study using Vampire theorem prover found annotation errors in public FOLIO, established cleaned validation set; auto-formalization baseline 86.70% on cleaned set

*Dataset analysis:*
- DATASET-D17: CRITICAL — NL 'does not invest' / FOL 'InvestInRegularly(matt, ...)' direct semantic contradiction
- DATASET-D14: Syntactic error (missing parenthesis) in FOL formula
- DATASET-D15: Syntactic error (missing parenthesis) in FOL formula
- DATASET-D16: Entity name inconsistency (John in NL, jim in FOL)
- DATASET-D20: Unbalanced parenthesis in FOL
- DATASET-D21: Extra closing parenthesis in FOL
- DATASET-D6: FOL over-specifies 'some' as double existential
- DATASET-D25: Conditional inside existential scope — atypical FOL formulation
- DATASET-D12: Predicate typo 'StongNationalCurrency' consistent in premises and conclusion

</details>

**Information gaps:**
- Rate of label-corruption due to NL/FOL annotation errors across the full corpus
- Whether the inference engine produced labels using corrected FOL (post-QA) or whether visible FOL errors in the HF data correspond to label-affecting errors
- Annotator demographics beyond English proficiency and FOL training

**Requires expert verification:**
- Whether lab uses original or 2025-cleaned FOLIO annotations
- Sample-based audit of label correctness against an independent FOL prover (e.g., Vampire or Prover9) to estimate label-noise rate

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output form aligns well for the primary task: classification accuracy on three-way categorical labels [Q80] matches the lab's exact intended metric. Premise ordering has been verified not to be exploitable as a positional heuristic [Q158, Q159, Q160], reinforcing metric robustness. For the secondary NL-FOL translation task, both Syntactic Validity (SynV) [Q73, Q74] and Inference Engine Execution Accuracy (ExcAcc) [Q75, Q76] are defined separately, supporting clean task separation. However, three concerns prevent a 5: (1) The original GPT-4 ceiling (53.1% on HybLogic) [Q20] is now substantially closed by neuro-symbolic pipelines (LLM-ARC 88.32% vs. human 95.98%) [WEB-4], creating a discriminability bifurcation between standard prompting and neuro-symbolic regimes — ceiling concern is reduced but remains live for standard prompting [WEB-4]. (2) Systematic label-class asymmetry: accuracy on False/Unknown is 54.0% few-shot vs. 61.9% fine-tuning, much lower than True [Q155, Q156, Q157] — the lab must account for this when interpreting aggregate accuracy. (3) Test split is not present in the HuggingFace dataset [DATASET concern 4]; only train (1,001) + validation (203) are available, reducing statistical power for primary evaluations on the documented test split (226 examples).

**Strengths:**
- Classification accuracy metric is an exact match for lab's intended evaluation regime [Q80]
- Premise-ordering robustness empirically verified [Q158-Q160]
- Separate SynV and ExcAcc metrics enable clean task separation for NL-FOL translation [Q73-Q76]
- Human expert ceiling (95.98%) provides interpretable upper bound [Q111, Q113]

**Checklist:**

- **OF-1**: Output modality matches exactly: categorical three-way label for primary task [Q80]; SynV/ExcAcc for secondary translation task [Q73-Q76]. Both align with lab's stated metrics. — _Sources: Q80, Q73, Q75_
- **OF-2**: Not applicable — no speech-based output requirements in this deployment.
- **OF-3**: Not applicable — expert evaluator population in well-resourced lab environment.
- **OF-4**: Form mismatches: (a) HF dataset lacks test split [DATASET concern 4]; primary documented performance comparisons reference the unavailable 226-example test set, so lab must obtain it from FOLIO GitHub or use validation set with reduced power (n=203). (b) Ceiling concern is partially resolved for neuro-symbolic pipelines [WEB-4] but remains live for standard prompting baselines on frontier models (GPT-4o, Claude 3.5, Gemini 1.5) which are not publicly documented [WEB-4]. (c) Systematic label-class asymmetry [Q155-Q157] means aggregate accuracy can mislead — per-class reporting is needed. — _Sources: Q20, Q156, WEB-4, WEB-5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q80] 'We use accuracy for evaluating logical reasoning performance.' (p.6)
- [Q73] 'Two metrics are adopted to evaluate NL-FOL translation... Syntactic validity (SynV)' (p.6)
- [Q75] 'Inference Engine execution accuracy (ExcAcc).' (p.6)
- [Q158] 'we shuffle the input premises to evaluate models.' (p.15)
- [Q160] 'the ordering of premises in FOLIO examples does not yield significant information about the label' (p.15)
- [Q156] 'The accuracy on examples with False or Unknown conclusions is 61.9% with fine-tuning and 54.0% with few-shot prompting.' (p.15)
- [Q155] 'LLMs are significantly better at making the correct predictions for conclusions with labels of True than the conclusions with labels of False or Unknown.' (p.15)
- [Q20] 'the most capable publicly available LLM so far achieves only 53.1% on the stories written in a hybrid manner, which is slightly better than random.' (p.2)
- [Q113] 'The expert and GPT-4 gap is 31.82%, suggesting significant room for model improvement.' (p.9)
- [Q96] 'The syntactic validity scores are around 93% with both GPT-3.5-Turbo and GPT-4.' (p.8)
- [Q97] 'GPT-3.5-Turbo and GPT-4 are not yet good at translating an NL story to a logically or semantically similar FOL counterpart' (p.8)

*Web sources:*
- [WEB-4] LLM-ARC neuro-symbolic system achieves 88.32% on FOLIO validation (2024 SotA)
- [WEB-5] Auto-formalization agent 86.70% on cleaned FOLIO vs. 73.89% CoT baseline
- [WEB-9] LogiConBench designed to remain discriminative when existing benchmarks saturate

*Dataset analysis:*
- HF Metadata observation: only train (1001) and validation (203) splits available; documented 226-example test split absent — reduces statistical power for replicating documented baselines

</details>

**Information gaps:**
- Vanilla prompting baselines for GPT-4o, Claude 3.5, Gemini 1.5 on FOLIO not publicly documented [WEB-4]
- Per-depth example counts at depth 6–7 — likely too small for reliable per-depth accuracy estimates [WEB-6]
- Test set availability via HuggingFace — must be sourced from GitHub

**Requires expert verification:**
- Whether the lab's specific evaluation paradigm (standard prompting vs. neuro-symbolic) maintains discriminability for its target frontier-model set
- Statistical power analysis for per-depth and per-label-class metrics on the lab's chosen evaluation split

---

## Remediation Suggestions

### Input Form ⚠

**Gap:** FOLIO is NL-first; pure-symbolic regime is weakly aligned with documented score distributions, and NL/FOL annotation errors observed in sample data corrupt FOL-only and hybrid signals

**Recommendation:** Restrict primary FOLIO evaluation to NL-only or hybrid NL+FOL conditions. For pure-symbolic evaluation, use ProverQA (ICLR 2025) or LogicGraph as primary; treat FOLIO FOL-only as ablation only. Apply the 2025 Vampire-cleaned annotation set (or equivalent QA pass) before any FOL-input experiments.

### Input Content

**Gap:** WikiLogic real-world entity references create contamination/shortcut-reasoning confound; HybLogic vs. WikiLogic subcorpus tag is not in the HuggingFace schema

**Recommendation:** Cross-reference the FOLIO GitHub repository to tag each example with its subcorpus origin. Report HybLogic and WikiLogic accuracies separately to disentangle genuine deductive capability from world-knowledge shortcuts.

### Input Ontology

**Gap:** Per-depth example counts at depth 6–7 are likely single-digit in the test set, limiting statistical reliability of per-depth performance estimates

**Recommendation:** When reporting per-depth performance, aggregate to depth bands (0–3, 4–5, 6+) rather than per-depth points, and provide confidence intervals. For finer-grained depth analysis, supplement with ProverQA which provides 500 examples per difficulty band.

### Output Content

**Gap:** Direct NL/FOL semantic contradictions and syntactic errors observed in sampled training data; 2025 study confirmed corpus-wide annotation errors warranting cleaning

**Recommendation:** Use the 2025 cleaned FOLIO validation set (or run an independent Vampire/Prover9 pass to identify and exclude examples with corrupted FOL or NL/FOL mismatches). Report results on both cleaned and original annotation sets to allow comparison with published baselines.

### Output Form

**Gap:** HuggingFace dataset lacks the documented 226-example test split; using only validation (n=203) reduces statistical power for per-depth and per-label-class analyses

**Recommendation:** Source the 226-example test split directly from the FOLIO GitHub repository. Report per-label-class accuracy (True / False / Unknown) separately given the documented systematic asymmetry [Q155-Q157], and treat per-depth scores at depth 6–7 as indicative only due to small subset sizes.

### Output Form

**Gap:** Standard-prompting ceiling for frontier models (GPT-4o, Claude 3.5, Gemini 1.5) on FOLIO is not publicly documented; neuro-symbolic SotA is 88.32% vs. human 95.98%, leaving discriminability uncertain for frontier prompting

**Recommendation:** Before deploying FOLIO as a discriminative benchmark, run a calibration pass on the lab's target frontier models with the lab's chosen prompting strategy. If ceiling effects emerge, supplement with LogicGraph or LogiConBench for harder depth tiers.

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
| Q20 | 2 | output_form | "Under the few-shot setting, the most capable publicly available LLM so far achieves only 53.1% on the stories written in a hybrid manner, which is slightly better than random." |
| Q21 | 2 | input_content | "We release a natural language reasoning dataset written by expert annotators, FOLIO, with first-order logical reasoning problems." |
| Q22 | 2 | input_form | "We use formal logic, i.e., FOL to ensure the logical validity of the examples written in NL and propose a new NL-FOL translation task." |
| Q23 | 2 | output_form | "We benchmark the performance of LMs by fine-tuning models and prompting LLMs with few-shot examples, on the FOLIO reasoning task." |
| Q24 | 3 | output_content | "We collected FOLIO through a carefully designed manual annotation process to achieve high-quality examples that necessitate complex logical reasoning." |
| Q25 | 3 | output_content | "Writing natural language reasoning stories with FOL requires sufficient knowledge in both semantic parsing and first-order logic, as well as strong analytical skills." |
| Q26 | 3 | output_content | "Given the complexities of such annotations, we selected annotators based on a few important criteria to ensures that our dataset is annotated with the highest level of precision and expertise, reflecting the complexity and nuance required for first-order logical reasoning." |
| Q27 | 3 | output_content | "Our annotators are either college or graduate students who are native English speakers or possess near-native proficiency in English." |
| Q28 | 3 | output_content | "They possess formal education in first-order logic, having either completed relevant coursework or undertaken self-directed studies in first-order logic or seman-" |
| Q29 | 4 | output_content | "At the NL quality check stage, only annotators who are experts in natural language processing or computational linguistics are involved. For the FOL quality check, only annotators who are experts in first-order logic are involved." |
| Q30 | 4 | output_content | "We also give the annotators several training sessions on how to write a story, by providing them with detailed annotation guidelines." |
| Q31 | 4 | output_content | "All stories and FOL annotations in FOLIO are written and reviewed by expert annotators, including CS undergraduate and graduate students, and senior researchers, who met the aforementioned criteria." |
| Q32 | 4 | input_content | "We develop our dataset in six stages: WikiLogic collection, HybLogic collection, NL quality control, FOL quality control, NL-FOL alignment and FOL verification, spending 980 man-hours in total." |
| Q33 | 4 | input_content | "We collected our dataset using two different methods in order to obtain examples that are both logically diverse and complex and have abundant abstract syntax tree (AST) variations." |
| Q34 | 4 | input_content | "WikiLogic: annotation from scratch using Wikipedia articles as seeds. At this annotation stage, the annotators are asked to select random Wikipedia pages by repeatedly using the Wikipedia Special Random link. The Wikipedia articles are used to develop ideas for topics to write new stories." |
| Q35 | 4 | input_form | "We ask the annotators to create new stories from scratch without using templates based on real-world knowledge, which should be plausible in general." |
| Q36 | 4 | output_ontology | "Each of the stories is composed of several premises and conclusions with truth values of True, False, or Unknown (see Table 2 for an example)." |
| Q37 | 4 | input_form | "We also ask the annotators to write parallel FOL sentences for both the premises and conclusions." |
| Q38 | 4 | input_content | "This results in a wide range of topics, abundant AST variations, and a wide vocabulary for FOLIO." |
| Q39 | 4 | input_content | "HybLogic: hybrid annotation The task of generating logically sound stories from scratch for a set of facts is very time-consuming for human writers, where the main challenge is to create complex and varied logical patterns to arrive at a conclusion." |
| Q40 | 4 | input_content | "To address the problems of solely using manual annotation, we also consider a hybrid approach to facilitate the process. Our hybrid method is based on a common form of logical stories: syllogisms." |
| Q41 | 4 | input_ontology | "A syllogism consists of two premises and a single conclusion, and the conclusion states some facts about the entities and categories in the premises." |
| Q42 | 4 | input_content | "In this approach, we first generate logically valid stories, which are templates containing abstract categories and entities, by combining multiple syllogisms into a single story template: the conclusion of one syllogism is used as a premise for the next syllogism." |
| Q43 | 4 | input_ontology | "There are 256 logically distinct types of syllogisms and 24 of them are valid (Lehman, 1973). We use various combinations of 24 valid syllogisms. We also add in conjunction, disjunction, and implication." |
| Q44 | 4 | input_content | "We then ask human annotators to assign nouns, phrases, or clauses to the abstract entities or categories that reflect real-life scenarios to each template and write logically-valid stories in natural language." |
| Q45 | 4 | input_form | "The usage of the template is to ensure that we have a set of varied and complex logical stories with multiple conclusions. There are many ways of expressing the same logic template in natural language, and so the generated templates augment, rather than limit, the creativity of humans." |
| Q46 | 4 | output_content | "To ensure the highest quality of the dataset, we dedicated considerable attention to the following key aspects of the natural language sentences during the quality control process." |
| Q47 | 4 | input_content | "Our dataset prioritizes realism and factual accuracy, steering clear of biases and stereotypes linked to identity markers like race, ethnicity, gender, sexuality, nationality, class, and religion." |
| Q48 | 4 | output_content | "Toward these objectives, we manually screened all stories and found that 39.2% of the stories suffer from at least one of these issues. We implemented a detailed protocol to rewrite these stories." |
| Q49 | 4 | input_form | "Apart from grammar, we make sure the sentences in our dataset are highly natural. All the sentences are first checked with a grammar checking tool, Grammarly." |
| Q50 | 4 | output_content | "Our annotators who have graduated from or are senior students studying English Literature conducted a thorough round of review for grammatical correctness and language naturalness." |
| Q51 | 4 | input_form | "We also eliminate natural language ambiguity when it is possible." |
| Q52 | 5 | input_form | "We adopt the FOL definitions and syntax most widely used in the AI community (Russell and Norvig, 2010)." |
| Q53 | 5 | output_content | "In preliminary investigations, we found that the human-written FOL formulas suffer from FOL consistency issues, which necessitates an additional round of quality control for FOL formulas." |
| Q54 | 5 | output_content | "One NL sentence can be translated into FOL through multiple non-equivalent ways. For example, sometimes additional information inferred from a sentence can be represented in FOL, leading to multiple representations. We therefore design an annotation protocol for FOL translation in order to ensure that our FOL translations are as consistent as possible across all examples in our dataset." |
| Q55 | 5 | output_content | "Apart from checking whether NL and FOL express equivalent meanings, we also add necessary commonsense knowledge in both the NL and FOL premises. Sometimes humans do not write certain commonsense knowledge in the premises that is required in the FOL reasoning process, which is based solely on the premises given. We add such knowledge as additional premises at this stage." |
| Q56 | 5 | input_form | "In particular, intrinsic properties of some predicates are required in the FOL reasoning process. For example, "LocatedIn(x,y)" should be transitive and "BeFamily(x,y)" should be symmetric." |
| Q57 | 5 | output_content | "Recognizing that the FOL formula annotations can be error-prone, we verify the syntactic validity and label consistency of FOL formula annotations with an FOL inference engine." |
| Q58 | 5 | input_content | "Table 3 shows that examples based on Wikipedia make up the largest portion of FOLIO, with 304 stories, 1,353 NL and FOL premise pairs, and 753 NL and FOL conclusion pairs. Hybrid annotations consist of 183 stories with 1,054 NL and FOL premise pairs, and 682 NL and FOL conclusion pairs in total." |
| Q59 | 5 | input_form | "We use the Dale-Chall Readability Formula (Dale and Chall, 1948, 1995) to show the text complexity of FOLIO following (Singh et al., 2023; Arps et al., 2022; Wei et al., 2021)." |
| Q60 | 5 | input_ontology | "As shown in Figure 1, the mode of reasoning depths is four in FOLIO. 28.7% of the examples need five or more depths of reasoning to infer the conclusions, while the previous datasets needed at most five reasoning depths as shown in Table 1." |
| Q61 | 5 | input_ontology | "Table 1 shows that FOLIO also has a much larger number of distinct ASTs than the previous datasets, indicating that FOLIO is much more logically diverse." |
| Q62 | 5 | input_content | "Table 3 shows that our dataset has a vocabulary of 4,351 words, and the examples based on Wikipedia account for 74% of the total vocabulary even though the WikiLogic stories take up only 63% of the total number of stories." |
| Q63 | 6 | input_ontology | "We define two new tasks based on FOLIO, natural language reasoning with first-order logic and NL-FOL translation." |
| Q64 | 6 | input_form | "Each natural language (NL) story S in FOLIO consists of n premises: P = {p1, p2, ..., pn} and m conclusions: H = {h1, h2, ..., hm}." |
| Q65 | 6 | input_form | "All NL stories are annotated with parallel FOL stories SF, which are sets of FOL formulas consisting of n premises PF = {pf1, pf2, ..., pfn} and m conclusions HF = {hf1, hf2, ..., hfm}." |
| Q66 | 6 | output_ontology | "Given P and H, the goal is to determine the truth values of the conclusions: "True", "False" or "Unknown", based on FOL reasoning." |
| Q67 | 6 | input_ontology | "We propose a new natural language to first-order logic translation (NL-FOL translation) task alongside our reasoning dataset." |
| Q68 | 6 | input_form | "In particular, each of the NL sentence pi or hi and the parallel FOL formula pfi or hfi should be logically and semantically equivalent." |
| Q69 | 6 | input_form | "Moreover, the truth values for the conclusions should be the same based on the NL story S and the parallel FOL story FS." |
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
| Q85 | 7 | input_form | "We fine-tune the base and large versions of both BERT and RoBERTa, with an additional two-layer classification layer to predict the truth values." |
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
| Q103 | 8 | input_ontology | "We hypothesize that this is because HybLogic has high logical complexity that the SoTA LLMs like GPT-4 cannot solve yet while WikiLogic examples require shorter reasoning chains which the model is already capable of solving." |
| Q104 | 8 | input_content | "Moreover, since the examples in WikiLogic are created from scratch by humans, it is possible that LLMs have seen similar texts with similar logical patterns in the training data." |
| Q105 | 8 | input_content | "However, fine-tuning RoBERTa-large achieves higher performance on HybLogic than on WikiLogic. This is likely because HybLogic is created from templates and some of the logical patterns can be learned during fine-tuning." |
| Q106 | 8 | input_form | "In NL-FOL translation, performs 10 points better on HybLogic than WikiLogic. This could be because WikiLogic has more distinct and diverse sentence-level logical and language patterns and FOL annotations. WikiLogic has 53 ASTs while HybLogic has 33." |
| Q107 | 9 | output_content | "We collected truth value annotations of logical reasoning for FOLIO test set from expert and non-expert annotators." |
| Q108 | 9 | output_content | "Our expert annotators are computer science college students familiar with FOL." |
| Q109 | 9 | output_content | "Non-expert annotators are community college or high school students who have not taken the SAT." |
| Q110 | 9 | output_content | "Both expert and non-expert annotators are native English speakers." |
| Q111 | 9 | output_content | "Expert annotations achieve an accuracy of 95.98% while non-expert annotations achieves 61.82%, with a gap of 34.16%." |
| Q112 | 9 | input_ontology | "This shows that sufficient domain knowledge of FOL is necessary for good performance on FOLIO." |
| Q113 | 9 | output_form | "The expert and GPT-4 gap is 31.82%, suggesting significant room for model improvement." |
| Q114 | 9 | input_content | "We focus on collecting a very high-quality dataset in evaluating logical reasoning rather than merely a large dataset." |
| Q115 | 9 | output_content | "Optimizing for quality required us to adopt a rigorous annotation process with domain experts selected based on a few important criteria as mentioned in Appendix A: Annotator Selection." |
| Q116 | 9 | input_content | "Significantly scaling up this process would have required resources beyond our current means and we are unable further expand our dataset for investigating how the size of training data affects the performance of fine-tuning experiments." |
| Q117 | 9 | input_content | "We encourage the community to apply our annotation protocol to expand this realistic and complex FOL reasoning story set." |
| Q118 | 9 | output_form | "Approximately 65% of the time, the model struggles to construct accurate reasoning chains for complex problems with intricate steps, leading to faulty reasoning paths and indicating a limited ability to solve problems with long reasoning chains." |
| Q119 | 9 | output_form | "In 25% of cases, erroneous derivations occur within certain reasoning steps, highlighting potential inaccuracies and flaws in logical deductions." |
| Q120 | 9 | output_ontology | "5% of conclusions in FOLIO have a complex syntactic structure, posing comprehension challenges for GPT-4." |
| Q121 | 9 | output_form | "5% of outputs show that GPT-4 leverage commonsense reasoning to employ spurious shortcuts that lead to the wrong truth value for the conclusion." |
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
| Q142 | 13 | input_ontology | "However, we do not use the Davidsonian (Davidson, 2001) or neo-Davidsonian semantics (Parsons, 1990) because translating the majority of the FOL formulas in our dataset only requires one-place and two-place predicates." |
| Q143 | 14 | output_content | "We therefore design an annotation protocol for first-order logic translation in order to ensure that our FOL translations are as consistent as possible across all examples in our dataset." |
| Q144 | 14 | output_content | "First-order logic formulas need to preserve as much as possible the semantics of natural language sentences." |
| Q145 | 14 | output_content | "First-order logic formulas should stay as faithful to the structure of the original NL sentence as possible." |
| Q146 | 14 | output_content | "Semantic decomposition is not needed unless necessary for maintaining the NL expressivity." |
| Q147 | 14 | input_form | "In terms of abstraction, we neglect tense and remove all the plural forms of verbs." |
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
| Q158 | 15 | output_form | "To test if the premise ordering in FOLIO has spurious correlations with the conclusion label which a model can exploit, we shuffle the input premises to evaluate models." |
| Q159 | 15 | output_form | "We find that accuracy increases or decreases by roughly 1% in most settings compared to our unshuffled premises." |
| Q160 | 15 | output_form | "This indicates that the ordering of premises in FOLIO examples does not yield significant information about the label, and thus models will not be able to use the premise ordering as a strong heuristic or statistical feature for its predictions." |
| Q161 | 15 | input_form | "FOL formulas have a clearer and more straightforward logical structure than NL sentences." |
| Q162 | 15 | input_form | "As shown in Table 11, the performance slightly increases in the NL+FOL setting for GPT-4 while GPT-3.5 performs worse in both the NL+FOL and the FOL-only settings." |
| Q163 | 15 | input_form | "FOL always serves as additional useful information for GPT-4, but not for GPT-3.5 regardless of whether FOL is concatenated with NL." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.emergentmind.com/topics/prontoqa |
| WEB-2 | https://proceedings.iclr.cc/paper_files/paper/2025/file/862819c227b16f9af64dd6ad6cfdf275-Paper-Conference.pdf |
| WEB-3 | https://arxiv.org/html/2602.21044v1 |
| WEB-4 | https://arxiv.org/pdf/2406.17663 |
| WEB-5 | https://arxiv.org/pdf/2603.02788 |
| WEB-6 | https://aclanthology.org/2024.emnlp-main.1229.pdf |
| WEB-7 | https://www.nist.gov/itl/ai-risk-management-framework |
| WEB-8 | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf |
| WEB-9 | https://openreview.net/pdf?id=ULEHJkolxB |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (config: default)
**Analysis date:** 2025-07-11
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | FOLIO/default | Ex. 1 | True | "No plants are fungi. Mushrooms are fungi." / "∀x (Plant(x) → ¬Fungi(x)) ∀x (Mushroom(x) → Fungi(x))" | Simple 2-premise syllogism with exact NL/FOL parallel; confirms NL-first design with FOL annotation layer | IF |
| D2 | FOLIO/default | Ex. 2 | Uncertain | "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises." / "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" | Multi-premise story with 7 premises including mixed disjunction/implication; illustrates chain-depth complexity and NL-FOL alignment | IF, IO |
| D3 | FOLIO/default | Ex. 3 | Uncertain | "A project is written either in C++ or Python." / "∀x (Project(x) → (WrittenIn(x, cplusplus) ⊕ WrittenIn(x, python)))" | Exclusive disjunction (⊕) expressed in NL as "either-or"; confirms documented NL convention alignment | IF |
| D4 | FOLIO/default | Ex. 4 | False | "No trick-shot artist in Yale's varsity team struggles with half court shots." / "∀x ((In(x, yaleSVarsityTeam) ∧ TrickShotArtist(x)) → ¬StruggleAt(x, halfCourtShot))" | Multi-step syllogism chain; same premise set generates multiple conclusions with different labels (also Ex. 18, 32) | IO, OO |
| D5 | FOLIO/default | Ex. 11 | False | "The bird is in Size Town and it is not both heavy and still." / "In(bird, sizeTown) ∧ ¬(Heavy(bird) ∧ Still(bird))" | 8-premise chain with 5+ reasoning depth; conclusion tests compound conditional | IO, IF |
| D6 | FOLIO/default | Ex. 12 | True | "Some cats are not pets. All cats are mammals." / "∃x (Cat(x) ∧ ¬Pet(x)) ∀x (Cat(x) → Mammal(x))" | Minimal existential quantifier example; note that conclusion-FOL uses double existential (∃x ∃y) where the NL "some mammals" might only require ∃x — potential over-specification in FOL | OC, IF |
| D7 | FOLIO/default | Ex. 13 | False | "No satin-finish lipsticks in the set do not have 'rosewood' in its offical description." | Double-negative NL sentence with typo ("offical"); NL quality issue in training data | IC, IF |
| D8 | FOLIO/default | Ex. 15 | Uncertain | "Oxford Circus is the entrance to Oxford Circus tube station, a part of the Central line in 1900." / "EntraceTo(oxfordCircus, tubeStation) ∧ PartOf(tubeStation, centralline) ∧ In(tubeStation, 1900)" | WikiLogic story with real-world entity (Oxford Circus, John Nash); typo "EntraceTo" in FOL | OC, IC |
| D9 | FOLIO/default | Ex. 16 | True | "All professional athletes spend most of their time on sports... Amy spends the most time on sports, or Amy is an Olympic gold medal winner." / "∀x (ProfessionalAthlete(x) → SpendOn(x, mostOfTheirTime, sports)) ... SpendOn(amy, mostOfTheirTime, sports) ∨ OlympicGoldMedalWinner(amy)" | Multi-step deductive chain with negation and implication; 6 premises, illustrates chain-depth coverage | IO |
| D10 | FOLIO/default | Ex. 17 | False | "Michael O'Donnell is a British physician, journalist, author, and broadcaster." / "British(michael) ∧ Physician(michael) ∧ Journalist(michael) ∧ Author(michael) ∧ Broadcaster(michael)" | WikiLogic: real Wikipedia person; FOL uses "michael" as constant but full name is John Nash / Michael O'Donnell | IC, OC |
| D11 | FOLIO/default | Ex. 22 | Uncertain | "Everyone in the Franco-China diplomatic conference is either a PRC national or a French national, but not both." / "∀x (In(x, franco-ChinaDiplomaticConference) → PRCNational(x) ⊕ FrenchNational(x))" | NL "but not both" correctly mapped to ⊕; confirms NL disjunction conventions | IF |
| D12 | FOLIO/default | Ex. 28 | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency." / "∀x (Country(x) ∧ PossibleEffectiveMonetaryPolicy(x) → SuccessfulInflationControl(x) ∧ StongNationalCurrency(x))" | Typo "StongNationalCurrency" appears in both premises-FOL and conclusion-FOL consistently | OC |
| D13 | FOLIO/default | Ex. 34 | True | "If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." / "¬(Planet(pSOJ318.5-22) ∧ Rogue(pSOJ318.5-22) ∧ BoundBy(pSOJ318.5-22, sun, gravitationally)) → (Planet(pSOJ318.5-22) ∧ Rogue(pSOJ318.5-22))" | Complex compound premise with negation and conditional; WikiLogic astronomy topic | IO |
| D14 | FOLIO/default | Ex. 36 | True | "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" | Missing closing parenthesis in FOL formula — syntactic error in training data | OC, IF |
| D15 | FOLIO/default | Ex. 43 | True | "∀x (MajorArgumentForm(x) → (InductiveReasoning(x) ⊕ DeductiveReasoning(x))" | Missing closing parenthesis in premises-FOL | OC, IF |
| D16 | FOLIO/default | Ex. 52 | True | "Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." / "¬(ProfessionalBasketballPlayer(jim) ⊕ NeverExercises(jim))" | Premises describe "John" but FOL uses "jim" — name inconsistency between NL and FOL | OC, IF |
| D17 | FOLIO/default | Ex. 57 | False | "Matt does not invest in the public stock market regularly." / "InvestInRegularly(matt, publicStockMarket)" | NL premise says Matt does NOT invest; FOL asserts he DOES — direct NL/FOL semantic contradiction | OC, IF |
| D18 | FOLIO/default | Ex. 4, 18, 32 | False/Uncertain/False | Same story_id=408, same 5 premises, but three different conclusions with labels False, Uncertain, False | Confirms premise reuse design: multiple conclusions per premise set; tests multi-conclusion inference from same world | IO, OO |
| D19 | FOLIO/default | Ex. 8, 19, 30 | Uncertain/Uncertain/False | Same story_id=482 (Potterville), three conclusions: "Harry is cool" (Uncertain), "Harry is not cool" (Uncertain), "Harry is a wizard or angry" (False) | Both "Harry is cool" and "Harry is not cool" labeled Uncertain — confirms Unknown/Uncertain label calibration; also Harry Potter cultural reference | IO, OO |
| D20 | FOLIO/default | Ex. 10 | Uncertain | "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" | Unbalanced parenthesis in premises-FOL | OC, IF |
| D21 | FOLIO/default | Ex. 55 | False | "Contain(tikTok, chatFeature) ⊕ ComputerProgram(tikTok))" | Unbalanced closing parenthesis in conclusion-FOL | OC, IF |
| D22 | FOLIO/default | Ex. 1 | True | Conclusion: "No plants are mushrooms." / "∀x (Plant(x) → ¬Mushroom(x))" | Minimal 2-premise example; low reasoning depth (depth ≤ 2) | IO |
| D23 | FOLIO/default | Ex. 50 | Uncertain | "Each building is tall. Everything tall has height." / "∀x (Building(x) → Tall(x)) ∀x (Tall(x) → Height(x))" | Minimal 2-premise example; low reasoning depth | IO |
| D24 | FOLIO/default | Ex. 29 | False | "The only types of mammals that lay eggs are either platypuses or echidnas... Grebes lay eggs. Grebes are not platypuses and also not echidnas." | 9-premise story requiring multi-step chain; illustrates higher depth coverage | IO |
| D25 | FOLIO/default | Ex. 37 | False | "Conclusion-FOL: ∃x (SavesFor(jane, enoughMoney, theSummer) ∧ Kangaroo(x) → WillSee(x, jane, berlinzoo))" | Conclusion-FOL encodes conditional inside existential scope — unusual FOL formulation that may represent annotation inconsistency | OC |
| D26 | FOLIO/default | Ex. 6 | Uncertain | "Ho is at the business conference and prefers state ownership of the means of production." | Non-Western name ("Ho") in story; ideologically loaded topic (communist/planned economy) used as logical content — within scope of deductive task | IC |
| D27 | FOLIO/default | Ex. 13 | False | "Lipstcks in the Rouge Dior set, Lunar New Year Limited Edition either does not have 'rosewood' in its offical description or it has 'rosewood' in its official description." | Typo "Lipstcks" in NL premises; tautological premise (p ∨ ¬p) | IC, OC |
| D28 | FOLIO/default | Ex. 56 | Uncertain | "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin." / "DistrictIn(xiufeng, guilin) ∧ DistrictIn(xiangshan, guilin)..." | WikiLogic: Chinese geographic entities (Guilin districts); conclusion about Kowloon/HK is unrelated to premises — exemplifies "Unknown" label for unrelated conclusions | OO |

---

### Deployment-Relevant Strengths

#### Strength 1: Complete NL/FOL parallel annotation for all examples
- **Dimension(s):** IF
- **Observation:** Every example in the sampled data provides complete, aligned natural-language premises and conclusions alongside their FOL counterparts. The NL and FOL layers are present and co-aligned at the formula level (not just story level), directly enabling hybrid NL+FOL presentation mode testing as well as ablation between NL-only and FOL-only conditions.
- **Deployment relevance:** The lab's highest-priority concern is the undecided choice between pure-symbolic and hybrid presentation modes. The parallel annotation structure means FOLIO directly supports the NL+FOL hybrid condition out of the box without any preprocessing, and also permits constructing a FOL-only input condition, even if the latter is not the benchmark's native mode.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO/default, split=train, label=True): "No plants are fungi. Mushrooms are fungi." / "∀x (Plant(x) → ¬Fungi(x)) ∀x (Mushroom(x) → Fungi(x))" — Demonstrates clean NL/FOL parallel at the sentence level, with semantically equivalent representations.
  - [D2] Example 2 (FOLIO/default, split=train, label=Uncertain): "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" — Multi-premise story shows FOL is provided at per-sentence granularity throughout, not just as a story-level summary.
  - [D11] Example 22 (FOLIO/default, split=train, label=Uncertain): "NL: 'Everyone in the Franco-China diplomatic conference is either a PRC national or a French national, but not both.' / FOL: ∀x (In(x, franco-ChinaDiplomaticConference) → PRCNational(x) ⊕ FrenchNational(x))" — Shows NL disjunction "but not both" correctly rendered as ⊕, confirming semantic equivalence.

#### Strength 2: Full classical FOL operator coverage observed in sample
- **Dimension(s):** IO
- **Observation:** The sampled examples exhibit all core FOL operators documented in the benchmark: negation (¬), conjunction (∧), disjunction (∨), exclusive disjunction (⊕), implication (→), universal quantifier (∀), existential quantifier (∃), and equality (=). Multi-place predicates also appear.
- **Deployment relevance:** The lab targets broad classical-deductive FOL coverage with explicit exclusion of temporal, modal, arithmetic, and probabilistic reasoning. The sample confirms the benchmark delivers this precisely.
- **Datapoint citations:**
  - [D3] Example 3 (FOLIO/default, split=train, label=Uncertain): "∀x (Project(x) → (WrittenIn(x, cplusplus) ⊕ WrittenIn(x, python)))" — Exclusive disjunction with universal quantifier.
  - [D13] Example 34 (FOLIO/default, split=train, label=True): "¬(Planet(pSOJ318.5-22) ∧ Rogue(pSOJ318.5-22) ∧ BoundBy(pSOJ318.5-22, sun, gravitationally)) → (Planet(pSOJ318.5-22) ∧ Rogue(pSOJ318.5-22))" — Negated conjunction in antecedent of implication; n-place predicate (BoundBy).
  - [D9] Example 16 (FOLIO/default, split=train, label=True): "SpendOn(amy, mostOfTheirTime, sports) ∨ OlympicGoldMedalWinner(amy)" — Ground-atom disjunction.

#### Strength 3: Multi-conclusion reuse of premise sets enables multi-depth inference evaluation
- **Dimension(s):** IO, OO
- **Observation:** Multiple examples share the same premise set (same story_id) but have different conclusions with different labels. This directly confirms that FOLIO generates multiple conclusions per story at varying logical depths and with varying truth values, providing richer per-story coverage.
- **Deployment relevance:** The lab prioritizes multi-step deduction chains. The multi-conclusion design means the benchmark can test whether models hold a consistent world model across conclusions, not just whether they answer individual questions correctly.
- **Datapoint citations:**
  - [D18] Examples 4, 18, 32 (FOLIO/default, split=train, story_id=408): Same 5 premises about Yale's varsity team, producing conclusions labeled False, Uncertain, and False respectively — confirms multiple conclusions per premise set with varying labels.
  - [D19] Examples 8, 19, 30 (FOLIO/default, split=train, story_id=482): Same 7 premises about Potterville; "Harry is cool" (Uncertain), "Harry is not cool" (Uncertain), "Harry is a wizard or angry" (False) — illustrates that complementary conclusions can both be Unknown when premises are insufficient.

#### Strength 4: Three-way label distribution with genuine Unknown calibration
- **Dimension(s):** OO
- **Observation:** The sample shows meaningful use of all three label categories (True, False, Uncertain), and the Unknown/Uncertain label is correctly applied even to complementary conclusions ("Harry is cool" and "Harry is not cool" are both Uncertain from the same premises), confirming that the label is not a catch-all for hard cases but reflects genuine logical underdetermination.
- **Deployment relevance:** The lab confirmed that True/False/Unknown maps cleanly to entailment/contradiction/neutral. The data confirms the Unknown label is used with logical precision, not as a default.
- **Datapoint citations:**
  - [D19] Examples 8 and 19 (FOLIO/default, split=train, story_id=482, label=Uncertain): Both "Harry is cool" and "Harry is not cool" are labeled Uncertain — confirms the label reflects logical underdetermination, not difficulty.
  - [D23] Example 50 (FOLIO/default, split=train, label=Uncertain): "All buildings are magnificent." / "∀x (Building(x) → Magnificent(x))" — Conclusion introduces a predicate absent from premises; correctly labeled Uncertain.

#### Strength 5: Broad topical coverage across WikiLogic stories
- **Dimension(s):** IC
- **Observation:** The sample spans a wide range of real-world topics: astronomy (rogue planets), biology (mammals/echidnas), geography (Guilin, New Haven, Bronx), economics (monetary policy/Russia), cinema (Adventures of Rusty, Tintin), social media (TikTok), medicine, and sports. This confirms the documented 4,351-word vocabulary and Wikipedia-seeded diversity.
- **Deployment relevance:** For a US research lab evaluating formal reasoning, topical variety ensures the benchmark does not probe domain-specific knowledge artifacts but rather general deductive capacity. The breadth reduces the risk that any single topic dominates performance variance.
- **Datapoint citations:**
  - [D13] Example 34 (FOLIO/default, split=train, label=True): "PSO J318.5−22 is a rogue planet" — Astronomy/astrophysics topic.
  - [D28] Example 56 (FOLIO/default, split=train, label=Uncertain): "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin." — Chinese geography topic confirming non-US content.
  - [D26] Example 6 (FOLIO/default, split=train, label=Uncertain): "Everyone at the business conference is either an investor or an entrepreneur." — Political economy topic with non-Western name.

#### Strength 6: NL quantifier-to-FOL mapping follows documented conventions consistently
- **Dimension(s):** IF
- **Observation:** Across the sample, NL phrasing conventions for quantifiers and disjunction are consistently rendered in FOL. "All A are B" → ∀x (A(x) → B(x)); "Some A are B" → ∃x (A(x) ∧ B(x)); "either-or" (exclusive) → ⊕; "or both" (inclusive) → ∨; "neither...nor" → ¬ ... ∧ ¬. This confirms the documented annotation protocol is followed.
- **Deployment relevance:** Consistent NL-FOL mapping reduces construct-irrelevant variance when the lab presents hybrid inputs; models that handle the NL-FOL mapping correctly should receive comparable signals across examples.
- **Datapoint citations:**
  - [D3] Example 3 (FOLIO/default, split=train, label=Uncertain): "A project is written either in C++ or Python." → "WrittenIn(x, cplusplus) ⊕ WrittenIn(x, python)" — Exclusive disjunction convention confirmed.
  - [D1] Example 1 (FOLIO/default, split=train, label=True): "No plants are fungi." → "∀x (Plant(x) → ¬Fungi(x))" — Universal negation convention confirmed.
  - [D11] Example 22 (FOLIO/default, split=train, label=Uncertain): "'but not both'" → "⊕" — Additional exclusive disjunction confirmation.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Direct NL/FOL semantic contradiction in at least one training example
- **Dimension(s):** OC, IF
- **Observation:** Example 57 contains a NL premise "Matt does not invest in the public stock market regularly" paired with a FOL formula "InvestInRegularly(matt, publicStockMarket)" — the negation is dropped in the FOL encoding. This is a direct semantic contradiction between the NL and FOL layers in the same example, meaning the FOL annotation does not faithfully represent the NL content.
- **Deployment relevance:** This is the most serious quality concern in the sample. If the lab presents hybrid NL+FOL inputs, this example will provide conflicting signals to the model. If presenting FOL-only, the label may be computed from incorrect premises. The web search findings noted that a 2025 study found annotation errors in FOLIO requiring a cleaned validation set — this sampled example is direct evidence of such errors in the training split.
- **Datapoint citations:**
  - [D17] Example 57 (FOLIO/default, split=train, label=False): NL: "Matt does not invest in the public stock market regularly." / FOL: "InvestInRegularly(matt, publicStockMarket)" — Negation ¬ is absent in FOL where it should be present; direct NL/FOL semantic mismatch.

---

#### MAJOR

#### Concern 2: Multiple syntactic errors in FOL formulas (unbalanced parentheses, typos in predicate names)
- **Dimension(s):** OC, IF
- **Observation:** At least four examples in the 57-sample contain syntactic errors in FOL formulas: unbalanced parentheses in Examples 10, 36, 43, and 55; a typo predicate name "StongNationalCurrency" (missing letter) appearing consistently in Example 28's premises and conclusion FOL; a typo "EntraceTo" in Example 15's FOL. These errors would cause parsing failures in a syntactic checker and potentially corrupt inference engine execution.
- **Deployment relevance:** The lab intends to use FOLIO's FOL layer (for hybrid or FOL-only input modes, or for the NL-to-FOL translation task). Syntactically malformed FOL formulas in the training set could corrupt fine-tuning for the translation task and would cause failures if fed directly to the Stanford CS221 inference engine. The web search findings explicitly noted that a 2025 cleaning study found annotation errors — the syntactic errors observed here are direct confirmation of that finding in the training split.
- **Datapoint citations:**
  - [D14] Example 36 (FOLIO/default, split=train, label=True): "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" — Missing closing parenthesis after "jameSFamily".
  - [D15] Example 43 (FOLIO/default, split=train, label=True): "∀x (MajorArgumentForm(x) → (InductiveReasoning(x) ⊕ DeductiveReasoning(x))" — Missing closing parenthesis.
  - [D20] Example 10 (FOLIO/default, split=train, label=Uncertain): "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" — Unmatched closing parenthesis.
  - [D21] Example 55 (FOLIO/default, split=train, label=False): "Contain(tikTok, chatFeature) ⊕ ComputerProgram(tikTok))" — Extra closing parenthesis in conclusion-FOL.
  - [D12] Example 28 (FOLIO/default, split=train, label=False): "StongNationalCurrency(x)" — Consistent typo in both premises-FOL and conclusion-FOL (likely from copy-paste, but still non-standard predicate name).

#### Concern 3: NL name inconsistency between premises and FOL (John → Jim)
- **Dimension(s):** OC, IF
- **Observation:** Example 52 refers to "John" throughout the NL premises ("Either John is a professional basketball player...") but the FOL formulas consistently use "jim" as the constant (e.g., "¬(ProfessionalBasketballPlayer(jim) ⊕ NeverExercises(jim))"). This creates a cross-layer entity reference inconsistency.
- **Deployment relevance:** For the NL-to-FOL translation task, this inconsistency would produce erroneous training signal — a model that correctly translates "John" to a constant named "john" would be penalized relative to the gold standard using "jim". For hybrid NL+FOL input, the mismatch may confuse models tracking entity identity across layers.
- **Datapoint citations:**
  - [D16] Example 52 (FOLIO/default, split=train, label=True): NL: "Either John is a professional basketball player and he never exercises" / FOL: "¬(ProfessionalBasketballPlayer(jim) ⊕ NeverExercises(jim))" — "John" in NL, "jim" in FOL.

#### Concern 4: Test split not present in HuggingFace dataset; only train + validation available
- **Dimension(s):** OF
- **Observation:** The HF metadata schema shows only `train` (1,001 examples) and `validation` (203 examples) splits, totalling 1,204 examples. The documented test set (226 examples with 87 True, 78 False, 61 Unknown) is not present in the HuggingFace dataset. Benchmark documentation and web search findings refer to the test set for all primary performance comparisons.
- **Deployment relevance:** The lab's evaluation pipeline will likely want to hold out a test set not seen during any prompting or fine-tuning experiments. If the lab uses the HuggingFace dataset as its data source, there is no separate held-out test split available; the lab would need to obtain the test set from the FOLIO GitHub repository directly. Reliance only on the validation set (203 examples) reduces statistical power, especially for per-depth or per-label-class analyses.
- **Datapoint citations:**
  - HF Metadata: `"splits": {"train": {"num_examples": 1001}, "validation": {"num_examples": 203}}` — No `test` split present; total 1,204 examples vs. documented 1,430.

#### Concern 5: NL quality issues (typos, double negatives) appear in training data despite documented quality control
- **Dimension(s):** IC, IF
- **Observation:** Several training examples contain NL-layer issues: Example 13 has a double negative ("No satin-finish lipsticks in the set do not have 'rosewood'") and two spelling errors ("offical", "Lipstcks"); Example 28 has the consistent predicate typo "Stong"; Example 43 contains a redundant variable ("∃x ∃y ∃y ∃w" with duplicate ∃y) in premises-FOL.
- **Deployment relevance:** For a US research lab using FOLIO to benchmark NL reasoning, NL-layer errors introduce construct-irrelevant variance: a model that gets Example 13 wrong may be failing on the grammatical ambiguity rather than the logical structure. The 2025 annotation-cleaning study is relevant here — the lab should verify whether it uses the original or cleaned annotation set.
- **Datapoint citations:**
  - [D7] Example 13 (FOLIO/default, split=train, label=False): "No satin-finish lipsticks in the set do not have 'rosewood' in its offical description." — Double negative NL premise; two typos ("offical", "Lipstcks").
  - [D27] Example 13 (FOLIO/default, split=train, label=False): "Lipstcks in the Rouge Dior set, Lunar New Year Limited Edition either does not have 'rosewood' in its offical description or it has 'rosewood' in its official description." — Tautological NL premise (p ∨ ¬p) that adds no logical content.

#### Concern 6: Potential FOL annotation inconsistency — over-specification in existential quantification
- **Dimension(s):** OC, IF
- **Observation:** In Example 12, the NL conclusion "Some mammals are not pets" is translated to FOL as "∃x ∃y (Mammal(x) ∧ Mammal(y) ∧ ¬Pet(x) ∧ ¬Pet(y))" — requiring two distinct non-pet mammals, which is stronger than what "some" conventionally requires (just ∃x). This may introduce subtle annotation biases where conclusions are harder to satisfy in FOL than in NL. Similarly, Example 37's conclusion-FOL encodes a conditional inside an existential scope in an atypical formulation.
- **Deployment relevance:** For the NL-to-FOL translation task, inconsistencies in how "some" is formalized (sometimes ∃x, sometimes ∃x ∃y) create label noise that would penalize models making the simpler but logically valid translation. For the reasoning task, if the inference engine uses the over-specified FOL, labels may differ from what a pure NL reasoning model would compute.
- **Datapoint citations:**
  - [D6] Example 12 (FOLIO/default, split=train, label=True): "Some mammals are not pets." / "∃x ∃y (Mammal(x) ∧ Mammal(y) ∧ ¬Pet(x) ∧ ¬Pet(y))" — Double existential where single would suffice.
  - [D25] Example 37 (FOLIO/default, split=train, label=False): "∃x (SavesFor(jane, enoughMoney, theSummer) ∧ Kangaroo(x) → WillSee(x, jane, berlinzoo))" — Conditional embedded inside existential scope; unusual formulation.

---

#### MINOR

#### Concern 7: Label field uses "Uncertain" rather than documented "Unknown"
- **Dimension(s):** OO
- **Observation:** The HF dataset uses the string "Uncertain" as the label value (observed in examples 2, 3, 5, 6, 7, 8, 9, etc.), while the benchmark paper and YAML consistently use "Unknown" (True/False/Unknown). The lab's elicitation confirmed the three-way mapping to entailment/contradiction/neutral.
- **Deployment relevance:** Minor inconsistency that requires a string normalization step in the evaluation pipeline. No logical misalignment — the category is the same — but any code that filters by label="Unknown" will fail on the HF dataset without transformation.
- **Datapoint citations:**
  - [D2] Example 2 (FOLIO/default, split=train, label=Uncertain): label field contains "Uncertain" — HF dataset label string differs from paper documentation's "Unknown".

#### Concern 8: Shallow-depth examples are present in the sample, potentially reducing discriminability at low depths
- **Dimension(s):** IO
- **Observation:** Several examples in the sample have only 2 premises and require very shallow reasoning (depth ≤ 2): Examples 1 (2 premises), 12 (2 premises), 17 (4 premises, simple syllogism), 50 (2 premises). These would contribute little to discriminating frontier model capability.
- **Deployment relevance:** The lab prioritizes multi-step chains. While the benchmark documents 28.7% of examples at depth ≥5, the presence of very shallow examples means aggregate accuracy is influenced by a mixture of difficulties. Per-depth performance analysis will be essential; per-depth example counts at depth 6–7 may be too small for reliable statistical inference (as noted in the web search findings, ~65 examples total at depth ≥5 in the test set).
- **Datapoint citations:**
  - [D22] Example 1 (FOLIO/default, split=train, label=True): "No plants are fungi. Mushrooms are fungi." — 2-premise, depth ≤ 2.
  - [D23] Example 50 (FOLIO/default, split=train, label=Uncertain): "Each building is tall. Everything tall has height." — 2-premise, depth ≤ 2; conclusion introduces predicate absent from premises.

#### Concern 9: WikiLogic stories reference real-world entities that may be in LLM pretraining data
- **Dimension(s):** IC
- **Observation:** Multiple WikiLogic examples reference specific real-world entities whose facts are available in pretraining corpora: Michael O'Donnell (British journalist), Bobby Flynn (Australian Idol), Oxford Circus / John Nash, Adventures of Rusty / Columbia Pictures. A model may arrive at correct answers by recalling facts rather than deductive reasoning from premises.
- **Deployment relevance:** The lab's expert evaluator population will be aware of this confound. For evaluating pure deductive reasoning capability, WikiLogic examples with real-world entities may allow shortcut reasoning; the HybLogic subset would be cleaner for this purpose. The benchmark paper documents this concern [Q104].
- **Datapoint citations:**
  - [D10] Example 17 (FOLIO/default, split=train, label=False): "Michael O'Donnell is a British physician, journalist, author, and broadcaster... Michael O'Donnell was born in Yorkshire as the son of a general practitioner." — Real Wikipedia person; conclusion "There are no journalists that were born in Yorkshire" is falsifiable from world knowledge.
  - [D8] Example 15 (FOLIO/default, split=train, label=Uncertain): "Oxford Circus is a road junction connecting Oxford Street and Regent Street... John Nash designed Oxford Circus." — Real-world architect and landmark.

#### Concern 10: Reasoning depth distribution skewed toward lower depths in sample
- **Dimension(s):** IO
- **Observation:** Of the 57 sampled examples, premise counts (a proxy for reasoning depth) range from 2 to 9. The modal depth in the benchmark is 4, but the sample contains a noticeable number of 2-premise examples. Without the test split, per-depth analysis must use the validation set (203 examples), with potentially very few examples at depth 6–7.
- **Deployment relevance:** As noted in the web search findings, depth 6–7 subsets in the 226-example test set are likely single-digit counts, making accuracy estimates at those depths statistically unreliable. The lab should treat per-depth scores at depth 6–7 as indicative only.
- **Datapoint citations:**
  - [D22] Example 1 (train, 2 premises), [D5] Example 11 (train, 8 premises) — Range of depths observed in sample confirms mixture.
  - [D24] Example 29 (FOLIO/default, split=train, label=False): 9 premises about platypuses/echidnas/hyraxes/grebes — higher-depth example present in sample.

---

### Content Coverage Summary

The 57 sampled training examples span a wide topical range (astronomy, biology, geography, economics, media, sports, logic/reasoning meta-examples) consistent with WikiLogic's Wikipedia-seeding design. Both WikiLogic (free-form stories with real-world entities) and HybLogic (syllogism-template-based with populated slots) subcorpora appear to be represented, though the sample does not tag subcorpus origin explicitly.

All core FOL operators are present in the sample. NL-FOL alignment conventions (exclusive vs. inclusive disjunction, quantifier phrasing) are largely followed. Logical structure ranges from 2-premise minimal syllogisms (depth ≤ 2) to 9-premise multi-step chains (depth ≥ 5). The three-way label distribution (True/False/Uncertain) is represented, with Uncertain being the most common label in the sample.

**Quality observations from the sample:** Five examples show syntactic errors in FOL formulas (unbalanced parentheses); one shows a direct NL/FOL semantic contradiction (negation dropped); one shows a name inconsistency (John/Jim) between NL and FOL layers; two show NL typos that passed quality control. These are consistent with the 2025 annotation-cleaning study's finding of errors in the public dataset.

**Input format:** Every example provides the full NL/FOL parallel structure. The NL layer is natural English prose; the FOL layer uses standard AI/education FOL notation (Russell & Norvig style) with Unicode operators (∀, ∃, ∧, ∨, ¬, →, ⊕, =). The benchmark natively supports NL-only, FOL-only, and hybrid input construction from the HF data fields.

---

### Limitations

1. **Sample size:** 57 examples from the 1,001-example training split. While the sample reveals concrete quality issues, the rate of annotation errors (syntactic and semantic) cannot be reliably estimated from this sample alone.

2. **Test split unavailable on HuggingFace:** The 226-example test set referenced in the paper and web search findings is not present in the HF dataset. All per-label and per-depth performance statistics in the paper (87 True / 78 False / 61 Unknown) refer to this unavailable split. The validation set (203 examples) is the only evaluation split accessible via HF.

3. **Subcorpus label not in schema:** The HF schema does not include a field distinguishing WikiLogic from HybLogic examples. Subcorpus-stratified analysis (which is important for the lab's ceiling-effect assessment, since GPT-4 performs near-randomly on HybLogic) requires external cross-referencing with the FOLIO GitHub repository.

4. **Reasoning depth not in schema:** The `reasoning_depth` field is not present in the HF dataset. Per-depth analysis requires external computation or cross-referencing with GitHub metadata.

5. **Cleaned vs. original dataset:** The 2025 annotation-cleaning study (arxiv 2603.02788) established a cleaned validation set. The HF dataset appears to be the original uncleaned version. The lab should verify which version it is using, as scores on the two versions may differ.

6. **Cannot inspect FOL inference engine behavior:** The sample reveals syntactic errors in FOL formulas, but it is not possible from data inspection alone to determine whether the inference engine successfully resolved these (e.g., via the Python parser bridge) or whether they propagated to label errors. The 2025 cleaning study used Vampire rather than the Stanford CS221 engine, suggesting the original engine may have been more tolerant of these errors.

