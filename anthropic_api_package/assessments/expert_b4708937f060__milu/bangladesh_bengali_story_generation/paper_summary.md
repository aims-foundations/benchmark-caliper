```markdown
# Validity Extraction: MILU: A Multi-task Indic Language Understanding Benchmark
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: MILU: A Multi-task Indic Language Understanding Benchmark
- **Authors**: Sshubam Verma, Mohammed Safi Ur Rahman Khan, Vishwajeet Kumar, Rudra Murthy, Jaydeep Sen
- **Venue/Year**: Not explicitly stated in registry (inferred 2024 from model references)
- **Total Pages**: 57
- **Quotes Extracted**: 132

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

### 1. Task Taxonomy / Test Case Categories

MILU is framed as a large-scale multiple-choice understanding benchmark spanning 8 domains and 41 subjects across 11 Indic languages, explicitly designed to capture both general academic knowledge and culturally specific Indian knowledge [Q1, Q17]. The eight domains are: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies [Q38], and the benchmark is described as assessing "general problem-solving abilities and India-specific knowledge" [Q19]. The 41-subject taxonomy was derived through a semi-automated clustering process and covers a wide disciplinary range including science, humanities, arts, business studies, and law [Q18]. Detailed subject-level statistics are provided across all languages [Q99], and model evaluations are reported at the subject level in extensive appendix tables [Q128]. Critically for the Bangladesh deployment context, this entire taxonomic structure is India-centric by design: the cultural, historical, and institutional categories that are foundational to Bangladeshi identity — the 1971 Liberation War as a Bangladeshi national event, Bangladeshi national curriculum exams (SSC/HSC), Bangladeshi universities, and Bangladeshi political history — are structurally absent from a subject ontology derived from Indian competitive examinations. The benchmark explicitly acknowledges poor model performance in Arts & Humanities and Law & Governance [Q6], the very domains where Bangladesh-specific cultural content would most plausibly appear, further limiting its diagnostic value for this deployment.

### 2. Data Sources and Collection

MILU's data was collected from over 1,500 competitive examinations from India, scraped from online exam portals that host previously released question papers [Q11, Q21], following an approach analogous to the AGIEVAL benchmark [Q20]. The benchmark includes questions from over 40 types of national and state-level exams — including civil service examinations, government and private organization exams, and state-level competitive tests — with detailed coverage tables provided for national, state, and organizational exam categories [Q93, Q96, Q97, Q98]. A key design principle is the emphasis on region-specific state exams to "authentically capture local knowledge in the respective language" [Q12, Q24], and English-language questions with Indian cultural content were deliberately included to address gaps in existing benchmarks [Q26]. A separate validation set of approximately 9,000 questions was maintained for few-shot evaluation [Q47]. The total released dataset comprises approximately 79,000 questions, with 25% translated from English and the remainder organically sourced in the target languages [Q42, Q43]. All data was scraped from publicly available resources and will be released under permissible licenses [Q88, Q89]. For the Bangladesh deployment, this provenance is the single most consequential validity gap: every data source is an Indian examination, meaning Bengali-language items almost certainly reflect West Bengali or pan-Indian cultural references rather than Bangladeshi-specific named entities, institutions, geography, and political history. No Bangladeshi exam sources (e.g., SSC/HSC board papers, Dhaka University entrance exams) are mentioned anywhere in the registry.

### 3. Data Format and Preprocessing

MILU consists exclusively of text-based multiple-choice questions with up to four answer options [Q29], making it a unimodal text benchmark in Indic scripts. For the Bangladesh deployment, where the target modality is also text-based Bengali, this represents no modality mismatch — though script rendering consistency for Bengali (Bangla script) warrants routine verification. The preprocessing pipeline involved multiple cleaning layers: manual review of a large sample to detect noise, automated language identification using INDICLID and Unicode-based filtering to ensure correct language assignment [Q27, Q28, Q30], and deduplication to retain only unique questions [Q31]. Reading comprehension questions, image-based questions, and items with more than four answer options were excluded to enforce uniformity [Q29]. For subjects where fewer than 100 questions existed in a given language, English-language questions from that subject were translated into the target language using GPT-4O, chosen for its task-aware translation capability [Q39, Q40, Q41]. Topic tags were assigned using GPT-4O-MINI for untagged questions (approximately 55% of the dataset), with tags embedded and clustered into 50 groups using NV-EMBED-V2 and K-means clustering before manual label assignment [Q34, Q36]. A final manual verification step was applied to a sample from each language [Q32], and detailed distribution statistics are available in appendix tables [Q94].

### 4. Label Categories and Output Types

The primary output label for each MILU item is a single correct answer among up to four multiple-choice options, reflecting the format of Indian competitive examinations. The subject-level label taxonomy comprises 41 distinct subject names organized into 8 domains [Q38], which serve as metadata labels for domain-level analysis rather than model output targets. Approximately 45% of questions arrived with topic tags from the source portals, while the remaining 55% were labeled programmatically [Q33]; the resulting ~20,000 fine-grained topic tags were merged into the final 41-subject ontology [Q35, Q38]. The content of "culturally relevant subjects" such as local history, arts, festivals, and laws is explicitly described as an intended coverage area alongside standard academic subjects [Q10]. For the Bangladesh deployment, the output label space — correct answers validated by Indian examination frameworks — is misaligned in two respects: the MCQ correctness labels reflect Indian knowledge standards rather than Bangladeshi ones, and the benchmark's output format (discrete MCQ labels) does not match the deployment's target output (open-ended culturally grounded story generation).

### 5. Annotation Process

The annotation and quality assurance process for MILU was relatively lean and relied heavily on the source exam portals' own verification infrastructure. Portals from which questions were scraped are described as manually tagging questions with topic names and language details, with subject experts ensuring answer accuracy at the source [Q22]. The benchmark team additionally performed manual cluster review to assign appropriate subject labels after automated clustering [Q37], and AI4Bharat team volunteers conducted manual audits of the dataset [Q87]. No formal inter-annotator agreement statistics, annotator demographic profiles, or structured annotation protocols are disclosed in the registry. This absence is validity-relevant for the Bangladesh deployment: the paper provides no information about whether any native Bangladeshi Bengali speakers participated in reviewing, validating, or auditing the Bengali-language items. Given that the source exams are Indian, it is reasonable to infer that annotators and subject-matter validators were predominantly Indian, meaning ground-truth labels for Bengali items were established within an Indian cultural and linguistic frame — a meaningful reliability concern for a deployment requiring Bangladeshi Bengali ground truth.

### 6. Evaluation Metrics and Output Modality

MILU evaluates LLMs using accuracy as the primary metric across 42–45 models spanning proprietary, open-source multilingual, and Indic-language-specific categories [Q3, Q13, Q44]. For non-API models, evaluation uses the log-likelihood method via LM-EVALUATION-HARNESS, selecting the answer option with the highest conditional log probability [Q48, Q49, Q50, Q51]; API-based models use a generative approach with structured JSON output due to the absence of log-probability support [Q52, Q53]. Models are evaluated under 0-shot, 1-shot, and 5-shot conditions wherever feasible, with 5-shot accuracy reported as the primary figure for open models [Q46, Q55]; API models are evaluated only in the zero-shot setting due to cost constraints [Q54]. The benchmark documents performance trends across model scale [Q64, Q65, Q66], in-context learning behavior [Q60, Q61], and domain-level breakdown [Q67, Q16]. Extensive per-model, per-subject, per-language result tables are provided in the appendix (Tables 11–54) [Q100–Q132]. For the Bangladesh deployment, the output modality gap is significant: MILU measures factual recall accuracy on MCQ items, while the deployment requires evaluating culturally grounded open-ended story generation in Bengali. Benchmark accuracy scores on Indian exam questions therefore do not directly transfer as validity evidence for story generation quality, though strong cultural-knowledge performance might be a necessary (but not sufficient) precondition for culturally grounded generation.

### 7. Stated Limitations

The authors acknowledge several limitations with direct bearing on the Bangladesh deployment. The most structurally relevant is the restriction to 11 languages due to unavailability of exam questions for lower-resource languages [Q82], which implicitly confirms that language coverage is entirely dependent on Indian exam availability — a framework that excludes Bangladeshi exam systems by design. The authors explicitly note that models perform significantly better in high-resource languages than low-resource ones [Q5, Q76], and that Bengali, while included, sits within a resource hierarchy shaped by Indian data availability. Domain-level analysis consistently shows that models perform poorly in culturally relevant areas such as Arts & Humanities and Law & Governance compared to STEM [Q6, Q16, Q59, Q68], and the authors directly attribute this to training corpora lacking "sufficient culturally specific data" [Q69], calling for "a more inclusive data distribution that ensures equitable representation of all cultures and languages" [Q70]. The benchmark also acknowledges that open multilingual models outperform language-specific fine-tuned models, with the latter performing near random baselines [Q4, Q58], that instruction-tuned models behave inconsistently under few-shot prompting [Q62, Q63], and that limited performance gains from language adaptation may reflect small language-specific datasets and parameter-efficient fine-tuning constraints [Q73, Q78, Q79]. Additional methodological limitations include: partial dataset translation from English introducing potential register and content distortion [Q84]; evaluation reliance on the log-likelihood approach, which may diverge from generation-based or chain-of-thought evaluation [Q85]; and computational resource constraints limiting full evaluation of the largest models [Q83]. The paper does not, however, explicitly acknowledge the India–Bangladesh cultural distinction within its Bengali coverage, nor does it flag that "Bengali" in MILU refers to Indian Bengali exam content that may not generalize to Bangladeshi linguistic and cultural contexts.

### 8. Authors and Affiliations

The benchmark was produced by researchers affiliated with three Indian institutions: the Nilekani Centre at AI4Bharat, the Indian Institute of Technology Madras (IIT Madras), and IBM Research India [Q8]. Funding was provided by the EkStep Foundation and Nilekani Philanthropies, both India-based organizations oriented toward Indian language technology [Q86]. The codebase will be released under the MIT License [Q90], and a broader reference to Indic NLP infrastructure development situates this work within the AI4Bharat ecosystem of Indian-language benchmarks and models [Q92]. The institutional composition is entirely Indian, which is consistent with the benchmark's India-first design philosophy [Q9] but confirms that no Bangladeshi institutional perspective, Bangladeshi linguistic expertise, or Bangladesh-focused research agenda shaped the benchmark's construction. This affiliation profile reinforces the content validity concern: the benchmark was built by and for an Indian context, and its Bengali component reflects Indian Bengali educational and cultural norms rather than Bangladeshi ones. Additional model details referenced in the appendix [Q95] further document the Indian-ecosystem focus of the evaluated model suite.
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
| Q8 | 1 | authors_affiliations | "Sshubam Verma1 Mohammed Safi Ur Rahman Khan1,2 Vishwajeet Kumar3 Rudra Murthy3 Jaydeep Sen3 1Nilekani Centre at AI4Bharat 2Indian Institute of Technology, Madras 3IBM Research, India" |
| Q9 | 2 | data_sources | "We designed MILU with an India-first perspective by collecting questions from various national, state, and regional exams." |
| Q10 | 2 | label_categories | "These questions include culturally relevant subjects such as local history, arts, festivals, and laws, alongside traditional academic subjects like science." |
| Q11 | 2 | data_sources | "We create this benchmark by collecting questions from over 1500 competitive exams from India." |
| Q12 | 2 | data_sources | "We focus on region-specific exams to authentically capture local knowledge in the respective language." |
| Q13 | 2 | evaluation_metrics | "We evaluate 45 different LLMs - a mix of closed proprietary, open-source, and language-specific models- on MILU." |
| Q14 | 2 | evaluation_metrics | "Our findings suggest that models struggle with MILU, with GPT-4o achieving the highest average accuracy at 74%." |
| Q15 | 2 | evaluation_metrics | "Our analysis of in-context learning reveals that adding more examples improves performance in base models, but the effect on instruct models remains inconclusive." |
| Q16 | 2 | evaluation_metrics | "Our domain-wise analysis reveals that models perform poorly in culturally relevant areas, such as Arts & Humanities and Social Sciences, compared to more general fields like STEM." |
| Q17 | 3 | task_taxonomy | "MILU is a large, multi-domain test set containing multiple-choice based questions (MCQs) taken from over 41 subjects with an emphasis on India-specific knowledge." |
| Q18 | 3 | task_taxonomy | "This benchmark covers many domains, including Science, Social Sciences, Humanities, Arts, Business Studies, and Law, among others." |
| Q19 | 3 | task_taxonomy | "MILU is designed as a culturally relevant benchmark to assess general problem-solving abilities and India-specific knowledge." |
| Q20 | 3 | data_sources | "These questions were sourced following an approach similar to AGIEVAL (Zhong et al., 2023), collecting the questions from various public exams taken by individuals intending to either pursue higher studies or seek career advancements, such as qualification tests and national and state-level civil services exams, among others." |
| Q21 | 3 | data_sources | "We gathered exam-specific questions by scraping various online exam portals that offer previously released question papers from various exams in multiple different languages." |
| Q22 | 3 | annotation_process | "These portals typically tag questions manually with topic names and language details, and subject experts ensure the accuracy of the answers." |
| Q23 | 3 | data_sources | "Our benchmark includes questions from over 40 different types of exams conducted both at the national and state levels over recent years." |
| Q24 | 3 | data_sources | "Regional state exams are particularly valuable as they cover various state-level topics and emphasize the official language of each state." |
| Q25 | 3 | data_sources | "In total, we collected more than 150K questions across 11 Indian Languages- Bengali (bn), Gujarati (gu), Hindi (hi), Kannada (kn), Malayalam (ml), Marathi (mr), Odia (or), Punjabi (pn), Tamil (ta), Telugu (te), and English (en)-spanning 41 diverse subjects." |
| Q26 | 3 | data_sources | "English questions are also included as these often address Indian culture-specific content, which is notably missing from existing popular benchmarks." |
| Q27 | 4 | data_format | "Despite our best efforts to maintain the quality of questions collected, some amount of noise or errors may still be present. To address potential noise in the questions, we employ multiple layers of manual and automated cleaning filters." |
| Q28 | 4 | data_format | "Initially, we manually review a large sample of questions to detect and eliminate potential sources of noise." |
| Q29 | 4 | data_format | "During the collection process, we exclude any reading-comprehension-style questions, images-based questions, and those with more than four answer options to ensure uniformity and consistency." |
| Q30 | 4 | data_format | "To remove incorrect language entries, we utilize a combination of INDICLID (Madhani et al., 2023) and Unicode-based filtering (Khan et al., 2024), ensuring that the questions are in the correct language." |
| Q31 | 4 | data_format | "To further refine the dataset, we remove any duplicate questions to retain only the unique ones." |
| Q32 | 4 | data_format | "As a final step, we manually verify a sample of questions from each language to ensure accuracy and correct any remaining errors." |
| Q33 | 4 | label_categories | "Upon examination, we found that approximately 45% of questions were accurately labeled with a topic name, while the remaining questions lacked this information." |
| Q34 | 4 | data_format | "To address this issue, we first translate the untagged questions into English using INDICTRANS2 (Gala et al., 2023) and then prompt GPT-4O-MINI model to assign an appropriate topic name to the question." |
| Q35 | 4 | label_categories | "Finally, in total, we get around 20K tags. However, these tags are highly fine-grained, often having a heavy overlap." |
| Q36 | 4 | data_format | "To organize them, we embed the tags using the NV-EMBED-V2 (Lee et al., 2024) model and apply K-means clustering to group tags into 50 clusters." |
| Q37 | 4 | annotation_process | "We manually review these clusters and assign appropriate subject labels." |
| Q38 | 4 | label_categories | "Following the manual merging of related clusters, we determine 41 distinct subject names, which fall into eight main domains: Arts and Humanities, Social Sciences, Environmental Sciences, Law and Governance, Health and Medicine, Science, Engineering and Technology, and Business Studies." |
| Q39 | 4 | data_format | "Finally, we observed that some topics in certain languages had less than 100 questions. To ensure thorough evaluation across all subjects and languages, we aimed to have at least 100 questions per subject in each language." |
| Q40 | 4 | data_format | "For subjects with insufficient questions, we sampled questions from the English set from that subject and translated them into the required language using GPT-4O." |
| Q41 | 4 | data_format | "We chose GPT-4O over specialized translation models for their ability to remain task-aware during translation (Ahuja et al., 2024), ensuring the translated content aligns with the intent of the question." |
| Q42 | 4 | data_sources | "In total, we release around 79K questions across 41 subjects across 8 domains in 11 languages, capping each subject-language pair at 500 questions for feasible evaluations." |
| Q43 | 4 | data_sources | "Table 2 shows the overall statistics of MILU. Of the total 79K questions, only 25% of questions are translated from English, with the remainder" |
| Q44 | 5 | evaluation_metrics | "We evaluate 42 different models on MILU, including large proprietary models, open-source multilingual models, and popular fine-tuned models specific to Indic languages." |
| Q45 | 5 | evaluation_metrics | "Both the base versions and instruction fine-tuned variants of these models, wherever applicable, are evaluated to measure the improvements gained from fine-tuning." |
| Q46 | 5 | evaluation_metrics | "All models, except for proprietary models and LLAMA-3.1-405B, are tested under 0-shot, 1-shot, and 5-shot setups." |
| Q47 | 5 | data_sources | "We maintain a separate validation set of approximately 9,000 questions to serve as examples for few-shot evaluations." |
| Q48 | 5 | evaluation_metrics | "For non-API-based models, we use the LM-EVALUATION-HARNESS (Gao et al., 2024; Biderman et al., 2024) to ensure clean and reproducible evaluations." |
| Q49 | 5 | evaluation_metrics | "We use the log-likelihood method, where the probability of a given output string is computed by conditioning it on some provided input (Brown et al., 2020)." |
| Q50 | 5 | evaluation_metrics | "Specifically, the log-likelihood of an answer (a) given the question (x), i.e., logP(a\|x), is calculated by concatenating the answer (a) with question (x), and then summing up the log probabilities, of each target token." |
| Q51 | 5 | evaluation_metrics | "For multiple choice questions, given k possible answer strings, we select the answer string (ai) with the highest conditional log probability, i.e., argmax(logP(a1\|x), ..., logP(ak\|x))." |
| Q52 | 5 | evaluation_metrics | "The API-based models are evaluated using the generative approach due to the lack of support for prompt log probabilities." |
| Q53 | 5 | evaluation_metrics | "We explicitly prompt these models to generate the correct response in a structured JSON format to simplify response parsing." |
| Q54 | 5 | stated_limitations | "Due to the high costs involved, these models are evaluated only in the zero-shot setup." |
| Q55 | 6 | evaluation_metrics | "We report 5-shot accuracies for all open models (except for LLAMA-3.1-70B-INSTRUCT & LLAMA-3.1-405B for which we report 0-shot accuracy) with the accuracy averaged across all the domains per language." |
| Q56 | 6 | data_sources | "We evaluate around 16 Indic language LLMs on MILU." |
| Q57 | 6 | task_taxonomy | "These models are primarily built by adapting English LLMs, such as LLAMA-2-7B, by first continually pretraining on small amount Indic language data, followed by optionally instruction finetuning them." |
| Q58 | 6 | stated_limitations | "As seen from Table 4, across languages, the models exhibit average performance comparable to random baselines, with minimal variations among them." |
| Q59 | 6 | stated_limitations | "When analyzed across domains, the models generally perform worse in Arts, Humanities, and Social Sciences than in STEM subjects." |
| Q60 | 6 | evaluation_metrics | "We compare the performance of different Base and Instruct models across zero, one, and five-shot setups." |
| Q61 | 6 | evaluation_metrics | "As shown in Figure 3, the performance of base models consistently improves with an increasing number of in-context examples, with the 5-shot setup yielding the best results." |
| Q62 | 6 | stated_limitations | "In contrast, Instruct models exhibit more varied behavior, where models either stagnate or even degrade in performance." |
| Q63 | 6 | stated_limitations | "This also aligns with expectations, as Instruct models are specifically fine-tuned as conversation assistants and may not respond well to the few-shot in-context examples format." |
| Q64 | 7 | evaluation_metrics | "We evaluate the LLAMA and GEMMA family of models, ranging from 1B to 405B parameters, to analyze how performance scales with model size." |
| Q65 | 7 | evaluation_metrics | "Figure 5 shows that the model performance improves significantly with increasing scale." |
| Q66 | 7 | evaluation_metrics | "Notably, instruction-tuned models in the LLAMA family show more substantial improvements as compared to those in the GEMMA family." |
| Q67 | 7 | evaluation_metrics | "We analyze the performance of various base and instruct models across multiple domains and languages." |
| Q68 | 7 | stated_limitations | "Similar trends to those in Section (§5.2) are observed where the open models perform poorly in domains specific to Indian culture—such as Arts & Humanities, Social Sciences, and Law & Governance—but demonstrate higher performance in STEM fields." |
| Q69 | 7 | stated_limitations | "This suggests that the training corpora for these models lack sufficient culturally specific data." |
| Q70 | 7 | stated_limitations | "Bridging this gap requires a more inclusive data distribution that ensures equitable representation of all cultures and languages." |
| Q71 | 7 | evaluation_metrics | "As most Indic LLMs are built on English base models like LLAMA-2-7B, we assess the impact of language adaptation on their performance." |
| Q72 | 7 | evaluation_metrics | "Table 5 compares language-specific models with the original LLAMA-2-7B, and instruction-tuned models with LLAMA-2-7B-CHAT." |
| Q73 | 7 | stated_limitations | "Our findings show minimal gains, with some models even underperforming post-adaptation." |
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
| Q90 | 9 | authors_affiliations | "Additionally, the code used for our evaluations will be made publicly available under the MIT License." |
| Q91 | 9 | stated_limitations | "We only used ChatGPT for assistance purely with the language of the paper, e.g., paraphrasing, spell-checking, or polishing the author's original content, without suggesting new content." |
| Q92 | 10 | authors_affiliations | "Sumanth Doddapaneni, Rahul Aralikatte, Gowtham Ramesh, Shreya Goyal, Mitesh M. Khapra, Anoop Kunchukuttan, and Pratyush Kumar. 2023. Towards leaving no Indic language behind: Building monolingual corpora, benchmark and models for Indic languages. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 12402–12426, Toronto, Canada. Association for Computational Linguistics." |
| Q93 | 17 | data_sources | "We collected our questions from over 40 exam types ranging from various National and state level civil service examinations to examinations conducted by various government and private organizations." |
| Q94 | 17 | data_format | "Detailed analysis of topic and language distribution across languages can be found in Table 9 and Figure 6" |
| Q95 | 17 | authors_affiliations | "Model details about the different models evaluated in this work is present in Table 10." |
| Q96 | 18 | data_sources | "Table 6: Overview of various national-level exams and the corresponding years of coverage considered in MILU." |
| Q97 | 18 | data_sources | "Table 7: Overview of various government and private organization exams and the corresponding years of coverage considered in MILU." |
| Q98 | 18 | data_sources | "Table 8: Overview of various State-level civil services exams and the corresponding years of coverage considered in MILU." |
| Q99 | 20 | task_taxonomy | "Table 9: Detailed subject level statistics of MILU across different languages." |
| Q100 | 22 | evaluation_metrics | "Table 11: Detailed subject-wise evaluation for ABHINAND/TAMIL-LLAMA-7B-INSTRUCT-V0.2 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q101 | 23 | evaluation_metrics | "Table 12: Detailed subject-wise evaluation for AI4BHARAT/AIRAVATA on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q102 | 24 | evaluation_metrics | "Table 13: Detailed subject-wise evaluation for BHABHAAI/GAJENDRA-V0.1 on MILU across different languages." |
| Q103 | 24 | evaluation_metrics | "The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q104 | 25 | evaluation_metrics | "Table 14: Detailed subject-wise evaluation for COGNITIVE-LAB/AMBARI-7B-BASE-V0.1 on MILU across different languages." |
| Q105 | 26 | evaluation_metrics | "Table 15: Detailed subject-wise evaluation for COGNITIVE-LAB/AMBARI-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q106 | 27 | evaluation_metrics | "Table 16: Detailed subject-wise evaluation for GENVRADMIN/ARYABHATTA-GEMMAGENZ-VIKAS-MERGED on MILU across different languages." |
| Q107 | 28 | evaluation_metrics | "Table 17: Detailed subject-wise evaluation for MANISHIITG/OPEN-ADITI-V6-LLAMA3 on MILU across different languages." |
| Q108 | 29 | evaluation_metrics | "Table 18: Detailed subject-wise evaluation for NICKMALHOTRA/PROJECTINDUS on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q109 | 30 | evaluation_metrics | "Table 19: Detailed subject-wise evaluation for SARVAMAI/OPENHATHI-7B-HI-V0.1-BASE on MILU across different languages." |
| Q110 | 31 | evaluation_metrics | "Table 20: Detailed subject-wise evaluation for TENSOIC/KAN-LLAMA-7B-BASE on MILU across different languages." |
| Q111 | 32 | evaluation_metrics | "Table 21: Detailed subject-wise evaluation for ABHINAND/MALAYALAM-LLAMA-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q112 | 33 | evaluation_metrics | "Table 22: Detailed subject-wise evaluation for ABHINAND/TELUGU-LLAMA-7B-INSTRUCT-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q113 | 34 | evaluation_metrics | "Table 23: Detailed subject-wise evaluation for SMALLSTEPAI/MISAL-7B-INSTRUCT-V0.1 on MILU across different languages." |
| Q114 | 35 | evaluation_metrics | "Table 24: Detailed subject-wise evaluation for SMALLSTEPAI/MISAL-7B-BASE-V0.1 on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q115 | 36 | evaluation_metrics | "Table 25: Detailed subject-wise evaluation for TELUGU-LLM-LABS/TELUGU-LLAMA2-7B-V0-BASE on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q116 | 37 | evaluation_metrics | "Table 26: Detailed subject-wise evaluation for GPT-4o on MILU across different languages. The results reported are for 0-shot experiments." |
| Q117 | 38 | evaluation_metrics | "Table 27: Detailed subject-wise evaluation for GPT-4O-MINI on MILU across different languages. The results reported are for 0-shot experiments." |
| Q118 | 39 | evaluation_metrics | "Table 28: Detailed subject-wise evaluation for GEMINI-1.5-PRO on MILU across different languages. The results reported are for 0-shot experiments." |
| Q119 | 40 | evaluation_metrics | "Table 29: Detailed subject-wise evaluation for GEMINI-1.5-FLASH on MILU across different languages. The results reported are for 0-shot experiments." |
| Q120 | 41 | evaluation_metrics | "The results reported are for 0-shot experiments." |
| Q121 | 42 | evaluation_metrics | "Table 31: Detailed subject-wise evaluation for SARVAMAI/SARVAM-1 on MILU across different languages. The results reported are for 5-shot experiments." |
| Q122 | 44 | evaluation_metrics | "Table 34: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-2B on MILU across different languages." |
| Q123 | 44 | evaluation_metrics | "Table 35: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-2B-IT on MILU across different languages." |
| Q124 | 47 | evaluation_metrics | "Table 39: Detailed subject-wise evaluation for NVIDIA/NEMOTRON-4-MINI-HINDI-4B-BASE on MILU across different languages. The results reported are for 5-shot experiments." |
| Q125 | 48 | evaluation_metrics | "Table 40: Detailed subject-wise evaluation for META-LLAMA/LLAMA-2-7B-HF on MILU across different languages." |
| Q126 | 48 | evaluation_metrics | "Table 41: Detailed subject-wise evaluation for META-LLAMA/LLAMA-2-7B-CHAT-HF on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q127 | 49 | evaluation_metrics | "Table 42: Detailed subject-wise evaluation for NEULAB/PANGEA-7B on MILU across different languages. The results reported are for 5-shot experiments." |
| Q128 | 52 | task_taxonomy | "Table 47: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-9B-IT on MILU across different languages." |
| Q129 | 52 | evaluation_metrics | "Table 48: Detailed subject-wise evaluation for GOOGLE/GEMMA-2-27B on MILU across different languages. The results reported are X / Y / Z where X denote the 0-shot, Y denotes 1-shot and Z denotes 5-shot performance respectively." |
| Q130 | 55 | evaluation_metrics | "Table 52: 0-shot subject-wise evaluation for META-LLAMA/LLAMA-3.1-70B-INSTRUCT on MILU across different languages." |
| Q131 | 56 | evaluation_metrics | "1-shot subject-wise evaluation for META-LLAMA/LLAMA-3.1-70B-INSTRUCT on MILU across different languages." |
| Q132 | 57 | evaluation_metrics | "Table 54: Detailed subject-wise evaluation for META-LLAMA/LLAMA-3.1-405B on MILU across different languages. The results reported are for 0-shot experiments." |

### Category Index
- **task_taxonomy**: Q1, Q17, Q18, Q19, Q57, Q74, Q99, Q128
- **data_sources**: Q2, Q9, Q11, Q12, Q20, Q21, Q23, Q24, Q25, Q26, Q42, Q43, Q47, Q56, Q88, Q89, Q93, Q96, Q97, Q98
- **data_format**: Q27, Q28, Q29, Q30, Q31, Q32, Q34, Q36, Q39, Q40, Q41, Q94
- **label_categories**: Q10, Q33, Q35, Q38
- **annotation_process**: Q22, Q37, Q87
- **evaluation_metrics**: Q3, Q13, Q14, Q15, Q16, Q44, Q45, Q46, Q48, Q49, Q50, Q51, Q52, Q53, Q55, Q60, Q61, Q64, Q65, Q66, Q67, Q71, Q72, Q75, Q100, Q101, Q102, Q103, Q104, Q105, Q106, Q107, Q108, Q109, Q110, Q111, Q112, Q113, Q114, Q115, Q116, Q117, Q118, Q119, Q120, Q121, Q122, Q123, Q124, Q125, Q126, Q127, Q129, Q130, Q131, Q132
- **stated_limitations**: Q4, Q5, Q6, Q7, Q54, Q58, Q59, Q62, Q63, Q68, Q69, Q70, Q73, Q76, Q77, Q78, Q79, Q80, Q81, Q82, Q83, Q84, Q85, Q91
- **authors_affiliations**: Q8, Q86, Q90, Q92, Q95
