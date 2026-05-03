## Deployment Context

**Use case:** Amharic utility chatbots for Ethiopian Electric Utility and Addis Ababa Water handling prepaid meter top-ups, outage reports, and bill disputes
**Target population:** Urban households in Addis Ababa and regional capitals interacting with utility support over Telegram and SMS

# Validity Analysis: INJONGO
**Target context:** Urban Ethiopian Utility Chatbot Users — Amharic-Language Telegram/SMS
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 4 | Minor gaps | high |
| **Average** | **2.7** | | |

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

INJONGO is a serious, ground-up effort to build a culturally grounded African intent detection and slot-filling benchmark, and Amharic is one of its 17 supported languages. Dataset inspection confirms that the Amharic split contains genuine Ethiopian-grounded content: Telebirr appears as PAYMENT_COMPANY, Ethiopian banks (Amara, CBE) appear as BANK_NAME, Ethiopian regional cities and calendar months populate slot values, and Ethiopic script renders cleanly. However, for the specific deployment of an Amharic-language utility chatbot for EEU and AAWSA on Telegram/SMS, three high-priority dimensions (input ontology, input content, output ontology, output content) show substantive validity gaps. The 40-intent taxonomy lacks the deployment's primary use cases (prepaid meter top-up, STS token entry, outage report, load-shedding schedule). The 23-slot ontology lacks all deployment-critical slot types (METER_ID, UTILITY_ACCOUNT_NUMBER, STS_TOKEN, KEBELE). Code-switching — a confirmed high-priority deployment requirement — is absent from sampled Amharic data. Annotation was performed by pan-African crowdworkers without documented utility domain expertise, against a deployment requirement that ground truth be validated by EEU/AAWSA agents. Strongest dimensions are input form (text Ethiopic Unicode matches Telegram exactly) and output form (text intent+slots, standard metrics). The benchmark is best used as a fine-tuning starting point for general Amharic intent detection rather than a deployment-readiness evaluation for utility-specific tasks.

## Practical Guidance

### What This Benchmark Measures

INJONGO measures general-purpose Amharic intent detection (across banking, home, travel, kitchen & dining, and a generic utility domain) and slot-filling for 23 broad named-entity types. For the Ethiopian utility deployment, it can evaluate baseline Amharic NLU competence — whether a model recognizes Ethiopian banks, Telebirr, Ethiopian cities/calendar, formal polite Amharic register, and electricity/water bill_balance queries. Strongest dimensions are input form (Ethiopic Unicode in text matches Telegram deployment exactly) and output form (standard intent accuracy + slot F1 metrics).

### Construct Depth

Construct depth is shallow for the deployment task. The benchmark probes general conversational NLU with cultural grounding but does not probe the specific constructs the deployment requires: prepaid meter workflows, STS token recognition, outage reporting, load-shedding queries, kebele-level address resolution, or Amharic-English code-switched technical vocabulary. The benchmark's 80-per-intent uniform distribution does not reflect real EEU/AAWSA traffic skew, so even on the intents that exist, the evaluation does not measure performance under deployment-realistic frequencies. Annotation is by general native speakers, not utility domain experts, so slot-boundary correctness for utility billing terminology is not validated against the authoritative ground-truth standard.

### What Else You Need

Substantial supplementation is required. (1) Augment intent taxonomy with deployment-specific intents (input_ontology gap) using EEU/AAWSA conversation logs or expert-elicited examples. (2) Augment slot ontology with METER_ID, UTILITY_ACCOUNT_NUMBER, STS_TOKEN, KEBELE, WOREDA, sub-city types (output_ontology gap). (3) Collect or synthesize Amharic-English code-switched utterances for utility domain technical vocabulary (input_content gap), since INJONGO's monolingual Amharic data will overestimate deployment performance. (4) Re-annotate or validate utility-specific slot boundaries with EEU/AAWSA customer service agents (output_content gap). (5) Build a deployment-distribution test set reflecting real intent frequencies, not uniform 80-per-intent. (6) Verify Unicode normalization (NFC/NFD) compatibility between INJONGO release files and the production tokenizer pipeline.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
INJONGO includes a Utility domain explicitly selected as 'most suitable to African contexts' [Q39, Q117] and Amharic data does contain utility-adjacent bill_balance examples (D1, D8). However, for the Ethiopian deployment specifically, the dimension is HIGH priority and the gaps are concrete and severe: prepaid meter top-up, STS token entry, outage reporting, load-shedding schedule queries, and account/meter lookup intents are not represented in the 19-example Amharic sample (D20) and are not enumerated in the documented intent list. The paper itself acknowledges domains 'essential for real-world applications' are missing [Q107] and notes the fixed uniform distribution may not reflect real-world frequencies [Q111]. Additionally, the bill_balance intent conflates utility billing with cable TV, retail credit, and phone bills across language splits (D1 vs D22), introducing construct-irrelevant variance for an EEU/AAWSA-scoped deployment. The 40-intent ceiling is also flagged as a source of measurement noise [Q86].

**Strengths:**
- Utility is one of five named domains [Q5, Q39] and the bill_balance intent contains genuine electricity utility content in Amharic (D1: ለመብራት annotated as BILL_TYPE)
- Cross-lingual evidence confirms electricity and water billing intents are operationally populated (D17 Luganda, D18 Kinyarwanda), so the utility category is not a stub
- Ground-up African design rather than translated CLINC reduces baseline Western bias in category selection [Q39, Q101]

**Checklist:**

- **IO-1**: Required deployment categories include prepaid meter top-up, STS token entry, outage report, outage status query, load-shedding schedule, bill dispute, payment history, account/meter lookup, payment via Telebirr/CBE Birr, water complaints, and human-agent escalation (per elicitation and YAML deployment_required_intents).
- **IO-2**: Yes — confirmed omissions: no prepaid meter top-up, STS token, outage report, or load-shedding intents observed in 19 Amharic examples (D20) and not enumerated in documented intent list; paper explicitly notes 'healthcare and education' missing and 5/40 may miss real-world domains [Q107]. Flagged gap_id 1 in YAML resolved as NOT FOUND for utility-specific Ethiopian intents. — _Sources: Q107, DATASET-D20, WEB-11_
- **IO-3**: Yes, partially — domains like Kitchen & Dining, Home (alarm, calendar_update, music), Travel (book_flight: D5, D20), and non-utility billing (cable TV, retail credit cards in bill_balance D22, D21) are present in the 40-intent space but irrelevant to an EEU/AAWSA chatbot, consuming evaluation weight when averaged over the 40-intent label space [Q86]. — _Sources: Q39, Q86, DATASET-D22_
- **IO-4**: Content underrepresentation gap: deployment-critical utility intents absent. Construct-irrelevant variance gap: heterogeneous bill_balance scope and non-utility domains inflate label space without serving deployment. Distributional mismatch: uniform 80-per-intent distribution [Q56] does not reflect skewed real-world utility interaction frequencies [Q111]. — _Sources: Q107, Q111, Q86, DATASET-D20_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q39] 'we extracted 40 intents from five most suitable domains to the African contexts: Banking ... Home ... Kitchen and Dining ... Travel ... and Utility' (p.3)
- [Q107] 'The scope of INJONGO is constrained by its coverage of only 5 domains and 40 intents, missing some other domains such as healthcare and education that are essential for real-world applications.' (p.9)
- [Q111] 'the fixed distribution of examples across intents may not accurately reflect the natural frequency of these interactions in real-world conversations' (p.9)
- [Q86] 'the large label space (i.e. 40) for the classification task' (p.7)

*Web sources:*
- [WEB-11] INJONGO paper Appendix A.1 — full Utility intent label list not surfaced; gap_id 1 resolved NOT FOUND
- [WEB-22] Masakhane-NLU HuggingFace dataset — direct enumeration of utility intents requires dataset inspection

*Dataset analysis:*
- D1: bill_balance intent in Amharic with electricity-specific BILL_TYPE (ለመብራት) — utility-adjacent coverage exists
- D8: bill_balance Amharic example with utility expense (ፍጆታ) — closest deployment-relevant intent observed
- D20: 19 Amharic examples span 8 intents (bill_balance, alarm, balance, book_flight, cancel_reservation, calendar_update, car_rental, confirm_reservation) with no prepaid top-up, outage report, STS token, or load-shedding intents
- D22: Hausa bill_balance covers GOTV cable TV — confirms heterogeneity within bill_balance label across deployment-irrelevant domains

</details>

**Information gaps:**
- Full enumeration of the eight Utility-domain intent labels in INJONGO is not surfaced (gap_id 1)
- Full Amharic intent distribution beyond 19 sampled examples is unknown — utility-domain content density at scale is unquantified

**Requires expert verification:**
- EEU/AAWSA production intent frequency distribution to compare against INJONGO's uniform 80-per-intent design
- Whether INJONGO's documented utility intents (e.g., 'pay bill') map onto EEU prepaid top-up workflow conventions

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Mixed evidence with one decisive negative for this HIGH-priority dimension. INJONGO was designed with cultural grounding as an explicit principle [Q13, Q30, Q37], and dataset inspection confirms Ethiopian-specific entities in the Amharic split: Telebirr as PAYMENT_COMPANY (D4, D11), Ethiopian banks Amara Bank and CBE (D2, D3), Ethiopian cities Dire Dawa, Bahir Dar, Hawassa (D5, D12), and Ethiopian calendar months Hamle and Meskerem (D5, D6) — these resolve key gaps from web search positively. However, the deployment-critical requirement of Amharic-English code-switching is not represented: zero of 19 Amharic samples contain Latin-script tokens or English insertions (D24), and code-switching was not an explicit design criterion in the paper. The deployment elicitation marks code-switching as 'common and increasing' particularly for technical vocabulary (token, top-up, balance, meter), and a benchmark monolingual in Ethiopic script will overestimate performance on naturalistic deployment input. Additionally, regional dialectal variation (Oromo/Tigrinya substrate) is not addressed, and Amharic is acknowledged as systematically lower-resource than Swahili [Q88, Q89].

**Strengths:**
- Explicit cultural-grounding methodology, with native-speaker generation rather than translation [Q37, Q40, Q41]
- Telebirr confirmed as PAYMENT_COMPANY value in Amharic data (D4) — a high-priority deployment entity
- Ethiopian banks (Amara Bank, CBE) and Ethiopian regional cities (Dire Dawa, Bahir Dar, Hawassa) appear as slot values (D2, D3, D5, D12)
- Ethiopian calendar months (Hamle, Meskerem) appear as DATE values (D5, D6), reflecting authentic Amharic temporal expression
- Formal polite Amharic register present in samples (D29), matching deployment norms for formal service interaction

**Checklist:**

- **IC-1**: Yes — deployment requires Ethiopian-specific cultural/geographic knowledge (Ethiopian payment platforms, banks, kebele/sub-city addresses, Ethiopian calendar) and dialectal robustness (Amharic-English code-switching, possible Oromo/Tigrinya substrate). — _Sources: WEB-5_
- **IC-2**: Partially — Ethiopian financial entities (Telebirr D4, Amara Bank D2, CBE D3) and geography (D5, D12) are present, satisfying baseline cultural grounding [Q30]. However, code-switching is absent (D24) and regional dialectal variation is undocumented (gap_id 6 NOT FOUND). — _Sources: Q30, Q41, DATASET-D2, DATASET-D3, DATASET-D4, DATASET-D5, DATASET-D11, DATASET-D29_
- **IC-3**: Some Western residue persists (e.g., 'taco bell' in Hausa D22), though for the Amharic split the sampled instances appear consistently Ethiopia-grounded. Cross-lingual training data drawn from 'Combined INJONGO' [Q72, Q128] could expose models to non-Ethiopian entities. — _Sources: Q72_
- **IC-4**: INSUFFICIENT DOCUMENTATION — paper documents pan-African native-speaker recruitment via Kenya-based logistics [Q44]; whether Amharic annotators were Ethiopia-based or had urban Addis Ababa familiarity is not specified. Would need annotator location/demographic breakdown.
- **IC-5**: Major content issue: zero observed code-switching across 19 Amharic examples (D24) despite deployment confirming high code-switching frequency for English domain vocabulary. This represents a content distribution mismatch likely to harm external validity. Secondary issue: Amharic web-data resource asymmetry vs. higher-resource African languages may compound performance gaps [Q88, Q89]. — _Sources: Q88, Q89, DATASET-D24, WEB-9, WEB-12_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q13] 'two key challenges: (1) the translationese effect ... and (2) the creation of utterances that are less culturally relevant.' (p.1)
- [Q30] 'we ensured that the slot entities are more culturally relevant in the respective countries the languages are from' (p.2)
- [Q37] 'we provide each annotator with sample sentences from the CLINC dataset ... with a specified intent type' (p.3)
- [Q41] 'the annotator used the R200 as "money" with currency Rand (R), and more familiar South African banks such as "FNB" and "Absa"' (p.3)
- [Q88] 'The performance of some African languages is often higher than others, this is probably connected to the amount of monolingual data available on the web.' (p.7)
- [Q89] 'Swahili (swa) with over 1 billion monolingual data ... 80.6 accuracy point ... while other languages have much lower performance.' (p.7)

*Web sources:*
- [WEB-5] Telebirr 54.84M users, dominant Ethiopian utility payment channel — confirms deployment relevance of Telebirr coverage
- [WEB-9] INJONGO paper — code-switching not mentioned as design criterion (gap_id 2 NOT FOUND)
- [WEB-12] Code-switching NLP literature — no Amharic-English Ethiopian utility code-switching benchmark exists
- [WEB-3] McGill-NLP/Injongo GitHub — Amharic example አባይ ባንክ confirms Ethiopic rendering

*Dataset analysis:*
- D2: Amara Bank confirmed as BANK_NAME — Ethiopian financial entity
- D3: ንግድ ባንክ (Commercial Bank of Ethiopia) as BANK_NAME — major Ethiopian bank
- D4: ቴሌብር (Telebirr) as PAYMENT_COMPANY in Amharic — resolves a flagged YAML gap positively
- D5: Dire Dawa and Bahir Dar as CITY_OR_PROVINCE; Meskerem as Ethiopian-calendar DATE
- D6: Hamle (Ethiopian calendar) as DATE
- D11: Telebirr also confirmed in eng config Amharic-source utterance
- D24: Zero code-switched utterances in 19 Amharic samples — confirmed gap on HIGH-priority requirement
- D29: Formal polite Amharic register (ሊነግሩኝ ይችላሉ) consistent with deployment norms

</details>

**Information gaps:**
- Frequency of Telebirr/CBE Birr appearances at full-corpus scale (sample shows present but not density)
- Regional dialectal variation in Amharic split (gap_id 6 NOT FOUND) — Addis Ababa vs Dire Dawa/Hawassa/Mekelle representation
- Whether any utility-specific Amharic content beyond bill_balance exists in unsampled portions of the 2,240 train examples
- Code-switching density across full Amharic split — sample of 19 may understate

**Requires expert verification:**
- Whether sampled Amharic register and lexical choices reflect EEU/AAWSA customer service interactions specifically
- Whether informal Addis Ababa neighborhood naming (Bole, Piassa, Megenagna) appears in PLACE_NAME slots in unsampled data

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Strongest overall match. INJONGO is text-only [Q43] aligning with Telegram/SMS deployment, and dataset inspection confirms Ethiopic Unicode renders correctly without artifacts in all 19 sampled Amharic examples (D29, D5). Annotation occurred on LabelStudio in native script [Q43]. Mixed Ethiopic/Arabic numeral usage is observed incidentally (D27), reflecting a pattern relevant to deployment without being formally designed. Two minor concerns moderate the score: (a) Unicode normalization form (NFC/NFD) is undocumented (gap_id 5 NOT FOUND), which could cause tokenizer mismatches in deployment, and (b) eng config exhibits transliteration degradation (D10: 'Dashen' → 'dasion'), which affects translate-test cross-lingual evaluation but not the primary in-language Amharic deployment path. SMS-specific signal degradation is not addressed in documentation, but per elicitation Telegram is the dominant primary channel and the deployment explicitly excludes romanized fallback (Q4 elicitation).

**Strengths:**
- Text-only modality matches Telegram/SMS deployment exactly [Q43]
- Ethiopic script renders correctly in all 19 sampled Amharic examples without encoding artifacts (D29, D5)
- Native-script annotation on LabelStudio [Q43]
- Incidental coverage of mixed Ethiopic/Arabic numerals (D27) reflects realistic input pattern
- License (CC BY 4.0 [Q23]) permits adaptation for production fine-tuning

**Checklist:**

- **IF-1**: Signal distribution match is good for primary channel: text in Ethiopic Unicode confirmed (D29). SMS-specific degradation (encoding loss, length truncation) is not represented in benchmark, but deployment scopes SMS as secondary and full Ethiopic as required (elicitation Q4). — _Sources: Q43, DATASET-D29, DATASET-D5_
- **IF-2**: Yes — Telegram and Ethio Telecom infrastructure support Ethiopic Unicode reliably; 4G coverage exceeds 80% in primary deployment cities [WEB-6, WEB-8]; Telegram transmits Ethiopic reliably (YAML). — _Sources: WEB-6, WEB-8, WEB-3_
- **IF-3**: Numeral mixing observed (D27); Unicode normalization undocumented (gap_id 5); SMS Ethiopic transmission reliability may vary by carrier — not benchmarked. eng-config translate-test path shows transliteration noise (D10) that would affect cross-lingual transfer evaluation but not in-language deployment. — _Sources: DATASET-D27, DATASET-D10_
- **IF-4**: Minor form gaps: (a) NFC/NFD normalization unspecified — could cause tokenizer subword mismatch; (b) no SMS-degraded variants tested; (c) romanized Amharic explicitly excluded from deployment scope so absence is acceptable. — _Sources: DATASET-D24_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q43] 'The annotation followed the named entity recognition setup on LabelStudio platform.' (p.4)
- [Q23] 'Dataset is released under CC BY 4.0 license.' (p.2)
- [Q129] 'All experiments are conducted using full precision (FP32) on NVIDIA H100/L40S GPUs' (p.14)
- [Q138] 'The prompts are language-specific and tailored to the task requirements.' (p.15)

*Web sources:*
- [WEB-3] McGill-NLP/Injongo GitHub — Amharic example አባይ ባንክ confirms Ethiopic rendering at release
- [WEB-6] Mordor Intelligence — Ethiopia 4G coverage >80% in urban hubs supports text channel viability
- [WEB-8] Ethio Telecom FY2024/25 — 1,683 new mobile sites, 512 cities with 4G

*Dataset analysis:*
- D29: Complex Ethiopic characters render without artifacts — encoding fidelity confirmed
- D5: Ethiopian place names and calendar month rendered correctly in Ethiopic
- D27: Arabic numeral '3' embedded in Ethiopic DATE span — confirms numeral mixing pattern at small scale
- D24: All 19 Amharic examples in pure Ethiopic script — no Latin-script tokens
- D10: eng config transliteration degradation (Dashen → dasion) — affects translate-test path

</details>

**Information gaps:**
- Unicode normalization form (NFC/NFD) of release files (gap_id 5 NOT FOUND)
- Whether SMS channel Ethiopic delivery reliability has been measured by EEU/AAWSA
- Byte-offset vs character-offset behavior for span annotations in Ethiopic UTF-8 (dataset analysis Limitation 5)

**Requires expert verification:**
- Whether tokenizers used in deployment match the byte-level normalization of INJONGO release files

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
MODERATE-priority dimension with concrete structural gaps. The 23-slot ontology was rigorously developed with merge consolidation [Q54, Q55, Q119] and includes deployment-relevant types (BANK_NAME, PAYMENT_COMPANY, BILL_TYPE, MONEY, ACCOUNT_TYPE, CITY_OR_PROVINCE, PLACE_NAME, DATE, TIME). However, the dimension fails on critical deployment requirements: dataset inspection confirms (D19) that no METER_ID, UTILITY_ACCOUNT_NUMBER, STS_TOKEN, KEBELE, WOREDA, or sub-city slot types exist in any of 19 Amharic examples, and these are core to EEU prepaid top-up and AAWSA billing workflows. Nine 'infrequent slots' were eliminated [Q52] without documented utility-deployment justification. Cross-lingual annotation choices show ontological ambiguity: SNEL (DRC electricity utility) is annotated as PAYMENT_COMPANY (D28), conflating utility provider with payment channel — relevant if EEU/AAWSA appear similarly. The deployment elicitation flags this as MODERATE priority because BANK_NAME/PAYMENT_COMPANY/BILL_TYPE provide partial coverage, but the missing types are non-negotiable for the core workflow.

**Strengths:**
- 23 slot types include deployment-relevant categories: BANK_NAME, PAYMENT_COMPANY, BILL_TYPE, MONEY, ACCOUNT_TYPE, CITY_OR_PROVINCE, PLACE_NAME, DATE, TIME, NUMBER [Q144]
- Telebirr fits PAYMENT_COMPANY (D4) and BILL_TYPE accommodates electricity (D1) — partial coverage of deployment slot space
- Annotation guide provides explicit disambiguation rules (e.g., temporal: <1 day → TIME; ≥1 day → DATE [Q153, Q154]; bank name excludes 'bank' unless attached [Q152])
- Slot consolidation 34→23 was driven by frequency analysis [Q51, Q119], reducing label noise

**Checklist:**

- **OO-1**: Deployment-relevant present categories: BANK_NAME, PAYMENT_COMPANY, BILL_TYPE, MONEY, ACCOUNT_TYPE, CITY_OR_PROVINCE, PLACE_NAME, DATE, TIME, NUMBER [Q144]. — _Sources: Q144, DATASET-D2, DATASET-D4_
- **OO-2**: Confirmed missing for Ethiopian utility deployment (D19): METER_ID, UTILITY_ACCOUNT_NUMBER, STS_TOKEN (20-digit prepaid token), KEBELE, WOREDA, sub-city, NEIGHBORHOOD_NAME (informal Addis Ababa toponyms). The annotation guide requires explicit named entities for PLACE_NAME [Q156], so informal kebele/neighborhood references may not even fit existing types cleanly. — _Sources: DATASET-D19, Q156_
- **OO-3**: Some category encodings reflect non-Ethiopian assumptions: PAYMENT_COMPANY conflated with utility provider (D28: SNEL); SHOPPING_ITEM, MUSIC_GENRE, ARTIST_NAME, DISH_OR_FOOD, MEAL_PERIOD relevant only to non-utility domains. Nine slots (NATIONALITY through PLUG TYPE) were eliminated [Q52] — without justification of trade-off against utility-specific slots. — _Sources: Q52, DATASET-D28_
- **OO-4**: Stakeholder-driven taxonomy redesign is required. EEU customer service agents and AAWSA billing staff should define slot schemas for METER_ID format, account-number format, kebele granularity, and STS token recognition.
- **OO-5**: Structural validity issue: deployment-critical decision boundaries (meter ID extraction, STS token recognition, kebele resolution) cannot be expressed in the 23-slot taxonomy, so benchmark performance does not reflect deployment task structure. Content validity issue: 9 missing slot types are deployment-critical. — _Sources: Q55, DATASET-D19_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q144] '# Named Entities Types to Identify ACCOUNT_TYPE, ARTIST_NAME, BANK_NAME, BILL_TYPE, CALENDAR_EVENT, CITY_OR_PROVINCE, COUNTRY, CURRENCY, DATE, DISH_OR_FOOD, HOTEL_NAME, LANGUAGE_NAME, MEAL_PERIOD, MONEY, MUSIC_GENRE, NUMBER, PAYMENT_COMPANY, PERSONAL_NAME, PLACE_NAME, RESTAURANT_NAME, SHOPPING_ITEM, SONG_NAME, TIME' (p.19)
- [Q52] 'Consequently, nine infrequent slots from NATIONALITY through PLUG TYPE were eliminated.' (p.4)
- [Q55] 'This merging process resulted in a reduction from 34 to 23 slot types.' (p.5)
- [Q156] 'With this entity, only annotate if entity is named explicitly, e.g Name of airport, museum or mall is not and nt just "mall", "airport" etc' (p.24)

*Web sources:*
- [WEB-11] gap_id 4 — no Ethiopian utility-specific NLP slot extraction literature exists; gap is documentation-confirmed

*Dataset analysis:*
- D19: All 19 Amharic examples confirmed absent of METER_ID, UTILITY_ACCOUNT_NUMBER, KEBELE, STS_TOKEN spans
- D2, D3: BANK_NAME accommodates Ethiopian banks — partial alignment
- D4: PAYMENT_COMPANY accommodates Telebirr — partial alignment
- D28: SNEL (DRC utility provider) annotated as PAYMENT_COMPANY — ontological conflation between utility provider and payment channel

</details>

**Information gaps:**
- EEU and AAWSA's actual slot schemas for meter IDs, account numbers, and addresses (not in public sources)
- Whether any pre-merge slot types (among the dropped 9) would have been useful for utility deployment

**Requires expert verification:**
- EEU billing system's canonical slot taxonomy and how informal Amharic place references should be normalized
- AAWSA's account-number and address conventions

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
HIGH-priority dimension with substantial concerns. INJONGO followed a rigorous quality control process (three annotators per utterance [Q42, Q45], two review rounds [Q109], post-review Kappa 0.912–1.00 [Q48]). However, for the Ethiopian utility deployment specifically: (1) Ground-truth authority mismatch — annotators were recruited via a Kenya-based logistics company at per-country rates [Q44], and there is no documentation that Amharic annotators had EEU/AAWSA utility billing domain expertise (gap_id 3 NOT FOUND); the deployment elicitation explicitly requires utility agent validation. (2) Annotation quality issues observable in samples — D15 and D16 show Amharic utterances with clearly extractable DATE, TIME, and CALENDAR_EVENT entities but empty span annotations; D13 (Oromo) and D21 (Sesotho) show similar omissions. (3) Amharic-specific Fleiss Kappa not surfaced (gap_id 7 NOT FOUND), so where Amharic falls in the 0.618–0.934 pre-review range is unknown. (4) Pre-to-post improvements were largest in Sesotho and Zulu [Q49], suggesting language-specific quality variation that is not transparent for Amharic.

**Strengths:**
- Three-annotator majority-vote QC with two-round review [Q42, Q45, Q109]
- Post-review Fleiss Kappa 0.912–1.00 across all languages [Q48]
- Detailed annotation guide with explicit disambiguation rules [Q149, Q152, Q153, Q154, Q155]
- Native-speaker annotators across all languages [Q7]
- Per-country remuneration via professional logistics company [Q44]

**Checklist:**

- **OC-1**: No — ground truth was set by pan-African native-speaker crowdworkers, not by EEU/AAWSA customer service agents as the deployment requires. The deployment elicitation explicitly states utility agent/billing staff judgment determines correctness. — _Sources: Q44_
- **OC-2**: Likely substantial for utility-specific spans (BILL_TYPE boundaries, place-name resolution to kebele/sub-city). D7 ('የቦሎ ማሳደሻ' annotated as BILL_TYPE) — whether this matches EEU/AAWSA categorization cannot be confirmed without domain-expert review. Cultural conventions around formal Amharic register also vary by service institution. — _Sources: DATASET-D7_
- **OC-3**: Demographics partially documented: native speakers via Kenya-based logistics company [Q44]; per-language counts and Ethiopia-specific recruitment unspecified (NOT FOUND in YAML benchmark_amharic_split_details). No domain-expertise requirement documented. — _Sources: Q7, Q44, WEB-9_
- **OC-4**: Re-annotation by EEU and AAWSA staff (or supervised review) is needed for any utility-specific slot labels before deployment use. The deployment explicitly requires this.
- **OC-5**: Aggregation method is majority vote with review [Q45]; minority-perspective erasure risk is moderate, particularly for ambiguous slot types where annotators disagreed [Q53]. Reviewer identity and resolution rules are not detailed. — _Sources: Q45, Q53_
- **OC-6**: Convergent validity concern: Amharic ground-truth labels may not correlate with EEU/AAWSA agent judgments. External validity concern: under-annotation observed in samples (D15, D16) reduces reliability of slot-filling F1 as a deployment-readiness signal. — _Sources: DATASET-D15, DATASET-D16, DATASET-D13, DATASET-D21_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q42] 'Each utterance was annotated by three annotators so that we could check for agreement in the slot annotations.' (p.4)
- [Q44] 'all recruited participants received an appropriate remuneration based on the per-country rate decided by our logistics company in Kenya.' (p.4)
- [Q45] 'we follow a rigorous quality control process using a majority voting system with a minimum of three annotators per sentence' (p.4)
- [Q47] 'Initial Fleiss\' Kappa scores revealed substantial variation across languages, ranging from 0.618 (Zulu) to 0.934 (Shona)' (p.4)
- [Q48] 'Following the review process, agreement scores improved markedly across all languages, reaching 0.912-1.00.' (p.4)
- [Q53] 'ambiguous slot types significantly impacted annotation quality and introduced unnecessary complexity.' (p.4)
- [Q109] 'requiring two rounds of review to achieve consistent quality.' (p.9)

*Web sources:*
- [WEB-9] INJONGO paper — gap_id 3 NOT FOUND on Amharic annotator domain expertise; gap_id 7 NOT FOUND on Amharic-specific Kappa

*Dataset analysis:*
- D15: Amharic alarm utterance with empty spans despite identifiable DATE (ነገ) and TIME (12 ሰአት) — annotation under-coverage
- D16: Amharic calendar_update with empty spans despite CALENDAR_EVENT content
- D13: Oromo book_flight with three identifiable city names but empty spans
- D21: Sesotho bill_balance with empty spans despite BILL_TYPE/SHOPPING_ITEM candidate
- D7: Amharic BILL_TYPE 'የቦሎ ማሳደሻ' (Bole road expansion) — labeled by general native speaker; domain-expert validation status unknown

</details>

**Information gaps:**
- Amharic-specific pre- and post-review Fleiss Kappa values (gap_id 7)
- Per-language annotator counts and locations for Amharic (NOT FOUND)
- Whether reviewers had domain expertise in any specific industry

**Requires expert verification:**
- Whether EEU/AAWSA agents agree with sampled BILL_TYPE boundary decisions in Amharic data
- Whether under-annotated examples (D15, D16) are isolated or systematic across the full Amharic split

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
LOWER-priority dimension with strong alignment. Both benchmark and deployment use structured text output (intent label + slot extraction) with standard text representation. Intent detection is scored by accuracy and slot-filling by F1 [Q84], and the structured `$$`-separated extraction format [Q146] is a reasonable text representation that maps to programmatic parsing. Models are instructed to return `$$` only when no entities are found [Q145], handling the empty-output case explicitly. Five seeds for fine-tuning [Q63] and five prompt templates for LLM eval [Q73] provide robustness. The output modality is text-only, matching deployment exactly. Minor concerns: the `$$` separator is benchmark-specific syntax that requires post-processing in production, and the text-string output form can complicate confidence-score extraction useful for chatbot dialogue management. F1 metric is appropriate for span extraction.

**Strengths:**
- Intent accuracy and slot F1 are standard, well-understood metrics [Q84]
- Five-seed averaging for fine-tuning and five-template averaging for LLMs reduce evaluation variance [Q63, Q73]
- Structured output format with explicit empty-case handling [Q145, Q146]
- Text-only modality matches Telegram/SMS deployment exactly
- Both fine-tuning and prompting paradigms evaluated [Q61, Q65], allowing the user to choose deployment-appropriate models

**Checklist:**

- **OF-1**: Yes — text output for intent + slots matches Telegram/SMS chatbot needs. No speech, image, or open-ended generation required. — _Sources: Q84_
- **OF-2**: N/A — TTS not required; deployment is text-based.
- **OF-3**: Adult literacy in Addis Ababa is high (male ~93.6%, female ~80% per 2005 baseline [WEB-2, WEB-4]) — text-based interaction is feasible for the target population. Telegram dominance and 4G coverage >80% [WEB-6] support text channel. — _Sources: WEB-2, WEB-4, WEB-6_
- **OF-4**: Minor: `$$`-separated string output [Q146] requires production-side parsing logic; no probabilistic confidence scores in benchmark output schema, which is sub-optimal for dialogue-management uncertainty handling but does not invalidate evaluation. — _Sources: Q146, Q145_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q84] 'Evaluation is based on accuracy and F1-score for ID and SF tasks. Average computed on five templates, and on only African languages.' (p.7)
- [Q145] 'unstated entities should not be included in the response if no entities are found, return `$$` only.' (p.19)
- [Q146] 'Sentence: John went to Paris and paid 100 dollars at an Awater restaurant. Output: PERSONAL_NAME John $$ CITY_OR_PROVINCE Paris $$ MONEY 100 $$ RESTAURANT_NAME Awater' (p.19)
- [Q63] 'All results are averaged over five seeds.' (p.5)
- [Q73] 'The evaluations of LLMs use 5 different prompting templates and a temperature of 0.5.' (p.6)

*Web sources:*
- [WEB-2] Addis Ababa adult literacy >93% male, ~80% female — text-based interaction feasible
- [WEB-4] Wikipedia Demographics of Addis Ababa corroborates literacy figures
- [WEB-6] 4G coverage >80% in primary deployment cities — text channel infrastructure available

</details>

**Information gaps:**
- Whether F1 with macro vs micro averaging is reported by slot type or language
- Whether confidence scores can be extracted from fine-tuned models for production uncertainty handling

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** Deployment-critical utility intents (prepaid meter top-up, STS token entry, outage report, load-shedding schedule query, account/meter lookup) are absent from the documented 40-intent taxonomy.

**Recommendation:** Define an extended intent set with EEU and AAWSA customer service leads; collect 80–200 seed utterances per new intent in Amharic via supervised elicitation from Ethiopian native speakers familiar with the utility workflow; concatenate to INJONGO Amharic data for fine-tuning.

### Input Ontology ⚠

**Gap:** Uniform 80-per-intent distribution does not reflect real EEU/AAWSA traffic skew (likely heavily weighted toward top-up and outage queries).

**Recommendation:** Build a frequency-weighted evaluation set sampled in proportion to observed EEU/AAWSA chatbot or call-center intent distribution; report per-intent metrics alongside macro-averaged accuracy to surface deployment-relevant performance.

### Output Ontology ⚠

**Gap:** 23-slot ontology lacks METER_ID, UTILITY_ACCOUNT_NUMBER, STS_TOKEN, KEBELE, WOREDA, sub-city, and NEIGHBORHOOD_NAME types — confirmed absent in dataset (D19).

**Recommendation:** Co-design an extended slot schema with EEU and AAWSA billing staff; add at minimum METER_ID, UTILITY_ACCOUNT_NUMBER, STS_TOKEN, and KEBELE; re-annotate the existing Amharic split or annotate a deployment-specific augmentation under the extended schema.

### Input Content ⚠

**Gap:** Zero observed Amharic-English code-switched utterances in sampled INJONGO Amharic, despite code-switching being a confirmed high-priority deployment pattern especially for technical vocabulary (token, top-up, balance, meter).

**Recommendation:** Augment training data with code-switched Amharic-English variants, ideally elicited from younger urban Telegram users; ensure technical English domain vocabulary appears in mixed-script form; evaluate a held-out code-switched test split separately from monolingual.

### Output Content ⚠

**Gap:** Annotators were pan-African native-speaker crowdworkers with no documented utility domain expertise; deployment requires EEU/AAWSA agent validation as ground-truth authority.

**Recommendation:** Have EEU and AAWSA customer service agents re-validate a stratified sample of the Amharic test split's utility-relevant labels; resolve discrepancies; retain only utility-domain examples whose labels match agent judgment for deployment-readiness evaluation.

### Input Form

**Gap:** Unicode normalization form (NFC vs NFD) of INJONGO Amharic release is undocumented, which can cause tokenizer subword mismatch in production.

**Recommendation:** Audit the parquet files for Unicode normalization, normalize to a single form (NFC recommended for Ethiopic), and verify tokenizer behavior on Telegram-sourced production input matches the normalized training data.

## Evidence Registries

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
| Q8 | 1 | output_form | "Through extensive experiments, we benchmark the fine-tuning multilingual transformer models and the prompting large language models (LLMs), and show the advantage of leveraging African-cultural utterances over Western-centric utterances for improving cross-lingual transfer from the English language." |
| Q9 | 1 | output_form | "Experimental results reveal that current LLMs struggle with the slot-filling task, with GPT-4o achieving an average performance of 26% F1-score." |
| Q10 | 1 | output_form | "In contrast, intent detection performance is notably better, with an average accuracy of 70.6%, though it still falls behind the fine-tuning baselines." |
| Q11 | 1 | output_form | "When compared to the English language, GPT-4o and fine-tuning baselines perform similarly on intent detection, achieving an accuracy of approximately 81%." |
| Q12 | 1 | input_ontology | "current large-scale benchmarks for these tasks often exclude evaluations of low-resource languages and rely on translations from English benchmarks, thereby predominantly reflecting Western-centric concepts." |
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
| Q26 | 2 | input_ontology | "Most of the existing benchmarks for intent detection and slot-filling tasks are English-only." |
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
| Q40 | 3 | input_content | "A Xhosa annotator was asked to generate another utterance belonging to the same intent type but capturing the South African context where the language is spoken." |
| Q41 | 3 | input_content | "Thus, the annotator used the R200 as "money" with currency Rand (R), and more familiar South African banks such as "FNB" and "Absa" for "bank name" slot." |
| Q42 | 4 | output_content | "Each utterance was annotated by three annotators so that we could check for agreement in the slot annotations." |
| Q43 | 4 | input_form | "The annotation followed the named entity recognition setup on LabelStudio platform." |
| Q44 | 4 | output_content | "For both utterance elicitation and slot-filling annotation, all recruited participants received an appropriate remuneration based on the per-country rate decided by our logistics company in Kenya." |
| Q45 | 4 | output_content | "To ensure annotation quality and consistency, we follow a rigorous quality control process using a majority voting system with a minimum of three annotators per sentence to resolve disagreements." |
| Q46 | 4 | output_content | "The annotation quality was evaluated using Fleiss' Kappa score (Fleiss, 1971), with scores presented in Table 3 comparing agreement levels before and after the review process." |
| Q47 | 4 | output_content | "Initial Fleiss' Kappa scores revealed substantial variation across languages, ranging from 0.618 (Zulu) to 0.934 (Shona), indicating significant inter-annotator disagreement." |
| Q48 | 4 | output_content | "Following the review process, agreement scores improved markedly across all languages, reaching 0.912-1.00." |
| Q49 | 4 | output_content | "Notable improvements were observed in Sesotho (+0.327) and Zulu (+0.294), with other languages showing average improvements of approximately 0.1 in their Fless' Kappa scores." |
| Q50 | 4 | input_form | "We performed an analysis of entity frequency distribution across all languages." |
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
| Q75 | 6 | input_form | "We leveraged the NLLB-200-3.3B (NLLB Team et al., 2022) machine translation model for the Translate-test setting." |
| Q76 | 6 | output_form | "Experiments of the baselines and cross-lingual transfer runs make use of five fixed random seeds." |
| Q77 | 6 | output_form | "Table 5 summarizes the results of the multilingual encoders fine-tuned INJONGO dataset." |
| Q78 | 6 | output_form | "Overall, AfroXLMR-76L achieves the best performance on both ID-SF tasks, with an average accuracy of 93.7% and an F1 score of 85.6%, respectively." |
| Q79 | 6 | output_content | "We attribute the success of this model to the coverage of all languages in INJONGO during its pre-training (see Appendix Table 11)." |
| Q80 | 6 | output_form | "AfroXLMR, the earlier version of AfroXLMR-76L, follows closely with an average accuracy of 92.2% and an F1 score of 85.2%." |
| Q81 | 6 | output_form | "However, this model was not pre-trained on some of the languages such as ewe, twi, lin, and wol leading to a significant drop in performance of −5.8, −4.8, −1.3, −0.4 for intent detection when compared to AfroXLMR-76L." |
| Q82 | 6 | output_form | "This shows that multilingual encoders for African languages can significantly improve the performance over massively multilingual encoders covering more than 100 languages such as XLM-R and NLLB LLM2Vec." |
| Q83 | 7 | output_form | "Table 6 shows the zero-shot LLM evaluation of five open models and two closed models." |
| Q84 | 7 | output_form | "Evaluation is based on accuracy and F1-score for ID and SF tasks. Average computed on five templates, and on only African languages." |
| Q85 | 7 | output_form | "Slot-filling task is difficult for all LLMs including on English The highest average performance achieved by the LLMs is 33.3% for GPT-4o, although much better than the open model at 28.8. We attribute this to the difficulty of LLMs on the named entity recognition task as reported by other researchers (Yu et al., 2023; Ojo et al., 2023). In comparison to the best-finetuned model, there is a large drop in performance of −53.2. This shows that having training data is still relevant for this task even in the LLM era, especially for low-resource languages." |
| Q86 | 7 | output_ontology | "For intent detection, we find that all open models achieved below 50% on the relatively easy task of intent detection. The poor performance may be attributed to either a lack of exposure to many African languages or the large label space (i.e. 40) for the classification task." |
| Q87 | 7 | output_form | "The closed models result are better, with GPT-4o and Gemini 1.5 Pro achieving more than +20 points than the best open model, Llama 3.3 70B. However, if we compare the results in the English language, open models such as Gemma 2 27B and Llama 3.3 70B are competitive with closed models. This shows that open models are more biased toward high-resource languages." |
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
| Q120 | 13 | input_content | "Table 8: Statistics of the INJONGO dataset across 17 languages, including corpus statistics (token counts and distributions) and slot entity analysis (entity counts, averages, and inter-annotator agreement measures) with unmerged slot types." |
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

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.macrotrends.net/global-metrics/cities/20921/addis-ababa/population |
| WEB-2 | https://worldpopulationreview.com/cities/ethiopia/addis-ababa |
| WEB-3 | https://github.com/McGill-NLP/Injongo |
| WEB-4 | https://en.wikipedia.org/wiki/Addis_Ababa |
| WEB-5 | https://techafricanews.com/2025/07/25/ethio-telecom-achieves-83-2m-subscribers-and-73-revenue-surge-as-lead-strategy-concludes/ |
| WEB-6 | https://www.mordorintelligence.com/industry-reports/ethiopia-telecom-mno-market |
| WEB-7 | https://www.addisinsight.net/2025/02/12/telebirr-hits-51-5-million-users-facilitating-1-03-trillion-etb-in-transactions/ |
| WEB-8 | https://addisinsight.net/2025/07/24/ethio-telecom-reports-162-billion-birr-revenue-and-4-9-trillion-birr-in-telebirr-transfers-in-2017-fiscal-year/ |
| WEB-9 | https://arxiv.org/abs/2502.09814 |
| WEB-10 | https://aclanthology.org/2025.acl-long.464/ |
| WEB-11 | https://arxiv.org/pdf/2502.09814 |
| WEB-12 | https://github.com/gentaiscool/code-switching-papers |
| WEB-13 | https://cipit.org/ethiopias-personal-data-protection-proclamation-of-2024-and-its-budding-digital-identity-regime/ |
| WEB-14 | https://www.techhiveadvisory.africa/insights/review-of-ethiopias-data-protection-act |
| WEB-15 | https://regulations.ai/regulations/RAI-ET-NA-PDPPNXX-2024 |
| WEB-16 | https://assets.bii.co.uk/wp-content/uploads/2024/10/09105903/BII-Impact-of-investment-in-the-Ethiopian-telecoms-market_2024.pdf |
| WEB-17 | https://arxiv.org/html/2411.14343v1 |
| WEB-18 | https://arxiv.org/pdf/2403.13737 |
| WEB-19 | https://aclanthology.org/2024.findings-emnlp.25/ |
| WEB-20 | https://github.com/topics/amharic-nlp |
| WEB-21 | https://www.huawei.com/en/media-center/transform/10/frehiwot-tamru |
| WEB-22 | https://huggingface.co/datasets/masakhane/injongo |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** masakhane/InjongoIntent (config: amh primary; configs eng, ewe, hau, ibo, kin, lin, lug, orm, sna, sot, swa, twi, wol, xho, yor, zul reviewed for cross-language comparison)
**Analysis date:** 2025-07-28
**Examples reviewed:** 232 total across 17 language configs (19 amh train, 13 eng train, and 11–27 examples per remaining 15 configs)
**Columns shown:** intent, text, spans, target, example_id; eng config additionally has `raw`
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | amh | train-00000044 | bill_balance | "በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" — BILL_TYPE: ለመብራት | "How much do I need to pay for electricity per month?" — electricity utility bill query in Amharic | IO, IC |
| D2 | amh | train-00000016 | balance | "የአማራ ባንክ አካውንቴ ስንት አለው" — BANK_NAME: አማራ ባንክ | "How much is in my Amara Bank account?" — Ethiopian bank (Amara Bank) named as BANK_NAME slot | IC, OO |
| D3 | amh | train-00000018 | balance | "ንግድ ባንክ ላይ የቀረኝ ገንዘብ አለ" — BANK_NAME: ንግድ ባንክ | "Is there money remaining at Commercial Bank?" — CBE (Commercial Bank of Ethiopia) named | IC, OO |
| D4 | amh | train-00000003 | balance | "በቴሌብር የብድር አካውንቴ ላይ አሁን ያለብኝ ቀሪ ሂሳብ ምን ያህል ነው።" — PAYMENT_COMPANY: ቴሌብር | "What is the remaining balance on my Telebirr loan account?" — Telebirr named as PAYMENT_COMPANY | IC, OO |
| D5 | amh | train-00000042 | book_flight | "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ።" — CITY_OR_PROVINCE: ድሬዳዋ, ባህርዳር | "Book me a flight from Dire Dawa to Bahir Dar for the fifth of Meskerem." — Ethiopian cities and Ethiopian calendar month | IC, OO |
| D6 | amh | train-00000011 | car_rental | "ከሃምሌ 4 እስከ 6 የቤት መኪና ኪራይ ማግኘት እችላለሁ?" — DATE: ከሃምሌ 4 እስከ 6 | "Can I get a home car rental from Hamle 4 to 6?" — Ethiopian calendar month (Hamle) used for DATE slot | IC, IF |
| D7 | amh | train-00000051 | bill_balance | "የቦሎ ማሳደሻ ስንት ነው መክፈል የሚኖርብኝ?" — BILL_TYPE: የቦሎ ማሳደሻ | "How much do I need to pay for Bole road expansion?" — bill query referencing Bole (Addis Ababa neighborhood) | IC, IO |
| D8 | amh | train-00000052 | bill_balance | "የዚህ ወር መከፈል ያለባቸውን የፍጆታ ዝርዝር አሳየኝ።" — DATE: የዚህ ወር | "Show me the list of utility expenses to be paid this month." — direct utility bill balance query | IO |
| D9 | amh | train-00000031 | confirm_reservation | "በቶቶት ለቃለአብ ቦታ ማስያዝ እንዳለብኝ መሞከር እና ማረጋገጥ እፈልጋለሁ" — RESTAURANT_NAME: ቶቶት, PERSONAL_NAME: ቃለአብ | "I want to try and confirm that I should book a spot at Totot for Kaleab." — Ethiopian restaurant and personal name | IC |
| D10 | eng | train-00000045 | balance | raw: "እባካችሁ የዳሽን ባንክ ሂሳቤን ታረጋግጡልኛላችሁ?" text: "can you please check my dasion bank account" — BANK_NAME: dasion bank | Original Amharic cites Dashen Bank; English translation renders "dasion" (spelling error) — shows transliteration degradation in eng config | IC, IF |
| D11 | eng | train-00000092 | spending_history | raw: "ከቴሌ ብር አካዉንቴ ገንዘብ ለማን ለማን እንደላኩ ዝርዝሩን አሳየኝ?" text: "Show me history of my telebirr transfers?" — PAYMENT_COMPANY: telebirr | Telebirr confirmed in Amharic source utterance as code-switched reference; PAYMENT_COMPANY slot correctly labeled | IC, OO |
| D12 | eng | train-00000053 | travel_suggestion | raw: "ለቀጣይ የጉብኝት ጉዞዬ በሃዋሳ እና በአርባ ምንጭ መካከል እንድመርጥ…" text: "help me decide between Hawassa and Arbaminch…" — CITY_OR_PROVINCE: Hawassa, Arbaminch | Ethiopian regional cities (Hawassa, Arba Minch) correctly identified in travel context | IC |
| D13 | orm | train-00000041 | book_flight | "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" — no spans | Oromo: "Book me a flight from Dire Dawa to Bole then to Jimma on Ethiopian Airlines" — Bole airport and Dire Dawa named, spans incorrectly empty | IC, OC |
| D14 | orm | train-00000044 | bill_balance | "Yeroo darbe tajaajila humna ibsaa meeqan kanfale naaf himi mee" — BILL_TYPE: tajaajila humna ibsaa | Oromo: "Tell me how much I paid for electricity service last time" — electricity bill query paralleling Ethiopian utility context | IO |
| D15 | amh | train-00000045 | alarm | "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ በደንብ እንዲሰማኝ ድምጽ ጨምርበት" — spans: [] | "Increase the volume of the alarm I set for 12 o'clock tomorrow morning so I can hear it well." — TIME and DATE slots present in text but no spans annotated | OC |
| D16 | amh | train-00000035 | calendar_update | "የእናቴን እና የአባቴን የልደት ቀን የቀን መቁጠሪያዬ ላይ ስላቀያየርኩት አስተካክለው" — spans: [] | "Fix it because I changed my mother's and father's birthday on my calendar." — CALENDAR_EVENT-like content but no spans annotated | OC |
| D17 | lug | train-00000044 | bill_balance | "Obukuumi n'amasannyalaze nteekeddwa kubisasula ddi?" — BILL_TYPE: Obukuumi, amasannyalaze | Luganda: "When do I need to pay the water and electricity bills?" — two BILL_TYPE slots; "amasannyalaze" = electricity | IO |
| D18 | kin | train-00000044 | bill_balance | "Mu bisanzwe nakwishyura fagitire y'amafaranga angahe ku mazi n'umuriro" — BILL_TYPE: mazi n'umuriro | Kinyarwanda: "How much do I normally pay for water and electricity bills?" — utility billing domain confirmed | IO |
| D19 | amh | train-00000044 (config amh) | bill_balance | "በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" | No METER_ID, UTILITY_ACCOUNT_NUMBER, or STS_TOKEN slots present anywhere in Amharic sample | OO |
| D20 | amh | train-00000041 | book_flight | "ወደ ቱርክ በፍጥነት የምደርስበት የበረራ አማራጭ ንገረኝ።" — COUNTRY: ቱርክ | "Tell me a flight option to Turkey quickly." — Travel domain; no utility-specific intents observed in 19 Amharic samples | IO |
| D21 | sot | train-00000044 | bill_balance | "Ke hloka bokae ho lefa karete ya Edgars" — spans: [] | Sesotho: "How much do I need to pay the Edgars card?" — Edgars is South African retail credit card; no slots annotated despite implied BILL_TYPE/SHOPPING_ITEM | OC |
| D22 | hau | train-00000015 | confirm_reservation | "Za ku iya tabbatar min ina da ajiyar tebur a taco bell da ƙarfe 7 na yamma" — RESTAURANT_NAME: taco bell | Hausa: "Can you confirm I have a table reservation at Taco Bell at 7 PM?" — Western fast food chain in culturally-specific dataset | IC |
| D23 | eng | train-00000164 | restaurant_reservation | raw: "miateŋu kpɔ teƒe le nuɖuƒe aɖe le Adidogoméa?" text: "Can you make a reservation in this restaurant in Adidogomé?" — CITY_OR_PROVINCE: Adidogomé | Ewe source utterance; English eng config translates with non-standard place name (Adidogomé, Togo) | IC |
| D24 | amh | (all 19 examples) | various | All 19 Amharic examples use Ethiopic script without any romanized characters or Latin-script code-switching | No code-switched (Amharic + English intrasentential) utterances observed in 19 Amharic train examples | IC |
| D25 | amh | train-00000003 | balance | "በቴሌብር የብድር አካውንቴ ላይ አሁን ያለብኝ ቀሪ ሂሳብ ምን ያህል ነው።" | Intent is `balance` not a utility-specific intent; Telebirr loan balance query in banking domain | IO |
| D26 | orm | train-00000008 | book_flight | "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" — no spans annotated | Oromo flight booking utterance involving Dire Dawa, Bole (Addis Ababa airport), Jimma, Ethiopian Airlines — slot spans missing | OC |
| D27 | amh | train-00000023 | car_rental | "ከሚመጣው ወር ጀምሮ ለ3 ወር ቶዮታ መኪና መከራየት እፈልጋለሁ።" — DATE: ከሚመጣው ወር ጀምሮ ለ3 ወር | "I want to rent a Toyota car for 3 months starting next month." — Arabic numeral "3" mixed with Ethiopic in DATE span | IF |
| D28 | lin | train-00000044 | bill_balance | "Niongo ya snel ezali 2000 FC Yebisa ngai soki nakosi" — PAYMENT_COMPANY: snel, MONEY: 2000 FC | Lingala: "SNEL bill is 2000 FC, tell me if I've paid" — SNEL is the DRC national electricity utility; utility company annotated as PAYMENT_COMPANY | OO |
| D29 | amh | train-00000036 | balance | "የእኔ የወጭ አካውንት ቀሪ ሂሳብ ስንት እንደሆነ ሊነግሩኝ ይችላሉ።" — ACCOUNT_TYPE: የወጭ አካውንት | "Can you tell me the remaining balance of my expense account?" — formal polite register (ሊነግሩኝ ይችላሉ) | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Amharic utility-adjacent bill balance intents with electricity-specific BILL_TYPE slots
- **Dimension(s):** IO, IC
- **Observation:** The Amharic split contains direct electricity bill balance queries with correctly annotated BILL_TYPE slots. Example D1 ("በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" — "How much do I need to pay for electricity per month?") annotates "ለመብራት" (for electricity/light) as BILL_TYPE. Example D8 ("የዚህ ወር መከፈል ያለባቸውን የፍጆታ ዝርዝር አሳየኝ།" — "Show me this month's utility expenses list") annotates "የዚህ ወር" as DATE. These utterances are structurally identical to what an EEU chatbot user would produce for a bill_balance intent.
- **Deployment relevance:** EEU and AAWSA billing chatbots require robust `bill_balance` intent detection with electricity-specific BILL_TYPE slots. The Amharic data directly provides labeled training examples for this pattern.
- **Datapoint citations:**
  - [D1] Example train-00000044 (amh, split=train, label=bill_balance): "በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" — electricity (ለመብራት) tagged as BILL_TYPE
  - [D8] Example train-00000052 (amh, split=train, label=bill_balance): "የዚህ ወር መከፈል ያለባቸውን የፍጆታ ዝርዝር አሳየኝ።" — utility expense list query with DATE slot correctly annotated

#### Strength 2: Ethiopian-specific financial institutions confirmed as named entity values in Amharic split
- **Dimension(s):** IC, OO
- **Observation:** The Amharic examples include Ethiopian banks as BANK_NAME values: "አማራ ባንክ" (Amara Bank, D2) and "ንግድ ባንክ" (Commercial Bank of Ethiopia, D3). Critically, Telebirr — Ethiopia's dominant mobile money platform used to pay utility bills — appears as a PAYMENT_COMPANY slot in D4 ("በቴሌብር የብድር አካውንቴ ላይ አሁን ያለብኝ ቀሪ ሂሳብ ምን ያህል ነው።"). This resolves one of the flagged gaps from the web search findings, which could not confirm Telebirr's presence in the dataset.
- **Deployment relevance:** The deployment specification requires robust Telebirr slot-filling as a high-priority payment company value. Its confirmed presence in Amharic training data means models fine-tuned on INJONGO will have at least some exposure to this entity.
- **Datapoint citations:**
  - [D4] Example train-00000003 (amh, split=train, label=balance): "በቴሌብር የብድር አካውንቴ ላይ አሁን ያለብኝ ቀሪ ሂሳብ ምን ያህል ነው።" — PAYMENT_COMPANY: ቴሌብር — Telebirr confirmed as PAYMENT_COMPANY value
  - [D2] Example train-00000016 (amh, split=train, label=balance): "የአማራ ባንክ አካውንቴ ስንት አለው" — BANK_NAME: አማራ ባንክ — Ethiopian bank confirmed as BANK_NAME
  - [D3] Example train-00000018 (amh, split=train, label=balance): "ንግድ ባንክ ላይ የቀረኝ ገንዘብ አለ" — BANK_NAME: ንግድ ባንክ — CBE confirmed as BANK_NAME

#### Strength 3: Ethiopian regional cities and Ethiopian calendar system used in Amharic slot values
- **Dimension(s):** IC
- **Observation:** The Amharic split uses Ethiopian-specific geographic entities and the Ethiopian calendar. D5 names Dire Dawa (ድሬዳዋ) and Bahir Dar (ባህርዳር) as CITY_OR_PROVINCE slot values, while D6 uses the Ethiopian calendar month Hamle (ሃምሌ) and D5 uses Meskerem (መስከረም) as DATE slot values. The eng config corroborates this: D12 identifies Hawassa and Arba Minch as CITY_OR_PROVINCE values in an Amharic-sourced utterance.
- **Deployment relevance:** Ethiopian utility accounts and user queries reference regional capitals (Dire Dawa, Hawassa) that are confirmed deployment cities. The use of the Ethiopian calendar is directly relevant because users will phrase temporal references using Amharic calendar month names, not Gregorian months.
- **Datapoint citations:**
  - [D5] Example train-00000042 (amh, split=train, label=book_flight): "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ።" — CITY_OR_PROVINCE: ድሬዳዋ, ባህርዳር; DATE uses Ethiopian month Meskerem
  - [D6] Example train-00000011 (amh, split=train, label=car_rental): "ከሃምሌ 4 እስከ 6 የቤት መኪና ኪራይ ማግኘት እችላለሁ?" — DATE: ከሃምሌ 4 እስከ 6 — Ethiopian calendar month Hamle
  - [D12] Example train-00000053 (eng, split=train, label=travel_suggestion): raw "ለቀጣይ የጉብኝት ጉዞዬ በሃዋሳ እና በአርባ ምንጭ መካከል…" — Hawassa and Arbaminch confirmed as city entities

#### Strength 4: Telebirr confirmed in eng config from an Amharic source utterance, resolving a flagged gap
- **Dimension(s):** IC, OO
- **Observation:** The eng config (which contains English translations of utterances from all 16 African language annotators as practice utterances) contains an Amharic-sourced utterance (raw: "ከቴሌ ብር አካዉንቴ ገንዘብ ለማን ለማን እንደላኩ ዝርዝሩን አሳየኝ?" / text: "Show me history of my telebirr transfers?") with PAYMENT_COMPANY: telebirr labeled. The raw Amharic also shows intra-word spacing variation ("ቴሌ ብር" vs "ቴሌብር") that reflects real user variation.
- **Deployment relevance:** The web search flagged Telebirr's presence in INJONGO as unresolved (gap_id 8). This example resolves part of the gap: Telebirr appears both in the Amharic config (D4) and in the eng config's Amharic-sourced practice utterances, confirming it is a represented entity value in training data.
- **Datapoint citations:**
  - [D11] Example train-00000092 (eng, split=train, label=spending_history): raw "ከቴሌ ብር አካዉንቴ ገንዘብ ለማን ለማን እንደላኩ ዝርዝሩን አሳየኝ?" text "Show me history of my telebirr transfers?" — PAYMENT_COMPANY: telebirr confirmed in Amharic-sourced utterance

#### Strength 5: Ethiopic script confirmed functional in dataset with correct character rendering
- **Dimension(s):** IF
- **Observation:** All 19 Amharic examples render Ethiopic script correctly, including complex fidel characters, compound characters, and diacritics. Example D29 ("የእኔ የወጭ አካውንት ቀሪ ሂሳብ ስንት እንደሆነ ሊነግሩኝ ይችላሉ།") demonstrates polite register markers. No garbled characters, replacement characters (U+FFFD), or encoding artifacts were observed in the sampled Amharic data.
- **Deployment relevance:** Telegram transmits Ethiopic Unicode reliably, and the deployment specifies full Ethiopic script. Confirmed rendering fidelity means the benchmark data is compatible with Telegram-based deployment inputs at the character level, at least for the sampled examples.
- **Datapoint citations:**
  - [D29] Example train-00000036 (amh, split=train, label=balance): "የእኔ የወጭ አካውንት ቀሪ ሂሳብ ስንት እንደሆነ ሊነግሩኝ ይችላሉ።" — complex Ethiopic characters render without artifacts
  - [D5] Example train-00000042 (amh, split=train, label=book_flight): "ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት በረራ ያዝልኝ།" — place names and calendar month rendered correctly in Ethiopic

#### Strength 6: Utility domain appears across multiple languages, including electricity and water bill references
- **Dimension(s):** IO
- **Observation:** The `bill_balance` intent includes utility-specific BILL_TYPE values across languages. Luganda D17 annotates electricity ("amasannyalaze") and water ("Obukuumi") as two separate BILL_TYPE spans. Kinyarwanda D18 labels "mazi n'umuriro" (water and electricity) as a single BILL_TYPE span. Lingala D28 annotates SNEL (DRC national electricity utility) as PAYMENT_COMPANY. These cross-language examples confirm the utility domain is operationally populated with electricity and water billing intents.
- **Deployment relevance:** The presence of electricity and water utility queries across multiple language splits confirms that the `bill_balance` intent is not an empty or generic category — it contains real utility billing content that transfers to the Ethiopian deployment context.
- **Datapoint citations:**
  - [D17] Example train-00000044 (lug, split=train, label=bill_balance): "Obukuumi n'amasannyalaze nteekeddwa kubisasula ddi?" — BILL_TYPE: Obukuumi (water), amasannyalaze (electricity)
  - [D18] Example train-00000044 (kin, split=train, label=bill_balance): "Mu bisanzwe nakwishyura fagitire y'amafaranga angahe ku mazi n'umuriro" — BILL_TYPE: mazi n'umuriro (water and electricity)
  - [D28] Example train-00000044 (lin, split=train, label=bill_balance): "Niongo ya snel ezali 2000 FC Yebisa ngai soki nakosi" — PAYMENT_COMPANY: snel; MONEY: 2000 FC

#### Strength 7: Formal polite register in Amharic consistent with urban utility customer service interactions
- **Dimension(s):** IC
- **Observation:** Several Amharic utterances use formal polite Amharic grammatical register. D29 uses "ሊነግሩኝ ይችላሉ" (polite second-person plural form, equivalent to formal "you can tell me"), which is consistent with how urban Ethiopian users address formal service systems. D3 uses "አለ" as a balance query without explicit pronoun, matching natural Amharic speech patterns.
- **Deployment relevance:** The deployment context specifies that Addis Ababa users interact with formal service institutions using deferential but direct register. The presence of formal polite forms in training data means models will see appropriate formal register examples during fine-tuning.
- **Datapoint citations:**
  - [D29] Example train-00000036 (amh, split=train, label=balance): "የእኔ የወጭ አካውንት ቀሪ ሂሳብ ስንት እንደሆነ ሊነግሩኝ ይችላሉ።" — formal polite register (ሊነግሩኝ ይችላሉ)
  - [D3] Example train-00000018 (amh, split=train, label=balance): "ንግድ ባንክ ላይ የቀረኝ ገንዘብ አለ" — natural Amharic query without over-formalized structure

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: No METER_ID, UTILITY_ACCOUNT_NUMBER, KEBELE, or STS_TOKEN slot types exist in the 23-slot ontology — confirmed by data inspection
- **Dimension(s):** OO
- **Observation:** Inspection of all 19 Amharic examples confirms that the slot taxonomy, as implemented, has no slot types for meter identifiers, utility account numbers, STS tokens, or Ethiopian administrative sub-units (kebele, woreda, sub-city). The 23 slot types available (ACCOUNT_TYPE, BANK_NAME, BILL_TYPE, CITY_OR_PROVINCE, CURRENCY, DATE, MONEY, NUMBER, PAYMENT_COMPANY, PLACE_NAME, TIME, etc.) cannot capture these critical deployment-required entities. D19 makes this concrete: the bill_balance utterance D1 ("በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?") has no slots for meter or account reference, and no examples in the 19-sample Amharic set contain meter IDs, account numbers, or kebele references.
- **Deployment relevance:** The core functionality of an EEU prepaid meter top-up chatbot requires extracting METER_ID and STS_TOKEN from user input. The core functionality of an AAWSA chatbot requires extracting UTILITY_ACCOUNT_NUMBER and kebele-level address. None of these can be evaluated or trained using INJONGO's existing slot ontology. This is a fundamental structural gap that requires augmentation of the slot taxonomy before INJONGO can support the full deployment task.
- **Datapoint citations:**
  - [D19] Observation across all 19 amh train examples: no METER_ID, UTILITY_ACCOUNT_NUMBER, KEBELE, or STS_TOKEN spans appear in any of the 19 Amharic examples reviewed — confirmed absence of deployment-critical slot types
  - [D1] Example train-00000044 (amh, split=train, label=bill_balance): "በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" — utility bill query with only DATE and BILL_TYPE slots; no mechanism to annotate meter or account reference

#### CRITICAL Concern 2: Zero code-switched (Amharic-English) utterances observed in the 19 Amharic training examples
- **Dimension(s):** IC
- **Observation:** All 19 sampled Amharic examples are monolingual Ethiopic script. Not a single example contains English words, English morphology grafted onto Amharic roots, or mixed-script tokens. This is consistent with the YAML documentation's confirmed gap (gap_id 2: "code-switching was not an explicit design criterion"). By contrast, the deployment specification states that "code-switching with English is common and increasing, especially among younger generations" and that "technical/domain vocabulary (e.g., 'meter', 'top-up', 'token', 'balance') frequently borrowed or switched to English." D24 documents this absence explicitly.
- **Deployment relevance:** If the benchmark's Amharic split lacks code-switched utterances and the deployment population produces them with high frequency (especially for utility-specific English-origin technical vocabulary like "token", "top-up", "balance"), then benchmark evaluation scores will overestimate actual deployment performance. A model that achieves 93% accuracy on monolingual INJONGO Amharic may perform substantially worse on naturalistic Amharic-English mixed input.
- **Datapoint citations:**
  - [D24] All 19 amh train examples reviewed: "ነገ ጠዋት 12 ሰአት…", "ንግድ ባንክ ላይ…", "በቴሌብር…" — zero Latin-script tokens, zero English insertions in any of 19 Amharic examples
  - [D4] Example train-00000003 (amh, split=train, label=balance): "በቴሌብር የብድር አካውንቴ ላይ አሁን ያለብኝ ቀሪ ሂሳብ ምን ያህል ነው።" — Telebirr written in full Ethiopic (ቴሌብር), not as Latin-script "Telebirr" as deployed users would commonly type

#### CRITICAL Concern 3: No deployment-specific utility intents observed — prepaid meter top-up, outage reporting, STS token query, and load-shedding schedule absent from sampled Amharic data
- **Dimension(s):** IO
- **Observation:** The 19 Amharic samples span intents: bill_balance (3), alarm (3), balance (4), book_flight (3), cancel_reservation (2), calendar_update (2), car_rental (2), confirm_reservation (1). No `meter_top_up`, `outage_report`, `token_query`, `power_schedule_query`, `account_registration`, or analogous utility-specific intents appear. The `bill_balance` intent is present and utility-relevant (D1, D8), but the prepaid meter top-up workflow — the primary use case for EEU chatbot interactions — is not represented. D20 confirms that travel and general banking intents dominate over utility-specific ones in the sample.
- **Deployment relevance:** The deployment elicitation identified prepaid meter top-up, outage reporting, and load-shedding schedule queries as the three core use cases. The absence of these as distinct intent categories means INJONGO cannot directly train or evaluate the system's primary tasks. The paper itself acknowledges that the 5-domain/40-intent taxonomy "misses some other domains essential for real-world applications."
- **Datapoint citations:**
  - [D20] Example train-00000041 (amh, split=train, label=book_flight): "ወደ ቱርክ በፍጥነት የምደርስበት የበረራ አማራጭ ንገረኝ።" — travel intent in Amharic split, illustrating domain distribution
  - [D8] Example train-00000052 (amh, split=train, label=bill_balance): "የዚህ ወር መከፈል ያለባቸውን የፍጆታ ዝርዝር አሳየኝ།" — closest to deployment use case but scoped to bill balance inquiry, not top-up or outage

---

#### MAJOR

#### MAJOR Concern 4: Annotation quality issues — missing spans on utterances with clearly extractable entities
- **Dimension(s):** OC
- **Observation:** Multiple examples across languages have empty span targets despite containing entity-rich text. D15 (amh, alarm): "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ በደንብ እንዲሰማኝ ድምጽ ጨምርበት" clearly contains DATE (ነገ = tomorrow) and TIME (12 ሰአት = 12 o'clock) but spans are empty. D16 (amh, calendar_update): "የእናቴን እና የአባቴን የልደት ቀን" contains CALENDAR_EVENT and PERSONAL_NAME candidates but no spans annotated. D13 (orm, book_flight): "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" contains CITY_OR_PROVINCE values (Dirree dawaa = Dire Dawa, Boolee = Bole, jimmaa = Jimma) and an implied carrier name but has no spans. D21 (sot, bill_balance): "Ke hloka bokae ho lefa karete ya Edgars" contains an implied BILL_TYPE/SHOPPING_ITEM (Edgars card) but is annotated empty.
- **Deployment relevance:** Missing spans on entity-rich utterances directly reduce the quality signal for slot-filling F1 evaluation and fine-tuning. If the Amharic split contains similar under-annotated examples at scale (the sample rate is ~1%), slot-filling models trained on INJONGO may learn to under-predict spans, harming deployment performance on the extraction tasks most critical to the EEU/AAWSA workflow.
- **Datapoint citations:**
  - [D15] Example train-00000045 (amh, split=train, label=alarm): "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ በደንብ እንዲሰማኝ ድምጽ ጨምርበት" — spans empty despite clear DATE (ነገ) and TIME (12 ሰአት) candidates
  - [D16] Example train-00000035 (amh, split=train, label=calendar_update): "የእናቴን እና የአባቴን የልደት ቀን የቀን መቁጠሪያዬ ላይ ስላቀያየርኩት አስተካክለው" — spans empty despite CALENDAR_EVENT content
  - [D13] Example train-00000041 (orm, split=train, label=book_flight): "Balallii Dirree dawaa irraa gara Boolee achiin gara jimmaa Xiyyaara Itoopiyaa irraa naaf kuti" — spans empty despite 3 city names identifiable

#### MAJOR Concern 5: Ground-truth label authority mismatch — Amharic annotations by pan-African crowdworkers, not Ethiopian utility domain experts
- **Dimension(s):** OC
- **Observation:** The deployment specification states that "correct extraction should be validated by the respective utility's customer service agents (Ethiopian Electric Utility or Addis Ababa Water billing staff)." No evidence in the sampled data or documentation confirms that Amharic annotators had domain familiarity with Ethiopian utility billing. The web search confirmed this gap explicitly (gap_id 3: "NOT FOUND"). The annotator pool was managed through a Kenya-based logistics company at per-country rates. The Amharic examples sampled (D1, D7, D8) contain utility-relevant content, but their BILL_TYPE slot boundaries and values reflect general native-speaker intuition, not EEU/AAWSA billing terminology conventions.
- **Deployment relevance:** For a deployment where ground truth is defined by utility agents (e.g., whether "ለመብራት" correctly maps to the BILL_TYPE that EEU's billing system recognizes, or whether informal Addis Ababa neighborhood references in PLACE_NAME slots match official utility account address fields), the benchmark's crowdworker annotations may systematically diverge from the authoritative ground truth. This could manifest as false positive slot extractions in production.
- **Datapoint citations:**
  - [D7] Example train-00000051 (amh, split=train, label=bill_balance): "የቦሎ ማሳደሻ ስንት ነው መክፈል የሚኖርብኝ?" — BILL_TYPE: የቦሎ ማሳደሻ — "Bole upgrade/road expansion" billed to resident; whether this maps to an EEU/AAWSA billing category cannot be confirmed without domain expert review
  - [D1] Example train-00000044 (amh, split=train, label=bill_balance): "በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" — BILL_TYPE: ለመብራት — electricity payment query annotated by general native speaker, not EEU billing staff

#### MAJOR Concern 6: `bill_balance` intent conflates utility bill queries with unrelated payment queries across the dataset
- **Dimension(s):** IO, OO
- **Observation:** The `bill_balance` intent is used heterogeneously across language configs. In Amharic (D1, D8), it maps to electricity utility bill queries. In Hausa D28-equivalent (hau config), it covers GOTV (cable TV) subscription: "Zaka iya sanar da ni nawa ne kuɗin gotv ɗin wata biyu?" In Twi, it covers telecel fiber bills. In Zulu, it covers electricity ("sagesi") and phone bills. In Sesotho (D21), it covers a retail credit card (Edgars). This heterogeneity means `bill_balance` as an intent label covers a wide range of billing contexts that may not all be relevant or may require disambiguation in an EEU/AAWSA deployment.
- **Deployment relevance:** An EEU chatbot trained on INJONGO's `bill_balance` intent would learn from examples spanning cable TV, retail credit, mobile phone bills, and utility bills. In a deployment scoped exclusively to electricity and water utilities, this may introduce noise in intent classification precision, or require post-processing to distinguish utility billing from general billing.
- **Datapoint citations:**
  - [D1] Example train-00000044 (amh, split=train, label=bill_balance): "በወር ለመብራት ስንት ነው መክፈል የሚገባኝ?" — electricity utility bill
  - [D22] Example train-00000052 (hau, split=train, label=bill_balance): "Zaka iya sanar da ni nawa ne kuɗin gotv ɗin wata biyu?" — GOTV cable TV bill — same intent label, different domain

#### MAJOR Concern 7: Transliteration degradation in eng config reduces reliability of cross-lingual transfer evaluation for Amharic
- **Dimension(s):** IF, OC
- **Observation:** The eng config contains English translations of utterances from all 16 African languages' annotators as practice utterances. D10 shows an Amharic-sourced utterance where "ዳሽን ባንክ" (Dashen Bank, a major Ethiopian bank) is translated as "dasion bank" — a misspelling that would introduce noise in English-side training data. The BANK_NAME slot value in English ("dasion bank") does not match the correct romanization ("Dashen Bank") and would not be recognized by an English-language model as a known Ethiopian bank.
- **Deployment relevance:** Cross-lingual transfer from the INJONGO English split to Amharic is a documented evaluation setup. If the English-side training data contains transliteration errors for Ethiopian entities, zero-shot transfer experiments may underestimate Amharic-centric model performance or produce incorrect entity extractions in translate-test settings.
- **Datapoint citations:**
  - [D10] Example train-00000045 (eng, split=train, label=balance): raw "እባካችሁ የዳሽን ባንክ ሂሳቤን ታረጋግጡልኛላችሁ?" text "can you please check my dasion bank account" — BANK_NAME: dasion bank — "ዳሽን" (Dashen) mistransliterated as "dasion"

#### MAJOR Concern 8: Amharic-specific Fleiss' Kappa scores not surfaced; Amharic pre-review annotation quality unknown
- **Dimension(s):** OC
- **Observation:** The YAML documentation and web search both flag that Amharic-specific Kappa scores from Table 3 were not accessible (gap_id 7: "NOT FOUND"). The paper reports a range of 0.618–0.934 pre-review across all languages. The two largest pre-to-post improvements were Sesotho (+0.327) and Zulu (+0.294). It is unknown where Amharic falls within this range. The sampled data shows concerning annotation gaps (D15, D16) with empty spans on entity-rich utterances, suggesting potential annotation inconsistency.
- **Deployment relevance:** For a deployment relying on INJONGO Amharic slot-filling labels as ground truth for model training and evaluation, unknown pre-review annotation quality represents unquantified uncertainty. If Amharic had a pre-review Kappa closer to 0.618 (like Zulu) rather than 0.934, the reviewed annotations may have involved substantial disagreement resolution that could systematically diverge from the utility-domain interpretation needed for EEU/AAWSA deployment.
- **Datapoint citations:**
  - [D15] Example train-00000045 (amh, split=train, label=alarm): "ነገ ጠዋት 12 ሰአት የቀጠርኩትን ማንቂያ" — empty spans despite identifiable DATE and TIME — consistent with annotation inconsistency
  - [D16] Example train-00000035 (amh, split=train, label=calendar_update): "የእናቴን እና የአባቴን የልደት ቀን" — empty spans despite CALENDAR_EVENT content

---

#### MINOR

#### MINOR Concern 9: Arabic numeral mixing in Amharic DATE spans alongside Ethiopic text — not explicitly addressed
- **Dimension(s):** IF
- **Observation:** D27 (amh, car_rental): "ከሚመጣው ወር ጀምሮ ለ3 ወር ቶዮታ መኪና መከራየት እፈልጋለሁ།" uses Arabic numeral "3" embedded within an otherwise Ethiopic-script Amharic utterance. The DATE span annotation covers "ከሚመጣው ወር ጀምሮ ለ3 ወር" including the numeral. This confirms that mixed-numeral usage appears in the dataset, but it is an incidental occurrence rather than a systematically designed feature.
- **Deployment relevance:** Ethiopian utility users may mix Ethiopic numerals (፩፪፫), Western Arabic numerals (1 2 3), and numeral words in Amharic, particularly in meter IDs, account numbers, and payment amounts. The benchmark's casual handling of numeral mixing (no dedicated slot type, incidental inclusion) means tokenizer and extraction behavior on numeral-heavy utility inputs cannot be assessed from the benchmark alone.
- **Datapoint citations:**
  - [D27] Example train-00000023 (amh, split=train, label=car_rental): "ከሚመጣው ወር ጀምሮ ለ3 ወር ቶዮታ መኪና መከራየት እፈልጋለሁ།" — DATE span includes Arabic numeral "3" embedded in Ethiopic text

#### MINOR Concern 10: Some Western cultural entities remain in the dataset despite the cultural grounding mandate
- **Dimension(s):** IC
- **Observation:** D22 (hau, confirm_reservation): "Za ku iya tabbatar min ina da ajiyar tebur a taco bell da ƙarfe 7 na yamma" annotates "taco bell" as RESTAURANT_NAME — a Western fast-food chain with no presence in Nigeria or most of Sub-Saharan Africa. This is a residual Western entity despite the dataset's stated cultural grounding mandate.
- **Deployment relevance:** For the Amharic Ethiopian deployment specifically, this observation is lower severity since the RESTAURANT_NAME slot type is not relevant to EEU/AAWSA chatbot interactions. However, it confirms that the cultural grounding mandate was not fully enforced across all language splits, which marginally reduces confidence in the broader cultural validity claim.
- **Datapoint citations:**
  - [D22] Example train-00000031 (hau, split=train, label=confirm_reservation): "Za ku iya tabbatar min ina da ajiyar tebur a taco bell da ƙarfe 7 na yamma" — RESTAURANT_NAME: taco bell — Western chain in Hausa-language African context

#### MINOR Concern 11: Utility entity annotated as PAYMENT_COMPANY rather than a utility-specific slot type in Lingala
- **Dimension(s):** OO
- **Observation:** D28 (lin, bill_balance): "Niongo ya snel ezali 2000 FC Yebisa ngai soki nakosi" annotates SNEL (Société Nationale d'Électricité, DRC's national electricity utility) as PAYMENT_COMPANY. While this is a reasonable annotation under the existing 23-slot ontology, it conflates a utility service provider with a payment company, potentially causing confusion when similar Ethiopian entities (EEU, AAWSA) appear in utterances.
- **Deployment relevance:** In an Ethiopian deployment, EEU and AAWSA are utility providers, not payment companies. If the model learns from cross-lingual examples where utility companies are labeled PAYMENT_COMPANY, it may incorrectly classify Ethiopian utility references. This is a minor ontological ambiguity that could affect cross-lingual transfer quality.
- **Datapoint citations:**
  - [D28] Example train-00000044 (lin, split=train, label=bill_balance): "Niongo ya snel ezali 2000 FC Yebisa ngai soki nakosi" — PAYMENT_COMPANY: snel — national electricity utility labeled as payment company

---

### Content Coverage Summary

The 19 Amharic training examples reviewed span 8 intent categories: bill_balance, alarm, balance, book_flight, cancel_reservation, calendar_update, car_rental, and confirm_reservation. All utterances are monolingual Ethiopic script with natural Amharic register. Ethiopian-specific entities are well-represented: Telebirr (ቴሌብር) appears as PAYMENT_COMPANY, Ethiopian banks (Amara Bank, Commercial Bank of Ethiopia) appear as BANK_NAME, Ethiopian regional cities (Dire Dawa, Bahir Dar) appear as CITY_OR_PROVINCE, and Ethiopian calendar months (Hamle, Meskerem) appear as DATE values. The utility domain is touched by bill_balance intents referencing electricity (ለመብራት) and general utility expenses, but there is no representation of the deployment's primary intents: prepaid meter top-up, outage reporting, STS token entry, or load-shedding schedule queries. The 23-slot ontology, while useful for general banking, travel, and household intents, lacks all deployment-critical slot types (METER_ID, UTILITY_ACCOUNT_NUMBER, KEBELE, STS_TOKEN). No code-switched Amharic-English utterances were observed in the 19 Amharic samples, despite this being a confirmed high-priority deployment requirement. Across the 16 non-Amharic language configs, the dataset shows strong cultural grounding with local payment companies (Flooz in Ewe, Orange Money and SNEL in Lingala, MoMo in Kinyarwanda, Tigo-Pesa in Swahili), local banks, and locally appropriate geographic entities, reinforcing that the cultural grounding principle was applied. Annotation quality shows some gaps, with empty span annotations on utterances containing identifiable entities (most notably in Amharic, Oromo, and Sesotho examples), suggesting some under-annotation that may reduce slot-filling training signal.

---

### Limitations

1. **Sample size per language:** Only 19 Amharic training examples were reviewed out of 2,240 total (0.85%). Patterns observed (absence of code-switching, absence of meter/account intents) are consistent with design documentation but cannot be claimed as exhaustive — rare phenomena in the full corpus may not appear in the sample.

2. **Test and validation splits not inspected:** Only training split examples were sampled. Evaluation results on INJONGO are reported on test splits; annotation quality in the test split cannot be assessed from the training sample.

3. **Utility-domain intent distribution unknown:** The 19 Amharic examples include only 3 bill_balance instances. The full distribution across all 40 intents (80 per intent = 8 utility-domain intents × 80 = ~640 utility examples in Amharic) cannot be assessed from the sample. The actual utility domain content (including any outage or top-up adjacent intents) may differ from what the sample shows.

4. **Telebirr coverage depth unquantifiable:** While Telebirr was confirmed as present in both the Amharic config (D4) and the eng config (D11), the frequency of its appearance as a PAYMENT_COMPANY value across the full 2,240 Amharic training examples cannot be determined from two instances. It may appear only rarely.

5. **Annotation spans use byte offsets, not character offsets:** The `spans` field uses `start_byte` and `limit_byte`. For Ethiopic script, multi-byte UTF-8 characters mean character and byte positions diverge. This was not independently verified against the raw text in the sample, but annotation correctness was inferred from the `target` field string values.

6. **Non-Amharic configs reviewed only partially:** The 15 non-Amharic configs were reviewed primarily to contextualize the Amharic data and cross-linguistic ontology observations. Language-specific validity claims for other languages are outside the deployment scope and not fully assessed here.

7. **Unicode normalization form (NFC vs. NFD) not determinable from rendered output:** Character rendering appeared correct, but whether the underlying bytes use NFC or NFD normalization cannot be verified through text inspection alone and requires direct encoding analysis of the raw parquet files.

