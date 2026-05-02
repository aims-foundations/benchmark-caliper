```markdown
# Validity Extraction: Teaching Machines to Read and Comprehend
<!-- Model routing: Haiku (per-page extraction) → script (registry assembly) → Sonnet (narrative) -->

## Metadata
- **Title**: Teaching Machines to Read and Comprehend
- **Authors**: Karl Moritz Hermann, Tomáš Kočiský, Edward Grefenstette, Lasse Espeholt, Will Kay, Mustafa Suleyman, Phil Blunsom
- **Venue/Year**: Neural Information Processing Systems (NeurIPS) / 2015
- **Total Pages**: 12
- **Quotes Extracted**: 88

## Narrative Context

Interpretive prose organized by extraction category. Each factual claim references quote IDs from the registry. **This section is non-authoritative — it provides readability but is not evidence. Only the Quote Registry contains verbatim text from the paper.**

---

### 1. Task Taxonomy / Test Case Categories

The benchmark is structured around a single, unified task type: machine reading comprehension evaluated via Cloze-style fill-in-the-blank queries, formalized as estimating the conditional probability p(a|c, q) over a context document, query, and answer [Q10]. The paper explicitly frames this as a supervised learning problem designed to measure a model's ability to detect and understand linguistic relationships between entities within a single document, deliberately excluding world knowledge or co-occurrence statistics as confounds [Q11, Q17]. The anonymization and entity-permutation procedure reinforces this focus: by replacing named entities with abstract markers, the task is designed so that "the only remaining strategy for answering questions is to do so by exploiting the context presented with each question" [Q20], which the authors argue makes performance a pure measure of reading comprehension capability. Several model architectures are taxonomized within this framing — Deep LSTM Readers [Q39, Q44], Attentive Readers, and Impatient Readers [Q54] — with the paper also benchmarking traditional frame-semantic and NLP pipeline approaches [Q23, Q24] as comparative baselines.

From the standpoint of the Ecuador humanitarian deployment, this task taxonomy represents a profound mismatch across every axis of operational relevance. The benchmark covers only English-language news comprehension via entity retrieval [Q1, Q2]; it has no categories corresponding to humanitarian crisis types, disaster response workflows, socio-political emergency classification, or the compound-crisis scenarios that NGO analysts prioritize. There is no temporal reasoning or event-sequencing component [Q41] — the task is a single-document, single-answer lookup — whereas the deployment requires generating temporally ordered timelines tracking how affected populations' needs evolve. The paper's own taxonomy of "traditional NLP vs. neural models" [Q55] and its emphasis on LSTM sequence modeling for long documents [Q38, Q44, Q80] provide no coverage of the information extraction and summarization structures that humanitarian coordination demands.

---

### 2. Data Sources and Collection

The benchmark data is drawn entirely from two English-language Western news outlets: CNN and the Daily Mail [Q4]. Specifically, approximately 93,000 CNN articles and 220,000 Daily Mail articles were collected, spanning from April 2007 and June 2010 respectively through April 2015 [Q14], producing roughly one million document–query–answer triples [Q16]. Articles were filtered to exclude those exceeding 2,000 tokens or whose answer entity did not appear in the context document, and validation and test splits were assigned by publication month in early 2015 [Q9]. The data pipeline is entirely automated — no human crowdsourcing, expert annotation, or community-sourced collection is involved; bullet-point summaries published by the news outlets themselves are algorithmically converted into Cloze queries [Q14, Q16].

For the Ecuador deployment, this data sourcing represents a critical content gap. The source corpus is rooted in US/UK institutional news register, Western geographic references, and English-language journalistic conventions — with zero coverage of Latin American administrative structures, Ecuadorian emergency agencies, informal Spanish social media register, or indigenous-language entity names. The automated extraction methodology, while enabling scale, produces labels that reflect the editorial judgment of anglophone journalists, not the operational relevance judgments of humanitarian field coordinators or affected Ecuadorian communities.

---

### 3. Data Format and Preprocessing

Input instances are structured as (context document, query, answer) triples, where the query is a Cloze-style sentence derived from an abstractive bullet-point summary with one entity replaced by a placeholder [Q3, Q16]. A key preprocessing step is entity anonymization and random permutation: coreference resolution is used to cluster entity mentions, all named entities are replaced with abstract markers (e.g., ent5, ent85), and these markers are randomly shuffled at each data load [Q18]. This design forces models to rely on document-internal context rather than world knowledge, as illustrated by the contrast between anonymized and non-anonymized versions of the same query [Q19]. Documents average 763 tokens and 27 entities in the CNN validation set [Q76], and frame-semantic model variants additionally require unanonymized text for parser compatibility [Q26, Q25, Q28, Q30].

The input format is formal, written English text from a structured news domain — a genre and language that are categorically misaligned with the deployment context. The deployment processes informal-to-semi-formal Ecuadorian Spanish tweets, potentially mixing Kichwa or other indigenous-language terms in place and entity names, crisis-specific abbreviations, and non-standard orthography [Elicitation Q4]. The anonymization procedure [Q18] is particularly relevant to note: while it was designed to isolate reading comprehension from world-knowledge confounds in English news, it would entirely suppress the dialect-specific, register-specific, and indigenous-language entity signals that are diagnostically important for anchoring events to Ecuadorian geographic and institutional references. The Deep LSTM architecture's handling of long sequences [Q40, Q42, Q43, Q46, Q47, Q48] and its sensitivity to document length [Q78] also raise questions about applicability to short, fragmented tweet-length inputs.

---

### 4. Label Categories and Output Types

NOT DOCUMENTED: The paper contains no dedicated discussion of a label ontology or output category schema beyond the implicit structure of the Cloze task itself — the "label" for each instance is a single entity token drawn from the context document's vocabulary. No structured label taxonomy, humanitarian category set, or multi-class output schema is described anywhere in the paper.

This absence is a validity-relevant finding for the Ecuador deployment. The deployment requires outputs structured as temporally ordered, operationally relevant narrative timeline summaries — a fundamentally different output ontology from token-level entity fill-in. The benchmark's implicit label space (a vocabulary of anonymized entity markers drawn from individual news documents) has no correspondence to any humanitarian coordination output structure, relevance tier, or event-type classification that NGO analysts would use.

---

### 5. Annotation Process

NOT DOCUMENTED: The paper is entirely silent on human annotation. There are no annotators in the traditional sense — the ground-truth answers are generated algorithmically by replacing entities in machine-extracted bullet-point summaries [Q16], not by human judgment. No annotator demographics, inter-annotator agreement statistics, or human quality assurance procedures are described anywhere in the paper.

This absence is a critical validity-relevant finding for the Ecuador deployment. The deployment's authoritative quality standard rests with an inter-operational team of field coordinators, social analysts, and domain experts who collectively judge relevance and summary quality for Ecuadorian crisis content [Elicitation Q3]. The benchmark's automated label generation, rooted in anglophone editorial conventions, provides no approximation of this multi-role humanitarian validation structure — and there is no mechanism within the benchmark's design to incorporate the kind of community-representative or operationally-grounded annotation that the deployment context demands.

---

### 6. Evaluation Metrics and Output Modality

The benchmark evaluates models using classification accuracy over a closed entity set — the model must select the correct anonymized entity token from those appearing in the context document [Q34]. Multiple baselines are defined: majority-frequency entity selection [Q22], word-distance alignment [Q32, Q33], frame-semantic rule-based heuristics tuned iteratively on validation data [Q29, Q31], and neural models whose attention weights are interpreted as soft probability distributions over document tokens [Q49, Q50, Q51]. Hyperparameters for all neural models were tuned on validation sets [Q58, Q60, Q61, Q62], and performance is reported as accuracy on held-out test sets [Q59]. The paper also analyzes performance as a function of document length [Q78] and visualizes attention heat maps to interpret model behavior on correctly and incorrectly answered queries [Q79, Q85, Q86, Q87, Q88], finding that attention-based models outperform pure LSTM approaches [Q72, Q73].

For the Ecuador deployment, this evaluation framework is categorically mismatched with operational needs. The output modality is a single discrete entity label per query — not a temporally ordered narrative summary, not an operational relevance ranking, and not a multi-sentence synthesis of evolving humanitarian conditions. The metric of entity-prediction accuracy has no analog in timeline quality assessment. The attention visualization work [Q88] and the analysis of semantic propagation over long documents [Q72] are intellectually interesting but do not translate to metrics for evaluating timeline coherence, geographic anchoring accuracy, or operational relevance as judged by NGO coordinators.

---

### 7. Stated Limitations

The authors acknowledge several limitations relevant to generalizability. They note that prior work using synthetic narratives has historically failed to transfer to real environments because "such closed worlds inevitably fail to capture the complexity, richness, and noise of natural language" [Q6] — a criticism that, ironically, applies with even greater force to the benchmark's own anonymization procedure when evaluated against informal social media data. The training corpus limitation (prior corpora limited to hundreds of examples) is cited as a key motivation for the new dataset [Q12, Q13], but the solution remains narrowly scoped to English news. The frame-semantic pipeline is explicitly flagged as having poor coverage due to PropBank parser limitations [Q64] and poor scalability to multi-sentence inference [Q66, Q67], with the authors predicting significantly worse performance "on other types of machine reading data where questions rather than Cloze queries are used" [Q68].

Additional limitations bear directly on deployment validity. The fixed-width hidden vector in LSTM models is acknowledged as an information bottleneck [Q45], and memory constraints prevented experimentation with deeper attentive architectures [Q69]. The paper explicitly flags ambiguous queries as a failure mode [Q81, Q82] — particularly for geographic location queries where the anonymization process makes it impossible to distinguish between administrative levels (neighborhood, town, region, country) [Q82] — a problem that would be severely amplified in an Ecuadorian context where precise sub-national anchoring (parroquia, cantón, provincia) is operationally critical. The authors also acknowledge that "many queries requiring complex inference and long range reference resolution" remain unsolved [Q75], and that incorporating world knowledge and multi-document queries would require fundamentally different architectures [Q74] — both of which are baseline requirements for the Ecuador deployment's timeline generation task.

---

### 8. Authors and Affiliations

All seven authors are affiliated with Google DeepMind and/or the University of Oxford [Q8]: Karl Moritz Hermann, Tomáš Kočiský, Edward Grefenstette, Lasse Espeholt, Will Kay, Mustafa Suleyman, and Phil Blunsom. This institutional provenance signals a UK/US academic-industrial research context focused on advancing neural NLP capabilities for English-language comprehension tasks. There is no indication of collaboration with Latin American institutions, humanitarian organizations, or Spanish-language NLP communities — affiliations that would be relevant for assessing whether the benchmark's design choices reflect any awareness of deployment contexts like the Ecuador humanitarian scenario described in the elicitation summary.
```

---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | task_taxonomy | "Machine reading systems can be tested on their ability to answer questions posed on the contents of documents that they have seen, but until now large scale training and test datasets have been missing for this type of evaluation." |
| Q2 | 1 | task_taxonomy | "In this work we define a new methodology that resolves this bottleneck and provides large scale supervised reading comprehension data." |
| Q3 | 1 | data_format | "We observe that summary and paraphrase sentences, with their associated documents, can be readily converted to context–query–answer triples using simple entity detection and anonymisation algorithms." |
| Q4 | 1 | data_sources | "Using this approach we have collected two new corpora of roughly a million news stories with associated queries from the CNN and Daily Mail websites." |
| Q5 | 1 | stated_limitations | "While obtaining supervised natural language reading comprehension data has proved difficult, some researchers have explored generating synthetic narratives and queries [3, 4]." |
| Q6 | 1 | stated_limitations | "Historically, however, many similar approaches in Computational Linguistics have failed to manage the transition from synthetic data to real environments, as such closed worlds inevitably fail to capture the complexity, richness, and noise of natural language [5]." |
| Q7 | 1 | evaluation_metrics | "These models draw on recent developments for incorporating attention mechanisms into recurrent neural network architectures [6, 7, 8, 4]." |
| Q8 | 1 | authors_affiliations | "Karl Moritz Hermann, Tomáš Kočiský, Edward Grefenstette, Lasse Espeholt, Will Kay, Mustafa Suleyman, Phil Blunsom are from Google DeepMind and University of Oxford." |
| Q9 | 2 | data_sources | "Articles were collected starting in April 2007 for CNN and June 2010 for the Daily Mail, both until the end of April 2015. Validation data is from March, test data from April 2015. Articles of over 2000 tokens and queries whose answer entity did not appear in the context were filtered out." |
| Q10 | 2 | task_taxonomy | "The reading comprehension task naturally lends itself to a formulation as a supervised learning problem. Specifically we seek to estimate the conditional probability p(a\|c, q), where c is a context document, q a query relating to that document, and a the answer to that query." |
| Q11 | 2 | task_taxonomy | "For a focused evaluation we wish to be able to exclude additional information, such as world knowledge gained from co-occurrence statistics, in order to test a model's core capability to detect and understand the linguistic relationships between entities in the context document." |
| Q12 | 2 | stated_limitations | "Such an approach requires a large training corpus of document–query–answer triples and until now such corpora have been limited to hundreds of examples and thus mostly of use only for testing [9]." |
| Q13 | 2 | stated_limitations | "This limitation has meant that most work in this area has taken the form of unsupervised approaches which use templates or syntactic/semantic analysers to extract relation tuples from the document to form a knowledge graph that can be queried." |
| Q14 | 2 | data_sources | "We have collected 93k articles from the CNN and 220k articles from the Daily Mail websites. Both news providers supplement their articles with a number of bullet points, summarising aspects of the information contained in the article." |
| Q15 | 2 | data_format | "Of key importance is that these summary points are abstractive and do not simply copy sentences from the documents." |
| Q16 | 2 | data_format | "We construct a corpus of document–query–answer triples by turning these bullet points into Cloze [12] style questions by replacing one entity at a time with a placeholder. This results in a combined corpus of roughly 1M data points (Table 1)." |
| Q17 | 2 | task_taxonomy | "Note that the focus of this paper is to provide a corpus for evaluating a model's ability to read and comprehend a single document, not world knowledge or co-occurrence." |
| Q18 | 3 | data_format | "To prevent such degenerate solutions and create a focused task we anonymise and randomise our corpora with the following procedure, a) use a coreference system to establish coreferents in each data point; b) replace all entities with abstract entity markers according to coreference; c) randomly permute these entity markers whenever a data point is loaded." |
| Q19 | 3 | data_format | "Clearly a human reader can answer both queries correctly. However in the anonymised setup the context document is required for answering the query, whereas the original version could also be answered by someone with the requisite background knowledge." |
| Q20 | 3 | task_taxonomy | "Therefore, following this procedure, the only remaining strategy for answering questions is to do so by exploiting the context presented with each question. Thus performance on our two corpora truly measures reading comprehension capability." |
| Q21 | 3 | task_taxonomy | "Table 2 gives an indication of the difficulty of the task, showing how frequent the correct answer is contained in the top N entity markers in a given document. Note that our models don't distinguish between entity markers and regular words. This makes the task harder and the models more general." |
| Q22 | 3 | evaluation_metrics | "We define two simple baselines, the majority baseline (maximum frequency) picks the entity most frequently observed in the context document, whereas the exclusive majority (exclusive frequency) chooses the entity most frequently observed in the context but not observed in the query." |
| Q23 | 3 | task_taxonomy | "Traditionally, a pipeline of NLP models has been used for attempting question answering, that is models that make heavy use of linguistic annotation, structured world knowledge and semantic parsing and similar NLP pipeline outputs." |
| Q24 | 3 | task_taxonomy | "Frame-semantic parsing attempts to identify predicates and their arguments, allowing models access to information about "who did what to whom"." |
| Q25 | 4 | data_format | "makes use of frame-semantic annotations which we obtained by parsing our model with a state-of-the-art frame-semantic parser [13, 14]." |
| Q26 | 4 | data_format | "As the parser makes extensive use of linguistic information we run these benchmarks on the unanonymised version of our corpora." |
| Q27 | 4 | stated_limitations | "There is no significant advantage in this as the frame-semantic approach used here does not possess the capability to generalise through a language model beyond exploiting one during the parsing phase." |
| Q28 | 4 | data_format | "Extracting entity-predicate triples—denoted as (e1, V, e2)—from both the query q and context document d, we attempt to resolve queries using a number of rules with an increasing recall/precision trade-off as follows (Table 4)." |
| Q29 | 4 | evaluation_metrics | "Strategies are ordered by precedence and answers determined accordingly. This heuristic algorithm was iteratively tuned on the validation data set." |
| Q30 | 4 | data_format | "For reasons of clarity, we pretend that all PropBank triples are of the form (e1, V, e2). In practice, we take the argument numberings of the parser into account and only compare like with like, except in cases such as the permuted frame rule, where ordering is relaxed." |
| Q31 | 4 | evaluation_metrics | "In the case of multiple possible answers from a single rule, we randomly choose one." |
| Q32 | 4 | evaluation_metrics | "We consider another baseline that relies on word distance measurements. Here, we align the placeholder of the Cloze form question with each possible entity in the context document and calculate a distance measure between the question and the context around the aligned entity." |
| Q33 | 4 | evaluation_metrics | "We tune the maximum penalty per word (m = 8) on the validation data." |
| Q34 | 4 | evaluation_metrics | "We propose three neural models for estimating the probability of word type a from document d answering query q: p(a\|d, q) ∝ exp (W(a)g(d, q)), s.t. a ∈ V, where V is the vocabulary, and W(a) indexes row a of weight matrix W and through a slight abuse of notation word types double as indexes." |
| Q35 | 4 | task_taxonomy | "Note that we do not privilege entities or variables, the model must learn to differentiate these in the input sequence." |
| Q36 | 4 | data_format | "The function g(d, q) returns a vector embedding of a document and query pair." |
| Q37 | 4 | task_taxonomy | "Long short-term memory (LSTM, [18]) networks have recently seen considerable success in tasks such as machine translation and language modelling [17]." |
| Q38 | 4 | task_taxonomy | "When used for translation, Deep LSTMs [19] have shown a remarkable ability to embed long sequences into a vector representation which contains enough information to generate a full translation in another language." |
| Q39 | 4 | task_taxonomy | "Our first neural model for reading comprehension tests the ability of Deep LSTM encoders to handle significantly longer sequences." |
| Q40 | 4 | data_format | "We feed our documents one word at a time into a Deep LSTM encoder, after a delimiter we then also feed the query into the encoder. Alternatively we also experiment with processing the query then the document." |
| Q41 | 4 | task_taxonomy | "The result is that this model processes each document query pair as a single long sequence. Given the embedded document and query the network predicts which token in the document answers the query." |
| Q42 | 5 | data_format | "We employ a Deep LSTM cell with skip connections from each input x(t) to every hidden layer, and from every hidden layer to the output y(t):" |
| Q43 | 5 | data_format | "Thus our Deep LSTM Reader is defined by g^LSTM(d, q) = y(\|d\|+\|q\|) with input x(t) the concatenation of d and q separated by the delimiter \|\|\|." |
| Q44 | 5 | task_taxonomy | "The Deep LSTM Reader must propagate dependencies over long distances in order to connect queries to their answers." |
| Q45 | 5 | stated_limitations | "The fixed width hidden vector forms a bottleneck for this information flow that we propose to circumvent using an attention mechanism inspired by recent results in translation and image recognition [6, 7]." |
| Q46 | 5 | data_format | "This attention model first encodes the document and the query using separate bidirectional single layer LSTMs [19]." |
| Q47 | 5 | data_format | "The encoding u of a query of length \|q\| is formed by the concatenation of the final forward and backward outputs, u = −→yq (\|q\|) \|\| ←−yq (1)." |
| Q48 | 5 | data_format | "For the document the composite output for each token at position t is, yd(t) = −→yd(t) \|\| ←−yd(t)." |
| Q49 | 5 | evaluation_metrics | "The representation r of the document d is formed by a weighted sum of these output vectors." |
| Q50 | 5 | evaluation_metrics | "These weights are interpreted as the degree to which the network attends to a particular token in the document when answering the query:" |
| Q51 | 5 | evaluation_metrics | "The variable s(t) is the normalised attention at token t." |
| Q52 | 6 | evaluation_metrics | "Having described a number of models in the previous section, we next evaluate these models on our reading comprehension corpora." |
| Q53 | 6 | task_taxonomy | "Our hypothesis is that neural models should in principle be well suited for this task." |
| Q54 | 6 | task_taxonomy | "We expect that the attention-based models would therefore outperform the pure LSTM-based approaches." |
| Q55 | 6 | task_taxonomy | "Considering the second dimension of our investigation, the comparison of traditional versus neural approaches to NLP, we do not have a strong prior favouring one approach over the other." |
| Q56 | 6 | data_format | "The entity anonymisation and permutation aspect of the task presented here may end up levelling the playing field in that regard, favouring models capable of dealing with syntax rather than just semantics." |
| Q57 | 6 | evaluation_metrics | "With these considerations in mind, the experimental part of this paper is designed with a threefold aim. First, we want to establish the difficulty of our machine reading task by applying a wide range of models to it. Second, we compare the performance of parse-based methods versus that of neural models. Third, within the group of neural models examined, we want to determine what each component contributes to the end performance; that is, we want to analyse the extent to which an LSTM can solve this task, and to what extent various attention mechanisms impact performance." |
| Q58 | 6 | evaluation_metrics | "All model hyperparameters were tuned on the respective validation sets of the two corpora." |
| Q59 | 6 | evaluation_metrics | "Our experimental results are in Table 5, with the Attentive and Impatient Readers performing best across both datasets." |
| Q60 | 6 | evaluation_metrics | "For the Deep LSTM Reader, we consider hidden layer sizes [64, 128, 256], depths [1, 2, 4], initial learning rates [1E−3, 5E−4, 1E−4, 5E−5], batch sizes [16, 32] and dropout [0.0, 0.1, 0.2]. We evaluate two types of feeds. In the cqa setup we feed first the context document and subsequently the question into the encoder, while the qca model starts by feeding in the question followed by the context document. We report results on the best model (underlined hyperparameters, qca setup)." |
| Q61 | 6 | evaluation_metrics | "For the attention models we consider hidden layer sizes [64, 128, 256], single layer, initial learning rates [1E−4, 5E−5, 2.5E−5, 1E−5], batch sizes [8, 16, 32] and dropout [0, 0.1, 0.2, 0.5]." |
| Q62 | 6 | evaluation_metrics | "For all models we used asynchronous RmsProp [20] with a momentum of 0.9 and a decay of 0.95." |
| Q63 | 7 | stated_limitations | "While the one frame-semantic model proposed in this paper is clearly a simplification of what could be achieved with annotations from an NLP pipeline, it does highlight the difficulty of the task when approached from a symbolic NLP perspective." |
| Q64 | 7 | stated_limitations | "First, the frame-semantic pipeline has a poor degree of coverage with many relations not being picked up by our PropBank parser as they do not adhere to the default predicate-argument structure." |
| Q65 | 7 | stated_limitations | "This effect is exacerbated by the type of language used in the highlights that form the basis of our datasets." |
| Q66 | 7 | stated_limitations | "The second issue is that the frame-semantic approach does not trivially scale to situations where several sentences, and thus frames, are required to answer a query." |
| Q67 | 7 | stated_limitations | "This was true for the majority of queries in the dataset." |
| Q68 | 7 | stated_limitations | "We expect that on other types of machine reading data where questions rather than Cloze queries are used this particular model would perform significantly worse." |
| Q69 | 7 | stated_limitations | "Memory constraints prevented us from experimenting with deeper Attentive Readers." |
| Q70 | 8 | task_taxonomy | "The supervised paradigm for training machine reading and comprehension models provides a promising avenue for making progress on the path to building full natural language understanding systems." |
| Q71 | 8 | task_taxonomy | "We have demonstrated a methodology for obtaining a large number of document-query-answer triples and shown that recurrent and attention based neural networks provide an effective modelling framework for this task." |
| Q72 | 8 | evaluation_metrics | "Our analysis indicates that the Attentive and Impatient Readers are able to propagate and integrate semantic information over long distances." |
| Q73 | 8 | evaluation_metrics | "In particular we believe that the incorporation of an attention mechanism is the key contributor to these results." |
| Q74 | 8 | stated_limitations | "However, the incorporation of world knowledge and multi-document queries will also require the development of attention and embedding mechanisms whose complexity to query does not scale linearly with the data set size." |
| Q75 | 8 | stated_limitations | "There are still many queries requiring complex inference and long range reference resolution that our models are not yet able to answer." |
| Q76 | 8 | data_format | "Note that these examples were chosen as they were short, the average CNN validation document contained 763 tokens and 27 entities, thus most instances were significantly harder to answer than these examples." |
| Q77 | 10 | data_format | "The precise hyperparameters used for the various attentive models are as in Table 6. All models were trained using asynchronous RmsProp [20] with a momentum of 0.9 and a decay of 0.95." |
| Q78 | 10 | evaluation_metrics | "To understand how the model performance depends on the size of the context, we plot performance versus document lengths in Figures 4 and 5. The first figure (Fig. 4) plots a sliding window of performance across document length, showing that performance of the attentive models degrades slightly as documents increase in length. The second figure (Fig. 5) shows the cumulative performance with documents up to length N, showing that while the length does impact the models' performance, that effect becomes negligible after reaching a length of ~500 tokens." |
| Q79 | 10 | evaluation_metrics | "We expand on the analysis of the attention mechanism presented in the paper by including visualisations for additional queries from the CNN validation dataset below. We consider examples from the Attentive Reader as well as the Impatient Reader in this appendix." |
| Q80 | 10 | task_taxonomy | "Figure 6 shows two positive examples from the CNN validation set that require reasonable levels of lexical generalisation and co-reference in order to be answered. The first query in Figure 7 contains strong lexical cues through the quote, but requires identifying the entity" |
| Q81 | 11 | stated_limitations | "Figures 8 and 9 show examples of queries where the Attentive Reader fails to select the correct answer. The two examples in Figure 8 highlight a fairly common phenomenon in the data, namely ambiguous queries, where—at least following the anonymisation process—multiple entities are plausible answers even when evaluated manually." |
| Q82 | 11 | stated_limitations | "Note that in both cases the query searches for an entity marker that describes a geographic location, preceded by the word "in". Here it is unclear whether the placeholder refers to a part of town, town, region or country." |
| Q83 | 11 | stated_limitations | "Figure 9 contains two additional negative cases. The first failure is caused by the co-reference entity selection process. The correct entity, ent15, and the predicted one, ent81, both refer to the same person, but not being clustered together. Arguably this is a difficult clustering as one entity refers to "Kate Middleton" and the other to "The Duchess of Cambridge"." |
| Q84 | 11 | stated_limitations | "The right example shows a situation in which the model fails as it perhaps gets too little information from the short query and then selects the wrong cue with the term "claims" near the wrongly identified entity ent1 (correct: ent74)." |
| Q85 | 11 | evaluation_metrics | "To give a better intuition for the behaviour of the Impatient Reader, we use a similar visualisation technique as before. However, this time around we highlight the attention at every time step as the model updates its focus while moving through a given query. Figures 10–13 shows how the attention of the Impatient Reader changes and becomes increasingly more accurate as the model" |
| Q86 | 12 | evaluation_metrics | "Figure 7: Two more correctly answered validation set queries. The left example (entity ent315) requires correctly attributing the quote, which does not appear trivial with a number of other candidate entities in the vicinity. The right hand side shows our model is not afraid of Chuck Norris (ent164)." |
| Q87 | 12 | evaluation_metrics | "Figure 8: Attention heat maps from the Attentive Reader for two wrongly answered validation set queries. In the left case the model returns ent85 (correct: ent67), in the right example it gives ent24 (correct: ent64). In both cases the query is unanswerable due to its ambiguous nature and the model selects a plausible answer." |
| Q88 | 12 | evaluation_metrics | "Note how the attention is distributed fairly arbitraty at first, slowly focussing on the correct entity ent5 only once the question has sufficiently been parsed." |

### Category Index
- **task_taxonomy**: Q1, Q2, Q10, Q11, Q17, Q20, Q21, Q23, Q24, Q35, Q37, Q38, Q39, Q41, Q44, Q53, Q54, Q55, Q70, Q71, Q80
- **data_sources**: Q4, Q9, Q14
- **data_format**: Q3, Q15, Q16, Q18, Q19, Q25, Q26, Q28, Q30, Q36, Q40, Q42, Q43, Q46, Q47, Q48, Q56, Q76, Q77
- **label_categories**: NO QUOTES — paper is silent
- **annotation_process**: NO QUOTES — paper is silent
- **evaluation_metrics**: Q7, Q22, Q29, Q31, Q32, Q33, Q34, Q49, Q50, Q51, Q52, Q57, Q58, Q59, Q60, Q61, Q62, Q72, Q73, Q78, Q79, Q85, Q86, Q87, Q88
- **stated_limitations**: Q5, Q6, Q12, Q13, Q27, Q45, Q63, Q64, Q65, Q66, Q67, Q68, Q69, Q74, Q75, Q81, Q82, Q83, Q84
- **authors_affiliations**: Q8
