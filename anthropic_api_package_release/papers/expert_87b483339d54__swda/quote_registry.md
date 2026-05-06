---

## Quote Registry

**This section is authoritative.** Every entry is verbatim text from the paper.

| ID | Page | Category | Text |
|----|------|----------|------|
| Q1 | 1 | task_taxonomy | "SWITCHBOARD is a large multispeaker corpus of conversational speech and text which should be of interest to researchers in speaker authentication and large vocabulary speech recognition." |
| Q2 | 1 | data_sources | "About 2500 conversations by 500 speakers from around the U.S. were collected automatically over T1 lines at Texas Instruments." |
| Q3 | 1 | data_sources | "SWITCHBOARD, which is about 65% complete at the time of this writing, will include 2500 conversations of three to ten minutes' duration, carried on by about 500 paid volunteers of both sexes from every major dialect of American English." |
| Q4 | 1 | data_sources | "In round numbers, this amounts to over 250 hours of speech and nearly 3 million words of text." |
| Q5 | 1 | data_format | "It has over an hour of speech from each of 50 speakers, and several minutes each from hundreds of others." |
| Q6 | 1 | data_format | "A time-aligned word for word transcription accompanies each recording." |
| Q7 | 1 | data_format | "all-digital 4-wire format" |
| Q8 | 1 | data_format | "detailed transcription and time alignment of all conversations" |
| Q9 | 1 | annotation_process | "The conversations in SWITCHBOARD were collected under computer control, without human intervention." |
| Q10 | 1 | annotation_process | "From a human factors perspective, automation guards against the intrusion of experimenter bias, and provides a degree of uniformity in the collection environment." |
| Q11 | 1 | evaluation_metrics | "SWITCHBOARD has a number of unique features designed to support research in both speaker authentication and speech recognition for telephone-based applications." |
| Q12 | 1 | evaluation_metrics | "design for multiple testing runs and a variety of technical approaches" |
| Q13 | 1 | stated_limitations | "There is a potential disadvantage, in that once an automated system is in place, it cannot readily be" |
| Q14 | 1 | authors_affiliations | "John J. Godfrey, Edward C. Holliman, Jane McDaniel, Texas Instruments, Inc., Dallas, TX 75265" |
| Q15 | 2 | data_sources | "The SWITCHBOARD collection protocol was therefore developed over months of extensive piloting. Experiments determined the kind and amount of man-machine interaction, the order of presentation, the types of prompts, and other factors needed to insure smooth participation and to elicit natural and spontaneous speech by the participants." |
| Q16 | 2 | data_sources | "The hardware platform was a commercial system, known as a "Robotooperator," consisting of an IBM Model 80 computer, 700MB disk drive, T1 interface, and a programmable switching system for connecting among the channels of the T1 span." |
| Q17 | 2 | data_sources | "An application software package intended for commercial use was modified to control the SWITCHBOARD protocol." |
| Q18 | 2 | data_format | "Upon receiving an incoming call on one of the T1 channels, it would play appropriate messages, tic collect touchtones indicating the caller's identification and telephone number." |
| Q19 | 2 | data_collection | "Before the two callers are interconnected, they are engaged in two separate telephone calls with the computer, listening to recorded messages and sending touchtones back." |
| Q20 | 2 | data_format | "This pair of 8 kHz, mu-law encoded signal files is later integrated into one file in the NIS-7 standard SPHERE format, with alternating bytes from the two sides of the conversation interleaved." |
| Q21 | 2 | stated_limitations | "The isolation of the two talkers is limited by the long distance telephone network's echo cancelling performance, but is generally better than 20dB." |
| Q22 | 2 | annotation_process | "Transcribers were later asked to rate the naturalness of conversations they listened to, using a five point scale from "very natural" (1) to "forced or unnatural-sounding" (5)." |
| Q23 | 2 | evaluation_metrics | "The average rating of 1.48 suggests that the collection protocol was successful in this respect." |
| Q24 | 2 | data_format | "Each conversation is fully transcribed, with special conventions to show speakers' turns, simultaneous talking, interrupted sentences, partial words, and other phenomena common in spontaneous conversational speech." |
| Q25 | 2 | annotation_process | "After producing the text, the transcribers were asked to rate each conversation on a number of properties, such as the amount of background noise or static, difficulty in understanding the talkers, and degree to which the conversants stayed on one subject." |
| Q26 | 3 | data_format | "The SWITCHBOARD conversations are also time aligned at the word level." |
| Q27 | 3 | data_format | "The time alignment is accomplished using supervised phone-based recognition, as described in a companion paper by Wheatley [5]." |
| Q28 | 3 | data_format | "This process produces phone to phone time markings, which are then reduced to a word by word format for publication with the transcripts." |
| Q29 | 3 | data_format | "The original phonetic base forms will be available in a dictionary with the SWITCHBOARD corpus." |
| Q30 | 3 | data_sources | "The configuration illustrated in Figure 1 shows 60% of the conversations being used for training and 40% for repeated tests." |
| Q31 | 3 | task_taxonomy | "The design of the SWITCHBOARD corpus emphasizes the importance of both depth and breadth of coverage, especially for speaker verification research." |
| Q32 | 3 | data_sources | "Fifty 'target' speakers participated at least 25 times, which adds up to more than an hour of speech gathered over a period of weeks." |
| Q33 | 3 | data_sources | "The target callers were six different from the rest of the population, except that they had to make and receive calls with multiple telephone instruments." |
| Q34 | 3 | data_sources | "This was intended to prevent speakers from being identified by channel effects due to handled characteristics." |
| Q35 | 3 | data_sources | "The design assumes that 25 target speakers should suffice to get statistically reliable estimates of the performance of a speaker verification algorithm under development; an equal number is available to be set aside for final evaluation of the system." |
| Q36 | 3 | data_sources | "The other 450 speakers who participate in from one to twenty calls constitute a pool of 'imposters.'" |
| Q37 | 4 | data_sources | "Demographic information about the speakers is entered in an Oracle data base when they register to participate. This includes their age, sex, level of education, and the geographically-defined dialect area where they grew up." |
| Q38 | 4 | data_format | "The callers' identification numbers, the date, time, and length of the call, as well as the area codes and telephone numbers of the participants and other pertinent information about each call are all automatically entered into Oracle tables." |
| Q39 | 4 | data_sources | "The information in these tables, except for protected personal data, will accompany the speech and text files when the SWITCHBOARD corpus becomes publicly available." |
| Q40 | 4 | data_sources | "Distribution will be through the National Institutes of Standards and Technology." |
| Q41 | 4 | authors_affiliations | "This work was sponsored by DARPA/SPAWAR Contract No. N00039-90-0168." |

### Category Index
- **task_taxonomy**: Q1, Q31
- **data_sources**: Q2, Q3, Q4, Q15, Q16, Q17, Q30, Q32, Q33, Q34, Q35, Q36, Q37, Q39, Q40
- **data_format**: Q5, Q6, Q7, Q8, Q18, Q20, Q24, Q26, Q27, Q28, Q29, Q38
- **label_categories**: NO QUOTES — paper is silent
- **annotation_process**: Q9, Q10, Q22, Q25
- **evaluation_metrics**: Q11, Q12, Q23
- **stated_limitations**: Q13, Q21
- **authors_affiliations**: Q14, Q41
