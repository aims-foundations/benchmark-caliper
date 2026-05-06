## Deployment Context

**Use case:** Support high school students (G10-12) in editing and revising their Arabic essay drafts before submitting them for grading.
**Target population:** high school students (G10-12) in Arab countries (especially Qatar)

# Validity Analysis: asap_plus_plus
**Target context:** Qatari and Arab High School Arabic Essay Writers (Grades 10–12)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 1 | Serious concern | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ⚠ | 1 | Serious concern | high |
| Output Ontology ⚠ | 1 | Serious concern | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ⚠ | 1 | Serious concern | high |
| **Average** | **1.0** | | |

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

ASAP++ is severely misaligned with the target deployment across all six validity dimensions, all of which were flagged HIGH priority in the elicitation. The benchmark provides English-only essays from native English-speaking US Grade 7–10 students, scored on US-pedagogy-derived genres (argumentative, source-dependent, narrative) by India-based English-MA annotators anchored to US holistic scores, with numeric ordinal output evaluated by QWK. The deployment requires Arabic (MSA) Grade 10–12 essays under Qatar MOEHE and other Arab national curricula, covering literary analysis, religious-text commentary, and cultural commentary genres absent from the benchmark, evaluated against Arab curriculum stakeholders, and producing natural-language revision suggestions with explanatory rationale. There is no overlap in language, script, age band, curriculum, annotator expertise, genre coverage, or output modality. ASAP++ is at best a methodological reference (multi-trait scoring structure, QWK reliability template) for a future Arabic AES effort; it cannot serve as a validity anchor for the deployment. More directly relevant Arabic resources — LAILA (7,859 high school essays, seven-trait rubric, QRDI-funded), QAES/QCAW (195 Qatari argumentative essays), and Arwi (Arabic feedback-generation system) — should replace ASAP++ as the primary references.

## Practical Guidance

### What This Benchmark Measures

ASAP++ measures the ability to predict numeric ordinal trait scores (content, organization, word choice, sentence fluency, conventions, and analogous traits) for English-language US student essays in argumentative, source-dependent, and narrative genres, evaluated against US-anchored ground truth via QWK. None of the strongest dimensions of the benchmark align with the target deployment; all six dimensions score 1.

### Construct Depth

Within its English/US scope, the benchmark provides moderate construct depth on multi-trait holistic scoring with reasonable inter-rater methodology (QWK-anchored QC). For the Arab high school Arabic writing construct, however, depth is effectively zero: the benchmark probes none of the rhetorical, morphological, diglossic, or curricular dimensions that define writing quality in MSA, and produces no evidence about feedback-generation quality.

### What Else You Need

Wholesale supplementation is required. Replace ASAP++ as the validity anchor with: (1) LAILA [WEB-12] for trait taxonomy and high school Arabic essay coverage, (2) QAES/QCAW [WEB-3] for Qatari-anchored argumentative writing, (3) Arwi [WEB-22] for Arabic feedback-generation methodology, and (4) recruit Qatar MOEHE-curriculum teacher annotators for genre-specific rubric validation across literary analysis, religious-text commentary, and cultural commentary essays. Build an Arabic NLP pipeline on CAMeL Tools / CAMeLBERT-MSA [WEB-7, WEB-9] rather than Stanford CoreNLP. Commission a feedback-generation evaluation framework (rubric-aligned human evaluation with Qatari teachers) since QWK cannot validate generated revision suggestions.

## Dimension Details

### Input Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark's category inventory consists of three essay types — argumentative/persuasive, source-dependent, and narrative/descriptive [Q12, Q13, Q14, Q15] — drawn from a US middle-school context. The deployment requires coverage of literary analysis, religious-text commentary, and cultural commentary genres that are standard in Arab high school curricula but entirely absent from the benchmark. The Qatar MOEHE curriculum confirms Arabic Literature as a distinct subject and Islamic Education as compulsory [WEB-11, WEB-5], yet no AES benchmark covers these genres in Arabic. The expert elicitation flagged IO as HIGH priority precisely because the benchmark's taxonomy omits the test-case types the deployment requires. Even within the persuasive genre that nominally overlaps, scoring logic is type-specific and embedded in English pedagogical norms [Q43, Q44, Q45].

**Strengths:**
- The conceptual move toward attribute-level (multi-trait) scoring across multiple essay types [Q4, Q18] is methodologically analogous to what an Arabic formative feedback system would target, as later Arabic AES work like LAILA's seven-trait rubric demonstrates [WEB-12].

**Checklist:**

- **IO-1**: The deployment requires at least five genres: persuasive/argumentative (مقالة إقناعية), explanatory/expository, literary analysis (مقالة تحليل أدبي), religious-text commentary (تفسير / تأمل نص ديني), and cultural commentary (مقالة ثقافية / اجتماعية), grounded in Qatar MOEHE Arabic Language and Arabic Literature curricula [WEB-10, WEB-11, WEB-5]. — _Sources: WEB-10, WEB-11, WEB-5_
- **IO-2**: Yes — literary analysis, religious-text commentary, and cultural commentary are all absent from the benchmark, which covers only argumentative/persuasive, source-dependent, and narrative/descriptive types [Q12, Q13, Q14, Q15]. — _Sources: Q12, Q13, Q14, Q15, WEB-11_
- **IO-3**: The narrative/descriptive category and source-dependent responses keyed to specific US source texts [Q14, Q15] introduce categories not aligned with formal Arab high school assessment, where literary analysis and religious-text engagement are more central [WEB-11]. — _Sources: Q14, Q15, WEB-11_
- **IO-4**: Category gaps — absence of literary analysis, religious commentary, and cultural commentary — represent severe construct underrepresentation. The benchmark also embeds genre-specific scoring rules (length-weighted for source-dependent; coherence/cohesion-weighted for argumentative) [Q43, Q44, Q45] that would not transfer to Arabic rhetorical norms even within the nominally overlapping argumentative genre. — _Sources: Q43, WEB-12_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q12] 'There are 3 types of essays in the dataset.' (p.2)
- [Q13] 'Argumentative / Persuasive essays - These are essays where the prompt is one in which the writer has to convince the reader about their stance for or against a topic...' (p.2)
- [Q14] 'Source-dependent responses - These essays are responses to a source text...' (p.2)
- [Q15] 'Narrative / Descriptive essays - These are essays where the prompt requires us to describe / narrate a story.' (p.2)
- [Q43] 'For source-dependent essays, we found out that the most important feature for content was length, while for argumentative / persuasive essays, it was coherence and cohesion features, followed by length.' (p.4)

*Web sources:*
- [WEB-11] Qatar MOEHE 2025–2026 curriculum covers Arabic Language and Arabic Literature as separate subjects
- [WEB-5] Islamic Education is compulsory in Qatar national curriculum schools for Qatari pupils and Arab passport holders
- [WEB-10] Qatar MOE curriculum standards portal identifies writing across literary engagement and creative writing strands
- [WEB-12] LAILA Arabic AES dataset uses a seven-trait rubric on 7,859 high school essays — the closest validated proxy for trait taxonomy in this deployment

</details>

**Information gaps:**
- Whether Quranic/religious-text commentary essays are graded within the Arabic Language curriculum versus only Islamic Education is not resolvable from open sources.
- Cross-country curricular variation among Arab nations for genre coverage and weighting is undocumented in open sources.

**Requires expert verification:**
- Genre inventory and weighting in Qatar MOEHE Grades 10–12 Arabic writing assessment
- Whether literary analysis essays follow distinct rubric structures across Arab national curricula

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark's input instances are ~13,000 essays written entirely by native English-speaking US students in Grades 7–10 [Q3, Q10] across 8 prompts. The deployment targets Arabic-language Grade 10–12 students under the Qatar MOEHE curriculum (and other Arab curricula), writing to prompts grounded in Arab cultural, literary, and Islamic frames of reference [WEB-10, WEB-11]. There is no overlap in language, age band, nationality, curriculum, or cultural frame of reference. The anonymization scheme (e.g., @ORGANIZATION1, @PERSON1) was itself a source of interpretive difficulty even for the English annotators [Q41], and would compound transfer issues. No Arabic-language instances exist in the dataset.

**Strengths:**
- The dataset is openly available for non-commercial research use under CC-BY-SA [Q51, Q52], so it could in principle serve as a methodological reference (not a content reference) for designing an Arabic counterpart.

**Checklist:**

- **IC-1**: Yes — Arab high school essay tasks require knowledge of Arabic literary tradition, Islamic ethical framing, classical rhetorical conventions (بلاغة / فصاحة), and country-specific civic content [WEB-11, cultural_norms_notes]. None of this is present in the benchmark inputs [Q10]. — _Sources: WEB-11, Q10_
- **IC-2**: No — the benchmark inputs are US student essays on US-curriculum prompts [Q3, Q10]; there is no alignment with Qatari/Arab cultural framing, Islamic values, or Arabic rhetorical norms. — _Sources: Q3, Q10, WEB-11_
- **IC-3**: Yes — all benchmark inputs require Western-specific knowledge (US topics, English-language conventions, US-anonymized named entities like '@PERSON1' standing for figures such as Donald Trump [Q41]) that does not transfer to Arab student writers. — _Sources: Q41, Q10_
- **IC-4**: INSUFFICIENT DOCUMENTATION — the benchmark documentation does not address recruiting regional annotators for re-validation; this would be a recommended remediation step.
- **IC-5**: Content issues are categorical: zero Arabic-language data, zero Arab student writers, zero culturally-anchored prompts. This is a complete content validity violation for the deployment. — _Sources: Q10, WEB-12, WEB-3_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q3] 'The ASAP AEG dataset comprises of approximately 13,000 essays, written across 8 prompts. The essays were written by students of class 7 to 10...' (p.1)
- [Q10] 'All the essays were written by native English speaking children from classes 7 to 10.' (p.2)
- [Q41] 'One of the major problems that the annotators faced was the fact that all the essays were anonymized. Named entities, like The New York Times would be referred to as @ORGANIZATION1, Donald Trump would be referred to as @PERSON1...' (p.4)
- [Q51] 'The resource is available online at https://cfilt.iitb.ac.in/˜egdata/.' (p.5)

*Web sources:*
- [WEB-10] Qatar MOE Arabic Language curriculum framework anchors Grades 1–12 writing standards
- [WEB-11] IMPACT-se review of Qatar 2025–2026 curriculum confirms Arabic Literature and politically/religiously contextualized content
- [WEB-12] LAILA dataset (7,859 Arabic high school essays) exists as a much more relevant content reference than ASAP++
- [WEB-3] ZaQQ/MDPI 2025: total Arabic AES corpus ~12,000 essays, none covering literary analysis or religious commentary genres

</details>

**Information gaps:**
- The benchmark does not document any provision for non-English content, so it is structurally unable to support Arabic input.

**Requires expert verification:**
- Specific Qatar/Arab essay prompt corpora that could substitute as content anchors (LAILA and QAES are candidates per [WEB-12, WEB-3]).

---

### Input Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark operates on English plain text with a feature pipeline (Zesch et al. attribute-independent features, Barzilay & Lapata entity grids) extracted via Stanford CoreNLP [Q31, Q32, Q33]. The deployment operates in MSA, written in right-to-left Arabic script with root-and-pattern morphology, optional diacritics (tashkeel), Arabic-specific punctuation (،, ؟), and potential Gulf Arabic dialect intrusion [writing_systems, languages.dialect_influence, WEB-3, WEB-4]. Stanford CoreNLP's English pipeline cannot be applied to Arabic text directly; the canonical Arabic tools (CAMeL Tools, Camel Morph MSA, CAMeLBERT-MSA) are entirely separate ecosystems [WEB-7, WEB-8, WEB-9]. This is a complete signal-distribution mismatch, not a parameter mismatch.

**Strengths:**
- The structural choice to use morphology- and discourse-aware features (entity grids, coherence features) is conceptually portable to Arabic if rebuilt on Arabic-specific tools such as CAMeL Tools [Q32, WEB-7].

**Checklist:**

- **IF-1**: Signal distributions are fundamentally different: English Latin-script LTR plain text [Q31, Q33] vs. Arabic RTL script with rich morphology and optional diacritics [writing_systems]. There is no overlap in encoding, script direction, or morphological structure. — _Sources: Q31, Q33_
- **IF-2**: Qatar's digital infrastructure supports Arabic text capture and processing well — internet penetration is ~99–100% [WEB-13, WEB-14] and the Qeducation LMS supports Arabic interfaces [WEB-15, WEB-17] — but the benchmark's English-only pipeline does not connect to this infrastructure. — _Sources: WEB-13, WEB-14, WEB-15, WEB-17_
- **IF-3**: Domain-specific form differences include: (a) RTL rendering and mixed-direction handling, (b) MSA/dialect code-mixing (empirically documented in Gulf student writing [WEB-3, WEB-4]), (c) diacritization decisions for literary/Quranic essays, (d) Arabic punctuation. None are addressed by the benchmark. — _Sources: WEB-3, WEB-4_
- **IF-4**: Form mismatches are total: the benchmark cannot ingest Arabic input at all without a complete pipeline replacement. This represents the most severe class of external validity violation. — _Sources: Q33, WEB-7, WEB-8_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q31] 'We used the attribute independent feature set provided by Zesch et al. (2015).' (p.3)
- [Q32] 'In addition to those features, we also made use of entity grid features described in Barzilay and Lapata (2005).' (p.3)
- [Q33] 'All the features were extracted using Stanford Core NLP (Manning et al., 2014).' (p.3)

*Web sources:*
- [WEB-7] CAMeL Tools provides MSA morphological analysis, POS, dialect ID and diacritization — the Arabic counterpart ecosystem to Stanford CoreNLP
- [WEB-8] Camel Morph MSA is the largest open-source MSA morphological analyzer (LREC-COLING 2024)
- [WEB-9] CAMeLBERT-MSA is the standard pre-trained Arabic encoder used in ZAEBUC, LAILA, and TAQEEM AES systems
- [WEB-3] MSA/Gulf-Arabic code-mixing in student writing is empirically documented but unresourced for AES
- [WEB-4] ZAEBUC-Spoken confirms MSA/Gulf/English code-switching among Gulf students

</details>

**Information gaps:**
- Whether any of the Zesch et al. attribute-independent features have validated Arabic equivalents specifically calibrated to high school student register.

**Requires expert verification:**
- Choice of Arabic morphological analyzer and tokenization scheme (e.g., MADA-style, CAMeL Tools defaults) for student writing input.

---

### Output Ontology — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark output ontology is a fixed integer score range [Q11] over a small set of attributes (content, organization, word choice, sentence fluency, conventions for narrative; analogous traits for other types) [Q16, Q17, Q18, Q19], with annotations described as gold standard for predicting attribute scores [Q50]. The deployment requires natural-language revision suggestions with explanatory rationale (per elicitation Q3/A3), which is a categorically different output space — not a numeric score taxonomy at all. Additionally, traits like 'word choice' and 'sentence fluency' are calibrated to English vocabulary range and syntactic variety; Arabic writing quality dimensions critical for this deployment include morphological correctness, classical rhetorical structure (بلاغة / فصاحة), and dialect intrusion handling [cultural_norms_notes, writing_systems.morphological_considerations], which are not represented.

**Strengths:**
- The trait inventory (content, organization, vocabulary/word choice, fluency, conventions) [Q19] partially overlaps with the seven-trait rubric used in LAILA [WEB-12] (relevance, organization, vocabulary, style, development, mechanics, grammar), so the methodological design is a useful precedent for an Arabic rubric — even if the labels themselves are not transferable.

**Checklist:**

- **OO-1**: The benchmark's label categories [Q19] are partially conceptually relevant (content, organization) but miss categories central to MSA writing (morphological correctness, rhetorical eloquence, dialect intrusion) [writing_systems, cultural_norms_notes]. — _Sources: Q19_
- **OO-2**: Missing categories include: morphological/grammatical correctness as a distinct trait, adherence to classical Arabic rhetorical norms (بلاغة), diacritical accuracy where applicable, and dialect-intrusion handling [writing_systems.morphological_considerations, languages.diglossia_note]. — _Sources: Q19, WEB-12_
- **OO-3**: Yes — 'word choice' and 'sentence fluency' [Q19] encode English vocabulary-range and syntactic-variety assumptions that map poorly onto MSA writing-quality criteria. — _Sources: Q19_
- **OO-4**: Stakeholder-driven taxonomy redesign is required. LAILA's seven-trait rubric on Qatari high-school-adjacent data [WEB-12] is the closest available proxy for an appropriate redesign; QAES (Qatari argumentative writing, 195 essays) [WEB-3] provides additional Qatar-anchored evidence. — _Sources: WEB-12, WEB-3_
- **OO-5**: Critically, the output is numeric scores, but the deployment requires natural-language feedback. This is a structural validity violation: the output construct is fundamentally different. [Q11, Q50] confirm the benchmark targets numeric attribute prediction only. — _Sources: Q11, Q50, WEB-22_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q11] 'We use the same score range as the overall score range of the essays.' (p.2)
- [Q16] 'The ASAP dataset already contains attribute scores for the narrative essays, namely content, organization, word choice, sentence fluency, conventions, etc.' (p.2)
- [Q18] 'Based on the types of essays, there are 2 sets of attributes.' (p.2)
- [Q19] 'There are 5 attributes for narrative essays, namely 1. Content... 2. Organization... 3. Word Choice...' (p.2)
- [Q50] 'These annotations can be used as a gold standard for future experiments in predicting different attribute scores.' (p.5)

*Web sources:*
- [WEB-12] LAILA's seven-trait rubric (relevance, organization, vocabulary, style, development, mechanics, grammar) on 7,859 Arabic high school essays — closest validated Arabic rubric
- [WEB-3] QAES Qatari Corpus of Argumentative Writing trait annotations provide Qatar-anchored taxonomy reference
- [WEB-22] Arwi system uses CEFR-level rubric, illustrating an alternative Arabic-validated output schema

</details>

**Information gaps:**
- No published official MOEHE rubric for Grades 10–12 Arabic writing was located in open sources [WEB-10]; LAILA serves as a proxy but is not authoritative.

**Requires expert verification:**
- Definition of trait inventory and weighting for Qatar Grades 10–12 from MOEHE rubric documents
- Cross-country trait taxonomy variation across Arab national curricula

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Ground-truth labels were produced by three India-based annotators with English MA-level training, English newspaper editorial experience, and high English exam/TOEFL scores [Q27, Q28, Q29, Q30, Q53], scoring single-pass [Q22, Q40] with anchoring to the original US ASAP raters' overall scores [Q23, Q25]. None of these qualifications confer expertise in Arabic writing assessment or Qatari/Arab curriculum norms. The anchoring mechanism [Q25, Q26] further embeds US rater judgments as the normative standard. Per the elicitation, OC was flagged HIGH priority because Qatar/Arab teachers may apply different MSA convention, organization, and style standards. Convergent validity with the deployment's regional stakeholders is essentially zero.

**Strengths:**
- The QC mechanism — second annotator triggered when any attribute differs by 2+ points from either original rater [Q24] — is methodologically sound as a template that could be re-applied with Arabic-curriculum annotators.
- Annotator credentials and roles are at least partially documented [Q27–Q30, Q53], enabling explicit comparison with required regional expertise.

**Checklist:**

- **OC-1**: No — labels reflect Indian English-MA annotators anchoring to US ASAP raters [Q23, Q25, Q30]. There is no Qatari/Arab curriculum stakeholder representation. — _Sources: Q23, Q25, Q30_
- **OC-2**: Disagreement with the regional population is expected to be very high: zero overlap in language, curriculum, or rubric tradition. The closest Arab-anchored rubric (LAILA seven-trait, [WEB-12]) was developed by separate teams and uses different trait definitions. — _Sources: WEB-12_
- **OC-3**: Annotator demographics are partially documented [Q27, Q28, Q29, Q30, Q53]: three named individuals, all India-based, all with MA-level English study, all with English-language editorial experience or high TOEFL/English exam scores. No Datasheet or Data Statement is referenced. — _Sources: Q27, Q28, Q29, Q30, Q53_
- **OC-4**: Re-annotation by representative Qatari/Arab teachers is required and is the only route to label validity for this deployment. QAES/QCAW's Qatari-context annotation work [WEB-3] and LAILA's Arabic high school annotation [WEB-12] are precedents. — _Sources: WEB-12, WEB-3_
- **OC-5**: Aggregation anchors to the original US holistic score [Q25] — a strong erasure mechanism for any non-US perspective. The 0.9 Pearson correlation justification [Q26] is circular: it merely shows the original US raters' holistic and trait scores agree with each other. — _Sources: Q25, Q26_
- **OC-6**: Label issues are categorical: ground truth encodes US-rater judgments mediated by Indian English annotators, with no path to Arab curriculum norms. This violates both convergent and external validity for the deployment. — _Sources: Q23, Q30_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'Unlike the ASAP AEG dataset in which every essay was annotated by 2 annotators, we use only 1 annotator here for each essay.' (p.3)
- [Q23] 'For the ground truth, we make use of the overall score of the essays given by the original annotators of the ASAP AEG dataset.' (p.3)
- [Q24] 'In case the scoring of a particular attribute for a particular prompt differs from either of the original scorers by 2 or more points, the essay is then annotated by another annotator.' (p.3)
- [Q25] 'The final score that is chosen is the one from the annotator that is closest to the overall scores.' (p.3)
- [Q27] 'We made use of a total of three annotators to annotate the essays.' (p.3)
- [Q28] 'Each of the annotators had competence in English, either by scoring quite high marks in their high school exams (over 90% in English), or scoring over 110 in ToEFL.' (p.3)
- [Q30] 'All the annotators have either studied or are studying English at a Master of Arts (MA) level.' (p.3)
- [Q53] 'We thank the annotators of our task - Advaith Jayakumar, Janice Pereira and Elaine Mathias...' (p.5)

*Web sources:*
- [WEB-12] LAILA used annotators trained on Arab high school writing — example of appropriate annotator profile for this deployment
- [WEB-3] QAES annotated Qatari argumentative writing with trait-specific conventions appropriate to Qatari context

</details>

**Information gaps:**
- No information on Arabic-language competence of any benchmark annotator (none is claimed); paper does not mention Arabic at all.

**Requires expert verification:**
- Whether Qatari teacher rubric judgments converge or diverge meaningfully from other Arab curriculum bodies (per elicitation Q2/A2).

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
The benchmark's output form is integer ordinal scores per trait, evaluated by Quadratic Weighted Kappa using an Ordinal Class Classifier with Random Forest internals under 5-fold CV [Q34, Q35, Q36, Q37, Q38, Q39]. The deployment explicitly requires free-text natural-language revision suggestions with explanatory rationale (elicitation Q3/A3). QWK has no mechanism to evaluate the quality, actionability, or pedagogical appropriateness of generated feedback text. This is a complete output-form mismatch: numeric ordinal classification vs. open-ended generation. The benchmark cannot validate the deployment's output modality at all.

**Strengths:**
- QWK is a methodologically appropriate metric for ordinal-score agreement and is the field standard [Q35, Q36, Q37]; if the deployment ever needs an internal numeric score head (e.g., for triggering feedback templates), the QWK methodology is reusable.

**Checklist:**

- **OF-1**: No — expected output modality is numeric ordinal scores [Q34, Q38], not natural-language feedback. The deployment requires generated Arabic-script revision suggestions with rationale (elicitation Q3/A3). — _Sources: Q34, Q38_
- **OF-2**: Not applicable directly: text-to-speech is not the deployment's primary output channel, but the deployment does require Arabic-script text generation, which the benchmark does not produce or evaluate at all. RTL Arabic rendering on the Qeducation LMS [WEB-15, WEB-17] would be the relevant infrastructure consideration. — _Sources: WEB-15, WEB-17_
- **OF-3**: Literacy is high in Qatar (general internet penetration ~99–100% suggests strong digital access [WEB-13, WEB-14]); accessibility for Arabic-script text feedback on the Qeducation mobile app is supported [WEB-17]. The benchmark does not address any of this because it produces no text output. — _Sources: WEB-13, WEB-14, WEB-17_
- **OF-4**: The mismatch is total: numeric ordinal score outputs evaluated by QWK [Q34–Q39] cannot validate generated explanatory feedback. External validity for the deployment's output form is zero. — _Sources: Q34, Q35, Q37, Q38, Q39, WEB-22_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q34] 'We evaluate each of the annotators using Cohen's Kappa, with quadratic weights - i.e. Quadratic Weighted Kappa (QWK) (Cohen, 1968).' (p.4)
- [Q35] 'We chose this as the evaluation metric (as compared to accuracy and weighted F-Score) because of the following reasons: Unlike accuracy and F-Score, Kappa takes into account random agreement.' (p.4)
- [Q37] 'To the best of our knowledge, all of the papers using the ASAP dataset make use of this as the evaluation metric.' (p.4)
- [Q38] 'We made use of the Ordinal Class Classifier (Frank and Hall, 2001) in Weka... We used the Random Forest classifier (Breiman, 2001) as the internal classifier.' (p.4)
- [Q39] 'We used 5-fold cross validation to get the results for each attribute for each prompt.' (p.4)

*Web sources:*
- [WEB-15] Qeducation LMS (CYPHER) supports Arabic-language interface — relevant target platform for natural-language Arabic feedback delivery
- [WEB-17] Official 'Qatar Education' mobile app provides RTL Arabic delivery channel
- [WEB-22] Arwi (CAMeLBERT-MSA, ZAEBUC) demonstrates the kind of feedback-generation output form the deployment requires; QWK is insufficient to evaluate such systems

</details>

**Information gaps:**
- How feedback-generation quality should be evaluated for Arabic high school writing is itself an open methodological question; no validated framework exists [WEB-22].

**Requires expert verification:**
- Pedagogical appropriateness criteria for Arabic feedback text (e.g., register, formality, use of Arabic technical grammar terminology) from Qatari teacher experts.

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** Benchmark covers only argumentative/persuasive, source-dependent, and narrative/descriptive genres; deployment requires literary analysis, religious-text commentary, and cultural commentary.

**Recommendation:** Construct a genre inventory aligned with Qatar MOEHE Arabic Language and Arabic Literature curricula [WEB-10, WEB-11], using LAILA's prompt set [WEB-12] as a partial proxy and commissioning new Qatari teacher-authored prompts for the three missing genres.

### Input Content ⚠

**Gap:** Benchmark essays are English US Grade 7–10 student writing; deployment requires Arabic Grade 10–12 student writing under Arab curricula.

**Recommendation:** Replace ASAP++ entirely as a content reference. Use LAILA (7,859 essays) [WEB-12] as the primary corpus and QAES/QCAW [WEB-3] as the Qatari-anchored validation set; collect new student writing from Qatar MOEHE schools via the Qeducation LMS [WEB-15, WEB-17].

### Input Form ⚠

**Gap:** English Latin-script Stanford CoreNLP feature pipeline cannot ingest Arabic input.

**Recommendation:** Rebuild the input pipeline on CAMeL Tools / Camel Morph MSA / CAMeLBERT-MSA [WEB-7, WEB-8, WEB-9] with explicit handling for RTL rendering, optional diacritization for literary/Quranic essays, Arabic punctuation, and MSA/Gulf-Arabic dialect intrusion detection [WEB-3, WEB-4].

### Output Ontology ⚠

**Gap:** Numeric ordinal score taxonomy with English-anchored traits ('word choice', 'sentence fluency'); deployment requires natural-language feedback aligned to Arabic rhetorical norms.

**Recommendation:** Adopt a trait taxonomy aligned to Qatari MOEHE rubrics (commission expert elicitation to fill the open-source rubric gap [WEB-10]); use LAILA's seven-trait rubric [WEB-12] as a starting point and add categories for morphological correctness, classical rhetorical eloquence (بلاغة), and dialect intrusion; redefine output as natural-language revision suggestions with rationale.

### Output Content ⚠

**Gap:** Ground truth produced by India-based English-MA annotators anchored to US ASAP raters; no Arab curriculum stakeholder representation.

**Recommendation:** Re-annotate any Arabic AES dataset used for this deployment with Qatar MOEHE-trained Arabic teachers, using a multi-rater protocol with explicit disagreement resolution; document annotator demographics and curriculum training in a Datasheet/Data Statement.

### Output Form ⚠

**Gap:** QWK-evaluated numeric scores cannot validate natural-language revision suggestions with explanatory rationale.

**Recommendation:** Develop a feedback-generation evaluation framework with Qatari teachers (e.g., rubric-aligned ratings of feedback usefulness, accuracy, and pedagogical appropriateness), using Arwi [WEB-22] as a methodological reference, and retain QWK only as a secondary check on any internal numeric score head.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | output_content | "In this paper, we describe the creation of a resource - ASAP++ - which is basically annotations of the Automatic Student Assessment Prize's Automatic Essay Grading dataset. These annotations are scores for different attributes of the essays, such as content, word choice, organization, sentence fluency, etc. Each of these essays is scored by an annotator." |
| Q2 | 1 | output_form | "We also report the results of each of the attributes using a Random Forest Classifier using a baseline set of attribute independent features as described by Zesch et al. (2015)." |
| Q3 | 1 | input_content | "The ASAP AEG dataset comprises of approximately 13,000 essays, written across 8 prompts. The essays were written by students of class 7 to 10. Each essay was evaluated by 2 evaluators. 6 out of the 8 prompts only have overall scores. Only 2 of them have scores for individual essay attributes, like content, organization, style, etc." |
| Q4 | 1 | input_ontology | "Our contribution is the scoring of individual attributes of the essays, like content, organization, style, etc. in the ASAP dataset for the remainder of the essays." |
| Q5 | 1 | input_ontology | "A lot of the work in essay grading today makes use of the ASAP AEG dataset. However, most of the essays only have an overall score, not attribute-specific scores. This limitation limits the utility of this dataset for predicting the scores of particular attributes of essays." |
| Q6 | 1 | input_ontology | "However, most of them (in particular the deep learning systems) are constrained by the fact that there are very few prompts to handle scoring of individual attributes." |
| Q7 | 1 | input_ontology | "While there has been a lot of work done in overall essay scoring, not much has been done with respect to scoring particular attributes of essays. Some of the attributes that have been scored include organization (Persing et al., 2010), prompt adherence (Persing and Ng, 2014), coherence (Somasundaran et al., 2014)." |
| Q8 | 1 | input_content | "The entire ASAP dataset has nearly 13,000 essays across 8 prompts. 6 of those 8 prompts, comprising nearly 10,400 essays, only have an overall score." |
| Q9 | 1 | output_content | "Sandeep Mathias, Pushpak Bhattacharyya Department of Computer Science and Engineering Indian Institute of Technology, Bombay" |
| Q10 | 2 | input_content | "All the essays were written by native English speaking children from classes 7 to 10." |
| Q11 | 2 | output_ontology | "We use the same score range as the overall score range of the essays." |
| Q12 | 2 | input_ontology | "There are 3 types of essays in the dataset." |
| Q13 | 2 | input_ontology | "Argumentative / Persuasive essays - These are essays where the prompt is one in which the writer has to convince the reader about their stance for or against a topic (for example, free speech in public colleges)." |
| Q14 | 2 | input_ontology | "Source-dependent responses - These essays are responses to a source text, where the writer responds to a question about the text (for instance, describing the writer's opinion about an incident that happened to him in the text)." |
| Q15 | 2 | input_ontology | "Narrative / Descriptive essays - These are essays where the prompt requires us to describe / narrate a story." |
| Q16 | 2 | output_ontology | "The ASAP dataset already contains attribute scores for the narrative essays, namely content, organization, word choice, sentence fluency, conventions, etc." |
| Q17 | 2 | output_ontology | "Since we already have scores present for the narrative essays, we describe the scores for the other types of essays." |
| Q18 | 2 | output_ontology | "Based on the types of essays, there are 2 sets of attributes." |
| Q19 | 2 | output_ontology | "There are 5 attributes for narrative essays, namely 1. Content: The quantity of relevant text present in the essay. 2. Organization: The way the essay is structured. 3. Word Choice: The choice and aptness of the vocabulary used in the essay." |
| Q20 | 3 | output_content | "Each of the essays in a particular prompt were scored by an annotator." |
| Q21 | 3 | input_form | "Each prompt was split into sets of 100 essays each, with the assumption that a set would correspond to a week's worth of time for the annotator." |
| Q22 | 3 | output_content | "Unlike the ASAP AEG dataset in which every essay was annotated by 2 annotators, we use only 1 annotator here for each essay." |
| Q23 | 3 | output_content | "For the ground truth, we make use of the overall score of the essays given by the original annotators of the ASAP AEG dataset." |
| Q24 | 3 | output_content | "In case the scoring of a particular attribute for a particular prompt differs from either of the original scorers by 2 or more points, the essay is then annotated by another annotator." |
| Q25 | 3 | output_content | "The final score that is chosen is the one from the annotator that is closest to the overall scores." |
| Q26 | 3 | output_content | "One of the reasons that we do this is because, in the 2 prompts that were rated by the original raters, there is a very high Pearson correlation (nearly 0.9) between the overall scores and the individual attribute scores." |
| Q27 | 3 | output_content | "We made use of a total of three annotators to annotate the essays." |
| Q28 | 3 | output_content | "Each of the annotators had competence in English, either by scoring quite high marks in their high school exams (over 90% in English), or scoring over 110 in ToEFL." |
| Q29 | 3 | output_content | "Each of them also had some experience in evaluating texts, such as interning at The Hindu (a top English newspaper in India), being the chief editor of the college magazine, etc." |
| Q30 | 3 | output_content | "All the annotators have either studied or are studying English at a Master of Arts (MA) level." |
| Q31 | 3 | input_form | "We used the attribute independent feature set provided by Zesch et al. (2015)." |
| Q32 | 3 | input_form | "In addition to those features, we also made use of entity grid features described in Barzilay and Lapata (2005)." |
| Q33 | 3 | input_form | "All the features were extracted using Stanford Core NLP (Manning et al., 2014)." |
| Q34 | 4 | output_form | "We evaluate each of the annotators using Cohen's Kappa, with quadratic weights - i.e. Quadratic Weighted Kappa (QWK) (Cohen, 1968)." |
| Q35 | 4 | output_form | "We chose this as the evaluation metric (as compared to accuracy and weighted F-Score) because of the following reasons: Unlike accuracy and F-Score, Kappa takes into account random agreement." |
| Q36 | 4 | output_form | "Weighted Kappa, takes into account the distance between the actual score and the reported score. Quadratic weights reward matches and penalize mismatches more than linear weights." |
| Q37 | 4 | output_form | "Due to these reasons, this is one of the most used evaluation metrics to evaluate the performance of essay grading systems. To the best of our knowledge, all of the papers using the ASAP dataset make use of this as the evaluation metric." |
| Q38 | 4 | output_form | "We made use of the Ordinal Class Classifier (Frank and Hall, 2001) in Weka (Frank et al., 2016). This classifier is a meta-classifier, that first converts ordinal data into categorical data, before running an internal classifier on the data. We used the Random Forest classifier (Breiman, 2001) as the internal classifier." |
| Q39 | 4 | output_form | "We used 5-fold cross validation to get the results for each attribute for each prompt." |
| Q40 | 4 | output_content | "Most of the essays required only a single annotator. Only about a sixth of the essays required a second annotator." |
| Q41 | 4 | input_content | "One of the major problems that the annotators faced was the fact that all the essays were anonymized. Named entities, like The New York Times would be referred to as @ORGANIZATION1, Donald Trump would be referred to as @PERSON1, etc." |
| Q42 | 4 | output_content | "The annotators were instructed not to penalize the essays because of the anonymizations, but were told to replace them with placeholders (like @PERSON1 being replaced by either Joe, or Jane, etc. wherever applicable)." |
| Q43 | 4 | input_ontology | "For source-dependent essays, we found out that the most important feature for content was length, while for argumentative / persuasive essays, it was coherence and cohesion features, followed by length." |
| Q44 | 4 | input_ontology | "For source-dependent essays, the coherence and cohesion feature set is the most important feature set for each of the other 3 attributes." |
| Q45 | 4 | input_ontology | "For persuasive / argumentative essays, coherence and cohesion features are the most important features for 4 of the 5 attributes." |
| Q46 | 5 | input_content | "In this paper, we present a manually annotated dataset for automated essay grading." |
| Q47 | 5 | output_content | "The annotation was done for different attributes of the essays." |
| Q48 | 5 | output_content | "Most of the essays were annotated by a single annotator." |
| Q49 | 5 | output_content | "However, about a sixth of them were annotated by a second annotator." |
| Q50 | 5 | output_ontology | "These annotations can be used as a gold standard for future experiments in predicting different attribute scores." |
| Q51 | 5 | input_content | "The resource is available online at https://cfilt.iitb.ac.in/˜egdata/." |
| Q52 | 5 | input_content | "The resource is available for non-commercial research use under the Creative Commons Attribution-ShareAlike License." |
| Q53 | 5 | output_content | "We thank the annotators of our task - Advaith Jayakumar, Janice Pereira and Elaine Mathias - for their help in creating this resource." |
| Q54 | 5 | output_content | "We also thank members of CFILT at IIT Bombay for their valuable comments and suggestions." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://www.trade.gov/country-commercial-guides/qatar-education-and-training-services-industry-snapshot |
| WEB-2 | https://www.data.gov.qa/explore/dataset/c1-students-in-schools/ |
| WEB-3 | https://www.mdpi.com/2306-5729/10/9/148 |
| WEB-4 | https://arxiv.org/html/2403.18182v1 |
| WEB-5 | https://www.qisweb.qis.org/arabic-department/ |
| WEB-6 | https://consulting-haus.com/wp-content/uploads/2023/09/CH_Education_Sector-Overview_September-2023.pdf |
| WEB-7 | https://aclanthology.org/2020.lrec-1.868.pdf |
| WEB-8 | https://aclanthology.org/2024.lrec-main.240/ |
| WEB-9 | https://nyuad.nyu.edu/en/research/faculty-labs-and-projects/computational-approaches-to-modeling-language-lab/resources.html |
| WEB-10 | http://www.sec.gov.qa/En/Education/Pages/GradeAndSubject.aspx |
| WEB-11 | https://www.impact-se.org/wp-content/uploads/Qatar-Report-2026-final.pdf |
| WEB-12 | https://arxiv.org/abs/2512.24235 |
| WEB-13 | https://datareportal.com/reports/digital-2026-qatar |
| WEB-14 | https://thepeninsulaqatar.com/article/18/02/2025/at-100-qatar-continues-to-lead-in-global-internet-penetration |
| WEB-15 | https://www.cypherlearning.com/blog/k-20/qatar-march-workshop-recap-empowering-students-teachers-and-parents-with-digital-technology-for-learning |
| WEB-16 | https://link.springer.com/chapter/10.1007/978-981-97-9667-0_5 |
| WEB-17 | https://play.google.com/store/apps/details?id=app.qeducation.edu.gov.qa |
| WEB-18 | https://sites.google.com/view/zaebuc/home |
| WEB-19 | https://nyuscholars.nyu.edu/en/publications/zaebuc-an-annotated-arabic-english-bilingual-writer-corpus |
| WEB-20 | https://arxiv.org/abs/2407.11212 |
| WEB-21 | https://arxiv.org/html/2604.17569 |
| WEB-22 | https://arxiv.org/html/2504.11814v1 |
| WEB-23 | https://camel-lab.github.io/camel_tools_updates/2020/09/08/camel-tools-release-v1.0.0.html |
| WEB-24 | https://arxiv.org/html/2502.13520 |

---

