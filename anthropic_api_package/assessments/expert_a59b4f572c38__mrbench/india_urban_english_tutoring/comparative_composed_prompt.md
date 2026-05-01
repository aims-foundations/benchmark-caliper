I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **MATHDIAL: A Good Teacher Knows When to Tell** is valid for use in **Indian Metropolitan Professional Teachers (Grades 1–8)**.

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

- **Name**: mathdial
- **Full Name**: MATHDIAL: A Good Teacher Knows When to Tell
- **Domain**: Pedagogical dialogue evaluation / AI tutoring quality
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2023

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### 1. Input Ontology
MATHDIAL organizes its evaluation taxonomy around four top-level teacher move categories —
Focus, Probing, Telling, and Generic — each decomposing into finer-grained intents listed
in Table 2 [Q42]. Focus is defined as constraining the student toward direct progress [Q38],
Probing as generalizing aspects of the problem to explore underlying concepts [Q39], Telling
as revealing parts of the solution [Q40], and Generic as conversational elements with limited
pedagogical value [Q41]. The taxonomy is explicitly grounded in Reiser's (2004) scaffolding
framework distinguishing "structure" from "problematize" moves [Q36, Q37], and is thus
theoretically anchored in constructivist, Western learning sciences. Secondary tasks
benchmarked include tutor response generation [Q81, Q82] and interactive end-to-end
tutoring simulation [Q94, Q104]. The conversation lifecycle is taxonomically constrained:
it ends when the student solves the problem or after 10 minutes [Q141], and unresolved
conversations are positioned as useful for training intervention classifiers [Q80].
The taxonomy does not cover all teaching goals — the authors acknowledge it omits
meta-cognitive support, rapport-building [Q112], and visual instructional practices [Q113].
For the Indian metro deployment context, the user confirmed that curriculum-agnostic errors
and the benchmark's eight pedagogical categories are considered necessary and sufficient,
reducing the ontological gap; however, the taxonomy's systemic privileging of scaffolding
over directive correction remains a structural concern for exam-oriented Indian teachers.

### 2. Input Content
The benchmark's student-facing dialogue instances are generated through a semi-synthetic
pipeline in which an LLM (InstructGPT, text-davinci-003) simulates student turns [Q32],
with student confusions sampled via chain-of-thought prompting from ChatGPT [Q29], and
math word problems drawn from GSM8k [Q103]. GSM8k is a US-origin elementary school
dataset selected because its problems are simple enough for teachers while remaining
challenging for students [Q118]. The simulated student is instructed via a student profile
specifying confusion type and persona [Q34], with student names diversified across
backgrounds and pronouns [Q123]; however, this nominal diversity does not extend to
Indian classroom interaction dynamics. The authors explicitly acknowledge that the LLM
student simulation has "a limited understanding of human learning" and that certain
student confusions may be under- or over-represented [Q106]. Annotators validated that
the majority of student generations were judged as typical of a sixth grader [Q55, Q56,
Q57], but this validation was performed by predominantly UK/US teachers [Q27], not Indian
educators. The user identified that Indian students tend to be brief, deferential, and
less likely to verbalize reasoning [A2], while teachers in Indian metros tend toward
direct, exam-oriented correction — interaction norms that the LLM student simulation,
calibrated to Western tutoring conventions, does not capture. Procedure-heavy learning
patterns and language-related misunderstandings common in Indian classrooms are
underrepresented. Furthermore, the pipeline excludes culturally situated problem content
(e.g., Indian currency, Indian naming conventions, NCERT-aligned problem structures);
all MWPs are US-origin. Teachers interacting with the LLM student may have adapted
their behavior to the model's patterns rather than exhibiting naturalistic classroom
behavior [Q108], further reducing ecological validity for Indian deployment.

### 3. Input Form
MATHDIAL is an English text-only benchmark [Q1, Q32]. All dialogue turns, math word
problems, and student profiles are encoded as natural language text. The student turn
generation uses temperature sampling from InstructGPT [Q122]; dialogues are conditioned
on a structured prompt containing the MWP, dialogue history, initial confusion, and
student profile [Q33, Q34]. Data is split 80/20 with seen/unseen problem splits [Q85,
Q86, Q87, Q88]. A safety filter using the Perspective API removes toxic content [Q157,
Q158]. The benchmark and the Indian metro deployment context are both English text-only,
so no modality, script, or language-encoding mismatch exists. This dimension poses
minimal validity risk for the target use case.

### 4. Output Ontology
The benchmark's output taxonomy operates at two levels. For human evaluation, three
dimensions are rated: Coherence, Correctness, and Equitable Tutoring [Q97, Q166],
where Equitable Tutoring is defined as giving the student room for reflection, exploration,
and challenge [Q98, Q166] — explicitly encoding a constructivist, anti-telling orientation.
For teacher move classification, the label set is Focus, Probing, Telling, and Generic
[Q151, Q152, Q153], with Focus and Probing designated as "productive for long-term
learning" [Q154] and Telling positioned as a last resort when a student is stuck [Q155].
The benchmark explicitly rewards scaffolding and penalizes premature solution revelation
via the Telling@k metric [Q96]. The user confirmed that the eight pedagogical categories
are accepted as necessary and sufficient, and that "providing guidance" is the dominant
evaluation criterion [A3]. However, the benchmark treats guidance as one of three
co-equal human evaluation dimensions and embeds it within a Socratic framework
(Equitable Tutoring), rather than weighting direct, exam-readiness-oriented guidance
commensurately with the preferences of Indian professional teachers. This scoring
emphasis misalignment represents a moderate ontological risk.

### 5. Output Content
MATHDIAL's ground-truth quality judgments were produced by 91 professional teachers
recruited via Prolific [Q23], predominantly nationals of the UK, followed by the USA,
Canada, Australia, India, and Germany [Q27]. India is listed as a source country but
appears as a minority contributor following four predominantly Western nations, meaning
the benchmark's quality standards are shaped primarily by UK/US pedagogical norms.
Annotators were instructed explicitly not to correct student solutions by telling
what is correct or incorrect, but to give students opportunities to explore [Q148],
reinforcing the constructivist orientation in the ground-truth labels. Inter-annotator
agreement for teacher move labeling was κ=0.60 between two independent annotators
but only κ=0.49 and κ=0.34 between either annotator and the original teacher [Q69],
with the authors attributing the divergence partly to the subjective boundary between
Focus and Probing [Q70]. For human evaluation of model outputs, agreement on Equitable
Tutoring was κ=0.34 — notably low for the dimension most sensitive to cross-cultural
variation [Q100]. The user expects systematic divergence between Indian professional
teachers' quality judgments and those of the benchmark's Western-norm annotators [A4],
particularly on direct-correction versus Socratic probing and the weighting of
exam-readiness. This represents the highest-priority validity risk for the deployment.

### 6. Output Form
MATHDIAL evaluates text-based open-ended tutoring dialogue outputs. Automatic metrics
include sacreBLEU, BERTScore, token-level F1 (KF1), and Uptake [Q89, Q90, Q93].
Interactive simulation uses Success@k and Telling@k [Q95, Q96, Q102]. Human evaluation
uses a 3-point Likert scale for Coherence and Equitable Tutoring and a binary scale for
Correctness [Q167]. The authors acknowledge that automatic faithfulness metrics are
insufficient [Q91, Q92] and that measuring only immediate solving success fails to
capture long-term learning outcomes [Q114]. The benchmark does not evaluate language
mismatches or non-English outputs. For the Indian metro deployment (English text-only,
augmented GPT-4 output evaluated by professional teachers), no output-form mismatch
exists. This dimension poses minimal validity risk for the target use case.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "We describe how we use this framework to collect MATHDIAL, a dataset of 3k one-to-one teacher-student tutoring dialogues grounded in multi-step math reasoning problems." |
| Q2 | 1 | input_content | "To address this, we propose a framework to generate such dialogues by pairing human teachers with a Large Language Model (LLM) prompted to represent common student errors." |
| Q3 | 1 | input_ontology | "We let teachers provide learning opportunities to students by guiding them using various scaffolding questions according to a taxonomy of teacher moves." |
| Q4 | 1 | output_ontology | "We demonstrate MATHDIAL and its extensive annotations can be used to finetune models to be more effective tutors (and not just solvers)." |
| Q5 | 1 | output_form | "We confirm this by automatic and human evaluation, notably in an interactive setting that measures the trade-off between student solving success and telling solutions." |
| Q6 | 1 | stated_limitations | "While models like GPT-3 are good problem solvers, they fail at tutoring because they generate factually incorrect feedback or are prone to revealing solutions to students too early." |
| Q7 | 1 | output_content | "Jakub Macina, Nico Daheim, Sankalan Pal Chowdhury, Tanmay Sinha, Manu Kapur, Iryna Gurevych, Mrinmaya Sachan." |
| Q8 | 1 | output_content | "ETH AI Center, Department of Computer Science, ETH Zurich, Ubiquitous Knowledge Processing Lab (UKP Lab), Department of Computer Science and Hessian Center for AI (hessian.AI), TU Darmstadt, National Institute of Education, Nanyang Technological University, Professorship for Learning Sciences and Higher Education, ETH Zurich." |
| Q9 | 2 | input_ontology | "Research on task-oriented dialogue systems has mainly focused on customer service, for instance, restaurant reservations (Henderson et al., 2014; Gašic et al., 2014)." |
| Q10 | 2 | input_content | "Notably, Wen et al. (2017) collect such dialogues with the Wizard-of-Oz (WoZ) paradigm (Kelley, 1984), where crowdworkers are connected to roleplay interlocutors." |
| Q11 | 2 | input_content | "WoZ has been used to collect many popular datasets, such as MultiWoZ (Budzianowski et al., 2018) and extensions (Kim et al., 2020; Zhu et al., 2020), Taskmaster (Byrne et al., 2019), and open-domain datasets like Wizard-of-Wikipedia (Dinan et al., 2019)." |
| Q12 | 2 | input_content | "Other collection methods include crowdworkers filling dialogue outlines (Shah et al., 2018; Rastogi et al., 2020; Majewska et al., 2023), or scraping from the web (Li et al., 2017; Dziri et al., 2019)." |
| Q13 | 2 | output_content | "Multiple works have shown shortcomings in using non-expert crowdworkers." |
| Q14 | 2 | output_content | "For instance, document-grounded corpora often contain hallucinations in ground-truth data (Dziri et al., 2022), and task-oriented corpora tend to suffer from annotation errors and low lexical diversity (Casanueva et al., 2022)." |
| Q15 | 2 | output_content | "More closely related to this work, current tutoring corpora lack sufficient tutoring quality" |
| Q16 | 3 | input_content | "Figure 2: Overview of the data collection pipeline: First, student confusions are oversampled from an LLM and sorted by frequency. Then, a human teacher synchronously interacts with a student simulated by an LLM that is instructed with a student profile and incorrect solution." |
| Q17 | 3 | input_content | "MATHDIAL mitigates these issues by adapting the WoZ paradigm to using human teachers as experts in collaboration with an LLM." |
| Q18 | 3 | input_ontology | "Theoretical and empirical studies have shown the importance of questioning in human learning (Roscoe and Chi, 2008; Shahriar and Matsuda, 2021; Shridhar et al., 2022)." |
| Q19 | 3 | input_ontology | "Nye et al. (2014), for instance, show the effectiveness of deep reasoning questions, and (Howe et al., 2019) find that elaboration and challenging of previous contributions can benefit student learning." |
| Q20 | 3 | input_content | "All of them suffer from several limitations, such as missing grounding information (TSCC, TalkMoves, NCTE), low tutoring quality (CIMA), small dataset sizes (all), or a focus on noisy classroom scenarios (see Table 1)." |
| Q21 | 3 | output_content | "However, Tack and Piech (2022); Macina et al. (2023) show that they can not yet perform well as teachers out-of-the-box, because they often incorrectly assess student solutions and reveal answers too quickly." |
| Q22 | 3 | input_content | "This section introduces a framework for collecting high-quality tutoring conversations, highlighted in Figure 2. The core idea behind it is to connect" |
| Q23 | 4 | output_content | "We recruit professionals with teaching experience through Prolific. We only select teachers who have completed at least 500 submissions and achieved a 100% completion rate." |
| Q24 | 4 | output_content | "Annotators read guidelines for the task in an initial training phase (cf. Section D.3) and then complete a test on an example conversation to assess their understanding of the task." |
| Q25 | 4 | output_content | "We only select annotators with 100% test scores for further rounds of data collection, similar to Zhang et al. (2023)." |
| Q26 | 4 | output_content | "We employ 91 expert annotators, of which 71 identify as female and 18 as male." |
| Q27 | 4 | output_content | "The majority of annotators are nationals of the UK, followed by the USA, Canada, Australia, India, and Germany, with a median age of 39 years." |
| Q28 | 4 | input_content | "We employ an LLM to generate plausible student confusions and base the dialogues on them." |
| Q29 | 4 | input_content | "We pick the most frequent incorrect solution sampled from ChatGPT (gpt-3.5-turbo) (Ouyang et al., 2022) using chain-of-thought prompting." |
| Q30 | 4 | input_form | "To be precise, we first use temperature sampling to obtain N = 50 reasoning paths for every MWP in GSM8k, with T = 0.7 and no top-k truncation Wang et al. (2023b)." |
| Q31 | 4 | input_form | "Then, we group incorrect solutions according to their final numeric answer and pick one from the set with the largest cardinality." |
| Q32 | 5 | input_content | "We use InstructGPT (text-davinci-003) (Ouyang et al., 2022) to generate student turns." |
| Q33 | 5 | input_form | "We prompt the model with the previous dialogue history and additional information that grounds the next turn." |
| Q34 | 5 | input_form | "The prompt contains the MWP, the initial student confusion, as well as the student profile which explains the type of confusion and persona of the student." |
| Q35 | 5 | input_ontology | "This section defines the taxonomy of all teacher moves that are used in MATHDIAL." |
| Q36 | 5 | input_ontology | "We base the first two on the work of Reiser (2004), who suggest that scaffolding strategies can be split into two main categories: structure and problematize." |
| Q37 | 5 | input_ontology | "These form the basis for the Focus and Probing moves employed in our study." |
| Q38 | 5 | input_ontology | "Focus is used to constrain the student to make direct progress towards solving the problem." |
| Q39 | 5 | input_ontology | "Probing is used to generalize certain aspects of the problem which allows the student to explore its underlying concepts." |
| Q40 | 5 | input_ontology | "This is called Telling." |
| Q41 | 5 | input_ontology | "Finally, turns that just serve as conversational elements and have limited pedagogical value are classed as Generic." |
| Q42 | 5 | input_ontology | "Table 2 lists finer-grained intents for each of these four categories along with a set of accompanying examples." |
| Q43 | 5 | output_form | "We quantitatively evaluate the collected tutoring dialogues to assess their quality." |
| Q44 | 5 | input_content | "First of all, we can see that our dataset is significantly larger in terms of the number of dialogues and utterances than all related datasets that are listed." |
| Q45 | 5 | input_content | "By open-sourcing such a large dataset, we fill a crucial gap of sufficiently-sized open-source tutoring corpora which has so far hindered research in the area (Macina et al., 2023)." |
| Q46 | 5 | output_form | "Furthermore, MATHDIAL exhibits a higher diversity, measured in bigram entropy (Zhang et al., 2018), than CIMA and TalkMoves." |
| Q47 | 5 | output_form | "The diversity is similar to NCTE and TSCC which consist of transcripts of classroom and one-to-one tutoring sessions, respectively." |
| Q48 | 5 | output_content | "This supports the observation that expert annotators tend to create more diverse utterances than untrained crowdworkers (Casanueva et al., 2022), and also that LLMs can be used to generate diverse tutoring dialogues." |
| Q49 | 5 | output_form | "Finally, we measure the Uptake (Demszky et al., 2021) of annotated teacher utterances." |
| Q50 | 5 | output_form | "Uptake indicates how coherent the teacher's utterance is with respect to the previous student's turn." |
| Q51 | 5 | output_form | "We find that MATHDIAL and CIMA have similar uptake." |
| Q52 | 5 | output_form | "Both surpass the other datasets in our comparison." |
| Q53 | 5 | input_content | "Our collection methodology relies on LLMs for simulating students." |
| Q54 | 5 | input_content | "Therefore, it is crucial to ensure that the turns simulated by the LLM also match what a teacher would expect of a real student, who in our case is a sixth grader." |
| Q55 | 5 | output_content | "Figure 3 shows that annotators rate the majority of generations by the model positively along two dimensions." |
| Q56 | 5 | output_ontology | "The first one says that the confusion of the student is typical confusion of a sixth grader." |
| Q57 | 5 | output_ontology | "The second one says that the interaction with the student as a whole is as expected of a sixth grader." |
| Q58 | 5 | output_content | "We release these annotations with our final dataset which allows users of MATHDIAL to filter out utterances that are of a lower quality." |
| Q59 | 5 | input_content | "Moreover, LLMs can be prone to incorrect arithmetic calculations." |
| Q60 | 5 | output_content | "Therefore, we asked annotators to distinguish conceptual errors from such simple calculation mistakes." |
| Q61 | 5 | output_ontology | "Arithmetic errors may be easily resolved through calculators but conceptual errors are likely to require tutors to resolve them, for example by scaffolding." |
| Q62 | 5 | output_content | "Annotators identified around 80% of the confusions as conceptual, leaving around a fifth containing arithmetic errors." |
| Q63 | 5 | output_content | "Again, we include these annotations to allow for data filtering." |
| Q64 | 5 | output_ontology | "In this Section, we evaluate when teachers use which teacher moves in the conversations." |
| Q65 | 5 | output_ontology | "Figure 4 shows that teachers most frequently use Focus questions which are found in 37% of utterances." |
| Q66 | 5 | output_ontology | "Focus is followed by Generic and Probing." |
| Q67 | 5 | output_ontology | "Telling is the rarest move." |
| Q68 | 5 | output_content | "To validate these annotations, we sampled 17 conversations consisting of 102 teacher utterances and asked two independent annotators to" |
| Q69 | 6 | output_content | "We obtain an agreement of κ = 0.60 between the two annotators and κ = 0.49 and κ = 0.34, respectively, between either of the annotators and the teacher." |
| Q70 | 6 | output_content | "We note that Probing and Focus appear to be particularly challenging to distinguish and acknowledge that the boundary between them may be subjective." |
| Q71 | 6 | output_content | "Merging these two categories into one larger 'scaffolding' category improves agreements to κ = 0.67, κ = 0.75 and κ = 0.55." |
| Q72 | 6 | output_content | "Our observations are in line with related works that have shown low inter-annotator agreement between experts for detailed teacher moves in classroom settings (Kelly et al., 2020)." |
| Q73 | 6 | input_ontology | "The sequence of moves employed by the teachers constitutes their teaching strategy which we analyze in the following." |
| Q74 | 6 | input_ontology | "We find that the initial utterance by the teacher is usually generic and serves as a conversation opener, oftentimes by asking the student to repeat the question or solution attempt." |
| Q75 | 6 | input_ontology | "During the conversation, teachers mainly use scaffolding to either probe the student or focus the conversation on a specific part of the problem." |
| Q76 | 6 | input_ontology | "The more the conversations progress the more likely teachers are to resort to Telling because students often get stuck at a specific subproblem and are unable to resolve it themselves." |
| Q77 | 6 | input_ontology | "The goal of MATHDIAL is to enable building tutors that can help students resolve their confusion." |
| Q78 | 6 | output_content | "Teachers assessed that they were successful in almost 89% of the conversations." |
| Q79 | 6 | output_content | "In ca. 75% of the conversations by using mainly scaffolding questions, and only in around 14% by revealing the majority of the answer." |
| Q80 | 6 | input_ontology | "The conversations in which confusions could not be resolved can still be useful, as they, for instance, can be used to train classifiers to determine when human intervention in such tutoring sessions is required." |
| Q81 | 6 | input_ontology | "We focus our initial studies on MATHDIAL on the task of tutor response generation." |
| Q82 | 6 | input_ontology | "Tutor response generation aims to model the teacher in a dialogue by generating follow-up turns to guide the student towards learning and solving the problem." |
| Q83 | 6 | output_form | "We compare different finetuned and prompted language models on the task and evaluate how much detailed information that can be given to the model, such as step-by-step solutions of the MWP, influence performance." |
| Q84 | 6 | input_form | "We use neural conditional language models that given a tutoring dialogue history u_1^T, grounding" |
| Q85 | 7 | input_form | "We split our data into a training split containing 80% of the conversations and a test set containing the remaining 20%." |
| Q86 | 7 | input_form | "Around 60% of the problems in the test set are also found in the training data, where at least one conversation was based on it, and therefore constitute our 'seen' split." |
| Q87 | 7 | input_form | "The remaining 40% are unseen during training and test the ability of the model to generalize to new problems." |
| Q88 | 7 | input_form | "The dataset split is published with the dataset." |
| Q89 | 7 | output_form | "We assess our models using the sacrebleu (Post, 2018) implementation of BLEU (sBLEU) (Papineni et al., 2002), as well as BERTScore between generated response (uT +1) and annotated response (uˆT +1) for each teacher response in the conversation." |
| Q90 | 7 | output_form | "Furthermore, in line with previous works (Dziri et al., 2022; Daheim et al., 2023), we report BERTScore and the token level F1 (KF1) between generated utterance and math word problem as a proxy for faithfulness." |
| Q91 | 7 | output_form | "However, we note that an increase in these metrics can be caused by an increase in overlap, which may also indicate more telling and can be undesirable." |
| Q92 | 7 | output_form | "However, finding good evaluation metrics for assessing the faithfulness of dialogue tutors remains an open problem." |
| Q93 | 7 | output_form | "Finally, we measure the Uptake of the generated response (Demszky et al., 2021)." |
| Q94 | 7 | output_form | "We propose two evaluation metrics for end-to-end tutoring, where a tutor model is evaluated interactively by using it to teach an LLM that simulates a student." |
| Q95 | 7 | output_form | "Success@k measures the percentage of conversations where the student reaches the correct final answer at least once within the first k turns (equivalent of % solve rate in prior work)." |
| Q96 | 7 | output_form | "Telling@k measures the percentage of conversations where the teacher explicitly tells the final answer before the student has reached it on their own within the first k turns." |
| Q97 | 8 | output_ontology | "Finally, we conduct a human evaluation according to three criteria: 1) Coherence: how coherent the teacher's response is with respect to the preceding dialogue, 2) Correctness: whether it is in itself correct, and 3) Equitable tutoring." |
| Q98 | 8 | output_ontology | "Equitable tutoring describes how well the model provides the student with room for exploring the problem and solution space." |
| Q99 | 8 | output_content | "We use three expert annotators that each annotate n = 50 responses." |
| Q100 | 8 | output_content | "We obtain agreements of κ = 0.29, κ = 0.69, and κ = 0.34 for the three categories." |
| Q101 | 8 | output_form | "Good tutoring models need to maintain high quality not only when viewed per-utterance but especially over an entire conversation." |
| Q102 | 8 | output_form | "In order to assess this, we use them to tutor an InstructGPT student and measure their success (Success@k), as well as the rate of telling (Telling@k)." |
| Q103 | 9 | input_content | "Our dataset consists of ca. 3k tutoring conversations grounded in math word problems from GSM8k." |
| Q104 | 9 | input_ontology | "We benchmark open-source models on the task of tutor response generation and show that smaller models finetuned on our MATHDIAL can significantly surpass the performance of much larger prompted LLMs." |
| Q105 | 9 | output_form | "In our proposed interactive tutoring simulation, the finetuned model achieves similar student-solving success as prompted LLM while keeping the direct telling rate lower." |
| Q106 | 9 | input_content | "In this work, we used an LLM to simulate student confusion. However, we acknowledge that these models have a limited understanding of human learning and this is a key limitation in our dataset – certain kinds of student confusions may be under- or over-represented in our dataset." |
| Q107 | 9 | input_content | "We introduce a new framework for semi-synthetic dialogue dataset collection. We use it to collect a pedagogically rich dataset for tutoring math word problems that follow equitable tutoring practices and learning sciences research on scaffolding student understanding, called MATHDIAL." |
| Q108 | 10 | input_content | "Furthermore, in our setup, teachers were interacting with an LLM role-playing as a student. However, it is possible that some teachers might have learned to interact with the student model in a different way than they would do in the classroom." |
| Q109 | 10 | input_content | "Moreover, it is also possible that some teachers may have lost motivation when found out they are not interacting with real students, leading to lower data quality." |
| Q110 | 10 | input_content | "In the future, we would like to explore solutions to build better LLM-based student models (Zhou et al., 2023)." |
| Q111 | 10 | input_ontology | "The methodology to collect the dataset was instantiated just for the domain of math reasoning. The collection of additional domain-specific datasets is necessary to further generalize the effectiveness of our methodology." |
| Q112 | 10 | input_ontology | "Inspired by previous work in scaffolding, we acknowledge our focus is on a subset of common teaching moves. However, this does not cover all the goals of human tutors, such as meta-cognitive support or building rapport with a student." |
| Q113 | 10 | input_form | "Moreover, text tutoring limits teachers' use of additional instructional practices such as drawings." |
| Q114 | 10 | output_form | "Finally, measuring a student's immediate success in solving a problem does not capture all the aspects of student learning. From a learning perspective, focusing on and measuring long-term learning is desired." |
| Q115 | 10 | output_content | "This project was made possible by an ETH AI Center Doctoral Fellowship to Jakub Macina with further support from the Asuera Stiftung and the ETH Zurich Foundation. Nico Daheim has received funding by the German Federal Ministry of Education and Research and the Hessian Ministry of Higher Education, Research, Science and the Arts within their joint support of the National Research Center for Applied Cybersecurity ATHENE. Mrinmaya Sachan acknowledges support from the Swiss National Science Foundation (Project No. 197155), a Responsible AI grant by the Haslerstiftung; and an ETH Grant (ETH-19 21-1)." |
| Q116 | 14 | output_form | "For NCTE, uptake is calculated on the teacher-student dialogue pairs while bigram entropy is calculated on all teacher utterances." |
| Q117 | 14 | output_form | "For TalkMoves and TSCC, bigram entropy is calculated on all teacher utterances having more than three words, while uptake is calculated on teacher utterances immediately following student utterances if both have more than three words." |
| Q118 | 14 | input_content | "While the problems in GSM8k are simple enough to be understood quickly by teachers, they remain challenging for students, who among others have to deal with equations or percentages." |
| Q119 | 14 | input_form | "We follow the GSM8k reasoning format and prompt ChatGPT (gpt-3.5-turbo) with a 2-shot prompt." |
| Q120 | 14 | input_form | "Given a prompt and a math word problem, we sample n reasoning paths ri solutions from the model." |
| Q121 | 14 | input_form | "We parse the first numerical answer ai after the model" |
| Q122 | 15 | input_form | "We use InstructGPT (text-davinci-003) with the following prompt using temperature sampling with T = 0.4 and no top-k truncation:" |
| Q123 | 15 | input_content | "To build a dataset that would reflect students of various backgrounds, we use numerous student names associated with their given pronouns." |
| Q124 | 15 | output_ontology | "List of all student characteristics based on prior work studying misconceptions in learning algebra (Booth et al., 2017):" |
| Q125 | 15 | output_ontology | "has a problem with understanding what steps or procedures are required to solve a problem." |
| Q126 | 15 | output_ontology | "has a problem with understanding underlying ideas and principles and a recognition of when to apply them." |
| Q127 | 15 | output_ontology | "struggle most with understanding what the problem is asking them to do." |
| Q128 | 15 | output_ontology | "has difficulty determining which pieces of information are relevant and which are irrelevant to solving the problem." |
| Q129 | 15 | output_ontology | "struggle to put the numbers in the correct order in the equation or determine the correct operation to use." |
| Q130 | 15 | output_ontology | "struggle to recognize the problem type and therefore do not know what strategy to use to solve it." |
| Q131 | 16 | output_content | "We use Prolific for data collection and hire annotators with teaching experience." |
| Q132 | 16 | output_content | "To ensure the data quality we filter only annotators with 100% completion rate with more than 500 total submissions." |
| Q133 | 16 | output_content | "All the payments to the annotators exceeded the US federal minimum wage and the final batch of annotators were paid the equivalent of $12/hour." |
| Q134 | 16 | output_content | "Annotators were restricted to having a maximum of five conversations in one annotation session." |
| Q135 | 16 | output_content | "One conversation takes ca. 6 minutes." |
| Q136 | 16 | output_content | "Data collection took place over a period of 2 months." |
| Q137 | 16 | output_content | "For each annotator, we randomly assign a student and math word problem." |
| Q138 | 16 | output_content | "Teachers were instructed to first analyze the student homework solution and then start the conversation to scaffold student problem understanding." |
| Q139 | 16 | output_content | "Post-conversation questionnaire is filled out by teachers to rate the conversation and get feedback on the type of student error." |
| Q140 | 16 | output_ontology | "The teacher marks the exact line of a first student error and categorizes the problem into the following categories: Reached correct solution but proceeded further, Extra quantity or Missing quantity, Unit conversion error, Calculation error easily solved by a calculator, Missing / Wrong factual knowledge, Misunderstanding of a question, None of the above." |
| Q141 | 16 | input_ontology | "The conversation ends when the student correctly solves the problem or if the total conversation time exceeds 10 minutes." |
| Q142 | 16 | output_content | "We let annotators read best practices on how to have a productive conversation with students and tested them on their understanding of our task afterwards." |
| Q143 | 16 | output_content | "We started the data annotation with all the annotators able to successfully pass the test." |
| Q144 | 16 | output_content | "Moreover, to improve the training phase we manually checked several conversations by each annotator in terms of the quality and usage of diverse scaffolding questions." |
| Q145 | 17 | output_content | "Teachers were instructed to have a one-on-one tutoring session with different 6th-grade students." |
| Q146 | 17 | input_content | "They were told that students received a math word problem for homework and submitted their solutions beforehand." |
| Q147 | 17 | output_content | "In a tutoring conversation, teachers were asked to go through the student's solution and try to let the student understand using a series of sensemaking questions to support student reasoning and learning." |
| Q148 | 17 | output_content | "Specifically, they were instructed to not just correct student solutions by telling what's correct/incorrect, but to give students the opportunity to explore the problem with a focus on core aspects, such as their chosen strategy." |
| Q149 | 17 | output_content | "However, as the goal is to focus on conceptual errors, they were allowed to let students use calculators or correct their arithmetic mistakes." |
| Q150 | 17 | output_ontology | "Table 2 refers to the details of teacher moves used during annotation." |
| Q151 | 17 | output_ontology | "In summary, Focus comprises of all conversation elements that direct the student towards the solution without actually giving out any of the solution, while Probing attempts to develop reasoning skills and world knowledge relevant to the problem, but not necessarily specific to the given problem." |
| Q152 | 17 | output_ontology | "Telling is giving out parts of the solution, either calculations or strategy or both." |
| Q153 | 17 | output_ontology | "All other conversational elements, including trying to understand what the student has already tried, fall under Generic." |
| Q154 | 17 | output_ontology | "Most importantly, scaffolding questions that are productive for long-term learning are Focus and Probing." |
| Q155 | 17 | output_ontology | "On the other hand, Telling represents giving out the partial or full answer to the student and should be mostly used when a student is stuck." |
| Q156 | 17 | input_ontology | "Scaffolding (Reiser, 2004; Anghileri, 2006) assists students to succeed in tasks that would otherwise be complex and differentiates between guidance (e.g. decomposing problem, clarifying) from cognitive activation (e.g. causing cognitive conflicts, activating prior knowledge (Limón, 2001))." |
| Q157 | 18 | input_form | "As we are interested in real educational use cases for our tutoring system, we apply a safety filter to filter out conversations with any sensitive content." |
| Q158 | 18 | input_form | "In particular, we use the Perspective API to filter out conversations containing toxic content (<1%)." |
| Q159 | 18 | input_content | "We initially explored two additional approaches of data collection: i) human-human conversations, and ii) synthetic generation by LLMs." |
| Q160 | 18 | input_content | "The framework we used in the final data collection enables us to scalably create data since we are only reliant on one user who can quickly create entire conversations with the LLM, taking ca. 6 minutes per 7+ turn conversation." |
| Q161 | 18 | input_content | "We found this more efficient and performant than both human-human conversations and synthetic data generation." |
| Q162 | 18 | input_content | "Specifically, the human-to-human collection is too time-consuming (on average 15 minutes per conversation in our pilot experiments) and requires waiting times to synchronously connect participants, and synthetic generation has proven to be error-prone; for example, models fail to understand student solutions and themselves make arithmetic errors that are not expected from teachers." |
| Q163 | 18 | input_content | "The student model in all 3 cases is an InstructGPT model (text-davinci-003) as defined in Section C.1, with the student name fixed to "Kayla"." |
| Q164 | 18 | input_content | "The first utterance of the teacher is hardcoded to "Hi Kayla, could you walk me through your solution?"." |
| Q165 | 18 | output_form | "For Flan-T5780M teacher model decoding, we used sampling without a beam search." |
| Q166 | 18 | output_ontology | "The following dimensions were rated by annotators: Coherence - "The response naturally follows up on the previous utterance and context and has no logical conflicts with the context." Correctness - "The response is factually and mathematically correct and respects the learning concepts being taught." Equitable tutoring - "The response gives a learning opportunity for the student by providing space for reflection, explanation, pointing to follow-up challenge, or engaging the student in other ways."" |
| Q167 | 18 | output_form | "We use a 3-point Likert scale ranging from 1 (poor) and 3 (very good) for coherence and equitable tutoring and a binary scale for correctness." |
| Q168 | 18 | input_ontology | "ChatGPT prompt is the same as in the interactive tutoring scenario (Section E) with an additional section containing student solution." |
| Q169 | 20 | input_content | "In our initial pilot study we observed that synthetic data generation by InstructGPT strictly followed the same structure of only asking next-step questions (highlighted in yellow) and was prone to inconsistencies in factual correctness and order of steps (highlighted in red)." |

---

## Regional Context

```yaml
name: Indian Metropolitan Professional Teachers (Grades 1–8)
abbreviation: IN-METRO-TEACHERS
deployment_context:
  country: India
  cities:
  - Delhi
  - Mumbai
  institutional_setting: Formal school sector, Grades 1–8, operating under NCERT/CBSE
    curricular framework
  population_description: Experienced, formally credentialed professional teachers
    working in major Indian metropolitan cities (Delhi and Mumbai), evaluating the
    pedagogical quality of AI-augmented one-on-one math tutoring responses. Evaluators
    are English-fluent, accustomed to exam-oriented and teacher-directed instructional
    norms, and expected to judge response quality primarily on the adequacy of guidance
    provided to the student.
  role_in_system: Human evaluators who assess whether GPT-4-augmented tutoring responses
    meet teacher-acceptable pedagogical standards, with particular emphasis on the
    'providing guidance' dimension.
  grade_band: Grades 1–8 (ages approximately 6–14)
  subject_domain: Mathematics (curriculum-agnostic math reasoning errors; no NCERT/CBSE
    topic alignment required per user confirmation)
languages:
  deployment_language: English (text only)
  note: Single-language deployment confirmed. No code-switching, script variation,
    or vernacular-language content is present in the benchmark or deployment interface.
    Hindi and other Indian languages are not part of the evaluation interface, though
    they are the home languages of many students being discussed.
writing_systems:
  scripts_in_use:
  - Latin (English)
  note: No script mismatch between benchmark and deployment. All dialogue instances
    and evaluation rubrics are English Latin-script text.
population_characteristics:
  professional_credentials: 'Formally trained and credentialed teachers regulated
    by the National Council for Teacher Education (NCTE), a statutory body established
    under the NCTE Act 1993. For primary (Grades 1–5), the minimum qualification is
    a 2-year Diploma in Elementary Education (D.El.Ed.); for upper primary (Grades
    6–8), a Bachelor of Education (B.Ed.) or equivalent is required per NCTE norms.
    A 2023 Supreme Court ruling confirmed B.Ed. holders cannot apply for primary posts
    without a D.El.Ed. bridge course. By 2030, the 4-year integrated B.A./B.Sc.B.Ed.
    (ITEP) will become the minimum qualification for all school teachers. Source:
    NCTE official qualification norms — [WEB-1];
    CTET eligibility 2026 — [WEB-2]'
  experience_profile: '[NEEDS VERIFICATION — deferred: below search budget; no India
    metro-specific median experience figure found in UDISE or comparable source]'
  english_proficiency: 'English-fluent; English is the primary medium of instruction
    in a large proportion of private and government-aided schools in Delhi and Mumbai.
    Delhi alone lists over 3,000 English-medium schools (directory data). Government
    Schools of Excellence in Delhi operate in English medium. Mumbai similarly has
    a substantial English-medium private school sector alongside Marathi-medium government
    schools. No aggregate percentage of English-medium enrollment at metro level was
    found; this remains a partially verified slot. Source: Delhi English-medium school
    directory — [WEB-3]; Delhi
    Schools of Excellence (English medium, govt) — [WEB-4]'
  gender_distribution: 'Teaching workforce nationally skews female at the school level:
    54% of all Indian school teachers are female per UDISE+ 2024-25 data, with private
    schools at 66% female in 2023-24. Delhi specifically: women constitute 61% of
    government school teachers (UDISE+ 2023-24 state-level data). Metro private-school
    figures for Mumbai are not separately published but the national private-school
    trend (66% female) is indicative. Source: IndiaSpend/UDISE+ 2024-25 — [WEB-5];
    UDISE+ 2023-24 (Delhi 61% figure) — [WEB-6]'
  employment_sector: 'India''s overall school teacher distribution (UDISE+ 2024-25):
    ~51% in government schools, ~40% in private unaided, remainder in government-aided
    schools. In metropolitan contexts the private unaided share is higher. Source:
    IndiaSpend/UDISE+ 2024-25 — [WEB-7]'
  digital_literacy: '[NEEDS VERIFICATION — deferred: below search budget; likely unsearchable
    at metro teacher cohort level; UDISE+ 2024-25 reports 64.7% of schools nationally
    have computers and 63.5% have internet connectivity, but teacher-level digital
    literacy figures for Delhi/Mumbai are not published separately. Source: UDISE+
    2024-25 analysis — [WEB-8]]'
pedagogical_norms:
  dominant_orientation: Exam-oriented, teacher-directed instruction; emphasis on procedural
    correctness and exam-readiness over constructivist exploration
  guidance_style: Direct correction and explicit solution guidance are valorized;
    Socratic scaffolding is less normative than in Western constructivist frameworks
  student_interaction_expectations: Indian metro students are typically brief and
    deferential in teacher interactions; low verbalization of reasoning; deference
    to teacher authority
  procedure_emphasis: High weight placed on step-by-step procedural accuracy, standard
    algorithms, and exam-relevant solution formats
  socratic_scaffolding_reception: Extended Socratic probing may be perceived as withholding
    guidance rather than facilitating learning; systematic divergence from MATHDIAL's
    constructivist orientation expected
  telling_as_legitimate_move: Direct revelation of correct steps or answers is considered
    pedagogically appropriate (not a failure mode) in exam-preparation contexts; contrasts
    sharply with MATHDIAL's Telling@k penalty framework
  exam_readiness_weighting: Exam performance is a primary success criterion; responses
    that build toward board/competitive exam formats are rated favorably
  language_related_misunderstandings: English-medium instruction may create comprehension
    gaps for students; teachers account for L2-mediated mathematical misunderstandings
    not captured in MATHDIAL's US-origin dialogues
benchmark_alignment_notes:
  primary_evaluation_criterion: Providing adequate guidance to the student (user-confirmed
    as the single most critical dimension among the eight pedagogical categories)
  accepted_ontology: The benchmark's eight pedagogical categories are accepted as
    necessary and sufficient per user confirmation; curriculum-agnostic math errors
    are sufficient
  key_divergence_ic: MATHDIAL's LLM-simulated student is calibrated to Western tutoring
    conventions — expressive, reasoning-out-loud behavior — that does not reflect
    the brief, deferential, low-verbalization interaction style typical of Indian
    metro classrooms
  key_divergence_oc: Ground-truth quality annotations are dominated by UK/US educators
    instructed to favor Socratic scaffolding; Indian professional teachers are expected
    to systematically rate more directive responses higher, particularly on guidance
    and exam-readiness dimensions
  equitable_tutoring_mismatch: MATHDIAL's 'Equitable Tutoring' dimension encodes a
    constructivist anti-telling orientation (κ=0.34 inter-annotator agreement) that
    may systematically penalize responses Indian teachers would judge as appropriately
    guidance-rich
  telling_framing_mismatch: The benchmark treats Telling as a last resort and measures
    Telling@k as a negative metric; Indian professional teachers may view directive
    telling as a primary pedagogical tool rather than a failure mode
  form_alignment: No modality, script, or language mismatch — both benchmark and deployment
    are English text-only
annotator_provenance:
  mathdial_annotator_pool: 91 professional teachers recruited via Prolific; majority
    UK nationals, followed by USA, Canada, Australia, India, Germany
  indian_representation: India listed as minority contributor (fifth of six named
    countries); no disaggregated count of Indian annotators reported
  indian_educator_involvement_in_guidance_annotation: '[NOT FOUND — searched MATHDIAL
    paper (arXiv:2305.14536) and ACL Anthology version; no disaggregated count of
    Indian annotators by rating dimension is reported. The paper confirms annotator
    country-level breakdown at Q27 but provides no sub-analysis of which dimensions
    Indian annotators rated. This remains unresolvable from public sources.]'
  annotator_instruction_bias: All annotators explicitly instructed to avoid direct
    correction and to favor Socratic exploration — encoding Western constructivist
    norms regardless of annotator origin
infrastructure_and_access:
  device_context: Mobile and enterprise platforms; English text interface
  internet_connectivity: 'Metro deployment assumes reliable internet access. National
    UDISE+ 2024-25 data: 63.5% of Indian schools have internet connectivity (up from
    53.9% in 2023-24); metro schools in Delhi and Mumbai are expected to have significantly
    higher connectivity rates, though no disaggregated metro-level figure is published.
    Source: UDISE+ 2024-25 — [WEB-8]'
  platform_used: '[NEEDS VERIFICATION — deferred: below search budget; the specific
    LMS or interface through which teachers access tutoring dialogue evaluation is
    not publicly documented and is likely proprietary to the deploying organization]'
  data_protection_regulation: 'The Digital Personal Data Protection Act 2023 (DPDPA),
    enacted 11 August 2023 and operationalized by the DPDP Rules notified 13 November
    2025, is the applicable framework for AI deployments processing personal data
    in India. The Act specifically prohibits processing of children''s data for tracking,
    behavioral monitoring, or targeted advertising, with narrow educational exemptions
    only for defined purposes (e.g., delivering education services). Full substantive
    compliance obligations take effect from May 2027 (Phase III, 18 months from notification).
    Educational AI deployments must comply with consent, notice, data minimization,
    and security obligations as Data Fiduciaries. Source: DPDPA official text (MeitY)
    — [WEB-9];
    DPDP Rules 2025 (Hogan Lovells analysis) — [WEB-10];
    DLA Piper implementation timeline — [WEB-11]'
sub_national_variation:
  delhi_notes: 'Delhi government schools are primarily Hindi-medium, but the government
    has introduced English-medium Schools of Excellence since 2018 and English-medium
    instruction is widespread in the large private-school sector. Women constitute
    61% of Delhi government school teachers (UDISE+ 2023-24). Delhi operates under
    both CBSE and the Delhi Board of Secondary Education. No specific evidence found
    of Delhi-unique pedagogical norms diverging from national-level findings on exam
    orientation and direct instruction. Source: Delhi Schools of Excellence — [WEB-4];
    Delhi teacher gender — [WEB-6]'
  mumbai_notes: Mumbai has significant linguistic diversity (Marathi, Hindi, Gujarati,
    English-medium schools coexist); government schools are predominantly Marathi-medium
    while private schools are heavily English-medium. No metro-specific published
    figure found on the share of English-medium enrollment or teacher gender breakdown
    in Mumbai separately. The sub-national variation (Marathi vs. English medium instruction
    norms) may affect evaluation expectations for teachers from different sectors;
    this is a flagged gap requiring stakeholder elicitation. [NOT FOUND — no Mumbai-specific
    teacher evaluation norm study found in public sources]
  city_level_differentiation_by_user: User did not differentiate between Delhi and
    Mumbai in elicitation; sub-national variation is a flagged gap requiring investigation
regulatory_and_curricular_context:
  curriculum_framework: NCERT/CBSE (National Council of Educational Research and Training
    / Central Board of Secondary Education)
  curriculum_alignment_requirement: Curriculum-agnostic math errors confirmed sufficient;
    no NCERT/CBSE topic or algorithm alignment required for this assessment
  teacher_regulatory_body: 'National Council for Teacher Education (NCTE), a statutory
    body established under the NCTE Act 1993, is the regulatory authority for teacher
    education and minimum qualification standards in India. NCTE sets minimum qualifications
    (D.El.Ed. for primary; B.Ed. for upper primary), accredits teacher education institutions,
    and is revising programs in line with NEP 2020 through the 4-year Integrated Teacher
    Education Programme (ITEP). Source: NCTE official site — [WEB-12];
    NCTE minimum qualifications — [WEB-1]'
  ai_in_education_policy: 'India''s NEP 2020 and NCERT''s CIET (Central Institute
    of Educational Technology) have both addressed AI in schools. NEP 2020 emphasizes
    technology integration and acknowledges AI''s potential for personalized learning
    and intelligent tutoring systems. CIET-NCERT ran a ''Leveraging AI for Transforming
    School Education'' teacher training series in January 2026, framing AI as a tool
    that ''augments teachers'' pedagogical capabilities rather than replacing the
    human element.'' The national DIKSHA platform is positioned as the primary ecosystem
    for AI-enabled educational resources. No specific regulation on AI tutoring tool
    use in classrooms was found; the DPDPA 2023/Rules 2025 and the NEP 2020 framework
    together constitute the operative policy environment. Source: CIET-NCERT AI training
    program (Jan 2026) — [WEB-13]'
  national_education_policy_2020_relevance: 'NEP 2020 explicitly promotes technology
    integration including AI and coding from Class 6 onward, personalized learning,
    and teacher training in technology use. It also envisages a National Educational
    Technology Forum (NETF). The policy shift from rote learning toward competency-based
    education may create a slight receptivity gap relative to the exam-oriented direct-instruction
    culture that currently dominates Indian metro classrooms — a tension relevant
    to how Indian teachers evaluate AI tutoring quality. NCTE is revising all teacher
    education programs in alignment with NEP 2020. Source: Multiple NEP 2020 AI integration
    analyses — [WEB-14];
    CIET-NCERT — [WEB-13]'
existing_india_specific_benchmarks:
  known_alternatives: 'No India-specific math tutoring dialogue benchmark capturing
    CBSE/NCERT classroom interaction dynamics or Indian student deferential behavior
    profiles was found. The closest existing resources are: (1) MILU (Multi-task Indic
    Language Understanding, Verma et al. 2024) — covers 11 Indic languages across
    8 domains including STEM, India-first perspective using national/state exam questions,
    but is a knowledge QA benchmark not a tutoring dialogue benchmark; (2) IndicEval
    (2026) — bilingual (English/Hindi) evaluation using UPSC/JEE/NEET questions, grounded
    in Indian high-stakes examinations, but again a reasoning benchmark not a pedagogical
    dialogue benchmark; (3) GSM8K-Hi — Hindi version of GSM8K (the same base dataset
    as MATHDIAL), created by NVIDIA with human annotation + translate-and-verify,
    but focused on math reasoning not tutoring interaction. None of these capture
    Indian classroom discourse, deferential student interaction styles, or tutoring
    quality evaluation from an Indian pedagogical standpoint. Source: MILU — [WEB-15];
    IndicEval — [WEB-16]; Hindi LLM benchmarks suite
    (NVIDIA) — [WEB-17]'
  relevant_datasets: 'The PARIKSHA benchmark (Watts et al. 2024) evaluates LLM outputs
    across 10 Indic languages using human annotators in a multicultural setting, covering
    finance, health, and culture topics. A key finding directly relevant to this deployment:
    ''LLM evaluators tend to align less with human evaluations on assessing culturally
    nuanced responses.'' This supports the expectation of divergence between MATHDIAL''s
    Western-norm ground truth and Indian teacher judgments. No dataset capturing Hindi-English
    code-switching in math tutoring or Indian classroom discourse corpora was found.
    Source: PARIKSHA — [WEB-18]'
  net_new_finding_indic_benchmark_gap: 'A systematic review of Indic LLM evaluation
    datasets (2025) found that ''a majority of these datasets are a direct translation
    of existing English datasets which is a serious limitation'' and that ''models
    may fare poorly on tasks where socio-cultural understanding is required.'' This
    directly corroborates the OC validity risk: even general cultural benchmarks for
    India are predominantly translated from English, and no pedagogical-dialogue benchmark
    with Indian classroom grounding exists. Source: Analysis of Indic Language Capabilities
    in LLMs — [WEB-15]'
validity_risk_summary:
  highest_risk_dimensions:
  - dimension: IC — Input Content (HIGH)
    risk: MATHDIAL's simulated student dialogues do not reflect Indian classroom interaction
      norms (deferential, brief, low-verbalization students); construct-irrelevant
      variance at the individual datapoint level
  - dimension: OC — Output Content (HIGH)
    risk: Ground-truth quality standards encoded by predominantly Western annotators
      instructed toward Socratic scaffolding; systematic divergence expected from
      Indian professional teachers' direct-correction preferences
  moderate_risk_dimensions:
  - dimension: OO — Output Ontology (MODERATE)
    risk: Primacy of 'providing guidance' in Indian context not commensurately weighted
      in MATHDIAL's three co-equal human evaluation dimensions; Equitable Tutoring
      operationalization encodes constructivist anti-telling bias
  lower_risk_dimensions:
  - dimension: IO — Input Ontology (LOWER)
    risk: Curriculum-agnostic errors and eight benchmark categories accepted as sufficient;
      reduced ontological gap
  - dimension: IF — Input Form (LOWER)
    risk: No modality or script mismatch; both benchmark and deployment are English
      text-only
  - dimension: OF — Output Form (LOWER)
    risk: No output-form mismatch; text-based open-ended tutoring dialogue in both
      benchmark and deployment
cultural_norms_notes: 'Key pedagogical and cultural characteristics relevant to this
  deployment population:

  - Teacher authority: Strong hierarchical teacher-student relationship; teachers
  are primary knowledge source, not Socratic facilitators

  - Exam orientation: Evaluation of tutoring quality is heavily mediated by perceived
  exam-readiness of the guidance provided

  - Direct correction norm: Explicit correction of student errors is a culturally
  accepted and expected teacher behavior, not a pedagogical failure

  - Student deference: Students are expected to be brief, deferential, and receptive
  rather than expressive or reasoning-out-loud

  - Procedure primacy: Step-by-step algorithmic correctness is valued over conceptual
  exploration

  - L2 math instruction: Many students receive math instruction in English as a second
  language; teachers calibrate guidance for language-mediated misunderstandings

  - Professional identity: Teachers identify as subject-matter authorities and correctors,
  not as coaches or facilitators in the constructivist sense

  - Rote and drill culture: Memorization and repeated practice of standard procedures
  remain normative in many Delhi/Mumbai school environments [NEEDS VERIFICATION —
  deferred: likely unsearchable (lived practice); sub-school-type variation not aggregated
  in public sources]

  - NEP 2020 tension: The policy aspiration toward competency-based, technology-assisted
  personalized learning (NEP 2020) exists alongside the deeply entrenched exam-oriented
  direct-instruction culture; the degree to which metro teachers have internalized
  NEP 2020''s constructivist framing is unknown and requires stakeholder elicitation'
net_new_fields:
  ncte_regulatory_update_2025: 'NCTE issued new rules for B.Ed and D.El.Ed programs
    effective 2025, including: banning simultaneous enrollment in both programs, mandatory
    6-month school internship for all teacher trainees, and stricter admission rules.
    The 4-year Integrated Teacher Education Programme (ITEP) is slated to become mandatory
    for all school teachers by 2030. These reforms affect the credential profile of
    incoming teachers but do not change the current minimum standards for the deployed
    evaluator population. Source: NCTE new B.Ed/D.El.Ed rules 2025 — [WEB-19]'
  dpdpa_child_data_provisions: 'The DPDP Rules 2025 (notified November 2025) include
    specific provisions for educational institutions: they are among the exempt classes
    for certain child data processing (e.g., delivering education services), but this
    is a narrow, purpose-specific carve-out. The Act prohibits processing detrimental
    to child well-being or involving behavioral monitoring/targeted advertising of
    children. For the AI tutoring deployment, the DPDPA''s child data protections
    are highly relevant: student interaction data in tutoring sessions likely constitutes
    personal data of minors, requiring careful data governance design. Source: Hogan
    Lovells DPDP Rules 2025 analysis — [WEB-10]'
  indic_llm_evaluator_human_alignment_gap: 'The PARIKSHA study (2024) found that LLM
    evaluators align less with human evaluations specifically on culturally nuanced
    responses across 10 Indian languages. This is a directly relevant methodological
    caution for the deployment: if LLM-as-judge is used at any stage of the pipeline
    (e.g., filtering, pre-screening), alignment with Indian teacher judgments cannot
    be assumed and may be lower than alignment with the Western-norm MATHDIAL ground
    truth. Source: PARIKSHA — [WEB-18]'
  india_specific_math_education_benchmarks_absence: 'A search across ACL Anthology,
    arXiv, and general academic sources found no India-specific math tutoring dialogue
    benchmark capturing Indian classroom interaction norms, CBSE/NCERT curricular
    alignment, or deferential student behavior profiles. The most India-relevant educational
    evaluation frameworks (MILU, IndicEval, GSM8K-Hi) are all knowledge/reasoning
    benchmarks, not pedagogical dialogue quality benchmarks. This confirms a genuine
    documentation gap that materially strengthens the case for the high IC and OC
    validity risk ratings. Source: Indic LLM evaluation landscape review — [WEB-15]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://ncte.gov.in/Website/NCTEACT12.aspx |
| WEB-2 | https://competition.careers360.com/articles/ctet-eligibility-criteria |
| WEB-3 | https://ezyschooling.com/english-medium-schools-in-delhi |
| WEB-4 | https://www.schoolmykids.com/schools/list-of-schools-of-excellence-in-delhi-india |
| WEB-5 | https://idronline.org/article/education/a-closer-look-at-indias-expanding-teaching-workforce/ |
| WEB-6 | https://www.ensureias.com/blog/current-affairs/udise-2023-24-report-reveals-sharp-decline-in-school-enrolment |
| WEB-7 | https://www.newslaundry.com/2025/09/22/mapping-indias-10-million-teachers-in-six-charts |
| WEB-8 | https://educationforallinindia.com/analysis-of-udise-2024-25-data-by-prof-arun-c-mehta/ |
| WEB-9 | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf |
| WEB-10 | https://www.hoganlovells.com/en/publications/indias-digital-personal-data-protection-act-2023-brought-into-force- |
| WEB-11 | https://www.dlapiperdataprotection.com/?t=law&c=IN |
| WEB-12 | https://web.ncte.gov.in/page/introduction |
| WEB-13 | https://ciet.ncert.gov.in/activity/laie |
| WEB-14 | https://www.researchgate.net/publication/377437769_The_Role_of_Artificial_Intelligence_in_Implementing_the_National_Education_Policy-2020_Challenges_and_Opportunities |
| WEB-15 | https://arxiv.org/html/2501.13912v1 |
| WEB-16 | https://arxiv.org/html/2602.16467 |
| WEB-17 | https://arxiv.org/abs/2508.19831 |
| WEB-18 | https://arxiv.org/html/2406.15053v1 |
| WEB-19 | https://sardarpateleducation.com/ncte-new-rules-for-b-ed-and-d-el-ed/ |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: For your Grade 1–8 teachers in Delhi and Mumbai, do the student mistake scenarios covered by the benchmark need to reflect the Indian curriculum (e.g., NCERT/CBSE topics, Indian arithmetic conventions like the Indian place-value system with lakhs and crores, or standard algorithms taught differently in Indian textbooks)? Or would curriculum-agnostic math errors be sufficient for evaluating pedagogical quality?
A1: Curriculum-agnostic math errors are considered sufficient for evaluating pedagogical quality; alignment with Indian curriculum specifics is not required.

Q2 [IC]: The benchmark's student-tutor conversations are drawn from a particular linguistic and cultural context that may not reflect Indian classroom dynamics. For your professional teachers in Indian metros, would the depicted student mistakes, student communication styles, or classroom interaction norms feel realistic and recognisable — or do you expect meaningful differences?
A2: The mathematical content feels broadly familiar, but the interaction dynamics are meaningfully mismatched. Indian students tend to be brief, deferential, and less likely to verbalize reasoning; teachers tend toward direct, exam-oriented correction rather than extended Socratic dialogue. Procedure-heavy learning patterns and language-related misunderstandings common in Indian classrooms are underrepresented in the benchmark's Western-origin dialogues.

Q3 [OO]: The benchmark scores pedagogical quality along multiple dimensions. For your teachers evaluating acceptability of an augmented response, which dimensions matter most — and are there missing dimensions your teachers would actually judge on?
A3: The eight benchmark dimensions are considered necessary and sufficient for the evaluation task. The single most critical dimension is "providing guidance"; no additional dimensions are required.

Q4 [OC]: The benchmark's ground-truth annotations were produced by a likely non-Indian annotator pool. Do you expect your professional Indian teachers' judgments of good guidance to systematically differ from Western educator norms?
A4: Yes, meaningful differences are expected due to Indian cultural context, teaching style, and pedagogy — particularly around preferences for direct correction versus Socratic probing and the weighting of exam-readiness relative to conceptual exploration.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | LOWER | The user confirmed curriculum-agnostic errors suffice and the benchmark's eight pedagogical categories are accepted as necessary and sufficient, removing the main source of ontological misalignment. |
| IC | HIGH | The user explicitly identified that Indian classroom interaction norms — deferential student style, direct teacher correction, procedure-heavy patterns — diverge from the Western-origin dialogue instances in the benchmark, creating construct-irrelevant variance in individual datapoints. |
| IF | LOWER | Both deployment and benchmark are English text-only on mobile/enterprise platforms; no modality or script mismatch exists. |
| OO | MODERATE | The benchmark's eight output dimensions are accepted as sufficient, but the primacy of "providing guidance" in the Indian context may not be weighted commensurately in the benchmark's scoring rubric, creating potential scoring emphasis misalignment. |
| OC | HIGH | The user expects systematic divergence between Indian professional teachers' quality judgments and those of the benchmark's likely non-Indian annotators, particularly on direct-correction vs. Socratic probing and exam-readiness weighting. |
| OF | LOWER | Both benchmark and deployment operate in text-based, open-ended tutoring dialogue format; no output-form mismatch is present. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** eth-nlped/mathdial (default config)
**Analysis date:** 2025-01-31
**Examples reviewed:** 18 from `train` split
**Columns shown:** qid, scenario, question, ground_truth, student_incorrect_solution, student_profile, teacher_described_confusion, self-correctness, self-typical-confusion, self-typical-interactions, conversation
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | mathdial | Ex. 3 | — | "Hi Jia, please talk me through your solution" ... "at what point in time will Maxwell be twice his sister's age?" ... "and what is his sister's age now?" ... "how can you calculate his sister's age in 2 years from now?" | Multi-turn Socratic probing sequence; teacher asks successive guiding questions rather than correcting directly | IC, OC |
| D2 | mathdial | Ex. 12 | — | "Hi Rishi. Can you tell me how many hours it would take Apple to run 24 miles?" ... "Good. How many hours would it take Mac?" ... "How much longer does it take Apple?" ... "How much longer is that in minutes?" ... "So how much faster is Mac then Apple in minutes?" | Six consecutive probing questions guiding student to answer; entirely Socratic, no direct correction | IC, OC |
| D3 | mathdial | Ex. 1 | — | "Carmela has 600*2 + 50 = 1250" ... "It is 1250. Not 2450" ... "600+950+1250 = 2800" | Teacher resorts to Telling only after multiple Focus moves fail; Telling framed as reluctant fallback | OC, OO |
| D4 | mathdial | Ex. 8 | self-correctness=Yes | "ok so Harry donated the $30. We know there is 3 friends who would have donated the other $60 they donated an equasl amount between the three of them for the $60 so how much would of each friend donated?" | Teacher gives extensive step-by-step narration before student arrives at answer; Telling used repeatedly; teacher text contains spelling/grammar errors | IC, OC |
| D5 | mathdial | Ex. 9 | self-correctness=Yes, but I had to reveal the answer | "No 32-7 = 25. So the difference is 25" ... "No. His total runninhg time ws 25 seconds. You need to subtract the amount of time it took him to run up the first half of the hill to find your answer" | Telling moves are labeled and visible in transcript; student resolves confusion only after explicit revelation | OC, OO |
| D6 | mathdial | Ex. 3 | — | "Jia: Sure. I started by figuring out Maxwell's age in 2 years... So, if Maxwell is twice her age in 2 years, he will be 4 years old. Then, I subtracted 2 from 4 to get the answer that Maxwell is currently 2 years old." | Simulated student gives detailed, multi-sentence explanation of reasoning — verbose, articulate, reasoning-out-loud style | IC |
| D7 | mathdial | Ex. 2 | — | "Student: Sure. In the first half of the year, Nicki ran for 26 weeks. Since I wanted to calculate how many miles she ran per week, I divided the total number of weeks by 2 to get the average number of miles she ran per week." | Simulated student produces unprompted multi-clause explanation of own reasoning process | IC |
| D8 | mathdial | Ex. 16 | — | "Student: I divided the total number of desserts (126) by the number of people in the family (7) to find out how many desserts each person would get (18). Then, I divided 18 by 3, since there are 3 types of desserts, to find out how many of each dessert each person would get (6)." | Unprompted full explanation of two-step reasoning from student | IC |
| D9 | mathdial | Ex. 4 | — | "Student: I started by adding the number of racers at the beginning of the race (50) and the number of racers who joined after 20 minutes (30), which gave me a total of 80 racers. Then, I multiplied that number by two... Finally, I subtracted the total number of racers who finished the race (130) from the total number of racers after 30 minutes (160) to get the total number of people who dropped before finishing the race, which was 80." | Three-step unprompted reasoning walkthrough by simulated student | IC |
| D10 | mathdial | Ex. 5 | — | "Student profile: Winnie is a 7th grade student. She struggle most with understanding what the problem is asking them to do." | US-style student name and brief English-language confusion profile; no Indian cultural markers | IC |
| D11 | mathdial | Ex. 9 | — | "Student profile: Rishi is a 7th grade student." | Student name "Rishi" is South Asian; however student behavior pattern (detailed equation explanation) remains Western-expressive | IC |
| D12 | mathdial | Ex. 11 | — | "Teacher: Hi Riyi. Shawn painted 9 red pebbles, 13 blue pebbles, and the 18 remaining pebbles into 3 equal groups of 6 yellow, 6 purple, and 6 green pebbles. Correct?" | Teacher opens by recapping the correct setup — essentially pre-solving before asking student; minimal scaffolding effort | OC |
| D13 | mathdial | Ex. 1 | — | "Student: That's correct. Carmela has $1200 x 2 + $50 = $2450." (after teacher corrects with "Carmela has 600*2 + 50 = 1250") | Student continues to repeat prior error even after told correct answer; simulated LLM student fails to update believably | IC |
| D14 | mathdial | Ex. 10 | — | "Student: Oh, I see. That means he gave Bobby 3 gumballs. He gave him 4 times as many as he gave Alisha, but then subtracted 5. So, 3 = 4 x 2 - 5." (repeated three times with nearly identical text after teacher corrections) | Simulated student persists in same wrong answer verbatim across multiple teacher moves; artificial LLM loop behavior | IC |
| D15 | mathdial | Ex. 1 | — | "question: Cecil has $600. Catherine has $250 less than twice as much as Cecil..." | US-dollar amounts and US-style name inventory (Cecil, Catherine, Carmela); no Indian cultural grounding | IC |
| D16 | mathdial | Ex. 5 | — | "question: Jack collects all his neighbors' recycling and sorts out the cans and bottles to return for the deposit. He gets 10 cents per can." | US-specific recycling-deposit context; cultural scenario without Indian analogue | IC |
| D17 | mathdial | Ex. 17 | — | "question: 20% of the job candidates at a temp agency have experience with Excel. 70% of the candidates are only willing to work day shifts." | US labor-market scenario (temp agency, day-shift context); no Indian cultural equivalent | IC |
| D18 | mathdial | Ex. 6 | — | "Teacher: okay you calculated the time that would take if all the signals are red is 19. but you see the last sentence of the question asks you how much longer will it take if all three lights are green." | Teacher misreads question mid-dialogue ("green" vs. "red"); demonstrates quality imperfection in human-annotator dialogues | OC |
| D19 | mathdial | Ex. 8 | — | "Teacher: Luca do you think yoou could check your answer again please? maye try and think..." / "Teacher: was the total three trimes the amount oof his contribution before oor after he contributed?" | Multiple spelling and typographic errors in teacher utterances; affects naturalness of benchmark dialogue | IF |
| D20 | mathdial | Ex. 15 | — | "Teacher: I feel you have made this more complicated than needed could you maybe find a simpler way" | Generic, mild correction without directing student to specific error; low-directive style | OC |
| D21 | mathdial | Ex. 7 | — | "Teacher: (probing)So 10 people brought an extra guest and 10 did not." / "Student: Yes, that's correct. So the total number of people at the party is 20 + 10 + Ashley = 31." | Teacher states the key intermediate fact directly (borderline Telling/Probing) and student immediately incorporates it | OC |
| D22 | mathdial | Ex. 18 | — | "Teacher: (probing)If my age is 20, my brother's 24 and sister's be 14, can i write 20 + 24 + 16 = 44?" | Teacher uses analogy-based probing — creative but requires student to apply abstract reasoning rather than being told the step | OC |
| D23 | mathdial | Ex. 13 | self-correctness=Yes, but I had to reveal the answer | "Teacher: (telling)You need to find out how many times 48 goes into 192" / "Teacher: (telling)192 divide by 48 =?" / "Teacher: (telling)4 is the correct answer you dont need to calculate further" | Three consecutive Telling moves before student accepts correct answer; demonstrates reluctant resort to direct instruction | OC |
| D24 | mathdial | Ex. 2 | self-correctness=Yes | "Teacher: (generic)Hi mariana, how are you?" / "Student: Hi, I'm doing well. How can I help you?" | Casual social opener from student; register is informal and conversational in Western peer-style rather than deferential | IC |
| D25 | mathdial | Ex. 3 | — | "Jia: Thank you!" | Cheerful single-utterance acknowledgement after successful resolution; brief but not deferential | IC |
| D26 | mathdial | Ex. 4 | — | "Student: Yes, we should subtract what he made from the bottles before we can determine the number of cans. His total earnings are 800 + 0.05x = 1500 cents, or $15." | Student continues to assert wrong setup after teacher redirect; simulated student maintains incorrect position actively | IC |
| D27 | mathdial | Ex. 6 | self-correctness=Yes, but I had to reveal the answer | "Teacher: (telling)19 - 14 = 5 minutes." | Single arithmetic Telling move that resolves the conversation; teacher had already spent multiple Focus moves before telling | OC |
| D28 | mathdial | Ex. 11 | — | "Teacher: (generic)Hi Riyi. Shawn painted 9 red pebbles, 13 blue pebbles, and the 18 remaining pebbles into 3 equal groups of 6 yellow, 6 purple, and 6 green pebbles. Correct?" | Opening move presents the full correct setup to student before posing the actual question; near-complete Telling at the outset | OC |

---

### Deployment-Relevant Strengths

#### Strength 1: Comprehensive teacher move labeling enables multi-dimensional pedagogical evaluation
- **Dimension(s):** IO, OO
- **Observation:** Every teacher utterance in every dialogue is labeled with one of four move types (generic, focus, probing, telling), providing fine-grained annotation for pedagogical quality assessment. The move taxonomy is transparently applied across dialogues of varying complexity.
- **Deployment relevance:** The Indian metro deployment requires professional teachers to evaluate AI tutoring quality across multiple pedagogical dimensions. The labeled taxonomy gives evaluators a structured vocabulary for assessing whether responses are appropriately directive, scaffolding, or generic — directly supporting the benchmark's utility for the stated use case.
- **Datapoint citations:**
  - [D3] Example 1 (train, label=telling): "Carmela has 600*2 + 50 = 1250" — Telling move labeled explicitly; allows downstream assessment of when and how telling is used.
  - [D2] Example 12 (train, label=probing): Six consecutive "(probing)" moves in the conversation header — move sequence is machine-readable and systematically applied.

#### Strength 2: Breadth of student confusion types across procedural and conceptual errors
- **Dimension(s):** IO
- **Observation:** The 18 sampled dialogues cover six distinct confusion categories drawn from prior research on algebra misconceptions: procedural misordering, problem-type misidentification, question misunderstanding, irrelevant-information difficulty, step/procedure understanding gaps, and underlying-principle deficits. Both arithmetic errors and conceptual errors are represented.
- **Deployment relevance:** The user confirmed curriculum-agnostic math errors are sufficient; the breadth of confusion types visible in the sample supports adequate coverage of the student error space for Grades 1–8 math reasoning evaluation.
- **Datapoint citations:**
  - [D10] Example 5 (train): "student_profile: Winnie is a 7th grade student. She struggle most with understanding what the problem is asking them to do." — problem-type misunderstanding category.
  - [D7] Example 2 (train): "student_profile: Mariana is a 7th grade student. She has problem with understanding of what steps or procedures are required to solve a problem." — procedural confusion category.
  - [D8] Example 16 (train): "student_profile: Emily is a 7th grade student. She has problem with understanding of underlying ideas and principles." — conceptual-principle confusion category.

#### Strength 3: Self-correctness annotations enable filtering by tutoring outcome difficulty
- **Dimension(s):** OC, OF
- **Observation:** Every dialogue is annotated by the teacher with a `self-correctness` flag ("Yes," "No," "Yes, but I had to reveal the answer"), allowing users to stratify the dataset by resolution difficulty and teaching strategy used.
- **Deployment relevance:** For Indian metro deployment where the research question is whether GPT-4-augmented responses "meet teacher-acceptable standards," being able to isolate dialogues that required Telling moves (vs. pure scaffolding) is directly useful for understanding where directive instruction was necessary.
- **Datapoint citations:**
  - [D5] Example 9 (train, self-correctness="Yes, but I had to reveal the answer"): Multiple Telling moves before resolution — filterable subpopulation for studying when telling is legitimate.
  - [D23] Example 13 (train, self-correctness="Yes, but I had to reveal the answer"): "Teacher: (telling)4 is the correct answer you dont need to calculate further" — example of dialogues where telling was the terminal resolution strategy.

#### Strength 4: English text-only format matches deployment modality with no encoding gap
- **Dimension(s):** IF, OF
- **Observation:** All 18 sampled examples are English text only. Student profiles, math word problems, teacher turns, student turns, and annotations are all in English natural language. No script variation, transliteration, or code-switching is present.
- **Deployment relevance:** The Indian metro deployment is confirmed as single-language English text-only on mobile/enterprise platforms. There is no modality, script, or encoding mismatch between the benchmark and deployment interface.
- **Datapoint citations:**
  - [D6] Example 3 (train): All turns in standard English prose — no Hindi, Hinglish, or transliteration present in any sampled example.
  - [D15] Example 1 (train): Question, ground truth, student solution, and conversation all in English — consistent with deployment interface requirements.

#### Strength 5: Telling moves do appear in the dataset and are not absent
- **Dimension(s):** OO
- **Observation:** Contrary to a reading that might suggest Telling is systematically suppressed, Telling moves appear in 9 of 18 sampled dialogues and are sometimes used in sequences of multiple consecutive Telling turns when scaffolding fails.
- **Deployment relevance:** While the benchmark penalizes premature Telling via Telling@k, the actual dialogue data includes substantial Telling content that Indian metro teachers (who value direct correction) can evaluate. The labeled presence of these moves means the benchmark is not devoid of directive instruction examples.
- **Datapoint citations:**
  - [D23] Example 13 (train): Three consecutive Telling turns — "You need to find out how many times 48 goes into 192" / "192 divide by 48 =?" / "4 is the correct answer" — showing multi-step direct instruction.
  - [D27] Example 6 (train): "(telling)19 - 14 = 5 minutes." — single definitive Telling that resolves the problem.
  - [D3] Example 1 (train): "(telling)Carmela has 600*2 + 50 = 1250" followed by "(telling)It is 1250. Not 2450" — correction via explicit statement of the right answer.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Simulated student communication style is systematically Western-expressive, misaligning with Indian metro classroom norms
- **Dimension(s):** IC
- **Observation:** Across all 18 sampled examples, the LLM-simulated student invariably produces long, multi-sentence, reasoning-out-loud responses that detail every step of their logic unprompted. This behavior — volunteering full chains of reasoning, explaining their own error, and offering comprehensive solution walkthroughs — is the opposite of the brief, deferential, low-verbalization student behavior the elicitation identifies as characteristic of Indian metro classrooms. The simulated student also pushes back on teacher corrections (in multiple examples continuing to assert wrong answers after being told the correct one), which contrasts with the high-deference interaction norm of Indian students.
- **Deployment relevance:** This is the highest-severity input content concern. When Indian professional teachers use MATHDIAL to evaluate GPT-4 tutoring responses, the dialogues they are evaluating are built on a student simulation that does not represent the students they teach. Teacher moves that make sense in response to a reasoning-out-loud student (Socratic probing to elicit elaboration) may not map to responses Indian teachers would generate for a deferential, silent, or monosyllabic student. This is construct-irrelevant variance at the level of every individual datapoint.
- **Datapoint citations:**
  - [D6] Example 3 (train): "Jia: Sure. I started by figuring out Maxwell's age in 2 years. Since his sister is currently 2 years old, in 2 years she will be 4 years old. So, if Maxwell is twice her age in 2 years, he will be 4 years old. Then, I subtracted 2 from 4 to get the answer that Maxwell is currently 2 years old." — Unprompted four-sentence explanation of entire solution path.
  - [D7] Example 2 (train): "Student: Sure. In the first half of the year, Nicki ran for 26 weeks. Since I wanted to calculate how many miles she ran per week, I divided the total number of weeks by 2 to get the average number of miles she ran per week." — Student explains their own reasoning rationale unsolicited.
  - [D9] Example 4 (train): Three-step reasoning walkthrough volunteered before any question is asked — entirely unlike deferential Indian student behavior.
  - [D24] Example 2 (train): "Student: Hi, I'm doing well. How can I help you?" — Casual, informal peer-level register; not the deferential response ("Yes sir/ma'am") typical of Indian student-teacher interaction.
  - [D14] Example 10 (train): "Student: Oh, I see. That means he gave Bobby 3 gumballs... So, 3 = 4 x 2 - 5." (repeated nearly verbatim three times after teacher corrections) — LLM student loops on wrong answer in an unnatural way that does not reflect human student behavior under any pedagogical norm, but is especially unlike deferential Indian students who would modify behavior upon teacher correction.

#### CRITICAL Concern 2: Ground-truth quality standards encode Socratic anti-telling norms that systematically diverge from Indian professional teacher pedagogy
- **Dimension(s):** OC
- **Observation:** Annotators were instructed to "not just correct student solutions by telling what's correct/incorrect, but to give students the opportunity to explore." This instruction is structurally encoded in the ground-truth dialogues. In the sample, the Socratic mode dominates: multiple Focus and Probing moves are consistently deployed before Telling is used as a last resort. The "Equitable Tutoring" dimension (κ=0.34, the lowest-reliability human evaluation dimension) explicitly rewards withholding answers. Indian professional teachers, who view direct correction as a primary pedagogical tool, would be expected to judge many of the benchmark's preferred teacher behaviors as insufficiently directive and many of the benchmark's penalized Telling behaviors as appropriately guidance-rich.
- **Deployment relevance:** This is the central OC validity risk. The benchmark's ground truth systematically privileges scaffolding over direct instruction. When Indian teachers evaluate GPT-4 responses using this benchmark, the quality standard they are compared against encodes values that the user explicitly identifies as misaligned with their professional norms. The κ=0.34 for Equitable Tutoring means this dimension is already low-reliability even among Western annotators; cross-cultural divergence would be expected to lower it further.
- **Datapoint citations:**
  - [D2] Example 12 (train): Six consecutive probing questions before the student arrives at the answer — this dialogue would score very high on Equitable Tutoring by MATHDIAL standards; Indian teachers would likely prefer more direct guidance earlier.
  - [D3] Example 1 (train): Focus moves deployed four times before Telling is used — annotator instruction to delay Telling is visible in the structure of the dialogue.
  - [D20] Example 15 (train): "Teacher: I feel you have made this more complicated than needed could you maybe find a simpler way" — gentle, vague correction; no direct identification of the error; would likely be rated as inadequate guidance by Indian professional teachers.
  - [D12] Example 11 (train): Teacher opens by restating the full correct setup to the student before asking the trivial question — despite this being nearly a complete solution reveal, it is labeled (generic) not (telling), suggesting the taxonomy may not capture the guidance content Indian teachers would evaluate.
  - [D28] Example 11 (train): "Hi Riyi. Shawn painted 9 red pebbles, 13 blue pebbles, and the 18 remaining pebbles into 3 equal groups of 6 yellow, 6 purple, and 6 green pebbles. Correct?" — The teacher's opening move gives the student almost the entire answer; this is labeled as Generic rather than Telling, illustrating a classification ambiguity that would likely be resolved differently by Indian annotators.

---

#### MAJOR

#### MAJOR Concern 3: Math word problem contexts are US-origin with no Indian cultural grounding
- **Dimension(s):** IC
- **Observation:** All 18 sampled math word problems use US monetary units (dollars and cents), US place-name conventions, US labor-market scenarios (temp agencies, recycling deposits), and names drawn from a Western-diverse but non-Indian name pool. No Indian currency (rupees), no Indian place names, no NCERT-style problem structures appear.
- **Deployment relevance:** While the user confirmed curriculum-agnostic errors are sufficient, the absence of any Indian cultural content in the problems creates a mild ecological validity gap. Indian teachers evaluating AI tutoring responses will be assessing dialogue grounded in cultural contexts (US recycling deposits, US highway driving, US birthday party norms) that are foreign to their students' lived experience. This does not invalidate the benchmark but adds a layer of unfamiliarity that may affect how naturally teachers can judge pedagogical quality.
- **Datapoint citations:**
  - [D16] Example 5 (train): "Jack collects all his neighbors' recycling and sorts out the cans and bottles to return for the deposit. He gets 10 cents per bottle and 5 cents per can." — US bottle-deposit recycling system; no Indian analogue.
  - [D17] Example 17 (train): "20% of the job candidates at a temp agency have experience with Excel. 70% of the candidates are only willing to work day shifts." — US temp-agency labor market context.
  - [D15] Example 1 (train): "Cecil has $600. Catherine has $250 less than twice as much as Cecil" — US dollar denominations; Indian problems would use rupees (₹) and may use lakh/crore notation.

#### MAJOR Concern 4: Simulated student interaction quality degrades in ways that are artificial rather than pedagogically representative
- **Dimension(s):** IC
- **Observation:** In multiple sampled dialogues, the LLM student simulation produces behavior that is not naturalistic for any real student: repeatedly looping on the same incorrect answer verbatim after explicit teacher correction, updating only partially, or producing self-contradictory statements within single turns. This is an artifact of LLM temperature sampling, not a representation of any student population's confusion patterns.
- **Deployment relevance:** When Indian teachers use MATHDIAL to evaluate GPT-4 tutoring responses, the student they see in the dialogue is displaying confusion patterns that would not occur in real Indian classrooms. Teacher responses that are calibrated to a looping, non-updating LLM student may differ substantially from what Indian teachers would produce for a real deferential student who has simply stopped responding or gives a brief wrong answer. This reduces the ecological validity of the dialogues as a testing ground for Indian classroom tutoring quality.
- **Datapoint citations:**
  - [D13] Example 1 (train): "Student: That's correct. Carmela has $1200 x 2 + $50 = $2450." — Student verbally agrees with the teacher's correction ("That's correct") while simultaneously repeating the wrong calculation.
  - [D14] Example 10 (train): "Student: Oh, I see. That means he gave Bobby 3 gumballs. He gave him 4 times as many as he gave Alisha, but then subtracted 5. So, 3 = 4 x 2 - 5." — Identical wrong statement repeated three times across consecutive teacher moves despite different teacher approaches.
  - [D26] Example 5 (train): Student continues to assert wrong setup "His total earnings are 800 + 0.05x = 1500 cents" after teacher has already redirected twice.

#### MAJOR Concern 5: Telling@k metric framework treats direct instruction as a failure mode, misaligning with Indian professional teacher evaluation criteria
- **Dimension(s):** OO
- **Observation:** The benchmark's Telling@k metric measures the proportion of conversations where the teacher explicitly reveals the answer before the student solves it independently — and frames this as a negative outcome to be minimized. In the sampled data, Telling sequences are structurally positioned as late-stage fallbacks, occurring after multiple scaffolding failures. However, Indian professional teachers (per the elicitation) consider direct correction a primary — not last-resort — pedagogical strategy, and would view early Telling as appropriate guidance rather than a quality deficit.
- **Deployment relevance:** If MATHDIAL's Telling@k metric is used to evaluate GPT-4 augmented responses in the Indian metro context, responses that Indian teachers would rate as "adequately directive" may be systematically penalized as "prematurely telling." This scoring emphasis misalignment means the benchmark's automatic evaluation framework may produce quality rankings that are inverted relative to Indian professional teacher judgments.
- **Datapoint citations:**
  - [D5] Example 9 (train, self-correctness="Yes, but I had to reveal the answer"): Telling is labeled as a failure-adjacent outcome ("had to reveal") even when it successfully resolved the student's confusion — the framing encodes Telling as inferior.
  - [D23] Example 13 (train, self-correctness="Yes, but I had to reveal the answer"): Three consecutive Telling moves succeed — labeled as "had to reveal," not as "appropriate directive guidance."
  - [D27] Example 6 (train, self-correctness="Yes, but I had to reveal the answer"): Single Telling move resolves a long stuck conversation — again framed as a fallback rather than a legitimate first-line strategy.

---

#### MINOR

#### MINOR Concern 6: Teacher utterance quality is uneven, including factual errors and typographic issues
- **Dimension(s):** OC
- **Observation:** Several teacher utterances contain spelling errors, grammatical issues, and at least one factual/reading error mid-dialogue. This affects the naturalness of the benchmark dialogues as representatives of professional teaching behavior.
- **Deployment relevance:** Indian professional teachers evaluating AI tutoring responses against MATHDIAL ground truth may notice the imperfect teacher utterances and find the benchmark's standard of "professional teaching" lower than expected. This is a minor concern unlikely to substantially affect validity scoring.
- **Datapoint citations:**
  - [D19] Example 8 (train): "Luca do you think yoou could check your answer again please? maye try and think of the total more than referring the contribution to x" / "was the total three trimes the amount oof his contribution before oor after he contributed?" — Multiple spelling errors in teacher turns.
  - [D18] Example 6 (train): "okay you calculated the time that would take if all the signals are red is 19. but you see the last sentence of the question asks you how much longer will it take if all three lights are green." — Teacher misquotes the question (it asks about red lights, not green lights); factual error in teacher utterance.

#### MINOR Concern 7: Student name diversity is nominal and does not extend to interaction dynamics
- **Dimension(s):** IC
- **Observation:** The sample includes student names from diverse backgrounds (Rishi, Riya, Jia, Luca, DeAndre, Winnie, Hunter, Mariana, Brenda, Ronny, Emily). One name (Rishi) is recognizably South Asian. However, the interaction dynamics (verbose, reasoning-out-loud, peer-register) are identical across all student names — the nominal name diversity does not translate to behavioral diversity.
- **Deployment relevance:** Indian teachers evaluating dialogues featuring a student named "Rishi" may expect behavior patterns consonant with Indian classroom norms. The disconnect between the culturally-suggestive name and the Western-expressive behavior pattern is a minor additional form of ecological mismatch, though it is unlikely to substantially affect benchmark validity scoring.
- **Datapoint citations:**
  - [D11] Example 9 (train): "student_profile: Rishi is a 7th grade student." — South Asian name, but the student's dialogue behavior (detailed equation explanation, confident assertion of wrong answers) is indistinguishable from students named Hunter or Brenda.
  - [D25] Example 3 (train): "Jia: Thank you!" — Brief turn, but overall the "Jia" character is as verbose as other student profiles throughout the dialogue.

---

### Content Coverage Summary

The 18 sampled MATHDIAL dialogues are coherent, consistently structured tutoring conversations grounded in elementary school math reasoning problems (multi-step word problems involving arithmetic, percentages, rates, and equations). Every dialogue follows the same format: a student arrives with a specific incorrect solution, a teacher opens with a generic move, then uses Focus and Probing moves in the middle, and resorts to Telling when stuck. The conversations are labeled at the move level throughout.

The dominant register is informal but pedagogically oriented: teachers use question-posing, hint-giving, and occasional direct correction; students produce long, articulate explanations of their reasoning. Culturally, the content is entirely US/UK-origin: dollar amounts, US names, US scenarios (recycling, temp agencies, birthday parties). Student profiles reference English-language confusion taxonomies drawn from algebra misconceptions research. No Indian cultural content, no Indian currency, no Indian names (beyond nominal), and no Hindi or code-switching appear in any sampled example.

The benchmark's pedagogical stance is visibly constructivist: the data reflects an annotator population trained to prefer scaffolding over direct correction, and this preference is structurally embedded in the dialogue flow. Telling moves exist but are positioned as late-stage fallbacks, flagged with "had to reveal" in self-correctness annotations. The Equitable Tutoring dimension's constructivist anti-telling orientation is operationally present in every sampled conversation.

---

### Limitations

**Sample size:** 18 examples from a 2,262-example training split (~0.8% coverage). Coverage statistics about rare confusion types, edge-case teacher behaviors, or outlier dialogue structures cannot be reliably estimated from this sample.

**Split coverage:** Only the training split was sampled. The test split (599 examples, including an "unseen problems" subset) was not reviewed; it may have different distributional properties.

**Self-typicality ratings unverified:** The `self-typical-confusion` and `self-typical-interactions` fields are teacher-reported Likert ratings (1–5), but what these ratings mean at the distributional level (e.g., what fraction of dialogues are rated low-typicality) cannot be established from 18 examples.

**Annotator-level disaggregation not inspectable:** The dataset does not expose which of the 91 annotators produced which dialogue, so it is impossible to identify whether any Indian-origin annotators contributed to the sampled examples or whether any dialogues reflect Indian pedagogical norms at the individual level.

**Conversation field is serialized text:** The `conversation` field encodes the full dialogue as a pipe-delimited string with `|EOM|` separators and inline move labels. Turn-level statistics (average student turn length, probing ratio per dialogue) would require parsing; approximate patterns visible in the sample suggest student turns are uniformly verbose.

**No test-split examples reviewed:** The benchmark's seen/unseen problem split distinction (60%/40% of test problems) and its implications for coverage cannot be assessed without sampling from the test split.

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
  "benchmark": "mathdial",
  "region": "Indian Metropolitan Professional Teachers (Grades 1–8)",
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
