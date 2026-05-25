## Deployment Context

We are a US consulting firm evaluating whether an LLM can help American management consultants build persuasive business cases. The system should assemble evidence, structure arguments, anticipate counterarguments, and tailor reasoning to executive audiences. We need to evaluate the LLM's reasoning capabilities for argument construction in a business context.

# Validity Analysis: folio
**Target context:** US Management Consulting — Business Case Reasoning
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content | 2 | Significant gaps | high |
| Output Form ⚠ | 1 | Serious concern | high |
| **Average** | **1.7** | | |

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

FOLIO is a rigorous, internally well-validated benchmark for formal first-order-logic deductive reasoning in closed-world settings. For the target deployment — US management consultants constructing business cases — it is fundamentally misaligned across five of six dimensions. Four HIGH-priority dimensions (IO, IC, OO, OF) and one MODERATE-priority dimension (OC) show severe construct underrepresentation or categorical mismatch with deployment requirements. The consulting deployment requires inductive, abductive, analogical, and rhetorical reasoning over real-world business domain content, producing long-form audience-calibrated argumentative text evaluated by engagement partner professional judgment. FOLIO provides none of these: it tests only deductive classification on domain-knowledge-free closed logical worlds, producing discrete True/False/Unknown labels evaluated by an FOL inference engine. The only well-aligned dimension is Input Form (text-only English), which was marked LOWER priority precisely because alignment was expected. Dataset inspection confirms all documentation-level concerns empirically: even FOLIO examples using business vocabulary (Meta, Google, monetary policy, Wall Street Journal, supply chain) use those terms as arbitrary predicate labels with no business knowledge tested. FOLIO is a clean baseline for the small deductive sub-component of consulting reasoning, but it provides no signal on the dominant capabilities the deployment requires.

## Practical Guidance

### What This Benchmark Measures

FOLIO measures a model's ability to perform multi-step formal deductive reasoning in closed logical worlds, evaluated as discrete True/False/Unknown classification against FOL-prover ground truth. For the consulting deployment, this corresponds only to the deductive sub-component of argument-chain validity — a minor part of the full reasoning task per elicitation A1. The strongest dimension (Input Form, text-only English) is necessary but not sufficient evidence of fit.

### Construct Depth

Construct coverage is narrow but deep within its frame: FOLIO probes deductive reasoning across 4,351-word vocabulary, with up to 7+ reasoning steps, and challenges frontier LLMs (GPT-4 near-chance on HybLogic). It provides a documented, non-trivial floor assessment for deductive validity. However, for inductive, abductive, analogical, and rhetorical reasoning — the dominant consulting modes — FOLIO provides zero signal. For business domain knowledge, output ontology fit, and output-form generation, the benchmark is structurally incapable of providing evidence.

### What Else You Need

Substantial supplementation is required: (1) for Input Ontology gaps, multi-reasoning-type benchmarks (WEB-2, WEB-3) or development of a consulting-specific inductive/abductive scenario benchmark; (2) for Input Content gaps, financial domain benchmarks (FinQA, FIRE, BizFinBench, FinBen — WEB-4, WEB-5, WEB-7, WEB-8, WEB-9) plus US regulatory content evaluation aligned to CCPA/CPRA, SEC/FINRA; (3) for Output Ontology and Output Form, rubric-based long-form evaluation frameworks (RubricRAG, RRD — WEB-13, WEB-14) adapted with engagement-partner-derived quality dimensions, mindful of LLM-as-judge persuasive-language inflation risk (WEB-27); (4) for Output Content, a human-in-the-loop engagement-partner review pipeline. No off-the-shelf consulting argument quality benchmark exists (gap_id 5, NOT FOUND), so partner-annotated evaluation infrastructure must be built.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's task taxonomy is restricted to formal deductive reasoning in closed logical worlds [Q15], with a fixed FOL operator set [Q138] and explicit exclusion of temporal and modal logics [Q139, Q140]. The elicitation explicitly states that strict deductive reasoning is a small minority of the consulting task, with inductive, abductive, analogical, and rhetorical reasoning dominating. Dataset inspection confirms that all 57 sampled examples are strictly deductive — even the example that names 'inductive reasoning' in its premises is evaluated through deductive classification [D11]. This is a HIGH-priority dimension per elicitation, and the mismatch is categorical: FOLIO provides zero signal on the dominant reasoning modes for this deployment.

**Strengths:**
- Provides a documented, non-trivial floor assessment for the deductive sub-component of consulting reasoning; multi-step chains up to 7+ premises are present [Q60, D24], and GPT-4 performance is near-chance on HybLogic [Q20], confirming the deductive task is not saturated.
- Logical structural diversity (large AST count, [Q61]) ensures the deductive sub-component is probed across varied forms rather than a single template.

**Checklist:**

- **IO-1**: Consulting deployment requires inductive (market sizing from partial data), abductive (best-explanation inference), analogical (comparable engagement pattern-matching), and rhetorical (audience-calibrated argument construction) reasoning, with deductive reasoning as a minor secondary component. Per elicitation A1 and dimension priority weights.
- **IO-2**: Yes. FOLIO explicitly covers only formal deductive reasoning [Q15, Q63] with a standard FOL operator set [Q138]; temporal and modal logics are explicitly out of scope [Q139, Q140]. Inductive, abductive, analogical, and rhetorical reasoning are entirely absent. WEB-2 documents that frontier LLMs perform meaningfully differently across reasoning types, confirming these are distinct evaluable capabilities that FOLIO does not test. — _Sources: Q15, Q63, Q138, Q139, Q140, WEB-2, D11_
- **IO-3**: FOLIO's category coverage is narrow rather than irrelevant — formal deductive reasoning is a legitimate (though minor) component of consulting argument construction. The benchmark does not include categories that are actively misleading for this deployment, but it does require the strong assumption that closed-world deductive validity is a meaningful proxy for consulting reasoning ability, which the elicitation rejects. — _Sources: Q15_
- **IO-4**: Construct underrepresentation is severe: four of five reasoning modes required by the deployment are absent. Documented gap; the elicitation explicitly confirms (A1) that deductive reasoning is a small minority of the consulting task. No business reasoning benchmark covering inductive/abductive/analogical reasoning at the consulting scenario level was found [WEB-2, WEB-3, WEB-23]. — _Sources: D8, D11, D7, WEB-2, WEB-3, WEB-23_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q15] 'a natural language reasoning dataset, FOLIO, with first-order logic reasoning problems which require the models to decide the correctness of conclusions given a world defined by the premises' (p.1)
- [Q138] 'We include the following operators: negation ¬, conjunction ∧, disjunction ∨, implication →, universal quantifier ∀, existential quantifier ∃, equal =.' (p.13)
- [Q139] 'Following (Russell and Norvig, 2010), we consider temporal logic and modal logic as special-purpose logics.' (p.13)
- [Q140] '[temporal and modal logics] are beyond the scope of the definition of first-order logic used in our dataset.' (p.13)
- [Q63] 'We define two new tasks based on FOLIO, natural language reasoning with first-order logic and NL-FOL translation.' (p.6)

*Web sources:*
- [WEB-2] Multi-reasoning benchmark shows frontier LLMs score 87.67% on abductive vs 72–78% on deductive, confirming distinct capabilities not jointly tested by FOLIO
- [WEB-3] Inductive/abductive benchmark degrades sharply with ontology complexity, demonstrating these are distinct evaluable reasoning modes absent from FOLIO
- [WEB-23] No business-context inductive/abductive reasoning benchmark found at the consulting-scenario level

*Dataset analysis:*
- DATASET-D8: 'Size Town' fictional categorical world epitomizes closed-world deductive design — no incompleteness, uncertainty, or explanatory inference
- DATASET-D11: Benchmark names inductive reasoning in its premise content but evaluates only deductive classification — the benchmark cannot evaluate the reasoning type it discusses
- DATASET-D7: Closed-world binary choice with fully specified premises; nothing analogous to inferring market opportunity from partial signals
- DATASET-D24: 6-premise chain with nested implications demonstrates deductive depth but no reasoning-mode diversity

</details>

**Information gaps:**
- No FOLIO documentation addresses how deductive validity correlates with performance on inductive/abductive/rhetorical reasoning tasks; transfer of FOLIO performance to non-deductive reasoning is unknown.

**Requires expert verification:**
- Engagement partner verification of the exact ratio of deductive vs non-deductive reasoning across representative consulting deliverables would refine the magnitude of IO underrepresentation.

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's content design explicitly excludes domain-specific knowledge: WikiLogic stories are written from scratch using Wikipedia seeds with no domain-specific knowledge requirement [Q34, Q35], and the paper itself acknowledges that none of the prior benchmarks (and by extension FOLIO) 'are written by humans with information drawn from real-world knowledge, making them less applicable to real-world reasoning scenarios' [Q14]. Dataset inspection confirms that even examples with business-adjacent vocabulary (Meta, Google, Walmart, Wall Street Journal, monetary policy) use these terms as arbitrary predicate labels rather than testable domain knowledge [D2, D3, D6, D15, D20]. The elicitation marks IC as HIGH priority and confirms the deployment is 'deeply' dependent on real-world business domain knowledge — a full content mismatch.

**Strengths:**
- Topical breadth (4,351-word vocabulary, 74% from WikiLogic) [Q62] and explicit screening for bias/stereotypes [Q47, Q127] mean the content is not actively misaligned with US norms even though it provides no business grounding.
- Annotation effort (980 man-hours [Q32], 39.2% rewrite rate [Q48]) yields high-quality input prose suitable as a clean deductive testbed.

**Checklist:**

- **IC-1**: The deployment requires deep region-specific business domain knowledge — financial metrics, sector benchmarks, US regulatory context (e.g., CCPA/CPRA [WEB-17, WEB-18], SEC/FINRA model risk principles [WEB-20]), and competitive dynamics. FOLIO inputs require none of these. — _Sources: WEB-17, WEB-18, WEB-20_
- **IC-2**: Content is screened for bias and stereotypes [Q47, Q127] and uses 'psychologically fundamental generalizations' rather than identity-tied stereotypes [Q128]. No active cultural misalignment with US deployment, but no positive alignment either — content is largely domain-neutral with fictional and non-US settings (Guilin, Potterville, Franco-China conference) [D8, D9, D12]. — _Sources: Q47, Q127, Q128, D8, D9, D12_
- **IC-3**: Western-specific knowledge is not particularly required by FOLIO inputs; the closed-world design means cultural transfer is largely irrelevant. Named entities like Meta, Google, Wall Street Journal appear but function as logical constants only [D20, D3]. — _Sources: D20, D3_
- **IC-4**: INSUFFICIENT DOCUMENTATION on regional annotator review of cultural sensitivity. Would need US business-professional review of the subset of FOLIO examples using business vocabulary to confirm no inadvertent misrepresentation, though dataset analysis suggests vocabulary is cosmetic and unlikely to mislead.
- **IC-5**: Content gap is severe: FOLIO explicitly excludes domain knowledge [Q14, Q34, Q35] while the deployment depends entirely on it (elicitation A3). Multiple financial/business benchmarks (FinQA, FIRE, BizFinBench, FinBen) exist that better approximate domain content [WEB-4, WEB-5, WEB-7, WEB-8, WEB-9] but none target consulting argument construction. Construct-irrelevant variance is minimal; construct underrepresentation is total. — _Sources: Q14, Q34, Q35, D2, D3, D6, D15, WEB-4, WEB-5, WEB-7, WEB-8, WEB-9_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q14] 'none of them are written by humans with information drawn from real-world knowledge, making them less applicable to real-world reasoning scenarios' (p.1)
- [Q34] 'WikiLogic: annotation from scratch using Wikipedia articles as seeds... The Wikipedia articles are used to develop ideas for topics to write new stories.' (p.4)
- [Q35] 'We ask the annotators to create new stories from scratch without using templates based on real-world knowledge, which should be plausible in general.' (p.4)
- [Q47] 'Our dataset prioritizes realism and factual accuracy, steering clear of biases and stereotypes linked to identity markers like race, ethnicity, gender, sexuality, nationality, class, and religion.' (p.4)
- [Q62] 'our dataset has a vocabulary of 4,351 words' (p.5)

*Web sources:*
- [WEB-5] FinanceQA covers professional financial analysis tasks — a domain content layer FOLIO entirely lacks
- [WEB-7] FIRE benchmark covers market analysis, risk assessment, investment strategy with rubric-scored open-ended items
- [WEB-8] BizFinBench covers business-driven adversarial financial tasks
- [WEB-9] FinBen covers 42 financial datasets across 24 tasks
- [WEB-17] US privacy law patchwork (20 state laws) creates regulatory content domain consultants must reason over — entirely absent from FOLIO

*Dataset analysis:*
- DATASET-D2: Monetary policy / Russian embargo example uses macroeconomic vocabulary but answer derives by pure closed-world deduction; no economics knowledge tested
- DATASET-D3: 'Wall Street Journal' and 'financial metrics' appear as opaque predicate labels with no financial knowledge engaged
- DATASET-D6: Supply-chain framing with no real supply-chain knowledge required
- DATASET-D15: 'Seasoned software engineer at Google' is a location predicate with no Google domain knowledge tested
- DATASET-D20: 'Meta' functions as named constant; no knowledge of Meta or commuting patterns required
- DATASET-D16: 'Rouge Dior' product attributes used as arbitrary categorical predicates; no cosmetics domain knowledge tested
- DATASET-D8: Fully fictional 'Size Town' world — paradigmatic of FOLIO's closed-world domain-free design

</details>

**Information gaps:**
- Whether any subset of FOLIO inadvertently tests latent business knowledge through pattern-matching on training-corpus business text is not documented; [Q104] notes contamination risk for WikiLogic generally but not for business-vocabulary subsets specifically.

**Requires expert verification:**
- Practitioner review confirming that no FOLIO subset can serve as a partial proxy for any business-knowledge component would be useful for completeness; dataset analysis already suggests not.

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
FOLIO is text-only in well-formed American English, with grammar reviewed by Grammarly and English Literature specialists [Q49, Q50], using naturalistic quantifier and connective phrasing [Q130–Q133]. The consulting deployment is also text-only English with executive register requirements. There is no script, modality, or encoding mismatch. The main residual concern is register: FOLIO's prose is naturalistic narrative rather than executive business register, but this is a relatively minor form gap given both contexts are text-only English. The dimension is marked LOWER priority in the elicitation.

**Strengths:**
- Clean, grammatically reviewed English prose [Q49, Q50] with idiomatic logical phrasing [Q130–Q133] aligns with business writing conventions at the sentence level.
- Dataset inspection confirms uniform high-quality American English prose across all sampled examples; no encoding, script, or naturalness issues observed [D10, D3].
- Premise ordering robustness was tested [Q158–Q160], reducing concerns that input form artifacts drive results.

**Checklist:**

- **IF-1**: Both benchmark and deployment are text-only English; no signal distribution mismatch [Q22, Q64, Q65]. Dataset inspection confirms uniformly natural sentence-level English across all sampled examples. — _Sources: Q22, Q64, Q65, D10_
- **IF-2**: Regional infrastructure (US enterprise consulting firm with high-bandwidth connectivity and standard desktop workstations) trivially supports text-only English input/output. No infrastructure gap. — _Sources: WEB-15_
- **IF-3**: Domain-specific form considerations: consulting outputs often include structured frameworks (2x2 matrices, waterfall analyses described in prose) and financial notation that FOLIO does not test on the input side. The benchmark prose is narrative rather than executive business register, but at the input level this is a minor gap. — _Sources: D3, D10_
- **IF-4**: External validity for input form is largely preserved. Minor residual concern: FOLIO does not test register variation (analyst vs. executive prose) or structured business document inputs (memos, term sheets, financial tables), but this is below the threshold for a significant validity violation given the LOWER priority weighting. — _Sources: Q49, Q50_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'We use formal logic, i.e., FOL to ensure the logical validity of the examples written in NL and propose a new NL-FOL translation task.' (p.2)
- [Q49] 'All the sentences are first checked with a grammar checking tool, Grammarly.' (p.4)
- [Q50] 'Our annotators who have graduated from or are senior students studying English Literature conducted a thorough round of review for grammatical correctness and language naturalness.' (p.4)
- [Q130] 'We always use either-or to express exclusive disjunction.' (p.13)
- [Q131] 'We use either A or B or A or B, or both to express inclusive disjunction.' (p.13)

*Web sources:*
- [WEB-15] Enterprise consulting LLM deployment is text-only via commercial API + RAG — matches FOLIO's text-only form

*Dataset analysis:*
- DATASET-D10: Natural quantifier phrasing ('all,' 'no') mirrors business writing conventions
- DATASET-D3: Natural conditional phrasing in a quasi-business context confirms register at sentence level is acceptable

</details>

**Information gaps:**
- No FOLIO evaluation of inputs with embedded tables, financial notation, or structured frameworks that may appear in consulting workflows; impact is likely minor for the input-form dimension specifically.

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's output ontology is a discrete three-way classification label (True/False/Unknown) reflecting closed-world logical validity [Q36, Q66], plus FOL formula strings for the translation subtask [Q73–Q76]. The elicitation marks OO as HIGH priority and identifies persuasiveness, narrative coherence, objection anticipation, executive-audience calibration, evidence selection quality, and confidence calibration as the operative success criteria — none of which appear in FOLIO's output taxonomy. The benchmark's ground truth is an FOL inference engine [Q2, Q57]; the deployment's ground truth is engagement partner professional judgment. Dataset inspection confirms every example terminates in a single classification label with no mechanism for evaluating argument construction [D9, D13, D18]. This is a categorical structural validity violation. The Unknown label's epistemic-humility analog [D18, D25] is a narrow strength but does not redeem the broader mismatch.

**Strengths:**
- Three-way True/False/Unknown taxonomy captures absence-of-evidence as a distinct epistemic state [Q66, D18, D25], conceptually analogous to consulting need to flag what evidence does not support.
- FOL representation is unambiguous and mechanically verifiable [Q135, Q136, Q137], providing internally rigorous ground truth within its own frame.

**Checklist:**

- **OO-1**: FOLIO output categories (True/False/Unknown) do not include persuasiveness, narrative coherence, objection anticipation, executive-audience framing, evidence selection quality, or appropriate confidence calibration — all of which are operative quality dimensions in the consulting deployment per elicitation A2. — _Sources: Q36, Q66, Q94_
- **OO-2**: Missing categories: rhetorical effectiveness, argument structure quality, audience calibration. ArgBench [WEB-10] documents an output ontology for argument quality including rhetoric, cogency, and effectiveness across 46 tasks; FOLIO covers none of these dimensions. — _Sources: WEB-10, WEB-11, D9, D13_
- **OO-3**: The FOLIO ontology encodes the assumption that logical validity is the relevant decision rule for evaluating a reasoning system's output. For the consulting deployment, this assumption is rejected by the elicitation: validity is necessary but insufficient. The category structure embeds a formal-deductive value system orthogonal to the consulting deployment's quality criteria. — _Sources: Q135, Q136, Q2_
- **OO-4**: Stakeholder-driven taxonomy redesign is necessary. The deployment requires rubric-based evaluation of long-form argumentative output [WEB-13, WEB-14] with engagement-partner-derived criteria. No off-the-shelf consulting argument quality taxonomy exists [WEB-12 NOT FOUND result for consulting-specific benchmarks]. — _Sources: WEB-13, WEB-14_
- **OO-5**: Structural validity is severely compromised: the construct's structure (multi-dimensional argument quality) is represented as a single discrete logical-validity label. Content validity is severely compromised: missing categories cover the dominant success criteria. External validity is severely compromised: benchmark performance does not generalize to partner-review outcomes. — _Sources: Q66, D18, WEB-10, WEB-27_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q36] 'Each of the stories is composed of several premises and conclusions with truth values of True, False, or Unknown' (p.4)
- [Q66] 'Given P and H, the goal is to determine the truth values of the conclusions: True, False or Unknown, based on FOL reasoning.' (p.6)
- [Q2] 'The logical correctness of the premises and conclusions is ensured by their FOL annotations, which are automatically verified by an FOL inference engine.' (p.1)
- [Q135] 'FOL enables deriving facts from other facts' (p.13)
- [Q136] 'FOL... can be used as input to an FOL prover in order to obtain the exact truth values for the conclusions.' (p.13)
- [Q94] 'The majority baseline of our dataset is 38.5% since in our test set, there are 87, 78 and 61 examples with labels of true, false and unknown respectively.' (p.7)

*Web sources:*
- [WEB-10] ArgBench provides argument quality output ontology (rhetoric, cogency, effectiveness across 46 tasks) — FOLIO covers none of these
- [WEB-11] Argument quality assessment requires cogency/effectiveness/robustness dimensions, not present in FOLIO
- [WEB-13] RubricRAG rubric-based evaluation framework for open-ended long-form outputs — closer to what consulting evaluation requires
- [WEB-27] LLM-as-judge persuasive-language inflation risk (up to 8% score inflation) is a critical evaluation design concern absent from FOLIO's classification ontology

*Dataset analysis:*
- DATASET-D9: Same story yields three independently classified conclusions with no mechanism to synthesize into a coherent argument or evaluate framing
- DATASET-D13: Three conclusions from the Yale basketball story scored as separate classification labels — no evaluation of how findings would be presented or structured for a client
- DATASET-D18: Single-word classification label suffices as entire output; no narrative structure, evidence selection, or audience calibration possible or evaluated
- DATASET-D25: Demonstrates Unknown label for unrelated conclusions — narrow conceptual analog to flagging insufficient evidence

</details>

**Information gaps:**
- Engagement partner-derived rubric structure for consulting argument quality is not documented in any source found; primary stakeholder elicitation would be required to define the missing taxonomy.

**Requires expert verification:**
- Engagement partner specification of the canonical quality-dimension taxonomy for consulting deliverables (e.g., a formal rubric capturing persuasiveness, evidence selection, framing, objection anticipation).

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
FOLIO's labels are generated through a rigorous multi-stage pipeline: parallel NL+FOL annotation by trained annotators [Q17, Q25–Q31], FOL expert review [Q29, Q125], and automated FOL inference engine verification [Q2, Q57]. Within the FOL-validity frame, labels are internally rigorous — but this is structurally orthogonal to the deployment's ground truth (engagement partner professional judgment). The 34.16% expert vs. non-expert gap [Q111] confirms labels measure a specialist FOL skill, not business reasoning. Annotators are CS students familiar with FOL [Q108], native English speakers [Q27, Q110] — no business professionals, consulting practitioners, or management domain experts in the annotator pool. WEB-12 documents LLM-judge agreement with domain experts drops to 64–68% vs. inter-expert baselines of 72–75%, concentrated on factual accuracy, actionability, and tone — precisely the dimensions partner review targets. The score is 2 rather than 1 because the labels are not wrong within their frame; they are simply correlated with a different construct than the deployment requires. Dataset inspection also revealed a minor annotation inconsistency (John/Jim name mismatch in D21) that the FOL prover did not catch.

**Strengths:**
- Rigorous multi-stage annotation pipeline with FOL-expert review and automated inference-engine verification [Q2, Q17, Q57] produces high-reliability labels within the formal-logic frame.
- Documented human expert ceiling (95.98% [Q111]) and expert/non-expert gap (34.16%) establish that label noise is low and the task discriminates skill levels — useful for the deductive sub-component baseline.
- All annotators native or near-native English speakers [Q27, Q110] reduces language-noise risk in label assignment.

**Checklist:**

- **OC-1**: FOLIO ground-truth labels reflect FOL prover output, not consulting practitioner perspectives. The elicitation explicitly states partner judgment — not formal logical validity — is the operative ground truth. — _Sources: Q2, Q57_
- **OC-2**: High potential disagreement on what 'correct output' means: a model could produce FOLIO-correct deductive classifications while failing partner review for poor framing, weak evidence selection, or inappropriate confidence. The 34.16% non-expert/expert gap [Q111] is for FOL-skill annotators; no consulting practitioner annotation exists. WEB-12 documents 64–68% LLM-judge/expert agreement on domain-expert tasks. — _Sources: Q111, WEB-12, D19_
- **OC-3**: Annotator demographics: native or near-native English speakers [Q27, Q110]; CS undergraduate/graduate students or researchers with FOL training [Q31, Q108, Q123]; expert review by NLP/computational linguistics or FOL experts [Q124, Q125]. No business or consulting practitioners documented. — _Sources: Q27, Q108, Q123, Q124, Q125_
- **OC-4**: Re-annotation by consulting practitioners would be necessary for valid OC alignment, but is structurally limited because the underlying output ontology (classification labels) cannot represent the dimensions consulting practitioners would evaluate. The mismatch is more fundamental than label re-annotation can remedy. — _Sources: WEB-12_
- **OC-5**: Aggregation: labels are determined by FOL inference engine output [Q2, Q57], not by majority vote among human annotators, so minority-perspective erasure in the traditional sense does not apply. However, the entire human annotator population is structurally absent from the deployment's stakeholder pool. — _Sources: Q2, Q57_
- **OC-6**: Convergent validity is severely compromised: labels correlate with FOL prover output, not with regional/professional stakeholder judgment. External validity is severely compromised: FOLIO performance does not generalize to consulting partner-review outcomes. WEB-27 also identifies a separate risk that LLM-as-judge evaluation pipelines inflate scores for persuasive but weak arguments by up to 8% — a risk amplified by FOLIO's lack of training in distinguishing rhetorical polish from substantive validity. — _Sources: Q2, WEB-12, WEB-27, D19_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'The logical correctness of the premises and conclusions is ensured by their FOL annotations, which are automatically verified by an FOL inference engine.' (p.1)
- [Q27] 'Our annotators are either college or graduate students who are native English speakers or possess near-native proficiency in English.' (p.3)
- [Q29] 'At the NL quality check stage, only annotators who are experts in natural language processing or computational linguistics are involved. For the FOL quality check, only annotators who are experts in first-order logic are involved.' (p.4)
- [Q57] 'we verify the syntactic validity and label consistency of FOL formula annotations with an FOL inference engine.' (p.5)
- [Q108] 'Our expert annotators are computer science college students familiar with FOL.' (p.9)
- [Q111] 'Expert annotations achieve an accuracy of 95.98% while non-expert annotations achieves 61.82%, with a gap of 34.16%.' (p.9)

*Web sources:*
- [WEB-12] LLM-judge vs domain-expert agreement drops to 64–68% (vs inter-expert 72–75%), concentrated on factual accuracy, actionability, tone — the dimensions partner review prioritizes
- [WEB-27] LLM-as-judge persuasive-language inflation up to 8% score inflation, critical risk if FOLIO-style classification is used to proxy consulting output quality

*Dataset analysis:*
- DATASET-D19: 'No television stars are CPAs / all CPAs have business sense' labeled Uncertain because FOL prover cannot derive 'all TV stars have business sense'; a business-context judgment would ask whether the claim is plausible to investigate — categorically different question
- DATASET-D21: Annotation inconsistency (John in premises, Jim in conclusion) not caught by NL quality check or FOL prover — minor isolated quality issue but indicates pipeline limits on cross-name consistency

</details>

**Information gaps:**
- No published study of inter-rater agreement between FOLIO labels and business-professional judgment on the same examples; the structural orthogonality is inferred from construct definitions rather than measured empirically.

**Requires expert verification:**
- Engagement partner re-annotation of a FOLIO sample under consulting-quality criteria would empirically establish the magnitude of the convergent validity gap, though structural arguments already establish it qualitatively.

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
FOLIO's output form is a discrete three-way classification label evaluated by accuracy [Q80], plus FOL formula strings evaluated for syntactic validity and inference-engine execution accuracy [Q73–Q76]. The deployment requires open-ended, long-form structured argumentative text — business case narratives, executive summaries, recommendation memos. The benchmark has no evaluation infrastructure for natural language generation quality, argument structure, or audience calibration. The paper itself acknowledges 'we leave for future work the design of a more reliable metric of NL-FOL translation' [Q77]. Dataset inspection confirms every example terminates in a single classification label with no free-text output evaluation [D9, D13, D18]. This is HIGH priority per elicitation and a fundamental output-form mismatch.

**Strengths:**
- Robustness checks on premise ordering [Q158–Q160] and confusion-matrix-level reporting [Q155–Q157] provide some methodological rigor within the classification frame.
- Accuracy averaged over five random training samples [Q93] reduces variance in reported deductive-classification performance.

**Checklist:**

- **OF-1**: Output modality mismatch is fundamental: FOLIO produces a discrete True/False/Unknown label or an FOL formula string; the deployment requires long-form structured argumentative natural language text. No FOLIO evaluation infrastructure produces or scores long-form output. WEB-13 and WEB-14 document rubric-based evaluation frameworks (RubricRAG, RRD) as active research directions for the output form the deployment needs, but none are validated for consulting-specific evaluation. — _Sources: Q80, Q73, Q74, Q85, WEB-13, WEB-14, D9, D13, D18_
- **OF-2**: Not applicable to this deployment — text-only input/output is required by the consulting deployment context; no speech requirement.
- **OF-3**: Target population is graduate-educated professionals with high analytical literacy [target_population in YAML]; no literacy or accessibility constraints relevant to output form.
- **OF-4**: External validity for output form is severely compromised: classification accuracy on FOLIO provides no signal on a model's ability to produce partner-reviewable business case narratives. The output-form mismatch is categorical, not gradient. — _Sources: Q80, Q77, WEB-13, D18_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q80] 'We use accuracy for evaluating logical reasoning performance.' (p.6)
- [Q73] 'Two metrics are adopted to evaluate NL-FOL translation to capture different aspects of the generation results: 1). Syntactic validity (SynV).' (p.6)
- [Q74] 'The Syntactic Validity score measures whether the FOL formulas are syntactically valid.' (p.6)
- [Q76] 'We define the accuracy of the output labels as the execution accuracy.' (p.6)
- [Q77] 'We leave for future work the design of a more reliable metric of NL-FOL translation.' (p.6)
- [Q85] 'We fine-tune the base and large versions of both BERT and RoBERTa, with an additional two-layer classification layer to predict the truth values.' (p.7)

*Web sources:*
- [WEB-13] RubricRAG rubric-based long-form output evaluation framework — methodology FOLIO does not employ
- [WEB-14] RRD rubric-based evaluation for long-form outputs — closer to consulting evaluation needs
- [WEB-26] CaseGen legal case document generation with expert-validated rubrics — analog methodology that could transfer to consulting memos but does not exist as a consulting-specific benchmark

*Dataset analysis:*
- DATASET-D9: Three classification labels (Uncertain/Uncertain/False) from one story — no mechanism for synthesizing into coherent argument or evaluating framing
- DATASET-D13: Three independent classification labels from one Yale basketball story — no evaluation of presentation or structure for client
- DATASET-D18: Single classification label suffices as entire output; no narrative structure, evidence selection, or audience calibration possible or evaluated

</details>

**Information gaps:**
- No FOLIO documentation of any extension to long-form natural language output evaluation; [Q77] acknowledges need for better translation metrics but does not address argument-quality evaluation.

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** Inductive, abductive, analogical, and rhetorical reasoning — the dominant consulting modes — are entirely absent from FOLIO's deductive-only taxonomy.

**Recommendation:** Supplement FOLIO with multi-reasoning-type benchmarks (e.g., arXiv:2505.11854, arXiv:2509.03345) and commission a consulting-scenario benchmark that tests market-sizing inference (inductive), best-explanation business signal interpretation (abductive), and comparable-engagement pattern-matching (analogical) with practitioner-derived items.

### Input Ontology ⚠

**Gap:** No coverage of probabilistic/uncertainty reasoning (confidence intervals, scenario analysis) which is present-but-secondary in the deployment.

**Recommendation:** Add scenario-analysis and confidence-calibration evaluation items, potentially drawing on financial scenario benchmarks (FIRE open-ended items) and uncertainty-quantification benchmarks, to cover the secondary reasoning modes FOLIO omits.

### Input Content ⚠

**Gap:** FOLIO excludes real-world domain knowledge by design; the deployment depends entirely on financial, regulatory, sector, and competitive content.

**Recommendation:** Combine FOLIO with domain-grounded financial reasoning benchmarks (FinQA, FIRE, BizFinBench, FinBen) for baseline domain-knowledge signal, and add US-regulatory-context items (CCPA/CPRA, SEC Model Risk, FINRA AI advisory) relevant to consulting sector coverage. Treat FOLIO score in isolation as uninformative for domain reasoning.

### Output Ontology ⚠

**Gap:** FOLIO's three-way logical-validity label does not capture persuasiveness, narrative coherence, objection anticipation, executive-audience calibration, evidence selection, or confidence calibration.

**Recommendation:** Adopt a multi-dimensional argument-quality rubric derived from engagement-partner review criteria, anchored on ArgBench dimensions (rhetoric, cogency, effectiveness) plus consulting-specific axes (CFO/board-register, fiduciary-objection coverage). Treat logical validity as one necessary-but-insufficient dimension, not the full ontology.

### Output Form ⚠

**Gap:** FOLIO produces discrete classification labels; deployment requires open-ended, long-form structured argumentative text. No FOLIO evaluation infrastructure exists for long-form generation.

**Recommendation:** Develop a rubric-based long-form evaluation harness adapting RubricRAG/RRD methodology (WEB-13, WEB-14) and CaseGen-style expert-validated task rubrics (WEB-26) to consulting memos. Score persuasiveness, evidence selection, framing, and objection anticipation as separate axes rather than collapsed into a single quality score.

### Output Content

**Gap:** FOLIO labels are FOL-prover output produced by CS/FOL-expert annotators; no consulting practitioner annotation. Convergent validity with partner judgment is unestablished and structurally questionable.

**Recommendation:** Build a human-in-the-loop evaluation pipeline with engagement partner annotation as ground truth for a sample of deployment-representative outputs. Calibrate LLM-as-judge pipelines against this expert pool, and explicitly test for persuasive-language score inflation (WEB-27) before relying on automated scoring.

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
| Q98 | 8 | input_ontology | "Below we provide analysis of our results and key findings, providing additional insights into our dataset FOLIO and the current capabilities of LLMs in logical reasoning." |
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
| Q161 | 15 | output_form | "FOL formulas have a clearer and more straightforward logical structure than NL sentences." |
| Q162 | 15 | output_form | "As shown in Table 11, the performance slightly increases in the NL+FOL setting for GPT-4 while GPT-3.5 performs worse in both the NL+FOL and the FOL-only settings." |
| Q163 | 15 | output_form | "FOL always serves as additional useful information for GPT-4, but not for GPT-3.5 regardless of whether FOL is concatenated with NL." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://bloomberry.com/blog/the-state-of-enterprise-ai-adoption/ |
| WEB-2 | https://arxiv.org/pdf/2505.11854 |
| WEB-3 | https://arxiv.org/pdf/2509.03345 |
| WEB-4 | https://awesomeagents.ai/leaderboards/finance-llm-leaderboard/ |
| WEB-5 | https://arxiv.org/pdf/2501.18062 |
| WEB-6 | https://arxiv.org/pdf/2509.04468 |
| WEB-7 | https://arxiv.org/pdf/2602.22273 |
| WEB-8 | https://arxiv.org/pdf/2505.19457 |
| WEB-9 | https://proceedings.neurips.cc/paper_files/paper/2024/file/adb1d9fa8be4576d28703b396b82ba1b-Paper-Datasets_and_Benchmarks_Track.pdf |
| WEB-10 | https://arxiv.org/abs/2604.17366 |
| WEB-11 | https://arxiv.org/pdf/2403.16084 |
| WEB-12 | https://www.emergentmind.com/topics/llm-judge-evaluation |
| WEB-13 | https://arxiv.org/html/2603.20882v1 |
| WEB-14 | https://arxiv.org/pdf/2602.05125 |
| WEB-15 | https://portkey.ai/blog/enterprise-llm/ |
| WEB-16 | https://www.harmonic.security/resources/what-22-million-enterprise-ai-prompts-reveal-about-shadow-ai-in-2025 |
| WEB-17 | https://iapp.org/resources/article/us-state-privacy-laws-overview |
| WEB-18 | https://www.kolmogorovlaw.com/california-ai-compliance-2025-2026-what-your-business-must-do-now |
| WEB-19 | https://www.wsgr.com/en/insights/cppa-approves-new-ccpa-regulations-on-ai-cybersecurity-and-risk-governance-and-advances-updated-data-broker-regulations.html |
| WEB-20 | https://www.liminal.ai/blog/enterprise-ai-governance-guide |
| WEB-21 | https://www.knostic.ai/blog/ai-governance-best-practices |
| WEB-22 | https://www.cxtoday.com/security-privacy-compliance/enterprise-llm-governance/ |
| WEB-23 | https://arxiv.org/pdf/2406.05506 |
| WEB-24 | https://arxiv.org/pdf/2601.10660 |
| WEB-25 | https://arxiv.org/pdf/2402.08498 |
| WEB-26 | https://arxiv.org/pdf/2502.17943 |
| WEB-27 | https://arxiv.org/pdf/2508.07805 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (default config)
**Analysis date:** 2025-01-31
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | FOLIO | Ex.1 (story_id=271) | True | "No plants are fungi. Mushrooms are fungi." — "No plants are mushrooms." | Minimal 2-premise syllogism; domain-free categorical reasoning | IO, IC |
| D2 | FOLIO | Ex.28 (story_id=252) | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency... There is an embargo on Russian foreign trade goods." | Closest to business domain content in sample; still a closed formal logical puzzle with no quantitative metrics | IC |
| D3 | FOLIO | Ex.57 (story_id=362) | False | "People who like financial risks invest in the public stock market regularly or enjoy gambling regularly. If people invest in the public stock market regularly, then they read the Wall Street Journal and other newspapers regularly to keep updated on financial metrics." | Uses financial-domain vocabulary superficially; logic structure identical to non-business examples | IC, IO |
| D4 | FOLIO | Ex.6 (story_id=423) | Uncertain | "Everyone at the business conference is either an investor or an entrepreneur. None of those at the business conference who enjoy the opportunity of starting a business prefer a planned economy." | Business-themed surface vocabulary masking pure categorical deduction; no business reasoning required | IC |
| D5 | FOLIO | Ex.2 (story_id=376) | Uncertain | "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises... Mike works in this tech company." | Tech-company framing; reasoning purely about personality traits as formal predicates | IC |
| D6 | FOLIO | Ex.14 (story_id=436) | False | "All of this brand's products are either produced in China or in the US. All of this brand's products produced in China are labeled... G-910 is a product of this brand." | Supply-chain vocabulary; conclusion is purely a logical deduction from closed-world rules, no real supply-chain knowledge | IC |
| D7 | FOLIO | Ex.3 (story_id=180) | Uncertain | "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac." | Self-contained narrative; no domain knowledge required or applicable | IO |
| D8 | FOLIO | Ex.11 (story_id=486) | False | "Everything in Size Town is big or small. All big things in Size Town are heavy... The bird is in Size Town and it is not both heavy and still." | Fully abstract fictional-world taxonomy; epitomizes closed-world design | IO, IC |
| D9 | FOLIO | Ex.8/19/30 (story_id=482) | Uncertain/Uncertain/False | "If someone in Potterville yells, then they are not cool. If someone in Potterville is angry, then they yell... Harry, who lives in Potterville either yells or flies." | Fantasy fictional world; single story_id generates multiple conclusions — all evaluated as deductive classification | IO, OO |
| D10 | FOLIO | Ex.16 (story_id=346) | True | "All professional athletes spend most of their time on sports. All Olympic gold medal winners are professional athletes... If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." | Multi-step syllogistic chain; label True by deductive closure | IO |
| D11 | FOLIO | Ex.43 (story_id=393) | True | "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning... Modus Ponens is a component of a major part of reasoning rule." | Ironically, FOLIO uses inductive/deductive reasoning as narrative content, but evaluates it through deductive classification only | IO |
| D12 | FOLIO | Ex.22 (story_id=475) | Uncertain | "Everyone who is entitled to national social insurance coverage can have their medical bills partially covered. All PRC nationals are entitled to national social insurance coverage. Everyone in the Franco-China diplomatic conference is either a PRC national or a French national." | Geopolitical and policy vocabulary; all reasoning is closed-world categorical deduction | IC |
| D13 | FOLIO | Ex.4/18/32 (story_id=408) | False/Uncertain/False | "No trick-shot artist in Yale's varsity team struggles with half court shots... Jack is on Yale's varsity team, and he is either a trick-shot artist or he successfully shoots a high percentage of 3-pointers." | Same story yields 3+ distinct conclusions all scored as discrete True/False/Uncertain labels | OO, OF |
| D14 | FOLIO | Ex.36 (story_id=422) | True | "All customers in James' family who subscribe to AMC A-List are eligible to watch three movies every week without any additional fees... Lily is in James' family; she watches TV series in cinemas." | Consumer-services framing; logic is purely closed-world set membership | IC |
| D15 | FOLIO | Ex.46/47 (story_id=448) | Uncertain/False | "Everyone that knows about breath-first-search knows how to use a queue. If someone is a seasoned software engineer interviewer at Google, then they know what breath-first-search is." | Computer-science professional vocabulary; entirely closed-world deductive | IC |
| D16 | FOLIO | Ex.13/51 (story_id=395) | False/False | "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable... ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." | Consumer product details used as predicate placeholders; no product domain knowledge required | IC |
| D17 | FOLIO | Ex.55 (story_id=477) | False | "All social media applications containing chat features are software... TikTok is a social media application, and it is not ideal for preteens." | TikTok named but reasoning requires no actual knowledge of TikTok; named entity is a logical constant only | IC |
| D18 | FOLIO | Ex.50 (story_id=284) | Uncertain | "Each building is tall. Everything tall has height." — "All buildings are magnificent." | Minimal 2-premise example demonstrating Unknown label for unprovable conclusions | OO |
| D19 | FOLIO | Ex.9 (story_id=264) | Uncertain | "No television stars are certified public accountants. All certified public accountants have good business sense." — "All television stars have good business sense." | Business-adjacent vocabulary; Unknown because the premises don't entail the conclusion | OO |
| D20 | FOLIO | Ex.38 (story_id=425) | False | "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination... James has a car or works at Meta." — "James is a student." | Meta/tech employer named; logic is purely closed-world | IC |
| D21 | FOLIO | Ex.52 (story_id=337) | True | "No athletes never exercise. All professional basketball players are athletes... Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." — "Jim is not a Knicks player." | Contains minor internal inconsistency (premises refer to "John" but conclusion and FOL refer to "Jim") | OC |
| D22 | FOLIO | Ex.31 (story_id=60) | True | "All buildings in New Haven are not high. All buildings managed by Yale Housing are located in New Haven... Tower A is managed by Yale Housing." — "Tower A is low." | 7-premise chain with recognizable US place names; closed-world deductive | IO |
| D23 | FOLIO | Ex.34 (story_id=377) | True | "Everything is either outside the solar system or in the solar system... If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." | Scientific/astronomical vocabulary; multi-step deductive chain; no astronomy knowledge needed | IC |
| D24 | FOLIO | Ex.21 (story_id=381) | False | "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing... If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up." | Complex 6-premise chain; demonstrates benchmark's structural diversity | IO |
| D25 | FOLIO | Ex.56 (story_id=27) | Uncertain | "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin. Yangshuo is not a district in Guilin." — "Kowloon District is in Hong Kong." | Conclusion is entirely unrelated to premises; Unknown because nothing can be deduced | OO |

---

### Deployment-Relevant Strengths

#### Strength 1: Clean English prose with natural logical connective phrasing
- **Dimension(s):** IF
- **Observation:** All 57 examples are grammatically correct, well-formed American English sentences. Logical connectives are expressed in idiomatic forms ("either-or," "if...then," "some," "all") rather than formal symbolic notation, matching the register of professional business writing at the sentence level.
- **Deployment relevance:** The consulting deployment requires text-only English input and output. There is zero script, modality, or encoding mismatch between the benchmark and deployment. This is a genuine, if narrow, strength.
- **Datapoint citations:**
  - [D10] Example 16 (story_id=346, label=True): "All professional athletes spend most of their time on sports. All Olympic gold medal winners are professional athletes. No full-time scientists spend the majority of their time on sports." — Demonstrates natural quantifier phrasing ("all," "no") that mirrors business writing conventions.
  - [D3] Example 57 (story_id=362, label=False): "If people invest in the public stock market regularly, then they read the Wall Street Journal and other newspapers regularly to keep updated on financial metrics." — Natural conditional phrasing in a quasi-business context.

#### Strength 2: Multi-step reasoning chains with documented depth up to 7+ steps
- **Dimension(s):** IO
- **Observation:** Several examples in the sample require extended chains of inference. The story_id=408 examples (D13) involve 5-premise chains with exclusive disjunctions at each step. Story_id=381 (D24) and story_id=448 (D15) require tracking 6–7 premises simultaneously. This multi-step structure corresponds to the deductive sub-component of consulting argument chains.
- **Deployment relevance:** While deductive reasoning is only a minor component of the consulting task, the benchmark's documented difficulty (GPT-4 near-chance on HybLogic) confirms it provides a non-trivial floor assessment for that sub-component.
- **Datapoint citations:**
  - [D13] Examples 4/18/32 (story_id=408): "No trick-shot artist in Yale's varsity team struggles with half court shots. Everyone on Yale's varsity team is someone who struggles with half court shots or who successfully shoots a high percentage of 3-pointers. Everyone on Yale's varsity team who successfully shoots a high percentage of 3-pointers is solid at shooting 2-pointers. No one on Yale's varsity team who is solid at shooting 2-pointers is bad at mid-range shots." — 5-premise chain requiring careful tracking of quantifier scope.
  - [D24] Example 21 (story_id=381, label=False): "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing. If people are fascinated by the history of the Renaissance and other past eras, then they attend Renaissance fairs regularly." — 6-premise chain with nested implications.

#### Strength 3: Three-way label taxonomy catches absence-of-evidence cases
- **Dimension(s):** OO
- **Observation:** The True/False/Unknown trichotomy is a genuine strength relative to binary benchmarks: "Unknown" correctly captures conclusions that are neither provable nor disprovable from given premises. This mirrors the consulting need to distinguish "this follows from the evidence," "this contradicts the evidence," and "the evidence is silent on this."
- **Deployment relevance:** Although the full output ontology is misaligned for the consulting use case, the Unknown category's logic — acknowledging what cannot be inferred from available premises — maps conceptually to epistemic humility in evidence-based business arguments.
- **Datapoint citations:**
  - [D18] Example 50 (story_id=284, label=Uncertain): "Each building is tall. Everything tall has height." — "All buildings are magnificent." — Unknown because "magnificent" is not derivable, illustrating that silence of evidence is a distinct epistemic state.
  - [D25] Example 56 (story_id=27, label=Uncertain): "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin. Yangshuo is not a district in Guilin." — "Kowloon District is in Hong Kong." — Unknown because the premises contain no information about Kowloon or Hong Kong.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Zero business domain knowledge in any content — including surface business-themed examples
- **Dimension(s):** IC
- **Observation:** The 57 sampled examples confirm the documented design choice: even examples using business-adjacent vocabulary (financial risks, stock market, business conference, supply chain, tech company) require zero real-world business knowledge to solve. Every reasoning step is derivable purely from the closed-world premises. Real business content — financial metrics, valuation, competitive dynamics, regulatory context — is entirely absent.
- **Deployment relevance:** The consulting deployment requires LLMs to retrieve, weigh, and integrate real-world financial metrics, sector benchmarks, and competitive dynamics. The most business-adjacent example in the sample (D2, D3) still treats business concepts as arbitrary predicate labels, not as knowledge domains requiring domain expertise.
- **Datapoint citations:**
  - [D2] Example 28 (story_id=252, label=False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. A country cannot simultaneously regulate the exchange rate and successfully control inflation. The introduction of an embargo on foreign trade goods in a country leads to a sharp decrease in exports." — Despite macroeconomic vocabulary, the answer is derived by pure closed-world deduction; no economics knowledge is needed or tested.
  - [D3] Example 57 (story_id=362, label=False): "People who like financial risks invest in the public stock market regularly or enjoy gambling regularly. If people invest in the public stock market regularly, then they read the Wall Street Journal and other newspapers regularly to keep updated on financial metrics." — "Wall Street Journal" and "financial metrics" appear as opaque predicate labels; no financial knowledge is engaged.
  - [D4] Example 6 (story_id=423, label=Uncertain): "Everyone at the business conference is either an investor or an entrepreneur. None of those at the business conference who enjoy the opportunity of starting a business prefer a planned economy." — Business framing is pure decoration; the reasoning is a syllogism about set membership.
  - [D6] Example 14 (story_id=436, label=False): "All of this brand's products are either produced in China or in the US. All of this brand's products produced in China are labeled... None of this brand's products that are returned by customers are sold at Walmart." — Supply-chain vocabulary, but the conclusion ("G-910 is a product returned by customers") is determined entirely by the internal rules, not by any knowledge of retail or supply-chain practices.

#### Concern 2: Entire output ontology is a discrete classification label — no natural language generation evaluated
- **Dimension(s):** OO, OF
- **Observation:** Every example in the dataset terminates in a True/False/Uncertain label. The schema confirms no free-text output field exists. The dataset structure (premises → conclusion → label) is structurally incapable of evaluating open-ended argument construction, narrative coherence, executive-audience framing, or objection anticipation. Multiple conclusions from a single story (D9, D13) are each scored independently as classification labels with no mechanism for evaluating how arguments are synthesized or communicated.
- **Deployment relevance:** The consulting deployment requires the model to produce a complete, structured, partner-reviewable business case narrative — a long-form text output. FOLIO's evaluation infrastructure is entirely classification-based and cannot produce or evaluate any component of that output form.
- **Datapoint citations:**
  - [D9] Examples 8/19/30 (story_id=482): Three distinct conclusions from the Potterville story — "Harry is cool" (Uncertain), "Harry is not cool" (Uncertain), "Harry is a wizard or angry" (False) — each independently classified. There is no mechanism for synthesizing these into a coherent argument or evaluating how they would be framed for an audience.
  - [D13] Examples 4/18/32 (story_id=408): Three conclusions from the Yale basketball story scored as separate classification labels (False, Uncertain, False). No evaluation of how a consultant would present these findings or structure them for a client.
  - [D18] Example 50 (story_id=284, label=Uncertain): "Each building is tall. Everything tall has height." — "All buildings are magnificent." — A single sentence suffices as the entire output; no narrative structure, evidence selection, or audience calibration is possible or evaluated.

#### Concern 3: Reasoning type coverage gap — no inductive, abductive, analogical, or rhetorical reasoning
- **Dimension(s):** IO
- **Observation:** All 57 examples are strictly deductive: given fully specified closed-world premises, determine if the conclusion is entailed, contradicted, or undetermined. Not a single example requires inferring a general principle from partial observations (inductive), identifying the best explanation for a pattern (abductive), drawing on analogous cases (analogical), or calibrating an argument to an audience (rhetorical). Even the one example that uses reasoning-type vocabulary as content (D11, story_id=393) evaluates it through deductive classification.
- **Deployment relevance:** The user explicitly confirmed that strict deductive reasoning is a small minority of the consulting task. The bulk is inductive (market sizing from partial data) and abductive (best-explanation inference from business signals). FOLIO provides zero signal on these dominant reasoning modes.
- **Datapoint citations:**
  - [D8] Example 11 (story_id=486, label=False): "Everything in Size Town is big or small. All big things in Size Town are heavy. All small things in Size Town are light. All heavy things in Size Town are still." — Paradigmatic closed-world deduction; no incompleteness, uncertainty, or explanatory inference.
  - [D11] Example 43 (story_id=393, label=True): "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning." — The benchmark uses inductive reasoning as a named category in premises but evaluates whether a conclusion about Modus Ponens follows deductively. The irony is instructive: the benchmark cannot evaluate the reasoning type it names.
  - [D7] Example 3 (story_id=180, label=Uncertain): "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac. Sam is using a Mac." — Closed world, binary choice, fully specified — nothing analogous to inferring market opportunity from partial signals.
  - [D1] Example 1 (story_id=271, label=True): "No plants are fungi. Mushrooms are fungi." — Minimal syllogism; represents the simplest form of the benchmark's only task type.

---

#### MAJOR

#### Concern 4: Ground-truth labels defined by FOL inference engine, not professional judgment
- **Dimension(s):** OC
- **Observation:** Labels in the dataset are determined by FOL prover output, verified by CS students with formal logic training. The annotator pool (documented as native-English CS undergraduates/graduates) has no overlap with the consulting deployment's evaluative standard: engagement partner professional judgment. The 34.16% accuracy gap between FOL experts and non-experts (documented in the YAML) means the benchmark's human-performance ceiling is a specialist logic skill, not a proxy for professional business reasoning.
- **Deployment relevance:** The user's ground truth is whether an engagement partner would present the output to a client. FOLIO's ground truth is whether an FOL prover returns True/False/Unknown. These two standards are structurally orthogonal. A model that scores well on FOLIO (correct deductive classification) may produce outputs that fail partner review for poor framing, weak evidence selection, or inappropriate confidence level.
- **Datapoint citations:**
  - [D19] Example 9 (story_id=264, label=Uncertain): "No television stars are certified public accountants. All certified public accountants have good business sense." — "All television stars have good business sense." — Labeled Uncertain because the FOL prover cannot derive this from the premises. A business-context judgment would ask whether this is a plausible claim worth investigating — a categorically different question.
  - [D21] Example 52 (story_id=337, label=True): "No athletes never exercise. All professional basketball players are athletes... Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." — "Jim is not a Knicks player." — The premises introduce "John" but the conclusion and FOL annotation refer to "Jim," suggesting a minor annotation inconsistency that the FOL prover may have resolved by treating them as separate constants. A human reviewer would flag this as an error.

#### Concern 5: Surface business/professional vocabulary masks complete absence of domain reasoning
- **Dimension(s):** IC
- **Observation:** Several examples use professional-sounding nouns and contexts (business conference, tech company, Google software engineer, Meta employee, Walmart supply chain, AMC A-List subscriptions, Rouge Dior lipsticks, Wall Street Journal). In every case, these are used purely as arbitrary labels for formal predicates. No example requires or rewards knowing what these concepts actually mean in business practice.
- **Deployment relevance:** A practitioner reviewing the benchmark might initially perceive alignment with business contexts; the surface vocabulary could create a false impression that FOLIO tests business reasoning. Closer inspection confirms the vocabulary is cosmetic — the reasoning structure is identical to abstract examples like "Size Town" (D8) or "Potterville" (D9).
- **Datapoint citations:**
  - [D15] Examples 46/47 (story_id=448): "If someone is a seasoned software engineer interviewer at Google, then they know what breath-first-search is. Someone is either a seasoned software engineer interviewer at Google, has human rights, or both." — "Google" is used as a location predicate; whether Jack is a seasoned software engineer at Google follows from the FOL premises, not from any knowledge of Google's hiring practices.
  - [D20] Example 38 (story_id=425, label=False): "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination." — "Meta" functions as a named constant; the reasoning requires knowing nothing about Meta, high-income workers, or commuting patterns beyond the stated premises.
  - [D16] Examples 13/51 (story_id=395): "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable." — "Rouge Dior" product attributes are used as arbitrary categorical predicates; no cosmetics domain knowledge is tested.

#### Concern 6: Multiple conclusions per story creates test-set redundancy that overstates coverage
- **Dimension(s):** IO, OC
- **Observation:** Three examples from story_id=408 (D13) appear in the sample (examples 4, 18, 32), three from story_id=482 (D9) (examples 8, 19, 30), two from story_id=70 (examples 17, 41), two from story_id=436 (examples 14, 42), two from story_id=395 (examples 13, 51), two from story_id=474 (examples 44, 49), and two from story_id=448 (examples 46, 47). This means a significant portion of the 1,430 examples share premise sets. A model that learns the premise set succeeds on all derived conclusions.
- **Deployment relevance:** For the consulting use case, this redundancy is doubly problematic: it concentrates test signal on a small number of narrative worlds, and it means benchmark accuracy may overstate a model's ability to generalize across diverse reasoning contexts — precisely the generalization that the consulting deployment requires.
- **Datapoint citations:**
  - [D13] Examples 4/18/32 (story_id=408): Three distinct conclusions evaluated from the same 5-premise basketball story. A model memorizing the premise set scores on all three; a model failing the structure fails all three.
  - [D9] Examples 8/19/30 (story_id=482): Three conclusions from the Potterville story (labels: Uncertain, Uncertain, False). All three share the same 7-premise set.

---

#### MINOR

#### Concern 7: Minor annotation inconsistency observed (name mismatch)
- **Dimension(s):** OC
- **Observation:** Example 52 (story_id=337) introduces "John" in the premises ("Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises") but the conclusion and FOL refer to "Jim" ("Jim is not a Knicks player"). This appears to be an annotator error not caught by the FOL prover (which would treat John and Jim as distinct constants).
- **Deployment relevance:** Isolated quality issue; unlikely to affect aggregate validity scores but suggests the annotation pipeline's NL quality check did not catch all name-consistency errors. In a consulting context, such inconsistencies in evidence presentation would fail partner review.
- **Datapoint citations:**
  - [D21] Example 52 (story_id=337, label=True): Premises: "Either John is a professional basketball player and he never exercises..." Conclusion: "Jim is not a Knicks player." FOL: "¬KnicksPlayer(jim)" — John and Jim appear to be intended as the same individual, but the FOL treats them as separate constants.

#### Concern 8: Fictional and non-US content throughout; no US business or regulatory grounding
- **Dimension(s):** IC, IO-2
- **Observation:** The sample includes fictional worlds (Potterville, Size Town), non-US geographies (Guilin, China, Russia, Franco-China diplomatic conference, Australian Idol, Bobby Flynn from Queensland, Hong Kong), and domain-specific non-business content (astronomy, biology, film, cosmetics, literature). US business regulatory or competitive contexts are entirely absent.
- **Deployment relevance:** The deployment is a US consulting firm evaluating LLMs for US business case construction. While geographic diversity is not per se a problem for a pure-logic benchmark, it underscores that no content is calibrated to US business norms, regulatory environments, or competitive dynamics — the raw material of the consulting task.
- **Datapoint citations:**
  - [D12] Example 22 (story_id=475, label=Uncertain): "All PRC nationals are entitled to national social insurance coverage. Everyone in the Franco-China diplomatic conference is either a PRC national or a French national." — Non-US geopolitical context used as predicate domain.
  - [D25] Example 56 (story_id=27, label=Uncertain): "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin. Yangshuo is not a district in Guilin." — Chinese administrative geography as logical domain.
  - [D8] Example 11 (story_id=486, label=False): "Everything in Size Town is big or small." — Completely fictional world with no real-world grounding of any kind.

---

### Content Coverage Summary

The 57 sampled examples confirm FOLIO's documented design across all priority dimensions. Content is exclusively deductive — every example presents a closed set of premises and asks whether a conclusion follows, contradicts, or is undetermined by those premises. The benchmark's topical breadth (biology, astronomy, sports, technology, film, geography, consumer products, quasi-business) is entirely superficial: domain vocabulary functions as interchangeable predicate labels, not as knowledge to be tested.

The most business-proximate examples in the sample (supply chain in story_id=436, monetary policy in story_id=252, financial risks in story_id=362, business conference in story_id=423) all require zero business domain knowledge. The reasoning required is structurally identical to the abstract "Size Town" example. Named entities (Meta, Google, Walmart, Wall Street Journal, Rouge Dior) appear as logical constants with no semantic content beyond what the premises explicitly stipulate.

Label distribution in the sample: 15 True, 13 False, 29 Uncertain — slightly more Uncertain than documented test-set proportions (87/226 ≈ 38.5% True), but consistent with the documented pattern. Output form is uniformly a single-word classification label. No natural language generation, argument structure, narrative coherence, or audience calibration is evaluated anywhere in the dataset.

The benchmark is internally rigorous within its own frame: FOL annotations are consistent, premises and conclusions are well-formed English, and the closed-world evaluation is mechanically sound. The data simply does not correspond to the deployment's evaluation requirements across the four highest-priority dimensions (IO, IC, OO, OF).

---

### Limitations

1. **Sample size:** 57 examples from 1,001 training instances (~5.7% of train split). The validation split (203 examples) and undisclosed test split were not sampled. Coverage characterizations are based on this sample.

2. **No test split accessible via HF viewer:** The schema shows only `train` and `validation` splits available through the HF dataset viewer; the test split (226 examples, the primary evaluation set) is not in the accessible data. All sampled examples are from training.

3. **HybLogic vs. WikiLogic breakdown not observable from data:** The distinction between the two collection methods (template-based vs. Wikipedia-seeded) cannot be reliably determined from the examples alone without the original metadata. The documented performance difference (GPT-4 near-chance on HybLogic vs. better on WikiLogic) cannot be verified from this sample.

4. **FOL annotation quality not independently verifiable:** The FOL premises and conclusions are present in the schema but evaluating their semantic correctness requires running the Stanford CS221 inference engine, which was not done. The name inconsistency observed in D21 was detectable from NL inspection alone; other annotation issues may exist in the FOL layer.

5. **Label distribution in sample:** The 29/57 Uncertain rate in this sample (51%) is higher than the documented 61/226 ≈ 27% in the test set, suggesting either train-set distribution differs from test, or sampling variance at n=57 is significant. This limits inference about overall label balance from this sample alone.

