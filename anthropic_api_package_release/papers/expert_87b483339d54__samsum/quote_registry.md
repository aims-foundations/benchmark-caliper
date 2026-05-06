---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | data_sources | "This paper introduces the SAMSum Corpus, a new dataset with abstractive dialogue summaries." |
| Q2 | 1 | task_taxonomy | "We investigate the challenges it poses for automated summarization by testing several models and comparing their results with those obtained on a corpus of news articles." |
| Q3 | 1 | evaluation_metrics | "We show that model-generated summaries of dialogues achieve higher ROUGE scores than the model-generated summaries of news – in contrast with human evaluators' judgement." |
| Q4 | 1 | stated_limitations | "This suggests that a challenging task of abstractive dialogue summarization requires dedicated models and non-standard quality measures." |
| Q5 | 1 | data_sources | "To our knowledge, our study is the first attempt to introduce a high-quality chat-dialogues corpus, manually annotated with abstractive summarizations, which can be used by the research community for further studies." |
| Q6 | 1 | task_taxonomy | "In the abstractive approach important pieces of information are presented using words and phrases not necessarily appearing in the source text." |
| Q7 | 1 | task_taxonomy | "Major research efforts have focused so far on summarization of single-speaker documents like news (e.g., Nallapati et al. (2016)) or scientific publications (e.g., Nikolov et al. (2018))." |
| Q8 | 1 | data_sources | "One of the reasons is the availability of large, high-quality news datasets with annotated summaries, e.g., CNN/Daily Mail (Hermann et al., 2015; Nallapati et al., 2016)." |
| Q9 | 1 | stated_limitations | "Such a comprehensive dataset for dialogues is lacking." |
| Q10 | 1 | task_taxonomy | "The challenges posed by the abstractive dialogue summarization task have been discussed in the literature with regard to AMI meeting corpus (McCowan et al., 2005), e.g. Banerjee et al. (2015), Mehdad et al. (2014), Goo and Chen (2018)." |
| Q11 | 1 | stated_limitations | "Since the corpus has a low number of summaries (for 141 dialogues), Goo and Chen (2018) proposed to use assigned topic descriptions as gold references." |
| Q12 | 1 | task_taxonomy | "With the growing popularity of online conversations via applications like Messenger, WhatsApp and WeChat, summarization of chats between a few participants is a new interesting direction of summarization research." |
| Q13 | 1 | data_sources | "For this purpose we have created the SAMSum Corpus which contains over 16k chat dialogues with manually annotated summaries." |
| Q14 | 1 | data_sources | "The dataset is freely available for the research community." |
| Q15 | 1 | authors_affiliations | "Bogdan Gliwa, Iwona Mochol, Maciej Biesek, Aleksander Wawer" |
| Q16 | 1 | authors_affiliations | "Samsung R&D Institute Poland" |
| Q17 | 2 | data_sources | "Our dialogue summarization dataset contains natural messenger-like conversations created and written down by linguists fluent in English." |
| Q18 | 2 | data_format | "The style and register of conversations are diversified – dialogues could be informal, semi-formal or formal, they may contain slang phrases, emoticons and typos." |
| Q19 | 2 | data_sources | "We asked linguists to create conversations similar to those they write on a daily basis, reflecting the proportion of topics of their real-life messenger conversations." |
| Q20 | 2 | task_taxonomy | "It includes chit-chats, gossiping about friends, arranging meetings, discussing politics, consulting university assignments with colleagues, etc." |
| Q21 | 2 | stated_limitations | "Therefore, this dataset does not contain any sensitive data or fragments of other corpora." |
| Q22 | 2 | data_sources | "Each dialogue was created by one person." |
| Q23 | 2 | annotation_process | "After collecting all of the conversations, we asked language experts to annotate them with summaries, assuming that they should (1) be rather short, (2) extract important pieces of information, (3) include names of interlocutors, (4) be written in the third person." |
| Q24 | 2 | label_categories | "Each dialogue contains only one reference summary." |
| Q25 | 2 | annotation_process | "We asked two linguists to doubly annotate 50 conversations in order to verify whether the dialogues could appear in a messenger app and could be summarized (i.e. a dialogue is not too general or unintelligible) or not (e.g. a dialogue between two people in a shop)." |
| Q26 | 2 | annotation_process | "The results revealed that 94% of examined dialogues were classified by both annotators as good i.e. they do look like conversations from a messenger app and could be condensed in a reasonable way." |
| Q27 | 2 | annotation_process | "In a similar validation task, conducted for the existing dialogue-type datasets (described in the Initial approach section), the annotators agreed that only 28% of the dialogues resembled conversations from a messenger app." |
| Q28 | 2 | data_format | "After preparing the dataset, we conducted a process of cleaning it in a semi-automatic way." |
| Q29 | 2 | data_format | "Beforehand, we specified a format for written dialogues with summaries: a colon should separate an author of utterance from its content, each utterance is expected to be in a separate line." |
| Q30 | 2 | data_format | "Therefore, we could easily find all deviations from the agreed structure – some of them could be automatically fixed (e.g. when instead of a colon, someone used a semicolon right after the interlocutor's name at the beginning of an utterance), others were passed for verification to linguists." |
| Q31 | 2 | data_format | "We also tried to correct typos in interlocutors' names (if one person has several utter-" |
| Q32 | 3 | data_sources | "The created dataset is made of 16369 conversations distributed uniformly into 4 groups based on the number of utterances in conversations: 3-6, 7-12, 13-18 and 19-30." |
| Q33 | 3 | data_format | "Each utterance contains the name of the speaker." |
| Q34 | 3 | data_sources | "Most conversations consist of dialogues between two interlocutors (about 75% of all conversations), the rest is between three or more people." |
| Q35 | 3 | annotation_process | "we used the Levenshtein distance to find very similar names (possibly with typos e.g. 'George' and 'Goerge') in a single conversation, and those cases with very similar names were passed to linguists for verification." |
| Q36 | 3 | data_format | "Table 1 presents the size of the dataset split used in our experiments." |
| Q37 | 3 | evaluation_metrics | "Results of the evaluation of the above models are reported in Table 3." |
| Q38 | 3 | stated_limitations | "There is no obvious baseline for the task of dialogues summarization." |
| Q39 | 3 | stated_limitations | "We expected rather low results for Lead-3, as the beginnings of the conversations usually contain greetings, not the main part of the discourse." |
| Q40 | 4 | data_sources | "In order to build a dialogue summarization model, we adopt the following strategies: (1) each candidate architecture is trained and evaluated on the dialogue dataset; (2) each architecture is trained on the train set of CNN/Daily Mail joined together with the train set of the dialogue data, and evaluated on the dialogue test set." |
| Q41 | 4 | data_format | "In addition, we prepare a version of dialogue data, in which utterances are separated with a special token called the separator (artificially added token e.g. '<EOU>' for models using word embeddings, '\|' for models using subword embeddings)." |
| Q42 | 4 | data_format | "In all our experiments, news and dialogues are truncated to 400 tokens, and summaries – to 100 tokens." |
| Q43 | 4 | data_format | "The maximum length of generated summaries was not limited." |
| Q44 | 4 | task_taxonomy | "We carry out experiments with the following summarization models (for all architectures we set the beam size for beam search decoding to 5): Pointer generator network, Transformer, Fast Abs RL, Fast Abs RL Enhanced, LightConv and DynamicConv." |
| Q45 | 4 | stated_limitations | "For dialogues, we change the convolutional word-level sentence encoder (used in extractor part) to only use kernel with size equal 3 instead of 3-5 range. It is caused by the fact that some of utterances are very short and the default setting is unable to handle that." |
| Q46 | 4 | data_format | "The additional variant of the Fast Abs RL model with slightly changed utterances i.e. to each utterance, at the end, after artificial separator, we add names of all other interlocutors." |
| Q47 | 4 | evaluation_metrics | "We evaluate models with the standard ROUGE metric (Lin, 2004), reporting the F1 scores (with stemming) for ROUGE-1, ROUGE-2 and ROUGE-L following previous works (Chen and Bansal, 2018; See et al., 2017)." |
| Q48 | 5 | annotation_process | "We asked two linguists to mark the quality of every summary on the scale of −1, 0, 1, where −1 means that a summarization is poor, extracts irrelevant information or does not make sense at all, 1 – it is understandable and gives a brief overview of the text, and 0 stands for a summarization that extracts only a part of relevant information, or makes some mistakes in the produced summary." |
| Q49 | 5 | annotation_process | "We noticed a few annotations (7 for news and 4 for dialogues) with opposite marks (i.e. one annotator judgement was −1, whereas the second one was 1) and decided to have them annotated once again by another annotator who had to resolve conflicts." |
| Q50 | 5 | evaluation_metrics | "For the rest, we calculated the linear weighted Cohen's kappa coefficient (McHugh, 2012) between annotators' scores." |
| Q51 | 5 | annotation_process | "For news examples, we obtained agreement on the level of 0.371 and for dialogues – 0.506." |
| Q52 | 5 | stated_limitations | "The annotators' agreement is higher on dialogues than on news, probably because of structures of those data – articles are often long and it is difficult to decide what the key-point of the text is; dialogues, on the contrary, are rather short and focused mainly on one topic." |
| Q53 | 5 | evaluation_metrics | "For manually evaluated samples, we calculated ROUGE metrics and the mean of two human ratings; the prepared statistics is presented in Table 6." |
| Q54 | 5 | stated_limitations | "Models generating dialogue summaries can obtain high ROUGE results, but their outputs are marked as poor by human annotators." |
| Q55 | 5 | stated_limitations | "Our conclusion is that the ROUGE metric corresponds with the quality of generated summaries for news much better than for dialogues, confirmed by Pearson's correlation between human evaluation and the ROUGE metric." |
| Q56 | 6 | stated_limitations | "In a structured text, such as a news article, the information flow is very clear. However, in a dialogue, which contains discussions (e.g. when people try to agree on a date of a meeting), questions (one person asks about something and the answer may appear a few utterances later) and greetings, most important pieces of information are scattered across the utterances of different speakers." |
| Q57 | 6 | stated_limitations | "What is more, articles are written in the third-person point of view, but in a chat everyone talks about themselves, using a variety of pronouns, which further complicates the structure." |
| Q58 | 6 | stated_limitations | "Additionally, people talking on messengers often are in a hurry, so they shorten words, use the slang phrases (e.g. 'u r gr8' means 'you are great') and make typos. These phenomena increase the difficulty of performing dialogue summarization." |
| Q59 | 6 | stated_limitations | "Firstly, the models frequently have difficulties in associating names with actions, often repeating the same name, e.g., for Dialogue 1 in Table 8, Fast Abs RL generates the following summary: 'lilly and lilly are going to eat salmon'." |
| Q60 | 6 | data_format | "To help the model deal with names, the utterances are enhanced by adding information about the other interlocutors – Fast Abs RL enhanced variant de-" |
| Q61 | 7 | task_taxonomy | "This paper is a step towards abstractive summarization of dialogues by (1) introducing a new dataset, created for this task, (2) comparison with news summarization by the means of automated (ROUGE) and human evaluation." |
| Q62 | 7 | stated_limitations | "Most of the tools and the metrics measuring the quality of text summarization have been developed for a single-speaker document, such as news; as such, they are not necessarily the best choice for conversations with several speakers." |
| Q63 | 7 | evaluation_metrics | "In terms of human evaluation, the results of dialogues summarization are worse than the results of news summarization." |
| Q64 | 7 | stated_limitations | "This is connected with the fact that the dialogue structure is more complex – information is spread in multiple utterances, discussions, questions, more typos and slang words appear there, posing new challenges for summarization." |
| Q65 | 7 | data_format | "On the other hand, dialogues are divided into utterances, and for each utterance its author is assigned." |
| Q66 | 7 | data_format | "We demonstrate in experiments that the models benefit from the introduction of separators, which mark utterances for each person." |
| Q67 | 8 | evaluation_metrics | "We show that the most popular summarization metric ROUGE does not reflect the quality of a summary." |
| Q68 | 8 | evaluation_metrics | "We performed an independent, manual analysis of summaries and we demonstrated that high ROUGE results, obtained for automatically-generated dialogue summaries, correspond with lower evaluation marks given by human annotators." |
| Q69 | 8 | stated_limitations | "We conclude that when measuring the quality of model-generated summaries, the ROUGE metrics are more indicative for news than for dialogues, and a new metric should be designed to measure the quality of abstractive dialogue summaries." |
| Q70 | 8 | task_taxonomy | "In our paper we have studied the challenges of abstractive dialogue summarization." |
| Q71 | 8 | data_sources | "To the best of our knowledge, this is the first attempt to create a comprehensive resource of this type which can be used in future research." |
| Q72 | 8 | stated_limitations | "The next step could be creating an even more challenging dataset with longer dialogues that not only cover one topic, but span over" |
| Q73 | 9 | stated_limitations | "As shown, summarization of dialogues is much more challenging than of news." |
| Q74 | 9 | stated_limitations | "In order to perform well, it may require designing dedicated tools, but also new, non-standard measures to capture the quality of abstractive dialogue summaries in a relevant way." |
| Q75 | 9 | authors_affiliations | "We would like to express our sincere thanks to Tunia Błachno, Oliwia Ebebenge, Monika Jędras and Małgorzata Krawentek for their huge contribution to the corpus collection – without their ideas, management of the linguistic task and verification of examples we would not be able to create this paper." |

### Category Index
- **task_taxonomy**: Q2, Q6, Q7, Q10, Q12, Q20, Q44, Q61, Q70
- **data_sources**: Q1, Q5, Q8, Q13, Q14, Q17, Q19, Q22, Q32, Q34, Q40, Q71
- **data_format**: Q18, Q28, Q29, Q30, Q31, Q33, Q36, Q41, Q42, Q43, Q46, Q60, Q65, Q66
- **label_categories**: Q24
- **annotation_process**: Q23, Q25, Q26, Q27, Q35, Q48, Q49, Q51
- **evaluation_metrics**: Q3, Q37, Q47, Q50, Q53, Q63, Q67, Q68
- **stated_limitations**: Q4, Q9, Q11, Q21, Q38, Q39, Q45, Q52, Q54, Q55, Q56, Q57, Q58, Q59, Q62, Q64, Q69, Q72, Q73, Q74
- **authors_affiliations**: Q15, Q16, Q75
