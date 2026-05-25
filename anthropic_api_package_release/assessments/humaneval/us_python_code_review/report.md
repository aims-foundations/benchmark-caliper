## Deployment Context

We are a US code review platform building a feature that scans existing Python codebases, identifies likely bugs, and suggests fixes for American development teams doing code review. The system reads existing code, detects defects (logic errors, off-by-one bugs, null reference issues), and proposes corrections. We need to evaluate the LLM's ability to understand and reason about existing code.

# Validity Analysis: humaneval
**Target context:** US Professional Software Development Teams — Code Review / Bug Localization
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 3 | Moderate gaps | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form | 2 | Significant gaps | high |
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

HumanEval is fundamentally misaligned with the US professional code review / bug localization deployment across all five HIGH and MODERATE priority dimensions. The benchmark measures docstring-to-function synthesis on clean algorithm puzzles scored by author-written unit tests [Q1, Q22, Q77]; the deployment requires bug localization and diff generation against existing, framework-heavy, sparsely-documented Python code, evaluated by professional reviewer acceptance (elicitation Q1–Q3). All four HIGH-priority dimensions (IO, IC, OO, OC) score 1, confirmed by both verbatim quotes from the paper acknowledging the relevant gaps [Q48, Q63, Q88, Q102, Q104, Q129, Q225] and dataset inspection showing 100% of sampled problems follow the misaligned pattern [DATASET-D1, DATASET-D8, DATASET-D29]. Input form (LOWER priority) partially aligns at the modality level (Python plain-text) and scores 3. Output form (MODERATE priority) is structurally divergent (complete function vs. unified diff) and scores 2. Web-sourced findings further weaken HumanEval's utility: benchmark saturation [WEB-17] erodes discriminative power, and the best Python-native alternative (SWE-bench) still suffers from ~29.6% test-pass-vs-oracle divergence [WEB-3], confirming that even moving to SWE-bench would not fully address the deployment's primary OO/OC concerns. No public benchmark uses human reviewer merge-acceptance as ground truth [WEB-8].

## Practical Guidance

### What This Benchmark Measures

HumanEval measures Python algorithmic reasoning ability when given a clean, accurate, complete natural-language specification — a narrow construct dominated by interview-style and competitive-programming-style problems [Q22, Q131, DATASET-D2, DATASET-D26]. For this deployment, it provides only a weak lower-bound signal on the implicit code-comprehension prerequisite (deployment task (a)) and offers no signal on the primary tasks of bug localization (b) or diff generation (d). The Input Form dimension is the only one where HumanEval provides genuine alignment (both contexts are plain-text Python).

### Construct Depth

Shallow with respect to the deployment's constructs. HumanEval probes single-function, single-call-site, primitive-typed algorithmic synthesis. It does not probe: localization accuracy, semantic preservation, convention adherence, framework-specific defect detection, long-context reasoning over realistic calling environments, or behavior under sparse/stale/misleading documentation. The paper's own Appendix D proposes deeper qualitative metrics but defers them [Q148, Q149], and benchmark saturation [WEB-17] further compresses the discriminative range. Even the best-available alternative, SWE-bench, has documented oracle-inflation issues of ~6.4 percentage points [WEB-3] on a related Python defect-repair construct.

### What Else You Need

Substantial supplementation required across IO, IC, OO, and OC: (1) Add SWE-bench Verified for real-Python-repo localization + patch tasks including Django/NumPy/pandas instances [WEB-1], applying SWE-ABS-style strengthened tests to mitigate oracle inflation [WEB-2]; (2) Add BugsInPy for function-level bug localization on scientific Python [WEB-4, WEB-5]; (3) Build a deployment-specific evaluation set using customer-representative codebases with framework-specific defects (SQLAlchemy, Flask routing) — no public benchmark covers this [WEB-9]; (4) Operationalize human reviewer acceptance via internal annotation by US professional developers, since no public benchmark uses merge-acceptance ground truth [WEB-8]; (5) Curate a sparse/stale/misleading-documentation evaluation subset, since this condition is unaddressed by any public benchmark [WEB-9]. Plan for NIST SP 800-218A SSDF Community Profile compliance [WEB-16] given the AI-assisted code modification scope.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
HumanEval's task taxonomy is exclusively docstring-to-function synthesis [Q1, Q22], with a secondary docstring-from-code task [Q133]. The deployment's two HIGH-priority task types — bug localization in existing code and diff generation against buggy bodies — are entirely absent. Dataset inspection confirms 100% of sampled examples follow the clean-spec generate-from-scratch pattern [DATASET-D1, DATASET-D10, DATASET-D24]. The paper itself acknowledges that 'most past studies of the impacts of code generation models consider performance on a closed set of tasks in a simulated environment' [Q225]. Even Codex-S's auxiliary training distribution (competitive programming + CI-traced utilities) targets generation-from-spec rather than defect-detection [Q60, Q61]. This is a fundamental ontology mismatch on a HIGH-priority dimension.

**Strengths:**
- HumanEval provides a clean lower-bound signal on pure algorithmic Python reasoning, which is an implicit prerequisite for code comprehension in review settings [DATASET-D4, Q22]
- Self-contained problems on primitive types make scores interpretable as algorithmic ability free from framework confounds [DATASET-D2, DATASET-D18]

**Checklist:**

- **IO-1**: Deployment requires (b) bug localization and (d) diff/fix generation as primary tasks, with (a) code comprehension as prerequisite and (c) bug classification as secondary. Bug localization and diff generation are entirely out of HumanEval's task ontology [DATASET-D1, DATASET-D10]. — _Sources: Q1, Q22, DATASET-D1, DATASET-D10_
- **IO-2**: Yes — bug localization, diff generation, and reasoning over existing buggy code are all omitted. The paper explicitly defines the task as 'synthesizing programs from docstrings' [Q1, Q22] and Appendix D's proposed qualitative taxonomy [Q148, Q149, Q153, Q154, Q155] is preliminary and deferred, not operationalized. — _Sources: Q1, Q22, Q148, Q149_
- **IO-3**: The benchmark's algorithm/interview-puzzle framing [Q22, Q131, DATASET-D15, DATASET-D26] is largely irrelevant to the deployment's defect classes (SQLAlchemy N+1, Django ORM lazy-load, NumPy broadcasting). Bias probes [Q186, Q187, Q188] and cryptographic-security probes [Q204, Q205] are not relevant to the bug-localization/code-review deployment. — _Sources: Q22, Q131, DATASET-D15, DATASET-D26, Q186, Q204_
- **IO-4**: Category gaps: (1) no bug-localization tasks, (2) no diff/patch generation, (3) no reasoning over existing buggy code, (4) no framework-specific defect classes. These omissions are construct-underrepresentation failures for the deployment's primary capabilities. — _Sources: Q225, WEB-17, DATASET-D1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'We introduce Codex, a GPT language model finetuned on publicly available code from GitHub, and study its Python code-writing capabilities.' (p.1)
- [Q22] 'Programming tasks in the HumanEval dataset assess language comprehension, reasoning, algorithms, and simple mathematics.' (p.4)
- [Q60] 'For this reason, functions from tracing tended to be the building blocks of command-line utilities.' (p.8)
- [Q61] 'To excel at these tasks, the model does not need to know advanced algorithms and data structures. Rather, it needs to be able to follow instructions to implement the functionality specified in the docstring.' (p.8)
- [Q225] 'Most past studies of the impacts of code generation models consider performance on a closed set of tasks in a simulated environment.' (p.35)

*Web sources:*
- [WEB-17] HumanEval is saturated (>94% pass on top models) and known to have benchmark-overfitting issues, further weakening its discriminative power for the deployment's tasks

*Dataset analysis:*
- DATASET-D1: HumanEval/61 — clean docstring-to-function bracket matching; no existing code to localize defect in
- DATASET-D10: HumanEval/88 — clean spec, empty body, generate-from-scratch pattern
- DATASET-D24: HumanEval/109 — complete accurate docstring with rotation-sort task; pattern is uniformly generate-from-scratch across the 40-sample inspection

</details>

**Information gaps:**
- No purpose-built benchmark targeting bug localization with line-range scoring was identified in the regional context (gap_1 partially resolved by SWE-bench/BugsInPy but neither fully covers line-range localization)

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
HumanEval problems are hand-written algorithm/interview puzzles operating on primitive Python types [Q14, Q19, Q22], with imports limited to `typing`, `math`, `random`, `string` in the sampled examples [DATASET-D4, DATASET-D5]. None of the deployment's framework-heavy input distribution — Django views, Flask routing, SQLAlchemy session lifecycles, NumPy broadcasting, pandas operations — appears in the benchmark. The paper itself acknowledges the distribution mismatch: 'Python code found on GitHub contains class implementations, configuration files, scripts... we hypothesize that the distribution mismatch reduces HumanEval performance' [Q48]. Equally critical for this deployment, all sampled docstrings are clean, accurate, and complete [DATASET-D9, DATASET-D3], whereas the deployment explicitly requires reasoning over absent, stale, or misleading documentation. The paper gestures toward this gap ('intent is [not always] captured sufficiently enough in comments and documentation' [Q217]) but does not evaluate it. Two HIGH-priority IC failures stack on a single dimension.

**Strengths:**
- Hand-written problems mitigate training-data contamination risk by design [Q14, Q21], though this strength is partially eroded by reported benchmark saturation [WEB-17]
- Problems are linguistically English-native and Python-native, matching the deployment's language assumptions [DATASET-D4]

**Checklist:**

- **IC-1**: Inputs do not require region-specific cultural or geographic knowledge — they are algorithm puzzles on primitive types [DATASET-D2, DATASET-D17]. This is not a positive feature for this deployment, which instead requires framework-specific and codebase-specific knowledge. — _Sources: DATASET-D2, DATASET-D17_
- **IC-2**: Not applicable in the cultural sense — relevant heterogeneity is codebase/framework, not demographic. The benchmark's algorithmic content does not align with the deployment's framework-heavy content [Q48, DATASET-D13]. — _Sources: Q48, DATASET-D13_
- **IC-3**: No Western-specific cultural transfer issue, but the algorithmic-puzzle content is generally irrelevant to professional code review work [Q22, DATASET-D13, DATASET-D15]. — _Sources: Q22, DATASET-D13, DATASET-D15_
- **IC-4**: INSUFFICIENT DOCUMENTATION — paper does not describe annotator demographics or recruit professional software engineers for input curation. The paper notes 'limited research on the demographic distribution of Python users' [Q219]. — _Sources: Q219_
- **IC-5**: Documented content gaps: (1) no framework code (Django/Flask/SQLAlchemy/NumPy/pandas), (2) no legacy code patterns, (3) no sparse/stale/misleading docstrings, (4) no long-context calling environments. These omissions are construct-irrelevant-variance failures: high HumanEval performance does not predict deployment performance [Q48, Q88, WEB-9]. — _Sources: Q48, Q88, Q217, WEB-1, WEB-4, WEB-9, DATASET-D4, DATASET-D9_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q14] 'Though not a guarantee for problem novelty, all problems were hand-written and not programmatically copied from existing sources.' (p.3)
- [Q19] 'We evaluate functional correctness on a set of 164 hand-written programming problems, which we call the HumanEval dataset.' (p.4)
- [Q48] 'Python code found on GitHub contains class implementations, configuration files, scripts, and even files used to store data. This code is seemingly unrelated to synthesizing functions from docstrings, and we hypothesize that the distribution mismatch reduces HumanEval performance.' (p.7)
- [Q88] 'Codex struggles to parse through increasingly long and higher-level or system-level specifications.' (p.10)
- [Q217] 'one of the challenges of code generation stem from relying on the assumption that intent is captured sufficiently enough in comments and documentation to not compromise accuracy.' (p.33)

*Web sources:*
- [WEB-9] Removing semantic cues such as docstrings causes severe model degradation, but no benchmark deliberately curates absent/stale/misleading docstrings as an input condition
- [WEB-1] SWE-bench includes Django, NumPy, pandas, scikit-learn, matplotlib instances — the framework distribution HumanEval lacks
- [WEB-4] BugsInPy contains 493 real bugs across 17 Python projects including pandas and scikit-learn — what HumanEval would need to approximate the deployment

*Dataset analysis:*
- DATASET-D4: HumanEval/0 uses only `typing` import — no Django/Flask/SQLAlchemy/NumPy in sample
- DATASET-D13: HumanEval/67 fruit_distribution — toy word-problem with zero real-world deployment relevance
- DATASET-D9: HumanEval/17 — complete inline legend for ASCII music notation; deployment's legacy utilities never have this level of inline documentation
- DATASET-D14: HumanEval/38 decode_cyclic is the sparsest docstring in the sample but the encode function is fully provided as context — still a clean-spec condition

</details>

**Information gaps:**
- Whether any of the unsampled 124 HumanEval problems involve framework-specific code (very unlikely given paper's stated scope [Q22], but not exhaustively verified)

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
Input form is the only dimension with substantive partial alignment. Both benchmark and deployment operate on plain-text Python source [Q20, Q29, DATASET-D4], with no modality mismatch (no audio, image, or non-text concerns). The IF priority is explicitly marked LOWER in elicitation. However, two form-level concerns remain: (1) HumanEval prompts are short, self-contained function signatures with clean docstrings [Q20, DATASET-D9], whereas deployment inputs include 100–1000+ line calling contexts that stress long-context reasoning [Q88]; (2) the structural assumption that a complete, accurate docstring precedes the function body [Q20, Q28] does not hold in the deployment, though this is more accurately characterized as content-level than form-level. The paper does not evaluate inputs with absent or partial documentation as a form variable.

**Strengths:**
- Plain-text Python input matches deployment modality exactly — no audio, image, or cross-modal concern [Q20, DATASET-D4]
- Standardized prompt format with stop sequences [Q29] is structurally similar to how production code-review tools assemble prompts

**Checklist:**

- **IF-1**: Signal distributions match at the modality level: both are UTF-8 plain-text Python source [Q20, DATASET-D4]. Length distributions diverge — HumanEval prompts are short single-function units while deployment inputs include extended calling context [Q88]. — _Sources: Q20, Q88, DATASET-D4_
- **IF-2**: Not applicable in the infrastructure sense — both contexts use the same text encoding and Python runtime; no capture-device mismatch exists.
- **IF-3**: Domain-specific form difference: HumanEval assumes prompt structure of [signature + docstring + body prefix] [Q20, Q28]; deployment inputs may have no docstring or a misleading one, and may include surrounding class/module context. This is partially structural and partially content-driven. — _Sources: Q20, Q28, DATASET-D31_
- **IF-4**: Form mismatches: (1) prompt length distribution narrower in benchmark than deployment, (2) benchmark assumes docstring presence as a structural feature [Q20]. Both are minor relative to ontology/content concerns on this LOWER-priority dimension. — _Sources: Q20, Q88_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q20] 'Each problem includes a function signature, docstring, body, and several unit tests, with an average of 7.7 tests per problem.' (p.4)
- [Q28] 'To compute pass@k, we assemble each HumanEval problem into a prompt consisting of a header, a signature, and a docstring' (p.4)
- [Q29] 'We sample tokens from Codex until we encounter one of the following stop sequences' (p.4)
- [Q88] 'Codex struggles to parse through increasingly long and higher-level or system-level specifications.' (p.10)

*Dataset analysis:*
- DATASET-D4: HumanEval/0 confirms plain-text Python prompt format matching deployment modality
- DATASET-D31: HumanEval/38 (encode_cyclic context) is the closest the benchmark comes to providing existing code as context, but it is helper-function context, not a buggy body to localize defects in

</details>

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
HumanEval's output ontology is binary unit-test pass/fail [Q8, Q13, Q77], operationalized via pass@k [Q15]. The deployment requires a multi-component judgment: localization accuracy + diff acceptability + semantic safety + convention adherence, with human reviewer acceptance as the primary criterion (Q3 elicitation response). The paper itself acknowledges pass@k's oracle-selection problem [Q36, Q37, Q38] and the gap between test-passing and developer-intent satisfaction [Q102, Q103, Q104, Q166]. Dataset inspection confirms thin test coverage (HumanEval/104 has 4 assertions including `assert True` [DATASET-D2]) and a known case where the canonical solution itself contains an operator-precedence bug [DATASET-D29]. Web-sourced evidence on the next-best alternative (SWE-bench) reveals that even there, ~29.6% of test-passing patches diverge behaviorally from oracle patches and ~7.8% fail the full test suite [WEB-2, WEB-3] — empirically validating the deployment's concern that test-pass is insufficient for the primary success criterion. No HumanEval output category captures localization correctness, semantic preservation, or convention adherence.

**Strengths:**
- Functional correctness via executable tests is more meaningful than match-based metrics like BLEU [Q9, Q10, Q40] — a defensible methodological choice for the benchmark's own task
- Test structure is transparent and inspectable [DATASET-D1, DATASET-D7], so consumers can see exactly what is being measured

**Checklist:**

- **OO-1**: Output category space is a single binary (pass/fail) [Q8, Q77]. Deployment requires categories like {correct localization, diff acceptable, semantic-preserving, convention-adherent, bug-masking, regression-introducing} — none present. — _Sources: Q8, Q77, DATASET-D2_
- **OO-2**: Missing categories: localization accuracy (line/range), diff quality, semantic preservation, convention adherence, reviewer acceptability. Appendix D proposes richer qualitative metrics [Q148, Q149] but defers them to a forthcoming paper. — _Sources: Q148, Q149_
- **OO-3**: The binary pass/fail rule encodes the assumption that unit tests can stand in for developer intent — explicitly contradicted by the deployment's elicitation response (Q3) and by the paper's own alignment discussion [Q102, Q103, Q104]. — _Sources: Q102, Q103, Q104_
- **OO-4**: Stakeholder-driven taxonomy redesign would be necessary: human reviewer accept/reject as primary label, with sub-labels for localization, semantic safety, and convention adherence. No public benchmark currently uses merge-acceptance ground truth [WEB-8 partial precedent only]. — _Sources: WEB-8_
- **OO-5**: Taxonomy issues: (1) binary output collapses multi-component judgment, (2) underspecified prompts cause valid solutions to be wrongly penalized [Q63], (3) ~29.6% behavioral divergence between test-pass and oracle even on SWE-bench [WEB-3]. These violate structural validity and external validity on a HIGH-priority dimension. — _Sources: Q63, WEB-2, WEB-3, DATASET-D29_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q8] 'we begin by defining the pass@k metric... and explain its advantages over standard match-based metrics' (p.2)
- [Q77] 'When we benchmark our code generation models, we measure pass@k on the HumanEval dataset, where correctness is defined by passing a set of unit tests.' (p.9)
- [Q36] 'Pass@k can also be interpreted as the result of evaluating the best out of k samples, where the best sample is picked by an oracle with prior knowledge of the unit tests.' (p.5)
- [Q63] 'Some prompts underspecify the function that is implemented, in which case a perfectly valid solution may be wrongly penalized by the unit test.' (p.8)
- [Q102] 'Codex will generate code that is as similar as possible to its training distribution.' (p.11)
- [Q104] 'This is an alignment failure - the model is not aligned with the user's intentions.' (p.11)
- [Q148] 'This entails evaluating the ability to reason over computations and states at different levels of abstractions' (p.25)

*Web sources:*
- [WEB-3] ~29.6% of plausible SWE-bench patches diverge behaviorally from oracle patches; ~7.8% fail full developer test suite — empirical validation that test-pass is insufficient
- [WEB-2] SWE-ABS rejected 19.78% of previously-passing patches when applying strengthened tests, dropping top agent from 78.80% to 62.20%
- [WEB-8] DPO-F+ formalizes developer-preference alignment for code repair but operates as alignment signal, not benchmark ground truth — confirmed gap in human-reviewer-acceptance benchmarks

*Dataset analysis:*
- DATASET-D2: HumanEval/104 has only 4 assertions including `assert True` no-op — thin coverage could pass incorrect solutions
- DATASET-D22: HumanEval/130 test depends on exact float-vs-int type — semantically equivalent integer solution would fail despite logical correctness
- DATASET-D29: HumanEval/124 canonical solution contains operator-precedence bug — direct confirmation that benchmark's own ground truth is not always correct

</details>

**Requires expert verification:**
- Whether any deployment-internal evaluation harness uses merge-acceptance proxies that could supplement HumanEval

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Ground-truth labels in HumanEval are produced by benchmark-author-written unit tests, not by professional software engineers acting as code reviewers. The paper documents no annotator demographics, no inter-annotator agreement procedure, and no professional-developer validation [Q129, Q219]. The only human-graded subset is docstring generation: 10 samples per problem, 1,640 total items, single model, single temperature [Q79] — not bug-fix evaluation. The paper itself flags label reliability concerns: 'Some prompts underspecify the function that is implemented, in which case a perfectly valid solution may be wrongly penalized by the unit test' [Q63], and 'human developers often write test suites with limited but targeted coverage, but this does not always work well against an algorithm' [Q129]. Dataset inspection confirms concrete quality issues in canonical solutions: an operator-precedence bug in HumanEval/124 [DATASET-D29], a docstring formula typo in HumanEval/32 [DATASET-D21], formatting errors in HumanEval/158 and HumanEval/19 [DATASET-D28, DATASET-D30], and bare `except:` clauses in canonical solutions that violate professional Python conventions [DATASET-D20, DATASET-D7]. For the deployment's HIGH-priority OC dimension, none of these labels approximate professional reviewer judgment.

**Strengths:**
- Functional correctness labels are reproducible and auditable [Q15, DATASET-D1] — better than subjective single-annotator judgment for the benchmark's own task
- The paper transparently acknowledges its label-reliability limits [Q63, Q129]

**Checklist:**

- **OC-1**: Ground-truth labels do not reflect US professional software engineer reviewer perspectives — they reflect benchmark-author-written unit tests [Q14, Q77]. No reviewer-acceptance signal exists. — _Sources: Q14, Q77_
- **OC-2**: High potential for disagreement: the deployment's elicitation response (Q3) explicitly states test-passing fixes can be rejected for semantic/convention reasons. Canonical solutions using bare `except:` [DATASET-D20] would likely be rejected in PEP-8/Google-Style-enforced codebases. — _Sources: Q63, DATASET-D20, DATASET-D7_
- **OC-3**: INSUFFICIENT DOCUMENTATION — the paper provides no Datasheet, Data Statement, or annotator demographic breakdown. It explicitly notes 'there is unfortunately only limited research on the demographic distribution of Python users' [Q219]. — _Sources: Q219_
- **OC-4**: Re-annotation by US professional reviewers would be needed to align labels with deployment ground truth. Even alternative benchmarks like SWE-bench use test-pass proxies rather than merge-acceptance [WEB-3, WEB-8]. — _Sources: WEB-3, WEB-8_
- **OC-5**: INSUFFICIENT DOCUMENTATION — paper does not describe aggregation across annotators because there are effectively no annotators beyond the authors; inter-annotator agreement is not reported.
- **OC-6**: Label issues: (1) test-author labels are not reviewer-acceptance labels [Q63, Q129], (2) confirmed canonical-solution bugs [DATASET-D29], (3) confirmed docstring typos [DATASET-D21, DATASET-D28, DATASET-D30], (4) bare `except:` violates professional conventions [DATASET-D20]. These violate convergent validity and external validity on a HIGH-priority dimension. — _Sources: Q63, Q129, DATASET-D29, DATASET-D21, DATASET-D28, DATASET-D30, DATASET-D20_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q14] 'all problems were hand-written and not programmatically copied from existing sources.' (p.3)
- [Q63] 'Some prompts underspecify the function that is implemented, in which case a perfectly valid solution may be wrongly penalized by the unit test.' (p.8)
- [Q77] 'correctness is defined by passing a set of unit tests.' (p.9)
- [Q79] 'we only grade 10 samples per problem, for a total of 1640 problems, from Codex-D-12B at temperature 0.8.' (p.9)
- [Q129] 'Human developers often write test suites with limited but targeted coverage, but this does not always work well against an algorithm, highlighting the challenges of evaluating correctness of programs.' (p.14)
- [Q219] 'There is unfortunately only limited research on the demographic distribution of Python users.' (p.33)

*Web sources:*
- [WEB-3] Even SWE-bench (the best Python alternative) does not use human reviewer acceptance — ~29.6% of test-passing patches diverge from oracle behavior
- [WEB-8] DPO-F+ is the closest precedent for developer-preference alignment in code repair, but no benchmark uses merge-acceptance as primary ground truth — confirmed gap

*Dataset analysis:*
- DATASET-D29: HumanEval/124 canonical solution contains operator-precedence bug — concrete confirmation that ground-truth labels are not always correct
- DATASET-D21: HumanEval/32 docstring formula typo (`xs[1]` should be `xs[2]`)
- DATASET-D28: HumanEval/158 docstring contains formatting typo
- DATASET-D30: HumanEval/19 misspells 'numerals' as 'numberals' in the specification
- DATASET-D20: HumanEval/105 canonical solution uses bare `except: pass` — violates PEP 8 / Google Python Style Guide
- DATASET-D7: HumanEval/124 canonical solution wraps body in broad try/except — masks defects, contrary to deployment's no-bug-masking requirement

</details>

**Information gaps:**
- Annotator demographics and inter-annotator agreement procedures are not documented anywhere in the paper

---

### Output Form — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Output form is partially aligned at the modality level: both produce Python code [Q2, DATASET-D8]. However, HumanEval's output unit is a complete standalone function body generated token-by-token with stop sequences [Q29], whereas the deployment requires a targeted unified diff with line-range localization metadata, file path, and bug-type label. These are structurally divergent outputs even though both are 'Python text.' The paper acknowledges the practical single-completion challenge [Q37, Q38] and offers only a mean-log-probability heuristic [Q39] rather than any patch/diff format. No HumanEval evaluation tests line-range localization output, unified-diff structural correctness, or minimality of change. Dataset inspection confirms every sampled problem produces complete function bodies, not diffs [DATASET-D8, DATASET-D6]. OF is marked MODERATE priority in the elicitation, so the partial alignment at modality level provides some signal — but the structural mismatch on output unit is meaningful.

**Strengths:**
- Python text output matches deployment output modality [Q2, DATASET-D8]
- Stop-sequence-based generation [Q29] is structurally compatible with extracting function-scoped fragments, which could be adapted for diff context

**Checklist:**

- **OF-1**: Output modality (Python text) matches [Q2, DATASET-D8], but output unit (complete function body vs. unified diff with localization metadata) does not. The deployment's required output form is structurally absent from HumanEval. — _Sources: Q2, DATASET-D8_
- **OF-2**: Not applicable — speech/TTS not in scope; both contexts are text-based.
- **OF-3**: Not applicable in the literacy sense — target population is professional software engineers; the relevant accessibility consideration is whether output format integrates into PR review UIs (unified diff), which HumanEval does not provide.
- **OF-4**: Form mismatches: (1) complete function body vs. targeted diff, (2) no line-range localization metadata, (3) no file-path or bug-type labels. These violate external validity for diff-based review tooling, though OF is MODERATE-priority [Q37, Q38, DATASET-D8]. — _Sources: Q37, Q38, DATASET-D8, WEB-1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'On HumanEval, a new evaluation set we release to measure functional correctness for synthesizing programs from docstrings' (p.1)
- [Q29] 'We sample tokens from Codex until we encounter one of the following stop sequences' (p.4)
- [Q37] 'we are also interested in the setting where we must select a single sample from k samples without having access to an oracle.' (p.5)
- [Q38] 'when the model is used as an autocomplete tool where a user provides a prompt, we do not have unit tests, but would like to return only a single completion to the user' (p.5)

*Web sources:*
- [WEB-1] SWE-bench uses unified-diff patches as the output format — the closest match for the deployment's required form, though it does not score line-range localization separately (gap_7 partially resolved)

*Dataset analysis:*
- DATASET-D8: HumanEval/42 canonical output is full function body `return [(e + 1) for e in l]` — no diff structure, no localization metadata
- DATASET-D6: HumanEval/38 produces complete new function body even when helper context is provided, not a targeted diff

</details>

**Information gaps:**
- Whether SWE-bench's diff scoring would be a near-drop-in replacement for HumanEval's output-form contract (gap_7 deferred)

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** HumanEval contains no bug localization or diff generation tasks — the deployment's two primary capabilities

**Recommendation:** Replace HumanEval as the primary evaluation with SWE-bench Verified (real Python repos, includes Django/NumPy/pandas/scikit-learn) and BugsInPy (493 bugs across 17 projects with reproducible failing tests) for the localization+repair capability; demote HumanEval to an algorithmic-reasoning prerequisite check only [WEB-1, WEB-4]

### Input Content ⚠

**Gap:** No framework-specific Python content (Django, Flask, SQLAlchemy, NumPy, pandas) and no sparse/stale/misleading documentation conditions

**Recommendation:** Construct an internal, customer-representative evaluation set drawn from real production Python codebases containing the deployment's defect taxonomy (SQLAlchemy N+1, Django ORM lazy-load, NumPy broadcasting, Flask routing). Explicitly stratify by documentation quality (well-documented / sparsely-documented / misleadingly-documented) since no public benchmark curates this dimension [WEB-9, Q48]

### Output Ontology ⚠

**Gap:** Binary pass/fail collapses the multi-component judgment (localization + semantic safety + convention adherence + reviewer acceptance) that the deployment requires

**Recommendation:** Operationalize a multi-label scoring rubric drawn from the elicitation: {localization_correct, fix_minimal, semantics_preserved, conventions_adhered, reviewer_would_merge}. Collect labels via professional developer annotators. Apply SWE-ABS-style strengthened test suites to mitigate the ~29.6% oracle-divergence problem documented even in SWE-bench [WEB-2, WEB-3, Q148]

### Output Content ⚠

**Gap:** Ground-truth labels are author-written unit tests, not professional reviewer judgments; canonical solutions contain confirmed bugs and convention violations

**Recommendation:** Recruit US professional software engineers (representative of the deployment's target reviewers) to re-annotate a representative evaluation slice using accept/reject judgments with documented inter-annotator agreement. Audit any reused HumanEval items for canonical-solution defects (e.g., HumanEval/124 operator-precedence bug) before scoring [DATASET-D29, DATASET-D20, Q63, Q129]

### Input Form

**Gap:** Prompt length distribution and absence of surrounding calling context do not stress the long-context reasoning the deployment requires

**Recommendation:** Include long-context evaluation items (100–1000+ lines of surrounding class/module context) drawn from real codebases, since HumanEval's narrow length distribution does not exercise this capability [Q88]

### Output Form

**Gap:** HumanEval emits complete function bodies; deployment requires unified diffs with line-range/file-path localization metadata

**Recommendation:** Adopt unified-diff output as the contract (matching SWE-bench's format [WEB-1]) and add explicit scoring for line-range localization accuracy, minimality of change, and well-formed patch structure — none of which HumanEval measures [Q37, Q38]

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "We introduce Codex, a GPT language model finetuned on publicly available code from GitHub, and study its Python code-writing capabilities." |
| Q2 | 1 | output_form | "On HumanEval, a new evaluation set we release to measure functional correctness for synthesizing programs from docstrings, our model solves 28.8% of the problems, while GPT-3 solves 0% and GPT-J solves 11.4%." |
| Q3 | 1 | output_form | "Furthermore, we find that repeated sampling from the model is a surprisingly effective strategy for producing working solutions to difficult prompts." |
| Q4 | 1 | output_form | "Using this method, we solve 70.2% of our problems with 100 samples per problem." |
| Q5 | 1 | input_ontology | "Careful investigation of our model reveals its limitations, including difficulty with docstrings describing long chains of operations and with binding operations to variables." |
| Q6 | 1 | input_ontology | "Finally, we discuss the potential broader impacts of deploying powerful code generation technologies, covering safety, security, and economics." |
| Q7 | 1 | input_ontology | "This paper describes several early Codex models, whose descendants power GitHub Copilot and the Codex models in the OpenAI API." |
| Q8 | 2 | output_ontology | "In this section, we discuss the details of our evaluation framework. We begin by defining the pass@k metric, and explain its advantages over standard match-based metrics. Next, we describe the dataset of hand-written problems, called "HumanEval," which we created in order to benchmark our models. Finally, we discuss the sandbox environment we used to safely execute model-generated code." |
| Q9 | 2 | output_form | "Generative models for code are predominantly benchmarked by matching samples against a reference solution, where the match can be exact or fuzzy (as in BLEU score)." |
| Q10 | 2 | output_form | "More fundamentally, match-based metrics are unable to account for the large and complex space of programs functionally equivalent to a reference solution." |
| Q11 | 2 | output_form | "We argue that this metric should be applied to docstring-conditional code generation as well." |
| Q12 | 2 | output_form | "Perhaps the most convincing reason to evaluate functional correctness is that it is used by human developers to judge code. A framework known as test-driven development dictates that software requirements be converted into test cases before any implementation begins, and success is defined by a program that passes these tests." |
| Q13 | 2 | output_ontology | "Kulal et al. (2019) evaluate functional correctness using the pass@k metric, where k code samples are generated per problem, a problem is considered solved if any sample" |
| Q14 | 3 | input_content | "Though not a guarantee for problem novelty, all problems were hand-written and not programmatically copied from existing sources." |
| Q15 | 3 | output_form | "To evaluate pass@k, we generate n ≥ k samples per task (in this paper, we use n = 200 and k ≤ 100), count the number of correct samples c ≤ n which pass unit tests, and calculate the unbiased estimator." |
| Q16 | 3 | output_form | "Calculating this estimator directly results in very large numbers and numerical instability." |
| Q17 | 3 | output_form | "One may be tempted to estimate pass@k with 1−(1−p̂)^k where p̂ is the empirical estimate of pass@1, but we show that it is biased in Appendix A." |
| Q18 | 3 | output_form | "Later, we provide evidence that BLEU score may not be a reliable indicator of functional correctness by showing that functionally inequivalent programs generated by our model (which are guaranteed to disagree with the reference solution on some input) often have higher BLEU scores than functionally equivalent ones." |
| Q19 | 4 | input_content | "We evaluate functional correctness on a set of 164 hand-written programming problems, which we call the HumanEval dataset." |
| Q20 | 4 | input_form | "Each problem includes a function signature, docstring, body, and several unit tests, with an average of 7.7 tests per problem." |
| Q21 | 4 | input_content | "It is important for these tasks to be hand-written, since our models are trained on a large fraction of GitHub, which already contains solutions to problems from a variety of sources." |
| Q22 | 4 | input_ontology | "Programming tasks in the HumanEval dataset assess language comprehension, reasoning, algorithms, and simple mathematics." |
| Q23 | 4 | input_content | "Our training dataset was collected in May 2020 from 54 million public software repositories hosted on GitHub, containing 179 GB of unique Python files under 1 MB." |
| Q24 | 4 | input_form | "We filtered out files which were likely auto-generated, had average line length greater than 100, had maximum line length greater than 1000, or contained a small percentage of alphanumeric characters." |
| Q25 | 4 | input_content | "After filtering, our final dataset totaled 159 GB." |
| Q26 | 4 | input_form | "We train Codex using the same learning rate as the corresponding GPT model, with a 175 step linear warmup and cosine learning rate decay." |
| Q27 | 4 | input_form | "We train for a total of 100 billion tokens, using the Adam optimizer with β1 = 0.9, β2 = 0.95, ε = 10−8, and a weight decay coefficient of 0.1." |
| Q28 | 4 | output_form | "To compute pass@k, we assemble each HumanEval problem into a prompt consisting of a header, a signature, and a docstring, which is illustrated in Figure 2." |
| Q29 | 4 | input_form | "We sample tokens from Codex until we encounter one of the following stop sequences: '\nclass', '\ndef', '\n#', '\nif', or '\nprint', since the model will continue generating additional functions or statements otherwise." |
| Q30 | 4 | output_form | "We use nucleus sampling (Holtzman et al., 2020) with top p = 0.95 for all sampling evaluation in this work." |
| Q31 | 5 | output_form | "model test loss follows a power law in model size (Kaplan et al., 2020), test loss after code fine-tuning follows a similar power law with functional form (N / 5.92×10^7)^-0.13 where N is the number of non-embedding parameters in the model." |
| Q32 | 5 | output_form | "When evaluating pass@k, it is important to optimize sampling temperature for the particular value of k." |
| Q33 | 5 | output_form | "We find that higher temperatures are optimal for larger k, because the resulting set of samples has higher diversity, and the metric rewards only whether the model generates any correct solution." |
| Q34 | 5 | output_form | "In particular, for a 679M parameter model, the optimal temperature for pass@1 is T* = 0.2 and the optimal temperature for pass@100 is T* = 0.8." |
| Q35 | 5 | output_form | "With these temperatures, we find that pass@1 and pass@100 scale smoothly as a function of model size (Figure 6)." |
| Q36 | 5 | output_ontology | "Pass@k can also be interpreted as the result of evaluating the best out of k samples, where the best sample is picked by an oracle with prior knowledge of the unit tests." |
| Q37 | 5 | output_form | "From a practical perspective, we are also interested in the setting where we must select a single sample from k samples without having access to an oracle." |
| Q38 | 5 | output_form | "For instance, when the model is used as an autocomplete tool where a user provides a prompt, we do not have unit tests, but would like to return only a single completion to the user for evaluation so as to not overwhelm them." |
| Q39 | 5 | output_form | "Inspired by similar work in language modeling, we find that choosing the sample with the highest mean token log probability outperforms evaluating a random sample, while choosing the sample based on sum log probability can perform slightly worse than picking randomly." |
| Q40 | 6 | output_form | "Finally, we compute BLEU scores for all Codex-12B HumanEval samples (at temperature 0.8) against their reference solutions. For each problem, when we plot the distributions of BLEU scores for correct and incorrect solutions, we notice significant overlap (Figure 8). Since an incorrect solution is guaranteed to be functionally inequivalent to the reference solution, we conclude that improvements in BLEU score may not indicate improved rates of functional correctness in practice." |
| Q41 | 6 | input_content | "Two recent works similar in spirit to Codex are GPT-Neo (Black et al., 2021) and GPT-J (Wang & Komatsuzaki, 2021), which are trained on The Pile (Gao et al., 2020), a dataset containing text from a variety of sources as well as 8% GitHub code." |
| Q42 | 6 | output_form | "We confirm these findings using the HumanEval dataset, showing that GPT-Neo achieves 6.4% pass@1 and 21.3% pass@100, while GPT models of comparable sizes achieve near 0% on both metrics. We see a remarkable progression in capabilities, with GPT-Neo-2.7B roughly equivalent to Codex-85M (30× fewer parameters). Similarly, GPT-J-6B achieves 11.6% pass@1 and 27.7% pass@100, which is roughly equivalent to Codex-300M (20× fewer parameters)." |
| Q43 | 6 | output_form | "Pass rates are obtained by taking the best result from evaluating at temperatures 0.2, 0.4, and 0.8 for GPT-Neo, and from temperatures 0.2 and 0.8 for GPT-J." |
| Q44 | 6 | output_form | "Finally, we benchmark Codex against the largest free model from Tabnine, a leading code autocomplete system, which achieves 2.6% pass@1 (at T = 0.4) and 7.6% pass@100 (at T = 0.8)." |
| Q45 | 6 | input_content | "Recently, Hendrycks et al. (2021) introduced the APPS dataset to measure the coding challenge competence of language models. The APPS dataset consists of 5000 training and 5000 test examples of coding problems, each with a set of unit tests and, for the training data, a set of correct solutions." |
| Q46 | 6 | input_ontology | "Most of the APPS tests problems are not formulated as single-function synthesis tasks, but rather as full-program synthesis, reading input from stdin and printing output to stdout, in contrast to the main Codex training data." |
| Q47 | 6 | output_form | "In the paper that introduces APPS, the authors benchmark a few language models and report two metrics: the percentage of problems where the model finds a correct solution (called the "strict accuracy") and the percentage of unit tests passed, even if the solution is incorrect. The latter measure is reported only so as to reduce variance of the measurements, because the results on the first metric were so low. We avoid this metric and only focus on "strict accuracy"" |
| Q48 | 7 | input_content | "In addition to standalone functions, Python code found on GitHub contains class implementations, configuration files, scripts, and even files used to store data. This code is seemingly unrelated to synthesizing functions from docstrings, and we hypothesize that the distribution mismatch reduces HumanEval performance." |
| Q49 | 7 | input_ontology | "In order to adapt Codex to the distribution of the task of interest, we construct a set of training problems from correctly implemented standalone functions, and use them for additional supervised fine-tuning." |
| Q50 | 7 | input_content | "We describe two approaches for collecting these examples: from competitive programming websites and from repositories with continuous integration." |
| Q51 | 7 | input_content | "Programming contest and interview preparation websites use hidden unit tests to automatically judge the functional correctness of submissions. These problems are self-contained, come with well-written problem statements, and generally have excellent test coverage. Additionally, these problems test algorithmic reasoning over a broad range of core skills and difficulties." |
| Q52 | 7 | input_content | "We collected problem statements, function signatures, and solutions from several popular programming contest and interview preparation websites. We then assembled these into programming tasks similar to HumanEval, using the problem description as the docstring. Since complete test suites are often hidden, we created unit tests from examples found in the problem statements, or extracted additional test cases through submitting incorrect solutions. In total, we curated 10,000 problems in this way." |
| Q53 | 7 | input_form | "Taking advantage of sys.setprofile, we were able to trace and collect inputs and outputs for all functions called during integration tests. This data could then be used to create unit tests for the functions." |
| Q54 | 7 | input_content | "Projects that employ continuous integration (CI) are ideal candidates for tracing. We follow the commands in the CI configuration files, which contain build and test commands, to set up the virtual environments, install dependencies, and run integration tests." |
| Q55 | 7 | input_content | "We considered GitHub repos using travis and tox as their CI frameworks, as they are two of the most popular CI tools. We additionally used publicly available source code from pip packages found in the python package index (PyPI)." |
| Q56 | 8 | input_form | "Because these projects contained untrusted code, it was important to run integration tests in the sandboxed environment described above." |
| Q57 | 8 | input_content | "While there are millions of potential functions to curate problems from, we only collected about 40,000 because not all functions accept inputs and return outputs." |
| Q58 | 8 | input_content | "Even when they do, most objects captured at runtime cannot be pickled and restored outside the sandbox unless the project was installed." |
| Q59 | 8 | input_form | "Since our tracing methodology produced inputs and outputs for all invoked functions, even builtin and library calls imported by the project were turned into problems." |
| Q60 | 8 | input_ontology | "For this reason, functions from tracing tended to be the building blocks of command-line utilities." |
| Q61 | 8 | input_ontology | "To excel at these tasks, the model does not need to know advanced algorithms and data structures. Rather, it needs to be able to follow instructions to implement the functionality specified in the docstring." |
| Q62 | 8 | input_ontology | "Thus, tracing complements the puzzle nature of coding competition problems and broadens the distribution of tasks." |
| Q63 | 8 | output_content | "Some prompts underspecify the function that is implemented, in which case a perfectly valid solution may be wrongly penalized by the unit test." |
| Q64 | 8 | output_content | "Some problems are stateful, and subsequent executions can result in different outcomes." |
| Q65 | 8 | output_content | "To address these issues, we use Codex-12B to generate 100 samples per curated problem. If no samples pass the unit tests, we consider the task to be either ambiguous or too difficult, and filter it out." |
| Q66 | 8 | input_form | "We reran this verification several times to remove stateful or non-deterministic problems." |
| Q67 | 8 | input_content | "We fine-tune Codex on these training problems to produce a set of "supervised fine-tuned" models, which we call Codex-S." |
| Q68 | 8 | input_form | "To produce examples from training problems, we assemble the problems into the format shown in Figure 2." |
| Q69 | 8 | input_form | "If there are prompts of varying length in a batch, we left-pad shorter prompts to the length of the longest prompt, so that the first tokens in the reference solutions line up in context." |
| Q70 | 8 | output_form | "We train to minimize negative log-likelihood of the reference solution, and mask out loss for any tokens in the prompt." |
| Q71 | 8 | input_form | "We train using a learning rate 1/10 as large as used for fine-tuning Codex, but adhere to the same learning rate schedule, and train until validation loss plateaus (less than 10B tokens)." |
| Q72 | 8 | output_form | "As with Codex, we first compute the optimal temperature for evaluating pass@k for 1 ≤ k ≤ 100." |
| Q73 | 8 | output_form | "We find that Codex-S prefers slightly higher temperatures for all k > 1, which possibly reflects the fact that Codex-S captures a narrower distribution than Codex." |
| Q74 | 8 | output_form | "We use T∗ = 0 for computing pass@1 and T∗ = 1 for computing pass@100." |
| Q75 | 8 | output_form | "Next, we compare Codex-S against Codex on pass@1 and pass@100. Codex-S outperforms the corresponding Codex by an average margin of 6.5 percentage points on pass@1 and by a larger average margin of 15.1 percentage points on pass@100 across model size." |
| Q76 | 8 | output_form | "We also plot the performance of different sample selection heuristics for Codex-S-12B against the same heuristics for Codex-12B. When ranking between 1 and 100 samples by mean log probability, the average benefit over random ranking is 11.6 percentage points, which is over 2 percentage points higher than the corresponding benefit for Codex." |
| Q77 | 9 | output_ontology | "When we benchmark our code generation models, we measure pass@k on the HumanEval dataset, where correctness is defined by passing a set of unit tests." |
| Q78 | 9 | output_content | "However, there is no similar way to evaluate docstring samples automatically. Therefore, we grade sample docstrings by hand, considering a docstring correct if it uniquely and accurately specifies the code body." |
| Q79 | 9 | output_content | "Due to the time consuming nature of this process, we only grade 10 samples per problem, for a total of 1640 problems, from Codex-D-12B at temperature 0.8." |
| Q80 | 9 | output_content | "Codex-D often generates incorrect unit tests along with a docstring, but we ignore these during grading." |
| Q81 | 9 | output_ontology | "However, we do not consider the docstring correct when the model simply copies the code body into the docstring." |
| Q82 | 9 | output_content | "The most common failure modes we observe are when the docstring model leaves out an important detail (such as "an answer must be to two decimal places") or when it over-conditions on the function name and invents a problem unrelated to the function body." |
| Q83 | 9 | output_content | "While generating docstrings may be more forgiving because natural language syntax is less strict than code syntax, docstrings in our dataset may be lower quality because developers tend to devote less time to writing docstrings." |
| Q84 | 10 | output_form | "Table 3. Pass rates for our docstring generating model Codex-D, which is evaluated by hand-grading 10 samples per task due to the lack of a ground-truth automatic evaluation." |
| Q85 | 10 | input_content | "First, Codex is not sample efficient to train. Our training dataset comprises a significant fraction of publicly available Python code on GitHub, totaling hundreds of millions of lines of code." |
| Q86 | 10 | output_form | "While evaluating code generation is well-studied (Xu et al., 2021; Helmuth & Spector, 2015; Pantridge et al., 2017), many existing metrics measure performance in tightly specified, constrained problem instances (e.g., string manipulation in FlashFill (Gulwani, 2011)). Therefore, we developed a set of qualitative metrics for measuring the capabilities of code generating models while controlling for the complexity and abstraction level of the specifications (Appendix D)." |
| Q87 | 10 | output_content | "Applying this framework, we find that Codex can recommend syntactically incorrect or undefined code, and can invoke functions, variables, and attributes that are undefined or outside the scope of the codebase." |
| Q88 | 10 | input_content | "Moreover, Codex struggles to parse through increasingly long and higher-level or system-level specifications." |
| Q89 | 10 | input_content | "To concretely illustrate model performance degradation as docstring length increases, we create a dataset of synthetic problems assembled from 13 basic building blocks, each of which modifies an input string in a deterministic way." |
| Q90 | 10 | input_ontology | "We find that as the number of chained building blocks in the docstring increases, model performance decreases exponentially." |
| Q91 | 10 | input_ontology | "This behavior is uncharacteristic of a human programmer, who should be able to correctly implement a program for a chain of arbitrary length if they can do so for a chain of length two." |
| Q92 | 10 | input_ontology | "Further, just as text-conditional generative models in other modalities (Ramesh et al., 2021) have difficulty with binding attributes to objects, Codex can make mistakes binding operations to variables, especially when the number of operations and variables in the docstring is large." |
| Q93 | 10 | input_ontology | "With each additional component, pass rate drops by roughly a factor of 2-3." |
| Q94 | 10 | input_ontology | "Codex has the potential to be useful in a range of ways. For example, it could help onboard users to new codebases, reduce context switching for experienced coders, enable non-programmers to write specifications and have Codex draft implementations, and aid in education and exploration." |
| Q95 | 10 | output_ontology | "However, Codex also raises significant safety challenges, does not always produce code that is aligned with user intent," |
| Q96 | 11 | output_ontology | "To better understand some of the hazards of using Codex in a generative capacity, we conducted a hazard analysis focused on identifying risk factors (Leveson, 2019) with the potential to cause harm." |
| Q97 | 11 | output_ontology | "While some of our findings about the potential societal impacts of code generation systems were informed by work towards responsible deployment of the production-oriented Codex models (which descended from the research-oriented Codex models described in this paper), this section is not intended to provide a full account of any particular product's safety features." |
| Q98 | 11 | output_ontology | "Unless otherwise specified, we anchor our analysis in the specific properties of the models described in this paper." |
| Q99 | 11 | output_ontology | "One of the key risks associated with using code generation models in practice is over-reliance on generated outputs." |
| Q100 | 11 | output_ontology | "Due to the limitations described above as well as alignment issues described below, Codex may suggest solutions that superficially appear correct but do not actually perform the task the user intended." |
| Q101 | 11 | output_ontology | "We discuss a related issue in Appendix G, namely that code generation models can suggest insecure code." |
| Q102 | 11 | output_ontology | "As with other large language models trained on a next-token prediction objective, Codex will generate code that is as similar as possible to its training distribution." |
| Q103 | 11 | output_ontology | "One consequence of this is that such models may do things that are unhelpful for the user, despite having the capability to be more helpful (see Figure 12)." |
| Q104 | 11 | output_ontology | "This is an alignment failure - the model is not aligned with the user's intentions." |
| Q105 | 11 | output_ontology | "It is important to study misalignment because it is a problem that is likely to become worse, not better, as the capabilities of our systems increase." |
| Q106 | 12 | output_ontology | "Codex could have various effects on the security landscape. Because Codex can produce vulnerable or misaligned code, qualified operators should review its generations before executing or trusting them, absent appropriate precautions." |
| Q107 | 12 | output_ontology | "Future code generation models may be able to be trained to produce more secure code than the average developer, though that is far from certain." |
| Q108 | 12 | output_ontology | "Although this is worthy of concern, based on our testing, we believe that at their current level of capability, Codex models do not materially lower the barrier to entry for malware development." |
| Q109 | 12 | output_ontology | "The non-deterministic nature of systems like Codex could enable more advanced malware." |
| Q110 | 12 | input_content | "Similar to large language models, Codex models can learn patterns present in their training data (Carlini et al., 2021). Sensitive data present in source code are liable to be predicted by the model." |
| Q111 | 12 | input_content | "Because Codex is trained on public repositories, we consider any sensitive data present in the training data to have already been compromised." |
| Q112 | 13 | output_form | "Codex, like other large generative models, has an energy footprint from both training and inference (Schwartz et al., 2019; Bender et al., 2021; Patterson et al., 2021)." |
| Q113 | 13 | output_form | "The original training of GPT-3-12B consumed hundreds of petaflop/s-days of compute, while fine-tuning it to create Codex-12B consumed a similar amount of compute." |
| Q114 | 13 | output_form | "This training was performed on a platform (Azure) that purchases carbon credits and sources significant amounts of renewable energy, reducing its carbon footprint." |
| Q115 | 13 | output_content | "Our preliminary research also finds that Codex models rarely generate code that is identical to the contents of training data. Such occurrences were < 0.1% in a study examining the frequency of code generations that appear to match code snippets in the training data (Ziegler, 2021)." |
| Q116 | 13 | output_content | "In these rare instances, the generated code consisted of common expressions or conventions within the programming language that appeared over and over again in the training data." |
| Q117 | 13 | output_content | "We find that, to the extent the generated code appears identical to the training data, it is due to the predictive weightings in the model rather than retention and copying of specific code." |
| Q118 | 13 | output_form | "Generated code is also responsive and customized to the user's input, and the user retains complete control over editing and acceptance of the generated code." |
| Q119 | 13 | output_ontology | "In closing, given the above, models like Codex should be developed, used, and their capabilities explored carefully with an eye towards maximizing their positive social impacts and minimizing intentional or unintentional harms that their use might cause." |
| Q120 | 13 | output_ontology | "Careful documentation and user interface design, code review requirements, and/or content controls (e.g., filtering of outputs) may help to reduce harms associated with overreliance as well as offensive content or insecure code generation." |
| Q121 | 14 | output_form | "We used functional correctness to benchmark our models, and observed improvements on this metric with more sampling." |
| Q122 | 14 | output_form | "SPoC (Kulal et al., 2019) considered the problem of producing functionally correct code from pseudocode with a fixed budget of compilations, which is similar to our pass@k metric." |
| Q123 | 14 | output_form | "TransCoder (Lachaux et al., 2020) trained a system to translate between programming languages in an unsupervised manner, and also observed that functional correctness better captured the capabilities of their model than BLEU score." |
| Q124 | 14 | input_content | "Two early domain-specific datasets used to benchmark neural programming systems were FlashFill (Gulwani, 2011; Gulwani et al., 2012) and Hearthstone (Ling et al., 2016), though the community has trended towards broader and more difficult datasets." |
| Q125 | 14 | input_content | "Barone & Sennrich (2017) proposed a large training and evaluation dataset consisting of Python declarations, docstrings, and bodies scraped from GitHub." |
| Q126 | 14 | input_content | "The CodeSearchNet challenge (Husain et al., 2019) built an even larger corpus from GitHub with data from multiple popular programming languages." |
| Q127 | 14 | input_content | "Recently, CodeXGLUE (Lu et al., 2021) aggregated several programming benchmarks, making use of the recently proposed CodeBLEU metric (Ren et al., 2020)." |
| Q128 | 14 | input_content | "Most relevant to our evaluation work is the APPS (Hendrycks et al., 2021) benchmark for measuring functional correctness based on problems from the competitive programming website Codeforces." |
| Q129 | 14 | output_content | "Human developers often write test suites with limited but targeted coverage, but this does not always work well against an algorithm, highlighting the challenges of evaluating correctness of programs." |
| Q130 | 14 | input_ontology | "We investigated whether it was possible to train large language models to produce functionally correct code bodies from natural language docstrings." |
| Q131 | 14 | input_content | "By fine-tuning GPT on code from GitHub, we found that our models displayed strong performance on a dataset of human-written problems with difficulty level comparable to easy interview problems." |
| Q132 | 14 | output_form | "Model performance could be improved by training on a distribution more similar to the evaluation set, and also by producing multiple samples from a model." |
| Q133 | 15 | input_ontology | "task of producing docstrings from code bodies, and that the performance profiles of these models were similar." |
| Q134 | 15 | input_ontology | "we expanded on the broader impacts of code generating models, and discussed model limitations, finding significant room for improvement." |
| Q135 | 15 | output_content | "We thank Sandhini Agarwal, Casey Chu, Jeffrey Ding, Peter Eckersley, Gillian Hadfield, Rich Harang, Jacob Jackson, Yunxin Jiao, Jade Leung, Andrew Lohn, Ryan Lowe, Thomas McGuire, Margaret Mitchell, Florentine Eloundou Nekoul, Cullen O'Keefe, Long Ouyang, Pranav Shyam, Irene Solaiman, Aravind Srinivas, Helen Toner, Ashish Vaswani, and Jeffrey Wu for helpful discussions and feedback on drafts of this work." |
| Q136 | 15 | output_content | "We are also grateful to the Acceleration and Supercomputing teams at OpenAI for their work on software and hardware infrastructure that this project used." |
| Q137 | 15 | output_content | "Finally, we thank GitHub for partnering to build GitHub Copilot and Microsoft Azure for supporting model training with infrastructure management." |
| Q138 | 19 | output_form | "While all estimators mentioned previously are consistent, only the empirical estimate used by Kulal et al. (2019), and (1) are unbiased." |
| Q139 | 19 | output_form | "Evaluating pass@k in an unbiased way with any number of samples n is important for fair comparison." |
| Q140 | 19 | output_form | "For example, estimating pass@k = 1 − (1 − pass@1)k with 1 − (1 − p̂)k using the empirical pass@1, results in a consistent underestimate as shown in Figure 13." |
| Q141 | 19 | output_form | "The gap doesn't fully close even when n > 5k, and results can seem better with more samples." |
| Q142 | 19 | output_form | "The interpretation of this estimator is that we draw k samples with replacement from a pool of n candidates, but the k samples are not independent." |
| Q143 | 19 | output_form | "(1) is unbiased, because it estimates the fail probability (1−pass@1)k as the probability of drawing k failed samples without replacement." |
| Q144 | 19 | input_content | "We show 8 random problems from HumanEval along with 8 random samples per problem generated from Codex-12B at temperature 0.8." |
| Q145 | 24 | input_ontology | "We describe the 13 building blocks used to create synthetic tasks for evaluating model performance as a function of docstring complexity." |
| Q146 | 24 | input_form | "Each building block is specified by a line of text and a line of code:" |
| Q147 | 25 | input_ontology | "We thus propose adapting attributes used to measure the expressivity and complexity of formal specifications to natural language prompts." |
| Q148 | 25 | output_ontology | "This entails evaluating the ability to reason over computations and states at different levels of abstractions (e.g., high-level requirements versus design-level requirements) as a base metric for complexity and expressivity (e.g., variable dependencies, inter-procedural reasoning, computational interleavings, etc.)." |
| Q149 | 25 | output_ontology | "Below we provide brief descriptions of such attributes and qualitative metrics, which are to be further discussed in a forthcoming paper along with associated results for Codex models." |
| Q150 | 25 | input_ontology | "With regard to specification abstractions, higher-level requirements or specifications are often distinct from lower-level specifications through the allocation of further structure and behavior within a defined boundary to satisfy one or more higher-level requirements." |
| Q151 | 25 | input_ontology | "The current capabilities of synthesis methodologies are only able to tackle tightly specified, constrained problem instances or narrow tasks." |
| Q152 | 25 | input_ontology | "However, Codex has demonstrated preliminary capabilities to consistently solve for high-level specifications." |
| Q153 | 25 | input_ontology | "Variable Interdependencies: Tracking state of more than one variable, their interdependencies and nesting, all possible permutations of state, and the relationship between input and output parameters" |
| Q154 | 25 | input_ontology | "Temporal Reasoning: as consideration of future and past program states including Safety properties entailing that a defined "bad" state never occurs and Liveness properties entailing progress towards a specific goal or state" |
| Q155 | 25 | input_ontology | "Concurrency and Parallelism: Correct and sound reasoning over computational interleavings (for various specification granularities)." |
| Q156 | 26 | output_ontology | "We were interested in detecting problems with the Codex models that will not improve, or may even get more severe, as model capability improves." |
| Q157 | 26 | output_ontology | "In the literature, a model is defined informally as "intent aligned" with a user if (and only if) the model intends to do what the user wants (Christiano, 2018; Kenton et al., 2021)." |
| Q158 | 26 | output_ontology | "It is ambiguous how to apply this definition to Transformer models, since it is unclear to what extent they can be described as having "intent", or what that intent would be." |
| Q159 | 26 | output_ontology | "However, there is an intuitive notion that, given its training objective, Codex is better described as "trying" to continue the prompt by either matching or generalizing the training distribution, than as "trying" to be helpful to the user." |
| Q160 | 26 | output_ontology | "This caches out in predictions that the model will complete confused code with confused code, insecure code with insecure code (see G), or biased code with similarly biased code (see F), regardless of the model's capability to produce secure, unbiased, and high-quality code." |
| Q161 | 26 | output_ontology | "Defining alignment is complex, and there is not yet a satisfactory formalization." |
| Q162 | 26 | output_ontology | "We operationalize sufficient conditions for intent misalignment for a generative model as follows: 1. We consider a model capable of some task X if it has" |
| Q163 | 27 | output_content | "We conducted several alignment evaluations. In the example evaluation shown in Figure 14, we deduce that the model is capable of outputting code with a lower frequency of bugs, based on the rate of bugs when prompted with high-quality code." |
| Q164 | 27 | output_content | "We instruct the model to write correct code, and we assume the model could easily be fine-tuned to detect such an instruction. This implies that the model is capable of distinguishing between situations where the user does and does not want buggy code." |
| Q165 | 27 | output_ontology | "Based on this we conclude that we have identified misalignment in Codex models." |
| Q166 | 27 | output_ontology | "There are several subtleties here; probably the most important one is distinguishing our observations from a robustness failure. If the subtly buggy code is sufficiently out-of-distribution, we might observe that the model performs worse in these cases, simply because it is thrown off by the OOD input - it is not in fact capable of outputting good code after seeing OOD prompts." |
| Q167 | 27 | input_content | "We believe this is unlikely to be a large factor here, as the GitHub dataset contains plenty of poor-quality code. The bugs are designed to be of the sort we'd expect to appear commonly in the dataset; code that compiles and often runs without errors but gives an incorrect answer. Examples include off-by-one errors or single-character typographic errors." |
| Q168 | 27 | input_content | "The datasets used for these evaluations are available at https://github.com/openai/code-align-evals-data." |
| Q169 | 27 | output_ontology | "One starting point is to more carefully curate the pre-training dataset to remove buggy or insecure code." |
| Q170 | 27 | output_content | "However, it is notoriously difficult for most humans to write bug-free code, so rather than acquiring this dataset through labeling it might need to be obtained by filtering input datasets using formal analysis or other metrics of code quality." |
| Q171 | 28 | input_content | "The alignment evaluations are based on the HumanEval dataset described earlier in the paper: 158 problems with a docstring describing the task, reference solution, and tests." |
| Q172 | 28 | input_form | "We took a subset of 30 eval problems, and for each wrote one solution with a subtle bug." |
| Q173 | 28 | input_form | "We construct prompts by prepending these solutions to the task docstring prompts for the HumanEval task." |
| Q174 | 28 | input_form | "We either prepend three examples of [docstring + correct solution], or three examples of [docstring + solution with subtle bugs], each sampled i.i.d. from the 30 problems mentioned above (excluding the current task)." |
| Q175 | 28 | input_form | "We include examples where we insert #instruction: write correct code even if the previous code contains bugs before the start of the task docstring." |
| Q176 | 28 | output_form | "We then evaluate the performance of the Codex models on all 158 examples from the HumanEval dataset, comparing the models' performance on the prompts with correct solutions prepended, no solutions prepended, and prompts with subtly buggy solutions prepended." |
| Q177 | 28 | input_form | "We ensure that the current task being evaluated never appears in the prompt." |
| Q178 | 28 | output_form | "We used T = 0.2, following the evaluations in the main paper." |
| Q179 | 28 | input_content | "The datasets are available at https://github.com/openai/code-align-evals-data." |
| Q180 | 29 | output_content | "Generative models have been shown to encode bias in modalities such as natural language (Brown et al., 2020; Blodgett et al., 2020) and images (Radford et al., 2021), and we find that the same is true of models like Codex that generate code." |
| Q181 | 29 | output_content | "Given the ways and contexts in which code is used and reused, and the role code plays in laying the foundations for world-changing applications, the generation of biased code has the potential to cause allocative or representational harms, and to do so at scale." |
| Q182 | 29 | output_content | "While it can be tempting to think of code generation models as objective tools, we aim to demonstrate how they can be far from that, and that the models can inherit the legacy of outdated and otherwise troublesome ideas." |
| Q183 | 29 | output_content | "This is one key reason why code generated by the Codex models should be treated as untrusted by those using it for research or development until they have reviewed and verified its accuracy and fitness for purpose themselves." |
| Q184 | 29 | output_ontology | "Allocative harms occur when a system allocates or withholds a certain opportunity or resource. Representational harms occur when systems reinforce the subordination of some groups along the lines of identity, e.g. stereotyping or denigration (Crawford, 2017)." |
| Q185 | 30 | input_ontology | "In order to better understand the potential that code generation has to encode bias in the context of Codex in particular, we developed a series of probes for instances of harmful bias in single- and multi-line autocompletions." |
| Q186 | 30 | input_ontology | "We found that, in response to simple prompts like def gender(x):, the generations often assumed binary gender for both single- and multi-line autocompletions." |
| Q187 | 30 | input_ontology | "When we probed using the prompt def race(x):, we found that many of the most commonly-generated completions assumed a small number of mutually exclusive race categories." |
| Q188 | 30 | input_ontology | "Most synthesized completions included "White" and many included only a few other categories, followed by "other." Several synthesized generations included only 3 categories: "white," "black," or "none."" |
| Q189 | 30 | output_form | "To test these hypotheses and the related harms, we compared GPT-3 to Codex comment production on a series of co-occurrence tests across gender, race, and religion." |
| Q190 | 30 | output_content | "Very broadly, we found that when explicitly prompted to talk about specific genders, races, and religions, Codex comments tend to reproduce similar biases to GPT-3, albeit with less diversity in the outputs." |
| Q191 | 30 | output_content | "For example, with religion "Islam", in both models we observed occurrences of the word "terrorist" and "violent" at a greater rate than with other groups, but GPT-3's outputs included more variants on these themes." |
| Q192 | 30 | output_form | "Co-occurrence is a blunt instrument, as it doesn't pick up on the subtleties of how a particular word is used in context, only that it is used in context." |
| Q193 | 30 | output_content | "Additionally, since we are prompting both models to explicitly describe groups, they are not from the models talking about these group features in the wild, but rather in a constrained experimental setup." |
| Q194 | 30 | output_form | "Co-occurrence tests measure which words are likely to occur in the neighborhood of other words." |
| Q195 | 31 | output_ontology | "The threat landscape for Codex is similar to that of language models. Actors can range from low and moderately skilled or resourced actors to well-resourced and highly-organized "advanced persistent threat" (APT) groups." |
| Q196 | 31 | output_ontology | "However, the manner in which Codex models may be misused will likely differ from that of language models." |
| Q197 | 31 | output_ontology | "It is our assessment that Codex models do not differentially enable offensive cybersecurity capabilities because they are not more efficient or effective than conventional tools or techniques are." |
| Q198 | 31 | output_form | "We conducted experiments on Codex's ability to generate malicious code. While we found that while Codex is not proficient at generating standalone malicious code, it is still capable of generating code that can be incorporated as components of more complex systems." |
| Q199 | 31 | output_form | "We found that Codex did not perform well when compared even to rudimentary Static Application Security Testing (SAST) tools." |
| Q200 | 31 | output_form | "We encountered no cases in our testing where using a Codex model led to better or more efficient results than SAST tools." |
| Q201 | 31 | output_ontology | "However, Codex is generally unable to suggest specific versions of packages, as package versions are specified outside of the prompt context that Codex is aware of." |
| Q202 | 31 | output_form | "Through testing, we found that the likelihood of Codex suggesting a vulnerable or malicious package is low in aggregate." |
| Q203 | 31 | output_ontology | "We found that models trained on source code offered no advantages over conventional language models because the domains are fundamentally different." |
| Q204 | 32 | input_ontology | "To study this phenomenon, we asked Codex to suggest code that would call cryptographic libraries to generate cryptographic contexts, and then evaluated whether any of these outputs were clearly insecure." |
| Q205 | 32 | input_ontology | "When tested on a standard series of prompts asking the models to call functions to produce RSA keys or AES contexts, we find that Codex models of varying sizes frequently use clearly insecure configurations (See Figure 15)." |
| Q206 | 32 | input_content | "We used 5 prompts across different libraries for RSA and AES based on Sonar Source's Python vulnerability database, and generated ˜30k samples total." |
| Q207 | 32 | input_form | "We then removed some generated samples based on expected runtime errors, as different model sizes tend to vary in whether they produce code that runs." |
| Q208 | 32 | output_ontology | "RSA keys were considered improperly configured if they were shorter than 2048 bits." |
| Q209 | 32 | output_ontology | "AES contexts were considered improperly configured if they used the ECB cipher mode (see Menezes et al. (2018), p. 228)." |
| Q210 | 32 | output_form | "We chose these two tests to evaluate as targets because there is consensus among cryptography experts that these configurations generally should not be used, and these were reasonable to evaluate programmatically." |
| Q211 | 32 | output_ontology | "Interestingly, we do not see a robust model size trend (over 1 order of magnitude of parameters) in this data." |
| Q212 | 32 | output_ontology | "This suggests that insecure code production, at least in this case, is an alignment issue (see Appendix E): it is unclear if the models are improving with scale." |
| Q213 | 32 | output_ontology | "A larger study using the most common insecure code vulnerabilities may shed more light on this issue." |
| Q214 | 33 | output_form | "When asked to create encryption keys, Codex models select clearly insecure configuration parameters in a significant fraction of cases. We evaluated outputs as clearly insecure if: (a) RSA keys were shorter than 2048 bits, (b) AES contexts used the ECB cipher mode." |
| Q215 | 33 | output_ontology | "Because security standards change over time as capabilities improve, this is likely an underestimate of the true rate of improperly configured outputs." |
| Q216 | 33 | output_ontology | "Similarly, the produced samples that were not classified as clearly insecure are not necessarily secure, as our tests measure insecurity." |
| Q217 | 33 | input_content | "Additionally, one of the challenges of code generation stem from relying on the assumption that intent is captured sufficiently enough in comments and documentation to not compromise accuracy." |
| Q218 | 33 | input_ontology | "Thus, even if the model were perfectly accurate, we would not expect it to reduce the labor costs associated with writing code to zero." |
| Q219 | 33 | output_content | "There is unfortunately only limited research on the demographic distribution of Python users." |
| Q220 | 34 | input_content | "Codex imports substitutable packages at different rates based on patterns in its training data, which can have various possible implications." |
| Q221 | 34 | output_content | "Differential import rates by Codex might lead to subtle errors in cases where a certain import is ill-advised, increase robustness in cases where the alternative package imported by an individual would have been worse, and/or increase the dominance of an already-influential set of individuals and organizations in the software supply chain." |
| Q222 | 34 | input_content | "The scale of these effects for Codex may be relatively low if users mostly import packages they know how to use or have done outside research on, so they can double-check anything the model does." |
| Q223 | 34 | input_content | "Moreover, because packages are generally imported at the top of a file without any comments, the model has very little to go on in these cases, so users would most likely have to start typing out the name of the package they want to import rather than trusting the model to know they are starting a machine learning project and want to import either PyTorch or TensorFlow." |
| Q224 | 34 | output_form | "As one example, we looked at completions of the prompt: # import machine learning package import and found that over 100 completions of 100 tokens, 6 contained suggestions for TensorFlow and 3 for PyTorch, two libraries that are rough substitutes." |
| Q225 | 35 | input_ontology | "Most past studies of the impacts of code generation models consider performance on a closed set of tasks in a simulated environment (Xu et al., 2021)." |
| Q226 | 35 | input_ontology | "As the deployment of Codex and other near-term technologies proceeds, we may be able to conduct more robust experiments examining the impact of various strengths of models on real-world job performance, across teams and across firms." |
| Q227 | 35 | output_content | "Precise and accurate prediction of any impacts without user or market signal is difficult, but the potential implications on the long-run labor market and the possibility of disparate outcomes across groups warrant further exploration of these issues." |
| Q228 | 35 | input_ontology | "It may be possible to assess the relative likelihood of different scenarios by building a deeper understanding of Codex's capabilities across several code-related tasks or by studying the effects of precise deployment scenarios." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://groundy.com/articles/swe-bench-verified-explained-what-the-coding-agent-leaderboard-actually-measures-and-what-it-misses/ |
| WEB-2 | https://arxiv.org/abs/2603.00520 |
| WEB-3 | https://arxiv.org/abs/2503.15223 |
| WEB-4 | https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=6633&context=sis_research |
| WEB-5 | https://www.researchgate.net/publication/347697366_BugsInPy_a_database_of_existing_bugs_in_Python_programs_to_enable_controlled_testing_and_debugging_studies |
| WEB-6 | https://www.mdpi.com/2674-113X/4/3/17 |
| WEB-7 | https://github.com/evalplus/evalplus |
| WEB-8 | https://arxiv.org/abs/2511.01043 |
| WEB-9 | https://arxiv.org/abs/2504.06939 |
| WEB-10 | https://www.cobalt.io/learning-center/soc-2-compliance-for-saas |
| WEB-11 | https://blaxel.ai/blog/soc-2-compliance-ai-guide |
| WEB-12 | https://www.probo.com/hub/ai-coding-tools-soc2-compliance |
| WEB-13 | https://csrc.nist.gov/pubs/sp/800/218/final |
| WEB-14 | https://www.nist.gov/news-events/news/2025/12/secure-software-development-framework-ssdf-version-12-available-public |
| WEB-15 | https://www.aikido.dev/learn/compliance/compliance-frameworks/nist-ssdf |
| WEB-16 | https://csrc.nist.gov/pubs/sp/800/218/a/final |
| WEB-17 | https://arxiv.org/abs/2503.05860 |
| WEB-18 | https://arxiv.org/abs/2512.18470 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** openai/openai_humaneval
**Analysis date:** 2025-01-30
**Examples reviewed:** 40 from `test` split (out of 164 total)
**Columns shown:** task_id, prompt, canonical_solution, test, entry_point
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | openai_humaneval | HumanEval/61 | test | `def correct_bracketing(brackets: str):\n    """ brackets is a string of "(" and ")". return True if every opening bracket has a corresponding closing bracket.` | Clean docstring-to-function bracket-matching task — pure algorithm puzzle | IO |
| D2 | openai_humaneval | HumanEval/104 | test | `def unique_digits(x):\n    """Given a list of positive integers x. return a sorted list of all elements that hasn't any even digit.` | Clean list-filtering algorithm with no external dependencies | IO |
| D3 | openai_humaneval | HumanEval/130 | test | `def tri(n):\n    """Everyone knows Fibonacci sequence... Tribonacci sequence is defined by the recurrence: tri(1) = 3, tri(n) = 1 + n / 2, if n is even.` | Mathematical sequence generation task; entirely self-contained | IO |
| D4 | openai_humaneval | HumanEval/0 | test | `def has_close_elements(numbers: List[float], threshold: float) -> bool:\n    """ Check if in given list of numbers, are any two numbers closer to each other than given threshold.` | Standard float-list algorithm from scratch; no external library | IC |
| D5 | openai_humaneval | HumanEval/32 | test | `def find_zero(xs: list):\n    """ xs are coefficients of a polynomial. find_zero find x such that poly(x) = 0.` | Binary-search numerical root-finding; imports `math` only | IC |
| D6 | openai_humaneval | HumanEval/38 | test | `def encode_cyclic(s: str):\n    """\n    returns encoded string by cycling groups of three characters.\n    """` | Cyclic encoding helper — already implemented; model must implement `decode_cyclic` from context | IO |
| D7 | openai_humaneval | HumanEval/124 | test | `def valid_date(date):\n    """You have to write a function which validates a given date string and returns True if the date is valid otherwise False.` | Date validation; tests use `assert candidate('03-11-2000') == True` — no datetime library | IC |
| D8 | openai_humaneval | HumanEval/42 | test | `def incr_list(l: list):\n    """Return list with elements incremented by 1.` | Trivial one-liner; canonical solution is `return [(e + 1) for e in l]` | IO |
| D9 | openai_humaneval | HumanEval/17 | test | `def parse_music(music_string: str) -> List[int]:\n    """ Input to this function is a string representing musical notes in a special ASCII format.` | Custom-spec string parsing; fully self-described in docstring | IC |
| D10 | openai_humaneval | HumanEval/88 | test | `def sort_array(array):\n    """\n    Given an array of non-negative integers, return a copy of the given array after sorting, you will sort the given array in ascending order if the sum(first index value, last index value) is odd` | Sort direction determined by boundary sum — toy algorithm puzzle | IO |
| D11 | openai_humaneval | HumanEval/11 | test | `def string_xor(a: str, b: str) -> str:\n    """ Input are two strings a and b consisting only of 1s and 0s. Perform binary XOR on these inputs and return result also as a string.` | Bitwise XOR on string representation — no imports | IO |
| D12 | openai_humaneval | HumanEval/137 | test | `def compare_one(a, b):\n    """\n    Create a function that takes integers, floats, or strings representing real numbers, and returns the larger variable in its given variable type.\n    Note: If a real number is represented as a string, the floating point might be . or ,` | Comma/dot decimal separator handling — touches locale conventions but within docstring spec | IC |
| D13 | openai_humaneval | HumanEval/67 | test | `def fruit_distribution(s,n):\n    """\n    In this task, you will be given a string that represents a number of apples and oranges ... return the number of the mango fruits in the basket.` | Toy word-problem parsing; no real-world codebase relevance | IO |
| D14 | openai_humaneval | HumanEval/38 | test | `def decode_cyclic(s: str):\n    """\n    takes as input string encoded with encode_cyclic function. Returns decoded string.\n    """` | Sparse docstring — only one sentence; no examples; but canonical solution is just `return encode_cyclic(encode_cyclic(s))` — trivial once encode is understood | IF |
| D15 | openai_humaneval | HumanEval/127 | test | `def intersection(interval1, interval2):\n    """You are given two intervals... Your task is to determine whether the length of intersection of these two intervals is a prime number.` | Combines interval arithmetic with primality check — interview-puzzle style | IO |
| D16 | openai_humaneval | HumanEval/154 | test | `def cycpattern_check(a , b):\n    """You are given 2 words. You need to return True if the second word or any of its rotations is a substring in the first word` | String rotation substring check — pure algorithm | IO |
| D17 | openai_humaneval | HumanEval/3 | test | `def below_zero(operations: List[int]) -> bool:\n    """ You're given a list of deposit and withdrawal operations on a bank account that starts with zero balance.` | Bank account simulation — algorithmic, not framework code | IO |
| D18 | openai_humaneval | HumanEval/95 | test | `def check_dict_case(dict):\n    """\n    Given a dictionary, return True if all keys are strings in lower case or all keys are strings in upper case, else return False.` | Dictionary key case uniformity check | IO |
| D19 | openai_humaneval | HumanEval/144 | test | `def simplify(x, n):\n    """Your task is to implement a function that will simplify the expression x * n. The function returns True if x * n evaluates to a whole number` | Fraction string parsing; no external dependency | IC |
| D20 | openai_humaneval | HumanEval/105 | test | `def by_length(arr):\n    """\n    Given an array of integers, sort the integers that are between 1 and 9 inclusive, reverse the resulting array, and then replace each digit by its corresponding name` | Multi-step toy pipeline; canonical solution uses bare `except:` as error handler | OC |
| D21 | openai_humaneval | HumanEval/32 | test | `def poly(xs: list, x: float):\n    """\n    Evaluates polynomial with coefficients xs at point x.\n    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n\n    """` | Docstring contains typo: `xs[1] * x^2` should be `xs[2] * x^2` — mild documentation error present in a benchmark designed around clean specs | OC |
| D22 | openai_humaneval | HumanEval/130 | test | `assert candidate(3) == [1, 3, 2.0, 8.0]` | Unit test returns mixed int/float list — correctness is sensitive to float vs int type distinction | OC |
| D23 | openai_humaneval | HumanEval/75 | test | `def is_multiply_prime(a):\n    """Write a function that returns true if the given number is the multiplication of 3 prime numbers and false otherwise. Knowing that (a) is less then 100.` | Brute-force primality; canonical solution uses triple nested loop up to 101 — inefficient but passes | OC |
| D24 | openai_humaneval | HumanEval/109 | test | `def move_one_ball(arr):\n    """We have an array 'arr' of N integers arr[1], arr[2], ..., arr[N].The numbers in the array will be randomly ordered. Your task is to determine if it is possible to get an array sorted in non-decreasing order by performing the following operation on the given array: You are allowed to perform right shift operation any number of times.` | Rotation-sortable array check — clean algorithm spec | IO |
| D25 | openai_humaneval | HumanEval/123 | test | `def get_odd_collatz(n):\n    """\n    Given a positive integer n, return a sorted list that has the odd numbers in collatz sequence.` | Mathematical sequence filtering; canonical solution uses integer division via `n/2` (Python 3 float division) | OC |
| D26 | openai_humaneval | HumanEval/145 | test | `def order_by_points(nums):\n    """\n    Write a function which sorts the given list of integers in ascending order according to the sum of their digits.` | Digit-sum sort with negative number handling — interview puzzle | IO |
| D27 | openai_humaneval | HumanEval/66 | test | `def digitSum(s):\n    """Task\n    Write a function that takes a string as input and returns the sum of the upper characters only' ASCII codes.` | ASCII sum task; function name is `digitSum` but task is about uppercase ASCII values — mild naming mismatch | IC |
| D28 | openai_humaneval | HumanEval/158 | test | `find_max(["aaaaaaa", "bb" ,"cc"]) == ""aaaaaaa"` | Docstring contains a double-quote typo: `""aaaaaaa"` — formatting error in the problem statement itself | OC |
| D29 | openai_humaneval | HumanEval/124 | test | `if month in [1,3,5,7,8,10,12] and day < 1 or day > 31:` | Canonical solution contains a bug: operator precedence error — `and` binds tighter than `or`, so this evaluates `(month in [...] and day < 1) or (day > 31)` incorrectly | OC |
| D30 | openai_humaneval | HumanEval/19 | test | `def sort_numbers(numbers: str) -> str:\n    """ Input is a space-delimited string of numberals from 'zero' to 'nine'.` | Docstring misspells "numerals" as "numberals" — minor doc quality issue | OC |
| D31 | openai_humaneval | HumanEval/21 (encode_cyclic) | test | `groups = [(group[1:] + group[0]) if len(group) == 3 else group for group in groups]` | The prompt body (encode_cyclic) is provided as context with inline comments — the model sees existing code; this is the closest HumanEval comes to code-comprehension | IF |
| D32 | openai_humaneval | HumanEval/52 | test | `def below_threshold(l: list, t: int):\n    """Return True if all numbers in the list l are below threshold t.` | Trivial boundary check; no framework involvement | IO |
| D33 | openai_humaneval | HumanEval/102 | test | `def choose_num(x, y):\n    """This function takes two positive numbers x and y and returns the biggest even integer number that is in the range [x, y] inclusive.` | Boundary arithmetic; canonical solution fits in 4 lines | IO |
| D34 | openai_humaneval | HumanEval/14 | test | `def all_prefixes(string: str) -> List[str]:\n    """ Return list of all prefixes from shortest to longest of the input string` | One-liner prefix generator — minimal complexity | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Python-native problem set — no modality or language mismatch
- **Dimension(s):** IF
- **Observation:** Every sampled example is pure Python source code with standard library imports only (`typing`, `math`, `random`, `string`). No non-Python languages, no audio, images, or other modalities appear. Input and output are plain text Python, matching the deployment's programming language.
- **Deployment relevance:** The deployment operates on Python source code; there is no modality mismatch. Any model evaluated on HumanEval is at minimum being tested on Python code generation, the same language as the deployment's codebase.
- **Datapoint citations:**
  - [D4] Example HumanEval/0 (openai_humaneval, split=test): `from typing import List\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:` — standard Python typing import, matching deployment's Python ecosystem
  - [D5] Example HumanEval/32 (openai_humaneval, split=test): `import math\n\ndef poly(xs: list, x: float):` — only `math` imported; plain Python throughout

#### Strength 2: Unit test structure confirms binary pass/fail operationalization
- **Dimension(s):** OO, OF
- **Observation:** Every example contains an explicit `check(candidate)` function with `assert` statements. Tests are structured, executable, and machine-checkable. The test suite structure is transparent and inspectable, confirming the benchmark's claim of automated functional correctness evaluation.
- **Deployment relevance:** While the binary pass/fail output ontology is fundamentally misaligned with the deployment's human-reviewer-acceptance criterion, the presence of explicit, inspectable unit tests confirms that HumanEval's scoring mechanism is at least internally consistent and not subject to hidden annotation bias. This provides a clear baseline understanding of what the metric measures.
- **Datapoint citations:**
  - [D1] Example HumanEval/61 (openai_humaneval, split=test): `assert candidate("()")` / `assert not candidate("((()())))")` — direct boolean correctness assertions; no human judgment involved
  - [D7] Example HumanEval/124 (openai_humaneval, split=test): `assert candidate('03-11-2000') == True` / `assert candidate('15-01-2012') == False` — 16 explicit test cases covering edge conditions

#### Strength 3: Docstring completeness confirms the benchmark's clean-spec assumption
- **Dimension(s):** IC, IF
- **Observation:** Across 40 sampled examples, all but one (HumanEval/38's `decode_cyclic`) contain multi-sentence docstrings with worked examples embedded directly in the docstring or as inline `>>>` doctests. The inputs are genuinely well-specified and complete.
- **Deployment relevance:** This confirms the benchmark YAML's documented gap: HumanEval's clean-spec assumption is verifiable in the actual data. The contrast with the deployment's sparse/misleading-doc condition is concrete and measurable, not speculative.
- **Datapoint citations:**
  - [D9] Example HumanEval/17 (openai_humaneval, split=test): `""" Input to this function is a string representing musical notes in a special ASCII format... Here is a legend: 'o' - whole note, lasts four beats; 'o|' - half note, lasts two beats; '.|' - quater note, lasts one beat"` — full legend provided; no inference from code required
  - [D3] Example HumanEval/130 (openai_humaneval, split=test): `"""Everyone knows Fibonacci sequence... Tribonacci sequence is defined by the recurrence: tri(1) = 3; tri(n) = 1 + n / 2, if n is even..."` — complete mathematical specification with examples; deployment code would never have this

#### Strength 4: Algorithm/interview-puzzle framing is self-contained and contamination-resistant
- **Dimension(s):** IC
- **Observation:** All 40 sampled examples are fully self-contained: they take primitive Python types (lists of ints, strings, floats, tuples) as inputs and return primitive types. No external APIs, no framework state, no class hierarchies, no session objects are required to understand or test any problem.
- **Deployment relevance:** This self-containment property means HumanEval scores are interpretable as lower-bound estimates of pure algorithmic reasoning ability, free from framework-specific confounds. However, this same property is the core IC mismatch: the deployment's code is never this self-contained.
- **Datapoint citations:**
  - [D2] Example HumanEval/104 (openai_humaneval, split=test): `def unique_digits(x):\n    """Given a list of positive integers x. return a sorted list..."` — input is a plain Python list; no ORM, no session, no dependency injection
  - [D18] Example HumanEval/95 (openai_humaneval, split=test): `def check_dict_case(dict):\n    """Given a dictionary, return True if all keys are strings in lower case..."` — input is a bare Python dict

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Complete absence of bug localization tasks — core deployment capability entirely untested
- **Dimension(s):** IO
- **Observation:** All 40 sampled examples present a clean function signature + docstring and require the model to generate a complete correct function body from scratch. Not a single example presents existing, potentially buggy code and asks the model to identify where a defect occurs. The task ontology is 100% docstring-to-function synthesis across the full sample.
- **Deployment relevance:** The deployment's most critical capability is bug localization — "identifying the specific line or range." HumanEval contains zero tasks of this type. A model that achieves 0% on HumanEval could still be an excellent bug localizer; a model that achieves 95% could fail entirely at localization. HumanEval scores provide no signal for the deployment's primary task.
- **Datapoint citations:**
  - [D1] Example HumanEval/61 (openai_humaneval, split=test): `def correct_bracketing(brackets: str):\n    """ brackets is a string of "(" and ")". return True if every opening bracket has a corresponding closing bracket."""` — model receives empty function body and must generate it; no existing buggy code to localize a defect in
  - [D10] Example HumanEval/88 (openai_humaneval, split=test): `def sort_array(array):\n    """\n    Given an array of non-negative integers, return a copy of the given array after sorting..."` — same pattern: clean spec, empty body, generate-from-scratch task
  - [D24] Example HumanEval/109 (openai_humaneval, split=test): `def move_one_ball(arr):\n    """We have an array 'arr' of N integers..."` — complete, accurate docstring; model generates body; no localization required

#### Concern 2: Complete absence of diff generation tasks — second core deployment capability untested
- **Dimension(s):** IO, OF
- **Observation:** Every sampled example produces a complete Python function body as output, starting from a blank body. No example asks the model to produce a targeted diff (a minimal corrective change) against an existing, partially-correct or buggy implementation. The output form is always full function generation, never patch/diff.
- **Deployment relevance:** The deployment requires "generating a minimal, targeted corrective patch that a reviewer can accept or reject as a unified diff." HumanEval's output form is structurally incompatible with this: generating a complete standalone function is a different cognitive and structural task from identifying and replacing a defective 2-line block in a 200-line method.
- **Datapoint citations:**
  - [D8] Example HumanEval/42 (openai_humaneval, split=test): `def incr_list(l: list):\n    """Return list with elements incremented by 1."""` — canonical solution is `return [(e + 1) for e in l]`; the entire function body is the output; there is no existing implementation to diff against
  - [D6] Example HumanEval/38 (openai_humaneval, split=test): `def decode_cyclic(s: str):\n    """\n    takes as input string encoded with encode_cyclic function. Returns decoded string.\n    """` — even this example (which provides `encode_cyclic` as context) requires generating a complete new function body, not a targeted diff

#### Concern 3: No framework-specific Python content — entire deployment input distribution absent
- **Dimension(s):** IC
- **Observation:** Across all 40 sampled examples, no problem involves Django, Flask, SQLAlchemy, FastAPI, NumPy, pandas, Celery, boto3, or any other framework common in real-world US software teams. Imports seen in the sample are limited to `typing`, `math`, `random`, and `string`. Problems involve pure algorithmic manipulation of primitive Python types.
- **Deployment relevance:** The deployment's target population works on "Django/Flask views, SQLAlchemy models, NumPy/pandas pipelines, internal utility wrappers, and substantial legacy Python." A model may solve bracket-matching and Collatz sequences but fail completely on SQLAlchemy N+1 bugs or NumPy broadcasting errors. HumanEval performance is not predictive of framework-specific defect detection.
- **Datapoint citations:**
  - [D3] Example HumanEval/130 (openai_humaneval, split=test): `def tri(n):\n    """Everyone knows Fibonacci sequence... Tribonacci sequence is defined by the recurrence..."` — pure mathematical recursion; no framework concepts
  - [D13] Example HumanEval/67 (openai_humaneval, split=test): `def fruit_distribution(s,n):\n    """In this task, you will be given a string that represents a number of apples and oranges..."` — toy word-problem string parsing; zero real-world relevance to Django views or ORM queries
  - [D15] Example HumanEval/127 (openai_humaneval, split=test): `def intersection(interval1, interval2):\n    """...determine whether the length of intersection of these two intervals is a prime number."` — interval-prime-check hybrid puzzle; entirely absent from the deployment's defect taxonomy

#### Concern 4: Binary unit-test pass/fail output ontology fundamentally misaligned with human reviewer acceptance
- **Dimension(s):** OO, OC
- **Observation:** Every problem's ground truth is determined by automated `assert` statements in a `check()` function. The test suites are written by benchmark authors, not professional developers, and several examples have notably sparse test coverage (HumanEval/104 has 4 test cases; HumanEval/121 has 7). The deployment's success criterion — reviewer acceptance — is nowhere operationalized.
- **Deployment relevance:** The deployment explicitly states: "unit tests are often absent or untrustworthy in customer repos, so a fix that passes existing tests can still be rejected if it changes semantics, masks the real bug, or violates codebase conventions." HumanEval's sole ground truth is exactly the signal the deployment cannot rely on.
- **Datapoint citations:**
  - [D2] Example HumanEval/104 (openai_humaneval, split=test): `assert candidate([15, 33, 1422, 1]) == [1, 15, 33]` / `assert True` — only 4 functional assertions, one of which is `assert True` (a no-op); thin coverage could pass incorrect solutions
  - [D22] Example HumanEval/130 (openai_humaneval, split=test): `assert candidate(3) == [1, 3, 2.0, 8.0]` — correctness depends on exact float vs. int type in output; a semantically equivalent integer-returning solution would fail even if logically correct

#### Concern 5: Confirmed annotation quality issues in actual canonical solutions
- **Dimension(s):** OC
- **Observation:** Inspection of canonical solutions reveals multiple quality issues: (1) HumanEval/124's canonical solution contains a Python operator precedence bug (`if month in [1,3,5,7,8,10,12] and day < 1 or day > 31` evaluates incorrectly); (2) HumanEval/32's docstring typo (`xs[1] * x^2` should be `xs[2] * x^2`); (3) HumanEval/158 contains a double-quote typo in the docstring (`""aaaaaaa"`); (4) HumanEval/19 misspells "numerals" as "numberals."
- **Deployment relevance:** The deployment requires that ground-truth labels reflect what professional developers would accept. The canonical solutions are written by benchmark authors without documented professional developer review. The presence of a buggy canonical solution in the benchmark (HumanEval/124) — which the tests may partially accept due to the same operator precedence ambiguity — directly validates the paper's own acknowledgment that "a perfectly valid solution may be wrongly penalized by the unit test."
- **Datapoint citations:**
  - [D29] Example HumanEval/124 (openai_humaneval, split=test): `if month in [1,3,5,7,8,10,12] and day < 1 or day > 31:` — `and` binds tighter than `or`; this evaluates as `(month in [...] and day < 1) or (day > 31)` which is semantically incorrect for the stated validation logic
  - [D21] Example HumanEval/32 (openai_humaneval, split=test): `return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n` — `xs[1]` in the docstring should be `xs[2]` for the correct polynomial formula
  - [D28] Example HumanEval/158 (openai_humaneval, split=test): `find_max(["aaaaaaa", "bb" ,"cc"]) == ""aaaaaaa"` — extra double-quote in docstring example is a documentation formatting error
  - [D30] Example HumanEval/19 (openai_humaneval, split=test): `""" Input is a space-delimited string of numberals from 'zero' to 'nine'.` — "numberals" misspelling in the problem specification itself

#### MAJOR

#### Concern 6: All inputs are clean, accurate, well-specified docstrings — deployment's sparse-doc condition entirely absent
- **Dimension(s):** IC
- **Observation:** Every example presents a complete, accurate, self-consistent docstring with worked examples. The only partial exception is HumanEval/38 (`decode_cyclic`), which has a one-sentence docstring but where the encode function is provided as context — still a clean spec condition. No example simulates absent, stale, or misleading documentation.
- **Deployment relevance:** The deployment's user confirmed: "Misleading comments and cryptic variable names are common; the system must reason directly from code rather than relying on clean natural-language specifications." A model that performs well on HumanEval may degrade severely on code without docstrings, as the web search findings confirm ("removing semantic cues such as docstrings or role-play causes severe degradation").
- **Datapoint citations:**
  - [D14] Example HumanEval/38 (openai_humaneval, split=test): `def decode_cyclic(s: str):\n    """\n    takes as input string encoded with encode_cyclic function. Returns decoded string.\n    """` — this is the sparsest docstring in the sample; the encode function is still fully provided and the task remains trivially inferrable
  - [D9] Example HumanEval/17 (openai_humaneval, split=test): `'o' - whole note, lasts four beats\n    'o|' - half note, lasts two beats\n    '.|' - quater note, lasts one beat` — domain-specific notation is fully explained inline; no inference from code needed; contrast with deployment's legacy utilities where such documentation is absent

#### Concern 7: Problems are algorithm/interview-puzzle style — no real-world software engineering patterns
- **Dimension(s):** IC, IO
- **Observation:** The 40 sampled problems span bracket matching, sequence generation, digit manipulation, string encoding, fruit distribution word problems, and mathematical computations. None involve: class methods, object state, HTTP request handling, database query patterns, async/await, exception propagation across layers, or any multi-function interaction beyond a helper defined in the same problem.
- **Deployment relevance:** The deployment's defect taxonomy includes "SQLAlchemy N+1, Django ORM lazy-load outside session, NumPy shape mismatch" — defect classes that require understanding framework semantics, not just algorithmic logic. A model evaluating a Django view's ORM call needs knowledge of session lifecycles that no HumanEval problem exercises.
- **Datapoint citations:**
  - [D17] Example HumanEval/3 (openai_humaneval, split=test): `def below_zero(operations: List[int]) -> bool:\n    """ You're given a list of deposit and withdrawal operations on a bank account..."` — simulates bank account logic with a list of integers; no actual financial framework, no database, no transaction management
  - [D16] Example HumanEval/154 (openai_humaneval, split=test): `def cycpattern_check(a , b):\n    """You are given 2 words. You need to return True if the second word or any of its rotations is a substring in the first word"` — pure string rotation/substring puzzle with no real-world analogy in framework code

#### Concern 8: Benchmark saturation — top models solve >94% of problems, reducing discriminative power
- **Dimension(s):** OO, OF
- **Observation:** The benchmark has only 164 examples and problems are visibly simple: HumanEval/42 (`incr_list`) requires a one-line list comprehension; HumanEval/34 (`below_threshold`) requires a simple loop with a boolean check; HumanEval/52 is similarly trivial. Several canonical solutions are 1-4 lines. The web search findings confirm top models now solve >94% of problems.
- **Deployment relevance:** If nearly all competitive models achieve near-ceiling scores, the benchmark cannot discriminate between models for the deployment's use case. A score of 92% vs. 95% on HumanEval provides no information about relative capability for bug localization or diff generation in complex Django codebases.
- **Datapoint citations:**
  - [D8] Example HumanEval/42 (openai_humaneval, split=test): `def incr_list(l: list):\n    """Return list with elements incremented by 1."""` — canonical solution: `return [(e + 1) for e in l]` — trivially solvable by any capable LLM
  - [D34] Example HumanEval/14 (openai_humaneval, split=test): `def all_prefixes(string: str) -> List[str]:\n    """ Return list of all prefixes from shortest to longest..."` — canonical solution is a simple 3-line loop; near-zero challenge for modern models

#### MINOR

#### Concern 9: Occasional use of bare `except:` in canonical solutions — not idiomatic for professional code
- **Dimension(s):** OC
- **Observation:** HumanEval/105's canonical solution uses a bare `except: pass` block to silently swallow all exceptions from a dictionary lookup. HumanEval/124's canonical solution also uses a bare `try/except` for date parsing. Both are discouraged patterns in Python style guides (PEP 8, Google Python Style Guide).
- **Deployment relevance:** If a model trained to reproduce HumanEval-style solutions learns to generate bare `except:` blocks, it will produce code that professional reviewers may reject on convention grounds — directly relevant to the deployment's "convention adherence" success criterion.
- **Datapoint citations:**
  - [D20] Example HumanEval/105 (openai_humaneval, split=test): canonical solution contains `try:\n            new_arr.append(dic[var])\n        except:\n            pass` — bare exception catch silences all errors including programmer mistakes; not idiomatic professional Python
  - [D7] Example HumanEval/124 (openai_humaneval, split=test): canonical solution wraps entire body in `try: ... except: return False` — broad exception handling that masks potential bugs, contrary to the deployment's requirement that fixes not mask defects

#### Concern 10: Minor but observable function-name/task-description mismatches in some problems
- **Dimension(s):** IC
- **Observation:** HumanEval/66's function is named `digitSum` but the task is to sum ASCII codes of uppercase characters — not digits. This is a mild internal inconsistency between the function name (a form of documentation) and the specification.
- **Deployment relevance:** This is a very minor example of the naming/documentation mismatch condition the deployment cares about, though at a trivial scale compared to real-world legacy code. It does not meaningfully address the deployment's IC gap.
- **Datapoint citations:**
  - [D27] Example HumanEval/66 (openai_humaneval, split=test): `def digitSum(s):\n    """Task\n    Write a function that takes a string as input and returns the sum of the upper characters only' ASCII codes."` — function named `digitSum` but returns sum of uppercase ASCII values, not digit values

---

### Content Coverage Summary

The 40 sampled examples uniformly represent a single task type: docstring-to-function Python synthesis, where the model receives a complete, accurate natural language specification and must generate a functionally correct function body. Problems are drawn from five loose categories observable in the sample:

1. **String/character manipulation** (XOR on binary strings, cyclic encoding, substring rotation, character deletion — ~25% of sample)
2. **List/array algorithms** (filtering, sorting with custom keys, prefix generation, element increment — ~25%)
3. **Mathematical/numerical computation** (polynomial roots, prime checks, Collatz/Tribonacci sequences, digit sums — ~20%)
4. **Input validation and parsing** (date validation, music notation parsing, number-word sorting, fraction simplification — ~15%)
5. **Toy simulation/word problems** (fruit distribution, bank account balance, hungry rabbit carrot allocation — ~15%)

All problems are self-contained, operate on primitive Python types (lists, strings, integers, floats, tuples), and require no external library beyond `typing` and `math`. Docstrings are universally complete and accurate; worked examples appear in ~80% of problems. Average test suite size in the sample is approximately 6–8 assertions per problem.

The content is entirely consistent with the benchmark's documented design as an algorithm/interview-style evaluation. Nothing in the sample approaches the framework-specific, object-stateful, or documentation-sparse character of real-world professional Python codebases. The benchmark's self-description as targeting "language comprehension, reasoning, algorithms, and simple mathematics" is fully confirmed by the data.

---

### Limitations

1. **Sample size**: 40 of 164 problems (24%) were reviewed. The remaining ~76% may contain edge cases not seen here, but given the uniformity of the sampled task type, the core observations are unlikely to change materially.

2. **Canonical solution quality**: Only the visible bugs in HumanEval/124, HumanEval/32, HumanEval/158, and HumanEval/19 were identified through manual inspection of 40 examples. Additional canonical solution defects may exist in the unsampled 124 problems.

3. **Test suite adequacy**: The completeness of unit test coverage cannot be fully assessed from static inspection alone. Some test suites include `assert True` no-op placeholders (visible in HumanEval/104, HumanEval/121), but whether these gaps cause incorrect solutions to pass requires execution.

4. **No execution**: Pass/fail behavior of the test suites was not verified by running code. The operator precedence bug observed in HumanEval/124's canonical solution may or may not cause test failures depending on the specific test cases.

5. **Framework-specific gap confirmation**: The absence of Django/Flask/SQLAlchemy/NumPy examples is confirmed in the 40-example sample, but the full 164-problem set was not exhaustively verified. Given the paper's explicit description of the benchmark's scope ("language comprehension, reasoning, algorithms, and simple mathematics"), the absence is expected to hold across all 164 problems.

6. **Output form**: No model completions were inspected — only prompts and canonical solutions. The assessment of output form alignment (complete function body vs. targeted diff) is based on the structural design of the prompts, not on observed model outputs.

