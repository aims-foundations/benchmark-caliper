## Deployment Context

We are a US developer tools company building an inline code completion feature. When an American software engineer writes a Python docstring or function signature in their IDE, our tool autocompletes the function body. We need to evaluate whether the LLM can generate correct, self-contained Python functions from natural language specifications. Correctness is verified by automated test suites.

# Validity Analysis: humaneval
**Target context:** US Professional Software Engineers — Python IDE Inline Completion
**Overall risk:** MEDIUM

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology | 2 | Significant gaps | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 5 | Strong alignment | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content | 3 | Moderate gaps | high |
| Output Form ✓ | 5 | Strong alignment | high |
| **Average** | **3.0** | | |

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

For US professional software engineers using Python IDE inline completion, HumanEval provides a precisely-formatted but narrow evaluation. Input form and output form are excellent matches (5/5 each): English docstring + Python signature → function body sampled at standard temperatures, with execution-based scoring. The benchmark's hand-authored, contamination-resistant problems and unbiased pass@k estimator are genuine strengths. However, on the two HIGH-priority dimensions, the benchmark falls significantly short. Input content (1/5) is the largest concern: 40/40 sampled problems are dependency-free and stdlib-only, while the elicitation confirms the majority of real completions involve third-party libraries (pandas, FastAPI, SQLAlchemy, requests) or internal helpers — a gap the paper itself acknowledges [Q48]. Output ontology (2/5) is the next-largest: the binary pass/fail criterion discards idiomaticity and efficiency, both confirmed as user-relevant; dataset analysis shows canonical solutions themselves use bare `except:` and contain precedence bugs that the metric cannot surface. Input ontology (2/5) omits async/await, modern typing, and web-framework patterns. Output content (3/5) is conceptually sound but empirically compromised by EvalPlus's quantification of 19–29% score inflation and 11% ground-truth errors, plus dataset-confirmed filler `assert True` statements. HumanEval should be treated as a lower-bound algorithmic-correctness baseline, supplemented by HumanEval+ (test-suite reliability), DS-1000 (library-dependent completions), and emerging human-preference benchmarks (idiomaticity).

## Practical Guidance

### What This Benchmark Measures

HumanEval measures general-purpose Python function-synthesis correctness on hand-authored, dependency-free algorithmic and string-manipulation problems, scored binary via unit tests. For the deployment, it provides a calibrated lower-bound signal on the smallest but still relevant slice of real usage — interview-style algorithmic completions in self-contained contexts. Strongest dimensions (input form and output form, both 5/5) confirm the prompt/output modality precisely matches inline IDE completion.

### Construct Depth

The benchmark probes functional correctness shallowly but broadly within its taxonomy: 164 problems averaging 7.7 tests each, with documented per-problem coverage variance (some problems have only 3–6 functional assertions plus `assert True` filler [D11–D17, D25]). EvalPlus's 80× test-suite expansion [WEB-10] empirically demonstrates that base HumanEval over-credits models by 19–29%. The benchmark provides no depth at all on idiomaticity, efficiency, library-use appropriateness, async patterns, or typed-signature complexity — all confirmed user-relevant quality dimensions per the elicitation.

### What Else You Need

To approach a complete evaluation for this deployment, supplement HumanEval with: (1) HumanEval+ [WEB-11] as the minimum baseline to address the output_content reliability gap; (2) DS-1000 [WEB-4] to address the input_content/input_ontology pandas/numpy gap; (3) SWE-bench Verified [WEB-7] for repo-context completion (though more agentic than inline); (4) an internal evaluation incorporating linter-based idiomaticity scoring and accept/reject telemetry to address the output_ontology style gap; (5) a custom evaluation of async/await and typed-signature synthesis, since no public benchmark fills these gaps per regional research.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
HumanEval's taxonomy is explicitly 'language comprehension, reasoning, algorithms, and simple mathematics' [Q22] — interview-style algorithmic problems. The deployment elicitation confirms a large production gap: pandas/numpy data manipulation, Flask/FastAPI route handlers, async/await I/O, and heavily typed signatures form a major share of real completions. Dataset analysis of 40 problems confirms zero async functions, only primitive `List[T]` typing, and no third-party library tasks. The paper itself acknowledges the distribution mismatch [Q48]. With IO marked MODERATE priority and explicit acknowledgement that this is a lower-bound starting point, a score of 2 reflects significant construct underrepresentation while recognizing the algorithmic core is genuinely covered.

**Strengths:**
- Hand-authored coverage of core algorithmic categories (bracket matching, sorting, sequences, polynomial roots, string manipulation) is broad within its scope and provides a meaningful lower-bound signal for general-purpose correctness.

**Checklist:**

- **IO-1**: Required categories per elicitation: data manipulation (pandas/numpy), web framework route handlers (Flask/FastAPI/Django), async/await patterns, heavily type-annotated complex signatures, and general algorithmic correctness. Only the last is covered by HumanEval [Q22]. — _Sources: Q22_
- **IO-2**: Yes — HumanEval's taxonomy omits pandas/numpy data workflows, async/await, web framework idioms, and modern typed APIs. The paper acknowledges class implementations, configurations, and scripts in real GitHub data are absent from the synthesis task [Q48]. Dataset analysis confirms no async, no third-party libs, no modern typing across 40 sampled problems [D1, D6, D32]. — _Sources: Q48, Q22, WEB-4, WEB-7, D1, D6_
- **IO-3**: No category in HumanEval is positively irrelevant to the target population — interview-style algorithmic problems remain a (smaller) part of professional engineering practice. The narrative/puzzle framings ('hungry rabbit', 'Tribonacci') introduce minor stylistic mismatch but the underlying task categories are still in-scope [D27, D28]. — _Sources: D27, D28_
- **IO-4**: Documented gaps harming content validity: (a) async/await — no benchmark in the field fills this per regional research [gap_id 2 NOT FOUND]; (b) typed-signature synthesis — same gap; (c) web framework boilerplate — confirmed unaddressed [gap_id 3 NOT FOUND]; (d) library-dependent completions — partially addressed by DS-1000 [WEB-4] and SWE-bench [WEB-7] as supplements. — _Sources: WEB-4, WEB-7, WEB-2_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'Programming tasks in the HumanEval dataset assess language comprehension, reasoning, algorithms, and simple mathematics.' (p.4)
- [Q48] 'Python code found on GitHub contains class implementations, configuration files, scripts, and even files used to store data. This code is seemingly unrelated to synthesizing functions from docstrings, and we hypothesize that the distribution mismatch reduces HumanEval performance.' (p.7)
- [Q88] 'Codex struggles to parse through increasingly long and higher-level or system-level specifications.' (p.10)

*Web sources:*
- [WEB-4] DS-1000 provides 1,000 data-science problems across seven libraries — supplements pandas/numpy gap
- [WEB-7] SWE-bench finding: models 'do not leverage existing third-party libraries' — corroborates taxonomy gap
- [WEB-2] FastAPI adoption grew from 29% to 38% among Python developers in 2024 — amplifies web-framework gap

*Dataset analysis:*
- DATASET-D1: HumanEval/0 uses only `List[float]` — most complex typing observed across sample
- DATASET-D6: HumanEval/34 uses only `from typing import List`; no domain library across 40 problems
- DATASET-D8: HumanEval/61 bracket-matching is canonical algorithmic problem — within scope
- DATASET-D9: HumanEval/130 Tribonacci — pure math recursion typical of HumanEval taxonomy

</details>

**Information gaps:**
- No quantification in the paper of what fraction of real-world completions fall in each category
- Async/await and typed-signature benchmarks remain unaddressed in the literature per regional research

**Requires expert verification:**
- Empirical distribution of completion categories observed in the deploying organization's actual user telemetry

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Input content is the highest-priority dimension per elicitation (HIGH). HumanEval problems are 'hand-written and not programmatically copied from existing sources' [Q14, Q21] and are explicitly self-contained — every sampled problem uses at most stdlib (`math`, `typing`) [D3, D5, D6]. The elicitation states 'the majority of real completions reference imports already in the file, internal helper modules, or third-party libraries (requests, sqlalchemy, pandas).' Dataset analysis confirms zero third-party libraries across 40 sampled problems [Concern 1]. The paper itself flags this as a distribution mismatch [Q48]. Several docstrings also use narrative/puzzle register ('hungry rabbit', 'In this task') rather than professional API style [D26, D27, D28], adding further content mismatch. Score 1 reflects the magnitude of this gap on a HIGH-priority dimension.

**Strengths:**
- Hand-authored problems explicitly avoid GitHub contamination [Q14, Q21] — preserves the integrity of the correctness signal for models trained on public code, confirmed by dataset analysis showing idiosyncratic framings unlikely to appear in training data [D26, D27].

**Checklist:**

- **IC-1**: Region-specific knowledge is minimal — the deployment is US English-speaking professional engineers. One minor instance: HumanEval/124 hardcodes US MM-DD-YYYY date format as correct and rejects ISO 8601 [D10, D35]. This aligns with US deployment but represents a regional encoding. — _Sources: D10, D35_
- **IC-2**: Culturally aligned — both benchmark designers and target users are professional engineers in the US/Global North Python ecosystem; no cultural mismatch.
- **IC-3**: No problematic Western-specific knowledge for this deployment; the US date format is in fact aligned with the population.
- **IC-4**: Not necessary — population and benchmark designers share technical culture; the validity concerns are structural (dependency-free, register) rather than culturally annotative.
- **IC-5**: Major content gaps: (a) zero third-party library usage in 40/40 sampled problems [D3, D5, D6] vs. majority of real completions using imports [elicitation A3]; (b) no internal helper / multi-file context — only HumanEval/32 and /38 use a second function in the prompt [D29, D30]; (c) docstring register skews narrative/puzzle rather than `Args:`/`Returns:` professional style [D26, D27, D28]; (d) paper acknowledges distribution mismatch [Q48] but does not quantify it. — _Sources: Q48, D3, D5, D6, D26, D27, D28, WEB-4, WEB-7_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q14] 'Though not a guarantee for problem novelty, all problems were hand-written and not programmatically copied from existing sources.' (p.3)
- [Q19] 'We evaluate functional correctness on a set of 164 hand-written programming problems, which we call the HumanEval dataset.' (p.4)
- [Q48] 'we hypothesize that the distribution mismatch reduces HumanEval performance.' (p.7)
- [Q21] 'It is important for these tasks to be hand-written, since our models are trained on a large fraction of GitHub, which already contains solutions to problems from a variety of sources.' (p.4)

*Web sources:*
- [WEB-4] DS-1000 covers seven data-science libraries with 1.8% false-accept rate — direct supplement for library-dependent completions
- [WEB-7] SWE-bench provides 2,294 repo-level Python tasks; finding that models 'do not leverage existing third-party libraries' corroborates the input_content gap
- [WEB-2] FastAPI adoption widening (29%→38% in 2024) — production-distribution mismatch is growing year over year

*Dataset analysis:*
- DATASET-D3: HumanEval/32 — only stdlib `import math`; no pip dependency
- DATASET-D5: HumanEval/38 — no imports at all
- DATASET-D6: HumanEval/34 — typing-only import; no domain library
- DATASET-D26: HumanEval/67 — 'In this task' narrative register, not professional API docstring
- DATASET-D27: HumanEval/159 — 'You're a hungry rabbit' puzzle framing
- DATASET-D35: HumanEval/124 — US date format MM-DD-YYYY hardcoded as correct; ISO 8601 rejected

</details>

**Information gaps:**
- Paper does not quantify what fraction of real GitHub Python code uses third-party libraries vs. self-contained patterns
- No empirical telemetry from the deployment's user base on import-frequency distribution

**Requires expert verification:**
- Audit of the deploying organization's actual completion logs to confirm the elicitation's claim that 'majority' of completions involve imports

---

### Input Form — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
Input form is a precise match. HumanEval prompts consist of 'a header, a signature, and a docstring' in plain Python text [Q28], which is exactly the IDE inline-completion trigger described in the deployment context. Stop sequences (`\nclass`, `\ndef`, etc.) [Q29] match how IDE completions naturally terminate. Dataset analysis confirms every sampled problem follows this format [D1, D7, D29]. No modality mismatch, no script issues (Latin/ASCII throughout), no infrastructure constraint. IF was marked LOWER priority precisely because of this alignment.

**Strengths:**
- Signature + English docstring → function body prompt format is identical to the IDE inline completion trigger [Q28, D1]
- Stop-token handling matches natural IDE completion boundaries [Q29]
- Latin script / ASCII / UTF-8 / standard sandboxed Python execution — zero infrastructure mismatch with deployment

**Checklist:**

- **IF-1**: Signal distributions match exactly — text-in/code-out, English docstring + Python signature. Standard sandboxed Python execution sufficient [Q28, Q29]. — _Sources: Q28, Q29, D1_
- **IF-2**: US developer infrastructure (VS Code at 48% primary IDE share, PyCharm 25%, per PSF/JetBrains 2024) supports the same plain-text prompt/completion format used by HumanEval [WEB-1, WEB-2]. — _Sources: WEB-1, WEB-2_
- **IF-3**: One domain-specific observation: HumanEval typing is limited to legacy `from typing import List` and primitives; no `async def`, no `Optional/Union`, no PEP 604 `X | Y`, no dataclass, no Protocol [D1, D2, D32]. This is more an ontology gap than a pure form gap, but to the extent 'form' includes modern syntactic constructs, the benchmark's form is somewhat dated relative to Python 3.11–3.13 (the dominant versions per [WEB-1]). — _Sources: D1, D2, D32, WEB-1_
- **IF-4**: No form mismatch that materially harms external validity for the deployment's primary text-in/code-out modality. — _Sources: Q28_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q28] 'To compute pass@k, we assemble each HumanEval problem into a prompt consisting of a header, a signature, and a docstring, which is illustrated in Figure 2.' (p.4)
- [Q29] 'We sample tokens from Codex until we encounter one of the following stop sequences: \nclass, \ndef, \n#, \nif, or \nprint, since the model will continue generating additional functions or statements otherwise.' (p.4)
- [Q20] 'Each problem includes a function signature, docstring, body, and several unit tests, with an average of 7.7 tests per problem.' (p.4)

*Web sources:*
- [WEB-1] PSF/JetBrains Python Developers Survey 2024 — VS Code 48% primary IDE share, PyCharm 25%, confirms text-based IDE completion is universal
- [WEB-2] Python 3.11–3.13 dominant versions; modern syntax beyond HumanEval's coverage

*Dataset analysis:*
- DATASET-D1: HumanEval/0 — signature + docstring + List typing matches IDE trigger format
- DATASET-D7: HumanEval/17 — `>>>` example notation in docstring mirrors real engineering docstrings
- DATASET-D29: HumanEval/32 — two-function prompt confirms multi-function context handling
- DATASET-D32: HumanEval/76 — completely untyped signature; benchmark covers untyped cases too

</details>

**Information gaps:**
- Whether the deployment's IDE plugin prepends additional context (open file contents, other files in workspace) that HumanEval does not simulate

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Output ontology is HIGH priority per elicitation. HumanEval's output ontology is binary functional correctness: 'correctness is defined by passing a set of unit tests' [Q77]. The paper extensively argues this supersedes BLEU [Q10, Q18, Q40] — a genuine strength. However, the paper itself acknowledges that pass@k does not distinguish among functionally equivalent solutions [Q86] and that the autocomplete deployment requires a single-sample heuristic [Q37, Q38] for which mean log probability is the only recommendation [Q39] — no idiomaticity or efficiency signal is incorporated. The elicitation directly confirms that 'users will reject non-idiomatic completions even when functionally correct' and 'two passing solutions are considered substantively different in quality by end users.' Dataset analysis shows canonical solutions themselves use anti-idiomatic patterns (bare `except:` in HumanEval/105, operator-precedence bugs) that the binary metric cannot surface [D21, D33]. Score 2 reflects significant scoring-function misalignment with the user-relevant quality dimension on a HIGH-priority dimension.

**Strengths:**
- Functional correctness over BLEU is well-justified and demonstrated empirically [Q40] — eliminates a major class of false signals
- Test-driven development framing [Q12] aligns with professional engineering practice
- Unbiased pass@k estimator [Q15, Q17, Q138] addresses statistical bias other reports do not
- Paper explicitly identifies the autocomplete single-sample selection problem [Q37, Q38] and recommends mean log probability as a heuristic [Q39]

**Checklist:**

- **OO-1**: Binary pass/fail [Q77] is relevant to the deployment's primary signal but does not cover idiomaticity (rank-2 signal in elicitation) or efficiency (rank-3 signal). The elicitation explicitly identifies these as user-relevant quality dimensions not captured by binary pass@k. — _Sources: Q77, Q86_
- **OO-2**: Missing categories: idiomaticity scoring (style, PEP-8 adherence, avoidance of bare `except:` etc.), efficiency scoring, library-use appropriateness. CodeArena [WEB-8] and BigCodeArena [WEB-9] are emerging human-preference benchmarks that begin to address this but are not Python-specific. — _Sources: Q86, Q148, Q149, WEB-8, WEB-9, D33_
- **OO-3**: No category in HumanEval encodes non-regional values — the cryptographic security thresholds (RSA ≥ 2048, no ECB mode) [Q208, Q209, Q210] reflect standard professional consensus aligned with US engineering practice. — _Sources: Q208, Q209, Q210_
- **OO-4**: Stakeholder-driven extension would add: (a) linter-based idiomaticity score, (b) runtime/complexity efficiency check, (c) human-preference pairwise comparison per CodeArena methodology [WEB-8]. The deployment's elicitation confirms users would value these signals. — _Sources: WEB-8, WEB-9, Q39_
- **OO-5**: Documented harm to structural and content validity: the binary criterion treats `try: ... except: pass` solutions [D33] identically to clean idiomatic implementations, and treats O(n³) prime factorization identically to O(n log log n) — collapsing a quality dimension the user population explicitly cares about. Paper itself acknowledges deferred qualitative metrics [Q86, Q148, Q149]. — _Sources: Q77, Q86, D21, D22, D33_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q77] 'When we benchmark our code generation models, we measure pass@k on the HumanEval dataset, where correctness is defined by passing a set of unit tests.' (p.9)
- [Q37] 'From a practical perspective, we are also interested in the setting where we must select a single sample from k samples without having access to an oracle.' (p.5)
- [Q38] 'when the model is used as an autocomplete tool where a user provides a prompt, we do not have unit tests, but would like to return only a single completion to the user' (p.5)
- [Q86] 'we developed a set of qualitative metrics for measuring the capabilities of code generating models while controlling for the complexity and abstraction level of the specifications (Appendix D).' (p.10)
- [Q40] 'when we plot the distributions of BLEU scores for correct and incorrect solutions, we notice significant overlap ... improvements in BLEU score may not indicate improved rates of functional correctness in practice.' (p.6)

*Web sources:*
- [WEB-8] CodeArena (2024) — human-preference benchmark; reveals gap between execution-based and preference-based scoring across 40+ LLMs
- [WEB-9] BigCodeArena (2024) — crowdsourced human pairwise preference platform, 14K+ sessions, confirms binary pass/fail misses preference signal

*Dataset analysis:*
- DATASET-D33: HumanEval/105 canonical solution uses bare `except:` — anti-idiomatic but passes; binary metric cannot distinguish
- DATASET-D21: HumanEval/124 canonical solution has operator-precedence bug yet passes test suite — correctness signal itself contaminated
- DATASET-D22: HumanEval/105 canonical solution sorts entire array descending instead of filtering 1–9 first — obscures intent but still passes

</details>

**Information gaps:**
- No automated, deployment-ready Python-specific idiomaticity metric is identified in either paper or regional research
- Paper defers qualitative metrics to 'forthcoming work' [Q149] which is not directly usable

**Requires expert verification:**
- Whether the deploying team's user acceptance telemetry (accept/reject rates) correlates with pass@k or diverges based on style — this would empirically confirm the elicited concern

---

### Output Content — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
Output content (label correctness) was rated LOWER priority because labels are objective unit-test outcomes [Q77] authored by domain insiders sharing the target population's technical culture. This is a real strength. However, dataset analysis reveals significant label-quality issues: (a) filler `assert True` statements appear in ≥8 of 40 sampled test suites [D11–D16]; (b) several test suites have only 3–6 functional assertions [D17, D18, D25]; (c) the canonical solution for HumanEval/124 contains an operator-precedence bug not surfaced by the test suite [D21]; (d) EvalPlus (NeurIPS 2023) [WEB-10] empirically quantifies that scores drop 19.3–28.9% across 26 LLMs when tests are expanded 80×, and 11% of original ground-truth solutions contain errors. The paper itself acknowledges 'some prompts underspecify the function' [Q63] and that human test suites have limited coverage [Q129]. Score 3 reflects strong conceptual alignment (objective labels, no cultural mismatch) tempered by empirically documented label-quality problems.

**Strengths:**
- Objective unit-test outcomes [Q77] eliminate annotator subjectivity that plagues many benchmarks
- Annotator population (OpenAI engineers + collaborators) shares technical culture with US professional engineers — no cross-cultural label mismatch
- Docstring-generation evaluation [Q78, Q79] uses transparent grading rule (excluding code-copying [Q81]) even though IAA is not reported

**Checklist:**

- **OC-1**: Ground truth (unit-test pass/fail) reflects regional stakeholder perspectives directly — US professional engineers use the same functional-correctness criterion. No cultural mismatch. — _Sources: Q77_
- **OC-2**: Disagreement between original annotators and target population is minimal at the labeling level. The disagreement is structural (binary vs. quality-aware) rather than annotative. — _Sources: Q77_
- **OC-3**: Paper does not report annotator demographics for docstring-grading or test-suite-authoring [Q79 notes 1,640 judgments but no demographic breakdown]. INSUFFICIENT DOCUMENTATION on who authored test suites and their qualifications.
- **OC-4**: Re-annotation is not the primary remediation here; test-suite augmentation (EvalPlus [WEB-10]) is. EvalPlus has already done this work — adopting HumanEval+ closes most of the label-correctness gap. — _Sources: WEB-10, WEB-11_
- **OC-5**: Aggregation method (pass@k unbiased estimator [Q15, Q138]) is statistically sound and does not erase minority perspectives — the issue is the underlying test suites' coverage, not aggregation. — _Sources: Q15_
- **OC-6**: Documented label issues: filler `assert True` statements [D11–D16, Concern 3], thin per-problem coverage [D17, D18, D25], operator-precedence bug in HumanEval/124 canonical solution [D21], paper acknowledgement of underspecified prompts [Q63] and limited test coverage [Q129], and EvalPlus's quantification of 19–29% score inflation and 11% ground-truth errors [WEB-10]. — _Sources: Q63, Q129, D11, D13, D14, D17, D21, D25, WEB-10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q63] 'Some prompts underspecify the function that is implemented, in which case a perfectly valid solution may be wrongly penalized by the unit test.' (p.8)
- [Q79] 'Due to the time consuming nature of this process, we only grade 10 samples per problem, for a total of 1640 problems, from Codex-D-12B at temperature 0.8.' (p.9)
- [Q129] 'Human developers often write test suites with limited but targeted coverage, but this does not always work well against an algorithm, highlighting the challenges of evaluating correctness of programs.' (p.14)
- [Q77] 'correctness is defined by passing a set of unit tests.' (p.9)

*Web sources:*
- [WEB-10] EvalPlus (NeurIPS 2023) — expands HumanEval test suite 80×; scores drop 19.3–28.9% across 26 LLMs; 11% of original ground-truth solutions contain errors
- [WEB-11] EvalPlus GitHub — HumanEval+ available as drop-in replacement
- [WEB-12] AlphaXiv EvalPlus summary confirms model rankings flip on HumanEval+ vs. base

*Dataset analysis:*
- DATASET-D11: HumanEval/105 contains `assert True, "This prints if this assert fails"` filler — zero coverage
- DATASET-D13: HumanEval/145 — filler assert at end of edge-cases section
- DATASET-D14: HumanEval/121 — section header 'edge cases' with no following assertions
- DATASET-D17: HumanEval/72 — only 6 functional assertions
- DATASET-D18: HumanEval/123 — only 4 test cases for an infinite-sequence function
- DATASET-D21: HumanEval/124 — canonical solution operator-precedence bug not caught by test suite
- DATASET-D25: HumanEval/11 — only 3 test cases for XOR function

</details>

**Information gaps:**
- Inter-annotator agreement for docstring-grading not reported [Q79]
- Annotator demographics and qualification criteria not documented
- Per-problem test coverage variance not analyzed in original paper

---

### Output Form — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
Output form is a precise match: HumanEval expects open-ended Python function bodies sampled via nucleus sampling [Q30], which is exactly the deployment's output modality. Dataset analysis confirms all problems output Python function bodies evaluated via `assert` statements [Strength 2, D8, D34]. The paper explicitly discredits BLEU as a reliability indicator [Q18, Q40], aligning with the deployment's preference for execution-based evaluation. OF was marked LOWER priority precisely because of this fit.

**Strengths:**
- Open-ended Python text output matches IDE inline-completion output modality exactly [Q30]
- Unbiased pass@k estimator [Q15, Q17, Q138, Q143] provides statistically sound scoring
- BLEU explicitly discredited [Q18, Q40] — eliminates a misleading form-based metric
- Temperature optimization per k [Q34] supports the deployment's k=1 inline-completion setting (T*=0.2)

**Checklist:**

- **OF-1**: Expected output modality (Python function body as text) matches deployment requirements exactly [Q30, D8]. — _Sources: Q30, D8_
- **OF-2**: Not applicable — text/code modality, no speech-output requirement.
- **OF-3**: Not applicable — population is professional software engineers with full technical literacy; no accessibility constraints differentiate this deployment.
- **OF-4**: No form mismatches identified. The only minor caveat: pass@k assumes oracle access for ranking, while inline-completion returns a single sample; the paper addresses this with mean log probability as a heuristic [Q39], but this is a scoring-procedure issue (output ontology) rather than output form. — _Sources: Q39_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q30] 'We use nucleus sampling (Holtzman et al., 2020) with top p = 0.95 for all sampling evaluation in this work.' (p.4)
- [Q18] 'BLEU score may not be a reliable indicator of functional correctness' (p.3)
- [Q34] 'for a 679M parameter model, the optimal temperature for pass@1 is T* = 0.2 and the optimal temperature for pass@100 is T* = 0.8.' (p.5)
- [Q39] 'choosing the sample with the highest mean token log probability outperforms evaluating a random sample' (p.5)

*Dataset analysis:*
- DATASET-D8: HumanEval/61 — 12 boolean assertions over generated function body output
- DATASET-D34: HumanEval/32 — numeric tolerance assertion `math.fabs(...) < 1e-4` over generated function output

</details>

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** Zero third-party library usage in benchmark; elicitation confirms majority of real completions involve imports (pandas, FastAPI, SQLAlchemy, requests)

**Recommendation:** Adopt DS-1000 [WEB-4] alongside HumanEval as the primary library-dependent evaluation. DS-1000's 1,000 problems across seven libraries with 1.8% false-accept rate directly address the pandas/numpy slice of the deployment's production distribution.

### Output Ontology ⚠

**Gap:** Binary pass/fail discards idiomaticity and efficiency — both confirmed user-relevant; canonical solutions themselves use bare `except:` and non-idiomatic patterns [D33, D22]

**Recommendation:** Layer a Python-specific style scoring pass (pylint or ruff) on top of pass@k, and stand up an internal pairwise human-preference evaluation following the CodeArena/BigCodeArena methodology [WEB-8, WEB-9]. Use deployment accept/reject telemetry as a proxy for the missing idiomaticity signal.

### Output Ontology ⚠

**Gap:** Pass@k assumes oracle test access; inline completion returns a single sample without tests [Q37, Q38]

**Recommendation:** Operationalize the paper's mean-log-probability heuristic [Q39] as a baseline single-sample ranker, but evaluate it against alternative rankers (e.g., reranker models, style-score-weighted ranking) using deployment accept/reject telemetry as ground truth.

### Input Ontology

**Gap:** No async/await, no modern typing (Optional/Union/Protocol/dataclass/PEP 604), no web-framework patterns; gaps confirmed as unfilled in published literature

**Recommendation:** Build an internal mini-benchmark targeting these three explicit gaps (async function synthesis, complex typed signatures, FastAPI/Flask route handlers) sized at 50–100 hand-authored problems following HumanEval methodology. This is the only available path since no public benchmark covers these patterns.

### Input Ontology

**Gap:** No multi-file or repo-context completion in HumanEval; deployment files typically contain pre-existing imports and helpers

**Recommendation:** Add SWE-bench Verified [WEB-7] as a secondary agentic-coding signal, while recognizing it tests a different (multi-file editing) use case than inline completion. For inline-completion-specific repo-context evaluation, consider building an internal eval from real workspace contexts.

### Output Content

**Gap:** Filler `assert True` statements, thin per-problem coverage, and canonical-solution bugs (e.g., HumanEval/124 precedence error) inflate pass rates; EvalPlus quantifies 19–29% score inflation across 26 LLMs

**Recommendation:** Replace base HumanEval with HumanEval+ [WEB-11] as the minimum reliability bar. EvalPlus has already done the 80× test-suite augmentation and corrected 11% of buggy ground-truth solutions.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "We introduce Codex, a GPT language model finetuned on publicly available code from GitHub, and study its Python code-writing capabilities." |
| Q2 | 1 | output_form | "On HumanEval, a new evaluation set we release to measure functional correctness for synthesizing programs from docstrings, our model solves 28.8% of the problems, while GPT-3 solves 0% and GPT-J solves 11.4%." |
| Q3 | 1 | output_form | "Furthermore, we find that repeated sampling from the model is a surprisingly effective strategy for producing working solutions to difficult prompts." |
| Q4 | 1 | output_form | "Using this method, we solve 70.2% of our problems with 100 samples per problem." |
| Q5 | 1 | input_ontology | "Careful investigation of our model reveals its limitations, including difficulty with docstrings describing long chains of operations and with binding operations to variables." |
| Q6 | 1 | output_ontology | "Finally, we discuss the potential broader impacts of deploying powerful code generation technologies, covering safety, security, and economics." |
| Q7 | 1 | input_ontology | "This paper describes several early Codex models, whose descendants power GitHub Copilot and the Codex models in the OpenAI API." |
| Q8 | 2 | output_form | "In this section, we discuss the details of our evaluation framework. We begin by defining the pass@k metric, and explain its advantages over standard match-based metrics. Next, we describe the dataset of hand-written problems, called "HumanEval," which we created in order to benchmark our models. Finally, we discuss the sandbox environment we used to safely execute model-generated code." |
| Q9 | 2 | output_form | "Generative models for code are predominantly benchmarked by matching samples against a reference solution, where the match can be exact or fuzzy (as in BLEU score)." |
| Q10 | 2 | output_ontology | "More fundamentally, match-based metrics are unable to account for the large and complex space of programs functionally equivalent to a reference solution." |
| Q11 | 2 | output_ontology | "We argue that this metric should be applied to docstring-conditional code generation as well." |
| Q12 | 2 | output_ontology | "Perhaps the most convincing reason to evaluate functional correctness is that it is used by human developers to judge code. A framework known as test-driven development dictates that software requirements be converted into test cases before any implementation begins, and success is defined by a program that passes these tests." |
| Q13 | 2 | output_form | "Kulal et al. (2019) evaluate functional correctness using the pass@k metric, where k code samples are generated per problem, a problem is considered solved if any sample" |
| Q14 | 3 | input_content | "Though not a guarantee for problem novelty, all problems were hand-written and not programmatically copied from existing sources." |
| Q15 | 3 | output_form | "To evaluate pass@k, we generate n ≥ k samples per task (in this paper, we use n = 200 and k ≤ 100), count the number of correct samples c ≤ n which pass unit tests, and calculate the unbiased estimator." |
| Q16 | 3 | output_form | "Calculating this estimator directly results in very large numbers and numerical instability." |
| Q17 | 3 | output_form | "One may be tempted to estimate pass@k with 1−(1−p̂)^k where p̂ is the empirical estimate of pass@1, but we show that it is biased in Appendix A." |
| Q18 | 3 | output_ontology | "Later, we provide evidence that BLEU score may not be a reliable indicator of functional correctness by showing that functionally inequivalent programs generated by our model (which are guaranteed to disagree with the reference solution on some input) often have higher BLEU scores than functionally equivalent ones." |
| Q19 | 4 | input_content | "We evaluate functional correctness on a set of 164 hand-written programming problems, which we call the HumanEval dataset." |
| Q20 | 4 | input_form | "Each problem includes a function signature, docstring, body, and several unit tests, with an average of 7.7 tests per problem." |
| Q21 | 4 | input_content | "It is important for these tasks to be hand-written, since our models are trained on a large fraction of GitHub, which already contains solutions to problems from a variety of sources." |
| Q22 | 4 | input_ontology | "Programming tasks in the HumanEval dataset assess language comprehension, reasoning, algorithms, and simple mathematics." |
| Q23 | 4 | input_content | "Our training dataset was collected in May 2020 from 54 million public software repositories hosted on GitHub, containing 179 GB of unique Python files under 1 MB." |
| Q24 | 4 | input_form | "We filtered out files which were likely auto-generated, had average line length greater than 100, had maximum line length greater than 1000, or contained a small percentage of alphanumeric characters." |
| Q25 | 4 | input_content | "After filtering, our final dataset totaled 159 GB." |
| Q26 | 4 | input_form | "We train Codex using the same learning rate as the corresponding GPT model, with a 175 step linear warmup and cosine learning rate decay." |
| Q27 | 4 | input_form | "We train for a total of 100 billion tokens, using the Adam optimizer with β1 = 0.9, β2 = 0.95, ε = 10−8, and a weight decay coefficient of 0.1." |
| Q28 | 4 | input_form | "To compute pass@k, we assemble each HumanEval problem into a prompt consisting of a header, a signature, and a docstring, which is illustrated in Figure 2." |
| Q29 | 4 | input_form | "We sample tokens from Codex until we encounter one of the following stop sequences: '\nclass', '\ndef', '\n#', '\nif', or '\nprint', since the model will continue generating additional functions or statements otherwise." |
| Q30 | 4 | output_form | "We use nucleus sampling (Holtzman et al., 2020) with top p = 0.95 for all sampling evaluation in this work." |
| Q31 | 5 | output_form | "model test loss follows a power law in model size (Kaplan et al., 2020), test loss after code fine-tuning follows a similar power law with functional form (N / 5.92×10^7)^-0.13 where N is the number of non-embedding parameters in the model." |
| Q32 | 5 | output_form | "When evaluating pass@k, it is important to optimize sampling temperature for the particular value of k." |
| Q33 | 5 | output_form | "We find that higher temperatures are optimal for larger k, because the resulting set of samples has higher diversity, and the metric rewards only whether the model generates any correct solution." |
| Q34 | 5 | output_form | "In particular, for a 679M parameter model, the optimal temperature for pass@1 is T* = 0.2 and the optimal temperature for pass@100 is T* = 0.8." |
| Q35 | 5 | output_form | "With these temperatures, we find that pass@1 and pass@100 scale smoothly as a function of model size (Figure 6)." |
| Q36 | 5 | output_form | "Pass@k can also be interpreted as the result of evaluating the best out of k samples, where the best sample is picked by an oracle with prior knowledge of the unit tests." |
| Q37 | 5 | output_ontology | "From a practical perspective, we are also interested in the setting where we must select a single sample from k samples without having access to an oracle." |
| Q38 | 5 | output_ontology | "For instance, when the model is used as an autocomplete tool where a user provides a prompt, we do not have unit tests, but would like to return only a single completion to the user for evaluation so as to not overwhelm them." |
| Q39 | 5 | output_form | "Inspired by similar work in language modeling, we find that choosing the sample with the highest mean token log probability outperforms evaluating a random sample, while choosing the sample based on sum log probability can perform slightly worse than picking randomly." |
| Q40 | 6 | output_ontology | "Finally, we compute BLEU scores for all Codex-12B HumanEval samples (at temperature 0.8) against their reference solutions. For each problem, when we plot the distributions of BLEU scores for correct and incorrect solutions, we notice significant overlap (Figure 8). Since an incorrect solution is guaranteed to be functionally inequivalent to the reference solution, we conclude that improvements in BLEU score may not indicate improved rates of functional correctness in practice." |
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
| Q65 | 8 | input_form | "To address these issues, we use Codex-12B to generate 100 samples per curated problem. If no samples pass the unit tests, we consider the task to be either ambiguous or too difficult, and filter it out." |
| Q66 | 8 | input_form | "We reran this verification several times to remove stateful or non-deterministic problems." |
| Q67 | 8 | input_form | "We fine-tune Codex on these training problems to produce a set of "supervised fine-tuned" models, which we call Codex-S." |
| Q68 | 8 | input_form | "To produce examples from training problems, we assemble the problems into the format shown in Figure 2." |
| Q69 | 8 | input_form | "If there are prompts of varying length in a batch, we left-pad shorter prompts to the length of the longest prompt, so that the first tokens in the reference solutions line up in context." |
| Q70 | 8 | output_content | "We train to minimize negative log-likelihood of the reference solution, and mask out loss for any tokens in the prompt." |
| Q71 | 8 | input_form | "We train using a learning rate 1/10 as large as used for fine-tuning Codex, but adhere to the same learning rate schedule, and train until validation loss plateaus (less than 10B tokens)." |
| Q72 | 8 | output_form | "As with Codex, we first compute the optimal temperature for evaluating pass@k for 1 ≤ k ≤ 100." |
| Q73 | 8 | output_form | "We find that Codex-S prefers slightly higher temperatures for all k > 1, which possibly reflects the fact that Codex-S captures a narrower distribution than Codex." |
| Q74 | 8 | output_form | "We use T∗ = 0 for computing pass@1 and T∗ = 1 for computing pass@100." |
| Q75 | 8 | output_form | "Next, we compare Codex-S against Codex on pass@1 and pass@100. Codex-S outperforms the corresponding Codex by an average margin of 6.5 percentage points on pass@1 and by a larger average margin of 15.1 percentage points on pass@100 across model size." |
| Q76 | 8 | output_form | "We also plot the performance of different sample selection heuristics for Codex-S-12B against the same heuristics for Codex-12B. When ranking between 1 and 100 samples by mean log probability, the average benefit over random ranking is 11.6 percentage points, which is over 2 percentage points higher than the corresponding benefit for Codex." |
| Q77 | 9 | output_ontology | "When we benchmark our code generation models, we measure pass@k on the HumanEval dataset, where correctness is defined by passing a set of unit tests." |
| Q78 | 9 | output_ontology | "However, there is no similar way to evaluate docstring samples automatically. Therefore, we grade sample docstrings by hand, considering a docstring correct if it uniquely and accurately specifies the code body." |
| Q79 | 9 | output_content | "Due to the time consuming nature of this process, we only grade 10 samples per problem, for a total of 1640 problems, from Codex-D-12B at temperature 0.8." |
| Q80 | 9 | output_content | "Codex-D often generates incorrect unit tests along with a docstring, but we ignore these during grading." |
| Q81 | 9 | output_ontology | "However, we do not consider the docstring correct when the model simply copies the code body into the docstring." |
| Q82 | 9 | output_content | "The most common failure modes we observe are when the docstring model leaves out an important detail (such as "an answer must be to two decimal places") or when it over-conditions on the function name and invents a problem unrelated to the function body." |
| Q83 | 9 | output_content | "While generating docstrings may be more forgiving because natural language syntax is less strict than code syntax, docstrings in our dataset may be lower quality because developers tend to devote less time to writing docstrings." |
| Q84 | 10 | output_form | "Table 3. Pass rates for our docstring generating model Codex-D, which is evaluated by hand-grading 10 samples per task due to the lack of a ground-truth automatic evaluation." |
| Q85 | 10 | input_content | "First, Codex is not sample efficient to train. Our training dataset comprises a significant fraction of publicly available Python code on GitHub, totaling hundreds of millions of lines of code." |
| Q86 | 10 | output_ontology | "While evaluating code generation is well-studied (Xu et al., 2021; Helmuth & Spector, 2015; Pantridge et al., 2017), many existing metrics measure performance in tightly specified, constrained problem instances (e.g., string manipulation in FlashFill (Gulwani, 2011)). Therefore, we developed a set of qualitative metrics for measuring the capabilities of code generating models while controlling for the complexity and abstraction level of the specifications (Appendix D)." |
| Q87 | 10 | output_content | "Applying this framework, we find that Codex can recommend syntactically incorrect or undefined code, and can invoke functions, variables, and attributes that are undefined or outside the scope of the codebase." |
| Q88 | 10 | input_ontology | "Moreover, Codex struggles to parse through increasingly long and higher-level or system-level specifications." |
| Q89 | 10 | input_content | "To concretely illustrate model performance degradation as docstring length increases, we create a dataset of synthetic problems assembled from 13 basic building blocks, each of which modifies an input string in a deterministic way." |
| Q90 | 10 | input_ontology | "We find that as the number of chained building blocks in the docstring increases, model performance decreases exponentially." |
| Q91 | 10 | input_ontology | "This behavior is uncharacteristic of a human programmer, who should be able to correctly implement a program for a chain of arbitrary length if they can do so for a chain of length two." |
| Q92 | 10 | input_ontology | "Further, just as text-conditional generative models in other modalities (Ramesh et al., 2021) have difficulty with binding attributes to objects, Codex can make mistakes binding operations to variables, especially when the number of operations and variables in the docstring is large." |
| Q93 | 10 | input_ontology | "With each additional component, pass rate drops by roughly a factor of 2-3." |
| Q94 | 10 | input_ontology | "Codex has the potential to be useful in a range of ways. For example, it could help onboard users to new codebases, reduce context switching for experienced coders, enable non-programmers to write specifications and have Codex draft implementations, and aid in education and exploration." |
| Q95 | 10 | output_ontology | "However, Codex also raises significant safety challenges, does not always produce code that is aligned with user intent," |
| Q96 | 11 | output_ontology | "To better understand some of the hazards of using Codex in a generative capacity, we conducted a hazard analysis focused on identifying risk factors (Leveson, 2019) with the potential to cause harm." |
| Q97 | 11 | input_ontology | "While some of our findings about the potential societal impacts of code generation systems were informed by work towards responsible deployment of the production-oriented Codex models (which descended from the research-oriented Codex models described in this paper), this section is not intended to provide a full account of any particular product's safety features." |
| Q98 | 11 | input_ontology | "Unless otherwise specified, we anchor our analysis in the specific properties of the models described in this paper." |
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
| Q112 | 13 | output_ontology | "Codex, like other large generative models, has an energy footprint from both training and inference (Schwartz et al., 2019; Bender et al., 2021; Patterson et al., 2021)." |
| Q113 | 13 | output_ontology | "The original training of GPT-3-12B consumed hundreds of petaflop/s-days of compute, while fine-tuning it to create Codex-12B consumed a similar amount of compute." |
| Q114 | 13 | output_ontology | "This training was performed on a platform (Azure) that purchases carbon credits and sources significant amounts of renewable energy, reducing its carbon footprint." |
| Q115 | 13 | output_content | "Our preliminary research also finds that Codex models rarely generate code that is identical to the contents of training data. Such occurrences were < 0.1% in a study examining the frequency of code generations that appear to match code snippets in the training data (Ziegler, 2021)." |
| Q116 | 13 | output_content | "In these rare instances, the generated code consisted of common expressions or conventions within the programming language that appeared over and over again in the training data." |
| Q117 | 13 | output_content | "We find that, to the extent the generated code appears identical to the training data, it is due to the predictive weightings in the model rather than retention and copying of specific code." |
| Q118 | 13 | output_form | "Generated code is also responsive and customized to the user's input, and the user retains complete control over editing and acceptance of the generated code." |
| Q119 | 13 | output_ontology | "In closing, given the above, models like Codex should be developed, used, and their capabilities explored carefully with an eye towards maximizing their positive social impacts and minimizing intentional or unintentional harms that their use might cause." |
| Q120 | 13 | output_ontology | "Careful documentation and user interface design, code review requirements, and/or content controls (e.g., filtering of outputs) may help to reduce harms associated with overreliance as well as offensive content or insecure code generation." |
| Q121 | 14 | output_form | "We used functional correctness to benchmark our models, and observed improvements on this metric with more sampling." |
| Q122 | 14 | output_form | "SPoC (Kulal et al., 2019) considered the problem of producing functionally correct code from pseudocode with a fixed budget of compilations, which is similar to our pass@k metric." |
| Q123 | 14 | output_ontology | "TransCoder (Lachaux et al., 2020) trained a system to translate between programming languages in an unsupervised manner, and also observed that functional correctness better captured the capabilities of their model than BLEU score." |
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
| Q135 | 15 | input_content | "We thank Sandhini Agarwal, Casey Chu, Jeffrey Ding, Peter Eckersley, Gillian Hadfield, Rich Harang, Jacob Jackson, Yunxin Jiao, Jade Leung, Andrew Lohn, Ryan Lowe, Thomas McGuire, Margaret Mitchell, Florentine Eloundou Nekoul, Cullen O'Keefe, Long Ouyang, Pranav Shyam, Irene Solaiman, Aravind Srinivas, Helen Toner, Ashish Vaswani, and Jeffrey Wu for helpful discussions and feedback on drafts of this work." |
| Q136 | 15 | input_content | "We are also grateful to the Acceleration and Supercomputing teams at OpenAI for their work on software and hardware infrastructure that this project used." |
| Q137 | 15 | input_content | "Finally, we thank GitHub for partnering to build GitHub Copilot and Microsoft Azure for supporting model training with infrastructure management." |
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
| Q169 | 27 | input_content | "One starting point is to more carefully curate the pre-training dataset to remove buggy or insecure code." |
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
| Q183 | 29 | output_ontology | "This is one key reason why code generated by the Codex models should be treated as untrusted by those using it for research or development until they have reviewed and verified its accuracy and fitness for purpose themselves." |
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
| Q198 | 31 | output_ontology | "We conducted experiments on Codex's ability to generate malicious code. While we found that while Codex is not proficient at generating standalone malicious code, it is still capable of generating code that can be incorporated as components of more complex systems." |
| Q199 | 31 | output_form | "We found that Codex did not perform well when compared even to rudimentary Static Application Security Testing (SAST) tools." |
| Q200 | 31 | output_form | "We encountered no cases in our testing where using a Codex model led to better or more efficient results than SAST tools." |
| Q201 | 31 | input_content | "However, Codex is generally unable to suggest specific versions of packages, as package versions are specified outside of the prompt context that Codex is aware of." |
| Q202 | 31 | output_content | "Through testing, we found that the likelihood of Codex suggesting a vulnerable or malicious package is low in aggregate." |
| Q203 | 31 | input_ontology | "We found that models trained on source code offered no advantages over conventional language models because the domains are fundamentally different." |
| Q204 | 32 | input_ontology | "To study this phenomenon, we asked Codex to suggest code that would call cryptographic libraries to generate cryptographic contexts, and then evaluated whether any of these outputs were clearly insecure." |
| Q205 | 32 | input_ontology | "When tested on a standard series of prompts asking the models to call functions to produce RSA keys or AES contexts, we find that Codex models of varying sizes frequently use clearly insecure configurations (See Figure 15)." |
| Q206 | 32 | input_content | "We used 5 prompts across different libraries for RSA and AES based on Sonar Source's Python vulnerability database, and generated ˜30k samples total." |
| Q207 | 32 | input_form | "We then removed some generated samples based on expected runtime errors, as different model sizes tend to vary in whether they produce code that runs." |
| Q208 | 32 | output_ontology | "RSA keys were considered improperly configured if they were shorter than 2048 bits." |
| Q209 | 32 | output_ontology | "AES contexts were considered improperly configured if they used the ECB cipher mode (see Menezes et al. (2018), p. 228)." |
| Q210 | 32 | output_ontology | "We chose these two tests to evaluate as targets because there is consensus among cryptography experts that these configurations generally should not be used, and these were reasonable to evaluate programmatically." |
| Q211 | 32 | output_content | "Interestingly, we do not see a robust model size trend (over 1 order of magnitude of parameters) in this data." |
| Q212 | 32 | output_ontology | "This suggests that insecure code production, at least in this case, is an alignment issue (see Appendix E): it is unclear if the models are improving with scale." |
| Q213 | 32 | output_ontology | "A larger study using the most common insecure code vulnerabilities may shed more light on this issue." |
| Q214 | 33 | output_ontology | "When asked to create encryption keys, Codex models select clearly insecure configuration parameters in a significant fraction of cases. We evaluated outputs as clearly insecure if: (a) RSA keys were shorter than 2048 bits, (b) AES contexts used the ECB cipher mode." |
| Q215 | 33 | output_ontology | "Because security standards change over time as capabilities improve, this is likely an underestimate of the true rate of improperly configured outputs." |
| Q216 | 33 | output_ontology | "Similarly, the produced samples that were not classified as clearly insecure are not necessarily secure, as our tests measure insecurity." |
| Q217 | 33 | input_content | "Additionally, one of the challenges of code generation stem from relying on the assumption that intent is captured sufficiently enough in comments and documentation to not compromise accuracy." |
| Q218 | 33 | input_ontology | "Thus, even if the model were perfectly accurate, we would not expect it to reduce the labor costs associated with writing code to zero." |
| Q219 | 33 | input_content | "There is unfortunately only limited research on the demographic distribution of Python users." |
| Q220 | 34 | input_content | "Codex imports substitutable packages at different rates based on patterns in its training data, which can have various possible implications." |
| Q221 | 34 | output_content | "Differential import rates by Codex might lead to subtle errors in cases where a certain import is ill-advised, increase robustness in cases where the alternative package imported by an individual would have been worse, and/or increase the dominance of an already-influential set of individuals and organizations in the software supply chain." |
| Q222 | 34 | input_content | "The scale of these effects for Codex may be relatively low if users mostly import packages they know how to use or have done outside research on, so they can double-check anything the model does." |
| Q223 | 34 | input_content | "Moreover, because packages are generally imported at the top of a file without any comments, the model has very little to go on in these cases, so users would most likely have to start typing out the name of the package they want to import rather than trusting the model to know they are starting a machine learning project and want to import either PyTorch or TensorFlow." |
| Q224 | 34 | output_form | "As one example, we looked at completions of the prompt: # import machine learning package import and found that over 100 completions of 100 tokens, 6 contained suggestions for TensorFlow and 3 for PyTorch, two libraries that are rough substitutes." |
| Q225 | 35 | input_ontology | "Most past studies of the impacts of code generation models consider performance on a closed set of tasks in a simulated environment (Xu et al., 2021)." |
| Q226 | 35 | output_ontology | "As the deployment of Codex and other near-term technologies proceeds, we may be able to conduct more robust experiments examining the impact of various strengths of models on real-world job performance, across teams and across firms." |
| Q227 | 35 | output_ontology | "Precise and accurate prediction of any impacts without user or market signal is difficult, but the potential implications on the long-run labor market and the possibility of disparate outcomes across groups warrant further exploration of these issues." |
| Q228 | 35 | output_ontology | "It may be possible to assess the relative likelihood of different scenarios by building a deeper understanding of Codex's capabilities across several code-related tasks or by studying the effects of precise deployment scenarios." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://lp.jetbrains.com/python-developers-survey-2024/ |
| WEB-2 | https://www.theregister.com/2025/08/19/python_survey/ |
| WEB-3 | https://www.secondtalent.com/resources/ide-statistics/ |
| WEB-4 | https://arxiv.org/abs/2211.11501 |
| WEB-5 | https://ds1000-code-gen.github.io/ |
| WEB-6 | https://www.evidentlyai.com/blog/llm-coding-benchmarks |
| WEB-7 | https://openai.com/index/introducing-swe-bench-verified/ |
| WEB-8 | https://arxiv.org/pdf/2412.05210 |
| WEB-9 | https://arxiv.org/pdf/2510.08697 |
| WEB-10 | https://proceedings.neurips.cc/paper_files/paper/2023/file/43e9d647ccd3e4b7b5baab53f0368686-Paper-Conference.pdf |
| WEB-11 | https://github.com/evalplus/evalplus |
| WEB-12 | https://www.alphaxiv.org/benchmarks/university-of-illinois-at-urbana-champaign/evalplus |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** openai/openai_humaneval
**Analysis date:** 2025-01-30
**Examples reviewed:** 40 from `test` split (164 total problems)
**Columns shown:** task_id, prompt, canonical_solution, test, entry_point
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | openai_humaneval | HumanEval/0 | pass/fail | `def has_close_elements(numbers: List[float], threshold: float) -> bool:` | Uses `from typing import List` type annotation — basic typing import only | IF |
| D2 | openai_humaneval | HumanEval/11 | pass/fail | `from typing import List` / `def string_xor(a: str, b: str) -> str:` | Primitive type annotations only; no complex generics, no dataclass, no TypeVar | IF |
| D3 | openai_humaneval | HumanEval/32 | pass/fail | `import math` / `def poly(xs: list, x: float):` | Only stdlib `math` import; no third-party library | IC |
| D4 | openai_humaneval | HumanEval/37 | pass/fail | `import math` / `def find_zero(xs: list):` | Bisection method problem; purely algorithmic, self-contained | IC |
| D5 | openai_humaneval | HumanEval/38 | pass/fail | `def encode_cyclic(s: str):` / `def decode_cyclic(s: str):` | Self-contained string cycling; no external dependencies | IC |
| D6 | openai_humaneval | HumanEval/34 | pass/fail | `from typing import List` / `def below_zero(operations: List[int]) -> bool:` | Bank-account balance; no imports beyond typing | IC |
| D7 | openai_humaneval | HumanEval/17 | pass/fail | `from typing import List` / `def parse_music(music_string: str) -> List[int]:` | String-parsing problem with docstring examples; self-contained | IF |
| D8 | openai_humaneval | HumanEval/61 | pass/fail | `def correct_bracketing(brackets: str):` / `""" brackets is a string of "(" and ")". return True if every opening bracket has a corresponding closing bracket.` | Classic bracket-matching algorithmic problem | IO |
| D9 | openai_humaneval | HumanEval/130 | pass/fail | `def tri(n):` / `"""Everyone knows Fibonacci sequence, it was studied deeply by mathematicians in the last couple centuries. However, what people don't know is Tribonacci sequence.` | Custom sequence definition; pure math recursion | IO |
| D10 | openai_humaneval | HumanEval/124 | pass/fail | `def valid_date(date):` / `"""You have to write a function which validates a given date string and returns True if the date is valid otherwise False.` | Date validation; no `datetime` library used — reinvents wheel | OO |
| D11 | openai_humaneval | HumanEval/105 | pass/fail | `assert True, "This prints if this assert fails 1 (good for debugging!)"` / `assert True, "This prints if this assert fails 2 (also good for debugging!)"` | Filler `assert True` statements provide no coverage | OC |
| D12 | openai_humaneval | HumanEval/88 | pass/fail | `assert True, "This prints if this assert fails 1 (good for debugging!)"` / `assert True, "This prints if this assert fails 2 (also good for debugging!)"` | Additional filler assert placeholders in test suite | OC |
| D13 | openai_humaneval | HumanEval/145 | pass/fail | `assert True, "This prints if this assert fails 2 (also good for debugging!)"` | Filler assert with no functional test content | OC |
| D14 | openai_humaneval | HumanEval/121 | pass/fail | `# Check some edge cases that are easy to work out by hand.` (no assertions follow) | Section header with no edge-case assertions after it | OC |
| D15 | openai_humaneval | HumanEval/128 | pass/fail | `assert True, "This prints if this assert fails 1 (good for debugging!)"` / `assert True, "This prints if this assert fails 2 (also good for debugging!)"` | Two filler asserts bookend functional tests | OC |
| D16 | openai_humaneval | HumanEval/104 | pass/fail | `assert True` (edge cases section) | Edge-case section ends with bare `assert True` | OC |
| D17 | openai_humaneval | HumanEval/22 | pass/fail | `def will_it_fly(q,w):` / `assert candidate([1, 2, 3], 6) is False` / `assert candidate([5], 5) is True` | Only 6 functional assertions; thin edge-case coverage | OC |
| D18 | openai_humaneval | HumanEval/20 | pass/fail | `def get_odd_collatz(n):` / `assert candidate(14) == [1, 5, 7, 11, 13, 17]` / `assert candidate(1) == [1]` | Only 4 test cases for an infinite-sequence function | OC |
| D19 | openai_humaneval | HumanEval/109 | pass/fail | `def move_one_ball(arr):` / `assert candidate([3, 4, 5, 1, 2])==True` / `assert candidate([])==True` | 5 total assertions for rotation-sort problem | OC |
| D20 | openai_humaneval | HumanEval/137 | pass/fail | `def compare_one(a, b):` / `Note: If a real number is represented as a string, the floating point might be . or ,` | Locale-aware comma-decimal: tests this but only with specific values | OC |
| D21 | openai_humaneval | HumanEval/124 | pass/fail | `if month in [1,3,5,7,8,10,12] and day < 1 or day > 31: return False` | Canonical solution has a precedence bug (`and` before `or`); test suite passes it anyway | OC |
| D22 | openai_humaneval | HumanEval/105 | pass/fail | `canonical_solution: sorted_arr = sorted(arr, reverse=True)` | Sorts descending instead of filtering 1–9 then reversing — functionally diverges from docstring | OC |
| D23 | openai_humaneval | HumanEval/38 | pass/fail | `def check(candidate): from random import randint, choice import string` | Randomized test using fixed seed (none stated) — non-determinism edge case | OC |
| D24 | openai_humaneval | HumanEval/61 | pass/fail | `assert not candidate("()()(()())())(()")` / `assert not candidate("()()(()())()))()")` | 12 assertions — one of the better-covered problems | OC |
| D25 | openai_humaneval | HumanEval/8 | pass/fail | `def string_xor(a: str, b: str) -> str:` / `assert candidate('111000', '101010') == '010010'` | Only 3 test cases for XOR function | OC |
| D26 | openai_humaneval | HumanEval/67 | pass/fail | `def fruit_distribution(s,n):` / `"""In this task, you will be given a string that represents a number of apples and oranges that are distributed in a basket of fruit this basket contains apples, oranges, and mango fruits.` | Narrative/word-problem style docstring — not a professional API docstring | IC |
| D27 | openai_humaneval | HumanEval/30 | pass/fail | `def eat(number, need, remaining):` / `"""You're a hungry rabbit, and you already have eaten a certain number of carrots` | Game/puzzle narrative docstring; not API-style | IC |
| D28 | openai_humaneval | HumanEval/9 | pass/fail | `def tri(n):` / `"""Everyone knows Fibonacci sequence, it was studied deeply by mathematicians in the last couple centuries.` | Narrative/essay-style docstring opener | IC |
| D29 | openai_humaneval | HumanEval/37 | pass/fail | `def poly(xs: list, x: float):` / `find_zero returns only only zero point, even if there are many.` | Two-function prompt: model must generate body of `find_zero` given helper `poly` already defined | IF |
| D30 | openai_humaneval | HumanEval/21 | pass/fail | `def encode_cyclic(s: str): ... def decode_cyclic(s: str):` | Two-function prompt with helper already provided — multi-function context | IF |
| D31 | openai_humaneval | HumanEval/19 | pass/fail | `from typing import List` / `def sort_numbers(numbers: str) -> str:` | Uses `from typing import List` in import but function signature uses `str` → `str`; basic typing only | IF |
| D32 | openai_humaneval | HumanEval/27 | pass/fail | `def is_simple_power(x, n):` / `"""Your task is to write a function that returns true if a number x is a simple power of n` | No type annotations at all; untyped signature | IF |
| D33 | openai_humaneval | HumanEval/105 | pass/fail | `canonical_solution: dic = {1: "One", 2: "Two", ... 9: "Nine"}` | Uses bare `except:` clause in canonical solution — non-idiomatic Python | OO |
| D34 | openai_humaneval | HumanEval/37 | pass/fail | `assert math.fabs(poly(coeffs, solution)) < 1e-4` | Test uses random with seeded RNG (`random.Random(42)`) — 100-iteration fuzz test | OF |
| D35 | openai_humaneval | HumanEval/124 | pass/fail | `assert candidate('2003-04-12') == False` | Tests YYYY-MM-DD format as invalid — only MM-DD-YYYY accepted | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Precise input/output form alignment with IDE deployment
- **Dimension(s):** IF
- **Observation:** Every sampled problem is structured as a Python function signature with an English docstring, and the model must generate the function body. This matches the inline IDE completion trigger exactly. Several problems also include `from typing import List` or basic type annotations, confirming the text-in / code-out format.
- **Deployment relevance:** The deployment triggers when a user writes a function signature or docstring; the benchmark evaluates exactly this pairing. No modality gap, no script mismatch, no infrastructure constraint.
- **Datapoint citations:**
  - [D1] Example HumanEval/0 (openai_humaneval, split=test, label=pass/fail): `def has_close_elements(numbers: List[float], threshold: float) -> bool:` — Signature + English docstring format matches IDE completion trigger exactly.
  - [D7] Example HumanEval/17 (openai_humaneval, split=test, label=pass/fail): `def parse_music(music_string: str) -> List[int]:` — Docstring with examples in `>>>` format mirrors real engineering docstrings.
  - [D29] Example HumanEval/32 (openai_humaneval, split=test, label=pass/fail): `def poly(xs: list, x: float): ... def find_zero(xs: list):` — Two-function prompt shows benchmark handles multi-function context, present in real files.

#### Strength 2: Automated, objective unit-test correctness signal
- **Dimension(s):** OO, OF
- **Observation:** All 40 sampled problems use executable `assert` statements against concrete input/output pairs as the sole correctness criterion. The evaluation is fully automated and reviewer-independent, matching the deployment's own automated unit-test execution pipeline.
- **Deployment relevance:** The deployment evaluates completions by running unit tests; the benchmark scores completions the same way. No human annotation step, no string-match bias.
- **Datapoint citations:**
  - [D8] Example HumanEval/61 (openai_humaneval, split=test, label=pass/fail): `assert candidate("()")` / `assert not candidate("((()())))")` — 12 concrete boolean assertions covering true and false cases.
  - [D34] Example HumanEval/32 (openai_humaneval, split=test, label=pass/fail): `assert math.fabs(poly(coeffs, solution)) < 1e-4` — Numeric tolerance check using randomized inputs (100 iterations, seeded RNG).

#### Strength 3: Problem taxonomy covers core algorithmic and string-manipulation correctness
- **Dimension(s):** IO
- **Observation:** The 40 sampled problems span bracket matching, sorting, string XOR, Collatz sequences, polynomial root-finding, date validation, cyclic pattern checking, and digit-manipulation — covering the "language comprehension, reasoning, algorithms, simple mathematics" taxonomy documented in the paper. These categories correspond to real lower-complexity completions that engineers write.
- **Deployment relevance:** For an initial evaluation focused on general-purpose algorithmic correctness, the breadth within this category is adequate as a lower-bound baseline.
- **Datapoint citations:**
  - [D8] Example HumanEval/61 (openai_humaneval, split=test, label=pass/fail): `def correct_bracketing(brackets: str):` — Stack-based bracket matching; canonical algorithmic problem.
  - [D9] Example HumanEval/130 (openai_humaneval, split=test, label=pass/fail): `def tri(n):` — Custom recurrence; tests mathematical reasoning.
  - [D10] Example HumanEval/124 (openai_humaneval, split=test, label=pass/fail): `def valid_date(date):` — Validates date strings; string-parsing + logic.

#### Strength 4: Zero dependency on external infrastructure or third-party state
- **Dimension(s):** IF, IC
- **Observation:** Every sampled problem is entirely self-contained — the only imports observed across 40 examples are `from typing import List`, `import math`, and `from random import randint, choice` (all stdlib). No network calls, database connections, or library API state required.
- **Deployment relevance:** This makes the benchmark runnable in any sandboxed Python environment without package installation, which matches the deployment's automated evaluation pipeline and eliminates environment-dependent flakiness.
- **Datapoint citations:**
  - [D3] Example HumanEval/32 (openai_humaneval, split=test, label=pass/fail): `import math` — Only stdlib import; no pip dependencies.
  - [D5] Example HumanEval/38 (openai_humaneval, split=test, label=pass/fail): `def decode_cyclic(s: str):` — No import at all; pure Python.

#### Strength 5: Hand-authored problems reduce data contamination risk
- **Dimension(s):** IC
- **Observation:** No problem in the sample appears to be copied from a standard competitive-programming corpus or textbook. Problem framings are original (hungry rabbit, flying objects, Tribonacci variant, cyclic encoding), consistent with the paper's claim that problems were hand-written to avoid GitHub training data overlap.
- **Deployment relevance:** For a deployment evaluating models trained on public code corpora, contamination-free test items are necessary for the score to reflect generalization rather than memorization.
- **Datapoint citations:**
  - [D27] Example HumanEval/159 (openai_humaneval, split=test, label=pass/fail): `"""You're a hungry rabbit, and you already have eaten a certain number of carrots` — Idiosyncratic narrative framing unlikely to appear verbatim in training data.
  - [D26] Example HumanEval/67 (openai_humaneval, split=test, label=pass/fail): `"""In this task, you will be given a string that represents a number of apples and oranges that are distributed in a basket` — Original problem framing.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: No third-party library problems — benchmark systematically misrepresents production input difficulty
- **Dimension(s):** IC
- **Observation:** Across all 40 sampled examples, zero problems involve third-party libraries. The only non-trivial imports are `import math` (stdlib) and `from typing import List` (stdlib). No pandas, numpy, requests, SQLAlchemy, FastAPI, Flask, or any pip-installable package appears. Every problem is self-contained pure Python.
- **Deployment relevance:** The user confirmed that "the majority of real completions reference imports already in the file, internal helper modules, or third-party libraries." This benchmark therefore measures a systematically easier problem distribution than the deployment sees. A model that scores well on HumanEval may still fail on the majority of production completions, making HumanEval scores a potentially misleading lower-bound indicator of real-world capability.
- **Datapoint citations:**
  - [D3] Example HumanEval/32 (openai_humaneval, split=test, label=pass/fail): `import math` / `def poly(xs: list, x: float):` — Only stdlib import across all 40 examples reviewed.
  - [D6] Example HumanEval/34 (openai_humaneval, split=test, label=pass/fail): `from typing import List` / `def below_zero(operations: List[int]) -> bool:` — Typing-only import; no domain library.
  - [D5] Example HumanEval/38 (openai_humaneval, split=test, label=pass/fail): `def decode_cyclic(s: str):` — No imports at all.

#### Concern 2: Binary pass/fail discards idiomaticity and efficiency — confirmed user-relevant quality dimension
- **Dimension(s):** OO
- **Observation:** The canonical solutions in the sample reveal non-idiomatic patterns that would pass all tests but that experienced Python engineers would reject. HumanEval/105's canonical solution uses a bare `except:` clause (broad exception suppression, considered anti-idiomatic per PEP 8 and pylint). HumanEval/124's canonical solution implements date validation with operator precedence bugs that the thin test suite does not catch. Two passing solutions — one using `pandas.to_datetime()` with proper error handling and one using this manual implementation — would receive identical scores.
- **Deployment relevance:** The user explicitly confirmed that "users will reject non-idiomatic completions even when functionally correct" and that "two passing solutions are considered substantively different in quality by end users." The benchmark's binary score cannot distinguish these cases.
- **Datapoint citations:**
  - [D33] Example HumanEval/105 (openai_humaneval, split=test, label=pass/fail): `canonical_solution: try: new_arr.append(dic[var]) except: pass` — Bare `except:` is broadly discouraged in professional Python; a model generating this would pass but be rejected by linters and code review.
  - [D10] Example HumanEval/124 (openai_humaneval, split=test, label=pass/fail): `if month in [1,3,5,7,8,10,12] and day < 1 or day > 31: return False` — Operator precedence error in canonical solution that the test suite does not surface.

#### MAJOR

#### Concern 3: Widespread filler `assert True` statements reduce test-suite coverage
- **Dimension(s):** OC
- **Observation:** Across the 40 sampled problems, at least 8 test suites contain `assert True` statements — either as stand-alone assertions that trivially pass regardless of model output, or as section headers for "edge cases" that are never followed by actual assertions. These occupy slots in the test suites that contribute nothing to coverage but count toward the visual impression of thoroughness.
- **Deployment relevance:** This directly corroborates the EvalPlus finding (NeurIPS 2023) that HumanEval's average 7.7 tests per problem over-credits models — scores drop 19–29% when the test suite is expanded 80×. For the deployment's primary correctness signal, these filler statements mean that some incorrect solutions may pass all "tests" because the tests simply do not exercise the relevant edge cases.
- **Datapoint citations:**
  - [D11] Example HumanEval/105 (openai_humaneval, split=test, label=pass/fail): `assert True, "This prints if this assert fails 1 (good for debugging!)"` — Filler assertion at start of edge-case section provides zero coverage.
  - [D13] Example HumanEval/145 (openai_humaneval, split=test, label=pass/fail): `assert True, "This prints if this assert fails 2 (also good for debugging!)"` — Filler at end; edge cases section contains only this.
  - [D14] Example HumanEval/121 (openai_humaneval, split=test, label=pass/fail): `# Check some edge cases that are easy to work out by hand.` — Section header with no following assertions.
  - [D16] Example HumanEval/104 (openai_humaneval, split=test, label=pass/fail): `assert True` — Bare filler in edge-case section.

#### Concern 4: Several individual test suites have very few functional assertions
- **Dimension(s):** OC
- **Observation:** A number of problems have extremely thin test coverage in terms of actual functional assertions. HumanEval/72 has 6 total assertions (excluding filler). HumanEval/123 has 4. HumanEval/109 has 5. HumanEval/11 (string_xor) has 3. This is well below the average of 7.7 documented in the paper, suggesting high variance in test quality across problems.
- **Deployment relevance:** Thin per-problem test suites mean that a model generating an incorrect solution can still pass if the incorrect solution happens to satisfy the small set of provided inputs. This inflates pass@k scores relative to true functional correctness, which the deployment relies on as its primary evaluation signal.
- **Datapoint citations:**
  - [D25] Example HumanEval/11 (openai_humaneval, split=test, label=pass/fail): `assert candidate('111000', '101010') == '010010'` / `assert candidate('1', '1') == '0'` / `assert candidate('0101', '0000') == '0101'` — Only 3 test cases; does not cover equal-length edge cases or empty strings.
  - [D18] Example HumanEval/123 (openai_humaneval, split=test, label=pass/fail): `assert candidate(14) == [1, 5, 7, 11, 13, 17]` / `assert candidate(1) == [1]` — 4 test cases for an infinite-sequence function; large n behavior untested.
  - [D17] Example HumanEval/72 (openai_humaneval, split=test, label=pass/fail): `assert candidate([3, 2, 3], 9) is True` — 6 assertions; empty list, large palindrome, weight exactly equal to sum not tested.

#### Concern 5: Canonical solution contains observable correctness bugs
- **Dimension(s):** OC
- **Observation:** HumanEval/124 (`valid_date`) has a canonical solution with an operator precedence bug: `if month in [1,3,5,7,8,10,12] and day < 1 or day > 31` evaluates as `(month in [...] and day < 1) or (day > 31)`. This means the function incorrectly returns `False` for valid dates when `day > 31` regardless of month. The test suite does not surface this because no test checks a month-in-list case with day exactly at the boundary in a way that exposes the bug. This is consistent with EvalPlus's finding that 11% of original HumanEval ground-truth solutions contained errors.
- **Deployment relevance:** If the deployment uses HumanEval ground-truth solutions as reference implementations or for data quality checks, this introduces noise into the evaluation signal. More broadly, it confirms that the benchmark's correctness criteria are not fully reliable without augmented test suites.
- **Datapoint citations:**
  - [D21] Example HumanEval/124 (openai_humaneval, split=test, label=pass/fail): `if month in [1,3,5,7,8,10,12] and day < 1 or day > 31: return False` — Operator precedence bug in canonical solution; passes the existing test suite because no test specifically targets this path.
  - [D35] Example HumanEval/124 (openai_humaneval, split=test, label=pass/fail): `assert candidate('2003-04-12') == False` — Tests an unrelated rejection; does not probe the buggy month+day condition.

#### Concern 6: No async/await or complex type annotation problems present
- **Dimension(s):** IO, IF
- **Observation:** Across all 40 sampled problems, all function signatures are synchronous. The most complex type annotations observed are `List[float]`, `List[int]`, and `List[str]` — all from the legacy `typing` module. No `async def`, `await`, `asyncio`, `Optional`, `Union`, `TypeVar`, `Protocol`, `dataclass`, `TypedDict`, or `ParamSpec` appears. No PEP 604 (`X | Y`) union syntax appears.
- **Deployment relevance:** The user confirmed that "async I/O and heavily type-annotated code" constitute a large fraction of professional Python completions. The benchmark offers no signal about model performance on these patterns, which are prevalent in modern Python 3.10–3.13 codebases (the dominant versions per the PSF/JetBrains 2024 survey). This is a confirmed gap with no benchmark in the field currently filling it.
- **Datapoint citations:**
  - [D1] Example HumanEval/0 (openai_humaneval, split=test, label=pass/fail): `def has_close_elements(numbers: List[float], threshold: float) -> bool:` — `List[float]` is the most complex annotation observed; no async, no Union, no dataclass.
  - [D32] Example HumanEval/76 (openai_humaneval, split=test, label=pass/fail): `def is_simple_power(x, n):` — Completely untyped signature; no annotations at all.
  - [D2] Example HumanEval/11 (openai_humaneval, split=test, label=pass/fail): `def string_xor(a: str, b: str) -> str:` — Simple primitive annotation only.

#### Concern 7: Docstring register mismatches professional API documentation conventions
- **Dimension(s):** IC
- **Observation:** Several problems use narrative or puzzle-framing docstrings that do not resemble how professional engineers write docstrings in production code. "You're a hungry rabbit," "Everyone knows Fibonacci sequence," and "In this task, you will be given" are pedagogical or interview-competition registers, not the terse, parameter-documenting style (`Args:`, `Returns:`, `Raises:`) typical of professional Python codebases.
- **Deployment relevance:** IDE completion is triggered by real engineering docstrings. If models are benchmarked primarily on puzzle-narrative docstrings, there is some construct-irrelevant variance: the model's ability to parse competition-style problem statements may not transfer directly to parsing professional API docstrings with `Args:`/`Returns:` sections.
- **Datapoint citations:**
  - [D27] Example HumanEval/159 (openai_humaneval, split=test, label=pass/fail): `"""You're a hungry rabbit, and you already have eaten a certain number of carrots, but now you need to eat more carrots to complete the day's meals.` — Narrative game register; not a professional API docstring.
  - [D28] Example HumanEval/130 (openai_humaneval, split=test, label=pass/fail): `"""Everyone knows Fibonacci sequence, it was studied deeply by mathematicians in the last couple centuries. However, what people don't know is Tribonacci sequence.` — Essay-style opener atypical of engineering documentation.
  - [D26] Example HumanEval/67 (openai_humaneval, split=test, label=pass/fail): `"""In this task, you will be given a string that represents a number of apples and oranges` — "In this task" framing is interview/competition register.

#### MINOR

#### Concern 8: Date validation problem encodes US-specific MM-DD-YYYY date format
- **Dimension(s):** IC
- **Observation:** HumanEval/124 specifies that "the date should be in the format: mm-dd-yyyy" and tests that `'2003-04-12'` (ISO 8601, YYYY-MM-DD) is `False`. This hardcodes a specifically US-preferred date format as the correct one.
- **Deployment relevance:** The deployment serves US-based engineers, so this does not create a validity problem for the primary population. However, it is worth noting for international extensions of this evaluation.
- **Datapoint citations:**
  - [D10] Example HumanEval/124 (openai_humaneval, split=test, label=pass/fail): `"""The date should be in the format: mm-dd-yyyy` — US date format hardcoded as correct; ISO 8601 tested as invalid.
  - [D35] Example HumanEval/124 (openai_humaneval, split=test, label=pass/fail): `assert candidate('2003-04-12') == False` — ISO 8601 format explicitly rejected.

#### Concern 9: Some canonical solutions use non-idiomatic Python patterns
- **Dimension(s):** OO
- **Observation:** Beyond the `except:` case noted above, HumanEval/105's canonical solution applies a `sorted(..., reverse=True)` followed by dict lookup instead of filtering 1–9 values first and then reversing — producing correct output but obscuring the algorithm's intent. HumanEval/75's canonical solution uses a triple nested loop to factor `a` into three primes, which is O(n³) and non-idiomatic.
- **Deployment relevance:** Since the benchmark treats any passing solution as equivalent to the canonical solution, a model that generates the idiomatic, efficient solution receives the same score as one that generates the canonical non-idiomatic one. This is a known limitation of binary pass@k that the user confirmed matters.
- **Datapoint citations:**
  - [D22] Example HumanEval/105 (openai_humaneval, split=test, label=pass/fail): `canonical_solution: sorted_arr = sorted(arr, reverse=True)` — Sorts all input descending (including out-of-range values) before filtering; obscures the intended filter-then-reverse algorithm.
  - [D33] Example HumanEval/105 (openai_humaneval, split=test, label=pass/fail): `except: pass` — Bare except suppresses all exceptions including `KeyError` from invalid keys.

---

### Content Coverage Summary

The 40 sampled problems span: bracket/parenthesis matching, sorting with custom keys, string XOR and string manipulation, mathematical sequences (Collatz, Tribonacci, polynomial root-finding), list filtering, date validation, prime factorization, cyclic string encoding/decoding, digit-sum operations, palindrome checking, interval intersection, and dictionary key validation. All problems are standalone function synthesis tasks with English docstrings and Python signatures.

The register of docstrings is mixed: some resemble engineering API documentation (brief, example-driven, `>>>` notation) while others use narrative/puzzle framing more typical of competitive programming problem statements. Type annotations are minimal — primarily `List[T]` from the legacy `typing` module — with no modern Python typing constructs (no `TypeVar`, `Protocol`, `dataclass`, `ParamSpec`, `X | Y` union syntax). All function signatures are synchronous. No third-party libraries appear in any of the 40 problems reviewed. Test suites vary substantially in quality: some problems have 12+ targeted assertions covering true/false cases and edge inputs, while others contain as few as 3 functional assertions padded with `assert True` filler. One canonical solution (HumanEval/124) contains an observable operator precedence bug that the test suite does not catch.

---

### Limitations

1. **Sample size:** 40 of 164 problems were reviewed (24%). The observed patterns — especially regarding test-suite quality variance and canonical solution bugs — may not generalize uniformly to all 164 problems. EvalPlus's finding that 11% of ground-truth solutions contain errors (from full-benchmark analysis) suggests the sample rate here is conservative.

2. **Test suite coverage is not inspectable via execution:** This analysis identified structural weaknesses in test suites (filler `assert True`, low assertion counts) but cannot determine false-negative rates without running test suites against known-incorrect solutions. EvalPlus (NeurIPS 2023) provides this data externally, but it cannot be verified from the raw dataset alone.

3. **Canonical solutions may not represent the full correctness space:** The analysis can observe whether canonical solutions are non-idiomatic or contain apparent bugs, but cannot enumerate all valid solutions a model might generate and whether they would correctly pass/fail.

4. **No execution environment available:** Whether Python version (3.8 vs. 3.12) affects pass/fail outcomes for any individual problem cannot be determined without running the test suite. The `tri()` canonical solution (HumanEval/130) returns floats from integer division (`i / 2 + 1`) — this behavior is correct in Python 3 but its interaction with test assertions like `assert candidate(3) == [1, 3, 2.0, 8.0]` is Python-3-specific.

5. **Idiomaticity is not quantitatively assessable from this sample:** Observations about non-idiomatic canonical solutions reflect domain judgment; a formal automated measurement (pylint, flake8, cyclomatic complexity) would require executing linters against the canonical solutions, which was not done here.

