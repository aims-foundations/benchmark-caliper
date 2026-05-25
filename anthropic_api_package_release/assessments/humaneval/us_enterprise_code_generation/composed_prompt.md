I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **HumanEval: Hand-Written Evaluation Set for Python Code Generation** is valid for use in **US Enterprise Software Architects — Full-Stack Scaffolding Generation**.

Analyze the evidence sources below against each of the 6 validity dimensions. For each dimension, assign a score (1-5), provide justification with cited evidence, respond to each checklist item, and identify information gaps.

### Critical Constraints

- **Evidence-grounded only**: Base your analysis ONLY on the three evidence sources provided: (1) benchmark documentation with verbatim quotes, (2) regional context with web-sourced findings, and (3) dataset analysis findings with datapoint citations (if present). Do NOT role-play as a member of the target culture or speculate beyond what these sources support.
- **Cite evidence**: For each finding, cite at least one source — a verbatim quote `[QN]`, a web source `[WEB-N]`, or a dataset citation `DATASET-D{n}`.
- **Flag gaps explicitly**: When none of the three evidence sources addresses a checklist item, say "INSUFFICIENT DOCUMENTATION" and describe what would be needed.
- **Distinguish documentable vs. expert-needed**: Classify each finding as either (a) determinable from documentation, or (b) requiring regional expert verification.
- **Regional specificity**: Evaluate validity *for the specified target region*, not in general.
- **Conservative scoring**: When evidence is ambiguous or insufficient, score lower rather than higher.

### Scoring Rubric

- **1**: Major validity violations identified; benchmark component fundamentally misaligned with target context.
- **2**: Significant concerns; multiple concrete violations or gaps identified.
- **3**: Partially addressed; mixed evidence; some alignment, some gaps.
- **4**: Well addressed; minor concerns or gaps; documentation shows awareness of regional needs.
- **5**: Fully addressed; no concerns identified; documentation demonstrates explicit validity-preserving practices.

### Evidence Sources

The prompt below contains three evidence sources:

1. **Benchmark Documentation** + **Verbatim Quote Registry** — paper content, with authoritative quotes labeled `[QN]`
2. **Regional Context** (YAML) + **Web Source Registry** — deployment context with web research findings cited as `[WEB-N]`
3. **Dataset Analysis Findings** (if present) — empirical observations from the benchmark's HuggingFace data, cited as `DATASET-D{n}`

Citation rules for each source are in your system instructions.

---

## Benchmark Information

- **Name**: humaneval
- **Full Name**: HumanEval: Hand-Written Evaluation Set for Python Code Generation
- **Domain**: Code generation / functional correctness evaluation
- **Languages**: en, py
- **Porting Strategy**: none
- **Year**: 2021

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
HumanEval's task taxonomy is entirely confined to standalone, self-contained Python
function synthesis from natural-language docstrings [Q22, Q130]. The paper
characterises the coverage as spanning "language comprehension, reasoning, algorithms,
and simple mathematics" [Q22] — an interview-problem profile that maps to a single
category in a broader enterprise software taxonomy. The paper explicitly contrasts
this with the APPS benchmark, which at least extends to full-program stdin/stdout
synthesis [Q46], and acknowledges that GitHub code at large encompasses "class
implementations, configuration files, scripts, and even files used to store data"
that are underrepresented in HumanEval-style tasks [Q48].

Appendix D prospectively enumerates richer specification attributes — variable
interdependencies [Q153], temporal reasoning [Q154], and concurrency/parallelism
[Q155] — but these remain qualitative descriptions of future metrics rather than
instantiated test cases [Q149]. A supplementary dataset of 13 "building block"
string-manipulation tasks probes docstring complexity [Q145] but is similarly
confined to single-function synthesis. Safety probe tasks covering gender/race
co-occurrence [Q185, Q186, Q187, Q188] and cryptographic API misuse [Q204, Q205]
extend the taxonomy into bias and security dimensions, but introduce no multi-artifact
or multi-layer scaffolding categories. The benchmark contains zero problems exercising
SQL/ORM schema generation, REST/GraphQL API routing, frontend component stubs, or
infrastructure-as-code — the four artifact layers central to the enterprise
scaffolding deployment.

### Input Content
The 164 HumanEval problems are entirely hand-written and explicitly not copied from
existing sources [Q14, Q19], a design choice motivated by contamination risk given
that the training corpus covers a large fraction of public GitHub [Q21]. The training
data was collected from 54 million public GitHub repositories, yielding 159 GB of
filtered Python [Q23, Q25]; filtering removed auto-generated files and low-density
character content [Q24]. The Codex-S fine-tuning corpus adds approximately 10,000
problems from competitive programming and interview-prep websites [Q52] and roughly
40,000 CI-traced functions from projects using Travis/tox/PyPI [Q55, Q57].

All data sources share the same fundamental content limitation: they originate from
open-source, algorithmic, or competitive programming contexts with no enterprise
architecture conventions, framework-specific idioms (FastAPI dependency injection,
SQLAlchemy ORM, Pydantic schema validation, Spring Boot annotations), business-logic
data models, or compliance/SLA constraints. The security evaluation content uses
approximately 30,000 samples across five RSA/AES prompts drawn from Sonar Source's
Python vulnerability database [Q206], which is somewhat more operationally grounded
but still restricted to cryptographic library calls. The paper notes that "there is
unfortunately only limited research on the demographic distribution of Python users"
[Q219], making it impossible to characterize whose coding conventions are most
represented. Training data is acknowledged to contain poor-quality and buggy code
[Q167], and any sensitive data in public repositories is treated as already
compromised [Q111].

### Input Form
Each HumanEval problem is a short, self-contained function stub: a function
signature, docstring, body, and unit tests assembled into a single prompt [Q20, Q28].
The paper's building-block synthetic dataset specifies each complexity element via
"a line of text and a line of code" [Q146] — an even more minimal input form.
Alignment evaluation prompts prepend three few-shot examples (correct or subtly
buggy solutions) to task docstrings [Q174], slightly lengthening inputs but not
approaching document-length specifications.

The paper explicitly acknowledges that "Codex struggles to parse through increasingly
long and higher-level or system-level specifications" [Q88] and that performance
degrades exponentially as docstring complexity grows [Q90, Q93] — a direct
finding that the short-docstring input form is not a valid proxy for document-length
requirements inputs. Stop sequences are tuned for single-function completion
(`\nclass`, `\ndef`, `\n#`) [Q29] and would require substantial redesign to handle
multi-section structured documents. No inputs in any HumanEval variant approach
the 3–10 page Confluence/PRD format of the deployment's specification inputs.

### Output Ontology
HumanEval's output label space is binary: a generated function either passes all
unit tests or it does not [Q77]. The paper argues explicitly that this functional
correctness criterion is superior to match-based metrics like BLEU [Q10, Q18, Q40],
and draws an analogy to test-driven development as a natural human correctness
standard [Q12]. The docstring generation variant (Codex-D) uses a hand-graded
binary label — correct if the docstring "uniquely and accurately specifies the code
body" and not correct if "the model simply copies the code body into the docstring"
[Q81] — a slightly richer but still binary schema. Security evaluation adds two
expert-defined insecurity labels: RSA keys shorter than 2048 bits [Q208] and AES
contexts using ECB mode [Q209], grounded in cryptographic consensus [Q210].

None of these output ontologies contain categories for syntactic validity, linting
compliance, requirements-level completeness, architectural convention adherence,
naming conventions, folder structure, auth middleware patterns, or multi-file
coherence — the multi-dimensional correctness layers required by the enterprise
rubric. The paper itself acknowledges that "evaluating code generation" for "tightly
specified, constrained problem instances" is different from the broader qualitative
metrics it prospectively describes [Q86, Q151], and that "there is no similar way
to evaluate docstring samples automatically" [Q78] — a direct acknowledgment that
the unit-test ontology does not generalize even within the paper's own scope.

### Output Content
The annotation process for HumanEval is minimal and sparsely documented. The only
human annotation activity described is hand-grading 10 docstring samples per problem
for Codex-D — "due to the time consuming nature of this process" [Q79]. No
information is provided about annotator demographics, professional backgrounds,
geographic origin, or inter-annotator agreement for any grading task. The paper
provides no documentation of who hand-wrote the 164 HumanEval problems, whether
multiple reviewers assessed each problem, or what difficulty calibration process
was applied.

The alignment evaluation treats the model itself as the effective labeler — the
paper "instructs the model to write correct code" and "assumes the model could
easily be fine-tuned to detect such an instruction" [Q164] — which is a model-
behavior probe rather than a human annotation task. Unit-test labels for the
competitive programming subset were partially constructed from problem-statement
examples rather than complete hidden test suites [Q52]. The paper acknowledges that
"human developers often write test suites with limited but targeted coverage, but
this does not always work well against an algorithm" [Q129], conceding that ground-
truth label completeness is an open limitation. For the deployment context, where
correct labels require expert architectural judgment against an internal style guide,
HumanEval's label provenance is entirely inapplicable.

### Output Form
The primary output form is a single Python function completion, evaluated by
deterministic unit-test execution inside a sandboxed environment. The pass@k
metric is computed over n=200 samples with k≤100, using nucleus sampling with
top_p=0.95 [Q13, Q15, Q30]. Temperature is optimized per evaluation mode (T*=0.2
for pass@1, T*=0.8 for pass@100 for the 679M model) [Q34]. The paper provides a
mean log-probability sample-selection heuristic as a proxy for oracle selection in
the single-completion autocomplete scenario [Q39], which is structurally closer to
the deployment's single-completion use case.

The benchmark evaluates only single-file, single-function Python completions.
There is no evaluation of multi-file output trees, cross-file consistency, outputs
in SQL, TypeScript/JavaScript, YAML, HCL, or any language beyond Python, or
structural properties such as folder layout or import graph coherence. The paper
acknowledges the mismatch between BLEU and functional correctness for isolated
functions [Q40, Q123] but does not propose any metric applicable to multi-artifact
scaffolding outputs. The security and bias evaluations use programmatic checks
[Q210, Q214] and co-occurrence statistics [Q189, Q190, Q194] respectively — output
form extensions that remain confined to single-file Python contexts. For docstring
generation, the paper explicitly flags that automatic evaluation is impossible and
hand-grading is required [Q78, Q84] — a direct acknowledgment of the limits of
the unit-test output form, though the hand-grading process itself is not scaled to
the rubric complexity of the enterprise deployment scenario.


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

## Regional Context

```yaml
name: US Enterprise Software Architects — Full-Stack Scaffolding Generation
abbreviation: US-ESA-SCAFFOLD
assessment_context:
  benchmark: humaneval
  deployment_use_case: LLM evaluation for generating complete full-stack web application
    scaffolding (database schemas, API routes, frontend component stubs, deployment
    configurations) from multi-page semi-structured requirements documents (Confluence/PRDs).
  evaluating_organization_type: US enterprise software company (internal AI capability
    evaluation)
  primary_region: United States
  sub_national_scope: No formal sub-national boundary; user population is implicitly
    concentrated in US tech-industry hubs (e.g., San Francisco Bay Area, Seattle,
    New York, Austin, Boston). Remote/distributed teams also represented.
target_population:
  description: American software architects and senior engineers employed at a US
    enterprise software company who are evaluating LLM-generated full-stack scaffolding.
    They are the end-users and primary graders of model output. They possess strong
    technical expertise across multiple layers of a modern web stack and grade outputs
    against an internal architecture guide rather than purely algorithmic correctness.
  occupation_cohort: Software architects and senior software engineers
  seniority_level: Senior / Staff / Principal (architecture-decision makers)
  organizational_role: Primary consumers and evaluators of LLM-generated scaffolding;
    authors and custodians of the internal architecture guide used as the grading
    rubric
  team_context: Enterprise software product teams; evaluation context is pre-deployment
    capability assessment, not production use
languages:
  primary:
  - English (US)
  code_languages:
  - Python (FastAPI, SQLAlchemy, Pydantic)
  - SQL (PostgreSQL dialect)
  - TypeScript / JavaScript (React, Next.js, Angular)
  - Java (Spring Boot)
  - YAML (Docker Compose, Kubernetes manifests)
  - HCL (Terraform)
  - Bash / shell (CI/CD scripts)
  natural_language_input_form: English-language semi-structured PRD / Confluence documents
    (3–10 pages, consistent headings but variable prose)
writing_systems:
  scripts:
  - Latin (ASCII + Unicode; standard US English prose and code)
  note: All specification inputs and expected outputs are in US English / standard
    ASCII-compatible code. No CJK, RTL, or special-script handling required. Tokenization
    challenges are code-specific (e.g., camelCase, snake_case, kebab-case identifiers)
    rather than script-level.
technical_literacy:
  general_literacy: Near-universal among target population (professional engineers)
  code_literacy: Expert — primary graders are software architects fluent in multiple
    languages and frameworks
  ai_tool_familiarity: 'High and broadly confirmed. Stack Overflow''s 2025 Developer
    Survey reports 80% of developers now use AI tools in their workflows, with experienced
    developers showing the highest distrust of output accuracy (only 2.6% ''highly
    trust'' AI output), suggesting widespread familiarity paired with critical evaluation
    posture — well-matched to an architect-grader cohort. Gartner (July 2025) predicts
    90% of enterprise software engineers will use AI code assistants by 2028, up from
    under 14% in early 2024, confirming rapid adoption trajectory.

    Sources: Stack Overflow Developer Survey 2025 — [WEB-1];
    Gartner press release July 2025 — [WEB-2]'
  note: 'Population is not a lay-user cohort; all output evaluation is conducted by
    domain experts capable of identifying syntactic, semantic, and architectural errors.
    Per Stack Overflow 2025, experienced developers show the highest rate of AI output
    distrust (20% ''highly distrust''), reinforcing that architect-graders in this
    cohort will apply rigorous verification. Source: Stack Overflow Developer Survey
    2025 — [WEB-1]'
technology_stack:
  primary_stack:
    backend_framework: FastAPI (Python)
    orm: SQLAlchemy
    schema_validation: Pydantic
    database: PostgreSQL
    frontend_framework: React / Next.js
    language: TypeScript
  secondary_stack:
    backend_framework: Spring Boot (Java)
    database: MySQL
    frontend_framework: Angular
    language: TypeScript / Java
  deployment_targets:
    containerization: Docker (Docker Compose for local dev)
    orchestration: Kubernetes
    cloud_provider: AWS
    iac_tooling: Terraform (occasional use)
  auxiliary_tooling:
    api_style: REST (primary); GraphQL (mentioned as possibility)
    ci_cd: '[NEEDS VERIFICATION — deferred: below search budget; internal toolchain
      (GitHub Actions, Jenkins, CircleCI, or similar) not specified in elicitation
      and not searchable without org-specific context]'
    linting_formatting: '[NEEDS VERIFICATION — deferred: below search budget; likely
      unsearchable (internal convention); Black/ESLint/Prettier/Checkstyle are the
      dominant tools in the relevant ecosystem but specific org selection not confirmable]'
    testing_frameworks: '[NEEDS VERIFICATION — deferred: below search budget; pytest,
      Jest, and JUnit are the de-facto standards for FastAPI/React/Spring Boot respectively
      but org-specific confirmation requires stakeholder elicitation]'
artifact_layers_under_evaluation:
  layer_priority: All four layers required; database schema and API routes are highest
    priority due to refactoring cost
  layers:
  - layer: Database schema
    artifact_types:
    - SQL DDL (PostgreSQL)
    - SQLAlchemy ORM models
    - MySQL DDL (secondary stack)
    criticality: HIGHEST — hardest to refactor post-generation
  - layer: API routes
    artifact_types:
    - FastAPI route handlers
    - Pydantic request/response schemas
    - Spring Boot controllers and DTOs
    criticality: HIGHEST — hardest to refactor post-generation
  - layer: Frontend component stubs
    artifact_types:
    - React/Next.js components (TypeScript)
    - Angular components (TypeScript)
    criticality: HIGH — required for end-to-end scaffolding value proposition
  - layer: Deployment configuration
    artifact_types:
    - Dockerfile
    - Docker Compose YAML
    - Kubernetes manifests (YAML)
    - Terraform modules (HCL)
    criticality: HIGH — required for end-to-end scaffolding value proposition; Terraform
      use is occasional
input_specification_format:
  document_type: Confluence pages or PRD documents
  typical_length_pages: 3–10 pages
  structure: Semi-structured with consistent headings (business context, user stories,
    data entities, API expectations, non-functional requirements) and variable prose
    under each section
  prompt_strategy: 'Currently: full document in a single prompt. Explored: section-by-section
    prompting for larger specs'
  note: 'This input format is categorically different from HumanEval''s short single-paragraph
    docstrings. Long-context handling and structured document parsing are central
    evaluation concerns. LongCodeBench (2025) documents dramatic performance degradation
    from 29% to 3% for Claude 3.5 Sonnet as context length increases within coding
    tasks, confirming the input-form gap is quantitatively severe.

    Source: LongCodeBench arXiv 2025 — [WEB-3]'
correctness_model:
  grading_approach: Rubric-based expert review (not binary unit-test pass/fail)
  rubric_source: Internal architecture guide maintained by the organization
  correctness_layers:
  - layer: Syntactic / lint correctness
    description: Output must parse/compile and pass relevant linters without errors
  - layer: Requirements completeness
    description: All entities, endpoints, and flows named in the PRD must be present
  - layer: Architectural convention adherence
    description: Output must conform to internal naming conventions, folder structure,
      auth middleware patterns, and error handling patterns as specified in the architecture
      guide
  - layer: Multi-file coherence
    description: Schema entities must match API models must match frontend prop types;
      import graphs must be consistent across generated files
  multiple_valid_designs: true
  grading_note: Multiple valid architectural designs are acceptable provided they
    satisfy the rubric. The rubric, not a single reference solution, is the ground
    truth.
infrastructure_notes:
  development_environment: Laptops/workstations with high-speed corporate network
    access; cloud IDE or local IDE (VS Code, IntelliJ) assumed
  internet_access: '[NEEDS VERIFICATION — deferred: likely unsearchable (internal
    IT policy); unrestricted corporate internet access is the US enterprise tech-industry
    norm but VPN/proxy configuration is org-specific and not publicly verifiable]'
  llm_access_mode: API-based LLM access (single-prompt, full-document context window);
    section-by-section prompting explored as alternative
  context_window_requirements: 'Large context window required (3–10 page PRDs); exact
    token counts depend on document verbosity — [NEEDS VERIFICATION — deferred: below
    search budget; average token count per enterprise spec is not published in any
    accessible benchmark; rough estimate is 2,000–8,000 tokens per page at typical
    PRD prose density, placing full-document prompts in the 6,000–80,000 token range]'
  output_size: 'Multi-file project tree; estimated total output size per scaffolding
    generation [NEEDS VERIFICATION — deferred: below search budget; no published benchmark
    measures total token output for full-stack scaffolding; empirical measurement
    against org''s own PRD corpus is the recommended path]'
organizational_and_process_notes:
  evaluation_workflow: Architects review LLM-generated scaffolding against internal
    architecture guide; evaluation is conducted as a capability assessment prior to
    deciding whether to integrate LLM scaffolding into the development workflow
  architecture_guide_status: Codified internal document; serves as grading rubric
  internal_conventions_examples:
  - Naming conventions (file names, variable names, endpoint path patterns)
  - Folder/module structure
  - Auth middleware placement and patterns
  - Error handling conventions
  - ORM relationship patterns
  - API versioning conventions
  specific_conventions: '[NEEDS VERIFICATION — deferred: likely unsearchable (internal
    to organization); exact convention details require stakeholder / expert elicitation
    and are not publicly available]'
cultural_norms_notes: 'Population is US-based professional software engineers operating
  in an enterprise software product context. Relevant norms include:

  - English as the exclusive working language for both natural language (specifications,
  comments) and code conventions.

  - Strong preference for explicit documentation and typed interfaces (TypeScript,
  Pydantic, OpenAPI specs).

  - Convention-over-configuration culture: internal architecture guides are treated
  as authoritative, reducing tolerance for creative deviation from established patterns.

  - Expectation of code reviewability: generated scaffolding must be legible to senior
  engineers, not just functionally correct.

  - Security and compliance sensitivity typical of enterprise software contexts (auth
  patterns, secrets management, data access controls).

  - US enterprise software industry norms around code ownership, IP, and third-party
  dependency choices may influence acceptable library selections in generated scaffolding.

  - Notable population-specific caution signal: Stack Overflow 2025 survey finds 76%
  of developers show resistance specifically to AI for high-responsibility systemic
  tasks like ''Deployment and monitoring'' (76% don''t plan to use AI) and ''Project
  planning'' (69%), directly relevant to the scaffolding deployment config and architecture
  layers. Source: Stack Overflow Developer Survey 2025 — [WEB-1]'
domain_specific_notes:
  architecture_patterns: RESTful API design with layered architecture (controller/service/repository
    or equivalent). FastAPI dependency injection pattern; SQLAlchemy declarative ORM
    models; Pydantic v2 schema validation; Spring Boot @RestController + @Service
    + JPA Repository pattern.
  security_patterns: 'Auth middleware (JWT or OAuth2 assumed but [NEEDS VERIFICATION
    — deferred: low impact for scoring; specific auth standard not specified in elicitation
    and is org-internal]); secrets management (AWS Secrets Manager or similar [NEEDS
    VERIFICATION — deferred: low impact for scoring]); input validation via Pydantic/DTO
    layer.'
  database_conventions: 'PostgreSQL as primary; Alembic migration tooling likely [NEEDS
    VERIFICATION — deferred: low impact for scoring; Alembic is the standard migration
    tool for SQLAlchemy but org-specific confirmation requires stakeholder elicitation];
    MySQL for secondary Spring Boot stack.'
  deployment_conventions: 'Docker multi-stage builds expected; Kubernetes manifests
    (Deployments, Services, ConfigMaps, Secrets); Terraform for AWS infrastructure
    provisioning (VPC, EKS, RDS patterns assumed [NEEDS VERIFICATION — deferred: low
    impact for scoring]).


    Net-new IaC finding: Two dedicated benchmarks now exist for NL-to-IaC evaluation.
    IaC-Eval (Kon et al. 2024) covers Terraform/HCL generation against AWS services,
    using OPA Rego intent specifications for correctness validation beyond syntax.
    DPIaC-Eval (2025) adds 153 real-world AWS tasks with deployability, intent-matching,
    and security dimensions; it finds mainstream LLMs achieve only ~50% success even
    on simplest scenarios, and that 42.7% of syntactically correct templates fail
    actual deployment. Multi-IaC-Eval (arXiv 2409) covers CloudFormation, Terraform,
    and CDK. These benchmarks are directly relevant as supplementary evaluation candidates
    for the deployment config layer.

    Sources: IaC-Eval — [WEB-4];
    DPIaC-Eval arXiv 2506.05623 — [WEB-5]; Multi-IaC-Eval
    arXiv 2509.05303 — [WEB-6]'
  non_functional_requirements: NFRs (SLA constraints, performance targets, compliance
    requirements) appear in PRD sections; LLM must surface these in generated scaffolding
    (e.g., connection pooling config, rate limiting middleware, CORS settings).
  frontend_conventions: 'Next.js App Router or Pages Router [NEEDS VERIFICATION —
    deferred: low impact for scoring; specific routing paradigm not confirmed]; TypeScript
    strict mode assumed; component stub conventions (prop interfaces, placeholder
    return JSX) [NEEDS VERIFICATION — deferred: low impact for scoring].'
benchmark_population_match:
  geographic_match: Exact — HumanEval is US/Anglophone-origin; deployment population
    is US-based.
  language_match: Partial — English NL match is exact; HumanEval covers only Python,
    while deployment requires Python, SQL, TypeScript, Java, YAML, HCL.
  occupational_match: Poor — HumanEval's implicit target is competitive programmers
    / interview candidates; deployment population is senior enterprise architects
    evaluating multi-layer scaffolding.
  task_match: Very poor — HumanEval covers only isolated single-function Python synthesis;
    deployment requires multi-artifact, multi-language, multi-layer, rubric-graded
    scaffolding generation.
  input_form_match: Very poor — HumanEval inputs are short docstrings (~1–5 sentences);
    deployment inputs are 3–10 page semi-structured PRDs.
  output_form_match: Poor — HumanEval outputs are single Python functions evaluated
    by binary unit tests; deployment outputs are multi-file project trees graded by
    rubric.
flagged_gaps_for_web_search:
- gap_id: 1
  label: Multi-artifact / multi-language code generation benchmarks
  search_targets:
  - SWE-bench
  - CoderEval
  - DevEval
  - APIBench
  - RepoEval
  - Spider (SQL)
  - multi-artifact scaffolding evaluation LLM
  priority: HIGH
  resolution_status: RESOLVED
  findings: 'Several repository-level and multi-stage benchmarks now exist that partially
    address this gap, though none cover the full four-layer enterprise scaffolding
    profile:


    1. SWE-bench (Jimenez et al. 2024): 2,294 GitHub issue-PR pairs from 12 Python
    repositories; evaluates multi-file patch generation against execution-based validation.
    Highly cited as the de-facto standard for repository-level coding agents. Caveat:
    limited to Python bug-fixing, not scaffolding generation from requirements. Current
    SOTA achieves ~75% on SWE-bench Verified (GPT-5). Source: SWE-bench ICLR 2024
    — [WEB-7]; emergentmind SWE-bench+ overview — [WEB-8]


    2. SWE-bench++ (arXiv 2512.17419): Scalable pipeline generating 11,133 instances
    from 3,971 repositories across 11 languages including TypeScript, Java, and Go;
    addresses Python-centrism of original. Relevant for multi-language coverage but
    still issue-resolution-oriented, not scaffolding-from-spec. Source: arXiv 2512.17419
    — [WEB-9]


    3. DevEval (ACL 2024 Findings): 1,825-sample repository-level code generation
    benchmark with comprehensive annotations (natural language requirements, original
    repos, ground-truth dependencies); proposes Recall@k for dependency accuracy alongside
    Pass@k. Closer to real-world repo structure than HumanEval but still Python-centric
    and does not cover IaC or frontend stubs. Source: ACL Anthology 2024 — [WEB-10];
    arXiv 2405.19856 — [WEB-11]


    4. DevBench (arXiv 2403.08604): Evaluates LLMs across the full software development
    lifecycle — software design, environment setup, implementation, acceptance testing,
    and unit testing — across four programming languages. Empirical studies show GPT-4-Turbo
    fails to solve DevBench challenges, revealing LLM struggles with complex repository
    structures. Most aligned with the multi-stage nature of the scaffolding task.
    Source: arXiv 2403.08604 — [WEB-12]


    5. FrontendBench (arXiv 2506.13832): Specialized benchmark for front-end code
    generation emphasizing user interactivity and dynamic behavior; addresses gap
    in frontend evaluation not covered by general code benchmarks. Source: arXiv 2506.13832
    — [WEB-13]


    Critical gap remaining: No benchmark covers the composite four-layer scaffolding
    profile (DB schema + API routes + frontend stubs + IaC) generated from multi-page
    PRD-style inputs. DevBench is the closest candidate but lacks IaC and framework-specific
    (FastAPI/Spring Boot) coverage.'
- gap_id: 2
  label: Rubric-based architectural correctness evaluation frameworks
  search_targets:
  - LLM-as-judge code quality rubric
  - CodeScore
  - enterprise code review automated evaluation
  - architectural convention adherence LLM assessment
  priority: HIGH
  resolution_status: RESOLVED
  findings: 'Rubric-based LLM-as-judge evaluation is now a well-established methodology,
    with multiple validated frameworks:


    1. Prometheus / Prometheus 2 (Kim et al. 2023/2024): Open-source evaluator LMs
    specialized in rubric-conditioned scoring. Prometheus 2 supports both pointwise
    and pairwise ranking with user-defined evaluation criteria, achieving highest
    correlation with human and GPT-4 judgments among open evaluator models across
    four direct-assessment and four pairwise-ranking benchmarks. Directly applicable
    as a judge model if the org''s architecture guide is encoded as a structured rubric.
    Source: arXiv 2405.01535 — [WEB-14]; GitHub prometheus-eval
    — [WEB-15]


    2. TRACE framework (arXiv 2603.24586): Identifies 35 significant misalignment
    sources between LLM judges and human developers across code quality dimensions.
    Finds LLM judges are biased toward longer code explanations while humans prefer
    shorter ones — a validity concern for automated rubric scoring of enterprise scaffolding.
    Source: arXiv 2603.24586 — [WEB-16]


    3. Research consensus (2024–2026): Anthropic''s guidance for coding agents explicitly
    recommends combining unit tests for correctness with LLM rubrics for overall code
    or interaction quality. Rubrics improve reliability when the task is open-ended
    and the rubric is explicit, criterion-separated, and calibrated. Source: Medium
    rubric-based evals analysis — [WEB-17]


    Key caveat: No existing rubric-based framework has been validated specifically
    for enterprise architectural convention adherence (naming conventions, folder
    structure, auth patterns). The org would need to encode its internal architecture
    guide as a structured Prometheus-style rubric and validate judge calibration against
    a small human-annotated gold set before using automated scoring.'
- gap_id: 3
  label: Long-context document-to-code generation benchmarks
  search_targets:
  - PRD to code generation benchmark
  - requirements document code generation LLM
  - long-context code generation evaluation user stories specification
  priority: HIGH
  resolution_status: PARTIALLY RESOLVED
  findings: 'No benchmark specifically evaluates code generation from multi-page PRD/Confluence-style
    documents. Relevant findings:


    1. LongCodeBench (arXiv 2505.07897, 2025): Evaluates coding LLMs at up to 1M-token
    context windows on real-world codebase comprehension and bug-fixing tasks. Documents
    dramatic performance degradation — Claude 3.5 Sonnet drops from 29% to 3% as context
    length increases in coding tasks. Covers code comprehension and completion, not
    spec-to-scaffolding generation. Source: arXiv 2505.07897 — [WEB-3]


    2. LoCoBench (arXiv 2509.09614): Long-context code benchmark; explicitly notes
    that existing benchmarks ''primarily emphasize code completion and comprehension
    tasks rather than complex software development workflows.'' Confirms the spec-to-code
    gap. Source: arXiv 2509.09614 — [WEB-18]


    3. DevBench''s software design stage involves reading structured requirements
    and generating multi-file implementations, making it the closest available analog
    to the PRD-to-scaffolding workflow, but inputs are not 3–10 page semi-structured
    documents. Source: arXiv 2403.08604 — [WEB-12]


    Conclusion: No PRD-to-code benchmark exists. This is a confirmed evaluation gap.
    The performance degradation data from LongCodeBench (29%→3% for Claude 3.5 Sonnet)
    provides strong quantitative justification for flagging long-context input form
    as a high-severity validity concern.'
- gap_id: 4
  label: FastAPI / Spring Boot / SQLAlchemy / Pydantic framework-specific evaluation
  search_targets:
  - FastAPI code generation benchmark
  - SQLAlchemy ORM generation LLM
  - Spring Boot code generation evaluation
  - framework-specific LLM code quality
  priority: HIGH
  resolution_status: NOT FOUND — searched via general repository-level benchmark literature
    (SWE-bench, DevEval, DevBench surveys); no benchmark specifically targeting FastAPI,
    SQLAlchemy, Pydantic, or Spring Boot idiom generation was identified. This remains
    a confirmed gap. Framework-specific evaluation would require custom benchmark
    construction using org-internal PRDs and architecture guide as ground truth.
- gap_id: 5
  label: Multi-file project coherence evaluation
  search_targets:
  - multi-file code generation coherence evaluation
  - repository-level LLM code generation
  - cross-file consistency benchmark
  - SWE-bench RepoEval import graph coherence
  priority: HIGH
  resolution_status: PARTIALLY RESOLVED
  findings: 'Repository-level benchmarks (SWE-bench, DevEval) implicitly require cross-file
    consistency but do not explicitly score it as a distinct dimension. DevEval introduces
    Recall@k for dependency accuracy (measuring whether generated code correctly invokes
    elements defined in the repository), which is the closest published metric to
    import-graph coherence. However, no benchmark explicitly scores entity-model alignment
    across DB schema, API models, and frontend prop types as required by the enterprise
    scaffolding task. DevBench''s ''implementation'' stage evaluates multi-file output
    against acceptance and unit tests, providing an execution-based proxy for coherence
    but not a dedicated cross-layer consistency metric.

    Sources: DevEval arXiv 2405.19856 — [WEB-11]; DevBench
    arXiv 2403.08604 — [WEB-12]


    Conclusion: Cross-layer type consistency (schema ↔ API model ↔ frontend props)
    remains an unmet evaluation need. Recommendation: custom coherence checks (e.g.,
    automated schema diffing across generated artifact layers) would need to be implemented
    as part of a bespoke evaluation harness.'
- gap_id: 6
  label: Deployment configuration / IaC generation correctness
  search_targets:
  - Dockerfile generation LLM benchmark
  - Kubernetes manifest generation evaluation
  - Terraform IaC generation correctness
  - OPA Checkov static analysis IaC LLM
  - infrastructure-as-code benchmark
  priority: HIGH
  resolution_status: RESOLVED
  findings: 'IaC generation evaluation is now an active research area with dedicated
    benchmarks:


    1. IaC-Eval (Kon et al. 2024): First dedicated Terraform/HCL benchmark; uses OPA
    Rego intent specifications for correctness validation beyond syntax; covers wide
    range of AWS services. State-of-the-art models achieve <20% pass@1 on compositional
    IaC requirements. Source: IaC-Eval description — [WEB-4]


    2. DPIaC-Eval (arXiv 2506.05623, 2025): 153 real-world AWS infrastructure tasks;
    validates across syntax correctness, deployability, user intent matching, and
    security. Finds 42.7% of syntactically correct templates fail deployment, and
    mainstream LLMs achieve only ~50% on simplest scenarios. Source: arXiv 2506.05623
    — [WEB-5]


    3. Multi-IaC-Eval (arXiv 2509.05303): Covers CloudFormation, Terraform, and CDK;
    uses CFN-Lint and Checkov for static analysis validation. Syntactic pass rates
    exceed 95% for top models but semantic/deployability accuracy remains a key gap.
    Source: arXiv 2509.05303 — [WEB-6]


    4. TerraFormer (arXiv 2601.08734, 2026): Addresses IaC mutation (modifying existing
    configs via NL) in addition to generation; notes real-world IaC is rarely shared
    publicly, limiting LLM domain-specific training. Source: arXiv 2601.08734 — [WEB-19]


    Key validity concern: LLM IaC generation performance on real-world compositional
    requirements (VPC + EKS + RDS patterns, as assumed for this deployment) is documented
    to be substantially lower than on simple isolated resource tasks. IaC-Eval and
    DPIaC-Eval are directly usable as supplementary benchmarks for the deployment
    configuration layer.'
- gap_id: 7
  label: Current market share and usage statistics for tech-hub concentration and
    enterprise LLM adoption
  search_targets:
  - enterprise software architect LLM adoption rate US 2024
  - LLM code generation enterprise survey
  - US tech hub remote work distribution software engineers
  priority: LOW
  resolution_status: RESOLVED
  findings: 'AI tool adoption in the enterprise software engineering cohort is now
    well-documented:

    - Stack Overflow 2025 Developer Survey: 80% of developers use AI tools in workflows;
    trust in AI accuracy has fallen to 29% (from 40% prior years); experienced developers
    show highest distrust rate (20% ''highly distrust''). Source: [WEB-1]

    - Gartner (July 2025): Predicts 90% of enterprise software engineers will use
    AI code assistants by 2028, up from <14% in early 2024. Source: [WEB-2]

    - Menlo Ventures 2025: Enterprise generative AI spend reached $37B in 2025 (3.2x
    YoY); code generation is described as ''AI''s first breakout use case.'' Anthropic
    holds ~40% of enterprise LLM spend for 2025, with Claude Sonnet models preferred
    by professional developers (45% usage). Source: [WEB-20]

    - Full-stack developers lead AI coding tool adoption at 32.1%. Source: secondtalent.com
    AI coding stats — [WEB-21]'
net_new_fields:
  enterprise_ai_adoption_risk_signal:
    label: Enterprise AI code review burden finding
    finding: 'Analysis of telemetry from 10,000+ developers across 1,255 teams finds
      that AI-assisted developers merge 98% more PRs but PR review time increases
      91%, with a 322% increase in privilege escalation paths and 153% increase in
      architectural flaws in AI-generated code. This ''AI productivity paradox'' directly
      affects the validity assessment: architects evaluating LLM scaffolding in this
      deployment will likely encounter not just functional errors but architectural
      flaw patterns that automated scanners miss.'
    validity_dimension: OC — Output Content
    source: Faros.ai enterprise AI coding adoption analysis 2025 — [WEB-22]
  iac_generation_performance_baseline:
    label: Quantitative IaC generation performance floor
    finding: State-of-the-art LLMs achieve less than 20% pass@1 on compositional IaC
      requirements (IaC-Eval), and only ~50% success on the simplest DPIaC-Eval scenarios.
      42.7% of syntactically correct Terraform/CloudFormation templates fail actual
      deployment validation. This provides a quantitative performance floor for the
      deployment configuration layer that is materially lower than pass rates on Python
      coding tasks.
    validity_dimension: OO — Output Ontology
    sources: IaC-Eval — [WEB-4];
      DPIaC-Eval arXiv 2506.05623 — [WEB-5]
  long_context_code_degradation_quantitative:
    label: Quantitative long-context code performance degradation
    finding: LongCodeBench (2025) documents Claude 3.5 Sonnet dropping from 29% to
      3% accuracy as context length increases on coding tasks. This quantitative degradation
      rate is directly relevant to the deployment's 3–10 page PRD inputs and confirms
      that HumanEval short-docstring performance is not a valid predictor of PRD-length
      input performance.
    validity_dimension: IF — Input Form
    source: LongCodeBench arXiv 2505.07897 — [WEB-3]
  devbench_multi_stage_relevance:
    label: DevBench as nearest available multi-stage analog
    finding: DevBench (Li et al. 2024, arXiv 2403.08604) is the closest publicly available
      benchmark to the deployment's multi-stage scaffolding task, covering software
      design, environment setup, implementation, acceptance testing, and unit testing
      across four programming languages. Empirical studies show current LLMs including
      GPT-4-Turbo fail to solve DevBench challenges, with models struggling specifically
      with complex repository structures and compilation management — directly relevant
      failure modes for the scaffolding use case.
    validity_dimension: IO — Input Ontology
    source: DevBench arXiv 2403.08604 — [WEB-12]
  prometheus2_rubric_judge_applicability:
    label: Prometheus 2 as candidate rubric judge for architectural conventions
    finding: Prometheus 2 (Kim et al. 2024, arXiv 2405.01535) is an open-source evaluator
      LM supporting user-defined evaluation criteria in both pointwise and pairwise
      formats, achieving the highest human-agreement scores among open evaluator models.
      It can in principle be applied to score LLM scaffolding against a structured
      encoding of the org's internal architecture guide. However, TRACE research (arXiv
      2603.24586) identifies 35 LLM-judge / human-developer misalignment sources,
      requiring calibration against human-annotated gold examples before automated
      scoring can be trusted for architectural convention adherence.
    validity_dimension: OO — Output Ontology
    sources: Prometheus 2 arXiv 2405.01535 — [WEB-14];
      TRACE arXiv 2603.24586 — [WEB-16]
  developer_resistance_to_ai_on_deployment_tasks:
    label: Developer resistance to AI on high-responsibility deployment and architecture
      tasks
    finding: Stack Overflow 2025 Developer Survey reports that 76% of developers do
      not plan to use AI for 'Deployment and monitoring' tasks, and 69% do not plan
      to use AI for 'Project planning.' This resistance is highest among experienced
      developers and directly reflects the population likely to be evaluating scaffolding
      outputs for deployment configuration correctness in the enterprise target cohort.
    validity_dimension: OC — Output Content
    source: Stack Overflow Developer Survey 2025 — [WEB-1]
```

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

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: HumanEval covers standalone Python functions in isolation. Your task involves multi-file, multi-layer artifacts: database schemas (SQL/ORM), REST or GraphQL API route definitions, frontend component stubs (React, Vue, etc.), and deployment configs (Docker, Kubernetes, Terraform). Does your evaluation need to cover all of these artifact types, or are some layers more critical to validate than others? Are there specific technology stacks your architects work with most?
A1: All four layers must be covered since the value proposition is end-to-end scaffolding, but the database schema and API route layers are the most critical — they are hardest to refactor post-generation. Primary stack is FastAPI + PostgreSQL + React/Next.js; secondary stack is Spring Boot + MySQL + Angular. Deployment targets Docker + Kubernetes on AWS, with occasional Terraform use.

Q2 [OO]: HumanEval scores outputs by running unit tests against a single correct function — binary pass/fail. For your scaffolding task, what does 'correct' mean: syntactic validity, requirements satisfaction, architectural convention adherence? Do architects accept multiple valid designs or grade against a house style?
A2: Correctness is layered: outputs must parse/compile and pass linting, satisfy stated requirements (entities, endpoints, flows present), and conform to internal conventions (naming, folder structure, auth middleware patterns, error handling). Multiple valid designs are acceptable, but a codified internal architecture guide serves as the grading rubric. Evaluation is closer to rubric-based expert review than binary unit-test pass/fail.

Q3 [IF]: HumanEval inputs are concise, self-contained docstrings. How long and structured are your requirements documents, and does the LLM receive them whole or in chunks?
A3: Specs are typically 3–10 page Confluence documents or PRDs with consistent headings (business context, user stories, data entities, API expectations, non-functional requirements) but variable prose under each section. The full document is currently fed in a single prompt; section-by-section prompting has been explored for larger specs.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | HumanEval's ontology covers only isolated single-function Python synthesis; the deployment requires multi-artifact, multi-language, multi-layer scaffolding across at minimum four structurally distinct output types, leaving most of the task's input category space completely unrepresented. |
| IC | HIGH | HumanEval instances are algorithm/interview-style problems with no enterprise conventions, framework-specific idioms, or business-logic complexity; the deployment's inputs embed compliance requirements, SLA constraints, and domain-specific data models that are categorically absent from the benchmark's item pool. |
| IF | HIGH | HumanEval inputs are short, self-contained docstrings; deployment inputs are 3–10 page semi-structured PRDs fed as long single-context prompts, representing a fundamentally different input distribution in length, structure, and information density. |
| OO | HIGH | HumanEval's output space is a single Python function evaluated by deterministic unit tests (binary correctness); the deployment's output space is a multi-file, multi-language artifact set graded by rubric against architectural conventions, making the scoring function categorically incompatible. |
| OC | HIGH | HumanEval ground-truth labels are unit-test pass/fail on algorithm problems; the deployment's "correct" labels require expert architectural judgment against an internal style guide, meaning HumanEval label correctness is entirely inapplicable to the deployment task. |
| OF | MODERATE | Both benchmark and deployment use text-in / code-out modality, which limits mismatch at the signal level; however, HumanEval outputs a single function file while the deployment expects multi-file project trees across several languages and frameworks, creating a structural output-form gap that is non-trivial but less severe than the ontology and content mismatches. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

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

---

## Framework Dimensions to Evaluate

### Input Ontology

**Definition**: The input data ontology consists of the set of test case categories represented by the benchmark, which should cover the query types that evaluated systems are expected to encounter during deployment (e.g., factual questions, creative writing help, or restaurant recommendations for NLP dialogue systems; pick-and-place tasks, point navigation, or planning for robotics).

**Theoretical Importance**: A misalignment in this taxonomy — whether through the omission of necessary categories (construct underrepresentation) or the inclusion of irrelevant ones (construct-irrelevant variance) — harms the content validity of the benchmark.

**Checklist:**
- [IO-1] Identify test case categories required for regional deployment.
- [IO-2] Check if source benchmark's taxonomy omits regionally-relevant categories.
- [IO-3] Check if source benchmark includes categories irrelevant to regional context.
- [IO-4] Document category gaps that would harm content validity.

### Input Content

**Definition**: Whereas the ontology defines the types of input queries, the content of dataset inputs refers to the explicit instances specified by individual datapoints — an LLM prompt, an image, a database entry, etc.

**Theoretical Importance**: Even when the test case taxonomy provides good coverage, implementation-level details of individual datapoints can introduce construct-irrelevant variance, violating content validity.

**Checklist:**
- [IC-1] Determine if input queries require region-specific cultural, geographic, or dialectal knowledge.
- [IC-2] Assess whether culturally sensitive content aligns with target deployment culture.
- [IC-3] Flag inputs requiring Western-specific knowledge that may not transfer.
- [IC-4] Recruit regional annotators to identify culturally sensitive instances if resources permit.
- [IC-5] Document content issues that would harm content validity.

### Input Form

**Definition**: The form of dataset inputs determines the encoding of the input signal — e.g., text vs. audio for natural language, or camera parameters such as focal length and resolution for visual data.

**Theoretical Importance**: Since machine learning systems are sensitive to signal distributions, a mismatch between the benchmark's input representation and the real-world signals that deployed models would encounter violates the external validity of the evaluation.

**Checklist:**
- [IF-1] Compare signal distributions (e.g., image resolution, MRI field strength) between source and target contexts.
- [IF-2] Check if regional infrastructure supports the same data capture specifications.
- [IF-3] Identify domain-specific form differences relevant to the intended use case.
- [IF-4] Document form mismatches that would harm external validity.

### Output Ontology

**Definition**: A benchmark's output ontology determines the space of outputs an AI system is expected to produce and the decision rules by which those outputs are organized and scored — i.e., the benchmark's criteria. For categorical outputs, the mapping is direct (e.g., safe/unsafe, or object class labels). For free-form outputs, the scoring function must first interpret what the output means before mapping it to a score — and this interpretive step is where validity violations most readily arise, since decision rules can differ across cultural contexts. For instance, an LLM recommending "red wine" for a dinner party may score highly for helpfulness in a Western context but poorly where alcohol consumption is prohibited.

**Theoretical Importance**: A misaligned output taxonomy thus violates structural validity (the construct's structure is misrepresented), content validity (through missing or irrelevant categories), and risks violating external validity (benchmark performance is less likely to generalize to regional settings).

**Checklist:**
- [OO-1] Review output label categories for regional relevance.
- [OO-2] Identify missing categories specific to regional contexts (e.g., autorickshaws in Indian driving data).
- [OO-3] Flag categories that encode non-regional values or assumptions.
- [OO-4] Consider stakeholder-driven taxonomy redesign if significant misalignment exists.
- [OO-5] Document taxonomy issues that would harm structural validity and content validity.

### Output Content

**Definition**: Whereas taxonomic alignment addresses whether abstract decision boundaries reflect regional values, label correctness concerns whether the labels for particular datapoints correlate with the judgments of regional stakeholders.

**Theoretical Importance**: Disagreement between regional and original annotators violates both convergent validity (the labels fail to correlate with regional perspectives on the construct) and external validity (the original judgments do not generalize to the target context).

**Checklist:**
- [OC-1] Determine if ground truth labels reflect regional stakeholder perspectives.
- [OC-2] Assess potential disagreement between original annotators and regional population.
- [OC-3] Review annotator demographics in benchmark documentation (Datasheets, Data Statements).
- [OC-4] Consider label re-annotation by representative regional annotator pool.
- [OC-5] Review aggregation methods for potential erasure of minority perspectives.
- [OC-6] Document label issues that would harm convergent validity and external validity.

### Output Form

**Definition**: The form of dataset outputs pertains to the representation of output signals models are expected to produce.

**Theoretical Importance**: If a benchmark does not evaluate models on the output forms encountered during real-world deployment, this violates the external validity of the evaluation.

**Checklist:**
- [OF-1] Check if expected output modality matches regional deployment needs.
- [OF-2] Assess text-to-speech availability for speech-based output requirements.
- [OF-3] Consider literacy rates and accessibility requirements in target population.
- [OF-4] Document form mismatches that would harm external validity.


---

## Required Output Format

Output a single valid JSON object with this structure:

```json
{
  "benchmark": "humaneval",
  "region": "US Enterprise Software Architects — Full-Stack Scaffolding Generation",
  "dimensions": {
    "input_ontology": {
      "score": "<integer 1-5>",
      "justification": "...",
      "strengths": ["what this dimension captures well for the target context"],
      "checklist_responses": { "IO-1": "...", "IO-2": "..." },
      "evidence_quotes": ["[Q1] 'quote text' (p.7)", ...],
      "evidence_web_sources": ["[WEB-1] literacy rate 96%", ...],
      "evidence_dataset": ["DATASET-D1: observation", ...],
      "evidence_map": { "IO-1": ["Q1", "WEB-3"], "IO-2": ["DATASET-D1"] },
      "confidence": "<high|medium|low>",
      "information_gaps": ["..."],
      "requires_expert_verification": ["..."]
    },
    "input_content": { "..." },
    "input_form": { "..." },
    "output_ontology": { "..." },
    "output_content": { "..." },
    "output_form": { "..." }
  },
  "overall_summary": "...",
  "risk_assessment": "<high|medium|low>",
  "practical_guidance": {
    "what_this_benchmark_measures": "...",
    "construct_depth": "...",
    "supplementation_needed": "..."
  },
  "remediation_suggestions": [
    { "dimension": "...", "gap": "...", "recommendation": "..." }
  ],
  "highest_concern_dimensions": ["..."],
  "strongest_dimensions": ["..."]
}
```
