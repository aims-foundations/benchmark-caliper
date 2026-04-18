I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **SEA-HELM: A Holistic Linguistic and Cultural LLM Evaluation Suite for Southeast Asian Languages** is valid for use in **indonesia_bahasa_administrative_citizen**.

Analyze the benchmark documentation and regional context below against each of the 6 validity dimensions. For each dimension, assign a score (1-5), provide justification with evidence quotes, respond to each checklist item, and identify information gaps.

### Critical Constraints

- **Document-grounded only**: Base your analysis ONLY on evidence found in the provided benchmark documentation and the factual regional context given. Do NOT role-play as a member of the target culture or speculate beyond what the documentation supports.
- **Cite evidence**: For each finding, quote or reference specific parts of the benchmark documentation.
- **Flag gaps explicitly**: When information is missing from the documentation, say "INSUFFICIENT DOCUMENTATION" and describe what would be needed.
- **Distinguish documentable vs. expert-needed**: Classify each finding as either (a) determinable from documentation, or (b) requiring regional expert verification.
- **Regional specificity**: Evaluate validity *for the specified target region*, not in general.
- **Conservative scoring**: When evidence is ambiguous or insufficient, score lower rather than higher.

### Scoring Rubric

- **1**: Major validity violations identified; benchmark component fundamentally misaligned with target context.
- **2**: Significant concerns; multiple concrete violations or gaps identified.
- **3**: Partially addressed; mixed evidence; some alignment, some gaps.
- **4**: Well addressed; minor concerns or gaps; documentation shows awareness of regional needs.
- **5**: Fully addressed; no concerns identified; documentation demonstrates explicit validity-preserving practices.

### Quote Provenance Rules

The benchmark documentation below contains two types of text:

- **Verbatim quotes** from the original paper, listed in the "Verbatim Quote Registry"
  section with IDs (Q1, Q2, ...), page numbers, and exact text. These are
  **authoritative evidence** extracted directly from the PDF.
- **Interpretive context** in the "Benchmark Documentation" section, written by the
  extraction pipeline. This provides useful framing and references quote IDs like
  [Q3], but is NOT evidence from the paper itself.

When populating `evidence_quotes` in your output JSON:
- ONLY include text from the Verbatim Quote Registry
- Format each entry as: `"[QN] 'exact quote text' (p.X)"`
- Do NOT cite interpretive context as if it were from the paper
- If you cannot find a verbatim quote to support a finding, state this explicitly
  rather than citing paraphrased text

---

## Benchmark Information

- **Name**: SEA-HELM
- **Full Name**: SEA-HELM: A Holistic Linguistic and Cultural LLM Evaluation Suite for Southeast Asian Languages
- **Domain**: Regional LLM evaluation for Southeast Asian languages and cultures
- **Languages**: fil, id, ta, th, vi
- **Porting Strategy**: mixed
- **Year**: 2025

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### 1. Input Ontology
SEA-HELM organizes its evaluation around five core pillars — NLP Classics, LLM-Specifics,
SEA Linguistics, SEA Culture, and Safety — representing a deliberate and granular taxonomy
of the capabilities expected of LLMs deployed in the SEA region [Q1, Q15, Q60]. Within
NLP Classics, the taxonomy further subdivides into three competencies: NLU (question
answering and sentiment analysis), NLG (translation and summarization), and NLR (causal
reasoning and NLI) [Q17]. LLM-Specifics covers instruction-following (SEA-IFEval) and
multi-turn chat (SEA-MTBench), with the latter organized around categories such as
creative writing, mathematics, STEM, and humanities [Q30]. LINDSEA, the SEA Linguistics
pillar, targets a "granular taxonomy of syntactic, semantic and pragmatic phenomena"
handcrafted for SEA languages [Q32]. The SEA Culture pillar addresses culturally-specific
situations Filipino people may encounter in daily life [Q40]. However, the authors
acknowledge that SEA-HELM "is not yet exhaustive in its coverage of languages and tasks"
[Q62], and plan future expansion of language, cultural, and task coverage [Q63, Q67].
A notable gap in input ontology is that the cultural pillar currently covers only Filipino
(KALAHI), with Indonesian, Thai, Vietnamese, and Filipino covered for safety tasks [Q42],
leaving Tamil and some other languages underrepresented in the cultural and safety pillars.

### 2. Input Content
SEA-HELM grounds its input content firmly in the SEA region. The benchmark serves a
region of nearly 700 million speakers across more than 1,000 languages [Q6], and the
five currently supported languages — Filipino, Indonesian, Tamil, Thai, and Vietnamese —
are drawn from this ecosystem [Q2, Q16]. A foundational data selection principle is to
prefer data originally written in native languages, resorting to careful translation by
native speakers only when native-language originals are unavailable [Q18]. SEA-IFEval
was manually translated and crucially localised from the English IF-Eval benchmark to
fit linguistic and cultural nuances of SEA languages [Q22]. Manual translations were
verified for linguistic faithfulness, cultural authenticity, and relevance [Q23]. KALAHI
consists of 150 high-quality Filipino-language prompts created collaboratively with native
Filipino speakers, representing situations Filipino people can reasonably encounter in
daily life [Q40]. Newly created datasets (SEA-IFEval, SEA-MTBench, LINDSEA) are released
under CC-BY-SA 4.0 [Q12]. The use of translated datasets is flagged as a potential
concern: "translated datasets often contain elements of translationese (Gellerstam, 1986),
which can differ significantly from natively written text" [Q19]. Community participation
by native speakers at each stage of dataset planning and construction is a stated design
principle [Q13]. Prior cultural evaluation work is critiqued for not starting from
consulting speaker communities and for relying on aggregate reference sources that "cannot
comprehensively represent the complex nature of culture" [Q37, Q38]; SEA-HELM responds
with a participatory approach [Q39].

### 3. Input Form
SEA-HELM is a text-based benchmark and explicitly addresses script-level mismatches
between its constituent inputs and the diverse writing systems of the SEA region. SEA-IFEval
construction involved filtering out instructions inapplicable to SEA scripts — for example,
"prompts asking to change the capitalisation or punctuation do not make sense in many scripts
in the region, such as Burmese, Tamil, or Thai" [Q24]. Letter-count instructions were
converted to number-count instructions to handle non-Latin scripts: e.g., requiring a
specific letter to appear at least six times was adapted to require a specific numeral [Q25].
Each evaluation prompt is given in the target language rather than in English (except for
English tasks) and is manually translated by native speakers [Q46]. An example Vietnamese
instruction-following prompt is provided in the appendix [Q84], and Indonesian-language
prompt templates are likewise shown [Q85, Q86]. The instruction-following metric penalises
responses in the wrong language by multiplying accuracy by the rate at which the model
responds in the correct target language [Q27]. LINDSEA examples are handcrafted from
scratch rather than automatically generated, to ensure they "sound natural, are semantically
coherent and target the relevant phenomena effectively" [Q34].

### 4. Output Ontology
SEA-HELM employs distinct output taxonomies tuned to task type. For the SEA Culture pillar,
KALAHI responses are classified as either culturally-relevant (helpful and harmless within
the given culture) or culturally-irrelevant (unhelpful and harmful within a culture) [Q87] —
a binary taxonomy explicitly grounded in cultural context rather than generic helpfulness.
For LINDSEA syntactic minimal pair tasks, a binary forced-choice label schema (A or B) is
used, while pragmatic reasoning tasks use true/false labels [Q85, Q86]. For multi-turn chat
(SEA-MTBench), judging criteria include accuracy, relevance, and coherence [Q31]. Instruction-
following accuracy penalises wrong-language responses, ensuring the output taxonomy rewards
culturally and linguistically appropriate outputs [Q27, Q47]. The authors acknowledge that
"it is not possible to enumerate every type of unsafe response in real-world scenarios" [Q68],
so the safety evaluation taxonomy is framed as necessary but not sufficient [Q69]. The
framework's explicit goal is "fair, transparent, and authentic multilingual and multicultural
evaluations" [Q14], with the output taxonomy designed to reflect regional deployment realities
rather than English-centric defaults.

### 5. Output Content
SEA-HELM makes strong efforts to ground its labels and ground-truth in regional stakeholder
perspectives. The benchmark involves native speakers at each stage of dataset planning and
construction [Q13], and the QA team consists of paid native speakers of SEA languages who
worked as translators and annotators [Q70]. LINDSEA examples are handcrafted by linguists
in collaboration with native speakers and iteratively reviewed [Q34]. Manual translations
for SEA-IFEval were verified for linguistic faithfulness, cultural authenticity, and
relevance [Q23]. The QA team was recruited through public advertisements, composed
predominantly of students at local universities and members of the public who are adults
[Q72, Q73]. Participation was voluntary, PII was removed, and participants could withdraw
at any time [Q74, Q75, Q77, Q78]. The project received full IRB approval [Q71]. Annotator
demographics are withheld for anonymity but available upon request [Q20]. Workers were not
involved in the construction of sensitive SAFETY pillar data [Q76]. A methodological
limitation is that leaderboard results are based on single model runs without error bars,
though the authors argue deterministic evaluation (temperature=0) justifies this approach
in line with common benchmark practice [Q64, Q65].

### 6. Output Form
SEA-HELM evaluates text-based model outputs exclusively, appropriate for the target
languages and their high-literacy written traditions. Instruction-following accuracy
is computed using the same verifiers as English IF-Eval, then adjusted by the rate
of correct-language responses [Q27]. Models that fail to append the required answer
tag are deemed to have given a null response [Q45], enabling efficient automatic
evaluation at scale even for verbose models. For multiple-choice tasks, answer options
are extracted via regular expressions and compared against gold labels [Q44]. SEA-MTBench
uses an LLM-as-a-Judge paradigm with gpt-4-1106-preview as judge, comparing each
candidate model's win rate against gpt-3.5-turbo-0125 [Q29, Q31]. Scores are normalized
by subtracting a random baseline and rescaling to 0–100, with negative scores clamped to
zero [Q49, Q50]. Aggregation proceeds from task level to competency level to language level
to a final SEA average [Q51, Q52]. Instruction-tuned models are evaluated zero-shot;
pre-trained models use 5-shot examples [Q48].


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "SEA-HELM, a holistic linguistic and cultural LLM evaluation suite that emphasises SEA languages, comprising five core pillars: (1) NLP CLASSICS, (2) LLM-SPECIFICS, (3) SEA LINGUISTICS, (4) SEA CULTURE, (5) SAFETY." |
| Q2 | 1 | input_content | "SEA-HELM currently supports Filipino, Indonesian, Tamil, Thai, and Vietnamese." |
| Q3 | 1 | output_form | "We also introduce the SEA-HELM leaderboard, which allows users to understand models' multilingual and multicultural performance in a systematic and user-friendly manner." |
| Q4 | 1 | output_ontology | "Traditional approaches to NLP evaluation, which emphasise on alignment with a predefined ground truth reference, are not sufficient in measuring the complex abilities of LLMs." |
| Q5 | 1 | input_content | "This gap is further exacerbated in lower-resource languages in South East Asia (SEA), owing to a lack of both training and testing data on the internet." |
| Q6 | 1 | input_content | "The SEA region is home to nearly 700 million speakers across more than 1,000 languages." |
| Q7 | 1 | input_content | "While this region represents almost 10% of the global population and constitutes approximately one-seventh of the world's total languages, most of these languages remain unsupported by major LLMs, such as Mistral (Mistral AI, 2023) and Claude (Anthropic, 2023)." |
| Q8 | 1 | output_content | "Yosephine Susanto, Adithya Venkatadri Hulagadri, Jann Railey Montalan, Jian Gang Ngui, Xian Bin Yong, Weiqi Leong, Hamsawardhini Rengarajan, Peerat Limkonchotiwat, Yifan Mai, William Chandra Tjhi from AI Singapore, National University of Singapore, and Center for Research on Foundation Models (CRFM), Stanford University." |
| Q9 | 1 | output_form | "We make the SEA-HELM evaluation code publicly available." |
| Q10 | 2 | input_ontology | "Over the years, AI practitioners have employed either an individual task-based or, more rarely, a holistic approach to assess the performance and capabilities of LLMs." |
| Q11 | 2 | input_ontology | "Popular tasks for evaluating LLMs include translation (Hendy et al., 2023), summarisation (Zhang et al., 2023), decision-making (Shen et al., 2023), detecting scalar implicatures (Jeretic et al., 2020; Pandia et al., 2021; Hu et al., 2023; Liu et al., 2023)" |
| Q12 | 2 | input_content | "We release SEA-IFEval, SEA-MTBench and LINDSEA datasets under the Creative Commons Attribution Share-Alike 4.0 (CC-BY-SA 4.0) license." |
| Q13 | 2 | output_content | "We deliberately incorporate community participation by involving native speakers of the SEA languages at each stage of the dataset planning and construction to ensure linguistic accuracy and cultural authenticity." |
| Q14 | 2 | output_ontology | "The five pillars are also meticulously and rigorously crafted to achieve fair, transparent, and authentic multilingual and multicultural evaluations of LLMs in the region." |
| Q15 | 3 | input_ontology | "This evaluation suite consists of five core pillars: (1) NLP CLASSICS, (2) LLM-SPECIFICS, (3) SEA LINGUISTICS, (4) SEA CULTURE, and (5) SAFETY, and has been recently integrated with HELM." |
| Q16 | 3 | input_content | "SEA-HELM currently supports five SEA languages – Filipino, Indonesian, Tamil, Thai, and Vietnamese, enabling users and AI practitioners to assess the overall performance of LLMs for these languages." |
| Q17 | 3 | input_ontology | "First, for the Natural Language Understanding (NLU) competency, we include QA (extractive question answering) and sentiment analysis tasks. Second, for the Natural Language Generation (NLG) competency, we include translation (English to native language and native language to English) and abstractive summarisation tasks. Third, for the Natural Language Reasoning (NLR) competency, we include causal reasoning and natural language inference (NLI) tasks." |
| Q18 | 3 | input_content | "We selected datasets that comprised of data originally written in the native language as far as possible. Otherwise, existing datasets in English were carefully translated by native speakers." |
| Q19 | 3 | input_form | "This is important because translated datasets often contain elements of translationese (Gellerstam, 1986), which can differ significantly from natively written text (Baker, 1993; Lembersky et al., 2012; Volansky et al., 2015; Riley et al., 2020)." |
| Q20 | 3 | output_content | "Annotator demographics are not included in this paper for anonymity, demographics can be provided upon request." |
| Q21 | 3 | output_form | "With LLMs enabling unprecedented NLP applications, there is a need to develop automated, dedicated evaluation metrics for these higher-order tasks. SEA-HELM focuses on two specific capabilities - the ability to follow human" |
| Q22 | 4 | input_content | "SEA-IFEval is an instruction-following benchmark we created collaboratively with native speakers. It was manually translated from the English IF-Eval benchmark (Zhou et al., 2023) and, crucially, localised to fit the linguistic and cultural nuances of SEA languages." |
| Q23 | 4 | output_content | "Manual translations ensured faithful and accurate linguistic representation, while localisation ensured cultural authenticity and removed any unintended or inherent biases. Additionally, this involved manually verifying that each sample was relevant and applicable to the languages concerned." |
| Q24 | 4 | input_form | "Specifically, to create the SEA-IFEval dataset, we first filtered out instructions that could not reasonably apply to most SEA languages. For example, prompts asking to change the capitalisation or punctuation do not make sense in many scripts in the region, such as Burmese, Tamil, or Thai." |
| Q25 | 4 | input_form | "We also changed instructions that required inclusion of a stated quantity of instances of letters to instead require a stated quantity of instances of numbers as it was not easy to localise them for non-Latin scripts. An example of this change is to convert the instruction of "[respond] with the letter 'l' appearing at least 6 times" to "[respond] with the number '4' appearing at least 6 times." |
| Q26 | 4 | input_form | "Thus, by filtering out and adapting instructions given the SEA context, we ensure a fair basis of comparison for the instruction-following competency." |
| Q27 | 4 | output_form | "The accuracy with which LLMs follow the exact instruction following requirements is calculated using the same verifiers as those found in the English IF-Eval benchmark (Zhou et al., 2023). The model's accuracy is then adjusted to penalise instructions that responded in the wrong language by multiplying its accuracy with the rate at which it responds in the correct target language." |
| Q28 | 4 | input_content | "SEA-MTBench is a manually translated and localised version of the popular MT-Bench dataset (Zheng et al., 2023), which also introduced the paradigm of LLM-as-a-Judge to approximate human preferences." |
| Q29 | 5 | output_form | "grading approach, where we compare the win-rate of each candidate model against a fixed reference model, namely gpt-3.5-turbo-0125. The models' responses were compared with the reference response using gpt-4-1106-preview as the judge model. This setup sees the number of judge calls scale linearly with the number of models being compared, whereas pairwise comparisons would scale quadratically." |
| Q30 | 5 | input_ontology | "Models receive an initial prompt based on a category such as creative writing, mathematics, STEM or humanities. They are then given a follow-up instruction which related to the initial prompt, and are expected to respond appropriately." |
| Q31 | 5 | output_ontology | "Finally, a model's responses to both the initial and follow-up prompts are evaluated as a whole given accuracy, relevance, and coherence as judging criteria. Results are reported based on each model's average win rate against the reference model." |
| Q32 | 5 | input_ontology | "As one of the five core evaluation pillars, LINDSEA (LINguistic Diagnostics for SouthEast Asian languages) is a high quality, manually-crafted linguistic dataset that systematically diagnoses models' language proficiency and grammatical understanding based on a granular taxonomy of syntactic, semantic and pragmatic phenomena. It is also the first to be created for SEA languages." |
| Q33 | 5 | input_ontology | "The design of LINDSEA is based on three principles: breadth, depth, and quality." |
| Q34 | 5 | output_content | "That is, rather than using a small set of lexical items and grammatical rules to automatically generate large numbers of test sentences, the examples in LINDSEA are handcrafted from scratch by linguists in collaboration with native speakers and reviewed iteratively to ensure that they sound natural, are semantically coherent and target the relevant phenomena effectively (quality)." |
| Q35 | 5 | input_ontology | "While there are existing syntactic and semantic diagnostic datasets for English (Warstadt et al., 2020; Jeretic et al., 2020; Liu et al., 2023), Mandarin (Xiang et al., 2021) and even Japanese (Someya and Oseki, 2023), none yet exist for SEA languages, and, to our knowledge, there has yet to be such an extensive coverage of linguistic phenomena in any dataset." |
| Q36 | 5 | input_content | "Cultural representation and bias have also become increasingly important with LLM use (Adilazuarda et al., 2024) since a lack thereof can potentially cause social harm (Solaiman et al., 2023)." |
| Q37 | 5 | output_content | "Much prior work on analysing or evaluating cultural representation in LLMs is created in ways that do not start from consulting the communities of speakers of the language but instead starts from reference sources that aggregate cultural knowledge, opinions, and values at a population level." |
| Q38 | 6 | output_content | "Such datasets are inherently limited and cannot comprehensively represent the complex nature of culture (Causadias, 2020), even if they can capture aggregated value alignment." |
| Q39 | 6 | output_content | "Thus, we place emphasis on a strong participatory approach that includes the native speaker communities in order to authentically represent the target culture." |
| Q40 | 6 | input_content | "The KALAHI dataset is designed to determine if LLMs can provide culturally-relevant responses to culturally-specific situations that Filipino people can reasonably encounter in their daily lives, and the dataset is composed of 150 high-quality Filipino-language prompts created in collaboration with native Filipino speakers." |
| Q41 | 6 | output_ontology | "Multilingual inputs, especially when given in lower-resource languages such as those in the SEA region, can increase the likelihood that LLMs produce unsafe responses (Song et al., 2024; Shen et al., 2024)." |
| Q42 | 6 | input_ontology | "Currently, we cover Indonesian, Thai, Vietnamese, and Filipino for this task." |
| Q43 | 6 | output_form | "For each task, we opted to be explicit in instructing the LLM to output the answer following a specified format." |
| Q44 | 6 | output_form | "The answer can then be extracted using regular expressions and compared against the corresponding gold label." |
| Q45 | 7 | output_form | "tag to its answer, the model is deemed to have given a null response. This approach allows for more efficient automatic evaluation at scale, even for models that may tend to have lengthy outputs." |
| Q46 | 7 | input_form | "It should also be noted that each prompt is given in the target language rather than in English (except for the English tasks) and is manually translated by native speakers of each language." |
| Q47 | 7 | output_ontology | "In our view, for full SEA languages support, an LLM should be able to output coherent responses and should also be able to correctly interpret native instructions." |
| Q48 | 7 | output_form | "Instruction-tuned models were evaluated in a zero-shot manner while pre-trained models are evaluated with 5-shot examples." |
| Q49 | 7 | output_form | "As per equation 1, the normalised metric score (snorm) is calculated by subtracting the random baseline score (sbaseline) from the raw metric score (sraw). This is then divided by the difference between the maximum score (smax) and the random baseline score. The range of the normalised score is then scaled to a range of 0–100 (Hulagadri et al., 2025). For negative normalised score, we set the score to 0." |
| Q50 | 7 | output_form | "For multiple-choice task with n options, the baseline score using a random strategy is (100/n)%. For open ended questions with a score range between 0–1, we set the guessing score to 0% and the best possible score to 100%." |
| Q51 | 7 | output_form | "First, metrics are aggregated at the competency level. The normalised scores of each tasks belonging to each competency are averaged to calculate the competency score (The list of tasks in each competency can be found in Table 1). This is done since some competencies have more tasks than others, and if the final language average score was taken from all available tasks, some competencies would be over-represented." |
| Q52 | 7 | output_form | "Next, the language score is calculated by taking the average of the competency scores for each language. This provides an indication of how well the models are performing at a per-language basis Finally, a SEA average score is calculated as the mean of all the language score in SEA-HELM." |
| Q53 | 8 | output_form | "Of all the open-sourced models tested, DeepSeek-R1 was the strongest performing model and showed comparable results to gpt-4o-2024-08-06 on the SEA-HELM suite (Figure 2a, Table 2)." |
| Q54 | 8 | input_content | "Given the large size of DeepSeek-R1 (671B), finding comparisons to other models that support SEA languages was not trivial." |
| Q55 | 8 | output_form | "Thus, we chose to focus our discussion on LLMs of sizes ranging between 7-9B parameters (See Table 2 for the full list of models) and used both the DeepSeek-R1 and gpt-4o-2024-08-06 as the reference models for what was the best available open-sourced and closed-sourced model respectively." |
| Q56 | 8 | output_form | "We also observe that the gap between the smaller models and the reference models is closing, as evidenced by the smaller gap between gpt-4o-2024-08-06 with the newer LLaMA model Llama-3.1-8B-Instruct as compared to the earlier LLaMA model Meta-Llama-3-8B-Instruct (Figure 2a, 2b, Table 2)." |
| Q57 | 8 | output_form | "Notably, continued pre-training and further tuning for the SEA languages resulted in this gap closing even further (Figure 2b; llama3.1-8b-cpt-sea-lionv3-instruct compared against Llama-3.1-8B-Instruct)." |
| Q58 | 8 | input_content | "This suggests that there is still room for improvement and spending the effort to train LLMs to target the specific SEA languages can result in models that are more suited for the SEA region and thus work better for the region's use cases." |
| Q59 | 9 | input_ontology | "In conclusion, we introduce SEA-HELM, a holistic evaluation suite that caters to the SEA languages and cultures." |
| Q60 | 9 | input_ontology | "To achieve a comprehensive evaluation suite, SEA-HELM was designed around the following five core pillars: (1) NLP CLASSICS, (2) LLM-SPECIFICS, (3) SEA LINGUISTICS, (4) SEA CULTURE, (5) SAFETY." |
| Q61 | 9 | input_content | "Our results show that there are still significant gaps between high-resource languages such as English and the mid- to low-resource languages in Southeast Asia, including several with official status and millions of speakers." |
| Q62 | 9 | input_ontology | "While aiming to achieve holistic and authentic evaluations for LLMs in Southeast Asia, SEA-HELM is not yet exhaustive in its coverage of languages and tasks." |
| Q63 | 9 | input_ontology | "As we iteratively improve the coverage of the various SEA-HELM pillars, more language and cultural coverage will added and refined in the future." |
| Q64 | 9 | output_form | "Our leaderboard results are based on single model runs." |
| Q65 | 9 | output_form | "However, as we have assumed deterministic model behaviour and set every model's temperature to 0, we did not publish error bars for the results, in line with most other benchmarks in the field." |
| Q66 | 9 | input_ontology | "We recognise that although SEA-HELM currently covers Filipino, Indonesian, Tamil, Thai, and Vietnamese, we still have much more work to do and therefore we are committed to iteratively expanding each pillar." |
| Q67 | 9 | input_ontology | "Specifically, we plan to expand SEA-HELM to include a broader range of languages, cultures, tasks and models to encourage stronger SEA representation in models." |
| Q68 | 10 | output_ontology | "acknowledge that passing our evaluations with a high score is not necessarily a guarantee of the safety of an LLM in the SEA context, as it is not possible to enumerate every type of unsafe response in real-world scenarios." |
| Q69 | 10 | output_ontology | "Thus, passing the safety evaluations in SEA-HELM must be seen as a necessary but not sufficient requirement for ensuring safety in real-world LLM applications." |
| Q70 | 10 | output_content | "SEA-HELM is grateful to our Quality Assurance (QA) team, consisting of paid native speakers of SEA languages who worked as translators and annotators, enabling us to construct localised datasets needed for this research." |
| Q71 | 10 | output_content | "The SEA-HELM project has received full and official approval from our university's internal review board after undergoing a rigorous review process, and the compensation and working hours for all members involved were established in full compliance with the prevailing university guidelines and applicable regulations in the country where this research is conducted." |
| Q72 | 10 | output_content | "Our QA team was recruited through public advertisements that clearly outlined the estimated workload and hourly pay, consistent with all relevant legal and regulatory requirements." |
| Q73 | 10 | output_content | "The team is composed predominantly of students at local universities and members of the public, all of whom are adults who satisfy the legal age requirements for employment, as defined by the labour laws of the country." |
| Q74 | 10 | output_content | "Although participants are compensated for their participation, their involvement in the study is entirely voluntary." |
| Q75 | 10 | output_content | "Any personally identifiable information (PII) is removed from the data collected and will not be tied to their identity." |
| Q76 | 10 | output_content | "We did not estimate that their work involved significant risks of exposure to offensive material, as they were not involved in the construction of sensitive data such as those under the SAFETY pillar." |
| Q77 | 10 | output_content | "Nonetheless, they were encouraged to report inappropriate samples and were given the option to withdraw their participation at any time, including after its completion, without any negative consequences or loss of benefits." |
| Q78 | 10 | output_content | "If they chose to withdraw, they could do so without providing any reason, and all data collected from the withdrawn individual were excluded from this research." |
| Q79 | 10 | output_content | "We do not foresee negative social impacts from our research, for our research introduces evaluation datasets in SEA languages by working with native speakers, paying due respect to local cultural sensitivities." |
| Q80 | 10 | output_content | "We thus do not believe that our research will contribute to over-generalisations regarding SEA cultures." |
| Q81 | 10 | output_content | "This research/project is supported by the National Research Foundation, Singapore under its National Large Language Models Funding Initiative." |
| Q82 | 19 | input_content | "Supported SEA Languages comprises of tested languages that are reported on the respective model cards or reports." |
| Q83 | 23 | input_ontology | "SEA-IFeval Categories with descriptions, each with 5 samples. Sourced from Zhou et al. (2023)" |
| Q84 | 23 | input_form | "An example of a Vietnamese instruction following prompt from SEA-IFEval. The target constraint in this particular instruction is that the response must repeat the phrase before proceeding to give the summary." |
| Q85 | 25 | output_ontology | "Anda adalah seorang ahli bahasa Indonesia. Jawablah hanya dengan menggunakan format berikut ini: Jawaban: $OPTION Ganti $OPTION dengan pilihan yang telah dipilih. Gunakan huruf A atau B saja sebagai jawabannya." |
| Q86 | 25 | output_ontology | "Anda adalah seorang ahli bahasa Indonesia Jawablah hanya dengan menggunakan format berikut ini: Jawaban: $OPTION Ganti $OPTION dengan benar atau salah." |
| Q87 | 26 | output_ontology | "Each sample is composed of a prompt and a list of responses that are culturally-relevant (helpful and harmless within the context of the given culture) and culturally-irrelevant (unhelpful and harmful within a culture)." |
| Q88 | 26 | input_content | "Each prompt is contains a query representing a unique situation that a Filipino may encounter, information regarding the person posing that question, and the person's personal context." |

---

## Target Region

- **Name**: indonesia_bahasa_administrative_citizen

### Regional Context

```yaml
region:
  country: Indonesia
  primary_language: Bahasa Indonesia (id)
  language_register_scope: formal and informal, including Betawi-inflected, Sundanese-inflected,
    and Javanese-influenced colloquial input; formal plain-language output required
  script: Latin (standard Indonesian orthography; EYD/PUEBI)
  primary_region: Indonesia — national deployment with sub-national variation
  sub_regions_of_concern:
  - DKI Jakarta (Jakipedia/JakEVO digital infrastructure; Betawi-inflected input)
  - West Java / Sleman area (Sundanese-inflected input)
  - East Nusa Tenggara (NTT; outer-island, lower digital literacy, distinct procedural
    flows)
  - Eastern Indonesia broadly (Sulawesi, Maluku, Papua; procedural and access variation)
deployment:
  use_case: Public-facing government chatbot answering citizen questions about administrative
    procedures — KTP/e-KTP applications, DJP Online/Coretax tax filing, business registration
    (OSS-RBA), and permit renewals
  deploying_entity: Indonesian central government ministry (digital services division)
  interaction_types:
  - step-by-step procedural instruction
  - pre-application document prerequisite checking (e-materai, format requirements)
  - error recovery (rejection, missing documents, unregistered NIK)
  - jurisdictional referral (Dukcapil vs. Imigrasi vs. DJP vs. OSS-RBA)
  - citation and deferral for recently changed regulations
  critical_interaction_types:
  - step-by-step procedural instruction (ranked highest by elicitation)
  - error recovery (ranked highest by elicitation)
  evaluator_tiers:
  - civil servants (Dukcapil, DJP) for procedural correctness
  - ministry legal and policy experts for regulatory compliance
  - ordinary citizens (including low-education, non-Jakarta users) for accessibility/usability
  accessibility_kpi: responses must be understandable to low-education, non-Jakarta
    users; technically accurate but bureaucratically impenetrable answers are explicitly
    failures
regulatory_environment:
  primary_data_regulation:
    name: UU 27/2022 — Undang-Undang Pelindungan Data Pribadi (Personal Data Protection
      Law / PDP Law)
    effective_date: '2022-10-17'
    transition_period_ended: 2024-10-17 (two-year transition ended; full compliance
      now required)
    data_protection_authority_status: PDP Agency (Lembaga PDP) not yet established
      as of April 2026; Presidential Regulation draft in harmonization stage at Ministry
      of Law since October 2025; agency targeted operational in 2026
    key_obligations_for_deployment:
    - consent required for personal data collection and processing (written or recorded,
      in Indonesian language)
    - data minimization and purpose limitation principles apply
    - breach notification within 72 hours to data subject and PDP Agency (currently
      Ministry of Communication and Digital Affairs / MOCD in lieu of PDP Agency)
    - public agency chatbot is a Public Electronic System Operator (PSE Publik) under
      PP 71/2019 — must store and process data within Indonesian territory
    source: Library of Congress Global Legal Monitor 2022-12-18 — https://www.loc.gov/item/global-legal-monitor/2022-12-18/indonesia-personal-data-protection-act-enters-into-force;
      DLA Piper Data Protection Laws of the World (Indonesia, updated Feb 2026) —
      https://www.dlapiperdataprotection.com/?t=law&c=ID
  electronic_systems_regulation:
    name: PP 71/2019 — Peraturan Pemerintah No. 71 Tahun 2019 tentang Penyelenggaraan
      Sistem dan Transaksi Elektronik (Government Regulation on Electronic Systems
      and Transactions)
    effective_date: '2019-10-10'
    replaces: PP 82/2012
    key_provision_for_deployment: Public ESOs (government institutions) must store
      and process electronic systems and data within Indonesian territory; registration
      with Ministry of Communication and Digital Affairs required; data localization
      requirement applies to this deployment as a government chatbot
    status_relative_to_pdp_law: PP 71/2019 remains in force to the extent it does
      not conflict with UU PDP 27/2022; both apply concurrently to this deployment
    source: Google Cloud Indonesia GR 71 compliance page — https://cloud.google.com/security/compliance/indonesia-gr71;
      Regulations.AI entry for PP 71/2019 — https://regulations.ai/regulations/RAI-ID-NA-PPRINXX-2019
  tax_administration_system:
    name: Coretax (Core Tax Administration System / SIAP DJP / CTAS / PSIAP)
    formal_regulation: PMK No. 81/2024 (Ministry of Finance Regulation No. 81 of 2024);
      also regulated under Presidential Decree No. 40/2018 (PSIAP project)
    launch_date: 2025-01-01 (corporate functions including withholding tax and VAT
      invoicing); individual SPT filing via Coretax mandatory for 2025 tax year with
      deadlines March–April 2026
    replaces: DJP Online (pajak.go.id legacy platform) and multiple legacy sub-systems;
      pre-Coretax e-Filing flow now superseded
    parallel_operation: DJP Online retained for 2024 tax year annual returns (filed
      early 2025); e-Faktur desktop retained for some taxpayer categories; full exclusive
      Coretax mandated for 2025 tax year returns filed in 2026
    adoption_status: As of September 2025, approximately 65% of registered taxpayers
      had activated Coretax accounts (DJP official article)
    known_implementation_issues: Documented temporary difficulties in NPWP issuance
      and registration during data migration; ongoing usability challenges reported
      by taxpayers and businesses
    benchmark_validity_implication: Any static benchmark or training corpus predating
      January 2025 encodes the pre-Coretax DJP Online procedural flow, which is now
      superseded. SEA-HELM has no versioning or timestamp mechanism for regulatory
      content; DJP procedural knowledge in training data is likely outdated for this
      deployment.
    source: DJP official article (pajak.go.id) — https://www.pajak.go.id/en/artikel/embracing-digital-future-coretax;
      ASEAN Briefing Coretax guide — https://www.aseanbriefing.com/doing-business-guide/indonesia/taxation-and-accounting/coretax-indonesia;
      LMI Consultancy Coretax guide — https://www.lmiconsultancy.com/indonesia/core-tax-registration-indonesia-djp-coretax-system/
  population_civil_registration:
    key_agencies:
    - Dukcapil (Direktorat Jenderal Kependudukan dan Pencatatan Sipil, Kemendagri)
      — responsible for KTP/e-KTP, NIK registration, IKD (Identitas Kependudukan Digital)
    - Imigrasi (Ditjen Imigrasi) — passports and immigration documents
    digital_identity_infrastructure: Indonesia Digital Public Infrastructure (DPI)
      being tested; biometric authentication via Dukcapil population data; IKD digital
      identity app deployed but adoption uneven (study of Bojonegoro found low readiness)
    regional_variation_note: KTP registration steps and permit requirements differ
      materially between DKI Jakarta (Jakipedia/JakEVO platform), Sleman, Makassar,
      and rural kabupaten — the deployment must not present Jakarta-specific flows
      as universally applicable
    source: GovInsider Asia DPI article (Jan 2026) — https://govinsider.asia/intl-en/article/digital-public-infrastructure-is-changing-how-the-indonesian-government-works
  business_registration:
    system: OSS-RBA (Online Single Submission — Risk-Based Approach)
    note: Managed by BKPM/BKIPM; pemda-level permit variation persists within the
      OSS-RBA framework; benchmark content should be verified for current OSS-RBA
      v2.x procedural flows
population:
  total_population_approx: ~277 million (2023 estimate)
  target_users: Indonesian citizens nationwide using government digital services
  expected_user_concentration:
  - Urban Java (Jakarta, Surabaya, Yogyakarta/Sleman corridor)
  - Outer islands including East Nusa Tenggara (NTT) and eastern Indonesia
  user_education_range: low-education non-urban to urban professional (chatbot is
    a public service with explicit accessibility KPIs)
  language_input_characteristics:
    formal_standard: Bahasa Indonesia (formal register, PUEBI orthography)
    informal_urban: Betawi-inflected colloquial (gue/lu pronouns, Jakarta slang);
      Javanese-influenced phrasing (adem ayem, etc.); Sundanese-influenced phrasing
    eastern_varieties: Manado-influenced speech and other eastern Indonesian colloquial
      varieties
    code_switching: Indonesian-English and Indonesian-Javanese code-mixing common
      in digital communication (documented in NusaDialect research, 2025)
  language_output_requirement: Consistent, polite, plain formal Bahasa Indonesia regardless
    of input register (comprehension-generation asymmetry explicitly required)
nlp_ecosystem:
  existing_indonesian_benchmarks:
  - name: IndoNLU
    year: 2020
    description: 12-task Indonesian NLU benchmark covering sentiment analysis, NER,
      question answering, and other tasks; introduced IndoBERT. No government administrative
      procedure tasks; general-domain.
    source: ACL Anthology AACL-IJCNLP 2020 — https://aclanthology.org/2020.aacl-main.85/
  - name: IndoNLG
    year: 2021
    description: NLG benchmark for Indonesian, Javanese, and Sundanese covering summarization,
      QA, chit-chat, and translation tasks; introduced IndoBART and IndoGPT.
    source: arXiv 2104.08200 — https://arxiv.org/abs/2104.08200
  - name: IndoCulture (Koto et al., 2024)
    year: 2024
    description: Cultural commonsense reasoning benchmark manually developed by local
      people across 11 Indonesian provinces (Aceh, North Sumatra, West Sumatra, West
      Java, Central Java, East Java, Bali, South Borneo, East Nusa Tenggara/NTT, South
      Sulawesi, Papua). Province-level coverage including NTT (relevant for outer-island
      deployment concern). Tasks are sentence-completion MCQ evaluating cultural reasoning.
      SOTA accuracy 76.4 (Sailor2-20B); RAG with IndoSoSci raises this to 79.3.
    validity_relevance: HIGH for IC/OC dimensions — fills the SEA-HELM Indonesian
      cultural pillar gap for cultural commonsense; covers NTT and outer-island provinces
      directly relevant to this deployment; does NOT cover administrative procedure
      content
    limitation: Cultural commonsense reasoning (food, clothing, customs, etc.), not
      government procedure knowledge; MCQ format only; no regulatory compliance dimension
    source: MIT Press TACL (Dec 2024) — https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00726/125984/;
      arXiv 2404.01854 — https://arxiv.org/html/2404.01854
  - name: IndoMMLU (Koto et al., 2023)
    year: 2023
    description: 64-subject multiple-choice benchmark based on Indonesian educational
      curriculum from elementary to university entrance exam level; includes 9 regional
      language/culture subjects; curriculum varies by province.
    validity_relevance: LOW-MEDIUM for this deployment — educational/exam content,
      not government procedure knowledge; useful for general Indonesian language competence
      baseline
    source: AI-Scholar summary — https://ai-scholar.tech/en/articles/large-language-models/indommlu
  - name: IndoCareer (IndoCareer benchmark, 2024)
    year: 2024
    description: 8,834 MCQ from Indonesian professional competency and certification
      exams across 22 professions in 6 categories (healthcare, insurance/finance,
      creative/design, tourism, education, law); first professional-exam benchmark
      for Indonesia.
    validity_relevance: LOW-MEDIUM for this deployment — professional domain but covers
      legal and finance categories; does not include public administration, Dukcapil,
      or DJP procedure content specifically
    source: arXiv 2409.08564 — https://arxiv.org/html/2409.08564
  - name: NusaX
    year: 2022
    description: Multilingual parallel sentiment and MT corpus for 10 Indonesian local
      languages (Acehnese, Balinese, Banjarese, Buginese, Madurese, Minangkabau, Javanese,
      Ngaju, Sundanese, Toba Batak) plus Indonesian and English. Sentiment analysis
      and translation tasks.
    validity_relevance: MEDIUM for IF dimension — covers Javanese and Sundanese as
      regional input languages but tasks are sentiment/MT, not comprehension of colloquial
      input in administrative dialogue contexts
    source: arXiv 2205.15960 — https://ar5iv.labs.arxiv.org/html/2205.15960; IndoNLP
      projects page — https://indonlp.github.io/projects.html
  - name: NusaCrowd
    year: 2023
    description: 137 Indonesian-language datasets unified under standardized loaders;
      covers 19 Indonesian languages; enables zero-shot NLU/NLG benchmarks and first
      multilingual ASR benchmark for Indonesian and local languages.
    validity_relevance: MEDIUM — broad consolidation effort; no government procedure
      domain content identified; useful as resource inventory baseline
    source: ACL Anthology Findings ACL 2023 — https://aclanthology.org/2023.findings-acl.868/
  - name: LoraxBench (Google, 2025)
    year: 2025
    description: 6-task benchmark (reading comprehension, MT, cultural reasoning,
      NLI, cultural QA) across 20 Indonesian languages including several with no prior
      downstream NLP coverage; covers both formal and casual registers for some languages.
    validity_relevance: MEDIUM for IF dimension — addresses formal/casual register
      distinction explicitly; net-new coverage of low-resource regional languages;
      does not cover government procedure domain
    source: arXiv 2508.12459 — https://arxiv.org/html/2508.12459
  - name: ID-MoCQA (multi-hop cultural QA, 2026)
    year: 2026
    description: Multi-hop expansion of IndoCulture requiring province identification
      then province-specific cultural reasoning; built on IndoCulture 11-province
      dataset; bilingual (Indonesian and English).
    validity_relevance: MEDIUM — strengthens province-level cultural evaluation but
      still cultural commonsense domain, not government procedures
    source: arXiv 2602.03709 — https://arxiv.org/html/2602.03709
  - name: IndoSoSci (NTU, 2026)
    year: 2026
    description: Novel text corpus from 151 open-source Indonesian social science
      journals; used for RAG injection of Indonesian cultural knowledge into LLMs;
      improves SOTA on IndoCulture benchmark.
    validity_relevance: LOW-MEDIUM — cultural/social science knowledge, not administrative
      procedure; useful signal for RAG-augmented government chatbot designs
    source: arXiv 2601.12921 — https://arxiv.org/abs/2601.12921
  informal_register_benchmarks:
    gap_assessment: NO dedicated benchmark exists for evaluating LLM comprehension
      of Betawi-inflected or Sundanese-inflected colloquial Bahasa Indonesia in an
      administrative dialogue context. This is the most critical unresolved gap for
      the IF dimension of this deployment.
    relevant_research:
    - name: NusaDialect (synthetic benchmark, Surya et al. 2025)
      description: Synthetic dataset (NusaDialect benchmark) for Indonesian dialectal
        NLP covering Jakartan/Betawi colloquialisms, Javanese-influenced Indonesian,
        Sundanese-influenced Indonesian, and Eastern Indonesian varieties; code-mixing
        (Indonesian-English and Indonesian-Javanese); tasks include sentiment analysis
        and NER. Quantitative results show mBERT achieves only 62.1% F1 on informal/code-mixed
        text; GPT-4 shows stronger zero-shot resilience.
      limitation: Synthetic dataset; published in Attaqwa journal (2025), not ACL-tier
        peer review; NER and sentiment tasks, not administrative dialogue comprehension
      source: Attaqwa journal Vol.21 No.1 2025 — https://jurnal.insida.ac.id/index.php/attaqwa/article/download/978/461/3267
    - name: IndoRobusta (Adilazuarda et al., 2022)
      description: 'Framework to assess and enhance code-mixing resilience in Indonesian
        NLP across four embedded languages: English, Sundanese, Javanese, and Malay.
        Documents that multilingual models struggle with code-switching prevalent
        in Indonesian daily communication.'
      source: EACL 2022 Workshop — referenced in NusaBERT (arXiv 2403.01817)
    - name: One Country, 700+ Languages (Aji et al., 2022)
      description: ACL 2022 survey documenting NLP challenges for Indonesian's 700+
        local languages; notes that Betawi (bew) and Minangkabau (min) are among the
        few regional languages that benefit from cross-lingual transfer with standard
        Indonesian; Sundanese and Javanese transfer is limited.
      source: ACL 2022 — referenced in NusaBERT (arXiv 2403.01817)
    assessment_for_deployment: The comprehension-generation asymmetry requirement
      (must understand colloquial input, must produce formal output) has no direct
      benchmark analog in any existing Indonesian NLP suite, including SEA-HELM. The
      NusaDialect research confirms systematic weakness in current models on Betawi
      and Javanese-influenced input, directly relevant to the target population.
  government_procedure_nlp:
    gap_assessment: NO Indonesian-language government administrative procedure NLP
      benchmark was found covering Dukcapil, DJP/Coretax, OSS-RBA, or Imigrasi procedures.
      Existing chatbot research (Researchgate 2023; Dukcapil cloud chatbot studies)
      documents system implementations but no evaluation benchmark or labeled dataset
      for procedural correctness scoring.
    relevant_research:
    - description: Indonesian-language research documents Dukcapil chatbot implementations
        (e.g., IKD application support chatbots in Bojonegoro) but evaluates only
        user adoption and system architecture, not procedural correctness of LLM outputs
      source: ResearchGate Dukcapil chatbot study 2023 — https://www.researchgate.net/publication/373124017
    - description: IndoCareer (2024) covers professional certification exams including
        legal and finance domains but does not include public administration or government
        procedure content
      source: arXiv 2409.08564
    conclusion: 'Flagged gap confirmed: no existing benchmark covers pemda-level procedural
      variation, regulatory-compliance scoring, or citation-quality metrics for Indonesian
      government administrative procedures.'
  regulatory_compliance_scoring:
    gap_assessment: NO benchmark was found that implements regulation-version-aware
      scoring, timestamp-anchored procedural correctness, or citation-quality metrics
      in Indonesian. This scoring dimension — distinguishing plausible-but-outdated
      from currently-compliant answers — appears absent from all Indonesian NLP benchmarks
      and from SEA-HELM.
    conclusion: 'Flagged gap confirmed: the most critical failure mode for this deployment
      (outdated DJP/Adminduk procedural guidance generating ministerial liability)
      has no analog in any available benchmark.'
benchmark_validity_assessment:
  benchmark: SEA-HELM (2025)
  deployment_language: id (Bahasa Indonesia)
  sea_helm_indonesian_coverage_notes:
  - SEA-HELM covers Indonesian across all five pillars (NLP Classics, LLM-Specifics,
    SEA Linguistics/LINDSEA, SEA Culture, Safety)
  - KALAHI (SEA Culture pillar) covers only Filipino daily-life situations; there
    is NO equivalent Indonesian cultural dataset in SEA-HELM's current release
  - LINDSEA targets standard formal Indonesian syntactic/semantic/pragmatic phenomena;
    does not evaluate colloquial, code-mixed, or regionally-inflected input
  - SEA-HELM Safety pillar covers Indonesian, Thai, Vietnamese, Filipino (not Tamil)
  - 'SEA-HELM contains no Indonesian-language government administrative procedure
    content (confirmed: no Dukcapil/DJP/OSS-RBA domain)'
  - SEA-HELM has no regulatory-compliance output dimension; output taxonomy is culturally-relevant/irrelevant
    (KALAHI), win-rate (MTBench), and binary forced-choice (LINDSEA)
  dimension_priority_weights:
    IO:
      priority: HIGH
      rationale: SEA-HELM task taxonomy covers NLU/NLG/NLR and cultural prompts but
        contains no pillar for government administrative procedure types (error recovery,
        prerequisite checking, jurisdictional referral). KALAHI covers Filipino only.
        No equivalent Indonesian procedural taxonomy exists in any current benchmark.
    IC:
      priority: HIGH
      rationale: SEA-HELM content is general Indonesian; no DJP/Dukcapil/OSS-RBA domain
        content confirmed absent. Coretax migration (effective January 2025) means
        pre-2025 training data encodes superseded DJP e-Filing flows. Informal-to-formal
        comprehension asymmetry (Betawi, Sundanese-inflected) not addressed in benchmark
        construction. IndoCulture covers NTT and 11 provinces for cultural commonsense
        but not administrative procedures.
    IF:
      priority: MODERATE
      rationale: Both deployment and benchmark are text-only in Bahasa Indonesia with
        Latin script. SEA-HELM's LINDSEA and IFEval target standard formal Indonesian
        and may not reflect conversational, regionally inflected input. NusaDialect
        research (2025) confirms models systematically underperform on Betawi/Javanese-influenced
        colloquial input (mBERT 62.1% F1). No audio/speech modality required.
    OO:
      priority: HIGH
      rationale: SEA-HELM output taxonomy has no regulatory-compliance dimension.
        The deployment's central failure mode — plausible-but-outdated vs. currently-compliant
        — is absent from all available Indonesian benchmarks. This gap is unresolvable
        via SEA-HELM without custom evaluation overlay.
    OC:
      priority: HIGH
      rationale: SEA-HELM annotators are predominantly Singapore-based university
        students (per Q73). Deployment's authoritative judges include low-education,
        non-Jakarta citizens (accessibility KPI) and civil servants. Population mismatch
        is material for procedural correctness and plain-language accessibility labeling.
        IndoCulture used local in-province annotators across 11 provinces including
        NTT — this methodology is a positive precedent not replicated in SEA-HELM's
        Indonesian content.
    OF:
      priority: MODERATE
      rationale: Deployment requires open-ended conversational text with citation-and-deferral
        behavior for outdated guidance. SEA-HELM uses MCQ (LINDSEA), win-rate (MTBench),
        and instruction-following verifiers. These formats do not measure citation
        quality or deferral appropriateness.
  flagged_gaps:
    gap_1_pemda_procedure_content:
      status: CONFIRMED ABSENT
      description: SEA-HELM contains no Indonesian-language administrative procedure
        content for kelurahan, kabupaten, or provincial flows. No existing Indonesian
        NLP benchmark covers Dukcapil, DJP Online/Coretax, OSS-RBA, or Imigrasi procedures.
      recommendation: Bespoke evaluation dataset required; consider participatory
        elicitation with Dukcapil and DJP civil servants as annotators/evaluators
    gap_2_regulatory_compliance_scoring:
      status: CONFIRMED ABSENT
      description: No benchmark (SEA-HELM or otherwise) implements regulation-version-aware
        scoring or citation-quality metrics in Indonesian. Coretax launch (January
        2025) created an immediate version discontinuity in tax procedure knowledge.
      recommendation: Custom regulatory-compliance scoring dimension required; timestamped
        regulation version should be encoded as metadata in any evaluation item; consider
        reference to PMK-81/2024 as the current governing instrument for DJP procedures
    gap_3_indonesian_cultural_pillar:
      status: PARTIALLY MITIGATED EXTERNALLY
      description: SEA-HELM's SEA Culture pillar (KALAHI) covers Filipino only; no
        Indonesian equivalent in SEA-HELM. However, IndoCulture (Koto et al., 2024)
        fills this gap for cultural commonsense across 11 provinces including NTT.
        IndoCulture does not cover government procedure knowledge.
      recommendation: IndoCulture is a strong supplementary resource for assessing
        province-level cultural reasoning but does not substitute for a government-procedure
        cultural dataset; SEA-HELM roadmap states intention to expand Indonesian cultural
        coverage but no published release date found
    gap_4_annotator_population_mismatch:
      status: CONFIRMED CONCERN
      description: SEA-HELM annotators are predominantly university students recruited
        via public advertisement, based in Singapore (per Q72, Q73, Q71). Deployment's
        accessibility KPI requires labels validated by low-education, non-Jakarta
        citizens. Annotator demographics withheld for anonymity but available upon
        request (per Q20). IndoCulture's use of in-province local annotators across
        11 Indonesian provinces (including NTT) demonstrates a feasible alternative
        methodology.
      recommendation: Request SEA-HELM annotator demographics (per Q20) to confirm
        or refute Indonesia-specific annotator coverage; commission supplementary
        annotation using three-tier evaluator model (civil servants + legal experts
        + citizen panel) for accessibility labeling
    gap_5_informal_register_comprehension:
      status: CONFIRMED ABSENT (benchmark gap); PARTIALLY DOCUMENTED (research gap)
      description: SEA-HELM's LINDSEA and IFEval target standard formal Indonesian.
        NusaDialect (2025) documents Betawi, Javanese-influenced, Sundanese-influenced,
        and Eastern Indonesian varieties in a synthetic NER/sentiment dataset but
        no benchmark exists for colloquial-to-formal comprehension in administrative
        dialogue. Models show systematic weakness on non-standard Indonesian (mBERT
        62.1% F1 on informal/code-mixed input).
      recommendation: Targeted comprehension-side evaluation of regionally-inflected
        input → correct formal interpretation required; potentially addressable via
        IndoRobusta methodology or NusaDialect extension to administrative dialogue
        domain
    gap_6_outer_island_subpopulation:
      status: PARTIALLY MITIGATED EXTERNALLY
      description: SEA-HELM does not specify sub-national Indonesian regional representation.
        IndoCulture explicitly covers East Nusa Tenggara (NTT) as one of 11 provinces,
        developed by local NTT annotators. LoraxBench (2025) adds coverage of languages
        with no prior downstream NLP tasks. Neither covers government procedures.
      recommendation: IndoCulture's NTT coverage is a positive signal for cultural
        commonsense but does not address the procedural variation concern (NTT procedural
        flows vs. Jakarta flows); field-based elicitation with NTT civil servants
        recommended
    gap_7_coretax_regulatory_version:
      status: RESOLVED (factual context confirmed)
      description: DJP Coretax (CTAS/PSIAP/SIAP DJP) launched January 1, 2025, replacing
        DJP Online; governed by PMK No. 81/2024 (issued October 2024, consolidating
        42 prior tax regulations). Corporate functions fully on Coretax from January
        2025; individual SPT filing via Coretax mandatory for 2025 tax year (deadlines
        March–April 2026). Parallel operation of legacy systems ongoing for some functions.
        As of September 2025, only ~65% of registered taxpayers had activated Coretax
        accounts. Any LLM training corpus or benchmark dataset predating January 2025
        encodes the now-superseded DJP Online procedural flow.
      implication: SEA-HELM (published January 2025) was prepared concurrently with
        Coretax launch; its Indonesian content almost certainly reflects pre-Coretax
        DJP Online flows. Static benchmark cannot track ongoing regulatory changes.
        Deployment chatbot must route DJP questions to pajak.go.id official channel
        rather than provide static procedural answers.
      source: DJP official article — https://www.pajak.go.id/en/artikel/embracing-digital-future-coretax;
        ASEAN Briefing — https://www.aseanbriefing.com/doing-business-guide/indonesia/taxation-and-accounting/coretax-indonesia;
        cekindo.com PMK-81 summary — https://www.cekindo.com/blog/core-tax-administration-system
net_new_fields:
  indonesian_cultural_benchmarking_landscape:
    summary: 'A growing ecosystem of Indonesian cultural and linguistic benchmarks
      exists, none of which directly addresses government administrative procedure
      knowledge. Key resources: IndoCulture (province-level cultural commonsense,
      11 provinces including NTT); NusaX (10 local language sentiment/MT); NusaCrowd
      (137-dataset consolidation); LoraxBench (20 languages, formal/casual registers,
      2025); ID-MoCQA (multi-hop province reasoning, 2026); IndoSoSci (social science
      RAG corpus, 2026).'
    assessment_implication: The gap between available benchmarks and this deployment's
      needs is domain-specific (government procedures), not language-resource specific.
      Indonesian NLP infrastructure is moderately well-developed; the missing piece
      is procedure-domain and regulatory-compliance content.
  pdp_agency_status_2026:
    description: The dedicated PDP Agency (Lembaga PDP) mandated by UU 27/2022 has
      not yet been established as of April 2026. The Presidential Regulation establishing
      it is in the harmonization stage at the Ministry of Law (commenced October 2025).
      Agency targeted to become operational in 2026. Until established, MOCD (Ministry
      of Communication and Digital Affairs) serves as interim supervisory authority.
    deployment_implication: Enforcement risk is currently low but transitional uncertainty
      exists; any chatbot handling NIK, NPWP, or other personal data from citizens
      is subject to UU PDP 27/2022 from October 2024 onward.
    source: DLA Piper Data Protection Laws of the World — Indonesia (updated Feb 2026)
      — https://www.dlapiperdataprotection.com/?t=law&c=ID
  register_variation_in_nlp_benchmarks:
    finding: LoraxBench (2025) explicitly notes that existing Indonesian NLP datasets
      'frequently overlook this nuance [formal/informal register variation], typically
      focusing solely on the casual register' — confirming that the formal-output/informal-input
      asymmetry required by this deployment is systematically underserved in the benchmark
      ecosystem.
    source: arXiv 2508.12459 — https://arxiv.org/html/2508.12459
  coretax_citizen_adoption_barrier:
    finding: As of September 2025, approximately 65% of registered taxpayers had activated
      Coretax accounts; main barriers include incomplete/outdated data (unverified
      NIK, inactive email). This creates a high-frequency citizen error state directly
      relevant to the chatbot's error-recovery interaction type.
    source: DJP official article — https://www.pajak.go.id/en/artikel/embracing-digital-future-coretax
```

---

## Deployment Context

## Use Case
An Indonesian central government ministry's digital services division is evaluating LLMs to power a public-facing Bahasa Indonesia chatbot that answers citizen questions about administrative procedures — KTP applications, DJP Online tax filing, business registration, and permit renewals. The chatbot must handle step-by-step procedural instruction, document prerequisite checking, error recovery, and referral to the correct government office, and must operate across formal and informal registers of Bahasa Indonesia.

## Target Population
Indonesian citizens nationwide, with expected concentration in urban Java (Jakarta, Surabaya, Yogyakarta area); also must serve users in outer islands including East Nusa Tenggara and eastern Indonesia. Language: Bahasa Indonesia in formal and informal registers, including Javanese-influenced, Sundanese-influenced, and Betawi-inflected phrasing on the input side. Users range from low-education, non-urban citizens to urban professionals; the chatbot is a public service with explicit accessibility KPIs. Counterpart evaluators include Dukcapil and DJP civil servants, ministry legal/policy experts, and ordinary citizens who have navigated administrative procedures.

## Elicitation Responses

Q1 [IO]: Does the deployment require step-by-step procedural instruction, form-field disambiguation, error recovery, and referral to the correct government office, and which of these are most critical?
A1: All four are critical, with step-by-step procedural instruction and error recovery ranked highest — most citizen contacts occur after something went wrong (rejection, missing documents, unregistered NIK). Referral to the correct agency (Dukcapil vs. Imigrasi vs. DJP vs. OSS-RBA) is also essential due to frequent jurisdictional confusion. A fifth interaction type was added: pre-application document prerequisite checking (what to bring, format requirements, e-materai), which prevents most rejections.

Q2 [IC]: Does the chatbot need to handle regional procedural variation (kelurahan/kabupaten-level), or only standardized national-level guidance?
A2: Regional variation is unavoidable — permit requirements and KTP registration steps differ materially between DKI Jakarta (Jakipedia/JakEVO), Sleman, Makassar, and rural kabupaten. At minimum the system must not present Jakarta-specific steps as universally applicable. The user explicitly doubts SEA-HELM captures pemda-level procedural knowledge for Indonesian administrative contexts.

Q3 [OO]: Does the evaluation need to distinguish factually plausible but procedurally incorrect or outdated responses from fully regulation-compliant ones?
A3: Yes — this is the central evaluation requirement. A plausible but outdated answer (e.g., the pre-Coretax DJP e-Filing flow or pre-UU Adminduk KTP rules) is worse than a non-answer because it creates ministerial liability. For recently changed regulations, the correct behavior is to cite the regulation or SE number, timestamp the guidance, and route to the official channel rather than improvise. PP 71/2019 compliance on data handling is also a requirement.

Q4 [IC]: Should the chatbot handle informal and regionally flavored Bahasa Indonesia input, or only standard formal Indonesian?
A4: There is an explicit comprehension-vs-generation asymmetry requirement: the system must understand informal and regional-inflected input (e.g., Betawi slang, Sundanese-inflected phrasing, casual queries like "bang gimana caranya urus KTP ilang") on the comprehension side, but must produce consistent, polite, plain formal Bahasa Indonesia on the output side. The user is uncertain whether SEA-HELM evaluates this asymmetry.

Q5 [OC]: Who should be the authoritative judge of chatbot response quality, and are technically correct but inaccessible answers considered failures?
A5: A three-tier evaluator model is required: civil servants (Dukcapil, DJP) for procedural correctness, ministry legal staff for regulatory compliance, and ordinary citizens for practical usability. Responses that are technically accurate but written in impenetrable bureaucratic Indonesian are explicitly classified as failures; accessibility for low-education and non-Jakarta users is a stated KPI. The user identified a concrete gap: if SEA-HELM annotators were predominantly university-educated Jakarta residents, that population mismatch would undermine label validity for this deployment.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | SEA-HELM's task taxonomy covers NLU/NLG/NLR and cultural prompts but contains no pillar for government administrative procedure types (error recovery, prerequisite checking, jurisdictional referral) that are this deployment's primary use cases; the cultural pillar covers only Filipino (KALAHI), not Indonesian procedural contexts. |
| IC | HIGH | The deployment requires pemda-level regional procedural variation that SEA-HELM almost certainly does not capture; benchmark content is general Indonesian rather than DJP/Dukcapil/OSS-RBA domain content; the informal-to-formal comprehension asymmetry (Betawi, Sundanese-inflected input) is not evidenced in benchmark construction materials. |
| IF | MODERATE | Both deployment and benchmark are text-only in Bahasa Indonesia with Latin script, reducing signal mismatch; however, SEA-HELM's IFEval and LINDSEA were built for standard written Indonesian and may not reflect conversational, regionally inflected input forms citizens will actually use. |
| OO | HIGH | SEA-HELM's output taxonomy (culturally relevant/irrelevant for KALAHI; win-rate for MTBench; binary forced-choice for LINDSEA) does not include a regulatory-compliance dimension — the deployment requires distinguishing plausible-but-outdated from currently compliant answers, a scoring category absent from the benchmark. |
| OC | HIGH | SEA-HELM annotators are described as predominantly university students recruited via public advertisement in Singapore; the deployment's authoritative judges are a three-tier mix of civil servants, legal experts, and low-education non-Jakarta citizens — a substantial population mismatch for labeling procedural correctness and plain-language accessibility. |
| OF | MODERATE | Deployment output is open-ended conversational text in formal Bahasa Indonesia, while SEA-HELM uses a mix of MCQ (LINDSEA), win-rate (MTBench), and instruction-following verifiers — these formats do not directly measure the citation-and-deferral behavior required when guidance is outdated or legally sensitive. |

## Flagged Gaps

1. **Pemda-level procedural content absent from benchmark**: SEA-HELM contains no Indonesian-language administrative procedure content specific to kelurahan, kabupaten, or provincial flows. Downstream search should investigate whether any existing Indonesian-language benchmark covers Dukcapil, DJP Online (including post-Coretax migration), OSS-RBA, or Imigrasi procedures.

2. **No regulatory-compliance scoring dimension**: The deployment's most critical failure mode — a plausible but outdated or legally non-compliant answer — has no analog in SEA-HELM's output taxonomy. Search should identify whether any government-chatbot or legal-QA benchmark has implemented regulation-version-aware scoring or citation-quality metrics in Indonesian.

3. **Indonesian cultural pillar gap**: SEA-HELM's SEA Culture pillar (KALAHI) covers only Filipino daily-life situations; there is no equivalent Indonesian cultural dataset in the current benchmark release. Search should determine whether an Indonesian-language cultural evaluation component is planned or exists in the SEA-HELM roadmap or in parallel efforts (e.g., IndoNLU, IndoCulture).

4. **Annotator population mismatch for accessibility KPI**: SEA-HELM annotators are predominantly Singapore-based university students; the deployment requires labels validated by low-education, non-Jakarta citizens as a primary usability measure. Search should investigate annotator demographic details available on request (per Q20), and whether any Indonesian government digital-service evaluation has used citizen-panel annotation.

5. **Informal-register comprehension evaluation**: The deployment requires the model to correctly interpret Betawi slang, Sundanese-inflected Indonesian, and casual phrasing on the input side. SEA-HELM's LINDSEA and IFEval target standard formal Indonesian; search should examine whether Indonesian colloquial or dialect-inflected comprehension benchmarks exist (e.g., from ITB, UI, or BRIN NLP groups).

6. **Outer-island and eastern Indonesia subpopulation coverage**: The user notes that guidance must not be Jakarta-centric for users in East Nusa Tenggara and similar regions. SEA-HELM does not specify sub-national Indonesian regional representation in its content. Search should identify whether benchmark datapoints were sourced from or validated by communities outside Java.

7. **Post-Coretax and recent regulatory change coverage**: DJP's transition to Coretax and ongoing Adminduk amendments mean any static benchmark risks encoding outdated procedural knowledge. Search should investigate whether SEA-HELM or companion benchmarks have a versioning or timestamp mechanism for regulatory content, and what the benchmark's data cut-off date implies for Indonesian tax and ID procedure accuracy.

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
  "benchmark": "SEA-HELM",
  "region": "indonesia_bahasa_administrative_citizen",
  "dimensions": {
    "input_ontology": {
      "score": "<1-5>",
      "justification": "...",
      "checklist_responses": { "IO-1": "...", "IO-2": "..." },
      "evidence_quotes": ["[Q1] 'quote text' (p.7)", ...],
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
  "remediation_suggestions": "...",
  "highest_concern_dimensions": ["..."],
  "strongest_dimensions": ["..."]
}
```
