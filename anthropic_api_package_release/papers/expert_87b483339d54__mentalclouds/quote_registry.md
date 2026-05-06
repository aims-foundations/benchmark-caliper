---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | task_taxonomy | "This study evaluates the effectiveness of state-of-the-art Large Language Models (LLMs) in selectively summarizing various components of therapy sessions through aspect-based summarization, aiming to benchmark their performance." |
| Q2 | 1 | data_sources | "We introduce MentalCLOUDS, a counseling-component guided summarization dataset." |
| Q3 | 1 | data_sources | "This benchmarking dataset consists of 191 counseling sessions with summaries focused on three distinct counseling components (aka counseling aspects)." |
| Q4 | 1 | task_taxonomy | "Additionally, we assess the capabilities of 11 state-of-the-art LLMs in addressing the task of component-guided summarization in counseling." |
| Q5 | 1 | evaluation_metrics | "The generated summaries are evaluated quantitatively using standard summarization metrics and verified qualitatively by mental health professionals." |
| Q6 | 1 | evaluation_metrics | "Our findings demonstrate the superior performance of task-specific LLMs such as MentalLlama, Mistral, and MentalBART in terms of standard quantitative metrics such as Rouge-1, Rouge-2, Rouge-L, and BERTScore across all aspects of counseling components." |
| Q7 | 1 | evaluation_metrics | "Further, expert evaluation reveals that Mistral supersedes both" |
| Q8 | 1 | authors_affiliations | "Prottay Kumar Adhikary, Aseem Srivastava, Shivani Kumar, Salam Michael Singh, Puneet Manuja, Jini K Gopinath, Vijay Krishnan, Swati Kedia, Koushik Sinha Deb, Tanmoy Chakraborty" |
| Q9 | 1 | authors_affiliations | "Department of Electrical Engineering, Indian Institute of Technology Delhi, India; Department of Computer Science & Engineering, Indraprastha Institute of Information Technology Delhi, India; YourDOST, Karnataka, India; Department of Psychiatry, All India Institute of Medical Sciences, Rishikesh, India; Department of Psychiatry, All India Institute of Medical Sciences, New Delhi, India; Yardi School of Artificial Intelligence, Indian Institute of Technology Delhi, India" |
| Q10 | 1 | stated_limitations | "However, existing approaches often overlook the nuanced intricacies inherent in counseling interactions." |
| Q11 | 6 | task_taxonomy | "To evaluate the performance of diverse summarization systems across various aspects of counseling interactions, we expand upon the MEMO dataset [37]." |
| Q12 | 6 | data_sources | "Comprising 11.5K utterances extracted from 191 counseling sessions involving therapists and patients, this dataset draws from publicly accessible platforms such as YouTube." |
| Q13 | 6 | data_sources | "Embracing a heterogeneous demographic spectrum with distinctive mental health concerns and diverse therapists, the dataset facilitates the formulation of a comprehensive and inclusive approach for researchers." |
| Q14 | 6 | data_format | "Utilizing pre-processed transcriptions derived from counseling videos, the constituent dialogues within the dataset exhibit a dyadic structure, exclusively featuring patients and therapists as interlocutors." |
| Q15 | 6 | label_categories | "Within each conversation, three pivotal counseling components (aspects) emerge – symptom and history exploration, patient discovery, and reflective utterances." |
| Q16 | 6 | task_taxonomy | "Our study aims to capture the essence of each aforementioned counseling component, embarking on the creation of three distinct summaries for a single dialogue — each tailored to a specific counseling component." |
| Q17 | 6 | annotation_process | "Expanding upon the MEMO dataset, we augment it with annotated dialogue summaries corresponding to the three identified" |
| Q18 | 9 | evaluation_metrics | "We undertake a comprehensive evaluation of the generated summaries across various architectures, employing a dual approach of quantitative and qualitative assessments." |
| Q19 | 9 | task_taxonomy | "This section reports the aspect-based (psychotherapy element-based) summarization results based on the automatic evaluation scores." |
| Q20 | 9 | evaluation_metrics | "Given the generative nature of the task, we employ standard summarization evaluation metrics such as Rouge-1 (R-1), Rouge-2 (R-2), Rouge-L (R-L), and BERTScore (BS) along with their corresponding Precision (P), Recall (R) and F1 scores." |
| Q21 | 9 | evaluation_metrics | "Since F1 accounts for Precision and Recall, we compare LLM's performance based on F1 unless stated otherwise." |
| Q22 | 9 | evaluation_metrics | "ROUGE (Recall-Oriented Understudy for Gisting Evaluation) [58] assesses the overlap of n-grams (sequences of n consecutive words) between the generated summary and reference summaries." |
| Q23 | 9 | evaluation_metrics | "This metric measures the number of overlapping units such as n-gram, word sequences, and word pairs between the generated summary evaluated against the gold summary typically created by humans." |
| Q24 | 9 | evaluation_metrics | "ROUGE-L takes into account the longest co-occurring n-gram between the candidate and the reference summaries." |
| Q25 | 10 | evaluation_metrics | "Notably, in the context of counseling summaries, which are inherently tied to a domain-specific conversation, we embark on a meticulous qualitative examination of the generated summaries for individual counseling components." |
| Q26 | 10 | task_taxonomy | "Table 2 reports the automatic evaluation scores of LLMs on the summarization task for the Symptom and History (SH) psychotherapy element." |
| Q27 | 10 | evaluation_metrics | "MentalLlama outperforms the other LLMs across all the automatic evaluation metrics." |
| Q28 | 10 | evaluation_metrics | "For the R-1 metric, it achieves an F1 score of 30.86, followed by MentalBART with an F1 score of 28.00." |
| Q29 | 10 | evaluation_metrics | "In terms of the R-2 metric, Mistral is comparable with MentalLlama with a difference of mere 0.90 F1 score." |
| Q30 | 10 | evaluation_metrics | "For R-L, Mistral is preceded by MentalLlama by a difference of 2.93 F1 score." |
| Q31 | 10 | task_taxonomy | "The experimental results presented in Table 3 focus on the summarization task for the Patient Discovery (PD) psychotherapy element." |
| Q32 | 10 | evaluation_metrics | "Considering the R-1 metric, MentalLlama demonstrates superior performance compared to other LLMs." |
| Q33 | 10 | evaluation_metrics | "MentalLlama shows a 30.95 F1 score, followed by MentalBART (29.94 F1 Score)." |
| Q34 | 10 | evaluation_metrics | "For the R-2 metric, GPT-J outperforms the other models, followed by MentalLlama." |
| Q35 | 10 | evaluation_metrics | "Additionally, in terms of the R-L metric, the top two highest F1 score models are MentalLlama and Mistral." |
| Q36 | 10 | evaluation_metrics | "MentalBART supersedes the other models with an F1 score of 88.61 w.r.t BS metric." |
| Q37 | 11 | evaluation_metrics | "and MentalBART, which were pre-trained on the mental domain data, show consistent superiority." |
| Q38 | 11 | evaluation_metrics | "Notably, the base Mistral model also performs comparable and sometimes better than the models trained on the mental health domain data." |
| Q39 | 11 | task_taxonomy | "Table 3. Results obtained on MentalCLOUDS for the summarization task on the Patient Discovery (PD) psychotherapy element." |
| Q40 | 11 | task_taxonomy | "Table 4. Results obtained on MentalCLOUDS for the summarization task on the Reflecting (RT) psychotherapy element." |
| Q41 | 12 | annotation_process | "In order to conduct a comprehensive expert assessment, five healthcare professionals were employed to assess the clinical appropriateness of the summaries produced by the LLMs based on the evaluation framework of Sekhon et al. [39]." |
| Q42 | 12 | annotation_process | "Among them were two clinical psychologists, with the remaining three comprising psychiatrists and medical practitioners." |
| Q43 | 12 | annotation_process | "Of the group, four were male, and one was female, with ages ranging from 40 to 55 years and possessing over a decade of therapeutic experience." |
| Q44 | 12 | evaluation_metrics | "The evaluation framework encompasses six crucial parameters — affective attitude, burden, ethicality, coherence, opportunity costs, and perceived effectiveness." |
| Q45 | 12 | evaluation_metrics | "Experts evaluate each summary against these acceptability parameters, assigning continuous ratings on a scale from 0 to 2, where a higher rating signifies enhanced acceptability." |
| Q46 | 12 | evaluation_metrics | "Additionally, we incorporate a new parameter – the extent of hallucination. It is categorical – 0 (too much hallucinated), 1 (hallucination barely observed), and 2 (no hallucination observed)." |
| Q47 | 13 | annotation_process | "Table 6 reports the clinical experts' scores averaged over the ratings given by five experts." |
| Q48 | 13 | label_categories | "The clinical acceptability framework [39] involves six parameters – affective attitude, burden, ethicality, coherence, opportunity costs, and perceived effectiveness (c.f. Table 5 for more details)." |
| Q49 | 13 | evaluation_metrics | "We select the three best LLMs (MentalLlama, Mistral and MentalBART) for the expert evaluation based on the automatic result." |
| Q50 | 13 | annotation_process | "Overall, all the raters were more aligned in rating the MentalBART model with lesser variance as compared to the other two LLMs for all the metrics." |
| Q51 | 14 | stated_limitations | "As all three models have poor scores on the more sensitive aspects i.e. the overall efficacy and the opportunity cost, this indicates that these models share the same weakness and are not suitable for clinical use as they stand now." |
| Q52 | 14 | annotation_process | "Table 7. Hallucination frequency marked by experts for the top three LLMs. Here the average of hallucination frequencies for each rater are reported." |
| Q53 | 14 | label_categories | "Additionally, the evaluation of hallucination identification is divided into three categories: no hallucination observed, hallucination barely observed, and too much hallucinated in a set of 39 conversations." |
| Q54 | 14 | label_categories | "These categories essentially determine how well the response is consistent with the context and whether it is also incorrect, nonsensical, or contains global information beyond the scope of the conversation." |
| Q55 | 14 | evaluation_metrics | "Out of the 39 test conversations, the majority of cases on average demonstrate no hallucination, with Mistral and MentalBART achieving 75.13% and 76.15% each, while MentalLlama shows a slightly higher value of 77.69%." |
| Q56 | 14 | annotation_process | "Table 7 presents the total numbers for each model and hallucination category as assessed by five individual raters." |
| Q57 | 14 | stated_limitations | "The data shows fluctuations in how hallucinations are perceived among different models and stresses the importance of reviewing evaluations from numerous appraisers for a complete assessment." |
| Q58 | 15 | task_taxonomy | "In this work, we assessed the state-of-the-art LLMs on the aspect-based summarization task of mental health therapy conversations." |
| Q59 | 15 | evaluation_metrics | "Specifically, we benchmarked 11 LLMs for aspect-based summarization and evaluated them using both automatic and human evaluation approaches." |
| Q60 | 15 | data_sources | "The counseling dataset was curated from multiple multimedia online sources such as youtube transcripts [37]." |
| Q61 | 15 | data_format | "Hence, most of these natural conversations are incoherent and grammatically unfluent." |
| Q62 | 15 | stated_limitations | "However, the models did not do as well with the structure separation of the information. The sections of "symptoms and history", "patient discovery", and "reflection" frequently overlap, posing clinical and legal problems." |
| Q63 | 15 | stated_limitations | "The models are also unable to identify psychotherapy types (e.g., cognitive behavior therapy) and therapy techniques, which form an integral part of counseling notes." |
| Q64 | 15 | stated_limitations | "Important negative histories gathered during the session, such as the history of suicide risk or substance use were also not recorded, and in at least one instance, the presence of suicide risk was not identified." |
| Q65 | 15 | stated_limitations | "In general, the models exhibited stronger performance in handling medical histories and examinations but struggled when faced with more technical and sensitive aspects, such as conversations related to actual therapeutic strategies." |
| Q66 | 16 | stated_limitations | "First, this work aims to benchmark the efficacy of only 11 LLMs on the aspect-based summarization task." |
| Q67 | 16 | stated_limitations | "Second, for faster and easier reproduction, we did not assess models larger than 7 billion parameters; however, such models can be part of future examinations." |
| Q68 | 16 | stated_limitations | "Third, for the initial study and to promote research in this field, only open-source models were assessed in this work." |
| Q69 | 16 | stated_limitations | "Finally, this work explored only three aspects (counseling component) of the conversation." |
| Q70 | 16 | stated_limitations | "Additionally, the counseling sessions in this work represented a certain demographic region (American) and thus may not apply to therapy counseling for other demographics." |
| Q71 | 16 | task_taxonomy | "Our study benchmarked the efficacy and role of large language models towards component-guided counseling summarization tasks." |
| Q72 | 16 | data_sources | "In doing so, we introduced a new dataset, MentalCLOUDS, which comprises summaries corresponding to three counseling components." |
| Q73 | 16 | data_sources | "The dataset will be available upon request." |

### Category Index
- **task_taxonomy**: Q1, Q4, Q11, Q16, Q19, Q26, Q31, Q39, Q40, Q58, Q71
- **data_sources**: Q2, Q3, Q12, Q13, Q60, Q72, Q73
- **data_format**: Q14, Q61
- **label_categories**: Q15, Q48, Q53, Q54
- **annotation_process**: Q17, Q41, Q42, Q43, Q47, Q50, Q52, Q56
- **evaluation_metrics**: Q5, Q6, Q7, Q18, Q20, Q21, Q22, Q23, Q24, Q25, Q27, Q28, Q29, Q30, Q32, Q33, Q34, Q35, Q36, Q37, Q38, Q44, Q45, Q46, Q49, Q55, Q59
- **stated_limitations**: Q10, Q51, Q57, Q62, Q63, Q64, Q65, Q66, Q67, Q68, Q69, Q70
- **authors_affiliations**: Q8, Q9
