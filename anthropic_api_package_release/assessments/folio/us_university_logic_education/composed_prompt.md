I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **FOLIO: Natural Language Reasoning with First-Order Logic** is valid for use in **US Undergraduate Introductory Logic Course — Automated Validity Checker**.

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
- **Domain**: Natural language logical reasoning (first-order logic)
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2022

### Benchmark Documentation

## Key characteristics relevant to validity analysis

### 1. Input Ontology
FOLIO defines two tasks: (1) a primary natural language reasoning task requiring models to
determine the truth value of a conclusion given a set of premises [Q15], and (2) a secondary
NL-FOL translation task in which a natural language reasoning example is translated into its
FOL counterpart [Q3, Q18, Q67]. The reasoning task is explicitly framed as an independent
evaluation of logical reasoning capability [Q7]. The logical scope covers FOL including
syllogisms and combinations of conjunction, disjunction, and implication [Q43], with modal
logic and temporal logic explicitly excluded as outside the benchmark's definition of FOL
[Q139, Q140]. The benchmark does not document a propositional-only task category or
quantifier-free subset; the entire dataset is built around predicate-level FOL structures.
Reasoning complexity is a design priority: the modal depth distribution peaks at four steps,
with 28.7% of examples requiring five or more depths [Q60], and FOLIO has substantially more
distinct abstract syntax trees than prior datasets [Q61]. Models evaluated include BERT,
RoBERTa [Q84], LLaMA, GPT-3, GPT-3.5-Turbo, and GPT-4 [Q88], tested via fine-tuning and
few-shot prompting [Q82, Q87], including chain-of-thought, self-consistency, tree-of-thought
[Q89, Q90], and logic-specific methods [Q91].

A significant input-ontology gap for the deployment context is the absence of a purely
propositional task category. The course's first half is propositional (no quantifiers), and
FOLIO does not document any quantifier-free or propositional-only subset that would cover
this domain.

### 2. Input Content
FOLIO's 1,430 examples were assembled through two distinct collection pipelines [Q1, Q33].
The WikiLogic pipeline had annotators select random Wikipedia pages as creative seeds and write
entirely original stories from scratch — without templates [Q34, Q35] — yielding 304 stories
with 753 conclusion pairs and 74% of FOLIO's 4,351-word vocabulary [Q62]. The HybLogic
pipeline generated logically valid syllogistic templates and had human annotators fill abstract
entity slots with real-world content [Q40, Q42, Q44], yielding 183 stories with 682 conclusion
pairs [Q58]. The two pipelines were designed to maximize logical diversity (AST variety) and
naturalistic language breadth [Q33, Q38].

For the deployment context, both pipelines produce expert-authored naturalistic or
template-instantiated prose that differs substantially from the syntactically controlled,
pedagogically stylized register of Hurley-style course-packet problems (e.g., "All A are B,"
"If P then Q," "Some A is not B"). The paper explicitly chose to avoid bare template-style
generation in WikiLogic in favor of free composition [Q35], and adopted naturalness conventions
such as preferring "Some A is B" over existential notation [Q132, Q133] and adding epistemic
qualifiers to generalization statements [Q129]. While HybLogic's syllogistic template
structure is closer in spirit to Hurley-style templates, its instantiation with natural-language
fillers still differs from the deployment's syntactically controlled register. The possibility
that WikiLogic examples overlap with LLM training data [Q104] further complicates use as a
deployment benchmark. The dataset explicitly avoids stereotypes and identity-linked biases [Q47]
and removed or rewrote stories with opinionated language [Q127].

### 3. Input Form
FOLIO is text-only English, written in standard Latin script, by native or near-native English
speakers [Q27]. All inputs are structured natural-language text consisting of n premises and m
conclusions [Q64]. The FOL annotations use standard AI-community FOL syntax [Q52]. Readability
is documented using the Dale-Chall formula [Q59, Q154]. Grammar was checked with Grammarly and
reviewed by annotators with English Literature backgrounds [Q49, Q50], and natural-language
ambiguity was eliminated where possible [Q51]. The train/validation/test split is 70%/15%/15%
by story [Q78, Q79].

For the deployment context, the input form is well-matched: both benchmark and deployment are
English text, standard script, no modality mismatch. The primary surface-form concern is
register (natural prose vs. pedagogical templates), which is an input-content rather than
input-form issue. Sentence-level formatting conventions — e.g., how disjunction is expressed
[Q130, Q131] and how generalization statements are qualified [Q129] — differ from bare
Hurley-style templates but remain within the same textual modality.

### 4. Output Ontology
FOLIO uses a three-way label schema: True, False, or Unknown [Q36, Q66]. The logical
correctness of labels is guaranteed by FOL annotations automatically verified by an FOL
inference engine [Q2]. The label "Unknown" is defined as the case where the inference engine
returns neither True nor False given the premises [Q70]. The FOL operators in scope are
negation, conjunction, disjunction, implication, universal quantifier, existential quantifier,
and equality [Q138]; n-place predicates are used for expressivity [Q141], while Davidsonian
semantics are excluded [Q142]. The majority baseline on the test set is 38.5%, with 87 True,
78 False, and 61 Unknown examples in the test set [Q94]. GPT-4 struggles with 5% of
conclusions that have complex syntactic structure [Q120]. The inference engine proving pipeline
involves three steps: conversion to Python code, theorem-prover execution, and truth-value
output [Q153].

The output ontology is a HIGH-priority concern for the deployment context. The course's
three-way scheme — valid (premises entail conclusion), invalid (premises entail the negation
of the conclusion), and indeterminate (consistent with both conclusion and negation) — does
not map straightforwardly onto FOLIO's True/False/Unknown labels. In particular, the course's
"invalid" strictly requires the premises to entail the negation of the conclusion, not merely
the failure of entailment. The proving pipeline [Q153] does return False when the negation is
provable, but the paper does not explicitly distinguish "False because the negation is entailed"
from "False because the conclusion simply fails to follow," leaving a residual ambiguity. The
Unknown label (defined by the inference engine returning neither True nor False [Q70]) maps
conceptually onto the course's indeterminate, but the course explicitly excludes undecidable
formulas, which FOLIO does not explicitly address. The label imbalance — Unknown is the
smallest class with 61 test examples (27%) — is also relevant: if FOLIO's indeterminate rate
does not match the course's problem distribution, overall accuracy may not reliably predict
indeterminate-case performance.

### 5. Output Content
All FOL annotations were written and reviewed by expert annotators — CS undergraduate and
graduate students and senior researchers in academia and industry [Q16, Q31] — with formal
education in first-order logic or semantic parsing [Q28, Q123] and native or near-native
English proficiency [Q27, Q122]. The annotation process spanned six stages totaling 980
person-hours [Q32], with separate NL and FOL quality checks by domain experts [Q29, Q124,
Q125]. A detailed FOL annotation protocol was designed to maximize cross-annotator consistency
in FOL formula construction [Q54, Q143, Q144, Q145, Q146]. Preliminary investigations found
consistency issues in human-written FOL, prompting an additional quality-control round [Q53].
A screening pass found 39.2% of stories had at least one quality issue, all rewritten under a
detailed protocol [Q48]. Commonsense knowledge implicit in human annotation was added as
explicit premises [Q55], and tense and plural verb forms were abstracted away in FOL formulas
[Q147]. The syntactic validity and label consistency of all FOL annotations were verified by
the inference engine [Q57].

Non-expert annotators achieved only 61.82% accuracy on the test set versus 95.98% for expert
annotators [Q111], confirming the consequential role of expert quality control. GPT-4 achieves
only 64.16%, a 31.82-point gap behind expert annotators [Q113]. Confusion matrix analysis
shows systematic bias toward True predictions, with False and Unknown accuracy at only 61.9%
under fine-tuning and 54.0% under few-shot prompting [Q155, Q156, Q157]. GPT-4 sometimes uses
commonsense shortcuts to arrive at wrong truth values [Q121]. Premise ordering experiments
found less than 1% accuracy change after shuffling [Q158, Q159, Q160], indicating no spurious
ordering cues.

For the deployment context, the expert annotation pipeline and FOL-engine verification are
significant strengths: ground-truth labels for clear cases are highly reliable. The primary
concern is the label-ontology mismatch (see Output Ontology): even if individual FOLIO labels
are correct under FOLIO's own scheme, some may be systematically misaligned with the course
rubric's stricter definition of "invalid." The annotator population (expert FOL knowledge,
native English, academic context) is appropriate for the US undergraduate deployment context,
though it reflects expert rather than student-novice production norms.

### 6. Output Form
The primary metric for the NL reasoning task is accuracy [Q80], evaluated in both fine-tuned
and few-shot settings [Q19, Q23, Q93], with results reported on five randomly sampled sets
from the training set [Q93]. For NL-FOL translation, two metrics are used: Syntactic Validity
(SynV), a binary score for whether all generated FOL formulas pass a syntactic check [Q73,
Q74], and Inference Engine Execution Accuracy (ExcAcc), measuring whether translated FOL
produces matching truth values [Q75, Q76]. The proving pipeline converts FOL to Python code,
runs the theorem prover, and outputs truth values [Q153]. A custom Python FOL parser converts
human-annotated FOL to the inference engine's input format [Q150, Q151]; the inference engine
does not natively support the FOL syntax used in the dataset [Q149]. The conversion step
introduces a potential reliability gap [Q152].

For the deployment context, the output form is well-matched: both benchmark and deployment
produce a categorical label from a fixed three-item set, with accuracy as the primary metric.
The secondary NL-FOL translation metrics (SynV, ExcAcc) are not deployment-relevant. The
acknowledged gap in NL-FOL translation metric reliability [Q77] is noted but does not affect
the primary reasoning task evaluation.


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
| Q20 | 2 | output_content | "Under the few-shot setting, the most capable publicly available LLM so far achieves only 53.1% on the stories written in a hybrid manner, which is slightly better than random." |
| Q21 | 2 | output_content | "We release a natural language reasoning dataset written by expert annotators, FOLIO, with first-order logical reasoning problems." |
| Q22 | 2 | input_form | "We use formal logic, i.e., FOL to ensure the logical validity of the examples written in NL and propose a new NL-FOL translation task." |
| Q23 | 2 | output_form | "We benchmark the performance of LMs by fine-tuning models and prompting LLMs with few-shot examples, on the FOLIO reasoning task." |
| Q24 | 3 | output_content | "We collected FOLIO through a carefully designed manual annotation process to achieve high-quality examples that necessitate complex logical reasoning." |
| Q25 | 3 | output_content | "Writing natural language reasoning stories with FOL requires sufficient knowledge in both semantic parsing and first-order logic, as well as strong analytical skills." |
| Q26 | 3 | output_content | "Given the complexities of such annotations, we selected annotators based on a few important criteria to ensures that our dataset is annotated with the highest level of precision and expertise, reflecting the complexity and nuance required for first-order logical reasoning." |
| Q27 | 3 | input_form | "Our annotators are either college or graduate students who are native English speakers or possess near-native proficiency in English." |
| Q28 | 3 | output_content | "They possess formal education in first-order logic, having either completed relevant coursework or undertaken self-directed studies in first-order logic or seman-" |
| Q29 | 4 | output_content | "At the NL quality check stage, only annotators who are experts in natural language processing or computational linguistics are involved. For the FOL quality check, only annotators who are experts in first-order logic are involved." |
| Q30 | 4 | output_content | "We also give the annotators several training sessions on how to write a story, by providing them with detailed annotation guidelines." |
| Q31 | 4 | output_content | "All stories and FOL annotations in FOLIO are written and reviewed by expert annotators, including CS undergraduate and graduate students, and senior researchers, who met the aforementioned criteria." |
| Q32 | 4 | input_content | "We develop our dataset in six stages: WikiLogic collection, HybLogic collection, NL quality control, FOL quality control, NL-FOL alignment and FOL verification, spending 980 man-hours in total." |
| Q33 | 4 | input_content | "We collected our dataset using two different methods in order to obtain examples that are both logically diverse and complex and have abundant abstract syntax tree (AST) variations." |
| Q34 | 4 | input_content | "WikiLogic: annotation from scratch using Wikipedia articles as seeds. At this annotation stage, the annotators are asked to select random Wikipedia pages by repeatedly using the Wikipedia Special Random link. The Wikipedia articles are used to develop ideas for topics to write new stories." |
| Q35 | 4 | input_content | "We ask the annotators to create new stories from scratch without using templates based on real-world knowledge, which should be plausible in general." |
| Q36 | 4 | output_ontology | "Each of the stories is composed of several premises and conclusions with truth values of True, False, or Unknown (see Table 2 for an example)." |
| Q37 | 4 | output_ontology | "We also ask the annotators to write parallel FOL sentences for both the premises and conclusions." |
| Q38 | 4 | input_content | "This results in a wide range of topics, abundant AST variations, and a wide vocabulary for FOLIO." |
| Q39 | 4 | input_content | "HybLogic: hybrid annotation The task of generating logically sound stories from scratch for a set of facts is very time-consuming for human writers, where the main challenge is to create complex and varied logical patterns to arrive at a conclusion." |
| Q40 | 4 | input_content | "To address the problems of solely using manual annotation, we also consider a hybrid approach to facilitate the process. Our hybrid method is based on a common form of logical stories: syllogisms." |
| Q41 | 4 | input_ontology | "A syllogism consists of two premises and a single conclusion, and the conclusion states some facts about the entities and categories in the premises." |
| Q42 | 4 | input_content | "In this approach, we first generate logically valid stories, which are templates containing abstract categories and entities, by combining multiple syllogisms into a single story template: the conclusion of one syllogism is used as a premise for the next syllogism." |
| Q43 | 4 | input_ontology | "There are 256 logically distinct types of syllogisms and 24 of them are valid (Lehman, 1973). We use various combinations of 24 valid syllogisms. We also add in conjunction, disjunction, and implication." |
| Q44 | 4 | input_content | "We then ask human annotators to assign nouns, phrases, or clauses to the abstract entities or categories that reflect real-life scenarios to each template and write logically-valid stories in natural language." |
| Q45 | 4 | input_content | "The usage of the template is to ensure that we have a set of varied and complex logical stories with multiple conclusions. There are many ways of expressing the same logic template in natural language, and so the generated templates augment, rather than limit, the creativity of humans." |
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
| Q68 | 6 | output_ontology | "In particular, each of the NL sentence pi or hi and the parallel FOL formula pfi or hfi should be logically and semantically equivalent." |
| Q69 | 6 | output_ontology | "Moreover, the truth values for the conclusions should be the same based on the NL story S and the parallel FOL story FS." |
| Q70 | 6 | output_ontology | "In our dataset, the premises and conclusions are set up in such a way to ensure that the inference engine always returns an answer given enough resources such as time and memory." |
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
| Q101 | 8 | input_ontology | "FOLIO's unique complexity reveals that current LMs are limited in their ability to extrapolate to longer and more complex reasoning chains, and suggests an avenue for further study." |
| Q102 | 8 | output_form | "As shown in Table 6, in logical reasoning, GPT-3.5 and GPT-4 achieve substantially lower results on HybLogic than on WikiLogic and the result is slightly higher than chance." |
| Q103 | 8 | input_content | "We hypothesize that this is because HybLogic has high logical complexity that the SoTA LLMs like GPT-4 cannot solve yet while WikiLogic examples require shorter reasoning chains which the model is already capable of solving." |
| Q104 | 8 | input_content | "Moreover, since the examples in WikiLogic are created from scratch by humans, it is possible that LLMs have seen similar texts with similar logical patterns in the training data." |
| Q105 | 8 | input_content | "However, fine-tuning RoBERTa-large achieves higher performance on HybLogic than on WikiLogic. This is likely because HybLogic is created from templates and some of the logical patterns can be learned during fine-tuning." |
| Q106 | 8 | input_content | "In NL-FOL translation, performs 10 points better on HybLogic than WikiLogic. This could be because WikiLogic has more distinct and diverse sentence-level logical and language patterns and FOL annotations. WikiLogic has 53 ASTs while HybLogic has 33." |
| Q107 | 9 | output_content | "We collected truth value annotations of logical reasoning for FOLIO test set from expert and non-expert annotators." |
| Q108 | 9 | output_content | "Our expert annotators are computer science college students familiar with FOL." |
| Q109 | 9 | output_content | "Non-expert annotators are community college or high school students who have not taken the SAT." |
| Q110 | 9 | output_content | "Both expert and non-expert annotators are native English speakers." |
| Q111 | 9 | output_content | "Expert annotations achieve an accuracy of 95.98% while non-expert annotations achieves 61.82%, with a gap of 34.16%." |
| Q112 | 9 | input_ontology | "This shows that sufficient domain knowledge of FOL is necessary for good performance on FOLIO." |
| Q113 | 9 | output_content | "The expert and GPT-4 gap is 31.82%, suggesting significant room for model improvement." |
| Q114 | 9 | input_content | "We focus on collecting a very high-quality dataset in evaluating logical reasoning rather than merely a large dataset." |
| Q115 | 9 | output_content | "Optimizing for quality required us to adopt a rigorous annotation process with domain experts selected based on a few important criteria as mentioned in Appendix A: Annotator Selection." |
| Q116 | 9 | input_content | "Significantly scaling up this process would have required resources beyond our current means and we are unable further expand our dataset for investigating how the size of training data affects the performance of fine-tuning experiments." |
| Q117 | 9 | input_content | "We encourage the community to apply our annotation protocol to expand this realistic and complex FOL reasoning story set." |
| Q118 | 9 | output_form | "Approximately 65% of the time, the model struggles to construct accurate reasoning chains for complex problems with intricate steps, leading to faulty reasoning paths and indicating a limited ability to solve problems with long reasoning chains." |
| Q119 | 9 | output_form | "In 25% of cases, erroneous derivations occur within certain reasoning steps, highlighting potential inaccuracies and flaws in logical deductions." |
| Q120 | 9 | output_ontology | "5% of conclusions in FOLIO have a complex syntactic structure, posing comprehension challenges for GPT-4." |
| Q121 | 9 | output_content | "5% of outputs show that GPT-4 leverage commonsense reasoning to employ spurious shortcuts that lead to the wrong truth value for the conclusion." |
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
| Q158 | 15 | output_content | "To test if the premise ordering in FOLIO has spurious correlations with the conclusion label which a model can exploit, we shuffle the input premises to evaluate models." |
| Q159 | 15 | output_content | "We find that accuracy increases or decreases by roughly 1% in most settings compared to our unshuffled premises." |
| Q160 | 15 | output_content | "This indicates that the ordering of premises in FOLIO examples does not yield significant information about the label, and thus models will not be able to use the premise ordering as a strong heuristic or statistical feature for its predictions." |
| Q161 | 15 | output_ontology | "FOL formulas have a clearer and more straightforward logical structure than NL sentences." |
| Q162 | 15 | output_form | "As shown in Table 11, the performance slightly increases in the NL+FOL setting for GPT-4 while GPT-3.5 performs worse in both the NL+FOL and the FOL-only settings." |
| Q163 | 15 | output_form | "FOL always serves as additional useful information for GPT-4, but not for GPT-3.5 regardless of whether FOL is concatenated with NL." |

---

## Regional Context

```yaml
name: US Undergraduate Introductory Logic Course — Automated Validity Checker
abbreviation: us_undergrad_intro_logic
benchmark: folio
assessment_slug: us-undergrad-intro-logic_folio
population:
  description: 'US university undergraduates enrolled in introductory formal reasoning
    or symbolic logic courses. Students have no assumed prior background in formal
    logic. They interact with the system through a logic-checking tool that accepts
    natural-language arguments and returns one of three classification labels: valid,
    invalid, or indeterminate. The tool is intended as a pedagogical aid aligned to
    a specific course rubric.'
  institution_type: US four-year university (undergraduate)
  course_context: Introductory formal logic / critical reasoning course, modeled on
    Hurley's Concise Introduction to Logic. First half covers propositional logic
    (connectives, truth tables, basic argument forms); second half covers first-order
    predicate logic (quantifiers, basic predicate structure). Strictly classical deductive
    logic throughout; modal, temporal, and probabilistic reasoning are not in scope.
  prior_domain_knowledge: None assumed. Students are novice-level reasoners encountering
    formal logic for the first time. They are not expected to know FOL notation, proof
    theory, or technical semantics.
  role_in_system: End users submitting natural-language logic problems drawn from
    a course packet; receiving automated validity classifications as feedback or grading
    support.
  demographic_variation: Not a primary concern. The population is functionally uniform
    in language (English, monolingual academic register) and educational context.
    No sub-national, ethnic, or socioeconomic segmentation is identified as salient
    for this assessment.
language:
  primary: English
  variant: US academic English
  script: Standard Latin alphabet
  register_notes: Dominant input register is syntactically controlled, pedagogically
    stylized English derived from Hurley-style course-packet templates (e.g., 'All
    A are B,' 'If P then Q,' 'Some A is not B'). Natural-language paraphrases are
    introduced later in the course but remain a secondary register. FOLIO's naturalistic,
    annotator-composed prose is a distinct and more varied register than the deployment's
    primary input style.
  nli_tooling_availability: Strong — English is the dominant language for NLP/NLI
    tooling; no resource gaps.
input_ontology:
  logical_scope:
    propositional_logic: First-half course content. Connectives (negation, conjunction,
      disjunction, conditional, biconditional), truth tables, basic valid argument
      forms (modus ponens, modus tollens, hypothetical syllogism, disjunctive syllogism,
      etc.). No quantifiers.
    first_order_predicate_logic: Second-half course content. Universal and existential
      quantifiers, basic predicate structure, syllogistic forms, combinations of quantifiers
      with connectives. Matches FOLIO's primary logical scope.
    excluded: Modal logic, temporal logic, probabilistic reasoning, inductive reasoning,
      informal fallacies (unless recast as formal arguments).
  folio_coverage_of_propositional_logic: 'FOLIO contains no documented quantifier-free
    or propositional-only subset. The FOL2NS paper (arxiv 2605.18155) explicitly notes
    that ''quantifier is the key feature that sets FOL and other propositional logics
    apart'' and treats FOLIO as inherently FOL with quantifier depth as a core design
    parameter. No paper surveying FOLIO identifies a propositional sub-corpus. LogicBench
    (ACL 2024 — [WEB-1]) is a complementary
    benchmark that explicitly covers nine propositional inference rules (modus ponens,
    modus tollens, hypothetical syllogism, disjunctive syllogism, and others) alongside
    FOL axioms, and would substantially close the propositional coverage gap for the
    course''s first half. Source: FOL2NS — [WEB-2]; LogicBench
    — [WEB-1]'
  reasoning_depth_profile: Introductory course problems are typically shallow (1–3
    reasoning steps). FOLIO's design peaks at 4-step reasoning depth with 28.7% of
    examples requiring 5+ steps — substantially deeper than the deployment target.
    This mismatch may inflate apparent difficulty relative to course-representative
    inputs.
  template_style_coverage_in_folio: 'No FOL benchmark was found that explicitly samples
    from Hurley-style bare-template sentence forms. FOLIO''s HybLogic pipeline is
    closest in spirit (syllogistic templates instantiated with natural-language fillers),
    but its naturalistic prose instantiation still differs from the deployment''s
    unqualified syntactic templates. LogicBench uses heuristically designed templates
    that are more controlled than FOLIO''s prose but are purpose-built for single-inference-rule
    isolation rather than course-packet simulation. No supplementary dataset replicating
    the exact Hurley-style register was identified. Source: LogicBench — [WEB-1];
    [NOT FOUND — no benchmark explicitly sampling Hurley-style bare templates found
    after searching ACL Anthology and arXiv]'
output_ontology:
  deployment_label_schema:
    valid: Premises deductively entail the conclusion.
    invalid: 'Premises entail the negation of the conclusion. Strict definition: not
      merely failure to entail, but positive entailment of the negation.'
    indeterminate: Premises are consistent with both the conclusion and its negation
      — neither entailment nor contradiction. Undecidable formulas are not in scope.
  folio_label_schema:
    'True': Conclusion follows from premises (inference engine returns True); formally
      S ⊨ H.
    'False': Inference engine returns False; formally S ⊨ ¬H — the negation of the
      conclusion is entailed by the premises.
    Unknown: Inference engine returns neither True nor False; formally S ⊭ H and S
      ⊭ ¬H — premises are consistent with both the conclusion and its negation.
  label_mapping_concerns:
    valid_to_True: Conceptually aligned. Both require deductive entailment of the
      conclusion from premises (S ⊨ H).
    invalid_to_False: 'ALIGNMENT CONFIRMED. The course''s ''invalid'' strictly requires
      premises to entail the negation of the conclusion. FOLIO''s ''False'' label
      is formally defined as S ⊨ ¬H by the resolution-based Stanford CS221 inference
      engine: the engine tests entailment of ¬H by adding ¬(¬H) = H to the KB and
      checking for unsatisfiability, meaning False is returned only when the negation
      is provably entailed — not merely when the conclusion fails to follow. This
      formal equivalence resolves the previously flagged ambiguity. Source: CGD-PD
      paper formal definition — [WEB-3]; Stanford CS221
      resolution engine semantics — [WEB-4]'
    indeterminate_to_Unknown: 'ALIGNMENT CONFIRMED. FOLIO''s Unknown is formally defined
      as S ⊭ H and S ⊭ ¬H (the premises neither entail the conclusion nor its negation),
      which precisely matches the course''s indeterminate definition of ''premises
      consistent with both the conclusion and its negation.'' The FOLIO paper (Q70)
      specifies that the premises and conclusions are set up so the inference engine
      always returns an answer given sufficient resources, meaning undecidable formulas
      are excluded by construction — directly matching the course''s exclusion of
      undecidable cases. Source: CGD-PD paper formal definition — [WEB-3];
      FOLIO paper Q70 — [WEB-5]'
  label_distribution_in_folio_test_set:
    'True': 87
    'False': 78
    Unknown: 61
    majority_baseline_pct: 38.5
    unknown_share_pct: '27.0% (61 of 226 test examples). This is the smallest class.
      Whether this matches the course''s expected indeterminate problem rate depends
      on course-packet design and cannot be resolved from public sources; course instructors
      should verify their typical indeterminate problem frequency against this baseline.
      [NEEDS VERIFICATION — deferred: requires course-instructor elicitation, not
      searchable from public sources]'
  model_performance_on_false_and_unknown: 'FOLIO confusion matrix analysis shows False
    and Unknown accuracy at only 61.9% (fine-tuning) and 54.0% (few-shot prompting)
    — substantially below True accuracy. This is a high-priority reliability concern
    for the deployment''s indeterminate and invalid categories. Note: a 2026 cleaning
    pipeline using the Vampire theorem prover found label errors and misalignments
    in the original FOLIO dataset; after cleaning, auto-formalization achieved 86.70%
    on the validation set, suggesting some of the original low performance reflects
    annotation noise rather than pure reasoning difficulty. Source: Agentified Assessment
    paper — [WEB-6]'
input_content:
  deployment_source: Custom course packet modeled on Hurley's Concise Introduction
    to Logic. Problems feature heavily templated sentence forms (e.g., 'All A are
    B,' 'If P then Q,' 'Some A is not B'). Natural-language paraphrases appear later
    in the term but are secondary.
  folio_source_pipelines:
    WikiLogic: Annotators wrote original stories from scratch using Wikipedia pages
      as creative seeds, explicitly without templates. Yields naturalistic, topic-diverse
      prose — substantially different register from Hurley-style templates.
    HybLogic: Syllogistic logical templates were generated and instantiated with human-authored
      natural-language fillers. Logically closer in spirit to course-packet forms
      but still uses naturalistic prose instantiation rather than bare syntactic templates.
  register_mismatch_severity: HIGH — FOLIO explicitly avoided bare template-style
    generation (WikiLogic pipeline) and adds epistemic qualifiers to generalizations
    and naturalistic disjunction phrasing — all differing from deployment's unqualified
    Hurley-style templates.
  potential_llm_training_data_overlap: WikiLogic examples may overlap with LLM pretraining
    data, which could inflate apparent model performance on those examples relative
    to held-out course-packet inputs.
input_form:
  modality: Text only
  script: Standard Latin alphabet
  format: Structured natural-language premises and conclusions
  language_naturalness: 'FOLIO: grammar-checked, naturalness-reviewed by English Literature
    annotators, NL ambiguity minimized. Deployment: syntactically controlled pedagogical
    templates, not naturalistic prose.'
  modality_mismatch: None — both benchmark and deployment are text-only English. Surface-form
    concern is register (naturalistic prose vs. pedagogical templates), not modality.
  readability_complexity: '[NOT FOUND — The FOLIO paper references a Dale-Chall readability
    distribution in Figure 3 (Q154) but does not report a mean score in any accessible
    text passage. No secondary source reporting FOLIO''s mean Dale-Chall score was
    found. Introductory logic course-packet problems using short, controlled templates
    (e.g., ''All A are B,'' ''If P then Q'') would likely score in the 5–7 range on
    Dale-Chall, appropriate for grades 5–10, whereas FOLIO''s naturalistic Wikipedia-seeded
    prose with technical predicates may score higher. Resolution requires direct inspection
    of the FOLIO paper''s Figure 3 or computation from the released dataset — [WEB-7]]'
output_form:
  deployment_output: 'Categorical label from fixed three-item set: valid / invalid
    / indeterminate'
  folio_primary_metric: Accuracy (categorical label from True / False / Unknown)
  form_match: Well-matched — both benchmark and deployment produce a single categorical
    label from a fixed small set. Output form is not a priority concern.
  secondary_folio_metrics: NL-FOL translation metrics (SynV, ExcAcc) — not relevant
    to the deployment's primary reasoning task evaluation.
  primary_evaluation_metric: Accuracy, reported per label class (critical given label
    imbalance and known model bias toward True predictions)
output_content:
  folio_annotation_quality: Expert-annotated by CS undergraduate and graduate students
    and senior researchers with formal FOL training. Six-stage annotation process,
    980 person-hours. Separate NL and FOL expert quality checks. All labels FOL-engine
    verified. Expert human accuracy 95.98%.
  label_reliability_strengths: Strong for True (valid) cases where entailment is clear.
    FOL-engine verification provides proof-theoretic grounding. The False label is
    formally S ⊨ ¬H (entailment of negation confirmed by the resolution prover), directly
    matching the course's strict 'invalid' definition.
  label_reliability_concerns: 'A 2026 data-cleaning study using the Vampire theorem
    prover found label errors and NL-FOL misalignments in the original FOLIO dataset,
    flagging it as having ''potential label errors and misalignments between natural
    language and formal annotations due to the complexity of semantic parsing.'' Users
    deploying FOLIO for the validity-checker assessment should consider using the
    cleaned split if available. Source: Agentified Assessment paper — [WEB-6]'
  annotator_population_match: FOLIO annotators are expert FOL-trained academics, appropriate
    for generating reliable ground-truth labels. They do not represent the novice-student
    production norms of the deployment population, but this is expected and not a
    concern for ground-truth label quality.
  premise_ordering_bias: Confirmed absent — shuffling premises changes accuracy by
    less than 1%, indicating no spurious ordering cues in FOLIO labels.
pedagogical_context:
  textbook_reference: Hurley, P. J., Concise Introduction to Logic (various editions)
  typical_problem_forms:
  - All A are B.
  - Some A is not B.
  - If P then Q.
  - Either P or Q.
  - No A is B.
  - Some A is B.
  - P if and only if Q.
  rubric_definitions:
    valid: Premises deductively entail the conclusion; truth of premises guarantees
      truth of conclusion.
    invalid: Premises entail the negation of the conclusion (not merely failure to
      entail — positive entailment of negation required).
    indeterminate: Premises are consistent with both the conclusion and its negation;
      no entailment in either direction.
  course_structure_implications_for_benchmark: 'The course''s first half (propositional
    logic) is not covered by FOLIO''s documented scope. Benchmark results will be
    informative only for the second half (FOL). A tool assessment using FOLIO alone
    will systematically undertest propositional-logic performance. LogicBench (ACL
    2024) provides explicit coverage of nine propositional inference rules (MP, MT,
    HS, DS, CD, DD, BD, CT, MI) and is recommended as a complementary benchmark for
    the first-half propositional scope. Source: LogicBench — [WEB-1]'
flagged_verification_targets:
- id: FV1
  priority: HIGH
  label: FOLIO False-label annotation protocol
  question: Does FOLIO's 'False' label strictly require that the FOL prover confirms
    entailment of the negation of the conclusion, or can it also apply when the conclusion
    merely fails to follow (negation-as-failure)? Verify the exact proving pipeline
    semantics for the False label.
  search_target: FOLIO false label annotation protocol entailment negation vs failure
    to entail FOL prover semantics
  resolution: 'RESOLVED — ALIGNED. The CGD-PD paper (arxiv 2604.06196) provides the
    formal definition: False = S ⊨ ¬H (premises entail the negation of the conclusion),
    and Unknown = S ⊭ H and S ⊭ ¬H. The Stanford CS221 resolution-based inference
    engine used in FOLIO tests entailment by adding the negation of the query to the
    KB and checking for unsatisfiability (contradiction), meaning False is returned
    only when negation is provably entailed — not as negation-as-failure. This fully
    aligns with the course''s strict ''invalid'' definition. The label-mapping concern
    originally flagged under OO is now resolved as aligned. Source: [WEB-3];
    [WEB-4]'
- id: FV2
  priority: HIGH
  label: FOLIO propositional logic coverage
  question: What proportion of FOLIO examples are quantifier-free or propositional-only?
    Is there any documented propositional subset or split?
  search_target: FOLIO propositional logic subset quantifier-free examples benchmark
    coverage
  resolution: 'RESOLVED — FULL GAP CONFIRMED. No quantifier-free or propositional-only
    subset exists in FOLIO. The FOL2NS paper explicitly characterizes FOLIO as inherently
    FOL with quantifier depth as a core structural parameter, noting that quantifiers
    are ''the key feature that sets FOL and other propositional logics apart.'' The
    propositional coverage gap for the course''s first half is confirmed as a full
    gap. LogicBench (ACL 2024) is identified as the primary supplementary benchmark
    to close this gap, covering nine propositional inference rules including all major
    forms tested in introductory courses (MP, MT, HS, DS). Source: FOL2NS — [WEB-2];
    LogicBench — [WEB-1]'
- id: FV3
  priority: HIGH
  label: Hurley-style template register in FOL benchmarks
  question: Does FOLIO or any related FOL benchmark explicitly sample from formal-logic
    textbook problem styles (Hurley-style bare templates)? Are there supplementary
    datasets that better represent this register?
  search_target: FOL benchmark textbook-style templated sentences Hurley logic course
    evaluation
  resolution: SEARCHED, NOT FOUND — No benchmark explicitly designed to replicate
    Hurley-style bare-template sentence forms ('All A are B,' 'If P then Q') was identified.
    LogicBench uses heuristically designed templates for single-inference-rule isolation
    but targets rule-by-rule evaluation rather than course-packet simulation. The
    register mismatch remains unaddressed by any existing benchmark. Practitioners
    should consider constructing a small course-packet-aligned probe set for deployment-specific
    validation.
- id: FV4
  priority: MODERATE
  label: FOLIO Unknown/indeterminate class distribution and course base rate
  question: Confirm FOLIO Unknown class share (~27% of test set). Investigate whether
    the course's expected indeterminate problem distribution differs substantially,
    and whether this mismatch would distort accuracy metrics for the indeterminate
    category.
  search_target: FOLIO unknown indeterminate class distribution base rate logic benchmark
    three-way classification
  resolution: 'PARTIALLY RESOLVED. FOLIO Unknown share is confirmed at 27.0% (61/226
    test examples) — the smallest class. Whether this matches the course''s indeterminate
    problem rate requires course-instructor elicitation and cannot be resolved from
    public sources. The formal definition of Unknown (S ⊭ H and S ⊭ ¬H) is confirmed
    as precisely matching the course''s indeterminate definition. The performance
    concern remains: False and Unknown combined accuracy is only 61.9% (fine-tuning)
    and 54.0% (few-shot). [NEEDS VERIFICATION — deferred: course-instructor elicitation
    required to compare FOLIO''s 27% Unknown rate against actual course problem distribution]'
- id: FV5
  priority: MODERATE
  label: FOLIO Unknown label and undecidability
  question: Does FOLIO's Unknown category ever include undecidable formulas? The course
    explicitly excludes undecidable cases from its indeterminate category; any residual
    inclusion in FOLIO could introduce label misalignment.
  search_target: FOLIO unknown label undecidable formulas inference engine semantics
  resolution: 'RESOLVED — NO MISMATCH. FOLIO paper Q70 states: ''the premises and
    conclusions are set up in such a way to ensure that the inference engine always
    returns an answer given enough resources such as time and memory.'' This means
    undecidable formulas are excluded by construction — the Unknown label arises only
    from logical underspecification (S ⊭ H and S ⊭ ¬H), not from undecidability. This
    directly matches the course''s requirement that indeterminate excludes undecidable
    cases. Source: FOLIO paper Q70 — [WEB-5]'
- id: FV6
  priority: LOWER
  label: FOLIO Dale-Chall readability score vs. course-packet complexity
  question: What is the mean Dale-Chall readability score for FOLIO examples, and
    how does it compare to the expected reading complexity of introductory logic course-packet
    problems?
  search_target: FOLIO Dale-Chall readability score distribution introductory logic
    textbook complexity
  resolution: '[NOT FOUND — The FOLIO paper reports a readability distribution in
    Figure 3 but does not state a mean score in any accessible text passage. No secondary
    source reports FOLIO''s mean Dale-Chall score. Resolution requires direct inspection
    of Figure 3 in the FOLIO paper PDF or computation from the released GitHub dataset:
    [WEB-7]. Hurley-style templates (''All A are B,''
    ''If P then Q'') are structurally short and use familiar vocabulary, likely scoring
    5–7 (grades 5–10 range on Dale-Chall), whereas FOLIO''s Wikipedia-seeded naturalistic
    prose with technical predicate vocabulary likely scores higher. This is a low-impact
    gap for scoring purposes.]'
dimension_priority_summary:
  IC: HIGH — Register mismatch between FOLIO's naturalistic annotator-composed prose
    and the deployment's Hurley-style syntactically controlled templates is the primary
    input-content concern. May inflate or deflate apparent model capability on course-representative
    inputs. No existing benchmark closes this specific register gap.
  OO: MODERATE (downgraded from HIGH) — The previously flagged label-mapping ambiguity
    for 'invalid' and 'indeterminate' has been resolved. FOLIO's False = S ⊨ ¬H (entailment
    of negation confirmed by resolution prover) and Unknown = S ⊭ H and S ⊭ ¬H (neither
    entailment nor contradition, undecidables excluded by construction) both align
    directly with the course's strict rubric definitions. The label schema mapping
    is now confirmed as well-aligned across all three categories.
  IO: MODERATE — FOLIO's FOL scope aligns with the course's second half, but the complete
    absence of a propositional-only subset creates a systematic coverage gap for the
    first half of the course. LogicBench is recommended as a complementary benchmark
    to cover propositional inference rules.
  OC: MODERATE — Expert annotation quality is high, but a 2026 cleaning study identified
    label errors and NL-FOL misalignments in the original dataset. The cleaned FOLIO
    split (using Vampire theorem prover verification) is preferable for deployment
    assessment if available.
  IF: LOWER — No modality or script mismatch; both are English text, standard Latin
    alphabet.
  OF: LOWER — Both benchmark and deployment use a fixed categorical label from a small
    set; output form is well-matched.
net_new_fields:
  folio_label_formal_semantics_confirmed: 'A 2025/2026 paper on consistency-guided
    decoding (CGD-PD) explicitly formalizes FOLIO''s three-way label schema as: True
    = S ⊨ H, False = S ⊨ ¬H, Unknown = S ⊭ H and S ⊭ ¬H. This confirmation resolves
    the highest-priority label-mapping concern in the original assessment. Source:
    CGD-PD — [WEB-3]'
  folio_cleaning_pipeline_2026: 'A 2026 paper introduced a systematic data-cleaning
    pipeline for FOLIO using the Vampire theorem prover to identify label errors and
    NL-FOL misalignments, described as arising from ''the complexity of semantic parsing.''
    After cleaning, an auto-formalization agent achieved 86.70% accuracy on the validation
    set (vs. 73.89% for chain-of-thought baseline), suggesting original low performance
    partly reflects annotation noise. Deployment assessments should prefer the cleaned
    split when available. Source: Agentified Assessment — [WEB-6]'
  logicbench_as_complementary_benchmark: 'LogicBench (ACL 2024, Parmar et al.) explicitly
    covers 25 reasoning patterns across propositional, first-order, and non-monotonic
    logics, including nine propositional inference rules directly relevant to the
    course''s first half: modus ponens (MP), modus tollens (MT), hypothetical syllogism
    (HS), disjunctive syllogism (DS), constructive dilemma (CD), destructive dilemma
    (DD), bidirectional dilemma (BD), commutation (CT), and material implication (MI).
    It uses controlled NL templates evaluated against single inference rules, making
    it a strong complement to FOLIO for assessing propositional-logic performance
    in the deployment context. Source: LogicBench ACL 2024 — [WEB-1]'
  folio_unknown_epistemic_ambiguity_in_llm_outputs: 'Recent work (CGD-PD, 2026) identifies
    a practical failure mode relevant to the deployment: in LLM-based pipelines, the
    Unknown label plays a dual role — it can represent genuine logical underspecification
    (S ⊭ H and S ⊭ ¬H), but can also act as an implicit abstention when the model
    is uncertain. This means that even if FOLIO''s Unknown ground-truth labels are
    well-defined, a deployed model''s ''indeterminate'' outputs may conflate genuine
    logical underspecification with model uncertainty — a distinction the course rubric
    requires but that accuracy metrics alone cannot diagnose. Source: CGD-PD — [WEB-3]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://aclanthology.org/2024.acl-long.739/ |
| WEB-2 | https://arxiv.org/abs/2605.18155 |
| WEB-3 | https://arxiv.org/abs/2604.06196 |
| WEB-4 | https://stanford-cs221.github.io/autumn2022-extra/modules/logic/first-order-resolution.pdf |
| WEB-5 | https://arxiv.org/abs/2209.00840 |
| WEB-6 | https://arxiv.org/abs/2603.02788 |
| WEB-7 | https://github.com/Yale-LILY/FOLIO |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: FOLIO covers first-order logic deductive reasoning broadly, but introductory undergraduate logic courses vary in scope. Does your course focus primarily on propositional logic, predicate/first-order logic, or a mix? Are modal logic, temporal reasoning, or probabilistic arguments in scope, or strictly classical deductive logic?
A1: The course covers both propositional and predicate/first-order logic (with FOL as the second-half focus), strictly within classical deductive logic. Quantifiers, connectives, and basic predicate structure are all in scope; modal, temporal, and probabilistic reasoning are not.

Q2 [OO]: Your tool outputs one of three labels — valid, invalid, or indeterminate. Does your course treat 'indeterminate' as a single category, or does it distinguish between e.g. undecidable formulas vs. conclusions not entailed but not contradicted either?
A2: 'Indeterminate' means the premises are consistent with both the conclusion and its negation — neither entailment nor contradiction. Undecidable formulas are not in scope. The rubric treats valid, invalid (premises entail the negation of the conclusion), and indeterminate as three fully distinct, non-collapsed categories.

Q3 [IC]: Are students' problems drawn from a specific textbook or problem set with a constrained syntactic style that might differ from FOLIO's sentence patterns?
A3: Problems come from a custom course packet modeled on Hurley's style, featuring heavily templated sentence forms (e.g., "All A are B," "If P then Q," "Some A is not B"). Natural-language paraphrases are introduced later in the term but remain a secondary register; the dominant style is syntactically controlled and pedagogically stylized.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | FOLIO's FOL scope aligns well with the course's second-half focus, but the benchmark may underrepresent purely propositional problems that constitute the course's first half, creating a coverage gap for that sub-domain. |
| IC | HIGH | The deployment uses highly constrained, template-driven sentence patterns (Hurley-style) while FOLIO uses expert-authored naturalistic text; surface-form mismatch may introduce construct-irrelevant difficulty or inflate/deflate apparent model capability on course-representative inputs. |
| IF | LOWER | Both benchmark and deployment are text-only, English, standard Latin script — no modality or infrastructure mismatch. |
| OO | HIGH | FOLIO's native output space is true/false/unknown and may not map cleanly onto the deployment's three-way valid/invalid/indeterminate scheme, especially since 'invalid' in the course requires premises to *entail the negation* (not merely fail to entail the conclusion), a stricter and distinct condition from FOLIO's 'false' label. |
| OC | MODERATE | FOLIO is expert-annotated with FOL-engine verification, which strengthens label reliability for clear cases, but the three-way label mapping (see OO) means some ground-truth labels may be systematically misaligned with the course rubric's definitions, even if individually correct under FOLIO's own scheme. |
| OF | LOWER | Both benchmark and deployment produce a categorical label from a small fixed set; the output form is well-matched. |

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
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | FOLIO train | Ex 1 (story 271) | True | "No plants are fungi. Mushrooms are fungi." / conclusion: "No plants are mushrooms." | Two-premise syllogism with "No A are B" / "All C are B" form — structurally close to Hurley-style templates | IC, IO |
| D2 | FOLIO train | Ex 12 (story 257) | True | "Some cats are not pets. All cats are mammals." / conclusion: "Some mammals are not pets." | Minimal two-premise syllogism using Hurley-canonical forms ("Some A is not B", "All A are B") | IC, IO |
| D3 | FOLIO train | Ex 20 (story 269) | Uncertain | "All proteins are organic compounds. All enzymes are organic compounds." / conclusion: "All enzymes are proteins." | Two-premise syllogism illustrating classic undistributed-middle fallacy — directly analogous to Hurley course problems | IC, OO |
| D4 | FOLIO train | Ex 50 (story 284) | Uncertain | "Each building is tall. Everything tall has height." / conclusion: "All buildings are magnificent." | Minimal two-premise syllogism with irrelevant conclusion — indeterminate case, pedagogically transparent | IC, OO |
| D5 | FOLIO train | Ex 9 (story 264) | Uncertain | "No television stars are certified public accountants. All certified public accountants have good business sense." / conclusion: "All television stars have good business sense." | Two-premise syllogism, "No A are B" / "All B are C" form — near-Hurley template register | IC |
| D6 | FOLIO train | Ex 53 (story 37) | True | "Heptalogyy is a compound literary or narrative work that is made up of seven distinct works. The Harry Potter series consists of 7 distinct works." / conclusion: "The Harry Potter series of books is Heptalogy." | Simple two-premise syllogism with named entities; close to textbook form | IC |
| D7 | FOLIO train | Ex 2 (story 376) | Uncertain | "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises. People in this tech company who wear the same flannel shirts every day are consistent..." | Long naturalistic prose narrative with 7 premises and XOR embedded in premise — substantially more complex than Hurley problems | IC, IO |
| D8 | FOLIO train | Ex 3 (story 180) | Uncertain | "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac. Sam is using a Mac. If Sam uses a Mac, he will play a song." | 6-premise narrative scenario with chained conditionals and exclusive disjunction | IC, IO |
| D9 | FOLIO train | Ex 13 (story 395) | False | "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable...ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." | Complex branded-product scenario with 5 premises and compound conclusion | IC |
| D10 | FOLIO train | Ex 21 (story 381) | False | "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing...If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up..." | 6-premise Wikipedia-seeded narrative; convoluted tautological final premise | IC |
| D11 | FOLIO train | Ex 4 (story 408) | False | "No trick-shot artist in Yale's varsity team struggles with half court shots...Jack is on Yale's varsity team, and he is either a trick-shot artist or he successfully shoots a high percentage of 3-pointers." | Sports-domain narrative, 5 premises, label=False — tests invalid-conclusion case | OO, OC |
| D12 | FOLIO train | Ex 17 (story 70) | False | "Michael O'Donnell is a British physician, journalist, author, and broadcaster...Michael O'Donnell was born in Yorkshire as the son of a general practitioner." / conclusion: "There are no journalists that were born in Yorkshire." | WikiLogic biographical narrative; False label from clear counterexample in premises | OO, OC |
| D13 | FOLIO train | Ex 29 (story 210) | False | "The only types of mammals that lay eggs are either platypuses or echidnas...Grebes are not platypuses and also not echidnas." / conclusion: "Hyraxes lay eggs." | Biology-domain story; False conclusion via FOL entailment of negation | OO |
| D14 | FOLIO train | Ex 28 (story 252) | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency...There is an embargo on Russian foreign trade goods." / conclusion: "In Russia, an effective monetary policy is possible." | Economics-domain story; False via chain of conditionals; requires domain knowledge about Russia | IC |
| D15 | FOLIO train | Ex 6 (story 423) | Uncertain | "Everyone at the business conference is either an investor or an entrepreneur...Ho is at the business conference and prefers state ownership of the means of production." / conclusion: "Ho is not an ardent communist." | Unknown because ardent communist status is underdetermined given premises | OO |
| D16 | FOLIO train | Ex 22 (story 475) | Uncertain | "All PRC nationals are entitled to national social insurance coverage...Mei is at the Franco-China diplomatic conference." / conclusion: "Mei is a PRC national." | Diplomatic conference scenario; Uncertain because Mei's nationality not determinable | OO |
| D17 | FOLIO train | Ex 23 (story 108) | Uncertain | "The world's only major large passenger aircraft manufacturers are Boeing and Airbus...Airbus made more revenue than Boeing last year." / conclusion: "There exists a SpaceX commercial aircraft." | Conclusion about SpaceX is irrelevant to premises — clear indeterminate case | OO |
| D18 | FOLIO train | Ex 43 (story 393) | True | "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning...Modus Ponens is a component of a major part of reasoning rule." | Logic-domain story mentioning Modus Ponens — meta-logical content | IC |
| D19 | FOLIO train | Ex 7 (story 30) | Uncertain | "EndGame is a movie released in 2006...Andy Chang is from Hong Kong." / conclusion: "All of Andy Chang's movies are filmed outside of Washington." | WikiLogic film-domain story with insufficient premises to determine universal conclusion | IO, OO |
| D20 | FOLIO train | Ex 11 (story 486) | False | "Everything in Size Town is big or small...The bird is in Size Town and it is not both heavy and still." / conclusion: "If the bird is small or still, then it is either unpredictable or changing." | Abstract "Size Town" scenario; complex conditional conclusion with XOR | IC, OO |
| D21 | FOLIO train | Ex 16 (story 346) | True | "All professional athletes spend most of their time on sports...If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." / conclusion: "Amy is neither a full-time scientist nor an Olympic gold medal winner." | 6-premise chained syllogism with conditional; multi-step reasoning | IO |
| D22 | FOLIO train | Ex 33 (story 341) | Uncertain | "No battery-powered watch is automatic...Moonwatch is either a digital watch and an automatic, or it is neither." / conclusion: "Moonwatch is a mechanical watch." | Watch-domain story; mechanical watch status underdetermined from premises | OO |
| D23 | FOLIO train | Ex 38 (story 425) | False | "Everyone working at Meta has a high income...James has a car or works at Meta." / conclusion: "James is a student." | Modern tech-company scenario; False conclusion derivable via short chain | IC |
| D24 | FOLIO train | Ex 52 (story 337) | True | "No athletes never exercise...Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." (Note: conclusion uses "Jim" while premises use "John/Jim" inconsistently) | Name inconsistency between premises (John) and conclusion (Jim) — annotation quality issue | OC |
| D25 | FOLIO train | Ex 34 (story 377) | True | "All orphan planets are rogue planets...PSO J318.5−22 is a rogue planet." / conclusion: "PSO J318.5−22 is an orphan planet or it does not have the Sun as its star, or both." | Astronomy domain; complex disjunctive conclusion | IC |
| D26 | FOLIO train | Ex 56 (story 27) | Uncertain | "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin...Yangshuo is not a district in Guilin." / conclusion: "Kowloon District is in Hong Kong." | Irrelevant conclusion — Unknown because premises have nothing to say about Hong Kong | OO |
| D27 | FOLIO train | Ex 2 (story 376) | Uncertain | FOL premise: "¬(∃y (flannelShirt(y) ∧ WearEveryday(x, y)) ∧ Have(mike, highEnergy) ∧ Impulsive(mike)) → (Consistent(mike) ∧ StickTo(mike, theirRegularRoutine)) ⊕ ¬Like(mike, surprise)" | Malformed FOL — free variable `x` in antecedent of conditional; annotation error | OC |
| D28 | FOLIO train | Ex 57 (story 362) | False | "Matt does not invest in the public stock market regularly. Matt likes financial risks." / conclusion: "Matt is not at risk of a gambling addiction and Mike does not both read..." | Conclusion mentions "Mike" but premises are about "Matt" — name inconsistency in annotation | OC |
| D29 | FOLIO train | Ex 36 (story 422) | True | "Lily is in James' family; she watches TV series in cinemas." FOL: "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" | Missing closing parenthesis in FOL formula — syntactic annotation error | OC |
| D30 | FOLIO train | Ex 55 (story 477) | False | "TikTok is a social media application, and it is not ideal for preteens." / conclusion-FOL: "Contain(tikTok, chatFeature) ⊕ ComputerProgram(tikTok))" | Trailing unmatched parenthesis in conclusion-FOL | OC |
| D31 | FOLIO train | Ex 39 (story 243) | False | "If a person can distinguish the taste of different condiments, then they can also use different condiments for cooking...John can make meals which are popular at the party." / conclusion: "John cannot use different condiments for cooking." | 5-premise story; False conclusion derivable via clear chain | IO |
| D32 | FOLIO train | Ex 44 (story 474) | False | "All humans are capable of abstract thoughts. Plants are not capable of abstract thoughts...Hulu is a goat or a human." / conclusion: "If Hulu is either an animal or dirt, then Hulu is capable of abstract thoughts and is dirt." | XOR used in third premise in FOL but not NL; complex conditional conclusion | OC |
| D33 | FOLIO train | Ex 48 (story 92) | True | "Adventures of Rusty is a drama film and children's film. Columbia Pictures produced Adventures of Rusty." / conclusion: "Columbia pictures produced some drama film." | Simple existential conclusion from two-premise story | IO |
| D34 | FOLIO train | Ex 31 (story 60) | True | "All buildings in New Haven are not high...Tower A is managed by Yale Housing." / conclusion: "Tower A is low." (conclusion-FOL: ¬High(tower-a)) | Simple two-step chain; low premise count, close to textbook syllogistic form | IC |
| D35 | FOLIO train | Ex 10 (story 391) | Uncertain | "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" | Unmatched parenthesis in FOL formula — additional annotation error instance | OC |
| D36 | FOLIO train | Ex 46 (story 448) | Uncertain | "Someone is either a seasoned software engineer interviewer at Google, has human rights, or both." / premises-FOL: "∀x ((Seasoned(x) ∧ SoftwareEngineerInterviewer(x) ∧ At(x, google)) ∨ Have(x, humanRights))" | NL says "or both" (inclusive disjunction) but FOL uses ∨ — potential NL-FOL alignment gap | OC |
| D37 | FOLIO train | Ex 5 (story 348) | Uncertain | "All young adults at the event like independence...If Susan is a Yale student, then she does not like independence." / conclusion: "Susan is a college student." | 7-premise story with competing conditional chains; classic indeterminate case | OO |
| D38 | FOLIO train | Ex 8 (story 482) | Uncertain | "Harry, who lives in Potterville either yells or flies. Potter, who lives in Potterville, is a wizard and flies." / conclusion: "Harry is cool." | Fantasy-domain story; multiple conclusions from same story_id test same premises | IO |

---

### Deployment-Relevant Strengths

#### Strength 1: Three-way label schema maps directly onto the deployment rubric for FOL cases
- **Dimension(s):** OO, OC
- **Observation:** Across all 57 sampled examples, the three labels (True, False, Uncertain) appear in clear logical patterns consistent with the formally verified schema: False is assigned when the negation of the conclusion is provably entailed by the premises (not merely when the conclusion fails to follow), and Uncertain is assigned when premises are consistent with both the conclusion and its negation. The False examples in the sample (D11, D12, D13, D29, D38) all involve clear counterexamples entailed by premises, not merely absent entailment, aligning with the deployment's strict "invalid = premises entail negation" definition.
- **Deployment relevance:** The course's most exacting rubric requirement — that "invalid" requires positive entailment of the negation, not just failure to entail — is confirmed as operationally satisfied in the data examined. Annotators and the FOL prover jointly enforce this distinction.
- **Datapoint citations:**
  - [D12] Ex 17 (FOLIO train, label=False): "Michael O'Donnell is a British physician, journalist, author, and broadcaster...Michael O'Donnell was born in Yorkshire as the son of a general practitioner." / conclusion: "There are no journalists that were born in Yorkshire." — False because premises explicitly establish a counterexample (Michael O'Donnell is both a journalist and born in Yorkshire), confirming provable negation entailment rather than mere absence of entailment.
  - [D13] Ex 29 (FOLIO train, label=False): "Grebes are not platypuses and also not echidnas." / conclusion: "Hyraxes lay eggs." — False derivable via clear FOL chain through the exclusive mammal egg-laying premise; provable negation entailment confirmed.
  - [D11] Ex 4 (FOLIO train, label=False): "No trick-shot artist...struggles with half court shots...Jack is on Yale's varsity team, and he is either a trick-shot artist or he successfully shoots a high percentage of 3-pointers." / conclusion: "Jack is bad at mid-range shots." — False because either branch of the disjunction entails the negation.

#### Strength 2: Presence of minimal syllogistic examples close to Hurley-style template forms
- **Dimension(s):** IC
- **Observation:** A subset of examples — especially from the HybLogic pipeline and simpler WikiLogic stories — exhibit the short, template-like premise structures ("No A are B", "All C are B", "Some A is not B") that characterize Hurley-style course-packet problems, with low premise counts (2–3 premises) and clear categorical conclusions.
- **Deployment relevance:** These examples partially bridge the register gap between FOLIO's naturalistic prose and the course's Hurley-style templates. Models tested on FOLIO that perform well on this subset would demonstrate some relevant capability on the deployment's dominant input register.
- **Datapoint citations:**
  - [D1] Ex 1 (FOLIO train, label=True): "No plants are fungi. Mushrooms are fungi." / conclusion: "No plants are mushrooms." — Two-premise syllogism with canonical "No A are B" / "All C are B" structure directly paralleling Hurley examples.
  - [D2] Ex 12 (FOLIO train, label=True): "Some cats are not pets. All cats are mammals." / conclusion: "Some mammals are not pets." — Uses both "Some A is not B" and "All A are B" forms, core Hurley template patterns.
  - [D3] Ex 20 (FOLIO train, label=Uncertain): "All proteins are organic compounds. All enzymes are organic compounds." / conclusion: "All enzymes are proteins." — Classic undistributed-middle fallacy in bare "All A are B" form, highly representative of introductory logic course problems.
  - [D5] Ex 9 (FOLIO train, label=Uncertain): "No television stars are certified public accountants. All certified public accountants have good business sense." / conclusion: "All television stars have good business sense." — "No A are B" / "All B are C" form nearly identical to Hurley syllogism templates.
  - [D4] Ex 50 (FOLIO train, label=Uncertain): "Each building is tall. Everything tall has height." / conclusion: "All buildings are magnificent." — Minimal two-premise story with pedagogically transparent irrelevant-conclusion indeterminate case.

#### Strength 3: FOL operator coverage matches the deployment's second-half logical scope
- **Dimension(s):** IO
- **Observation:** The sampled examples contain all FOL operators the course requires for its second half: universal quantifier (∀), existential quantifier (∃), negation (¬), conjunction (∧), disjunction (∨), implication (→), exclusive disjunction (⊕), and equality (=). Examples span basic universal syllogisms, existential conclusions, chained conditionals, and combinations of quantifiers with connectives.
- **Deployment relevance:** The course's second-half FOL scope is comprehensively covered by the operator set observable in the data. A model scoring well on FOLIO would have been tested on all structural patterns relevant to the predicate-logic half of the course.
- **Datapoint citations:**
  - [D21] Ex 16 (FOLIO train, label=True): "All professional athletes spend most of their time on sports...If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." — Uses ∀, ∃ (via "all"), ¬, →, ∨ in combination across 6 premises.
  - [D8] Ex 3 (FOLIO train, label=Uncertain): "A project is written either in C++ or Python" → FOL uses ⊕ (exclusive disjunction) alongside ∀, ∃, →, ¬ — full operator set in a single story.
  - [D38] Ex 8 (FOLIO train, label=Uncertain): "All wizards in Potterville know magic...Harry, who lives in Potterville either yells or flies." — ∀, →, ¬, ⊕ in a chained multi-step reasoning structure.

#### Strength 4: Indeterminate (Unknown) label cases are clearly defined and pedagogically recognizable
- **Dimension(s):** OO
- **Observation:** The Uncertain/Unknown examples in the sample exhibit clearly recognizable patterns of logical underspecification: premises that are silent on a dimension needed to determine the conclusion (D15, D16, D17, D26), or premises that are consistent with both the conclusion and its negation due to insufficient information (D3, D22, D37). The course rubric's definition of indeterminate — "premises consistent with both the conclusion and its negation" — matches these cases precisely.
- **Deployment relevance:** The Unknown label's formal alignment with the course rubric is confirmed in the data. Students using the tool would receive "indeterminate" classifications on exactly the cases where neither entailment nor contradiction is provable, matching the intended pedagogical behavior.
- **Datapoint citations:**
  - [D17] Ex 23 (FOLIO train, label=Uncertain): "The world's only major large passenger aircraft manufacturers are Boeing and Airbus...Airbus made more revenue than Boeing last year." / conclusion: "There exists a SpaceX commercial aircraft." — Premises are entirely silent on SpaceX; neither conclusion nor its negation follows. Exemplary indeterminate case.
  - [D26] Ex 56 (FOLIO train, label=Uncertain): "Xiufeng, Xiangshan, Diecai, Qixing are districts in the city of Guilin...Yangshuo is not a district in Guilin." / conclusion: "Kowloon District is in Hong Kong." — Conclusion about Hong Kong is logically disconnected from premises about Guilin — paradigmatic indeterminate.
  - [D3] Ex 20 (FOLIO train, label=Uncertain): "All proteins are organic compounds. All enzymes are organic compounds." / conclusion: "All enzymes are proteins." — Undistributed middle; premises consistent with enzymes being or not being proteins.

#### Strength 5: Multi-step reasoning chains test the higher end of the course's FOL difficulty range
- **Dimension(s):** IO
- **Observation:** Many examples require 3–6 chained reasoning steps across multiple premises, with conclusions that can only be reached by tracing through multiple universal rules applied to specific individuals. This covers the deeper end of the reasoning depth distribution that the course's FOL section targets.
- **Deployment relevance:** While some FOLIO examples may be harder than typical course-packet problems, the presence of 3–5 step chains ensures the benchmark is not trivially solvable for the second-half FOL content and provides meaningful signal about model capability at the difficulty level instructors care about.
- **Datapoint citations:**
  - [D21] Ex 16 (FOLIO train, label=True): "All professional athletes spend most of their time on sports. All Olympic gold medal winners are professional athletes. No full-time scientists spend the majority of their time on sports. All Nobel physics laureates are full-time scientists. Amy spends the most time on sports, or Amy is an Olympic gold medal winner. If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." — 6-premise chain requiring case analysis.
  - [D38] Ex 8 (FOLIO train, label=Uncertain): Potterville scenario — 7 premises with chained wizard→magic→fly→cool chain; conclusion requires tracing through 4 steps.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete absence of propositional-logic (quantifier-free) examples
- **Dimension(s):** IO
- **Observation:** Every single example in the 57-item sample contains at least one universal (∀) or existential (∃) quantifier in the premises-FOL field. No quantifier-free example was observed. The YAML gap analysis and web search confirm this is a structural property of FOLIO, not a sampling artifact — the benchmark was designed around FOL predicate structures, and the FOL2NS paper explicitly characterizes quantifiers as the defining feature of FOLIO's logical scope.
- **Deployment relevance:** The course's first half is entirely propositional (connectives, truth tables, modus ponens, modus tollens, hypothetical syllogism, disjunctive syllogism, etc. — no quantifiers). If a model is assessed using FOLIO alone, there is zero coverage of approximately half the course's logical scope. A system that fails on propositional logic but succeeds on FOL would receive a misleadingly favorable evaluation. This is a deployment-critical gap for any tool intended to cover the full course.
- **Datapoint citations:**
  - [D1] Ex 1 (FOLIO train, label=True): "∀x (Plant(x) → ¬Fungi(x)) / ∀x (Mushroom(x) → Fungi(x))" — Even the simplest two-premise example uses universal quantifiers throughout; no quantifier-free propositional version exists in FOLIO.
  - [D4] Ex 50 (FOLIO train, label=Uncertain): "∀x (Building(x) → Tall(x)) / ∀x (Tall(x) → Height(x))" — The two shortest examples in the sample still use ∀; confirming no propositional subset.
  - [D2] Ex 12 (FOLIO train, label=True): "∃x (Cat(x) ∧ ¬Pet(x)) / ∀x (Cat(x) → Mammal(x))" — Minimal example uses both ∃ and ∀; no propositional-only FOLIO examples observed.

---

#### MAJOR

#### MAJOR Concern 1: Register mismatch — dominant FOLIO style is naturalistic prose, not Hurley-style templates
- **Dimension(s):** IC
- **Observation:** The majority of examples in the sample are naturalistic, topic-rich narratives substantially different from the bare template forms of Hurley-style course problems. Examples involve tech companies (D7), film directors (D19), diplomacy (D16), economics with Russia (D14), lipstick product lines (D9), and social media platforms (D23). The register is annotator-composed prose with epistemic qualifiers, complex noun phrases, and embedded real-world knowledge — the opposite of the syntactically constrained "All A are B" / "If P then Q" forms that dominate the course packet. While some simpler examples (D1, D2, D3, D5) approach Hurley register, they are a minority.
- **Deployment relevance:** Model performance on FOLIO's naturalistic prose may not predict performance on the course's dominant templated inputs. A model that successfully classifies "People in this tech company who wear the same flannel shirts every day are consistent" may still fail on "All A are B. Some B are not C. Therefore some A are not C." — and vice versa. Benchmark results may inflate or deflate apparent capability relative to the actual deployment inputs.
- **Datapoint citations:**
  - [D7] Ex 2 (FOLIO train, label=Uncertain): "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises. People in this tech company who wear the same flannel shirts every day are consistent and enjoy sticking to their regular routines." — Naturalistic narrative with embedded relative clauses and real-world scenario; maximally different from Hurley-style bare templates.
  - [D9] Ex 13 (FOLIO train, label=False): "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable...ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." — Branded-product prose with complex noun phrases; requires parsing product line terminology.
  - [D14] Ex 28 (FOLIO train, label=False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency...There is an embargo on Russian foreign trade goods." — Economics domain with contemporary geopolitical content; no structural equivalent in Hurley-style templates.
  - [D25] Ex 34 (FOLIO train, label=True): "All orphan planets are rogue planets...PSO J318.5−22 is a rogue planet." — Astronomy technical nomenclature ("PSO J318.5−22") requiring domain knowledge entirely absent from introductory logic course packets.

#### MAJOR Concern 2: Multiple annotation errors visible in the sampled data
- **Dimension(s):** OC
- **Observation:** The 57-item sample contains at least five distinct annotation errors or quality issues: (1) a free variable `x` in a FOL conditional antecedent (D27, story 376); (2) a name inconsistency between premises ("John") and conclusion ("Jim") (D24, story 337); (3) a name inconsistency between premises ("Matt") and conclusion ("Mike") in the conclusion text (D28, story 362); (4) a missing closing parenthesis in a FOL formula (D29, story 422; D30, story 477; D35, story 391); (5) a potential NL-FOL alignment gap where "either...or both" (inclusive disjunction) in NL is rendered as ∨ rather than explicitly verified (D36, story 448). These occur across different story IDs, suggesting this is not an isolated issue.
- **Deployment relevance:** A 2026 cleaning study cited in the web search found label errors and NL-FOL misalignments in the original FOLIO dataset. The sampled data confirms this concern is real and observable. For a deployment assessing model logic-checking capability, annotation noise in the ground truth directly undermines the validity of benchmark scores — a model might classify a mislabeled example "incorrectly" while reasoning correctly from the NL premises. The original (uncleaned) HuggingFace dataset should be used with caution.
- **Datapoint citations:**
  - [D27] Ex 2 (FOLIO train, story 376, label=Uncertain): FOL premise contains "¬(∃y (flannelShirt(y) ∧ WearEveryday(x, y)) ∧ Have(mike, highEnergy) ∧ Impulsive(mike)) → (Consistent(mike) ∧ StickTo(mike, theirRegularRoutine)) ⊕ ¬Like(mike, surprise)" — `x` is a free variable in the antecedent; this is a syntactic/semantic annotation error in the FOL.
  - [D24] Ex 52 (FOLIO train, story 337, label=True): Premises use "John" throughout; conclusion states "Jim is not a Knicks player." — Name inconsistency suggests a copy-paste or editing error in annotation.
  - [D28] Ex 57 (FOLIO train, story 362, label=False): Conclusion text reads "Matt is not at risk of a gambling addiction and Mike does not both read the Wall Street Journal..." — "Mike" appears in the conclusion while all premises discuss "Matt."
  - [D29] Ex 36 (FOLIO train, story 422, label=True): FOL premises contain "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" — missing closing parenthesis after `jameSFamily`.
  - [D35] Ex 10 (FOLIO train, story 391, label=Uncertain): FOL premises contain "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" — unmatched trailing parenthesis.

#### MAJOR Concern 3: Reasoning depth substantially exceeds typical introductory course-packet complexity
- **Dimension(s):** IO, IC
- **Observation:** Many examples in the sample require 4–7 chained reasoning steps and involve 5–8 premises with complex interactions among universal rules, conditional chains, and disjunctions. The course's introductory context involves 1–3 step arguments drawn from a structured textbook. FOLIO's documented mode reasoning depth is 4 steps with 28.7% requiring 5+, and the data confirms this — numerous examples involve extended chains not representative of introductory course problems.
- **Deployment relevance:** If a model struggles on deep FOLIO examples but would succeed on the 1–3 step problems in the course packet, FOLIO accuracy scores would underestimate actual deployment performance. Conversely, a model that performs adequately on FOLIO may be assessed as adequate when it could still fail on pedagogically simpler but register-distinct Hurley-style problems. The depth distribution mismatch distorts the benchmark's predictive validity for the deployment.
- **Datapoint citations:**
  - [D7] Ex 2 (FOLIO train, label=Uncertain): 7 premises with chained rules about tech company employees; final premise has an XOR embedded in a nested conditional structure — far beyond a first-semester logic student's typical 2–3 premise problem.
  - [D10] Ex 21 (FOLIO train, label=False): "All people who attend Renaissance fairs regularly enjoy dressing up...If Clyde is not focused on futuristic and vocational subjects, then he is neither focused on futuristic and vocational subjects nor enjoys dressing up in old-fashioned and historical period clothing." — 6 premises; convoluted tautological final premise requires 4–5 step reasoning.
  - [D21] Ex 16 (FOLIO train, label=True): 6-premise problem about Amy's professional status requiring complete case analysis across two disjuncts, spanning 4 distinct predicate categories.

#### MAJOR Concern 4: Label field uses "Uncertain" in HuggingFace data vs. "Unknown" in paper documentation
- **Dimension(s):** OO, OF
- **Observation:** The FOLIO paper and all citations consistently use "Unknown" as the third label category. However, in the actual HuggingFace dataset sampled, the third label appears as "Uncertain" (e.g., D3, D5, D15, D16, D22, D37). This is an inconsistency between the paper's documented label schema and the dataset schema in the deployed HuggingFace version. All 57 examples with a non-True/False label use "Uncertain," not "Unknown."
- **Deployment relevance:** For any automated pipeline that relies on the label strings from the HuggingFace dataset for evaluation, using "Unknown" (from the paper) as the target class label would cause a mismatch. This is a practical implementation concern that could invalidate accuracy calculations if not caught. The deployment tool's evaluation code must use "Uncertain" to match the actual data labels.
- **Datapoint citations:**
  - [D3] Ex 20 (FOLIO train, label=Uncertain): "All proteins are organic compounds. All enzymes are organic compounds." / label field value: "Uncertain" — paper documentation calls this "Unknown."
  - [D15] Ex 6 (FOLIO train, label=Uncertain): "Ho is at the business conference and prefers state ownership of the means of production." / conclusion: "Ho is not an ardent communist." — label field: "Uncertain."
  - [D37] Ex 5 (FOLIO train, label=Uncertain): Susan/Yale/Harvard event story — label field: "Uncertain."

---

#### MINOR

#### MINOR Concern 1: Test split not available in the HuggingFace dataset
- **Dimension(s):** OF
- **Observation:** The HuggingFace metadata shows only `train` (1,001 examples) and `validation` (203 examples) splits. The `test` split (226 examples, on which FOLIO's published results and majority baseline of 38.5% are computed) is not accessible in the public HuggingFace dataset. The analysis is based entirely on the training split.
- **Deployment relevance:** Benchmark comparisons to published model performance (GPT-4 64.16%, expert human 95.98%) are based on the test set. Users deploying FOLIO for assessment will need to use the validation set (203 examples) or the training set as a proxy, which may not precisely replicate published distributional statistics. This does not affect content validity observations but limits direct comparison to published baselines.
- **Datapoint citations:** (structural observation; no specific datapoint required)

#### MINOR Concern 2: Topic diversity includes content that may introduce construct-irrelevant domain knowledge requirements
- **Dimension(s):** IC
- **Observation:** Several WikiLogic examples presuppose domain-specific real-world knowledge that is not included in the premises and whose absence could affect whether a naive reader (or model without that knowledge) correctly identifies a classification. The economics-Russia example (D14) presupposes knowledge of what an embargo does; the lipstick example (D9) requires parsing branded product terminology; the astronomy example (D25) involves a technical astronomical designation.
- **Deployment relevance:** The deployment's course-packet problems are designed to be self-contained and domain-neutral, relying only on formal structure and explicitly stated premises. FOLIO's Wikipedia-seeded stories may introduce construct-irrelevant difficulty for models that lack the relevant world knowledge to parse the semantic content of the premises, creating a conflation between logical-reasoning ability and domain knowledge.
- **Datapoint citations:**
  - [D14] Ex 28 (FOLIO train, label=False): "The introduction of an embargo on foreign trade goods in a country leads to a sharp decrease in exports...There is an embargo on Russian foreign trade goods." — The logical chain depends on understanding what an embargo causes, which is given as a premise; however, the contemporary geopolitical context adds semantic load absent from Hurley-style problems.
  - [D25] Ex 34 (FOLIO train, label=True): "PSO J318.5−22 is a rogue planet" — Technical astronomical object name; while the premises are formally stated, the vocabulary creates parsing difficulty for readers unfamiliar with the domain.

#### MINOR Concern 3: Multiple conclusions drawn from a single story may create non-independence between test examples
- **Dimension(s):** IO, OF
- **Observation:** Several story_ids appear multiple times in the sample with different conclusions tested against the same premise set (story 408 appears as Ex 4, Ex 18, Ex 32; story 482 as Ex 8, Ex 19, Ex 30; story 70 as Ex 17, Ex 41; story 474 as Ex 44, Ex 49; story 436 as Ex 14, Ex 42; story 448 as Ex 46, Ex 47). This is by design (the benchmark is split by story, not by conclusion), but it means that per-example accuracy metrics treat correlated items as independent.
- **Deployment relevance:** If a model systematically misrepresents one story's premises, it will fail on all conclusions derived from that story, creating correlated errors that inflate apparent variance in model performance estimates. For deployment purposes, per-story accuracy may be a more informative metric than per-example accuracy, but this is not the primary reported metric.
- **Datapoint citations:**
  - [D11] and [D18] (both story 408): Same 5 premises about Yale varsity team; one tests "Jack is bad at mid-range shots" (False), the other tests a compound conditional conclusion (Uncertain) — shared premise set makes these non-independent.
  - [D38] Ex 8 and Ex 19 and Ex 30 (all story 482): Same Potterville premises tested with three different conclusions ("Harry is cool" / "Harry is not cool" / "Harry is a wizard or angry") — three dependent test items from one story.

---

### Content Coverage Summary

The 57 sampled examples span a wide range of topics: sports (basketball, basketball shooting), technology (software engineering, social media, computer science), biology (mammals, plants, fish), film, astronomy, economics, everyday scenarios (travel planning, family streaming subscriptions), and abstract fictional domains ("Size Town," "Potterville"). Approximately one-third of examples (estimated from the sample) come from short 2–4 premise stories that are structurally close to Hurley-style syllogistic forms; the remaining two-thirds involve 5–8 premise naturalistic narratives with complex logical interactions.

All examples use FOL predicate structures — universal and existential quantifiers are present in every example examined. No quantifier-free propositional example was found. The label distribution in the sample is approximately: True (~25%), False (~28%), Uncertain (~47%) — somewhat more Uncertain-heavy than the documented test set (27% Unknown), though this may reflect training set distribution differences.

The FOL annotations are generally well-formed but the sample reveals at least five distinct annotation errors (free variables, name inconsistencies, parenthesis mismatches) across different story IDs. The label field uses "Uncertain" rather than the paper-documented "Unknown." The register ranges from simple two-premise syllogisms in bare categorical form to complex multi-clause narratives with embedded real-world knowledge, with the naturalistic prose register predominating.

---

### Limitations

1. **Test split inaccessible**: All 57 examples are from the training split. The published performance baselines (GPT-4 64.16%, majority baseline 38.5%) are computed on the test split (226 examples), which is not available in the public HuggingFace repository. The training set may have a different label distribution or difficulty profile.

2. **Sample size**: 57 examples represent ~5.7% of the training set (1,001 examples) and ~4.7% of the combined train+validation set (1,204 examples). Topic and difficulty distributions observed may not fully represent the broader dataset.

3. **FOL annotation quality**: The FOL formulas (premises-FOL, conclusion-FOL fields) were inspected visually but not computationally verified against a theorem prover. The annotation errors noted (free variables, parenthesis mismatches, name inconsistencies) were identified by human inspection; there may be additional errors not visible through manual review of 57 examples.

4. **HybLogic vs. WikiLogic split**: The sample does not identify which pipeline produced each example. Conclusions about register (naturalistic vs. template-like) are inferred from content, not from a verified pipeline tag. The HybLogic subset (which would be most relevant to Hurley-style comparisons) cannot be isolated from this sample.

5. **Readability complexity**: The Dale-Chall readability distribution referenced in the paper (Figure 3) was not inspectable from the HuggingFace data. The claim that FOLIO examples are more complex than Hurley-style templates is inferred from content inspection, not from a computed readability comparison.

6. **Cleaned dataset**: The 2026 cleaning pipeline (using Vampire theorem prover) mentioned in the web search findings is not reflected in the current HuggingFace dataset. The label reliability concerns observed in the sample may be partially addressed by that cleaned version, which was not available for inspection.

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
  "region": "US Undergraduate Introductory Logic Course — Automated Validity Checker",
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
