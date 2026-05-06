## Deployment Context

**Use case:** Educational tutoring and supporting students studying with answers related to their curriculums in different subjects on the primary, middle, and high school, level as well as some university level subjects (management, economics, law, CS, political science, accounting)
**Target population:** Students (primary, middle, high school, and university) from Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, or KSA.

# Validity Analysis: arabicmmlu
**Target context:** MENA Multi-Country Arabic Tutoring System — Eight-Country Curriculum Deployment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 3 | Moderate gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology | 3 | Moderate gaps | high |
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

ArabicMMLU is the only large-scale natively-sourced Arabic exam benchmark available and is genuinely better-suited for MENA evaluation than translated MMLU alternatives [Q5, Q6]. For the deployment's MSA school-level STEM coverage and overall MCQ format alignment, it provides meaningful and trustworthy signal. However, for the deployment's eight-country curriculum-alignment requirement, ArabicMMLU has serious validity limitations that the dataset analysis confirms empirically rather than merely speculatively. The most acute concerns are content-level (IC) and label-correctness (OC): Jordanian-curriculum civics, history, social science, and economics content is encoded as universal ground truth across school levels [DATASET-D1–D7, D20–D22, D25, D30]; university-level non-CS subjects come almost exclusively from a single Egyptian university [DATASET-D39, D40]; Law (Professional) is exclusively Moroccan procedural law in the sample [DATASET-D8–D10, D34]; Kuwait has no observed examples and no documented annotators [Q31, Q96]; Palestinian content (top-three contributor by volume) was verified without Palestinian annotators [Q96, WEB-1]. The flat label schema [Q27] cannot encode jurisdiction-specific correctness despite the deployment user explicitly requiring per-country legal tailoring [elicitation A2]. University-level coverage is also structurally thin (~6.1% [Q71]) for a deployment serving university students.

## Practical Guidance

### What This Benchmark Measures

ArabicMMLU can validly measure: (a) MSA reading comprehension and Arabic grammar at school level (input_form score 4); (b) MCQ-format scoring alignment for the deployment's primary use case (output_form score 4); (c) STEM factual recall across all eight countries since STEM content is curriculum-neutral [DATASET-D24]; (d) Jordanian school-curriculum knowledge specifically (the dominant cohort); (e) some Egyptian university accounting/economics/management/political science alignment, subject to OCR caveats; (f) Moroccan procedural law specifically. The benchmark also supports rough comparative evaluation of model robustness across prompt/output configurations [Q47, Q105–Q110].

### Construct Depth

Construct depth is shallow for the deployment's stated needs. The benchmark probes factual recall and modest reasoning at primary/middle/high school levels well, but university-level depth is thin (~6.1% of items, ~889 questions across all subjects [Q71]). Country-specific construct depth is highly uneven: Jordan is over-probed, Kuwait is essentially un-probed, Morocco is probed only in law and a few Arabic items, Palestine is probed in STEM but not verified by Palestinian experts. Madhab-specific Islamic studies depth is undocumented [gap_id 7]. Jurisdiction-specific legal depth is single-jurisdiction in the sample [DATASET-D34]. Construct depth strengths are concentrated in dimensions input_form and output_form; depth weaknesses are concentrated in input_content and output_content — the dimensions the elicitation marked HIGH priority.

### What Else You Need

For a defensible deployment, ArabicMMLU should be supplemented with: (1) per-country re-annotation of civics, history, social science, economics, and law subsets by curriculum experts from Morocco, Kuwait, Palestine, UAE (addresses input_content and output_content gaps); (2) ArabLegalEval [WEB-3] for Saudi-specific law and MizanQA [WEB-4] for additional Moroccan law coverage, with a custom evaluation built for Egyptian/UAE/Jordanian/Lebanese/Kuwaiti/Palestinian legal jurisdictions which remain unfilled; (3) AraSTEM [WEB-2] for richer STEM coverage at university level (addresses input_ontology thinness); (4) a French-Arabic bilingual evaluation for Moroccan university science (no existing benchmark, must be built [gap_id 6]); (5) madhab-stratified Islamic studies evaluation built with Maliki and Hanbali curriculum experts [gap_id 7]; (6) cleaning or replacement of OCR-corrupted Management and Political Science (University) items [DATASET-D14, D15, D29].

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
ArabicMMLU's taxonomy of 40 tasks across STEM, Social Science, Humanities, Arabic Language, and Other [Q25, Q107], spanning primary through university levels, broadly matches the deployment's educational tiers and subject scope. All six university subjects required by the deployment (law, CS, management, economics, political science, accounting) are confirmed present in the benchmark configurations [DATASET-D8, D11, D13, D14, D16]. However, university-level questions constitute only ~6.1% of the benchmark [Q71], yielding roughly ~889 questions spread across all university subjects — thin coverage for a deployment that explicitly targets university students. Country coverage at the ontology level is structurally uneven: Jordan dominates with over 6,000 questions while some countries contributed 'as few as 100 or, in some cases, none at all' [Q89]. Several configurations have null country/level metadata [DATASET-D26, D27], limiting their use for country-specific diagnostics. The taxonomy includes no madhab labeling for Islamic studies and no jurisdiction-specific branching for law, both flagged as HIGH-priority deployment requirements.

**Strengths:**
- All six deployment-required university subjects are present as queryable configurations [DATASET-D8, D11, D13, D14, D16]
- Multi-level coverage (primary, middle, high school, university) is empirically confirmed in the data [DATASET-D5, D13, D21]
- Subject taxonomy explicitly includes country-variation-prone subjects: history, geography, civics, political science [Q72, Q73]
- Negation is treated as a distinct linguistic phenomenon [Q83, Q84], providing some construct depth beyond factual recall

**Checklist:**

- **IO-1**: Required categories include MSA-medium primary/middle/high school content for Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, KSA across STEM, humanities, civics, Islamic studies, Arabic language; plus university-level coverage for law, CS, management, economics, political science, accounting [elicitation A1, A2]. — _Sources: Q25, Q107_
- **IO-2**: Several regionally-relevant categories are omitted or thinly covered: madhab-specific Islamic studies tracks (Maliki for Morocco, Hanbali for KSA) have no labeling [gap_id 7]; jurisdiction-specific law branches are absent (flat label schema [Q27]); Kuwaiti civic/national content appears absent — no Kuwaiti workers documented [Q31, Q96] and no Kuwaiti examples observed in data sample [DATASET content summary]; French-medium Moroccan university science content is fully out of scope [Q92]. — _Sources: Q27, Q31, Q89, Q92, Q96, WEB-1, WEB-4_
- **IO-3**: Some included categories are not directly relevant to all deployment cohorts: 'Driving Test' configuration [DATASET-D35] is not a tutoring subject; null-country generic Islamic Studies and Arabic Language items [DATASET-D26, D27] cannot be used for country-stratified evaluation. These are not harmful inclusions per se but contribute construct-irrelevant variance to aggregate scores. — _Sources: DATASET-D26, DATASET-D27, DATASET-D35_
- **IO-4**: Documented gaps: (a) university-level coverage at ~6.1% [Q71] is structurally thin for a deployment serving university students; (b) no madhab calibration [gap_id 7]; (c) no jurisdiction-specific law taxonomy [Q27, gap_id 4]; (d) Kuwait coverage likely near-zero [Q89, Q96]; (e) French-medium Moroccan content fully absent [Q92]. — _Sources: Q71, Q89, Q92, WEB-1, WEB-4_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q25] 'ArabicMMLU is an Arabic multiple-choice question-answering dataset comprising 40 tasks spanning a wide range of subjects and education levels.' (p.3)
- [Q71] 'This could be attributed to the relatively small portion (i.e., 6%) of university-level questions in ArabicMMU' (p.7)
- [Q89] 'ArabicMMLU does not represent all Arabic countries equally. For example, we have collected over 6K multiple-choice questions from Jordan, while other countries are represented with only 100 questions or, in some cases, not at all.' (p.9)
- [Q92] 'The dataset primarily focuses on Modern Standard Arabic (MSA).' (p.9)
- [Q107] 'Table 9 presents results organized by subject groups: STEM, Social Science, Humanities, Arabic Language, and Other.' (p.16)

*Web sources:*
- [WEB-1] ArabicMMLU paper Figure 1 lists Jordan, Egypt, and Palestine as top-three contributors; Kuwait not mentioned in acknowledgments
- [WEB-4] Arabic LLM benchmark survey confirms structural geographic bias toward Saudi/Gulf, with Kuwait remaining underrepresented across 40+ benchmarks
- [WEB-3] ArabLegalEval uses ~299 ArabicMMLU law questions and ~195 political science questions as baselines, confirming subset sizes

*Dataset analysis:*
- DATASET-D8, D9, D10, D34: All sampled Law (Professional) questions are exclusively from Morocco, single Google Drive PDF source — no observed multi-jurisdictional law branches
- DATASET-D26: Islamic Studies (All) configuration has Country=null, Source=folderat.com — no curriculum or madhab attribution
- DATASET-D27: Arabic Language (General) has Country=null, Source=madinaharabic.com — generic non-curriculum source
- DATASET-D35: Driving Test contains country-specific UAE and Lebanese traffic rules — narrow but country-stratified
- DATASET content summary: No Kuwait examples observed in any sampled configuration outside zero-coverage assumption

</details>

**Information gaps:**
- Exact per-country question counts beyond Jordan (>6,000) are not text-published [gap_id 5]
- Madhab calibration of Islamic studies questions is undocumented anywhere [gap_id 7]
- Jurisdictional distribution of law questions beyond Moroccan procedural law sample is unknown

**Requires expert verification:**
- Whether observed Moroccan-only Law (Professional) sample generalizes to the full ~299 law questions or whether other configurations contain embedded jurisdiction-specific content
- Whether Islamic Studies configurations contain madhab-specific fiqh that would diverge across Maliki/Hanbali/Shafi'i traditions

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Content-level validity is the dimension where ArabicMMLU diverges most sharply from the deployment's eight-country requirement. While the benchmark's content is sourced from real native Arabic exams [Q1, Q26] — a clear strength over translated alternatives [Q5, Q6] — the empirical content distribution is heavily skewed: civics, social science, history, and economics at school level are dominated by Jordanian-specific institutional, royal, and constitutional content presented as universal curriculum knowledge [DATASET-D1, D2, D3, D4, D5, D6, D7, D20, D21, D22, D25, D30, D31]. University-level economics, accounting, management, and political science come exclusively from a single Egyptian university (Assiut University) in the sample [DATASET-D13, D14, D28, D39, D40], and Law (Professional) is exclusively Moroccan in the observed sample [DATASET-D8, D9, D10, D34]. The deployment user explicitly requires country-specific tailoring for law [elicitation A2] and curriculum-aligned content for each of the eight countries [elicitation A1]. Kuwait has no observed examples and no documented annotators [Q31, Q96]; Morocco has no documented annotators [Q31, Q96]. Egypt-specific currency (جنيه) appears in university economics presented as universal [DATASET-D28]. The benchmark's own admission that countries are represented unequally [Q89] is empirically confirmed and amplified by the dataset analysis: rather than uniform under-coverage, the data shows Jordanian-curriculum content is propagated as default for non-Jordanian cohorts. This generates substantial construct-irrelevant variance for Moroccan, Emirati, Kuwaiti, Saudi, Lebanese, and Palestinian students.

**Strengths:**
- Native exam provenance avoids translation artifacts that plague competing Arabic benchmarks [Q5, Q6]
- STEM content (math, biology, physics, CS factual) is genuinely curriculum-neutral and reliable across all eight countries [DATASET-D24]
- Palestine is substantively represented in STEM subjects (Biology HS, CS Primary, Math Primary) [DATASET-D23, D24]
- Some Moroccan legal content is present, even if narrow [DATASET-D8, D9, D10]
- Native annotators and exam URLs document content provenance per question [Q32, Q33]

**Checklist:**

- **IC-1**: Inputs heavily require region-specific knowledge but the regions covered diverge from the deployment's eight-country target. Civics and history items reference Jordanian royal lineage, the 1952 Jordanian constitution, Jordan's Royal Medical Services, and Central Bank of Jordan URLs as universal facts [DATASET-D1, D2, D4, D5, D6, D20, D21, D25, D31]. University accounting and economics use Egyptian institutional and currency context [DATASET-D28, D39, D40]. Law uses Moroccan procedural code [DATASET-D8, D9, D10]. — _Sources: DATASET-D1, DATASET-D2, DATASET-D4, DATASET-D5, DATASET-D6, DATASET-D20, DATASET-D28, DATASET-D34_
- **IC-2**: Cultural-content alignment is partial. Islamic studies content observed (Hadith ethics, Quran recitation etiquette) appears broadly Sunni-consistent, aligning with the deployment's predominantly Sunni population [DATASET-D17, D37, D38]. However, no madhab calibration exists [gap_id 7], and Hanbali/Maliki specificity is not verified. Politically sensitive content (e.g., King Abdullah I and Zionism [DATASET-D31]) is framed in Jordanian national narrative — potentially misaligned with Palestinian, Lebanese, or other framings. — _Sources: DATASET-D17, DATASET-D31, DATASET-D37, DATASET-D38_
- **IC-3**: Western-specific knowledge is largely avoided due to native exam sourcing [Q5, Q6]. The primary content-validity threat is not Western bias but intra-regional bias — Jordanian and Egyptian content dominating non-Jordanian/non-Egyptian cohorts. — _Sources: Q5, Q6_
- **IC-4**: Annotators are exclusively from Jordan, Egypt, Lebanon, UAE, KSA [Q31] — Morocco, Kuwait, Palestine have no documented annotators despite (in Palestine's case) contributing top-three question volume [Q96, WEB-1]. Recruiting Kuwaiti, Moroccan, and Palestinian curriculum experts would be essential for any deployment use. — _Sources: Q31, Q96, WEB-1_
- **IC-5**: Documented content issues harming validity: (a) Jordanian-default civics/history/social science presented as universal [DATASET-D1, D2, D4, D21]; (b) single-Egyptian-university dominance of university social science subjects [DATASET-D39, D40]; (c) single-source single-jurisdiction Law (Professional) [DATASET-D34]; (d) no Kuwait content observed; (e) Egypt-specific currency in 'general' economics [DATASET-D28]; (f) French-medium Moroccan university content absent [Q92]. — _Sources: Q89, Q92, DATASET-D1, DATASET-D34, DATASET-D39, DATASET-D40_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'we present ArabicMMLU, the first multi-task language understanding benchmark for the Arabic language, sourced from school exams across diverse educational levels in different countries' (p.1)
- [Q26] 'The questions are sourced from eight different countries in North Africa (Morocco and Egypt), the Levant (Jordan, Palestine, and Lebanon), and the Gulf (UAE, Kuwait, and KSA).' (p.3)
- [Q31] 'a total of 10 Arabic native speakers from different countries: 6 internal workers (1 Jordanian, 1 Egyptian, 1 Lebanese, 1 from UAE, and 2 from KSA) and 4 external workers (3 Jordanian and 1 Egyptian)' (p.4)
- [Q89] 'we have collected over 6K multiple-choice questions from Jordan, while other countries are represented with only 100 questions or, in some cases, not at all.' (p.9)
- [Q90] 'This is largely due to the availability of publicly-accessible exams in each country' (p.9)
- [Q96] 'We extend our gratitude to all collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia' (p.10)

*Web sources:*
- [WEB-1] ArabicMMLU Figure 1 confirms Jordan/Egypt/Palestine as top-three contributors; Morocco and UAE among lower contributors
- [WEB-1] Models perform notably poorly on Morocco- and UAE-sourced questions in country-stratified analysis
- [WEB-3] ArabLegalEval is Saudi-only; does not fill multi-jurisdictional legal content gap

*Dataset analysis:*
- DATASET-D1: Civics HS asks 'manifestations of change in modern Jordanian society' — Jordan-specific framed as general curriculum
- DATASET-D2: Jordanian 1952 coalition government question framed as standard middle-school civics
- DATASET-D6: Economics HS gives Central Bank of Jordan URL (cbj.gov.jo) as exam answer
- DATASET-D7: 67% Jordanian financial-exclusion statistic embedded as universal economics fact
- DATASET-D21: Primary social science teaches reign of Jordanian King Talal as factual content
- DATASET-D28: University economics uses Egyptian pounds (جنيه) in ROI calculations
- DATASET-D34: All 5 sampled Law (Professional) questions from Morocco, single PDF source
- DATASET-D39, D40: All sampled Accounting and Economics (University) from Assiut University Egypt
- DATASET-D31: Jordanian-narrative framing of King Abdullah I and Zionism — politically sensitive cross-country variation

</details>

**Information gaps:**
- Whether Jordanian dominance in civics/history/social science extends to the full benchmark or is concentrated in specific level/subject configurations [gap_id 5]
- Whether Law subset beyond the sampled Moroccan questions includes other jurisdictions [gap_id 4]
- Madhab-specific framing in Islamic studies is undocumented [gap_id 7]

**Requires expert verification:**
- Per-country curriculum review by national-curriculum experts from Kuwait, Morocco, Palestine, UAE to identify questions presented as 'universal' that are actually national-curriculum-specific
- Islamic studies curriculum experts to assess madhab calibration risk for Moroccan Maliki and Saudi Hanbali contexts

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input form aligns well with the deployment. All 14,575 questions are MSA [Q2], matching the formal medium of instruction across all eight target countries [Q29]. The text-only, MCQ format with embedded contextual passages [Q37, Q38] is exactly the deployment's primary use case. Arabic-script fidelity is empirically confirmed [DATASET-D24, D25]. The MSA-only scope appropriately excludes Darija (which the deployment explicitly excludes) and dialectal Arabic [Q92]. The main form-level gap is French-medium Moroccan university content [Q92], which the deployment user explicitly identified as in-scope for Moroccan university science programs [elicitation A4]. A secondary form concern is OCR corruption observed in Management and Political Science (University) questions from Egyptian PDF sources [DATASET-D14, D15, D29], which compromises the input signal quality for those configurations. A minor anomaly is one Arabic Grammar question with English-language stem [DATASET-D19].

**Strengths:**
- MSA throughout matches the formal medium of instruction in all eight countries [Q2, Q29]
- MCQ + 2–5 options format directly matches deployment's primary use case [Q27]
- Text-only modality matches the deployment's text-based interface [Q93, infrastructure section]
- Contextual passages bundled with dependent questions [Q38] preserves single-shot evaluability

**Checklist:**

- **IF-1**: Signal distributions align: MSA Arabic text input matches the deployment's text-based interface and matches the formal language of instruction across all eight countries [Q2, Q29]. No image/audio mismatch since both the benchmark and deployment exclude multimodal content [Q37, Q93]. — _Sources: Q2, Q29_
- **IF-2**: Regional infrastructure supports text-based delivery: ITU 2024 data shows ~100% internet penetration in UAE/KSA/Kuwait [WEB-8], ~83-88% in Levant per Arab Barometer [WEB-10], and majority mobile-dominant access across all eight [WEB-11]. Mobile-dominant access is compatible with text MCQ delivery. — _Sources: WEB-8, WEB-10, WEB-11_
- **IF-3**: Domain-specific form gap: French-medium Moroccan university science content is entirely outside benchmark scope [Q92]; deployment explicitly identifies this as in-scope for Moroccan universities [elicitation A4]. No companion benchmark identified [gap_id 6]. Additionally, OCR corruption in some Egyptian-sourced university PDFs [DATASET-D14, D15, D29] degrades input form for those subjects. — _Sources: Q92, DATASET-D14, DATASET-D15, DATASET-D29_
- **IF-4**: Documented form mismatches: (a) French-medium Moroccan university content absent [Q92, gap_id 6]; (b) OCR-corrupted text in Management and Political Science university questions [DATASET-D14, D15, D29]; (c) one English-stem grammar question [DATASET-D19]; (d) several configurations have null country/level metadata limiting form-level diagnostics [DATASET-D26, D27]. — _Sources: Q92, DATASET-D14, DATASET-D15, DATASET-D19, DATASET-D26, WEB-4_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q2] 'Our data comprises 40 tasks and 14,575 multiple-choice questions in Modern Standard Arabic (MSA)' (p.1)
- [Q29] 'In public schools, Arabic is commonly used for teaching and assessment' (p.3)
- [Q37] 'workers were instructed to include only questions accompanied by an answer key, and to discard questions containing multi-modal information' (p.4)
- [Q38] 'If a question had additional contextual information (e.g., a passage referenced by several questions), the context was required to be included with each corresponding question.' (p.4)
- [Q92] 'The dataset primarily focuses on Modern Standard Arabic (MSA).' (p.9)
- [Q93] 'ArabicMMLU is focused solely on text-based assessment' (p.9)

*Web sources:*
- [WEB-8] World Bank/ITU 2024: UAE/KSA/Kuwait at ~100% internet penetration
- [WEB-11] ITU 2025: 83% mobile ownership in Arab States; mobile-dominant access patterns
- [WEB-10] Arab Barometer 2020: ~84% Jordanian, ~83% Palestinian, ~88% Lebanese internet usage
- [WEB-4] Arabic LLM benchmark survey confirms no French-Arabic bilingual benchmark for Moroccan higher education exists

*Dataset analysis:*
- DATASET-D14, D15: Severe OCR corruption in Management (University) — answer options unreadable
- DATASET-D29: OCR-distorted Political Science (University) text
- DATASET-D19: Single English-stem question in Arabic Grammar configuration
- DATASET-D24, D25: Confirmed clean MSA in Biology HS and Civics HS

</details>

**Information gaps:**
- Total proportion of OCR-corrupted questions in Management and Political Science (University) configurations is unknown [DATASET limitations §6]

---

### Output Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
The flat single-correct-answer MCQ schema with 2–5 options [Q27] structurally matches the deployment's MCQ tutoring use case, and the user explicitly noted that for MCQ tasks explanation format is not exam-critical [elicitation A3]. This is a meaningful structural alignment. However, the schema provides no mechanism for jurisdiction-specific or country-specific correct answers. The deployment user explicitly stated 'the system must tailor legal answers to each country's specific legal system' [elicitation A2], but the benchmark's flat label structure encodes a single ground-truth answer per question [Q27], with no country-stratified branching. The dataset analysis empirically confirms this: a Moroccan procedural-law answer is simply marked correct without any 'correct-for-Morocco' qualifier [DATASET-D8, D9, D10]. For civics, history, and law subjects where correct answers legitimately vary by country, this schema cannot represent the variation the deployment requires. The benchmark does provide country, subject, and level metadata fields per question [Q33], which would in principle allow country-stratified scoring — but this is a metadata affordance rather than a label-schema accommodation, and the metadata is null for some configurations [DATASET-D26, D27].

**Strengths:**
- Flat MCQ schema with 2–5 options [Q27] directly matches deployment's MCQ tutoring format
- Country, subject, and level metadata fields are present per question [Q33], enabling country-stratified analysis even without label-schema branching
- Subject-group taxonomy (STEM, Social Science, Humanities, Arabic Language, Other) [Q107] supports diagnostic per-subject reporting
- Education-level stratification (primary, middle, high, university) [Q102, Q103] aligns with the deployment's tier structure

**Checklist:**

- **OO-1**: Output label categories (single correct option from 2–5) are regionally relevant for MCQ tutoring [Q27]; the format itself is appropriate. The categorical label space (A/B/C/D/E or Arabic equivalents [Q51, Q52]) is universally usable. — _Sources: Q27, Q51, Q52_
- **OO-2**: Missing categories: no jurisdiction-specific correct-answer branching for law and civics [Q27], explicitly required by deployment [elicitation A2]; no madhab-specific branching for Islamic studies [gap_id 7]; no mechanism for 'correct in country X but not in country Y' [DATASET-D8, D34]. — _Sources: Q27, DATASET-D8, DATASET-D34_
- **OO-3**: The Driving Test configuration encodes country-specific traffic regulations as correct answers [DATASET-D35] — a positive example of country-tied ground truth, but applied inconsistently across other subjects where country variation also exists. — _Sources: DATASET-D35_
- **OO-4**: Stakeholder-driven taxonomy redesign would benefit law and civics subsets to add jurisdiction tags. This is feasible given existing per-question country metadata [Q33] but not implemented in the published label schema. — _Sources: Q33_
- **OO-5**: Documented taxonomy issues harming structural validity: (a) no jurisdiction tagging in label schema for law [DATASET-D34]; (b) Jordanian-default civics presented as universal [DATASET-D1, D2]; (c) no madhab labeling [gap_id 7]; (d) null country metadata for several configurations [DATASET-D26, D27]. — _Sources: DATASET-D1, DATASET-D2, DATASET-D26, DATASET-D27, DATASET-D34_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q27] 'Each question has 2–5 candidate answers, with one correct answer.' (p.3)
- [Q33] 'collect metadata, including the source (URL of the source document), country, subject, level, question, multiple-choice options, and the correct answer key.' (p.4)
- [Q102] 'Table 8 presents the detailed zero-shot results across subjects and education levels' (p.15)
- [Q107] 'Table 9 presents results organized by subject groups: STEM, Social Science, Humanities, Arabic Language, and Other.' (p.16)

*Web sources:*
- [WEB-3] ArabLegalEval reuses ArabicMMLU law subsets without jurisdiction tagging — confirms multi-jurisdiction gap is structural
- [WEB-13] ALARB 2025 confirms Arabic legal evaluation is moving toward open-ended reasoning beyond MCQ — suggests MCQ schema limits even within Arabic legal NLP

*Dataset analysis:*
- DATASET-D8, D9, D10, D34: Moroccan-only Law sample with no jurisdiction tag in label schema
- DATASET-D35: Driving Test does encode country-specific traffic rules as correct answers — counter-example showing country-tied ground truth is technically feasible
- DATASET-D26, D27: Null country metadata in some configurations limits diagnostic stratification

</details>

**Information gaps:**
- Whether per-question country metadata is consistently populated across the full dataset (sample shows null for Islamic Studies All and Arabic Language General [DATASET-D26, D27])

**Requires expert verification:**
- Whether subject-matter experts in law and civics deem the existing single-answer schema redeemable through metadata-stratified evaluation, or whether label-schema redesign is required

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Output content (label correctness for the deployment context) is the dimension most exposed to validity violations. The 96% spot-check agreement [Q43, Q44] was conducted on 100 randomly sampled questions [Q42] without country stratification, so it cannot speak to per-country annotation quality. Annotators are exclusively from Jordan, Egypt, Lebanon, UAE, and KSA [Q31] — Morocco, Kuwait, and Palestine have no documented annotators [Q96], yet Palestine is a top-three question contributor [WEB-1] and Moroccan law content is present [DATASET-D34]. This means Palestinian, Moroccan, and Kuwaiti questions (where present) had ground-truth labels verified by workers from other national educational contexts. Empirically, the dataset analysis shows: (a) Jordanian-curriculum facts (King Talal's reign, 1952 constitution, Royal Medical Services, CBJ URL) are encoded as universally correct answers [DATASET-D3, D4, D7, D20, D21]; (b) Egypt-specific currency and institutions are encoded as universal in university economics [DATASET-D28, D39, D40]; (c) Moroccan procedural law is encoded as 'the' law answer without jurisdiction tag [DATASET-D8, D9, D10, D34]; (d) at least one likely-incorrect ground-truth label is observed [DATASET-D32]; (e) OCR-corrupted questions [DATASET-D14, D15] cannot have reliably verifiable answer keys. Pretraining contamination is also acknowledged as not ruled out [Q94, Q95]. For a deployment that requires curriculum-aligned answers per country [elicitation A1] and country-specific legal correctness [elicitation A2], the ground-truth labels do not reliably reflect regional stakeholder perspectives for Moroccan, Emirati, Kuwaiti, Saudi, Lebanese, or Palestinian cohorts.

**Strengths:**
- Annotator credentials are documented: Master's students/Research Assistants and Bachelor's-degree-holders, all native MSA speakers [Q35, Q39]
- 96% inter-annotator agreement on 100-question spot check provides a baseline quality signal [Q43]
- Compensation exceeded monthly average wages in respective countries [Q36]
- One-hour orientation workshop conducted before data collection [Q40]
- STEM ground truth (math, biology, physics, factual CS) is curriculum-neutral and reliable across all eight countries [DATASET-D24, strength 5]

**Checklist:**

- **OC-1**: Ground-truth labels reflect regional stakeholder perspectives unevenly. For STEM and curriculum-neutral content, labels are reliable across all eight countries. For civics, history, social science, economics, and law, labels reflect the originating exam's jurisdiction without country-stratified validation [DATASET-D1, D7, D34]. — _Sources: DATASET-D1, DATASET-D7, DATASET-D24, DATASET-D34_
- **OC-2**: Disagreement is highly likely between original annotators and regional populations for: (a) Moroccan students reviewing Jordanian civics [DATASET-D1, D2]; (b) UAE/Kuwait students reviewing Egyptian university economics [DATASET-D28]; (c) Egyptian/Saudi/Jordanian/UAE/Kuwaiti/Lebanese/Palestinian law students reviewing Moroccan procedural law [DATASET-D8, D9, D10]; (d) Palestinian students reviewing Jordanian-narrative King Abdullah I content [DATASET-D31]. — _Sources: DATASET-D1, DATASET-D28, DATASET-D31, DATASET-D34_
- **OC-3**: Annotator demographics documented [Q31] but limited: 10 annotators total, all from Jordan/Egypt/Lebanon/UAE/KSA. No Morocco/Kuwait/Palestine representation [Q96]. No formal datasheet or data statement beyond paper text. — _Sources: Q31, Q96_
- **OC-4**: Re-annotation by representative annotators from Morocco, Kuwait, and Palestine is essential before deployment use, especially for civics, history, law, social science, and economics subsets. — _Sources: Q31, Q96, WEB-1_
- **OC-5**: Aggregation: 96% agreement reported as a single global figure [Q43] without country stratification — minority-country perspectives are erased in the aggregate. No formal IAA statistic beyond this [Q43]. — _Sources: Q43, Q44_
- **OC-6**: Documented label issues: (a) Jordanian-curriculum facts as universal ground truth [DATASET-D1, D3, D4, D7, D20, D21]; (b) Egyptian university content as universal [DATASET-D28, D39, D40]; (c) Moroccan-only law ground truth [DATASET-D34]; (d) no Palestinian annotator review of Palestinian content [Q96, WEB-1]; (e) at least one likely-incorrect answer key observed [DATASET-D32]; (f) OCR-corrupted questions where verifiability is compromised [DATASET-D14, D15]; (g) potential pretraining contamination not ruled out [Q94, Q95]. — _Sources: Q94, Q95, DATASET-D14, DATASET-D32, DATASET-D34, DATASET-D39_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] '10 Arabic native speakers from different countries: 6 internal workers (1 Jordanian, 1 Egyptian, 1 Lebanese, 1 from UAE, and 2 from KSA) and 4 external workers (3 Jordanian and 1 Egyptian)' (p.4)
- [Q42] 'we assessed the accuracy of our data collection by having two native Arabic speakers annotate 100 randomly sampled questions' (p.4)
- [Q43] 'We found that 96% of the questions and answer keys match on average, while the remaining could have incorrect answer keys.' (p.4)
- [Q44] 'This 96% score is considered to represent the maximum score meaningfully achievable for ArabicMMLU.' (p.4)
- [Q94] 'our experimental results do not provide conclusive answers regarding the performance of LLMs in Arabic.' (p.9)
- [Q95] 'we cannot assert that the model's pretraining data is free from contamination.' (p.10)
- [Q96] 'We extend our gratitude to all collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia' (p.10)

*Web sources:*
- [WEB-1] Palestine is a top-three contributor by question count yet has no documented annotators
- [WEB-1] Models perform notably poorly on Morocco- and UAE-sourced questions, consistent with thin annotation coverage

*Dataset analysis:*
- DATASET-D3: Jordanian Council of Ministers structure encoded as universal correct answer
- DATASET-D4: Jordanian Hashemite Kingdom constitution as 'the' constitutional answer
- DATASET-D7: Jordan-specific 67% financial-exclusion statistic as universal economic fact
- DATASET-D28: Egyptian-pound calculation as universal university economics ROI
- DATASET-D34: All 5 Law (Professional) answers from Moroccan jurisdiction without tag
- DATASET-D32: Likely-incorrect Social Science (MS) answer key (gas importance attributed to scarcity)
- DATASET-D14, D15: OCR-corrupted answer options where label correctness cannot be verified from text

</details>

**Information gaps:**
- Country-stratified inter-annotator agreement is not reported [Q43]
- Pretraining contamination extent is not measured [Q95]
- Total proportion of incorrect answer keys beyond the 4% noise floor implied by 96% agreement is unknown

**Requires expert verification:**
- Per-country curriculum experts (especially Moroccan Maliki Islamic studies, Kuwaiti civics, Palestinian national history, UAE 4-4-4 curriculum) to re-validate ground-truth labels
- Legal experts from Egypt, UAE, KSA, Jordan, Lebanon, Kuwait, Palestine to assess law-subset jurisdictional correctness

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output form is the strongest dimension for this deployment. Both the benchmark and deployment use single-token MCQ accuracy [Q50, Q53], and the elicitation explicitly confirmed that for MCQ tasks 'explanations are not graded, so any correct explanation adequately supports the student's understanding without exam risk' [elicitation A3]. The benchmark provides multiple prompt-language and output-alphabet configurations [Q47] with detailed per-configuration results [Q105, Q106, Q108, Q110], offering rich diagnostic capacity. Calibration analysis (r > 0.9 between answer probability and accuracy [Q80]) provides additional signal quality. Models are evaluated in zero-shot and few-shot settings across 35 models [Q45, Q46], giving comparative reference points. The remaining concerns are residual: the form does not capture explanation quality (which is acceptable per elicitation A3) and does not evaluate generative tutoring output that the deployment may also produce. Literacy is a non-issue since target users are enrolled students [regional_context literacy section].

**Strengths:**
- Single-token MCQ accuracy directly matches deployment's MCQ scoring needs [Q50, Q53]
- Four prompt-language/output-alphabet configurations tested, with per-configuration results published [Q47, Q105, Q106, Q108, Q110]
- Calibration analysis (r > 0.9) confirms answer-probability reliability for open-source models [Q80]
- Per-subject and per-level result breakdowns enable diagnostic targeting [Q102, Q103]

**Checklist:**

- **OF-1**: Expected output modality (single-letter MCQ answer) matches the deployment's primary MCQ tutoring use case [Q50, Q53; elicitation A3]. The deployment may also need free-form explanations, which the benchmark does not evaluate — but the elicitation confirmed this is non-critical for MCQ contexts [elicitation A3]. — _Sources: Q50, Q53_
- **OF-2**: Text-to-speech is not required by the deployment (text-based interface per regional_context platform_context). Not applicable. — _Sources: WEB-11_
- **OF-3**: Target population is enrolled students with high literacy by definition [literacy_and_educational_attainment note]; mobile-dominant access is documented [WEB-11]. Output form is compatible with regional access patterns. — _Sources: WEB-8, WEB-11_
- **OF-4**: Documented form mismatches are minimal: (a) explanation-quality output is not evaluated, but elicitation confirmed this is acceptable [elicitation A3]; (b) generative tutoring output (e.g., step-by-step explanations) falls outside benchmark scope but is a deployment use case the benchmark does not validate. — _Sources: Q45_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q45] 'Our experiments focus on zero-shot and few-shot settings across 35 models.' (p.5)
- [Q47] 'we initially conducted experiments with four settings: (1) Arabic prompt and Arabic alphabetic output, (2) Arabic prompt and English alphabetic output, (3) English prompt and Arabic alphabetic output, and (4) English prompt and English alphabetic output.' (p.5)
- [Q50] 'for open-source models, we determine the answer based on the highest probability among all possible options.' (p.6)
- [Q53] 'For closed-source models, we determine the answer based on the first token generated in the text using a regular expression.' (p.6)
- [Q80] 'we observe that the three open-source models are well calibrated with correlation scores r > 0.9.' (p.8)
- [Q102] 'Table 8 presents the detailed zero-shot results across subjects and education levels' (p.15)

*Web sources:*
- [WEB-8] ~100% internet penetration in UAE/KSA/Kuwait — text-based output reaches target users
- [WEB-11] 83% mobile ownership in Arab States; mobile-dominant text delivery is feasible

</details>

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** Jordanian-curriculum civics, history, social science, and high-school economics content is encoded as universal across configurations, creating construct-irrelevant variance for the seven non-Jordanian deployment cohorts [DATASET-D1, D2, D6, D7, D21, D25].

**Recommendation:** Use the per-question country metadata field [Q33] to filter or stratify evaluation by source country; do not aggregate across countries for civics, history, or social science. Build a Kuwaiti, Moroccan, and Palestinian curriculum supplement before deploying to those cohorts.

### Input Content ⚠

**Gap:** Islamic studies has no madhab labeling anywhere in the benchmark [gap_id 7]; observed Islamic Studies HS content is Jordanian-curriculum-sourced [DATASET-D38] without Maliki (Morocco) or Hanbali (KSA) calibration.

**Recommendation:** Engage Islamic studies curriculum experts from Morocco (Maliki), KSA (Hanbali), and a Shafi'i-region representative to audit a stratified sample of Islamic studies items and tag madhab-specific items; flag madhab-divergent questions for country-conditioned evaluation.

### Output Content ⚠

**Gap:** Ground-truth labels for Palestinian, Moroccan, and Kuwaiti questions were verified by workers without those national curriculum backgrounds [Q31, Q96]; 96% agreement is a global figure not stratified by country [Q43].

**Recommendation:** Recruit at least 2–3 curriculum experts each from Morocco, Kuwait, and Palestine to re-verify ground-truth labels for at least the civics, history, social science, and law subsets relevant to those countries. Report country-stratified IAA before deployment use.

### Input Ontology ⚠

**Gap:** University-level coverage is ~6.1% of total [Q71] (~889 questions across all subjects), and Law (Professional) is exclusively Moroccan in the sample [DATASET-D34]; jurisdiction-specific tagging is absent.

**Recommendation:** Supplement with ArabLegalEval [WEB-3] for Saudi law, MizanQA [WEB-4] for Moroccan law, and AraSTEM [WEB-2] for STEM university content. Commission custom evaluation sets for Egyptian, UAE, Jordanian, Lebanese, Kuwaiti, and Palestinian legal jurisdictions which remain entirely unfilled by existing Arabic benchmarks.

### Input Form

**Gap:** OCR-corrupted text in Management and Political Science (University) configurations [DATASET-D14, D15, D29] compromises input signal quality, and French-medium Moroccan university content is entirely outside scope [Q92].

**Recommendation:** Quarantine or replace OCR-corrupted university management and political science items. For Moroccan university science, build or commission a French-Arabic bilingual evaluation since no existing benchmark addresses this gap [gap_id 6, WEB-4].

### Output Ontology

**Gap:** Flat single-correct-answer schema [Q27] cannot represent jurisdiction-specific correctness, despite deployment requirement for country-tailored legal answers [elicitation A2].

**Recommendation:** Add a jurisdiction-tag overlay on top of ArabicMMLU's existing country metadata for law and civics subsets; rescore tutoring outputs against jurisdiction-conditioned ground truth rather than the flat label.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we present ArabicMMLU, the first multi-task language understanding benchmark for the Arabic language, sourced from school exams across diverse educational levels in different countries spanning North Africa, the Levant, and the Gulf regions." |
| Q2 | 1 | input_form | "Our data comprises 40 tasks and 14,575 multiple-choice questions in Modern Standard Arabic (MSA) and is carefully constructed by collaborating with native speakers in the region." |
| Q3 | 1 | output_form | "Our comprehensive evaluations of 35 models reveal substantial room for improvement, particularly among the best open-source models." |
| Q4 | 1 | output_form | "Notably, BLOOMZ, mT0, LLaMA2, and Falcon struggle to achieve a score of 50%, while even the top-performing Arabic-centric model only achieves a score of 62.3%." |
| Q5 | 1 | input_content | "Although large language models (LLMs) such as GPT-3.5 (Ouyang et al., 2022), BLOOMZ (Muennighoff et al., 2022), and Jais (Sengupta et al., 2023) have been pretrained with substantial coverage of Modern Standard Arabic (MSA), their reasoning and knowledge assessments are primarily conducted using datasets translated from English to Arabic (Sengupta et al., 2023; Huang et al., 2023), which means there is limited capacity to evaluate content specific to Arabic." |
| Q6 | 1 | input_content | "This reliance on translation systems not only demonstrates an Anglocentric approach (Ramesh et al., 2023; Talat et al., 2022) but also potentially introduces errors and biases." |
| Q7 | 1 | input_content | "Given that Arabic is one of the most widely-spoken languages in the world, with a speaker population of over 400 million people (Shoufan and Alameri, 2015; Diab et al., 2017), it is critically important that datasets be constructed for the language that are regionally- and culturally-localized." |
| Q8 | 1 | input_content | "Fajri Koto, Haonan Li, Sara Shatnawi, Jad Doughman, Abdelrahman Boda Sadallah, Aisha Alraeesi, Khalid Almubarak, Zaid Alyafeai, Neha Sengupta, Shady Shehata, Nizar Habash, Preslav Nakov, Timothy Baldwin" |
| Q9 | 1 | input_content | "Department of Natural Language Processing, MBZUAI; Prince Sattam bin Abdulaziz University; King Fahd University of Petroleum and Minerals; Core42; New York University Abu Dhabi; The University of Melbourne" |
| Q10 | 1 | input_ontology | "The evaluation of language models has increasingly shifted from linguistically-centric tasks, such as part-of-speech (POS) tagging and named entity recognition (NER), towards reasoning and knowledge evaluation." |
| Q11 | 2 | input_content | "Early Arabic pretrained language models typically had less than 2 billion parameters and were primarily monolingual." |
| Q12 | 2 | input_ontology | "These models can be classified into three main categories: encoder-only, decoder-only, and encoder–decoder models." |
| Q13 | 2 | input_content | "The encoder-only models, such as AraBERT (Antoun et al., 2020), CAMeLBERT (Inoue et al., 2021), AraELECTRA (Antoun et al., 2021a), and ARBERT & MARBERT (Abdul-Mageed et al., 2021), are mainly from the BERT family." |
| Q14 | 2 | input_content | "AraGPT2 (Antoun et al., 2021b), on the other hand, is a decoder-only model available in different sizes ranging from 135M to 1.4B parameters." |
| Q15 | 2 | input_content | "Examples of encoder–decoder models include AraT5 (Nagoudi et al., 2022) and AraBART (Kamal Eddine et al., 2022)." |
| Q16 | 2 | input_content | "Jais (Sengupta et al., 2023) and AceGPT (Huang et al., 2023) are two recent Arabic-centric decoder-only models with parameter sizes of up to 30B and 13B, respectively." |
| Q17 | 2 | input_content | "Jais is pretrained on a corpus of 72 billion Arabic tokens, while AceGPT builds upon LLaMA2 and is enhanced with reinforcement learning from AI feedback (Lee et al., 2023) to localize the model to Arabic values and culture." |
| Q18 | 2 | input_content | "Both models are bilingual (English and Arabic), and were fine-tuned on various instruction datasets." |
| Q19 | 2 | input_content | "Arabic is also present in multilingual models." |
| Q20 | 2 | input_content | "This includes earlier models such as mBERT (Devlin et al., 2019) and XLM-R (Conneau et al., 2020), and more recent LLMs such as BLOOMZ (Muennighoff et al., 2022), mT0 (Muennighoff et al., 2022), Falcon (Penedo et al., 2023), GPT-3.5 (Ouyang et al., 2022), and GPT-4 (OpenAI, 2023)." |
| Q21 | 2 | output_form | "In the original papers, only GPT-4 was evaluated in Arabic in terms of its reasoning and knowledge capabilities, using the English–Arabic translated MMLU dataset, reporting an accuracy of 80%." |
| Q22 | 2 | input_content | "Arabic is included in various multilingual benchmarks for natural language understanding and generation, such as XGLUE (Liang et al., 2020), XTREME (Hu et al., 2020), XTREME-R (Ruder et al., 2021) and GEM (Gehrmann et al., 2021)." |
| Q23 | 2 | input_content | "In recent years, several Arabic-centric benchmarks have been released, such as Dolphin (Nagoudi et al., 2023), OCRA (Elmadany et al., 2023), and LAraBench (Abdelali et al., 2024)." |
| Q24 | 2 | input_ontology | "Many tasks in these benchmarks involve classification, such as natural language." |
| Q25 | 3 | input_ontology | "ArabicMMLU is an Arabic multiple-choice question-answering dataset comprising 40 tasks spanning a wide range of subjects and education levels." |
| Q26 | 3 | input_content | "The questions are sourced from eight different countries in North Africa (Morocco and Egypt), the Levant (Jordan, Palestine, and Lebanon), and the Gulf (UAE, Kuwait, and KSA)." |
| Q27 | 3 | output_ontology | "Each question has 2–5 candidate answers, with one correct answer." |
| Q28 | 3 | input_ontology | "The subjects are drawn from different education levels (primary school, middle school, and KSA, prioritize Islamic studies alongside subjects like mathematics, natural science, social science, and geography." |
| Q29 | 3 | input_form | "In public schools, Arabic is commonly used for teaching and assessment, while in international schools, English is the predominant language of instruction for most subjects, following either the UK or USA curriculum." |
| Q30 | 3 | input_form | "When designing ArabicMMLU, we excluded questions in English and only included questions in Arabic." |
| Q31 | 4 | input_content | "The data construction process involved a total of 10 Arabic native speakers from different countries: 6 internal workers (1 Jordanian, 1 Egyptian, 1 Lebanese, 1 from UAE, and 2 from KSA) and 4 external workers (3 Jordanian and 1 Egyptian)." |
| Q32 | 4 | input_content | "During the first stage of data collection, the internal workers were tasked with collecting relevant sources for data collection. These sources were URLs containing the questions, which needed to be publicly available." |
| Q33 | 4 | input_form | "In the second stage, all workers were asked to manually scrape the data within a 2-month period. The task was to collect metadata, including the source (URL of the source document), country, subject, level, question, multiple-choice options, and the correct answer key." |
| Q34 | 4 | input_content | "Each external worker was assigned to gather 2,000 questions, while internal workers were tasked with gathering 1,000–2,000 questions each." |
| Q35 | 4 | output_content | "Our internal workers are Master's students and Research Assistants in Computer Science, while the external workers hold Bachelor's degrees." |
| Q36 | 4 | output_content | "We ensured competitive compensation for the workers, exceeding the monthly average wage in each respective country." |
| Q37 | 4 | input_form | "During manual data scraping, workers were instructed to include only questions accompanied by an answer key, and to discard questions containing multi-modal information (e.g., images, videos, or tables)." |
| Q38 | 4 | input_form | "If a question had additional contextual information (e.g., a passage referenced by several questions), the context was required to be included with each corresponding question." |
| Q39 | 4 | output_content | "While our workers are native speakers of Modern Standard Arabic with at least Bachelor's degrees, we maintain the quality of our dataset construction through meticulous steps." |
| Q40 | 4 | output_content | "Firstly, we conducted a 1-hour workshop before the data collection stage to clarify the process." |
| Q41 | 4 | input_form | "Secondly, we automatically filtered out repetitive questions and those without an answer key, reducing the initial set of over 15,000 questions to 14,575 unique questions." |
| Q42 | 4 | output_content | "Finally, we assessed the accuracy of our data collection by having two native Arabic speakers annotate 100 randomly sampled questions. They were provided with all metadata, including the answer key, and tasked with verifying the correctness of each sample using any available resources (e.g., search engines)." |
| Q43 | 4 | output_content | "We found that 96% of the questions and answer keys match on average, while the remaining could have incorrect answer keys." |
| Q44 | 4 | output_content | "This 96% score is considered to represent the maximum score meaningfully achievable for ArabicMMLU." |
| Q45 | 5 | output_form | "Our experiments focus on zero-shot and few-shot settings across 35 models." |
| Q46 | 5 | output_form | "This includes 22 open-source multilingual models (XGLM (Lin et al., 2022), BLOOMZ (Muennighoff et al., 2022), mT0 (Muennighoff et al., 2022), Falcon (Penedo et al., 2023), and LLaMA2 (Touvron et al., 2023), across various sizes), 11 open-source Arabic-centric models (AraT5 (Nagoudi et al., 2022), AraGPT2 (Antoun et al., 2021b), AceGPT (Huang et al., 2023) and Jais (Sengupta et al., 2023), also across various sizes), and 2 closed-source models (GPT-3.5: gpt-3.5-turbo (Ouyang et al., 2022) and GPT-4: gpt-4-0613 (OpenAI, 2023))." |
| Q47 | 5 | output_form | "We initially conducted experiments with four settings: (1) Arabic prompt and Arabic alphabetic output, (2) Arabic prompt and English (i.e. Latin script) alphabetic output, (3) English prompt and Arabic alphabetic output, and (4) English prompt and English alphabetic output." |
| Q48 | 5 | input_form | "Figure 4 illustrates the Arabic and English prompts." |
| Q49 | 5 | input_form | "The placeholders [SUBJECT], [LEVEL], and [COUNTRY] are replaced with the corresponding Arabic and English words, while the placeholders [INPUT] and [OPTION] are in Arabic." |
| Q50 | 6 | output_form | "Following previous studies (Koto et al., 2023; Li et al., 2023), for open-source models, we determine the answer based on the highest probability among all possible options." |
| Q51 | 6 | output_form | "In the case of English alphabetic output, we measure the probability of the first generated token being A, B, C, D, or E." |
| Q52 | 6 | output_form | "For Arabic, we measure the probability of the first generated token being @, H., h., X, or è." |
| Q53 | 6 | output_form | "For closed-source models, we determine the answer based on the first token generated in the text using a regular expression." |
| Q54 | 6 | output_form | "If there is no match, we assign a random answer." |
| Q55 | 6 | output_form | "To evaluate the influence of prompt language, we initially benchmarked the open-source models using all four prompt settings (Section 4.1), as depicted in Figure 5." |
| Q56 | 6 | output_form | "We observe that the optimal configuration across all models is to use an English prompt and English alphabetic output." |
| Q57 | 6 | output_form | "Predictably, the Arabic-specific LLMs — Jais-chat (30B) and AceGPT-chat (13B) — demonstrate the greatest robustness when employing Arabic alphabetic output." |
| Q58 | 6 | output_form | "For the remaining experiments, we will report based on the setting of English prompt and English alphabetic output." |
| Q59 | 7 | output_form | "As expected, the Arabic-centric model Jais-chat (30B) emerges as the top-performing open-source model, boasting an average score of 62.3%, surpassing GPT-3.5 by 4.6 points." |
| Q60 | 7 | output_form | "Compared to AceGPT-chat (13B), both Jais-chat models (13B and 30B) exhibit substantially higher accuracy in areas including STEM, Social Science, Humanities, and Others." |
| Q61 | 7 | output_form | "For multilingual models such as BLOOMZ (7B) and mT0 (13B), their performance lags behind Jais, with a disparity of more than 14 points." |
| Q62 | 7 | output_form | "XGLM, LLaMA2, and Falcon perform at a level close to random, suggesting their limited proficiency in Arabic." |
| Q63 | 7 | output_form | "GPT-4 achieves the highest accuracy, with a score of 72.5%, surpassing Jais-chat (30B) by 10 points." |
| Q64 | 7 | output_content | "It is noteworthy that in the GPT-4 technical report (OpenAI, 2023), the accuracy of the English-Arabic translated MMLU dataset is reported as 80%, which is 8 points higher than our ArabicMMU results." |
| Q65 | 7 | output_content | "One possible explanation for this difference is that our ArabicMMU presents a greater challenge due to its inclusion of a higher proportion of Arabic-specific content." |
| Q66 | 7 | output_form | "Furthermore, we notice a trend of increasing accuracy with larger models, with the exception of XGLM." |
| Q67 | 7 | output_form | "For example, BLOOMZ (7B) achieves an accuracy 15.9 points higher than BLOOMZ (560M), while mT0 (13B) shows a 13.8-point increase compared to mT0 (300M)." |
| Q68 | 7 | input_ontology | "We observe that ArabicMMU questions are more challenging at the high school level compared to the primary and middle school levels." |
| Q69 | 7 | output_form | "Specifically, for high school questions, GPT-4 achieves a score of only 61.7%, while Jais-chat scores 51.2%." |
| Q70 | 7 | output_form | "Interestingly, we notice that the model accuracy at the university level is higher than for high school." |
| Q71 | 7 | input_ontology | "This could be attributed to the relatively small portion (i.e., 6%) of university-level questions in ArabicMMU, which potentially skews the results." |
| Q72 | 7 | input_ontology | "We present the performance of open-source models on selected subjects that potentially contain Arabic-specific contexts." |
| Q73 | 7 | input_ontology | "These subjects include history, geography, civics, political" |
| Q74 | 8 | output_form | "We focus our more detailed analysis in this section solely on the best open-source models, namely BLOOMZ, AceGPT, and Jais, providing researchers and the community with insights to better understand these models and opportunities for future improvements." |
| Q75 | 8 | output_form | "While all the results in Section 4.2 were based on zero-shot learning, we observe in Figure 7 that when we move to few-shot learning, results for base models improve but those for instruction-tuned models deteriorate." |
| Q76 | 8 | output_form | "Specifically, AceGPT and Jais show an improvement of 2–10 points when using few-shot learning, but the results for BLOOMZ and Jais-chat drop." |
| Q77 | 8 | output_form | "These findings are consistent with prior research over IndoMMIU (Koto et al., 2023) and CMMLU (Li et al., 2023)." |
| Q78 | 8 | output_form | "We analyze whether BLOOMZ, AceGPT, and Jais are well-calibrated in answering ArabicMMLU questions by comparing the probability of the correct answers with the actual accuracy for each task (i.e., subject and level combination)." |
| Q79 | 8 | output_form | "The answer probability is obtained through softmax normalization across the available candidate answers." |
| Q80 | 8 | output_form | "In Figure 8, we observe that the three open-source models are well calibrated with correlation scores r > 0.9." |
| Q81 | 8 | output_form | "Additionally, we investigate the correlation between model confidence and question length in Figure 9." |
| Q82 | 8 | output_form | "We find no correlation between the length of the questions and the model confidence for either Jais or AceGPT." |
| Q83 | 8 | input_ontology | "Despite negation being an absolutely foundational linguistic phenomenon, LLMs have been shown to be worryingly insensitive to its effects in English (Kassner and Schütze, 2020; Hosseini et al., 2021; Truong et al., 2023)." |
| Q84 | 8 | input_ontology | "We thus perform an analysis of LLM performance over questions in ArabicMMLU with and without negation to determine whether this observation ports across to Arabic." |
| Q85 | 8 | input_form | "We utilize specific negation phrases to identify questions containing negations in Arabic." |
| Q86 | 9 | input_ontology | "We introduce ArabicMMLU, the first large-scale multi-task language understanding dataset designed to evaluate real-world knowledge in Arabic." |
| Q87 | 9 | input_content | "Through experiments with over 14K multiple-choice questions spanning various subjects and education levels, we observed that Arabic-centric LLMs outperform multilingual LLMs, albeit with lower accuracy than GPT-4." |
| Q88 | 9 | input_ontology | "For future work, ArabicMMLU can be extended to include short-answer or essay questions, different modalities (i.e., images, audio, video), larger region coverage, and more questions in professional settings." |
| Q89 | 9 | input_content | "ArabicMMLU does not represent all Arabic countries equally. For example, we have collected over 6K multiple-choice questions from Jordan, while other countries are represented with only 100 questions or, in some cases, not at all." |
| Q90 | 9 | input_content | "This is largely due to the availability of publicly-accessible exams in each country; some countries have digitized their exams, but not others." |
| Q91 | 9 | input_content | "Additionally, our search for relevant Arabic content across the internet was not exhaustive." |
| Q92 | 9 | input_form | "The dataset primarily focuses on Modern Standard Arabic (MSA). However, multilingual and Arabic LLMs are often exposed to both MSA and dialectical Arabic." |
| Q93 | 9 | input_form | "ArabicMMLU is focused solely on text-based assessment, and the exploration of multimodal questions is left for future work." |
| Q94 | 9 | output_content | "It is important to emphasize that our experimental results do not provide conclusive answers regarding the performance of LLMs in Arabic." |
| Q95 | 10 | output_content | "to a lack of sufficient information about its training regimen. As such, we cannot assert that the model's pretraining data is free from contamination." |
| Q96 | 10 | input_content | "We extend our gratitude to all collaborators from Jordan, Egypt, Lebanon, UAE, and Saudi Arabia who participated in the data collection process." |
| Q97 | 10 | input_content | "We also acknowledge the contributions of Samta Kamboj, Sarah Al Barri, and Onkar Pandit from Core42, who assisted in collecting the Arabic Language question dataset." |
| Q98 | 14 | input_content | "Table 7 presents the distribution of ArabicMMLU data categorized by subject across different education levels." |
| Q99 | 14 | input_form | "Figure 10 illustrates a complete example of prompts used in this study. This example features a Natural Science question with prompts provided in both Arabic and English." |
| Q100 | 14 | input_ontology | "This is a Natural Science question for primary school in Jordan. Select the correct answer!" |
| Q101 | 14 | input_content | "Table 7: The distribution of ArabicMMLU for each subject in different education levels." |
| Q102 | 15 | output_form | "Table 8 presents the detailed zero-shot results across subjects and education levels, while Table 9, Table 10, Table 11 display the results with different prompts and alphabetic outputs (complementing the main result at Table 8)." |
| Q103 | 15 | output_form | "Zero-shot LLM performance (% accuracy) with English prompt and English alphabetic output, for each subject and education level." |
| Q104 | 15 | output_form | "The models are BLOOMZ (7B), AceGPT-chat (13B), Jais-chat (30B), GPT-3.5 (175B), and GPT-4." |
| Q105 | 16 | output_form | "Zero-shot LLM performance (% accuracy) with Arabic prompt and Arabic alphabetic output, combined across subject groups." |
| Q106 | 16 | output_form | ""Average" means the average across all questions in ArabicMMLU." |
| Q107 | 16 | input_ontology | "Table 9 presents results organized by subject groups: STEM, Social Science, Humanities, Arabic Language, and Other." |
| Q108 | 17 | output_form | "Zero-shot LLM performance (% accuracy) with Arabic prompt and English alphabetic output, combined across subject groups." |
| Q109 | 17 | input_ontology | "Table 10: Zero-shot LLM performance (% accuracy) with Arabic prompt and English alphabetic output, combined across subject groups." |
| Q110 | 18 | output_form | "Zero-shot LLM performance (% accuracy) with English prompt and Arabic alphabetic output, combined across subject groups." |
| Q111 | 19 | input_content | "Table 12 lists the sources of pre-trained models used in this study. All models are sourced from Huggingface (Wolf et al., 2020)." |
| Q112 | 19 | input_content | "With the exception of GPT-3.5 and GPT-4, all the models used in this study were sourced from Huggingface (Wolf et al., 2020)." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://arxiv.org/html/2402.12840v1 |
| WEB-2 | https://arxiv.org/abs/2501.00559 |
| WEB-3 | https://arxiv.org/abs/2408.07983 |
| WEB-4 | https://arxiv.org/abs/2510.13430 |
| WEB-5 | https://www.nyulawglobal.org/globalex/egypt.html |
| WEB-6 | https://www.themoonlight.io/en/review/arabicmmlu-assessing-massive-multitask-language-understanding-in-arabic |
| WEB-7 | https://www.itu.int/itu-d/reports/statistics/2023/10/10/ff23-internet-use/ |
| WEB-8 | https://statisticsoftheworld.com/ranking/internet-users |
| WEB-9 | https://datahub.itu.int/ |
| WEB-10 | https://www.arabbarometer.org/2020/09/the-mena-digital-divide/ |
| WEB-11 | https://www.itu.int/dms_pub/itu-d/opb/ind/D-IND-SDDT_ARB-2025-PDF-E.pdf |
| WEB-12 | https://huggingface.co/datasets/MBZUAI/ArabicMMLU |
| WEB-13 | https://arxiv.org/html/2510.00694 |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** MBZUAI/ArabicMMLU
**Analysis date:** 2025-01-30
**Examples reviewed:** ~185 examples across 40 subject-level configurations
**Columns shown:** ID, Source, Country, Group, Subject, Level, Question, Context, Answer Key, Option 1–5, is_few_shot
**Columns skipped (media):** None (all text)

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | ArabicMMLU | Civics (HS), ID 14501 | A | "من مظاهر التغير التي طرأت على طبيعة المجتمع الاردني الحديث" | "What are the manifestations of change in modern Jordanian society?" — country-specific Jordanian civics | IC |
| D2 | ArabicMMLU | Civics (MS), ID 14291 | C | "تم تشكيل أول حكومة ائتلافية في الأردن عام 1952 وقد عرفت باسم الحكومة:" | "The first coalition government in Jordan in 1952 was known as the ___ government" — Jordanian political history | IC |
| D3 | ArabicMMLU | Civics (MS), ID 14255 | D | "المجلس صاحب الولآية العامة على شؤون الدولة كافة هو ب" with answer "مجلس الوزارء" | "The council with general sovereignty over all state affairs is the Council of Ministers" — specifically Jordanian constitutional structure | OC |
| D4 | ArabicMMLU | History (HS), ID 2827 | A | "من الحقوق والحريات التي يشترط الدستور بممارستها ان تكون طبقا للعادات المرعية في المملكة" | "Rights under the [Jordanian] Kingdom's constitution" — explicitly references the Jordanian Hashemite Kingdom | IC, OC |
| D5 | ArabicMMLU | History (HS), ID 2819 | D | "صدر دستور عام 1952 في عهد جلالة الملك" with options referring to Jordanian kings | "The 1952 constitution was issued during the reign of King [Talal bin Abdullah]" — Jordanian royal history | IC |
| D6 | ArabicMMLU | Economics (HS), ID 11412 | C | "ارسال الشكوى عن طريق الموقع الالكتروني للبنك المركزي وهو: www.cbj.gov.jo" | "Complaints to the Central Bank [of Jordan] via www.cbj.gov.jo" — explicitly references Jordan's central bank | IC |
| D7 | ArabicMMLU | Economics (HS), ID 11561 | B | "نسبة الأردنيين الذين لا يستطيعون الوصول إلى الخدمات المالية الرسمية: 0.67" | "67% of Jordanians cannot access formal financial services" — Jordan-specific statistic as universal economic fact | IC, OC |
| D8 | ArabicMMLU | Law (Prof), ID 4881 | B | "لا يقبل استئناف الأحكام التمهميدية أو الصادرة في نزاع عارض أو دفوع إلا بعد صدور الحكم في جوهر الدعوى" | Moroccan procedural law — appeals rules under Moroccan Code of Civil Procedure | IC, OC |
| D9 | ArabicMMLU | Law (Prof), ID 4652 | C | "يمكن تخويل صفة ضابط الشرطة القضائية للدركيين...بقرار من وزبر العدل والسلطة الحكومية المكلفة بالدفاع الوطني" | Moroccan judicial police powers — references "الدرك الملكي" (Royal Gendarmerie of Morocco) | IC, OO |
| D10 | ArabicMMLU | Law (Prof), ID 4843 | C | "إذا تنازل الطرف المدني قبل صدور الحكم: جميع الأجوبة صحيحة" | Moroccan civil party withdrawal in criminal proceedings | IC, OC |
| D11 | ArabicMMLU | Political Science (Univ), ID 6960 | C | "احداث متتابعة قد تكون تعاونیة أو صراعیة ھى: التفاعلات" | "Sequential events, cooperative or conflictual, are called: interactions" — general IR concept | IC |
| D12 | ArabicMMLU | Political Science (Univ), ID 7131 | A | "ﺗﻌﺗﺑر اﻟﺛورة اﻟﻔرﻧﺳﯾﺔ ﻋﺎم 1789 أﺑرز ﻣﺛﺎل ﻟﻠﺛورات اﻟﻛﺑرى اﻟﺗﻲ ﻋززت ﺣﻘوق اﻹﻧﺳﺎن: ﺻﺢ" | "The French Revolution is the foremost example of revolutions that strengthened human rights: True" — all from Egyptian sources (aun.edu.eg) | IC |
| D13 | ArabicMMLU | Accounting (Univ), ID 7245 | A | "يفترض أسموب المراجعة حول الحاسب أنو إذا كانت المدخالت سميمة...فإن عممية التشغيل تكون سميمة بالتبعية" | Computer auditing concept — general accounting principle, from Egyptian source | IC |
| D14 | ArabicMMLU | Management (Univ), ID 6175 | B | "درجتة تهييتع الدتلطة بتين الألتخاص والسدتتهيات اإلداريتة السختلفتة...تذتير إلى" | Severely OCR-distorted text about authority distribution in organizations, from Egyptian source | IF |
| D15 | ArabicMMLU | Management (Univ), ID 6174 | C | "ال يعد مثاالً على الخطط دائسة اإلستخدام... الرخرحم ت... الح ً ت." | Severely OCR-corrupted management question with unreadable answer options | IF |
| D16 | ArabicMMLU | Computer Science (Univ), ID 7280 | C | "الكمبيوتر الدقيق هو عبارة عن: جهاز الكمبيوتر المكتبي" | "A microcomputer is a desktop computer" — from KSA source (faculty.ksu.edu.sa) | IC |
| D17 | ArabicMMLU | Islamic Studies (HS), ID 14064 | E | "للتفكير آثار إيجابية عدة: جميع ما ذكر" — Country: Jordan | 5-option Islamic studies question about positive effects of thinking | IO, OO |
| D18 | ArabicMMLU | Islamic Studies (General), ID 165 | D | "قال الرسول صلى الله عليه وسلام: (لا يدخل الجنة قتات)، فمن هو القتات؟ النمام" | "The Prophet said: the 'qattat' shall not enter paradise — who is qattat? A gossip/slanderer" — no country field, generic Islamic trivia source | IC |
| D19 | ArabicMMLU | Arabic Language (Grammar), ID 12626 | A | "In the following Quranic verse, what is the correct parsing of the word ــكَ" | English-language question stem in an Arabic grammar dataset | IF |
| D20 | ArabicMMLU | Social Science (PS), ID 5489 | D | "تشمل الخدمات الطبية الملكية الحكومية العديد من المؤسسات...منها: مستشفى المدينة الطبية" | "Royal Medical Services include: Medical City Hospital" — specifically Jordanian Royal Medical Services | IC |
| D21 | ArabicMMLU | Social Science (PS), ID 5481 | D | "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" | "King Talal bin Hussein's reign ended for health reasons in 1952 — one year" — Jordanian royal history in primary school | IC |
| D22 | ArabicMMLU | Geography (MS), ID 8055 | A | "توجد كنيسة سيدة الجبل في ……. عنجرة" | "Lady of the Mountain Church is in Anjara [Jordan]" — Jordanian religious geography | IC |
| D23 | ArabicMMLU | Computer Science (PS), ID 7354 | A | "أحد أنظمة العد يستخدمه الحاسوب في تمثيل وحفظ البيانات ومعالجتها: النظام الثنائي" | "The binary number system is used by computers" — Palestine-sourced primary CS | IC |
| D24 | ArabicMMLU | Biology (HS), ID 9842 | D | "إذا نتج (3) جزيئات غلوكوز عن حلقة كالفن فكم عدد جزيئات (CO2) التي تم تثبيتها ؟" | Calvin cycle question — Palestine-sourced biology; universal factual content | IC |
| D25 | ArabicMMLU | Civics (HS), ID 14529 | C | "كان الهدف الرئيس للمعاهده الأردنيه البريطانيه عام ١٩٢٨: تحرر البلاد من قيود فك الانتداب" | "The main goal of the 1928 Jordanian-British treaty was liberation from Mandate restrictions" — Jordanian national history | IC |
| D26 | ArabicMMLU | All (Islamic Studies), ID 165–54 | null | All 5 examples: Country = null, Source = folderat.com, Subject = Islamic Studies | Islamic Studies "All" config examples have no country metadata — source appears to be generic Arabic quiz site | IO, OC |
| D27 | ArabicMMLU | Arabic Language (General), ID 11849–11736 | null | All 5 examples: Country = null, Source = madinaharabic.com | Arabic Language General has no country metadata — sourced from online Arabic language learning site | IO |
| D28 | ArabicMMLU | Economics (Univ), ID 11228 | B | "إذا كان حجم الاستثمار المطلوب ١٠٠ر٠٠٠ جنيه...معدل العائد على الأموال المستثمرة هو: % ١٥" | Egyptian currency (جنيه = Egyptian pound) in university economics — Egypt-specific monetary context | IC, OC |
| D29 | ArabicMMLU | Political Science (Univ), ID 7008 | D | "مررن الشررروط الاساسررٌ التررً ٌ ررب توافر ررا فررً ال رراكم فررً الدولرر الاسررالمٌ" | Severely OCR-distorted Arabic text about conditions for an Islamic ruler — from Egyptian source | IF |
| D30 | ArabicMMLU | Geography (HS), ID 8529 | D | "محمية طبيعية في الأردن تشرف عليها إدارة مشتركة...وادي رم" | "Wadi Rum is a Jordanian nature reserve under joint management" — Jordan-specific geography fact | IC |
| D31 | ArabicMMLU | History (HS), ID 3049 | D | "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين" | King Abdullah I's positions on Zionism — highly sensitive political content, Jordanian framing of Palestinian history | IC, OC |
| D32 | ArabicMMLU | Social Science (MS), ID 5261 | D | "أنعم الله على بلادنا العربية بثروات كبيرة من النفط والغاز الطبيعي...يرجع السبب في ذلك إلى: توافره بكميات قليلة" | "Gas is available in limited quantities" — possibly incorrect answer key for general Arab world social science | OC |
| D33 | ArabicMMLU | Computer Science (MS), ID 7333–7343 | all Jordan | All 5 examples: Country = Jordan, Windows OS questions | Middle school CS focuses on Windows OS user interface — likely dated Jordanian curriculum content | IC |
| D34 | ArabicMMLU | Law (Prof), all 5 examples | Morocco | All 5 Law (Professional) examples: Country = Morocco, from single Google Drive PDF | All sampled law questions are exclusively from Morocco — single-source PDF | IC, OC |
| D35 | ArabicMMLU | Driving Test, ID 687, 695 | UAE | "في حال تعطل مركبتك ولديك مثلث التحذير العاكس، أين عليك وضعه؟ على بعد 50 متر" | UAE driving rule (50m warning triangle placement) — country-specific traffic regulation | IO, OO |
| D36 | ArabicMMLU | General Knowledge (MS), ID 4556 | A | "الشامل الأكاديمي يمثل ……. الأدبي" | "The 'comprehensive academic' [track] is the humanities track" — Jordanian secondary school track system | IC |
| D37 | ArabicMMLU | Islamic Studies (Primary), ID 12853 | D | "من آداب تلاوة القرآن الكريم: جميع ما ذكر" — Country: Jordan | Generic Islamic etiquette of Quran recitation — no madhab specificity indicated | IC |
| D38 | ArabicMMLU | Islamic Studies (HS), ID 14042 | D | "فوائد إيراد الأمثال في القرآن الكريم: جميع ما ذكر" — Country: Jordan | Islamic studies question about examples in Quran — Jordanian curriculum framing | IC |
| D39 | ArabicMMLU | Accounting (Univ), ID 7245 | A | Source: http://www.aun.edu.eg/commerce/... | All 5 accounting examples from Assiut University (Egypt) — single Egyptian university source | IC, OC |
| D40 | ArabicMMLU | Economics (University), all 5 | Egypt | Source: http://www.aun.edu.eg — all 5 from same Assiut University Egypt URL | University economics exclusively from Egyptian university source | IC |

---

### Deployment-Relevant Strengths

#### Strength 1: Authentic country-sourced exam content in target languages and format
- **Dimension(s):** IC, IF
- **Observation:** The sampled questions demonstrate genuine national exam provenance — questions are clearly drawn from real school assessments, not translations. Arabic language, grammar, STEM, and Islamic studies questions are well-formed MSA suitable for the school tutoring context. The format is entirely MCQ with 2–5 options, directly matching the deployment's primary format.
- **Deployment relevance:** For the deployment's core use case (supporting students with MCQ exam preparation), the native exam origin means content register, vocabulary difficulty, and question structure are authentic to what students encounter in real exams.
- **Datapoint citations:**
  - [D24] Example Biology (HS), ID 9842 (Palestine, test): "إذا نتج (3) جزيئات غلوكوز عن حلقة كالفن فكم عدد جزيئات (CO2) التي تم تثبيتها ؟" — Authentic Palestinian high school biology question in proper MSA with scientific terminology.
  - [D37] Example Islamic Studies (PS), ID 12853 (Jordan, test): "من آداب تلاوة القرآن الكريم: جميع ما ذكر" — Primary school Islamic studies question in standard school format.
  - [D25] Example Civics (HS), ID 14529 (Jordan, test): "كان الهدف الرئيس للمعاهده الأردنيه البريطانيه عام ١٩٢٨: تحرر البلاد من قيود فك الانتداب" — Tawjihi-style question format.

#### Strength 2: Broad subject taxonomy covering all six deployment university subjects
- **Dimension(s):** IO
- **Observation:** The dataset's 40 configurations directly observed include Accounting (University), Computer Science (University), Economics (University), Management (University), Political Science (University), and Law (Professional) — all six university-level subjects the deployment targets. This is confirmed through direct data inspection, not just paper claims.
- **Deployment relevance:** The deployment specifically requires coverage of law, management, economics, CS, political science, and accounting for university students. All are present as distinct, queryable configurations.
- **Datapoint citations:**
  - [D13] Example Accounting (Univ), ID 7245 (Egypt, test): "يفترض أسموب المراجعة حول الحاسب أنو إذا كانت المدخالت سميمة...فإن عممية التشغيل تكون سميمة بالتبعية" — University accounting question about computer auditing methodology.
  - [D16] Example CS (Univ), ID 7280 (KSA, test): "الكمبيوتر الدقيق هو عبارة عن: جهاز الكمبيوتر المكتبي" — University CS definitional question from Saudi source.
  - [D11] Example Political Science (Univ), ID 6960 (Egypt, test): "احداث متتابعة قد تكون تعاونیة أو صراعیة ھى: التفاعلات" — University-level international relations concept.

#### Strength 3: Moroccan law content is present and confirmed in the data
- **Dimension(s):** IC, IO
- **Observation:** The Law (Professional) configuration — the only university/professional law split — contains exclusively Moroccan questions in the sample (all 5 sampled questions from Morocco, sourced from a single Google Drive PDF of Moroccan procedural law). These cover Moroccan appellate procedures, civil party rules, and judicial police powers under Moroccan law, referencing Morocco-specific institutions (الدرك الملكي — Royal Gendarmerie).
- **Deployment relevance:** The web search found this Moroccan law content was used as an illustrative example in the paper, and the data confirms it is genuinely present. For the deployment's Moroccan law students, some Moroccan-jurisdiction legal content exists.
- **Datapoint citations:**
  - [D8] Example Law (Prof), ID 4881 (Morocco, test): "لا يقبل استئناف الأحكام التمهميدية...إلا بعد صدور الحكم في جوهر الدعوى" — Moroccan Code of Civil Procedure appeal rules.
  - [D9] Example Law (Prof), ID 4652 (Morocco, test): "يمكن تخويل صفة ضابط الشرطة القضائية للدركيين...من وزبر العدل والسلطة الحكومية المكلفة بالدفاع الوطني" — Moroccan judicial police appointment procedure referencing Morocco-specific institutions.
  - [D10] Example Law (Prof), ID 4843 (Morocco, test): "إذا تنازل الطرف المدني قبل صدور الحكم: جميع الأجوبة صحيحة" — Moroccan criminal procedure rule.

#### Strength 4: Palestine is substantively present across STEM and language subjects
- **Dimension(s):** IC, IO
- **Observation:** Palestinian-sourced questions appear across multiple configurations: Biology (HS) — 4 of 5 examples from Palestine; Computer Science (Primary) — all 5 examples from Palestine; Math (Primary) — multiple Palestine examples; Arabic Language (Primary) — one Palestine example; Geography (Middle) — 2 Palestine examples; Physics (HS) — 2 Palestine examples. This confirms Palestine is a real contributor, not just a nominal listing.
- **Deployment relevance:** Palestine is a high-priority deployment target. The data shows that for STEM and basic academic subjects, Palestinian curriculum content is genuinely represented.
- **Datapoint citations:**
  - [D23] Example CS (PS), ID 7354 (Palestine, test): "أحد أنظمة العد يستخدمه الحاسوب في تمثيل وحفظ البيانات ومعالجتها: النظام الثنائي" — Palestinian primary school CS.
  - [D24] Example Biology (HS), ID 9842 (Palestine, test): "إذا نتج (3) جزيئات غلوكوز عن حلقة كالفن فكم عدد جزيئات (CO2) التي تم تثبيتها ؟" — Palestinian HS biology.

#### Strength 5: STEM content is genuinely curriculum-neutral and reliable across countries
- **Dimension(s):** IC, OC
- **Observation:** Math (Primary), Biology (HS), Physics (HS), Natural Science, and CS questions in the data contain factual content that does not vary by national curriculum. The answers are objectively verifiable regardless of student nationality, making ground-truth labels reliable across all eight deployment countries for these subjects.
- **Deployment relevance:** For the large portion of the deployment serving STEM students, the benchmark's content validity is high. Country-specific annotation bias (the major OC concern) does not affect factual STEM questions.
- **Datapoint citations:**
  - [D24] Example Biology (HS), ID 9842 (Palestine, test): "إذا نتج (3) جزيئات غلوكوز عن حلقة كالفن فكم عدد جزيئات (CO2) التي تم تثبيتها ؟" — Universal biology fact.
  - [D1] through standard math examples: "ما ناتج جمع 2+ 6 = 8" — universal arithmetic.

#### Strength 6: Multi-level education coverage confirmed in data
- **Dimension(s):** IO
- **Observation:** The data directly confirms questions at Primary, Middle, High School, and University (Univ/Prof) levels across multiple subjects. The Level field is consistently populated for school-level questions, and university-level configurations (Accounting, Economics, Management, CS, Political Science) are separately queryable.
- **Deployment relevance:** The deployment targets all four educational tiers. The benchmark's level-specific configurations allow the tutoring system to select difficulty-appropriate questions.
- **Datapoint citations:**
  - [D13] Example Accounting (Univ), Level=Univ — university-level confirmed.
  - [D21] Example Social Science (PS), ID 5481, Level=Primary — primary level confirmed with Jordanian political content.
  - [D5] Example History (HS), ID 2819, Level=High — high school level confirmed.

#### Strength 7: Driving Test subject provides country-specific coverage for UAE, Egypt, and Lebanon
- **Dimension(s):** IO, IC
- **Observation:** The Driving Test configuration contains questions from UAE, Egypt, and Lebanon with country-specific traffic regulations. The UAE examples reference specific UAE road authority rules (50m warning triangle placement), and Lebanon examples reference Lebanese traffic law.
- **Deployment relevance:** While not a core tutoring subject, this demonstrates the benchmark's actual country-specific rule calibration for at least some subjects beyond academic content.
- **Datapoint citations:**
  - [D35] Example Driving Test, ID 687 (UAE, test): "في حال تعطل مركبتك ولديك مثلث التحذير العاكس، أين عليك وضعه؟ على بعد 50 متر" — UAE-specific driving rule.
  - [D35] Example Driving Test, ID 1025 (Lebanon, test): "يُحَظَّر على سائق المركبة: يجري مناورة عكس الإتجاه (Demi Tour) وسط الطريق" — Lebanese traffic law (note French loan word "Demi Tour").

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Civics and Social Studies are overwhelmingly Jordanian-centric — not pan-Arab
- **Dimension(s):** IC, OC
- **Severity:** CRITICAL
- **Observation:** In the sampled civics, history, social science, geography, and general knowledge data, the vast majority of country-specific content reflects exclusively Jordanian national curriculum content — Jordanian constitutional structure, Jordanian royal history, Jordanian medical institutions, Jordanian party laws, and Jordanian geographic landmarks. This is not a minor imbalance: the content is not presented as Jordanian-specific but as general curriculum knowledge. A Moroccan, UAE, or Kuwaiti student encountering these questions would be tested on Jordanian national content.
- **Deployment relevance:** The deployment requires curriculum-aligned answers for each of the eight countries. Questions about "الملك طلال بن الحسين," "مجلس التعاون الأردني," and Jordan's 1952 constitution are irrelevant or actively misleading for students from Morocco, UAE, Kuwait, or Palestine whose civics exams test entirely different national content. For civics subjects specifically, the benchmark effectively functions as a Jordanian civics test.
- **Datapoint citations:**
  - [D1] Example Civics (HS), ID 14501 (Jordan): "من مظاهر التغير التي طرأت على طبيعة المجتمع الاردني الحديث" — Explicitly asks about Jordanian society; not applicable to students from other eight countries.
  - [D2] Example Civics (MS), ID 14291 (Jordan): "تم تشكيل أول حكومة ائتلافية في الأردن عام 1952 وقد عرفت باسم الحكومة:" — Jordanian political history fact irrelevant to Moroccan or Emirati civics.
  - [D3] Example Civics (MS), ID 14255 (Jordan): "المجلس صاحب الولآية العامة على شؤون الدولة كافة هو ب: مجلس الوزارء" — Framed as a general question but answer is grounded in Jordanian constitutional law.
  - [D21] Example Social Science (PS), ID 5481 (Jordan): "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" — Jordanian royal history taught as primary school social studies.
  - [D36] Example General Knowledge (MS), ID 4556 (Jordan): "الشامل الأكاديمي يمثل ……. الأدبي" — Jordanian secondary school track labeling system specific to Jordan's education structure.

#### CRITICAL Concern 2: University-level content is dominated by a single Egyptian institution
- **Dimension(s):** IC, OC
- **Severity:** CRITICAL
- **Observation:** All 5 sampled Accounting (University) examples, all 5 Economics (University) examples, all 5 Management (University) examples, and all 5 Political Science (University) examples originate from a single source: Assiut University's Faculty of Commerce (aun.edu.eg). The Management examples notably include severely OCR-corrupted text rendering some questions and answer options unreadable. The Computer Science (University) examples all come from a single KSA source (faculty.ksu.edu.sa).
- **Deployment relevance:** The deployment requires university-level content for students in all eight countries. If university-level accounting, management, economics, and political science are sourced almost exclusively from one Egyptian university's question bank, the benchmark is measuring alignment with that specific institution's curriculum framing, not pan-Arab or per-country university education. For university students in Morocco, UAE, Kuwait, Lebanon, or Jordan, these Egyptian university questions may reflect different course structures, textbook traditions, or exam formats.
- **Datapoint citations:**
  - [D39] Examples Accounting (Univ), IDs 7245, 7196, 7215, 7186, 7185 — all Source: http://www.aun.edu.eg/commerce/... — single Egyptian university.
  - [D40] Examples Economics (Univ), all 5 — all Source: http://www.aun.edu.eg — same Egyptian university.
  - [D14] Example Management (Univ), ID 6175 (Egypt): "درجتة تهييتع الدتلطة بتين الألتخاص والسدتتهيات اإلداريتة السختلفتة فتى السشمستة تذتير إلى" — OCR-corrupted to the point of being unreadable; correct answer cannot be verified from the text alone.
  - [D15] Example Management (Univ), ID 6174 (Egypt): "ال يعد مثاالً على الخطط دائسة اإلستخدام... الرخرحم ت... الح ً ت." — Answer options are corrupted Arabic OCR artifacts.

#### CRITICAL Concern 3: Law (Professional) is exclusively Moroccan in the observed data — no evidence of multi-jurisdiction coverage
- **Dimension(s):** IC, OO, OC
- **Severity:** CRITICAL
- **Observation:** All 5 sampled Law (Professional) questions come from a single Moroccan source (a single Google Drive PDF of Moroccan procedural law). While this confirms Moroccan law is present, the deployment requires country-specific legal tutoring for Egypt (Egyptian civil code), UAE (federal civil law with Sharia overlay), Jordan (civil law), KSA (Sharia-based), Lebanon, Kuwait, and Palestine. The observed data provides no evidence that other legal jurisdictions are covered. The benchmark's flat single-correct-answer schema cannot encode that the answer to an appellate procedure question differs between Morocco and Egypt.
- **Deployment relevance:** The deployment user explicitly stated that "the system must tailor legal answers to each country's specific legal system." A benchmark where all sampled law questions are Moroccan procedural law cannot validate a tutoring system's legal correctness for Egyptian, UAE, Jordanian, or Saudi students. The jurisdictional ground truth cannot be determined from the flat label schema.
- **Datapoint citations:**
  - [D8] Example Law (Prof), ID 4881 (Morocco): "لا يقبل استئناف الأحكام التمهميدية...إلا بعد صدور الحكم في جوهر الدعوى" — Moroccan appellate rule; rule may differ under Egyptian or UAE procedural law.
  - [D9] Example Law (Prof), ID 4652 (Morocco): "يمكن تخويل صفة ضابط الشرطة القضائية للدركيين...من وزبر العدل والسلطة الحكومية المكلفة بالدفاع الوطني" — References "الدرك الملكي" (Morocco's Royal Gendarmerie) — institution does not exist in other deployment countries.
  - [D34] All 5 Law examples — Country = Morocco, single source URL — confirms single-jurisdiction observation.

---

#### MAJOR

#### MAJOR Concern 4: Significant OCR corruption in university-level management and political science questions
- **Dimension(s):** IF, OC
- **Severity:** MAJOR
- **Observation:** Multiple university-level management and political science questions contain severely corrupted Arabic text that appears to result from poor OCR of PDF scan material. Answer options in some management questions are entirely unreadable (e.g., "الرخرحم ت," "الح ً ت," "اليؾام"). Some political science questions have broken Arabic words mid-sentence. This affects ground-truth label reliability — if the question text is corrupted, it is unclear whether annotators could correctly verify the answer.
- **Deployment relevance:** The deployment targets university students including management and political science majors. Questions with corrupted text cannot reliably serve as evaluation items and would confuse or mislead students in a tutoring context.
- **Datapoint citations:**
  - [D15] Example Management (Univ), ID 6174 (Egypt): "ال يعد مثاالً على الخطط دائسة اإلستخدام... الرخرحم ت... الح ً ت. ...اليؾام" — Multiple answer options are OCR artifacts, not valid Arabic words.
  - [D14] Example Management (Univ), ID 6175 (Egypt): "درجتة تهييتع الدتلطة بتين الألتخاص والسدتتهيات اإلداريتة السختلفتة فتى السشمستة" — Question text has inserted random Arabic letters/diacritics breaking word boundaries.
  - [D29] Example Political Science (Univ), ID 7008 (Egypt): "مررن الشررروط الاساسررٌ التررً ٌ ررب توافر ررا فررً ال رراكم فررً الدولرر الاسررالمٌ" — Letters are doubled/tripled throughout, rendering text difficult to parse.

#### MAJOR Concern 5: Islamic Studies has no country metadata in the "General" and "All" configurations, and no madhab labeling anywhere
- **Dimension(s):** IC, OC
- **Severity:** MAJOR
- **Observation:** The five sampled Islamic Studies (General/All config) examples all have Country = null and are sourced from a generic Arabic quiz website (folderat.com). These questions cover Hadith-based ethics and Prophetic biography — content that is broadly consistent across Sunni traditions. However, no Islamic Studies question observed across any configuration has any madhab labeling, and the Islamic Studies (HS) questions are all Jordanian-curriculum. For Morocco (Maliki), the specific fiqh rulings and jurisprudential framing that appear in school Islamic studies curricula differ from Jordanian (mixed Shafi'i/unspecified) or Saudi (Hanbali) tradition.
- **Deployment relevance:** While the deployment user assessed madhab-level divergence as unlikely at school level, the actual data shows no mechanism for madhab identification or filtering. If a Moroccan student encounters a Hanbali-framing fiqh question from the Jordanian curriculum, the benchmark provides no flag for this. For the tutoring system to confidently support Moroccan Islamic studies students, this is a latent risk.
- **Datapoint citations:**
  - [D26] Examples Islamic Studies (All), IDs 165, 385, 46, 157, 54 — Country = null, Source = folderat.com — no curriculum attribution; generic Islamic knowledge quiz.
  - [D38] Example Islamic Studies (HS), ID 14042 (Jordan): "فوائد إيراد الأمثال في القرآن الكريم: جميع ما ذكر" — Jordanian high school framing of Quranic analysis; Saudi or Moroccan curricula may frame this differently.
  - [D37] Example Islamic Studies (PS), ID 12853 (Jordan): "من آداب تلاوة القرآن الكريم: جميع ما ذكر" — Practices of Quran recitation etiquette; factually consistent but Jordanian curriculum source only.

#### MAJOR Concern 6: Jordan-specific national content embedded as school-level "social science" and "history" without country-specific flagging
- **Dimension(s):** IC, OC
- **Severity:** MAJOR
- **Observation:** Primary and middle school Social Science questions include Jordanian-specific institutional facts (Jordan's Royal Medical Services, King Talal's reign) presented as factual questions without explicit country labels in question text. History questions at all levels heavily feature Jordanian royal history and Jordanian constitutional content. A benchmark user evaluating model performance on "History (Middle School)" or "Social Science (Primary School)" would receive a metric reflecting Jordanian curriculum knowledge, not pan-Arab or country-neutral historical knowledge.
- **Deployment relevance:** For Moroccan, Emirati, Saudi, or Kuwaiti primary and middle school students, the tutoring system evaluated against ArabicMMLU's history/social science subset would be tested on Jordanian-specific knowledge that is irrelevant to their national curriculum. This creates construct-irrelevant variance that could make a model appear stronger or weaker than it truly is for non-Jordanian curricula.
- **Datapoint citations:**
  - [D21] Example Social Science (PS), ID 5481 (Jordan): "الملك طلال بن الحسين انتهت ولايته لأسباب صحية وذلك في: 1952م، ومدة حكمه سنة" — Primary school Jordan-specific royal history.
  - [D20] Example Social Science (PS), ID 5489 (Jordan): "تشمل الخدمات الطبية الملكية الحكومية العديد من المؤسسات المتخصصة...مستشفى المدينة الطبية" — Jordan-specific institution.
  - [D4] Example History (HS), ID 2827 (Jordan): "من الحقوق والحريات التي يشترط الدستور بممارستها ان تكون طبقا للعادات المرعية في المملكة" — Explicitly the Jordanian (Hashemite) Kingdom's constitution.
  - [D31] Example History (HS), ID 3049 (Jordan): "واحدة من الآتية ليست من مواقف الملك عبدالله الأول من الحركة الصهيونية وأطماعها في فلسطين" — Politically sensitive question about King Abdullah I's positions; framing reflects Jordanian historical narrative which may differ from Palestinian national narrative.

#### MAJOR Concern 7: Economics (HS) contains Jordan-specific financial statistics and institutions
- **Dimension(s):** IC, OC
- **Severity:** MAJOR
- **Observation:** High school economics questions reference Jordan's Central Bank (CBJ) website and Jordan-specific financial inclusion statistics (67% of Jordanians without access to formal financial services) as factual questions without flagging them as Jordanian-specific. These figures are not cross-nationally applicable.
- **Deployment relevance:** For a UAE or Saudi Arabian high school economics student, a question asking for the Central Bank of Jordan's website address or Jordan-specific financial statistics would be irrelevant and potentially misleading. The benchmark does not distinguish between general economics principles and jurisdiction-specific institutional facts.
- **Datapoint citations:**
  - [D6] Example Economics (HS), ID 11412 (Jordan): "ارسال الشكوى عن طريق الموقع الالكتروني للبنك المركزي وهو: www.cbj.gov.jo" — Jordan-specific institutional URL as exam fact.
  - [D7] Example Economics (HS), ID 11561 (Jordan): "نسبة الأردنيين الذين لا يستطيعون الوصول إلى الخدمات المالية الرسمية: 0.67" — Jordan-specific statistic presented as curriculum fact.

#### MAJOR Concern 8: Egyptian currency denomination used as default in university economics
- **Dimension(s):** IC, OC
- **Severity:** MAJOR
- **Observation:** University Economics examples from Assiut University use Egyptian pounds (جنيه) in quantitative finance problems. For students in UAE (using dirhams), Kuwait (dinars), Jordan (dinars), or Morocco (dirhams), the currency denomination embeds Egyptian economic context as a universal fact.
- **Deployment relevance:** For the deployment's university economics students in non-Egyptian countries, correct application of financial formulas requires recognizing this currency context, and any tutor response would need to translate this into local context. The benchmark's ground truth treats Egyptian pound calculations as universally correct.
- **Datapoint citations:**
  - [D28] Example Economics (Univ), ID 11228 (Egypt): "إذا كان حجم الاستثمار المطلوب ١٠٠ر٠٠٠ جنيه...معدل العائد على الأموال المستثمرة هو: % ١٥" — Egyptian pound (جنيه) used in an ROI calculation presented as a general economics problem.

---

#### MINOR

#### MINOR Concern 9: One Arabic grammar question has an English-language question stem
- **Dimension(s):** IF
- **Severity:** MINOR
- **Observation:** In the Arabic Language (Grammar) configuration, one example (ID 12626) has an English question stem: "In the following Quranic verse, what is the correct parsing of the word ــكَ" — while the answer options are in Arabic. This appears to be a data entry anomaly from the madinaharabic.com source.
- **Deployment relevance:** Minor data quality concern; single example unlikely to materially affect aggregate scores, but suggests the data scraping pipeline did not filter out mixed-language question stems consistently.
- **Datapoint citations:**
  - [D19] Example Arabic Language (Grammar), ID 12626 (null country): "In the following Quranic verse, what is the correct parsing of the word ــكَ" — English stem in an Arabic grammar configuration.

#### MINOR Concern 10: Multiple configurations have null Country and null Level fields
- **Dimension(s):** IO, IC
- **Severity:** MINOR
- **Observation:** The Islamic Studies (General), Islamic Studies (All config), Arabic Language (General), Arabic Language (Grammar), and several other configurations have Country = null and Level = null for all sampled examples. These questions come from generic online quiz platforms (folderat.com, madinaharabic.com) rather than national exam sources, meaning they are not tied to any specific national curriculum or education level.
- **Deployment relevance:** Null-country questions cannot be used for country-specific evaluation. For the deployment's diagnostic use case (evaluating model performance per country and per level), these questions contribute noise to aggregate metrics without providing actionable per-country signal.
- **Datapoint citations:**
  - [D26] Examples Islamic Studies (All), IDs 165, 385, 46, 157, 54 — Country = null, Level = null.
  - [D27] Examples Arabic Language (General), IDs 11849–11736 — Country = null, Level = null, Source = madinaharabic.com.

#### MINOR Concern 11: Social Science (Middle School) may contain a questionable ground-truth label
- **Dimension(s):** OC
- **Severity:** MINOR
- **Observation:** Example ID 5261 from Social Science (Middle School) asks why natural gas is an important energy source and provides the answer "توافره بكميات قليلة" ("available in limited quantities") as correct. This appears to be an odd ground truth — natural gas importance is generally attributed to abundance, not scarcity. This could be an exam error carried over from the source, or a printing artifact. The benchmark's 96% accuracy ceiling acknowledges approximately 4% error rate.
- **Deployment relevance:** For a tutoring system, propagating potentially incorrect factual claims to students would be harmful. This single example is unlikely to be more than a data error within the acknowledged 4% noise floor, but it illustrates that some answer keys may be incorrect.
- **Datapoint citations:**
  - [D32] Example Social Science (MS), ID 5261 (null country): "يرجع السبب في ذلك إلى: توافره بكميات قليلة" — Answer states natural gas is important because it is available in limited quantities, which is contrary to standard economic reasoning.

#### MINOR Concern 12: Middle school Computer Science is Windows OS-centric with potentially dated content
- **Dimension(s):** IC
- **Severity:** MINOR
- **Observation:** The Computer Science (Middle School) sample contains multiple questions about Windows desktop interface operations (background images, right-click menus, icon arrangement, Windows system files). This is curriculum-specific to Jordan's circa 2015–2020 ICT curriculum and may not reflect UAE, Egyptian, or Palestinian CS middle school content, which may focus on different platforms or concepts.
- **Deployment relevance:** For a tutoring system supporting all eight countries' CS curricula, a heavily Windows-GUI-focused CS subset may misrepresent what CS knowledge looks like for students in other countries.
- **Datapoint citations:**
  - [D33] Example CS (MS), ID 7340 (Jordan): "لتخصيص صورة تحل محل الخلفية الافتراضية تنقر زر: خلفية سطح المكتب" — "To change the desktop background, click: Desktop Background" — Windows UI tutorial question.
  - [D33] Example CS (MS), ID 7343 (Jordan): "إذا تم حذف ملف من ملفات النظام Windows هل يؤثر ذلك على عمل النظام: يؤثر" — Windows system files question.

---

### Content Coverage Summary

The 185+ examples reviewed span all 40 subject-level configurations and provide a clear picture of the benchmark's content composition:

**Country distribution in sample:** Jordan is the dominant country across school-level humanities, social science, civics, history, geography, Arabic language, economics, general knowledge, and Islamic studies configurations. Palestine appears substantially in STEM subjects (Biology HS, CS Primary/HS, Physics HS, Math Primary, Geography Middle) and some social science. Egypt dominates all university-level non-CS configurations (Accounting, Economics, Management, Political Science). Morocco appears exclusively in Law (Professional). KSA appears in CS (University). UAE appears in Driving Test. Lebanon appears in Driving Test. Kuwait and several other countries have zero observed examples across the sample.

**Register and difficulty:** Questions are appropriate for their labeled educational level — primary questions are simple and short, high school questions involve more complex reasoning, and university questions involve domain-specific terminology. MSA is consistently used throughout, with appropriate formal register for educational contexts.

**Content types observed:** (1) Factual recall of national curriculum content — heavily Jordanian for school level; (2) definitional/conceptual questions in STEM and social science; (3) procedural/institutional knowledge (legal procedures, constitutional facts); (4) quantitative problems in mathematics and applied economics; (5) Arabic language morphology and grammar analysis.

**Quality issues:** OCR corruption is a material concern in some university-level PDFs, particularly management and political science from Egyptian sources. A small number of questions have null answer options (Option 3/4 = null when only 2-3 options provided) which is expected given the 2–5 option range. Some questions have truncated or incomplete text, likely from the original PDF scraping.

**Geographic representation gap confirmed in data:** No Kuwait or UAE examples observed outside the Driving Test. No Moroccan examples outside Law (Professional) and one or two Arabic language items. The Jordan-Egypt-Palestine dominance documented in the paper is directly observable in the data.

---

### Limitations

1. **Sample size per configuration:** Most configurations were sampled at 5–8 examples out of test splits ranging from 50–500+ questions. Individual configurations (especially smaller ones) may be substantially different from what the sample shows. Country distribution within configurations beyond Jordan/Egypt/Palestine is particularly uncertain.

2. **Kuwait coverage unverifiable:** No Kuwaiti examples appeared in any sampled configuration. This is consistent with the documented concern but cannot be definitively confirmed as zero-coverage from this sample alone — a full dataset scan would be needed.

3. **University-level sample is thin:** With ~6.1% of questions at university level (~889 total), each university subject configuration is small. The 5 examples sampled per university configuration may represent a substantial fraction of the total, making these configurations particularly sensitive to source diversity (or lack thereof).

4. **Law (Professional) is the only law configuration:** The sample cannot determine whether other law content is embedded in other humanities configurations. The Moroccan dominance of Law (Professional) in the sample may not generalize to all 299+ law questions identified by ArabLegalEval.

5. **Islamic studies madhab calibration:** The data does not contain any explicit madhab identifiers, and the question content observed does not clearly differentiate between madhab traditions. Confirming whether any questions are madhab-specific would require expert Islamic jurisprudence review, which is outside the scope of this data analysis.

6. **OCR corruption extent:** The Management (University) and Political Science (University) OCR corruption was observed in the sample but the total proportion of corrupted questions in these configurations cannot be estimated from 5-question samples.

7. **No inspection of few-shot split:** The `is_few_shot` field was observed (value = 0 for all sampled test examples), but the dev split (few-shot examples) was not sampled. Few-shot examples may have different country distributions.

