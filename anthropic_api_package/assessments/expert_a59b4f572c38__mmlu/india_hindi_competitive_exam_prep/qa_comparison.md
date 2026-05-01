# Q&A Comparison: Original (MILU) vs Cleaned (for MMLU)

Tuple: `india_hindi_competitive_exam_prep`

---

## Q1 [IO]

**Original:**
For a graduate student in North India preparing for competitive job exams (e.g., UPSC, SSC, state PSC, banking exams), which subject areas are most critical — General Knowledge, Current Affairs, Indian Polity & Constitution, Hindi language proficiency, regional history of North Indian states (UP, Bihar, Rajasthan, MP), or Mathematics/Reasoning? Are there specific exam types (Central vs. state-level) that your deployment must prioritize?

**Cleaned:**
For a graduate student in North India preparing for competitive job exams (e.g., UPSC, SSC, state PSC, banking exams), which subject areas are most critical — General Knowledge, Current Affairs, Indian Polity & Constitution, Hindi language proficiency, regional history of North Indian states (UP, Bihar, Rajasthan, MP), or Mathematics/Reasoning? Are there specific exam types (Central vs. state-level) that your deployment must prioritize?

**Delta:** No change (question was already deployment-focused).

**A1 (verbatim):**
Most critical subject areas are General Knowledge, Current Affairs, History, and Mathematics/Reasoning. Additionally, there may be some familiarity required with Indian Polity & Constitution, and proficiency in the Hindi language. To be more specific, let's focus on the central examinations conducted in India.

---

## Q2 [IC]

**Original:**
Competitive exam questions for North Indian students often draw on culturally specific knowledge — e.g., festivals like Chhath Puja, regional administrative units like tehsils or mandals, state-specific historical figures, or North Indian legal and land-revenue traditions. Does your deployment expect the AI to handle this kind of regionally grounded content, or is the focus on pan-India general knowledge content?

**Cleaned:**
Competitive exam questions for North Indian students often draw on culturally specific knowledge — e.g., festivals like Chhath Puja, regional administrative units like tehsils or mandals, state-specific historical figures, or North Indian legal and land-revenue traditions. Does your deployment expect the AI to handle this kind of regionally grounded content, or is the focus on pan-India general knowledge content?

**Delta:** No change (question was already deployment-focused).

**A2 (verbatim):**
Central competitive examinations cover both regional aspects as well as pan-India general knowledge content, so AI should be able to handle both sets of knowledge.

---

## Q3 [OO]

**Original:**
When the AI provides feedback on a student's response, what should that feedback look like — a simple correct/incorrect label, an explanation of why an answer is right or wrong, a hint toward the correct answer, or an encouragement message in Hindi? Competitive exam prep often benefits from explanatory feedback, but if the benchmark only scores label accuracy **(MCQ)**, there may be a mismatch with what your deployment needs the model to actually produce.

**Cleaned:**
When the AI provides feedback on a student's response, what should that feedback look like — a simple correct/incorrect label, an explanation of why an answer is right or wrong, a hint toward the correct answer, or an encouragement message in Hindi? Competitive exam prep often benefits from explanatory feedback, so if **the benchmark under assessment** only scores label accuracy, there may be a mismatch with what your deployment needs the model to actually produce.

**Delta:** Removed `(MCQ)` (MILU-specific format detail). Changed `"but if the benchmark"` → `"so if the benchmark under assessment"` — abstracted to generic reference.

**A3 (verbatim):**
AI feedback should include a simple correct/incorrect label and an explanation of why an answer is right or wrong in the Hindi language.

---

## Q4 [IC]

**Original:**
Since your target student has limited English exposure and interacts primarily in Hindi, would it be a problem if some benchmark questions **— even in the Hindi portion —** contain English technical terms, code-mixed phrasing, or assume familiarity with English-medium textbook conventions? Or does your deployment require that all content be fully accessible to a Hindi-medium educated student?

**Cleaned:**
Since your target student has limited English exposure and interacts primarily in Hindi, would it be a problem if some benchmark questions contain English technical terms, code-mixed phrasing, or assume familiarity with English-medium textbook conventions? Or does your deployment require that all content be fully accessible to a Hindi-medium educated student?

**Delta:** Removed `"— even in the Hindi portion —"` — MILU-specific property (MILU has a dedicated Hindi portion; MMLU does not).

**A4 (verbatim):**
A small portion of code-mixing with English technical terms is acceptable, but it should not exceed ~10%.
