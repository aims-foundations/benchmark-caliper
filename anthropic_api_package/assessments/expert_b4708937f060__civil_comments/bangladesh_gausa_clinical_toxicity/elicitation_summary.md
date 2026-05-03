## Use Case
A domain-specific content moderation system evaluating the robustness of a patient-centric chat assistant LLM against toxic content generation. The deployment targets low-literacy users in Gazipur, Bangladesh, who interact with the chatbot in textual form under conditions of frequent code-switching and punctuation errors. The developer needs to assess how well the system detects and blocks toxicity that may be induced — intentionally or unintentionally — during health-oriented interactions.

## Target Population
- **Geography:** Gazipur, Bangladesh (peri-urban/industrial context)
- **Language(s):** Bangla (standard and regional varieties), Banglish (Bangla in Roman/Latin script), phonetic Bangla in ASCII, code-switched Bangla-English with degraded punctuation and spacing
- **Literacy:** Low literacy; interaction patterns include irregular orthography, no punctuation, phonetic approximations
- **Role:** Patients or health-information seekers using a clinical chatbot
- **Adversarial actors:** Could be same low-literacy user population or deliberate bad actors operating in the same degraded-text register
- **Demographic relevance:** Multi-religious context (Muslim majority, Hindu/Christian minorities); caste and gender norms salient; locally grounded superstitious belief systems in play

## Elicitation Responses

Q1 [IO]: The benchmark was built around identity groups defined in a Western/English-language online-comment context. Which identity groups or social fault lines should your content moderation system actually be robust against in Gazipur?
A1: The most operationally relevant toxicity is not primarily identity-attack-based but is instead contextually induced through patient-chatbot interaction — e.g., queries that embed son-preference gender discrimination (asking how to conceive a boy rather than a girl). Identity-based dimensions such as religious minority targeting, caste, and gender do matter but are secondary to the specific modality of harmful prompts that emerge naturally within health queries.

Q2 [IC]: Does your system need to handle locally grounded implicit toxicity — indirect religious insults, racial remarks, regionally specific slang, or superstition-coded harmful language?
A2: Yes. Key locally grounded patterns include: religiously coded slurs (e.g., "malaun" as a derogatory term for Hindus), colorist/racial remarks (e.g., skin-whitening queries), and prompts that encode harmful superstitious beliefs. These forms of implicit toxicity are embedded in culturally specific phrasing that standard English or even standard Bengali toxicity classifiers would not flag.

Q3 [IF]: Will adversarial toxic inputs arrive in degraded or code-switched forms (Banglish, phonetic Bangla in ASCII, no punctuation, unusual spacing)?
A3: Yes, definitively. Toxic inputs are expected to arrive in the same degraded, code-switched register as ordinary user messages — Banglish in Roman script, phonetic approximations of Bangla, absent or erratic punctuation. There is no clean separation between "adversarial" and "normal" input form.

Q4 [OC]: Whose judgment should be authoritative for labeling content as toxic in this deployment?
A4: Ideally, multiple annotators from the target region (Bangladesh) with clinical and cultural context. As a minimum viable standard, one or two native Bangladeshi annotators who understand local health, religious, and social context are considered acceptable — explicitly framed as better than no regional representation, even if not fully sufficient.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark's identity-group taxonomy (Western online-comment demographics) is almost entirely misaligned with the health-query-induced, religiously coded, and gender-norm-embedded toxicity categories relevant to Gazipur users. |
| IC | HIGH | Concrete datapoints are drawn from English-language online comments with no representation of Banglish code-switching, health-context toxicity triggers, colorist remarks, or superstition-encoded harmful prompts salient in this deployment. |
| IF | HIGH | Benchmark assumes clean, standard English text; deployment input is systematically degraded — Roman-script Bangla, phonetic ASCII, absent punctuation — and toxic signals are embedded within this non-standard signal distribution. |
| OO | HIGH | Benchmark output taxonomy scores toxicity against demographic identity categories defined for a different cultural context; the deployment requires scoring health-context implicit toxicity, son-preference gender bias, and religious slur detection that fall outside those categories. |
| OC | HIGH | Ground-truth labels are annotated by non-representative (Western, English-language) crowdworkers; user's answer explicitly identifies the absence of Bangladeshi regional annotators as a critical gap, and the content involves highly subjective, culturally variable judgments. |
| OF | MODERATE | Both benchmark and deployment use text-in, label/score-out pipelines, so the output representation is broadly matched; however, the score calibration and threshold assumptions were derived from a different language and population distribution, creating a secondary mismatch. |

## Flagged Gaps

1. **Banglish / Roman-script Bangla toxicity detection:** The benchmark contains no instances of toxicity encoded in Latin-script Bangla or phonetically approximated Bangla. Downstream search should investigate whether any existing toxicity benchmark covers Roman-script Bangla or Banglish code-switching, particularly in health contexts.

2. **Health-context-induced toxicity patterns:** No known large-scale benchmark specifically addresses toxic prompts that are embedded within patient-chatbot interactions (e.g., son-preference queries, harmful traditional medicine requests, superstition-driven health misinformation). Downstream search should look for clinical NLP safety benchmarks in South Asian languages.

3. **Religiously coded implicit toxicity in Bengali:** Terms like "malaun" (anti-Hindu slur) and similar community-specific derogatory language are unlikely to appear in the benchmark dataset. Downstream search should investigate Bengali hate speech datasets (e.g., HatEval for Bengali, or datasets from BUET or other Bangladeshi institutions) that cover inter-communal slurs.

4. **Colorism and skin-tone-based harmful content in South Asian context:** Racial/colorist remarks in the South Asian register (e.g., skin-whitening queries) differ structurally from the racial identity categories in the benchmark. Downstream search should check whether any South Asian NLP fairness datasets include colorism-specific annotations.

5. **Superstition-encoded harmful health content:** Prompts reflecting locally held superstitious beliefs that could cause patient harm are a distinct toxicity sub-category with no analog in the source benchmark. Search should look for any Bangladeshi or South Asian health misinformation datasets.

6. **Annotator representativeness:** The benchmark's ~450,000 annotated comments were labeled by crowdworkers with no documented Bangladeshi or South Asian regional representation. Downstream scoring should flag the OC dimension accordingly and search for any Bangladeshi community annotation efforts or regional content moderation guidelines.

7. **Sub-national variation within Bangladesh:** Gazipur's peri-urban, garment-industry demographic may differ linguistically and culturally from Dhaka urban, Sylheti, or Chittagongian populations. The benchmark provides no mechanism to distinguish these sub-national variation patterns, and no current Bangladeshi NLP benchmark is known to stratify by intra-national demographic cohort.