```markdown
# Validity Extraction: ArabicMMLU: Advancing Rigorous Arabic Language Evaluation
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: ArabicMMLU: Advancing Rigorous Arabic Language Evaluation
- **Authors**: Fajri Koto, Haonan Li, Sara Shatnawi, Jad Doughman, Abdelrahman Boda Sadallah, Aisha Alraeesi, Khalid Almubarak, Zaid Alyafeai, Neha Sengupta, Shady Shehata, Nizar Habash, Preslav Nakov, Timothy Baldwin
- **Venue/Year**: Not explicitly stated in registry (inferred as 2024 ACL-era publication based on cited works)
- **Total Pages**: 19
- **Quotes Extracted**: 112

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

---

### 1. Task Taxonomy / Test Case Categories

ArabicMMLU is structured as a multiple-choice question-answering benchmark comprising 40 tasks that span a wide range of subjects and educational levels [Q25], explicitly framing itself as a shift away from purely linguistic tasks like POS tagging and NER toward reasoning and knowledge evaluation [Q10]. The subjects are drawn across primary, middle, and high school levels, with KSA-sourced data prioritizing Islamic studies alongside mathematics, natural science, social science, and geography [Q28]; subject groups are further organized into STEM, Social Science, Humanities, Arabic Language, and Other [Q107]. For the tutoring deployment context, this taxonomy is directly relevant: the benchmark covers the educational strata (primary through university) that the system targets, and explicitly includes subjects — history, geography, civics, political science — that carry country-specific content variation [Q72, Q73]. However, the taxonomy's country-level granularity is uneven: Jordan and Egypt appear to dominate question counts [Q89], meaning tasks nominally labeled "Social Science" or "Civics" may in practice reflect Jordanian or Egyptian curriculum framing rather than Kuwaiti or Palestinian equivalents. University-level coverage is acknowledged as thin, representing only approximately 6% of all questions [Q71], which is a significant gap for the deployment's goal of supporting university students in law, management, economics, and political science. The benchmark notes future directions for extension, including professional-setting questions, short-answer formats, and multimodal content [Q88], but these remain aspirational rather than implemented. Performance analysis confirms that high school questions are more challenging than primary or middle school ones, with GPT-4 achieving only 61.7% at high school level [Q68, Q69], and negation — a foundational Arabic linguistic phenomenon — is also examined as a distinct analytical dimension [Q84], suggesting the taxonomy captures some linguistic complexity beyond mere factual recall. Importantly, the benchmark explicitly excludes classification-heavy tasks common in prior Arabic NLP benchmarks [Q24], aligning more directly with the generative knowledge demands of a tutoring application.

---

### 2. Data Sources and Collection

ArabicMMLU is sourced from real school examinations collected from eight countries spanning North Africa (Morocco and Egypt), the Levant (Jordan, Palestine, and Lebanon), and the Gulf (UAE, Kuwait, and KSA) [Q26], making it the first Arabic-language benchmark of this kind [Q1]. Data collection involved 10 native Arabic speakers — 6 internal (from Jordan, Egypt, Lebanon, UAE, and KSA) and 4 external (3 Jordanian, 1 Egyptian) — who were tasked with identifying and scraping publicly available exam URLs [Q31, Q32]; each external worker gathered approximately 2,000 questions and internal workers 1,000–2,000 [Q34]. This sourcing strategy is critically relevant for the deployment's Input Content (IC) validity: while Palestine and Kuwait are listed as source countries [Q26], the documented worker nationalities are exclusively Jordanian, Egyptian, Lebanese, Emirati, and Saudi [Q31], raising a material question about whether Palestinian and Kuwaiti exam sources were systematically identified and collected or were underrepresented due to limited public digital availability. The paper explicitly acknowledges that Jordan alone contributed over 6,000 questions while some countries are represented with as few as 100 questions [Q89], and that some countries have not digitized their exams [Q90]. The benchmark also situates itself relative to prior multilingual benchmarks (XGLUE, XTREME, GEM) [Q22] and Arabic-centric benchmarks (Dolphin, OCRA, LAraBench) [Q23], distinguishing itself by using natively Arabic exam content rather than translations. The data distributions by subject and education level are tabulated [Q98, Q101], providing some transparency about coverage, though the detailed per-country breakdown is not captured in the registry. Acknowledgments confirm collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia [Q96], but no collaborator from Kuwait, Palestine, or Morocco is mentioned, reinforcing concerns about uneven national coverage for the deployment's eight target markets.

---

### 3. Data Format and Preprocessing

The benchmark comprises 14,575 multiple-choice questions in Modern Standard Arabic (MSA) across 40 tasks [Q2], collected through manual web scraping within a two-month period; workers captured metadata including source URL, country, subject, level, question text, answer options, and the correct answer key [Q33]. Questions containing multimodal content (images, videos, tables) were explicitly excluded [Q37], and questions with additional contextual passages were required to include that context with each dependent question [Q38]. For the tutoring deployment, the text-only, MSA format aligns well with the formal instructional medium used across all eight target countries at the school level [Q29]; the benchmark also explicitly excluded English-language questions, retaining only Arabic-medium content [Q30]. However, this design choice means that French-medium Moroccan university content — which the deployment may need to support — is entirely absent from the benchmark's scope [Q92], as MSA is the sole language of the dataset. Automatic filtering removed duplicate questions and those lacking answer keys, reducing an initial pool of over 15,000 to 14,575 unique items [Q41]. Prompt templates include placeholders for subject, level, and country in both Arabic and English [Q49], as illustrated in Figure 4 [Q48] and Figure 10 [Q99], which is a noteworthy design feature for the deployment context since it signals that the benchmark was designed with country-aware prompting in mind. Answer probabilities are computed via softmax normalization across candidate options [Q79], and negation detection uses specific Arabic negation phrases [Q85]. The presence of 2–5 answer options per question [Q27] introduces some structural variability relative to a uniform 4-option MCQ format, which may affect random-baseline comparisons across tasks.

---

### 4. Label Categories and Output Types

The label schema is minimal but clearly defined: each question has between 2 and 5 candidate answers with exactly one correct answer designated [Q27]. This single-correct-answer MCQ structure is shared between the benchmark and the tutoring deployment, which reduces output ontology mismatch for multiple-choice instructional contexts.

For the deployment's validity, however, this label schema carries a significant limitation: it encodes a single ground-truth answer without any country-specific branching. For subjects like law or civics — where the correct answer may legitimately differ by national jurisdiction (e.g., Egyptian civil code vs. UAE law) — the flat label structure cannot represent this variability, and a question sourced from one country's exam becomes the universal ground truth for all eight deployment countries. The registry provides no evidence of any country-stratified label scheme or secondary annotation layer that would capture jurisdiction-specific correctness; this is an important gap for Output Content (OC) validity in the deployment context.

---

### 5. Annotation Process

Workers are described as native Arabic speakers with at least Bachelor's degrees — internal workers being Master's students and Research Assistants in Computer Science, and external workers holding Bachelor's degrees [Q35, Q39]. Compensation exceeded the monthly average wage in each respective country [Q36], and a one-hour orientation workshop was conducted before data collection began [Q40]. Quality assurance involved two native Arabic speakers independently annotating 100 randomly sampled questions, verifying correctness of questions and answer keys using available resources including search engines [Q42]; the agreement rate was 96%, which the authors designate as the effective ceiling score for ArabicMMLU [Q43, Q44]. While the annotation workforce is geographically diverse (Jordanian, Egyptian, Lebanese, Emirati, Saudi), the registry does not document annotators from Kuwait, Palestine, or Morocco — a relevant gap given that questions from those national curricula, if present, may have been verified by workers unfamiliar with their specific educational context. The absence of formal inter-annotator agreement statistics beyond the 96% spot-check figure, and the lack of documented annotator demographic details beyond nationality and degree level, means the annotation process meets a reasonable but not comprehensive standard for a benchmark intended to cover eight distinct national curricula.

---

### 6. Evaluation Metrics and Output Modality

The benchmark evaluates 35 models in zero-shot and few-shot settings [Q45], covering 22 open-source multilingual models, 11 open-source Arabic-centric models, and 2 closed-source models (GPT-3.5 and GPT-4) [Q46]. Accuracy is the primary metric, determined for open-source models by the highest probability among candidate options [Q50], with Arabic alphabetic outputs mapped to Arabic letter tokens and English outputs to Latin letter tokens [Q51, Q52]; for closed-source models, the first generated token is extracted via regular expression, with random assignment on failure [Q53, Q54]. The benchmark was tested under four prompt-language and output-alphabet combinations [Q47], with the finding that English prompt with English alphabetic output is optimal for most models [Q56, Q58], though Arabic-centric models (Jais, AceGPT) show greater robustness to Arabic alphabetic output [Q57] — a finding relevant to the deployment, which serves Arabic-speaking students and would likely use Arabic-language prompting. Key results show GPT-4 at 72.5% [Q63], Jais-chat (30B) at 62.3% [Q59], and most open-source multilingual models (BLOOMZ, mT0, LLaMA2, Falcon) below 50% [Q4, Q61, Q62], with substantial room for improvement overall [Q3]. The benchmark explicitly notes that GPT-4 scores 8 points lower on ArabicMMLU than on translated MMLU [Q64], attributing this to the higher proportion of Arabic-specific content [Q65], which is a direct validity signal: the benchmark is meaningfully harder for models that were optimized on translated rather than native Arabic content. Detailed zero-shot results are presented per subject and education level [Q102, Q103], and by subject group under all four prompt configurations [Q105, Q106, Q108, Q110], providing granular diagnostic capability. Calibration analysis shows all three open-source models achieve r > 0.9 correlation between answer probability and accuracy [Q80], and no correlation is found between question length and model confidence [Q81, Q82]; few-shot learning improves base models but degrades instruction-tuned model performance [Q75, Q76], consistent with findings on IndoMMLU and CMMLU [Q77]. Prior Arabic model evaluations relied predominantly on translated MMLU, with GPT-4 reporting 80% on the translated version [Q21], making ArabicMMLU's native-content evaluation a meaningful methodological advance for the deployment context.

---

### 7. Stated Limitations

The authors identify several limitations that are directly consequential for the tutoring deployment's validity. The most foundational concern is the reliance of prior work on English-to-Arabic translated datasets [Q5], which introduces Anglocentric framing and translation errors [Q6]; ArabicMMLU addresses this by using native exam content, but this strength is unevenly distributed across countries. Country representation is explicitly acknowledged as imbalanced: Jordan contributes over 6,000 questions while some countries contribute as few as 100 or are absent entirely [Q89], attributable to the uneven digitization of national exams [Q90] and non-exhaustive web search [Q91]. For the deployment, this means that Kuwait and Palestine — both listed as target countries — may be substantively underrepresented, creating a material Input Content (IC) and Output Content (OC) validity gap for students preparing for Kuwaiti or Palestinian national exams. The benchmark is restricted to Modern Standard Arabic and does not cover dialectical Arabic [Q92], which the authors note as a limitation given that LLMs are often exposed to both; for the deployment this is partially acceptable (MSA is the formal instructional medium) but excludes French-medium Moroccan university content entirely [Q93]. The 96% annotation agreement score is designated as the practical ceiling, meaning up to 4% of answer keys may be incorrect [Q44], and the authors caution that results do not provide conclusive performance assessments due to unknown model pretraining data contamination [Q94, Q95]. University-level questions constitute only approximately 6% of the dataset, potentially skewing results at that level [Q71], which is a notable gap for the deployment's university student cohort. The paper also observes that GPT-4's lower score on ArabicMMLU compared to translated MMLU [Q64] is likely due to Arabic-specific content difficulty [Q65], and flags LLM insensitivity to Arabic negation as a concern [Q83]. The authors explicitly propose future extensions including larger regional coverage, professional-setting questions, and multimodal content [Q88], acknowledging the current scope's incompleteness. The benchmark's importance is underscored by Arabic's status as a language with over 400 million speakers [Q7], making robust, culturally localized evaluation critical.

---

### 8. Authors and Affiliations

The paper is authored by a 13-person team [Q8] affiliated with MBZUAI (Mohammed Bin Zayed University of Artificial Intelligence, UAE), Prince Sattam bin Abdulaziz University (Saudi Arabia), King Fahd University of Petroleum and Minerals (Saudi Arabia), Core42 (UAE), New York University Abu Dhabi (UAE), and the University of Melbourne (Australia) [Q9]. The institutional base is heavily Gulf-centric — four of the five named institutions are UAE or Saudi Arabian — which is consistent with the benchmark's relative strength in Gulf-region exam coverage and may partly explain the stronger representation of KSA and UAE content relative to North African or Levantine countries. Additional contributions came from Core42 team members (Samta Kamboj, Sarah Al Barri, Onkar Pandit) who assisted with Arabic Language question collection [Q97], and the paper acknowledges collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia [Q96]. All open-source models were sourced from HuggingFace [Q111, Q112], and the paper provides extensive background on both Arabic-centric (AraBERT, CAMeLBERT, AraGPT2, AraT5, Jais, AceGPT) [Q13, Q14, Q15, Q16] and multilingual (mBERT, XLM-R, BLOOMZ, Falcon, GPT-4) [Q20] model families, reflecting deep familiarity with the Arabic NLP landscape. The absence of authors affiliated with Moroccan, Palestinian, or Kuwaiti institutions is consistent with the documented gaps in coverage for those national curricula and is a relevant signal for the deployment's validity assessment.
```

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | data_sources | "we present ArabicMMLU, the first multi-task language understanding benchmark for the Arabic language, sourced from school exams across diverse educational levels in different countries spanning North Africa, the Levant, and the Gulf regions." |
| Q2 | 1 | data_format | "Our data comprises 40 tasks and 14,575 multiple-choice questions in Modern Standard Arabic (MSA) and is carefully constructed by collaborating with native speakers in the region." |
| Q3 | 1 | evaluation_metrics | "Our comprehensive evaluations of 35 models reveal substantial room for improvement, particularly among the best open-source models." |
| Q4 | 1 | evaluation_metrics | "Notably, BLOOMZ, mT0, LLaMA2, and Falcon struggle to achieve a score of 50%, while even the top-performing Arabic-centric model only achieves a score of 62.3%." |
| Q5 | 1 | stated_limitations | "Although large language models (LLMs) such as GPT-3.5 (Ouyang et al., 2022), BLOOMZ (Muennighoff et al., 2022), and Jais (Sengupta et al., 2023) have been pretrained with substantial coverage of Modern Standard Arabic (MSA), their reasoning and knowledge assessments are primarily conducted using datasets translated from English to Arabic (Sengupta et al., 2023; Huang et al., 2023), which means there is limited capacity to evaluate content specific to Arabic." |
| Q6 | 1 | stated_limitations | "This reliance on translation systems not only demonstrates an Anglocentric approach (Ramesh et al., 2023; Talat et al., 2022) but also potentially introduces errors and biases." |
| Q7 | 1 | stated_limitations | "Given that Arabic is one of the most widely-spoken languages in the world, with a speaker population of over 400 million people (Shoufan and Alameri, 2015; Diab et al., 2017), it is critically important that datasets be constructed for the language that are regionally- and culturally-localized." |
| Q8 | 1 | authors_affiliations | "Fajri Koto, Haonan Li, Sara Shatnawi, Jad Doughman, Abdelrahman Boda Sadallah, Aisha Alraeesi, Khalid Almubarak, Zaid Alyafeai, Neha Sengupta, Shady Shehata, Nizar Habash, Preslav Nakov, Timothy Baldwin" |
| Q9 | 1 | authors_affiliations | "Department of Natural Language Processing, MBZUAI; Prince Sattam bin Abdulaziz University; King Fahd University of Petroleum and Minerals; Core42; New York University Abu Dhabi; The University of Melbourne" |
| Q10 | 1 | task_taxonomy | "The evaluation of language models has increasingly shifted from linguistically-centric tasks, such as part-of-speech (POS) tagging and named entity recognition (NER), towards reasoning and knowledge evaluation." |
| Q11 | 2 | authors_affiliations | "Early Arabic pretrained language models typically had less than 2 billion parameters and were primarily monolingual." |
| Q12 | 2 | task_taxonomy | "These models can be classified into three main categories: encoder-only, decoder-only, and encoder–decoder models." |
| Q13 | 2 | authors_affiliations | "The encoder-only models, such as AraBERT (Antoun et al., 2020), CAMeLBERT (Inoue et al., 2021), AraELECTRA (Antoun et al., 2021a), and ARBERT & MARBERT (Abdul-Mageed et al., 2021), are mainly from the BERT family." |
| Q14 | 2 | authors_affiliations | "AraGPT2 (Antoun et al., 2021b), on the other hand, is a decoder-only model available in different sizes ranging from 135M to 1.4B parameters." |
| Q15 | 2 | authors_affiliations | "Examples of encoder–decoder models include AraT5 (Nagoudi et al., 2022) and AraBART (Kamal Eddine et al., 2022)." |
| Q16 | 2 | authors_affiliations | "Jais (Sengupta et al., 2023) and AceGPT (Huang et al., 2023) are two recent Arabic-centric decoder-only models with parameter sizes of up to 30B and 13B, respectively." |
| Q17 | 2 | data_sources | "Jais is pretrained on a corpus of 72 billion Arabic tokens, while AceGPT builds upon LLaMA2 and is enhanced with reinforcement learning from AI feedback (Lee et al., 2023) to localize the model to Arabic values and culture." |
| Q18 | 2 | authors_affiliations | "Both models are bilingual (English and Arabic), and were fine-tuned on various instruction datasets." |
| Q19 | 2 | authors_affiliations | "Arabic is also present in multilingual models." |
| Q20 | 2 | authors_affiliations | "This includes earlier models such as mBERT (Devlin et al., 2019) and XLM-R (Conneau et al., 2020), and more recent LLMs such as BLOOMZ (Muennighoff et al., 2022), mT0 (Muennighoff et al., 2022), Falcon (Penedo et al., 2023), GPT-3.5 (Ouyang et al., 2022), and GPT-4 (OpenAI, 2023)." |
| Q21 | 2 | evaluation_metrics | "In the original papers, only GPT-4 was evaluated in Arabic in terms of its reasoning and knowledge capabilities, using the English–Arabic translated MMLU dataset, reporting an accuracy of 80%." |
| Q22 | 2 | data_sources | "Arabic is included in various multilingual benchmarks for natural language understanding and generation, such as XGLUE (Liang et al., 2020), XTREME (Hu et al., 2020), XTREME-R (Ruder et al., 2021) and GEM (Gehrmann et al., 2021)." |
| Q23 | 2 | data_sources | "In recent years, several Arabic-centric benchmarks have been released, such as Dolphin (Nagoudi et al., 2023), OCRA (Elmadany et al., 2023), and LAraBench (Abdelali et al., 2024)." |
| Q24 | 2 | task_taxonomy | "Many tasks in these benchmarks involve classification, such as natural language." |
| Q25 | 3 | task_taxonomy | "ArabicMMLU is an Arabic multiple-choice question-answering dataset comprising 40 tasks spanning a wide range of subjects and education levels." |
| Q26 | 3 | data_sources | "The questions are sourced from eight different countries in North Africa (Morocco and Egypt), the Levant (Jordan, Palestine, and Lebanon), and the Gulf (UAE, Kuwait, and KSA)." |
| Q27 | 3 | label_categories | "Each question has 2–5 candidate answers, with one correct answer." |
| Q28 | 3 | task_taxonomy | "The subjects are drawn from different education levels (primary school, middle school, and KSA, prioritize Islamic studies alongside subjects like mathematics, natural science, social science, and geography." |
| Q29 | 3 | data_format | "In public schools, Arabic is commonly used for teaching and assessment, while in international schools, English is the predominant language of instruction for most subjects, following either the UK or USA curriculum." |
| Q30 | 3 | data_format | "When designing ArabicMMLU, we excluded questions in English and only included questions in Arabic." |
| Q31 | 4 | data_sources | "The data construction process involved a total of 10 Arabic native speakers from different countries: 6 internal workers (1 Jordanian, 1 Egyptian, 1 Lebanese, 1 from UAE, and 2 from KSA) and 4 external workers (3 Jordanian and 1 Egyptian)." |
| Q32 | 4 | data_sources | "During the first stage of data collection, the internal workers were tasked with collecting relevant sources for data collection. These sources were URLs containing the questions, which needed to be publicly available." |
| Q33 | 4 | data_format | "In the second stage, all workers were asked to manually scrape the data within a 2-month period. The task was to collect metadata, including the source (URL of the source document), country, subject, level, question, multiple-choice options, and the correct answer key." |
| Q34 | 4 | data_sources | "Each external worker was assigned to gather 2,000 questions, while internal workers were tasked with gathering 1,000–2,000 questions each." |
| Q35 | 4 | annotation_process | "Our internal workers are Master's students and Research Assistants in Computer Science, while the external workers hold Bachelor's degrees." |
| Q36 | 4 | annotation_process | "We ensured competitive compensation for the workers, exceeding the monthly average wage in each respective country." |
| Q37 | 4 | data_format | "During manual data scraping, workers were instructed to include only questions accompanied by an answer key, and to discard questions containing multi-modal information (e.g., images, videos, or tables)." |
| Q38 | 4 | data_format | "If a question had additional contextual information (e.g., a passage referenced by several questions), the context was required to be included with each corresponding question." |
| Q39 | 4 | annotation_process | "While our workers are native speakers of Modern Standard Arabic with at least Bachelor's degrees, we maintain the quality of our dataset construction through meticulous steps." |
| Q40 | 4 | annotation_process | "Firstly, we conducted a 1-hour workshop before the data collection stage to clarify the process." |
| Q41 | 4 | data_format | "Secondly, we automatically filtered out repetitive questions and those without an answer key, reducing the initial set of over 15,000 questions to 14,575 unique questions." |
| Q42 | 4 | annotation_process | "Finally, we assessed the accuracy of our data collection by having two native Arabic speakers annotate 100 randomly sampled questions. They were provided with all metadata, including the answer key, and tasked with verifying the correctness of each sample using any available resources (e.g., search engines)." |
| Q43 | 4 | annotation_process | "We found that 96% of the questions and answer keys match on average, while the remaining could have incorrect answer keys." |
| Q44 | 4 | stated_limitations | "This 96% score is considered to represent the maximum score meaningfully achievable for ArabicMMLU." |
| Q45 | 5 | evaluation_metrics | "Our experiments focus on zero-shot and few-shot settings across 35 models." |
| Q46 | 5 | evaluation_metrics | "This includes 22 open-source multilingual models (XGLM (Lin et al., 2022), BLOOMZ (Muennighoff et al., 2022), mT0 (Muennighoff et al., 2022), Falcon (Penedo et al., 2023), and LLaMA2 (Touvron et al., 2023), across various sizes), 11 open-source Arabic-centric models (AraT5 (Nagoudi et al., 2022), AraGPT2 (Antoun et al., 2021b), AceGPT (Huang et al., 2023) and Jais (Sengupta et al., 2023), also across various sizes), and 2 closed-source models (GPT-3.5: gpt-3.5-turbo (Ouyang et al., 2022) and GPT-4: gpt-4-0613 (OpenAI, 2023))." |
| Q47 | 5 | evaluation_metrics | "We initially conducted experiments with four settings: (1) Arabic prompt and Arabic alphabetic output, (2) Arabic prompt and English (i.e. Latin script) alphabetic output, (3) English prompt and Arabic alphabetic output, and (4) English prompt and English alphabetic output." |
| Q48 | 5 | data_format | "Figure 4 illustrates the Arabic and English prompts." |
| Q49 | 5 | data_format | "The placeholders [SUBJECT], [LEVEL], and [COUNTRY] are replaced with the corresponding Arabic and English words, while the placeholders [INPUT] and [OPTION] are in Arabic." |
| Q50 | 6 | evaluation_metrics | "Following previous studies (Koto et al., 2023; Li et al., 2023), for open-source models, we determine the answer based on the highest probability among all possible options." |
| Q51 | 6 | evaluation_metrics | "In the case of English alphabetic output, we measure the probability of the first generated token being A, B, C, D, or E." |
| Q52 | 6 | evaluation_metrics | "For Arabic, we measure the probability of the first generated token being @, H., h., X, or è." |
| Q53 | 6 | evaluation_metrics | "For closed-source models, we determine the answer based on the first token generated in the text using a regular expression." |
| Q54 | 6 | evaluation_metrics | "If there is no match, we assign a random answer." |
| Q55 | 6 | evaluation_metrics | "To evaluate the influence of prompt language, we initially benchmarked the open-source models using all four prompt settings (Section 4.1), as depicted in Figure 5." |
| Q56 | 6 | evaluation_metrics | "We observe that the optimal configuration across all models is to use an English prompt and English alphabetic output." |
| Q57 | 6 | evaluation_metrics | "Predictably, the Arabic-specific LLMs — Jais-chat (30B) and AceGPT-chat (13B) — demonstrate the greatest robustness when employing Arabic alphabetic output." |
| Q58 | 6 | evaluation_metrics | "For the remaining experiments, we will report based on the setting of English prompt and English alphabetic output." |
| Q59 | 7 | evaluation_metrics | "As expected, the Arabic-centric model Jais-chat (30B) emerges as the top-performing open-source model, boasting an average score of 62.3%, surpassing GPT-3.5 by 4.6 points." |
| Q60 | 7 | evaluation_metrics | "Compared to AceGPT-chat (13B), both Jais-chat models (13B and 30B) exhibit substantially higher accuracy in areas including STEM, Social Science, Humanities, and Others." |
| Q61 | 7 | evaluation_metrics | "For multilingual models such as BLOOMZ (7B) and mT0 (13B), their performance lags behind Jais, with a disparity of more than 14 points." |
| Q62 | 7 | evaluation_metrics | "XGLM, LLaMA2, and Falcon perform at a level close to random, suggesting their limited proficiency in Arabic." |
| Q63 | 7 | evaluation_metrics | "GPT-4 achieves the highest accuracy, with a score of 72.5%, surpassing Jais-chat (30B) by 10 points." |
| Q64 | 7 | stated_limitations | "It is noteworthy that in the GPT-4 technical report (OpenAI, 2023), the accuracy of the English-Arabic translated MMLU dataset is reported as 80%, which is 8 points higher than our ArabicMMU results." |
| Q65 | 7 | stated_limitations | "One possible explanation for this difference is that our ArabicMMU presents a greater challenge due to its inclusion of a higher proportion of Arabic-specific content." |
| Q66 | 7 | evaluation_metrics | "Furthermore, we notice a trend of increasing accuracy with larger models, with the exception of XGLM." |
| Q67 | 7 | evaluation_metrics | "For example, BLOOMZ (7B) achieves an accuracy 15.9 points higher than BLOOMZ (560M), while mT0 (13B) shows a 13.8-point increase compared to mT0 (300M)." |
| Q68 | 7 | task_taxonomy | "We observe that ArabicMMU questions are more challenging at the high school level compared to the primary and middle school levels." |
| Q69 | 7 | evaluation_metrics | "Specifically, for high school questions, GPT-4 achieves a score of only 61.7%, while Jais-chat scores 51.2%." |
| Q70 | 7 | evaluation_metrics | "Interestingly, we notice that the model accuracy at the university level is higher than for high school." |
| Q71 | 7 | stated_limitations | "This could be attributed to the relatively small portion (i.e., 6%) of university-level questions in ArabicMMU, which potentially skews the results." |
| Q72 | 7 | task_taxonomy | "We present the performance of open-source models on selected subjects that potentially contain Arabic-specific contexts." |
| Q73 | 7 | task_taxonomy | "These subjects include history, geography, civics, political" |
| Q74 | 8 | task_taxonomy | "We focus our more detailed analysis in this section solely on the best open-source models, namely BLOOMZ, AceGPT, and Jais, providing researchers and the community with insights to better understand these models and opportunities for future improvements." |
| Q75 | 8 | evaluation_metrics | "While all the results in Section 4.2 were based on zero-shot learning, we observe in Figure 7 that when we move to few-shot learning, results for base models improve but those for instruction-tuned models deteriorate." |
| Q76 | 8 | evaluation_metrics | "Specifically, AceGPT and Jais show an improvement of 2–10 points when using few-shot learning, but the results for BLOOMZ and Jais-chat drop." |
| Q77 | 8 | evaluation_metrics | "These findings are consistent with prior research over IndoMMIU (Koto et al., 2023) and CMMLU (Li et al., 2023)." |
| Q78 | 8 | evaluation_metrics | "We analyze whether BLOOMZ, AceGPT, and Jais are well-calibrated in answering ArabicMMLU questions by comparing the probability of the correct answers with the actual accuracy for each task (i.e., subject and level combination)." |
| Q79 | 8 | data_format | "The answer probability is obtained through softmax normalization across the available candidate answers." |
| Q80 | 8 | evaluation_metrics | "In Figure 8, we observe that the three open-source models are well calibrated with correlation scores r > 0.9." |
| Q81 | 8 | evaluation_metrics | "Additionally, we investigate the correlation between model confidence and question length in Figure 9." |
| Q82 | 8 | evaluation_metrics | "We find no correlation between the length of the questions and the model confidence for either Jais or AceGPT." |
| Q83 | 8 | stated_limitations | "Despite negation being an absolutely foundational linguistic phenomenon, LLMs have been shown to be worryingly insensitive to its effects in English (Kassner and Schütze, 2020; Hosseini et al., 2021; Truong et al., 2023)." |
| Q84 | 8 | task_taxonomy | "We thus perform an analysis of LLM performance over questions in ArabicMMLU with and without negation to determine whether this observation ports across to Arabic." |
| Q85 | 8 | data_format | "We utilize specific negation phrases to identify questions containing negations in Arabic." |
| Q86 | 9 | task_taxonomy | "We introduce ArabicMMLU, the first large-scale multi-task language understanding dataset designed to evaluate real-world knowledge in Arabic." |
| Q87 | 9 | data_sources | "Through experiments with over 14K multiple-choice questions spanning various subjects and education levels, we observed that Arabic-centric LLMs outperform multilingual LLMs, albeit with lower accuracy than GPT-4." |
| Q88 | 9 | task_taxonomy | "For future work, ArabicMMLU can be extended to include short-answer or essay questions, different modalities (i.e., images, audio, video), larger region coverage, and more questions in professional settings." |
| Q89 | 9 | stated_limitations | "ArabicMMLU does not represent all Arabic countries equally. For example, we have collected over 6K multiple-choice questions from Jordan, while other countries are represented with only 100 questions or, in some cases, not at all." |
| Q90 | 9 | stated_limitations | "This is largely due to the availability of publicly-accessible exams in each country; some countries have digitized their exams, but not others." |
| Q91 | 9 | stated_limitations | "Additionally, our search for relevant Arabic content across the internet was not exhaustive." |
| Q92 | 9 | stated_limitations | "The dataset primarily focuses on Modern Standard Arabic (MSA). However, multilingual and Arabic LLMs are often exposed to both MSA and dialectical Arabic." |
| Q93 | 9 | stated_limitations | "ArabicMMLU is focused solely on text-based assessment, and the exploration of multimodal questions is left for future work." |
| Q94 | 9 | stated_limitations | "It is important to emphasize that our experimental results do not provide conclusive answers regarding the performance of LLMs in Arabic." |
| Q95 | 10 | stated_limitations | "to a lack of sufficient information about its training regimen. As such, we cannot assert that the model's pretraining data is free from contamination." |
| Q96 | 10 | data_sources | "We extend our gratitude to all collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia who participated in the data collection process." |
| Q97 | 10 | authors_affiliations | "We also acknowledge the contributions of Samta Kamboj, Sarah Al Barri, and Onkar Pandit from Core42, who assisted in collecting the Arabic Language question dataset." |
| Q98 | 14 | data_sources | "Table 7 presents the distribution of ArabicMMLU data categorized by subject across different education levels." |
| Q99 | 14 | data_format | "Figure 10 illustrates a complete example of prompts used in this study. This example features a Natural Science question with prompts provided in both Arabic and English." |
| Q100 | 14 | task_taxonomy | "This is a Natural Science question for primary school in Jordan. Select the correct answer!" |
| Q101 | 14 | data_sources | "Table 7: The distribution of ArabicMMLU for each subject in different education levels." |
| Q102 | 15 | evaluation_metrics | "Table 8 presents the detailed zero-shot results across subjects and education levels, while Table 9, Table 10, Table 11 display the results with different prompts and alphabetic outputs (complementing the main result at Table 8)." |
| Q103 | 15 | evaluation_metrics | "Zero-shot LLM performance (% accuracy) with English prompt and English alphabetic output, for each subject and education level." |
| Q104 | 15 | task_taxonomy | "The models are BLOOMZ (7B), AceGPT-chat (13B), Jais-chat (30B), GPT-3.5 (175B), and GPT-4." |
| Q105 | 16 | evaluation_metrics | "Zero-shot LLM performance (% accuracy) with Arabic prompt and Arabic alphabetic output, combined across subject groups." |
| Q106 | 16 | evaluation_metrics | ""Average" means the average across all questions in ArabicMMLU." |
| Q107 | 16 | task_taxonomy | "Table 9 presents results organized by subject groups: STEM, Social Science, Humanities, Arabic Language, and Other." |
| Q108 | 17 | evaluation_metrics | "Zero-shot LLM performance (% accuracy) with Arabic prompt and English alphabetic output, combined across subject groups." |
| Q109 | 17 | task_taxonomy | "Table 10: Zero-shot LLM performance (% accuracy) with Arabic prompt and English alphabetic output, combined across subject groups." |
| Q110 | 18 | evaluation_metrics | "Zero-shot LLM performance (% accuracy) with English prompt and Arabic alphabetic output, combined across subject groups." |
| Q111 | 19 | authors_affiliations | "Table 12 lists the sources of pre-trained models used in this study. All models are sourced from Huggingface (Wolf et al., 2020)." |
| Q112 | 19 | authors_affiliations | "With the exception of GPT-3.5 and GPT-4, all the models used in this study were sourced from Huggingface (Wolf et al., 2020)." |

### Category Index
- **task_taxonomy**: Q10, Q12, Q24, Q25, Q28, Q68, Q72, Q73, Q74, Q84, Q86, Q88, Q100, Q104, Q107, Q109
- **data_sources**: Q1, Q17, Q22, Q23, Q26, Q31, Q32, Q34, Q87, Q96, Q98, Q101
- **data_format**: Q2, Q29, Q30, Q33, Q37, Q38, Q41, Q48, Q49, Q79, Q85, Q99
- **label_categories**: Q27
- **annotation_process**: Q35, Q36, Q39, Q40, Q42, Q43
- **evaluation_metrics**: Q3, Q4, Q21, Q45, Q46, Q47, Q50, Q51, Q52, Q53, Q54, Q55, Q56, Q57, Q58, Q59, Q60, Q61, Q62, Q63, Q66, Q67, Q69, Q70, Q75, Q76, Q77, Q78, Q80, Q81, Q82, Q102, Q103, Q105, Q106, Q108, Q110
- **stated_limitations**: Q5, Q6, Q7, Q44, Q64, Q65, Q71, Q83, Q89, Q90, Q91, Q92, Q93, Q94, Q95
- **authors_affiliations**: Q8, Q9, Q11, Q13, Q14, Q15, Q16, Q18, Q19, Q20, Q97, Q111, Q112
