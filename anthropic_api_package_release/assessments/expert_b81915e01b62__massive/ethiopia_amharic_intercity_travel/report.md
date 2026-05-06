## Deployment Context

**Use case:** Amharic intercity-travel booking bots for Sky Bus, Selam Bus, and Ride covering routes, fares, and seat changes
**Target population:** Inter-regional commuters and travelers booking long-distance buses and ride-hail trips via smartphone apps

# Validity Analysis: massive
**Target context:** Ethiopian Intercity Travelers — Amharic-Language Booking Bot
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology | 2 | Significant gaps | medium |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 4 | Minor gaps | medium |
| Output Ontology | 2 | Significant gaps | medium |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ✓ | 4 | Minor gaps | high |
| **Average** | **2.3** | | |

> ⚠ = highest concern &nbsp; ✓ = strongest dimension

### Dimension Key

| Abbr. | Dimension | Definition |
|:-----:|-----------|------------|
| IO | Input Ontology | Whether the benchmark's test case categories cover the query types expected in deployment. |
| IC | Input Content | Whether individual datapoint content is culturally and contextually appropriate for the target region. |
| IF | Input Form | Whether the input signal encoding (text, audio, image parameters) matches deployment conditions. |
| OO | Output Ontology | Whether the benchmark's output categories and scoring criteria reflect regionally valid decision boundaries. |
| OC | Output Content | Whether ground-truth labels align with the judgments of regional stakeholders. |
| OF | Output Form | Whether the expected output modality matches regional deployment needs and accessibility. |

## Overall Summary

MASSIVE provides a strong modality and output-format match for an Amharic intent-classification + slot-filling booking bot, but exhibits severe content-level gaps for the Ethiopian intercity-travel deployment. The translation-from-English pipeline [Q2, Q4, Q106] guarantees that Amharic data lacks Ethiopian calendar dates, local city name variants, Birr fare conventions, and code-switching with Oromo or Tigrinya — all of which the user has confirmed appear in real user utterances. Operator-specific intents and slot types (operator_name, seat_class, route_closure_reason, surcharge_event, departure_terminal) are absent from the 60-intent / 55-slot taxonomy, which the paper itself describes as 'relatively simple' [Q108]. Annotator demographics for Amharic are undisclosed, raising convergent-validity concerns about whether labels reflect Ethiopian intercity-traveler judgments. Per-language data is small (~19.5k records, [Q103]) and Amharic — a unique-script, lower-resource language — is expected to fall in the lower performance tier per the script/pretraining-data correlation [Q87, Q98, Q100]. Strengths: text-only modality match, Ethiopic-script inclusion, output format directly compatible, and rich per-language breakdowns enabling expected-performance estimation.

## Practical Guidance

### What This Benchmark Measures

MASSIVE provides a baseline for Amharic intent-classification and slot-filling on translated-from-English virtual-assistant utterances [Q2, Q5, Q73]. For the deployment, it can establish a lower-bound expectation for how XLM-R or mT5-class models handle generic booking-style intents in Amharic and provide per-language performance figures [Q126, Q127, Q128] useful for capacity planning. Output Form (score 4) and Input Form (score 4) are the strongest dimensions and indicate that the evaluation paradigm itself transfers cleanly.

### Construct Depth

Construct depth is shallow for the deployment. MASSIVE measures translation-quality intent/slot accuracy on a generic taxonomy, not naturalistic Ethiopian intercity-booking utterances. Input Content (score 1) and Output Content (score 1) gaps mean the benchmark cannot probe Ethiopian-calendar slot extraction, Birr fare normalization, city-name-variant handling, code-switching, or L2-speaker phrasing — the phenomena most likely to drive real-world failure. Input Ontology (score 2) and Output Ontology (score 2) gaps mean operator-specific intents and slot types are entirely outside the evaluation surface.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** medium

**Justification:**
MASSIVE's taxonomy of 18 domains, 60 intents, and 55 slots [Q1] was designed around major virtual assistants [Q16] and the 'general multi-domain NLU task' [Q12]. The corpus consists primarily of interrogatives and imperatives [Q30], which broadly aligns with booking-bot utterances. However, the taxonomy contains no intercity-transport-specific intents (route_query, operator_query, seat_class_query, cancel_and_rebook for road closures, holiday_surcharge_query, departure_terminal_query) that are explicitly required for the deployment, and the paper acknowledges its labeling schema is 'relatively simple when compared with hierarchical labeling schemata or flat schemata with more intent and slot options' [Q108]. The user views booking flows as broadly generic (Q1 elicitation), reducing concern, but at least six intent types relevant to the deployment are absent, and a confirmed full gap exists across African NLP for transport-domain NLU intents (search_target gap_id 6).

**Strengths:**
- Question and command coverage matches booking-bot interaction patterns — corpus 'primarily consists of interrogatives (i.e., questions) and imperatives (commands or requests)' [Q30]
- Includes Amharic as one of 51 languages, with WALS-derived typological metadata that lets evaluators stratify performance by SOV order, verb morphology, etc. [Q34, Q37]

**Checklist:**

- **IO-1**: Required deployment categories include route_query, operator_query, seat_class_query, cancel_and_rebook, holiday_surcharge_query, departure_terminal_query (regional context, booking_flow_intents.absent_intents). Generic booking intents (book, reschedule, check availability) are partially covered. — _Sources: Q1, Q30_
- **IO-2**: MASSIVE's 60-intent taxonomy was selected to 'benchmark today's [virtual assistant] systems' [Q16] and omits intercity-transport-specific intents listed above. Confirmed by gap_id 6 search [WEB-21, WEB-22] showing no African transport NLU benchmark exists. — _Sources: Q1, Q16, WEB-21, WEB-22_
- **IO-3**: MASSIVE includes domains (smart-home, music, IoT-style commands implied by SLURP heritage [Q12, Q13]) that are irrelevant to a transport booking deployment, contributing construct-irrelevant variance to overall accuracy metrics. INSUFFICIENT DOCUMENTATION on per-domain relevance scoring; would need a domain-by-domain mapping to deployment scope. — _Sources: Q12_
- **IO-4**: Significant content-validity gaps: Ethiopian-calendar holiday surcharge intents, route-closure rebooking, operator/seat-class queries, and terminal-station queries are absent [Q108; gap_id 6]. The booking flow's transactional core (book/cancel/reschedule) is partially captured but operator-specific scenarios are not. — _Sources: Q108, WEB-21_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'MASSIVE contains 1M realistic, parallel, labeled virtual assistant utterances spanning 51 languages, 18 domains, 60 intents, and 55 slots.' (p.1)
- [Q12] 'This work focuses on the general multi-domain NLU task and builds off the SLURP (Bastianelli et al., 2020) benchmark dataset to extend to an unprecedented 50 new languages.' (p.2)
- [Q16] 'Second, we determined existing languages available in major virtual assistants, such that the dataset could be used to benchmark today's systems.' (p.3)
- [Q30] 'Specifically, the corpus primarily consists of interrogatives (i.e., questions) and imperatives (commands or requests).' (p.4)
- [Q108] 'Fourth, our labeling schema is relatively simple when compared with hierarchical labeling schemata or flat schemata with more intent and slot options.' (p.9)

*Web sources:*
- [WEB-21] EthioBenchmark covers NER, POS, news classification, hate speech, sentiment, MT — no intent classification or slot filling, confirming gap in African NLP for transport NLU
- [WEB-22] EthioLLM/EthioBenchmark arXiv — no booking-domain NLU resource

</details>

**Information gaps:**
- Per-domain mapping showing what fraction of MASSIVE's 18 domains/60 intents are relevant to intercity bus booking
- Complete operator-specific intent list from Sky Bus, Selam Bus, and Ride

**Requires expert verification:**
- Whether booking-flow elicitation in Ethiopia would surface additional intent types beyond the listed gaps
- Whether holiday-surcharge or road-closure intents are framed by users as separate intents or as parameter values within general booking intents

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
MASSIVE's Amharic content was created by 'tasking professional translators to localize the English-only SLURP dataset' [Q2, Q4], with seed data 'originally created through crowd-sourcing, not from a real virtual assistant, which introduces artificialities' [Q106]. This means Amharic instances will not contain Ethiopian calendar dates (Meskerem, Tikimt — 13-month Ge'ez calendar offset 7–8 years from Gregorian, [WEB-4]), local city name variants (Adama/Nazret, Mekelle/Mek'ele), Birr-denominated fares, or holiday-surcharge contexts (Timkat, Meskel, Enkutatash — [WEB-5, WEB-6]) — all of which the user has confirmed are required slot values (Q2 elicitation). Worker-decided localization 'added further noise' [Q107], and per-language data is 'relatively small at 19.5k total records and 11.5k records for training' [Q103]. The IC dimension was rated HIGH priority and the mismatch is severe.

**Strengths:**
- Translation workflow allows slot localization — workers could localize values like song names [Q57, Q58], so some Amharic content adaptation occurred
- Metadata stores the translate/localize/unchanged decision per slot [Q58], enabling researchers to filter for genuinely localized content

**Checklist:**

- **IC-1**: Yes — the deployment requires Ethiopian calendar dates (Meskerem, Tikimt — [WEB-4]), local city names with Amharic spellings and alternate variants, Birr fare conventions, and operator/route knowledge specific to Sky Bus, Selam Bus, Ride. None of these are present in MASSIVE's English-derived content [Q2, Q4, Q106]. — _Sources: Q2, Q4, Q106, WEB-4, WEB-5, WEB-6_
- **IC-2**: MASSIVE's content originates from English crowd-workers [Q106] and was translated into Amharic [Q2]; cultural alignment with Ethiopian intercity travelers is incidental. Holiday concepts, calendar conventions, and currency expressions are not Ethiopianized. — _Sources: Q2, Q106_
- **IC-3**: Yes — the seed SLURP data reflects Western/Anglophone virtual-assistant interaction patterns (smart-home, music, weather domains [Q9, Q13, Q14]). Localization noise [Q107] further means inputs may carry residual Western reference frames. — _Sources: Q106, Q107_
- **IC-4**: Recruitment of Ethiopian intercity-traveler-representative annotators is necessary; gap_id 5 confirms no L2-Amharic-speaker NLP dataset exists, and gap_id 11 confirms operator-specific data requires direct elicitation. INSUFFICIENT DOCUMENTATION on Amharic translator demographics in MASSIVE. — _Sources: WEB-17_
- **IC-5**: Severe content-validity issues: absence of Ethiopian temporal expressions, locally varied city names, Birr fares, and code-switching with Oromo/Tigrinya (gaps 1, 2, 3, 4, 7) means the benchmark's Amharic inputs do not represent the target distribution. This is the dominant validity concern. — _Sources: Q103, Q107, WEB-21_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'MASSIVE was created by tasking professional translators to localize the English-only SLURP dataset into 50 typologically diverse languages from 29 genera.' (p.1)
- [Q4] 'MASSIVE was created by localizing the SLURP NLU dataset (created only in English) in a parallel manner.' (p.1)
- [Q103] 'Starting with the dataset, the per-language data quantities are relatively small at 19.5k total records and 11.5k records for training.' (p.9)
- [Q106] 'Third, the data were originally created through crowd-sourcing, not from a real virtual assistant, which introduces artificialities.' (p.9)
- [Q107] 'Relatedly, allowing the worker to decide on translation versus localization of slot entities added further noise to the dataset, although we try to store this decision in the metadata.' (p.9)

*Web sources:*
- [WEB-4] Ethiopian (Ge'ez) calendar: 13 months, 7–8-year offset from Gregorian — temporal expression slot values absent from MASSIVE
- [WEB-5] Timkat/Ethiopian Epiphany — major travel surge, Tir 11 E.C.
- [WEB-6] Meskel, Genna, Enkutatash — peak travel periods unrepresented in MASSIVE
- [WEB-21] EthioBenchmark does not include intent/slot data with Ethiopian temporal expressions, confirming absence of any bridge resource
- [WEB-17] EthioNLP survey — no booking-domain Amharic content

</details>

**Information gaps:**
- What fraction of Amharic slot instances in MASSIVE were marked 'localize' vs. 'translate' vs. 'unchanged' [Q58 metadata not summarized in paper]
- Whether any Amharic city names (e.g., Addis Ababa, Bahir Dar) appear in MASSIVE slot values

**Requires expert verification:**
- Confirmation that Ethiopian intercity travelers' real utterances frequently mix Birr/Ethiopian-calendar/local-variant values with code-switching
- Whether MASSIVE's Amharic data (despite limitations) provides sufficient typological prior for transfer learning to a finetuned booking model

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** medium

**Justification:**
Modality alignment is strong: MASSIVE is text-only [Q3] and Amharic is included as one of 51 languages, with 21 distinct scripts represented [Q25] including Ethiopic/Ge'ez fidel as a 'unique' script [Q27]. The deployment is also text-only smartphone input in Ethiopic script. Script diversity was explicitly sought 'to drive experimentation in tokenization and normalization' [Q20]. The paper acknowledges 'our collection system did not have a robust method to preserving or denoting native tokenization practices' [Q109], leaving slot-boundary handling for Amharic's morphologically rich, fusional structure as an open question (gap_id 8 PARTIAL — amseg and HornMorpho exist but not evaluated against MASSIVE Amharic). Amharic uses spaces as word delimiters, so unlike Japanese/Chinese/Khmer it does not require character-level splitting [Q80, Q92, Q96]. The IF dimension is rated LOWER priority and modality match is good, but documentation of Amharic-specific tokenization quality is absent.

**Strengths:**
- Text-only modality matches deployment exactly [Q3]
- Amharic Ethiopic script is included as a 'unique' script category [Q27]; script diversity was an explicit design goal [Q20]
- Amharic uses space-delimited words, sidestepping the character-spacing issues that affected Japanese/Chinese/Khmer [Q80, Q92] — the 'default spacing provided by annotators' [Q82] applies

**Checklist:**

- **IF-1**: Both source and target are text in Ethiopic script; no signal-distribution mismatch on modality. Smartphone keyboard input methods (fidel, phonetic IME, occasional Latin-script Amharic) are not specifically validated by MASSIVE — INSUFFICIENT DOCUMENTATION on input-method robustness. — _Sources: Q3_
- **IF-2**: Ethiopian smartphone infrastructure supports Ethiopic input; mobile penetration reached 61.4% Q1 2024 [WEB-9]; smartphone penetration ~15% nationally [WEB-8]. The deployment population is a self-selected app-user cohort with sufficient infrastructure. — _Sources: WEB-9, WEB-8_
- **IF-3**: Amharic morphological richness (cliticization, root-and-pattern morphology — regional context) means slot boundaries may span morphologically complex tokens; MASSIVE acknowledges 'collection system did not have a robust method to preserving or denoting native tokenization practices' [Q109], leaving slot-boundary quality for Amharic unverified. amseg and HornMorpho tokenizers exist [WEB-17, WEB-19] but were not used. — _Sources: Q109, WEB-17, WEB-19_
- **IF-4**: Form mismatches are minor: text-modality alignment is strong, but Amharic-specific tokenization quality and IME variants (fidel vs. romanized input) are not documented; this is a moderate but not severe external-validity risk. — _Sources: Q82, Q109_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] '587k train utterances, 104k dev utterances, 152k test utterances, and 153k utterances currently held out' (p.1)
- [Q20] 'Fifth, we examined the script of each language, seeking to increase script diversity to drive experimentation in tokenization and normalization.' (p.3)
- [Q25] 'There are 21 distinct scripts used in the dataset.' (p.3)
- [Q27] 'The Arabic script is used for three languages, the Cyrillic script for two languages, and the remaining 18 languages have "unique" scripts...' (p.3)
- [Q82] 'We use the default spacing provided by annotators for all other languages.' (p.7)
- [Q109] 'Fifth, our collection system did not have a robust method to preserving or denoting native tokenization practices...' (p.9)

*Web sources:*
- [WEB-9] Mobile penetration 61.4% Q1 2024; 4G expanded to 45+ cities — adequate infrastructure for text-modality deployment
- [WEB-8] Smartphone penetration ~15% nationally — deployment cohort is self-selected high-digital-literacy users
- [WEB-17] amseg Amharic segmenter/tokenizer (Yimam et al. 2021) exists
- [WEB-19] HornMorpho rule-based morphological analyzer used in Ethiopian NLP pipelines

</details>

**Information gaps:**
- Whether MASSIVE Amharic utterances were tokenized with amseg or default whitespace
- Per-language slot-F1 sensitivity to tokenization choice for Amharic specifically

**Requires expert verification:**
- Whether smartphone IME variation (fidel vs. phonetic vs. Latin) introduces real-world input distributions not represented in MASSIVE

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** medium

**Justification:**
The output label space (60 intents and 55 slots [Q1]) is the same structure used to generate the input ontology, so the same gaps apply on the output side. Operator-specific slot types required by the deployment — operator_name, seat_class, route_closure_reason, surcharge_event, trip_change_type, departure_terminal — are absent from the 55-slot taxonomy (regional context, operator_specific_slot_types). The paper itself describes the schema as 'relatively simple when compared with hierarchical labeling schemata or flat schemata with more intent and slot options' [Q108]. Output decision rules (label/F1/exact match) are language-agnostic, so cultural decision-rule misalignment per se is limited — the violation is primarily content-validity (missing categories) rather than structural-validity for the labels that do exist. The text-to-text decoder format ('sequence of labels … followed by the intent' [Q73]) is compatible with the deployment.

**Strengths:**
- 55-slot taxonomy includes generic temporal, location, and entity slots [Q1] that partially cover booking attributes
- Slot localization metadata (translate/localize/unchanged) is preserved [Q58], allowing post-hoc filtering
- Judgment metadata for intent/slot semantic match is included [Q63, Q64], supporting label-quality auditing

**Checklist:**

- **OO-1**: Generic booking-relevant slot types (date, time, place_name, person, etc.) implied by 18 domains [Q1] partially apply. Ethiopian-specific slots (operator_name, seat_class, departure_terminal) are absent — confirmed by gap_id 11 (operator-specific seat-class taxonomy not publicly available). — _Sources: Q1_
- **OO-2**: Missing categories: operator_name, seat_class, route_closure_reason, surcharge_event (holiday-driven), trip_change_type, departure_terminal — none are in the 55-slot taxonomy [Q1, Q108]. — _Sources: Q1, Q108, WEB-21_
- **OO-3**: The 60 intents reflect global virtual-assistant priorities [Q16] (smart-home, music, weather, etc.) that encode non-Ethiopian commercial assumptions; this is more construct-irrelevant variance than a values-encoding violation. — _Sources: Q16_
- **OO-4**: Stakeholder-driven taxonomy redesign is needed for operator-specific slots; gap_id 11 confirms no public operator taxonomy exists, requiring direct elicitation. — _Sources: Q108_
- **OO-5**: Structural validity is only mildly affected (label format is compatible); content validity is moderately to strongly affected by missing slot types [Q108]. — _Sources: Q108, Q73_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] '... 18 domains, 60 intents, and 55 slots.' (p.1)
- [Q58] '... whether the worker elected to "localize," "translate," or keep the slot "unchanged," primarily for the purposes of researchers evaluating machine translation systems...' (p.6)
- [Q73] 'The decoder output is a sequence of labels (including the Other label) for all of the tokens followed by the intent.' (p.7)
- [Q108] 'Fourth, our labeling schema is relatively simple when compared with hierarchical labeling schemata or flat schemata with more intent and slot options.' (p.9)

*Web sources:*
- [WEB-21] No African transport-domain slot taxonomy exists — operator-specific slot types must be developed locally

</details>

**Information gaps:**
- Detailed list of MASSIVE's 55 slot types to determine partial overlap with booking-domain needs

**Requires expert verification:**
- Operator-specific seat-class enumeration and route-closure reason categories (gap_id 11)

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Annotators were vendor-pool MTurk workers selected via a listening-based fluency test [Q51], a three-judgment quality test [Q52], and a translator quiz with 'customized local-language examples' [Q53]; workers self-certified as 'native speaker or … fluent in the required language' [Q122]. Annotator demographics — whether Amharic translators are urban Addis residents, Amhara-region speakers, or L2 speakers — are not disclosed (regional context, amharic_dialect_variation.massive_annotator_dialect_representation: NOT FOUND). The paper acknowledges 'the lack of labeled data … that is realistic for the task and that is natural for each given language' [Q6] as the central problem the dataset attempts to address — but the translation-from-English pipeline means Amharic instances reflect English-language pragmatics translated into Amharic [Q2, Q4]. The user has confirmed code-switching with Oromo (Q3 elicitation) will occur in real utterances, and gaps 3 and 4 confirm no Oromo–Amharic or Tigrinya–Amharic code-switching booking-domain corpus exists. 'Some low-quality utterances' are acknowledged [Q104] and removable only at the cost of further reducing the already small per-language sample [Q103, Q105]. OC was rated HIGH priority and the violation is severe.

**Strengths:**
- Multi-stage quality controls: fluency test [Q51], three-judgment QA [Q52], translator quiz [Q53], MT-detection alarms [Q66]
- Three independent judgment scores per utterance covering intent match, slot match, grammaticality, spelling, language identification [Q63] — included in metadata [Q64] for filtering
- Self-certified native/fluent speakers [Q122] and vendor monitoring for engagement quality [Q44, Q66]

**Checklist:**

- **OC-1**: No — labels reflect English-source intent/slot judgments translated into Amharic [Q2, Q4]; they do not reflect Ethiopian intercity-traveler stakeholder perspectives. Code-switching, L2-speaker phrasing, and operator-specific slot judgments are not represented (gaps 3, 4, 5). — _Sources: Q2, Q4, Q6_
- **OC-2**: Substantial disagreement is likely between MASSIVE Amharic annotators (translators of English seed data) and the actual Ethiopian intercity-traveler population, particularly for code-switched and Ethiopian-calendar-bearing utterances (Q3 elicitation; gaps 3, 4, 5). — _Sources: Q104, WEB-18, WEB-20, WEB-1_
- **OC-3**: Demographic information for Amharic translators is not disclosed in the paper — workers are described only as fluency-tested vendors [Q41, Q42, Q51, Q122]. The regional context confirms 'NOT FOUND' for translator regional/dialect background. — _Sources: Q41, Q51, Q122_
- **OC-4**: Re-annotation by representative Ethiopian intercity travelers (urban Addis, regional Amhara, Amharic-as-L2 speakers) is needed; gap_id 5 confirms no existing L2-speaker NLP dataset to bootstrap from. — _Sources: Q6_
- **OC-5**: Aggregation uses three judgment workers per utterance [Q63]; if the three-worker pool is demographically homogeneous (e.g., all urban Addis fluent speakers), L2-speaker and code-switched perspectives are systematically excluded. INSUFFICIENT DOCUMENTATION on judgment-worker demographics. — _Sources: Q63_
- **OC-6**: Severe convergent and external-validity risks: labels do not correlate with regional stakeholder judgments for the linguistic phenomena (code-switching, L2 phrasing, calendar/operator slots) that the deployment must handle [Q6, Q104, Q107]. — _Sources: Q104, Q107, WEB-20_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q6] 'one difficulty in creating massively multilingual NLU models is the lack of labeled data for training and evaluation, particularly data that is realistic for the task and that is natural for each given language.' (p.1)
- [Q41] 'The MASSIVE dataset was collected using a customized workflow powered by Amazon MTurk.' (p.5)
- [Q51] '... an Amazon MTurk-hosted fluency test where workers listen to questions and statements in the relevant language and were evaluated using a multiple-choice questionnaire.' (p.6)
- [Q63] 'The output of the second workflow ... is judged by three workers for (1) whether the utterance matches the intent semantically, (2) whether the slots match their labels semantically, (3) grammaticality and naturalness, (4) spelling, and (5) language identification...' (p.6)
- [Q104] 'Second, there are some low-quality utterances, both in the seed data and in the translations.' (p.9)
- [Q105] '... if a user does filtering based on these judgments, then the data size decreases even further.' (p.9)
- [Q122] 'By clicking "SUBMIT", I also certify that I am a native speaker or am fluent in the required language' (p.17)

*Web sources:*
- [WEB-18] Amharic–Afaan Oromo bilingual code-switching corpus exists for hate speech only — domain mismatch with booking
- [WEB-20] Amharic/Oromo/Tigrigna code-switching empirically documented in Ethiopian social media — confirms the phenomenon is real and is unrepresented in monolingual MASSIVE Amharic
- [WEB-1] Oromo speakers >40% of Ethiopia's population — large L2-Amharic share among intercity travelers

</details>

**Information gaps:**
- Vendor identity and translator regional/dialect demographics for Amharic
- Distribution of judgment scores for Amharic utterances and how filtering by score affects size

**Requires expert verification:**
- Empirical disagreement rate between MASSIVE Amharic labels and Ethiopian intercity-traveler relabels on a sample
- Whether code-switched Amharic–Oromo utterances would be rejected by MASSIVE's language-identification judgment [Q63]

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
MASSIVE's output format — intent classification + token-level slot-fill sequence [Q70, Q71, Q73] — directly matches what an intent-and-slot booking system requires. Three primary metrics are reported: 'exact match accuracy, intent classification accuracy, and slot-filling F1 score' [Q5], with per-language breakdowns [Q126, Q127, Q128] and 95% confidence intervals [Q89]. Per-language Amharic results are reported, allowing direct estimation of expected performance. However, two structural concerns remain: (1) Pearson correlation of 0.54 between XLM-R pretraining data quantity and zero-shot exact match [Q87], combined with the finding that 'Germanic genera and Latin scripts performed the best overall' [Q98] and that low-pretraining-data languages like Icelandic underperformed [Q100], strongly suggests Amharic — a unique-script, lower-resource language — will fall in the lower-performance tier; (2) deployment may eventually require text-to-speech for accessibility (literacy ~51.8% in 2017, urban–rural gap [WEB-3, WEB-12, WEB-11]), but MASSIVE evaluates only text outputs [Q5]. OF was rated LOWER priority and overall format alignment is strong.

**Strengths:**
- Output format (intent label + slot-token sequence) directly matches deployment requirement [Q70, Q73]
- Three primary metrics (exact match, intent accuracy, slot F1) match standard NLU evaluation [Q5]
- Per-language results published for Amharic [Q126, Q127, Q128] allowing direct expected-performance estimation
- Reports both full-dataset and zero-shot performance [Q83, Q85] enabling lower-bound estimation for low-resource transfer scenarios

**Checklist:**

- **OF-1**: Yes — text-based intent + slot output matches the booking-bot deployment exactly [Q70, Q71, Q73]. — _Sources: Q5, Q73_
- **OF-2**: MASSIVE evaluates text only [Q5]; if accessibility for lower-literacy users requires TTS output (literacy ~51.8% adult, [WEB-3, WEB-12]; rural literacy lower [WEB-11]), MASSIVE provides no signal on TTS quality. INSUFFICIENT DOCUMENTATION on speech-output evaluation. — _Sources: Q5, WEB-3, WEB-12_
- **OF-3**: Adult literacy ~51.8% (2017 data, [WEB-3, WEB-12]); the deployment's smartphone-app cohort is a higher-literacy self-selected subset, but accessibility for less literate or older travelers may require speech output not evaluated by MASSIVE. — _Sources: WEB-3, WEB-12, WEB-11_
- **OF-4**: Form mismatches are minor for the text-NLU output but expected Amharic performance is in the lower tier per the script/pretraining-data correlation [Q87, Q98, Q100]; this is a performance-distribution concern rather than a form mismatch. — _Sources: Q87, Q98, Q100_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q5] 'We also present modeling results on XLM-R and mT5, including exact match accuracy, intent classification accuracy, and slot-filling F1 score.' (p.1)
- [Q73] 'The decoder output is a sequence of labels (including the Other label) for all of the tokens followed by the intent.' (p.7)
- [Q87] '... Pearson correlation of 0.54 for exact match' (p.7)
- [Q98] 'Germanic genera and Latin scripts performed the best overall...' (p.8)
- [Q100] 'Icelandic was the lowest-performing Germanic language, likely due to a lack of pretraining data...' (p.8)
- [Q126] 'Exact match accuracy by language for our three models using the full dataset and the zero-shot setup.' (p.20)

*Web sources:*
- [WEB-3] Ethiopia adult literacy ~51.8% (2017)
- [WEB-12] UNESCO literacy data corroborates ~51.8% figure
- [WEB-11] Significant urban–rural literacy gap; pastoralist regions much lower

</details>

**Information gaps:**
- Reported MASSIVE Amharic exact-match / intent-acc / slot-F1 numbers (Tables 7–9, [Q126, Q127, Q128]) were not surfaced in the documentation extract

**Requires expert verification:**
- Whether the deployment ultimately requires TTS output for accessibility, beyond text-only NLU

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** Ethiopian-calendar dates, local city name variants (Adama/Nazret, Mekelle/Mek'ele), Birr fare expressions, and holiday-surcharge contexts are absent from translated MASSIVE Amharic data

**Recommendation:** Construct a supplementary slot-filling test set of 1–3k Amharic booking utterances elicited from Ethiopian intercity travelers, covering Ge'ez calendar months, alternate city names, Birr numerals (Arabic, Ethiopic, and verbalized forms), and named holidays (Timkat, Meskel, Enkutatash, Genna, Fasika, Eid). Use this as the primary acceptance test, with MASSIVE Amharic as a secondary baseline.

### Output Content ⚠

**Gap:** Amharic translator demographics undisclosed; no representation of L2-Amharic speakers or code-switching with Oromo/Tigrinya, despite user confirmation that these occur in real utterances

**Recommendation:** Recruit a regional annotator pool stratified across urban Addis, Amhara region, and L2-Amharic speakers from Oromia and Tigray corridors. Re-label a sample of MASSIVE Amharic utterances and measure inter-annotator agreement against original labels; then build a code-switched evaluation set drawing on the Amharic–Oromo corpus [WEB-18] and RAIL 2024 lexicon [WEB-20] adapted to booking-domain vocabulary.

### Input Form

**Gap:** Amharic tokenization for slot boundaries not robustly handled by MASSIVE [Q109]; morphological richness may obscure slot spans

**Recommendation:** Re-tokenize Amharic training/eval data using amseg [WEB-17] or HornMorpho [WEB-19] morphological segmentation, and compare slot-F1 against MASSIVE's default whitespace tokenization to quantify the tokenization-quality effect on slot boundary detection.

### Input Ontology

**Gap:** Intercity-transport-specific intents (route_query, operator_query, seat_class_query, cancel_and_rebook, holiday_surcharge_query, departure_terminal_query) absent from MASSIVE's 60-intent taxonomy

**Recommendation:** Extend the intent taxonomy with at least these six transport-specific intents through stakeholder elicitation with Sky Bus, Selam Bus, and Ride operators (gap_id 11). Ensure each new intent has ≥100 elicited Amharic examples for training and ≥50 for held-out testing.

### Output Form

**Gap:** Expected lower-tier performance for Amharic per pretraining-data and script correlations [Q87, Q98, Q100]; reliance on text-only output may underserve lower-literacy users (~51.8% adult literacy)

**Recommendation:** Report Amharic-specific exact-match, intent-accuracy, and slot-F1 separately rather than aggregated; set deployment thresholds based on Amharic-only metrics. If accessibility for lower-literacy users is in scope, supplement with a TTS-output evaluation track outside MASSIVE.

### Output Ontology

**Gap:** Operator-specific slot types (operator_name, seat_class, route_closure_reason, surcharge_event, trip_change_type, departure_terminal) missing from 55-slot taxonomy

**Recommendation:** Define an extended slot taxonomy with operator-specific types and an enumerated value set per slot (e.g., seat_class ∈ {VIP, economy, sleeper, …} resolved via direct operator elicitation). Annotate the supplementary test set against this extended taxonomy, keeping MASSIVE-compatible slot types for backward comparability.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "MASSIVE contains 1M realistic, parallel, labeled virtual assistant utterances spanning 51 languages, 18 domains, 60 intents, and 55 slots." |
| Q2 | 1 | input_content | "MASSIVE was created by tasking professional translators to localize the English-only SLURP dataset into 50 typologically diverse languages from 29 genera." |
| Q3 | 1 | input_form | "With the English seed data included, there are 587k train utterances, 104k dev utterances, 152k test utterances, and 153k utterances currently held out for the MMNLU-22 competition, which will be released after the competition." |
| Q4 | 1 | input_content | "MASSIVE was created by localizing the SLURP NLU dataset (created only in English) in a parallel manner." |
| Q5 | 1 | output_form | "We also present modeling results on XLM-R and mT5, including exact match accuracy, intent classification accuracy, and slot-filling F1 score." |
| Q6 | 1 | output_content | "one difficulty in creating massively multilingual NLU models is the lack of labeled data for training and evaluation, particularly data that is realistic for the task and that is natural for each given language." |
| Q7 | 1 | output_content | "High naturalness typically requires human-based vetting, which is often costly." |
| Q8 | 1 | input_content | "Jack FitzGerald, Christopher Hench, Charith Peris, Scott Mackie, Kay Rottmann, Ana Sanchez, Aaron Nash, Liam Urbach, Vishesh Kakarala, Richa Singh, Swetha Ranganath, Laurie Crist, Misha Britan, Wouter Leeuwis, Gokhan Tur, Prem Natarajan from Amazon, Microsoft, Tripadvisor, and Capital One." |
| Q9 | 2 | input_content | "The first iteration for the foundation of the MASSIVE dataset was the NLU Evaluation Benchmarking Dataset, with 25k utterances across 18 domains (Liu et al., 2019a)." |
| Q10 | 2 | input_form | "The authors updated the dataset and added audio and ASR transcriptions in the release of the Spoken Language Understanding Resource Package (SLURP) (Bastianelli et al., 2020), allowing for full end-to-end Spoken Language Understanding (SLU) evaluation similar to the Fluent Speech Commands dataset (Lugosch et al., 2019) and Chinese Audio-Textual Spoken Language Understanding (CATSLU) (Zhu et al., 2019)." |
| Q11 | 2 | input_ontology | "We release the MASSIVE dataset along with baselines from large pre-trained models fine-tuned on the NLU slot and intent prediction tasks." |
| Q12 | 2 | input_ontology | "This work focuses on the general multi-domain NLU task and builds off the SLURP (Bastianelli et al., 2020) benchmark dataset to extend to an unprecedented 50 new languages." |
| Q13 | 2 | input_ontology | "The Snips datasets (both the original English only and the English and French releases) are most similar to the NLU contained in the MASSIVE dataset, spanning smart home and music domains for a generic voice-based virtual assistant." |
| Q14 | 2 | input_content | "Facebook released a general Intelligent Virtual Assistant (IVA) dataset across the domains of Alarm, Reminder, and Weather (Schuster et al., 2019) created for the purpose of demonstrating cross-lingual transfer learning; and so did not need to be parallel or have an equal number of datapoints, resulting in far fewer examples in Thai (5k) compared to Spanish (7.6k) and English (43k)." |
| Q15 | 3 | input_content | "The languages in MASSIVE were chosen according to the following considerations. First, we acquired cost and worker availability estimates for over 100 languages, providing a constraint to our choices given our fixed budget." |
| Q16 | 3 | input_ontology | "Second, we determined existing languages available in major virtual assistants, such that the dataset could be used to benchmark today's systems." |
| Q17 | 3 | input_content | "Third, we categorized the full pool of languages according to their genera as taken from the World Atlas of Linguistic Structures (WALS) database (Dryer and Haspelmath, 2013), where a genus is a language group that is clear to most linguists without systematic comparative analysis." |
| Q18 | 3 | input_ontology | "Genus is a better indicator of typological diversity, which we sought to maximize, than language family (Dryer, 1989)." |
| Q19 | 3 | input_content | "Fourth, we used the eigenvector centrality of Wikipedia articles, tweets, and book translations (Ronen et al., 2014) as proxies for the internet influence and thus the resource availability of a given language, particularly for self-supervised pretraining applications, and we chose languages spanning the breadth of resource availability." |
| Q20 | 3 | input_form | "Fifth, we examined the script of each language, seeking to increase script diversity to drive experimentation in tokenization and normalization." |
| Q21 | 3 | input_content | "Ultimately, we created 50 new, distinct text corpora, representing 49 different spoken languages." |
| Q22 | 3 | input_content | "Mandarin Chinese was collected twice, once with native speakers who use the traditional set of characters, and once with native speakers who use the modern simplified set of characters." |
| Q23 | 3 | input_content | "There are 14 language families in the dataset." |
| Q24 | 3 | input_ontology | "In MASSIVE, we also include "language isolates" as families. These are languages that have no clear relationship to any known language." |
| Q25 | 3 | input_form | "There are 21 distinct scripts used in the dataset." |
| Q26 | 3 | input_form | "The majority of languages in MASSIVE (28 including English) use some variety of the Latin alphabet, which is also the most widely used script in the world." |
| Q27 | 3 | input_form | "The Arabic script is used for three languages, the Cyrillic script for two languages, and the remaining 18 languages have "unique" scripts, in the sense that only one language in the dataset uses that script." |
| Q28 | 3 | input_form | "Fourteen scripts are unique to a single language, although they may belong to a larger family of writing systems." |
| Q29 | 4 | input_content | "MASSIVE consists of utterances directed at a device, rather than a person, which has some consequences for the type of linguistic patterns it contains." |
| Q30 | 4 | input_ontology | "Specifically, the corpus primarily consists of interrogatives (i.e., questions) and imperatives (commands or requests)." |
| Q31 | 4 | input_ontology | "There are relatively few declarative utterances in the set." |
| Q32 | 4 | input_ontology | "This is in contrast to many large datasets from other sources (e.g., wikipedia, movie scripts, newspapers) which contain a high proportion of declaratives, since the language is collected from situations where humans are communicating with humans." |
| Q33 | 4 | input_content | "In the context of a voice assistant, a user typically asks a device to perform an action or answer a question, so declaratives are less common." |
| Q34 | 4 | input_ontology | "In MASSIVE, 39 languages are subject-initial (24 SVO and 15 SOV), while only three are verb-initial (VSO specifically)." |
| Q35 | 4 | input_ontology | "No object-initial languages are represented." |
| Q36 | 4 | input_ontology | "Five languages are marked in WALS as having no preferred word order, and four do not have any word order data at all." |
| Q37 | 4 | input_ontology | "The majority of them (33) use some kind of verb morphology, such as adding a suffix." |
| Q38 | 4 | input_ontology | "About half of those languages (18) have distinct imperative" |
| Q39 | 5 | input_content | "We randomly sampled a subset of the English seed data which was then paraphrased by professional annotators, resulting in new, more challenging utterances, including 49% more slots per utterance." |
| Q40 | 5 | output_form | "These utterances were localized along with the other splits to be used as a held out evaluation set for the Massively Multilingual NLU-22 competition and workshop." |
| Q41 | 5 | input_content | "The MASSIVE dataset was collected using a customized workflow powered by Amazon MTurk." |
| Q42 | 5 | input_content | "We required a vendor pool with the capability and resources to collect a large multilingual dataset." |
| Q43 | 5 | output_content | "Our original vendor pool consisted of five vendors adjudicated based on previous engagements." |
| Q44 | 5 | output_content | "This vendor pool was reduced to three based on engagement and resource availability." |
| Q45 | 5 | output_content | "Vendors for each language were selected based on their resource" |
| Q46 | 5 | input_ontology | "Nearly half of the languages in MASSIVE (21) make a two-way formal/informal distinction in their second-person pronouns." |
| Q47 | 5 | input_ontology | "A further eight languages have more than two levels of formality, such as informal, formal, and honorific." |
| Q48 | 5 | input_ontology | "Seven languages have an "avoidance" strategy, which means that pronouns are omitted entirely in a polite scenario." |
| Q49 | 5 | input_ontology | "Finally, eleven languages have no data on politeness in WALS at all." |
| Q50 | 6 | input_content | "A majority of languages were supported by a single vendor, while some languages required cross-vendor support to be completed with the required quality and within the required timeline." |
| Q51 | 6 | output_content | "We offered two mechanisms to vendors for evaluating workers to be selected for each language. The first, which was used to select workers for the translation task, was an Amazon MTurk-hosted fluency test where workers listen to questions and statements in the relevant language and were evaluated using a multiple-choice questionnaire." |
| Q52 | 6 | output_content | "The second, which was used to select workers for the judgment task, was a test with a set of three judgments that the vendor could use to assess if workers were able to detect issues in the translated utterances." |
| Q53 | 6 | output_content | "In order to further improve worker selection quality, we created a translator quiz using the Amazon MTurk instructions that were created for translation and judgment tasks, coupled with customized local-language examples." |
| Q54 | 6 | output_content | "Before commencing operations, an initial pilot run of this customized workflow was completed in three languages." |
| Q55 | 6 | input_form | "The collection was conducted by locale on an individual utterance level. Each utterance from the "train," "dev," "test," and "heldout" splits of the SLURP dataset went through two sequential task workflows and a judgment workflow." |
| Q56 | 6 | input_ontology | "The first task is slot translation or localization (see Figure 1). Workers are presented the entire utterance with colored highlighting of the slot values for the utterance (if any) and then presented with each slot value and its corresponding label individually." |
| Q57 | 6 | input_ontology | "The worker is asked to either localize or translate the slot, depending on whether the value should be translated (e.g., "tomorrow") or localized (e.g., the movie "La La Land", which in French is "Pour l'amour d'Hollywood.")" |
| Q58 | 6 | output_ontology | "The metadata of the released dataset includes whether the worker elected to "localize," "translate," or keep the slot "unchanged," primarily for the purposes of researchers evaluating machine translation systems, where it would be unreasonable to expect the system to "localize" to a specific song name the worker selected." |
| Q59 | 6 | input_ontology | "After the slot task, the second worker is asked to translate or localize the entire phrase using the slot task output provided by the first worker (see Figure 2)." |
| Q60 | 6 | input_ontology | "The phrase worker can decide to keep the slot as it was translated, modify it, or remove it entirely if it is not relevant for the language in that scenario." |
| Q61 | 6 | input_ontology | "This worker is also responsible for aligning grammatical genders or prepositional affixes to any of the slots." |
| Q62 | 6 | output_content | "Note that this two-step system alleviates the annotation burden often encountered with such work. Traditionally in such collections, workers would be given a light annotation guide and asked to highlight spans of the slots in a translated or localized utterance." |
| Q63 | 6 | output_form | "The output of the second workflow (the fully localized utterance) is judged by three workers for (1) whether the utterance matches the intent semantically, (2) whether the slots match their labels semantically, (3) grammaticality and naturalness, (4) spelling, and (5) language identification—English or mixed utterances are acceptable if that is natural for the language, but localizations without any tokens in the target language were not accepted." |
| Q64 | 6 | output_ontology | "These judgments are also included in the metadata of the dataset." |
| Q65 | 6 | output_content | "In addition to the workers judging each other's work, the collection system had alarms in place for workers with high rejection rates, high rates of slot deletion, and high rates of English tokens in the translations." |
| Q66 | 6 | output_content | "Workers were also monitored to see if their tasks were primarily machine translated. Such workers were removed from the pool and all of their work was resubmitted to be completed by the other workers." |
| Q67 | 7 | input_ontology | "As initial model benchmarks, we fine-tuned publicly-available pre-trained language models on the MASSIVE dataset and evaluated them on intent classification and slot filling." |
| Q68 | 7 | output_form | "Our models of choice for this exercise were XLM-Roberta (XLM-R; Conneau et al. 2020) and mT5 (Xue et al., 2021)." |
| Q69 | 7 | output_form | "In the case of XLM-R, we utilized the pretrained encoder with two separate classification heads trained from scratch, based on JointBERT (Chen et al., 2019a)." |
| Q70 | 7 | output_form | "The first classification head used the pooled output from the encoder to predict the intent and the second used the sequence output to predict the slots." |
| Q71 | 7 | output_form | "As pooling for the intent classification head, we experimented with using hidden states from the first position, averaged hidden states across the sequence, and the maximally large hidden state from the sequence." |
| Q72 | 7 | output_form | "With mT5, we explored two separate architectures. In one architecture, we only used the pre-trained encoder extracted from mT5, and we trained two classification heads from scratch similarly to the XLM-R setup. We refer to this setup as mT5 Encoder-Only. In the other architecture, we used the full sequence-to-sequence mT5 model in text-to-text mode, where the input is "Annotate:" followed by the unlabeled utterance." |
| Q73 | 7 | output_ontology | "The decoder output is a sequence of labels (including the Other label) for all of the tokens followed by the intent." |
| Q74 | 7 | output_form | "For all models, we used the Base size, which corresponds to 270M parameters for XLM-R, 258M parameters for mT5 Encoder-Only, and 580M parameters for mT5 Text-to-Text, including 192M parameters for embeddings for all three." |
| Q75 | 7 | output_form | "For each model, we performed 128 trials of hyperparameter tuning using the Tree of Parzen Estimators algorithm and Asynchronous Successive Halving Algorithm (ASHA) (Li et al., 2018a) for scheduling, which are both part of the hyperopt library (Bergstra et al., 2013) integrated into the ray[tune] library (Liaw et al., 2018)." |
| Q76 | 7 | output_form | "We trained our models with the Adam optimizer (Kingma and Ba, 2017) and chose the best performing model checkpoint based on overall exact match accuracy across all locales." |
| Q77 | 7 | output_form | "Hyperparameter tuning and fine-tuning was performed using single p3dn.24xlarge instances (8 x Nvidia v100) for XLM-R and mT5 Text-to-Text and a single g4dn.metal instance (8 x Nvidia T4) for mT5 Encoder-Only." |
| Q78 | 7 | output_form | "Hyperparameter tuning times were less than 4 days per model and training times were less than 1 day per model." |
| Q79 | 7 | input_form | "Our dataset includes several languages where white spacing is not used as a word delimiter. In some cases, spaces do occur, but they might serve as phrase delimiters or denote the end of a sentence." |
| Q80 | 7 | input_form | "Three of these written languages, Japanese, Chinese (Traditional), and Chinese (Simplified), do not use spaces anywhere except to identify the end of a sentence. For these languages, we separate each character in the unlabeled input with a whitespace." |
| Q81 | 7 | input_form | "We leave exploration of more sophisticated techniques (such as MeCab for Japanese; Kudo 2005) to future work." |
| Q82 | 7 | input_form | "We use the default spacing provided by annotators for all other languages." |
| Q83 | 7 | output_form | "Zero-shot performance was also assessed, in which the models were trained on English data, validation was performed on all languages, and testing was performed on all non-English locales." |
| Q84 | 7 | output_form | "Table 3 shows the results for each model and training setup, including those for the best performing locale, the worst performing locale, and locale-averaged results for intent accuracy, micro-averaged slot F1 score, and exact match accuracy." |
| Q85 | 7 | output_form | "Zero-shot exact match performance is 25-37 points worse than that of full-dataset training runs." |
| Q86 | 7 | output_form | "Additionally, the variance in task performance across locales is significantly greater for the zero-shot setup than for full-dataset training. For example, there is a 15 point difference in exact match accuracy between the highest and lowest locales for mT5 Text-to-Text when using the full training set, while the gap expands to 44 points with zero-shot." |
| Q87 | 7 | output_form | "We compared the pretraining data quantities by language for XLM-R to its per-language task performance values, and in the zero shot setup, we found a Pearson correlation of 0.54 for exact match" |
| Q88 | 8 | output_form | "Each table includes the highest locale, the lowest locale, and locale-averaged results for intent accuracy, micro-averaged slot F1 score, and exact match accuracy." |
| Q89 | 8 | output_form | "Intervals for 95% confidence are given assuming normal distributions." |
| Q90 | 8 | output_form | "In the full dataset training setup, the correlations decrease to 0.42 for exact match accuracy, 0.47 for intent accuracy, and 0.24 for micro-averaged slot F1 score." |
| Q91 | 8 | input_form | "In Thai, for which spacing is optional, the model can learn from artificial spacing in the input (around where the slots will be) to improve task performance." |
| Q92 | 8 | output_content | "For Khmer, the workers had a difficult time adapting their translations and localizations to properly-slotted outputs given the space-optional nature of the language." |
| Q93 | 8 | input_form | "Additionally, for Japanese and Chinese, we added spaces between all characters when modeling." |
| Q94 | 8 | input_form | "By splitting into single characters, we don't allow the model to the use embeddings learned for chunks of characters." |
| Q95 | 8 | output_form | "This is a likely major cause of the drop in exact match accuracy for Japanese from 58.3% when training on the full dataset to 9.4% for zero shot." |
| Q96 | 8 | input_form | "character spacing was necessary in order to properly assign the slots to the right characters." |
| Q97 | 8 | input_form | "As mentioned in Section 5.1, we leave exploration of more sophisticated spacing techniques for slot filling (such as MeCab; Kudo 2005) to future work." |
| Q98 | 8 | output_form | "Discounting for artificial spacing effects, Germanic genera and Latin scripts performed the best overall (See Appendix E), which is unsurprising given the amount of pretraining data for those genera and scripts, as well as the quantity of Germanic and Latin-script languages in MASSIVE." |
| Q99 | 8 | output_form | "Within the Germanic genera, Swedish, English, Danish, Norwegian, and Dutch all performed comparably (within 95% confidence bounds) for exact match accuracy." |
| Q100 | 8 | output_form | "Icelandic was the lowest-performing Germanic language, likely due to a lack of pretraining data, as well as to its linguistic evolution away from the others due to isolated conditions." |
| Q101 | 8 | input_ontology | "We have released a truly MASSIVE multilingual dataset for NLU spanning 51 typologically diverse languages." |
| Q102 | 9 | input_content | "There are several significant limitations of the MASSIVE dataset and of our modeling." |
| Q103 | 9 | input_content | "Starting with the dataset, the per-language data quantities are relatively small at 19.5k total records and 11.5k records for training." |
| Q104 | 9 | output_content | "Second, there are some low-quality utterances, both in the seed data and in the translations." |
| Q105 | 9 | output_content | "For the most part, these are surfaced through the judgment scores we provide for each record, but if a user does filtering based on these judgments, then the data size decreases even further." |
| Q106 | 9 | input_content | "Third, the data were originally created through crowd-sourcing, not from a real virtual assistant, which introduces artificialities." |
| Q107 | 9 | input_content | "Relatedly, allowing the worker to decide on translation versus localization of slot entities added further noise to the dataset, although we try to store this decision in the metadata." |
| Q108 | 9 | output_ontology | "Fourth, our labeling schema is relatively simple when compared with hierarchical labeling schemata or flat schemata with more intent and slot options." |
| Q109 | 9 | input_form | "Fifth, our collection system did not have a robust method to preserving or denoting native tokenization practices—some languages do not separate with whitespace, while others do but there is no set practice." |
| Q110 | 9 | input_form | "This results in potentially easier (larger chunks to predict slot labels) or harder (each character individually predicted) tasks." |
| Q111 | 9 | output_content | "Sixth, it's possible, though unlikely, that some of our new crowd-sourced records may contain toxic or otherwise objectionable content." |
| Q112 | 9 | output_content | "We performed analyses to check for such malicious activities and did not find any as such." |
| Q113 | 9 | output_form | "Regarding modeling, we have only investigated base-sized models in relatively standard setups, leaving room for much more sophisticated modeling." |
| Q114 | 9 | output_content | "The risks associated with this dataset and work are relatively low, given that we have released a research dataset meant to promote better multilinguality in NLP systems." |
| Q115 | 13 | input_form | "Additional linguistic characteristics of our languages are given in Table 4." |
| Q116 | 13 | input_content | "Screenshots from our collection workflow are given in Figures 1, 2, and 3." |
| Q117 | 13 | output_form | "The hyperparameter search spaces and the chosen hyperparameters are given in Tables 5 and 6." |
| Q118 | 13 | output_form | "Results for all languages are given for exact match accuracy in Table 7, intent accuracy in Table 8, and micro-averaged slot-filling F1 in Table 9." |
| Q119 | 13 | output_form | "We pick our best performing model, mT5 Text-to-Text, and provide a summary of its performance on different language characteristics in Figures 4 and 5." |
| Q120 | 17 | output_content | "How would you rate these sentences?" |
| Q121 | 17 | output_content | "Please respond to the following questions about the TRANSLATED SENTENCE TO RATE." |
| Q122 | 17 | output_content | "By clicking "SUBMIT", I also certify that I am a native speaker or am fluent in the required language" |
| Q123 | 18 | output_form | "The full-dataset hyperparameter search space, the sampling technique, and the chosen hyperparameter for our 3 models." |
| Q124 | 18 | output_form | "The search space for the "quniform" and "qloguniform" sampling techniques is given as [min, max, increment]." |
| Q125 | 19 | output_form | "The zero-shot hyperparameter search space, the sampling technique, and the chosen hyperparameter for our 3 models." |
| Q126 | 20 | output_form | "Exact match accuracy by language for our three models using the full dataset and the zero-shot setup." |
| Q127 | 21 | output_form | "Table 8: Intent accuracy by language for our three models using the full dataset and the zero-shot setup." |
| Q128 | 22 | output_form | "Micro-averaged slot-filling F1 by language for our three models using the full dataset and the zero-shot setup." |
| Q129 | 23 | output_form | "The categories of each language characteristic are sorted by exact match accuracy for readability." |
| Q130 | 23 | input_content | "The number of languages falling into each category is provided in the bar chart in the lowest panel for each characteristic." |
| Q131 | 24 | output_form | "mT5 Text-to-Text performance grouped by Script, Family, Order, Politeness, Imperative Morphology, Imperative Hortative, Optative and Prohibitive." |
| Q132 | 24 | output_form | "As with Figure 4, the categories of each language characteristic are sorted by exact match accuracy for readability." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/html/2403.19365v1 |
| WEB-2 | https://srv1.worldometers.info/world-population/ethiopia-population/ |
| WEB-3 | https://www.cia.gov/the-world-factbook/about/archives/2023/countries/ethiopia/ |
| WEB-4 | https://ethiocal.com/ |
| WEB-5 | https://www.ethiopiancalendar.net/ethiopian-holidays |
| WEB-6 | https://holidays.ertale.com/ |
| WEB-7 | https://ethiopiancalendars.com/ |
| WEB-8 | https://birrmetrics.com/ethiopia-narrows-mobile-gender-gap-to-24-but-smartphone-access-for-women-remains-just-6/ |
| WEB-9 | https://www.connectingafrica.com/connectivity/ethiopia-s-telecoms-liberalization-makes-progress-omdia |
| WEB-10 | https://www.globenewswire.com/news-release/2025/01/27/3015813/0/en/Ethiopia-Mobile-Value-Added-Services-Market-to-Worth-Over-US-10-23-Billion-By-2033-Astute-Analytica.html |
| WEB-11 | https://zoetalentsolutions.com/education-statistics-for-ethiopia/ |
| WEB-12 | https://www.theglobaleconomy.com/Ethiopia/Literacy_rate/ |
| WEB-13 | https://cipit.org/ethiopias-personal-data-protection-proclamation-of-2024-and-its-budding-digital-identity-regime/ |
| WEB-14 | https://www.metaappz.com/References/ethiopian_laws/federal/pr_1321_2024/en/txt |
| WEB-15 | https://digitalpolicyalert.org/event/24922-implemented-personal-data-protection-proclamation-proclamation-no-13212024-including-data-localisation-requirements |
| WEB-16 | https://digitalpolicyalert.org/digest/dpa-digital-digest-ethiopia |
| WEB-17 | https://github.com/EthioNLP/Ethiopian-Language-Survey |
| WEB-18 | https://link.springer.com/article/10.1186/s40537-024-01044-y |
| WEB-19 | https://ethionlp.github.io/ |
| WEB-20 | https://aclanthology.org/2024.rail-1.13.pdf |
| WEB-21 | https://aclanthology.org/2024.lrec-main.561/ |
| WEB-22 | https://arxiv.org/abs/2403.13737 |
| WEB-23 | https://www.gsma.com/newsroom/press-release/ethiopias-digital-economy-to-contribute-etb-1-3-trillion-to-gdp-by-2028-unlocking-jobs-and-growth-through-telecom-and-policy-reforms/ |

---

