## Use Case
A Hindi-speaking postgraduate- or PhD-qualified teacher in North India uses an LLM-powered mobile or enterprise application to evaluate student responses to multiple-choice questions (MCQs), assign scores (with positive/negative marking), and provide feedback. The benchmark under evaluation (MILU) is being assessed specifically through its Hindi-language MCQ items.

## Target Population
- **Geography:** North India (states such as Uttar Pradesh, Madhya Pradesh, Rajasthan, Bihar, and adjacent regions)
- **Language:** Hindi (Devanagari script; formal/standard register expected)
- **Role:** Postgraduate- or PhD-qualified Hindi-medium teacher with 0–20+ years of experience
- **Curricular scope:** All Hindi state boards (UP, MP, Rajasthan, Bihar, etc.) and central boards (CBSE); English-medium board content is in scope only when translated into Hindi and aligned with Hindi-board norms
- **Assessment format:** Strict MCQ format with a single correct answer per question and positive/negative marking; no open-ended or partial-credit grading

## Elicitation Responses

Q1 [IO]: Does the assessment context involve open-ended/long-form student answers, structured short answers, or primarily factual single-item MCQ questions?
A1: The deployment involves only MCQs with a single correct answer. Scoring is binary in effect: positive marks for correct selections and negative marks for incorrect ones. No partial credit or rubric-based judgment is required.

Q2 [OO]: Should the AI support graded scoring, binary correct/incorrect judgments, or qualitative rubric-based feedback, and in what Hindi register should scoring rationale be expressed?
A2: Because all questions are MCQ-type with a single correct answer, scoring is straightforwardly binary. Graded or rubric-based output is not needed for this deployment.

Q3 [IC]: Does the deployment target a specific board/institution type, or must the AI handle content across multiple curricula, including culturally specific canonical texts and regional reference points?
A3: The deployment must accommodate all Hindi state and central board syllabi. Questions may also be drawn from English-medium boards, provided they are translated into Hindi and aligned in style with Hindi-board norms. Regional and curriculum-specific content (e.g., Tulsidas, Premchand, regional historical figures) should therefore be in scope.

Q4 [OC]: Are student answers and teacher mark schemes in North India likely to reflect norms that diverge from national competitive-exam keyed answers, such that a regionally specific correct answer might differ from a pan-India standard answer?
A4: No significant divergence is expected. Evaluation schemas across boards and states are described as broadly similar, so competitive-exam-sourced answer keys are considered largely compatible with what North Indian teachers would accept as correct.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | MILU's MCQ format from regional/national competitive exams aligns well with the deployment's strict MCQ requirement, but the benchmark must cover the breadth of Hindi state and central board syllabi (not just competitive-exam domains), leaving a potential gap in curricular coverage. |
| IC | HIGH | The deployment spans all Hindi state and central board syllabi, including culturally loaded content (canonical Hindi literature, regional history, local governance) that may be framed differently in competitive-exam-sourced items than in school or university board contexts; translated English-board content adds further surface-level risk. |
| IF | LOWER | Both benchmark and deployment are text-only in Hindi with Devanagari script, a high-resource language-script pairing; no modality mismatch exists. |
| OO | LOWER | Output is binary correct/incorrect label matching, co-designed for the same India-centric MCQ format; no culturally variable scoring taxonomy is involved. |
| OC | LOWER | The user confirms that evaluation schemas are broadly consistent across North Indian boards and competitive-exam settings, and MILU was designed by the target population (India); annotator-population mismatch is therefore low. |
| OF | LOWER | Benchmark output is a label/answer key and deployment requires the same binary scoring signal; output form is fully aligned. |

## Flagged Gaps

1. **Hindi state-board syllabus coverage vs. competitive-exam framing:** MILU draws questions from competitive exams (1500+ national, state, and regional exams), but the deployment must also cover school and university board syllabi (CBSE, UP Board, MP Board, Rajasthan Board, Bihar Board, etc.). Downstream web search should investigate whether MILU's Hindi-language items adequately represent board-level curricular content — particularly in Hindi literature, regional history, and civics — or whether they skew toward entrance-exam registers that presuppose different canonical framings.

2. **Regional Hindi linguistic variation in item language:** Hindi MCQ items sourced from competitive exams may use a pan-India standard Khari Boli/formal register. North Indian teachers and students in states like UP, Bihar, or Rajasthan may encounter lexical or orthographic choices that differ subtly from local academic norms. Web search should check whether MILU's Hindi items show evidence of dialect or register standardisation that could disadvantage state-board-aligned content.

3. **Translated English-board content:** The deployment includes English-medium board questions translated into Hindi. MILU does not appear to include such translated content. Web search should investigate whether any published Hindi-language MCQ benchmarks include translated CBSE/ICSE English-medium items, and whether translation adequacy has been validated for subject-specific terminology (science, economics, etc.) in a North Indian Hindi register.

4. **Sub-national state-board granularity:** MILU is described at the pan-India/Indic-language level. It is unclear whether its Hindi-language items are distributed across state-level competitive exams from UP, MP, Rajasthan, and Bihar equally, or whether certain states dominate. Web search should seek any published breakdown of MILU's exam-source distribution by state for Hindi-language items, as under-representation of a major Hindi-belt state's exam content would be a concrete validity gap.

5. **Culturally specific Hindi literary and historical content:** Canonical Hindi-board topics — Tulsidas's Ramcharitmanas, Premchand's fiction, Kabir's dohas, Rani Lakshmibai, regional medieval history — may appear in MILU under Arts & Humanities but could be framed from a competitive-exam (UPSC/SSC) perspective rather than a school-literature perspective. Web search should examine whether MILU's Arts & Humanities and Language & Literature subjects under Hindi include board-syllabus-aligned literary questions or primarily administrative/general-knowledge framings of the same figures.