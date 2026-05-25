## Deployment Context

We are a US fintech startup building a personal finance chatbot that helps American adults with everyday money math: splitting bills, comparing loan APRs, calculating how long to pay off credit card balances, and budgeting across expense categories. Users type natural language questions about their finances. We want to evaluate whether an LLM can handle the quantitative reasoning these queries require before deploying the chatbot.

# Validity Analysis: gsm8k
**Target context:** US Adult Personal Finance Chatbot Users
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content | 2 | Significant gaps | high |
| Output Form | 3 | Moderate gaps | high |
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

GSM8K is a well-constructed grade-school math word-problem benchmark whose taxonomy, content, scoring ontology, and labels are explicitly scoped to elementary arithmetic in everyday consumer contexts. For a US adult personal-finance chatbot whose core value proposition is multi-step financial-instrument reasoning (APR, compound interest, amortization, payoff timelines) over assumption-sensitive queries with potentially range-valued correct answers, the misalignment is severe across the three HIGH-priority dimensions: Input Ontology (no financial-instrument problem types — 0/80 in dataset sample), Input Content (no consumer-finance vocabulary, no formula-selection or rate-disambiguation requirement), and Output Ontology (binary exact-match scoring incompatible with assumption-sensitive answer ranges). The Input Form dimension is well-aligned (typed English, CoT), and Output Content/Form are partially functional but cannot transfer to the deployment's financial-domain needs without substantial supplementation. The benchmark may still serve as a low-bar arithmetic-prerequisite filter and as infrastructure inspiration (calculator annotations, token-level verifier, socratic decomposition) for purpose-built financial evaluations.

## Practical Guidance

### What This Benchmark Measures

GSM8K measures a model's ability to perform multi-step natural-language arithmetic reasoning at grade-school complexity with traceable intermediate steps. For the deployment, this maps cleanly only to the commoditized simpler-tier queries (bill splitting, percentage budgeting) and to the prerequisite arithmetic skill underlying all financial computation. The strongest dimension is Input Form (text-in/text-out, English, CoT-required), which matches the deployment surface exactly.

### Construct Depth

Shallow for the deployment's core value proposition. GSM8K provides zero direct evidence on compound interest, APR comprehension, amortization, payoff timelines, minimum-payment semantics, or credit utilization — the three HIGH-priority dimensions (IO, IC, OO) each scored 1. The benchmark also acknowledges its own complexity ceiling [Q48, Q101], and FinChain independently confirms that even frontier LLMs show clear limitations in symbolic financial reasoning that GSM8K does not surface [WEB-16]. A high GSM8K score is necessary but far from sufficient evidence of deployment readiness.

### What Else You Need

(1) For IO/IC: adopt FinChain [WEB-16] to evaluate compound-interest and other symbolic financial-reasoning competence, supplemented with a bespoke evaluation covering consumer-specific query types (credit card payoff, minimum payment, balance transfer, credit utilization) since FinChain does not cover these. (2) For OO: implement assumption-pinned problem statements (FinChain-style parameterized templates) plus tolerance-band scoring for legitimately-range-valued queries. (3) For IC terminology grounding: build a targeted evaluation that tests term-to-operation mapping (APR→annualized periodic rate, minimum payment→issuer-formula-dependent) as a distinct construct from arithmetic — this gap is unaddressed by any benchmark surveyed [regional YAML gap 2]. (4) For OC: any new financial-content evaluation must use annotators with documented consumer-finance expertise, and the annotation framework must address the 1.7%-lower-bound labeling-error issue with greater rigor given regulatory exposure [WEB-5].

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
GSM8K's taxonomy is explicitly scoped to grade-school math word problems [Q1, Q8, Q11], with the authors positioning it as a 'tractable goal' at the lower end of the difficulty spectrum [Q11, Q20]. The deployment team identified APR comparisons, compound interest, amortization, and payoff timelines as ~40-50% of expected queries and the product's core value proposition. Empirical sampling of 80 datapoints found zero compound-interest, amortization, APR, minimum-payment, credit-utilization, or balance-transfer problems; the single 'interest' problem (DATASET-D3) is explicitly labeled simple interest and applies a flat annual rate. The authors themselves acknowledge a complexity ceiling [Q48, Q49, Q50] and note hope that future work will scale to 'problem distributions that require more complex mathematical reasoning' [Q101], implicitly conceding GSM8K does not represent such distributions. For this HIGH-priority dimension, the taxonomy gap is total for the core-value query types.

**Strengths:**
- Multi-step arithmetic reasoning with 3-6 sequential operations is exercised consistently [DATASET-D17, DATASET-D12], which is a prerequisite skill for any financial computation.

**Checklist:**

- **IO-1**: Required categories per deployment: APR comparisons, credit card payoff timelines, amortization schedules, compound interest, credit utilization, balance transfer cost/benefit, bill splitting, budgeting percentages. The first six are the core value proposition (~40-50% of queries). — _Sources: WEB-16_
- **IO-2**: Yes — GSM8K omits all financial-instrument categories. The 80-example dataset sample contains zero compound interest, APR, amortization, credit card, minimum payment, balance transfer, or credit utilization problems. The lone interest example (DATASET-D3) is explicit simple interest. The paper scopes problems to 'elementary concepts' [Q11] and 'grade school math' [Q1, Q8]. — _Sources: Q1, Q11, DATASET-D1, DATASET-D3, DATASET-D2_
- **IO-3**: Most GSM8K categories (animals, food, school, household items, sports) are construct-irrelevant for a personal-finance chatbot. They are not harmful per se but consume evaluation weight without informing the deployment use case, per the dataset sample showing groceries, baseball cards, toy cars, cupcakes, etc. [DATASET-D1, DATASET-D14, DATASET-D22]. — _Sources: DATASET-D1, DATASET-D14, DATASET-D22_
- **IO-4**: Major content-validity gap: the dimension marked HIGH priority by the user has zero coverage for compound interest, APR, amortization, payoff timelines, and minimum-payment semantics. GSM8K's documented complexity ceiling [Q48, Q49, Q50] further means even harder GSM8K problems would not reach the structural complexity of multi-period amortization or recursive compounding. — _Sources: Q48, Q101, DATASET-D3, DATASET-D11, WEB-16_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems.' (p.1)
- [Q11] 'GSM8K solutions depend only on elementary concepts, so achieving high test performance is a tractable goal.' (p.2)
- [Q20] 'The MATH dataset (Hendrycks et al., 2021) is larger and significantly more complex than GSM8K' (p.4)
- [Q48] 'a model with 10^16 parameters would be required to reach an 80% solve rate, when using the full GSM8K training set.' (p.6)
- [Q101] 'We expect verification to scale well to problem distributions that require more complex mathematical reasoning, and we hope GSM8K supports the development of new methods that scale even better.' (p.12)

*Web sources:*
- [WEB-16] FinChain (2025) explicitly covers compound interest and 57 other financial topics with verifiable CoT — the gap relative to GSM8K is well-established in the literature
- [WEB-17] FinBen aggregates FinQA/ConvFinQA/TAT-QA but targets corporate filings, not consumer personal finance — independent confirmation that consumer-finance taxonomic coverage is absent across major benchmarks

*Dataset analysis:*
- DATASET-D1: Baseball card counting problem — representative of modal GSM8K problem type, zero financial content
- DATASET-D3: 'Ariella's account earns her simple interest at the rate of 10% per annum' — only interest-bearing problem in 80-sample audit; explicitly simple, not compound
- DATASET-D2: '50% growth every year' on toy cars solved additively — structurally distinct from compound-interest formula application
- DATASET-D11: Two-variable linear equation about car collection — hardest algebraic problem sampled, still below structural complexity of amortization formulas

</details>

**Information gaps:**
- Whether the test split (not sampled) contains any financial-instrument problems — unlikely given documented scope but not empirically ruled out.

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
GSM8K's content was authored by Upwork/Surge AI contractors with no documented financial expertise [Q103, Q104], guided by GPT-3 seed questions [Q110, Q111] and a linguistic-diversity-within-elementary-concepts principle [Q9]. No annotator demographics — geographic, educational, financial-literacy — are reported. Empirically, the 80-example sample contains zero use of consumer-finance vocabulary (APR, minimum payment, balance transfer, credit utilization, amortization); even monetary problems use plain consumer-purchase framing [DATASET-D14, DATASET-D16, DATASET-D5]. The deployment team explicitly identified terminology-to-operation mapping as a distinct construct and a serious failure mode independent of arithmetic correctness. For this HIGH-priority dimension, GSM8K provides no scaffolding for the financial-vocabulary disambiguation the deployment requires.

**Strengths:**
- Monetary arithmetic with dollar amounts, percentages, and consumer-purchase framing is present in roughly 40-50% of sampled problems [DATASET-D16, DATASET-D5, DATASET-D6], providing some signal on US-style dollar/percentage handling — a prerequisite for the deployment's simpler bill-splitting and budgeting tier.
- Linguistic diversity is an explicit design principle [Q9] enforced via pairwise similarity scoring [Q113], reducing template-matching shortcuts.

**Checklist:**

- **IC-1**: Yes — the deployment requires recognition of US-specific financial vocabulary (APR per TILA/Reg Z [WEB-7], minimum payment, credit utilization, balance transfer) embedded in colloquial natural-language queries. The financial register is explicitly central to the deployment per elicitation. — _Sources: WEB-7, WEB-1_
- **IC-2**: Cultural framing of GSM8K (everyday US-style consumer life: food, animals, school) is broadly US-compatible per the regional YAML, and the dataset sample shows no obvious non-US monetary conventions; however, expert review of the source-culture flag remains deferred and unverified. — _Sources: DATASET-D5, DATASET-D14_
- **IC-3**: INSUFFICIENT DOCUMENTATION — annotator demographics (geographic location, educational background, financial literacy, native language) are not reported anywhere in the paper. Contractors were sourced via Upwork and Surge AI [Q103, Q104] but no further information is provided. — _Sources: Q103, Q104_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional annotator pool composition is documented; impossible to assess representativeness against the US adult personal-finance-chatbot user population.
- **IC-5**: Two concrete content gaps harm content validity: (a) complete absence of consumer-finance terminology across the 80-example sample [DATASET-D10, DATASET-D5, DATASET-D7]; (b) no problems requiring financial-formula selection or rate-type disambiguation — even the one explicit-interest problem pins the type as 'simple' [DATASET-D3, DATASET-D21]. — _Sources: DATASET-D10, DATASET-D5, DATASET-D7, DATASET-D3, DATASET-D21_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q9] 'We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts.' (p.2)
- [Q103] 'We initially collected a starting set of a thousand problems and natural language solutions by hiring freelance contractors on Upwork' (p.15)
- [Q104] 'We then worked with Surge AI ... to scale up our data collection.' (p.15)
- [Q110] 'we provided seed questions automatically generated from a few-shot prompted 175B GPT-3 model.' (p.15)

*Web sources:*
- [WEB-7] CFPB Reg Z §1026.22 establishes APR as the standardized US consumer-facing disclosure — vocabulary that GSM8K does not exercise
- [WEB-1] FINRA NFCS shows ~70% of US adults fail the compound-interest doubling question, confirming terminology comprehension is a distinct and high-stakes construct

*Dataset analysis:*
- DATASET-D10: 'Ian won $100 in the lottery. He decided to use the money to pay off debts.' — uses 'debts' as a plain word; no interest, no schedule
- DATASET-D5: Monthly rent/food/insurance percentage increases — personal-budget framing but zero financial-instrument vocabulary
- DATASET-D7: $98/sq ft real estate price computation — no mortgage, interest rate, or amortization content
- DATASET-D21: Explicit 'simple interest at the rate of 10% per annum' — removes the rate-type disambiguation challenge the deployment requires

</details>

**Information gaps:**
- Annotator demographics, including geographic distribution, financial literacy, and educational background, are entirely undocumented.
- Source-culture flag from the benchmark metadata is unverified; expert sample review would help confirm US compatibility of problem framings.

**Requires expert verification:**
- Whether any GSM8K problems reflect non-US monetary or institutional conventions (deferred in the regional YAML).

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Both benchmark and deployment are text-only English with standard Latin script [Q32, Q33], processed through GPT-family tokenizers [Q35, Q43]. The deployment's interaction modality is typed natural language, matching GSM8K's surface form. The chain-of-thought requirement [Q56, Q57] aligns with the 'show your work' expectation surfaced by CFPB regulatory scrutiny [WEB-5]. The socratic config additionally provides explicit sub-question scaffolding [DATASET-D20, DATASET-D15] that mirrors stepwise financial-calculation explanation. This LOWER-priority dimension is well-matched at the form level; minor concerns are pedagogical (additive vs. exponential growth framing [DATASET-D15]) rather than form-level.

**Strengths:**
- Text-only English input matches deployment modality exactly [Q32, Q33].
- Inline calculator annotations [Q40, DATASET-D14] provide a template for machine-verifiable arithmetic traces, useful infrastructure for a CFPB-relevant 'show-your-work' deployment.
- Socratic decomposition format [DATASET-D20] supports step-level reasoning evaluation, closer to what regulatory transparency requires.

**Checklist:**

- **IF-1**: Signal distributions match: typed English text, ASCII + standard Unicode punctuation, numerals, decimal notation. Both benchmark and deployment use the same input encoding. — _Sources: Q32, Q33_
- **IF-2**: US infrastructure supports typed text input; 90% smartphone ownership and 95% internet use [WEB-12, WEB-14] confirm the regional substrate. — _Sources: WEB-12_
- **IF-3**: Domain-specific form note: deployment queries embed consumer-finance vocabulary in natural language, which is a content rather than form difference; surface form (typed English) is unchanged. — _Sources: Q56, Q57_
- **IF-4**: No material form mismatches identified. Minor: the calculator-annotation format [Q40, Q119] is a benchmark-internal training artifact and is unlikely to appear in user queries, but this does not harm external validity since it is a training-time intervention not part of the input contract. — _Sources: Q40, DATASET-D14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q32] 'we focus attention on the space of natural language solutions, as this is a richer and more general solution format than pure mathematical expressions.' (p.5)
- [Q33] 'this choice enables our models to develop verbal analytical skills and to produce solutions that are more readily interpretable by humans.' (p.5)
- [Q56] 'it is important to allow the model to generate the full natural language solution before outputting a final answer.' (p.7)
- [Q57] 'If we instead finetune a 6B model to directly output the final answer without any intermediate steps, performance drops drastically from 20.6% to 5.2%.' (p.7)

*Web sources:*
- [WEB-12] ~95% of US adults use the internet; 90% own smartphone — typed-text deployment infrastructure is well-supported
- [WEB-5] CFPB June 2023 chatbot spotlight — confirms regulatory expectation that chatbot reasoning be transparent and traceable, matching GSM8K's CoT requirement

*Dataset analysis:*
- DATASET-D14: Inline <<9*4=36>> annotations confirm machine-verifiable arithmetic trace format across the dataset
- DATASET-D20: Socratic config decomposes algebraic reasoning into named sub-operations — useful step-level evaluation scaffold

</details>

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
GSM8K's output ontology is binary exact-match against a single ground-truth final number [Q31, Q60], with the only background-knowledge concession being 'basic background knowledge, like the number of days in a week' [Q21]. No tolerance bands, no range-based correctness, no assumption-pinning, no partial credit. The deployment requires range-based or assumption-conditioned scoring because a meaningful share of target queries (payoff timelines, effective vs. nominal APR, budgeting recommendations) have legitimate answer ranges depending on compounding frequency, issuer-specific minimum-payment formulas, and timing conventions — confirmed by the user in Q3 of elicitation and by regulatory context [WEB-7] (Reg Z fixes APR conventions for closed-end loans but not for credit-card effective vs. nominal communications, and not for issuer-specific minimum-payment formulas). The 80-example sample confirms uniform single-answer #### N termination [DATASET-D9, DATASET-D4]. For this HIGH-priority dimension, the structural and content validity of the scoring scheme is fundamentally misaligned with the deployment.

**Strengths:**
- For the well-defined deterministic problems GSM8K does cover, exact-match scoring is objectively verifiable and reproducible [Q60, DATASET-D9].

**Checklist:**

- **OO-1**: Output ontology is single category: exact numeric match to final answer [Q31, Q60]. For the deployment's assumption-sensitive queries (payoff timelines, effective APR, amortization total interest), this is too narrow. — _Sources: Q31, Q60_
- **OO-2**: Missing categories specific to the deployment: (a) range/tolerance-band correctness for assumption-sensitive queries, (b) assumption-conditioned correctness (e.g., 'correct given monthly compounding'), (c) partial credit for correct reasoning with wrong arithmetic vs. correct arithmetic on wrong formula — the verifier visualization appendix [Q61, Q155] documents these as known failure modes but does not score them differently. — _Sources: Q61, DATASET-D4_
- **OO-3**: The single-answer convention encodes an assumption that mathematical problems have one correct answer. This holds for grade-school arithmetic but does not generalize to consumer finance where compounding-frequency conventions, issuer-specific minimum-payment formulas [regional YAML], and timing assumptions create legitimate answer ranges. — _Sources: Q21, WEB-7_
- **OO-4**: Significant misalignment exists; stakeholder-driven redesign is warranted. FinChain's CHAINEVAL framework [WEB-16] illustrates how parameterized symbolic templates can pin assumptions explicitly while evaluating both final-answer and step-level correctness. — _Sources: WEB-16_
- **OO-5**: Both structural validity (the scoring construct misrepresents the answer-space structure of financial queries) and content validity (entire output categories like 'valid range' and 'assumption-conditioned correct' are missing) are harmed. The deployment's hardest queries cannot be scored meaningfully under this ontology. — _Sources: Q60, DATASET-D9, DATASET-D4_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'Verifiers are trained to judge the correctness of solutions, with the training signal determined solely by whether or not the solution reached the correct final answer.' (p.5)
- [Q60] 'Training solutions are labeled as correct or incorrect based solely on whether they reach the correct final answer.' (p.7)
- [Q21] 'GSM8K includes questions that require basic background knowledge, like the number of days in a week.' (p.4)
- [Q61] 'In practice, some solutions will reach the correct final answer using flawed reasoning, leading to false positives.' (p.7)

*Web sources:*
- [WEB-7] CFPB Reg Z §1026.22 — Appendix J APR method pins one correct answer for closed-end loans but leaves credit-card effective-vs-nominal communication outside this resolution
- [WEB-16] FinChain's CHAINEVAL metric demonstrates assumption-pinned parameterized symbolic templates as the closest available framework for the required scoring ontology

*Dataset analysis:*
- DATASET-D9: 'Let N be the original price...10N=6(N+8)...#### 120' — single labeled answer with no tolerance
- DATASET-D4: 'In the second year, she earns the same amount of interest, which $60 + $60 = $120 ... #### 720' — single answer would be wrong if interpreted as compound (correct would be $726); illustrates structural mismatch

</details>

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Label correctness within GSM8K's own scope is supported by a re-solve verification pass [Q105, Q106] with a documented 1.7% disagreement rate [Q107, Q108], acknowledged as a lower bound [Q109]. However, this quality control was performed by the same Upwork/Surge AI contractor pool with no documented domain expertise [Q103, Q104], and no annotator demographic information is reported. For the deployment, the more severe issue is that GSM8K labels for financial-adjacent problems may be conceptually correct grade-school answers but pedagogically misleading for finance: DATASET-D2 treats 50% annual growth additively (still hits answer for n=3 by coincidence in this case but mis-frames the operation); DATASET-D3/D4 explicitly uses simple interest where a real savings account would compound. The verifier failure-mode appendix [Q61, Q153, Q155] also documents that flawed reasoning with correct final answers and surface ambiguity create labeling errors — issues that would be amplified in financial content. The MODERATE-priority dimension is partially functional (labels are correct for grade-school content) but not fit for downstream financial-label transfer.

**Strengths:**
- Documented re-solve verification pass with disagreement-driven repair/discard [Q105, Q106] establishes a non-trivial quality floor for the labels that do exist.
- 1.7% disagreement rate [Q107] is empirically measured rather than asserted, with the limitation explicitly acknowledged as a lower bound [Q108, Q109].

**Checklist:**

- **OC-1**: For grade-school arithmetic, ground-truth labels are mathematically determined and stakeholder-independent. For deployment-relevant financial questions, GSM8K provides no labels — and the one financial-adjacent label (simple interest, DATASET-D4) reflects a pedagogical convention that diverges from real consumer-savings behavior. — _Sources: Q60, DATASET-D4_
- **OC-2**: Disagreement between original annotators and regional financial-domain experts is likely for any borderline financial-adjacent problem, since contractors had no documented financial expertise [Q103, Q104]. Regional YAML notes ~70% of US adults answer the NFCS compound-interest question incorrectly [WEB-1], implying the contractor pool is unlikely to skew higher on this dimension. — _Sources: Q103, Q104, WEB-1_
- **OC-3**: INSUFFICIENT DOCUMENTATION — no Datasheet or Data Statement; the paper reports only that contractors came from Upwork [Q103] and Surge AI [Q104] with no demographics, expertise, or geographic information.
- **OC-4**: Re-annotation by a financial-expert regional pool would be needed for any extension into consumer finance; FinChain's expert-curated symbolic templates [WEB-16] offer a model for this. — _Sources: WEB-16_
- **OC-5**: INSUFFICIENT DOCUMENTATION — aggregation method is described as disagreement-triggered repair/discard [Q106]; minority annotator perspectives are not surfaced or analyzed.
- **OC-6**: Convergent validity is unverified for any financial-content extension because the annotator pool's financial expertise is undocumented. External validity is harmed because the simple-interest convention used in the lone interest-adjacent problem [DATASET-D21] does not generalize to deployment query expectations. — _Sources: Q109, DATASET-D21, Q155_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q105] 'we asked workers to re-solve all problems, with no workers re-solving problems they originally wrote.' (p.15)
- [Q106] 'any problems that produced disagreements were either repaired or discarded.' (p.15)
- [Q107] '1.7% of problems still produce disagreements among contractors.' (p.15)
- [Q108] 'We estimate this to be the fraction of problems that contain breaking errors or ambiguities.' (p.15)
- [Q109] 'It is possible that a larger percentage of problems contain subtle errors.' (p.15)
- [Q155] 'Verifiers occasionally make mistakes with performing this variable binding of quantities to their relationships.' (p.22)

*Web sources:*
- [WEB-1] FINRA NFCS — only 27% of US adults answer ≥5/7 financial-knowledge questions; ~70% wrong on compound-interest doubling — confirms general-population annotators (the likely contractor pool composition) cannot reliably produce financial-domain labels
- [WEB-16] FinChain uses expert-curated parameterized symbolic templates with machine-verifiable Python traces — illustrates the level of annotation rigor required for financial content

*Dataset analysis:*
- DATASET-D4: Year-two interest computed as identical to year-one — labeled correct, but pedagogically misleading if transferred to a real savings-account framing
- DATASET-D21: Explicit 'simple interest at the rate of 10% per annum' — removes disambiguation but encodes a non-default convention for actual savings accounts

</details>

**Information gaps:**
- Annotator demographics and financial expertise levels are entirely undocumented.
- Aggregation method beyond binary disagreement-repair/discard is unspecified.

**Requires expert verification:**
- Whether any GSM8K problems contain subtle labeling errors that would matter for a deployment-adjacent skill (the authors acknowledge subtle errors may exist beyond the 1.7% bound [Q109]).

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
GSM8K's output form is step-by-step natural-language solutions terminating in a single final number [Q56, Q57, Q29, Q46], which partially aligns with a typed-text chatbot deployment. The chain-of-thought requirement supports the deployment's need for transparent reasoning (relevant for CFPB-flagged UDAAP/Reg Z risk [WEB-5]), and the calculator-annotation format [Q40, Q119, DATASET-D14] provides a template for arithmetic verifiability. However, the deployment also requires the model to produce assumption disclosures, caveats, and range-based answers — outputs that GSM8K's form contract does not exercise or score. The token-level verifier interpretability [Q147-Q149] is a constructive form-level feature that could be ported to financial reasoning. This MODERATE-priority dimension is functional at the surface level (text-in/text-out, CoT) but does not exercise the assumption-disclosure or range-presentation aspects the deployment needs.

**Strengths:**
- Natural-language step-by-step solutions [Q32, Q33] match the deployment's text-out modality and CFPB transparency expectations [WEB-5].
- Token-level verifier provides per-token interpretability [Q147, Q148, Q149], a diagnostic capability transferable to financial reasoning evaluation.
- Socratic config sub-question structure [DATASET-D20] models the kind of stepwise explanation users may need in personal-finance chatbot contexts.

**Checklist:**

- **OF-1**: Output modality (typed English text with embedded step-by-step reasoning) matches deployment needs at the surface level [Q32, Q33]; however, the form does not include assumption-disclosure, range-presentation, or caveat-emission constructs that the deployment requires for assumption-sensitive queries. — _Sources: Q32, Q33, Q56_
- **OF-2**: Not applicable — text-only chatbot deployment; no TTS requirement per regional YAML.
- **OF-3**: Digital-literacy assumption is reasonable for the target population [regional YAML, WEB-14]; ~90% smartphone ownership and 95% internet use support typed-text accessibility for the deployment's intended user base, though the 5% gap is documented [WEB-12]. — _Sources: WEB-14, WEB-12_
- **OF-4**: Form mismatches harming external validity: (a) GSM8K does not score whether a solution states its assumptions, (b) does not score whether a solution offers a range when appropriate, (c) does not score whether a solution flags issuer-specific or convention-dependent variability. These are explicit deployment requirements that the output form does not exercise. — _Sources: Q29, Q46, WEB-5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q29] 'we judge performance by autoregressively sampling a single low temperature solution and checking whether the final answer is correct.' (p.5)
- [Q46] 'Test performance is determined by a single low temperature (T = 0) sample for each test problem.' (p.6)
- [Q56] 'it is important to allow the model to generate the full natural language solution before outputting a final answer.' (p.7)
- [Q147] 'One benefit of the token-level verifiers is that these models become immediately interpretable' (p.21)

*Web sources:*
- [WEB-5] CFPB June 2023 chatbot spotlight identifies chatbots as UDAAP/Reg E/Reg Z compliance risk — making assumption disclosure and reasoning transparency operationally important
- [WEB-14] 90% US smartphone ownership; 81% mobile bank access — typed-text output modality is appropriate

*Dataset analysis:*
- DATASET-D20: Socratic sub-question decomposition exemplifies step-level explanatory form transferable to financial walkthroughs
- DATASET-D14: Inline <<expr=result>> annotations across all sampled problems confirm consistent arithmetic-trace format

</details>

**Information gaps:**
- GSM8K does not document any output convention for stating assumptions or producing ranges; whether such outputs would be rejected by the scoring harness or simply ignored is not specified.

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** GSM8K's taxonomy contains no financial-instrument problem types covering the deployment's core value proposition (~40-50% of queries).

**Recommendation:** Pair GSM8K with FinChain [WEB-16] for compound-interest and symbolic-financial-reasoning coverage, and commission a bespoke benchmark of ~500-1000 consumer-finance scenarios (APR comparisons, credit card payoff timelines, amortization, minimum-payment semantics, credit utilization, balance transfer break-even) using parameterized templates that pin assumptions explicitly.

### Input Ontology ⚠

**Gap:** GSM8K is documented as having a complexity ceiling [Q48, Q49, Q50] that does not reach the structural complexity of multi-period amortization or recursive compounding even at its hardest.

**Recommendation:** Treat GSM8K performance as a necessary but non-sufficient prerequisite: require a minimum GSM8K threshold (e.g., 90%+) as a gate before deploying, but base deployment decisions on the financial-specific evaluations above. Do not extrapolate GSM8K headline numbers to financial reasoning competence.

### Input Content ⚠

**Gap:** No consumer-finance terminology in GSM8K; the term-to-operation mapping construct (e.g., APR→periodic rate) is untested by any surveyed benchmark.

**Recommendation:** Build a targeted terminology-grounding evaluation suite that varies surface phrasing of consumer-finance terms (APR vs. interest rate vs. finance charge; minimum payment vs. full balance) and tests whether the model selects the mathematically correct operation. Use TILA/Reg Z conventions [WEB-7] as the canonical ground truth where applicable, and document deviations from those conventions explicitly.

### Output Ontology ⚠

**Gap:** Binary exact-match scoring cannot accommodate range-valued or assumption-conditioned correct answers for ~half the deployment's query mix.

**Recommendation:** Adopt assumption-pinned problem statements (FinChain CHAINEVAL pattern [WEB-16]) as the primary mechanism, supplemented by tolerance-band acceptance for issuer-variable quantities (minimum-payment formulas) and explicit multi-answer ground truth where conventions diverge (effective vs. nominal APR). Score both final-answer correctness and step-level reasoning consistency.

### Output Content

**Gap:** Annotator demographics and financial expertise are undocumented; 1.7% disagreement is an explicit lower bound on labeling errors [Q108, Q109], and the contractor pool is unlikely to have financial-domain expertise.

**Recommendation:** For any financial-content extension or supplementary benchmark, recruit annotators with demonstrated consumer-finance expertise (e.g., CFP credential, lending operations experience). Publish a Datasheet/Data Statement documenting annotator demographics, financial background, and inter-annotator agreement broken down by problem type.

### Output Form

**Gap:** Output form does not exercise or score assumption-disclosure, caveat-emission, or range-presentation — explicit deployment requirements and CFPB-relevant compliance behaviors [WEB-5].

**Recommendation:** Extend the evaluation rubric to score (a) presence and accuracy of stated assumptions for assumption-sensitive queries, (b) appropriate use of ranges where conventions vary, (c) explicit flags when issuer-specific variation makes a definitive answer impossible. The token-level verifier interpretability pattern [Q147-Q149] can be adapted as scoring infrastructure for these constructs.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "we introduce GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems." |
| Q2 | 1 | input_ontology | "To increase performance, we propose training verifiers to judge the correctness of model completions." |
| Q3 | 1 | output_form | "At test time, we generate many candidate solutions and select the one ranked highest by the verifier." |
| Q4 | 1 | output_form | "We demonstrate that verification significantly improves performance on GSM8K, and we provide strong empirical evidence that verification scales more effectively with increased data than a finetuning baseline." |
| Q5 | 1 | stated_limitations | "One significant challenge in mathematical reasoning is the high sensitivity to individual mistakes (Shen et al., 2021a)." |
| Q6 | 1 | stated_limitations | "When generating a solution, autoregressive models have no mechanism to correct their own errors." |
| Q7 | 1 | input_content | "Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, John Schulman, OpenAI" |
| Q8 | 2 | input_ontology | "We are releasing GSM8K, a dataset of 8.5K high quality problems at the grade school math level." |
| Q9 | 2 | input_content | "We designed this dataset to have high linguistic diversity while relying on relatively simple grade school math concepts." |
| Q10 | 2 | input_content | "State-of-the-art language models struggle to achieve high performance on this dataset, primarily due to the high diversity among problems." |
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
| Q21 | 4 | output_ontology | "Similar to CommonsenseQA, GSM8K includes questions that require basic background knowledge, like the number of days in a week." |
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
| Q47 | 6 | output_form | "Unsurprisingly, we see that the 175B model significantly outperforms the smaller models." |
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
| Q69 | 8 | output_content | "We find that it is not beneficial to use verification at low dataset sizes." |
| Q70 | 8 | output_content | "We believe this is due to the pressure to overfit to the correct answer: with small datasets, overfitting to the correct answer happens faster than learning more generalizable properties of correct reasoning." |
| Q71 | 8 | output_form | "However, once we use a sufficiently large dataset, we see a strong boost from verifiers." |
| Q72 | 9 | input_ontology | "We can either train verifiers to make a single scalar prediction conditioned on the entire generated solution, or to make a scalar prediction after each token in the solution." |
| Q73 | 9 | input_ontology | "By default, we choose the latter, training verifiers to make predictions after each token." |
| Q74 | 9 | input_ontology | "This can be viewed as a token-level value function." |
| Q75 | 9 | input_ontology | "Predicting the value function at every token is a more challenging and noisier task than judging only the full completion." |
| Q76 | 9 | output_form | "However, despite the initially slower training, the token-level verifier ultimately outperforms the solution-level verifier." |
| Q77 | 9 | output_content | "Moreover, the token-level verifier is still improving late in training, whereas the solution-level verifier quickly shows signs of overfitting." |
| Q78 | 9 | input_ontology | "We hypothesize that the full value function provides a useful auxiliary signal that encourages the model to judge the reasoning throughout solutions, rather than merely memorizing the correct final answer." |
| Q79 | 9 | input_ontology | "As discussed in Section 4.2, we can optionally include a language modeling objective alongside the verification objective." |
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
| Q127 | 18 | output_content | "Samples were slightly cherry-picked for diversity." |
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
| WEB-1 | https://www.finrafoundation.org/sites/finrafoundation/files/2025-07/NFCS-Report-Sixth-Edition-July-2025.pdf |
| WEB-2 | https://www.finra.org/media-center/newsreleases/2025/finra-foundation-releases-state-state-financial-knowledge-findings |
| WEB-3 | https://www.finra.org/media-center/newsreleases/2025/finra-foundation-releases-sixth-wave-national-financial-capability |
| WEB-4 | https://www.consumerfinance.gov/about-us/newsroom/cfpb-comment-on-request-for-information-on-uses-opportunities-and-risks-of-artificial-intelligence-in-the-financial-services-sector/ |
| WEB-5 | https://www.consumerfinance.gov/about-us/newsroom/cfpb-issue-spotlight-analyzes-artificial-intelligence-chatbots-in-banking/ |
| WEB-6 | https://www.skadden.com/insights/publications/2024/08/cfpb-comments-on-artificial-intelligence |
| WEB-7 | https://www.consumerfinance.gov/rules-policy/regulations/1026/22/ |
| WEB-8 | https://files.consumerfinance.gov/f/201503_cfpb_truth-in-lending-act.pdf |
| WEB-9 | https://www.ftc.gov/business-guidance/privacy-security/gramm-leach-bliley-act |
| WEB-10 | https://www.orrick.com/en/Insights/2025/07/Where-is-the-GLBA-Entity-Level-Exemption-Two-More-State-Privacy-Laws |
| WEB-11 | https://www.consumerfinancemonitor.com/2026/05/12/glba-modernization-legislation-key-implications-for-financial-institutions-data-practices/ |
| WEB-12 | https://www.pewresearch.org/short-reads/2026/01/08/internet-use-smartphone-ownership-digital-divides-in-u-s/ |
| WEB-13 | https://www.pewresearch.org/internet/2024/01/31/americans-use-of-mobile-technology-and-home-broadband/ |
| WEB-14 | https://www.pewresearch.org/internet/fact-sheet/mobile/ |
| WEB-15 | https://www.finra.org/investors/insights/finra-foundation-national-financial-capability-study |
| WEB-16 | https://arxiv.org/abs/2506.02515 |
| WEB-17 | https://proceedings.neurips.cc/paper_files/paper/2024/file/adb1d9fa8be4576d28703b396b82ba1b-Paper-Datasets_and_Benchmarks_Track.pdf |
| WEB-18 | https://awesomeagents.ai/leaderboards/finance-llm-leaderboard/ |
| WEB-19 | https://www.securityscientist.net/blog/glba-gramm-leach-bliley-act-compliance-guide/ |

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
| D1 | main | 1 | 32 | "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them. On Wednesday Buddy buys 12 baseball cards. On Thursday he buys a third of what he had on Tuesday." | Multi-step counting problem with no financial domain content | IO |
| D2 | main | 19 | 54 | "Bobby has 16 toy cars, and the number of cars he has increases by 50% every year. How many toy cars will Bobby have in three years?" | Percentage growth applied to toy cars — not compound interest | IO |
| D3 | main | 43 | 720 | "Ariella has $200 more in her son's saving account than Daniella has in her son's savings account. Ariella's account earns her simple interest at the rate of 10% per annum. If Daniella has $400, how much money will Arialla have after two years?" | Simple interest problem — uses savings account framing but applies flat annual rate, not compound | IC, IO |
| D4 | main | 43 | 720 | "In the second year, she earns the same amount of interest, which $60 + $60 = $120" | Answer treats the second year interest as identical to year one — confirming this is simple interest, not compound | OO, OC |
| D5 | main | 30 | 7200 | "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month. This year her rent goes up by 30%, food costs increase by 50%, and the cost of her car insurance triples because she was at fault in an accident." | Personal budgeting scenario — percentage increases on fixed monthly expenses | IO, IC |
| D6 | main | 44 | 11000 | "James decides to replace his car. He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value. How much was he out of pocket?" | Car resale/purchase — percentage of face value, single-step arithmetic | IO |
| D7 | main | 35 | 333200 | "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft and the barn out back is 1,000 sq ft. How much is this property?" | Real estate price calculation — multiplication of unit price by area | IO |
| D8 | main | 13 | 1825 | "Sally and Bob have made plans to go on a trip at the end of the year. They both decide to work as babysitters and save half of what they've earned for their trip. If Sally makes $6 per day and Bob makes $4 per day, how much money will they both have saved for their trip after a year?" | Simple daily savings with no interest; savings framing but no financial instrument | IO, IC |
| D9 | main | 45 | 120 | "Ten friends decide to get an end-of-year gift for their teacher. They plan to split the cost of the gift equally. But four of the group drop out. The remaining friends split the cost equally among themselves. If each share is now $8 more, how much does the gift cost, in dollars?" | Algebraic bill-splitting — the closest GSM8K analog to the deployment's "bill splitting" use case | IO |
| D10 | main | 39 | 20 | "Ian won $100 in the lottery. He decided to use the money to pay off debts. He paid $20 to Colin. He then paid twice as much to Helen, as he had paid to Colin. Then finally, he paid half as much to Benedict, as he had paid to Helen. How much money, in dollars, does he have left after paying off debts?" | Debt-payment problem — uses "debts" vocabulary but involves no interest, APR, or balance computations | IC |
| D11 | main | 23 | 220 | "Jim collects model cars, and he has 301 models total. Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys. How many Buicks does Jim have?" | Multi-variable algebraic word problem — no financial content | IO |
| D12 | main | 7 | 90 | "There are enough provisions in a castle to feed 300 people for 90 days. After 30 days, 100 people leave the castle. How many more days are left until all the food runs out?" | Rate/ratio problem — requires proportional reasoning across changing quantities | IO |
| D13 | main | 6 | 54 | "Nancy is filling an aquarium for her fish...If the aquarium is 4 feet long, 6 feet wide, and 3 feet high, how many cubic feet of water are in the aquarium?" | Volume + fraction chaining — geometry-based multi-step | IO |
| D14 | main | 3 | 99 | "They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag. How much did the unicorn piñata and the treats cost altogether?" | Grocery/party supply addition — simplest form of monetary arithmetic | IO |
| D15 | socratic | 19 | 54 | "How many new cars will Bobby acquire in the first year? ** In the first year, Bobby will acquire 16 * .5 = <<16*.5=8>>8 new cars. ... How many cars will Bobby have after the third year? ** After the third year, he will have 36 + 18 = <<36+18=54>>54 cars in total." | Socratic format decomposes growth steps but each year is computed from prior year's total — additive not exponential framing | IF, OO |
| D16 | main | 22 | 80 | "Austin bought his seven friends each a robot. Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change. How much did Austin start with?" | Retail transaction with tax and change — closest analog to everyday consumer arithmetic with dollar amounts | IO |
| D17 | main | 32 | 2290 | "Daniel has a collection of 346 video games. 80 of them, Daniel bought for $12 each. Of the rest, 50% were bought for $7. All others had a price of $3 each. How much did Daniel spend on all the games in his collection?" | Multi-tier cost calculation with percentages — 3-step monetary reasoning | IO |
| D18 | main | 38 | 90 | "The ratio of coins that Elsa has to that which Amalie has is 10:45. If the total number of coins they have is 440, and Amalie spends 3/4 of what she has on toys, how many will she remain with?" | Ratio-based partition problem — abstract currency-free | IO |
| D19 | main | 20 | 138 | "One pie costs $4 for a piece. Each pie is having 3 pieces. During one hour the bakery can make 12 pies. Creating one pie costs the bakery $0.5. Considering the bakery would be able to sell all pie pieces, how much money would it make?" | Bakery profit calculation — revenue minus cost | IO |
| D20 | socratic | 23 | 220 | "Define a variable ** Let x represent the number of Chevys ... Combine like terms ** 11x+15=301 ... Divide by 11 ** x=<<26=26>>26" | Socratic config adds explicit algebraic reasoning sub-steps — useful for evaluating chain-of-thought decomposition | IF |
| D21 | main | 43 | 720 | "Ariella's account earns her simple interest at the rate of 10% per annum" | Explicit "simple interest" label — benchmark treats this as equivalent in difficulty to non-financial problems, but distinguishes from compound | OO, IC |
| D22 | main | 2 | 9 | "Anna baked 60 cupcakes. She gives away 4/5 of the cupcakes to her classmates. Of the remaining 1/5 of cupcakes, she eats 3 cupcakes. How many cupcakes does she have left?" | Fraction subtraction — everyday context, zero financial domain content | IO |
| D23 | main | 28 | 40 | "A company has 200 employees. 60% of the employees drive to work. Of the employees who don't drive to work, half take public transportation. How many more employees drive to work than take public transportation?" | Percentage partition — applied to commuting, not finance | IO |
| D24 | main | 31 | 10 | "Dan owns an ice cream shop and every sixth customer gets a free ice cream cone. Cones cost $2 each. If he sold $100 worth of cones, how many free ones did he give away?" | Simple division with a promotional rule — monetary context but trivial | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Multi-step arithmetic with traceable natural-language reasoning chains
- **Dimension(s):** IO, IF
- **Observation:** The benchmark consistently demands 3–6 sequential arithmetic operations expressed in coherent natural language before arriving at a final answer. The `main` config shows step-by-step solutions embedded inline with calculator annotations; the `socratic` config decomposes the same problems into explicit sub-questions. Both formats confirm the chain-of-thought requirement documented in the paper.
- **Deployment relevance:** The deployment requires a chatbot that can walk users through multi-step finance calculations (e.g., tracking a payoff timeline month by month). GSM8K exercises the structural skill of multi-step traceable reasoning, even though the content domain differs. A model that scores well must produce coherent intermediate steps, not just final answers.
- **Datapoint citations:**
  - [D17] Example 32 (main, train, label=2290): "On 80 games, Daniel spend 80 games * $12/game = $960. The rest of the collection is 346 games - 80 games = 266 games. 50% of these games means 50/100 * 266 games = 133 games..." — Three-tier cost computation requiring sequential sub-totals before a final sum.
  - [D12] Example 7 (main, train, label=90): "After 30 days, there will be enough food left to sustain 300 people for 90 days – 30 days = 60 days... The 200 people will eat 200/300 = 2/3 as much food... The 60 days' worth of food will last this smaller group for 60 days / (2/3) = 90 more days." — Rate-ratio chaining requiring proportion manipulation across multiple steps.

#### Strength 2: Socratic sub-question decomposition format
- **Dimension(s):** IF, OF
- **Observation:** The `socratic` config reformats every problem so that each sub-step is explicitly prefaced by a natural-language sub-question, then answered. This structure provides a finer-grained window into whether a model's intermediate reasoning is correct, not just its final answer.
- **Deployment relevance:** For a fintech chatbot where reasoning transparency is a CFPB-relevant concern, the socratic format offers an evaluation scaffold that better mirrors the "show your work" expectation. It provides a basis for step-level correctness scoring that is closer to what the deployment needs than the flat main-format evaluation.
- **Datapoint citations:**
  - [D20] Example 23 (socratic, train, label=220): "Define a variable ** Let x represent the number of Chevys ... Combine like terms ** 11x+15=301 ... Divide by 11 ** x=26" — Algebraic reasoning decomposed into named sub-operations, enabling step-level verification.
  - [D15] Example 19 (socratic, train, label=54): "How many new cars will Bobby acquire in the first year? ** In the first year, Bobby will acquire 16 * .5 = 8 new cars. ... How many cars will Bobby have after the third year? ** After the third year, he will have 36 + 18 = 54 cars in total." — Growth-over-time problem decomposed into per-period steps, structurally parallel to how one might verify a compound-interest accumulation calculation period by period.

#### Strength 3: Monetary arithmetic with dollar amounts and percentages
- **Dimension(s):** IO, IC
- **Observation:** A meaningful subset of the sampled problems use dollar amounts, percentages, and consumer-purchase framing. These problems require correct handling of decimal arithmetic, percentage-to-decimal conversion, and multi-item totaling — skills that are prerequisite for any financial reasoning task.
- **Deployment relevance:** The deployment's simpler query tier (bill splitting, expense totaling, percentage-based budgeting) uses the same arithmetic primitives tested in these problems. A model that fails on GSM8K dollar-amount problems would almost certainly fail on the chatbot's simpler tasks.
- **Datapoint citations:**
  - [D16] Example 22 (main, train, label=80): "Austin bought his seven friends each a robot. Each robot costs $8.75. He was charged $7.22 total for tax. He left with $11.53 in change. How much did Austin start with?" — Retail transaction with tax and change arithmetic.
  - [D5] Example 30 (main, train, label=7200): "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month. This year her rent goes up by 30%, food costs increase by 50%... How much more does Jessica pay for her expenses over the whole year compared to last year?" — Monthly budget with percentage increases annualized.
  - [D6] Example 44 (main, train, label=11000): "He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value. How much was he out of pocket?" — Two-transaction net cost computation.

#### Strength 4: Inline calculator annotations confirm arithmetic execution traceability
- **Dimension(s):** IF, OF
- **Observation:** Every arithmetic operation in the answer string is annotated with a `<<expression=result>>` inline tag (e.g., `<<30/2=15>>`, `<<9*4=36>>`). This annotation convention provides machine-verifiable intermediate computation traces alongside natural language.
- **Deployment relevance:** The deployment needs a model that can be verified at the arithmetic level, not just at the final answer. The annotation format provides a template for building similar verification infrastructure over financial reasoning answers, and its presence in all 80 sampled examples confirms consistent coverage.
- **Datapoint citations:**
  - [D14] Example 3 (main, train, label=99): "The four bags of Reese's cost $9 x 4 = $<<9*4=36>>36. The three bags of Snickers cost $5 x 3 = $<<5*3=15>>15." — Each arithmetic step tagged independently, enabling automated step verification.
  - [D9] Example 45 (main, train, label=120): "10N=6(N+8) ... 4N=48 ... N=<<12=12>>12 ... the present costs 10*12=<<10*12=120>>120." — Algebraic solution with all numeric derivations annotated.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete absence of financial-instrument problem types
- **Dimension(s):** IO
- **Observation:** Across all 80 sampled examples, zero problems involve compound interest, APR, amortization, credit card payoff timelines, minimum payment calculations, credit utilization ratios, or balance transfer computations. The closest financial-domain example is a simple interest problem (Example 43) that explicitly labels itself "simple interest" and applies a flat annual rate rather than compounding. All other monetary problems involve one-time retail purchases, salary/savings accumulation without interest, or abstract cost allocation.
- **Deployment relevance:** The deployment team confirmed that 40–50% of expected queries involve APR, compound interest, amortization, and payoff timelines — described as the product's core value proposition. The benchmark provides zero signal on the model's ability to perform these computations. A model that achieves high GSM8K accuracy could still fail entirely on the deployment's defining query types.
- **Datapoint citations:**
  - [D3] Example 43 (main, train, label=720): "Ariella's account earns her simple interest at the rate of 10% per annum. If Daniella has $400, how much money will Arialla have after two years?" — The only savings/interest problem in the sample; explicitly "simple interest," not compound.
  - [D4] Example 43 (main, train, label=720): "In the second year, she earns the same amount of interest, which $60 + $60 = $120" — Second-year interest is identical to first year — confirming flat-rate simple interest; compound interest would yield $66 in year two (10% of $660), making this structurally different from a real savings account.
  - [D1] Example 1 (main, train, label=32): "On Monday Buddy has 30 baseball cards. On Tuesday Buddy loses half of them." — Representative of the modal problem type: no monetary content whatsoever.
  - [D8] Example 13 (main, train, label=1825): "They both decide to work as babysitters and save half of what they've earned for their trip. If Sally makes $6 per day... how much money will they both have saved... after a year?" — Savings accumulation with zero interest — no financial instrument logic.

#### CRITICAL Concern 2: No financial terminology — complete semantic grounding gap
- **Dimension(s):** IC
- **Observation:** Across all 80 sampled examples, no problem uses the terms APR, annual percentage rate, compound interest, credit card, minimum payment, balance transfer, credit utilization, amortization, or any related consumer finance vocabulary. All monetary problems use colloquial consumer-purchase framing (candy, robots, shoes, bakery goods, car purchase at a discount). No problem requires a model to parse a financial term and map it to a mathematical operation.
- **Deployment relevance:** The deployment team identified financial terminology handling as essential and named the misinterpretation of APR as a flat rate as "a serious failure mode even when the arithmetic itself is trivial." GSM8K does not test this construct at all. A model could achieve perfect GSM8K performance while having no ability to correctly interpret "APR" or "minimum payment" in a user query.
- **Datapoint citations:**
  - [D10] Example 39 (main, train, label=20): "Ian won $100 in the lottery. He decided to use the money to pay off debts. He paid $20 to Colin." — Uses "debts" as a plain word but involves no interest, no schedule, no rate — pure arithmetic subtraction.
  - [D5] Example 30 (main, train, label=7200): "Last year Jessica paid $1000 for rent, $200 for food, and $100 for car insurance each month. This year her rent goes up by 30%..." — Personal budget language but zero financial instrument vocabulary; the arithmetic is percentage application to fixed costs.
  - [D7] Example 35 (main, train, label=333200): "The price of a home is $98 per square foot (sq ft). The house is 2,400 sq ft..." — Real estate multiplication; no mortgage, interest rate, or amortization content.

#### CRITICAL Concern 3: Binary exact-match scoring is structurally misaligned with assumption-sensitive financial queries
- **Dimension(s):** OO
- **Observation:** All 80 sampled problems have a single unambiguous correct integer or decimal answer, and the answer field terminates with a `#### N` final-answer marker that is compared by exact match. There is no mechanism in the dataset for range-based answers, tolerance bands, or assumption-pinned variants. Even the one interest problem (Example 43) has a single correct answer because the problem explicitly pins the interest type as "simple."
- **Deployment relevance:** The deployment team confirmed that a meaningful fraction of target queries (credit card payoff timelines, effective vs. nominal APR comparisons, amortization total interest) have legitimate answer ranges depending on compounding frequency, issuer minimum payment formulas, and assumed timing conventions. Evaluating a chatbot on such queries using GSM8K's binary scoring scheme would penalize correct answers that use different but valid assumptions, and reward numerically matching but reasoning-flawed answers.
- **Datapoint citations:**
  - [D4] Example 43 (main, train, label=720): "In the second year, she earns the same amount of interest, which $60 + $60 = $120 ... #### 720" — Single labeled answer; if this were compound interest, the correct answer would be $726, and neither answer would be accepted under the other's label.
  - [D9] Example 45 (main, train, label=120): "Let N be the original price each friend was going to pay. 10N=6(N+8) ... #### 120" — Algebraic problem with one exact solution; illustrates the scoring schema's assumption that each well-posed problem has exactly one correct numeric answer.
  - [D2] Example 19 (main, train, label=54): "Bobby has 16 toy cars, and the number of cars he has increases by 50% every year. How many toy cars will Bobby have in three years?" — Growth problem stated additively rather than as compound growth; the single answer 54 would be wrong if interpreted as exponential compounding (which would yield the same result here coincidentally, but the method differs significantly for financial instruments where compounding convention matters).

---

#### MAJOR

#### MAJOR Concern 4: Difficulty ceiling — grade-school arithmetic does not proxy financial instrument complexity
- **Dimension(s):** IO
- **Observation:** The arithmetic operations present in the sampled problems are: addition, subtraction, multiplication, division, simple percentage application, basic ratios, and single-variable algebra. The hardest sampled problem (Example 23, car collection algebra) requires solving a two-variable linear equation. No problem requires iterative computation across multiple periods, recursive formula application, or manipulation of annuity formulas.
- **Deployment relevance:** Multi-month amortization, compound interest over years, and break-even analysis on balance transfers require iterative application of financial formulas that exceed grade-school arithmetic by structural complexity, not just magnitude. A model that achieves 80%+ on GSM8K may still fail on the deployment's hardest queries (amortization over 360 months, effective APR computation) because those queries demand different reasoning patterns entirely, not just harder arithmetic.
- **Datapoint citations:**
  - [D2] Example 19 (main, train, label=54): "Bobby has 16 toy cars, and the number of cars he has increases by 50% every year. How many toy cars will Bobby have in three years?" — Year-over-year growth computed by iterating 3 times; a full amortization schedule would require 360 iterations with changing principal — a categorically different computational demand.
  - [D11] Example 23 (main, train, label=220): "Jim has 4 times as many Buicks as Fords, and 3 more than twice the number of Fords than Chevys. How many Buicks does Jim have?" — Most algebraically complex sampled problem; single-variable linear equation, far below the complexity of compound interest or loan amortization formulas.
  - [D3] Example 43 (main, train, label=720): "Ariella's account earns her simple interest at the rate of 10% per annum... how much money will Arialla have after two years?" — Only two periods computed; compound interest over 10 or 30 years would require a formula (P(1+r)^n) rather than repeated addition — a structural leap.

#### MAJOR Concern 5: No signal on financial context disambiguation
- **Dimension(s):** IC
- **Observation:** In the sampled problems, all quantities are fully specified numerically in the problem statement. No problem requires a model to recognize that a described quantity maps to a specific financial formula, to disambiguate between nominal and effective rates, or to identify when a stated rate implies a particular compounding convention. The problems that use percentages always state them as direct multipliers applied once.
- **Deployment relevance:** In the deployment, users will phrase queries like "my APR is 24%, how long to pay off $3,000 if I pay $100/month?" — requiring the model to (a) recognize that APR implies monthly periodic rate = APR/12, (b) apply a loan payoff formula, and (c) handle the iterative nature of the calculation. GSM8K trains no part of this disambiguation and formula-selection reasoning.
- **Datapoint citations:**
  - [D5] Example 30 (main, train, label=7200): "This year her rent goes up by 30%... $1000 * .3 = $300" — Percentage applied as a direct multiplier to a single base; no periodic compounding, no formula selection, no disambiguation of rate type.
  - [D6] Example 44 (main, train, label=11000): "He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value." — Percentage-of-face-value calculation; the rate type is unambiguous and the operation is a single multiplication.
  - [D21] Example 43 (main, train, label=720): "Ariella's account earns her simple interest at the rate of 10% per annum" — The problem explicitly labels the rate type ("simple interest"), removing the disambiguation challenge that real financial queries present.

---

#### MINOR

#### MINOR Concern 6: Socratic config growth-problem framing is additive, not exponential
- **Dimension(s):** IF, OO
- **Observation:** Example 19 in the socratic config (50% annual growth in toy cars) is computed by iterating addition: new cars = prior_total × 0.5, then added to prior total. While mathematically equivalent for this 3-year problem, the framing trains a model to approach growth problems additively rather than through the compound formula P(1+r)^n. For a financial chatbot, this framing could reinforce the incorrect "multiply then add" approach that leads to errors on longer time horizons.
- **Deployment relevance:** Minor: the difference is negligible for small n and the benchmark makes no claim to teach formula selection. But it is a concrete signal that the benchmark's implicit pedagogy may not transfer to financial instrument reasoning, even for problems that superficially resemble growth scenarios.
- **Datapoint citations:**
  - [D15] Example 19 (socratic, train, label=54): "How many new cars will Bobby acquire in the first year? ** In the first year, Bobby will acquire 16 * .5 = 8 new cars. ... After the third year, he will have 36 + 18 = 54 cars in total." — Step-by-step addition of new cars per period rather than formula application; same pattern would diverge from correct answers at year 10+ under compound vs. simple growth interpretation.

#### MINOR Concern 7: Dollar-amount problems use simplified tax and pricing conventions
- **Dimension(s):** IC
- **Observation:** The monetary problems in the sample use simple dollar amounts and do not reflect US tax conventions (sales tax, income tax withholding), APY vs. APR distinctions, or any financial regulatory context. Tax appears once (Example 22) as a flat dollar add-on with no percentage derivation. Prices are always whole dollars or simple decimals; no problem involves interest accrual, fees, or conditional charges.
- **Deployment relevance:** Minor, since the benchmark does not claim to test tax or regulatory knowledge. However, it means the benchmark's monetary vocabulary provides no scaffolding for a model that needs to handle real US financial product pricing conventions (e.g., balance transfer fees as a percentage of transferred balance, or daily periodic rate derived from APR).
- **Datapoint citations:**
  - [D16] Example 22 (main, train, label=80): "He was charged $7.22 total for tax." — Tax appears as a pre-computed lump sum, not as a rate applied to a base; no percentage derivation required.
  - [D14] Example 3 (main, train, label=99): "They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag." — Consumer purchase at stated unit prices; no sales tax, no discount structure, no conditional fee.

---

### Content Coverage Summary

The 80 sampled examples confirm that GSM8K is uniformly composed of grade-school arithmetic word problems set in everyday consumer, school, sports, and household contexts. Problem domains include: food and candy purchases (Examples 2, 3, 25), sports scoring (Example 18), animals and pets (Examples 12, 36), retail and toy purchases (Examples 16, 22, 32), travel and time (Examples 7, 15, 26, 40), simple budgeting (Examples 13, 30), and one explicit savings/interest problem (Example 43, simple interest only). Monetary quantities appear in roughly 40–50% of sampled problems, but invariably as simple multiplicative or additive computations without financial-instrument logic.

The language register is plain American English at approximately a 5th–8th grade reading level, with proper names drawn from a diverse set (Kantana, Omi, Ariella, Amalie), consistent with the documented linguistic diversity goal. All arithmetic annotations use the `<<expr=result>>` inline format and all answers terminate with `#### N`. The socratic config adds sub-question scaffolding to the same problem set, providing a finer-grained reasoning trace.

No example in the sample involves APR, compound interest, amortization, credit cards, minimum payments, balance transfers, credit utilization, or any other consumer finance instrument. The one interest-bearing problem (Example 43) uses simple interest with explicit problem-statement labeling, providing no information about a model's ability to handle compound interest or financial-term disambiguation.

---

### Limitations

1. **Sample size and distribution**: 80 examples from 7,473 training examples represent ~1% of the training set. It is possible — though unlikely given the documented scope — that financial-instrument problems exist elsewhere in the corpus; the sample cannot rule this out with certainty.

2. **Test split not sampled**: All examples are from the training split. If the test split contains categorically different problem types (e.g., more financial-adjacent content), this analysis would not capture that. Given the benchmark's design principles, this is unlikely, but unverifiable from the current sample.

3. **Scoring infrastructure not inspectable**: The `<<expr=result>>` annotation format is visible in the data, but the actual evaluation harness (Python `eval` override at test time, calculator bug behavior) is not inspectable from the HF dataset alone. The paper's documented ~1% performance impact from calculator bugs cannot be confirmed from the data.

4. **Annotator demographics unverifiable**: No annotator metadata is present in the HF dataset or dataset card. Claims about Upwork/Surge AI contractor provenance cannot be verified from the data itself.

5. **Socratic config structural identity**: The socratic config appears to be a reformatted version of the same underlying problems as the main config (all 33 socratic examples match the first 33 main examples). This limits the diversity contribution of the second config for coverage assessment.

