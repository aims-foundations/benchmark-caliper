I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **MRBench – A Benchmark for Evaluating AI Tutor Responses in Student Mistake Remediation** is valid for use in **Indian Metropolitan Grade 1–8 Mathematics Teachers (Delhi & Mumbai)**.

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

- **Name**: mrbench
- **Full Name**: MRBench – A Benchmark for Evaluating AI Tutor Responses in Student Mistake Remediation
- **Domain**: Pedagogical quality evaluation of AI tutor responses in educational dialogue
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### 1. Input Ontology
MRBench defines a specific and narrow task taxonomy: educational dialogues in
mathematics in which the student's most recent utterance contains a mistake or
confusion, and the benchmark evaluates the appropriateness of the AI tutor's next
response [Q12, Q13, Q14]. The eight pedagogical dimensions — active learning,
student-goal adaptation, cognitive-load management, motivation, mistake
identification, answer non-revelation, guidance provision, actionability, logical
coherence, tutor tone, and human-likeness — were derived through iterative analysis
from learning science principles and validated by pilot annotation [Q1, Q15, Q129].
Candidate dimensions such as grammaticality and empathy were explicitly excluded
after the validation pilot confirmed the eight retained dimensions are both necessary
and sufficient for this task [Q131, Q132]. The taxonomy is restricted to mistake
remediation in mathematics and would require verification or adaptation for other
tasks (e.g., concept learning) or other subjects [Q117, Q118, Q130]. Coverage
spans two mathematical difficulty levels — elementary operations (Bridge) and
middle-school reasoning (MathDial) — providing a mix of easy and challenging
problems [Q143, Q144]. The taxonomy makes no reference to any specific national
curriculum; it is curriculum-agnostic by construction [Q111, Q112]. No
domain-specific subcategories reflect Indian curriculum topics (e.g., Indian
place-value conventions, NCERT/CBSE problem types).

### 2. Input Content
MRBench is assembled from two existing English-language datasets: Bridge [Q44]
and MathDial [Q48], both containing real educational dialogues in mathematics
grounded in student errors or misconceptions [Q41, Q42, Q43]. Bridge comprises
partial dialogues between real human tutors and students at the elementary level,
with 60 high-quality instances selected from 700 dialogues on the criterion that
the student's last utterance exhibits an error or confusion [Q45, Q46, Q47].
MathDial consists of complete multi-turn conversations between a real human tutor
and an LLM acting as a student in middle-school mathematical reasoning, with 132
instances retained after manual quality inspection [Q48, Q49, Q51]. MathDial
conversations are longer, structurally more complex, and grounded in reasoning
tasks [Q95], while Bridge conversations are shorter and focused on fundamental
operations [Q44, Q45, Q92]. Both source datasets were constructed in Western
academic settings where student verbalization of reasoning is extensive; neither
dataset was designed to capture the briefer, more deferential student communication
styles characteristic of Indian classrooms. The paper does not acknowledge this
cultural provenance as a limitation. The benchmark's claim to being "challenging and
comprehensive" is defined exclusively in terms of mathematical difficulty level, not
cultural or interactional diversity [Q97].

### 3. Input Form
All benchmark data is text-only, consisting of English-language dialogue histories
and tutor responses [Q133, Q134]. LLM responses were generated using a standardized
prompt template adapted from Wang et al. (2024a) [Q133, Q134]. Conversation and
response lengths differ systematically between the two datasets, with Bridge being
shorter in character count and turn count, and MathDial longer and more structured
[Q141, Q142]. Length is uniformly estimated in characters [Q147]. Conversation topic
metadata is absent from MathDial [Q145]. The format is consistent with a text-based
English deployment environment and presents no signal-distribution mismatch for
Indian metro professional teachers who operate in English. No multimodal signals
(e.g., images of handwritten work) are included, and no spoken or script-level
variation is evaluated.

### 4. Output Ontology
Each tutor response is scored across the eight pedagogical dimensions using a
three-tier labeling system (e.g., "yes," "to some extent," "no") [Q58, Q59]. The
taxonomy specifies a "desired label" for each dimension [Q65, Q128], and these
desired labels collectively underpin the Desired Annotation Match Rate (DAMR) metric
[Q64, Q65]. The output taxonomy focuses on the appropriateness of individual tutor
turns rather than cumulative learning impact [Q119, Q120, Q121], and all eight
dimensions are treated analytically as independent and orthogonal despite
acknowledged interdependencies [Q30, Q116]. The equal analytical weighting of all
eight dimensions in DAMR does not reflect the user-identified emphasis on "providing
guidance" as the single most critical dimension for Indian professional teachers.
The label scheme collapses "neutral" and "encouraging" tutor tone into a
"non-offensive" composite for DAMR purposes, achieving 100% compliance across all
tutors [Q90]. The taxonomy is explicitly scoped to mathematics mistake remediation
and may not generalize to other tasks or subjects [Q117, Q118].

### 5. Output Content
The annotation team consisted of four individuals — two male, two female — all
holding at least a post-graduate degree in Computer Science and proficient in English,
affiliated with MBZUAI in Abu Dhabi [Q31, Q6]. Crucially, the authors explicitly
state that direct teaching experience was not required; the ability to judge responses
from the perspective of a student or potential AI tutor user was deemed sufficient
[Q32]. Public crowdsourcing platforms were avoided in favor of rigorous in-house
training protocols [Q33, Q34, Q135, Q136, Q137]. A validation pilot study yielded a
Fleiss' kappa of 0.65 (substantial agreement) [Q37, Q38, Q39], and the full
annotation achieved an average Cohen's kappa of 0.71 [Q56, Q57, Q61]. LLM-based
annotation using Prometheus2 and Llama-3.1-8B was also conducted [Q105], but
resulting correlations with human annotations were predominantly negative across
pedagogical dimensions [Q107, Q108, Q109], indicating unreliability. No annotator
had documented exposure to Indian educational norms, CBSE/NCERT curricula, or
South Asian pedagogy, and the paper does not acknowledge this as a limitation.
Because the "providing guidance" dimension's desired labels were calibrated by
annotators whose implicit pedagogical model likely reflects Western or generic
academic norms — favoring Socratic scaffolding over direct correction — the
ground-truth labels for this most-critical dimension may systematically diverge
from the judgments Indian professional teachers would render.

### 6. Output Form
The benchmark employs two primary quantitative metrics: DAMR (percentage of
responses receiving the desired annotation label per dimension) [Q64, Q65] and
Annotation Correlation (Pearson's correlation between LLM-generated and human
annotations) [Q66, Q138]. Human annotations are treated as the gold standard [Q68].
Results are reported both overall and broken down by dataset [Q149, Q150]. The
output form is categorical labels and percentage/correlation scores — consistent
with a deployment scenario where teachers evaluate binary or graded acceptability.
The benchmark does not evaluate free-form output quality through generative metrics;
the paper explicitly notes that general NLG metrics like BLEU and BERTScore fail to
capture pedagogical values [Q4, Q7, Q8]. LLM evaluators are assessed as unreliable
critics for pedagogical dimensions [Q114, Q123].


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "we propose a unified evaluation taxonomy with eight pedagogical dimensions based on key learning sciences principles, which is designed to assess the pedagogical value of LLM-powered AI tutor responses grounded in student mistakes or confusions in the mathematical domain." |
| Q2 | 1 | input_content | "We release MRBench – a new evaluation benchmark containing 192 conversations and 1,596 responses from seven state-of-the-art LLM-based and human tutors, providing gold annotations for eight pedagogical dimensions." |
| Q3 | 1 | output_form | "We assess reliability of the popular Prometheus2 and Llama-3.1-8B LLMs as evaluators and analyze each tutor's pedagogical abilities, highlighting which LLMs are good tutors and which ones are more suitable as question-answering systems." |
| Q4 | 1 | output_form | "General domain-agnostic natural language generation (NLG) metrics (Lin, 2004; Popovic´, 2017; Post, 2018; Gao et al., 2020; Liu et al., 2023) are not well-suited for this context, as most of them fail to account for pedagogical values and require gold references, which are often not available, especially in online interactions." |
| Q5 | 1 | input_ontology | "Specifically, for the student mistake remediation task, we need to assess complex pedagogical aspects and abilities of such systems, ensuring that they provide students with sufficient, helpful, and factually correct guidance and do not simply reveal answers when a student makes a mistake." |
| Q6 | 1 | output_content | "Kaushal Kumar Maurya, KV Aditya Srivatsa, Kseniia Petukhova and Ekaterina Kochmar. Mohamed bin Zayed University of Artificial Intelligence, Abu Dhabi, UAE." |
| Q7 | 2 | output_form | "General domain-agnostic natural language generation (NLG) metrics like BLEU (Papineni et al., 2002), BERTScore (Lin, 2004), DialogRPT (Gao et al., 2020), and so on have been used as proxies to measure the coherence and human-likeness of AI tutor responses." |
| Q8 | 2 | output_form | "However, these metrics do not account for pedagogical values (Jurenka et al., 2024; Liu et al., 2024) and often require a ground truth answer to evaluate matching responses." |
| Q9 | 2 | output_content | "For a given input dialogue, there can be multiple valid, pedagogically correct ground truth responses, making detection of the optimal answer non-deterministic (Tack and Piech, 2022; Al-Hossami et al., 2024)." |
| Q10 | 2 | output_form | "Additionally, these metrics can be easily manipulated; for instance, simple responses like "Hello" or "teacher:" (Baladón et al., 2023; Jurenka et al., 2024) can inflate scores." |
| Q11 | 2 | output_form | "In this section, we first briefly overview and discuss the limitations of the existing general-purpose NLG metrics and then turn to pedagogically-oriented approaches to evaluation." |
| Q12 | 3 | input_ontology | "In this work, we focus on educational dialogues between a student and a tutor in the mathematical domain. Specifically, the conversations are grounded in students' mistakes or confusions, and the AI tutor aims to respond in order to remediate such mistakes or confusions." |
| Q13 | 3 | input_ontology | "Formally, let's define the conversation history between a tutor and a student as H = {(T1, S1),(T2, S2), . . . ,(Tt, St)}, where Ti represents the i-th response from the tutor, and Si represents the i-th response from the student. Let Sk denote the student's most recent k utterances, where k ∈ [1, ..., t], containing a mistake or confusion. Then the objective of the tutor is to provide the most appropriate response Tt+1 to address this mistake or confusion." |
| Q14 | 3 | input_ontology | "The evaluation taxonomy detailed in Section 4 assesses the appropriateness of the Tt+1 response across eight key pedagogical dimensions." |
| Q15 | 3 | input_ontology | "In this section, we first present our approach, narrowing the evaluation taxonomy down to eight measurable dimensions aligned with key pedagogical strategies (Jurenka et al., 2024; Hennessy et al., 2016). These dimensions are most suitable for the student mistake remediation task and are based on the learning sciences principles." |
| Q16 | 3 | input_ontology | "We then dive into the details of each dimension and its relationship to previous research. An overview of the taxonomy is presented in Table 2." |
| Q17 | 3 | input_ontology | "Encourage active learning (Chi and Wylie, 2014; Oakley and Sejnowski, 2021): The tutor should encourage students to actively participate in the discussion and practice rather than passively receive information. The tutor can achieve this by not revealing the answer immediately and scaffolding guidance." |
| Q18 | 3 | input_ontology | "Adapt to students' goals and needs (King and South, 2017): The tutor should respond coherently by adapting to the current state and goals of the student's learning rather than following a pre-defined learning path. In the context of student mistake remediation, this happens when the tutor identifies the mistake, pinpoints its location, and responds coherently." |
| Q19 | 3 | input_ontology | "Manage cognitive load and enhance metacognitive skills (Mayer, 2002; Dehaene, 2020; Cohen et al., 2021): The tutor should present the information in a structured manner, with elaboration and examples in manageably small chunks that enable the student to generalize their learning skills beyond the current problem. For the task at hand, this can be achieved by providing appropriate guidance." |
| Q20 | 3 | input_ontology | "Foster motivation and stimulate curiosity (Keller, 1987; Patall et al., 2008): The tutor" |
| Q21 | 4 | input_ontology | "Since all dialogues in the dataset contain a mistake made by the student, a good-quality response from the tutor should include the relevant mistake identification." |
| Q22 | 4 | input_ontology | "A good tutor response should not only notify the student of the committed error but also point to its location in the answer and outline what the error is to help the student remediate it in their subsequent response." |
| Q23 | 4 | input_ontology | "Since most dialogues are relatively short and present contexts for the mistakes made early in the student's solution, a good tutor strategy is not to reveal the answer to the student immediately but rather provide helpful guidance." |
| Q24 | 4 | input_ontology | "In addition to not revealing the answer immediately, a good tutor response should provide the student with relevant and helpful guidance, such as a hint, an explanation, or a supporting question." |
| Q25 | 4 | input_ontology | "Once the guidance is provided to a student, it should be clear from a good tutor response what the student should do next; in other words, the tutor response should not be vague, unclear, or a conversation stopper." |
| Q26 | 4 | input_ontology | "We postulate that a high-quality tutor's response should be logically consistent with the student's previous responses." |
| Q27 | 4 | input_ontology | "In addition to addressing student mistakes, a good tutor should encourage them and avoid using toxic language, which is aligned with the care dimension in the evaluation schema of Wang et al. (2024a)." |
| Q28 | 4 | output_content | "This dimension is particularly critical for LLM-based AI tutors, as they often exhibit unpredictable behavior." |
| Q29 | 4 | input_ontology | "Effective tutoring requires that students feel a connection with the tutor, which is more likely when the tutor's responses appear human-like rather than robotic." |
| Q30 | 4 | output_ontology | "Although there are inherent interdependencies among the proposed dimensions of the taxonomy (e.g., a response that reveals the answer is less likely to be actionable, and vice versa), we explicitly instructed all annotators to treat each dimension as independent and orthogonal to minimize confounding factors and potential biases during the annotation process." |
| Q31 | 5 | output_content | "The annotation team consisted of two male and two female annotators, with all four annotators holding at least a post-graduate degree in Computer Science and being proficient in English." |
| Q32 | 5 | output_content | "We note that for this study, we do not require annotators to have direct teaching experience, as understanding of the mathematical tasks at the middle school level and being able to judge the responses from the perspective of a potential user of such AI tutors (or a student), rather than specifically a teacher, is sufficient." |
| Q33 | 5 | output_content | "To control the annotation workflow and ensure quality, we opted not to use public annotation outsourcing platforms such as Prolific or MTurk, which allowed us to implement rigorous training protocols and a robust validation mechanism for the annotations." |
| Q34 | 5 | output_content | "First, we provided all annotators with comprehensive training, including an interactive training document (see Section C for more details) and oral instructions." |
| Q35 | 5 | output_content | "Following this, we conducted validation pilot study to evaluate the annotation quality and the annotators' understanding of the instructions before rolling out the large-scale human evaluation detailed in Section 5.2." |
| Q36 | 5 | output_content | "In this validation pilot study, all four annotators iteratively reviewed the annotation scheme and guidelines." |
| Q37 | 5 | output_content | "Each annotator also independently labeled the same eight randomly sampled dialogues – four from each of the two datasets (Bridge and MathDial) – across the eight dimensions of the evaluation taxonomy." |
| Q38 | 5 | output_content | "Given that each dialogue contained multiple responses from both LLMs and humans, and each response was annotated across eight evaluation dimensions, this resulted in a total of 544 annotations per annotator." |
| Q39 | 5 | output_form | "To measure inter-annotator agreement, we computed Fleiss' kappa value, which for this annotation experiment equals 0.65, indicating substantial agreement." |
| Q40 | 5 | input_ontology | "None of the annotators identified any additional or redundant dimensions necessary for student mistake remediation." |
| Q41 | 5 | input_content | "We have compiled mistake remediation benchmark, MRBench, from the Bridge (Wang et al., 2024a) and MathDial (Macina et al., 2023) datasets." |
| Q42 | 5 | input_content | "Each instance in both datasets comprises educational dialogue interactions between students and tutors within the mathematical domain." |
| Q43 | 5 | input_content | "These interactions are specifically anchored in the students' errors or misconceptions, accompanied by the subsequent human tutor response, which aims to remediate the mistake or confusion." |
| Q44 | 5 | input_content | "The Bridge dataset (Wang et al., 2024a) comprises partial dialogue interactions between real human tutors and students at the elementary level, featuring two distinct human tutor responses (novice and expert)." |
| Q45 | 5 | input_content | "The dialogue context is typically short (few turns) and predominantly focused on fundamental mathematical concepts, including operations such as multiplication, addition, and so on." |
| Q46 | 5 | input_content | "The original dataset consists of a total of 700 dialogues; we filtered 60 high-quality instances for MRBench." |
| Q47 | 5 | input_content | "Among the various criteria for selecting high-quality dialogues, the key one was that the student's last utterance (or last few utterances) should exhibit an error or confusion." |
| Q48 | 5 | input_content | "The dialogues in the MathDial dataset (Macina et al., 2023) consist of complete multi-turn conversations between a real human tutor and an LLM acting as a student, where the tutor aims to remediate the student's mistakes." |
| Q49 | 5 | input_content | "Specifically, these conversations are grounded in middle school-level mathematical reasoning questions." |
| Q50 | 5 | input_form | "To match the format of Bridge (partial conversations with the last few student's utterances exhibiting a mistake or confusion), we prepared the dataset by terminating a conversation where the student makes a mistake and considering the next tutor response as the expert tutor response (there are no associated novice" |
| Q51 | 6 | input_content | "To further ensure the reliability of our benchmark, we manually inspected the data in order to retain only high-quality examples, which resulted in 132 instances for MRBench." |
| Q52 | 6 | input_content | "Next, for the 192 instances in MRBench (60 from Bridge and 132 from MathDial), we generated appropriate subsequent responses based on the conversation history and the last utterance, which contained confusions or mistakes, using seven state-of-the-art LLMs." |
| Q53 | 6 | input_content | "We consider state-of-the-art LLMs of various sizes and capabilities, including: GPT-4 (Achiam et al., 2023), Gemini (Reid et al., 2024), Sonnet (Anthropic, 2024), Mistral (Jiang et al., 2023), Llama-3.1-8B and Llama-3.1-405B (Dubey et al., 2024), and Phi3 (Abdin et al., 2024)." |
| Q54 | 6 | input_form | "Furthermore, each LLM has associated responses for 192 dialogues, resulting in a benchmark of 192 × 7 (7 LLM responses) + 192 × 1 (expert responses) + 60 × 1 (novice responses) = 1,596 responses, which makes the evaluation benchmark reasonably large while still manageable for human annotation described in Section 5.2." |
| Q55 | 6 | output_content | "Four trained annotators (see Section 4.2) annotated MRBench using the validated taxonomy." |
| Q56 | 6 | output_content | "Each annotator was asked to annotate human and LLM-based tutor responses across 8 dimensions of the taxonomy in the context of 48 dialogues." |
| Q57 | 6 | output_content | "A total of 192 instances were annotated, with 40 of those annotated independently by two annotators (10 instances from Bridge and 30 from MathDial) allowing us to calculate pairwise inter-annotator agreement." |
| Q58 | 6 | output_ontology | "Each dimension was annotated using a three-tier labeling system (see Figure 1 and Table 4)." |
| Q59 | 6 | output_ontology | "For instance, the 'mistake identification' dimension employed the following labels: (i) yes, (ii) to some extent, and (iii) no." |
| Q60 | 6 | output_content | "Annotators were instructed to assign 'yes' if the tutor accurately identified the mistake, 'no' if the mistake was missed, and 'to some extent' when there was ambiguity or uncertainty in the mistake identification." |
| Q61 | 6 | output_content | "The annotators reached an average Cohen's kappa score of 0.71, which indicates substantial inter-annotator agreement (McHugh, 2012)." |
| Q62 | 6 | output_form | "We used Prometheus2 (Kim et al., 2024) because: (i) it was specifically trained as an evaluator using reinforcement learning with human feedback (RLHF), (ii) it has a high correlation with human annotations and GPT-4, and (iii) it does not belong to any of the LLM families considered as AI tutors in our framework." |
| Q63 | 6 | output_form | "In addition, we also used Llama-3.1-8B as a lightweight LLM to assess the reliability of smaller models that were not fine-tuned for evaluation objectives as a critic." |
| Q64 | 6 | output_form | "We utilize two key metrics to quantitatively assess the pedagogical effectiveness of LLMs and for comparative analysis: (1) Desired Annotation Match Rate (DAMR): This metric quantifies the percentage of responses from each human or LLM-based tutor that received the desired annotation labels." |
| Q65 | 6 | output_ontology | "The desired labels for each dimension are detailed in Table 2." |
| Q66 | 6 | output_form | "(2) Annotation Correlation (AC): This metric is based on Pearson's correlation (Sedgwick, 2012), and it estimates the correlation between LLM-generated and human annotations (Kim et al., 2024), allowing us to assess the reliability of LLMs as evaluators in the context of student mistake remediation." |
| Q67 | 7 | output_form | "Table 3 shows DAMR scores for each LLM across all eight dimensions." |
| Q68 | 7 | output_content | "We consider human-based evaluations as gold standard." |
| Q69 | 7 | output_form | "Both these LLMs perform well in identifying students' mistakes and their exact location, with Llama-3.1-405B having a slight edge as GPT-4 reveals the answer approximately 47% of the time, making its responses less actionable and impacting student's learning experience." |
| Q70 | 7 | output_ontology | "This shows that GPT-4 is a good question-answering system but a relatively poor tutor." |
| Q71 | 7 | output_form | "Among these three LLMs, Gemini performs the worst as its responses are often incoherent, while also achieving low scores for mistake identification and exact location." |
| Q72 | 7 | output_form | "Phi3 is the worst-performing LLM model in this context, with the lowest score for coherence, suggesting that the responses from Phi3 are often irrelevant to the conversation context, as well as overall low scores in other dimensions." |
| Q73 | 7 | output_content | "This underscores the model's inadequate capacity for contextual understanding and semantic alignment in educational dialogues considered in this study." |
| Q74 | 7 | output_form | "In the few cases where Phi3 demonstrates some competence, it frequently reveals the answer, reflecting more of a question-answer system than a pedagogical tutor behavior." |
| Q75 | 7 | output_form | "Moreover, its outputs tend to be robotic, template-based and lack the nuance expected in human responses." |
| Q76 | 7 | output_form | "In contrast, despite having fewer parameters, Llama-3.1-8B demonstrates reasonable performance, albeit still below that of larger LLMs." |
| Q77 | 7 | output_form | "Specifically, its responses are coherent, strategically avoid immediate answer revelation, robustly identify and rectify mistakes, and exhibit human-like behavior, as evidenced by the DAMR scores." |
| Q78 | 7 | output_form | "We also investigated the pedagogical value of human responses for both Novice and Expert." |
| Q79 | 7 | output_form | "It can be observed that Novice responses do not have a high score for guidance and are poor in terms of actionability (DAMR score of 1.67)." |
| Q80 | 7 | output_form | "Furthermore, the responses are generally short and ambiguous, such as "this is a good try," which leads to lower scores for mistake identification and location." |
| Q81 | 7 | output_form | "At the same time, they often do not reveal the answer." |
| Q82 | 7 | input_content | "*For the Novice, we have considered only 60 dialogues from the Bridge dataset." |
| Q83 | 7 | output_form | "The DAMR scores for Novice are reported on these 60 instances, while for Expert and all LLMs, all 192 instances were considered." |
| Q84 | 8 | output_ontology | "Can a tutor achieve a higher DAMR score for actionability while receiving a lower score for providing guidance? This is possible since we consider only factually correct guidance as useful (see Table 4)." |
| Q85 | 8 | output_content | "At the same time, even incorrect or incomplete guidance can lead to certain actions on the part of the student and can foster their curiosity, thus providing them with learning opportunities." |
| Q86 | 8 | output_ontology | "This further demonstrates the need to treat the dimensions as independent." |
| Q87 | 8 | output_content | "In terms of the other qualities of the Expert responses, they do not normally reveal the answer and tend to include scaffolding; however, there are a small number of instances where they failed to identify the mistake or its location." |
| Q88 | 8 | output_content | "Overall, we conclude that human responses from Expert are significantly better than Novice." |
| Q89 | 8 | output_form | "Our findings on the Tutor Tone align with those of Wang et al. (2024a) – in task-oriented conversations, AI tutors tend to be more Neutral than Encouraging." |
| Q90 | 8 | output_ontology | "When we combine these two labels into "Non-offensive", the DAMR score reaches 100% as we observe no offensive responses from any LLMs or humans." |
| Q91 | 8 | input_ontology | "We observe high scores for most of the LLMs on human-likeness, which demonstrates their capability to generate human-like output with minimal or no grammatical and fluency mistakes, showing the timely nature of our study, which focuses more on in-depth semantic and pedagogical aspects of tutor responses rather than only on superficial attributes like grammaticality and fluency." |
| Q92 | 8 | input_content | "As discussed in Section 5.1, the conversational contexts in the Bridge dataset are typically very short (see Table 7) and the dialogues are grounded in elementary math operations, so most models are able to identify the mistakes and their locations." |
| Q93 | 8 | input_content | "However, they struggle to provide appropriate guidance without revealing the answer because the mistakes are generally related to quite basic operations like addition or multiplication, often in a one-step type of mathematical problems." |
| Q94 | 8 | output_form | "Still, models like GPT-4 and Llama-3.1-405B are able to offer some reasonable guidance." |
| Q95 | 8 | input_content | "In contrast, for MathDial, the contexts are longer, the mistakes are grounded in reasoning, and the responses are more structured." |
| Q96 | 8 | output_content | "Yet, many LLMs do not meet the expectations for each dimension of the taxonomy, as discussed earlier." |
| Q97 | 8 | input_content | "Combining both types of data in MRBench makes it both challenging and comprehensive." |
| Q98 | 8 | output_content | "In summary, all LLMs and even human tutors lack some pedagogical abilities required for effective tutoring." |
| Q99 | 8 | output_form | "While Llama-3.1-405B is the most effective, followed by Mistral and other state-of-the-art models, GPT-4 reveals the answer too quickly." |
| Q100 | 8 | output_form | "Gemini is less coherent and accurate, and Sonnet focuses on human-likeness and encouraging tone but is less effective in other dimensions." |
| Q101 | 8 | output_form | "Phi3 is the worst-performing model according to our analysis, as it fails to understand the context, while Llama-3.1-8B, despite being smaller, performs reasonably well." |
| Q102 | 8 | output_content | "Human responses are also not perfect – Novice responses are ambiguous and short, whereas Expert responses are more focused on actionability and less on other dimensions." |
| Q103 | 8 | input_ontology | "Overall, the proposed taxonomy precisely categorizes performance across 8 dimensions, reflecting the current state-of-the-art in AI tutors." |
| Q104 | 8 | output_content | "Our study demonstrates that there is a considerable room for improvement in the pedagogical abilities of AI tutors." |
| Q105 | 8 | output_content | "We also performed annotations using Prometheus2 and Llama-3.1-8B as critic LLMs." |
| Q106 | 8 | output_form | "The correlation scores with human annotations are presented in Appendix Tables 5 and 6, respectively." |
| Q107 | 8 | output_content | "Across both LLMs, it can be observed that most of the correlation scores are negative (except for the human-likeness dimension), indicating that the annotations from the LLMs are unreliable for the challenging pedagogical dimensions." |
| Q108 | 8 | output_content | "Prometheus2 is not trained on our taxonomy dimensions, except for the general human-likeness dimension, where the model shows slightly better correlations with positive scores." |
| Q109 | 8 | output_content | "We believe both LLMs have a limited understanding of rich pedagogical concepts, as they were not specifically trained on pedagogically rich datasets." |
| Q110 | 8 | output_form | "At the same time, we acknowledge that the experiments presented in this work are preliminary" |
| Q111 | 9 | input_ontology | "This paper presents the first effort to unify AI tutor evaluation for the student mistake remediation task in the mathematics domain." |
| Q112 | 9 | input_ontology | "Specifically, we propose an evaluation taxonomy with eight pedagogical dimensions based on the key learning sciences principles." |
| Q113 | 9 | output_content | "We also release the MRBench benchmark with seven state-of-the-art LLM-as-tutors responses, along with gold human annotations." |
| Q114 | 9 | output_form | "We also assess the feasibility of LLMs as evaluators in this context by correlating their judgements with human annotations, indicating that they are often unreliable." |
| Q115 | 9 | output_ontology | "This study evaluates tutor response quality across the proposed eight dimensions independently." |
| Q116 | 9 | output_ontology | "However, in practice, these dimensions may be inherently interrelated and may influence one another." |
| Q117 | 9 | input_ontology | "The proposed taxonomy primarily focuses on the task of the student mistake remediation in the domain of mathematics." |
| Q118 | 9 | input_ontology | "We acknowledge that the proposed taxonomy will need to be verified on and likely adapted if applied to other tasks such as concept learning, and to subjects other than mathematics." |
| Q119 | 9 | output_ontology | "The current taxonomy and annotation scheme focus on the appropriateness of the tutor responses." |
| Q120 | 9 | output_ontology | "However, one of the limitations is that it does not consider the tutoring dialogues' impact on the overall student learning." |
| Q121 | 9 | output_ontology | "Specifically, the annotation pertains to the individual tutor turns within educational dialogues, which restricts our understanding of broader implications on student learning processes and learning gains, typically observed after a conversation concludes." |
| Q122 | 9 | output_form | "In this study, we limit the LLM-based evaluation to two LLMs as critics, using the evaluation prompt presented in Figure 6." |
| Q123 | 9 | output_form | "The results obtained with these LLMs are not encouraging, as detailed in Section 6." |
| Q124 | 9 | output_content | "Although we do not foresee any ethical risks, we acknowledge that this work relies on the outputs from LLMs, and there are certain risks associated with such outputs in general since these models may generate responses that, although plausible, can be factually incorrect, nonsensical, or even offensive." |
| Q125 | 9 | output_content | "Of particular importance for the educational domain is the fact that hallucinations can misguide students and propagate biases." |
| Q126 | 10 | output_content | "This research is partially supported by Google through the Google Academic Research Award (GARA) 2024. We are grateful for their support. We also extend our gratitude to the campus supercomputing center at MBZUAI." |
| Q127 | 10 | output_content | "strongly believe that this study will help shed light on the current capabilities of LLMs in the context of educational dialogues, and the insights gained from this study may help mitigate issues related to the use of LLMs in the educational domain in the future." |
| Q128 | 12 | output_ontology | "The definitions, associated labels, and the desired labels for each dimension of the proposed taxonomy are provided in Table 4." |
| Q129 | 12 | input_ontology | "Through an iterative analysis of the taxonomy, we identify eight dimensions that comprehensively assess tutor response quality in the context of mistake remediation." |
| Q130 | 12 | input_ontology | "However, other educational settings, particularly those involving tutorial dialogues beyond mistake remediation, may require modifications, as discussed in the limitations section." |
| Q131 | 12 | input_ontology | "To establish a robust framework, we initially considered additional dimensions such as grammaticality and empathy, among others." |
| Q132 | 12 | output_content | "However, our validation pilot study (see Section 4.2) confirmed that the selected eight dimensions are both necessary and sufficient for evaluating tutor response quality in dialogues aimed at mistake remediation." |
| Q133 | 12 | input_form | "The prompt template used to generate responses from the seven considered LLMs for both the Bridge and MathDial datasets is shown in Figure 2." |
| Q134 | 12 | input_form | "The template is adapted from Wang et al. (2024a)." |
| Q135 | 13 | output_content | "As discussed in Section 5.2, prior to commencing large-scale human annotation, we implemented a two-phase interactive training and evaluation protocol and asked each annotator to undertake training." |
| Q136 | 13 | output_content | "Subsequently, we assessed annotators' understanding through a structured quiz, as is shown in a screenshot presented in Figure 5." |
| Q137 | 13 | output_content | "Additionally, we developed a comprehensive set of annotation guidelines, serving as a reference for annotators during the large-scale annotation process." |
| Q138 | 13 | output_form | "The correlation scores are calculated using Pearson's correlation (Sedgwick, 2012)." |
| Q139 | 13 | input_content | "*Only 60 dialogues were considered for Novice, whereas all 192 dialogues were considered for Expert and other tutors." |
| Q140 | 14 | input_content | "Table 7 shows the statistics for the Bridge, MathDial, and MRBench datasets." |
| Q141 | 14 | input_form | "It can be observed that the conversation history and response lengths from different LLMs and humans are generally shorter in the Bridge dataset compared to the MathDial dataset." |
| Q142 | 14 | input_form | "Additionally, the number of turns differs between them." |
| Q143 | 14 | input_ontology | "These aspects highlight that including both datasets in MRBench ensures diversity and provides for a good mix of easy and difficult mathematical problems, making the benchmark both comprehensive and challenging." |
| Q144 | 14 | input_ontology | "The problems covered in the Bridge dataset are at the elementary school level, whereas those in MathDial are at the middle school level." |
| Q145 | 14 | input_form | "The conversation topic is not provided in MathDial." |
| Q146 | 14 | output_content | "* indicates that the annotations are considered for 8 evaluation dimensions of the taxonomy." |
| Q147 | 14 | input_form | "In all cases, length is estimated using the number of characters." |
| Q148 | 15 | output_content | "The template is based on the insights drawn from the Prometheus2 model's official guidelines." |
| Q149 | 16 | output_form | "Pedagogical ability assessment of different LLMs using the DAMR scores (in %) across eight evaluation dimensions with human evaluation on the Bridge data." |
| Q150 | 16 | output_form | "Pedagogical ability assessment of different LLMs using the DAMR scores (in %) across eight evaluation dimensions with human evaluation on the MathDial data." |
| Q151 | 16 | input_content | "'-' indicates that DAMR scores for Novice are not available for MathDial data." |
| Q152 | 17 | output_content | "Figure 4: An example from the annotator training phase for the Mistake Identification dimension." |
| Q153 | 17 | output_content | "Figure 5: An example from the annotator testing phase for the Revealing of the Answer dimension." |

---

## Regional Context

```yaml
name: Indian Metropolitan Grade 1–8 Mathematics Teachers (Delhi & Mumbai)
abbreviation: IN-METRO-MATH-TEACHERS
deployment_context:
  application: One-on-one mathematics tutoring mobile/enterprise application where
    GPT-4 responses are augmented by a human tutor's input
  evaluator_role: Professional Grade 1–8 teachers evaluate the pedagogical quality
    of combined AI + human tutor responses, specifically whether augmented output
    provides acceptable guidance to students
  benchmark_use: MRBench is being assessed for validity as a measure of tutoring quality
    relevant to this deployment
  interaction_modality: Text-based, English-language, mobile-first interface
target_population:
  description: 'High-end professional teachers working in major Indian metropolitan
    cities (Delhi and Mumbai), teaching mathematics at Grade 1–8 level. They are fluent
    in English and operate within a pedagogical culture shaped by CBSE/NCERT norms,
    exam-oriented correction practices, and teacher-directed interaction styles. Their
    role in this deployment is evaluative: they judge the acceptability of AI-augmented
    tutor responses as guidance for students.'
  geography:
    country: India
    cities:
    - Delhi
    - Mumbai
    geographic_scope: Major metropolitan / urban professional teaching workforce;
      sub-national variation within these cities (e.g., school type, board affiliation)
      is unspecified and represents a flagged gap
  occupational_profile:
    role: Professional schoolteacher
    subject: Mathematics
    grade_band: Grade 1–8 (elementary through lower secondary)
    employment_context: 'Formal school setting; likely includes government, private,
      and potentially international-board schools — specific distribution [NEEDS VERIFICATION
      — deferred: below search budget; no publicly available disaggregated school-type
      employment statistics by city and grade band found]'
    professional_standing: 'For CBSE-affiliated schools (which include all Delhi government
      schools per CBSE rules, and many private schools nationwide), teachers at Grade
      1–8 must hold a B.Ed or D.El.Ed qualification and pass the Central Teacher Eligibility
      Test (CTET Paper I or II). B.Ed is required for Classes VI–VIII (TGT level);
      D.El.Ed or B.El.Ed for Classes I–V. High-end private and international schools
      may additionally require subject-specific postgraduate degrees. Source: NCTE/CBSE
      official qualification norms — [WEB-1];
      CTET eligibility criteria — [WEB-2]'
  estimated_population_size: '[NOT FOUND — searched general sources; no published
    disaggregated figure for Grade 1–8 mathematics teachers specifically in Delhi
    and Mumbai formal school sector found. National UDISE+ data tracks total teachers
    by state but not by city, grade band, and subject combination.]'
languages:
  primary_evaluation_language: English
  fluency_level: Fluent — the target population uses English professionally and can
    evaluate English-language tutoring dialogues without assistance
  other_languages_in_context:
  - Hindi (dominant regional language in Delhi; likely used in classroom instruction
    at government schools)
  - Marathi (dominant regional language in Mumbai; likely used in classroom instruction
    at government schools)
  - Other L1s of students taught, which may introduce L1-interference error patterns
    in student mathematics language
  language_note: The benchmark is English-only, matching the deployment's evaluation
    interface. However, many students in these classrooms may be instructed in Hindi,
    Marathi, or other regional languages, and L1-interference in students' mathematical
    communication is a flagged validity gap for the benchmark's source datasets.
  hindi_math_register_notes: '[NEEDS VERIFICATION — deferred: likely unsearchable
    (lived practice); no published study found that specifically quantifies how Indian
    math teachers conducting English-language evaluations interpret student errors
    through the lens of Hindi/Marathi-medium instruction patterns. Requires stakeholder/expert
    elicitation.]'
writing_systems:
  script_used_in_deployment: Latin (English text only)
  script_notes: No script mismatch exists between the benchmark and the deployment.
    The evaluation interface and benchmark are both Latin-script English. No RTL,
    Devanagari, or other script handling is required.
pedagogical_culture:
  curriculum_frameworks:
    primary: CBSE (Central Board of Secondary Education) — dominant board in Delhi
      and influential in Mumbai private schools
    secondary:
    - NCERT (textbook and syllabus authority underlying CBSE)
    - ICSE (Indian Certificate of Secondary Education)
    - Maharashtra State Board (relevant to Mumbai government schools)
    - IB (International Baccalaureate, present in elite private schools in both cities)
    board_distribution_in_target_cities: 'All Delhi government schools are CBSE-affiliated
      (confirmed by CBSE). In Mumbai, the Maharashtra State Board (SSC) dominates
      government schools, while CBSE, ICSE, and a small number of IB schools operate
      in private sector. Nationally, ICSE has approximately 2,891 affiliated schools
      with Maharashtra leading at ~118 new schools, and IB schools remain a small
      elite minority. No city-level proportional breakdown by teacher count is publicly
      available. Source: CBSE affiliation rules — [WEB-3];
      ICSE school count — [WEB-4]'
    curriculum_alignment_requirement: User confirmed curriculum-agnostic math errors
      are sufficient for this evaluation; strict NCERT/CBSE alignment is NOT required
  pedagogical_norms:
    correction_style: Direct, explicit correction is preferred over extended Socratic
      dialogue; teachers are more likely to value responses that clearly identify
      and correct errors rather than those that only prompt student reflection
    exam_orientation: Strong emphasis on exam-readiness framing; guidance quality
      is partly assessed by whether it prepares students for structured examination
      contexts
    teacher_directedness: Teacher-directed interaction is normative; Socratic or student-led
      exploration is less central than in Western constructivist models
    procedure_emphasis: Procedural fluency and algorithmic correctness are highly
      valued, reflecting rote-procedural instructional traditions common in Indian
      mathematics education
    socratic_probing_value: Lower priority compared to Western-default benchmarks;
      extended questioning sequences may be perceived as less effective than direct
      instructional correction
  student_interaction_norms:
    verbalization_of_reasoning: Indian Grade 1–8 students tend to be brief and provide
      less spontaneous verbalization of reasoning steps compared to Western counterparts
    deference_to_teacher: Students are typically deferential; they are less likely
      to challenge, elaborate, or ask follow-up questions unprompted
    turn_length: Student turns tend to be short; extended multi-turn Socratic exchanges
      of the type found in MathDial are less representative of authentic Indian classroom
      dynamics
    procedure_over_concept: Students are more likely to present procedural errors
      than to engage in exploratory conceptual dialogue
  key_pedagogical_concept_note: The benchmark's implicit model of good tutoring (Socratic
    scaffolding, withholding answers, prompting extended student reasoning) partially
    conflicts with Indian professional teachers' expectations of acceptable guidance,
    which favor directness, correction clarity, and exam-preparedness framing.
dimension_priority_profile:
  most_critical_dimension:
    name: Providing Guidance
    rationale: User identified this as the single most critical dimension for evaluating
      acceptability in student mistake remediation; a response that fails on guidance
      is unacceptable regardless of performance on other dimensions
  accepted_as_necessary_and_sufficient: User confirmed all eight MRBench dimensions
    are necessary and sufficient; no additional dimensions were flagged as missing
  equal_weight_concern: MRBench's DAMR scoring treats all eight dimensions with equal
    analytical weight; this does not reflect the deployment-relevant prioritization
    of 'providing guidance' as the dominant acceptability criterion. Re-weighting
    would be required to use DAMR directly as a proxy for Indian teachers' binary
    acceptability judgments.
  guidance_operationalization_mismatch: MRBench operationalizes 'providing guidance'
    primarily through Socratic scaffolding (hints, supporting questions, not revealing
    answers). Indian professional teachers may evaluate guidance quality differently,
    favoring direct-correction forms. Whether the benchmark rubric rewards Western-style
    scaffolding over Indian-style direct instructional correction is a flagged gap
    requiring verification.
  eight_dimensions:
  - Encouraging active learning
  - Adapting to student goals and needs
  - Managing cognitive load / metacognitive skills
  - Fostering motivation
  - Mistake identification
  - Answer non-revelation
  - Providing guidance (highest deployment priority)
  - Actionability
  - Logical coherence
  - Appropriate tone
  - Human-likeness
annotator_representativeness:
  mrbench_annotator_profile: Four CS-educated post-graduates at MBZUAI, Abu Dhabi;
    no teaching experience required; no documented South Asian educational expertise
  deployment_evaluator_profile: High-end professional Grade 1–8 mathematics teachers
    in Delhi and Mumbai with CBSE/NCERT pedagogical backgrounds and exam-oriented
    correction norms
  alignment_assessment: Systematic divergence is expected. Indian professional teachers
    are likely to apply different judgments of guidance quality than the MBZUAI annotator
    pool, particularly on what constitutes 'providing guidance' (direct correction
    vs. Socratic scaffolding), exam-readiness framing, and teacher-directed pedagogy.
  india_specific_annotation_studies: '[NOT FOUND — searched for cross-cultural annotation
    studies and India-specific educator annotation of AI tutor quality; no studies
    found involving Indian educators or South Asian pedagogy experts in MRBench annotation
    or any directly comparable tutoring benchmark annotation exercise.]'
  inter_annotator_agreement_among_indian_teachers: '[NOT FOUND — no published studies
    found measuring Indian professional teachers'' inter-annotator agreement on AI
    tutor pedagogical quality judgments. This remains an open empirical question requiring
    primary research.]'
infrastructure_notes:
  deployment_format: Mobile and/or enterprise application; text-based interface
  language_interface: English text only; no spoken or multimodal interface described
  device_access: 'Mobile-first assumed. Urban Tier-1 cities (including Delhi and Mumbai)
    show internet penetration rates as high as 88% and lead broadband adoption with
    penetration exceeding 50% in urban households. India had 660 million smartphone
    users as of 2024–2025. For professional urban teachers specifically, smartphone
    access can be assumed near-universal. Source: muftinternet.com urban internet
    stats 2025 — [WEB-5];
    Storyboard18 Digital Bharat 2026 report — [WEB-6]'
  internet_connectivity: 'Urban Tier-1 cities (Delhi NCR: ~80% internet penetration;
    Mumbai: among top broadband cities nationally) show adequate connectivity for
    the professional teacher cohort. National mobile data speeds as of early 2024
    averaged 94.62 Mbps median. The specific urban professional teacher sub-cohort
    can reasonably be assumed to have reliable mobile broadband. Source: muftinternet.com
    — [WEB-5];
    DataReportal Digital 2024 India — [WEB-7]'
  enterprise_vs_consumer_split: '[NEEDS VERIFICATION — deferred: below search budget;
    no publicly available data distinguishes school-enterprise from individual teacher
    consumer deployment for this application type in India.]'
school_system_context:
  board_types_present_in_target_cities:
    CBSE: 'Dominant national board; all Delhi government schools are CBSE-affiliated;
      significant in Mumbai private schools; NCERT textbooks and syllabus. Source:
      Wikipedia/CBSE — [WEB-3]'
    ICSE: 'Present in elite private schools in both cities; more emphasis on conceptual
      depth and English proficiency than state boards; approximately 2,891 affiliated
      schools nationally with Maharashtra having a notable share. Source: candidschools.com
      — [WEB-4]'
    Maharashtra_State_Board: 'Dominant in Mumbai government and many private schools;
      Marathi-medium instruction common; proportion of target teachers from state
      board schools not disaggregated at city level in available sources — [NEEDS
      VERIFICATION — deferred: below search budget for precise Mumbai-level figure]'
    Delhi_State_Board: 'Per CBSE rules, all Delhi state government schools are CBSE-affiliated,
      meaning a separate ''Delhi State Board'' for primary/secondary education does
      not exist as a competing exam board for Grade 1–8; the Delhi Board of Higher
      Secondary Education was merged into CBSE in 1962. Source: Wikipedia/CBSE — [WEB-3]'
    IB: 'Present in small number of elite private schools in both cities; very different
      pedagogical norms; Socratic methods more valued; IB schools constitute a small
      elite minority nationally. Exact proportion of target teachers from IB schools
      not available — [NEEDS VERIFICATION — deferred: below search budget]'
  board_specific_pedagogical_variation_note: Each board carries distinct pedagogical
    expectations for what constitutes acceptable tutoring guidance. The acceptability
    criterion for AI-augmented tutor responses may differ meaningfully across CBSE,
    ICSE, Maharashtra State Board, and IB contexts. The elicitation does not specify
    which boards the target teacher population primarily serves, and this sub-national
    granularity is a flagged gap.
  relevant_policy_frameworks:
    NEP_2020: 'NEP 2020 explicitly calls for AI and computational thinking integration
      across all levels of schooling, and the Union Budget 2025–26 allocated ₹500
      crore for a Centre of Excellence in AI for Education. AI and Computational Thinking
      (AI & CT) is being introduced as a compulsory subject from Class 3 onwards starting
      in academic year 2026–27. However, NEP 2020 does not materially alter Grade
      1–8 mathematics pedagogical norms for the core CBSE curriculum relevant to this
      deployment — its pedagogical language emphasises inquiry and learner-centred
      approaches, potentially widening the gap between policy aspiration and prevailing
      teacher-directed classroom norms. Source: PIB Government of India — [WEB-8];
      educationforallinindia.com — [WEB-9]'
    NCERT_curriculum_revision: 'NCERT approved India''s first AI-crafted school curriculum
      for Classes 3–8 in July 2025, covering Mathematics, Science, and Social Science,
      with adaptive content and multilingual support, to be rolled out via PM eVidya
      and DIKSHA platforms. A new Class 8 Mathematics textbook (''Ganita Prakash'')
      has been introduced, emphasising exploration of mathematical patterns alongside
      procedural learning. These revisions are recent and may not yet have materially
      altered teacher correction norms in deployment. Source: myidcm.com — [WEB-10];
      EduRev on Ganita Prakash — [WEB-11]'
    digital_education_initiatives: 'Key national platforms include DIKSHA (Digital
      Infrastructure for Knowledge Sharing, used for AI-based content delivery and
      teacher training), PM eVidya, and SWAYAM/SWAYAM Prabha for teacher upskilling.
      No specific NCERT or CBSE regulatory guidance on AI-assisted one-on-one tutoring
      tools (as distinct from AI curriculum content) was found. CBSE currently offers
      a 15-hour AI skill module from Class VI onwards. Source: PIB — [WEB-8];
      NCERT CIET — [WEB-12]'
validity_gap_summary:
  IC_student_interaction_style:
    priority: HIGH
    description: MRBench source datasets (Bridge, MathDial) reflect Western classroom
      dynamics with extended student verbalization. Indian Grade 1–8 students are
      briefer, more deferential, and procedure-focused. Benchmark conversation structures
      may not be recognizable as realistic to Indian teachers.
    verification_target: '[NOT FOUND — no AI tutoring benchmark specifically designed
      for Indian student interaction styles or short-turn, low-verbalization student
      input scenarios exists in the literature reviewed. MathTutorBench (EMNLP 2025)
      is a related new benchmark (see net-new fields below) but is also sourced from
      Western academic datasets and does not address Indian classroom dynamics. This
      gap remains fully open and requires primary data collection or India-specific
      dataset creation.]'
  OC_annotator_representativeness:
    priority: HIGH
    description: Ground-truth labels reflect CS-trained MBZUAI annotators' pedagogical
      priors, not Indian professional teachers' judgments. Systematic divergence is
      expected on guidance quality, exam-orientation, and direct-correction norms.
    verification_target: '[NOT FOUND — no cross-cultural comparison of teacher judgments
      on AI tutoring acceptability, and no India-specific educator annotation study
      of tutoring quality, was found in literature search. Research on Indian teacher-AI
      collaboration (Sebastian et al., 2024, cited in arxiv.org/html/2507.00456v1)
      confirms Indian teachers face usability barriers and misalignment with generative
      AI outputs, but does not directly address annotation-level agreement on pedagogical
      quality rubrics. Requires primary research.]'
  OC_guidance_dimension_calibration:
    priority: HIGH
    description: MRBench's 'providing guidance' rubric implicitly favors Socratic
      scaffolding. Indian teachers may evaluate guidance quality by direct-correction
      and exam-readiness criteria not captured in the current rubric.
    verification_target: '[NOT FOUND — no MRBench rubric variant addressing direct-correction-style
      guidance found. The MathTutorBench (2025) benchmark similarly operationalizes
      good tutoring through Socratic questioning and withholding of answers (see net-new
      field). No published rubric variant calibrated to Indian pedagogical norms was
      identified. Requires expert elicitation with Indian mathematics educators.]'
  IC_misconception_types:
    priority: HIGH
    description: Bridge and MathDial misconception types are Western-sourced. Rote-procedural
      errors, L1-interference errors, and NCERT-specific algorithmic conventions common
      among Indian Grade 1–8 students are absent from documented selection criteria.
    verification_target: 'NCERT''s own journal (ejournals.ncert.gov.in) publishes
      error-analysis research on Indian students, and CBSE has collaborated with Educational
      Initiatives on competency-based assessment items explicitly designed to probe
      common misconceptions in NCERT-aligned content. However, no published taxonomy
      of Indian-specific Grade 1–8 mathematics misconceptions that maps to MRBench
      error types was found. The CBSE-EI competency-based question booklets reference
      conceptual vs. procedural error categories without a culturally-specific misconception
      taxonomy. Source: NCERT journal error analysis — [WEB-13];
      CBSE-EI competency booklets — [WEB-14]'
  OO_equal_weight_damr:
    priority: MODERATE
    description: DAMR scoring treats all eight dimensions equally. Indian teachers'
      acceptability judgments are anchored primarily on 'providing guidance.' The
      equal-weight aggregate score cannot be directly used as a deployment validity
      proxy without re-weighting.
    verification_target: '[NOT FOUND — no published MRBench variant applying dimension-weighted
      DAMR or any re-weighting calibrated to teacher populations found. A 2025 follow-on
      survey paper on ITS evaluation (arxiv.org/html/2510.22581v1) cites MRBench but
      does not propose weighted scoring. Per-dimension DAMR scores are reported separately
      in MRBench, enabling manual re-weighting in analysis, but no systematic re-weighting
      methodology has been published.]'
  IC_subnational_school_type_variation:
    priority: MODERATE
    description: Target population spans Delhi and Mumbai with unspecified board distribution
      (CBSE, ICSE, Maharashtra State Board, IB). Pedagogical expectations for acceptable
      guidance vary across boards. This granularity is unresolved.
    verification_target: 'Partial resolution: All Delhi government schools are CBSE-affiliated;
      Mumbai government schools are predominantly Maharashtra State Board (SSC). Private
      school distribution in both cities spans CBSE, ICSE, and a small number of IB
      schools. No city-level proportional teacher count by board type is available
      in public data. Source: CBSE Wikipedia — [WEB-3];
      ICSE school count — [WEB-4]'
cultural_norms_notes: 'Indian professional teachers in this deployment operate within
  a pedagogical culture that differs systematically from the Western-default assumptions
  embedded in MRBench:

  - Direct instructional correction is normative and valued; Socratic probing is used
  more sparingly

  - Exam-readiness is a central frame for evaluating whether guidance is ''acceptable''

  - Teacher authority is central to the interaction model; student-led discovery has
  lower cultural salience than in Western constructivist frameworks

  - Hierarchical classroom relationships mean students are less likely to verbalize
  confusion or push back on tutor responses

  - Professional identity of Indian teachers is strongly tied to content mastery and
  examination outcomes, which shapes their evaluation criteria for AI-augmented tutoring

  - Language context: many teachers navigate between English (professional evaluation
  language) and Hindi, Marathi, or other regional languages in daily instruction,
  which may affect their sensitivity to L1-interference errors in student mathematical
  communication

  - India-based research on teacher-AI collaboration confirms that Indian educators
  value time-saving potential of generative tools but face usability barriers including
  misalignment with school routines and absence of vernacular content (Sebastian et
  al., 2024, cited in [WEB-15])'
domain_specific_notes:
  mathematics_education: Grade 1–8 mathematics in Indian metropolitan schools covers
    arithmetic, basic algebra, geometry, and early number theory, broadly aligned
    with NCERT/CBSE scope and sequence. Curriculum-agnostic errors are accepted as
    sufficient for this deployment, but procedural error types (carrying, borrowing,
    place-value errors including lakh/crore conventions) are culturally salient even
    if not required by the benchmark.
  place_value_conventions: Indian number system uses lakhs and crores rather than
    millions and billions; this is a culturally specific arithmetic convention. However,
    the user confirmed curriculum-agnostic errors are sufficient, so this is noted
    for context rather than as a blocking validity concern.
  exam_culture: '[NEEDS VERIFICATION — deferred: below search budget; specific CBSE
    board exam formats for Grade 1–8 (school-level annual exams, continuous assessment
    patterns post-CCE) require detailed CBSE circular review beyond current budget.
    The general structure is well-established but specific rubric formats relevant
    to ''exam-ready guidance'' are not publicly catalogued in searchable form.]'
  private_tutoring_ecosystem: '[NEEDS VERIFICATION — deferred: likely unsearchable
    (lived practice); the role of the coaching/tutoring center ecosystem (e.g., Byju''s,
    Vedantu, in-person coaching centers) in shaping teacher expectations of one-on-one
    tutoring guidance norms is not documented in searchable form in ways that distinguish
    metro professional teacher expectations from student/parent expectations.]'
  AI_in_education_india: 'NEP 2020 explicitly supports AI integration; CBSE has introduced
    AI as a formal subject from Class VI (15-hour module) and optional elective for
    Classes IX–XII. The Union Budget 2025–26 allocated ₹500 crore for a dedicated
    Centre of Excellence in AI for Education. DIKSHA platform uses AI for content
    search and accessibility. No specific NCERT or CBSE regulatory guidance on AI-assisted
    one-on-one tutoring tools (as distinct from AI as a curriculum subject) has been
    issued as of available sources. India-based AI tutoring deployments (e.g., Shiksha
    Copilot in Karnataka) highlight the importance of curriculum alignment, vernacular
    support, and teacher agency as critical success factors. Source: PIB — [WEB-8];
    arxiv Teacher-AI Collaboration — [WEB-15]'
net_new_fields:
  mathtutorbench_2025:
    description: 'MathTutorBench (Macina et al., EMNLP 2025 Oral) is a directly relevant
      new benchmark for holistic evaluation of open-ended pedagogical capabilities
      of LLM tutors in mathematics, released after MRBench. It covers three high-level
      teacher skills and seven concrete tasks, uses a reward model trained on expert
      vs. novice teacher responses, and finds that subject expertise and pedagogical
      ability trade off against each other. Like MRBench, MathTutorBench is grounded
      in Western academic datasets and learning-science principles (including Socratic
      questioning) with no documented adaptation to Indian classroom norms or non-Western
      pedagogical models. Its reward model operationalizes ''good tutoring'' as withholding
      answers and using Socratic questioning, reinforcing the same Western pedagogical
      default as MRBench. Relevant as a validity comparator: a deployment seeking
      India-appropriate benchmarking cannot directly substitute MathTutorBench for
      MRBench without the same cultural validity concerns. Source: arXiv 2502.18940
      — [WEB-16]; ACL Anthology EMNLP 2025 — [WEB-17];
      GitHub — [WEB-18]'
    deployment_relevance: 'Confirms that the field''s current best benchmarks for
      math tutoring evaluation (MRBench, MathTutorBench) share the same cultural provenance
      gap: both are Western-default, Socratic-scaffolding-oriented, and lack any Indian
      or South Asian pedagogical adaptation. This strengthens the IC and OC gap assessments
      in the validity summary.'
  india_ai_tutoring_deployment_evidence:
    description: 'A 2025 study on teacher-AI collaboration in Indian classrooms (Shiksha
      Copilot, Karnataka) found that Indian teachers valued AI tools for time-saving
      but faced critical barriers: misalignment with school routines, absence of vernacular
      content, and long response times. Teachers required AI outputs to align with
      state-mandated curriculum frameworks and the 5E pedagogical format. This is
      direct evidence that Indian teachers'' pedagogical expectations for AI-generated
      guidance differ structurally from Western defaults, corroborating the OC validity
      gap. Source: arXiv 2507.00456 — [WEB-15]'
    deployment_relevance: 'Provides empirical grounding (beyond elicitation) for the
      OC gap: Indian teachers actively evaluate AI outputs against curriculum-specific
      and institutional norms that benchmarks like MRBench do not operationalize.'
  ncert_new_curriculum_ganita_prakash:
    description: 'NCERT introduced a new Class 8 Mathematics textbook ''Ganita Prakash''
      (2024–25) as part of NEP 2020 curriculum reform, emphasising exploration of
      mathematical patterns and Indian mathematical heritage alongside procedural
      learning. An AI-crafted curriculum for Classes 3–8 in Mathematics, Science,
      and Social Science was approved in July 2025 for rollout via DIKSHA and PM eVidya.
      These reforms signal a policy shift toward more conceptual and inquiry-based
      learning, but teacher classroom practice typically lags curriculum reform by
      several years. Source: EduRev Ganita Prakash — [WEB-11];
      myidcm.com AI curriculum — [WEB-10]'
    deployment_relevance: 'Caveat on the pedagogical norms described in this document:
      the prevailing rote-procedural, exam-oriented norms described are accurate for
      current practice, but NEP 2020 and NCERT reforms are actively pushing toward
      more conceptual instruction. The deployment''s target teacher population may
      be in transition, and this should be noted as a temporal caveat on the OC gap
      characterization.'
  pedagogy_driven_its_evaluation_survey_2025:
    description: 'A 2025 survey paper on pedagogy-driven evaluation of generative
      AI-powered ITS (accepted at Springer, arXiv 2510.22581) explicitly notes the
      absence of reliable, universally accepted, pedagogy-driven evaluation frameworks
      and confirms that most existing ITS evaluations rely on non-standardized benchmarks
      with limited generalizability. It cites MRBench as a step toward unification
      but identifies the lack of domain coverage and interaction depth as ongoing
      limitations. No India-specific or cross-cultural ITS evaluation framework is
      cited. Source: arXiv 2510.22581 — [WEB-19]'
    deployment_relevance: 'Confirms the field-level assessment: there is no published
      AI tutoring benchmark with documented validity for Indian classroom contexts.
      The gap identified in this document (IC, OC) is not a local assessment artifact
      but a field-wide limitation.'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.asiancollegeofteachers.com/blogs/1524-Teaching-License-In-India-What-It-Is-And-How-Do-You-Renew-It-blog.php |
| WEB-2 | https://testbook.com/ctet/eligibility-criteria |
| WEB-3 | https://en.wikipedia.org/wiki/Central_Board_of_Secondary_Education |
| WEB-4 | https://candidschools.com/icse-schools-in-india-a-state-wise-list/ |
| WEB-5 | https://muftinternet.com/blog/usage-statistics-internet-and-mobile-users-in-india-2025/ |
| WEB-6 | https://www.storyboard18.com/digital/660-million-smartphone-users-16-17-billion-monthly-upi-transactions-power-digital-bharat-report-89731.htm |
| WEB-7 | https://datareportal.com/reports/digital-2024-india |
| WEB-8 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2234853&reg=3&lang=1 |
| WEB-9 | https://educationforallinindia.com/artificial-intelligence-in-indian-school-education-use-misuse-and-preventive-measures/ |
| WEB-10 | https://www.myidcm.com/blog/artificial-intelligence-course-in-india |
| WEB-11 | https://edurev.in/courses/118419_Mathematics-Ganita-Prakash-Class-8-New-NCERT |
| WEB-12 | https://ciet.ncert.gov.in/activity/eaie |
| WEB-13 | https://ejournals.ncert.gov.in/index.php/tpt/article/download/1323/1261 |
| WEB-14 | https://www.scribd.com/document/628027385/CFPQ-Maths10 |
| WEB-15 | https://arxiv.org/html/2507.00456v1 |
| WEB-16 | https://arxiv.org/abs/2502.18940 |
| WEB-17 | https://aclanthology.org/2025.emnlp-main.11/ |
| WEB-18 | https://github.com/eth-lre/mathtutorbench |
| WEB-19 | https://arxiv.org/html/2510.22581v1 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark focuses on mathematics mistake remediation in a general (Western-default) curriculum context. For your Grade 1–8 teachers in Delhi and Mumbai, do the student mistake scenarios need to reflect the Indian curriculum (e.g., NCERT/CBSE topics, Indian arithmetic conventions like the Indian place-value system with lakhs and crores, or standard algorithms taught differently in Indian textbooks)? Or would curriculum-agnostic math errors be sufficient for evaluating pedagogical quality?
A1: Curriculum-agnostic math errors are sufficient for evaluating pedagogical quality in this deployment context; strict alignment to the Indian curriculum is not required.

Q2 [IC]: The benchmark's student-tutor conversations were drawn from existing English-language datasets likely reflecting Western classroom dynamics. For your professional teachers in Indian metros, would the depicted student mistakes, student communication styles, or classroom interaction norms feel realistic and recognisable — or do you expect meaningful differences?
A2: The mathematical content feels broadly familiar, but the communication dynamics are meaningfully mismatched. Indian students tend to be more brief and deferential and less likely to verbalize reasoning, while Indian teachers use more direct, exam-oriented correction rather than extended Socratic dialogue. Procedure-heavy learning patterns and language-related misunderstandings common to Indian students are underrepresented in the benchmark's Western-sourced conversations.

Q3 [OO]: The benchmark scores pedagogical quality across eight dimensions. For your teachers evaluating whether an augmented GPT-4 response is 'acceptable,' which dimensions matter most — and are there dimensions the benchmark may be missing that teachers would actually judge responses on?
A3: The eight benchmark dimensions are considered necessary and sufficient for this deployment. "Providing guidance" is identified as the single most critical dimension for evaluating acceptability in student mistake remediation.

Q4 [OC]: The benchmark's ground-truth annotations were produced by a general (likely non-Indian) annotator pool. Do you expect Indian professional teachers' judgments of guidance quality to systematically differ from those of Western educators?
A4: Yes, systematic differences are expected. Indian teachers are likely to value more direct correction, exam-readiness framing, and teacher-directed pedagogy over Socratic probing or conceptual exploration, reflecting distinct cultural, pedagogical, and institutional norms.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | LOWER | The user confirmed that curriculum-agnostic math errors are sufficient, and the benchmark's eight pedagogical dimensions are deemed necessary and sufficient, reducing concern about category-level misalignment. |
| IC | HIGH | The user confirmed meaningful mismatches in student communication style, interaction norms, and procedure-heavy learning patterns between the benchmark's Western-sourced conversations and Indian metro classroom dynamics. |
| IF | LOWER | Both the benchmark and deployment are text-only in English, a high-resource language the target population uses fluently; no signal-distribution mismatch is indicated. |
| OO | MODERATE | The eight dimensions are accepted as sufficient, but the user's emphasis on "providing guidance" as uniquely critical suggests that the benchmark's equal-weight scoring across dimensions may not reflect how Indian teachers actually prioritize acceptability judgments. |
| OC | HIGH | The user explicitly expects systematic differences between Indian teachers' judgments of guidance quality and those of the likely non-Indian annotator pool, driven by cultural, pedagogical, and exam-orientation factors. |
| OF | LOWER | The benchmark produces labels and scores, and the deployment involves tutor evaluation of categorical acceptability; the output modality mismatch is minimal. |

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
  "benchmark": "mrbench",
  "region": "Indian Metropolitan Grade 1–8 Mathematics Teachers (Delhi & Mumbai)",
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
