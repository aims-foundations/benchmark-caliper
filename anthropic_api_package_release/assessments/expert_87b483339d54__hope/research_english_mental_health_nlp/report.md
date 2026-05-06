## Deployment Context

**Use case:** An NLP/AI researcher uses the HOPE benchmark dataset to evaluate and improve dialogue-understanding for AI-assistive chatbots. The benchmark provides a evaluation protocol across 12 dialogue act categories in counseling conversations.
**Target population:** NLP/AI researchers in English speaking countries or willing to work with English data working on computational approaches to mental health, dialogue systems, and psycholinguistics. This includes PhD students, postdoctoral researchers, and industry practitioners building LLM-based systems for clinical NLP and digital mental health applications serving underrepresented regional communities.

# Validity Analysis: hope_dac
**Target context:** Global NLP/AI Research Community — Computational Mental Health (HOPE Benchmark Assessment)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ✓ | 3 | Moderate gaps | medium |
| Input Content ⚠ | 2 | Significant gaps | high |
| Input Form ✓ | 4 | Minor gaps | high |
| Output Ontology | 3 | Moderate gaps | high |
| Output Content ⚠ | 2 | Significant gaps | high |
| Output Form | 3 | Moderate gaps | high |
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

HOPE provides a methodologically careful, transparent benchmark for dialogue-act classification in dyadic individual counseling — its task framing [Q7–Q9, Q22], 12-label scheme developed with expert consultation [Q27], substantial inter-annotator agreement [Q49], and statistically significant SPARTA results [Q88] make it a reasonable starting point for the elicited use case of evaluating chatbots in individual counseling-style conversations. The strongest validity dimensions are Input Form (text-only English matches deployment exactly) and Input Ontology (well-scoped task framing for individual dyadic counseling). The most significant validity concerns are concentrated in the two HIGH-priority dimensions: Input Content (sessions are explicitly US-clinical [Q98] while downstream chatbots target South Asian, African American, and Latino communities whose communicative norms diverge in well-documented ways [WEB-5, WEB-9, WEB-11]) and Output Content (annotator cultural backgrounds undocumented [Q50], no label-stratified IAA, RoBERTa backbone inherits documented AAVE bias [WEB-8, WEB-9]). The Output Ontology and Output Form dimensions show acknowledged but unresolved limitations — single-label assignment [Q30] mismatches multi-intent reality (per elicitation A3), and no subgroup-disaggregated metrics are reported, which conflicts with emerging FDA equity expectations [WEB-20]. Many of these gaps are field-wide rather than HOPE-specific [WEB-17], but they materially limit the benchmark's external validity for the target downstream populations.

## Practical Guidance

### What This Benchmark Measures

HOPE measures a model's ability to assign one of 12 counseling-domain dialogue-act labels [Q22] to utterances in dyadic individual-counseling text transcripts [Q26], with strongest signal on speaker-initiative questions and clear delivery acts and weakest signal on Acknowledgment [Q77] and on the speaker-initiative/responsive complementary pairs [Q51, Q91]. It is best suited to comparing dialogue-aware architectures' ability to model local context, global context, and speaker dynamics on US-clinical English counseling conversations — the Input Ontology and Input Form dimensions support this well.

### Construct Depth

The benchmark probes the dialogue-act classification construct moderately deeply on US-clinical English material — with hierarchical taxonomy design [Q29, Q32], expert-consulted label definitions [Q27], substantial annotator agreement [Q49], proper statistical testing [Q88], and ablations that disentangle local/global context and speaker-awareness contributions [Q115]. However, depth is constrained on the Output Content and Input Content dimensions: it does not probe whether the construct generalizes across cultural communicative norms, does not test multi-intent labeling [Q30], and provides no subgroup-disaggregated evidence for the populations the downstream chatbots are intended to serve.

### What Else You Need

For valid use in evaluating chatbots targeting South Asian, African American, and Latino communities, supplementation is required across IC, OC, OO, and OF: (1) re-annotation or fresh annotation of a held-out evaluation sample by representative regional annotators (addresses OC); (2) collection or curation of supplementary counseling conversation samples from target communities (addresses IC); (3) multi-label or ranked-output evaluation protocols built on top of HOPE single-label predictions (addresses OO and OF, supports A3); (4) subgroup-disaggregated performance reporting consistent with emerging FDA equity expectations [WEB-20]; (5) AAVE-specific bias audits given RoBERTa backbone bias evidence [WEB-8, WEB-9]. AnnoMI [WEB-15] provides a methodological model for richer annotator documentation. As of May 2025 no culturally adapted counseling DA benchmark exists [WEB-23] to substitute for HOPE — supplementation rather than replacement is the realistic path.

## Dimension Details

### Input Ontology — 3/5 (Moderate gaps)

**Confidence:** medium

**Justification:**
HOPE's task taxonomy targets dialogue-act classification in dyadic counseling, explicitly distinguished from goal-oriented and chit-chat dialogue [Q7, Q8, Q9], with the well-defined objective of assigning one DAC label per utterance [Q22, Q58]. For the elicited use case — individual counseling-style chatbot conversations — this coverage is appropriate, and the elicitation explicitly affirms that 'individual counseling-style conversations' are well covered. However, the taxonomy is restricted to individual dyadic sessions [Q26], with no sub-task disaggregation for group therapy, crisis intervention, or culturally adapted modalities (e.g., spiritually grounded counseling, collectivist distress framing). The elicitation marks IO as MODERATE priority and treats cultural adaptation as deferred future work, so this is a known but accepted gap rather than a fundamental misalignment. The baseline architecture comparison and ablations [Q79, Q80, Q115] cover utterance, local context, global context, and speaker-awareness signals, which is structurally appropriate for the construct.

**Strengths:**
- Task framing explicitly recognizes counseling dialogue as distinct from goal-oriented and chit-chat conversations [Q7, Q8, Q9], avoiding category misalignment with general-purpose DA schemes.
- Ablation design [Q115, Q118, Q125] systematically tests local context, global context, and speaker awareness — structurally relevant signals for counseling DAC.
- Coverage of individual dyadic CBT-compatible modalities aligns with the elicited primary use case (Q1/A1).

**Checklist:**

- **IO-1**: For the target context, required categories are dialogue-act types in individual counseling dyads — covered by HOPE's framing [Q22, Q58]. Culturally adapted modality categories (e.g., spiritually grounded counseling, community healing frameworks) would also be relevant for downstream chatbot deployment per the regional context, but are explicitly out of scope. — _Sources: Q22, Q58_
- **IO-2**: Yes — the taxonomy omits sub-categories for crisis intervention, group therapy, motivational interviewing as a distinct modality, and culturally adapted therapeutic frameworks. The elicitation (A1) treats this as deferred future work rather than a current failure. No published culturally adapted DA taxonomy for counseling NLP exists [WEB-23], confirming this is a field-wide gap. — _Sources: Q26, WEB-23, WEB-15_
- **IO-3**: No clearly irrelevant categories identified for the target context. The 12 DA categories [Q33–Q44] are general communicative-intent labels that plausibly apply across counseling sub-types. — _Sources: Q33, Q44_
- **IO-4**: Documented gap: absence of culturally adapted counseling modality categories [WEB-23] and absence of crisis/group sub-task disaggregation. INSUFFICIENT DOCUMENTATION on per-modality session counts within HOPE — would need session-level metadata tagging therapy sub-type. — _Sources: WEB-23_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q7] 'Unlike general goal-oriented dialogues, a conversation between a patient and a therapist is considerably implicit, though the objective of the conversation is quite apparent.' (p.1)
- [Q22] 'we annotated ∼ 12.9𝐾 utterances with 12 dialogue-act labels carefully designed to cater to the requirements of a counseling session.' (p.3)
- [Q26] 'all of them are dyadic conversations only.' (p.3)
- [Q79] 'we categorize the baselines into three groups – utterance-driven, utterance+global context driven, and utterance + global context + speaker-aware driven.' (p.7)
- [Q118] 'Dialogue-act labels in a counseling based conversation not only depend on the abstract information of the dialogue but also on the utterances in the immediate vicinity of the current utterance.' (p.11)

*Web sources:*
- [WEB-23] JMIR Mental Health (2025) confirms most LLM mental health studies have 'limited attention to linguistic or cultural adaptation'
- [WEB-15] AnnoMI uses MI-specific behavior codes — demonstrates alternative taxonomic framings exist for counseling NLP

</details>

**Information gaps:**
- Per-modality session counts (CBT vs. child vs. family vs. substance use) within HOPE are not documented in retrievable sources.
- No empirical evidence of how the taxonomy performs across counseling sub-types.

**Requires expert verification:**
- Whether the 12-label scheme adequately captures dialogue acts in crisis intervention or culturally adapted therapeutic sessions — would require clinical and cross-cultural psychology expert review.

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Input content is sourced from 212 publicly available YouTube counseling videos [Q3, Q13, Q23], and the paper explicitly states that 'the majority of the sessions in HOPE belong to the mental health professionals and patients based in United States' [Q98], with explicit acknowledgment that 'the effectiveness of SPARTA on data from other geographical or demographical regions may vary' [Q99]. The elicitation marks IC as HIGH priority precisely because the downstream chatbot deployment targets South Asian, African American, and Latin American communities whose communicative norms diverge from US clinical baseline (indirect disclosure, somatic idioms, AAVE pragmatics, familismo, personalismo). No participant demographic metadata is documented — gap_id 6 confirmed [WEB-17]. Latino adults are 28% less likely than US adults overall to receive mental health treatment [WEB-11], and Asian Americans utilize services at roughly half the general-population rate [WEB-5] — meaning the populations the chatbot targets are precisely those least represented in HOPE's source content. AAVE-related transformer bias is documented in the literature backbone (RoBERTa) [WEB-8, WEB-9]. Utterance length distributions (~103/124 words) [Q56, Q57] further diverge from short-turn chatbot deployment patterns. Construct-irrelevant variance risk is high.

**Strengths:**
- Authors explicitly disclose US-centric source population and warn about geographic/demographic generalization limits [Q98, Q99] — meeting transparency norms even if substantive coverage is limited.
- Confidentiality protections (synthetic name assignment) [Q24, Q97] are documented.
- Sample size of ~12.9K utterances across 212 sessions [Q13, Q53] provides reasonable statistical power for the represented population.

**Checklist:**

- **IC-1**: Yes — appropriate interpretation of utterances frequently requires US clinical-cultural background knowledge (e.g., implicit individualist distress framing, secular/Protestant therapeutic register). The regional context documents that South Asian, African American, and Latino communicative norms differ materially from this baseline. — _Sources: Q98, WEB-5, WEB-11_
- **IC-2**: Substantially misaligned for the downstream populations the chatbot is intended to serve. The benchmark content is grounded in US mainstream clinical culture [Q98]; downstream users include communities with distinct communicative norms (familismo, personalismo, AAVE, indirect disclosure) per the regional context. — _Sources: Q98, Q99, WEB-9_
- **IC-3**: Yes — sessions implicitly encode US clinical CBT-compatible discourse norms. Spiritual/religious coping language, code-switching, narrative-style disclosure, and call-and-response patterns characteristic of target downstream communities are not represented in HOPE's source material per the regional context's documented norm divergences. — _Sources: Q98, WEB-8, WEB-9_
- **IC-4**: INSUFFICIENT DOCUMENTATION — no information on whether regional annotators were recruited or whether culturally sensitive instances were flagged. A field-wide gap: only 39.2% of NLP-MHI studies report demographic information [WEB-17]. — _Sources: WEB-17_
- **IC-5**: Documented content issues: (a) US-only session origin [Q98]; (b) no participant demographic metadata [WEB-17]; (c) lengthy utterances (~103/124 words) [Q56, Q57] mismatched with short-turn chatbot deployment; (d) RoBERTa backbone [Q61] inherits documented AAVE bias [WEB-8, WEB-9]. — _Sources: Q98, Q56, Q57, Q61, WEB-8, WEB-9, WEB-17_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q98] 'the majority of the sessions in HOPE belong to the mental health professionals and patients based in United States.' (p.8)
- [Q99] 'Hence, the effectiveness of SPARTA on data from other geographical or demographical regions may vary.' (p.8)
- [Q23] 'One of major hurdles we faced in the process of data collection was the unavailability of public counseling sessions...we carefully explored the web and collected publicly-available pre-recorded counselling videos on YouTube.' (p.3)
- [Q56] 'the dialogue sessions in HOPE are usually lengthy (∼ 59 utterances per session).' (p.5)
- [Q57] 'the average length of utterance of a patient being 103 words, whereas for therapist, it is ∼ 124 words.' (p.5)

*Web sources:*
- [WEB-17] Translational Psychiatry (2023) systematic review: only 40 of 102 NLP-MHI studies report patient demographic information
- [WEB-11] HHS Office of Minority Health: Latino adults 28% less likely than US adults overall to receive mental health treatment in 2024
- [WEB-5] PMC review: only 9% of Asian Americans utilized mental health services vs. 18% of general US population
- [WEB-8] ResearchGate study quantifying AAVE bias in transformer-based language models (including RoBERTa)
- [WEB-9] npj Digital Medicine (2025): LLMs provide differential treatment recommendations when AAVE dialect cues indicate patient race

</details>

**Information gaps:**
- Participant demographic composition (race, ethnicity, SES, age) of HOPE sessions is not documented.
- No empirical performance disaggregation by community subgroup exists [WEB-17].
- Therapy-type breakdown of the 212 sessions is not documented.

**Requires expert verification:**
- A regional clinical/cultural expert review of sample HOPE transcripts to identify cultural register signals and assess construct-irrelevant variance for South Asian, African American, and Latino downstream communities.

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
Input form is text-only English derived from speech via OTTER ASR with manual correction [Q25], with names systematically masked [Q97]. The benchmark language matches the deployment modality exactly (text-only English chatbot evaluation), with no script or primary-modality mismatch — the regional context marks IF as LOWER priority. Standard ML compute infrastructure (Tesla V100, 32GB GPU, PyTorch, HuggingFace) [Q108, Q64] is accessible for the global researcher cohort. The only meaningful concern is that the speech-to-text transfer 'causes some information loss' [Q94], removing prosodic and paralinguistic cues that may carry communicative-intent signal in counseling — but this is acknowledged. Utterance length distribution (~103/124 words) [Q56, Q57] is a mild form-distribution mismatch with short-turn chatbot deployment, though this is more of a content-distribution issue than a signal-encoding issue.

**Strengths:**
- Text-only English form matches deployment modality exactly — no script mismatch, no infrastructure barriers for the researcher population.
- ASR transcription errors were hand-corrected for spelling and grammar [Q25], reducing surface-level noise.
- Compute requirements (Tesla V100, 32GB) [Q108] are accessible via standard cloud GPU providers.
- Authors acknowledge the speech-to-text information loss limitation transparently [Q94].

**Checklist:**

- **IF-1**: Signal distribution match is good for text-only chatbot deployment. The original modality was speech, and the speech-to-text transfer causes acknowledged information loss [Q94] — but downstream deployment is also text-only, so this loss is consistent across train and deployment. — _Sources: Q25, Q94_
- **IF-2**: Yes — researcher infrastructure (cloud GPU, GitHub, HuggingFace) supports the form requirements [Q64, Q107, Q108]. No regional infrastructure constraints apply. — _Sources: Q64, Q107, Q108, WEB-14_
- **IF-3**: Domain-specific form difference: HOPE's lengthy utterances (~103/124 words avg.) [Q56, Q57] are atypical of short-turn text chatbot interactions. This is documented but not framed as a formal limitation in the paper. — _Sources: Q56, Q57_
- **IF-4**: Form mismatches are minor: (a) speech-derived rather than natively-typed text [Q25, Q94]; (b) utterance length distribution mismatch with chatbot turn length [Q56, Q57]. Neither rises to the level of a script or modality violation. — _Sources: Q25, Q94, Q56, Q57_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q25] 'we extract the transcriptions of each video using OTTER...an automatic speech recognition tool. Subsequently, we correct transcription errors to remove any noise.' (p.3)
- [Q94] 'The automatic transfer of utterance from the speech modality to the text causes some information loss, though we tried our best to recover them through manual intervention.' (p.8)
- [Q97] 'The names of the patients and therapists involved in these sessions have been systematically masked.' (p.8)
- [Q108] 'GPU: TeslaV100, Memory: 32GB, Linux 64 Bit: Ubuntu 18.04 LTS' (p.10)
- [Q56] 'the dialogue sessions in HOPE are usually lengthy (∼ 59 utterances per session).' (p.5)

*Web sources:*
- [WEB-14] HOPE paper documents Tesla V100 / 32GB / Ubuntu 18.04 training environment — accessible via standard cloud GPU providers

</details>

**Information gaps:**
- ASR error rate per session is not documented, so residual transcription noise after manual correction is unquantified.

---

### Output Ontology — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
The 12-label DA taxonomy [Q2, Q14, Q17] was developed in consultation with therapist and counseling experts [Q27], explicitly distinguished from general schemes (Switchboard) on domain specificity grounds [Q27], and organized hierarchically [Q29, Q32]. For the elicited use case, the elicitation (A2) affirms that 'the dialogue-act taxonomy is designed to capture intent and conversational flow in a way that is generally applicable across settings' and treats the taxonomy as useful for guiding chatbot dialogue trajectory. However, three structural concerns remain: (1) Single-label assignment is acknowledged by the authors to be a simplification — 'sometimes, an utterance can have multiple dialog-acts' [Q30] — and the elicitation (A3) confirms this is a real concern for downstream chatbot use; (2) The authors themselves note that speaker-initiative/responsive label pairs 'seem complementary in nature' [Q51] with confirmed systematic confusion in error analysis (OD:ID 43%, ID:ACK 28%, YNQ:IRQ 26%) [Q91, Q92]; (3) The taxonomy is grounded in US clinical practice [Q98] and may systematically misclassify communicative acts prevalent in target downstream communities (call-and-response → potentially miscoded as ACK or GC; personalismo opening → possibly GT/GC instead of therapeutically functional rapport-building; spiritual coping → possibly OD or GC). No multi-label counseling DA benchmark currently exists [WEB-15, WEB-18], and no culturally adapted DA taxonomy has been identified [WEB-23], so HOPE is not exceptional but the gap is real.

**Strengths:**
- Taxonomy was developed with therapist and counseling expert consultation [Q27], grounding it in domain knowledge.
- Hierarchical organization (initiative/responsive/general) [Q29, Q32] provides a coherent structural framing.
- Explicit differentiation from general-purpose DA schemes [Q27] addresses domain specificity.
- Authors transparently flag the multi-label simplification [Q30] and label-pair complementarity [Q51], enabling informed downstream interpretation.

**Checklist:**

- **OO-1**: The 12 labels [Q33–Q44] are plausibly relevant to general counseling dialogue. For the elicited individual-counseling-chatbot use case (A2), the taxonomy is treated as generally applicable. — _Sources: Q27, Q33, Q44_
- **OO-2**: Missing categories of concern: no labels for spiritually framed coping, narrative-style extended disclosure, indirect disclosure via family narrative, or call-and-response acknowledgment patterns — all flagged in regional context as therapeutically functional in target downstream communities. No published culturally adapted counseling DA taxonomy exists [WEB-23]. — _Sources: WEB-23, WEB-15_
- **OO-3**: The taxonomy implicitly encodes US clinical assumptions [Q98] — e.g., GC ('General Chit-Chat...possibly because of the vagueness and the lack of sense in the context') [Q44] is a residual category that risks absorbing therapeutically functional culture-specific moves (personalismo rapport-building, spiritual framing) per the regional context. — _Sources: Q44, Q98_
- **OO-4**: Stakeholder-driven taxonomy redesign would be appropriate for culturally adapted deployment, per the elicitation A2 framing this as 'complementary/future work.' No such redesign has been undertaken in the field [WEB-23]. — _Sources: WEB-23_
- **OO-5**: Documented taxonomy issues: (a) single-label simplification [Q30] mismatches multi-intent reality [A3]; (b) US-clinical grounding [Q98] risks structural misalignment for target downstream communities; (c) confirmed systematic confusion among complementary label pairs [Q51, Q91, Q92]; (d) ACK is a weak point (F1=47.86%) [Q77] with documented confusion with ID. — _Sources: Q30, Q51, Q91, Q77, Q98_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q27] 'we, in consultation with therapist and counselling experts, design a set of 12 dialog-act labels that are arranged in a hierarchy.' (p.3)
- [Q30] 'Sometimes, an utterance can have multiple dialog-acts; however, they are rare in the annotated dataset. Hence, for simplicity, we consider only one (primary) label for each utterance.' (p.3)
- [Q51] 'The broad definitions of speaker-initiative and speaker-responsive dialogue-act label pairs, IRQ & ID; ORQ & OD, and CRQ & CD, seem complementary in nature.' (p.4)
- [Q91] 'We observe three pairs with significant error-rates (≥ 25%) – YNQ:IRQ (26%), OD:ID (43%), ID:ACK (28%).' (p.7)
- [Q44] 'General Chit-Chat (GC): Other utterances that do not belong to any of the above labels are tagged as GC, possibly because of the vagueness and the lack of sense in the context of the conversation.' (p.4)

*Web sources:*
- [WEB-23] JMIR Mental Health (2025) confirms 'limited attention to linguistic or cultural adaptation' in LLM mental health studies
- [WEB-15] AnnoMI uses MI-specific behavior codes; no multi-label counseling DA benchmark identified
- [WEB-18] Scientific Reports (2025): MultiWD covers multi-label wellness dimensions but for social media, not counseling dialogue acts

</details>

**Information gaps:**
- Whether expert consultants who helped design the taxonomy [Q27] included clinicians experienced with target downstream communities is not documented.

**Requires expert verification:**
- Cross-cultural counseling experts should review the 12 labels for whether they adequately partition the DA space for target downstream communities, particularly regarding GC, ACK, GT, and ID boundaries.

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Three expert linguists annotated the corpus [Q45], operating from a hierarchical scheme developed with mental health professional and linguist consultation [Q16, Q95], with calibration phase [Q46] and expert-therapist-moderated discussion [Q47]. Aggregate Cohen's Kappa is 0.7234 ('substantial') [Q48, Q49]. The authors transparently acknowledge that 'the annotator's bias cannot be ruled out completely' [Q96]. However, multiple critical gaps remain for the elicited HIGH-priority use case: (1) Annotator cultural backgrounds, native languages, and exposure to target downstream communities are entirely undocumented — the only reported demographics are age 25–35 and 2–10 years professional experience [Q50]; (2) No label-stratified IAA scores are reported, masking whether agreement varies on culturally loaded labels (GC, ACK, GT, ID); (3) The institutional affiliations (BITS Pilani, MAIT Delhi, IIIT-Delhi) [Q12] suggest annotators are likely South Asian by background — itself a confound when annotating US-clinical content for downstream targeting of US underrepresented communities; (4) Empirical evidence shows LLMs and transformer models (including RoBERTa, HOPE's backbone) exhibit racial and dialectal bias in clinical contexts [WEB-8, WEB-9], grounding the OC concern empirically. AnnoMI [WEB-15] demonstrates that richer annotator documentation is achievable in this field, making HOPE's gap a methodological choice rather than a constraint.

**Strengths:**
- Substantial aggregate inter-annotator agreement (κ=0.7234) [Q49] indicates reasonable annotator consistency on the labels overall.
- Multi-stage annotation process with calibration [Q46] and expert-therapist-moderated discussion [Q47] follows good annotation methodology practice.
- Mental health professionals and linguists were consulted in guideline preparation [Q95].
- Authors transparently acknowledge that annotator bias cannot be ruled out [Q96] and that downstream effectiveness 'may vary' across regions [Q99].

**Checklist:**

- **OC-1**: Substantially misaligned for target downstream communities. Ground truth labels reflect annotators applying a US-clinical-derived scheme [Q98] without documented exposure to or grounding in target communities' communicative norms. — _Sources: Q98, Q50_
- **OC-2**: High potential for disagreement on culturally loaded utterances. Regional context documents that AAVE pragmatics, familismo opening, spiritual coping language, and indirect disclosure narratives are likely to be misclassified as GC, GT, OD, or ID by US-clinical-trained annotators. No empirical disagreement test exists [WEB-17]. — _Sources: Q98, WEB-9, WEB-17_
- **OC-3**: Annotator demographics are partially documented (age 25–35, 2–10 years experience [Q50]) but cultural background, native language, exposure to minority US clinical populations, and institutional clinical training are NOT DOCUMENTED — would need a Datasheet-style annotator demographics table. — _Sources: Q50, Q12_
- **OC-4**: Re-annotation by a representative regional pool is appropriate for high-stakes downstream deployment. The elicitation (A2) frames this as complementary work. AnnoMI's 10-annotator design with post-annotation survey [WEB-15] demonstrates feasibility. — _Sources: WEB-15_
- **OC-5**: Aggregation: only aggregate κ is reported [Q48, Q49]. No per-label IAA, no minority-perspective preservation mechanism documented. INSUFFICIENT DOCUMENTATION on whether disagreements were resolved by majority vote, expert moderator decision, or other mechanism beyond the qualitative 'group discussion' description [Q47]. — _Sources: Q47, Q48, Q49_
- **OC-6**: Documented label issues threatening convergent and external validity: (a) annotator cultural backgrounds undocumented; (b) no label-stratified IAA; (c) RoBERTa backbone [Q61] inherits AAVE bias [WEB-8]; (d) field-wide evidence that LLMs are more racially biased in mental health contexts than other domains [WEB-9, WEB-22]; (e) acknowledged residual annotator bias [Q96]. — _Sources: Q96, Q61, WEB-8, WEB-9, WEB-22_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q45] 'We employed three annotators who are experts in linguistics.' (p.4)
- [Q49] 'We obtain the inter-rater agreement score of 0.7234 – which falls under the "substantial" category.' (p.4)
- [Q50] 'Annotators are in the age group of 25-35, with 2-10 years of professional experience.' (p.4)
- [Q96] 'However, the annotator's bias cannot be ruled out completely.' (p.8)
- [Q47] 'every annotation was discussed in the presence of the annotators and an expert therapist as moderator to ensure consistency.' (p.4)
- [Q12] 'BITS Pilani, Goa, India, Maharaja Agrasen Institute of Technology, New Delhi, India, IIIT-Delhi, India.' (p.1)

*Web sources:*
- [WEB-9] npj Digital Medicine (2025): LLMs more racially biased in mental health than other health domains; AAVE dialect cues trigger inferior treatment recommendations
- [WEB-8] ResearchGate: RoBERTa shows complex bias toward AAVE in masked language modeling — bias inherited by SPARTA
- [WEB-15] AnnoMI uses 10 annotators with post-annotation survey, demonstrating richer annotator documentation is achievable
- [WEB-17] Translational Psychiatry (2023): only 4 of 102 NLP-MHI studies used external validation; demographic reporting is rare field-wide
- [WEB-22] PMC (2024): documented racial bias in clinical LLMs

</details>

**Information gaps:**
- Annotator cultural background, native language, race/ethnicity, and clinical exposure to target downstream communities.
- Label-stratified Cohen's Kappa scores.
- Disagreement resolution protocol beyond qualitative group discussion.
- Background of the moderating expert therapist.

**Requires expert verification:**
- Re-annotation of a sample of HOPE utterances by annotators representative of South Asian, African American, and Latino communities to empirically test for systematic divergence in label assignment.

---

### Output Form — 3/5 (Moderate gaps)

**Confidence:** high

**Justification:**
Performance is reported via macro-F1, weighted-F1, and accuracy [Q63], with label-wise F1 [Q76] and 3-fold cross-validation [Q87]. SPARTA-TAA achieves 60.29 macro-F1 / 64.53 weighted-F1 / 64.75% accuracy [Q73, Q85] with statistical significance vs. CASA [Q88]. Strengths include label-wise reporting that surfaces ACK weakness (F1=47.86%) [Q77] and proper statistical testing. However, the OF dimension (MODERATE priority) faces a confirmed mismatch: evaluation is single-label classification only [Q63], while the elicited downstream chatbot use case benefits from multi-label or ranked outputs (A3 explicitly confirms 'multi-label or ranked outputs would yield more contextually appropriate downstream responses'). The benchmark itself acknowledges multi-intent utterances [Q30] but defers the form change as future work. The emotion annotation experiment was abandoned due to imbalance [Q126–Q129], leaving no affective dimension in the output form. No subgroup-disaggregated performance metrics are reported, which becomes a regulatory issue under emerging FDA equity expectations [WEB-20, WEB-27]. Confusion analysis [Q90, Q91, Q92] is reported but not disaggregated by speaker role or cultural subgroup.

**Strengths:**
- Label-wise F1 reporting [Q76, Q77] surfaces uneven benchmark signal across DA categories.
- Statistical significance testing with t-tests at >95% confidence [Q88] follows good methodological practice.
- 3-fold cross-validation results consistent with primary split [Q87] indicates result stability.
- Confusion matrix analysis [Q90, Q91, Q92] provides interpretable error structure information.

**Checklist:**

- **OF-1**: Output modality is single categorical label per utterance [Q63]. The elicited downstream chatbot use case benefits from multi-label or ranked outputs (A3) — this is a documented mismatch. — _Sources: Q63, Q30_
- **OF-2**: Not applicable — the use case is text-only, no TTS requirement applies.
- **OF-3**: Not applicable — the user population is researchers (English-proficient), not literacy-constrained end users. Downstream chatbot literacy concerns are out of scope per the regional context's IF=LOWER framing.
- **OF-4**: Documented form mismatches: (a) single-label vs. multi-label/ranked output need [Q30, Q63, A3]; (b) no affective dimension after emotion annotation was abandoned [Q129]; (c) no subgroup-disaggregated metrics, which conflicts with emerging FDA equity expectations [WEB-20, WEB-27]; (d) macro-F1 weights all classes equally despite label imbalance and may obscure systematic culture-related failures. — _Sources: Q30, Q63, Q129, WEB-20, WEB-27_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q63] 'we compute macro-F1, weighted-F1, and accuracy scores.' (p.6)
- [Q73] 'The SPARTA-TAA system obtains the best scores of 60.29 macro-F1, 64.53 weighted-F1' (p.6)
- [Q77] 'SPARTA consistently yields good scores for the majority of the dialogue-acts, except for the Acknowledgement (ACK) where it records F1-score of merely 47.86%.' (p.7)
- [Q88] 'our results are significant with > 95% confidence across macro-F1 (p-value= 0.009), weighted-F1 (p-value= 0.014), and accuracy (p-value= 0.048).' (p.7)
- [Q129] 'Due to such imbalance, this data was not used in the final version of our proposed architecture.' (p.11)

*Web sources:*
- [WEB-20] Orrick (Nov 2025): FDA DHAC signals sponsors will need 'evidence of equitable performance across populations and languages' for AI mental health devices
- [WEB-27] FDA document on generative AI in digital mental health medical devices
- [WEB-17] Translational Psychiatry (2023): only 4 of 102 NLP-MHI studies used external validation — subgroup performance reporting is field-wide rare

</details>

**Information gaps:**
- No subgroup-disaggregated performance metrics — would require running HOPE-trained classifiers on stratified evaluation samples.

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** US-only session origin [Q98] with no participant demographic metadata creates construct-irrelevant variance for downstream chatbots targeting South Asian, African American, and Latino communities.

**Recommendation:** Augment HOPE with a held-out evaluation set drawn from counseling sessions (or carefully constructed counseling-style dialogues) representing target downstream communities, with documented participant ethnicity, language background, and therapy modality. Use this set as a subgroup-stratified evaluation sample alongside the standard HOPE test split.

### Output Content ⚠

**Gap:** Annotator cultural backgrounds and label-stratified IAA are not documented [Q50, Q49], and the RoBERTa backbone [Q61] inherits documented AAVE bias [WEB-8, WEB-9].

**Recommendation:** Run a re-annotation pilot on a sample of HOPE utterances using annotators representative of South Asian, African American, and Latino communities; compute label-stratified Cohen's Kappa and identify systematic divergences. Publish a Datasheet-style annotator demographics extension. Conduct an AAVE-specific bias audit on SPARTA following the protocols in [WEB-25].

### Output Content ⚠

**Gap:** Aggregation methods beyond qualitative 'group discussion' [Q47] for resolving annotator disagreement are not documented, risking erasure of minority annotator perspectives.

**Recommendation:** Document and report the disagreement resolution protocol explicitly; preserve and release individual annotator labels where feasible (following AnnoMI's [WEB-15] practice) to enable downstream researchers to model annotator disagreement as a signal rather than discarding it.

### Input Ontology

**Gap:** Per-modality session counts (CBT, child, family, substance use) are not documented within HOPE, preventing modality-specific validity assessment.

**Recommendation:** Publish session-level metadata tagging therapy sub-type and report performance disaggregated by sub-modality. Where coverage is thin (e.g., substance use), explicitly caveat downstream chatbot use in those modalities.

### Output Form

**Gap:** No subgroup-disaggregated performance metrics are reported, conflicting with emerging FDA equity expectations [WEB-20, WEB-27].

**Recommendation:** Adopt a reporting standard that disaggregates macro-F1, weighted-F1, and per-label F1 by speaker role and (when subgroup data are available) by demographic subgroup. Add ranked-output metrics (top-k accuracy, mean reciprocal rank) to align with multi-intent downstream needs.

### Output Ontology

**Gap:** Single-label assignment [Q30] mismatches multi-intent utterance reality (elicitation A3) and complementary label pairs show systematic confusion (OD:ID 43%, ID:ACK 28%) [Q91].

**Recommendation:** Extend HOPE annotations to support primary + secondary labels per utterance on a sample, enabling multi-label and ranked-output evaluation protocols. Report joint top-2 accuracy in addition to top-1 macro-F1 to better reflect downstream chatbot generation needs.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "We develop a novel dataset, named HOPE, to provide a platform for the dialogue-act classification in counselling conversations." |
| Q2 | 1 | output_ontology | "We identify the requirement of such conversation and propose twelve domain-specific dialogue-act (DAC) labels." |
| Q3 | 1 | input_content | "We collect ∼ 12.9𝐾 utterances from publicly-available counselling session videos on YouTube, extract their transcripts, clean, and annotate them with DAC labels." |
| Q4 | 1 | input_ontology | "Further, we propose SPARTA, a transformer-based architecture with a novel speaker- and time-aware contextual learning for the dialogue-act classification." |
| Q5 | 1 | output_form | "Our evaluation shows convincing performance over several baselines, achieving state-of-the-art on HOPE." |
| Q6 | 1 | output_form | "We also supplement our experiments with extensive empirical and qualitative analyses of SPARTA." |
| Q7 | 1 | input_ontology | "Unlike general goal-oriented dialogues, a conversation between a patient and a therapist is considerably implicit, though the objective of the conversation is quite apparent." |
| Q8 | 1 | input_ontology | "The nature of conversations in a social counselling setting is particularly distinct as compared to a conventional chit-chat or goal-oriented conversations." |
| Q9 | 1 | input_ontology | "It follows a pattern which is different from both goal-oriented and general chit-chat based conversations." |
| Q10 | 1 | input_ontology | "Usually these conversations begin with greetings followed by the therapist inquiring for problems faced by the patient." |
| Q11 | 1 | output_content | "Ganeshan Malhotra, Abdul Waheed, Aseem Srivastava, Md Shad Akhtar, Tanmoy Chakraborty." |
| Q12 | 1 | output_content | "1BITS Pilani, Goa, India, 2Maharaja Agrasen Institute of Technology, New Delhi, India, 3IIIT-Delhi, India." |
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
| Q102 | 8 | output_content | "It is important to note that we do not make any diagnostic claims." |
| Q103 | 8 | output_content | "Further, the deployment of any such technology will be done keeping in mind the safety-risks and mitigating any sources of bias that may arise." |
| Q104 | 8 | output_ontology | "We defined twelve dialogue-act labels to cater to the requirement of counselling sessions." |
| Q105 | 8 | input_content | "In total, we annotated ∼ 12.9𝑘 utterances across 212 sessions." |
| Q106 | 8 | output_content | "The authors acknowledge the support of the Ramanujan Fellowship, ihub-Anubhuti-iiitd Foundation set up under the NM-ICPS scheme of the DST, and CAI at IIIT-Delhi." |
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
| WEB-1 | https://www.thefdalawblog.com/2025/12/the-ai-chatbot-is-in/ |
| WEB-2 | https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-software-medical-device |
| WEB-3 | https://en.wikipedia.org/wiki/Asian_Americans |
| WEB-4 | https://www.census.gov/quickfacts/fact/faq/US/PST045224 |
| WEB-5 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3208524/ |
| WEB-6 | https://minorityhealth.hhs.gov/blackafrican-american-health |
| WEB-7 | https://www.statista.com/statistics/183489/population-of-the-us-by-ethnicity-since-2000/ |
| WEB-8 | https://www.researchgate.net/publication/371085866_Quantifying_the_Bias_of_Transformer-Based_Language_Models_for_African_American_English_in_Masked_Language_Modeling |
| WEB-9 | https://www.nature.com/articles/s41746-025-01746-4 |
| WEB-10 | https://www.census.gov/newsroom/press-releases/2024/population-estimates-characteristics.html |
| WEB-11 | https://minorityhealth.hhs.gov/mental-and-behavioral-health-hispaniclatinos |
| WEB-12 | https://unidosus.org/blog/2024/03/23/rompiendo-barreras-dismantling-barriers-to-latino-mental-health-care/ |
| WEB-13 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3756540/ |
| WEB-14 | https://arxiv.org/abs/2204.09361 |
| WEB-15 | https://www.mdpi.com/1999-5903/15/3/110 |
| WEB-16 | https://github.com/uccollab/AnnoMI |
| WEB-17 | https://www.nature.com/articles/s41398-023-02592-2 |
| WEB-18 | https://www.nature.com/articles/s41598-025-30873-x |
| WEB-19 | https://bipartisanpolicy.org/issue-brief/fda-oversight-understanding-the-regulation-of-health-ai-tools/ |
| WEB-20 | https://www.orrick.com/en/Insights/2025/11/FDAs-Digital-Health-Advisory-Committee-Considers-Generative-AI-Therapy-Chatbots-for-Depression |
| WEB-21 | https://arxiv.org/html/2411.10681v1 |
| WEB-22 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12137607/ |
| WEB-23 | https://mental.jmir.org/2025/1/e78410 |
| WEB-24 | https://arxiv.org/pdf/2508.07902 |
| WEB-25 | https://aclanthology.org/2023.emnlp-main.421.pdf |
| WEB-26 | https://link.springer.com/article/10.1007/s41666-025-00194-9 |
| WEB-27 | https://www.fda.gov/media/189391/download |

---

