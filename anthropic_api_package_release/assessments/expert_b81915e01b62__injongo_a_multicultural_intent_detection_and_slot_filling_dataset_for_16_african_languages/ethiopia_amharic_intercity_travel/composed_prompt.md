I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **INJONGO: A Multicultural Intent Detection and Slot-Filling Benchmark for African Languages** is valid for use in **Ethiopian Intercity/Ride-Hail Commuter Cohort (Amharic-Primary)**.

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

- **Name**: INJONGO
- **Full Name**: INJONGO: A Multicultural Intent Detection and Slot-Filling Benchmark for African Languages
- **Domain**: Multicultural intent detection and slot-filling for African languages
- **Languages**: am, yo, ig, ha, sw, zu, xh, af, so, om, ti, wo, lin, tw, ee, sn, en
- **Porting Strategy**: ground_up
- **Year**: 2025

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Test Case Categories (Input Ontology)
INJONGO targets two canonical conversational AI tasks — intent detection and slot-filling —
which together form the natural language understanding module of task-oriented dialogue systems
[Q1, Q2, Q3]. The benchmark frames slot-filling explicitly as a named entity extraction task
within multi-domain dialogue [Q150, Q151], with close kinship to NER benchmarks but at finer
semantic granularity [Q25]. The full intent taxonomy comprises 40 categories across 5 domains:
Banking, Kitchen & Dining, Travel, Utility, and Home [Q117], derived by selecting the most
suitable subset from the English CLINC dataset's 150-intent, 10-domain taxonomy [Q39].

The benchmark also evaluates encoder-only, encoder-decoder, and LLM2Vec architectures [Q61],
zero-shot and few-shot LLM prompting [Q74], cross-lingual transfer from English to African
languages [Q101], and supervised fine-tuning as an upper-bound baseline [Q71]. The final
summarizing result is presented as a complete benchmark evaluation [Q105].

From a deployment validity standpoint, the paper explicitly acknowledges that INJONGO covers
only 5 domains and 40 intents, "missing some other domains such as healthcare and education
that are essential for real-world applications" [Q107]. The travel domain includes generic
intents (e.g., "exchange rate", "book flight") but not operator-specific intercity bus flows
such as seat-class selection, road-closure rebooking, or holiday-surge booking (Timkat,
Meskel). The fixed distribution of 80 utterances per intent "may not accurately reflect the
natural frequency of these interactions in real-world conversations" [Q111].

### Content (Input Content)
INJONGO is the first large-scale multicultural ID-SF dataset covering 16 African languages
[Q4, Q106], described as the largest of its kind for African Conversational AI. The 16
languages span two dominant African language families — 13 Niger-Congo and 3 Afro-Asiatic —
with speaker populations ranging from 98 million (Swahili) to 5 million (Wolof) [Q32, Q33,
Q34]. Amharic is among the three Afro-Asiatic languages included.

Rather than translating CLINC utterances — an approach criticized for translationese artifacts
and Western cultural bias [Q13, Q27] — annotators were shown CLINC sample sentences as prompts
and asked to independently generate culturally relevant utterances in their native language
[Q37]. A key illustration of the cultural grounding methodology is the Xhosa annotator
example: South African banks (FNB, Absa) and the Rand currency replaced Western exemplars
[Q40, Q41]. The paper explicitly states that slot entities are intended to be "more culturally
relevant in the respective countries the languages are from" [Q30].

However, the paper does not document whether Ethiopian-specific slot values — Amharic city
names (Hawassa, Mekelle, Gondar), Birr-denominated fares, or Ethiopian calendar references
(Meskerem, Tikimt) — are present in the travel-domain instances. Web coverage is noted as a
confounding variable: Swahili, with over 1 billion monolingual tokens, achieves near-English
performance [Q88, Q89], suggesting that the depth and cultural specificity of instances varies
substantially across languages and that Amharic instances may have lower coverage of
Ethiopia-specific toponyms and fare conventions. MASSIVE, the predecessor benchmark, is
explicitly criticized for leaving "Western entities still prevalent" even after partial cultural
replacement [Q29], and INJONGO positions itself as addressing this gap — but the degree to
which this was achieved for the Amharic subset's travel domain is NOT DOCUMENTED in the
registry.

### Input Signal Form (Input Form)
INJONGO is a text-only benchmark. Data construction proceeds from text utterance elicitation
through slot-filling annotation, and the output format represents slot spans as labeled entity
types in plain text [Q38, Q43]. Amharic (Ge'ez script) is one of the 16 covered languages
[Q4]. The deployment context is a text-based smartphone app, which fully matches INJONGO's
input modality. No script mismatch issues arise for Amharic.

The dataset is released under CC BY 4.0 [Q23], and the annotation was performed on the
LabelStudio platform using an NER setup [Q43]. Closed-source models were accessed via vendor
APIs and open-source models via vLLM or TGI [Q131, Q132], all operating on text. Few-shot
shot counts are defined differently per task: for slot-filling, 1-shot equals one example per
slot type (23 examples total) [Q143]. No modality mismatch concerns exist for the Ethiopian
smartphone deployment; input form is a low-concern dimension.

### Output Categories (Output Ontology)
The output label space consists of two components: (1) an intent label from 40 categories
across 5 domains [Q117], and (2) slot entity labels from 23 final slot types [Q118, Q119].
The full enumeration of slot types used in prompts is: ACCOUNT_TYPE, ARTIST_NAME, BANK_NAME,
BILL_TYPE, CALENDAR_EVENT, CITY_OR_PROVINCE, COUNTRY, CURRENCY, DATE, DISH_OR_FOOD,
HOTEL_NAME, LANGUAGE_NAME, MEAL_PERIOD, MONEY, MUSIC_GENRE, NUMBER, PAYMENT_COMPANY,
PERSONAL_NAME, PLACE_NAME, RESTAURANT_NAME, SHOPPING_ITEM, SONG_NAME, TIME [Q144].

The original 34-type ontology is documented in Appendix A.2 [Q54], and the merging process
that reduced it to 23 types involved removing slot entities appearing fewer than 500 times
across all languages [Q51, Q52] and merging similar types [Q55, Q119]. Fine-grained boundary
rules are documented: TIME applies to sub-day durations and DATE to periods of one day or more
[Q153, Q154]; BANK_NAME excludes the word "bank" unless part of the name [Q152]; BILL_TYPE
includes the word "bill" [Q155].

For the Ethiopian deployment, CURRENCY and MONEY slot types are present and support
Birr-denominated fare extraction in principle. However, DATE annotation examples use Gregorian
conventions [Q153, Q154], and there is no documented accommodation for Ethiopian calendar
months in the annotation guide — a direct output-ontology gap for travel-date slot extraction.
Similarly, CITY_OR_PROVINCE and PLACE_NAME slots are present, but whether their training
instances contain Ethiopian intercity toponyms is NOT DOCUMENTED. The intent taxonomy (40
classes) covers generic travel but not operator-specific booking flows such as seat-class
upgrades or road-closure rebooking.

### Annotation Process (Output Content)
Utterances were generated and annotated by native speakers of each target language [Q7],
recruited through a logistics company in Kenya that handled compensation at per-country rates
[Q44]. Each utterance received slot-filling annotations from at least three annotators, with
disagreements resolved by majority voting [Q42, Q45].

Initial Fleiss' Kappa scores showed substantial cross-language variation (0.618 for Zulu to
0.934 for Shona) [Q47]; after a two-round review process [Q109], scores improved to
0.912–1.00 across all languages [Q48], with the largest gains in Sesotho (+0.327) and Zulu
(+0.294) [Q49]. The review process was partly motivated by ambiguous slot type definitions
that degraded early annotation quality [Q53], and the annotation guide was detailed enough to
include edge-case rules [Q156, Q157] and a complete slot-type instruction set [Q149].

A critical gap for the Ethiopian deployment: while native Amharic speakers annotated the
Amharic portion, the paper does not disclose the specific regional or demographic profile of
those annotators — urban vs. rural origin, Addis Ababa–centric vs. other regions, or L1 vs.
L2 Amharic. The actual user population includes L2 Amharic speakers from Oromia, Tigray, and
Amhara regions who code-switch. INJONGO includes Oromo and Tigrinya as separate languages but
does not document intra-utterance code-switching within Amharic utterances. Dataset statistics
are summarized in Table 8 [Q120], but annotator demographic sub-profiles by language are NOT
DOCUMENTED in the registry.

### Output Modality (Output Form)
The benchmark reports intent detection performance using accuracy and slot-filling performance
using F1-score [Q84]. The best fine-tuned model (AfroXLMR-76L) achieves 93.7% accuracy on
intent detection and 85.6% F1 on slot-filling [Q19, Q78]; GPT-4o in zero-shot achieves 70.6%
average intent detection accuracy [Q10] and 26% F1 on slot-filling [Q9]. Few-shot prompting
substantially closes the slot-filling gap — GPT-4o and Gemini 1.5 Pro each improve by more
than +19 F1 points with just 5 examples [Q91] — while SFT on Gemma 2 9B remains 34.1 F1
points above 4-shot prompting [Q98].

LLM evaluations use 5 prompt templates and temperature 0.5 [Q73], with best-prompt selection
applied for few-shot comparisons [Q134, Q135], and evaluation is averaged over templates and
African languages [Q84]. Prompts are language-specific [Q137, Q138] and use a structured
`$$`-delimited entity format [Q145, Q146]. The output modality (intent class + slot tags in
structured text) fully matches the deployment's requirements for a task-oriented dialogue
system. F1-score for slot-filling is well-suited to partial-match assessment of slot spans,
and accuracy for intent detection is appropriate given the closed 40-class label space. Output
form is a low-concern dimension for this deployment.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "Slot-filling and intent detection are well-established tasks in Conversational AI." |
| Q2 | 1 | input_ontology | "Intent detection and slot-filling are crucial components of the natural language understanding module in task-oriented dialogue systems (Hemphill et al., 1990; Coucke et al., 2018; Gupta et al., 2018)." |
| Q3 | 1 | input_ontology | "They map a user's request to a predefined semantic category recognized by the dialogue manager, along with extracting specific entities (known as slots)." |
| Q4 | 1 | input_content | "We develop INJONGO—the first large-scale multicultural intent detection and slot-filling dataset covering 16 African languages, and English language." |
| Q5 | 1 | input_ontology | "We cover the following five domains: banking, home, travel, utility, and kitchen & dining." |
| Q6 | 1 | input_content | "The data construction process starts with providing an annotator with sentences from the CLINC dataset (Larson et al., 2019a) with a specified intent type, and they are to come up with culturally-relevant similar sentences and relevant slot entities (see Figure 1)." |
| Q7 | 1 | output_content | "utterances generated by native speakers across diverse domains, including banking, travel, home, and dining." |
| Q8 | 1 | input_ontology | "Through extensive experiments, we benchmark the fine-tuning multilingual transformer models and the prompting large language models (LLMs), and show the advantage of leveraging African-cultural utterances over Western-centric utterances for improving cross-lingual transfer from the English language." |
| Q9 | 1 | output_form | "Experimental results reveal that current LLMs struggle with the slot-filling task, with GPT-4o achieving an average performance of 26% F1-score." |
| Q10 | 1 | output_form | "In contrast, intent detection performance is notably better, with an average accuracy of 70.6%, though it still falls behind the fine-tuning baselines." |
| Q11 | 1 | output_form | "When compared to the English language, GPT-4o and fine-tuning baselines perform similarly on intent detection, achieving an accuracy of approximately 81%." |
| Q12 | 1 | input_content | "current large-scale benchmarks for these tasks often exclude evaluations of low-resource languages and rely on translations from English benchmarks, thereby predominantly reflecting Western-centric concepts." |
| Q13 | 1 | input_content | "However, these efforts face two key challenges: (1) the translationese effect, which makes utterances sound less natural in the target languages (Vanmassenhove et al., 2021; Bizzoni et al., 2020), and (2) the creation of utterances that are less culturally relevant." |
| Q14 | 1 | input_content | "Despite improvements in the utterance generation process, MASSIVE includes only three African languages (Amharic, Afrikaans and Swahili), and many utterances remain culturally irrelevant to the target language communities." |
| Q15 | 1 | output_form | "Our findings suggest that the performance of LLMs is still behind for many low-resource African languages, and more work is needed to further improve their downstream performance." |
| Q16 | 1 | output_content | "Hao Yu1, Jesujoba O. Alabi3,∗, Andiswa Bukula4,∗, Jian Yun Zhuang5, En-Shiun Annie Lee6, Tadesse Kebede Guge∗, Israel Abebe Azime3, Happy Buzaaba7,∗, Blessing Kudzaishe Sibanda∗, Godson K. Kalipe∗, Jonathan Mukiibi8,∗, Salomon Kabongo Kabenamualu9,∗, Mmasibidi Setaka4, Lolwethu Ndolela∗, Nkiruka Odu∗, Rooweither Mabuya4,∗, Shamsuddeen Hassan Muhammad10,∗, Salomey Osei11, Sokhar Samb12, Juliet W. Murage∗, Dietrich Klakow3, David Ifeoluwa Adelani1,2,∗" |
| Q17 | 1 | output_content | "∗Masakhane NLP, 1Mila - Quebec AI Institute & McGill University, Canada, 2Canada CIFAR AI Chair, 3Saarland University, Germany, 4SADiLaR, South Africa, 5University of Toronto, Canada, 6 OntarioTech University, Canada, 7Princeton University, USA, 8Makerere University, Uganda, 9L3S Research Center, Germany, 10Imperial College London, United Kingdom, 11Universidad de Deusto, Spain, 12DAUST, Senegal." |
| Q18 | 2 | input_ontology | "INJONGO dataset covers 5 domains, 40 intents, 23 slots, and 3,200 instances per African language." |
| Q19 | 2 | output_form | "Our result shows that fine-tuning baselines could reach an accuracy of 93.7% and F1-score of 85.6 for intent detection and slot-filling tasks respectively." |
| Q20 | 2 | output_form | "While the best prompting of LLMs results (GPT-4o) drops by -28% accuracy point and −52.6 F1 score." |
| Q21 | 2 | output_form | "While slot-filling and named entity recognition tasks are often challenging for LLMs even for English (Yu et al., 2023), intent detection performance in English is similar performance whether we use fine-tuning baselines or prompt GPT-4o." |
| Q22 | 2 | output_form | "Our findings suggest that LLMs performance is still behind for many low-resource African languages, and more work is needed to further improve their downstream performance." |
| Q23 | 2 | input_form | "Dataset is released under CC BY 4.0 license." |
| Q24 | 2 | input_content | "Limited available labeled datasets are one of the major challenges of AfricaNLP." |
| Q25 | 2 | input_ontology | "The closest benchmark to our task of slot-filling is MasakhaNER (Adelani et al., 2021, 2022) that covers 20 African languages but they focus on four entity types "personal names", "organization", "location", and "dates", which are not fine-grained and well adapted to several domains such as banking and travel that we cover in INJONGO." |
| Q26 | 2 | input_content | "Most of the existing benchmarks for intent detection and slot-filling tasks are English-only." |
| Q27 | 2 | input_content | "There are a few efforts to make them multilingual in two ways: (1) human generating the utterances in a particular domain, followed by intent and slot filling annotation. (2) through human translation of annotated data from English to other languages which introduces some cultural bias since Western entities are being propagated." |
| Q28 | 2 | input_content | "While the first approach is the most ideal methodology, it is very cost-intensive when scaling to many languages." |
| Q29 | 2 | input_content | "MASSIVE benchmark partially addresses this Western cultural bias by encouraging translators to replace entities with more culturally relevant ones, but Western entities are still prevalent in the dataset." |
| Q30 | 2 | input_content | "In our paper, we introduce INJONGO which is the largest intent detection and slot-filling dataset covering 16 African languages, and we ensured that the slot entities are more culturally relevant in the respective countries the languages are from." |
| Q31 | 2 | input_ontology | "INJONGO is a joint intent detection and slot-filling dataset (ID-SF) for typologically diverse Sub-Saharan African languages and English." |
| Q32 | 2 | input_content | "The selected languages represent diverse linguistic families and are widely spoken in Africa." |
| Q33 | 2 | input_content | "These languages come from the two dominant language families in Africa: 13 from Niger-Congo and three from Afro-Asiatic." |
| Q34 | 2 | input_content | "The languages covered are spoken by a large population in Africa, ranging from Swahili with 98M speakers to Wolof with 5M speakers." |
| Q35 | 3 | input_content | "Typical ID-SF data collection often requires large crowd-sourcing efforts to collect utterances, with additional labeling of intents and slots in various domains." |
| Q36 | 3 | input_content | "Developing such a large crowd-sourcing effort is time-consuming and costly for several low-resource languages." |
| Q37 | 3 | input_content | "To simplify the process while making the dataset cultural, we provide each annotator with sample sentences from the CLINC dataset (Larson et al., 2019a) with a specified intent type, say "transfer"." |
| Q38 | 3 | input_form | "Then, the dataset construction follows two stages: (1) Utterance elicitation in an African language and (2) Slot-filling annotation of the generated utterance." |
| Q39 | 3 | input_ontology | "The source data for our multilingual benchmark is from the CLINC English dataset—an intent detection with 150 intent classes across 10 domains (but without slot annotation), we extracted 40 intents from five most suitable domains to the African contexts: Banking (e.g. "transfer", "pay bill"), Home (e.g. "play music", "calendar update"), Kitchen and Dining (e.g. "recipe", "confirm reservation"), Travel (e.g. "exchange rate", "book flight"), and Utility (e.g." |
| Q40 | 3 | output_content | "A Xhosa annotator was asked to generate another utterance belonging to the same intent type but capturing the South African context where the language is spoken." |
| Q41 | 3 | input_content | "Thus, the annotator used the R200 as "money" with currency Rand (R), and more familiar South African banks such as "FNB" and "Absa" for "bank name" slot." |
| Q42 | 4 | output_content | "Each utterance was annotated by three annotators so that we could check for agreement in the slot annotations." |
| Q43 | 4 | input_form | "The annotation followed the named entity recognition setup on LabelStudio platform." |
| Q44 | 4 | output_content | "For both utterance elicitation and slot-filling annotation, all recruited participants received an appropriate remuneration based on the per-country rate decided by our logistics company in Kenya." |
| Q45 | 4 | output_content | "To ensure annotation quality and consistency, we follow a rigorous quality control process using a majority voting system with a minimum of three annotators per sentence to resolve disagreements." |
| Q46 | 4 | output_content | "The annotation quality was evaluated using Fleiss' Kappa score (Fleiss, 1971), with scores presented in Table 3 comparing agreement levels before and after the review process." |
| Q47 | 4 | output_content | "Initial Fleiss' Kappa scores revealed substantial variation across languages, ranging from 0.618 (Zulu) to 0.934 (Shona), indicating significant inter-annotator disagreement." |
| Q48 | 4 | output_content | "Following the review process, agreement scores improved markedly across all languages, reaching 0.912-1.00." |
| Q49 | 4 | output_content | "Notable improvements were observed in Sesotho (+0.327) and Zulu (+0.294), with other languages showing average improvements of approximately 0.1 in their Fless' Kappa scores." |
| Q50 | 4 | output_ontology | "We performed an analysis of entity frequency distribution across all languages." |
| Q51 | 4 | output_ontology | "We decided to exclude slot entities appearing less than 500 times across all languages (after MUSIC GENRE in the figure)." |
| Q52 | 4 | output_ontology | "Consequently, nine infrequent slots from NATIONALITY through PLUG TYPE were eliminated." |
| Q53 | 4 | output_content | "Examination of annotator feedback and comparative analysis between unreviewed and reviewed versions indicated that ambiguous slot types significantly impacted annotation quality and introduced unnecessary complexity." |
| Q54 | 4 | output_ontology | "Appendix A.2 contains all 34 slot types selected." |
| Q55 | 5 | output_ontology | "This merging process resulted in a reduction from 34 to 23 slot types." |
| Q56 | 5 | input_content | "Our final annotation resulted in 3,200 annotated utterances, with 80 utterances per intent for each of the 16 African languages." |
| Q57 | 5 | input_form | "The dataset is partitioned following ratios of 70%, 10%, and 20% for train, dev, and test splits respectively, stratified by intent for each language." |
| Q58 | 5 | input_content | "Additionally, we aggregated the practice utterances generated and the practice slot annotations as the English dataset, leading to 17 annotated languages." |
| Q59 | 5 | input_content | "In total, the English consist of 1779 utterances." |
| Q60 | 5 | input_content | "Finally, we sampled 4000 CLINC intent-only dataset to compare westerncentric English dataset to our curated INJONGO dataset that captures the African contexts." |
| Q61 | 5 | input_ontology | "We evaluate three categories of models: (1) encoder-only models such as XLM-RoBERTa Large (Conneau et al., 2019), AfroXLMR (Alabi et al., 2022), AfroXLMR-76L (Adelani et al., 2023a), AfriBERTa V2 (Oladipo, 2024), (2) encoder-decoder models such as mT5-Large (Xue et al., 2020), AfriTeVa V2 Large (Oladipo et al., 2023), and (3) a multilingual variant of LLM2Vec model (BehnamGhader et al., 2024) i.e. NLLB-LLM2Vec (Schmidt et al., 2024) that stack NLLB-encoder (NLLB Team et al., 2022) model with LLaMa 3.1 8B (Grattafiori et al., 2024) to develop a multilingual sentence transformer model." |
| Q62 | 5 | output_form | "These models are fine-tuned using the AdamW optimizer for 20 epochs with early stopping." |
| Q63 | 5 | output_form | "All results are averaged over five seeds." |
| Q64 | 5 | output_form | "Learning rates are calibrated for each architecture and task as detailed in Appendix B.2." |
| Q65 | 5 | output_form | "First, we conduct zero-shot prompting using the following widely used LLMs for evaluation: GPT4o, Gemini 1.5 Pro (Reid et al., 2024), Gemma 2 9B/27B Instruct (Team et al., 2024), Llama 3.1 8B/3.3 70B Instruct (Grattafiori et al., 2024), and Aya-101 (Üstün et al., 2024)." |
| Q66 | 5 | output_form | "We make use of five different prompts for each LLM." |
| Q67 | 6 | output_form | "we perform few-shot evaluation using the best-performing zero-shot template for each task (see Appendix C)." |
| Q68 | 6 | output_form | "We employ two few-shot strategies (1) 5-examples: prompting with any 5 samples from different domains (see Figure 1) i.e. one intent type is covered by domain (2) One-shot intent-type prompting i.e. one sample per intent type or 40 samples from different intent types." |
| Q69 | 6 | output_form | "We used the same samples for both tasks." |
| Q70 | 6 | output_form | "Finally, we extend to 4 shots—acceptable maximum context length (CL) for Gemma 2, Aya-101 was excluded for small CL." |
| Q71 | 6 | input_ontology | "Finally, as an additional strong baseline for LLMs, we performed supervised fine-tuning (SFT) on Gemma 2 9B for 5 epochs using learning rates of 2 × 10−5/ 2.5 × 10−5for intent detection and slot filling." |
| Q72 | 6 | input_content | "The dataset of SFT was obtained by aggregating all the training samples of the 17 languages in INJONGO i.e. "Combined INJONGO", with randomly sampled prompts from a pool of 5." |
| Q73 | 6 | output_form | "The evaluations of LLMs use 5 different prompting templates and a temperature of 0.5." |
| Q74 | 6 | input_ontology | "To investigate how well our dataset facilitates cross-lingual learning and transfer capabilities across languages, we tested two settings (1) zero-shot transfer from the English split of INJONGO, and evaluated on African languages. (2) Translate-Test where we evaluate on the machine-translated sentence test sets from an African language to English." |
| Q75 | 6 | input_content | "We leveraged the NLLB-200-3.3B (NLLB Team et al., 2022) machine translation model for the Translate-test setting." |
| Q76 | 6 | output_form | "Experiments of the baselines and cross-lingual transfer runs make use of five fixed random seeds." |
| Q77 | 6 | output_form | "Table 5 summarizes the results of the multilingual encoders fine-tuned INJONGO dataset." |
| Q78 | 6 | output_form | "Overall, AfroXLMR-76L achieves the best performance on both ID-SF tasks, with an average accuracy of 93.7% and an F1 score of 85.6%, respectively." |
| Q79 | 6 | output_content | "We attribute the success of this model to the coverage of all languages in INJONGO during its pre-training (see Appendix Table 11)." |
| Q80 | 6 | output_form | "AfroXLMR, the earlier version of AfroXLMR-76L, follows closely with an average accuracy of 92.2% and an F1 score of 85.2%." |
| Q81 | 6 | output_content | "However, this model was not pre-trained on some of the languages such as ewe, twi, lin, and wol leading to a significant drop in performance of −5.8, −4.8, −1.3, −0.4 for intent detection when compared to AfroXLMR-76L." |
| Q82 | 6 | output_form | "This shows that multilingual encoders for African languages can significantly improve the performance over massively multilingual encoders covering more than 100 languages such as XLM-R and NLLB LLM2Vec." |
| Q83 | 7 | output_form | "Table 6 shows the zero-shot LLM evaluation of five open models and two closed models." |
| Q84 | 7 | output_form | "Evaluation is based on accuracy and F1-score for ID and SF tasks. Average computed on five templates, and on only African languages." |
| Q85 | 7 | output_form | "Slot-filling task is difficult for all LLMs including on English The highest average performance achieved by the LLMs is 33.3% for GPT-4o, although much better than the open model at 28.8. We attribute this to the difficulty of LLMs on the named entity recognition task as reported by other researchers (Yu et al., 2023; Ojo et al., 2023). In comparison to the best-finetuned model, there is a large drop in performance of −53.2. This shows that having training data is still relevant for this task even in the LLM era, especially for low-resource languages." |
| Q86 | 7 | output_form | "For intent detection, we find that all open models achieved below 50% on the relatively easy task of intent detection. The poor performance may be attributed to either a lack of exposure to many African languages or the large label space (i.e. 40) for the classification task." |
| Q87 | 7 | output_content | "The closed models result are better, with GPT-4o and Gemini 1.5 Pro achieving more than +20 points than the best open model, Llama 3.3 70B. However, if we compare the results in the English language, open models such as Gemma 2 27B and Llama 3.3 70B are competitive with closed models. This shows that open models are more biased toward high-resource languages." |
| Q88 | 7 | input_content | "The performance of some African languages is often higher than others, this is probably connected to the amount of monolingual data available on the web." |
| Q89 | 7 | input_content | "For example, Swahili (swa) with over 1 billion monolingual data (Kudugunta et al., 2023) has 80.6 accuracy point that is comparable performance to English performance (81.1) with Llama 3.3 70B, while other languages have much lower performance." |
| Q90 | 8 | output_form | "Figure 3 shows the result of the various few-shot setups: 5-examples, 1-shot (40 examples, one from each intent type), and 4-shots (160 examples)." |
| Q91 | 8 | output_form | "Our result shows a big boost in performance with only 5-examples, especially for the slot-filling task and some LLMs: GPT-4o and Gemini 1.5 Pro improved the most by more than +19 points." |
| Q92 | 8 | output_form | "Similarly, Gemma 2 9B improved from 2.4 to 33.5 matching the performance of Llama 3.3 70B (with 5-examples)." |
| Q93 | 8 | output_form | "Additional samples from 1-shot and 4-shot consistently improved performance for all models except Llama 3.3 70B." |
| Q94 | 8 | output_form | "We find Gemini 1.5 Pro, Gemma 2 9B and Gemma 2 27B to benefit the most from 5-examples, with an accuracy boost of +14.3, +15.7, and +21.8 respectively." |
| Q95 | 8 | output_form | "While the zero-shot performance of Gemini 1.5 Pro is worse than GPT-4o, the few-shot performance exceeds that of GPT-4o with +1.8 and +2.3 improvement in 5-examples and 1-shot." |
| Q96 | 8 | output_form | "Our result shows the effectiveness of LLMs in adapting quickly to a new task in low-resource settings." |
| Q97 | 8 | output_form | "While all LLMs improve performance with more shots, there is still a large gap with SFT." |
| Q98 | 8 | output_form | "We performed SFT on Gemma 2 9B with all training samples and prompt templates, we found a large performance gap of +15.8 and +34.1 for intent detection and slot-filling respectively if we compare SFT (52k samples) to 4-shots (160 examples)." |
| Q99 | 8 | output_form | "However, for closed models, the gap of SFT on Gemma 2 9B to Gemini 1.5 Pro and GPT-4o is much smaller, especially for intent detection." |
| Q100 | 8 | output_form | "In general, few-shots of LLMs are still worse than SFT but are very crucial and effective when training data are scarce." |
| Q101 | 8 | input_ontology | "Figure 4 shows our final experiments that compare cross-lingual transfer results from two English datasets: CLINC (Western-centric) and INJONGO (African-centric) on the intent detection task." |
| Q102 | 8 | output_form | "At 5-shots, in both in-language and translate-test settings, the accuracy of all settings is quite similar, however as we increase the number of instances to 10-shots (400 examples), we find that the INJONGO in-language performance was better than the CLINC (16.1 vs. 4.0) that is more Western-centric." |
| Q103 | 8 | output_form | "Similarly, in translate-test setting, the gain in performance is much larger (+29), which implies that in a low-resource setting, leveraging a multicultural dataset with the African context is effective." |
| Q104 | 8 | input_content | "However, with more samples (25-shots), there is no significant difference in whether the samples are Western-centric or not, and training data size seems to be more important." |
| Q105 | 9 | input_ontology | "We present INJONGO, a new benchmark dataset for evaluating intent detection and slot-filling for 16 African languages." |
| Q106 | 9 | input_content | "INJONGO represents the first large-scale multicultural dataset focused on African language Conversation AI." |
| Q107 | 9 | input_ontology | "The scope of INJONGO is constrained by its coverage of only 5 domains and 40 intents, missing some other domains such as healthcare and education that are essential for real-world applications." |
| Q108 | 9 | input_content | "Our language selection, while substantial, still represents only a fraction of Africa's linguistic diversity, particularly lacking representation from other language families such as Nilo-Saharan languages." |
| Q109 | 9 | output_content | "The annotation process revealed inherent challenges in entity classification across languages, requiring two rounds of review to achieve consistent quality." |
| Q110 | 9 | input_content | "Although significant for low-resource languages, the dataset size of 3,200 examples per language remains modest compared to high-resource benchmarks, potentially limiting model performance." |
| Q111 | 9 | input_ontology | "Additionally, the fixed distribution of examples across intents may not accurately reflect the natural frequency of these interactions in real-world conversations." |
| Q112 | 10 | input_content | "MASSIVE: A 1M-example multilingual natural language understanding dataset with 51 typologically-diverse languages." |
| Q113 | 10 | output_content | "Joseph L Fleiss. 1971. Measuring nominal scale agreement among many raters." |
| Q114 | 10 | input_ontology | "MasakhaNEWS: News topic classification for African languages." |
| Q115 | 10 | input_content | "Afridoc-mt: Document-level mt corpus for african languages." |
| Q116 | 10 | input_content | "MADLAD-400: A multilingual and document-level large audited dataset." |
| Q117 | 13 | input_ontology | "These are a total of 40 categories across 5 domains (Banking, Kitchen and Dining, Travel, Utility, and Home)." |
| Q118 | 13 | output_ontology | "The "Original Slot Type"are used during the dataset annotation phase, which contained 34 slot types." |
| Q119 | 13 | output_ontology | "After merging similar or low-frequency types during data preprocessing in Section 3.3, it was reduced to 23 distinct slot types as shown in the "Final Merged Type" column." |
| Q120 | 13 | output_content | "Table 8: Statistics of the INJONGO dataset across 17 languages, including corpus statistics (token counts and distributions) and slot entity analysis (entity counts, averages, and inter-annotator agreement measures) with unmerged slot types." |
| Q121 | 13 | output_form | "To ensure equitable comparison across architectures, we implement a standardized training protocol." |
| Q122 | 13 | output_form | "All SLMs are finetuned using the AdamW optimizer in 20 epochs with a learning rate schedule incorporating 10% linear warmup steps followed by linear decay." |
| Q123 | 13 | output_form | "Early stopping (patience=5) is adopted, and the dev set performance is monitored." |
| Q124 | 13 | output_form | "Learning rates are carefully calibrated for each architecture type as detailed in Table 10." |
| Q125 | 13 | output_form | "Our empirical investigations demonstrate that slot filling tasks consistently require higher learning rates compared to intent detection tasks specifically, encoder-only models utilize 1 × 10−5/3 × 10−5for intent detection/slot filling respectively, while encoder-decoder architectures necessitate elevated rates of 5 × 10−5/1 × 10−4." |
| Q126 | 13 | output_form | "Given the computational constraints of finetuning LLMs, Fully Supervised Fine-Tuning (FSFT) is exclusively performed on the Gemma 2 9B model with 5 epochs." |
| Q127 | 14 | output_form | "Based on established SFT practices and task-specific requirements, we use learning rates of 2 × 10−5 and 2.5 × 10−5 for intent detection and slot filling respectively." |
| Q128 | 14 | input_content | "Training data is constructed from the combined train splits of INJONGO dataset across all 17 languages, with prompts randomly sampled from a pool of 5 predefined templates." |
| Q129 | 14 | input_form | "All experiments are conducted using full precision (FP32) on NVIDIA H100/L40S GPUs with a consistent batch size of 32, achieved through gradient accumulation when necessary." |
| Q130 | 14 | output_form | "Before the final model training, we conducted a comprehensive analysis of learning rate variations to understand their effect on model performance across Intent Detection and Slot Filling tasks." |
| Q131 | 14 | input_form | "For closed-source models (GPT-4o and Gemini 1.5 Pro), we utilize the API provided by the respective vendor for inference." |
| Q132 | 14 | input_form | "For open-source models, inference is performed using vLLM (Kwon et al., 2023), except for Aya-101, where Text Generation Inference (TGI) is employed." |
| Q133 | 14 | output_form | "Across 5 LLMs, we evaluated the performance of zero-shot and few-shot learning on the Intent Detection and Slot Filling tasks." |
| Q134 | 14 | output_form | "We only evaluate the performance of the models on the best prompt for each task." |
| Q135 | 14 | output_form | "The 2nd prompt for Intent Detection and the 3rd prompt for Slot Filling are used for evaluation." |
| Q136 | 15 | output_form | "We provide the prompts in Jinja format used for the Intent Detection and Slot Filling tasks in the zero-shot and few-shot learning experiments." |
| Q137 | 15 | output_form | "The prompts are designed to guide the model to perform the specific task on the given input text." |
| Q138 | 15 | input_form | "The prompts are language-specific and tailored to the task requirements." |
| Q139 | 15 | output_form | "The variables in the prompts are replaced with the actual input text during the model evaluation." |
| Q140 | 15 | output_form | "shot_count: The number of examples provided to the model, if shot_count is 0 zero, means zero-shot." |
| Q141 | 15 | output_form | "examples: A list of examples provided to the model for few-shot learning." |
| Q142 | 15 | input_form | "text: The sentence for which the model needs to predict the intent or slot." |
| Q143 | 16 | output_form | "For Intent Detection, shots refer to examples per domain 5 examples, per (1 shot), and 4 examples per (4 shots). For Slot Filling, shots refer to examples per domain 5 examples, per slot type (1 shot), and 4 examples per slot type (4 shots)." |
| Q144 | 19 | output_ontology | "# Named Entities Types to Identify ACCOUNT_TYPE, ARTIST_NAME, BANK_NAME, BILL_TYPE, CALENDAR_EVENT, CITY_OR_PROVINCE, COUNTRY, CURRENCY, DATE, DISH_OR_FOOD, HOTEL_NAME, LANGUAGE_NAME, MEAL_PERIOD, MONEY, MUSIC_GENRE, NUMBER, PAYMENT_COMPANY, PERSONAL_NAME, PLACE_NAME, RESTAURANT_NAME, SHOPPING_ITEM, SONG_NAME, TIME" |
| Q145 | 19 | output_form | "Please ensure that the entities match the listed types and that unstated entities should not be included in the response if no entities are found, return `$$` only." |
| Q146 | 19 | output_form | "Sentence: John went to Paris and paid 100 dollars at an Awater restaurant. Output: PERSONAL_NAME John $$ CITY_OR_PROVINCE Paris $$ MONEY 100 $$ RESTAURANT_NAME Awater" |
| Q147 | 19 | input_ontology | "Extract named entities from the provided text and format the output by placing $$ between each entity type and its respective content. Ensure the output contains only the extracted entities and their labels, with no additional commentary or information." |
| Q148 | 19 | input_ontology | "Detect named entities in the supplied sentence. Use $$ as a separator between entities and their corresponding parts of the sentence. Limit the response strictly to the formatted list." |
| Q149 | 20 | output_content | "This section provides the complete annotation guide and instruction for annotators working for labeling all slots types." |
| Q150 | 20 | input_ontology | "A Slot Filling task is a natural language processing (NLP) task that involves extracting specific pieces of information (slots) from a given text." |
| Q151 | 20 | input_ontology | "This task is commonly used in dialogue systems and information extraction applications where the goal is to identify and fill predefined categories or slots with relevant information from user inputs or text data." |
| Q152 | 21 | output_ontology | "When annotating Bank names, you do not need to include "bank" unless it is attached to the bank name, like seen above, with Ecobank." |
| Q153 | 21 | output_ontology | "Anything that is less than one day should be annotated as TIME and not DATE, as seen in the above examples." |
| Q154 | 21 | output_ontology | "Anything that is more than one day must be annotated as DATE and not time, as seen above" |
| Q155 | 21 | output_ontology | "You include "bill" as part of the annotation." |
| Q156 | 24 | output_content | "With this entity, only annotate if entity is named explicitly, e.g Name of airport, museum or mall is not and nt just "mall", "airport" etc" |
| Q157 | 24 | output_content | "PS: Do not skip any annotations, if there is nothing to annotate, submit and go to the next one." |

---

## Regional Context

```yaml
name: Ethiopian Intercity/Ride-Hail Commuter Cohort (Amharic-Primary)
abbreviation: ETH-INTERCITY-AM
deployment_context:
  system_description: Amharic-language conversational booking system serving three
    Ethiopian intercity and ride-hail operators (Sky Bus, Selam Bus, Ride), handling
    intent detection and slot-filling for routes, fares, and seat changes via smartphone
    apps.
  operators:
  - Sky Bus
  - Selam Bus
  - Ride
  task_types:
  - intent detection
  - slot-filling
  slot_filling_domains:
  - route queries
  - fare lookup
  - seat selection
  - booking
  - cancellation/rebooking
  benchmark_under_assessment: INJONGO
target_population:
  description: Ethiopian inter-regional commuters and travelers who interact with
    smartphone-based booking apps in Amharic. The population spans multiple Ethiopian
    regions and intercity corridors. Urban Addis Ababa users are likely over-represented
    in any annotator pool, but actual users include travelers from Amhara, Oromia,
    Tigray, SNNP, and other regions. Many users are L2 Amharic speakers from other
    Ethiopian ethnic groups who code-switch within utterances.
  primary_language: Amharic (am)
  l2_and_code_switching_languages:
  - Oromo (om)
  - Tigrinya (ti)
  - Somali (so)
  - Sidama
  - Wolayta
  geography:
    country: Ethiopia
    relevant_regions:
    - Addis Ababa (urban hub, annotator over-representation risk)
    - Amhara Region (e.g., Gondar, Bahir Dar, Dessie corridors)
    - Oromia Region (e.g., Jimma, Adama/Nazret, Shashamane corridors)
    - Tigray Region (e.g., Mekelle corridor)
    - SNNP Region (e.g., Hawassa corridor)
    - Somali Region (e.g., Dire Dawa/Jigjiga corridor)
    - Harari Region (e.g., Dire Dawa hub)
    key_intercity_corridors:
    - Addis Ababa – Hawassa
    - Addis Ababa – Gondar
    - Addis Ababa – Mekelle
    - Addis Ababa – Dire Dawa / Jigjiga
    - Addis Ababa – Jimma
    - Addis Ababa – Bahir Dar
    - Addis Ababa – Adama (Nazret)
languages:
  primary: Amharic (Ge'ez / Ethiopic script)
  l2_present_in_user_utterances:
  - Oromo (Latin script in standard written form; but spoken L2 users may produce
    Amharic utterances with Oromo lexical items)
  - Tigrinya (Ge'ez script; closely related to Amharic; intra-utterance mixing anticipated)
  - Somali (Latin script; less frequent code-switching)
  - Sidama, Wolayta, and other SNNP languages (low-frequency mixing)
  code_switching_note: Intra-utterance code-switching between Amharic and Oromo or
    Amharic and Tigrinya is anticipated among L2 Amharic speakers. INJONGO covers
    Oromo and Tigrinya as separate languages but does not document intra-utterance
    code-switching within Amharic utterances. Extent of code-switching in actual booking
    utterances is uncertain and was not controlled for in INJONGO curation.
  benchmark_language_coverage: Amharic (am), Oromo (om), and Tigrinya (ti) are each
    included in INJONGO as separate language tracks, but no code-switched Amharic
    track exists.
writing_systems:
  primary_script: Ge'ez (Ethiopic) script — used for Amharic and Tigrinya
  secondary_scripts:
  - Latin alphabet (Oromo in standard orthography; Somali)
  script_notes: Amharic uses the Ge'ez/Ethiopic abugida script. INJONGO's Amharic
    subset uses Ge'ez script throughout. No script mismatch exists between the benchmark
    and the deployment context. Code-switched Oromo terms in Amharic utterances may
    appear in either Ge'ez or Latin spelling depending on the speaker's literacy conventions
    — this boundary condition is undocumented in INJONGO.
  benchmark_script_match: Full match for primary Amharic deployment; code-switched
    token script handling is undocumented.
literacy_and_demographics:
  national_literacy_rate_ethiopia: '~71% adult literacy (ages 15+) as of 2022 per
    UNESCO/World Bank modelled estimates (statbase.org citing UNESCO UIS — [WEB-1];
    World Bank indicator — [WEB-2]).
    Caveat: an older UNESCO survey figure of ~51.8% (2017) circulates in older sources;
    the 71% figure reflects model-based interpolation from 2022. Addis Ababa literacy
    substantially higher than rural regional averages. Smartphone app deployment further
    selects for literate users.'
  amharic_l1_speaker_population: 'Approximately 29.3% of Ethiopia''s population (~128
    million as of 2024) speaks Amharic as a mother tongue, implying roughly 37–38
    million L1 Amharic speakers. Source: Ethio-ASR (2026 paper on Ethiopian multilingual
    ASR) — [WEB-3]. Caveat: this is cited in an NLP
    paper, not an official census figure; the 2007 Ethiopian census estimated ~29%
    but a new census has not been fully published.'
  amharic_l2_speaker_population_estimate: '[NEEDS VERIFICATION — deferred: below search
    budget; figure is noted as substantial given Amharic''s role as national lingua
    franca, but no reliable recent quantitative estimate found in searches. Requires
    Ethiopian CSA census data or ethnologue survey.]'
  smartphone_ownership_rate_ethiopia: '~15% of the population owned a smartphone as
    of 2024 (18% male, 6% female). Basic mobile phone ownership: 86% male, 65% female.
    Source: GSMA Mobile Economy Ethiopia 2024 report via birrmetrics.com — [WEB-4].
    This strong selection effect means the actual app-user population is skewed toward
    urban, male, higher-income travelers.'
  urban_rural_split_ethiopia: '[NEEDS VERIFICATION — deferred: below search budget;
    Ethiopia is predominantly rural (~80%+ rural by most estimates), but no recent
    official figure was retrieved in searches. World Bank indicator page surfaced
    but data not extracted.]'
  addis_ababa_population: '[NEEDS VERIFICATION — deferred: below search budget; commonly
    cited as 4–5 million in the city proper, 6–8 million in metro area, but no verified
    2023/2024 figure retrieved.]'
  intercity_bus_ridership_annual_estimate: '[NEEDS VERIFICATION — deferred: likely
    unsearchable at national aggregate level; no Ethiopian Transport Authority ridership
    statistics were found in searches.]'
  notes: 'Smartphone app deployment implies a positively selected subset of the general
    Ethiopian population: literate, smartphone-owning, and sufficiently data-connected
    to use an app. Rural travelers who board at regional depots may have lower average
    smartphone literacy than urban Addis Ababa users. The national smartphone penetration
    of ~15% underscores that the actual user population is a narrow urban-skewed segment
    of the Ethiopian public.'
cultural_norms_notes: '- Ethiopian Orthodox Christianity is the dominant religion;
  major holidays (Timkat/Epiphany, Meskel/Finding of the True Cross, Enkutatash/Ethiopian
  New Year, Genna/Christmas) drive significant demand surges for intercity travel
  bookings.

  - The Ethiopian calendar (Ge''ez calendar) is 13 months long, runs approximately
  7–8 years behind the Gregorian calendar, and has distinct month names (Meskerem,
  Tikimt, Hidar, Tahsas, Tir, Yekatit, Megabit, Miazia, Ginbot, Sene, Hamle, Nehase,
  Pagume). Users are expected to reference travel dates using these month names natively.

  - Ethiopian time convention: the clock is offset by 6 hours from standard international
  convention (1:00 Ethiopian time = 7:00 AM internationally). Bus departure times
  quoted in user utterances may follow Ethiopian clock convention.

  - Communal travel norms: travelers frequently book on behalf of extended family
  members; utterances may reference third-party passengers.

  - Respect for elders and hierarchical deference may influence how users phrase requests
  or corrections to booking agents.

  - Code-switching between Amharic and Oromo, Tigrinya, or other regional languages
  is socially unremarkable and pragmatically functional in multi-ethnic urban contexts
  such as Addis Ababa.

  - Seat-class terminology may vary by operator (e.g., VIP/economy on Sky Bus or Selam
  Bus); users may use operator-specific colloquial terms not present in any benchmark.'
infrastructure_notes: '- Deployment is text-based smartphone app; INJONGO is a text-only
  benchmark — full modality match, no audio or speech interface concerns.

  - Mobile internet penetration in Ethiopia: 19.4% of population (24.83 million users)
  as of January 2024. Source: DataReportal Digital 2024 Ethiopia — [WEB-5].

  - Mobile network coverage: 3G covers ~98% of population (2023); 4G coverage at ~33%
  of population (2023). Source: GSMA Mobile Economy Ethiopia Report, October 2024
  — [WEB-6].
  This implies significant 4G connectivity gaps on rural intercity corridors.

  - Dominant mobile network operators: Ethio Telecom (state-owned, ~94.5% market share
  with 78.3 million subscribers as of June 2024) and Safaricom Ethiopia (launched
  October 2022, ~5.5% share with 4.6 million subscribers). Source: Business Daily
  Africa citing Ethio Telecom IPO prospectus — [WEB-7].
  Safaricom''s entry in 2022 broke Ethio Telecom''s decades-long monopoly and prompted
  ~70% cuts in mobile data tariffs.

  - Smartphone OS distribution among Ethiopian app users (Android vs. iOS split):
  [NEEDS VERIFICATION — deferred: below search budget; Android dominance is expected
  given smartphone price points (~5,000 ETB entry-level) but no Ethiopia-specific
  OS share figure was retrieved.]

  - Ge''ez script keyboard availability and input method editor (IME) quality on Android:
  [NEEDS VERIFICATION — deferred: likely unsearchable at quantitative level; qualitative
  evidence from Ethiopian NLP community indicates Ge''ez IME support is available
  on major Android distributions but quality varies by device tier.]

  - Connectivity quality on intercity routes (bus depots, en-route rest stops): 4G
  coverage at only 33% of population as of 2023; rural and intercity corridor connectivity
  is predominantly 3G or below. Users on long-haul routes (e.g., Addis–Gondar, Addis–Mekelle)
  will likely experience intermittent connectivity. This creates a latency/offline-resilience
  requirement not reflected in any INJONGO evaluation setting.

  - Data cost per MB for Ethiopian mobile users relative to income: Ethio Telecom
  has cut data tariffs by ~70% since 2017 following Safaricom''s competitive entry;
  median mobile download speed was 27.19 Mbps as of early 2024. Source: DataReportal
  2024 — [WEB-5]. Absolute data
  cost relative to income remains a barrier for low-income rural users.

  - Ethio Telecom market share and competitive landscape: Duopoly as of 2024. Ethio
  Telecom dominates with ~94.5% subscriber share; Safaricom Ethiopia holds ~5.5%.
  A third license tender was suspended in November 2023 after no bids received. Sources:
  Business Daily Africa — [WEB-7];
  Connecting Africa/Omdia — [WEB-8].'
calendar_and_temporal_conventions:
  ethiopian_calendar_months:
  - Meskerem (September–October)
  - Tikimt (October–November)
  - Hidar (November–December)
  - Tahsas (December–January)
  - Tir (January–February)
  - Yekatit (February–March)
  - Megabit (March–April)
  - Miazia (April–May)
  - Ginbot (May–June)
  - Sene (June–July)
  - Hamle (July–August)
  - Nehase (August–September)
  - Pagume (intercalary month, 5–6 days)
  injongo_date_slot_coverage_of_ethiopian_calendar: NOT DOCUMENTED — INJONGO's DATE
    slot annotation guide examples use Gregorian conventions only; whether Ge'ez month
    names appear as valid DATE slot values in the Amharic training instances is a
    flagged gap requiring web search verification.
  ethiopian_time_convention_note: Users may quote bus departure times in Ethiopian
    clock convention (offset by 6 hours from international standard); TIME slot extraction
    should accommodate this convention. Undocumented in INJONGO.
  major_travel_surge_events:
  - event: Timkat (Ethiopian Epiphany)
    approximate_gregorian_date: 'January 19–20 (fixed in Ethiopian calendar: 11 Tir;
      Gregorian equivalent varies slightly by year and by Ethiopian Orthodox vs. Eritrean
      Orthodox reckoning). Gregorian date is typically January 19 in non-leap years,
      January 20 in leap years.'
  - event: Meskel (Finding of the True Cross)
    approximate_gregorian_date: 'September 27 (fixed in Ethiopian calendar: 17 Meskerem;
      Gregorian September 27 in non-leap years, September 28 in leap years).'
  - event: Enkutatash (Ethiopian New Year)
    approximate_gregorian_date: 'September 11 (Ethiopian calendar: 1 Meskerem; September
      12 in leap years).'
  - event: Genna (Ethiopian Christmas)
    approximate_gregorian_date: 'January 7 (Ethiopian calendar: 29 Tahsas; corresponds
      to Julian December 25).'
  - event: Fasika (Ethiopian Easter)
    approximate_gregorian_date: Variable — determined by Ethiopian Orthodox computus,
      typically April–May; can differ by weeks from Western Easter. Exact date changes
      each year.
slot_filling_ethiopia_specific:
  city_toponym_coverage:
    key_ethiopian_cities_in_scope:
    - 'Addis Ababa (also: አዲስ አበባ, colloquial abbrev. ''Addis'')'
    - 'Hawassa (also: Awassa)'
    - 'Mekelle (also: Mekele)'
    - Gondar
    - Bahir Dar
    - Dire Dawa
    - Jimma
    - Adama (Nazret)
    - Dessie
    - Shashamane
    - Jigjiga
    - Arba Minch
    - Dilla
    - Woldia
    injongo_toponym_coverage_status: 'NOT DOCUMENTED — CITY_OR_PROVINCE and PLACE_NAME
      slots exist in INJONGO, but whether Amharic travel-domain instances include
      Ethiopian intercity toponyms (vs. generic or pan-African city references) is
      unverified. The GitHub dataset shows a banking-domain Amharic example referencing
      ''አባይ ባንክ'' (Abay Bank), suggesting culturally grounded Ethiopian entities are
      used in at least the banking domain (Source: INJONGO GitHub — [WEB-9]),
      but travel-domain toponym coverage remains unverified.'
    amharic_spelling_variation_note: Many Ethiopian city names have multiple attested
      Amharic spellings and abbreviations; slot extraction must handle orthographic
      variation.
  currency_and_fare:
    currency: 'Ethiopian Birr (ETB; symbol: ብር or Br)'
    fare_tier_conventions:
    - VIP / First class (long-haul bus, e.g., Sky Bus, Selam Bus)
    - Economy / Regular class
    - Express service variants
    injongo_birr_coverage_status: 'NOT DOCUMENTED — CURRENCY and MONEY slot types
      are present in INJONGO, and cultural entity substitution is documented for South
      African Rand; whether ETB/Birr appears in Amharic training instances is unverified.
      The GitHub example shows Amharic banking utterances use Ethiopian bank names,
      consistent with local entity substitution, but fare/currency slot coverage in
      the travel domain specifically remains unconfirmed (Source: INJONGO GitHub —
      [WEB-9]).'
    pricing_range_typical: '[NEEDS VERIFICATION — deferred: below search budget; typical
      Addis–Hawassa (~275 km), Addis–Gondar (~750 km) fare ranges in Birr for VIP
      vs. economy classes require operator-level current pricing data not found in
      searches.]'
  operator_specific_intents:
    sky_bus:
      known_service_features: '[NEEDS VERIFICATION — deferred: below search budget;
        operator-specific cancellation policy and booking API structure not publicly
        documented in sources retrieved.]'
      operator_specific_intents_not_in_injongo:
      - seat-class upgrade
      - VIP seat selection
      - road-closure rebooking
      - agent-assisted cancellation
    selam_bus:
      known_service_features: '[NEEDS VERIFICATION — deferred: below search budget;
        operator-specific cancellation policy and booking API structure not publicly
        documented in sources retrieved.]'
      operator_specific_intents_not_in_injongo:
      - seat-class upgrade
      - route suspension query
      - group booking
    ride:
      known_service_features: '[NEEDS VERIFICATION — deferred: below search budget;
        ride-hail vs. intercity scope, platform features not documented in retrieved
        sources.]'
      operator_specific_intents_not_in_injongo:
      - ride type selection
      - driver preference
      - shared ride booking
    injongo_travel_intent_coverage_note: INJONGO's travel domain contains generic
      intents (e.g., 'exchange rate', 'book flight') derived from CLINC. Operator-specific
      intercity bus flows (seat-class selection, road-closure rebooking, holiday-surge
      booking, platform-specific cancellation) are absent from the 40-intent taxonomy.
      Gap analysis between INJONGO travel intents and actual operator booking APIs
      is recommended.
annotator_population_vs_user_population:
  injongo_annotator_profile_amharic:
    documented: Native Amharic speakers; recruited via a Kenyan logistics company;
      compensated at per-country rates.
    undocumented:
    - Regional origin within Ethiopia (Addis Ababa vs. other regions)
    - Urban vs. rural background
    - L1 vs. L2 Amharic status
    - Age distribution
    - Education level
    - Familiarity with intercity bus booking apps
    concern: Addis Ababa–centric annotator pool is a plausible hypothesis given urbanization
      of Amharic NLP resources; if so, slot instances may under-represent regional
      city names, route-specific terminology, and phrasing patterns of non-Addis travelers.
  actual_user_population_characteristics: Includes L2 Amharic speakers from Oromia
    (Oromo L1), Tigray (Tigrinya L1), SNNP, and Somali regions; code-switching anticipated;
    regional toponyms and fare conventions vary by corridor.
  annotator_user_mismatch_risk: HIGH — L2 Amharic speakers and code-switched utterances
    are likely underrepresented in INJONGO Amharic annotations; label validity for
    code-switched or regionally accented slot expressions is a primary construct-validity
    concern.
  web_search_target: INJONGO paper annotator section — Amharic subset regional demographics,
    recruitment methodology detail
code_switching_profile:
  anticipated_patterns:
  - Amharic matrix utterance with Oromo city/place names (e.g., Jimma, Adama in Oromo
    phonology)
  - Amharic matrix utterance with Tigrinya lexical items for route segments near Tigray
  - Amharic utterances with English loanwords for booking terminology (e.g., 'seat',
    'ticket', 'cancel')
  - Numerals and fare amounts sometimes vocalized in Oromo or Amharic depending on
    speaker
  injongo_code_switching_coverage: INJONGO covers Oromo and Tigrinya as independent
    language tracks but does not document intra-utterance Amharic–Oromo or Amharic–Tigrinya
    code-switching. No known Ethiopian NLP benchmark specifically addresses this phenomenon
    for intent detection or slot-filling.
  net_new_ethiopian_code_switching_research: 'A 2025 EthioNLP workshop paper (Tadesse
    et al.) addresses morphology-aware sentiment analysis of code-switched Ethiopian
    social media posts mixing Amharic, Afaan Oromo, and Tigrinya, using HornMorpho
    and XLM-R under multi-task learning. This is the closest known work to the deployment''s
    code-switching challenge, but covers sentiment — not intent detection or slot-filling.
    Source: EthioNLP workshop proceedings — [WEB-10]. Confirms
    the gap: no intent/slot benchmark for code-switched Ethiopian utterances exists.'
  web_search_target: Amharic Oromo Tigrinya code-switching NLP benchmark Ethiopian
    language mixing intent detection slot filling
regulatory_and_policy_context:
  ethiopian_data_protection_framework: 'Ethiopia''s first comprehensive Personal Data
    Protection Proclamation (No. 1321/2024) was passed by the Federal House of Representatives
    on April 4, 2024, and officially published in the Federal Negarit Gazette on July
    24, 2024, entering into force on that date. The law covers all automated and non-automated
    personal data processing by controllers/processors established in Ethiopia or
    using equipment in Ethiopia. The Ethiopian Communications Authority (ECA) is designated
    as the independent supervisory authority. The law includes rights of data subjects
    (access, erasure, rectification, object to automated decisions), data localization
    requirements (personal data must be stored domestically unless conditions for
    cross-border transfer are met), and mandates registration of controllers/processors
    with the ECA. Sources: CIPIT analysis — [WEB-11];
    Mondaq business guide — [WEB-12];
    DLA Piper tracker — [WEB-13].
    Relevance: the booking system collects personal traveler data (names, routes,
    payment); the operators must register with ECA and conduct DPIAs for high-risk
    automated processing.'
  transport_sector_regulation: '[NEEDS VERIFICATION — deferred: below search budget;
    Ethiopian Transport Authority regulations specifically applicable to digital booking
    platforms for intercity buses were not surfaced in searches. Likely requires direct
    review of Ethiopian federal transport proclamations.]'
  telecom_regulatory_body: 'Ethiopian Communications Authority (ECA) — established
    under Proclamation No. 1148/2019 as the independent regulator for the telecom
    sector post-liberalization. ECA also serves as the data protection supervisory
    authority under PDPP 1321/2024. ECA sets mobile and fixed termination rates and
    issues operator licenses. Source: ECA referenced across multiple search results
    — [WEB-14].'
  ai_policy_ethiopia: 'Ethiopia has a National Artificial Intelligence Policy referenced
    alongside the PDPP 2024 as the data governance framework for responsible AI deployment.
    The policy is referenced in Proclamation 1321/2024''s context but its full content
    and effective date were not retrieved in detail. Source: regulations.ai PDPP analysis
    — [WEB-15]. Ethiopia''s Digital
    Ethiopia 2025 strategy and the 2020–2030 program also set targets for digital
    transformation that contextualize NLP system deployment. Caveat: the specific
    scope and enforcement provisions of the AI policy remain unverified in detail
    — deferred below search budget.'
domain_specific_notes: '- Travel domain is directly relevant: INJONGO includes Travel
  as one of 5 domains, with intents covering generic travel booking scenarios.

  - Key gap: INJONGO''s travel intents are derived from CLINC (''exchange rate'',
  ''book flight'') and do not include intercity bus-specific flows that are the actual
  deployment use case (road-closure rebooking, seat-class upgrade, operator-specific
  cancellation).

  - Ethiopian calendar is the operative temporal reference system for users; Gregorian-only
  DATE slot annotation in INJONGO is a direct failure mode for travel-date slot extraction.

  - Birr (ETB) should in principle be extractable via CURRENCY/MONEY slots, and the
  INJONGO GitHub dataset shows culturally grounded Ethiopian entities in the banking
  domain (e.g., Abay Bank), but empirical coverage of Birr in Amharic travel-domain
  INJONGO instances is unverified.

  - Ethiopian intercity bus fare structure (VIP vs. economy, route-specific pricing)
  produces slot value distributions unlikely to appear in INJONGO''s training data.

  - No Ethiopian NLP corpus is known to cover Amharic-language fare-slot or date-slot
  extraction for bus booking specifically; the closest resources are EthioLLM/EthioBenchmark
  (NER, classification, MT tasks — not intent/slot) and INJONGO itself.

  - INJONGO''s fixed 80-utterances-per-intent distribution does not reflect real booking
  interaction frequency (e.g., route queries and seat selection will dominate over
  less frequent intents in actual operator logs).

  - LLM zero-shot slot-filling performance on INJONGO Amharic is expected to be substantially
  below fine-tuned baselines; GPT-4o achieves only ~26% average F1 zero-shot across
  African languages; Amharic-specific figure requires verification from per-language
  Table 5 in the INJONGO paper (not fully extractable from available search snippets).'
benchmark_amharic_performance_data:
  best_finetuned_model_intent_detection_accuracy_avg_all_languages: 93.7% (AfroXLMR-76L)
  best_finetuned_model_slot_filling_f1_avg_all_languages: 85.6% (AfroXLMR-76L)
  gpt4o_zero_shot_intent_detection_avg_all_african_languages: 70.6%
  gpt4o_zero_shot_slot_filling_f1_avg_all_african_languages: 26%
  amharic_specific_intent_detection_accuracy: '[NOT FOUND — searched INJONGO paper
    PDF (arXiv 2502.09814), ResearchGate, ACL Anthology, and OpenReview; Table 5 per-language
    columns (amh, ewe, hau, ...) are confirmed to exist in the paper but the specific
    Amharic (amh) accuracy value was not extractable from available search snippets.
    The per-language row data is present in the full paper PDF. Downstream assessors
    should consult Table 5 of the ACL 2025 paper directly: [WEB-16]]'
  amharic_specific_slot_filling_f1: '[NOT FOUND — same limitation as intent detection;
    per-language F1 for Amharic slot-filling requires direct inspection of Table 5
    in the INJONGO paper. ACL Anthology full paper: [WEB-16]]'
  amharic_initial_fleiss_kappa_before_review: '0.836 — sourced from INJONGO Table
    8 (dataset statistics across 17 languages). Source: ResearchGate full-text snippet
    — [WEB-17]'
  amharic_fleiss_kappa_after_review: '0.933 (+0.096 improvement) — sourced from INJONGO
    Table 8. Among the 16 languages, Amharic showed modest improvement compared to
    Sesotho (+0.327) and Zulu (+0.294). The initial Amharic kappa of 0.836 was already
    the second-highest after Shona (0.934), suggesting Amharic annotation was relatively
    consistent from the start. Source: ResearchGate full-text snippet — [WEB-17]'
  note: Swahili (high web-resource language) achieves near-English performance (~80.6%
    accuracy with Llama 3.3 70B); Amharic is lower-resource and likely achieves lower
    scores, but exact figures require verification from per-language result tables
    in the INJONGO paper. The INJONGO GitHub repository (McGill-NLP/Injongo — [WEB-9])
    provides direct access to the Amharic (amh) dataset instances, which could be
    inspected to assess Ethiopian toponym and Birr currency coverage empirically.
net_new_fields:
  ethiopian_nlp_ecosystem_context:
    ethiollm_and_ethiobenchmark: 'EthioLLM (Tonja et al., LREC-COLING 2024) introduced
      multilingual LLMs for five Ethiopian languages (Amharic, Ge''ez, Afan Oromo,
      Somali, Tigrinya) and EthioBenchmark covering NER, POS tagging, news classification,
      machine translation, and sentiment analysis tasks. Notably, EthioBenchmark does
      NOT include intent detection or slot-filling. Source: ACL Anthology — [WEB-18].
      Relevance: confirms that INJONGO is the only available benchmark covering Ethiopian-language
      intent/slot tasks, and that EthioLLM models could serve as strong baselines
      for Amharic slot-filling.'
    amharic_as_l2_lingua_franca: 'Amharic functions as the most learned second language
      across Ethiopia, used by speakers of Oromo, Tigrinya, Somali, and other languages
      for inter-ethnic communication. This L2 dominance underpins the code-switching
      concern: the actual user base is heavily L2-Amharic. Source: Ethio-ASR paper
      citing ~29.3% L1 speaker rate — [WEB-3].'
    afar_oromo_somali_tigrinya_now_official_languages: 'As of recent constitutional
      changes, Afar, Oromo, Somali, and Tigrinya have been recognized as additional
      official working languages of Ethiopia alongside Amharic. This changes the sociolinguistic
      context for Amharic-only NLP deployment: users in Oromia, Tigray, and the Somali
      region may have growing expectations for their L1 language to be supported.
      Source: Ethio-ASR paper — [WEB-3].'
    afrobench_includes_injongo_amharic: 'AfroBench (ACL 2025 Findings) includes INJONGO
      as one of its evaluated benchmarks and covers Amharic among its 14 languages,
      providing a multi-benchmark context for Amharic LLM performance. Source: ACL
      Anthology — [WEB-19]. Net-new
      relevance: AfroBench results may provide additional Amharic-specific INJONGO
      performance data beyond what is in the INJONGO paper itself.'
  telecom_infrastructure_connectivity_risks:
    4g_coverage_gap_on_intercity_corridors: Only 33% population 4G coverage nationally
      as of 2023 (GSMA). Most intercity corridors outside the Addis Ababa–Adama axis
      will be predominantly 3G. Median mobile download speed of 27.19 Mbps nationally
      (DataReportal 2024 — [WEB-5])
      likely overstates corridor-level speeds. The booking app must tolerate intermittent
      or low-bandwidth conditions.
    ethio_telecom_data_tariff_reduction: 'Safaricom Ethiopia''s entry in October 2022
      forced Ethio Telecom to cut mobile data tariffs by ~70%, improving affordability.
      Source: Mordor Intelligence Ethiopia Telecom Market report — [WEB-20].
      Relevance: improved data affordability increases the feasible user base for
      smartphone booking apps but does not resolve the coverage gap on rural corridors.'
flagged_gaps_summary:
- gap_id: 1
  label: Ethiopian calendar slot coverage
  priority: HIGH
  description: INJONGO DATE slot annotation examples use Gregorian conventions only;
    Ge'ez calendar month names (Meskerem, Tikimt, etc.) are not documented as valid
    DATE slot values. This is a direct failure mode for travel-date extraction.
  web_search_target: Ethiopian calendar Amharic NLP date extraction Ge'ez months Meskerem
    Tikimt slot filling INJONGO
  search_outcome: NOT FOUND — No published work on Ethiopian calendar date extraction
    for Amharic NLP was surfaced. The INJONGO paper does not document Ethiopian calendar
    accommodation. EthioBenchmark covers NER but not date slot filling with Ethiopian
    calendar conventions. This gap is unresolved and constitutes a high-risk construct-validity
    issue.
- gap_id: 2
  label: Ethiopian city/toponym coverage in slot instances
  priority: HIGH
  description: CITY_OR_PROVINCE and PLACE_NAME slots exist but whether Amharic travel-domain
    instances include Ethiopian intercity toponyms (Hawassa, Mekelle, Gondar, Dire
    Dawa, Jimma) is undocumented.
  web_search_target: INJONGO Amharic travel domain slot instances Ethiopian city names
    toponym coverage
  search_outcome: 'PARTIALLY RESOLVED — The INJONGO GitHub dataset shows Amharic banking-domain
    utterances use Ethiopian bank names (e.g., ''አባይ ባንክ'' = Abay Bank), confirming
    culturally grounded entity substitution in at least one domain. Source: [WEB-9].
    However, travel-domain toponym coverage (intercity city names) remains empirically
    unverified. Direct inspection of the Amharic travel-domain split in the dataset
    is required.'
- gap_id: 3
  label: Code-switching (Amharic–Oromo, Amharic–Tigrinya) in utterances
  priority: HIGH
  description: INJONGO covers Oromo and Tigrinya separately but has no intra-utterance
    code-switching track. User utterances from L2 Amharic speakers are expected to
    contain code-switched tokens.
  web_search_target: Amharic Oromo Tigrinya code-switching NLP benchmark Ethiopian
    language mixing intent detection slot filling
  search_outcome: CONFIRMED GAP — No intent detection or slot-filling benchmark for
    code-switched Amharic–Oromo or Amharic–Tigrinya utterances exists. EthioNLP community
    has emerging work on code-switched sentiment analysis (morphology-aware, multi-task
    learning) using XLM-R + HornMorpho (Tadesse et al., EthioNLP 2025 — [WEB-10]),
    but this covers sentiment, not intent/slot. The gap is a genuine documentation
    hole in the Ethiopian NLP ecosystem.
- gap_id: 4
  label: Annotator demographic representativeness
  priority: HIGH
  description: INJONGO's Amharic annotator regional origin, L1/L2 status, and urban/rural
    background are undisclosed. Addis Ababa–centric annotators may produce a distribution
    poorly matched to non-Addis traveler utterances.
  web_search_target: INJONGO paper annotator section Amharic demographics regional
    Ethiopia NLP crowdsourcing
  search_outcome: NOT FOUND — The INJONGO paper confirms annotators were native speakers
    recruited via a Kenyan logistics company compensated at per-country rates, but
    no regional origin, urban/rural breakdown, or L1/L2 Amharic status data for the
    Amharic annotator pool is published. Multiple versions of the paper were searched
    (arXiv, ACL Anthology, OpenReview) without finding additional demographic detail.
    This demographic opacity is an inherent limitation of the benchmark for this deployment.
- gap_id: 5
  label: Operator-specific intent gaps (Sky Bus, Selam Bus, Ride)
  priority: MODERATE
  description: INJONGO's 40-intent travel taxonomy is derived from generic CLINC intents
    and does not include seat-class selection, road-closure rebooking, or operator-specific
    cancellation flows.
  web_search_target: Ethiopian intercity bus booking intent taxonomy Sky Bus Selam
    Bus conversational AI NLP
  search_outcome: NOT FOUND — No published intent taxonomy or conversational AI dataset
    specific to Ethiopian intercity bus booking operators was found. Operator-specific
    booking flows must be elicited directly from Sky Bus, Selam Bus, and Ride APIs/documentation.
- gap_id: 6
  label: Birr fare tiers and pricing utterances
  priority: MODERATE
  description: CURRENCY/MONEY slots are present, but whether Birr (ETB) and Ethiopian
    fare-tier conventions (VIP vs. economy) appear in Amharic INJONGO instances is
    undocumented.
  web_search_target: Ethiopian Birr fare extraction Amharic NLP e-commerce transport
    corpus slot filling ETB
  search_outcome: 'PARTIALLY RESOLVED — INJONGO GitHub shows culturally grounded Ethiopian
    entities in banking domain (Abay Bank). No published Amharic transport fare corpus
    exists. Direct dataset inspection required. Source: [WEB-9].'
- gap_id: 7
  label: Ethiopian holiday calendar events in slot instances
  priority: MODERATE
  description: CALENDAR_EVENT slot type exists, but whether Ethiopian religious holidays
    (Timkat, Meskel, Enkutatash) appear as travel-domain slot instances is undocumented.
  web_search_target: Ethiopian holiday Timkat Meskel travel booking NLP Amharic calendar
    event slot INJONGO
  search_outcome: NOT FOUND — No evidence that Ethiopian religious holidays appear
    in INJONGO's CALENDAR_EVENT slot training instances. The annotation guide does
    not reference Ethiopian holidays. Approximate Gregorian dates for all major Ethiopian
    holidays have been resolved in the calendar_and_temporal_conventions section above.
- gap_id: 8
  label: Amharic-specific per-language performance metrics
  priority: MODERATE
  description: Aggregate INJONGO results are reported across all African languages;
    per-language breakdowns for Amharic on intent detection accuracy and slot-filling
    F1 are not surfaced in the registry summary.
  web_search_target: INJONGO Amharic per-language results intent detection slot filling
    accuracy F1 Table 5 paper
  search_outcome: 'PARTIALLY RESOLVED — Table 5 per-language columns confirmed to
    include ''amh'' (Amharic). Amharic Fleiss'' Kappa scores have been resolved: initial
    κ = 0.836, post-review κ = 0.933. Per-language intent detection accuracy and slot-filling
    F1 for Amharic require direct reading of Table 5 in the full paper PDF (ACL Anthology
    — [WEB-16]). Snippet extraction was
    insufficient to retrieve the exact numerical values.'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://statbase.org/data/wld-literacy-rate/ |
| WEB-2 | https://data.worldbank.org/indicator/SE.ADT.LITR.ZS?locations=ET |
| WEB-3 | https://arxiv.org/html/2603.23654 |
| WEB-4 | https://birrmetrics.com/ethiopia-narrows-mobile-gender-gap-to-24-but-smartphone-access-for-women-remains-just-6/ |
| WEB-5 | https://datareportal.com/reports/digital-2024-ethiopia |
| WEB-6 | https://www.gsma.com/about-us/regions/sub-saharan-africa/wp-content/uploads/2024/10/GSMA_Ethiopia-Report_Oct-2024_v2-1.pdf |
| WEB-7 | https://www.businessdailyafrica.com/bd/corporate/companies/safaricom-ethiopia-market-share-hits-5-5pc-in-22-months-4799324 |
| WEB-8 | https://www.connectingafrica.com/connectivity/ethiopia-s-telecoms-liberalization-makes-progress-omdia |
| WEB-9 | https://github.com/McGill-NLP/Injongo |
| WEB-10 | https://ethionlp.github.io/ |
| WEB-11 | https://cipit.org/ethiopias-personal-data-protection-proclamation-of-2024-and-its-budding-digital-identity-regime/ |
| WEB-12 | https://www.mondaq.com/privacy-protection/1766200/ethiopian-personal-data-protection-law-proclamation-13212024-business-compliance-guide |
| WEB-13 | https://www.dlapiperdataprotection.com/index.html?t=law&c=ET |
| WEB-14 | https://eca.et/wp-content/uploads/2024/05/Determination-on-Mobile-and-Fixed-Termination-Rates.pdf |
| WEB-15 | https://regulations.ai/regulations/RAI-ET-NA-PDPPNXX-2024 |
| WEB-16 | https://aclanthology.org/2025.acl-long.464.pdf |
| WEB-17 | https://www.researchgate.net/publication/389056008_INJONGO_A_Multicultural_Intent_Detection_and_Slot-filling_Dataset_for_16_African_Languages |
| WEB-18 | https://aclanthology.org/2024.lrec-main.561/ |
| WEB-19 | https://aclanthology.org/2025.findings-acl.976.pdf |
| WEB-20 | https://www.mordorintelligence.com/industry-reports/ethiopia-telecom-mno-market |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Does the system need to handle intents specific to Ethiopian intercity travel — e.g., route queries between regional cities, holiday-surge bookings (Timkat, Meskel), operator-specific seat classes, or rebooking due to road closures?
A1: The user acknowledges INJONGO covers general domains but considers Ethiopian bus/ride-share booking flows broadly comparable. The expectation is that the system handles all standard travel scenarios without requiring a heavily expanded, operator-specific intent taxonomy.

Q2 [IC]: Will users' slot values reflect Ethiopian-specific conventions — Amharic city names/abbreviations, Ethiopian calendar dates (Meskerem, Tikimt), and fares quoted in Birr with local pricing tiers — and does the system need to extract these correctly?
A2: Yes — users' natural utterances are expected to follow these conventions (local city names, Ethiopian calendar, Birr-denominated fares), and correct slot extraction of these values is a system requirement.

Q3 [OC]: Are there systematic phrasing differences across the commuter population — e.g., code-switching with Oromo or Tigrinya words for routes or city names — that a single native-Amharic annotator profile might not capture?
A3: Yes, code-switching is anticipated, particularly Amharic mixed with other Ethiopian languages, though the extent is uncertain and was not specifically controlled for in INJONGO's curation.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | The user accepts INJONGO's general travel intents as broadly sufficient, but operator-specific flows (rebooking on road closures, seat-class selection) and Ethiopian holiday demand patterns remain unchecked against the benchmark's intent set. |
| IC | HIGH | Users will produce slot values in Ethiopian calendar dates, Amharic city names/abbreviations, and Birr-denominated fares — none of which are likely represented in INJONGO's travel-domain slot instances, creating direct construct-irrelevant variance in slot-filling evaluation. |
| IF | LOWER | Deployment is text-only on smartphones, matching INJONGO's text input modality and Amharic script coverage exactly. |
| OO | MODERATE | INJONGO's 40-intent taxonomy was designed ground-up with African contexts, which is a strength, but the travel subdomain's intent granularity for long-distance bus booking (vs. generic travel) has not been verified against operator booking flows. |
| OC | HIGH | Annotators were native Amharic speakers, but the actual user base includes L2 Amharic speakers who code-switch with Oromo or Tigrinya; this annotator–user mismatch is likely to reduce label validity for code-switched or regionally accented slot expressions. |
| OF | LOWER | The benchmark's label output (intent class + slot tags) matches the deployment's structured output requirements for a task-oriented dialogue system. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** masakhane/InjongoIntent (configs: amh, eng, ewe, hau, ibo, kin, lin, lug, orm, sna, sot, swa, twi, wol, xho, yor, zul)
**Analysis date:** 2025-07-15
**Examples reviewed:** 224 total (19 amh, 13 eng, 14 ewe, 16 hau, 16 ibo, 13 kin, 13 lin, 15 lug, 13 orm, 11 sna, 27 sot, 13 swa, 13 twi, 15 wol, 14 xho, 14 yor, 11 zul)
**Columns shown:** intent, text, spans, target, example_id (+ raw in eng config)
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | amh | train-00000042 | book_flight | "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ።" | "Book me a flight from Dire Dawa to Bahir Dar for Meskerem fifth." | IC |
| D2 | amh | train-00000042 | book_flight | target: "CITY_OR_PROVINCE: ድሬዳዋ $$ CITY_OR_PROVINCE: ባህርዳር $$ DATE: መስከረም አምስት" | Slot annotations for Dire Dawa, Bahir Dar (Ethiopian cities), and Meskerem (Ethiopian calendar month) | IC, OO |
| D3 | amh | train-00000016 | balance | "የአማራ ባንክ አካውንቴ ስንት አለው" / target: "BANK_NAME: አማራ ባንክ" | "How much is in my Amhara Bank account?" — Ethiopian bank name annotated | IC |
| D4 | amh | train-00000018 | balance | "ንግድ ባንክ ላይ የቀረኝ ገንዘብ አለ" / target: "BANK_NAME: ንግድ ባንክ" | "Is there money left in Commercial Bank [of Ethiopia]?" — major Ethiopian bank | IC |
| D5 | amh | train-00000003 | balance | "በቴሌብር የብድር አካውንቴ ላይ …" / target: "PAYMENT_COMPANY: ቴሌብር" | "In my TeleBirr credit account…" — TeleBirr is Ethiopia's dominant mobile payment platform | IC |
| D6 | amh | train-00000011 | car_rental | "ከሃምሌ 4 እስከ 6 የቤት መኪና ኪራይ ማግኘት እችላለሁ?" / target: "DATE: ከሃምሌ 4 እስከ 6" | "Can I find a car rental from Hamle 4 to 6?" — Hamle is the 11th month of Ethiopian calendar | IC, OO |
| D7 | amh | train-00000041 | book_flight | "ወደ ቱርክ በፍጥነት የምደርስበት የበረራ አማራጭ ንገረኝ།" / target: "COUNTRY: ቱርክ" | "Tell me a flight option to get to Turkey quickly." — international destination, no Ethiopian intercity booking | IO |
| D8 | amh | train-00000047 | book_flight | "ወደ ሱዳን የበረራ ትኬት ያስፈልገኛል።" / target: "COUNTRY: ሱዳን" | "I need a flight ticket to Sudan." — international destination, not intercity bus | IO |
| D9 | eng (raw=amh) | train-00000053 | travel_suggestion | raw: "ለቀጣይ የጉብኝት ጉዞዬ በሃዋሳ እና በአርባ ምንጭ መካከል…" / text: "help me decide between Hawassa and Arbaminch…" | Ethiopian cities Hawassa and Arba Minch appear as travel suggestions — confirms cultural grounding | IC |
| D10 | eng (raw=amh) | train-00000092 | spending_history | raw: "ከቴሌ ብር አካዉንቴ ገንዘብ ለማን ለማን እንደላኩ ዝርዝሩን አሳየኝ?" / text: "Show me history of my telebirr transfers?" | TeleBirr payment company referenced in Amharic utterance | IC |
| D11 | amh | train-00000045 | alarm | "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ በደንብ እንዲሰማኝ ድምጽ ጨምርበት" | "Make the alarm I set for tomorrow morning at 12 o'clock ring loudly." — TIME slot unnanotated despite "12 ሰአት" | OC |
| D12 | orm | train-00000041 | book_flight | "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" | "Book me an Ethiopian Airlines flight from Dire Dawa to Bole then to Jimma." — spans empty despite city names and airline | OC |
| D13 | orm | train-00000011 | car_rental | "Ebila 12 hanga Ebila 14tti Mattuu keessatti kireeffannaa konkolaataa argachuun ni danda'amaa" / target: "DATE: Ebila 12 hanga Ebila 14 $$ CITY_OR_PROVINCE: Mattuu" | Oromo month name "Ebila" (April) used as date slot — culturally grounded Ethiopian Oromo calendar | IC, OO |
| D14 | orm | train-00000035 | calendar_update | "Sagantaa sirna cidhaaf sadaasa 21tti qabame kalaandarii koo irraa haqi maloo" / target: "CALENDAR_EVENT: sirna cidhaa $$ DATE: sadaasa 21" | Oromo month "Sadaasa" (November in Oromo calendar) used as date slot | IC, OO |
| D15 | amh | train-00000052 | bill_balance | "የዚህ ወር መከፈል ያለባቸውን የፍጆታ ዝርዝር አሳየኝ።" / target: "DATE: የዚህ ወር" | "Show me the utility list to be paid this month." — relative date expression, not calendar month name | OO |
| D16 | amh | train-00000053 | car_rental | "ከሚመጣው ወር ጀምሮ ለ3 ወር ቶዮታ መኪና መከራየት እፈልጋለሁ።" / target: "DATE: ከሚመጣው ወር ጀምሮ ለ3 ወር" | "I want to rent a Toyota car starting next month for 3 months." — relative date, no named calendar month | OO |
| D17 | amh | train-00000031 | confirm_reservation | "በቶቶት ለቃለአብ ቦታ ማስያዝ እንዳለብኝ…" / target: "RESTAURANT_NAME: ቶቶት $$ PERSONAL_NAME: ቃለአብ" | Restaurant "ቶቶት" (Totot) — Ethiopian cultural reference; personal name "ቃለአብ" is distinctly Ethiopian | IC |
| D18 | amh | train-00000051 | bill_balance | "የቦሎ ማሳደሻ ስንት ነው" / target: "BILL_TYPE: የቦሎ ማሳደሻ" | "What is the Bole maintenance/upgrade fee?" — "ቦሎ" likely refers to Bole (Addis Ababa district) | IC |
| D19 | hau | train-00000018 | balance | "Naira nawa gare ni … na bankin Gt?" / target: "CURRENCY: Naira $$ BANK_NAME: Gt" | Nigerian Naira currency annotated in Hausa — confirms per-language currency grounding | IC |
| D20 | sot | train-00000016 | balance | "Ho setse bokae ka akhaontong ya Nedbank" / target: "BANK_NAME: Nedbank" | Sesotho uses South African bank Nedbank — culturally grounded for South Africa | IC |
| D21 | sot | train-00000003 | balance | "Ho setse bokae bankeng ya FNB" / target: "BANK_NAME: FNB" | FNB (First National Bank, SA) in Sesotho — same grounding documented for Xhosa in INJONGO paper | IC |
| D22 | xho | train-00000018 | balance | "Ndinganayo imali engange R700 kwiakhawunti yam yaseStandard Bank?" / target: "MONEY: R700 $$ BANK_NAME: yaseStandard Bank" | South African Rand (R700) and Standard Bank in Xhosa | IC |
| D23 | amh | train-00000045 | alarm | "ነገ ጠዋት 12 ሰአት…" (no span annotation) | "12 ሰአት" (12 o'clock) unnanotated — "ጠዋት" (morning) absent from target; Ethiopian time convention unclear | OC, OO |
| D24 | orm | train-00000012 | car_rental | "Torban jalqabaa ji'a kanaf Toyotaa kireeffame Naqamtee keessa nan argadhaa" / target: "DATE: ji'a kana $$ CITY_OR_PROVINCE: Naqamtee" | Oromo city Naqamtee (Nekemte) used in CITY_OR_PROVINCE slot | IC |
| D25 | amh | train-00000041 | book_flight | intent=book_flight, COUNTRY: ቱርክ (Turkey) | Flight to Turkey — no intercity bus, seat class, or operator-specific slots present | IO |
| D26 | amh | train-00000047 | book_flight | intent=book_flight, COUNTRY: ሱዳን (Sudan) | Flight to Sudan — air travel framing, not surface transport | IO |
| D27 | eng | train-00000053 | travel_suggestion | "help me decide between Hawassa and Arbaminch for my upcoming trip. What are the unique attractions in each location?" | English translation of Amharic utterance confirms Ethiopian city coverage in the dataset | IC |
| D28 | amh | train-00000053 (calendar_update) | calendar_update | "በዚህ ሳምንት ምንም ቀጠሮ እንዲኖረኝ አልፈልግም።" / target: "DATE: በዚህ ሳምንት" | Relative week reference, no Ethiopian calendar month | OO |
| D29 | orm | train-00000045 | alarm | "Galgala kana caalaan akka dhufuuf dammaksituu guutiif saatii 7tti" / target includes misannotated "PERSONAL_NAME: caalaa" | "caalaa" annotated as PERSONAL_NAME but may be part of "Galgala caalaan" (this evening) phrase | OC |
| D30 | amh | train-00000041 | book_flight | no intercity corridors, no seat class, no bus operator, no fare tier present | All Amharic travel utterances use air travel framing | IO |
| D31 | hau | train-00000031 | confirm_reservation | "Za ku iya tabbatar min ina da ajiyar tebur a taco bell da ƙarfe 7 na yamma" / target: "RESTAURANT_NAME: taco bell" | "Taco Bell" — US fast-food chain, Western entity in Hausa utterance | IC |
| D32 | ibo | train-00000012 | food_last | "How many hours does it take cooked Indomie noodles to spoil?" | "Indomie noodles" — popular West African brand, regionally grounded | IC |
| D33 | amh | train-00000035 | calendar_update | "የእናቴን እና የአባቴን የልደት ቀን የቀን መቁጠሪያዬ ላይ ስላቀያየርኩት አስተካክለው" | "I changed my parents' birthdays in my calendar, please fix it." — no slots annotated despite calendar events | OC |
| D34 | eng (raw=amh) | train-00000045 | balance | raw: "እባካችሁ የዳሽን ባንክ ሂሳቤን ታረጋግጡልኛላችሁ?" / text: "can you please check my dasion bank account" | "Dashen Bank" (major Ethiopian bank) — Amharic source is culturally grounded but English transliteration is lossy ("dasion") | IC, OF |
| D35 | swa | train-00000011 | car_rental | "Kukodisha gari la kutembeza watalii pale Maasai Mara tarehe saba hadi tarehe kumi" / target includes "PLACE_NAME: Maasai Mara" | Swahili uses Maasai Mara (Kenya) — East African cultural grounding | IC |
| D36 | lug | train-00000047 | book_flight | "Weekwate ekifo ku nnyonyi eva e Algiers okudda e London" / target: "CITY_OR_PROVINCE: Algiers $$ CITY_OR_PROVINCE: London" | Luganda flight utterance routes through Algiers to London — non-African destination present | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Ethiopian calendar month names present as valid DATE slot values in Amharic utterances
- **Dimension(s):** IC, OO
- **Observation:** The single most important flagged gap in the benchmark YAML — whether Ethiopian (Ge'ez) calendar month names are present in Amharic DATE slot annotations — is directly addressed in the sampled data. Example 19 of the Amharic split contains the utterance "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ።" with slot annotation "DATE: መስከረም አምስት" (Meskerem fifth). This is a travel-domain instance using an Ethiopian calendar month name (Meskerem = September–October) as the date slot value. Additionally, Amharic example 11 (car_rental) annotates "DATE: ከሃምሌ 4 እስከ 6", where Hamle (11th Ethiopian month) is used as a date reference.
- **Deployment relevance:** This directly resolves the highest-priority flagged gap. Users of an Ethiopian intercity booking app will natively reference Ethiopian calendar months for travel dates; the benchmark does capture this convention in at least some Amharic travel-domain instances, making evaluation of date-slot extraction for Ethiopian calendar dates partially feasible.
- **Datapoint citations:**
  - [D1] Example train-00000042 (amh, split=train, label=book_flight): "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ།" — Ethiopian calendar month Meskerem as DATE slot value in a flight booking utterance
  - [D2] Example train-00000042 (amh, split=train, label=book_flight): target: "DATE: መስከረም አምስት" — DATE annotation confirms Ge'ez calendar month is treated as a valid DATE slot value
  - [D6] Example train-00000011 (amh, split=train, label=car_rental): "ከሃምሌ 4 እስከ 6 የቤት መኪና ኪራይ ማግኘት እችላለሁ?" / target: "DATE: ከሃምሌ 4 እስከ 6" — Hamle (Ethiopian month) appears in a travel-adjacent domain

#### Strength 2: Ethiopian intercity city toponyms present as CITY_OR_PROVINCE slot values in Amharic travel utterances
- **Dimension(s):** IC, OO
- **Observation:** The second highest-priority flagged gap — whether Ethiopian intercity city names appear in travel-domain slot instances — is partially resolved by direct data inspection. Example 19 (train-00000042) contains both Dire Dawa (ድሬዳዋ) and Bahir Dar (ባህርዳር) as CITY_OR_PROVINCE slots in a book_flight intent. The English config (raw=amh) example train-00000053 shows Hawassa (ሃዋሳ) and Arba Minch (አርባ ምንጭ) as CITY_OR_PROVINCE slots in a travel_suggestion utterance. These cities are on key Ethiopian intercity corridors.
- **Deployment relevance:** Ethiopian city toponyms that match actual Sky Bus / Selam Bus corridors (Dire Dawa, Bahir Dar, Hawassa, Arba Minch) appear in the training data. This mitigates — though does not fully resolve — the toponym coverage gap, since the sample confirms at least some corridor-relevant cities are present.
- **Datapoint citations:**
  - [D2] Example train-00000042 (amh, split=train, label=book_flight): target: "CITY_OR_PROVINCE: ድሬዳዋ $$ CITY_OR_PROVINCE: ባህርዳር" — Dire Dawa and Bahir Dar, both major intercity bus hubs
  - [D9] Example train-00000053 (eng config, raw=amh, split=train, label=travel_suggestion): text: "help me decide between Hawassa and Arbaminch for my upcoming trip" — Hawassa and Arba Minch in CITY_OR_PROVINCE slots

#### Strength 3: Ethiopian financial ecosystem entities culturally grounded in Amharic utterances
- **Dimension(s):** IC
- **Observation:** Multiple Amharic banking-domain examples use distinctly Ethiopian entities: Amhara Bank (አማራ ባንክ), Commercial Bank of Ethiopia (ንግድ ባንክ), and TeleBirr (ቴሌብር, Ethiopia's dominant mobile payment platform). The TeleBirr reference appears in both native Amharic (example 16) and the English config raw Amharic utterance (train-00000092). These are not pan-African or Western placeholders — they are Ethiopia-specific financial institutions directly relevant to the deployment context.
- **Deployment relevance:** For a booking system that handles fare payment, the presence of TeleBirr (the leading Ethiopian mobile money platform, operated by Ethio Telecom) as an annotated PAYMENT_COMPANY entity is directly useful for payment-related slot extraction.
- **Datapoint citations:**
  - [D3] Example train-00000016 (amh, split=train, label=balance): "የአማራ ባንክ አካውንቴ ስንት አለው" — Amhara Bank, an Ethiopian-specific institution
  - [D4] Example train-00000018 (amh, split=train, label=balance): "ንግድ ባንክ ላይ የቀረኝ ገንዘብ አለ" — Commercial Bank of Ethiopia (ንግድ ባንክ)
  - [D5] Example train-00000003 (amh, split=train, label=balance): "በቴሌብር የብድር አካውንቴ ላይ…" — TeleBirr mobile payment platform

#### Strength 4: Culturally grounded entity substitution confirmed across multiple language tracks, not just one
- **Dimension(s):** IC
- **Observation:** The benchmark YAML cited the Xhosa/South African entity substitution as the key example of cultural grounding. The data confirms this extends across language tracks: Hausa (Naira currency, GT Bank), Sesotho (Nedbank, FNB — South African banks), Xhosa (R700 Rand, Standard Bank), Swahili (Maasai Mara, Tigo-Pesa), Oromo (Ethiopian cities, Ethiopian Airlines, Oromo calendar months). Each language uses locally relevant financial institutions, currencies, and toponyms.
- **Deployment relevance:** The consistent pattern across all sampled language tracks strengthens confidence that the Amharic track has similarly received culturally grounded Ethiopian entities (which is confirmed by D1–D5 above), rather than generic or Western placeholders inherited from CLINC.
- **Datapoint citations:**
  - [D19] Example train-00000018 (hau, split=train, label=balance): "Naira nawa gare ni … na bankin Gt?" — Naira currency, GT Bank (Nigeria)
  - [D21] Example train-00000003 (sot, split=train, label=balance): "Ho setse bokae bankeng ya FNB" — FNB South Africa
  - [D22] Example train-00000018 (xho, split=train, label=balance): "imali engange R700 kwiakhawunti yam yaseStandard Bank?" — Rand and Standard Bank
  - [D35] Example train-00000011 (swa, split=train, label=car_rental): "Kukodisha gari la kutembeza watalii pale Maasai Mara" — Kenyan landmark

#### Strength 5: Oromo calendar month names present as DATE slot values, confirming methodology extends to the L2 population's language
- **Dimension(s):** IC, OO
- **Observation:** In the Oromo (orm) config, example train-00000011 uses "Ebila 12 hanga Ebila 14" (April in the Oromo calendar) as a DATE slot value, and example train-00000035 uses "sadaasa 21" (November in the Oromo calendar). Since INJONGO's deployment context includes L2 Amharic speakers from Oromia who may code-switch, the presence of Oromo-language calendar conventions confirms the benchmark methodology generates language-authentic temporal expressions.
- **Deployment relevance:** Though code-switched Amharic–Oromo utterances are absent (a separate concern), the Oromo track's culturally grounded date expressions confirm the overall methodology is consistent and that a system trained on INJONGO for Oromo separately would handle Ethiopian Oromo calendar references.
- **Datapoint citations:**
  - [D13] Example train-00000011 (orm, split=train, label=car_rental): "Ebila 12 hanga Ebila 14tti Mattuu keessatti kireeffannaa konkolaataa argachuun ni danda'amaa" — Ebila (April, Oromo calendar) as DATE
  - [D14] Example train-00000035 (orm, split=train, label=calendar_update): "Sagantaa sirna cidhaaf sadaasa 21tti qabame" — Sadaasa (November, Oromo) as DATE

#### Strength 6: Ethiopian airline and domestic route vocabulary present in Oromo flight utterances
- **Dimension(s):** IC
- **Observation:** Oromo example train-00000041 contains "Xiyyaara Itoopiyaa" (Ethiopian Airlines) and references Dire Dawa (Dirree dawaa), Bole Airport, and Jimma — all key Ethiopian intercity aviation/travel nodes. While this utterance has empty span annotations (a concern noted separately), the vocabulary itself confirms that Ethiopian Airlines and domestic route city names are present in the dataset.
- **Deployment relevance:** For an Ethiopian booking system, familiarity with Ethiopian Airlines and domestic city-pair references is relevant. The presence of these entities in the Oromo track strengthens the inference that similar entities exist in the Amharic track.
- **Datapoint citations:**
  - [D12] Example train-00000041 (orm, split=train, label=book_flight): "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" — Ethiopian Airlines, Dire Dawa, Bole, Jimma all present

#### Strength 7: Ge'ez script used throughout Amharic track with no script anomalies
- **Dimension(s):** IF
- **Observation:** All 19 sampled Amharic examples use correct Ge'ez (Ethiopic) script throughout, including proper representation of Amharic-specific characters and ligatures. No romanized Amharic or mixed-script anomalies were observed in the amh config.
- **Deployment relevance:** The deployment is a text-based smartphone app using Ge'ez input. Full script match eliminates the IF concern entirely for the Amharic track.
- **Datapoint citations:**
  - [D1] Example train-00000042 (amh): "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ།" — all text in Ge'ez script
  - [D5] Example train-00000003 (amh): "በቴሌብር የብድር አካውንቴ ላይ አሁን ያለብኝ ቀሪ ሂሳብ ምን ያህል ነው።" — Ge'ez script throughout

#### Strength 8: Ethiopian personal names and restaurant names used in Amharic examples
- **Dimension(s):** IC
- **Observation:** Amharic example train-00000031 (confirm_reservation) contains the restaurant name "ቶቶት" (Totot, a known Addis Ababa restaurant) and the personal name "ቃለአብ" (Kaleab, a distinctly Ethiopian/Tigrinya-Amharic name). This confirms that the annotators used locally recognizable named entities rather than translating Western names.
- **Deployment relevance:** For a booking system where restaurant and personal name extraction is tested, culturally grounded Amharic personal names and locally known venue names increase ecological validity for the Ethiopian user population.
- **Datapoint citations:**
  - [D17] Example train-00000031 (amh, split=train, label=confirm_reservation): "RESTAURANT_NAME: ቶቶት $$ PERSONAL_NAME: ቃለአብ" — Ethiopian restaurant and personal name

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Travel domain uses air travel framing exclusively — no surface transport, bus booking, seat class, or operator-specific intents
- **Dimension(s):** IO
- **Observation:** Every sampled Amharic travel-domain utterance (book_flight, car_rental, travel_suggestion) uses air travel or general rental car framing. The two book_flight examples explicitly reference flights to Turkey and Sudan (international air travel). There are no utterances involving intercity bus booking, seat-class selection (VIP vs. economy), operator-specific flows (Sky Bus, Selam Bus, Ride), road-closure rebooking, or fare-tier queries. The intent taxonomy does not include any of these categories.
- **Deployment relevance:** The deployment system is specifically for Sky Bus, Selam Bus, and Ride — intercity bus and ride-hail operators. The benchmark's travel domain is built around generic air travel and car rental intents from CLINC. This is a fundamental domain-level mismatch between what the benchmark tests and what the deployment system handles. A model that achieves high accuracy on INJONGO's travel intents (book_flight, car_rental) may not generalize to intercity bus booking intents that are absent from the taxonomy entirely.
- **Datapoint citations:**
  - [D7] Example train-00000041 (amh, split=train, label=book_flight): "ወደ ቱርክ በፍጥነት የምደርስበት የበረራ አማራጭ ንገረኝ།" — international flight, no surface transport
  - [D8] Example train-00000047 (amh, split=train, label=book_flight): "ወደ ሱዳን የበረራ ትኬት ያስፈልገኛል።" — international air ticket, no bus booking
  - [D25, D26] — Both Amharic book_flight examples are international air travel

#### MAJOR

#### MAJOR Concern 1: Amharic DATE slots predominantly use relative temporal expressions, not Ethiopian calendar month names — calendar coverage is sparse in sample
- **Dimension(s):** IC, OO
- **Observation:** While Strength 1 identified that Ethiopian calendar month names *do* appear in the data (Meskerem in train-00000042, Hamle in train-00000011), the majority of Amharic DATE slot annotations in the sample use relative expressions: "የዚህ ወር" (this month), "ከሚመጣው ወር ጀምሮ ለ3 ወር" (starting next month for 3 months), "ነገ" (tomorrow), "ዛሬ" (today), "በዚህ ሳምንት" (this week). Only 2 of 9 Amharic DATE-annotated examples in the sample use named Ethiopian calendar months. The annotation guide examples explicitly use Gregorian conventions (as documented in Q153, Q154).
- **Deployment relevance:** Users of an Ethiopian booking system will frequently reference specific Ethiopian calendar dates for travel (e.g., "ለጥምቅት ሰኞ" — for Timkat Monday). The benchmark's DATE slot evaluation may not adequately stress-test a model's ability to extract named Ethiopian calendar months vs. relative expressions, and if most training instances use relative expressions, a fine-tuned model may not learn robust calendar-month extraction.
- **Datapoint citations:**
  - [D15] Example train-00000052 (amh): "DATE: የዚህ ወር" — relative expression "this month," no named month
  - [D16] Example train-00000023 (amh): "DATE: ከሚመጣው ወር ጀምሮ ለ3 ወር" — relative expression, no named calendar month
  - [D28] Example train-00000053 (amh, calendar_update): "DATE: በዚህ ሳምንት" — "this week," relative
  - [D2] Example train-00000042 (amh): "DATE: መስከረም አምስት" — Ethiopian month Meskerem present (counterevidence — one instance confirmed)

#### MAJOR Concern 2: Missing slot annotations in Amharic examples — potential annotation gaps
- **Dimension(s):** OC
- **Observation:** Amharic example 3 (alarm, train-00000045) contains "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ" (the alarm I set for tomorrow morning at 12 o'clock) but has completely empty spans and empty target. The utterance contains at minimum a DATE slot ("ነገ" = tomorrow) and TIME slot ("12 ሰአት ጠዋት" = 12 o'clock in the morning). Similarly, example 7 (calendar_update, train-00000035) "የእናቴን እና የአባቴን የልደት ቀን የቀን መቁጠሪያዬ ላይ ስላቀያየርኩት አስተካክለው" has empty spans despite containing a calendar event reference. The Oromo book_flight example (train-00000041) is similarly unnanotated despite containing multiple city names and Ethiopian Airlines.
- **Deployment relevance:** Slot-filling F1 evaluation depends on accurate ground truth. Missing annotations inflate false-negative counts during model evaluation, artificially depressing F1 scores and potentially misdirecting model fine-tuning. For a deployment system where slot extraction accuracy is the primary requirement, under-annotated training instances reduce the quality of the evaluation benchmark.
- **Datapoint citations:**
  - [D11] Example train-00000045 (amh, split=train, label=alarm): "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ…" spans=[] — DATE "ነገ" and TIME "12 ሰአት" absent from annotation
  - [D33] Example train-00000035 (amh, split=train, label=calendar_update): "የእናቴን እና የአባቴን የልደት ቀን…" spans=[] — birthday calendar event unannotated
  - [D12] Example train-00000041 (orm, split=train, label=book_flight): "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" spans=[] — three city names and airline unannotated

#### MAJOR Concern 3: Ethiopian time convention (6-hour offset) not represented or validated in TIME slot annotations
- **Dimension(s):** IC, OO
- **Observation:** Ethiopian clock convention offsets standard time by 6 hours (1:00 Ethiopian = 7:00 AM internationally). Amharic example 5 (alarm, train-00000053) annotates "TIME: ሰባት ከአስራአምስት" (7:15 in Ethiopian time = 1:15 AM internationally, or more likely 7:15 AM). Example 3 references "12 ሰአት" (12 o'clock in Ethiopian time = 6:00 AM or PM). No TIME annotation in the sample includes disambiguation of Ethiopian vs. international clock convention, and the annotation guide is silent on this (per YAML documentation).
- **Deployment relevance:** For a booking system where users ask about bus departure times, Ethiopian clock convention is actively used (e.g., "ሰባት ሰዓት ለምን ምንም አይሄደም?" could mean "Why is there no bus at 1 AM?" or "at 7 AM?" depending on convention). Ambiguous TIME slot values are a direct failure mode for bus departure slot extraction.
- **Datapoint citations:**
  - [D23] Example train-00000045 (amh, split=train, label=alarm): "ነገ ጠዋት 12 ሰአት…" (12 o'clock, morning) — annotated as empty, but "12 ሰአት" in Ethiopian time = 6 AM international; no convention documented
  - [D6] Example train-00000011 (amh, split=train): "TIME" slot not present; date range uses Hamle — no TIME slot with Ethiopian clock reference in sample

#### MAJOR Concern 4: No code-switched Amharic utterances present; Amharic track is monolingual throughout
- **Dimension(s):** IC, OC
- **Observation:** All 19 sampled Amharic utterances are monolingual Ge'ez script Amharic. None contains Oromo lexical items (Latin script), Tigrinya words, or English loanwords for booking terms such as "ticket," "seat," or "cancel." The eng config's raw Amharic utterances (e.g., train-00000045, train-00000053) also show pure Amharic without code-switching. This is consistent with the INJONGO paper's silence on intra-utterance code-switching.
- **Deployment relevance:** The target population includes L2 Amharic speakers from Oromia and Tigray who produce code-switched utterances. A model evaluated purely on monolingual Amharic will not be assessed for its robustness to code-switched inputs, which are expected to be frequent in actual booking interactions. This is the OC annotator–user mismatch concern identified as HIGH priority in the elicitation.
- **Datapoint citations:**
  - [D1] through [D18] — All Amharic examples are monolingual; no Oromo terms (e.g., Jimma, Adama in Oromo pronunciation), no Tigrinya lexical items, no mixed-script tokens observed in any of the 19 sampled Amharic training examples

#### MAJOR Concern 5: Birr currency not observed in any Amharic travel or utility domain example
- **Dimension(s):** IC, OO
- **Observation:** Despite CURRENCY and MONEY slots being present in the ontology and TeleBirr appearing as a PAYMENT_COMPANY (D5), no sampled Amharic example contains a CURRENCY or MONEY slot value denominated in Ethiopian Birr (ብር or ETB). The currency evidence comes entirely from other languages: Hausa uses Naira (D19), Xhosa uses Rand (D22), Wolof uses Dollar (wol train-00000047). In the Amharic sample, no fare amount or Birr symbol appears as a slot value.
- **Deployment relevance:** The deployment system needs to extract Birr-denominated fares (e.g., "ለVIP መቀሌ ድረስ ስንት ብር ነው?" = "How many Birr to Mekelle VIP?"). If the Amharic training data has few or no Birr-denominated MONEY/CURRENCY slot examples in the travel domain, fine-tuned models may not reliably extract fare values.
- **Datapoint citations:**
  - [D5] Example train-00000003 (amh): TeleBirr appears as PAYMENT_COMPANY, not as a CURRENCY/MONEY value — no Birr amount in slots
  - [D3, D4] — Banking domain Amharic examples reference balance queries without extracting currency amounts
  - [D19] Example train-00000018 (hau): "CURRENCY: Naira" — contrast: Hausa does have currency in slot, Amharic sample does not

#### MINOR

#### MINOR Concern 1: Some Western entity leakage in non-Amharic tracks
- **Dimension(s):** IC
- **Observation:** Hausa example train-00000031 (confirm_reservation) contains "RESTAURANT_NAME: taco bell" — a US fast-food chain that is unlikely to be familiar to Nigerian Hausa speakers in the natural booking context. Luganda train-00000047 (book_flight) routes Algiers to London. Yoruba train-00000036 references "$500" and "Amẹ́ríkà" (America). These are isolated cases and not the dominant pattern, but they confirm that Western entity leakage documented for MASSIVE is not entirely absent from INJONGO.
- **Deployment relevance:** For the Ethiopian Amharic deployment specifically, no Western entity leakage was observed in the Amharic sample. The concern is minor for this specific deployment but may indicate that the cultural grounding methodology was applied unevenly across languages.
- **Datapoint citations:**
  - [D31] Example train-00000031 (hau, split=train, label=confirm_reservation): "Za ku iya tabbatar min ina da ajiyar tebur a taco bell" — Taco Bell, US restaurant chain
  - [D36] Example train-00000047 (lug, split=train, label=book_flight): "eva e Algiers okudda e London" — Algiers to London routing

#### MINOR Concern 2: Potential annotation inconsistency — "12 ሰአት" (a time value) goes unannotated in one Amharic alarm example
- **Dimension(s):** OC
- **Observation:** Amharic example 3 (train-00000045, alarm) contains the text "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ" with completely empty spans. Comparable Amharic alarm examples (train-00000053) annotate "TIME: ሰባት ከአስራአምስት" and "DATE: ነገ" for structurally similar utterances. This suggests inconsistent annotation treatment of the same temporal elements across utterances — one annotated, one not.
- **Deployment relevance:** Inconsistent TIME annotation reduces the reliability of TIME slot F1 as a measure of model quality for the deployment's bus-departure-time extraction use case.
- **Datapoint citations:**
  - [D11] Example train-00000045 (amh): "ነገ ጠዋት 12 ሰአት…" spans=[] — empty despite temporal content
  - [D2] Example train-00000053 (amh): "DATE: ነገ $$ TIME: ሰባት ከአስራአምስት" — similar alarm utterance with full temporal annotation

#### MINOR Concern 3: Lossy English transliteration of Ethiopian entities in eng config may reduce cross-lingual transfer reliability
- **Dimension(s):** OF
- **Observation:** The eng config (which serves as the cross-lingual transfer source) contains English translations of Amharic utterances with some transliteration loss: train-00000045 transliterates "ዳሽን ባንክ" (Dashen Bank — a major Ethiopian bank) as "dasion bank" in the English text. The slot annotation uses "dasion bank" as BANK_NAME. If cross-lingual transfer experiments use this English data as source, "dasion bank" is not a recognizable English entity and would not benefit from English pre-training on bank name recognition.
- **Deployment relevance:** Cross-lingual transfer from African-centric English (INJONGO English) to Amharic is one of the benchmark's documented evaluation settings. Transliteration errors in the English source reduce the quality of this transfer evaluation for Ethiopian-specific entities.
- **Datapoint citations:**
  - [D34] Example train-00000045 (eng config, raw=amh, split=train, label=balance): raw: "እባካችሁ የዳሽን ባንክ ሂሳቤን ታረጋግጡልኛላችሁ?" / text: "can you please check my dasion bank account" — "ዳሽን" → "dasion" (should be "Dashen")

---

### Content Coverage Summary

The Amharic track of INJONGO contains culturally grounded utterances generated by native speakers using distinctly Ethiopian entities: Ethiopian banks (Amhara Bank, Commercial Bank of Ethiopia), the TeleBirr mobile payment platform, Ethiopian restaurant names (Totot), Ethiopian personal names (Kaleab), and crucially — Ethiopian calendar month names in travel-domain DATE slots (Meskerem, Hamle). Two of the three key Ethiopian intercity travel cities examined (Dire Dawa, Bahir Dar, Hawassa, Arba Minch) are confirmed present as CITY_OR_PROVINCE slot values across the amh and eng configs.

The benchmark covers 17 language tracks including Amharic, Oromo, and Tigrinya as separate tracks, all using culturally grounded elicitation. The Oromo track additionally shows Oromo calendar month names (Ebila, Sadaasa, Guraandhala) and Oromo-specific cities (Mattuu/Metu, Naqamtee/Nekemte) as annotated slot values.

However, the travel domain in Amharic is exclusively framed as air travel and car rental (book_flight, car_rental, travel_suggestion, car_rental intents) with no surface transport, intercity bus, seat-class, or operator-specific content. Ethiopian Birr as a MONEY/CURRENCY slot value was absent from all sampled Amharic examples. Ethiopian clock convention (6-hour offset) is unaddressed. All Amharic utterances are monolingual with no code-switching. Annotation gaps (empty spans for utterances with clear temporal content) were observed in 2–3 of 19 Amharic examples.

Across all 17 language tracks, the data consistently shows culturally grounded named entities (local banks, currencies, cities, personal names) with Gregorian and local calendar date references mixed throughout. The `eng` config contains English translations with raw original-language utterances, serving cross-lingual transfer evaluation.

---

### Limitations

1. **Sample size per config:** 11–27 examples per language track from the training split only. With 80 utterances per intent × 40 intents = 3,200 total per language, the sampled 19 Amharic examples represent ~0.6% of the Amharic training set. Ethiopian calendar month coverage may be higher overall than the 2/9 rate observed in DATE annotations here.

2. **Travel domain coverage unquantifiable from sample:** Only 4 Amharic examples fall in the travel domain (book_flight ×3, car_rental ×1 in the sample). The full set has 80 utterances per intent × 8 travel intents = 640 travel-domain Amharic instances. Toponym and Birr currency coverage in the full travel-domain split requires direct dataset inspection beyond this sample.

3. **Validation and test splits not sampled:** The analysis is based on training split only. Test split annotation quality (which is what benchmark evaluation scores reflect) has not been independently verified here.

4. **Code-switching absence confirmed but not quantified:** The absence of code-switched utterances in the 19 Amharic examples is consistent with documentation, but a larger sample (or full dataset inspection) would be needed to confirm this is a systematic absence rather than a sampling artifact.

5. **Amharic-specific per-language F1 scores not available in this dataset:** The HuggingFace dataset contains utterances and labels but not model evaluation scores. Per-language Amharic benchmark performance requires reading Table 5 of the INJONGO ACL 2025 paper directly.

6. **Ethiopian time convention cannot be audited from text alone:** Without ground truth on what clock convention annotators assumed, it is not possible to determine from utterance text whether TIME slot values use Ethiopian or international clock conventions.

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
  "benchmark": "INJONGO",
  "region": "Ethiopian Intercity/Ride-Hail Commuter Cohort (Amharic-Primary)",
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
