## Deployment Context

We are a US enterprise software company evaluating whether an LLM can generate full-stack web application scaffolding from high-level requirements documents. Given a requirements spec, the system should produce database schemas, API route definitions, frontend component stubs, and deployment configurations. Our users are American software architects. We need to evaluate the LLM's code generation capabilities for this multi-layer task.

# Validity Analysis: humaneval
**Target context:** US Enterprise Software Architects — Full-Stack Scaffolding Generation
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content | 2 | Significant gaps | high |
| Input Form | 1 | Serious concern | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ✓ | 2 | Significant gaps | high |
| **Average** | **1.3** | | |

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

HumanEval is a foundational benchmark for isolated Python function synthesis evaluated by unit-test pass/fail. For the deployment use case — multi-page PRD-to-multi-file-scaffolding generation graded by an internal architecture rubric — the benchmark is fundamentally misaligned across all four user-flagged HIGH-priority dimensions (IO, IC, IF, OO, OC) and substantially misaligned on OF. Five of six dimensions score 1–2. The only points of genuine contact are: (a) US English natural-language register, (b) typed Python function signatures, (c) text-in/code-out modality, and (d) a usable sandboxed-execution infrastructure that can serve as a lower-bound check for Python utility sub-components inside larger scaffolding outputs. The paper itself acknowledges most of the relevant limitations — long-specification handling [Q88], absence of qualitative architectural metrics [Q86, Q149], lack of automatic docstring evaluation [Q78], and distribution mismatch with broader GitHub code [Q48]. Web research confirms dedicated benchmarks (DevBench, SWE-bench++, IaC-Eval, DPIaC-Eval, Multi-IaC-Eval, FrontendBench, LongCodeBench, Prometheus 2) now exist that cover most of the validity gaps individually, though none combines all four artifact layers required here.

## Practical Guidance

### What This Benchmark Measures

HumanEval measures a model's ability to synthesize a single self-contained Python function from a short docstring and have it pass a small set of unit tests on algorithmic/mathematical problems. For the deployment, this corresponds to at most one narrow sub-component of the broader scaffolding task: isolated Python utility functions that might appear inside FastAPI route handlers or SQLAlchemy model methods. The strongest dimension is Output Form (modality match) and the weakest are Input Ontology, Output Ontology, and Output Content (each scoring 1).

### Construct Depth

The benchmark probes functional correctness at a behavioral-contract level only. It does not probe: (a) framework-idiom adherence (FastAPI dependency injection, SQLAlchemy declarative models, Pydantic v2 validation, Spring Boot annotations), (b) cross-file/cross-language coherence, (c) architectural-convention adherence against an internal style guide, (d) long-context document parsing, or (e) infrastructure-as-code generation. The paper explicitly defers richer specification attributes (variable interdependencies, temporal reasoning, concurrency) to future work [Q149]. Quantitative ceilings reported in the literature for the layers HumanEval omits are sobering: <20% pass@1 on compositional IaC [WEB-4], ~50% on simplest IaC scenarios with 42.7% deployment-failure rate among syntactically correct templates [WEB-5], and 29%→3% degradation as coding-task context length grows [WEB-3].

### What Else You Need

Comprehensive supplementation is required: (1) DevBench [WEB-12] or SWE-bench++ [WEB-9] for multi-stage / multi-language repository-level coverage; (2) IaC-Eval [WEB-4] + DPIaC-Eval [WEB-5] + Multi-IaC-Eval [WEB-6] for the Dockerfile/Kubernetes/Terraform deployment-config layer; (3) FrontendBench [WEB-13] for React/Angular component-stub evaluation; (4) LongCodeBench [WEB-3] or LoCoBench [WEB-18] for long-context input form; (5) Prometheus 2 [WEB-14] as a rubric-judge framework with the org's architecture guide encoded as structured criteria, calibrated against a small human-annotated gold set per TRACE [WEB-16]; (6) a custom in-house harness for multi-file entity-name coherence (schema ↔ API model ↔ frontend prop types) since no public benchmark explicitly scores this. Framework-specific evaluation for FastAPI/SQLAlchemy/Pydantic/Spring Boot remains a confirmed gap (search gap 4 NOT FOUND) and requires custom benchmark construction using org-internal PRDs and the architecture guide as ground truth.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
HumanEval's task taxonomy is confined entirely to standalone Python function synthesis assessing 'language comprehension, reasoning, algorithms, and simple mathematics' [Q22]. The deployment requires four structurally distinct artifact categories (DB schema, API routes, frontend stubs, IaC) that are wholly absent from the benchmark. The paper itself acknowledges that GitHub code includes 'class implementations, configuration files, scripts, and even files used to store data' that are underrepresented [Q48], and that current synthesis capabilities only address 'tightly specified, constrained problem instances' [Q151]. Empirical sampling confirms zero examples of SQL, ORM, REST, frontend, or IaC content across the dataset.

**Strengths:**
- The benchmark does test isolated Python function synthesis with typed signatures, which corresponds to one narrow sub-component (utility helper functions inside FastAPI/SQLAlchemy code) of the broader scaffolding task [Q22, DATASET-D2].

**Checklist:**

- **IO-1**: Required categories for the deployment: (a) SQL DDL / SQLAlchemy ORM model generation, (b) FastAPI/Spring Boot route handlers with Pydantic/DTO schemas, (c) React/Next.js/Angular component stubs in TypeScript, (d) Dockerfile/Kubernetes/Terraform IaC. None of these are represented in the benchmark's taxonomy. — _Sources: DATASET-D1, DATASET-D8_
- **IO-2**: Yes — the benchmark omits all four deployment-required categories. The paper explicitly scopes itself to 'producing functionally correct code bodies from natural language docstrings' [Q130] and characterizes coverage as algorithms/math [Q22]. Empirical sampling found 0/40 examples covering any required category. — _Sources: Q22, Q130, DATASET-D1, DATASET-D3_
- **IO-3**: Yes — competitive-programming puzzle problems (Tribonacci sequences, palindromic 'flying objects', polynomial root finding) consume the entire taxonomy without bearing on enterprise scaffolding. Appendix-D extensions to bias [Q185-Q188] and cryptographic API misuse [Q204-Q205] are partially relevant (security patterns) but still confined to single-function Python. — _Sources: Q22, DATASET-D22, DATASET-D3_
- **IO-4**: Gaps that harm content validity: complete absence of multi-artifact scaffolding, no framework-idiom categories, no IaC categories, no cross-layer entity-modeling tasks. DevBench [WEB-12] is the nearest available analog and itself reveals LLMs fail repository-level multi-stage tasks. — _Sources: Q48, Q151, WEB-12, WEB-13_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'Programming tasks in the HumanEval dataset assess language comprehension, reasoning, algorithms, and simple mathematics.' (p.4)
- [Q46] 'Most of the APPS tests problems are not formulated as single-function synthesis tasks, but rather as full-program synthesis...in contrast to the main Codex training data.' (p.6)
- [Q48] 'Python code found on GitHub contains class implementations, configuration files, scripts, and even files used to store data. This code is seemingly unrelated to synthesizing functions from docstrings, and we hypothesize that the distribution mismatch reduces HumanEval performance.' (p.7)
- [Q130] 'We investigated whether it was possible to train large language models to produce functionally correct code bodies from natural language docstrings.' (p.14)
- [Q151] 'The current capabilities of synthesis methodologies are only able to tackle tightly specified, constrained problem instances or narrow tasks.' (p.25)

*Web sources:*
- [WEB-12] DevBench evaluates full software-development lifecycle across four languages and is the nearest multi-stage analog; current LLMs fail its challenges
- [WEB-13] FrontendBench targets front-end code generation — a category absent from HumanEval

*Dataset analysis:*
- DATASET-D1: HumanEval/61 bracket-matching algorithm — no enterprise artifact
- DATASET-D3: HumanEval/130 Tribonacci sequence — competitive-programming math
- DATASET-D8: HumanEval/3 bank-balance simulation is closest to a 'business' domain yet still pure algorithm with no ORM/API content
- DATASET-D22: HumanEval/72 whimsical 'will it fly' puzzle illustrates the puzzle register

</details>

**Information gaps:**
- Whether the 124 unsampled problems contain any framework-idiom content (highly unlikely given paper documentation, but not exhaustively confirmed).

**Requires expert verification:**
- Confirmation from the organization's architects that all four artifact layers are required, and that the rubric scope cannot be reduced to a single layer where HumanEval has more applicability.

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Content is hand-written algorithmic/interview-style problems [Q14, Q19, Q131] sourced from no enterprise-development context. Training data is GitHub Python at large [Q23, Q25], and the Codex-S fine-tune adds competitive-programming and CI-traced functions [Q52, Q55] — none of which encode FastAPI/SQLAlchemy/Pydantic/Spring Boot idioms, business data models, compliance constraints, or SLA requirements. The natural language *register* is US English [DATASET-D7] which matches the deployment, and typed Python signatures appear [DATASET-D2, DATASET-D6] — narrow points of contact. The security probe content [Q206] is operationally grounded but still single-function. No content addresses the deployment's PRD-embedded business context, non-functional requirements, or convention encoding.

**Strengths:**
- All docstrings are in standard US English, matching the deployment's exclusive working language [DATASET-D7].
- Some problems use modern typed Python signatures (List[float], etc.) consistent with Pydantic/FastAPI typing expectations [DATASET-D2, DATASET-D6].
- Security probe content [Q206] adds a small amount of operational vulnerability-pattern content relevant to enterprise security review.

**Checklist:**

- **IC-1**: The deployment requires enterprise-software cultural knowledge (FastAPI conventions, Spring Boot annotations, Kubernetes manifest structure, AWS IaC patterns), not regional/dialectal cultural knowledge in the traditional sense. The benchmark's content does not encode any of this enterprise-stack knowledge [Q22, DATASET-D4]. — _Sources: Q22, DATASET-D4_
- **IC-2**: The puzzle/whimsical register ('will it fly', musical-note parsing, fruit-distribution word problems) is categorically different from enterprise-development prose [DATASET-D22, DATASET-D6, DATASET-D21]. Geographically the benchmark is US/Anglophone-origin which matches the target population. — _Sources: DATASET-D22, DATASET-D6, DATASET-D21_
- **IC-3**: Western-specific knowledge is not the main issue; the issue is competitive-programming-specific framing. One observed locale artifact (comma-as-decimal in HumanEval/137 [DATASET-D11]) is European in origin but irrelevant to the deployment. — _Sources: DATASET-D11_
- **IC-4**: INSUFFICIENT DOCUMENTATION — annotator demographics are not provided; the paper states 'there is unfortunately only limited research on the demographic distribution of Python users' [Q219]. Re-annotation would require org-internal architects (already available as the grading population). — _Sources: Q219_
- **IC-5**: Content harms validity by failing to probe framework idioms, business entity modeling, or compliance/SLA constraints; training-data quality issues are acknowledged [Q167] but do not bear directly on the deployment task. — _Sources: Q167, WEB-22_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q14] 'Though not a guarantee for problem novelty, all problems were hand-written and not programmatically copied from existing sources.' (p.3)
- [Q23] 'Our training dataset was collected in May 2020 from 54 million public software repositories hosted on GitHub, containing 179 GB of unique Python files under 1 MB.' (p.4)
- [Q52] 'We curated 10,000 problems in this way.' (p.7)
- [Q167] 'The GitHub dataset contains plenty of poor-quality code...code that compiles and often runs without errors but gives an incorrect answer.' (p.27)
- [Q206] 'We used 5 prompts across different libraries for RSA and AES based on Sonar Source's Python vulnerability database, and generated ~30k samples total.' (p.32)
- [Q219] 'There is unfortunately only limited research on the demographic distribution of Python users.' (p.33)

*Web sources:*
- [WEB-22] Enterprise AI-generated code shows 153% increase in architectural flaws — the content domain that HumanEval cannot evaluate is exactly the domain where production failures concentrate

*Dataset analysis:*
- DATASET-D7: HumanEval/124 date-validation docstring exemplifies clean US English prose register
- DATASET-D2: typed signature `List[float]` consistent with Pydantic/FastAPI typing
- DATASET-D22: 'will_it_fly' whimsical framing alien to enterprise context
- DATASET-D21: fruit-distribution word problem unrelated to software-development register
- DATASET-D11: comma-as-decimal European locale artifact (irrelevant minor finding)

</details>

**Information gaps:**
- Annotator demographics and selection process for the 164 problems are not documented.
- Whether any framework-specific patterns appear in the Codex-S 40k CI-traced functions (training-side, not in HumanEval test set).

**Requires expert verification:**
- Architect-team review of whether the security probe content [Q206] has any reusable value for evaluating auth-middleware or secrets-handling correctness in the deployment.

---

### Input Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
HumanEval inputs are short single-paragraph docstrings averaging 7.7 tests per problem [Q20], assembled as 'a header, a signature, and a docstring' [Q28]. The deployment requires 3–10 page semi-structured PRDs with consistent headings and variable prose under each section. The paper itself explicitly acknowledges Codex 'struggles to parse through increasingly long and higher-level or system-level specifications' [Q88] and demonstrates exponential degradation with docstring complexity [Q90, Q93]. Empirical sampling confirms docstrings range from a single sentence [DATASET-D13, DATASET-D14] to ~15 lines maximum [DATASET-D7] — orders of magnitude shorter than a 3–10 page PRD. LongCodeBench [WEB-3] documents Claude 3.5 Sonnet dropping from 29% to 3% as context length increases on coding tasks, quantifying the severity of this mismatch.

**Strengths:**
- Input form within HumanEval is clean and parseable, making the benchmark easy to load and run as a lower-bound check for single-function Python utilities embedded within the deployment's broader output [DATASET-D1].

**Checklist:**

- **IF-1**: Signal-distribution mismatch is severe: short docstrings (~1 sentence to ~15 lines) vs. 3–10 page semi-structured PRDs with multi-section headings. The paper acknowledges this kind of long-specification handling is a known weakness [Q88]. — _Sources: Q20, Q28, Q88, DATASET-D13, DATASET-D7_
- **IF-2**: Infrastructure question is largely inapplicable — both contexts use text. However, stop-sequence tuning ('\nclass', '\ndef', '\n#', '\nif', '\nprint') [Q29] is configured for single-function termination and would need redesign for multi-file output. — _Sources: Q29_
- **IF-3**: Domain-specific form differences: HumanEval lacks structured-document parsing (headings, user-story templates, NFR tables); requires no long-context attention; provides no multi-section coherence test. LongCodeBench [WEB-3] is the closest published evidence base on long-context degradation. LoCoBench [WEB-18] explicitly notes existing benchmarks 'primarily emphasize code completion and comprehension tasks rather than complex software development workflows'. — _Sources: Q90, Q93, WEB-3, WEB-18_
- **IF-4**: External validity is severely harmed: short-docstring pass rates do not predict PRD-length input performance; quantified degradation rate (29%→3% [WEB-3]) provides empirical justification. The benchmark cannot surface context-length failure modes at all. — _Sources: Q88, WEB-3_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q20] 'Each problem includes a function signature, docstring, body, and several unit tests, with an average of 7.7 tests per problem.' (p.4)
- [Q28] 'To compute pass@k, we assemble each HumanEval problem into a prompt consisting of a header, a signature, and a docstring.' (p.4)
- [Q29] 'We sample tokens from Codex until we encounter one of the following stop sequences: \nclass, \ndef, \n#, \nif, or \nprint.' (p.4)
- [Q88] 'Codex struggles to parse through increasingly long and higher-level or system-level specifications.' (p.10)
- [Q90] 'As the number of chained building blocks in the docstring increases, model performance decreases exponentially.' (p.10)
- [Q93] 'With each additional component, pass rate drops by roughly a factor of 2-3.' (p.10)

*Web sources:*
- [WEB-3] LongCodeBench documents Claude 3.5 Sonnet dropping from 29% to 3% as context length increases on coding tasks
- [WEB-18] LoCoBench confirms existing benchmarks emphasize completion/comprehension rather than complex software-development workflows

*Dataset analysis:*
- DATASET-D13: HumanEval/42 single-sentence docstring 'Return list with elements incremented by 1.'
- DATASET-D14: HumanEval/52 one-sentence docstring with no structured sections
- DATASET-D7: HumanEval/124 — longest sampled docstring (~10 lines), still orders of magnitude shorter than a 3–10 page PRD

</details>

**Information gaps:**
- Exact token-count distribution of the org's PRD corpus is not measured (noted as [NEEDS VERIFICATION] in regional context).

**Requires expert verification:**
- Architect-team measurement of typical PRD token counts on the org's actual document corpus to size context-window requirements precisely.

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
HumanEval's output ontology is binary functional correctness via unit tests [Q77]. The paper argues this is superior to BLEU-style match metrics [Q10, Q18, Q40] — a defensible position for algorithm problems — but explicitly acknowledges that 'evaluating code generation' for tightly specified tasks is different from broader qualitative metrics it can only prospectively describe [Q86, Q149], and that 'there is no similar way to evaluate docstring samples automatically' [Q78]. The deployment requires a four-layer rubric (syntactic/lint, requirements completeness, architectural convention adherence, multi-file coherence) — none of which can be expressed by pass/fail unit tests. Appendix-D specification attributes (variable interdependencies [Q153], temporal reasoning [Q154], concurrency [Q155]) and the security-probe ontology (RSA <2048 bits [Q208], AES ECB [Q209]) extend the schema slightly but remain incompatible with rubric-based architectural grading. Prometheus 2 [WEB-14] offers a candidate rubric-judge framework that the org would need to deploy separately.

**Strengths:**
- Pass/fail unit-test scoring provides a usable lower-bound signal for the 'syntactic/lint correctness' layer of the deployment rubric where Python utility functions are concerned [Q77, DATASET-D1].
- The security probe ontology (RSA key length, AES mode) [Q208, Q209] provides a small precedent for adding programmatic correctness checks beyond unit tests, partially reusable for the deployment's security-pattern checks.

**Checklist:**

- **OO-1**: The deployment's label space (4-layer rubric with multiple valid designs) is fundamentally categorical/multi-dimensional. HumanEval's binary unit-test pass/fail label has minimal overlap. — _Sources: Q77, DATASET-D16_
- **OO-2**: Missing categories: syntactic/lint compliance scoring (not just execution), requirements-completeness coverage, architectural convention adherence (naming, folder structure, auth patterns), multi-file coherence (entity ↔ API ↔ frontend type alignment). Cross-layer consistency is unmeasurable [WEB-11, WEB-12]. — _Sources: Q78, WEB-11, WEB-12_
- **OO-3**: The benchmark's ontology assumes a single correct behavioral contract per problem, which conflicts with the deployment's explicit acceptance of multiple valid architectural designs (correctness_model.multiple_valid_designs=true). — _Sources: Q10, DATASET-D15_
- **OO-4**: Stakeholder-driven redesign is required: the architecture guide must be encoded as a structured rubric (Prometheus 2-compatible [WEB-14]) and validated against human gold-annotated samples, with TRACE [WEB-16] biases addressed (LLM-judge preference for longer code, etc.). — _Sources: WEB-14, WEB-16_
- **OO-5**: Structural validity is harmed because the construct's structure (multi-dimensional architectural correctness) is collapsed to a single binary axis. Content validity is harmed by missing categories. External validity is harmed because HumanEval scores cannot predict rubric-based performance. IaC performance floors of <20% pass@1 [WEB-4] and ~50% on simplest scenarios [WEB-5] confirm that ontology gaps in HumanEval map to known LLM weakness areas. — _Sources: Q86, Q149, WEB-4, WEB-5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q10] 'Match-based metrics are unable to account for the large and complex space of programs functionally equivalent to a reference solution.' (p.2)
- [Q77] 'When we benchmark our code generation models, we measure pass@k on the HumanEval dataset, where correctness is defined by passing a set of unit tests.' (p.9)
- [Q78] 'However, there is no similar way to evaluate docstring samples automatically.' (p.9)
- [Q86] 'Many existing metrics measure performance in tightly specified, constrained problem instances...Therefore, we developed a set of qualitative metrics for measuring the capabilities of code generating models while controlling for the complexity and abstraction level of the specifications.' (p.10)
- [Q149] 'Below we provide brief descriptions of such attributes and qualitative metrics, which are to be further discussed in a forthcoming paper.' (p.25)
- [Q208] 'RSA keys were considered improperly configured if they were shorter than 2048 bits.' (p.32)

*Web sources:*
- [WEB-4] IaC-Eval reports SOTA <20% pass@1 on compositional IaC requirements — output-ontology gap in HumanEval maps to known LLM weakness
- [WEB-5] DPIaC-Eval finds 42.7% of syntactically correct templates fail deployment, demonstrating ontology layers HumanEval cannot capture
- [WEB-11] DevEval introduces Recall@k for dependency accuracy alongside Pass@k — closest published metric to import-graph coherence
- [WEB-12] DevBench covers full SDLC stages — illustrates richer output ontology the deployment requires
- [WEB-14] Prometheus 2 supports user-defined rubric criteria in pointwise and pairwise formats
- [WEB-16] TRACE identifies 35 LLM-judge / human-developer misalignment sources requiring calibration

*Dataset analysis:*
- DATASET-D16: random-input test harness exemplifies single-function functional-correctness ontology incompatible with architectural rubric scoring
- DATASET-D15: trivial one-liner shows correctness collapses to behavioral output match — no architectural dimension scoreable

</details>

**Information gaps:**
- Whether the architecture guide can be reduced to a rubric format compatible with Prometheus 2-style judging without losing fidelity.

**Requires expert verification:**
- Architect-team encoding of the internal architecture guide into a structured criterion-separated rubric.
- Calibration of any rubric-judge model against human-annotated gold samples per TRACE recommendations [WEB-16].

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Ground-truth label provenance for HumanEval is sparse and inapplicable to the deployment. The paper provides no annotator demographics, no inter-annotator agreement, and only minimal documentation of who hand-wrote the problems. The only explicit human annotation activity is hand-grading 10 docstring samples per problem 'due to the time consuming nature of this process' [Q79]. Unit-test labels for the Codex-S competitive-programming subset were partially constructed from problem-statement examples rather than complete hidden suites [Q52], and the paper acknowledges 'human developers often write test suites with limited but targeted coverage' [Q129]. Alignment evaluations treat the model itself as the labeler [Q164]. For a deployment whose ground truth requires expert architectural judgment against an internal style guide written by senior architects, HumanEval's label provenance is entirely inapplicable. Empirical sampling further confirms vacuous filler assertions [DATASET-D17] and minor annotation quality issues [DATASET-D27] suggesting no formal multi-reviewer process.

**Strengths:**
- Unit-test labels in the sampled set generally cover edge cases (empty inputs, format violations, boundary conditions) [DATASET-D1, DATASET-D7], so where HumanEval is reused as a sub-component check for Python utility functions, the labels provide meaningful behavioral signal.

**Checklist:**

- **OC-1**: No — labels reflect algorithmic-correctness ground truth, not architectural-convention ground truth required by US enterprise architects [Q77, DATASET-D3]. — _Sources: Q77, DATASET-D3_
- **OC-2**: Potential disagreement is total: HumanEval ground truth has no architectural-convention dimension to disagree about. A model passing all unit tests may still violate every internal convention. Faros.ai analysis [WEB-22] documents 153% increase in architectural flaws in AI-generated code — precisely the failure mode HumanEval cannot label. — _Sources: WEB-22, DATASET-D17_
- **OC-3**: INSUFFICIENT DOCUMENTATION — the paper provides no Datasheet, no Data Statement, no annotator demographics, no professional-background information, no inter-annotator agreement statistics. The paper itself notes limited research on Python-user demographics [Q219]. — _Sources: Q219_
- **OC-4**: Re-annotation would require the org's own architects working from the internal architecture guide — effectively building a new benchmark, not relabeling HumanEval.
- **OC-5**: INSUFFICIENT DOCUMENTATION — no aggregation method is documented because labels are binary per-task and not aggregated across annotators.
- **OC-6**: Convergent validity and external validity are both violated: original labels do not correlate with regional/organizational stakeholder judgments because they probe a different construct entirely. Stack Overflow 2025 [WEB-1] also notes 76% of developers resist AI for 'deployment and monitoring' tasks — the very tasks HumanEval's labels cannot evaluate. — _Sources: Q129, Q164, WEB-1_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q52] 'Since complete test suites are often hidden, we created unit tests from examples found in the problem statements, or extracted additional test cases through submitting incorrect solutions.' (p.7)
- [Q79] 'Due to the time consuming nature of this process, we only grade 10 samples per problem.' (p.9)
- [Q129] 'Human developers often write test suites with limited but targeted coverage, but this does not always work well against an algorithm.' (p.14)
- [Q164] 'We instruct the model to write correct code, and we assume the model could easily be fine-tuned to detect such an instruction.' (p.27)
- [Q219] 'There is unfortunately only limited research on the demographic distribution of Python users.' (p.33)

*Web sources:*
- [WEB-1] Stack Overflow 2025 — 76% of developers don't plan to use AI for deployment/monitoring; 69% don't plan to use AI for project planning — reflects target-cohort skepticism about LLM outputs in exactly the layers HumanEval cannot grade
- [WEB-22] Faros.ai — 153% increase in architectural flaws in AI-generated code; 322% increase in privilege escalation paths

*Dataset analysis:*
- DATASET-D17: HumanEval/105 contains vacuous `assert True` filler assertions, inflating reported test-count and indicating no formal multi-reviewer process
- DATASET-D27: HumanEval/66 has stray apostrophe in docstring — minor annotation-quality artifact
- DATASET-D3: ground-truth label is exact floating-point output match — no code-quality dimension labeled

</details>

**Information gaps:**
- Who hand-wrote the 164 problems and what calibration process was applied is not documented.
- Whether multiple reviewers assessed each problem is not documented.
- Inter-annotator agreement for the docstring grading task is not reported.

**Requires expert verification:**
- Construction of a new gold-annotated sample set by the org's architects against the internal architecture guide if HumanEval-style labels are to be supplemented for the deployment.

---

### Output Form — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
HumanEval outputs are single Python function completions [Q2] evaluated by deterministic unit-test execution with nucleus sampling top_p=0.95 [Q30] and temperature optimized per k [Q34]. The deployment requires multi-file project trees spanning Python (FastAPI/SQLAlchemy/Pydantic), SQL, TypeScript (React/Angular), Java (Spring Boot), YAML (Docker/Kubernetes), and HCL (Terraform). Stop sequences are explicitly configured for single-function termination ('\nclass', '\ndef', etc.) [Q29], which would require complete redesign for multi-file output. The mean-log-probability sample-selection heuristic [Q39] is structurally closer to the deployment's single-completion API use case than to pass@k, so partial reusability exists for the autocomplete-style aspect. Empirical sampling confirms zero multi-file or non-Python outputs across the dataset.

**Strengths:**
- The text-in / code-out modality matches the deployment at the signal level [Q2].
- Single-completion sample selection via mean log probability [Q39] is structurally aligned with the deployment's single-prompt LLM-API usage pattern.
- Sandboxed execution infrastructure [Q8, DATASET-D1] is directly reusable for evaluating any Python sub-components in the deployment's output.

**Checklist:**

- **OF-1**: Partial match — both contexts output text-form code, but HumanEval is restricted to single-file single-function Python while the deployment requires multi-file, multi-language output trees [Q2 vs. deployment.artifact_layers_under_evaluation]. — _Sources: Q2, Q29_
- **OF-2**: Not applicable — neither context involves speech output.
- **OF-3**: Not applicable — target population is professional engineers with expert technical literacy [regional context: technical_literacy].
- **OF-4**: External validity is moderately harmed: HumanEval cannot evaluate multi-file outputs, cross-language outputs (SQL, TypeScript, YAML, HCL), or structural properties (folder layout, import graph coherence). DevEval Recall@k [WEB-11] is the closest published metric for cross-file dependency accuracy. IaC-Eval [WEB-4] and Multi-IaC-Eval [WEB-6] cover the YAML/HCL output form HumanEval omits entirely. — _Sources: Q29, WEB-4, WEB-6, WEB-11_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'On HumanEval, a new evaluation set we release to measure functional correctness for synthesizing programs from docstrings, our model solves 28.8% of the problems.' (p.1)
- [Q8] 'We discuss the sandbox environment we used to safely execute model-generated code.' (p.2)
- [Q29] 'We sample tokens from Codex until we encounter one of the following stop sequences: \nclass, \ndef, \n#, \nif, or \nprint.' (p.4)
- [Q30] 'We use nucleus sampling (Holtzman et al., 2020) with top p = 0.95 for all sampling evaluation in this work.' (p.4)
- [Q39] 'Choosing the sample with the highest mean token log probability outperforms evaluating a random sample.' (p.5)

*Web sources:*
- [WEB-4] IaC-Eval provides Terraform/HCL output-form evaluation HumanEval lacks
- [WEB-6] Multi-IaC-Eval covers CloudFormation, Terraform, and CDK output forms
- [WEB-11] DevEval introduces Recall@k for dependency accuracy — closest published cross-file coherence metric
- [WEB-13] FrontendBench covers front-end interactivity output forms

*Dataset analysis:*
- DATASET-D5: HumanEval/38 contains two functions in one file — closest the dataset comes to multi-function output, still single-file scope
- DATASET-D9: HumanEval/95 entirely self-contained, no imports from other modules

</details>

**Information gaps:**
- Whether the org would treat partial-output reuse (e.g., extracting the Python-only sub-component score) as meaningful signal for any deployment decision.

**Requires expert verification:**
- Architect-team decision on whether multi-file coherence metrics (e.g., entity-name diffing across generated artifact layers) should be implemented as custom evaluation harnesses to supplement HumanEval-style execution checks.

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** No coverage of DB schema, API route, frontend stub, or IaC artifact categories.

**Recommendation:** Adopt DevBench [WEB-12] for multi-stage SDLC coverage and add IaC-Eval/DPIaC-Eval/Multi-IaC-Eval [WEB-4/5/6] for the deployment-config layer; build a small org-specific benchmark of PRD→scaffolding examples sampled from the internal architecture guide to cover FastAPI/SQLAlchemy/Pydantic/Spring Boot idioms.

### Output Ontology ⚠

**Gap:** Binary unit-test pass/fail cannot express the deployment's 4-layer rubric (syntactic/lint, requirements completeness, architectural convention adherence, multi-file coherence).

**Recommendation:** Encode the internal architecture guide as a structured Prometheus 2-compatible rubric [WEB-14], with criterion-separated scoring; calibrate the judge model against a small human-annotated gold set per TRACE recommendations [WEB-16]; complement with deterministic checks (linters, schema diffing) where possible.

### Output Content ⚠

**Gap:** No annotator demographics, no inter-annotator agreement, no architectural-convention labels.

**Recommendation:** Recruit 2–3 senior architects from the target team to independently grade a sample of model outputs against the architecture guide; measure inter-annotator agreement to validate the rubric and identify ambiguous criteria before scaling.

### Input Content

**Gap:** Absence of framework-idiomatic content, business entity models, and NFR/compliance constraints.

**Recommendation:** Construct an internal evaluation set from anonymized real PRDs paired with architect-approved scaffolding solutions; capture the full content register (business context, entity definitions, NFRs, auth/SLA constraints) that HumanEval omits.

### Input Form

**Gap:** Short docstrings cannot probe long-context PRD parsing (29%→3% Claude 3.5 Sonnet degradation [WEB-3]).

**Recommendation:** Add LongCodeBench [WEB-3] / LoCoBench [WEB-18] to the evaluation suite and measure typical PRD token counts on the org's actual document corpus to calibrate context-window sizing; compare full-document vs. section-by-section prompting empirically.

### Output Form

**Gap:** Single-file single-function output cannot evaluate multi-file project trees or cross-language coherence.

**Recommendation:** Build an in-house harness for multi-file coherence checks (entity-name diffing between DB schema, API model, frontend prop types; import-graph validation) since no public benchmark explicitly scores this; reuse DevEval's Recall@k [WEB-11] as a starting metric for cross-file dependency accuracy.

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
| Q8 | 2 | output_form | "In this section, we discuss the details of our evaluation framework. We begin by defining the pass@k metric, and explain its advantages over standard match-based metrics. Next, we describe the dataset of hand-written problems, called "HumanEval," which we created in order to benchmark our models. Finally, we discuss the sandbox environment we used to safely execute model-generated code." |
| Q9 | 2 | output_form | "Generative models for code are predominantly benchmarked by matching samples against a reference solution, where the match can be exact or fuzzy (as in BLEU score)." |
| Q10 | 2 | output_ontology | "More fundamentally, match-based metrics are unable to account for the large and complex space of programs functionally equivalent to a reference solution." |
| Q11 | 2 | output_form | "We argue that this metric should be applied to docstring-conditional code generation as well." |
| Q12 | 2 | output_ontology | "Perhaps the most convincing reason to evaluate functional correctness is that it is used by human developers to judge code. A framework known as test-driven development dictates that software requirements be converted into test cases before any implementation begins, and success is defined by a program that passes these tests." |
| Q13 | 2 | output_form | "Kulal et al. (2019) evaluate functional correctness using the pass@k metric, where k code samples are generated per problem, a problem is considered solved if any sample" |
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
| Q28 | 4 | input_form | "To compute pass@k, we assemble each HumanEval problem into a prompt consisting of a header, a signature, and a docstring, which is illustrated in Figure 2." |
| Q29 | 4 | output_form | "We sample tokens from Codex until we encounter one of the following stop sequences: '\nclass', '\ndef', '\n#', '\nif', or '\nprint', since the model will continue generating additional functions or statements otherwise." |
| Q30 | 4 | output_form | "We use nucleus sampling (Holtzman et al., 2020) with top p = 0.95 for all sampling evaluation in this work." |
| Q31 | 5 | output_form | "model test loss follows a power law in model size (Kaplan et al., 2020), test loss after code fine-tuning follows a similar power law with functional form (N / 5.92×10^7)^-0.13 where N is the number of non-embedding parameters in the model." |
| Q32 | 5 | output_form | "When evaluating pass@k, it is important to optimize sampling temperature for the particular value of k." |
| Q33 | 5 | output_form | "We find that higher temperatures are optimal for larger k, because the resulting set of samples has higher diversity, and the metric rewards only whether the model generates any correct solution." |
| Q34 | 5 | output_form | "In particular, for a 679M parameter model, the optimal temperature for pass@1 is T* = 0.2 and the optimal temperature for pass@100 is T* = 0.8." |
| Q35 | 5 | output_form | "With these temperatures, we find that pass@1 and pass@100 scale smoothly as a function of model size (Figure 6)." |
| Q36 | 5 | output_form | "Pass@k can also be interpreted as the result of evaluating the best out of k samples, where the best sample is picked by an oracle with prior knowledge of the unit tests." |
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
| Q65 | 8 | input_form | "To address these issues, we use Codex-12B to generate 100 samples per curated problem. If no samples pass the unit tests, we consider the task to be either ambiguous or too difficult, and filter it out." |
| Q66 | 8 | input_form | "We reran this verification several times to remove stateful or non-deterministic problems." |
| Q67 | 8 | input_form | "We fine-tune Codex on these training problems to produce a set of "supervised fine-tuned" models, which we call Codex-S." |
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
| Q88 | 10 | input_form | "Moreover, Codex struggles to parse through increasingly long and higher-level or system-level specifications." |
| Q89 | 10 | input_content | "To concretely illustrate model performance degradation as docstring length increases, we create a dataset of synthetic problems assembled from 13 basic building blocks, each of which modifies an input string in a deterministic way." |
| Q90 | 10 | input_form | "We find that as the number of chained building blocks in the docstring increases, model performance decreases exponentially." |
| Q91 | 10 | input_form | "This behavior is uncharacteristic of a human programmer, who should be able to correctly implement a program for a chain of arbitrary length if they can do so for a chain of length two." |
| Q92 | 10 | input_form | "Further, just as text-conditional generative models in other modalities (Ramesh et al., 2021) have difficulty with binding attributes to objects, Codex can make mistakes binding operations to variables, especially when the number of operations and variables in the docstring is large." |
| Q93 | 10 | input_form | "With each additional component, pass rate drops by roughly a factor of 2-3." |
| Q94 | 10 | input_ontology | "Codex has the potential to be useful in a range of ways. For example, it could help onboard users to new codebases, reduce context switching for experienced coders, enable non-programmers to write specifications and have Codex draft implementations, and aid in education and exploration." |
| Q95 | 10 | output_ontology | "However, Codex also raises significant safety challenges, does not always produce code that is aligned with user intent," |
| Q96 | 11 | output_ontology | "To better understand some of the hazards of using Codex in a generative capacity, we conducted a hazard analysis focused on identifying risk factors (Leveson, 2019) with the potential to cause harm." |
| Q97 | 11 | output_ontology | "While some of our findings about the potential societal impacts of code generation systems were informed by work towards responsible deployment of the production-oriented Codex models (which descended from the research-oriented Codex models described in this paper), this section is not intended to provide a full account of any particular product's safety features." |
| Q98 | 11 | output_ontology | "Unless otherwise specified, we anchor our analysis in the specific properties of the models described in this paper." |
| Q99 | 11 | output_content | "One of the key risks associated with using code generation models in practice is over-reliance on generated outputs." |
| Q100 | 11 | output_content | "Due to the limitations described above as well as alignment issues described below, Codex may suggest solutions that superficially appear correct but do not actually perform the task the user intended." |
| Q101 | 11 | output_ontology | "We discuss a related issue in Appendix G, namely that code generation models can suggest insecure code." |
| Q102 | 11 | output_content | "As with other large language models trained on a next-token prediction objective, Codex will generate code that is as similar as possible to its training distribution." |
| Q103 | 11 | output_content | "One consequence of this is that such models may do things that are unhelpful for the user, despite having the capability to be more helpful (see Figure 12)." |
| Q104 | 11 | output_ontology | "This is an alignment failure - the model is not aligned with the user's intentions." |
| Q105 | 11 | output_ontology | "It is important to study misalignment because it is a problem that is likely to become worse, not better, as the capabilities of our systems increase." |
| Q106 | 12 | output_content | "Codex could have various effects on the security landscape. Because Codex can produce vulnerable or misaligned code, qualified operators should review its generations before executing or trusting them, absent appropriate precautions." |
| Q107 | 12 | output_content | "Future code generation models may be able to be trained to produce more secure code than the average developer, though that is far from certain." |
| Q108 | 12 | output_content | "Although this is worthy of concern, based on our testing, we believe that at their current level of capability, Codex models do not materially lower the barrier to entry for malware development." |
| Q109 | 12 | output_content | "The non-deterministic nature of systems like Codex could enable more advanced malware." |
| Q110 | 12 | input_content | "Similar to large language models, Codex models can learn patterns present in their training data (Carlini et al., 2021). Sensitive data present in source code are liable to be predicted by the model." |
| Q111 | 12 | input_content | "Because Codex is trained on public repositories, we consider any sensitive data present in the training data to have already been compromised." |
| Q112 | 13 | input_content | "Codex, like other large generative models, has an energy footprint from both training and inference (Schwartz et al., 2019; Bender et al., 2021; Patterson et al., 2021)." |
| Q113 | 13 | input_content | "The original training of GPT-3-12B consumed hundreds of petaflop/s-days of compute, while fine-tuning it to create Codex-12B consumed a similar amount of compute." |
| Q114 | 13 | input_content | "This training was performed on a platform (Azure) that purchases carbon credits and sources significant amounts of renewable energy, reducing its carbon footprint." |
| Q115 | 13 | input_content | "Our preliminary research also finds that Codex models rarely generate code that is identical to the contents of training data. Such occurrences were < 0.1% in a study examining the frequency of code generations that appear to match code snippets in the training data (Ziegler, 2021)." |
| Q116 | 13 | input_content | "In these rare instances, the generated code consisted of common expressions or conventions within the programming language that appeared over and over again in the training data." |
| Q117 | 13 | input_content | "We find that, to the extent the generated code appears identical to the training data, it is due to the predictive weightings in the model rather than retention and copying of specific code." |
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
| Q160 | 26 | output_content | "This caches out in predictions that the model will complete confused code with confused code, insecure code with insecure code (see G), or biased code with similarly biased code (see F), regardless of the model's capability to produce secure, unbiased, and high-quality code." |
| Q161 | 26 | output_ontology | "Defining alignment is complex, and there is not yet a satisfactory formalization." |
| Q162 | 26 | output_ontology | "We operationalize sufficient conditions for intent misalignment for a generative model as follows: 1. We consider a model capable of some task X if it has" |
| Q163 | 27 | output_ontology | "We conducted several alignment evaluations. In the example evaluation shown in Figure 14, we deduce that the model is capable of outputting code with a lower frequency of bugs, based on the rate of bugs when prompted with high-quality code." |
| Q164 | 27 | output_content | "We instruct the model to write correct code, and we assume the model could easily be fine-tuned to detect such an instruction. This implies that the model is capable of distinguishing between situations where the user does and does not want buggy code." |
| Q165 | 27 | output_content | "Based on this we conclude that we have identified misalignment in Codex models." |
| Q166 | 27 | output_content | "There are several subtleties here; probably the most important one is distinguishing our observations from a robustness failure. If the subtly buggy code is sufficiently out-of-distribution, we might observe that the model performs worse in these cases, simply because it is thrown off by the OOD input - it is not in fact capable of outputting good code after seeing OOD prompts." |
| Q167 | 27 | input_content | "We believe this is unlikely to be a large factor here, as the GitHub dataset contains plenty of poor-quality code. The bugs are designed to be of the sort we'd expect to appear commonly in the dataset; code that compiles and often runs without errors but gives an incorrect answer. Examples include off-by-one errors or single-character typographic errors." |
| Q168 | 27 | input_content | "The datasets used for these evaluations are available at https://github.com/openai/code-align-evals-data." |
| Q169 | 27 | output_content | "One starting point is to more carefully curate the pre-training dataset to remove buggy or insecure code." |
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
| Q188 | 30 | output_content | "Most synthesized completions included "White" and many included only a few other categories, followed by "other." Several synthesized generations included only 3 categories: "white," "black," or "none."" |
| Q189 | 30 | output_form | "To test these hypotheses and the related harms, we compared GPT-3 to Codex comment production on a series of co-occurrence tests across gender, race, and religion." |
| Q190 | 30 | output_content | "Very broadly, we found that when explicitly prompted to talk about specific genders, races, and religions, Codex comments tend to reproduce similar biases to GPT-3, albeit with less diversity in the outputs." |
| Q191 | 30 | output_content | "For example, with religion "Islam", in both models we observed occurrences of the word "terrorist" and "violent" at a greater rate than with other groups, but GPT-3's outputs included more variants on these themes." |
| Q192 | 30 | output_form | "Co-occurrence is a blunt instrument, as it doesn't pick up on the subtleties of how a particular word is used in context, only that it is used in context." |
| Q193 | 30 | output_content | "Additionally, since we are prompting both models to explicitly describe groups, they are not from the models talking about these group features in the wild, but rather in a constrained experimental setup." |
| Q194 | 30 | output_form | "Co-occurrence tests measure which words are likely to occur in the neighborhood of other words." |
| Q195 | 31 | output_ontology | "The threat landscape for Codex is similar to that of language models. Actors can range from low and moderately skilled or resourced actors to well-resourced and highly-organized "advanced persistent threat" (APT) groups." |
| Q196 | 31 | output_ontology | "However, the manner in which Codex models may be misused will likely differ from that of language models." |
| Q197 | 31 | output_content | "It is our assessment that Codex models do not differentially enable offensive cybersecurity capabilities because they are not more efficient or effective than conventional tools or techniques are." |
| Q198 | 31 | output_form | "We conducted experiments on Codex's ability to generate malicious code. While we found that while Codex is not proficient at generating standalone malicious code, it is still capable of generating code that can be incorporated as components of more complex systems." |
| Q199 | 31 | output_form | "We found that Codex did not perform well when compared even to rudimentary Static Application Security Testing (SAST) tools." |
| Q200 | 31 | output_form | "We encountered no cases in our testing where using a Codex model led to better or more efficient results than SAST tools." |
| Q201 | 31 | output_content | "However, Codex is generally unable to suggest specific versions of packages, as package versions are specified outside of the prompt context that Codex is aware of." |
| Q202 | 31 | output_content | "Through testing, we found that the likelihood of Codex suggesting a vulnerable or malicious package is low in aggregate." |
| Q203 | 31 | input_content | "We found that models trained on source code offered no advantages over conventional language models because the domains are fundamentally different." |
| Q204 | 32 | input_ontology | "To study this phenomenon, we asked Codex to suggest code that would call cryptographic libraries to generate cryptographic contexts, and then evaluated whether any of these outputs were clearly insecure." |
| Q205 | 32 | input_ontology | "When tested on a standard series of prompts asking the models to call functions to produce RSA keys or AES contexts, we find that Codex models of varying sizes frequently use clearly insecure configurations (See Figure 15)." |
| Q206 | 32 | input_content | "We used 5 prompts across different libraries for RSA and AES based on Sonar Source's Python vulnerability database, and generated ˜30k samples total." |
| Q207 | 32 | input_form | "We then removed some generated samples based on expected runtime errors, as different model sizes tend to vary in whether they produce code that runs." |
| Q208 | 32 | output_ontology | "RSA keys were considered improperly configured if they were shorter than 2048 bits." |
| Q209 | 32 | output_ontology | "AES contexts were considered improperly configured if they used the ECB cipher mode (see Menezes et al. (2018), p. 228)." |
| Q210 | 32 | output_ontology | "We chose these two tests to evaluate as targets because there is consensus among cryptography experts that these configurations generally should not be used, and these were reasonable to evaluate programmatically." |
| Q211 | 32 | output_content | "Interestingly, we do not see a robust model size trend (over 1 order of magnitude of parameters) in this data." |
| Q212 | 32 | output_content | "This suggests that insecure code production, at least in this case, is an alignment issue (see Appendix E): it is unclear if the models are improving with scale." |
| Q213 | 32 | output_content | "A larger study using the most common insecure code vulnerabilities may shed more light on this issue." |
| Q214 | 33 | output_ontology | "When asked to create encryption keys, Codex models select clearly insecure configuration parameters in a significant fraction of cases. We evaluated outputs as clearly insecure if: (a) RSA keys were shorter than 2048 bits, (b) AES contexts used the ECB cipher mode." |
| Q215 | 33 | output_ontology | "Because security standards change over time as capabilities improve, this is likely an underestimate of the true rate of improperly configured outputs." |
| Q216 | 33 | output_ontology | "Similarly, the produced samples that were not classified as clearly insecure are not necessarily secure, as our tests measure insecurity." |
| Q217 | 33 | input_form | "Additionally, one of the challenges of code generation stem from relying on the assumption that intent is captured sufficiently enough in comments and documentation to not compromise accuracy." |
| Q218 | 33 | input_form | "Thus, even if the model were perfectly accurate, we would not expect it to reduce the labor costs associated with writing code to zero." |
| Q219 | 33 | input_content | "There is unfortunately only limited research on the demographic distribution of Python users." |
| Q220 | 34 | input_content | "Codex imports substitutable packages at different rates based on patterns in its training data, which can have various possible implications." |
| Q221 | 34 | output_content | "Differential import rates by Codex might lead to subtle errors in cases where a certain import is ill-advised, increase robustness in cases where the alternative package imported by an individual would have been worse, and/or increase the dominance of an already-influential set of individuals and organizations in the software supply chain." |
| Q222 | 34 | output_content | "The scale of these effects for Codex may be relatively low if users mostly import packages they know how to use or have done outside research on, so they can double-check anything the model does." |
| Q223 | 34 | input_form | "Moreover, because packages are generally imported at the top of a file without any comments, the model has very little to go on in these cases, so users would most likely have to start typing out the name of the package they want to import rather than trusting the model to know they are starting a machine learning project and want to import either PyTorch or TensorFlow." |
| Q224 | 34 | output_form | "As one example, we looked at completions of the prompt: # import machine learning package import and found that over 100 completions of 100 tokens, 6 contained suggestions for TensorFlow and 3 for PyTorch, two libraries that are rough substitutes." |
| Q225 | 35 | input_ontology | "Most past studies of the impacts of code generation models consider performance on a closed set of tasks in a simulated environment (Xu et al., 2021)." |
| Q226 | 35 | input_ontology | "As the deployment of Codex and other near-term technologies proceeds, we may be able to conduct more robust experiments examining the impact of various strengths of models on real-world job performance, across teams and across firms." |
| Q227 | 35 | output_ontology | "Precise and accurate prediction of any impacts without user or market signal is difficult, but the potential implications on the long-run labor market and the possibility of disparate outcomes across groups warrant further exploration of these issues." |
| Q228 | 35 | output_ontology | "It may be possible to assess the relative likelihood of different scenarios by building a deeper understanding of Codex's capabilities across several code-related tasks or by studying the effects of precise deployment scenarios." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://survey.stackoverflow.co/2025/ai |
| WEB-2 | https://www.gartner.com/en/newsroom/press-releases/2025-07-01-gartner-identifies-the-top-strategic-trends-in-software-engineering-for-2025-and-beyond |
| WEB-3 | https://arxiv.org/pdf/2505.07897 |
| WEB-4 | https://medium.com/gft-engineering/evaluating-llms-for-infrastructure-as-code-9f8b9ac4ca33 |
| WEB-5 | https://arxiv.org/html/2506.05623v1 |
| WEB-6 | https://arxiv.org/pdf/2509.05303 |
| WEB-7 | https://arxiv.org/pdf/2310.06770 |
| WEB-8 | https://www.emergentmind.com/topics/swe-bench-3b86a734-b378-4ee6-bcaf-640949ed7afb |
| WEB-9 | https://arxiv.org/pdf/2512.17419 |
| WEB-10 | https://aclanthology.org/2024.findings-acl.214.pdf |
| WEB-11 | https://arxiv.org/pdf/2405.19856 |
| WEB-12 | https://arxiv.org/abs/2403.08604 |
| WEB-13 | https://arxiv.org/html/2506.13832v2 |
| WEB-14 | https://arxiv.org/abs/2405.01535 |
| WEB-15 | https://github.com/prometheus-eval/prometheus-eval |
| WEB-16 | https://arxiv.org/pdf/2603.24586 |
| WEB-17 | https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80 |
| WEB-18 | https://arxiv.org/pdf/2509.09614 |
| WEB-19 | https://arxiv.org/html/2601.08734v1 |
| WEB-20 | https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/ |
| WEB-21 | https://www.secondtalent.com/resources/ai-coding-assistant-statistics/ |
| WEB-22 | https://www.faros.ai/blog/enterprise-ai-coding-assistant-adoption-scaling-guide |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** openai/openai_humaneval
**Analysis date:** 2025-07-14
**Examples reviewed:** 40 from `test` split (164 total)
**Columns shown:** task_id, prompt, canonical_solution, test, entry_point
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | openai_humaneval | HumanEval/61 | pass/fail | `def correct_bracketing(brackets: str): """ brackets is a string of "(" and ")". return True if every opening bracket has a corresponding closing bracket."""` | Classic bracket-matching algorithm problem — no enterprise context | IO, IC |
| D2 | openai_humaneval | HumanEval/0 | pass/fail | `def has_close_elements(numbers: List[float], threshold: float) -> bool: """ Check if in given list of numbers, are any two numbers closer to each other than given threshold."""` | Pairwise distance threshold check — pure algorithmic problem | IO, IC |
| D3 | openai_humaneval | HumanEval/130 | pass/fail | `def tri(n): """Everyone knows Fibonacci sequence... Tribonacci sequence is defined by the recurrence: tri(1) = 3, tri(n) = 1 + n / 2, if n is even."""` | Mathematical sequence computation — competitive-programming style | IO, IC |
| D4 | openai_humaneval | HumanEval/32 | pass/fail | `def find_zero(xs: list): """ xs are coefficients of a polynomial. find_zero find x such that poly(x) = 0."""` | Numerical root-finding for polynomial — algorithm/math problem | IO, IC |
| D5 | openai_humaneval | HumanEval/38 | pass/fail | `def encode_cyclic(s: str): """ returns encoded string by cycling groups of three characters."""` | String encoding scheme — single self-contained function stub | IF |
| D6 | openai_humaneval | HumanEval/17 | pass/fail | `def parse_music(music_string: str) -> List[int]: """ Input to this function is a string representing musical notes in a special ASCII format. Your task is to parse this string and return list of integers corresponding to how many beats does each not last."""` | ASCII music note parser — short docstring, single function | IF, IC |
| D7 | openai_humaneval | HumanEval/124 | pass/fail | `def valid_date(date): """You have to write a function which validates a given date string and returns True if the date is valid otherwise False. The date should be in the format: mm-dd-yyyy"""` | Date validation — single utility function, no framework idioms | IO, IC |
| D8 | openai_humaneval | HumanEval/3 | pass/fail | `def below_zero(operations: List[int]) -> bool: """ You're given a list of deposit and withdrawal operations on a bank account that starts with zero balance."""` | Bank account balance simulation — simple algorithm, no ORM/API context | IO, IC |
| D9 | openai_humaneval | HumanEval/95 | pass/fail | `def check_dict_case(dict): """Given a dictionary, return True if all keys are strings in lower case or all keys are strings in upper case, else return False."""` | Dictionary key case check — generic utility, no enterprise conventions | IO |
| D10 | openai_humaneval | HumanEval/11 | pass/fail | `def string_xor(a: str, b: str) -> str: """ Input are two strings a and b consisting only of 1s and 0s. Perform binary XOR on these inputs and return result also as a string."""` | Binary string XOR — pure algorithmic, no real-world domain | IO, IC |
| D11 | openai_humaneval | HumanEval/137 | pass/fail | `def compare_one(a, b): """ Create a function that takes integers, floats, or strings representing real numbers, and returns the larger variable in its given variable type. Note: If a real number is represented as a string, the floating point might be . or ,"""` | Numeric comparison with comma-decimal format — minor internationalisation note | IC |
| D12 | openai_humaneval | HumanEval/127 | pass/fail | `def intersection(interval1, interval2): """...determine whether the length of intersection of these two intervals is a prime number."""` | Interval intersection + primality check — competitive-programming flavour | IO |
| D13 | openai_humaneval | HumanEval/42 | pass/fail | `def incr_list(l: list): """Return list with elements incremented by 1."""` | Trivially simple list transform — minimal docstring | IF |
| D14 | openai_humaneval | HumanEval/52 | pass/fail | `def below_threshold(l: list, t: int): """Return True if all numbers in the list l are below threshold t."""` | Threshold comparison — very short docstring | IF |
| D15 | openai_humaneval | HumanEval/30 | pass/fail | `def get_positive(l: list): """Return only positive numbers in the list."""` | Positive filter — one-liner solution, minimal specification | IF, OO |
| D16 | openai_humaneval | HumanEval/38 | pass/fail | `def check(candidate): from random import randint, choice import string letters = string.ascii_lowercase for _ in range(100): str = ''.join(choice(letters) for i in range(randint(10, 20))) encoded_str = encode_cyclic(str) assert candidate(encoded_str) == str` | Unit test uses randomised inputs — tests functional correctness only | OO |
| D17 | openai_humaneval | HumanEval/105 | pass/fail | `def by_length(arr): """ Given an array of integers, sort the integers that are between 1 and 9 inclusive, reverse the resulting array, and then replace each digit by its corresponding name from "One", "Two", "Three"..."""` | Word-for-digit mapping — contrived puzzle task | IO |
| D18 | openai_humaneval | HumanEval/144 | pass/fail | `def simplify(x, n): """Your task is to implement a function that will simplify the expression x * n. The function returns True if x * n evaluates to a whole number... Both x and n, are string representation of a fraction"""` | Fraction arithmetic — interview-style math problem | IO |
| D19 | openai_humaneval | HumanEval/109 | pass/fail | `def move_one_ball(arr): """...determine if it is possible to get an array sorted in non-decreasing order by performing the following operation... You are allowed to perform right shift operation any number of times."""` | Circular sort feasibility — competitive programming | IO |
| D20 | openai_humaneval | HumanEval/2 | pass/fail | `def truncate_number(number: float) -> float: """ Given a positive floating point number... Return the decimal part of the number."""` | Decimal extraction — trivially short docstring | IF |
| D21 | openai_humaneval | HumanEval/67 | pass/fail | `def fruit_distribution(s,n): """ In this task, you will be given a string that represents a number of apples and oranges that are distributed in a basket of fruit this basket contains apples, oranges, and mango fruits."""` | Word-problem arithmetic parsing — no enterprise relevance | IC |
| D22 | openai_humaneval | HumanEval/72 | pass/fail | `def will_it_fly(q,w): ''' Write a function that returns True if the object q will fly, and False otherwise. The object q will fly if it's balanced (it is a palindromic list) and the sum of its elements is less than or equal the maximum possible weight w.'''` | Palindrome + sum constraint — whimsical puzzle framing | IC, IO |
| D23 | openai_humaneval | HumanEval/154 | pass/fail | `def cycpattern_check(a , b): """You are given 2 words. You need to return True if the second word or any of its rotations is a substring in the first word"""` | Cyclic substring check — string algorithm | IO |
| D24 | openai_humaneval | HumanEval/88 | pass/fail | `def sort_array(array): """ Given an array of non-negative integers, return a copy of the given array after sorting, you will sort the given array in ascending order if the sum(first index value, last index value) is odd, or sort it in descending order if the sum is even."""` | Conditional sort direction — contrived rule | IO |
| D25 | openai_humaneval | HumanEval/14 | pass/fail | `def all_prefixes(string: str) -> List[str]: """ Return list of all prefixes from shortest to longest of the input string"""` | Prefix enumeration — minimal single-sentence docstring | IF |
| D26 | openai_humaneval | HumanEval/37 | pass/fail | `def find_zero(xs: list): """ xs are coefficients of a polynomial. find_zero find x such that poly(x) = 0. find_zero returns only only zero point, even if there are many."""` | Polynomial root finding via bisection — numeric algorithm | IO |
| D27 | openai_humaneval | HumanEval/66 | pass/fail | `def digitSum(s): """Task Write a function that takes a string as input and returns the sum of the upper characters only' ASCII codes."""` | ASCII uppercase character sum — simple string processing | IO |
| D28 | openai_humaneval | HumanEval/121 | pass/fail | `def solution(lst): """Given a non-empty list of integers, return the sum of all of the odd elements that are in even positions."""` | Index-parity filter — competitive-programming style | IO |
| D29 | openai_humaneval | HumanEval/104 | pass/fail | `def unique_digits(x): """Given a list of positive integers x. return a sorted list of all elements that hasn't any even digit."""` | Digit-evenness filter — puzzle problem | IO |
| D30 | openai_humaneval | HumanEval/132 | pass/fail | `def is_nested(string): ''' Create a function that takes a string as input which contains only square brackets. The function should return True if and only if there is a valid subsequence of brackets where at least one bracket in the subsequence is nested.'''` | Bracket nesting check — algorithmic | IO |
| D31 | openai_humaneval | HumanEval/158 | pass/fail | `def find_max(words): """Write a function that accepts a list of strings. The list contains different words. Return the word with maximum number of unique characters."""` | Max-unique-chars word selection — string/sort algorithm | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Clean, executable Python function format with deterministic unit tests
- **Dimension(s):** IF, OF
- **Observation:** Every sampled example follows a strict schema: function signature, docstring, canonical solution, and a `check(candidate)` unit-test function. The test harness is immediately executable in a Python sandbox without any preprocessing. All 40 sampled examples conform perfectly to this format.
- **Deployment relevance:** The Python layer of the enterprise stack (FastAPI route handlers, SQLAlchemy model methods) does involve single-function Python generation. This execution-based evaluation infrastructure — pass/fail against deterministic assertions — could serve as a lower-bound baseline for isolated Python utility functions, which may appear as sub-components of API logic. The clean schema also means the benchmark can be loaded and executed without engineering overhead.
- **Datapoint citations:**
  - [D1] Example HumanEval/61 (openai_humaneval, split=test, label=pass/fail): `"def correct_bracketing(brackets: str): ... METADATA = {} def check(candidate): assert candidate('()') ..."` — Exemplifies the consistent schema: prompt, canonical solution, and an immediately runnable test function.
  - [D15] Example HumanEval/30 (openai_humaneval, split=test, label=pass/fail): `"def get_positive(l: list): """Return only positive numbers in the list.""""` — Even the simplest entries follow the same executable structure, confirming schema consistency across difficulty levels.

#### Strength 2: English-language natural language docstrings
- **Dimension(s):** IC, IF
- **Observation:** All docstrings are written in standard US English, with consistent use of imperative-mood task descriptions, explicit examples, and typed Python signatures. The natural language register is professional and unambiguous.
- **Deployment relevance:** The deployment population writes specifications in US English and expects generated code with English-language docstrings and comments. HumanEval's English-only NL matches the deployment's NL requirement exactly at the language level, even though the content is categorically different.
- **Datapoint citations:**
  - [D7] Example HumanEval/124 (openai_humaneval, split=test, label=pass/fail): `"You have to write a function which validates a given date string and returns True if the date is valid otherwise False. The date is valid if all of the following rules are satisfied..."` — Clear, multi-rule English specification with numbered conditions; mirrors the instructional prose style found in PRD requirements sections.
  - [D6] Example HumanEval/17 (openai_humaneval, split=test, label=pass/fail): `"Input to this function is a string representing musical notes in a special ASCII format. Your task is to parse this string and return list of integers..."` — Illustrates task-description prose analogous to API requirements phrasing.

#### Strength 3: Typed Python function signatures with `from typing import List`
- **Dimension(s):** IC, IF
- **Observation:** Several problems use Python type annotations (`List[float]`, `List[int]`, `List[str]`), which is consistent with modern Python practice and with the deployment's use of Pydantic v2 and typed FastAPI schemas.
- **Deployment relevance:** The presence of typed signatures in HumanEval problems at least tests whether models produce type-annotated Python, which is a prerequisite for Pydantic schema generation in the deployment stack. This is a narrow but genuine point of contact.
- **Datapoint citations:**
  - [D2] Example HumanEval/0 (openai_humaneval, split=test, label=pass/fail): `"from typing import List def has_close_elements(numbers: List[float], threshold: float) -> bool:"` — Uses explicit type annotations including `List[float]` and a typed return value.
  - [D6] Example HumanEval/17 (openai_humaneval, split=test, label=pass/fail): `"from typing import List def parse_music(music_string: str) -> List[int]:"` — Typed signature with string input and list output.

#### Strength 4: Unit test coverage captures edge cases
- **Dimension(s):** OO, OC
- **Observation:** The unit tests in the sampled examples are thoughtfully constructed: they cover normal cases, boundary conditions, empty inputs, negative numbers, and invalid inputs. Average test count across the sample is consistent with the paper's reported 7.7 per problem.
- **Deployment relevance:** While the binary pass/fail ontology does not match the deployment's rubric-based grading, the practice of asserting edge-case behavior is directly relevant to the deployment's "syntactic and lint correctness" layer. Architects evaluating scaffolding would also expect models to handle empty collections, null inputs, and invalid formats.
- **Datapoint citations:**
  - [D1] Example HumanEval/61 (openai_humaneval, split=test, label=pass/fail): `"assert not candidate('((()())))')\nassert not candidate(')(()')\nassert not candidate('(')\nassert not candidate('((((')"` — Tests multiple distinct failure modes including empty nesting and unbalanced leading/trailing brackets.
  - [D7] Example HumanEval/124 (openai_humaneval, split=test, label=pass/fail): `"assert candidate('04122003') == False\nassert candidate('20030412') == False\nassert candidate('2003-04') == False\nassert candidate('2003-04-12') == False"` — Edge cases test format violations including wrong separators and truncated dates.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Complete absence of multi-artifact, multi-language scaffolding tasks
- **Dimension(s):** IO
- **Observation:** Every single one of the 40 sampled examples — and by extension all 164 benchmark problems — is a standalone, self-contained Python function. The benchmark contains zero examples of SQL schema generation, ORM model definition, REST API route handler creation, frontend component stubs, or infrastructure-as-code. The task taxonomy is exclusively single-function algorithmic/mathematical Python synthesis.
- **Deployment relevance:** The deployment requires evaluation across four structurally distinct artifact layers: (1) database schemas (SQL DDL, SQLAlchemy ORM), (2) API routes (FastAPI handlers, Pydantic schemas), (3) frontend stubs (React/Next.js TypeScript), and (4) deployment configs (Dockerfile, Kubernetes YAML, Terraform HCL). HumanEval covers none of these layers. The entire purpose of the deployment evaluation — end-to-end scaffolding generation — is unrepresented in the benchmark's input ontology.
- **Datapoint citations:**
  - [D1] Example HumanEval/61 (openai_humaneval, split=test, label=pass/fail): `"def correct_bracketing(brackets: str): """ brackets is a string of '(' and ')'. return True if every opening bracket has a corresponding closing bracket.""""` — Pure bracket-matching algorithm; no resemblance to any enterprise scaffolding artifact.
  - [D3] Example HumanEval/130 (openai_humaneval, split=test, label=pass/fail): `"def tri(n): """Everyone knows Fibonacci sequence... Tribonacci sequence is defined by the recurrence: tri(1) = 3, tri(n) = 1 + n / 2, if n is even.""""` — Mathematical sequence task; categorically unrelated to database schema, API, or frontend generation.
  - [D8] Example HumanEval/3 (openai_humaneval, split=test, label=pass/fail): `"def below_zero(operations: List[int]) -> bool: """ You're given a list of deposit and withdrawal operations on a bank account that starts with zero balance.""""` — The closest to a "business" domain in the sample, yet it is still a pure algorithmic simulation with no ORM, endpoint, or schema relevance.

#### Concern 2: Binary pass/fail unit-test scoring is categorically incompatible with rubric-based enterprise grading
- **Dimension(s):** OO, OC
- **Observation:** The entire benchmark scores outputs as either passing or failing all unit tests. There is no dimension for naming conventions, folder structure, architectural pattern adherence, auth middleware placement, or multi-file coherence. The scoring function cannot be extended to these dimensions without a complete redesign.
- **Deployment relevance:** The deployment's correctness model has at least four layers: syntactic validity, requirements completeness, architectural convention adherence (measured against an internal style guide), and multi-file coherence. HumanEval's unit-test pass/fail captures at most the first layer (syntactic validity is a prerequisite for test execution) and partially the second (if the function's behavior matches the docstring). Layers 3 and 4 are structurally impossible to evaluate with this scoring function. A score on HumanEval is therefore not a valid predictor of performance on the deployment's rubric.
- **Datapoint citations:**
  - [D16] Example HumanEval/38 (openai_humaneval, split=test, label=pass/fail): `"def check(candidate): from random import randint, choice import string letters = string.ascii_lowercase for _ in range(100): str = ''.join(choice(letters) for i in range(randint(10, 20))) encoded_str = encode_cyclic(str) assert candidate(encoded_str) == str"` — The test harness verifies functional correctness of a single isolated function via randomised input/output matching; it cannot assess naming conventions, module structure, or cross-file consistency.
  - [D15] Example HumanEval/30 (openai_humaneval, split=test, label=pass/fail): `"def get_positive(l: list): """Return only positive numbers in the list.""""` — A one-liner function whose "correctness" is entirely captured by whether `[e for e in l if e > 0]` returns the right values; no architectural dimension is evaluable.

#### Concern 3: Input form — all prompts are short single-paragraph docstrings; deployment inputs are 3–10 page PRDs
- **Dimension(s):** IF
- **Observation:** Across all 40 sampled examples, docstrings range from one sentence (D13, D14, D15, D20, D25) to approximately 15–20 lines for the most complex problems (D3, D7, D22). None approach even a single page of structured specification text. The longest prompts in the sample contain a handful of examples and constraints; none embed business context, user stories, non-functional requirements, or multi-section structured headings.
- **Deployment relevance:** Deployment inputs are 3–10 page Confluence/PRD documents with consistent headings (business context, user stories, data entities, API expectations, non-functional requirements), fed as single-context prompts. LongCodeBench (2025) documents Claude 3.5 Sonnet degrading from 29% to 3% as context length increases on coding tasks. HumanEval's short-docstring pass rates are not valid predictors of PRD-length input performance; the benchmark cannot surface context-length degradation at all.
- **Datapoint citations:**
  - [D13] Example HumanEval/42 (openai_humaneval, split=test, label=pass/fail): `"def incr_list(l: list): """Return list with elements incremented by 1.""""` — Single-sentence docstring; represents minimum possible specification length — the opposite extreme from a 3–10 page PRD.
  - [D14] Example HumanEval/52 (openai_humaneval, split=test, label=pass/fail): `"def below_threshold(l: list, t: int): """Return True if all numbers in the list l are below threshold t.""""` — One-sentence docstring; no structured sections, no non-functional requirements, no multi-entity context.
  - [D7] Example HumanEval/124 (openai_humaneval, split=test, label=pass/fail): `"You have to write a function which validates a given date string and returns True if the date is valid otherwise False. The date is valid if all of the following rules are satisfied: 1. The date string is not empty. 2. The number of days is not less than 1 or higher than 31 days for months 1,3,5,7,8,10,12..."` — One of the longer docstrings in the sample (~10 lines); still orders of magnitude shorter than a 3–10 page PRD with multiple business-context sections.

#### Concern 4: No framework-specific idioms — FastAPI, SQLAlchemy, Pydantic, Spring Boot absent from all sampled problems
- **Dimension(s):** IC
- **Observation:** None of the 40 sampled problems contain any import, reference, or pattern from FastAPI, SQLAlchemy, Pydantic, Spring Boot, React, Next.js, Docker, Kubernetes, or Terraform. The content domain is exclusively generic Python algorithmic problems: bracket matching, sequence generation, polynomial root-finding, string manipulation, list filtering. The most "domain-like" problem is a bank account balance simulation (D8) that uses only a plain list of integers.
- **Deployment relevance:** The deployment's primary and secondary stacks require framework-specific idiomatic code: FastAPI dependency injection (`Depends()`), SQLAlchemy declarative ORM models, Pydantic v2 model definitions, Spring Boot `@RestController` and `@Service` annotations, React component prop interfaces, and Kubernetes manifest structure. A model that scores highly on HumanEval's generic algorithmic problems may have no demonstrated capability with these framework idioms. The benchmark provides no signal on the content the deployment actually needs evaluated.
- **Datapoint citations:**
  - [D4] Example HumanEval/32 (openai_humaneval, split=test, label=pass/fail): `"def find_zero(xs: list): """ xs are coefficients of a polynomial. find_zero find x such that poly(x) = 0... find_zero only takes list xs having even number of coefficients and largest non zero coefficient as it guarantees a solution.""""` — Pure numerical analysis algorithm; no database, API, or framework context.
  - [D22] Example HumanEval/72 (openai_humaneval, split=test, label=pass/fail): `"def will_it_fly(q,w): ''' Write a function that returns True if the object q will fly, and False otherwise. The object q will fly if it's balanced (it is a palindromic list) and the sum of its elements is less than or equal the maximum possible weight w.'''` — Whimsical puzzle with no enterprise analogue; illustrates the content register gap between competitive-programming problems and enterprise scaffolding requirements.
  - [D21] Example HumanEval/67 (openai_humaneval, split=test, label=pass/fail): `"def fruit_distribution(s,n): """ In this task, you will be given a string that represents a number of apples and oranges that are distributed in a basket of fruit this basket contains apples, oranges, and mango fruits.""""` — Word-problem arithmetic; the closest to a "real-world" parsing task but still entirely unrelated to enterprise software development.

#### Concern 5: Single-file, single-function output scope — no multi-file coherence evaluation possible
- **Dimension(s):** OF, OO
- **Observation:** Every problem in the dataset defines exactly one function and one unit-test harness for that function. There are no examples where a correct solution requires generating multiple files, defining class hierarchies across modules, maintaining consistent entity names across layers, or producing configuration files alongside code.
- **Deployment relevance:** The deployment's highest-priority correctness requirement beyond functional correctness is multi-file coherence: schema entities must match API model field names must match frontend TypeScript prop types. This cross-layer consistency cannot be represented or scored within HumanEval's single-function output form. The benchmark's stop-sequence design (`\nclass`, `\ndef`) is explicitly configured to terminate generation at a single-function boundary, making it structurally incapable of evaluating multi-file output.
- **Datapoint citations:**
  - [D5] Example HumanEval/38 (openai_humaneval, split=test, label=pass/fail): `"def encode_cyclic(s: str): """ returns encoded string by cycling groups of three characters.""" ... def decode_cyclic(s: str): """takes as input string encoded with encode_cyclic function. Returns decoded string.""""` — The only multi-function example in the sample; the second function depends on the first, but both are in the same single file and tested together, still within single-file scope.
  - [D9] Example HumanEval/95 (openai_humaneval, split=test, label=pass/fail): `"def check_dict_case(dict): """Given a dictionary, return True if all keys are strings in lower case or all keys are strings in upper case, else return False.""""` — Entirely self-contained; no imports from other modules, no multi-file dependency, no schema entity referencing.

---

#### MAJOR

#### Concern 6: Ground-truth labels are unit-test pass/fail on algorithm problems — inapplicable to enterprise architectural judgment
- **Dimension(s):** OC
- **Observation:** The canonical solutions and unit tests in the sample are written for algorithmic problems with a single correct behavioral contract. For example, `canonical_solution` for HumanEval/130 (Tribonacci) is a specific numerical sequence generator; correctness is defined by matching specific floating-point outputs. There is no annotation of code quality, style, naming appropriateness, or structural soundness — these dimensions are simply absent from the ground truth.
- **Deployment relevance:** The deployment's ground-truth correctness requires expert architectural judgment against an internal style guide. Architect-graders at the target enterprise would assess whether a FastAPI route handler follows the internal naming convention for endpoints, whether the Pydantic model uses the correct field validation patterns, and whether the folder structure matches the architecture guide. HumanEval's ground-truth labels have zero applicability to this grading task. A model that passes all HumanEval tests may still generate scaffolding that fails every architectural convention check.
- **Datapoint citations:**
  - [D3] Example HumanEval/130 (openai_humaneval, split=test, label=pass/fail): `"assert candidate(3) == [1, 3, 2.0, 8.0]\nassert candidate(4) == [1, 3, 2.0, 8.0, 3.0]"` — Ground truth is exact floating-point output matching for a mathematical sequence; this annotation methodology has no relationship to enterprise code review criteria.
  - [D17] Example HumanEval/105 (openai_humaneval, split=test, label=pass/fail): `"assert candidate([2, 1, 1, 4, 5, 8, 2, 3]) == ['Eight', 'Five', 'Four', 'Three', 'Two', 'Two', 'One', 'One']"` — Correctness defined by exact string list output; no code quality, naming, or structural dimension is present in the label.

#### Concern 7: Competitive-programming / interview-problem framing is categorically different from enterprise development register
- **Dimension(s):** IC
- **Observation:** The sample reveals a consistent problem-framing register: self-contained mathematical puzzles ("Everyone knows Fibonacci sequence," "You're a hungry rabbit"), competitive-programming constructs (Tribonacci sequences, palindromic lists as flight conditions, cyclic pattern matching), and abstract algorithmic challenges (polynomial roots, binary XOR). This register is characteristic of LeetCode/Codeforces-style interview preparation, not enterprise software development.
- **Deployment relevance:** Enterprise scaffolding generation from PRDs involves a completely different cognitive and linguistic register: business entities (User, Order, Product), API contracts (GET /api/v1/users/{id}), compliance constraints (rate limiting, CORS, JWT auth), and operational concerns (connection pooling, health check endpoints). The mismatch in problem-framing register means models trained or evaluated on HumanEval learn to respond to puzzle-style cues rather than business-requirement cues, which is precisely the distribution the deployment needs to evaluate.
- **Datapoint citations:**
  - [D22] Example HumanEval/72 (openai_humaneval, split=test, label=pass/fail): `"def will_it_fly(q,w): ''' Write a function that returns True if the object q will fly, and False otherwise. The object q will fly if it's balanced (it is a palindromic list) and the sum of its elements is less than or equal the maximum possible weight w.'''` — Whimsical "flying object" framing for a palindrome+sum check; entirely alien to enterprise development context.
  - [D6] Example HumanEval/17 (openai_humaneval, split=test, label=pass/fail): `"Input to this function is a string representing musical notes in a special ASCII format. Your task is to parse this string and return list of integers corresponding to how many beats does each not last. Here is a legend: 'o' - whole note, lasts four beats; 'o|' - half note, lasts two beats; '.|' - quater note, lasts one beat"` — Custom musical notation parsing; the kind of bespoke puzzle specification typical of interview problems, not enterprise API development.
  - [D11] Example HumanEval/137 (openai_humaneval, split=test, label=pass/fail): `"Note: If a real number is represented as a string, the floating point might be . or ,"` — The comma-as-decimal convention is a European locale artifact embedded in a US-origin benchmark problem; irrelevant to the deployment's US enterprise context and illustrative of the ad-hoc nature of problem construction.

---

#### MINOR

#### Concern 8: Docstring quality is variable; some problems have imprecise or ambiguous specifications
- **Dimension(s):** OC, IC
- **Observation:** Several sampled docstrings contain minor quality issues: HumanEval/66 has a stray apostrophe in the task description (`"returns the sum of the upper characters only' ASCII codes"`), HumanEval/158 has a misquoted string in the docstring example (`'aaaaaaa"` mixing quote styles), and HumanEval/19 contains a typo ("numberals" for "numerals"). These are cosmetic issues but indicate the annotation was not formally reviewed.
- **Deployment relevance:** For the deployment context, docstring quality matters as a signal of specification clarity. Architects feeding PRDs expect the model to handle ambiguous or underspecified requirements gracefully — but HumanEval's problems are designed to be unambiguous, so the benchmark cannot probe this capability. The minor quality issues in annotations do not materially affect validity scoring but suggest the benchmark was authored quickly without multi-reviewer validation.
- **Datapoint citations:**
  - [D27] Example HumanEval/66 (openai_humaneval, split=test, label=pass/fail): `"Write a function that takes a string as input and returns the sum of the upper characters only' ASCII codes."` — Stray apostrophe breaks the natural-language description; minor annotation quality issue.
  - [D26] Example HumanEval/19 (openai_humaneval, split=test, label=pass/fail): `"Input is a space-delimited string of numberals from 'zero' to 'nine'."` — "numberals" is a misspelling of "numerals"; minor but confirms absence of formal annotation review.

#### Concern 9: Some unit tests are underspecified or rely on vacuous assertions
- **Dimension(s):** OC, OO
- **Observation:** Multiple sampled tests include placeholder assertions like `assert True, "This prints if this assert fails 1 (good for debugging!)"`. While these do not affect correctness scoring (a vacuous assertion always passes), they indicate the test suites have coverage gaps. Additionally, HumanEval/104 and HumanEval/121 have relatively few meaningful test cases.
- **Deployment relevance:** The benchmark documentation claims an average of 7.7 tests per problem, but the presence of vacuous filler assertions inflates this count. For the deployment context, test suite completeness is a direct analog of requirements completeness — a concern noted in the paper itself (Q129). This is a minor issue for HumanEval's primary use case but reinforces the inapplicability of the unit-test evaluation model to the deployment's rubric-based grading.
- **Datapoint citations:**
  - [D17] Example HumanEval/105 (openai_humaneval, split=test, label=pass/fail): `"assert True, 'This prints if this assert fails 1 (good for debugging!)' ... assert True, 'This prints if this assert fails 2 (also good for debugging!)'"` — Two of the six test assertions are vacuous; actual test count is four, not six.
  - [D28] Example HumanEval/121 (openai_humaneval, split=test, label=pass/fail): `"assert candidate([5, 8, 7, 1]) == 12 ... # Check some edge cases that are easy to work out by hand."` — The "edge cases" section header is followed by no actual edge case assertions, leaving test coverage incomplete for boundary conditions.

---

### Content Coverage Summary

The 40 sampled HumanEval examples represent a highly uniform content domain: standalone, self-contained Python function synthesis problems drawn from algorithmic and mathematical problem-solving traditions. The register is consistently competitive-programming / interview-preparation: problems involve bracket matching, sequence generation, polynomial root-finding, string encoding/decoding, cyclic pattern detection, digit-sum filtering, and list manipulation under contrived sorting rules. No problem in the sample involves any enterprise software artifact type (database schema, API route handler, ORM model, frontend component, deployment configuration).

Docstrings range from one sentence (most common) to approximately 15 lines for the most complex problems. All are in standard US English with imperative-mood task descriptions and inline examples. Type annotations appear in roughly 25–30% of sampled problems. Unit tests are deterministic and cover normal cases plus several edge cases; a minority of tests include vacuous `assert True` placeholders.

The canonical solutions are clean, idiomatic Python: comprehensions, simple loops, standard library use (`math`, `typing`). No imports from third-party libraries appear in any solution. The solutions are typically 3–15 lines and demonstrate correct algorithmic reasoning at an easy-to-medium interview difficulty level.

Ground-truth correctness is entirely defined by behavioral matching against the unit tests. No annotation of code style, naming conventions, architectural patterns, or cross-file consistency exists or is possible within this schema.

---

### Limitations

1. **Sample coverage**: 40 of 164 problems were reviewed (~24%). The sample may not include the most complex problems (higher task IDs in the 140–163 range are well-represented, which may overrepresent the harder problems). The benchmark's full distribution across the 13 "building block" synthetic tasks and safety/security probes described in the paper are not present in the HuggingFace dataset and could not be inspected.

2. **Safety probes not in dataset**: The cryptographic security evaluation (~30k samples), gender/race bias probes, and alignment evaluation datasets described extensively in the paper are not included in the HuggingFace `openai/openai_humaneval` repository. These components cannot be assessed from the available data.

3. **Canonical solution quality**: The analysis can observe that canonical solutions exist and are syntactically valid Python, but cannot execute them to verify correctness or assess whether edge cases in the unit tests are actually handled correctly by the canonical solution (e.g., the date validation in HumanEval/124 has a known operator-precedence bug in the canonical solution that is not detectable by static inspection alone).

4. **No negative examples available**: The dataset contains only the benchmark problems themselves, not model-generated completions. The analysis cannot inspect what kinds of incorrect outputs are produced by models or whether scoring discriminates meaningfully among different failure modes relevant to the deployment.

5. **Framework-specific absence is confirmed but not exhaustively verified**: The 40 sampled examples show zero FastAPI/SQLAlchemy/Pydantic/Spring Boot content. Given the full benchmark has only 164 problems and the paper's documentation confirms the content domain, it is highly likely — but not mathematically certain — that the remaining 124 unsampled problems also contain no such content.

