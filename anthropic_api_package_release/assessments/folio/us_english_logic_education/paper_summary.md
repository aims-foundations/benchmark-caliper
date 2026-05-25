```markdown
# Validity Extraction: FOLIO: Natural Language Reasoning with First-Order Logic
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: FOLIO: Natural Language Reasoning with First-Order Logic
- **Authors**: Not individually named in the registry (see Q21 for collective attribution to "expert annotators")
- **Venue/Year**: Not specified in the registry
- **Total Pages**: 15 (based on highest page number in registry)
- **Quotes Extracted**: 163

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

### 1. Task Taxonomy / Test Case Categories

FOLIO defines two primary tasks: (1) natural language reasoning with first-order logic, where models determine the truth value of conclusions given a set of premises [Q15, Q63], and (2) NL-FOL translation, where natural language stories are converted into their parallel FOL representations [Q18, Q67]. The reasoning task is framed as a central test of logical inference capability [Q7], explicitly distinguished from other forms of reasoning evaluated by existing benchmarks [Q9]. A key differentiator is reasoning depth: the modal depth in FOLIO is four steps, and 28.7% of examples require five or more reasoning steps [Q60], while FOLIO also exhibits substantially greater logical diversity as measured by distinct abstract syntax trees [Q61].

For the experimental scope, the benchmark tests both supervised fine-tuning (using BERT and RoBERTa [Q84]) and few-shot prompting across open-source and proprietary LLMs including LLaMA, GPT-NeoX, GPT-3, GPT-3.5-Turbo, and GPT-4 [Q87, Q88]. Advanced prompting strategies — chain-of-thought, self-consistency, and tree-of-thought — are also evaluated [Q89, Q90], along with methods specifically designed for logical reasoning such as Logic-LM, LINC, and DetermLR [Q91]. The benchmark also examines discourse-level consistency requirements, distinguishing FOLIO's translation task from simpler sentence-level NL-to-FOL translation [Q71, Q72].

From a deployment-validity perspective, **FOLIO's task taxonomy covers deductive FOL reasoning well but presents a moderate coverage gap for the educational platform**. The tool must also handle propositional logic, which FOLIO does not address as a distinct layer, and must support argument reconstruction from natural English with implicit premises [Q3 in elicitation]. While the NL-FOL translation subtask [Q67] partially addresses the natural-language-to-formal-form requirement, FOLIO does not include pedagogical explanation tasks or propositional-only reasoning problems. The benchmark explicitly requires that domain knowledge of FOL is necessary for good performance [Q112], which aligns with the advanced student register but may not reflect the introductory propositional logic register the deployment must also serve.

### 2. Data Sources and Collection

FOLIO comprises 1,430 examples paired with 487 premise sets [Q1], collected through two distinct pipelines totaling approximately 980 man-hours [Q32]. The first pipeline, WikiLogic, uses Wikipedia articles as creative seeds: annotators select random Wikipedia pages and write entirely new reasoning stories from scratch [Q34], yielding 304 stories with 1,353 NL-FOL premise pairs and 753 conclusion pairs [Q58]. This method maximizes topical diversity, accounting for 74% of the total vocabulary despite representing only 63% of the stories [Q62], and produces 53 distinct abstract syntax trees [Q106]. The second pipeline, HybLogic, employs a hybrid approach based on combinations of the 24 valid syllogism types [Q40, Q43], generating logical templates that human annotators then populate with real-world entities [Q42, Q44], yielding 183 stories [Q58] with 33 distinct ASTs [Q106].

The dual-source design is deliberate: it seeks to balance logical diversity with complexity [Q33], addressing the limitations of prior datasets that relied on purely template-based generation [Q14]. However, the Wikipedia seed approach raises a potential data-contamination concern for LLM evaluation — the authors note that LLMs may have seen similar logical patterns during pretraining [Q104], while the template-based HybLogic stories show the inverse pattern in fine-tuning experiments [Q105]. For the educational deployment, the Wikipedia-derived stories offer naturally varied everyday topics that may partially approximate the quasi-legal and everyday argument structures students encounter, though the stories are still written with explicit, formalized FOL premises rather than the implicit-premise style characteristic of student-facing arguments.

### 3. Data Format and Preprocessing

FOLIO is a text-only, English-language dataset using FOL notation consistent with the standard adopted in the AI community [Q52]. Each story consists of n NL premises and m NL conclusions, with parallel FOL annotations for each [Q64, Q65], and NL-FOL pairs are required to be logically and semantically equivalent [Q68]. Stories are created from scratch without templates in the WikiLogic track [Q35], while the HybLogic track uses syllogism-derived templates as scaffolds, explicitly designed so that the template augments rather than constrains linguistic creativity [Q45].

Multiple preprocessing steps ensure linguistic quality: all sentences are checked with Grammarly [Q49], and annotators with English Literature backgrounds conducted thorough naturalness reviews [Q50]. The dataset applies explicit guidelines to resolve natural language ambiguity [Q51], including standardized conventions for inclusive versus exclusive disjunction [Q130, Q131], quantifier phrasing [Q132, Q133], and singular/plural consistency [Q134]. Stories containing opinionated language or identity-linked biases were removed [Q127], and factually inaccurate claims were rewritten [Q126]. For generalization statements, specifiers like "all Dan knows" were added to introduce reasonable factual constraints [Q129]. The dataset is split 70%/15%/15% (train/validation/test) by story to ensure models face unseen stories at evaluation [Q78, Q79].

FOL-specific formatting deserves note: the inference engine required a custom Python parser to convert the human-written FOL syntax into the prover's input format [Q150, Q151, Q153], and properties such as transitivity and symmetry of predicates were explicitly encoded as additional premises [Q56]. This level of formal overhead is specific to the FOL reasoning setting and diverges from the Fitch-style natural deduction notation used in the target curriculum. From an input-form validity standpoint, the text-only English format aligns well with the deployment [IF = LOWER priority], and the readability distribution is documented [Q59, Q154], though the formal FOL annotation layer uses a different syntactic register than the Barwise & Etchemendy textbook conventions the students are trained on.

### 4. Label Categories and Output Types

The ground-truth label set is a three-way classification: **True**, **False**, or **Unknown** [Q36, Q66], with the majority class (True) comprising 87 of 226 test examples, yielding a majority baseline of 38.5% [Q94]. Labels are determined by an FOL inference engine that verifies whether the conclusions follow from, contradict, or are underdetermined by the premises [Q2]. The use of FOL as the representational substrate is motivated by its freedom from natural language ambiguity [Q137] and its capacity to serve as input to a theorem prover to obtain exact truth values [Q136]. The operator inventory includes negation, conjunction, disjunction, implication, universal and existential quantifiers, and equality [Q138], with n-place predicates used where applicable [Q141].

**From an output-ontology standpoint, this label schema is fundamentally misaligned with the deployment's requirements [OO = HIGH priority].** The deployment requires not a truth-value label but structured, rule-justified proof traces differentiated by student register — numbered deduction steps citing specific premises and naming inference rules (e.g., modus ponens), paired with plain-English summaries. FOLIO provides no output schema for explanation structure, countermodel construction, or register-differentiated reasoning presentation. For invalid arguments, the deployment expects a countermodel or counterexample; FOLIO labels these as "False" or "Unknown" but generates no countermodel artifact [Q66]. An additional limitation is that 5% of FOLIO conclusions have complex syntactic structures that challenge even GPT-4 [Q120], and temporal and modal logic are explicitly excluded from the label scope [Q139, Q140], further narrowing coverage relative to the full range of argument types a student might encounter. The FOL operator set also does not include Davidsonian or neo-Davidsonian semantics [Q142], which may be relevant for more expressive argument forms.

### 5. Annotation Process

FOLIO was constructed through a carefully controlled expert annotation process [Q24] requiring annotators to possess both FOL expertise and strong English proficiency [Q27, Q28]. Annotators were either college or graduate students — native speakers or near-native — with formal coursework or self-directed study in first-order logic or semantic parsing [Q122, Q123]. The annotation pipeline is staged: NL quality control is handled by NLP/computational linguistics experts [Q29, Q124], and FOL quality control exclusively by FOL experts [Q29, Q125]. Annotators received multiple training sessions and detailed annotation guidelines [Q30], and all stories were reviewed by senior researchers as well as undergraduate and graduate CS students [Q31].

The annotation protocol for FOL translation was designed to maximize consistency, including rules requiring that FOL formulas preserve the semantics and structure of the NL source as faithfully as possible [Q144, Q145], that semantic decomposition be minimized [Q146], and that tense be neglected while plural verb forms are removed [Q147]. A preliminary investigation found systematic FOL consistency issues in human-written formulas, prompting an additional quality control round [Q53, Q54]. Commonsense knowledge implicit in NL premises but required for FOL proofs was explicitly added as auxiliary premises [Q55]. The total annotation screening identified that 39.2% of stories required rewriting to address quality issues [Q48].

Human performance was benchmarked separately: expert annotators (CS students familiar with FOL) achieved 95.98% accuracy on the test set, while non-experts (community college or high school students without prior logic training) achieved only 61.82% [Q107, Q108, Q109, Q111]. Both groups were native English speakers [Q110]. This 34-point accuracy gap [Q111] confirms the FOL expertise requirement and is directly relevant to deployment: introductory students are likely to perform closer to the non-expert ceiling without tool assistance. The FOL inference engine was used to verify syntactic validity and label consistency of all FOL annotations [Q57]. Notably, the annotation protocol was designed to avoid biases linked to race, ethnicity, gender, sexuality, nationality, class, and religion [Q47], though the annotator pool itself is described at a high level without detailed demographic breakdown.

### 6. Evaluation Metrics and Output Modality

For the primary reasoning task, accuracy against the engine-verified three-way label is the sole metric [Q80]. For NL-FOL translation, two metrics are used: Syntactic Validity (SynV), a binary score checking whether all FOL formulas in a story pass a syntactic check [Q73, Q74], and Execution Accuracy (ExcAcc), measuring whether the translated FOL story, when fed to the inference engine, produces the correct truth values [Q75, Q76]. Results are averaged over five randomly sampled training-set example sets [Q93].

Key empirical findings include: GPT-3.5-Turbo and GPT-4 achieve ~93% syntactic validity on NL-FOL translation [Q96], but execution accuracy remains low [Q97], indicating a gap between surface-level FOL fluency and semantic fidelity. Models perform substantially worse on examples with 4–7 reasoning depths than on 0–3 depth examples [Q99], and the gap between GPT-4 and expert human performance is 31.82 percentage points [Q113]. Error analysis reveals that in ~65% of cases, models fail to construct accurate reasoning chains for complex multi-step problems [Q118]; in ~25% of cases, individual reasoning steps contain erroneous derivations [Q119]; and in ~5% of cases, models exploit commonsense shortcuts to reach wrong conclusions [Q121]. Confusion matrices show models disproportionately predict "True," with False and Unknown conclusions achieving only 61.9% accuracy under fine-tuning and 54.0% under few-shot prompting [Q155, Q156, Q157]. Premise shuffling has minimal impact (~1% accuracy change), confirming that premise ordering is not a spurious correlate [Q158, Q159].

**From an output-form validity standpoint, these metrics are entirely misaligned with the deployment's required outputs [OF = HIGH priority].** The benchmark's accuracy metric evaluates label prediction; the deployment requires evaluation of step-by-step proof traces, citation of premises, correct inference-rule naming, and register appropriateness. No metric in FOLIO assesses whether a model's reasoning trace is pedagogically clear, Fitch-style compliant, or appropriately differentiated for introductory versus advanced students. The authors themselves note the need for a more reliable NL-FOL translation metric [Q77], and the evaluation infrastructure (a custom FOL parser and a Stanford CS221 inference engine [Q148, Q149, Q150]) is purpose-built for label verification rather than explanation quality assessment. A custom FOL parser was necessary because the inference engine does not natively support the standard FOL syntax used in the dataset [Q149], further illustrating the distance between FOLIO's formal apparatus and the Fitch-style notation the target curriculum employs.

### 7. Stated Limitations

The authors acknowledge several limitations with direct bearing on the deployment. First, FOLIO is explicitly scoped to FOL and excludes temporal logic and modal logic as "special-purpose logics" beyond the dataset's definitional scope [Q139, Q140] — this is a moderate gap for the deployment, which must handle propositional logic as a distinct layer. Second, FOLIO's NL-FOL translation metric is acknowledged as insufficient, with the authors calling for future work on a more reliable translation metric [Q77]. Third, the dataset's scale is constrained by the resource-intensive annotation process: the authors acknowledge that significantly scaling up would exceed available resources, and they explicitly invite the community to expand the dataset using their protocol [Q116, Q117].

The dataset also accepts certain "psychologically fundamental generalizations" that may not be factually invariant (e.g., "Tigers eat other animals") as a deliberate design choice that introduces semantic nuance [Q128], which could introduce reasoning edge cases. The HybLogic subset presents near-chance performance for state-of-the-art LLMs in few-shot settings [Q20], and the authors hypothesize this reflects the logical complexity of syllogistic chains rather than data artifacts [Q103]. The limitations of existing benchmarks that motivated FOLIO's creation are also documented: prior datasets such as RuleTaker and LogicNLI had shallow reasoning depths (max five), fewer than 50 distinct ASTs, and highly restricted vocabularies [Q11, Q12, Q13], and none were written by humans with real-world knowledge [Q14]. The authors' prioritization of quality over quantity [Q114] means that fine-tuning experiments cannot adequately probe how dataset size affects performance [Q116]. Finally, the NL-FOL translation metric's reliance on an inference engine that required custom conversion tooling [Q152] limits the reproducibility and generalizability of the translation evaluation, and the use of LLMs for this conversion step is flagged as unreliable [Q152].

### 8. Authors and Affiliations

NOT FULLY DOCUMENTED: The registry contains only a single quote attributing the dataset to "expert annotators" without naming individual authors or their institutional affiliations [Q21]. The annotation team is described as comprising CS undergraduate and graduate students and senior researchers in academia and industry [Q16, Q31], but specific universities, companies, or countries of affiliation are not identified in any quoted passage. This absence is itself a validity-relevant finding: without knowing the institutional and geographic origins of the authors and annotators, it is difficult to assess whether the benchmark's design choices, example topics, or linguistic norms reflect a US educational context or another academic tradition. The annotator pool's use of native or near-native English speakers [Q27] and the Wikipedia-seeded content [Q34] suggest a broadly Anglophone academic origin, but sub-national or institutional specificity — relevant for assessing alignment with US undergraduate logic pedagogy — cannot be confirmed from the available quotes.
```

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | data_sources | "FOLIO consists of 1,430 examples (unique conclusions), each paired with one of 487 sets of premises used to deductively reason for the validity of each conclusion." |
| Q2 | 1 | label_categories | "The logical correctness of the premises and conclusions is ensured by their FOL annotations, which are automatically verified by an FOL inference engine." |
| Q3 | 1 | task_taxonomy | "In addition to the main NL reasoning task, NL-FOL pairs in FOLIO constitute a new NL-FOL translation dataset." |
| Q4 | 1 | evaluation_metrics | "Our experiments on FOLIO systematically evaluate the FOL reasoning ability of supervised fine-tuning on medium-sized language models." |
| Q5 | 1 | evaluation_metrics | "For both NL reasoning and NL-FOL translation, we benchmark multiple state-of-the-art language models." |
| Q6 | 1 | evaluation_metrics | "Our results show that a subset of FOLIO presents a challenge for one of the most capable Large Language Model (LLM) publicly available, GPT-4." |
| Q7 | 1 | task_taxonomy | "Logical reasoning is a central component for intelligent systems and should be sufficiently and independently evaluated (Russell and Norvig, 2010)." |
| Q8 | 1 | stated_limitations | "However, existing natural language tasks are inadequate in measuring the complex logical reasoning capability of a model (Srivastava et al., 2023; Saparov and He, 2023; Tian et al., 2021)." |
| Q9 | 1 | stated_limitations | "Some of these common benchmarks do not specifically evaluate logical reasoning independently of other forms of reasoning (Yu et al., 2020; Liu et al., 2021)." |
| Q10 | 1 | stated_limitations | "Those specifically designed for measuring logical reasoning are insufficient in terms of logical reasoning complexity and natural language variety." |
| Q11 | 1 | stated_limitations | "Examples in RuleTaker (Clark et al., 2020) and LogicNLI (Tian et al., 2021) need at most five depths of reasoning." |
| Q12 | 1 | stated_limitations | "The entire corpus of RuleTaker or LogicNLI has fewer than 50 distinct abstract syntax trees." |
| Q13 | 1 | stated_limitations | "RuleTaker has only 101 words in its vocabulary and LogicNLI has 1077 words in the vocabulary." |
| Q14 | 1 | stated_limitations | "Moreover, none of them are written by humans with information drawn from real-world knowledge, making them less applicable to real-world reasoning scenarios." |
| Q15 | 1 | task_taxonomy | "We present a natural language reasoning dataset, FOLIO, with first-order logic reasoning problems which require the models to decide the correctness of conclusions given a world defined by the premises." |
| Q16 | 2 | annotation_process | "FOLIO is a high-quality and manually curated dataset, written by CS undergraduate and graduate students and researchers in academia and industry." |
| Q17 | 2 | annotation_process | "To ensure the conclusions of our examples follow the premises logically, we annotated all reasoning examples with first-order logic (FOL) formulas." |
| Q18 | 2 | task_taxonomy | "Based on our annotations, we propose a new NL-FOL translation task where an NL reasoning example is translated into its FOL counterpart." |
| Q19 | 2 | evaluation_metrics | "Finally, we benchmark the performance of strong LMs in both fully supervised and few-shot settings to understand their capabilities in logical reasoning (i.e., deriving the truth value of a logical conclusion from NL premises)." |
| Q20 | 2 | stated_limitations | "Under the few-shot setting, the most capable publicly available LLM so far achieves only 53.1% on the stories written in a hybrid manner, which is slightly better than random." |
| Q21 | 2 | authors_affiliations | "We release a natural language reasoning dataset written by expert annotators, FOLIO, with first-order logical reasoning problems." |
| Q22 | 2 | data_format | "We use formal logic, i.e., FOL to ensure the logical validity of the examples written in NL and propose a new NL-FOL translation task." |
| Q23 | 2 | evaluation_metrics | "We benchmark the performance of LMs by fine-tuning models and prompting LLMs with few-shot examples, on the FOLIO reasoning task." |
| Q24 | 3 | annotation_process | "We collected FOLIO through a carefully designed manual annotation process to achieve high-quality examples that necessitate complex logical reasoning." |
| Q25 | 3 | annotation_process | "Writing natural language reasoning stories with FOL requires sufficient knowledge in both semantic parsing and first-order logic, as well as strong analytical skills." |
| Q26 | 3 | annotation_process | "Given the complexities of such annotations, we selected annotators based on a few important criteria to ensures that our dataset is annotated with the highest level of precision and expertise, reflecting the complexity and nuance required for first-order logical reasoning." |
| Q27 | 3 | annotation_process | "Our annotators are either college or graduate students who are native English speakers or possess near-native proficiency in English." |
| Q28 | 3 | annotation_process | "They possess formal education in first-order logic, having either completed relevant coursework or undertaken self-directed studies in first-order logic or seman-" |
| Q29 | 4 | annotation_process | "At the NL quality check stage, only annotators who are experts in natural language processing or computational linguistics are involved. For the FOL quality check, only annotators who are experts in first-order logic are involved." |
| Q30 | 4 | annotation_process | "We also give the annotators several training sessions on how to write a story, by providing them with detailed annotation guidelines." |
| Q31 | 4 | annotation_process | "All stories and FOL annotations in FOLIO are written and reviewed by expert annotators, including CS undergraduate and graduate students, and senior researchers, who met the aforementioned criteria." |
| Q32 | 4 | data_sources | "We develop our dataset in six stages: WikiLogic collection, HybLogic collection, NL quality control, FOL quality control, NL-FOL alignment and FOL verification, spending 980 man-hours in total." |
| Q33 | 4 | data_sources | "We collected our dataset using two different methods in order to obtain examples that are both logically diverse and complex and have abundant abstract syntax tree (AST) variations." |
| Q34 | 4 | data_sources | "WikiLogic: annotation from scratch using Wikipedia articles as seeds. At this annotation stage, the annotators are asked to select random Wikipedia pages by repeatedly using the Wikipedia Special Random link. The Wikipedia articles are used to develop ideas for topics to write new stories." |
| Q35 | 4 | data_format | "We ask the annotators to create new stories from scratch without using templates based on real-world knowledge, which should be plausible in general." |
| Q36 | 4 | label_categories | "Each of the stories is composed of several premises and conclusions with truth values of True, False, or Unknown (see Table 2 for an example)." |
| Q37 | 4 | data_format | "We also ask the annotators to write parallel FOL sentences for both the premises and conclusions." |
| Q38 | 4 | data_sources | "This results in a wide range of topics, abundant AST variations, and a wide vocabulary for FOLIO." |
| Q39 | 4 | data_sources | "HybLogic: hybrid annotation The task of generating logically sound stories from scratch for a set of facts is very time-consuming for human writers, where the main challenge is to create complex and varied logical patterns to arrive at a conclusion." |
| Q40 | 4 | data_sources | "To address the problems of solely using manual annotation, we also consider a hybrid approach to facilitate the process. Our hybrid method is based on a common form of logical stories: syllogisms." |
| Q41 | 4 | task_taxonomy | "A syllogism consists of two premises and a single conclusion, and the conclusion states some facts about the entities and categories in the premises." |
| Q42 | 4 | data_sources | "In this approach, we first generate logically valid stories, which are templates containing abstract categories and entities, by combining multiple syllogisms into a single story template: the conclusion of one syllogism is used as a premise for the next syllogism." |
| Q43 | 4 | task_taxonomy | "There are 256 logically distinct types of syllogisms and 24 of them are valid (Lehman, 1973). We use various combinations of 24 valid syllogisms. We also add in conjunction, disjunction, and implication." |
| Q44 | 4 | annotation_process | "We then ask human annotators to assign nouns, phrases, or clauses to the abstract entities or categories that reflect real-life scenarios to each template and write logically-valid stories in natural language." |
| Q45 | 4 | data_format | "The usage of the template is to ensure that we have a set of varied and complex logical stories with multiple conclusions. There are many ways of expressing the same logic template in natural language, and so the generated templates augment, rather than limit, the creativity of humans." |
| Q46 | 4 | annotation_process | "To ensure the highest quality of the dataset, we dedicated considerable attention to the following key aspects of the natural language sentences during the quality control process." |
| Q47 | 4 | stated_limitations | "Our dataset prioritizes realism and factual accuracy, steering clear of biases and stereotypes linked to identity markers like race, ethnicity, gender, sexuality, nationality, class, and religion." |
| Q48 | 4 | annotation_process | "Toward these objectives, we manually screened all stories and found that 39.2% of the stories suffer from at least one of these issues. We implemented a detailed protocol to rewrite these stories." |
| Q49 | 4 | data_format | "Apart from grammar, we make sure the sentences in our dataset are highly natural. All the sentences are first checked with a grammar checking tool, Grammarly." |
| Q50 | 4 | annotation_process | "Our annotators who have graduated from or are senior students studying English Literature conducted a thorough round of review for grammatical correctness and language naturalness." |
| Q51 | 4 | data_format | "We also eliminate natural language ambiguity when it is possible." |
| Q52 | 5 | data_format | "We adopt the FOL definitions and syntax most widely used in the AI community (Russell and Norvig, 2010)." |
| Q53 | 5 | annotation_process | "In preliminary investigations, we found that the human-written FOL formulas suffer from FOL consistency issues, which necessitates an additional round of quality control for FOL formulas." |
| Q54 | 5 | annotation_process | "One NL sentence can be translated into FOL through multiple non-equivalent ways. For example, sometimes additional information inferred from a sentence can be represented in FOL, leading to multiple representations. We therefore design an annotation protocol for FOL translation in order to ensure that our FOL translations are as consistent as possible across all examples in our dataset." |
| Q55 | 5 | annotation_process | "Apart from checking whether NL and FOL express equivalent meanings, we also add necessary commonsense knowledge in both the NL and FOL premises. Sometimes humans do not write certain commonsense knowledge in the premises that is required in the FOL reasoning process, which is based solely on the premises given. We add such knowledge as additional premises at this stage." |
| Q56 | 5 | data_format | "In particular, intrinsic properties of some predicates are required in the FOL reasoning process. For example, "LocatedIn(x,y)" should be transitive and "BeFamily(x,y)" should be symmetric." |
| Q57 | 5 | annotation_process | "Recognizing that the FOL formula annotations can be error-prone, we verify the syntactic validity and label consistency of FOL formula annotations with an FOL inference engine." |
| Q58 | 5 | data_sources | "Table 3 shows that examples based on Wikipedia make up the largest portion of FOLIO, with 304 stories, 1,353 NL and FOL premise pairs, and 753 NL and FOL conclusion pairs. Hybrid annotations consist of 183 stories with 1,054 NL and FOL premise pairs, and 682 NL and FOL conclusion pairs in total." |
| Q59 | 5 | evaluation_metrics | "We use the Dale-Chall Readability Formula (Dale and Chall, 1948, 1995) to show the text complexity of FOLIO following (Singh et al., 2023; Arps et al., 2022; Wei et al., 2021)." |
| Q60 | 5 | task_taxonomy | "As shown in Figure 1, the mode of reasoning depths is four in FOLIO. 28.7% of the examples need five or more depths of reasoning to infer the conclusions, while the previous datasets needed at most five reasoning depths as shown in Table 1." |
| Q61 | 5 | task_taxonomy | "Table 1 shows that FOLIO also has a much larger number of distinct ASTs than the previous datasets, indicating that FOLIO is much more logically diverse." |
| Q62 | 5 | data_sources | "Table 3 shows that our dataset has a vocabulary of 4,351 words, and the examples based on Wikipedia account for 74% of the total vocabulary even though the WikiLogic stories take up only 63% of the total number of stories." |
| Q63 | 6 | task_taxonomy | "We define two new tasks based on FOLIO, natural language reasoning with first-order logic and NL-FOL translation." |
| Q64 | 6 | data_format | "Each natural language (NL) story S in FOLIO consists of n premises: P = {p1, p2, ..., pn} and m conclusions: H = {h1, h2, ..., hm}." |
| Q65 | 6 | data_format | "All NL stories are annotated with parallel FOL stories SF, which are sets of FOL formulas consisting of n premises PF = {pf1, pf2, ..., pfn} and m conclusions HF = {hf1, hf2, ..., hfm}." |
| Q66 | 6 | label_categories | "Given P and H, the goal is to determine the truth values of the conclusions: "True", "False" or "Unknown", based on FOL reasoning." |
| Q67 | 6 | task_taxonomy | "We propose a new natural language to first-order logic translation (NL-FOL translation) task alongside our reasoning dataset." |
| Q68 | 6 | data_format | "In particular, each of the NL sentence pi or hi and the parallel FOL formula pfi or hfi should be logically and semantically equivalent." |
| Q69 | 6 | data_format | "Moreover, the truth values for the conclusions should be the same based on the NL story S and the parallel FOL story FS." |
| Q70 | 6 | data_format | "In our dataset, the premises and conclusions are set up in such a way to ensure that the inference engine always returns an answer given enough resources such as time and memory." |
| Q71 | 6 | task_taxonomy | "Unlike previous work (Singh et al., 2020) which translates problems with a single premise and a single hypothesis, our task is on translating examples of various lengths with a focus on stories with multiple premises." |
| Q72 | 6 | task_taxonomy | "Thus, it also requires the models to consider discourse-level consistencies as opposed to translation at the sentence level." |
| Q73 | 6 | evaluation_metrics | "Two metrics are adopted to evaluate NL-FOL translation to capture different aspects of the generation results: 1). Syntactic validity (SynV)." |
| Q74 | 6 | evaluation_metrics | "The Syntactic Validity score measures whether the FOL formulas are syntactically valid. The score will be 1 if all FOL formulas of an example can pass the syntactic check and 0 otherwise 2)." |
| Q75 | 6 | evaluation_metrics | "Inference Engine execution accuracy (ExcAcc). The group of translated FOL for premises and conclusions in one story is fed into our inference engine to output the truth value for each conclusion." |
| Q76 | 6 | evaluation_metrics | "We define the accuracy of the output labels as the execution accuracy." |
| Q77 | 6 | stated_limitations | "We leave for future work the design of a more reliable metric of NL-FOL translation." |
| Q78 | 6 | data_format | "We split FOLIO by 70%/15%/15% split for the train/validation/test sets with 1,001/203/226 examples respectively." |
| Q79 | 6 | data_format | "We split by story so that models are evaluated on unseen stories." |
| Q80 | 6 | evaluation_metrics | "We use accuracy for evaluating logical reasoning performance." |
| Q81 | 6 | evaluation_metrics | "For NL-FOL translation, we use the metrics in Section 4.2." |
| Q82 | 6 | task_taxonomy | "We test the logical reasoning capabilities of LMs using fully supervised fine-tuning and few-shot prompting." |
| Q83 | 6 | task_taxonomy | "We also test NL-FOL translation with few-shot prompting." |
| Q84 | 7 | task_taxonomy | "As fine-tuning baselines, we experiment with BERT (Devlin et al., 2019), and RoBERTa (Liu et al., 2020)." |
| Q85 | 7 | data_format | "We fine-tune the base and large versions of both BERT and RoBERTa, with an additional two-layer classification layer to predict the truth values." |
| Q86 | 7 | task_taxonomy | "For the second task, i.e., NL-FOL translation, we only report few-shot prompting methods." |
| Q87 | 7 | task_taxonomy | "We conduct zero-shot and few-shot prompting experiments on larger LMs with few-shot capabilities." |
| Q88 | 7 | task_taxonomy | "For open-source models, we test LLaMA-13B and LLaMA-70B (Touvron et al., 2023), GPT-NeoX-20B (Black et al., 2022); for proprietary models we test GPT-3 (Brown et al., 2020), GPT-3.5-Turbo and GPT-4 (OpenAI et al., 2023) using prompts with 8 examples." |
| Q89 | 7 | task_taxonomy | "We experiment with incorporating recent prompting strategies into GPT-4 as they have shown improvements in the general reasoning performance of LLMs." |
| Q90 | 7 | task_taxonomy | "The prompting strategies include chain-of-thought (CoT) prompting (Wei et al., 2022b), chain-of-thought prompting with self-consistency (Wang et al., 2023) and tree-of-thought prompting (Yao et al., 2023)." |
| Q91 | 7 | task_taxonomy | "We also test recent methods specifically designed for logical reasoning: Logic-LM (2023), LINC (Olausson et al., 2023) and DetermLR(Sun et al., 2023), using GPT-4 as the base model." |
| Q92 | 7 | data_format | "For the second task (NL-FOL translation), we use the same examples as in the Few-Shot NL experiments except that all the conclusions are included in each example." |
| Q93 | 7 | evaluation_metrics | "We run experiments on five randomly sampled sets of examples from the training set and report the average accuracy." |
| Q94 | 7 | label_categories | "The majority baseline of our dataset is 38.5% since in our test set, there are 87, 78 and 61 examples with labels of true, false and unknown respectively." |
| Q95 | 7 | stated_limitations | "In experimenting with different prompts, we found 8 shot examples to perform slightly better. It is also the maximum number of examples that fits in the text-davinci-002 context." |
| Q96 | 8 | evaluation_metrics | "Table 5 shows the results of NL-FOL translation. The syntactic validity scores are around 93% with both GPT-3.5-Turbo and GPT-4. This indicates that language models with sufficient scales are good at picking up the patterns for FOL formulas and generating syntactically valid FOL formulas." |
| Q97 | 8 | stated_limitations | "However, GPT-3.5-Turbo and GPT-4 are not yet good at translating an NL story to a logically or semantically similar FOL counterpart, as indicated by the low inference engine execution accuracy score." |
| Q98 | 8 | task_taxonomy | "Below we provide analysis of our results and key findings, providing additional insights into our dataset FOLIO and the current capabilities of LLMs in logical reasoning." |
| Q99 | 8 | evaluation_metrics | "With few-shot prompting, GPT-3.5 and GPT-4 both perform much better on examples with a 0 ∼ 3 reasoning depth, indicating that examples with a 4 ∼ 7 reasoning depth pose a challenge to the SoTA LMs." |
| Q100 | 8 | evaluation_metrics | "This indicates that fine-tuning on longer and more difficult reasoning chains in the training set can improve model performance on equally-long test example chains." |
| Q101 | 8 | stated_limitations | "FOLIO's unique complexity reveals that current LMs are limited in their ability to extrapolate to longer and more complex reasoning chains, and suggests an avenue for further study." |
| Q102 | 8 | evaluation_metrics | "As shown in Table 6, in logical reasoning, GPT-3.5 and GPT-4 achieve substantially lower results on HybLogic than on WikiLogic and the result is slightly higher than chance." |
| Q103 | 8 | stated_limitations | "We hypothesize that this is because HybLogic has high logical complexity that the SoTA LLMs like GPT-4 cannot solve yet while WikiLogic examples require shorter reasoning chains which the model is already capable of solving." |
| Q104 | 8 | data_sources | "Moreover, since the examples in WikiLogic are created from scratch by humans, it is possible that LLMs have seen similar texts with similar logical patterns in the training data." |
| Q105 | 8 | data_sources | "However, fine-tuning RoBERTa-large achieves higher performance on HybLogic than on WikiLogic. This is likely because HybLogic is created from templates and some of the logical patterns can be learned during fine-tuning." |
| Q106 | 8 | data_format | "In NL-FOL translation, performs 10 points better on HybLogic than WikiLogic. This could be because WikiLogic has more distinct and diverse sentence-level logical and language patterns and FOL annotations. WikiLogic has 53 ASTs while HybLogic has 33." |
| Q107 | 9 | annotation_process | "We collected truth value annotations of logical reasoning for FOLIO test set from expert and non-expert annotators." |
| Q108 | 9 | annotation_process | "Our expert annotators are computer science college students familiar with FOL." |
| Q109 | 9 | annotation_process | "Non-expert annotators are community college or high school students who have not taken the SAT." |
| Q110 | 9 | annotation_process | "Both expert and non-expert annotators are native English speakers." |
| Q111 | 9 | evaluation_metrics | "Expert annotations achieve an accuracy of 95.98% while non-expert annotations achieves 61.82%, with a gap of 34.16%." |
| Q112 | 9 | task_taxonomy | "This shows that sufficient domain knowledge of FOL is necessary for good performance on FOLIO." |
| Q113 | 9 | evaluation_metrics | "The expert and GPT-4 gap is 31.82%, suggesting significant room for model improvement." |
| Q114 | 9 | stated_limitations | "We focus on collecting a very high-quality dataset in evaluating logical reasoning rather than merely a large dataset." |
| Q115 | 9 | annotation_process | "Optimizing for quality required us to adopt a rigorous annotation process with domain experts selected based on a few important criteria as mentioned in Appendix A: Annotator Selection." |
| Q116 | 9 | stated_limitations | "Significantly scaling up this process would have required resources beyond our current means and we are unable further expand our dataset for investigating how the size of training data affects the performance of fine-tuning experiments." |
| Q117 | 9 | stated_limitations | "We encourage the community to apply our annotation protocol to expand this realistic and complex FOL reasoning story set." |
| Q118 | 9 | evaluation_metrics | "Approximately 65% of the time, the model struggles to construct accurate reasoning chains for complex problems with intricate steps, leading to faulty reasoning paths and indicating a limited ability to solve problems with long reasoning chains." |
| Q119 | 9 | evaluation_metrics | "In 25% of cases, erroneous derivations occur within certain reasoning steps, highlighting potential inaccuracies and flaws in logical deductions." |
| Q120 | 9 | label_categories | "5% of conclusions in FOLIO have a complex syntactic structure, posing comprehension challenges for GPT-4." |
| Q121 | 9 | evaluation_metrics | "5% of outputs show that GPT-4 leverage commonsense reasoning to employ spurious shortcuts that lead to the wrong truth value for the conclusion." |
| Q122 | 12 | annotation_process | "Given the complexities of our annotations, we selected annotators based on a few important criteria 1). Our annotators are either college or graduate students who are native English speakers or possess near-native proficiency in English." |
| Q123 | 12 | annotation_process | "They possess formal education in first-order logic, having either completed relevant coursework or undertaken self-directed studies in first-order logic or semantic parsing." |
| Q124 | 12 | annotation_process | "At the NL quality check stage, only annotators who are experts in natural language processing or computational linguistics are involved." |
| Q125 | 12 | annotation_process | "For the FOL quality check, only annotators who are experts in first-order logic are involved." |
| Q126 | 13 | data_format | "We rewrote those that are not reflective of well-established scientific, historical, or legal facts." |
| Q127 | 13 | data_format | "We took out stories that had strongly opinionated language and contained gender, racial, and classist biases." |
| Q128 | 13 | stated_limitations | "We accept certain classes of "psychologically fundamental generalizations" (Leslie, 2008), however, such as "Covid is transmitted through the air" or "Tigers eat other animals," that may not be factually invariant but add logical and semantic nuances to the stories." |
| Q129 | 13 | data_format | "For stories that pertain to generalization, such as "All As are Bs," we have added specifiers like "all Dan knows" to give a degree of reasonable factuality." |
| Q130 | 13 | data_format | "We always use "either-or" to express exclusive disjunction." |
| Q131 | 13 | data_format | "We use either "A or B" or "A or B, or both" to express inclusive disjunction." |
| Q132 | 13 | data_format | "It is more natural to say "Some A is B" rather than "there exists an A such that A is B."" |
| Q133 | 13 | data_format | ""All A are B" can be more natural than "If A then B"." |
| Q134 | 13 | data_format | "Other common issues in NL quality include singular/plural issues, especially in statements that deal with both categories and individual members of those categories; as well as ambiguities resulting from improper introduction of, or failure to introduce, proper nouns." |
| Q135 | 13 | label_categories | "FOL enables deriving facts from other facts (Russell and Norvig, 2010)." |
| Q136 | 13 | label_categories | "FOL, as a logical form, is a more explicit logical representation than its NL counterpart and can be used as input to an FOL prover in order to obtain the exact truth values for the conclusions." |
| Q137 | 13 | label_categories | "FOL has no ambiguity while ambiguity can occur at various levels of NLP." |
| Q138 | 13 | label_categories | "We include the following operators: negation ¬, conjunction ∧, disjunction ∨, implication →, universal quantifier ∀, existential quantifier ∃, equal =." |
| Q139 | 13 | stated_limitations | "Following (Russell and Norvig, 2010), we consider temporal logic and modal logic as special-purpose logics." |
| Q140 | 13 | stated_limitations | "Consequently, they are beyond the scope of the definition of first-order logic used in our dataset." |
| Q141 | 13 | label_categories | "We use n-place predicates when applicable for the expressivity of the FOL formulas." |
| Q142 | 13 | stated_limitations | "However, we do not use the Davidsonian (Davidson, 2001) or neo-Davidsonian semantics (Parsons, 1990) because translating the majority of the FOL formulas in our dataset only requires one-place and two-place predicates." |
| Q143 | 14 | annotation_process | "We therefore design an annotation protocol for first-order logic translation in order to ensure that our FOL translations are as consistent as possible across all examples in our dataset." |
| Q144 | 14 | annotation_process | "First-order logic formulas need to preserve as much as possible the semantics of natural language sentences." |
| Q145 | 14 | annotation_process | "First-order logic formulas should stay as faithful to the structure of the original NL sentence as possible." |
| Q146 | 14 | annotation_process | "Semantic decomposition is not needed unless necessary for maintaining the NL expressivity." |
| Q147 | 14 | annotation_process | "In terms of abstraction, we neglect tense and remove all the plural forms of verbs." |
| Q148 | 14 | evaluation_metrics | "Although there are many provers widely used in the community (McCune, 2005–2010; Sutcliffe, 2017; Nipkow et al., 2002), we adopt the inference engine provided in the Stanford CS221 course page, which is a compact module designed specifically for procesing first-order logic statements." |
| Q149 | 14 | evaluation_metrics | "The inference engine does not support input in the FOL syntax adopted by standard education material (Russell and Norvig, 2010), which is used in our dataset." |
| Q150 | 14 | evaluation_metrics | "We therefore developed a FOL parser in order to convert the FOL formulas written by humans to the input format of the inference engine." |
| Q151 | 14 | evaluation_metrics | "The converter is a semantic parser tool written in Python." |
| Q152 | 14 | stated_limitations | "Although LLMs such as GPT-4 can be utilized to conduct the conversion, it is hard to ensure the GPT-4 outputs are always correct." |
| Q153 | 14 | evaluation_metrics | "Proving a story requires three steps. First, the FOL statements of the premises and conclusions of a story annotated by humans are converted to Python code. Then, the code snippets are used as input to the theorem prover. Finally, the theorem prover outputs whether the conclusions are True / False / Unknown, based on the premises." |
| Q154 | 14 | data_format | "We show the distribution of readability in Figure 3." |
| Q155 | 15 | evaluation_metrics | "Confusion matrices in Figure 4 for the fine-tuning and 8-shot NL prompt results both show that LLMs are significantly better at making the correct predictions for conclusions with labels of True than the conclusions with labels of False or Unknown." |
| Q156 | 15 | evaluation_metrics | "The accuracy on examples with False or Unknown conclusions is 61.9% with fine-tuning and 54.0% with few-shot prompting." |
| Q157 | 15 | evaluation_metrics | "They also tend to make more predictions of True than the other labels." |
| Q158 | 15 | evaluation_metrics | "To test if the premise ordering in FOLIO has spurious correlations with the conclusion label which a model can exploit, we shuffle the input premises to evaluate models." |
| Q159 | 15 | evaluation_metrics | "We find that accuracy increases or decreases by roughly 1% in most settings compared to our unshuffled premises." |
| Q160 | 15 | stated_limitations | "This indicates that the ordering of premises in FOLIO examples does not yield significant information about the label, and thus models will not be able to use the premise ordering as a strong heuristic or statistical feature for its predictions." |
| Q161 | 15 | data_format | "FOL formulas have a clearer and more straightforward logical structure than NL sentences." |
| Q162 | 15 | evaluation_metrics | "As shown in Table 11, the performance slightly increases in the NL+FOL setting for GPT-4 while GPT-3.5 performs worse in both the NL+FOL and the FOL-only settings." |
| Q163 | 15 | evaluation_metrics | "FOL always serves as additional useful information for GPT-4, but not for GPT-3.5 regardless of whether FOL is concatenated with NL." |

### Category Index
- **task_taxonomy**: Q3, Q7, Q15, Q18, Q41, Q43, Q60, Q61, Q63, Q67, Q71, Q72, Q82, Q83, Q84, Q86, Q87, Q88, Q89, Q90, Q91, Q98, Q112
- **data_sources**: Q1, Q32, Q33, Q34, Q38, Q39, Q40, Q42, Q58, Q62, Q104, Q105
- **data_format**: Q22, Q35, Q37, Q45, Q49, Q51, Q52, Q56, Q64, Q65, Q68, Q69, Q70, Q78, Q79, Q85, Q92, Q106, Q126, Q127, Q129, Q130, Q131, Q132, Q133, Q134, Q154, Q161
- **label_categories**: Q2, Q36, Q66, Q94, Q120, Q135, Q136, Q137, Q138, Q141
- **annotation_process**: Q16, Q17, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q44, Q46, Q48, Q50, Q53, Q54, Q55, Q57, Q107, Q108, Q109, Q110, Q115, Q122, Q123, Q124, Q125, Q143, Q144, Q145, Q146, Q147
- **evaluation_metrics**: Q4, Q5, Q6, Q19, Q23, Q59, Q73, Q74, Q75, Q76, Q80, Q81, Q93, Q96, Q99, Q100, Q102, Q111, Q113, Q118, Q119, Q121, Q148, Q149, Q150, Q151, Q153, Q155, Q156, Q157, Q158, Q159, Q162, Q163
- **stated_limitations**: Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q20, Q47, Q77, Q95, Q97, Q101, Q103, Q114, Q116, Q117, Q128, Q139, Q140, Q142, Q152, Q160
- **authors_affiliations**: Q21
