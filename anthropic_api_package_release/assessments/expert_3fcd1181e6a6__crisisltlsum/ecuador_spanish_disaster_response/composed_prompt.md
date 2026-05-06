I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **CrisisLTLSum: A Benchmark for Local Crisis Event Timeline Extraction and Summarization** is valid for use in **Ecuador — Humanitarian Crisis Social Media Analysts**.

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
- **Domain**: Crisis event timeline extraction and summarization from social media
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2023

### Benchmark Documentation

## Key characteristics relevant to validity analysis:

### Input Ontology
CrisisLTLSum is organized around two primary task types — timeline extraction and timeline
summarization — applied to four crisis event domains: wildfire, local fire, traffic, and
storm [Q1, Q4, Q53, Q122]. The extraction task is framed as binary classification of
whether a given tweet is relevant, informative, and non-redundant relative to a seed tweet
describing an ongoing local event [Q5, Q83]. The summarization task requires abstractive
generation of a narrative capturing event progression [Q6, Q84]. The benchmark explicitly
restricts its scope to *local* crisis events — incidents bound to a specific location
(building, street, county) of short duration [Q12] — and the online clustering step is
designed to mimic a real-time sequential scenario [Q38] where each cluster represents
events as granular as "a fire in building A" or "a wildfire in a specific area" [Q40].

The four-domain taxonomy is a critical structural constraint. The authors confirm the
benchmark covers exactly these four categories [Q122], and the selection logic
explicitly excludes any large-scale geophysical or humanitarian emergency types [Q124].
No volcanic eruption sequences, mass displacement events, landslides, coastal floods,
or complex humanitarian emergencies are represented. The benchmark's claim to novelty
rests partly on covering "a thousand timelines compared to only tens of events covered
by each of the existing datasets" [Q22], but this scale applies within the four-domain
taxonomy only, not across disaster types. The timeline summarization task was the first
proposed for this domain on Twitter [Q20], meaning no alternative domain-comparative
baseline exists in the literature at time of publication.

### Input Content
All source data was collected from seven US states (New York, Illinois, Massachusetts,
California, Texas, Florida) and two Australian states (New South Wales, Victoria)
during 2020–2021 [Q123]. Geographic areas were selected because they are "subject to
the most events falling into our crisis domains of interest" [Q124] — California,
Victoria, and New South Wales for wildfires; Texas and Florida for wildfires and storms;
Massachusetts, Illinois, and New York for weather, traffic, and local fires. All
geographic and institutional content in the dataset reflects US and Australian crisis
contexts. Tweet filtering relies on a list of location candidates assembled from cities,
towns, and "famous neighborhoods" in the areas of interest [Q30], and on domain-specific
keyword lists curated using "expert knowledge gathered through over-viewing crisis
stories in news, social media, and related big disaster events of the past" [Q126].
These keyword lists are explicitly described as "generic for each category and not
specific to unique events" [Q127] and as "not comprehensive or exhaustive but somewhat
representative of each crisis domain" [Q31].

The 1,000 final clusters were manually selected by the authors — not external annotators
— with authors specifying the seed tweet for each [Q52]. The resulting dataset contains
10,610 tweets [Q69] drawn entirely from this US/Australian geographic frame. No
Spanish-language, Latin American, indigenous-language, or humanitarian-organizational
content is present or documented.

### Input Form
The benchmark is text-based and English-language throughout. Input preprocessing
applies English-specific operations: lemmatization, lowercasing, and keyword matching
against English-language crisis vocabulary [Q129, Q130]. The named entity recognition
pipeline uses a pre-trained AllenNLP model trained on CoNLL03 [Q33] — an English NLP
benchmark — and a BERT-based NER model fine-tuned on English Twitter data [Q35].
Location augmentation uses the OpenStreetMap API to map mentions to physical addresses
[Q36], relying on the ability to match English place-name mentions in US and Australian
geography. Fuzzy string matching for duplicate removal [Q136] and cluster similarity
metrics incorporating shared hashtags [Q41] are calibrated to English-language Twitter
conventions.

Input tweet sequences are constructed by concatenating timeline tweets as text strings
[Q85], with BERT fine-tuned on sequences up to 512 tokens [Q86, Q141] and BART on
sequences up to 512 target tokens [Q143]. No audio, image, or multimodal input is
represented. No documentation exists of any adaptation for non-English scripts, informal
register variation, or code-switching. The authors explicitly flag that "replicating the
same process for other language or based on other locations may be hard because of such
dependencies" [Q119], directly acknowledging the language-specificity of the entire
preprocessing pipeline.

### Output Ontology
For timeline extraction, the output is a binary label: a tweet either is or is not part
of the timeline, determined by three conjunctive criteria — relevant (same event as seed),
informative (provides facts, not personal opinions only), and not repetitive (adds new
information) [Q58]. The label distribution is 41% positive / 59% negative [Q71]. The
definition of "informative" — specifically the distinction between "facts about the event"
and "personal points of view" [Q58] — embeds an operational relevance criterion reflecting
US annotator norms about what counts as crisis-relevant information.

For timeline summarization, the output ontology is structured around a four-axis human
evaluation rubric: Coherence, Accuracy, Coverage, and Overall quality, each scored 1–5
[Q106, Q151]. The Coherence rubric explicitly references English grammar and English-
language comprehensibility as the evaluation target [Q153]. The Accuracy axis assesses
whether summaries "accurately match" timeline information without making things up or
being misleading [Q155]. The Coverage axis asks whether "important information" from the
timeline is represented in the summary [Q157]. These criteria are defined in English for
English-language summaries and contain no documentation of how "importance" or
"coherence" were operationalized for non-English, non-US deployment contexts.

### Output Content
Ground-truth extraction labels were determined by majority vote among three MTurk workers
per timeline [Q70]. The annotation setup explicitly restricted workers to "countries where
native English speakers are most likely to be found" [Q61], ensuring the entire label
set reflects the operational intuitions of English-language, likely US-context annotators.
Workers passed a qualification test checked against expert labels [Q62, Q64], with ongoing
quality monitoring [Q66], yielding an average inter-annotator agreement of 90.06% between
the two most-agreeing workers per timeline [Q77] and 91.77% against expert annotations
on 20% of timelines [Q79].

For summarization evaluation, a separate MTurk worker group rated eight summaries per
timeline under the same location restriction (QC1) [Q105, Q106]. The two human-written
summaries used as references for ROUGE scoring were selected as those written by the two
workers with the highest extraction-label agreement [Q87, Q88]. No Spanish-speaking,
Latin American, indigenous-language-fluent, or humanitarian-practitioner annotators
participated at any stage of label production or quality evaluation. The authors do not
document any cross-cultural validation of their labels or summaries.

### Output Form
Timeline extraction is evaluated using average timeline-level accuracy [Q91], with human
performance at 88.98 and the best model at 73.51 — a gap the authors characterize as
highlighting task difficulty [Q96, Q97]. Timeline summarization is evaluated with ROUGE
(via SacreROUGE in a multi-reference setting against the two most-agreeing worker
summaries [Q98, Q99, Q100]) and a five-worker human evaluation on four axes [Q103, Q106].
Model baselines span oracle (gold extraction labels) and pipeline (predicted labels)
settings [Q101]. Human-written summaries substantially outperform model outputs, with an
average overall quality rating of 4.12 [Q108].

The output modality is text-based throughout — binary classification labels and abstractive
text summaries. ROUGE is applied as an English n-gram overlap metric against English
reference summaries [Q98]. The human evaluation rubric is defined and administered in
English [Q153–Q160]. No documentation exists of how ROUGE or the human rubric would be
adapted for Spanish-language summaries, non-English reference texts, or the operational
reporting conventions of humanitarian organizations. The benchmark does not penalize or
evaluate language mismatch between input and output.


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
| Q9 | 1 | input_content | "Hossein Rajaby Faghihi, Bashar Alhafni, Ke Zhang, Shihao Ran, Joel Tetreault, Alejandro Jaimes" |
| Q10 | 1 | input_content | "Michigan State University, New York University Abu Dhabi, Dataminr, Inc." |
| Q11 | 2 | input_ontology | "To the best of our knowledge, this is the first annotated dataset for such an extraction task, while this problem has been tackled before in unsupervised settings (Zhang et al., 2018)." |
| Q12 | 2 | input_ontology | "Moreover, we focus on the extraction of local crisis events. The term "local" indicates that an event is bound to an exact location, such as a building, a street, or a county, and usually lasts for a short period." |
| Q13 | 2 | input_content | "Building a corpus of local crisis events is particularly useful for first responders but also challenging because the timelines of these events are often not captured in existing knowledge sources." |
| Q14 | 2 | input_content | "This means one has to design mechanisms for automatically detecting and tracking events directly from the Twitter stream, which is especially hard for existing clustering methods (Guille and Favre, 2015; Asgari-Chenaghlu et al., 2021) given the low number of available tweets for each local event." |
| Q15 | 2 | input_form | "First, the process of identifying and extracting relevant updates for a specific event has to contend with the large volume of noise (Alam et al., 2021a) and informal tone (Rudra et al., 2018) compared to other domains such as news." |
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
| Q30 | 3 | input_form | "The location filtering relies on a list of location candidates created by gathering cities, towns, and famous neighborhoods in a big area of interest. A tweet is considered relevant to our area of interest if 1) the text mentions one of the candidates, 2) the geo-tag matches the area of interest, or 3) the user location matches the area of interest." |
| Q31 | 3 | input_content | "To limit the tweets to a specified crisis domain, we curate domain-specific keywords and only select tweets with phrases matching one of the keywords. This approach is not comprehensive or exhaustive but somewhat representative of each crisis domain." |
| Q32 | 3 | input_content | "The combinations of (area a, domain d, time t) are manually selected so that the events of type d at location a are more frequent during time period t." |
| Q33 | 3 | input_form | "We use three different modules. First, we use a pre-trained neural model from AllenNLP (Gardner et al., 2018), trained on CoNLL03 (Tjong Kim Sang and De Meulder, 2003), to extract entities with types of people, location, and organization." |
| Q34 | 3 | input_form | "Although this module extracts some important entities in the text, it fails to extract uncommon entities or special mentions" |
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
| Q50 | 4 | input_form | "First, we manually merge pairs of clusters with a cluster head similarity higher than a threshold headmin." |
| Q51 | 4 | input_form | "This step compensates for some of the errors from missing entities in the pre-processing step, which affects the intermediate similarity scores in the clustering algorithm." |
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
| Q75 | 6 | input_form | "We notice an interesting trend across the domains: the longer the timeline, the lower the average percentage of tweets to be part of the timeline." |
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
| Q102 | 8 | output_form | "In the oracle setting, we use the gold labels in the DEV set to identify tweets that are part of each timeline to the summarization models." |
| Q103 | 8 | output_form | "We further conducted a human evaluation to better assess the quality of the summaries." |
| Q104 | 8 | output_form | "We take the whole TEST set and we evaluate eight summaries per timeline: 1) the three human-written summaries; 2) three model-generated summaries using the three models we develop for timeline summarization in the oracle setting; 3) two summaries from random systems: a random tweet that is part of the timeline, and a summary from a randomly selected timeline that belongs to a different crisis domain." |
| Q105 | 8 | output_content | "Following a similar process in 3.2, we recruit a group of workers from MTurk with the same Location restriction (QC1), who can pass our pilot study as a qualification test." |
| Q106 | 8 | output_content | "Each summary was evaluated by five different workers on a scale from 1 to 5 across four axes: Coherence, Accuracy, Coverage, and Overall quality, as was done by Lai et al. (2022)." |
| Q107 | 8 | output_content | "Detailed instructions and annotation workflows are presented as Figures 15–21 in Appendix E." |
| Q108 | 8 | output_form | "Looking at the results over all the timelines, the human-written summaries are significantly better than the ones generated by models, in terms of overall quality with an average rating of 4.12." |
| Q109 | 9 | input_content | "We presented CrisisLTLSum, the first dataset on local crisis timelines extracted from Twitter and the first to provide human-written summaries on information extracted from Twitter." |
| Q110 | 9 | input_ontology | "We showed that CrisisLTLSum supports two downstream tasks: Timeline Extraction and Timeline Summarization." |
| Q111 | 9 | output_form | "Our experiments with SOTA baselines indicate that both of these tasks are challenging and encourage future research." |
| Q112 | 9 | input_ontology | "Our dataset further provides a resource for developing methods on utilizing microblogs toward aiding first-responders in evaluating ongoing crisis events." |
| Q113 | 9 | output_form | "For timeline extraction, 66 timelines (77%) have at least one error, in which 272 out of 958 tweets (28%) are wrong." |
| Q114 | 9 | output_form | "We observe that the model performance decreases with increasing timeline length for both timeline extraction and summarization tasks, with significant drops in accuracy and ROUGE scores when timelines get longer." |
| Q115 | 9 | output_form | "Most of the summarization errors were due to hallucinations or to copying specific sentences that are present in the timeline without covering all the important event details described in the timeline." |
| Q116 | 10 | input_content | "We thank Aoife Cahill for providing detailed feedback on this paper, Alison Smith-Renner and Wenjuan Zhang for helpful discussions on MTurk annotations, our colleagues at Dataminr, and the EMNLP reviewers for their helpful and constructive comments." |
| Q117 | 10 | input_content | "This study has some limitations on the dataset generation workflow. First, our noisy timeline collection process is not a comprehensive and exhaustive extraction to find all available information about a local crisis event. Here, our focus is to provide a representative dataset rather performing a comprehensive set containing all the local crisis events and their updates." |
| Q118 | 10 | input_form | "Second, the proposed noisy timeline collection pipeline is highly dependent to the performance of the entity extraction modules, especially for the location extraction, and the accuracy of the OpenStreetMap API to find the correct physical address of each location mention." |
| Q119 | 10 | input_form | "Accordingly, replicating the same process for other language or based on other locations may be hard because of such dependencies." |
| Q120 | 10 | output_form | "Furthermore, the online clustering method used in this paper has a set of hyperparameters which are tuned heuristically from a small set of experiments. More comprehensive and large scale experiments on tuning those parameters could potentially impact the quality of the generated timelines." |
| Q121 | 10 | input_content | "Generating similar results by following our noisy timeline collection process is in general limited by the users' access to the public Twitter stream and the changes in the available posts (they may become restricted or deleted)." |
| Q122 | 12 | input_ontology | "We build CrisisLTLSum by limiting the search to four crisis domains: wildfire, local fire, traffic, and storm." |
| Q123 | 12 | input_content | "We collect CrisisLTLSum across seven states in the USA and two states of Australia during 2020 and 2021. The selected states in the USA are New York, Illinois, Massachusetts, California, Texas, and Florida. From Australia, we have selected the states of New South Wales and Victoria." |
| Q124 | 13 | input_content | "These states are selected as they are some of the areas subject to the most events falling into our crisis domains of interest. California, Victoria, and New South Wales are mainly selected due to the abundance of wildfires in hot seasons. Texas and Florida have been selected as they are both subject to wildfires and storm events during different months. Massachusetts and Illinois are selected first because those areas are frequently subjected to bad weather, and second as they contain big cities subject to traffic and local fire events alongside New York." |
| Q125 | 13 | input_form | "This step selects the subset of filtered tweets related to a specific crisis category of interest. Ideally, this task can be performed by a neural model trained on a large set of tweets with labeled data indicating the categories. However, as such a large amount of labeled data is unavailable, we rely on a common approach of designing keywords." |
| Q126 | 13 | input_content | "We carefully curate a keyword list for each of our categories of interest by employing expert knowledge gathered through over-viewing crisis stories in news, social media, and related big disaster events of the past." |
| Q127 | 13 | input_content | "Please note that these lists are generic for each category and not specific to unique events. For instance, instead of defining keywords specific to an event called "Hurricane Ida", our keywords list includes phrases such as "fallen tree", "building collapse", or "storm"." |
| Q128 | 13 | input_form | "The quality of the keywords list is crucial to the final quality of the generated timelines, and we polish this list multiple times based on small sets of experiments before using them for the final task." |
| Q129 | 13 | input_form | "To avoid making a long list of keywords and ensure that different lexical formats of the same word are still considered in the keyword matching process, we maintain both a lower-cased and a lemittized version of the keywords and the tweet's text." |
| Q130 | 13 | input_form | "If any of the keywords exist in the text and in any of these formats, then the tweet is considered related to the category." |
| Q131 | 13 | input_form | "The multi-word keywords are not considered n-grams but as an indication that all the words in the keyword should exist in the text, even if not as a sequence." |
| Q132 | 13 | input_content | "This approach will not be comprehensive or exhaustive but rather representative of each crisis domain. Improving this method to be more encompassing is an area for future research." |
| Q133 | 13 | input_form | "We use the following parameters shared among all different domains: shashtag is set to 0.2 and sdist is 0.3. The simthreshold and timethreshold are set to 0.7 and 15 hours respectively. The timethreshold is reduced to 3 hours to avoid merging various accidents at different times but in the same location. The mindist and maxdist are set to 0.4 kilometer and 4 kilometer for fire and traffic events while having the larger range of 0.4 and 10 kilometers for the wildfire and storm extraction. The expirationthreshold is set to 15 hours and tweetthreshold is 4." |
| Q134 | 13 | input_content | "The online clustering approach may fail to properly relate some tweets due to missing entities, clustering method hyper-parameters, or the difference in the description of various angles of the same story." |
| Q135 | 13 | output_content | "To address this, we merge clusters by comparing all cluster heads with each other and combining those with a higher similarity score than a threshold shead. Additionally, we use human feedback to merge clusters where their similarity score is below shead but higher than a second hyper parameter s min head." |
| Q136 | 13 | input_form | "Here, the goal is to remove tweets from the same cluster with identical or similar text. The duplicate removal relies on a fuzzy string sequence-matching technique to compute the similarity between a pair of tweets. We simply go over each tweet sorted in chronological order and remove the ones that match any of the previous tweets in the same cluster with a matching score higher than dmatch." |
| Q137 | 13 | input_form | "Although the keyword filtering step would reduce the number of tweets unrelated to the category of interest, this step aims to further remove the unrelated clusters generated from the pipeline." |
| Q138 | 14 | input_content | "Our goal is to select 1000 clusters that contain enough tweets describing an evolving crisis event." |
| Q139 | 14 | input_form | "In particular, we first identify a "seed tweet" as the first observed post mentioning a local crisis event, then roughly check whether the following tweets in the cluster contain updates about the same event." |
| Q140 | 14 | input_ontology | "We select clusters across four crisis domains, including wildfire, fire, storm, and traffic, depending on how frequently each type of event happens in extracted noisy clusters." |
| Q141 | 14 | input_form | "We fine-tune BERT base uncased on a single GPU for 10 epochs with a learning rate of 5e-5, batch size of 32, a seed of 42, and a maximum sequence length of 512." |
| Q142 | 14 | input_form | "The GRU has one layer with a hidden size of 128. The model was trained for 50 epochs with early stopping after five epochs if the performance did not improve on the DEV set. We use a learning rate of 5e-5, a batch size of 16, and a seed of 42." |
| Q143 | 14 | input_form | "We fine-tune BART based on a single GPU for ten epochs with a learning rate of 5e-5, batch size of 16, a seed of 42, and a maximum target sequence length of 512." |
| Q144 | 14 | input_form | "During inference, we use beam search with a beam size of 4." |
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
name: Ecuador — Humanitarian Crisis Social Media Analysts
abbreviation: ECU-HumSMA
country: Ecuador
sub_national_scope:
  regions:
  - Costa (coastal region, including Guayas, Manabí, Esmeraldas provinces)
  - Sierra (Andean highlands, including Pichincha, Chimborazo, Cotopaxi, Tungurahua
    provinces)
  - Oriente / Amazonía (including Napo, Pastaza, Morona Santiago, Zamora Chinchipe
    provinces)
  note: Disaster risk profiles, language use, and infrastructure differ substantially
    across these three macro-regions. Coastal provinces face flood and tsunami risk;
    Sierra provinces face volcanic, earthquake, and landslide risk; Amazonian provinces
    face flooding, displacement, and environmental emergency risk with higher indigenous-language
    presence.
deployment_population:
  description: Data and social analysts, field coordinators, and domain experts employed
    by or partnering with international humanitarian organizations (Red Cross / Cruz
    Roja Ecuatoriana, UN OCHA) and NGOs operating in Ecuador. These professionals
    use AI-generated crisis event timelines derived from Ecuadorian Spanish Twitter/social
    media streams to track evolving humanitarian situations. They are fluent in both
    American English and Spanish, may hold advanced degrees, and are operationally
    familiar with inter-agency coordination protocols, humanitarian needs assessments,
    and Ecuador-specific crisis response structures.
  roles:
  - Social media / data analysts (monitoring and classification of social media signals)
  - Field coordinators (ground-truth authority on operational relevance of events)
  - Domain experts (thematic specialists in displacement, WASH, food security, protection)
  - Inter-operational team members serving as joint ground-truth annotators and evaluators
  organizational_context: Red Cross / Cruz Roja Ecuatoriana, UN OCHA Ecuador, and
    partner NGOs operating under inter-agency coordination frameworks (e.g., Cluster
    system). Analysts may be international staff (Spanish/English bilingual) or locally-hired
    Ecuadorian nationals.
languages:
  primary_working:
  - Ecuadorian Spanish (predominant language of the tweet stream being analyzed)
  - American English (primary professional and reporting language of analysts)
  tweet_stream_characteristics:
    dominant: Ecuadorian Spanish — informal and semi-formal registers, crisis-specific
      lexicon
    register_notes: Mix of informal abbreviations, phonetic spelling, hashtag-driven
      discourse, and semi-formal agency announcements. Crisis-specific vocabulary
      includes terms such as 'damnificados', 'albergue', 'colapsado', 'desbordamiento',
      'lahares', 'evacuar', 'cordón de seguridad', 'reubicación'.
    code_switching: Kichwa-Spanish code-switching present, particularly in tweets
      originating from or about Sierra and Amazonian communities. Kichwa toponyms
      (place names) appear even in otherwise all-Spanish tweets. Shuar-Spanish mixing
      may occur in southeastern Amazonian content.
    indigenous_language_entity_names: Kichwa place names are common across Sierra
      and Oriente coverage areas; Shuar toponyms present in Morona Santiago and Zamora
      Chinchipe. These may not be recognized by standard Spanish NLP pipelines.
  analyst_language_profile: Bilingual Spanish-English professionals; may have varying
    familiarity with specific Ecuadorian regional slang or Kichwa vocabulary.
writing_systems:
  scripts:
  - Latin alphabet (Spanish tweets and English analyst outputs)
  - Latin alphabet with Kichwa orthographic conventions (Kichwa toponyms and code-switched
    fragments)
  note: Kichwa has a standardized written orthography established through the intercultural
    bilingual education system. The 2008 constitutional reform recognised Kichwa as
    an official language of intercultural communication and mandated a unified spelling
    system, but changes in Kichwa orthography introduced in 2008 were contested by
    many highland communities, leading to rejection of teaching materials and continued
    spelling variation in practice (Open Book Publishers — [WEB-1]).
    Each of Ecuador's indigenous languages now has its own official alphabet, but
    social media usage is informal and may vary. Non-standard orthography, phonetic
    spelling, and abbreviations are common in crisis tweets.
literacy_and_education:
  analyst_population: University-educated professionals; high literacy in Spanish
    and English. This dimension is not a barrier for the analyst user population.
  tweet_author_population_note: Tweets in the monitored stream originate from a broad
    population including affected community members, local journalists, NGO field
    staff, and government agencies. Literacy rates and register formality vary significantly
    by source.
  national_literacy_rate_ecuador: '94–96% (adult population age 15+). TheGlobalEconomy.com
    reports 94% as of 2022 (World Bank source — [WEB-2]);
    WorldViewData reports 96.3% for 2022 (World Bank — [WEB-3]).
    Youth literacy (ages 15–24) is approximately 99% (2020 estimate — [WEB-4]).
    Caveat: national aggregate; rural and indigenous communities have significantly
    lower rates.'
  rural_indigenous_community_literacy_rate: Literacy rates are lower among indigenous
    peoples than in the general population; indigenous families face elevated poverty
    and school dropout rates (IWGIA Indigenous World 2023 — [WEB-5]).
    A large portion of the indigenous ethnic population remains illiterate, particularly
    in written use of indigenous languages outside schools (Open Book Publishers —
    [WEB-1]). No
    sub-national figure by province is publicly available in a citable aggregate source.
    This field requires expert or stakeholder elicitation for operational precision.
  kichwa_written_literacy_rate: '[NEEDS VERIFICATION — deferred: likely unsearchable
    (lived practice). Available evidence suggests Kichwa written literacy is minimal
    outside formal school settings; sources note that reading and writing of indigenous
    languages outside schools is minimal and that only a small number of indigenous
    speakers can read and write in their native languages (Open Book Publishers —
    [WEB-1]). No
    numeric figure is published in a searchable source.]'
crisis_typology:
  benchmark_crisis_types:
  - Wildfire
  - Local fire
  - Traffic incident
  - Storm
  deployment_priority_crisis_types:
  - type: Volcanic eruption and associated hazards (lahares, ash fall, exclusion zones)
    key_examples: Cotopaxi, Tungurahua, Sangay, Reventador
    benchmark_coverage: absent
  - type: Earthquake and aftershock sequences
    key_examples: Manabí 2016 earthquake sequence and aftermath
    benchmark_coverage: absent
  - type: Landslide and debris flow (movimiento en masa)
    key_examples: Sierra and Oriente rainy-season cascades; La Niña-driven events
    benchmark_coverage: absent
  - type: Coastal and riverine flooding (desbordamiento, inundación)
    key_examples: Guayas basin flooding, Manabí coastal flood events, Oriente river
      overflow
    benchmark_coverage: absent
  - type: Mass displacement and population movement
    key_examples: Displacement from volcanic exclusion zones, conflict-driven displacement
      from Colombian border, Venezuelan migration flows
    benchmark_coverage: absent
  - type: Complex humanitarian emergencies (food insecurity, protection crises, disease
      outbreaks)
    key_examples: COVID-19 response coordination, border emergency situations
    benchmark_coverage: absent
  - type: Tsunami and coastal alert sequences
    key_examples: Pacific coastal risk areas
    benchmark_coverage: absent
  note: The benchmark's four crisis types are almost entirely absent from the operational
    priority list of Ecuadorian humanitarian coordinators. Only storm events have
    partial overlap with Ecuadorian flooding scenarios, but the benchmark's 'storm'
    category reflects North American meteorological contexts, not Andean or coastal
    tropical precipitation events.
geographic_and_institutional_entities:
  administrative_hierarchy:
  - level: Provincia (province)
    count: 24 provinces (Wikipedia Provinces of Ecuador — [WEB-6];
      confirmed by multiple sources including ResearchGate — [WEB-7])
    examples: Pichincha, Guayas, Manabí, Tungurahua, Chimborazo, Napo, Morona Santiago
  - level: Cantón (canton)
    count: Approximately 221–224 cantons. One source reports 221 cantons including
      three unassigned (Storyteller Travel — [WEB-8]);
      a scientific diagram caption cites 224 cantons (ResearchGate 2022 — [WEB-7]).
      A new canton (Sevilla Don Bosco, Morona Santiago) was created in 2024 (Wikipedia
      Cantons of Ecuador — [WEB-9]).
    examples: Quito, Guayaquil, Ambato, Latacunga, Tena, Macas
  - level: Parroquia (parish — urban and rural)
    count: More than 1,500 parroquias (Storyteller Travel — [WEB-8])
    examples: Rural parroquias are the operational unit most relevant for last-mile
      crisis coverage
  key_emergency_institutions:
  - name: SNGR — Secretaría Nacional de Gestión de Riesgos (formerly SGR, renamed
      per Ley Orgánica para la Gestión Integral del Riesgo de Desastres, January 2024)
    role: National disaster risk management authority; issues official alerts and
      situation reports
    social_media_presence: Maintains official website at gestionderiesgos.gob.ec with
      situation reports (SITREP), real-time monitoring reports, and alert levels (confirmed
      active — [WEB-10]). Twitter/X handle presence
      for alert dissemination is documented in operational practice but handle not
      directly verified in this search pass.
    institutional_note: Renamed from SGR to SNGR under Decreto Ejecutivo No. 641 (January
      2023) and formalized by Ley Orgánica para la Gestión Integral del Riesgo de
      Desastres (Registro Oficial No. 488, 30 January 2024 — [WEB-11]).
      Analysts and tweets may still reference 'SGR'; both acronyms should be recognized.
  - name: Cuerpo de Bomberos (provincial and cantonal fire and rescue corps)
    role: First-responder coordination; local fire and rescue operations
    social_media_presence: '[NEEDS VERIFICATION — deferred: below search budget]'
  - name: Cruz Roja Ecuatoriana
    role: Humanitarian response, shelter, emergency health; key inter-agency partner
    social_media_presence: '[NEEDS VERIFICATION — deferred: below search budget]'
  - name: Fuerzas Armadas del Ecuador
    role: Military support to disaster response; logistics and engineering in large-scale
      events
    social_media_presence: '[NEEDS VERIFICATION — deferred: below search budget]'
  - name: Policía Nacional del Ecuador
    role: Security, evacuation enforcement, traffic and crowd control in crisis areas
    social_media_presence: '[NEEDS VERIFICATION — deferred: below search budget]'
  - name: Ministerio de Salud Pública (MSP)
    role: Health emergency coordination, disease surveillance
    social_media_presence: '[NEEDS VERIFICATION — deferred: below search budget]'
  - name: IGEPN — Instituto Geofísico de la Escuela Politécnica Nacional
    role: Volcanic and seismic monitoring authority; issues eruption alerts and technical
      bulletins
    social_media_presence: '[NEEDS VERIFICATION — deferred: below search budget]'
  - name: INAMHI — Instituto Nacional de Meteorología e Hidrología
    role: Weather and hydrological alerts (rainfall, river levels, flood risk)
    social_media_presence: '[NEEDS VERIFICATION — deferred: below search budget]'
  international_humanitarian_actors_in_country:
  - UN OCHA Ecuador
  - UNHCR Ecuador (Venezuelan displacement focus)
  - WFP Ecuador
  - UNICEF Ecuador
  - IOM Ecuador
  - MSF / Médecins Sans Frontières Ecuador
  - '[NEEDS VERIFICATION — deferred: below search budget; confirm current active presence
    and social media handles for key actors]'
  landmark_and_geographic_references_in_crisis_tweets: Tweets will reference local
    landmarks, barrio names, road identifiers (e.g., 'la vía Latacunga-Quito cortada'),
    river names (Río Pastaza, Río Coca), volcano names (Cotopaxi, Tungurahua, Sangay),
    and neighborhood-level identifiers absent from any US/Australian geographic reference
    database.
indigenous_language_context:
  primary_indigenous_languages_in_tweet_stream:
  - language: Kichwa (Quichua ecuatoriano)
    geographic_presence: Sierra (Andean highlands) and Oriente (Amazonia); largest
      indigenous language in Ecuador; also present in some coastal cities through
      labour migration
    speaker_population: 'Approximately 527,333 speakers per INEC 2010 census data
      (Wikipedia Demographics of Ecuador — [WEB-12]);
      IWGIA 2023 cites the Kichwa nationality as comprising 85.87% of Ecuador''s indigenous
      population, accounting for nearly 800,000 individuals (IWGIA Indigenous World
      2023 — [WEB-5]). Note: ethnic
      self-identification and actual speaker population differ; total indigenous population
      is estimated at over 1 million, with highland communities comprising approximately
      68% (IWGIA — [WEB-5]).'
    tweet_stream_relevance: Kichwa toponyms appear in tweets about Sierra and Amazonian
      disasters even when the tweet is predominantly in Spanish. Full Kichwa-language
      tweets are less common but possible from community sources.
    NLP_resource_availability: No dedicated Kichwa pre-trained language model or large
      NLP corpus was identified in this search pass. The 2008 unified Kichwa alphabet
      is contested, adding orthographic variation. An Ecuadorian Spanish NLP corpus
      (first corpus for the country) was developed (IEEE Xplore — [WEB-13])
      but does not cover Kichwa. No Kichwa-specific NER, word embeddings, or transformer
      model was found in the literature. This is a confirmed gap requiring specialist
      elicitation.
  - language: Shuar
    geographic_presence: Southeastern Amazonia (Morona Santiago, Zamora Chinchipe,
      parts of Pastaza)
    speaker_population: Approximately 59,894 speakers per INEC 2010 census (Wikipedia
      Demographics of Ecuador — [WEB-12]);
      constitutes approximately 4.6% of the indigenous population.
    tweet_stream_relevance: Shuar toponyms and occasional Shuar-Spanish code-switching
      in tweets about southeastern Oriente events
    NLP_resource_availability: No Shuar NLP tools or corpora identified. Shuar has
      an official alphabet established through the bilingual education system, but
      written use outside schools is minimal (Open Book Publishers — [WEB-1]).
      Confirmed gap.
  - language: Other Amazonian indigenous languages (Achuar, Waorani, Siona, Secoya,
      Cofán, Zápara, etc.)
    geographic_presence: Various Oriente provinces
    tweet_stream_relevance: Low frequency in tweet stream but toponyms may appear
      in coverage of Oriente disasters
    NLP_resource_availability: No NLP tools identified for any of these languages.
      The Ecuador 2008 Constitution recognises all indigenous languages as official
      in their respective ethnic territories, but written literacy is very recent
      and very limited. Zápara (Zapara) has only 5 elderly speakers remaining (Open
      Book Publishers — [WEB-1]).
      Confirmed gap for all.
  kichwa_toponym_examples: '[NEEDS VERIFICATION — deferred: likely unsearchable as
    a compiled list; requires field expert or indigenous federations (CONAIE, ECUARUNARI)
    for authoritative curation. Representative examples known from general sources:
    Latacunga (La Tacunga), Ambato, Riobamba (Liribamba), Cotopaxi, Tungurahua — many
    Sierra province and canton names are of Kichwa origin but are now fully absorbed
    into standard Spanish administrative usage. Novel community-level Kichwa toponyms
    in high-risk zones require stakeholder elicitation.]'
  code_switching_pattern: Predominantly Kichwa nouns (place names, community names)
    embedded in Spanish syntax; full Kichwa sentences rare in public Twitter stream
    but possible from community-managed accounts or civil society organizations.
  indigenous_community_crisis_relevance: Indigenous communities in Sierra and Oriente
    face elevated exposure to volcanic, seismic, flooding, and environmental crisis
    events. Their social media presence (community radio announcements shared on social
    media, indigenous organization accounts) constitutes operationally critical signal
    that may be underrepresented in any English-trained crisis NLP system.
infrastructure_notes:
  internet_access:
    national_internet_penetration: '77.2% of the population in 2024 (World Bank /
      ITU via TradingEconomics — [WEB-14]).
      A separate estimate puts internet users at approximately 15.4 million as of
      October 2025 (DataReportal Digital 2026: Ecuador — [WEB-15]).'
    urban_rural_gap: 'As of late 2025, 65.4% of Ecuador''s population lived in urban
      centres and 34.6% in rural areas (DataReportal Digital 2026: Ecuador — [WEB-15]).
      Rural and Amazonian communities have significantly lower internet access; specific
      rural-vs-urban internet penetration sub-figures are not published in a single
      citable aggregate for Ecuador.'
    mobile_internet_penetration: As of end 2025, 95.8% of mobile connections in Ecuador
      connect via 3G, 4G, or 5G broadband networks (GSMA Intelligence data via DataReportal
      — [WEB-15]). Total mobile connections
      reached approximately 18.43 million in 2024, roughly 1.0 per person (WorldData.info
      — [WEB-16]).
    dominant_device_type: '[NEEDS VERIFICATION — deferred: below search budget. Available
      evidence indicates smartphone penetration is high nationally (mobile broadband
      at 95.8% of connections), but rural/Oriente-specific device distribution requires
      stakeholder elicitation.]'
  social_media_platform_usage:
    primary_platform_for_crisis_tweets: 'Existing Ecuadorian crisis NLP research (e.g.,
      UrbangEnCy dataset, 2020–2021) used Twitter as the primary data source for Ecuador
      emergency monitoring (ScienceDirect — [WEB-17]).
      Government agencies including SNGR, IGEPN, and municipal offices also use Twitter/X
      for official alerts. Caveat: post-2022 Twitter API changes and platform evolution
      may have shifted dynamics toward Facebook and WhatsApp, particularly for affected-community
      communications; this requires current field verification.'
    government_agency_platforms: 'SNGR (formerly SGR), IGEPN, and municipal emergency
      offices use Twitter/X for official alerts and situation reports (confirmed from
      SNGR website — [WEB-10]). [NEEDS VERIFICATION
      — deferred: specific handle names require direct platform verification]'
    community_and_informal_sources: WhatsApp broadcast groups, Facebook community
      pages, and local radio station social media accounts are often primary sources
      for affected-population information; these may not be captured in a Twitter-only
      stream
  nlp_infrastructure_gaps:
    spanish_crisis_nlp: General Spanish NLP tools exist (Spanish BERT variants, etc.)
      but are not specifically trained on Ecuadorian social media crisis content.
      A system developed at a Ecuadorian university filters Twitter content into four
      categories relevant to Ecuador (volcanic, telluric/seismic, fires, climatological)
      using NLTK (ResearchGate — [WEB-18]),
      but this is a keyword-based prototype, not a validated NLP model.
    ecuadorian_spanish_specificity: A first corpus for Ecuadorian natural language
      words was developed as of 2017 (IEEE Xplore — [WEB-13]).
      The UrbangEnCy dataset (2020–2021) provides over 25,500 Spanish-language emergency/non-emergency
      labeled tweets from Ecuador, covering urban scenarios (ScienceDirect — [WEB-17]).
      This is the only Ecuador-specific Spanish crisis tweet dataset identified. It
      is publicly available at [WEB-19] and covers
      binary emergency classification but not timeline extraction, summarization,
      or humanitarian coordinator relevance criteria.
    kichwa_nlp: No pre-trained Kichwa language model, word embeddings, or annotated
      NLP corpus identified in this search. This is a confirmed documentation gap.
      The language is low-resource with contested orthographic conventions. Stakeholder
      elicitation required.
    ecuador_ner_tools: No NER tool validated on Ecuadorian administrative geography
      (parroquia/cantón level) was identified. A Spanish NER approach for disaster
      tweet toponyms was developed for Mexico City earthquakes using CoNLL-2002 merged
      with manually inspected Spanish tweets (PMC — [WEB-20]),
      offering a methodological template, but not validated on Ecuadorian geography.
    openstreetmap_coverage_quality: '[NEEDS VERIFICATION — deferred: below search
      budget. OpenStreetMap coverage of rural Ecuadorian parroquias, Kichwa community
      names, and informal settlement names has not been specifically assessed in the
      literature identified by this search. Known limitation: benchmark''s OSM-based
      location augmentation was calibrated to US/Australian cities.]'
operational_context_notes:
  analyst_workflow: Analysts consume AI-generated event timelines to track how affected-population
    needs evolve over time, feeding information into situation reports, inter-agency
    dashboards (e.g., ReliefWeb, OCHA HDX), and operational decisions (resource allocation,
    evacuation guidance, needs assessment triggers).
  ground_truth_authority: An inter-operational team combining field coordinators,
    social analysts, and domain experts jointly determines tweet relevance and summary
    quality — not any single role or automated annotator pool. This is structurally
    different from the MTurk crowd-sourcing model used in the benchmark.
  relevance_criteria_for_humanitarian_coordinators:
  - Information about road or bridge access status to affected communities (critical
    for logistics)
  - Informal community broadcasts indicating shelter, water, food, or medical needs
  - Displacement movement indicators (population leaving affected zones, arrival at
    collection points)
  - Institutional coordination signals (agency activation, inter-agency meeting announcements)
  - Casualty and affected population counts (including 'damnificados' counts at parroquia/cantón
    level)
  - Infrastructure damage affecting service delivery (hospital, school, water system)
  - Official alert level changes (e.g., IGEPN volcanic alert color changes, SNGR declarations)
  reporting_language_and_format: Analysts produce operational outputs in English (UN
    OCHA situation reports, Red Cross global reporting) and Spanish (national-level
    coordination with Ecuadorian government counterparts). Summary quality must be
    evaluated in both languages.
  inter_agency_coordination_frameworks: '[NEEDS VERIFICATION — deferred: below search
    budget; confirm current active Cluster system lead agencies and coordination mechanisms
    for Ecuador humanitarian response]'
  annotation_and_evaluation_protocols:
    existing_red_cross_guidelines: '[NEEDS VERIFICATION — deferred: below search budget]'
    existing_un_ocha_guidelines: '[NEEDS VERIFICATION — deferred: below search budget]'
    echo_of_crs_frameworks: '[NEEDS VERIFICATION — deferred: below search budget]'
cultural_norms_notes: '- Ecuadorian crisis communication often involves a mix of official
  agency accounts (SNGR, IGEPN, municipal governments) and informal community-level
  broadcasting, with the latter carrying operationally critical information not available
  through official channels.

  - Affected communities may refer to events using local place names, community identifiers,
  or informal neighborhood names that do not appear in any official geographic database.

  - Indigenous community social media presence (especially Kichwa-speaking Sierra
  communities organized through indigenous federations such as CONAIE or ECUARUNARI)
  may generate crisis signals in Kichwa or bilingual Kichwa-Spanish that standard
  NLP pipelines will not process correctly.

  - Humanitarian response in Ecuador operates through a mixed national-international
  coordination structure; institutional references in tweets will include both Ecuadorian
  government bodies (SNGR, MSP, fuerzas armadas) and international actors (Cruz Roja,
  OCHA, ACNUR/UNHCR).

  - The concept of ''damnificado'' (disaster-affected person with loss of livelihood
  or home) carries specific operational and legal weight in Ecuadorian disaster response
  and appears frequently in both tweet stream and humanitarian reporting.

  - Ecuadorian crisis social media frequently references ''albergues'' (collective
  shelters) as both locations and indicators of displacement scale; these references
  carry high operational salience for humanitarian coordinators.

  '
domain_specific_notes:
  crisis_nlp_benchmark_gap: 'No Spanish-language crisis NLP benchmark covering Ecuadorian
    or Andean disaster types (volcanic eruptions, landslides, displacement) with timeline
    extraction or summarization tasks has been identified. The UrbangEnCy dataset
    (Parraga-Alava et al., 2021) is the closest existing resource: 25,500+ Spanish
    tweets from Ecuador labeled for binary emergency classification, collected January–August
    2020 (ScienceDirect — [WEB-17]).
    It covers urban emergency scenarios broadly but does not include timeline structure,
    summarization annotation, volcanic/geophysical crisis types, or humanitarian coordinator
    relevance criteria. It is referenced in the HumVI multilingual humanitarian dataset
    paper as a known Ecuador-specific resource (arXiv — [WEB-21]).'
  applicable_crisis_nlp_datasets: 'Key existing crisis NLP resources and their Ecuador/Spanish
    relevance:

    1. CrisisNLP / HumAID (QCRI): HumAID includes 19 disaster events (2016–2019) with
    ~77K English-labeled tweets; includes tweets from the 2016 Ecuador Earthquake
    as one event (approximately 1.7M raw tweets, 2K annotated — ResearchGate HumAID
    — [WEB-22]).
    All annotations are in English; covers earthquake type but not timeline structure.
    HumAID also includes a multimodal sub-corpus (CrisisMMD) with Ecuador Earthquake
    2016 images (CrisisNLP — [WEB-23]).

    2. UrbangEnCy (Parraga-Alava et al., 2021): Ecuador-specific Spanish-language
    emergency tweet dataset, 25,500+ texts, binary classification only (ScienceDirect
    — [WEB-17]). Available
    at [WEB-19].

    3. Mexico 2017 Earthquake Spanish NLP: Spanish NER approach merging CoNLL-2002
    with manually annotated Spanish earthquake tweets for toponym extraction (PMC
    — [WEB-20]). Latin American Spanish
    context but not Ecuador-specific.

    4. HumVI (2024): Multilingual humanitarian incident dataset including Spanish;
    covers violent incidents impacting humanitarian aid workers, not natural disaster
    timelines (arXiv — [WEB-21]).

    5. No timeline extraction or abstractive summarization benchmark in Spanish or
    for Ecuador has been identified. This is a confirmed full gap.'
  volcanic_crisis_timeline_specifics: 'Volcanic crises in Ecuador (Cotopaxi, Tungurahua,
    Sangay, Reventador) involve multi-phase sequences: early warning signals, alert
    level escalation (IGEPN color codes), lahar flow advisories, exclusion zone declarations,
    evacuation orders, and shelter/return phases. These temporal structures differ
    from the single-location, short-duration events in the benchmark.'
  humanitarian_information_management:
    relevant_platforms:
    - ReliefWeb
    - OCHA Humanitarian Data Exchange (HDX)
    - OCHA Financial Tracking Service (FTS)
    ecuador_specific_dashboards: '[NEEDS VERIFICATION — deferred: below search budget]'
  evaluation_metric_adaptation:
    rouge_for_spanish: ROUGE computed against Spanish-language reference summaries
      is feasible but requires Spanish-tokenization-aware implementation; multilingual
      BERTScore or other semantic similarity metrics may be more appropriate for evaluating
      Spanish humanitarian summaries against English-trained baselines.
    available_multilingual_metrics: '[NEEDS VERIFICATION — deferred: below search
      budget]'
    humanitarian_reporting_style_norms: UN OCHA situation reports and Red Cross emergency
      appeals follow specific genre conventions (numbered bullet points, standardized
      section headers, use of figures and percentages) that differ from the abstractive
      summary style elicited in the benchmark. Evaluation rubrics should be anchored
      to these conventions for deployment-relevant assessment.
sub_national_variation:
- region: Costa (coastal region)
  key_provinces: Guayas, Manabí, Esmeraldas, Los Ríos, El Oro, Santa Elena
  primary_crisis_types: Coastal flooding, El Niño-driven inundation, earthquake (Manabí
    2016), tsunami risk, tropical storms
  language_notes: Predominantly coastal Ecuadorian Spanish; lower Kichwa presence
    than Sierra/Oriente
  infrastructure_notes: '[NEEDS VERIFICATION — deferred: below search budget; internet
    and mobile coverage in coastal rural areas]'
  key_risk_indicators: '[NEEDS VERIFICATION — deferred: below search budget]'
- region: Sierra (Andean highlands)
  key_provinces: Pichincha, Tungurahua, Chimborazo, Cotopaxi, Azuay, Imbabura, Carchi,
    Loja, Bolívar, Cañar
  primary_crisis_types: Volcanic eruptions, lahares, earthquakes, landslides, cold
    waves (heladas), páramo fires
  language_notes: Significant Kichwa-speaking population; highest frequency of Kichwa
    toponyms and code-switching in tweet stream; indigenous federations (ECUARUNARI,
    CONAIE) maintain active social media presence. Indigenous population is largest
    in the highlands, comprising approximately 68% of Ecuador's total indigenous population
    (IWGIA 2023 — [WEB-5]).
  infrastructure_notes: '[NEEDS VERIFICATION — deferred: below search budget; coverage
    in high-altitude rural communities]'
  key_risk_indicators: '[NEEDS VERIFICATION — deferred: below search budget; current
    volcanic alert levels and risk zones around Cotopaxi, Tungurahua, Sangay]'
- region: Oriente / Amazonía
  key_provinces: Napo, Pastaza, Orellana, Sucumbíos, Morona Santiago, Zamora Chinchipe
  primary_crisis_types: River flooding (desbordamiento), landslides, environmental
    emergencies (oil spills), displacement, disease outbreaks
  language_notes: Kichwa-speaking communities throughout; Shuar in southeastern Morona
    Santiago and Zamora Chinchipe (59,894 speakers per 2010 INEC census — Wikipedia
    Demographics of Ecuador — [WEB-12]);
    Achuar, Waorani, and other Amazonian indigenous languages in specific areas; nine
    of Ecuador's eleven indigenous languages are spoken in the Amazon lowlands (Open
    Book Publishers — [WEB-1]).
    Very low presence in general social media monitoring streams.
  infrastructure_notes: '[NEEDS VERIFICATION — deferred: below search budget; internet
    and mobile coverage in Amazonian communities is severely limited in many areas]'
  key_risk_indicators: '[NEEDS VERIFICATION — deferred: below search budget; current
    displacement situation from Colombian border and Venezuelan migration route]'
- region: Galápagos and Insular region
  notes: Low population; crisis types include volcanic activity (Fernandina, Sierra
    Negra), tourism-related incidents; low relevance to primary humanitarian coordination
    use case
  language_notes: Standard Ecuadorian Spanish; no significant indigenous-language
    presence in tweet stream
  infrastructure_notes: '[NEEDS VERIFICATION — deferred: below search budget]'
regulatory_and_institutional_framework:
  national_disaster_risk_law: 'Ecuador''s primary disaster risk management legal framework
    comprises: (1) Ley de Seguridad Pública y del Estado (State and Public Security
    Law) — the longstanding primary disaster law, analysed by IFRC Disaster Law (IFRC
    — [WEB-24]); (2) Ley Orgánica para
    la Gestión Integral del Riesgo de Desastres — a new comprehensive disaster risk
    management law published in Registro Oficial No. 488, 30 January 2024, which formally
    renamed the SGR as Secretaría Nacional de Gestión de Riesgos (SNGR) and updated
    its mandate (SNGR official resolution — [WEB-11]).
    The 2024 law supersedes key aspects of the earlier Ley de Seguridad Pública for
    disaster management purposes. Tweet streams and analyst documents may reference
    both ''SGR'' and ''SNGR''; both acronyms should be recognized in NLP pipelines.'
  humanitarian_coordination_legal_basis: '[NEEDS VERIFICATION — deferred: below search
    budget; identify Ecuador government agreements with OCHA, Red Cross, and other
    international actors governing information sharing and coordination]'
  data_protection_and_social_media_monitoring: '[NEEDS VERIFICATION — deferred: below
    search budget; identify applicable Ecuadorian data protection regulations governing
    social media monitoring for humanitarian purposes]'
  indigenous_peoples_rights_framework: Ecuador's 2008 Constitution established Spanish
    as the official language while recognising Kichwa and Shuar as official languages
    of intercultural communication, and all other indigenous languages as official
    in their respective ethnic territories. The Constitution mandates State promotion
    of intercultural communication and indigenous-language education (Open Book Publishers
    — [WEB-1]; UNESCO
    LitBase — [WEB-25]).
    This has direct bearing on the legal status of Kichwa and Shuar content in humanitarian
    monitoring applications.
net_new_fields:
  ecuador_specific_crisis_twitter_monitoring_system:
    description: 'A Twitter monitoring system specifically designed for Ecuador was
      developed by Ecuadorian researchers, filtering tweets into four categories matching
      Ecuador''s primary disaster risk profile: volcanic, telluric (seismic), fires,
      and climatological. This keyword-based system (using NLTK) demonstrates that
      Ecuador-specific crisis categorization on Twitter is feasible and needed, but
      constitutes a prototype rather than a validated NLP benchmark.'
    source: ResearchGate — [WEB-18]
    validity_relevance: Confirms that Ecuador's geophysical crisis categories (volcanic,
      telluric) are operationally distinct from the benchmark's four-category taxonomy
      and have been independently identified as requiring dedicated NLP treatment.
  urbangency_dataset:
    description: UrbangEnCy is an Ecuador-specific emergency Twitter dataset of 25,500+
      Spanish-language tweets (January–August 2020) labeled for binary emergency/non-emergency
      classification for urban scenarios. Developed by Universidad Técnica de Manabí
      researchers.
    source: ScienceDirect (Parraga-Alava et al., 2021) — [WEB-17];
      data available at [WEB-19]
    validity_relevance: This is the only publicly available Ecuador-specific Spanish
      crisis tweet dataset identified. It is useful as a starting point for Ecuadorian
      Spanish emergency NLP but does not cover timeline structure, summarization,
      humanitarian coordinator relevance criteria, geophysical disaster types beyond
      urban emergencies, or indigenous-language content.
  humaid_ecuador_earthquake_subset:
    description: The HumAID dataset (QCRI, 2021) includes the 2016 Ecuador Earthquake
      as one of 19 disaster events, with approximately 1.7 million raw tweets in the
      pool and approximately 2,000 annotated tweets. However, all HumAID annotations
      are in English and the dataset covers tweet classification (11 categories) rather
      than timeline extraction or summarization.
    source: ResearchGate HumAID paper — [WEB-22];
      dataset at [WEB-26]
    validity_relevance: Provides earthquake-type crisis data with an Ecuador event,
      but English-only annotations and classification-only task design mean it cannot
      substitute for the timeline extraction and summarization tasks required by the
      deployment. The 2016 Ecuador Earthquake subset also showed severe class imbalance
      (e.g., only 3 tweets in the 'displaced people and evacuations' class — MDPI
      — [WEB-27]), limiting training utility.
  sngr_institutional_name_change_2024:
    description: The national disaster risk management authority was renamed from
      SGR (Secretaría de Gestión de Riesgos) to SNGR (Secretaría Nacional de Gestión
      de Riesgos) by Decreto Ejecutivo No. 641 (January 2023) and formally codified
      by the Ley Orgánica para la Gestión Integral del Riesgo de Desastres (Registro
      Oficial No. 488, 30 January 2024). The Ecuador Sphere Manual was also institutionalized
      by SNGRE-034-2020 as the technical framework for humanitarian assistance.
    source: SNGR official resolution SNGR-102-2024 — [WEB-11]
    validity_relevance: NLP pipelines and training data referencing 'SGR' may not
      match current entity mentions of 'SNGR' in post-2023 tweets. Any NER or entity-linking
      system must handle both acronyms as referring to the same institution.
  multilingual_humanitarian_disaster_nlp_english_dominance:
    description: A 2024 review (HumVI paper) confirms that most humanitarian event
      detection datasets are disproportionately English, and identifies this as a
      key issue for improving adoption of NLP techniques in the humanitarian sector.
      The HumVI dataset itself attempts to be multilingual but focuses on violent
      incidents affecting humanitarian workers rather than natural disaster timelines.
    source: arXiv HumVI paper (2024) — [WEB-21]
    validity_relevance: Confirms that the English-dominance gap identified in the
      benchmark's coverage analysis is a known sector-wide problem, not an edge case.
      No multilingual timeline extraction or summarization benchmark for Spanish humanitarian
      crisis content exists.
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://books.openbookpublishers.com/10.11647/obp.0032/chapter11.html |
| WEB-2 | https://www.theglobaleconomy.com/Ecuador/literacy_rate/ |
| WEB-3 | https://www.worldviewdata.com/countries/ecuador/literacy-rate |
| WEB-4 | http://www.mannaproject.org/ecuador |
| WEB-5 | https://iwgia.org/en/ecuador/5087-iw-2023-ecuador.html |
| WEB-6 | https://en.wikipedia.org/wiki/Provinces_of_Ecuador |
| WEB-7 | https://www.researchgate.net/figure/Geographic-map-of-Ecuador-Administratively-Ecuador-is-divided-in-24-provinces-containing_fig1_360575372 |
| WEB-8 | https://storyteller.travel/map-provinces-ecuador/ |
| WEB-9 | https://en.wikipedia.org/wiki/Cantons_of_Ecuador |
| WEB-10 | https://www.gestionderiesgos.gob.ec/ |
| WEB-11 | https://www.gestionderiesgos.gob.ec/wp-content/uploads/downloads/2024/05/Resol.SNGR-102-2024.pdf |
| WEB-12 | https://en.wikipedia.org/wiki/Demographics_of_Ecuador |
| WEB-13 | https://ieeexplore.ieee.org/document/7889589 |
| WEB-14 | https://tradingeconomics.com/ecuador/individuals-using-the-internet-percent-of-population-wb-data.html |
| WEB-15 | https://datareportal.com/reports/digital-2026-ecuador |
| WEB-16 | https://www.worlddata.info/america/ecuador/telecommunication.php |
| WEB-17 | https://www.sciencedirect.com/science/article/pii/S2352340920315729 |
| WEB-18 | https://www.researchgate.net/publication/312485537_System_for_monitoring_natural_disasters_using_natural_language_processing_in_the_social_network_Twitter |
| WEB-19 | https://doi.org/10.17632/4x37zz82k8 |
| WEB-20 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6484392/ |
| WEB-21 | https://arxiv.org/html/2410.06370 |
| WEB-22 | https://www.researchgate.net/publication/350720422_HumAID_Human-Annotated_Disaster_Incidents_Data_from_Twitter |
| WEB-23 | https://crisisnlp.qcri.org/ |
| WEB-24 | https://disasterlaw.ifrc.org/dmi/dmi_country/49 |
| WEB-25 | https://www.uil.unesco.org/en/litbase/basic-education-young-people-and-adults-ecuador |
| WEB-26 | https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/A7NVF7 |
| WEB-27 | https://www.mdpi.com/2076-3417/15/8/4330 |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: CrisisLTLSum covers four crisis categories: wildfires, local fires, traffic incidents, and storms. For your Ecuador-focused deployment, are there disaster types your users would prioritize that fall outside this set — for example, volcanic eruptions, landslides, coastal floods, or earthquake aftershock sequences? Which crisis types matter most to Red Cross and UN OCHA coordinators in your context?
A1: The deployment prioritizes large-scale social and humanitarian crises — events whose impact exceeds local response capacity — many of which (volcanic eruptions, mass displacement, complex humanitarian emergencies) are not represented in the benchmark's four-category taxonomy.

Q2 [IC]: The benchmark tweets reference US-specific geographic markers (street names, county identifiers, US emergency agency handles like FEMA or local fire departments). Would your analysts expect the system to correctly anchor events to Ecuador-specific administrative units (parroquias, cantones, provincias), local agencies (SGR, Cuerpo de Bomberos), and local landmarks?
A2: Yes — analysts would require precise anchoring to Ecuador-specific geographic and institutional entities; US-default references would be operationally meaningless or misleading.

Q3 [OC]: Ground-truth relevance labels and summaries in the benchmark were produced for US English tweets by annotators in a US crisis-response context. Who in your organization would serve as the authoritative judge of tweet relevance and summary quality?
A3: An inter-operational team — combining local field coordinators, social analysts, and domain experts — would jointly serve as the authoritative judges, rather than any single role.

Q4 [IF]: The benchmark is built entirely from English-language tweets. Your deployment targets Ecuadorian Spanish, potentially including code-switching with Kichwa, regional slang, informal abbreviations, and non-standard orthography. Would your tweet stream be predominantly standard written Spanish, or do you expect significant register variation and indigenous-language mixing?
A4: The stream would be predominantly Ecuadorian Spanish in a mix of informal and semi-formal registers, with some indigenous-language entity names (especially place names). A system trained solely on English social media — even if fine-tuned on general Spanish — would likely miss local Ecuadorian social media characteristics.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark's four US-local crisis categories (fires, traffic, storms) structurally exclude the large-scale humanitarian and geophysical disaster types (volcanic eruptions, mass displacement, complex emergencies) that are the primary operational focus for Ecuador-based NGO coordinators. |
| IC | HIGH | Benchmark instances are anchored to US geographic, institutional, and cultural markers (FEMA, county names, US emergency handles) that are entirely absent from Ecuadorian crisis tweets, which reference SGR, parroquias, cantones, and local landmarks — making construct-irrelevant variance pervasive at the instance level. |
| IF | HIGH | The benchmark is English-only text; the deployment processes Ecuadorian Spanish social media with informal register, crisis-specific vocabulary ("damnificados," "albergue"), and indigenous-language entity names (Kichwa place names), creating a substantial signal-distribution mismatch for any system trained or calibrated on the benchmark. |
| OO | HIGH | Relevance and summarization categories were designed for US local incidents with implicit assumptions about operational salience; for humanitarian coordinators, relevance criteria (e.g., road access to rural communities, informal community broadcasts) differ structurally from US annotation norms, meaning the output taxonomy is misaligned. |
| OC | HIGH | Ground-truth labels were produced by US-context annotators; the deployment requires inter-operational validation by teams combining Ecuadorian field coordinators, social analysts, and domain experts — a fundamentally different and unavailable annotator population, making label transferability low. |
| OF | MODERATE | Both the benchmark and deployment involve text-based extraction and summarization tasks, so the surface output modality matches; however, the benchmark includes English-language human-written summaries whose style may not match the operational reporting conventions expected by UN OCHA or Red Cross analysts writing in Spanish. |

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
  "region": "Ecuador — Humanitarian Crisis Social Media Analysts",
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
