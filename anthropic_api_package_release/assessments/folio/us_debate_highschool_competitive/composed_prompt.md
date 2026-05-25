I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **FOLIO: Natural Language Reasoning with First-Order Logic** is valid for use in **US High School Competitive Debate — Argument Quality Assessment**.

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

- **Name**: folio
- **Full Name**: FOLIO: Natural Language Reasoning with First-Order Logic
- **Domain**: Logical reasoning / Natural language inference
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2022

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
FOLIO defines two primary tasks: a natural language reasoning task (deductive entailment:
True/False/Unknown given NL premises) [Q15, Q63] and an NL-to-FOL translation task [Q3,
Q18, Q67]. Task complexity is operationalized by reasoning depth — the modal depth in FOLIO
is four, with 28.7% of examples requiring five or more inference steps [Q60], and FOLIO
exhibits substantially more distinct abstract syntax trees than prior datasets [Q61]. The
reasoning task is explicitly framed as an independent evaluation of logical reasoning [Q7].
Subtask variety includes syllogistic reasoning patterns with conjunction, disjunction, and
implication [Q43], as well as discourse-level multi-premise translation [Q71, Q72].

The ontology contains no task types corresponding to inductive reasoning, evidentiary
argument assessment, rhetorical effectiveness, value-laden claim evaluation, or debate-specific
structural moves (disadvantages, counterplans, kritiks). Prior datasets are criticized for
having fewer than 50 distinct ASTs and limited reasoning depth [Q11, Q12, Q13], motivating
FOLIO's design, but the coverage gap relative to the deployment remains total: the benchmark's
taxonomy is organized exclusively around formal deductive inference [Q9, Q10].

### Input Content
FOLIO data were collected via two complementary methods [Q33]. WikiLogic had annotators
select random Wikipedia articles as topical seeds and write new stories from scratch [Q34],
yielding 304 stories and 74% of the total 4,351-word vocabulary [Q38, Q62]. HybLogic used
algorithmically generated syllogism templates that annotators instantiated with real-world
noun phrases and clauses [Q39, Q40, Q42, Q44]. Both tracks were developed specifically to
achieve logical diversity and natural language variety [Q33]. The dataset explicitly avoids
biases and stereotypes linked to identity markers and steers clear of opinionated language
and normatively contested content [Q47, Q127]. Stories with factual inaccuracies were
rewritten [Q126], and "psychologically fundamental generalizations" are accepted as a
deliberate design choice [Q128]. 39.2% of stories were found to have quality issues and
were rewritten under a detailed protocol [Q48].

Crucially for the deployment, neither track contains content resembling competitive debate
arguments: there are no empirical claims with disputed evidence, no value-laden assertions,
and no argumentative exchanges between opposing positions. WikiLogic stories may overlap
with LLM pretraining corpora [Q104], and HybLogic stories exhibit learnable structural
patterns exploitable by fine-tuned models [Q105].

### Input Form
All FOLIO examples are text-only, consisting of natural language premise sets and
conclusions annotated with parallel FOL formulas [Q64, Q65]. The dataset is written in
standard American English with careful attention to grammatical naturalness — all sentences
were checked with Grammarly and reviewed by annotators with English Literature backgrounds
[Q49, Q50]. NL conventions were standardized (e.g., "either-or" for exclusive disjunction,
"A or B, or both" for inclusive disjunction, naturalistic quantifier phrasing) [Q130, Q131,
Q132, Q133]. The train/validation/test split is 70%/15%/15% (1,001/203/226 examples),
split by story to prevent contamination [Q78, Q79]. FOL syntax follows the Russell and
Norvig (2010) standard [Q52]. The dataset is entirely text-based, in English, with no
modality or script mismatch relative to the deployment context [Q22, Q161].

### Output Ontology
FOLIO's output label space is a three-way categorical scheme — True, False, or Unknown —
applied to each conclusion given its premise set [Q36, Q66]. The majority baseline in the
test set is 38.5% (87 true, 78 false, 61 unknown) [Q94]. FOL operators supported include
negation, conjunction, disjunction, implication, universal and existential quantifiers, and
equality [Q138]; n-place predicates are used for expressivity [Q141]. FOL is characterized
as unambiguous, enabling exact truth-value derivation via theorem proving [Q135, Q136, Q137].
Temporal logic and modal logic are explicitly excluded as out of scope [Q139, Q140], and
Davidsonian/neo-Davidsonian semantics are also excluded [Q142]. 5% of conclusions have
complex syntactic structures posing comprehension challenges even for GPT-4 [Q120].

The output ontology is categorically mismatched to the deployment's requirements: the
three-way entailment label cannot represent multi-dimensional sub-scores (evidence quality,
relevance, persuasive effectiveness), qualitative coaching feedback, pairwise comparative
rankings, or format/circuit-conditioned quality norms.

### Output Content
The logical correctness of all labels is guaranteed by automatic verification through an
FOL inference engine, not by human judgment of plausibility or argument quality [Q2].
The annotation pipeline covered six stages consuming 980 person-hours [Q32], with NL
quality checks performed only by NLP/computational linguistics experts and FOL quality
checks only by FOL experts [Q29, Q124, Q125]. All stories and FOL annotations were
reviewed by senior researchers [Q31, Q115]. Annotators were CS undergraduate and graduate
students with formal education in first-order logic [Q16, Q27, Q28, Q122, Q123], all
native English speakers or near-native proficient [Q27, Q110].

The human performance gap between expert annotators (CS students familiar with FOL,
95.98% accuracy) and non-experts (community college/high school students unfamiliar with
FOL, 61.82%) is 34.16% [Q107, Q108, Q109, Q111], confirming that domain knowledge of
FOL is necessary for good performance [Q112]. The annotator population is entirely unlike
the deployment's quality-defining community (debate judges, coaches, NSDA/TOC community
members), and the ground-truth labels are mechanically derived from a formal inference
engine — not from pluralistic human judging norms.

### Output Form
For the NL reasoning task, the primary metric is accuracy over three-way categorical
labels [Q80]. For the NL-FOL translation task, two metrics are used: Syntactic Validity
(SynV, binary pass/fail on syntactic check) [Q73, Q74] and Inference Engine Execution
Accuracy (ExcAcc, whether translated FOL reproduces correct truth values via the inference
engine) [Q75, Q76]. Experiments are run over five randomly sampled training sets with
averaged results [Q93]. Confusion matrix analysis shows LLMs are significantly better on
True-labeled conclusions than False or Unknown [Q155, Q156, Q157]. Premise ordering is
confirmed not to carry significant label-predictive signal [Q158, Q159, Q160]. The
translation metric is acknowledged as insufficiently reliable, with better metrics
deferred to future work [Q77].

The output form is a single categorical label produced by a theorem prover [Q153]; the
evaluation framework produces no multi-dimensional scores, free-text rationales, or
pairwise comparative outputs. This represents a fundamental output-form mismatch: benchmark
performance metrics (accuracy over True/False/Unknown) are structurally uninformative for
the deployment's validity requirements.

### Stated Limitations
The authors acknowledge that existing NL benchmarks are inadequate for measuring complex
logical reasoning [Q8, Q9, Q10], and several self-identified limitations bear on validity.
The dataset is intentionally small and high-quality rather than large-scale [Q114]; scaling
is acknowledged as beyond current resources [Q116], with community expansion encouraged
[Q117]. The NL-FOL translation metric is acknowledged as insufficiently reliable [Q77].
GPT-4's use of commonsense shortcuts leading to wrong conclusions is flagged as a model
failure mode [Q121]. The 8-shot maximum context window constraint for text-davinci-002
is noted as a practical limitation [Q95]. The dataset explicitly avoids normatively charged
content [Q47], making it unsuitable for applications requiring assessment of contested
empirical or value-laden claims.


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

## Regional Context

```yaml
name: US High School Competitive Debate — Argument Quality Assessment
abbreviation: us_hs_debate
deployment_context:
  platform_type: Debate coaching platform (US-based, interscholastic)
  primary_use_case: LLM-based scoring of argument quality and delivery of qualitative
    coaching feedback for high school competitive debaters
  user_roles:
  - Student debaters (primary end users receiving scores and feedback)
  - Debate coaches (defining rubrics, interpreting output, calibrating platform standards)
  - Tournament judges (implicit quality-norm setters via circuit paradigms)
  interaction_mode: Text-based input (speech transcripts or written cases) and text-based
    output (sub-scores + qualitative coaching rationales)
target_population:
  description: United States high school students competing in NSDA-sanctioned and
    independent interscholastic debate. Students range across all four major competitive
    formats — Policy, Lincoln-Douglas (LD), Public Forum (PF), and Congressional Debate
    — and compete at both local/regional circuit events and national-circuit bid tournaments
    (TOC, NSDA Nationals). Quality standards are defined externally by NSDA norms,
    TOC circuit paradigms, and coaching staff rubrics rather than by the platform
    itself.
  country: United States
  sub_national_scope: Significant sub-national variation by regional circuit (e.g.,
    Texas lay circuits, California national-circuit hubs, Midwest lay circuits); see
    circuit_variation below.
  age_band: Approximately 14–18 years old (grades 9–12)
  approximate_student_population: '141,132 total NSDA student members as of 2024 (includes
    middle and high school, across all speech and debate events, not broken down by
    format); chapters at 3,152 high schools. Source: Wikipedia/NSDA — [WEB-1];
    corroborated by NSDA media page — [WEB-2].
    Note: NSDA membership figures cover all speech and debate events; format-level
    breakdowns (Policy vs. LD vs. PF vs. Congressional) are not publicly disaggregated.'
  approximate_school_programs: '3,152 high school chapters chartered with NSDA as
    of 2024. Source: Wikipedia/NSDA — [WEB-1].
    Note: this is the number of NSDA-chartered high school programs; programs competing
    outside NSDA or in independent circuits are not counted.'
languages:
  primary: English (American)
  register_variation: 'Significant register variation by format and circuit: spread/fast
    delivery in tech-circuit Policy and LD; conversational oratory register in Congressional;
    persuasive public rhetoric register in lay PF'
  technical_vocabulary:
  - 'Debate-format-specific jargon: disadvantage (DA), counterplan (CP), kritik (K),
    link, impact, turn, solvency, flow, shell, off-case, on-case, topicality (T),
    framework (FW), value/criterion (VC), contention, plan text, net benefit, permutation,
    burden of proof, fiat'
  - 'Evidence-handling terminology: card, cut card, tag, cite, warrant, extend, miscut,
    out-of-context evidence, recency'
  - 'Circuit/community terminology: TOC, bid, octafinals, NSDA, lay judge, tech judge,
    paradigm, flow, judge philosophy'
  minority_or_secondary_languages: None applicable to this deployment population
  note: All input and output is English text. No multilingual, RTL, or script considerations
    apply. Speech-to-text preprocessing may be relevant if audio is used as input,
    but current scope is text-only.
debate_formats:
  policy:
    description: Two-person teams debate a yearly national resolution (typically a
      federal government policy action). Rounds involve a case structure with plan,
      advantages, disadvantages, counterplans, and topicality arguments. National
      circuit is characterized by rapid delivery (spreading) and dense technical flows.
    typical_round_duration_minutes: 'Approximately 90–100 minutes total including
      cross-examination and preparation time. Speech times: 1AC 8 min, CX 3 min, 1NC
      8 min, CX 3 min, 2AC 8 min, CX 3 min, 2NC 8 min, CX 3 min, 1NR 5 min, 1AR 5
      min, 2NR 5 min, 2AR 5 min; each team also receives 8 minutes of preparation
      time. The prevailing 8/5-minute speech structure was introduced in the 1990s.
      Source: Wikipedia Structure of Policy Debate — [WEB-3];
      DebateUS — [WEB-4].'
    speech_structure: '8 speeches total in order: 1AC (8 min) → CX → 1NC (8 min) →
      CX → 2AC (8 min) → CX → 2NC (8 min) → CX → 1NR (5 min) → 1AR (5 min) → 2NR (5
      min) → 2AR (5 min). The 2NC+1NR together form the ''negative block'' (13 minutes).
      Each team receives 8 minutes of preparation time distributed across the round.
      Source: Wikipedia Structure of Policy Debate — [WEB-3].'
    argument_types_central:
    - Disadvantages (DAs)
    - Counterplans (CPs)
    - Topicality (T)
    - Kritiks (Ks)
    - Solvency arguments
    - Impact calculus
    quality_norm_axis: Strongly tech-circuit on national circuit; some local circuits
      remain flow-heavy but not speed-focused
  lincoln_douglas:
    description: Individual one-on-one debate on a bi-monthly NSDA resolution, typically
      framed as a value/criterion dispute. National-circuit LD has shifted significantly
      toward policy-style argumentation including plans, counterplans, and kritiks.
    typical_round_duration_minutes: 'Approximately 40–45 minutes including cross-examinations
      and preparation time. Total speaking time is 13 minutes per side. Each debater
      receives 4 minutes of preparation time. Source: NSD Debate Camp format guide
      — [WEB-5]; Debate Experts
      — [WEB-6].'
    speech_structure: '5 speeches and 2 cross-examinations: 1AC (6 min) → CX by Neg
      (3 min) → 1NC (7 min) → CX by Aff (3 min) → 1AR (4 min) → 2NR (6 min) → 2AR
      (3 min). Each debater receives 4 minutes of preparation time. Total speaking
      time is 13 minutes per side. Source: NSD Debate Camp — [WEB-5];
      Debate Experts — [WEB-6].'
    argument_types_central:
    - Value/criterion framework disputes
    - Contention-level offense
    - Plans and counterplans (national circuit)
    - Kritiks (national circuit)
    - Theory arguments
    - Philosophical/normative framework debates
    quality_norm_axis: 'Bimodal: lay/traditional LD rewards rhetoric and clarity;
      national-circuit LD rewards technical flow and speed'
  public_forum:
    description: Two-person teams debate a monthly NSDA resolution, typically a current-events
      policy or evaluative topic. Historically lay-oriented with emphasis on persuasion
      and accessible argument; national circuit has grown more technical.
    typical_round_duration_minutes: 'Approximately 40–50 minutes. Speeches are 2–4
      minutes each, interspersed with 3-minute crossfire sections. Source: Wikipedia
      Public Forum Debate — [WEB-7].'
    speech_structure: 'Standard PF order: Team A Constructive (4 min) → Team B Constructive
      (4 min) → Crossfire (3 min) → Team A Rebuttal (4 min) → Team B Rebuttal (4 min)
      → Crossfire (3 min) → Team A Summary (3 min) → Team B Summary (3 min) → Grand
      Crossfire (3 min) → Team A Final Focus (2 min) → Team B Final Focus (2 min);
      each team receives 2–3 minutes of preparation time. Source: Wikipedia Public
      Forum Debate — [WEB-7].'
    argument_types_central:
    - Contentions with empirical evidence
    - Rebuttal and refutation
    - Weighing (magnitude, probability, timeframe)
    - Summary/final focus collapse strategy
    quality_norm_axis: Local/lay circuits strongly weight clarity, rhetoric, and accessibility;
      national circuit increasingly rewards technical evidence battles and flow
  congressional:
    description: Simulated legislative session format where students give prepared
      speeches on legislation, respond to questions, and are ranked by a presiding
      officer and judges on persuasiveness, research quality, and oratory. Less head-to-head
      adversarial structure than other formats.
    argument_types_central:
    - Legislative advocacy (pro/con positions)
    - Refutation and response to prior speakers
    - Rhetorical effectiveness and oratory
    - Research quality and evidence citation
    quality_norm_axis: Strongly oratory/rhetoric-weighted; less circuit variation
      than Policy or LD
circuit_variation:
  description: The US high school debate community is not uniform. Quality standards
    vary substantially by geographic circuit and by whether a tournament is on the
    'national circuit' (TOC bid events, prestigious invitationals) versus local/regional
    circuits.
  national_circuit:
    description: TOC bid tournaments and major invitationals drawing national-caliber
      competitors. Judges are typically experienced coaches or former debaters who
      value technical argumentation, speed, flow, and dense evidence engagement.
    key_quality_norms:
    - Technical flowing accuracy
    - Speed (spreading) tolerance in Policy and LD
    - Evidence quality and warrants
    - Impact calculus precision
    - Argument layering and prioritization
    representative_tournaments: 'The TOC qualifies competitors via bids earned at
      over 100 designated qualifying tournaments across the US and internationally.
      Examples for 2025–2026 include the Grapevine Classic (TX) for Policy, Yale Invitational
      (CT) for LD and PF, and the Glenbrooks Tournament (IL) for multiple events.
      Popular bid tournaments across formats include Greenhill (TX), Harvard (MA),
      and UC Berkeley (CA). Qualification generally requires two gold bids (LD, Policy,
      PF Gold TOC) or one gold/two silver bids (PF Silver TOC). Source: TOC official
      site — [WEB-8]; TOC Bid Tournaments page — [WEB-9];
      Wikipedia TOC — [WEB-10];
      Policy Debate Central 2024–25 — [WEB-11].'
  local_and_regional_circuits:
    description: District, regional, and invitational tournaments served by lay judges
      (community volunteers, parents, non-debate coaches). Quality standards emphasize
      clarity, rhetoric, accessibility, and persuasive effectiveness over technical
      flow.
    key_quality_norms:
    - Clarity of delivery and organization
    - Persuasive rhetoric and storytelling
    - Accessibility of arguments (avoiding jargon)
    - Confidence and presentation style
    notable_examples: Texas lay PF circuit is a frequently cited example of a regional
      circuit with strongly lay-judge norms; similar dynamics exist in many Midwest
      and Southeast state circuits
  nsda_nationals:
    description: NSDA National Championship, the largest competitive debate tournament
      in the US, with state-qualifying requirements. Mix of lay and experienced judges;
      NSDA maintains official rules and guidelines.
    notes: 'NSDA Nationals 2024 drew approximately 6,700 middle and high school students
      from 1,500 schools, competing for 42 championship titles. Qualification proceeds
      through District Tournaments; a Last-Chance Qualifier also provides additional
      qualification pathways. The tournament covers Policy, LD, PF, Congressional,
      and multiple speech events. Source: Aralia Education guide — [WEB-12].'
argument_quality_dimensions:
  description: Per the elicitation, the system must produce separate sub-scores across
    these dimensions plus qualitative coaching feedback. 'Strong' is defined by external
    community standards (NSDA norms, TOC circuit paradigms, coaching staff rubrics).
  dimensions:
  - name: Evidence quality
    weight: Highest (per elicitation)
    components:
    - Source credibility and authority
    - Recency of evidence
    - Contextual integrity (card not miscut or out-of-context)
    - Warrant clarity (does the evidence actually support the claim)
    - Cherry-picking detection
  - name: Logical structure and warrant quality
    weight: High
    components:
    - Claim-warrant-impact structure
    - Inferential validity (deductive and inductive)
    - Argument completeness (no missing warrants)
    - Internal consistency
  - name: Relevance and responsiveness
    weight: High
    components:
    - On-topic relevance to the resolution
    - Direct responsiveness to opponent's arguments
    - Burden fulfillment
    - Clash quality in rebuttal
  - name: Persuasive effectiveness
    weight: Format/circuit-conditioned
    components:
    - Rhetorical clarity and organization
    - Impact framing and weighing
    - Narrative coherence
    - Accessibility to the judging audience
  output_types_required:
  - Separate sub-scores per dimension
  - Qualitative coaching feedback explaining weaknesses
  - Pairwise comparison scores for rebuttal practice
  - Format-conditioned and circuit-conditioned scoring norms
normative_standards:
  nsda:
    description: National Speech and Debate Association — sets official rules, event
      structures, and ethical guidelines for all four formats
    relevant_documents: '[NEEDS VERIFICATION — deferred: below search budget; NSDA
      official rulebooks are available at speechanddebate.org but format-specific
      document URLs were not retrieved in this pass]'
    evidence_ethics_policy: '[NEEDS VERIFICATION — deferred: below search budget;
      NSDA evidence ethics rules (standards for cutting, citing, and representing
      evidence) require direct access to current NSDA rulebook documents]'
  toc:
    description: Tournament of Champions (hosted by University of Kentucky) — the
      most prestigious US high school debate tournament; TOC bid qualification structures
      the national-circuit competitive calendar
    bid_structure: 'For the 2025–2026 season, most debate events (Policy, LD, Congressional)
      require at least two bids for full qualification. In PF, a Gold TOC requires
      two Gold bids and a Silver TOC requires two Silver bids or one Gold bid. Bids
      are awarded at over 100 qualifying tournaments selected by event-specific advisory
      committees. Bid levels are tiered (Octafinals, Quarterfinals, Semifinals, Finals,
      etc.) based on tournament size. All US entries must represent the degree-granting
      school at which students are enrolled. Source: TOC official bid page — [WEB-9];
      CDA Debate blog — [WEB-13];
      NSD Debate Camp glossary — [WEB-14].'
  judge_paradigms:
    description: Individual judges publish paradigms stating their preferences, which
      function as the operative quality-norm document for a given round. Paradigms
      vary on speed tolerance, argument type preferences, evidence standards, and
      voting issues.
    platforms: 'Tabroom.com is the primary platform for tournament management and
      paradigm hosting; it is also the official registration portal for NSDA events
      and TOC qualification reporting. Source: Aralia Education NSDA guide — [WEB-12];
      TOC bid page — [WEB-9].'
  coaching_rubrics:
    description: Coaching staff at individual programs may define internal rubrics
      that supplement NSDA and circuit norms. These are the proximate quality-standard
      setters for the platform's coaching feedback function.
infrastructure_and_access:
  platform_delivery: US-based SaaS debate coaching platform; end users access via
    web browser or app on school-issued or personal devices
  device_context: Mix of school-issued Chromebooks/laptops and personal smartphones/tablets;
    connectivity generally reliable in school settings
  input_pipeline: Text-based (written cases, typed flows, speech transcripts); no
    audio/video processing in current scope
  school_technology_access: '[NEEDS VERIFICATION — deferred: below search budget;
    reliable sub-national figures on broadband and device access specifically for
    debate programs not found in this pass]'
  data_privacy_considerations: Students are minors (under 18); FERPA and COPPA compliance
    required for any student data handling
  applicable_regulations: 'Federal baseline: FERPA (Family Educational Rights and
    Privacy Act) governs privacy of education records for all schools receiving federal
    funding; EdTech vendors access records as ''school officials'' under FERPA. COPPA
    (Children''s Online Privacy Protection Act) applies to services collecting personal
    data from children under 13. As of 2024–2025, more than 40 states have enacted
    additional student data privacy laws beyond federal requirements; California''s
    SOPIPA (prohibits sale of student data and targeted advertising), New York''s
    Education Law 2-d, and Illinois'' SOPPA are among the most impactful state-level
    laws. At least 13 states have passed SOPIPA-modeled legislation. COPPA 2.0 passed
    the US Senate in July 2024 and may expand coverage. Multi-state platforms must
    satisfy the strictest applicable state law. Source: McDermott Law — [WEB-15];
    StudentDPA — [WEB-16];
    Hireplicity — [WEB-17].'
content_considerations:
  topic_volatility: Debate resolutions address current-events policy and normative
    questions that may be politically or socially sensitive (e.g., immigration, criminal
    justice, healthcare, foreign policy, environmental regulation). The system must
    assess argument quality without taking sides on contested value questions.
  value_pluralism: LD and Congressional debates explicitly center on normatively contested
    premises where reasonable people disagree. The system must score argument structure
    and warrant quality independently of whether the system 'agrees' with the underlying
    value claim.
  empirical_contestation: PF and Policy debates frequently involve disputed empirical
    claims (e.g., economic impact estimates, scientific consensus questions, statistical
    projections). Evidence credibility assessment must be calibrated to distinguish
    genuine expert disagreement from misrepresented or cherry-picked evidence.
  age_appropriateness: All content involves high school students (minors). Feedback
    must be constructively framed for educational development contexts.
  current_resolution_topics: 'Active and recent NSDA resolutions (2025–2026 season
    unless noted):

    - Policy (CX) 2025–2026: Resolved: The United States federal government should
    significantly increase its exploration and/or development of the Arctic.

    - LD 2025–2026 topics include (by cycle): ''Democracies ought to prioritize the
    protection of civil liberties over national security'' (Nationals 2026); ''The
    United States military ought to abide by the principle of non-intervention'' (March/April);
    ''The possession of nuclear weapons is immoral'' (Jan/Feb); ''In the United States
    criminal justice system, plea bargaining is just'' (active cycle per DebateUS).

    - PF Nov/Dec 2025: Resolved: The United States federal government should require
    technology companies to provide lawful access to encrypted communications.

    - PF Nationals 2025: Resolved: On balance, in the United States, the benefits
    of presidential executive orders outweigh the harms.

    - Congressional: Topics set by student-submitted legislation voted on by National
    Tournament participants; submissions open Oct 1, 2025 with deadline Feb 5, 2026
    for 2026 nationals.

    Source: NSDA Topics page — [WEB-18]; Wikipedia
    Public Forum Debate — [WEB-7]; DebateUS
    current resources — [WEB-19]; Tabroom tournament listing — [WEB-20].'
population_specific_notes: '- The quality-defining community for this deployment is
  not the platform itself but the external NSDA/TOC/coaching ecosystem; benchmark
  annotator populations (e.g., FOL-trained CS students or NLP researchers) are categorically
  mismatched to this community.

  - Circuit-level adaptation is a strong desideratum per the elicitation: a single
  universal scoring standard will systematically mis-score arguments evaluated against
  lay vs. tech norms.

  - Evidence quality assessment (card quality, recency, contextualization) is the
  highest-weight sub-dimension and is the farthest from any existing logical reasoning
  benchmark''s coverage.

  - Debate-specific structural argument types (DAs, CPs, kritiks, T shells, theory
  arguments) constitute a first-class argument ontology with no representation in
  standard NLI or argument mining benchmarks.

  - Pairwise rebuttal comparison is a structural requirement not met by any standalone
  argument scoring benchmark; this is a near-unique deployment requirement.

  - Congressional debate has a meaningfully different quality ontology from the other
  three formats (oratory-focused, less adversarial, no flowing) and may require a
  partially separate evaluation approach.

  - Student development trajectory matters: coaching feedback should be calibrated
  to student skill level (novice vs. varsity), which may require the platform to track
  student baseline and adapt feedback accordingly.'
net_new_fields:
  relevant_datasets_and_benchmarks:
    description: Searches surfaced several datasets and benchmarks directly relevant
      to gap analysis. None cover the full deployment requirement, but some partially
      address specific gaps.
    entries:
    - name: DebateSum
      relevance: Large-scale Policy Debate evidence dataset compiled from NSDA community
        data over 7 years (2013–2019), containing 187,000+ pieces of evidence with
        extractive/abstractive summaries and rich metadata (citation, author, word
        counts). Directly covers Policy Debate evidence structure. However, it focuses
        on argument mining and summarization, not argument quality scoring or circuit-conditioned
        evaluation.
      gap_addressed: Partial coverage of evidence-handling terminology and Policy
        Debate card structure (evidence quality gap); does not address multi-dimensional
        scoring, format-conditioned norms, or pairwise comparison.
      source: Semantic Scholar — [WEB-21]
    - name: OpenDebateEvidence (NeurIPS 2024)
      relevance: Massive-scale dataset (3.5 million documents) from the American Competitive
        Debate community, covering both high school and college debates across the
        full season. Includes rich metadata (author, date, source, citation, debate
        round). Directly sourced from the deployment population. However, the benchmark
        task is argumentative summarization evaluated with ROUGE and LLM-as-judge
        scores, not argument quality scoring or circuit-conditioned evaluation.
      gap_addressed: Strong corpus-level coverage of actual US competitive debate
        evidence (addresses IC gap for evidence content); does not address output
        ontology mismatch, pairwise comparison, or format/circuit-conditioned scoring.
      source: arXiv 2406.14657 — [WEB-22]; NeurIPS 2024
        — [WEB-23]
    - name: IBM Project Debater datasets (argument quality, key point analysis)
      relevance: IBM's Project Debater published multiple datasets covering argument
        detection, argument quality ranking (IBM-ArgQ-5.3kArgs, IBM-Rank-30k, IBM-ArgQ-9.1kPairs),
        and key point analysis on controversial topics. Argument quality is assessed
        on general controversial topics (not competitive debate formats) using crowdsourced
        annotations. Pairwise argument quality classification tasks exist. However,
        content is general debate topics, not NSDA format-specific; annotators are
        crowdworkers, not debate judges; no circuit-conditioned or format-conditioned
        norms.
      gap_addressed: Partial coverage of pairwise argument ranking task structure;
        partial coverage of argument quality multi-dimensional scoring. Does not address
        debate-specific argument ontology, evidence card quality, or NSDA/TOC circuit
        norms.
      source: IBM Research blog — [WEB-24];
        neurohive.io overview — [WEB-25]
    - name: ArgQuality / CompAQA (pairwise argument ranking)
      relevance: Research benchmarks for pairwise argument quality ranking (IBM-ArgQ
        family, Habernal & Gurevych 2016). Tasks include pointwise and pairwise argument
        quality classification on controversial topics. A 2024 MDPI paper (CompAQA)
        proposes a comparison-based framework integrating both pairwise classification
        and ranking. LLMs (GPT-3.5-turbo) have been shown to struggle to match supervised
        models on pairwise ranking tasks. Annotation inter-rater agreement for quality
        is low (kappa ~0.10–0.12), confirming inherent subjectivity.
      gap_addressed: Directly addresses the pairwise comparison gap at the task-structure
        level; however, content is general controversial topics, not competitive debate
        formats, and annotators are not debate community members.
      source: MDPI Electronics 2024 — [WEB-26];
        arXiv 2406.13905 — [WEB-27]
    - name: DebateBench (2025)
      relevance: A benchmark of British Parliamentary (BP) debate transcripts with
        speech-level scores and house rankings from official adjudication data (256
        speeches across 32 debates). Tests LLMs on speech scoring, argument ranking,
        and long-context reasoning. Closest existing benchmark to the deployment's
        scoring task. However, it covers BP format only (not NSDA Policy/LD/PF/Congressional),
        adjudication norms differ substantially, and it does not capture lay vs. tech
        circuit variation.
      gap_addressed: Provides existence proof that LLM-based debate speech scoring
        benchmarks are feasible; partially relevant to output form (multi-score +
        rationale) and output content (community-anchored judge scores). Format mismatch
        to NSDA is significant.
      source: arXiv 2502.06279 — [WEB-28]
    - name: ArgBench (2025)
      relevance: A recent benchmark (arXiv 2604.17366) covering multiple computational
        argumentation tasks including argument mining, quality assessment, argument
        similarity, and ad-hominem detection. Evaluates transfer learning across tasks.
        Relevant as a multi-task argumentation benchmark but does not cover competitive
        debate formats, circuit-conditioned norms, or evidence card quality.
      gap_addressed: Partially addresses IO gap (argument task taxonomy broader than
        FOLIO); does not address deployment-specific requirements.
      source: arXiv 2604.17366 — [WEB-29]
    overall_assessment: 'No existing benchmark covers the full deployment requirement.
      The closest partial matches are: OpenDebateEvidence for evidence corpus coverage;
      IBM ArgQ datasets for pairwise argument quality task structure; DebateBench
      for speech-level adjudication scoring. The combination of NSDA-format-specific
      content, circuit-conditioned quality norms, multi-dimensional sub-scores, and
      pairwise rebuttal comparison is unmet by any single existing resource.'
  generative_ai_policy_in_debate:
    description: 'The NSDA competitive debate community has explicitly addressed generative
      AI use. Multiple state-level organizations (e.g., Ohio Speech and Debate Association)
      prohibit using or paraphrasing AI-generated text as student original work in
      competition, and prohibit AI-generated text as evidence in rounds. This is deployment-relevant:
      the platform must be positioned as a coaching tool that does not generate content
      students present as their own, and any evidence quality assessment must be able
      to distinguish AI-generated from human-authored evidence.'
    source: Ohio Speech and Debate Association policy — [WEB-30]
```

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

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: FOLIO focuses on formal deductive reasoning — given a set of premises, is a conclusion true, false, or uncertain. Your deployment involves much richer argument types: empirical claims backed by evidence, value-laden claims, rhetorical moves like analogy or burden-shifting, and debate-specific structures like disadvantages, counterplans, or kritiks. Which of these categories does your system need to assess, and are any of them more central than pure deductive validity?
A1: All four categories are required — empirical claims with evidence, value-laden claims, rhetorical moves, and debate-specific structural moves (DAs, CPs, kritiks). Pure deductive validity is the least central; most arguments are inductive or evidentiary. The heaviest weight falls on evidence quality and claim warrants, followed by relevance and responsiveness to the opponent's case.

Q2 [OO]: FOLIO scores outputs as a three-way label (true / false / uncertain), which captures logical entailment but not argument quality. Your deployment requires holistic strength assessment — covering logical validity, evidence quality, relevance, and persuasive effectiveness. Should the system produce a single composite score, separate scores per dimension, qualitative feedback, or a ranking across competing arguments? And who defines what 'strong' means — coaches, judges, debate norms, or the platform itself?
A2: The system should produce separate sub-scores across logic, evidence, relevance, and persuasiveness, plus qualitative coaching feedback explaining weaknesses. A composite score alone is not actionable for student development. Pairwise comparison for rebuttal practice is also needed. "Strong" is defined by external community standards — NSDA norms, TOC circuit paradigms, and coaching staff rubrics — not a purely platform-internal standard.

Q3 [OC]: In competitive high school debate, what counts as a strong argument is shaped by community norms that vary across circuits — for example, policy debate judges in the national circuit may reward speed and technical flow, while LD or PF judges in local circuits may weight rhetoric and clarity more heavily. Should the system's quality judgments reflect a single universal standard, or adapt to the judging community and format (policy, LD, PF, congressional) your students compete in?
A3: Adaptation by format is a minimum requirement; circuit-level adaptation is a strong desideratum. Winning criteria differ substantially — a lay PF round in Texas rewards clarity and rhetoric, while a tech-heavy LD round at a TOC bid event rewards speed and technical flow. The system must accommodate PF, LD, and Policy across both local and national circuit contexts.

Q4 [IC]: Debate arguments frequently involve contested empirical claims where evidence quality is disputed and value claims where reasonable people disagree. Does your system need to evaluate the credibility and recency of cited evidence, or only assess the logical structure of the argument as stated — and how should it handle premises that are empirically false but internally consistent?
A4: Evidence credibility and recency must be evaluated, since card quality is central to competitive debate; cherry-picked, outdated, or miscontextualized evidence should be flagged. For empirically false but internally consistent arguments, the system should note the factual problem while scoring logical structure separately, giving students feedback on both dimensions independently.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | FOLIO's ontology covers only formal FOL deductive entailment, while the deployment requires inductive/evidentiary reasoning, value-laden claims, rhetorical moves, and debate-specific structures (DAs, CPs, kritiks) — nearly none of which appear in FOLIO's category set. |
| IC | HIGH | FOLIO uses logically constructed premise sets with no normatively charged, culturally embedded, or evidentially disputed content; the deployment centers on contested empirical claims, miscontextualized evidence, and value judgments that carry heavy construct-irrelevant variance risk when assessed by a benchmark with clean logical scenarios. |
| IF | LOWER | Both benchmark and deployment are text-only in standard American English; no modality or script mismatch exists. |
| OO | HIGH | FOLIO's three-way entailment label (true/false/uncertain) is categorically mismatched to the deployment's required output space — multi-dimensional sub-scores, qualitative coaching feedback, pairwise strength rankings, and format/circuit-conditioned quality norms cannot be approximated by an entailment label. |
| OC | HIGH | FOLIO's ground-truth labels are determined by formal FOL inference engines and expert logicians, whereas the deployment's correctness standard is set by a pluralistic, format-varying, circuit-varying human judging community; annotator-population mismatch is near-total. |
| OF | HIGH | FOLIO produces a single categorical label; the deployment requires multi-dimensional scores, free-text coaching rationales, and pairwise comparative outputs — a fundamental output-form mismatch that makes benchmark performance metrics largely uninformative for deployment validity. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

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
  "benchmark": "folio",
  "region": "US High School Competitive Debate — Argument Quality Assessment",
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
