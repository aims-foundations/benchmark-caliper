I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **MRBench – A Benchmark for Evaluating AI Tutor Responses in Student Mistake Remediation** is valid for use in **Metropolitan India – Grade 1–8 Mathematics Tutoring (English-medium)**.

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
- **Domain**: Pedagogical evaluation of AI tutor responses in mathematics education
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2024

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### 1. Input Ontology
MRBench is scoped to a single well-defined educational task: student mistake remediation in
mathematics [Q1, Q111, Q112]. The benchmark formalizes the task as generating an appropriate
tutor response Tt+1 to a student's most recent utterance(s) containing a mistake or
confusion, given the full dialogue history [Q13, Q14]. The output of this task is assessed
across eight pedagogical dimensions drawn iteratively from learning sciences literature
[Q15, Q16, Q129]: encouraging active learning [Q17], adapting to student goals [Q18],
managing cognitive load [Q19], fostering motivation [Q20], mistake identification [Q21, Q22],
answer non-revelation [Q23], providing guidance [Q24], actionability [Q25], logical coherence
[Q26], appropriate tone [Q27], and human-likeness [Q29]. The taxonomy was refined iteratively,
with the pilot study confirming that these eight dimensions are necessary and sufficient for
evaluating mistake remediation [Q132]; additional dimensions such as grammaticality and empathy
were considered but excluded [Q131]. The benchmark covers both elementary and middle school
content [Q144, Q143], providing a mix of difficulty levels. However, the taxonomy is explicitly
scoped to mathematics and to mistake remediation only; the authors acknowledge it would need
verification and likely adaptation for other tasks or subjects [Q117, Q118, Q130]. The equal
analytical weight given to all eight dimensions does not encode the deployment-relevant
priority of "providing guidance" as a uniquely critical acceptability criterion for Indian
professional teachers.

### 2. Input Content
MRBench is compiled from two English-language datasets sourced from Western educational
contexts [Q41]. Bridge provides 60 partial dialogue interactions between real human tutors
and elementary-level students, grounded in fundamental mathematical operations like
multiplication and addition, with characteristically short conversation turns [Q44, Q45, Q46,
Q92]. MathDial provides 132 complete multi-turn conversations between a human tutor and an
LLM acting as a student, grounded in middle-school reasoning problems, with longer and more
structured response patterns [Q48, Q49, Q95]. Together these produce 192 benchmark instances
[Q52], described as making MRBench "both challenging and comprehensive" [Q97]. The student
communication register embedded in both source datasets reflects Western classroom dynamics:
students verbalize reasoning at length across multiple turns, engage in extended Socratic
dialogue, and present mistakes in forms characteristic of Western instructional environments.
The brief, deferential, procedure-heavy interaction styles of Indian Grade 1–8 students are
absent from the source data. Additionally, MathDial uses an LLM as the student interlocutor
[Q48], further distancing the benchmark's conversation instances from authentic student
behavior. Conversation topic metadata is available for Bridge but not for MathDial [Q145],
limiting the ability to assess subject-matter coverage. Manual inspection was applied to
ensure quality [Q51], but no documentation indicates that Indian classroom misconception
types or culturally grounded error patterns were considered in data selection.

### 3. Input Form
The benchmark is entirely text-based, with conversation inputs consisting of multi-turn
English dialogue histories of varying length and turn count [Q133, Q134, Q141, Q142].
Length is measured in characters, with Bridge conversations characteristically shorter
than MathDial ones [Q147, Q141]. A standardized prompt template adapted from Wang et al.
(2024a) was used to elicit LLM responses [Q133, Q134]. The text-only, English-language
format is well-matched to both the benchmark's intended use and the target Indian metro
deployment, where teachers and students are English-fluent and interaction is text-based.
No spoken, multimodal, or non-Latin script modalities are present or required. MathDial
conversations do not include topic metadata [Q145], which is a minor structural limitation
but does not constitute a modality mismatch. No significant input form validity concerns
arise for the target deployment.

### 4. Output Ontology
Each of the eight taxonomy dimensions is scored using a three-tier labeling system [Q58,
Q59], exemplified by "yes / to some extent / no" for mistake identification [Q59, Q60].
The desired label for each dimension is specified in the paper's Table 4 [Q128, Q65]. The
ontology incorporates a factual correctness gate: only factually correct guidance is counted
as useful for the DAMR score [Q84]. The "Tutor Tone" dimension collapses Neutral and
Encouraging into a combined "Non-offensive" label, which achieves 100% DAMR across all
tutors by construction [Q90]. The current annotation scheme focuses on the appropriateness
of individual tutor turns rather than downstream student learning gains [Q119]; the output
ontology explicitly does not capture post-conversation outcomes [Q120, Q121]. Dimension
interdependencies are acknowledged but were suppressed during annotation by instructing
annotators to treat all dimensions as orthogonal [Q30, Q116]. For the Indian deployment,
the equal-weight DAMR reporting across all eight dimensions does not reflect the
deployment-relevant prioritization of "providing guidance" as the dominant acceptability
criterion, nor does the ontology encode distinctions between Socratic scaffolding and
direct-correction guidance styles that Indian professional teachers would recognize as
categorically different.

### 5. Output Content
The annotation team comprised four annotators — two male and two female — all holding at
least a post-graduate degree in Computer Science and proficient in English [Q31]. The
authors explicitly state that teaching experience was not required, as the task was designed
to be assessable from the perspective of a potential user of AI tutors rather than a
practitioner teacher [Q32]. Annotation was conducted in-house to ensure quality control,
avoiding public crowdsourcing platforms [Q33], with comprehensive training including
interactive documents, oral instructions, and a structured quiz [Q34, Q135, Q136, Q137].
A two-phase pilot validated the taxonomy, with each annotator independently labeling the
same eight dialogues across all eight dimensions, yielding 544 annotations per annotator
[Q35, Q36, Q37, Q38]. Inter-annotator agreement reached Fleiss' kappa = 0.65 in the pilot
[Q39] and Cohen's kappa = 0.71 in the main annotation phase [Q61], indicating substantial
agreement — but this agreement is among a culturally homogeneous group of CS-educated
annotators affiliated with MBZUAI in Abu Dhabi [Q6], not among Indian professional
educators. No documentation indicates that any annotator had South Asian educational
expertise, familiarity with CBSE/NCERT pedagogy, or experience with exam-oriented
correction styles. LLM critics (Prometheus2 and Llama-3.1-8B) were also evaluated as
automated annotators [Q105], but their annotations proved unreliable for most pedagogical
dimensions, showing mostly negative correlation with human annotations [Q107, Q108, Q109].
The ground-truth labels therefore reflect the pedagogical priors of CS-trained, likely
non-Indian annotators, which the user has flagged as a source of systematic divergence from
Indian professional teachers' judgments of guidance quality.

### 6. Output Form
The benchmark produces categorical three-tier labels per dimension per response, aggregated
into DAMR scores (percentage of responses receiving the desired label) [Q64, Q65] and
Annotation Correlation (AC) scores based on Pearson's correlation between LLM and human
annotations [Q66, Q138]. Human annotations are treated as the gold standard [Q68]. DAMR
scores are reported separately for Bridge and MathDial subsets [Q149, Q150] and for each
tutor condition (novice human, expert human, and each of the seven LLMs) [Q67, Q83]. General
NLG metrics (BLEU, BERTScore, DialogRPT) are explicitly rejected as insufficient for
pedagogical evaluation because they ignore pedagogical values and require gold references
not always available [Q4, Q7, Q8], and because multiple valid responses may exist for any
given input [Q9]. The output form — categorical labels and aggregate percentages — is
well-suited to the deployment's binary acceptability judgments by professional teachers.
No output modality mismatch is present. The primary output form concern for the deployment
is structural rather than representational: the equal-weight DAMR summary statistic does
not surface dimension-level prioritization, making it difficult to use the benchmark score
directly as a proxy for Indian teachers' acceptability judgments without re-weighting.


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
| Q9 | 2 | output_form | "For a given input dialogue, there can be multiple valid, pedagogically correct ground truth responses, making detection of the optimal answer non-deterministic (Tack and Piech, 2022; Al-Hossami et al., 2024)." |
| Q10 | 2 | output_form | "Additionally, these metrics can be easily manipulated; for instance, simple responses like "Hello" or "teacher:" (Baladón et al., 2023; Jurenka et al., 2024) can inflate scores." |
| Q11 | 2 | input_ontology | "In this section, we first briefly overview and discuss the limitations of the existing general-purpose NLG metrics and then turn to pedagogically-oriented approaches to evaluation." |
| Q12 | 3 | input_content | "In this work, we focus on educational dialogues between a student and a tutor in the mathematical domain. Specifically, the conversations are grounded in students' mistakes or confusions, and the AI tutor aims to respond in order to remediate such mistakes or confusions." |
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
| Q39 | 5 | output_content | "To measure inter-annotator agreement, we computed Fleiss' kappa value, which for this annotation experiment equals 0.65, indicating substantial agreement." |
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
| Q53 | 6 | input_ontology | "We consider state-of-the-art LLMs of various sizes and capabilities, including: GPT-4 (Achiam et al., 2023), Gemini (Reid et al., 2024), Sonnet (Anthropic, 2024), Mistral (Jiang et al., 2023), Llama-3.1-8B and Llama-3.1-405B (Dubey et al., 2024), and Phi3 (Abdin et al., 2024)." |
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
| Q65 | 6 | output_form | "The desired labels for each dimension are detailed in Table 2." |
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
| Q85 | 8 | output_ontology | "At the same time, even incorrect or incomplete guidance can lead to certain actions on the part of the student and can foster their curiosity, thus providing them with learning opportunities." |
| Q86 | 8 | output_ontology | "This further demonstrates the need to treat the dimensions as independent." |
| Q87 | 8 | output_content | "In terms of the other qualities of the Expert responses, they do not normally reveal the answer and tend to include scaffolding; however, there are a small number of instances where they failed to identify the mistake or its location." |
| Q88 | 8 | output_content | "Overall, we conclude that human responses from Expert are significantly better than Novice." |
| Q89 | 8 | output_form | "Our findings on the Tutor Tone align with those of Wang et al. (2024a) – in task-oriented conversations, AI tutors tend to be more Neutral than Encouraging." |
| Q90 | 8 | output_ontology | "When we combine these two labels into "Non-offensive", the DAMR score reaches 100% as we observe no offensive responses from any LLMs or humans." |
| Q91 | 8 | output_form | "We observe high scores for most of the LLMs on human-likeness, which demonstrates their capability to generate human-like output with minimal or no grammatical and fluency mistakes, showing the timely nature of our study, which focuses more on in-depth semantic and pedagogical aspects of tutor responses rather than only on superficial attributes like grammaticality and fluency." |
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
| Q110 | 8 | output_content | "At the same time, we acknowledge that the experiments presented in this work are preliminary" |
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
| Q127 | 10 | input_ontology | "strongly believe that this study will help shed light on the current capabilities of LLMs in the context of educational dialogues, and the insights gained from this study may help mitigate issues related to the use of LLMs in the educational domain in the future." |
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
name: Metropolitan India – Grade 1–8 Mathematics Tutoring (English-medium)
abbreviation: IN-METRO-MATH-K8
deployment_context:
  description: GPT-4 augmented by human tutors, deployed as a one-on-one tutoring
    assistant via mobile application or enterprise software for students in grades
    1–8 in metropolitan Indian cities. Human tutors co-author responses; student satisfaction
    is the primary success criterion.
  primary_use_case: Student mistake remediation and guided practice in mathematics,
    NCERT-aligned, for ages approximately 6–14
  delivery_channels:
  - mobile application
  - enterprise software
  end_user_roles:
    primary: Students (grades 1–8, ages approximately 6–14) in metropolitan India
    secondary: Human tutors acting as co-authors and response quality evaluators
geography:
  country: India
  scope: Metropolitan cities (no specific sub-national region specified beyond 'metropolitan')
  representative_metros:
  - 'Delhi (highest density of CBSE schools among Indian cities; heavily CBSE-centric
    urban education landscape — Source: Pune Pulse / DNA India — [WEB-1])'
  - 'Mumbai / Mumbai Metropolitan Region (Maharashtra has ~3,815 CBSE schools; strong
    competitive exam culture — Source: ddhehamirpur.in — [WEB-2])'
  - 'Bengaluru (Karnataka hosts 2,000+ CBSE schools; many IT families prefer CBSE
    — Source: ddhehamirpur.in — [WEB-2])'
  - Chennai
  - Hyderabad
  - Kolkata
  - Pune
  sub_national_variation_note: The target population spans vastly different linguistic,
    socioeconomic, and pedagogical contexts across Indian metropolitan areas. No sub-national
    granularity was specified in the elicitation. In metros such as Bengaluru, Chennai,
    Hyderabad, Mumbai, and Pune, the education ecosystem is shared more evenly between
    CBSE, ICSE, and state boards, unlike Delhi where the landscape is heavily CBSE-centric.
    Downstream search should flag whether Indian metropolitan cohorts differ meaningfully
    in math tutoring expectations or communication style norms.
languages:
  instruction_language: English
  proficiency_level: Fluent English speakers (confirmed by elicitation)
  home_language_diversity_note: Students in Indian metros typically speak one or more
    Indian languages at home alongside English. Home language backgrounds may include
    Hindi, Tamil, Telugu, Kannada, Marathi, Bengali, and others depending on the city.
    L1-interference in mathematical reasoning and vocabulary may affect error typologies
    even in English-medium instruction.
  home_languages_by_metro: '[NEEDS VERIFICATION — deferred: below search budget; requires
    city-level census or NSSO sub-national linguistic data not readily queryable in
    aggregate form]'
  medium_of_instruction: English (confirmed by elicitation as the deployment language)
writing_systems:
  scripts_in_use:
  - Latin (English)
  note: Interaction is text-based in English using the Latin script. No script mismatch
    with the benchmark. Numerals follow Indian conventions (see curriculum_notes).
target_population_demographics:
  age_band: Approximately 6–14 years
  grade_band: Grades 1–8
  school_board_types:
  - 'CBSE (dominant in metros; Delhi is most CBSE-dense city; all CBSE schools follow
    NCERT curriculum — Source: Wikipedia CBSE article — [WEB-3];
    veclakhanpur.in — [WEB-4])'
  - ICSE
  - IB
  - 'State boards (co-dominant with CBSE in Chennai, Hyderabad, Bengaluru, and Mumbai
    — Source: Pune Pulse — [WEB-1])'
  school_board_distribution_note: 'CBSE is the single most prevalent board in Indian
    metros, with approximately 25.3 million enrolled students nationally and 20,800+
    affiliated schools as of 2026. Delhi is the most CBSE-dense city; in other metros
    (Bengaluru, Chennai, Hyderabad, Mumbai, Pune), education ecosystems are more evenly
    split between CBSE, ICSE, and state boards. For this deployment, CBSE/NCERT alignment
    is the instructional reference standard. Source: modelpapers2021.in — [WEB-5];
    Pune Pulse — [WEB-1]'
  socioeconomic_profile: 'Metropolitan school students; likely skewed toward middle-
    and upper-middle-income families given mobile/enterprise software access. Only
    approximately 12% of CBSE students nationally are in government schools; the rest
    are in private or aided institutions, suggesting the deployment cohort skews toward
    private-school urban families. Source: modelpapers2021.in — [WEB-5]'
  device_access: 'Mobile phone usage in urban India is 97.6% (ages 15–29 per Comprehensive
    Modular Survey 2025); 97.6% of urban youth in this age group own a smartphone.
    Direct data for ages 6–14 is not publicly available at metro level; household-level
    mobile data access is high in urban India (approximately 80% of homes connected
    by 2023). These figures are national/urban-aggregate; metro-specific rates for
    primary school children are [NOT FOUND — searched PIB, NSSO, and ICEA sources;
    no city-specific device-ownership data for the 6–14 sub-cohort published]. Sources:
    PIB Comprehensive Modular Survey 2025 — [WEB-6];
    Data For India — [WEB-7]'
  internet_penetration_metros: 'Approximately 95.7% of urban Indian youth (ages 15–29)
    used the internet in the last three months as of 2025 (Comprehensive Modular Survey,
    PIB). National-level internet penetration stood at approximately 55–65% across
    all ages and regions combined as of 2025, with urban areas significantly higher.
    Metro-specific broadband penetration for the school-age cohort is not separately
    published. Source: PIB — [WEB-6];
    DataReportal Digital 2025 India — [WEB-8]'
  literacy_rate_india_national: '[NEEDS VERIFICATION — deferred: low impact for scoring
    given deployment population is confirmed English-fluent metropolitan students;
    national literacy rate is not the binding constraint here]'
  digital_literacy_children_metros: '[NOT FOUND — searched NSSO, NCERT, and related
    sources; no validated metro-specific digital literacy rate for Grade 1–8 children
    published. Rural digital literacy is approximately 27% per one industry source,
    but metro figures for this age cohort are not available in a form that would meaningfully
    change the assessment.]'
curriculum_and_pedagogy:
  curriculum_alignment: NCERT (National Council of Educational Research and Training)
    — confirmed required by elicitation
  ncert_grade_band_topics:
    grades_1_to_5: 'Foundational arithmetic: counting, place value, addition, subtraction,
      multiplication, division, basic fractions, measurement, simple geometry'
    grades_6_to_8: Rational numbers, integers, algebraic expressions, linear equations,
      geometry (triangles, quadrilaterals, circles), data handling, percentages, ratio
      and proportion, mensuration
    notes: 'NCERT has introduced new textbooks for Class 3 (2024–25) emphasizing activity-based
      learning and foundational skills; new textbooks for Class 6 are also being rolled
      out with bridge courses and deeper practical applications. AI has been introduced
      as a skill-based subject in Classes 8 and above. NCERT''s own AI Integration
      Manual outlines 7 markers for AI integration across K–12, explicitly emphasizing
      real-life Indian examples in mathematics. Source: Vedantu NCERT Solutions —
      [WEB-9]; ai4education.in — [WEB-10]'
  numeral_naming_conventions:
    required: true
    conventions:
    - Lakhs (1,00,000)
    - Crores (1,00,00,000)
    - Indian place-value grouping system (2-digit grouping above hundreds)
    - Rupee (₹) as currency unit in word problems
    notes: NCERT content explicitly uses Indian numeral naming conventions and rupee-denominated
      problems. Benchmark source datasets (Bridge, MathDial) are Western-sourced and
      do not reflect these conventions — a confirmed ontological gap.
  culturally_grounded_contexts_required: true
  required_context_examples:
  - Cricket scores and statistics
  - Local market transactions
  - School fee calculations
  - Train timetables
  - Rupee-based pricing problems
  - Cooking/recipe measurements (common in NCERT word problems)
  - Shopping discounts and profit/loss (standard NCERT middle-school content)
  prohibited_context_types: Culture-distant Western examples (e.g., baseball statistics,
    US grocery prices, American school scenarios) — confirmed inappropriate by elicitation
  algorithmic_conventions:
    note: Indian standard algorithms for arithmetic (e.g., long division layout, column
      addition/subtraction format) may differ from Western conventions used in benchmark
      source datasets.
    details: '[NEEDS VERIFICATION — deferred: requires expert elicitation or curriculum
      document review; specific algorithmic layout differences (e.g., long division
      column orientation, carrying conventions) are not documented in publicly searchable
      sources at the level of detail needed]'
  dominant_pedagogical_tradition:
    description: Indian primary and middle school mathematics instruction has historically
      emphasized procedural fluency, rote memorization, exam-oriented drilling, and
      direct correction by teachers. India's own National Curriculum Framework 2023
      explicitly identifies 'rote memorisation, narrow goals, and inadequate resources'
      as serious challenges in Indian education. NCERT's National Achievement Survey
      shows math scores dropping from 57% in Class 3 to 44% in Class 5 and 36% in
      Class 8 nationally, indicating cumulative procedural-gap accumulation consistent
      with rote-learning patterns. Socratic scaffolding and extended student verbalization
      — common in Western tutoring benchmarks — are less characteristic of Indian
      classroom norms.
    implications_for_benchmark: MRBench's evaluation taxonomy implicitly favors Socratic
      guidance (non-revelation of answers, extended student reasoning) over direct
      instructional correction. This operationalization may not align with Indian
      teachers' acceptability judgments.
    empirical_basis: 'India''s National Curriculum Framework 2023 explicitly flags
      rote memorisation as a systemic challenge (Source: cbseguess.com citing NCF
      2023 — [WEB-11]).
      NAS 2021 math score trajectory (57% Cl.3 → 36% Cl.8) is consistent with procedural-gap
      accumulation under rote-learning regimes (Source: Drishti IAS citing MoE NAS
      2021 — [WEB-12]).
      No peer-reviewed empirical study specifically comparing Socratic vs. direct-correction
      preferences among Indian primary-school math tutors was found within search
      budget — this specific sub-claim requires expert/stakeholder elicitation.'
  exam_orientation:
    relevant_exams:
    - CBSE board examinations (Class 10 and Class 12)
    - School-level term assessments (internal)
    - 'National Achievement Survey (NAS) — government benchmark for Classes 3, 5,
      8, 10 (Source: nas.gov.in — [WEB-13])'
    - Competitive entrance exam pipelines (JEE/NEET) — begin influencing CBSE school
      choices from Grade 8 onwards
    note: Exam-readiness framing may be a culturally salient criterion for judging
      tutor response quality that is absent from the benchmark's taxonomy. The CBSE
      board allocates marks for intermediate solution steps, making step-by-step correctness
      particularly valued in this context.
cultural_norms_notes: 'Key cultural factors relevant to tutoring satisfaction in metropolitan
  Indian Grade 1–8 contexts:

  - Hierarchical teacher-student relationship: students are socialized to show deference
  to teachers; direct correction by authority figures is normalized and expected

  - Warmth register: encouragement that feels culturally appropriate to Indian students
  may differ from generic motivational language; formulaic Western encouragement phrases
  may feel distant or hollow

  - Face-saving norms: public identification of errors must be handled sensitively;
  mistake remediation framing should preserve student dignity

  - Parental and family involvement: metropolitan Indian parents are often highly
  engaged with academic performance; tutor tone may be evaluated partly through parent-mediated
  student feedback

  - Exam culture: student satisfaction may be partially mediated by perceived exam-readiness
  of tutor guidance, not just conceptual clarity. CBSE even allocates step-wise marks,
  making procedural scaffolding culturally salient

  - Communication register: brief, directive tutor turns may be more culturally consonant
  than extended Socratic dialogues for younger grades

  - Rote-learning heritage: India''s National Curriculum Framework 2023 explicitly
  identifies rote memorisation as a systemic educational challenge; this shapes the
  error typology students bring to tutoring interactions (Source: NCF 2023 as cited
  in cbseguess.com — [WEB-11])

  - Empirical work on Indian AI-tutoring communication norms: [NOT FOUND — no peer-reviewed
  study on Indian primary/middle-school student interaction style with AI tutors was
  found within search budget; this is a documented evidence gap, not an absence of
  the phenomenon]'
student_interaction_style:
  description: Indian Grade 1–8 students in metropolitan contexts typically exhibit
    brief, deferential interaction turns in tutoring contexts. Extended student verbalization
    of reasoning across multiple dialogue turns — characteristic of MathDial and Bridge
    benchmark instances — is not well-documented for this population.
  typical_turn_length: '[NOT FOUND — no empirical study specifically measuring Indian
    Grade 1–8 student turn length in math tutoring (human or AI-mediated) was surfaced
    in searches. This is a genuine evidence gap requiring in-deployment observational
    study or stakeholder input.]'
  error_presentation_style: 'Errors are likely to be procedural (wrong step execution,
    place-value errors, algorithmic missteps) rather than conceptual reasoning errors,
    reflecting rote-procedure instruction. India''s NCF 2023 explicitly identifies
    rote memorisation as producing students who ''memorised patterns'' that ''don''t
    apply'' when problems are rephrased (Source: cbseguess.com — [WEB-11]).
    NAS 2021 data shows math scores drop sharply from Class 3 to Class 8, consistent
    with cumulative procedural-gap accumulation. L1-interference may produce characteristic
    misconception types not present in Western-sourced benchmark data.'
  common_misconception_types: 'No dedicated academic literature specifically cataloguing
    Indian Grade 1–8 NCERT-aligned math misconception typologies was found. General
    K–8 misconception research (Western) identifies: equal-sign-as-operator errors,
    fraction-addition-by-adding-numerators-and-denominators, place-value errors in
    multi-digit operations, and rote-rule overgeneralization (e.g., ''always write
    the bigger number on top''). For Indian CBSE/NCERT students, rote-learning artifacts
    are expected to produce additional error types: formula recall without understanding
    (inability to reapply when problem is rephrased), procedural execution errors
    in multi-step NCERT algorithms, and errors arising from Indian numeral grouping
    conventions (lakhs/crores confusion) not present in Western benchmarks. Source
    for general misconception literature: Mathnasium — [WEB-14];
    NCF 2023 rote-learning characterisation: cbseguess.com — [WEB-11].
    A dedicated India-specific AI tutoring misconception benchmark does not appear
    to exist.'
success_criterion:
  primary_metric: Student satisfaction (not pedagogical correctness per se)
  joint_requirement: A response must be BOTH pedagogically sound AND culturally appropriate
    to count as satisfying — confirmed by elicitation (A4). Pedagogically correct
    but culturally distant or overly formal responses do not meet the deployment success
    criterion.
  judges:
    primary: Human tutors (co-authors) — evaluate pedagogical soundness and cultural
      appropriateness
    secondary: Student engagement signals (implicit satisfaction indicators)
  alignment_with_benchmark_annotators: Partial. Metropolitan Indian student satisfaction
    judgments are expected to largely align with MRBench annotators on pedagogical
    correctness dimensions, but divergence is expected on tone, warmth register, and
    culturally appropriate communication style. MRBench annotators are CS-educated
    MBZUAI affiliates with no documented South Asian educational expertise or NCERT
    familiarity.
  satisfaction_construct_validation: '[NOT FOUND — no validation study linking MRBench
    scores or equivalent pedagogical rubric scores to learner-reported satisfaction
    for Indian or other non-Western student populations was found. This is a genuine
    evidence gap: the benchmark measures annotator-judged pedagogical correctness;
    no published study validates this as a proxy for Indian student satisfaction.]'
infrastructure_notes: '- Deployment is via mobile application and/or enterprise software
  in Indian metropolitan areas

  - Urban mobile phone usage is 97.6% (Comprehensive Modular Survey 2025 — [WEB-6]);
  approximately 80% of Indian homes were connected to the internet by 2023 (Data For
  India — [WEB-7]). Metro-specific connectivity
  for the 6–14 cohort is not disaggregated in published data.

  - Mobile internet connectivity in Indian metros is generally strong; 92.3% of Indian
  mobile connections are 3G/4G/5G broadband (DataReportal Digital 2025 — [WEB-8]).
  Bandwidth variability during peak school hours is not documented at city level.

  - Enterprise software channel suggests some deployments may be school- or institution-mediated,
  with institutional device or network constraints. This is consistent with CBSE schools
  using school-managed EdTech platforms.

  - Text-based interaction in English only; no speech, image, or multilingual modality
  required by deployment

  - Data localization and child data protection requirements under India''s DPDPA
  2023 and DPDP Rules 2025 apply: see regulatory notes below.'
regulatory_and_compliance_notes:
  applicable_data_protection_law: 'India''s Digital Personal Data Protection Act,
    2023 (DPDPA 2023) applies to any entity processing digital personal data collected
    online or digitised offline in India, including EdTech platforms offering tutoring
    services to Indian users. The Act received Presidential assent on August 11, 2023
    and is the country''s first comprehensive data protection regime. The Digital
    Personal Data Protection Rules, 2025 (DPDP Rules) operationalise its provisions.
    Source: DPDPA official text via MeitY — [WEB-15];
    PRS India analysis — [WEB-16]'
  child_data_protection_provisions: 'Under Section 9 of DPDPA 2023, a ''child'' is
    any individual below 18 years of age — a threshold higher than GDPR. Key obligations
    for EdTech platforms serving this deployment''s entire student cohort (ages 6–14):
    (1) Verifiable parental consent is mandatory before processing any child''s personal
    data; simple checkboxes or declarations are insufficient — Aadhaar-linked Digital
    Locker tokens or equivalent are required; (2) Behavioural tracking, targeted advertising,
    and profiling of children is prohibited even with parental consent; (3) Non-compliance
    penalties can reach ₹150–200 crore per violation for children''s data provisions;
    (4) Large EdTech platforms may be designated Significant Data Fiduciaries (SDFs)
    with additional governance obligations. Source: KSA&NK legal analysis — [WEB-17];
    DPDPA Section 9 commentary — [WEB-18];
    EdTech-specific DPDP compliance analysis — [WEB-19]'
  edtech_platform_classification: 'EdTech platforms deploying AI tutoring tools may
    function as Data Processors (when acting under school/institutional instructions)
    or as independent Data Fiduciaries (when determining their own processing purposes,
    e.g., training AI models, analytics). An EdTech company that trains AI on student
    interaction data or builds learning analytics independently becomes a Data Fiduciary
    with full DPDPA obligations. Source: KSA&NK — [WEB-19]'
  education_sector_regulations: 'NCERT''s AI Integration Manual (published under Ministry
    of Education auspices) explicitly endorses AI integration into K–12 mathematics,
    with an emphasis on India-specific real-life examples and a mandate to ''move
    away from rote learning.'' No Ministry of Education, UGC, or NCERT-specific regulatory
    prohibition on AI tutoring in K–8 settings has been identified; the current regulatory
    frame is DPDPA-centered rather than AI-use-specific for this sector. Source: ai4education.in
    summarising NCERT AI Integration Manual — [WEB-10]'
  edtech_regulatory_context: '[NEEDS VERIFICATION — deferred: DPIIT-specific guidance
    on AI-assisted tutoring post-2023 may exist but was not reached within search
    budget; the primary actionable compliance framework is the DPDPA 2023 and DPDP
    Rules 2025 documented above]'
benchmark_validity_concerns:
  curriculum_ontology_mismatch:
    severity: HIGH
    description: MRBench is derived from Bridge (Western elementary arithmetic) and
      MathDial (Western middle-school reasoning). Neither dataset is aligned to NCERT
      Grade 1–8 topics, Indian numeral naming conventions (lakhs/crores), or rupee-based
      word problems.
    search_target: '[NOT FOUND — no existing math tutoring benchmark covering NCERT
      Grade 1–8 topics, Indian numeral conventions, and rupee-based word problems
      was identified. VIRAASAT (arxiv.org/abs/2602.18429) is the closest Indian cultural
      reasoning benchmark found, but it targets general cultural QA (history, festivals,
      cuisine, etc.) across 28 states and does not cover NCERT math tutoring content.
      Source: arXiv VIRAASAT — [WEB-20]. This is a confirmed
      evidence gap: no NCERT-aligned math tutoring benchmark exists in the public
      literature.]'
  cultural_context_mismatch:
    severity: HIGH
    description: Benchmark instances embed Western contextual framings (US school
      scenarios, dollar-denominated problems). Deployment requires Indian everyday
      contexts (cricket, local markets, school fees). No India-specific word problems
      are documented in Bridge or MathDial.
    search_target: '[NOT FOUND — no documentation of India-specific word problems
      in MathDial or Bridge datasets was found. No search result indicated any India-relevant
      student error typology in either source dataset. Confirms the cultural context
      mismatch as a full gap.]'
  satisfaction_vs_pedagogical_quality:
    severity: HIGH
    description: MRBench measures pedagogical correctness across eight dimensions;
      the deployment success criterion is student satisfaction. Cultural appropriateness
      and warmth are necessary conditions for satisfaction in this deployment but
      are not captured in the benchmark taxonomy.
    search_target: '[NOT FOUND — no validation study linking MRBench scores or equivalent
      pedagogical rubric scores to learner-reported satisfaction for Indian or non-Western
      student populations was found. AI Socratic tutors (e.g., Khanmigo) have been
      studied for learning gains but without Indian-cohort-specific satisfaction validation
      (Source: aicompetence.org — [WEB-21]).
      This gap remains unresolved in the public literature.]'
  annotator_representativeness:
    severity: HIGH
    description: MRBench annotators are four CS-educated MBZUAI affiliates in Abu
      Dhabi with no documented South Asian educational expertise. Ground-truth labels
      reflect non-Indian pedagogical priors. No Indian educators or students participated
      in annotation.
    search_target: '[NOT FOUND — no subsequent annotation study involving Indian educators
      or re-annotation of MRBench for Indian pedagogical priors was found. This remains
      a full gap. The VIRAASAT benchmark (arXiv 2025) demonstrates how Indian cultural
      knowledge requires expert-curated, India-specific annotation; MRBench has no
      equivalent Indian educator involvement. Source: VIRAASAT — [WEB-20]]'
  equal_weight_damr_scoring:
    severity: MODERATE
    description: DAMR reports equally across all eight dimensions. Indian teacher
      acceptability judgments may weight 'providing guidance' and 'cultural appropriateness'
      heavily; the benchmark provides no mechanism for dimension re-weighting.
    search_target: '[NOT FOUND — no dimension-weighting study for pedagogical AI evaluation
      in Indian or exam-oriented educational contexts was found within search budget.
      This remains a partial gap: the concern is structurally valid but lacks India-specific
      empirical grounding.]'
  western_misconception_types:
    severity: HIGH
    description: Neither Bridge nor MathDial was designed to include Indian student
      error patterns arising from rote-procedural instruction, L1-interference, or
      NCERT-specific algorithmic conventions. India's NCF 2023 explicitly identifies
      rote memorisation as producing procedural errors when problems are rephrased.
      NAS 2021 shows math scores dropping from 57% in Class 3 to 36% in Class 8, suggesting
      cumulative procedural gap accumulation not captured in Western benchmark error
      typologies.
    search_target: 'No dedicated India-specific AI-tutoring math misconception benchmark
      was found. General K–8 misconception literature (Western) documents equal-sign
      errors, fraction addition errors, place-value errors, and rote-rule overgeneralisation.
      India-specific rote-learning artifacts (formula recall failures on rephrased
      problems; Indian numeral-convention errors) are acknowledged in NCF 2023 and
      NAS 2021 but not captured in any AI tutoring benchmark. Source: cbseguess.com
      (NCF 2023) — [WEB-11];
      NAS 2021 via Drishti IAS — [WEB-12]'
  socratic_vs_direct_correction_bias:
    severity: MODERATE
    description: MRBench taxonomy implicitly favors Socratic scaffolding (non-revelation,
      extended student reasoning) over direct correction. Indian pedagogical tradition
      — shaped by exam culture, CBSE step-marking, and rote-learning heritage — may
      treat direct correction as acceptable or preferred, creating rubric misalignment.
    search_target: 'No peer-reviewed empirical study specifically comparing Socratic
      vs. direct-correction preferences among Indian primary/middle-school math teachers
      or students was found. General tutoring research notes that Socratic questioning
      can be frustrating for students accustomed to direct instruction, particularly
      weaker students (Source: aicompetence.org — [WEB-21]).
      The India-specific pedagogical preference for direct correction remains a claimed
      but empirically unvalidated concern requiring stakeholder/expert elicitation.'
domain_specific_notes: '- Mathematics domain only; no other subject areas are in scope

  - Grade band spans both foundational arithmetic (Grades 1–5) and pre-algebraic/reasoning
  content (Grades 6–8), matching the Bridge/MathDial split in MRBench but with different
  topic coverage

  - CBSE is the dominant board in Indian metro schools with approximately 25.3 million
  students nationally enrolled; Delhi has the highest city-level CBSE school density
  while other metros (Bengaluru, Chennai, Mumbai) show a more even split between CBSE,
  ICSE, and state boards (Source: modelpapers2021.in — [WEB-5];
  Pune Pulse — [WEB-1])

  - Human tutor co-authorship layer partially mitigates benchmark-deployment gaps
  by filtering culturally inappropriate outputs before student delivery

  - Warmth and encouragement are deployment-required properties; the benchmark''s
  Tutor Tone dimension collapses Neutral and Encouraging into ''Non-offensive'' (100%
  DAMR by construction), providing no discriminative signal on warmth quality

  - NAS 2021 data (national math scores: 57% Cl.3 → 44% Cl.5 → 36% Cl.8) provides
  a publicly available measure of learning outcomes against which AI tutoring effectiveness
  could be benchmarked in future validation studies. Source: nas.gov.in — [WEB-13];
  Drishti IAS — [WEB-12]

  - Sub-national metro variation (e.g., Mumbai vs. Delhi vs. Bengaluru) in tutoring
  norms and communication style is undocumented in peer-reviewed literature; downstream
  search or stakeholder elicitation should investigate whether metro-level cohort
  differences are empirically meaningful for this deployment'
net_new_fields:
  indian_cultural_reasoning_benchmark:
    name: VIRAASAT
    description: 'A semi-automated, symbolically-grounded QA benchmark for Indian
      cultural reasoning, covering 13 cultural attributes (history, cuisine, costume,
      festivals, sports, etc.) across all 28 states and 8 UTs, with 3,200+ multi-hop
      questions. Not math-tutoring-specific, but confirms that (a) no Indian-culture-specific
      math tutoring benchmark exists, and (b) zero-shot LLM performance on Indian
      cultural knowledge tasks is unreliable without fine-tuning. Indic models and
      SLMs performed weakest in zero-shot settings due to limited pretraining on long-tail
      Indian cultural entities. Relevance: confirms that benchmark cultural coverage
      gaps for India are a broader documented problem across AI evaluation, not unique
      to MRBench.'
    source: arXiv 2025 — [WEB-20]
  nas_2021_math_score_trajectory:
    description: 'India''s National Achievement Survey 2021 (NAS 2021) — conducted
      by NCERT/CBSE across 34 lakh students in 1.18 lakh schools nationally — found
      mathematics scores of 57% at Class 3, 44% at Class 5, 36% at Class 8, and 32%
      at Class 10. Urban schools significantly outperformed rural schools. This score
      trajectory is consistent with cumulative procedural gap accumulation under rote-learning
      regimes. NAS 2021 is the most recent national mathematics learning assessment
      and provides a publicly available calibration baseline for the Grade 1–8 target
      cohort. Note: NAS scores are national aggregates; metro-specific breakdowns
      exist in state/district report cards at nas.gov.in but were not retrieved within
      search budget.'
    source: NAS 2021 via Drishti IAS — [WEB-12];
      nas.gov.in — [WEB-13]
  dpdpa_child_data_key_provisions_summary:
    description: 'All students in this deployment (ages 6–14) qualify as ''children''
      under DPDPA 2023 (child = below 18 years). Key compliance implications for the
      tutoring platform: verifiable parental consent required before any data processing;
      behavioural profiling and targeted advertising prohibited even with consent;
      designation as Significant Data Fiduciary (SDF) possible if platform processes
      children''s data at scale with AI tools; penalties up to ₹150–200 crore for
      children''s data violations. The DPDP Rules 2025 operationalise these requirements.
      This is a high-impact compliance constraint with direct implications for how
      student interaction data may be used to train or fine-tune the AI tutoring system.'
    source: KSA&NK DPDP analysis — [WEB-17];
      DPDPA Section 9 — [WEB-18]
  ncf_2023_rote_learning_acknowledgement:
    description: 'India''s National Curriculum Framework 2023 (NCF 2023), published
      by the Ministry of Education, explicitly identifies ''rote memorisation, narrow
      goals, and inadequate resources'' as serious challenges in Indian education.
      This official policy acknowledgement provides authoritative grounding for the
      claim that Indian students in the Grade 1–8 cohort are likely to present procedural-error
      typologies rooted in rote instruction — typologies absent from the Western-sourced
      MRBench benchmark. Relevance: validates the HIGH-severity ''western_misconception_types''
      concern in the benchmark validity analysis.'
    source: cbseguess.com citing NCF 2023 — [WEB-11]
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.mypunepulse.com/which-indian-city-actually-leads-in-cbse-schools-a-closer-look-at-the-facts/ |
| WEB-2 | https://ddhehamirpur.in/which-state-has-the-most-cbse-schools-in-india |
| WEB-3 | https://en.wikipedia.org/wiki/Central_Board_of_Secondary_Education |
| WEB-4 | https://veclakhanpur.in/top-popular-schools-in-india-understanding-the-cbse-system |
| WEB-5 | https://modelpapers2021.in/how-many-students-are-there-in-cbse-board-in-india |
| WEB-6 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2132330&reg=3&lang=2 |
| WEB-7 | https://www.dataforindia.com/comm-tech/ |
| WEB-8 | https://datareportal.com/reports/digital-2025-india |
| WEB-9 | https://www.vedantu.com/ncert-solutions |
| WEB-10 | https://ai4education.in/ai-for-ncert%2Fcbse |
| WEB-11 | https://www.cbseguess.com/article/detail/why-most-students-struggle-with-cbse-mathematics-and-how-to-fix-it-33 |
| WEB-12 | https://www.drishtiias.com/daily-news-analysis/national-achievement-survey-nas-2021 |
| WEB-13 | https://nas.gov.in/about-nas |
| WEB-14 | https://www.mathnasium.com/math-centers/hydepark/news/common-math-misconceptions-k-8 |
| WEB-15 | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf |
| WEB-16 | https://prsindia.org/billtrack/digital-personal-data-protection-bill-2023 |
| WEB-17 | https://ksandk.com/data-protection-and-data-privacy/childrens-data-protection-under-indias-dpdp-rules/ |
| WEB-18 | https://www.dpdpa.com/dpdpa2023/chapter-2/section9.html |
| WEB-19 | https://ksandk.com/data-protection-and-data-privacy/dpdp-compliance-for-schools-and-edtech/ |
| WEB-20 | https://arxiv.org/html/2602.18429 |
| WEB-21 | https://aicompetence.org/ai-socratic-tutors/ |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Your students are in grades 1–8 in metropolitan India. Should the tutoring system handle content tied to the Indian school curriculum (e.g., NCERT-aligned topics, Indian numeral naming conventions like lakhs and crores, word problems referencing rupees or local contexts like train timetables)? Or is the math content entirely curriculum-agnostic in your deployment?
A1: The system must be tied to the Indian school curriculum. NCERT-aligned content, Indian numeral naming conventions, and locally grounded word problems are all required — the deployment is not curriculum-agnostic.

Q2 [IC]: Word problems and tutoring examples in Western benchmarks often use culturally specific contexts (e.g., baseball statistics, US grocery prices, American school scenarios). In your deployment, would students encounter these kinds of culture-distant examples, or would the system generate problems grounded in familiar Indian everyday contexts — like cricket scores, local market transactions, or school fee calculations?
A2: The system should generate problems grounded in familiar Indian everyday contexts (e.g., cricket, local markets, school fees). Culture-distant Western examples are not appropriate for this deployment.

Q3 [OC]: The benchmark's pedagogical quality labels were annotated by human raters — but the actual measure of success is student satisfaction. Who in the deployment context are the right judges of a "good" tutor response, and would their judgments align with the benchmark's annotators?
A3: The appropriate judges are human tutors (co-authors) and student engagement signals. Satisfaction judgments from a metropolitan Indian child are expected to largely align with benchmark annotators, though some divergence may occur due to cultural and educational context differences.

Q4 [OO]: The benchmark scores responses on pedagogical dimensions (guidance, tone, mistake identification), but the deployment goal is student satisfaction — which may depend on culturally specific warmth or communication style. Would a pedagogically correct but culturally distant or overly formal response still count as satisfying?
A4: No. A response must be both pedagogically sound and culturally appropriate to count as satisfying. Overly formal or culturally distant responses, even if pedagogically correct, would not meet the deployment's success criterion.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | MRBench derives from Western/general-context math datasets (MathDial, Bridge), and the deployment explicitly requires NCERT-aligned Indian curriculum categories — a clear ontological mismatch in topic coverage and numeral conventions. |
| IC | HIGH | Benchmark instances likely embed Western cultural contexts (US school scenarios, dollar-denominated problems), while the deployment requires Indian everyday contexts (cricket, rupees, local markets); this is a confirmed gap from A2. |
| IF | LOWER | Both benchmark and deployment are text-only in English, and the target population is fluent English-speaking; no modality or script mismatch exists. |
| OO | HIGH | The benchmark's eight pedagogical dimensions do not map cleanly onto student satisfaction as the deployment's success criterion; A4 confirms that cultural appropriateness and warmth are necessary conditions for a "good" response that the benchmark's output taxonomy does not capture. |
| OC | MODERATE | Human tutors and student engagement are the intended judges, and A3 indicates partial alignment with benchmark annotators — but cultural and educational context differences mean ground-truth labels from non-Indian raters may diverge on tone and style judgments for this population. |
| OF | LOWER | The benchmark outputs labels and scores which serve as intermediate evaluation signals; the deployment's output is free-form tutor text, but this mismatch is partially bridged by the human tutor co-authorship layer and is not the primary validity risk. |

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
  "region": "Metropolitan India – Grade 1–8 Mathematics Tutoring (English-medium)",
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
