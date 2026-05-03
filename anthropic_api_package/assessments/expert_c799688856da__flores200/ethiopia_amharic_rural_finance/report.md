## Deployment Context

**Use case:** Document-level translation of agricultural input subsidy notices, land-use policy updates, and credit-scheme terms from federal and regional bureaus into Amharic
**Target population:** Farmer cooperative leaders and rural microfinance clients (e.g., ACSI, ADCSI borrowers) in Amhara interpreting government and lender document

# Validity Analysis: nllb
**Target context:** Amhara Region Agricultural and Microfinance Translation Cohort
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

Flores-200/NLLB provides credible language- and script-level support for Amharic — Ge'ez script is included with a dedicated SentencePiece vocabulary [Q382], and the benchmark's text-only output form aligns with the deployment's accepted format [elicitation A4]. These are real strengths for this text-only Amharic deployment. However, the four HIGH-priority dimensions (Input Ontology, Input Content, Output Ontology, Output Content) show substantial validity gaps. The benchmark's task taxonomy excludes agricultural, land-tenure, and microfinance genres entirely [Q95, Q166-Q169]; its content is exclusively Wikimedia-derived [Q95, Q151] with the authors themselves acknowledging cultural-coverage limitations [Q151]; its output ontology offers only general translation-quality scalars [Q455, Q648] that cannot detect the high-consequence error types (numerical-threshold alteration, conditional-logic distortion, terminology drift) that matter for binding administrative documents; and its annotator workforce is professional generalist translators [Q97-Q103], not the federal bureau translators with Ethiopian government-domain expertise that the deployer identifies as the validation authority [elicitation A3]. Independent 2025 research [WEB-10] empirically confirms that Flores+ scores fail to predict out-of-domain translation quality and that chrF++/BLEU can reward superficial named-entity copying. Web search found no Ethiopian agricultural/administrative MT benchmark exists [WEB-3, WEB-4] and no public ACSI/ADCSI Amharic terminology resource [WEB-15, WEB-16], meaning the gaps are real and unaddressed by the broader research community. Aggregate NLLB scores on Flores-200 should be treated as a coarse general-domain capability signal for Amharic, not as evidence of fitness for binding subsidy, land-policy, or credit documents.

## Practical Guidance

### What This Benchmark Measures

NLLB/Flores-200 measures general-domain sentence-level translation quality for Amharic prose, anchored in English-Wikimedia-derived content [Q95] and scored with chrF++/spBLEU/calibrated XSTS [Q455, Q648, Q654]. The strongest dimensions for this deployment are Input Form and Output Form: the benchmark validly assesses whether a model can produce coherent Amharic text in Ge'ez script for general-purpose prose, which is a necessary precondition for the deployment.

### Construct Depth

The benchmark probes general translation capability shallowly across many directions rather than deeply for any one domain. For Amharic specifically, evaluation is limited to 3,001 Wikimedia-derived sentences [Q95] scored with sentence-level metrics [Q336] that 2025 evidence shows can reward superficial overlap [WEB-10]. There is no evidence depth on: (a) terminology consistency across a multi-clause document, (b) numerical-threshold fidelity, (c) conditional-logic preservation, (d) acceptance by Ethiopian federal bureau translators, or (e) any agricultural/financial/bureaucratic register. The benchmark's evidence stops well short of what is needed for binding administrative document deployment.

### What Else You Need

To achieve a complete assessment for this deployment, the user should commission: (1) a domain-specific Amharic evaluation set covering agricultural input subsidies, land-tenure proclamations, and ACSI/ADCSI credit documents (Input Ontology + Input Content gaps); (2) a domain rubric with rules for numerical-fidelity, terminology-consistency, and conditional-logic preservation, since chrF++ cannot detect these error types (Output Ontology gap); (3) a federal-bureau-translator annotator pool to produce reference translations and acceptability ratings for representative documents (Output Content gap); (4) document-level coherence and terminology-consistency scoring on multi-clause samples (Output Form residual gap); and (5) a targeted Amharic Flores-200 audit analogous to those done for Hausa/Sepedi/Xitsonga/isiZulu [WEB-14], since no such audit has been published.

## Dimension Details

### Input Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The benchmark's task taxonomy is organized along resource level (high/low/very low) and a narrow set of domains (news, scripted talks, chat, WHO health) tested only in NLLB-MD for six language directions [Q159, Q166-Q169], none of which include Amharic. The deployment's core document genres — agricultural input subsidy notices, land-use policy updates, and credit-scheme terms — fall entirely outside the evaluation taxonomy. The paper itself frames the generalization question as 'How well do models generalize to non-Wikimedia domains?' [Q159] but does not extend domain testing to administrative, agricultural, or financial genres. Independent 2025 evidence confirms Flores+ scores do not reliably predict out-of-domain translation quality [WEB-10]. Given the HIGH priority assigned to this dimension by the elicitation, the absence of any agricultural/bureaucratic/financial category in the benchmark taxonomy is a significant content-validity concern.

**Strengths:**
- The benchmark explicitly anticipates the domain-generalization question and creates NLLB-MD to probe it [Q159], providing a documented framework (if not coverage) for thinking about non-Wikimedia domains.
- Resource-level stratification (high/low/very-low) [Q419, Q420] gives users a coarse signal of expected difficulty for Amharic, classified as low-resource.

**Checklist:**

- **IO-1**: Required deployment categories include: agricultural input subsidy notices, land-use/land-tenure policy updates, microfinance credit-scheme terms, and bureaucratic/legal register documents with numbered clauses and conditional eligibility logic. None of these are represented in Flores-200 or NLLB-MD task taxonomy [Q95, Q166-Q169]; web search confirms no Ethiopian agricultural or administrative MT benchmark exists [WEB-3, WEB-4, WEB-10]. — _Sources: Q95, WEB-3, WEB-4, WEB-10_
- **IO-2**: Yes — the taxonomy omits all regionally relevant administrative/financial/agricultural categories. NLLB-MD covers only news, scripted talks, chat, and WHO health [Q166-Q169], and only for six languages not including Amharic [Q161]. The Flores-200 evaluation set is sourced from Wikinews, Wikijunior, and Wikivoyage [Q95]. — _Sources: Q95, Q161, Q166, Q167, Q169_
- **IO-3**: The benchmark includes ancillary subtasks (LID [Q179], bitext mining [Q286], toxicity [Q699]) that are upstream model-development tasks rather than irrelevant for the deployment per se, but no category is irrelevant in a way that consumes evaluation weight. Domain coverage in NLLB-MD (chat, scripted talks) is not aligned with the deployment but does not displace deployment-relevant evaluation since Amharic is excluded from NLLB-MD entirely [Q161]. — _Sources: Q161_
- **IO-4**: Category gaps that harm content validity: (a) no agricultural/subsidy genre, (b) no land-tenure/legal proclamation genre, (c) no microfinance/credit-agreement genre, (d) no document-level coherence or terminology-consistency task. These omissions are confirmed structural — not addressable by tuning thresholds [WEB-10 confirms domain-benchmark mismatch is real]. — _Sources: Q159, WEB-10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q95] '3001 sentences sampled from English-language Wikimedia projects... Wikinews, Wikijunior, and Wikivoyage' (p.19)
- [Q159] 'How well do models generalize to non-Wikimedia domains?' (p.24)
- [Q161] 'NLLB-MD covers the following six languages: Central Aymara, Bhojpuri, Dyula, Friulian, Russian and Wolof' (p.24)
- [Q166] 'We translate the English side of the WMT21 English-German development set' (p.25)
- [Q167] 'scripted English-language talks' (p.25)
- [Q169] 'one World Health Organisation report... combined with sentences translated from the English portion of the TAUS Corona Crisis Report' (p.25)
- [Q419] '40 high-resource and 70 low-resource directions' (p.49)
- [Q420] '22 are very low-resource, i.e., have less than 100K training examples' (p.49)

*Web sources:*
- [WEB-3] EthioLLM/EthioBenchmark covers NER, sentiment, MT, summarization, QA for Amharic but only general-domain/news/social media — no agricultural/administrative/financial domain
- [WEB-4] EthioMT parallel corpora (15 Ethiopian languages) drawn from religious and general domains, not administrative/financial
- [WEB-10] 2025 'Languages Still Left Behind' study: NLLB models fine-tuned on naturalistic domain data outperformed Flores+ on domain test sets but underperformed on Flores+ — direct evidence that Flores+ scores do not predict domain-specific quality

</details>

**Information gaps:**
- Whether any private-sector or government-internal Amharic agricultural/financial MT benchmark exists; web search found none.

**Requires expert verification:**
- Whether the document-genre distinctions matter as much in practice as the elicitation suggests, given that source documents are primarily already in Amharic (per regional context, the deployment is converting documents into Amharic).

---

### Input Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Flores-200 and NLLB-Seed inputs are exclusively sampled from English-language Wikimedia projects [Q95, Q146], and the paper explicitly acknowledges 'the content reflects what Wikipedia editors find is relevant for English Wikipedia, and likely does not cover diverse content from different cultures' [Q151]. Low-resource bitext for African languages is 'often opportunistically drawn from known collections of multilingual content, such as the Christian Bible or publications of multinational organizations' [Q284], 'often limited in quantity and domain' [Q285]. The deployment requires Ethiopian-specific land-tenure proclamation vocabulary, ACSI/ADCSI financial terminology, and regional cooperative administrative phrasing — none of which is documented as present in NLLB training or evaluation data. The Hugging Face NLLB model card confirms 'Our model has been tested on the Wikimedia domain with limited investigation on other domains' [WEB-11]. Web search found no public ACSI/ADCSI Amharic terminology resources [WEB-15, WEB-16], confirming the absence of any reference content for the deployment's core terminology. Given HIGH priority and binding-document consequences, the content gap is severe.

**Strengths:**
- Deliberate Amharic support: dedicated 8,000-token Ge'ez-script SentencePiece vocabulary [Q382] and combined supervised cosine-loss + unsupervised MLM training [Q373, Q374], demonstrating attention to Amharic representation at the modeling level.
- Acknowledged limitation: the paper transparently flags the English-Wikipedia-centric content bias [Q151], allowing users to factor it into deployment decisions.
- Cross-referencing with Ethnologue and Glottolog [Q80, Q81] provides linguistic metadata that confirms language identity, even if content remains Wikimedia-derived.

**Checklist:**

- **IC-1**: Yes — the deployment requires region-specific cultural, legal-administrative, and financial knowledge: Ethiopian federal land proclamation vocabulary, ACSI/ADCSI loan terminology, cooperative-tier benefit language. The benchmark's content is sourced from English Wikinews/Wikijunior/Wikivoyage [Q95] and contains no documented Ethiopian administrative content. — _Sources: Q95, WEB-15, WEB-16_
- **IC-2**: The benchmark's culturally sensitive content (toxicity wordlists, etc.) is not regionally calibrated for Ethiopian context [Q715, Q716]. The general-domain Wikimedia content does not align with the deployment's bureaucratic/financial register. — _Sources: Q151, Q715, Q716_
- **IC-3**: Inputs derive from English-Wikipedia-relevance judgments [Q151], which encode topic priorities (Western-perspective biographies, geography, philosophy [Q146]) that do not transfer to Ethiopian agricultural/microfinance content. — _Sources: Q151, Q146_
- **IC-4**: INSUFFICIENT DOCUMENTATION — the registry contains no record of Ethiopian regional annotators reviewing Amharic input content for cultural specificity. Web search [WEB-13, WEB-14] documents post-hoc corrections for several African Flores-200 splits (Hausa, Sepedi, Xitsonga, isiZulu) but none for Amharic. — _Sources: WEB-13, WEB-14_
- **IC-5**: Content issues harming validity: (a) zero coverage of Ethiopian agricultural/financial vocabulary [WEB-15, WEB-16]; (b) zero coverage of federal land proclamation terminology; (c) Wikimedia content bias acknowledged by authors [Q151]; (d) low-resource African bitext relies on Bible and multinational publications [Q284] — domains divergent from the deployment. — _Sources: Q151, Q284, Q285, WEB-3, WEB-15_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q95] '3001 sentences sampled from English-language Wikimedia projects... Wikinews, Wikijunior, and Wikivoyage' (p.19)
- [Q146] 'Wikimedia's List of articles every Wikipedia should have... 11 categories such as People, History, Philosophy and Religion, Geography' (p.23)
- [Q151] 'the content reflects what Wikipedia editors find is relevant for English Wikipedia, and likely does not cover diverse content from different cultures' (p.24)
- [Q284] 'often opportunistically drawn from known collections of multilingual content, such as the Christian Bible or publications of multinational organizations' (p.37)
- [Q285] 'often limited in quantity and domain' (p.37)
- [Q369] 'Twelve of them even have less than hundred thousand sentence pairs' (p.44)
- [Q370] 'we struggled to curate meaningful amounts of monolingual data' (p.44)
- [Q382] 'a specific 8k SentencePiece vocabulary to better support the Ge'ez script' (p.45)

*Web sources:*
- [WEB-11] NLLB Hugging Face model card: 'Our model has been tested on the Wikimedia domain with limited investigation on other domains'
- [WEB-15] ACSI official website provides institutional background only — no Amharic terminology resources publicly available
- [WEB-16] FinDev Gateway ACSI profile — no terminology guide
- [WEB-3] No Ethiopian agricultural or administrative-domain Amharic benchmark exists
- [WEB-12] WaliaLLM paper: GPT-4 'often missing grammatical details in Amharic sentences', suggesting Amharic MT quality evaluation is unreliable

</details>

**Information gaps:**
- No corpus-level analysis of NLLB training data is publicly available to confirm or deny presence of Ethiopian government administrative vocabulary [WEB-11].
- No Amharic-specific Flores-200 audit of error rates exists [WEB-14].

**Requires expert verification:**
- Whether ACSI/ADCSI internal terminology actually diverges from federally standardized vocabulary, or whether federal standardization is sufficient — registry flags this as 'NEEDS VERIFICATION'.
- Whether domain-specific terminology gaps are recoverable through fine-tuning or require rebuilt evaluation data.

---

### Input Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
The benchmark's input form is well-aligned with the deployment at the modality and script levels. All inputs are text-only encoded via BCP 47 with ISO 639-3 + ISO 15924 script subtags [Q79], the Ethiopic (Ge'ez) script is explicitly supported with a dedicated 8k SentencePiece vocabulary [Q382], and the deployer confirmed text-only prose input is acceptable [elicitation A4]. Average sentence length (~21 words) [Q133] reflects general-domain prose. The deployment is HIGH on text-only operation, and the benchmark matches. Residual concerns are: (a) sentence-level evaluation architecture does not assess document-level structures (numbered clauses, conditional logic), and (b) Flores-200 sentences are general-domain prose, whereas administrative source documents have higher punctuation density and clause structure — though deployer accepted prose output [elicitation A4]. IF was assigned LOWER priority by elicitation, consistent with this score.

**Strengths:**
- Dedicated 8,000-token Ge'ez SentencePiece vocabulary trained jointly for Amharic and Tigrinya [Q382] addresses a key low-resource representation issue.
- BCP 47 / ISO 639-3 / ISO 15924 standardization [Q79] gives unambiguous language and script identification, important since Amharic uses Ethiopic exclusively.
- Combined supervised cosine-loss + unsupervised MLM training procedure [Q373, Q374] leverages monolingual Amharic data, which is more plentiful than bitext.

**Checklist:**

- **IF-1**: Signal distributions broadly match: text-only, Ethiopic script, sentence-level prose [Q79, Q133]. Source documents in deployment are also text in Ethiopic script. Sentence length distribution may differ (administrative documents have longer, clause-heavy sentences) but benchmark sentences average ~21 words [Q133] which is in a reasonable range. — _Sources: Q79, Q133_
- **IF-2**: Regional infrastructure can support text input; the deployment is text-only. However, web search [WEB-7, WEB-8] documents recurring mobile internet shutdowns in Amhara (August 2023–July 2024 and April–May 2023) which could disrupt connected pipelines, but this is an operational risk rather than a benchmark-form mismatch. — _Sources: WEB-7, WEB-8_
- **IF-3**: Domain-specific form differences: administrative source documents contain numbered clauses, tables, and cross-references absent from Flores-200 sentences [Q95, Q133]. The benchmark does not evaluate document-level coherence. The deployer accepted prose output [elicitation A4], reducing the severity of this gap. — _Sources: Q95, Q133_
- **IF-4**: Form mismatch is minor at the script/modality level. The principal residual gap is the absence of document-level evaluation, which is more accurately a scoring/output issue than an input-form issue. — _Sources: Q133_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q79] 'BCP 47 tag sequence using a three-letter ISO 639-3 code as the base subtag, which we complement with ISO 15924 script subtags' (p.17)
- [Q133] 'On average, sentences are approximately 21 words long' (p.22)
- [Q373] 'a new training procedure which combines supervised training... and unsupervised masked LM training' (p.44)
- [Q382] 'a specific 8k SentencePiece vocabulary to better support the Ge'ez script' (p.45)

*Web sources:*
- [WEB-7] Freedom House 2024: documented Amhara mobile internet shutdowns Aug 2023–July 2024 (operational risk, not benchmark form mismatch)
- [WEB-8] Freedom House 2023: prior April–May 2023 connectivity blackouts in Amhara

</details>

**Information gaps:**
- Sentence-length distribution comparison between Flores-200 and actual administrative Amharic documents is not documented.

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
The benchmark's output scoring ontology is a uniform scalar quality score (chrF++, spBLEU, or calibrated XSTS) applied to all directions and sentence types [Q455, Q648, Q661]. There is no domain-specific rubric for correctly rendering numerical eligibility conditions, conditional legal clauses, or financial terminology — the most consequential error types for the deployment. The XSTS scale measures 'meaning preservation' on a 5-point scale [Q654] but treats sentences uniformly. For toxicity, the taxonomy distinguishes source-present from added toxicity [Q705, Q706] with categories covering vulgar/profane/pornographic/hate-speech/bullying [Q712-Q714]; the paper acknowledges this is 'culturally sensitive' [Q715] with no Ethiopian regional calibration. A chrF++ improvement of +0.5 corresponds to detectable human improvement [Q624, Q631] but cannot distinguish silently altered subsidy thresholds from generally good prose. Independent 2025 evidence [WEB-10] shows mock translations reproducing named entities scored non-trivially on BLEU/ChrF++, confirming these metrics reward superficial overlap. Given OO is HIGH priority for binding documents, this is a structural-validity violation.

**Strengths:**
- XSTS protocol with calibration sets [Q650, Q664] addresses cross-language comparability of human evaluations, a non-trivial methodological contribution.
- Toxicity ontology distinguishing source-present vs. added toxicity [Q705, Q706] is conceptually appropriate for safety and partially relevant to the deployment's high-stakes context.
- The paper rejects unreliable model-based and roundtrip metrics [Q638, Q639] and explains its choice of chrF++ as the primary metric, providing transparency.

**Checklist:**

- **OO-1**: The output label categories (chrF++, spBLEU, XSTS 1-5) [Q455, Q654, Q648] are general translation-quality scores. They are not designed to flag deployment-critical errors such as misrendered eligibility thresholds, altered penalty rates, or inconsistent terminology across clauses. — _Sources: Q455, Q648, Q654, WEB-10_
- **OO-2**: Missing categories specific to the deployment: (a) numerical-fidelity scoring (correct rendering of percentages, dates, monetary amounts in legal clauses); (b) terminology-consistency scoring across a document; (c) conditional-logic preservation scoring; (d) administrative-register adherence scoring. None of these exist in NLLB's output ontology [Q455, Q648, Q654]. — _Sources: Q455, Q648, Q654_
- **OO-3**: The toxicity taxonomy is acknowledged as culturally sensitive [Q715, Q716] with English-anchored start [Q717], and no Ethiopian-specific calibration is documented. This may encode source-culture defaults but is a secondary concern relative to the missing domain-correctness rubric. — _Sources: Q715, Q716, Q717_
- **OO-4**: Stakeholder-driven taxonomy redesign would be required: federal bureau translators (deployer's stated authority [elicitation A3]) would need to define a domain rubric distinguishing acceptable from catastrophic translation error types for subsidy/credit/land documents. — _Sources: Q654_
- **OO-5**: Taxonomy issues harming validity: (a) structural validity — output ontology does not represent the construct of 'fitness for binding administrative documents'; (b) content validity — categories for high-consequence error types are absent; (c) external validity — chrF++ improvements do not predict deployment fitness [WEB-10]. — _Sources: Q455, Q661, WEB-10_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q455] 'We use the chrF++ metric to compare the model performance' (p.53)
- [Q648] 'we primarily evaluate using chrF++ using the settings from sacrebleu' (p.73)
- [Q654] 'XSTS rates each source sentence and its machine translation on a five-point scale' (p.74)
- [Q661] 'we take the majority XSTS score for each sentence and average these majority scores over all evaluated sentences' (p.74)
- [Q624] 'chrF++ improvements of +0.5 chrF++ usually correlate to statistically significant human evaluation improvements' (p.70)
- [Q705] 'In the context of translation, toxicity may originally be present in the source text or it can be generated de-novo in the target text (added toxicity)' (p.79)
- [Q715] 'Toxicity is culturally sensitive' (p.80)
- [Q716] 'Hate speech terms such as racial or ethnic slurs, for example, may well be the most challenging of all' (p.80)

*Web sources:*
- [WEB-10] 2025 study: mock translations merely reproducing named entities achieved non-trivial BLEU and ChrF++ scores, confirming metrics can reward superficial overlap rather than translational adequacy

</details>

**Information gaps:**
- No documented case study of NLLB mistranslating a numerical legal-financial clause in Amharic specifically [WEB-10]; the gap is inferential from metric design rather than empirically demonstrated for this language.

**Requires expert verification:**
- Federal bureau translators' specification of which error categories should be tracked for subsidy/credit document QA — required to design any deployment-specific rubric.

---

### Output Content — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
Flores-200 reference translations were produced through a multi-step workflow [Q93] with translators requiring 2-5 years of experience [Q97], 18-month re-testing [Q98], and reviewer native-speaker status with typically 5+ years of experience [Q99, Q100]. For low-resource languages, qualification thresholds were relaxed to accept broader linguistics degrees or extensive commercial experience [Q103]. No Amharic-specific annotator provenance, domain expertise, or inter-annotator agreement figures are documented in the registry. The community interview study informing research priorities included only 12 African-language speakers [Q31], a majority being immigrants in US/Europe with ~1/3 tech workers [Q32], whose perspectives 'may not consummately capture the sentiments of their communities back home' [Q39]. The deployer's required validation authority — federal bureau translators with Ethiopian agricultural/financial domain expertise [elicitation A3] — is not represented in the Flores-200 annotator workforce. Web search confirms post-publication corrections exist for Hausa/Sepedi/Xitsonga/isiZulu Flores-200 splits [WEB-14] but not Amharic, leaving Amharic reference quality unaudited. Common errors documented include 'mistranslation and unnatural translation errors' from non-English language influences and 'lower levels of standardization' [Q136-Q138]. Given OC is HIGH priority, this is a substantial concern.

**Strengths:**
- Documented multi-step QA workflow with 90% quality threshold [Q93, Q115, Q135] and post-editing for sub-threshold languages provides a baseline quality floor.
- Native-speaker reviewer requirement [Q99] preserves a basic legitimacy criterion for translation correctness.
- Transparency about diaspora bias in the community study [Q38, Q39, Q40] allows users to factor in selection bias when interpreting community-grounded claims.

**Checklist:**

- **OC-1**: Ground-truth labels are general-translation-quality judgments by professional translators with 2+ years' experience [Q97]. They do not reflect Ethiopian federal bureau translator perspectives on agricultural/financial document correctness — the deployer's stated authority [elicitation A3]. — _Sources: Q97, Q99_
- **OC-2**: High potential for disagreement: the deployer requires domain-trained federal bureau translators as primary authority [elicitation A3], whereas Flores-200 annotators are general translators without documented Ethiopian government-domain expertise [Q97-Q103]. Domain-specific terminology choices (e.g., loan-penalty rendering) likely differ. — _Sources: Q97, Q103_
- **OC-3**: Annotator demographics for Amharic specifically are not documented in the verbatim quote registry. General requirements [Q97-Q103] are documented but no Amharic-specific breakdown exists. Web search [WEB-13, WEB-14] confirms Nature 2024 paper documents the general workflow but no Amharic-specific annotator details. — _Sources: Q97, Q98, Q99, Q100, Q103, WEB-13_
- **OC-4**: Re-annotation by representative regional annotator pool would be required for deployment validation. No such pool is documented; ACSI/ADCSI publish no terminology guides [WEB-15, WEB-16] that could serve as gold standard. — _Sources: WEB-15, WEB-16_
- **OC-5**: Aggregation uses majority XSTS score per sentence then averaging [Q661]; this could erase minority perspectives, but for translation quality the more relevant concern is that minority-but-correct domain-specific renderings could be averaged out. — _Sources: Q661_
- **OC-6**: Label issues harming validity: (a) convergent validity — annotator pool does not converge on Ethiopian government-domain perspective [elicitation A3]; (b) external validity — Flores-200 quality judgments unlikely to predict acceptance by federal bureau translators or cooperative end-users with established administrative vocabulary. — _Sources: Q136, Q137, WEB-14_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q93] 'professional translators and reviewers aligned on language standards... If the quality assessment indicated that the quality is above 90 percent' (p.19)
- [Q97] 'Translators are required to have at least two to three years of translation experience' (p.20)
- [Q99] 'Flores-200 reviewers are also required to be native speakers of the target language' (p.20)
- [Q103] 'we modified the qualification process to accept applications from reviewers with more general language degrees' (p.20)
- [Q31] '12 in Africa' (p.8) — community study's African-speaker count
- [Q32] 'majority of our participants are immigrants living in the U.S. and Europe, and about a third of them (n = 17) identify as tech workers' (p.8)
- [Q39] 'their perspectives may not consummately capture the sentiments of their communities back home' (p.8)
- [Q136] 'Mistranslation and unnatural translation errors were still the most common errors' (p.22)
- [Q137] 'influences from other non-English languages... lower levels of standardization' (p.22)

*Web sources:*
- [WEB-13] Nature NLLB paper confirms general workflow but no Amharic-specific domain expertise documentation
- [WEB-14] Post-publication FLORES-200 corrections exist for Hausa, Sepedi, Xitsonga, isiZulu — but not Amharic, leaving Amharic reference unaudited
- [WEB-15] ACSI official website — no Amharic financial terminology guide publicly available
- [WEB-16] FinDev Gateway ACSI profile — no terminology resource

</details>

**Information gaps:**
- No public record of who specifically annotated the Amharic Flores-200 split, their credentials, or their domain backgrounds.
- No published Amharic-specific Flores-200 error audit comparable to those for Hausa/Sepedi/Xitsonga/isiZulu [WEB-14].

**Requires expert verification:**
- Whether federal bureau translators would actually disagree with Flores-200 Amharic reference renderings on general-domain Wikimedia content (a separate question from domain-specific document fitness).

---

### Output Form — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
The benchmark evaluates text outputs only [Q5] using sentence-level chrF++ and spBLEU [Q455, Q645, Q648] plus 5-point XSTS [Q654]. The deployer confirmed text-only prose output is acceptable for this NLLB deployment [elicitation A4], and this matches the benchmark's output form. However, no document-level coherence, terminology-consistency, or structural-preservation metrics are reported, all evaluation is sentence-level on general-domain content [Q5, Q336], and aggregate sentence-level chrF++ improvements may not indicate fitness for binding administrative documents requiring consistent rendering across clauses. National Ethiopia adult literacy is ~51.8% [WEB-5] with rural Amhara likely lower, meaning translated documents are often relayed orally through cooperative leaders — a use case that further increases the importance of consistent terminology, which sentence-level scoring does not assess. OF was rated LOWER priority by elicitation; given form alignment at the modality level, a moderately high score is warranted, with the residual concern being absence of document-level scoring.

**Strengths:**
- Text-only prose output [Q5] aligns directly with the deployer's confirmed acceptable format [elicitation A4].
- chrF++ as primary metric [Q648] with documented +0.5 detectability threshold [Q624, Q631] provides interpretable signal.
- Use of standardized SPM-200 for spBLEU [Q645] supports cross-system comparability.

**Checklist:**

- **OF-1**: Output modality (text prose) matches the deployer's text-only acceptance [elicitation A4]. Both benchmark and deployment operate on Amharic text in Ethiopic script [Q79, Q382]. — _Sources: Q5, Q79, Q382_
- **OF-2**: Text-to-speech is not in scope for the benchmark or this deployment, but oral relay through cooperative leaders is a documented end-use pattern [regional context]; the benchmark does not evaluate any output that supports oral-relay quality (e.g., terminology consistency across read-aloud clauses). — _Sources: WEB-5_
- **OF-3**: National adult literacy ~51.8% [WEB-5], with rural Amhara expected lower — translated prose will frequently be read aloud by cooperative leaders to lower-literacy borrowers, which depends on consistent administrative vocabulary not assessed by sentence-level chrF++ [Q455, Q648]. This is a partial form-mismatch insofar as the benchmark's evaluation unit (sentence) does not reflect the deployment's accessibility-mediated use unit (document read aloud). — _Sources: Q455, Q648, WEB-5_
- **OF-4**: Form mismatch at the modality level is minimal; the principal residual gap is the absence of document-level/terminology-consistency scoring [Q5, Q336], which constrains how reliably aggregate scores predict fitness for binding documents. — _Sources: Q5, Q336_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q5] 'evaluated the performance of over 40,000 different translation directions using a human-translated benchmark, Flores-200' (p.1)
- [Q336] 'report detokenized BLEU on Flores-200 devtest' (p.41)
- [Q455] 'We use the chrF++ metric to compare the model performance' (p.53)
- [Q624] 'chrF++ improvements of +0.5 chrF++ usually correlate to statistically significant human evaluation improvements' (p.70)
- [Q645] 'spBLEU, a BLEU metric based on a standardized SentencePiece model (SPM) covering 101 languages' (p.73)
- [Q648] 'we primarily evaluate using chrF++ using the settings from sacrebleu' (p.73)

*Web sources:*
- [WEB-5] Ethiopia adult literacy ~51.8% (UNESCO via World Bank, 2017) — establishes oral-relay relevance for output use

</details>

**Information gaps:**
- Amhara-specific rural literacy rate not publicly disaggregated [registry NOT FOUND].

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** Wikimedia-derived English-centric content [Q95, Q151] contains no Ethiopian agricultural/financial/administrative vocabulary; ACSI/ADCSI publish no public terminology resources [WEB-15, WEB-16].

**Recommendation:** Build a controlled Ethiopian administrative terminology lexicon covering federal land proclamation terms, ACSI/ADCSI loan vocabulary, and cooperative-tier benefits — sourced from federal/regional bureaus and validated by domain translators — and use it both as fine-tuning augmentation and as a glossary check during evaluation.

### Input Content ⚠

**Gap:** No public ACSI/ADCSI terminology guide [WEB-15, WEB-16] and no domain reference data exists for validation [WEB-3, WEB-4].

**Recommendation:** Engage ACSI/ADCSI directly through a memorandum of understanding to access internal Amharic terminology references and historical borrower-facing communications; treat these as the institutional gold standard for terminology rendering.

### Output Ontology ⚠

**Gap:** Scoring is uniform scalar chrF++/spBLEU/XSTS [Q455, Q648, Q654] with no rubric for numerical-fidelity, conditional-logic preservation, or terminology consistency — the highest-consequence error types for binding documents.

**Recommendation:** Develop a deployment-specific error rubric (in collaboration with federal bureau translators) that flags catastrophic categories: (a) altered numerical thresholds or dates, (b) reversed/dropped conditional clauses, (c) inconsistent rendering of defined terms across the document, (d) loss of named entities. Score translations against this rubric in addition to chrF++.

### Output Content ⚠

**Gap:** Amharic Flores-200 annotator credentials and provenance not documented [no Q-evidence]; annotators are general professional translators [Q97-Q103], not Ethiopian government-domain specialists; no Amharic-specific post-publication audit exists [WEB-14].

**Recommendation:** Commission an Amharic Flores-200 audit analogous to the Abdulmumin et al. corrections for other African languages, and recruit a panel of federal bureau translators to re-annotate a domain-specific evaluation sample, treating their judgments as the convergent-validity gold standard.

### Input Ontology ⚠

**Gap:** No agricultural, land-tenure, microfinance, or bureaucratic-legal genres in the task taxonomy; NLLB-MD covers only news/talks/chat/health and excludes Amharic [Q161, Q166-Q169].

**Recommendation:** Construct a deployment-specific evaluation set covering the three target document genres (subsidy notices, land-use updates, credit-scheme terms) with at least 200-500 sentences per genre, drawn from real federal/regional bureau and ACSI/ADCSI documents (with appropriate redaction).

### Output Form

**Gap:** All evaluation is sentence-level [Q5, Q336]; no document-level coherence or terminology-consistency scoring, which matters for oral-relay use to lower-literacy borrowers [WEB-5].

**Recommendation:** Add document-level evaluation: score multi-clause document translations on (a) cross-clause terminology consistency for defined terms, (b) preservation of numbered-clause structure in prose form, and (c) intelligibility when read aloud (oral-relay test with cooperative extension worker raters).

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "we took on this challenge by first contextualizing the need for low-resource language translation support through exploratory interviews with native speakers." |
| Q2 | 1 | input_ontology | "we created datasets and models aimed at narrowing the performance gap between low and high-resource languages." |
| Q3 | 1 | input_content | "we developed a conditional compute model based on Sparsely Gated Mixture of Experts that is trained on data obtained with novel and effective data mining techniques tailored for low-resource languages." |
| Q4 | 1 | input_ontology | "We propose multiple architectural and training improvements to counteract overfitting while training on thousands of tasks." |
| Q5 | 1 | output_form | "we evaluated the performance of over 40,000 different translation directions using a human-translated benchmark, Flores-200, and combined human evaluation with a novel toxicity benchmark covering all languages in Flores-200 to assess translation safety." |
| Q6 | 1 | output_form | "Our model achieves an improvement of 44% BLEU relative to the previous state-of-the-art, laying important groundwork towards realizing a universal translation system." |
| Q7 | 1 | output_content | "NLLB Team, Marta R. Costa-jussà, James Cross, Onur Çelebi, Maha Elbayad, Kenneth Heafield, Kevin Heffernan, Elahe Kalbassi, Janice Lam, Daniel Licht, Jean Maillard, Anna Sun, Skyler Wang, Guillaume Wenzek, Al Youngblood, Bapi Akula, Loic Barrault, Gabriel Mejia Gonzalez, Prangthip Hansanti, John Hoffman, Semarley Jarrett, Kaushik Ram Sadagopan, Dirk Rowe, Shannon Spruit, Chau Tran, Pierre Andrews, Necip Fazil Ayan, Shruti Bhosale, Sergey Edunov, Angela Fan, Cynthia Gao, Vedanuj Goswami, Francisco Guzmán, Philipp Koehn, Alexandre Mourachko, Christophe Ropers, Safiyyah Saleem, Holger Schwenk, Jeff Wang, Meta AI, UC Berkeley, Johns Hopkins University." |
| Q8 | 5 | input_content | "We begin by creating Flores-200, a many-to-many multilingual dataset that allows us to measure translation quality through any of the 40,602 total translation directions." |
| Q9 | 5 | input_content | "We developed a distillation-based sentence encoding technique, LASER3 (Heffernan et al., 2022), that helped us mine web data to create parallel datasets for low-resource languages." |
| Q10 | 5 | input_content | "Using both mined data and a set of human-translated seed data, we trained multilingual Mixtures-of-Experts models with state of the art performance." |
| Q11 | 5 | output_form | "Despite doubling the number of languages, our final model performs 40% better than the previous state of the art on Flores-101." |
| Q12 | 5 | output_ontology | "To detect and prevent potentially harmful translations that are hallucinated by the translation models, we created a dataset of toxic words for all 200 languages by combining automatic and" |
| Q13 | 5 | input_ontology | "Finally, developing translation models for low-resource languages requires the existence of high-quality, human-translated evaluation benchmarks." |
| Q14 | 5 | output_content | "The latter techniques are often plagued by noise and biases, making it difficult to validate the quality of the created datasets (Kreutzer et al., 2022)." |
| Q15 | 6 | output_form | "We proposed and conducted human evaluations on many languages our models cover, in addition to the common automatic metrics, to gain qualitative insight into the impact of the translation." |
| Q16 | 6 | input_content | "We open source all the benchmarks, data, scripts, and models described in this effort to support further research." |
| Q17 | 6 | input_ontology | "In addition, we focus on the practical applicability of our work for low-resource speaking communities." |
| Q18 | 6 | input_ontology | "Section 4 summarizes the creation process of Flores-200 and NLLB-Seed + NLLB-MD, our translation seed datasets, with quality analysis." |
| Q19 | 6 | input_content | "Section 5 overviews the creation of monolingual and mined bilingual data, which enables the creation of models for hundreds of languages." |
| Q20 | 6 | output_form | "Section 7 traces the automatic and human evaluation of our translations, including the detection of catastrophic and toxic translations." |
| Q21 | 6 | input_content | "Datasets shown in blue are novel datasets created in No Language Left Behind." |
| Q22 | 7 | input_ontology | "model that currently supports 202 languages, and analyze its quality and performance in Section 8." |
| Q23 | 7 | input_content | "To make our work available to the community, we open source the following: Human-Translated Datasets Flores-200: Evaluation dataset in 204 languages NLLB-Seed: Seed training data in 39 languages NLLB-MD: Seed data in different domains in 6 languages to assess generalization Toxicity-200: wordlists to detect toxicity in 200 languages" |
| Q24 | 7 | input_form | "Tools to Create Large Scale Bitext Datasets Language Identification for more than 200 languages LASER3: sentence encoders for identifying aligned bitext for 148 languages stopes: a data mining library that can be used to process and clean monolingual data, then create aligned bitext Training data recreation: Scripts that recreate our training data" |
| Q25 | 7 | input_ontology | "Translation Models covering 202 languages NLLB-200: A 54.5B Sparsely Gated Mixture-of-Experts model 3.3B and 1.3B Dense Transformer models 1.3B and 600M Dense transformer models distilled from NLLB-200" |
| Q26 | 7 | output_content | "To understand how low-resource language speakers perceive machine translation, we conducted an interview study with 44 low-resource language speakers." |
| Q27 | 7 | output_content | "Inspired by Value Sensitive Design (Friedman and Hendry, 2019; Van Der Hoven and Manders-Huits, 2020), we attribute community-level interests and values as the cornerstone of our research." |
| Q28 | 8 | input_ontology | "We designed a semi-structured interview protocol aimed at exploring the needs and concerns of low-resource language speakers vis-à-vis machine translation." |
| Q29 | 8 | input_ontology | "Although low-resource languages could be deemed low-resource for a variety of reasons, including being under-researched, digitized, or taught (Cieri et al., 2016; Magueresse et al., 2020), for the purpose of the study, we define low-resource as languages which had less than 1 million sentences of publicly available example translations at the time of the study." |
| Q30 | 8 | output_content | "Overall, our recruitment effort led us to 44 native speakers of low-resource languages from diverse backgrounds, with ages ranging from 23 to 58." |
| Q31 | 8 | output_content | "Covering a total of 36 languages, the distribution is as follows: 5 languages are spoken predominantly in North America, 8 in South America, 4 in Europe, 12 in Africa, and 7 in Asia." |
| Q32 | 8 | output_content | "Although our sample has breadth in terms of race, education, and location, the majority of our participants are immigrants living in the U.S. and Europe, and about a third of them (n = 17) identify as tech workers." |
| Q33 | 8 | output_content | "All interviews were conducted remotely via video conferencing software." |
| Q34 | 8 | output_content | "On average, the interviews lasted 1.5 hours." |
| Q35 | 8 | input_form | "Two-third of the interviews were recorded and transcribed." |
| Q36 | 8 | input_form | "For unrecorded interviews, two researchers took extensive notes throughout." |
| Q37 | 8 | output_content | "Bringing all 44 interviews together, responses were then systematically coded to allow major themes and ideas to emerge." |
| Q38 | 8 | output_content | "We acknowledge that sampling low-resource language speakers from diasporic contexts comes with its limitations." |
| Q39 | 8 | output_content | "For one, as immigrants, their perspectives may not consummately capture the sentiments of their communities back home." |
| Q40 | 8 | output_content | "Over-sampling tech workers may introduce another form of selection bias." |
| Q41 | 9 | output_content | "These nuanced perspectives were vital in shaping our research processes and procedures." |
| Q42 | 9 | output_content | "Even though many of our low-resource language interviewees are also fluent English speakers, almost all of them maintain that their native tongue remains a foundational part of their identity." |
| Q43 | 9 | output_content | "more than half of the participants of our study lament that without sustained efforts at prioritizing the usage and application of their native languages, many of them would face endangerment in time to come." |
| Q44 | 10 | input_content | "When asked about translation coverage, most low-resource language speakers express comfort in the fact that their respective languages are supported by existing systems." |
| Q45 | 10 | input_form | "For a select group of low-resource language speakers, whose languages contain multiple scripts and variants, full coverage remains lacking." |
| Q46 | 10 | input_form | "A Moroccan Arabic speaker said that fully supporting the Arabic language requires us to take the various extant Arabic languoids into account so that we do not end up favoring one form over another." |
| Q47 | 10 | input_form | "By excluding certain languoids or scripts and propping more well-resourced variants as the "default" option (Sunstein and Thaler, 2003), we not only jeopardize accurate cultural representation, but also exacerbate the unequal field that already plagues language distribution and usage across different parts of the world." |
| Q48 | 10 | output_content | "Reflecting on a sizable quality gap pitching high-resource language translation against low-resource language translation (Joshi et al., 2019), many interviewees cite poor and unreliable results as the key reason for irregular or discontinued use." |
| Q49 | 10 | output_ontology | "A few interviewees even mentioned that the lack of care given to their languages in some translation platforms have led to occasional toxic or crude translations, further eroding their confidence in these systems." |
| Q50 | 10 | input_content | "A Tigrinya speaker notes that in Ethiopia, where less than 20 percent of the country has internet access, actual access to what the web offers is even more restricted due to the lack of quality translation." |
| Q51 | 11 | output_content | "Combining insights drawn from interviews with low-resource language speakers and good practices distilled from literature on responsible AI (Arrieta et al., 2020; Bender et al., 2021; Blodgett et al., 2022; Paullada et al., 2021; Sambasivan and Holbrook, 2018), we introduce four key guiding principles underlying our research:" |
| Q52 | 11 | input_ontology | "Prioritize the needs of underserved communities. As aforementioned, we put the needs of low-resource language communities at the front and center of our effort. Recognizing that machine translation is a value-laden technological artifact that has historically de-prioritized certain populations, we use this effort to redistribute power and resources to underserved communities." |
| Q53 | 11 | input_ontology | "Sharing through open-sourcing. Low-resource language speakers across the board remind us that transparency ought to be a key emphasis when developing NLLB. With the dual intent to foster transparency and avoid a duplication of effort, we decided early on that we were going to open source NLLB." |
| Q54 | 11 | input_content | "low-resource language communities are not a monolithic group; they each navigate unique sociopolitical and cultural contexts." |
| Q55 | 12 | output_content | "our research effort is taken on by an interdisciplinary team with scholars from a wide array of humanities (i.e., Philosophy, Ethics), social scientific (i.e., Sociology, Linguistics), and technical (i.e., Computer Science, Statistics) backgrounds." |
| Q56 | 12 | input_ontology | "Broadly accessible machine translation systems support around 130 languages; our goal is to bring this number up to 200." |
| Q57 | 12 | input_content | "In deciding what languages to offer, we first parsed through the 101 languages covered in Flores-101, a dataset for translation evaluation covering predominantly low-resource languages." |
| Q58 | 12 | input_ontology | "From there, we generated a preliminary list of over 250 possible language candidates, eventually trimming it down to around 210 for final expansion from 101 to 200+ languages." |
| Q59 | 12 | input_content | "First, we considered all languages with a Wikipedia presence." |
| Q60 | 12 | input_content | "Wikipedia is a key site of knowledge dissemination for many speaking low-resource languages, making it a pertinent place to start." |
| Q61 | 12 | input_content | "Currently, Wikipedia supports over 300 languages, extending mindfully its content beyond English (Johnson and Lescak, 2022), and new languages can be added" |
| Q62 | 13 | input_form | "Code Language Script Family Subgrouping Res. Specification" |
| Q63 | 16 | input_content | "We display the language Code, language name, Script, and language Family. The symbol 🌐 indicates machine translation support by Google and/or Microsoft, whereas ✗ indicates support by neither. Res. indicates if we classify the language as high or low-resource. Specification contains, if available, additional information on the language variant collected in Flores-200. The superscript new indicates new languages added to Flores-200 compared to Flores-101." |
| Q64 | 16 | input_content | "as part of a community request process. Next, we solicited lists of languages spoken in various regions by native speakers, focusing particularly on African languages—a category of languages that have historically been underrepresented in translation efforts (Nekoto et al., 2020)." |
| Q65 | 16 | input_content | "We then examined language coverage in multiple existing datasets in the natural language processing community, paying focused attention on training datasets without accompanying evaluation datasets." |
| Q66 | 16 | input_content | "Finally, we considered the adoption and usage of each language by looking at the approximate number of native speakers and other community-level variables relevant to our work." |
| Q67 | 16 | output_content | "Next, for each of the language candidates, we partnered with linguists from various specialized language service providers to understand if each of these languages has a standardized written form." |
| Q68 | 16 | output_form | "We did this because having a reliable, high-quality evaluation dataset is critical to accelerated experimental progress." |
| Q69 | 16 | input_form | "However, prioritizing languages with fairly standardized written forms has notable downsides (see Appendix A)." |
| Q70 | 16 | input_form | "For one, many languages have natural variations and are being written in different standards or scripts in different regions." |
| Q71 | 16 | input_form | "For instance, languages such as Fulah include several distinct varieties and languages such as Kashmiri and Central Kanuri contain multiple scripts in common use." |
| Q72 | 16 | input_form | "Systematically documenting these dimensions helped us assess how we could best support multiple variants of different languages (such as languages with multiple writing systems or natural variation)." |
| Q73 | 17 | input_ontology | "In tandem with these considerations, deciding which languages to include in the final list ultimately came down to assessing the potential impact we might have on the respective low-resource language communities." |
| Q74 | 17 | input_ontology | "For instance, we exclude languages with extremely low number of native speakers." |
| Q75 | 17 | input_ontology | "Without a concerted plan to thoroughly understand the needs of these communities and potential risks we could cause, we do not feel comfortable including their languages in our effort." |
| Q76 | 17 | input_content | "Many of the languages that made the final cut have a presence on Wikipedia and are from historically underrepresented regions." |
| Q77 | 17 | input_ontology | "In this work, we exclude many languages that do not have written standards or are predominantly oral." |
| Q78 | 17 | input_ontology | "In accordance with the #BenderRule (Bender, 2019), we summarize information about each of our 204 supported languages in Table 1." |
| Q79 | 17 | input_form | "We represent each language with a BCP 47 tag sequence using a three-letter ISO 639-3 code as the base subtag, which we complement with ISO 15924 script subtags, as we collected resources for several languages in more than one script." |
| Q80 | 17 | input_content | "The language names have been cross-referenced with major linguistic information platforms such as Ethnologue (Lewis, 2009) and Glottolog (Hammarström et al., 2022)." |
| Q81 | 17 | input_content | "We provide Language family information for each language based on the Glottolog database (Hammarström et al., 2022)." |
| Q82 | 17 | input_content | "We examine if each language is supported by Google Translate and/or Microsoft Translate." |
| Q83 | 17 | output_ontology | "We categorize a language as low-resource if there are fewer than 1M publicly available, de-duplicated bitext samples with any other language within our set of 200 languages." |
| Q84 | 17 | input_form | "Note this goes beyond counting English-centric training data, as many languages may have available datasets in languages spoken more prominently in their region." |
| Q85 | 17 | output_ontology | "This results in 150 languages classified as low-resource." |
| Q86 | 17 | input_content | "The language information provided in Table 1 reflects the resources gathered through the Flores-200 collection efforts, which are described in the next section." |
| Q87 | 18 | input_content | "Low-resource translation faces several challenges, first and foremost that of data availability." |
| Q88 | 18 | input_content | "First, we describe the creation of Flores-200, a high quality, many-to-many benchmark dataset that doubles the language coverage of a previous effort known as Flores101." |
| Q89 | 18 | input_content | "Then, we trace the development process of professionally-translated seed bitext data in 39 low-resource languages, giving us the ability to train any models that require parallel data." |
| Q90 | 18 | input_ontology | "Finally, we describe NLLB-MD, a dataset in multiple different domains to evaluate generalizable translation capability." |
| Q91 | 18 | input_ontology | "A major area of focus in machine translation research has been on the development of high-quality evaluation datasets, or benchmarks that can be reliably used to assess progress in the field." |
| Q92 | 18 | input_ontology | "The creation of benchmark datasets at the yearly Workshop on Machine Translation (Akhbardeh et al., 2021) led to rapid progress on translation directions such as English to German and English to French." |
| Q93 | 19 | output_content | "We created a complex, multi-step process to ensure quality. First, professional translators and reviewers aligned on language standards. Next, translators translated the full set of Flores-200 sentences, followed by automated checks. Subsequently, the group of independent reviewers reviewed the quality, and based on their assessment, we sent some translations out for post-editing. If the quality assessment indicated that the quality is above 90 percent, the language is considered ready for inclusion in Flores-200." |
| Q94 | 19 | input_ontology | "The creation of Flores-200 seeks to double the existing language coverage of Flores101. This raises significant challenges due to the even more low-resource nature of the languages we have introduced in this effort. More specifically, these languages may require ever increasingly specialized professional translators, have less standardization, and the verifying process to ensure translation quality becomes more complex." |
| Q95 | 19 | input_content | "As a significant extension of Flores-101, Flores-200 consists of 3001 sentences sampled from English-language Wikimedia projects for 204 total languages. Approximately one third of sentences are collected from each of these sources: Wikinews, Wikijunior, and Wikivoyage. The content is professionally translated into 200+ languages to create Flores-200. As we translate the same set of content into all languages, Flores-200 is a many-to-many multilingual benchmark." |
| Q96 | 19 | output_content | "These are clearly separate sentences. The first fragment describes the overall FLORES-200 creation process and vetting, while the second fragment begins a new thought about specific requirements for translators.  SEPARATE" |
| Q97 | 20 | output_content | "Translators are required to have at least two to three years of translation experience in the relevant language pair if they have an academic degree in translation or linguistics and three to five years of translation experience if they do not have any relevant academic qualification." |
| Q98 | 20 | output_content | "Translators also undergo a translation test every 18 months to assess their translation quality." |
| Q99 | 20 | output_content | "Flores-200 reviewers are also required to be native speakers of the target language." |
| Q100 | 20 | output_content | "Reviewers typically have a translation degree, at least five years of experience working as a translator, translation review experience, and where possible are accredited by a relevant translation board." |
| Q101 | 20 | output_content | "We note that these are stringent standards, and extensions of Flores-200 to even more low-resource languages in the future may be difficult." |
| Q102 | 20 | output_content | "Already for many languages, finding a reviewer that meets the criteria above is very challenging." |
| Q103 | 20 | output_content | "In these cases, we modified the qualification process to accept applications from reviewers with more general language degrees such as Linguistics or African Language Studies, or no degree provided they have had extensive commercial translation experience (e.g. >10 years)." |
| Q104 | 20 | input_form | "The Flores-200 data creation workflow incorporates the original Flores-101 processes along with a few new initial phases as shared in detail below." |
| Q105 | 20 | output_content | "We have introduced an initial alignment phase to the workflow for the translators and reviewers before translating Flores-200." |
| Q106 | 20 | output_content | "There are several steps incorporated in alignment between the translation and quality assurance agencies – aligning on resourcing and target regions, linguistic topics between the translators and reviewers per language through a new alignment template, and query logs between the linguists on both sides." |
| Q107 | 20 | input_form | "The alignment template helped linguists identify approaches on the language script, standardization, spelling, borrowed terms, neologisms, informative content style, and resources for glossaries, and sample content in the target language." |
| Q108 | 20 | output_content | "This has been especially helpful for languages with less established standards for translation." |
| Q109 | 20 | input_form | "Translation then begins with an initial translation phase, where the same 200 sentences are translated by all participating translators for each language." |
| Q110 | 20 | input_content | "The initial translation data contains an even split across the three sources — Wikinews, Wikijunior, and Wikivoyage, with the segments corresponding to the same articles for context and continuity." |
| Q111 | 20 | output_form | "The initial translations are then sent to the QA LSP team for review." |
| Q112 | 20 | output_content | "The main focus of the initial translation and QA steps is to understand and align on the translation approach between the translators and reviewers." |
| Q113 | 20 | output_ontology | "The report contains sentence-level feedback (identified error category, error severity level and comments where possible) and high-level feedback on locale expectations, use of specified script, use of borrowings and/or neologisms, named entities, and overall style and register." |
| Q114 | 21 | output_content | "Translation LSP teams may respond to the initial QA reports with arbitration. Adjustments are then made to all alignment materials where needed and the translation approach is updated and re-aligned on. The full translation of all 3000 sentences then begins (see Goyal et al. (2022) for details)." |
| Q115 | 21 | output_content | "When full translation is completed, the QA LSP team performs a final QA review and assesses a 20% sample data. Optional arbitration, rework and QA spot checks may follow if the final quality score of the translation dataset is below 90%." |
| Q116 | 21 | input_content | "The standard Flores-200 workflow focuses on translation only from English. While this standardizes the process for all languages, it has clear limitations." |
| Q117 | 21 | output_content | "For example, there are many qualified translators who may not speak English, but are able to translate between several non-English languages. Further, several languages may be easier to translate from a non-English source." |
| Q118 | 21 | input_form | "LSP teams analyzed the linguistic characteristics of each Arabic languoid and how much they differed from Modern Standard Arabic on various linguistic aspects such as vocabulary differences, grammatical and structural differences, influence from other regional languages and informative content style." |
| Q119 | 21 | input_form | "Arabic languoids were either translated directly from English or adapted from the Modern Standard Arabic dataset with the English source provided as context." |
| Q120 | 21 | input_form | "For each languoid that implemented adaptation, LSP teams also created a termlist consisting of terms from Modern Standard Arabic and an equivalent term in the target Arabic languoid to ensure consistent adaptation." |
| Q121 | 21 | output_content | "One tier encompassed a partial QA review where the reviewer assessed a 10% sample data and reviewed the termlist. This process was applied to languoids that were assessed to have mainly vocabulary differences, some structural differences and some influence from other regional languages." |
| Q122 | 21 | output_content | "Another tier required the reviewer to only assess the termlist as the languoids mainly differed from Modern Standard Arabic minimally and on vocabulary usage." |
| Q123 | 21 | output_form | "The 90% quality threshold is applied as usual." |
| Q124 | 21 | input_form | "There were four languages (ace_Arab, bjn_Arab, min_Arab, taq_Tfng) that were transliterated from their Latin script counterparts." |
| Q125 | 21 | output_content | "The translation LSP performs transliteration into the appropriate scripts. The QA LSP reviews a 20% sample of the transliterated text with the English source and Latin script data provided for context." |
| Q126 | 21 | output_form | "In the QA report, transliteration errors are flagged only by severity level; there are no error categories for transliteration errors. Two or more errors found in one segment would be flagged with a major severity level. Anything fewer would be flagged as minor." |
| Q127 | 21 | output_form | "The quality threshold for transliteration is 95%." |
| Q128 | 22 | input_form | "FLORES is divided into three evaluation splits, totaling 3001 sentences." |
| Q129 | 22 | output_content | "Summary of Quality Control based on the statistics of 73 languages that implemented the new Flores-200 workflow." |
| Q130 | 22 | input_content | "FLORES-200 consists of translations from 842 distinct web articles, totaling 3001 sentences." |
| Q131 | 22 | input_form | "These sentences are divided into three splits: dev, devtest, and test." |
| Q132 | 22 | input_form | "We release the full text of the dev and devtest splits, and keep the test set hidden through an evaluation server." |
| Q133 | 22 | input_form | "On average, sentences are approximately 21 words long." |
| Q134 | 22 | output_content | "To consider a language ready for inclusion in Flores-200 requires a final human quality assurance evaluation." |
| Q135 | 22 | output_form | "The minimum acceptable standard is 90 percent." |
| Q136 | 22 | output_content | "Mistranslation and unnatural translation errors were still the most common errors found while assessing the quality of the human translations." |
| Q137 | 22 | output_content | "These were mainly due to influences from other non-English languages that may be prominently used in the target communities, leading to excessive borrowings of vocabulary and grammar, literal translations due to infrequent usage of the target language in a formal, informative content style and the lower levels of standardization." |
| Q138 | 22 | output_content | "There has also been an increasing trend in spelling inconsistencies in the human translations due to lower levels of standardization leading to inconsistent or even subjective or preferential approaches." |
| Q139 | 23 | input_content | "Overall, compared to Flores-101, our new translation workflow substantially streamlines the translation effort. For example, the number of languages requiring re-translation (see Table 2, right) is only 10, down from 45 in Flores-101." |
| Q140 | 23 | output_content | "However, despite these improvements, we continued to experience similar challenges as in Flores-101 — but at even greater scale due to the increasing low-resource nature of the languages." |
| Q141 | 23 | output_content | "For example, low-resource languages are not as often worked with in the localization or translation fields. As a result, there are lower levels of industry-wide standardization, leading to a more challenging path to navigate (Skadiņš et al., 2014a)." |
| Q142 | 23 | output_content | "This led to longer turnaround times, and often required finding new translators and reviewers several times. These challenges were especially felt during some of the more difficult languages such as Sicilian and Buginese, which have taken significantly longer periods of time to complete (287 days)." |
| Q143 | 23 | input_content | "To this end, we create NLLB-Seed, a set of professionally-translated sentences in the Wikipedia domain. NLLB-Seed consists of around six thousand sentences in 39 languages." |
| Q144 | 23 | output_content | "Critically, NLLB-Seed contains data that is definitely in the specified language, as it is fully professionally translated by humans." |
| Q145 | 23 | input_ontology | "NLLB-Seed's target-side data in various languages can be utilized for language identification models that classify which language an arbitrary piece of input text is in. The dataset can also be used for its aligned bitext, for example to train translation models. Another option is to utilize NLLB-Seed to do domain finetuning, such as adapting general-purpose translation models to the Wikipedia domain." |
| Q146 | 23 | input_content | "Data for NLLB-Seed was sampled from Wikimedia's List of articles every Wikipedia should have, a collection of 10,000 Wikidata IDs corresponding to notable topics in different fields of knowledge and human activity. These are split into 11 categories such as People, History, Philosophy and Religion, Geography." |
| Q147 | 23 | input_content | "We uniformly sampled a subset of IDs from which we would draw data, and mapped these to the corresponding English Wikipedia articles. From each of these articles we then sampled the data that would be sent to translators." |
| Q148 | 23 | input_form | "Instead of extracting individual sentences, which would have left translators with little context to work with, we chose to sample triplets of" |
| Q149 | 23 | input_content | "Note that we focus on 39 for NLLB-Seed as these were the languages where there did not exist publicly available high-quality bitext for training in large quantities." |
| Q150 | 24 | input_form | "contiguous sentences, ensuring no more than one triplet per article was used (similar to Flores-200)." |
| Q151 | 24 | input_content | "We note that like Flores-200, NLLB-Seed's source data is English-centric and sampled from English Wikipedia. This has an important effect: the content reflects what Wikipedia editors find is relevant for English Wikipedia, and likely does not cover diverse content from different cultures." |
| Q152 | 24 | output_content | "Further, the target text in NLLB-Seed is ultimately translated by humans, and thus potentially contains effects of translationese (often defined as awkward, unnatural, or overly literal translations)." |
| Q153 | 24 | output_content | "Script, specification, spelling and translation approaches were first established and aligned on from Flores-200." |
| Q154 | 24 | input_form | "The datasets were translated directly from English for 39 languages while two Arabic script languages (Acehnese and Banjar) and Tamasheq in Tifinagh script were transliterated from their respective Latin script datasets that were first translated from English." |
| Q155 | 24 | output_content | "Following the translation or transliteration phase was a linguistic quality assessment phase in which the completed datasets were checked against the linguistic alignments from FLORES along with automatic quality control checks." |
| Q156 | 24 | output_content | "We note that NLLB-Seed has a key distinction compared to evaluation benchmarks such as Flores-200. Critically, NLLB-Seed is meant to be used for training rather than model evaluation. Due to this difference, NLLB-Seed does not go through the human quality assurance process present in Flores-200." |
| Q157 | 24 | input_ontology | "Avoiding overfitting and achieving strong out-of-domain performance remains a major challenge in neural machine translation (Koehn and Knowles, 2017)." |
| Q158 | 24 | input_ontology | "While both Flores200 and NLLB-Seed cover a large number of topics, we want to ensure that models perform well on text coming from different domains." |
| Q159 | 24 | input_ontology | "More specifically, we want to answer the following two questions: (1) How well do models generalize to non-Wikimedia domains? (2) Does fine-tuning on high quality in-domain parallel text lead to good performance?" |
| Q160 | 24 | input_content | "In order to investigate these questions, we create the NLLB-MD parallel dataset, covering six directions and made up of 3,000 professionally-translated sentences in each of four different domains." |
| Q161 | 24 | input_content | "NLLB-MD covers the following six languages: Central Aymara (ayr_Latn), Bhojpuri (bho_Deva), Dyula (dyu_Latn), Friulian (fur_Latn), Russian (rus_Cyrl) and Wolof (wol_Latn)." |
| Q162 | 24 | input_content | "Along with five low-resource languages, we also chose to include one high-resource language to enable comparisons with other models and datasets." |
| Q163 | 24 | input_content | "We chose low-resource languages related to other high-resource ones (e.g., fur_Latn is related to ita_Latn), so as to enable future studies investigating language transfer." |
| Q164 | 25 | input_content | "We collected 3,000 English sentences in each of four different domains, and sent them to professional translators to be translated into each of NLLB-MD's six target languages." |
| Q165 | 25 | output_content | "The translation workflow used is analogous to the one followed for NLLB-Seed." |
| Q166 | 25 | input_content | "We translate the English side of the WMT21 English-German development set, containing a sample of newspapers from 2020 (Akhbardeh et al., 2021)." |
| Q167 | 25 | input_content | "We translate text extracted from a series of scripted English-language talks covering a variety of topics." |
| Q168 | 25 | input_content | "We extract 3,000 utterances from the multi-session chat dataset of Xu et al. (2022), which contains on average 23 words per turn." |
| Q169 | 25 | input_content | "We translated one World Health Organisation report (Donaldson and Rutter, 2017) and combined it with sentences translated from the English portion of the TAUS Corona Crisis Report." |
| Q170 | 25 | output_form | "Flores-200, which enables reliable evaluation of over 200 languages, is critical for ensuring the quality of the results our systems generate." |
| Q171 | 25 | input_ontology | "NLLB-Seed plays an important role for training both sentence encoders (see Section 5) and translation models (see Section 6.5)." |
| Q172 | 25 | output_form | "We utilize NLLB-MD to measure the generalizability of our translation models across multiple domains (see Section 8.3)." |
| Q173 | 25 | input_content | "The current techniques used for training translation models are difficult to extend to low-resource settings — that is, when data for a language is limited in both aligned textual data (bitext, or pairs of translated sentences) and single language data (monolingual, or data in one language only)." |
| Q174 | 25 | input_ontology | "Many low-resource languages are supported only through small targeted bitext datasets such as the Christian Bible (McCarthy et al., 2020), which are extremely limited in domain diversity." |
| Q175 | 25 | input_content | "Publicly available bitext data is often scarce (Gowda et al., 2021)." |
| Q176 | 25 | input_content | "Our approach centers around extending existing datasets by collecting non-aligned monolingual data and using large-scale data mining (Schwenk et al., 2021b) to identify sentences that have a high probability of being translations of each other in different languages." |
| Q177 | 25 | input_form | "We first develop language identification systems (LID, Section 5.1) that label which language a given piece of text is written in." |
| Q178 | 26 | input_ontology | "As highlighted, we create language identification and a monolingual data cleaning process, then describe the training of LASER3 to produce large-scale mined bitext for hundreds of languages." |
| Q179 | 26 | input_ontology | "Language identification (LID) is the task of predicting the primary language for a span of texts." |
| Q180 | 26 | input_content | "The rise of large-scale pretraining, particularly the increasing focus on multilingual models, is strongly dependent on the existence and identification of monolingual data at scale." |
| Q181 | 26 | input_content | "Advances in cross-lingual representation learning such as large-scale bitext mining, unsupervised machine translation and back-translation at scale require large quantities of clean monolingual data." |
| Q182 | 26 | input_content | "These disparate approaches, including our focus on large-scale data mining of aligned sentences, involve taking large quantities of input text often drawn from web corpora such as CommonCrawl and labeling them with corresponding languages." |
| Q183 | 26 | input_content | "There are a few well-known challenges associated with large-scale and accurate language identification using web data: (1) Domain mismatch could occur due to the scarcity of text reliably labeled by language." |
| Q184 | 27 | input_ontology | "Language identification is applied on web corpora to extract monolingual sentences. Aligned pairs are later identified with LASER3." |
| Q185 | 27 | input_content | "while the web contains data in thousands of languages (Prasad et al., 2018; Scannell, 2007), most of it is unlabeled." |
| Q186 | 27 | input_content | "Filling in this gap is Wikipedia, which is frequently used for training language identification (Thoma, 2018) on a broader scale beyond the Christian Bible (although such relatively clean formal text is not representative of the web at large)" |
| Q187 | 27 | input_content | "Severe class imbalance could exist because many of the low-resource languages of interest to us have low presence on the web." |
| Q188 | 27 | input_content | "For classifiers to work, they must have an extremely low false positive rate. Otherwise, low-resource languages are prone to misidentification" |
| Q189 | 27 | input_form | "Efficiency to run over large web collections remains low. Even though classification is massively parallelizable, running it on all texts makes speed critical." |
| Q190 | 27 | input_content | "While LID could be seen as a solved problem in some domains (McNamee, 2005), it remains an open challenge for web data (Abadji et al., 2022; Caswell et al., 2020; Zampieri et al., 2015b)." |
| Q191 | 27 | input_form | "Specifically, issues coalesce around (1) scaling successful approaches to more languages (Jauhiainen et al., 2017); (2) incidents where there is significant domain mismatch (Widdows and Brew, 2021) in the cases of short tweets or multiple languages (Duvenhage, 2019); and (3) distinguishing similar languages (Goutte et al., 2016)." |
| Q192 | 27 | output_form | "CLD3 and fasttext (Grave et al., 2018) are two readily available models offering high detection performance for 107 and 187 languages respectively." |
| Q193 | 28 | input_content | "In contrast, we curate Flores-200 to use as development set, so that our LID system performance is tuned over a uniform domain mix." |
| Q194 | 28 | input_content | "We believe Flores-200 is closer to web content." |
| Q195 | 28 | input_ontology | "Our approach combines a data-driven fasttext (Grave et al., 2018) model trained on Flores-200 with a small set of handwritten rules to address human feedback on classification errors." |
| Q196 | 28 | input_ontology | "In this work, we collaborate in close partnership with linguists to understand which languages can be easily confused and analyze the model performance while employing a flat classification strategy." |
| Q197 | 28 | input_ontology | "We utilize fasttext to train language identification models (Bojanowski et al., 2017; Joulin et al., 2017)." |
| Q198 | 28 | input_ontology | "fasttext is widely used for text classification tasks due to its simplicity and speed, while achieving good quality." |
| Q199 | 28 | input_form | "We embed character-level n-grams from the input text, then leverage a multi-class linear classifier on top." |
| Q200 | 28 | input_ontology | "The lightweight nature of fasttext enables our LID models to handle web-scale data." |
| Q201 | 28 | output_form | "A linear model has the benefit of being easily explainable, allowing us to trace any classification error back to its" |
| Q202 | 29 | input_ontology | "We experimented with two different designs. (1) A combination of multiple binary classifiers where the final decision is obtained by selecting the language having the highest score after a threshold is applied. We apply threshold optimization so that when the confidence of a classifier is low, the corresponding language is not considered for the final decision. If none of the classifiers surpass its threshold, the sentence is filtered out. (2) A multiclass classifier using softmax over all possible languages. In this case, the threshold optimization is done after the softmax." |
| Q203 | 29 | input_ontology | "Our experiments motivated us to focus on the second approach, which offers several advantages. First, changing the threshold for one language does not impact the performance of the other, while this is not true in the first setting. Second, we found that this approach generalizes better to out of domain data which is our primary use case (Wikipedia → Web data). Finally, a single classifier has the added benefit of being computationally simpler, thus streamlining the language identification process." |
| Q204 | 29 | input_content | "We use publicly available datasets to train our LID system, partially covering our of interest. We supplement these with NLLB-Seed (see Section 4.2) for any missing language." |
| Q205 | 29 | input_form | "However, the amount of data available for each language is far from uniform, and massive class imbalance in the raw training data exists (Caswell et al., 2020; Dunn, 2020). For example, English alone represents 10.1% of our training data, while Minangkabau (Latin script) represents only 0.06%." |
| Q206 | 29 | input_form | "Following Arivazhagan et al. (2019), we experimented with multiple settings of temperature upsampling for under represented, where sentences from a language l representing pl percent of the dataset are sampled proportionally to p^(1/T)_l. Optimal performance was obtained at 1/T = 0.3." |
| Q207 | 29 | output_form | "Our best model was trained with softmax loss over two epochs with a learning rate of 0.8 and embeddings with 256 dimensions. We discarded words with less than a thousand occurrences after upsampling and picked a minimum and maximum character n-gram length of two and five respectively, which were assigned a slot in buckets of size 1,000,000. All hyperparameters were tuned on Flores-200 dev." |
| Q208 | 29 | input_content | "Language identification is a challenging task where numerous failure modes exist, often exacerbated by the gap between the clean data that LID models are trained on and the noisy data that LID models are applied to. LID models that are trained in a supervised manner on fluently written sentences may have difficulty identifying grammatically incorrect and incomplete strings extracted from the web. Furthermore, models can easily learn spurious correlations that are not meaningful for the task itself." |
| Q209 | 29 | output_content | "In light of these challenges, we collaborated closely with a team of linguists throughout different stages of LID development to identify proper areas of focus, mitigate issues, and explore solutions." |
| Q210 | 29 | output_content | "We leveraged the linearity of fasttext to build an easy-to-use interface for linguists to peek into its inner workings. The tool enabled linguists to" |
| Q211 | 30 | input_form | "To mitigate the learning of spurious correlations due to noisy training samples while modeling hundreds of languages, we worked in collaboration with linguists to develop several filters, illustrated in Table 3 and described below." |
| Q212 | 30 | input_content | "The public datasets we used for training were mostly built from webpages." |
| Q213 | 30 | input_content | "Through investigation by linguists, numerous occurrences of mislabeled sentences were found, likely caused by short passages in a different language within a page, such as Indonesian sites that display a collection of Javanese poems." |
| Q214 | 30 | input_form | "We also noticed random creative use of unexpected scripts, typically used for decoration or emphasis as pointed out in Caswell et al. (2020)." |
| Q215 | 30 | input_form | "We computed the character distributions of each language on our development set and defined an arbitrary accepted character set for each of them by considering all characters falling within the first 95th percentile." |
| Q216 | 30 | input_form | "We consequently filtered out any sentence from our training set that was composed of less than 80% of such accepted characters." |
| Q217 | 30 | input_form | "For languages whose script spans thousands of characters, the character histogram method mentioned above was not as effective since the character distribution trends were less prominent." |
| Q218 | 30 | output_content | "As an alternative, linguists provided Unicode ranges to define accepted character sets." |
| Q219 | 30 | input_form | "Any sentence containing less than 50% of characters from that set was eventually discarded." |
| Q220 | 31 | input_form | "Linguists also pointed out that many mislabeled training samples were actually plain English sentences. This can be explained by the massive prevalence of English on the web, even on pages primarily written in other languages. We built a simple, dedicated binary fasttext classifier to filter these samples out of our training dataset." |
| Q221 | 31 | output_form | "This section presents a comparison of our approach to existing publicly available models on both Flores-200 and annotated noisy web data, followed by an error analysis." |
| Q222 | 31 | output_form | "We analyze the performance of our LID models on the Flores-200 dataset from Section 4 and compare to other open-source models. We utilize Flores-200 for evaluation as the target-side text is human-verified as being in the right language. Utilizing standard public datasets for evaluation is less reliable given they often contain untrustworthy language labels and are quite noisy (Kreutzer et al., 2022)." |
| Q223 | 31 | output_form | "We compare our LID model with three publicly available models: CLD3, LangId and LangDetect. Table 4 reports performance of our final LID model on the set of various language intersections covered by all four models. Micro F1 scores and False Positive Rates across all languages found in Flores-200 are displayed in Table 5." |
| Q224 | 31 | output_form | "Given the different scopes of languages supported, we report on 3 cascading intersections with Flores-200: (1) the 51 languages also supported by LangId, LangDetect and CLD3, (2) the 78 languages also supported by LangId and CLD3 and (3) the 95 languages also supported by CLD3. We report metrics of all models across all intersections to reflect the impact of false positives on unseen languages." |
| Q225 | 31 | output_form | "Our model is capable of handling the 200 languages of Flores-200 (compared to the 107 languages supported by CLD3) while achieving significantly higher performance than all three of LangId, LangDetect and CLD3. Furthermore, the gain in F1 score is accompanied by a noticeable improvement in False Positive Rate, suggesting a much stronger fit for extracting low-resource languages from web corpora (Caswell et al., 2020)." |
| Q226 | 31 | input_content | "Despite strong results on Flores-200, we expect a sizable gap in performance when applying our LID model to our target web data." |
| Q227 | 32 | input_content | "Indeed, various sources of noise such as language mixing, creative use of various scripts, and leetspeak are widespread online." |
| Q228 | 32 | input_content | "Extracting sentences from internet pages is also prone to unexpected artifacts introduced after parsing." |
| Q229 | 32 | output_form | "There is no readily available evaluation set from the web domain on which to properly assess and tune performance, let alone iterate on design choices when modeling." |
| Q230 | 32 | input_content | "To this end, we select 74 low-resource languages on which our preliminary LID model yield low F1 scores." |
| Q231 | 32 | input_content | "After a first run of language identification on web data, we randomly selected several thousand sentences across various languages for which prediction scores fell between 50% and 90%." |
| Q232 | 32 | input_form | "That hard threshold was chosen upon manual inspection, noticing that many classification errors were found within that range." |
| Q233 | 32 | output_content | "Human annotators were tasked with inspecting our random sentences and assessing whether each was indeed in the predicted language." |
| Q234 | 32 | output_ontology | "Based on these annotations, we built a challenge set for language identification to benchmark our final LID model." |
| Q235 | 32 | input_content | "As shown on Table 6, we achieve lower performance than on the Flores-200 dataset, hinting at a non-negligible domain mismatch." |
| Q236 | 32 | output_form | "As suggested in Caswell et al. (2020), we report False Positive Rates (FPR) on top of F1 scores, to get a better picture of how well our model would fare" |
| Q237 | 33 | output_content | "It should be noted that since the sentences to annotate were chosen based on a previous model, this challenge set is biased by that underlying intermediate model." |
| Q238 | 33 | output_content | "We worked closely with linguists to analyze them." |
| Q239 | 33 | input_ontology | "Upon inspection, we found that these language pairs correspond to highly similar languages, displaying major vocabulary and grammar overlap." |
| Q240 | 33 | input_ontology | "For example, Asante Twi (aka_Latn) and Akuapem Twi (twi_Latn) are two mutually intelligible languoids of the Akan language continuum, which share common words, phrases, or even identical sentence translations." |
| Q241 | 33 | output_content | "This suggests that from a linguistic point of view, the LID confusion found in these similar languages is to be expected and is not a symptom of a deeper modeling issue." |
| Q242 | 33 | output_content | "In practice, this means prediction performance might be underestimated for some languages and calls for collecting and accepting multiple language labels in future work." |
| Q243 | 33 | output_form | "We noticed that predictions tend to be more robust for long sentences." |
| Q244 | 33 | output_form | "This is consistent with an observation by Jauhiainen et al. (2017) and could be further investigated." |
| Q245 | 33 | output_form | "A potential mitigation strategy would be to tune our models on a more balanced development set with respect to length." |
| Q246 | 33 | input_form | "In our current approach, we mitigate this issue by applying length filters in the downstream monolingual pipeline described in Section 5.2." |
| Q247 | 34 | input_form | "We synthetically create test samples of a specific length without cutting words, except for languages with continuous scripts." |
| Q248 | 34 | input_content | "Monolingual data is a valuable resource which can be used for a variety of downstream tasks such as bitext mining, backtranslation, and language model training." |
| Q249 | 34 | input_content | "Additionally, data quality can have a large impact on the performance of such tasks." |
| Q250 | 34 | input_content | "In order to maximize the potential benefits of leveraging these data sources, we aim to produce high quality and clean monolingual data." |
| Q251 | 34 | input_content | "As discussed earlier in this section, such data can be scarce, particularly in the low-resource setting." |
| Q252 | 34 | input_content | "We therefore decided to extend the work done in CCNet, CCMatrix (Schwenk et al., 2021b; Wenzek et al., 2020), and others like OSCAR (Ortiz Suárez et al., 2019)." |
| Q253 | 34 | input_content | "In this section, we describe our end-to-end process for both curating and cleaning monolingual data." |
| Q254 | 34 | input_content | "We begin with web data as our starting point, provided by CommonCrawl (CC) and ParaCrawl (Bañón et al., 2020)." |
| Q255 | 34 | input_form | "This data has been preprocessed to remove all markup and (approximately) normalize encoding to UTF-8." |
| Q256 | 34 | input_form | "HTML stripping converts block tags to newlines while inline tags are removed." |
| Q257 | 34 | input_form | "The resulting lines can contain many sentences or simply a short snippet of text; we refer to them as "paragraphs"." |
| Q258 | 34 | input_form | "To convert the raw web text in paragraph form to sentences, we apply language identification in a hierarchical fashion." |
| Q259 | 34 | input_form | "First, we apply LID to each web paragraph." |
| Q260 | 34 | input_form | "Subsequently, we use the predicted language to choose a sentence splitter for the language." |
| Q261 | 34 | input_form | "The raw paragraphs sometimes contain a mix of different languages or might include code switching." |
| Q262 | 34 | input_form | "To avoid having a mix of languages, once we have split the documents in sentences, we re-run LID to identify the language of each sentence." |
| Q263 | 34 | input_form | "If the sentence-level LID does not match the paragraph-level LID, we discard the sentence to be sure we keep" |
| Q264 | 35 | input_form | "We also discard sentences if they do not use the expected script for the target language." |
| Q265 | 35 | input_form | "Note that many sentences are extremely noisy. In particular, they often contain long URLs or lists of hashtags. These confuse the LID and script identification process as they are in Latin script and not always in the same language as the original sentence." |
| Q266 | 35 | input_form | "To identify the actual language of the sentence, we truncate the URLs and hashtags before running the language identification." |
| Q267 | 35 | input_content | "Given the domain mismatch (see Section 5.1), our development set could not be utilized to tune the detection thresholds of our fasttext classifier to a desired performance level." |
| Q268 | 35 | input_content | "Instead, we relied on the distribution of model scores on the monolingual data of the ParaCrawl dataset (Bañón et al., 2020) across all predicted languages." |
| Q269 | 35 | input_content | "We chose that dataset based on the assumption that its language distribution would realistically match that of CommonCrawl, despite the inevitable bias induced by the LID model used in the creation of ParaCrawl itself." |
| Q270 | 35 | input_form | "This analysis motivated our choice of 0.5 as a default threshold in the first two cases, except for high-resource languages, where we could afford a more stringent value of 0.9 and still collect enough monolingual data in our downstream pipeline depicted in Section 5.2. In the last case, we picked values corresponding to the peak of each distribution (ranging from 0.2 to 0.4), in the hope to collect a sizable amount of data from our pipeline." |
| Q271 | 35 | input_form | "We subsequently apply a few heuristics to remove sentences that do not match reasonable quality criteria: minimum and maximum length, space/punctuation/number/emoji ratios, and maximum number of repeated characters." |
| Q272 | 35 | input_form | "For example, if a sentence contains over 20% punctuation, it likely is not a well-formed sentence." |
| Q273 | 35 | input_form | "As our model encoders (see Section 5.3) were not trained on substantial content with emojis, we prefer to strip emojis from all text to avoid losing sentences that could match if they did not have the special characters." |
| Q274 | 36 | input_form | "Table 8: Examples of Filtered Sentences in our monolingual pipeline." |
| Q275 | 36 | input_form | "We note that these ratios should differ between languages, and are not universally applicable. In certain languages, concepts may take many more words to convey, meaning that setting length-related thresholds is problematic. Similarly, other languages may utilize more punctuation or have shorter words. Thus, we do not set extremely stringent filters, and we examine the amount of text filtered across all 200 languages for each of the filters." |
| Q276 | 36 | input_form | "Deduplication. The margin-based criterion of our mining approach requires unique sentences (see Section 5.3), but the sentence splitting and cleaning process might generate a lot of duplicate content, so we run a global deduplication process over all sentences of the same language." |
| Q277 | 36 | input_form | "Language Model Filtering. As we are interested in keeping high quality sentences in our datasets to later train our final multilingual translation models, when possible, we also run a Language Model (LM) filtering. In practice, it is difficult to train high-quality language models for low-resource languages, so we focus on applying language model filters on a few high-resource languages only. Because we do most of the mining where one side of the pair is English, we believe that if we have high-quality content in the English corpus, the mining alignment process will also output high-quality content on the other side of the pair. For English, we use the KenLM (Heafield, 2011) model from CCNet (Wenzek et al., 2020)." |
| Q278 | 36 | input_content | "We processed around 37.7 Petabytes of data through the whole pipeline. This was a challenge for data management and disk usage. In particular, we had to make hard decisions when filtering high-resource languages to artificially keep only around 30% of data from the most voluminous languages. This threshold was identified as the limit under which the LM score would identify sentences of low quality." |
| Q279 | 36 | input_content | "We realize that processing such volume of data is not always possible and are open-sourcing much of our results and code to make it easier for everyone to benefit from our effort." |
| Q280 | 36 | input_content | "We started with 107.9 billion paragraphs from the web (97.4% high-resource, 2.6% low-resource) and discarded 2.8 billion sentences (85.3% high, 14.7% low) because of LID/Script mismatch or low LID score (see Section 5.1) to produce 43.7 billion monolingual sentences, of which 21.5 billion sentences are in English." |
| Q281 | 37 | input_form | "Note that we have such a big drop in number of sentences because we drastically filtered high-resource languages to keep the top 30% of sentences based on LM score." |
| Q282 | 37 | input_ontology | "Machine translation, like many machine learning applications, is heavily data-driven." |
| Q283 | 37 | input_content | "Previous works have clearly established that translation quality generally increases with the amount of available high-quality training data (Koehn and Knowles, 2017)." |
| Q284 | 37 | input_content | "Existing parallel corpora for low-resource languages are often opportunistically drawn from known collections of multilingual content, such as the Christian Bible or publications of multinational organizations." |
| Q285 | 37 | input_content | "These are often limited in quantity and domain." |
| Q286 | 37 | input_ontology | "The underlying idea of our bitext mining approach is to first learn a multilingual sentence embedding space and to use a similarity measure in that space to decide whether two sentences are parallel or not." |
| Q287 | 37 | input_ontology | "This comparison can be done for all possible pairs in two collections of monolingual texts, termed global mining in Schwenk et al. (2021a)." |
| Q288 | 37 | input_ontology | "Another common alternative approach is referred to as hierarchical or local mining and comprises of first performing a selection of potential document pairs, and then limiting the mining to sentences within each document pair." |
| Q289 | 37 | input_ontology | "In this work we follow the approach from WikiMatrix (Schwenk et al., 2021a) and CCMatrix (Schwenk et al., 2021b), which both used global mining." |
| Q290 | 37 | input_content | "As our mining approach requires a multilingual embedding space, we faced several challenges when scaling this representation to the 200 languages of the No Language Left Behind effort." |
| Q291 | 37 | input_content | "For example, how do we make sure that all languages are well-learned? And how should we account for large imbalances of available training data?" |
| Q292 | 37 | input_ontology | "Training a massively multilingual sentence encoder from scratch each time a new set of languages is added would be computationally very expensive." |
| Q293 | 38 | input_ontology | "the drawback that the learned embedding spaces from each new model are not (naturally) mutually compatible. This can make mining intractable as for each new encoder, the entirety of available monolingual data needs to be re-embedded, and for English alone, this means tens of billions of sentences and large compute resources." |
| Q294 | 38 | input_ontology | "In order to overcome these issues, one approach is to train smaller mutually compatible sentence encoders using the teacher-student distillation technique proposed by Reimers and Gurevych (2020)." |
| Q295 | 38 | input_ontology | "Several extensions of this underlying idea were proposed by Heffernan et al. (2022) that we adopt (see Section 5.3.2)." |
| Q296 | 38 | input_ontology | "In order to find aligned texts, early approaches focused on information beyond the text itself." |
| Q297 | 38 | input_ontology | "More recent approaches have begun to leverage advancements in representation learning by encoding texts into an embedding space, and then using a distance-based method to determine if a pair of texts in different languages have a similar meaning." |
| Q298 | 38 | input_ontology | "Works such as España-Bonet et al. (2017); Guo et al. (2018); Hassan et al. (2018); Yang et al. (2019) used bilingual embeddings, but this has the limitation of not being able to directly mine across many languages." |
| Q299 | 38 | input_ontology | "In order to address this, learning a massively multilingual embedding space allows for any pair of languages to be encoded and mined (Artetxe and Schwenk, 2019a,b; Feng et al., 2020; Kvapilíková et al., 2020; Schwenk, 2018)." |
| Q300 | 38 | output_form | "However, when applying these approaches to obtain representations at the sentence level, they can often suffer from the lack of an explicit sentence-based criterion during training, resulting in poor performance on tasks such as bitext retrieval (Hu et al., 2020)." |
| Q301 | 39 | input_form | "However, pre-training for the BERT encoders is done using both a masked language modelling (MLM) and translation language modelling (TLM) objective (Conneau et al., 2020)." |
| Q302 | 39 | output_ontology | "Sentence embeddings are then produced by passing bilingual translation pairs through the dual-encoder setup and then applying an additive margin softmax loss (Yang et al., 2019)." |
| Q303 | 39 | input_form | "Unlike the previous BERT-based approaches, there is no pre-training, and sentence embeddings are produced by using an encoder-decoder architecture, and then max-pooling over the encoder outputs." |
| Q304 | 39 | input_ontology | "When attempting to learn a multilingual embedding space, one of the limitations of many existing approaches is that each time a model is to be expanded to include a new set of languages, the entire model must be retrained from scratch, which is very costly." |
| Q305 | 39 | input_content | "In this distillation setup, English-paired bitexts are used to both learn the English embedding space of a monolingual teacher (SBERT), while also using the non-English side to learn a new language." |
| Q306 | 39 | input_ontology | "Heffernan et al. (2022) further built upon this approach by experimenting with different architectures for teacher and student (e.g., BiLSTM and Transformer), and also applying such distilled sentence representations to the task of bitext mining." |
| Q307 | 39 | input_ontology | "The overall approach focuses on starting with a massively multilingual sentence encoder teacher model and adapting it to several different low-resource student models." |
| Q308 | 39 | input_ontology | "This enables us to add low-resource languages without needing to compete with high-resource languages for capacity, to avoid retraining the full model from scratch, and to maintain compatibility of the multilingual embedding spaces for subsequent mining." |
| Q309 | 40 | input_form | "The original training procedure (Artetxe and Schwenk, 2019b) was changed as follows: the use of SentencePiece tokenization and upsampling of low-resource languages." |
| Q310 | 40 | input_content | "Training was performed on the same 93 languages with public resources obtained from OPUS (Tiedemann, 2012)." |
| Q311 | 40 | input_ontology | "students are specialized for one language or several similar languages;" |
| Q312 | 40 | input_ontology | "students are randomly initialized since we want to handle low-resource language for which we don't have a pre-trained LM;" |
| Q313 | 40 | input_form | "students may have a dedicated SentencePiece vocabulary different from the teacher, to better accommodate scripts and tokens in the student languages (see Section 5.3.3)" |
| Q314 | 40 | output_ontology | "students learn to minimize the cosine loss with the teacher, since we also use cosine distance for bitext mining (see Figure 12);" |
| Q315 | 40 | output_ontology | "students can have an MLM loss to leverage student language monolingual data (see Figure 12 and Section 5.3.3)." |
| Q316 | 40 | input_ontology | "Our student encoders used a 12-layer transformer, hidden size of 1024, with 4 attention heads, totalling around 250M parameters." |
| Q317 | 40 | input_content | "All students were trained with available bitexts in their respective language, complemented by two million sentences of English/English and English/Spanish." |
| Q318 | 40 | input_ontology | "Teacher-student training was performed on 16 GPUs, ADAM optimizer, a learning rate of 0.0005, and a batch size of 10,000." |
| Q319 | 40 | input_ontology | "We trained student encoders for 148 languages and named these models LASER3." |
| Q320 | 40 | input_ontology | "Mined bitexts will be subsequently utilized to improve translation quality for 200 languages." |
| Q321 | 40 | output_form | "Consequently, our primary metric is neural machine translation (NMT) quality." |
| Q322 | 40 | output_form | "However, mining and NMT training are computationally expensive, and it is intractable to systematically perform this evaluation for many different sentence encoder variants." |
| Q323 | 40 | output_form | "As an evaluation proxy, we use a mining-based multilingual similarity search error rate, referred to here as xsim." |
| Q324 | 40 | output_form | "As opposed to cosine accuracy which aligns embeddings based on the highest cosine score, xsim aligns source and target embeddings based on the highest margin score, which was shown to be beneficial in mining (Artetxe and Schwenk, 2019a)." |
| Q325 | 41 | output_form | "where x and y are the source and target sentences, and NNk(x) denotes the k nearest neighbors of x in the other language. We set k to 4." |
| Q326 | 41 | output_form | "All xsim results are calculated on Flores-200 devtest, using the ratio margin where margin(a, b) = a/b." |
| Q327 | 41 | output_form | "Additionally, all scores are calculated into English (i.e. xxx → eng). English is encoded by the teacher and the other language by the LASER3 student." |
| Q328 | 41 | output_form | "Initial experiments indicated that a threshold on the margin of 1.06 seems to be the best compromise between precision and recall for most of the languages." |
| Q329 | 41 | input_form | "For these NMT baselines, we do not apply additional filtering on the bitexts and leave this to the training procedure of our massively multilingual NMT system." |
| Q330 | 41 | output_form | "We further limit our experimentation to the translation from foreign languages into English. This helps to compare resources and assess the translation quality among all languages." |
| Q331 | 41 | input_content | "The English corpus we mine in has 21.5 billion unique sentences." |
| Q332 | 41 | output_form | "We do not attempt to optimize the architecture and parameters of the bilingual NMT systems to the characteristics of each language pair, namely the size of available bitexts, but use the same architecture for all." |
| Q333 | 41 | output_form | "Therefore, the reported results should not be interpreted as the best possible ones given the available resources – they are mainly provided to validate the mined bitexts." |
| Q334 | 41 | input_form | "We use a 12 layer encoder and decoder and train for 100 epochs." |
| Q335 | 41 | input_form | "The SentencePiece (SPM) vocabulary has 7,000 tokens." |
| Q336 | 41 | output_form | "We look for best performance on the Flores-200 development set, and report detokenized BLEU on Flores-200 devtest." |
| Q337 | 41 | input_content | "The original LASER encoder, as used in the CCMatrix project (Schwenk et al., 2021b) performs very well on several high-resource languages like Arabic, Chinese, Czech, German, Japanese, Polish or Indonesian." |
| Q338 | 41 | input_content | "We used the CCMatrix bitexts directly for these languages. We then trained new sentence encoders and performed mining for the 148 remaining ones." |
| Q339 | 41 | output_form | "On average the xsim error is brought down from 61 to 0.91." |
| Q340 | 41 | output_form | "In particular, some languages such as Burmese (mya_Mymr) and Irish (gle_Latn) saw the biggest reductions in xsim, with decreases of 93.3 → 0.89 and 92.5 → 0.79, respectively." |
| Q341 | 41 | input_ontology | "There is a large variety of languages which are spoken locally in various regions of Europe. We consider here 10 languages." |
| Q342 | 41 | input_content | "For most of them, we were not able to find meaningful amounts of public bitexts and heavily utilize NLLB-Seed" |
| Q343 | 42 | input_content | "Therefore, we chose to train individual sentence encoders specific to each of these languages and complemented the training data with 2M bitexts in a similar higher-resource European languages." |
| Q344 | 42 | input_content | "Typical examples are Sicilian paired with Italian or Silesian paired with Polish." |
| Q345 | 42 | output_form | "We observe that pairing the minority language with another similar major language yields encoders with very low xsim error rates for most of the languages, and we were able to mine large amounts of bitexts yielding good NMT performance." |
| Q346 | 42 | output_form | "Three languages reach a BLEU score superior to 20 (fur_Latn, lmo_Latn and srd_Latn), and two languages superior to 30 (ltz_Latn and ydd_Hebr)." |
| Q347 | 42 | input_ontology | "We applied a similar strategy for Creole languages." |
| Q348 | 42 | input_ontology | "Linguistically speaking, Creole languages are a possible outcome of a contact situation between languages over a fairly brief period of time (Lent et al., 2022)." |
| Q349 | 42 | input_content | "When training the sentence encoders, we paired each Creole language with a "similar" high-resource language (see Table 11)." |
| Q350 | 42 | input_content | "The sentence encoders have a very low xsim error rate for all languages except Sango (sag_Latn) for which we were not able to identify a similar language with sufficient resources." |
| Q351 | 43 | input_content | "For the former, we were able to crawl 28M sentences of monolingual data, while we have less than 300k for the latter." |
| Q352 | 43 | input_content | "Both have less than ten thousand sentences of existing bitexts which is largely insufficient to train an NMT system." |
| Q353 | 43 | output_form | "We were able to mine more than 7M bitexts for Papiamento which yielded an impressive BLEU score of 40.9, while we only achieve BLEU 4.9 for Kabuverdianu." |
| Q354 | 43 | input_content | "This highlights that the amount of available monolingual data is crucial to make bitext mining successful." |
| Q355 | 43 | input_ontology | "We considered several languages of the Berber family, namely Kabyle (kab_Latn), Tamashek (taq) and Central Atlas Tamazight (tzm)." |
| Q356 | 43 | input_form | "We consider Tamazight written in the Tifinagh script and Tamashek both in Latin and Tifinagh script." |
| Q357 | 43 | input_content | "All are very low-resource languages with barely 10,000 sentences of available bitext, and 72,000 for Kabyle." |
| Q358 | 43 | input_content | "It was also very challenging to collect monolingual data for these Berber languages." |
| Q359 | 43 | output_form | "xsim error rates for Tamashek are above 20% and insufficient amount of monolingual data make it impossible to mine bitext of good quality for Tamashek." |
| Q360 | 43 | input_content | "Tamashek and Tamazight are typical examples of very low-resource languages for which it seems to be very hard to collect written material to support training of machine translation system." |
| Q361 | 43 | input_ontology | "We discuss here 13 languages from this family, and use a single encoder for ten of them." |
| Q362 | 43 | input_ontology | "The languages Fijian, Maori, and Samoan are handled by a separate encoder." |
| Q363 | 43 | output_form | "We observe very low xsim error rates for most of the languages, although several languages have less than hundred thousand sentences of bitexts." |
| Q364 | 43 | input_ontology | "Training all languages together in one specific encoder for this family seems to be very beneficial for these very low-resource languages." |
| Q365 | 43 | input_content | "In addition, we were able to collect several million sentences of monolingual text for most of the languages." |
| Q366 | 43 | output_form | "This gives us optimal conditions for mining and we achieve substantial improvements in the BLEU score compared to training a bilingual NMT system on the public bitexts only." |
| Q367 | 44 | input_ontology | "Among the 200 languages of the NLLB project, 55 are spoken in the African continent, which is more than a quarter of all languages we handle." |
| Q368 | 44 | input_content | "Except for seven languages — Modern Standard Arabic, Afrikaans, Southern Sotho, Swahili, Tswana, Xhosa and Zulu — all are low-resource languages, i.e. with less than one million publicly available sentence pairs." |
| Q369 | 44 | input_content | "Twelve of them even have less than hundred thousand sentence pairs, which we named very low-resource languages." |
| Q370 | 44 | input_content | "In addition, we struggled to curate meaningful amounts of monolingual data." |
| Q371 | 44 | input_content | "Given these facts, training sentence encoders for African languages and mining high quality bitexts turned out to be a major challenge — even in the broader community." |
| Q372 | 44 | output_form | "The average BLEU score over 44 languages increased from 11.0 to 14.8 with help of the mined bitexts." |
| Q373 | 44 | input_form | "We also deployed a new training procedure which combines supervised training, i.e. minimizing the cosine loss between the teacher and student embedding, and unsupervised masked LM training (see left part of Figure 12)." |
| Q374 | 44 | input_form | "This enabled us to benefit from monolingual data during encoder training." |
| Q375 | 44 | output_content | "A detailed description and analysis of our effort is reported in Heffernan et al. (2022)." |
| Q376 | 45 | output_form | "Table 14: xsim Error Rates on FLORES devtest for Amharic and Tigrinya and different training strategies. The specified amount of training data excludes 4M sentences of English for our models." |
| Q377 | 45 | input_form | "In massively multilingual systems, a common approach is to utilize the same SentencePiece vocabulary." |
| Q378 | 45 | input_form | "In our initial experimentation, we re-used the LASER2 teacher 50k vocabulary for all student encoders." |
| Q379 | 45 | input_form | "However, despite upsampling, low-resource languages could be poorly represented in a joint vocabulary." |
| Q380 | 45 | input_form | "We next explore utilizing specific vocabularies for small subsets of languages." |
| Q381 | 45 | input_ontology | "We first explore training an encoder for three Semitic languages: Amharic, Tigrinya, and Maltese." |
| Q382 | 45 | input_form | "We then trained an encoder for Amharic and Tigrinya only, paired with English as in all our experiments, and a specific 8k SentencePiece vocabulary to better support the Ge'ez script." |
| Q383 | 45 | input_content | "Overall, we mined 148 bitexts paired with English which totals to 761 million sentence pairs with an alignment score of at least 1.06." |
| Q384 | 45 | input_content | "Bitexts aligned with English for the remaining languages were taken from CCMatrix (Schwenk et al., 2021b)." |
| Q385 | 45 | input_content | "We also provide 1465 non-English bitext pairs. This corresponds to 302 million sentence pairs. This includes all language pairs among African, Indic and Malayo-Polynesian families, respectively, as well as alignments of all African languages with French." |
| Q386 | 45 | input_content | "We note that for some languages, we are only able to create a small amount of bitext through data mining. The limiting factor is predominantly the lack of monolingual data." |
| Q387 | 45 | input_content | "Many low-resource languages have limited presence on the web, and the data that we curate can be heavily filtered at many stages: language identification, aggressive cleaning of monolingual data, or even poorly aligned bitext." |
| Q388 | 45 | input_content | "Even with our best efforts, those challenges compound, and they can affect certain languages far more than others." |
| Q389 | 45 | input_content | "Further, note that even in our mined bitext, we still end up including some content that is already available from" |
| Q390 | 46 | input_content | "An important final consideration is the web already has machine translated content. For example, many websites may use translation to 'internationalize' their content. A positive is that a large majority of the languages we focus on are not contained in most existing commercial translation services (see Table 1), however as we mine against higher-resource languages, it is likely our mined datasets contain translated content." |
| Q391 | 46 | input_content | "While we performed our due diligence on deployments of all licensed datasets, the ownership of low-resource language data remains an open debate." |
| Q392 | 46 | output_content | "In our interview study, many low-resource stakeholders express that sharing language access might in fact be a necessary trade-off for technological advancement." |
| Q393 | 46 | input_content | "Even though we deploy many low-resource language datasets, ownership ultimately belongs to the speakers of these languages." |
| Q394 | 46 | input_content | "We describe our methodology for automatically creating aligned translation training data for low-resource languages. We face significant challenges, as bitext data to train sentence encoders such as LASER and monolingual data to mine in is extremely scarce." |
| Q395 | 46 | input_ontology | "we develop (1) a high-quality language identification system for over 200 languages that outperforms publicly available LIDs in both Flores-200 and web domains, (2) a detailed, documented monolingual dataset curation and cleaning pipeline, and (3) a teacher-student based multilingual sentence encoder training methodology that enables transfer to extremely low-resource languages with minimal supervised bitext. These contributions combine to create over 1.1 billion new sentence pairs of training data for 148 languages." |
| Q396 | 46 | input_content | "We are releasing all the code that was used to train the LID model, and run the monolingual sentence splitting and filtering. We are also releasing the mining code, under an open source license, with tools to run mining with our open-sourced LASER encoders." |
| Q397 | 47 | input_ontology | "Existing research in massively multilingual machine translation has been predominantly restricted to about 100 languages, which represent only a fraction of globally written languages (Arivazhagan et al., 2019; Fan et al., 2020; Zhang et al., 2020)." |
| Q398 | 47 | output_form | "Some works have extended beyond (Mueller et al., 2020; Siddhant et al., 2022), but critically lack reliable performance evaluation." |
| Q399 | 47 | output_form | "Despite much research, the translation quality for languages with low volumes of data is typically poor." |
| Q400 | 47 | input_content | "Further, adding extremely low-resource languages beyond 100 is very challenging because there is often very little existing good quality available bitext, and even large scale bitext mining (Schwenk et al., 2021b) can struggle to create sufficiently large datasets (see Section 5.3)." |
| Q401 | 47 | input_content | "Data often varies widely in available volume across languages, creating imbalance between different language directions." |
| Q402 | 47 | input_content | "This complicates massively multilingual training, as some language directions have begun overfitting while others have not yet even converged." |
| Q403 | 47 | input_ontology | "We develop several novel techniques that tackle the major challenges of low-resource translation, such as training models with sufficient capacity to represent 200+ languages while adjusting to variable data capacity per language pair." |
| Q404 | 47 | input_ontology | "These involve (1) conditional compute models to minimize interference between unrelated language directions, (2) studying the best self-supervision strategies on monolingual data, and (3)" |
| Q405 | 48 | input_ontology | "We model multilingual neural machine translation as a sequence-to-sequence task, where we condition on an input sequence in the source language with an encoder and generate the output sequence in the expected target language with a decoder (Bahdanau et al., 2015)." |
| Q406 | 48 | output_ontology | "We train to maximize the probability of the translation in the target language T, given the source sentence S, the source language ℓs, and the target language ℓt, i.e., P(T\|S, ℓs, ℓt)." |
| Q407 | 48 | input_form | "To tokenize our text sequences, we train a single SentencePiece (SPM) (Kudo and Richardson, 2018) model for all languages." |
| Q408 | 48 | input_content | "We sample a total of 100M sentences from primary bitext data." |
| Q409 | 48 | input_form | "To ensure low-resource languages are well-represented in the vocabulary, we downsample high-resource and upsample low-resource languages with a sampling temperature of 5 (Arivazhagan et al., 2019)." |
| Q410 | 48 | input_form | "Vocabulary size is a critical hyperparameter in multilingual translation models involving low-resource languages (Oladipo et al., 2022; Rajab, 2022)." |
| Q411 | 48 | input_form | "The vocabulary size of our trained SPM model is 256,000." |
| Q412 | 48 | input_ontology | "Our sequence-to-sequence multilingual machine translation model is based on the Transformer encoder-decoder architecture (Vaswani et al., 2017)." |
| Q413 | 48 | input_form | "Note that we prefix the source sequence with the source language, as opposed to the target language as previously done in several works (Arivazhagan et al., 2019; Johnson et al., 2017)." |
| Q414 | 48 | input_ontology | "This is primarily because we prioritize optimizing zero-shot performance of our model on any pair of 200 languages at a minor cost to supervised performance." |
| Q415 | 48 | input_ontology | "Empirically, we find zero-shot performance to be negatively affected when conditioning the encoder on" |
| Q416 | 49 | input_ontology | "We construct a multilingual machine translation benchmark such that it is representative of our final benchmark on 200+ languages." |
| Q417 | 49 | input_ontology | "We choose a representative sub-sample of 53 out of 202 languages and a total of 110 translation directions (see Table 51 in the appendix)." |
| Q418 | 49 | input_ontology | "These consist of 45 directions out of English (aggregated as eng_Latn-xx), 45 directions into English (aggregated as xx-eng_Latn) and 20 non-English directions (aggregated as xx-yy)." |
| Q419 | 49 | input_ontology | "In terms of resource level, there are 40 high-resource and 70 low-resource directions (see Table 1 and Table 51)." |
| Q420 | 49 | input_ontology | "Out of 70 low-resource directions, 22 are very low-resource, i.e., have less than 100K training examples." |
| Q421 | 49 | input_content | "The dataset is composed of publicly available bitext in all 110 language directions (see Section 8.1.2) and large scale mined data (see Section 5.3)" |
| Q422 | 49 | input_form | "Ablation Dataset Counts depicting the amount of training data across all language pairs, ranking from 39,992 to 18.7 million sentence pairs." |
| Q423 | 50 | input_content | "There are a total of 864M examples in this benchmark." |
| Q424 | 50 | input_content | "The highest resource language pair has 186M examples and the lowest resource language pair has 40K examples, thus representing the extreme skew characteristic of the final dataset with 202 languages." |
| Q425 | 50 | input_content | "Figure 15 shows the data distribution over language pairs sorted by the example count per pair." |
| Q426 | 50 | input_ontology | "We call this dataset our ablation dataset and use this throughout all experiments in this section." |
| Q427 | 50 | input_content | "For this ablation dataset, we only include English-centric data to manage experimental iteration speed." |
| Q428 | 50 | input_ontology | "A massively multilingual translation model is trained on several translation directions at once, utilizing the same shared model capacity." |
| Q429 | 50 | input_ontology | "This can lead to beneficial crosslingual transfer between related languages at the risk of increasing interference between unrelated languages." |
| Q430 | 50 | input_ontology | "Sparsely Gated Mixture of Experts (MoE) models are a type of conditional compute models that activate a subset of model parameters per input, as opposed to dense models that activate all model parameters per input." |
| Q431 | 50 | input_ontology | "We follow the Top-k-Gating algorithm of Lepikhin et al. (2020) and dispatch each token to at most k = 2 experts." |
| Q432 | 50 | input_ontology | "We always choose the top 2 scoring experts per token, and do not add randomization to the choice of the second expert." |
| Q433 | 51 | input_ontology | "The Transformer encoder-decoder model, supplemented with MoE layers and their respective gating networks, learns to route input tokens to the corresponding top-2 experts by optimizing a linearly weighted combination of label-smoothed cross entropy (Szegedy et al., 2015) and an auxiliary load balancing loss (Shazeer et al., 2017)." |
| Q434 | 51 | output_form | "This additional loss term (LB) pushes the tokens to be uniformly distributed across experts and is evaluated as: LB = E · ∑ E e=1 fe pe, pe = 1/T · ∑ T t=1 Gt e, where fe is the fraction of tokens routed to the eth expert, as their first choice, through Top-k-Gating, and pe is the average routing probability to that expert over the T tokens in the mini-batch." |
| Q435 | 51 | input_ontology | "In the rest of this section, we first detail how we train vanilla Sparsely Gated MoE models for multilingual machine translation on our benchmark and show how they compare to dense models." |
| Q436 | 51 | input_ontology | "We then discuss why these vanilla Sparsely Gated MoE models are suboptimal for low-resource language pairs (Section 6.2.1)." |
| Q437 | 51 | input_ontology | "We propose in Section 6.2.2 a series of architectural changes that significantly improve the performance on low-resource language pairs with MoE models." |
| Q438 | 52 | input_ontology | "We train a baseline dense Transformer encoder-decoder model with 1.3B parameters with model dimension 1024, FFN dimension 8192, 16 attention heads, 24 encoder layers and 24 decoder layers." |
| Q439 | 52 | input_ontology | "Next, we train a corresponding Sparsely Gated MoE model by replacing the dense FFN sublayer with an MoE sublayer in every alternate" |
| Q440 | 52 | output_form | "We report averages in each set of directions: eng_Latn-xx, xx-eng_Latn and xx-yy as all." |
| Q441 | 52 | output_form | "For eng_Latn-xx and xx-eng_Latn we breakdown the pairs by resource level: high-resource (high), low-resource (low) and very low resource (v.low)" |
| Q442 | 52 | output_form | "We see that a vanilla MoE model does not outperform the corresponding 1.3B dense model on the ablation benchmark." |
| Q443 | 52 | output_form | "On adding overall dropout, we see a significant improvement in all directions on MoE models." |
| Q444 | 52 | output_form | "At smaller computational cost per update (615M), MoE with overall dropout shows larger gains." |
| Q445 | 52 | input_ontology | "The motivation behind sparsely activating expert subnetworks in an MoE model is to allow different parameters to model different aspects of the input space." |
| Q446 | 52 | input_ontology | "We hypothesize that the added expert capacity should help higher resource language pairs that might otherwise be constrained to share the same dense model capacity with many other language pairs." |
| Q447 | 52 | input_ontology | "We also hypothesize that with a massive number of translation directions, the added expert capacity would reduce interference, thus benefiting tasks of all resource levels." |
| Q448 | 53 | input_ontology | "Each MoE sublayer has 64 experts (close to the number of languages in the benchmark, i.e., 53) and routes input tokens to the top-2 expert FFN sublayers in the MoE layer as in Lepikhin et al. (2020)." |
| Q449 | 53 | input_form | "All models are trained for 100k updates with an effective batch size of 1M tokens per update." |
| Q450 | 53 | output_form | "For dense models, the objective function is label-smoothed cross-entropy (ε = 0.1) (Szegedy et al., 2015), and for MoE models, the objective function is a weighted sum of label-smoothed cross-entropy and the load balancing loss (Equation (9)) with weights 1.0 and 0.01, respectively." |
| Q451 | 53 | input_form | "We optimize with Adam (Kingma and Ba, 2015) using (β1, β2, ε) = (0.9, 0.98, 10−6)." |
| Q452 | 53 | input_form | "We linearly increase the learning rate up to 0.004 through 8000 warmup updates, then follow the inverse square root learning rate schedule." |
| Q453 | 53 | input_form | "For Top-2-Gating, we set the expert capacity to 2 × T/E, i.e., we enforce that each expert processes, at most, 2 × T/E tokens, where T is the number of tokens in the mini-batch and E is the number of experts." |
| Q454 | 53 | input_form | "During generation, we set the capacity to T so that all tokens can be routed to whichever expert they choose." |
| Q455 | 53 | output_form | "We use the chrF++ metric to compare the model performance (see Section 7.1)." |
| Q456 | 53 | output_form | "We see 1+ chrF++ score improvements on all subsets except for very low resource pairs (v.low) and non-English pairs (xx-yy)." |
| Q457 | 53 | output_form | "Adding overall dropout (sweeping over pdrop∈{0.1, 0.2, 0.3}) significantly improves the performance of MoE-64 in both the 615M and 1.3B variants." |
| Q458 | 53 | input_content | "We hypothesize two potential reasons for this: (1) we use a temperature of 1.0 for sampling, i.e., we do not upsample datasets from low-resource pairs." |
| Q459 | 53 | input_content | "As we increase computational cost per update, the propensity for low or very low-resource pairs to overfit increases thus causing performance to deteriorate." |
| Q460 | 53 | input_content | "We observe in the case of eng_Latn-kon_Latn, a very low-resource pair, that the model continues to face significant overfitting when trained for 100k updates." |
| Q461 | 53 | input_content | "This is unsurprising, as iterating over a small training set with large capacity causes overfitting." |
| Q462 | 54 | input_content | "Although overall dropout is sufficient to regularize dense models, MoE models with overall dropout still significantly overfit on low-resource pairs as seen in Figure 17." |
| Q463 | 54 | input_content | "MoE models enable specialized expert capacity to be activated based on the input token. However, with increased capacity, the learned token-expert assignment can cause the models to overfit, especially on low-resource translation directions." |
| Q464 | 54 | input_ontology | "In this proposed regularization strategy, we mask the expert output for a random fraction (peom) of the input tokens." |
| Q465 | 54 | input_ontology | "For input tokens with dropped expert outputs, the first and/or second expert is effectively skipped." |
| Q466 | 54 | input_ontology | "Note that although this masking will zero out some combination weights Gt,e in Equation (13), it will not affect the weights used in the load balancing loss in Equation (9)." |
| Q467 | 54 | input_ontology | "We compare EOM to Gating Dropout (Liu et al., 2022), a strategy for reducing cross-machine communication in MoE layers which also has a regularizing effect." |
| Q468 | 55 | input_ontology | "Figure 18: Illustration of MoE Expert Output Masking in contrast to overall dropout for MoE layers: a color represents a token, and each token is dispatched to two experts (Top-k-Gating). Faded colors correspond to dropped units or masked outputs." |
| Q469 | 55 | input_ontology | "skips the All-to-All communication between GPUs with probability pgd, routing tokens to the local experts instead." |
| Q470 | 55 | input_ontology | "Final Output Masking (FOM). A simpler alternative to EOM would be to mask the combined expert output for a random fraction of tokens, i.e., after the last stage in Figure 18b. We denote with pfom the fraction of tokens masked with this regularization method. Note that this type of masking is more generic as it can be applied to dense models as well — in testing it here, we validate the advantages of using an MoE-specific masking i.e. MoE Expert Output Masking." |
| Q471 | 55 | input_ontology | "Conditional MoE Routing (CMR). Instead of randomly dropping a proportion of activations or masking expert outputs, in this section, we consider the option of letting the model decide, and learn, which tokens need the extra capacity or specialization of MoE layers, and which tokens are better routed to a limited-capacity shared layer." |
| Q472 | 55 | input_ontology | "Inspired by Zhang et al. (2021)'s CLSR-Gate, we design Conditional MoE Routing layers (CMR for short). As depicted in Figure 19, we augment MoE layers with a binary gate that decides the weights associated with two branches of the computational graph: (1) a shared dense FFN sublayer (FFNshared) and (2) an MoE layer with its own E expert FFN sublayers." |
| Q473 | 55 | input_ontology | "Unlike Zhang et al. (2021)'s CLSR-Gate, our CMR branches are FFN sublayers (dense or sparsely gated MoE) and not linear projections. Furthermore, our CMR does not have language-specfic parameters, but learned routing to experts using an MoE layer." |
| Q474 | 55 | output_form | "The CMR gate weights are learned by optimizing translation accuracy under a budget constraint p." |
| Q475 | 56 | input_ontology | "Our baseline is a Sparsely Gated MoE model with model dimension 1024, FFN dimension 8192, 16 attention heads and 24 layers." |
| Q476 | 56 | input_ontology | "We have 64 experts per MoE layer and we place an MoE layer in every alternate Transformer layer of the model (fMoE=2)." |
| Q477 | 56 | input_ontology | "We compare this unregularized baseline to a variant with an overall dropout rate of 0.3 (pdrop=0.3), best performing after a sweep of pdrop ∈ {0.1, 0.2, 0.3}." |
| Q478 | 56 | output_form | "For EOM, we sweep over the values of (pdrop, peom) ∈ {0.1, 0.2, 0.3}2 and choose the best out of 9 variants based on the average chrF++ score on the validation set." |
| Q479 | 56 | output_form | "For FOM, we set pdrop=0.3 and sweep over pfom ∈ {0.1, 0.2, 0.3} and choose the best out of the variants based on the average chrF++ score on the validation set." |
| Q480 | 56 | input_ontology | "For CMR, we train the baseline augmented with a shared FFN sublayer with the same dimensions as the rest of the model." |
| Q481 | 56 | output_form | "We sweep over the values of (pdrop, pcmr) ∈ {0.1, 0.2, 0.3}2 and choose the best out of 9 variants based on the average chrF++ score on the validation set." |
| Q482 | 56 | output_form | "Initial experiments on other benchmarks show that the value of p = 0.8 achieves the desirable trade-off of improving the performance on low-resource pairs without hindering the performance on high-resource ones." |
| Q483 | 56 | output_form | "From our initial experiments, we find that the addition of the auxiliary budget constraint LCMR and pcmr are important for improving accuracy." |
| Q484 | 57 | output_form | "For each model, we report chrF++ averages on the validation set in 3 groups of directions: eng_Latn-xx, xx-eng_Latn and xx-yy, broken down w.r.t. to resource levels: high, low and very low (v.low) for eng_Latn-xx and xx-eng_Latn." |
| Q485 | 57 | output_form | "In terms of alleviating the overfitting issue, the last column of Figure 17 shows that EOM leads to better regularization and less overfitting on low-resource tasks compared to overall dropout." |
| Q486 | 57 | output_form | "In terms of translation quality, and as shown in Table 16, we observe gains of +0.4 chrF++ across all pairs into English and +0.6 chrF++ across non-English pairs for MoE EOM compared to vanilla MoE with overall dropout." |
| Q487 | 57 | output_form | "Gains are larger on low and very low-resource languages — for out of English, there are improvements of +0.6 and 0.9 chrF++ with EOM." |
| Q488 | 57 | input_ontology | "The comparison between EOM and FOM proves that masking before combining the expert outputs is more beneficial than simply masking tokens in the final output." |
| Q489 | 57 | output_form | "Our hypothesis is that this gain in performance stems from EOM strengthening the residual connection surrounding the MoE layer and reducing co-adaptation between selected top-2 experts, as well as co-adaptation between experts and the subsequent layers of the model." |
| Q490 | 57 | output_form | "For CMR, we see +0.8 chrF++ across all pairs into English and +0.7 chrF++ across non-English pairs." |
| Q491 | 57 | output_form | "Similarly, the improvements are larger for low and very low-resource languages, with +0.7 and +1.0 chrF++ respectively." |
| Q492 | 57 | output_form | "CMR is computationally more expensive by 18-25% at training time because of the additional shared FFN layer at the level of each MoE layer in the model." |
| Q493 | 57 | output_form | "Given the additional computational overhead, we use the simpler MoE EOM strategy." |
| Q494 | 57 | output_form | "For Gating Dropout (Liu et al., 2022), we sweep over the values of (pdrop, pgd) ∈ {0.1, 0.2, 0.3}2 and choose the best out of 9 variants based on the average chrF++ score on the validation set." |
| Q495 | 58 | input_ontology | "To reduce overfitting on low-resource language pairs further, we next explore alternative means of adding additional regularization. We try a straightforward curriculum of introducing these low-resource language pairs in phases during model training. The language pairs that empirically overfit within K updates are introduced K updates before the end of training." |
| Q496 | 58 | input_ontology | "We train MoE-64 models with fMoE=2 for a total of T updates (see Section 6.2.1 for details of the base architecture). To derive the phases of the curriculum, we first train a regular model, i.e., without curriculum, then we partition language pairs into n buckets {b0, b1, . . . , bn−1} based on when they start to overfit." |
| Q497 | 58 | input_ontology | "Based on observed overfitting patterns, we introduce pairs during training in n = 3 phases - we set T = 100k, k0 = 100k, k1 = 40k, k2 = 20k, so b0 is introduced first, b1 is introduced at step T − 40k, and b2 is introduced at step T − 20k." |
| Q498 | 58 | input_ontology | "We compare to the baseline of an MoE model with overall dropout 0.3 without curriculum learning, i.e. introducing all pairs at the start of training and training for 100k updates." |
| Q499 | 58 | output_form | "As shown in Table 17, for vanilla MoE, when translating out of English (eng_Latn-xx), there is an average improvement of +0.6 chrF++ on low-resource directions (low) and a +0.8 chrF++ improvement on very low-resource (v.low) directions." |
| Q500 | 58 | output_form | "There is, however, no significant improvement on high-resource directions (high) or translation into English (xx-eng_Latn), most likely because there is no overfitting on these directions in the baseline." |
| Q501 | 58 | output_form | "For MoE EOM, training with a curriculum actually hurts performance across eng_Latn-xx, xx-eng_Latn and xx-yy." |
| Q502 | 58 | output_form | "Our analysis indicates that overfitting on the ablation dataset is already reduced by EOM, which has a higher fraction of language pairs with their best checkpoint by validation perplexity at ≥ 70000 steps." |
| Q503 | 58 | output_form | "We hypothesize that adding a curriculum on top of EOM is not needed for the ablation dataset." |
| Q504 | 58 | output_form | "However, results in Table 29 show that with the full dataset and larger model, combining curriculum learning and EOM improves performance, especially on low and very low-resource language pairs." |
| Q505 | 58 | input_ontology | "MoE theoretically enables models to specialize expert capacity for different tasks, but what do these models actually learn?" |
| Q506 | 58 | input_form | "We now take a closer look at the routing of tokens to experts in MoE layers at different points of the encoder-decoder architecture. We take an MoE model (E=64, pdrop=0.3, peom=0.2) trained on our ablation dataset and do a forward pass on Flores-200 dev set data in teacher-forcing mode, i.e., we feed the true target prefix to predict the next target token." |
| Q507 | 58 | output_form | "For each task (language pair), we log the routing decisions prior to Top-k-Gating, and depending on whether it is an encoder layer or a decoder layer, we average the routing vectors across multiple language pairs to estimate language-level routing vectors." |
| Q508 | 59 | output_form | "Table 17: Curriculum Learning Results demonstrate that for vanilla MoE, training on a curriculum reduces overfitting, particularly for eng_Latn-xx low and very low resource pairs. For MoE EOM, a curriculum does not help." |
| Q509 | 59 | input_form | "where T<lang> is the set of all tokens in <lang>, source-side for encoder layers and target-side for decoder layers." |
| Q510 | 59 | output_form | "The similarity heatmaps demonstrate that in late decoder layers (see Figure 20d), the languages are being separated, i.e., dispatched to different set of experts." |
| Q511 | 59 | output_form | "Languages within the same family are highly similar in their choice of experts, i.e., the late decoder MoE layers are language-specific." |
| Q512 | 59 | output_form | "This is particularly the case for languages in the Atlantic-Congo family (the rows/columns from cjk to yor) and some pairs like {snd_Arab, urd_Arab} in the Indo-European family or {yue_Hant, zho_Hans} in the Sino-Tibetan family." |
| Q513 | 59 | output_form | "To a lesser extent, the early encoder MoE layers (see Figure 20a), also show some language-expert specialization." |
| Q514 | 59 | output_form | "The late encoder MoE layers and the early decoder MoE layers (see Figure 20b and Figure 20c) seem to be language-agnostic." |
| Q515 | 59 | output_form | "In Figure 21, we visualize the vectors of expert-distribution per language G<lang> (Equation (13)) using UMAP (McInnes et al., 2018)." |
| Q516 | 59 | output_form | "Separation of languages is more discernible in the decoder's last layer (last column of Figure 21) particularly along language family lines, e.g., Atlantic-Congo in green and Dravidian in pink." |
| Q517 | 59 | input_content | "For low-resource languages, there is generally limited or no bitext data available." |
| Q518 | 59 | input_content | "In cases where bitext data is publicly available, the domain of the available data could be narrow (e.g. religious texts) or the bitext data could be noisy." |
| Q519 | 59 | input_content | "In comparison, there is relatively more abundant monolingual data available in low-resource languages." |
| Q520 | 59 | input_ontology | "In addition to bitext mining detailed in Section 5.3, another way of leveraging this monolingual data is via incorporating a self-supervised task into the process of training a multilingual machine translation model (Bapna et al., 2022; Chi et al., 2021; Ma et al., 2021)." |
| Q521 | 60 | output_form | "Cosine Similarity Scores between languages of the ablation dataset at different layers of the encoder-decoder architecture. The similarity is measured w.r.t. the gating decisions (expert choice) per language (source-side in the encoder and target-side in the decoder)" |
| Q522 | 61 | input_ontology | "We first study the effect of the choice of the self-supervised task: (1) language modeling objective, (2) denoising autoencoder objective (Liu et al., 2020), or (3) the combination of both." |
| Q523 | 61 | input_ontology | "We follow that up with studying the optimal curriculum when combining the task of self-supervised learning (SSL) on monolingual data along with the task of training on multilingual machine translation (MMT) on bitext data." |
| Q524 | 61 | input_ontology | "We use the recommendations from this study to decide on our self-supervision strategy for our final model on 200 languages." |
| Q525 | 61 | input_content | "There are different ways of incorporating self-supervision on monolingual data in the training procedure of multilingual machine translation models." |
| Q526 | 61 | input_content | "Traditionally, self-supervised learning in NLP takes the form of pretraining with a self-supervised objective on monolingual data, followed by finetuning on the task-specific supervised data." |
| Q527 | 61 | input_content | "Another strategy is to consider SSL on monolingual data and MMT on bitext data as separate tasks in a multi-task learning setup, where examples from both tasks are present in every batch during training." |
| Q528 | 61 | input_content | "Our third strategy is a combination of the first two strategies. We can first pretrain with the multi-task setting of self-supervision on monolingual data and multilingual machine translation on bitext data, followed by finetuning on multilingual machine translation alone." |
| Q529 | 62 | input_ontology | "There are different self-supervised objectives we can use on monolingual data." |
| Q530 | 62 | input_ontology | "We follow Liu et al. (2020) and use a Transformer encoder-decoder architecture which is the same architecture used for multilingual machine translation." |
| Q531 | 62 | input_ontology | "We set the target to be a sentence from the monolingual corpus. We set the source to be a noised version of the target monolingual sentence. We mask random spans of text from the target sentence. Rather than always replacing the masked token with the mask token (<mask>), with a specified probability, we replace the masked token with a random token from the vocabulary." |
| Q532 | 62 | input_ontology | "The SSL objective here is to maximize the likelihood of predicting the target given the source which is a noised version of the target." |
| Q533 | 62 | input_ontology | "Past work has shown some success with initializing components of a machine translation model with a pretrained decoder Transformer language model. So, we set up the language modeling task in a seq2seq setting where the source is empty and the target is a sentence from a monolingual corpus." |
| Q534 | 62 | input_ontology | "The SSL objective here is to maximize the likelihood of predicting the target i.e. the causal language modeling objective." |
| Q535 | 62 | input_content | "In our setup, we use the multilingual denoising autoencoder objective for self-supervision on the multilingual text corpus for languages in our ablation benchmark." |
| Q536 | 62 | output_form | "Our baseline is a dense 1.3B model trained for 100K updates on the MMT task with a sampling temperature of 1.0." |
| Q537 | 62 | output_form | "We train the SSL task variants with the same architecture and sampling temperature for 200K updates each to ensure that SSL task variants are exposed to as much multilingual parallel data as the baseline." |
| Q538 | 62 | input_content | "We hope to find the best variant that improves the performance on low-resource pairs which do not have sufficient parallel bitext data but relatively abundant monolingual data." |
| Q539 | 62 | input_ontology | "We consider three options: Pretraining on SSL, followed by finetuning on MMT (DAE⇒MMT). We train on SSL for the first 100K updates, followed by finetuning on MMT task for the next 100K updates. We use a sampling temperature of 1.25 for SSL pretraining." |
| Q540 | 62 | input_ontology | "Multitask training on SSL and MMT (DAE+MMT). We combine the training examples for SSL and MMT and train the model for 200K updates on a combination of both tasks." |
| Q541 | 62 | input_ontology | "Multitask training on SSL and MMT, followed by finetuning on MMT (DAE+MMT ⇒ MMT). We first perform multitask training on SSL and MMT for 150K updates, followed by finetuning on MMT only for 50K updates." |
| Q542 | 62 | output_form | "First, we see that pretraining on SSL, followed by finetuning on MMT (DAE ⇒ MMT) hurts performance (-0.7 chrF++ on eng_Latn-xx, -1.2 chrF++ on xx-eng_Latn)" |
| Q543 | 63 | input_ontology | "Table 18: Effect of SSL Curriculum. We find DAE+MMT training jointly to be the most effective strategy." |
| Q544 | 63 | input_ontology | "Multi-task training on SSL and MMT (DAE+MMT) shows +0.4 chrF++ on low-resource eng_Latn-xx pairs and +1.1 chrF++ on very low-resource eng_Latn-xx pairs, thus confirming that the additional monolingual data in the low-resource target languages is useful when presented in a multitask framework." |
| Q545 | 63 | output_form | "Similarly, we see +1.3 and +1.9 chrF++ improvements on low and very low-resource pairs in xx-eng_Latn directions as well as +1.1 chrF++ on xx-yy pairs." |
| Q546 | 63 | input_content | "We hypothesize that we observe stronger performance translating into English as there is an abundance of very high-quality English monolingual data which is critical for SSL." |
| Q547 | 63 | input_ontology | "This indicates that when SSL and MMT are jointly trained in a multi-task setup, they do not suffer from interference that could be countered by the final stage of finetuning purely on the final task (MMT)." |
| Q548 | 63 | input_ontology | "Experimental Setup. We train all SSL task variants in this section in a multitask learning setup of training SSL and MMT tasks together, because that is the best performing curriculum as demonstrated in Section 6.3.3." |
| Q549 | 63 | input_ontology | "Our baseline is a dense 1.3B model trained for 100K updates and SSL models trained for 200K updates." |
| Q550 | 63 | input_ontology | "We train the SSL variants with the same architecture and sampling temperature for 200K updates each to ensure that SSL variants are exposed to as much supervised bitext data as the baseline." |
| Q551 | 63 | input_ontology | "We hope to find the best self-supervised objective that improves the performance on low-resource pairs which do not have enough bitext data, and relatively abundant monolingual data." |
| Q552 | 63 | input_ontology | "We consider three options. (1) Denoising Autoencoder (DAE), (2) Causal Language Modeling (LM), and (3) the combination of both (DAE+LM)." |
| Q553 | 63 | output_form | "First, we observe that the LM task as an SSL objective results in a decline in performance compared to the baseline of training MMT alone." |
| Q554 | 63 | output_form | "One hypothesis is that self-supervision on the encoder-decoder attention plays an important role, and this is not" |
| Q555 | 64 | output_form | "We find training MMT+DAE the most effective compared to adding the LM task." |
| Q556 | 64 | output_form | "The results show a decline in performance compared to using only the DAE task." |
| Q557 | 64 | output_form | "This suggests that there might be some interference between the different tasks, which reduces the overall performance when combining them." |
| Q558 | 64 | input_ontology | "Recent works (Bapna et al., 2022; Chi et al., 2021; Ma et al., 2021) have demonstrated that denoising and similar self-supervised objectives are very useful for improving model performance when trained along with machine translation task in a multitask setup." |
| Q559 | 64 | input_ontology | "In our work, we try two SSL objectives, DAE and LM and experimented with different combinations of both along with the MMT task." |
| Q560 | 64 | output_form | "We observed that only DAE performs best when trained with MMT." |
| Q561 | 64 | output_form | "Benefits of the LM task in a multitask setup with MMT is still not evident and future work could reveal a deeper understanding regarding this finding." |
| Q562 | 64 | input_ontology | "We also study different curriculum learning strategies with the SSL tasks and find that multitask learning of DAE and MMT is usually the best setup, similar to findings in (Chi et al., 2021; Ma et al., 2021)." |
| Q563 | 64 | input_content | "Another way of leveraging monolingual data is through backtranslation (Edunov et al., 2018; Sennrich et al., 2016a), a technique which involves creating parallel corpora that are noisy on the source side via machine translation." |
| Q564 | 64 | input_content | "However, when it comes to low-resource languages, the machine translation models that are used to generate backtranslation data are often not good enough, and hence the generated data is often noisy and degenerate." |
| Q565 | 64 | input_content | "Hoang et al. (2018) proposed iterative backtranslation to offset this, as better models are" |
| Q566 | 65 | input_content | "Since the aim is to use the best possible models to generate backtranslated data, this means using massively multilingual models, which are computationally intensive to run both at training and inference time." |
| Q567 | 65 | input_content | "Backtranslation is a source of synthetically augmented data for translation models." |
| Q568 | 65 | input_content | "We contrast it with two other sources of data: (1) primary bitext data, i.e. high-quality parallel corpora that have been human-translated, and (2) mined bitext data, i.e. parallel corpora obtained via mining (see Section 5.3)." |
| Q569 | 65 | input_content | "Backtranslation relies on the availability of an initial translation system, a teacher, to produce a noisy parallel corpus from a monolingual corpus." |
| Q570 | 65 | input_content | "However, these neural systems are often thought to be data-inefficient when compared with traditional phrase or rule based statistical machine translation (Koehn and Knowles, 2017) models." |
| Q571 | 65 | input_content | "We will therefore distinguish four different sources of data in the following experiments, one primary and three augmented sources: human-translated data; mined data; backtranslated data via multilingual neural machine translation; and backtranslated data via statistical machine translation." |
| Q572 | 65 | input_content | "NLLB-Seed: our professionally-translated seed datasets as described in Section 4.2." |
| Q573 | 65 | input_content | "PublicBitext: publicly available parallel corpora. These datasets may be human-translated but are often automatically aligned." |
| Q574 | 65 | input_content | "Primary: the combination of the above two sources." |
| Q575 | 65 | input_content | "Mined: mined data as described in Section 5.3." |
| Q576 | 65 | input_content | "MmtBT: backtranslations obtained via a 1.3B-parameter dense multilingual neural model." |
| Q577 | 65 | input_content | "SmtBT: backtranslations obtained via a series of bilingual MOSES models (Koehn et al., 2007) trained on Primary and Mined data. The optimal model hyperparameters were chosen via Flores-200 validation data." |
| Q578 | 65 | input_form | "First, we study the effect of using MmtBT in addition to Primary and Mined data. We use a dense 1.3B model and train on two data setups, namely Primary and Primary+Mined." |
| Q579 | 65 | input_form | "We then use the model trained on the Primary+Mined dataset and generate backtranslation data for all the English-centric pairs in the dataset." |
| Q580 | 65 | input_form | "In the next experiment, we use the exact same model setup and train on a dataset comprising Primary+Mined+MmtBT. Our objective here is to observe the benefits of backtranslation over Primary+Mined." |
| Q581 | 66 | input_content | "Table 20: Dataset Characteristics of the sources we compare in this section. Of these datasets, NLLB-Seed is by far the smallest. For low-resource languages, PublicBitext is often extremely limited. Mined, MmtBT, and SmtBT are limited only by the amount of available monolingual data and the quality of the models used to produce them." |
| Q582 | 66 | output_form | "the models for 200,000 updates and compare the best checkpoints on the Flores-200 development set using chrF++." |
| Q583 | 66 | input_ontology | "In the second set of experiments, we try to understand the benefits of adding an additional source of backtranslated data, SmtBT. For this, we train bilingual statistical machine translation (SMT) models on Primary+Mined bitexts. We compare the performance of these models against the multilingual machine translation (MMT) model trained on the same data, and pick the directions where the SMT models are either better or comparable to the MMT models. For the directions we pick, we generate backtranslation data using the SMT teacher models." |
| Q584 | 66 | input_ontology | "In Table 21, we report the performance of the baseline model using only Primary data, and then the other three models trained by incrementally augmenting the training data with the Mined, MmtBT, and SmtBT datasets. We observe that the highest performance is achieved when using all sources of data. Despite recent advances which cast into doubt the supposed data inefficiency of neural machine translation (Sennrich and Zhang, 2019), we see that using SMT as a source of backtranslation still leads to improvements for very low-resource directions." |
| Q585 | 66 | output_form | "Table 21: Comparison of aggregate Model Performance trained on Different Data Combinations, evaluated on Flores-200 dev for ablation dataset directions. We observe that adding SmtBT data improves over the +Mined+MmtBT and overall gives the best performance across all language directions and resource level types." |
| Q586 | 67 | output_form | "Table 22: Average Performance of Teacher Backtranslation Models, evaluated on Flores-200 dev for the subset of backtranslated directions where both methods were used." |
| Q587 | 67 | output_form | "In Table 22 the MMT teacher is, as expected, outperforming traditional SMT on all but a few directions." |
| Q588 | 67 | output_form | "Although the average SMT performance might be low, we hypothesize that the combination of different, complementary sources of noise is the reason why its addition is still beneficial to the overall performance of the model." |
| Q589 | 67 | input_form | "Tagged backtranslation (Caswell et al., 2019) is a technique to help the model discern between the different sources of data it is being exposed to during training." |
| Q590 | 67 | input_form | "This is achieved by pre-pending special tokens to backtranslated training examples, and has been shown to boost performance by helping the model distinguish noisy data and avoid overfitting on it (Marie et al., 2020)." |
| Q591 | 67 | input_form | "In the experiments of the previous section we used an extended tagging scheme, using special tokens for each of the three data sources: <MINED_DATA> for Mined, <MMT_BT_DATA> for MmtBT and <SMT_BT_DATA> for SmtBT." |
| Q592 | 67 | input_form | "We train MMT models on the full dataset made up of Primary, Mined, MmtBT and SmtBT, but ablate different tagging schemes." |
| Q593 | 67 | input_form | "The no tags setting does not use any tags at all, the single tag setting uses the same tag for Mined, MmtBT and SmtBT." |
| Q594 | 67 | input_form | "Finally the finegrained tags setting uses separate tags for Mined, MmtBT and SmtBT." |
| Q595 | 67 | output_form | "The results in Table 23 demonstrate the benefits of using finegrained tags." |
| Q596 | 67 | output_form | "This provides further evidence to support the hypothesis of Caswell et al. (2019) that tagging is useful to help the model distinguish between synthetic and natural data." |
| Q597 | 67 | output_form | "It also suggests that signaling the specific nature of synthetic data can further boost performance." |
| Q598 | 67 | input_content | "For a considerable number of the low-resource languages examined in this work, the parallel corpora which are publicly available for research often have only a few thousand sentences." |
| Q599 | 67 | input_content | "They frequently come from sources with a highly specific domain such as scripture, and the level of quality assurance is often unclear." |
| Q600 | 68 | output_form | "We compare models trained on the ablation dataset using no tags, a single tag, and finegrained tags. We report chrF++ scores aggregated by language direction and resource level type. We observe that finegrained tagging gives the best performance." |
| Q601 | 68 | input_ontology | "We quantify the impact of using NLLB-Seed in various experimental settings." |
| Q602 | 68 | input_content | "It is important to understand whether there is value in such small but high quality human-annotated seed datasets for low-resource languages." |
| Q603 | 68 | input_ontology | "Is such a small dataset sufficient to bootstrap a machine translation system for a new low-resource language or finetune an existing machine translation system on a new domain?" |
| Q604 | 68 | input_ontology | "In this section, we investigate these questions and we aim to measure the effect of training translation models on such a small human annotated seed dataset like NLLB-Seed (see Section 4.2)." |
| Q605 | 68 | output_content | "We are interested in quantifying the importance of a dataset which has been professionally translated, covers a wider domain, and which can be confidently attributed to the specified language." |
| Q606 | 68 | input_ontology | "First, we want to measure the performance of bilingual models trained on NLLB-Seed against those trained on publicly available data (PublicBitext) as well as on the combination of both (NLLB-Seed+PublicBitext)." |
| Q607 | 68 | input_ontology | "Secondly, given a certain amount of publicly available parallel data, we study the incremental effect of adding NLLB-Seed, compared to simply adding more data from the original domain of the public bitext." |
| Q608 | 68 | input_content | "To answer this we create for each language a new dataset, which we call Diminished+NLLB-Seed. This is obtained by subtracting from PublicBitext a random sample of sentences of the same size as the seed dataset (∼6.2k), and swapping in NLLB-Seed in its place." |
| Q609 | 68 | input_form | "The result is a dataset which is of the same size as PublicBitext, but which also contains NLLB-Seed." |
| Q610 | 69 | input_content | "We select eight low-resource directions covered by NLLB-Seed data. For fair comparison to existing datasets we only select directions for which we could also find a minimum of 10 k sentences of publicly available parallel text." |
| Q611 | 69 | input_content | "These are ban_Latn, dik_Latn, fuv_Latn and mri_Latn, translated into and out of eng_Latn." |
| Q612 | 69 | input_ontology | "We train bilingual models for each direction, using a transformer architecture with 6 encoder layers and 6 decoder layers trained with an inverse square-root learning rate schedule with warm-up." |
| Q613 | 69 | input_form | "Each language pair uses a custom SentencePiece vocabulary of size 1k." |
| Q614 | 69 | input_content | "To study the incremental effect of adding NLLB-Seed, we prepare Diminished+NLLB-Seed datasets for each of the above languages." |
| Q615 | 69 | output_form | "To control for noise, we repeat each experiment three times with different subsets of PublicBitext and report the averages and standard deviations for each." |
| Q616 | 69 | output_content | "The small variance validates that the low scores on PublicBitext data are not due to any bias of sampling but the lower quality of the PublicBitext data compared to NLLB-Seed." |
| Q617 | 69 | input_ontology | "We investigate whether using NLLB-Seed might additionally affect performance when backtranslation is used, for example, if using a small amount of human-translated data such as NLLB-Seed might increase backtranslation quality." |
| Q618 | 70 | input_ontology | "We evaluate four models: a dense model baseline, our best performing MoE variant, our best performing SSL variant, and our best performing BT variant." |
| Q619 | 70 | input_content | "For simplicity, we evaluate the same 24 translation directions for all models with 506 source sentences translated per model." |
| Q620 | 70 | input_ontology | "9 directions are translation into English, 11 out of English, and 4 non-English directions for representativeness." |
| Q621 | 70 | output_form | "For rapid experimental iteration, the vast majority of modeling ablation decisions are assessed using automatic metrics such as BLEU or chrF++." |
| Q622 | 70 | output_form | "However, performance improvements in automatic metrics may not translate to human-perceived quality, especially for minor improvements in scores such as BLEU." |
| Q623 | 70 | output_content | "In this section, we conduct a human evaluation (see Section 7 for a description of our protocol) to understand if our described modeling improvements correlate with quality improvements detectable through human evaluation." |
| Q624 | 70 | output_form | "We investigate the relationship between chrF++ score and human evaluation score to understand what quantity of automatic metric improvement in a model ablation overall, we find that chrF++ improvements of +0.5 chrF++ usually correlate to statistically significant human evaluation improvements, with a score of +1 chrF++ almost always being detectable by human evaluators." |
| Q625 | 71 | output_form | "For our best MoE variant, there were 14 directions with chrF++ improvements more than +0.5 over the baseline and 10 of these were statistically significant improvements in human evaluation." |
| Q626 | 71 | output_form | "For these 10 directions, the human evaluation score more than 0.2 (on a 5-point scale) over the baseline with a corresponding chrF++ improvement of +2.5" |
| Q627 | 71 | output_form | "For our best SSL variant, there were 9 directions with chrF++ improvement more than +0.5 over the baseline and 4 directions were statistically significantly better in human evaluation." |
| Q628 | 71 | output_form | "For these 4 directions, the human evaluation score improved +0.2 over the baseline with a corresponding chrF++ improvement of +2.7." |
| Q629 | 71 | output_form | "For our best BT variant, there were 14 directions with chrF++ improvement more than +0.5 over the baseline and 10 directions with statistically significant human evaluation improvements." |
| Q630 | 71 | output_form | "For these 10 directions, the human evaluation score improved +0.18 over the baseline and chrF++ improved on average by +3." |
| Q631 | 71 | output_form | "In conclusion, we believe that based on our human evaluation studies of model ablations, that an improvement of +0.5 chrF++ is often detectable by human evaluators." |
| Q632 | 71 | output_form | "Machine translation is commonly evaluated using automatic metrics as well as human evaluation, e.g., in the WMT evaluation campaign (Akhbardeh et al., 2021), in the AmericasNLP Shared Task (Mager et al., 2021)." |
| Q633 | 71 | output_form | "In this section, we describe the automatic metrics that we used and the methodology we followed to perform human evaluation." |
| Q634 | 71 | output_form | "We present the results of various studies conducted on multilingual translation models and analyze the reliability of automatic metrics on such a varied and low-resource set of languages." |
| Q635 | 71 | output_ontology | "Metrics such as BLEU and human evaluation often focus on an axis of translation quality heavily grounded in accuracy and" |
| Q636 | 72 | output_ontology | "We open source these novel toxicity lists for all 200 languages." |
| Q637 | 72 | output_form | "Various metrics for automatic translation quality assessment exist, including model-based metrics such as COMET (Rei et al., 2020) and BLEURT (Sellam et al., 2020)." |
| Q638 | 72 | output_form | "While model-based metrics have shown better correlation with human judgment in recent metrics shared tasks (Freitag et al., 2021), they require training and are not easily extended to a large set of low-resource languages." |
| Q639 | 72 | output_form | "Another approach is to use highly approximate metrics based on roundtrip translations such as RttLangIDChrF (Bapna et al., 2022), although roundtrip translation may not correlate well with translation quality (Koehn, 2005)." |
| Q640 | 72 | output_form | "While such methods are more easily scaled to new languages, they are highly dependent on factors which makes results difficult to replicate." |
| Q641 | 72 | output_form | "In this work, we therefore choose not make use of model-based and roundtrip-based metrics, and rely instead on BLEU and chrF++." |
| Q642 | 72 | output_form | "Both measures rely on the core concept that translation quality can be quantified based on how" |
| Q643 | 73 | output_form | "The BLEU score (Papineni et al., 2002) has been the standard metric for machine translation evaluation since its proposal two decades ago. It measures overlap between machine translation and a human reference translation by combining precision of 1-grams to 4-grams with a brevity penalty." |
| Q644 | 73 | output_form | "A major downside of BLEU is that it is tokenization-dependent." |
| Q645 | 73 | output_form | "Goyal et al. (2022) propose spBLEU, a BLEU metric based on a standardized SentencePiece model (SPM) covering 101 languages, released with Flores101. In this work, we provide SPM-200 along with Flores-200 to enable measurement of spBLEU." |
| Q646 | 73 | output_form | "The chrF++ score (Popović, 2017) overcomes the limitation of the BLEU score which requires that a sentence can be broken up into word tokens. However, some languages, such as Chinese or Thai, do not use spaces to separate words and word segmentation tools may not be readily available or even exist." |
| Q647 | 73 | output_form | "chrF++ overcomes this weakness by basing the overlap calculation on character-level n-grams F-score (n ranging from 1 to 6) and complementing with word unigrams and bi-grams." |
| Q648 | 73 | output_form | "In this work, we primarily evaluate using chrF++ using the settings from sacrebleu. However, when comparing to other published works, we utilize BLEU and spBLEU where appropriate." |
| Q649 | 73 | output_form | "While automatic scores are a great tool to drive research, human evaluation is essential to ensure meaningful assessments of translation quality (Kocmi et al., 2021)." |
| Q650 | 73 | output_form | "We use two advances — the XSTS evaluation protocol and the use of calibration sets — to enable meaningful human evaluation scores that are comparable across language pairs." |
| Q651 | 73 | output_form | "We adapt the recently proposed crosslingual Semantic Text Similarity (XSTS) methodology from Agirre et al. (2012). In short, XSTS is a human evaluation protocol that focuses on meaning preservation far more than fluency." |
| Q652 | 73 | output_form | "For low-resource languages, translations are usually of weaker quality, and so we focus far more on usable (meaning-preserving) translations, even if they are not fully fluent." |
| Q653 | 73 | output_ontology | "When building machine translation systems for many different language pairs, a core question is which language pairs reach certain levels of quality. Hence, we need meaningful scores that are comparable across language pairs." |
| Q654 | 74 | output_ontology | "XSTS rates each source sentence and its machine translation on a five-point scale, where 1 is the lowest score and 5 is the highest score." |
| Q655 | 74 | output_content | "work has found that XSTS yields higher interannotator agreement (Licht et al., 2022)." |
| Q656 | 74 | output_content | "To enable meaningful scores that are comparable across language pairs, we ask each evaluator to provide assessments using the XSTS scale on exactly the same set of sentence pairs." |
| Q657 | 74 | output_content | "The purpose of this is to identify which sets of annotators have a systemic tendency to be more harsh or generous in their scoring, and correct for this effect." |
| Q658 | 74 | output_content | "While evaluators assess different languages, the calibration set consists of machine translation output into English paired with an English reference translation." |
| Q659 | 74 | output_content | "Based on how evaluators use the XSTS scale on this calibration set, we adjust their raw scores on the actual evaluation task to ensure consistency across evaluators." |
| Q660 | 74 | output_form | "While the monolingual task does not precisely mimic the bilingual XSTS task, it is a reasonable first approximation and has been shown to increase the correlation between human and automatic metrics, primarily by reducing one source of 'noise' in the human evaluations; the lack of score calibration between annotators." |
| Q661 | 74 | output_form | "To obtain an aggregate human quality metric for each language direction in an evaluation study, we take the majority XSTS score for each sentence and average these majority scores over all evaluated sentences." |
| Q662 | 75 | output_form | "Mls→lt denotes the total amount of evaluators evaluating the (source, translation) sentence pair (S, T) for translation direction ls → lt and Tls→lt = {(Sls→lt,k, Tls→lt,k) \| 1 ≤ k ≤ Nls→lt} is the set of Nls→lt(source, translation) sentence pairs being evaluated for translation direction ls → lt." |
| Q663 | 75 | output_content | "Every evaluator in a given study s is also asked to provide ratings for all or part of a calibration set, Cs = {(Ss,k, Ts,k) \| 1 ≤ k ≤ Ks}, where Ss,k denotes the k-th source sentence in the calibration set for evaluation study s, Ts,k denotes the translated sentence corresponding to Ss,k, and Ks = \|Cs\| is the number of sentence pairs in the calibration set for evaluation study." |
| Q664 | 75 | output_content | "The calibration sets for all evaluation studies are drawn from a set of source, target sentence pairs consisting of K = 1000 backtranslated Flores-200 sentences of varying quality." |
| Q665 | 75 | output_form | "For each language direction evaluated in a study, we obtain the mean median XSTS score ("majority score") on the calibration set." |
| Q666 | 75 | output_form | "To obtain aggregate calibrated XSTS scores on the language direction level, we explored several different calibration methodologies of the form He(s)ls→lt = f(H(s)ls→lt, C(s)ls→lt)." |
| Q667 | 75 | output_form | "We also explored other calibration strategies, including clipping the strength of the calibration, adding a multiplicative factor H(s)ls→lt − α(C(s)ls→lt − C¯), as well as a more sophisticated heuristic calibration adjustment we name "moderated calibration" designed to keep the calibrated scores within the same [1, 5] domain as the initial majority XSTS scores, to attenuate extreme calibration shifts, and to attenuate calibration shifts when the XSTS score is close to extreme values." |
| Q668 | 75 | output_form | "C¯ is the mean majority XSTS score on the calibration set across all evaluated language directions across all studies, which in practice is close to 3 (3.01) and therefore for analysis of individual studies we often replace C¯ with 3 to obviate the need for interacting with all evaluation data across all studies." |
| Q669 | 76 | input_ontology | "Note that NLLB-200 refers to a 55B parameter MoE model, and NLLB-200 Baseline refers to a dense 3.3B parameter model." |
| Q670 | 76 | output_form | "None of the calibration methods we investigated showed a dramatic difference in correlation with automated scores, and all calibration methodologies we explored provided superior correlation compared with uncalibrated XSTS scores." |
| Q671 | 76 | output_form | "For this paper, any references to calibrated scores refer to He[mod](s)_ls→lt." |
| Q672 | 76 | output_content | "The performance of machine translation models according to human evaluators has been extensively analyzed for bilingual models and specific domains." |
| Q673 | 76 | output_ontology | "In contrast, we focus on multilingual translation." |
| Q674 | 76 | output_form | "In this section, we analyze the correlation between human evaluation scores and automatic metrics such as chrF++, examine the difficulty of" |
| Q675 | 76 | output_form | "All automated scores were computed only on the sentences evaluated for a given model and translation direction (either the full Flores-200 dataset or a subset)." |
| Q676 | 77 | output_form | "We use aggregated results from three large-scale multilingual human evaluation studies (Study A, Study B, and Study C) to examine relationships between human measures of quality and automated scores like spBLEU and chrF++." |
| Q677 | 77 | output_content | "These evaluation studies contain evaluations of translations from five distinct translation models (NLLB-200 (MoE 55B), M2M-100 12B (Fan et al., 2020), NLLB-125 — a MoE model covering 125 languages — and an English-Centric multilingual WMT2021 Submission covering 7 languages (Tran et al., 2021), and a dense 3.3B NLLB-200 model used as a baseline for NLLB-200 (MoE 55B)) and 86 distinct translation directions evaluated by up to 292 distinct human evaluators." |
| Q678 | 77 | output_content | "Each (source, translation) pair was scored by 3 evaluators, though the evaluators may (rarely) change between different pairs of (source, translation) sentences." |
| Q679 | 77 | output_content | "Study B was an exception: the study was conducted in two parts, with one set of evaluators evaluating the first half of the evaluations and another evaluating the second (though evaluator overlap was allowed)." |
| Q680 | 77 | input_content | "The source, translation pairs come from the Flores-200 dataset (1,000 sentences), however some language directions in some studies were evaluated on a randomly chosen subset of Flores-200 containing only 500 sentences." |
| Q681 | 77 | output_form | "Studies A and B shared the same calibration set of 1,000 items, and Study C contained a randomly chosen subset of 500 calibration sentences drawn from the original calibration set." |
| Q682 | 77 | output_form | "We find that automated metrics like spBLEU and chrF++ correlate reasonably well with calibrated human evaluations of translation quality, as seen in Figure 24." |
| Q683 | 77 | output_form | "In particular, we find that the Spearman R correlation coefficients between aggregated XSTS and spBLEU, chrF++ (corpus) and chrF++ (average sentence-level) are 0.710, 0.687, and 0.694 respectively." |
| Q684 | 77 | output_form | "Corpus spBLEU provides the best nominal correlation, followed by average sentence-level chrF++ with corpus chrF++ being the least well correlated out of the three." |
| Q685 | 77 | output_form | "We also find that calibrated human evaluation scores correlate more strongly with automated scores than uncalibrated human evaluation scores across all automated metrics and choices of correlation coefficient." |
| Q686 | 77 | output_form | "In particular, uncalibrated human evaluation scores have a Spearman R correlation coefficient of 0.625, 0.607, and 0.611 for spBLEU, chrF++ (corpus) and chrF++ (average sentence-level), respectively." |
| Q687 | 77 | input_ontology | "We also inspect the individual score distributions for the NLLB-125 model." |
| Q688 | 77 | output_ontology | "We observe three rough categories of XSTS score distribution." |
| Q689 | 78 | input_content | "All translations were generated with the NLLB-125 model, and all scores are from a single evaluation study." |
| Q690 | 78 | input_ontology | "We show six distributions that illustrate the three rough categories of score distributions seen in our dataset." |
| Q691 | 78 | output_form | "Such a distribution indicates the translation for almost all sentences evaluated has strong performance." |
| Q692 | 78 | output_form | "For these languages, while the average score can be high, there are many sentences that are rated poorly." |
| Q693 | 78 | output_form | "Finally, the third pattern we observe is large numbers of poor-quality translations (XSTS scores of 1) along with high rates of incoherent sentences, meaning the evaluator specifically marked the translation as incoherent." |
| Q694 | 78 | output_form | "These are shown in Figure 25's third column and often represents text that is mostly incomprehensible or has completely distorted wording." |
| Q695 | 78 | output_form | "Several previous works (Arivazhagan et al., 2019) and our findings in Section 6 indicate that translation from various languages into English yields higher BLEU scores than translation out of English." |
| Q696 | 78 | output_form | "Generally we find that, as suggested by automated scores like chrF++ and spBLEU, human evaluation scores seem to also reflect that into English translation quality is typically better than out of English translation quality, with some exceptions such as snd and azj where into English performance is notably worse on both automated metrics and human evaluation metrics." |
| Q697 | 79 | output_ontology | "Toxicity detection in digital content has received significant attention in recent years, both for user-generated language (Kiritchenko et al., 2021; Mishra et al., 2019; Vidgen et al., 2019; Zampieri et al., 2019) and machine-generated text (Bender et al., 2021; Xu et al., 2020)." |
| Q698 | 79 | output_ontology | "The generation of toxic content has been explored for various sentence classification and dialogue tasks, but not extensively in translation." |
| Q699 | 79 | output_ontology | "Our goal in this section is to provide an analysis of toxicity in multilingual MT models." |
| Q700 | 79 | output_ontology | "We provide the first baseline to evaluate toxicity in a massive number of languages by collecting and releasing toxicity wordlists in 200 languages (Section 7.3.1)." |
| Q701 | 79 | output_form | "Subsequently, in Section 7.3.3 we propose and evaluate simple yet scalable toxicity detectors that can be optimized in precision or recall depending on the particular application (i.e., filtering or detection, respectively)." |
| Q702 | 79 | output_form | "Then, we propose a filtering strategy to mitigate toxicity imbalance in training data and visualize the source contributions of several examples with added toxicity in Section 7.3.3." |
| Q703 | 79 | output_ontology | "Note that in this section we will be giving translation examples that contain toxic language." |
| Q704 | 79 | output_ontology | "Toxicity in natural language processing can be defined as the use of words or phrase structures that induce offensive utterances and bad sentiments (Google Jigsaw, 2017)." |
| Q705 | 79 | output_ontology | "In the context of translation, toxicity may originally be present in the source text or it can be generated de-novo in the target text (added toxicity)." |
| Q706 | 79 | output_ontology | "This added toxicity can come from a mistranslation (e.g., wrong lexical choice) or as a hallucination of a new target word from zero — both produce inaccurate translations." |
| Q707 | 80 | output_ontology | "Reliable general-purpose MT systems should be able to translate any source content adequately regardless of the domain or register, which includes translating language that may be regarded as toxic." |
| Q708 | 80 | output_ontology | "They should remain faithful to the source content, and should not add through the translation process any elements of toxicity that are not found in the source." |
| Q709 | 80 | output_ontology | "Our main purpose is to improve translation safety through minimizing the probability of catastrophic mistranslations." |
| Q710 | 80 | output_ontology | "Note that added toxicity represents one of several types of catastrophic mistranslations (Specia et al., 2021), along with mistranslations of named entities, genders (Levy et al., 2021), numbers and units, and reversal of semantic polarity." |
| Q711 | 80 | output_form | "To enable toxicity detection at scale, we focus on a wordlist-based approach." |
| Q712 | 80 | output_ontology | "We include items that are commonly referred to as vulgar or profane language." |
| Q713 | 80 | output_ontology | "In addition to these, we include items more specifically associated with depictions of pornographic content or sexual acts, some frequently used hate speech expressions, and some bullying expressions (including language that can cause trauma or be used with the purpose of silencing someone)." |
| Q714 | 80 | output_ontology | "We also include items, vulgar or not, referring to body parts that are commonly associated with sexual practices." |
| Q715 | 80 | output_ontology | "Toxicity is culturally sensitive, which constitutes a challenge when starting from one source language (in this case, English) and attempting to find equivalents in such a largely multilingual setting." |
| Q716 | 80 | output_ontology | "Hate speech terms such as racial or ethnic slurs, for example, may well be the most challenging of all." |
| Q717 | 80 | input_content | "We begin based on the professional translation of an initial list assembled in English, and allow additions to adapt to cultural specificities." |
| Q718 | 80 | output_form | "We iteratively designed a template for toxicity translation that provides information for disambiguation and contextualization purposes." |
| Q719 | 80 | output_ontology | "In the latest iteration of the template, the additional information includes a breakdown into domains (e.g., slurs, sex-related terms, abbreviations), part-of-speech information, pointers to the dictionary definitions of the words in their toxic sense, indications as to the language register(s) (slang, vulgar, formal, etc.)." |
| Q720 | 80 | output_form | "In addition, the template provides clearly identified areas for morphological variants to be added (if the target language is morphologically rich)." |
| Q721 | 80 | output_form | "For polysemous terms, which may or may not be toxic depending on context, the template offers additional room and guidance as to best disambiguation practices through suggesting much less ambiguous, short n-grams (typically, 0 < n < 4)." |
| Q722 | 80 | output_content | "For the purpose of reducing cultural blind spots, another section of the template gives translators the possibility to insert common toxic language for which it may be difficult to find direct English equivalence." |
| Q723 | 80 | output_content | "The translators are asked to provide explanations or verbatim descriptions." |
| Q724 | 80 | output_form | "Suggestions were limited to around forty" |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://link.springer.com/article/10.1007/s43621-023-00161-7 |
| WEB-2 | https://www.academia.edu/99257540/The_role_of_Amhara_credit_and_saving_institution_in_improving_rural_households_livelihood |
| WEB-3 | https://arxiv.org/abs/2403.13737 |
| WEB-4 | https://arxiv.org/html/2403.19365v1 |
| WEB-5 | https://data.worldbank.org/indicator/SE.ADT.LITR.ZS?locations=ET |
| WEB-6 | https://zoetalentsolutions.com/education-statistics-for-ethiopia/ |
| WEB-7 | https://freedomhouse.org/country/ethiopia/freedom-net/2024 |
| WEB-8 | https://freedomhouse.org/country/ethiopia/freedom-net/2023 |
| WEB-9 | https://www.macrotrends.net/global-metrics/countries/eth/ethiopia/electricity-access-statistics |
| WEB-10 | https://arxiv.org/html/2508.20511v1 |
| WEB-11 | https://huggingface.co/facebook/nllb-200-3.3B |
| WEB-12 | https://aclanthology.org/2024.findings-emnlp.25.pdf |
| WEB-13 | https://www.nature.com/articles/s41586-024-07335-x |
| WEB-14 | https://www.emergentmind.com/topics/flores-200-benchmark-dataset |
| WEB-15 | http://www.acsi.org.et/ |
| WEB-16 | https://www.findevgateway.org/case-study/2004/01/amhara-credit-and-saving-institution-acsi-institutional-profile-current-status |

---

