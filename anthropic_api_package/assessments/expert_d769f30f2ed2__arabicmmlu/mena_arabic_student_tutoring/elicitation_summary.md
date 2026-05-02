## Use Case
An AI tutoring system that answers curriculum-aligned questions for students at primary, middle, high school, and university levels across eight MENA countries: Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, and Saudi Arabia. The system must align answers to each country's specific national curriculum, including country-specific law, while handling university-level subjects (management, economics, law, CS, political science, accounting) in Arabic (and potentially French for Morocco).

## Target Population
Geography: Morocco, Egypt, Jordan, Palestine, Lebanon, UAE, Kuwait, Saudi Arabia — eight distinct national curriculum systems spanning North Africa, the Levant, and the Gulf.
Sub-national cohort: School-level students (primary through high school) and university students; predominantly Sunni Muslim majorities across all eight countries.
Language(s): Modern Standard Arabic as primary medium; French as secondary medium for Moroccan students in science and university-level subjects; Darija (Moroccan spoken Arabic) explicitly excluded from scope.
Occupation/role: Students preparing for national examinations (e.g., Egyptian Thanawiyya Amma, Jordanian Tawjihi, Gulf equivalents) and university coursework.

## Elicitation Responses

Q1 [IO]: Your deployment spans eight countries with distinct national curricula — for example, Morocco follows a French-influenced baccalaureate system, Egypt has its own Thanawiyya Amma content, and Gulf states have their own civic and religious education frameworks. Does your tutoring system need to align with each country's specific national curriculum, or does it serve a pan-Arab 'common core'? Are there subject areas — such as Islamic studies, national history, or civics — where a Moroccan student's expected answers would differ meaningfully from a Jordanian or Emirati student's?
A1: The system must align with each country's specific national curriculum. For factual questions a single correct answer is expected regardless of country. Islamic studies presents a minor edge case due to different madhabs (schools of jurisprudence) across countries, but this level of specificity is not anticipated at the school level. All eight target countries are majority Sunni, so Shia-specific rulings (relevant in Iraq or Yemen) are not a concern here.

Q2 [IC]: For university-level subjects like law, political science, and economics, the 'correct' answer can depend heavily on which legal tradition or regulatory framework is in scope. Would your system need to tailor its answers to a student's specific country's legal or economic system, or is a general Arabic-world framing acceptable?
A2: The system must tailor legal answers to each country's specific legal system (e.g., Egyptian civil code vs. UAE or Moroccan law). Country-specific tailoring is required for law; the user did not specify the same requirement for economics or political science, implying a more general framing may be acceptable there.

Q3 [OO]: Should correct answers match the exact phrasing or reasoning style of a specific national exam's marking scheme, or is any accurate explanation acceptable? Would a student lose marks if the system's reasoning diverges from the expected answer structure?
A3: For open-ended school questions, divergence from the national marking scheme could disadvantage students who rely on rote Q&A formats (as is common in Egyptian schooling). However, for multiple-choice questions — which is the format ArabicMMLU uses — explanations are not graded, so any correct explanation adequately supports the student's understanding without exam risk.

Q4 [IC]: Would Moroccan students need responses accommodating French-medium content or Darija code-switching, or is Modern Standard Arabic sufficient?
A4: MSA is the formal medium of instruction across all eight countries and is sufficient for school settings. Darija code-switching is informal and out of scope. French may need to be accommodated for subjects taught in French at Moroccan universities (e.g., sciences, certain professional programs).

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | The benchmark covers eight countries but Palestine is absent from its documented source countries, and university-level subjects (law, CS, management, accounting) may have thin or uneven coverage across all eight distinct national curricula the deployment requires. |
| IC | HIGH | Country-specific legal systems, national history content, and civics vary substantially across the eight countries; individual questions calibrated to one national curriculum (e.g., Egyptian or Jordanian) may carry incorrect or inapplicable ground truth for students in Kuwait, Morocco, or Lebanon. |
| IF | MODERATE | Deployment is text-only and MSA matches the benchmark's language; however, Moroccan students may encounter French-medium university content that falls entirely outside the benchmark's scope, creating a partial modality/language gap. |
| OO | MODERATE | The MCQ output format is shared between benchmark and deployment, which reduces scoring misalignment risk; however, the scoring taxonomy does not capture country-differentiated correct answers (e.g., legal questions with different correct answers per jurisdiction). |
| OC | HIGH | Ground-truth labels sourced from national exams of a subset of countries (Jordan, Egypt, UAE, Lebanon, KSA) may not represent correct answers for Kuwait or Palestine curricula; annotator and source-exam coverage is uneven across the eight deployment targets. |
| OF | LOWER | Both benchmark and deployment use MCQ / label output; the user confirmed that explanation format is not exam-critical for MCQ contexts, so output form mismatch is minimal. |

## Flagged Gaps

1. **Palestine curriculum coverage**: Palestine is explicitly listed as a deployment target but is not among the countries documented as benchmark sources. Downstream search should investigate whether ArabicMMLU includes any Palestinian Ministry of Education exam content, and if not, how large the coverage gap is for subjects like history, civics, and social studies.

2. **Kuwait curriculum coverage**: Kuwait does not appear prominently in the benchmark's documented source countries. Web search should verify whether Kuwaiti school exams contributed questions, particularly for civic education, national history, and Islamic studies calibrated to the Kuwaiti curriculum.

3. **University-level law questions per jurisdiction**: The benchmark's university-level law content (if any) may be calibrated to a single legal tradition (likely Egyptian civil law as the dominant MENA model). Search should identify which legal systems are represented in ArabicMMLU's law tasks and whether UAE, Moroccan, or Jordanian legal frameworks are separately instantiated.

4. **French-medium Moroccan university content**: Moroccan university science and professional programs are taught in French, which is outside ArabicMMLU's MSA scope. Search should assess whether any companion benchmark or coverage exists for French-Arabic bilingual Moroccan higher education.

5. **Islamic studies madhab specificity**: While the user assessed this as unlikely at the school level, downstream search should verify whether ArabicMMLU Islamic studies questions are calibrated to a single madhab (e.g., Shafi'i, Maliki, Hanbali) or are deliberately madhab-neutral, given that Morocco (Maliki) and Saudi Arabia (Hanbali) have different normative traditions.

6. **Marking-scheme alignment for open-ended subjects**: Although MCQ format reduces this risk, the benchmark does not appear to test whether model explanations align with national rote-learning expectations (e.g., Egyptian Thanawiyya Q&A banks). Search should check if any rubric-alignment evaluation has been done for the benchmark's tasks in Egyptian or Jordanian school contexts.