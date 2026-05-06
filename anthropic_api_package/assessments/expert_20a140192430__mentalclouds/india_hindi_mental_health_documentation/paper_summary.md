```markdown
# Validity Extraction: MentalCLOUDS — A Counseling-Component Guided Summarization Dataset for Benchmarking LLMs in Mental Health Therapy Sessions

<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: MentalCLOUDS — A Counseling-Component Guided Summarization Dataset for Benchmarking LLMs in Mental Health Therapy Sessions
- **Authors**: Prottay Kumar Adhikary, Aseem Srivastava, Shivani Kumar, Salam Michael Singh, Puneet Manuja, Jini K Gopinath, Vijay Krishnan, Swati Kedia, Koushik Sinha Deb, Tanmoy Chakraborty
- **Venue/Year**: Not explicitly stated in registry (inferred from content as ~2024)
- **Total Pages**: 16
- **Quotes Extracted**: 73

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

---

### 1. Task Taxonomy / Test Case Categories

The benchmark defines its core task as aspect-based summarization of therapy session transcripts, specifically aiming to assess whether LLMs can selectively capture distinct therapeutic components rather than producing holistic session summaries [Q1]. The benchmark evaluates 11 state-of-the-art LLMs on this component-guided summarization task [Q4], generating three distinct summaries per counseling dialogue — one for each counseling component — from a single conversation [Q16]. The three psychotherapy elements are: symptom and history exploration, patient discovery, and reflective utterances [Q15], with results reported separately for each component [Q26, Q31, Q39, Q40]. The taxonomy is explicitly framed as psychotherapy element-based rather than generically topic-based, grounding it in clinical structure [Q19, Q58, Q71].

From a deployment-validity perspective (IO dimension, HIGH priority), this three-component taxonomy represents a significant structural constraint: it omits elements that practitioners in India and the broader Global South routinely require in complete clinical notes. The authors themselves acknowledge that the models cannot identify psychotherapy types or therapy techniques [Q63], and that important negative histories such as suicide risk or substance use were not recorded [Q64] — confirming that risk-flag documentation and safety content fall outside the benchmark's summarization targets. The benchmark also does not appear to include family intervention suggestions or spiritual/religious coping strategies as distinct summarization aspects, which are clinically salient components for South Asian practitioners in particular [Q10, Q69]. The limitation that only three counseling aspects were explored is openly acknowledged [Q69], but this acknowledgment does not resolve the deployment gap — it confirms that the benchmark's input ontology is structurally incomplete relative to what the deployment population requires.

---

### 2. Data Sources and Collection

MentalCLOUDS is introduced as a new dataset built by expanding the previously published MEMO dataset [Q2, Q11], comprising 191 counseling sessions with component-specific summaries across three therapeutic aspects [Q3]. The underlying session transcripts — totalling 11.5K utterances — were sourced from publicly accessible online platforms, specifically YouTube [Q12, Q60], and the dataset will be made available upon request [Q73]. The dataset is described as drawing from a heterogeneous demographic spectrum with diverse mental health concerns and diverse therapists [Q13], though the paper later clarifies that these counseling sessions represented a specifically American demographic region [Q70].

From an IC (HIGH priority) and IO (HIGH priority) standpoint, the American origin of the source sessions is a critical validity concern for the target deployment in India and the Global South. Cultural disclosure patterns in American online counseling recordings are unlikely to reflect somatization, family-system framing, stigma-shaped disclosure, or caste/religion-inflected stressors characteristic of South Asian clinical presentations. The claim of demographic heterogeneity [Q13] may refer to diversity within the American context rather than cross-cultural diversity relevant to the deployment population. The YouTube sourcing also raises an ecological validity concern: these are mock or publicly posted counseling exchanges in standard English [Q14], not naturalistic clinical sessions, which may produce scripted interaction patterns that differ from real-world therapeutic dialogue the deployment system will process.

---

### 3. Data Format and Preprocessing

The input data consists of pre-processed transcriptions derived from counseling videos, structured as dyadic dialogues featuring only patients and therapists as interlocutors [Q14]. The paper acknowledges that because the source material consists of natural conversations pulled from online multimedia, most of these dialogues are incoherent and grammatically unfluent [Q61], indicating that the transcripts are not polished or cleaned to a high standard.

This format — English-only text transcripts with dyadic structure — aligns well with the deployment system's text-in/text-out configuration (IF dimension, LOWER priority). The user confirmed that code-switching is absent from this dataset, consistent with the benchmark's standard-English online sourcing [Q12], and no audio, image, or non-Latin script modalities are involved. The grammatical disfluency noted in [Q61] is a realistic property of transcribed speech and does not introduce a modality mismatch, though it may affect LLM summarization quality in ways the benchmark's reference summaries may not fully account for.

---

### 4. Label Categories and Output Types

The output label structure is organized around three counseling components: symptom and history exploration, patient discovery, and reflective utterances [Q15], each receiving its own reference summary against which model outputs are evaluated. For the qualitative evaluation layer, the benchmark employs a clinical acceptability framework with six parameters — affective attitude, burden, ethicality, coherence, opportunity costs, and perceived effectiveness [Q48] — supplemented by a hallucination identification dimension with three categorical levels: no hallucination observed, hallucination barely observed, and too much hallucinated [Q53]. Hallucination is defined in terms of consistency with conversational context and the absence of nonsensical or globally extraneous content [Q54].

From an OO (HIGH priority) perspective, the three-component output ontology is a significant gap relative to the deployment's requirements. The benchmark's label space does not include family-intervention notes, risk-flag documentation (e.g., suicidal ideation), or spiritual/religious coping elements — all of which are clinically required outputs in South Asian counseling practice. A deployment system scored against this benchmark would receive no credit or penalty for how well it handles these absent categories, meaning the benchmark's output ontology systematically fails to capture whether the system produces complete clinical notes for the target practitioner population.

---

### 5. Annotation Process

The dataset annotations — specifically the component-guided reference summaries — were created by expanding the existing MEMO dataset with annotated dialogue summaries for the three identified counseling components [Q17], though the paper does not provide detailed information about who produced these reference summaries, their credentials, or their inter-annotator agreement at the data-creation stage. For the qualitative expert evaluation layer, five healthcare professionals were employed to rate LLM-generated summaries using the Sekhon et al. clinical acceptability framework [Q41], comprising two clinical psychologists and three psychiatrists/medical practitioners [Q42]. The expert group was predominantly male (four of five), aged 40–55, and all possessed over a decade of therapeutic experience [Q43], with ratings averaged across the five experts [Q47] and hallucination frequencies also reported per rater [Q52, Q56]. Inter-rater alignment was highest for the MentalBART model, which showed lesser variance across raters compared to MentalLlama and Mistral [Q50].

From an OC (MODERATE priority) perspective, the expert evaluators' demographic and institutional context matters for deployment validity. The paper affiliates the team with Indian institutions [Q9], suggesting the validating clinicians are likely Indian-trained practitioners — which represents partial alignment with the deployment population. However, the five evaluators are senior psychiatrists and psychologists, not peer-support practitioners or counselors working in community mental health settings, which may mean their quality judgments reflect a more formal clinical standard than the benchmark's intended OMHC deployment context would require. The paper does not indicate whether evaluators used CBT-specific rubrics, family-systems considerations, or cultural adaptation criteria in their assessments, leaving open the question of whether their acceptability judgments would align with practitioners who blend Western and South Asian clinical modalities.

---

### 6. Evaluation Metrics and Output Modality

The benchmark uses a dual quantitative-qualitative evaluation approach [Q5, Q18]. Quantitatively, model outputs are scored using ROUGE-1, ROUGE-2, ROUGE-L (measuring n-gram and longest-common-subsequence overlap between generated and reference summaries [Q22, Q23, Q24]), and BERTScore, all reported as F1 unless otherwise specified [Q20, Q21]. For the qualitative layer, the three best-performing LLMs — MentalLlama, Mistral, and MentalBART — were selected based on automatic scores and submitted to expert evaluation [Q49] across six clinical acceptability parameters rated on a 0–2 continuous scale [Q44, Q45], plus the categorical hallucination dimension [Q46]. MentalLlama and MentalBART (both domain-specific) showed generally superior quantitative performance [Q6, Q37], while Mistral — a general-purpose model — was competitive and sometimes exceeded the domain-specific models [Q38]; expert evaluation further revealed Mistral's relative strengths [Q7]. Hallucination rates were low across the top three models, with no-hallucination rates of approximately 75–78% [Q55], and the counseling-domain sensitivity of summaries motivated the domain-specific qualitative evaluation layer [Q25].

The output modality is text-based structured summaries throughout, matching the deployment system's target output format. The F1-based ROUGE scoring framework [Q21] is standard but known to reward lexical overlap rather than clinical completeness — a concern when the deployment requires capturing safety-critical content (e.g., suicide risk flags) that may be present in only a small portion of a session and thus contribute minimally to aggregate ROUGE scores regardless of clinical importance [Q59].

---

### 7. Stated Limitations

The authors explicitly acknowledge several limitations with direct relevance to the deployment context. Most critically for clinical use, the models performed poorly on the more sensitive aspects of overall efficacy and opportunity cost, leading the authors to conclude that these models are not suitable for clinical use as they currently stand [Q51]. The models were unable to identify psychotherapy types and therapy techniques [Q63], failed to capture important negative histories including suicide risk and substance use [Q64], and generally struggled with technical and sensitive therapeutic strategy content while performing better on medical history elements [Q65]. The structure separation problem is also flagged: the three counseling components frequently overlap, creating clinical and legal problems in practice [Q62]. The authors also note that hallucination perceptions fluctuate across raters, underscoring the importance of multi-appraiser review [Q57].

Methodologically, the benchmark scope is limited to 11 LLMs, all open-source and capped at 7 billion parameters for reproducibility [Q66, Q67, Q68], and only three counseling aspects were explored [Q69]. The most significant limitation from a deployment-validity perspective is explicitly stated: the counseling sessions represent an American demographic and may not apply to therapy counseling for other demographics [Q70]. This directly confirms the benchmark's cultural misalignment with the India-and-Global-South deployment target. The existing approaches' tendency to overlook the nuanced intricacies of counseling interactions [Q10] thus extends not only to model capability but to the benchmark design itself.

---

### 8. Authors and Affiliations

The paper's authorship team [Q8] spans multiple prominent Indian research institutions, including the Department of Electrical Engineering at IIT Delhi, the Department of Computer Science & Engineering at IIIT Delhi, the Yardi School of Artificial Intelligence at IIT Delhi, and the Department of Psychiatry at AIIMS Rishikesh and AIIMS New Delhi [Q9]. The team also includes an affiliation with YourDOST, a Karnataka-based online mental health platform [Q9], which signals direct engagement with Indian digital mental health service delivery and lends practical grounding to the deployment context. This institutional composition — combining top Indian engineering schools with Indian psychiatric institutions and an Indian OMHC platform — suggests the benchmark was designed with the Indian deployment context in mind, though the underlying session data remains American in origin [Q70], creating a notable tension between the authorship's regional expertise and the data's cultural provenance.
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
