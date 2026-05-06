```markdown
# Validity Extraction: ArabicMMLU: Evaluating Language Models on the Arabic Language and its Culture

<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: ArabicMMLU: Evaluating Language Models on the Arabic Language and its Culture
- **Authors**: Fajri Koto, Haonan Li, Sara Shatnawi, Jad Doughman, Abdelrahman Boda Sadallah, Aisha Alraeesi, Khalid Almubarak, Zaid Alyafeai, Neha Sengupta, Shady Shehata, Nizar Habash, Preslav Nakov, Timothy Baldwin
- **Venue/Year**: Not explicitly stated in registry (inferred as 2024 based on cited contemporaries)
- **Total Pages**: 19
- **Quotes Extracted**: 112

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

---

### 1. Task Taxonomy / Test Case Categories

ArabicMMLU is framed as a shift away from linguistically-centric NLP tasks (e.g., POS tagging, NER) toward knowledge and reasoning evaluation [Q10], following prior multilingual benchmarks that relied mainly on classification tasks [Q24]. The benchmark comprises 40 tasks organized around school subjects spanning primary, middle, and high school levels, with a smaller university-level component [Q25, Q28]. Subject groups include STEM, Social Science, Humanities, Arabic Language, and Other [Q107], and several subjects are specifically flagged as likely to contain Arabic-specific contexts — including history, geography, and civics [Q72, Q73]. For the deployment scenario, these subject groupings are broadly appropriate for school-curriculum-level tourist/expat knowledge, but the benchmark's structural limitation is visible in its difficulty gradient: high school questions are substantially harder than primary and middle school questions, and the university-level pool is only 6% of the dataset [Q68, Q71], meaning subject coverage is uneven across education levels. Future extensions proposed by the authors include short-answer and essay questions, multimodal inputs, larger regional coverage, and professional-domain content [Q88] — none of which are present in the current version, leaving significant gaps for deployment contexts requiring open-ended or explanatory responses. The benchmark's single-correct-answer MCQ structure also means that inherently multi-perspective tasks (e.g., contested historical or civic questions) are taxonomically collapsed into a single-answer frame, which is a critical mismatch for a deployment requiring acknowledgment of competing national narratives [Q84, Q100].

---

### 2. Data Sources and Collection

ArabicMMLU sources its 40 tasks from school examination materials collected across eight countries: Morocco and Egypt (North Africa), Jordan, Palestine, and Lebanon (the Levant), and UAE, Kuwait, and KSA (the Gulf) [Q26]. Data was gathered via a structured process in which 10 native Arabic-speaking workers — 6 internal and 4 external — identified publicly available URLs containing exam questions and then manually scraped metadata including source, country, subject, level, question text, options, and answer key [Q31, Q32, Q33, Q34]. Each external worker was assigned 2,000 questions and each internal worker 1,000–2,000 [Q34]. This sourcing approach is meaningfully distinct from translated benchmarks: existing Arabic evaluations largely rely on English-to-Arabic translation of MMLU [Q5, Q6], while ArabicMMLU explicitly draws on regionally and educationally authentic source material [Q1]. However, the distribution across countries is highly unequal — Jordan alone contributes over 6,000 questions, while some countries contribute as few as 100 [Q89, Q90], meaning Morocco and Palestine (both deployment-relevant countries) are likely underrepresented or absent in substantive numbers, even though both appear in the country list [Q26]. The availability of digitized public exams differs sharply across the region, and the authors acknowledge that their internet search was not exhaustive [Q90, Q91]. Acknowledgment of collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia [Q96] — but notably not Morocco or Palestine — further signals the geographic concentration of the data pipeline. Related multilingual and Arabic-centric benchmarks (XGLUE, XTREME, Dolphin, OCRA, LAraBench) [Q22, Q23] are positioned as prior work, not as data sources, and Jais's 72B-token Arabic pretraining corpus [Q17] is cited only for model context.

---

### 3. Data Format and Preprocessing

The benchmark consists of 14,575 multiple-choice questions in Modern Standard Arabic (MSA), with the number of candidate answers ranging from 2 to 5 per question [Q2, Q27]. A deliberate design choice was made to exclude questions in English and to include only Arabic-language questions [Q30], reflecting the educational reality that public schools in the target countries use Arabic for instruction and assessment, while international schools predominantly use English [Q29]. During scraping, workers were instructed to discard questions containing multimodal content (images, videos, tables) and to include contextual passages where needed alongside their dependent questions [Q37, Q38]. Automatic filtering removed duplicate questions and those lacking an answer key, reducing an initial pool of over 15,000 to 14,575 unique items [Q41]. For evaluation, prompts were constructed with structured placeholders for subject, level, country, question text, and answer options, available in both Arabic and English versions [Q49, Q99]. The text-only, MSA format aligns well with the deployment's text-based modality [Q93], but creates a signal-distribution gap for the target user population — non-native Arabic learners whose input Arabic may be imperfect, code-switched, or at learner register — since the benchmark assumes fluent MSA throughout [Q92]. Softmax normalization over candidate answers was used to derive answer probabilities for open-source models [Q79], and negation detection was implemented via specific Arabic negation phrases [Q85].

---

### 4. Label Categories and Output Types

The label schema is a single-correct-answer multiple-choice format: each question has between 2 and 5 candidate options, exactly one of which is marked as the correct answer [Q27]. This is the benchmark's only label type — there are no partial-credit labels, confidence tiers, or multi-answer categories documented in the registry. **For the deployment context, this output ontology is a high-priority mismatch.** The deployment explicitly requires that the system acknowledge multiple perspectives on contested historical and civic questions and flag country-specific answers rather than asserting a single universal truth [Q72, Q73]. The MCQ single-label structure structurally cannot capture contested, pluralistic, or regionally variable correct answers. For example, questions on Palestinian history, pan-Arab political geography, or events with competing national narratives would be forced into a single-answer frame that may reflect only one national curriculum's official position. The 96% verified accuracy ceiling on answer keys [Q43, Q44] provides a useful validity bound for what the benchmark can measure, but this ceiling applies only within the single-correct-answer paradigm and does not address the deeper issue that some "correct" answers are epistemically contested across the deployment's eight target countries.

---

### 5. Annotation Process

The annotation workforce consisted of 10 Arabic native speakers: Master's students and Research Assistants in Computer Science (internal workers) and Bachelor's degree holders (external workers) [Q35, Q39]. Workers received competitive compensation exceeding the monthly average wage in their respective countries [Q36], and a one-hour onboarding workshop was held before data collection to standardize procedures [Q40]. Quality was assessed post-hoc by having two native Arabic speakers independently verify 100 randomly sampled questions — including metadata and answer keys — using any available resources such as search engines; this yielded a 96% match rate, establishing a practical performance ceiling for the benchmark [Q42, Q43, Q44]. While the use of native speakers with formal educational backgrounds is a positive signal for linguistic validity, the annotator pool skews heavily toward Jordanian and Egyptian workers (1 Jordanian, 1 Egyptian, 1 Lebanese, 1 UAE, 2 KSA internally; 3 Jordanian and 1 Egyptian externally) [Q31], meaning Moroccan and Palestinian cultural perspectives on historically or civically sensitive content are not represented in the annotation or verification process — a gap that is directly relevant to the deployment's multi-perspective output requirement.

---

### 6. Evaluation Metrics and Output Modality

The benchmark evaluates 35 models in zero-shot and few-shot settings [Q45], spanning 22 open-source multilingual models, 11 open-source Arabic-centric models, and 2 closed-source models (GPT-3.5 and GPT-4) [Q46]. The primary metric is accuracy (percentage of correct MCQ answers) [Q3, Q4], with four prompt configurations tested — Arabic prompt/Arabic output, Arabic prompt/English output, English prompt/Arabic output, and English prompt/English output — to assess the effect of prompt language [Q47, Q55]. For open-source models, the answer is determined by the highest token probability among candidate option letters [Q50, Q51, Q52]; for closed-source models, by regex matching on the first generated token, with random assignment if no match is found [Q53, Q54]. The finding that an English prompt with English alphabetic output yields the best overall performance [Q56] — while Arabic-centric models are most robust with Arabic alphabetic output [Q57] — is notable for the deployment, since non-native Arabic learners may naturally produce English prompts and expect English-language explanations. Key performance results show that GPT-4 achieves 72.5%, Jais-chat (30B) achieves 62.3%, and models like BLOOMZ, mT0, LLaMA2, and Falcon fall below 50% [Q4, Q59, Q63]. The benchmark also reveals a high school difficulty spike (GPT-4 scores only 61.7% at high school level) [Q69] and reasonable model calibration (r > 0.9 for the three best open-source models) [Q80], while no correlation was found between question length and model confidence [Q82]. Additional analyses cover few-shot performance trends [Q75, Q76, Q77], scaling behavior [Q66, Q67], and negation sensitivity [Q84]. Crucially, because the output modality is discrete MCQ accuracy, the benchmark cannot evaluate whether a model provides appropriately nuanced, multi-perspective, or explanatory natural-language responses — a direct and high-priority mismatch with the deployment's output requirements [Q88].

---

### 7. Stated Limitations

The authors identify several limitations with direct bearing on deployment validity. The most fundamental is the reliance on MSA-only content: existing Arabic LLM evaluations depend on English-to-Arabic translations, which introduce Anglocentric biases and errors [Q5, Q6], and while ArabicMMLU corrects for this, it remains restricted to MSA and does not capture dialectal Arabic [Q92] — a limitation that affects both the deployment's learner-register users and the region's actual linguistic diversity. Geographic coverage is explicitly skewed: Jordan contributes over 6,000 questions while some countries contribute only ~100, driven by differential digitization of national exams [Q89, Q90], and the search was not exhaustive [Q91]. This is a critical gap for the deployment, as Morocco (Maghrebi curriculum, French-influenced educational tradition) and Palestine (politically sensitive historical narratives) are likely among the underrepresented countries despite being listed as source regions. The text-only scope leaves multimodal questions for future work [Q93], which is acceptable for this deployment but limits the benchmark's general scope. The 96% answer-key verification ceiling means up to 4% of questions may carry incorrect ground-truth labels [Q44]. A performance gap between GPT-4 on translated MMLU (80%) and on ArabicMMLU (72.5%) is noted and attributed to ArabicMMLU's higher proportion of Arabic-specific content [Q64, Q65] — a finding that supports the benchmark's construct validity for culturally grounded knowledge, but also signals that translation-based training data disadvantages models on authentic regional content. The authors also flag potential training data contamination as an unverifiable concern [Q95], and note that high school questions are disproportionately difficult relative to university-level questions, partly due to the small university-level sample (6%) [Q71]. Finally, LLMs' insensitivity to negation in English [Q83] is flagged as a phenomenon the paper investigates in Arabic, with implications for whether model failures reflect genuine knowledge gaps or surface linguistic sensitivity issues.

---

### 8. Authors and Affiliations

The paper's 13 authors [Q8] are primarily affiliated with the Mohamed bin Zayed University of Artificial Intelligence (MBZUAI) in Abu Dhabi, with additional affiliations at Prince Sattam bin Abdulaziz University (KSA), King Fahd University of Petroleum and Minerals (KSA), Core42 (UAE), New York University Abu Dhabi, and the University of Melbourne [Q9]. The institutional concentration in Gulf-region AI organizations (MBZUAI, Core42, KFUPM) is consistent with the benchmark's relatively stronger coverage of Gulf countries in its data sources. Additional acknowledgment is given to Core42 contributors for Arabic language question collection [Q97], and all open-source models were sourced through Hugging Face [Q111, Q112]. Background references to Arabic pretrained models such as AraBERT, CAMeLBERT, AraELECTRA, ARBERT, MARBERT [Q13], AraGPT2 [Q14], AraT5, AraBART [Q15], Jais [Q16], and AceGPT [Q16, Q18] position the authors as deeply embedded in the Arabic NLP research community, lending credibility to their design choices — while also highlighting that the community's institutional center of gravity lies in the Gulf rather than the Levant or Maghreb.
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
