# Validity Extraction: SEA-HELM: A Holistic Linguistic and Cultural LLM Evaluation Suite for Southeast Asian Languages
<!-- Model routing: Haiku (per-page extraction) → Sonnet (consolidation) -->

## Metadata
- **Title**: SEA-HELM: A Holistic Linguistic and Cultural LLM Evaluation Suite for Southeast Asian Languages
- **Authors**: Yosephine Susanto, Adithya Venkatadri Hulagadri, Jann Railey Montalan, Jian Gang Ngui, Xian Bin Yong, Weiqi Leong, Hamsawardhini Rengarajan, Peerat Limkonchotiwat, Yifan Mai, William Chandra Tjhi
- **Venue/Year**: Not explicitly stated in extracted content (arXiv / 2025 inferred from citations)
- **Total Pages**: 29
- **Quotes Extracted**: 89

---

## Narrative Context

### 1. Task Taxonomy / Test Case Categories

SEA-HELM is organized around five core pillars: NLP Classics, LLM-Specifics, SEA Linguistics, SEA Culture, and Safety [Q1, Q3, Q47, Q48]. The NLP Classics pillar further subdivides into three competencies: NLU (QA and sentiment analysis), NLG (translation and summarization), and NLR (causal reasoning and NLI) [Q5]. The LLM-Specifics pillar addresses instruction-following and multi-turn chat, with SEA-IFEval covering a granular taxonomy of constraint types including format constraints, keyword constraints, length constraints, and language constraints [Q55–Q76]. The SEA Linguistics pillar, called LINDSEA, targets syntactic, semantic, and pragmatic phenomena [Q23], while the SEA Culture pillar includes datasets like KALAHI for Filipino cultural scenarios [Q31]. The benchmark evaluates models on multi-turn chat categories including creative writing, mathematics, STEM, and humanities [Q18].

### 2. Data Sources and Collection

SEA-HELM currently supports Filipino, Indonesian, Tamil, Thai, and Vietnamese [Q2, Q4, Q49], drawing on a region home to nearly 700 million speakers across more than 1,000 languages [Q6]. Key datasets include SEA-IFEval (manually translated and localized from the English IF-Eval benchmark) [Q29], SEA-MTBench (translated and localized from MT-Bench) [Q35], and the KALAHI dataset of 150 Filipino-language prompts [Q31]. Newly created datasets including SEA-IFEval, SEA-MTBench, and LINDSEA are released under CC-BY-SA 4.0 [Q12]. SEA-IFEval constraint categories are sourced from Zhou et al. (2023) [Q77], and the supported SEA languages for evaluated models are derived from respective model cards or reports [Q84].

### 3. Data Format and Preprocessing

The benchmark strongly prefers data originally written in native languages; English datasets are carefully translated by native speakers only when native-language originals are unavailable [Q7]. Each prompt is given in the target language rather than English (except for English tasks), manually translated by native speakers [Q40]. SEA-IFEval construction involved filtering out instructions inapplicable to SEA scripts (e.g., capitalization-related prompts for Thai or Tamil) and converting letter-count instructions to number-count instructions for non-Latin scripts [Q10, Q11]. The LINDSAY design principle emphasizes handcrafted examples rather than automatic generation [Q24]. KALAHI prompts each contain a query, information about the person posing the question, and personal context [Q87]. Indonesian prompt templates instruct the model to output answers in a strict format using specified options [Q81, Q83].

### 4. Label Categories and Output Types

KALAHI responses are classified as either culturally-relevant (helpful and harmless within the given culture) or culturally-irrelevant (unhelpful and harmful within a culture) [Q86]. For multiple-choice tasks, answer options are extracted via regular expressions and compared against gold labels [Q37]. For open-ended questions, a score range of 0–1 is used [Q44]. Syntactic minimal pair tasks use binary forced-choice labels (A or B) [Q82], while pragmatic reasoning tasks use true/false labels [Q83].

### 5. Annotation Process

SEA-HELM places strong emphasis on community participation, involving native speakers at each stage of dataset planning and construction [Q13]. Annotator demographics are withheld for anonymity but available upon request [Q9]. LINDSEA examples are handcrafted by linguists in collaboration with native speakers and iteratively reviewed [Q24]. SEA-IFEval involved manual translation verified for linguistic faithfulness, cultural authenticity, and relevance [Q30]. The QA team consisted of paid native speakers recruited through public advertisements, composed predominantly of university students and adult members of the public [Q60, Q61]. Participation was voluntary, PII was removed, and participants could withdraw at any time [Q62, Q64, Q65, Q66]. The project received IRB approval and compensation complied with university and legal guidelines [Q59].

### 6. Evaluation Metrics and Output Modality

SEA-HELM uses a normalized scoring scheme that subtracts a random baseline from raw scores and rescales to 0–100, with negative scores clamped to 0 [Q43]. For multiple-choice tasks, the baseline is 100/n%; for open-ended tasks it is 0% [Q44]. Scores are first aggregated at the competency level (averaging tasks within a competency), then at the language level (averaging competencies), and finally as a SEA average across all languages [Q45, Q46]. Instruction-following accuracy is computed with the same verifiers as English IF-Eval, then multiplied by the rate of correct-language responses [Q34]. SEA-MTBench uses an LLM-as-a-Judge paradigm comparing each candidate model's win rate against gpt-3.5-turbo-0125 using gpt-4-1106-preview as judge [Q15, Q16, Q17]. Instruction-tuned models are evaluated zero-shot; pre-trained models use 5-shot examples [Q42]. For null responses (models that fail to append the required answer tag), the model is scored as having given no response [Q39].

### 7. Stated Limitations

The authors identify several limitations. Traditional NLP evaluation metrics tied to ground truth are insufficient for measuring LLM capabilities [Q16-original/Q16]; SEA languages suffer from a lack of both training and testing data [Q17-original]. Translated datasets risk translationese effects [Q8]. Most SEA languages remain unsupported by major LLMs [Q18-original]. The safety evaluations are necessary but not sufficient for real-world safety assurance [Q68, Q69]. SEA-HELM is not yet exhaustive in language or task coverage [Q50, Q51, Q52], and leaderboard results are based on single runs without error bars [Q53, Q54]. There remain significant performance gaps between English and SEA languages [Q49-body]. Cultural datasets like aggregated value surveys cannot fully capture the complex nature of culture [Q27]. Prior cultural evaluation work often fails to consult speaker communities [Q26]. Multilingual inputs in lower-resource languages can increase unsafe LLM outputs [Q33].

### 8. Authors and Affiliations

The paper lists ten authors affiliated with AI Singapore, the National University of Singapore, and the Center for Research on Foundation Models (CRFM) at Stanford University [Q14]. The research is funded by the National Research Foundation, Singapore, under its National Large Language Models Funding Initiative [Q67]. The evaluation code is made publicly available [Q15-affil].

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | task_taxonomy | "SEA-HELM, a holistic linguistic and cultural LLM evaluation suite that emphasises SEA languages, comprising five core pillars: (1) NLP CLASSICS, (2) LLM-SPECIFICS, (3) SEA LINGUISTICS, (4) SEA CULTURE, (5) SAFETY." |
| Q2 | 1 | data_sources | "SEA-HELM currently supports Filipino, Indonesian, Tamil, Thai, and Vietnamese." |
| Q3 | 1 | evaluation_metrics | "We also introduce the SEA-HELM leaderboard, which allows users to understand models' multilingual and multicultural performance in a systematic and user-friendly manner." |
| Q4 | 1 | stated_limitations | "Traditional approaches to NLP evaluation, which emphasise on alignment with a predefined ground truth reference, are not sufficient in measuring the complex abilities of LLMs." |
| Q5 | 1 | stated_limitations | "This gap is further exacerbated in lower-resource languages in South East Asia (SEA), owing to a lack of both training and testing data on the internet." |
| Q6 | 1 | data_sources | "The SEA region is home to nearly 700 million speakers across more than 1,000 languages." |
| Q7 | 1 | stated_limitations | "While this region represents almost 10% of the global population and constitutes approximately one-seventh of the world's total languages, most of these languages remain unsupported by major LLMs, such as Mistral (Mistral AI, 2023) and Claude (Anthropic, 2023)." |
| Q8 | 1 | authors_affiliations | "Yosephine Susanto, Adithya Venkatadri Hulagadri, Jann Railey Montalan, Jian Gang Ngui, Xian Bin Yong, Weiqi Leong, Hamsawardhini Rengarajan, Peerat Limkonchotiwat, Yifan Mai, William Chandra Tjhi from AI Singapore, National University of Singapore, and Center for Research on Foundation Models (CRFM), Stanford University." |
| Q9 | 1 | authors_affiliations | "We make the SEA-HELM evaluation code publicly available." |
| Q10 | 2 | task_taxonomy | "Over the years, AI practitioners have employed either an individual task-based or, more rarely, a holistic approach to assess the performance and capabilities of LLMs." |
| Q11 | 2 | task_taxonomy | "Popular tasks for evaluating LLMs include translation (Hendy et al., 2023), summarisation (Zhang et al., 2023), decision-making (Shen et al., 2023), detecting scalar implicatures (Jeretic et al., 2020; Pandia et al., 2021; Hu et al., 2023; Liu et al., 2023)" |
| Q12 | 2 | data_sources | "We release SEA-IFEval, SEA-MTBench and LINDSEA datasets under the Creative Commons Attribution Share-Alike 4.0 (CC-BY-SA 4.0) license." |
| Q13 | 2 | annotation_process | "We deliberately incorporate community participation by involving native speakers of the SEA languages at each stage of the dataset planning and construction to ensure linguistic accuracy and cultural authenticity." |
| Q14 | 2 | evaluation_metrics | "The five pillars are also meticulously and rigorously crafted to achieve fair, transparent, and authentic multilingual and multicultural evaluations of LLMs in the region." |
| Q15 | 3 | task_taxonomy | "This evaluation suite consists of five core pillars: (1) NLP CLASSICS, (2) LLM-SPECIFICS, (3) SEA LINGUISTICS, (4) SEA CULTURE, and (5) SAFETY, and has been recently integrated with HELM." |
| Q16 | 3 | data_sources | "SEA-HELM currently supports five SEA languages – Filipino, Indonesian, Tamil, Thai, and Vietnamese, enabling users and AI practitioners to assess the overall performance of LLMs for these languages." |
| Q17 | 3 | task_taxonomy | "First, for the Natural Language Understanding (NLU) competency, we include QA (extractive question answering) and sentiment analysis tasks. Second, for the Natural Language Generation (NLG) competency, we include translation (English to native language and native language to English) and abstractive summarisation tasks. Third, for the Natural Language Reasoning (NLR) competency, we include causal reasoning and natural language inference (NLI) tasks." |
| Q18 | 3 | data_format | "We selected datasets that comprised of data originally written in the native language as far as possible. Otherwise, existing datasets in English were carefully translated by native speakers." |
| Q19 | 3 | stated_limitations | "This is important because translated datasets often contain elements of translationese (Gellerstam, 1986), which can differ significantly from natively written text (Baker, 1993; Lembersky et al., 2012; Volansky et al., 2015; Riley et al., 2020)." |
| Q20 | 3 | annotation_process | "Annotator demographics are not included in this paper for anonymity, demographics can be provided upon request." |
| Q21 | 3 | evaluation_metrics | "With LLMs enabling unprecedented NLP applications, there is a need to develop automated, dedicated evaluation metrics for these higher-order tasks. SEA-HELM focuses on two specific capabilities - the ability to follow human" |
| Q22 | 4 | data_sources | "SEA-IFEval is an instruction-following benchmark we created collaboratively with native speakers. It was manually translated from the English IF-Eval benchmark (Zhou et al., 2023) and, crucially, localised to fit the linguistic and cultural nuances of SEA languages." |
| Q23 | 4 | annotation_process | "Manual translations ensured faithful and accurate linguistic representation, while localisation ensured cultural authenticity and removed any unintended or inherent biases. Additionally, this involved manually verifying that each sample was relevant and applicable to the languages concerned." |
| Q24 | 4 | data_format | "Specifically, to create the SEA-IFEval dataset, we first filtered out instructions that could not reasonably apply to most SEA languages. For example, prompts asking to change the capitalisation or punctuation do not make sense in many scripts in the region, such as Burmese, Tamil, or Thai." |
| Q25 | 4 | data_format | "We also changed instructions that required inclusion of a stated quantity of instances of letters to instead require a stated quantity of instances of numbers as it was not easy to localise them for non-Latin scripts. An example of this change is to convert the instruction of \"[respond] with the letter 'l' appearing at least 6 times\" to \"[respond] with the number '4' appearing at least 6 times." |
| Q26 | 4 | stated_limitations | "Thus, by filtering out and adapting instructions given the SEA context, we ensure a fair basis of comparison for the instruction-following competency." |
| Q27 | 4 | evaluation_metrics | "The accuracy with which LLMs follow the exact instruction following requirements is calculated using the same verifiers as those found in the English IF-Eval benchmark (Zhou et al., 2023). The model's accuracy is then adjusted to penalise instructions that responded in the wrong language by multiplying its accuracy with the rate at which it responds in the correct target language." |
| Q28 | 4 | data_sources | "SEA-MTBench is a manually translated and localised version of the popular MT-Bench dataset (Zheng et al., 2023), which also introduced the paradigm of LLM-as-a-Judge to approximate human preferences." |
| Q29 | 5 | evaluation_metrics | "grading approach, where we compare the win-rate of each candidate model against a fixed reference model, namely gpt-3.5-turbo-0125. The models' responses were compared with the reference response using gpt-4-1106-preview as the judge model. This setup sees the number of judge calls scale linearly with the number of models being compared, whereas pairwise comparisons would scale quadratically." |
| Q30 | 5 | task_taxonomy | "Models receive an initial prompt based on a category such as creative writing, mathematics, STEM or humanities. They are then given a follow-up instruction which related to the initial prompt, and are expected to respond appropriately." |
| Q31 | 5 | evaluation_metrics | "Finally, a model's responses to both the initial and follow-up prompts are evaluated as a whole given accuracy, relevance, and coherence as judging criteria. Results are reported based on each model's average win rate against the reference model." |
| Q32 | 5 | task_taxonomy | "As one of the five core evaluation pillars, LINDSEA (LINguistic Diagnostics for SouthEast Asian languages) is a high quality, manually-crafted linguistic dataset that systematically diagnoses models' language proficiency and grammatical understanding based on a granular taxonomy of syntactic, semantic and pragmatic phenomena. It is also the first to be created for SEA languages." |
| Q33 | 5 | data_format | "The design of LINDSEA is based on three principles: breadth, depth, and quality." |
| Q34 | 5 | annotation_process | "That is, rather than using a small set of lexical items and grammatical rules to automatically generate large numbers of test sentences, the examples in LINDSEA are handcrafted from scratch by linguists in collaboration with native speakers and reviewed iteratively to ensure that they sound natural, are semantically coherent and target the relevant phenomena effectively (quality)." |
| Q35 | 5 | stated_limitations | "While there are existing syntactic and semantic diagnostic datasets for English (Warstadt et al., 2020; Jeretic et al., 2020; Liu et al., 2023), Mandarin (Xiang et al., 2021) and even Japanese (Someya and Oseki, 2023), none yet exist for SEA languages, and, to our knowledge, there has yet to be such an extensive coverage of linguistic phenomena in any dataset." |
| Q36 | 5 | task_taxonomy | "Cultural representation and bias have also become increasingly important with LLM use (Adilazuarda et al., 2024) since a lack thereof can potentially cause social harm (Solaiman et al., 2023)." |
| Q37 | 5 | stated_limitations | "Much prior work on analysing or evaluating cultural representation in LLMs is created in ways that do not start from consulting the communities of speakers of the language but instead starts from reference sources that aggregate cultural knowledge, opinions, and values at a population level." |
| Q38 | 6 | stated_limitations | "Such datasets are inherently limited and cannot comprehensively represent the complex nature of culture (Causadias, 2020), even if they can capture aggregated value alignment." |
| Q39 | 6 | annotation_process | "Thus, we place emphasis on a strong participatory approach that includes the native speaker communities in order to authentically represent the target culture." |
| Q40 | 6 | task_taxonomy | "The KALAHI dataset is designed to determine if LLMs can provide culturally-relevant responses to culturally-specific situations that Filipino people can reasonably encounter in their daily lives, and the dataset is composed of 150 high-quality Filipino-language prompts created in collaboration with native Filipino speakers." |
| Q41 | 6 | stated_limitations | "Multilingual inputs, especially when given in lower-resource languages such as those in the SEA region, can increase the likelihood that LLMs produce unsafe responses (Song et al., 2024; Shen et al., 2024)." |
| Q42 | 6 | data_sources | "Currently, we cover Indonesian, Thai, Vietnamese, and Filipino for this task." |
| Q43 | 6 | evaluation_metrics | "For each task, we opted to be explicit in instructing the LLM to output the answer following a specified format." |
| Q44 | 6 | evaluation_metrics | "The answer can then be extracted using regular expressions and compared against the corresponding gold label." |
| Q45 | 7 | evaluation_metrics | "tag to its answer, the model is deemed to have given a null response. This approach allows for more efficient automatic evaluation at scale, even for models that may tend to have lengthy outputs." |
| Q46 | 7 | data_format | "It should also be noted that each prompt is given in the target language rather than in English (except for the English tasks) and is manually translated by native speakers of each language." |
| Q47 | 7 | task_taxonomy | "In our view, for full SEA languages support, an LLM should be able to output coherent responses and should also be able to correctly interpret native instructions." |
| Q48 | 7 | evaluation_metrics | "Instruction-tuned models were evaluated in a zero-shot manner while pre-trained models are evaluated with 5-shot examples." |
| Q49 | 7 | evaluation_metrics | "As per equation 1, the normalised metric score (snorm) is calculated by subtracting the random baseline score (sbaseline) from the raw metric score (sraw). This is then divided by the difference between the maximum score (smax) and the random baseline score. The range of the normalised score is then scaled to a range of 0–100 (Hulagadri et al., 2025). For negative normalised score, we set the score to 0." |
| Q50 | 7 | evaluation_metrics | "For multiple-choice task with n options, the baseline score using a random strategy is (100/n)%. For open ended questions with a score range between 0–1, we set the guessing score to 0% and the best possible score to 100%." |
| Q51 | 7 | evaluation_metrics | "First, metrics are aggregated at the competency level. The normalised scores of each tasks belonging to each competency are averaged to calculate the competency score (The list of tasks in each competency can be found in Table 1). This is done since some competencies have more tasks than others, and if the final language average score was taken from all available tasks, some competencies would be over-represented." |
| Q52 | 7 | evaluation_metrics | "Next, the language score is calculated by taking the average of the competency scores for each language. This provides an indication of how well the models are performing at a per-language basis Finally, a SEA average score is calculated as the mean of all the language score in SEA-HELM." |
| Q53 | 8 | evaluation_metrics | "Of all the open-sourced models tested, DeepSeek-R1 was the strongest performing model and showed comparable results to gpt-4o-2024-08-06 on the SEA-HELM suite (Figure 2a, Table 2)." |
| Q54 | 8 | stated_limitations | "Given the large size of DeepSeek-R1 (671B), finding comparisons to other models that support SEA languages was not trivial." |
| Q55 | 8 | evaluation_metrics | "Thus, we chose to focus our discussion on LLMs of sizes ranging between 7-9B parameters (See Table 2 for the full list of models) and used both the DeepSeek-R1 and gpt-4o-2024-08-06 as the reference models for what was the best available open-sourced and closed-sourced model respectively." |
| Q56 | 8 | evaluation_metrics | "We also observe that the gap between the smaller models and the reference models is closing, as evidenced by the smaller gap between gpt-4o-2024-08-06 with the newer LLaMA model Llama-3.1-8B-Instruct as compared to the earlier LLaMA model Meta-Llama-3-8B-Instruct (Figure 2a, 2b, Table 2)." |
| Q57 | 8 | evaluation_metrics | "Notably, continued pre-training and further tuning for the SEA languages resulted in this gap closing even further (Figure 2b; llama3.1-8b-cpt-sea-lionv3-instruct compared against Llama-3.1-8B-Instruct)." |
| Q58 | 8 | stated_limitations | "This suggests that there is still room for improvement and spending the effort to train LLMs to target the specific SEA languages can result in models that are more suited for the SEA region and thus work better for the region's use cases." |
| Q59 | 9 | task_taxonomy | "In conclusion, we introduce SEA-HELM, a holistic evaluation suite that caters to the SEA languages and cultures." |
| Q60 | 9 | task_taxonomy | "To achieve a comprehensive evaluation suite, SEA-HELM was designed around the following five core pillars: (1) NLP CLASSICS, (2) LLM-SPECIFICS, (3) SEA LINGUISTICS, (4) SEA CULTURE, (5) SAFETY." |
| Q61 | 9 | stated_limitations | "Our results show that there are still significant gaps between high-resource languages such as English and the mid- to low-resource languages in Southeast Asia, including several with official status and millions of speakers." |
| Q62 | 9 | stated_limitations | "While aiming to achieve holistic and authentic evaluations for LLMs in Southeast Asia, SEA-HELM is not yet exhaustive in its coverage of languages and tasks." |
| Q63 | 9 | stated_limitations | "As we iteratively improve the coverage of the various SEA-HELM pillars, more language and cultural coverage will added and refined in the future." |
| Q64 | 9 | stated_limitations | "Our leaderboard results are based on single model runs." |
| Q65 | 9 | stated_limitations | "However, as we have assumed deterministic model behaviour and set every model's temperature to 0, we did not publish error bars for the results, in line with most other benchmarks in the field." |
| Q66 | 9 | data_sources | "We recognise that although SEA-HELM currently covers Filipino, Indonesian, Tamil, Thai, and Vietnamese, we still have much more work to do and therefore we are committed to iteratively expanding each pillar." |
| Q67 | 9 | task_taxonomy | "Specifically, we plan to expand SEA-HELM to include a broader range of languages, cultures, tasks and models to encourage stronger SEA representation in models." |
| Q68 | 10 | stated_limitations | "acknowledge that passing our evaluations with a high score is not necessarily a guarantee of the safety of an LLM in the SEA context, as it is not possible to enumerate every type of unsafe response in real-world scenarios." |
| Q69 | 10 | stated_limitations | "Thus, passing the safety evaluations in SEA-HELM must be seen as a necessary but not sufficient requirement for ensuring safety in real-world LLM applications." |
| Q70 | 10 | annotation_process | "SEA-HELM is grateful to our Quality Assurance (QA) team, consisting of paid native speakers of SEA languages who worked as translators and annotators, enabling us to construct localised datasets needed for this research." |
| Q71 | 10 | annotation_process | "The SEA-HELM project has received full and official approval from our university's internal review board after undergoing a rigorous review process, and the compensation and working hours for all members involved were established in full compliance with the prevailing university guidelines and applicable regulations in the country where this research is conducted." |
| Q72 | 10 | annotation_process | "Our QA team was recruited through public advertisements that clearly outlined the estimated workload and hourly pay, consistent with all relevant legal and regulatory requirements." |
| Q73 | 10 | annotation_process | "The team is composed predominantly of students at local universities and members of the public, all of whom are adults who satisfy the legal age requirements for employment, as defined by the labour laws of the country." |
| Q74 | 10 | annotation_process | "Although participants are compensated for their participation, their involvement in the study is entirely voluntary." |
| Q75 | 10 | annotation_process | "Any personally identifiable information (PII) is removed from the data collected and will not be tied to their identity." |
| Q76 | 10 | annotation_process | "We did not estimate that their work involved significant risks of exposure to offensive material, as they were not involved in the construction of sensitive data such as those under the SAFETY pillar." |
| Q77 | 10 | annotation_process | "Nonetheless, they were encouraged to report inappropriate samples and were given the option to withdraw their participation at any time, including after its completion, without any negative consequences or loss of benefits." |
| Q78 | 10 | annotation_process | "If they chose to withdraw, they could do so without providing any reason, and all data collected from the withdrawn individual were excluded from this research." |
| Q79 | 10 | stated_limitations | "We do not foresee negative social impacts from our research, for our research introduces evaluation datasets in SEA languages by working with native speakers, paying due respect to local cultural sensitivities." |
| Q80 | 10 | stated_limitations | "We thus do not believe that our research will contribute to over-generalisations regarding SEA cultures." |
| Q81 | 10 | authors_affiliations | "This research/project is supported by the National Research Foundation, Singapore under its National Large Language Models Funding Initiative." |
| Q82 | 19 | data_sources | "Supported SEA Languages comprises of tested languages that are reported on the respective model cards or reports." |
| Q83 | 23 | data_sources | "SEA-IFeval Categories with descriptions, each with 5 samples. Sourced from Zhou et al. (2023)" |
| Q84 | 23 | data_format | "An example of a Vietnamese instruction following prompt from SEA-IFEval. The target constraint in this particular instruction is that the response must repeat the phrase before proceeding to give the summary." |
| Q85 | 25 | data_format | "Anda adalah seorang ahli bahasa Indonesia. Jawablah hanya dengan menggunakan format berikut ini: Jawaban: $OPTION Ganti $OPTION dengan pilihan yang telah dipilih. Gunakan huruf A atau B saja sebagai jawabannya." |
| Q86 | 25 | data_format | "Anda adalah seorang ahli bahasa Indonesia Jawablah hanya dengan menggunakan format berikut ini: Jawaban: $OPTION Ganti $OPTION dengan benar atau salah." |
| Q87 | 26 | label_categories | "Each sample is composed of a prompt and a list of responses that are culturally-relevant (helpful and harmless within the context of the given culture) and culturally-irrelevant (unhelpful and harmful within a culture)." |
| Q88 | 26 | data_format | "Each prompt is contains a query representing a unique situation that a Filipino may encounter, information regarding the person posing that question, and the person's personal context." |

---

### Category Index
- **task_taxonomy**: Q1, Q10, Q11, Q15, Q17, Q30, Q32, Q36, Q40, Q47, Q59, Q60, Q67
- **data_sources**: Q2, Q6, Q12, Q16, Q22, Q28, Q42, Q66, Q82, Q83
- **data_format**: Q18, Q24, Q25, Q33, Q46, Q84, Q85, Q86, Q88
- **label_categories**: Q87
- **annotation_process**: Q13, Q20, Q23, Q34, Q39, Q70, Q71, Q72, Q73, Q74, Q75, Q76, Q77, Q78
- **evaluation_metrics**: Q3, Q14, Q21, Q27, Q29, Q31, Q43, Q44, Q45, Q48, Q49, Q50, Q51, Q52, Q53, Q55, Q56, Q57
- **stated_limitations**: Q4, Q5, Q7, Q19, Q26, Q35, Q37, Q38, Q41, Q54, Q58, Q61, Q62, Q63, Q64, Q65, Q68, Q69, Q79, Q80
- **authors_affiliations**: Q8, Q9, Q81