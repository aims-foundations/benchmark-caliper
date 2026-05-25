I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **HumanEval: Hand-Written Evaluation Set for Python Code Generation** is valid for use in **US Professional Software Development Teams — Code Review / Bug Localization**.

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
- **Languages**: en, python
- **Porting Strategy**: none
- **Year**: 2021

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
HumanEval's task taxonomy is narrowly defined around clean docstring-to-function synthesis:
the model receives a natural language docstring and must produce a functionally correct Python
function body [Q1, Q22]. The paper describes the problems as assessing "language comprehension,
reasoning, algorithms, and simple mathematics" [Q22] — a scope mapping to competitive
programming and interview-style tasks rather than real-world software engineering. A secondary
task of generating docstrings from code bodies (Codex-D) is evaluated [Q133], and a supervised
fine-tuning variant (Codex-S) draws on problems from competitive programming sites [Q49, Q51]
and CI-traced repositories [Q54, Q55, Q62]. Appendix D proposes a qualitative taxonomy of
specification complexity including variable interdependencies [Q153], temporal reasoning [Q154],
and concurrency [Q155], and evaluates bias-relevant generation probes for gender [Q186, Q187],
race [Q188], and cryptographic security [Q204, Q205].

Critically, the benchmark contains no tasks involving bug localization in existing code,
defect identification, or diff generation against a buggy function body. The APPS dataset
is benchmarked as a comparison, but its tasks are full-program synthesis from stdin/stdout [Q46],
also not code repair. Codex-S tracing data targets "building blocks of command-line utilities"
where "the model does not need to know advanced algorithms and data structures" but must "follow
instructions to implement the functionality specified in the docstring" [Q60, Q61] — still
generation-from-spec, not defect-detection. The paper explicitly acknowledges that "most past
studies of the impacts of code generation models consider performance on a closed set of tasks
in a simulated environment" [Q225], flagging the gap between benchmark task taxonomy and
real-world deployment diversity.

### Input Content
HumanEval consists of 164 hand-written problems explicitly designed to avoid overlap with
GitHub training data [Q14, Q19]. The training corpus was scraped from 54 million public GitHub
repositories (179 GB raw, 159 GB filtered) [Q23, Q25], but the evaluation inputs are
sanitized hand-crafted problems rather than representative samples of that distribution.
Codex-S training data was sourced from competitive programming websites [Q51, Q52] and
GitHub CI-integrated projects [Q54, Q55, Q57], but these remain algorithm-puzzle and
utility-building-block inputs rather than real-world framework-heavy code. The paper
acknowledges a distribution mismatch: "Python code found on GitHub contains class
implementations, configuration files, scripts, and even files used to store data. This code
is seemingly unrelated to synthesizing functions from docstrings, and we hypothesize that
the distribution mismatch reduces HumanEval performance" [Q48]. The alignment evaluation
appendix notes that the GitHub training data "contains plenty of poor-quality code" including
"off-by-one errors or single-character typographic errors" [Q167] — but this characterizes
the training distribution, not the benchmark's evaluation inputs, which remain clean and
well-specified.

No HumanEval problems involve Django views, Flask routing, SQLAlchemy ORM patterns,
NumPy/pandas pipelines, or legacy internal utilities with sparse or stale documentation —
the actual input distribution of the target deployment. The paper notes that Codex "struggles
to parse through increasingly long and higher-level or system-level specifications" [Q88] and
that "intent is [not always] captured sufficiently enough in comments and documentation"
[Q217], gesturing toward the relevance of missing or misleading documentation without
evaluating it.

### Input Form
HumanEval inputs are formatted as plain-text Python prompts comprising a function signature,
docstring, and body prefix, with stop sequences applied to prevent generation beyond the
function boundary [Q20, Q29]. Training data was filtered to remove likely auto-generated
files, those with excessively long lines, or those with a low proportion of alphanumeric
characters [Q24]. For Codex-S, prompts are assembled in a standardized format with
left-padding for batch alignment [Q68, Q69]. The alignment evaluation constructs prompts by
prepending correct or subtly-buggy example solutions to task docstrings [Q172, Q173, Q174,
Q175, Q177], with stateful or non-deterministic problems filtered out [Q66].

Both the benchmark and the target deployment operate on plain-text Python source code, with
no modality mismatch (no audio, image, or non-Python-script concerns). The primary format
divergence is structural: HumanEval assumes a clean, accurate docstring as the primary
signal [Q20], whereas deployment inputs frequently lack docstrings or have misleading ones.
This is a content-level concern (addressed under Input Content) rather than a form-level
mismatch. NOT DOCUMENTED: no evaluation of model behavior on inputs with absent, stale, or
incorrect inline comments, which is a primary real-world condition for the target deployment.

### Output Ontology
HumanEval's output taxonomy is binary functional correctness: a generated function either
passes all unit tests or it does not [Q8, Q77]. This is operationalized via the pass@k metric,
where k code samples are generated per problem and the problem is considered solved if any
sample passes [Q13, Q15, Q36]. The paper argues that functional correctness is superior to
match-based metrics like BLEU, since BLEU scores of functionally incorrect solutions
significantly overlap those of correct ones [Q9, Q10, Q40, Q123]. For docstring generation
(Codex-D), labels are assigned by human graders who consider a docstring correct "if it
uniquely and accurately specifies the code body," explicitly excluding cases where "the model
simply copies the code body" [Q81]. For cryptographic security evaluation, labels are defined
by specific technical thresholds: RSA keys shorter than 2048 bits are considered improperly
configured [Q208], and AES contexts using ECB mode are considered insecure [Q209]. Appendix D
proposes richer qualitative metrics covering specification abstraction levels and complexity
dimensions [Q148, Q149], but describes these as preliminary and deferred to a forthcoming paper.

For the target deployment, the binary pass/fail output ontology is fundamentally misaligned.
The deployment requires a multi-component output judgment: correct localization of the defective
line or block, a proposed diff that is semantically safe, convention-adherent, and not
bug-masking, and overall human reviewer acceptance. A fix that passes existing tests can be
rejected; a fix with no test coverage can be correct if reviewers accept it. The paper
explicitly acknowledges pass@k's oracle-selection problem [Q36, Q37, Q38] and the gap between
test-passing and developer-intent satisfaction [Q102, Q103, Q104], but proposes no output
taxonomy that captures localization accuracy, diff quality, or reviewer acceptability.

### Output Content
Annotation for HumanEval ground truth is minimal by design: problems are hand-written by the
authors, and correctness is determined by automated unit test execution rather than human
judgment [Q14, Q77]. The one exception is docstring generation (Codex-D), where human graders
assessed 10 samples per problem for 1,640 total graded items from a single model configuration
at a single temperature [Q79]. For the alignment evaluation, the annotation process involved
researchers constructing prompts with subtly buggy solutions and assuming the model could
detect an explicit instruction to "write correct code" [Q164]. The paper does not document
annotator demographics, inter-annotator agreement procedures, or any quality assurance process
beyond author judgment. It explicitly acknowledges that "there is unfortunately only limited
research on the demographic distribution of Python users" [Q219], limiting assessment of
disparate impacts.

For the target deployment, the absence of professional software developer annotation is a
significant validity gap. HumanEval's "annotators" are benchmark authors writing unit tests,
not independent professional developers evaluating code quality, convention adherence, or
semantic correctness against real-world reviewer standards. The paper acknowledges that
"human developers often write test suites with limited but targeted coverage, but this does
not always work well against an algorithm" [Q129], and that some prompts "underspecify the
function that is implemented, in which case a perfectly valid solution may be wrongly penalized
by the unit test" [Q63] — evidence that even the benchmark's own ground truth labels are not
fully reliable. NOT DOCUMENTED: any label validation by professional developers representing
the target population of US software engineers.

### Output Form
The primary output form evaluated is complete Python function bodies generated token-by-token,
with stop sequences applied to prevent generation beyond the function boundary [Q29]. The
metric is pass@k computed via an unbiased combinatorial estimator [Q15, Q16, Q17, Q138, Q139],
with temperature tuning playing an important role [Q32, Q33, Q34]. The paper also evaluates
mean log-probability ranking as a heuristic for selecting among k samples without oracle access
[Q39, Q76], and BLEU score as a negative example of an inadequate output form metric [Q9, Q40,
Q123]. For docstring generation, hand-graded pass rates are reported [Q84]. For bias and
security evaluations, output form metrics include word co-occurrence rates [Q189, Q190, Q191,
Q194] and rates of insecure cryptographic configurations [Q198, Q199, Q200, Q202, Q210, Q214].

For the target deployment, HumanEval's output form is partially aligned: both involve Python
code as output. However, HumanEval produces complete standalone function bodies starting from
a clean prompt, whereas the deployment requires targeted diffs that identify a specific
defective region and propose a minimal corrective change — a structurally different output
form with its own representation requirements (e.g., unified diff format, line-range
localization metadata). The paper acknowledges the practical single-completion challenge
[Q37, Q38] but proposes only a mean-log-probability heuristic [Q39] rather than any output
form designed for diff generation or localization. NOT DOCUMENTED: any evaluation of output
form requirements for code repair, patch generation, or line-range defect localization.


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

## Regional Context

```yaml
name: US Professional Software Development Teams — Code Review / Bug Localization
abbreviation: US-SWE-CODE-REVIEW
deployment_context:
  description: A US-based code review platform deploying an LLM to scan existing Python
    codebases, localize bugs (logic errors, off-by-one, null dereferences), and propose
    concrete diffs that developers can accept or reject during code review.
  platform_type: Code review SaaS — integrated LLM assistant surfacing diff suggestions
    inline during pull request or code review workflows.
  user_role: Professional software developers on American development teams, acting
    as code reviewers who accept or reject proposed fixes.
  geography: United States
  sub_national_variation: Not a primary concern; the relevant heterogeneity is codebase
    style, framework diversity, and documentation quality rather than geography or
    demographics.
target_population:
  primary_users: Professional software engineers (SWEs) on US-based development teams,
    ranging from individual contributors performing code review to senior engineers
    evaluating semantic correctness and convention adherence of proposed diffs.
  relevant_heterogeneity:
  - Codebase style variation (Google-style, PEP 8-strict, legacy pre-PEP8, auto-formatted)
  - Framework diversity (Django, Flask, SQLAlchemy, NumPy/pandas, internal utility
    layers)
  - Documentation density (well-docstringed libraries vs. sparsely or misleadingly
    documented legacy code)
  - Code quality spectrum (greenfield clean code vs. decade-old internal utilities
    with cryptic naming)
  - Team size and review process maturity (formal PR gates vs. informal review)
  excluded_variation: Sub-national, demographic, linguistic, and literacy variation
    is not a primary assessment concern for this deployment.
languages:
  programming:
  - Python (primary — all deployment inputs are Python source code)
  - Python 3.x mainstream (Django, Flask, SQLAlchemy, NumPy, pandas, Celery, pytest
    ecosystems)
  - Python 2.x legacy (present in older internal utilities; EOL but still encountered
    in customer repos)
  natural_language:
  - English (primary — code comments, docstrings, variable names, PR descriptions)
  documentation_quality_spectrum:
    well_documented: Clean docstrings, type annotations, inline comments — rare in
      legacy code, common in public-facing libraries
    sparsely_documented: Minimal or absent docstrings, single-letter variable names,
      terse inline comments
    misleadingly_documented: Stale docstrings that no longer match implementation,
      comments describing removed behavior, misleading parameter descriptions — common
      in long-lived internal utilities
frameworks_and_libraries:
  web_frameworks:
  - Django (ORM, views, middleware, signals, migrations)
  - Flask (routing, request context, blueprints, application factory pattern)
  - FastAPI (async handlers, Pydantic models)
  data_and_orm:
  - SQLAlchemy (session management, relationship loading strategies, query construction)
  - Django ORM (QuerySet chaining, prefetch_related, select_related, F/Q expressions)
  - Alembic (migration scripts)
  scientific_and_data:
  - NumPy (broadcasting, indexing, dtype coercion, vectorized operations)
  - pandas (DataFrame/Series operations, apply chains, groupby, merge/join semantics)
  - SciPy
  infrastructure_and_utilities:
  - Celery (task definitions, retry logic, chord/group patterns)
  - Redis (cache patterns, pub/sub)
  - boto3 / AWS SDK patterns
  - Internal utility wrappers (proprietary, undocumented, idiosyncratic)
  testing:
  - pytest
  - unittest
  - coverage.py
  note: Customer repos typically combine several of these in a single codebase. Framework-specific
    bug patterns (e.g., SQLAlchemy N+1, Django ORM lazy-load outside session, NumPy
    shape mismatch) are the primary defect classes; none appear in HumanEval.
task_taxonomy:
  primary_tasks:
  - task: Bug localization
    description: Identifying the specific line or range of lines in existing code
      where a defect occurs.
    in_scope: true
    humaneval_coverage: None — HumanEval contains no tasks requiring localization
      within existing code.
  - task: Diff generation
    description: Generating a minimal, targeted corrective patch that a reviewer can
      accept or reject as a unified diff.
    in_scope: true
    humaneval_coverage: None — HumanEval produces complete standalone function bodies
      from scratch, not targeted diffs against buggy code.
  - task: Code understanding (prerequisite)
    description: Reading and comprehending existing, potentially framework-specific,
      sparsely documented code without relying on a clean natural-language spec.
    in_scope: true
    humaneval_coverage: Indirect — HumanEval evaluates code generation from clean
      docstrings, not comprehension of underdocumented existing code.
  secondary_tasks:
  - task: Bug classification / triage
    description: Labeling the bug type (logic error, off-by-one, null dereference,
      etc.) to aid developer triage.
    in_scope: true
    required: false
    humaneval_coverage: None.
  out_of_scope_tasks:
  - Pure code generation from scratch (docstring-to-function synthesis — the only
    task HumanEval measures)
  - Full-program synthesis from stdin/stdout specifications
  - Docstring generation from code bodies
output_success_criteria:
  primary_criterion: Human reviewer acceptance — the correct defect was localized
    and the proposed fix is something the reviewer would merge.
  secondary_criterion: Semantic safety — the fix does not change unintended semantics,
    mask the underlying bug, or introduce new defects.
  tertiary_criterion: Convention adherence — the fix respects codebase style, naming
    conventions, and idiomatic patterns.
  explicitly_excluded_criteria:
  - Unit test pass/fail — existing tests are often absent, incomplete, or unreliable
    in customer repos.
  - BLEU or token-match scores against a reference solution.
  edge_cases:
  - A fix that passes existing tests may still be rejected if it masks the real bug
    or violates conventions.
  - A fix with no test coverage may be accepted as correct if reviewers sign off.
  - Semantics-preserving refactors that incidentally pass tests are not considered
    correct fixes.
  humaneval_alignment: Fundamental mismatch — HumanEval's sole success criterion is
    unit-test pass/fail on freshly generated code. The deployment requires a multi-component
    human judgment not captured by any HumanEval metric.
input_characteristics:
  input_type: Existing, potentially buggy Python source code — not clean docstring
    specifications.
  documentation_conditions:
  - Absent docstrings (function body only, no specification)
  - Stale docstrings (describe removed or changed behavior)
  - Misleading inline comments (copied from elsewhere, incorrect assertions)
  - Cryptic variable and function names (single-letter vars, abbreviations, legacy
    naming)
  code_quality_conditions:
  - Logic errors (incorrect conditional branching, wrong operator precedence)
  - Off-by-one errors (loop bounds, slice indices, pagination offsets)
  - Null / None dereferences (missing guard clauses, unchecked Optional returns)
  - Framework misuse (SQLAlchemy session lifecycle errors, Django ORM N+1, NumPy broadcasting
    mismatches)
  - Legacy patterns (Python 2-style idioms in nominally Python 3 codebases, deprecated
    API calls)
  context_window_considerations: Real-world function bodies and their calling context
    (imports, class definitions, related methods) may be substantially longer than
    HumanEval's average problem size, stressing models on long-context reasoning.
  humaneval_alignment: Fundamental mismatch — HumanEval inputs are clean, hand-written,
    accurate docstrings with correct function signatures. No HumanEval problem simulates
    absent, stale, or misleading documentation.
ground_truth_and_annotation:
  ground_truth_source: Professional software developer acceptance judgment — not automated
    unit test execution.
  annotator_profile: Experienced US-based software engineers performing code review
    in production workflows.
  annotation_scheme_gaps:
  - HumanEval ground truth is automated unit-test pass/fail by benchmark authors —
    not professional developer judgment.
  - HumanEval's only human-labeled subset is docstring generation grades (1,640 items,
    single model configuration, single temperature) — not representative of bug-fix
    evaluation.
  - No documented inter-annotator agreement procedure for code-fix acceptability in
    HumanEval or its derivatives.
  - No annotation of semantic preservation, convention adherence, or bug-masking risk.
  label_reliability_risks:
  - Underspecified prompts in HumanEval already cause valid solutions to be wrongly
    penalized by unit tests — a known reliability problem that is amplified in the
    deployment setting.
  - Customer codebases may have tests that are themselves buggy or that fail to cover
    the defective path.
  - Developer acceptance is subjective and team-convention-dependent — no universal
    ground truth exists.
benchmark_validity_summary:
  benchmark: HumanEval
  overall_alignment: Poor — HumanEval was designed to measure a fundamentally different
    task (docstring-to-function synthesis) with a fundamentally different success
    criterion (unit-test pass/fail). The deployment's core tasks (bug localization,
    diff generation) are entirely absent from the benchmark's task ontology.
  dimension_assessments:
  - dimension: Input Ontology (IO)
    priority: HIGH
    alignment: None
    notes: HumanEval contains exclusively docstring-to-function generation tasks.
      Bug localization and diff generation against existing buggy code are absent.
  - dimension: Input Content (IC)
    priority: HIGH
    alignment: None
    notes: HumanEval problems are algorithm/interview-style with clean specs. No Django,
      Flask, SQLAlchemy, NumPy/pandas, or legacy-with-sparse-docs instances exist.
  - dimension: Input Form (IF)
    priority: LOWER
    alignment: Partial
    notes: Both are plain-text Python. Mismatch is content-level (absent/stale docstrings)
      rather than modality-level.
  - dimension: Output Ontology (OO)
    priority: HIGH
    alignment: None
    notes: HumanEval uses binary unit-test pass/fail. Deployment requires multi-component
      human reviewer judgment (localization accuracy + semantic safety + convention
      adherence).
  - dimension: Output Content (OC)
    priority: HIGH
    alignment: None
    notes: HumanEval annotations are benchmark-author-written unit tests. Deployment
      ground truth is professional developer acceptance of bug-fix diffs.
  - dimension: Output Form (OF)
    priority: MODERATE
    alignment: Partial
    notes: Both involve Python code output. HumanEval produces complete standalone
      functions; deployment requires targeted diffs with line-range localization metadata
      — structurally divergent.
alternative_benchmarks_to_investigate:
  bug_localization_and_repair:
  - name: SWE-bench / SWE-bench Lite / SWE-bench Verified
    relevance: Real GitHub issues requiring localization and patch generation in real
      Python repos
    coverage_notes: 'RESOLVED: SWE-bench includes Django, NumPy, pandas, matplotlib,
      scikit-learn, sympy, pytest, and astropy as source repositories — directly overlapping
      the deployment''s framework distribution (Source: Groundy analysis — [WEB-1]).
      Ground truth is FAIL_TO_PASS test transitions: the original developers wrote
      the tests to verify the fixed behavior. SWE-bench Verified (500 instances, released
      Aug 2024 with OpenAI collaboration) adds human-annotator screening for problem
      clarity, test correctness, and solvability (Source: same). IMPORTANT CAVEAT:
      Recent empirical work (Wang et al., Mar 2025) found that 7.8% of plausible (test-passing)
      patches actually fail the full developer-written test suite, and ~29.6% exhibit
      behavioral divergences from oracle patches — estimated inflation of ~6.4 percentage
      points in reported resolution rates. The SWE-ABS framework found 19.78% of previously-passing
      patches were rejected by strengthened test suites, dropping top agent score
      from 78.80% to 62.20% (Source: arXiv 2603.00520 — [WEB-2];
      arXiv 2503.15223 — [WEB-3]). This oracle-inflation
      problem is directly analogous to the deployment''s concern about test-passing
      fixes that violate semantic expectations. No direct human-reviewer-acceptance
      ground truth is used in SWE-bench — test passage remains the proxy.'
  - name: BugsInPy
    relevance: Curated real Python bugs from open-source projects with reproducible
      test failures
    coverage_notes: 'RESOLVED: BugsInPy contains 493 real bugs from 17 real-world
      Python projects, including pandas, scikit-learn, Keras, FastAPI, Matplotlib,
      Scrapy, and others (Source: SMU ink library PDF — [WEB-4];
      ResearchGate — [WEB-5]).
      Each bug is accompanied by a failing test case that passes once the bug is fixed
      (inspired by Defects4J). CAVEAT: Ground truth is automated test-pass verification,
      not human developer acceptance. No Django or SQLAlchemy web-framework instances
      have been documented in the curated project list — the focus is on scientific
      Python and CLI tools rather than web frameworks. BugsInPy explicitly supports
      fault localization (SBFL) research, making it the closest available Python-native
      benchmark for the localization subtask.'
  - name: Defects4J
    relevance: Widely used Java defect benchmark; Python equivalent coverage unclear
    coverage_notes: 'RESOLVED: Defects4J is Java-centric (initial version: 357 bugs
      from 5 Java projects; well-established as the inspiration for BugsInPy). No
      Python port or equivalent under the Defects4J name has been confirmed. BugsInPy
      is the recognized Python analog (Source: BugsInPy paper — [WEB-4]).
      Direct applicability to deployment is limited — skip in favor of SWE-bench and
      BugsInPy for Python-specific use.'
  - name: CodeFlaws
    relevance: Codeforces-sourced C program bugs; relevance to Python framework code
      limited
    coverage_notes: 'RESOLVED: CodeFlaws is sourced from Codeforces competitive programming
      (C programs) and is referenced in automated program repair literature alongside
      BugsInPy and Defects4J (Source: ResearchGate MultiMend citation — [WEB-5]).
      No Python coverage confirmed; competitive-programming bug class does not overlap
      with Django/SQLAlchemy/NumPy framework defects. Low relevance for this deployment
      — skip.'
  - name: HumanEval-Fix / EvalPlus repair variants
    relevance: Extensions of HumanEval designed for bug-repair evaluation
    coverage_notes: 'RESOLVED: HumanEvalFix (from the BigCode project) introduces
      a synthetic bug into each of the 164 canonical HumanEval solutions, turning
      the benchmark into a bug-fixing task (Source: MDPI reproducibility study — [WEB-6]).
      Bugs are ''missing logic, extra logic, or incorrect logic'' injected into HumanEval''s
      algorithm-puzzle functions. EvalPlus (HumanEval+) extends the original test
      suite 80x per problem for more rigorous generation evaluation but does NOT add
      bug-repair or localization tasks — it remains a code-generation benchmark (Source:
      EvalPlus GitHub — [WEB-7]). CRITICAL GAP: HumanEvalFix
      does NOT cover bug localization as a standalone task (the buggy line must be
      fixed, not identified), inputs remain clean algorithm problems (no framework
      code, no sparse docs), and ground truth remains unit-test pass/fail — not human
      reviewer acceptance. None of these variants address the deployment''s primary
      gaps.'
  human_reviewer_acceptance_benchmarks:
  - name: DPO-F+ (developer-preference-aligned code repair feedback)
    relevance: 'Direct analog to deployment''s primary success criterion: aligning
      code repair with developer preferences'
    coverage_notes: 'RESOLVED: DPO-F+ (Fang et al., 2025) formalizes developer-profiled,
      domain-specific metrics for feedback alignment and automatically constructs
      pairwise preference datasets from code-repair tasks, evaluated on SWE-bench
      Lite (Source: arXiv 2511.01043 — [WEB-8]). This
      is the closest identified work that operationalizes developer preference as
      an alignment signal for code repair, though it focuses on feedback quality rather
      than diff acceptability. No benchmark using merge-acceptance rate or direct
      human reviewer accept/reject judgment as the primary ground truth was identified
      in available literature — this remains a confirmed gap. Field requires stakeholder/expert
      elicitation.'
  framework_specific_python_benchmarks:
  - name: SWE-bench (Django, NumPy, pandas instances)
    relevance: Covers the actual defect classes most common in customer repos
    coverage_notes: 'RESOLVED: SWE-bench includes Django issues (e.g., django_django-10973
      cited in SWE-ABS — see arXiv 2603.00520 — [WEB-2])
      as well as NumPy, pandas, matplotlib, scikit-learn, sympy, and pytest repositories.
      This is the best-available benchmark for framework-specific Python bug localization
      and patch generation. No standalone benchmark covering only Django ORM session
      patterns, SQLAlchemy lifecycle errors, or NumPy broadcasting mismatches as a
      curated defect class was identified — that level of framework specificity remains
      a gap not covered by any known public benchmark.'
  sparse_documentation_benchmarks:
  - name: '[NOT FOUND — no benchmark using stale/absent/misleading inline documentation
      as a deliberate input condition identified]'
    relevance: Directly tests the model's ability to reason from code rather than
      spec — the primary real-world condition identified by the user
    coverage_notes: 'Searched via implicit coverage in BugsInPy and SWE-bench literature;
      neither benchmark curates or characterizes documentation sparsity as an input
      variable. FeedbackEval (Dai et al., 2026) notes that ''removing semantic cues
      such as docstrings or role-play causes severe degradation'' but this is a model-robustness
      finding, not a benchmark designed around sparse-doc inputs (Source: arXiv 2504.06939
      — [WEB-9]). This gap is confirmed as unaddressed
      by any public benchmark and likely requires purpose-built evaluation or expert
      elicitation.'
flagged_gaps_for_web_search:
- gap_id: 1
  topic: Bug localization as a task type in existing benchmarks
  search_target: HumanEval-Fix bug localization benchmark SWE-bench Defects4J code
    repair Python evaluation localization accuracy
  resolution_status: RESOLVED — see alternative_benchmarks_to_investigate. SWE-bench
    covers localization+patch generation for real Python repos including Django/NumPy.
    HumanEvalFix covers bug-fix but NOT localization as a standalone task. No benchmark
    with explicit line-range localization scoring identified.
- gap_id: 2
  topic: Buggy-code-as-input benchmarks with real-world Python
  search_target: BugsInPy SWE-bench Lite CodeFlaws automated program repair benchmark
    Python real-world codebase evaluation 2023 2024
  resolution_status: RESOLVED — BugsInPy (493 bugs, 17 projects, includes pandas/scikit-learn/FastAPI)
    and SWE-bench (real GitHub issues, includes Django/NumPy/pandas) are the best
    options. CodeFlaws is C-only and not applicable.
- gap_id: 3
  topic: Framework-specific Python bug patterns in benchmarks
  search_target: Django Flask SQLAlchemy NumPy pandas bug benchmark defect dataset
    Python framework-specific evaluation
  resolution_status: PARTIALLY RESOLVED — SWE-bench includes Django and scientific
    Python (NumPy, pandas, matplotlib) instances. No benchmark specifically targeting
    SQLAlchemy session management, Flask routing bugs, or NumPy broadcasting errors
    as a curated defect class was found. Flask/SQLAlchemy-specific coverage remains
    a confirmed gap.
- gap_id: 4
  topic: Human reviewer acceptance as ground truth for code repair
  search_target: code repair benchmark human reviewer acceptance merge rate developer
    preference pull request evaluation ground truth 2022 2023 2024
  resolution_status: SEARCHED, NOT FOUND — DPO-F+ (arXiv 2511.01043) uses developer
    preference as an alignment signal but not as a benchmark ground truth label. No
    public benchmark using accept/reject merge decisions by human reviewers as primary
    ground truth was identified. This gap is confirmed.
- gap_id: 5
  topic: Sparse or misleading documentation as deliberate input condition
  search_target: code benchmark stale docstrings absent documentation misleading comments
    code understanding evaluation robustness
  resolution_status: SEARCHED, NOT FOUND — confirmed gap, no benchmark deliberately
    curates absent/stale/misleading docstrings as an input condition. Requires purpose-built
    evaluation design.
- gap_id: 6
  topic: Semantic preservation and convention adherence as scoring dimensions
  search_target: code fix correctness semantic preservation convention adherence scoring
    benchmark automated program repair evaluation metric
  resolution_status: PARTIALLY RESOLVED — SWE-ABS and PatchDiff (arXiv 2503.15223,
    2603.00520) demonstrate that ~29.6% of plausible SWE-bench patches diverge behaviorally
    from oracle patches, and ~11% are certainly incorrect. This is methodological
    evidence that test-pass is insufficient for semantic correctness — but no benchmark
    has integrated semantic preservation or convention adherence as a first-class
    scoring dimension.
- gap_id: 7
  topic: Diff / unified patch output format evaluation
  search_target: code repair diff output format evaluation unified patch generation
    benchmark line range localization scoring 2022 2023 2024
  resolution_status: 'NEEDS VERIFICATION — deferred: below search budget. SWE-bench
    uses unified diff patches as the output format but does not appear to score line-range
    localization accuracy as a separate metric; scoring is FAIL_TO_PASS test transition
    only.'
- gap_id: 8
  topic: Test-free correctness assessment for bug fixes
  search_target: code repair evaluation without unit tests test-free bug fix correctness
    sparse test coverage benchmark assessment
  resolution_status: 'NEEDS VERIFICATION — deferred: below search budget. PatchDiff
    and UTBoost are relevant methodologies (differential test generation) but target
    supplementing existing tests rather than test-free evaluation.'
infrastructure_and_deployment_notes:
  interface: Integrated into code review tooling (e.g., GitHub PR comments, GitLab
    MR suggestions, or dedicated review platform UI); output is a proposed diff, not
    a full code file.
  latency_requirements: '[NEEDS VERIFICATION — deferred: likely unsearchable as SLA
    figures are platform-specific and proprietary; typical inline suggestion latency
    expectations in CI/CD-integrated review tools are not publicly standardized]'
  input_size_constraints: Real-world function bodies with their calling context (imports,
    class hierarchy, related methods) may be 100–1000+ lines; substantially larger
    than HumanEval's average prompt size.
  output_format_requirements: Unified diff format (or equivalent line-range replacement)
    with localization metadata (file path, line range, bug type label). Complete function
    regeneration is not an acceptable output form.
  trust_model: Developer retains accept/reject control over every suggested fix; the
    system is advisory, not autonomous.
  security_considerations: 'Customer codebases may contain proprietary logic, credentials
    in comments, and sensitive business logic — privacy and confidentiality constraints
    on what context can be sent to an LLM API are significant. SOC 2 Type II certification
    is effectively a procurement prerequisite for enterprise SaaS platforms processing
    customer code: enterprise customers routinely require it, and it covers confidentiality
    (protection of intellectual property and sensitive customer data) as one of its
    five Trust Services Criteria (Source: Cobalt.io SOC 2 guide — [WEB-10];
    Blaxel AI agent SOC 2 guide — [WEB-11]).
    Additionally, code snippets flowing to LLM APIs introduce LLM provider subprocessor
    obligations: enterprise agreements typically require explicit opt-out of training
    data use, and major providers (GitHub Copilot Business/Enterprise, Claude for
    Enterprise) offer zero-retention configurations (Source: Probo AI coding tools
    SOC 2 guide — [WEB-12]).'
regulatory_and_professional_context:
  applicable_us_standards: 'RESOLVED: The primary US software security standard is
    NIST SP 800-218 (Secure Software Development Framework, SSDF) Version 1.1, finalized
    February 2022. SSDF v1.2 (SP 800-218 Rev.1) entered initial public draft in December
    2025 per Executive Order 14306 (Source: NIST CSRC — [WEB-13];
    NIST news — [WEB-14]).
    SSDF compliance via self-attestation is required for software vendors selling
    to US federal agencies under EO 14028 and OMB Memo M-22-18 (Source: aikido.dev
    SSDF explainer — [WEB-15]).
    NIST has also finalized SP 800-218A, an SSDF Community Profile specifically for
    generative AI and dual-use foundation models (Source: NIST CSRC — [WEB-16]).
    For SaaS platforms, SOC 2 Type II (AICPA framework) is the de facto enterprise
    procurement requirement covering security, availability, processing integrity,
    confidentiality, and privacy (Source: Cobalt.io — [WEB-10]).'
  intellectual_property_considerations: 'Generated diffs potentially raise questions
    about IP ownership and license compliance when the model has been trained on open-source
    code. [NEEDS VERIFICATION — deferred: current US legal status of AI-generated
    code suggestions as of assessment date is rapidly evolving and requires legal
    expert consultation rather than web search alone]'
  professional_norms: US software engineering teams operate under implicit or explicit
    code style guides (PEP 8, Google Python Style Guide, Black formatting), security
    review checklists (OWASP, internal threat models), and semantic versioning conventions
    — none of which are represented in HumanEval's evaluation criteria.
  developer_acceptance_standards: A fix must be idiomatic, minimal, non-breaking,
    and convention-consistent to be merged; test passage is necessary but not sufficient.
net_new_findings:
  swe_bench_test_oracle_reliability:
    finding: 'SWE-bench''s test-pass ground truth is materially unreliable for semantic
      correctness: 7.8% of plausible (test-passing) patches fail the full developer-written
      test suite; 29.6% exhibit behavioral divergences from oracle patches; and an
      estimated 11% of plausible patches are certainly incorrect (inflating reported
      resolution rates by ~6.4 percentage points). The SWE-ABS adversarial framework
      rejected 19.78% of all previously-passing patches when applying strengthened
      test suites, dropping the top agent''s score from 78.80% to 62.20%.'
    relevance_to_deployment: This empirical evidence from the best available alternative
      benchmark (SWE-bench) directly validates the deployment's concern that test-passing
      fixes may be semantically wrong or bug-masking. Even when using SWE-bench as
      an alternative to HumanEval, the test-oracle inflation problem persists — strengthening
      the case that human reviewer acceptance cannot be proxied by automated test
      metrics alone.
    source: arXiv 2503.15223 (Wang et al., Mar 2025) — [WEB-3];
      arXiv 2603.00520 (SWE-ABS) — [WEB-2]
  bugsinpy_localization_performance:
    finding: A recent evaluation of locally executed LLMs on BugsInPy (349 bugs, 17
      projects, zero-shot function-level prompting) found accuracy between 43–45%,
      with a large proportion of 'partially correct' responses that identify problematic
      code regions without pinpointing the exact fix. Performance varied significantly
      across projects based on codebase characteristics.
    relevance_to_deployment: This provides a concrete baseline for LLM bug localization
      accuracy on real Python projects, suggesting that precise localization (vs.
      approximate region identification) is particularly difficult — directly relevant
      to the deployment's core task. Results are function-level, not line-level, which
      may overstate localization precision for the deployment's use case.
    source: ResearchGate BugsInPy FGDM study — [WEB-5]
  nist_ssdf_generative_ai_profile:
    finding: NIST finalized SP 800-218A, an SSDF Community Profile specifically for
      generative AI and dual-use foundation models, adding AI-specific secure development
      practices to the SSDF baseline. This is directly relevant to a SaaS platform
      deploying an LLM for code repair.
    relevance_to_deployment: Enterprise customers (especially those under US federal
      procurement requirements) may require the platform to demonstrate compliance
      with SSDF practices, including the AI-specific SP 800-218A addendum. This is
      a net-new regulatory touchpoint beyond standard SSDF v1.1.
    source: NIST CSRC SP 800-218A — [WEB-16]
  humaneval_contamination_note:
    finding: Top models now solve over 94% of HumanEval problems, and HumanEval has
      documented flaws including incorrect problem statements and likely data contamination/benchmark
      overfitting. The benchmark is considered saturated for discriminating among
      competitive models.
    relevance_to_deployment: HumanEval's saturation problem further erodes its validity
      as a proxy for deployment performance — high HumanEval scores reflect memorization
      and benchmark-specific optimization rather than generalizable code understanding,
      amplifying the existing task-mismatch concerns documented in the validity summary.
    source: AI4SE benchmarking review (arXiv 2503.05860, IEEE TSE) — [WEB-17];
      SWE-EVO paper — [WEB-18]
```

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

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: HumanEval tests generation of new functions from scratch (docstring-to-code). Your system reads existing, potentially buggy code and identifies defects — logic errors, off-by-one bugs, null dereferences. Do your review tasks primarily involve: (a) understanding what existing code does, (b) localizing where a bug occurs, (c) classifying the bug type, or (d) generating a corrected code snippet? Which of these are most critical, and are any out of scope?
A1: The most critical capabilities are (b) bug localization — identifying the specific line or range — and (d) generating a valid corrected snippet that reviewers can accept as a diff. Understanding existing code (a) is an implicit prerequisite. Bug classification (c) is useful for triage but not required. Pure code generation from scratch is explicitly out of scope.

Q2 [IC]: Your users are American development teams, which implies real-world codebases with framework-specific patterns (Django, Flask, NumPy), legacy code styles, incomplete or misleading variable names, and missing or incorrect docstrings. Does your system need to handle code that lacks docstrings or has misleading comments — conditions essentially absent from HumanEval's clean, well-documented problem set?
A2: Yes. Customer codebases contain Django/Flask views, SQLAlchemy models, NumPy/pandas pipelines, internal utility wrappers, and substantial legacy Python with sparse or stale docstrings. Misleading comments and cryptic variable names are common; the system must reason directly from code rather than relying on clean natural-language specifications.

Q3 [OO]: HumanEval scores by pass/fail on unit tests — a binary correctness signal for freshly generated code. For your bug-detection feature, what counts as a correct system output: flagging the right line, naming the right bug category, producing a fix that passes tests, or producing a fix that a human reviewer would accept even if tests weren't available? Could a technically passing fix still be rejected by your reviewers as wrong or unsafe?
A3: The primary success criterion is human reviewer acceptance — the right defect was localized and the proposed fix is something they would merge. Unit tests are often absent or untrustworthy in customer repos, so a fix that passes existing tests can still be rejected if it changes semantics, masks the real bug, or violates codebase conventions. Conversely, a fix with no test coverage can be considered correct if reviewers sign off.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | HumanEval's category space covers only clean, scratch function-generation tasks; the deployment's core task types — bug localization and diff generation against existing buggy code — are essentially absent from the benchmark's ontology. |
| IC | HIGH | HumanEval problems are clean, well-specified, and docstring-driven; deployment code is framework-heavy (Django, SQLAlchemy, NumPy), legacy, sparsely documented, and often semantically misleading, making the benchmark's instances unrepresentative of real inputs. |
| IF | LOWER | Both benchmark and deployment are text-only Python; no modality or infrastructure mismatch exists. |
| OO | HIGH | HumanEval's output taxonomy is binary unit-test pass/fail on freshly generated code; the deployment requires a multi-component output judgment (correct localization + acceptable diff + semantic safety + convention adherence) evaluated by human reviewers, not automated tests. |
| OC | HIGH | HumanEval ground-truth labels are unit-test outcomes on generated code; the deployment's ground truth is human reviewer acceptance of bug fixes, meaning label correctness depends on professional developer judgment that HumanEval's annotation scheme never captures. |
| OF | MODERATE | Both use code output, but HumanEval produces complete standalone functions while the deployment produces targeted diffs with localization metadata; the output form is partially aligned but the structural requirements diverge meaningfully. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

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
  "region": "US Professional Software Development Teams — Code Review / Bug Localization",
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
