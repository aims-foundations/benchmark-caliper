## Use Case
A toxicity-evaluation pipeline in which large-to-small LLMs are asked to rate the toxicity of text spanning generic and domain-specific offensive content (racist remarks, sexual/offensive jokes, subtle remarks). The primary scientific goal is to compare how LLMs perceive South Asian region-specific offensive language (including code-mixed and implicit varieties) against Western-equivalent stimuli, to surface cross-regional disparities in LLM safety behavior.

## Target Population
Academic safety researchers based in the South Asian region (Bangladesh, India, Pakistan, Sri Lanka, and adjacent countries), studying how LLMs respond to region-specific toxic language. End-target of the offensive content includes caste-based groups (Dalits, OBCs), religious communities implicated in Hindu–Muslim and India–Pakistan tensions, political communities associated with parties such as BJP, Congress, and Awami League, and ethnic/linguistic minorities. Relevant languages include English, Hinglish, Romanized Urdu, Tanglish, and other code-mixed South Asian varieties.

## Elicitation Responses

Q1 [IO]: TOXIGEN was built around 13 U.S.-defined minority groups. Which target group categories are essential for South Asian researchers, and are there offense categories common in South Asia with no close U.S. equivalent in the benchmark's taxonomy?
A1: Country-specific contexts are essential. For Bangladesh and India, this includes Hindu–Muslim communal conflict; for India–Pakistan, border-tension rhetoric drawn from everyday speech. Political slurs tied to specific parties (BJP, Congress, Awami League) are required. Caste-based groups must be represented. These categories have no meaningful equivalent in TOXIGEN's 13 U.S.-minority-group taxonomy.

Q2 [IC]: Would the offensive content include code-mixed language, implicit casteist microaggressions, or religious dog-whistles that are surface-benign but toxic to in-group readers? Would purely English, U.S.-framed stimuli be ecologically valid for South Asian annotators or LLMs?
A2: Code-mixed language is essential. The most important category is content that appears benign on the surface but is recognized as toxic only by in-group South Asian readers. Purely U.S.-framed English stimuli would not feel ecologically valid; South-Asian-specific rewording is the core requirement of the research.

Q3 [OC]: Whose judgment should serve as ground truth for South Asian toxicity labels, and would systematic annotator disagreement be expected across Indian, Pakistani, and Sri Lankan raters?
A3: Cross-regional consensus is the ideal but is acknowledged as difficult and costly to obtain. Systematic disagreement across Indian, Pakistani, and Sri Lankan annotators on the same text is explicitly anticipated and is itself a research object — making the annotation process both sensitive and expensive.

Q4 [OO]: Should the output scoring be a single score, a multi-dimensional rating, or a comparative ranking? Is TOXIGEN's label granularity sufficient?
A4: A multi-dimensional rating is required (e.g., severity, target-group specificity, implicitness level). A comparative ranking between South Asian and Western equivalent stimuli — or between LLM ratings of equivalent sentences — would be analytically valuable. TOXIGEN's Likert-scale scoring (not purely binary) is closer to what is needed, but the dimensional structure still needs expansion for this use case.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | TOXIGEN's 13 U.S.-minority-group taxonomy entirely omits caste groups, South Asian communal conflict categories, and politically specific slur targets (BJP, Awami League, etc.) that are central to the deployment. |
| IC | HIGH | The deployment explicitly requires code-mixed, surface-benign but in-group-toxic content anchored in South Asian cultural frames; U.S.-generated English stimuli are confirmed by the user to lack ecological validity for this population. |
| IF | MODERATE | The deployment is text-only and TOXIGEN is text-only, which aligns; however, code-mixed Romanized scripts and non-standard orthographies introduce a signal-distribution mismatch that standard English-trained pipelines may not handle. |
| OO | HIGH | The required output structure (multi-dimensional Likert ratings plus comparative cross-regional rankings) exceeds TOXIGEN's output taxonomy, and the benchmark's categories were designed for a U.S. cultural context where legitimate pluralism in toxicity judgment is not foregrounded. |
| OC | HIGH | Ground-truth labels will need to come from cross-regional South Asian annotators whose judgments are expected to systematically disagree by country; TOXIGEN's labels were produced in a U.S. context with no South Asian community validation. |
| OF | MODERATE | TOXIGEN does use a Likert-scale score rather than a strict binary label, which partially aligns with the deployment's need for graded output; however, the dimensional axes (severity, implicitness, target specificity, cross-regional comparison) still require extension beyond TOXIGEN's current form. |

## Flagged Gaps

1. **Missing target-group ontology for South Asia**: Web search should investigate whether any existing benchmark covers caste-based hate (Dalit/OBC slurs), Hindu–Muslim communal conflict text, India–Pakistan political rhetoric, and party-specific political slurs (BJP, Congress, Awami League, PTI). The absence of these categories in TOXIGEN is near-certain and needs confirmation with alternative resources.

2. **Code-mixed and Romanized script toxicity data**: There is likely no validated toxic-language dataset in Hinglish, Romanized Urdu, or Tanglish that covers implicit/adversarial toxicity. Downstream search should look for datasets such as HatEval (multilingual), SemEval hate speech tasks, or South Asian NLP workshop outputs that address code-switching.

3. **In-group-only recognizable toxicity (dog-whistles and microaggressions)**: TOXIGEN's adversarial implicit examples are U.S.-calibrated. Search should identify any annotated corpus of South Asian dog-whistles or casteist microaggressions where surface-benign statements were labeled by affected community members (e.g., Dalit activists, Muslim scholars in India/Bangladesh/Pakistan).

4. **Cross-national annotator disagreement**: The user confirmed that Indian, Pakistani, and Sri Lankan annotators are expected to rate identical stimuli differently. Search should locate any empirical study documenting inter-annotator disagreement in South Asian toxicity annotation across national boundaries, as this will inform what cross-regional consensus methodology is feasible.

5. **Partition-era and sectarian language varieties**: Language rooted in the 1947 Partition and subsequent communal violence carries specific semantic loading not present in U.S. minority discourse. Search should check whether any NLP resource captures this historical-linguistic register as a toxicity category.

6. **Sub-national variation within India and Bangladesh**: The user's answers addressed India and Bangladesh at the national level, but strong sub-national variation (e.g., West Bengal vs. Uttar Pradesh vs. Tamil Nadu; Dhaka vs. Sylhet) in offensive idioms and target groups is plausible and unaddressed. Downstream stages should flag whether any benchmark or dataset distinguishes sub-national South Asian varieties.

7. **LLM toxicity-rating behavior on non-English/code-mixed input**: Since the deployment evaluates how LLMs assign toxicity scores rather than training a classifier, search should look for existing studies measuring LLM toxicity-rating disparities across English vs. code-mixed South Asian inputs to establish a baseline for what is already known.