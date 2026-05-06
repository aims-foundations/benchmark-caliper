```markdown
# Validity Extraction: MentalCLOUDS: Benchmarking LLMs on Counseling-Component Guided Summarization
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: MentalCLOUDS: Benchmarking LLMs on Counseling-Component Guided Summarization
- **Authors**: Prottay Kumar Adhikary, Aseem Srivastava, Shivani Kumar, Salam Michael Singh, Puneet Manuja, Jini K Gopinath, Vijay Krishnan, Swati Kedia, Koushik Sinha Deb, Tanmoy Chakraborty
- **Venue/Year**: Not explicitly stated in registry (inferred as 2024 from content)
- **Total Pages**: 16
- **Quotes Extracted**: 73

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

### 1. Task Taxonomy / Test Case Categories

The benchmark is organized around aspect-based summarization of therapy sessions, specifically targeting three counseling components: symptom and history exploration, patient discovery, and reflective utterances [Q15, Q16]. The primary evaluation task is component-guided summarization, in which a single counseling dialogue yields three distinct summaries, one for each psychotherapy element [Q16], with results reported separately for the Symptom and History (SH) element [Q26], the Patient Discovery (PD) element [Q31, Q39], and the Reflecting (RT) element [Q40]. Eleven state-of-the-art LLMs are benchmarked against this task [Q4, Q59], and the study explicitly frames itself as measuring models' ability to capture "the essence of each aforementioned counseling component" [Q16]. From a deployment-validity standpoint, this three-component taxonomy is CBT-aligned and reflects a clinical framework developed without documented attention to MENA-specific distress framings (e.g., religious or fatalistic attributions) or South Asian family-dynamic constructs such as izzat — a gap the authors themselves acknowledge in passing [Q69, Q70]. For South Asian and MENA users, the absence of components covering shame-based help-seeking, intergenerational conflict, or religiously framed coping represents a meaningful divergence between what the benchmark tests and what a regionally appropriate summarization system would need to capture.

### 2. Data Sources and Collection

The MentalCLOUDS dataset is introduced as a new counseling-component guided summarization resource comprising 191 counseling sessions [Q2, Q3] built by expanding the existing MEMO dataset [Q11]. The 11,500 utterances were drawn from publicly accessible platforms such as YouTube [Q12, Q60], which introduces a specific demographic profile: the sessions reflect a "heterogeneous demographic spectrum with distinctive mental health concerns and diverse therapists" [Q13], but the paper later clarifies that the counseling sessions "represented a certain demographic region (American)" [Q70] — meaning the source data is primarily US-sourced English-language clinical content, not Indian or MENA content. For South Asian and MENA researchers using this benchmark to evaluate real-world tools, this is a critical input-validity concern: the training signal and reference summaries embedded in the dataset derive from American therapeutic communication norms rather than those of India, Pakistan, or any MENA country. The dataset will be made available upon request [Q73], which limits immediate independent replication of demographic assessments.

### 3. Data Format and Preprocessing

The input data consists of pre-processed transcriptions of counseling videos structured as dyadic dialogues featuring only patients and therapists as interlocutors [Q14]. The paper notes that these natural conversations are often "incoherent and grammatically unfluent" [Q61], reflecting the spontaneous spoken-language origin of the transcripts. Both the benchmark and its intended deployment are text-only in the core evaluation pipeline, which means no modality mismatch exists for English-system users [Q14]; however, the English-only transcription format is a structural barrier for researchers building or evaluating systems in Arabic, Hindi, Urdu, or Farsi, as the input format provides no multilingual signal whatsoever.

### 4. Label Categories and Output Types

The benchmark defines three counseling aspects as label categories for the summarization task: symptom and history exploration, patient discovery, and reflective utterances [Q15]. For qualitative expert evaluation, the output label framework is expanded to six clinical acceptability parameters — affective attitude, burden, ethicality, coherence, opportunity costs, and perceived effectiveness [Q48] — drawn from an established clinical acceptability framework [Q39 as cited in Q41]. A seventh parameter, hallucination, is added as a categorical label with three levels: no hallucination observed, hallucination barely observed, and too much hallucinated [Q53], where hallucination is defined as output inconsistent with the conversation context or containing globally incorrect or nonsensical content [Q54]. From an output-ontology validity perspective (HIGH priority), these label categories were constructed within a CBT-aligned, India/US professional frame without documented adaptation for MENA clinical norms; what counts as "clinically appropriate" or "perceived effectiveness" in a summary may differ meaningfully for practitioners who integrate religious frameworks or shame-based conceptualizations of mental distress into their clinical reasoning — a divergence the current label set does not capture.

### 5. Annotation Process

The dataset's ground-truth summaries were created by augmenting the MEMO dataset with annotated dialogue summaries corresponding to the three identified counseling components [Q17], though the paper provides limited detail on the specific annotators involved in this initial labeling step — a gap relevant to assessing whether Indian or MENA professional perspectives were represented. For the qualitative expert evaluation, five healthcare professionals were employed to assess clinical appropriateness of LLM-generated summaries [Q41]: two clinical psychologists and three psychiatrists or medical practitioners [Q42], all with over a decade of therapeutic experience, four male and one female, ages 40–55 [Q43]. Ratings were averaged across the five experts [Q47], and inter-rater variance analysis revealed that all raters were more aligned in rating MentalBART than the other two LLMs [Q50]. Hallucination frequencies were also assessed by the same five raters across 39 test conversations [Q52, Q56]. Critically for MENA deployment validity, the expert pool is described as India/US-trained without any documented MENA representation, meaning the professional consensus embedded in the ground-truth labels reflects a particular clinical tradition that may not generalize to practitioners in Saudi Arabia, Egypt, or Iran.

### 6. Evaluation Metrics and Output Modality

The evaluation combines automatic quantitative metrics with qualitative expert review [Q5, Q18]. Automatic metrics include Rouge-1, Rouge-2, Rouge-L, and BERTScore, each reported with Precision, Recall, and F1, with F1 used as the primary comparison basis [Q20, Q21]. ROUGE metrics assess n-gram overlap between generated and reference summaries [Q22, Q23], with ROUGE-L capturing the longest co-occurring n-gram [Q24]; BERTScore provides a semantic similarity dimension beyond surface overlap [Q6]. Empirical results show MentalLlama, Mistral, and MentalBART consistently outperforming other models across automatic metrics [Q6, Q27, Q28, Q29, Q30, Q32, Q33, Q34, Q35, Q36, Q37, Q38], with Mistral performing comparably to domain-specific models despite not being pre-trained on mental health data [Q38]. Expert evaluation uses the six-parameter clinical acceptability framework supplemented by the hallucination scale [Q44, Q45, Q46], with Mistral emerging as the top performer in qualitative review [Q7, Q49]. Hallucination rates are notably low across all three top models, with MentalLlama achieving 77.69% "no hallucination" cases [Q55]. For the HIGH-priority output-form validity concern: ROUGE and BERTScore operate on surface-level text overlap against English reference summaries [Q22, Q23], making them entirely non-transferable as evaluation signals for systems generating summaries in Arabic, Hindi, Urdu, or Farsi — users building multilingual counseling tools gain no valid evaluation signal from this metric framework without separate target-language reference summaries that the benchmark does not provide.

### 7. Stated Limitations

The authors acknowledge several limitations with direct relevance to deployment validity. Most critically for the target user base, they explicitly state that "the counseling sessions in this work represented a certain demographic region (American) and thus may not apply to therapy counseling for other demographics" [Q70] — a direct acknowledgment that the benchmark's geographic scope excludes the South Asian and MENA contexts of primary concern to the target users described in the elicitation summary. The paper also notes that models struggled with structurally and clinically sensitive aspects: the sections of "symptoms and history," "patient discovery," and "reflection" frequently overlap, posing "clinical and legal problems" [Q62]; models failed to identify psychotherapy types such as cognitive behavior therapy and specific therapy techniques [Q63]; and crucially, important negative histories including suicide risk and substance use were not reliably recorded, with at least one instance of missed suicide risk [Q64]. These gaps have heightened significance in MENA and South Asian deployment contexts where stigma and legal-professional norms around suicide documentation differ substantially from US clinical practice. Models showed stronger performance on medical histories than on "more technical and sensitive aspects, such as conversations related to actual therapeutic strategies" [Q65], and all three top models received poor scores on overall efficacy and opportunity cost, with the authors concluding they are "not suitable for clinical use as they stand now" [Q51]. Additional scope limitations include the restriction to 11 LLMs [Q66], the exclusion of models larger than 7 billion parameters [Q67], the focus on open-source models only [Q68], coverage of only three counseling aspects [Q69], and noted fluctuations in hallucination perception across raters [Q57]. The paper's initial framing also flags that existing summarization approaches "often overlook the nuanced intricacies inherent in counseling interactions" [Q10], a concern that remains unresolved by the benchmark's own design.

### 8. Authors and Affiliations

The paper's ten authors [Q8] are affiliated with institutions spanning Indian academia, Indian industry, and Indian clinical medicine [Q9]: the Indian Institute of Technology Delhi (Electrical Engineering and Yardi School of Artificial Intelligence), the Indraprastha Institute of Information Technology Delhi (Computer Science and Engineering), YourDOST (a Karnataka-based digital mental health platform), and two departments of Psychiatry at All India Institute of Medical Sciences campuses in Rishikesh and New Delhi. The uniformly Indian institutional base — with no co-authors from MENA institutions or MENA mental health systems — directly contextualizes the benchmark's design choices: the counseling components, clinical acceptability framework, and expert validation pool all reflect a professional environment shaped by Indian academic and clinical norms, with no documented input from Arabic-speaking, Farsi-speaking, or MENA-based clinical practitioners. For South Asian users, the IIT Delhi and AIIMS affiliations represent high-credibility domestic institutions, but the absence of any multilingual NLP expertise in the author list is consistent with the benchmark's English-only evaluation design.
```

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
