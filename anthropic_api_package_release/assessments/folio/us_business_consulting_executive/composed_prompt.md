I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **FOLIO: Natural Language Reasoning with First-Order Logic** is valid for use in **US Management Consulting — Business Case Reasoning**.

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

### 1. Input Ontology
FOLIO defines two primary tasks: natural language logical reasoning (truth-value
classification given premises) and NL-FOL translation [Q63]. The reasoning task
covers only formal deductive reasoning within closed, fully specified logical worlds
[Q15], including syllogistic forms, conjunctions, disjunctions, and implications [Q43],
with logical depth measured by reasoning steps [Q60] and structural diversity measured
by distinct abstract syntax trees [Q61]. A standard FOL operator set — negation,
conjunction, disjunction, implication, universal and existential quantifiers, and
equality — defines the logical coverage [Q138], while temporal and modal logics are
explicitly excluded as out of scope [Q139, Q140].

The task taxonomy is thus narrowly deductive and closed-world. No inductive,
abductive, analogical, or rhetorical reasoning modes appear anywhere in the benchmark.
The benchmark itself acknowledges that existing NL tasks fail to measure complex
logical reasoning independently [Q8, Q9, Q10], and the finding that "sufficient domain
knowledge of FOL is necessary for good performance on FOLIO" [Q112] underscores that
the benchmark targets a specialist formal-logic competency. Prior benchmarks are
criticized for shallow reasoning depth [Q11] and small logical vocabularies [Q12, Q13],
but the contrast FOLIO draws is entirely within the formal-deductive space — the
non-deductive reasoning modes that dominate real-world business argumentation are
simply absent from the design.

### 2. Input Content
FOLIO's 1,430 examples are derived from two sources [Q1, Q32]: WikiLogic stories
written from scratch using Wikipedia pages as idea seeds [Q34], and HybLogic stories
assembled by filling syllogistic templates with real-world noun phrases [Q42]. The
WikiLogic method explicitly instructs annotators to create stories without templates,
based on real-world knowledge that "should be plausible in general" [Q35], while
deliberately avoiding domain-specific knowledge. The dual-method design produces
topical breadth (4,351-word vocabulary, 74% from WikiLogic) [Q62] and logical
structural diversity [Q33, Q38], but all instances are artificial narratives constructed
to isolate formal logical structure.

None of the examples are grounded in real business content — no financial metrics,
sector benchmarks, regulatory context, or competitive dynamics appear. The paper
itself acknowledges that none of the prior benchmarks (and by design FOLIO itself)
"are written by humans with information drawn from real-world knowledge, making them
less applicable to real-world reasoning scenarios" [Q14]. WikiLogic seeds may
introduce pre-training contamination risk [Q104], while HybLogic's template origins
make some patterns learnable through fine-tuning [Q105] — both of which are
content-level concerns independent of the domain mismatch.

### 3. Input Form
FOLIO is text-only and entirely in English. Premises and conclusions are written in
natural language prose accompanied by parallel FOL annotations [Q64, Q65]. The
dataset uses standardized English conventions for logical quantifiers and connectives
(e.g., "either-or" for exclusive disjunction [Q130], "A or B, or both" for inclusive
disjunction [Q131], naturalistic quantifier phrasing [Q132, Q133]), with grammar
checked by Grammarly and reviewed by English Literature specialists for naturalness
[Q49, Q50]. Readability is reported using the Dale-Chall formula [Q154]. The input
signal is clean, well-formed English prose with no multi-modal components. The dataset
is split 70%/15%/15% into train/validation/test sets [Q78, Q79].

NOT DOCUMENTED: spoken or multi-modal input variants; non-Latin scripts; dialectal
or register variation. Both the benchmark and the consulting deployment are text-only
in English, so no modality or script mismatch exists for that deployment context.

### 4. Output Ontology
FOLIO's output ontology for the main reasoning task is a three-way classification
label: True, False, or Unknown [Q36, Q66]. These labels represent the logical validity
of a conclusion within a closed-world frame defined entirely by the premises; the
FOL prover's output is the definitive ground truth [Q2]. The majority baseline is
38.5% (87 True, 78 False, 61 Unknown examples in the test set) [Q94]. For the
NL-FOL translation subtask, outputs are FOL formula strings evaluated for syntactic
validity [Q73, Q74] and inference-engine execution accuracy [Q75, Q76]. The FOL
representation is privileged because it is unambiguous, enables explicit derivation,
and can be mechanically checked [Q135, Q136, Q137].

No output category exists for persuasiveness, narrative coherence, executive-audience
framing, objection anticipation, evidence selection quality, or argument structure —
the criteria that define success in the consulting deployment. The paper acknowledges
that more reliable NL-FOL translation metrics are needed [Q77], and that 5% of
conclusions have syntactic complexity that challenges GPT-4 [Q120], but the label
taxonomy itself is not questioned. The entire output ontology is built around
formal-logical validity, not communicative or rhetorical effectiveness.

### 5. Output Content
FOLIO's ground-truth labels are generated through a multi-stage annotation and
verification pipeline: human annotators write NL and FOL in parallel [Q17], FOL
annotations are reviewed by FOL experts [Q29, Q125], and all labels are
automatically verified by an FOL inference engine for syntactic validity and label
consistency [Q57]. The annotation protocol enforces cross-example consistency in
FOL translation [Q54, Q143, Q144, Q145, Q146, Q147], and 39.2% of stories required
rewriting to address quality issues (bias, factual error, unnaturalistic language) [Q48].

Human performance benchmarking reveals a 34.16% accuracy gap between FOL-expert
annotators (95.98%) and non-experts — community college and high school students
[Q111], underscoring that the labels measure a specialist formal-logic skill. All
annotators are native or near-native English speakers [Q27, Q110], and expert
annotators are CS students familiar with FOL [Q108]. No annotators representing
business professionals, consulting practitioners, or management domain experts are
documented. The formal objectivity of the labels — verified by an FOL prover — is
internally rigorous but structurally irrelevant to the ground truth the consulting
deployment requires, which is an engagement partner's professional judgment.

### 6. Output Form
For the main reasoning task, FOLIO expects a discrete three-way label (True/False/Unknown)
selected from a fixed classification set, evaluated by accuracy [Q80]. Model outputs
are tested under both fine-tuning (BERT, RoBERTa with classification layers [Q84, Q85])
and few-shot prompting settings [Q87, Q88]. For the NL-FOL translation task, outputs
are FOL formula strings evaluated by syntactic validity and execution accuracy [Q73,
Q74, Q75, Q76] through a three-step pipeline: human FOL → Python parser → theorem
prover [Q148, Q149, Q150, Q151, Q153]. Performance is reported as classification
accuracy averaged over five random training samples [Q80, Q93], with confusion
matrices showing label-level accuracy breakdowns [Q155, Q156, Q157], and robustness
checks on premise ordering [Q158, Q159, Q160].

NOT DOCUMENTED: evaluation of open-ended, long-form natural language outputs;
metrics for argument quality, persuasiveness, or narrative structure. The NL-FOL
translation task involves text generation, but output quality is assessed by FOL
correctness, not by language quality or rhetorical effectiveness [Q96, Q97]. The
output form (discrete label or FOL string) is categorically different from the
long-form structured business narrative that the consulting deployment requires.


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

## Regional Context

```yaml
name: US Management Consulting — Business Case Reasoning
abbreviation: us_mgmt_consulting_folio
assessment_context:
  benchmark: folio
  deployment_description: 'A US consulting firm evaluating whether an LLM can assist
    American management consultants in constructing persuasive business cases: assembling
    evidence, structuring arguments, anticipating counterarguments, and tailoring
    reasoning to C-suite and board audiences.'
  primary_concern: FOLIO's closed-world deductive ontology, domain-knowledge-free
    content, discrete classification output, and FOL-validity ground truth are all
    categorically misaligned with the inductive, abductive, rhetorical, and domain-grounded
    reasoning that defines success in this deployment.
countries:
  primary:
  - United States
  sub_national_variation: None identified. No regional or sub-national variation noted
    in the elicitation; the deployment is firm-wide across US office locations.
languages:
  primary: English (American)
  variants:
  - Standard American business English
  - Executive/boardroom register
  - Financial and sector-specific terminology
  note: 'All interactions are in English. Register variation is significant: consultants
    must produce output calibrated to CFO and board-level audiences, distinct from
    analyst-tier or general prose. No script or language mismatch with FOLIO''s English-only
    benchmark.'
writing_systems:
  scripts:
  - Latin alphabet (standard ASCII and Unicode)
  note: No script mismatch. Both benchmark and deployment are text-only English. Financial
    notation, tables, and structured frameworks (e.g., 2x2 matrices, waterfall charts
    described in prose) may appear in deployment outputs but not in benchmark inputs.
target_population:
  description: United States–based management consultants and engagement partners
    at a consulting firm. Users are highly educated professionals with graduate-level
    business or domain training, experienced in structuring persuasive arguments for
    senior executive audiences. Business audiences (CFOs, boards, C-suite) are the
    downstream recipients of LLM-assisted outputs, not direct LLM users.
  roles:
  - Management consultant (analyst through manager level)
  - Engagement partner (senior reviewer and quality gatekeeper)
  - 'Indirect audience: CFO, board members, C-suite executives across corporate sectors'
  education_level: Graduate-level (MBA, JD, domain-specialist Master's or PhD typical);
    high quantitative and analytical literacy
  professional_norms: Outputs are subject to partner review before client delivery.
    Partner judgment — not formal logical validity — is the operative ground truth
    for output quality. Consulting culture prizes precision, confidence, concision,
    and audience calibration over exhaustive hedging.
  sector_coverage: Cross-sector corporate clients; financial services, industrials,
    healthcare, technology, consumer goods, and other verticals may all appear in
    engagement scenarios
  no_demographic_variation_noted: true
  industry_llm_adoption_context: 'Business consulting leads enterprise LLM adoption
    at approximately 11.10% of firms analyzed, ahead of law (8.98%) and accounting
    (5.90%), reflecting consulting''s natural fit with LLM-assisted research synthesis
    and client deliverable drafting. Source: Bloomberry enterprise AI adoption analysis
    (76k companies, Oct 2025) — [WEB-1]'
reasoning_types_required:
  dominant:
  - Inductive reasoning (market sizing from partial data, trend extrapolation)
  - Abductive reasoning (best-explanation inference from business signals)
  - Analogical reasoning (comparable deal or engagement pattern-matching)
  - Rhetorical reasoning (audience-calibrated argument framing, objection anticipation)
  present_but_secondary:
  - Deductive reasoning (logical structure of argument chain)
  - Probabilistic/uncertainty reasoning (confidence intervals, scenario analysis)
  absent_from_benchmark: FOLIO covers only formal deductive reasoning in closed logical
    worlds. All dominant reasoning types in this deployment are entirely absent from
    the benchmark.
  note: The elicitation explicitly confirms that strict deductive reasoning is a small
    minority of the consulting reasoning task.
  net_new_reasoning_benchmark_evidence: 'A 2025 multi-reasoning benchmark (arXiv:2505.11854)
    evaluating deductive, inductive, abductive, and analogical reasoning across 6,235
    instances found that current frontier LLMs perform meaningfully differently across
    types: o4-mini achieves 87.67% on abductive tasks but deductive reasoning scores
    range only 72–78%, suggesting models are relatively stronger on the abductive
    reasoning this deployment demands than on formal deduction. Source: arXiv 2505.11854
    — [WEB-2]


    A separate inductive/abductive benchmark (arXiv:2509.03345) using fictional ontology-grounded
    worlds reports performance degrades sharply as ontology complexity increases,
    consistent with consulting''s multi-layered inference chains. Source: arXiv 2509.03345
    — [WEB-3]'
domain_knowledge_requirements:
  description: The deployment is deeply dependent on real-world business domain knowledge.
    Financial metrics, sector benchmarks, regulatory context, and competitive dynamics
    are the raw material of consulting arguments.
  knowledge_domains:
  - 'Financial metrics and valuation frameworks (EBITDA, NPV, ROIC, etc.) — Commonly
    referenced frameworks in LLM financial evaluation include FinQA (multi-step numerical
    reasoning over S&P 500 earnings reports), FinanceQA (professional financial analysis
    tasks), and CFA-exam-grounded benchmarks covering valuation, risk, and portfolio
    reasoning. Source: AwesomeAgents Finance LLM Leaderboard (Apr 2026) — [WEB-4];
    arXiv FinanceQA 2501.18062 — [WEB-5]; arXiv CFA benchmark
    2509.04468 — [WEB-6]'
  - 'Sector-specific benchmarks and KPIs — [NEEDS VERIFICATION — deferred: sector
    breakdown for specific target firm is not publicly available; low impact given
    the assessment already establishes full content mismatch between FOLIO and all
    sector domains]'
  - 'Regulatory and compliance context — [NEEDS VERIFICATION — deferred: sector-dependent;
    below remaining search budget]'
  - M&A and competitive dynamics
  - Macroeconomic indicators and scenario framing
  benchmark_gap: FOLIO explicitly excludes domain-specific knowledge by design. No
    financial, regulatory, or competitive content appears in any FOLIO example. This
    is a full content mismatch.
  available_domain_benchmarks: 'Several financial domain reasoning benchmarks exist
    that better approximate consulting domain content than FOLIO: FinQA (8,281 QA
    pairs over S&P 500 earnings reports, multi-step numerical reasoning, Exact Match
    scoring); FIRE benchmark (3,000 financial scenario questions including open-ended
    rubric-scored items covering market analysis, risk assessment, and investment
    strategy); BizFinBench (business-driven tasks including anomalous event attribution,
    financial time reasoning, and adversarial robustness); and FinBen (42 datasets,
    24 financial tasks including forecasting, risk management, and decision-making).
    None are designed for consulting-specific argument construction or executive-audience
    calibration, but they represent a meaningful domain-knowledge step up from FOLIO.
    Sources: arXiv FIRE 2602.22273 — [WEB-7]; arXiv BizFinBench
    2505.19457 — [WEB-8]; FinBen NeurIPS 2024 — [WEB-9]'
output_quality_criteria:
  description: A successful output is one an engagement partner would present to a
    client without revision. Quality is multi-dimensional and audience-sensitive.
  criteria:
  - Persuasiveness and rhetorical effectiveness
  - Narrative coherence and structured argumentation
  - Objection anticipation and preemptive rebuttal
  - Executive-audience calibration (CFO/board register and framing)
  - Evidence selection quality and appropriate confidence levels
  - Logical validity (necessary but insufficient alone)
  ground_truth_standard: Engagement partner professional judgment — not formal logical
    validity or automated scoring.
  benchmark_gap: FOLIO's output ontology is a three-way logical-validity label (True/False/Unknown).
    None of the deployment's success criteria map to this label. The benchmark's ground
    truth is an FOL inference engine; the deployment's ground truth is a senior professional's
    expert judgment.
  argument_quality_evaluation_evidence: 'ArgBench (arXiv:2604.17366, Apr 2026) is
    the first standardized benchmark covering 33 computational argumentation datasets
    across 46 tasks including argument mining, quality assessment (rhetoric, cogency,
    effectiveness), perspective assessment, argument reasoning, and generation. LLMs
    show a systematic tendency toward middle-quality ratings on rhetorical dimensions,
    with models selecting ''medium'' labels in 57–83% of argument quality rating cases
    — a central-tendency bias that would suppress discrimination between strong and
    weak consulting arguments. Source: arXiv 2604.17366 — [WEB-10]


    Research on argument quality assessment frameworks (arXiv:2403.16084) confirms
    that LLM-based argument quality scoring using cogency, effectiveness, and robustness
    dimensions is feasible but requires systematic instruction with argumentation
    theory, not just fine-tuning. Source: arXiv 2403.16084 — [WEB-11]


    For LLM-as-judge evaluation of open-ended outputs more generally, domain-specific
    expert tasks show LLM–human agreement rates dropping to 64–68%, well below inter-expert
    baselines of ~72–75%, with disagreements concentrated on factual accuracy, actionability,
    and appropriate tone — precisely the dimensions consulting partner review prioritizes.
    Source: EmergentMind LLM-Judge Analysis — [WEB-12]'
output_form_requirements:
  deployment_form: Open-ended, long-form structured argumentative text (business case
    narratives, executive summaries, structured frameworks, recommendation memos)
    — suitable for partner review and client delivery.
  benchmark_form: Discrete three-way classification label or FOL formula string.
  mismatch_severity: Fundamental. The benchmark produces no natural language output
    that could be evaluated for argument quality. No evaluation infrastructure for
    long-form generation exists within FOLIO.
  rubric_based_evaluation_evidence: 'Rubric-based judging frameworks (RubricRAG, arXiv:2603.20882;
    RRD, arXiv:2602.05125) are an active research direction for evaluating open-ended
    long-form outputs; retrieval-augmented rubric generation improves alignment with
    human-rubric-based judgments and discriminative power between good and bad responses.
    These frameworks represent a plausible evaluation infrastructure for consulting
    memo quality, but none are deployed or validated for consulting-specific output
    assessment as of May 2026. Sources: arXiv 2603.20882 — [WEB-13];
    arXiv 2602.05125 — [WEB-14]'
infrastructure_and_access:
  deployment_channel: 'Internal consulting firm tooling; likely enterprise LLM API
    integration. The dominant enterprise deployment pattern as of 2025 is commercial
    API + RAG (retrieval-augmented generation) rather than self-hosted models, enabling
    faster production deployment with lower operational burden. Source: Portkey Enterprise
    LLM guide — [WEB-15]'
  modality: Text-only input and output
  language_tooling: High-quality NLP tooling for American English is well-established;
    no tooling gap.
  connectivity: Enterprise US office environment; high-bandwidth connectivity assumed;
    no connectivity constraints relevant to assessment.
  device_context: Desktop/laptop professional workstation; no mobile or low-bandwidth
    considerations.
  shadow_ai_risk: 'A notable deployment-context risk: analysis of 22.4 million enterprise
    prompts (2025) found that while only ~40% of companies have purchased official
    AI subscriptions, employees at 90%+ of organizations actively use AI tools — often
    via personal accounts IT cannot govern. This shadow-AI pattern is relevant to
    consulting deployments because it means LLM-assisted output may reach clients
    through unapproved channels with no audit trail and potential client-data exposure
    to public model training pipelines. Source: Harmonic Security AI Usage Index 2025
    — [WEB-16]'
regulatory_and_compliance_context:
  applicable_data_protection_law: 'No single federal US AI/privacy law; compliance
    is governed by a patchwork of state laws. As of 2025, 20 states have enacted comprehensive
    privacy regulations. The most material for a national consulting firm: California
    CCPA/CPRA (with CPPA ADMT rules adopted July 24, 2025, covering automated decision-making
    technology, risk assessments, and cybersecurity audits — effective Q4 2025/Q1
    2026 pending OAL review); Virginia, Colorado, Connecticut, and 16+ additional
    state frameworks with varying consent, opt-out, and data minimization standards.
    No comprehensive federal privacy law was enacted as of May 2026; a 10-year federal
    moratorium on state AI/ADM enforcement was proposed in the House but removed by
    the Senate in 2025 budget amendments. Sources: IAPP US State Privacy Laws Overview
    2025 — [WEB-17];
    Kolmogorov Law CPPA ADMT analysis — [WEB-18];
    Wilson Sonsini CPPA July 2025 — [WEB-19]'
  professional_liability_considerations: Consulting outputs carry client-advisory
    liability; factual accuracy and appropriate confidence calibration are legally
    and professionally significant — not merely stylistic preferences.
  sector_specific_regulation: 'Regulated practice areas trigger additional AI constraints:
    financial services (SEC Model Risk Management principles, FINRA rules on AI-assisted
    advisory outputs); healthcare (HIPAA restrictions on client PHI in LLM prompts);
    and legal/regulatory advisory work (evolving state bar guidance on AI use in advice-giving).
    US sectoral regulators — OCC, SEC, FINRA, HHS — apply existing frameworks to AI
    under their mandates rather than AI-specific statutes as of May 2026. Source:
    Liminal AI Governance Guide — [WEB-20]'
  ai_governance_policies: 'Enterprise AI governance maturity is low: a 2024 Deloitte
    report found only 9% of organizations had a mature AI governance framework, and
    a 2025 McKinsey report found only 28% of organizations had a board-level AI governance
    strategy. A 2025 Financial Times-cited survey found 23% of firms had no formal
    AI policy at all. For consulting firms specifically, the primary governance mechanism
    is partner-review of client deliverables, not formal AI-output policy. Sources:
    Knostic AI Governance Best Practices — [WEB-21];
    McKinsey/CX Today LLM Governance — [WEB-22]'
cultural_and_professional_norms:
  communication_register: Formal American business English; precise, confident, concise.
    Executive audiences expect structured logic, quantified claims, and clear recommendations
    — not hedged academic prose.
  audience_calibration_norms: CFO and board audiences prioritize financial impact,
    risk, and strategic optionality. Argument framing must lead with business value
    and anticipate fiduciary objections.
  partner_review_culture: Engagement partners function as quality gatekeepers; their
    professional judgment is the operative success criterion. A technically valid
    but poorly framed argument will fail this review.
  sector_norms_variation: '[NEEDS VERIFICATION — deferred: likely unsearchable (lived
    professional practice); sector-specific argument conventions are transmitted through
    apprenticeship and firm culture, not documented online at a level of specificity
    useful for benchmark assessment]'
benchmark_validity_summary:
  overall_alignment: Very low. FOLIO evaluates a narrow sub-component (formal deductive
    reasoning) of a much broader capability requirement, uses artificial domain-knowledge-free
    content, produces discrete labels rather than long-form text, and defines ground
    truth via FOL proof rather than professional judgment.
  dimension_priority_weights:
    IO: 'HIGH — FOLIO''s deductive-only ontology excludes the inductive, abductive,
      and rhetorical reasoning that dominate the consulting task. Net-new evidence:
      frontier LLMs score 73–87% on abductive reasoning (better than deductive) and
      degrade on complex multi-step induction, which is more directly relevant to
      market-sizing and trend extrapolation tasks in consulting. Source: arXiv 2505.11854
      — [WEB-2]'
    IC: HIGH — FOLIO's domain-knowledge-free artificial premises are categorically
      mismatched with the deployment's dependence on real-world financial, regulatory,
      and competitive content. Multiple financial reasoning benchmarks (FinQA, FIRE,
      BizFinBench, FinBen) now exist that better approximate the domain content required,
      but none target consulting argument construction specifically.
    IF: LOWER — Both benchmark and deployment are text-only in English; no modality
      or script mismatch.
    OO: HIGH — FOLIO's three-way logical-validity label does not map to any consulting
      success criterion; persuasiveness, coherence, and audience calibration are entirely
      absent. ArgBench (2025) provides the closest available output ontology for argument
      quality, but covers general argumentation, not executive-audience business cases.
    OC: MODERATE — FOLIO's FOL-prover ground truth is internally rigorous but structurally
      irrelevant to partner-review-based ground truth; convergent validity gap is
      large. Research on LLM-as-judge for domain-expert tasks shows agreement rates
      drop to 64–68% vs. inter-expert baselines of 72–75%, concentrated on exactly
      the dimensions (factual accuracy, actionability, tone) that partner review targets.
    OF: HIGH — Discrete classification label vs. long-form structured argumentative
      narrative is a fundamental output-form mismatch. Rubric-based judging frameworks
      (RubricRAG, RRD) are maturing but not yet validated for consulting-specific
      output evaluation.
  usable_signal: FOLIO provides a documented baseline for the deductive reasoning
    sub-component only. GPT-4's near-chance performance on HybLogic examples and the
    31.82% expert–GPT-4 gap establish a minimum deductive floor, but this signal is
    peripheral to the deployment's core requirements.
  flagged_gaps_for_web_search:
  - gap_id: 1
    label: Reasoning-type coverage gap
    description: No existing FOLIO coverage of inductive, abductive, or analogical
      reasoning in business contexts.
    search_target: business reasoning benchmark inductive abductive analogical LLM
      evaluation MBA case consulting scenario
    resolution_status: 'PARTIALLY RESOLVED — General inductive/abductive benchmarks
      exist (arXiv:2509.03345, arXiv:2505.11854) but none are business-context or
      consulting-specific. The closest business process reasoning benchmark (arXiv:2406.05506)
      covers causal process reasoning, not market-sizing or argument construction.
      No MBA case reasoning or consulting-scenario testbed found. Sources: [WEB-3];
      [WEB-2]; [WEB-23]'
  - gap_id: 2
    label: Persuasion and audience-calibration gap
    description: No benchmark dimension for rhetorical effectiveness, executive framing,
      or objection anticipation.
    search_target: argument quality evaluation benchmark LLM persuasion executive
      communication rhetorical effectiveness rubric scoring
    resolution_status: 'PARTIALLY RESOLVED — ArgBench (arXiv:2604.17366) provides
      the most comprehensive available benchmark for argument quality including rhetoric,
      cogency, and effectiveness dimensions across 46 tasks. Winning Arguments (WA)
      dataset and Counterfire corpus also exist for persuasiveness evaluation. However,
      none target executive-audience calibration, business case framing, or consulting-register
      output. LLMs show central-tendency bias in rhetorical quality rating tasks (57–83%
      middle-label selection), a significant validity concern for deploying LLM-as-judge
      for consulting output. Sources: [WEB-10]; [WEB-24];
      [WEB-25]'
  - gap_id: 3
    label: Business domain knowledge gap
    description: FOLIO excludes all real-world domain knowledge; deployment is fully
      dependent on it.
    search_target: financial domain reasoning benchmark LLM FinQA BusinessBench consulting
      domain knowledge evaluation sector benchmarks
    resolution_status: 'RESOLVED — Multiple financial domain reasoning benchmarks
      confirmed: FinQA (numerical reasoning over S&P 500 earnings reports, Exact Match
      scoring), FIRE (3,000 financial scenario questions, open-ended rubric evaluation),
      BizFinBench (business-driven adversarial financial tasks), FinBen (42 datasets,
      24 tasks), FinanceQA (professional financial analysis), and CFA-exam-grounded
      benchmarks. None are consulting argument construction benchmarks, but they document
      the domain-knowledge layer FOLIO entirely lacks. Sources: [WEB-7];
      [WEB-8]; [WEB-5];
      [WEB-4]'
  - gap_id: 4
    label: Open-ended generation evaluation gap
    description: FOLIO has no infrastructure for evaluating long-form argumentative
      text quality.
    search_target: long-form argument generation evaluation LLM structured business
      narrative scoring rubric-based assessment consulting memo
    resolution_status: 'PARTIALLY RESOLVED — Rubric-based judging frameworks for long-form
      output (RubricRAG arXiv:2603.20882; RRD arXiv:2602.05125) are active research
      directions and show improved alignment with human judgment over holistic scoring.
      No consulting-memo-specific evaluation rubric or benchmark found. The closest
      analog is CaseGen (arXiv:2502.17943) for legal case document generation, which
      uses expert-validated task-oriented rubrics — this methodology could potentially
      transfer to consulting memo evaluation. Sources: [WEB-13];
      [WEB-14]; [WEB-26]'
  - gap_id: 5
    label: Partner-review alignment gap
    description: FOLIO ground truth is FOL-prover output; deployment ground truth
      is expert professional judgment.
    search_target: professional expert annotation benchmark consulting business reasoning
      LLM evaluation partner review judgment human expert ground truth
    resolution_status: 'NOT FOUND — No consulting-practitioner-annotated benchmark
      or partner-review-validated evaluation dataset found. The LLM-as-judge literature
      confirms that for domain-expert tasks, LLM–human agreement drops to 64–68% vs.
      inter-expert baselines of ~72–75%, with gaps concentrated on factual accuracy,
      actionability, and tone. Hybrid human-in-the-loop workflows with domain-adapted
      rubrics are cited as necessary for expert-level reliability but no consulting-specific
      implementation was found. This gap remains unresolved and requires primary stakeholder
      elicitation (engagement partner annotation protocol design). Source: [WEB-12]'
net_new_fields:
  llm_judge_validity_risk:
    description: 'A critical evaluation design risk for this deployment: if LLM-as-judge
      is used to score consulting output quality (a natural choice given no human
      expert ground truth), persuasive language systematically inflates LLM judge
      scores for incorrect or weak arguments. Research across six math benchmarks
      found persuasive language leads judges to assign inflated scores by up to 8%
      on average, with the Consistency strategy (appeals to logical coherence) causing
      the most severe distortion — a pattern directly relevant to consulting arguments,
      which are designed to be persuasive. GPT-4o, the most robust judge tested, still
      shows 4.2% score inflation under persuasive influence.'
    relevance: Any automated evaluation pipeline for consulting output quality that
      uses LLM-as-judge will be vulnerable to rewarding rhetorically polished but
      substantively weak arguments — the opposite of what partner review is designed
      to catch. This makes human-in-the-loop evaluation with domain-expert reviewers
      not merely desirable but methodologically necessary for valid assessment.
    source: arXiv 2508.07805 — [WEB-27]
  consulting_sector_ai_adoption_maturity:
    description: As of October 2025, only 67 Fortune 500 companies (13.4%) had deployed
      enterprise LLM products firm-wide — a 3x increase from 22 in October 2024. Business
      consulting leads all sectors in LLM adoption at 11.10% of firms analyzed, ahead
      of law and accounting. Enterprise GenAI spending reached $37B in 2025 (3.2x
      increase from $11.5B in 2024). This rapid adoption acceleration means the deployment
      population is actively expanding and benchmark validity assessments conducted
      today will be applied to a significantly larger and more varied deployment context
      within 12–18 months.
    relevance: Benchmark validity findings for this deployment context have elevated
      urgency given the pace of consulting sector adoption; the window for pre-deployment
      assessment is short.
    sources: Bloomberry enterprise AI adoption (Oct 2025) — [WEB-1];
      Portkey enterprise LLM guide — [WEB-15]
```

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

## Expert Elicitation

## Elicitation Responses
Q1 [IO]: FOLIO tests formal deductive reasoning within closed logical worlds. How much of the consulting reasoning task is strictly deductive versus inductive, abductive, or rhetorical?
A1: Strict deductive reasoning is a small minority. The bulk is inductive and abductive — inferring opportunity size from partial data, drawing analogies from comparable engagements, and constructing rhetorical framings for specific executive audiences. Even logically structured arguments derive value from evidence selection and audience calibration, not formal validity.

Q2 [OO]: FOLIO scores outputs as a three-way logical-validity label (true/false/unknown). What counts as a 'good' output in the deployment — logical validity alone, or also persuasiveness, narrative coherence, and stakeholder calibration?
A2: A good output is one an engagement partner would present to a client — persuasive, well-structured, objection-anticipating, and audience-calibrated. Logical validity is necessary but insufficient; a technically valid but poorly framed argument fails partner review and would be scored as a failure.

Q3 [IC]: FOLIO uses self-contained, domain-knowledge-free logical worlds. Do the consulting reasoning chains depend heavily on real-world business domain knowledge?
A3: Yes, deeply so. Financial metrics, sector benchmarks, regulatory context, and competitive dynamics are the raw material of the arguments. The deployment requires the model to retrieve, weigh, and integrate messy, real-world business facts — context-free structural logic evaluation is not the goal.

## Dimension Priority Weights
| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | FOLIO's closed-world deductive ontology covers only a narrow slice of the inductive, abductive, and rhetorical reasoning types that dominate the consulting use case, per the user's explicit answer. |
| IC | HIGH | FOLIO's premises are artificial, domain-knowledge-free logical constructs, while the deployment requires reasoning over messy, real-world business facts — a direct content mismatch confirmed by the user. |
| IF | LOWER | Both benchmark and deployment are text-only in English, with no modality or script mismatch. |
| OO | HIGH | FOLIO's three-way logical-validity label is categorically misaligned with the deployment's success criteria, which include persuasiveness, narrative coherence, executive calibration, and objection anticipation. |
| OC | MODERATE | FOLIO's ground-truth labels are formally verified by an FOL inference engine — objective within the benchmark's own frame — but that frame is irrelevant to whether partner-reviewed consulting outputs succeed, creating a convergent validity gap. |
| OF | HIGH | FOLIO produces a discrete classification label (true/false/unknown); the deployment requires open-ended, long-form argumentative text structured for executive audiences — a fundamental output-form mismatch. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

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
  "region": "US Management Consulting — Business Case Reasoning",
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
