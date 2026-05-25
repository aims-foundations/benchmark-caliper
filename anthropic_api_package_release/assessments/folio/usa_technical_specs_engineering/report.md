## Deployment Context

We are a US engineering firm building a tool that identifies logical inconsistencies across technical specification documents for American systems engineers. The tool analyzes structured requirements and design documents to find contradictions — for example, requirements that contradict each other or conditions that can never be jointly satisfied. We need to evaluate the LLM's ability to perform logical analysis over semi-structured technical prose.

# Validity Analysis: folio
**Target context:** US Defense and High-Reliability Systems Engineers
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 3 | Moderate gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ✓ | 2 | Significant gaps | high |
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

FOLIO is structurally misaligned with the US Defense and High-Reliability Systems Engineering deployment on five of the six validity dimensions. The benchmark probes closed-world, fully-explicit, domain-neutral, single-context logical reasoning, with bare True/False/Unknown classification scored by accuracy. The deployment requires open-world, implicit-premise, domain-grounded, cross-document contradiction detection with natural-language explanations, confidence grades, and resolution paths for uncertain findings. Input Ontology, Input Content, Output Ontology, and Output Form score 1 (major violations); Output Content scores 2 (labels correct for the closed-world construct but reflect FOL-provability rather than engineering judgment, plus tangible annotation errors observable in sample); only Input Form scores 3, since both benchmark and deployment are text-only English even though length and register differ substantially. FOLIO accuracy should be treated as a weak lower-bound proxy for general logical-reasoning capability — useful for filtering models that fail at multi-hop closed-world inference — but cannot serve as a predictive measure of deployment performance on any of the deployment's high-priority dimensions (IO, IC, OO, OF). The regulatory environment (CMMC, ITAR, CUI) adds an orthogonal deployment constraint that further restricts which models can be evaluated in compliant infrastructure.

## Practical Guidance

### What This Benchmark Measures

FOLIO measures a model's ability to perform closed-world, multi-hop deductive inference over fully-explicit narrative premises in English, classifying conclusions as True/False/Unknown by FOL semantics. It exercises broad logical-operator coverage (negation, conjunctions, disjunctions, implication, quantifiers, equality) and reasoning depths up to 7 hops. For the deployment, FOLIO can serve as a baseline filter on classical-logic competence — informative for the crisp-contradiction sub-task (explicit numeric conflicts), where Input Ontology's multi-hop closed-world chains are a useful lower-bound proxy.

### Construct Depth

FOLIO probes its target construct (closed-world FOL reasoning) deeply: 1,430 inference-engine-verified examples, balanced True/False/Unknown distribution, 5+ hop reasoning in 28.7% of examples, broad AST diversity, and rigorous annotation QC. However, this depth does not extend to the deployment's high-priority constructs. Implicit-premise inference (IO-HIGH), latent domain contradictions (IC-HIGH), structured explanation + confidence (OO-HIGH), and cross-document reasoning (OF-HIGH) are not probed at any depth — they are absent from the benchmark's task taxonomy, content register, output schema, and evaluation apparatus. A model could achieve high FOLIO accuracy while failing completely on the deployment's primary use case.

### What Else You Need

Substantial supplementation is required across IO, IC, OC, and OF. For implicit-premise document NLI (closest legal-domain analog): ContractNLI [WEB-10] and LawngNLI [WEB-11]. For multi-document long-context reasoning (OF gap): MDBench [WEB-16], LongBench v2 [WEB-17], and PRELUDE [WEB-18]. For explanation faithfulness (OO/OF gap): the FaithLM framework [WEB-19] and contradiction-explanation literature [WEB-21]. None of these proxies covers MIL-STD/IEEE requirements-language reasoning [WEB-13, WEB-22] — that gap can only be filled by a purpose-built test suite of real or synthetic defense specification contradictions, reviewed by practicing systems engineers, ideally constructed to exercise latent thermal/timing/bandwidth contradiction patterns. Human-expert validation is methodologically necessary rather than optional, given that LLM explanation faithfulness measurement is itself an unresolved research problem [WEB-20, WEB-24].

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's input ontology is structurally opposite to the deployment's core challenge. The benchmark is explicitly built around closed-world, fully-explicit premise sets where models 'decide the correctness of conclusions given a world defined by the premises' [Q15], and it explicitly excludes temporal and modal logics as 'beyond the scope' [Q139, Q140]. The deployment's central task — recognizing latent conflicts where one or both relevant premises live implicitly in referenced MIL-STD/IEEE standards or shared engineering conventions — has no corresponding category in FOLIO's taxonomy. Dataset analysis confirms this without exception: every sampled example provides a complete self-contained premise set with no implicit-premise inference required [DATASET-D1, D3, D5]. The deliberate exclusion of temporal/modal logic is particularly damaging since timing and conditional state requirements are first-class concerns in engineering specs. Cross-document/multi-context reasoning, the deployment's primary use case per Q4 elicitation, is also absent from FOLIO's task structure.

**Strengths:**
- Operator coverage is broad — negation, conjunction, inclusive/exclusive disjunction, implication, universal and existential quantifiers, and equality are all represented [Q138, DATASET-D12, D15], which provides at least minimal exposure to the logical structures (biconditionals, disjunctive requirements) that appear in specs.
- Reasoning depth diversity is substantive: 28.7% of examples require 5+ hops [Q60], and the sample confirms multi-hop chains of 4–6 universal conditionals [DATASET-D13, D6], providing a lower-bound proxy for explicit-chain reasoning capability.
- Includes both supervised fine-tuning and few-shot prompting evaluation regimes [Q82, Q88], plus advanced CoT/self-consistency/ToT and logic-specialized methods [Q90, Q91], which span the prompting strategies a deployment would likely use.

**Checklist:**

- **IO-1**: Required deployment categories per elicitation include: implicit-premise inference from referenced standards (Q1 elicitation), latent contradiction detection requiring domain reasoning (Q2 elicitation), cross-document conflict tracing (Q4 elicitation), and confidence-graded uncertainty with resolution paths (Q3 elicitation, Q6 gap). None of these are represented in FOLIO's two-task ontology of NL reasoning and NL-FOL translation [Q63]. — _Sources: Q15, Q63, Q66_
- **IO-2**: FOLIO omits every high-priority deployment category. The benchmark defines closed-world reasoning over self-contained premises [Q15] and explicitly excludes temporal and modal logics [Q139, Q140] — directly relevant to timing and conditional-state requirements. Dataset sample confirms no example involves implicit-premise inference [DATASET-D1, D3, D5]. Confirmed external gap: no benchmark targets MIL-STD/IEEE implicit-premise reasoning [WEB-13 — space mission requirement verification paper notes 'benchmarking is difficult due to the lack of standardized datasets']. — _Sources: Q15, Q139, Q140, WEB-13, DATASET-D1, DATASET-D3, DATASET-D5_
- **IO-3**: The NL-FOL translation sub-task [Q67] and academic FOL-notation focus introduce categories not directly relevant to deployment, which targets natural-language explanation rather than FOL translation. Not fatal — accuracy on the NL reasoning sub-task can be reported in isolation — but consumes evaluation weight on a capability irrelevant to deployment value. — _Sources: Q63, Q67_
- **IO-4**: Category gaps harming content validity: (a) no open-world / implicit-premise category, (b) no cross-document reasoning category, (c) no temporal/modal logic category, (d) no actionable-uncertainty category (Unknown means formal undecidability [Q66], not 'what would resolve this'), (e) no domain-specific latent-contradiction category. Combined, these gaps represent construct underrepresentation of the deployment's primary tasks. — _Sources: Q15, Q66, Q139, Q140, WEB-10, WEB-13, DATASET-D21_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q15] 'We present a natural language reasoning dataset, FOLIO, with first-order logic reasoning problems which require the models to decide the correctness of conclusions given a world defined by the premises.' (p.1)
- [Q139] 'Following (Russell and Norvig, 2010), we consider temporal logic and modal logic as special-purpose logics.' (p.13)
- [Q140] 'Consequently, they are beyond the scope of the definition of first-order logic used in our dataset.' (p.13)
- [Q60] '28.7% of the examples need five or more depths of reasoning to infer the conclusions' (p.5)
- [Q63] 'We define two new tasks based on FOLIO, natural language reasoning with first-order logic and NL-FOL translation.' (p.6)
- [Q66] 'Given P and H, the goal is to determine the truth values of the conclusions: True, False or Unknown, based on FOL reasoning.' (p.6)
- [Q138] 'We include the following operators: negation ¬, conjunction ∧, disjunction ∨, implication →, universal quantifier ∀, existential quantifier ∃, equal =.' (p.13)

*Web sources:*
- [WEB-13] No standardized NLP benchmark exists for defense/aerospace requirements-language reasoning; space mission paper explicitly notes the gap
- [WEB-10] ContractNLI is the closest structural analog for implicit-premise document NLI, but in the legal domain rather than engineering

*Dataset analysis:*
- DATASET-D1: Two-premise closed-world syllogism with no external knowledge required — confirms structural pattern across sample
- DATASET-D3: Programming scenario with all constraints explicitly stated — no implicit premise from external standard
- DATASET-D5: Geopolitical facts restated as premises rather than assumed from world knowledge
- DATASET-D13: Four chained universal conditionals demonstrate multi-hop closed-world inference (deployment-relevant strength for crisp contradictions)
- DATASET-D21: Single 'event world' with all premises consolidated — confirms single-context structural unit

</details>

**Information gaps:**
- No correlation study between FOLIO accuracy and capability on implicit-premise or cross-document benchmarks (e.g., ContractNLI, MDBench).

**Requires expert verification:**
- Whether FOLIO's multi-hop chain coverage is a useful lower-bound proxy for engineering crisp-contradiction detection requires domain-expert validation against representative specs.

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's content is general-knowledge narrative prose drawn from Wikipedia seeds [Q34] and syllogism templates [Q42], with a vocabulary of 4,351 words [Q62] curated to avoid identity bias [Q47, Q127] and stay close to real-world facts [Q126]. Dataset analysis confirms zero engineering-domain content across the sampled 57 examples: topics span sports, consumer products, biology, film, pop culture, and policy [DATASET-D9, D10, D22, D23, D24], with no MIL-STD/IEEE vocabulary, no tolerance/timing/thermal/bandwidth content, and no requirements-language modal verbs ('shall'/'should'). This produces systematic construct-irrelevant variance relative to the deployment's highest-priority targets — latent contradictions in thermal budgets, timing margins, and bus bandwidth (elicitation Q2). Web search confirms no available benchmark targets this content register [WEB-13, WEB-22]. The WikiLogic contamination concern [Q104] further weakens the evidentiary value of FOLIO scores for novel technical content.

**Strengths:**
- Content is intentionally screened against identity bias [Q47, Q127], reducing one class of construct-irrelevant variance that could plausibly affect engineering-domain deployment.
- Logical complexity and AST diversity are genuine — 4,351-word vocabulary, 28.7% of examples requiring 5+ hops [Q60, Q62] — providing a substantively non-trivial logical-reasoning probe even if domain-irrelevant.
- Commonsense premises required for FOL reasoning are explicitly added as additional premises [Q55], demonstrating awareness of implicit-knowledge issues — though this is solved by elimination (making everything explicit) rather than by testing implicit-knowledge invocation, which is exactly what the deployment needs.

**Checklist:**

- **IC-1**: Deployment requires inputs in normalized requirements-language register with modal verbs ('shall', 'should'), standards identifiers (MIL-STD-461, IEEE 15288), tolerance expressions, and interface parameter conventions. FOLIO contains none of this register — every sample example is general-purpose narrative English [DATASET-D9, D10, D22]. — _Sources: DATASET-D9, DATASET-D10, DATASET-D22, WEB-22_
- **IC-2**: Cultural alignment is partial — content is English-language and US-acceptable [DATASET-D11, D22, D26], but 'cultural fit' to the engineering professional culture is essentially zero: no examples involve the standards-driven, traceability-focused register engineers work in. — _Sources: DATASET-D11, DATASET-D22, DATASET-D26_
- **IC-3**: Inputs require general Western/Anglophone cultural knowledge (TikTok, Meta, Yale, Hong Kong references — [DATASET-D11, D22, D26]). This is compatible with US deployment at the surface level, but irrelevant to engineering content. WikiLogic contamination [Q104] is a confound: LLMs may answer from pretraining rather than logical inference. — _Sources: Q104, DATASET-D24, DATASET-D26_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no evidence of recruiting systems engineers as annotators or reviewers; benchmark used CS/NLP/FOL experts [Q29, Q124, Q125], not aerospace/defense practitioners. Regional expert recruitment would be needed.
- **IC-5**: Content issues harming content validity: (a) zero engineering-domain examples [DATASET-D9, D10, D22], (b) no normalized requirements-language register, (c) no MIL-STD/IEEE/INCOSE vocabulary, (d) Wikipedia contamination confound [Q104, DATASET-D26], (e) HybLogic template learnability [Q105] inflates measured performance on patterns absent from real specs. — _Sources: Q104, Q105, DATASET-D9, DATASET-D10, DATASET-D22, WEB-13_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q62] 'our dataset has a vocabulary of 4,351 words' (p.5)
- [Q34] 'WikiLogic: annotation from scratch using Wikipedia articles as seeds.' (p.4)
- [Q47] 'Our dataset prioritizes realism and factual accuracy, steering clear of biases and stereotypes linked to identity markers' (p.4)
- [Q104] 'since the examples in WikiLogic are created from scratch by humans, it is possible that LLMs have seen similar texts with similar logical patterns in the training data.' (p.8)
- [Q105] 'HybLogic is created from templates and some of the logical patterns can be learned during fine-tuning.' (p.8)
- [Q55] 'we also add necessary commonsense knowledge in both the NL and FOL premises... We add such knowledge as additional premises at this stage.' (p.5)

*Web sources:*
- [WEB-13] No NLP benchmark exists for defense/aerospace requirements-language content
- [WEB-22] NLP requirements inconsistency work (IEEE RE 2023) confirms a gap in standardized benchmarks for INCOSE-style requirements
- [WEB-23] GPT-4 has been tested on building-regulation contradictions but not defense specifications

*Dataset analysis:*
- DATASET-D9: Software/BFS scenario — closest to technical content but still fully domain-neutral, no MIL-STD/IEEE vocabulary
- DATASET-D10: Aviation-adjacent (Boeing/Airbus) but no technical specifications or tolerances
- DATASET-D22: Meta brand reference — contemporary social/consumer content
- DATASET-D23: Political philosophy content — illustrates breadth-but-irrelevance of topic spread
- DATASET-D24: Biology facts drawn from Wikipedia — illustrates contamination concern
- DATASET-D26: Named individual likely Wikipedia-derived — contamination confound for LLM evaluation

</details>

**Information gaps:**
- Whether the test split (226 examples, not publicly visible) contains any engineering-domain content — sample was train-only.
- Whether full annotator pool includes anyone with systems-engineering background — documentation suggests no [Q108, Q122].

**Requires expert verification:**
- Whether any FOLIO content patterns transfer at all to MIL-STD/IEEE requirements-language reasoning would require empirical testing with practicing systems engineers.

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
Input form is the one dimension where FOLIO partially aligns with the deployment. Both are text-only English [Q22, DATASET-D4, D8], with no modality or script mismatch. FOLIO's surface conventions are carefully standardized: 'either-or' for exclusive disjunction [Q130], 'A or B, or both' for inclusive [Q131], grammar-checked with Grammarly [Q49], reviewed for naturalness [Q50], and ambiguity actively eliminated [Q51]. However, two substantial form mismatches remain. First, FOLIO inputs are short self-contained narratives (sampled premises range from 2 to ~9 sentences, ~50–200 tokens [DATASET-D1, D2]), while deployment documents are multi-thousand-word, multi-section specs (20,000–250,000+ words; 27K–100K+ tokens [WEB-6, WEB-7]). Second, FOLIO's deliberate elimination of ambiguity [Q51] produces inputs cleaner than real specs, which contain modal verbs, cross-references, and tolerance expressions absent from FOLIO. Recent long-context research [WEB-7] shows accuracy degradation from ~95% to ~60% at long contexts — a regime FOLIO cannot probe. The form mismatch is real but not categorical, so the dimension scores higher than IO/IC/OO/OF.

**Strengths:**
- Text-only English with no modality mismatch [Q22, DATASET-D4, D8] — directly aligns with deployment's text-only English interface.
- Russell & Norvig FOL syntax standard [Q52] is widely taught in CS curricula and would be familiar to engineering reviewers with formal training.
- Premise ordering does not encode label information [Q158, Q159, Q160] — accuracy changes ~1% under shuffling — so the benchmark is robust to one class of input-form artifact.
- Story-level train/val/test split [Q78, Q79] prevents premise leakage, supporting external validity for the form.

**Checklist:**

- **IF-1**: Signal distributions partially match: both are text-only English, but FOLIO inputs are short stories (~50–200 tokens) [DATASET-D1, D2] while deployment requires multi-thousand-word, multi-section documents (27K–100K+ tokens per [WEB-6]). The benchmark does not exercise long-context capability at all. — _Sources: Q22, WEB-6, DATASET-D1, DATASET-D2_
- **IF-2**: Regional infrastructure supports text input trivially. No capture-specification mismatch. However, on-premises/FedRAMP High deployment constraints driven by CUI/ITAR [WEB-3, WEB-4, WEB-9] mean models with very large context windows may not be available in compliant deployment configurations. — _Sources: WEB-3, WEB-4, WEB-9_
- **IF-3**: Domain-specific form differences: (a) FOLIO eliminates NL ambiguity [Q51], deployment documents are full of modal verbs and conditional language; (b) FOLIO uses standardized either-or/inclusive-or conventions [Q130, Q131], deployment uses normalized 'shall/should' register; (c) FOLIO has parallel FOL annotations [Q65], deployment has no FOL parallel — engineers reason directly on NL. — _Sources: Q51, Q65, Q130, Q131_
- **IF-4**: Form mismatches harming external validity: (a) input length 2–3 orders of magnitude shorter than deployment [DATASET-D1, D2, WEB-6]; (b) ambiguity actively eliminated [Q51] whereas deployment must handle ambiguity; (c) no multi-document structural form; (d) no normalized requirements-language register. — _Sources: Q51, WEB-6, WEB-7, DATASET-D1, DATASET-D2_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'We use formal logic, i.e., FOL to ensure the logical validity of the examples written in NL' (p.2)
- [Q49] 'All the sentences are first checked with a grammar checking tool, Grammarly.' (p.4)
- [Q51] 'We also eliminate natural language ambiguity when it is possible.' (p.4)
- [Q52] 'We adopt the FOL definitions and syntax most widely used in the AI community (Russell and Norvig, 2010).' (p.5)
- [Q78] 'We split FOLIO by 70%/15%/15% split for the train/validation/test sets' (p.6)
- [Q130] 'We always use either-or to express exclusive disjunction.' (p.13)
- [Q158] 'we shuffle the input premises to evaluate models.' (p.15)
- [Q159] 'accuracy increases or decreases by roughly 1% in most settings compared to our unshuffled premises.' (p.15)

*Web sources:*
- [WEB-6] 250-page technical spec can exceed 60,000 tokens; ~20,000-word SRD+ICD pair yields ~27,000 tokens
- [WEB-7] Long-context accuracy degrades from ~95% to ~60% on frontier models as input length grows
- [WEB-17] LongBench v2 covers multi-document tasks with median 54K-word contexts as proxy for long-context evaluation

*Dataset analysis:*
- DATASET-D1: Two-sentence minimal premise set — represents lower bound of FOLIO input length
- DATASET-D2: ~7-sentence, ~180-word premise set — upper end of FOLIO input length, orders of magnitude shorter than deployment documents
- DATASET-D4: Clean English declarative prose with no ambiguity — confirms register difference from spec language
- DATASET-D8: Unambiguous English prose — confirms Q51 ambiguity-elimination practice

</details>

**Information gaps:**
- No data on FOLIO performance under controlled length perturbations (e.g., padding stories with distractor premises) — would be informative for length sensitivity.

**Requires expert verification:**
- Whether the elimination of ambiguity [Q51] makes FOLIO performance an upper bound on real-spec performance — domain experts could validate by reviewing model outputs on real specs.

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's output ontology — True/False/Unknown classification labels [Q36, Q66, Q94] — is fundamentally misaligned with deployment requirements. The deployment explicitly demands natural-language explanations of the conflict mechanism paired with a confidence grade [Q3 elicitation, output_requirements.required_output_form], with bare classification 'explicitly non-actionable' for engineers reviewing hundreds of requirements. Dataset analysis confirms every example has exactly one of three string labels with no explanation, rationale, or confidence field [DATASET-D11, D25]. Furthermore, FOLIO's 'Unknown' label denotes formal undecidability from stated premises [Q66, DATASET-D25] — a fundamentally different concept from the deployment's notion of actionable uncertainty, which requires a statement of what additional information (referenced standard content, interface parameter) would resolve the ambiguity. An unexplained 'Uncertain' is treated as a tool failure in this deployment [output_requirements.uncertain_handling]. The output taxonomy violates both structural validity (the construct's structure is misrepresented — actionable contradiction explanation is reduced to a 3-way classification) and content validity (missing categories: explanation quality, calibrated confidence, resolution paths).

**Strengths:**
- Three-way label structure (not binary) [Q36, DATASET-D14, D25] is preferable to a pure binary, since it minimally distinguishes 'definitively conflicts' from 'undetermined' — a partial echo of the deployment's triage need.
- Labels are grounded in FOL semantics verified by an inference engine [Q2, Q57], so label correctness for the benchmark's intended construct is high.
- FOL operator coverage is comprehensive [Q138] — negation, conjunctions, disjunctions, implication, quantifiers, equality — supporting unambiguous derivation of truth values [Q136, Q137].

**Checklist:**

- **OO-1**: The True/False/Unknown taxonomy [Q66] is regionally relevant only in the most abstract sense (the labels themselves are not culturally biased). But for the deployment, the relevant 'output category' is structured natural-language explanation + confidence grade — a category entirely absent from FOLIO. — _Sources: Q66, DATASET-D11_
- **OO-2**: Missing categories specific to deployment: (a) natural-language explanation of conflict mechanism, (b) confidence grade for triage [output_requirements.triage_function], (c) resolution-path statement for uncertain findings, (d) traceability citation (REQ-IDs, document/section references) per cultural_and_professional_norms_notes. All four are essential to the deployment and none is in FOLIO's output ontology [DATASET-D11, D25]. — _Sources: DATASET-D11, DATASET-D25_
- **OO-3**: The 'Unknown' label encodes a non-deployment assumption: closed-world formal undecidability [Q66, DATASET-D25]. This is the opposite of the deployment's actionable-uncertainty notion. Models optimized on FOLIO learn to recognize closed-world undecidability, not to articulate what missing information would resolve an open-world conflict [output_requirements.uncertain_handling]. — _Sources: Q66, DATASET-D25_
- **OO-4**: Stakeholder-driven taxonomy redesign is necessary. The deployment requires a fundamentally different output schema (structured explanation + confidence + resolution path + traceability). FOLIO cannot be adapted by relabeling — the entire output structure must be replaced. — _Sources: Q66, DATASET-D11_
- **OO-5**: Taxonomy issues harming validity: (a) bare classification labels reduce a generative, explanatory task to a 3-way categorization [DATASET-D11]; (b) Unknown ≠ deployment's Uncertain [Q66, DATASET-D25]; (c) no confidence/calibration category [WEB-20 confirms calibration is a broader unresolved issue]; (d) no mechanism to assess explanation faithfulness [WEB-19, WEB-20, WEB-24]. — _Sources: DATASET-D11, DATASET-D25, WEB-19, WEB-20_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q36] 'Each of the stories is composed of several premises and conclusions with truth values of True, False, or Unknown' (p.4)
- [Q66] 'Given P and H, the goal is to determine the truth values of the conclusions: True, False or Unknown, based on FOL reasoning.' (p.6)
- [Q94] 'The majority baseline of our dataset is 38.5% since in our test set, there are 87, 78 and 61 examples with labels of true, false and unknown respectively.' (p.7)
- [Q135] 'FOL enables deriving facts from other facts' (p.13)
- [Q136] 'FOL, as a logical form, is a more explicit logical representation than its NL counterpart' (p.13)
- [Q138] 'We include the following operators: negation ¬, conjunction ∧, disjunction ∨, implication →, universal quantifier ∀, existential quantifier ∃, equal =.' (p.13)

*Web sources:*
- [WEB-19] FaithLM quantifies natural-language explanation faithfulness — directly relevant to deployment's explanation requirement, not addressed by FOLIO
- [WEB-20] All tested faithfulness metrics often fail to surpass a random baseline — explanation quality measurement is unresolved
- [WEB-21] Recent benchmark on reconciliatory contradiction explanation finds 'most models achieve limited success' across 18 LLMs
- [WEB-24] ACL 2024 faithfulness research confirms LLM explanations frequently unfaithful to actual reasoning

*Dataset analysis:*
- DATASET-D11: Label 'False' stored as bare string; no explanation of why disjunctive conclusion fails
- DATASET-D25: Uncertain label gives no indication of what would resolve the undecidability — confirms semantic mismatch with deployment's actionable uncertainty

</details>

**Information gaps:**
- Whether composite metrics combining FOLIO accuracy with separately-measured explanation-quality scores correlate with deployment-task performance — no such study exists.

**Requires expert verification:**
- Definition of acceptable confidence-grade calibration in the deployment context (e.g., what 'high confidence' threshold maps to engineering action) requires program-office input.

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
FOLIO's ground-truth labels are derived from automated FOL inference engine verification [Q2, Q57] over annotations written by CS students/researchers with formal FOL training [Q31, Q108, Q122, Q123]. The human expert baseline (95.98% accuracy) versus non-expert (61.82%) [Q111] confirms labels reflect what is logically provable from stated premises by FOL-trained humans. For the deployment, this introduces two convergent-validity concerns. First, annotators have no documented systems-engineering, aerospace, or defense expertise [Q108, Q122] — the ground truth reflects logical provability, not whether a practicing engineer would recognize a latent domain-convention conflict. Second, dataset analysis surfaces tangible annotation quality issues in the small sample: name mismatches between NL and FOL [DATASET-D18], an NL/FOL semantic contradiction [DATASET-D17], and several FOL parenthesis errors [DATASET-D16, D27, D28]. With ~5 identifiable issues in a 57-example sample, the error rate may be non-trivial, weakening the evidentiary value of FOLIO accuracy scores as a deployment proxy. The dimension scores 2 (not 1) because labels are correct in the closed-world FOL sense — they are wrong as a proxy for engineering judgment, not internally inconsistent in their own taxonomy.

**Strengths:**
- Inference-engine verification of label correctness [Q2, Q57] provides strong intra-construct ground truth — labels are not subjective and have been programmatically checked.
- Annotator selection criteria are explicit and rigorous: native or near-native English speakers with formal FOL coursework [Q26, Q27, Q28], multi-stage NL and FOL quality control by NLP/CL and FOL experts respectively [Q29, Q124, Q125].
- Substantial annotation investment: 980 man-hours across six stages [Q32], with 39.2% of stories rewritten after review [Q48] — suggests strong internal quality discipline.
- Three-way label distribution is reasonably balanced [Q94, DATASET-D14, D25] — models cannot trivially collapse to a binary classifier.

**Checklist:**

- **OC-1**: Labels reflect FOL-provability judgments by CS/FOL-expert annotators [Q108, Q122], not systems-engineering stakeholder perspectives. For deployment-relevant 'latent contradictions involving implicit domain constraints,' the labels do not encode the practicing engineer's judgment. — _Sources: Q108, Q122_
- **OC-2**: Likely substantial disagreement: a systems engineer reviewing a real spec would invoke MIL-STD/IEEE conventions and physical constraints not in the premise set. FOLIO annotators were instructed to add necessary commonsense as explicit premises [Q55] — solving the problem by elimination, not by testing implicit-knowledge invocation. Confirmed structural gap [WEB-13]. — _Sources: Q55, WEB-13_
- **OC-3**: Documentation discloses annotator demographics: CS undergraduate/graduate students and researchers [Q16, Q31], native or near-native English [Q27], FOL coursework [Q28, Q123]. No aerospace/defense/ICD background documented. Datasheet-style disclosure is partial. — _Sources: Q16, Q27, Q28, Q108, Q122, Q123_
- **OC-4**: Re-annotation by representative regional pool (US-based practicing systems engineers) would be necessary to assess deployment validity but is impractical at FOLIO scale; the more economical path is a purpose-built test suite of real or synthetic defense spec contradictions reviewed by domain experts. — _Sources: Q108, WEB-13_
- **OC-5**: INSUFFICIENT DOCUMENTATION on aggregation. Paper does not describe inter-annotator agreement statistics by sub-population or whether minority-perspective disagreements were preserved; the FOL-verification step [Q57] arguably erases human disagreement entirely in favor of automated provability.
- **OC-6**: Label issues harming convergent/external validity: (a) annotator pool lacks deployment-domain expertise [Q108, Q122]; (b) labels reflect closed-world provability, not open-world engineering judgment [Q66]; (c) observable annotation errors in sample (NL/FOL mismatches, FOL parenthesis issues) [DATASET-D17, D18, D16, D27]; (d) Wikipedia contamination [Q104] confounds label-quality interpretation for LLM evaluation. — _Sources: Q66, Q104, Q108, DATASET-D16, DATASET-D17, DATASET-D18, DATASET-D27_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'The logical correctness of the premises and conclusions is ensured by their FOL annotations, which are automatically verified by an FOL inference engine.' (p.1)
- [Q16] 'FOLIO is a high-quality and manually curated dataset, written by CS undergraduate and graduate students and researchers in academia and industry.' (p.2)
- [Q31] 'All stories and FOL annotations in FOLIO are written and reviewed by expert annotators, including CS undergraduate and graduate students, and senior researchers' (p.4)
- [Q48] '39.2% of the stories suffer from at least one of these issues. We implemented a detailed protocol to rewrite these stories.' (p.4)
- [Q108] 'Our expert annotators are computer science college students familiar with FOL.' (p.9)
- [Q111] 'Expert annotations achieve an accuracy of 95.98% while non-expert annotations achieves 61.82%' (p.9)
- [Q122] 'Our annotators are either college or graduate students who are native English speakers' (p.12)
- [Q124] 'At the NL quality check stage, only annotators who are experts in natural language processing or computational linguistics are involved.' (p.12)

*Web sources:*
- [WEB-13] Space mission paper explicitly notes lack of standardized datasets for requirements verification — confirms no off-the-shelf engineer-annotated benchmark

*Dataset analysis:*
- DATASET-D14: Inference-engine-verified True label on 6-premise chain — confirms strong internal label quality for closed-world construct
- DATASET-D16: FOL parenthesis error in Ex. 36 — annotation quality issue
- DATASET-D17: NL says Matt 'does not invest' but FOL ground fact says InvestInRegularly(matt, publicStockMarket) — direct semantic mismatch
- DATASET-D18: NL says 'John' but FOL says 'jim' — entity-name mismatch
- DATASET-D27: Missing closing parenthesis in FOL — syntactic issue
- DATASET-D28: Extra closing parenthesis in FOL — syntactic issue

</details>

**Information gaps:**
- Annotation error rate on full dataset (sample suggests ~5-9% of examples have issues; test split not inspected).
- Inter-annotator agreement statistics are not reported in the documentation.

**Requires expert verification:**
- Whether a defense systems engineer would assign the same labels to FOLIO examples as the CS-trained annotators — informative for understanding the label-construct gap.

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's output form — accuracy on True/False/Unknown classification [Q80] plus SynV and ExcAcc for translation [Q73–Q76] — is fundamentally mismatched with deployment needs. The deployment requires structured natural-language explanations citing specific requirement IDs (e.g., 'REQ-SYS-0042 in the SRD conflicts with ICD-PWR-007 Section 3.2.1' per cultural_and_professional_norms_notes), a confidence grade for triage [output_requirements.triage_function], and resolution paths for uncertain findings — none of which FOLIO measures. Critically, FOLIO evaluates single isolated (premise_set, conclusion) pairs [DATASET-D21, D2], whereas the deployment's central use case is cross-document reasoning across multiple long-form documents simultaneously [Q4 elicitation, cross_document_reasoning_note]. There is no benchmark mechanism that probes multi-document context handling or traceability output. Auxiliary findings amplify the concern: GPT-4 is 31.82% below expert human accuracy [Q113], models systematically overpredict True [Q155, Q157] with False/Unknown accuracy only 54–62% [Q156], and performance degrades sharply beyond 3 reasoning hops [Q99] — all indicating that even the closed-world classification baseline is challenged, while the deployment requires capabilities entirely outside the benchmark's measurement apparatus. The authors themselves defer 'a more reliable metric' for translation to future work [Q77].

**Strengths:**
- Stability protocol — five randomly-sampled training sets with averaged accuracy [Q93] — produces robust point estimates rather than noisy single runs.
- Premise-shuffling experiment confirms minimal label-order artifacts (~1% accuracy change) [Q158, Q159, Q160], so accuracy reflects reasoning rather than positional heuristics.
- Story-level train/val/test split [Q78, Q79] prevents premise leakage, supporting external validity of the accuracy estimate within the benchmark's construct.
- Reporting breakdowns by reasoning depth [Q99] and by sub-pipeline (WikiLogic vs. HybLogic) [Q102, Q105] provides diagnostic granularity useful for capability profiling.

**Checklist:**

- **OF-1**: Output modality mismatch is total. Deployment requires structured natural-language explanations + confidence grade + traceability citations [output_requirements]; FOLIO outputs a single label per example [Q80, DATASET-D11]. Single-context vs. multi-document mismatch [DATASET-D21, D2] is equally categorical. — _Sources: Q80, DATASET-D11, DATASET-D21, DATASET-D2_
- **OF-2**: Not applicable — deployment is text-only [infrastructure_and_deployment_notes.interface_modality]; no speech output requirement.
- **OF-3**: Not applicable — target users are professional engineers with high literacy in normalized requirements register; accessibility constraints are not the binding constraint here. The relevant accessibility analog is whether outputs are actionable for expert review, which they are not [DATASET-D11, D25]. — _Sources: DATASET-D11, DATASET-D25_
- **OF-4**: Form mismatches harming external validity: (a) classification accuracy is the only metric [Q80], cannot assess explanation quality [WEB-19, WEB-20]; (b) no multi-document evaluation [DATASET-D21]; (c) no confidence-calibration metric; (d) no traceability/citation metric; (e) NL-FOL translation metrics SynV and ExcAcc are acknowledged as imperfect [Q77] and target a capability deployment does not need. — _Sources: Q77, Q80, DATASET-D11, DATASET-D21, WEB-19, WEB-20_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q80] 'We use accuracy for evaluating logical reasoning performance.' (p.6)
- [Q73] 'Two metrics are adopted to evaluate NL-FOL translation... Syntactic validity (SynV).' (p.6)
- [Q75] 'Inference Engine execution accuracy (ExcAcc).' (p.6)
- [Q77] 'We leave for future work the design of a more reliable metric of NL-FOL translation.' (p.6)
- [Q99] 'GPT-3.5 and GPT-4 both perform much better on examples with a 0 ∼ 3 reasoning depth, indicating that examples with a 4 ∼ 7 reasoning depth pose a challenge to the SoTA LMs.' (p.8)
- [Q113] 'The expert and GPT-4 gap is 31.82%, suggesting significant room for model improvement.' (p.9)
- [Q155] 'LLMs are significantly better at making the correct predictions for conclusions with labels of True than the conclusions with labels of False or Unknown.' (p.15)
- [Q156] 'The accuracy on examples with False or Unknown conclusions is 61.9% with fine-tuning and 54.0% with few-shot prompting.' (p.15)
- [Q158] 'we shuffle the input premises to evaluate models.' (p.15)

*Web sources:*
- [WEB-16] MDBench targets multi-document reasoning — usable as supplementary proxy for cross-document deployment capability
- [WEB-17] LongBench v2 covers multi-document tasks with median 54K-word contexts — partial proxy for OF gap
- [WEB-19] FaithLM evaluates natural-language explanation faithfulness — capability FOLIO does not assess
- [WEB-21] Reconciliatory contradiction explanation benchmark across 18 LLMs finds 'most models achieve limited success'

*Dataset analysis:*
- DATASET-D11: Single string label 'False' is the entire output — no explanation, no confidence, no citation
- DATASET-D2: Single 'company world' premise block — no cross-document or multi-source structural form
- DATASET-D21: Single 'event world' — confirms single-context structural unit, no cross-document analog
- DATASET-D25: Uncertain label with no resolution path — confirms output-form gap for actionable uncertainty

</details>

**Information gaps:**
- Whether FOLIO accuracy correlates at all with explanation-quality or multi-document-reasoning capability — no such correlation study exists [gap_id 4].

**Requires expert verification:**
- Whether MDBench or LongBench v2 scores serve as adequate supplementary proxies for the deployment's cross-document requirement requires domain validation.

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** FOLIO has no task category for open-world / implicit-premise reasoning or cross-document tracing — directly opposite to the deployment's core challenge.

**Recommendation:** Construct a purpose-built test suite (~100–300 examples) of synthetic or de-classified defense spec excerpts where the relevant constraint lives in a referenced MIL-STD/IEEE/ICD section. Pair each example with a target finding written by a practicing systems engineer. Use FOLIO only as a baseline filter; do not treat FOLIO accuracy as evidence of deployment readiness.

### Input Content ⚠

**Gap:** Zero engineering-domain vocabulary or 'shall/should' requirements-language register in FOLIO; systematic construct-irrelevant variance for the deployment.

**Recommendation:** Augment evaluation with a small, curated corpus of requirements-language examples drawn from publicly available NASA, INCOSE, or unclassified DoD specs, annotated for crisp and latent contradictions by systems engineers. Even 50–100 high-quality engineer-validated examples will provide more signal than FOLIO's 1,430 domain-neutral stories for the deployment-specific construct.

### Output Ontology ⚠

**Gap:** Bare True/False/Unknown classification cannot capture the deployment's required output (NL explanation + confidence grade + resolution path).

**Recommendation:** Redesign the output schema for any deployment evaluation: require structured outputs with (a) NL conflict-mechanism explanation citing specific requirement IDs, (b) calibrated confidence grade for triage, and (c) for uncertain findings, an explicit statement of what missing information would resolve the ambiguity. Evaluate explanation quality using a faithfulness-aware protocol (e.g., FaithLM-style [WEB-19]) plus blind engineer review.

### Output Form ⚠

**Gap:** FOLIO measures single-example classification accuracy with no mechanism for multi-document or long-context evaluation, no confidence-calibration metric, and no traceability-citation metric.

**Recommendation:** Add MDBench [WEB-16] and LongBench v2 [WEB-17] as supplementary cross-document/long-context proxies. Build a multi-document evaluation harness using SRD+ICD pairs (real or synthetic) where the contradiction spans documents; report not only accuracy but explanation quality, confidence calibration (e.g., ECE), and citation accuracy (correct REQ-IDs cited).

### Input Form

**Gap:** FOLIO inputs are short ambiguity-free narratives (50–200 tokens); deployment inputs are 27K–100K+ token multi-section specifications where LLM reasoning quality is known to degrade.

**Recommendation:** Include explicit long-context stress tests in the deployment evaluation: replicate or extend the Chroma 2025-style length-degradation analysis [WEB-7] with representative spec documents to characterize the operating context-length envelope. Pair this with infrastructure planning (FedRAMP High / on-premises) per the CMMC/ITAR constraints [WEB-1, WEB-4].

### Output Content

**Gap:** Annotators are CS/FOL experts, not systems engineers; ground-truth labels reflect closed-world provability rather than engineering domain judgment. Sample inspection also reveals scattered NL/FOL inconsistencies.

**Recommendation:** For the deployment's purpose-built test suite, recruit ≥3 practicing systems engineers per example for label consensus, retain dissent for ambiguous cases rather than aggregating it away, and explicitly capture whether the contradiction requires invocation of an implicit referenced-standard constraint. Treat FOLIO ground-truth as informative only for the closed-world sub-construct.

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
| Q13 | 1 | input_content | "RuleTaker has only 101 words in its vocabulary and LogicNLI has 1077 words in the vocabulary." |
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
| Q50 | 4 | input_form | "Our annotators who have graduated from or are senior students studying English Literature conducted a thorough round of review for grammatical correctness and language naturalness." |
| Q51 | 4 | input_form | "We also eliminate natural language ambiguity when it is possible." |
| Q52 | 5 | input_form | "We adopt the FOL definitions and syntax most widely used in the AI community (Russell and Norvig, 2010)." |
| Q53 | 5 | output_content | "In preliminary investigations, we found that the human-written FOL formulas suffer from FOL consistency issues, which necessitates an additional round of quality control for FOL formulas." |
| Q54 | 5 | output_content | "One NL sentence can be translated into FOL through multiple non-equivalent ways. For example, sometimes additional information inferred from a sentence can be represented in FOL, leading to multiple representations. We therefore design an annotation protocol for FOL translation in order to ensure that our FOL translations are as consistent as possible across all examples in our dataset." |
| Q55 | 5 | input_content | "Apart from checking whether NL and FOL express equivalent meanings, we also add necessary commonsense knowledge in both the NL and FOL premises. Sometimes humans do not write certain commonsense knowledge in the premises that is required in the FOL reasoning process, which is based solely on the premises given. We add such knowledge as additional premises at this stage." |
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
| Q101 | 8 | output_form | "FOLIO's unique complexity reveals that current LMs are limited in their ability to extrapolate to longer and more complex reasoning chains, and suggests an avenue for further study." |
| Q102 | 8 | output_form | "As shown in Table 6, in logical reasoning, GPT-3.5 and GPT-4 achieve substantially lower results on HybLogic than on WikiLogic and the result is slightly higher than chance." |
| Q103 | 8 | output_form | "We hypothesize that this is because HybLogic has high logical complexity that the SoTA LLMs like GPT-4 cannot solve yet while WikiLogic examples require shorter reasoning chains which the model is already capable of solving." |
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
| Q129 | 13 | input_content | "For stories that pertain to generalization, such as "All As are Bs," we have added specifiers like "all Dan knows" to give a degree of reasonable factuality." |
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
| WEB-1 | https://www.federalregister.gov/documents/2024/10/15/2024-22905/cybersecurity-maturity-model-certification-cmmc-program |
| WEB-2 | https://www.crowell.com/en/insights/client-alerts/finally-the-cmmc-final-rule-dod-completes-cmmc-rulemaking-ushering-in-new-era-in-dod-cybersecurity |
| WEB-3 | https://www.dwt.com/blogs/privacy--security-law-blog/2025/09/defense-department-cybersecurity-cmmc-final-rule |
| WEB-4 | https://www.kiteworks.com/regulatory-compliance/itar-ai-agents-compliance-gap/ |
| WEB-5 | https://www.justsecurity.org/126643/ai-model-outputs-export-control/ |
| WEB-6 | https://www.devtoolkit.cloud/blog/llm-context-windows-explained-why-size-matters |
| WEB-7 | https://blog.bytebytego.com/p/a-guide-to-context-engineering-for |
| WEB-8 | https://www.hklaw.com/en/insights/publications/2025/11/cmmc-regulations-key-questions-and-answers-for-defense-contractors |
| WEB-9 | https://www.kiteworks.com/cmmc-compliance/military-technology-contractors/ |
| WEB-10 | https://www.emergentmind.com/topics/contractnli |
| WEB-11 | https://arxiv.org/abs/2212.03222 |
| WEB-12 | https://github.com/HazyResearch/legalbench |
| WEB-13 | https://arxiv.org/abs/2503.14130 |
| WEB-14 | https://arxiv.org/abs/1510.02669 |
| WEB-15 | https://arxiv.org/abs/2508.03215 |
| WEB-16 | https://arxiv.org/abs/2506.14927 |
| WEB-17 | https://arxiv.org/abs/2412.15204 |
| WEB-18 | https://arxiv.org/abs/2508.09848 |
| WEB-19 | https://arxiv.org/abs/2402.04678 |
| WEB-20 | https://arxiv.org/abs/2502.18848 |
| WEB-21 | https://arxiv.org/abs/2603.22735 |
| WEB-22 | https://medium.com/@dsobczynski88/applying-nlp-and-ai-to-improve-quality-of-software-requirement-statements-using-incose-guide-to-bd57ce2db14f |
| WEB-23 | https://arxiv.org/abs/2412.20602 |
| WEB-24 | https://www.lgresearch.ai/blog/view?seq=485 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (config: default)
**Analysis date:** 2025-01-31
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | yale-nlp/FOLIO | Ex. 1 (story_id 271) | True | "No plants are fungi. Mushrooms are fungi." | Minimal 2-premise syllogism; fully explicit closed-world premises | IO, IC |
| D2 | yale-nlp/FOLIO | Ex. 2 (story_id 376) | Uncertain | "People in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises." | Multi-premise narrative about a tech company employee; all predicates fully stated | IO, IC |
| D3 | yale-nlp/FOLIO | Ex. 3 (story_id 180) | Uncertain | "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac." | Self-contained programming scenario; all relevant constraints explicitly stated in premises | IO |
| D4 | yale-nlp/FOLIO | Ex. 28 (story_id 252) | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. A country cannot simultaneously regulate the exchange rate and successfully control inflation." | Policy/economics domain; fully explicit premises; no external standard referenced | IC, IO |
| D5 | yale-nlp/FOLIO | Ex. 22 (story_id 475) | Uncertain | "Everyone who is entitled to national social insurance coverage can have their medical bills partially covered. All PRC nationals are entitled to national social insurance coverage." | International policy scenario; all rules fully spelled out | IO |
| D6 | yale-nlp/FOLIO | Ex. 11 (story_id 486) | False | "Everything in Size Town is big or small. All big things in Size Town are heavy." | Abstract taxonomy story; no real-world domain knowledge required | IC |
| D7 | yale-nlp/FOLIO | Ex. 43 (story_id 393) | True | "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning." | Meta-logical content; fully closed-world | IC, IO |
| D8 | yale-nlp/FOLIO | Ex. 34 (story_id 377) | True | "Everything is either outside the solar system or in the solar system. Nothing outside the solar system has the Sun as its star." | Scientific premises fully stated; no reference to external standards | IC |
| D9 | yale-nlp/FOLIO | Ex. 46/47 (story_id 448) | Uncertain/False | "Everyone that knows about breath-first-search knows how to use a queue. If someone is a seasoned software engineer interviewer at Google, then they know what breath-first-search is." | CS/software domain; all premises explicit and domain-neutral | IC |
| D10 | yale-nlp/FOLIO | Ex. 23 (story_id 108) | Uncertain | "The world's only major large passenger aircraft manufacturers are Boeing and Airbus. All American Airlines planes are from the world's major large passenger aircraft manufacturers." | Aviation adjacent; but no technical specifications, tolerances, or implicit standards | IC, IO |
| D11 | yale-nlp/FOLIO | Ex. 55 (story_id 477) | False | "TikTok is a social media application, and it is not ideal for preteens." | Consumer tech scenario; ¬(chat ⊕ computer_program) conclusion structure | OO |
| D12 | yale-nlp/FOLIO | Ex. 2 (story_id 376) | Uncertain | "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" | FOL parallel annotation; shows explicit closed-world FOL encoding | IF, OO |
| D13 | yale-nlp/FOLIO | Ex. 4 (story_id 408) | False | "No trick-shot artist in Yale's varsity team struggles with half court shots." | Multi-premise sports scenario; label False from fully explicit premises | OO |
| D14 | yale-nlp/FOLIO | Ex. 16 (story_id 346) | True | "All Olympic gold medal winners are professional athletes. No full-time scientists spend the majority of their time on sports." | 6-premise chain with compound conditional; inference-engine verified True | OC |
| D15 | yale-nlp/FOLIO | Ex. 21 (story_id 381) | False | "If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up in old-fashioned and historical period clothing." | Complex conditional with exclusive disjunction; no domain knowledge required | IO |
| D16 | yale-nlp/FOLIO | Ex. 36 (story_id 422) | True | "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" | Parenthesis error in FOL annotation for Lily's premise | OC |
| D17 | yale-nlp/FOLIO | Ex. 57 (story_id 362) | False | "Matt does not invest in the public stock market regularly. Matt likes financial risks." | Contradictory premise pair (Ex 57 NL says Matt does NOT invest but FOL says InvestInRegularly(matt, publicStockMarket)) | OC |
| D18 | yale-nlp/FOLIO | Ex. 52 (story_id 337) | True | "Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises. … ¬(ProfessionalBasketballPlayer(jim) ⊕ NeverExercises(jim))" | NL says "John," FOL says "jim" — name inconsistency between NL and FOL | OC |
| D19 | yale-nlp/FOLIO | Ex. 33 (story_id 341) | Uncertain | "Moonwatch is either a digital watch and an automatic, or it is neither." | Product-domain scenario; conclusion-FOL uses "moonWatch" while NL uses "Moonwatch" — capitalization inconsistency | OC |
| D20 | yale-nlp/FOLIO | Ex. 13 (story_id 395) | False | "No satin-finish lipsticks in the set do not have 'rosewood' in its offical description." | Double negation in premise NL ("do not have" in a "No…not" construction); potential NL ambiguity | IC, OC |
| D21 | yale-nlp/FOLIO | Ex. 5 (story_id 348) | Uncertain | "All Yale students at the event are college students. Everyone at the event is a Yale student or a Harvard student." | Classic syllogistic structure, fully explicit | IO |
| D22 | yale-nlp/FOLIO | Ex. 38 (story_id 425) | False | "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination." | Contemporary brand reference; all premises fully stated | IC |
| D23 | yale-nlp/FOLIO | Ex. 6 (story_id 423) | Uncertain | "Everyone at the business conference who is an ardent communist prefers state ownership of the means of production." | Political/ideological content (communist, planned economy); explicitly stated in premises | IC |
| D24 | yale-nlp/FOLIO | Ex. 29 (story_id 210) | False | "The only types of mammals that lay eggs are either platypuses or echidnas. … Grebes are not platypuses and also not echidnas." | Biology facts used as premises; verifiable real-world knowledge | IC |
| D25 | yale-nlp/FOLIO | Ex. 50 (story_id 284) | Uncertain | "Each building is tall. Everything tall has height." | Minimal 2-premise story; "All buildings are magnificent" — Uncertain since 'magnificent' not derivable | OO |
| D26 | yale-nlp/FOLIO | Ex. 7 (story_id 30) | Uncertain | "Andy Chang is from Hong Kong." | Specific named person (likely real individual); Wikipedia-seeded | IC |
| D27 | yale-nlp/FOLIO | Ex. 57 (story_id 362) | False | "∀x (SpendAt(x, alotOfMoney, casino) ∨ (∃y (¬(y=casino) ∧ BettingGame(y) ∧ SpendAt(x, aLotOfMoney, y)) → AtRiskOf(x, gamblingAddiction))" | FOL missing closing parenthesis — syntactic issue in annotation | OC |
| D28 | yale-nlp/FOLIO | Ex. 10 (story_id 391) | Uncertain | "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" | Extra closing parenthesis in FOL — syntactic issue | OC |

---

### Deployment-Relevant Strengths

#### Strength 1: Verified multi-hop logical inference chains
- **Dimension(s):** IO
- **Observation:** Examples in the sample demonstrate multi-step deductive chains that require chaining several conditional rules before a conclusion can be evaluated. The Yale varsity team scenario (story 408) chains four universal conditionals before the False label for "Jack is bad at mid-range shots" can be derived; the Size Town scenario (story 486) chains six sequential implications.
- **Deployment relevance:** For the deployment's crisp-contradiction detection sub-task (e.g., explicit numeric contradictions), FOLIO's multi-hop classical logic coverage is genuinely relevant as a lower-bound proxy for a model's ability to chain explicit rules. A model that performs poorly here is almost certainly unfit for deployment.
- **Datapoint citations:**
  - [D13] Example 4 (yale-nlp/FOLIO, split=train, label=False): "No trick-shot artist in Yale's varsity team struggles with half court shots. Everyone on Yale's varsity team is someone who struggles with half court shots or who successfully shoots a high percentage of 3-pointers." — Four chained universals required to reach False verdict.
  - [D6] Example 11 (yale-nlp/FOLIO, split=train, label=False): "Everything in Size Town is big or small. All big things in Size Town are heavy. All small things in Size Town are light. All heavy things in Size Town are still. All light things in Size Town are unstable." — Six-hop chain ending in a compound disjunctive conclusion.

#### Strength 2: Full operator coverage including exclusive disjunction and implication
- **Dimension(s):** IO
- **Observation:** The sampled examples confirm FOLIO's documented operator coverage: negation (¬), conjunction (∧), inclusive and exclusive disjunction (∨, ⊕), implication (→), and quantifiers (∀, ∃) all appear throughout the sample, often combined within single premises.
- **Deployment relevance:** Defense specification contradictions often hinge on biconditional or disjunctive requirements ("A or B, but not both"). FOLIO's operator breadth ensures a tested model has been exposed to these logical structures in at least a minimal sense.
- **Datapoint citations:**
  - [D12] Example 2 (yale-nlp/FOLIO, split=train, label=Uncertain): "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" — Shows conjunction + implication + negation combined.
  - [D15] Example 21 (yale-nlp/FOLIO, split=train, label=False): "¬(FocusedOn(clyde, futuristicSubject) ∧ FocusedOn(clyde, vocationalSubject))→ ¬(FocusedOn(clyde, futuristicSubject) ∧ FocusedOn(clyde, vocationalSubject) ∨ (Enjoy(clyde, dressingUp, oldFashionedClothing)…)" — Complex nested negation and disjunction.

#### Strength 3: Well-balanced three-way label distribution confirmed in sample
- **Dimension(s):** OO, OC
- **Observation:** Of the 57 sampled examples, True/False/Uncertain labels are all substantially represented, consistent with the documented near-equal split (~38.5% True majority in test set). The sample includes clear True examples (Ex. 1, 12, 31, 48, 53), clear False examples (Ex. 4, 11, 17, 29, 30, 37, 38, 47), and many Uncertain examples, with labels verified by inference engine.
- **Deployment relevance:** A model trained or evaluated on FOLIO is unlikely to collapse to a binary classifier, which is minimally necessary for downstream use in detecting "possibly conflicting but not definitively" requirement relationships.
- **Datapoint citations:**
  - [D14] Example 16 (yale-nlp/FOLIO, split=train, label=True): "All Olympic gold medal winners are professional athletes. No full-time scientists spend the majority of their time on sports." — True label from 6-premise chain, inference-engine verified.
  - [D25] Example 50 (yale-nlp/FOLIO, split=train, label=Uncertain): "Each building is tall. Everything tall has height." with conclusion "All buildings are magnificent." — Uncertain because "magnificent" is not derivable from stated premises — good illustration of the undecidability semantics.

#### Strength 4: Self-contained English prose — no modality mismatch
- **Dimension(s):** IF
- **Observation:** All examples are written in grammatical English prose with no images, tables, audio, or non-English content. Premises and conclusions are short declarative sentences amenable to direct text input.
- **Deployment relevance:** The deployment is text-only English, so there is no input modality mismatch. This is the one dimension where FOLIO is well-aligned.
- **Datapoint citations:**
  - [D4] Example 28 (yale-nlp/FOLIO, split=train, label=False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency." — Clean English declarative prose.
  - [D8] Example 34 (yale-nlp/FOLIO, split=train, label=True): "Everything is either outside the solar system or in the solar system. Nothing outside the solar system has the Sun as its star." — Unambiguous English prose.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: All premises are fully and explicitly stated — the inverse of the deployment's core challenge
- **Dimension(s):** IO, IC
- **Observation:** Every example in the sample provides a complete, self-contained premise set. No example requires a model to recognize that a referenced external authority (standard, specification, convention) carries implicit constraints. When domain facts are needed, they are added directly as explicit premises. This is confirmed across the entire reviewed sample without exception.
- **Deployment relevance:** The deployment's highest-priority challenge is detecting latent contradictions where one side of the conflict is implicit in a referenced standard (MIL-STD, IEEE) not restated in the document. FOLIO systematically excludes this challenge by design. A model that achieves high FOLIO accuracy may still completely fail to invoke implicit domain constraints — and FOLIO provides no signal for this capability.
- **Datapoint citations:**
  - [D1] Example 1 (yale-nlp/FOLIO, split=train, label=True): "No plants are fungi. Mushrooms are fungi." — Complete logical world in two sentences; no external knowledge needed.
  - [D3] Example 3 (yale-nlp/FOLIO, split=train, label=Uncertain): "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac. Sam is using a Mac." — All constraints explicitly stated; nothing implicit.
  - [D5] Example 22 (yale-nlp/FOLIO, split=train, label=Uncertain): "Everyone who is entitled to national social insurance coverage can have their medical bills partially covered. All PRC nationals are entitled to national social insurance coverage." — Even geopolitical facts are restated as premises rather than assumed.

#### Concern 2: Zero engineering-domain vocabulary or domain-grounded latent contradiction content
- **Dimension(s):** IC
- **Observation:** The full sample of 57 examples contains no examples involving thermal budgets, timing requirements, bus bandwidth, interface parameters, tolerances, power dissipation, signal integrity, mass/volume allocations, or any other systems-engineering domain. Domains present include: sports, consumer products, biology, film, geography, social policy, personal habits, philosophy of logic, and pop culture. Even examples that touch adjacent technical domains (aviation, software) remain fully domain-neutral.
- **Deployment relevance:** The deployment's highest-value cases are latent contradictions that require physics- and systems-engineering-grounded reasoning. FOLIO provides no coverage of this content whatsoever. FOLIO accuracy scores will be construct-irrelevant for this sub-task.
- **Datapoint citations:**
  - [D10] Example 23 (yale-nlp/FOLIO, split=train, label=Uncertain): "The world's only major large passenger aircraft manufacturers are Boeing and Airbus. All American Airlines planes are from the world's major large passenger aircraft manufacturers." — Aviation adjacent but entirely domain-neutral; no technical specifications.
  - [D9] Example 46 (yale-nlp/FOLIO, split=train, label=Uncertain): "Everyone that knows about breath-first-search knows how to use a queue. If someone is a seasoned software engineer interviewer at Google, then they know what breath-first-search is." — Software domain but fully explicit; no MIL-STD, IEEE, or technical constraint vocabulary.
  - [D7] Example 43 (yale-nlp/FOLIO, split=train, label=True): "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning." — Meta-logical content; no engineering domain.

#### Concern 3: Single self-contained story per example — no cross-document or multi-context reasoning
- **Dimension(s):** OF, IO
- **Observation:** Every example in the sample is structurally a single story with one consolidated premise set and one or more conclusions derived from that single context. No example requires a model to hold multiple documents or premise sets in context simultaneously and detect a contradiction between them. The benchmark's structural unit is the (premise_set, conclusion) pair.
- **Deployment relevance:** Cross-document reasoning — tracing a requirement in a system-level SRD against a constraint in a subsystem spec or ICD — is the deployment's central use case. FOLIO cannot measure this capability at all. Performance on FOLIO provides no evidence about cross-document reasoning.
- **Datapoint citations:**
  - [D21] Example 5 (yale-nlp/FOLIO, split=train, label=Uncertain): "All Yale students at the event are college students. Everyone at the event is a Yale student or a Harvard student. Susan is at the event…" — Single event/world; all premises in one consolidated set.
  - [D2] Example 2 (yale-nlp/FOLIO, split=train, label=Uncertain): "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises. … Mike works in this tech company." — Single company "world"; all context in one premise block.

#### Concern 4: Output is bare True/False/Uncertain label — no natural-language explanation or confidence grade
- **Dimension(s):** OO, OF
- **Observation:** Every example in the dataset has exactly one of three string labels: "True", "False", or "Uncertain". The schema confirms no explanation field, no rationale field, no confidence field, and no mechanism to produce or evaluate natural-language descriptions of why a conclusion holds or fails. The NL and FOL columns provide input but no output explanatory structure.
- **Deployment relevance:** The deployment explicitly requires natural-language explanations of the conflict mechanism paired with a confidence grade. Bare True/False/Uncertain labels are described as explicitly non-actionable. FOLIO's evaluation apparatus cannot assess this requirement at all.
- **Datapoint citations:**
  - [D11] Example 55 (yale-nlp/FOLIO, split=train, label=False): "TikTok is a social media application, and it is not ideal for preteens." — Label is simply "False"; no explanation of why the disjunctive conclusion fails is stored or evaluated.
  - [D25] Example 50 (yale-nlp/FOLIO, split=train, label=Uncertain): "Each building is tall. Everything tall has height." — Label "Uncertain" gives no indication of what additional information would resolve the undecidability, which is a hard requirement for this deployment's uncertainty outputs.

---

#### MAJOR

#### Concern 5: Annotation errors and NL/FOL inconsistencies observed in sample
- **Dimension(s):** OC
- **Observation:** Several examples in the sample contain apparent annotation errors: (a) Ex. 57 (story 362) has a contradiction between NL ("Matt does not invest in the public stock market regularly") and FOL (InvestInRegularly(matt, publicStockMarket) as a ground fact) along with a missing closing parenthesis in a FOL formula; (b) Ex. 52 (story 337) uses "John" in the NL premises but "jim" in the FOL; (c) Ex. 36 (story 422) has a missing closing parenthesis in the FOL for Lily's premise; (d) Ex. 10 (story 391) has an extra closing parenthesis in the last FOL premise; (e) Ex. 20 (story 395) has a double negation in the NL ("No satin-finish lipsticks in the set do not have 'rosewood' in its official description") that may not parse as intended.
- **Deployment relevance:** These errors in a 57-example sample suggest the annotation quality, while generally high, is not error-free. For a deployment where ground-truth label reliability directly calibrates trust in the benchmark as a proxy, annotation errors undermine the evidentiary value of FOLIO accuracy scores.
- **Datapoint citations:**
  - [D17] Example 57 (yale-nlp/FOLIO, split=train, label=False): "Matt does not invest in the public stock market regularly. Matt likes financial risks." (NL) vs. "InvestInRegularly(matt, publicStockMarket)" (FOL) — NL and FOL directly contradict on whether Matt invests.
  - [D18] Example 52 (yale-nlp/FOLIO, split=train, label=True): "Either John is a professional basketball player and he never exercises…" (NL uses "John") vs. "¬(ProfessionalBasketballPlayer(jim) ⊕ NeverExercises(jim))" (FOL uses "jim") — Name mismatch.
  - [D16] Example 36 (yale-nlp/FOLIO, split=train, label=True): "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" — Parenthesis closed inside the In() predicate rather than after it, producing syntactically malformed FOL.
  - [D27] Example 57 (yale-nlp/FOLIO, split=train, label=False): "∀x (SpendAt(x, alotOfMoney, casino) ∨ (∃y (¬(y=casino) ∧ BettingGame(y) ∧ SpendAt(x, aLotOfMoney, y)) → AtRiskOf(x, gamblingAddiction))" — Missing closing parenthesis on existential quantifier scope.
  - [D20] Example 13 (yale-nlp/FOLIO, split=train, label=False): "No satin-finish lipsticks in the set do not have 'rosewood' in its offical description." — Double negation in NL ("No … do not have") creates potential ambiguity about intended logical content.

#### Concern 6: Domain-neutral general knowledge content — systematic construct-irrelevant variance for the deployment
- **Dimension(s):** IC
- **Observation:** The sample spans consumer products (lipstick, watches, brand products), pop culture (Harry Potter, TikTok, Meta), sports (basketball, Yale varsity), entertainment (films, TV), political philosophy (communism, planned economy), and casual social scenarios (travel planning, party food). No example is recognizably from technical specification, requirements engineering, or defense/aerospace domains. Even the economics example (story 252, Russian embargo) uses general macroeconomic reasoning, not engineering domain logic.
- **Deployment relevance:** Every topic in FOLIO introduces construct-irrelevant variance relative to the deployment. A model could learn topic-specific heuristics from FOLIO that do not transfer to technical specification reasoning. FOLIO accuracy measures general logical reasoning in familiar narrative registers, not reasoning in the normalized "shall/should" requirements-language register used by defense engineers.
- **Datapoint citations:**
  - [D23] Example 6 (yale-nlp/FOLIO, split=train, label=Uncertain): "Everyone at the business conference who is an ardent communist prefers state ownership of the means of production." — Political philosophy scenario with no engineering relevance.
  - [D22] Example 38 (yale-nlp/FOLIO, split=train, label=False): "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination." — Consumer/social scenario; contemporary brand reference.
  - [D26] Example 7 (yale-nlp/FOLIO, split=train, label=Uncertain): "Andy Chang is from Hong Kong." — Named individual from Wikipedia; general-knowledge prose.

#### Concern 7: Annotators are CS students/researchers — no systems engineering expertise represented
- **Dimension(s):** OC
- **Observation:** As confirmed by the YAML documentation (Q108, Q111, Q122, Q123), annotators are CS students with formal FOL training. The sample content reflects their background: CS/software examples (story 448 on BFS/queues, story 180 on C++/Python), academic and social settings dominate. No annotator with aerospace, defense, ICD, or requirements engineering background is documented.
- **Deployment relevance:** Ground-truth labels in FOLIO are correct for closed-world logical provability from stated premises — but this is a fundamentally different correctness criterion from "would a practicing systems engineer recognize this as a latent contradiction involving an implicit domain constraint?" The annotator pool lacks the expertise to evaluate the deployment's actual task.
- **Datapoint citations:**
  - [D9] Example 46 (yale-nlp/FOLIO, split=train, label=Uncertain): "Everyone that knows about breath-first-search knows how to use a queue." — CS-domain content consistent with annotator background; no engineering specification domain.
  - [D14] Example 16 (yale-nlp/FOLIO, split=train, label=True): "All Olympic gold medal winners are professional athletes. No full-time scientists spend the majority of their time on sports." — Accurate label from logical provability perspective, but annotators have no basis to evaluate domain-convention conflicts in engineering specifications.

---

#### MINOR

#### Concern 8: Short-story input format — no evaluation of long-context or multi-section document handling
- **Dimension(s):** IF
- **Observation:** Premises in the sample range from 2 sentences (Ex. 1, Ex. 12, Ex. 50) to approximately 8–9 sentences (Ex. 2, Ex. 21, Ex. 57). No example approaches the multi-thousand-word, multi-section input format of a real specification document. The benchmark does not evaluate any form of long-document processing.
- **Deployment relevance:** Target documents are 20,000–250,000+ words. FOLIO's short stories (estimated 50–200 tokens per example) cannot assess whether a model maintains reasoning quality at the document lengths encountered in deployment. This is a structural gap in IF, though the benchmark documentation already acknowledges it.
- **Datapoint citations:**
  - [D1] Example 1 (yale-nlp/FOLIO, split=train, label=True): "No plants are fungi. Mushrooms are fungi." — Two-sentence premise set; represents minimal possible input complexity relative to deployment documents.
  - [D2] Example 2 (yale-nlp/FOLIO, split=train, label=Uncertain): Full premises span approximately 7 sentences and ~180 words — still orders of magnitude shorter than a system-level SRD.

#### Concern 9: "Uncertain" label semantics do not match deployment's actionable uncertainty requirement
- **Dimension(s):** OO
- **Observation:** FOLIO's "Uncertain" (labeled "Uncertain" in the data, not "Unknown" as in some documentation) means the conclusion is not provable in either direction from the stated closed-world premises — formal undecidability. In the deployment, an "Uncertain" output must be accompanied by a statement of what additional information would resolve the ambiguity (e.g., "the content of MIL-STD-461F Section 4.3 is needed to determine if this requirement conflicts"). These are different concepts with different user actions required.
- **Deployment relevance:** Models evaluated on FOLIO's Uncertain label learn to recognize closed-world undecidability, not to reason about what missing information would resolve an open-world conflict. An "Uncertain" output without a resolution path is described as a tool failure for this deployment.
- **Datapoint citations:**
  - [D25] Example 50 (yale-nlp/FOLIO, split=train, label=Uncertain): "Each building is tall. Everything tall has height." with conclusion "All buildings are magnificent." — Uncertain because "magnificent" is not in the premise vocabulary at all; no resolution path is possible or expected in FOLIO's framework.
  - [D5] Example 22 (yale-nlp/FOLIO, split=train, label=Uncertain): "Mei is at the Franco-China diplomatic conference… Either Mei is a North Korean and can have medical bills partially covered, or neither is true." — Uncertain because Mei's nationality is underdetermined; in the deployment context, this would require a statement like "the specific text of section X would resolve this."

#### Concern 10: Some NL content uses real named entities that may create Wikipedia contamination confounds
- **Dimension(s):** IC
- **Observation:** Several WikiLogic examples reference real-world entities by name: Michael O'Donnell (British physician/broadcaster, story 70), Bobby Flynn (Australian Idol contestant, story 89), the Croton River (story 12), Oxford Circus (story 205), and PSO J318.5−22 (rogue planet, story 377). LLMs that have processed Wikipedia may have seen related content.
- **Deployment relevance:** In the deployment context, this contamination concern is somewhat less relevant since the deployment goal is not benchmark leaderboard performance — but it does mean FOLIO scores may overestimate reasoning capability for novel technical content that LLMs have not encountered.
- **Datapoint citations:**
  - [D26] Example 7 (yale-nlp/FOLIO, split=train, label=Uncertain): "Andy Chang directed EndGame. Andy Chang is from Hong Kong." — Real or Wikipedia-plausible person; LLMs may have pretraining signal about this entity.
  - [D24] Example 29 (yale-nlp/FOLIO, split=train, label=False): "The only types of mammals that lay eggs are either platypuses or echidnas. … Grebes lay eggs. Grebes are not platypuses and also not echidnas." — Uses real biological facts from Wikipedia; model may answer from world knowledge rather than logical inference.

---

### Content Coverage Summary

The 57 sampled examples span a wide range of everyday and academic topics: sports (basketball, Olympic athletes), consumer technology (TikTok, Meta, products), biology (mammals, plants, fish), geography (New York, London, Guilin), film and media, economics (monetary policy, embargo), philosophy (inductive/deductive reasoning), and social scenarios (family, travel, parties). Two examples touch CS/software domains (BFS/queues; C++/Python projects) but remain fully domain-neutral.

Every example is structured as a compact self-contained "world" with 2–9 explicit premises followed by one conclusion to be evaluated as True, False, or Uncertain. Premises are grammatical English prose supported by parallel FOL annotations using standard logical operators (∧, ∨, ⊕, →, ¬, ∀, ∃). The register is informal general English, completely absent of requirements-language conventions ("shall," "should," standards identifiers).

A small number of annotation quality issues are observable in the sample: at least one NL/FOL name inconsistency (John vs. jim in story 337), one NL/FOL semantic inconsistency (Matt's investment status in story 362), and several FOL parenthesis errors (stories 362, 391, 422). These suggest the annotation process, while largely rigorous, is not error-free at the individual example level.

---

### Limitations

- **Sample size:** 57 examples from 1,001 training examples (~5.7%). The observed annotation error rate (~3–4 examples with identifiable issues) may not be representative of the full dataset.
- **Test split not accessible:** The HF schema shows only `train` and `validation` splits publicly; the test split (226 examples) is not in the viewer. Benchmark accuracy results in the literature are reported on test; this analysis covers only training examples.
- **No validation split reviewed:** The 203 validation examples were not sampled; topic or complexity distribution may differ.
- **HybLogic vs. WikiLogic proportions:** The sample may oversample one pipeline; the relative proportion of the two pipeline types in the 57 examples was not directly verifiable from the data alone.
- **FOL annotation correctness:** Syntactic issues in the FOL were identifiable by inspection, but semantic correctness of FOL translations (NL–FOL alignment) cannot be fully assessed without running the inference engine.
- **Explanation quality:** FOLIO has no explanation field; the downstream scoring module cannot assess the quality of model-generated explanations from this dataset, only classification accuracy.

