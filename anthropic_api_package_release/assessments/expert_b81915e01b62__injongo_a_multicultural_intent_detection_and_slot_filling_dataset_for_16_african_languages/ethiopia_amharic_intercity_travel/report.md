## Deployment Context

**Use case:** Amharic intercity-travel booking bots for Sky Bus, Selam Bus, and Ride covering routes, fares, and seat changes
**Target population:** Inter-regional commuters and travelers booking long-distance buses and ride-hail trips via smartphone apps

# Validity Analysis: INJONGO
**Target context:** Ethiopian Intercity/Ride-Hail Commuter Cohort (Amharic-Primary)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 3 | Moderate gaps | high |
| Input Form ✓ | 5 | Strong alignment | high |
| Output Ontology | 2 | Significant gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ✓ | 4 | Minor gaps | high |
| **Average** | **3.0** | | |

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

INJONGO is the most relevant existing benchmark for Amharic intent detection and slot-filling, and the only large-scale resource of its kind. For the Ethiopian intercity/ride-hail deployment, it provides genuine value in three respects: (1) Amharic is included as a first-class language with culturally grounded entities (Ethiopian banks, TeleBirr, Ethiopian cities including Dire Dawa, Bahir Dar, Hawassa, Arba Minch, and even Ge'ez calendar months Meskerem and Hamle as DATE slot values); (2) text/Ge'ez script and structured intent+slot output exactly match deployment requirements; (3) annotation quality after review is high (κ=0.933 for Amharic). However, three substantive gaps limit construct validity for this specific deployment: (a) the 40-intent travel taxonomy is air-travel-framed and entirely lacks intercity bus, seat-class, fare-tier, and operator-specific rebooking intents — confirmed empirically in the Amharic split (HIGH-priority IO concern); (b) Ethiopian Birr is absent as a CURRENCY/MONEY slot value in the sampled Amharic data while other tracks' currencies (Naira, Rand) are well-represented, and most Amharic DATE slots use relative expressions rather than named Ge'ez months (HIGH-priority IC residuals); (c) no code-switched Amharic–Oromo / Amharic–Tigrinya utterances exist despite the L2-heavy multi-regional user base, and annotator regional demographics are undisclosed (HIGH-priority OC concern). The benchmark is suitable as a foundation but requires deployment-specific supplementation before being treated as sufficient evaluation evidence.

## Practical Guidance

### What This Benchmark Measures

INJONGO measures Amharic NLU performance on a 40-intent / 23-slot taxonomy spanning banking, home, kitchen-and-dining, travel, and utility domains, using accuracy (intent) and F1 (slot). It provides a valid measure of (i) general Amharic text comprehension by encoder, encoder-decoder, and LLM-prompted models, (ii) culturally grounded slot extraction for Ethiopian banks, payment platforms (TeleBirr), and major intercity cities, and (iii) cross-lingual transfer behavior from English to Amharic. Strongest dimensions for this deployment are input form (full text/Ge'ez match) and output form (structured intent+slot output matches NLU module). It can support model selection across encoder, decoder, and LLM families for the Amharic NLU layer.

### Construct Depth

Construct depth is shallow-to-moderate for the deployment's actual task. The benchmark probes generic conversational NLU on Amharic and partially covers Ethiopian cultural grounding in banking and selected travel slots, but it does not probe (a) intercity bus operator booking flows, (b) seat-class/fare-tier reasoning, (c) Ethiopian Birr fare extraction in travel context, (d) Ethiopian-clock-convention TIME extraction, (e) Ge'ez-calendar dense temporal reasoning beyond the few sampled instances, or (f) code-switched Amharic–Oromo / Amharic–Tigrinya robustness. High benchmark scores would not justify confidence that a deployed model handles fare extraction, holiday-surge bookings, or L2-speaker code-switched utterances correctly.

### What Else You Need

(1) For input ontology: build an operator-specific intent inventory (Sky Bus, Selam Bus, Ride) covering seat-class upgrade, road-closure rebooking, holiday-surge booking, and operator-specific cancellation; benchmark on this. (2) For input content: collect or synthesize an Amharic test slice with Ethiopian Birr-denominated fares, dense Ge'ez calendar month references including Pagume, Ethiopian-clock-convention TIME values, and the full set of intercity corridor toponyms; supplement with code-switched Amharic–Oromo and Amharic–Tigrinya utterances. (3) For output content: re-annotate or expert-validate a slice using non-Addis-centric L2 Amharic annotators, including rural and Tigray/Oromia-region speakers, to assess label validity for code-switched utterances. (4) Supplement with EthioBenchmark NER/POS as auxiliary evidence, and operator-log-derived utterances for ecological validity.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
INJONGO's travel domain is derived from CLINC's generic intent set ('exchange rate', 'book flight') [Q39] and explicitly omits intercity bus operator flows. Empirical inspection of the Amharic split confirms that all sampled travel-domain Amharic utterances use air-travel framing (book_flight to Turkey, Sudan) or generic car rental — there are no intercity bus, seat-class, or operator-specific intents [DATASET-D7, D8, D25, D26]. The deployment requires intent detection for Sky Bus / Selam Bus / Ride bus and ride-hail booking, including seat-class upgrade, road-closure rebooking, holiday-surge booking, and operator-specific cancellation, none of which appear in the 40-intent taxonomy. The paper itself acknowledges scope limits [Q107, Q111]. Although elicitation marked IO as MODERATE priority (user accepts general travel intents as broadly comparable), the empirical ontology mismatch in the travel subdomain is concrete and substantial.

**Strengths:**
- Joint intent + slot taxonomy is well-defined and matches the deployment's NLU module structure [Q2, Q31]
- Travel is one of five included domains, providing partial overlap with bus booking flows [Q5, Q117]
- Ground-up African-context elicitation rather than translation reduces some Western framing [Q8, Q30]

**Checklist:**

- **IO-1**: Required categories for the deployment include intercity bus route queries, fare lookup, seat selection (VIP/economy), booking, cancellation/rebooking — only generic 'book_flight', 'car_rental', and 'travel_suggestion' overlap, established by elicitation and observed in the Amharic data [DATASET-D7, D8]. — _Sources: DATASET-D7, DATASET-D8_
- **IO-2**: Yes. INJONGO covers 5 domains and 40 intents derived from CLINC [Q39, Q117] and omits intercity bus, seat-class selection, holiday-surge booking, and road-closure rebooking. The paper explicitly notes the taxonomy 'missing some other domains such as healthcare and education' [Q107] and a non-natural intent frequency distribution [Q111]. — _Sources: Q39, Q107, Q117_
- **IO-3**: The travel domain is dominated by air travel framing in the Amharic split (international flights to Turkey, Sudan) [DATASET-D7, D8, D25, D26]; these are not necessarily irrelevant but concentrate evaluation weight on air rather than surface intercity transport relevant to the deployment. — _Sources: DATASET-D7, DATASET-D8, DATASET-D25, DATASET-D26_
- **IO-4**: Documented gaps: (a) no intercity bus operator intents, (b) no seat-class/fare-tier intents, (c) no rebooking-on-disruption intent, (d) no Ethiopian-holiday surge booking intents — all of which harm content validity for this specific deployment. — _Sources: Q107, Q111, DATASET-D30_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q39] 'we extracted 40 intents from five most suitable domains to the African contexts: Banking ... Travel (e.g. "exchange rate", "book flight")' (p.3)
- [Q107] 'The scope of INJONGO is constrained by its coverage of only 5 domains and 40 intents, missing some other domains such as healthcare and education that are essential for real-world applications.' (p.9)
- [Q111] 'the fixed distribution of examples across intents may not accurately reflect the natural frequency of these interactions in real-world conversations.' (p.9)
- [Q117] 'These are a total of 40 categories across 5 domains (Banking, Kitchen and Dining, Travel, Utility, and Home).' (p.13)

*Web sources:*
- [WEB-9] INJONGO GitHub confirms domain/intent inventory matches CLINC-derived taxonomy

*Dataset analysis:*
- DATASET-D7: Amharic book_flight is international air travel (to Turkey), no surface transport
- DATASET-D8: Amharic book_flight to Sudan — international air, no bus operator
- DATASET-D25, D26: Both Amharic book_flight examples are international air; no intercity bus intents
- DATASET-D30: No intercity corridors, seat class, bus operator, or fare tier present in Amharic travel utterances

</details>

**Information gaps:**
- Whether any Amharic travel-domain utterances in the unsampled 99.4% of the dataset use surface-transport framing

**Requires expert verification:**
- Definitive intent inventory of Sky Bus / Selam Bus / Ride booking APIs to quantify gap

---

### Input Content — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
Empirical dataset inspection partially resolves what the paper does not document. Ethiopian calendar months (Meskerem, Hamle) appear as DATE slot values [DATASET-D1, D2, D6], Ethiopian intercity cities (Dire Dawa, Bahir Dar, Hawassa, Arba Minch) appear as CITY_OR_PROVINCE slots [DATASET-D2, D9], and Ethiopia-specific financial entities (Amhara Bank, Commercial Bank of Ethiopia, TeleBirr, Dashen Bank) appear in banking-domain instances [DATASET-D3, D4, D5, D34]. This is materially better than the registry feared. However, several deployment-critical content gaps remain: (a) Ethiopian Birr (ETB) was absent as a CURRENCY/MONEY slot value in any sampled Amharic example despite Naira/Rand appearing in other tracks [DATASET-D5, D19, D22 vs Amharic absence]; (b) most Amharic DATE slots used relative expressions rather than named Ge'ez months (only 2/9) [DATASET-D15, D16, D28]; (c) Ethiopian time convention (6-hour offset) is unaddressed in TIME annotations [DATASET-D11, D23]; (d) no code-switched Amharic–Oromo / Amharic–Tigrinya utterances appear, despite ~70% L2 Amharic users in the deployment population [DATASET-D1–D18 monolingual]. IC was marked HIGH priority in elicitation, so these residual gaps weigh heavily.

**Strengths:**
- Ethiopian calendar months (Meskerem, Hamle) confirmed as valid DATE slot annotations in travel-domain Amharic instances [DATASET-D1, D2, D6]
- Major Ethiopian intercity cities (Dire Dawa, Bahir Dar, Hawassa, Arba Minch) appear as CITY_OR_PROVINCE slots [DATASET-D2, D9]
- Ground-up cultural elicitation methodology rather than translation [Q6, Q13, Q30]
- Ethiopia-specific banks and TeleBirr appear as natively grounded entities [DATASET-D3, D4, D5]

**Checklist:**

- **IC-1**: Yes — deployment demands Amharic city names/abbreviations, Ethiopian calendar dates, Birr fares, and operator-specific terminology, confirmed by elicitation Q2 (HIGH priority) and YAML calendar/toponym sections. — _Sources: Q6, Q30_
- **IC-2**: Partially. Cultural grounding is confirmed for banking-domain Amharic [DATASET-D3, D4, D5] and partially for travel (Ethiopian cities + Meskerem present) [DATASET-D1, D2, D9]. The grounding methodology is documented [Q30, Q40, Q41]. — _Sources: Q40, DATASET-D1, DATASET-D2, DATASET-D3, DATASET-D4, DATASET-D5, DATASET-D9_
- **IC-3**: Western-content leakage was not observed in the Amharic sample (though present in some other tracks, e.g., Hausa Taco Bell [DATASET-D31]). Air-travel-to-international-destinations framing dominates the Amharic travel domain [DATASET-D7, D8]. — _Sources: DATASET-D7, DATASET-D8, DATASET-D31_
- **IC-4**: Native Amharic speakers annotated [Q7], but regional/L2 demographics undisclosed and code-switched utterances absent from sample [DATASET-D1–D18]; full re-annotation by Ethiopian regional pool would be advisable. — _Sources: Q7_
- **IC-5**: Documented residual content gaps: (a) Birr/ETB absent from sampled Amharic CURRENCY/MONEY slots; (b) Ethiopian calendar months sparse vs. relative dates [DATASET-D15, D16, D28]; (c) Ethiopian clock convention undocumented; (d) no code-switched utterances [DATASET-D1–D18]. — _Sources: DATASET-D11, DATASET-D15, DATASET-D16, DATASET-D28, DATASET-D5, DATASET-D19, DATASET-D22_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q6] 'providing an annotator with sentences from the CLINC dataset ... they are to come up with culturally-relevant similar sentences and relevant slot entities' (p.1)
- [Q30] 'we ensured that the slot entities are more culturally relevant in the respective countries the languages are from' (p.2)
- [Q40] 'A Xhosa annotator was asked to generate another utterance ... capturing the South African context' (p.3)
- [Q88] 'The performance of some African languages is often higher than others, this is probably connected to the amount of monolingual data available on the web.' (p.7)

*Web sources:*
- [WEB-9] INJONGO GitHub provides direct dataset access; banking-domain Amharic utterances reference Ethiopian banks (Abay Bank)
- [WEB-3] Amharic functions as L2 lingua franca; ~29.3% L1 speakers — code-switching expected in deployment population

*Dataset analysis:*
- DATASET-D1, D2: 'ከድሬዳዋ ወደ ባህርዳር ለመስከረም አምስት' — Ethiopian cities + Ge'ez month Meskerem in travel-domain DATE slot
- DATASET-D6: Hamle (Ethiopian month) used in DATE slot
- DATASET-D9: Hawassa and Arba Minch as CITY_OR_PROVINCE slots in travel_suggestion
- DATASET-D3, D4, D5: Amhara Bank, Commercial Bank of Ethiopia, TeleBirr — Ethiopia-specific banking entities
- DATASET-D15, D16, D28: Most Amharic DATE annotations use relative expressions ('this month', 'next month') rather than named Ethiopian calendar months
- DATASET-D5 vs D19, D22: TeleBirr present as PAYMENT_COMPANY but no Birr-denominated CURRENCY/MONEY slot in Amharic sample, while Naira (Hausa) and Rand (Xhosa) are well-represented
- DATASET-D1–D18: All Amharic utterances monolingual; no Oromo/Tigrinya/English code-switching observed
- DATASET-D11, D23: Ethiopian clock convention (12 ሰአት) ambiguity; one example unannotated

</details>

**Information gaps:**
- Birr coverage in the 99.4% of Amharic data not sampled
- Frequency of named Ethiopian calendar months vs. relative dates in full travel split
- Whether any code-switched Amharic utterances exist in unsampled portions

**Requires expert verification:**
- Native Amharic-speaking expert review of Ethiopian time convention handling in TIME slots across the full dataset

---

### Input Form — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
INJONGO is a text-only benchmark [Q38, Q43] released under CC BY 4.0 [Q23], with Amharic encoded in Ge'ez/Ethiopic script. The deployment is also a text-based smartphone app, with primary input in Ge'ez script. Dataset inspection confirms all sampled Amharic examples use proper Ge'ez script with no romanization or mixed-script anomalies [DATASET-D1, D5]. There is full modality and script alignment. Elicitation marked IF as LOWER priority, consistent with no concrete violations.

**Strengths:**
- Text modality fully matches deployment [Q38]
- Ge'ez script used consistently in all sampled Amharic examples with no anomalies [DATASET-D1, D5]
- CC BY 4.0 license permits adaptation [Q23]

**Checklist:**

- **IF-1**: Both source and target are plain text in Ge'ez script for Amharic [Q38, DATASET-D1]. — _Sources: Q38, DATASET-D1_
- **IF-2**: Smartphone IMEs support Ge'ez input on major Android distributions (qualitative web evidence). National 4G coverage of ~33% [WEB-6] affects connectivity but not signal form. — _Sources: WEB-6_
- **IF-3**: No domain-specific form differences relevant — both contexts are typed conversational text. — _Sources: Q38_
- **IF-4**: No form mismatches identified for the Amharic deployment. — _Sources: DATASET-D1, DATASET-D5_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q23] 'Dataset is released under CC BY 4.0 license.' (p.2)
- [Q38] 'the dataset construction follows two stages: (1) Utterance elicitation in an African language and (2) Slot-filling annotation of the generated utterance.' (p.3)
- [Q43] 'The annotation followed the named entity recognition setup on LabelStudio platform.' (p.4)

*Web sources:*
- [WEB-6] GSMA Ethiopia: 3G covers ~98% of population, 4G ~33% — connectivity context for smartphone app deployment

*Dataset analysis:*
- DATASET-D1: Amharic utterance in proper Ge'ez script throughout
- DATASET-D5: Ge'ez script consistent throughout Amharic banking example

</details>

**Information gaps:**
- Behavior on code-switched tokens written in Latin script (e.g., Oromo lexical insertions) is undocumented

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The 23-slot final ontology [Q118, Q119, Q144] includes structural fits for deployment needs (CITY_OR_PROVINCE, MONEY, CURRENCY, DATE, TIME, BANK_NAME), and merging of low-frequency types is principled [Q51, Q52, Q55]. However, several decision-rule mismatches arise for the Ethiopian deployment: (a) DATE/TIME boundary rules are documented [Q153, Q154] using Gregorian conventions only — no accommodation for Ethiopian calendar (13 months, Pagume intercalary) or 6-hour offset clock; (b) the 40-intent inventory excludes intercity bus, seat-class, fare-tier, and rebooking categories required for Sky Bus/Selam Bus/Ride [Q39, DATASET-D7, D8]; (c) dataset inspection shows Amharic DATE annotations dominated by relative expressions, suggesting the operative decision rule for Ethiopian month names is undertested [DATASET-D15, D16, D28]. These are structural-validity gaps. A redeeming factor: Ethiopian month names did appear as DATE slots [DATASET-D2, D6], so the ontology can host them in principle.

**Strengths:**
- 23 slot types including travel-relevant CITY_OR_PROVINCE, MONEY, CURRENCY, DATE, TIME [Q144]
- Detailed boundary rules for ambiguous cases (TIME vs DATE, BANK_NAME word inclusion) [Q152, Q153, Q154]
- Ontology can in principle host Ge'ez month names — confirmed empirically [DATASET-D2, D6]
- Merging process reduced ambiguity from 34 to 23 types [Q55, Q119]

**Checklist:**

- **OO-1**: Most slot types are regionally relevant (cities, money, banks). However, the intent ontology lacks bus-operator-specific categories required for the deployment [Q39, DATASET-D30]. — _Sources: Q144, DATASET-D30_
- **OO-2**: Missing: intercity bus intents, seat-class/fare-tier intents, rebooking-on-disruption intent. DATE rule does not encode Ethiopian calendar month set; TIME rule does not encode Ethiopian clock convention [Q153, Q154]. — _Sources: Q39, Q153, Q154, DATASET-D30_
- **OO-3**: DATE/TIME annotation conventions are implicitly Gregorian/international as documented [Q153, Q154]; this encodes a non-Ethiopian temporal convention as default, with no documented annotator instruction for Ge'ez calendar or 6-hour-offset clock. — _Sources: Q153, Q154, DATASET-D11, DATASET-D23_
- **OO-4**: Stakeholder-driven taxonomy redesign is recommended for the intent layer (add bus-specific intents) and for the DATE/TIME decision rules (specify Ge'ez calendar handling and Ethiopian clock disambiguation). — _Sources: DATASET-D30, DATASET-D11_
- **OO-5**: Documented issues: missing bus intents harm content validity; Gregorian-only DATE/TIME decision rules harm structural validity for Ethiopian temporal expressions. — _Sources: Q39, Q153, Q154_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q119] 'After merging similar or low-frequency types during data preprocessing in Section 3.3, it was reduced to 23 distinct slot types' (p.13)
- [Q144] 'ACCOUNT_TYPE, ARTIST_NAME, BANK_NAME, BILL_TYPE, CALENDAR_EVENT, CITY_OR_PROVINCE, COUNTRY, CURRENCY, DATE, ... TIME' (p.19)
- [Q153] 'Anything that is less than one day should be annotated as TIME and not DATE' (p.21)
- [Q154] 'Anything that is more than one day must be annotated as DATE and not time' (p.21)

*Web sources:*
- [WEB-9] INJONGO GitHub — 23-slot ontology in annotation prompts confirmed

*Dataset analysis:*
- DATASET-D2, D6: Ge'ez month names accepted as DATE slot values empirically
- DATASET-D15, D16, D28: Most DATE slot values are relative expressions rather than named Ethiopian months
- DATASET-D11, D23: Ethiopian clock TIME values either unannotated or ambiguous
- DATASET-D30: Travel intent set excludes bus operator and seat-class flows

</details>

**Information gaps:**
- Whether the annotation guide (full Appendix) includes any Ge'ez calendar examples beyond the verbatim quotes available

**Requires expert verification:**
- Whether 'CALENDAR_EVENT' would accommodate Timkat/Meskel as labels — taxonomy intent unclear from documentation

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Annotation methodology is sound on its face: ≥3 native annotators per utterance with majority voting [Q42, Q45], Fleiss' Kappa improving to 0.912–1.00 after a two-round review [Q47, Q48], with Amharic specifically reaching κ=0.933 post-review (initial 0.836). However, several documented and empirical gaps reduce convergent validity for this deployment: (a) annotator regional/L2 demographics within Ethiopia are undisclosed [Q44, gap-4 NOT FOUND]; (b) the actual user population includes L2 Amharic speakers from Oromia, Tigray, and SNNP regions who code-switch — a population mismatch flagged HIGH in elicitation; (c) dataset inspection reveals concrete annotation gaps (empty spans on utterances containing clear DATE/TIME content [DATASET-D11, D33], inconsistent treatment of '12 ሰአት' across alarm utterances [DATASET-D11 vs D23], misannotated PERSONAL_NAME in Oromo [DATASET-D29]); (d) no code-switched utterances at all in 19 Amharic samples [DATASET-D1–D18]. OC was marked HIGH priority in elicitation, so these residuals weigh heavily.

**Strengths:**
- Native-speaker annotation with three annotators and majority voting [Q42, Q45]
- Two-round review process raised inter-annotator agreement substantially [Q47, Q48, Q109]
- Amharic post-review κ=0.933, second-highest among all initial scores [WEB-17]
- Detailed annotation guide with edge-case rules [Q149, Q156, Q157]

**Checklist:**

- **OC-1**: Partially. Native Amharic annotators were used [Q7], but their regional/L2 representativeness for the actual deployment user base (multi-regional, L2-heavy) is undisclosed [Q44]. — _Sources: Q7, Q44_
- **OC-2**: Likely disagreement on (a) code-switched utterances (absent from training entirely), (b) Ethiopian time convention, (c) regional toponyms beyond major cities. Demographic profile of annotators is not published. — _Sources: DATASET-D1, DATASET-D11, WEB-3_
- **OC-3**: Documentation specifies 'native speakers' [Q7] and recruitment via a Kenyan logistics company [Q44]. No demographic breakdown by region, urban/rural, age, or L1/L2 status is provided. — _Sources: Q7, Q44_
- **OC-4**: Re-annotation by a representative pool (including non-Addis L2 speakers and code-switching annotators) is recommended given the deployment's user heterogeneity. — _Sources: WEB-3_
- **OC-5**: Majority voting [Q45] is used. With three annotators and absence of demographic diversity controls, minority regional perspectives may be erased; the review process explicitly resolved disagreement toward consistency [Q53, Q109]. — _Sources: Q45, Q53, Q109_
- **OC-6**: Documented issues: undisclosed demographics, observed annotation gaps in Amharic [DATASET-D11, D33], absence of code-switched data — all harming convergent and external validity. — _Sources: DATASET-D11, DATASET-D33, DATASET-D29_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q7] 'utterances generated by native speakers across diverse domains' (p.1)
- [Q42] 'Each utterance was annotated by three annotators so that we could check for agreement in the slot annotations.' (p.4)
- [Q44] 'all recruited participants received an appropriate remuneration based on the per-country rate decided by our logistics company in Kenya.' (p.4)
- [Q45] 'a majority voting system with a minimum of three annotators per sentence to resolve disagreements.' (p.4)
- [Q48] 'agreement scores improved markedly across all languages, reaching 0.912-1.00.' (p.4)
- [Q53] 'ambiguous slot types significantly impacted annotation quality and introduced unnecessary complexity.' (p.4)
- [Q109] 'requiring two rounds of review to achieve consistent quality.' (p.9)

*Web sources:*
- [WEB-17] INJONGO Table 8 — Amharic initial κ=0.836, post-review κ=0.933
- [WEB-3] Amharic L2 lingua-franca status — most learned second language across Ethiopia

*Dataset analysis:*
- DATASET-D11: Amharic alarm utterance with empty spans despite containing 'ነገ' (tomorrow) and '12 ሰአት' (12 o'clock) — annotation gap
- DATASET-D33: Amharic calendar_update with empty spans despite birthday calendar event content
- DATASET-D23: Same utterance type annotated inconsistently across two examples — '12 ሰአት' once unannotated, once with TIME slot
- DATASET-D29: Oromo PERSONAL_NAME 'caalaa' likely misannotated from 'galgala caalaan' phrase
- DATASET-D1–D18: No code-switched Amharic utterances in any sample — annotator pool/methodology did not produce them

</details>

**Information gaps:**
- Annotator demographics within Ethiopia (region of origin, urban/rural, L1/L2 Amharic, age, education)
- Number of annotators recruited for the Amharic split specifically
- Whether any annotation review was performed by Ethiopian regional sub-population

**Requires expert verification:**
- Native Amharic speaker review of suspected misannotations and empty-span examples to confirm rate of annotation gaps

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output is intent class (closed 40-class label) plus structured slot-tag spans in $$-delimited text [Q145, Q146], scored with accuracy and F1 [Q84]. This matches the deployment's task-oriented dialogue NLU output requirements directly. Best fine-tuned models reach 93.7% intent accuracy / 85.6% F1 [Q19, Q78], setting an upper bound; Amharic-specific scores are reported in Table 5 (per-language) but not extracted in registry — gap noted. One minor concern: the eng config used for cross-lingual transfer contains lossy transliterations of Ethiopian entities (e.g., 'Dashen' → 'dasion') [DATASET-D34], which slightly degrades cross-lingual transfer evaluation quality. OF was marked LOWER priority and substantively the form fits.

**Strengths:**
- Structured intent + slot-tag output format directly matches deployment NLU module requirements [Q145, Q146]
- Accuracy and F1 metrics appropriate for closed-class intent and span-based slot evaluation [Q84]
- Amharic post-review annotation quality high (κ=0.933) [WEB-17]

**Checklist:**

- **OF-1**: Yes — text-based intent class + slot-tag output exactly matches deployment NLU module needs [Q145, Q146]. — _Sources: Q145, Q146_
- **OF-2**: TTS not relevant — deployment is text-based smartphone app. — _Sources: Q84_
- **OF-3**: Smartphone-app users are positively selected for literacy [WEB-4 ~15% smartphone ownership]; text output is appropriate. National literacy ~71% [WEB-1, WEB-2] is lower than the smartphone-using subset, but for the deployment's user segment text output is suitable. — _Sources: WEB-4_
- **OF-4**: Minor: lossy transliteration of Ethiopian entities in the eng config [DATASET-D34] could weaken cross-lingual transfer evaluation but does not affect direct Amharic deployment evaluation. — _Sources: DATASET-D34_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q19] 'fine-tuning baselines could reach an accuracy of 93.7% and F1-score of 85.6 for intent detection and slot-filling tasks respectively.' (p.2)
- [Q84] 'Evaluation is based on accuracy and F1-score for ID and SF tasks.' (p.7)
- [Q145] 'Please ensure that the entities match the listed types and that unstated entities should not be included in the response if no entities are found, return $$ only.' (p.19)
- [Q146] 'Output: PERSONAL_NAME John $$ CITY_OR_PROVINCE Paris $$ MONEY 100 $$ RESTAURANT_NAME Awater' (p.19)

*Web sources:*
- [WEB-4] Ethiopia smartphone ownership ~15% — text-based output appropriate for app user segment
- [WEB-17] Amharic post-review κ=0.933 supports output reliability

*Dataset analysis:*
- DATASET-D34: 'Dashen Bank' transliterated as 'dasion bank' in eng config — cross-lingual transfer source quality concern

</details>

**Information gaps:**
- Amharic-specific intent accuracy and slot F1 from Table 5 of the paper not directly extracted

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** INJONGO's 40-intent travel taxonomy is air-travel framed and lacks intercity bus operator flows (seat-class, rebooking, holiday-surge)

**Recommendation:** Define a deployment-specific intent supplement (~10–15 intents) drawn from Sky Bus / Selam Bus / Ride API surfaces; collect 50–100 Amharic utterances per intent via native speaker elicitation following INJONGO's methodology; treat this as a required held-out evaluation alongside INJONGO's travel domain.

### Input Content ⚠

**Gap:** Ethiopian Birr (ETB) absent as CURRENCY/MONEY slot in sampled Amharic; most DATE slots use relative expressions rather than named Ge'ez months; Ethiopian clock convention undocumented; no code-switched utterances

**Recommendation:** Construct a 'ETH-Travel-Slot Stress Set' of Amharic utterances densely populated with (a) Birr fare amounts (VIP/economy tiers), (b) Ge'ez calendar month names across all 13 months including Pagume, (c) Ethiopian-clock TIME values with explicit annotator convention, (d) code-switched Amharic–Oromo and Amharic–Tigrinya tokens for cities and booking terms; evaluate alongside INJONGO Amharic test.

### Input Content ⚠

**Gap:** Annotation gaps observed empirically (empty spans on temporally explicit utterances)

**Recommendation:** Run a targeted audit pass over Amharic train/dev/test for empty-span utterances containing temporal lexemes ('ሰአት', 'ጠዋት', 'ነገ', Ge'ez month names) and patch with corrected annotations before using F1 as a model-selection metric.

### Output Content ⚠

**Gap:** Annotator regional/L2 demographics within Ethiopia undisclosed; observed annotation gaps (empty spans on utterances with clear DATE/TIME content); no code-switched data ever annotated

**Recommendation:** Recruit a regionally diverse annotator pool — explicitly including non-Addis annotators from Amhara, Oromia, Tigray, SNNP, and Somali regions, with documented L1/L2 status — and re-annotate a stratified sample (~500 utterances) of the Amharic INJONGO test split plus a new code-switched mini-set; report κ stratified by annotator subgroup.

### Output Form

**Gap:** Lossy transliteration of Ethiopian entities in the eng config used for cross-lingual transfer (e.g., Dashen Bank → 'dasion')

**Recommendation:** If using INJONGO's English split as a cross-lingual source, normalize transliterations of Ethiopian named entities to standard English spellings (Dashen Bank, Awash Bank, Abay Bank) before training; otherwise prefer in-language SFT.

### Output Ontology

**Gap:** DATE/TIME annotation rules implicitly Gregorian/international; no documented decision rule for Ge'ez calendar or Ethiopian 6-hour-offset clock; no intent categories for bus-specific flows

**Recommendation:** Author a Ge'ez-calendar and Ethiopian-clock annotation addendum to the INJONGO guide, specifying acceptable surface forms for each Ge'ez month, intercalary Pagume handling, and disambiguation rules for ambiguous TIME expressions; add bus-specific intents to the operative ontology for downstream evaluation.

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

### Dataset Analysis

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

