## Use Case
A US K-8 math tutoring platform is deploying an LLM-powered homework-checker that receives arithmetic word problems via text and determines whether a student's final numerical answer is correct. The evaluation goal is to assess the LLM's ability to solve multi-step arithmetic word problems (four operations, fractions, decimals, percentages, ratios, measurement, area/perimeter, and basic statistics) before live deployment.

## Target Population
Geography: United States (nationwide); no sub-national targeting specified. Students are American elementary and middle schoolers in grades K-8, with the highest-volume cohort in grades 3-6. Language: English only. Problems are written to US Common Core standards and use US customary units, US currency (dollars/cents), and culturally familiar American settings (school cafeterias, sports practice, shopping).

## Elicitation Responses
Q1 [IO]: Which operation types and complexity levels are most critical for your K-8 students, and do your word problems include Common Core-aligned topics like measurement, geometry, or data/statistics that might not appear in a general grade school benchmark?
A1: The core volume is grades 3-6: multi-step problems with four operations on multi-digit numbers, followed by fractions (grades 4-5) and decimals/percentages/ratios (grades 6-8). The platform also regularly includes US customary measurement conversion problems and basic data/statistics problems (mean/median from small datasets). Area/perimeter word problems appear frequently; formal geometry proofs do not.

Q2 [IC]: Do your platform's word problems use US-specific contexts (dollars, customary units, American settings), and would a mismatch in benchmark context affect evaluation representativeness?
A2: Yes — problems are written for US students and consistently use dollars/cents, US customary units, and American settings. Metric appears only where Common Core mandates some exposure in upper grades. A benchmark with non-US currency or heavy metric usage would be a meaningful mismatch for context fidelity, though for pure arithmetic the numerical skills being tested remain the same.

Q3 [OO]: Does your system need to evaluate only the final numerical answer, or also partial credit, intermediate steps, or written reasoning?
A3: The system performs a binary correct/incorrect check on the final numerical answer only. Intermediate steps and written reasoning are not evaluated. An unconventional solution method that yields the correct number is scored as correct.

## Dimension Priority Weights
| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | MODERATE | GSM8K is US-sourced grade school math and covers the core operation types well, but the user confirmed that measurement conversions, basic statistics (mean/median), and area/perimeter problems appear regularly and may be underrepresented in GSM8K's general problem set. |
| IC | MODERATE | The platform uses US dollars, US customary units, and American cultural settings consistently; GSM8K is US-primary but flagged as "transferred from different cultural context," creating a non-trivial risk that some benchmark problems carry non-US unit or currency conventions that reduce representativeness for this deployment. |
| IF | LOWER | Both the benchmark and deployment are text-only in English; no modality or script mismatch exists. |
| OO | LOWER | The deployment requires only binary correct/incorrect judgment on a final numerical answer, which aligns directly with GSM8K's answer-verification structure; no culturally variable output categories are involved. |
| OC | LOWER | Ground-truth labels are objective numerical answers to arithmetic problems; correctness is verifiable and not subject to annotator subjectivity or cultural interpretation. |
| OF | LOWER | The benchmark produces a final numerical label that maps directly onto the platform's binary answer-checking output; no format mismatch. |

## Flagged Gaps
1. **Measurement conversion problems**: The user explicitly noted that US customary unit conversions (feet↔inches, cups↔gallons, pounds↔ounces) appear regularly on the platform and are Common Core-aligned. Downstream search should verify how frequently GSM8K contains such problems and whether the unit systems used match US customary conventions.

2. **Basic statistics problems**: Mean and median calculations from small datasets are part of the platform's problem set (Common Core grades 6-8). GSM8K's coverage of data/statistics word problems (as distinct from pure arithmetic) should be checked, as this is a topic area likely underrepresented in a 2021 grade school dataset.

3. **Area and perimeter word problems**: The platform includes these regularly. GSM8K is not a geometry-focused benchmark; the proportion of area/perimeter problems present in GSM8K should be verified to determine whether this sub-skill is adequately tested.

4. **"Source culture: transferred from different cultural context" flag**: Despite GSM8K's US primary region label, the metadata notes a cultural transfer. Downstream search should investigate whether GSM8K problems contain non-US currency, metric-primary unit usage, or non-American cultural settings (e.g., problems originally written for a different English-speaking population), which would reduce IC validity for this platform's US-customary-unit, US-dollar problem set.

5. **K-2 and early grade coverage**: The platform serves K-8, but single-digit and early-grade arithmetic (grades K-2) may be underrepresented in GSM8K, which targets "grade school" breadth. If the platform ever expands the checker to younger students, this gap should be assessed separately.

6. **Grade-band difficulty calibration**: The user's problem distribution spans a wide difficulty range (single-step K-2 through ratio/percentage grades 7-8). Whether GSM8K's difficulty distribution skews toward upper-elementary complexity — and thus under-tests simpler problems the platform serves — should be confirmed through search or item-level analysis.