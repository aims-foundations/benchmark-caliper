```markdown
# Validity Extraction: INJONGO — A Multicultural Intent Detection and Slot-Filling Dataset for African Languages
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: INJONGO — A Multicultural Intent Detection and Slot-Filling Dataset for African Languages
- **Authors**: Hao Yu, Jesujoba O. Alabi, Andiswa Bukula, Jian Yun Zhuang, En-Shiun Annie Lee, Tadesse Kebede Guge, Israel Abebe Azime, Happy Buzaaba, Blessing Kudzaishe Sibanda, Godson K. Kalipe, Jonathan Mukiibi, Salomon Kabongo Kabenamualu, Mmasibidi Setaka, Lolwethu Ndolela, Nkiruka Odu, Rooweither Mabuya, Shamsuddeen Hassan Muhammad, Salomey Osei, Sokhar Samb, Juliet W. Murage, Dietrich Klakow, David Ifeoluwa Adelani
- **Venue/Year**: Not explicitly stated in registry (paper appears to be a 2024/2025 preprint or conference submission)
- **Total Pages**: 24
- **Quotes Extracted**: 157

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

---

### 1. Task Taxonomy / Test Case Categories

INJONGO is a joint intent detection and slot-filling (ID-SF) benchmark targeting typologically diverse Sub-Saharan African languages and English [Q31], framing both tasks as the core natural language understanding components of task-oriented dialogue systems [Q2]. The tasks themselves are well-established: intent detection maps user requests to predefined semantic categories recognized by a dialogue manager, while slot-filling extracts specific entities from utterances [Q3]. The dataset covers 40 intent categories organized across five domains — Banking, Home, Travel, Utility, and Kitchen & Dining — for a total of 40 categories [Q117], and the 40 intents were selected from an original pool of 150 from the CLINC English dataset as best suited to African contexts [Q39].

For the Ethiopian utility deployment context, the Utility domain is the most directly relevant, but the benchmark's pan-African framing means this domain was designed to generalize across the continent rather than reflect the specific workflow of utilities like Ethiopian Electric Utility or Addis Ababa Water. Notably, the benchmark does not appear to include Ethiopian-specific intents such as prepaid STS token top-ups, mobile-money platforms (e.g., Telebirr, CBE Birr), or tiered-pricing disputes [Q107 flags that domains such as healthcare and education are explicitly acknowledged as missing, but utility-specific sub-intents are not discussed]. The closest comparable task in the African NLP ecosystem, MasakhaNER, covers named entity recognition but only four coarse entity types and lacks domain-specific depth in banking and travel [Q25], underscoring that INJONGO's slot ontology is a genuine advance. Experimental evaluation tests encoder-only, encoder-decoder, and LLM-based models [Q61], and cross-lingual transfer experiments explicitly compare African-centric (INJONGO) versus Western-centric (CLINC) English source data [Q101], directly relevant to understanding whether the Ethiopian utility deployment can benefit from African-context training data. The benchmark also includes a named-entity extraction formulation for slot-filling [Q147, Q148], and provides annotator guidelines defining the task as extracting predefined slot categories from user inputs [Q150, Q151].

---

### 2. Data Sources and Collection

INJONGO is described as the first large-scale multicultural intent detection and slot-filling dataset covering 16 African languages plus English [Q4], with 3,200 annotated utterances per African language across 5 domains, 40 intents, and 23 slots [Q18]. The 16 languages span two dominant African language families — 13 from Niger-Congo and 3 from Afro-Asiatic — and represent a speaker range from Swahili (98 million speakers) to Wolof (5 million speakers) [Q33, Q34]. Amharic, as an Afro-Asiatic language and one of the three Afro-Asiatic languages in the dataset, is thus included, though its coverage is proportionally narrow within the 16-language sweep.

Data collection was deliberately designed to avoid the two common pitfalls of prior multilingual NLU datasets: the translationese effect and cultural irrelevance [Q13]. Rather than translating English utterances, annotators were provided with sample CLINC sentences for a given intent and asked to generate culturally relevant utterances in their own language with locally appropriate slot entities [Q37]. For example, a Xhosa annotator replaced generic currency and bank references with South African-specific entities (Rand, FNB, Absa) [Q40, Q41] — illustrating the cultural grounding principle, though it is an open question whether the Amharic annotators similarly substituted Ethiopian utility-specific entities (e.g., Telebirr, Ethiopian Electric Utility account codes). The English portion of the dataset was assembled from the practice utterances generated by annotators across all languages, yielding 1,779 English utterances [Q58, Q59], and a 4,000-instance sample from CLINC was retained for direct Western-centric vs. African-centric comparison [Q60]. The dataset was complemented by NLLB-200-3.3B machine translation for translate-test evaluation [Q75], and training data for supervised fine-tuning was constructed by aggregating all 17 languages' training splits [Q128]. Performance disparities across languages are partly attributed to differences in monolingual web data availability [Q88], with Swahili's 1 billion+ monolingual tokens enabling near-English LLM performance [Q89] — a factor that likely disadvantages Amharic relative to Swahili in zero-shot LLM settings.

**Critical gap for Ethiopian deployment**: The dataset explicitly notes that the MASSIVE benchmark (the prior state-of-the-art multilingual NLU dataset) included only three African languages — Amharic, Afrikaans, and Swahili — and that many utterances in MASSIVE remained culturally irrelevant even after entity substitution efforts [Q14]. INJONGO was designed to address this, but whether the Amharic split reflects code-switching with English (confirmed as common in Ethiopia [Q2 from elicitation]) or regional dialect variation (Oromo/Tigrinya interference in Dire Dawa, Hawassa, Mekelle) is not documented in the paper. The paper notes that "limited available labeled datasets are one of the major challenges of AfricaNLP" [Q24], and the selected languages "represent diverse linguistic families and are widely spoken" [Q32], but does not characterize intra-language regional or sociolinguistic variation within the Amharic split.

---

### 3. Data Format and Preprocessing

The dataset construction proceeds in two stages: (1) utterance elicitation in an African language and (2) slot-filling annotation of the generated utterance [Q38], with annotations performed on the LabelStudio platform following a named entity recognition setup [Q43]. The dataset is released under a CC BY 4.0 license [Q23] and partitioned into 70% train, 10% dev, and 20% test splits stratified by intent for each language [Q57].

Preprocessing involved analysis of entity frequency distributions across all languages, with slot entities appearing fewer than 500 times excluded [Q51], reducing the slot type inventory from 34 to 23 by merging similar or low-frequency types [Q55, Q119]. Nine infrequent slot types (from NATIONALITY through PLUG TYPE) were eliminated in this step [Q52]. The final 23 slot types are listed in the appendix [Q144], and include types highly relevant to the Ethiopian utility context such as MONEY, PAYMENT_COMPANY, ACCOUNT_TYPE, BANK_NAME, and CITY_OR_PROVINCE, as well as PLACE_NAME — though the granularity of address-type slots (kebele numbers, informal neighborhood names) is not documented.

For the deployment context, the benchmark is text-only, which matches the Telegram/SMS channels. The paper documents inference infrastructure for both closed-source (API calls to GPT-4o, Gemini 1.5 Pro [Q131]) and open-source models (vLLM, TGI [Q132]), all under FP32 precision on NVIDIA H100/L40S GPUs [Q129]. An illustrative output format uses `$$` as a separator between entity type and value [Q146], and prompts are described as language-specific and tailored to task requirements [Q138]. Whether the Amharic data was collected and stored in normalized Unicode Ge'ez (Ethiopic) script — critical for tokenizer compatibility with Telegram inputs — is not explicitly confirmed in the registry; the paper does not document script normalization procedures.

---

### 4. Label Categories and Output Types

The label ontology for slot-filling was initially 34 slot types [Q118], reduced to 23 final slot types after merging and frequency filtering [Q54, Q119]. The full final set of 23 named entity types is enumerated in the appendix [Q144]: ACCOUNT_TYPE, ARTIST_NAME, BANK_NAME, BILL_TYPE, CALENDAR_EVENT, CITY_OR_PROVINCE, COUNTRY, CURRENCY, DATE, DISH_OR_FOOD, HOTEL_NAME, LANGUAGE_NAME, MEAL_PERIOD, MONEY, MUSIC_GENRE, NUMBER, PAYMENT_COMPANY, PERSONAL_NAME, PLACE_NAME, RESTAURANT_NAME, SHOPPING_ITEM, SONG_NAME, TIME.

For the Ethiopian utility deployment, several slot types are directly relevant (ACCOUNT_TYPE, BANK_NAME, MONEY, PAYMENT_COMPANY, CITY_OR_PROVINCE, PLACE_NAME), but the ontology lacks a dedicated METER_ID, UTILITY_ACCOUNT_NUMBER, or ADDRESS_SUBUNIT slot type that would capture kebele numbers or neighborhood-level administrative units important for Ethiopian utility billing. The annotation guide provides specific disambiguation rules: temporal spans under one day should be labeled TIME and longer spans DATE [Q153, Q154]; bank name annotation excludes the word "bank" unless it is part of the proper name (e.g., "Ecobank") [Q152]; and bill-type annotation includes the word "bill" as part of the span [Q155]. These rules reflect general banking and utility conventions but do not document Ethiopian-specific naming conventions for utility payment types or local payment platforms. The 40 intent categories across 5 domains are listed in the appendix [Q117], but specific intent labels are not enumerated in the registry beyond domain-level examples such as "transfer," "pay bill," "exchange rate," and "book flight" [Q39].

---

### 5. Annotation Process

Utterances were generated by native speakers across diverse domains [Q7], with each utterance annotated by three independent annotators to enable agreement checking [Q42]. All recruited participants received remuneration based on per-country rates determined by a logistics company in Kenya [Q44]. Quality control used majority voting with a minimum of three annotators per sentence to resolve disagreements [Q45], and the process required two rounds of review to achieve consistent quality [Q109].

Initial Fleiss' Kappa scores varied substantially across languages, from 0.618 (Zulu) to 0.934 (Shona) [Q47], indicating that annotation difficulty differed meaningfully by language. After the review process, scores improved to 0.912–1.00 across all languages [Q48], with the largest gains in Sesotho (+0.327) and Zulu (+0.294) and average improvements of approximately 0.1 elsewhere [Q49]. Ambiguous slot types were identified as a significant source of disagreement [Q53]. The annotation guide instructs annotators to only label explicitly named place entities (e.g., named airports or malls, not generic references to "mall" or "airport") [Q156] and not to skip any utterance even if no entities are present [Q157]. The complete annotation guide for all slot types is included in the appendix [Q149].

For the Ethiopian utility deployment, a critical validity concern is the representativeness of the Amharic annotators. The paper confirms that native speakers were used and that remuneration was managed through a Kenya-based logistics company [Q44], but does not specify whether Amharic annotators had domain familiarity with Ethiopian utility billing terminology (meter accounts, prepaid token workflows, Telebirr transactions). The standard Fleiss' Kappa reporting does not break out inter-annotator agreement by language in the main text in sufficient detail to determine whether the Amharic split achieved high or low initial agreement, though the post-review range of 0.912–1.00 applies across all languages [Q48]. The lack of documentation on whether utility-domain utterances were validated by agents or billing staff — rather than only general native-speaker crowdworkers — is a gap directly flagged by the deployment context.

---

### 6. Evaluation Metrics and Output Modality

The benchmark evaluates intent detection using accuracy and slot-filling using F1-score [Q84], with results averaged over five random seeds for fine-tuning runs [Q63] and five prompting templates for LLM evaluations [Q73]. The best fine-tuning baseline (AfroXLMR-76L) achieves an average accuracy of 93.7% for intent detection and an F1 of 85.6% for slot-filling [Q78, Q19], while zero-shot GPT-4o achieves only 26% F1 for slot-filling [Q9] and 70.6% average accuracy for intent detection across African languages [Q10] — compared to approximately 81% on English [Q11], a gap of over 10 percentage points.

The LLM evaluation framework is extensive: seven models are benchmarked in zero-shot settings [Q65], with five prompting templates per model [Q66] and three few-shot strategies (5-examples, 1-shot/40 examples, 4-shots/160 examples) [Q68]. Few-shot prompting yields substantial gains, especially for slot-filling: GPT-4o and Gemini 1.5 Pro improve by more than 19 F1 points with only 5 examples [Q91], and Gemma 2 9B improves from 2.4 to 33.5 F1 [Q92]. Supervised fine-tuning on Gemma 2 9B (52k samples) still outperforms 4-shot prompting by +15.8 accuracy and +34.1 F1 [Q98], confirming that having training data remains critical for low-resource languages [Q85]. Cross-lingual transfer experiments directly compare African-centric (INJONGO) vs. Western-centric (CLINC) English source data, finding that INJONGO in-language cross-lingual transfer outperforms CLINC at 10-shot (16.1 vs. 4.0 accuracy gain) and in translate-test at the same shot count (+29 accuracy gain) [Q102, Q103], though at 25+ shots the advantage diminishes [Q104]. Training protocol details include AdamW optimization, 20 epochs, 10% linear warmup with linear decay, early stopping (patience=5) [Q122, Q123], and learning rates calibrated per architecture [Q124, Q125]. The annotation quality metric (Fleiss' Kappa) is also reported as part of the evaluation framework [Q46].

---

### 7. Stated Limitations

The authors explicitly acknowledge that existing large-scale benchmarks for intent detection and slot-filling "often exclude evaluations of low-resource languages and rely on translations from English benchmarks, thereby predominantly reflecting Western-centric concepts" [Q12] — and that INJONGO was designed to address this gap. Two persistent structural challenges are noted: the translationese effect (utterances sounding unnatural in target languages) and cultural irrelevance of translated content [Q13], both of which INJONGO's elicitation-based design attempts to mitigate.

Domain coverage is explicitly limited to five domains, and the authors acknowledge that "healthcare and education" are absent but "essential for real-world applications" [Q107]. For the Ethiopian utility deployment, this is a relevant gap: while a Utility domain exists, sub-intents specific to Ethiopian prepaid meter top-ups, mobile-money platforms, or outage reporting are not documented. Language coverage is also described as incomplete: INJONGO covers only a fraction of Africa's linguistic diversity and "particularly lacks representation from other language families such as Nilo-Saharan languages" [Q108]. The dataset size of 3,200 examples per language is acknowledged as "modest compared to high-resource benchmarks" and potentially limiting for model performance [Q110], and the fixed uniform distribution across intents "may not accurately reflect the natural frequency of these interactions in real-world conversations" [Q111].

Performance limitations for LLMs are prominently documented. Slot-filling is described as "difficult for all LLMs including on English," with the highest average LLM performance at 33.3% F1 (GPT-4o) [Q85]. Intent detection failure for open models is attributed to either a lack of African language exposure or the large 40-label classification space [Q86]. Open models are described as "more biased toward high-resource languages" — performing competitively with closed models on English but lagging significantly on African languages [Q87]. Models not pre-trained on some INJONGO languages (e.g., ewe, twi, lin, wol) show significant performance drops [Q81], directly relevant for assessing Amharic-specific model behavior. The lack of labeled data for AfricaNLP is cited as a persistent challenge [Q24], and the authors explicitly recommend "more work is needed to further improve downstream performance" for low-resource African languages [Q15, Q22]. The annotation process itself revealed ambiguous slot types as a significant quality challenge [Q53], and the cost and scalability constraints of native-speaker elicitation are acknowledged [Q28, Q36]. The observation that model success correlates with pre-training language coverage [Q79] has direct implications for whether currently available multilingual models can reliably serve Amharic utility users. Finally, while few-shot LLM prompting is "very crucial and effective when training data are scarce" [Q100], the gap with supervised fine-tuning remains large [Q97], and code-switching — confirmed as frequent in the Ethiopian target population — is not documented as a design criterion or addressed in the limitations section.

---

### 8. Authors and Affiliations

The author list is large and geographically diverse [Q16], with affiliations spanning Mila/McGill University and Canada CIFAR AI Chair (Hao Yu, David Adelani), Saarland University Germany (Alabi, Klakow, Azime), SADiLaR South Africa (Bukula, Setaka, Mabuya), University of Toronto and OntarioTech University Canada (Zhuang, Lee), Princeton University USA (Buzaaba), Makerere University Uganda (Mukiibi), L3S Research Center Germany (Kabenamualu), Imperial College London UK (Muhammad), Universidad de Deusto Spain (Osei), and DAUST Senegal (Samb) [Q17]. A substantial number of authors are affiliated with Masakhane NLP [Q16], a well-known African NLP community organization, which explains the pan-African focus and native-speaker-driven design philosophy. The presence of Ethiopian co-author Tadesse Kebede Guge (affiliated with Masakhane NLP) is relevant to the Amharic deployment context, as it suggests Ethiopian native-speaker involvement in dataset design, though the depth of that involvement in the Amharic utility sub-domain is not documented in the registry.
```

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | task_taxonomy | "Slot-filling and intent detection are well-established tasks in Conversational AI." |
| Q2 | 1 | task_taxonomy | "Intent detection and slot-filling are crucial components of the natural language understanding module in task-oriented dialogue systems (Hemphill et al., 1990; Coucke et al., 2018; Gupta et al., 2018)." |
| Q3 | 1 | task_taxonomy | "They map a user's request to a predefined semantic category recognized by the dialogue manager, along with extracting specific entities (known as slots)." |
| Q4 | 1 | data_sources | "We develop INJONGO—the first large-scale multicultural intent detection and slot-filling dataset covering 16 African languages, and English language." |
| Q5 | 1 | data_sources | "We cover the following five domains: banking, home, travel, utility, and kitchen & dining." |
| Q6 | 1 | data_format | "The data construction process starts with providing an annotator with sentences from the CLINC dataset (Larson et al., 2019a) with a specified intent type, and they are to come up with culturally-relevant similar sentences and relevant slot entities (see Figure 1)." |
| Q7 | 1 | annotation_process | "utterances generated by native speakers across diverse domains, including banking, travel, home, and dining." |
| Q8 | 1 | evaluation_metrics | "Through extensive experiments, we benchmark the fine-tuning multilingual transformer models and the prompting large language models (LLMs), and show the advantage of leveraging African-cultural utterances over Western-centric utterances for improving cross-lingual transfer from the English language." |
| Q9 | 1 | evaluation_metrics | "Experimental results reveal that current LLMs struggle with the slot-filling task, with GPT-4o achieving an average performance of 26% F1-score." |
| Q10 | 1 | evaluation_metrics | "In contrast, intent detection performance is notably better, with an average accuracy of 70.6%, though it still falls behind the fine-tuning baselines." |
| Q11 | 1 | evaluation_metrics | "When compared to the English language, GPT-4o and fine-tuning baselines perform similarly on intent detection, achieving an accuracy of approximately 81%." |
| Q12 | 1 | stated_limitations | "current large-scale benchmarks for these tasks often exclude evaluations of low-resource languages and rely on translations from English benchmarks, thereby predominantly reflecting Western-centric concepts." |
| Q13 | 1 | stated_limitations | "However, these efforts face two key challenges: (1) the translationese effect, which makes utterances sound less natural in the target languages (Vanmassenhove et al., 2021; Bizzoni et al., 2020), and (2) the creation of utterances that are less culturally relevant." |
| Q14 | 1 | stated_limitations | "Despite improvements in the utterance generation process, MASSIVE includes only three African languages (Amharic, Afrikaans and Swahili), and many utterances remain culturally irrelevant to the target language communities." |
| Q15 | 1 | stated_limitations | "Our findings suggest that the performance of LLMs is still behind for many low-resource African languages, and more work is needed to further improve their downstream performance." |
| Q16 | 1 | authors_affiliations | "Hao Yu1, Jesujoba O. Alabi3,∗, Andiswa Bukula4,∗, Jian Yun Zhuang5, En-Shiun Annie Lee6, Tadesse Kebede Guge∗, Israel Abebe Azime3, Happy Buzaaba7,∗, Blessing Kudzaishe Sibanda∗, Godson K. Kalipe∗, Jonathan Mukiibi8,∗, Salomon Kabongo Kabenamualu9,∗, Mmasibidi Setaka4, Lolwethu Ndolela∗, Nkiruka Odu∗, Rooweither Mabuya4,∗, Shamsuddeen Hassan Muhammad10,∗, Salomey Osei11, Sokhar Samb12, Juliet W. Murage∗, Dietrich Klakow3, David Ifeoluwa Adelani1,2,∗" |
| Q17 | 1 | authors_affiliations | "∗Masakhane NLP, 1Mila - Quebec AI Institute & McGill University, Canada, 2Canada CIFAR AI Chair, 3Saarland University, Germany, 4SADiLaR, South Africa, 5University of Toronto, Canada, 6 OntarioTech University, Canada, 7Princeton University, USA, 8Makerere University, Uganda, 9L3S Research Center, Germany, 10Imperial College London, United Kingdom, 11Universidad de Deusto, Spain, 12DAUST, Senegal." |
| Q18 | 2 | data_sources | "INJONGO dataset covers 5 domains, 40 intents, 23 slots, and 3,200 instances per African language." |
| Q19 | 2 | evaluation_metrics | "Our result shows that fine-tuning baselines could reach an accuracy of 93.7% and F1-score of 85.6 for intent detection and slot-filling tasks respectively." |
| Q20 | 2 | evaluation_metrics | "While the best prompting of LLMs results (GPT-4o) drops by -28% accuracy point and −52.6 F1 score." |
| Q21 | 2 | stated_limitations | "While slot-filling and named entity recognition tasks are often challenging for LLMs even for English (Yu et al., 2023), intent detection performance in English is similar performance whether we use fine-tuning baselines or prompt GPT-4o." |
| Q22 | 2 | stated_limitations | "Our findings suggest that LLMs performance is still behind for many low-resource African languages, and more work is needed to further improve their downstream performance." |
| Q23 | 2 | data_format | "Dataset is released under CC BY 4.0 license." |
| Q24 | 2 | stated_limitations | "Limited available labeled datasets are one of the major challenges of AfricaNLP." |
| Q25 | 2 | task_taxonomy | "The closest benchmark to our task of slot-filling is MasakhaNER (Adelani et al., 2021, 2022) that covers 20 African languages but they focus on four entity types "personal names", "organization", "location", and "dates", which are not fine-grained and well adapted to several domains such as banking and travel that we cover in INJONGO." |
| Q26 | 2 | stated_limitations | "Most of the existing benchmarks for intent detection and slot-filling tasks are English-only." |
| Q27 | 2 | data_sources | "There are a few efforts to make them multilingual in two ways: (1) human generating the utterances in a particular domain, followed by intent and slot filling annotation. (2) through human translation of annotated data from English to other languages which introduces some cultural bias since Western entities are being propagated." |
| Q28 | 2 | stated_limitations | "While the first approach is the most ideal methodology, it is very cost-intensive when scaling to many languages." |
| Q29 | 2 | stated_limitations | "MASSIVE benchmark partially addresses this Western cultural bias by encouraging translators to replace entities with more culturally relevant ones, but Western entities are still prevalent in the dataset." |
| Q30 | 2 | data_sources | "In our paper, we introduce INJONGO which is the largest intent detection and slot-filling dataset covering 16 African languages, and we ensured that the slot entities are more culturally relevant in the respective countries the languages are from." |
| Q31 | 2 | task_taxonomy | "INJONGO is a joint intent detection and slot-filling dataset (ID-SF) for typologically diverse Sub-Saharan African languages and English." |
| Q32 | 2 | data_sources | "The selected languages represent diverse linguistic families and are widely spoken in Africa." |
| Q33 | 2 | data_sources | "These languages come from the two dominant language families in Africa: 13 from Niger-Congo and three from Afro-Asiatic." |
| Q34 | 2 | data_sources | "The languages covered are spoken by a large population in Africa, ranging from Swahili with 98M speakers to Wolof with 5M speakers." |
| Q35 | 3 | data_sources | "Typical ID-SF data collection often requires large crowd-sourcing efforts to collect utterances, with additional labeling of intents and slots in various domains." |
| Q36 | 3 | stated_limitations | "Developing such a large crowd-sourcing effort is time-consuming and costly for several low-resource languages." |
| Q37 | 3 | data_sources | "To simplify the process while making the dataset cultural, we provide each annotator with sample sentences from the CLINC dataset (Larson et al., 2019a) with a specified intent type, say "transfer"." |
| Q38 | 3 | data_format | "Then, the dataset construction follows two stages: (1) Utterance elicitation in an African language and (2) Slot-filling annotation of the generated utterance." |
| Q39 | 3 | data_sources | "The source data for our multilingual benchmark is from the CLINC English dataset—an intent detection with 150 intent classes across 10 domains (but without slot annotation), we extracted 40 intents from five most suitable domains to the African contexts: Banking (e.g. "transfer", "pay bill"), Home (e.g. "play music", "calendar update"), Kitchen and Dining (e.g. "recipe", "confirm reservation"), Travel (e.g. "exchange rate", "book flight"), and Utility (e.g." |
| Q40 | 3 | annotation_process | "A Xhosa annotator was asked to generate another utterance belonging to the same intent type but capturing the South African context where the language is spoken." |
| Q41 | 3 | data_format | "Thus, the annotator used the R200 as "money" with currency Rand (R), and more familiar South African banks such as "FNB" and "Absa" for "bank name" slot." |
| Q42 | 4 | annotation_process | "Each utterance was annotated by three annotators so that we could check for agreement in the slot annotations." |
| Q43 | 4 | data_format | "The annotation followed the named entity recognition setup on LabelStudio platform." |
| Q44 | 4 | annotation_process | "For both utterance elicitation and slot-filling annotation, all recruited participants received an appropriate remuneration based on the per-country rate decided by our logistics company in Kenya." |
| Q45 | 4 | annotation_process | "To ensure annotation quality and consistency, we follow a rigorous quality control process using a majority voting system with a minimum of three annotators per sentence to resolve disagreements." |
| Q46 | 4 | evaluation_metrics | "The annotation quality was evaluated using Fleiss' Kappa score (Fleiss, 1971), with scores presented in Table 3 comparing agreement levels before and after the review process." |
| Q47 | 4 | annotation_process | "Initial Fleiss' Kappa scores revealed substantial variation across languages, ranging from 0.618 (Zulu) to 0.934 (Shona), indicating significant inter-annotator disagreement." |
| Q48 | 4 | annotation_process | "Following the review process, agreement scores improved markedly across all languages, reaching 0.912-1.00." |
| Q49 | 4 | annotation_process | "Notable improvements were observed in Sesotho (+0.327) and Zulu (+0.294), with other languages showing average improvements of approximately 0.1 in their Fless' Kappa scores." |
| Q50 | 4 | data_format | "We performed an analysis of entity frequency distribution across all languages." |
| Q51 | 4 | data_format | "We decided to exclude slot entities appearing less than 500 times across all languages (after MUSIC GENRE in the figure)." |
| Q52 | 4 | data_format | "Consequently, nine infrequent slots from NATIONALITY through PLUG TYPE were eliminated." |
| Q53 | 4 | stated_limitations | "Examination of annotator feedback and comparative analysis between unreviewed and reviewed versions indicated that ambiguous slot types significantly impacted annotation quality and introduced unnecessary complexity." |
| Q54 | 4 | label_categories | "Appendix A.2 contains all 34 slot types selected." |
| Q55 | 5 | data_format | "This merging process resulted in a reduction from 34 to 23 slot types." |
| Q56 | 5 | data_sources | "Our final annotation resulted in 3,200 annotated utterances, with 80 utterances per intent for each of the 16 African languages." |
| Q57 | 5 | data_format | "The dataset is partitioned following ratios of 70%, 10%, and 20% for train, dev, and test splits respectively, stratified by intent for each language." |
| Q58 | 5 | data_sources | "Additionally, we aggregated the practice utterances generated and the practice slot annotations as the English dataset, leading to 17 annotated languages." |
| Q59 | 5 | data_sources | "In total, the English consist of 1779 utterances." |
| Q60 | 5 | data_sources | "Finally, we sampled 4000 CLINC intent-only dataset to compare westerncentric English dataset to our curated INJONGO dataset that captures the African contexts." |
| Q61 | 5 | task_taxonomy | "We evaluate three categories of models: (1) encoder-only models such as XLM-RoBERTa Large (Conneau et al., 2019), AfroXLMR (Alabi et al., 2022), AfroXLMR-76L (Adelani et al., 2023a), AfriBERTa V2 (Oladipo, 2024), (2) encoder-decoder models such as mT5-Large (Xue et al., 2020), AfriTeVa V2 Large (Oladipo et al., 2023), and (3) a multilingual variant of LLM2Vec model (BehnamGhader et al., 2024) i.e. NLLB-LLM2Vec (Schmidt et al., 2024) that stack NLLB-encoder (NLLB Team et al., 2022) model with LLaMa 3.1 8B (Grattafiori et al., 2024) to develop a multilingual sentence transformer model." |
| Q62 | 5 | evaluation_metrics | "These models are fine-tuned using the AdamW optimizer for 20 epochs with early stopping." |
| Q63 | 5 | evaluation_metrics | "All results are averaged over five seeds." |
| Q64 | 5 | evaluation_metrics | "Learning rates are calibrated for each architecture and task as detailed in Appendix B.2." |
| Q65 | 5 | evaluation_metrics | "First, we conduct zero-shot prompting using the following widely used LLMs for evaluation: GPT4o, Gemini 1.5 Pro (Reid et al., 2024), Gemma 2 9B/27B Instruct (Team et al., 2024), Llama 3.1 8B/3.3 70B Instruct (Grattafiori et al., 2024), and Aya-101 (Üstün et al., 2024)." |
| Q66 | 5 | evaluation_metrics | "We make use of five different prompts for each LLM." |
| Q67 | 6 | evaluation_metrics | "we perform few-shot evaluation using the best-performing zero-shot template for each task (see Appendix C)." |
| Q68 | 6 | evaluation_metrics | "We employ two few-shot strategies (1) 5-examples: prompting with any 5 samples from different domains (see Figure 1) i.e. one intent type is covered by domain (2) One-shot intent-type prompting i.e. one sample per intent type or 40 samples from different intent types." |
| Q69 | 6 | evaluation_metrics | "We used the same samples for both tasks." |
| Q70 | 6 | evaluation_metrics | "Finally, we extend to 4 shots—acceptable maximum context length (CL) for Gemma 2, Aya-101 was excluded for small CL." |
| Q71 | 6 | task_taxonomy | "Finally, as an additional strong baseline for LLMs, we performed supervised fine-tuning (SFT) on Gemma 2 9B for 5 epochs using learning rates of 2 × 10−5/ 2.5 × 10−5for intent detection and slot filling." |
| Q72 | 6 | data_sources | "The dataset of SFT was obtained by aggregating all the training samples of the 17 languages in INJONGO i.e. "Combined INJONGO", with randomly sampled prompts from a pool of 5." |
| Q73 | 6 | evaluation_metrics | "The evaluations of LLMs use 5 different prompting templates and a temperature of 0.5." |
| Q74 | 6 | task_taxonomy | "To investigate how well our dataset facilitates cross-lingual learning and transfer capabilities across languages, we tested two settings (1) zero-shot transfer from the English split of INJONGO, and evaluated on African languages. (2) Translate-Test where we evaluate on the machine-translated sentence test sets from an African language to English." |
| Q75 | 6 | data_sources | "We leveraged the NLLB-200-3.3B (NLLB Team et al., 2022) machine translation model for the Translate-test setting." |
| Q76 | 6 | evaluation_metrics | "Experiments of the baselines and cross-lingual transfer runs make use of five fixed random seeds." |
| Q77 | 6 | evaluation_metrics | "Table 5 summarizes the results of the multilingual encoders fine-tuned INJONGO dataset." |
| Q78 | 6 | evaluation_metrics | "Overall, AfroXLMR-76L achieves the best performance on both ID-SF tasks, with an average accuracy of 93.7% and an F1 score of 85.6%, respectively." |
| Q79 | 6 | stated_limitations | "We attribute the success of this model to the coverage of all languages in INJONGO during its pre-training (see Appendix Table 11)." |
| Q80 | 6 | evaluation_metrics | "AfroXLMR, the earlier version of AfroXLMR-76L, follows closely with an average accuracy of 92.2% and an F1 score of 85.2%." |
| Q81 | 6 | stated_limitations | "However, this model was not pre-trained on some of the languages such as ewe, twi, lin, and wol leading to a significant drop in performance of −5.8, −4.8, −1.3, −0.4 for intent detection when compared to AfroXLMR-76L." |
| Q82 | 6 | stated_limitations | "This shows that multilingual encoders for African languages can significantly improve the performance over massively multilingual encoders covering more than 100 languages such as XLM-R and NLLB LLM2Vec." |
| Q83 | 7 | evaluation_metrics | "Table 6 shows the zero-shot LLM evaluation of five open models and two closed models." |
| Q84 | 7 | evaluation_metrics | "Evaluation is based on accuracy and F1-score for ID and SF tasks. Average computed on five templates, and on only African languages." |
| Q85 | 7 | stated_limitations | "Slot-filling task is difficult for all LLMs including on English The highest average performance achieved by the LLMs is 33.3% for GPT-4o, although much better than the open model at 28.8. We attribute this to the difficulty of LLMs on the named entity recognition task as reported by other researchers (Yu et al., 2023; Ojo et al., 2023). In comparison to the best-finetuned model, there is a large drop in performance of −53.2. This shows that having training data is still relevant for this task even in the LLM era, especially for low-resource languages." |
| Q86 | 7 | stated_limitations | "For intent detection, we find that all open models achieved below 50% on the relatively easy task of intent detection. The poor performance may be attributed to either a lack of exposure to many African languages or the large label space (i.e. 40) for the classification task." |
| Q87 | 7 | stated_limitations | "The closed models result are better, with GPT-4o and Gemini 1.5 Pro achieving more than +20 points than the best open model, Llama 3.3 70B. However, if we compare the results in the English language, open models such as Gemma 2 27B and Llama 3.3 70B are competitive with closed models. This shows that open models are more biased toward high-resource languages." |
| Q88 | 7 | data_sources | "The performance of some African languages is often higher than others, this is probably connected to the amount of monolingual data available on the web." |
| Q89 | 7 | data_sources | "For example, Swahili (swa) with over 1 billion monolingual data (Kudugunta et al., 2023) has 80.6 accuracy point that is comparable performance to English performance (81.1) with Llama 3.3 70B, while other languages have much lower performance." |
| Q90 | 8 | evaluation_metrics | "Figure 3 shows the result of the various few-shot setups: 5-examples, 1-shot (40 examples, one from each intent type), and 4-shots (160 examples)." |
| Q91 | 8 | evaluation_metrics | "Our result shows a big boost in performance with only 5-examples, especially for the slot-filling task and some LLMs: GPT-4o and Gemini 1.5 Pro improved the most by more than +19 points." |
| Q92 | 8 | evaluation_metrics | "Similarly, Gemma 2 9B improved from 2.4 to 33.5 matching the performance of Llama 3.3 70B (with 5-examples)." |
| Q93 | 8 | evaluation_metrics | "Additional samples from 1-shot and 4-shot consistently improved performance for all models except Llama 3.3 70B." |
| Q94 | 8 | evaluation_metrics | "We find Gemini 1.5 Pro, Gemma 2 9B and Gemma 2 27B to benefit the most from 5-examples, with an accuracy boost of +14.3, +15.7, and +21.8 respectively." |
| Q95 | 8 | evaluation_metrics | "While the zero-shot performance of Gemini 1.5 Pro is worse than GPT-4o, the few-shot performance exceeds that of GPT-4o with +1.8 and +2.3 improvement in 5-examples and 1-shot." |
| Q96 | 8 | evaluation_metrics | "Our result shows the effectiveness of LLMs in adapting quickly to a new task in low-resource settings." |
| Q97 | 8 | stated_limitations | "While all LLMs improve performance with more shots, there is still a large gap with SFT." |
| Q98 | 8 | evaluation_metrics | "We performed SFT on Gemma 2 9B with all training samples and prompt templates, we found a large performance gap of +15.8 and +34.1 for intent detection and slot-filling respectively if we compare SFT (52k samples) to 4-shots (160 examples)." |
| Q99 | 8 | stated_limitations | "However, for closed models, the gap of SFT on Gemma 2 9B to Gemini 1.5 Pro and GPT-4o is much smaller, especially for intent detection." |
| Q100 | 8 | stated_limitations | "In general, few-shots of LLMs are still worse than SFT but are very crucial and effective when training data are scarce." |
| Q101 | 8 | task_taxonomy | "Figure 4 shows our final experiments that compare cross-lingual transfer results from two English datasets: CLINC (Western-centric) and INJONGO (African-centric) on the intent detection task." |
| Q102 | 8 | evaluation_metrics | "At 5-shots, in both in-language and translate-test settings, the accuracy of all settings is quite similar, however as we increase the number of instances to 10-shots (400 examples), we find that the INJONGO in-language performance was better than the CLINC (16.1 vs. 4.0) that is more Western-centric." |
| Q103 | 8 | evaluation_metrics | "Similarly, in translate-test setting, the gain in performance is much larger (+29), which implies that in a low-resource setting, leveraging a multicultural dataset with the African context is effective." |
| Q104 | 8 | stated_limitations | "However, with more samples (25-shots), there is no significant difference in whether the samples are Western-centric or not, and training data size seems to be more important." |
| Q105 | 9 | task_taxonomy | "We present INJONGO, a new benchmark dataset for evaluating intent detection and slot-filling for 16 African languages." |
| Q106 | 9 | data_sources | "INJONGO represents the first large-scale multicultural dataset focused on African language Conversation AI." |
| Q107 | 9 | stated_limitations | "The scope of INJONGO is constrained by its coverage of only 5 domains and 40 intents, missing some other domains such as healthcare and education that are essential for real-world applications." |
| Q108 | 9 | stated_limitations | "Our language selection, while substantial, still represents only a fraction of Africa's linguistic diversity, particularly lacking representation from other language families such as Nilo-Saharan languages." |
| Q109 | 9 | annotation_process | "The annotation process revealed inherent challenges in entity classification across languages, requiring two rounds of review to achieve consistent quality." |
| Q110 | 9 | stated_limitations | "Although significant for low-resource languages, the dataset size of 3,200 examples per language remains modest compared to high-resource benchmarks, potentially limiting model performance." |
| Q111 | 9 | stated_limitations | "Additionally, the fixed distribution of examples across intents may not accurately reflect the natural frequency of these interactions in real-world conversations." |
| Q112 | 10 | data_sources | "MASSIVE: A 1M-example multilingual natural language understanding dataset with 51 typologically-diverse languages." |
| Q113 | 10 | annotation_process | "Joseph L Fleiss. 1971. Measuring nominal scale agreement among many raters." |
| Q114 | 10 | task_taxonomy | "MasakhaNEWS: News topic classification for African languages." |
| Q115 | 10 | data_sources | "Afridoc-mt: Document-level mt corpus for african languages." |
| Q116 | 10 | data_sources | "MADLAD-400: A multilingual and document-level large audited dataset." |
| Q117 | 13 | task_taxonomy | "These are a total of 40 categories across 5 domains (Banking, Kitchen and Dining, Travel, Utility, and Home)." |
| Q118 | 13 | label_categories | "The "Original Slot Type"are used during the dataset annotation phase, which contained 34 slot types." |
| Q119 | 13 | data_format | "After merging similar or low-frequency types during data preprocessing in Section 3.3, it was reduced to 23 distinct slot types as shown in the "Final Merged Type" column." |
| Q120 | 13 | data_sources | "Table 8: Statistics of the INJONGO dataset across 17 languages, including corpus statistics (token counts and distributions) and slot entity analysis (entity counts, averages, and inter-annotator agreement measures) with unmerged slot types." |
| Q121 | 13 | evaluation_metrics | "To ensure equitable comparison across architectures, we implement a standardized training protocol." |
| Q122 | 13 | evaluation_metrics | "All SLMs are finetuned using the AdamW optimizer in 20 epochs with a learning rate schedule incorporating 10% linear warmup steps followed by linear decay." |
| Q123 | 13 | evaluation_metrics | "Early stopping (patience=5) is adopted, and the dev set performance is monitored." |
| Q124 | 13 | evaluation_metrics | "Learning rates are carefully calibrated for each architecture type as detailed in Table 10." |
| Q125 | 13 | evaluation_metrics | "Our empirical investigations demonstrate that slot filling tasks consistently require higher learning rates compared to intent detection tasks specifically, encoder-only models utilize 1 × 10−5/3 × 10−5for intent detection/slot filling respectively, while encoder-decoder architectures necessitate elevated rates of 5 × 10−5/1 × 10−4." |
| Q126 | 13 | evaluation_metrics | "Given the computational constraints of finetuning LLMs, Fully Supervised Fine-Tuning (FSFT) is exclusively performed on the Gemma 2 9B model with 5 epochs." |
| Q127 | 14 | data_format | "Based on established SFT practices and task-specific requirements, we use learning rates of 2 × 10−5 and 2.5 × 10−5 for intent detection and slot filling respectively." |
| Q128 | 14 | data_sources | "Training data is constructed from the combined train splits of INJONGO dataset across all 17 languages, with prompts randomly sampled from a pool of 5 predefined templates." |
| Q129 | 14 | data_format | "All experiments are conducted using full precision (FP32) on NVIDIA H100/L40S GPUs with a consistent batch size of 32, achieved through gradient accumulation when necessary." |
| Q130 | 14 | evaluation_metrics | "Before the final model training, we conducted a comprehensive analysis of learning rate variations to understand their effect on model performance across Intent Detection and Slot Filling tasks." |
| Q131 | 14 | data_format | "For closed-source models (GPT-4o and Gemini 1.5 Pro), we utilize the API provided by the respective vendor for inference." |
| Q132 | 14 | data_format | "For open-source models, inference is performed using vLLM (Kwon et al., 2023), except for Aya-101, where Text Generation Inference (TGI) is employed." |
| Q133 | 14 | evaluation_metrics | "Across 5 LLMs, we evaluated the performance of zero-shot and few-shot learning on the Intent Detection and Slot Filling tasks." |
| Q134 | 14 | evaluation_metrics | "We only evaluate the performance of the models on the best prompt for each task." |
| Q135 | 14 | evaluation_metrics | "The 2nd prompt for Intent Detection and the 3rd prompt for Slot Filling are used for evaluation." |
| Q136 | 15 | evaluation_metrics | "We provide the prompts in Jinja format used for the Intent Detection and Slot Filling tasks in the zero-shot and few-shot learning experiments." |
| Q137 | 15 | evaluation_metrics | "The prompts are designed to guide the model to perform the specific task on the given input text." |
| Q138 | 15 | evaluation_metrics | "The prompts are language-specific and tailored to the task requirements." |
| Q139 | 15 | evaluation_metrics | "The variables in the prompts are replaced with the actual input text during the model evaluation." |
| Q140 | 15 | evaluation_metrics | "shot_count: The number of examples provided to the model, if shot_count is 0 zero, means zero-shot." |
| Q141 | 15 | evaluation_metrics | "examples: A list of examples provided to the model for few-shot learning." |
| Q142 | 15 | evaluation_metrics | "text: The sentence for which the model needs to predict the intent or slot." |
| Q143 | 16 | data_format | "For Intent Detection, shots refer to examples per domain 5 examples, per (1 shot), and 4 examples per (4 shots). For Slot Filling, shots refer to examples per domain 5 examples, per slot type (1 shot), and 4 examples per slot type (4 shots)." |
| Q144 | 19 | label_categories | "# Named Entities Types to Identify ACCOUNT_TYPE, ARTIST_NAME, BANK_NAME, BILL_TYPE, CALENDAR_EVENT, CITY_OR_PROVINCE, COUNTRY, CURRENCY, DATE, DISH_OR_FOOD, HOTEL_NAME, LANGUAGE_NAME, MEAL_PERIOD, MONEY, MUSIC_GENRE, NUMBER, PAYMENT_COMPANY, PERSONAL_NAME, PLACE_NAME, RESTAURANT_NAME, SHOPPING_ITEM, SONG_NAME, TIME" |
| Q145 | 19 | evaluation_metrics | "Please ensure that the entities match the listed types and that unstated entities should not be included in the response if no entities are found, return `$$` only." |
| Q146 | 19 | data_format | "Sentence: John went to Paris and paid 100 dollars at an Awater restaurant. Output: PERSONAL_NAME John $$ CITY_OR_PROVINCE Paris $$ MONEY 100 $$ RESTAURANT_NAME Awater" |
| Q147 | 19 | task_taxonomy | "Extract named entities from the provided text and format the output by placing $$ between each entity type and its respective content. Ensure the output contains only the extracted entities and their labels, with no additional commentary or information." |
| Q148 | 19 | task_taxonomy | "Detect named entities in the supplied sentence. Use $$ as a separator between entities and their corresponding parts of the sentence. Limit the response strictly to the formatted list." |
| Q149 | 20 | annotation_process | "This section provides the complete annotation guide and instruction for annotators working for labeling all slots types." |
| Q150 | 20 | task_taxonomy | "A Slot Filling task is a natural language processing (NLP) task that involves extracting specific pieces of information (slots) from a given text." |
| Q151 | 20 | task_taxonomy | "This task is commonly used in dialogue systems and information extraction applications where the goal is to identify and fill predefined categories or slots with relevant information from user inputs or text data." |
| Q152 | 21 | label_categories | "When annotating Bank names, you do not need to include "bank" unless it is attached to the bank name, like seen above, with Ecobank." |
| Q153 | 21 | label_categories | "Anything that is less than one day should be annotated as TIME and not DATE, as seen in the above examples." |
| Q154 | 21 | label_categories | "Anything that is more than one day must be annotated as DATE and not time, as seen above" |
| Q155 | 21 | label_categories | "You include "bill" as part of the annotation." |
| Q156 | 24 | annotation_process | "With this entity, only annotate if entity is named explicitly, e.g Name of airport, museum or mall is not and nt just "mall", "airport" etc" |
| Q157 | 24 | annotation_process | "PS: Do not skip any annotations, if there is nothing to annotate, submit and go to the next one." |

### Category Index
- **task_taxonomy**: Q1, Q2, Q3, Q25, Q31, Q61, Q71, Q74, Q101, Q105, Q114, Q117, Q147, Q148, Q150, Q151
- **data_sources**: Q4, Q5, Q18, Q27, Q30, Q32, Q33, Q34, Q35, Q37, Q39, Q56, Q58, Q59, Q60, Q72, Q75, Q88, Q89, Q106, Q112, Q115, Q116, Q120, Q128
- **data_format**: Q6, Q23, Q38, Q41, Q43, Q50, Q51, Q52, Q55, Q57, Q119, Q127, Q129, Q131, Q132, Q143, Q146
- **label_categories**: Q54, Q118, Q144, Q152, Q153, Q154, Q155
- **annotation_process**: Q7, Q40, Q42, Q44, Q45, Q47, Q48, Q49, Q109, Q113, Q149, Q156, Q157
- **evaluation_metrics**: Q8, Q9, Q10, Q11, Q19, Q20, Q46, Q62, Q63, Q64, Q65, Q66, Q67, Q68, Q69, Q70, Q73, Q76, Q77, Q78, Q80, Q83, Q84, Q90, Q91, Q92, Q93, Q94, Q95, Q96, Q98, Q102, Q103, Q121, Q122, Q123, Q124, Q125, Q126, Q130, Q133, Q134, Q135, Q136, Q137, Q138, Q139, Q140, Q141, Q142, Q145
- **stated_limitations**: Q12, Q13, Q14, Q15, Q21, Q22, Q24, Q26, Q28, Q29, Q36, Q53, Q79, Q81, Q82, Q85, Q86, Q87, Q97, Q99, Q100, Q104, Q107, Q108, Q110, Q111
- **authors_affiliations**: Q16, Q17
