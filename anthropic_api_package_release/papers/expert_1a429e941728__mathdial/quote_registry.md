---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | data_sources | "We describe how we use this framework to collect MATHDIAL, a dataset of 3k one-to-one teacher-student tutoring dialogues grounded in multi-step math reasoning problems." |
| Q2 | 1 | data_sources | "To address this, we propose a framework to generate such dialogues by pairing human teachers with a Large Language Model (LLM) prompted to represent common student errors." |
| Q3 | 1 | task_taxonomy | "We let teachers provide learning opportunities to students by guiding them using various scaffolding questions according to a taxonomy of teacher moves." |
| Q4 | 1 | label_categories | "We demonstrate MATHDIAL and its extensive annotations can be used to finetune models to be more effective tutors (and not just solvers)." |
| Q5 | 1 | evaluation_metrics | "We confirm this by automatic and human evaluation, notably in an interactive setting that measures the trade-off between student solving success and telling solutions." |
| Q6 | 1 | stated_limitations | "While models like GPT-3 are good problem solvers, they fail at tutoring because they generate factually incorrect feedback or are prone to revealing solutions to students too early." |
| Q7 | 1 | authors_affiliations | "Jakub Macina, Nico Daheim, Sankalan Pal Chowdhury, Tanmay Sinha, Manu Kapur, Iryna Gurevych, Mrinmaya Sachan." |
| Q8 | 1 | authors_affiliations | "ETH AI Center, Department of Computer Science, ETH Zurich, Ubiquitous Knowledge Processing Lab (UKP Lab), Department of Computer Science and Hessian Center for AI (hessian.AI), TU Darmstadt, National Institute of Education, Nanyang Technological University, Professorship for Learning Sciences and Higher Education, ETH Zurich." |
| Q9 | 2 | task_taxonomy | "Research on task-oriented dialogue systems has mainly focused on customer service, for instance, restaurant reservations (Henderson et al., 2014; Gašic et al., 2014)." |
| Q10 | 2 | data_sources | "Notably, Wen et al. (2017) collect such dialogues with the Wizard-of-Oz (WoZ) paradigm (Kelley, 1984), where crowdworkers are connected to roleplay interlocutors." |
| Q11 | 2 | data_sources | "WoZ has been used to collect many popular datasets, such as MultiWoZ (Budzianowski et al., 2018) and extensions (Kim et al., 2020; Zhu et al., 2020), Taskmaster (Byrne et al., 2019), and open-domain datasets like Wizard-of-Wikipedia (Dinan et al., 2019)." |
| Q12 | 2 | data_sources | "Other collection methods include crowdworkers filling dialogue outlines (Shah et al., 2018; Rastogi et al., 2020; Majewska et al., 2023), or scraping from the web (Li et al., 2017; Dziri et al., 2019)." |
| Q13 | 2 | stated_limitations | "Multiple works have shown shortcomings in using non-expert crowdworkers." |
| Q14 | 2 | stated_limitations | "For instance, document-grounded corpora often contain hallucinations in ground-truth data (Dziri et al., 2022), and task-oriented corpora tend to suffer from annotation errors and low lexical diversity (Casanueva et al., 2022)." |
| Q15 | 2 | stated_limitations | "More closely related to this work, current tutoring corpora lack sufficient tutoring quality" |
| Q16 | 3 | data_sources | "Figure 2: Overview of the data collection pipeline: First, student confusions are oversampled from an LLM and sorted by frequency. Then, a human teacher synchronously interacts with a student simulated by an LLM that is instructed with a student profile and incorrect solution." |
| Q17 | 3 | task_taxonomy | "MATHDIAL mitigates these issues by adapting the WoZ paradigm to using human teachers as experts in collaboration with an LLM." |
| Q18 | 3 | task_taxonomy | "Theoretical and empirical studies have shown the importance of questioning in human learning (Roscoe and Chi, 2008; Shahriar and Matsuda, 2021; Shridhar et al., 2022)." |
| Q19 | 3 | task_taxonomy | "Nye et al. (2014), for instance, show the effectiveness of deep reasoning questions, and (Howe et al., 2019) find that elaboration and challenging of previous contributions can benefit student learning." |
| Q20 | 3 | stated_limitations | "All of them suffer from several limitations, such as missing grounding information (TSCC, TalkMoves, NCTE), low tutoring quality (CIMA), small dataset sizes (all), or a focus on noisy classroom scenarios (see Table 1)." |
| Q21 | 3 | stated_limitations | "However, Tack and Piech (2022); Macina et al. (2023) show that they can not yet perform well as teachers out-of-the-box, because they often incorrectly assess student solutions and reveal answers too quickly." |
| Q22 | 3 | data_sources | "This section introduces a framework for collecting high-quality tutoring conversations, highlighted in Figure 2. The core idea behind it is to connect" |
| Q23 | 4 | annotation_process | "We recruit professionals with teaching experience through Prolific. We only select teachers who have completed at least 500 submissions and achieved a 100% completion rate." |
| Q24 | 4 | annotation_process | "Annotators read guidelines for the task in an initial training phase (cf. Section D.3) and then complete a test on an example conversation to assess their understanding of the task." |
| Q25 | 4 | annotation_process | "We only select annotators with 100% test scores for further rounds of data collection, similar to Zhang et al. (2023)." |
| Q26 | 4 | annotation_process | "We employ 91 expert annotators, of which 71 identify as female and 18 as male." |
| Q27 | 4 | annotation_process | "The majority of annotators are nationals of the UK, followed by the USA, Canada, Australia, India, and Germany, with a median age of 39 years." |
| Q28 | 4 | data_sources | "We employ an LLM to generate plausible student confusions and base the dialogues on them." |
| Q29 | 4 | data_sources | "We pick the most frequent incorrect solution sampled from ChatGPT (gpt-3.5-turbo) (Ouyang et al., 2022) using chain-of-thought prompting." |
| Q30 | 4 | data_format | "To be precise, we first use temperature sampling to obtain N = 50 reasoning paths for every MWP in GSM8k, with T = 0.7 and no top-k truncation Wang et al. (2023b)." |
| Q31 | 4 | data_format | "Then, we group incorrect solutions according to their final numeric answer and pick one from the set with the largest cardinality." |
| Q32 | 5 | data_sources | "We use InstructGPT (text-davinci-003) (Ouyang et al., 2022) to generate student turns." |
| Q33 | 5 | data_format | "We prompt the model with the previous dialogue history and additional information that grounds the next turn." |
| Q34 | 5 | data_format | "The prompt contains the MWP, the initial student confusion, as well as the student profile which explains the type of confusion and persona of the student." |
| Q35 | 5 | task_taxonomy | "This section defines the taxonomy of all teacher moves that are used in MATHDIAL." |
| Q36 | 5 | task_taxonomy | "We base the first two on the work of Reiser (2004), who suggest that scaffolding strategies can be split into two main categories: structure and problematize." |
| Q37 | 5 | task_taxonomy | "These form the basis for the Focus and Probing moves employed in our study." |
| Q38 | 5 | task_taxonomy | "Focus is used to constrain the student to make direct progress towards solving the problem." |
| Q39 | 5 | task_taxonomy | "Probing is used to generalize certain aspects of the problem which allows the student to explore its underlying concepts." |
| Q40 | 5 | task_taxonomy | "This is called Telling." |
| Q41 | 5 | task_taxonomy | "Finally, turns that just serve as conversational elements and have limited pedagogical value are classed as Generic." |
| Q42 | 5 | task_taxonomy | "Table 2 lists finer-grained intents for each of these four categories along with a set of accompanying examples." |
| Q43 | 5 | evaluation_metrics | "We quantitatively evaluate the collected tutoring dialogues to assess their quality." |
| Q44 | 5 | evaluation_metrics | "First of all, we can see that our dataset is significantly larger in terms of the number of dialogues and utterances than all related datasets that are listed." |
| Q45 | 5 | data_sources | "By open-sourcing such a large dataset, we fill a crucial gap of sufficiently-sized open-source tutoring corpora which has so far hindered research in the area (Macina et al., 2023)." |
| Q46 | 5 | evaluation_metrics | "Furthermore, MATHDIAL exhibits a higher diversity, measured in bigram entropy (Zhang et al., 2018), than CIMA and TalkMoves." |
| Q47 | 5 | evaluation_metrics | "The diversity is similar to NCTE and TSCC which consist of transcripts of classroom and one-to-one tutoring sessions, respectively." |
| Q48 | 5 | annotation_process | "This supports the observation that expert annotators tend to create more diverse utterances than untrained crowdworkers (Casanueva et al., 2022), and also that LLMs can be used to generate diverse tutoring dialogues." |
| Q49 | 5 | evaluation_metrics | "Finally, we measure the Uptake (Demszky et al., 2021) of annotated teacher utterances." |
| Q50 | 5 | evaluation_metrics | "Uptake indicates how coherent the teacher's utterance is with respect to the previous student's turn." |
| Q51 | 5 | evaluation_metrics | "We find that MATHDIAL and CIMA have similar uptake." |
| Q52 | 5 | evaluation_metrics | "Both surpass the other datasets in our comparison." |
| Q53 | 5 | data_sources | "Our collection methodology relies on LLMs for simulating students." |
| Q54 | 5 | stated_limitations | "Therefore, it is crucial to ensure that the turns simulated by the LLM also match what a teacher would expect of a real student, who in our case is a sixth grader." |
| Q55 | 5 | annotation_process | "Figure 3 shows that annotators rate the majority of generations by the model positively along two dimensions." |
| Q56 | 5 | label_categories | "The first one says that the confusion of the student is typical confusion of a sixth grader." |
| Q57 | 5 | label_categories | "The second one says that the interaction with the student as a whole is as expected of a sixth grader." |
| Q58 | 5 | annotation_process | "We release these annotations with our final dataset which allows users of MATHDIAL to filter out utterances that are of a lower quality." |
| Q59 | 5 | stated_limitations | "Moreover, LLMs can be prone to incorrect arithmetic calculations." |
| Q60 | 5 | annotation_process | "Therefore, we asked annotators to distinguish conceptual errors from such simple calculation mistakes." |
| Q61 | 5 | label_categories | "Arithmetic errors may be easily resolved through calculators but conceptual errors are likely to require tutors to resolve them, for example by scaffolding." |
| Q62 | 5 | annotation_process | "Annotators identified around 80% of the confusions as conceptual, leaving around a fifth containing arithmetic errors." |
| Q63 | 5 | annotation_process | "Again, we include these annotations to allow for data filtering." |
| Q64 | 5 | evaluation_metrics | "In this Section, we evaluate when teachers use which teacher moves in the conversations." |
| Q65 | 5 | evaluation_metrics | "Figure 4 shows that teachers most frequently use Focus questions which are found in 37% of utterances." |
| Q66 | 5 | evaluation_metrics | "Focus is followed by Generic and Probing." |
| Q67 | 5 | evaluation_metrics | "Telling is the rarest move." |
| Q68 | 5 | annotation_process | "To validate these annotations, we sampled 17 conversations consisting of 102 teacher utterances and asked two independent annotators to" |
| Q69 | 6 | annotation_process | "We obtain an agreement of κ = 0.60 between the two annotators and κ = 0.49 and κ = 0.34, respectively, between either of the annotators and the teacher." |
| Q70 | 6 | stated_limitations | "We note that Probing and Focus appear to be particularly challenging to distinguish and acknowledge that the boundary between them may be subjective." |
| Q71 | 6 | annotation_process | "Merging these two categories into one larger 'scaffolding' category improves agreements to κ = 0.67, κ = 0.75 and κ = 0.55." |
| Q72 | 6 | stated_limitations | "Our observations are in line with related works that have shown low inter-annotator agreement between experts for detailed teacher moves in classroom settings (Kelly et al., 2020)." |
| Q73 | 6 | task_taxonomy | "The sequence of moves employed by the teachers constitutes their teaching strategy which we analyze in the following." |
| Q74 | 6 | task_taxonomy | "We find that the initial utterance by the teacher is usually generic and serves as a conversation opener, oftentimes by asking the student to repeat the question or solution attempt." |
| Q75 | 6 | task_taxonomy | "During the conversation, teachers mainly use scaffolding to either probe the student or focus the conversation on a specific part of the problem." |
| Q76 | 6 | task_taxonomy | "The more the conversations progress the more likely teachers are to resort to Telling because students often get stuck at a specific subproblem and are unable to resolve it themselves." |
| Q77 | 6 | task_taxonomy | "The goal of MATHDIAL is to enable building tutors that can help students resolve their confusion." |
| Q78 | 6 | label_categories | "Teachers assessed that they were successful in almost 89% of the conversations." |
| Q79 | 6 | label_categories | "In ca. 75% of the conversations by using mainly scaffolding questions, and only in around 14% by revealing the majority of the answer." |
| Q80 | 6 | task_taxonomy | "The conversations in which confusions could not be resolved can still be useful, as they, for instance, can be used to train classifiers to determine when human intervention in such tutoring sessions is required." |
| Q81 | 6 | task_taxonomy | "We focus our initial studies on MATHDIAL on the task of tutor response generation." |
| Q82 | 6 | task_taxonomy | "Tutor response generation aims to model the teacher in a dialogue by generating follow-up turns to guide the student towards learning and solving the problem." |
| Q83 | 6 | evaluation_metrics | "We compare different finetuned and prompted language models on the task and evaluate how much detailed information that can be given to the model, such as step-by-step solutions of the MWP, influence performance." |
| Q84 | 6 | data_format | "We use neural conditional language models that given a tutoring dialogue history u_1^T, grounding" |
| Q85 | 7 | data_format | "We split our data into a training split containing 80% of the conversations and a test set containing the remaining 20%." |
| Q86 | 7 | data_format | "Around 60% of the problems in the test set are also found in the training data, where at least one conversation was based on it, and therefore constitute our 'seen' split." |
| Q87 | 7 | data_format | "The remaining 40% are unseen during training and test the ability of the model to generalize to new problems." |
| Q88 | 7 | data_format | "The dataset split is published with the dataset." |
| Q89 | 7 | evaluation_metrics | "We assess our models using the sacrebleu (Post, 2018) implementation of BLEU (sBLEU) (Papineni et al., 2002), as well as BERTScore between generated response (uT +1) and annotated response (uˆT +1) for each teacher response in the conversation." |
| Q90 | 7 | evaluation_metrics | "Furthermore, in line with previous works (Dziri et al., 2022; Daheim et al., 2023), we report BERTScore and the token level F1 (KF1) between generated utterance and math word problem as a proxy for faithfulness." |
| Q91 | 7 | stated_limitations | "However, we note that an increase in these metrics can be caused by an increase in overlap, which may also indicate more telling and can be undesirable." |
| Q92 | 7 | stated_limitations | "However, finding good evaluation metrics for assessing the faithfulness of dialogue tutors remains an open problem." |
| Q93 | 7 | evaluation_metrics | "Finally, we measure the Uptake of the generated response (Demszky et al., 2021)." |
| Q94 | 7 | evaluation_metrics | "We propose two evaluation metrics for end-to-end tutoring, where a tutor model is evaluated interactively by using it to teach an LLM that simulates a student." |
| Q95 | 7 | evaluation_metrics | "Success@k measures the percentage of conversations where the student reaches the correct final answer at least once within the first k turns (equivalent of % solve rate in prior work)." |
| Q96 | 7 | evaluation_metrics | "Telling@k measures the percentage of conversations where the teacher explicitly tells the final answer before the student has reached it on their own within the first k turns." |
| Q97 | 8 | evaluation_metrics | "Finally, we conduct a human evaluation according to three criteria: 1) Coherence: how coherent the teacher's response is with respect to the preceding dialogue, 2) Correctness: whether it is in itself correct, and 3) Equitable tutoring." |
| Q98 | 8 | evaluation_metrics | "Equitable tutoring describes how well the model provides the student with room for exploring the problem and solution space." |
| Q99 | 8 | annotation_process | "We use three expert annotators that each annotate n = 50 responses." |
| Q100 | 8 | annotation_process | "We obtain agreements of κ = 0.29, κ = 0.69, and κ = 0.34 for the three categories." |
| Q101 | 8 | evaluation_metrics | "Good tutoring models need to maintain high quality not only when viewed per-utterance but especially over an entire conversation." |
| Q102 | 8 | evaluation_metrics | "In order to assess this, we use them to tutor an InstructGPT student and measure their success (Success@k), as well as the rate of telling (Telling@k)." |
| Q103 | 9 | data_sources | "Our dataset consists of ca. 3k tutoring conversations grounded in math word problems from GSM8k." |
| Q104 | 9 | task_taxonomy | "We benchmark open-source models on the task of tutor response generation and show that smaller models finetuned on our MATHDIAL can significantly surpass the performance of much larger prompted LLMs." |
| Q105 | 9 | evaluation_metrics | "In our proposed interactive tutoring simulation, the finetuned model achieves similar student-solving success as prompted LLM while keeping the direct telling rate lower." |
| Q106 | 9 | stated_limitations | "In this work, we used an LLM to simulate student confusion. However, we acknowledge that these models have a limited understanding of human learning and this is a key limitation in our dataset – certain kinds of student confusions may be under- or over-represented in our dataset." |
| Q107 | 9 | data_sources | "We introduce a new framework for semi-synthetic dialogue dataset collection. We use it to collect a pedagogically rich dataset for tutoring math word problems that follow equitable tutoring practices and learning sciences research on scaffolding student understanding, called MATHDIAL." |
| Q108 | 10 | stated_limitations | "Furthermore, in our setup, teachers were interacting with an LLM role-playing as a student. However, it is possible that some teachers might have learned to interact with the student model in a different way than they would do in the classroom." |
| Q109 | 10 | stated_limitations | "Moreover, it is also possible that some teachers may have lost motivation when found out they are not interacting with real students, leading to lower data quality." |
| Q110 | 10 | stated_limitations | "In the future, we would like to explore solutions to build better LLM-based student models (Zhou et al., 2023)." |
| Q111 | 10 | stated_limitations | "The methodology to collect the dataset was instantiated just for the domain of math reasoning. The collection of additional domain-specific datasets is necessary to further generalize the effectiveness of our methodology." |
| Q112 | 10 | stated_limitations | "Inspired by previous work in scaffolding, we acknowledge our focus is on a subset of common teaching moves. However, this does not cover all the goals of human tutors, such as meta-cognitive support or building rapport with a student." |
| Q113 | 10 | stated_limitations | "Moreover, text tutoring limits teachers' use of additional instructional practices such as drawings." |
| Q114 | 10 | stated_limitations | "Finally, measuring a student's immediate success in solving a problem does not capture all the aspects of student learning. From a learning perspective, focusing on and measuring long-term learning is desired." |
| Q115 | 10 | authors_affiliations | "This project was made possible by an ETH AI Center Doctoral Fellowship to Jakub Macina with further support from the Asuera Stiftung and the ETH Zurich Foundation. Nico Daheim has received funding by the German Federal Ministry of Education and Research and the Hessian Ministry of Higher Education, Research, Science and the Arts within their joint support of the National Research Center for Applied Cybersecurity ATHENE. Mrinmaya Sachan acknowledges support from the Swiss National Science Foundation (Project No. 197155), a Responsible AI grant by the Haslerstiftung; and an ETH Grant (ETH-19 21-1)." |
| Q116 | 14 | evaluation_metrics | "For NCTE, uptake is calculated on the teacher-student dialogue pairs while bigram entropy is calculated on all teacher utterances." |
| Q117 | 14 | evaluation_metrics | "For TalkMoves and TSCC, bigram entropy is calculated on all teacher utterances having more than three words, while uptake is calculated on teacher utterances immediately following student utterances if both have more than three words." |
| Q118 | 14 | data_sources | "While the problems in GSM8k are simple enough to be understood quickly by teachers, they remain challenging for students, who among others have to deal with equations or percentages." |
| Q119 | 14 | data_format | "We follow the GSM8k reasoning format and prompt ChatGPT (gpt-3.5-turbo) with a 2-shot prompt." |
| Q120 | 14 | data_format | "Given a prompt and a math word problem, we sample n reasoning paths ri solutions from the model." |
| Q121 | 14 | data_format | "We parse the first numerical answer ai after the model" |
| Q122 | 15 | data_format | "We use InstructGPT (text-davinci-003) with the following prompt using temperature sampling with T = 0.4 and no top-k truncation:" |
| Q123 | 15 | annotation_process | "To build a dataset that would reflect students of various backgrounds, we use numerous student names associated with their given pronouns." |
| Q124 | 15 | label_categories | "List of all student characteristics based on prior work studying misconceptions in learning algebra (Booth et al., 2017):" |
| Q125 | 15 | label_categories | "has a problem with understanding what steps or procedures are required to solve a problem." |
| Q126 | 15 | label_categories | "has a problem with understanding underlying ideas and principles and a recognition of when to apply them." |
| Q127 | 15 | label_categories | "struggle most with understanding what the problem is asking them to do." |
| Q128 | 15 | label_categories | "has difficulty determining which pieces of information are relevant and which are irrelevant to solving the problem." |
| Q129 | 15 | label_categories | "struggle to put the numbers in the correct order in the equation or determine the correct operation to use." |
| Q130 | 15 | label_categories | "struggle to recognize the problem type and therefore do not know what strategy to use to solve it." |
| Q131 | 16 | annotation_process | "We use Prolific for data collection and hire annotators with teaching experience." |
| Q132 | 16 | annotation_process | "To ensure the data quality we filter only annotators with 100% completion rate with more than 500 total submissions." |
| Q133 | 16 | annotation_process | "All the payments to the annotators exceeded the US federal minimum wage and the final batch of annotators were paid the equivalent of $12/hour." |
| Q134 | 16 | annotation_process | "Annotators were restricted to having a maximum of five conversations in one annotation session." |
| Q135 | 16 | annotation_process | "One conversation takes ca. 6 minutes." |
| Q136 | 16 | annotation_process | "Data collection took place over a period of 2 months." |
| Q137 | 16 | annotation_process | "For each annotator, we randomly assign a student and math word problem." |
| Q138 | 16 | annotation_process | "Teachers were instructed to first analyze the student homework solution and then start the conversation to scaffold student problem understanding." |
| Q139 | 16 | annotation_process | "Post-conversation questionnaire is filled out by teachers to rate the conversation and get feedback on the type of student error." |
| Q140 | 16 | label_categories | "The teacher marks the exact line of a first student error and categorizes the problem into the following categories: Reached correct solution but proceeded further, Extra quantity or Missing quantity, Unit conversion error, Calculation error easily solved by a calculator, Missing / Wrong factual knowledge, Misunderstanding of a question, None of the above." |
| Q141 | 16 | task_taxonomy | "The conversation ends when the student correctly solves the problem or if the total conversation time exceeds 10 minutes." |
| Q142 | 16 | annotation_process | "We let annotators read best practices on how to have a productive conversation with students and tested them on their understanding of our task afterwards." |
| Q143 | 16 | annotation_process | "We started the data annotation with all the annotators able to successfully pass the test." |
| Q144 | 16 | annotation_process | "Moreover, to improve the training phase we manually checked several conversations by each annotator in terms of the quality and usage of diverse scaffolding questions." |
| Q145 | 17 | annotation_process | "Teachers were instructed to have a one-on-one tutoring session with different 6th-grade students." |
| Q146 | 17 | data_sources | "They were told that students received a math word problem for homework and submitted their solutions beforehand." |
| Q147 | 17 | annotation_process | "In a tutoring conversation, teachers were asked to go through the student's solution and try to let the student understand using a series of sensemaking questions to support student reasoning and learning." |
| Q148 | 17 | annotation_process | "Specifically, they were instructed to not just correct student solutions by telling what's correct/incorrect, but to give students the opportunity to explore the problem with a focus on core aspects, such as their chosen strategy." |
| Q149 | 17 | annotation_process | "However, as the goal is to focus on conceptual errors, they were allowed to let students use calculators or correct their arithmetic mistakes." |
| Q150 | 17 | label_categories | "Table 2 refers to the details of teacher moves used during annotation." |
| Q151 | 17 | label_categories | "In summary, Focus comprises of all conversation elements that direct the student towards the solution without actually giving out any of the solution, while Probing attempts to develop reasoning skills and world knowledge relevant to the problem, but not necessarily specific to the given problem." |
| Q152 | 17 | label_categories | "Telling is giving out parts of the solution, either calculations or strategy or both." |
| Q153 | 17 | label_categories | "All other conversational elements, including trying to understand what the student has already tried, fall under Generic." |
| Q154 | 17 | label_categories | "Most importantly, scaffolding questions that are productive for long-term learning are Focus and Probing." |
| Q155 | 17 | label_categories | "On the other hand, Telling represents giving out the partial or full answer to the student and should be mostly used when a student is stuck." |
| Q156 | 17 | task_taxonomy | "Scaffolding (Reiser, 2004; Anghileri, 2006) assists students to succeed in tasks that would otherwise be complex and differentiates between guidance (e.g. decomposing problem, clarifying) from cognitive activation (e.g. causing cognitive conflicts, activating prior knowledge (Limón, 2001))." |
| Q157 | 18 | data_format | "As we are interested in real educational use cases for our tutoring system, we apply a safety filter to filter out conversations with any sensitive content." |
| Q158 | 18 | data_format | "In particular, we use the Perspective API to filter out conversations containing toxic content (<1%)." |
| Q159 | 18 | data_sources | "We initially explored two additional approaches of data collection: i) human-human conversations, and ii) synthetic generation by LLMs." |
| Q160 | 18 | data_sources | "The framework we used in the final data collection enables us to scalably create data since we are only reliant on one user who can quickly create entire conversations with the LLM, taking ca. 6 minutes per 7+ turn conversation." |
| Q161 | 18 | stated_limitations | "We found this more efficient and performant than both human-human conversations and synthetic data generation." |
| Q162 | 18 | stated_limitations | "Specifically, the human-to-human collection is too time-consuming (on average 15 minutes per conversation in our pilot experiments) and requires waiting times to synchronously connect participants, and synthetic generation has proven to be error-prone; for example, models fail to understand student solutions and themselves make arithmetic errors that are not expected from teachers." |
| Q163 | 18 | task_taxonomy | "The student model in all 3 cases is an InstructGPT model (text-davinci-003) as defined in Section C.1, with the student name fixed to "Kayla"." |
| Q164 | 18 | task_taxonomy | "The first utterance of the teacher is hardcoded to "Hi Kayla, could you walk me through your solution?"." |
| Q165 | 18 | evaluation_metrics | "For Flan-T5780M teacher model decoding, we used sampling without a beam search." |
| Q166 | 18 | label_categories | "The following dimensions were rated by annotators: Coherence - "The response naturally follows up on the previous utterance and context and has no logical conflicts with the context." Correctness - "The response is factually and mathematically correct and respects the learning concepts being taught." Equitable tutoring - "The response gives a learning opportunity for the student by providing space for reflection, explanation, pointing to follow-up challenge, or engaging the student in other ways."" |
| Q167 | 18 | evaluation_metrics | "We use a 3-point Likert scale ranging from 1 (poor) and 3 (very good) for coherence and equitable tutoring and a binary scale for correctness." |
| Q168 | 18 | task_taxonomy | "ChatGPT prompt is the same as in the interactive tutoring scenario (Section E) with an additional section containing student solution." |
| Q169 | 20 | stated_limitations | "In our initial pilot study we observed that synthetic data generation by InstructGPT strictly followed the same structure of only asking next-step questions (highlighted in yellow) and was prone to inconsistencies in factual correctness and order of steps (highlighted in red)." |

### Category Index
- **task_taxonomy**: Q3, Q9, Q17, Q18, Q19, Q35, Q36, Q37, Q38, Q39, Q40, Q41, Q42, Q73, Q74, Q75, Q76, Q77, Q80, Q81, Q82, Q104, Q141, Q156, Q163, Q164, Q168
- **data_sources**: Q1, Q2, Q10, Q11, Q12, Q16, Q22, Q28, Q29, Q32, Q45, Q53, Q103, Q107, Q118, Q146, Q159, Q160
- **data_format**: Q30, Q31, Q33, Q34, Q84, Q85, Q86, Q87, Q88, Q119, Q120, Q121, Q122, Q157, Q158
- **label_categories**: Q4, Q56, Q57, Q61, Q78, Q79, Q124, Q125, Q126, Q127, Q128, Q129, Q130, Q140, Q150, Q151, Q152, Q153, Q154, Q155, Q166
- **annotation_process**: Q23, Q24, Q25, Q26, Q27, Q48, Q55, Q58, Q60, Q62, Q63, Q68, Q69, Q71, Q99, Q100, Q123, Q131, Q132, Q133, Q134, Q135, Q136, Q137, Q138, Q139, Q142, Q143, Q144, Q145, Q147, Q148, Q149
- **evaluation_metrics**: Q5, Q43, Q44, Q46, Q47, Q49, Q50, Q51, Q52, Q64, Q65, Q66, Q67, Q83, Q89, Q90, Q93, Q94, Q95, Q96, Q97, Q98, Q101, Q102, Q105, Q116, Q117, Q165, Q167
- **stated_limitations**: Q6, Q13, Q14, Q15, Q20, Q21, Q54, Q59, Q70, Q72, Q91, Q92, Q106, Q108, Q109, Q110, Q111, Q112, Q113, Q114, Q161, Q162, Q169
- **authors_affiliations**: Q7, Q8, Q115
