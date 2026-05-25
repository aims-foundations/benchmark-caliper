## Deployment Context

We are a US debate coaching platform evaluating whether an LLM can assess the strength of informal, real-world arguments made by American high school students in competitive debate contexts. Arguments involve empirical claims, value judgments, rhetorical moves, and evidence of varying quality. The system should assess argument strength holistically — including logical validity, evidence quality, relevance, and persuasive effectiveness.

# Validity Analysis: folio
**Target context:** US High School Competitive Debate — Argument Quality Assessment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ⚠ | 1 | Serious concern | high |
| **Average** | **1.5** | | |

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

FOLIO is a high-quality benchmark for formal deductive entailment over natural-language premises, with rigorous annotation, verified labels, and substantial logical complexity. However, for the US high school competitive debate argument-quality assessment deployment, FOLIO is fundamentally misaligned across five of six validity dimensions. The input ontology omits all deployment-required argument categories (evidence-backed claims, value-laden arguments, rhetorical moves, debate-structural arguments). The input content is deliberately stripped of normative contestation and evidentiary disputes — the very content types most central to debate. The output ontology (True/False/Unknown) cannot represent multi-dimensional sub-scores, qualitative feedback, or pairwise rankings. The output content's correctness standard (theorem-prover verification by FOL-trained CS students) is categorically different from the pluralistic, format-varying, circuit-varying debate-community judgment standard. The output form produces a single categorical label, structurally uninformative for the deployment's required outputs. Only the input form (text in standard American English) aligns well. Dataset analysis across 57 sampled examples confirms these gaps empirically: no example contains evidence citation, normative contestation, debate-structural arguments, sub-scores, rationales, or pairwise comparisons. The benchmark provides at most a narrow upper-bound test on multi-step deductive validity, which is one minor component of the deployment's logical-structure sub-score — far from sufficient for deployment-level evaluation.

## Practical Guidance

### What This Benchmark Measures

FOLIO measures formal deductive entailment over natural-language premise sets and NL-to-FOL translation accuracy. Within the deployment's framework, it provides signal for only a narrow sub-component of the 'logical structure and warrant quality' sub-score — specifically, whether a model can correctly determine entailment relationships under multi-step deduction. It does not measure evidence quality (the highest-weight deployment sub-dimension), relevance/responsiveness, persuasive effectiveness, debate-structural argument recognition, value-laden argument assessment, or format/circuit-conditioned quality norms.

### Construct Depth

FOLIO probes deductive validity rigorously, with reasoning depth modal at 4 and a diverse AST distribution [Q60, Q61], and provides a clean expert/non-expert performance gap demonstrating the construct is meaningfully measured [Q111]. However, the construct it probes deeply is *not* the construct the deployment needs. The benchmark provides no probing of inductive reasoning, evidence credibility, warrant-claim coherence in hedged empirical claims, or pluralistic argument quality. The depth of FOLIO's measurement on deductive validity does not compensate for the breadth gap across the deployment's required constructs.

### What Else You Need

Substantial supplementation is required across nearly every dimension. For input ontology (IO) and input content (IC): supplement with debate-specific corpora such as DebateSum [WEB-21] and OpenDebateEvidence [WEB-22] for evidence-card content, and develop NSDA-format-specific argument-type taxonomies covering DAs, CPs, kritiks, T shells, theory, and impact calculus. For output ontology (OO) and output form (OF): construct a multi-dimensional rubric with separate sub-scores (evidence, logic, relevance, persuasion), qualitative rationale generation, and pairwise comparison structures, drawing on DebateBench [WEB-28], IBM ArgQ pairwise datasets [WEB-24], and CompAQA [WEB-26]. For output content (OC): recruit a panel of NSDA-credentialed judges and coaches, stratified by format (Policy/LD/PF/Congressional) and circuit (lay/tech), to provide ground-truth annotations that reflect actual debate-community norms. Pair circuit-conditioned scoring with judge-paradigm metadata from Tabroom. Verify NSDA evidence-ethics policy compliance [NSDA verification gap noted in regional context]. FOLIO can be retained only as a narrow component sub-test for deductive-validity-specific capability, not as an end-to-end deployment proxy.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's input ontology is organized exclusively around formal deductive entailment and NL-FOL translation [Q15, Q63, Q67], with task complexity operationalized through reasoning depth and AST diversity [Q60, Q61]. The deployment requires assessment of inductive/evidentiary reasoning, value-laden claims, rhetorical moves, and debate-specific structural arguments (DAs, CPs, kritiks, T shells, theory) — none of which appear in FOLIO's taxonomy. Dataset analysis confirms zero coverage: even when 'inductive reasoning' appears, it is treated as a deductive predicate label rather than as an actual inductive inference [DATASET-D3, D25]. The HIGH-priority elicitation flag on IO is fully borne out.

**Strengths:**
- Provides a rigorous upper-bound test for the narrow sub-component of multi-step deductive validity, with reasoning depth modal at 4 and 28.7% of examples requiring 5+ inference steps [Q60], and substantially more distinct ASTs than prior datasets [Q61]

**Checklist:**

- **IO-1**: The deployment requires test categories spanning: (a) evidence-backed empirical arguments, (b) value-laden/normative claims (LD, Congressional), (c) rhetorical/persuasive moves, (d) debate-specific structural arguments (DAs, CPs, kritiks, T, theory, impact calculus), and (e) pairwise rebuttal comparison. Evidence quality is identified as the highest-weight sub-dimension per elicitation. — _Sources: WEB-22, WEB-28_
- **IO-2**: FOLIO's taxonomy omits all five of the above categories. The benchmark is framed strictly around deductive entailment over premise sets [Q15, Q66] and NL-FOL translation [Q18, Q67]. Dataset analysis confirms zero presence of debate-specific tokens (disadvantage, counterplan, kritik, topicality, solvency, impact, turn, burden, framework, value, criterion) across the 57 sampled examples. — _Sources: Q15, Q63, DATASET-D1, DATASET-D7, DATASET-D20_
- **IO-3**: FOLIO includes the NL-FOL translation task [Q3, Q67] which is largely irrelevant to the deployment — debate coaching does not require translating speeches into formal first-order logic. Syllogism-template-instantiated stories [Q42, Q43] also have low ecological validity for actual debate discourse. — _Sources: Q3, Q43, Q67_
- **IO-4**: Category gaps are total relative to deployment-critical evaluation: evidence-handling, value-laden argument assessment, rhetorical effectiveness, and debate-structural moves are entirely unrepresented. Authors themselves note prior NL benchmarks are inadequate for measuring complex reasoning [Q8, Q9, Q10], but FOLIO's response narrows the scope further into pure deductive logic rather than broadening to argumentation. — _Sources: Q8, Q9, Q10, DATASET-D3_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q15] 'We present a natural language reasoning dataset, FOLIO, with first-order logic reasoning problems which require the models to decide the correctness of conclusions given a world defined by the premises.' (p.1)
- [Q43] 'There are 256 logically distinct types of syllogisms and 24 of them are valid (Lehman, 1973). We use various combinations of 24 valid syllogisms. We also add in conjunction, disjunction, and implication.' (p.4)
- [Q60] 'the mode of reasoning depths is four in FOLIO. 28.7% of the examples need five or more depths of reasoning' (p.5)
- [Q63] 'We define two new tasks based on FOLIO, natural language reasoning with first-order logic and NL-FOL translation.' (p.6)

*Web sources:*
- [WEB-28] DebateBench (arXiv 2502.06279) demonstrates that LLM-based debate speech scoring benchmarks exist for BP format but with adjudication-norm content absent in FOLIO
- [WEB-22] OpenDebateEvidence (NeurIPS 2024) provides actual US competitive debate evidence corpus structure, confirming the categorical gap from FOLIO's logic-puzzle ontology

*Dataset analysis:*
- DATASET-D1: Two-premise syllogism with no evidentiary content — confirms purely formal deductive task structure
- DATASET-D3: 'Inductive reasoning' appears only as a named predicate within deductive reasoning — no actual inductive inference performed
- DATASET-D7: Exclusive-disjunction chain with no debate-relevant structure
- DATASET-D20: Six-premise WikiLogic chain with no rhetorical, persuasive, or debate-structural elements

</details>

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO content is deliberately constructed to be free of evidentiary disputes, normative contestation, and culturally embedded judgment [Q47, Q127], with stories rewritten to remove biases and opinionated language [Q48, Q127]. The deployment, by contrast, centers on contested empirical claims, value-laden arguments, and miscontextualized evidence as the highest-weight sub-dimensions. Dataset analysis confirms that even when politically adjacent content appears (Russia embargo, state ownership, TikTok addictiveness, human rights), it is rendered as deductive predicate labels rather than as evidentiary or normative claims [DATASET-D2, D4, D5, D10, D22]. The HIGH-priority elicitation flag on IC is fully borne out.

**Strengths:**
- Diverse topical breadth in WikiLogic stories covers geography, science, economics, technology, and consumer products [Q38, Q62, DATASET-D2, D15, D16], so the benchmark does not over-narrow into a single domain vocabulary
- Authors deliberately screened out biased/stereotyped content [Q47, Q127] — for general logical-validity sub-testing this is a quality-positive even though it removes the very normative contestation the deployment requires

**Checklist:**

- **IC-1**: The deployment requires content that reflects contested empirical claims (PF/Policy), value disputes (LD/Congressional), and circuit-specific argument registers (lay vs. tech). Content must include cited evidence with sources, authors, and recency [WEB-21, WEB-22]. FOLIO content does not require this — premises are stated as definitional universals or given facts [DATASET-D1, D2, D17, D24]. — _Sources: WEB-21, WEB-22, DATASET-D1, DATASET-D2, DATASET-D17, DATASET-D24_
- **IC-2**: FOLIO content is deliberately neutralized of normatively charged content [Q47, Q127], and 'psychologically fundamental generalizations' are explicitly accepted as a workaround [Q128]. The deployment requires content that *engages* contested value claims (e.g., 'civil liberties vs. national security' per 2026 NSDA LD topics [WEB-18]) — the benchmark systematically excludes this content type. — _Sources: Q47, Q127, Q128, WEB-18_
- **IC-3**: FOLIO does not require region-specific knowledge in a problematic way (American English, broad topic seeds), but it does not contain Western-debate-specific knowledge either — no evidence cards, no warrant-citation patterns, no spread/flow language. The mismatch is in argument register, not regional culture per se. — _Sources: DATASET-D22, DATASET-D24_
- **IC-4**: INSUFFICIENT DOCUMENTATION — the paper does not report regional annotator review. The dataset analysis substitutes for this: 57 sampled examples were reviewed against deployment criteria and found to contain zero competitive-debate content.
- **IC-5**: Content issues are severe: (a) no evidence-citation structure — confirmed across all sampled examples; (b) no hedged empirical claims [DATASET-D24, D22]; (c) no value-pluralism content [DATASET-D4, D5]; (d) potential pretraining contamination of WikiLogic stories [Q104, DATASET concern 9]. — _Sources: Q104, DATASET-D4, DATASET-D5, DATASET-D10, DATASET-D22_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q47] 'Our dataset prioritizes realism and factual accuracy, steering clear of biases and stereotypes linked to identity markers like race, ethnicity, gender, sexuality, nationality, class, and religion.' (p.4)
- [Q127] 'We took out stories that had strongly opinionated language and contained gender, racial, and classist biases.' (p.13)
- [Q104] 'since the examples in WikiLogic are created from scratch by humans, it is possible that LLMs have seen similar texts with similar logical patterns in the training data.' (p.8)
- [Q128] 'We accept certain classes of "psychologically fundamental generalizations"' (p.13)

*Web sources:*
- [WEB-18] NSDA topics include normatively contested resolutions (civil liberties vs. national security, plea bargaining justice, encryption lawful access) — the exact content FOLIO excludes
- [WEB-21] DebateSum exemplifies the evidence-card structure with citation/author/recency metadata absent from FOLIO
- [WEB-22] OpenDebateEvidence provides 3.5M documents of actual debate evidence with source citations — confirms the IC content gap

*Dataset analysis:*
- DATASET-D2: Russia embargo claim stated as logical axiom rather than as cited evidence requiring credibility assessment
- DATASET-D4: 'State ownership of means of production' appears as a predicate label — no value judgment required
- DATASET-D5: Social insurance policy treated as definitional universal — no contested empirical claim
- DATASET-D10: Human rights framing used purely as deductive predicate — no normative weight evaluated
- DATASET-D22: TikTok addictiveness rendered as logical axiom rather than empirically contested claim
- DATASET-D17: Boeing/Airbus/SpaceX factual claims encoded as fixed premises, not as warranted evidence

</details>

**Information gaps:**
- No paper-level documentation of how debate-community reviewers would assess FOLIO content (substituted by dataset analysis)

**Requires expert verification:**
- Whether any subset of WikiLogic stories happens to mirror specific Policy/PF resolution content closely enough to provide partial deployment signal — likely zero based on sample, but full corpus not reviewed

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
FOLIO is text-only, standard American English, with grammar checked via Grammarly and reviewed by English Literature annotators [Q49, Q50]. The deployment is also text-only English (with possible speech-transcript input out of current scope). Dataset analysis confirms no modality or script mismatch across all 57 sampled examples. The IF priority was correctly flagged LOWER in elicitation; main residual concern is register mismatch — FOLIO uses logic-textbook universal-statement register, while debate discourse uses hedged, evidence-citing, warrant-heavy language.

**Strengths:**
- Text-only English with no modality, script, or language mismatch [Q22, DATASET-D1, D8]
- Grammar and naturalness checked by linguistically trained annotators [Q49, Q50]
- Standardized NL conventions reduce ambiguity [Q130-Q133]

**Checklist:**

- **IF-1**: Both source and target are text in standard American English [Q49, Q50]. Signal distribution matches at the modality level; no resolution/sampling-rate analog applies to text. — _Sources: Q22, Q49, DATASET-D1, DATASET-D8_
- **IF-2**: US school infrastructure supports text input via Chromebooks and personal devices per deployment context. No infrastructure mismatch.
- **IF-3**: Register mismatch is a domain-specific form difference: FOLIO uses formal-universal sentences ('All X are Y') with named constants [DATASET-D1, D24], while debate discourse uses hedged citations, spread delivery transcripts, and warrant-heavy phrasing [WEB-21, WEB-22]. If speech transcripts (with disfluencies, mid-sentence corrections) enter scope, the gap widens further. — _Sources: DATASET-D1, DATASET-D24, WEB-21, WEB-22_
- **IF-4**: Form mismatches at the modality level are minimal; register-level differences are documentable but secondary to the IO/IC/OO/OC/OF mismatches. — _Sources: Q130_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'We use formal logic, i.e., FOL to ensure the logical validity of the examples written in NL' (p.2)
- [Q49] 'All the sentences are first checked with a grammar checking tool, Grammarly.' (p.4)
- [Q50] 'Our annotators who have graduated from or are senior students studying English Literature conducted a thorough round of review for grammatical correctness and language naturalness.' (p.4)
- [Q130] 'We always use "either-or" to express exclusive disjunction.' (p.13)

*Web sources:*
- [WEB-21] DebateSum evidence cards include hedged author/citation register absent from FOLIO
- [WEB-22] OpenDebateEvidence transcripts include the hedged, warrant-citing register typical of competitive debate

*Dataset analysis:*
- DATASET-D1: Standard English text confirmed
- DATASET-D8: Grammatically natural complex sentence structure
- DATASET-D24: Formal-universal register ('Everyone working at Meta has a high income') differs from hedged empirical debate claims

</details>

**Information gaps:**
- Whether deployment will include ASR-transcribed speech (with disfluencies, spread delivery artifacts) — out of current scope per deployment context but flagged as potential future expansion

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's output label space is the three-way categorical scheme True/False/Unknown [Q36, Q66], with FOL operators restricted to standard truth-functional connectives and quantifiers [Q138]. Temporal logic, modal logic, and Davidsonian semantics are explicitly excluded [Q139-Q142]. The deployment requires multi-dimensional sub-scores across evidence quality, logical structure, relevance, and persuasive effectiveness, plus qualitative coaching feedback, pairwise rebuttal rankings, and format/circuit-conditioned norms. Dataset analysis confirms every example produces exactly one categorical label with no sub-scores, no rationales, and no comparative structure [DATASET-D11, D13, D18, D23]. The HIGH-priority elicitation flag on OO is fully borne out.

**Strengths:**
- Output label space is unambiguous and well-defined [Q135-Q137] — for the narrow sub-component of logical validity, the three-way scheme is principled
- Open-world assumption is correctly handled via the Unknown label [DATASET-D23]

**Checklist:**

- **OO-1**: FOLIO labels are True/False/Unknown [Q36, Q66]. These categories do not map to any deployment-required output: sub-score per dimension, qualitative feedback, pairwise ranking, or circuit-conditioned scoring [elicitation A2, A3]. — _Sources: Q36, Q66_
- **OO-2**: All deployment-relevant output categories are missing: (a) evidence-quality sub-score, (b) relevance/responsiveness sub-score, (c) persuasive-effectiveness sub-score, (d) pairwise comparative ranking, (e) format/circuit-conditioned quality bands. Note that BP-debate scoring benchmarks exist [WEB-28] but FOLIO does not approximate them. — _Sources: WEB-26, WEB-28, DATASET-D13, DATASET-D18_
- **OO-3**: FOLIO's output ontology encodes the assumption that argument correctness is mechanically verifiable via theorem proving [Q2, Q135-Q137]. The deployment's correctness standard is pluralistic and community-norm-based — these assumptions are categorically incompatible. — _Sources: Q2, Q135, Q137_
- **OO-4**: Stakeholder-driven taxonomy redesign would not be a 'redesign' of FOLIO — it would require constructing an entirely separate evaluation with no shared output space. FOLIO cannot be adapted; only supplemented. — _Sources: Q138, Q139_
- **OO-5**: Taxonomy issues represent a fundamental structural validity violation. Benchmark performance metrics (accuracy over True/False/Unknown, majority baseline 38.5% [Q94]) cannot inform any of the deployment's required output dimensions. — _Sources: Q94, DATASET-D11_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q36] 'Each of the stories is composed of several premises and conclusions with truth values of True, False, or Unknown' (p.4)
- [Q66] 'Given P and H, the goal is to determine the truth values of the conclusions: "True", "False" or "Unknown", based on FOL reasoning.' (p.6)
- [Q135] 'FOL enables deriving facts from other facts (Russell and Norvig, 2010).' (p.13)
- [Q138] 'We include the following operators: negation ¬, conjunction ∧, disjunction ∨, implication →, universal quantifier ∀, existential quantifier ∃, equal =.' (p.13)
- [Q139] 'Following (Russell and Norvig, 2010), we consider temporal logic and modal logic as special-purpose logics.' (p.13)

*Web sources:*
- [WEB-26] CompAQA framework demonstrates pairwise argument quality ranking as a separate task structure — confirms FOLIO's OO does not support it
- [WEB-28] DebateBench uses speech-level scores and house rankings — a fundamentally different output ontology from FOLIO's True/False/Unknown

*Dataset analysis:*
- DATASET-D11: Output is single True/False/Uncertain label with no sub-dimensions
- DATASET-D13: Six-premise chain collapses to single 'True' label — no sub-scores, no rationale
- DATASET-D18: Multiple conclusions from same story scored independently, not pairwise
- DATASET-D23: Open-world assumption correctly handled via Uncertain label

</details>

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO ground-truth labels are mechanically derived from a theorem prover [Q2, Q57] and human annotators are CS undergraduates/graduates with formal FOL training and native or near-native English proficiency [Q27, Q28, Q122, Q123]. The expert/non-expert performance gap (95.98% vs. 61.82%, 34.16 points) confirms that FOL domain knowledge is necessary for the benchmark's correctness standard [Q107-Q112]. The deployment's quality-defining community is NSDA/TOC judges, circuit coaches, and the broader competitive-debate community — a categorically different population with different domain expertise and different correctness norms (paradigms, lay vs. tech circuit). Dataset analysis confirms every label is theorem-prover output [DATASET-D9, D12]. The HIGH-priority elicitation flag on OC is fully borne out.

**Strengths:**
- Within the narrow scope of formal deductive validity, labels are mechanically verified and reproducible [Q2, Q57] — no annotator disagreement or subjective variance
- Annotation process is rigorous: 980 person-hours across six stages [Q32], senior researcher review [Q31], dedicated FOL and NL expert subgroups [Q29, Q124, Q125]

**Checklist:**

- **OC-1**: Ground-truth labels are theorem-prover outputs [Q2, Q57] derived from FOL annotations by CS-trained annotators [Q27, Q28]. They do not reflect debate-community quality judgments — paradigm-based judging, circuit norms, and coach rubrics play no role. — _Sources: Q2, Q57, WEB-12_
- **OC-2**: The annotator population (CS students familiar with FOL [Q108]) is categorically different from the deployment's quality-defining community (NSDA judges, TOC paradigms, coaches). The non-expert annotation experiment in the paper itself shows that even high school students unfamiliar with FOL achieve only 61.82% accuracy on FOLIO labels [Q109, Q111] — indicating that FOLIO's correctness standard does not converge with the population most similar to the deployment's end users. — _Sources: Q108, Q109, Q111, WEB-26_
- **OC-3**: Annotator demographics are documented: native or near-native English speakers, CS/graduate students with FOL coursework or self-study [Q27, Q28, Q122, Q123]. No debate-community annotators are reported. — _Sources: Q27, Q28, Q122, Q123_
- **OC-4**: Label re-annotation by debate judges/coaches would not produce comparable labels — the labels capture FOL entailment, not argument quality. Re-annotation would require redefining the task, not refining labels. — _Sources: Q2, Q137_
- **OC-5**: Labels are deterministic (theorem-prover output), so aggregation does not erase minority perspectives within FOLIO's scope. However, this very determinism is the problem: pluralistic debate-community judgment cannot be approximated by a deterministic prover [Q137]. — _Sources: Q137, DATASET-D9_
- **OC-6**: Convergent validity is violated because FOLIO labels do not correlate with the deployment's correctness standard; external validity is violated because performance on FOLIO labels does not generalize to debate-community quality judgments. — _Sources: Q111, Q112, DATASET-D12_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'The logical correctness of the premises and conclusions is ensured by their FOL annotations, which are automatically verified by an FOL inference engine.' (p.1)
- [Q27] 'Our annotators are either college or graduate students who are native English speakers or possess near-native proficiency in English.' (p.3)
- [Q108] 'Our expert annotators are computer science college students familiar with FOL.' (p.9)
- [Q111] 'Expert annotations achieve an accuracy of 95.98% while non-expert annotations achieves 61.82%, with a gap of 34.16%.' (p.9)
- [Q112] 'This shows that sufficient domain knowledge of FOL is necessary for good performance on FOLIO.' (p.9)

*Web sources:*
- [WEB-12] NSDA Nationals adjudication and judge paradigms define a community-norm-based quality standard fundamentally different from theorem-prover labels
- [WEB-26] CompAQA notes low inter-rater agreement (kappa ~0.10-0.12) for argument quality — confirming inherent pluralism in debate-relevant judgment absent in FOLIO

*Dataset analysis:*
- DATASET-D9: Label derived from FOL formula and theorem prover, not human judgment of argument quality
- DATASET-D12: Ground truth 'False' on Russia monetary policy story is mechanically derived from FOL inference, not from debate-community judgment

</details>

**Requires expert verification:**
- Whether any FOLIO labels would be considered 'persuasive' or 'well-warranted' by debate judges if the corresponding NL stories were used as speech material — likely no systematic correlation, but not empirically tested

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's output form is a single categorical label per conclusion [Q80, Q153], with the NL-FOL translation task using Syntactic Validity and Inference Engine Execution Accuracy [Q73-Q76]. The deployment requires multi-dimensional sub-scores, free-text coaching rationales, and pairwise comparative outputs (per elicitation A2). Dataset analysis confirms all 57 examples produce single labels with no sub-scores, no rationales, no comparative structures [DATASET-D13, D14, D19, D21]. The authors themselves acknowledge the translation metric is insufficiently reliable [Q77]. The HIGH-priority elicitation flag on OF is fully borne out.

**Strengths:**
- Accuracy over a balanced three-way label space [Q80, Q94] is a clean, reproducible metric within FOLIO's scope
- Multiple random seeds and averaged results [Q93] support statistical reliability of the metric
- Premise-shuffling analysis confirms metric is not gameable via ordering heuristics [Q158-Q160]

**Checklist:**

- **OF-1**: Output modality (single categorical label) does not match deployment needs: separate sub-scores per dimension, free-text qualitative feedback, and pairwise rankings are all required [elicitation A2]. None can be derived from FOLIO's output form. — _Sources: Q80, Q153, DATASET-D13, DATASET-D14, DATASET-D18_
- **OF-2**: Not applicable — deployment is text-based; speech output not required in current scope.
- **OF-3**: Not applicable in the conventional sense — target users are literate US high school students.
- **OF-4**: Form mismatches are fundamental: benchmark performance metrics (accuracy, SynV, ExcAcc) are structurally uninformative for assessing whether a model can produce multi-dimensional argument scores, coaching rationales, or pairwise comparisons. The translation metric is itself flagged as insufficient by the authors [Q77]. — _Sources: Q73, Q76, Q77, WEB-26, WEB-28_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q80] 'We use accuracy for evaluating logical reasoning performance.' (p.6)
- [Q73] 'Two metrics are adopted to evaluate NL-FOL translation to capture different aspects of the generation results: 1). Syntactic validity (SynV).' (p.6)
- [Q76] 'We define the accuracy of the output labels as the execution accuracy.' (p.6)
- [Q77] 'We leave for future work the design of a more reliable metric of NL-FOL translation.' (p.6)
- [Q153] 'Proving a story requires three steps... Finally, the theorem prover outputs whether the conclusions are True / False / Unknown' (p.14)

*Web sources:*
- [WEB-28] DebateBench evaluates speech-level scoring and ranking — confirms multi-output debate benchmarks are feasible but FOLIO does not match
- [WEB-26] CompAQA argues for combined pairwise classification and ranking — the kind of output form the deployment requires and FOLIO lacks

*Dataset analysis:*
- DATASET-D13: Six-premise reasoning chain collapses to single 'True' label with no sub-scores or rationale
- DATASET-D14: Complex multi-step deduction produces single categorical label
- DATASET-D18: Multiple conclusions scored independently — no pairwise comparison structure
- DATASET-D19: Negation/disjunction complexity still produces single binary-equivalent label
- DATASET-D21: Machine-verified label with no qualitative feedback dimension

</details>

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** FOLIO's taxonomy covers only formal deductive entailment and NL-FOL translation; the deployment requires evidentiary, value-laden, rhetorical, and debate-structural argument categories.

**Recommendation:** Construct a debate-specific argument-type taxonomy aligned to NSDA formats (Policy: DA/CP/T/K; LD: V/C framework, plans, kritiks, theory; PF: contention/weighing; Congressional: legislative advocacy/oratory). Use FOLIO only as a narrow sub-test for the deductive-validity component of the logical-structure sub-score, not as a primary evaluation.

### Input Content ⚠

**Gap:** FOLIO content deliberately excludes normative contestation, evidentiary disputes, and value-laden claims — the highest-weight content types for the deployment.

**Recommendation:** Supplement with content drawn from OpenDebateEvidence [WEB-22] and DebateSum [WEB-21], which provide actual US competitive debate evidence with citation/author/recency metadata. Curate format-specific test sets covering current NSDA resolutions [WEB-18] across Policy, LD, PF, and Congressional, including value-laden LD topics and empirically contested PF topics.

### Input Content ⚠

**Gap:** NSDA evidence-ethics rules and AI-generated content policies are deployment-critical but flagged [NEEDS VERIFICATION] in the regional context; current NSDA rulebook URLs were not retrieved.

**Recommendation:** Before deployment, retrieve current NSDA evidence-ethics rules and any state-level AI policies (e.g., Ohio SDA policy [WEB-30]). Build evidence-quality scoring criteria to align with NSDA standards on cutting, citing, and contextualizing evidence, and include explicit detection of AI-generated content per state-level prohibitions.

### Output Ontology ⚠

**Gap:** FOLIO's True/False/Unknown label space cannot represent the deployment's multi-dimensional sub-scores, qualitative feedback, pairwise rankings, or format/circuit-conditioned norms.

**Recommendation:** Design a four-sub-score rubric (evidence, logic, relevance, persuasion) plus pairwise comparative output, with quality bands conditioned on format (Policy/LD/PF/Congressional) and circuit (lay/national). Draw structural templates from DebateBench [WEB-28] and CompAQA [WEB-26]. Validate the taxonomy with NSDA coaches and TOC-circuit judges before deployment.

### Output Content ⚠

**Gap:** FOLIO labels are theorem-prover outputs from CS/FOL-trained annotators; deployment correctness is defined by NSDA judges, TOC paradigms, and coaching rubrics — a categorically different community.

**Recommendation:** Recruit a stratified panel of debate-community annotators (NSDA-credentialed judges, active coaches, recent national-circuit competitors) to produce ground-truth scores on the deployment-specific rubric. Stratify by format and by lay vs. tech circuit. Use paradigm metadata from Tabroom to surface circuit-conditioned norms. Measure and report inter-rater agreement; expect lower kappa than FOLIO (consistent with [WEB-26]) and design aggregation to preserve circuit-level signal rather than averaging it away.

### Output Form ⚠

**Gap:** FOLIO produces a single categorical label per example; the deployment requires multi-dimensional scores, free-text coaching rationales, and pairwise comparison outputs.

**Recommendation:** Design the evaluation harness to require structured multi-score output plus a free-text rationale per sub-score, plus a separate pairwise comparison subtask. Evaluate rationale quality with both automated metrics (faithfulness, citation correctness) and judge-panel review. FOLIO accuracy can be used only as an ancillary diagnostic for deductive-validity behavior, not as a deployment KPI.

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
| Q48 | 4 | input_content | "Toward these objectives, we manually screened all stories and found that 39.2% of the stories suffer from at least one of these issues. We implemented a detailed protocol to rewrite these stories." |
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
| Q101 | 8 | output_ontology | "FOLIO's unique complexity reveals that current LMs are limited in their ability to extrapolate to longer and more complex reasoning chains, and suggests an avenue for further study." |
| Q102 | 8 | output_form | "As shown in Table 6, in logical reasoning, GPT-3.5 and GPT-4 achieve substantially lower results on HybLogic than on WikiLogic and the result is slightly higher than chance." |
| Q103 | 8 | input_content | "We hypothesize that this is because HybLogic has high logical complexity that the SoTA LLMs like GPT-4 cannot solve yet while WikiLogic examples require shorter reasoning chains which the model is already capable of solving." |
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
| Q139 | 13 | output_ontology | "Following (Russell and Norvig, 2010), we consider temporal logic and modal logic as special-purpose logics." |
| Q140 | 13 | output_ontology | "Consequently, they are beyond the scope of the definition of first-order logic used in our dataset." |
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
| Q160 | 15 | input_form | "This indicates that the ordering of premises in FOLIO examples does not yield significant information about the label, and thus models will not be able to use the premise ordering as a strong heuristic or statistical feature for its predictions." |
| Q161 | 15 | input_form | "FOL formulas have a clearer and more straightforward logical structure than NL sentences." |
| Q162 | 15 | output_form | "As shown in Table 11, the performance slightly increases in the NL+FOL setting for GPT-4 while GPT-3.5 performs worse in both the NL+FOL and the FOL-only settings." |
| Q163 | 15 | output_form | "FOL always serves as additional useful information for GPT-4, but not for GPT-3.5 regardless of whether FOL is concatenated with NL." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://en.wikipedia.org/wiki/National_Speech_and_Debate_Association |
| WEB-2 | https://www.speechanddebate.org/media/ |
| WEB-3 | https://en.wikipedia.org/wiki/Structure_of_policy_debate |
| WEB-4 | https://debateus.org/the-basic-structure-of-policy-debate-3/ |
| WEB-5 | https://www.nsdebatecamp.com/lincoln-douglas/debate-format |
| WEB-6 | https://debateexperts.com/mastering-lincoln-douglas-debate-format/ |
| WEB-7 | https://en.wikipedia.org/wiki/Public_forum_debate |
| WEB-8 | https://ci.uky.edu/debate/toc |
| WEB-9 | https://ci.uky.edu/debate/toc/bids/bid-tournaments |
| WEB-10 | https://en.wikipedia.org/wiki/Tournament_of_Champions_(debate) |
| WEB-11 | https://policydebatecentral.com/2024-25-policy-toc-bid-tournaments-by-state/ |
| WEB-12 | https://www.aralia.com/helpful-information/guide-to-the-nsda-nationals/ |
| WEB-13 | https://www.cdadebate.com/blog/how-to-qualify-to-the-tournament-of-champions-as-independents |
| WEB-14 | https://www.nsdebatecamp.com/glossary/tournament-of-champions |
| WEB-15 | https://www.mcdermottlaw.com/insights/edtech-and-privacy-navigating-a-shifting-regulatory-landscape/ |
| WEB-16 | https://studentdpa.com/blog/understanding-ferpa-coppa-state-privacy-laws-03202025 |
| WEB-17 | https://www.hireplicity.com/blog/ferpa-coppa-soc2-edtech-compliance-guide |
| WEB-18 | https://www.speechanddebate.org/topics/ |
| WEB-19 | https://debateus.org/ |
| WEB-20 | https://www.tabroom.com/index/tourn/index.mhtml?webpage_id=36055&tourn_id=36375 |
| WEB-21 | https://www.semanticscholar.org/paper/DebateSum:-A-large-scale-argument-mining-and-Roush-Balaji/d27b3096c0707f42b068fc9b3b47ce87560cbd56 |
| WEB-22 | https://arxiv.org/abs/2406.14657 |
| WEB-23 | https://neurips.cc/virtual/2024/poster/97854 |
| WEB-24 | https://research.ibm.com/blog/project-debater-api |
| WEB-25 | https://neurohive.io/en/datasets/more-than-10-nlp-datasets-available-from-ibm-s-project-debater/ |
| WEB-26 | https://www.mdpi.com/2079-9292/13/20/4088 |
| WEB-27 | https://arxiv.org/html/2406.13905 |
| WEB-28 | https://arxiv.org/pdf/2502.06279 |
| WEB-29 | https://arxiv.org/html/2604.17366v1 |
| WEB-30 | https://sites.google.com/theosda.org/theosda/resources/debate |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (config: default)
**Analysis date:** 2025-01-31
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | FOLIO | Ex. 1 (story_id=271) | True | "No plants are fungi. Mushrooms are fungi. / No plants are mushrooms." | Simple two-premise syllogism; purely formal deductive structure with no evidentiary content | IO |
| D2 | FOLIO | Ex. 28 (story_id=252) | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. … There is an embargo on Russian foreign trade goods." | Macro-economics scenario; premises stated as given facts, not cited evidence requiring credibility assessment | IC |
| D3 | FOLIO | Ex. 43 (story_id=393) | True | "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning." | Story uses "inductive reasoning" as a named category but treats it deductively — no actual inductive inference is performed | IO |
| D4 | FOLIO | Ex. 6 (story_id=423) | Uncertain | "Everyone at the business conference is either an investor or an entrepreneur. … Ho is at the business conference and prefers state ownership of the means of production." | Normative terms (planned economy, state ownership, ardent communist) appear only as predicate labels; no value judgment is required or possible | IC |
| D5 | FOLIO | Ex. 22 (story_id=475) | Uncertain | "Everyone who is entitled to national social insurance coverage can have their medical bills partially covered. … Either Mei is a North Korean and can have medical bills partially covered, or neither is true." | Policy-adjacent content framed as pure deductive entailment; no contested empirical or value claim is assessed | IC |
| D6 | FOLIO | Ex. 2 (story_id=376) | Uncertain | "Mike works in this tech company. If Mike is not a person who wears the same flannel shirts every day, has very high energy, and is impulsive, then Mike either is very consistent and enjoys sticking to his regular routines or does not like surprises." | Multi-premise WikiLogic scenario with 7 premises; reasoning depth is high but entirely deductive | IO |
| D7 | FOLIO | Ex. 3 (story_id=180) | Uncertain | "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac. Sam is using a Mac." | Technical CS scenario with exclusive disjunction chain; no debate-relevant argument structure | IO |
| D8 | FOLIO | Ex. 8 (story_id=482) | Uncertain | "Harry, who lives in Potterville either yells or flies. Potter, who lives in Potterville, is a wizard and flies." | Fictional fantasy premise set; content has no overlap with competitive debate argument types | IC |
| D9 | FOLIO | Ex. 2 (story_id=376) | Uncertain | "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" | FOL annotation is theorem-prover verified; labels are mechanically derived, not from human judgment of argument quality | OC |
| D10 | FOLIO | Ex. 46 (story_id=448) | Uncertain | "If someone is a seasoned software engineer interviewer at Google, then they know what breath-first-search is. … Jack is entitled to the right to life and liberty, has human rights, or knows about the first-in-first-out data structure." | Human rights framing used as deductive predicate; no normative assessment required or possible | OO |
| D11 | FOLIO | Ex. 11 (story_id=486) | False | "Everything in Size Town is big or small. … The bird is in Size Town and it is not both heavy and still." | Fully abstract fictional scenario; label is True/False/Uncertain with no sub-dimensions | OO |
| D12 | FOLIO | Ex. 28 (story_id=252) | False | "∀x (Country(x) ∧ PossibleEffectiveMonetaryPolicy(x) → SuccessfulInflationControl(x) ∧ StongNationalCurrency(x))" | Ground truth derived from FOL inference engine, not from domain expert or debate-community judgment | OC |
| D13 | FOLIO | Ex. 16 (story_id=346) | True | "All professional athletes spend most of their time on sports. All Olympic gold medal winners are professional athletes. … If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." | Six-premise chain requiring multi-step deductive inference; output is single True/False/Unknown label | OF |
| D14 | FOLIO | Ex. 57 (story_id=362) | False | "People who like financial risks invest in the public stock market regularly or enjoy gambling regularly. … Matt does not invest in the public stock market regularly. Matt likes financial risks." | Complex multi-step deduction; conclusion collapses to single categorical label with no sub-scores or rationale | OF |
| D15 | FOLIO | Ex. 13 (story_id=395) | False | "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable. … ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." | Real consumer product used as topic seed; content is factual/commercial, not argumentative or evidentiary | IC |
| D16 | FOLIO | Ex. 34 (story_id=377) | True | "All orphan planets are rogue planets. If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." | Scientific real-world entity used as topic; premises are stated as fixed facts, not contested empirical claims | IC |
| D17 | FOLIO | Ex. 23 (story_id=108) | Uncertain | "The world's only major large passenger aircraft manufacturers are Boeing and Airbus. … There exists a SpaceX commercial aircraft." | Factual world knowledge embedded as premise; no evidence citation, credibility assessment, or warrant evaluation | IC |
| D18 | FOLIO | Ex. 4 (story_id=408) | False | "No trick-shot artist in Yale's varsity team struggles with half court shots. … Jack is on Yale's varsity team, and he is either a trick-shot artist or he successfully shoots a high percentage of 3-pointers." | Same story_id generates multiple conclusions (examples 1134, 1141, 1140) — confirms single-label per conclusion structure | OF |
| D19 | FOLIO | Ex. 52 (story_id=337) | True | "No athletes never exercise. … Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." | Negation/exclusive-disjunction complexity; output remains a single binary-equivalent label | OF |
| D20 | FOLIO | Ex. 21 (story_id=381) | False | "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing. … If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up in old-fashioned and historical period clothing." | Long six-premise chain typical of WikiLogic track; no rhetorical, persuasive, or debate-structural elements | IO |
| D21 | FOLIO | Ex. 36 (story_id=422) | True | "Customers in James' family subscribe to AMC A-List or HBO service. … Lily is in James' family; she watches TV series in cinemas." | Everyday consumer scenario; label is machine-verified True — no qualitative feedback dimension possible | OF |
| D22 | FOLIO | Ex. 55 (story_id=477) | False | "If a social media application is addictive, then it is not ideal for preteens. TikTok is a social media application, and it is not ideal for preteens." | Contemporary tech topic; "addictive" treated as a logical predicate, not a value-laden or contested empirical claim | IC |
| D23 | FOLIO | Ex. 56 (story_id=27) | Uncertain | "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin. … Kowloon District is in Hong Kong." | Geographic factual premises; conclusion about a completely different city is Uncertain — confirms open-world assumption | OO |
| D24 | FOLIO | Ex. 38 (story_id=425) | False | "Everyone working at Meta has a high income. … James has a car or works at Meta." | Contemporary workplace scenario; premises stated as definitional universals, not empirically disputed claims | IC |
| D25 | FOLIO | Ex. 43 (story_id=393) | True | "∀x (MajorArgumentForm(x) → (InductiveReasoning(x) ⊕ DeductiveReasoning(x))" | Inductive reasoning is modeled as a named entity/predicate; the reasoning task itself remains purely deductive | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Text-Only English Input with No Modality or Script Mismatch
- **Dimension(s):** IF
- **Observation:** All 57 sampled examples are text-based, written in standard American English with grammatically natural sentences. No audio, images, non-Latin scripts, or multilingual content appear anywhere in the sample.
- **Deployment relevance:** The deployment platform processes written cases and transcripts in English text. There is zero signal-distribution mismatch at the input form level between FOLIO and the deployment context; this dimension does not introduce construct-irrelevant variance.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO, train, True): "No plants are fungi. Mushrooms are fungi." — Grammatically natural English, text-only, no modality concerns.
  - [D8] Example 8 (FOLIO, train, Uncertain): "Harry, who lives in Potterville either yells or flies." — Complex sentence structure rendered cleanly in standard English prose.

#### Strength 2: High Logical Complexity and Multi-Step Inference Chains
- **Dimension(s):** IO
- **Observation:** Multiple sampled examples require chaining five or more premises through conjunction, disjunction, implication, and universal/existential quantifiers. Examples 2, 16, 20, 21, 36, 43, 46, and 57 all involve four to seven distinct premises with multi-step inference requirements. This is the highest-fidelity logical-validity signal available in any natural-language benchmark.
- **Deployment relevance:** While insufficient on its own for the deployment's needs, one of the four required sub-scores (logical structure and warrant quality) does include inferential validity as a component. FOLIO provides a rigorous upper bound on that sub-dimension — if a model scores well here, its deductive validity component is demonstrably strong.
- **Datapoint citations:**
  - [D6] Example 2 (FOLIO, train, Uncertain): "Mike works in this tech company. If Mike is not a person who wears the same flannel shirts every day, has very high energy, and is impulsive, then Mike either is very consistent and enjoys sticking to his regular routines or does not like surprises." — 7-premise scenario requiring multi-step deductive inference.
  - [D20] Example 21 (FOLIO, train, False): "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing. … If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up in old-fashioned and historical period clothing." — 6-premise WikiLogic chain.
  - [D14] Example 57 (FOLIO, train, False): "People who like financial risks invest in the public stock market regularly or enjoy gambling regularly. … Matt does not invest in the public stock market regularly. Matt likes financial risks." — Multi-step deductive chain with complex disjunction.

#### Strength 3: Mechanically Verified, Unambiguous Ground-Truth Labels
- **Dimension(s):** OC
- **Observation:** Every label in the dataset is verified by an FOL inference engine, not by human subjective judgment. Within the narrow scope of formal deductive entailment, labels are objectively correct and consistent across all examples reviewed.
- **Deployment relevance:** For the specific sub-task of checking whether a stated logical argument form is internally consistent (a sub-component of "logical structure" sub-score), FOLIO provides a reliable, reproducible signal. There is no annotator disagreement or subjective variance within its defined scope.
- **Datapoint citations:**
  - [D9] Example 2 (FOLIO, train, Uncertain): "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" — FOL formula mechanically derived and verified; label is theorem-prover output, not human judgment.
  - [D12] Example 28 (FOLIO, train, False): "∀x (Country(x) ∧ PossibleEffectiveMonetaryPolicy(x) → SuccessfulInflationControl(x) ∧ StongNationalCurrency(x))" — Ground truth is FOL inference engine output, internally consistent and reproducible.

#### Strength 4: Diverse Topic Coverage Across WikiLogic Stories
- **Dimension(s):** IC
- **Observation:** The WikiLogic track (which dominates the sample) draws on a wide range of real-world topics: geography (Croton River, Guilin districts), science (mammals, planets, biology), economics (Russian trade embargo), technology (Meta employees, TikTok), films (EndGame, Adventures of Rusty), and consumer products (Rouge Dior lipstick, watch types). This topical breadth means the benchmark does not test a narrow domain vocabulary.
- **Deployment relevance:** While topical variety does not substitute for debate-specific content, it confirms that FOLIO does not introduce systematic domain-specific knowledge bias (e.g., only testing science or history). For any sub-component testing of domain-neutral logical validity, this breadth is a minor positive.
- **Datapoint citations:**
  - [D16] Example 34 (FOLIO, train, True): "All orphan planets are rogue planets. If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." — Astronomy topic seed.
  - [D2] Example 28 (FOLIO, train, False): "There is an embargo on Russian foreign trade goods." — Economic/geopolitical topic seed.
  - [D15] Example 13 (FOLIO, train, False): "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable." — Consumer product topic seed.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Zero Coverage of Inductive, Evidentiary, or Evidence-Quality Reasoning
- **Dimension(s):** IO, IC
- **Observation:** Every single one of the 57 sampled examples is a closed-world deductive entailment problem: premises are stated as definitional universals or given facts, conclusions are derived by formal inference rules, and no example contains cited sources, empirical uncertainty, evidence recency, or warrant credibility. The word "evidence" does not appear in any premise or conclusion. No example models contested empirical claims.
- **Deployment relevance:** The deployment user explicitly identified evidence quality (source credibility, recency, miscontextualization, cherry-picking) as the *highest-weight* sub-dimension. FOLIO contains literally zero content of this type. An LLM that scores at ceiling on FOLIO may still be completely unable to assess whether a card is outdated, miscut, or from a non-credible source. The benchmark provides no signal whatsoever for this top-priority deployment requirement.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO, train, True): "No plants are fungi. Mushrooms are fungi." — Premises are stated definitional facts with no source, citation, or credibility dimension.
  - [D2] Example 28 (FOLIO, train, False): "There is an embargo on Russian foreign trade goods." — An empirically contested geopolitical claim is stated as a given logical axiom, stripping all evidence quality assessment from the task.
  - [D17] Example 23 (FOLIO, train, Uncertain): "The world's only major large passenger aircraft manufacturers are Boeing and Airbus. … There exists a SpaceX commercial aircraft." — Factual claims are encoded as fixed premises; no warrant or source credibility evaluation is possible or required.

#### Concern 2: Total Absence of Debate-Specific Argument Structures
- **Dimension(s):** IO
- **Observation:** None of the 57 sampled examples contains any structure resembling a disadvantage (DA), counterplan (CP), kritik (K), topicality shell (T), theory argument, burden-of-proof claim, or impact calculus. The argument structures present are exclusively syllogistic/predicate-logic chains. The tokens "disadvantage," "counterplan," "kritik," "topicality," "solvency," "impact," "turn," "burden," "framework," "value," "criterion" do not appear in any premise or conclusion in the sample.
- **Deployment relevance:** The deployment user identified DAs, CPs, kritiks, and burden-shifting as "first-class argument types" required by the system. FOLIO's ontology has zero overlap with these structures. A model evaluated on FOLIO cannot demonstrate any capability for recognizing or scoring these debate-specific moves.
- **Datapoint citations:**
  - [D7] Example 3 (FOLIO, train, Uncertain): "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac." — Exclusively syllogistic structure; no debate argument structure present.
  - [D20] Example 21 (FOLIO, train, False): "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing." — Extended WikiLogic syllogism; no debate-structural elements.
  - [D3] Example 43 (FOLIO, train, True): "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning." — "Inductive reasoning" is used as a deductive predicate label, not as an actual inductive argument structure.

#### Concern 3: Output Space Categorically Mismatched to Deployment Requirements
- **Dimension(s):** OO, OF
- **Observation:** Every example produces exactly one of three outputs: True, False, or Uncertain. No example produces a sub-score breakdown, a qualitative rationale, a pairwise comparison, or any circuit/format-conditioned evaluation. The schema confirms this: the only label column is a single string field. Multiple conclusions from the same story (e.g., story_id=408 generates examples 1134, 1140, 1141) each receive their own independent True/False/Uncertain label with no cross-conclusion comparison.
- **Deployment relevance:** The deployment requires: (a) separate sub-scores across logic, evidence, relevance, and persuasiveness; (b) qualitative coaching feedback; (c) pairwise comparison for rebuttal practice; and (d) format/circuit-conditioned scoring. FOLIO's output space cannot approximate any of these. Benchmark performance metrics (accuracy over True/False/Unknown) are structurally uninformative for assessing whether a model can provide coaching feedback or rank arguments comparatively.
- **Datapoint citations:**
  - [D13] Example 16 (FOLIO, train, True): "All professional athletes spend most of their time on sports. … If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." — Six-premise reasoning chain collapses to single label "True"; no sub-scores, no rationale.
  - [D18] Example 4 / story_id=408 (FOLIO, train, multiple): "No trick-shot artist in Yale's varsity team struggles with half court shots." — Same premises generate three separate conclusions (examples 1134, 1140, 1141) each with independent True/False/Uncertain labels; no head-to-head comparative ranking structure exists.
  - [D21] Example 36 (FOLIO, train, True): Label is machine-verified "True" — no coaching explanation, no weakness identification, no qualitative feedback dimension.

#### Concern 4: Annotator Population Completely Mismatched to Deployment Quality Standards
- **Dimension(s):** OC
- **Observation:** All labels are derived from a formal FOL inference engine, not from human judges with debate expertise. The human annotators are CS students with formal FOL training. The deployment's correctness standard is defined by NSDA norms, TOC circuit paradigms, and coaching staff rubrics — a community with entirely different domain knowledge and quality intuitions.
- **Deployment relevance:** Whether an argument is "strong" in competitive debate is a community-norm judgment that varies by circuit and format. FOLIO's theorem-prover labels have no relationship to these norms. A label of "True" on a FOLIO example says nothing about whether a debate judge would find the corresponding argument persuasive, well-warranted, or topically responsive.
- **Datapoint citations:**
  - [D9] Example 2 (FOLIO, train, Uncertain): "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" — Label is theorem-prover output; a debate judge paradigm plays no role in determining this label.
  - [D12] Example 28 (FOLIO, train, False): Ground truth "False" is derived mechanically from FOL inference over stated premises about Russia's monetary policy; no debate-community judgment is involved or approximated.

#### Concern 5: No Value-Laden or Normatively Contested Content
- **Dimension(s):** IC
- **Observation:** As explicitly documented in the benchmark design and confirmed across all 57 examples, FOLIO deliberately avoids normatively contested content. Even examples that name politically adjacent entities (state ownership of means of production, North Korean nationals, Russian trade embargoes) use these as deductive predicate labels requiring no value judgment. The content is cleansed of the very quality — genuine normative contestation — that defines LD and Congressional debate.
- **Deployment relevance:** LD and Congressional debate center on value claims where reasonable people disagree (e.g., "civil liberties outweigh national security"). The system must score argument structure and warrant quality for these claims without taking sides. FOLIO's total avoidance of such content means it cannot measure any aspect of a model's capacity to assess value-laden arguments without injecting normative bias.
- **Datapoint citations:**
  - [D4] Example 6 (FOLIO, train, Uncertain): "Everyone at the business conference is either an investor or an entrepreneur. … Ho is at the business conference and prefers state ownership of the means of production." — "Planned economy" and "state ownership" appear as logical predicates, not contested value claims; no normative assessment is required.
  - [D5] Example 22 (FOLIO, train, Uncertain): "Everyone who is entitled to national social insurance coverage can have their medical bills partially covered." — Social policy claim treated as a definitional universal; no value dispute is present or assessed.
  - [D10] Example 46 (FOLIO, train, Uncertain): "Every person who has human rights is entitled to the right to life and liberty. … Jack is entitled to the right to life and liberty, has human rights, or knows about the first-in-first-out data structure." — Human rights framing is purely a logical predicate; no normative weight is assigned or evaluated.

---

#### MAJOR

#### Concern 6: No Pairwise or Comparative Argument Structure
- **Dimension(s):** OO, OF
- **Observation:** All 57 examples evaluate a single conclusion against a fixed premise set in isolation. No example involves two competing arguments, a rebuttal structure, or a head-to-head comparison. Multiple conclusions from the same story (story_id=408: examples 1134, 1140, 1141; story_id=482: examples 1406, 1407, 1408) are scored independently, not comparatively.
- **Deployment relevance:** The deployment explicitly requires pairwise argument comparison for rebuttal practice. This is a structural requirement with no analog in FOLIO's design. There is no way to derive pairwise rankings or contrastive strength assessments from FOLIO's True/False/Uncertain labels.
- **Datapoint citations:**
  - [D18] Example 4 / story_id=408 (FOLIO, train, False and Uncertain): Three separate conclusions from the same premise set receive independent labels (False, Uncertain, False); no comparative ranking between these conclusions is provided or evaluable.
  - [D11] Example 11 (FOLIO, train, False): "The bird is in Size Town and it is not both heavy and still." — Single isolated conclusion scored in isolation; no opposing argument structure present.

#### Concern 7: Register Mismatch — Formal Logical Universals vs. Competitive Debate Discourse
- **Dimension(s):** IC, IF
- **Observation:** FOLIO premises are written as formal logical universals ("All X are Y," "No X are Z," "If X then Y") with named constants (Mike, Amy, Jack, Ho, Mei). This register is characteristic of logic textbooks. Competitive debate arguments — even structurally similar ones — use hedged empirical language ("Studies show that…," "According to [author], the [mechanism] causes…," "Extend the [impact] — it outweighs because…"). The surface form difference is substantial.
- **Deployment relevance:** A model fine-tuned on or evaluated by FOLIO learns to process clean formal-universal sentence structures that differ significantly from the hedged, warrant-heavy, evidence-citing register of actual debate arguments. Even the logical structure sub-dimension of the deployment involves discourse forms not represented in FOLIO.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO, train, True): "No plants are fungi. Mushrooms are fungi." — Formal universal statements characteristic of logic textbooks, not debate speech transcripts.
  - [D24] Example 38 (FOLIO, train, False): "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination." — Clean formal universals; no hedging, no citation, no warrant-evidence structure typical of competitive debate.
  - [D22] Example 55 (FOLIO, train, False): "If a social media application is addictive, then it is not ideal for preteens. TikTok is a social media application, and it is not ideal for preteens." — Contemporary content but rendered as definitional logical axioms, not contested empirical claims with evidence.

---

#### MINOR

#### Concern 8: Small Dataset Size Limits Statistical Reliability for Sub-Population Analysis
- **Dimension(s):** IF
- **Observation:** The full dataset contains only 1,204 examples (train + validation; test set is withheld on HuggingFace). Even if the benchmark were otherwise appropriate for the deployment, the small size makes it difficult to analyze performance by topic domain, reasoning depth, or label distribution with statistical confidence.
- **Deployment relevance:** If used as a proxy for any sub-component of deployment scoring, the small dataset limits the ability to distinguish model performance on harder vs. easier reasoning chains or to detect systematic failure modes across topic categories.
- **Datapoint citations:**
  - [D13] Example 16 / [D1] Example 1: Both are training examples from a dataset totaling ~1,000 train examples — insufficient to disaggregate by the multiple format × circuit × argument-type combinations required by the deployment.

#### Concern 9: Potential Pretraining Data Contamination for WikiLogic Examples
- **Dimension(s):** IC
- **Observation:** WikiLogic stories are based on Wikipedia article topics and may share surface patterns with LLM pretraining corpora (as acknowledged in the benchmark documentation). Examples like Ex. 15 (Oxford Circus, John Nash), Ex. 17 (Michael O'Donnell), and Ex. 27 (Bobby Flynn, Australian Idol) use real named entities drawn from Wikipedia.
- **Deployment relevance:** If an LLM is being evaluated for deployment on this benchmark, strong performance on WikiLogic examples may reflect memorized factual patterns rather than genuine reasoning capability — making benchmark performance an overestimate of the model's actual logical reasoning ability on novel debate arguments.
- **Datapoint citations:**
  - [D15] Example 15 (FOLIO, train, Uncertain): "Oxford Circus is a road junction connecting Oxford Street and Regent Street. … John Nash designed Oxford Circus." — Named real-world entities likely present in Wikipedia-derived pretraining data.
  - [D8] Example 27 (FOLIO, train, Uncertain): "Bobby Flynn finished 7th while competing on Australian Idol. … Bobby Flynn was born in Queensland." — Specific biographical facts from Wikipedia; potential contamination risk.

---

### Content Coverage Summary

The 57 sampled examples represent FOLIO's two collection tracks faithfully. **WikiLogic examples** (the majority) cover a diverse range of real-world topics seeded from Wikipedia: geography (Guilin districts, Croton River, New Haven/Manhattan buildings), scientific entities (rogue planets, mammalian egg-laying, sea eels), consumer products (Rouge Dior lipstick, Moonwatch), technology companies (Meta, Google, TikTok, tech company with "Mike"), sports (Yale varsity basketball, Olympic athletes), media (Harry Potter, films, Bobby Flynn), and geopolitical scenarios (Russia embargo, Franco-China conference). **HybLogic examples** (the minority) use more abstract or archetypal scenarios with named constants: a fictional town "Potterville" with wizards, "Size Town" with abstract properties, and syllogism-heavy chains about cooking talent or financial risk.

In every case, the content is structured as a closed-world logical puzzle: premises are stated as definitional universals or given facts, and the task is to determine whether a conclusion follows by formal deduction. No example contains cited evidence, disputed empirical claims, normative arguments, rhetorical moves, or debate-specific structural elements. The register is consistently that of a logic textbook — formal universal statements, named constants, and clean implications — rather than the hedged, evidence-citing, warrant-heavy language of competitive debate.

The label distribution in the sample shows roughly equal representation of True (approximately 30%), False (approximately 30%), and Uncertain (approximately 40%), consistent with the documented test set distribution (87/78/61). All labels are mechanically verified by an FOL inference engine.

---

### Limitations

1. **Test split not available on HuggingFace**: The HF repository exposes only train (1,001 examples) and validation (203 examples). The test split (226 examples) is withheld. All analysis is based on training examples; any systematic differences in the test split cannot be assessed from this sample.

2. **Sample size (57/1,001 train)**: The reviewed sample is 5.7% of the training split. While the logical structure and content register are highly consistent across all examples reviewed, rare topic categories or unusual reasoning patterns in the other 94% cannot be ruled out from this sample alone.

3. **No FOL formula evaluation**: The `premises-FOL` and `conclusion-FOL` columns contain parallel formal logic annotations that were reviewed visually but not formally executed against an inference engine. Annotation errors in the FOL (noted as a known quality issue in the benchmark documentation) cannot be detected from the natural language alone.

4. **No audio, image, or speech-transcript examples**: The deployment involves potentially processing speech transcripts from debate rounds. Whether the clean prose register of FOLIO examples generalizes to ASR-transcribed speech artifacts (disfluencies, mid-sentence corrections, spread delivery) cannot be assessed from this dataset.

5. **HybLogic vs. WikiLogic proportion in sample**: The sample appears heavily WikiLogic-weighted (consistent with the 304 vs. 183 story split documented in the benchmark). HybLogic patterns — which tend to be more structurally regular and potentially more learnable by fine-tuned models — may be underrepresented in the reviewed examples.

