## Use Case
A Bengali-speaking university student in Dhaka, Bangladesh is using a regional LLM to generate locally grounded stories as part of a BSc thesis. The deployment evaluates how well generic frontier models, small LLMs, and region-specific LLMs handle Bangladesh-specific cultural, geographic, linguistic, and historical context in Bengali story generation tasks.

## Target Population
- **Geography:** Dhaka, Bangladesh (urban, but deployment context also spans rural/village Bangladesh, hill tracts, and river delta regions)
- **Language:** Bangladeshi Standard Bengali (Cholti register with Arabic/Persian loanword patterns, distinct from West Bengali Standard Bengali)
- **Role:** Undergraduate university student; BSc thesis work in story generation
- **Relevant demographics:** Native Bangladeshi Bengali speaker; expects familiarity with Bangladeshi institutions (Dhaka University, BUET, IUT, DMC, BRAC University), political history (1971–2026), cultural events (Ekushe Boi Mela, Pohela Boishakh as celebrated in Bangladesh), geography (Cox's Bazar, Rangamati, Bandarban, Sajek), and rural/riverine village life

## Elicitation Responses

Q1 [IO]: Does the deployment require Bangladesh-specific cultural touchstones rather than the Indian cultural references likely present in MILU's Bengali content?
A1: Yes. Required coverage includes: the 1971 Liberation War and subsequent political history through 2026; Bangladeshi educational landmarks (SSC, HSC exams; Dhaka University, BUET, IUT, DMC, Rajshahi University, Shahjalal University, BRAC University); rural/village life and river-area contexts; Bangladeshi drama and film history; cultural events such as Ekushe Boi Mela; and tourism sites including Cox's Bazar, Rangamati, Bandarban, and Sajek. These are largely absent from Indian exam-sourced content.

Q2 [IC]: Are the Bengali datapoints in MILU — sourced from Indian competitive exams — expected to contain Bangladeshi-specific named entities such as Dhaka neighbourhoods, Bangladeshi institutions, political figures, and local geography?
A2: Yes, the deployment expects such Bangladeshi-specific named entities. However, given MILU's Indian exam provenance, the benchmark's concrete references are presumed to be predominantly India-centric, creating a significant gap for this deployment.

Q3 [IC]: Does the deployment require the Bangladeshi Bengali register specifically, and do Indian exam-derived questions adequately reflect that register?
A3: Yes, the Bangladeshi register is specifically required (vocabulary, idiom, Arabic/Persian loanword patterns distinct from West Bengali). Indian exam-derived questions do not adequately reflect this register and are therefore insufficient for evaluating the target deployment.

Q4 [OC]: Whose judgment should serve as ground truth for evaluating locally grounded Bangladeshi story generation, and does annotator mismatch affect score reliability?
A4: Native Bangladeshi Bengali speakers should serve as the primary ground truth; a mixed annotator pool is acceptable as a secondary option. Indian annotator validation of MILU's Bengali content is considered to meaningfully affect the reliability of evaluation scores for this Bangladesh-targeted deployment.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | MILU's Bengali content is sourced entirely from Indian state and competitive exams, systematically excluding the Bangladeshi cultural, political, educational, and geographic categories the deployment requires (Liberation War, SSC/HSC, Ekushe Boi Mela, Bangladeshi tourism, rural river life). |
| IC | HIGH | Concrete datapoint-level references — named institutions, political figures, Dhaka neighbourhoods, Bangladeshi rivers — are almost certainly India-centric, and the user explicitly confirmed the need for Bangladesh-specific named entities and register, with Indian exam content deemed inadequate. |
| IF | LOWER | The deployment is text-only in a high-resource Indic script (Bengali) and MILU is also text-only; no modality mismatch exists, though non-Latin script rendering deserves routine verification. |
| OO | MODERATE | MILU uses MCQ label output from Indian exam questions; the output category space (correct exam answers) does not map cleanly onto evaluating culturally grounded story generation quality, though downstream scoring for story generation may differ from benchmark scoring itself. |
| OC | HIGH | MILU's Bengali labels were validated through Indian exam frameworks and likely by Indian annotators; the user confirmed this mismatch degrades reliability, and native Bangladeshi Bengali speakers are required as the primary ground-truth population. |
| OF | MODERATE | MILU produces MCQ labels while the deployment targets open-ended story generation; this format gap means benchmark scores measure recall of factual/cultural knowledge rather than generative cultural grounding, limiting direct transfer of evaluation validity. |

## Flagged Gaps

1. **Bangladeshi Bengali register:** MILU's Bengali content almost certainly reflects West Bengali Standard Bengali orthographic and lexical norms derived from Indian exams. Downstream search should investigate whether any MILU Bengali items use Bangladeshi-standard vocabulary or Arabic/Persian loanword patterns, or whether the benchmark documents any dialect stratification within its Bengali split.

2. **Bangladesh-specific ontological coverage:** Verify whether MILU's 41 subjects and 8 domains include any items referencing the 1971 Liberation War (as a Bangladeshi rather than Indian partition event), Bangladeshi national curriculum exams (SSC, HSC), Bangladeshi universities, or post-1971 Bangladeshi political history (1975 coup, 1990 uprising, 2024 political events). This is the single largest content validity gap.

3. **Named entity provenance in Bengali items:** Confirm whether Dhaka-specific place names (Dhanmondi, Old Dhaka, Wari), Bangladeshi rivers (Buriganga, Meghna, Padma as it flows in Bangladesh), and Bangladeshi cultural sites (Cox's Bazar, Sajek, Rangamati, Bandarban, Sundarbans in Bangladesh) appear in any Bengali datapoints, or whether all geographic references are India-centric.

4. **Annotator population for Bengali items:** Investigate whether MILU documentation discloses the regional composition of Bengali-language annotators and validators — specifically whether any native Bangladeshi Bengali speakers were included in item review or answer validation.

5. **Rural and riverine Bangladesh sub-contexts:** The deployment requires coverage of Bangladeshi village life, river-area livelihoods, and farming contexts specific to Bangladesh's river delta ecology. These sub-national, non-urban registers are unlikely to appear in competitive exam content and should be flagged as a structural absence.

6. **Bangladeshi drama, film, and literary figures:** Verify presence of Bangladeshi cultural figures (Humayun Ahmed, Zafar Iqbal, Selim Al Deen) and Bangladeshi media history in MILU's Arts & Humanities domain, as this domain is documented as low-performing but its geographic scope within Bengali content is unverified.

7. **Ekushe Boi Mela and Language Movement:** The 1952 Language Movement is a foundational Bangladeshi (not Indian) cultural event; confirm whether MILU treats it from an Indian or Bangladeshi national perspective, as framing differences would affect answer correctness for a Bangladeshi user.