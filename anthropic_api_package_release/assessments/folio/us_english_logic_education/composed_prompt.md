I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **FOLIO: Natural Language Reasoning with First-Order Logic** is valid for use in **US Undergraduate Logic Students — Introductory and Intermediate Courses**.

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
- **Domain**: Logical reasoning (first-order logic)
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2022

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### 1. Input Ontology
FOLIO defines two primary tasks: (1) natural language reasoning with FOL, requiring
models to determine the truth value of a conclusion given a set of premises [Q15, Q63],
and (2) NL-FOL translation, converting natural language stories into their parallel FOL
representations [Q18, Q67]. The benchmark emphasizes deductive FOL inference as a
capability "that should be sufficiently and independently evaluated" [Q7], explicitly
differentiating itself from benchmarks that conflate logical reasoning with other
reasoning types [Q9]. Within FOL reasoning, the taxonomy covers syllogistic chains
[Q43], multi-premise discourse-level arguments [Q71, Q72], and complex multi-step chains
where 28.7% of examples require five or more reasoning depths [Q60]. The benchmark also
covers a range of model types and prompting strategies — fine-tuning (BERT, RoBERTa [Q84]),
few-shot prompting across LLaMA, GPT-NeoX, GPT-3, GPT-3.5-Turbo, and GPT-4 [Q88], and
advanced prompting methods including chain-of-thought, self-consistency, tree-of-thought
[Q89, Q90], and logic-specialized systems [Q91].

From a deployment-validity standpoint, the task taxonomy aligns with the core deductive
FOL reasoning requirement but presents a moderate coverage gap. FOLIO does not define a
propositional-logic-only reasoning subtask, and while the NL-FOL translation task [Q67]
addresses natural-language-to-formal-form conversion, it operates on stories with fully
explicit, formally structured premises rather than the implicit-premise, natural-English
arguments students encounter [Q14]. Argument reconstruction from everyday or quasi-legal
scenarios — a priority for the deployment — is not documented as a distinct subtask
category. Additionally, FOLIO explicitly excludes temporal and modal logic [Q139, Q140],
which is consistent with the deployment's stated scope but confirms that propositional
logic as a distinct layer is absent.

### 2. Input Content
FOLIO's 1,430 examples originate from two sources: 304 WikiLogic stories seeded by
random Wikipedia pages [Q34, Q58], yielding topical diversity (74% of total vocabulary
from 63% of stories [Q62]), and 183 HybLogic stories derived from combinations of the
24 valid syllogism types augmented with real-world entity assignments [Q42, Q44, Q58]).
The dual-source design was deliberate — to obtain "examples that are both logically
diverse and complex and have abundant abstract syntax tree (AST) variations" [Q33].
WikiLogic stories are created from scratch without templates [Q35], drawing on real-world
knowledge to cover a wide range of everyday topics [Q38].

However, all FOLIO instances are written with fully explicit, formalized premises, and
commonsense knowledge required for inference was explicitly added as auxiliary premises
during annotation [Q55]. This design choice maximizes formal rigor but diverges from the
implicit-premise style of the everyday and quasi-legal arguments students are trained to
reconstruct. The Wikipedia seed approach raises a potential data-contamination concern
for LLM evaluation [Q104], and fine-tuning experiments show inverse performance patterns
between the two pipelines [Q105], suggesting that instance-level content characteristics
interact substantially with model architecture. The dataset contains 4,351 distinct words
[Q62] and a documented readability distribution [Q59, Q154], providing some grounding for
assessing linguistic accessibility. Stories containing opinionated language or
identity-linked biases were removed [Q127], and factually inaccurate claims were rewritten
[Q126], supporting neutrality but reducing coverage of the contested-claim scenarios
students may encounter in real arguments.

### 3. Input Form
FOLIO is a text-only, English-language dataset [Q22] using FOL notation consistent with
the standard adopted in the AI community (Russell & Norvig, 2010) [Q52]. Each story
consists of NL premises and conclusions paired with parallel FOL annotations [Q64, Q65],
and the NL layer was carefully naturalized: all sentences were checked with Grammarly
[Q49], reviewed for naturalness by English Literature annotators [Q50], and disambiguated
using explicit conventions for disjunction [Q130, Q131], quantifier phrasing [Q132, Q133],
and singular/plural usage [Q134]. The dataset is split 70%/15%/15% by story [Q78, Q79]
to ensure unseen-story evaluation.

For the deployment, the input-form dimension presents no substantial mismatch: both FOLIO
and the target system are text-only, English-language, and operate in a high-resource
written register. The one formal-register tension is that FOLIO uses the Russell & Norvig
FOL syntax convention, which the benchmark's own inference engine does not natively
support and required a custom Python parser to bridge [Q149, Q150] — a symptom of the
distance between FOLIO's notation and the Fitch-style natural deduction syntax used in
the Barwise & Etchemendy curriculum. This is, however, a notation mismatch rather than
a modality or language mismatch, and it falls within the input-form dimension only
insofar as it affects the encoding of formal input strings.

### 4. Output Ontology
The ground-truth label set is a three-way classification — **True**, **False**, or
**Unknown** — determined by a FOL inference engine [Q36, Q66]. The majority class (True)
comprises 87 of 226 test examples, yielding a 38.5% majority baseline [Q94]. The FOL
representational layer is motivated by its freedom from natural language ambiguity [Q137]
and its capacity to serve as input to a theorem prover for exact truth-value derivation
[Q136]. The operator inventory covers negation, conjunction, disjunction, implication,
universal and existential quantifiers, and equality [Q138], with n-place predicates used
for expressivity [Q141]. Temporal and modal logic are explicitly excluded [Q139, Q140],
and Davidsonian semantics are not used [Q142].

For the deployment, this output ontology is fundamentally misaligned (HIGH priority).
The deployment's required output is not a truth-value label but a structured, rule-
justified proof trace differentiated by student register — numbered deduction steps
citing specific premises, naming inference rules (e.g., modus ponens), and paired with
plain-English summaries. For invalid arguments, the deployment expects a countermodel or
counterexample; FOLIO labels these as False or Unknown but generates no countermodel
artifact [Q66]. FOLIO also provides no output schema for pedagogical explanation
structure, register differentiation, or alternative valid reasoning paths. The scoring
function cannot evaluate whether an explanation is Fitch-style compliant, premise-citing,
or appropriately leveled for introductory versus advanced students. Expert human
performance (95.98%) versus non-expert performance (61.82%) [Q111] confirms that FOL
domain knowledge is a prerequisite [Q112], but the benchmark's output taxonomy captures
none of the explanation-quality or countermodel-construction criteria the deployment
requires.

### 5. Output Content
FOLIO's ground-truth labels are generated and verified by a FOL inference engine [Q2],
providing a formal, deterministic correctness criterion for deductive validity. The
annotation pipeline is staged — NL quality control by NLP/computational-linguistics
experts and FOL quality control exclusively by FOL experts [Q29, Q124, Q125] — and all
stories were reviewed by senior researchers and CS students [Q31]. The annotation
protocol was designed to ensure semantic consistency: FOL formulas must preserve the
semantics and structure of the NL source [Q144, Q145], semantic decomposition is
minimized [Q146], and tense is abstracted away [Q147]. A preliminary investigation
identified systematic FOL consistency issues in human-written formulas, prompting an
additional quality control round [Q53, Q54], and 39.2% of stories required rewriting
to address quality issues [Q48]. Commonsense premises required for FOL proofs but
implicit in NL were explicitly added [Q55].

The benchmark documents no ground-truth schema for what constitutes a pedagogically
acceptable explanation or a valid countermodel — because no such output is elicited
from annotators. Annotator demographics are described at a high level: college or
graduate students, native or near-native English speakers, with formal FOL coursework
[Q27, Q28, Q122, Q123] — but no detailed demographic breakdown is provided. The
expert/non-expert performance gap (34.16 percentage points [Q111]) and the finding
that GPT-4 still lags expert annotators by 31.82 points [Q113] establish the reliability
of the engine-verified labels for deductive correctness. However, no label content exists
for the explanation quality, register appropriateness, or countermodel correctness
dimensions that the deployment's output content requires, creating a fundamental gap for
this dimension.

### 6. Output Form
For the primary reasoning task, accuracy against the engine-verified three-way label is
the sole metric [Q80]. For NL-FOL translation, two metrics are used: Syntactic Validity
(SynV), a binary score checking whether all FOL formulas in a story pass syntactic
checking [Q73, Q74], and Execution Accuracy (ExcAcc), measuring whether the translated
FOL story yields correct truth values when fed to the inference engine [Q75, Q76]. Results
are averaged over five randomly sampled training-set example sets [Q93]. The evaluation
infrastructure relies on a Stanford CS221 inference engine [Q148] accessed via a custom
Python FOL parser [Q150, Q151, Q153] because the engine does not natively support the
dataset's FOL syntax [Q149]. Key empirical findings include: GPT-3.5-Turbo and GPT-4
achieve ~93% syntactic validity on translation [Q96] but low execution accuracy [Q97];
models perform substantially worse at reasoning depths 4–7 than 0–3 [Q99]; and confusion
matrices show systematic over-prediction of True [Q155, Q156, Q157]. The authors
themselves acknowledge the need for a more reliable NL-FOL translation metric [Q77].

For the deployment, the output form is fundamentally misaligned (HIGH priority). The
benchmark's accuracy metric evaluates label prediction; the deployment requires
evaluation of multi-step proof traces, premise-citation correctness, inference-rule
naming, and register appropriateness (introductory vs. advanced). No metric in FOLIO
assesses whether a reasoning trace is pedagogically clear, Fitch-style compliant, or
appropriately differentiated by student level. The evaluation infrastructure (custom FOL
parser + inference engine) is purpose-built for label verification rather than
explanation-quality assessment, and the reliance on LLMs for any conversion step is
flagged as unreliable [Q152]. The output-form mismatch is thus complete: FOLIO produces
and evaluates single labels; the deployment requires and must evaluate structured,
register-differentiated, rule-justified proof artifacts and countermodels.


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
| Q50 | 4 | output_content | "Our annotators who have graduated from or are senior students studying English Literature conducted a thorough round of review for grammatical correctness and language naturalness." |
| Q51 | 4 | input_form | "We also eliminate natural language ambiguity when it is possible." |
| Q52 | 5 | input_form | "We adopt the FOL definitions and syntax most widely used in the AI community (Russell and Norvig, 2010)." |
| Q53 | 5 | output_content | "In preliminary investigations, we found that the human-written FOL formulas suffer from FOL consistency issues, which necessitates an additional round of quality control for FOL formulas." |
| Q54 | 5 | output_content | "One NL sentence can be translated into FOL through multiple non-equivalent ways. For example, sometimes additional information inferred from a sentence can be represented in FOL, leading to multiple representations. We therefore design an annotation protocol for FOL translation in order to ensure that our FOL translations are as consistent as possible across all examples in our dataset." |
| Q55 | 5 | input_content | "Apart from checking whether NL and FOL express equivalent meanings, we also add necessary commonsense knowledge in both the NL and FOL premises. Sometimes humans do not write certain commonsense knowledge in the premises that is required in the FOL reasoning process, which is based solely on the premises given. We add such knowledge as additional premises at this stage." |
| Q56 | 5 | input_form | "In particular, intrinsic properties of some predicates are required in the FOL reasoning process. For example, "LocatedIn(x,y)" should be transitive and "BeFamily(x,y)" should be symmetric." |
| Q57 | 5 | output_content | "Recognizing that the FOL formula annotations can be error-prone, we verify the syntactic validity and label consistency of FOL formula annotations with an FOL inference engine." |
| Q58 | 5 | input_content | "Table 3 shows that examples based on Wikipedia make up the largest portion of FOLIO, with 304 stories, 1,353 NL and FOL premise pairs, and 753 NL and FOL conclusion pairs. Hybrid annotations consist of 183 stories with 1,054 NL and FOL premise pairs, and 682 NL and FOL conclusion pairs in total." |
| Q59 | 5 | input_form | "We use the Dale-Chall Readability Formula (Dale and Chall, 1948, 1995) to show the text complexity of FOLIO following (Singh et al., 2023; Arps et al., 2022; Wei et al., 2021)." |
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
| Q85 | 7 | input_form | "We fine-tune the base and large versions of both BERT and RoBERTa, with an additional two-layer classification layer to predict the truth values." |
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
| Q114 | 9 | output_content | "We focus on collecting a very high-quality dataset in evaluating logical reasoning rather than merely a large dataset." |
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
| Q161 | 15 | input_form | "FOL formulas have a clearer and more straightforward logical structure than NL sentences." |
| Q162 | 15 | output_form | "As shown in Table 11, the performance slightly increases in the NL+FOL setting for GPT-4 while GPT-3.5 performs worse in both the NL+FOL and the FOL-only settings." |
| Q163 | 15 | output_form | "FOL always serves as additional useful information for GPT-4, but not for GPT-3.5 regardless of whether FOL is concatenated with NL." |

---

## Regional Context

```yaml
name: US Undergraduate Logic Students — Introductory and Intermediate Courses
abbreviation: us_undergrad_logic
assessment_context:
  benchmark: FOLIO
  deployment_description: An LLM-powered educational tool on a US platform that (1)
    determines the validity of logical arguments, (2) produces step-by-step, rule-justified
    proof traces in Fitch-style natural deduction notation, and (3) differentiates
    explanations by student register (introductory vs. advanced). The tool also handles
    natural-language-to-formal-logic translation and generates countermodels for invalid
    arguments.
  population_description: English-speaking undergraduate students enrolled in introductory
    and intermediate logic courses at US higher-education institutions. Curriculum
    is anchored to widely used US textbooks, primarily Barwise & Etchemendy's Language,
    Proof and Logic, with pedagogy centered on Fitch-style natural deduction. No sub-national
    geographic differentiation is specified.
geography:
  country: United States
  sub_national_scope: None specified — deployment is national across US higher-education
    institutions offering introductory and intermediate logic courses.
  institutional_context: US colleges and universities; courses typically housed in
    philosophy departments, mathematics departments, and computer science departments
    depending on institutional structure.
languages:
  primary:
  - English
  variants:
  - Standard American Academic English
  formal_notation_registers:
  - Fitch-style natural deduction (Barwise & Etchemendy syntax)
  - Standard FOL notation (Russell & Norvig convention, used in FOLIO)
  - Informal natural-language argumentation (everyday and quasi-legal registers)
  note: 'No multilingual or translation concerns. The critical register distinction
    is not linguistic but formal-notational: FOLIO uses Russell & Norvig FOL syntax,
    which differs from the Fitch-style notation students are taught. This notation
    mismatch is a deployment-salient concern even within English.'
writing_systems:
  scripts:
  - Latin alphabet
  - Standard logical notation symbols (¬, ∧, ∨, →, ↔, ∀, ∃, =)
  fitch_specific_symbols:
  - Vertical bar / subproof box notation
  - Inference rule abbreviations (MP, MT, DN, ∧I, ∧E, ∨I, ∨E, →I, →E, ¬I, ¬E, ∀I,
    ∀E, ∃I, ∃E)
  note: All content is Latin-script English. The deployment-salient concern is that
    Fitch-style proof notation uses structural conventions (subproof boxes, line-numbered
    deductions, rule citations) not present in FOLIO's flat FOL annotation format.
target_population_profile:
  education_level: Undergraduate (first and second year most common for introductory;
    second through fourth year for intermediate/advanced)
  prior_logic_exposure:
    introductory_register: Little to no prior formal logic training; students reason
      informally and require heavy natural-language scaffolding with minimal symbolic
      notation.
    advanced_register: Completed at least one semester of formal logic; comfortable
      with quantifiers, predicates, and named inference rules; expect formal annotations
      alongside prose.
  course_types:
  - Introductory symbolic logic (philosophy departments)
  - Discrete mathematics / proof-writing (mathematics and CS departments)
  - Intermediate logic / formal methods
  primary_textbook_anchor: 'Barwise & Etchemendy, Language, Proof and Logic (LPL);
    the LPL package includes the Fitch proof environment (a natural deduction proof
    checker), the Boole truth-table tool, and Tarski''s World, and is described as
    appropriate for logic courses across philosophy, mathematics, and CS departments
    from first logic courses to first graduate courses. Secondary references may include
    Hurley''s A Concise Introduction to Logic, Bergmann/Moor/Nelson The Logic Book,
    and the open-access forall x (Calgary Remix) which also uses a Fitch-style system
    compatible with LPL. Source: CSLI/UCP publisher description — [WEB-1];
    OpenLogicProject fitch-checker README — [WEB-2]'
  argument_types_encountered:
  - Propositional logic arguments (sentential logic with connectives only)
  - Predicate/FOL arguments (quantifiers, predicates, identity)
  - Natural-language arguments with implicit premises requiring reconstruction
  - Everyday scenario arguments (quasi-legal, ethical, practical)
  - Multi-step deduction chains from course exercises and textbook problems
  out_of_scope_argument_types:
  - Modal logic
  - Temporal logic
  - Inductive reasoning
  - Fallacy identification (planned as separate module)
curriculum_and_pedagogy:
  proof_system: Fitch-style natural deduction
  proof_system_description: Proofs are presented as numbered lines in a structured
    box format. Each line is either a premise, an assumption (opening a subproof),
    or a derived conclusion with an explicit rule citation and the line numbers of
    the premises or lines the rule was applied to. Subproofs are used for conditional
    introduction, negation introduction, and universal introduction.
  canonical_inference_rules:
  - Modus Ponens (→E)
  - Modus Tollens (MT)
  - Conditional Introduction (→I)
  - Conjunction Introduction (∧I) and Elimination (∧E)
  - Disjunction Introduction (∨I) and Elimination (∨E)
  - Negation Introduction (¬I) and Elimination (¬E) / Double Negation (DN)
  - Universal Introduction (∀I) and Elimination (∀E)
  - Existential Introduction (∃I) and Elimination (∃E)
  - Biconditional Introduction (↔I) and Elimination (↔E)
  countermodel_expectation: For invalid arguments, students are expected to produce
    a countermodel (an interpretation that makes all premises true and the conclusion
    false) rather than a failed or incomplete proof.
  register_differentiation:
    introductory: Numbered steps with plain-English descriptions of each logical move;
      minimal symbolic notation; connective names spelled out (e.g., 'and', 'if…then');
      step-by-step prose summaries dominate.
    advanced: Numbered steps with formal rule names and citations in Fitch notation;
      quantifiers and predicates rendered symbolically; prose summaries condensed
      or optional; countermodels expressed as explicit domain assignments.
  textbook_notation_vs_folio_notation: 'FOLIO uses the Russell & Norvig (2010) FOL
    syntax convention, which differs from the Barwise & Etchemendy Fitch-style syntax
    students are taught. A community-maintained LaTeX package (lplfitch) exists specifically
    to typeset proofs in the LPL Fitch format, confirming the distinctiveness of this
    notation from other natural deduction styles (Jaśkowski, Kalish-Montague, Gamut).
    No documented systematic mapping between FOLIO''s FOL operators and LPL Fitch
    rule names was found. Source: OpenLogicProject — [WEB-3];
    logicmatters.net — [WEB-4]'
infrastructure_and_access:
  delivery_context: US higher-education platform; web-based LLM tool accessed via
    browser on campus or at home.
  device_access: 'Majority laptop/desktop primary for coursework: EDUCAUSE and community-college
    survey data (2020–2022) indicate approximately 66–72% of undergraduates primarily
    use laptops or desktops for course access, while ~20% rely primarily on mobile/cellular
    devices. Four out of five students reported connecting both a smartphone and a
    laptop to campus Wi-Fi daily, indicating dual-device ownership is typical. The
    formal-notation input requirements of a Fitch-style tool strongly favor keyboard/desktop
    access; mobile use for symbolic input is likely a secondary or edge case. Source:
    New America / EDUCAUSE community-college survey (Dec 2022) — [WEB-5];
    EDUCAUSE 2023 mobile learning report — [WEB-6]'
  connectivity: 'A majority of undergraduates (77–88% across institution types) report
    having high-speed internet at home, but connectivity quality is uneven: a 2022
    national EDUCAUSE survey found roughly 64% of undergraduates experienced unstable
    internet connections, and roughly half of community-college students with broadband
    described internet access as a high financial burden. Low-income and community-college
    students face disproportionate connectivity gaps, relevant for any deployment
    targeting diverse institution types. Source: New America / EDUCAUSE community-college
    survey — [WEB-5]'
  accessibility_considerations: 'Screen-reader compatibility for formal notation (MathML
    or equivalent) may be relevant for students with disabilities. [NEEDS VERIFICATION
    — deferred: below search budget; platform-specific accessibility commitments require
    vendor documentation not retrievable via web search]'
  platform_modality: Text-only; structured proof output with numbered lines and formal
    symbols; no audio or image modality required.
  nlp_tooling: High-resource English NLP ecosystem; strong model availability for
    English formal reasoning tasks.
cultural_and_institutional_norms:
  academic_integrity: US higher-education academic integrity policies are directly
    relevant — the tool must be designed so it supports learning rather than answer-copying;
    proof traces should be pedagogically scaffolded to encourage student reasoning,
    not replace it.
  disciplinary_variation: Logic is taught across philosophy, mathematics, and CS departments
    with different notational conventions and emphases (philosophers favor Fitch natural
    deduction; mathematicians may use sequent calculus or informal proof; CS may use
    resolution or tableau methods). The deployment is specifically anchored to the
    philosophy/LPL tradition.
  student_diversity: '[NEEDS VERIFICATION — deferred: below search budget; undergraduate
    logic enrollment demographics by institution type and department are not aggregated
    in a form retrievable via web search; community college vs. four-year university
    differences in prior preparation would require IPEDS or NSF survey analysis]'
  pedagogical_expectations: US undergraduate logic pedagogy emphasizes showing work
    explicitly — partial credit for correct reasoning steps is standard. The tool's
    step-by-step trace requirement directly reflects this norm.
  sensitivity_considerations: Argument content drawn from everyday and quasi-legal
    scenarios may touch on politically or ethically sensitive topics (e.g., legal
    reasoning examples involving rights, liability). Content neutrality consistent
    with FOLIO's own bias-removal protocol is appropriate.
benchmark_alignment_notes:
  primary_coverage_strengths:
  - FOLIO's FOL deductive reasoning coverage maps to the advanced register of the
    deployment's predicate logic requirements.
  - FOLIO's NL-FOL translation task partially covers the deployment's natural-language-to-formal-form
    translation need.
  - Engine-verified correctness labels provide reliable ground truth for the deductive
    validity component.
  - FOLIO's reasoning-depth stratification (modes at 4 steps; 28.7% requiring 5+)
    maps loosely to the introductory/advanced difficulty distinction.
  primary_coverage_gaps:
  - gap: Output form mismatch — proof traces vs. classification labels
    priority: HIGH
    description: FOLIO outputs a three-way truth-value label (True/False/Unknown).
      The deployment requires numbered, rule-justified Fitch-style proof traces with
      premise citations, differentiated by student register. No FOLIO metric evaluates
      explanation quality, pedagogical clarity, or register appropriateness.
    web_search_target: Logic reasoning benchmark step-by-step proof trace evaluation
      pedagogical explanation NaturalProofs ProofWriter Fitch natural deduction rubric
    search_findings: 'NaturalProofs (NeurIPS 2021) and NaturalProver (NeurIPS 2022)
      benchmark neural proof generation on mathematical theorems but operate over
      informal mathematical language (LaTeX/ProofWiki), not Fitch-style symbolic logic,
      and evaluate via reference retrieval and human ratings from university-level
      math students rather than rule-citation rubrics. ProofWriter (ACL Findings 2021)
      generates natural-language proof chains over synthetic RuleTaker-style data
      and evaluates proof correctness (answer+proof accuracy), but its proof format
      is flat natural-language chain, not Fitch-style numbered deductions with rule
      names; FOLIO itself does not include reasoning chains. The directly relevant
      finding is P-FOLIO (EMNLP Findings 2024), a companion dataset to FOLIO containing
      human-written, step-by-step natural-language reasoning chains for FOLIO stories,
      with reasoning steps spanning 0–20 and single-step inference-rule classification.
      P-FOLIO is the closest existing resource to what the deployment requires, but
      its proof format is natural-language narrative, not Fitch-style formal notation
      with rule abbreviations. A 2025 study (arXiv 2505.04736) directly evaluates
      LLMs on stepwise propositional logic proof construction for an ITS, finding
      DeepSeek-V3 achieves ~84–87% stepwise accuracy on propositional problems but
      LLM hints score only 75% accurate and underperform on contextual explanation.
      No benchmark with Fitch-style rule-citation rubrics for undergraduate logic
      courses was found. Sources: P-FOLIO — [WEB-7];
      NaturalProver — [WEB-8]; LLM ITS proof
      study — [WEB-9]'
  - gap: Countermodel generation
    priority: HIGH
    description: FOLIO labels invalid arguments False or Unknown but does not construct
      or evaluate countermodels. The deployment requires explicit countermodel artifacts
      for all invalid arguments.
    web_search_target: Countermodel generation benchmark FOL propositional logic counterexample
      evaluation NLP educational
    search_findings: 'No benchmark specifically eliciting and evaluating formal countermodel
      construction (domain + assignment pairs) for FOL or propositional logic as a
      first-class output was found in NLP/educational AI literature. A 2026 preprint
      (arXiv 2603.19514, ''Learning to Disprove'') introduces formal counterexample
      generation using Lean 4 verification, noting that CounterMath (Li et al. 2025)
      is the sole dataset curated for benchmarking counterexample generation, comprising
      only 1,216 natural-language problems — scope is mathematical theorem disproving
      in Lean, not FOL/propositional logic pedagogical countermodels. This gap is
      confirmed as a research frontier: no existing benchmark covers the deployment''s
      specific countermodel artifact requirement. Sources: arXiv 2603.19514 — [WEB-10]'
  - gap: Propositional logic coverage
    priority: HIGH
    description: FOLIO is exclusively FOL-scoped. The deployment explicitly requires
      propositional/sentential logic handling as a distinct layer. No FOLIO subtask
      covers propositional-only reasoning.
    web_search_target: Propositional sentential logic reasoning benchmark LLM evaluation
      LogiQA bAbI RuleTaker introductory undergraduate logic
    search_findings: 'Several benchmarks cover propositional or restricted FOL reasoning:
      RuleTaker (Clark et al. 2020/2021) and ProofWriter (Tafjord et al. 2021) include
      propositional-level chaining but use synthetic templates with limited vocabulary
      and at most ~50 distinct ASTs, making them thin on natural-language variety.
      LogiQA and ReClor cover multiple-choice logical reasoning but entangle formal
      inference with world knowledge. A new 2025 benchmark, Rosetta-PL (arXiv 2505.00001),
      is specifically designed to evaluate LLM propositional logic reasoning and generalization
      in a controlled environment by translating Lean propositions into a custom formal
      language. DivLogicEval (arXiv 2509.15587) samples classical logic expressions
      verifiable by a symbolic solver and transforms them to NL, targeting propositional
      logic reasoning more purely than LogiQA/ReClor. None of these cover Fitch-style
      proof traces. P-FOLIO (see above) adds proof chains to FOLIO''s FOL stories
      but does not add a propositional-only layer. The search confirms that no single
      benchmark covers both propositional and FOL logic with Fitch-style proof traces.
      Sources: Rosetta-PL — [WEB-11]; DivLogicEval — [WEB-12];
      ProofWriter ACL — [WEB-13]'
  - gap: Fitch-style notation vs. FOLIO FOL syntax
    priority: HIGH
    description: FOLIO uses Russell & Norvig FOL syntax, which its own inference engine
      does not natively support and which differs from the Barwise & Etchemendy Fitch-style
      notation the curriculum requires. Inference rule names, subproof structure,
      and formula syntax are all misaligned.
    web_search_target: Fitch natural deduction Barwise Etchemendy LPL LLM evaluation
      formal proof benchmark notation compatibility
    search_findings: 'No published LLM benchmark or evaluation framework specifically
      targeting Fitch-style natural deduction in the LPL (Barwise & Etchemendy) notation
      was found. Existing community tools include: (1) an open-source Fitch proof
      checker (el-sambal/fitch-proof on GitHub) that verifies LPL-style Fitch proofs,
      and (2) the lplfitch LaTeX package for typesetting LPL-style proofs, maintained
      by Richard Zach (University of Calgary) and the OpenLogicProject. These confirm
      the distinctiveness and community investment in LPL Fitch notation but are proof-verification
      utilities, not NLP benchmarks. The forall x: Calgary Remix uses a compatible
      Fitch system and has an associated proof checker, widening the practical ecosystem
      but not the benchmark coverage. No systematic mapping between FOLIO''s Russell
      & Norvig FOL operators and LPL Fitch rule names (e.g., →E vs. MP, ¬I vs. RAA)
      was found in published form. The notation gap is real and unaddressed in the
      NLP/LLM evaluation literature. Sources: el-sambal/fitch-proof — [WEB-14];
      OpenLogicProject fitch — [WEB-3]; logicmatters.net
      — [WEB-4]'
  - gap: Implicit-premise argument reconstruction
    priority: MODERATE
    description: FOLIO premises are fully explicit and formalized; implicit commonsense
      premises were added by annotators. The deployment requires handling everyday
      arguments where premises are left unstated and must be reconstructed — a distinct
      task not covered in FOLIO.
    web_search_target: Implicit premise argument reconstruction enthymeme NLP benchmark
      informal reasoning formalization dataset
    search_findings: '[NEEDS VERIFICATION — deferred: below search budget; this gap
      is confirmed from the FOLIO documentation analysis (annotators explicitly added
      commonsense premises to make all reasoning fully explicit) and does not require
      additional search to score. Enthymeme/implicit-premise NLP benchmarks are a
      known sparse area; no high-impact new finding was expected from the remaining
      budget.]'
  - gap: Register-differentiated explanation generation
    priority: MODERATE
    description: FOLIO has no output schema or metric for generating or evaluating
      register-appropriate explanations (introductory plain-language vs. advanced
      formal annotation). The expert/non-expert accuracy gap documents difficulty
      stratification but not explanation register.
    web_search_target: Register-differentiated logic explanation introductory advanced
      student LLM pedagogical output benchmark difficulty stratification undergraduate
    search_findings: 'No benchmark with explicit introductory-vs-advanced register
      differentiation for logic explanation output was found. The 2025 ITS study (arXiv
      2505.04736) evaluates LLM hints on 4 criteria (consistency, clarity, contextual
      explanation, and pedagogical appropriateness) for propositional logic ITS problems,
      finding that LLMs score 75% accurate on hints but underperform on explaining
      why a hint was provided — the closest evidence of a pedagogical-register evaluation
      gap in the literature. P-FOLIO uses pass@k metrics over multiple sampled reasoning
      chains but does not differentiate by student register. The gap is confirmed
      as unaddressed. Source: arXiv 2505.04736 — [WEB-9]'
  - gap: Pedagogical explanation quality metric
    priority: HIGH
    description: No existing FOLIO metric evaluates whether a reasoning trace is pedagogically
      clear, correctly cites premises, or uses appropriate rule names. A rubric or
      reference-trace evaluation framework is needed and absent from the benchmark.
    web_search_target: Pedagogical explanation quality rubric logic proof trace evaluation
      NLP benchmark educational AI step-by-step reasoning
    search_findings: 'P-FOLIO (EMNLP Findings 2024) introduces human-written natural-language
      proof chains for FOLIO stories and evaluates single-step inference-rule classification
      with pass@k metrics — this is the most pedagogically motivated evaluation extension
      of FOLIO to date. However, P-FOLIO uses narrative NL chains, not Fitch-style
      rule-cited proofs, and does not define a rubric for pedagogical clarity, premise-citation
      correctness, or register appropriateness. The 2025 ITS study (arXiv 2505.04736)
      is the first to evaluate LLM stepwise proof construction for propositional logic
      in an actual educational ITS context, using both LLM-grader and human expert
      ratings — but only for propositional logic (not FOL) and not in Fitch notation.
      NaturalProver (NeurIPS 2022) uses human evaluation from university-level math
      students for next-step suggestions, rated correct and useful >40% of the time,
      but for informal mathematical language, not Fitch notation. In summary: no rubric
      or reference-trace evaluation framework exists for Fitch-style undergraduate
      logic proof quality. Sources: P-FOLIO — [WEB-7];
      arXiv 2505.04736 — [WEB-9]; NaturalProver — [WEB-15]'
flagged_verification_items:
- item: US undergraduate enrollment in logic-relevant courses (philosophy logic, discrete
    math, CS formal methods)
  notes: '[NEEDS VERIFICATION — deferred: below search budget; course enrollment figures
    by department type require IPEDS or NSF SESTAT microdata analysis not retrievable
    via web search]'
- item: Prevalence of Barwise & Etchemendy LPL as primary textbook vs. competing texts
  notes: 'Partially resolved. LPL (2nd edition, CSLI/UCP) is described by its publisher
    as appropriate for logic courses across philosophy, mathematics, and CS from first
    undergraduate to first graduate courses, and has a MOOC launched in 2014. The
    forall x: Calgary Remix (open-access, P. D. Magnus / R. Zach) uses a compatible
    Fitch system and is widely used at institutions preferring open textbooks. Hurley''s
    A Concise Introduction to Logic remains dominant in introductory philosophy courses
    that emphasize informal logic and syllogistics over symbolic proof. Quantitative
    adoption-rate data is not available via web search. [NEEDS VERIFICATION — deferred:
    adoption rates require publisher sales data or course-adoption surveys] Sources:
    CSLI/UCP — [WEB-1];
    Wikipedia LPL — [WEB-16]'
- item: Availability of existing LLM-powered logic tutoring tools in US higher education
  notes: 'Partially resolved. The competitive landscape includes: (1) Carnap.io (open-source
    web-based Fitch and other proof systems used in logic courses), (2) the LPL/Fitch
    software bundled with Barwise & Etchemendy, (3) el-sambal/fitch-proof (open-source
    LPL-compatible online Fitch checker, [WEB-17]), and
    (4) emerging LLM-based ITS research. A 2025 peer-reviewed study (Computers & Education:
    AI, arXiv 2505.04736) directly evaluates LLMs as hint generators for a propositional
    logic ITS operating on student problem-solving states, finding 75% hint accuracy
    with limitations in contextual explanation — the first published evaluation of
    LLMs in this specific pedagogical role. No commercially deployed LLM-native Fitch-style
    logic tutor was identified in the literature as of May 2025. Sources: arXiv 2505.04736
    / ScienceDirect — [WEB-18];
    fitch-proof GitHub — [WEB-14]'
- item: NaturalProofs, ProofWriter, or other benchmark coverage of step-by-step natural
    deduction evaluation
  notes: 'Resolved. NaturalProofs (NeurIPS 2021) benchmarks mathematical reference
    retrieval and proof generation for informal mathematical language (ProofWiki);
    it does not cover Fitch-style symbolic logic. ProofWriter (ACL Findings 2021)
    generates and evaluates flat natural-language proof chains over synthetic RuleTaker
    data, with answer+proof accuracy metrics — but in natural language, not Fitch
    notation, and on synthetic rather than realistic stories. P-FOLIO (EMNLP Findings
    2024) is the most directly relevant resource: a human-annotated companion to FOLIO
    with step-by-step NL reasoning chains (0–20 steps), inference-rule classification,
    and pass@k evaluation, built on FOLIO''s realistic stories. None of these benchmarks
    include Fitch-style rule-citation rubrics. Sources: P-FOLIO — [WEB-7];
    arXiv P-FOLIO — [WEB-19]; NaturalProofs GitHub — [WEB-20];
    ProofWriter ACL — [WEB-13]'
- item: Existing propositional logic benchmarks suitable as FOLIO complements
  notes: 'Resolved. Strong candidates identified: (1) ProofWriter / RuleTaker (Clark
    et al. 2020–2021): propositional-level chaining with proof traces, but synthetic
    with limited vocabulary/AST diversity. (2) Rosetta-PL (arXiv 2505.00001, 2025):
    purpose-built propositional logic benchmark for LLM evaluation in a controlled
    environment using Lean-translated propositions. (3) DivLogicEval (arXiv 2509.15587,
    2025): samples classical logic expressions verified by symbolic solver, transforms
    to NL, focuses on propositional reasoning more purely than LogiQA. (4) LogiQA
    / ReClor: multiple-choice, but entangle world knowledge with formal inference.
    None of these cover Fitch-style proof traces; they are best used as FOLIO complements
    for propositional coverage only. Sources: Rosetta-PL — [WEB-11];
    DivLogicEval — [WEB-12]'
- item: Counterexample generation benchmarks for FOL and propositional logic
  notes: 'Resolved (null result). No benchmark specifically designed to elicit and
    evaluate formal countermodel construction (interpretation + domain assignment)
    for FOL or propositional logic as a first-class output was found. CounterMath
    (Li et al. 2025) is the sole dataset curated for counterexample generation benchmarking,
    but covers mathematical theorem disproving in Lean 4, not logic-course-style countermodels.
    The 2026 preprint ''Learning to Disprove'' (arXiv 2603.19514) introduces a training
    framework for formal counterexample generation using Lean 4 verification with
    three newly collected benchmarks, but these target graduate-level mathematical
    theorems. This is a confirmed gap with no available benchmark for the deployment''s
    specific use case. Source: arXiv 2603.19514 — [WEB-10]'
- item: FOLIO inference-rule vocabulary vs. Fitch-style rule names — formal compatibility
    mapping
  notes: 'Resolved (null result). No published systematic mapping between FOLIO''s
    Russell & Norvig FOL operators and LPL Fitch rule names was found. FOLIO''s operator
    inventory (¬, ∧, ∨, →, ∀, ∃, =) overlaps with Fitch connectives, but the rule-name
    vocabulary (e.g., FOLIO uses informal NL proof chains in P-FOLIO rather than named
    inference rules; LPL uses →E, ∧I, ∀E etc.) is not mapped in any published resource.
    The lplfitch LaTeX package and el-sambal/fitch-proof checker document LPL rule
    syntax but do not cross-reference FOLIO. Constructing this mapping would require
    manual alignment work. Sources: OpenLogicProject fitch — [WEB-3];
    el-sambal/fitch-proof — [WEB-14]'
- item: Device and connectivity profile of US undergraduate logic students
  notes: 'Resolved. EDUCAUSE and New America survey data (2020–2023) indicate: ~66–72%
    of undergraduates primarily use laptops/desktops for coursework; ~20% rely primarily
    on mobile/cellular devices; four in five students connect both smartphone and
    laptop to campus Wi-Fi daily. Approximately 77–88% of undergraduates across institution
    types have home high-speed internet, but a national EDUCAUSE survey found ~64%
    experienced unstable connections, and roughly half of community-college students
    with broadband described internet as a high financial burden. These figures are
    national aggregates; community-college and low-income student subpopulations face
    meaningfully higher connectivity barriers. Sources: New America/EDUCAUSE community-college
    survey — [WEB-5];
    EDUCAUSE 2023 mobile learning — [WEB-6]'
- item: Institutional variation in logic course conventions (proof system used, notation
    standards) across philosophy vs. math vs. CS departments
  notes: 'Partially resolved. The LPL/Fitch system is confirmed as the dominant proof
    environment for philosophy-department logic courses in the US (used at Stanford,
    Indiana University, and widely across philosophy departments). The forall x: Calgary
    Remix (open-access) uses a compatible Fitch system and is increasingly adopted
    at institutions preferring open textbooks. Mathematics departments typically use
    informal proof or sequent calculus; CS departments may use resolution, tableau,
    or formal methods tools (e.g., Lean, Coq). No national survey quantifying the
    distribution of proof systems across US logic courses was found. [NEEDS VERIFICATION
    — deferred: quantitative distribution of proof systems across departments requires
    survey data not available via web search] Sources: LPL Wikipedia — [WEB-16];
    OpenLogicProject fitch-checker — [WEB-2]'
net_new_fields:
  p_folio_companion_dataset:
    description: 'P-FOLIO (EMNLP Findings 2024, Yale NLP) is a human-annotated companion
      to FOLIO containing step-by-step natural-language reasoning chains (0–20 steps)
      for FOLIO''s realistic FOL stories, with inference-rule classification and pass@k
      evaluation metrics. It is the closest existing resource to the deployment''s
      proof-trace requirement, but uses narrative NL chains rather than Fitch-style
      rule-cited formal proofs. Fine-tuning LLaMA3-7B on P-FOLIO improves performance
      by 10%+ on three out-of-domain logical reasoning datasets. Relevance: P-FOLIO
      partially addresses the output-form and pedagogical-explanation gaps flagged
      for FOLIO, and should be included in any benchmark complement strategy for this
      deployment.'
    source: ACL Anthology EMNLP 2024 Findings — [WEB-7];
      arXiv 2410.09207 — [WEB-19]; HuggingFace dataset
      — [WEB-21]
  llm_logic_its_evaluation_2025:
    description: 'A May 2025 peer-reviewed study (Computers & Education: Artificial
      Intelligence) directly evaluates LLMs on stepwise propositional logic proof
      construction and hint generation for an intelligent tutoring system. Using 358
      propositional logic problems and 1,050 student problem-solving states from a
      live ITS, it finds DeepSeek-V3 achieves ~84–87% stepwise accuracy but LLM-generated
      hints score only 75% accurate and underperform on contextual explanation and
      pedagogical appropriateness. This is the first published evaluation of LLMs
      in a live propositional logic ITS context and directly informs the deployment''s
      achievability and key failure modes (hint context, not rule-citation accuracy).'
    source: arXiv 2505.04736 — [WEB-9]; ScienceDirect
      — [WEB-18]
  fol_traces_dataset_2025:
    description: 'FOL-Traces (arXiv 2505.14932, May 2025) introduces a large-scale
      dataset of verified FOL reasoning traces (3.5 billion tokens, 8.8 million LLM-augmented
      human-annotated examples and 7.5 million synthetic examples), each produced
      by an automated theorem solver with metadata tracing algorithmic provenance.
      Relevance: as a training and evaluation resource for FOL reasoning chain generation,
      FOL-Traces may be useful for training the deployment''s proof-trace generation
      component, though it targets algorithmic/formal FOL traces rather than pedagogical
      Fitch-style proofs.'
    source: arXiv 2505.14932 — [WEB-22]
  counterexample_generation_research_frontier:
    description: Formal counterexample generation for LLMs is an active 2025–2026
      research frontier. The 'Learning to Disprove' paper (arXiv 2603.19514, 2026)
      introduces a training framework requiring LLMs to produce formal counterexamples
      verified in Lean 4, with three newly collected benchmarks. CounterMath (Li et
      al. 2025) is the only published dataset for counterexample generation benchmarking
      (1,216 NL problems, mathematical scope). Neither covers FOL/propositional logic
      countermodels in the educational sense the deployment requires. This confirms
      that countermodel generation for undergraduate logic is a genuine benchmark
      gap with no off-the-shelf solution.
    source: arXiv 2603.19514 — [WEB-10]
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://press.uchicago.edu/ucp/books/book/distributed/L/bo12734345.html |
| WEB-2 | https://github.com/OpenLogicProject/fitch-checker |
| WEB-3 | https://github.com/OpenLogicProject/fitch |
| WEB-4 | https://www.logicmatters.net/latex-for-logicians/nd/ |
| WEB-5 | https://www.newamerica.org/education-policy/edcentral/how-do-community-college-students-access-online-learning/ |
| WEB-6 | https://er.educause.edu/articles/2023/1/the-evolving-landscape-of-students-mobile-learning-practices-in-higher-education |
| WEB-7 | https://aclanthology.org/2024.findings-emnlp.966/ |
| WEB-8 | https://openreview.net/forum?id=rhdfTOiXBng |
| WEB-9 | https://arxiv.org/abs/2505.04736 |
| WEB-10 | https://arxiv.org/pdf/2603.19514 |
| WEB-11 | https://arxiv.org/pdf/2505.00001 |
| WEB-12 | https://arxiv.org/html/2509.15587v3 |
| WEB-13 | https://aclanthology.org/2021.findings-acl.317.pdf |
| WEB-14 | https://github.com/el-sambal/fitch-proof |
| WEB-15 | https://openreview.net/pdf?id=rhdfTOiXBng |
| WEB-16 | https://en.wikipedia.org/wiki/Language,_Proof_and_Logic |
| WEB-17 | https://fitch.rug.themisjudge.nl/ |
| WEB-18 | https://www.sciencedirect.com/science/article/pii/S2666920X25001304 |
| WEB-19 | https://arxiv.org/abs/2410.09207 |
| WEB-20 | https://github.com/wellecks/naturalproofs |
| WEB-21 | https://huggingface.co/datasets/yale-nlp/P-FOLIO |
| WEB-22 | https://arxiv.org/pdf/2505.14932 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [OF]: FOLIO produces binary correctness labels (true/false/uncertain) as outputs, but your deployment requires step-by-step reasoning traces that students can follow. How detailed and structured should these explanations be, and would explanations differ between introductory and advanced students?
A1: The deployment needs numbered deduction steps that explicitly cite which premises are used at each step, paired with plain-English summaries of the logical move (e.g., "applying modus ponens to premises 2 and 4"). Introductory students get natural-language-heavy explanations with minimal notation; advanced students need quantifiers, predicates, and inference-rule names. Ideally the tool supports both registers, or a single layered explanation combining prose and formal annotations.

Q2 [OO]: Does the platform commit to a specific proof method, and must explanations follow the canonical reasoning path or can alternative valid paths be accepted?
A2: The canonical framework is Fitch-style natural deduction, matching mainstream US intro logic textbooks. Alternative valid reasoning paths are acceptable so long as every inference step is explicit and rule-justified — unexplained leaps to conclusions are not acceptable. For invalid arguments, the expected output is a countermodel or counterexample rather than a failed proof attempt.

Q3 [IO]: Which logical domains must the tool handle, and are there argument types that pure FOL exercises might not capture?
A3: The tool must handle propositional logic, predicate/FOL, and argument reconstruction from natural English. Modal logic and inductive reasoning are out of scope for this tool (fallacy identification is a planned separate module). Students regularly encounter arguments with implicit premises and multi-step chains drawn from everyday or quasi-legal scenarios, so the tool must support natural-language-to-logical-form translation, not just operate on pre-formalized premises.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | FOLIO's FOL deductive scope covers the core of the deployment's needs, but the tool must also handle propositional logic and natural-language argument reconstruction with implicit premises — categories FOLIO does not emphasize — creating a moderate coverage gap. |
| IC | MODERATE | FOLIO's examples are expert-annotated with formal FOL premises, whereas the deployment involves everyday and quasi-legal natural-language arguments with implicit premises; some FOLIO instances may be too artificial or too narrowly formalized to reflect the argument types students encounter. |
| IF | LOWER | Both FOLIO and the deployment are text-only, English-language, high-resource — no modality or script mismatch. |
| OO | HIGH | FOLIO's output space is a three-way classification label (true/false/uncertain), which is entirely misaligned with the deployment's required output: structured, rule-justified, register-differentiated proof traces and countermodels; the scoring function cannot directly evaluate explanation quality or pedagogical fidelity. |
| OC | MODERATE | FOLIO's ground-truth labels are verified by a FOL inference engine and expert annotators, making correctness labels reliable for deductive validity; however, no ground-truth exists for what constitutes a pedagogically acceptable explanation, particularly for the Fitch-style natural deduction register the curriculum requires. |
| OF | HIGH | The benchmark outputs a single label; the deployment requires multi-step natural-language and/or formally annotated proof traces differentiated by student level, plus countermodels for invalid arguments — this is a fundamental output-form mismatch that FOLIO cannot directly evaluate. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** yale-nlp/FOLIO (config: default)
**Analysis date:** 2025-07-14
**Examples reviewed:** 57 from `train` split
**Columns shown:** story_id, premises, premises-FOL, conclusion, conclusion-FOL, label, example_id
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | FOLIO/train | Ex. 1 | True | "No plants are fungi. Mushrooms are fungi. / ∀x (Plant(x) → ¬Fungi(x)) ∀x (Mushroom(x) → Fungi(x))" | Simple 2-premise syllogism with parallel NL and FOL | IO, IC |
| D2 | FOLIO/train | Ex. 2 | Uncertain | "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises… Mike works in this tech company. If Mike is not a person who wears the same flannel shirts every day, has very high energy, and is impulsive, then Mike either is very consistent and enjoys sticking to his regular routines or does not like surprises." | Multi-premise story (7 premises) about a tech company worker; complex conditional | IO, IC |
| D3 | FOLIO/train | Ex. 3 | Uncertain | "A project is written either in C++ or Python. If Sam does a project written in Python, he will not use a Mac. Sam is using a Mac. If a song is not titled 'Perfect,' Sam will never play it." | Multi-step chain mixing disjunction, implication, and named individual | IO |
| D4 | FOLIO/train | Ex. 4 | False | "No trick-shot artist in Yale's varsity team struggles with half court shots. Everyone on Yale's varsity team is someone who struggles with half court shots or who successfully shoots a high percentage of 3-pointers." — "Jack is bad at mid-range shots." | Basketball sports story requiring 4+ step chain | IO, IC |
| D5 | FOLIO/train | Ex. 5 | Uncertain | "All Yale students at the event are college students. Everyone at the event is a Yale student or a Harvard student. If Susan is a Yale student, then she does not like independence." | Classic university-setting syllogism with exclusive disjunction | IO |
| D6 | FOLIO/train | Ex. 6 | Uncertain | "All entrepreneurs at the business conference enjoy the opportunity of starting a business. Everyone at the business conference who is an ardent communist prefers state ownership of the means of production. Ho is at the business conference and prefers state ownership of the means of production." | Politically framed scenario with communist/investor dichotomy | IC, OC |
| D7 | FOLIO/train | Ex. 7 | Uncertain | "Andy Chang directed EndGame. Andy Chang is from Hong Kong." — conclusion: "All of Andy Chang's movies are filmed outside of Washington." | Wikipedia-seeded story about a real-world film director from Hong Kong | IC |
| D8 | FOLIO/train | Ex. 8 | Uncertain | "Every person in Potterville that knows magic flies. All wizards in Potterville know magic. Harry, who lives in Potterville either yells or flies." | Fictional Potterville scenario referencing Harry/Potter (Harry Potter allusion) | IC |
| D9 | FOLIO/train | Ex. 11 | False | "Everything in Size Town is big or small. All big things in Size Town are heavy… The bird is in Size Town and it is not both heavy and still." — conclusion: "If the bird is small or still, then it is either unpredictable or changing." | Purely abstract Size Town scenario — no real-world content | IC |
| D10 | FOLIO/train | Ex. 12 | True | "Some cats are not pets. All cats are mammals." — conclusion FOL: "∃x ∃y (Mammal(x) ∧ Mammal(y) ∧ ¬Pet(x) ∧ ¬Pet(y))" | Simple existential syllogism; conclusion FOL is strictly stronger than needed | OC, OO |
| D11 | FOLIO/train | Ex. 13 | False | "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable… ROUGE Dior Colored Lip Balm 999 is a lipstick in the set, and it either has 'rosewood' in its official description or has a velvet finish." | Real-world brand story about a specific luxury cosmetics product | IC |
| D12 | FOLIO/train | Ex. 15 | Uncertain | "John Nash designed Oxford Circus. John Nash is a British architect. Oxford Circus is the entrance to Oxford Circus tube station, a part of the Central line in 1900." | Wikipedia-seeded story about real architect John Nash | IC |
| D13 | FOLIO/train | Ex. 16 | True | "All Olympic gold medal winners are professional athletes. All Nobel physics laureates are full-time scientists. Amy spends the most time on sports, or Amy is an Olympic gold medal winner. If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." | Multi-step chain combining disjunction, contrapositive, complex reasoning | IO |
| D14 | FOLIO/train | Ex. 17 | False | "Michael O'Donnell is a British physician, journalist, author, and broadcaster… Michael O'Donnell was born in Yorkshire" — conclusion: "There are no journalists that were born in Yorkshire." | Simple false universal overgeneralization from a positive instance | OO |
| D15 | FOLIO/train | Ex. 21 | False | "All people who attend Renaissance fairs regularly enjoy dressing up in old-fashioned and historical period clothing… Clyde is a professor who takes a historical approach." | Complex 6-premise story about cultural interests and academic roles | IO |
| D16 | FOLIO/train | Ex. 22 | Uncertain | "All PRC nationals are entitled to national social insurance coverage. Everyone in the Franco-China diplomatic conference is either a PRC national or a French national, but not both… Either Mei is a North Korean and can have medical bills partially covered, or neither is true." | Geopolitical scenario involving PRC, France, North Korea nationals | IC |
| D17 | FOLIO/train | Ex. 23 | Uncertain | "The world's only major large passenger aircraft manufacturers are Boeing and Airbus." — conclusion: "There exists a SpaceX commercial aircraft." | Real-world entities (Boeing, Airbus, SpaceX) in an Uncertain-labeled example | IC, OC |
| D18 | FOLIO/train | Ex. 27 | Uncertain | "Bobby Flynn finished 7th while competing on Australian Idol. Australian Idol competitors are Australian citizens." — conclusion: "Bobby Flynn flew to America in 2007." | Wikipedia-seeded story about Australian musician | IC |
| D19 | FOLIO/train | Ex. 28 | False | "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. There is an embargo on Russian foreign trade goods." — conclusion: "In Russia, an effective monetary policy is possible." | Real-world geopolitical/economic scenario involving Russia and embargos | IC, OC |
| D20 | FOLIO/train | Ex. 33 | Uncertain | "No battery-powered watch is automatic. All digital watches are battery-powered. Moonwatch is either a digital watch and an automatic, or it is neither." | Classic syllogistic chain about watches | IO |
| D21 | FOLIO/train | Ex. 34 | True | "All orphan planets are rogue planets. If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." | Scientific Wikipedia-seeded story about astronomy | IC |
| D22 | FOLIO/train | Ex. 43 | True | "All inductive reasoning processes derive general principles from a body of observations. Modus Ponens is not both used in inductive reasoning and used for statistical generalization. Modus Ponens is a component of a major part of reasoning rule." | Story explicitly about Modus Ponens and inductive/deductive reasoning | IC, IO |
| D23 | FOLIO/train | Ex. 52 | True | "No athletes never exercise. All professional basketball players are athletes… Either John is a professional basketball player and he never exercises, or he is not a professional basketball player and he sometimes exercises." — NOTE: FOL annotation says "jim" while NL says "John" | Annotation inconsistency: NL uses "John," FOL uses "jim" | OC |
| D24 | FOLIO/train | Ex. 2 | Uncertain | premises-FOL contains: "¬(∃y (flannelShirt(y) ∧ WearEveryday(x, y)) ∧ Have(mike, highEnergy) ∧ Impulsive(mike)) → (Consistent(mike) ∧ StickTo(mike, theirRegularRoutine)) ⊕ ¬Like(mike, surprise)" — uses unbound variable x in outer formula | FOL annotation contains a free variable 'x' not properly bound | OC |
| D25 | FOLIO/train | Ex. 36 | True | "Lily is in James' family; she watches TV series in cinemas." — premises-FOL: "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" | Malformed FOL: missing closing parenthesis in the premises-FOL formula | OC |
| D26 | FOLIO/train | Ex. 57 | False | "Matt does not invest in the public stock market regularly. Matt likes financial risks." — premises-FOL premise 6: "InvestInRegularly(matt, publicStockMarket)" | NL premise contradicts FOL annotation: NL says "does not invest" but FOL asserts InvestInRegularly(matt) without negation | OC |
| D27 | FOLIO/train | Ex. 10 | Uncertain | "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" — extra closing parenthesis in last premise FOL | Minor FOL syntax artifact (extra parenthesis) | OC |
| D28 | FOLIO/train | Ex. 4 | False | "No trick-shot artist in Yale's varsity team struggles with half court shots." conclusion-FOL: "BadAt(jack, midRangeShot)" | Short FOL conclusion for a 5-premise story requiring multi-step chain | IO |
| D29 | FOLIO/train | Ex. 46 | Uncertain | "Everyone that knows about breath-first-search knows how to use a queue… Jack is entitled to the right to life and liberty, has human rights, or knows about the first-in-first-out data structure." | CS / human rights story — 7 premises requiring complex multi-step chain | IO |
| D30 | FOLIO/train | Ex. 54 | True | "All players must reach the yellow stage before they can reach the green stage. The yellow stage comes after the red stage." — premises-FOL contains "∃x ∃y ∃y ∃w" (duplicate variable y) | Minor FOL annotation typo: variable y declared twice | OC |
| D31 | FOLIO/train | Ex. 50 | Uncertain | "Each building is tall. Everything tall has height." — conclusion: "All buildings are magnificent." | Extremely short, minimal story (2 premises) — simple non-sequitur conclusion | IO |
| D32 | FOLIO/train | Ex. 55 | False | "TikTok is a social media application, and it is not ideal for preteens." — conclusion-FOL: "Contain(tikTok, chatFeature) ⊕ ComputerProgram(tikTok))" — extra closing parenthesis | FOL annotation has mismatched parenthesis | OC |
| D33 | FOLIO/train | Ex. 13 | False | "No satin-finish lipsticks in the set do not have 'rosewood' in its offical description." | Double-negative NL phrasing ("No X do not have") that may create ambiguity | IF |
| D34 | FOLIO/train | Ex. 43 | True | "Modus Ponens is a component of a major part of reasoning rule." premises-FOL: "ArgumentForm(modusPonens)" | Example featuring logic-domain content (Modus Ponens) — relevant to deployment | IC, IO |
| D35 | FOLIO/train | Ex. 16 | True | "All professional athletes spend most of their time on sports… If Amy is not a Nobel physics laureate, then Amy is not an Olympic gold medal winner." | Contrapositives and multi-step chains matching textbook exercise style | IO |
| D36 | FOLIO/train | Ex. 38 | False | "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination… James has a car or works at Meta." | Contemporary real-world scenario (Meta/Google) embedded in logic chain | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Strong coverage of multi-premise, multi-step deductive FOL reasoning
- **Dimension(s):** IO
- **Observation:** The sampled examples span a wide range of reasoning depths, from simple 2-premise syllogisms to 7-premise chains requiring sequential chaining of conditionals, universal quantifiers, and disjunctions. Multiple examples require traversing 4–6 logical steps before reaching a conclusion, directly matching the deployment's need to evaluate complex deductive reasoning.
- **Deployment relevance:** The deployment must assess whether an LLM can correctly determine argument validity before generating a pedagogical trace. FOLIO's depth distribution — confirmed in the data — provides genuine difficulty stratification across introductory (simple syllogisms) and advanced (multi-step chains) registers.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO, train, True): "No plants are fungi. Mushrooms are fungi." — Minimal 2-premise syllogism, analogous to introductory-level exercises.
  - [D2] Example 2 (FOLIO, train, Uncertain): "All people in this tech company who are consistent and enjoy sticking to their regular routines do not like surprises… Mike works in this tech company." — 7-premise story requiring multiple chained universals and a complex conditional, analogous to advanced-level exercises.
  - [D29] Example 46 (FOLIO, train, Uncertain): "Everyone that knows about breath-first-search knows how to use a queue… Jack is entitled to the right to life and liberty, has human rights, or knows about the first-in-first-out data structure." — 7-premise story with chained conditionals and disjunction.

#### Strength 2: Parallel NL and FOL representations per example
- **Dimension(s):** IO, IF
- **Observation:** Every example contains both a natural-language story and its parallel FOL annotation, supporting both the validity-determination task and the NL-to-FOL translation secondary task. The FOL layer uses the standard operator inventory (¬, ∧, ∨, →, ⊕, ∀, ∃, =) consistently across examples.
- **Deployment relevance:** The deployment requires NL-to-formal-logic translation as a core capability. FOLIO's parallel annotations allow evaluation of whether an LLM can correctly formalize NL premises, which is a prerequisite for the Fitch-style proof generation the tool needs to produce.
- **Datapoint citations:**
  - [D13] Example 16 (FOLIO, train, True): NL "All Olympic gold medal winners are professional athletes" → FOL "∀x (OlympicGoldMedalWinner(x) → ProfessionalAthlete(x))" — straightforward universal conditional mapping.
  - [D21] Example 34 (FOLIO, train, True): "All orphan planets are rogue planets. If PSO J318.5−22 is not both a rogue planet and a planet gravitationally bound by the Sun, then it is a rogue planet." — complex conditional with negated conjunction, illustrating the NL→FOL difficulty range.

#### Strength 3: Topical diversity supporting broad argument-type coverage
- **Dimension(s):** IC
- **Observation:** The sampled examples cover a wide range of content domains: natural science (biology, astronomy, physics), geography, sports, technology, economics, media, cultural activities, and everyday scenarios. This variety mirrors the range of argument types students encounter in US undergraduate logic courses, where textbook exercises span analogous domains.
- **Deployment relevance:** Students in intro logic courses encounter arguments drawn from diverse subject matter. FOLIO's topical range reduces the risk that a model fine-tuned or evaluated on FOLIO will be topically overfitted to any single domain.
- **Datapoint citations:**
  - [D21] Example 34 (FOLIO, train, True): "All orphan planets are rogue planets… PSO J318.5−22…" — astrophysics domain.
  - [D11] Example 13 (FOLIO, train, False): "All velvet-finish lipsticks in the Rouge Dior set, Lunar New Year Limited Edition are refillable…" — consumer products domain.
  - [D19] Example 28 (FOLIO, train, False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. There is an embargo on Russian foreign trade goods." — macroeconomics/geopolitics domain.
  - [D4] Example 4 (FOLIO, train, False): "No trick-shot artist in Yale's varsity team struggles with half court shots." — sports domain.

#### Strength 4: Three-way label distribution includes True, False, and Uncertain
- **Dimension(s):** OO
- **Observation:** The sampled examples include all three label categories. Across the 57 reviewed examples, all three labels appear in meaningful proportions, including several False examples requiring the reasoner to identify why a conclusion does not follow or is contradicted.
- **Deployment relevance:** The deployment must identify both valid and invalid arguments. The False and Uncertain labels cover two distinct failure modes (contradiction and underdetermination), which partially map to the deployment's need to handle invalid arguments (for which countermodels are required). FOLIO does not produce countermodels, but the label space at least identifies where they would be needed.
- **Datapoint citations:**
  - [D14] Example 17 (FOLIO, train, False): "Michael O'Donnell is a British physician, journalist, author, and broadcaster… Michael O'Donnell was born in Yorkshire" — conclusion "There are no journalists that were born in Yorkshire" is False because the premises provide a direct counterexample.
  - [D28] Example 4 (FOLIO, train, False): "Jack is bad at mid-range shots" — labeled False given the premises about Yale's varsity team.
  - [D5] Example 5 (FOLIO, train, Uncertain): "Susan is a college student" — labeled Uncertain because her affiliation (Yale vs. Harvard) cannot be determined.

#### Strength 5: Explicit formal premise structure matching formal-logic course exercises
- **Dimension(s):** IC
- **Observation:** FOLIO premises are stated as explicit, closed-world assertions (all universals, conditionals, and individual facts are spelled out), directly matching the style of textbook logic exercises where students are given a set of premises and asked to assess a conclusion. This matches the exercise format in Barwise & Etchemendy-style courses.
- **Deployment relevance:** The deployment tool must handle arguments presented as explicit premise sets (as in textbook exercises), which is the dominant format in US undergraduate logic courses. FOLIO's explicit-premise style is well-suited for this sub-task, even if implicit-premise reconstruction is separately needed.
- **Datapoint citations:**
  - [D20] Example 33 (FOLIO, train, Uncertain): "No battery-powered watch is automatic. All digital watches are battery-powered. Some mechanical watches are automatic. All smart watches are digital. Moonwatch is either a digital watch and an automatic, or it is neither." — Complete set of explicit premises in the style of a textbook exercise.
  - [D31] Example 50 (FOLIO, train, Uncertain): "Each building is tall. Everything tall has height." — Minimal premise set; conclusion "All buildings are magnificent" tests non-sequitur recognition.

#### Strength 6: One example contains content directly relevant to logic pedagogy
- **Dimension(s):** IC, IO
- **Observation:** One example in the sample explicitly features Modus Ponens as a named entity within the story, along with discussion of inductive vs. deductive reasoning. While framed as a logic puzzle rather than a pedagogical explanation, this content is directly relevant to the deployment's domain.
- **Deployment relevance:** Students using the tool will be reasoning about logic itself (meta-logical arguments). FOLIO contains at least some examples where the content domain is formal reasoning, which aligns with logic course content.
- **Datapoint citations:**
  - [D22] Example 43 (FOLIO, train, True): "All inductive reasoning processes derive general principles from a body of observations. Two major types of reasoning rules are inductive reasoning and deductive reasoning… Modus Ponens is a component of a major part of reasoning rule." — The entity "Modus Ponens" appears as a subject of logical predicates, directly engaging the deployment's pedagogical domain.
  - [D34] Example 43 (FOLIO, train, True): "ArgumentForm(modusPonens)" in the FOL annotation — confirms the named rule appears in formal representation.

---

### Potential Concerns

#### CRITICAL

#### Concern 1: Output space is a three-way classification label — no proof traces, no countermodels
- **Dimension(s):** OO, OF
- **Observation:** Every example in the dataset has a single string label (True/False/Uncertain). There are no fields for step-by-step reasoning chains, numbered deduction steps, premise citation patterns, inference rule names, or countermodel specifications. The schema has exactly six fields: premises, premises-FOL, conclusion, conclusion-FOL, label, and IDs. No ground-truth proof trace or explanation artifact exists anywhere in the data.
- **Deployment relevance:** The deployment's primary output requirement is a numbered, rule-justified, register-differentiated proof trace (or countermodel for invalid arguments). FOLIO cannot directly evaluate whether a model produces such an output. The benchmark's output ontology and output form are completely orthogonal to what the deployment needs to score. Every False-labeled example (where a countermodel is required) provides only the label, with no reference countermodel to evaluate against.
- **Datapoint citations:**
  - [D14] Example 17 (FOLIO, train, False): "Michael O'Donnell is a British physician, journalist, author, and broadcaster… Michael O'Donnell was born in Yorkshire as the son of a general practitioner." — Labeled False, but the dataset provides no countermodel showing that there exists a journalist born in Yorkshire; only the string "False" is present.
  - [D4] Example 4 (FOLIO, train, False): "Jack is bad at mid-range shots." — Labeled False with no explanation of which step in the chain fails or what interpretation demonstrates the falsity.
  - [D1] Example 1 (FOLIO, train, True): "No plants are fungi. Mushrooms are fungi." — Labeled True, but no proof trace showing the deduction steps is provided; a deployment requiring "applying modus ponens to premises 2 and 4" has no reference output to compare against.

#### Concern 2: Notation mismatch — FOLIO uses Russell & Norvig FOL, not Fitch-style natural deduction
- **Dimension(s):** IF, OO
- **Observation:** All FOL annotations in the dataset use Russell & Norvig-style flat predicate logic notation (e.g., `∀x (Plant(x) → ¬Fungi(x))`, with infix operators and no subproof structure). Fitch-style natural deduction, as used in Barwise & Etchemendy's LPL curriculum, uses a structurally different notation: numbered lines, subproof boxes, and named inference rules (e.g., →E, ∧I, ¬I). There is no Fitch-style annotation, no rule-name vocabulary, and no subproof structure anywhere in the 57 reviewed examples.
- **Deployment relevance:** The deployment's target students are taught Fitch-style notation. A tool producing outputs in Russell & Norvig FOL notation would be misaligned with what students are expected to produce and recognize. There is no documented mapping between FOLIO's operator vocabulary and LPL rule names. This is not merely a surface formatting difference — ∀E (universal elimination, a named Fitch rule) vs. the implicit universal instantiation in FOLIO's flat FOL involves different pedagogical scaffolding.
- **Datapoint citations:**
  - [D13] Example 16 (FOLIO, train, True): "∀x (OlympicGoldMedalWinner(x) → ProfessionalAthlete(x))" — flat FOL implication, no rule name cited; in Fitch style this would be referenced as line N, rule ∀E applied to a specific premise line.
  - [D2] Example 2 (FOLIO, train, Uncertain): "∀x (InThisTechCompany(x) ∧ Consistent(x) ∧ StickTo(x, theirRegularRoutine) → ¬Like(x, surprise))" — Russell & Norvig predicate notation with no Fitch structural markers.

#### MAJOR

#### Concern 3: No propositional-logic-only examples — all examples use FOL constructs
- **Dimension(s):** IO
- **Observation:** Every example in the sample uses at least one first-order logic construct (universal quantifier ∀, existential quantifier ∃, or predicates with arguments). There are no propositional-only examples using only sentential connectives (¬, ∧, ∨, →, ↔) applied to atomic propositions without quantification. The deployment requires handling of propositional logic as a distinct layer.
- **Deployment relevance:** US introductory logic courses (both philosophy and CS-flavored) typically begin with propositional/sentential logic before introducing predicate logic. Students learning to use the tool early in their course will present purely propositional arguments. FOLIO provides no coverage of this sub-domain.
- **Datapoint citations:**
  - [D1] Example 1 (FOLIO, train, True): "∀x (Plant(x) → ¬Fungi(x)) ∀x (Mushroom(x) → Fungi(x))" — even the simplest example uses universal quantification, not propositional logic.
  - [D31] Example 50 (FOLIO, train, Uncertain): "∀x (Building(x) → Tall(x)) ∀x (Tall(x) → Height(x))" — 2-premise minimal example still uses FOL quantifiers rather than sentential connectives.
  - [D9] Example 11 (FOLIO, train, False): "∀x (In(x, sizeTown) → (Big(x) ∨ Small(x)))" — abstract scenario still uses universal quantification throughout.

#### Concern 4: All premises are fully explicit — no implicit-premise or enthymeme cases
- **Dimension(s):** IC
- **Observation:** In every reviewed example, all premises needed for the inference are stated explicitly in the premise set. There are no enthymematic arguments where a premise is left implicit and must be reconstructed from context or background knowledge. The annotation process explicitly added commonsense premises as explicit FOL statements, confirmed by the data: even highly structured "everyday" scenarios list every required premise.
- **Deployment relevance:** The deployment explicitly requires handling arguments where premises are implicit and must be reconstructed — "Students regularly encounter arguments with implicit premises and multi-step chains drawn from everyday or quasi-legal scenarios." FOLIO provides no coverage of this sub-task. A model evaluated solely on FOLIO would have no signal about its ability to perform premise reconstruction.
- **Datapoint citations:**
  - [D36] Example 38 (FOLIO, train, False): "Everyone working at Meta has a high income. A person with a high income will not take a bus to their destination. People will either take a bus or drive to their destination. Everyone who has a car will choose to drive to their destination. No students drive to their destination. James has a car or works at Meta." — What could be a 1-premise implicit argument ("James works at Meta, so he won't take the bus") is instead fully expanded into 6 explicit premises, eliminating any need for premise reconstruction.
  - [D19] Example 28 (FOLIO, train, False): "For a country, if effective monetary policy is possible, it must have successful inflation control and a strong national currency. A country cannot simultaneously regulate the exchange rate and successfully control inflation… There is an embargo on Russian foreign trade goods." — All intermediate economic causal links are stated as explicit premises; no inference to unstated background knowledge is required.

#### Concern 5: FOL annotation errors found in sampled examples
- **Dimension(s):** OC
- **Observation:** Several FOL annotations in the reviewed sample contain apparent errors: (a) a free (unbound) variable `x` in Example 2's premises-FOL; (b) a missing closing parenthesis in Example 36's premises-FOL; (c) a contradictory annotation in Example 57 where the NL premise states "Matt does not invest in the public stock market regularly" but the FOL encodes `InvestInRegularly(matt, publicStockMarket)` without negation; (d) a variable declared twice (`∃x ∃y ∃y ∃w`) in Example 54; (e) an extra closing parenthesis in Example 55's conclusion-FOL; (f) a cross-name inconsistency in Example 52 where NL says "John" but FOL uses "jim."
- **Deployment relevance:** If FOLIO is used to evaluate a model's NL-to-FOL translation capability (the secondary task), annotation errors in the reference FOL create incorrect ground truth, inflating or deflating translation scores. More critically, if a model is trained on FOLIO's FOL annotations, these errors propagate into learned behavior. Given the deployment's requirement for formally correct proof traces, training data with FOL inconsistencies is a meaningful concern.
- **Datapoint citations:**
  - [D24] Example 2 (FOLIO, train, Uncertain): "¬(∃y (flannelShirt(y) ∧ WearEveryday(x, y)) ∧ Have(mike, highEnergy) ∧ Impulsive(mike)) → ..." — `x` is unbound in this formula while `mike` is bound, indicating a free-variable error.
  - [D25] Example 36 (FOLIO, train, True): "Customer(lily) ∧ In(lily, jameSFamily ∧ WatchIn(lily, tV, cinema)" — missing closing parenthesis after `jameSFamily`.
  - [D26] Example 57 (FOLIO, train, False): NL: "Matt does not invest in the public stock market regularly" vs. FOL premise 6: "InvestInRegularly(matt, publicStockMarket)" — the negation is absent from the FOL annotation.
  - [D23] Example 52 (FOLIO, train, True): NL uses "John" throughout; FOL uses "jim" — inconsistent entity naming between NL and FOL layers.
  - [D30] Example 54 (FOLIO, train, True): "∃x ∃y ∃y ∃w" — variable `y` declared twice in the existential prefix.
  - [D27] Example 10 (FOLIO, train, Uncertain): "(Knows(dan, dune) ∧ ScienceFiction(dune)) ∨ ProvedToBe(dune, false))" — extra closing parenthesis.

#### Concern 6: Content occasionally involves politically or geopolitically sensitive real-world scenarios
- **Dimension(s):** IC, OC
- **Observation:** Several examples use real-world geopolitical entities and politically loaded content: one example involves an "ardent communist" in a business conference context, another uses Russian economic sanctions, and another uses PRC/French/North Korean nationals in a diplomatic conference. While the logical structure is neutral, the content choices may introduce distracting associations for US undergraduate students and could touch on politically sensitive areas in a classroom setting.
- **Deployment relevance:** For an educational tool targeting US undergraduates, content involving communist ideology, Russian sanctions, or North Korean nationality may generate controversy or distraction unrelated to the logic task. The deployment context mentions content neutrality as a concern.
- **Datapoint citations:**
  - [D6] Example 6 (FOLIO, train, Uncertain): "Everyone at the business conference who is an ardent communist prefers state ownership of the means of production. Ho is at the business conference and prefers state ownership of the means of production." — "Ardent communist" as a predicate in a logical argument.
  - [D19] Example 28 (FOLIO, train, False): "There is an embargo on Russian foreign trade goods." — Contemporary geopolitical scenario.
  - [D16] Example 22 (FOLIO, train, Uncertain): "No North Korean nationals are citizens of the European Union… Either Mei is a North Korean and can have medical bills partially covered, or neither is true." — North Korean nationality as a logical predicate.

#### MINOR

#### Concern 7: Absent test split in the HuggingFace dataset
- **Dimension(s):** OF
- **Observation:** The HF dataset schema shows only `train` (1,001 examples) and `validation` (203 examples) splits. The test split (226 examples per the paper) is not present in the public HuggingFace release. All sampled examples are from the train split.
- **Deployment relevance:** If the deployment uses FOLIO as an evaluation benchmark, the relevant held-out test set is unavailable via the standard HuggingFace loader. The validation set (203 examples) would need to serve as the evaluation partition, which reduces the evaluation sample size and may introduce slight coverage differences from what the paper reports.
- **Datapoint citations:** (schema-level observation, not datapoint-specific — all 57 reviewed examples are from `train` split per the metadata)

#### Concern 8: Some examples contain double-negative or ambiguous NL phrasing
- **Dimension(s):** IF
- **Observation:** At least one premise in the reviewed examples uses a double-negative construction ("No satin-finish lipsticks in the set do not have 'rosewood' in its official description") that is grammatically non-standard and could be construed as either a negated universal or an accidentally-double-negated affirmative. While the FOL annotation resolves the ambiguity, NL-level phrasing quality is uneven.
- **Deployment relevance:** The deployment requires clear, natural-language explanations that students can follow. If FOLIO's NL tier contains confusingly phrased premises, models trained on or evaluated against these examples may learn to produce similarly unclear phrasing in pedagogical explanations.
- **Datapoint citations:**
  - [D33] Example 13 (FOLIO, train, False): "No satin-finish lipsticks in the set do not have 'rosewood' in its official description." — Double negative construction may confuse students who encounter this as an explanation example.

#### Concern 9: Some HybLogic examples are visibly template-derived with artificial scenario framing
- **Dimension(s):** IC
- **Observation:** Several examples use purely abstract or fictional settings (Size Town, Potterville) that have no real-world grounding. While logically valid as test cases, these scenarios may feel pedagogically thin relative to the everyday and quasi-legal argument contexts the deployment aims to support.
- **Deployment relevance:** The deployment specifically targets arguments "drawn from everyday or quasi-legal scenarios." Abstract fictional-world examples like Size Town or Potterville do not represent the argument types students encounter in practice, though they may still be useful for evaluating logical form comprehension in isolation.
- **Datapoint citations:**
  - [D9] Example 11 (FOLIO, train, False): "Everything in Size Town is big or small. All big things in Size Town are heavy… The bird is in Size Town and it is not both heavy and still." — Entirely abstract fictional world with no real-world referent.
  - [D8] Example 8 (FOLIO, train, Uncertain): "If someone in Potterville yells, then they are not cool… Harry, who lives in Potterville either yells or flies." — Fictional scenario (Harry Potter allusion) with no everyday reasoning context.

---

### Content Coverage Summary

The 57 reviewed examples span a realistic range of multi-step FOL deductive reasoning scenarios, drawn from both Wikipedia-seeded real-world topics (British architects, Australian musicians, aerospace companies, Russian economic policy, astronomy) and template-generated syllogistic chains (watch types, basketball shooting percentages, abstract Size Town). The label distribution in the sample skews toward Uncertain (approximately 55%), with True (~30%) and False (~15%) also present, consistent with the documented test-set distribution.

Topically, the examples cover science, sports, consumer goods, geopolitics, CS/technology, media, everyday social scenarios, and even one example explicitly about Modus Ponens and inductive reasoning. Register is consistently formal written English with care given to grammatical naturalness, though several double-negative or structurally complex NL phrasings were observed.

The FOL annotation layer is dense and uses the full operator inventory (¬, ∧, ∨, →, ⊕, ∀, ∃, =) across examples. However, the sample revealed a non-trivial rate of annotation artifacts: free variables, mismatched parentheses, contradictory NL/FOL pairs, and cross-entity name inconsistencies across 6 of 57 reviewed examples (~10%). These are not concentrated in any single story cluster but appear distributed across the sample.

Critically for the deployment, the dataset contains no propositional-logic-only examples, no implicit-premise cases, no proof traces of any kind, and no countermodel artifacts. The output schema is uniformly a three-way classification label. The FOL notation is Russell & Norvig-style flat predicate logic, with no Fitch-style structural markers, subproof annotations, or inference-rule name vocabulary.

---

### Limitations

1. **Sample size and split coverage:** Only 57 of 1,204 total examples were reviewed, all from the `train` split. The validation split (203 examples) was not sampled. Coverage uncertainty exists for rare story types and edge cases.

2. **Test split unavailability:** The HuggingFace release omits the test split (226 examples), so the reported benchmark performance figures (majority baseline 38.5%, expert accuracy 95.98%) cannot be directly verified against the available data.

3. **HybLogic vs. WikiLogic proportions:** The sample does not allow precise identification of which examples are WikiLogic vs. HybLogic (no `source` field is present in the schema). Differential analysis of implicit-premise style or AST diversity by source pipeline is not possible from the available data.

4. **FOL annotation error rate:** Six annotation artifacts were found in 57 examples. This is a lower bound — other syntactically valid but semantically incorrect annotations may exist and are not detectable without running the inference engine. The true error rate across the full dataset may differ.

5. **Countermodel content:** It is not possible from the data alone to determine whether the inference engine, when applied to False-labeled examples, could generate countermodels as a byproduct. The schema captures only the truth-value label, not any intermediate inference engine output.

6. **P-FOLIO companion dataset:** The web search findings identified P-FOLIO (EMNLP 2024) as a companion dataset with human-written NL proof chains for FOLIO stories. P-FOLIO was not sampled or analyzed here; it may partially address the output-form gap noted above, though it uses narrative NL chains rather than Fitch-style proofs.

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
  "region": "US Undergraduate Logic Students — Introductory and Intermediate Courses",
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
