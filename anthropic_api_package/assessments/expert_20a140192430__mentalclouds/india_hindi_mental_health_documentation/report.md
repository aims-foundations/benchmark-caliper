## Deployment Context

**Use case:** A mental health professional or researcher deploys an LLM to automatically summarize counseling session transcripts. The system processes dialogues between therapists and clients, generating concise session notes that capture key therapeutic exchanges, client concerns, and counselor responses. The benchmark evaluates LLM quality on domain-specific summarization of sensitive mental health conversations.
**Target population:** Mental health professionals, clinical psychologists, and counselors in South Asia (India) and the broader Global South who work in online mental health community (OMHC) settings. Users are typically Hindi-English bilingual or English-speaking practitioners seeking AI-assisted documentation support.

# Validity Analysis: mentalclouds
**Target context:** Global South Mental Health Practitioners — India-Anchored OMHC / Peer-Support Deployment
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content | 3 | Moderate gaps | high |
| Output Form ✓ | 3 | Moderate gaps | high |
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

MentalCLOUDS provides a methodologically thoughtful aspect-based summarization benchmark with a dual quantitative/qualitative evaluation design, English-only text input/output that matches the target deployment modality, and Indian-affiliated expert raters who provide partial alignment with the India-anchored OMHC/peer-support population. However, three HIGH-priority dimensions (Input Ontology, Input Content, Output Ontology) exhibit significant misalignment with the deployment context. The benchmark's three-component taxonomy structurally omits suicide/self-harm risk flagging, family-intervention documentation, and spiritual/religious coping — content categories that elicitation, MHCA 2017 Section 115, and India's National Suicide Prevention Strategy 2022 establish as clinically and legally required. Session content is explicitly American-sourced from YouTube, with no compensating Global South counseling-summarization benchmark to triangulate against. The five expert raters are senior India-based clinicians with no peer-support, younger-cohort, or non-Indian Global South representation. Output form and input form are well-matched at the modality level, though ROUGE F1 underweights safety-critical content. Empirical evidence that LLMs systematically miscalibrate responses to suicidal ideation compounds these structural gaps. The benchmark is informative for evaluating CBT-arc summarization performance but cannot validate deployment-readiness for a system operating under Indian regulatory duty-of-care obligations.

## Practical Guidance

### What This Benchmark Measures

MentalCLOUDS measures LLM ability to produce aspect-based summaries of CBT-aligned counseling sessions across three components — symptom-and-history exploration, patient discovery, and reflective utterances [Q15, Q19] — using both lexical-overlap metrics (ROUGE/BERTScore) and a clinical-acceptability framework with hallucination identification [Q44, Q46]. For the target deployment, it provides a meaningful signal on the CBT-arc summarization core that the primary practitioner cohort cares about (input_form: 4; partial strengths in output_form: 3 and output_content: 3), and acknowledges its own limitations transparently.

### Construct Depth

The construct of 'clinical-quality counseling summarization' is probed only partially. The three-component decomposition captures CBT-aligned reasoning steps, and the dual quantitative-qualitative evaluation [Q5, Q18] adds methodological depth. But the benchmark does not probe risk-flag recall, family-intervention documentation, spiritual/religious coping coverage, therapy-technique identification [Q63], or cross-cultural fidelity — all of which are required for the deployment's regulatory and clinical context. Expert qualitative evaluation is also limited to three models on 39 conversations [Q49, Q55], constraining statistical depth.

### What Else You Need

Supplementation should focus on the three HIGH-priority dimensions: (1) construct a deployment-specific risk-flag recall/precision evaluation set covering suicidal ideation, self-harm, and substance use, anchored to MHCA 2017 Section 115 obligations; (2) build a small India-anchored and broader Global South test corpus capturing family-system framing, spiritual/religious coping, and somatization patterns; (3) recruit a regional annotator pool that includes peer-support/OMHC counselors and non-Indian Global South practitioners to re-annotate a subset of model outputs and test for convergent-validity divergence from senior-clinician ratings; (4) replace or supplement ROUGE F1 with a content-coverage metric weighted toward safety-critical spans.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The benchmark's three-component taxonomy (symptom and history exploration, patient discovery, reflective utterances) [Q15] is structurally constrained relative to the clinical documentation needs of the target deployment. The authors themselves acknowledge that 'only three aspects (counseling component) of the conversation' were explored [Q69], that models cannot identify psychotherapy types or therapy techniques [Q63], and that 'important negative histories... such as the history of suicide risk or substance use were also not recorded' [Q64]. For the India-anchored deployment, MHCA 2017 Section 115 establishes a duty-of-care around suicide risk [WEB-10, WEB-11], and India's National Suicide Prevention Strategy 2022 [WEB-30] makes suicide-risk capture a national policy priority — yet the benchmark ontology has no category for it. The elicitation explicitly identifies risk flags, family-related suggestions, and spiritual/religious coping as required content (A2), all of which fall outside the three-component frame. The authors also flag that the three components 'frequently overlap, posing clinical and legal problems' [Q62], indicating internal incoherence of the taxonomy itself. Given IO is HIGH priority and multiple critical regional categories are absent, the dimension is significantly misaligned.

**Strengths:**
- Aspect-based decomposition into distinct counseling components is a meaningful conceptual advance over generic dialogue summarization [Q1, Q19, Q71], and the three components captured do reflect core CBT-aligned clinical reasoning steps that the primary CBT-trained practitioner cohort (A3) would recognize.
- Symptom-and-history and reflective utterances align reasonably with the CBT-anchored structure of the primary practitioner cohort's documentation needs [Q15, A3].

**Checklist:**

- **IO-1**: Required categories for the deployment include the three benchmark components plus risk-and-safety flagging (suicidal ideation, self-harm, substance use), family-directed interventions, spiritual/religious coping, and therapy-technique identification — established by elicitation (A2) and reinforced by Indian regulatory context (MHCA 2017 Section 115 [WEB-10]; National Suicide Prevention Strategy [WEB-30]). — _Sources: WEB-10, WEB-30_
- **IO-2**: Yes — the taxonomy omits suicide/self-harm risk and substance-use history [Q64], psychotherapy-type and therapy-technique identification [Q63], family-directed interventions (no quote; structural absence confirmed; MHCA 2017 itself critiqued for inadequate family-caregiver framing [WEB-9]), and spiritual/religious coping (American-sourced sessions cannot represent Indian faith-healer integration patterns [WEB-15]). — _Sources: Q63, Q64, WEB-9, WEB-15_
- **IO-3**: No clearly irrelevant categories were identified; the three components are clinically meaningful, though their frequent overlap [Q62] introduces construct-irrelevant variance. — _Sources: Q62_
- **IO-4**: Documented gaps that harm content validity: (a) absence of risk-flag category despite legal and policy duty in India; (b) absence of family-intervention category for South Asian relational documentation needs; (c) absence of spiritual-coping category given documented faith-healer integration [WEB-15]; (d) absence of therapy-technique identification [Q63]; (e) overlap between the three existing components [Q62]. — _Sources: Q62, Q63, Q64, WEB-15_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q15] 'Within each conversation, three pivotal counseling components (aspects) emerge – symptom and history exploration, patient discovery, and reflective utterances.' (p.6)
- [Q63] 'The models are also unable to identify psychotherapy types (e.g., cognitive behavior therapy) and therapy techniques, which form an integral part of counseling notes.' (p.15)
- [Q64] 'Important negative histories gathered during the session, such as the history of suicide risk or substance use were also not recorded, and in at least one instance, the presence of suicide risk was not identified.' (p.15)
- [Q62] 'The sections of "symptoms and history", "patient discovery", and "reflection" frequently overlap, posing clinical and legal problems.' (p.15)
- [Q69] 'Finally, this work explored only three aspects (counseling component) of the conversation.' (p.16)

*Web sources:*
- [WEB-10] MHCA 2017 Section 115 establishes duty-of-care around suicide risk
- [WEB-30] India National Suicide Prevention Strategy 2022 targets 10% mortality reduction by 2030
- [WEB-15] Indian patients widely seek faith-healers alongside allopathic care; 32.8% of bipolar patients first approached traditional faith healers
- [WEB-9] MHCA 2017 critiqued for not adequately addressing family caregiver roles

</details>

**Information gaps:**
- Whether reference summaries informally mention risk or family content even though no scoring component captures them — would require dataset-level inspection.

**Requires expert verification:**
- Clinical confirmation from Indian OMHC practitioners that risk, family, and spiritual categories are universally required (vs. context-dependent).

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The benchmark's authors explicitly state that 'the counseling sessions in this work represented a certain demographic region (American) and thus may not apply to therapy counseling for other demographics' [Q70], with sessions sourced from YouTube [Q12, Q60]. The deployment population is mixed — India-anchored with a meaningful share of non-Indian Global South contexts (deployment_context, A1). Although the elicitation notes that CBT protocols 'transfer reasonably' across regions (A1), critical India-specific stressors (caste, dowry, somatization, faith-healer integration [WEB-15]) and Sub-Saharan African conceptualizations (spiritual forces, ancestral relationships [WEB-16]) are structurally absent from American session content. The Lancet Digital Health viewpoint [WEB-29] explicitly identifies cultural and linguistic characteristics of mental-health expression as a key barrier for English-Western-trained LLMs. No compensating Global South counseling-summarization benchmark exists [WEB-27, WEB-28], so transfer cannot be triangulated. The claim of 'heterogeneous demographic spectrum' [Q13] refers to within-American diversity, not cross-cultural diversity. Additionally, the YouTube provenance raises ecological-validity concerns: 'natural conversations are incoherent and grammatically unfluent' [Q61] and likely reflect mock or semi-public exchanges, which may differ from real OMHC clinical transcripts in disclosure depth and risk-content density.

**Strengths:**
- The benchmark authors explicitly disclose the American demographic limitation [Q70], enabling downstream users to make informed decisions about transfer.
- The English-only standard register matches the deployment's stated dataset (A4), so for the subset of Indian deployment data resembling broadly standard English CBT exchanges, content overlap exists [Q12, Q60].
- The dataset embraces some demographic diversity within its source context [Q13], providing within-source variation across mental health concerns and therapists.

**Checklist:**

- **IC-1**: Yes — the deployment requires region-specific knowledge (Indian family-system framing, somatization patterns, caste/dowry-related stressors, faith-healer integration [WEB-15]; Sub-Saharan African spiritual/ancestral conceptualizations [WEB-16]) that are not present in American YouTube-sourced sessions [Q70]. — _Sources: Q70, WEB-15, WEB-16_
- **IC-2**: Partial misalignment: CBT-anchored disclosure overlaps (A1, A3), but India-specific and broader Global South cultural disclosure patterns are structurally absent from American session content [Q70, WEB-29]. — _Sources: Q70, WEB-29_
- **IC-3**: American-specific knowledge in the sessions (e.g., American healthcare-system references, US-specific stressors) may introduce construct-irrelevant variance for Global South practitioners — though specific instances could not be verified without dataset inspection. — _Sources: Q70_
- **IC-4**: INSUFFICIENT DOCUMENTATION — the paper does not document recruitment of regional (Indian or other Global South) annotators to flag culturally sensitive instances at the input-content level; reference annotation creator credentials are also undocumented (annotator_representativeness.reference_annotation_creators flagged as needing verification).
- **IC-5**: Documented harms to content validity: explicit American demographic bias [Q70]; YouTube-sourced sessions characterized as 'incoherent and grammatically unfluent' [Q61], suggesting mock/semi-public rather than naturalistic clinical material; absence of South Asian and broader Global South cultural framings; no compensating Global South benchmark exists for triangulation [WEB-27, WEB-28]. — _Sources: Q70, Q61, WEB-27, WEB-28_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q70] 'Additionally, the counseling sessions in this work represented a certain demographic region (American) and thus may not apply to therapy counseling for other demographics.' (p.16)
- [Q12] 'Comprising 11.5K utterances extracted from 191 counseling sessions involving therapists and patients, this dataset draws from publicly accessible platforms such as YouTube.' (p.6)
- [Q13] 'Embracing a heterogeneous demographic spectrum with distinctive mental health concerns and diverse therapists, the dataset facilitates the formulation of a comprehensive and inclusive approach for researchers.' (p.6)
- [Q60] 'The counseling dataset was curated from multiple multimedia online sources such as youtube transcripts.' (p.15)
- [Q61] 'Hence, most of these natural conversations are incoherent and grammatically unfluent.' (p.15)

*Web sources:*
- [WEB-15] Documented integration of faith-healers alongside psychiatrists in India (32.8% bipolar patients first approached faith healers)
- [WEB-16] Sub-Saharan African mental health frequently attributed to spiritual forces, ancestors, witchcraft
- [WEB-29] Lancet Digital Health 2025: cultural/linguistic characteristics pose major challenges for English/Western-trained LLMs in mental health
- [WEB-27] Africa Health Check covers medical LLM bias but not mental health summarization
- [WEB-28] JMIR systematic review: emerging Global South medical benchmarks (AfriMed-QA, TRINDs) but limited representation

</details>

**Information gaps:**
- Exact proportional split of India vs. other Global South content in deployment data (deferred in regional YAML).
- MEMO dataset annotator credentials and inter-annotator agreement at reference-summary creation stage.

**Requires expert verification:**
- Whether YouTube-sourced sessions are mock/scripted vs. naturalistic — needs direct inspection of dataset samples.
- Whether American YouTube content contains incidental cross-cultural representation that partially mitigates the demographic limitation.

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input form is the lowest-concern dimension. The benchmark uses pre-processed text transcriptions of dyadic patient-therapist dialogue [Q14] in English [Q12, Q60], matching the deployment's text-in/text-out modality and English-only dataset (A4, deployment_context). The grammatical disfluency noted [Q61] is a realistic property of transcribed speech and unlikely to be an external-validity threat at the form level. No audio, image, or multilingual modalities are involved; no script-mismatch concern (Latin alphabet only). The minor caveat is that real-world OMHC transcripts may differ in length, structure, and disfluency profile from YouTube-sourced sessions, but this is a content/ecological concern rather than a form-level signal mismatch. IF was rated LOWER priority in elicitation precisely because the form match is strong.

**Strengths:**
- English-only text input matches the deployment dataset [Q12, A4].
- Dyadic transcript structure [Q14] matches the OMHC counseling-session format.
- No modality, script, or infrastructure mismatches; both benchmark and deployment are text-in/text-out.
- Disfluency in transcripts [Q61] is a realistic property that may improve transfer to messy real-world transcripts.

**Checklist:**

- **IF-1**: Signal distributions match: both are English text transcripts of dyadic dialogue [Q12, Q14, A4]. No image-resolution or audio-fidelity concerns apply. — _Sources: Q12, Q14_
- **IF-2**: Yes — text-in/text-out infrastructure is broadly available across India and the wider Global South; internet penetration in India ~65% in 2023 [WEB-7], and credentialed practitioners self-select for digital access. — _Sources: WEB-7_
- **IF-3**: Domain-specific form: dyadic counseling transcripts [Q14] match the deployment's session-summarization use case. Disfluency [Q61] is realistic. No code-switching in the current dataset (A4); future deployment expansion to Hindi-English code-mixed sessions would re-open this dimension. — _Sources: Q14, Q61_
- **IF-4**: No significant form mismatches identified for the current deployment configuration.

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q12] 'Comprising 11.5K utterances extracted from 191 counseling sessions involving therapists and patients, this dataset draws from publicly accessible platforms such as YouTube.' (p.6)
- [Q14] 'Utilizing pre-processed transcriptions derived from counseling videos, the constituent dialogues within the dataset exhibit a dyadic structure, exclusively featuring patients and therapists as interlocutors.' (p.6)
- [Q60] 'The counseling dataset was curated from multiple multimedia online sources such as youtube transcripts.' (p.15)
- [Q61] 'Hence, most of these natural conversations are incoherent and grammatically unfluent.' (p.15)

*Web sources:*
- [WEB-7] India digital mental health market growing rapidly; telehealth surged 45% 2022–2024

</details>

**Information gaps:**
- Distribution of session length and disfluency density between benchmark and deployment transcripts is not directly compared.

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The output ontology mirrors the input ontology (three reference summaries per session aligned to the same three counseling components [Q15, Q16]) and inherits its structural gaps — risk-flag content, family-intervention suggestions, and spiritual/religious coping have no scoring representation. The authors confirm models 'are not suitable for clinical use as they stand now' due to poor scores on overall efficacy and opportunity cost [Q51], and note suicide-risk and substance-use content was not recorded [Q64]. The Sekhon et al. clinical acceptability framework [Q44, Q48] adds general dimensions (affective attitude, burden, ethicality, coherence, opportunity costs, perceived effectiveness) and a hallucination dimension [Q46, Q53], but none of these directly score risk-flag recall, family-intervention completeness, or cultural-content fidelity. The structure-separation problem [Q62] also undermines the scoring schema's coherence. Empirical evidence shows LLMs systematically over-rate appropriateness of responses to suicidal content vs. expert suicidologists [WEB-13], compounding the scoring gap. Given OO is HIGH priority and the gap is structural, the dimension is significantly misaligned.

**Strengths:**
- The dual quantitative-qualitative scoring design [Q5, Q18] is a methodological strength: ROUGE/BERTScore are supplemented by a six-parameter clinical acceptability framework [Q44, Q48] and a hallucination dimension [Q46], providing more multidimensional assessment than typical summarization benchmarks.
- Per-component scoring [Q26, Q31, Q40] enables granular diagnosis of which counseling aspects models handle well, supporting partial fitness diagnosis even with the taxonomy gap.
- Hallucination categorization [Q53, Q54] partially addresses the patient-safety dimension that pure ROUGE would miss.

**Checklist:**

- **OO-1**: The three counseling-component output categories [Q15] are partially regionally relevant (CBT-anchored, recognized by primary cohort per A3) but omit categories that the deployment requires. — _Sources: Q15_
- **OO-2**: Missing categories for regional deployment: risk-flag documentation [Q64], family intervention notes (structural absence), spiritual/religious coping (structural absence given American-sourced inputs [Q70, WEB-15]), therapy-technique identification [Q63]. National policy context (MHCA 2017 Section 115 [WEB-10]; NSPS 2022 [WEB-30]) elevates the severity of the risk-flag omission. — _Sources: Q63, Q64, Q70, WEB-10, WEB-15, WEB-30_
- **OO-3**: The clinical acceptability framework's six parameters [Q48] are general and not obviously encoding non-regional values, but they were not adapted to scoring South Asian family-systems or faith-coping content; the absence of such adaptation implicitly defaults to a Western/individualist clinical framing. — _Sources: Q44, Q48_
- **OO-4**: Stakeholder-driven taxonomy redesign is warranted: the elicitation explicitly identifies risk, family, and spiritual categories as required (A2), and the benchmark's own authors acknowledge the gap [Q64, Q69]. — _Sources: Q64, Q69_
- **OO-5**: Documented harms to structural and content validity: scoring schema provides no signal on safety-critical content [Q64]; structural overlap among the three categories [Q62]; expert-confirmed clinical unfitness 'as they stand now' [Q51]; empirical evidence that LLMs miscalibrate suicidal-content responses [WEB-13]. — _Sources: Q51, Q62, Q64, WEB-13_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q15] 'Within each conversation, three pivotal counseling components (aspects) emerge – symptom and history exploration, patient discovery, and reflective utterances.' (p.6)
- [Q44] 'The evaluation framework encompasses six crucial parameters — affective attitude, burden, ethicality, coherence, opportunity costs, and perceived effectiveness.' (p.12)
- [Q48] 'The clinical acceptability framework [39] involves six parameters – affective attitude, burden, ethicality, coherence, opportunity costs, and perceived effectiveness.' (p.13)
- [Q51] 'As all three models have poor scores on the more sensitive aspects i.e. the overall efficacy and the opportunity cost, this indicates that these models share the same weakness and are not suitable for clinical use as they stand now.' (p.14)
- [Q62] 'The sections of "symptoms and history", "patient discovery", and "reflection" frequently overlap, posing clinical and legal problems.' (p.15)
- [Q64] 'Important negative histories gathered during the session, such as the history of suicide risk or substance use were also not recorded, and in at least one instance, the presence of suicide risk was not identified.' (p.15)
- [Q53] 'Additionally, the evaluation of hallucination identification is divided into three categories: no hallucination observed, hallucination barely observed, and too much hallucinated in a set of 39 conversations.' (p.14)

*Web sources:*
- [WEB-10] MHCA 2017 Section 115 imposes duty-of-care on suicide risk
- [WEB-30] India National Suicide Prevention Strategy 2022
- [WEB-13] LLMs systematically over-rate appropriateness of responses to suicidal ideation vs. expert suicidologists
- [WEB-15] Faith-healer integration documented in Indian mental health practice

</details>

**Information gaps:**
- Whether the Sekhon et al. parameter ratings implicitly captured culturally salient content quality (e.g., did 'perceived effectiveness' downgrade summaries that omitted family/spiritual content?) — not documented.

**Requires expert verification:**
- Indian clinical experts' view on whether the six-parameter framework can be retrofitted with risk/family/spiritual sub-criteria, or whether a redesigned taxonomy is required.

---

### Output Content — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
The benchmark's expert evaluators are five Indian-affiliated healthcare professionals (two clinical psychologists, three psychiatrists/medical practitioners) [Q41, Q42], aged 40–55 with over a decade of experience [Q43], 4:1 male:female. Their institutional affiliations [Q9] (IIT Delhi, IIIT Delhi, AIIMS Rishikesh, AIIMS New Delhi, YourDOST Karnataka) provide partial alignment with the India-anchored deployment population, including one OMHC-affiliated organization (YourDOST). Inter-rater alignment is reported (variance lowest for MentalBART [Q50]; per-rater hallucination frequencies reported [Q52, Q56]; ratings averaged across five experts [Q47]). However, several gaps weaken convergent and external validity: (a) reference-summary creators' credentials and inter-annotator agreement at the data-creation stage are undocumented; (b) the senior-clinician profile (40–55, 10+ years) does not represent peer-support practitioners or younger OMHC counselors who form a meaningful share of the deployment population; (c) no Sub-Saharan African, Southeast Asian, or Latin American clinical practitioners were involved (annotator_representativeness gaps; [WEB-17, WEB-18]); (d) gender imbalance (4:1 male) may introduce blind spots around gendered disclosure patterns; (e) it is undocumented whether evaluators used CBT-specific, family-systems, or culturally adapted rubrics. OC was rated MODERATE, and the partial India alignment with explicit gaps justifies a middle score.

**Strengths:**
- Five expert raters with explicit reporting of per-rater hallucination frequencies [Q52, Q56] and acknowledgment that 'hallucinations are perceived [differently] among different models' [Q57] — supporting convergent-validity diagnostics.
- Indian institutional affiliation [Q9] including an OMHC platform (YourDOST) provides partial alignment with the India-anchored target population.
- Mix of clinical psychologists and psychiatrists [Q42] provides some disciplinary breadth within the senior-clinician profile.

**Checklist:**

- **OC-1**: Partial — ground-truth reference summaries' creators are undocumented (reference_annotation_creators flagged); expert acceptability ratings are by Indian senior clinicians [Q42, Q9] but it is unclear whether their judgments reflect peer-support/OMHC quality criteria or only senior-psychiatric standards. — _Sources: Q9, Q42_
- **OC-2**: Likely disagreement on culturally salient content: Indian-context practitioners may rate summaries lower if family-system or spiritual coping content is omitted (A3); peer-support practitioners may apply different quality criteria than AIIMS-affiliated senior psychiatrists; non-Indian Global South practitioners are entirely unrepresented. — _Sources: Q9, Q42, WEB-17_
- **OC-3**: Annotator demographics partially documented: five experts, 2:3 psychologist:psychiatrist split [Q42], 4:1 male:female, ages 40–55, 10+ years experience [Q43], Indian institutional affiliations [Q9]. No formal Datasheet/Data Statement disclosed in the paper. Reference-summary creator demographics undocumented. — _Sources: Q9, Q42, Q43_
- **OC-4**: Re-annotation by a regional pool that includes peer-support/OMHC counselors and non-Indian Global South practitioners would meaningfully strengthen convergent validity; not done in source benchmark. — _Sources: WEB-17, WEB-18_
- **OC-5**: Aggregation by averaging across five experts [Q47] could erase minority/divergent perspectives; the paper notes inter-rater variance, particularly higher for MentalLlama and Mistral [Q50], and stresses the importance of multiple appraisers [Q57], but does not separately analyze minority dissent. — _Sources: Q47, Q50, Q57_
- **OC-6**: Documented harms: undocumented reference-summary creator credentials (potential convergent-validity gap); senior-clinician profile mismatch with peer-support deployment cohort; absence of non-Indian Global South annotators; potential aggregation-driven minority erasure. — _Sources: Q42, Q43, WEB-17_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q9] 'Department of Electrical Engineering, Indian Institute of Technology Delhi, India; Department of Computer Science & Engineering, Indraprastha Institute of Information Technology Delhi, India; YourDOST, Karnataka, India; Department of Psychiatry, All India Institute of Medical Sciences, Rishikesh, India; Department of Psychiatry, All India Institute of Medical Sciences, New Delhi, India; Yardi School of Artificial Intelligence, Indian Institute of Technology Delhi, India' (p.1)
- [Q41] 'In order to conduct a comprehensive expert assessment, five healthcare professionals were employed to assess the clinical appropriateness of the summaries produced by the LLMs based on the evaluation framework of Sekhon et al. [39].' (p.12)
- [Q42] 'Among them were two clinical psychologists, with the remaining three comprising psychiatrists and medical practitioners.' (p.12)
- [Q43] 'Of the group, four were male, and one was female, with ages ranging from 40 to 55 years and possessing over a decade of therapeutic experience.' (p.12)
- [Q47] 'Table 6 reports the clinical experts' scores averaged over the ratings given by five experts.' (p.13)
- [Q50] 'Overall, all the raters were more aligned in rating the MentalBART model with lesser variance as compared to the other two LLMs for all the metrics.' (p.13)
- [Q57] 'The data shows fluctuations in how hallucinations are perceived among different models and stresses the importance of reviewing evaluations from numerous appraisers for a complete assessment.' (p.14)

*Web sources:*
- [WEB-17] No non-Indian Global South annotator involvement found in published MentalCLOUDS paper
- [WEB-18] No non-Indian Global South annotator involvement found in PMC-archived version

</details>

**Information gaps:**
- Reference-summary creator credentials, cultural backgrounds, and inter-annotator agreement at the data-creation stage.
- Whether evaluators used CBT-specific, family-systems, or culturally adapted rubrics when applying the Sekhon framework.
- Quality-criteria divergence between AIIMS senior clinicians and peer-support OMHC counselors.

**Requires expert verification:**
- Direct comparison of how Indian peer-support counselors vs. senior psychiatrists rate the same model summaries.
- Inclusion of Sub-Saharan African, Southeast Asian, and Latin American clinical raters.

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
The benchmark output form (text-based structured summaries scored via ROUGE-1/2/L and BERTScore F1 [Q20, Q21, Q22, Q24] plus expert-rated clinical-acceptability and hallucination dimensions [Q44, Q46]) matches the deployment's text-summary modality. OF was rated LOWER priority and the modality match is strong. However, the metric form raises validity concerns: ROUGE F1 rewards lexical overlap [Q22, Q23] and is not weighted toward safety-critical content density — suicidal-ideation flags occupying small token spans contribute minimally to aggregate scores, regardless of clinical importance. The qualitative layer partially mitigates this but covers only three models on 39 test conversations [Q49, Q53, Q55], limiting statistical scope. Hallucination rates of 22–25% (i.e., 75–78% no-hallucination [Q55]) at a small evaluation scope represent a meaningful patient-safety signal that the form-level evaluation cannot fully resolve. A 2025 systematic review notes mental health AI benchmarks lack multi-session and safety-consistency evaluation [WEB-26]. The match is good at the modality level but the metric form imperfectly captures deployment-relevant signals.

**Strengths:**
- Output modality (structured text summaries) is well-matched to the deployment's text-out requirement [Q5, Q20].
- Dual quantitative + qualitative evaluation [Q5, Q18] provides complementary signal: lexical overlap plus expert acceptability and hallucination ratings [Q44, Q46].
- Per-component reporting [Q26, Q31, Q40] preserves granularity rather than collapsing to a single aggregate score.

**Checklist:**

- **OF-1**: Yes — output modality (text summaries) matches deployment needs (text-in/text-out per deployment_context); both produce structured clinical summaries. — _Sources: Q5, Q20_
- **OF-2**: Not applicable — no speech-based output is required for the deployment.
- **OF-3**: Practitioner literacy is not a barrier (credentialed mental health professionals); accessibility requirements at the form level are met by text output.
- **OF-4**: Modality match is strong; documented metric-form concern is that ROUGE F1 [Q21] and BERTScore reward lexical overlap rather than clinical-completeness or safety-critical recall — a partial external-validity concern. The qualitative layer is limited to 39 conversations and three models [Q49, Q55]. — _Sources: Q21, Q22, Q49, Q55, WEB-26_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q5] 'The generated summaries are evaluated quantitatively using standard summarization metrics and verified qualitatively by mental health professionals.' (p.1)
- [Q18] 'We undertake a comprehensive evaluation of the generated summaries across various architectures, employing a dual approach of quantitative and qualitative assessments.' (p.9)
- [Q20] 'Given the generative nature of the task, we employ standard summarization evaluation metrics such as Rouge-1 (R-1), Rouge-2 (R-2), Rouge-L (R-L), and BERTScore (BS) along with their corresponding Precision (P), Recall (R) and F1 scores.' (p.9)
- [Q21] 'Since F1 accounts for Precision and Recall, we compare LLM's performance based on F1 unless stated otherwise.' (p.9)
- [Q22] 'ROUGE (Recall-Oriented Understudy for Gisting Evaluation) [58] assesses the overlap of n-grams (sequences of n consecutive words) between the generated summary and reference summaries.' (p.9)
- [Q49] 'We select the three best LLMs (MentalLlama, Mistral and MentalBART) for the expert evaluation based on the automatic result.' (p.13)
- [Q55] 'Out of the 39 test conversations, the majority of cases on average demonstrate no hallucination, with Mistral and MentalBART achieving 75.13% and 76.15% each, while MentalLlama shows a slightly higher value of 77.69%.' (p.14)

*Web sources:*
- [WEB-26] 2025 systematic review: mental health AI benchmarks lack multi-session and safety-consistency evaluation

</details>

**Information gaps:**
- Whether qualitative ratings included any weighting for safety-critical content recall.

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** No taxonomy categories for suicide/self-harm risk, substance use, family-directed interventions, spiritual/religious coping, or therapy-technique identification.

**Recommendation:** Extend the aspect taxonomy with at least three additional components — risk and safety, family/relational interventions, and spiritual/religious coping — and add therapy-technique identification as a sub-task. Tie the risk component explicitly to MHCA 2017 Section 115 documentation obligations.

### Input Content ⚠

**Gap:** Sessions are American-sourced YouTube transcripts; Indian and broader Global South cultural disclosure patterns are structurally absent.

**Recommendation:** Curate a supplementary mixed-cultural session corpus drawn from Indian OMHC partners (under appropriate consent and DPDP Act compliance) and at least one Sub-Saharan African or Southeast Asian counseling source, and treat this as a separate evaluation slice rather than a replacement.

### Input Content ⚠

**Gap:** Ecological-validity concern: YouTube-sourced sessions described as 'incoherent and grammatically unfluent' [Q61] and likely mock/semi-public, possibly differing from naturalistic OMHC sessions.

**Recommendation:** Conduct a side-by-side comparison study on a small sample of real OMHC transcripts (under IRB/consent) vs. benchmark sessions to quantify ecological-validity drift before relying on benchmark scores for deployment decisions.

### Output Ontology ⚠

**Gap:** Scoring frame provides no signal on risk-flag recall, family-intervention completeness, or spiritual-coping coverage; existing components frequently overlap.

**Recommendation:** Add discrete scoring dimensions for safety-critical content recall, family-intervention completeness, and cultural-coping coverage. Define explicit decision rules to disambiguate overlapping categories before re-scoring.

### Output Content

**Gap:** Expert raters are exclusively senior India-based clinicians; peer-support practitioners and non-Indian Global South clinicians are unrepresented; reference-summary creator credentials undocumented.

**Recommendation:** Recruit a mixed annotator pool that adds peer-support/OMHC counselors, younger practitioners, and at least one Sub-Saharan African or Southeast Asian clinical practitioner. Document MEMO/MentalCLOUDS reference-summary creator credentials and inter-annotator agreement, and report minority-rating distributions rather than only averaged scores.

### Output Form

**Gap:** ROUGE F1 underweights safety-critical content; qualitative layer covers only three models on 39 conversations.

**Recommendation:** Introduce a content-coverage recall metric weighted by clinical importance (e.g., span-level risk-flag recall) and expand qualitative evaluation to a larger subset of conversations and models, including specific safety-content rubrics.

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
| Q15 | 6 | output_ontology | "Within each conversation, three pivotal counseling components (aspects) emerge – symptom and history exploration, patient discovery, and reflective utterances." |
| Q16 | 6 | input_ontology | "Our study aims to capture the essence of each aforementioned counseling component, embarking on the creation of three distinct summaries for a single dialogue — each tailored to a specific counseling component." |
| Q17 | 6 | output_content | "Expanding upon the MEMO dataset, we augment it with annotated dialogue summaries corresponding to the three identified" |
| Q18 | 9 | output_form | "We undertake a comprehensive evaluation of the generated summaries across various architectures, employing a dual approach of quantitative and qualitative assessments." |
| Q19 | 9 | input_ontology | "This section reports the aspect-based (psychotherapy element-based) summarization results based on the automatic evaluation scores." |
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
| Q62 | 15 | output_ontology | "However, the models did not do as well with the structure separation of the information. The sections of "symptoms and history", "patient discovery", and "reflection" frequently overlap, posing clinical and legal problems." |
| Q63 | 15 | input_ontology | "The models are also unable to identify psychotherapy types (e.g., cognitive behavior therapy) and therapy techniques, which form an integral part of counseling notes." |
| Q64 | 15 | output_ontology | "Important negative histories gathered during the session, such as the history of suicide risk or substance use were also not recorded, and in at least one instance, the presence of suicide risk was not identified." |
| Q65 | 15 | output_ontology | "In general, the models exhibited stronger performance in handling medical histories and examinations but struggled when faced with more technical and sensitive aspects, such as conversations related to actual therapeutic strategies." |
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
| WEB-1 | https://www.business-standard.com/health/197-million-indians-need-mental-health-support-here-s-what-s-missing-125101000277_1.html |
| WEB-2 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10826870/ |
| WEB-3 | https://www.datamintelligence.com/research-report/india-mental-health-market |
| WEB-4 | https://blog.privatecircle.co/india-fy24-mental-health-therapy-startups/ |
| WEB-5 | https://www.mhfaindia.com/blog/mental-health-programs-india-expanding-support |
| WEB-6 | https://www.vandrevalafoundation.com/free-counseling |
| WEB-7 | https://www.globenewswire.com/news-release/2024/08/21/2933586/0/en/India-Mental-Health-Market-Valuation-to-Reach-USD-62-86-Billion-By-2032-Adults-are-Heavily-Seeking-Mood-Disorder-Treatments-Says-Astute-Analytica.html |
| WEB-8 | https://www.indiacode.nic.in/bitstream/123456789/2249/1/A2017-10.pdf |
| WEB-9 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8277537/ |
| WEB-10 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6482674/ |
| WEB-11 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5914247/ |
| WEB-12 | https://www.livelaw.in/articles/decoding-the-mental-healthcare-act-2017-an-in-depth-analysis-of-indias-mental-health-legislation-233453 |
| WEB-13 | https://www.jmir.org/2025/1/e67891 |
| WEB-14 | https://psychiatryonline.org/doi/10.1176/appi.ps.20250086 |
| WEB-15 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7616029/ |
| WEB-16 | https://cdn.techscience.cn/files/jpa/2025/TSP_JPA-35-1/TSP_JPA_65764/TSP_JPA_65764.pdf |
| WEB-17 | https://mental.jmir.org/2024/1/e57306 |
| WEB-18 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11303879/ |
| WEB-19 | https://arxiv.org/html/2508.08236 |
| WEB-20 | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf |
| WEB-21 | https://www.dlapiperdataprotection.com/?t=law&c=IN |
| WEB-22 | https://cmhlp.org/imho/blog/navigating-data-privacy-in-india-and-its-emerging-intersection-with-mental-health/ |
| WEB-23 | https://journals.sagepub.com/doi/10.1177/02537176251370651 |
| WEB-24 | https://cmhlp.org/blogs/know-your-mental-health-rights-in-india-understanding-the-mental-healthcare-act-2017/ |
| WEB-25 | https://link.springer.com/article/10.1007/s44192-025-00177-7 |
| WEB-26 | https://www.mdpi.com/2079-9292/15/3/524 |
| WEB-27 | https://aclanthology.org/2025.emnlp-main.1639.pdf |
| WEB-28 | https://www.jmir.org/2025/1/e84120/PDF |
| WEB-29 | https://www.thelancet.com/journals/landig/article/PIIS2589-7500(24)00255-3/fulltext |
| WEB-30 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2188003 |

---

