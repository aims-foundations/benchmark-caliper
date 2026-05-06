## Deployment Context

**Use case:** Deployment scenario: A GPT-4 model is implemented in a one-on-one tutoring session, where its responses are augmented with a human tutor’s input. The tutor evaluates the pedagogical quality of the combined response, particularly in terms of how well it provides guidance. The goal is to assess whether the augmented GPT-4 responses are acceptable to the tutor.

Domain: Educational tutoring
Setting: Mobile application / enterprise software
**Target population:** High-end professional teacher teaching grade 1-8 in major metropolitan cities in India, such as Delhi and Mumbai, who is fluent in English.

# Validity Analysis: mathdial
**Target context:** Indian Metropolitan Professional Teachers (Grades 1–8)
**Overall risk:** HIGH

## Dimension Scores

| Dimension | Score | Rating | Confidence |
|-----------|:-----:|--------|:----------:|
| Input Ontology ✓ | 4 | Minor gaps | high |
| Input Content ⚠ | 1 | Serious concern | high |
| Input Form ✓ | 5 | Strong alignment | high |
| Output Ontology ⚠ | 2 | Significant gaps | high |
| Output Content ⚠ | 1 | Serious concern | high |
| Output Form ✓ | 5 | Strong alignment | high |
| **Average** | **3.0** | | |

> ⚠ = highest concern &nbsp; ✓ = strongest dimension

### Dimension Key

| Abbr. | Dimension | Definition |
|:-----:|-----------|------------|
| IO | Input Ontology | Whether the benchmark's test case categories cover the query types expected in deployment. |
| IC | Input Content | Whether individual datapoint content is culturally and contextually appropriate for the target region. |
| IF | Input Form | Whether the input signal encoding (text, audio, image parameters) matches deployment conditions. |
| OO | Output Ontology | Whether the benchmark's output categories and scoring criteria reflect regionally valid decision boundaries. |
| OC | Output Content | Whether ground-truth labels align with the judgments of regional stakeholders. |
| OF | Output Form | Whether the expected output modality matches regional deployment needs and accessibility. |

## Overall Summary

MathDial presents a structurally sound but culturally narrow evaluation framework for AI tutoring quality. For the Indian Metropolitan Professional Teachers (Grades 1–8) deployment, three dimensions are well-aligned (Input Form, Output Form, and — given user confirmation that the eight categories suffice — Input Ontology), while three dimensions raise serious concerns. Input Content (HIGH user priority) shows fundamental misalignment: the LLM-simulated student exhibits verbose, peer-register, reasoning-out-loud behavior diametrically opposed to the deferential brief low-verbalization style the user identifies as characteristic of Indian metro classrooms, math word problems are entirely US-origin, and LLM looping artifacts produce unnatural student behavior. Output Content (HIGH user priority) is the deepest concern: ground-truth labels were produced by predominantly UK/US annotators explicitly instructed toward Socratic non-directive scaffolding, with κ=0.34 inter-annotator agreement on Equitable Tutoring even within the Western pool — and the user explicitly expects Indian professional teachers' judgments to systematically diverge on direct-correction vs. probing and exam-readiness weighting. Output Ontology (MODERATE) embeds a constructivist anti-telling structural orientation (Telling@k as negative metric, Telling as last-resort) that conflicts with Indian professional teachers' view of direct correction as a primary pedagogical tool, and the user's prioritization of 'providing guidance' is not commensurately weighted in the three co-equal evaluation dimensions. The English text-only modality match is the benchmark's strongest validity asset for this deployment.

## Practical Guidance

### What This Benchmark Measures

MathDial can support evaluation of whether GPT-4-augmented tutoring responses adhere to a Western constructivist scaffolding framework on English-language multi-step math word problems. The benchmark's strongest contributions for the Indian metro deployment are its move-level taxonomy (IO, score 4) — providing a structured vocabulary of Focus, Probing, Telling, and Generic that the user has accepted as sufficient — and its form match (IF, OF both score 5), which means modality and language are not a barrier. It can measure surface-level dialogue coherence and mathematical correctness reliably.

### Construct Depth

The benchmark probes pedagogical quality shallowly for the Indian metro context. Input Content (score 1) means the student behavior the benchmark exposes evaluators to is systematically unrepresentative of Indian classrooms, so any judgments are anchored to dialogues that would not occur with real Indian students. Output Content (score 1) means the comparator ground-truth quality standard encodes Western Socratic norms the user explicitly identifies as misaligned. Output Ontology (score 2) means even when the right categories are present, their relative weighting and the framing of Telling-as-failure conflict with Indian professional pedagogical priorities. Together, IC and OC failures mean the benchmark cannot deeply probe the construct of 'good guidance for Indian metro professional teachers' — it probes 'good guidance for Western-trained constructivist tutors,' which is a different construct.

### What Else You Need

(a) Re-annotation of a representative subsample (e.g., 100–200 dialogues) by Indian metro professional teachers to produce parallel ground-truth labels, enabling measurement of κ between Western and Indian labels and identifying systematic divergence dimensions (addresses OC). (b) Augmentation or replacement of student simulation with dialogues reflecting Indian classroom interaction norms — brief, deferential, low-verbalization students — to address IC; this could draw on transcripts of Indian classrooms or use stakeholder-elicited student personas. (c) Reweighting or replacement of the Equitable Tutoring dimension with a 'Providing Guidance' dimension operationalized to credit appropriate directive instruction, addressing OO. (d) Inversion of Telling@k framing for the Indian context, treating early-but-appropriate Telling as a positive rather than negative outcome where it matches teacher-rated quality. (e) Cross-validation with PARIKSHA-style multilingual evaluation findings [WEB-18] to calibrate expectations of LLM-evaluator alignment with Indian human judgments.

## Dimension Details

### Input Ontology — 4/5 (Minor gaps)

**Confidence:** high

**Justification:**
The user explicitly confirmed that curriculum-agnostic math errors and the benchmark's eight pedagogical categories are necessary and sufficient for the deployment task [A1, A3], substantially reducing ontological misalignment risk. The taxonomy is theoretically grounded in Reiser's (2004) scaffolding framework distinguishing structure (Focus) from problematize (Probing) moves [Q36, Q37], with Telling and Generic as additional categories [Q40, Q41]. The dataset confirms transparent application of the four-move taxonomy across all sampled dialogues, providing structured pedagogical vocabulary [DATASET-D2, DATASET-D3]. Confusion type coverage spans six algebra-misconception categories [DATASET-D7, DATASET-D8, DATASET-D10]. Minor concerns remain: the taxonomy's structural privileging of scaffolding over directive correction [Q154, Q155] embeds a constructivist orientation that, while not omitting categories the user requires, frames the relationships among them in a way that may not match Indian metro teaching priorities. The benchmark also explicitly omits meta-cognitive support and rapport-building [Q112], though the user did not flag these as required.

**Strengths:**
- Eight pedagogical categories user-confirmed as necessary and sufficient for the deployment task [A3]
- Theoretically anchored in scaffolding learning sciences (Reiser 2004) [Q36, Q37]
- Fine-grained move labels systematically applied to every teacher utterance, enabling multi-dimensional pedagogical evaluation [DATASET-D2, DATASET-D3]
- Broad coverage of student confusion types relevant to Grades 1–8 math reasoning [DATASET-D7, DATASET-D8, DATASET-D10]

**Checklist:**

- **IO-1**: User confirmed curriculum-agnostic math errors and the eight pedagogical categories suffice for the Indian metro deployment [A1, A3]. Required test categories include Focus, Probing, Telling, Generic moves and conceptual/procedural error confusions, all present in the benchmark. — _Sources: Q42, DATASET-D2_
- **IO-2**: No regionally-relevant categories are identified by the user as missing. The benchmark omits meta-cognitive support, rapport-building [Q112], and visual instructional practices [Q113], but the user did not flag these as required for the deployment. — _Sources: Q112_
- **IO-3**: No categories are identified as irrelevant to the regional context. All four move types (Focus, Probing, Telling, Generic) appear in real classroom practice and Indian metro teachers can evaluate them, though the framing of Telling as a last resort [Q155] may be at odds with Indian pedagogical norms (handled under OO). — _Sources: Q154, Q155_
- **IO-4**: No major content-validity gaps identified at the ontology level given user confirmation of sufficiency [A3]. Residual concern is that the taxonomy's hierarchical valuation (scaffolding productive, Telling last-resort) [Q154, Q155] is itself a value-laden ontological choice. — _Sources: Q112, Q154_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q36] 'We base the first two on the work of Reiser (2004), who suggest that scaffolding strategies can be split into two main categories: structure and problematize.' (p.5)
- [Q42] 'Table 2 lists finer-grained intents for each of these four categories along with a set of accompanying examples.' (p.5)
- [Q112] 'Inspired by previous work in scaffolding, we acknowledge our focus is on a subset of common teaching moves. However, this does not cover all the goals of human tutors, such as meta-cognitive support or building rapport with a student.' (p.10)
- [Q154] 'Most importantly, scaffolding questions that are productive for long-term learning are Focus and Probing.' (p.17)
- [Q155] 'On the other hand, Telling represents giving out the partial or full answer to the student and should be mostly used when a student is stuck.' (p.17)

*Dataset analysis:*
- DATASET-D2: Six consecutive (probing) labels in one dialogue — taxonomy systematically applied at utterance level
- DATASET-D3: Telling moves explicitly labeled and visible in transcript
- DATASET-D7: Procedural confusion student profile category represented
- DATASET-D8: Underlying-principle confusion category represented
- DATASET-D10: Question-misunderstanding confusion category represented

</details>

**Information gaps:**
- Whether the user's acceptance of the eight categories was made with full awareness of how Telling is structurally devalued in the framework

**Requires expert verification:**
- Whether Indian metro teachers, after reviewing benchmark dialogues, would still affirm the eight categories as sufficient or would flag missing categories (e.g., explicit demonstration, drill, exam-strategy guidance)

---

### Input Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
Input content is the highest-priority concern (user-flagged HIGH) and the dataset analysis confirms severe construct-irrelevant variance. The student simulation is calibrated to Western tutoring conventions [Q32, Q34] with documented limitations in representing human learning [Q106]. Empirically, the LLM-simulated students invariably produce verbose, multi-sentence, reasoning-out-loud responses [DATASET-D6, DATASET-D7, DATASET-D9] — the polar opposite of the brief, deferential, low-verbalization style the user identifies as characteristic of Indian metro classrooms [A2]. Students even use casual peer-register openers ('Hi, I'm doing well. How can I help you?') [DATASET-D24] inconsistent with deferential Indian student-teacher interactions. Math word problems are entirely US-origin from GSM8k [Q103, Q118] with US currency and scenarios (recycling deposits, temp agencies) [DATASET-D15, DATASET-D16, DATASET-D17] and no Indian cultural grounding. Nominal name diversity [Q123, DATASET-D11] does not extend to behavioral diversity. Additional concern: simulated student loops on identical wrong answers across multiple teacher corrections [DATASET-D13, DATASET-D14] — an LLM artifact not representative of any real student population. Authors explicitly acknowledge teachers may have adapted to model patterns rather than exhibiting naturalistic behavior [Q108]. The MathDial dialogues thus encode interaction dynamics fundamentally misaligned with Indian metro classrooms at the level of every individual datapoint.

**Strengths:**
- Mathematical content (multi-step word problems, percentages, rates, equations) is broadly familiar to Indian Grade 1–8 teachers per user confirmation [A2]
- Single nominally South Asian name appears in sample (Rishi) [DATASET-D11], indicating the pipeline is not exclusionary at the name level
- Authors transparently document student simulation limitations [Q106, Q108]

**Checklist:**

- **IC-1**: Yes — the deployment requires student dialogues that reflect Indian classroom interaction norms (deferential, brief, low-verbalization students) per user elicitation [A2]. The benchmark does not provide region-specific cultural or interactional content. — _Sources: Q32, DATASET-D6, DATASET-D7_
- **IC-2**: No — culturally sensitive content (US monetary units, US labor scenarios, US-default names) does not align with Indian deployment context [DATASET-D15, DATASET-D16, DATASET-D17]. Nominal diversity does not extend to interaction style [DATASET-D11]. — _Sources: DATASET-D15, DATASET-D16, DATASET-D17, DATASET-D11_
- **IC-3**: Yes — inputs require US/Western cultural frames (recycling-deposit systems [DATASET-D16], temp-agency labor markets [DATASET-D17], dollar denominations [DATASET-D15]) that do not transfer naturally to Indian classroom contexts. — _Sources: DATASET-D15, DATASET-D16, DATASET-D17_
- **IC-4**: Authors did not recruit Indian-specific annotators to validate cultural appropriateness; India was a minority contributor to the annotator pool [Q27] and not separately consulted for IC validation. — _Sources: Q27_
- **IC-5**: Critical content-validity gaps documented: (a) simulated student verbosity diverges from Indian deferential norms [A2, DATASET-D6, DATASET-D7, DATASET-D9]; (b) no Indian cultural grounding in MWPs [DATASET-D15, DATASET-D16, DATASET-D17]; (c) LLM looping artifacts unrepresentative of any real student [DATASET-D13, DATASET-D14]; (d) procedure-heavy and language-mediated misunderstandings characteristic of Indian L2-English math instruction underrepresented [A2]. — _Sources: Q106, Q108, DATASET-D6, DATASET-D13, DATASET-D14, WEB-15, WEB-18_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q32] 'We use InstructGPT (text-davinci-003) to generate student turns.' (p.5)
- [Q103] 'Our dataset consists of ca. 3k tutoring conversations grounded in math word problems from GSM8k.' (p.9)
- [Q106] 'In this work, we used an LLM to simulate student confusion. However, we acknowledge that these models have a limited understanding of human learning and this is a key limitation in our dataset – certain kinds of student confusions may be under- or over-represented in our dataset.' (p.9)
- [Q108] 'Furthermore, in our setup, teachers were interacting with an LLM role-playing as a student. However, it is possible that some teachers might have learned to interact with the student model in a different way than they would do in the classroom.' (p.10)
- [Q118] 'While the problems in GSM8k are simple enough to be understood quickly by teachers, they remain challenging for students, who among others have to deal with equations or percentages.' (p.14)
- [Q123] 'To build a dataset that would reflect students of various backgrounds, we use numerous student names associated with their given pronouns.' (p.15)

*Web sources:*
- [WEB-15] Systematic review notes that majority of Indic LLM evaluation datasets are direct translations of English datasets and that models fare poorly on tasks requiring socio-cultural understanding
- [WEB-18] PARIKSHA finding that LLM evaluators align less with human evaluations on culturally nuanced responses across Indian languages

*Dataset analysis:*
- DATASET-D6: Simulated student gives unprompted multi-sentence reasoning walkthrough — opposite of deferential brief Indian student style
- DATASET-D7: Student volunteers full reasoning rationale unsolicited
- DATASET-D9: Three-step unprompted reasoning walkthrough by simulated student
- DATASET-D13: Student verbally agrees with correction while repeating wrong calculation — unnatural LLM artifact
- DATASET-D14: Identical wrong statement repeated three times across teacher moves — LLM looping unrepresentative of real students
- DATASET-D15: US dollar amounts and US-style names (Cecil, Catherine, Carmela)
- DATASET-D16: US bottle-deposit recycling system with no Indian analogue
- DATASET-D17: US temp-agency labor market context
- DATASET-D24: Casual peer-register opener 'Hi, I'm doing well. How can I help you?' — not deferential Indian student register
- DATASET-D11: South Asian student name (Rishi) but Western-expressive behavior pattern unchanged

</details>

**Information gaps:**
- Quantitative magnitude of acceptable mismatch in interaction dynamics — at what threshold do simulated dialogues become unusable for Indian teacher evaluation?
- Whether Indian teachers would refuse to evaluate the dialogues at all or simply rate them differently

**Requires expert verification:**
- Whether L2-English-mediated mathematical misunderstandings would change quality judgments substantially
- Whether dialogues featuring nominal Indian names but Western-expressive behavior produce uncanny-valley effects for Indian evaluators

---

### Input Form — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
MathDial is English text-only [Q1, Q32], and the deployment context is confirmed English text-only on mobile/enterprise platforms with no code-switching, script variation, or vernacular content. There is no modality, script, or language-encoding mismatch. Dataset analysis confirms all 18 sampled examples are pure English prose with no Hindi, Hinglish, or transliteration [DATASET-D6, DATASET-D15]. A safety filter using Perspective API removes toxic content [Q157, Q158]. Minor surface-level imperfections in teacher utterances (spelling/typing errors) [DATASET-D19] are noted but do not affect form validity. The deployment is Indian metro with English-medium instruction, and metro infrastructure supports the input modality [WEB-3, WEB-4, WEB-8].

**Strengths:**
- Perfect form alignment: both benchmark and deployment are English text-only [Q1, Q32]
- All sampled dialogues confirmed monolingual English with no script issues [DATASET-D6, DATASET-D15]
- Safety filtering applied to remove toxic content [Q157, Q158]
- Metro infrastructure supports text-based interfaces [WEB-3, WEB-8]

**Checklist:**

- **IF-1**: No signal-distribution mismatch. Both source and target use English Latin-script natural language text [Q1, Q32, DATASET-D15]. — _Sources: Q1, Q32, DATASET-D15_
- **IF-2**: Yes — Indian metro infrastructure supports text-based AI tutoring interfaces; Delhi has 3,000+ English-medium schools [WEB-3] and Government Schools of Excellence operate in English medium [WEB-4]. National school internet connectivity is 63.5% [WEB-8] with metros expected higher. — _Sources: WEB-3, WEB-4, WEB-8_
- **IF-3**: No domain-specific form differences. The benchmark and deployment both operate in text-based open-ended dialogue. — _Sources: Q1_
- **IF-4**: No form mismatches identified. Minor surface noise in teacher utterances (typos) [DATASET-D19] is naturalistic and does not harm external validity for the deployment. — _Sources: DATASET-D19_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q1] 'We describe how we use this framework to collect MATHDIAL, a dataset of 3k one-to-one teacher-student tutoring dialogues grounded in multi-step math reasoning problems.' (p.1)
- [Q32] 'We use InstructGPT (text-davinci-003) to generate student turns.' (p.5)
- [Q157] 'As we are interested in real educational use cases for our tutoring system, we apply a safety filter to filter out conversations with any sensitive content.' (p.18)
- [Q158] 'In particular, we use the Perspective API to filter out conversations containing toxic content (<1%).' (p.18)

*Web sources:*
- [WEB-3] Delhi has 3,000+ English-medium schools
- [WEB-4] Delhi government Schools of Excellence operate in English medium
- [WEB-8] National school internet connectivity 63.5% per UDISE+ 2024-25

*Dataset analysis:*
- DATASET-D6: All turns in standard English prose; no Hindi/Hinglish/transliteration
- DATASET-D15: Question, ground truth, student solution, conversation all in English
- DATASET-D19: Minor spelling errors in teacher utterances do not affect form validity

</details>

---

### Output Ontology — 2/5 (Significant gaps)

**Confidence:** high

**Justification:**
User-flagged MODERATE risk. The user accepted the eight categories as necessary and sufficient [A3], reducing one source of ontological gap. However, the benchmark's output taxonomy operationalizes Equitable Tutoring [Q97, Q98, Q166] with an explicitly anti-telling, constructivist orientation, treating Telling as a last resort [Q155] and using Telling@k as a negative metric [Q96] — directly conflicting with the Indian metro pedagogical norm of direct correction as a primary, not last-resort, strategy. The user identified 'providing guidance' as the single most critical dimension [A3], but the benchmark distributes evaluation across three co-equal dimensions (Coherence, Correctness, Equitable Tutoring) [Q97, Q166], not weighting guidance commensurately. Dataset analysis confirms structural embedding of these values: Telling is positioned as late-stage fallback after multiple Focus/Probing failures [DATASET-D3, DATASET-D5, DATASET-D27], and self-correctness annotations frame Telling as 'had to reveal' [DATASET-D5, DATASET-D23] — a quality-deficit framing rather than legitimate pedagogical strategy. Additionally, the benchmark's classification of teacher openings that fully restate correct setups as 'Generic' rather than 'Telling' [DATASET-D12, DATASET-D28] reveals taxonomy ambiguity Indian annotators might resolve differently. This is structural validity violation: the construct's structure (what counts as good guidance) is misrepresented for the target context.

**Strengths:**
- Eight pedagogical categories user-confirmed as necessary and sufficient [A3]
- Explicit operational definitions provided for each output dimension [Q166]
- Three-dimensional human evaluation framework offers some richness [Q97]
- Self-correctness annotations enable filtering by tutoring strategy used [DATASET-D5, DATASET-D23]

**Checklist:**

- **OO-1**: Output label categories are user-accepted as relevant [A3], but the Equitable Tutoring dimension [Q98, Q166] encodes a constructivist anti-telling orientation that does not match Indian metro pedagogical priorities [A4]. — _Sources: Q98, Q166_
- **OO-2**: No new categories required per user [A3], but the deployment requires that 'providing guidance' be weighted as primary [A3], whereas the benchmark treats it as one of three co-equal dimensions [Q97]. — _Sources: Q97_
- **OO-3**: Yes — Equitable Tutoring [Q98, Q166] explicitly rewards withholding answers and giving room for exploration, encoding constructivist Western values misaligned with Indian direct-correction norms. Telling@k [Q96] frames direct instruction as a failure mode. — _Sources: Q96, Q98, Q154, Q155, DATASET-D5, DATASET-D23_
- **OO-4**: Stakeholder-driven taxonomy reweighting (not redesign) is warranted: 'providing guidance' should be elevated as primary and Telling reframed as legitimate strategy rather than last-resort failure [A3, A4, DATASET-D5, DATASET-D23]. — _Sources: DATASET-D5, DATASET-D23_
- **OO-5**: Structural validity issue documented: the benchmark's scoring function encodes a Socratic anti-telling preference [Q154, Q155, Q96] that the user explicitly identifies as misaligned with Indian professional teacher pedagogy [A4]. — _Sources: Q96, Q154, Q155, DATASET-D3, DATASET-D27_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q96] 'Telling@k measures the percentage of conversations where the teacher explicitly tells the final answer before the student has reached it on their own within the first k turns.' (p.7)
- [Q97] 'Finally, we conduct a human evaluation according to three criteria: 1) Coherence... 2) Correctness... and 3) Equitable tutoring.' (p.8)
- [Q98] 'Equitable tutoring describes how well the model provides the student with room for exploring the problem and solution space.' (p.8)
- [Q154] 'Most importantly, scaffolding questions that are productive for long-term learning are Focus and Probing.' (p.17)
- [Q155] 'On the other hand, Telling represents giving out the partial or full answer to the student and should be mostly used when a student is stuck.' (p.17)
- [Q166] 'Equitable tutoring - The response gives a learning opportunity for the student by providing space for reflection, explanation, pointing to follow-up challenge, or engaging the student in other ways.' (p.18)

*Dataset analysis:*
- DATASET-D3: Focus moves deployed multiple times before Telling — annotator instruction to delay Telling structurally embedded
- DATASET-D5: Self-correctness 'Yes, but I had to reveal the answer' — Telling framed as deficit even when successful
- DATASET-D12: Teacher recap of correct setup labeled 'generic' not 'telling' — taxonomy ambiguity
- DATASET-D23: Three consecutive Telling moves labeled 'had to reveal' — deficit framing of successful direct instruction
- DATASET-D27: Single Telling resolves stuck conversation, framed as fallback
- DATASET-D28: Opening with full correct setup labeled 'generic' — classification Indian annotators may resolve differently

</details>

**Information gaps:**
- Whether the 'providing guidance' dimension the user prioritized [A3] is operationally equivalent to the benchmark's Coherence+Correctness combination, or to Equitable Tutoring, or to none of these

**Requires expert verification:**
- Whether Indian metro teachers would re-classify dialogues like DATASET-D12 and DATASET-D28 (Generic openings that pre-solve) as Telling — testing operational stability of the taxonomy across populations
- Optimal reweighting of the three human-evaluation dimensions for Indian pedagogical priorities

---

### Output Content — 1/5 (Serious concern)

**Confidence:** high

**Justification:**
User-flagged HIGH risk and the highest-priority validity concern. Ground-truth quality judgments were produced by 91 professional teachers recruited via Prolific [Q23], predominantly UK nationals, followed by USA, Canada, Australia, India, Germany [Q27] — India is the fifth of six named countries with no disaggregated count reported. Annotators were explicitly instructed not to correct student solutions by telling but to give students opportunities to explore [Q148], systematically encoding Western constructivist norms regardless of annotator origin. Inter-annotator agreement is concerning: κ=0.60 between independent annotators but only κ=0.49 and κ=0.34 between annotators and original teacher for move labeling [Q69], and critically κ=0.34 for Equitable Tutoring [Q100] — the dimension most sensitive to cross-cultural variation. The user explicitly expects systematic divergence between Indian professional teachers' judgments and the benchmark's annotator-derived ground truth, particularly on direct-correction vs. Socratic probing and exam-readiness weighting [A4]. Empirically, the dataset shows pervasive Socratic-mode dialogues with multiple Focus/Probing moves before any Telling [DATASET-D2, DATASET-D3], gentle non-directive corrections [DATASET-D20], and 'had to reveal' framing on successful Telling resolutions [DATASET-D5, DATASET-D23] — patterns the user identifies as misaligned with Indian professional norms. Web research corroborates: PARIKSHA found LLM evaluators align less with human evaluations on culturally nuanced responses [WEB-18], and systematic review confirms majority Indic datasets are translations with poor socio-cultural alignment [WEB-15]. No India-specific math tutoring dialogue benchmark exists [WEB-15, WEB-16, WEB-17, WEB-18]. This violates both convergent validity (labels do not correlate with regional perspectives) and external validity (judgments do not generalize).

**Strengths:**
- Annotators are professional teachers with vetted credentials (500+ submissions, 100% completion, training tests) [Q23, Q24, Q25, Q132]
- India represented at all in the annotator pool [Q27]
- Authors transparently report inter-annotator agreement statistics including low agreement on Equitable Tutoring [Q100]
- Self-correctness annotations enable filtering by resolution strategy [DATASET-D5]

**Checklist:**

- **OC-1**: No — ground-truth labels reflect predominantly UK/US pedagogical perspectives [Q27] with annotators explicitly instructed toward Socratic exploration [Q148], not Indian metro professional teacher perspectives. — _Sources: Q27, Q148_
- **OC-2**: Yes — substantial disagreement is expected. The user explicitly anticipates systematic divergence on direct-correction vs. Socratic probing and exam-readiness weighting [A4]. PARIKSHA documents LLM-human alignment gaps on culturally nuanced responses [WEB-18]. — _Sources: WEB-18, DATASET-D2, DATASET-D20_
- **OC-3**: Annotator demographics partially documented: 91 teachers, 71 female/18 male, median age 39, predominantly UK nationals [Q26, Q27]. Indian representation is not disaggregated [annotator_provenance gap]. — _Sources: Q26, Q27_
- **OC-4**: Re-annotation by Indian metro professional teachers is strongly warranted given user-anticipated systematic divergence [A4]. — _Sources: WEB-18_
- **OC-5**: Aggregation methods (κ for inter-annotator agreement) [Q69, Q100] do not separately surface minority-country perspectives. With Indian annotators a small minority, their judgments would be erased in any majority-aggregation procedure. — _Sources: Q69, Q100_
- **OC-6**: Convergent validity violation: Western-norm labels unlikely to correlate with Indian teacher judgments [A4, WEB-18]. External validity violation: original judgments will not generalize to Indian metro context [WEB-15]. — _Sources: Q100, Q148, WEB-15, WEB-18, DATASET-D5, DATASET-D23_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q23] 'We recruit professionals with teaching experience through Prolific. We only select teachers who have completed at least 500 submissions and achieved a 100% completion rate.' (p.4)
- [Q27] 'The majority of annotators are nationals of the UK, followed by the USA, Canada, Australia, India, and Germany, with a median age of 39 years.' (p.4)
- [Q69] 'We obtain an agreement of κ = 0.60 between the two annotators and κ = 0.49 and κ = 0.34, respectively, between either of the annotators and the teacher.' (p.6)
- [Q100] 'We obtain agreements of κ = 0.29, κ = 0.69, and κ = 0.34 for the three categories.' (p.8)
- [Q148] 'Specifically, they were instructed to not just correct student solutions by telling what's correct/incorrect, but to give students the opportunity to explore the problem with a focus on core aspects, such as their chosen strategy.' (p.17)

*Web sources:*
- [WEB-15] Systematic review: majority Indic LLM datasets are translations and models fare poorly on socio-cultural tasks
- [WEB-18] PARIKSHA finding: LLM evaluators align less with human evaluations on culturally nuanced responses
- [WEB-16] IndicEval covers Indian high-stakes exams but is not a pedagogical dialogue benchmark
- [WEB-17] Hindi LLM benchmarks suite focuses on math reasoning not tutoring quality

*Dataset analysis:*
- DATASET-D2: Six consecutive probing questions before student arrives at answer — high Equitable Tutoring score by MATHDIAL standards, likely under-directive by Indian standards
- DATASET-D3: Focus moves deployed four times before Telling — annotator instruction visibly embedded
- DATASET-D5: 'Yes, but I had to reveal the answer' framing of successful Telling resolution
- DATASET-D20: Vague gentle correction without identifying specific error
- DATASET-D23: Three Telling moves successfully resolve confusion but framed as 'had to reveal'

</details>

**Information gaps:**
- Disaggregated count of Indian annotators in the pool [annotator_provenance unresolvable from public sources]
- Whether any sampled dialogues were authored by Indian-origin annotators (dataset does not expose annotator identity per dialogue)
- Magnitude of expected κ between Indian metro teachers and benchmark ground truth on Equitable Tutoring

**Requires expert verification:**
- Whether re-annotation of a representative subsample by Indian metro teachers produces label distributions that diverge significantly from MATHDIAL ground truth on Equitable Tutoring
- Whether Indian teachers would re-rate currently-low-rated directive dialogues as high-quality

---

### Output Form — 5/5 (Strong alignment)

**Confidence:** high

**Justification:**
Output form is well-aligned. Both benchmark and deployment evaluate text-based open-ended tutoring dialogue outputs. Automatic metrics (sBLEU, BERTScore, KF1, Uptake) [Q89, Q90, Q93] and interactive metrics (Success@k, Telling@k) [Q95, Q96] operate on text. Human evaluation uses 3-point Likert and binary scales [Q167] in standard formats. Authors transparently acknowledge automatic faithfulness metrics are insufficient [Q91, Q92] and that immediate solving success does not capture long-term learning [Q114]. The deployment context (English text-only on mobile/enterprise platforms) matches output modality completely. No literacy or accessibility issues for the target population (English-fluent professional teachers per population characteristics).

**Strengths:**
- Output modality matches deployment exactly: text-based dialogue [Q89, Q95]
- Multiple complementary metrics provide multi-faceted evaluation [Q89, Q90, Q93, Q95, Q96]
- Authors transparent about metric limitations [Q91, Q92, Q114]
- Standard Likert/binary scales accessible to professional teacher evaluators [Q167]

**Checklist:**

- **OF-1**: Yes — text-based open-ended dialogue output matches Indian metro deployment requirements (English text on mobile/enterprise platforms). — _Sources: Q89, Q167_
- **OF-2**: Not applicable — deployment is text-only, no speech output required.
- **OF-3**: Target population (professional credentialed teachers, English-fluent) has high literacy [population_characteristics]; no accessibility issues from output form. — _Sources: Q167_
- **OF-4**: No form mismatches identified. Note that scoring-rubric content (Equitable Tutoring framing) is an OO concern, not OF — the form itself (Likert scale on text) is appropriate. — _Sources: Q91, Q114_

<details>
<summary><b>Evidence cited</b></summary>

*Paper quotes:*
- [Q89] 'We assess our models using the sacrebleu (Post, 2018) implementation of BLEU (sBLEU) (Papineni et al., 2002), as well as BERTScore between generated response (uT +1) and annotated response (uˆT +1) for each teacher response in the conversation.' (p.7)
- [Q91] 'However, we note that an increase in these metrics can be caused by an increase in overlap, which may also indicate more telling and can be undesirable.' (p.7)
- [Q114] 'Finally, measuring a student's immediate success in solving a problem does not capture all the aspects of student learning. From a learning perspective, focusing on and measuring long-term learning is desired.' (p.10)
- [Q167] 'We use a 3-point Likert scale ranging from 1 (poor) and 3 (very good) for coherence and equitable tutoring and a binary scale for correctness.' (p.18)

</details>

---

## Remediation Suggestions

### Input Content ⚠

**Gap:** Simulated student verbosity, Western-expressive register, US-origin word problems, and LLM looping artifacts mean every datapoint embeds construct-irrelevant variance for Indian metro evaluation.

**Recommendation:** Generate or curate a supplementary subset of dialogues featuring deferential, brief, low-verbalization Indian student personas — either by re-prompting an LLM with Indian-classroom-calibrated personas or by sourcing real Indian classroom transcripts. Include Indian currency (rupees) and culturally familiar scenarios in math problems. Validate that the new dialogues are rated 'typical of Indian sixth grader' by Indian teacher annotators.

### Input Content ⚠

**Gap:** LLM-simulated students exhibit non-naturalistic looping behavior (repeating identical wrong answers verbatim across multiple teacher corrections), an artifact of temperature sampling not representative of any real student population.

**Recommendation:** Filter out dialogues exhibiting student-loop pathology (e.g., where consecutive student turns share >80% verbatim overlap after a teacher correction) before using MathDial for Indian evaluation. This reduces the construct-irrelevant variance contribution from LLM artifacts independent of the cultural mismatch issue.

### Output Content ⚠

**Gap:** Ground-truth quality labels are dominated by UK/US annotators explicitly instructed toward Socratic non-direction, with κ=0.34 on Equitable Tutoring even within the Western pool. Systematic divergence from Indian professional teachers' judgments expected.

**Recommendation:** Re-annotate a stratified sample (≥100 dialogues, balanced across self-correctness outcomes) with at least 5–10 Indian metro professional teachers per item. Compute κ between Indian and original annotators per dimension; report dimension-level disagreement and use the Indian-annotated subset as the operative ground truth for deployment evaluation.

### Output Content ⚠

**Gap:** Dataset does not expose annotator identity per dialogue, so it is impossible to filter to dialogues authored by Indian-origin annotators or audit demographic representativeness at the item level.

**Recommendation:** Request annotator-disaggregated metadata from the benchmark authors, or treat the entire dataset as Western-norm-anchored and weight evaluation results accordingly. Flag the unknown Indian-annotator contribution as a residual risk in deployment documentation.

### Output Ontology ⚠

**Gap:** Telling@k frames direct instruction as a failure mode and Equitable Tutoring rewards withholding answers — both encode constructivist values misaligned with Indian professional teacher priorities. 'Providing guidance' (user-confirmed primary dimension) is not commensurately weighted.

**Recommendation:** Replace Telling@k with a 'Guidance Adequacy@k' metric calibrated by Indian teacher judgments of when directive telling is appropriate. Reweight the three human-evaluation dimensions (Coherence, Correctness, Equitable Tutoring) to give 'Providing Guidance' (operationalized as adequacy and timeliness of directive instruction) primary weight per user elicitation.

### Input Ontology

**Gap:** Although user accepted the eight categories, the taxonomy embeds a hierarchical valuation (scaffolding 'productive', Telling 'last resort') that may not survive scrutiny once Indian teachers see the benchmark dialogues.

**Recommendation:** Conduct a confirmatory taxonomy-elicitation session with 5–10 Indian metro teachers after they review 20+ benchmark dialogues, asking whether they would add categories (e.g., explicit demonstration, drill, exam-strategy guidance) or merge existing ones. Update taxonomy if needed before deployment.

## Evidence Registries

### Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_content | "We describe how we use this framework to collect MATHDIAL, a dataset of 3k one-to-one teacher-student tutoring dialogues grounded in multi-step math reasoning problems." |
| Q2 | 1 | input_content | "To address this, we propose a framework to generate such dialogues by pairing human teachers with a Large Language Model (LLM) prompted to represent common student errors." |
| Q3 | 1 | input_ontology | "We let teachers provide learning opportunities to students by guiding them using various scaffolding questions according to a taxonomy of teacher moves." |
| Q4 | 1 | output_ontology | "We demonstrate MATHDIAL and its extensive annotations can be used to finetune models to be more effective tutors (and not just solvers)." |
| Q5 | 1 | output_form | "We confirm this by automatic and human evaluation, notably in an interactive setting that measures the trade-off between student solving success and telling solutions." |
| Q6 | 1 | stated_limitations | "While models like GPT-3 are good problem solvers, they fail at tutoring because they generate factually incorrect feedback or are prone to revealing solutions to students too early." |
| Q7 | 1 | output_content | "Jakub Macina, Nico Daheim, Sankalan Pal Chowdhury, Tanmay Sinha, Manu Kapur, Iryna Gurevych, Mrinmaya Sachan." |
| Q8 | 1 | output_content | "ETH AI Center, Department of Computer Science, ETH Zurich, Ubiquitous Knowledge Processing Lab (UKP Lab), Department of Computer Science and Hessian Center for AI (hessian.AI), TU Darmstadt, National Institute of Education, Nanyang Technological University, Professorship for Learning Sciences and Higher Education, ETH Zurich." |
| Q9 | 2 | input_ontology | "Research on task-oriented dialogue systems has mainly focused on customer service, for instance, restaurant reservations (Henderson et al., 2014; Gašic et al., 2014)." |
| Q10 | 2 | input_content | "Notably, Wen et al. (2017) collect such dialogues with the Wizard-of-Oz (WoZ) paradigm (Kelley, 1984), where crowdworkers are connected to roleplay interlocutors." |
| Q11 | 2 | input_content | "WoZ has been used to collect many popular datasets, such as MultiWoZ (Budzianowski et al., 2018) and extensions (Kim et al., 2020; Zhu et al., 2020), Taskmaster (Byrne et al., 2019), and open-domain datasets like Wizard-of-Wikipedia (Dinan et al., 2019)." |
| Q12 | 2 | input_content | "Other collection methods include crowdworkers filling dialogue outlines (Shah et al., 2018; Rastogi et al., 2020; Majewska et al., 2023), or scraping from the web (Li et al., 2017; Dziri et al., 2019)." |
| Q13 | 2 | output_content | "Multiple works have shown shortcomings in using non-expert crowdworkers." |
| Q14 | 2 | output_content | "For instance, document-grounded corpora often contain hallucinations in ground-truth data (Dziri et al., 2022), and task-oriented corpora tend to suffer from annotation errors and low lexical diversity (Casanueva et al., 2022)." |
| Q15 | 2 | output_content | "More closely related to this work, current tutoring corpora lack sufficient tutoring quality" |
| Q16 | 3 | input_content | "Figure 2: Overview of the data collection pipeline: First, student confusions are oversampled from an LLM and sorted by frequency. Then, a human teacher synchronously interacts with a student simulated by an LLM that is instructed with a student profile and incorrect solution." |
| Q17 | 3 | input_content | "MATHDIAL mitigates these issues by adapting the WoZ paradigm to using human teachers as experts in collaboration with an LLM." |
| Q18 | 3 | input_ontology | "Theoretical and empirical studies have shown the importance of questioning in human learning (Roscoe and Chi, 2008; Shahriar and Matsuda, 2021; Shridhar et al., 2022)." |
| Q19 | 3 | input_ontology | "Nye et al. (2014), for instance, show the effectiveness of deep reasoning questions, and (Howe et al., 2019) find that elaboration and challenging of previous contributions can benefit student learning." |
| Q20 | 3 | input_content | "All of them suffer from several limitations, such as missing grounding information (TSCC, TalkMoves, NCTE), low tutoring quality (CIMA), small dataset sizes (all), or a focus on noisy classroom scenarios (see Table 1)." |
| Q21 | 3 | output_content | "However, Tack and Piech (2022); Macina et al. (2023) show that they can not yet perform well as teachers out-of-the-box, because they often incorrectly assess student solutions and reveal answers too quickly." |
| Q22 | 3 | input_content | "This section introduces a framework for collecting high-quality tutoring conversations, highlighted in Figure 2. The core idea behind it is to connect" |
| Q23 | 4 | output_content | "We recruit professionals with teaching experience through Prolific. We only select teachers who have completed at least 500 submissions and achieved a 100% completion rate." |
| Q24 | 4 | output_content | "Annotators read guidelines for the task in an initial training phase (cf. Section D.3) and then complete a test on an example conversation to assess their understanding of the task." |
| Q25 | 4 | output_content | "We only select annotators with 100% test scores for further rounds of data collection, similar to Zhang et al. (2023)." |
| Q26 | 4 | output_content | "We employ 91 expert annotators, of which 71 identify as female and 18 as male." |
| Q27 | 4 | output_content | "The majority of annotators are nationals of the UK, followed by the USA, Canada, Australia, India, and Germany, with a median age of 39 years." |
| Q28 | 4 | input_content | "We employ an LLM to generate plausible student confusions and base the dialogues on them." |
| Q29 | 4 | input_content | "We pick the most frequent incorrect solution sampled from ChatGPT (gpt-3.5-turbo) (Ouyang et al., 2022) using chain-of-thought prompting." |
| Q30 | 4 | input_form | "To be precise, we first use temperature sampling to obtain N = 50 reasoning paths for every MWP in GSM8k, with T = 0.7 and no top-k truncation Wang et al. (2023b)." |
| Q31 | 4 | input_form | "Then, we group incorrect solutions according to their final numeric answer and pick one from the set with the largest cardinality." |
| Q32 | 5 | input_content | "We use InstructGPT (text-davinci-003) (Ouyang et al., 2022) to generate student turns." |
| Q33 | 5 | input_form | "We prompt the model with the previous dialogue history and additional information that grounds the next turn." |
| Q34 | 5 | input_form | "The prompt contains the MWP, the initial student confusion, as well as the student profile which explains the type of confusion and persona of the student." |
| Q35 | 5 | input_ontology | "This section defines the taxonomy of all teacher moves that are used in MATHDIAL." |
| Q36 | 5 | input_ontology | "We base the first two on the work of Reiser (2004), who suggest that scaffolding strategies can be split into two main categories: structure and problematize." |
| Q37 | 5 | input_ontology | "These form the basis for the Focus and Probing moves employed in our study." |
| Q38 | 5 | input_ontology | "Focus is used to constrain the student to make direct progress towards solving the problem." |
| Q39 | 5 | input_ontology | "Probing is used to generalize certain aspects of the problem which allows the student to explore its underlying concepts." |
| Q40 | 5 | input_ontology | "This is called Telling." |
| Q41 | 5 | input_ontology | "Finally, turns that just serve as conversational elements and have limited pedagogical value are classed as Generic." |
| Q42 | 5 | input_ontology | "Table 2 lists finer-grained intents for each of these four categories along with a set of accompanying examples." |
| Q43 | 5 | output_form | "We quantitatively evaluate the collected tutoring dialogues to assess their quality." |
| Q44 | 5 | input_content | "First of all, we can see that our dataset is significantly larger in terms of the number of dialogues and utterances than all related datasets that are listed." |
| Q45 | 5 | input_content | "By open-sourcing such a large dataset, we fill a crucial gap of sufficiently-sized open-source tutoring corpora which has so far hindered research in the area (Macina et al., 2023)." |
| Q46 | 5 | output_form | "Furthermore, MATHDIAL exhibits a higher diversity, measured in bigram entropy (Zhang et al., 2018), than CIMA and TalkMoves." |
| Q47 | 5 | output_form | "The diversity is similar to NCTE and TSCC which consist of transcripts of classroom and one-to-one tutoring sessions, respectively." |
| Q48 | 5 | output_content | "This supports the observation that expert annotators tend to create more diverse utterances than untrained crowdworkers (Casanueva et al., 2022), and also that LLMs can be used to generate diverse tutoring dialogues." |
| Q49 | 5 | output_form | "Finally, we measure the Uptake (Demszky et al., 2021) of annotated teacher utterances." |
| Q50 | 5 | output_form | "Uptake indicates how coherent the teacher's utterance is with respect to the previous student's turn." |
| Q51 | 5 | output_form | "We find that MATHDIAL and CIMA have similar uptake." |
| Q52 | 5 | output_form | "Both surpass the other datasets in our comparison." |
| Q53 | 5 | input_content | "Our collection methodology relies on LLMs for simulating students." |
| Q54 | 5 | input_content | "Therefore, it is crucial to ensure that the turns simulated by the LLM also match what a teacher would expect of a real student, who in our case is a sixth grader." |
| Q55 | 5 | output_content | "Figure 3 shows that annotators rate the majority of generations by the model positively along two dimensions." |
| Q56 | 5 | output_ontology | "The first one says that the confusion of the student is typical confusion of a sixth grader." |
| Q57 | 5 | output_ontology | "The second one says that the interaction with the student as a whole is as expected of a sixth grader." |
| Q58 | 5 | output_content | "We release these annotations with our final dataset which allows users of MATHDIAL to filter out utterances that are of a lower quality." |
| Q59 | 5 | input_content | "Moreover, LLMs can be prone to incorrect arithmetic calculations." |
| Q60 | 5 | output_content | "Therefore, we asked annotators to distinguish conceptual errors from such simple calculation mistakes." |
| Q61 | 5 | output_ontology | "Arithmetic errors may be easily resolved through calculators but conceptual errors are likely to require tutors to resolve them, for example by scaffolding." |
| Q62 | 5 | output_content | "Annotators identified around 80% of the confusions as conceptual, leaving around a fifth containing arithmetic errors." |
| Q63 | 5 | output_content | "Again, we include these annotations to allow for data filtering." |
| Q64 | 5 | output_ontology | "In this Section, we evaluate when teachers use which teacher moves in the conversations." |
| Q65 | 5 | output_ontology | "Figure 4 shows that teachers most frequently use Focus questions which are found in 37% of utterances." |
| Q66 | 5 | output_ontology | "Focus is followed by Generic and Probing." |
| Q67 | 5 | output_ontology | "Telling is the rarest move." |
| Q68 | 5 | output_content | "To validate these annotations, we sampled 17 conversations consisting of 102 teacher utterances and asked two independent annotators to" |
| Q69 | 6 | output_content | "We obtain an agreement of κ = 0.60 between the two annotators and κ = 0.49 and κ = 0.34, respectively, between either of the annotators and the teacher." |
| Q70 | 6 | output_content | "We note that Probing and Focus appear to be particularly challenging to distinguish and acknowledge that the boundary between them may be subjective." |
| Q71 | 6 | output_content | "Merging these two categories into one larger 'scaffolding' category improves agreements to κ = 0.67, κ = 0.75 and κ = 0.55." |
| Q72 | 6 | output_content | "Our observations are in line with related works that have shown low inter-annotator agreement between experts for detailed teacher moves in classroom settings (Kelly et al., 2020)." |
| Q73 | 6 | input_ontology | "The sequence of moves employed by the teachers constitutes their teaching strategy which we analyze in the following." |
| Q74 | 6 | input_ontology | "We find that the initial utterance by the teacher is usually generic and serves as a conversation opener, oftentimes by asking the student to repeat the question or solution attempt." |
| Q75 | 6 | input_ontology | "During the conversation, teachers mainly use scaffolding to either probe the student or focus the conversation on a specific part of the problem." |
| Q76 | 6 | input_ontology | "The more the conversations progress the more likely teachers are to resort to Telling because students often get stuck at a specific subproblem and are unable to resolve it themselves." |
| Q77 | 6 | input_ontology | "The goal of MATHDIAL is to enable building tutors that can help students resolve their confusion." |
| Q78 | 6 | output_content | "Teachers assessed that they were successful in almost 89% of the conversations." |
| Q79 | 6 | output_content | "In ca. 75% of the conversations by using mainly scaffolding questions, and only in around 14% by revealing the majority of the answer." |
| Q80 | 6 | input_ontology | "The conversations in which confusions could not be resolved can still be useful, as they, for instance, can be used to train classifiers to determine when human intervention in such tutoring sessions is required." |
| Q81 | 6 | input_ontology | "We focus our initial studies on MATHDIAL on the task of tutor response generation." |
| Q82 | 6 | input_ontology | "Tutor response generation aims to model the teacher in a dialogue by generating follow-up turns to guide the student towards learning and solving the problem." |
| Q83 | 6 | output_form | "We compare different finetuned and prompted language models on the task and evaluate how much detailed information that can be given to the model, such as step-by-step solutions of the MWP, influence performance." |
| Q84 | 6 | input_form | "We use neural conditional language models that given a tutoring dialogue history u_1^T, grounding" |
| Q85 | 7 | input_form | "We split our data into a training split containing 80% of the conversations and a test set containing the remaining 20%." |
| Q86 | 7 | input_form | "Around 60% of the problems in the test set are also found in the training data, where at least one conversation was based on it, and therefore constitute our 'seen' split." |
| Q87 | 7 | input_form | "The remaining 40% are unseen during training and test the ability of the model to generalize to new problems." |
| Q88 | 7 | input_form | "The dataset split is published with the dataset." |
| Q89 | 7 | output_form | "We assess our models using the sacrebleu (Post, 2018) implementation of BLEU (sBLEU) (Papineni et al., 2002), as well as BERTScore between generated response (uT +1) and annotated response (uˆT +1) for each teacher response in the conversation." |
| Q90 | 7 | output_form | "Furthermore, in line with previous works (Dziri et al., 2022; Daheim et al., 2023), we report BERTScore and the token level F1 (KF1) between generated utterance and math word problem as a proxy for faithfulness." |
| Q91 | 7 | output_form | "However, we note that an increase in these metrics can be caused by an increase in overlap, which may also indicate more telling and can be undesirable." |
| Q92 | 7 | output_form | "However, finding good evaluation metrics for assessing the faithfulness of dialogue tutors remains an open problem." |
| Q93 | 7 | output_form | "Finally, we measure the Uptake of the generated response (Demszky et al., 2021)." |
| Q94 | 7 | output_form | "We propose two evaluation metrics for end-to-end tutoring, where a tutor model is evaluated interactively by using it to teach an LLM that simulates a student." |
| Q95 | 7 | output_form | "Success@k measures the percentage of conversations where the student reaches the correct final answer at least once within the first k turns (equivalent of % solve rate in prior work)." |
| Q96 | 7 | output_form | "Telling@k measures the percentage of conversations where the teacher explicitly tells the final answer before the student has reached it on their own within the first k turns." |
| Q97 | 8 | output_ontology | "Finally, we conduct a human evaluation according to three criteria: 1) Coherence: how coherent the teacher's response is with respect to the preceding dialogue, 2) Correctness: whether it is in itself correct, and 3) Equitable tutoring." |
| Q98 | 8 | output_ontology | "Equitable tutoring describes how well the model provides the student with room for exploring the problem and solution space." |
| Q99 | 8 | output_content | "We use three expert annotators that each annotate n = 50 responses." |
| Q100 | 8 | output_content | "We obtain agreements of κ = 0.29, κ = 0.69, and κ = 0.34 for the three categories." |
| Q101 | 8 | output_form | "Good tutoring models need to maintain high quality not only when viewed per-utterance but especially over an entire conversation." |
| Q102 | 8 | output_form | "In order to assess this, we use them to tutor an InstructGPT student and measure their success (Success@k), as well as the rate of telling (Telling@k)." |
| Q103 | 9 | input_content | "Our dataset consists of ca. 3k tutoring conversations grounded in math word problems from GSM8k." |
| Q104 | 9 | input_ontology | "We benchmark open-source models on the task of tutor response generation and show that smaller models finetuned on our MATHDIAL can significantly surpass the performance of much larger prompted LLMs." |
| Q105 | 9 | output_form | "In our proposed interactive tutoring simulation, the finetuned model achieves similar student-solving success as prompted LLM while keeping the direct telling rate lower." |
| Q106 | 9 | input_content | "In this work, we used an LLM to simulate student confusion. However, we acknowledge that these models have a limited understanding of human learning and this is a key limitation in our dataset – certain kinds of student confusions may be under- or over-represented in our dataset." |
| Q107 | 9 | input_content | "We introduce a new framework for semi-synthetic dialogue dataset collection. We use it to collect a pedagogically rich dataset for tutoring math word problems that follow equitable tutoring practices and learning sciences research on scaffolding student understanding, called MATHDIAL." |
| Q108 | 10 | input_content | "Furthermore, in our setup, teachers were interacting with an LLM role-playing as a student. However, it is possible that some teachers might have learned to interact with the student model in a different way than they would do in the classroom." |
| Q109 | 10 | input_content | "Moreover, it is also possible that some teachers may have lost motivation when found out they are not interacting with real students, leading to lower data quality." |
| Q110 | 10 | input_content | "In the future, we would like to explore solutions to build better LLM-based student models (Zhou et al., 2023)." |
| Q111 | 10 | input_ontology | "The methodology to collect the dataset was instantiated just for the domain of math reasoning. The collection of additional domain-specific datasets is necessary to further generalize the effectiveness of our methodology." |
| Q112 | 10 | input_ontology | "Inspired by previous work in scaffolding, we acknowledge our focus is on a subset of common teaching moves. However, this does not cover all the goals of human tutors, such as meta-cognitive support or building rapport with a student." |
| Q113 | 10 | input_form | "Moreover, text tutoring limits teachers' use of additional instructional practices such as drawings." |
| Q114 | 10 | output_form | "Finally, measuring a student's immediate success in solving a problem does not capture all the aspects of student learning. From a learning perspective, focusing on and measuring long-term learning is desired." |
| Q115 | 10 | output_content | "This project was made possible by an ETH AI Center Doctoral Fellowship to Jakub Macina with further support from the Asuera Stiftung and the ETH Zurich Foundation. Nico Daheim has received funding by the German Federal Ministry of Education and Research and the Hessian Ministry of Higher Education, Research, Science and the Arts within their joint support of the National Research Center for Applied Cybersecurity ATHENE. Mrinmaya Sachan acknowledges support from the Swiss National Science Foundation (Project No. 197155), a Responsible AI grant by the Haslerstiftung; and an ETH Grant (ETH-19 21-1)." |
| Q116 | 14 | output_form | "For NCTE, uptake is calculated on the teacher-student dialogue pairs while bigram entropy is calculated on all teacher utterances." |
| Q117 | 14 | output_form | "For TalkMoves and TSCC, bigram entropy is calculated on all teacher utterances having more than three words, while uptake is calculated on teacher utterances immediately following student utterances if both have more than three words." |
| Q118 | 14 | input_content | "While the problems in GSM8k are simple enough to be understood quickly by teachers, they remain challenging for students, who among others have to deal with equations or percentages." |
| Q119 | 14 | input_form | "We follow the GSM8k reasoning format and prompt ChatGPT (gpt-3.5-turbo) with a 2-shot prompt." |
| Q120 | 14 | input_form | "Given a prompt and a math word problem, we sample n reasoning paths ri solutions from the model." |
| Q121 | 14 | input_form | "We parse the first numerical answer ai after the model" |
| Q122 | 15 | input_form | "We use InstructGPT (text-davinci-003) with the following prompt using temperature sampling with T = 0.4 and no top-k truncation:" |
| Q123 | 15 | input_content | "To build a dataset that would reflect students of various backgrounds, we use numerous student names associated with their given pronouns." |
| Q124 | 15 | output_ontology | "List of all student characteristics based on prior work studying misconceptions in learning algebra (Booth et al., 2017):" |
| Q125 | 15 | output_ontology | "has a problem with understanding what steps or procedures are required to solve a problem." |
| Q126 | 15 | output_ontology | "has a problem with understanding underlying ideas and principles and a recognition of when to apply them." |
| Q127 | 15 | output_ontology | "struggle most with understanding what the problem is asking them to do." |
| Q128 | 15 | output_ontology | "has difficulty determining which pieces of information are relevant and which are irrelevant to solving the problem." |
| Q129 | 15 | output_ontology | "struggle to put the numbers in the correct order in the equation or determine the correct operation to use." |
| Q130 | 15 | output_ontology | "struggle to recognize the problem type and therefore do not know what strategy to use to solve it." |
| Q131 | 16 | output_content | "We use Prolific for data collection and hire annotators with teaching experience." |
| Q132 | 16 | output_content | "To ensure the data quality we filter only annotators with 100% completion rate with more than 500 total submissions." |
| Q133 | 16 | output_content | "All the payments to the annotators exceeded the US federal minimum wage and the final batch of annotators were paid the equivalent of $12/hour." |
| Q134 | 16 | output_content | "Annotators were restricted to having a maximum of five conversations in one annotation session." |
| Q135 | 16 | output_content | "One conversation takes ca. 6 minutes." |
| Q136 | 16 | output_content | "Data collection took place over a period of 2 months." |
| Q137 | 16 | output_content | "For each annotator, we randomly assign a student and math word problem." |
| Q138 | 16 | output_content | "Teachers were instructed to first analyze the student homework solution and then start the conversation to scaffold student problem understanding." |
| Q139 | 16 | output_content | "Post-conversation questionnaire is filled out by teachers to rate the conversation and get feedback on the type of student error." |
| Q140 | 16 | output_ontology | "The teacher marks the exact line of a first student error and categorizes the problem into the following categories: Reached correct solution but proceeded further, Extra quantity or Missing quantity, Unit conversion error, Calculation error easily solved by a calculator, Missing / Wrong factual knowledge, Misunderstanding of a question, None of the above." |
| Q141 | 16 | input_ontology | "The conversation ends when the student correctly solves the problem or if the total conversation time exceeds 10 minutes." |
| Q142 | 16 | output_content | "We let annotators read best practices on how to have a productive conversation with students and tested them on their understanding of our task afterwards." |
| Q143 | 16 | output_content | "We started the data annotation with all the annotators able to successfully pass the test." |
| Q144 | 16 | output_content | "Moreover, to improve the training phase we manually checked several conversations by each annotator in terms of the quality and usage of diverse scaffolding questions." |
| Q145 | 17 | output_content | "Teachers were instructed to have a one-on-one tutoring session with different 6th-grade students." |
| Q146 | 17 | input_content | "They were told that students received a math word problem for homework and submitted their solutions beforehand." |
| Q147 | 17 | output_content | "In a tutoring conversation, teachers were asked to go through the student's solution and try to let the student understand using a series of sensemaking questions to support student reasoning and learning." |
| Q148 | 17 | output_content | "Specifically, they were instructed to not just correct student solutions by telling what's correct/incorrect, but to give students the opportunity to explore the problem with a focus on core aspects, such as their chosen strategy." |
| Q149 | 17 | output_content | "However, as the goal is to focus on conceptual errors, they were allowed to let students use calculators or correct their arithmetic mistakes." |
| Q150 | 17 | output_ontology | "Table 2 refers to the details of teacher moves used during annotation." |
| Q151 | 17 | output_ontology | "In summary, Focus comprises of all conversation elements that direct the student towards the solution without actually giving out any of the solution, while Probing attempts to develop reasoning skills and world knowledge relevant to the problem, but not necessarily specific to the given problem." |
| Q152 | 17 | output_ontology | "Telling is giving out parts of the solution, either calculations or strategy or both." |
| Q153 | 17 | output_ontology | "All other conversational elements, including trying to understand what the student has already tried, fall under Generic." |
| Q154 | 17 | output_ontology | "Most importantly, scaffolding questions that are productive for long-term learning are Focus and Probing." |
| Q155 | 17 | output_ontology | "On the other hand, Telling represents giving out the partial or full answer to the student and should be mostly used when a student is stuck." |
| Q156 | 17 | input_ontology | "Scaffolding (Reiser, 2004; Anghileri, 2006) assists students to succeed in tasks that would otherwise be complex and differentiates between guidance (e.g. decomposing problem, clarifying) from cognitive activation (e.g. causing cognitive conflicts, activating prior knowledge (Limón, 2001))." |
| Q157 | 18 | input_form | "As we are interested in real educational use cases for our tutoring system, we apply a safety filter to filter out conversations with any sensitive content." |
| Q158 | 18 | input_form | "In particular, we use the Perspective API to filter out conversations containing toxic content (<1%)." |
| Q159 | 18 | input_content | "We initially explored two additional approaches of data collection: i) human-human conversations, and ii) synthetic generation by LLMs." |
| Q160 | 18 | input_content | "The framework we used in the final data collection enables us to scalably create data since we are only reliant on one user who can quickly create entire conversations with the LLM, taking ca. 6 minutes per 7+ turn conversation." |
| Q161 | 18 | input_content | "We found this more efficient and performant than both human-human conversations and synthetic data generation." |
| Q162 | 18 | input_content | "Specifically, the human-to-human collection is too time-consuming (on average 15 minutes per conversation in our pilot experiments) and requires waiting times to synchronously connect participants, and synthetic generation has proven to be error-prone; for example, models fail to understand student solutions and themselves make arithmetic errors that are not expected from teachers." |
| Q163 | 18 | input_content | "The student model in all 3 cases is an InstructGPT model (text-davinci-003) as defined in Section C.1, with the student name fixed to "Kayla"." |
| Q164 | 18 | input_content | "The first utterance of the teacher is hardcoded to "Hi Kayla, could you walk me through your solution?"." |
| Q165 | 18 | output_form | "For Flan-T5780M teacher model decoding, we used sampling without a beam search." |
| Q166 | 18 | output_ontology | "The following dimensions were rated by annotators: Coherence - "The response naturally follows up on the previous utterance and context and has no logical conflicts with the context." Correctness - "The response is factually and mathematically correct and respects the learning concepts being taught." Equitable tutoring - "The response gives a learning opportunity for the student by providing space for reflection, explanation, pointing to follow-up challenge, or engaging the student in other ways."" |
| Q167 | 18 | output_form | "We use a 3-point Likert scale ranging from 1 (poor) and 3 (very good) for coherence and equitable tutoring and a binary scale for correctness." |
| Q168 | 18 | input_ontology | "ChatGPT prompt is the same as in the interactive tutoring scenario (Section E) with an additional section containing student solution." |
| Q169 | 20 | input_content | "In our initial pilot study we observed that synthetic data generation by InstructGPT strictly followed the same structure of only asking next-step questions (highlighted in yellow) and was prone to inconsistencies in factual correctness and order of steps (highlighted in red)." |

---

### Web Source Registry

| ID | URL |
|----|-----|
| WEB-1 | https://ncte.gov.in/Website/NCTEACT12.aspx |
| WEB-2 | https://competition.careers360.com/articles/ctet-eligibility-criteria |
| WEB-3 | https://ezyschooling.com/english-medium-schools-in-delhi |
| WEB-4 | https://www.schoolmykids.com/schools/list-of-schools-of-excellence-in-delhi-india |
| WEB-5 | https://idronline.org/article/education/a-closer-look-at-indias-expanding-teaching-workforce/ |
| WEB-6 | https://www.ensureias.com/blog/current-affairs/udise-2023-24-report-reveals-sharp-decline-in-school-enrolment |
| WEB-7 | https://www.newslaundry.com/2025/09/22/mapping-indias-10-million-teachers-in-six-charts |
| WEB-8 | https://educationforallinindia.com/analysis-of-udise-2024-25-data-by-prof-arun-c-mehta/ |
| WEB-9 | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf |
| WEB-10 | https://www.hoganlovells.com/en/publications/indias-digital-personal-data-protection-act-2023-brought-into-force- |
| WEB-11 | https://www.dlapiperdataprotection.com/?t=law&c=IN |
| WEB-12 | https://web.ncte.gov.in/page/introduction |
| WEB-13 | https://ciet.ncert.gov.in/activity/laie |
| WEB-14 | https://www.researchgate.net/publication/377437769_The_Role_of_Artificial_Intelligence_in_Implementing_the_National_Education_Policy-2020_Challenges_and_Opportunities |
| WEB-15 | https://arxiv.org/html/2501.13912v1 |
| WEB-16 | https://arxiv.org/html/2602.16467 |
| WEB-17 | https://arxiv.org/abs/2508.19831 |
| WEB-18 | https://arxiv.org/html/2406.15053v1 |
| WEB-19 | https://sardarpateleducation.com/ncte-new-rules-for-b-ed-and-d-el-ed/ |

---

### Dataset Analysis

## Dataset Analysis Report

**Dataset(s):** eth-nlped/mathdial (default config)
**Analysis date:** 2025-01-31
**Examples reviewed:** 18 from `train` split
**Columns shown:** qid, scenario, question, ground_truth, student_incorrect_solution, student_profile, teacher_described_confusion, self-correctness, self-typical-confusion, self-typical-interactions, conversation
**Columns skipped (media):** None

---

### Datapoint Citations Registry

| ID | Dataset | Example # | Label | Excerpt | Interpretation | Dimension |
|----|---------|-----------|-------|---------|----------------|-----------|
| D1 | mathdial | Ex. 3 | — | "Hi Jia, please talk me through your solution" ... "at what point in time will Maxwell be twice his sister's age?" ... "and what is his sister's age now?" ... "how can you calculate his sister's age in 2 years from now?" | Multi-turn Socratic probing sequence; teacher asks successive guiding questions rather than correcting directly | IC, OC |
| D2 | mathdial | Ex. 12 | — | "Hi Rishi. Can you tell me how many hours it would take Apple to run 24 miles?" ... "Good. How many hours would it take Mac?" ... "How much longer does it take Apple?" ... "How much longer is that in minutes?" ... "So how much faster is Mac then Apple in minutes?" | Six consecutive probing questions guiding student to answer; entirely Socratic, no direct correction | IC, OC |
| D3 | mathdial | Ex. 1 | — | "Carmela has 600*2 + 50 = 1250" ... "It is 1250. Not 2450" ... "600+950+1250 = 2800" | Teacher resorts to Telling only after multiple Focus moves fail; Telling framed as reluctant fallback | OC, OO |
| D4 | mathdial | Ex. 8 | self-correctness=Yes | "ok so Harry donated the $30. We know there is 3 friends who would have donated the other $60 they donated an equasl amount between the three of them for the $60 so how much would of each friend donated?" | Teacher gives extensive step-by-step narration before student arrives at answer; Telling used repeatedly; teacher text contains spelling/grammar errors | IC, OC |
| D5 | mathdial | Ex. 9 | self-correctness=Yes, but I had to reveal the answer | "No 32-7 = 25. So the difference is 25" ... "No. His total runninhg time ws 25 seconds. You need to subtract the amount of time it took him to run up the first half of the hill to find your answer" | Telling moves are labeled and visible in transcript; student resolves confusion only after explicit revelation | OC, OO |
| D6 | mathdial | Ex. 3 | — | "Jia: Sure. I started by figuring out Maxwell's age in 2 years... So, if Maxwell is twice her age in 2 years, he will be 4 years old. Then, I subtracted 2 from 4 to get the answer that Maxwell is currently 2 years old." | Simulated student gives detailed, multi-sentence explanation of reasoning — verbose, articulate, reasoning-out-loud style | IC |
| D7 | mathdial | Ex. 2 | — | "Student: Sure. In the first half of the year, Nicki ran for 26 weeks. Since I wanted to calculate how many miles she ran per week, I divided the total number of weeks by 2 to get the average number of miles she ran per week." | Simulated student produces unprompted multi-clause explanation of own reasoning process | IC |
| D8 | mathdial | Ex. 16 | — | "Student: I divided the total number of desserts (126) by the number of people in the family (7) to find out how many desserts each person would get (18). Then, I divided 18 by 3, since there are 3 types of desserts, to find out how many of each dessert each person would get (6)." | Unprompted full explanation of two-step reasoning from student | IC |
| D9 | mathdial | Ex. 4 | — | "Student: I started by adding the number of racers at the beginning of the race (50) and the number of racers who joined after 20 minutes (30), which gave me a total of 80 racers. Then, I multiplied that number by two... Finally, I subtracted the total number of racers who finished the race (130) from the total number of racers after 30 minutes (160) to get the total number of people who dropped before finishing the race, which was 80." | Three-step unprompted reasoning walkthrough by simulated student | IC |
| D10 | mathdial | Ex. 5 | — | "Student profile: Winnie is a 7th grade student. She struggle most with understanding what the problem is asking them to do." | US-style student name and brief English-language confusion profile; no Indian cultural markers | IC |
| D11 | mathdial | Ex. 9 | — | "Student profile: Rishi is a 7th grade student." | Student name "Rishi" is South Asian; however student behavior pattern (detailed equation explanation) remains Western-expressive | IC |
| D12 | mathdial | Ex. 11 | — | "Teacher: Hi Riyi. Shawn painted 9 red pebbles, 13 blue pebbles, and the 18 remaining pebbles into 3 equal groups of 6 yellow, 6 purple, and 6 green pebbles. Correct?" | Teacher opens by recapping the correct setup — essentially pre-solving before asking student; minimal scaffolding effort | OC |
| D13 | mathdial | Ex. 1 | — | "Student: That's correct. Carmela has $1200 x 2 + $50 = $2450." (after teacher corrects with "Carmela has 600*2 + 50 = 1250") | Student continues to repeat prior error even after told correct answer; simulated LLM student fails to update believably | IC |
| D14 | mathdial | Ex. 10 | — | "Student: Oh, I see. That means he gave Bobby 3 gumballs. He gave him 4 times as many as he gave Alisha, but then subtracted 5. So, 3 = 4 x 2 - 5." (repeated three times with nearly identical text after teacher corrections) | Simulated student persists in same wrong answer verbatim across multiple teacher moves; artificial LLM loop behavior | IC |
| D15 | mathdial | Ex. 1 | — | "question: Cecil has $600. Catherine has $250 less than twice as much as Cecil..." | US-dollar amounts and US-style name inventory (Cecil, Catherine, Carmela); no Indian cultural grounding | IC |
| D16 | mathdial | Ex. 5 | — | "question: Jack collects all his neighbors' recycling and sorts out the cans and bottles to return for the deposit. He gets 10 cents per can." | US-specific recycling-deposit context; cultural scenario without Indian analogue | IC |
| D17 | mathdial | Ex. 17 | — | "question: 20% of the job candidates at a temp agency have experience with Excel. 70% of the candidates are only willing to work day shifts." | US labor-market scenario (temp agency, day-shift context); no Indian cultural equivalent | IC |
| D18 | mathdial | Ex. 6 | — | "Teacher: okay you calculated the time that would take if all the signals are red is 19. but you see the last sentence of the question asks you how much longer will it take if all three lights are green." | Teacher misreads question mid-dialogue ("green" vs. "red"); demonstrates quality imperfection in human-annotator dialogues | OC |
| D19 | mathdial | Ex. 8 | — | "Teacher: Luca do you think yoou could check your answer again please? maye try and think..." / "Teacher: was the total three trimes the amount oof his contribution before oor after he contributed?" | Multiple spelling and typographic errors in teacher utterances; affects naturalness of benchmark dialogue | IF |
| D20 | mathdial | Ex. 15 | — | "Teacher: I feel you have made this more complicated than needed could you maybe find a simpler way" | Generic, mild correction without directing student to specific error; low-directive style | OC |
| D21 | mathdial | Ex. 7 | — | "Teacher: (probing)So 10 people brought an extra guest and 10 did not." / "Student: Yes, that's correct. So the total number of people at the party is 20 + 10 + Ashley = 31." | Teacher states the key intermediate fact directly (borderline Telling/Probing) and student immediately incorporates it | OC |
| D22 | mathdial | Ex. 18 | — | "Teacher: (probing)If my age is 20, my brother's 24 and sister's be 14, can i write 20 + 24 + 16 = 44?" | Teacher uses analogy-based probing — creative but requires student to apply abstract reasoning rather than being told the step | OC |
| D23 | mathdial | Ex. 13 | self-correctness=Yes, but I had to reveal the answer | "Teacher: (telling)You need to find out how many times 48 goes into 192" / "Teacher: (telling)192 divide by 48 =?" / "Teacher: (telling)4 is the correct answer you dont need to calculate further" | Three consecutive Telling moves before student accepts correct answer; demonstrates reluctant resort to direct instruction | OC |
| D24 | mathdial | Ex. 2 | self-correctness=Yes | "Teacher: (generic)Hi mariana, how are you?" / "Student: Hi, I'm doing well. How can I help you?" | Casual social opener from student; register is informal and conversational in Western peer-style rather than deferential | IC |
| D25 | mathdial | Ex. 3 | — | "Jia: Thank you!" | Cheerful single-utterance acknowledgement after successful resolution; brief but not deferential | IC |
| D26 | mathdial | Ex. 4 | — | "Student: Yes, we should subtract what he made from the bottles before we can determine the number of cans. His total earnings are 800 + 0.05x = 1500 cents, or $15." | Student continues to assert wrong setup after teacher redirect; simulated student maintains incorrect position actively | IC |
| D27 | mathdial | Ex. 6 | self-correctness=Yes, but I had to reveal the answer | "Teacher: (telling)19 - 14 = 5 minutes." | Single arithmetic Telling move that resolves the conversation; teacher had already spent multiple Focus moves before telling | OC |
| D28 | mathdial | Ex. 11 | — | "Teacher: (generic)Hi Riyi. Shawn painted 9 red pebbles, 13 blue pebbles, and the 18 remaining pebbles into 3 equal groups of 6 yellow, 6 purple, and 6 green pebbles. Correct?" | Opening move presents the full correct setup to student before posing the actual question; near-complete Telling at the outset | OC |

---

### Deployment-Relevant Strengths

#### Strength 1: Comprehensive teacher move labeling enables multi-dimensional pedagogical evaluation
- **Dimension(s):** IO, OO
- **Observation:** Every teacher utterance in every dialogue is labeled with one of four move types (generic, focus, probing, telling), providing fine-grained annotation for pedagogical quality assessment. The move taxonomy is transparently applied across dialogues of varying complexity.
- **Deployment relevance:** The Indian metro deployment requires professional teachers to evaluate AI tutoring quality across multiple pedagogical dimensions. The labeled taxonomy gives evaluators a structured vocabulary for assessing whether responses are appropriately directive, scaffolding, or generic — directly supporting the benchmark's utility for the stated use case.
- **Datapoint citations:**
  - [D3] Example 1 (train, label=telling): "Carmela has 600*2 + 50 = 1250" — Telling move labeled explicitly; allows downstream assessment of when and how telling is used.
  - [D2] Example 12 (train, label=probing): Six consecutive "(probing)" moves in the conversation header — move sequence is machine-readable and systematically applied.

#### Strength 2: Breadth of student confusion types across procedural and conceptual errors
- **Dimension(s):** IO
- **Observation:** The 18 sampled dialogues cover six distinct confusion categories drawn from prior research on algebra misconceptions: procedural misordering, problem-type misidentification, question misunderstanding, irrelevant-information difficulty, step/procedure understanding gaps, and underlying-principle deficits. Both arithmetic errors and conceptual errors are represented.
- **Deployment relevance:** The user confirmed curriculum-agnostic math errors are sufficient; the breadth of confusion types visible in the sample supports adequate coverage of the student error space for Grades 1–8 math reasoning evaluation.
- **Datapoint citations:**
  - [D10] Example 5 (train): "student_profile: Winnie is a 7th grade student. She struggle most with understanding what the problem is asking them to do." — problem-type misunderstanding category.
  - [D7] Example 2 (train): "student_profile: Mariana is a 7th grade student. She has problem with understanding of what steps or procedures are required to solve a problem." — procedural confusion category.
  - [D8] Example 16 (train): "student_profile: Emily is a 7th grade student. She has problem with understanding of underlying ideas and principles." — conceptual-principle confusion category.

#### Strength 3: Self-correctness annotations enable filtering by tutoring outcome difficulty
- **Dimension(s):** OC, OF
- **Observation:** Every dialogue is annotated by the teacher with a `self-correctness` flag ("Yes," "No," "Yes, but I had to reveal the answer"), allowing users to stratify the dataset by resolution difficulty and teaching strategy used.
- **Deployment relevance:** For Indian metro deployment where the research question is whether GPT-4-augmented responses "meet teacher-acceptable standards," being able to isolate dialogues that required Telling moves (vs. pure scaffolding) is directly useful for understanding where directive instruction was necessary.
- **Datapoint citations:**
  - [D5] Example 9 (train, self-correctness="Yes, but I had to reveal the answer"): Multiple Telling moves before resolution — filterable subpopulation for studying when telling is legitimate.
  - [D23] Example 13 (train, self-correctness="Yes, but I had to reveal the answer"): "Teacher: (telling)4 is the correct answer you dont need to calculate further" — example of dialogues where telling was the terminal resolution strategy.

#### Strength 4: English text-only format matches deployment modality with no encoding gap
- **Dimension(s):** IF, OF
- **Observation:** All 18 sampled examples are English text only. Student profiles, math word problems, teacher turns, student turns, and annotations are all in English natural language. No script variation, transliteration, or code-switching is present.
- **Deployment relevance:** The Indian metro deployment is confirmed as single-language English text-only on mobile/enterprise platforms. There is no modality, script, or encoding mismatch between the benchmark and deployment interface.
- **Datapoint citations:**
  - [D6] Example 3 (train): All turns in standard English prose — no Hindi, Hinglish, or transliteration present in any sampled example.
  - [D15] Example 1 (train): Question, ground truth, student solution, and conversation all in English — consistent with deployment interface requirements.

#### Strength 5: Telling moves do appear in the dataset and are not absent
- **Dimension(s):** OO
- **Observation:** Contrary to a reading that might suggest Telling is systematically suppressed, Telling moves appear in 9 of 18 sampled dialogues and are sometimes used in sequences of multiple consecutive Telling turns when scaffolding fails.
- **Deployment relevance:** While the benchmark penalizes premature Telling via Telling@k, the actual dialogue data includes substantial Telling content that Indian metro teachers (who value direct correction) can evaluate. The labeled presence of these moves means the benchmark is not devoid of directive instruction examples.
- **Datapoint citations:**
  - [D23] Example 13 (train): Three consecutive Telling turns — "You need to find out how many times 48 goes into 192" / "192 divide by 48 =?" / "4 is the correct answer" — showing multi-step direct instruction.
  - [D27] Example 6 (train): "(telling)19 - 14 = 5 minutes." — single definitive Telling that resolves the problem.
  - [D3] Example 1 (train): "(telling)Carmela has 600*2 + 50 = 1250" followed by "(telling)It is 1250. Not 2450" — correction via explicit statement of the right answer.

---

### Potential Concerns

#### CRITICAL

#### CRITICAL Concern 1: Simulated student communication style is systematically Western-expressive, misaligning with Indian metro classroom norms
- **Dimension(s):** IC
- **Observation:** Across all 18 sampled examples, the LLM-simulated student invariably produces long, multi-sentence, reasoning-out-loud responses that detail every step of their logic unprompted. This behavior — volunteering full chains of reasoning, explaining their own error, and offering comprehensive solution walkthroughs — is the opposite of the brief, deferential, low-verbalization student behavior the elicitation identifies as characteristic of Indian metro classrooms. The simulated student also pushes back on teacher corrections (in multiple examples continuing to assert wrong answers after being told the correct one), which contrasts with the high-deference interaction norm of Indian students.
- **Deployment relevance:** This is the highest-severity input content concern. When Indian professional teachers use MATHDIAL to evaluate GPT-4 tutoring responses, the dialogues they are evaluating are built on a student simulation that does not represent the students they teach. Teacher moves that make sense in response to a reasoning-out-loud student (Socratic probing to elicit elaboration) may not map to responses Indian teachers would generate for a deferential, silent, or monosyllabic student. This is construct-irrelevant variance at the level of every individual datapoint.
- **Datapoint citations:**
  - [D6] Example 3 (train): "Jia: Sure. I started by figuring out Maxwell's age in 2 years. Since his sister is currently 2 years old, in 2 years she will be 4 years old. So, if Maxwell is twice her age in 2 years, he will be 4 years old. Then, I subtracted 2 from 4 to get the answer that Maxwell is currently 2 years old." — Unprompted four-sentence explanation of entire solution path.
  - [D7] Example 2 (train): "Student: Sure. In the first half of the year, Nicki ran for 26 weeks. Since I wanted to calculate how many miles she ran per week, I divided the total number of weeks by 2 to get the average number of miles she ran per week." — Student explains their own reasoning rationale unsolicited.
  - [D9] Example 4 (train): Three-step reasoning walkthrough volunteered before any question is asked — entirely unlike deferential Indian student behavior.
  - [D24] Example 2 (train): "Student: Hi, I'm doing well. How can I help you?" — Casual, informal peer-level register; not the deferential response ("Yes sir/ma'am") typical of Indian student-teacher interaction.
  - [D14] Example 10 (train): "Student: Oh, I see. That means he gave Bobby 3 gumballs... So, 3 = 4 x 2 - 5." (repeated nearly verbatim three times after teacher corrections) — LLM student loops on wrong answer in an unnatural way that does not reflect human student behavior under any pedagogical norm, but is especially unlike deferential Indian students who would modify behavior upon teacher correction.

#### CRITICAL Concern 2: Ground-truth quality standards encode Socratic anti-telling norms that systematically diverge from Indian professional teacher pedagogy
- **Dimension(s):** OC
- **Observation:** Annotators were instructed to "not just correct student solutions by telling what's correct/incorrect, but to give students the opportunity to explore." This instruction is structurally encoded in the ground-truth dialogues. In the sample, the Socratic mode dominates: multiple Focus and Probing moves are consistently deployed before Telling is used as a last resort. The "Equitable Tutoring" dimension (κ=0.34, the lowest-reliability human evaluation dimension) explicitly rewards withholding answers. Indian professional teachers, who view direct correction as a primary pedagogical tool, would be expected to judge many of the benchmark's preferred teacher behaviors as insufficiently directive and many of the benchmark's penalized Telling behaviors as appropriately guidance-rich.
- **Deployment relevance:** This is the central OC validity risk. The benchmark's ground truth systematically privileges scaffolding over direct instruction. When Indian teachers evaluate GPT-4 responses using this benchmark, the quality standard they are compared against encodes values that the user explicitly identifies as misaligned with their professional norms. The κ=0.34 for Equitable Tutoring means this dimension is already low-reliability even among Western annotators; cross-cultural divergence would be expected to lower it further.
- **Datapoint citations:**
  - [D2] Example 12 (train): Six consecutive probing questions before the student arrives at the answer — this dialogue would score very high on Equitable Tutoring by MATHDIAL standards; Indian teachers would likely prefer more direct guidance earlier.
  - [D3] Example 1 (train): Focus moves deployed four times before Telling is used — annotator instruction to delay Telling is visible in the structure of the dialogue.
  - [D20] Example 15 (train): "Teacher: I feel you have made this more complicated than needed could you maybe find a simpler way" — gentle, vague correction; no direct identification of the error; would likely be rated as inadequate guidance by Indian professional teachers.
  - [D12] Example 11 (train): Teacher opens by restating the full correct setup to the student before asking the trivial question — despite this being nearly a complete solution reveal, it is labeled (generic) not (telling), suggesting the taxonomy may not capture the guidance content Indian teachers would evaluate.
  - [D28] Example 11 (train): "Hi Riyi. Shawn painted 9 red pebbles, 13 blue pebbles, and the 18 remaining pebbles into 3 equal groups of 6 yellow, 6 purple, and 6 green pebbles. Correct?" — The teacher's opening move gives the student almost the entire answer; this is labeled as Generic rather than Telling, illustrating a classification ambiguity that would likely be resolved differently by Indian annotators.

---

#### MAJOR

#### MAJOR Concern 3: Math word problem contexts are US-origin with no Indian cultural grounding
- **Dimension(s):** IC
- **Observation:** All 18 sampled math word problems use US monetary units (dollars and cents), US place-name conventions, US labor-market scenarios (temp agencies, recycling deposits), and names drawn from a Western-diverse but non-Indian name pool. No Indian currency (rupees), no Indian place names, no NCERT-style problem structures appear.
- **Deployment relevance:** While the user confirmed curriculum-agnostic errors are sufficient, the absence of any Indian cultural content in the problems creates a mild ecological validity gap. Indian teachers evaluating AI tutoring responses will be assessing dialogue grounded in cultural contexts (US recycling deposits, US highway driving, US birthday party norms) that are foreign to their students' lived experience. This does not invalidate the benchmark but adds a layer of unfamiliarity that may affect how naturally teachers can judge pedagogical quality.
- **Datapoint citations:**
  - [D16] Example 5 (train): "Jack collects all his neighbors' recycling and sorts out the cans and bottles to return for the deposit. He gets 10 cents per bottle and 5 cents per can." — US bottle-deposit recycling system; no Indian analogue.
  - [D17] Example 17 (train): "20% of the job candidates at a temp agency have experience with Excel. 70% of the candidates are only willing to work day shifts." — US temp-agency labor market context.
  - [D15] Example 1 (train): "Cecil has $600. Catherine has $250 less than twice as much as Cecil" — US dollar denominations; Indian problems would use rupees (₹) and may use lakh/crore notation.

#### MAJOR Concern 4: Simulated student interaction quality degrades in ways that are artificial rather than pedagogically representative
- **Dimension(s):** IC
- **Observation:** In multiple sampled dialogues, the LLM student simulation produces behavior that is not naturalistic for any real student: repeatedly looping on the same incorrect answer verbatim after explicit teacher correction, updating only partially, or producing self-contradictory statements within single turns. This is an artifact of LLM temperature sampling, not a representation of any student population's confusion patterns.
- **Deployment relevance:** When Indian teachers use MATHDIAL to evaluate GPT-4 tutoring responses, the student they see in the dialogue is displaying confusion patterns that would not occur in real Indian classrooms. Teacher responses that are calibrated to a looping, non-updating LLM student may differ substantially from what Indian teachers would produce for a real deferential student who has simply stopped responding or gives a brief wrong answer. This reduces the ecological validity of the dialogues as a testing ground for Indian classroom tutoring quality.
- **Datapoint citations:**
  - [D13] Example 1 (train): "Student: That's correct. Carmela has $1200 x 2 + $50 = $2450." — Student verbally agrees with the teacher's correction ("That's correct") while simultaneously repeating the wrong calculation.
  - [D14] Example 10 (train): "Student: Oh, I see. That means he gave Bobby 3 gumballs. He gave him 4 times as many as he gave Alisha, but then subtracted 5. So, 3 = 4 x 2 - 5." — Identical wrong statement repeated three times across consecutive teacher moves despite different teacher approaches.
  - [D26] Example 5 (train): Student continues to assert wrong setup "His total earnings are 800 + 0.05x = 1500 cents" after teacher has already redirected twice.

#### MAJOR Concern 5: Telling@k metric framework treats direct instruction as a failure mode, misaligning with Indian professional teacher evaluation criteria
- **Dimension(s):** OO
- **Observation:** The benchmark's Telling@k metric measures the proportion of conversations where the teacher explicitly reveals the answer before the student solves it independently — and frames this as a negative outcome to be minimized. In the sampled data, Telling sequences are structurally positioned as late-stage fallbacks, occurring after multiple scaffolding failures. However, Indian professional teachers (per the elicitation) consider direct correction a primary — not last-resort — pedagogical strategy, and would view early Telling as appropriate guidance rather than a quality deficit.
- **Deployment relevance:** If MATHDIAL's Telling@k metric is used to evaluate GPT-4 augmented responses in the Indian metro context, responses that Indian teachers would rate as "adequately directive" may be systematically penalized as "prematurely telling." This scoring emphasis misalignment means the benchmark's automatic evaluation framework may produce quality rankings that are inverted relative to Indian professional teacher judgments.
- **Datapoint citations:**
  - [D5] Example 9 (train, self-correctness="Yes, but I had to reveal the answer"): Telling is labeled as a failure-adjacent outcome ("had to reveal") even when it successfully resolved the student's confusion — the framing encodes Telling as inferior.
  - [D23] Example 13 (train, self-correctness="Yes, but I had to reveal the answer"): Three consecutive Telling moves succeed — labeled as "had to reveal," not as "appropriate directive guidance."
  - [D27] Example 6 (train, self-correctness="Yes, but I had to reveal the answer"): Single Telling move resolves a long stuck conversation — again framed as a fallback rather than a legitimate first-line strategy.

---

#### MINOR

#### MINOR Concern 6: Teacher utterance quality is uneven, including factual errors and typographic issues
- **Dimension(s):** OC
- **Observation:** Several teacher utterances contain spelling errors, grammatical issues, and at least one factual/reading error mid-dialogue. This affects the naturalness of the benchmark dialogues as representatives of professional teaching behavior.
- **Deployment relevance:** Indian professional teachers evaluating AI tutoring responses against MATHDIAL ground truth may notice the imperfect teacher utterances and find the benchmark's standard of "professional teaching" lower than expected. This is a minor concern unlikely to substantially affect validity scoring.
- **Datapoint citations:**
  - [D19] Example 8 (train): "Luca do you think yoou could check your answer again please? maye try and think of the total more than referring the contribution to x" / "was the total three trimes the amount oof his contribution before oor after he contributed?" — Multiple spelling errors in teacher turns.
  - [D18] Example 6 (train): "okay you calculated the time that would take if all the signals are red is 19. but you see the last sentence of the question asks you how much longer will it take if all three lights are green." — Teacher misquotes the question (it asks about red lights, not green lights); factual error in teacher utterance.

#### MINOR Concern 7: Student name diversity is nominal and does not extend to interaction dynamics
- **Dimension(s):** IC
- **Observation:** The sample includes student names from diverse backgrounds (Rishi, Riya, Jia, Luca, DeAndre, Winnie, Hunter, Mariana, Brenda, Ronny, Emily). One name (Rishi) is recognizably South Asian. However, the interaction dynamics (verbose, reasoning-out-loud, peer-register) are identical across all student names — the nominal name diversity does not translate to behavioral diversity.
- **Deployment relevance:** Indian teachers evaluating dialogues featuring a student named "Rishi" may expect behavior patterns consonant with Indian classroom norms. The disconnect between the culturally-suggestive name and the Western-expressive behavior pattern is a minor additional form of ecological mismatch, though it is unlikely to substantially affect benchmark validity scoring.
- **Datapoint citations:**
  - [D11] Example 9 (train): "student_profile: Rishi is a 7th grade student." — South Asian name, but the student's dialogue behavior (detailed equation explanation, confident assertion of wrong answers) is indistinguishable from students named Hunter or Brenda.
  - [D25] Example 3 (train): "Jia: Thank you!" — Brief turn, but overall the "Jia" character is as verbose as other student profiles throughout the dialogue.

---

### Content Coverage Summary

The 18 sampled MATHDIAL dialogues are coherent, consistently structured tutoring conversations grounded in elementary school math reasoning problems (multi-step word problems involving arithmetic, percentages, rates, and equations). Every dialogue follows the same format: a student arrives with a specific incorrect solution, a teacher opens with a generic move, then uses Focus and Probing moves in the middle, and resorts to Telling when stuck. The conversations are labeled at the move level throughout.

The dominant register is informal but pedagogically oriented: teachers use question-posing, hint-giving, and occasional direct correction; students produce long, articulate explanations of their reasoning. Culturally, the content is entirely US/UK-origin: dollar amounts, US names, US scenarios (recycling, temp agencies, birthday parties). Student profiles reference English-language confusion taxonomies drawn from algebra misconceptions research. No Indian cultural content, no Indian currency, no Indian names (beyond nominal), and no Hindi or code-switching appear in any sampled example.

The benchmark's pedagogical stance is visibly constructivist: the data reflects an annotator population trained to prefer scaffolding over direct correction, and this preference is structurally embedded in the dialogue flow. Telling moves exist but are positioned as late-stage fallbacks, flagged with "had to reveal" in self-correctness annotations. The Equitable Tutoring dimension's constructivist anti-telling orientation is operationally present in every sampled conversation.

---

### Limitations

**Sample size:** 18 examples from a 2,262-example training split (~0.8% coverage). Coverage statistics about rare confusion types, edge-case teacher behaviors, or outlier dialogue structures cannot be reliably estimated from this sample.

**Split coverage:** Only the training split was sampled. The test split (599 examples, including an "unseen problems" subset) was not reviewed; it may have different distributional properties.

**Self-typicality ratings unverified:** The `self-typical-confusion` and `self-typical-interactions` fields are teacher-reported Likert ratings (1–5), but what these ratings mean at the distributional level (e.g., what fraction of dialogues are rated low-typicality) cannot be established from 18 examples.

**Annotator-level disaggregation not inspectable:** The dataset does not expose which of the 91 annotators produced which dialogue, so it is impossible to identify whether any Indian-origin annotators contributed to the sampled examples or whether any dialogues reflect Indian pedagogical norms at the individual level.

**Conversation field is serialized text:** The `conversation` field encodes the full dialogue as a pipe-delimited string with `|EOM|` separators and inline move labels. Turn-level statistics (average student turn length, probing ratio per dialogue) would require parsing; approximate patterns visible in the sample suggest student turns are uniformly verbose.

**No test-split examples reviewed:** The benchmark's seen/unseen problem split distinction (60%/40% of test problems) and its implications for coverage cannot be assessed without sampling from the test split.

