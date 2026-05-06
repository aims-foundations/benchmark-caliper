---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | annotation_process | "In this paper, we describe the creation of a resource - ASAP++ - which is basically annotations of the Automatic Student Assessment Prize's Automatic Essay Grading dataset. These annotations are scores for different attributes of the essays, such as content, word choice, organization, sentence fluency, etc. Each of these essays is scored by an annotator." |
| Q2 | 1 | evaluation_metrics | "We also report the results of each of the attributes using a Random Forest Classifier using a baseline set of attribute independent features as described by Zesch et al. (2015)." |
| Q3 | 1 | data_sources | "The ASAP AEG dataset comprises of approximately 13,000 essays, written across 8 prompts. The essays were written by students of class 7 to 10. Each essay was evaluated by 2 evaluators. 6 out of the 8 prompts only have overall scores. Only 2 of them have scores for individual essay attributes, like content, organization, style, etc." |
| Q4 | 1 | task_taxonomy | "Our contribution is the scoring of individual attributes of the essays, like content, organization, style, etc. in the ASAP dataset for the remainder of the essays." |
| Q5 | 1 | stated_limitations | "A lot of the work in essay grading today makes use of the ASAP AEG dataset. However, most of the essays only have an overall score, not attribute-specific scores. This limitation limits the utility of this dataset for predicting the scores of particular attributes of essays." |
| Q6 | 1 | stated_limitations | "However, most of them (in particular the deep learning systems) are constrained by the fact that there are very few prompts to handle scoring of individual attributes." |
| Q7 | 1 | task_taxonomy | "While there has been a lot of work done in overall essay scoring, not much has been done with respect to scoring particular attributes of essays. Some of the attributes that have been scored include organization (Persing et al., 2010), prompt adherence (Persing and Ng, 2014), coherence (Somasundaran et al., 2014)." |
| Q8 | 1 | data_sources | "The entire ASAP dataset has nearly 13,000 essays across 8 prompts. 6 of those 8 prompts, comprising nearly 10,400 essays, only have an overall score." |
| Q9 | 1 | authors_affiliations | "Sandeep Mathias, Pushpak Bhattacharyya Department of Computer Science and Engineering Indian Institute of Technology, Bombay" |
| Q10 | 2 | data_sources | "All the essays were written by native English speaking children from classes 7 to 10." |
| Q11 | 2 | label_categories | "We use the same score range as the overall score range of the essays." |
| Q12 | 2 | task_taxonomy | "There are 3 types of essays in the dataset." |
| Q13 | 2 | task_taxonomy | "Argumentative / Persuasive essays - These are essays where the prompt is one in which the writer has to convince the reader about their stance for or against a topic (for example, free speech in public colleges)." |
| Q14 | 2 | task_taxonomy | "Source-dependent responses - These essays are responses to a source text, where the writer responds to a question about the text (for instance, describing the writer's opinion about an incident that happened to him in the text)." |
| Q15 | 2 | task_taxonomy | "Narrative / Descriptive essays - These are essays where the prompt requires us to describe / narrate a story." |
| Q16 | 2 | label_categories | "The ASAP dataset already contains attribute scores for the narrative essays, namely content, organization, word choice, sentence fluency, conventions, etc." |
| Q17 | 2 | label_categories | "Since we already have scores present for the narrative essays, we describe the scores for the other types of essays." |
| Q18 | 2 | label_categories | "Based on the types of essays, there are 2 sets of attributes." |
| Q19 | 2 | label_categories | "There are 5 attributes for narrative essays, namely 1. Content: The quantity of relevant text present in the essay. 2. Organization: The way the essay is structured. 3. Word Choice: The choice and aptness of the vocabulary used in the essay." |
| Q20 | 3 | annotation_process | "Each of the essays in a particular prompt were scored by an annotator." |
| Q21 | 3 | data_format | "Each prompt was split into sets of 100 essays each, with the assumption that a set would correspond to a week's worth of time for the annotator." |
| Q22 | 3 | annotation_process | "Unlike the ASAP AEG dataset in which every essay was annotated by 2 annotators, we use only 1 annotator here for each essay." |
| Q23 | 3 | annotation_process | "For the ground truth, we make use of the overall score of the essays given by the original annotators of the ASAP AEG dataset." |
| Q24 | 3 | annotation_process | "In case the scoring of a particular attribute for a particular prompt differs from either of the original scorers by 2 or more points, the essay is then annotated by another annotator." |
| Q25 | 3 | annotation_process | "The final score that is chosen is the one from the annotator that is closest to the overall scores." |
| Q26 | 3 | stated_limitations | "One of the reasons that we do this is because, in the 2 prompts that were rated by the original raters, there is a very high Pearson correlation (nearly 0.9) between the overall scores and the individual attribute scores." |
| Q27 | 3 | annotation_process | "We made use of a total of three annotators to annotate the essays." |
| Q28 | 3 | annotation_process | "Each of the annotators had competence in English, either by scoring quite high marks in their high school exams (over 90% in English), or scoring over 110 in ToEFL." |
| Q29 | 3 | annotation_process | "Each of them also had some experience in evaluating texts, such as interning at The Hindu (a top English newspaper in India), being the chief editor of the college magazine, etc." |
| Q30 | 3 | annotation_process | "All the annotators have either studied or are studying English at a Master of Arts (MA) level." |
| Q31 | 3 | data_format | "We used the attribute independent feature set provided by Zesch et al. (2015)." |
| Q32 | 3 | data_format | "In addition to those features, we also made use of entity grid features described in Barzilay and Lapata (2005)." |
| Q33 | 3 | data_format | "All the features were extracted using Stanford Core NLP (Manning et al., 2014)." |
| Q34 | 4 | evaluation_metrics | "We evaluate each of the annotators using Cohen's Kappa, with quadratic weights - i.e. Quadratic Weighted Kappa (QWK) (Cohen, 1968)." |
| Q35 | 4 | evaluation_metrics | "We chose this as the evaluation metric (as compared to accuracy and weighted F-Score) because of the following reasons: Unlike accuracy and F-Score, Kappa takes into account random agreement." |
| Q36 | 4 | evaluation_metrics | "Weighted Kappa, takes into account the distance between the actual score and the reported score. Quadratic weights reward matches and penalize mismatches more than linear weights." |
| Q37 | 4 | evaluation_metrics | "Due to these reasons, this is one of the most used evaluation metrics to evaluate the performance of essay grading systems. To the best of our knowledge, all of the papers using the ASAP dataset make use of this as the evaluation metric." |
| Q38 | 4 | evaluation_metrics | "We made use of the Ordinal Class Classifier (Frank and Hall, 2001) in Weka (Frank et al., 2016). This classifier is a meta-classifier, that first converts ordinal data into categorical data, before running an internal classifier on the data. We used the Random Forest classifier (Breiman, 2001) as the internal classifier." |
| Q39 | 4 | evaluation_metrics | "We used 5-fold cross validation to get the results for each attribute for each prompt." |
| Q40 | 4 | annotation_process | "Most of the essays required only a single annotator. Only about a sixth of the essays required a second annotator." |
| Q41 | 4 | stated_limitations | "One of the major problems that the annotators faced was the fact that all the essays were anonymized. Named entities, like The New York Times would be referred to as @ORGANIZATION1, Donald Trump would be referred to as @PERSON1, etc." |
| Q42 | 4 | annotation_process | "The annotators were instructed not to penalize the essays because of the anonymizations, but were told to replace them with placeholders (like @PERSON1 being replaced by either Joe, or Jane, etc. wherever applicable)." |
| Q43 | 4 | task_taxonomy | "For source-dependent essays, we found out that the most important feature for content was length, while for argumentative / persuasive essays, it was coherence and cohesion features, followed by length." |
| Q44 | 4 | task_taxonomy | "For source-dependent essays, the coherence and cohesion feature set is the most important feature set for each of the other 3 attributes." |
| Q45 | 4 | task_taxonomy | "For persuasive / argumentative essays, coherence and cohesion features are the most important features for 4 of the 5 attributes." |
| Q46 | 5 | data_sources | "In this paper, we present a manually annotated dataset for automated essay grading." |
| Q47 | 5 | annotation_process | "The annotation was done for different attributes of the essays." |
| Q48 | 5 | annotation_process | "Most of the essays were annotated by a single annotator." |
| Q49 | 5 | annotation_process | "However, about a sixth of them were annotated by a second annotator." |
| Q50 | 5 | label_categories | "These annotations can be used as a gold standard for future experiments in predicting different attribute scores." |
| Q51 | 5 | data_sources | "The resource is available online at https://cfilt.iitb.ac.in/˜egdata/." |
| Q52 | 5 | stated_limitations | "The resource is available for non-commercial research use under the Creative Commons Attribution-ShareAlike License." |
| Q53 | 5 | annotation_process | "We thank the annotators of our task - Advaith Jayakumar, Janice Pereira and Elaine Mathias - for their help in creating this resource." |
| Q54 | 5 | authors_affiliations | "We also thank members of CFILT at IIT Bombay for their valuable comments and suggestions." |

### Category Index
- **task_taxonomy**: Q4, Q7, Q12, Q13, Q14, Q15, Q43, Q44, Q45
- **data_sources**: Q3, Q8, Q10, Q46, Q51
- **data_format**: Q21, Q31, Q32, Q33
- **label_categories**: Q11, Q16, Q17, Q18, Q19, Q50
- **annotation_process**: Q1, Q20, Q22, Q23, Q24, Q25, Q27, Q28, Q29, Q30, Q40, Q42, Q47, Q48, Q49, Q53
- **evaluation_metrics**: Q2, Q34, Q35, Q36, Q37, Q38, Q39
- **stated_limitations**: Q5, Q6, Q26, Q41, Q52
- **authors_affiliations**: Q9, Q54
