## Deployment Context

We are a US educational platform building a tool for American logic students. The tool should not only determine whether a logical argument is valid but also explain why — producing step-by-step reasoning traces that students can follow. We need to evaluate the LLM's ability to both perform logical reasoning and articulate its reasoning process in a pedagogically clear way.

# Validity Analysis: folio
**Target context:** US Undergraduate Logic Students — Introductory and Intermediate Courses
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ✓ | 3 | Moderate gaps | high |
| Input Content | 3 | Moderate gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content | 2 | Significant gaps | high |
| Output Form ⚠ | 1 | Serious concern | high |
| **Average** | **2.3** | | |

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

FOLIO is a high-quality FOL deductive-reasoning benchmark with engine-verified labels, expert annotation, and topical diversity that partially serves a US undergraduate logic deployment — but only for one slice of what the deployment must evaluate. For the validity-precondition sub-judgment (does the conclusion follow from the premises?), FOLIO provides reliable ground truth and meaningful difficulty stratification, with strong support for the advanced predicate-logic register. However, the two HIGH-priority dimensions (output ontology and output form) are essentially completely misaligned: FOLIO outputs single labels, while the deployment requires numbered Fitch-style proof traces with rule citations, register-differentiated explanations, and countermodels for invalid arguments — none of which FOLIO produces, scores, or contains as ground truth. Secondary concerns include: no propositional-only coverage (deployment requires it), no implicit-premise reconstruction (deployment requires it), notation mismatch between FOLIO's Russell & Norvig syntax and the LPL Fitch syntax students learn, and a ~10% FOL annotation-artifact rate observed in dataset sampling. P-FOLIO and emerging propositional-logic benchmarks (Rosetta-PL, DivLogicEval, the 2025 ITS study) partially fill some gaps but no off-the-shelf benchmark covers Fitch-style rule-cited proof traces or pedagogical countermodel construction.

## Practical Guidance

### What This Benchmark Measures

FOLIO can directly support evaluation of two sub-capabilities the deployment requires: (1) the binary/ternary deductive-validity judgment that must precede any proof generation (strongest dimension: input ontology and input form, with reliable output content for the label itself), and (2) NL-to-FOL translation correctness at a discourse-multi-premise level. For predicate-logic content at advanced register, FOLIO's depth-stratified evaluation provides genuine difficulty discrimination. It does not measure proof-trace generation, rule-citation correctness, register-appropriate explanation, or countermodel construction — the deployment's primary output requirements.

### Construct Depth

Construct coverage is shallow relative to deployment needs: FOLIO probes the OUTCOME of deductive reasoning (final label) but not the STRUCTURE (numbered steps, rule applications, subproof discharges) or the PEDAGOGICAL FRAMING (register-appropriate prose, premise-citation correctness). The expert/non-expert 34-point performance gap [Q111] and the GPT-4-vs-expert 31.82-point gap [Q113] confirm FOLIO discriminates between sound and unsound FOL reasoning at the label level, but provides no evidence about explanation quality. The deepest gaps are in OO and OF (both HIGH-priority, both scored 1), with material secondary gaps in IO (propositional + implicit-premise) and OC (no explanation ground truth).

### What Else You Need

Multi-source supplementation required: (1) For Fitch-style proof-trace evaluation — no off-the-shelf benchmark exists; build a custom rubric-based evaluation harness, optionally bootstrapped from P-FOLIO's NL proof chains [WEB-7] adapted to Fitch notation with rule labels; (2) For propositional logic — supplement with Rosetta-PL [WEB-11] or DivLogicEval [WEB-12], noting they also lack Fitch traces; (3) For countermodel evaluation — no benchmark covers this; develop with logic instructors using textbook countermodel exercises, drawing on the Lean-based 'Learning to Disprove' framework as a methodological template [WEB-10]; (4) For implicit-premise reconstruction — develop a custom enthymeme corpus from textbook exercises (Hurley, Bergmann/Moor/Nelson); (5) For pedagogical clarity / register appropriateness — adapt the 2025 ITS study's 4-criterion rubric [WEB-9] to Fitch-notation outputs. Additionally, clean ~10% of FOL annotation artifacts in FOLIO before any training use [DATASET-D24, D25, D26].

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
FOLIO's task taxonomy centers on FOL deductive reasoning with multi-premise discourse-level arguments [Q15, Q71, Q72] and an NL-FOL translation subtask [Q67], which partially align with the deployment's predicate-logic and NL-to-formal-form translation requirements. However, the benchmark explicitly excludes temporal and modal logic [Q139, Q140] (consistent with deployment scope) but also offers no propositional-only subtask — the dataset sample confirms every example uses FOL quantifiers even in minimal 2-premise cases [DATASET-D1, D31]. Argument reconstruction from arguments with implicit premises is also not present as a category; FOLIO annotators added commonsense premises explicitly [Q55]. Given MODERATE priority on IO, these omissions represent a moderate coverage gap relative to the deployment's tri-partite requirement (propositional, FOL, implicit-premise reconstruction).

**Strengths:**
- Strong coverage of multi-step FOL deductive chains, with 28.7% of examples requiring 5+ reasoning depths [Q60], directly relevant to advanced-register predicate logic exercises
- Discourse-level multi-premise translation task [Q71, Q72] aligns with deployment's NL-to-formal-form translation need
- Syllogistic chains [Q43] map to canonical textbook exercise forms students encounter

**Checklist:**

- **IO-1**: Required categories per elicitation Q3/A3: propositional logic, predicate/FOL reasoning, and argument reconstruction with implicit premises from everyday/quasi-legal scenarios. Modal/temporal/inductive are out of scope. — _Sources: Q15, Q67_
- **IO-2**: Omitted categories: (a) propositional-only reasoning — no examples in the sample use only sentential connectives without quantifiers [DATASET-D1, D31]; (b) implicit-premise/enthymeme reconstruction — annotators explicitly added commonsense premises [Q55], and dataset sampling confirms every premise needed is explicit [DATASET-D36, D19]. — _Sources: Q55, DATASET-D1, DATASET-D31, DATASET-D36, WEB-11_
- **IO-3**: Categories present that may consume evaluation weight without serving the deployment: heavy reliance on HybLogic template-derived syllogism combinations [Q42, Q43] and abstract fictional-world scenarios [DATASET-D9, D8] that do not reflect everyday/quasi-legal argument types the deployment targets. — _Sources: Q42, Q43, DATASET-D9, DATASET-D8_
- **IO-4**: Content-validity gaps documented: (a) no propositional-only subtask; (b) no implicit-premise reconstruction subtask; (c) abstract template-derived scenarios consume evaluation weight beyond what deployment register requires. Modal/temporal exclusion [Q139, Q140] is aligned with deployment scope. — _Sources: Q139, Q55, WEB-11, WEB-13_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q15] 'a natural language reasoning dataset, FOLIO, with first-order logic reasoning problems which require the models to decide the correctness of conclusions given a world defined by the premises' (p.1)
- [Q60] '28.7% of the examples need five or more depths of reasoning to infer the conclusions' (p.5)
- [Q55] 'we also add necessary commonsense knowledge in both the NL and FOL premises... We add such knowledge as additional premises at this stage' (p.5)
- [Q67] 'We propose a new natural language to first-order logic translation (NL-FOL translation) task alongside our reasoning dataset' (p.6)
- [Q139] 'we consider temporal logic and modal logic as special-purpose logics' (p.13)

*Web sources:*
- [WEB-11] Rosetta-PL is a 2025 benchmark purpose-built for propositional logic LLM evaluation — confirms propositional-only coverage is a distinct need not addressed by FOLIO
- [WEB-13] ProofWriter covers propositional-level chaining with limited vocabulary but no Fitch notation

*Dataset analysis:*
- DATASET-D1: even simplest 2-premise example uses ∀x quantifier — no propositional-only examples found
- DATASET-D31: minimal 2-premise example 'Each building is tall' uses ∀x quantification, not sentential connectives
- DATASET-D36: 6 explicit premises about Meta employees rather than implicit-premise enthymeme
- DATASET-D2: 7-premise complex chain demonstrates advanced-register depth

</details>

**Information gaps:**
- No documented mapping between FOLIO's task taxonomy and Fitch-style natural deduction inference-rule taxonomy

**Requires expert verification:**
- Whether the advanced-register subset of the curriculum specifically needs subproof-discharge categories (∨E, ¬I, →I via subproof) that FOLIO's flat-FOL output cannot exercise

---

### Input Content — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
FOLIO's content is topically diverse (4,351 distinct words [Q62]; Wikipedia-seeded plus hybrid stories [Q33, Q58]) and explicitly bias-screened [Q47, Q127], which broadly fits a US undergraduate audience. Dataset sampling confirms wide topical coverage — science, sports, consumer goods, technology [DATASET-D4, D11, D21, D36]. However, FOLIO content is uniformly written as fully explicit, formalized premise sets [Q55], which mismatches the deployment's stated need for everyday/quasi-legal arguments with implicit premises. Several sampled examples involve geopolitically sensitive content (communist ideology, Russian sanctions, North Korean nationality) [DATASET-D6, D19, D16] that, while not pedagogically disqualifying, could create classroom-distraction concerns. With IC weighted MODERATE, the content profile partially serves the deployment but does not capture the implicit-premise everyday-argument register that students must learn to handle.

**Strengths:**
- Topical diversity from 304 Wikipedia-seeded stories yields 74% of vocabulary [Q62] — reduces topical overfitting risk
- Explicit bias-removal protocol [Q47, Q127] aligns with US classroom content-neutrality expectations
- Explicit-premise format directly matches textbook exercise style for the formal-exercise portion of the curriculum [DATASET-D20]

**Checklist:**

- **IC-1**: Most content does not require US-specific cultural knowledge; examples reference globally-recognizable entities (Olympic medals, universities, consumer brands) [DATASET-D13, D11]. Some Wikipedia-seeded stories use less familiar entities (Bobby Flynn, John Nash architect) [DATASET-D18, D12], but these do not block reasoning. — _Sources: Q62, DATASET-D13, DATASET-D11, DATASET-D18_
- **IC-2**: Cultural alignment is broadly acceptable. Bias-removal protocol [Q127] reduces identity-linked stereotype risk. Several sampled examples touch politically sensitive geopolitical content (Russian sanctions [DATASET-D19], North Korean nationality [DATASET-D16], ardent communist [DATASET-D6]) — these are logically neutral but may cause classroom-context friction. — _Sources: Q127, DATASET-D6, DATASET-D19, DATASET-D16_
- **IC-3**: Content does not require Western-specific knowledge in a disqualifying way; cross-cultural Wikipedia seeding [Q34] yields mixed-origin entities (Andy Chang from Hong Kong [DATASET-D7], PRC/French nationals [DATASET-D16]). — _Sources: DATASET-D7, DATASET-D16_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional annotators (US-undergrad-logic-instructor reviewers) have re-annotated FOLIO content for classroom appropriateness. Would need instructor panel review.
- **IC-5**: Content gap: explicit-premise-only format does not exercise implicit-premise reconstruction [Q55, DATASET-D36]; abstract fictional scenarios (Size Town, Potterville) [DATASET-D9, D8] do not represent everyday/quasi-legal arguments the deployment targets. — _Sources: Q55, DATASET-D36, DATASET-D9, DATASET-D8_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q62] 'our dataset has a vocabulary of 4,351 words, and the examples based on Wikipedia account for 74% of the total vocabulary' (p.5)
- [Q47] 'Our dataset prioritizes realism and factual accuracy, steering clear of biases and stereotypes' (p.4)
- [Q55] 'Sometimes humans do not write certain commonsense knowledge in the premises that is required in the FOL reasoning process... We add such knowledge as additional premises' (p.5)
- [Q127] 'We took out stories that had strongly opinionated language and contained gender, racial, and classist biases' (p.13)

*Dataset analysis:*
- DATASET-D36: 'Everyone working at Meta has a high income...' — 6 fully explicit premises rather than implicit-premise reconstruction
- DATASET-D6: 'ardent communist...prefers state ownership' — politically loaded predicate in classroom content
- DATASET-D19: Russian foreign trade embargo as a logical premise
- DATASET-D16: 'No North Korean nationals are citizens of the European Union' as a logical predicate
- DATASET-D9: Size Town abstract scenario with no real-world referent
- DATASET-D11: Rouge Dior lipstick product example — real-world content

</details>

**Information gaps:**
- No US-undergrad-instructor review of FOLIO content appropriateness for classroom use
- No data on whether geopolitically sensitive examples disproportionately affect specific demographic subgroups of students

**Requires expert verification:**
- Whether examples involving communist/Russian/North Korean content should be filtered or contextualized for US classroom deployment

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input modality (text-only English [Q22]) and writing system (Latin + standard logical symbols) match the deployment exactly. Linguistic register is high-quality formal English with documented quality control (Grammarly check [Q49], English Literature reviewer pass [Q50], disambiguation conventions for disjunction/quantifiers/plurals [Q130-Q134]). One material concern remains: FOLIO uses Russell & Norvig FOL syntax [Q52], not the Fitch-style notation of the Barwise & Etchemendy curriculum [WEB-1, WEB-3]. The benchmark's own inference engine does not natively support its syntax and required a custom parser [Q149, Q150]. With IF priority LOWER and notation being the only meaningful concern (not modality), the dimension is well-aligned with minor reservations. Dataset sampling also identified some double-negative NL phrasing [DATASET-D33] that could create pedagogical noise.

**Strengths:**
- Text-only English-language input [Q22] matches deployment modality exactly
- Strong NL quality control: Grammarly check [Q49] plus English Literature reviewer pass [Q50]
- Explicit disambiguation conventions for disjunction, quantifier phrasing, singular/plural [Q130-Q134] reduce surface-form ambiguity
- Readability distribution documented [Q59, Q154] supports accessibility assessment

**Checklist:**

- **IF-1**: Signal distributions match: both source and deployment are text-only English [Q22]. No image, audio, or multimodal mismatch. Dataset confirms uniformly text-formatted premises and conclusions [DATASET-D1 through D36]. — _Sources: Q22, DATASET-D1_
- **IF-2**: Regional infrastructure supports text input fully — ~66-72% of US undergraduates use laptop/desktop primary [WEB-5], appropriate for symbolic-input tasks. ~64% experience unstable internet [WEB-5], which is a delivery concern but not an input-form one. — _Sources: WEB-5_
- **IF-3**: Domain-specific form difference: FOLIO uses Russell & Norvig flat FOL syntax [Q52] rather than Fitch-style numbered-line subproof notation [WEB-3, WEB-4]. This is a notation mismatch within the input-form layer that affects how formal-input strings are encoded. — _Sources: Q52, Q149, WEB-3, WEB-4, DATASET-D13_
- **IF-4**: External-validity concerns: (a) FOL notation differs from Fitch syntax students are taught — no published mapping exists [WEB-3, WEB-14]; (b) some NL premises use double-negative phrasing that may be pedagogically noisy [DATASET-D33]. — _Sources: Q149, DATASET-D33, WEB-14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'We use formal logic, i.e., FOL to ensure the logical validity of the examples written in NL' (p.2)
- [Q52] 'We adopt the FOL definitions and syntax most widely used in the AI community (Russell and Norvig, 2010)' (p.5)
- [Q49] 'All the sentences are first checked with a grammar checking tool, Grammarly' (p.4)
- [Q50] 'Our annotators who have graduated from or are senior students studying English Literature conducted a thorough round of review' (p.4)
- [Q149] 'The inference engine does not support input in the FOL syntax adopted by standard education material (Russell and Norvig, 2010), which is used in our dataset' (p.14)

*Web sources:*
- [WEB-3] OpenLogicProject Fitch checker confirms LPL Fitch notation is a distinct community-standard syntax
- [WEB-4] logicmatters.net documents that Fitch (LPL), Jaśkowski, Kalish-Montague, and Gamut natural deduction styles are notationally distinct
- [WEB-5] ~66-72% of US undergraduates primarily use laptop/desktop — supports text/symbolic input
- [WEB-14] el-sambal/fitch-proof checker uses LPL Fitch notation distinct from FOLIO's R&N syntax

*Dataset analysis:*
- DATASET-D13: '∀x (OlympicGoldMedalWinner(x) → ProfessionalAthlete(x))' — Russell & Norvig flat FOL, no Fitch line numbers or rule citations
- DATASET-D33: 'No satin-finish lipsticks in the set do not have rosewood in its official description' — double-negative NL phrasing

</details>

**Information gaps:**
- No published systematic mapping between FOLIO's Russell & Norvig operators and LPL Fitch rule names

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's output ontology is a three-way truth-value label (True/False/Unknown) determined by a FOL inference engine [Q36, Q66, Q94]. The deployment requires fundamentally different outputs: numbered Fitch-style proof traces with premise citations and inference-rule names, plus countermodels for invalid arguments (elicitation A1, A2). Dataset sampling confirms the schema contains exactly six fields with no proof-trace, rule-citation, or countermodel artifact for any example [DATASET-D1, D14, D4]. With OO priority HIGH, the output-ontology mismatch is essentially total: FOLIO labels every False example with only 'False', providing no countermodel for the deployment's required artifact [DATASET-D14]. The operator inventory [Q138] overlaps with Fitch connectives but no rule-vocabulary mapping exists [WEB-14].

**Strengths:**
- Engine-verified three-way labels [Q36, Q66] are reliable ground truth for the deductive-validity sub-judgment the deployment must make before producing a proof
- Three-way distinction (True/False/Unknown) [Q94] identifies two distinct invalid-argument modes (contradiction vs. underdetermination) — useful signal even if countermodels are absent
- Standard FOL operator inventory [Q138] overlaps with Fitch connective set

**Checklist:**

- **OO-1**: Output categories required by deployment: (a) validity judgment (True/False/Unknown is approximately compatible); (b) numbered proof-trace with rule citations (absent); (c) countermodel for invalid arguments (absent); (d) register-differentiated explanation form (absent). — _Sources: Q36, Q66_
- **OO-2**: Missing categories specific to deployment: countermodel construction for False-labeled examples [Q66, DATASET-D14]; proof-trace structure (numbered lines, subproof boxes, rule-citation field) — none present in the FOLIO schema [DATASET schema observation in Concern 1]; register tags for introductory vs. advanced (absent). — _Sources: Q66, DATASET-D14, WEB-10_
- **OO-3**: FOLIO encodes Russell & Norvig FOL conventions [Q52] rather than Fitch-style rule taxonomy used by the LPL curriculum [WEB-3, WEB-4]. The decision rule (engine-verified single label) is curriculum-neutral but ignores the pedagogical structure of proof. — _Sources: Q52, WEB-3, WEB-4_
- **OO-4**: Stakeholder-driven redesign is warranted: a Fitch-rule-aligned proof-trace ontology would require introducing per-step rule labels, premise-citation fields, and subproof-structure tags — categories entirely absent from FOLIO. — _Sources: WEB-3, WEB-14_
- **OO-5**: Structural-validity violation: the construct 'logical argument validity in pedagogical context' has substantive internal structure (rule application, subproof discharge, countermodel) that FOLIO's single-label ontology collapses into a binary/ternary judgment. Content-validity violation: countermodel and rule-citation categories are entirely missing. — _Sources: Q94, Q138, DATASET-D1, DATASET-D14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q36] 'Each of the stories is composed of several premises and conclusions with truth values of True, False, or Unknown' (p.4)
- [Q66] 'Given P and H, the goal is to determine the truth values of the conclusions: True, False or Unknown, based on FOL reasoning' (p.6)
- [Q94] 'The majority baseline of our dataset is 38.5% since in our test set, there are 87, 78 and 61 examples with labels of true, false and unknown' (p.7)
- [Q138] 'We include the following operators: negation ¬, conjunction ∧, disjunction ∨, implication →, universal quantifier ∀, existential quantifier ∃, equal =' (p.13)

*Web sources:*
- [WEB-3] OpenLogicProject Fitch — LPL Fitch rule-name vocabulary (→E, ∧I, etc.) is distinct from FOLIO's flat-FOL representation
- [WEB-10] 'Learning to Disprove' and CounterMath confirm no off-the-shelf benchmark covers FOL countermodel construction as a pedagogical output
- [WEB-14] el-sambal/fitch-proof documents LPL rule syntax with no cross-reference to FOLIO's operators

*Dataset analysis:*
- DATASET-D1: True-labeled example provides only the label, no proof trace showing deduction steps
- DATASET-D14: False-labeled example 'There are no journalists that were born in Yorkshire' provides only the label 'False', no countermodel artifact
- DATASET-D4: False-labeled example provides only the label, no explanation of which step in the chain fails
- Dataset schema observation: exactly six fields (premises, premises-FOL, conclusion, conclusion-FOL, label, IDs) — no proof-trace, rule-citation, or countermodel fields exist

</details>

**Information gaps:**
- Whether the inference engine, internally, generates countermodels as a byproduct for False-labeled examples (not exposed in schema)

**Requires expert verification:**
- Whether a custom Fitch-rule-tagged extension of FOLIO is feasible as a supplementation strategy

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
For the labels FOLIO does provide, ground-truth quality is high: engine-verified [Q2, Q57], multi-stage expert annotation [Q29, Q124, Q125], 39.2% rewrite rate to address quality issues [Q48], and expert-annotator accuracy of 95.98% [Q111] confirming label reliability. However, with OC priority MODERATE, two distinct concerns lower the score substantially: (1) no ground-truth content exists for pedagogically-acceptable explanations, Fitch-style rule citations, register-appropriate prose, or countermodels — the artifacts the deployment needs to evaluate; (2) dataset sampling found ~10% rate of FOL annotation artifacts (free variables, missing parentheses, NL/FOL contradiction, name mismatches) [DATASET-D24, D25, D26, D23, D30, D27] that could propagate as incorrect ground truth if used for NL-FOL translation evaluation or model training.

**Strengths:**
- Engine-verified labels [Q2, Q57] provide deterministic ground truth for deductive validity
- Two-stage expert quality control (NLP/CL experts for NL, FOL experts for FOL) [Q29, Q124, Q125]
- 39.2% of stories rewritten to address quality issues [Q48] — substantial QC investment
- Expert annotators achieve 95.98% accuracy [Q111], confirming labels are well-formed

**Checklist:**

- **OC-1**: Truth-value labels are derived from formal inference and are not subject to regional-stakeholder disagreement — formal validity is invariant across US logic curricula. However, the deployment's required outputs (proof traces, countermodels, register-appropriate explanations) have no ground truth in FOLIO at all. — _Sources: Q2, Q57_
- **OC-2**: No disagreement expected on True/False/Unknown labels because they are engine-verified [Q2]. Disagreement is irrelevant because the deployment-relevant output types are absent. — _Sources: Q2, Q111_
- **OC-3**: Annotator demographics are documented at a high level: college/graduate students, native or near-native English, formal FOL coursework [Q27, Q28, Q122, Q123]. No fine-grained demographic breakdown is provided; geographic distribution of annotators unspecified. — _Sources: Q27, Q122, Q123_
- **OC-4**: Re-annotation by US-logic-instructor pool would be needed to introduce ground-truth Fitch-style proof traces, rule citations, register-tagged explanations, and countermodels — none exist in FOLIO. Dataset sampling also revealed FOL annotation errors that warrant cleanup [DATASET-D24, D25, D26]. — _Sources: DATASET-D24, DATASET-D25, DATASET-D26_
- **OC-5**: Aggregation method (single engine-verified label per example) cannot encode minority perspectives because formal validity admits no minority view. The relevant concern is not aggregation but absence of explanation-quality labels. — _Sources: Q2_
- **OC-6**: Convergent-validity concern is minimal for the label that is present; external-validity concern is high because no labels exist for the explanation/countermodel artifacts the deployment must evaluate. Additionally, ~10% FOL-annotation-artifact rate observed in sample [DATASET-D24, D25, D26, D23, D30, D27] could harm convergent validity for NL-FOL translation evaluation. — _Sources: Q53, DATASET-D24, DATASET-D25, DATASET-D26, DATASET-D23, DATASET-D30, WEB-7_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'The logical correctness of the premises and conclusions is ensured by their FOL annotations, which are automatically verified by an FOL inference engine' (p.1)
- [Q29] 'At the NL quality check stage, only annotators who are experts in natural language processing or computational linguistics are involved. For the FOL quality check, only annotators who are experts in first-order logic are involved' (p.4)
- [Q48] 'we manually screened all stories and found that 39.2% of the stories suffer from at least one of these issues' (p.4)
- [Q111] 'Expert annotations achieve an accuracy of 95.98% while non-expert annotations achieves 61.82%' (p.9)
- [Q53] 'we found that the human-written FOL formulas suffer from FOL consistency issues, which necessitates an additional round of quality control' (p.5)
- [Q122] 'Our annotators are either college or graduate students who are native English speakers or possess near-native proficiency in English' (p.12)

*Web sources:*
- [WEB-7] P-FOLIO companion adds NL proof chains but not Fitch-style rule-cited proofs
- [WEB-9] 2025 ITS study finds LLM hints score only 75% on contextual explanation — confirms explanation-quality evaluation is a research frontier without ground-truth corpora

*Dataset analysis:*
- DATASET-D24: free variable 'x' unbound in premises-FOL of Example 2 — FOL annotation error
- DATASET-D25: missing closing parenthesis in Example 36 premises-FOL
- DATASET-D26: NL says 'Matt does not invest' but FOL omits negation — direct NL/FOL contradiction
- DATASET-D23: Example 52 NL uses 'John' while FOL uses 'jim' — entity-naming inconsistency
- DATASET-D30: '∃x ∃y ∃y ∃w' duplicate variable declaration
- DATASET-D27: extra closing parenthesis in Example 10 premises-FOL

</details>

**Information gaps:**
- Full FOL-annotation error rate across all 1,430 examples (sample-based lower-bound is ~10%)
- Fine-grained annotator demographics beyond 'college/graduate students with FOL coursework'

**Requires expert verification:**
- Whether observed FOL annotation artifacts are systematic or distributed; would benefit from re-running the inference engine across the full corpus

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's output form is single-label classification accuracy [Q80] plus, for the translation subtask, Syntactic Validity and Execution Accuracy [Q73-Q76]. The deployment requires evaluation of structured, register-differentiated, rule-justified multi-step proof traces and countermodels — none of which FOLIO's metrics assess. With OF priority HIGH, the output-form mismatch is essentially complete. The evaluation infrastructure (Stanford CS221 inference engine + custom Python parser [Q148-Q151]) is purpose-built for label verification, and the authors themselves flag the need for a 'more reliable metric of NL-FOL translation' [Q77]. Dataset sampling confirms no proof-trace or countermodel artifact exists at the data level [Concern 1]. The only sub-task FOLIO can directly score for the deployment is the binary validity precondition, which is necessary but radically insufficient.

**Strengths:**
- Accuracy metric [Q80] is appropriate for the deductive-validity sub-judgment that must occur before proof generation
- Translation Execution Accuracy [Q75, Q76] measures whether translated FOL preserves semantics — partially relevant to NL-to-formal-form correctness in the deployment
- Confusion-matrix and depth-stratified analysis [Q99, Q155-Q157] reveal failure modes (over-prediction of True; harder at depths 4-7) that inform deployment risk assessment

**Checklist:**

- **OF-1**: Output modality mismatch is total. FOLIO output: single label. Deployment output: numbered Fitch-style proof trace + premise citations + rule names + plain-English summary + (for invalid args) countermodel + register tag. — _Sources: Q80, DATASET-D1, DATASET-D14_
- **OF-2**: Not applicable — speech/TTS not required for either source or deployment (text-only).
- **OF-3**: Text-only output is accessible for most US undergraduates. Accessibility for screen-reader users with formal-notation output (MathML or equivalent) is a separate platform concern flagged as needing verification.
- **OF-4**: External-validity violation is severe: no FOLIO metric assesses (a) Fitch-style rule-citation correctness, (b) premise-citation correctness, (c) register appropriateness, (d) countermodel validity, (e) pedagogical clarity. The authors themselves note the need for better translation metrics [Q77]. The output-form gap is the deepest validity problem identified. — _Sources: Q77, Q152, WEB-7, WEB-9, WEB-10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q80] 'We use accuracy for evaluating logical reasoning performance' (p.6)
- [Q73] 'Two metrics are adopted to evaluate NL-FOL translation: 1). Syntactic validity (SynV)' (p.6)
- [Q75] 'Inference Engine execution accuracy (ExcAcc). The group of translated FOL for premises and conclusions in one story is fed into our inference engine' (p.6)
- [Q77] 'We leave for future work the design of a more reliable metric of NL-FOL translation' (p.6)
- [Q148] 'we adopt the inference engine provided in the Stanford CS221 course page' (p.14)
- [Q152] 'Although LLMs such as GPT-4 can be utilized to conduct the conversion, it is hard to ensure the GPT-4 outputs are always correct' (p.14)

*Web sources:*
- [WEB-7] P-FOLIO adds pass@k over multi-step NL proof chains — closest existing extension but still not Fitch-style rule-cited proofs
- [WEB-9] 2025 ITS study uses 4-criterion rubric (consistency, clarity, contextual explanation, pedagogical appropriateness) for LLM hints — closest to deployment evaluation but for propositional logic, not Fitch
- [WEB-10] No benchmark evaluates formal countermodel construction as first-class output for pedagogical FOL/propositional logic

*Dataset analysis:*
- Schema observation (Concern 1): six fields (premises, premises-FOL, conclusion, conclusion-FOL, label, IDs) — no proof-trace, rule-citation, or countermodel fields
- DATASET-D14: False-labeled example with no countermodel artifact
- DATASET-D1: True-labeled example with no proof trace

</details>

**Information gaps:**
- Whether any FOLIO-derived rubric for proof-trace quality has been developed in follow-up work beyond P-FOLIO

**Requires expert verification:**
- Whether the deployment can use P-FOLIO's NL proof chains as a stepping-stone supplement despite their non-Fitch format

---

## Remediation Suggestions

### Output Ontology ⚠

**Gap:** No proof-trace structure or countermodel artifacts in output ontology; FOLIO collapses to single label

**Recommendation:** Build a Fitch-aligned output schema (numbered lines, rule-name field, premise-citation field, subproof-box markers, countermodel-as-domain-assignment field) and elicit reference proof traces from logic-instructor annotators for a curated subset of FOLIO stories; use P-FOLIO [WEB-7] as a starting NL-chain corpus and convert to Fitch notation.

### Output Form ⚠

**Gap:** Accuracy metric does not evaluate proof-trace quality, register, or countermodel correctness

**Recommendation:** Develop a multi-component rubric drawing on the 2025 ITS study's criteria [WEB-9] (consistency, clarity, contextual explanation, pedagogical appropriateness) extended with Fitch-specific items (rule-name correctness, premise-citation correctness, subproof-discharge correctness); use both LLM-grader and human-instructor ratings.

### Input Content

**Gap:** Explicit-premise-only content; some geopolitically sensitive examples may distract in US classroom context

**Recommendation:** Filter or contextualize examples involving politically loaded predicates (communist, North Korean nationality, Russian sanctions [DATASET-D6, D16, D19]) for classroom deployment; develop an everyday/quasi-legal enthymeme corpus to complement FOLIO's fully-explicit-premise content.

### Input Form

**Gap:** Russell & Norvig FOL syntax mismatches Fitch-style notation students learn

**Recommendation:** Develop and publish a systematic mapping between FOLIO's flat-FOL operators and LPL Fitch rule names (→E, ∧I/∧E, ∨E with subproof, ∀E, ∃E with subproof, ¬I); incorporate the lplfitch LaTeX package and el-sambal/fitch-proof checker [WEB-14] as reference encoders.

### Input Ontology

**Gap:** No propositional-only subtask and no implicit-premise/enthymeme reconstruction subtask

**Recommendation:** Complement FOLIO with Rosetta-PL [WEB-11] or DivLogicEval [WEB-12] for propositional coverage; develop a custom enthymeme corpus drawn from US-textbook exercises (Hurley, Bergmann/Moor/Nelson) for implicit-premise reconstruction evaluation.

### Output Content

**Gap:** ~10% FOL annotation-artifact rate observed in dataset sample (free variables, missing parens, NL/FOL contradiction, name mismatches)

**Recommendation:** Re-run the inference engine on the full corpus and audit examples flagged in the dataset analysis [DATASET-D24, D25, D26, D23, D30, D27]; produce a cleaned subset before using FOLIO for any training or NL-FOL translation evaluation.

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
| Q21 | 2 | output_content | "We release a natural language reasoning dataset written by expert annotators, FOLIO, with first-order logical reasoning problems." |
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
| Q35 | 4 | input_content | "We ask the annotators to create new stories from scratch without using templates based on real-world knowledge, which should be plausible in general." |
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
| Q55 | 5 | input_content | "Apart from checking whether NL and FOL express equivalent meanings, we also add necessary commonsense knowledge in both the NL and FOL premises. Sometimes humans do not write certain commonsense knowledge in the premises that is required in the FOL reasoning process, which is based solely on the premises given. We add such knowledge as additional premises at this stage." |
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
| Q70 | 6 | input_form | "In our dataset, the premises and conclusions are set up in such a way to ensure that the inference engine always returns an answer given enough resources such as time and memory." |
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
| Q114 | 9 | output_content | "We focus on collecting a very high-quality dataset in evaluating logical reasoning rather than merely a large dataset." |
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
| Q158 | 15 | output_form | "To test if the premise ordering in FOLIO has spurious correlations with the conclusion label which a model can exploit, we shuffle the input premises to evaluate models." |
| Q159 | 15 | output_form | "We find that accuracy increases or decreases by roughly 1% in most settings compared to our unshuffled premises." |
| Q160 | 15 | output_form | "This indicates that the ordering of premises in FOLIO examples does not yield significant information about the label, and thus models will not be able to use the premise ordering as a strong heuristic or statistical feature for its predictions." |
| Q161 | 15 | input_form | "FOL formulas have a clearer and more straightforward logical structure than NL sentences." |
| Q162 | 15 | output_form | "As shown in Table 11, the performance slightly increases in the NL+FOL setting for GPT-4 while GPT-3.5 performs worse in both the NL+FOL and the FOL-only settings." |
| Q163 | 15 | output_form | "FOL always serves as additional useful information for GPT-4, but not for GPT-3.5 regardless of whether FOL is concatenated with NL." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://press.uchicago.edu/ucp/books/book/distributed/L/bo12734345.html |
| WEB-2 | https://github.com/OpenLogicProject/fitch-checker |
| WEB-3 | https://github.com/OpenLogicProject/fitch |
| WEB-4 | https://www.logicmatters.net/latex-for-logicians/nd/ |
| WEB-5 | https://www.newamerica.org/education-policy/edcentral/how-do-community-college-students-access-online-learning/ |
| WEB-6 | https://er.educause.edu/articles/2023/1/the-evolving-landscape-of-students-mobile-learning-practices-in-higher-education |
| WEB-7 | https://aclanthology.org/2024.findings-emnlp.966/ |
| WEB-8 | https://openreview.net/forum?id=rhdfTOiXBng |
| WEB-9 | https://arxiv.org/abs/2505.04736 |
| WEB-10 | https://arxiv.org/pdf/2603.19514 |
| WEB-11 | https://arxiv.org/pdf/2505.00001 |
| WEB-12 | https://arxiv.org/html/2509.15587v3 |
| WEB-13 | https://aclanthology.org/2021.findings-acl.317.pdf |
| WEB-14 | https://github.com/el-sambal/fitch-proof |
| WEB-15 | https://openreview.net/pdf?id=rhdfTOiXBng |
| WEB-16 | https://en.wikipedia.org/wiki/Language,_Proof_and_Logic |
| WEB-17 | https://fitch.rug.themisjudge.nl/ |
| WEB-18 | https://www.sciencedirect.com/science/article/pii/S2666920X25001304 |
| WEB-19 | https://arxiv.org/abs/2410.09207 |
| WEB-20 | https://github.com/wellecks/naturalproofs |
| WEB-21 | https://huggingface.co/datasets/yale-nlp/P-FOLIO |
| WEB-22 | https://arxiv.org/pdf/2505.14932 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (config: default)
**Analysis date:** 2025-07-14
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | FOLIO/train | Ex. 1 | True | "No plants are fungi. Mushrooms are fungi. / ∀x (Plant(x) → ¬Fungi(x)) ∀x (Mushroom(x) → Fungi(x))" | Simple 2-premise syllogism with parallel NL and FOL | IO, IC |
| D2 | FOLIO/train | Ex. 2 | Uncertain | "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises… Mike works in this tech company. If Mike is not a person who wears the same flannel shirts every day, has very high energy, and is impulsive, then Mike either is very consistent and enjoys sticking to his regular routines or does not like surprises." | Multi-premise story (7 premises) about a tech company worker; complex conditional | IO, IC |
| D3 | FOLIO/train | Ex. 3 | Uncertain | "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac. Sam is using a Mac. If a song is not titled 'Perfect,' Sam will never play it." | Multi-step chain mixing disjunction, implication, and named individual | IO |
| D4 | FOLIO/train | Ex. 4 | False | "No trick-shot artist in Yale's varsity team struggles with half court shots. Everyone on Yale's varsity team is someone who struggles with half court shots or who successfully shoots a high percentage of 3-pointers." — "Jack is bad at mid-range shots." | Basketball sports story requiring 4+ step chain | IO, IC |
| D5 | FOLIO/train | Ex. 5 | Uncertain | "All Yale students at the event are college students. Everyone at the event is a Yale student or a Harvard student. If Susan is a Yale student, then she does not like independence." | Classic university-setting syllogism with exclusive disjunction | IO |
| D6 | FOLIO/train | Ex. 6 | Uncertain | "All entrepreneurs at the business conference enjoy the opportunity of starting a business. Everyone at the business conference who is an ardent communist prefers state ownership of the means of production. Ho is at the business conference and prefers state ownership of the means of production." | Politically framed scenario with communist/investor dichotomy | IC, OC |
| D7 | FOLIO/train | Ex. 7 | Uncertain | "Andy Chang directed EndGame. Andy Chang is from Hong Kong." — conclusion: "All of Andy Chang's movies are filmed outside of Washington." | Wikipedia-seeded story about a real-world film director from Hong Kong | IC |
| D8 | FOLIO/train | Ex. 8 | Uncertain | "Every person in Potterville that knows magic flies. All wizards in Potterville know magic. Harry, who lives in Potterville either yells or flies." | Fictional Potterville scenario referencing Harry/Potter (Harry Potter allusion) | IC |
| D9 | FOLIO/train | Ex. 11 | False | "Everything in Size Town is big or small. All big things in Size Town are heavy… The bird is in Size Town and it is not both heavy and still." — conclusion: "If the bird is small or still, then it is either unpredictable or changing." | Purely abstract Size Town scenario — no real-world content | IC |
| D10 | FOLIO/train | Ex. 12 | True | "Some cats are not pets. All cats are mammals." — conclusion FOL: "∃x ∃y (Mammal(x) ∧ Mammal(y) ∧ ¬Pet(x) ∧ ¬Pet(y))" | Simple existential syllogism; conclusion FOL is strictly stronger than needed | OC, OO |
| D11 | FOLIO/train | Ex. 13 | False | "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable… ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." | Real-world brand story about a specific luxury cosmetics product | IC |
| D12 | FOLIO/train | Ex. 15 | Uncertain | "John Nash designed Oxford Circus. John Nash is a British architect. Oxford Circus is the entrance to Oxford Circus tube station, a part of the Central line in 1900." | Wikipedia-seeded story about real architect John Nash | IC |
| D13 | FOLIO/train | Ex. 16 | True | "All Olympic gold medal winners are professional athletes. All Nobel physics laureates are full-time scientists. Amy spends the most time on sports, or Amy is an Olympic gold medal winner. If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." | Multi-step chain combining disjunction, contrapositive, complex reasoning | IO |
| D14 | FOLIO/train | Ex. 17 | False | "Michael O'Donnell is a British physician, journalist, author, and broadcaster… Michael O'Donnell was born in Yorkshire" — conclusion: "There are no journalists that were born in Yorkshire." | Simple false universal overgeneralization from a positive instance | OO |
| D15 | FOLIO/train | Ex. 21 | False | "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing… Clyde is a professor who takes a historical approach." | Complex 6-premise story about cultural interests and academic roles | IO |
| D16 | FOLIO/train | Ex. 22 | Uncertain | "All PRC nationals are entitled to national social insurance coverage. Everyone in the Franco-China diplomatic conference is either a PRC national or a French national, but not both… Either Mei is a North Korean and can have medical bills partially covered, or neither is true." | Geopolitical scenario involving PRC, France, North Korea nationals | IC |
| D17 | FOLIO/train | Ex. 23 | Uncertain | "The world's only major large passenger aircraft manufacturers are Boeing and Airbus." — conclusion: "There exists a SpaceX commercial aircraft." | Real-world entities (Boeing, Airbus, SpaceX) in an Uncertain-labeled example | IC, OC |
| D18 | FOLIO/train | Ex. 27 | Uncertain | "Bobby Flynn finished 7th while competing on Australian Idol. Australian Idol competitors are Australian citizens." — conclusion: "Bobby Flynn flew to America in 2007." | Wikipedia-seeded story about Australian musician | IC |
| D19 | FOLIO/train | Ex. 28 | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. There is an embargo on Russian foreign trade goods." — conclusion: "In Russia, an effective monetary policy is possible." | Real-world geopolitical/economic scenario involving Russia and embargos | IC, OC |
| D20 | FOLIO/train | Ex. 33 | Uncertain | "No battery-powered watch is automatic. All digital watches are battery-powered. Moonwatch is either a digital watch and an automatic, or it is neither." | Classic syllogistic chain about watches | IO |
| D21 | FOLIO/train | Ex. 34 | True | "All orphan planets are rogue planets. If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." | Scientific Wikipedia-seeded story about astronomy | IC |
| D22 | FOLIO/train | Ex. 43 | True | "All inductive reasoning processes derive general principles from a body of observations. Modus Ponens is not both used in inductive reasoning and used for statistical generalization. Modus Ponens is a component of a major part of reasoning rule." | Story explicitly about Modus Ponens and inductive/deductive reasoning | IC, IO |
| D23 | FOLIO/train | Ex. 52 | True | "No athletes never exercise. All professional basketball players are athletes… Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." — NOTE: FOL annotation says "jim" while NL says "John" | Annotation inconsistency: NL uses "John," FOL uses "jim" | OC |
| D24 | FOLIO/train | Ex. 2 | Uncertain | premises-FOL contains: "¬(∃y (flannelShirt(y) ∧ WearEveryday(x, y)) ∧ Have(mike, highEnergy) ∧ Impulsive(mike)) → (Consistent(mike) ∧ StickTo(mike, theirRegularRoutine)) ⊕ ¬Like(mike, surprise)" — uses unbound variable x in outer formula | FOL annotation contains a free variable 'x' not properly bound | OC |
| D25 | FOLIO/train | Ex. 36 | True | "Lily is in James' family; she watches TV series in cinemas." — premises-FOL: "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" | Malformed FOL: missing closing parenthesis in the premises-FOL formula | OC |
| D26 | FOLIO/train | Ex. 57 | False | "Matt does not invest in the public stock market regularly. Matt likes financial risks." — premises-FOL premise 6: "InvestInRegularly(matt, publicStockMarket)" | NL premise contradicts FOL annotation: NL says "does not invest" but FOL asserts InvestInRegularly(matt) without negation | OC |
| D27 | FOLIO/train | Ex. 10 | Uncertain | "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" — extra closing parenthesis in last premise FOL | Minor FOL syntax artifact (extra parenthesis) | OC |
| D28 | FOLIO/train | Ex. 4 | False | "No trick-shot artist in Yale's varsity team struggles with half court shots." conclusion-FOL: "BadAt(jack, midRangeShot)" | Short FOL conclusion for a 5-premise story requiring multi-step chain | IO |
| D29 | FOLIO/train | Ex. 46 | Uncertain | "Everyone that knows about breath-first-search knows how to use a queue… Jack is entitled to the right to life and liberty, has human rights, or knows about the first-in-first-out data structure." | CS / human rights story — 7 premises requiring complex multi-step chain | IO |
| D30 | FOLIO/train | Ex. 54 | True | "All players must reach the yellow stage before they can reach the green stage. The yellow stage comes after the red stage." — premises-FOL contains "∃x ∃y ∃y ∃w" (duplicate variable y) | Minor FOL annotation typo: variable y declared twice | OC |
| D31 | FOLIO/train | Ex. 50 | Uncertain | "Each building is tall. Everything tall has height." — conclusion: "All buildings are magnificent." | Extremely short, minimal story (2 premises) — simple non-sequitur conclusion | IO |
| D32 | FOLIO/train | Ex. 55 | False | "TikTok is a social media application, and it is not ideal for preteens." — conclusion-FOL: "Contain(tikTok, chatFeature) ⊕ ComputerProgram(tikTok))" — extra closing parenthesis | FOL annotation has mismatched parenthesis | OC |
| D33 | FOLIO/train | Ex. 13 | False | "No satin-finish lipsticks in the set do not have 'rosewood' in its offical description." | Double-negative NL phrasing ("No X do not have") that may create ambiguity | IF |
| D34 | FOLIO/train | Ex. 43 | True | "Modus Ponens is a component of a major part of reasoning rule." premises-FOL: "ArgumentForm(modusPonens)" | Example featuring logic-domain content (Modus Ponens) — relevant to deployment | IC, IO |
| D35 | FOLIO/train | Ex. 16 | True | "All professional athletes spend most of their time on sports… If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." | Contrapositives and multi-step chains matching textbook exercise style | IO |
| D36 | FOLIO/train | Ex. 38 | False | "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination… James has a car or works at Meta." | Contemporary real-world scenario (Meta/Google) embedded in logic chain | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Strong coverage of multi-premise, multi-step deductive FOL reasoning
- **Dimension(s):** IO
- **Observation:** The sampled examples span a wide range of reasoning depths, from simple 2-premise syllogisms to 7-premise chains requiring sequential chaining of conditionals, universal quantifiers, and disjunctions. Multiple examples require traversing 4–6 logical steps before reaching a conclusion, directly matching the deployment's need to evaluate complex deductive reasoning.
- **Deployment relevance:** The deployment must assess whether an LLM can correctly determine argument validity before generating a pedagogical trace. FOLIO's depth distribution — confirmed in the data — provides genuine difficulty stratification across introductory (simple syllogisms) and advanced (multi-step chains) registers.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO, train, True): "No plants are fungi. Mushrooms are fungi." — Minimal 2-premise syllogism, analogous to introductory-level exercises.
  - [D2] Example 2 (FOLIO, train, Uncertain): "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises… Mike works in this tech company." — 7-premise story requiring multiple chained universals and a complex conditional, analogous to advanced-level exercises.
  - [D29] Example 46 (FOLIO, train, Uncertain): "Everyone that knows about breath-first-search knows how to use a queue… Jack is entitled to the right to life and liberty, has human rights, or knows about the first-in-first-out data structure." — 7-premise story with chained conditionals and disjunction.

#### Strength 2: Parallel NL and FOL representations per example
- **Dimension(s):** IO, IF
- **Observation:** Every example contains both a natural-language story and its parallel FOL annotation, supporting both the validity-determination task and the NL-to-FOL translation secondary task. The FOL layer uses the standard operator inventory (¬, ∧, ∨, →, ⊕, ∀, ∃, =) consistently across examples.
- **Deployment relevance:** The deployment requires NL-to-formal-logic translation as a core capability. FOLIO's parallel annotations allow evaluation of whether an LLM can correctly formalize NL premises, which is a prerequisite for the Fitch-style proof generation the tool needs to produce.
- **Datapoint citations:**
  - [D13] Example 16 (FOLIO, train, True): NL "All Olympic gold medal winners are professional athletes" → FOL "∀x (OlympicGoldMedalWinner(x) → ProfessionalAthlete(x))" — straightforward universal conditional mapping.
  - [D21] Example 34 (FOLIO, train, True): "All orphan planets are rogue planets. If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." — complex conditional with negated conjunction, illustrating the NL→FOL difficulty range.

#### Strength 3: Topical diversity supporting broad argument-type coverage
- **Dimension(s):** IC
- **Observation:** The sampled examples cover a wide range of content domains: natural science (biology, astronomy, physics), geography, sports, technology, economics, media, cultural activities, and everyday scenarios. This variety mirrors the range of argument types students encounter in US undergraduate logic courses, where textbook exercises span analogous domains.
- **Deployment relevance:** Students in intro logic courses encounter arguments drawn from diverse subject matter. FOLIO's topical range reduces the risk that a model fine-tuned or evaluated on FOLIO will be topically overfitted to any single domain.
- **Datapoint citations:**
  - [D21] Example 34 (FOLIO, train, True): "All orphan planets are rogue planets… PSO J318.5−22…" — astrophysics domain.
  - [D11] Example 13 (FOLIO, train, False): "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable…" — consumer products domain.
  - [D19] Example 28 (FOLIO, train, False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. There is an embargo on Russian foreign trade goods." — macroeconomics/geopolitics domain.
  - [D4] Example 4 (FOLIO, train, False): "No trick-shot artist in Yale's varsity team struggles with half court shots." — sports domain.

#### Strength 4: Three-way label distribution includes True, False, and Uncertain
- **Dimension(s):** OO
- **Observation:** The sampled examples include all three label categories. Across the 57 reviewed examples, all three labels appear in meaningful proportions, including several False examples requiring the reasoner to identify why a conclusion does not follow or is contradicted.
- **Deployment relevance:** The deployment must identify both valid and invalid arguments. The False and Uncertain labels cover two distinct failure modes (contradiction and underdetermination), which partially map to the deployment's need to handle invalid arguments (for which countermodels are required). FOLIO does not produce countermodels, but the label space at least identifies where they would be needed.
- **Datapoint citations:**
  - [D14] Example 17 (FOLIO, train, False): "Michael O'Donnell is a British physician, journalist, author, and broadcaster… Michael O'Donnell was born in Yorkshire" — conclusion "There are no journalists that were born in Yorkshire" is False because the premises provide a direct counterexample.
  - [D28] Example 4 (FOLIO, train, False): "Jack is bad at mid-range shots" — labeled False given the premises about Yale's varsity team.
  - [D5] Example 5 (FOLIO, train, Uncertain): "Susan is a college student" — labeled Uncertain because her affiliation (Yale vs. Harvard) cannot be determined.

#### Strength 5: Explicit formal premise structure matching formal-logic course exercises
- **Dimension(s):** IC
- **Observation:** FOLIO premises are stated as explicit, closed-world assertions (all universals, conditionals, and individual facts are spelled out), directly matching the style of textbook logic exercises where students are given a set of premises and asked to assess a conclusion. This matches the exercise format in Barwise & Etchemendy-style courses.
- **Deployment relevance:** The deployment tool must handle arguments presented as explicit premise sets (as in textbook exercises), which is the dominant format in US undergraduate logic courses. FOLIO's explicit-premise style is well-suited for this sub-task, even if implicit-premise reconstruction is separately needed.
- **Datapoint citations:**
  - [D20] Example 33 (FOLIO, train, Uncertain): "No battery-powered watch is automatic. All digital watches are battery-powered. Some mechanical watches are automatic. All smart watches are digital. Moonwatch is either a digital watch and an automatic, or it is neither." — Complete set of explicit premises in the style of a textbook exercise.
  - [D31] Example 50 (FOLIO, train, Uncertain): "Each building is tall. Everything tall has height." — Minimal premise set; conclusion "All buildings are magnificent" tests non-sequitur recognition.

#### Strength 6: One example contains content directly relevant to logic pedagogy
- **Dimension(s):** IC, IO
- **Observation:** One example in the sample explicitly features Modus Ponens as a named entity within the story, along with discussion of inductive vs. deductive reasoning. While framed as a logic puzzle rather than a pedagogical explanation, this content is directly relevant to the deployment's domain.
- **Deployment relevance:** Students using the tool will be reasoning about logic itself (meta-logical arguments). FOLIO contains at least some examples where the content domain is formal reasoning, which aligns with logic course content.
- **Datapoint citations:**
  - [D22] Example 43 (FOLIO, train, True): "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning… Modus Ponens is a component of a major part of reasoning rule." — The entity "Modus Ponens" appears as a subject of logical predicates, directly engaging the deployment's pedagogical domain.
  - [D34] Example 43 (FOLIO, train, True): "ArgumentForm(modusPonens)" in the FOL annotation — confirms the named rule appears in formal representation.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Output space is a three-way classification label — no proof traces, no countermodels
- **Dimension(s):** OO, OF
- **Observation:** Every example in the dataset has a single string label (True/False/Uncertain). There are no fields for step-by-step reasoning chains, numbered deduction steps, premise citation patterns, inference rule names, or countermodel specifications. The schema has exactly six fields: premises, premises-FOL, conclusion, conclusion-FOL, label, and IDs. No ground-truth proof trace or explanation artifact exists anywhere in the data.
- **Deployment relevance:** The deployment's primary output requirement is a numbered, rule-justified, register-differentiated proof trace (or countermodel for invalid arguments). FOLIO cannot directly evaluate whether a model produces such an output. The benchmark's output ontology and output form are completely orthogonal to what the deployment needs to score. Every False-labeled example (where a countermodel is required) provides only the label, with no reference countermodel to evaluate against.
- **Datapoint citations:**
  - [D14] Example 17 (FOLIO, train, False): "Michael O'Donnell is a British physician, journalist, author, and broadcaster… Michael O'Donnell was born in Yorkshire as the son of a general practitioner." — Labeled False, but the dataset provides no countermodel showing that there exists a journalist born in Yorkshire; only the string "False" is present.
  - [D4] Example 4 (FOLIO, train, False): "Jack is bad at mid-range shots." — Labeled False with no explanation of which step in the chain fails or what interpretation demonstrates the falsity.
  - [D1] Example 1 (FOLIO, train, True): "No plants are fungi. Mushrooms are fungi." — Labeled True, but no proof trace showing the deduction steps is provided; a deployment requiring "applying modus ponens to premises 2 and 4" has no reference output to compare against.

#### Concern 2: Notation mismatch — FOLIO uses Russell & Norvig FOL, not Fitch-style natural deduction
- **Dimension(s):** IF, OO
- **Observation:** All FOL annotations in the dataset use Russell & Norvig-style flat predicate logic notation (e.g., `∀x (Plant(x) → ¬Fungi(x))`, with infix operators and no subproof structure). Fitch-style natural deduction, as used in Barwise & Etchemendy's LPL curriculum, uses a structurally different notation: numbered lines, subproof boxes, and named inference rules (e.g., →E, ∧I, ¬I). There is no Fitch-style annotation, no rule-name vocabulary, and no subproof structure anywhere in the 57 reviewed examples.
- **Deployment relevance:** The deployment's target students are taught Fitch-style notation. A tool producing outputs in Russell & Norvig FOL notation would be misaligned with what students are expected to produce and recognize. There is no documented mapping between FOLIO's operator vocabulary and LPL rule names. This is not merely a surface formatting difference — ∀E (universal elimination, a named Fitch rule) vs. the implicit universal instantiation in FOLIO's flat FOL involves different pedagogical scaffolding.
- **Datapoint citations:**
  - [D13] Example 16 (FOLIO, train, True): "∀x (OlympicGoldMedalWinner(x) → ProfessionalAthlete(x))" — flat FOL implication, no rule name cited; in Fitch style this would be referenced as line N, rule ∀E applied to a specific premise line.
  - [D2] Example 2 (FOLIO, train, Uncertain): "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" — Russell & Norvig predicate notation with no Fitch structural markers.

#### MAJOR

#### Concern 3: No propositional-logic-only examples — all examples use FOL constructs
- **Dimension(s):** IO
- **Observation:** Every example in the sample uses at least one first-order logic construct (universal quantifier ∀, existential quantifier ∃, or predicates with arguments). There are no propositional-only examples using only sentential connectives (¬, ∧, ∨, →, ↔) applied to atomic propositions without quantification. The deployment requires handling of propositional logic as a distinct layer.
- **Deployment relevance:** US introductory logic courses (both philosophy and CS-flavored) typically begin with propositional/sentential logic before introducing predicate logic. Students learning to use the tool early in their course will present purely propositional arguments. FOLIO provides no coverage of this sub-domain.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO, train, True): "∀x (Plant(x) → ¬Fungi(x)) ∀x (Mushroom(x) → Fungi(x))" — even the simplest example uses universal quantification, not propositional logic.
  - [D31] Example 50 (FOLIO, train, Uncertain): "∀x (Building(x) → Tall(x)) ∀x (Tall(x) → Height(x))" — 2-premise minimal example still uses FOL quantifiers rather than sentential connectives.
  - [D9] Example 11 (FOLIO, train, False): "∀x (In(x, sizeTown) → (Big(x) ∨ Small(x)))" — abstract scenario still uses universal quantification throughout.

#### Concern 4: All premises are fully explicit — no implicit-premise or enthymeme cases
- **Dimension(s):** IC
- **Observation:** In every reviewed example, all premises needed for the inference are stated explicitly in the premise set. There are no enthymematic arguments where a premise is left implicit and must be reconstructed from context or background knowledge. The annotation process explicitly added commonsense premises as explicit FOL statements, confirmed by the data: even highly structured "everyday" scenarios list every required premise.
- **Deployment relevance:** The deployment explicitly requires handling arguments where premises are implicit and must be reconstructed — "Students regularly encounter arguments with implicit premises and multi-step chains drawn from everyday or quasi-legal scenarios." FOLIO provides no coverage of this sub-task. A model evaluated solely on FOLIO would have no signal about its ability to perform premise reconstruction.
- **Datapoint citations:**
  - [D36] Example 38 (FOLIO, train, False): "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination. People will either take a bus or drive to their destination. Everyone who has a car will choose to drive to their destination. No students drive to their destination. James has a car or works at Meta." — What could be a 1-premise implicit argument ("James works at Meta, so he won't take the bus") is instead fully expanded into 6 explicit premises, eliminating any need for premise reconstruction.
  - [D19] Example 28 (FOLIO, train, False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. A country cannot simultaneously regulate the exchange rate and successfully control inflation… There is an embargo on Russian foreign trade goods." — All intermediate economic causal links are stated as explicit premises; no inference to unstated background knowledge is required.

#### Concern 5: FOL annotation errors found in sampled examples
- **Dimension(s):** OC
- **Observation:** Several FOL annotations in the reviewed sample contain apparent errors: (a) a free (unbound) variable `x` in Example 2's premises-FOL; (b) a missing closing parenthesis in Example 36's premises-FOL; (c) a contradictory annotation in Example 57 where the NL premise states "Matt does not invest in the public stock market regularly" but the FOL encodes `InvestInRegularly(matt, publicStockMarket)` without negation; (d) a variable declared twice (`∃x ∃y ∃y ∃w`) in Example 54; (e) an extra closing parenthesis in Example 55's conclusion-FOL; (f) a cross-name inconsistency in Example 52 where NL says "John" but FOL uses "jim."
- **Deployment relevance:** If FOLIO is used to evaluate a model's NL-to-FOL translation capability (the secondary task), annotation errors in the reference FOL create incorrect ground truth, inflating or deflating translation scores. More critically, if a model is trained on FOLIO's FOL annotations, these errors propagate into learned behavior. Given the deployment's requirement for formally correct proof traces, training data with FOL inconsistencies is a meaningful concern.
- **Datapoint citations:**
  - [D24] Example 2 (FOLIO, train, Uncertain): "¬(∃y (flannelShirt(y) ∧ WearEveryday(x, y)) ∧ Have(mike, highEnergy) ∧ Impulsive(mike)) → ..." — `x` is unbound in this formula while `mike` is bound, indicating a free-variable error.
  - [D25] Example 36 (FOLIO, train, True): "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" — missing closing parenthesis after `jameSFamily`.
  - [D26] Example 57 (FOLIO, train, False): NL: "Matt does not invest in the public stock market regularly" vs. FOL premise 6: "InvestInRegularly(matt, publicStockMarket)" — the negation is absent from the FOL annotation.
  - [D23] Example 52 (FOLIO, train, True): NL uses "John" throughout; FOL uses "jim" — inconsistent entity naming between NL and FOL layers.
  - [D30] Example 54 (FOLIO, train, True): "∃x ∃y ∃y ∃w" — variable `y` declared twice in the existential prefix.
  - [D27] Example 10 (FOLIO, train, Uncertain): "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" — extra closing parenthesis.

#### Concern 6: Content occasionally involves politically or geopolitically sensitive real-world scenarios
- **Dimension(s):** IC, OC
- **Observation:** Several examples use real-world geopolitical entities and politically loaded content: one example involves an "ardent communist" in a business conference context, another uses Russian economic sanctions, and another uses PRC/French/North Korean nationals in a diplomatic conference. While the logical structure is neutral, the content choices may introduce distracting associations for US undergraduate students and could touch on politically sensitive areas in a classroom setting.
- **Deployment relevance:** For an educational tool targeting US undergraduates, content involving communist ideology, Russian sanctions, or North Korean nationality may generate controversy or distraction unrelated to the logic task. The deployment context mentions content neutrality as a concern.
- **Datapoint citations:**
  - [D6] Example 6 (FOLIO, train, Uncertain): "Everyone at the business conference who is an ardent communist prefers state ownership of the means of production. Ho is at the business conference and prefers state ownership of the means of production." — "Ardent communist" as a predicate in a logical argument.
  - [D19] Example 28 (FOLIO, train, False): "There is an embargo on Russian foreign trade goods." — Contemporary geopolitical scenario.
  - [D16] Example 22 (FOLIO, train, Uncertain): "No North Korean nationals are citizens of the European Union… Either Mei is a North Korean and can have medical bills partially covered, or neither is true." — North Korean nationality as a logical predicate.

#### MINOR

#### Concern 7: Absent test split in the HuggingFace dataset
- **Dimension(s):** OF
- **Observation:** The HF dataset schema shows only `train` (1,001 examples) and `validation` (203 examples) splits. The test split (226 examples per the paper) is not present in the public HuggingFace release. All sampled examples are from the train split.
- **Deployment relevance:** If the deployment uses FOLIO as an evaluation benchmark, the relevant held-out test set is unavailable via the standard HuggingFace loader. The validation set (203 examples) would need to serve as the evaluation partition, which reduces the evaluation sample size and may introduce slight coverage differences from what the paper reports.
- **Datapoint citations:** (schema-level observation, not datapoint-specific — all 57 reviewed examples are from `train` split per the metadata)

#### Concern 8: Some examples contain double-negative or ambiguous NL phrasing
- **Dimension(s):** IF
- **Observation:** At least one premise in the reviewed examples uses a double-negative construction ("No satin-finish lipsticks in the set do not have 'rosewood' in its official description") that is grammatically non-standard and could be construed as either a negated universal or an accidentally-double-negated affirmative. While the FOL annotation resolves the ambiguity, NL-level phrasing quality is uneven.
- **Deployment relevance:** The deployment requires clear, natural-language explanations that students can follow. If FOLIO's NL tier contains confusingly phrased premises, models trained on or evaluated against these examples may learn to produce similarly unclear phrasing in pedagogical explanations.
- **Datapoint citations:**
  - [D33] Example 13 (FOLIO, train, False): "No satin-finish lipsticks in the set do not have 'rosewood' in its official description." — Double negative construction may confuse students who encounter this as an explanation example.

#### Concern 9: Some HybLogic examples are visibly template-derived with artificial scenario framing
- **Dimension(s):** IC
- **Observation:** Several examples use purely abstract or fictional settings (Size Town, Potterville) that have no real-world grounding. While logically valid as test cases, these scenarios may feel pedagogically thin relative to the everyday and quasi-legal argument contexts the deployment aims to support.
- **Deployment relevance:** The deployment specifically targets arguments "drawn from everyday or quasi-legal scenarios." Abstract fictional-world examples like Size Town or Potterville do not represent the argument types students encounter in practice, though they may still be useful for evaluating logical form comprehension in isolation.
- **Datapoint citations:**
  - [D9] Example 11 (FOLIO, train, False): "Everything in Size Town is big or small. All big things in Size Town are heavy… The bird is in Size Town and it is not both heavy and still." — Entirely abstract fictional world with no real-world referent.
  - [D8] Example 8 (FOLIO, train, Uncertain): "If someone in Potterville yells, then they are not cool… Harry, who lives in Potterville either yells or flies." — Fictional scenario (Harry Potter allusion) with no everyday reasoning context.

---

### Content Coverage Summary

The 57 reviewed examples span a realistic range of multi-step FOL deductive reasoning scenarios, drawn from both Wikipedia-seeded real-world topics (British architects, Australian musicians, aerospace companies, Russian economic policy, astronomy) and template-generated syllogistic chains (watch types, basketball shooting percentages, abstract Size Town). The label distribution in the sample skews toward Uncertain (approximately 55%), with True (~30%) and False (~15%) also present, consistent with the documented test-set distribution.

Topically, the examples cover science, sports, consumer goods, geopolitics, CS/technology, media, everyday social scenarios, and even one example explicitly about Modus Ponens and inductive reasoning. Register is consistently formal written English with care given to grammatical naturalness, though several double-negative or structurally complex NL phrasings were observed.

The FOL annotation layer is dense and uses the full operator inventory (¬, ∧, ∨, →, ⊕, ∀, ∃, =) across examples. However, the sample revealed a non-trivial rate of annotation artifacts: free variables, mismatched parentheses, contradictory NL/FOL pairs, and cross-entity name inconsistencies across 6 of 57 reviewed examples (~10%). These are not concentrated in any single story cluster but appear distributed across the sample.

Critically for the deployment, the dataset contains no propositional-logic-only examples, no implicit-premise cases, no proof traces of any kind, and no countermodel artifacts. The output schema is uniformly a three-way classification label. The FOL notation is Russell & Norvig-style flat predicate logic, with no Fitch-style structural markers, subproof annotations, or inference-rule name vocabulary.

---

### Limitations

1. **Sample size and split coverage:** Only 57 of 1,204 total examples were reviewed, all from the `train` split. The validation split (203 examples) was not sampled. Coverage uncertainty exists for rare story types and edge cases.

2. **Test split unavailability:** The HuggingFace release omits the test split (226 examples), so the reported benchmark performance figures (majority baseline 38.5%, expert accuracy 95.98%) cannot be directly verified against the available data.

3. **HybLogic vs. WikiLogic proportions:** The sample does not allow precise identification of which examples are WikiLogic vs. HybLogic (no `source` field is present in the schema). Differential analysis of implicit-premise style or AST diversity by source pipeline is not possible from the available data.

4. **FOL annotation error rate:** Six annotation artifacts were found in 57 examples. This is a lower bound — other syntactically valid but semantically incorrect annotations may exist and are not detectable without running the inference engine. The true error rate across the full dataset may differ.

5. **Countermodel content:** It is not possible from the data alone to determine whether the inference engine, when applied to False-labeled examples, could generate countermodels as a byproduct. The schema captures only the truth-value label, not any intermediate inference engine output.

6. **P-FOLIO companion dataset:** The web search findings identified P-FOLIO (EMNLP 2024) as a companion dataset with human-written NL proof chains for FOLIO stories. P-FOLIO was not sampled or analyzed here; it may partially address the output-form gap noted above, though it uses narrative NL chains rather than Fitch-style proofs.

