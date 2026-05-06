```markdown
# Validity Extraction: HOPE: A Task-Oriented Dialogue-Act Classification Dataset for Mental-Health Counselling
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: HOPE: A Task-Oriented Dialogue-Act Classification Dataset for Mental-Health Counselling
- **Authors**: Ganeshan Malhotra, Abdul Waheed, Aseem Srivastava, Md Shad Akhtar, Tanmoy Chakraborty
- **Venue/Year**: Not explicitly stated in registry; inferred from content as a recent NLP/computational linguistics venue
- **Total Pages**: 11 (pages 1–11 referenced in registry)
- **Quotes Extracted**: 129

---

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

---

### 1. Task Taxonomy / Test Case Categories

The core task is dialogue-act classification (DAC) applied to mental-health counseling conversations, framed as a sequence labeling problem in which every utterance in a dyadic session is assigned one of twelve domain-specific labels [Q4, Q22]. The authors explicitly distinguish counseling dialogue from both goal-oriented and chit-chat conversation, arguing that the domain is "considerably implicit" despite having an apparent objective [Q7, Q8, Q9], and that sessions follow a recognizable structural arc beginning with greetings and moving through problem inquiry [Q10]. SPARTA, the proposed model, is evaluated against a range of baseline architectures — utterance-driven (TextVDCNN, TextRNN, RoBERTa), utterance-plus-global-context (CASA, ProSeqo, DRNN), and speaker-aware (SA-CRF) — representing progressively richer contextual representations [Q66–Q72, Q79, Q80]. The model categorizes inputs by whether they incorporate local context, global context, and speaker dynamics [Q58, Q59, Q115, Q118], which is particularly relevant because therapist-initiated acts differ systematically from patient-initiated ones [Q125].

From a deployment-validity standpoint, the taxonomy is explicitly designed for structured dyadic therapy sessions (CBT, child, family) and does not include peer support or crisis intervention exchanges. Peer support conversations — in scope for the target deployment — are characterized by informal register, shorter turns, high emotional reciprocity, and the absence of a clinical therapeutic frame, none of which are explicitly represented among the session types in HOPE [Q21, Q22]. Crisis intervention exchanges involving safety-planning probes or de-escalation moves have no clearly designated home among the twelve labels [Q2], representing a meaningful ontological gap (HIGH-priority IO dimension) for the target deployment. The baselines chosen for comparison (CASA and ProSeqo, noted as state-of-the-art on the Switchboard corpus [Q86]) also reflect a general-domain dialogue-act framing that differs substantially from the counseling-specific context, highlighting the benchmark's deliberate departure from prior task formulations [Q21].

---

### 2. Data Sources and Collection

The HOPE dataset consists of approximately 12,900 utterances drawn from 212 publicly available mental-health counseling session videos on YouTube [Q1, Q3, Q13, Q15, Q23]. Sessions are dyadic only [Q26], with utterances roughly evenly split between patients (~6,380) and therapists (~6,470) [Q54]. The authors acknowledge that the primary hurdle was the scarcity of public counseling recordings due to the sensitivity of clinical data, and that YouTube was chosen precisely because those recordings were already in the public domain [Q23]; confidentiality was further protected by assigning synthetic names to all participants [Q24]. Sessions are notably long compared to standard conversational datasets (~59 utterances per session), and individual utterances are also longer than typical (patient average: ~103 words; therapist average: ~124 words) [Q56, Q57].

A critical validity concern for the deployment context is surfaced in Q98: "the majority of the sessions in HOPE belong to the mental health professionals and patients based in United States." This means the source data carries US clinical communication norms, counselor directiveness levels, and therapeutic framing conventions that may not generalize to South Asian counseling contexts — the explicitly named secondary deployment geography. The dataset also carries a selection bias intrinsic to YouTube sourcing: sessions were pre-selected for public sharing, which may suppress the disfluencies, hesitations, and spontaneous-speech phenomena present in real-time teletherapy transcripts [Q93]. The observation that certain dialogue-act labels are "majorly associated with the patient" while others are "related to the therapist" [Q60] further suggests that the data reflects the structured asymmetry of clinical sessions, which differs from peer support settings where role asymmetry is minimal.

---

### 3. Data Format and Preprocessing

Input to the benchmark is text only, derived from automatic speech recognition (ASR) transcripts obtained via OTTER (https://www.otter.ai/), subsequently manually corrected for spelling and grammatical errors [Q25]. Patient and therapist names were systematically masked in all session text [Q97]. The dataset is split 70:20:10 for train, test, and validation [Q31, Q55, Q62], and utterance representations are extracted using a pre-trained RoBERTa model from HuggingFace Transformers [Q61, Q64, Q111]. Additional architectural details include a GRU with hidden dimension 768, a classifier sub-module with LeakyReLU activation, and a three-layer attention block [Q112, Q113]. The full system was trained on a Tesla V100 GPU with 32GB memory [Q108].

The ASR-to-text pipeline introduces a known information loss, as the authors note: "the automatic transfer of utterance from the speech modality to the text causes some information loss, though we tried our best to recover them through manual intervention" [Q94]. From an IF (Input Form) validity standpoint, both the benchmark and the target deployment operate in text modality in English, which means there is no script or modality mismatch — the LOWER-priority IF dimension is well-matched [Q105, Q111]. However, real-time teletherapy transcripts may differ from YouTube-sourced text in terms of disfluency density, false starts, and overlapping turns, since YouTube recordings are likely edited or pre-selected; this is a latent content validity concern not addressed by the preprocessing steps described. The emotion annotation experiment — which found ~70% of patient utterances coded as 'negative' and ~90% of therapist utterances as 'neutral' — was ultimately discarded due to class imbalance [Q128, Q129], indicating the dataset's affective distribution may limit certain downstream analyses.

---

### 4. Label Categories and Output Types

The output label set comprises twelve dialogue-act labels organized in a three-tier hierarchy: speaker-initiative (three labels), speaker-responsive (three labels), and general (four labels, plus two overlapping pairs) [Q2, Q17, Q29, Q32]. The full set is: Information Request (IRQ), Yes/No Question (YNQ), Opinion Request (ORQ), Clarification Delivery (CD), Information Delivery (ID), Clarification Request (CRQ), Positive Answer (PA), Negative Answer (NA), Opinion Delivery (OD), Greeting (GT), Acknowledgment (ACK), and General Chit-Chat (GC) [Q33–Q44]. Labels were designed in consultation with therapist and counseling experts [Q27] to "capture the intents of both the patient and therapist" and to be "easily comprehensible to assist in the development of a conversational dialogue system" [Q28]. The GC category acts as a catch-all for utterances that do not fit any other label [Q44], and each utterance receives exactly one (primary) label [Q30].

From a deployment-validity perspective (MODERATE-priority OO dimension), the twelve-label ontology is appropriate for tracking conversational flow and trajectory in structured dyadic therapy, but may be overloaded or ambiguous when applied to peer support or crisis contexts. For example, peer support interactions may contain high volumes of emotional acknowledgment that the current ACK label partially captures but does not fully differentiate from empathic reflection or validation moves. Crisis-specific communicative acts such as safety-planning probes, risk assessment questions, or de-escalation responses lack dedicated labels and would likely be forced into IRQ, YNQ, or GC — introducing systematic label boundary ambiguity. The emotion annotation pilot [Q126, Q127] suggests the authors recognized affective dimensions of counseling dialogue but chose not to incorporate them in the final label set, which is relevant for downstream session quality assessment where emotional tone is a key signal. The label set was explicitly defined to be "aligned with mental-health counseling session" [Q104], reinforcing that its scope is clinical-therapeutic rather than peer-support or crisis-specific.

---

### 5. Annotation Process

Three annotators with expertise in linguistics performed the DAC labeling, supported by a novel hierarchical annotation scheme prepared specifically for counseling conversations [Q16, Q45]. Prior to full annotation, annotators completed a calibration exercise on a dataset sample, followed by consensus discussions moderated by an expert therapist to ensure scheme consistency [Q46, Q47]. Mental-health professionals and linguists were additionally consulted during guideline preparation [Q95]. Annotators ranged in age from 25 to 35 with 2–10 years of professional experience [Q50].

From a cross-cultural and deployment-validity standpoint (MODERATE-priority OC dimension), the annotation team is described only in terms of linguistic expertise and age/experience range — no geographic origin, cultural background, or clinical affiliation beyond "expert therapist moderator" is specified. Given that the sessions themselves are predominantly US-based [Q98], there is no evidence that South Asian clinicians, peer-support practitioners, or crisis workers participated in annotation, which means South Asian communicative norms and peer-support-specific label-boundary judgments are unrepresented in the ground-truth construction. The authors acknowledge that "annotator bias cannot be ruled out completely" [Q96], but do not detail how such bias might interact with cultural or session-type variability. The inter-annotator agreement of Cohen's Kappa = 0.7234 ('substantial') is reported as a single aggregate figure [Q48, Q49] — no breakdown by session type (CBT vs. child vs. family) or by label category is provided, making it impossible to assess whether agreement is lower for ambiguous or catch-all labels like GC or ACK, which are the labels most likely to be overloaded in peer support settings.

---

### 6. Evaluation Metrics and Output Modality

SPARTA and all baselines are evaluated using macro-F1, weighted-F1, and accuracy [Q63], with statistical significance assessed via T-test (>95% confidence across all three metrics comparing SPARTA-TAA to the best baseline, CASA) [Q88]. The best configuration, SPARTA-TAA, achieves macro-F1 of 60.29, weighted-F1 of 64.53, and accuracy of 64.75% — improvements of +8.64%, +8.58%, and +6.29% over CASA [Q73, Q85]. Results are validated via 3-fold cross-validation and are consistent with the train-val-test split [Q87]. Ablation studies cover each component of SPARTA (local context, global context, speaker-awareness) [Q19, Q74, Q119, Q122, Q123, Q124], and label-wise F1 is also reported [Q76], revealing that ACK is the weakest-performing label at 47.86% [Q77] while under-represented labels (ORQ, NA, PA) still achieve F1 scores in the 55–65% range [Q78].

The choice of macro-F1 as a primary metric is appropriate for an imbalanced label distribution, since it weights all classes equally regardless of frequency. However, for the deployment context — where certain dialogue acts (e.g., crisis-relevant IRQ or YNQ used for risk assessment) may be rare but high-stakes — even macro-F1 does not surface per-label performance on safety-critical categories. The qualitative error analysis highlights three high-confusion label pairs: YNQ:IRQ (26% error rate), OD:ID (43%), and ID:ACK (28%) [Q91, Q92], which are informative for deployment but do not cover how the classifier would behave on utterances that fall outside the label set's scope (e.g., peer support emotional co-regulation turns). Output form is classification labels, which aligns with the deployment's expected output modality — the OF dimension is well-matched [Q5, Q6].

---

### 7. Stated Limitations

The authors identify several limitations relevant to deployment validity. Most critically for cross-regional applicability: "the majority of the sessions in HOPE belong to the mental health professionals and patients based in United States. Hence, the effectiveness of SPARTA on data from other geographical or demographical regions may vary" [Q98, Q99]. This is a direct acknowledgment of the geographic scope restriction that affects the South Asian deployment context. The authors also note that the system "does not make any diagnostic claims" [Q102] and that deployment of any such technology must keep "safety-risks and mitigating any sources of bias" in mind [Q103], with a general caution that "no technology will work perfectly in solving the problems related to mental health" [Q101]. The single-label constraint — where each utterance receives only one (primary) dialogue-act label even though "sometimes, an utterance can have multiple dialog-acts" [Q30] — is an explicit simplification that may reduce label fidelity for complex peer-support or crisis utterances where multiple communicative functions co-occur.

Additional limitations include annotator bias [Q96], the information loss inherent in ASR-to-text transcription [Q94], and the fact that only a subset of the dataset has been made publicly available [Q20]. The emotion annotation pilot was ultimately excluded due to severe class imbalance (~70% patient utterances negative, ~90% therapist utterances neutral) [Q128, Q129], limiting the benchmark's utility for affective session quality assessment. Error analysis reveals systematic model confusion among label pairs that are structurally related (e.g., ID/OD/ACK, IRQ/YNQ) [Q91, Q92], which could be consequential in deployment if those label boundaries are important for distinguishing counselor feedback categories. The label pairs IRQ & ID, ORQ & OD, and CRQ & CD are noted as "complementary in nature" and acknowledged to create annotation boundary challenges [Q51, Q52], a limitation that has downstream implications for any clinical quality assessment system relying on precise communicative intent classification. The acknowledged absence of label coverage for peer support and crisis intervention dynamics is not explicitly flagged by the authors but is inferrable from the scope description [Q22, Q93], and represents the most significant validity gap for the target deployment.

---

### 8. Authors and Affiliations

The paper is authored by Ganeshan Malhotra, Abdul Waheed, Aseem Srivastava, Md Shad Akhtar, and Tanmoy Chakraborty [Q11], affiliated with BITS Pilani (Goa, India), Maharaja Agrasen Institute of Technology (New Delhi, India), and IIIT-Delhi (India) [Q12]. Funding acknowledgments reference the Ramanujan Fellowship, the ihub-Anubhuti-iiitd Foundation under the NM-ICPS scheme of India's DST, and the Centre for Artificial Intelligence at IIIT-Delhi [Q106]. Despite this Indian institutional base, the data itself is sourced from US-based YouTube counseling videos [Q98], creating a notable asymmetry: the research team is South Asian, but the benchmark data reflects US clinical communication norms. Implementation used PyTorch and PyTorch Lightning with HuggingFace Transformers [Q107, Q64], training on a Tesla V100 with 32GB RAM under Ubuntu 18.04 [Q108], and experiment logging via WandB [Q109].
```

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | data_sources | "We develop a novel dataset, named HOPE, to provide a platform for the dialogue-act classification in counselling conversations." |
| Q2 | 1 | label_categories | "We identify the requirement of such conversation and propose twelve domain-specific dialogue-act (DAC) labels." |
| Q3 | 1 | data_sources | "We collect ∼ 12.9𝐾 utterances from publicly-available counselling session videos on YouTube, extract their transcripts, clean, and annotate them with DAC labels." |
| Q4 | 1 | task_taxonomy | "Further, we propose SPARTA, a transformer-based architecture with a novel speaker- and time-aware contextual learning for the dialogue-act classification." |
| Q5 | 1 | evaluation_metrics | "Our evaluation shows convincing performance over several baselines, achieving state-of-the-art on HOPE." |
| Q6 | 1 | evaluation_metrics | "We also supplement our experiments with extensive empirical and qualitative analyses of SPARTA." |
| Q7 | 1 | task_taxonomy | "Unlike general goal-oriented dialogues, a conversation between a patient and a therapist is considerably implicit, though the objective of the conversation is quite apparent." |
| Q8 | 1 | task_taxonomy | "The nature of conversations in a social counselling setting is particularly distinct as compared to a conventional chit-chat or goal-oriented conversations." |
| Q9 | 1 | task_taxonomy | "It follows a pattern which is different from both goal-oriented and general chit-chat based conversations." |
| Q10 | 1 | task_taxonomy | "Usually these conversations begin with greetings followed by the therapist inquiring for problems faced by the patient." |
| Q11 | 1 | authors_affiliations | "Ganeshan Malhotra, Abdul Waheed, Aseem Srivastava, Md Shad Akhtar, Tanmoy Chakraborty." |
| Q12 | 1 | authors_affiliations | "1BITS Pilani, Goa, India, 2Maharaja Agrasen Institute of Technology, New Delhi, India, 3IIIT-Delhi, India." |
| Q13 | 2 | data_sources | "The HOPE dataset contains ∼ 12.9K utterances across 212 mental-health counseling sessions." |
| Q14 | 2 | label_categories | "Each utterance in the dataset is tagged with one of the 12 counseling-aligned dialogue-act labels (c.f. Section 3)." |
| Q15 | 2 | data_sources | "We present HOPE, a novel and large-scale manually annotated, counselling-based conversation data for dialogue-act classification." |
| Q16 | 2 | annotation_process | "To cater to the requirements of counseling conversations, we define a novel hierarchical annotation scheme for the dialogue-act annotation." |
| Q17 | 2 | label_categories | "We propose twelve dialogue-act labels that are aligned with mental-health counseling session." |
| Q18 | 2 | task_taxonomy | "We propose SPARTA, a novel dialogue-act classification system that combines speaker-dynamics and local context through a time-aware attention mechanism, along with long-term global context." |
| Q19 | 2 | evaluation_metrics | "We perform extensive ablation study to establish the efficacy of each module of SPARTA." |
| Q20 | 2 | stated_limitations | "We have made the code and (a subset of) the dataset available at github." |
| Q21 | 2 | task_taxonomy | "The current work is connected to the existing literature in at least two dimensions – first, the dialogue-act classification, and second, text processing for mental-health counseling." |
| Q22 | 3 | task_taxonomy | "In this section, we present our dialogue-act classification dataset, called HOPE. In total, we annotated ∼ 12.9𝐾 utterances with 12 dialogue-act labels carefully designed to cater to the requirements of a counseling session." |
| Q23 | 3 | data_sources | "One of major hurdles we faced in the process of data collection was the unavailability of public counseling sessions, mainly due to the fact that they usually contain sensitive personal information. To curate this data, we carefully explored the web and collected publicly-available pre-recorded counselling videos on YouTube." |
| Q24 | 3 | data_sources | "To ensure confidentiality, we randomly assign synthetic names to all patients and therapists in all examples." |
| Q25 | 3 | data_format | "In the next step, we extract the transcriptions of each video using OTTER (https://www.otter.ai/), an automatic speech recognition tool. Subsequently, we correct transcription errors to remove any noise (i.e., spelling or grammatical mistakes)." |
| Q26 | 3 | data_sources | "The data collection process provides us 12.9𝐾 utterances from 212 counseling therapy sessions – all of them are dyadic conversations only." |
| Q27 | 3 | label_categories | "Since the counseling conversations have inherent differences with the standard conversations (such as SwitchBoard dataset conversation), it demands a carefully designed set of dialogue-act labels capable of catering the requirements of counselling conversations. Hence, we, in consultation with therapist and counselling experts, design a set of 12 dialog-act labels that are arranged in a hierarchy." |
| Q28 | 3 | label_categories | "These labels are designed to capture the intents of both the patient and therapist, and also be easily comprehensible to assist in the development of a conversational dialogue system." |
| Q29 | 3 | label_categories | "Each utterance in the dialogue belongs to one of the three categories – speaker initiative, speaker responsive, and general." |
| Q30 | 3 | stated_limitations | "Sometimes, an utterance can have multiple dialog-acts; however, they are rare in the annotated dataset. Hence, for simplicity, we consider only one (primary) label for each utterance." |
| Q31 | 4 | data_format | "The train, test, and validation splits are 70:20:10" |
| Q32 | 4 | label_categories | "Our annotation scheme assigns three distinct dialogue-act labels to the first two categories, while the remaining four labels belong to the general category." |
| Q33 | 4 | label_categories | "Information Request (IRQ): This label is used as a request for some information, e.g., 'Tell me your name.'" |
| Q34 | 4 | label_categories | "Yes/No Question (YNQ): The YNQ label is similar to IRQ; however, the expected response is a trivial yes or no answer." |
| Q35 | 4 | label_categories | "Clarification Request (CRQ): This label is assigned to those utterances in which a speaker usually asks the therapist for further clarification about topic that is being currently discussed." |
| Q36 | 4 | label_categories | "Opinion Request (ORQ): The ORQ label is used when the speaker seeks opinions of the listener." |
| Q37 | 4 | label_categories | "Clarification Delivery (CD): This label is used when the speaker provides further clarifications about a topic/entity under discussion." |
| Q38 | 4 | label_categories | "Information Delivery (ID): When the speaker provides some factual objective information about herself." |
| Q39 | 4 | label_categories | "Positive Answer (PA): These labels are used when the utterance is an answer in the form of a simple yes to a question that was previously uttered." |
| Q40 | 4 | label_categories | "Negative Answer(NA): It is used when the utterance is an answer of the form of a simple No to a question asked earlier." |
| Q41 | 4 | label_categories | "Opinion Delivery (OD): When the speaker explicitly lists out her/his opinions." |
| Q42 | 4 | label_categories | "Greeting (GT): Each session usually starts with greeting by one speaker and an appropriate response from the other." |
| Q43 | 4 | label_categories | "Acknowledgment (ACK): In normal conversation, very often, we utter (e.g., 'Yeah! You are right.') to acknowledge the other speaker or to show our agreement without an explicit information request, question, or command." |
| Q44 | 4 | label_categories | "General Chit-Chat (GC): Other utterances that do not belong to any of the above labels are tagged as GC, possibly because of the vagueness and the lack of sense in the context of the conversation." |
| Q45 | 4 | annotation_process | "We employed three annotators who are experts in linguistics." |
| Q46 | 4 | annotation_process | "To ensure the understanding of the tasks and annotation scheme, we took a sample of the dataset and asked each annotator to annotate them as per the prepared set of guidelines." |
| Q47 | 4 | annotation_process | "Following this, every annotation was discussed in the presence of the annotators and an expert therapist as moderator to ensure consistency." |
| Q48 | 4 | evaluation_metrics | "After the annotation process, we compute Cohen's Kappa score [7] to measure the agreement among annotators." |
| Q49 | 4 | evaluation_metrics | "We obtain the inter-rater agreement score of 0.7234 – which falls under the 'substantial' [7] category." |
| Q50 | 4 | annotation_process | "Annotators are in the age group of 25-35, with 2-10 years of professional experience." |
| Q51 | 4 | stated_limitations | "The broad definitions of speaker-initiative and speaker-responsive dialogue-act label pairs, IRQ & ID; ORQ & OD, and CRQ & CD, seem complementary in nature." |
| Q52 | 4 | stated_limitations | "However, the dataset does not support the above view entirely." |
| Q53 | 5 | data_sources | "In total, HOPE has transcripts for 12.9𝑘 utterances which are annotated with 12 dialogue-act labels." |
| Q54 | 5 | data_sources | "These utterances are evenly distributed between the patients and therapists with 6.38𝐾 and 6.47𝐾 utterances, respectively." |
| Q55 | 5 | data_format | "We split the dataset into 70:20:10 ratio as the train, test, and validation sets, respectively." |
| Q56 | 5 | data_sources | "In contrast to the regular patient-doctor conversations (e.g., SOAP), the dialogue sessions in HOPE are usually lengthy (∼ 59 utterances per session)." |
| Q57 | 5 | data_sources | "Moreover, the utterances in these sessions are themselves significantly longer as compared to other conversational datasets, with the average length of utterance of a patient being 103 words, whereas for therapist, it is ∼ 124 words." |
| Q58 | 5 | task_taxonomy | "The objective of SPARTA is to assign a correct dialogue-act label 𝑦𝑡 to every utterance 𝑈𝑡in the dialogue." |
| Q59 | 5 | task_taxonomy | "SPARTA is a transformer-based architecture that incorporates the speaker-aware contextual information for the dialogue-act classification." |
| Q60 | 5 | data_sources | "In our analysis of the HOPE dataset, we observed that a few of the dialogue-act labels are majorly associated with the patient, while a few others are related to the therapist." |
| Q61 | 5 | data_format | "For each utterance 𝑈𝑡 in a conversation dialogue, we extract the semantic representation through pre-trained RoBERTa model [25], which is subsequently utilized to leverage the local (𝐿𝑡) and global (𝐺𝑡) contextual information within the dialogue." |
| Q62 | 6 | data_format | "For the experiments, we randomly split the HOPE dataset into 70 : 20 : 10 ratio for the train, test, and validation sets." |
| Q63 | 6 | evaluation_metrics | "To measure the performances of SPARTA and other baseline systems, we compute macro-F1, weighted-F1, and accuracy scores." |
| Q64 | 6 | data_format | "We implemented our system in PyTorch [32] and utilized the pre-trained models from Huggingface Transformers library." |
| Q65 | 6 | data_format | "The hyperparameters are listed in Table 6." |
| Q66 | 6 | task_taxonomy | "CASA [35]: It is a context-aware attention-based system for the dialogue-act classification." |
| Q67 | 6 | task_taxonomy | "SA-CRF [41]: This recent baseline incorporates a CRF layer for the classification." |
| Q68 | 6 | task_taxonomy | "DRNN [44]: It is a novel Disconnected RNNs architecture which incorporates the position-invariant features for modelling." |
| Q69 | 6 | task_taxonomy | "ProSeqo [16]: It was proposed to efficiently handle the short and long texts using dynamic recurrent projections and locality-sensitive projections [37]." |
| Q70 | 6 | task_taxonomy | "TextVDCNN [9]: This is a deep convolutional network with residual connections for text classification." |
| Q71 | 6 | task_taxonomy | "TextRNN [24]: This was the first work to integrate RNNs into the multi-task learning framework." |
| Q72 | 6 | task_taxonomy | "RoBERTa [25]: We use RoBERTa as a baseline in this work due to its superioirity on various benchamarks." |
| Q73 | 6 | evaluation_metrics | "Since SPARTA incorporates three major components – local context, global context, and speaker-aware modules. The SPARTA-TAA system obtains the best scores of 60.29 macro-F1, 64.53 weighted-F1," |
| Q74 | 7 | evaluation_metrics | "Table 3: Table showcasing the performance of baseline models as compared with our SPARTA model. 𝑈𝑡 represents the use of Utterance representation, GC represents Global Context, LC represents Local Context and SA means the presence of Speaker Aware representations." |
| Q75 | 7 | evaluation_metrics | "The dagger symbol (†) represents statistically significant results compared to the best baseline, CASA." |
| Q76 | 7 | evaluation_metrics | "We also present the label-wise performance of SPARTA in Table 4." |
| Q77 | 7 | evaluation_metrics | "We can observe that SPARTA consistently yields good scores for the majority of the dialogue-acts, except for the Acknowledgement (ACK) where it records F1-score of merely 47.86%." |
| Q78 | 7 | evaluation_metrics | "Even for the under-represented labels (ORQ,NA and PA) in HOPE, SPARTA reports good F1-scores of 59.09%, 64.38% and 55.84%, respectively for these three labels." |
| Q79 | 7 | task_taxonomy | "Based on the type of modelling, we categorize the baselines into three groups – utterance-driven (𝑈𝑡), utterance+global context driven (𝑈𝑡 + GC), and utterance + global context + speaker-aware driven (𝑈𝑡 + GC + SA)." |
| Q80 | 7 | task_taxonomy | "Comparatively, SPARTA incorporates local context in addition to utterance, global context, and speaker dynamics (𝑈𝑡 + LC + GC + SA)." |
| Q81 | 7 | evaluation_metrics | "In the first category, the standard RoBERTa model attains the best macro-F1, weighted-F1 and accuracy of 43.97, 49.13, and 52.97%, respectively." |
| Q82 | 7 | evaluation_metrics | "In comparison, CASA [35] yields the improved weighted-F1 and accuracy scores at 55.95% (+6.82%) and 58.46% (+5.49%), respectively, with the global context as an additional information." |
| Q83 | 7 | evaluation_metrics | "Finally, we experiment with SA-CRF [41] which also includes the speaker-dynamics for the dialogue-act classification; however, its performance on HOPE is not at par with CASA [35]." |
| Q84 | 7 | evaluation_metrics | "It reports 35.97, 24.20, and 45.07% macro-F1, weighted-F1, and accuracy, respectively." |
| Q85 | 7 | evaluation_metrics | "In comparison, SPARTA-TAA obtains significant improvements over all baselines. It reports improvements of +8.64%, +8.58%, and +6.29% in macro-F1 (60.29), weighted-F1 (64.53), and accuracy (64.75%), respectively, as compared to CASA suggesting the incorporation of local context extremely effective." |
| Q86 | 7 | evaluation_metrics | "Note that ProSeqo [16] and CASA [35] are currently the state-of-the-art on switchboard dialogue-act corpus benchmark; yet they report inferior scores on HOPE compared to SPARTA." |
| Q87 | 7 | evaluation_metrics | "Moreover, we also report the mean of the 3-fold cross-validation results for both SPARTA-MHA and SPARTA-TAA, and the results are consistent with the train-val-test split case." |
| Q88 | 7 | evaluation_metrics | "We also perform statistical significance T-test comparing SPARTA-TAA and the best performing baseline (CASA). We observe that our results are significant with > 95% confidence across macro-F1 (p-value= 0.009), weighted-F1 (p-value= 0.014), and accuracy (p-value= 0.048) values." |
| Q89 | 7 | evaluation_metrics | "Error Analysis: In this section, we present two-way error analyses of SPARTA in terms of quantitative and qualitative evaluations." |
| Q90 | 7 | evaluation_metrics | "Quantitative analysis: We report the confusion matrix for SPARTA-TAA in Figure 4." |
| Q91 | 7 | stated_limitations | "We observe three pairs with significant error-rates (≥ 25%) – YNQ:IRQ (26%), OD:ID (43%), ID:ACK (28%)." |
| Q92 | 7 | stated_limitations | "For the prediction of information delivery (ID), SPARTA is confused most of the time with other classes – 19% with PA, 20% with NA, 43% with OD." |
| Q93 | 8 | data_sources | "We aim to tackle a very sensitive and a pervasive public-health crisis. We transcribe the data from publicly available counselling videos." |
| Q94 | 8 | data_format | "The automatic transfer of utterance from the speech modality to the text causes some information loss, though we tried our best to recover them through manual intervention." |
| Q95 | 8 | annotation_process | "Moreover, we consulted with mental-health professionals and linguists in preparing the annotation guideline." |
| Q96 | 8 | stated_limitations | "However, the annotator's bias cannot be ruled out completely." |
| Q97 | 8 | data_format | "The names of the patients and therapists involved in these sessions have been systematically masked." |
| Q98 | 8 | stated_limitations | "Another important aspect of the current work is that the majority of the sessions in HOPE belong to the mental health professionals and patients based in United States." |
| Q99 | 8 | stated_limitations | "Hence, the effectiveness of SPARTA on data from other geographical or demographical regions may vary." |
| Q100 | 8 | stated_limitations | "We understand that the building computational models in mental-health avenues has high-stakes associated with it and ethical considerations, therefore, become necessary." |
| Q101 | 8 | stated_limitations | "No technology will work perfectly in solving the problems related to mental health." |
| Q102 | 8 | stated_limitations | "It is important to note that we do not make any diagnostic claims." |
| Q103 | 8 | stated_limitations | "Further, the deployment of any such technology will be done keeping in mind the safety-risks and mitigating any sources of bias that may arise." |
| Q104 | 8 | label_categories | "We defined twelve dialogue-act labels to cater to the requirement of counselling sessions." |
| Q105 | 8 | data_format | "In total, we annotated ∼ 12.9𝑘 utterances across 212 sessions." |
| Q106 | 8 | authors_affiliations | "The authors acknowledge the support of the Ramanujan Fellowship, ihub-Anubhuti-iiitd Foundation set up under the NM-ICPS scheme of the DST, and CAI at IIIT-Delhi." |
| Q107 | 10 | authors_affiliations | "We use PyTorch 11 and Pytorch Lightning 12 frameworks for all our experiments. We extensively used Hugging Face Library for implementation of transformer based NLP models." |
| Q108 | 10 | authors_affiliations | "The complete model training was done on a linux machine with following specifications: GPU: TeslaV100, Memory: 32GB, Linux 64 Bit: Ubuntu 18.04 LTS" |
| Q109 | 10 | authors_affiliations | "We use WandB13 library to log all our results." |
| Q110 | 10 | evaluation_metrics | "The categorical cross-entropy loss is optimized using the Adam optimizer. We use dropout= 0.15 and train the models for 50 epochs in a batch of 8 samples. We use EarlyStopping to prevent our model from overfiting." |
| Q111 | 10 | data_format | "We use pretrained RoBERTa available from the Hugginface14 transformers for speaker aware as well as speaker invariant utterance representations." |
| Q112 | 10 | data_format | "For the GRU, we use input size and hidden dimension of 768 with 1 layer. For the classifier sub-module, we use a dropout of 0.1 a linear layer of 768 neurons and LeakyReLU as the activation." |
| Q113 | 10 | data_format | "Our attention blocks comprise of 3 Linear Layers for keys,queries and values and one linear layer to project the keys, queries and values." |
| Q114 | 11 | evaluation_metrics | "To verify the effectiveness of the time-aware attention to compute the local context, we also report the results with standard multi-head attention (MHA) mechanism." |
| Q115 | 11 | task_taxonomy | "The first set of results (i.e., SPARTA-BS or the baseline version of SPARTA) in Table 7 represents the absence of local context in SPARTA." |
| Q116 | 11 | evaluation_metrics | "It yields macro and weighted F1-scores of 51.83 and 54.98 respectively with global context only." |
| Q117 | 11 | evaluation_metrics | "We obtain 57.70% accuracy for the same setup." |
| Q118 | 11 | task_taxonomy | "Dialogue-act labels in a counseling based conversation not only depend on the abstract information of the dialogue but also on the utterances in the immediate vicinity of the current utterance." |
| Q119 | 11 | evaluation_metrics | "As can be observed from Table 7, the presence of both the global and local contextual information plays an importance role in SPARTA." |
| Q120 | 11 | stated_limitations | "Moreover, the absence of either of the component degrades the overall performance." |
| Q121 | 11 | evaluation_metrics | "This corroborates that they carry distinct and diverse contextual information." |
| Q122 | 11 | evaluation_metrics | "The comparison between the standard multi-head attention and the novel time-aware attention highlights the importance of attending over the relative positions of utterances." |
| Q123 | 11 | evaluation_metrics | "As stated earlier, extensive experimental results show that TAA yields better performance compare to MHA for all possible configurations." |
| Q124 | 11 | evaluation_metrics | "For all combinations, we observe performance drop of [3 − 4]% without the speaker information." |
| Q125 | 11 | task_taxonomy | "This is particularly apparent as a majority portion of the counseling conversation is driven by the therapist, thus the speaker-initiative dialogue-acts have higher relevance with the therapist utterances." |
| Q126 | 11 | label_categories | "In earlier phases of experiments, we also considered the role of emotion in dialogue act classification." |
| Q127 | 11 | label_categories | "We annotated a subset of our dataset with three emotion classes consisting of 'positive', 'negative' and 'neutral'." |
| Q128 | 11 | data_format | "We found that around ∼ 70% of utterances by the patients belonged to 'negative' class whereas ∼ 90% of therapists' utterances belonged to 'neutral' class." |
| Q129 | 11 | stated_limitations | "Due to such imbalance, this data was not used in the final version of our proposed architecture." |

### Category Index
- **task_taxonomy**: Q4, Q7, Q8, Q9, Q10, Q18, Q21, Q22, Q58, Q59, Q66, Q67, Q68, Q69, Q70, Q71, Q72, Q79, Q80, Q115, Q118, Q125
- **data_sources**: Q1, Q3, Q13, Q15, Q23, Q24, Q26, Q53, Q54, Q56, Q57, Q60, Q93
- **data_format**: Q25, Q31, Q55, Q61, Q62, Q64, Q65, Q94, Q97, Q105, Q111, Q112, Q113, Q128
- **label_categories**: Q2, Q14, Q17, Q27, Q28, Q29, Q32, Q33, Q34, Q35, Q36, Q37, Q38, Q39, Q40, Q41, Q42, Q43, Q44, Q104, Q126, Q127
- **annotation_process**: Q16, Q45, Q46, Q47, Q50, Q95
- **evaluation_metrics**: Q5, Q6, Q19, Q48, Q49, Q63, Q73, Q74, Q75, Q76, Q77, Q78, Q81, Q82, Q83, Q84, Q85, Q86, Q87, Q88, Q89, Q90, Q110, Q114, Q116, Q117, Q119, Q121, Q122, Q123, Q124
- **stated_limitations**: Q20, Q30, Q51, Q52, Q91, Q92, Q96, Q98, Q99, Q100, Q101, Q102, Q103, Q120, Q129
- **authors_affiliations**: Q11, Q12, Q106, Q107, Q108, Q109
