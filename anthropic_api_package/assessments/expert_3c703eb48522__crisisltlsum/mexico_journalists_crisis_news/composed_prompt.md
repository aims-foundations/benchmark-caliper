I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **CrisisLTLSum: A Benchmark for Local Crisis Event Timeline Extraction and Summarization** is valid for use in **Mexico City and Central America Bilingual Crisis Journalism**.

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

- **Name**: crisisltlsum
- **Full Name**: CrisisLTLSum: A Benchmark for Local Crisis Event Timeline Extraction and Summarization
- **Domain**: Crisis event timeline extraction and abstractive summarization from Twitter
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2023

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
CrisisLTLSum is explicitly restricted to four crisis domains: wildfire, local fire, traffic
incidents, and storms [Q1, Q53, Q122]. The domain taxonomy was derived from the crisis types
most frequent in the selected US and Australian geographic footprint [Q124]. The benchmark
frames two task types — timeline extraction and timeline summarization — as the primary
evaluation categories [Q4], with the extraction task further organized around an online
clustering paradigm that mimics real-time stream processing [Q38, Q40]. The "local" event
scope is a deliberate ontological choice: events must be geographically bounded to a building,
street, or county and short-lived [Q12].

No crisis categories outside the four domains are represented. The paper acknowledges that
existing crisis-NLP datasets were limited to large-scale events [Q22], and CrisisLTLSum's
contribution is breadth within its four domains rather than taxonomic expansion. Earthquakes,
volcanic activity, tropical-system flooding, and civil unrest — all structurally important
event types for Latin American coverage — are entirely absent from the benchmark's ontology.
Even shared category labels (e.g., "storm") carry US-specific damage profiles and contextual
conventions not documented as transferable to other regional settings.

### Input Content
All tweet content was collected from a highly specific geographic and temporal scope: seven
US states (New York, Illinois, Massachusetts, California, Texas, Florida) and two Australian
states (New South Wales, Victoria) during 2020–2021 [Q123, Q124]. These states were selected
because they experience high frequencies of the four target crisis domains [Q124]. Location
filtering relied on lists of US and Australian city, town, and neighborhood names [Q30], and
domain filtering used English-language keyword lists curated through expert review of
English-language crisis news and social media [Q126, Q127]. The 1,000 cluster timelines were
manually selected by the paper's authors from US and Australian Twitter activity [Q52].

No data were collected from Mexico, Central America, or any Spanish-language region. The
NER pipeline used to extract location mentions relied on a BERT-based model tuned on English
Twitter data [Q35] and an OpenStreetMap location augmentation step [Q36, Q37] — both anchored
to Anglo-geography. The authors explicitly note that replicating this pipeline for other
languages or geographic regions would be difficult due to these dependencies [Q119]. The
keyword filtering approach is also described as not comprehensive or exhaustive, with
domain-coverage quality critically dependent on the English keyword lists [Q128, Q132].

### Input Form
The benchmark operates on text-only tweets filtered from the public Twitter stream [Q2, Q18].
Preprocessing includes lemmatization, lowercasing, and fuzzy string matching for duplicate
removal [Q129, Q136], all implemented for English-language text. The location augmentation
pipeline maps English location mentions to physical addresses via OpenStreetMap [Q36].
Input sequences for the BERT-based extraction model are formatted with SEP tokens up to a
512-token ceiling [Q86, Q92]. The modality (text-only social-media posts) is consistent
with the target deployment context, but the linguistic form is exclusively English; no
Spanish-language text processing infrastructure is documented.

### Output Ontology
For timeline extraction, the label schema is binary: a tweet is either part of the timeline
or not, governed by three simultaneous conditions — relevant (same event as seed), informative
(factual rather than purely opinion), and non-repetitive (new information) [Q58]. For timeline
summarization, the human evaluation rubric introduces four quality axes rated 1–5: Coherence,
Accuracy, Coverage, and Overall Quality [Q106, Q151]. Coherence is defined in terms of
readability and freedom from English errors [Q153, Q154]; Accuracy assesses factual fidelity
to the timeline [Q155, Q156]; Coverage measures completeness of important event information
[Q157, Q158]; Overall Quality provides a holistic judgment [Q159, Q160].

The three-way relevance/informativeness/non-redundancy criteria [Q58] were developed and
validated against US English tweets covering US crisis events. Whether the same decision
boundaries would produce equivalent judgments for Spanish-language tweets about Mexican
or Central American events is not addressed. The coherence rubric is explicitly anchored
to English-language writing norms [Q153], with no analog scoring dimension for
Spanish-language output quality, register, or editorial style.

### Output Content
Ground-truth timeline extraction labels were determined by majority vote among three MTurk
workers [Q70], achieving 90.06% average timeline-level inter-annotator agreement [Q77] and
91.77% agreement against expert annotations [Q78, Q79]. Reference summaries were written by
the two workers who agreed most on extraction labels [Q87, Q88]. Human evaluation of summary
quality used five MTurk workers per summary [Q106], recruited through the same location
restriction (QC1) that confined annotators to countries where native English speakers are
most likely to be found [Q61, Q105].

All annotators were therefore native English speakers operating within Anglophone news-reading
conventions. No Spanish-speaking annotators, no journalists, and no individuals with Latin
American geographic or cultural knowledge contributed to ground-truth labels or reference
summaries. The relevance and informativeness judgments embedded in the extraction labels,
and the completeness and accuracy judgments embedded in the reference summaries, reflect a
US-centric perspective on what constitutes a meaningful crisis update — a perspective not
validated for the target deployment's Mexican journalistic audience.

### Output Form
Timeline extraction is evaluated using average timeline-level accuracy against expert
annotations [Q91, Q94], with the best model achieving 73.51% versus 88.98% human-level
performance [Q96]. Timeline summarization is evaluated using multi-reference ROUGE scores
(SacreROUGE) comparing model output against the two summaries written by the most-agreeing
annotator pair [Q98, Q99, Q100]. Human evaluation supplements ROUGE with the four-axis
rubric applied to eight summaries per timeline rated by five MTurk workers each [Q103, Q104,
Q106]. Human-written summaries average 4.12 overall quality rating [Q108].

The benchmark provides no evaluation framework for Spanish-language summarization. All ROUGE
references are English-language summaries [Q99]; the human evaluation rubric is written in
English and scores coherence against English-language writing norms [Q153]; and no bilingual
evaluation protocol, register-appropriateness metric, or AP Español–aligned scoring rubric
is documented. The benchmark thus provides no signal for predicting system performance on
Spanish-language summarization — a direct mismatch with the target deployment requirement
for bilingual output.

### Stated Limitations
The authors acknowledge that the noisy timeline collection process is not exhaustive and
aims for representativeness rather than comprehensiveness [Q117]; that the pipeline is highly
dependent on entity extraction quality and OpenStreetMap accuracy [Q118]; and that replication
for other languages or geographic regions would be difficult due to these dependencies [Q119].
Keyword-based domain filtering is acknowledged as not comprehensive or exhaustive [Q132].
The benchmark's stated use case emphasizes aiding first responders [Q112] rather than
journalistic summarization workflows, and no limitations are explicitly stated regarding
multilingual capability, non-US geographic coverage, or editorial-style alignment.


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "CrisisLTLSum contains 1,000 crisis event timelines across four domains: wildfires, local fires, traffic, and storms." |
| Q2 | 1 | input_content | "We built CrisisLTLSum using a semi-automated cluster-then-refine approach to collect data from the public Twitter stream." |
| Q3 | 1 | output_ontology | "A timeline is a chronologically sorted set of posts, where each brings in new information or updates about an ongoing event (such as a fire, storm, or traffic incident)." |
| Q4 | 1 | input_ontology | "CrisisLTLSum supports two complex downstream tasks: timeline extraction and timeline summarization." |
| Q5 | 1 | input_ontology | "The timeline extraction task is formalized as: given a seed tweet as the initial mention of a crisis event, extract relevant tweets with updates on the same event from the incoming noisy tweet stream." |
| Q6 | 1 | input_ontology | "The timeline summarization task aims to generate abstractive summaries of evolving events by aggregating important details from temporal and incremental information." |
| Q7 | 1 | output_form | "Our initial experiments indicate a significant gap between the performance of strong baselines compared to the human performance on both tasks." |
| Q8 | 1 | input_content | "Our dataset, code, and models are publicly available." |
| Q9 | 1 | output_content | "Hossein Rajaby Faghihi, Bashar Alhafni, Ke Zhang, Shihao Ran, Joel Tetreault, Alejandro Jaimes" |
| Q10 | 1 | output_content | "Michigan State University, New York University Abu Dhabi, Dataminr, Inc." |
| Q11 | 2 | input_ontology | "To the best of our knowledge, this is the first annotated dataset for such an extraction task, while this problem has been tackled before in unsupervised settings (Zhang et al., 2018)." |
| Q12 | 2 | input_ontology | "Moreover, we focus on the extraction of local crisis events. The term "local" indicates that an event is bound to an exact location, such as a building, a street, or a county, and usually lasts for a short period." |
| Q13 | 2 | input_content | "Building a corpus of local crisis events is particularly useful for first responders but also challenging because the timelines of these events are often not captured in existing knowledge sources." |
| Q14 | 2 | input_ontology | "This means one has to design mechanisms for automatically detecting and tracking events directly from the Twitter stream, which is especially hard for existing clustering methods (Guille and Favre, 2015; Asgari-Chenaghlu et al., 2021) given the low number of available tweets for each local event." |
| Q15 | 2 | input_content | "First, the process of identifying and extracting relevant updates for a specific event has to contend with the large volume of noise (Alam et al., 2021a) and informal tone (Rudra et al., 2018) compared to other domains such as news." |
| Q16 | 2 | input_ontology | "Additionally, summarizing an on-going event helps toward a quick and better understanding of its progress. This requires a good level of abstraction with important details covered and properly presented (e.g., the temporal order of event evolution)." |
| Q17 | 2 | output_form | "CrisisLTLSum is the first dataset to provide human-written timeline summaries to support research in this direction." |
| Q18 | 2 | input_content | "CrisisLTLSum is developed through a two-step semi-automated process to create 1,000 local crisis timelines from the public Twitter stream." |
| Q19 | 2 | input_ontology | "To our best knowledge, this is the first timeline dataset focusing on "local" crisis events with the largest number of unique events." |
| Q20 | 2 | input_ontology | "We propose CrisisLTLSum, which is the largest dataset over local crisis event timelines. Notably, this is the first benchmark for abstractive timeline summarization in the crisis domain or on Twitter." |
| Q21 | 2 | output_form | "We develop strong baselines for both tasks, and our experiments show a considerable gap between these models and human performance, indicating the importance of this dataset for enabling future research on extracting timelines of crisis event updates and summarizing them." |
| Q22 | 2 | input_ontology | "While existing datasets on crisis event timelines (Binh Tran et al., 2013; Tran et al., 2015; Pasquali et al., 2021) are limited to a small set of large-scale events, CrisisLTLSum covers a thousand timelines compared to only tens of events covered by each of the existing datasets." |
| Q23 | 2 | input_ontology | "Additionally, we further go beyond the simple tweet categorization by enabling the extraction of information that include updates over the events' progress." |
| Q24 | 2 | input_ontology | "Timeline summarization (TLS) was firstly proposed in Allan et al. (2001), which extracts a single sentence from the news stream of an event topic." |
| Q25 | 2 | input_ontology | "In general, the TLS task aims to summarize the target's evolution (e.g., a topic or an entity) in a timeline (Martschat and Markert, 2018; Ghalandari and Ifrim, 2020)." |
| Q26 | 2 | input_ontology | "Existing approaches of TLS are mainly based on extractive methods, which are often grouped into several categories." |
| Q27 | 3 | input_content | "This section presents our semi-automated approach to collect CrisisLTLSum. We first extract clusters of tweets as noisy timelines and then refine them via human annotation to get clean timelines that only include non-redundant, informative, and relevant tweets." |
| Q28 | 3 | input_form | "Figure 2 shows the process for generating a set of noisy timelines starting from the Twitter stream and followed by pre-processing and knowledge enhancement steps, the online clustering method, and post-processing & cleaning steps." |
| Q29 | 3 | input_content | "We limit the incoming tweets to specific geographical areas, periods, and domains of interest." |
| Q30 | 3 | input_content | "The location filtering relies on a list of location candidates created by gathering cities, towns, and famous neighborhoods in a big area of interest. A tweet is considered relevant to our area of interest if 1) the text mentions one of the candidates, 2) the geo-tag matches the area of interest, or 3) the user location matches the area of interest." |
| Q31 | 3 | input_content | "To limit the tweets to a specified crisis domain, we curate domain-specific keywords and only select tweets with phrases matching one of the keywords. This approach is not comprehensive or exhaustive but somewhat representative of each crisis domain." |
| Q32 | 3 | input_content | "The combinations of (area a, domain d, time t) are manually selected so that the events of type d at location a are more frequent during time period t." |
| Q33 | 3 | input_form | "We use three different modules. First, we use a pre-trained neural model from AllenNLP (Gardner et al., 2018), trained on CoNLL03 (Tjong Kim Sang and De Meulder, 2003), to extract entities with types of people, location, and organization." |
| Q34 | 3 | input_content | "Although this module extracts some important entities in the text, it fails to extract uncommon entities or special mentions" |
| Q35 | 4 | input_form | "Since location mentions are crucial in extracting local events and existing models have low performance detecting them from noisy tweets text, we further developed a BERT-based NER model tuned on Twitter data to detect location mentions." |
| Q36 | 4 | input_form | "Location Augmentation We use OpenStreetMap API to map location mentions to physical addresses." |
| Q37 | 4 | input_form | "This step provides complementary information about each location while reducing the noise introduced by the entity extraction module through removing location mentions that are wrongly detected or are not located in the area of interest." |
| Q38 | 4 | input_ontology | "Online Clustering This step aims to mimic the real-life scenario where tweets are sequentially fed into a clustering algorithm (Wang et al., 2015)." |
| Q39 | 4 | input_ontology | "We further choose this method since this is a lot faster than the retro-spective (all data available at the same time) clustering methods for a large pool of input data." |
| Q40 | 4 | input_ontology | "Here, the clustering objective is to group tweets related to the same local event, such as a "fire in building A" or a "wildfire in a specific area"." |
| Q41 | 4 | output_form | "The online clustering method utilizes a custom similarity metric that combines the similarity of the entities, the closeness of locations in the real world, and the existence of shared hashtags." |
| Q42 | 4 | output_form | "The mindist, maxdist, shashtag, and sdist are hyper-parameters of the clustering algorithm." |
| Q43 | 4 | output_form | "We have only used heuristics and a small set of executions to tune these hyper-parameters." |
| Q44 | 4 | input_ontology | "The new tweet is added to the highest matching-score cluster where the similarity score is higher than simthreshold and the time elapsed between the new tweet and the last update of the cluster is less than timethreshold." |
| Q45 | 4 | input_ontology | "If the previous criteria are met for none of the clusters, a new cluster is created based on the new tweet." |
| Q46 | 4 | input_ontology | "During this process, we remove inactive clusters whose last update was at least expirationthreshold minutes ago and have less than tweetthreshold number of tweets available." |
| Q47 | 4 | input_ontology | "A cluster head is always the tweet with the most entity mentions; In case of a tie, the more recent tweet becomes the head of the cluster." |
| Q48 | 4 | input_ontology | "The hyper-parameters of this method is noted in Appendix A." |
| Q49 | 4 | input_form | "Cluster Post-Processing We apply three post-processing steps to improve the quality of the generated clusters." |
| Q50 | 4 | input_content | "First, we manually merge pairs of clusters with a cluster head similarity higher than a threshold headmin." |
| Q51 | 4 | input_content | "This step compensates for some of the errors from missing entities in the pre-processing step, which affects the intermediate similarity scores in the clustering algorithm." |
| Q52 | 5 | input_content | "We, authors of this work, manually selected 1,000 clusters that contain enough tweets describing how a crisis event evolves, while specifying the "seed tweet" (i.e. the first observed post that describes the ongoing event) of each timeline." |
| Q53 | 5 | input_ontology | "The selected clusters cover events mainly from four crisis domains, including wildfire, local fire, storm, and traffic." |
| Q54 | 5 | output_content | "We use the Amazon Mechanical Turk (MTurk) platform to label and refine the noisy clusters to generate a clean timeline and collect the summaries." |
| Q55 | 5 | output_content | "We split the annotation into multiple batches of Human Intelligence Tasks (HITs), where each batch contains timelines from the same domain." |
| Q56 | 5 | output_content | "Each HIT contains three noisy timelines, and we collect annotations from 3 different workers on each." |
| Q57 | 5 | output_content | "The workers are given the seed tweet and the subsequent tweets sorted by time, and they were asked to read the tweet one by one and answer i) whether the tweet should be part of the timeline, and ii) what is the reason if not." |
| Q58 | 5 | output_ontology | "A tweet is labeled as part of the timeline only if it satisfies all the following three conditions: relevant: talks about the same event indicated in the seed tweet, informative: provides facts about the event but not only contains personal points of view, not repetitive: brings in new information." |
| Q59 | 5 | output_content | "After reviewing all the tweets, the worker is finally asked to write a concise summary to describe how the event progresses over time." |
| Q60 | 5 | output_content | "Following prior quality control practices (Briakou et al., 2021), we use multiple quality control (QC) steps to ensure the recruitment of high-quality annotators." |
| Q61 | 5 | output_content | "First, we use location restriction (QC1) to limit the pool of workers to countries where native English speakers are most likely to be found." |
| Q62 | 5 | output_content | "Next, we recruit annotators who pass our qualification test (QC2), where we ask them to annotate 3 timelines." |
| Q63 | 5 | output_content | "We run several small pilot tasks, each with a replication factor of nine." |
| Q64 | 5 | output_content | "We check annotators' performance on timeline extraction task against experts' labels and have experts manually review (QC3) annotators' summary quality." |
| Q65 | 5 | output_content | "Only workers passing all the quality control steps contribute to the final task." |
| Q66 | 5 | output_content | "During the final task, we perform regular quality checks (QC4), and only use workers who consistently perform well." |
| Q67 | 5 | output_content | "We compensate the workers at a rate of $3 per HIT for the task." |
| Q68 | 5 | output_content | "Each batch of tasks is followed by a one-time bonus that makes the final rate over $10 per hour." |
| Q69 | 5 | input_content | "Out of these 1,000 annotated timelines (10,610 tweets) in CrisisLTLSum, 423 (42%) are about" |
| Q70 | 6 | output_content | "To make the ground-truth on whether each tweet is part of the timeline or not, we take the majority label among the three workers." |
| Q71 | 6 | output_ontology | "4,303 (41%) tweets are labeled as part of the timeline, whereas 6,307 (59%) are not." |
| Q72 | 6 | input_form | "Out of all timelines, 110 (11%) only include tweets that are part of the timeline, whereas 68 (7%) did not include any." |
| Q73 | 6 | input_form | "The majority of the timelines (447 or 45%) have five tweets or less." |
| Q74 | 6 | input_form | "Our dataset includes long timelines of 26 or more tweets, constituting 9% (94 timelines) across all domains." |
| Q75 | 6 | output_content | "We notice an interesting trend across the domains: the longer the timeline, the lower the average percentage of tweets to be part of the timeline." |
| Q76 | 6 | output_content | "To measure the agreement rate between workers on the timeline extraction task, we consider the annotations of two out of three workers who agree most per timeline." |
| Q77 | 6 | output_content | "The average timeline-level agreement between those two workers is 90.06%." |
| Q78 | 6 | output_content | "We also explore a more profound analysis by comparing the workers' annotations on 20% of the timelines against the annotations of experts." |
| Q79 | 6 | output_content | "The average timeline-level agreement rate of this analysis is 91.77%." |
| Q80 | 6 | input_form | "To aid reproducibility when using our dataset for various research experiments, we divided our dataset into: training (TRAIN: 70% or 706 timelines), development (DEV 10% or 86 timelines), and testing (TEST 20% or 208 timelines) splits." |
| Q81 | 6 | input_form | "The splits are created via stratified sampling based on the event crisis domains and the length of timelines (i.e., number of tweets) as shown in Table 2." |
| Q82 | 6 | input_ontology | "Given a crisis event timeline consisting of n tweets T = [t0, t1, ..., tn], where t0 is the seed tweet, i.e. the first observed post that describes the ongoing event, we define two tasks: Timeline Extraction and Timeline Summarization." |
| Q83 | 6 | input_ontology | "Given an initial seed tweet t0, and following chronologically sorted tweets ti, i = 1, ..., n, the goal of the timeline extraction task is to determine whether tweet ti is part of the timeline, i.e., related to the same event and adding new information compared to all prior tweets [t0, ..., ti−1]." |
| Q84 | 7 | input_ontology | "Timeline Summarization: Similar to previous work by Chen et al. (2019), this task aims to generate a summary Ŷ = {ŵ1, ..., ŵk} with sequence of words ŵi to concisely describe the crisis event and its evolution given the output from the timeline extraction task Textracted." |
| Q85 | 7 | input_form | "We construct a list of tweet sequences S by concatenating all the tweets that are part of the timeline from t1 to ti: S = [t1, t1 + t2, ..., t1 + ... + tn]." |
| Q86 | 7 | input_form | "For our first sentence-level classification model, we fine-tune BERT (Devlin et al., 2019) on the tweet sequences where every training example would have the form of "t0 [SEP] si"; where si ∈ S." |
| Q87 | 7 | output_content | "Since each timeline in our dataset is annotated by three workers (§3.2), it includes three summaries." |
| Q88 | 7 | output_content | "To adapt the timeline summarization task to this setting, we pick the two summaries written by the two workers who agree the most based on the timeline extraction labels they assign to the tweets in each timeline." |
| Q89 | 7 | output_content | "This reduces the variance between the summaries regarding their coverage of the crisis event described in the tweets that are part of the timeline." |
| Q90 | 7 | input_form | "During fine-tuning, we double the examples in TRAIN by repeating each timeline twice, once for each summary." |
| Q91 | 7 | output_form | "For evaluation, we use the average timeline-level accuracy." |
| Q92 | 7 | input_form | "Although the BERT-based sequence classification model has a limitation when extracting long timelines due to its limited size of 512 positional embeddings, it performs better than the BERT-GRU sequence labeling model." |
| Q93 | 7 | input_form | "We attribute this to: 1) the careful preprocessing we did when constructing the sequences used to train the BERT-based sequence classification model, and 2) the limited data size, which might not enable the BERT-GRU model to fully capture the sequential relation-" |
| Q94 | 8 | output_form | "For timeline extraction results on the TEST set, we compare both the human-level performance and the best model's performance against experts' annotations." |
| Q95 | 8 | output_content | "To get the human-level performance on the TEST set, we average the performance of the two workers who agree most across all timelines in TEST." |
| Q96 | 8 | output_form | "The best timeline extraction model achieves 73.51 average timeline accuracy, whereas the human-level performance is 88.98." |
| Q97 | 8 | output_form | "This highlights the difficulty of the timeline extraction task and indicates that more involved models are needed to close the gap between model performance and human-level performance." |
| Q98 | 8 | output_form | "We evaluate all timeline summarization models with ROUGE (Lin and Och, 2004)." |
| Q99 | 8 | output_form | "The summarization output of each model is evaluated in a multi-reference setting against the two summaries written by the two workers who agree the most based on the timeline extraction labels." |
| Q100 | 8 | output_form | "We use SacreROUGE (Deutsch and Roth, 2020) to compute multi-reference ROUGE scores." |
| Q101 | 8 | output_form | "For the Seq2Seq pretrained models, we present results in two settings: 1) using the oracle timeline; and 2) using the extracted timeline from the best timeline extraction model." |
| Q102 | 8 | input_form | "In the oracle setting, we use the gold labels in the DEV set to identify tweets that are part of each timeline to the summarization models." |
| Q103 | 8 | output_form | "We further conducted a human evaluation to better assess the quality of the summaries." |
| Q104 | 8 | output_form | "We take the whole TEST set and we evaluate eight summaries per timeline: 1) the three human-written summaries; 2) three model-generated summaries using the three models we develop for timeline summarization in the oracle setting; 3) two summaries from random systems: a random tweet that is part of the timeline, and a summary from a randomly selected timeline that belongs to a different crisis domain." |
| Q105 | 8 | output_content | "Following a similar process in 3.2, we recruit a group of workers from MTurk with the same Location restriction (QC1), who can pass our pilot study as a qualification test." |
| Q106 | 8 | output_form | "Each summary was evaluated by five different workers on a scale from 1 to 5 across four axes: Coherence, Accuracy, Coverage, and Overall quality, as was done by Lai et al. (2022)." |
| Q107 | 8 | output_content | "Detailed instructions and annotation workflows are presented as Figures 15–21 in Appendix E." |
| Q108 | 8 | output_form | "Looking at the results over all the timelines, the human-written summaries are significantly better than the ones generated by models, in terms of overall quality with an average rating of 4.12." |
| Q109 | 9 | input_content | "We presented CrisisLTLSum, the first dataset on local crisis timelines extracted from Twitter and the first to provide human-written summaries on information extracted from Twitter." |
| Q110 | 9 | input_ontology | "We showed that CrisisLTLSum supports two downstream tasks: Timeline Extraction and Timeline Summarization." |
| Q111 | 9 | output_form | "Our experiments with SOTA baselines indicate that both of these tasks are challenging and encourage future research." |
| Q112 | 9 | input_ontology | "Our dataset further provides a resource for developing methods on utilizing microblogs toward aiding first-responders in evaluating ongoing crisis events." |
| Q113 | 9 | output_content | "For timeline extraction, 66 timelines (77%) have at least one error, in which 272 out of 958 tweets (28%) are wrong." |
| Q114 | 9 | output_form | "We observe that the model performance decreases with increasing timeline length for both timeline extraction and summarization tasks, with significant drops in accuracy and ROUGE scores when timelines get longer." |
| Q115 | 9 | output_form | "Most of the summarization errors were due to hallucinations or to copying specific sentences that are present in the timeline without covering all the important event details described in the timeline." |
| Q116 | 10 | output_content | "We thank Aoife Cahill for providing detailed feedback on this paper, Alison Smith-Renner and Wenjuan Zhang for helpful discussions on MTurk annotations, our colleagues at Dataminr, and the EMNLP reviewers for their helpful and constructive comments." |
| Q117 | 10 | input_content | "This study has some limitations on the dataset generation workflow. First, our noisy timeline collection process is not a comprehensive and exhaustive extraction to find all available information about a local crisis event. Here, our focus is to provide a representative dataset rather performing a comprehensive set containing all the local crisis events and their updates." |
| Q118 | 10 | input_content | "Second, the proposed noisy timeline collection pipeline is highly dependent to the performance of the entity extraction modules, especially for the location extraction, and the accuracy of the OpenStreetMap API to find the correct physical address of each location mention." |
| Q119 | 10 | input_content | "Accordingly, replicating the same process for other language or based on other locations may be hard because of such dependencies." |
| Q120 | 10 | output_form | "Furthermore, the online clustering method used in this paper has a set of hyperparameters which are tuned heuristically from a small set of experiments. More comprehensive and large scale experiments on tuning those parameters could potentially impact the quality of the generated timelines." |
| Q121 | 10 | input_content | "Generating similar results by following our noisy timeline collection process is in general limited by the users' access to the public Twitter stream and the changes in the available posts (they may become restricted or deleted)." |
| Q122 | 12 | input_ontology | "We build CrisisLTLSum by limiting the search to four crisis domains: wildfire, local fire, traffic, and storm." |
| Q123 | 12 | input_content | "We collect CrisisLTLSum across seven states in the USA and two states of Australia during 2020 and 2021. The selected states in the USA are New York, Illinois, Massachusetts, California, Texas, and Florida. From Australia, we have selected the states of New South Wales and Victoria." |
| Q124 | 13 | input_content | "These states are selected as they are some of the areas subject to the most events falling into our crisis domains of interest. California, Victoria, and New South Wales are mainly selected due to the abundance of wildfires in hot seasons. Texas and Florida have been selected as they are both subject to wildfires and storm events during different months. Massachusetts and Illinois are selected first because those areas are frequently subjected to bad weather, and second as they contain big cities subject to traffic and local fire events alongside New York." |
| Q125 | 13 | input_form | "This step selects the subset of filtered tweets related to a specific crisis category of interest. Ideally, this task can be performed by a neural model trained on a large set of tweets with labeled data indicating the categories. However, as such a large amount of labeled data is unavailable, we rely on a common approach of designing keywords." |
| Q126 | 13 | input_content | "We carefully curate a keyword list for each of our categories of interest by employing expert knowledge gathered through over-viewing crisis stories in news, social media, and related big disaster events of the past." |
| Q127 | 13 | input_content | "Please note that these lists are generic for each category and not specific to unique events. For instance, instead of defining keywords specific to an event called "Hurricane Ida", our keywords list includes phrases such as "fallen tree", "building collapse", or "storm"." |
| Q128 | 13 | input_content | "The quality of the keywords list is crucial to the final quality of the generated timelines, and we polish this list multiple times based on small sets of experiments before using them for the final task." |
| Q129 | 13 | input_form | "To avoid making a long list of keywords and ensure that different lexical formats of the same word are still considered in the keyword matching process, we maintain both a lower-cased and a lemittized version of the keywords and the tweet's text." |
| Q130 | 13 | input_form | "If any of the keywords exist in the text and in any of these formats, then the tweet is considered related to the category." |
| Q131 | 13 | input_form | "The multi-word keywords are not considered n-grams but as an indication that all the words in the keyword should exist in the text, even if not as a sequence." |
| Q132 | 13 | input_content | "This approach will not be comprehensive or exhaustive but rather representative of each crisis domain. Improving this method to be more encompassing is an area for future research." |
| Q133 | 13 | input_form | "We use the following parameters shared among all different domains: shashtag is set to 0.2 and sdist is 0.3. The simthreshold and timethreshold are set to 0.7 and 15 hours respectively. The timethreshold is reduced to 3 hours to avoid merging various accidents at different times but in the same location. The mindist and maxdist are set to 0.4 kilometer and 4 kilometer for fire and traffic events while having the larger range of 0.4 and 10 kilometers for the wildfire and storm extraction. The expirationthreshold is set to 15 hours and tweetthreshold is 4." |
| Q134 | 13 | input_content | "The online clustering approach may fail to properly relate some tweets due to missing entities, clustering method hyper-parameters, or the difference in the description of various angles of the same story." |
| Q135 | 13 | output_content | "To address this, we merge clusters by comparing all cluster heads with each other and combining those with a higher similarity score than a threshold shead. Additionally, we use human feedback to merge clusters where their similarity score is below shead but higher than a second hyper parameter s min head." |
| Q136 | 13 | input_form | "Here, the goal is to remove tweets from the same cluster with identical or similar text. The duplicate removal relies on a fuzzy string sequence-matching technique to compute the similarity between a pair of tweets. We simply go over each tweet sorted in chronological order and remove the ones that match any of the previous tweets in the same cluster with a matching score higher than dmatch." |
| Q137 | 13 | input_content | "Although the keyword filtering step would reduce the number of tweets unrelated to the category of interest, this step aims to further remove the unrelated clusters generated from the pipeline." |
| Q138 | 14 | input_content | "Our goal is to select 1000 clusters that contain enough tweets describing an evolving crisis event." |
| Q139 | 14 | input_content | "In particular, we first identify a "seed tweet" as the first observed post mentioning a local crisis event, then roughly check whether the following tweets in the cluster contain updates about the same event." |
| Q140 | 14 | input_ontology | "We select clusters across four crisis domains, including wildfire, fire, storm, and traffic, depending on how frequently each type of event happens in extracted noisy clusters." |
| Q141 | 14 | output_form | "We fine-tune BERT base uncased on a single GPU for 10 epochs with a learning rate of 5e-5, batch size of 32, a seed of 42, and a maximum sequence length of 512." |
| Q142 | 14 | output_form | "The GRU has one layer with a hidden size of 128. The model was trained for 50 epochs with early stopping after five epochs if the performance did not improve on the DEV set. We use a learning rate of 5e-5, a batch size of 16, and a seed of 42." |
| Q143 | 14 | output_form | "We fine-tune BART based on a single GPU for ten epochs with a learning rate of 5e-5, batch size of 16, a seed of 42, and a maximum target sequence length of 512." |
| Q144 | 14 | output_form | "During inference, we use beam search with a beam size of 4." |
| Q145 | 14 | output_content | "To ensure the workers have a good understanding of the QE dimensions listed in the rubrics, as shown in Figure 18, the workers are asked to pass a screening test before they can access the quality rating part of the task interface." |
| Q146 | 15 | input_content | "Table 8: Aggregated data statistics based on crisis domains and timeline lengths of the TRAIN, DEV, and TEST splits." |
| Q147 | 15 | output_content | "Once they answer the test question with the correct answer, the rating interface will show up, as shown in Figure 19." |
| Q148 | 15 | output_content | "In this page, we display the original tweet timeline on the left hand side of the rating interface." |
| Q149 | 15 | output_content | "Before displaying all the summaries and the rating options, to make sure the workers go over the timeline carefully, we ask them to use the length of the timeline to answer the last screening question before conducting the rating task." |
| Q150 | 15 | output_content | "The rating part of the interface is shown in Figures 20 and 21." |
| Q151 | 21 | output_ontology | "During this task, you will be reading a timeline that consists of a sequence of tweets describing an event and eight different summaries for the event in the timeline. You will rate the quality of each of the eight summaries by four axes: coherence, accuracy, coverage, and overall quality." |
| Q152 | 21 | output_content | "The rubrics below give specific guidance on how each axis should be rated. Please read the rubrics carefully before continuing to the task." |
| Q153 | 21 | output_ontology | "For each summary, answer the question "how coherent is the summary on its own?" on a scale 1 to 5. A summary is coherent if when read by itself, it's easy to understand and free of English errors. A summary is not coherent if it's difficult to understand what the summary is trying to say. Generally, it's more important that the summary is understandable than it being free of grammar errors." |
| Q154 | 21 | output_ontology | "Score of 1: The summary is impossible to understand. Score of 2: The summary has many mistakes or confusing phrasing. Score of 3: The summary has some mistakes or confusing phrasing that made it hard to understand. Score of 4: The summary is mostly clear with only a few minor mistakes or confusing phrasing. Score of 5: The summary is perfectly clear." |
| Q155 | 21 | output_ontology | "For each summary, answer the question "Does the factual information in the summary accurately match the information in the timeline?" on a scale of 1 to 5. A summary is accurate if it doesn't say things that aren't in the timeline, it doesn't mix up information, and generally is not misleading." |
| Q156 | 21 | output_ontology | "Score of 1: The summary is completely wrong, made up, or exactly contradicts what is written in the timeline. Score of 2: The summary says many things not mentioned in or contradicting the timeline. Score of 3: The summary says at least one crucial piece of information that is not in the timeline, or it contradicts something in the timeline. Score of 4: The summary says anything at all that is not mentioned in the timeline or contradicts something in the timeline. Score of 5: The summary has no incorrect statements or misleading implications." |
| Q157 | 21 | output_ontology | "For each summary, answer the question "How well does the summary cover the important information in the timeline?" on a scale of 1 to 5. A good summary has good coverage if it mentions the main information from the timeline that's important to understand the event. A summary has poor coverage if someone reading only the summary would be missing several important pieces of information about the event in the timeline." |
| Q158 | 21 | output_ontology | "Score of 1: The summary contains no information relevant to the timeline. Score of 2: The summary is missing many important pieces of information required to understand the timeline. Score of 3: The summary is missing at least one crucial piece of information required to understand the timeline. Score of 4: The summary is missing some important information from the timeline. Score of 5: The summary covers all of the important information required to understand the timeline." |
| Q159 | 21 | output_ontology | "For each summary, answer the question "How good is the summary overall at representing the timeline?" on a scale of 1 to 5. This encompasses all of the above axes, as well as the information included in the summary and if it has helped you understand the event. If it's hard to find ways to make the summary better, give the summary a high score. If there are lots of different ways the summary could be better, give the summary a low score." |
| Q160 | 21 | output_ontology | "Score of 1: The summary is terrible. Score of 2: The summary is a pretty bad representation of the timeline and needs significant improvement. Score of 3: The summary is an okay representation of the timeline, but could be significantly improved. Score of 4: The summary is a pretty good representation of the timeline, but it's not perfect. Score of 5: The summary is an excellent representation of the timeline." |
| Q161 | 21 | output_content | "Now you will review an example timeline and two associated summaries." |
| Q162 | 21 | output_content | "For each of the summaries, we have provided ratings on the four axes: coherence, accuracy, coverage, and overall quality with explanations for why these ratings were chosen." |

---

## Regional Context

```yaml
name: Mexico City and Central America Bilingual Crisis Journalism
abbreviation: CDMX-CrisisJourn
assessment_context:
  benchmark: crisisltlsum
  use_case: AI summarization system processing social-media posts (primarily tweets)
    about crisis events to assist journalists and media workers in writing breaking-news
    articles. Covers events in Mexico City, Central America, and the US–Mexico border
    region.
  deployment_population: Journalists and media workers based primarily in Mexico City,
    fluent in both Mexican Spanish (native, neutral/standard variety) and English,
    covering breaking news across Mexico, Central America, and the southern United
    States under outlet-specific or wire-service editorial guidelines (e.g., AP Español).
primary_countries:
- Mexico (primary — Mexico City as hub)
- Guatemala
- Honduras
- El Salvador
- Nicaragua
- Costa Rica
- Panama
- United States (southern border region — Texas, California, Arizona, New Mexico)
primary_region_description: Deployment is centered on Mexico City (CDMX) as the journalistic
  hub, with coverage extending southward through Central America and northward to
  the US–Mexico border. The core user is a bilingual, professionally trained journalist
  operating in a high-stakes breaking-news newsroom environment, not a general public
  user.
languages:
  primary_working_languages:
  - Mexican Spanish (native; neutral/standard Latin American variety acceptable as
    system baseline; final register adaptation performed by journalist)
  - American English (high-proficiency; expected to be the higher-quality output language
    for direct use)
  language_notes: Users are bilingual professionals. English summaries are expected
    to be more directly publication-ready; Spanish summaries will require journalist
    revision for register and Mexican journalistic style. Neutral Latin American Spanish
    is acceptable as a system baseline. AP Español guidelines govern Spanish-language
    wire-service output for many outlets.
  regional_spanish_varieties:
    mexico_city: Neutral urban Mexican Spanish; basis for broadcast and print norms
    central_america: 'Voseo (use of ''vos'' as second-person singular pronoun) is
      a well-documented feature in Guatemala, Honduras, El Salvador, Nicaragua, and
      Costa Rica, and appears in informal/social-media registers. Panama generally
      uses tuteo. Source tweets from these regions may exhibit voseo verb conjugations
      and regionally distinct vocabulary that differ from neutral Mexican Spanish.
      This is a [NEEDS VERIFICATION — deferred: lived dialectal practice; degree of
      voseo penetration in crisis-specific tweets requires corpus analysis rather
      than web search] phenomenon requiring empirical corpus analysis.'
    border_region: High incidence of Spanglish and code-switching in social-media
      source content, particularly in tweets from Texas and California border communities
  code_switching_notes: Social-media source content (tweets) from border regions and
    some Central American users may include English–Spanish code-switching, Spanglish
    constructions, and informal registers that differ substantially from the professional
    output register expected by journalists.
  indigenous_language_considerations: 'Tweets from non-CDMX regions of Mexico (Oaxaca,
    Chiapas, Yucatán, etc.) and from Guatemala may embed indigenous-language place
    names or lexical items (Nahuatl, Maya, Zapotec, Mam, K''iche'', etc.) in otherwise
    Spanish-language text. Whether the deployed system must handle these is unresolved
    — flagged for further investigation. [NEEDS VERIFICATION — deferred: likely unsearchable
    (lived practice); frequency in crisis-specific tweets requires corpus study not
    available via web search]'
writing_systems:
  scripts:
  - Latin alphabet (Spanish and English — both deployment languages)
  - Standard Spanish diacritics (á, é, í, ó, ú, ñ, ü) required for correct Spanish
    output
  - No RTL or non-Latin script requirements in this deployment
  notes: Spanish tokenization, lemmatization, and NLP preprocessing infrastructure
    must handle accented characters and Spanish-specific morphology. Tweet-register
    input may omit diacritics (a common informal practice); the system must handle
    diacritic-dropped input gracefully.
professional_context:
  user_role: Journalists and media workers — professionally trained, deadline-driven,
    operating in breaking-news workflow
  editorial_standards:
    wire_service_reference: AP Español (cited by user as the relevant style standard
      for many outlets)
    ap_espanol_notes: '[NEEDS VERIFICATION — deferred: below search budget; AP Español
      guidelines are proprietary style documents not fully indexed on the open web.
      The AP Stylebook in Spanish exists as a commercial product. Specific operationalizable
      criteria for casualty framing, official source attribution, and community impact
      language in the Mexican context require expert elicitation or direct access
      to the AP Español manual.]'
    outlet_level_variation: Individual outlets may apply their own house style on
      top of AP Español or in lieu of it; the system is expected to produce broad
      summaries that journalists adapt rather than style-compliant copy
    preferred_output_posture: Less restrictive, broader summaries that journalists
      can then edit — the system should not pre-constrain to a single editorial voice
  workflow_position: System output is an intermediate artifact in a journalist's research
    and drafting process, not a publishable final product. Journalists perform final
    register adaptation, fact-verification, and editorial shaping.
  professional_norms_diverging_from_us_norms:
    casualty_framing: '[NEEDS VERIFICATION — deferred: likely unsearchable (professional
      norms encoded in proprietary style guides and journalistic tradition, not in
      indexed documents); requires expert elicitation from Mexican journalists or
      AP Español editors]'
    official_source_attribution: 'Key Mexican emergency management institutions whose
      statements carry authoritative weight in crisis reporting include: CENAPRED
      (Centro Nacional de Prevención de Desastres), subordinated to the Secretaría
      de Seguridad y Protección Ciudadana; the Coordinación Nacional de Protección
      Civil (@CNPC_MX on X/Twitter, with 100K+ posts); the Servicio Meteorológico
      Nacional (SMN, under CONAGUA); and the Servicio Sismológico Nacional (SSN, a
      UNAM agency). These differ substantially from US norms where fire departments,
      FEMA, and NWS are the primary crisis-authority sources. Source: Wikipedia CENAPRED
      entry — [WEB-1]; US Embassy Mexico City emergency
      guidance — [WEB-2]'
    community_impact_language: '[NEEDS VERIFICATION — deferred: likely unsearchable
      (lived journalistic practice); requires expert elicitation]'
    political_sensitivity: Crisis events in Mexico and Central America may carry political
      dimensions (government response accountability, organized crime involvement
      in border incidents, migration-related emergencies) that affect what information
      is foregrounded in summaries. These editorial judgments are absent from the
      benchmark's US-centric annotation framework.
crisis_ontology:
  benchmark_covered_types:
  - Wildfires (partial overlap — present in Mexico's dry season, but different geographic/ecological
    contexts)
  - Local fires (overlapping — structural fires in urban Mexico City context are broadly
    similar)
  - Traffic incidents (overlapping — but CDMX traffic and accident reporting has distinct
    local context, including metro/transit system)
  - Storms (partial overlap — hurricane/tropical-system storms on Pacific and Gulf
    coasts differ substantially from US storm profiles in the benchmark)
  benchmark_missing_types_high_priority:
  - crisis_type: Earthquakes
    regional_relevance: Mexico City sits on a seismically active zone with a history
      of major earthquakes (1985, 2017, 2022 Michoacán); earthquakes are among the
      highest-priority crisis types for CDMX journalists
    notes: 'The CrisisNLP HumAID dataset (ICWSM 2021) includes a subset for the 2017
      Mexico earthquake (~2,563 labeled tweets), but this is an English-language dataset
      and does not constitute a Spanish-language crisis-NLP resource. A Spanish-language
      NER model for earthquake tweet geolocation trained on Mexican Spanish tweets
      (merged CoNLL-2002 Spanish + manually annotated earthquake tweets from 2017,
      2014, 2012 events) was developed by Curiel et al. (PMC, 2019) as a case study
      — this is the closest known Mexican-Spanish crisis NLP resource. No Spanish-language
      crisis timeline extraction or summarization dataset anchored to Mexican earthquakes
      exists. Sources: HumAID dataset documentation — [WEB-3];
      Curiel et al. Twitter/NER earthquake study — [WEB-4]'
  - crisis_type: Volcanic activity
    regional_relevance: Popocatépetl (active volcano near CDMX) generates ongoing
      alert phases; Volcán de Fuego (Guatemala) produces periodic eruptions with high
      casualty potential; Colima also relevant
    notes: 'No crisis NLP dataset specifically covering volcanic event Twitter monitoring
      in Spanish was found in search. CENAPRED monitors Popocatépetl continuously
      and issues daily reports; the official Twitter account @CenapredMexico and @CNPC_MX
      are the primary official dissemination channels for volcanic alert information.
      Source: CENAPRED official site — [WEB-5]'
  - crisis_type: Tropical-system flooding (hurricanes, tropical storms, depressions)
    regional_relevance: Both Pacific (Baja California, Guerrero, Oaxaca, Chiapas)
      and Gulf/Caribbean (Veracruz, Yucatán, Tabasco, all of Central America) coasts
      are affected; flooding associated with these systems is distinct from convective
      storm flooding in the benchmark's US data
    notes: '[NEEDS VERIFICATION — deferred: below search budget; no Spanish-language
      hurricane/tropical-flooding crisis Twitter dataset identified in searches conducted;
      TREC-IS includes some hurricane events but the dataset is English-only]'
  - crisis_type: Civil unrest / social protests / political violence
    regional_relevance: Mexico City is a hub for national protests; Central American
      contexts include politically motivated violence, migration-related crises, and
      gang/cartel activity that intersects with humanitarian crisis reporting
    notes: '[NEEDS VERIFICATION — deferred: below search budget; no Latin American
      civil-unrest crisis NLP dataset identified; this category also raises editorial
      and safety concerns that make benchmark construction difficult]'
  - crisis_type: Organized crime / cartel-related incidents (road blockades, violence
      affecting civilian movement)
    regional_relevance: In Mexico and parts of Central America, certain crisis events
      that impede civilian movement or create public safety emergencies are crime-related
      rather than purely natural-disaster or accident-related; these require distinct
      sourcing and framing norms
    notes: '[NEEDS VERIFICATION — deferred: likely unsearchable (no indexed NLP research
      on cartel-adjacent crisis events found; this is a highly sensitive category
      with sparse academic documentation)]'
  - crisis_type: Transportation infrastructure failures (CDMX metro/tren ligero collapses,
      road subsidence due to relleno/land subsidence)
    regional_relevance: Mexico City's metro system has experienced serious structural
      incidents; the city sits on former lakebed with chronic subsidence; these are
      locally specific crisis types with no US analog in the benchmark
    notes: '[NEEDS VERIFICATION — deferred: below search budget; low likelihood of
      existing NLP dataset coverage; this is a CDMX-specific crisis type requiring
      bespoke corpus construction]'
  storm_category_transferability_notes: 'Even for the nominally overlapping ''storms''
    category, the benchmark''s keyword lists and event profiles reflect US meteorological
    conventions. Mexican and Central American tropical systems (naming conventions,
    alert phases used by SMN and CONRED/NHC, wind speed thresholds, Saffir-Simpson
    vs. regional scales, storm surge vocabulary in Spanish) differ in ways that may
    invalidate keyword-transfer assumptions. [NEEDS VERIFICATION — deferred: below
    search budget; comparison of US vs. Mexican storm crisis vocabulary requires corpus
    analysis]'
geographic_entities:
  mexico_city_administrative_structure:
    description: Mexico City (CDMX) is organized into 16 alcaldías (formerly delegaciones),
      each subdivided into colonias. These are the primary sub-city location references
      in local crisis reporting and in social-media posts about CDMX events.
    alcaldias:
    - Iztapalapa
    - Gustavo A. Madero
    - Álvaro Obregón
    - Tlalpan
    - Xochimilco
    - Tláhuac
    - Coyoacán
    - Cuauhtémoc
    - Miguel Hidalgo
    - Benito Juárez
    - Venustiano Carranza
    - Iztacalco
    - Azcapotzalco
    - Cuajimalpa de Morelos
    - Magdalena Contreras
    - Milpa Alta
    notable_colonias_for_crisis_coverage: '[NEEDS VERIFICATION — deferred: likely
      unsearchable (sub-colonia risk distribution requires local hazard mapping data
      not indexed via web search; CENAPRED risk atlases exist but are not machine-readable
      in this context)]'
    location_resolution_challenge: 'The benchmark''s location pipeline uses US/Australian
      city and neighborhood lists plus English-language OpenStreetMap queries. Mexican
      colonia names (e.g., Doctores, Tepito, Vallejo, Del Valle) and alcaldía names
      are absent; Spanish-language OSM queries and dedicated Mexican gazetteer resources
      are required. A Mexican-Spanish NER + geolocation pipeline for earthquake tweets
      was developed by Curiel et al. (PMC 2019) using CoNLL-2002 Spanish merged with
      manually annotated Mexican earthquake tweets — the only known proof-of-concept
      for this task. Source: [WEB-4]'
  national_mexico_administrative_structure:
    description: Mexico is organized into 31 estados plus CDMX, each subdivided into
      municipios. Crisis reporting beyond CDMX requires resolution of municipio-level
      location references, which have no direct analog in the US county-level schema
      used by the benchmark.
    key_states_for_crisis_coverage:
    - Estado de México (borders CDMX, high seismic and Popocatépetl risk)
    - Puebla (Popocatépetl corridor)
    - Morelos (Popocatépetl corridor)
    - Veracruz (Gulf coast, flooding, industrial risk)
    - Oaxaca (seismic, Pacific coast, indigenous-language place names)
    - Guerrero (Pacific coast, storm risk, organized crime context)
    - Chiapas (border with Guatemala, tropical flooding, migrant crisis)
    - Tabasco (flooding, historically affected by tropical systems)
    - Jalisco (second city Guadalajara, wildfires, cartel activity)
    - Baja California / Sonora (US border, cross-border incidents)
    indigenous_place_names: '[NEEDS VERIFICATION — deferred: likely unsearchable (frequency
      in crisis-specific tweets requires corpus study); requires stakeholder/expert
      elicitation from linguists familiar with Nahuatl, Zapotec, Maya, Mam, and K''iche''
      toponymy in the relevant states]'
  central_america_administrative_structure:
    description: Central American coverage spans six countries, each with distinct
      administrative terminologies (departamentos, municipios, distritos). Landmark
      and regional references in tweets may use informal geographic nicknames rather
      than formal administrative names.
    key_administrative_units: '[NEEDS VERIFICATION — deferred: below search budget;
      primary departamento/municipio structures for Guatemala, Honduras, El Salvador,
      Nicaragua, Costa Rica, and Panama are documented in national census sources
      but their relevance weighting for crisis-tweet georesolution requires expert
      assessment]'
    notable_landmarks_for_crisis_coverage: '[NEEDS VERIFICATION — deferred: below
      search budget; requires expert elicitation from Central American journalists]'
  us_mexico_border_region:
    description: Cross-border crisis events (bridge closures, flooding of the Rio
      Grande/Río Bravo, border-crossing incidents, industrial accidents in maquiladora
      zones) require resolving location references that span two national administrative
      systems and two languages simultaneously.
    key_locations: 'Primary border crossing pairs relevant to crisis coverage: Tijuana–San
      Diego (CA), Ciudad Juárez–El Paso (TX), Nuevo Laredo–Laredo (TX), Reynosa–McAllen
      (TX), Matamoros–Brownsville (TX). These represent the highest-volume pedestrian
      and commercial crossings on the US–Mexico border and are the most likely nodes
      for cross-border crisis events in this deployment''s coverage area. [NEEDS VERIFICATION
      — deferred: specific crossing-level crisis incident frequency requires CBP or
      INAMI data not retrieved in current search budget]'
social_media_context:
  platform: Twitter/X (primary per elicitation summary)
  spanish_twitter_crisis_corpora:
    known_resources: 'Search found no Spanish-language crisis tweet corpus anchored
      to Mexican or Central American events suitable for timeline extraction or summarization
      tasks. The closest relevant resources are: (1) HumAID (ICWSM 2021) — English-only,
      77K labeled tweets across 19 disaster events including a 2017 Mexico earthquake
      subset (~2,563 tweets), but English-language only. Source: [WEB-3].
      (2) Curiel et al. (PMC 2019) — Spanish-language NER model for geolocation of
      Mexican earthquake tweets, trained on CoNLL-2002 Spanish + manually annotated
      tweets from Mexico City earthquakes (2012, 2014, 2017); this is the closest
      known Mexican-Spanish crisis NLP resource but is a classification/NER tool,
      not a summarization dataset. Source: [WEB-4].
      (3) TREC-IS — contains a ''guatemalaEarthquake2012'' event subset with English-language
      tweets, but not Spanish. Source: [WEB-6].
      No CLEF-HIPE or IULA Spanish crisis tweet corpus specifically targeting Mexican
      or Central American events was identified.'
    gap_assessment: 'Confirmed: No Spanish-language crisis tweet corpus anchored to
      Mexican or Central American events exists for timeline extraction or summarization
      tasks. This is a critical primary data gap. The CrisisNLP ecosystem is predominantly
      English-language.'
  mexican_spanish_twitter_conventions:
    informal_register: Crisis-related tweets in Mexican Spanish routinely omit diacritics,
      use colloquial vocabulary (e.g., 'temblor' vs. 'sismo', 'neza' for Nezahualcóyotl,
      'edomex' for Estado de México), and employ hashtag conventions specific to Mexican
      events
    common_crisis_hashtags: 'Confirmed active SASMEX hashtag conventions: #TenemosSismo
      (all earthquake reports) and #AlertaSismica (warnings of serious earthquakes)
      are the official SASMEX/CIRES dissemination hashtags on X/Twitter. During the
      2017 #19S earthquake, citizen-generated verification hashtags #Verificado19S
      and #AquiNecesitamos were widely used for coordination and misinformation filtering.
      These hashtag ecosystems are distinct from US crisis hashtag conventions and
      are critical for timeline extraction keyword lists. Sources: Wikipedia SASMEX
      article — [WEB-7]; SASMEX
      X account — [WEB-8]; Medium/HCI@WVU post on #19S hashtags —
      [WEB-9]'
    official_account_ecosystem: 'Key authoritative Mexican emergency-management X/Twitter
      accounts: @CenapredMexico (CENAPRED — volcanic and seismic monitoring, subordinated
      to SSPC); @CNPC_MX (Coordinación Nacional de Protección Civil — national civil
      protection coordination, 100K+ posts); @SASMEX / AlertaSísmica SASMEX (CIRES
      — official seismic alert dissemination); @SismologicoMX (Servicio Sismológico
      Nacional/SSN — UNAM earthquake monitoring). The official government guidance
      directs the public to www.gob.mx/cenapred and @CNPC_MX as the authoritative
      channels. Sources: CENAPRED Wikipedia — [WEB-1];
      US Embassy Mexico guidance — [WEB-2];
      CNPC_MX X profile — [WEB-10]'
  noise_characteristics: Crisis tweet streams in Mexico and Central America include
    retweets of government alerts, citizen reports of variable reliability, misinformation
    propagation (historically significant in Mexican earthquake events), and politically
    motivated framing. The US-derived relevance/informativeness annotation framework
    may not correctly weight these local noise patterns.
regulatory_and_institutional_context:
  emergency_management_agencies:
    mexico_national: 'Confirmed current institutional structure: CENAPRED (Centro
      Nacional de Prevención de Desastres) is an administrative organ subordinated
      to the Secretaría de Seguridad y Protección Ciudadana (SSPC); its Twitter presence
      is @CenapredMexico. The Coordinación Nacional de Protección Civil (CNPC, @CNPC_MX)
      provides national civil protection coordination. The Servicio Sismológico Nacional
      (SSN) is a UNAM agency (@SismologicoMX) that monitors and reports on earthquakes.
      The Servicio Meteorológico Nacional (SMN) is part of CONAGUA and monitors weather/tropical
      systems. CENAPRED monitors Popocatépetl and other volcanic hazards continuously
      and publishes daily reports at cenapred.unam.mx. Sources: Spanish Wikipedia
      CENAPRED entry — [WEB-11];
      CENAPRED official site — [WEB-5]; disaster response
      services overview — [WEB-12]'
    mexico_cdmx: 'The CDMX civil protection body maintains a Popocatépetl monitoring
      page at data.proteccioncivil.cdmx.gob.mx and coordinates directly with CENAPRED.
      Current alert status as of early 2026: Semáforo Amarillo Fase 2. Source: CDMX
      Secretaría de Protección Civil monitoring page — [WEB-13]'
    central_america: 'Confirmed national civil protection agencies and Twitter/social-media
      presence: Guatemala — CONRED (Coordinadora Nacional para la Reducción de Desastres);
      Honduras — COPECO (Comisión Permanente de Contingencias); El Salvador — DGPC
      (Dirección General de Protección Civil); Nicaragua — SINAPRED (Sistema Nacional
      para la Prevención, Mitigación y Atención de Desastres); Costa Rica — CNE (Comisión
      Nacional de Prevención de Riesgos y Atención de Emergencias); Panama — SINAPROC
      (Sistema Nacional de Protección Civil). All maintain official social media presence
      but their Twitter/X account activity and authority level vary by country. Source:
      disaster response services documentation — [WEB-12]'
    us_border_relevant: FEMA, NWS (National Weather Service), CBP — relevant for cross-border
      crisis events
  data_and_press_law_context:
    mexico_press_freedom: '[NEEDS VERIFICATION — deferred: below search budget; press
      freedom context in Mexico is well-documented (RSF, CPJ) but the specific implication
      for crisis summary generation requires expert journalistic assessment rather
      than web-sourced facts]'
    data_protection: '[NEEDS VERIFICATION — deferred: below search budget; Mexico''s
      data protection law (Ley Federal de Protección de Datos Personales en Posesión
      de los Particulares, LFPDPPP, 2010) and its implementing regulations are the
      applicable framework for processing tweet content about identified individuals;
      verification of whether any successor legislation has been enacted is warranted
      but was not prioritized in the current search budget]'
infrastructure_notes:
  journalist_infrastructure: Target users are professional journalists in a newsroom
    setting — high-quality internet connectivity, desktop/laptop primary devices,
    professional publication-grade output expectations. No mobile-first or low-bandwidth
    constraints apply to the end user.
  source_tweet_infrastructure: Tweets being processed originate from a broader population
    (citizens, officials, emergency services) that may include users on mobile-only,
    lower-bandwidth connections, particularly in rural Central America and remote
    Mexican states. This affects tweet length, attachment type, and linguistic register
    of source content.
  mobile_internet_penetration_mexico: 'Mexico had approximately 152.44 million mobile
    phone connections in 2024, averaging 1.2 mobile phones per person (above the US
    figure of 1.1). Mobile internet download speed averages 43.33 Mbit/s (87th globally
    per Ookla January 2026 data). This indicates high mobile device penetration for
    source tweet generation, though connectivity quality varies significantly between
    urban CDMX and rural states. This is a national aggregate; sub-national variation
    is likely substantial. Source: worlddata.info telecom data citing ITU/Ookla —
    [WEB-14]'
  mobile_internet_penetration_central_america: '[NOT FOUND — searched ITU Facts and
    Figures 2024 and World Bank WDI; country-specific Central America mobile internet
    penetration figures were not returned in the search results. ITU DataHub at datahub.itu.int
    contains country-level data but specific Central America figures were not extracted
    within budget. Recommend direct ITU DataHub query: [WEB-15]]'
  twitter_penetration_mexico: '[NEEDS VERIFICATION — deferred: below search budget;
    Twitter/X active user counts for Mexico are not reliably published by the platform;
    third-party estimates vary. WhatsApp was documented as a major parallel channel
    for crisis misinformation during the 2017 earthquake (alongside Twitter), suggesting
    Twitter is not the sole or necessarily dominant crisis information channel in
    Mexico. Source: PS Mag 2017 earthquake misinformation reporting — [WEB-16]]'
  nlp_tooling_for_mexican_spanish:
    general_availability: Spanish is a high-resource NLP language globally, but Mexican
      Spanish–specific resources (trained on Mexican Twitter, covering Mexican place
      names and crisis vocabulary) are substantially less common than general Spanish
      resources
    crisis_specific_gap: 'The only identified Spanish-language crisis NER model specifically
      trained on Mexican earthquake tweets is from Curiel et al. (PMC 2019), which
      merged CoNLL-2002 Spanish NER data with manually inspected tweets from Mexico
      City earthquake events (2012, 2014, 2017). This model targets toponym extraction
      and geolocation rather than timeline extraction or summarization. No Spanish
      crisis-NLP models from TREC-IS, CrisisNLP, or published academic groups covering
      Mexican geographic entities at the colonia/alcaldía level were identified. Source:
      Curiel et al. — [WEB-4]'
evaluation_framework_implications:
  output_language_gap: The benchmark provides no Spanish-language reference summaries,
    no Spanish coherence rubric, and no bilingual evaluation protocol. Any assessment
    of Spanish-language output quality requires constructing a parallel evaluation
    framework.
  bilingual_rouge_notes: 'For Spanish-language summarization evaluation, the research
    literature suggests: (1) Standard ROUGE variants perform poorly for Spanish summarization
    as a sole metric — a 2025 study (arXiv 2503.17039) evaluating Spanish and Basque
    summarization found that most ROUGE variants correlate weakly with human judgments;
    (2) BERTScore-precision using multilingual models (XLM-R, mBERT) shows stronger
    correlation with human coherence and relevance judgments across languages, including
    Spanish; (3) LLM-as-a-judge approaches (GPT-4 class models) show promising correlation
    with human judgments in multilingual summarization (EMNLP 2024 re-evaluation study).
    A combined metric approach of BERTScore (with multilingual backbone) + LLM-as-judge
    + human evaluation with Spanish-speaking annotators is the current best practice
    for Spanish summarization evaluation. No dedicated Spanish crisis summarization
    evaluation benchmark exists. Sources: arXiv 2503.17039 Spanish/Basque summarization
    metrics — [WEB-17]; EMNLP 2024 multilingual summarization
    re-evaluation — [WEB-18]'
  ap_espanol_alignment_rubric: '[NEEDS VERIFICATION — deferred: AP Español style guidelines
    are a proprietary commercial product; no operationalizable open-access version
    was found. The downstream assessment should flag this as requiring direct access
    to AP Español guidelines or expert elicitation from AP Español editors.]'
  ground_truth_annotation_requirements: Any localized benchmark adaptation would require
    Spanish-speaking annotators with familiarity with Mexican crisis event types,
    Mexican geographic entities, and Latin American journalistic norms — a substantially
    different annotator profile from the English-speaking MTurk workers used in the
    original benchmark.
  relevance_label_transferability: The benchmark's three-way relevance/informativeness/non-redundancy
    label schema is conceptually sound but was validated only on US English tweets
    by Anglophone annotators. Cross-lingual transfer validity to Mexican Spanish tweets
    covering earthquake, volcanic, or civil-unrest events is unestablished and should
    be empirically assessed.
  coherence_rubric_language_adaptation: The benchmark's coherence rubric explicitly
    references 'English errors' as the evaluation criterion. A Spanish-language analog
    must be constructed that references Spanish-language writing norms and, where
    relevant, Mexican journalistic register conventions.
cultural_and_editorial_norms:
  crisis_reporting_culture: Mexican and Latin American crisis journalism operates
    in a context of complex institutional trust dynamics — official government agency
    statements (Protección Civil, CENAPRED) carry authority but are also subject to
    scrutiny; citizen social-media reports are a primary source for speed but require
    verification framing.
  seismic_alert_system_context: 'SASMEX (Sistema de Alerta Sísmica Mexicano), administered
    by CIRES (Centro de Instrumentación y Registro Sísmico), provides up to 60 seconds''
    warning to Mexico City and other cities. It disseminates alerts via dedicated
    receivers, public loudspeakers, radio/TV, and X/Twitter, reaching an estimated
    25 million people. The official SASMEX/CIRES X account (@SASMEX / AlertaSísmica
    SASMEX) posts all earthquake detections as #TenemosSismo and serious warnings
    as #AlertaSismica — these are the seed-tweet vocabulary for any earthquake timeline
    extraction in this deployment. The 2017 Chiapas (M8.1) and Puebla (M7.1, #19S)
    earthquakes demonstrated both the system''s effectiveness and its limitations
    for near-distance events. The @SismologicoMX (SSN/UNAM) account also posts post-event
    seismological data. Sources: Wikipedia SASMEX — [WEB-7];
    SASMEX X account — [WEB-8]; Frontiers Earth Science SASMEX retrospective
    — [WEB-19]'
  volcanic_alert_level_vocabulary: 'CENAPRED''s Semáforo de Alerta Volcánica uses
    a three-color, seven-phase system for Popocatépetl and other monitored volcanoes:
    Verde Fase 1 (calma/dormido), Verde Fase 2 (ligera actividad); Amarillo Fase 1
    (manifestación de actividad), Amarillo Fase 2 (incremento de actividad), Amarillo
    Fase 3 (actividad intermedia a alta); Rojo Fase 1 (actividad explosiva de peligro
    intermedio a alto), Rojo Fase 2 (actividad explosiva de peligro alto a extremo).
    As of May 2026, Popocatépetl is at Amarillo Fase 2. Daily status reports are published
    at cenapred.unam.mx/reportesVolcanesMX/ and official channels cite @CNPC_MX as
    the authoritative source. The volcano is colloquially called ''Don Goyo'' in social
    media. This vocabulary (semáforo color + fase number + specific hazard terms like
    ''exhalaciones'', ''ceniza'', ''fragmentos balísticos'', ''flujos piroclásticos'',
    ''lahares'') is the essential lexicon for any volcanic crisis timeline extraction
    keyword list and is entirely absent from the benchmark''s storm/fire/traffic vocabulary.
    Sources: CENAPRED monitoring page — [WEB-20];
    Milenio explainer — [WEB-21];
    CNN Español alert level explainer — [WEB-22]'
  community_solidarity_conventions: Mexican crisis social media often features community
    coordination posts (offering shelter, requesting blood donations, organizing volunteer
    rescue brigades — as notably observed after the 2017 earthquake). These posts
    have distinct informativeness profiles that may differ from the benchmark's US-centric
    informativeness judgments.
  political_and_institutional_sensitivity: Crisis summaries touching on government
    response adequacy, infrastructure failure, or migration-adjacent emergencies carry
    political weight in the Mexican journalistic context that has no direct analog
    in the benchmark's fire/traffic/storm framing.
  misinformation_dynamics: 'The 2017 #19S Mexico City earthquake (M7.1, September
    19) generated well-documented, large-scale misinformation on Twitter, WhatsApp,
    and Facebook. Major media outlets (including Televisa) spread false stories (e.g.,
    the fabricated ''Frida Sofía'' trapped schoolgirl narrative). Citizens organized
    misinformation-countering networks using hashtag #Verificado19S and Google Spreadsheets
    for ground-truth verification; journalists were found to engage earlier than non-journalists
    in both spreading and correcting false rumors. A detailed multi-platform analysis
    (2.9M tweets + Facebook posts + Slack messages over one month post-earthquake)
    is documented in Flores-Saviaga & Savage (2020/arXiv 2007.05848). This misinformation
    ecosystem differs fundamentally from the benchmark''s US-data noise model: the
    benchmark''s relevance/informativeness labels were constructed on US tweet streams
    where this type of coordinated community fact-checking and large-scale false-rumor
    propagation are not represented. Sources: arXiv 2007.05848 — [WEB-23];
    Springer/PUC published version — [WEB-24];
    PSMag reporting — [WEB-16]'
dimension_priority_summary:
  IO:
    priority: HIGH
    notes: The benchmark's four-category ontology is deeply misaligned with the target
      coverage area. Earthquakes, volcanic events, tropical flooding, and civil unrest
      are absent entirely. Even overlapping categories (storms) carry different regional
      profiles.
  IC:
    priority: HIGH
    notes: All benchmark input content is English-language US/Australian tweets. Mexican
      administrative geography (colonias, alcaldías, municipios) and Spanish-language
      social-media conventions are entirely absent from the benchmark's input content
      and processing pipeline.
  IF:
    priority: LOWER
    notes: Both benchmark and deployment operate on text-only social-media posts.
      No modality mismatch. Linguistic form mismatch (English vs. Spanish) is captured
      under IC and OF.
  OO:
    priority: HIGH
    notes: The relevance/informativeness/non-redundancy label schema was developed
      and validated on US English tweets; transfer validity to Mexican Spanish crisis
      tweets covering different event types is unestablished.
  OC:
    priority: HIGH
    notes: Reference summaries were authored by Anglophone MTurk workers using US
      news conventions. No journalists, no Spanish speakers, and no individuals with
      Latin American crisis knowledge contributed to ground truth.
  OF:
    priority: HIGH
    notes: The benchmark provides no Spanish-language summarization evaluation whatsoever.
      Bilingual output is a core deployment requirement. The entire Spanish evaluation
      dimension is a gap.
flagged_investigation_items:
- item_id: 1
  topic: Spanish-language crisis tweet corpora for Mexico and Central America
  search_target: TREC-IS Spanish subsets; CrisisNLP Spanish data; CLEF-HIPE; IULA
    crisis corpus; any Mexico- or Central America–specific crisis tweet datasets;
    assess geographic and temporal coverage
  search_outcome: SEARCHED — CONFIRMED GAP. No Spanish-language crisis tweet corpus
    anchored to Mexican or Central American events exists for timeline extraction
    or summarization. HumAID (English-only) includes a 2017 Mexico earthquake subset.
    TREC-IS has a guatemalaEarthquake2012 entry (English). A Spanish NER/geolocation
    model for Mexican earthquake tweets exists (Curiel et al., PMC 2019) but is not
    a summarization dataset. See social_media_context.spanish_twitter_crisis_corpora.known_resources
    for full detail.
- item_id: 2
  topic: Crisis NLP benchmarks covering earthquakes, volcanic activity, tropical flooding,
    civil unrest in Spanish
  search_target: Crisis NLP benchmark earthquake volcanic flooding civil unrest Spanish
    Latin America Twitter dataset
  search_outcome: SEARCHED — CONFIRMED GAP. No Spanish-language crisis NLP benchmark
    covering these event types for Latin America was identified. The CrisisNLP/HumAID
    ecosystem is English-only. No volcanic activity or civil-unrest NLP dataset in
    Spanish was found across CrisisNLP, TREC-IS, or academic repositories.
- item_id: 3
  topic: NER and geo-resolution tools for Mexican administrative geography
  search_target: Mexican administrative geography NER benchmark colonias municipios
    alcaldías delegaciones georesolution Spanish NLP gazetteer
  search_outcome: 'SEARCHED — PARTIAL. Curiel et al. (PMC 2019) built a Spanish NER
    + KDE geolocation pipeline for Mexican earthquake tweets using CoNLL-2002 Spanish
    + manually annotated CDMX earthquake tweets. This is the only identified proof-of-concept.
    No published benchmark covering colonia/alcaldía-level Mexican gazetteer resolution
    was found. Source: [WEB-4]'
- item_id: 4
  topic: Bilingual or Spanish-language crisis summarization evaluation frameworks
  search_target: Bilingual crisis summarization evaluation English Spanish benchmark
    AP Español multilingual ROUGE BERTScore
  search_outcome: 'SEARCHED — RESOLVED (general) / CONFIRMED GAP (crisis-specific).
    No Spanish-language crisis summarization evaluation framework exists. General
    Spanish summarization evaluation guidance: BERTScore-precision with multilingual
    models outperforms ROUGE for Spanish; LLM-as-judge approaches show promise. A
    2025 study (arXiv 2503.17039) provides the most current Spanish summarization
    metric evaluation. See evaluation_framework_implications.bilingual_rouge_notes.'
- item_id: 5
  topic: AP Español and Latin American crisis journalism style guidelines
  search_target: AP Español crisis journalism guidelines Mexico Latin America casualty
    framing attribution community impact language
  search_outcome: NOT SEARCHED within current budget — deferred. AP Español guidelines
    are a proprietary commercial product; specific operationalizable criteria are
    unlikely to be findable via open web search. Requires expert elicitation or institutional
    access.
- item_id: 6
  topic: Mexican and Central American emergency management agency Twitter ecosystems
  search_target: CENAPRED CONRED COPECO SMN Protección Civil Twitter social media
    crisis communication Mexico Central America
  search_outcome: SEARCHED — RESOLVED. Key accounts and institutional structure confirmed.
    See regulatory_and_institutional_context.emergency_management_agencies and social_media_context.mexican_spanish_twitter_conventions.official_account_ecosystem
    for full detail.
- item_id: 7
  topic: Indigenous-language place name frequency in Mexican and Guatemalan crisis
    tweets
  search_target: Mexican Spanish Twitter Nahuatl Zapotec Maya place names crisis NLP
    code-switching indigenous toponymy
  search_outcome: NOT SEARCHED within current budget — deferred. This is likely unsearchable
    via web search; frequency in crisis-specific tweets requires corpus analysis.
    Flagged for expert elicitation.
- item_id: 8
  topic: Misinformation patterns in Mexican crisis Twitter (especially post-earthquake)
  search_target: Mexico earthquake Twitter misinformation 2017 2022 crisis social
    media false rumors NLP detection
  search_outcome: 'SEARCHED — RESOLVED. See cultural_and_editorial_norms.misinformation_dynamics
    for full detail. Key finding: documented large-scale, coordinated misinformation
    ecosystem in #19S earthquake with citizen-organized fact-checking networks — fundamentally
    different from benchmark''s US noise model.'
- item_id: 9
  topic: SASMEX seismic alert system and associated Twitter cascade patterns
  search_target: SASMEX Mexico City seismic alert Twitter response pattern sismo hashtag
    crisis tweet cascade
  search_outcome: 'SEARCHED — RESOLVED. See cultural_and_editorial_norms.seismic_alert_system_context
    and social_media_context.mexican_spanish_twitter_conventions.common_crisis_hashtags
    for full detail. Key hashtags: #TenemosSismo (all events), #AlertaSismica (serious
    warnings). System reaches ~25 million people.'
- item_id: 10
  topic: Popocatépetl volcanic alert vocabulary and Twitter conventions
  search_target: Popocatépetl CENAPRED semáforo volcánico Twitter social media alert
    vocabulary Spanish
  search_outcome: 'SEARCHED — RESOLVED. See cultural_and_editorial_norms.volcanic_alert_level_vocabulary
    for the full seven-phase vocabulary (Verde F1–2, Amarillo F1–3, Rojo F1–2) with
    Spanish-language hazard terminology. Current status (May 2026): Amarillo Fase
    2.'
net_new_fields:
  humaid_mexico_earthquake_subset: 'The HumAID dataset (ICWSM 2021, CrisisNLP/QCRI)
    includes a 2017 Mexico earthquake subset: ~361,040 total tweets collected Sept
    20–23 2017, with 2,563 manually labeled tweets across humanitarian categories
    (infrastructure damage, requests, donations, etc.). Critically, HumAID is English-only
    — the labeled Mexico earthquake tweets are English-language tweets about the event,
    not Spanish-language tweets from Mexican users. This means even the closest existing
    crisis NLP resource for a Mexican earthquake event does not address the Spanish-language
    gap. Source: HumAID paper (ICWSM 2021) — [WEB-3];
    dataset statistics table — [WEB-25]'
  verified19s_citizen_journalism_model: 'The #19S earthquake response produced a documented
    ''Verificado19S'' citizen journalism ecosystem: crowds used Twitter, Facebook,
    Slack, and GitHub to create a ground-truth verification infrastructure for crisis
    information, with journalists engaging earlier than non-journalists in both spreading
    and correcting false rumors. This multi-platform coordination model (documented
    across 2.9M tweets + additional platforms over one month) represents a locally
    specific social-media crisis information architecture that has no analog in the
    benchmark''s US-context annotation framework. Any timeline-extraction relevance
    model applied to Mexican earthquake events must account for this verification-tweet
    genre as a high-informativeness category. Source: Flores-Saviaga & Savage, arXiv
    2007.05848 — [WEB-23]'
  spanish_summarization_metric_recommendation: 'A 2025 study (arXiv 2503.17039) specifically
    evaluating summarization metrics for Spanish found that BERTScore-precision correlates
    strongly (ρ > 0.6) with human coherence and relevance judgments for Spanish, while
    most standard ROUGE variants perform poorly. LLM-as-judge approaches also show
    strong correlation for 5W1H coverage in Spanish. This provides a concrete metric
    recommendation for constructing a Spanish-language evaluation supplement to the
    benchmark''s ROUGE-based framework. Source: arXiv 2503.17039 — [WEB-17]'
  popocatepetl_population_exposure: 'Within a 100km radius of the Popocatépetl crater
    live approximately 25 million people, making it one of the most densely populated
    volcanic risk zones globally. The volcano is currently (as of April/May 2026)
    at Amarillo Fase 2 with ongoing daily exhalations (e.g., 167 exhalaciones on April
    28, 2026). This persistent low-level activity means Popocatépetl-related crisis
    tweets are a near-continuous presence in the target deployment''s tweet stream,
    not just spike events — a structural difference from the benchmark''s event-triggered
    collection model. Sources: Milenio semáforo explainer — [WEB-21];
    Infobae April 2026 monitoring report — [WEB-26]'
  sasmex_twitter_seed_vocabulary: 'For any earthquake timeline extraction system applied
    to CDMX crisis events, the SASMEX/CIRES X account (@SASMEX) provides standardized
    seed-tweet vocabulary: #TenemosSismo for all detections, #AlertaSismica for serious
    warnings, with structured content including timestamp, sensor location (estado/coast),
    and affected cities. This standardized format creates a distinctive, machine-readable
    seed-tweet type with no analog in the benchmark''s US data. The SSN (@SismologicoMX)
    provides magnitude/depth data as follow-up tweets. Sources: SASMEX Wikipedia —
    [WEB-7]; SASMEX X sample
    posts — [WEB-8]'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://en.wikipedia.org/wiki/CENAPRED |
| WEB-2 | https://mx.usembassy.gov/natural-disaster-alert-u-s-embassy-mexico-city/ |
| WEB-3 | https://crisisnlp.qcri.org/humaid_dataset.html |
| WEB-4 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6484392/ |
| WEB-5 | https://www.gob.mx/cenapred |
| WEB-6 | https://github.com/wangcongcong123/crisis_nlp_progress/blob/master/datasets/TREC-IS.md |
| WEB-7 | https://en.wikipedia.org/wiki/Mexican_Seismic_Alert_System |
| WEB-8 | https://x.com/sasmex |
| WEB-9 | https://medium.com/hci-wvu/countering-fake-news-in-natural-disasters-using-bots-and-citizen-crowds-412bbef6b489 |
| WEB-10 | https://x.com/cnpc_mx |
| WEB-11 | https://es.wikipedia.org/wiki/Centro_Nacional_de_Prevenci%C3%B3n_de_Desastres |
| WEB-12 | https://whndn.org/portfolio-item/disaster-response-services-tools/ |
| WEB-13 | http://data.proteccioncivil.cdmx.gob.mx/Monitoreo-popo.html |
| WEB-14 | https://www.worlddata.info/america/mexico/telecommunication.php |
| WEB-15 | https://datahub.itu.int/data/?e=1&i=11624 |
| WEB-16 | https://psmag.com/social-justice/how-mexico-city-residents-used-social-media-to-debunk-fact-from-fiction/ |
| WEB-17 | https://arxiv.org/pdf/2503.17039 |
| WEB-18 | https://aclanthology.org/2024.emnlp-main.1085.pdf |
| WEB-19 | https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2022.827236/full |
| WEB-20 | https://www.cenapred.unam.mx/reportesVolcanesMX/ |
| WEB-21 | https://www.milenio.com/estados/que-es-el-semaforo-de-alerta-volcanica-y-como-funciona |
| WEB-22 | https://cnnespanol.cnn.com/2024/03/15/volcan-popocatepetl-alerta-amarilla-riesgos-orix |
| WEB-23 | https://arxiv.org/abs/2007.05848 |
| WEB-24 | https://link.springer.com/article/10.1007/s00779-020-01411-5 |
| WEB-25 | https://mimran.me/papers/HumAID_Human_Annotated_Disaster_Incidents_Data_from_Twitter_ICWSM21.pdf |
| WEB-26 | https://www.infobae.com/mexico/2026/04/29/popocatepetl-tuvo-167-emisiones-este-28-de-abril/ |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark covers four US-derived crisis categories: wildfires, local fires, traffic incidents, and storms. Are there crisis types relevant to your journalists' coverage area that fall outside these four, and do shared categories like storms differ meaningfully in their regional sub-types?
A1: Yes, important crisis types are missing — including volcanic activity (e.g., Popocatépetl), earthquakes, flooding from tropical systems, and civil unrest. Within shared categories like storms, the context and damage patterns differ substantially from US norms, even if the event type label is nominally the same.

Q2 [IC]: The benchmark anchors crisis events to US-specific named locations. How place-specific does the system need to be for Mexican and Central American events, particularly regarding administrative subdivisions and regional landmarks?
A2: Correct geographic identification is a core requirement. The system must accurately identify and contextualize location references (colonias, municipios, delegaciones, regional landmarks) appearing in Spanish-language social media, and must aggregate and group information around those location- and time-anchored event contexts.

Q3 [OC]: The benchmark's reference summaries were written by US English annotators. Do your journalists follow a distinct editorial style, and would their standard for a "good" crisis summary diverge from US news writing conventions?
A3: Yes, editorial style and relevance judgments differ by user profile. Journalists follow outlet-specific or wire-service guidelines (e.g., AP Español), which diverge from US norms in source attribution, casualty framing, and community impact language. However, the preferred model behavior is to produce less restrictive, broader summaries that journalists can then adapt — rather than summaries already shaped by a specific editorial convention.

Q4 [OF]: Does the deployment require bilingual output (English and Spanish), and if so, what register of Spanish is needed?
A4: Bilingual output is required. English summaries are expected to be higher quality and more directly usable; Spanish summaries will need journalist revision for register and format. Neutral Latin American Spanish would be acceptable as a baseline, with journalists performing the final adaptation to Mexican journalistic register.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark's four US-centric crisis categories miss structurally important event types (earthquakes, volcanic activity, tropical flooding, civil unrest) that are core to the target coverage area, and even shared categories carry different damage and context profiles. |
| IC | HIGH | The benchmark's location-anchored, US English tweet content will not represent the place names, administrative units, or Spanish-language social-media conventions that the system must handle correctly in the target deployment context. |
| IF | LOWER | Both deployment and benchmark operate on text-only social-media posts in a high-resource language pair; no modality mismatch is present. |
| OO | HIGH | The benchmark's output taxonomy and scoring were designed around US crisis events; the classification of what constitutes a relevant timeline update may not transfer to Mexican/Central American event structures or Spanish-language tweet conventions. |
| OC | HIGH | Reference summaries were authored by US English annotators using US news conventions; the user confirmed that journalistic relevance judgments, attribution norms, and summary scope differ by editorial profile, creating a direct ground-truth mismatch for the target population. |
| OF | HIGH | The benchmark produces English-only free-form summaries, but deployment requires bilingual output; Spanish-language summarization quality and register appropriateness are not assessed by the benchmark at all. |

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
  "benchmark": "crisisltlsum",
  "region": "Mexico City and Central America Bilingual Crisis Journalism",
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
