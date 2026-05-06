I need you to perform a validity analysis of an AI benchmark for a specific target region.

## Instructions

You are evaluating whether the benchmark **Teaching Machines to Read and Comprehend (CNN/Daily Mail Reading Comprehension Benchmark)** is valid for use in **Ecuador Humanitarian Crisis Tweet Analysis — NGO/IO Analyst Deployment**.

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

- **Name**: cnn_dailymail_rc
- **Full Name**: Teaching Machines to Read and Comprehend (CNN/Daily Mail Reading Comprehension Benchmark)
- **Domain**: Machine reading comprehension
- **Languages**: en
- **Porting Strategy**: none
- **Year**: 2015

### Benchmark Documentation

## Key characteristics relevant to validity analysis

### Input Ontology
The benchmark defines a single unified task type: supervised reading comprehension
via Cloze-style entity fill-in, formalized as estimating p(a|c, q) over a context
document, query, and answer [Q10]. The task is explicitly scoped to document-internal
linguistic relationship detection, with world knowledge and co-occurrence statistics
deliberately excluded as confounds [Q11, Q17]. The paper taxonomizes model architectures
across Deep LSTM Readers [Q39, Q44], Attentive Readers, and Impatient Readers [Q54],
and contrasts traditional NLP pipeline approaches against neural models [Q23, Q24, Q55],
but does not subdivide the task by content domain, crisis type, or cultural category.
There are no humanitarian crisis subtasks, no disaster-response categories, no
socio-political emergency classifications, and no temporal event-sequencing components
[Q41] — the task is a single-document, single-answer entity lookup.

For the Ecuador humanitarian deployment, this task taxonomy is entirely misaligned.
Operational users require coverage of compound and socio-political crises scored by
population impact and response-gap severity, not entity retrieval from news summaries.
No benchmark category corresponds to disaster type classification, needs-evolution
tracking, or timeline generation.

### Input Content
Data is drawn exclusively from two English-language Western news outlets: CNN
(~93,000 articles) and the Daily Mail (~220,000 articles), spanning April 2007 /
June 2010 through April 2015 [Q4, Q9, Q14]. Queries are generated fully automatically
by applying entity detection and anonymization algorithms to machine-extracted
bullet-point summaries [Q3, Q14, Q16]; no human curation, community sourcing, or
regional editorial input is involved. The corpus is rooted in US/UK institutional
news register, Western geographic references, and anglophone journalistic conventions.
Articles exceeding 2,000 tokens or lacking the answer entity in context were filtered
out [Q9], and average CNN validation documents contain 763 tokens and 27 entities [Q76].

For the Ecuador deployment, this content grounding represents a critical gap: the
source corpus contains zero coverage of Latin American administrative structures,
Ecuadorian emergency agencies (SGR, Cuerpo de Bomberos), informal disaster-register
vocabulary, or indigenous-language entity names. The automated label generation
[Q16] reflects anglophone editorial judgment, not the operational relevance assessments
of humanitarian field coordinators or affected Ecuadorian communities.

### Input Form
Benchmark inputs are formal, written English text drawn from a structured news domain,
processed as sequences of tokens fed into Deep LSTM encoders [Q40, Q42, Q43] or
bidirectional LSTM encoders for attention models [Q46, Q47, Q48]. The entity
anonymization and random permutation procedure [Q18] replaces all named entities
with abstract markers (ent5, ent85, etc.), which suppresses lexical surface form in
favor of structural context. Frame-semantic model variants additionally require
unanonymized text for PropBank parser compatibility [Q25, Q26, Q28, Q30]. The paper
notes that anonymization may favor models capable of exploiting syntax over
semantics [Q56].

The input form is categorically mismatched with the Ecuador deployment's tweet stream.
The deployment processes informal-to-semi-formal Ecuadorian Spanish tweets with
non-standard orthography, crisis-specific abbreviations, and indigenous-language
(Kichwa) terms in place and entity names. The anonymization procedure [Q18] would
entirely suppress the dialect-specific and register-specific entity signals that are
diagnostically critical for anchoring events to Ecuadorian geographic and institutional
references. The benchmark's sensitivity to document length [Q78] — designed for
documents averaging 763 tokens [Q76] — also raises questions about applicability to
short, fragmented tweet-length inputs.

### Output Ontology
The benchmark's implicit output ontology is a closed entity-classification schema:
the model must select the correct anonymized entity token from the candidate set
appearing in the context document [Q34], scored by classification accuracy [Q22, Q52].
No structured label taxonomy, multi-class output schema, or humanitarian category
hierarchy is described anywhere in the paper — the label space is a vocabulary of
anonymized entity markers drawn from individual news documents. The paper is entirely
silent on any output category taxonomy beyond this implicit structure.

NOT DOCUMENTED: No label ontology, output category schema, or structured decision
taxonomy beyond entity token prediction is described.

For the Ecuador deployment, this output ontology has no correspondence to any
humanitarian coordination output structure. The deployment requires temporally ordered,
operationally relevant narrative timeline summaries — a fundamentally different output
structure from token-level entity fill-in. No mapping exists between entity prediction
accuracy and timeline coherence, operational relevance, or needs-evolution tracking.

### Output Content
NOT DOCUMENTED: The paper contains no human annotation process. Ground-truth labels
are generated entirely algorithmically by replacing entities in machine-extracted
bullet-point summaries [Q16]. No annotator demographics, inter-annotator agreement
statistics, human quality assurance, or community validation procedures are described
anywhere in the paper. The authors acknowledge that the frame-semantic approach does
not generalize beyond its parsing phase [Q27] and that many queries remain ambiguous
or unanswerable even under human evaluation [Q81, Q82, Q83, Q84].

For the Ecuador deployment, this absence is critical. The authoritative quality standard
rests with an inter-operational team of field coordinators, social analysts, and domain
experts who collectively judge relevance and summary quality for Ecuadorian crisis content.
The benchmark's automated label generation rooted in anglophone editorial conventions
provides no approximation of this multi-role humanitarian validation structure.

### Output Form
The benchmark evaluates models on classification accuracy over a closed entity token
set — a single discrete entity label per query [Q34, Q52]. Multiple evaluation strategies
are defined including majority-frequency baselines [Q22], word-distance alignment [Q32,
Q33], frame-semantic rule-based heuristics tuned iteratively on validation data [Q29,
Q31], and neural models whose output is a probability distribution over document tokens
[Q49, Q50, Q51]. Performance is reported as accuracy on held-out test sets [Q59], with
hyperparameters tuned on validation sets [Q58, Q60, Q61, Q62]. Attention heat maps are
used to interpret model behavior [Q79, Q85, Q86, Q87, Q88], and performance is analyzed
as a function of document length [Q78].

For the Ecuador deployment, this output form is categorically mismatched. The deployment
requires temporally ordered, multi-sentence narrative summaries suited to NGO coordination
workflows. Entity prediction accuracy [Q34] has no analog in timeline quality assessment,
and attention visualization [Q88] does not translate to metrics for evaluating timeline
coherence, geographic anchoring precision, or operational relevance as judged by
humanitarian coordinators.

### Stated Limitations
The authors acknowledge several relevant limitations. They critique prior synthetic
data approaches for failing to "capture the complexity, richness, and noise of natural
language" [Q6] — a criticism that applies with force to the benchmark's own anonymization
procedure when evaluated against informal social media. Training corpus limitations are
acknowledged [Q12, Q13], but the solution remains narrowly scoped to English news.
The frame-semantic pipeline is flagged for poor coverage due to PropBank parser
limitations [Q64] and inability to scale to multi-sentence inference [Q66, Q67], with
predicted worse performance "on other types of machine reading data where questions
rather than Cloze queries are used" [Q68]. The fixed-width LSTM hidden vector is
identified as an information bottleneck [Q45], memory constraints limited architectural
depth [Q69], and ambiguous geographic queries are explicitly flagged as a failure mode
[Q81, Q82] — particularly for queries where anonymization makes it impossible to
distinguish between administrative levels. The authors acknowledge that "many queries
requiring complex inference and long range reference resolution" remain unsolved [Q75],
and that world knowledge and multi-document queries would require fundamentally different
architectures [Q74].


### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "Machine reading systems can be tested on their ability to answer questions posed on the contents of documents that they have seen, but until now large scale training and test datasets have been missing for this type of evaluation." |
| Q2 | 1 | input_ontology | "In this work we define a new methodology that resolves this bottleneck and provides large scale supervised reading comprehension data." |
| Q3 | 1 | input_content | "We observe that summary and paraphrase sentences, with their associated documents, can be readily converted to context–query–answer triples using simple entity detection and anonymisation algorithms." |
| Q4 | 1 | input_content | "Using this approach we have collected two new corpora of roughly a million news stories with associated queries from the CNN and Daily Mail websites." |
| Q5 | 1 | input_content | "While obtaining supervised natural language reading comprehension data has proved difficult, some researchers have explored generating synthetic narratives and queries [3, 4]." |
| Q6 | 1 | input_content | "Historically, however, many similar approaches in Computational Linguistics have failed to manage the transition from synthetic data to real environments, as such closed worlds inevitably fail to capture the complexity, richness, and noise of natural language [5]." |
| Q7 | 1 | output_form | "These models draw on recent developments for incorporating attention mechanisms into recurrent neural network architectures [6, 7, 8, 4]." |
| Q8 | 1 | output_content | "Karl Moritz Hermann, Tomáš Kočiský, Edward Grefenstette, Lasse Espeholt, Will Kay, Mustafa Suleyman, Phil Blunsom are from Google DeepMind and University of Oxford." |
| Q9 | 2 | input_content | "Articles were collected starting in April 2007 for CNN and June 2010 for the Daily Mail, both until the end of April 2015. Validation data is from March, test data from April 2015. Articles of over 2000 tokens and queries whose answer entity did not appear in the context were filtered out." |
| Q10 | 2 | input_ontology | "The reading comprehension task naturally lends itself to a formulation as a supervised learning problem. Specifically we seek to estimate the conditional probability p(a\|c, q), where c is a context document, q a query relating to that document, and a the answer to that query." |
| Q11 | 2 | input_ontology | "For a focused evaluation we wish to be able to exclude additional information, such as world knowledge gained from co-occurrence statistics, in order to test a model's core capability to detect and understand the linguistic relationships between entities in the context document." |
| Q12 | 2 | input_content | "Such an approach requires a large training corpus of document–query–answer triples and until now such corpora have been limited to hundreds of examples and thus mostly of use only for testing [9]." |
| Q13 | 2 | input_content | "This limitation has meant that most work in this area has taken the form of unsupervised approaches which use templates or syntactic/semantic analysers to extract relation tuples from the document to form a knowledge graph that can be queried." |
| Q14 | 2 | input_content | "We have collected 93k articles from the CNN and 220k articles from the Daily Mail websites. Both news providers supplement their articles with a number of bullet points, summarising aspects of the information contained in the article." |
| Q15 | 2 | input_form | "Of key importance is that these summary points are abstractive and do not simply copy sentences from the documents." |
| Q16 | 2 | output_content | "We construct a corpus of document–query–answer triples by turning these bullet points into Cloze [12] style questions by replacing one entity at a time with a placeholder. This results in a combined corpus of roughly 1M data points (Table 1)." |
| Q17 | 2 | input_ontology | "Note that the focus of this paper is to provide a corpus for evaluating a model's ability to read and comprehend a single document, not world knowledge or co-occurrence." |
| Q18 | 3 | input_form | "To prevent such degenerate solutions and create a focused task we anonymise and randomise our corpora with the following procedure, a) use a coreference system to establish coreferents in each data point; b) replace all entities with abstract entity markers according to coreference; c) randomly permute these entity markers whenever a data point is loaded." |
| Q19 | 3 | input_form | "Clearly a human reader can answer both queries correctly. However in the anonymised setup the context document is required for answering the query, whereas the original version could also be answered by someone with the requisite background knowledge." |
| Q20 | 3 | input_ontology | "Therefore, following this procedure, the only remaining strategy for answering questions is to do so by exploiting the context presented with each question. Thus performance on our two corpora truly measures reading comprehension capability." |
| Q21 | 3 | output_ontology | "Table 2 gives an indication of the difficulty of the task, showing how frequent the correct answer is contained in the top N entity markers in a given document. Note that our models don't distinguish between entity markers and regular words. This makes the task harder and the models more general." |
| Q22 | 3 | output_form | "We define two simple baselines, the majority baseline (maximum frequency) picks the entity most frequently observed in the context document, whereas the exclusive majority (exclusive frequency) chooses the entity most frequently observed in the context but not observed in the query." |
| Q23 | 3 | input_ontology | "Traditionally, a pipeline of NLP models has been used for attempting question answering, that is models that make heavy use of linguistic annotation, structured world knowledge and semantic parsing and similar NLP pipeline outputs." |
| Q24 | 3 | input_ontology | "Frame-semantic parsing attempts to identify predicates and their arguments, allowing models access to information about "who did what to whom"." |
| Q25 | 4 | input_form | "makes use of frame-semantic annotations which we obtained by parsing our model with a state-of-the-art frame-semantic parser [13, 14]." |
| Q26 | 4 | input_form | "As the parser makes extensive use of linguistic information we run these benchmarks on the unanonymised version of our corpora." |
| Q27 | 4 | output_content | "There is no significant advantage in this as the frame-semantic approach used here does not possess the capability to generalise through a language model beyond exploiting one during the parsing phase." |
| Q28 | 4 | input_form | "Extracting entity-predicate triples—denoted as (e1, V, e2)—from both the query q and context document d, we attempt to resolve queries using a number of rules with an increasing recall/precision trade-off as follows (Table 4)." |
| Q29 | 4 | output_content | "Strategies are ordered by precedence and answers determined accordingly. This heuristic algorithm was iteratively tuned on the validation data set." |
| Q30 | 4 | input_form | "For reasons of clarity, we pretend that all PropBank triples are of the form (e1, V, e2). In practice, we take the argument numberings of the parser into account and only compare like with like, except in cases such as the permuted frame rule, where ordering is relaxed." |
| Q31 | 4 | output_form | "In the case of multiple possible answers from a single rule, we randomly choose one." |
| Q32 | 4 | output_form | "We consider another baseline that relies on word distance measurements. Here, we align the placeholder of the Cloze form question with each possible entity in the context document and calculate a distance measure between the question and the context around the aligned entity." |
| Q33 | 4 | output_form | "We tune the maximum penalty per word (m = 8) on the validation data." |
| Q34 | 4 | output_ontology | "We propose three neural models for estimating the probability of word type a from document d answering query q: p(a\|d, q) ∝ exp (W(a)g(d, q)), s.t. a ∈ V, where V is the vocabulary, and W(a) indexes row a of weight matrix W and through a slight abuse of notation word types double as indexes." |
| Q35 | 4 | input_ontology | "Note that we do not privilege entities or variables, the model must learn to differentiate these in the input sequence." |
| Q36 | 4 | input_form | "The function g(d, q) returns a vector embedding of a document and query pair." |
| Q37 | 4 | input_ontology | "Long short-term memory (LSTM, [18]) networks have recently seen considerable success in tasks such as machine translation and language modelling [17]." |
| Q38 | 4 | input_ontology | "When used for translation, Deep LSTMs [19] have shown a remarkable ability to embed long sequences into a vector representation which contains enough information to generate a full translation in another language." |
| Q39 | 4 | input_ontology | "Our first neural model for reading comprehension tests the ability of Deep LSTM encoders to handle significantly longer sequences." |
| Q40 | 4 | input_form | "We feed our documents one word at a time into a Deep LSTM encoder, after a delimiter we then also feed the query into the encoder. Alternatively we also experiment with processing the query then the document." |
| Q41 | 4 | input_ontology | "The result is that this model processes each document query pair as a single long sequence. Given the embedded document and query the network predicts which token in the document answers the query." |
| Q42 | 5 | input_form | "We employ a Deep LSTM cell with skip connections from each input x(t) to every hidden layer, and from every hidden layer to the output y(t):" |
| Q43 | 5 | input_form | "Thus our Deep LSTM Reader is defined by g^LSTM(d, q) = y(\|d\|+\|q\|) with input x(t) the concatenation of d and q separated by the delimiter \|\|\|." |
| Q44 | 5 | input_ontology | "The Deep LSTM Reader must propagate dependencies over long distances in order to connect queries to their answers." |
| Q45 | 5 | input_form | "The fixed width hidden vector forms a bottleneck for this information flow that we propose to circumvent using an attention mechanism inspired by recent results in translation and image recognition [6, 7]." |
| Q46 | 5 | input_form | "This attention model first encodes the document and the query using separate bidirectional single layer LSTMs [19]." |
| Q47 | 5 | input_form | "The encoding u of a query of length \|q\| is formed by the concatenation of the final forward and backward outputs, u = −→yq (\|q\|) \|\| ←−yq (1)." |
| Q48 | 5 | input_form | "For the document the composite output for each token at position t is, yd(t) = −→yd(t) \|\| ←−yd(t)." |
| Q49 | 5 | output_form | "The representation r of the document d is formed by a weighted sum of these output vectors." |
| Q50 | 5 | output_form | "These weights are interpreted as the degree to which the network attends to a particular token in the document when answering the query:" |
| Q51 | 5 | output_form | "The variable s(t) is the normalised attention at token t." |
| Q52 | 6 | output_form | "Having described a number of models in the previous section, we next evaluate these models on our reading comprehension corpora." |
| Q53 | 6 | input_ontology | "Our hypothesis is that neural models should in principle be well suited for this task." |
| Q54 | 6 | input_ontology | "We expect that the attention-based models would therefore outperform the pure LSTM-based approaches." |
| Q55 | 6 | input_ontology | "Considering the second dimension of our investigation, the comparison of traditional versus neural approaches to NLP, we do not have a strong prior favouring one approach over the other." |
| Q56 | 6 | input_form | "The entity anonymisation and permutation aspect of the task presented here may end up levelling the playing field in that regard, favouring models capable of dealing with syntax rather than just semantics." |
| Q57 | 6 | output_form | "With these considerations in mind, the experimental part of this paper is designed with a threefold aim. First, we want to establish the difficulty of our machine reading task by applying a wide range of models to it. Second, we compare the performance of parse-based methods versus that of neural models. Third, within the group of neural models examined, we want to determine what each component contributes to the end performance; that is, we want to analyse the extent to which an LSTM can solve this task, and to what extent various attention mechanisms impact performance." |
| Q58 | 6 | output_form | "All model hyperparameters were tuned on the respective validation sets of the two corpora." |
| Q59 | 6 | output_form | "Our experimental results are in Table 5, with the Attentive and Impatient Readers performing best across both datasets." |
| Q60 | 6 | output_form | "For the Deep LSTM Reader, we consider hidden layer sizes [64, 128, 256], depths [1, 2, 4], initial learning rates [1E−3, 5E−4, 1E−4, 5E−5], batch sizes [16, 32] and dropout [0.0, 0.1, 0.2]. We evaluate two types of feeds. In the cqa setup we feed first the context document and subsequently the question into the encoder, while the qca model starts by feeding in the question followed by the context document. We report results on the best model (underlined hyperparameters, qca setup)." |
| Q61 | 6 | output_form | "For the attention models we consider hidden layer sizes [64, 128, 256], single layer, initial learning rates [1E−4, 5E−5, 2.5E−5, 1E−5], batch sizes [8, 16, 32] and dropout [0, 0.1, 0.2, 0.5]." |
| Q62 | 6 | output_form | "For all models we used asynchronous RmsProp [20] with a momentum of 0.9 and a decay of 0.95." |
| Q63 | 7 | output_ontology | "While the one frame-semantic model proposed in this paper is clearly a simplification of what could be achieved with annotations from an NLP pipeline, it does highlight the difficulty of the task when approached from a symbolic NLP perspective." |
| Q64 | 7 | output_ontology | "First, the frame-semantic pipeline has a poor degree of coverage with many relations not being picked up by our PropBank parser as they do not adhere to the default predicate-argument structure." |
| Q65 | 7 | input_content | "This effect is exacerbated by the type of language used in the highlights that form the basis of our datasets." |
| Q66 | 7 | output_ontology | "The second issue is that the frame-semantic approach does not trivially scale to situations where several sentences, and thus frames, are required to answer a query." |
| Q67 | 7 | output_ontology | "This was true for the majority of queries in the dataset." |
| Q68 | 7 | output_ontology | "We expect that on other types of machine reading data where questions rather than Cloze queries are used this particular model would perform significantly worse." |
| Q69 | 7 | output_form | "Memory constraints prevented us from experimenting with deeper Attentive Readers." |
| Q70 | 8 | input_ontology | "The supervised paradigm for training machine reading and comprehension models provides a promising avenue for making progress on the path to building full natural language understanding systems." |
| Q71 | 8 | input_ontology | "We have demonstrated a methodology for obtaining a large number of document-query-answer triples and shown that recurrent and attention based neural networks provide an effective modelling framework for this task." |
| Q72 | 8 | output_form | "Our analysis indicates that the Attentive and Impatient Readers are able to propagate and integrate semantic information over long distances." |
| Q73 | 8 | output_form | "In particular we believe that the incorporation of an attention mechanism is the key contributor to these results." |
| Q74 | 8 | output_ontology | "However, the incorporation of world knowledge and multi-document queries will also require the development of attention and embedding mechanisms whose complexity to query does not scale linearly with the data set size." |
| Q75 | 8 | output_ontology | "There are still many queries requiring complex inference and long range reference resolution that our models are not yet able to answer." |
| Q76 | 8 | input_form | "Note that these examples were chosen as they were short, the average CNN validation document contained 763 tokens and 27 entities, thus most instances were significantly harder to answer than these examples." |
| Q77 | 10 | output_form | "The precise hyperparameters used for the various attentive models are as in Table 6. All models were trained using asynchronous RmsProp [20] with a momentum of 0.9 and a decay of 0.95." |
| Q78 | 10 | output_form | "To understand how the model performance depends on the size of the context, we plot performance versus document lengths in Figures 4 and 5. The first figure (Fig. 4) plots a sliding window of performance across document length, showing that performance of the attentive models degrades slightly as documents increase in length. The second figure (Fig. 5) shows the cumulative performance with documents up to length N, showing that while the length does impact the models' performance, that effect becomes negligible after reaching a length of ~500 tokens." |
| Q79 | 10 | output_form | "We expand on the analysis of the attention mechanism presented in the paper by including visualisations for additional queries from the CNN validation dataset below. We consider examples from the Attentive Reader as well as the Impatient Reader in this appendix." |
| Q80 | 10 | input_ontology | "Figure 6 shows two positive examples from the CNN validation set that require reasonable levels of lexical generalisation and co-reference in order to be answered. The first query in Figure 7 contains strong lexical cues through the quote, but requires identifying the entity" |
| Q81 | 11 | output_content | "Figures 8 and 9 show examples of queries where the Attentive Reader fails to select the correct answer. The two examples in Figure 8 highlight a fairly common phenomenon in the data, namely ambiguous queries, where—at least following the anonymisation process—multiple entities are plausible answers even when evaluated manually." |
| Q82 | 11 | output_content | "Note that in both cases the query searches for an entity marker that describes a geographic location, preceded by the word "in". Here it is unclear whether the placeholder refers to a part of town, town, region or country." |
| Q83 | 11 | output_content | "Figure 9 contains two additional negative cases. The first failure is caused by the co-reference entity selection process. The correct entity, ent15, and the predicted one, ent81, both refer to the same person, but not being clustered together. Arguably this is a difficult clustering as one entity refers to "Kate Middleton" and the other to "The Duchess of Cambridge"." |
| Q84 | 11 | output_content | "The right example shows a situation in which the model fails as it perhaps gets too little information from the short query and then selects the wrong cue with the term "claims" near the wrongly identified entity ent1 (correct: ent74)." |
| Q85 | 11 | output_form | "To give a better intuition for the behaviour of the Impatient Reader, we use a similar visualisation technique as before. However, this time around we highlight the attention at every time step as the model updates its focus while moving through a given query. Figures 10–13 shows how the attention of the Impatient Reader changes and becomes increasingly more accurate as the model" |
| Q86 | 12 | output_form | "Figure 7: Two more correctly answered validation set queries. The left example (entity ent315) requires correctly attributing the quote, which does not appear trivial with a number of other candidate entities in the vicinity. The right hand side shows our model is not afraid of Chuck Norris (ent164)." |
| Q87 | 12 | output_form | "Figure 8: Attention heat maps from the Attentive Reader for two wrongly answered validation set queries. In the left case the model returns ent85 (correct: ent67), in the right example it gives ent24 (correct: ent64). In both cases the query is unanswerable due to its ambiguous nature and the model selects a plausible answer." |
| Q88 | 12 | output_form | "Note how the attention is distributed fairly arbitraty at first, slowly focussing on the correct entity ent5 only once the question has sufficiently been parsed." |

---

## Regional Context

```yaml
name: Ecuador Humanitarian Crisis Tweet Analysis — NGO/IO Analyst Deployment
abbreviation: ECU-HumTweet
scope_note: 'This region document is scoped to the specific deployment population
  described in the elicitation summary: social and data analysts at NGOs and international
  organizations (Red Cross, UN OCHA) processing Spanish-language Ecuadorian crisis
  tweets to generate operational timelines, together with the affected Ecuadorian
  populations who author those tweets. It is not a general Latin America or Ecuador
  country profile.'
primary_country: Ecuador
deployment_geography:
  national_level: Ecuador
  sub_national_administrative_hierarchy:
    levels:
    - provincia
    - cantón
    - parroquia
    note: Operational anchoring requires disambiguation to all three levels. Parroquia-level
      precision is frequently required for field coordination decisions.
    salient_provinces_for_disaster_response: Manabí (major coastal flooding; epicenter
      of 2016 earthquake), Esmeraldas (coastal flooding and seismic risk), El Oro
      (flooding), Loja (drought and flooding), Chimborazo and Cotopaxi (volcanic and
      highland hazards), Tungurahua (volcanic), Napo and Pastaza (Amazon flooding),
      Pichincha (volcanic, Quito metro area). Confirmed by SGR open event data 2010–2023
      and SNGRE operational resolutions — [WEB-1];
      [WEB-2].
    total_provincias: '24 — Source: INEC 2022 census and multiple corroborating sources
      (Provinces of Ecuador, Wikipedia — [WEB-3];
      geopostcodes.com — [WEB-4]).'
    total_cantones: '221–222 (221 per pre-2024 official records; Wikipedia notes 222
      as of 2025 following creation of Sevilla Don Bosco canton in Morona Santiago
      Province in 2024) — Source: Wikipedia Cantons of Ecuador — [WEB-5];
      INEC 2022 census data cited in Grokipedia — [WEB-6].'
    total_parroquias: 'Approximately 1,499–1,500 (1,499 per INEC 2022 census; some
      sources round to 1,500) — Source: INEC 2022 census as cited in Grokipedia —
      [WEB-6]; Storyteller Travel
      compendium — [WEB-7].'
  tweet_authorship_geography: Tweets originate from across Ecuador, including both
    urban centers (Quito, Guayaquil, Cuenca) and rural and peri-urban areas affected
    by crisis events; geographic spread of authorship is expected to be uneven and
    event-driven.
target_population:
  primary_users:
    description: Social and data analysts at NGOs and international humanitarian organizations
      — primarily Red Cross Ecuador and UN OCHA — who consume system outputs as decision-support
      tools for operational coordination. Includes field coordinators, domain experts
      (health, WASH, shelter, logistics), and social analysts who collectively form
      the authoritative inter-operational judgment panel for output quality.
    language_profile: Fluent in American English and Spanish; comfortable reading
      formal and semi-formal humanitarian reporting in both languages; may include
      speakers of varied Latin American Spanish accents and a range of English-language
      national backgrounds.
    roles_in_quality_judgment:
    - Field coordinators — assess operational relevance and geographic anchoring precision
    - Social analysts — assess tweet-level signal quality and register coverage
    - Domain experts — assess humanitarian taxonomy accuracy and needs-evolution tracking
    note: No single annotator archetype is authoritative; inter-operational consensus
      is the ground-truth standard per the elicitation.
  tweet_author_population:
    description: Ecuadorian residents affected by or witnessing disaster and humanitarian
      crisis events who post to Twitter/X during or immediately following emergencies.
      Includes direct crisis-affected populations, community observers, informal journalists,
      local NGO volunteers, and municipal officials.
    language_profile: Ecuadorian Spanish in mixed informal-to-semi-formal register;
      crisis-time abbreviations and non-standard orthography expected; indigenous-language
      terms (primarily Kichwa) appear in place names and entity references.
    digital_access_notes: Twitter authorship during crises is skewed toward urban
      and peri-urban populations with smartphone access; rural and indigenous community
      voices may be underrepresented in the tweet stream relative to their share of
      crisis-affected populations.
languages:
  primary_operational_languages:
  - Ecuadorian Spanish (tweet input stream and analyst bilingual fluency)
  - American English (analyst reporting and benchmark/system documentation)
  indigenous_language_presence:
    primary_indigenous_language: Kichwa (Ecuadorian variant of Quechua)
    role_in_deployment: Kichwa terms appear principally as components of place names,
      community names, and entity references embedded within Spanish-language tweets
      — not as full-sentence code-switching. Examples include cantón, parroquia, and
      community names of Kichwa origin.
    other_indigenous_languages_possible: 'NEEDS VERIFICATION — deferred: likely unsearchable
      (lived practice). Ecuador officially recognises approximately 14 indigenous
      languages (Kichwa, Shuar, Tsafiki/Tsáfiki, Achuar, Awá, Chachi, Epera, Andoa,
      Sapara, Siekopai, Siona, Waorani, Zápara, and others). Of these, Shuar in the
      Amazon and Tsáfiki (in Santo Domingo de los Tsáchilas) are most likely to contribute
      place-name tokens in crisis-time tweets from those regions. Whether their tokens
      appear in practice in Twitter data during specific crises is not documented
      in searchable sources and requires stakeholder elicitation with field analysts
      who monitor those regions.'
    kichwa_nlp_resources: 'Kichwa is confirmed as an extremely low-resource language
      with severe NLP tool gaps. The Killkan dataset (2024) is the first ASR resource
      for Kichwa incorporating morphosyntactic information; prior to this, no NLP
      resources existed for Kichwa for NLP applications. A 2021 IEEE paper confirms
      that insufficient digital bilingual Kichwa-Spanish texts preclude robust translation
      or NER tools for the Ecuadorian Kichwa variant specifically. No social-media-specific
      tokenizer, NER system, or entity recognizer for Kichwa-Spanish code-switching
      in Twitter contexts has been identified. This represents a hard gap for any
      NER system processing Ecuadorian crisis tweets with Kichwa-origin place names.
      Sources: Killkan arXiv preprint — [WEB-8]; IEEE
      Kichwa-Spanish NMT paper — [WEB-9].'
  register_and_dialect_notes: 'The tweet stream is predominantly Ecuadorian Spanish.
    Key register characteristics include: crisis-specific abbreviations (e.g., referencing
    emergency agencies), informal orthographic variation (vowel elision, phonetic
    spelling), and the use of local geographic shorthand. A system trained only on
    generic Spanish or English social media would be expected to miss dialect-specific
    signals. Costeño (coastal) and Serrano (highland) dialectal variation may appear
    within the same event dataset.'
  code_switching_pattern: 'Indigenous-language mixing is primarily lexical and onomastic
    (place and entity names), not full code-switching at the sentence level. This
    is diagnostically important for NER systems that must resolve ambiguous entity
    boundaries at Kichwa-Spanish token interfaces. Research on Quechua/Kichwa social
    media use confirms agglutinative morphology creates context-dependent word forms
    that do not appear consistently across datasets, compounding NLP challenges —
    Source: CDT Quechua social media report 2025 — [WEB-10].'
writing_systems:
  scripts:
  - Latin alphabet (Spanish and Kichwa as written in Ecuador)
  orthographic_variation_notes: 'Kichwa orthography in Ecuador is not fully standardized;
    place names may appear in variant spellings (e.g., historical Spanish-influenced
    vs. modern unified Kichwa orthography). Crisis-time tweets exhibit additional
    non-standard orthography: phonetic spelling, truncation, missing diacritics, all-caps
    for urgency, and SMS-era abbreviations. NLP systems must handle this variation
    robustly.'
  unicode_notes: Spanish diacritics (á, é, í, ó, ú, ñ, ü) are frequently omitted in
    informal tweet text; systems should not assume consistent diacritic usage.
literacy_and_digital_access:
  ecuador_national_literacy_rate: 'Approximately 94.6% (national illiteracy rate 5.4%
    as of 2024, down from ~14% in 2014) — Source: Statista/INEC 2024 — [WEB-11].
    Note: this is a national aggregate; rural and indigenous communities in crisis-affected
    provinces have historically higher illiteracy rates than the national figure.'
  ecuador_internet_penetration_pct: '78.2% of population had internet access as of
    December 2023 (ARCOTEL official figure), up from 74.4% in December 2022. A separate
    DataReportal figure for January 2024 gives 83.6%, reflecting different methodology.
    The ARCOTEL-sourced Freedom House figure is preferred as it cites the official
    regulator. Note: these are national aggregates; rural crisis-affected provinces
    have substantially lower connectivity. Sources: Freedom House / ARCOTEL 2024 —
    [WEB-12]; DataReportal 2024
    — [WEB-13].'
  ecuador_smartphone_penetration_pct: 'Over 57% of the Ecuadorian population owned
    a smartphone in 2024, up from 46% in 2019; mobile devices accounted for approximately
    48% of web traffic — Source: Statista 2024 — [WEB-14].
    Note: national aggregate; rural/indigenous communities in crisis-affected provinces
    likely substantially below this figure.'
  twitter_x_active_users_ecuador: 'Ecuador had approximately 12.66 million social
    media users in January 2024 (69.2% of population); no Ecuador-specific Twitter/X
    user count was identified. DataReportal notes 82.8% of internet users used at
    least one social media platform — Source: DataReportal 2024 — [WEB-13].
    A Twitter/X-specific Ecuador user count was not found in public sources; this
    slot remains partially unresolved.'
  rural_urban_connectivity_gap: 'Mobile internet penetration reached 62.4% nationally
    as of December 2023 (ARCOTEL), with LTE subscriptions accounting for 61% of all
    mobile lines in November 2023. Fixed-line broadband remained low at 15.4% nationally.
    Rural provinces (e.g., Manabí, Esmeraldas, Cotopaxi) have substantially lower
    connectivity than Quito and Guayaquil; no province-level breakdown was found in
    public sources. Additionally, in late 2023–early 2024, drought-related power outages
    of 1–13 hours/day disrupted telecommunications across Ecuador, compounding connectivity
    gaps during crisis periods — Source: Freedom House / ARCOTEL 2024 — [WEB-12].'
  crisis_time_connectivity_notes: 'Disaster events may degrade mobile and internet
    infrastructure precisely when the tweet stream is most operationally relevant.
    Coverage gaps in affected areas introduce survivorship bias in the tweet corpus:
    areas with destroyed infrastructure are underrepresented in the signal. This is
    a deployment-specific validity concern independent of benchmark coverage. Confirmed
    by Freedom House 2024 reporting on 2023–2024 power outage disruptions to telecom
    services — [WEB-12].'
  analyst_digital_literacy: High — primary users are professional data and social
    analysts at international organizations with full digital tool proficiency.
institutional_landscape:
  primary_humanitarian_actors:
    international:
    - UN OCHA Ecuador
    - International Federation of Red Cross and Red Crescent Societies (IFRC)
    - Cruz Roja Ecuatoriana (Red Cross Ecuador)
    - UNICEF Ecuador
    - WFP Ecuador
    - IOM Ecuador
    national_emergency_management:
    - name: Secretaría Nacional de Gestión de Riesgos y Emergencias (SNGRE / commonly
        SGR)
      role: Primary national emergency management authority; issues official alerts,
        activation levels, situation reports (SITREP), and COE National resolutions.
        Official website confirmed active as of January 2026 with regular COE National
        resolutions posted — [WEB-15].
      twitter_presence: SGR maintains a verified Twitter/X presence (linked from official
        website alongside Facebook, YouTube, Flickr). The official website header
        links to Twitter — [WEB-15]. Specific handle
        verification requires direct platform check; the institution is confirmed
        active on social media.
      open_data: 'SGR publishes open geospatial event data at national, province,
        cantón, and parroquia levels for events 2010–2023 via Ecuador Open Data portal
        — [WEB-1]. This is a net-new field:
        this dataset is a potential ground-truth reference for training and validating
        geographic entity anchoring.'
    - name: Cuerpo de Bomberos
      role: Municipal firefighting and emergency response; separate corps per cantón
      note: References in tweets typically specify the cantón-level corps (e.g., Bomberos
        Quito, Bomberos Guayaquil)
    - name: Policía Nacional del Ecuador
      role: Law enforcement; disaster perimeter control, evacuation enforcement
      twitter_presence: '[NEEDS VERIFICATION — deferred: below search budget]'
    - name: Fuerzas Armadas del Ecuador
      role: Military support to civilian emergency management; logistics and search
        and rescue
      twitter_presence: '[NEEDS VERIFICATION — deferred: below search budget]'
    - name: Ministerio de Salud Pública (MSP)
      role: Health emergency response, epidemiological monitoring, medical supply
        coordination
      twitter_presence: '[NEEDS VERIFICATION — deferred: below search budget]'
    - name: Secretaría Nacional de Planificación (SENPLADES / successor)
      role: 'SENPLADES was restructured; the planning function was transferred to
        the Secretaría Nacional de Planificación (SNP) under Decreto Ejecutivo 3 (2021),
        which reorganised executive branch entities. Crisis coordination role is secondary
        to SGR. Note: the SNGRE acronym (Servicio Nacional de Gestión de Riesgos y
        Emergencias) reflects an earlier rename of SGR; the entity currently operates
        as Secretaría Nacional de Gestión de Riesgos (SGR) — confirmed via official
        website — [WEB-15]. The prior SNGRE acronym
        still appears in some official resolutions (e.g., Resolución SNGRE-028-2019).'
    municipal_and_prefectural: Governments of affected cantones and provincias (GAD
      municipales and GAD provinciales) frequently post updates; analysts must disambiguate
      official municipal accounts from citizen accounts using similar geographic handles.
    note: System must correctly anchor tweets mentioning these actors to their institutional
      identity and geographic jurisdiction — rough regional geolocation is insufficient
      per the elicitation.
  humanitarian_coordination_mechanism:
    cluster_system: 'Ecuador activates COE (Comité de Operaciones de Emergencia) at
      national and cantonal levels during emergencies; COE Nacional resolutions are
      regularly published by SGR. The UN cluster system (Health, WASH, Shelter, Food
      Security, Logistics, Emergency Telecommunications) is activated during large-scale
      emergencies by OCHA Ecuador in coordination with SGR. COE Nacional activation
      is confirmed as the primary coordination mechanism, with UN clusters supplementary
      for international response. Source: SGR official site COE Nacional resolutions
      — [WEB-16].'
    sitrep_cadence: '[NEEDS VERIFICATION — deferred: below search budget. SITREP products
      are referenced on SGR website (Informes de Situación listed under transparency)
      but cadence during active emergencies was not confirmed in searches — [WEB-15]]'
    data_sharing_frameworks: 'Ecuador has an active COD-AB (Common Operational Dataset
      — Administrative Boundaries) on the Humanitarian Data Exchange (HDX), covering
      administrative levels 0–3 (national through parroquia), sourced from INEC and
      reviewed for accuracy in December 2024. This is the authoritative P-code reference
      for humanitarian operations and is maintained by OCHA ROLAC (Latin America and
      Caribbean). ReliefWeb actively covers Ecuador emergencies. Source: HDX Ecuador
      COD-AB — [WEB-17].'
crisis_taxonomy_for_deployment:
  prioritization_principle: Events are prioritized by population impact and response-gap
    severity, not by disaster category alone. Compound and socio-political crises
    are in scope alongside natural hazards.
  hazard_types_with_ecuadorian_context:
    volcanic:
      key_volcanoes: 'Ecuador''s active volcanoes most relevant for disaster response
        include: Cotopaxi (eruption alerts issued repeatedly; SGR has dedicated self-protection
        guides), Tungurahua (historically active; currently in reduced-activity phase),
        Reventador (persistently active in Napo/Sucumbíos), Sangay (active, Morona
        Santiago), and Pichincha/Guagua Pichincha (near Quito metro). SGR publishes
        official hazard guides for Cotopaxi specifically — [WEB-2].
        Current activity status requires real-time monitoring via IGEPN (Instituto
        Geofísico de la Escuela Politécnica Nacional).'
      typical_affected_zones: '[NEEDS VERIFICATION — deferred: official hazard zone
        maps at parroquia/cantón level per volcano are published by IGEPN and SGR
        but were not retrieved within search budget. See SGR geoportal — [WEB-18]
        for parroquia-level hazard zone data]'
    seismic:
      note: Ecuador sits on the Pacific Ring of Fire; major earthquakes (e.g., 2016
        Manabí earthquake) generate large tweet volumes with precise location references
      relevant_faults_and_zones: '[NEEDS VERIFICATION — deferred: below search budget.
        IGEPN maintains fault zone data; SGR open event data includes seismic events
        by province/cantón/parroquia 2010–2023 — [WEB-1]]'
    flooding_landslides:
      seasonal_pattern: '[NEEDS VERIFICATION — deferred: below search budget. La Niña/El
        Niño influence on Ecuadorian flooding seasons is well-documented in academic
        literature but specific seasonal parameters were not retrieved. Costa region
        flooding peaks roughly December–May; Sierra landslides tied to rainy seasons.
        SGR guidance documents reference época lluviosa — [WEB-2]]'
      historically_affected_provinces: Manabí (confirmed by SGR COE alerts including
        Resolución SNGRE-020-2019 Alerta Roja Cantón Portoviejo), Napo, Pastaza (Amazon
        flooding), Esmeraldas, El Oro, Loja, Bolívar (vulnerability analysis confirmed),
        Santa Elena, Chimborazo confirmed in SGR news and resolutions — [WEB-16];
        [WEB-1].
    socio_political:
      examples: Social protests blocking road access, fuel or medicine supply chain
        disruptions, internal displacement from conflict or insecurity
      note: These events generate humanitarian needs structurally similar to natural
        disasters and must be captured by the system taxonomy.
    compound_crises: Cascading events (e.g., earthquake followed by landslide, flooding
      compounding pre-existing food insecurity) are operationally critical and may
      not be captured by single-hazard benchmarks.
  needs_dimensions_tracked:
  - Access to affected areas (road conditions, bridge status)
  - Health and medical supply needs
  - Water, sanitation, and hygiene (WASH)
  - Shelter and displacement
  - Food security
  - Protection (including gender-based violence risk elevation during displacement)
  - Telecommunications and power restoration
  - Evacuation and search-and-rescue status
tweet_signal_characteristics:
  input_register: Mixed informal-to-semi-formal Ecuadorian Spanish; crisis-time orthographic
    degradation expected
  signal_types_in_scope:
  - Eyewitness reports from affected populations
  - Official agency updates (SGR, municipal governments, Red Cross)
  - Journalist and media organization posts
  - NGO field volunteer reports
  - Retweets and quote-tweets that propagate information with potential distortion
  - Informal community radio or WhatsApp content transcribed to Twitter
  operational_relevance_signals:
    high_value_low_visibility_signals:
    - Road access status for rural communities (high operational value; may not trend)
    - Community-level water/food shortage reports in informal register
    - Local place names at parroquia or community level (not provincial capitals)
    note: Per elicitation, a tweet about road access to a rural community carries
      high operational value for an NGO coordinator even if it would score low by
      external annotation standards. This is a population-specific relevance calibration
      that no existing general-purpose benchmark is likely to encode.
  entity_types_requiring_anchoring:
  - Administrative units (provincia, cantón, parroquia, sector/barrio)
  - Emergency management institutions (SGR/SNGRE, Cuerpo de Bomberos by cantón)
  - Humanitarian organization branches (Cruz Roja Ecuador, UN OCHA Ecuador)
  - Infrastructure references (named roads, bridges, rivers, hospitals, health centers)
  - Kichwa-origin place and community names
  - Colloquial geographic shorthand specific to Ecuadorian users
  crisis_specific_abbreviations: 'Key confirmed abbreviations include: SGR (Secretaría
    de Gestión de Riesgos), SNGRE (prior acronym for same entity), COE (Comité de
    Operaciones de Emergencia — activated at national and cantonal levels), EDAN (Evaluación
    de Daños y Análisis de Necesidades), GAD (Gobierno Autónomo Descentralizado —
    used for municipal and provincial governments), MSP (Ministerio de Salud Pública),
    ARCOTEL (telecoms regulator, appears in connectivity-disruption tweets). Informal
    population abbreviations were not retrieved and require field analyst elicitation.
    Source: SGR official documentation and SNGRE resolutions — [WEB-15];
    [WEB-1].'
output_task_requirements:
  primary_output_type: Temporally ordered narrative timeline summarizing how affected
    populations' needs evolve over the course of a crisis event
  output_consumers: Inter-operational teams at Red Cross and UN OCHA; outputs feed
    into situation reports, coordination meeting briefings, and resource allocation
    decisions
  quality_dimensions:
  - Geographic anchoring precision (parroquia/cantón level where possible)
  - Institutional attribution accuracy (correct identification of responding agencies)
  - Temporal coherence (events correctly sequenced; phase transitions identified)
  - Operational relevance calibration (high-value low-visibility signals surfaced)
  - Humanitarian needs taxonomy coverage (all relevant needs dimensions represented)
  - Register sensitivity (informal signals not filtered out as noise)
  ground_truth_validation_structure: Inter-operational team consensus across field
    coordinators, social analysts, and domain experts; no single annotator archetype
    is authoritative
  no_analog_in_benchmark: The CNN/Daily Mail benchmark's Cloze entity fill-in task
    has no structural, ontological, or metric correspondence to this output requirement.
  closest_existing_benchmark: CrisisFACTS (McCreadie & Buntain, 2023) is the closest
    identified benchmark for crisis timeline building from social media, referenced
    in ACL 2025 proceedings — [WEB-19].
    However, CrisisFACTS is English-only and does not cover Spanish-language or Latin
    American events. No timeline generation benchmark for Spanish-language disaster
    tweets was identified. This is a confirmed documentation gap.
cultural_and_operational_norms:
  humanitarian_coordination_culture: UN OCHA cluster system norms; situation report
    conventions; information management standards (e.g., 3W — Who does What Where);
    need-gap framing rather than damage-only framing
  ecuadorian_social_media_norms: Twitter/X is used by both official actors and affected
    populations during crises; hashtag conventions for Ecuadorian emergencies are
    event-specific and may emerge organically within hours of an event onset
  indigenous_community_representation: Kichwa and other indigenous communities in
    Ecuador may be disproportionately affected by certain hazard types (highland volcanic,
    Amazon flooding) but underrepresented in the tweet stream; analysts must account
    for this survivorship bias in timeline interpretation
  trust_and_verification_norms: Humanitarian analysts apply source credibility judgment;
    official agency accounts (SGR, Cruz Roja) are weighted differently from unverified
    citizen accounts; the system must preserve or surface source metadata to support
    this judgment
  language_of_official_reporting: Spanish is the language of all official Ecuadorian
    emergency management communications; English is used in UN OCHA inter-agency reporting;
    system outputs may need to support bilingual workflows
infrastructure_and_technical_context:
  tweet_stream_access: '[NEEDS VERIFICATION — deferred: below search budget. Twitter/X
    API access terms for humanitarian organizations, real-time rate limits, and existing
    Ecuador-focused crisis monitoring pipelines at UN OCHA or Red Cross were not confirmed
    in searches. This requires direct inquiry with UN OCHA Centre for Humanitarian
    Data and/or IFRC data-for-good teams.]'
  existing_humanitarian_nlp_tools:
    crisis_tweet_corpora: 'CrisisNLP, HumAID, CrisisLex, and the consolidated CrisisBench
      dataset are the primary humanitarian tweet corpora. Key finding: all major corpora
      are English-only or English-dominant. HumAID covers 19 major disaster events
      (2016–2019) globally but its focus is on English tweets. CrisisBench consolidates
      CrisisLex (T6 and T26), CrisisNLP, SWDM2013, ISCRAM13, DRD, DSM, CrisisMMD,
      and AIDR data. CrisisLexT26 covers 26 crises (2012–2013). TREC-IS covers ~50k
      tweets with 25 information types and 4 priority levels. None of these corpora
      include Ecuador-specific events or Ecuadorian Spanish informal register. The
      multilingual CrisisBench-all-lang dataset includes non-English tweets with language
      detection tags, but Ecuador/Spanish event coverage is not confirmed. No Spanish-language
      or Latin American disaster tweet benchmark specifically targeting Ecuador was
      identified. Sources: CrisisNLP — [WEB-20]; HumAID — [WEB-21];
      CrisisBench multilingual — [WEB-22].'
    spanish_language_nlp_infrastructure: '[NEEDS VERIFICATION — deferred: below search
      budget. Spanish BERT/transformer models (e.g., BETO, RoBERTa-es) exist for general
      Spanish but their coverage of Ecuadorian dialect or crisis-time social media
      register has not been evaluated in searchable literature. This requires targeted
      search or stakeholder inquiry.]'
    kichwa_nlp_resources: 'Confirmed gap: Kichwa is an extremely low-resource language
      with no prior NLP resources before the 2024 Killkan ASR dataset. No tokenizer,
      NER system, or social-media entity recognizer for Kichwa-Spanish exists. This
      is a hard constraint for any system processing Kichwa-origin place names in
      Ecuadorian crisis tweets. Sources: Killkan — [WEB-8];
      IEEE Kichwa-Spanish MT — [WEB-9].'
    ecuador_ner_geolocation_tools: '[NEEDS VERIFICATION — deferred: below search budget.
      No NER or geotagging tool confirmed to cover Ecuador''s sub-national administrative
      hierarchy at parroquia level was identified. The HDX COD-AB for Ecuador (admin
      levels 0–3, reviewed December 2024) provides the authoritative P-code gazetteer
      that any such tool would need to reference — [WEB-17].
      Gazetteer-based lookup against this COD-AB is a feasible approach but no pre-built
      tool was found.]'
  humanitarian_data_platforms:
    hdx: 'Ecuador COD-AB (administrative boundary dataset, levels 0–3) is confirmed
      on HDX, sourced from INEC, reviewed for accuracy December 2024, with live geoservices
      via ITOS/USAID. This is the authoritative P-code reference for humanitarian
      operations and is directly relevant for geographic entity anchoring validation.
      Source: HDX — [WEB-17].'
    reliefweb: ReliefWeb actively covers Ecuador emergencies (confirmed from SGR website
      cross-references and standard OCHA practice). No Ecuador-specific ReliefWeb
      dataset inventory was retrieved within budget; direct verification available
      at [WEB-23].
    ocha_ecuador_resources: '[NEEDS VERIFICATION — deferred: below search budget.
      OCHA ROLAC (Latin America and Caribbean) maintains the Ecuador COD-AB on HDX;
      specific OCHA Ecuador information management products (3W, SITREP templates)
      were not retrieved. Contact: OCHA ROLAC at [WEB-24]]'
  device_and_connectivity_context_for_analysts: Primary users (NGO/IO analysts) work
    in professional office or field coordination hub environments with reliable internet
    access; no mobile-only or low-bandwidth constraint applies to the analyst-facing
    output interface.
regulatory_and_data_governance_context:
  ecuador_data_protection_law: 'Ecuador enacted the Ley Orgánica de Protección de
    Datos Personales (LOPDP) on 26 May 2021, with a two-year compliance window making
    it fully effective from 26 May 2023. A Reglamento (implementing regulation) was
    issued by Presidential Decree on 13 November 2023. The law aligns with GDPR standards
    and establishes requirements for consent, data security, and transparency. The
    Superintendencia de Protección de Datos Personales is the enforcement authority.
    Controllers processing data of Ecuadorian residents must register with the National
    Register of Personal Data Protection. Processing of social media data from crisis-affected
    populations for humanitarian purposes may invoke ''vital interest'' or ''legitimate
    interest'' lawful bases under the LOPDP Reglamento, but no specific humanitarian
    exemption equivalent to GDPR Article 9(2)(c) was confirmed; legal counsel is advised.
    Sources: DLA Piper Data Protection — [WEB-25];
    CLYM LOPDP summary — [WEB-26];
    LOPDP Reglamento (Decreto 904) — [WEB-27].'
  humanitarian_data_responsibility_principles: '[NEEDS VERIFICATION — deferred: below
    search budget. ICRC and OCHA data responsibility frameworks (ICRC Handbook on
    Data Protection, OCHA Data Responsibility Guidelines) are publicly available but
    their specific applicability to tweet-stream processing in Ecuador requires legal/policy
    review beyond web search scope.]'
  twitter_x_terms_of_service_for_humanitarian_use: '[NEEDS VERIFICATION — deferred:
    below search budget. Twitter/X API terms change frequently; current terms for
    humanitarian/research use require direct verification at [WEB-28]
    and via direct contact with Twitter/X''s academic/humanitarian access programs.]'
benchmark_gap_summary_for_this_population:
  note: This section summarizes the most deployment-critical gaps between the CNN/Daily
    Mail benchmark and the Ecuador humanitarian tweet analysis deployment. It is derived
    from the elicitation summary and provided for downstream search targeting.
  gaps:
  - gap_id: 1
    dimension: IF
    description: Benchmark is formal English news; deployment is informal-to-semi-formal
      Ecuadorian Spanish tweets with crisis abbreviations, non-standard orthography,
      and Kichwa entity tokens
    search_target: Ecuadorian Spanish crisis tweet NLP benchmark informal register
      social media disaster language model evaluation
    search_finding: No Ecuadorian Spanish crisis tweet benchmark exists. The major
      crisis NLP corpora (CrisisNLP, HumAID, CrisisLex, CrisisBench) are English-only
      or English-dominant. CrisisBench-all-lang includes multilingual data with language
      detection tags but Ecuador/Spanish event coverage is unconfirmed. This is a
      confirmed full gap with no mitigating resource identified.
  - gap_id: 2
    dimension: IC
    description: Benchmark content is US/UK institutional news with no Ecuadorian
      administrative, geographic, or institutional entity coverage
    search_target: Ecuador named entity recognition geolocation parroquia cantón SGR
      Cuerpo de Bomberos NLP sub-national
    search_finding: No NER or geolocation benchmark covering Ecuador's sub-national
      administrative hierarchy at parroquia level was identified. The HDX COD-AB Ecuador
      dataset (admin levels 0–3, updated December 2024) provides a P-code gazetteer
      that could support entity anchoring validation — [WEB-17]
      — but no pre-built NER tool leveraging it was found. This is a confirmed full
      gap.
  - gap_id: 3
    dimension: IC
    description: No coverage of Kichwa-Spanish entity mixing in place names and NER
      contexts
    search_target: Kichwa Spanish code-switching NLP entity recognition social media
      Ecuador indigenous language Twitter
    search_finding: Confirmed hard gap. Kichwa is extremely low-resource with no social-media
      NLP tools. The 2024 Killkan ASR dataset is the first NLP resource for Kichwa.
      Kichwa's agglutinative morphology creates context-dependent word forms not seen
      consistently across datasets. No Kichwa-Spanish entity recognizer, tokenizer,
      or code-switching tool for Twitter exists — [WEB-8];
      [WEB-9].
  - gap_id: 4
    dimension: IO
    description: Benchmark has no humanitarian crisis taxonomy; deployment requires
      compound and socio-political crisis classification scored by population impact
      and response-gap severity
    search_target: humanitarian crisis tweet classification benchmark Latin America
      CrisisNLP HumAID TREC-IS disaster taxonomy compound crises
    search_finding: 'HumAID, CrisisLex, TREC-IS, and CrisisBench provide humanitarian
      taxonomy frameworks (informative/humanitarian class labels, 25 TREC-IS information
      types, 4 priority levels). However, all are English-only. None cover socio-political
      crises or compound cascading events. TREC-IS is the richest taxonomy (multi-label,
      prioritised) but English-only and not Ecuador-specific. No Latin American or
      Spanish-language humanitarian taxonomy benchmark was found. Sources: CrisisNLP/HumAID
      — [WEB-21]; CrisisBench GitHub — [WEB-29].'
  - gap_id: 5
    dimension: OO + OF
    description: Benchmark output is Cloze entity fill-in; deployment requires temporally
      ordered multi-sentence narrative timeline generation
    search_target: timeline generation disaster response humanitarian NLP benchmark
      temporal summarization crisis event tracking annotation
    search_finding: CrisisFACTS (McCreadie & Buntain, 2023) is the closest identified
      benchmark for crisis timeline building from social media, referenced in ACL
      2025 (CrisisTS paper) — [WEB-19].
      CrisisTS (ACL 2025) further couples social media text with time-series data
      for crisis monitoring. Neither covers Spanish-language events or Ecuador specifically.
      Timeline generation for Spanish crisis tweets remains a confirmed open research
      gap.
  - gap_id: 6
    dimension: OC
    description: Benchmark labels are algorithmically generated from anglophone editorial
      conventions; deployment requires inter-operational team validation by field
      coordinators, social analysts, and domain experts
    search_target: humanitarian NLP annotation framework UN OCHA IFRC data-for-good
      inter-annotator agreement crisis relevance multi-role validation
    search_finding: HumAID used Amazon Mechanical Turk crowd annotation (not humanitarian
      field experts) — [WEB-21]. AIDR (Artificial
      Intelligence for Disaster Response, QCRI) involves domain-expert labeling in
      some configurations but no systematic inter-operational team validation (field
      coordinators + social analysts + domain experts jointly) was found in any existing
      benchmark. This multi-role validation structure is absent from all reviewed
      resources.
  - gap_id: 7
    dimension: IF
    description: Spanish-language disaster tweet corpora with informal register may
      not exist for Ecuador specifically
    search_target: CrisisLex Spanish disaster tweets corpus CrisisNLP Latin America
      Ecuador informal register social media emergency NLP benchmark
    search_finding: Confirmed absence. No Spanish-language disaster tweet corpus for
      Ecuador or Latin America was identified in CrisisNLP, CrisisLex, HumAID, or
      CrisisBench. The CrisisBench-all-lang multilingual variant may contain some
      Spanish-language data (language-detected) but its coverage of Ecuador-specific
      events is unconfirmed — [WEB-22].
      This is a confirmed documentation gap.
net_new_fields:
  sgr_open_data_geoportal: 'The Secretaría Nacional de Gestión de Riesgos (SGR) publishes
    open geospatial hazard and event data at national, province, cantón, and parroquia
    levels for the period 2010–2023, including dangerous event records, safe zone
    locations, and vulnerability analyses, via Ecuador''s Open Data portal and the
    SGR Geoportal. This dataset is a high-value potential reference for training and
    validating geographic entity anchoring in crisis tweets. Source: Ecuador Open
    Data Portal / SGR — [WEB-1]; SGR Geoportal
    — [WEB-18].'
  ecuador_cod_ab_hdx: 'The HDX Ecuador COD-AB (Common Operational Dataset – Administrative
    Boundaries) covers administrative levels 0–3 (country, province, cantón, parroquia),
    sourced from INEC and reviewed December 2024. It includes P-codes and is maintained
    by OCHA ROLAC with live geoservices via ITOS/USAID. This is the authoritative
    reference for humanitarian geographic entity anchoring and NER validation. Source:
    HDX — [WEB-17].'
  ecuador_lopdp_compliance_status: 'Ecuador''s LOPDP became fully effective May 2023;
    implementing Reglamento issued November 2023. Humanitarian organisations processing
    tweet data from Ecuadorian crisis-affected populations should assess lawful processing
    bases (vital interest, legitimate interest) under the LOPDP and its Reglamento
    before deployment. The Superintendencia de Protección de Datos Personales is the
    enforcement authority. Source: CLYM — [WEB-26].'
  kichwa_agglutination_nlp_risk: 'Kichwa''s agglutinative morphology means words are
    formed by combining suffixes to lexical roots, creating context-dependent forms
    that do not appear consistently across datasets — a documented challenge for LLM-based
    NLP and content moderation confirmed by CDT research (2025). Combined with the
    near-total absence of Kichwa NLP resources, this means any system processing Kichwa-origin
    place names in Ecuadorian crisis tweets will have no linguistic grounding for
    those tokens. Source: CDT Quechua/Kichwa Social Media Report 2025 — [WEB-10].'
  crisisfacts_timeline_benchmark: 'CrisisFACTS (McCreadie & Buntain, 2023) is the
    only identified NLP benchmark targeting crisis timeline construction from social
    media data. It evaluates summarization and timeline quality but is English-only
    with no Spanish or Latin American event coverage. CrisisTS (ACL 2025) extends
    this by coupling text with multivariate time-series data. These are the methodologically
    closest existing resources to the deployment''s output task, but the gap to Ecuadorian
    Spanish informal register remains unbridged. Source: CrisisTS ACL 2025 — [WEB-19].'
```

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://datosabiertos.gob.ec/organization/sgr |
| WEB-2 | https://www.gestionderiesgos.gob.ec/biblioteca/ |
| WEB-3 | https://en.wikipedia.org/wiki/Provinces_of_Ecuador |
| WEB-4 | https://www.geopostcodes.com/country/ecuador/administrative-divisions/ |
| WEB-5 | https://en.wikipedia.org/wiki/Cantons_of_Ecuador |
| WEB-6 | https://grokipedia.com/page/List_of_cities_in_Ecuador |
| WEB-7 | https://storyteller.travel/map-provinces-ecuador/ |
| WEB-8 | https://arxiv.org/abs/2404.15501 |
| WEB-9 | https://ieeexplore.ieee.org/document/9532603/ |
| WEB-10 | https://cdt.org/wp-content/uploads/2025/06/2025-06-25-Quechua-Report-English-final.pdf |
| WEB-11 | https://www.statista.com/statistics/1322285/digital-illiteracy-ecuador/ |
| WEB-12 | https://freedomhouse.org/country/ecuador/freedom-net/2024 |
| WEB-13 | https://datareportal.com/reports/digital-2024-ecuador |
| WEB-14 | https://www.statista.com/statistics/1081753/smartphone-owners-ecuador/ |
| WEB-15 | https://www.gestionderiesgos.gob.ec/ |
| WEB-16 | https://www.gestionderiesgos.gob.ec/category/sgr/ |
| WEB-17 | https://data.humdata.org/dataset/cod-ab-ecu |
| WEB-18 | http://datosabiertos-gestionriesgosec.opendata.arcgis.com |
| WEB-19 | https://aclanthology.org/2025.acl-long.783.pdf |
| WEB-20 | https://crisisnlp.qcri.org/ |
| WEB-21 | https://crisisnlp.qcri.org/humaid_dataset |
| WEB-22 | https://huggingface.co/datasets/QCRI/CrisisBench-all-lang |
| WEB-23 | https://reliefweb.int/country/ecu |
| WEB-24 | https://www.unocha.org/latin-america-and-caribbean |
| WEB-25 | https://www.dlapiperdataprotection.com/index.html?t=law&c=EC |
| WEB-26 | https://www.clym.io/regulations/organic-law-on-the-protection-of-personal-data-lopdp-ecuador |
| WEB-27 | https://www.cosede.gob.ec/wp-content/uploads/2023/12/REGLAMENTO-GENERAL-A-LA-LEY-ORG%C3%81NICA-DE-PROTECCION-DE-DATOS-PERSONALES_compressed-1.pdf |
| WEB-28 | https://developer.twitter.com/en/developer-terms/policy |
| WEB-29 | https://github.com/firojalam/crisis_datasets_benchmarks |

---

## Expert Elicitation

## Elicitation Responses

Q1 [IO]: The benchmark under assessment covers a specific set of categories within its task domain. For your Ecuador-focused deployment, are there disaster types your users would prioritize — for example, volcanic eruptions (Cotopaxi, Tungurahua), landslides triggered by La Niña events, floods in coastal regions like Manabí, or earthquake aftershock sequences — that may fall outside the coverage of a general-purpose benchmark? Which crisis types matter most to Red Cross and UN OCHA coordinators in your context?
A1: The deployment focuses on large-scale social and humanitarian crises — those whose impact exceeds local response capacity — rather than any single disaster type. Users would prioritize events by population impact and response-gap severity, not by disaster category alone, meaning coverage must extend to compound and socio-political crises beyond natural hazards.

Q2 [IC]: Benchmarks in this domain often reference geographic markers and institutional handles tied to the cultural context in which they were built. In your deployment, location signals in tweets would reference Ecuadorian administrative units (parroquias, cantones, provincias), local emergency agencies (SGR, Cuerpo de Bomberos), and landmarks familiar to Ecuadorian users. Would your analysts expect the system to correctly anchor events to these local geographic and institutional references, or is rough regional-level geolocation sufficient?
A2: Analysts expect precise anchoring to Ecuador-specific entities — administrative units, local emergency agencies, and institutional actors — not merely rough regional-level geolocation.

Q3 [OC]: The benchmark's ground-truth labels and reference outputs were produced by annotators operating in a different cultural and operational context from your deployment. For your use case, relevance judgments may differ: a tweet about road access to a rural community, or an informal community radio broadcast transcribed into Twitter, might carry high operational value for an NGO coordinator but low value by external annotation standards. Who in your organization would serve as the authoritative judge of tweet relevance and summary quality — field coordinators, social analysts, or affected-community representatives — and do you have access to them for validation?
A3: Judgment authority rests with an inter-operational team rather than any single role; field coordinators, social analysts, and domain experts collectively determine relevance and summary quality. No single annotator archetype captures the authoritative standard.

Q4 [IF]: The benchmark's input signal may be drawn from a language and register different from your deployment context. Your deployment targets Ecuadorian Spanish, which may include code-switching with Kichwa or other indigenous languages, regional slang, informal abbreviations common in disaster contexts, and non-standard orthography in crisis conditions. Would the tweet stream your system processes be predominantly standard written Spanish, or do you expect significant informal register, dialect variation, or indigenous-language mixing?
A4: The input stream is predominantly Ecuadorian Spanish in a mixed informal-to-semi-formal register, with local indigenous-language terms appearing mainly in place and entity names. A system trained only on English social media (even if fine-tuned on generic Spanish) would likely miss dialect-specific and register-specific characteristics of Ecuadorian crisis-time social media.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark covers general English-language news comprehension via Cloze tasks; it has no coverage of humanitarian crisis taxonomy, Latin American disaster types, or socio-political emergency categories that drive operational relevance for NGO users. |
| IC | HIGH | Benchmark instances use US/UK news articles with Western geographic and institutional references; deployment requires anchoring to Ecuador-specific administrative units, local agencies, and informal disaster-register vocabulary — a profound content mismatch. |
| IF | HIGH | The benchmark is English text drawn from formal news; deployment data is informal-to-semi-formal Ecuadorian Spanish tweets, potentially mixing Kichwa entity names, non-standard orthography, and crisis-specific abbreviations — a language, register, and genre mismatch. |
| OO | HIGH | The benchmark's output ontology is Cloze-style entity fill-in, a classification/retrieval task; the deployment requires temporal timeline generation and operational relevance ranking, which are fundamentally different output structures with no correspondence to the benchmark's category space. |
| OC | HIGH | Benchmark labels were produced by automated conversion of CNN/Daily Mail summaries — non-representative of humanitarian operational judgment; deployment requires inter-operational team validation by field coordinators and domain experts assessing Ecuadorian crisis content. |
| OF | HIGH | The benchmark outputs entity labels (token-level answer fill-in); the deployment requires temporally ordered, narrative-form timeline summaries suited to NGO coordination workflows — the output form is categorically mismatched. |

---

## Dataset Analysis Findings

The following empirical findings were produced by automated profiling scripts that
sampled the benchmark's actual dataset on HuggingFace. Observations cite specific
datapoints using `DATASET-D{n}` IDs (e.g., QUAERO-D3). Both deployment-relevant
strengths and potential concerns are included; weigh CRITICAL-tagged concerns and
well-evidenced strengths accordingly when scoring the affected dimensions.

## Dataset Analysis Report

**Dataset(s):** abisee/cnn_dailymail (config 3.0.0)
**Analysis date:** 2025-07-14
**Examples reviewed:** 14 from `train` split
**Columns shown:** article, highlights, id
**Columns skipped (media):** none

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | cnn_dailymail | 1 | highlights | "A man named as a suspect in the fatal shooting of a Philadelphia, Pennsylvania, police officer last week was captured at a shelter in Miami, Florida" | US domestic crime reporting anchored to US cities and police institutions | IC |
| D2 | cnn_dailymail | 2 | highlights | "Two U.S. Air Force F-15s escorted two Russian Bear long-range bombers out of an air exclusion zone off the coast of Alaska" | US/Russian military content; US geographic and institutional references only | IC |
| D3 | cnn_dailymail | 3 | highlights | "Pakistani President Pervez Musharraf orders troops to take a television station's equipment… Pakistani opposition leader Imran Khan says he's under house arrest" | South Asian political crisis coverage; anglophone editorial framing of non-Western event | IC, OC |
| D4 | cnn_dailymail | 4 | highlights | "British graphic artist's identity remains a mystery despite huge popularity. Feted by the art world and Hollywood celebrities count among his collectors." | UK arts/culture story; no crisis relevance | IO |
| D5 | cnn_dailymail | 5 | highlights | "State-run news agency: China orders an investigation by quality control agencies. Children who swallow the beads can become comatose or have seizures." | Consumer safety story; no humanitarian crisis taxonomy | IO |
| D6 | cnn_dailymail | 6 | highlights | "Frank Lloyd Wright wanted store magnate to sleep on porch. Salvador Dalí's stated ambitions were bigger than Napoleon's." | Personality/celebrity feature; entirely irrelevant to humanitarian deployment | IO |
| D7 | cnn_dailymail | 7 | highlights | "Erik Prince: 'There was definitely incoming small arms fire from insurgents'… Iraqi government says Blackwater guards killed 17, fired without provocation." | Iraq war contracting dispute; Western institutional actors, no Latin American context | IC |
| D8 | cnn_dailymail | 8 | highlights | "NEW: The 17-year-old suspect allegedly fired the fatal shot… Taylor died after being shot in home invasion last week." | US criminal case; no disaster/humanitarian content | IO |
| D9 | cnn_dailymail | 9 | highlights | "BUPA was founded in 1947 in response to plans to establish the NHS. The company's biggest base is in the UK but has customers in three continents." | UK/European healthcare company profile | IC |
| D10 | cnn_dailymail | 11 | highlights | "Air Force says 2 pilots in good condition after ejecting from plane. Emergency responders on scene of crash at Andersen Air Force Base." | US military aviation accident; Guam/US institutional context | IC |
| D11 | cnn_dailymail | 12 | highlights | "Queen Elizabeth opens Heathrow Airport's $8.6 billion new Terminal 5. The new building took more than 15 years to complete following protests." | UK infrastructure story; no crisis or Latin American relevance | IC |
| D12 | cnn_dailymail | 13 | highlights | "Laura Bush calls on Myanmar junta to 'step aside,' allow for a democracy. Military leaders must give up the 'terror campaigns' against its people." | US foreign policy commentary on Myanmar; anglophone editorial framing of political crisis | IC, OC |
| D13 | cnn_dailymail | 14 | highlights | "Police confiscate computers, examine information on Web sites. Gunman may have frequented the Westroads Mall, police say." | US mass shooting in Nebraska; no relevance to Ecuadorian crisis context | IO |
| D14 | cnn_dailymail | 3 | article | "The country is at a critical and dangerous juncture -- threatened by rising tensions and spreading terrorism, Musharraf said in a televised address to the nation after declaring martial law." | Political crisis description in formal English news register — contrasts with informal Ecuadorian Spanish tweet register | IF |
| D15 | cnn_dailymail | 1 | article | "Miami Police Officer Gil Gonzalez said Lewis 'had a Bible and was praying when we went to get him. He had a look of guilt, a look of shock.'" | Formal English journalistic prose; illustrates register mismatch with informal crisis tweets | IF |
| D16 | cnn_dailymail | 5 | article | "Scientists have found the highly popular holiday toy contains a chemical that, once metabolized, converts into the toxic 'date rape' drug GHB (gamma-hydroxy butyrate), Scott Wolfson, a spokesman with the U.S. Consumer Product Safety Commission (CPSC), told CNN." | Western institutional actor reference (CPSC); no analog to Ecuadorian emergency institutions (SGR, COE) | IC |
| D17 | cnn_dailymail | 9 | article | "BUPA is a leading healthcare company in the UK, Spain, Australia, Ireland, Hong Kong, Thailand, Malta and Saudi Arabia." | UK-centric healthcare company geography; Spain mentioned but in European commercial context, not Latin American crisis context | IC |
| D18 | cnn_dailymail | 7 | article | "There was no 'deliberate violence,' committed by Blackwater employees, he added. Still, when asked whether it is possible someone with Blackwater 'screwed up' in the incident, Prince replied, 'Certainly it's possible.'" | Direct quotation in US English journalism; illustrates that all content is English formal register | IF |
| D19 | cnn_dailymail | 13 | article | "U.S. first lady Laura Bush -- in a rare foray into foreign policy -- called on Myanmar's military junta to 'step aside'… in a commentary published in Wednesday's Wall Street Journal." | US foreign policy voiced through US media outlet; anglophone editorial framing of humanitarian crisis | OC |
| D20 | cnn_dailymail | 14 | article | "Hawkins fired more than 30 rounds, the police chief said. The shootings sent panicked holiday shoppers fleeing for cover." | US mass violence event; content type entirely absent from humanitarian timeline task requirements | IO |

---

### Deployment-Relevant Strengths

Given the categorical misalignment documented throughout the YAML and confirmed by every sampled example, the data shows essentially no deployment-relevant strengths for the Ecuador humanitarian tweet analysis use case. The one partial technical observation below is noted for completeness, but the evidentiary record does not support characterizing it as a meaningful asset.

#### Strength 1: Abstractive highlight-article pairing structure is formally analogous to summarization
- **Dimension(s):** OF
- **Observation:** The dataset encodes article–highlights pairs where highlights are abstractive summaries (not sentence extracts), which is structurally analogous to a summarization or timeline-entry generation task. The article and highlights fields are cleanly separated, making the format technically straightforward for evaluating whether a model can compress a document into key facts.
- **Deployment relevance:** This is the weakest possible form of structural relevance: the format is recognizable as a summarization benchmark, but the content, language, domain, output structure, and annotation methodology are all misaligned with the deployment. It provides no evidence that the benchmark would serve the timeline-generation use case.
- **Datapoint citations:**
  - [D1] Example 1 (cnn_dailymail, split=train): "Tip leads police to John Lewis at homeless shelter in Miami. Lewis is suspected in fatal shooting of Philadelphia Ofc. Charles Cassidy." — Highlights are abstractive and non-extractive, confirming the format, but the content is a US crime story with zero relevance to Ecuadorian crisis timelines.
  - [D5] Example 5 (cnn_dailymail, split=train): "State-run news agency: China orders an investigation by quality control agencies. Children who swallow the beads can become comatose or have seizures." — Highlights condense a multi-source news story into bullet facts, structurally similar to timeline entries, but the domain (Chinese toy safety recall) is entirely irrelevant.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Complete language mismatch — English only, no Spanish, no Kichwa
- **Dimension(s):** IF
- **Observation:** Every article and every highlight in all 14 sampled examples is monolingual English in formal journalistic register. The dataset HF metadata explicitly tags the dataset as `language:en` and `multilinguality:monolingual`. No Spanish-language content, no Ecuadorian dialect variation, no informal register, no crisis-time abbreviations, no Kichwa-origin entity tokens appear anywhere in the sample.
- **Deployment relevance:** The deployment processes Ecuadorian Spanish tweets in a mixed informal-to-semi-formal register, with Kichwa terms appearing in place and entity names. A benchmark with zero Spanish content cannot measure a system's ability to process the target input signal. This is a categorical, not marginal, misalignment.
- **Datapoint citations:**
  - [D14] Example 3 (cnn_dailymail, split=train): "The country is at a critical and dangerous juncture -- threatened by rising tensions and spreading terrorism, Musharraf said in a televised address to the nation after declaring martial law." — Formal English journalistic prose; no register overlap with informal Ecuadorian Spanish crisis tweets.
  - [D15] Example 1 (cnn_dailymail, split=train): "Miami Police Officer Gil Gonzalez said Lewis 'had a Bible and was praying when we went to get him. He had a look of guilt, a look of shock.'" — US English direct quotation in news article; no analog to informal tweet register.
  - [D18] Example 7 (cnn_dailymail, split=train): "There was no 'deliberate violence,' committed by Blackwater employees, he added." — US English formal prose; no Spanish, no dialect variation, no non-standard orthography.

#### CRITICAL Concern 2: No humanitarian crisis content — taxonomy entirely absent
- **Dimension(s):** IO
- **Observation:** Across all 14 examples, zero articles concern natural disasters, floods, volcanic eruptions, earthquakes, landslides, or humanitarian emergencies. Topics include a US police shooting (Ex. 1), a US-Russia military incident (Ex. 2), a Pakistani political crisis (Ex. 3), a British street artist (Ex. 4), a Chinese toy recall (Ex. 5), an egotists feature (Ex. 6), an Iraq contractor shooting (Ex. 7), two US criminal cases (Ex. 8, 10), a UK healthcare company (Ex. 9), a US military crash (Ex. 11), a Heathrow terminal opening (Ex. 12), a US foreign policy commentary (Ex. 13), and a US mall shooting (Ex. 14). Not a single example falls within the humanitarian crisis domain.
- **Deployment relevance:** The deployment requires a system that can identify, classify, and track humanitarian needs across disaster types prioritized by population impact and response-gap severity. No benchmark category exists for volcanic eruptions, seismic events, flooding, landslides, compound crises, or socio-political emergencies. The benchmark provides no signal for this task.
- **Datapoint citations:**
  - [D4] Example 4 (cnn_dailymail, split=train, label="British graphic artist's identity remains a mystery despite huge popularity"): — Arts/culture content with no crisis relevance whatsoever.
  - [D6] Example 6 (cnn_dailymail, split=train, label="Frank Lloyd Wright wanted store magnate to sleep on porch. Salvador Dalí's stated ambitions were bigger than Napoleon's."): — Personality feature; exemplifies the breadth of topic coverage that is entirely orthogonal to humanitarian crisis taxonomy.
  - [D8] Example 8 (cnn_dailymail, split=train, label="NEW: The 17-year-old suspect allegedly fired the fatal shot… Taylor died after being shot in home invasion last week."): — US criminal case; no disaster, no humanitarian needs, no geographic or institutional anchoring to Ecuador.
  - [D13] Example 14 (cnn_dailymail, split=train, label="Police confiscate computers, examine information on Web sites. Gunman may have frequented the Westroads Mall, police say."): — US mass shooting; no crisis taxonomy overlap.

#### CRITICAL Concern 3: No Ecuador-specific geographic or institutional entity coverage
- **Dimension(s):** IC
- **Observation:** All geographic references across all 14 examples are US, UK, or Western institutional locations (Philadelphia, Miami, Alaska, London, Heathrow, Omaha, Guam, Washington DC) or non-Latin American international locations (Pakistan, Iraq, Myanmar, China). No Ecuadorian province, cantón, parroquia, or community appears. No Ecuadorian emergency management institution (SGR, SNGRE, Cuerpo de Bomberos, COE, GAD) is referenced. No Latin American humanitarian organization branch (Cruz Roja Ecuatoriana, OCHA ROLAC) appears.
- **Deployment relevance:** Analysts require precise anchoring to Ecuador-specific administrative units and institutional actors. A system trained and evaluated on this benchmark has no exposure to the entity space it must handle in deployment. The gap extends to all sub-national administrative levels required for field coordination decisions (parroquia, cantón, provincia).
- **Datapoint citations:**
  - [D1] Example 1 (cnn_dailymail, split=train): "A man named as a suspect in the fatal shooting of a Philadelphia, Pennsylvania, police officer last week was captured at a shelter in Miami, Florida." — US city and police department references; no Latin American geography.
  - [D16] Example 5 (cnn_dailymail, split=train): "Scientists have found the highly popular holiday toy contains a chemical… Scott Wolfson, a spokesman with the U.S. Consumer Product Safety Commission (CPSC), told CNN." — US regulatory agency (CPSC); no analog to SGR, Cuerpo de Bomberos, or COE.
  - [D9] Example 9 (cnn_dailymail, split=train): "BUPA is a leading healthcare company in the UK, Spain, Australia, Ireland, Hong Kong, Thailand, Malta and Saudi Arabia." — Spain mentioned only in a European corporate context; no Ecuadorian health or emergency institutions.
  - [D11] Example 12 (cnn_dailymail, split=train): "Queen Elizabeth opens Heathrow Airport's $8.6 billion new Terminal 5." — UK infrastructure; no relevance to Ecuador's sub-national emergency management geography.

#### CRITICAL Concern 4: Output task is extractive entity fill-in, not temporal narrative timeline generation
- **Dimension(s):** OO, OF
- **Observation:** The benchmark's output structure (for the reading comprehension task described in the YAML) is Cloze-style entity token prediction — selecting a single anonymized entity from a closed candidate set. The HuggingFace dataset as hosted is structured for summarization (article → highlights), but neither the Cloze entity fill-in nor the abstractive highlight format corresponds to temporally ordered, multi-sentence narrative timeline generation. No temporal sequencing, no needs-evolution tracking, no operational relevance ranking, and no humanitarian category labeling is present in any output field.
- **Deployment relevance:** The deployment requires temporally ordered narrative timelines suited to NGO coordination workflows — a fundamentally different output structure. The benchmark provides no evaluation signal for timeline coherence, geographic anchoring precision, institutional attribution accuracy, or humanitarian needs taxonomy coverage. Even if the summarization format were adopted, the summaries are of US/UK news stories without any temporal disaster-event sequencing.
- **Datapoint citations:**
  - [D1] Example 1 (cnn_dailymail, split=train, highlights="Tip leads police to John Lewis at homeless shelter in Miami."): — Four-bullet summary of a US crime story; no temporal ordering of evolving needs, no humanitarian phase transitions.
  - [D5] Example 5 (cnn_dailymail, split=train, highlights="State-run news agency: China orders an investigation by quality control agencies."): — Four-bullet summary of a product recall; no timeline structure, no population needs tracking.
  - [D3] Example 3 (cnn_dailymail, split=train, highlights="NEW: President Musharraf orders troops to take a television station's equipment."): — Political crisis highlights in English; no temporal evolution of humanitarian needs, no geographic anchoring to operational units.

#### CRITICAL Concern 5: Ground-truth labels algorithmically generated with no humanitarian validation
- **Dimension(s):** OC
- **Observation:** The HF metadata confirms `annotations_creators:no-annotation` — highlights are machine-extracted from CNN/Daily Mail bullet points with no human annotation. No field coordinator, social analyst, domain expert, or humanitarian professional was involved in any label generation. The authoritative quality standard is entirely determined by anglophone editorial conventions of two Western news organizations.
- **Deployment relevance:** The deployment's authoritative quality standard is inter-operational team consensus across field coordinators, social analysts, and domain experts collectively judging relevance and summary quality for Ecuadorian crisis content. The benchmark's automated label generation provides no approximation of this multi-role humanitarian validation structure. The two quality standards are not merely different in degree — they are structurally incompatible.
- **Datapoint citations:**
  - [D19] Example 13 (cnn_dailymail, split=train): "U.S. first lady Laura Bush -- in a rare foray into foreign policy -- called on Myanmar's military junta to 'step aside'… in a commentary published in Wednesday's Wall Street Journal." — Highlight generated from US media editorial framing of a political crisis; operational relevance judgment by Ecuadorian field coordinators would produce categorically different outputs for analogous content.
  - [D12] Example 13 (cnn_dailymail, split=train, highlights="Laura Bush calls on Myanmar junta to 'step aside,' allow for a democracy."): — The highlight reflects US foreign policy editorial priority; an inter-operational humanitarian team would foreground civilian casualty data, displacement figures, and access constraints rather than a US official's political statement.
  - [D3] Example 3 (cnn_dailymail, split=train): "Pakistani opposition leader Imran Khan says he's under house arrest." — Anglophone editorial judgment selects political actors as salient; humanitarian operational relevance would foreground affected population access and needs over political actors' statements.

---

#### MAJOR

#### MAJOR Concern 6: Western institutional and cultural knowledge assumed throughout
- **Dimension(s):** IC
- **Observation:** Articles consistently assume familiarity with US and UK institutions, geographic conventions, and cultural references: the NFL (Ex. 8, 10), US Air Force base names (Elmendorf, Andersen, Eglin — Ex. 2, 11), US political figures (Laura Bush, Condoleezza Rice — Ex. 13), British cultural figures (Banksy, Queen Elizabeth — Ex. 4, 12), and Western legal and media institutions. No Latin American institutional context appears.
- **Deployment relevance:** A system benchmarked on this dataset will have learned entity and context associations rooted entirely in US/UK institutional knowledge. When applied to Ecuadorian crisis tweets referencing SGR, SNGRE, COE, GAD municipales, IGEPN, or Cruz Roja Ecuatoriana, the system's learned representations will have no grounding in these entities.
- **Datapoint citations:**
  - [D2] Example 2 (cnn_dailymail, split=train): "Two U.S. Air Force F-15s escorted two Russian Bear long-range bombers out of an air exclusion zone off the coast of Alaska, U.S. military officials said Wednesday." — US military institutional framing; no analog to Ecuadorian emergency management chain.
  - [D7] Example 7 (cnn_dailymail, split=train): "Blackwater CEO Erik Prince said Sunday that guards 'definitely' faced insurgent fire September 16." — US private military contractor context; no Latin American institutional analog.
  - [D11] Example 12 (cnn_dailymail, split=train): "Queen Elizabeth helped launch Heathrow's $8.6 billion new Terminal 5 on Friday." — UK monarchy and infrastructure; no relevance to Ecuadorian deployment context.

#### MAJOR Concern 7: Formal written English register categorically mismatched with informal Ecuadorian Spanish tweet stream
- **Dimension(s):** IF
- **Observation:** All 14 articles are written in formal journalistic English prose with complete sentences, standard punctuation, institutional attribution, and no orthographic variation. This is the maximum possible register distance from informal crisis-time Ecuadorian Spanish tweets, which feature truncated sentences, phonetic spelling, missing diacritics, crisis-specific abbreviations (SGR, COE, EDAN, GAD), and Kichwa-origin place name tokens.
- **Deployment relevance:** A system calibrated on this benchmark's register would likely treat informal tweet-style inputs as out-of-distribution noise, potentially filtering out the high-value low-visibility signals (road access reports, community water shortages in informal register) that the deployment specifically requires to surface.
- **Datapoint citations:**
  - [D14] Example 3 (cnn_dailymail, split=train): "The country is at a critical and dangerous juncture -- threatened by rising tensions and spreading terrorism, Musharraf said in a televised address to the nation after declaring martial law." — 30-word formal clause with institutional attribution; contrast with a hypothetical tweet: "sgr activa alerta roja en Portoviejo #Manabí inundaciones sectorElVerano sin agua."
  - [D15] Example 1 (cnn_dailymail, split=train): "Miami Police Officer Gil Gonzalez said Lewis 'had a Bible and was praying when we went to get him. He had a look of guilt, a look of shock.'" — Formal attributed quotation; no register overlap with crisis tweet shorthand.

---

#### MINOR

#### MINOR Concern 8: Article length (averaging hundreds of tokens) is architecturally mismatched with tweet-length inputs
- **Dimension(s):** IF
- **Observation:** Sampled articles are long-form news texts ranging from approximately 200 to over 1,000 words. Example 3 (Pakistan martial law) runs to several thousand characters. The benchmark is explicitly designed for documents averaging 763 tokens. Tweet inputs average 280 characters (approximately 40–60 tokens).
- **Deployment relevance:** A model architecture benchmarked on 763-token documents and optimized for that length distribution will not generalize directly to tweet-length inputs without architectural adaptation. The YAML documentation notes that the benchmark's own performance analysis shows sensitivity to document length (Q78), but the relevant regime for tweets is far shorter than anything in this dataset.
- **Datapoint citations:**
  - [D14] Example 3 (cnn_dailymail, split=train): "Hours after declaring a state of emergency Saturday, Pakistani President Pervez Musharraf ordered troops to take a television station's equipment and put a popular opposition leader under house arrest…" — Multi-paragraph article of approximately 1,200+ words; no architectural overlap with sub-100-token tweet processing.

#### MINOR Concern 9: No temporal sequencing or event-phase structure in any output
- **Dimension(s):** OO
- **Observation:** The highlights fields across all 14 examples are unordered bullet-point summaries with no timestamp, no event-phase label, no before/after sequencing, and no indication of evolving states. Even in the Pakistan martial law example (Ex. 3), which covers a dynamic political crisis, the highlights are a flat list of discrete facts without temporal ordering.
- **Deployment relevance:** The deployment requires not just summarization but temporal ordering of how affected populations' needs evolve — identifying phase transitions (e.g., from search-and-rescue to shelter to WASH needs). The complete absence of temporal structure in any benchmark output means this dimension of the deployment task has no analog in the benchmark at all.
- **Datapoint citations:**
  - [D3] Example 3 (cnn_dailymail, split=train, highlights="NEW: President Musharraf orders troops to take a television station's equipment. Pakistani opposition leader Imran Khan says he's under house arrest. President Musharraf says his actions are for the good of the country. White House calls Musharraf's emergency declaration 'disappointing'."): — Four unordered facts; no temporal sequencing, no phase-transition labels, no needs-evolution tracking structure.

---

### Content Coverage Summary

All 14 sampled examples are drawn from CNN and Daily Mail news articles covering US domestic crime and law enforcement (Examples 1, 8, 10, 14), US and allied military affairs (Examples 2, 11), non-Western political crises reported through US/UK editorial lens (Examples 3, 13), UK and European culture and business (Examples 4, 9, 12), US-adjacent international consumer safety (Example 5), Western celebrity/arts features (Example 6), and the Iraq War as covered by US media (Example 7). Every article is monolingual formal English. Geographic references are exclusively US, UK, and Western-allied institutional locations. No Latin American, Ecuadorian, or Spanish-language content appears in any form. No humanitarian disaster, natural hazard, emergency response, or crisis taxonomy content appears. Ground-truth highlights are algorithmically derived from editorial bullet points with no human annotation. The output structure is flat, unordered bullet summaries with no temporal sequencing. The content is entirely consistent with what the YAML documentation describes — and entirely misaligned with every priority dimension of the Ecuador humanitarian tweet analysis deployment.

---

### Limitations

- **Sample size:** 14 examples from a 287,113-example training split. While every sampled example is categorically misaligned with the deployment, the sample cannot confirm the precise distribution of topic categories across the full dataset. However, given the documented source constraint (CNN and Daily Mail articles, 2007–2015, English-only), there is no plausible mechanism by which Ecuador-specific, Spanish-language, or humanitarian crisis content could appear in any portion of the dataset.
- **Config version:** Only config `3.0.0` (summarization format) was sampled. Configs `1.0.0` and `2.0.0` may differ in preprocessing but share the same underlying article corpus and therefore the same language, geographic, and domain coverage constraints.
- **Cloze task not directly observable:** The HuggingFace dataset as hosted presents the summarization version (article + highlights), not the original Cloze entity fill-in version described in the benchmark paper. The entity anonymization procedure (replacing named entities with abstract markers like `ent5`, `ent85`) is not visible in the sampled data. This does not affect the validity assessment — both the summarization and Cloze versions share the same fundamental misalignments — but the specific anonymization artifacts described in the YAML cannot be directly observed in this sample.
- **Temporal range not confirmed in sample:** The YAML documents articles from April 2007 to April 2015. The sample does not include date metadata, so the temporal distribution of the 14 examples cannot be confirmed. This is not material to the validity assessment.
- **No Spanish-language content possible:** The confirmed monolingual English constraint (HF metadata `language:en`, `multilinguality:monolingual`) means no amount of additional sampling would surface Spanish-language content. The absence is structural, not a sampling artifact.

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
  "benchmark": "cnn_dailymail_rc",
  "region": "Ecuador Humanitarian Crisis Tweet Analysis — NGO/IO Analyst Deployment",
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
