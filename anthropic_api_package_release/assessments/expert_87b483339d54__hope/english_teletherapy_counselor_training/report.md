## Deployment Context

**Use case:** A conversational AI system for mental health counseling classifies dialogue acts in real-time counseling conversations using the HOPE benchmark and any classification model. The system identifies the communicative intent (e.g.,  question, clarification) of each utterance by counselors and clients, and subsequently allows downstream tasks such as session quality assessment, automated counselor feedback, and training support in clinical and teletherapy settings.
**Target population:** Mental health counselors, trainee therapists, and clinical supervisors who conduct or review online counseling sessions in English. This includes practitioners and researchers working with teletherapy platforms and peer support services who need automated tools for counseling quality evaluation and dialogue understanding.

# Validity Analysis: hope
**Target context:** US and South Asian Mental Health Counseling Practitioners (OMHC/Teletherapy)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ⚠ | 2 | Significant gaps | high |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form | 3 | Moderate gaps | medium |
| Output Ontology ✓ | 3 | Moderate gaps | high |
| Output Content | 3 | Moderate gaps | medium |
| Output Form ✓ | 4 | Minor gaps | high |
| **Average** | **2.8** | | |

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

HOPE provides a well-engineered dialogue-act classification benchmark for structured US clinical counseling (CBT, child, family therapy) with a thoughtfully designed 12-label taxonomy [Q17, Q27], substantial inter-annotator agreement [Q49], and rigorous evaluation methodology [Q63, Q87, Q88]. For the in-scope structured clinical therapy portion of the US deployment, the benchmark is reasonably valid. However, the deployment explicitly extends to peer support, crisis intervention, and South Asian English contexts, and HOPE's source data, taxonomy, and annotators are predominantly aligned with US-based clinical therapy [Q98, Q99]. The HIGH-priority IO dimension shows a clear ontological gap: peer support communicative patterns and crisis-specific acts (safety-planning, risk stratification) have no dedicated representation and would default to overloaded categories like ACK or the residual GC catch-all [Q44, Q77]. No drop-in supplementary benchmark exists for crisis dialogue-act classification [WEB-2, WEB-20], and ESConv [WEB-18] / EMH [WEB-19] provide only structurally-different peer-support frameworks. Output form is well aligned (score 4); input form has bounded concerns from live-ASR fidelity (score 3); output ontology shows real boundary ambiguity even within scope (score 3); annotator representation lacks documented South Asian or peer/crisis presence (OC score 3). Input ontology and input content carry the largest validity risks (both score 2).

## Practical Guidance

### What This Benchmark Measures

HOPE measures the ability to assign one of 12 counseling-aligned dialogue-act labels to utterances in dyadic clinical therapy sessions, evaluating conversational-flow classification rather than clinical judgment [Q14, Q102]. For the deployment, this provides reasonable evidence about model performance on US-based structured clinical therapy (CBT/child/family) — particularly for tracking conversational trajectory in supervision and feedback workflows. Output Form (score 4) and Output Ontology design (score 3) are the strongest dimensions for this in-scope use case.

### Construct Depth

The benchmark probes dialogue-act classification with reasonable depth for structured clinical therapy: 12.9K utterances across 212 sessions [Q13], substantial inter-annotator agreement [Q49], multi-tier baseline comparison [Q79, Q80], and per-label diagnostic information [Q76]. However, depth degrades sharply outside this scope: there is no empirical evidence about how labels behave on peer support register, no evaluation on crisis-context utterances, no per-session-type or per-label Kappa breakdown, and no out-of-distribution diagnostic framework. The discarded emotion-annotation pilot [Q126, Q129] indicates the taxonomy intentionally excludes affective dimensions that matter for quality assessment.

### What Else You Need

For peer support deployment: ESConv [WEB-18] and EMH [WEB-19] provide complementary annotation frameworks (support strategies, empathy mechanisms) that should be evaluated alongside HOPE-trained models — neither uses HOPE-compatible labels, so cross-framework validation is required. For crisis intervention deployment: no equivalent benchmark exists [WEB-20], so crisis-specific dialogue-act validation is a net-new task — the 988 Lifeline structured model [WEB-2] should inform a custom label extension. For South Asian deployment: expert elicitation from South Asian clinical psychologists is needed to validate label-boundary behavior under different formality/directiveness norms (gap_id 3, deferred). For real-time teletherapy: empirical comparison of YouTube vs. live-ASR transcripts is needed to quantify input-form drift (gap_id 5, deferred). For supervisory feedback applications: per-label safety-critical performance reporting (especially for IRQ/YNQ behavior on crisis-relevant utterances) should supplement macro-F1.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The HOPE input ontology is explicitly scoped to dyadic, structured clinical counseling sessions (CBT, child, family) [Q22, Q26], with the taxonomy reflecting therapist-driven speaker asymmetry [Q125]. The deployment explicitly extends to peer support and crisis intervention, which involve communicative patterns the taxonomy was not designed to capture. Peer support contexts lack the formal clinical hierarchy embedded in the speaker-initiative/responsive structure, and crisis intervention involves safety-planning, de-escalation, and risk-stratification acts with no dedicated representation — these would default to IRQ, YNQ, or the residual GC catch-all [Q44]. The 988 Lifeline's structured three-phase crisis model (Explore/Clarify/Plan) does not map onto HOPE's flat 12-label taxonomy [WEB-2]. No crisis-specific dialogue-act benchmark exists to fill the gap [WEB-20]. ESConv's 8-strategy framework for peer/social support [WEB-18] is structurally different from HOPE's taxonomy, indicating that the field treats peer support as ontologically distinct. Given peer support and crisis are HIGH-priority deployment contexts, this is a substantial ontological gap. The user's elicitation acknowledges this directly (A1).

**Strengths:**
- Taxonomy is explicitly designed for counseling rather than borrowed from generic dialogue-act schemes, with hierarchical organization (initiative/responsive/general) tailored to therapy [Q27, Q29]
- Speaker-aware modeling (SPARTA) reflects the therapist-patient asymmetry that does hold within structured clinical therapy use cases in scope [Q125]
- The taxonomy is appropriate for the structured-therapy portion of the deployment (CBT/child/family in US contexts), which forms a substantial part of the practitioner workflow

**Checklist:**

- **IO-1**: Required categories include structured clinical therapy acts (covered), peer support acts (mutual disclosure, emotional co-regulation, informal acknowledgment), and crisis-specific acts (safety-planning probes, lethality assessment, de-escalation, risk stratification). The deployment scope explicitly includes all three [elicitation A1]. — _Sources: Q22, Q26_
- **IO-2**: Yes — peer support and crisis-specific dialogue-act categories are absent. HOPE's taxonomy is built for 'patient and therapist' dyads in 'social counselling' [Q7, Q8] and for 'mental-health counseling session' [Q17], with no peer or crisis coverage. The 988 Lifeline's distinct conversational phases [WEB-2] and ESConv's separate strategy taxonomy [WEB-18] confirm that peer/crisis acts require different representational frameworks. — _Sources: Q7, Q17, WEB-2, WEB-18_
- **IO-3**: No clearly irrelevant categories were identified — all 12 labels remain at least nominally applicable to general counseling dialogue. The risk is underrepresentation, not irrelevance.
- **IO-4**: Major content-validity gaps: (a) crisis-specific safety-planning and risk-assessment acts have no dedicated label and would be subsumed into IRQ/YNQ/GC, indistinguishably from routine acts; (b) peer support emotional co-regulation likely collapses into the already-overloaded ACK or residual GC [Q44]; (c) the speaker asymmetry baked into the taxonomy [Q125] does not map onto peer dyads. — _Sources: Q44, Q125, WEB-2, WEB-20_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q22] 'we annotated ∼ 12.9K utterances with 12 dialogue-act labels carefully designed to cater to the requirements of a counseling session' (p.3)
- [Q26] 'The data collection process provides us 12.9K utterances from 212 counseling therapy sessions – all of them are dyadic conversations only' (p.3)
- [Q44] 'Other utterances that do not belong to any of the above labels are tagged as GC, possibly because of the vagueness and the lack of sense in the context of the conversation' (p.4)
- [Q125] 'a majority portion of the counseling conversation is driven by the therapist, thus the speaker-initiative dialogue-acts have higher relevance with the therapist utterances' (p.11)
- [Q7] 'a conversation between a patient and a therapist is considerably implicit' (p.1)

*Web sources:*
- [WEB-2] 988 Lifeline documents a structured three-phase crisis conversation model (Explore/Clarify/Plan) that does not map to HOPE's flat 12-label taxonomy
- [WEB-18] ESConv (ACL 2021) uses an 8-strategy / 3-stage framework for peer/social support — structurally distinct from HOPE
- [WEB-20] Crisis Text Line research uses discourse analysis rather than HOPE-compatible dialogue-act labels; no crisis-specific dialogue-act benchmark identified

</details>

**Information gaps:**
- No empirical validation of how HOPE labels behave on peer support or crisis-register text
- No ontology defined for crisis-specific acts such as safety-planning probes or lethality assessment

**Requires expert verification:**
- Whether peer support practitioners would recognize their communicative patterns in HOPE's taxonomy
- Whether crisis intervention staff would consider the IRQ/YNQ collapse acceptable for their workflow

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
HOPE's source corpus is YouTube-sourced US-based counseling sessions [Q23, Q98], with the authors explicitly warning that 'the effectiveness of SPARTA on data from other geographical or demographical regions may vary' [Q99]. The deployment extends to South Asian (India and broader) contexts, where formality and counselor-directiveness norms may differ — though the user judges core label applicability to be largely intact (elicitation A2). YouTube selection bias likely suppresses disfluencies and false starts characteristic of real-time teletherapy [Q93]. Sessions are notably long (~59 utterances; therapist ~124 words/utterance) [Q56, Q57], reflecting structured formal therapy rather than peer support's shorter-turn register. No South Asian sessions or peer support sessions are present in the corpus. The South Asian deployment is HIGH-priority by user assessment but ranked MODERATE in the elicitation weights, since the user views label-level transfer as plausible. Combined gaps in geographic representation and session-type representation justify a score of 2.

**Strengths:**
- Reasonable scale (~12.9K utterances across 212 sessions) and balanced patient/therapist distribution [Q53, Q54]
- Authors transparently acknowledge US-centricity and explicitly caveat geographical/demographic generalization [Q98, Q99]
- Confidentiality handled via synthetic name assignment [Q24] and systematic name masking [Q97]

**Checklist:**

- **IC-1**: Yes — South Asian English clinical communication, including formality norms and counselor directiveness, may differ from US YouTube-sourced content. The user identifies this as a real but not acute concern (elicitation A2). National Mental Health Survey of India documented 75–93% treatment gaps and significant urban-rural heterogeneity [WEB-1], suggesting India-context delivery patterns differ materially from US. — _Sources: Q98, Q99, WEB-1_
- **IC-2**: Partial mismatch — content reflects US clinical communication norms and structured therapy register. Peer support and crisis register are entirely absent; South Asian register is unrepresented. — _Sources: Q98, Q56, Q57_
- **IC-3**: Yes — sessions encode US counselor directiveness and therapeutic framing conventions [Q98]. The extent to which these transfer to South Asian English clinical settings is documented as a deferred verification item in the regional context. — _Sources: Q98, Q99_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no regional annotators from South Asia or peer/crisis settings were recruited; geographic origin of annotators not specified beyond institutional affiliation.
- **IC-5**: Documented issues: (a) US-centricity acknowledged by authors [Q98, Q99]; (b) YouTube selection bias likely suppresses ASR-relevant phenomena like disfluencies/false starts [Q93]; (c) absence of peer support and crisis intervention content; (d) sessions are atypically long [Q56, Q57], representing formal therapy rather than the shorter-turn dynamics of OMHC peer/crisis exchanges. — _Sources: Q98, Q99, Q93, Q56, Q57_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q23] 'we carefully explored the web and collected publicly-available pre-recorded counselling videos on YouTube' (p.3)
- [Q98] 'the majority of the sessions in HOPE belong to the mental health professionals and patients based in United States' (p.8)
- [Q99] 'the effectiveness of SPARTA on data from other geographical or demographical regions may vary' (p.8)
- [Q56] 'the dialogue sessions in HOPE are usually lengthy (∼ 59 utterances per session)' (p.5)
- [Q57] 'the average length of utterance of a patient being 103 words, whereas for therapist, it is ∼ 124 words' (p.5)
- [Q93] 'We transcribe the data from publicly available counselling videos' (p.8)

*Web sources:*
- [WEB-1] National Mental Health Survey of India 2016 reported treatment gaps of 75–93% with significant urban-rural heterogeneity, indicating substantively different delivery patterns from US
- [WEB-16] Tele MANAS represents a distinct India-context deployment with different practitioner profiles and technology maturity than commercial OMHC platforms

</details>

**Information gaps:**
- Empirical comparison of South Asian English vs. US English counseling discourse [deferred — likely unsearchable]
- Quantitative comparison of YouTube-sourced vs. live teletherapy ASR transcripts for mental-health sessions
- Demographic breakdown of HOPE session participants beyond US-majority claim

**Requires expert verification:**
- Whether South Asian clinical psychologists view core HOPE label boundaries as preserved under Indian English directiveness norms
- Whether peer support and crisis content patterns differ enough from clinical content to invalidate model behavior trained on HOPE

---

### Input Form — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Both benchmark and deployment are text-only English with Latin script — no script or modality mismatch. ASR pipeline (OTTER + manual correction) [Q25] is text-aligned with deployment's teletherapy ASR transcripts. However, the benchmark text is hand-corrected for spelling and grammatical errors [Q25] and the authors acknowledge information loss in the speech-to-text pipeline [Q94], whereas live teletherapy transcripts will likely retain greater disfluency density, false starts, and overlapping turns. This is a latent form mismatch that the benchmark documentation does not address. Infrastructure assumptions are aligned for US contexts but India rural connectivity may degrade ASR quality [WEB-16, WEB-1]. Given the user's LOWER priority for IF and the absence of script/modality mismatch, a moderate score of 3 reflects the meaningful but bounded gap.

**Strengths:**
- No script or modality mismatch — both benchmark and deployment operate on English Latin-script text [Q25]
- Standard tokenization-friendly input via pretrained RoBERTa [Q61, Q111] is widely supported in deployment infrastructure
- Documented systematic name masking for privacy [Q97] aligns with HIPAA/DPDPA expectations

**Checklist:**

- **IF-1**: Partial mismatch — HOPE used hand-corrected OTTER transcripts [Q25], while live teletherapy ASR will not benefit from manual correction. Disfluency, false-start, and overlapping-turn distributions will likely differ. — _Sources: Q25, Q94_
- **IF-2**: US infrastructure adequate; India rural connectivity remains uneven [WEB-1, WEB-16]. Tele MANAS implementation challenges include 'overworked personnel, technology glitches, and uneven rural access' [WEB-16]. — _Sources: WEB-1, WEB-16_
- **IF-3**: Real-time teletherapy ASR vs. recorded YouTube ASR is the key domain-specific difference. Authors acknowledge information loss generally [Q94] but do not quantify the gap. — _Sources: Q25, Q93, Q94_
- **IF-4**: Documented form concerns: (a) hand-correction step in HOPE [Q25] not available in live deployment; (b) YouTube source data may be lightly edited or pre-selected [Q93]; (c) no quantitative comparison available between YouTube and real-time clinical ASR fidelity. — _Sources: Q25, Q93, Q94_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q25] 'we extract the transcriptions of each video using OTTER... we correct transcription errors to remove any noise (i.e., spelling or grammatical mistakes)' (p.3)
- [Q94] 'the automatic transfer of utterance from the speech modality to the text causes some information loss, though we tried our best to recover them through manual intervention' (p.8)
- [Q97] 'The names of the patients and therapists involved in these sessions have been systematically masked' (p.8)
- [Q61] 'we extract the semantic representation through pre-trained RoBERTa model' (p.5)

*Web sources:*
- [WEB-1] Indian rural connectivity and resource gaps documented in National Mental Health Survey context
- [WEB-16] Tele MANAS implementation faces technology glitches and uneven rural access

</details>

**Information gaps:**
- Quantitative comparison of YouTube-sourced vs. real-time teletherapy ASR fidelity for mental-health sessions [deferred]
- Platform-specific ASR quality benchmarks for OMHC platforms (proprietary, not searchable)

**Requires expert verification:**
- Whether disfluency-rich live ASR transcripts degrade SPARTA/HOPE-trained model performance materially

---

### Output Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
The 12-label taxonomy is explicitly 'aligned with mental-health counseling session' [Q17, Q104] and was designed in consultation with therapists [Q27]. The user judges the taxonomy fit-for-purpose for conversational flow tracking (elicitation A3). However, internal taxonomy stress is documented: ACK underperforms at F1=47.86% [Q77], indicating semantic overload even within clinical scope; confusion analysis shows YNQ:IRQ (26%), OD:ID (43%), ID:ACK (28%) error rates [Q91]; complementary label pairs are 'annotation-boundary-challenging' [Q51, Q52]. For the deployment's peer support and crisis extensions, the GC catch-all [Q44] becomes the de facto repository for any communicative act outside the clinical frame, and crisis-specific acts (safety-planning, risk stratification) lack dedicated labels — collapsing into IRQ/YNQ with potentially safety-critical consequences. The discarded emotion annotation pilot [Q126, Q127, Q129] indicates the authors recognized affective dimensions but chose not to incorporate them. Output is single-label per utterance [Q30], which is appropriate for the framing but limits expressiveness for utterances spanning multiple acts. Score of 3 reflects fit-for-purpose taxonomy for in-scope clinical use but real boundary ambiguity at deployment edges.

**Strengths:**
- Taxonomy designed in consultation with therapists and counseling experts [Q27], grounded in counseling-session requirements rather than borrowed
- Three-tier hierarchical structure (initiative/responsive/general) [Q29, Q32] provides interpretable organization
- Per-label F1 reporting [Q76] surfaces label-level performance limitations transparently
- Authors explicitly disclaim diagnostic intent [Q102], appropriate for a flow-classification scope

**Checklist:**

- **OO-1**: Labels are nominally regionally relevant (greeting, information delivery, etc. are universal) but encode US clinical session structure assumptions [Q98]. South Asian directiveness norms may shift label-boundary behavior. — _Sources: Q17, Q27, Q98_
- **OO-2**: Missing categories: (a) crisis-specific safety-planning and risk-assessment acts; (b) peer support emotional co-regulation acts; (c) empathic reflection vs. simple acknowledgment distinction (the user notes this is an intentional out-of-scope choice — A3); (d) affective dimension was piloted but discarded due to imbalance [Q126, Q127, Q129]. — _Sources: Q126, Q129, WEB-2, WEB-18_
- **OO-3**: GC as a residual catch-all [Q44] effectively encodes 'not part of the structured clinical frame' as a category, which biases against acts characteristic of peer/crisis registers. Speaker asymmetry [Q125] presupposes therapist-patient hierarchy not present in peer dyads. — _Sources: Q44, Q125_
- **OO-4**: Stakeholder-driven taxonomy redesign is needed for crisis-context deployment specifically; for in-scope clinical and South Asian extensions, the user judges core labels acceptable (A3). — _Sources: Q102_
- **OO-5**: Documented issues: ACK overload [Q77], complementary-pair confusion [Q51, Q52, Q91], lack of crisis or peer support labels, abandoned emotion dimension, and the GC residual category becoming a semantic black hole for out-of-frame utterances. — _Sources: Q77, Q91, Q51, Q52, Q44_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q17] 'We propose twelve dialogue-act labels that are aligned with mental-health counseling session' (p.2)
- [Q27] 'in consultation with therapist and counselling experts, design a set of 12 dialog-act labels that are arranged in a hierarchy' (p.3)
- [Q44] 'Other utterances that do not belong to any of the above labels are tagged as GC' (p.4)
- [Q51] 'The broad definitions of speaker-initiative and speaker-responsive dialogue-act label pairs, IRQ & ID; ORQ & OD, and CRQ & CD, seem complementary in nature' (p.4)
- [Q77] 'SPARTA consistently yields good scores for the majority of the dialogue-acts, except for the Acknowledgement (ACK) where it records F1-score of merely 47.86%' (p.7)
- [Q91] 'three pairs with significant error-rates (≥ 25%) – YNQ:IRQ (26%), OD:ID (43%), ID:ACK (28%)' (p.7)
- [Q126] 'In earlier phases of experiments, we also considered the role of emotion in dialogue act classification' (p.11)
- [Q129] 'Due to such imbalance, this data was not used in the final version' (p.11)
- [Q102] 'we do not make any diagnostic claims' (p.8)

*Web sources:*
- [WEB-2] 988 Lifeline three-phase crisis model uses communicative acts not represented in HOPE labels
- [WEB-18] ESConv 8-strategy framework for peer support is structurally distinct from HOPE

</details>

**Information gaps:**
- Per-label inter-annotator agreement breakdown (only aggregate Kappa reported)
- How GC and ACK absorb peer/crisis acts in practice — no empirical validation

**Requires expert verification:**
- Whether crisis intervention staff can operate with IRQ/YNQ collapse for safety-planning probes
- Whether peer support practitioners would adopt the speaker-asymmetric taxonomy

---

### Output Content — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
Annotation was performed by three linguists with calibration and an expert-therapist moderator [Q45, Q46, Q47], with mental health professional consultation during guideline preparation [Q95]. Aggregate Cohen's Kappa = 0.7234 (substantial) [Q49] is reasonable. The user judges the convergent-validity risk low because dialogue-act labels are communicative rather than clinical (elicitation A4). However, there are real concerns: no per-label or per-session-type Kappa breakdown is reported, so agreement on overloaded labels (ACK, GC) is unknown; no documented South Asian, peer support, or crisis worker participation in annotation; annotator demographics are limited to age and experience range [Q50] with no geographic or cultural background reported; authors acknowledge 'annotator's bias cannot be ruled out completely' [Q96]. Given the user's MODERATE priority on OC and the partial documentation, a score of 3 reflects substantial agreement on a US-clinical-centric annotation framework with unverified cross-cultural and cross-session-type calibration.

**Strengths:**
- Multi-annotator process with calibration exercise and expert-therapist moderation [Q46, Q47]
- Substantial aggregate inter-annotator agreement (Kappa = 0.7234) [Q49]
- Mental health professional and linguist consultation during guideline preparation [Q95]
- Authors transparently acknowledge residual annotator bias risk [Q96]

**Checklist:**

- **OC-1**: Partially — labels reflect US clinical communication norms as encoded by linguistically-trained annotators with therapist moderation; South Asian and peer/crisis stakeholder perspectives are not documented as represented. — _Sources: Q45, Q47, Q95_
- **OC-2**: Risk is bounded for in-scope clinical structured therapy (user judges A4 risk low) but unverified for South Asian clinical contexts, peer support practitioners, and crisis workers, none of whom are documented as annotators. — _Sources: Q50, Q96_
- **OC-3**: Limited annotator documentation [Q50] — three linguists, ages 25–35, 2–10 years experience, expert-therapist moderator. No geographic, cultural, gender, or clinical-affiliation breakdown. — _Sources: Q50_
- **OC-4**: Re-annotation by representative regional pool (South Asian clinicians, peer support workers, crisis staff) is not documented. The user's elicitation reasoning (A4) explicitly accepts this on grounds that labels are communicative, not clinical.
- **OC-5**: Aggregation method is consensus discussion moderated by expert therapist [Q47]; this could erase minority annotator perspectives (e.g., on ambiguous ACK boundaries), though no minority-perspective tracking is reported. — _Sources: Q47_
- **OC-6**: Documented issues: aggregate-only Kappa with no per-label or per-session-type breakdown; no cross-cultural annotator validation; complementary label pairs explicitly known to be challenging [Q51, Q52]; explicit acknowledgment of unresolved annotator bias [Q96]. — _Sources: Q49, Q51, Q52, Q96_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q45] 'We employed three annotators who are experts in linguistics' (p.4)
- [Q46] 'we took a sample of the dataset and asked each annotator to annotate them as per the prepared set of guidelines' (p.4)
- [Q47] 'every annotation was discussed in the presence of the annotators and an expert therapist as moderator to ensure consistency' (p.4)
- [Q49] 'We obtain the inter-rater agreement score of 0.7234 – which falls under the substantial category' (p.4)
- [Q50] 'Annotators are in the age group of 25-35, with 2-10 years of professional experience' (p.4)
- [Q95] 'we consulted with mental-health professionals and linguists in preparing the annotation guideline' (p.8)
- [Q96] 'However, the annotator's bias cannot be ruled out completely' (p.8)

</details>

**Information gaps:**
- Per-label and per-session-type Kappa breakdown [deferred — not in available paper sections]
- Annotator geographic, cultural, and clinical-background details
- Whether South Asian clinicians or peer/crisis workers were consulted at any stage

**Requires expert verification:**
- Whether South Asian psycholinguists would label ambiguous ACK/GC utterances consistently with HOPE annotators
- Whether peer support practitioners would assign the same labels to peer-register utterances

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Output form is single-label classification per utterance [Q14, Q30] with macro-F1, weighted-F1, and accuracy metrics [Q63] plus label-wise F1 reporting [Q76]. Statistical significance via T-test at >95% confidence is reported [Q88], and 3-fold cross-validation results are consistent with split-based results [Q87]. The output modality (categorical labels over text utterances) directly matches the deployment's expected output for session quality assessment and counselor feedback. Macro-F1 weights all classes equally regardless of frequency, appropriate for the imbalanced label distribution. The user marks OF as LOWER priority (form is well matched). Minor concerns: macro-F1 does not surface per-label safety-critical performance directly (e.g., crisis-relevant IRQ/YNQ behavior is averaged in); error analysis [Q89, Q90] is on in-distribution data only and does not assess behavior on out-of-scope (peer/crisis) utterances. Score of 4 reflects strong form alignment with minor diagnostic limitations.

**Strengths:**
- Output modality (categorical labels) directly matches deployment use case for flow classification [Q14, Q63]
- Multiple complementary metrics reported (macro-F1, weighted-F1, accuracy) [Q63] including per-label F1 [Q76]
- Statistical significance testing [Q88] and 3-fold cross-validation [Q87] support reliability claims
- Quantitative and qualitative error analysis [Q89, Q90, Q91] provides interpretable failure-mode information

**Checklist:**

- **OF-1**: Yes — categorical-label output over text utterances matches deployment requirements (session flow classification for feedback/supervision). — _Sources: Q14, Q30, Q63_
- **OF-2**: Not applicable — deployment is text-only; no TTS requirement indicated in deployment context.
- **OF-3**: Not applicable as a primary concern — practitioners (not therapy clients) are the system's users; literacy is high in the practitioner population.
- **OF-4**: Minor gaps: no separate evaluation of safety-critical label categories; no out-of-distribution evaluation framework for peer/crisis utterances; macro-F1 averaging may mask label-specific failure modes that matter for clinical review. — _Sources: Q76, Q63_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q14] 'Each utterance in the dataset is tagged with one of the 12 counseling-aligned dialogue-act labels' (p.2)
- [Q30] 'for simplicity, we consider only one (primary) label for each utterance' (p.3)
- [Q63] 'we compute macro-F1, weighted-F1, and accuracy scores' (p.6)
- [Q76] 'We also present the label-wise performance of SPARTA in Table 4' (p.7)
- [Q87] 'we also report the mean of the 3-fold cross-validation results... and the results are consistent with the train-val-test split case' (p.7)
- [Q88] 'our results are significant with > 95% confidence across macro-F1 (p-value= 0.009), weighted-F1 (p-value= 0.014), and accuracy (p-value= 0.048)' (p.7)

</details>

**Information gaps:**
- No reported evaluation framework for safety-critical label subsets
- No reported out-of-distribution behavior on peer/crisis-register utterances

**Requires expert verification:**
- Whether macro-F1 at the reported 60.29 threshold is sufficient for supervisory feedback in clinical training contexts

---

## Remediation Suggestions

### Input Ontology ⚠

**Gap:** No dedicated label coverage for crisis-specific (safety-planning, risk-stratification, de-escalation) or peer-support (mutual disclosure, emotional co-regulation) communicative acts; these collapse into IRQ/YNQ/GC.

**Recommendation:** Before deploying in crisis or peer-support contexts, extend the taxonomy with crisis-specific labels informed by the 988 Lifeline three-phase model [WEB-2] and peer-support strategy labels informed by ESConv [WEB-18]. Validate the extended taxonomy on a held-out sample of crisis and peer-support transcripts before integrating into production feedback workflows.

### Input Content ⚠

**Gap:** Source corpus is overwhelmingly US-based [Q98] with no South Asian sessions and no peer-support or crisis-intervention content.

**Recommendation:** Collect and annotate a supplementary evaluation set of South Asian English clinical sessions, OMHC peer-support transcripts, and crisis-intervention exchanges. Use this set strictly for validation (not training) to estimate performance drift relative to HOPE's reported metrics.

### Input Form

**Gap:** HOPE uses hand-corrected ASR transcripts [Q25]; live teletherapy ASR will retain disfluencies and errors that the benchmark does not represent.

**Recommendation:** Run an A/B comparison of model performance on hand-corrected vs. raw ASR samples from the target deployment platforms. If material degradation is observed, consider ASR post-processing, disfluency-aware fine-tuning, or confidence thresholding before surfacing labels to supervisors.

### Output Content

**Gap:** No documented South Asian, peer-support, or crisis-worker annotators; aggregate-only Kappa of 0.7234 [Q49] cannot reveal cross-cultural or cross-session-type calibration.

**Recommendation:** Convene a small expert panel of South Asian clinical psychologists, peer-support practitioners, and crisis-intervention staff to re-annotate a stratified evaluation subset. Compute disagreement rates relative to HOPE's labels and use these to bound deployment confidence by stakeholder type.

### Output Form

**Gap:** Macro-F1 averaging masks safety-critical label performance; no out-of-distribution evaluation for peer/crisis utterances [Q63, Q76].

**Recommendation:** Report and monitor per-label F1 (especially IRQ, YNQ, ACK, GC) separately in deployment dashboards. Add an out-of-distribution detection layer that flags utterances likely outside the trained label distribution rather than forcing a label assignment, particularly for crisis-context deployment.

### Output Ontology

**Gap:** ACK label is semantically overloaded (F1=47.86%) [Q77] and GC functions as a residual catch-all [Q44]; per-label and per-session-type Kappa breakdowns are unavailable.

**Recommendation:** Request or compute per-label and per-session-type inter-annotator agreement on a re-annotated subset. For deployment, suppress or flag (rather than display) ACK and GC predictions in supervisory dashboards until reliability is independently validated.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "We develop a novel dataset, named HOPE, to provide a platform for the dialogue-act classification in counselling conversations." |
| Q2 | 1 | output_ontology | "We identify the requirement of such conversation and propose twelve domain-specific dialogue-act (DAC) labels." |
| Q3 | 1 | input_content | "We collect ∼ 12.9𝐾 utterances from publicly-available counselling session videos on YouTube, extract their transcripts, clean, and annotate them with DAC labels." |
| Q4 | 1 | input_ontology | "Further, we propose SPARTA, a transformer-based architecture with a novel speaker- and time-aware contextual learning for the dialogue-act classification." |
| Q5 | 1 | output_form | "Our evaluation shows convincing performance over several baselines, achieving state-of-the-art on HOPE." |
| Q6 | 1 | output_form | "We also supplement our experiments with extensive empirical and qualitative analyses of SPARTA." |
| Q7 | 1 | input_ontology | "Unlike general goal-oriented dialogues, a conversation between a patient and a therapist is considerably implicit, though the objective of the conversation is quite apparent." |
| Q8 | 1 | input_ontology | "The nature of conversations in a social counselling setting is particularly distinct as compared to a conventional chit-chat or goal-oriented conversations." |
| Q9 | 1 | input_ontology | "It follows a pattern which is different from both goal-oriented and general chit-chat based conversations." |
| Q10 | 1 | input_ontology | "Usually these conversations begin with greetings followed by the therapist inquiring for problems faced by the patient." |
| Q11 | 1 | input_content | "Ganeshan Malhotra, Abdul Waheed, Aseem Srivastava, Md Shad Akhtar, Tanmoy Chakraborty." |
| Q12 | 1 | input_content | "1BITS Pilani, Goa, India, 2Maharaja Agrasen Institute of Technology, New Delhi, India, 3IIIT-Delhi, India." |
| Q13 | 2 | input_content | "The HOPE dataset contains ∼ 12.9K utterances across 212 mental-health counseling sessions." |
| Q14 | 2 | output_ontology | "Each utterance in the dataset is tagged with one of the 12 counseling-aligned dialogue-act labels (c.f. Section 3)." |
| Q15 | 2 | input_content | "We present HOPE, a novel and large-scale manually annotated, counselling-based conversation data for dialogue-act classification." |
| Q16 | 2 | output_content | "To cater to the requirements of counseling conversations, we define a novel hierarchical annotation scheme for the dialogue-act annotation." |
| Q17 | 2 | output_ontology | "We propose twelve dialogue-act labels that are aligned with mental-health counseling session." |
| Q18 | 2 | input_ontology | "We propose SPARTA, a novel dialogue-act classification system that combines speaker-dynamics and local context through a time-aware attention mechanism, along with long-term global context." |
| Q19 | 2 | output_form | "We perform extensive ablation study to establish the efficacy of each module of SPARTA." |
| Q20 | 2 | input_content | "We have made the code and (a subset of) the dataset available at github." |
| Q21 | 2 | input_ontology | "The current work is connected to the existing literature in at least two dimensions – first, the dialogue-act classification, and second, text processing for mental-health counseling." |
| Q22 | 3 | input_ontology | "In this section, we present our dialogue-act classification dataset, called HOPE. In total, we annotated ∼ 12.9𝐾 utterances with 12 dialogue-act labels carefully designed to cater to the requirements of a counseling session." |
| Q23 | 3 | input_content | "One of major hurdles we faced in the process of data collection was the unavailability of public counseling sessions, mainly due to the fact that they usually contain sensitive personal information. To curate this data, we carefully explored the web and collected publicly-available pre-recorded counselling videos on YouTube." |
| Q24 | 3 | input_content | "To ensure confidentiality, we randomly assign synthetic names to all patients and therapists in all examples." |
| Q25 | 3 | input_form | "In the next step, we extract the transcriptions of each video using OTTER (https://www.otter.ai/), an automatic speech recognition tool. Subsequently, we correct transcription errors to remove any noise (i.e., spelling or grammatical mistakes)." |
| Q26 | 3 | input_content | "The data collection process provides us 12.9𝐾 utterances from 212 counseling therapy sessions – all of them are dyadic conversations only." |
| Q27 | 3 | output_ontology | "Since the counseling conversations have inherent differences with the standard conversations (such as SwitchBoard dataset conversation), it demands a carefully designed set of dialogue-act labels capable of catering the requirements of counselling conversations. Hence, we, in consultation with therapist and counselling experts, design a set of 12 dialog-act labels that are arranged in a hierarchy." |
| Q28 | 3 | output_ontology | "These labels are designed to capture the intents of both the patient and therapist, and also be easily comprehensible to assist in the development of a conversational dialogue system." |
| Q29 | 3 | output_ontology | "Each utterance in the dialogue belongs to one of the three categories – speaker initiative, speaker responsive, and general." |
| Q30 | 3 | output_ontology | "Sometimes, an utterance can have multiple dialog-acts; however, they are rare in the annotated dataset. Hence, for simplicity, we consider only one (primary) label for each utterance." |
| Q31 | 4 | input_form | "The train, test, and validation splits are 70:20:10" |
| Q32 | 4 | output_ontology | "Our annotation scheme assigns three distinct dialogue-act labels to the first two categories, while the remaining four labels belong to the general category." |
| Q33 | 4 | output_ontology | "Information Request (IRQ): This label is used as a request for some information, e.g., 'Tell me your name.'" |
| Q34 | 4 | output_ontology | "Yes/No Question (YNQ): The YNQ label is similar to IRQ; however, the expected response is a trivial yes or no answer." |
| Q35 | 4 | output_ontology | "Clarification Request (CRQ): This label is assigned to those utterances in which a speaker usually asks the therapist for further clarification about topic that is being currently discussed." |
| Q36 | 4 | output_ontology | "Opinion Request (ORQ): The ORQ label is used when the speaker seeks opinions of the listener." |
| Q37 | 4 | output_ontology | "Clarification Delivery (CD): This label is used when the speaker provides further clarifications about a topic/entity under discussion." |
| Q38 | 4 | output_ontology | "Information Delivery (ID): When the speaker provides some factual objective information about herself." |
| Q39 | 4 | output_ontology | "Positive Answer (PA): These labels are used when the utterance is an answer in the form of a simple yes to a question that was previously uttered." |
| Q40 | 4 | output_ontology | "Negative Answer(NA): It is used when the utterance is an answer of the form of a simple No to a question asked earlier." |
| Q41 | 4 | output_ontology | "Opinion Delivery (OD): When the speaker explicitly lists out her/his opinions." |
| Q42 | 4 | output_ontology | "Greeting (GT): Each session usually starts with greeting by one speaker and an appropriate response from the other." |
| Q43 | 4 | output_ontology | "Acknowledgment (ACK): In normal conversation, very often, we utter (e.g., 'Yeah! You are right.') to acknowledge the other speaker or to show our agreement without an explicit information request, question, or command." |
| Q44 | 4 | output_ontology | "General Chit-Chat (GC): Other utterances that do not belong to any of the above labels are tagged as GC, possibly because of the vagueness and the lack of sense in the context of the conversation." |
| Q45 | 4 | output_content | "We employed three annotators who are experts in linguistics." |
| Q46 | 4 | output_content | "To ensure the understanding of the tasks and annotation scheme, we took a sample of the dataset and asked each annotator to annotate them as per the prepared set of guidelines." |
| Q47 | 4 | output_content | "Following this, every annotation was discussed in the presence of the annotators and an expert therapist as moderator to ensure consistency." |
| Q48 | 4 | output_content | "After the annotation process, we compute Cohen's Kappa score [7] to measure the agreement among annotators." |
| Q49 | 4 | output_content | "We obtain the inter-rater agreement score of 0.7234 – which falls under the 'substantial' [7] category." |
| Q50 | 4 | output_content | "Annotators are in the age group of 25-35, with 2-10 years of professional experience." |
| Q51 | 4 | output_ontology | "The broad definitions of speaker-initiative and speaker-responsive dialogue-act label pairs, IRQ & ID; ORQ & OD, and CRQ & CD, seem complementary in nature." |
| Q52 | 4 | output_ontology | "However, the dataset does not support the above view entirely." |
| Q53 | 5 | input_content | "In total, HOPE has transcripts for 12.9𝑘 utterances which are annotated with 12 dialogue-act labels." |
| Q54 | 5 | input_content | "These utterances are evenly distributed between the patients and therapists with 6.38𝐾 and 6.47𝐾 utterances, respectively." |
| Q55 | 5 | input_form | "We split the dataset into 70:20:10 ratio as the train, test, and validation sets, respectively." |
| Q56 | 5 | input_content | "In contrast to the regular patient-doctor conversations (e.g., SOAP), the dialogue sessions in HOPE are usually lengthy (∼ 59 utterances per session)." |
| Q57 | 5 | input_content | "Moreover, the utterances in these sessions are themselves significantly longer as compared to other conversational datasets, with the average length of utterance of a patient being 103 words, whereas for therapist, it is ∼ 124 words." |
| Q58 | 5 | input_ontology | "The objective of SPARTA is to assign a correct dialogue-act label 𝑦𝑡 to every utterance 𝑈𝑡in the dialogue." |
| Q59 | 5 | input_ontology | "SPARTA is a transformer-based architecture that incorporates the speaker-aware contextual information for the dialogue-act classification." |
| Q60 | 5 | input_content | "In our analysis of the HOPE dataset, we observed that a few of the dialogue-act labels are majorly associated with the patient, while a few others are related to the therapist." |
| Q61 | 5 | input_form | "For each utterance 𝑈𝑡 in a conversation dialogue, we extract the semantic representation through pre-trained RoBERTa model [25], which is subsequently utilized to leverage the local (𝐿𝑡) and global (𝐺𝑡) contextual information within the dialogue." |
| Q62 | 6 | input_form | "For the experiments, we randomly split the HOPE dataset into 70 : 20 : 10 ratio for the train, test, and validation sets." |
| Q63 | 6 | output_form | "To measure the performances of SPARTA and other baseline systems, we compute macro-F1, weighted-F1, and accuracy scores." |
| Q64 | 6 | input_form | "We implemented our system in PyTorch [32] and utilized the pre-trained models from Huggingface Transformers library." |
| Q65 | 6 | input_form | "The hyperparameters are listed in Table 6." |
| Q66 | 6 | input_ontology | "CASA [35]: It is a context-aware attention-based system for the dialogue-act classification." |
| Q67 | 6 | input_ontology | "SA-CRF [41]: This recent baseline incorporates a CRF layer for the classification." |
| Q68 | 6 | input_ontology | "DRNN [44]: It is a novel Disconnected RNNs architecture which incorporates the position-invariant features for modelling." |
| Q69 | 6 | input_ontology | "ProSeqo [16]: It was proposed to efficiently handle the short and long texts using dynamic recurrent projections and locality-sensitive projections [37]." |
| Q70 | 6 | input_ontology | "TextVDCNN [9]: This is a deep convolutional network with residual connections for text classification." |
| Q71 | 6 | input_ontology | "TextRNN [24]: This was the first work to integrate RNNs into the multi-task learning framework." |
| Q72 | 6 | input_ontology | "RoBERTa [25]: We use RoBERTa as a baseline in this work due to its superioirity on various benchamarks." |
| Q73 | 6 | output_form | "Since SPARTA incorporates three major components – local context, global context, and speaker-aware modules. The SPARTA-TAA system obtains the best scores of 60.29 macro-F1, 64.53 weighted-F1," |
| Q74 | 7 | output_form | "Table 3: Table showcasing the performance of baseline models as compared with our SPARTA model. 𝑈𝑡 represents the use of Utterance representation, GC represents Global Context, LC represents Local Context and SA means the presence of Speaker Aware representations." |
| Q75 | 7 | output_form | "The dagger symbol (†) represents statistically significant results compared to the best baseline, CASA." |
| Q76 | 7 | output_form | "We also present the label-wise performance of SPARTA in Table 4." |
| Q77 | 7 | output_form | "We can observe that SPARTA consistently yields good scores for the majority of the dialogue-acts, except for the Acknowledgement (ACK) where it records F1-score of merely 47.86%." |
| Q78 | 7 | output_form | "Even for the under-represented labels (ORQ,NA and PA) in HOPE, SPARTA reports good F1-scores of 59.09%, 64.38% and 55.84%, respectively for these three labels." |
| Q79 | 7 | input_ontology | "Based on the type of modelling, we categorize the baselines into three groups – utterance-driven (𝑈𝑡), utterance+global context driven (𝑈𝑡 + GC), and utterance + global context + speaker-aware driven (𝑈𝑡 + GC + SA)." |
| Q80 | 7 | input_ontology | "Comparatively, SPARTA incorporates local context in addition to utterance, global context, and speaker dynamics (𝑈𝑡 + LC + GC + SA)." |
| Q81 | 7 | output_form | "In the first category, the standard RoBERTa model attains the best macro-F1, weighted-F1 and accuracy of 43.97, 49.13, and 52.97%, respectively." |
| Q82 | 7 | output_form | "In comparison, CASA [35] yields the improved weighted-F1 and accuracy scores at 55.95% (+6.82%) and 58.46% (+5.49%), respectively, with the global context as an additional information." |
| Q83 | 7 | output_form | "Finally, we experiment with SA-CRF [41] which also includes the speaker-dynamics for the dialogue-act classification; however, its performance on HOPE is not at par with CASA [35]." |
| Q84 | 7 | output_form | "It reports 35.97, 24.20, and 45.07% macro-F1, weighted-F1, and accuracy, respectively." |
| Q85 | 7 | output_form | "In comparison, SPARTA-TAA obtains significant improvements over all baselines. It reports improvements of +8.64%, +8.58%, and +6.29% in macro-F1 (60.29), weighted-F1 (64.53), and accuracy (64.75%), respectively, as compared to CASA suggesting the incorporation of local context extremely effective." |
| Q86 | 7 | output_form | "Note that ProSeqo [16] and CASA [35] are currently the state-of-the-art on switchboard dialogue-act corpus benchmark; yet they report inferior scores on HOPE compared to SPARTA." |
| Q87 | 7 | output_form | "Moreover, we also report the mean of the 3-fold cross-validation results for both SPARTA-MHA and SPARTA-TAA, and the results are consistent with the train-val-test split case." |
| Q88 | 7 | output_form | "We also perform statistical significance T-test comparing SPARTA-TAA and the best performing baseline (CASA). We observe that our results are significant with > 95% confidence across macro-F1 (p-value= 0.009), weighted-F1 (p-value= 0.014), and accuracy (p-value= 0.048) values." |
| Q89 | 7 | output_form | "Error Analysis: In this section, we present two-way error analyses of SPARTA in terms of quantitative and qualitative evaluations." |
| Q90 | 7 | output_form | "Quantitative analysis: We report the confusion matrix for SPARTA-TAA in Figure 4." |
| Q91 | 7 | output_ontology | "We observe three pairs with significant error-rates (≥ 25%) – YNQ:IRQ (26%), OD:ID (43%), ID:ACK (28%)." |
| Q92 | 7 | output_ontology | "For the prediction of information delivery (ID), SPARTA is confused most of the time with other classes – 19% with PA, 20% with NA, 43% with OD." |
| Q93 | 8 | input_content | "We aim to tackle a very sensitive and a pervasive public-health crisis. We transcribe the data from publicly available counselling videos." |
| Q94 | 8 | input_form | "The automatic transfer of utterance from the speech modality to the text causes some information loss, though we tried our best to recover them through manual intervention." |
| Q95 | 8 | output_content | "Moreover, we consulted with mental-health professionals and linguists in preparing the annotation guideline." |
| Q96 | 8 | output_content | "However, the annotator's bias cannot be ruled out completely." |
| Q97 | 8 | input_form | "The names of the patients and therapists involved in these sessions have been systematically masked." |
| Q98 | 8 | input_content | "Another important aspect of the current work is that the majority of the sessions in HOPE belong to the mental health professionals and patients based in United States." |
| Q99 | 8 | input_content | "Hence, the effectiveness of SPARTA on data from other geographical or demographical regions may vary." |
| Q100 | 8 | output_content | "We understand that the building computational models in mental-health avenues has high-stakes associated with it and ethical considerations, therefore, become necessary." |
| Q101 | 8 | output_content | "No technology will work perfectly in solving the problems related to mental health." |
| Q102 | 8 | output_ontology | "It is important to note that we do not make any diagnostic claims." |
| Q103 | 8 | output_content | "Further, the deployment of any such technology will be done keeping in mind the safety-risks and mitigating any sources of bias that may arise." |
| Q104 | 8 | output_ontology | "We defined twelve dialogue-act labels to cater to the requirement of counselling sessions." |
| Q105 | 8 | input_content | "In total, we annotated ∼ 12.9𝑘 utterances across 212 sessions." |
| Q106 | 8 | input_content | "The authors acknowledge the support of the Ramanujan Fellowship, ihub-Anubhuti-iiitd Foundation set up under the NM-ICPS scheme of the DST, and CAI at IIIT-Delhi." |
| Q107 | 10 | input_form | "We use PyTorch 11 and Pytorch Lightning 12 frameworks for all our experiments. We extensively used Hugging Face Library for implementation of transformer based NLP models." |
| Q108 | 10 | input_form | "The complete model training was done on a linux machine with following specifications: GPU: TeslaV100, Memory: 32GB, Linux 64 Bit: Ubuntu 18.04 LTS" |
| Q109 | 10 | output_form | "We use WandB13 library to log all our results." |
| Q110 | 10 | output_form | "The categorical cross-entropy loss is optimized using the Adam optimizer. We use dropout= 0.15 and train the models for 50 epochs in a batch of 8 samples. We use EarlyStopping to prevent our model from overfiting." |
| Q111 | 10 | input_form | "We use pretrained RoBERTa available from the Hugginface14 transformers for speaker aware as well as speaker invariant utterance representations." |
| Q112 | 10 | input_form | "For the GRU, we use input size and hidden dimension of 768 with 1 layer. For the classifier sub-module, we use a dropout of 0.1 a linear layer of 768 neurons and LeakyReLU as the activation." |
| Q113 | 10 | input_form | "Our attention blocks comprise of 3 Linear Layers for keys,queries and values and one linear layer to project the keys, queries and values." |
| Q114 | 11 | output_form | "To verify the effectiveness of the time-aware attention to compute the local context, we also report the results with standard multi-head attention (MHA) mechanism." |
| Q115 | 11 | input_ontology | "The first set of results (i.e., SPARTA-BS or the baseline version of SPARTA) in Table 7 represents the absence of local context in SPARTA." |
| Q116 | 11 | output_form | "It yields macro and weighted F1-scores of 51.83 and 54.98 respectively with global context only." |
| Q117 | 11 | output_form | "We obtain 57.70% accuracy for the same setup." |
| Q118 | 11 | input_ontology | "Dialogue-act labels in a counseling based conversation not only depend on the abstract information of the dialogue but also on the utterances in the immediate vicinity of the current utterance." |
| Q119 | 11 | output_form | "As can be observed from Table 7, the presence of both the global and local contextual information plays an importance role in SPARTA." |
| Q120 | 11 | output_form | "Moreover, the absence of either of the component degrades the overall performance." |
| Q121 | 11 | output_form | "This corroborates that they carry distinct and diverse contextual information." |
| Q122 | 11 | output_form | "The comparison between the standard multi-head attention and the novel time-aware attention highlights the importance of attending over the relative positions of utterances." |
| Q123 | 11 | output_form | "As stated earlier, extensive experimental results show that TAA yields better performance compare to MHA for all possible configurations." |
| Q124 | 11 | output_form | "For all combinations, we observe performance drop of [3 − 4]% without the speaker information." |
| Q125 | 11 | input_ontology | "This is particularly apparent as a majority portion of the counseling conversation is driven by the therapist, thus the speaker-initiative dialogue-acts have higher relevance with the therapist utterances." |
| Q126 | 11 | output_ontology | "In earlier phases of experiments, we also considered the role of emotion in dialogue act classification." |
| Q127 | 11 | output_ontology | "We annotated a subset of our dataset with three emotion classes consisting of 'positive', 'negative' and 'neutral'." |
| Q128 | 11 | input_content | "We found that around ∼ 70% of utterances by the patients belonged to 'negative' class whereas ∼ 90% of therapists' utterances belonged to 'neutral' class." |
| Q129 | 11 | output_ontology | "Due to such imbalance, this data was not used in the final version of our proposed architecture." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7736743/ |
| WEB-2 | https://988lifeline.org/wp-content/uploads/2023/02/FINAL_988_Suicide_and_Crisis_Lifeline_Suicide_Safety_Policy_-3.pdf |
| WEB-3 | https://ismg-cdn.nyc3.cdn.digitaloceanspaces.com/asset_files/external/hhs-ocr-dear-colleagues-letter-re-ai-non-discrimination-1-10-25.pdf |
| WEB-4 | https://compliancehub.wiki/digital-therapy-compliance-hipaa-42-cfr-part-2-ftc-2026-mental-health-data/ |
| WEB-5 | https://pmhscribe.com/us-ai-regulation/ |
| WEB-6 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12022849/ |
| WEB-7 | https://www.indiacode.nic.in/handle/123456789/2249?locale=en |
| WEB-8 | https://journals.sagepub.com/doi/10.1177/02537176251370651 |
| WEB-9 | https://iclg.com/practice-areas/digital-health-laws-and-regulations/india |
| WEB-10 | https://nimhans.co.in/wp-content/uploads/2021/09/Telepsychiatry-Operational-Guidelines-2020.pdf |
| WEB-11 | https://indianpsychiatricsociety.org/e-book-telepsychiatry-operational-guidelines-2020/ |
| WEB-12 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8554922/ |
| WEB-13 | https://www.helpguide.org/mental-health/treatment/best-online-therapy |
| WEB-14 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12185383/ |
| WEB-15 | https://www.talktoangel.com/blog/best-mental-health-counselling-platform-in-india-and-the-world |
| WEB-16 | https://cmhlp.org/imho/blog/indias-digital-mental-health-landscape-government-initiatives-and-challenges/ |
| WEB-17 | https://scroll.in/article/1085095/as-young-indians-turn-to-ai-therapists-how-confidential-is-their-data |
| WEB-18 | https://aclanthology.org/2021.acl-long.269/ |
| WEB-19 | https://github.com/behavioral-data/Empathy-Mental-Health |
| WEB-20 | https://www.crisistextline.org/data-philosophy/research-impact/ |
| WEB-21 | https://aclanthology.org/2022.acl-long.104 |

---

