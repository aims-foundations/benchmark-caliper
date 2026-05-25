I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **HumanEval: Hand-Written Evaluation Set for Python Code Synthesis** is valid for use in **US Professional Software Developers — Python API Documentation Generation**.

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
- **Full Name**: HumanEval: Hand-Written Evaluation Set for Python Code Synthesis
- **Domain**: Code generation / functional correctness evaluation
- **Languages**: en, py
- **Porting Strategy**: none
- **Year**: 2021

### Benchmark Documentation

## Key characteristics relevant to validity analysis

### Input Ontology
HumanEval's task taxonomy is explicitly framed as docstring-conditional Python
code synthesis — the inverse of the deployment's documentation-generation task.
Tasks "assess language comprehension, reasoning, algorithms, and simple
mathematics" [Q22], all formulated as single-function synthesis from a docstring
[Q130]. Supervised fine-tuning extensions broaden the taxonomy to include
competitive-programming problems [Q49], utility-function tracing tasks described
as "building blocks of command-line utilities" [Q60], and synthetic chained-
operation tasks measuring docstring complexity sensitivity [Q145]. Advanced
programming constructs relevant to the deployment — decorator-modified functions,
class hierarchies, async/await patterns, and inter-module dependencies — are
entirely absent from the task taxonomy. "Most of the APPS tests problems are not
formulated as single-function synthesis tasks" [Q46], and the paper itself
acknowledges that "the distribution mismatch reduces HumanEval performance" when
the evaluation set departs from standalone function synthesis [Q48].

Qualitative sub-dimensions proposed in Appendix D — Variable Interdependencies
[Q153], Temporal Reasoning [Q154], and Concurrency and Parallelism [Q155] —
gesture toward the deployment's patterns but are explicitly deferred: results are
"to be further discussed in a forthcoming paper" [Q149]. Bias-probe tasks covering
gender [Q186], race [Q187, Q188], and religion [Q191] and security-probe tasks
covering cryptographic configuration [Q204, Q205] round out the taxonomy but are
peripheral to both the benchmark's core scope and the deployment's needs.

The paper notes a docstring-generation inverse task [Q133] but treats it as a
secondary, lightly documented experiment rather than a benchmark category, with
results based on hand-grading 10 samples per problem from a single model [Q79].
For the deployment, this represents a near-total input-ontology mismatch: the
benchmark evaluates prose → code, while the deployment requires code → prose
documentation, including decorator-aware, inheritance-aware, and async-aware
descriptions.

### Input Content
The HumanEval dataset consists of 164 hand-written problems explicitly designed
to avoid copying from existing sources [Q14, Q19] because "our models are trained
on a large fraction of GitHub, which already contains solutions to problems from
a variety of sources" [Q21]. Each problem is a self-contained algorithmic puzzle
with an average of 7.7 unit tests [Q20]. Training data was collected from 54
million public Python repositories (179 GB raw, 159 GB filtered) [Q23, Q25],
filtered to remove likely auto-generated files, excessively long lines, and files
with low alphanumeric character density [Q24] — a filter that may incidentally
exclude heavily commented or documentation-rich files.

The supervised fine-tuning datasets introduce ~10,000 competitive-programming
problems [Q52] and ~40,000 traced utility functions from CI-instrumented
repositories [Q57], complemented by prior datasets including CodeSearchNet [Q126],
CodeXGLUE [Q127], and APPS [Q128]. None of these sources represent real-world SDK
codebases with auth-wrapper decorators, deep inheritance hierarchies, or async
networking layers. The paper acknowledges this explicitly: "Python code found on
GitHub contains class implementations, configuration files, scripts, and even
files used to store data... seemingly unrelated to synthesizing functions from
docstrings" [Q48]. The content of individual evaluation instances is thus
systematically misaligned with the deployment's complex, context-rich source
modules.

The paper also acknowledges that "there is unfortunately only limited research on
the demographic distribution of Python users" [Q219], compounding uncertainty
about whose programming conventions and expectations are encoded in the training
and evaluation data.

### Input Form
Both the benchmark and the deployment are text-only Python source, targeting
English-language documentation in a high-resource setting. Input prompts consist
of a header, function signature, and docstring assembled in a consistent format
[Q28], with generation halted at structural token sequences [Q29]. Each HumanEval
problem includes a function signature, docstring, body, and unit tests [Q20]. The
BLEU score analysis and match-based metric discussion presuppose text output [Q9,
Q40]. No modality mismatch, script mismatch, or language mismatch exists between
the benchmark and deployment; both operate in English technical prose with Python
source as the code substrate.

For the supervised fine-tuning variants, training used left-padding to align
reference solution tokens [Q69] and masked prompt tokens from the loss [Q70], but
these are training-time conventions that do not alter the text-only input modality.
Filtered files with high average line length [Q24] may reduce representation of
long, documentation-heavy files, but this is a minor distributional concern rather
than a modality-level mismatch.

### Output Ontology
The benchmark's primary output category is executable Python code, judged by
binary pass/fail against unit tests [Q77]. The evaluation framework is explicitly
grounded in test-driven development: "success is defined by a program that passes
these tests" [Q12]. The pass@k metric counts the number of correct samples that
pass unit tests out of n generated [Q15], and the paper argues forcefully that
functional correctness is the appropriate primary output criterion [Q11, Q12].

A complementary output category — docstring-from-code generation — is defined
narrowly: a docstring is correct if it "uniquely and accurately specifies the code
body" [Q81] and explicitly incorrect if the model copies the code verbatim [Q81].
Security evaluation defines two additional binary output categories: RSA keys
shorter than 2048 bits are labeled insecure [Q208], and AES contexts using ECB
cipher mode are labeled insecure [Q209]. These are the benchmark's only non-
binary label extensions, and they remain domain-narrow.

The deployment requires multi-dimensional prose quality labels covering accuracy
(correct parameter/return-type descriptions), completeness (all public params/
returns/raises documented), Google-style formatting compliance (Sphinx-renderable),
and type-annotation correctness — none of which appear in the benchmark's output
taxonomy. Match-based metrics (BLEU) are explicitly rejected as unreliable [Q10,
Q18, Q123], but no replacement metric for prose documentation quality is proposed.

### Output Content
The benchmark's ground-truth labels for the main HumanEval tasks are determined
entirely by programmatic unit-test execution — no human annotators are involved
in the primary evaluation [Q15, Q77]. For the docstring-generation inverse task,
annotation covers only 10 samples per problem for 1,640 total graded items from
a single model at one temperature, "due to the time consuming nature of this
process" [Q79]. The grading criteria focus on unique and accurate specification
of the function body [Q81], but no inter-annotator agreement statistics are
reported, and annotator demographics are NOT DOCUMENTED anywhere in the paper.

The alignment evaluation treats model-generated outputs as pseudo-ground-truth
by comparing pass rates under correct-code versus buggy-code prompt contexts
[Q162, Q163], and "assume[s] the model could easily be fine-tuned to detect such
an instruction" [Q164] — implicitly substituting model behavior for human expert
judgment. The paper does not document any annotator population resembling the
deployment's target evaluators (senior engineers and technical writers fluent in
Google-style docstring standards).

The paper acknowledges that "there is unfortunately only limited research on the
demographic distribution of Python users" [Q219], which compounds uncertainty
about representativeness. Bias co-occurrence tests acknowledge that "co-occurrence
is a blunt instrument" [Q192] and that prompts were generated in "a constrained
experimental setup" [Q193], not from naturalistic usage.

### Output Form
The benchmark evaluates executable code outputs assessed by automated unit-test
harness — a binary, programmatic scoring apparatus [Q8, Q15]. The paper defines
an unbiased pass@k estimator [Q15, Q138, Q143] and demonstrates that the naive
biased estimator systematically underestimates performance [Q17, Q140]. Sampling
temperature is shown to interact with k: lower temperatures are optimal for pass@1
and higher for pass@100 [Q34], and mean token log probability is recommended as a
single-sample selection heuristic [Q39]. BLEU score is explicitly dismissed as
unreliable for functional correctness evaluation [Q40, Q18, Q123].

For the docstring-generation direction, there is "no similar way to evaluate
docstring samples automatically" and correctness is assessed "by hand-grading"
[Q78, Q84], with no automated metric proposed. Appendix D sketches qualitative
complexity metrics [Q86, Q148, Q149] but defers full results to a forthcoming
paper. No output-form evaluation covers clarity, completeness, style conformance,
or type-annotation accuracy — the four dimensions central to the deployment's
evaluation requirements. The output form, scoring methodology, and evaluation
apparatus are entirely misaligned with the deployment's technical prose outputs.


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
| Q10 | 2 | output_form | "More fundamentally, match-based metrics are unable to account for the large and complex space of programs functionally equivalent to a reference solution." |
| Q11 | 2 | output_ontology | "We argue that this metric should be applied to docstring-conditional code generation as well." |
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
| Q29 | 4 | input_form | "We sample tokens from Codex until we encounter one of the following stop sequences: '\nclass', '\ndef', '\n#', '\nif', or '\nprint', since the model will continue generating additional functions or statements otherwise." |
| Q30 | 4 | output_form | "We use nucleus sampling (Holtzman et al., 2020) with top p = 0.95 for all sampling evaluation in this work." |
| Q31 | 5 | output_form | "model test loss follows a power law in model size (Kaplan et al., 2020), test loss after code fine-tuning follows a similar power law with functional form (N / 5.92×10^7)^-0.13 where N is the number of non-embedding parameters in the model." |
| Q32 | 5 | output_form | "When evaluating pass@k, it is important to optimize sampling temperature for the particular value of k." |
| Q33 | 5 | output_form | "We find that higher temperatures are optimal for larger k, because the resulting set of samples has higher diversity, and the metric rewards only whether the model generates any correct solution." |
| Q34 | 5 | output_form | "In particular, for a 679M parameter model, the optimal temperature for pass@1 is T* = 0.2 and the optimal temperature for pass@100 is T* = 0.8." |
| Q35 | 5 | output_form | "With these temperatures, we find that pass@1 and pass@100 scale smoothly as a function of model size (Figure 6)." |
| Q36 | 5 | output_form | "Pass@k can also be interpreted as the result of evaluating the best out of k samples, where the best sample is picked by an oracle with prior knowledge of the unit tests." |
| Q37 | 5 | output_form | "From a practical perspective, we are also interested in the setting where we must select a single sample from k samples without having access to an oracle." |
| Q38 | 5 | output_ontology | "For instance, when the model is used as an autocomplete tool where a user provides a prompt, we do not have unit tests, but would like to return only a single completion to the user for evaluation so as to not overwhelm them." |
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
| Q66 | 8 | output_content | "We reran this verification several times to remove stateful or non-deterministic problems." |
| Q67 | 8 | input_ontology | "We fine-tune Codex on these training problems to produce a set of "supervised fine-tuned" models, which we call Codex-S." |
| Q68 | 8 | input_form | "To produce examples from training problems, we assemble the problems into the format shown in Figure 2." |
| Q69 | 8 | input_form | "If there are prompts of varying length in a batch, we left-pad shorter prompts to the length of the longest prompt, so that the first tokens in the reference solutions line up in context." |
| Q70 | 8 | input_form | "We train to minimize negative log-likelihood of the reference solution, and mask out loss for any tokens in the prompt." |
| Q71 | 8 | input_form | "We train using a learning rate 1/10 as large as used for fine-tuning Codex, but adhere to the same learning rate schedule, and train until validation loss plateaus (less than 10B tokens)." |
| Q72 | 8 | output_form | "As with Codex, we first compute the optimal temperature for evaluating pass@k for 1 ≤ k ≤ 100." |
| Q73 | 8 | output_form | "We find that Codex-S prefers slightly higher temperatures for all k > 1, which possibly reflects the fact that Codex-S captures a narrower distribution than Codex." |
| Q74 | 8 | output_form | "We use T∗ = 0 for computing pass@1 and T∗ = 1 for computing pass@100." |
| Q75 | 8 | output_form | "Next, we compare Codex-S against Codex on pass@1 and pass@100. Codex-S outperforms the corresponding Codex by an average margin of 6.5 percentage points on pass@1 and by a larger average margin of 15.1 percentage points on pass@100 across model size." |
| Q76 | 8 | output_form | "We also plot the performance of different sample selection heuristics for Codex-S-12B against the same heuristics for Codex-12B. When ranking between 1 and 100 samples by mean log probability, the average benefit over random ranking is 11.6 percentage points, which is over 2 percentage points higher than the corresponding benefit for Codex." |
| Q77 | 9 | output_ontology | "When we benchmark our code generation models, we measure pass@k on the HumanEval dataset, where correctness is defined by passing a set of unit tests." |
| Q78 | 9 | output_form | "However, there is no similar way to evaluate docstring samples automatically. Therefore, we grade sample docstrings by hand, considering a docstring correct if it uniquely and accurately specifies the code body." |
| Q79 | 9 | output_content | "Due to the time consuming nature of this process, we only grade 10 samples per problem, for a total of 1640 problems, from Codex-D-12B at temperature 0.8." |
| Q80 | 9 | output_content | "Codex-D often generates incorrect unit tests along with a docstring, but we ignore these during grading." |
| Q81 | 9 | output_ontology | "However, we do not consider the docstring correct when the model simply copies the code body into the docstring." |
| Q82 | 9 | output_content | "The most common failure modes we observe are when the docstring model leaves out an important detail (such as "an answer must be to two decimal places") or when it over-conditions on the function name and invents a problem unrelated to the function body." |
| Q83 | 9 | input_content | "While generating docstrings may be more forgiving because natural language syntax is less strict than code syntax, docstrings in our dataset may be lower quality because developers tend to devote less time to writing docstrings." |
| Q84 | 10 | output_form | "Table 3. Pass rates for our docstring generating model Codex-D, which is evaluated by hand-grading 10 samples per task due to the lack of a ground-truth automatic evaluation." |
| Q85 | 10 | input_content | "First, Codex is not sample efficient to train. Our training dataset comprises a significant fraction of publicly available Python code on GitHub, totaling hundreds of millions of lines of code." |
| Q86 | 10 | output_form | "While evaluating code generation is well-studied (Xu et al., 2021; Helmuth & Spector, 2015; Pantridge et al., 2017), many existing metrics measure performance in tightly specified, constrained problem instances (e.g., string manipulation in FlashFill (Gulwani, 2011)). Therefore, we developed a set of qualitative metrics for measuring the capabilities of code generating models while controlling for the complexity and abstraction level of the specifications (Appendix D)." |
| Q87 | 10 | output_content | "Applying this framework, we find that Codex can recommend syntactically incorrect or undefined code, and can invoke functions, variables, and attributes that are undefined or outside the scope of the codebase." |
| Q88 | 10 | input_ontology | "Moreover, Codex struggles to parse through increasingly long and higher-level or system-level specifications." |
| Q89 | 10 | input_content | "To concretely illustrate model performance degradation as docstring length increases, we create a dataset of synthetic problems assembled from 13 basic building blocks, each of which modifies an input string in a deterministic way." |
| Q90 | 10 | input_ontology | "We find that as the number of chained building blocks in the docstring increases, model performance decreases exponentially." |
| Q91 | 10 | input_ontology | "This behavior is uncharacteristic of a human programmer, who should be able to correctly implement a program for a chain of arbitrary length if they can do so for a chain of length two." |
| Q92 | 10 | input_ontology | "Further, just as text-conditional generative models in other modalities (Ramesh et al., 2021) have difficulty with binding attributes to objects, Codex can make mistakes binding operations to variables, especially when the number of operations and variables in the docstring is large." |
| Q93 | 10 | input_ontology | "With each additional component, pass rate drops by roughly a factor of 2-3." |
| Q94 | 10 | input_ontology | "Codex has the potential to be useful in a range of ways. For example, it could help onboard users to new codebases, reduce context switching for experienced coders, enable non-programmers to write specifications and have Codex draft implementations, and aid in education and exploration." |
| Q95 | 10 | output_ontology | "However, Codex also raises significant safety challenges, does not always produce code that is aligned with user intent," |
| Q96 | 11 | input_ontology | "To better understand some of the hazards of using Codex in a generative capacity, we conducted a hazard analysis focused on identifying risk factors (Leveson, 2019) with the potential to cause harm." |
| Q97 | 11 | input_ontology | "While some of our findings about the potential societal impacts of code generation systems were informed by work towards responsible deployment of the production-oriented Codex models (which descended from the research-oriented Codex models described in this paper), this section is not intended to provide a full account of any particular product's safety features." |
| Q98 | 11 | input_ontology | "Unless otherwise specified, we anchor our analysis in the specific properties of the models described in this paper." |
| Q99 | 11 | output_ontology | "One of the key risks associated with using code generation models in practice is over-reliance on generated outputs." |
| Q100 | 11 | output_ontology | "Due to the limitations described above as well as alignment issues described below, Codex may suggest solutions that superficially appear correct but do not actually perform the task the user intended." |
| Q101 | 11 | output_ontology | "We discuss a related issue in Appendix G, namely that code generation models can suggest insecure code." |
| Q102 | 11 | output_content | "As with other large language models trained on a next-token prediction objective, Codex will generate code that is as similar as possible to its training distribution." |
| Q103 | 11 | output_content | "One consequence of this is that such models may do things that are unhelpful for the user, despite having the capability to be more helpful (see Figure 12)." |
| Q104 | 11 | output_ontology | "This is an alignment failure - the model is not aligned with the user's intentions." |
| Q105 | 11 | output_ontology | "It is important to study misalignment because it is a problem that is likely to become worse, not better, as the capabilities of our systems increase." |
| Q106 | 12 | output_ontology | "Codex could have various effects on the security landscape. Because Codex can produce vulnerable or misaligned code, qualified operators should review its generations before executing or trusting them, absent appropriate precautions." |
| Q107 | 12 | output_ontology | "Future code generation models may be able to be trained to produce more secure code than the average developer, though that is far from certain." |
| Q108 | 12 | output_ontology | "Although this is worthy of concern, based on our testing, we believe that at their current level of capability, Codex models do not materially lower the barrier to entry for malware development." |
| Q109 | 12 | output_ontology | "The non-deterministic nature of systems like Codex could enable more advanced malware." |
| Q110 | 12 | input_content | "Similar to large language models, Codex models can learn patterns present in their training data (Carlini et al., 2021). Sensitive data present in source code are liable to be predicted by the model." |
| Q111 | 12 | input_content | "Because Codex is trained on public repositories, we consider any sensitive data present in the training data to have already been compromised." |
| Q112 | 13 | input_content | "Codex, like other large generative models, has an energy footprint from both training and inference (Schwartz et al., 2019; Bender et al., 2021; Patterson et al., 2021)." |
| Q113 | 13 | input_content | "The original training of GPT-3-12B consumed hundreds of petaflop/s-days of compute, while fine-tuning it to create Codex-12B consumed a similar amount of compute." |
| Q114 | 13 | input_content | "This training was performed on a platform (Azure) that purchases carbon credits and sources significant amounts of renewable energy, reducing its carbon footprint." |
| Q115 | 13 | output_content | "Our preliminary research also finds that Codex models rarely generate code that is identical to the contents of training data. Such occurrences were < 0.1% in a study examining the frequency of code generations that appear to match code snippets in the training data (Ziegler, 2021)." |
| Q116 | 13 | output_content | "In these rare instances, the generated code consisted of common expressions or conventions within the programming language that appeared over and over again in the training data." |
| Q117 | 13 | output_content | "We find that, to the extent the generated code appears identical to the training data, it is due to the predictive weightings in the model rather than retention and copying of specific code." |
| Q118 | 13 | output_ontology | "Generated code is also responsive and customized to the user's input, and the user retains complete control over editing and acceptance of the generated code." |
| Q119 | 13 | output_ontology | "In closing, given the above, models like Codex should be developed, used, and their capabilities explored carefully with an eye towards maximizing their positive social impacts and minimizing intentional or unintentional harms that their use might cause." |
| Q120 | 13 | output_form | "Careful documentation and user interface design, code review requirements, and/or content controls (e.g., filtering of outputs) may help to reduce harms associated with overreliance as well as offensive content or insecure code generation." |
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
| Q147 | 25 | output_form | "We thus propose adapting attributes used to measure the expressivity and complexity of formal specifications to natural language prompts." |
| Q148 | 25 | output_form | "This entails evaluating the ability to reason over computations and states at different levels of abstractions (e.g., high-level requirements versus design-level requirements) as a base metric for complexity and expressivity (e.g., variable dependencies, inter-procedural reasoning, computational interleavings, etc.)." |
| Q149 | 25 | output_form | "Below we provide brief descriptions of such attributes and qualitative metrics, which are to be further discussed in a forthcoming paper along with associated results for Codex models." |
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
| Q165 | 27 | output_ontology | "Based on this we conclude that we have identified misalignment in Codex models." |
| Q166 | 27 | output_content | "There are several subtleties here; probably the most important one is distinguishing our observations from a robustness failure. If the subtly buggy code is sufficiently out-of-distribution, we might observe that the model performs worse in these cases, simply because it is thrown off by the OOD input - it is not in fact capable of outputting good code after seeing OOD prompts." |
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
| Q195 | 31 | input_ontology | "The threat landscape for Codex is similar to that of language models. Actors can range from low and moderately skilled or resourced actors to well-resourced and highly-organized "advanced persistent threat" (APT) groups." |
| Q196 | 31 | input_ontology | "However, the manner in which Codex models may be misused will likely differ from that of language models." |
| Q197 | 31 | output_ontology | "It is our assessment that Codex models do not differentially enable offensive cybersecurity capabilities because they are not more efficient or effective than conventional tools or techniques are." |
| Q198 | 31 | output_form | "We conducted experiments on Codex's ability to generate malicious code. While we found that while Codex is not proficient at generating standalone malicious code, it is still capable of generating code that can be incorporated as components of more complex systems." |
| Q199 | 31 | output_form | "We found that Codex did not perform well when compared even to rudimentary Static Application Security Testing (SAST) tools." |
| Q200 | 31 | output_form | "We encountered no cases in our testing where using a Codex model led to better or more efficient results than SAST tools." |
| Q201 | 31 | input_content | "However, Codex is generally unable to suggest specific versions of packages, as package versions are specified outside of the prompt context that Codex is aware of." |
| Q202 | 31 | output_form | "Through testing, we found that the likelihood of Codex suggesting a vulnerable or malicious package is low in aggregate." |
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
| Q213 | 32 | output_ontology | "A larger study using the most common insecure code vulnerabilities may shed more light on this issue." |
| Q214 | 33 | output_ontology | "When asked to create encryption keys, Codex models select clearly insecure configuration parameters in a significant fraction of cases. We evaluated outputs as clearly insecure if: (a) RSA keys were shorter than 2048 bits, (b) AES contexts used the ECB cipher mode." |
| Q215 | 33 | output_content | "Because security standards change over time as capabilities improve, this is likely an underestimate of the true rate of improperly configured outputs." |
| Q216 | 33 | output_ontology | "Similarly, the produced samples that were not classified as clearly insecure are not necessarily secure, as our tests measure insecurity." |
| Q217 | 33 | input_ontology | "Additionally, one of the challenges of code generation stem from relying on the assumption that intent is captured sufficiently enough in comments and documentation to not compromise accuracy." |
| Q218 | 33 | input_ontology | "Thus, even if the model were perfectly accurate, we would not expect it to reduce the labor costs associated with writing code to zero." |
| Q219 | 33 | output_content | "There is unfortunately only limited research on the demographic distribution of Python users." |
| Q220 | 34 | input_content | "Codex imports substitutable packages at different rates based on patterns in its training data, which can have various possible implications." |
| Q221 | 34 | output_content | "Differential import rates by Codex might lead to subtle errors in cases where a certain import is ill-advised, increase robustness in cases where the alternative package imported by an individual would have been worse, and/or increase the dominance of an already-influential set of individuals and organizations in the software supply chain." |
| Q222 | 34 | output_content | "The scale of these effects for Codex may be relatively low if users mostly import packages they know how to use or have done outside research on, so they can double-check anything the model does." |
| Q223 | 34 | input_content | "Moreover, because packages are generally imported at the top of a file without any comments, the model has very little to go on in these cases, so users would most likely have to start typing out the name of the package they want to import rather than trusting the model to know they are starting a machine learning project and want to import either PyTorch or TensorFlow." |
| Q224 | 34 | output_form | "As one example, we looked at completions of the prompt: # import machine learning package import and found that over 100 completions of 100 tokens, 6 contained suggestions for TensorFlow and 3 for PyTorch, two libraries that are rough substitutes." |
| Q225 | 35 | input_ontology | "Most past studies of the impacts of code generation models consider performance on a closed set of tasks in a simulated environment (Xu et al., 2021)." |
| Q226 | 35 | input_ontology | "As the deployment of Codex and other near-term technologies proceeds, we may be able to conduct more robust experiments examining the impact of various strengths of models on real-world job performance, across teams and across firms." |
| Q227 | 35 | output_content | "Precise and accurate prediction of any impacts without user or market signal is difficult, but the potential implications on the long-run labor market and the possibility of disparate outcomes across groups warrant further exploration of these issues." |
| Q228 | 35 | input_ontology | "It may be possible to assess the relative likelihood of different scenarios by building a deeper understanding of Codex's capabilities across several code-related tasks or by studying the effects of precise deployment scenarios." |

---

## Regional Context

```yaml
name: US Professional Software Developers — Python API Documentation Generation
abbreviation: US-SW-APIDOC
deployment_context:
  country: United States
  organization_type: US software company (internal tooling evaluation)
  deployment_scope: Internal evaluation by senior engineers and technical writers;
    downstream consumption by external developer community
  task: LLM-assisted generation of API reference documentation (Google-style docstrings,
    Sphinx-rendered) from Python source code modules
  task_direction: code → prose documentation (inverse of HumanEval's docstring → code
    direction)
target_population:
  primary_evaluators: Senior software engineers and technical writers employed at
    the commissioning company, fluent in Python conventions, Google-style docstring
    standards, and Sphinx rendering behavior
  end_consumers: External software developers consuming the generated API reference
    documentation via Sphinx-rendered HTML or IDE tooling
  relevant_expertise: Professional Python development; familiarity with SDK-style
    codebases; Google developer documentation style; type annotation conventions (PEP
    484, PEP 526)
  language: English technical prose
  sub_national_variation: Not a primary concern — population is defined by professional
    role and technical fluency, not geography within the US
languages:
  natural_language: English
  code_language: Python
  documentation_standard: Google-style docstrings rendered via Sphinx
  note: High-resource language pair (English + Python); no script mismatch, no modality
    mismatch with benchmark
codebase_characteristics:
  class_hierarchy_depth: Deep class hierarchy in core SDK; inheritance relationships
    must be reflected in generated docs
  decorator_patterns: Heavy decorator use for auth and caching wrappers; documented
    interface may differ from raw function signature
  async_patterns: Async/await throughout network layer; async-aware documentation
    required
  module_interdependencies: Inter-dependent modules where understanding one function
    requires context from related helpers
  documentation_target: All public parameters, return values, raised exceptions, and
    side effects
evaluation_design:
  ground_truth_availability: No pre-existing reference documentation; multiple phrasings
    acceptable if factually accurate
  primary_evaluation_method: Human judgment by senior engineers and technical writers
  supplementary_evaluation: Automated checks for parameter name coverage and type-annotation
    consistency
  primary_failure_mode: Hallucinated parameters or incorrect return-type descriptions
  evaluation_dimensions:
  - dimension: factual_accuracy
    description: Correct descriptions of parameters, return types, side effects, and
      behavior
    criticality: HIGH
  - dimension: completeness
    description: All public params, returns, and raises documented; no omissions
    criticality: HIGH
  - dimension: type_annotation_correctness
    description: Generated type signatures match actual signatures; no hallucinated
      types; IDE autocomplete reliability
    criticality: HIGH
  - dimension: google_style_format_compliance
    description: Adherence to Google-style docstring schema as rendered through Sphinx
    criticality: HIGH
  - dimension: clarity
    description: Prose readable and unambiguous for the target developer audience
    criticality: MEDIUM-HIGH
  - dimension: decorator_awareness
    description: Documentation reflects the wrapped interface and decorator effects,
      not just the inner function
    criticality: HIGH
  - dimension: inheritance_awareness
    description: Inherited methods and overridden behaviors accurately described in
      SDK class hierarchy context
    criticality: HIGH
  - dimension: async_correctness
    description: Async/await semantics and concurrency behavior accurately described
    criticality: HIGH
benchmark_alignment_profile:
  benchmark: HumanEval
  overall_validity: LOW — near-total task-direction mismatch; benchmark evaluates
    docstring→code, deployment requires code→documentation prose
  dimension_gaps:
  - dimension: input_ontology
    severity: HIGH
    note: HumanEval tests prose→code; deployment requires code→prose; decorator, inheritance,
      async patterns entirely absent from benchmark task taxonomy
  - dimension: input_content
    severity: HIGH
    note: 164 standalone algorithmic puzzles vs. complex real-world SDK with auth
      wrappers, async layers, and deep class hierarchies
  - dimension: input_form
    severity: LOW
    note: Both use Python source and English; no modality or script mismatch
  - dimension: output_ontology
    severity: HIGH
    note: Benchmark output is executable code; deployment output is multi-dimensional
      structured prose
  - dimension: output_content
    severity: HIGH
    note: No annotators resembling senior engineers or tech writers; no inter-annotator
      agreement; hallucination detection requires domain experts absent from benchmark
  - dimension: output_form
    severity: HIGH
    note: Binary pass/fail via unit test harness vs. multi-dimensional human prose
      quality scoring (accuracy, completeness, clarity, style, type correctness)
flagged_benchmark_gaps:
- gap_id: 1
  label: Inverse task direction (code → documentation)
  description: No systematic benchmark tasks cover code-to-documentation-prose generation;
    HumanEval's docstring-generation experiment covers 10 samples/problem from one
    model only. CodeSearchNet provides (comment, code) pairs for code summarization
    but is designed for retrieval/summarization tasks rather than structured template-based
    API documentation generation. A 2025 INLG paper on 'Automated and Context-Aware
    Code Documentation' confirms that CodeSearchNet and CoDesc are 'primarily designed
    for code summarization, making them ill-suited for generating structured, template-based
    documentation' and lack contextual information such as class or package context.
  web_search_target: Python code to documentation generation LLM benchmark evaluation
    CodeSearchNet DocPrompting doc-generation
  search_finding: 'CodeSearchNet (Husain et al. 2020) and CoDesc are the closest public
    datasets but explicitly acknowledged as misaligned with structured template-based
    documentation generation. No benchmark specifically targeting Google-style or
    Sphinx-rendered API docstring generation from Python source has been identified.
    Gap confirmed as unresolved. Source: [WEB-1]'
- gap_id: 2
  label: Decorator and metaprogramming documentation
  description: No publicly known benchmark systematically tests documentation of decorator-wrapped
    functions where documented interface differs from raw function signature
  web_search_target: LLM code documentation benchmark decorator metaprogramming Python
    wrapped function evaluation
  search_finding: '[NOT FOUND — no benchmark covering decorator-aware documentation
    generation was surfaced in searches covering CodeSearchNet, ClassEval, and 2023–2025
    NLP/SE literature. Gap remains unresolved and novel.]'
- gap_id: 3
  label: Async/await and concurrency pattern documentation
  description: HumanEval contains no async Python; no code-documentation benchmark
    known to cover async patterns as a distinct category
  web_search_target: async Python code documentation LLM benchmark evaluation concurrency
    await
  search_finding: '[NOT FOUND — no benchmark specifically evaluating async/await documentation
    generation was surfaced. ClassEval and CodeSearchNet do not include async patterns
    as a distinct evaluation category. Gap confirmed unresolved.]'
- gap_id: 4
  label: Class hierarchy and inheritance documentation
  description: HumanEval is all standalone functions; no benchmark known to include
    class-level or inheritance-aware documentation tasks
  web_search_target: class hierarchy inheritance documentation generation LLM Python
    SDK benchmark evaluation
  search_finding: 'ClassEval (Du et al., 2023) is the first benchmark for class-level
    code generation (100 manually crafted Python class tasks, ~500 person-hours).
    It demonstrates a consistent 20–50 percentage-point drop in Pass@k compared to
    HumanEval function-level tasks, confirming class-level complexity degrades LLM
    performance. However, ClassEval evaluates code generation (natural language →
    code), not documentation generation (code → prose). A newer ClassEval-Pro (2025,
    300 tasks, 11 domains) extends coverage. Neither targets the documentation direction.
    ClassEval is a useful upper-bound comparator but does not resolve the class-level
    documentation gap. Sources: [WEB-2]; [WEB-3]'
- gap_id: 5
  label: Multi-dimensional prose quality evaluation
  description: No existing benchmark provides metrics for documentation clarity, completeness,
    or Google-style formatting compliance; HumanEval docstring grading is binary with
    no sub-dimensions
  web_search_target: documentation prose quality evaluation metrics LLM BARTScore
    G-Eval technical writing Google-style docstring rubric Sphinx
  search_finding: 'G-EVAL (Liu et al., 2023) is a general-purpose LLM-as-judge framework
    using chain-of-thought for multi-dimensional NLG evaluation; it has been applied
    to summarization quality dimensions (coherence, consistency, fluency, relevance)
    and is adaptable to documentation criteria. However, no G-EVAL application to
    Google-style docstring quality was found. A 2024 practitioner article on ''Evaluating
    an LLM code documentation generation application'' explicitly confirms ''a lack
    of well-defined quantitative metrics for evaluating the quality of free-text output''
    in documentation contexts, validating this as an open gap. Sources: [WEB-4];
    [WEB-5]'
- gap_id: 6
  label: Type annotation correctness as a distinct failure mode
  description: Hallucinated parameter types or return types are not measurable via
    pass@k; no known benchmark pairs ground-truth type signatures with documentation
    quality metrics
  web_search_target: Python type annotation correctness LLM evaluation hallucination
    parameter type return type benchmark PEP 484
  search_finding: 'CloudAPIBench (2024) measures API hallucination (incorrect API
    invocations, parameter names) in code generation, finding GPT-4o achieves only
    38.58% valid low-frequency API invocations. This is adjacent but not equivalent
    to type annotation correctness in documentation prose — it measures whether API
    calls are valid, not whether documented types match ground-truth signatures in
    docstrings. No benchmark specifically targeting type-annotation correctness in
    generated documentation was found. Source: [WEB-6]'
- gap_id: 7
  label: Human expert annotator population
  description: HumanEval docstring grading lacks documented annotator demographics,
    inter-annotator agreement, and expert-level reviewers matching the deployment's
    senior-engineer / tech-writer evaluators
  web_search_target: expert software engineer technical writer annotation LLM documentation
    evaluation inter-annotator agreement Google-style
  search_finding: '[NEEDS VERIFICATION — deferred: below search budget; likely unsearchable
    (annotator demographics for small-scale internal evaluations are rarely published).]'
- gap_id: 8
  label: Google-style / Sphinx docstring format compliance
  description: NOT DOCUMENTED — no HumanEval problem or evaluation criterion references
    Google-style docstring formatting, Sphinx rendering requirements, or any structured
    docstring schema; format compliance is entirely absent from the benchmark's output
    ontology
  web_search_target: Google-style docstring Sphinx format compliance LLM evaluation
    benchmark structured documentation
  search_finding: '[NOT FOUND — no benchmark specifically evaluating Google-style
    docstring format compliance or Sphinx rendering correctness was found in the literature.
    This remains an unresolved gap requiring custom evaluation protocol design.]'
docstring_format_requirements:
  style: Google-style docstrings
  renderer: Sphinx (sphinx.ext.napoleon or equivalent)
  required_sections:
  - Summary line
  - Args (with types and descriptions for all public parameters)
  - Returns (with type and description)
  - Raises (all documented exceptions)
  - Example (usage examples)
  applicable_style_guide: 'Google Python Style Guide — canonical living document maintained
    at google.github.io/styleguide/pyguide.html (no versioned releases; continuously
    updated). Docstring sections use indented blocks under section headers ending
    with colon (Args:, Returns:, Raises:, etc.), summary line ≤80 chars per PEP 257.
    Decorator docstrings must explicitly state the function is a decorator. Overriding
    methods may use brief ''See base class.'' docstrings unless behavior differs substantially.
    Source: [WEB-7]

    Note: Company-internal extensions are not searchable; must be confirmed with internal
    stakeholders.'
  sphinx_extension_config: 'sphinx.ext.napoleon is the current recommended extension,
    bundled with Sphinx since version 1.3. It supersedes the standalone sphinxcontrib-napoleon
    package (last released v0.7, still functional for Sphinx ≤1.2). For Google-style
    docstrings, enable via extensions = [''sphinx.ext.napoleon''] with napoleon_google_docstring
    = True in conf.py. Key configuration options affecting documentation output: napoleon_include_init_with_doc
    (default False), napoleon_include_special_with_doc (default True in sphinx.ext.napoleon),
    napoleon_use_param, napoleon_use_rtype, napoleon_attr_annotations (default True
    — uses PEP 484 type annotations from class attributes). Sources: [WEB-8];
    [WEB-9]'
infrastructure_notes:
  interface: Text-only; developers access generated docs via Sphinx-rendered HTML
    and IDE docstring popups (e.g., VS Code, PyCharm)
  ide_autocomplete_dependency: Type annotations in generated docs directly affect
    IDE autocomplete accuracy; hallucinated types cause downstream developer friction
  ci_integration: '[NEEDS VERIFICATION — deferred: low impact for scoring; requires
    internal stakeholder confirmation; not publicly searchable]'
  python_version_target: '[NEEDS VERIFICATION — deferred: low impact for scoring direction;
    requires internal confirmation. Note for assessors: PEP 484 type annotations are
    supported from Python 3.5+; PEP 526 variable annotations from 3.6+; union type
    syntax X | Y from 3.10+; parenthesized context managers from 3.10+. If codebase
    targets 3.10+, generated docs may use new-style union syntax not renderable by
    older Sphinx/napoleon configurations.]'
professional_and_regulatory_context:
  ip_and_licensing: '[NEEDS VERIFICATION — deferred: likely unsearchable (internal
    company policy); requires legal/policy stakeholder confirmation]'
  internal_doc_standards: '[NEEDS VERIFICATION — deferred: likely unsearchable (internal
    policy layered on Google style guide); requires internal stakeholder confirmation]'
  sdk_public_api_surface: '[NEEDS VERIFICATION — deferred: requires internal stakeholder
    confirmation; affects completeness requirements scoring but is not publicly determinable]'
domain_specific_notes: 'The deployment''s evaluation population (senior engineers
  and technical writers) is professionally specialized, not geographically or demographically
  diverse in ways relevant to standard regional benchmarking. The key population-level
  constraints are:

  - Shared professional fluency in Google-style docstring conventions and Sphinx rendering

  - High sensitivity to type annotation errors (IDE autocomplete dependency)

  - Expectation of decorator-aware, inheritance-aware, and async-aware documentation

  - No ground-truth reference docs; correctness is defined by expert human consensus

  - Primary risk is LLM hallucination of plausible-but-wrong parameter names, types,
  or return values


  The benchmark (HumanEval) was designed for an entirely different task direction
  (docstring→code) and output form (executable code, binary pass/fail). Validity for
  this deployment is near-zero on the dimensions of output ontology, output form,
  input ontology, and input content. The only partial coverage is on input form (shared
  Python + English substrate) and on the documented awareness of hallucination/misalignment
  failure modes.


  Downstream search should prioritize: code-to-documentation benchmarks (CodeSearchNet,
  DocPrompting), multi-dimensional prose quality evaluation frameworks (G-Eval, reference-free
  metrics applied to technical prose), and any evaluation suites covering decorator,
  async, or class-hierarchy documentation tasks.'
net_new_fields:
  class_level_code_generation_evidence:
    description: ClassEval (Du et al., 2023) is the first benchmark for class-level
      Python code generation (100 manually crafted tasks, ~500 person-hours). LLMs
      show a consistent 20–50 percentage-point drop in Pass@k compared to HumanEval
      function-level tasks. ClassEval-Pro (2025) extends to 300 tasks across 11 domains.
      Neither benchmark evaluates documentation generation from code, but both confirm
      that class-level complexity is a major LLM failure axis — directly informing
      the IC and IO gap severity for this deployment.
    relevance: Confirms that function-level benchmark scores (HumanEval) structurally
      underestimate failure rates on the class-level SDK patterns central to this
      deployment, even for the code-generation direction — making the gap even larger
      for the documentation-generation direction.
    sources: '[WEB-2]; [WEB-3]'
  code_documentation_generation_landscape:
    description: A 2025 INLG paper confirms that CodeSearchNet and CoDesc — the largest
      existing code-documentation datasets — 'are primarily designed for code summarization,
      making them ill-suited for generating structured, template-based documentation'
      and lack class/package context. A comparative analysis of LLMs for code documentation
      generation (Dvivedi et al., 2024) exists but evaluates only basic summarization
      metrics. No Python-specific, Google-style, or Sphinx-targeted documentation
      generation benchmark has been identified in the literature as of May 2025.
    relevance: Confirms gap_id 1 (inverse task direction) as a genuine hole in the
      evaluation landscape, not a gap that can be filled by redirecting an existing
      benchmark. Custom evaluation protocol is required.
    sources: '[WEB-1]; [WEB-10]'
  api_hallucination_evidence:
    description: CloudAPIBench (2024) measures API hallucination in code generation
      contexts. GPT-4o achieves only 38.58% valid low-frequency API invocations; Documentation
      Augmented Generation improves this to 47.94% for low-frequency APIs but degrades
      performance on high-frequency APIs by up to 39 percentage points.
    relevance: Provides quantitative evidence that LLM hallucination of API-related
      content (parameter names, types, invocation patterns) is a documented and measurable
      failure mode in adjacent contexts, supporting the deployment's identification
      of hallucinated parameter/type descriptions as the primary failure risk. The
      magnitude of low-frequency API hallucination is a useful prior for estimating
      hallucination rates in SDK documentation tasks.
    sources: '[WEB-6]'
  g_eval_applicability_for_documentation:
    description: G-EVAL (Liu et al., 2023) is a general-purpose LLM-as-judge framework
      using chain-of-thought prompting to evaluate NLG outputs on custom criteria
      without reference text. It has demonstrated strong correlation with human ratings
      on multi-dimensional prose quality dimensions. It has not been validated on
      technical documentation or Google-style docstring quality, but its reference-free,
      criteria-configurable design makes it the most readily adaptable existing framework
      for this deployment's evaluation needs.
    relevance: 'Addresses gap_id 5 (multi-dimensional prose quality evaluation): G-EVAL
      could be adapted with custom criteria (factual accuracy, completeness, Google-style
      compliance, type annotation correctness) to supplement human expert evaluation,
      particularly for scaling beyond the small expert annotator pool.'
    sources: '[WEB-4]'
  google_style_guide_decorator_documentation_requirement:
    description: The canonical Google Python Style Guide explicitly states 'A decorator
      docstring should clearly state that the function is a decorator.' This is a
      normative requirement in the authoritative style reference, confirming that
      decorator-awareness is a first-class documentation obligation under the target
      standard — not merely a deployment-specific preference.
    relevance: Directly supports the HIGH criticality rating for the decorator_awareness
      evaluation dimension. Any benchmark failing to test decorator-modified function
      documentation is missing a Google-style-required documentation pattern.
    sources: '[WEB-7]'
  sphinx_napoleon_inheritance_documentation_behavior:
    description: The Google Python Style Guide specifies that overriding methods 'may
      have a simple docstring sending the reader to its overridden method's docstring,
      such as "See base class."' but that substantially different behavior requires
      a full docstring. sphinx.ext.napoleon respects PEP 484 type annotations from
      class attributes (napoleon_attr_annotations=True by default in current Sphinx)
      and processes docstrings on modules, classes, attributes, methods, functions,
      and variables.
    relevance: Defines the normative behavior for inheritance documentation under
      the target standard — overriding method docs are conditionally required based
      on behavioral difference, which means LLM evaluation must assess whether the
      generated override docstring correctly identifies behavioral differences, not
      merely whether a docstring is present.
    sources: '[WEB-7]; [WEB-8]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/html/2509.14273v1 |
| WEB-2 | https://arxiv.org/abs/2308.01861 |
| WEB-3 | https://arxiv.org/html/2604.26923 |
| WEB-4 | https://arxiv.org/pdf/2303.16634 |
| WEB-5 | https://medium.com/gft-engineering/evaluating-an-llm-code-documentation-generation-application-719b57f801e5 |
| WEB-6 | https://arxiv.org/abs/2407.09726 |
| WEB-7 | https://google.github.io/styleguide/pyguide.html |
| WEB-8 | https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html |
| WEB-9 | https://sphinxcontrib-napoleon.readthedocs.io/ |
| WEB-10 | https://arxiv.org/pdf/2312.10349 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: HumanEval tests generation of code *from* docstrings, but your system generates documentation prose *from* code. Beyond basic function descriptions, does your system need to handle specific documentation patterns common in your codebase — for example, complex class hierarchies, decorator-modified functions, async/await patterns, or modules with extensive interdependencies between functions?
A1: Yes — the codebase has all of these patterns: a deep class hierarchy in the core SDK, heavy decorator use (auth, caching wrappers), async/await throughout the network layer, and inter-dependent modules where understanding one function requires context from related helpers. Documentation must correctly reflect inheritance relationships and explain decorator effects on wrapped function behavior, not just describe the inner function in isolation.

Q2 [OO]: For your API documentation output, how is correctness defined — is a description 'correct' only if it matches a ground-truth reference doc, or do multiple valid phrasings count as equally acceptable? Would your team evaluate quality by automated means, human reviewer judgment, or both?
A2: No ground-truth reference docs exist; multiple phrasings are acceptable provided they are factually accurate about parameters, return types, side effects, and behavior. Evaluation will be primarily human judgment by senior engineers and tech writers, potentially supplemented by automated checks for parameter name coverage and type-annotation consistency. The primary failure mode is hallucinated parameters or incorrect return-type descriptions.

Q3 [OF]: HumanEval measures functional correctness via unit tests passing (binary signal). For your use case, outputs are technical prose — does evaluation need to assess dimensions like clarity, completeness, formatting compliance, or accuracy of type annotations, beyond simple correctness?
A3: Yes, far beyond binary correctness. Required dimensions include: clarity for the reader, completeness (all public params/returns/raises documented), adherence to Google-style docstring format rendered through Sphinx, and accurate type annotations (developers rely on them for IDE autocomplete). Evaluation must catch LLM-invented plausible-but-wrong types.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | HumanEval covers docstring-to-code generation of isolated, self-contained functions; the deployment requires code-to-prose documentation covering decorators, inheritance hierarchies, async patterns, and cross-function context — categories entirely absent from the benchmark's test-case ontology. |
| IC | HIGH | HumanEval's 164 problems are simple, standalone algorithmic puzzles; the deployment's source code involves complex real-world SDK patterns (auth wrappers, async layers, interdependencies) whose documentation requirements the benchmark instances do not represent. |
| IF | LOWER | Both benchmark and deployment are text-only, use Python source, and target a high-resource language (English); no modality or script mismatch exists. |
| OO | HIGH | HumanEval's output space is executable Python scored by unit test pass/fail (binary); the deployment requires multi-dimensional prose quality scoring (accuracy, completeness, clarity, style conformance, type correctness) with no overlap in scoring mechanism or output category design. |
| OC | HIGH | HumanEval labels are objectively determined by unit test outcomes, whereas the deployment's ground truth is subjective human expert judgment on prose accuracy — annotator-population mismatch is total, and hallucination detection requires domain-expert reviewers absent from the benchmark's validation process. |
| OF | HIGH | HumanEval output is executable code evaluated by automated test harness; deployment output is structured technical prose evaluated across clarity, completeness, Google-style formatting, and type annotation correctness — the output form, representation, and scoring apparatus are entirely misaligned. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** openai/openai_humaneval
**Analysis date:** 2025-01-31
**Examples reviewed:** 40 from `test` split (164 total)
**Columns shown:** task_id, prompt, canonical_solution, test, entry_point
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | openai_humaneval | HumanEval/0 | pass/fail | `def has_close_elements(numbers: List[float], threshold: float) -> bool:` `""" Check if in given list of numbers, are any two numbers closer to each other than given threshold.` | Standalone function with type-annotated signature and brief docstring — exemplifies the benchmark's canonical input format | IO, IC |
| D2 | openai_humaneval | HumanEval/61 | pass/fail | `def correct_bracketing(brackets: str):` `""" brackets is a string of "(" and ")". return True if every opening bracket has a corresponding closing bracket.` | Single-function bracket-balancing puzzle — no class, decorator, async, or inheritance context | IO, IC |
| D3 | openai_humaneval | HumanEval/38 | pass/fail | `def encode_cyclic(s: str):` `""" returns encoded string by cycling groups of three characters. """` / `def decode_cyclic(s: str):` `""" takes as input string encoded with encode_cyclic function. Returns decoded string. """` | Two-function prompt with minimal docstrings — closest analog to multi-function context in the sample, but still self-contained and non-hierarchical | IO, IC |
| D4 | openai_humaneval | HumanEval/130 | pass/fail | `def tri(n):` `"""Everyone knows Fibonacci sequence... Tribonacci sequence is defined by the recurrence: tri(1) = 3 tri(n) = 1 + n / 2, if n is even...` | Mathematical/algorithmic puzzle docstring → code — docstrings are input stimuli, not documentation targets | IO, OO |
| D5 | openai_humaneval | HumanEval/159 | pass/fail | `def eat(number, need, remaining):` `""" You're a hungry rabbit, and you already have eaten a certain number of carrots... Variables: @number : integer the number of carrots that you have eaten.` | One of the richer parameter-documentation examples in the sample; uses `@param` style, not Google-style `Args:` | IC, OO |
| D6 | openai_humaneval | HumanEval/32 | pass/fail | `def poly(xs: list, x: float):` `""" Evaluates polynomial with coefficients xs at point x. return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n """` | Helper function + main function pair in one prompt; still purely algorithmic, no class/decorator/async | IC, IO |
| D7 | openai_humaneval | HumanEval/11 | pass/fail | `from typing import List` `def string_xor(a: str, b: str) -> str:` `""" Input are two strings a and b consisting only of 1s and 0s. Perform binary XOR on these inputs and return result also as a string.` | Python `typing` module import present — confirms Python type-annotation syntax appears in benchmark | IF |
| D8 | openai_humaneval | HumanEval/17 | pass/fail | `from typing import List` `def parse_music(music_string: str) -> List[int]:` `""" Input to this function is a string representing musical notes in a special ASCII format.` | Another `typing`-annotated function; docstring is informal prose with embedded legend, not Google-style | IF, OO |
| D9 | openai_humaneval | HumanEval/124 | pass/fail | `def valid_date(date):` `"""You have to write a function which validates a given date string and returns True if the date is valid otherwise False. The date is valid if all of the following rules are satisfied: 1. The date string is not empty.` | Multi-rule validation function; docstring is numbered-list prose, not Google-style `Args:`/`Returns:` | OO, IC |
| D10 | openai_humaneval | HumanEval/88 | pass/fail | `def sort_array(array):` `""" Given an array of non-negative integers, return a copy of the given array after sorting... Note: * don't change the given array.` | No type annotations on parameters; informal `Note:` convention not matching Google-style | OO, IF |
| D11 | openai_humaneval | HumanEval/109 | pass/fail | `def move_one_ball(arr):` `"""We have an array 'arr' of N integers arr[1], arr[2], ..., arr[N]...` `move_one_ball([3, 4, 5, 1, 2])==>True` | Longer docstring with inline examples using `==>` notation; no parameter type annotation; no Google-style section headers | OO, IC |
| D12 | openai_humaneval | HumanEval/95 | pass/fail | `def check_dict_case(dict):` `""" Given a dictionary, return True if all keys are strings in lower case or all keys are strings in upper case, else return False.` | No type annotations; informal docstring with inline examples; shadows Python builtin `dict` — a code quality anti-pattern | IC, OO |
| D13 | openai_humaneval | HumanEval/2 | pass/fail | `def truncate_number(number: float) -> float:` `""" Given a positive floating point number, it can be decomposed into and integer part... Return the decimal part of the number.` | Simple annotated function; docstring direction is prose→code; no `Raises:`, no `Args:` section | IO, OO |
| D14 | openai_humaneval | HumanEval/145 | pass/fail | `def order_by_points(nums):` `""" Write a function which sorts the given list of integers in ascending order according to the sum of their digits.` | No type annotation on parameter; inline `>>>` doctest examples embedded | OO, IF |
| D15 | openai_humaneval | HumanEval/37 | pass/fail | `def poly(xs: list, x: float):` `""" Evaluates polynomial with coefficients xs at point x. return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n """` | Contains `list` and `float` annotations without `typing` import — uses built-in type hints (Python 3.9+) | IF |
| D16 | openai_humaneval | HumanEval/104 | pass/fail | `def unique_digits(x):` `"""Given a list of positive integers x. return a sorted list of all elements that hasn't any even digit.` | No type annotations at all; docstring has no parameter section | OO |
| D17 | openai_humaneval | HumanEval/137 | pass/fail | `def compare_one(a, b):` `""" Create a function that takes integers, floats, or strings representing real numbers, and returns the larger variable in its given variable type. Return None if the values are equal.` | No type annotations; informal docstring style; no `Raises:` section | OO, IC |
| D18 | openai_humaneval | HumanEval/127 | pass/fail | `def intersection(interval1, interval2):` `"""You are given two intervals, where each interval is a pair of integers. For example, interval = (start, end) = (1, 2).` | No type annotations; describes parameter types informally in prose | OO |
| D19 | openai_humaneval | HumanEval/3 | pass/fail | `from typing import List` `def below_zero(operations: List[int]) -> bool:` `""" You're given a list of deposit and withdrawal operations on a bank account...` | Type-annotated; docstring describes behavior in informal narrative prose; no Google-style headers | IF, OO |
| D20 | openai_humaneval | HumanEval/21 | pass/fail | `def encode_cyclic(s: str):` `""" returns encoded string by cycling groups of three characters. """` | Minimal one-line docstring; `encode_cyclic` has full function body visible in prompt; `decode_cyclic` docstring is the generation target | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Shared code substrate — Python source and English technical prose
- **Dimension(s):** IF
- **Observation:** Every example in the sample is Python source code with English-language natural language descriptions. Type annotation imports (`from typing import List`) appear in multiple prompts, indicating the benchmark operates in the same technical register as the deployment. The code substrate and language match the deployment's Python SDK context.
- **Deployment relevance:** The deployment generates documentation from Python source; HumanEval confirms the benchmark operates on the same fundamental signal (Python + English). There is zero modality mismatch — no script, dialect, or format conversion is required. This is the benchmark's strongest alignment property for this deployment.
- **Datapoint citations:**
  - [D7] Example HumanEval/11 (openai_humaneval, split=test): `"from typing import List"` `"def string_xor(a: str, b: str) -> str:"` — typed Python function with English docstring, matching deployment substrate
  - [D8] Example HumanEval/17 (openai_humaneval, split=test): `"from typing import List"` `"def parse_music(music_string: str) -> List[int]:"` — confirms typing module usage in benchmark mirrors deployment codebase conventions
  - [D19] Example HumanEval/3 (openai_humaneval, split=test): `"from typing import List"` `"def below_zero(operations: List[int]) -> bool:"` — further confirms consistent Python + English text-only format

#### Strength 2: Type annotation presence in a subset of prompts
- **Dimension(s):** IF, IC
- **Observation:** Approximately one-third of the sampled examples include explicit Python type annotations on function parameters and return values (e.g., `-> bool`, `-> str`, `-> List[int]`, `-> float`). Both PEP 484-style `typing` imports and Python 3.9+ built-in generic annotations appear.
- **Deployment relevance:** The deployment's primary failure mode is hallucinated parameter types. The benchmark at minimum exercises type-annotated function signatures as inputs, meaning models evaluated on HumanEval have been exposed to type annotation syntax — even though HumanEval does not evaluate type annotation correctness in output documentation.
- **Datapoint citations:**
  - [D1] Example HumanEval/0 (openai_humaneval, split=test): `"def has_close_elements(numbers: List[float], threshold: float) -> bool:"` — full parameter and return type annotations present
  - [D13] Example HumanEval/2 (openai_humaneval, split=test): `"def truncate_number(number: float) -> float:"` — simple float annotation, representative of deployment's type-annotation conventions
  - [D15] Example HumanEval/37 (openai_humaneval, split=test): `"def poly(xs: list, x: float):"` — uses built-in type hints without typing import, representing Python 3.9+ annotation style

#### Strength 3: Docstring-as-input demonstrates benchmark awareness of natural-language function descriptions
- **Dimension(s):** IC
- **Observation:** Every prompt includes a natural-language docstring describing function behavior, parameters, and expected outputs. The docstrings vary in richness from one-liners (D20: `"returns encoded string by cycling groups of three characters."`) to multi-paragraph descriptions with parameter sections (D5: uses `@param`-style variable descriptions with constraints). This range confirms the benchmark contains functional natural-language descriptions of Python functions, the same raw material the deployment would generate.
- **Deployment relevance:** While the task direction is reversed (docstrings are inputs, not outputs), the presence of natural-language function descriptions confirms the benchmark has been used to study the relationship between docstrings and code — giving weak but non-zero evidence that evaluated models have learned to associate function semantics with natural-language descriptions.
- **Datapoint citations:**
  - [D5] Example HumanEval/159 (openai_humaneval, split=test): `"Variables: @number : integer the number of carrots that you have eaten. @need : integer the number of carrots that you need to eat. @remaining : integer the number of remaining carrots thet exist in stock"` — richer parameter description style present in benchmark
  - [D11] Example HumanEval/109 (openai_humaneval, split=test): `"We have an array 'arr' of N integers arr[1], arr[2], ..., arr[N].The numbers in the array will be randomly ordered."` — longer prose description of function behavior

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Entire task direction is inverted — benchmark measures prose→code, deployment requires code→prose
- **Dimension(s):** IO, OO
- **Observation:** Every single example in the dataset has the same structure: a natural-language docstring is the **input** prompt, and executable Python code is the **output** being evaluated. The schema confirms this: fields are `prompt` (docstring), `canonical_solution` (code body), and `test` (unit tests for pass/fail scoring). There is no example in the dataset where Python code is the input and a natural-language docstring is the target output.
- **Deployment relevance:** The deployment requires generating API reference documentation (function descriptions, parameter explanations, return value specifications) **from** Python source code. The benchmark evaluates the completely opposite transformation. Not a single benchmark item exercises the code→documentation direction that the deployment requires.
- **Datapoint citations:**
  - [D4] Example HumanEval/130 (openai_humaneval, split=test): `"tri(1) = 3 / tri(n) = 1 + n / 2, if n is even..."` — the mathematical recurrence specification is the **input** prompt; the task is to synthesize a Python function from it
  - [D2] Example HumanEval/61 (openai_humaneval, split=test): `"brackets is a string of '(' and ')'. return True if every opening bracket has a corresponding closing bracket."` — prose description is input; Python implementation is the target
  - [D20] Example HumanEval/38 (openai_humaneval, split=test): `"takes as input string encoded with encode_cyclic function. Returns decoded string."` — docstring is input; a one-line code body is the target output

#### Concern 2: No examples involve decorators, class hierarchies, async/await, or module interdependencies
- **Dimension(s):** IO, IC
- **Observation:** All 40 sampled examples are standalone, self-contained functions with no class context, no decorator wrappers, no `async def` signatures, and no cross-module dependencies. The most complex structural example is HumanEval/38, which includes a helper function (`encode_cyclic`) visible in the prompt, but both functions remain standalone and procedural. No example references `self`, class attributes, inheritance, `@property`, `@staticmethod`, `@classmethod`, authentication decorators, caching wrappers, or coroutine patterns.
- **Deployment relevance:** The deployment's codebase features "a deep class hierarchy in the core SDK, heavy decorator use (auth, caching wrappers), async/await throughout the network layer, and inter-dependent modules." The benchmark contains zero instances of these patterns. A model scoring well on HumanEval may fail completely on decorator-aware, inheritance-aware, or async-aware documentation generation — the benchmark provides no signal on these failure modes.
- **Datapoint citations:**
  - [D3] Example HumanEval/38 (openai_humaneval, split=test): `"def encode_cyclic(s: str):"` / `"def decode_cyclic(s: str):"` — closest thing to multi-function context; both are standalone procedural functions, no class or decorator involvement
  - [D6] Example HumanEval/32 (openai_humaneval, split=test): `"def poly(xs: list, x: float):"` / `"def find_zero(xs: list):"` — two-function prompt; both are mathematical utility functions with no OOP or async patterns
  - [D1] Example HumanEval/0 (openai_humaneval, split=test): `"def has_close_elements(numbers: List[float], threshold: float) -> bool:"` — typical standalone function; no class, decorator, or async context anywhere in the prompt

#### Concern 3: Output scoring is binary pass/fail via unit tests — no mechanism for multi-dimensional prose quality evaluation
- **Dimension(s):** OO, OF
- **Observation:** The dataset schema contains a `test` field with Python `assert` statements that execute the generated code. The canonical evaluation is whether the generated code passes these assertions. There is no field for documentation quality scores, no rubric for Google-style formatting compliance, no completeness metric, and no type annotation accuracy label. The scoring apparatus is entirely binary and automated.
- **Deployment relevance:** The deployment requires evaluation across five dimensions: factual accuracy of parameter/return/side-effect descriptions, completeness (all public params/returns/raises documented), Google-style format compliance (Sphinx-renderable), type annotation correctness, and clarity. HumanEval's binary pass/fail unit test harness has zero overlap with any of these evaluation dimensions.
- **Datapoint citations:**
  - [D2] Example HumanEval/61 (openai_humaneval, split=test): `"assert candidate('()')"` / `"assert not candidate('((()())))')"` — unit tests check code functional behavior; no documentation quality criterion present
  - [D14] Example HumanEval/145 (openai_humaneval, split=test): `"assert candidate([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]"` — pure functional assertion; no dimension of documentation quality is measurable from this test structure
  - [D9] Example HumanEval/124 (openai_humaneval, split=test): `"assert candidate('03-11-2000') == True"` — correctness defined entirely by return value; documentation style is irrelevant to the scoring

#### MAJOR

#### Concern 4: Docstring style in benchmark inputs is inconsistent and predominantly non-Google-style
- **Dimension(s):** OO, IC
- **Observation:** Examining the docstrings across 40 examples, none follow the Google-style `Args:` / `Returns:` / `Raises:` section format that the deployment requires. Styles observed include: inline `>>>` doctest examples (D1, D2, D8, D14), numbered-list prose rules (D9), `@variable` parameter labels (D5), informal `Note:` blocks (D10, D11), `==>` notation for examples (D11), and single-sentence descriptions with no parameter documentation at all (D20). Even examples with type annotations do not pair them with Google-style argument descriptions.
- **Deployment relevance:** The deployment's evaluation criteria include adherence to Google-style docstring format rendered through Sphinx. Models trained and evaluated on HumanEval's docstring style corpus have never been rewarded or penalized for Google-style compliance. The benchmark's docstrings actively demonstrate alternative, non-compliant styles — meaning models evaluated here may have internalized conventions that conflict with the deployment's formatting requirements.
- **Datapoint citations:**
  - [D5] Example HumanEval/159 (openai_humaneval, split=test): `"Variables: @number : integer the number of carrots that you have eaten."` — uses `@param` style, not Google-style `Args:` section
  - [D11] Example HumanEval/109 (openai_humaneval, split=test): `"move_one_ball([3, 4, 5, 1, 2])==>True / Explanation: By performin 2 right shift operations..."` — informal `==>` notation with spelling error ("performin"); non-compliant with any docstring standard
  - [D10] Example HumanEval/88 (openai_humaneval, split=test): `"Note: * don't change the given array."` — informal bullet note, not a Google-style `Note:` section header
  - [D9] Example HumanEval/124 (openai_humaneval, split=test): `"The date is valid if all of the following rules are satisfied: 1. The date string is not empty."` — numbered rules embedded in docstring prose; no `Args:` or `Returns:` section

#### Concern 5: Most function prompts lack type annotations — no consistent type information to evaluate
- **Dimension(s):** OO, IC
- **Observation:** A substantial fraction of the 40 sampled examples (roughly 60%) have no type annotations on function parameters or return values: HumanEval/88, /95, /104, /105, /109, /121, /123, /127, /130, /132, /137, /144, /145, /154, /158, /159. These functions use bare `def` signatures with no type hints, providing no ground-truth type information in the prompt.
- **Deployment relevance:** The deployment's primary failure mode is hallucinated parameter types or incorrect return-type descriptions, and type annotation correctness is a HIGH-criticality evaluation dimension. Because the benchmark's own prompts frequently lack type annotations, it cannot serve as a proxy for evaluating whether a model correctly infers and documents types from annotated SDK code. The absence of type annotations also means HumanEval cannot surface hallucinated-type failures even if the task direction were reversed.
- **Datapoint citations:**
  - [D16] Example HumanEval/104 (openai_humaneval, split=test): `"def unique_digits(x):"` — no type annotation on parameter or return value
  - [D17] Example HumanEval/137 (openai_humaneval, split=test): `"def compare_one(a, b):"` — no type annotations; informal description of accepted types in prose: "takes integers, floats, or strings representing real numbers"
  - [D18] Example HumanEval/127 (openai_humaneval, split=test): `"def intersection(interval1, interval2):"` — no type annotations; parameter types described informally as "pair of integers"
  - [D12] Example HumanEval/95 (openai_humaneval, split=test): `"def check_dict_case(dict):"` — no type annotations; shadows Python builtin `dict`

#### Concern 6: Ground-truth labels are determined by automated unit tests with no human annotator involvement
- **Dimension(s):** OC
- **Observation:** All 164 examples use the `test` field — programmatically executed `assert` statements — as the sole ground-truth correctness criterion. No human annotator is involved in labeling. The schema has no annotation fields beyond the unit test assertions. The dataset card tags include `annotations_creators:expert-generated`, but this refers to the hand-written problem design, not to human judgment of output quality.
- **Deployment relevance:** The deployment's evaluation will be "primarily human judgment by senior engineers and tech writers." The primary failure mode — hallucinated but plausible-sounding parameter descriptions — is by definition undetectable by automated unit tests (which measure code execution, not prose accuracy). The benchmark's labeling methodology has zero overlap with the deployment's evaluation methodology.
- **Datapoint citations:**
  - [D2] Example HumanEval/61 (openai_humaneval, split=test): `"assert candidate('()')"` / `"assert not candidate(')')"` — ground truth is fully determined by code execution outcome; no human judgment of documentation quality
  - [D14] Example HumanEval/145 (openai_humaneval, split=test): `"assert candidate([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]"` — purely computational ground truth; annotator identity and expertise are irrelevant and undocumented

#### MINOR

#### Concern 7: Problem set represents puzzle/algorithmic tasks not representative of SDK utility function documentation
- **Dimension(s):** IC
- **Observation:** The 40 sampled examples consist predominantly of mathematical algorithms (Tribonacci sequence D4, polynomial root finding D6, Collatz conjecture D20), combinatorial puzzles (cyclic bracket checking D2, palindrome detection D23), and toy utility functions (fruit basket subtraction D29, carrot-eating simulation D30). None involve network I/O, authentication flows, caching logic, error handling in distributed systems, or any domain pattern typical of SDK codebases.
- **Deployment relevance:** The deployment's SDK codebase involves auth wrappers, async network layers, and inter-dependent modules. The documentation challenges in those contexts (correctly describing rate-limiting behavior, propagated exceptions, coroutine semantics) are categorically different from the puzzle-function documentation challenges in HumanEval. Models fine-tuned or evaluated only on puzzle-style tasks may not generalize to the register and domain of SDK API documentation.
- **Datapoint citations:**
  - [D4] Example HumanEval/130 (openai_humaneval, split=test): `"Tribonacci sequence is defined by the recurrence: tri(1) = 3 tri(n) = 1 + n / 2, if n is even."` — mathematical recurrence definition; no analog in SDK documentation
  - [D29] Example HumanEval/67 (openai_humaneval, split=test): `"In this task, you will be given a string that represents a number of apples and oranges that are distributed in a basket of fruit"` — toy scenario; no relevance to SDK or API documentation domain
  - [D30] Example HumanEval/159 (openai_humaneval, split=test): `"You're a hungry rabbit, and you already have eaten a certain number of carrots"` — narrative-framed toy problem; entirely unlike the register of technical API documentation

#### Concern 8: Raises/exceptions documentation entirely absent from benchmark
- **Dimension(s):** OO
- **Observation:** None of the 40 sampled examples document exceptions that a function may raise, and no unit test validates exception-raising behavior as a primary concern. The `Raises:` section of Google-style docstrings — one of the four required documentation sections — has no representative in the benchmark.
- **Deployment relevance:** The deployment requires documenting "all public params, returns, and raises." The benchmark provides no signal whatsoever on whether a model can correctly identify and document the exceptions a function raises, including inherited or re-raised exceptions from decorated or async functions.
- **Datapoint citations:**
  - [D9] Example HumanEval/124 (openai_humaneval, split=test): `"The date is valid if all of the following rules are satisfied..."` — date validation function that raises no documented exceptions despite multiple potential failure modes (empty string, wrong format)
  - [D1] Example HumanEval/0 (openai_humaneval, split=test): `"def has_close_elements(numbers: List[float], threshold: float) -> bool:"` — no `Raises:` documentation present; no unit test exercises exception behavior

---

### Content Coverage Summary

The 40 sampled examples uniformly represent the benchmark's core design: self-contained, standalone Python functions presented with a natural-language docstring as input, paired with a canonical code body and unit tests as ground truth. Topics are drawn entirely from algorithmic puzzles and toy utility functions — bracket balancing, sequence computation, string manipulation, mathematical operations, list transformations. Problem framing is often playful or abstract (carrot-eating rabbits, flying objects, musical notes).

Docstring style across the sample is heterogeneous and predominantly informal: inline `>>>` doctest notation, numbered lists, `==>` example notation, `@variable` labels, and brief single-sentence descriptions all appear. No example uses Google-style `Args:` / `Returns:` / `Raises:` section headers. Approximately one-third of examples include Python type annotations (PEP 484 / `typing` module), while the majority use bare untyped signatures.

The benchmark is entirely text-based, English-language, Python-source — matching the deployment's modality. However, every example is structured as docstring→code (prose is input, code is output), the exact inverse of the deployment's code→documentation direction. No class methods, decorated functions, async functions, or multi-module dependency chains appear in any sampled example. Ground-truth labels are purely computational (unit test pass/fail), with no human judgment component.

---

### Limitations

1. **Sample coverage**: 40 of 164 examples were reviewed (24%). The remaining 124 examples could contain patterns not observed here, though the benchmark's documented design (standalone function synthesis) makes this unlikely for the highest-priority gaps (decorators, async, class hierarchies).

2. **No inspection of the docstring-generation experiment**: The paper describes a secondary Codex-D experiment grading docstring generation by hand for 10 samples/problem, but this experiment's data is not in the HuggingFace dataset — only the standard code-synthesis prompts are present. The quality and format of those hand-graded docstrings cannot be assessed from this dataset.

3. **No canonical_solution complexity analysis**: The canonical solutions were not systematically analyzed for complexity, length, or structural patterns. It is possible that some solutions contain patterns (e.g., class usage, exception handling) not visible from the prompts alone.

4. **Inter-annotator agreement and annotator demographics**: These are not assessable from the dataset content — they require consulting the paper's methodology, which documents that annotator demographics are undocumented and no inter-annotator statistics were computed.

5. **Coverage of all 164 problems' docstring styles**: The non-Google-style docstring observation is based on 40 examples; the full 164-problem set may contain some Google-style formatted prompts, though this would be incidental rather than systematic.

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
  "region": "US Professional Software Developers — Python API Documentation Generation",
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
