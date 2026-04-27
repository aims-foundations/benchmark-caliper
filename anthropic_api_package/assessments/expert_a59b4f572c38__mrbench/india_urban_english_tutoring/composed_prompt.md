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
      — deferred: low impact relative to other gaps; sub-national school-type distribution
      data not published at city level for this specific teacher cohort]'
    professional_standing: 'For CBSE-affiliated schools, Grade 1–5 teachers (PRT)
      are typically required to hold D.El.Ed or equivalent; Grade 6–8 teachers (TGT
      Mathematics) typically require a subject-specific degree (BA/BSc with Mathematics)
      plus a B.Ed from an NCTE-recognised institution, and clearance of CTET or relevant
      State TET. Private CBSE schools may accept equivalent qualifications. Government
      Delhi schools recruit through DSSSB with similar criteria. (Source: CBSE teacher
      qualification framework — [WEB-1];
      Superprof India teacher roles overview — [WEB-2];
      DSSSB eligibility — [WEB-3]).
      ''High-end professional'' likely implies private metro school context where
      B.Ed plus subject degree is standard; IB/ICSE schools may additionally require
      international certifications.'
  estimated_population_size: '[NOT FOUND — searched for total Grade 1–8 math teacher
    count in Delhi and Mumbai formal sector; no city-specific disaggregated figure
    for mathematics teachers at this grade band was located in UDISE+ or NCERT reports.
    National figure is approximately 8–9 million school teachers total (UDISE+ 2021-22),
    but no city-level math-teacher-specific count was published at the required granularity.]'
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
    communication is a flagged validity gap for the benchmark's source datasets. NCERT
    has used AI/ML to translate Grade 1–2 textbooks into 22 Indian languages, indicating
    awareness of the multilingual instructional reality (Government of India PIB —
    [WEB-4]).
  hindi_math_register_notes: '[NEEDS VERIFICATION — deferred: likely unsearchable
    (lived practice); the extent to which bilingual Hindi/Marathi-medium instruction
    shapes Indian teachers'' interpretive frames for English-medium student errors
    is a matter of pedagogical socialization, not documented in online sources. Requires
    expert/stakeholder elicitation.]'
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
    board_distribution_in_target_cities: '[NEEDS VERIFICATION — deferred: below search
      budget; no published city-level proportional split of CBSE/ICSE/state board/IB
      schools for Grade 1–8 math teachers specifically found; national UDISE+ data
      does not disaggregate by subject or board at city level]'
    curriculum_alignment_requirement: User confirmed curriculum-agnostic math errors
      are sufficient for this evaluation; strict NCERT/CBSE alignment is NOT required
    ncert_textbook_revision_note: 'NCERT introduced a new textbook series ''Ganita
      Prakash'' (Parts 1 and 2) for Class 8 effective from the 2026–27 academic year,
      replacing the previous thirteen-chapter textbook. The previous textbook remains
      relevant for students following the earlier syllabus. This revision may alter
      the specific procedural content teachers expect students to master, though curriculum-agnostic
      errors remain sufficient for this deployment. (Source: Tiwari Academy NCERT
      Class 8 syllabus overview — [WEB-5])'
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
  india_specific_annotation_studies: '[NOT FOUND — searched for MRBench annotations
    involving Indian educators, and for cross-cultural comparisons of teacher AI-tutoring
    quality judgments; no such studies were located. This gap is corroborated by a
    2025 comprehensive review of ITS evaluation which noted that existing studies
    are ''conducted on small, homogeneous populations, primarily from WEIRD (Western,
    Educated, Industrialized, Rich, and Democratic) countries'' (Pedagogy-Driven Evaluation
    of Generative AI-Powered ITS, Springer/arXiv 2025 — [WEB-6]).
    No India-specific educator annotation of AI tutor quality exists in the published
    literature.]'
  inter_annotator_agreement_among_indian_teachers: '[NOT FOUND — no studies measuring
    Indian professional teachers'' agreement on AI tutor pedagogical quality judgments
    were located. This is an open research gap not addressed in the current ITS evaluation
    literature.]'
infrastructure_notes:
  deployment_format: Mobile and/or enterprise application; text-based interface
  language_interface: English text only; no spoken or multimodal interface described
  device_access: 'Mobile-first assumed; smartphone penetration in Delhi and Mumbai
    professional workforce is high — urban India smartphone penetration broadly estimated
    at over 75% (World Bank and GSMA data), with professional metro teachers likely
    near full coverage. Specific teacher-cohort figure not published. (Caveat: national
    figure; professional urban cohort penetration likely higher.)'
  internet_connectivity: 'Urban professional population in Delhi and Mumbai; broadband
    and mobile data access assumed adequate. A 2025 report noted that only 40% of
    schools in India overall have reliable internet for real-time AI applications,
    but this national average is heavily depressed by rural schools — urban private
    metro schools in Delhi and Mumbai are substantially better connected. (Source:
    educationforallinindia.com, citing NCERT 2023 data — [WEB-7]).
    Specific connectivity figures for the urban professional teacher cohort in these
    two cities not independently published.'
  enterprise_vs_consumer_split: '[NEEDS VERIFICATION — deferred: below search budget;
    likely unsearchable without internal deployment data from the application provider]'
school_system_context:
  board_types_present_in_target_cities:
    CBSE: Dominant national board; strong presence in Delhi; significant in Mumbai
      private schools; NCERT textbooks and syllabus
    ICSE: 'Present in elite private schools in both cities; more emphasis on conceptual
      depth than state boards [NEEDS VERIFICATION — deferred: below search budget;
      characterization is widely accepted but proportional data not found]'
    Maharashtra_State_Board: 'Dominant in Mumbai government and many private schools;
      Marathi-medium instruction common [NEEDS VERIFICATION — deferred: below search
      budget; proportion of target teachers from state board schools not published
      at city-teacher level]'
    Delhi_State_Board: '[NEEDS VERIFICATION — deferred: below search budget; Delhi
      government schools use Delhi Board of School Education (DBSE) which co-exists
      with CBSE; characteristics not searched]'
    IB: 'Present in small number of elite private schools; very different pedagogical
      norms; Socratic methods more valued [NEEDS VERIFICATION — deferred: below search
      budget; proportion of target teachers from IB schools not published]'
  board_specific_pedagogical_variation_note: Each board carries distinct pedagogical
    expectations for what constitutes acceptable tutoring guidance. The acceptability
    criterion for AI-augmented tutor responses may differ meaningfully across CBSE,
    ICSE, Maharashtra State Board, and IB contexts. The elicitation does not specify
    which boards the target teacher population primarily serves, and this sub-national
    granularity is a flagged gap.
  relevant_policy_frameworks:
    NEP_2020: 'NEP 2020 recognises AI''s potential for personalised learning and emphasises
      technology integration across all educational levels, including at school stage.
      It explicitly envisions AI-based software for student learning support. However,
      NEP 2020 does not prescribe specific AI tutoring protocols for Grade 1–8 mathematics
      nor does it mandate particular pedagogical models (direct instruction vs. Socratic)
      — its guidance is broad and aspirational rather than operationally specific
      for this deployment context. (Source: NEP 2020 full text, Ministry of Education
      — [WEB-8];
      PIB summary — [WEB-4])'
    NCERT_curriculum_revision: 'NCERT introduced ''Ganita Prakash'' (Parts 1 and 2)
      as the new Class 8 mathematics textbook series for 2026–27, continuing the NCF
      2023-aligned textbook revision cycle. The revision is ongoing across grade levels;
      Class 8 is the latest update. This may affect which specific procedural and
      conceptual errors teachers consider grade-appropriate, though the user confirmed
      curriculum-agnostic errors are sufficient. (Source: Tiwari Academy NCERT Class
      8 overview — [WEB-5])'
    digital_education_initiatives: 'India''s primary national digital education platform
      is DIKSHA (Digital Infrastructure for Knowledge Sharing), a Ministry of Education
      initiative that uses AI for inclusivity features (e.g., AI-based search, read-aloud).
      CBSE has introduced a 15-hour AI skill module from Class VI onwards and AI as
      an optional subject in Classes IX–XII. As of 2025, no specific NCERT or CBSE
      regulatory guidance for AI-assisted tutoring tools in Grade 1–8 mathematics
      classrooms was found; policy remains promotional rather than regulatory. (Source:
      Government of India PIB — [WEB-4];
      CBSE AI curriculum — [WEB-9])'
validity_gap_summary:
  IC_student_interaction_style:
    priority: HIGH
    description: MRBench source datasets (Bridge, MathDial) reflect Western classroom
      dynamics with extended student verbalization. Indian Grade 1–8 students are
      briefer, more deferential, and procedure-focused. Benchmark conversation structures
      may not be recognizable as realistic to Indian teachers.
    verification_target: '[NOT FOUND — no AI tutoring benchmarks specifically addressing
      Indian student interaction styles were located. A 2025 comprehensive ITS review
      confirmed that existing studies are conducted primarily on WEIRD-country populations
      (Springer/arXiv 2025 — [WEB-6]). MRBench includes
      no documentation of short-turn, low-verbalization student input scenarios; the
      gap is confirmed unaddressed in the current benchmark landscape.]'
  OC_annotator_representativeness:
    priority: HIGH
    description: Ground-truth labels reflect CS-trained MBZUAI annotators' pedagogical
      priors, not Indian professional teachers' judgments. Systematic divergence is
      expected on guidance quality, exam-orientation, and direct-correction norms.
    verification_target: '[NOT FOUND — no India-specific educator annotation of AI
      tutor quality, and no cross-cultural comparison of teacher judgments on tutoring
      acceptability, were found in the published literature. The WEIRD-population
      homogeneity concern is corroborated by a 2025 ITS survey (arXiv:2510.22581 —
      [WEB-6]).]'
  OC_guidance_dimension_calibration:
    priority: HIGH
    description: MRBench's 'providing guidance' rubric implicitly favors Socratic
      scaffolding. Indian teachers may evaluate guidance quality by direct-correction
      and exam-readiness criteria not captured in the current rubric.
    verification_target: '[NOT FOUND — no rubric variants addressing direct-correction
      vs. Socratic scaffolding distinctions in an Indian pedagogical context were
      found. MathTutorBench (EMNLP 2025, arXiv:2502.18940 — [WEB-10])
      similarly defines tutoring quality around withholding answers and Socratic questioning,
      confirming that the entire field default is Western-constructivist. No India-adapted
      rubric exists.]'
  IC_misconception_types:
    priority: HIGH
    description: Bridge and MathDial misconception types are Western-sourced. Rote-procedural
      errors, L1-interference errors, and NCERT-specific algorithmic conventions common
      among Indian Grade 1–8 students are absent from documented selection criteria.
    verification_target: '[NOT FOUND — no published taxonomy of common Indian Grade
      1–8 math misconceptions was located in academic literature. The closest available
      misconception taxonomy resources (e.g., Fen Rivers Academy UK, Mathnasium US)
      are Western-sourced. This is a genuine documentation gap, not a null result
      from poor search strategy. India-specific misconception research for this grade
      band would require stakeholder or expert elicitation, or access to internal
      NCERT/CBSE assessment data not published online.]'
  OO_equal_weight_damr:
    priority: MODERATE
    description: DAMR scoring treats all eight dimensions equally. Indian teachers'
      acceptability judgments are anchored primarily on 'providing guidance.' The
      equal-weight aggregate score cannot be directly used as a deployment validity
      proxy without re-weighting.
    verification_target: '[NOT FOUND — no MRBench extensions proposing dimension-weighted
      DAMR variants were found. MathTutorBench (EMNLP 2025, arXiv:2502.18940 — [WEB-10])
      uses a different reward-model approach but also does not address culture-specific
      dimension weighting. The scoring infrastructure gap is confirmed as unaddressed
      in the current literature.]'
  IC_subnational_school_type_variation:
    priority: MODERATE
    description: Target population spans Delhi and Mumbai with unspecified board distribution
      (CBSE, ICSE, Maharashtra State Board, IB). Pedagogical expectations for acceptable
      guidance vary across boards. This granularity is unresolved.
    verification_target: '[NOT FOUND — no studies on board-specific AI tutoring acceptance
      criteria were located. City-level board-distribution data for Grade 1–8 math
      teachers is not published in accessible form. Urban private schools in metro
      cities show significantly higher AI resource access than national averages (approximately
      62% higher than rural, per educationforallinindia.com citing NCERT 2023 — [WEB-7]),
      but this does not resolve board-level pedagogical variation.]'
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
  communication'
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
  exam_culture: '[NEEDS VERIFICATION — deferred: likely unsearchable in the required
    granularity; specific examination formats shaping what Indian teachers consider
    ''exam-ready'' guidance are embedded in institutional practice and not aggregated
    in searchable form. CBSE school-level test formats closely follow CBSE board patterns
    (MCQ and descriptive); NCERT exercises are the primary reference. Stakeholder
    elicitation recommended.]'
  private_tutoring_ecosystem: '[NEEDS VERIFICATION — deferred: likely unsearchable
    (lived practice); the role of coaching centers such as FIITJEE, Byju''s, and similar
    in shaping professional teacher expectations of effective one-on-one tutoring
    is a cultural practice question not documented in academic literature in the required
    specificity.]'
  AI_in_education_india: 'NEP 2020 endorses AI integration in education; CBSE has
    introduced a 15-hour AI skill module from Class VI and AI as an optional subject
    in Classes IX–XII. NCERT has used AI to translate early-grade textbooks. The DIKSHA
    platform provides AI-enhanced digital resources. As of 2026, no specific CBSE
    or NCERT regulatory or pedagogical guidance on AI-assisted tutoring tools for
    Grade 1–8 mathematics exists — policy is promotional, not prescriptive about tutoring
    interaction models. Private metro schools show substantially higher AI adoption
    rates than the national average. (Sources: PIB Government of India — [WEB-4];
    CBSE AI curriculum update — [WEB-9];
    educationforallinindia.com — [WEB-7])'
net_new_fields:
  mathtutorbench_comparator:
    description: 'MathTutorBench (EMNLP 2025, Macina et al., ETH Zurich; arXiv:2502.18940)
      is a newer open-source benchmark for holistic LLM tutoring evaluation, covering
      three high-level teacher skills and seven concrete tasks. It uses a reward model
      trained on Bridge dataset expert/novice teacher responses to score open-ended
      pedagogical quality automatically. Key finding: subject expertise and pedagogy
      form a trade-off — math-specialist models often exhibit lower pedagogical quality.
      Like MRBench, MathTutorBench is grounded entirely in Western-default (WEIRD-country)
      datasets and Socratic scaffolding norms; no Indian context is included. Relevant
      because it confirms the current field-wide absence of India-adapted tutoring
      benchmarks and the universality of the Socratic scaffolding default. (Source:
      arXiv — [WEB-10]; ACL Anthology EMNLP 2025 — [WEB-11])'
    validity_relevance: Confirms OC and IC gaps are field-wide, not MRBench-specific;
      no alternative benchmark resolves the India-pedagogy validity concern.
  weird_population_bias_in_its_literature:
    description: 'A 2025 comprehensive review of ITS evaluation (Springer/arXiv 2025,
      arXiv:2510.22581) explicitly notes that existing studies on educational dialogue
      ITS are ''conducted on small, homogeneous populations, primarily from WEIRD
      (Western, Educated, Industrialized, Rich, and Democratic) countries, with variable
      implementation parameters.'' This structural bias in the research base directly
      corroborates the annotator representativeness gap and the student interaction
      style gap in this assessment. (Source: arXiv:2510.22581 — [WEB-6])'
    validity_relevance: Provides peer-reviewed corroboration that the IC and OC gaps
      flagged for MRBench are systemic across the ITS evaluation field, not idiosyncratic
      to MRBench.
  teacher_qualification_framework:
    description: 'Indian certification requirements for the Grade 1–8 band are stratified:
      Grade 1–5 (PRT) requires D.El.Ed or equivalent and TET clearance; Grade 6–8
      (TGT Mathematics) requires subject-specific graduation plus B.Ed (NCTE-recognised)
      and CTET/STET. Private metro schools may accept equivalent qualifications (e.g.,
      PgCTL, PGCE) in lieu of B.Ed. Delhi government school recruitment uses DSSSB.
      ''High-end professional'' teachers in private metropolitan schools overwhelmingly
      hold subject degrees plus B.Ed, with CTET certification. (Source: Superprof
      India — [WEB-2];
      DSSSB — [WEB-3])'
    validity_relevance: Clarifies that the target population's professional formation
      includes formal pedagogical training (B.Ed) aligned with NCTE norms, reinforcing
      their likely adherence to CBSE/NCERT pedagogical frameworks rather than Western
      constructivist models.
  india_urban_school_ai_access_disparity:
    description: 'Urban schools in Tier-1 cities (including Delhi and Mumbai) show
      approximately 62% higher AI resource access than rural institutions, and private
      schools implement AI solutions at nearly triple the rate of government schools,
      according to NCERT 2023 data. Only 40% of Indian schools overall have reliable
      internet for real-time AI applications, but this national average is heavily
      depressed by rural schools. (Source: educationforallinindia.com citing NCERT
      2023 — [WEB-7])'
    validity_relevance: Supports the assumption of adequate infrastructure for the
      target (urban private metro) teacher cohort, but flags that the deployment may
      not generalize to government school teachers even within Delhi and Mumbai.
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.cbse.gov.in/cbsenew/teacher_qual_num.html |
| WEB-2 | https://www.superprof.co.in/blog/maths-tutoring-jobs-certificates/ |
| WEB-3 | https://testbook.com/dsssb-teacher/eligibility-criteria |
| WEB-4 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2234853 |
| WEB-5 | https://www.tiwariacademy.com/ncert-solutions/class-8/maths/ |
| WEB-6 | https://arxiv.org/html/2510.22581 |
| WEB-7 | https://educationforallinindia.com/ai-tutors-and-human-teachers-in-indian-education-implementation-framework-under-samagra-shiksha-abhiyan/ |
| WEB-8 | https://www.education.gov.in/sites/upload_files/mhrd/files/NEP_Final_English_0.pdf |
| WEB-9 | https://edunovations.com/currentaffairs/national/cbse-ai-curriculum-for-classes/ |
| WEB-10 | https://arxiv.org/abs/2502.18940 |
| WEB-11 | https://aclanthology.org/2025.emnlp-main.11/ |

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
