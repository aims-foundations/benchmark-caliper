I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **ASAP++: Enriching the ASAP Automated Essay Grading Dataset with Essay Attribute Scores** is valid for use in **Qatari and Arab High School Arabic Essay Writers (Grades 10–12)**.

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

- **Name**: asap_plus_plus
- **Full Name**: ASAP++: Enriching the ASAP Automated Essay Grading Dataset with Essay Attribute Scores
- **Domain**: Automated Essay Grading / Writing Quality Assessment
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2018

### Benchmark Documentation

## Key characteristics relevant to validity analysis

### 1. Input Ontology
ASAP++ covers three essay types: argumentative/persuasive, source-dependent, and
narrative/descriptive [Q12, Q13, Q14, Q15]. Within each type, the benchmark measures
a fixed set of writing attributes — content, organization, word choice, sentence fluency,
and conventions for narrative essays [Q19], with analogous attributes for the other
two types [Q18]. The taxonomy was designed to broaden prior attribute-level work that
covered only a handful of traits such as organization, prompt adherence, and coherence
[Q7], and ASAP++ extends this across 6 prompts [Q4, Q5].

From a deployment validity perspective, this taxonomy is severely misaligned with the
target use case of Qatari and Arab high school students. The three essay types are drawn
entirely from a US middle-school context and do not include literary analysis,
religious-text commentary, or cultural commentary — genres that are standard in Arab
high school curricula [Q13, Q14, Q15]. Feature analysis also confirms that the scoring
logic is type-specific and embedded in English-language US pedagogical norms: source-
dependent essays weight length for content, while argumentative essays prioritize
coherence and cohesion [Q43, Q44, Q45]. Deep learning systems are additionally
constrained by the small number of prompts available [Q6], further limiting coverage.
There is no mention of Islamic rhetorical conventions, Arabic genre norms, or
curricular frameworks beyond the US context. This represents a fundamental Input
Ontology gap: the benchmark's category inventory does not contain the test-case types
the deployment requires.

### 2. Input Content
The underlying dataset comprises approximately 13,000 essays written across 8 prompts
by US students in Grades 7–10, each originally evaluated by 2 raters [Q3]. ASAP++
adds attribute annotations to the 6 prompts — approximately 10,400 essays — that
previously had only holistic scores [Q8]. Critically, all essays were written by
native English-speaking children [Q10]. The annotated dataset is publicly available
for non-commercial research use [Q51].

From a deployment validity perspective, the source population is entirely incompatible
with the deployment target. The essays originate from native English-speaking US
middle-schoolers writing to culturally embedded American prompts [Q10, Q3]; the
deployment targets Arabic-language high school students (Grades 10–12) in Qatar and
other Arab countries writing to prompts grounded in Arab cultural, literary, and
religious contexts. There is no overlap in language, nationality, curriculum, or
cultural frame of reference. The benchmark presents this as a data resource [Q46],
but makes no claim of cross-lingual or cross-cultural transferability, and no
Arabic-language instances are present anywhere in the dataset.

### 3. Input Form
For feature extraction, ASAP++ uses the attribute-independent feature set from Zesch
et al. (2015), supplemented by entity grid coherence features from Barzilay and
Lapata (2005), with all features extracted using Stanford CoreNLP [Q31, Q32, Q33].
Essays were batched for annotation in sets of approximately 100 [Q21]. The benchmark
operates entirely on English plain text.

From a deployment validity perspective, the benchmark is built on an exclusively
English-language signal chain. The deployment operates in Modern Standard Arabic (MSA),
which uses a right-to-left Arabic script, a richer root-and-pattern morphological
system, and an entirely different NLP preprocessing ecosystem. The feature pipeline —
including entity grids, coherence features, and the Zesch et al. attribute-independent
features — was designed and validated for English and cannot be directly applied to
Arabic text [Q33]. No Arabic tokenization, morphological analysis, or diacritical
handling is mentioned anywhere in the paper. This represents the most fundamental
form of Input Form invalidity: not a resolution or encoding mismatch, but a complete
language-script incompatibility.

### 4. Output Ontology
ASAP++ uses the same score range as the original ASAP holistic scores [Q11]. Two sets
of attributes are defined based on essay type [Q18]: the narrative set (content,
organization, word choice, sentence fluency, conventions) was already present in the
original ASAP dataset [Q16], while ASAP++ adds analogous attribute scores for
argumentative/persuasive and source-dependent essay prompts [Q17]. These annotations
are described as a gold standard for future attribute-score prediction [Q50].

From a deployment validity perspective, the label taxonomy is misaligned on multiple
axes. First, categories like "word choice" and "sentence fluency" carry implicit
English-language assumptions — vocabulary range and syntactic variety in English —
that do not map cleanly onto MSA writing quality criteria, where morphological
correctness, diacritical accuracy, and adherence to Arabic rhetorical structure may
be more salient. Second, and more critically, the deployment requires natural-language
revision suggestions with explanatory rationale rather than numeric trait scores
[Q11, Q50]. The benchmark's output ontology was never designed to validate a
feedback-generation system, and using it as such would constitute a fundamental
validity category error.

### 5. Output Content
Each essay was scored by a single annotator [Q20, Q22]. Quality control required a
second annotator when any attribute score differed from either original ASAP rater by
2 or more points [Q24], with the final label chosen as the score closest to the
original holistic score [Q25]; in practice only about one-sixth of essays required
a second pass [Q40]. Ground truth was anchored to the original ASAP raters' overall
scores [Q23]. Three annotators were used in total [Q27, Q53]: all were India-based
English-language specialists with MA-level English training [Q30], editorial experience
at English-language publications [Q29], and high English exam scores or TOEFL
performance [Q28]. Annotators were instructed to substitute plausible placeholders
for anonymized named entities rather than penalizing essays for the anonymization
[Q42], though the anonymization itself posed interpretive difficulties [Q41].

From a deployment validity perspective, the annotator profile reveals a significant
mismatch with the target deployment context [Q9]. The annotators are India-based
English specialists judging US student essays by inferred US curriculum standards
using ground-truth anchoring on original US rater scores [Q23]. None of the described
qualifications — English MA training, Indian newspaper editorial experience, TOEFL
scores — confer expertise in Arabic writing quality assessment or Qatari/Arab
curriculum norms. The quality-control mechanism of anchoring to holistic scores [Q25]
further embeds US rater judgments as the normative standard, with no mechanism for
capturing how Arab teachers or curriculum bodies would evaluate writing quality.
Label transfer to an Arabic-language Qatari deployment is highly unreliable under
this annotator profile.

### 6. Output Form
The primary evaluation metric is Quadratic Weighted Kappa (QWK), chosen over accuracy
and F-score because it accounts for both random agreement and the ordinal distance
between predicted and actual scores [Q34, Q35, Q36]. QWK is the dominant metric
across all prior work using the ASAP dataset [Q37]. The baseline uses an Ordinal
Class Classifier in Weka with a Random Forest internal classifier, evaluated via
5-fold cross-validation [Q38, Q39]. Inter-annotator agreement between ASAP++ annotators
and the original ASAP raters is also reported using QWK [Q2, Q34].

From a deployment validity perspective, the benchmark's evaluation framework is entirely
built around ordinal numeric scores and agreement metrics between human raters and
predicted scores. The deployment requires free-text, actionable revision suggestions
with explanatory rationale — not numeric labels. QWK has no mechanism for evaluating
the quality, actionability, or pedagogical appropriateness of natural-language feedback.
This is not a minor gap but a complete mismatch: there is no output form overlap
between what the benchmark measures (numeric trait score agreement) and what the
deployment produces (explanatory revision suggestions for student writers).

### Stated Limitations
The authors acknowledge that the original ASAP dataset's lack of attribute-specific
scores limits its utility for attribute-level prediction research [Q5], and that deep
learning systems are further constrained by the small number of prompts [Q6]. They
note a high Pearson correlation (~0.9) between holistic and attribute scores as
justification for the quality-control anchoring mechanism [Q26], though this
circularity is not critically examined. Annotators faced difficulty with anonymized
named entities [Q41]. The dataset is released under a Creative Commons
Attribution-ShareAlike License restricted to non-commercial research use [Q52].
None of the stated limitations address linguistic, cultural, or geographic scope —
there is no acknowledgment that the benchmark is limited to English-language essays,
US curriculum contexts, or native English-speaking students.


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

## Regional Context

```yaml
name: Qatari and Arab High School Arabic Essay Writers (Grades 10–12)
abbreviation: QA-HS-AES
deployment_context:
  use_case: AI-assisted formative feedback on Arabic essay drafts before formal grading.
    The system provides natural-language revision suggestions with explanatory rationale
    for each writing trait, targeting student writers in Grades 10–12 preparing academic
    essays under Arab national curricula.
  primary_geography: Qatar
  secondary_geography: Arab countries broadly (Egypt, Saudi Arabia, Jordan, Lebanon,
    and others), with reduced reliability outside Qatar due to curricular divergence
  institutional_anchor: Qatar national curriculum (primary); other Arab national curricula
    (secondary, partially divergent)
target_population:
  role: High school student writers (Grades 10–12) preparing formal academic essays
    for graded assessment
  age_band: approximately 15–18 years old
  grade_levels:
  - Grade 10
  - Grade 11
  - Grade 12
  language_profile: Modern Standard Arabic (MSA) as the formal written register; Gulf
    Arabic dialect influence possible in Qatari students' writing; other regional
    dialects (Egyptian, Levantine, Hijazi) possible in secondary populations
  curriculum_context: Qatar national curriculum is the primary anchor. Students write
    to essay prompts set within Qatari pedagogical and cultural norms. Secondary populations
    follow Egyptian, Saudi, Jordanian, or Lebanese national curricula with partially
    divergent writing conventions and rubric standards.
  population_size_qatar_g10_12: 'Approximately 53,000–55,000 total secondary school
    students (all grades, public and private) as of the 2020–21 academic year; Grade
    10–12 cohort estimated at roughly 35,000–40,000, spread across 168 secondary schools.
    Note: this figure covers all secondary students regardless of nationality or curriculum
    type; the Arabic-curriculum-only subset will be smaller. Grade-specific breakdowns
    for Grades 10–12 alone are not publicly disaggregated at this level. Source: US
    Commercial Service Qatar Education snapshot — [WEB-1];
    Qatar Open Data portal (student-level data available but requires direct query)
    — [WEB-2]'
  gender_composition_notes: 'Qatar public schools are free-of-charge and generally
    separated by gender; public schools are preferred by Qatari families at both primary
    and secondary levels. Both male and female student cohorts are in scope for this
    deployment. Any system evaluation should verify performance parity across gender
    cohorts. Source: US Commercial Service Qatar — [WEB-1]'
languages:
  primary_written: Modern Standard Arabic (MSA / الفصحى)
  dialect_influence:
    primary: Gulf Arabic (Qatari variety) — may surface in vocabulary choice, idiomatic
      expressions, or informal constructions within otherwise MSA student essays
    secondary:
    - Egyptian Arabic (for Egyptian-curriculum secondary population)
    - Levantine Arabic (for Jordanian/Lebanese-curriculum secondary population)
    - Hijazi/Najdi Arabic (for Saudi-curriculum secondary population)
    note: 'MSA/Gulf Arabic code-mixing in formal student writing is an empirically
      undercharacterized problem. The ZAEBUC-Spoken corpus documents active code-switching
      between MSA, Gulf Arabic, and English among Gulf university students, confirming
      the phenomenon is real. Diglossic variation creates processing challenges: roughly
      58% of common vocabulary differs between MSA and dialectal variants such as
      Egyptian Arabic, and dialects often abandon MSA verb–subject–object word order.
      No NLP dataset specifically targets MSA/Gulf-Arabic code-mixing in formal high
      school writing. Source: ZaQQ/MDPI 2025 — [WEB-3];
      ZAEBUC-Spoken — [WEB-4]'
  diglossia_note: MSA is the expected written norm in formal academic essays; however,
    students may inadvertently introduce dialect features. The feedback system must
    be calibrated to recognize and comment on dialect intrusion as a correctable feature
    without over-penalizing register variation that falls within acceptable pedagogical
    tolerance.
  instruction_language: 'Arabic is the primary medium of instruction for Arabic-language
    essay courses in Qatar national curriculum schools. Qatar''s MOE (MOEHE) mandates
    Arabic Language as a core compulsory subject for all Qatari pupils and Arab passport
    holders from Year 1 through Year 12 (continuing through secondary). International
    and private schools in Qatar operate under 23 different curricula (British curriculum
    leading at 45.8% of private schools), where English may be the parallel medium;
    the Arabic national curriculum is the primary deployment anchor. Source: Qatar
    International School Arabic Department — [WEB-5];
    Consulting Haus K-12 Qatar sector report 2023 — [WEB-6]'
writing_systems:
  primary_script: Arabic script (right-to-left, Unicode Arabic block)
  morphological_considerations: MSA uses a root-and-pattern (trilateral root) morphological
    system with rich inflectional morphology. Morphological correctness (verb conjugation,
    noun-adjective agreement, dual/plural forms, case endings) is a salient quality
    dimension in student writing that differs fundamentally from English writing quality
    metrics.
  diacritics: Tashkeel (short vowel diacritics / حركات) are generally omitted in student
    prose but may be relevant in literary or Quranic text commentary essays where
    diacritical accuracy signals comprehension. NLP tools must handle both diacritized
    and undiacritized input.
  punctuation_and_layout: Arabic punctuation conventions differ from English (e.g.,
    Arabic comma ،, Arabic question mark ؟). RTL rendering and mixed-direction text
    (e.g., embedded numerals or Latin-script citations) require specific handling
    in any NLP pipeline.
  nlp_tooling_status: 'Best-practice Arabic NLP tools for student-register MSA writing
    (as of 2024–2025): (1) CAMeL Tools (open-source Python toolkit, MIT license) —
    provides morphological analysis, disambiguation, POS tagging, dialect identification,
    and diacritization for MSA and dialects; (2) Camel Morph MSA (LREC-COLING 2024)
    — the largest open-source MSA morphological analyzer with 100K+ lemmas, integrates
    with CAMeL Tools; (3) CAMeLBERT-MSA — BERT model pre-trained on MSA, used in state-of-the-art
    Arabic AES systems (ZAEBUC, LAILA, TAQEEM). All these tools are primarily validated
    on news-domain or social-media MSA and may not transfer perfectly to student writing
    register; no published evaluation specifically on Arabic high school student writing
    exists as of 2025. Source: CAMeL Tools ACL 2020 — [WEB-7];
    Camel Morph MSA LREC-COLING 2024 — [WEB-8];
    NYU Abu Dhabi CAMeL Lab resources — [WEB-9]'
curriculum_and_genre_context:
  primary_curriculum_authority: Qatar Ministry of Education and Higher Education (MOE
    Qatar / MOEHE)
  applicable_curriculum_framework: 'The Qatar national Arabic-language curriculum
    framework is administered by MOEHE and applies to all government (SEC) schools
    from Grades 1–12. The SEC/MOEHE curriculum standards portal (sec.gov.qa) states
    that Arabic standards aim to enable students to use Arabic effectively in communication,
    critical thinking, engagement with literary texts, and creative writing. Qatari
    national curriculum textbooks for 2025–2026 cover Arabic Language and Arabic Literature
    as separate subjects. A published rubric document specific to Grades 10–12 Arabic
    writing assessment was not found in open-access sources; detailed rubric documentation
    likely requires direct request to MOEHE. Source: Qatar MOE curriculum standards
    portal — [WEB-10]; IMPACT-se
    Qatar curriculum review 2025–2026 — [WEB-11]'
  essay_genres_in_scope:
  - genre: Persuasive / argumentative essay (مقالة إقناعية / حجاجية)
    notes: Standard genre across Arab high school curricula; broadly analogous to
      benchmark essay type but anchored to Arabic rhetorical conventions (e.g., classical
      Arabic argumentation structures). The QAES dataset (Bashendy et al. 2024), built
      from the Qatari Corpus of Argumentative Writing (QCAW), provides 195 argumentative
      essays in Arabic with trait-specific annotations — the most directly relevant
      validated resource for this genre.
  - genre: Explanatory / expository essay (مقالة تفسيرية / إيضاحية)
    notes: Present in benchmark in limited form; deployment requires coverage calibrated
      to Arab curricular norms.
  - genre: Literary analysis essay (مقالة تحليل أدبي)
    notes: 'ABSENT from benchmark. The MOEHE curriculum for secondary school includes
      Arabic Literature as a distinct subject alongside Arabic Language, with textbooks
      covering both classical and modern Arabic literary texts. Rubric criteria specific
      to literary analysis essays in Qatar Grades 10–12 were not located in open-access
      sources and require expert elicitation. No AES benchmark covers this genre in
      Arabic. Source: IMPACT-se Qatar 2025–2026 — [WEB-11]'
  - genre: Religious text commentary / Quranic text engagement (تفسير / تأمل نص ديني)
    notes: 'ABSENT from benchmark. Islamic Education is a compulsory subject in Qatar
      national curriculum schools for all Qatari pupils and Arab passport holders.
      Whether graded Quranic commentary essay tasks appear specifically in the Arabic
      Language (vs. Islamic Education) curriculum for Grades 10–12 requires expert
      elicitation — this is not resolvable from open-access documentation. No AES
      benchmark or Arabic NLP dataset covers this genre. Source: Qatar International
      School Arabic/Islamic studies — [WEB-5]'
  - genre: Cultural commentary essay (مقالة ثقافية / اجتماعية)
    notes: 'ABSENT from benchmark. Confirmed present in Qatari curriculum through
      the Qatar History and Citizenship subject (which was substantially reformed
      post-2017 toward civic themes). No separate AES benchmark covers this genre.
      Rubric criteria for cultural commentary essays require expert elicitation. [NEEDS
      VERIFICATION — deferred: likely unsearchable (curriculum-internal rubric details)]'
  genre_coverage_gap_summary: The benchmark (ASAP++) covers only argumentative/persuasive,
    source-dependent, and narrative/descriptive genres in English. At minimum two
    of the five genres listed above (literary analysis and religious text commentary)
    are entirely unrepresented in the benchmark and require separate validation resources.
    A partial Arabic AES resource for argumentative essays in a Qatari context now
    exists (QAES/QCAW, 195 essays), but it does not cover the other genres.
  scoring_rubric_notes:
    qatar_rubric_status: 'The Qatar MOE Arabic Language curriculum standards portal
      confirms that writing is a core assessment strand, but a published, granular
      writing rubric for Grades 10–12 was not located in open-access sources. The
      LAILA dataset (Bashendy et al. 2026, funded by Qatar''s QRDI Council) uses a
      seven-trait rubric (relevance, organization, vocabulary, style, development,
      mechanics, grammar) applied to 7,859 high school essays — this represents the
      closest available validated rubric proxy anchored to Arab high school writing
      norms, though it is not an official MOEHE rubric. Source: LAILA — [WEB-12];
      Qatar MOE standards — [WEB-10]'
    cross_country_divergence: '[NEEDS VERIFICATION — deferred: below search budget;
      comparative Arab curriculum rubric studies were not surfaced by high-priority
      searches; would require expert elicitation or access to national exam board
      documents for Tawjihi, Thanaweya Amma, Lebanese baccalaureate]'
    pan_arab_shared_norms: MSA grammatical correctness and adherence to classical
      Arabic rhetorical norms (فصاحة, بلاغة) are broadly shared across Arab curricula,
      but practical rubric weighting differs. This shared layer provides a partial
      anchor for cross-country generalization.
cultural_norms_notes: '- Islamic values are deeply embedded in Qatari educational
  content and essay prompts; Quranic citations, hadith references, and Islamic ethical
  framing are culturally normative in student writing and should not be flagged as
  off-topic.

  - Arabic rhetorical and literary tradition (بلاغة / فصاحة): classical Arabic eloquence
  norms — including rhythm, lexical richness, and structural parallelism — are aesthetic
  values in Arabic writing that differ from English clarity/concision ideals.

  - High regard for classical Arabic literature and the Quran as linguistic models;
  student essays may draw on these sources as authorities.

  - Honor, family, and community as recurring thematic anchors in cultural commentary
  essays.

  - Gender-appropriate content expectations may vary by school type (public/private,
  single-sex/mixed) within Qatar and across Arab countries.

  - Sensitivity to political topics varies by country (Qatari, Saudi, Egyptian, Jordanian
  national narratives differ); the feedback system should avoid generating commentary
  that implicates politically sensitive content.

  - Ramadan and the Islamic calendar affect academic scheduling and student availability;
  this may be relevant for deployment timing considerations.

  - Note: Qatar national curriculum textbooks for 2025–2026 have been documented by
  external reviewers as containing content that may be politically or religiously
  sensitive (Arab nationalist narratives, materials related to the Israeli–Palestinian
  conflict). The feedback system should be designed to avoid taking positions on politically
  charged essay content. Source: IMPACT-se Qatar curriculum review — [WEB-11]

  '
infrastructure_and_access_notes:
  qatar_digital_infrastructure: 'Qatar has near-universal internet penetration: 99.0–100%
    as of 2025, placing it among the top four globally connected countries (alongside
    Saudi Arabia, UAE, and Bahrain). There were approximately 3.10 million internet
    users in Qatar at end-2025. Mobile broadband quality is extremely high: median
    mobile download speed of ~511 Mbps (second globally after UAE). This means internet
    connectivity is not a barrier to AI tool access for Qatari students. Source: DataReportal
    Digital 2026 Qatar — [WEB-13];
    The Peninsula Qatar Feb 2025 — [WEB-14]'
  school_technology_context: 'Qatar MOE (MOEHE) operates an official LMS: the ''Qeducation''
    platform (powered by CYPHER LMS), launched 2022, covering Grades 3–12 in government
    schools. Adoption in the first month reached 99% for teachers and 91% for students
    (Grades 3–12). The platform replaced an older Qatar Education System (QES) LMS.
    An official mobile app (''Qatar Education'' / قطر للتعليم) is available on Google
    Play as the official LMS mobile interface for public schools. The Qeducation initiative
    supports assignment submission, assessment delivery, and student progress tracking
    — providing a plausible integration pathway for an AI essay feedback tool. As
    of 2022–23, approximately 210,000 user accounts were synced to the system. Source:
    CYPHER Learning Qatar workshop recap — [WEB-15];
    Springer chapter on Qatar digital learning — [WEB-16];
    Google Play Qatar Education app — [WEB-17]'
  device_profile: 'Mobile-device access is extremely high in Qatar: 99.2% of mobile
    connections are broadband-capable (3G/4G/5G). Essay writing and feedback review
    likely occur on desktop/laptop in school labs or home contexts, but the official
    LMS has a dedicated mobile app, suggesting mobile access is a realistic use scenario.
    No specific device-type breakdown for Grades 10–12 student homework contexts was
    found.'
  arabic_interface_requirements: The system interface must support RTL text input
    and display. Keyboard layout (Arabic keyboard vs. transliteration input) affects
    user experience. Any feedback text output must be rendered in Arabic script with
    proper diacritics where pedagogically relevant. The official Qatar Education LMS
    app and CYPHER platform support Arabic-language interface.
  secondary_country_infrastructure_variation: '[NEEDS VERIFICATION — deferred: below
    search budget; infrastructure access for Egypt, Jordan, Lebanon, Saudi Arabia
    varies substantially; World Bank and ITU data for secondary countries available
    but not retrieved within this session. Known qualitatively: Egypt and Jordan have
    substantially lower internet penetration and device access than Qatar; Lebanon
    faces infrastructure crisis. Saudi Arabia has high penetration comparable to Qatar.]'
domain_specific_notes:
  automated_arabic_essay_scoring_landscape: 'Several Arabic AES datasets and systems
    now exist, representing a rapidly developing but still resource-scarce field:


    1. **LAILA** (Bashendy et al. 2026, funded by Qatar''s QRDI Council) — the largest
    publicly available Arabic AES dataset: 7,859 essays by 4,372 high school students,
    annotated with holistic and seven-trait scores (relevance, organization, vocabulary,
    style, development, mechanics, grammar) across 8 prompts. This is the most directly
    relevant proxy dataset for this deployment. Source: [WEB-12]


    2. **QAES / Qatari Corpus of Argumentative Writing (QCAW)** (Bashendy et al. 2024
    / Ahmed et al. 2024) — 195 argumentative Arabic essays with multi-trait annotations;
    limited to two prompts. Specifically sourced from a Qatari context, making it
    a high-validity but very small reference. Source (QAES via ZaQQ paper): [WEB-3]


    3. **ZAEBUC** (Habash & Palfreyman 2022) — 214 Arabic essays from Gulf university
    students (Zayed University, UAE) with CEFR grades and morphological annotations;
    limited to 3 topics. Useful for Gulf-Arabic writer profiles but university-level,
    not high school. Source: [WEB-18]; NYU Scholars
    — [WEB-19]


    4. **AR-AES** (Ghazawi & Simpson 2024) — 2,046 undergraduate Arabic essays from
    Al-Qura University (Saudi Arabia) with rubric-based scoring; covers argumentative,
    descriptive, and source-based types. Source: [WEB-20]


    5. **TAQEEM 2025 shared task** — Cross-prompt Arabic AES shared task using LAILA-derived
    data; top systems used GPT-4o/GPT-4.1 few-shot prompting. Source: [WEB-21]


    **Key limitation:** Combined total of all public Arabic essay datasets is approximately
    4,500 essays before LAILA; even with LAILA the corpus is ~12,000 essays across
    diverse contexts — compared to 130,000+ for English. None of the existing datasets
    specifically covers literary analysis, religious text commentary, or cultural
    commentary genres. Existing datasets are annotated for holistic quality or CEFR
    proficiency, not for the natural-language formative feedback output required by
    this deployment. Source on overall scarcity: ZaQQ/MDPI — [WEB-3]'
  feedback_generation_validation:
    requirement: The deployment output is actionable natural-language revision suggestions
      with explanatory rationale, not numeric scores. No validated Arabic feedback
      generation framework is known to exist for this population.
    gap_status: '**Arwi** (2025, arXiv:2504.11814) is the only identified Arabic writing
      assistant system that generates feedback rather than scores: it provides grammar/vocabulary
      assessment and CEFR-level tracking for MSA writers, using CAMeLBERT-MSA fine-tuned
      on ZAEBUC. However, Arwi targets general MSA learners, not specifically high
      school students under Arab national curricula, and does not generate trait-specific
      natural-language revision rationale. The authors note that existing Arabic writing
      assistant tools (e.g., Sahehly) focus narrowly on grammar correction, not holistic
      essay feedback. No human-in-the-loop evaluation study with Arab high school
      students and teachers was found. Source: Arwi — [WEB-22]'
  arabic_nlp_tools_for_student_writing: 'Best available tools as of 2024–2025:

    - **CAMeL Tools** (open-source, MIT): morphological analysis, POS tagging, diacritization,
    dialect identification for MSA and Gulf/Egyptian/Levantine dialects. Validated
    on news-domain MSA and social media; not specifically validated on student writing
    register. Source: [WEB-7]

    - **Camel Morph MSA** (LREC-COLING 2024): largest open-source MSA morphological
    analyzer, 100K+ lemmas, integrates with CAMeL Tools. Source: [WEB-8]

    - **CAMeLBERT-MSA**: BERT model pre-trained on MSA; used in ZAEBUC, LAILA, TAQEEM
    AES systems. Source: [WEB-9]

    - **QALB corpus** (Mohit et al. 2014/2015): ~1.2M words from Al Jazeera comments
    and native/non-native essays with grammatical error corrections; useful for error
    detection training but not holistic essay scoring. Source: referenced in Arwi
    paper — [WEB-22]

    - **No grammar checker specifically validated on Arabic high school student writing**
    was found; all existing tools target news MSA, social media, or adult language
    learners.'
  msa_dialect_codemixing_tools: 'CAMeL Tools includes a dialect identification system
    classifying text into 25 Arabic city dialects and MSA (based on Salameh, Bouamor
    & Habash 2018). The ZAEBUC-Spoken corpus documents MSA/Gulf Arabic/English code-switching
    in Emirati university students, confirming the phenomenon is real and linguistically
    complex. However, no tool or dataset specifically handles MSA/Gulf-Arabic code-mixing
    detection in formal Arabic student essay writing (as opposed to spoken or social-media
    code-switching). This remains a validation gap. Source: CAMeL Tools dialect ID
    — [WEB-23];
    ZAEBUC-Spoken — [WEB-4]'
  religious_text_genre_resources: 'No AES benchmark or Arabic NLP dataset specifically
    covering Quranic or religious-text commentary essays for high school assessment
    was found. The BAREC readability corpus (2025) includes a Religion and Philosophy
    subdomain (Quran, Hadith) but is a readability assessment corpus, not an essay-scoring
    dataset. The Arwi paper references a Hadith parallel corpus but this is for translation,
    not essay assessment. This genre remains entirely unresourced for AES purposes.
    Source: BAREC corpus — [WEB-24]'
  comparative_arab_curriculum_studies: '[NOT FOUND — searched for comparative Arabic
    writing rubrics across Arab countries and pan-Arab exam writing components (Tawjihi,
    Thanaweya Amma); no open-access comparative study specifically addressing writing
    assessment rubric divergence across Qatar, Saudi Arabia, Egypt, Jordan, and Lebanon
    was surfaced. This gap requires expert elicitation from curriculum specialists
    in each country.]'
benchmark_alignment_summary:
  benchmark: asap_plus_plus
  overall_alignment: Severely misaligned across all six validity dimensions. The benchmark
    provides no Arabic-language data, no Qatari or Arab student writing, no genre
    coverage for literary analysis or religious text commentary, no natural-language
    feedback output schema, and no annotation grounded in Arab curriculum norms. The
    benchmark may serve as a methodological reference (e.g., for QWK-based inter-rater
    agreement design) but cannot function as a validity anchor for this deployment.
  primary_validity_gaps:
  - All benchmark data is English-only; deployment is Arabic-only (MSA)
  - Benchmark essay genres (argumentative, source-dependent, narrative) do not include
    literary analysis, religious text commentary, or cultural commentary
  - Benchmark output is ordinal numeric scores; deployment requires natural-language
    revision suggestions
  - Benchmark ground truth is anchored to US curriculum raters; deployment requires
    Qatar/Arab curriculum norms
  - No Gulf Arabic, Qatari student, or Arab student writing appears anywhere in the
    benchmark
  partial_methodological_relevance:
  - Multi-trait attribute scoring structure (content, organization, vocabulary, etc.)
    is conceptually analogous to what a formative feedback system would target
  - QWK-based inter-rater reliability methodology is a valid template for any future
    Arabic annotation effort
  - Genre-specific scoring logic (different attributes weighted differently per genre)
    is a methodological precedent relevant to a multi-genre Arabic deployment
net_new_fields:
  arabic_aes_landscape_summary_2025:
    description: The Arabic AES field has accelerated significantly in 2024–2026 with
      several new public datasets. LAILA (arXiv 2512.24235, Dec 2025, QRDI-funded)
      is now the largest public Arabic AES dataset at 7,859 high school essays with
      seven-trait annotations — directly relevant to this deployment. The TAQEEM 2025
      shared task demonstrated that GPT-4o/GPT-4.1 few-shot prompting is competitive
      for Arabic trait scoring. However, even with these advances, total Arabic AES
      data (~12,000 essays) remains far below English (~130,000+), and no dataset
      covers literary analysis, religious text commentary, or cultural commentary
      genres.
    relevance: LAILA provides the most valid available proxy for evaluating scoring
      rubric design and trait alignment for this deployment; it should be referenced
      as the primary Arabic AES comparator rather than ASAP++.
    sources: LAILA — [WEB-12]; MAPLE meta-learning paper
      referencing TAQEEM — [WEB-21]; ZaQQ data scarcity
      figures — [WEB-3]
  qaes_qcaw_qatari_corpus:
    description: The Qatari Corpus of Argumentative Writing (QCAW, Ahmed et al. 2024)
      and its trait-annotated extension QAES (Bashendy et al. 2024) provide 195 Arabic
      argumentative essays specifically sourced from a Qatari context, with annotations
      for coherence, organization, grammar, and other traits. This is the only known
      Qatari-origin Arabic AES resource.
    relevance: Highest cultural validity for the argumentative essay genre in Qatar;
      too small (2 prompts, 195 essays) to be a primary validity anchor but should
      be cited as the Qatari-origin reference.
    sources: Referenced in Arwi paper — [WEB-22]; ZaQQ
      survey — [WEB-3]
  arwi_arabic_writing_assistant:
    description: Arwi (arXiv 2504.11814, April 2025) is an MSA writing assistant providing
      CEFR-level AES and grammar/vocabulary feedback for Arabic essays. It uses CAMeLBERT-MSA
      fine-tuned on ZAEBUC and a growing auto-annotated corpus. It is the closest
      existing system to the deployment's formative feedback requirement, though it
      targets general MSA learners and provides CEFR scores rather than rubric-trait
      natural-language rationale.
    relevance: Directly relevant as a methodological reference for Arabic feedback
      generation; its limitations (CEFR vs. curriculum rubric; no trait-level rationale;
      adult learner focus) demarcate the remaining development gap for this deployment.
    sources: Arwi — [WEB-22]
  qatar_lms_qeducation:
    description: Qatar MOEHE operates the Qeducation LMS (CYPHER platform) for all
      government schools Grades 3–12, with an official mobile app ('Qatar Education').
      First-month adoption reached 99% teachers / 91% students. This provides a concrete
      integration pathway for an AI essay feedback tool within existing Qatari school
      infrastructure.
    relevance: Deployment integration planning should target the Qeducation platform;
      RTL Arabic interface and essay-submission workflows should be validated against
      the platform's current capabilities.
    sources: CYPHER Learning Qatar recap — [WEB-15];
      Google Play app — [WEB-17]
  arabic_data_scarcity_calibration_note: 'As of 2025, the combined total of all public
    Arabic AES essay datasets (pre-LAILA) was approximately 4,500 essays across all
    contexts, compared to 130,000+ for English. Even including LAILA''s 7,859 essays,
    the Arabic AES resource base is roughly 10× smaller than English. None of the
    existing datasets covers literary analysis, religious text commentary, or cultural
    commentary genres. This scarcity is structural (morphological complexity, diglossia,
    cost of expert annotation) and is not resolvable by web search — it reflects a
    genuine documentation and resourcing gap that will constrain any benchmarking
    effort for this deployment. Source: ZaQQ/MDPI 2025 — [WEB-3]'
```

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

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: Does your deployment target students across multiple Arab countries or is it focused on Qatar, and do essay prompts, curricula, and writing conventions differ meaningfully across those countries?
A1: The system can support students in other Arab countries but is most reliable for Qatar, since essay prompts and curricula differ across countries. Sub-national and cross-country curricular variation exists and limits generalizability beyond Qatar.

Q2 [OC]: Whose standards should define quality on traits like style, vocabulary, and development — are local curriculum bodies' scoring conventions in different Arab countries meaningfully different from Qatar's?
A2: Local curriculum bodies and teacher communities exist in each country, but how much their scoring conventions diverge from Qatar's is uncertain and would need further research. In principle, MSA norms are shared across the Arab world, but practical rubric differences may exist.

Q3 [OO]: Does the system need to produce actionable natural-language revision suggestions, or are numeric trait scores sufficient for students?
A3: Actionable revision suggestions with natural-language explanations of why points were lost on each trait are more useful; a scored rubric alone is insufficient for the target student population.

Q4 [IC]: Do student essay prompts resemble those in the benchmark, or do they extend to genres like literary analysis, religious texts, or cultural commentary?
A4: The benchmark covers only 8 explanatory/persuasive prompts, which is too narrow — Qatari and other Arab high school students are also assigned literary analysis, religious-text engagement, and cultural commentary essays that require different evaluative knowledge.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark covers only 2 essay types (explanatory/persuasive) drawn from a US middle-school context; the deployment requires coverage of literary analysis, religious texts, and cultural commentary genres that are absent from the benchmark's category inventory. |
| IC | HIGH | Benchmark essays are English-language US student writing from grades 7–10; the deployment targets Arabic-language Qatari/Arab students writing to culturally embedded prompts, creating strong construct-irrelevant variance in individual datapoints. |
| IF | HIGH | The benchmark is English-only; the deployment operates entirely in Arabic (MSA with potential dialectal influence), a different script, morphological structure, and orthographic system — a fundamental signal-distribution mismatch. |
| OO | HIGH | The benchmark scores with a holistic+attribute rubric designed for English writing; the deployment requires natural-language revision suggestions, not numeric labels, and the scoring taxonomy was not designed for Arabic rhetorical or curricular norms. |
| OC | HIGH | Ground-truth labels were produced by annotators judging English essays by US curriculum standards; Qatar/Arab curriculum teachers may apply different quality standards for MSA conventions, organization, and style, making label transfer highly unreliable. |
| OF | HIGH | The benchmark outputs numeric trait scores and labels; the deployment explicitly requires free-text, actionable revision suggestions with explanatory rationale — a direct mismatch in output form that the benchmark cannot validate. |

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
  "benchmark": "asap_plus_plus",
  "region": "Qatari and Arab High School Arabic Essay Writers (Grades 10–12)",
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
