I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **No Language Left Behind: Scaling Human-Centered Machine Translation (Flores-200 Benchmark)** is valid for use in **Amhara Region Agricultural and Microfinance Translation Cohort**.

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

- **Name**: nllb
- **Full Name**: No Language Left Behind: Scaling Human-Centered Machine Translation (Flores-200 Benchmark)
- **Domain**: Multilingual machine translation evaluation
- **Languages**: amh, eng, fra, arb, zho, hin, swh, yor, hau
- **Porting Strategy**: ground_up
- **Year**: 2022

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
The core evaluation task is pairwise sentence-level translation quality assessment
across 40,000+ directions using Flores-200 [Q5]. The benchmark organizes task
coverage along two axes: (1) resource level — 40 high-resource, 70 low-resource,
and 22 very low-resource directions in a representative sub-sample of 110 directions
[Q419, Q420] — and (2) a small set of domains tested in NLLB-MD (news, scripted
talks, chat, WHO health) for six language directions only [Q159, Q166, Q167, Q168,
Q169]. Ancillary subtasks include language identification [Q179, Q184], bitext mining
[Q286, Q287, Q289], and toxicity detection [Q699, Q701]. The taxonomy explicitly
excludes oral/non-standardized languages [Q77] and has no evaluation category for
agricultural, land-tenure, financial, or bureaucratic document types. The benchmark
asks "How well do models generalize to non-Wikimedia domains?" [Q159] but does not
extend domain testing beyond news, talks, chat, and health, leaving agricultural
input subsidy notices, land-use policy updates, and credit-scheme terms entirely
outside the evaluation taxonomy [Q94]. The deployment's core document genres are
thus unrepresented at every level of the task hierarchy.

### Input Content
Flores-200 consists of 3,001 sentences translated from English-language Wikimedia
projects — specifically Wikinews, Wikijunior, and Wikivoyage [Q95]. NLLB-Seed adds
approximately 6,000 sentences per language sampled from Wikimedia's curated article
list spanning 11 topic categories including People, History, Philosophy, and
Geography [Q143, Q146], but not agriculture, land tenure, or microfinance. The
paper explicitly acknowledges that English-centric Wikipedia sourcing means "the
content reflects what Wikipedia editors find is relevant for English Wikipedia, and
likely does not cover diverse content from different cultures" [Q151]. For African
languages, low-resource bitext is "often opportunistically drawn from known
collections of multilingual content, such as the Christian Bible or publications
of multinational organizations" [Q284], sources that are "often limited in quantity
and domain" [Q285]. Twelve African languages in the set have fewer than 100,000
sentence pairs [Q369], and even for languages with more data, "we struggled to
curate meaningful amounts of monolingual data" [Q370]. For Amharic specifically, a
dedicated 8,000-token Ge'ez-script SentencePiece vocabulary was trained [Q382], and
combined supervised cosine-loss and unsupervised MLM training was deployed [Q373,
Q374], indicating deliberate attention to Amharic support — but the content of
evaluation instances remains exclusively Wikimedia-derived. Federally standardized
Ethiopian agricultural and financial administrative vocabulary (land proclamation
terms, ACSI credit schedules, subsidy eligibility conditions) is absent from both
training and evaluation content by construction.

### Input Form
All benchmark inputs are text-only, encoded via BCP 47 tags with ISO 639-3 base
codes and ISO 15924 script subtags [Q79]. The Ethiopic script (Ge'ez) used by
Amharic is explicitly supported with a dedicated SentencePiece vocabulary [Q382],
and all 204 languages are represented in Flores-200. The benchmark's monolingual
preprocessing pipeline handles HTML stripping, script filtering, length and
punctuation heuristics, and deduplication [Q256, Q264, Q271, Q276], with special
accommodations for languages without word-boundary spaces [Q646, Q647]. Average
sentence length is approximately 21 words [Q133], consistent with general-domain
prose. No audio, image, or document-layout modality is present. For this deployment
(text-only, Amharic-target, prose output confirmed acceptable), no input-form
mismatch exists at the script or modality level. The 21-word average sentence length
and sentence-level evaluation architecture do not accommodate document-level clause
sequences or structured tables, but the deployer has accepted prose output, reducing
the severity of this gap.

### Output Ontology
The primary output label for the translation task is a scalar quality score
(chrF++, spBLEU, or calibrated XSTS) applied uniformly to all translation directions
and all sentence types [Q455, Q648, Q661]. No domain-specific rubric distinguishes
correct rendering of agricultural jargon, subsidy eligibility conditions, or loan
penalty clauses from general prose quality. For toxicity assessment, the output
taxonomy distinguishes source-present toxicity from "added toxicity" introduced
de novo by the model [Q705, Q706], with label categories covering vulgar/profane
language, pornographic content, hate speech, bullying, and body-part references
[Q712, Q713, Q714]. Human evaluation output is structured on a five-point XSTS
meaning-preservation scale [Q654] with three rough distributional categories
identified [Q688]. The paper explicitly acknowledges the toxicity taxonomy is
"culturally sensitive" and that "hate speech terms such as racial or ethnic slurs
may well be the most challenging" [Q715, Q716], but no regional calibration for
Ethiopian context is documented. Crucially, the output scoring ontology contains
no category for false precision in numerical eligibility conditions, incorrect
rendering of conditional legal clauses, or mistranslation of domain-specific
administrative identifiers — the most consequential error types for binding
agricultural and financial documents. A chrF++ score cannot distinguish a
translation that renders a subsidy rate correctly from one that silently alters
an eligibility threshold, rendering the benchmark's scoring criteria structurally
misaligned with the deployment's correctness requirements.

### Output Content
For Flores-200, a multi-step professional translation workflow was employed:
translators aligned on language standards, translated all 3,001 sentences, underwent
automated checks, and independent reviewers assessed a 20% sample; languages scoring
below 90% quality were sent for post-editing [Q93]. Translators required two to five
years of translation experience [Q97] and undergo re-testing every 18 months [Q98];
reviewers required native-speaker status and typically five or more years of
translation experience [Q99, Q100]. For low-resource languages where qualified
reviewers were difficult to find, qualification thresholds were relaxed to accept
broader linguistics degrees or extensive commercial experience [Q103]. Human
evaluation studies covered 86 translation directions evaluated by up to 292 human
evaluators [Q677], with three evaluators per sentence pair [Q678], using a
calibration set of 1,000 backtranslated Flores-200 sentences of varying quality
[Q664]. The community interview study informing research priorities recruited 44
native speakers of 36 low-resource languages, but a majority were immigrants living
in the US and Europe and approximately one-third identified as tech workers [Q32] —
a demographic that "may not consummately capture the sentiments of their communities
back home" [Q39, Q40]. For the deployment's validation requirement (federal bureau
translators as the appropriate authority [elicitation A3]), the Flores-200 annotation
workforce — professional generalist translators without documented Ethiopian
government-domain expertise — represents a direct annotator-population mismatch.
No Amharic-specific inter-annotator agreement figures, annotator provenance details,
or domain-expertise requirements for the Amharic translation portion are documented
in the registry. Common translation errors include "mistranslation and unnatural
translation errors" driven by "influences from other non-English languages" and
"lower levels of standardization" [Q136, Q137, Q138].

### Output Form
The benchmark evaluates text outputs only, using two primary automatic metrics:
chrF++ (main metric throughout model development [Q455, Q648]) and spBLEU [Q645].
Model-based metrics such as COMET and BLEURT are explicitly rejected because they
are "not easily extended to a large set of low-resource languages" [Q638]; roundtrip
metrics are dismissed as unreliable [Q639]. Human evaluation uses the calibrated
XSTS five-point meaning-preservation scale [Q650, Q654], with Spearman R
correlations between XSTS and spBLEU/chrF++ at approximately 0.68–0.71 [Q683].
An improvement of +0.5 chrF++ is identified as approximately detectable by human
evaluators [Q624, Q631]. All evaluation scores are computed at the sentence level
on general-domain Flores-200 sentences [Q5, Q326, Q336]; no document-level
coherence metrics, terminology consistency measures, or structural preservation
checks are reported. The deployer confirmed text-only prose output is acceptable
[elicitation A4], which aligns with the benchmark's output modality. However, the
absence of any document-level or terminology-consistency scoring means that
aggregate chrF++ improvements cannot reliably indicate fitness for the deployment's
core use case (binding administrative documents requiring consistent rendering of
the same term across multiple clauses).


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

## Regional Context

```yaml
name: Amhara Region Agricultural and Microfinance Translation Cohort
abbreviation: AMHARA-AGFIN
deployment_context:
  country: Ethiopia
  region: Amhara
  sub_regional_scope: Rural and peri-urban areas served by agricultural cooperatives
    and microfinance institutions (ACSI, ADCSI service areas)
  deployment_description: AI translation system (NLLB, text-only) converting official
    government documents — agricultural input subsidy notices, land-use policy updates,
    and credit-scheme terms from federal and regional bureaus — into Amharic for use
    by farmer cooperative leaders and rural microfinance clients in the Amhara region
    of Ethiopia.
  benchmark_assessed: nllb
  assessment_year: 2025 (current assessment cycle; NLLB paper published 2022; Nature
    publication 2024)
target_population:
  primary_roles:
  - Farmer cooperative leaders and extension workers interpreting binding subsidy
    and land-policy documents
  - Rural microfinance clients (ACSI borrowers, ADCSI borrowers) acting on credit-scheme
    terms and repayment conditions
  - Cooperative administrative staff receiving translated policy notices from federal
    and regional bureaus
  geographic_concentration:
    region: Amhara Region, Ethiopia
    agro_ecological_zones:
    - Highland zones (e.g., North and South Gondar, North and South Wollo zones)
    - Lowland and semi-arid zones (e.g., Awi, Wag Himra, Oromia Special Zone of Amhara)
    zone_level_variation_note: '[NEEDS VERIFICATION — deferred: likely unsearchable
      (sub-national administrative vocabulary differences require domain expert /
      stakeholder elicitation; no searchable public documentation of zone-by-zone
      ACSI vs. ADCSI vocabulary divergence found)]'
  settlement_type: Predominantly rural; some peri-urban cooperative and MFI branch
    office contexts
  estimated_population_size: 'ACSI: approximately 1 million active borrowers per 2018
    World Bank Group microfinance performance assessment (cited in peer-reviewed literature
    as 1,056,390); operates across all 10 Amhara administrative zones with 461 branch
    offices; some sources cite up to ~2 million clients in rural Ethiopia in more
    recent estimates. ADCSI borrower count not separately documented in publicly accessible
    sources. Source: Springer Discover Sustainability (2023) — [WEB-1];
    Academia.edu livelihood study — [WEB-2]'
languages:
  target_language: Amharic (amh)
  script: 'Ethiopic (Ge''ez), ISO 15924: Ethi'
  source_document_languages:
  - Amharic (federal and regional bureau documents in Amharic register)
  - Possibly other Ethiopian official registers (e.g., documents originating from
    federal ministries may be in Amharic; regional variations may exist)
  register_note: Source documents are written in formal bureaucratic register — numbered
    clause structures, legal-administrative phrasing, and domain-specific agricultural
    and financial terminology derived from federal proclamations and regional bureau
    standards. The target population uses an established administrative vocabulary
    shaped by prior government communications; translation must align with this familiar
    register rather than producing generic or colloquial Amharic.
  diglossia_or_register_variation: Ethiopian Amharic exhibits significant register
    stratification between formal written (fidel-based bureaucratic prose) and everyday
    spoken varieties. Cooperative leaders and rural borrowers are accustomed to a
    specific administrative lexicon established through prior government contact;
    departure from this lexicon reduces practical uptake.
  sub_national_register_variation: '[NEEDS VERIFICATION — deferred: likely unsearchable
    (lived administrative practice); no public documentation of ACSI vs. ADCSI vocabulary
    divergence or zone-by-zone register differences found in searches; requires domain
    expert elicitation]'
writing_system:
  script: Ethiopic (Ge'ez script)
  script_note: Amharic uses the Ge'ez abugida script, written left-to-right. NLLB
    includes a dedicated 8,000-token SentencePiece vocabulary trained specifically
    for Amharic and Tigrinya to support this script. No RTL rendering challenges apply.
    Ge'ez script is unambiguous for Amharic in this deployment context.
  nlp_tooling_maturity: 'Amharic is the best-resourced Ethiopian language for NLP.
    The 2024 EthioLLM project introduced multilingual LLMs and EthioBenchmark covering
    five Ethiopian languages including Amharic across NLP tasks (NER, sentiment, MT,
    summarization, QA). EthioMT (2024) introduced parallel corpora for 15 Ethiopian
    languages. However, no domain-specific NLP tooling for agricultural/financial/bureaucratic
    Amharic terminology exists; all available benchmarks cover general-domain or news/social
    media content. Source: EthioLLM paper (arXiv:2403.13737) — [WEB-3];
    EthioMT paper — [WEB-4]'
literacy_and_education:
  regional_literacy_rate_amhara: '[NOT FOUND — searched UNESCO, World Bank, and Ethiopian
    statistics sources; no Amhara-region-specific adult literacy rate found in publicly
    accessible disaggregated data. National figure is ~51.8% (see national rate below);
    Amhara is expected to be broadly similar to or below national average given rural
    composition, but no sub-national figure confirmed]'
  rural_literacy_rate_amhara: '[NOT FOUND — searched UNESCO and World Bank; no rural-specific
    Amhara literacy rate in publicly accessible sources; national rural rate is substantially
    below national average given strong urban-rural literacy gap documented in Ethiopian
    education statistics]'
  national_literacy_rate_ethiopia: '~51.8% adult literacy rate (ages 15+) as of 2017
    (latest UNESCO/World Bank published figure); youth literacy (ages 15–24) approximately
    69%. No more recent national survey figure confirmed in available sources. Source:
    UNESCO Institute for Statistics via World Bank WDI — [WEB-5];
    corroborated by multiple secondary sources citing 2017 UNESCO data — [WEB-6]'
  education_language_note: Amhara regional schooling is conducted primarily in Amharic.
    Federal government communications and cooperative training materials also use
    Amharic. Cooperative leaders typically have primary or secondary education; rural
    borrowers may have lower formal literacy but high familiarity with spoken administrative
    vocabulary.
  functional_literacy_for_document_use: Target users are expected to engage with translated
    documents through a combination of personal reading and oral relay through cooperative
    leadership structures. Cooperative extension workers serve as key intermediaries
    for disseminating translated content to lower-literacy borrowers.
  relevant_note: Varying literacy levels within the cohort mean that even accurate
    Amharic translations must use vocabulary already familiar to end-users; novel
    or generic Amharic renderings of standardized administrative terms risk practical
    non-uptake even if linguistically correct.
cultural_and_institutional_norms:
  cooperative_structure: Ethiopian agricultural cooperatives operate under a tiered
    membership and leadership structure. Cooperative leaders (e.g., chair, secretary,
    extension liaison) are the primary translators-of-record for policy documents
    disseminated to member farmers. Federal and regional bureau translators are the
    recognized authority on translation correctness; cooperative leaders and borrowers
    are end-consumers rather than validators.
  land_tenure_context: Ethiopian land tenure is governed by federal and regional proclamations
    that have substantially standardized terminology, replacing many traditional local
    terms with official administrative vocabulary. However, residual locally-specific
    terminology and agro-ecological variation (highland vs. lowland) may produce sub-regional
    vocabulary differences not captured in general-purpose translation systems.
  microfinance_institutional_context: 'ACSI (Amhara Credit and Savings Institution)
    is the largest MFI in Ethiopia, constituting approximately 28.1% of all microfinance
    borrowing clients nationally and operating in all 10 Amhara administrative zones
    with 461 branch offices. ADCSI (Addis Credit and Savings Institution) serves the
    Addis Ababa and peri-urban context. Loan agreements, repayment schedules, and
    eligibility conditions are binding documents; mistranslation of penalty clauses
    or eligibility thresholds has direct financial consequences for borrowers. Source:
    Springer Discover Sustainability (2023) — [WEB-1]'
  trust_and_authority_norms: End-users treat government-issued translated documents
    as authoritative. Translation errors that alter the apparent terms of subsidy
    eligibility or loan conditions may not be identifiable by users without access
    to the original document, increasing the stakes of silent mistranslation.
  oral_relay_patterns: Translated documents are frequently read aloud and interpreted
    verbally within cooperative meetings. Terminology consistency and familiar administrative
    vocabulary are critical for accurate oral relay; inconsistent or unfamiliar Amharic
    renderings of standard terms create compounding interpretation errors.
  religious_and_cultural_calendar: '[NEEDS VERIFICATION — deferred: likely unsearchable
    (lived practice); Ethiopian Orthodox calendar observances and agricultural seasonal
    cycles are well-known to affect cooperative scheduling, but specific documentation
    of how these affect document-processing timelines in Amhara cooperative structures
    requires field-level elicitation rather than web search]'
infrastructure_notes:
  connectivity:
    rural_internet_penetration_amhara: 'Ethiopia national internet penetration is
      approximately 19.4% (ITU and DataReportal, February 2024); rural penetration
      is substantially lower given that ~80% of Ethiopia''s population is rural and
      telecommunications infrastructure is described as often absent from rural areas.
      The Amhara region specifically experienced mobile data shutdowns in multiple
      cities from August 2023 to July 2024 due to conflict between federal forces
      and Fano militias, and again in April–May 2023 over regional special forces
      disputes — severely disrupting connectivity during those periods. Note: this
      is a national aggregate with documented Amhara-specific disruptions; actual
      Amhara rural penetration is likely well below the 19.4% national figure. Source:
      Freedom House Freedom on the Net 2024 — [WEB-7];
      Freedom House 2023 — [WEB-8]'
    mobile_penetration_amhara: '[NOT FOUND — no Amhara-specific mobile penetration
      figure found in ITU, World Bank, or Ethio Telecom public data; national mobile
      coverage at 4G extends to 33% of population as of 2022 (Freedom House 2024),
      with 3G expansion ongoing; Amhara connectivity was additionally disrupted by
      conflict-related shutdowns 2023–2024. Source: Freedom House 2024 — [WEB-7]]'
    electricity_access_rural_amhara: 'National electricity access was 55.4% of the
      total population in 2022 (World Bank/ESMAP data), up from 51.1% in 2020. Rural
      access is substantially lower than the national average; the Freedom House 2024
      report notes infrastructure is unreliable and power outages inhibit internet
      access. No Amhara-region-specific rural electricity figure found in publicly
      accessible sources. Source: World Bank WDI / Macrotrends (World Bank data) —
      [WEB-9];
      Freedom House 2024 — [WEB-7]'
    general_pattern: Amhara region is predominantly rural with lower connectivity
      than Addis Ababa or major urban centers. Mobile network coverage and electricity
      access are variable across agro-ecological zones. The translation system is
      deployed text-only (NLLB), reducing infrastructure demands compared to multimodal
      deployments. However, repeated conflict-related internet and mobile data shutdowns
      in Amhara (2021–2024) represent a deployment-relevant disruption risk for any
      connected document-translation pipeline.
  device_and_interface: Translation system is text-only (NLLB). Output format is flowing
    prose Amharic; layout preservation is not required. End-users receive translated
    documents through cooperative office infrastructure (printed paper, SMS, or verbally
    relayed), not directly via AI interface.
  document_processing_pipeline: Source documents originate from federal and regional
    bureaus; translation occurs at the institutional (cooperative or MFI branch) level,
    not at the individual borrower level. Document-level coherence and terminology
    consistency across clauses are critical properties not captured by NLLB's sentence-level
    evaluation architecture.
domain_specific_notes:
  agricultural_policy_documents:
    document_types:
    - Agricultural input subsidy notices (fertilizer, improved seed, pesticide programs)
    - Land-use policy updates (rental terms, lease conditions, parcel reallocation
      notices)
    - Cooperative membership and benefit eligibility notices
    terminology_challenges: Ethiopian federal and regional proclamations have standardized
      most land-tenure terminology (replacing traditional local terms with official
      administrative vocabulary), but domain-specific terms related to subsidy eligibility
      criteria, input distribution schedules, and cooperative-tier benefits may not
      appear in general-purpose Amharic translation benchmarks. Mistranslation of
      eligibility thresholds or seasonal deadlines has direct material consequences
      for farming households.
    relevant_proclamations_and_standards: '[NEEDS VERIFICATION — deferred: below remaining
      search budget and partially unsearchable; Ethiopian federal land proclamations
      (e.g., Federal Rural Land Administration and Use Proclamation No. 456/2005 and
      amendments) are publicly documented but their vocabulary coverage in NLLB training
      data cannot be confirmed without corpus analysis; requires technical investigation
      beyond web search]'
  microfinance_and_credit_documents:
    document_types:
    - Loan agreement terms and conditions (ACSI, ADCSI)
    - Credit-scheme eligibility criteria and documentation requirements
    - Repayment schedules, interest rates, and penalty clause structures
    - Savings product terms
    terminology_challenges: Amharic rendering of financial terms (interest, penalty,
      collateral, guarantor, grace period) must align with vocabulary already in use
      by ACSI/ADCSI in their borrower-facing communications. NLLB training corpora
      are unlikely to contain ACSI-specific or Ethiopian MFI-specific parallel text.
      False precision in numerical loan conditions (interest rates, penalty amounts,
      eligibility cutoffs) represents a high-consequence error type not captured by
      chrF++ or XSTS scoring.
    acsi_adcsi_coverage: '[NOT FOUND — searched ACSI official website, FinDev Gateway,
      J-PAL, and academic literature; no publicly accessible ACSI/ADCSI Amharic-language
      financial terminology guide or parallel text corpus found; ACSI website (acsi.org.et)
      provides institutional background but no downloadable terminology resources.
      This confirms a real gap: no ACSI/ADCSI domain reference data is publicly available
      for use as translation evaluation ground truth.]'
  bureaucratic_and_legal_register:
    document_structure: Source documents typically use numbered clause structures,
      defined terms, and conditional eligibility language ('if … then … unless …').
      The NLLB/Flores-200 benchmark evaluates sentence-level translation with no provision
      for clause-sequence coherence, conditional-logic fidelity, or cross-reference
      consistency. Deployer confirmed prose output is acceptable for this text-only
      deployment, but document-level semantic consistency across clauses remains an
      unscored gap.
    validation_authority: Federal bureau translators are the primary validation authority;
      regional bureau staff and cooperative extension workers are acceptable fallbacks.
      Benchmark annotation workforce (professional generalist translators without
      documented Ethiopian government-domain expertise) does not match the deployer's
      stated validation authority.
benchmark_fit_assessment:
  language_and_script_fit:
    assessment: ADEQUATE — Amharic is explicitly included in Flores-200 with dedicated
      Ge'ez-script SentencePiece vocabulary. No script or modality mismatch exists
      for this text-only, prose-output deployment.
    residual_concern: Sentence-level evaluation architecture does not assess document-level
      Amharic coherence or cross-clause terminology consistency.
  domain_coverage_fit:
    assessment: POOR — Flores-200 evaluation data covers Wikinews, Wikijunior, and
      Wikivoyage content. No agricultural, land-tenure, microfinance, or Ethiopian
      bureaucratic content is present in evaluation or training data by design. Domain-transfer
      gap is the primary fitness risk.
    flagged_for_search: true
  output_scoring_fit:
    assessment: POOR — chrF++ and XSTS scores cannot distinguish correct rendering
      of subsidy eligibility conditions from silent alteration of numerical thresholds.
      No terminology-consistency or conditional-logic-fidelity rubric exists.
    flagged_for_search: true
  annotator_population_fit:
    assessment: POOR — Flores-200 annotators are professional generalist translators
      without documented Ethiopian government-domain expertise. The deployer's validation
      authority (federal bureau translators) is not represented in the annotation
      workforce.
    flagged_for_search: true
  format_fit:
    assessment: ADEQUATE — Deployer confirmed prose output is acceptable for this
      text-only NLLB deployment. Benchmark's text-only sentence-level output format
      aligns with the relaxed output requirement.
    residual_concern: No document-level scoring; aggregated sentence-level chrF++
      improvements may not indicate fitness for binding administrative documents.
flagged_gaps_requiring_web_search:
- gap_id: 1
  description: Agricultural and financial domain coverage in Flores-200 and NLLB evaluation
    extensions
  search_target: Whether any Flores-200 or NLLB evaluation extensions have added Ethiopian
    agricultural, land-tenure, or microfinance content, or whether alternative MT
    benchmarks cover these domains in Amharic
  search_result: 'NO DOMAIN-SPECIFIC BENCHMARK FOUND. EthioLLM (arXiv:2403.13737,
    2024) introduced EthioBenchmark covering NER, sentiment, MT, summarization, and
    QA for Amharic and four other Ethiopian languages, but all tasks use general-domain
    or news/social media data — no agricultural, land-tenure, or microfinance domain
    content. EthioMT (arXiv:2403.19365, 2024) introduced parallel corpora for 15 Ethiopian
    languages drawn from religious and general domains, not administrative/financial
    domains. No Flores-200 extension for Ethiopian agricultural or bureaucratic content
    was found. The Flores+ expansion program has added languages (Erzya, Tuvan, Emakhuwa,
    Iberian languages) but no Ethiopian domain-specific extension. This null result
    confirms the gap is real and unaddressed by the research community. Sources: EthioLLM
    — [WEB-3]; EthioMT — [WEB-4];
    Flores+ extensions survey — [WEB-10]'
- gap_id: 2
  description: NLLB document-level coherence and terminology consistency for Amharic
  search_target: Evidence on NLLB document-level translation quality for Amharic,
    including cross-clause terminology consistency — critical for subsidy eligibility
    conditions and loan agreements
  search_result: 'NO DOCUMENT-LEVEL AMHARIC EVALUATION FOUND. A 2025 paper (''Languages
    Still Left Behind: Toward a Better Multilingual Machine Translation Benchmark'',
    arXiv:2508.20511) found that NLLB models evaluated on Flores+ score well on that
    benchmark but perform poorly on naturalistic evaluation datasets: in experiments
    on Jinghpaw, fine-tuning on naturalistic corpora improved performance on domain-appropriate
    test sets but caused a drop in Flores+ scores, demonstrating domain-benchmark
    mismatch. The paper also found that mock translations merely reproducing named
    entities achieved non-trivial BLEU and ChrF++ scores, suggesting metrics reward
    superficial copying over translational adequacy. This provides strong independent
    evidence that NLLB/Flores-200 scores are unreliable indicators of fitness for
    domain-specific or naturalistic document translation. No Amharic-specific document-level
    evaluation study was found. Source: arXiv:2508.20511 — [WEB-10]'
- gap_id: 3
  description: Ethiopian federal and regional administrative vocabulary coverage in
    NLLB training corpora
  search_target: Whether federally standardized land and credit terminology (per Ethiopian
    proclamations) is present in NLLB's CCAligned or mC4-derived training sets; documented
    mistranslations of official Ethiopian administrative terms
  search_result: 'NOT DIRECTLY CONFIRMABLE. NLLB''s Hugging Face model card explicitly
    states: ''Our model has been tested on the Wikimedia domain with limited investigation
    on other domains.'' No documentation of Ethiopian government administrative vocabulary
    in NLLB training data was found. The Walia-LLM paper (EMNLP 2024 Findings) noted
    that GPT-4 ''encounters some challenges in evaluating machine translation, often
    missing grammatical details in Amharic sentences,'' suggesting quality evaluation
    of Amharic MT is itself unreliable. Source: NLLB Hugging Face model card — [WEB-11];
    WaliaLLM paper — [WEB-12]'
- gap_id: 4
  description: Annotator provenance for Amharic in Flores-200
  search_target: Who translated the Amharic portion of Flores-200 (professional generalist
    vs. domain specialists), what quality controls were applied, and whether post-publication
    audits of Amharic translation quality exist
  search_result: 'PARTIAL — CORRECTIONS EXIST FOR SOME AFRICAN LANGUAGES BUT NOT AMHARIC
    SPECIFICALLY. A 2024 study (Abdulmumin et al., 2024) corrected errors in several
    African language splits of FLORES-200 including Hausa, Sepedi, Xitsonga, and isiZulu,
    using token-level divergence statistics. No Amharic-specific correction or audit
    paper was found. The NLLB paper (Nature 2024) confirms the general workflow: 4-phase
    process, 90% quality threshold, professional translators with 2–5 years experience,
    relaxed thresholds for low-resource languages where qualified reviewers were scarce.
    No documentation of domain expertise requirements specifically for Amharic translators.
    Source: Nature NLLB paper — [WEB-13];
    Flores-200 African language corrections noted in — [WEB-14]'
- gap_id: 5
  description: Sub-national Amhara regional register variation and ACSI/ADCSI vocabulary
  search_target: Whether NLLB evaluation data or training corpora reflect regional
    administrative register differences within Amhara; whether ACSI/ADCSI parallel
    text is publicly available as domain reference data
  search_result: 'NOT FOUND — No ACSI or ADCSI Amharic terminology guides or parallel
    text corpora found in any public repository. ACSI official website (acsi.org.et)
    provides institutional background only. No academic study of sub-national Amhara
    administrative register variation was found. This confirms the absence of any
    domain reference data against which NLLB translations of ACSI/ADCSI documents
    could be validated. Source: ACSI official website — [WEB-15];
    FinDev Gateway ACSI profile — [WEB-16]'
- gap_id: 6
  description: Mistranslation risk in legal-financial numerical and conditional content
    for Amharic
  search_target: Documented cases of NLLB or similar MT systems mistranslating numerical
    or conditional legal content in Amharic or other low-resource African languages;
    whether any evaluation framework assesses false precision in financial clause
    translation
  search_result: 'NO AMHARIC-SPECIFIC CASES FOUND. The 2025 ''Languages Still Left
    Behind'' paper (arXiv:2508.20511) found that in Flores+ human evaluation, only
    1 out of 50 Jinghpaw sentences was judged correctly translated by a native speaker,
    and annotators reported many source sentences were ''highly domain-specific or
    culturally loaded, making them difficult to translate naturally.'' For Tigrinya
    (closely related Semitic language), a memory-efficient NLLB study found over-generation
    artifacts when translating to English. No framework for assessing false precision
    in numerical financial clauses in any low-resource language was found. Source:
    arXiv:2508.20511 — [WEB-10]'
- gap_id: 7
  description: Amhara region infrastructure and connectivity data
  search_target: Current rural internet penetration, mobile network coverage, electricity
    access, and literacy rates for the Amhara region of Ethiopia, disaggregated by
    rural/peri-urban where possible
  search_result: 'PARTIALLY RESOLVED — See infrastructure_notes.connectivity fields
    above. National figures confirmed; Amhara-specific disaggregated figures not publicly
    available. Key finding: Amhara region experienced documented mobile internet shutdowns
    (August 2023–July 2024 and April–May 2023) due to conflict, representing a concrete
    deployment risk for connected translation pipelines. Sources: Freedom House 2024
    — [WEB-7]; Freedom House
    2023 — [WEB-8]; World Bank
    electricity data — [WEB-9]'
- gap_id: 8
  description: ACSI and ADCSI service area scope and borrower population
  search_target: Current ACSI and ADCSI active borrower counts in Amhara region; geographic
    scope of ACSI vs. ADCSI service areas within Amhara zones; whether ACSI/ADCSI
    publish standardized Amharic-language financial terminology guides
  search_result: 'PARTIALLY RESOLVED — ACSI: approximately 1,056,390 active borrowers
    per 2018 World Bank microfinance performance assessment; operates in all 10 Amhara
    administrative zones with 461 branches; constitutes ~28.1% of Ethiopia''s microfinance
    borrowing clients. More recent estimates cite ~2 million clients in rural Ethiopia.
    No post-2020 official ACSI annual report with updated borrower counts found in
    public sources. ADCSI serves Addis Ababa and surrounding areas; no Amhara-specific
    ADCSI figure found. No Amharic financial terminology guides published by either
    institution in public domain. Sources: Springer article 2023 — [WEB-1];
    Academia.edu — [WEB-2]'
net_new_fields:
  amharic_nlp_ecosystem_2024:
    summary: As of 2024, Amharic is the best-resourced Ethiopian language for NLP,
      with EthioLLM (multilingual LLM for 5 Ethiopian languages + EthioBenchmark across
      NER, sentiment, MT, QA) and EthioMT (parallel corpora for 15 Ethiopian languages)
      released. However, all available Amharic NLP benchmarks cover general-domain,
      news, or social media content; no benchmark covers agricultural, administrative,
      or financial domains. This confirms the absence of any community-validated reference
      data for the deployment's core document types.
    source: EthioLLM arXiv:2403.13737 — [WEB-3]; EthioMT
      arXiv:2403.19365 — [WEB-4]
  flores_benchmark_domain_mismatch_evidence_2025:
    summary: A 2025 study ('Languages Still Left Behind', arXiv:2508.20511) found
      that NLLB models fine-tuned on naturalistic domain data outperformed Flores+
      baselines on domain-appropriate test sets but performed worse on Flores+ itself,
      demonstrating that Flores+ scores do not reliably predict out-of-domain translation
      quality. The study also found mock translations reproducing named entities scored
      non-trivially on BLEU and ChrF++, confirming that these metrics can reward superficial
      rather than accurate translation. This provides direct empirical support for
      the benchmark fitness concerns flagged in this assessment.
    source: arXiv:2508.20511 — [WEB-10]
  amhara_connectivity_disruption_risk:
    summary: Amhara region experienced documented mobile internet and phone line shutdowns
      affecting 19 cities from August 2023, with restrictions not fully lifted until
      July 2024, and a prior blackout in April–May 2023. Fixed-line internet remained
      nominally accessible but is uncommon in rural areas. Any deployment pipeline
      requiring connected document translation must account for this as a recurring
      operational risk specific to the Amhara deployment context.
    source: Freedom House Freedom on the Net 2024 — [WEB-7]
  flores_african_language_correction_efforts:
    summary: Post-publication correction work (Abdulmumin et al., 2024) has identified
      and corrected translation errors in several African FLORES-200 language splits
      (Hausa, Sepedi, Xitsonga, isiZulu). No corresponding Amharic correction study
      was found, but the pattern of errors in related African languages — attributed
      to lower standardization and professional translator scarcity — is consistent
      with known NLLB quality challenges for low-resource languages and warrants targeted
      human audit of the Amharic Flores-200 data.
    source: Emergent Mind FLORES-200 topic page summarizing Abdulmumin et al. 2024
      — [WEB-14]
```

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

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark under assessment may cover specific document genres that differ from your deployment's targets. Your deployment targets agricultural input subsidy notices, land-use policy updates, and credit-scheme terms — genres with distinctive bureaucratic phrasing, legal terminology, and numbered clause structures. Are there document types in your deployment that combine legal/regulatory language with agricultural or financial jargon in ways that may differ substantially from the benchmark's coverage?
A1: The benchmark's evaluation data (Flores-200) covers health and IT domains; the deployer acknowledges it does not cover agricultural domains. The deployer does not expect substantial structural differences at the document level, but does anticipate domain-specific terminology in agriculture that the benchmark has not explicitly evaluated.

Q2 [IC]: Government and lender documents in Amhara often carry culturally specific concepts — cooperative membership tiers, traditional land-tenure categories, regionally named subsidy schemes. Would your target documents contain terminology like these that requires locally grounded Amharic equivalents rather than direct transliterations or generic terms?
A2: The deployer confirms culturally specific concepts exist but notes that Ethiopian agricultural land-tenure terminology has been substantially standardized through federal and regional proclamations, which have replaced many traditional local terms with official administrative vocabulary. Some domain-specific terms remain that may not appear in general-purpose translation benchmarks.

Q3 [OC]: For your deployment, who should be the authority on whether an Amharic translation of a subsidy notice or loan agreement is correct and trustworthy — federal bureau translators, regional bureau staff, cooperative extension workers, or the farmer leaders and borrowers themselves?
A3: The deployer considers domain-trained federal bureau translators as the primary authority; in their absence, regional bureau staff and cooperative extension workers are acceptable fallbacks. The deployer implicitly treats the cooperative leaders and borrowers as end-consumers of translation rather than validation authorities, though administrative vocabulary familiar to those users matters for practical uptake.

Q4 [OF]: Do target users need translated output that preserves the original document structure — numbered clauses, tables of subsidy rates, signature blocks — or is flowing prose acceptable? Must layout be mirrored exactly for legal and administrative compliance?
A4: The deployer's answer is modality-contingent: if the model is multimodal and can process document layout, full structural preservation (tables, numbered clauses, etc.) is expected; if the model is text-only, flowing prose translation is acceptable. This deployment uses a text-only model (NLLB), so prose output without layout preservation is considered acceptable.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | Flores-200 evaluation data covers health and IT domains, not agricultural policy or financial/credit genres, creating a direct coverage gap for the deployment's core document types. |
| IC | HIGH | Deployment involves normatively consequential content (binding subsidy and loan terms) and the benchmark contains no validated agricultural or Ethiopian bureaucratic content; federally standardized terminology partially mitigates but does not eliminate culturally specific instantiation risk. |
| IF | LOWER | Both benchmark and deployment are text-only; no script, infrastructure, or modality mismatch — Amharic (Ethiopic script) is present in NLLB's 200-language scope. |
| OO | HIGH | NLLB/Flores-200 scores translation quality against general-domain held-out sentences; no output scoring rubric exists for domain-consistent rendering of agricultural jargon, subsidy eligibility conditions, or loan penalty clauses, meaning metric scores may not reflect fitness for this use case. |
| OC | HIGH | Flores-200 reference translations were produced by professional translators against general-domain sentences; ground-truth labels are not annotated by domain-trained Ethiopian agricultural or financial translation specialists, creating a clear annotator-population mismatch for this deployment. |
| OF | LOWER | User confirmed that flowing prose text output is acceptable given a text-only model; the benchmark's text output format aligns with this relaxed requirement, reducing structural format mismatch risk. |

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
  "benchmark": "nllb",
  "region": "Amhara Region Agricultural and Microfinance Translation Cohort",
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
