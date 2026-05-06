```markdown
# Validity Extraction: MILU: A Multi-task Indic Language Understanding Benchmark
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: MILU: A Multi-task Indic Language Understanding Benchmark
- **Authors**: Sshubam Verma, Mohammed Safi Ur Rahman Khan, Vishwajeet Kumar, Rudra Murthy, Jaydeep Sen (and others cited in acknowledgements and references)
- **Venue/Year**: Not explicitly stated in registry (preprint/conference paper, circa 2024 based on citations)
- **Total Pages**: 57 (based on highest page number in registry)
- **Quotes Extracted**: 132

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

### 1. Task Taxonomy / Test Case Categories

MILU is a multiple-choice question (MCQ) benchmark spanning 8 domains and 41 subjects across 11 Indic languages [Q1], with domains including Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies [Q42]. All test cases are multiple-choice questions, consistent with the deployment context's strict MCQ requirement [Q22]. The benchmark is described as "comprehensive" and India-centric in design [Q74], and the subject-level breakdown across languages is detailed in supplementary tables [Q98]. From a deployment-validity standpoint, the MCQ format is well-matched to the target teacher's scoring workflow; however, the 41 subjects are drawn from competitive exam content [Q23], which may not fully mirror the curricular framing used in Hindi state-board (UP, MP, Rajasthan, Bihar) or CBSE school contexts — particularly for Arts & Humanities items that could differ between UPSC-style general knowledge and school-literature registers. The evaluation of Indic language-specific fine-tuned LLMs is also covered as a distinct category [Q60], underscoring that the benchmark was designed with Indic-language model capabilities in mind, not just pan-India English-dominant models.

### 2. Data Sources and Collection

MILU's questions were sourced from over 1,500 competitive exams in India [Q13], scraped from online exam portals that host previously released question papers [Q25], and encompass more than 40 exam types at national and state levels [Q27, Q92]. The benchmark explicitly incorporates state- and region-level exams to capture local knowledge in each respective language [Q14, Q28], with detailed listings of national-level, government/private-organization, and state-level civil service exams provided in supplementary tables [Q95, Q96, Q97]. A separate validation set of approximately 9,000 questions is maintained for few-shot evaluation [Q51], and all scraped data derives from publicly available resources [Q88], to be released under permissible licenses [Q89, Q90]. For the Hindi deployment context, the critical validity question is whether MILU's Hindi-language items are drawn proportionally from the major Hindi-belt states (UP, MP, Rajasthan, Bihar) or whether certain states dominate — the paper does not break down exam-source distribution by state for individual languages [Q97], which is a flagged gap. English questions are also included because they often address India-specific cultural content absent from other benchmarks [Q30], and approximately 25% of total questions were translated from English [Q47], introducing a secondary concern about whether translated content aligns with North Indian Hindi-board norms and subject-specific terminology. The total released dataset comprises approximately 79,000 questions capped at 500 per subject-language pair [Q46].

### 3. Data Format and Preprocessing

All questions in MILU are text-only, multiple-choice format with up to four answer options; reading-comprehension-style questions, image-based questions, and items with more than four options were explicitly excluded to ensure uniformity [Q33]. This text-only, single-correct-answer MCQ structure is fully aligned with the deployment's format requirements (Devanagari-script Hindi text, binary scoring). Language verification was performed using INDICLID and Unicode-based filtering to ensure questions are in the correct language [Q34], and duplicate removal was applied to retain only unique items [Q35]. Approximately 45% of questions were already labeled with a topic name; the remaining untagged questions were translated into English via INDICTRANS2 and then labeled using GPT-4O-MINI [Q37, Q38], with tags subsequently embedded and clustered into 50 groups before manual assignment of subject labels [Q40, Q41]. For subjects with fewer than 100 questions in a given language, questions were sampled from the English set and translated using GPT-4O (preferred over specialized translation models for task-awareness) [Q44, Q45], a step that carries surface-level validity risk for Hindi items where subject-specific terminology must match North Indian academic norms. Manual review was applied both initially and as a final quality check on samples from each language [Q32, Q36], and a detailed distribution analysis is available in supplementary tables [Q93].

### 4. Label Categories and Output Types

Ground-truth labels in MILU are single correct answers for each MCQ, drawn from exam answer keys [Q12]. After the clustering and merging process, 41 distinct subject names were determined, organized into 8 domains [Q42]. The raw tag space was large and fine-grained — approximately 20,000 tags with significant overlap — before consolidation [Q39]. For the deployment context, the label schema is straightforwardly binary (correct/incorrect), consistent with the teacher's positive/negative marking scheme; no graded or rubric-based output labels are involved, and the benchmark's answer-key-based ground truth aligns with what North Indian educators would recognize as standard exam scoring.

### 5. Annotation Process

The primary annotation pipeline relied on online exam portals where questions were manually tagged with topic names and language details by portal staff, with subject experts ensuring answer accuracy [Q26]. Additional manual annotation was performed by AI4Bharat team volunteers who conducted manual audits of the collected data [Q87], and cluster-to-subject label assignment was also done manually [Q41]. NOT DOCUMENTED: the paper does not provide demographic details about annotators (regional background, language proficiency level, subject expertise domain), nor does it report inter-annotator agreement statistics. This absence is a moderate validity-relevant finding for the deployment context: if annotators were not drawn from Hindi-medium North Indian educational backgrounds, subtle misalignments in answer keys for culturally or regionally specific items (e.g., local history, Hindi literature) could remain undetected.

### 6. Evaluation Metrics and Output Modality

MILU evaluates models using accuracy as the primary metric, reported across domains and languages, with 42–45 LLMs assessed in the benchmark [Q48, Q75]. For non-API models, the log-likelihood method is used: the answer string with the highest conditional log probability given the question is selected [Q53, Q54, Q55], implemented via LM-EVALUATION-HARNESS for reproducibility [Q52]. API-based models are evaluated generatively in zero-shot setup only (due to cost constraints), with structured JSON output prompting to simplify parsing [Q56, Q57, Q58]. Results are reported at 0-shot, 1-shot, and 5-shot levels for most open models [Q50, Q100], with 5-shot accuracy generally reported as the headline figure [Q59]. The benchmark finds that GPT-4o achieves the highest average accuracy at 74% [Q3, Q16], while language-specific fine-tuned Indic models perform only marginally above random baselines [Q4, Q17, Q61], and performance is consistently weaker in culturally relevant domains such as Arts & Humanities and Law & Governance compared to STEM [Q20, Q62, Q71]. The extensive per-model, per-subject, per-language result tables [Q99–Q132] provide granular evidence for assessing Hindi-specific performance, though the paper does not isolate Hindi-only performance summaries in the main text. The authors also note that the log-likelihood evaluation method may yield different results compared to generation-based or chain-of-thought approaches [Q85], which is relevant if the deployment uses generative rather than discriminative model inference.

### 7. Stated Limitations

The authors identify several limitations directly relevant to the Hindi deployment context. The benchmark is restricted to 11 languages due to a lack of questions in lower-resource languages [Q82], and Hindi as a high-resource language benefits from relatively more data — but the paper acknowledges that models perform better in high-resource languages than low-resource ones [Q5, Q76], a finding that works in Hindi's favour without guaranteeing adequate coverage of state-board-specific content. The scarcity of questions in some subject-language pairs necessitated translation of a portion of the dataset [Q84], which is a concrete concern for Hindi items where translated English-board content may not match North Indian academic register or terminology norms. Domain-wise analysis confirms that models perform poorly in Arts & Humanities and Law & Governance — precisely the domains most relevant to culturally loaded Hindi-board content such as literature, regional history, and civics [Q6, Q77] — and the authors attribute this to insufficient culturally specific data in training corpora [Q72]. Additional limitations include: limited computational resources preventing thorough evaluation of larger models [Q83]; inconclusive effects of few-shot prompting on instruct models [Q65, Q66]; limited performance gains from language-specific fine-tuning, possibly due to small datasets and LoRA-based parameter-efficient methods [Q78, Q79, Q80]; and the reliance on log-likelihood evaluation rather than generation-based or CoT methods [Q85]. The authors also acknowledge that some topics in certain languages had fewer than 100 questions and required augmentation [Q43], and that further investigation is needed to fully understand these gaps [Q81]. All artifacts and code will be released publicly [Q8, Q21].

### 8. Authors and Affiliations

The core authors are Sshubam Verma, Mohammed Safi Ur Rahman Khan, Vishwajeet Kumar, Rudra Murthy, and Jaydeep Sen [Q9], affiliated with the Nilekani Centre at AI4Bharat, Indian Institute of Technology Madras, and IBM Research India [Q10]. The work received funding from EkStep Foundation and Nilekani Philanthropies, specifically supporting datasets, models, tools, and resources for Indian languages [Q86]. The institutional base is firmly within India, with direct ties to the AI4Bharat ecosystem — the same organisation that produced Indic NLP resources cited throughout the paper [Q91] — which strongly signals that the benchmark's cultural and linguistic design choices reflect an India-internal perspective, broadly aligned with the North Indian Hindi teacher deployment context. This affiliation reduces concerns about external-actor bias in content selection, though it does not guarantee proportional representation of all Hindi-belt states' board syllabi.
```

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | task_taxonomy | "MILU spans 8 domains and 41 subjects across 11 Indic languages, reflecting both general and culturally specific knowledge." |
| Q2 | 1 | data_sources | "With an India-centric design, MILU incorporates material from regional and state-level examinations, covering topics such as local history, arts, festivals, and laws, alongside standard subjects like science." |
| Q3 | 1 | evaluation_metrics | "We evaluate over 42 LLMs, and find that current LLMs struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q4 | 1 | stated_limitations | "Open multilingual models outperform language-specific fine-tuned models, which perform only slightly better than random baselines." |
| Q5 | 1 | stated_limitations | "Models also perform better in high-resource languages as compared to low-resource ones." |
| Q6 | 1 | stated_limitations | "Domain-wise analysis indicates that models perform poorly in culturally relevant areas like Arts & Humanities and Law & Governance compared to general fields like STEM." |
| Q7 | 1 | stated_limitations | "To the best of our knowledge, MILU is the first of its kind benchmark focused on Indic languages, serving as a crucial step towards comprehensive cultural evaluation." |
| Q8 | 1 | stated_limitations | "All code, benchmarks, and artifacts will be made publicly available to foster open research." |
| Q9 | 1 | authors_affiliations | "Sshubam Verma, Mohammed Safi Ur Rahman Khan, Vishwajeet Kumar, Rudra Murthy, Jaydeep Sen" |
| Q10 | 1 | authors_affiliations | "Nilekani Centre at AI4Bharat, Indian Institute of Technology, Madras, IBM Research, India" |
| Q11 | 2 | data_sources | "We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams." |
| Q12 | 2 | label_categories | "These questions include culturally relevant subjects such as local history, arts, festivals, and laws, alongside traditional academic subjects like science." |
| Q13 | 2 | data_sources | "Following previous efforts (Hendrycks et al., 2021; Zhong et al., 2023), we create this benchmark by collecting questions from over 1500 competitive exams from India." |
| Q14 | 2 | data_sources | "We focus on region-specific exams to authentically capture local knowledge in the respective language." |
| Q15 | 2 | evaluation_metrics | "We evaluate 45 different LLMs - a mix of closed proprietary, open-source, and language-specific models- on MILU." |
| Q16 | 2 | evaluation_metrics | "Our findings suggest that models struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q17 | 2 | evaluation_metrics | "Interestingly, open multilingual models outperform language-specific models, which only achieve slightly better than random scores." |
| Q18 | 2 | evaluation_metrics | "Our analysis of in-context learning reveals that adding more examples improves performance in base models, but the effect on instruct models remains inconclusive." |
| Q19 | 2 | evaluation_metrics | "We also explore how performance scales with the number of parameters, finding significant improvements as model size increases." |
| Q20 | 2 | evaluation_metrics | "Our domain-wise analysis reveals that models perform poorly in culturally relevant areas, such as Arts & Humanities and Social Sciences, compared to more general fields like STEM." |
| Q21 | 2 | stated_limitations | "All the artifacts will be released publicly." |
| Q22 | 3 | task_taxonomy | "MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge." |
| Q23 | 3 | task_taxonomy | "This benchmark covers many domains, including Science, Social Sciences, Humanities, Arts, Business Studies, and Law, among others." |
| Q24 | 3 | data_sources | "These questions were sourced following an approach similar to AGIEVAL (Zhong et al., 2023), collecting the questions from various public exams taken by individuals intending to either pursue higher studies or seek career advancements, such as qualification tests and national and state-level civil services exams, among others." |
| Q25 | 3 | data_sources | "We gathered exam-specific questions by scraping various online exam portals that offer previously released question papers from various exams in multiple different languages." |
| Q26 | 3 | annotation_process | "These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers." |
| Q27 | 3 | data_sources | "Our benchmark includes questions from over 40 different types of exams conducted both at the national and state levels over recent years." |
| Q28 | 3 | data_sources | "Regional state exams are particularly valuable as they cover various state-level topics and emphasize the official language of each state." |
| Q29 | 3 | data_sources | "In total, we collected more than 150K questions across 11 Indian Languages- Bengali (bn), Gujarati (gu), Hindi (hi), Kannada (kn), Malayalam (ml), Marathi (mr), Odia (or), Punjabi (pn), Tamil (ta), Telugu (te), and English (en)-spanning 41 diverse subjects." |
| Q30 | 3 | data_sources | "English questions are also included as these often address Indian culture-specific content, which is notably missing from existing popular benchmarks." |
| Q31 | 4 | data_format | "Despite our best efforts to maintain the quality of questions collected, some amount of noise or errors may still be present. To address potential noise in the questions, we employ multiple layers of manual and automated cleaning filters." |
| Q32 | 4 | data_format | "Initially, we manually review a large sample of questions to detect and eliminate potential sources of noise." |
| Q33 | 4 | data_format | "During the collection process, we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency." |
| Q34 | 4 | data_format | "To remove incorrect language entries, we utilize a combination of INDICLID (Madhani et al., 2023) and Unicode-based filtering (Khan et al., 2024), ensuring that the questions are in the correct language." |
| Q35 | 4 | data_format | "To further refine the dataset, we remove any duplicate questions to retain only the unique ones." |
| Q36 | 4 | data_format | "As a final step, we manually verify a sample of questions from each language to ensure accuracy and correct any remaining errors." |
| Q37 | 4 | data_format | "Upon examination, we found that approximately 45% of questions were accurately labeled with a topic name, while the remaining questions lacked this information." |
| Q38 | 4 | data_format | "To address this issue, we first translate the untagged questions into English using INDICTRANS2 (Gala et al., 2023) and then prompt GPT-4O-MINI model to assign an appropriate topic name to the question." |
| Q39 | 4 | label_categories | "Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap." |
| Q40 | 4 | data_format | "To organize them, we embed the tags using the NV-EMBED-V2 (Lee et al., 2024) model and apply K-means clustering to group tags into 50 clusters." |
| Q41 | 4 | annotation_process | "We manually review these clusters and assign appropriate subject labels." |
| Q42 | 4 | label_categories | "Following the manual merging of related clusters, we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies." |
| Q43 | 4 | stated_limitations | "Finally, we observed that some topics in certain languages had less than 100 questions. To ensure thorough evaluation across all subjects and languages, we aimed to have at least 100 questions per subject in each language." |
| Q44 | 4 | data_format | "For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O." |
| Q45 | 4 | data_format | "We chose GPT-4O over specialized translation models for their ability to remain task-aware during translation (Ahuja et al., 2024), ensuring the translated content aligns with the intent of the question." |
| Q46 | 4 | data_sources | "In total, we release around 79K questions across 41 subjects across 8 domains in 11 languages, capping each subject-language pair at 500 questions for feasible evaluations." |
| Q47 | 4 | data_sources | "Table 2 shows the overall statistics of MILU. Of the total 79K questions, only 25% of questions are translated from English, with the remainder" |
| Q48 | 5 | evaluation_metrics | "We evaluate 42 different models on MILU, including large proprietary models, open-source multilingual models, and popular fine-tuned models specific to Indic languages." |
| Q49 | 5 | evaluation_metrics | "Both the base versions and instruction fine-tuned variants of these models, wherever applicable, are evaluated to measure the improvements gained from fine-tuning." |
| Q50 | 5 | evaluation_metrics | "All models, except for proprietary models and LLAMA-3.1-405B, are tested under 0-shot, 1-shot, and 5-shot setups." |
| Q51 | 5 | data_sources | "We maintain a separate validation set of approximately 9,000 questions to serve as examples for few-shot evaluations." |
| Q52 | 5 | evaluation_metrics | "For non-API-based models, we use the LM-EVALUATION-HARNESS (Gao et al., 2024; Biderman et al., 2024) to ensure clean and reproducible evaluations." |
| Q53 | 5 | evaluation_metrics | "We use the log-likelihood method, where the probability of a given output string is computed by conditioning it on some provided input (Brown et al., 2020)." |
| Q54 | 5 | evaluation_metrics | "Specifically, the log-likelihood of an answer (a) given the question (x), i.e., logP(a\|x), is calculated by concatenating the answer (a) with question (x), and then summing up the log probabilities, of each target token." |
| Q55 | 5 | evaluation_metrics | "For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability, i.e., argmax(logP(a1\|x), ..., logP(ak\|x))." |
| Q56 | 5 | evaluation_metrics | "The API-based models are evaluated using the generative approach due to the lack of support for prompt log probabilities." |
| Q57 | 5 | evaluation_metrics | "We explicitly prompt these models to generate the correct response in a structured JSON format to simplify response parsing." |
| Q58 | 5 | stated_limitations | "Due to the high costs involved, these models are evaluated only in the zero-shot setup." |
| Q59 | 6 | evaluation_metrics | "We report 5-shot accuracies for all open models (except for LLAMA-3.1-70B-INSTRUCT & LLAMA-3.1-405B for which we report 0-shot accuracy) with the accuracy averaged across all the domains per language." |
| Q60 | 6 | task_taxonomy | "We evaluate around 16 Indic language LLMs on MILU. These models are primarily built by adapting English LLMs, such as LLAMA-2-7B, by first continually pretraining on small amount Indic language data, followed by optionally instruction finetuning them." |
| Q61 | 6 | evaluation_metrics | "As seen from Table 4, across languages, the models exhibit average performance comparable to random baselines, with minimal variations among them." |
| Q62 | 6 | evaluation_metrics | "When analyzed across domains, the models generally perform worse in Arts, Humanities, and Social Sciences than in STEM subjects." |
| Q63 | 6 | evaluation_metrics | "We compare the performance of different Base and Instruct models across zero, one, and five-shot setups." |
| Q64 | 6 | evaluation_metrics | "As shown in Figure 3, the performance of base models consistently improves with an increasing number of in-context examples, with the 5-shot setup yielding the best results." |
| Q65 | 6 | stated_limitations | "In contrast, Instruct models exhibit more varied behavior, where models either stagnate or even degrade in performance." |
| Q66 | 6 | stated_limitations | "This also aligns with expectations, as Instruct models are specifically fine-tuned as conversation assistants and may not respond well to the few-shot in-context examples format." |
| Q67 | 7 | evaluation_metrics | "Table 4: Evaluation results of all the language-specific fine-tuned models on MILU. We report domain level 5-shot accuracies for all the models on the language supported by the model. Higher values indicate better model performance for the given domain." |
| Q68 | 7 | evaluation_metrics | "Figure 3: Comparison of Base and Instruct models averaged across all languages for varying number of in-context examples. We plot the average accuracies of the GEMMA and LLAMA series of models, highlighting the performance trend as the number of in-context examples increases." |
| Q69 | 7 | evaluation_metrics | "We evaluate the LLAMA and GEMMA family of models, ranging from 1B to 405B parameters, to analyze how performance scales with model size." |
| Q70 | 7 | evaluation_metrics | "Figure 5 shows that the model performance improves significantly with increasing scale. Notably, instruction-tuned models in the LLAMA family show more substantial improvements as compared to those in the GEMMA family." |
| Q71 | 7 | evaluation_metrics | "We analyze the performance of various base and instruct models across multiple domains and languages. Similar trends to those in Section (§5.2) are observed where the open models perform poorly in domains specific to Indian culture—such as Arts & Humanities, Social Sciences, and Law & Governance—but demonstrate higher performance in STEM fields." |
| Q72 | 7 | stated_limitations | "This suggests that the training corpora for these models lack sufficient culturally specific data. Bridging this gap requires a more inclusive data distribution that ensures equitable representation of all cultures and languages." |
| Q73 | 7 | evaluation_metrics | "As most Indic LLMs are built on English base models like LLAMA-2-7B, we assess the impact of language adaptation on their performance. Table 5 compares language-specific models with the original LLAMA-2-7B, and instruction-tuned models with LLAMA-2-7B-CHAT. Our findings show minimal gains, with some models even underperforming post-adaptation." |
| Q74 | 8 | task_taxonomy | "In this paper, we introduced MILU—Multilingual Indic Language Understanding Benchmark-a comprehensive benchmark specifically designed to evaluate LLMs across 11 Indic languages, spanning diverse domains and culturally relevant subjects." |
| Q75 | 8 | evaluation_metrics | "We evaluate 45 different LLMs and find that the majority of LLMs struggle on MILU, with GPT4o achieving the highest average accuracy." |
| Q76 | 8 | stated_limitations | "The analysis also shows that models perform significantly better in high-resource languages than low-resource ones, highlighting the need for more robust multilingual strategies." |
| Q77 | 8 | stated_limitations | "Additionally, the domain-specific analysis indicates that models perform better in general fields such as STEM while facing challenges in culturally relevant subjects like Arts, Humanities, and Law, highlighting the lack of this knowledge in the current models and datasets." |
| Q78 | 8 | stated_limitations | "We conjecture that limited performance gains may result from small language-specific datasets and reliance on parameter-efficient methods like LoRA (Hu et al., 2022)." |
| Q79 | 8 | stated_limitations | "Another contributing factor could be the lack of diversity in instruction fine-tuning datasets." |
| Q80 | 8 | stated_limitations | "Models like AIRAVATA, which utilize more diverse data (Gala et al., 2024), exhibit noticeably better performance." |
| Q81 | 8 | stated_limitations | "Further investigation is required to fully understand the limitations and opportunities in this area." |
| Q82 | 9 | stated_limitations | "First, we restricted our study to the top 11 languages due to the lack of readily available questions in low-resource languages, which we aim to address in future work." |
| Q83 | 9 | stated_limitations | "Second, limited computational resources prevented a thorough evaluation of larger models, such as LLAMA-3.1-70B-INSTRUCT and LLAMA-3.1-405B." |
| Q84 | 9 | stated_limitations | "Third, the scarcity of questions necessitated translating a portion of the dataset." |
| Q85 | 9 | stated_limitations | "Finally, our evaluation primarily relies on the log-likelihood approach, which may yield different results compared to other established methods, such as generation-based evaluation and chain-of-thought (CoT) prompting." |
| Q86 | 9 | authors_affiliations | "We would like to thank EkStep Foundation and Nilekani Philanthropies for their generous grant towards building datasets, models, tools and other resources for Indian languages." |
| Q87 | 9 | annotation_process | "We are also immensely grateful to the volunteers from the AI4Bharat team for their motivation and meticulous efforts in conducting manual audits." |
| Q88 | 9 | data_sources | "All data described in this work was scraped from publicly available resources." |
| Q89 | 9 | data_sources | "The datasets used in this paper will be made available under permissible licenses." |
| Q90 | 9 | data_sources | "Additionally, the code used for our evaluations will be made publicly available under the MIT License." |
| Q91 | 10 | authors_affiliations | "Sumanth Doddapaneni, Rahul Aralikatte, Gowtham Ramesh, Shreya Goyal, Mitesh M. Khapra, Anoop Kunchukuttan, and Pratyush Kumar. 2023. Towards leaving no Indic language behind: Building monolingual corpora, benchmark and models for Indic languages. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 12402–12426, Toronto, Canada. Association for Computational Linguistics." |
| Q92 | 17 | data_sources | "We collected our questions from over 40 exam types ranging from various National and state level civil service examinations to examinations conducted by various government and private organizations." |
| Q93 | 17 | data_format | "Detailed analysis of topic and language distribution across languages can be found in Table 9 and Figure 6" |
| Q94 | 17 | evaluation_metrics | "Model details about the different models evaluated in this work is present in Table 10." |
| Q95 | 18 | data_sources | "Table 6: Overview of various national-level exams and the corresponding years of coverage considered in MILU." |
| Q96 | 18 | data_sources | "Table 7: Overview of various government and private organization exams and the corresponding years of coverage considered in MILU." |
| Q97 | 18 | data_sources | "Table 8: Overview of various State-level civil services exams and the corresponding years of coverage considered in MILU." |
| Q98 | 20 | task_taxonomy | "Table 9: Detailed subject level statistics of MILU across different languages." |
| Q99 | 22 | evaluation_metrics | "Table 11: Detailed subject-wise evaluation for ABHINAND/TAMIL-LLAMA-7B-INSTRUCT-V0.2 on MILU across different languages." |
| Q100 | 22 | evaluation_metrics | "The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q101 | 23 | evaluation_metrics | "Table 12: Detailed subject-wise evaluation for AI4BHARAT/AIRAVATA on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q102 | 24 | evaluation_metrics | "Table 13: Detailed subject-wise evaluation for BHABHAAI/GAJENDRA-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q103 | 25 | evaluation_metrics | "Table 14: Detailed subject-wise evaluation for COGNITIVE-LAB/AMBARI-7B-BASE-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q104 | 26 | evaluation_metrics | "Table 15: Detailed subject-wise evaluation for COGNITIVE-LAB/AMBARI-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q105 | 27 | evaluation_metrics | "Table 16: Detailed subject-wise evaluation for GENVRADMIN/ARYABHATTA-GEMMAGENZ-VIKAS-MERGED on MILU across different languages." |
| Q106 | 28 | evaluation_metrics | "Table 17: Detailed subject-wise evaluation for MANISHIITG/OPEN-ADITI-V6-LLAMA3 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q107 | 29 | evaluation_metrics | "Table 18: Detailed subject-wise evaluation for NICKMALHOTRA/PROJECTINDUS on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q108 | 30 | evaluation_metrics | "Table 19: Detailed subject-wise evaluation for SARVAMAI/OPENHATHI-7B-HI-V0.1-BASE on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q109 | 31 | evaluation_metrics | "Table 20: Detailed subject-wise evaluation for TENSOIC/KAN-LLAMA-7B-BASE on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q110 | 32 | evaluation_metrics | "Table 21: Detailed subject-wise evaluation for ABHINAND/MALAYALAM-LLAMA-7B-INSTRUCT-V0.1 on MILU across different languages." |
| Q111 | 33 | evaluation_metrics | "Table 22: Detailed subject-wise evaluation for ABHINAND/TELUGU-LLAMA-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q112 | 34 | evaluation_metrics | "Table 23: Detailed subject-wise evaluation for SMALLSTEPAI/MISAL-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q113 | 35 | evaluation_metrics | "Table 24: Detailed subject-wise evaluation for SMALLSTEPAI/MISAL-7B-BASE-V0.1 on MILU across different languages." |
| Q114 | 36 | evaluation_metrics | "Table 25: Detailed subject-wise evaluation for TELUGU-LLM-LABS/TELUGU-LLAMA2-7B-V0-BASE on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q115 | 37 | evaluation_metrics | "Table 26: Detailed subject-wise evaluation for GPT-4o on MILU across different languages. The results reported are for 0-shot experiments." |
| Q116 | 38 | evaluation_metrics | "Table 27: Detailed subject-wise evaluation for GPT-4O-MINI on MILU across different languages. The results reported are for 0-shot experiments." |
| Q117 | 39 | evaluation_metrics | "Table 28: Detailed subject-wise evaluation for GEMINI-1.5-PRO on MILU across different languages. The results reported are for 0-shot experiments." |
| Q118 | 40 | evaluation_metrics | "Table 29: Detailed subject-wise evaluation for GEMINI-1.5-FLASH on MILU across different languages. The results reported are for 0-shot experiments." |
| Q119 | 41 | evaluation_metrics | "Table 30: Detailed subject-wise evaluation for KRUTRIM-SPECTRE-V2 on MILU across different languages. The results reported are for 0-shot experiments." |
| Q120 | 42 | evaluation_metrics | "Table 31: Detailed subject-wise evaluation for SARVAMAI/SARVAM-1 on MILU across different languages. The results reported are for 5-shot experiments." |
| Q121 | 43 | evaluation_metrics | "Table 32: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.2-1B on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q122 | 43 | evaluation_metrics | "Table 33: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.2-1B-INSTRUCT on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q123 | 44 | evaluation_metrics | "Table 34: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-2B on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q124 | 44 | evaluation_metrics | "Table 35: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-2B-IT on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q125 | 46 | evaluation_metrics | "Table 38: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.2-3B-INSTRUCT on MILU across different languages." |
| Q126 | 47 | evaluation_metrics | "Table 39: Detailed subject-wise evaluation for NVIDIA/NEMOTRON-4-MINI-HINDI-4B-BASE on MILU across different languages. The results reported are for 5-shot experiments." |
| Q127 | 49 | evaluation_metrics | "Table 42: Detailed subject-wise evaluation for NEULAB/PANGEA-7B on MILU across different languages. The results reported are for 5-shot experiments." |
| Q128 | 52 | evaluation_metrics | "Table 47: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-9B-IT on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q129 | 52 | evaluation_metrics | "Table 48: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-27B on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q130 | 55 | evaluation_metrics | "Table 52: 0-shot subject-wise evaluation for META-LLAMA/LLAMA-3.1-70B-INSTRUCT on MILU across different languages." |
| Q131 | 56 | evaluation_metrics | "Table 53: 1-shot subject-wise evaluation for META-LLAMA/LLAMA-3.1-70B-INSTRUCT on MILU across different languages." |
| Q132 | 57 | evaluation_metrics | "Table 54: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.1-405B on MILU across different languages. The results reported are for 0-shot experiments." |

### Category Index
- **task_taxonomy**: Q1, Q22, Q23, Q60, Q74, Q98
- **data_sources**: Q2, Q11, Q13, Q14, Q24, Q25, Q27, Q28, Q29, Q30, Q46, Q47, Q51, Q88, Q89, Q90, Q92, Q95, Q96, Q97
- **data_format**: Q31, Q32, Q33, Q34, Q35, Q36, Q37, Q38, Q40, Q44, Q45, Q93
- **label_categories**: Q12, Q39, Q42
- **annotation_process**: Q26, Q41, Q87
- **evaluation_metrics**: Q3, Q15, Q16, Q17, Q18, Q19, Q20, Q48, Q49, Q50, Q52, Q53, Q54, Q55, Q56, Q57, Q59, Q61, Q62, Q63, Q64, Q67, Q68, Q69, Q70, Q71, Q73, Q75, Q94, Q99, Q100, Q101, Q102, Q103, Q104, Q105, Q106, Q107, Q108, Q109, Q110, Q111, Q112, Q113, Q114, Q115, Q116, Q117, Q118, Q119, Q120, Q121, Q122, Q123, Q124, Q125, Q126, Q127, Q128, Q129, Q130, Q131, Q132
- **stated_limitations**: Q4, Q5, Q6, Q7, Q8, Q21, Q43, Q58, Q65, Q66, Q72, Q76, Q77, Q78, Q79, Q80, Q81, Q82, Q83, Q84, Q85
- **authors_affiliations**: Q9, Q10, Q86, Q91
