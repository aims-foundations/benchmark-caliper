## Deployment Context

**Use case:** Researchers and developers building or evaluating AI-driven counseling support tools assess the capability of LLMs to produce faithful, coherent, and clinically appropriate summaries from counseling dialogues. The benchmark provides a standardized evaluation framework to compare multiple LLMs across summarization quality metrics relevant to the mental health domain.
**Target population:** NLP researchers and AI practitioners in South Asia and the Middle East and North Africa who are working on applied clinical NLP, digital mental health platforms, and LLM evaluation for low-resource or underrepresented languages and communities.

# Validity Analysis: mentalclouds
**Target context:** South Asia and MENA NLP/AI Practitioner Cohort — MentalCLOUDS Assessment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form ⚠ | 1 | Serious concern | high |
| **Average** | **2.2** | | |

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

MentalCLOUDS provides a structurally coherent English-only, CBT-aligned counseling-summarization benchmark whose authors are explicit about its American demographic origin [Q70] and three-aspect scope [Q69]. For the SA-MENA practitioner cohort, validity is highly use-case-dependent: South Asian academic researchers benchmarking English LLMs in CBT-aligned Indian institutional settings can derive partial signal, but four of five HIGH-priority dimensions (IO, OO, OC, OF) show substantive gaps. The output-form dimension is the most severe — ROUGE and BERTScore against English references provide zero valid signal for Arabic, Hindi, Urdu, Bengali, Farsi, or Dari output [Q22, Q23, WEB-8, WEB-10, WEB-12]. The input ontology and output ontology omit constructs (religious framing, shame/honor-protective omission, family-system dynamics, fatalistic attribution) that are clinically salient across the target region [WEB-4, WEB-5, WEB-6, WEB-7] and have not been NLP-operationalized elsewhere. Output content reflects an exclusively India-affiliated annotator pool with confirmed absence of MENA validation [WEB-13]. The benchmark also exhibits a safety-critical gap on suicide-risk capture [Q64] that compounds with documented regional stigma [WEB-1, WEB-2, WEB-3]. The IF dimension (LOWER priority) is the strongest area of fit.

## Practical Guidance

### What This Benchmark Measures

MentalCLOUDS measures, for English-language LLMs, the ability to produce CBT-aligned aspect-based summaries (Symptom and History, Patient Discovery, Reflecting) of American-sourced counseling dialogues, as judged by ROUGE/BERTScore overlap with India-annotated English references and by an India-based expert panel applying the Sekhon six-parameter clinical-acceptability framework plus a hallucination scale. Its strongest contribution for the SA-MENA cohort is the hallucination evaluation framework and the comparative open-source <7B model leaderboard, both of which transfer across regions as language-agnostic constructs (IF dimension is the strongest area of fit).

### Construct Depth

Construct depth is shallow-to-moderate for the SA-MENA target context. The benchmark probes only three counseling aspects [Q69] and does not surface psychotherapy-type identification [Q63], suicide-risk capture [Q64], religious/family-system content, or non-English language behavior. The IO and OO dimensions miss key region-relevant categories; the OF dimension provides no valid cross-lingual signal; the OC dimension lacks MENA professional validation [WEB-13]. South Asian English-system evaluation is the only sub-population for which the benchmark provides moderately complete construct coverage.

### What Else You Need

For MENA Arabic/Farsi/Dari practitioners (HIGH priority for OF, OO, OC): an entirely separate evaluation infrastructure is needed — multilingual reference summaries, cross-lingual metrics (LaBSE, XLM-R BERTScore, AraBERT-based BERTScore [WEB-8, WEB-9, WEB-11]), and a MENA expert annotator pool with Islamic psychology training [WEB-4, WEB-5, WEB-16]. For South Asian Hindi/Urdu/Bengali system builders (HIGH priority for IO, OO, OF): regionally adapted counseling component taxonomies covering izzat, family dynamics, and stigma-protective omissions, plus Hindi/Urdu reference summaries and MuRIL/IndicBERT-based metrics. For all sub-populations: additional safety-focused evaluation of suicide-risk capture given the documented benchmark failure [Q64] compounded by regional stigma [WEB-1, WEB-2, WEB-3].

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The benchmark's three-component CBT-aligned taxonomy (Symptom and History, Patient Discovery, Reflecting) [Q15, Q26, Q31, Q40] is explicitly limited in scope, with the authors themselves acknowledging that 'this work explored only three aspects (counseling component) of the conversation' [Q69] and that the sessions represent 'a certain demographic region (American)' that 'may not apply to therapy counseling for other demographics' [Q70]. For the HIGH-priority IO dimension in the SA-MENA target context, multiple clinically salient categories are absent: religious framing of distress (sabr, tawakkul, karma, nazar), shame and honor-based help-seeking inhibition (izzat, ird), family-system and intergenerational dynamics, and fatalistic attribution of suffering — all documented in the regional clinical literature [WEB-4, WEB-5, WEB-6, WEB-7]. The benchmark also documents internal taxonomic weaknesses: components 'frequently overlap, posing clinical and legal problems' [Q62], and models could not identify psychotherapy types or therapy techniques [Q63], or capture suicide risk and negative histories [Q64] — a safety-critical gap that compounds with documented stigma barriers in South Asia and MENA [WEB-1, WEB-2, WEB-3]. Established Islamic psychology frameworks such as TIIP (nafs, qalb, aql, ruh) exist in the clinical literature but have not been operationalized into NLP annotation schemas [WEB-4, WEB-5].

**Strengths:**
- The three CBT-aligned components (SH, PD, RT) provide partial baseline validity for South Asian academic researchers working in CBT-trained institutional environments [Q15], particularly given that CBT's directive therapeutic stance is documented as compatible with Arab and South Asian Muslim clinical expectations in some contexts [WEB-7].
- Authors explicitly flag the demographic scope limitation [Q70] and the three-aspect restriction [Q69], enabling downstream users to size the gap rather than discover it silently.

**Checklist:**

- **IO-1**: Required test case categories for SA-MENA deployment include religious/fatalistic distress framing, shame and honor-based disclosure inhibition, family-system and intergenerational conflict, and culturally specific somatic presentations of distress, in addition to the generic CBT components [WEB-4, WEB-5, WEB-6, WEB-7]. — _Sources: WEB-4, WEB-5, WEB-6, WEB-7_
- **IO-2**: Yes — the benchmark taxonomy omits all of the above regionally relevant categories. The taxonomy is restricted to SH, PD, and RT [Q15, Q16] with the authors acknowledging only three aspects were explored [Q69] and sessions represent a specific (American) demographic [Q70]. — _Sources: Q15, Q16, Q69, Q70_
- **IO-3**: No category is wholly irrelevant to the SA-MENA context — generic CBT components transfer partially [WEB-7] — but the absence of religious/family-system components means the included categories consume the entire evaluation surface without leaving room for region-relevant constructs. — _Sources: WEB-7, Q15_
- **IO-4**: Documented gaps: (a) no religious distress framing, (b) no shame/honor disclosure inhibition, (c) no family-system or intergenerational dynamics, (d) no fatalistic attribution, (e) no psychotherapy-type identification [Q63], (f) failure to record suicide risk [Q64] compounded by regional stigma [WEB-1, WEB-2, WEB-3]. These are content-validity-harming omissions for the HIGH-priority IO dimension. — _Sources: Q62, Q63, WEB-1, WEB-2, WEB-3_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q15] 'Within each conversation, three pivotal counseling components (aspects) emerge – symptom and history exploration, patient discovery, and reflective utterances.' (p.6)
- [Q16] 'Our study aims to capture the essence of each aforementioned counseling component, embarking on the creation of three distinct summaries for a single dialogue — each tailored to a specific counseling component.' (p.6)
- [Q62] 'However, the models did not do as well with the structure separation of the information. The sections of "symptoms and history", "patient discovery", and "reflection" frequently overlap, posing clinical and legal problems.' (p.15)
- [Q63] 'The models are also unable to identify psychotherapy types (e.g., cognitive behavior therapy) and therapy techniques, which form an integral part of counseling notes.' (p.15)
- [Q69] 'Finally, this work explored only three aspects (counseling component) of the conversation.' (p.16)
- [Q70] 'Additionally, the counseling sessions in this work represented a certain demographic region (American) and thus may not apply to therapy counseling for other demographics.' (p.16)

*Web sources:*
- [WEB-4] TIIP (Traditional Islamically Integrated Psychotherapy) grounds intervention in four aspects of the Islamic conception of the soul (nafs, qalb, aql, ruh) — a structured Islamic psychology counseling framework relevant to MENA deployment
- [WEB-5] Keshavarzi & Haque outline the four soul aspects as 'level' targets for clinical intervention
- [WEB-6] Cultural/spiritual treatment practices (ruqyah, dhikr, salah) documented as adjuncts in Muslim mental health literature
- [WEB-7] Narrative review notes CBT's directive stance is documented as compatible with Arab and South Asian Muslim clinical expectations in some contexts
- [WEB-1] BMC Psychiatry 2020 systematic review (n=6,767) — stigma toward mental illness in India higher than Western countries
- [WEB-2] Pakistan NPMS 2022 — ~1 in 3 adults meet psychiatric criteria; help-seeking low partly due to stigma
- [WEB-3] Bangladesh 2023 — mental health treatment gap ~94%; stigma a primary structural barrier

</details>

**Information gaps:**
- No NLP-operationalized Islamic psychology taxonomy exists [WEB-4]; the size of the gap between TIIP-style frameworks and MentalCLOUDS components has not been formally measured.
- Sub-national variation in component salience (urban/rural, religious community) within South Asia is not characterized.

**Requires expert verification:**
- MENA clinical psychologists integrating Islamic frameworks should review whether any of the three existing components (SH/PD/RT) require redefinition before being usable in their settings, beyond simple addition of new components.

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The 11.5K-utterance dataset drawn from 191 YouTube counseling sessions [Q12] is described by the authors as 'embracing a heterogeneous demographic spectrum' [Q13] but they explicitly clarify the sessions represent 'a certain demographic region (American)' [Q70]. For the SA-MENA cohort, this creates two overlapping content-validity issues. First, the input language is English only — there is zero Arabic, Hindi, Urdu, Farsi, Bengali, or Dari content [Q14], and no comparable Arabic counseling session summarization benchmark exists [WEB-14, WEB-15]; the closest Arabic resources (MentalQA, AraHealthQA) cover Q&A classification rather than session dialogue summarization [WEB-12, WEB-14]. No Hindi/Urdu, Farsi, or Dari clinical dialogue summarization datasets have been identified. Second, even at the discourse level, American therapeutic communication norms are encoded in the dialogues, while MENA contexts specifically have a diglossic gap (counseling occurs in spoken dialect; clinical notes in MSA) that has no analog in the dataset. Per the elicitation, the mock-dialogue format moderates the cultural communication-norm gap somewhat, making IC a MODERATE rather than HIGH-priority concern, but the linguistic gap remains structural for non-English deployment.

**Strengths:**
- Authors are explicit about the American demographic origin of sessions [Q70], allowing downstream users to scope external-validity claims appropriately.
- Dyadic dialogue structure [Q14] and natural conversational register [Q61] match the basic interactional shape of counseling encounters across regions, which (per A2) softens the cultural communication-norm gap for the standardized mock-dialogue format.

**Checklist:**

- **IC-1**: Yes — for non-English deployment, the input queries require region-specific linguistic knowledge (Arabic morphology and diglossia, Indic scripts, Perso-Arabic scripts) that the English-only inputs do not exercise [Q14]. For English-system deployment within South Asia, the queries also encode US therapeutic communication norms and culturally specific distress metaphors that may not match end-user discourse patterns. — _Sources: Q14, Q70_
- **IC-2**: Partial misalignment. Sessions sourced from US YouTube material [Q12, Q60] reflect American clinical conventions; cultural fit for SA-MENA is limited. The mock/standardized counseling format moderates but does not eliminate the gap. — _Sources: Q12, Q60, Q70_
- **IC-3**: Western-specific knowledge embedded in the inputs includes US help-seeking discourse, individual-centered framing of distress, and absence of religious-framing turns [Q70, WEB-6, WEB-7]. These do not transfer cleanly to Arabic, Urdu, or Farsi clinical NLP deployment. — _Sources: Q70, WEB-6, WEB-7_
- **IC-4**: INSUFFICIENT DOCUMENTATION — the paper does not document whether regional annotators reviewed the input instances for cultural sensitivity. Recommended action: recruit MENA and South Asian clinical psychologists to flag culturally non-transferable instances [WEB-13].
- **IC-5**: Documented content issues: (a) English-only content [Q14], (b) American demographic origin [Q70], (c) YouTube-sourced sessions [Q60] without documentation of session-level cultural representation, (d) no analog for Arabic spoken-dialect/MSA diglossia in the dataset, (e) no comparable Arabic [WEB-14, WEB-15], Hindi/Urdu, or Farsi/Dari clinical dialogue summarization resources exist to supplement. — _Sources: Q14, Q70, WEB-14, WEB-15_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q12] 'Comprising 11.5K utterances extracted from 191 counseling sessions involving therapists and patients, this dataset draws from publicly accessible platforms such as YouTube.' (p.6)
- [Q13] 'Embracing a heterogeneous demographic spectrum with distinctive mental health concerns and diverse therapists, the dataset facilitates the formulation of a comprehensive and inclusive approach for researchers.' (p.6)
- [Q14] 'Utilizing pre-processed transcriptions derived from counseling videos, the constituent dialogues within the dataset exhibit a dyadic structure, exclusively featuring patients and therapists as interlocutors.' (p.6)
- [Q60] 'The counseling dataset was curated from multiple multimedia online sources such as youtube transcripts.' (p.15)
- [Q61] 'Hence, most of these natural conversations are incoherent and grammatically unfluent.' (p.15)
- [Q70] 'Additionally, the counseling sessions in this work represented a certain demographic region (American) and thus may not apply to therapy counseling for other demographics.' (p.16)

*Web sources:*
- [WEB-12] AraHealthQA 2025 — Arabic mental health Q&A shared task using MentalQA (500 QA pairs), three subtasks; not session summarization
- [WEB-14] MentalQA — 500 Arabic mental health Q&A pairs, classification taxonomy; not dialogue summarization
- [WEB-15] MDPI scoping review confirms Arabic mental health NLP dominated by social media detection; limited labeled clinical dialogue data and dialectal variation challenges

</details>

**Information gaps:**
- Specific session-level cultural content (e.g., proportion mentioning religious framings, family conflict, etc.) is not documented in the paper.
- Session topic distribution and demographic breakdown of YouTube source therapists/clients beyond 'American' is not specified.

**Requires expert verification:**
- Regional clinical experts should review a sample of MentalCLOUDS sessions to characterize the magnitude of communication-norm mismatch for South Asian and MENA end users.

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
The benchmark input is text-only transcriptions of counseling video dialogues [Q14], described as 'incoherent and grammatically unfluent' reflecting natural conversational register [Q61]. Per the dimension priority weights, IF is LOWER priority because both benchmark and the core English-system deployment use case are text-only — no modality mismatch exists for English-interface deployment. The infrastructure context confirms the benchmark's open-source <7B-parameter focus [Q67, Q68] is practically applicable across SA-MENA compute environments. The remaining IF concern is script and right-to-left rendering: the benchmark provides no Arabic, Urdu, or Persian-script input form, but this is more accurately a content/language gap (covered in IC) than a signal-encoding mismatch. For the LOWER-priority IF dimension, this score reflects substantive alignment for English-system deployment with minor gaps for multilingual extension.

**Strengths:**
- Text-only modality matches text-only deployment for English-system users; no audio/visual capture infrastructure required [Q14].
- Open-source <7B-parameter model focus [Q67, Q68] aligns with compute constraints in much of the South Asian and MENA research ecosystem.
- Natural conversational register [Q61] matches realistic input distribution for deployed systems.

**Checklist:**

- **IF-1**: For English-system deployment, signal distributions match — text transcriptions in both source and target. For non-English deployment, the benchmark provides no script-specific input form (RTL Arabic, Nastaliq Urdu, Devanagari, Persian script). — _Sources: Q14_
- **IF-2**: Regional infrastructure supports text-based pipelines. Open-source model focus [Q67, Q68] is practically applicable across SA-MENA compute environments. UAE health data localization (Article 13) and Saudi SDAIA constraints affect data movement but not the input-form specification per se. — _Sources: Q67, Q68, WEB-17_
- **IF-3**: Domain-specific form considerations: counseling transcription quality and turn-taking conventions are encoded in English-language conventions; Arabic diglossia (spoken dialect vs. MSA written) has no analog in the benchmark's input form, but this is principally a content/language issue rather than a signal-encoding mismatch. — _Sources: Q14, Q61_
- **IF-4**: No documented form mismatches that would harm external validity for the English-system core use case. For multilingual extension, the absence of script-specific input examples is a gap but is downstream of the language-coverage gap addressed in IC and OF. — _Sources: Q14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q14] 'Utilizing pre-processed transcriptions derived from counseling videos, the constituent dialogues within the dataset exhibit a dyadic structure, exclusively featuring patients and therapists as interlocutors.' (p.6)
- [Q61] 'Hence, most of these natural conversations are incoherent and grammatically unfluent.' (p.15)
- [Q67] 'Second, for faster and easier reproduction, we did not assess models larger than 7 billion parameters; however, such models can be part of future examinations.' (p.16)
- [Q68] 'Third, for the initial study and to promote research in this field, only open-source models were assessed in this work.' (p.16)

*Web sources:*
- [WEB-17] UAE health data localization (Article 13 of UAE Health Data Law) constrains cloud-based clinical NLP data pipelines that route data to non-UAE servers

</details>

**Information gaps:**
- Specific transcription quality metrics (WER, speaker-segmentation accuracy) are not reported.

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The output label space comprises (a) free-text aspect-based summaries against the three counseling components [Q19], (b) the six-parameter Sekhon clinical acceptability framework — affective attitude, burden, ethicality, coherence, opportunity costs, perceived effectiveness [Q44, Q48], and (c) a three-level hallucination scale [Q46, Q53, Q54]. For the HIGH-priority OO dimension, the label categories encode CBT-aligned Indian/US professional consensus about what counts as a clinically appropriate, coherent, or effective summary. Parameters such as 'perceived effectiveness,' 'ethicality,' and 'opportunity costs' are normative judgments that depend on the professional clinical frame applied [Q51]; MENA practitioners integrating Islamic psychology frameworks (TIIP, ruqyah/dhikr/salah adjuncts) [WEB-4, WEB-5, WEB-6] may calibrate these parameters differently. The AraHealthQA 2025 work explicitly noted that surface-level metrics 'failed to fully measure appropriateness or trustworthiness' for Arabic mental health QA [WEB-12], supporting the structural concern that the OO is calibrated to a specific professional frame. The authors themselves acknowledge models score poorly on 'overall efficacy and the opportunity cost' [Q51] and that important negative histories (e.g., suicide risk) are not recorded [Q64] — a safety-critical taxonomic absence. There is no output category for religious framing, family-system salience, shame/honor-protective omissions, or fatalistic attribution.

**Strengths:**
- Explicit hallucination taxonomy [Q46, Q53, Q54] is largely region-neutral and transferable as a safety construct.
- Six-parameter Sekhon framework [Q44, Q48] provides a structural scaffold that, while calibrated to particular professional norms, can be partially repurposed if recalibrated by regional experts.
- Authors acknowledge clinical unsuitability of current outputs [Q51], reducing risk of overclaiming.

**Checklist:**

- **OO-1**: The six clinical-acceptability parameters [Q44] are partially region-relevant but encode CBT-aligned professional norms; their calibration in MENA Islamic-integrated practice may differ [WEB-4, WEB-5, WEB-6]. The free-text summary output [Q19] is region-agnostic at the form level but scored against region-specific reference summaries. — _Sources: Q44, Q19, WEB-4, WEB-5, WEB-6_
- **OO-2**: Missing categories include: religious-framing salience, shame/honor-protective omission detection, family-system content, fatalistic attribution flags, psychotherapy-type identification [Q63], and reliable suicide-risk and negative-history capture [Q64]. All are clinically salient for the SA-MENA target context. — _Sources: Q63, Q64_
- **OO-3**: 'Perceived effectiveness' and 'opportunity costs' [Q44, Q51] encode professional-frame-dependent value judgments that may not align with MENA clinical norms integrating Islamic psychology [WEB-4, WEB-5]. 'Ethicality' likewise depends on the underlying clinical-ethical framework (e.g., Qatar's CILE Islamic bioethics integration [WEB-20]) which differs from the unstated frame in the benchmark. — _Sources: Q44, Q51, WEB-4, WEB-5, WEB-20_
- **OO-4**: Stakeholder-driven taxonomy redesign is warranted given HIGH OO priority: MENA clinical psychologists and Islamic psychology researchers should be involved in extending the parameter set and recalibrating the existing six [WEB-4, WEB-16]. — _Sources: WEB-4, WEB-16_
- **OO-5**: Documented taxonomy issues harming structural and content validity: (a) missing region-relevant categories (religion, family, shame, fatalism), (b) value-laden parameters calibrated to undocumented professional norms, (c) safety-critical gap on suicide-risk capture [Q64] compounded by regional stigma [WEB-1, WEB-2, WEB-3], (d) absence of NLP-operationalized Islamic psychology categories [WEB-4]. — _Sources: Q63, Q64, WEB-1, WEB-2, WEB-3, WEB-4_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q19] 'This section reports the aspect-based (psychotherapy element-based) summarization results based on the automatic evaluation scores.' (p.9)
- [Q44] 'The evaluation framework encompasses six crucial parameters — affective attitude, burden, ethicality, coherence, opportunity costs, and perceived effectiveness.' (p.12)
- [Q46] 'Additionally, we incorporate a new parameter – the extent of hallucination. It is categorical – 0 (too much hallucinated), 1 (hallucination barely observed), and 2 (no hallucination observed).' (p.12)
- [Q48] 'The clinical acceptability framework [39] involves six parameters – affective attitude, burden, ethicality, coherence, opportunity costs, and perceived effectiveness.' (p.13)
- [Q51] 'As all three models have poor scores on the more sensitive aspects i.e. the overall efficacy and the opportunity cost, this indicates that these models share the same weakness and are not suitable for clinical use as they stand now.' (p.14)
- [Q53] 'Additionally, the evaluation of hallucination identification is divided into three categories: no hallucination observed, hallucination barely observed, and too much hallucinated in a set of 39 conversations.' (p.14)
- [Q54] 'These categories essentially determine how well the response is consistent with the context and whether it is also incorrect, nonsensical, or contains global information beyond the scope of the conversation.' (p.14)
- [Q64] 'Important negative histories gathered during the session, such as the history of suicide risk or substance use were also not recorded, and in at least one instance, the presence of suicide risk was not identified.' (p.15)

*Web sources:*
- [WEB-4] TIIP framework grounds intervention in Islamic conception of the soul (nafs, qalb, aql, ruh) — relevant clinical taxonomy not encoded in MentalCLOUDS
- [WEB-5] Keshavarzi & Haque four soul aspects as 'level' targets for Islamic-integrated clinical intervention
- [WEB-6] Ruqyah, dhikr, salah documented as cultural/spiritual treatment adjuncts in Muslim mental health literature
- [WEB-12] AraHealthQA 2025 found BERTScore 'failed to fully measure appropriateness or trustworthiness' for Arabic mental health QA
- [WEB-16] Stanford Muslim Mental Health & Islamic Psychology Lab — institutional locus for Islamic psychology NLP
- [WEB-20] Qatar Ministry of Public Health collaborates with CILE on Islamic bioethics frameworks for healthcare AI

</details>

**Information gaps:**
- The exact operationalization of each Sekhon parameter for the annotation task (rubric examples for 0, 1, 2) is not surfaced in the available quotes; this affects the precision of cross-cultural calibration assessment.

**Requires expert verification:**
- MENA clinical psychologists with Islamic psychology training should review the six Sekhon parameters and propose recalibrations or additions for regional applicability.

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Reference summaries were produced by augmenting MEMO with annotated dialogue summaries [Q17], with limited documentation of the initial labelers. The qualitative-evaluation expert pool is fully India-affiliated: five healthcare professionals (two clinical psychologists, three psychiatrists/medical practitioners) [Q41, Q42], aged 40–55, four male and one female [Q43], from IIT Delhi, AIIMS Rishikesh, and AIIMS New Delhi [Q9]. There is no documented MENA representation, and web searches confirm that 'no MENA-based mental health professional validation of MentalCLOUDS annotations has been conducted or announced' [WEB-13]. For the HIGH-priority OC dimension, this means salience judgments embedded in reference summaries reflect CBT-aligned Indian/US professional consensus and may not correlate with MENA professional judgments — a convergent-validity concern. The paper documents inter-rater variance ('raters were more aligned in rating MentalBART... with lesser variance' [Q50]; 'fluctuations in how hallucinations are perceived among different models' [Q57]) but does not analyze this variance by professional background or regional training. Aggregation by simple averaging across five raters [Q47] further risks erasing minority perspectives, though the small pool limits the severity of that concern. Notably, the affiliated practitioner organization YourDOST [Q9] strengthens India-specific OC validity for South Asian academic users somewhat but does not extend to MENA contexts.

**Strengths:**
- Five expert raters with >10 years therapeutic experience [Q43] provide non-trivial clinical grounding for South Asian academic deployment within Indian institutional clinical environments.
- Inter-rater variance is reported [Q50, Q57], enabling some calibration of label reliability.
- YourDOST industry affiliation [Q9] connects label provenance to active South Asian clinical practice.

**Checklist:**

- **OC-1**: Partially. For South Asian academic researchers in CBT-aligned Indian institutional settings, ground-truth labels likely reflect their stakeholder perspective. For MENA practitioners and South Asian practitioners integrating religious or family-system frameworks, the labels are unlikely to fully reflect their perspectives [WEB-13, WEB-4]. — _Sources: Q41, Q42, Q43, WEB-13, WEB-4_
- **OC-2**: Disagreement risk is high for MENA stakeholders given (a) zero MENA representation in the annotator pool [Q41–Q43, WEB-13], (b) Islamic psychology frameworks not encoded [WEB-4, WEB-5, WEB-6], (c) per A3, annotators 'did not consciously account for regional context.' — _Sources: Q41, Q43, WEB-13, WEB-4, WEB-5, WEB-6_
- **OC-3**: Annotator demographics are partially documented: five experts, two clinical psychologists / three psychiatrists/medical practitioners, ages 40–55, 4M/1F, >10 years experience [Q41, Q42, Q43]. Institutional affiliations (IIT Delhi, AIIMS Rishikesh, AIIMS New Delhi, YourDOST) are documented [Q9]. Initial-labeling annotator demographics for the reference summaries are not specified in the paper [Q17]. — _Sources: Q9, Q17, Q41, Q42, Q43_
- **OC-4**: Re-annotation by a representative regional pool is warranted. No MENA validation exists [WEB-13]; ideally a MENA mental-health-professional cohort (Gulf-region clinical psychologists with Islamic-framework training) and a broader South Asian pool (Pakistan, Bangladesh, Sri Lanka) should re-annotate a sample. — _Sources: WEB-13_
- **OC-5**: Aggregation by simple average across five raters [Q47] risks erasure of minority perspectives, though the small pool limits the practical severity. Inter-rater variance is reported [Q50] but not decomposed by professional background or region. — _Sources: Q47, Q50, Q57_
- **OC-6**: Documented label-content issues: (a) zero MENA representation [WEB-13], (b) all-India institutional affiliation [Q9], (c) gender imbalance (4M/1F) [Q43], (d) reference-summary annotator demographics underdocumented [Q17], (e) no decomposition of inter-rater variance by clinical framework or region [Q50, Q57]. — _Sources: Q9, Q17, Q43, Q50, WEB-13_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q9] 'Department of Electrical Engineering, Indian Institute of Technology Delhi, India; ... All India Institute of Medical Sciences, Rishikesh, India; ... All India Institute of Medical Sciences, New Delhi, India; Yardi School of Artificial Intelligence, Indian Institute of Technology Delhi, India' (p.1)
- [Q17] 'Expanding upon the MEMO dataset, we augment it with annotated dialogue summaries corresponding to the three identified' (p.6)
- [Q41] 'In order to conduct a comprehensive expert assessment, five healthcare professionals were employed to assess the clinical appropriateness of the summaries produced by the LLMs based on the evaluation framework of Sekhon et al.' (p.12)
- [Q42] 'Among them were two clinical psychologists, with the remaining three comprising psychiatrists and medical practitioners.' (p.12)
- [Q43] 'Of the group, four were male, and one was female, with ages ranging from 40 to 55 years and possessing over a decade of therapeutic experience.' (p.12)
- [Q47] 'Table 6 reports the clinical experts' scores averaged over the ratings given by five experts.' (p.13)
- [Q50] 'Overall, all the raters were more aligned in rating the MentalBART model with lesser variance as compared to the other two LLMs for all the metrics.' (p.13)
- [Q57] 'The data shows fluctuations in how hallucinations are perceived among different models and stresses the importance of reviewing evaluations from numerous appraisers for a complete assessment.' (p.14)

*Web sources:*
- [WEB-13] JMIR Mental Health 2024 — confirms no MENA-based mental health professional validation of MentalCLOUDS annotations conducted or announced; expert pool exclusively India-affiliated
- [WEB-4] TIIP framework — Islamic psychology clinical taxonomy not represented in the annotator pool's training
- [WEB-5] Keshavarzi & Haque four soul aspects framework — additional MENA clinical normative reference

</details>

**Information gaps:**
- Initial reference-summary annotator demographics for the MEMO expansion [Q17] are not detailed.
- No analysis of inter-rater variance by professional sub-specialty or training tradition.

**Requires expert verification:**
- MENA and South Asian (non-India) mental health professionals should re-annotate a sample of MentalCLOUDS reference summaries to quantify regional disagreement.

---

### Output Form — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Automatic evaluation uses ROUGE-1, ROUGE-2, ROUGE-L, and BERTScore [Q20, Q21], all computed against English reference summaries via 'overlap of n-grams... between the generated summary and reference summaries' [Q22, Q23] and 'longest co-occurring n-gram' [Q24]. For the HIGH-priority OF dimension, this design provides zero valid evaluation signal for systems generating summaries in Arabic, Hindi, Urdu, Bengali, Farsi, or Dari — covering the majority of MENA-focused practitioners and many South Asian sub-populations. The 2026 multilingual mental health evaluation study confirms that for Arabic, BLEU scores ~0.54 vs LaBSE ~0.78 demonstrate n-gram metrics are 'especially poorly suited for Arabic clinical NLP evaluation' [WEB-8]. The XLingEval benchmark documents statistically significant English-vs-Hindi BERTScore performance gaps confirming validity concerns for non-English clinical NLP [WEB-10]. AraHealthQA 2025 explicitly found BERTScore 'failed to fully measure appropriateness or trustworthiness' for Arabic mental health QA [WEB-12]. Cross-lingual alternatives (LaBSE, XLM-RoBERTa BERTScore, Arabic-specific BERTScore via AraBERT/CAMeLBERT/MARBERT, Hindi/Urdu via MuRIL/IndicBERT) are technically viable [WEB-8, WEB-9, WEB-11] but have not been applied to MentalCLOUDS or to clinical summarization in target languages. The qualitative six-parameter expert evaluation [Q45] is partially region-transferable as scaffolding but inherits the calibration concerns documented in OO. Per A4, the benchmark 'is applicable only to English-language systems; multilingual evaluation requires an entirely separate framework.'

**Strengths:**
- For English-system deployment, ROUGE/BERTScore metrics are standard summarization metrics with established interpretability [Q20, Q21].
- Dual quantitative + qualitative pipeline [Q5, Q18, Q25] reduces over-reliance on surface-overlap metrics for English deployment.
- Hallucination scale [Q46] and per-conversation reporting (39 test conversations) [Q53, Q55] provide a partly language-agnostic safety signal.

**Checklist:**

- **OF-1**: Output modality (free-text summaries) matches deployment for English systems but provides zero valid signal for Arabic, Hindi, Urdu, Bengali, Farsi, or Dari output [Q22, Q23, WEB-8, WEB-10, WEB-12]. — _Sources: Q22, Q23, WEB-8, WEB-10, WEB-12_
- **OF-2**: INSUFFICIENT DOCUMENTATION — text-to-speech is not within the benchmark's scope. Counseling deployment in low-literacy regional sub-populations may require speech output, but the benchmark does not address this.
- **OF-3**: Literacy and accessibility considerations are not addressed in the benchmark documentation. Regional variation in literacy rates and clinical-language register (e.g., Arabic diglossia between dialect and MSA) are not modeled in the output form.
- **OF-4**: Documented form mismatches harming external validity: (a) ROUGE/BERTScore against English-only references provide no valid signal for non-English output [Q22, Q23, WEB-8]; (b) no multilingual reference summaries provided; (c) no cross-lingual metric variants documented; (d) qualitative parameter calibration carries over OO concerns; (e) cross-lingual alternatives (LaBSE, XLM-R BERTScore, AraBERT-based BERTScore) viable but unapplied [WEB-8, WEB-9, WEB-11]. — _Sources: Q22, Q23, Q24, WEB-8, WEB-9, WEB-11_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q5] 'The generated summaries are evaluated quantitatively using standard summarization metrics and verified qualitatively by mental health professionals.' (p.1)
- [Q18] 'We undertake a comprehensive evaluation of the generated summaries across various architectures, employing a dual approach of quantitative and qualitative assessments.' (p.9)
- [Q20] 'Given the generative nature of the task, we employ standard summarization evaluation metrics such as Rouge-1 (R-1), Rouge-2 (R-2), Rouge-L (R-L), and BERTScore (BS) along with their corresponding Precision (P), Recall (R) and F1 scores.' (p.9)
- [Q21] 'Since F1 accounts for Precision and Recall, we compare LLM's performance based on F1 unless stated otherwise.' (p.9)
- [Q22] 'ROUGE (Recall-Oriented Understudy for Gisting Evaluation) [58] assesses the overlap of n-grams (sequences of n consecutive words) between the generated summary and reference summaries.' (p.9)
- [Q23] 'This metric measures the number of overlapping units such as n-gram, word sequences, and word pairs between the generated summary evaluated against the gold summary typically created by humans.' (p.9)
- [Q24] 'ROUGE-L takes into account the longest co-occurring n-gram between the candidate and the reference summaries.' (p.9)
- [Q45] 'Experts evaluate each summary against these acceptability parameters, assigning continuous ratings on a scale from 0 to 2, where a higher rating signifies enhanced acceptability.' (p.12)

*Web sources:*
- [WEB-8] arXiv 2602.02440 — Arabic LLM evaluation: BLEU ~0.54 vs LaBSE ~0.78 confirms n-gram metrics like ROUGE poorly suited for Arabic clinical NLP
- [WEB-9] MDPI Healthcare 2025 — AraBERT, CAMeLBERT, MARBERT applied to Arabic mental health classification; BERTScore for Arabic clinical summarization not yet evaluated
- [WEB-10] ACM Web Conference 2024 (XLingEval) — statistically significant BERTScore gap between English (0.9206) and Hindi for healthcare queries, confirming metric validity concerns for non-English clinical NLP
- [WEB-11] MDPI Applied Sciences 2025 — XLM-RoBERTa BERTScore demonstrated robust for cross-lingual summarization including low-resource languages; not yet applied to clinical mental health summarization
- [WEB-12] AraHealthQA 2025 — BERTScore 'failed to fully measure appropriateness or trustworthiness' for Arabic mental health QA

</details>

**Information gaps:**
- No documented exploration of multilingual BERTScore variants or cross-lingual evaluation pathways within the benchmark itself.
- No reported behavior of the benchmark when evaluating machine-translated outputs.

**Requires expert verification:**
- Cross-lingual NLP evaluators should pilot LaBSE and XLM-R BERTScore on a translated MentalCLOUDS reference subset to characterize the magnitude of cross-lingual signal loss empirically.

---

## Remediation Suggestions

### Output Form ⚠

**Gap:** ROUGE and BERTScore against English-only references [Q22, Q23] provide no valid signal for Arabic, Hindi, Urdu, Bengali, Farsi, or Dari output [WEB-8, WEB-10, WEB-12].

**Recommendation:** Pilot cross-lingual metrics (LaBSE [WEB-8], XLM-R BERTScore [WEB-11], AraBERT/CAMeLBERT/MARBERT-based BERTScore for Arabic [WEB-9], MuRIL/IndicBERT for Hindi/Urdu) on a translated reference subset and validate against expert ratings; do not report ROUGE for non-English output systems.

### Input Ontology ⚠

**Gap:** Three-aspect taxonomy [Q15, Q69] omits region-salient categories (religious framing, shame/honor, family-system dynamics, fatalistic attribution) and fails to identify psychotherapy types [Q63].

**Recommendation:** Extend the taxonomy with region-specific component categories developed in collaboration with MENA Islamic-psychology specialists [WEB-4, WEB-16] and South Asian clinical psychologists; pilot annotation on a sample of regionally sourced sessions before claiming validity for SA-MENA deployment.

### Input Ontology ⚠

**Gap:** Documented benchmark failure to record suicide-risk and negative-history information [Q64] is not represented as a separate evaluation category and is compounded by regional stigma [WEB-1, WEB-2, WEB-3].

**Recommendation:** Add a dedicated safety-critical sub-task to the evaluation pipeline that explicitly tests negative-history and suicide-risk capture, with region-stratified evaluation reflecting SA-MENA stigma context.

### Output Ontology ⚠

**Gap:** Six-parameter Sekhon framework [Q44, Q48] encodes professional-norm-dependent value judgments (perceived effectiveness, ethicality, opportunity costs) calibrated to undocumented Indian/US frames; no categories for religious-framing salience, shame-protective omission, or family-system content; safety-critical suicide-risk capture is absent [Q64].

**Recommendation:** Convene a MENA + South Asian expert panel including TIIP-trained clinicians [WEB-4, WEB-5] and Qatar-CILE-style Islamic bioethics specialists [WEB-20] to recalibrate the six parameters, add region-specific categories, and define a safety-critical suicide-risk-capture sub-rubric.

### Output Content ⚠

**Gap:** Five-rater India-affiliated expert pool [Q9, Q41–Q43] with no MENA representation [WEB-13]; gender imbalance (4M/1F); aggregation by simple averaging [Q47] without decomposition by clinical framework.

**Recommendation:** Recruit a parallel MENA + non-India South Asian (Pakistan, Bangladesh, Sri Lanka) expert pool to re-annotate a sample of MentalCLOUDS reference summaries; report inter-rater variance decomposed by region and clinical framework; preserve minority/regional rating distributions rather than averaging.

### Input Content

**Gap:** Sessions are American-origin English-only [Q14, Q70]; no Arabic, Hindi, Urdu, Bengali, Farsi, or Dari content; no analog for Arabic spoken-dialect/MSA diglossia.

**Recommendation:** Construct a complementary regionally sourced counseling dialogue corpus in target languages, drawing on MENA digital mental health platforms [WEB-21] and South Asian platforms (e.g., YourDOST [Q9]) with appropriate IRB/data-localization protocols [WEB-17, WEB-18]; document session demographics explicitly.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "This study evaluates the effectiveness of state-of-the-art Large Language Models (LLMs) in selectively summarizing various components of therapy sessions through aspect-based summarization, aiming to benchmark their performance." |
| Q2 | 1 | input_content | "We introduce MentalCLOUDS, a counseling-component guided summarization dataset." |
| Q3 | 1 | input_content | "This benchmarking dataset consists of 191 counseling sessions with summaries focused on three distinct counseling components (aka counseling aspects)." |
| Q4 | 1 | input_ontology | "Additionally, we assess the capabilities of 11 state-of-the-art LLMs in addressing the task of component-guided summarization in counseling." |
| Q5 | 1 | output_form | "The generated summaries are evaluated quantitatively using standard summarization metrics and verified qualitatively by mental health professionals." |
| Q6 | 1 | output_form | "Our findings demonstrate the superior performance of task-specific LLMs such as MentalLlama, Mistral, and MentalBART in terms of standard quantitative metrics such as Rouge-1, Rouge-2, Rouge-L, and BERTScore across all aspects of counseling components." |
| Q7 | 1 | output_form | "Further, expert evaluation reveals that Mistral supersedes both" |
| Q8 | 1 | output_content | "Prottay Kumar Adhikary, Aseem Srivastava, Shivani Kumar, Salam Michael Singh, Puneet Manuja, Jini K Gopinath, Vijay Krishnan, Swati Kedia, Koushik Sinha Deb, Tanmoy Chakraborty" |
| Q9 | 1 | output_content | "Department of Electrical Engineering, Indian Institute of Technology Delhi, India; Department of Computer Science & Engineering, Indraprastha Institute of Information Technology Delhi, India; YourDOST, Karnataka, India; Department of Psychiatry, All India Institute of Medical Sciences, Rishikesh, India; Department of Psychiatry, All India Institute of Medical Sciences, New Delhi, India; Yardi School of Artificial Intelligence, Indian Institute of Technology Delhi, India" |
| Q10 | 1 | input_ontology | "However, existing approaches often overlook the nuanced intricacies inherent in counseling interactions." |
| Q11 | 6 | input_content | "To evaluate the performance of diverse summarization systems across various aspects of counseling interactions, we expand upon the MEMO dataset [37]." |
| Q12 | 6 | input_content | "Comprising 11.5K utterances extracted from 191 counseling sessions involving therapists and patients, this dataset draws from publicly accessible platforms such as YouTube." |
| Q13 | 6 | input_content | "Embracing a heterogeneous demographic spectrum with distinctive mental health concerns and diverse therapists, the dataset facilitates the formulation of a comprehensive and inclusive approach for researchers." |
| Q14 | 6 | input_form | "Utilizing pre-processed transcriptions derived from counseling videos, the constituent dialogues within the dataset exhibit a dyadic structure, exclusively featuring patients and therapists as interlocutors." |
| Q15 | 6 | input_ontology | "Within each conversation, three pivotal counseling components (aspects) emerge – symptom and history exploration, patient discovery, and reflective utterances." |
| Q16 | 6 | input_ontology | "Our study aims to capture the essence of each aforementioned counseling component, embarking on the creation of three distinct summaries for a single dialogue — each tailored to a specific counseling component." |
| Q17 | 6 | output_content | "Expanding upon the MEMO dataset, we augment it with annotated dialogue summaries corresponding to the three identified" |
| Q18 | 9 | output_form | "We undertake a comprehensive evaluation of the generated summaries across various architectures, employing a dual approach of quantitative and qualitative assessments." |
| Q19 | 9 | output_ontology | "This section reports the aspect-based (psychotherapy element-based) summarization results based on the automatic evaluation scores." |
| Q20 | 9 | output_form | "Given the generative nature of the task, we employ standard summarization evaluation metrics such as Rouge-1 (R-1), Rouge-2 (R-2), Rouge-L (R-L), and BERTScore (BS) along with their corresponding Precision (P), Recall (R) and F1 scores." |
| Q21 | 9 | output_form | "Since F1 accounts for Precision and Recall, we compare LLM's performance based on F1 unless stated otherwise." |
| Q22 | 9 | output_form | "ROUGE (Recall-Oriented Understudy for Gisting Evaluation) [58] assesses the overlap of n-grams (sequences of n consecutive words) between the generated summary and reference summaries." |
| Q23 | 9 | output_form | "This metric measures the number of overlapping units such as n-gram, word sequences, and word pairs between the generated summary evaluated against the gold summary typically created by humans." |
| Q24 | 9 | output_form | "ROUGE-L takes into account the longest co-occurring n-gram between the candidate and the reference summaries." |
| Q25 | 10 | output_form | "Notably, in the context of counseling summaries, which are inherently tied to a domain-specific conversation, we embark on a meticulous qualitative examination of the generated summaries for individual counseling components." |
| Q26 | 10 | input_ontology | "Table 2 reports the automatic evaluation scores of LLMs on the summarization task for the Symptom and History (SH) psychotherapy element." |
| Q27 | 10 | output_form | "MentalLlama outperforms the other LLMs across all the automatic evaluation metrics." |
| Q28 | 10 | output_form | "For the R-1 metric, it achieves an F1 score of 30.86, followed by MentalBART with an F1 score of 28.00." |
| Q29 | 10 | output_form | "In terms of the R-2 metric, Mistral is comparable with MentalLlama with a difference of mere 0.90 F1 score." |
| Q30 | 10 | output_form | "For R-L, Mistral is preceded by MentalLlama by a difference of 2.93 F1 score." |
| Q31 | 10 | input_ontology | "The experimental results presented in Table 3 focus on the summarization task for the Patient Discovery (PD) psychotherapy element." |
| Q32 | 10 | output_form | "Considering the R-1 metric, MentalLlama demonstrates superior performance compared to other LLMs." |
| Q33 | 10 | output_form | "MentalLlama shows a 30.95 F1 score, followed by MentalBART (29.94 F1 Score)." |
| Q34 | 10 | output_form | "For the R-2 metric, GPT-J outperforms the other models, followed by MentalLlama." |
| Q35 | 10 | output_form | "Additionally, in terms of the R-L metric, the top two highest F1 score models are MentalLlama and Mistral." |
| Q36 | 10 | output_form | "MentalBART supersedes the other models with an F1 score of 88.61 w.r.t BS metric." |
| Q37 | 11 | output_form | "and MentalBART, which were pre-trained on the mental domain data, show consistent superiority." |
| Q38 | 11 | output_form | "Notably, the base Mistral model also performs comparable and sometimes better than the models trained on the mental health domain data." |
| Q39 | 11 | input_ontology | "Table 3. Results obtained on MentalCLOUDS for the summarization task on the Patient Discovery (PD) psychotherapy element." |
| Q40 | 11 | input_ontology | "Table 4. Results obtained on MentalCLOUDS for the summarization task on the Reflecting (RT) psychotherapy element." |
| Q41 | 12 | output_content | "In order to conduct a comprehensive expert assessment, five healthcare professionals were employed to assess the clinical appropriateness of the summaries produced by the LLMs based on the evaluation framework of Sekhon et al. [39]." |
| Q42 | 12 | output_content | "Among them were two clinical psychologists, with the remaining three comprising psychiatrists and medical practitioners." |
| Q43 | 12 | output_content | "Of the group, four were male, and one was female, with ages ranging from 40 to 55 years and possessing over a decade of therapeutic experience." |
| Q44 | 12 | output_ontology | "The evaluation framework encompasses six crucial parameters — affective attitude, burden, ethicality, coherence, opportunity costs, and perceived effectiveness." |
| Q45 | 12 | output_form | "Experts evaluate each summary against these acceptability parameters, assigning continuous ratings on a scale from 0 to 2, where a higher rating signifies enhanced acceptability." |
| Q46 | 12 | output_ontology | "Additionally, we incorporate a new parameter – the extent of hallucination. It is categorical – 0 (too much hallucinated), 1 (hallucination barely observed), and 2 (no hallucination observed)." |
| Q47 | 13 | output_content | "Table 6 reports the clinical experts' scores averaged over the ratings given by five experts." |
| Q48 | 13 | output_ontology | "The clinical acceptability framework [39] involves six parameters – affective attitude, burden, ethicality, coherence, opportunity costs, and perceived effectiveness (c.f. Table 5 for more details)." |
| Q49 | 13 | output_form | "We select the three best LLMs (MentalLlama, Mistral and MentalBART) for the expert evaluation based on the automatic result." |
| Q50 | 13 | output_content | "Overall, all the raters were more aligned in rating the MentalBART model with lesser variance as compared to the other two LLMs for all the metrics." |
| Q51 | 14 | output_ontology | "As all three models have poor scores on the more sensitive aspects i.e. the overall efficacy and the opportunity cost, this indicates that these models share the same weakness and are not suitable for clinical use as they stand now." |
| Q52 | 14 | output_content | "Table 7. Hallucination frequency marked by experts for the top three LLMs. Here the average of hallucination frequencies for each rater are reported." |
| Q53 | 14 | output_ontology | "Additionally, the evaluation of hallucination identification is divided into three categories: no hallucination observed, hallucination barely observed, and too much hallucinated in a set of 39 conversations." |
| Q54 | 14 | output_ontology | "These categories essentially determine how well the response is consistent with the context and whether it is also incorrect, nonsensical, or contains global information beyond the scope of the conversation." |
| Q55 | 14 | output_form | "Out of the 39 test conversations, the majority of cases on average demonstrate no hallucination, with Mistral and MentalBART achieving 75.13% and 76.15% each, while MentalLlama shows a slightly higher value of 77.69%." |
| Q56 | 14 | output_content | "Table 7 presents the total numbers for each model and hallucination category as assessed by five individual raters." |
| Q57 | 14 | output_content | "The data shows fluctuations in how hallucinations are perceived among different models and stresses the importance of reviewing evaluations from numerous appraisers for a complete assessment." |
| Q58 | 15 | input_ontology | "In this work, we assessed the state-of-the-art LLMs on the aspect-based summarization task of mental health therapy conversations." |
| Q59 | 15 | output_form | "Specifically, we benchmarked 11 LLMs for aspect-based summarization and evaluated them using both automatic and human evaluation approaches." |
| Q60 | 15 | input_content | "The counseling dataset was curated from multiple multimedia online sources such as youtube transcripts [37]." |
| Q61 | 15 | input_form | "Hence, most of these natural conversations are incoherent and grammatically unfluent." |
| Q62 | 15 | input_ontology | "However, the models did not do as well with the structure separation of the information. The sections of "symptoms and history", "patient discovery", and "reflection" frequently overlap, posing clinical and legal problems." |
| Q63 | 15 | input_ontology | "The models are also unable to identify psychotherapy types (e.g., cognitive behavior therapy) and therapy techniques, which form an integral part of counseling notes." |
| Q64 | 15 | output_ontology | "Important negative histories gathered during the session, such as the history of suicide risk or substance use were also not recorded, and in at least one instance, the presence of suicide risk was not identified." |
| Q65 | 15 | input_ontology | "In general, the models exhibited stronger performance in handling medical histories and examinations but struggled when faced with more technical and sensitive aspects, such as conversations related to actual therapeutic strategies." |
| Q66 | 16 | input_ontology | "First, this work aims to benchmark the efficacy of only 11 LLMs on the aspect-based summarization task." |
| Q67 | 16 | input_ontology | "Second, for faster and easier reproduction, we did not assess models larger than 7 billion parameters; however, such models can be part of future examinations." |
| Q68 | 16 | input_ontology | "Third, for the initial study and to promote research in this field, only open-source models were assessed in this work." |
| Q69 | 16 | input_ontology | "Finally, this work explored only three aspects (counseling component) of the conversation." |
| Q70 | 16 | input_content | "Additionally, the counseling sessions in this work represented a certain demographic region (American) and thus may not apply to therapy counseling for other demographics." |
| Q71 | 16 | input_ontology | "Our study benchmarked the efficacy and role of large language models towards component-guided counseling summarization tasks." |
| Q72 | 16 | input_content | "In doing so, we introduced a new dataset, MentalCLOUDS, which comprises summaries corresponding to three counseling components." |
| Q73 | 16 | input_content | "The dataset will be available upon request." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://link.springer.com/article/10.1186/s12888-020-02937-x |
| WEB-2 | https://www.medrxiv.org/content/10.1101/2024.07.08.24310056v1.full.pdf |
| WEB-3 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10579681/ |
| WEB-4 | https://www.routledge.com/Applying-Islamic-Principles-to-Clinical-Mental-Health-Care-Introducing-Traditional-Islamically-Integrated-Psychotherapy/Keshavarzi-Khan-Ali-Awaad/p/book/9780367488864 |
| WEB-5 | https://www.tandfonline.com/doi/abs/10.1080/10508619.2012.712000 |
| WEB-6 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8267770/ |
| WEB-7 | https://pmc.ncbi.nlm.nih.gov/articles/PMC9119255/ |
| WEB-8 | https://arxiv.org/html/2602.02440 |
| WEB-9 | https://www.mdpi.com/2227-9032/13/9/985 |
| WEB-10 | https://dl.acm.org/doi/10.1145/3589334.3645643 |
| WEB-11 | https://www.mdpi.com/2076-3417/15/14/7800 |
| WEB-12 | https://arxiv.org/html/2508.20047v2 |
| WEB-13 | https://mental.jmir.org/2024/1/e57306 |
| WEB-14 | https://arxiv.org/abs/2405.12619 |
| WEB-15 | https://www.mdpi.com/2227-9032/13/9/963 |
| WEB-16 | https://med.stanford.edu/mmhip.html |
| WEB-17 | https://www.pwc.com/m1/en/publications/healthcare-data-protection-in-the-uae.html |
| WEB-18 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11250741/ |
| WEB-19 | https://blogs.loc.gov/law/2024/12/falqs-ai-regulations-in-the-gulf-cooperation-council-member-states-part-one/ |
| WEB-20 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12141507/ |
| WEB-21 | https://www.digitalbricks.ai/blog-posts/the-state-of-ai-in-the-middle-east-2025 |

---

