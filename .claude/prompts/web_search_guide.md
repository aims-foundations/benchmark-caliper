# Web Search Guide for Cultural Validity Assessment
<!-- Layer 2: Pipeline-facing operational guide | Date: 2026-04-02 -->
<!-- Evidence base: ~59 papers across 12 cultural topics + 19 KG extractions -->
<!-- Budget: ~5-10 queries per assessment session -->

---

## 1. How to Use This File

You are the search agent in a cultural validity assessment pipeline. Your job is to find web-accessible evidence that would **change** the assessment of a benchmark's validity for a specific regional deployment context. You have already received:

- **Benchmark metadata**: what the benchmark tests, its source region, its data sources, its evaluation format.
- **User context from elicitation**: the target deployment region, the use case, the cultural domains involved, the population, and any known concerns.

This guide tells you **what to search for**, **where to search**, **how to construct queries**, and **what you cannot find via web search** (which must be flagged for expert review).

### Operating Principles

1. **Bias toward novelty.** Do not search for information that confirms what the pipeline already knows. Search for evidence that would **change the assessment** -- a benchmark that covers the gap, a study that documents a new failure mode, a data source that contradicts the current evidence.

2. **Budget is scarce.** You have approximately 5-10 queries. Each query must be targeted. Use the weighting heuristics (Section 2) to allocate queries to the highest-impact targets.

3. **Flag what you cannot find.** Many cultural knowledge types are structurally unsearchable (Section 7). Do not waste queries on them. Instead, flag them explicitly as requiring expert/stakeholder input.

4. **Cross-reference dimensions and domains.** Every search result should be tagged with (a) which cultural domain(s) it informs and (b) which framework dimension(s) it addresses. Use the cross-reference table in Section 5.

5. **Distrust automated metrics.** If you find a paper claiming to measure cultural validity via Region-CLIPScore, CLIP-based metrics, or similar automated measures, flag the result with a reliability warning (see Section 7.3).

6. **Check web corpus size.** For any target language or region, check the language's representation in Common Crawl or equivalent web corpora. Web data volume is the strongest single predictor of LLM cultural alignment (r = 0.94, Sukiennik et al.). If the target language has minimal web presence, flag this as a baseline viability concern before proceeding with other searches.

---

## 2. Weighting Heuristics: Allocating Your Search Budget

Use these decision rules to decide where to spend your 5-10 queries. Evaluate each condition against the user's context and benchmark metadata.

### 2.1 High-Priority Triggers (allocate 2-3 queries)

| Condition | Search Target | Rationale |
|-----------|---------------|-----------|
| Target region is Latin America, Sub-Saharan Africa, Pacific Islands, Caribbean, or Central Asia | Region-specific benchmarks (Section 6) | These regions have thin-to-zero evidence in the pipeline's knowledge base. Any new benchmark or study is high-impact. |
| Benchmark involves visual/multimodal input or output | Multimodal cultural evaluation papers (Section 4.1) | Input Form and Output Form are the weakest dimensions. Multimodal evidence is the largest methodological gap. |
| Benchmark tests religious, spiritual, or belief-system knowledge | Religious knowledge benchmarks (Section 4.8) | Deep coverage exists only for Islam and Indian religions. All other traditions are uncovered. |
| Target deployment involves speech/audio interaction | Speech modality papers (see Section 7.1) | Complete evidence vacuum. Flag immediately. |
| Benchmark covers lifecycle events (weddings, funerals, birth rites) | Lifecycle cultural evaluation (Section 4.5) | Near-zero coverage despite cultural universality. |

### 2.2 Medium-Priority Triggers (allocate 1-2 queries)

| Condition | Search Target | Rationale |
|-----------|---------------|-----------|
| Benchmark uses MCQ-only evaluation format | MCQ-vs-OEQ format studies | MCQ inflates scores by 20-66 pp over open-ended formats. Search for format-comparison evidence specific to the domain. |
| Target language is low-resource (< 1% of Common Crawl) | Language-specific NLP evaluation | Language competence confounds cultural knowledge measurement. Search for diagnostic methodology. |
| Benchmark was constructed from Wikipedia or Wikidata | Wikipedia coverage bias studies for target region | Wikipedia systematically underrepresents Africa, Oceania, and oral-tradition cultures. |
| Benchmark claims sub-national coverage | Sub-national cultural evaluation studies | Country-level analysis erases critical variation. Search for state/province-level evidence. |
| Use case involves content moderation or bias detection | Regional stereotype/bias benchmarks | Standard debiasing fails on non-Western stereotypes (37-45% vs. 80-89% reduction). |

### 2.3 Lower-Priority (allocate remaining queries)

| Condition | Search Target | Rationale |
|-----------|---------------|-----------|
| Benchmark covers well-evidenced domains (norms, cuisines) for well-covered regions (US, EU, East Asia) | Skip or minimal search | Pipeline already has strong evidence. Search only if user flags a specific concern. |
| Target deployment is monolingual English for Western population | Skip cultural search | Low risk of cultural validity failure. Focus on other assessment dimensions. |

### 2.4 Budget Allocation Algorithm

```
1. Check high-priority triggers. Assign 2-3 queries to the FIRST matching condition.
2. Check medium-priority triggers. Assign 1-2 queries.
3. If budget remains, allocate to region-specific strategies (Section 6).
4. Reserve 1 query for a general "cultural benchmark + [target region]" sweep.
5. If no high-priority triggers match, distribute budget across medium-priority.
```

---

## 3. Search Targets by Cultural Domain

For each of the 12 cultural topics in the pipeline's taxonomy, this section provides: what to search for, recommended query strategies, high-value source types, known unsearchable knowledge, which framework dimensions the search informs, and when the topic is conditionally relevant.

---

### 3.1 Cuisines and Food

**What to search for:**
- Regional food knowledge benchmarks beyond the 7 papers in the evidence base (BLEnD, SCALE, CANDLE, DOSA, CulturalBench, CultureGen, MAKIEval)
- Visual food recognition or food VQA datasets for the target region
- Specialized food knowledge bases (FAO databases, FoodKG, regional recipe corpora) -- none are used by any paper in the current evidence base
- Community-sourced food inventories for underrepresented regions (Central Africa, Caribbean, Pacific Islands, Central Asia, indigenous cuisines)
- Studies documenting food-related stereotyping in LLM outputs

**Recommended query strategies:**
- Comparative: `"food recognition" OR "cuisine knowledge" + [target country/region] + LLM OR benchmark`
- Seed-term: `WorldCuisines OR "food VQA" OR "culinary NLP" + [target region]`
- Source-specific: `site:aclanthology.org "food" + "cultural" + evaluation`

**High-value source types:**
- Open-license cultural food images: Flickr CC, WikimediaCommons, Dollar Street/Gapminder
- FAO food databases, regional recipe corpora, ethnographic food literature (untapped by all 7 papers)
- Non-English Wikipedia food articles for target region

**Known unsearchable knowledge (flag for expert review):**
- Everyday food practices (what people actually eat daily vs. iconic national dishes)
- Preparation methods, dietary restrictions, ceremonial food, food economics
- Ingredients/raw materials and spice palettes for underrepresented regions
- Food knowledge from oral-tradition communities

**Framework dimensions informed:** IO (taxonomy gaps), IC (Western food default), OC (stereotyping rates)

**Conditionally relevant when:** Benchmark includes food/cuisine items; deployment involves recommendations, health/nutrition, or everyday assistants in non-Western contexts; benchmark was built from web scraping or LLM generation without community validation.

---

### 3.2 Fashion and Style

**What to search for:**
- Visual clothing recognition or fashion VQA datasets (none exist in evidence base)
- Non-Western garment knowledge bases or textile heritage databases
- Cross-lingual clothing terminology studies (clothing has the lowest cross-lingual resolve rate of any topic: 6.9%)
- Hairstyle cultural knowledge datasets (zero coverage in all 5 papers)
- Studies on LLM clothing markedness or "traditional" framing bias

**Recommended query strategies:**
- `"cultural clothing" OR "garment recognition" + [target region] + NLP OR LLM OR benchmark`
- `"fashion AI" + "bias" OR "stereotype" + non-Western OR [region]`
- `"textile heritage" + digital + [target country]`

**High-value source types:**
- Community-sourced garment inventories (only DOSA for India and SCALE for 9 countries exist)
- Regional textile heritage registries, museum databases
- Non-English fashion media for target region

**Known unsearchable knowledge:**
- Contemporary everyday fashion (all papers focus on traditional/ceremonial)
- Footwear, body adornment, textile materials
- Gender/age variation in dress norms
- Occasion-appropriateness rules (when to wear what)

**Framework dimensions informed:** IO (flat taxonomy), IC (markedness bias), IF (visual modality gap), OC (stereotyping)

**Conditionally relevant when:** Benchmark involves visual cultural representation, image generation, or fashion recommendation; target region has strong sub-national clothing identity (India, Nigeria, Indonesia); cross-lingual deployment is planned.

---

### 3.3 Architectural Spaces

**What to search for:**
- Landmark or place recognition benchmarks for the target region
- Informal architectural space datasets (markets, neighborhood spaces, community gathering places) -- zero coverage in evidence base
- Heritage registries, urban planning databases, UNESCO World Heritage data for target region
- Studies on geographic bias in text-to-image generation for built environments

**Recommended query strategies:**
- `"landmark recognition" OR "place knowledge" + [target country] + LLM OR VLM`
- `"cultural heritage" + digital + benchmark + [target region]`
- `"geographic bias" + "image generation" + architecture OR landmark`

**High-value source types:**
- Government heritage registries, UNESCO heritage lists
- Geographic databases (OpenStreetMap cultural layer, GeoNames)
- Local government records, urban planning documents (untapped by all papers)

**Known unsearchable knowledge:**
- Informal markets (souks, bazaars, tianguis, palengkes, wet markets)
- Behavioral norms within spaces (gender access, bargaining customs, prayer protocols)
- Neighborhood character and community spatial identity
- Vernacular architecture and non-heritage-listed spaces

**Framework dimensions informed:** IO (missing space types), IC (tourism framing bias), IF (visual/spatial gap)

**Conditionally relevant when:** Benchmark targets vision-language models; use case involves navigation, tourism, heritage, or urban planning; target region has near-zero landmark representation (Iran, Thailand, Indonesia, Nigeria, Ethiopia, Morocco, Ghana per SCALE scores).

---

### 3.4 Performance and Art

**What to search for:**
- Music/dance knowledge benchmarks for non-Western traditions
- Oral poetry, folklore, or storytelling NLP datasets (4 of 7 facets -- theatre, poetry, folklore, literature -- have zero evidence)
- Computational folkloristics, oral tradition digitization
- Audio-based cultural evaluation datasets (music recognition, speech)

**Recommended query strategies:**
- `"music knowledge" OR "dance recognition" + LLM OR benchmark + [target region]`
- `"oral tradition" + NLP OR digitization + [target region]`
- `"computational folkloristics" OR "folk narrative" + NLP`
- `"cultural music" + evaluation + AI + [region]`

**High-value source types:**
- UNESCO Intangible Cultural Heritage lists (728 Cultural Elements of Folklore across 144 countries, per GIMMICK)
- Regional music databases, folk song archives
- Community-generated performance documentation

**Known unsearchable knowledge:**
- Theatre traditions, dramatic arts (zero evidence)
- Oral poetry traditions (Somali poetry, Arabic qasida, Urdu ghazal)
- Performance context (who performs, for whom, when, what it signifies)
- Folk narrative traditions, creation myths, storytelling practices

**Framework dimensions informed:** IO (4/7 facets missing), IC (Western default, Bollywood substitution), IF/OF (multimodal gap)

**Conditionally relevant when:** Benchmark targets music, dance, or artistic knowledge; target region has strong oral performance traditions; benchmark was built from LLM generation or Wikidata (both systematically distort non-Western performance culture).

---

### 3.5 Events (Festivals, Holidays, Lifecycle Ceremonies)

**What to search for:**
- Wedding or funeral cultural knowledge benchmarks (absent from all evidence)
- Lifecycle event evaluation methodologies (CAPTex-style procedural text, CUNIT-style cross-cultural matching -- search for follow-up work)
- Non-Western holiday calendar databases or cultural event inventories
- Studies on Western holiday projection in LLM outputs

**Recommended query strategies:**
- `"wedding traditions" OR "funeral customs" + LLM OR NLP OR benchmark + [target region]`
- `CAPTex OR CUNIT OR DIWALI OR GIMMICK + cultural + evaluation`
- `"lifecycle event" OR "rite of passage" + AI OR cultural evaluation`
- `"cultural VQA" + "event" OR "ceremony" + [region]`

**High-value source types:**
- UNESCO ICH knowledge graph (728 CEFs across 144 countries -- note state-mediation bias toward public traditions)
- Regional cultural calendar databases
- Ethnographic studies of lifecycle ceremonies (academic databases)

**Known unsearchable knowledge:**
- Birth rites (near-zero coverage despite cultural universality)
- Coming-of-age ceremonies
- Private/domestic lifecycle rites (structurally excluded by all data collection methods)
- Funeral practices for most cultures
- Ritual sequences and procedural knowledge (how ceremonies are performed step by step)

**Framework dimensions informed:** IO (lifecycle events absent), IC (Western holiday projection), OC (multi-religious plurality)

**Conditionally relevant when:** Benchmark targets multi-religious or multi-ethnic societies; use case involves culturally sensitive content generation (greeting cards, calendar apps, cultural assistants); target region has low digital representation.

---

### 3.6 Rituals and Social Practices

**What to search for:**
- Participatory ritual elicitation studies from Africa, Latin America, or Southeast Asia (only India has community-sourced ritual data)
- Non-English ritual extraction from local-language web corpora
- Multimodal ritual datasets (images of ceremonies, ritual objects, sacred spaces)
- Ritual knowledge in VLMs or multimodal benchmarks

**Recommended query strategies:**
- `"ritual knowledge" OR "ceremonial practice" + LLM OR AI + [target region]`
- `"cultural practice" + benchmark + "community" + [region]`
- `DOSA OR "social artifact" + "ritual" + [region outside India]`

**Known unsearchable knowledge:**
- Birth and death rites (structurally absent from both CANDLE and DOSA)
- Procedural enactment knowledge (who performs which action, in what sequence)
- Domestic/private rituals
- Ritual knowledge transmitted through oral tradition

**Framework dimensions informed:** IO (no sub-facet decomposition), IC (Anglophone bias), OC (community vs. outsider framing)

**Conditionally relevant when:** Benchmark includes cultural practices, festivals, or ceremonies; target region has significant ritual diversity underrepresented in English web text.

---

### 3.7 Sports and Games

**What to search for:**
- Traditional/indigenous game inventories or benchmarks (structurally absent from all evidence)
- Non-English sports knowledge extraction from local-language sports media
- Community-sourced sports practice studies for Global South
- Sub-national sports culture documentation

**Recommended query strategies:**
- `"traditional games" OR "indigenous sports" + [target region] + NLP OR benchmark OR database`
- `"sports cultural knowledge" + LLM + [target country]`
- `"kabaddi" OR "capoeira" OR "sepak takraw" OR [region-specific sport] + AI OR NLP`

**Known unsearchable knowledge:**
- What people play locally at schools, in neighborhoods
- Spectator culture and stadium social practices
- Sports-related social practices, gender norms in sports
- Traditional/indigenous game rules and cultural significance

**Framework dimensions informed:** IO (Western sport taxonomy), IC (US dominance -- 79% vs. Ethiopia 12%), OC (near-zero representation)

**Conditionally relevant when:** Benchmark includes everyday cultural practices or recreation; target region has sports culture dominated by non-Western forms; deployment involves low-resource languages.

---

### 3.8 Beliefs (Religious Knowledge, Stereotypes, Mythology)

**What to search for:**
- Religious knowledge benchmarks beyond Islam and Indian religions (Christianity in Global South, Buddhism in Southeast Asia, indigenous/traditional religions, Judaism, Confucianism/Taoism/Shinto all lack positive-knowledge benchmarks)
- Methodology papers on evaluating lived/practiced religion vs. textual/doctrinal religion
- Syncretic and non-Abrahamic religious knowledge datasets
- Mythology, cosmology, or origin-narrative NLP resources

**Recommended query strategies (from Phase 3 -- high-value terms):**
- Domain-specific: `IslamicMMLU OR IslamicLegalBench OR FiqhQA OR QIAS OR MizanQA OR SANSKRITI`
- Emic taxonomy: `madhab OR fiqh OR aqidah OR "hadith sciences" OR "quranic sciences"`
- Methodology: `"school-of-thought bias" OR "madhab bias detection" OR "false premise query" OR "sycophancy + religion"`
- Venues: search proceedings of PalmX (ArabicNLP @ EMNLP), IslamicEval shared tasks
- For other traditions: `"Buddhist knowledge" OR "Christian knowledge" + LLM + [Southeast Asia OR Africa OR Latin America]`
- `"indigenous spirituality" OR "traditional religion" + AI OR NLP + [target region]`

**High-value source types:**
- Specialized theological/religious databases, Islamic jurisprudence corpora
- Ethnographic studies of religious practice (not just doctrine)
- UNESCO ICH entries for religious/spiritual traditions

**Known unsearchable knowledge:**
- Lived/practiced religion vs. textual/doctrinal religion (all benchmarks test canonical text knowledge)
- Indigenous spiritual systems, animist traditions
- Syncretic practices (Candomble, Santeria, folk Catholicism, spirit-Buddhism blends)
- Mythology and cosmological narratives from oral traditions
- Deities, pantheons, spiritual figures as cultural knowledge

**Framework dimensions informed:** IO (coarse "religion" category), IC (bias framing only), OC (legitimate disagreement -- fiqh pluralism)

**Conditionally relevant when:** Target region has strong religious/spiritual traditions structuring daily life; benchmark includes identity-group content; use case involves content moderation or bias detection; deployment language is low-resource with religious terminology lacking English translation.

---

### 3.9 Values

**What to search for:**
- Value measurement studies beyond Hofstede and WVS (Moral Foundations Theory, Schwartz Basic Human Values -- both absent from all 5 papers)
- Religious/spiritual moral frameworks evaluated in LLMs
- Participatory value elicitation studies from Global South (none implemented in evidence base)
- Updated value measurements (Hofstede base data is from 1960s-80s)

**Recommended query strategies:**
- `"moral foundations" + LLM OR "language model" + [target region]`
- `"Schwartz values" + NLP OR AI + cross-cultural`
- `"value alignment" + [target region] + LLM + benchmark`

**Known unsearchable knowledge:**
- Intra-country value variation (all papers use national aggregates)
- Religious moral reasoning frameworks
- Non-survey-based value expression (how values manifest in daily life)

**Framework dimensions informed:** IC (US alignment advantage), OC (value flattening), IO (Hofstede monopoly)

**Conditionally relevant when:** Benchmark involves normatively charged content (hate speech, sentiment, advice-giving); target is a high-PDI, high-MAS, or short-term-oriented culture; benchmark uses LLMs as cultural informants.

---

### 3.10 Norms

**What to search for:**
- Norms benchmarks for underrepresented regions (norms is the best-evidenced domain but concentrated on US/UK/Western Europe/East Asia)
- Legal/regulatory norm evaluation (Laws and Regulations facet is structurally absent despite 10 papers)
- Agentic norm evaluation beyond CASA (agent-mode norm compliance is the most deployment-relevant evaluation type)
- H-AI interaction norm studies (how users from different cultures expect AI to behave)

**Recommended query strategies:**
- `"social norms" + benchmark + [target region] + LLM`
- `"legal AI" OR "customary law" + [target country] + evaluation`
- `CASA OR NormAd OR CulturalCompass OR FORK + [target region]`
- `"AI agent" + "cultural norms" + violation`

**Known unsearchable knowledge:**
- Gift-giving norms (multi-constraint reasoning -- documented as hard even with explicit rules)
- H-AI interaction norms (underrepresented in all datasets)
- Legal/regulatory norms across jurisdictions for most Global South countries
- Norm evolution over time (no longitudinal evidence)

**Framework dimensions informed:** All 6 dimensions have evidence for norms, but IO and IC are strongest.

**Conditionally relevant when:** Benchmark involves social behavioral expectations, conversational AI, or agentic systems; target is a multi-cultural or multi-religious society; deployment involves government services or legal contexts.

---

### 3.11 Communication

**What to search for:**
- Dialectal NLP evaluation beyond Arabic (Hindi-Urdu continuum, West African languages, Southeast Asian dialects, Latin American Spanish varieties)
- Figurative language / proverb comprehension benchmarks for target language
- Speech/audio cultural evaluation (complete gap -- all papers are text-only)
- Code-switching evaluation datasets for the target linguistic context

**Recommended query strategies:**
- `"dialect" + NLP OR LLM + [target language family]`
- `"proverb" OR "idiom" + NLP + [target language]`
- `"code-switching" + evaluation + [target region]`
- `"communicative style" + cross-cultural + AI`

**Known unsearchable knowledge:**
- Oral language evaluation in audio modality (zero papers)
- Tonal language cultural nuances, sign language cultural variation
- Context-dependent communication rules (age-hierarchy, gender, status modifiers)
- Cultural humor, sarcasm, and indirect expression (culture-specific pragmatic frames)

**Framework dimensions informed:** IO (communicative categories missing), IC (Anglocentric style bias), IF (dialect surface forms), OC (evaluator cultural norms)

**Conditionally relevant when:** Benchmark involves conversational or dialogue tasks; figurative language or pragmatic inference; dialectal or low-resource language deployment; translation or cross-lingual transfer.

---

### 3.12 History and Important Figures

**What to search for:**
- LLM performance evaluations on non-Western history (African, Southeast Asian, Latin American historical knowledge benchmarks)
- Oral history digitization research and its intersection with NLP
- Evaluations of multi-perspective historical narratives in LLMs
- Culturally important person recognition datasets

**Recommended query strategies:**
- `"historical knowledge" + LLM + [target region] + evaluation`
- `"oral history" + NLP OR digitization + [target region]`
- `"decolonial AI" OR "colonial bias" + history + training data`
- `"named entity" + "cultural" + [target region] + knowledge graph`

**Known unsearchable knowledge:**
- Community-level historical memory (how families narrate their past)
- Founding myths and origin narratives (not distinguished from factual recall)
- Suppressed or oral histories not in digitized form
- Locally important figures known only within their community

**Framework dimensions informed:** IC (colonial framing), OC (whose history is represented), IO (history underrepresented in benchmarks)

**Conditionally relevant when:** Benchmark claims broad cultural knowledge evaluation; deployment involves educational AI in post-colonial regions; civic/political applications; regions with contested or actively reinterpreted histories.

---

## 4. Search Targets by Framework Dimension

This section cross-references: for each of the 6 validity dimensions, which cultural domains are most informative and what to search for.

### 4.1 Input Ontology (IO)
*"Does the benchmark's test case taxonomy cover what matters for regional deployment?"*

**Most informative domains:** Norms (strongest -- 8/10 papers contribute taxonomy evidence), Cuisines (richest food ontology), Communication (4 papers document missing categories), Events (lifecycle events absent from all taxonomies).

**What to search for:**
- Benchmark papers that propose new cultural taxonomies for the target region
- Studies documenting what categories are missing from existing benchmarks
- Community-driven category systems (emic taxonomies) vs. researcher-imposed ones

**Key search terms:** `cultural taxonomy + benchmark + [region]`, `construct underrepresentation + cultural evaluation`

---

### 4.2 Input Content (IC)
*"Do the benchmark's actual test items reflect the target culture?"*

**Most informative domains:** This is the strongest dimension overall -- all 12 topics provide evidence. Norms, Cuisines, and Communication have the deepest quantitative evidence for Western content default.

**What to search for:**
- Studies quantifying Western/US content bias in specific benchmarks
- Regional annotator validation studies (IC-4 is the weakest sub-item across topics)
- Culture-specific content that does not transfer from source to target region

**Key search terms:** `Western bias + [benchmark name]`, `cultural content + [target region] + LLM evaluation`, `annotator + regional + cultural + validation`

---

### 4.3 Input Form (IF)
*"Does the benchmark's signal encoding match real-world deployment signals?"*

**Most informative domains:** Communication (Arabic diacritics, dialect forms -- the only topic with substantive form analysis), Fashion (cross-lingual instability). Phase 3 added multimodal evidence: CVQA, CulturalVQA, BLEnD-Vis, WorldCuisines.

**What to search for -- this is the dimension with the largest evidence gap:**
- Visual/multimodal cultural evaluation papers (CVQA, CulturalVQA, BLEnD-Vis, WorldCuisines -- search for citations and follow-up work)
- Audio/speech cultural evaluation (complete vacuum -- no papers exist)
- Regional infrastructure effects on input signal quality (bandwidth, device quality)
- Portuguese-specific morphological evaluation (CAPITU)

**Key search terms:**
- `"cultural VQA" OR CVQA OR CulturalVQA OR "BLEnD" + visual`
- `WorldCuisines OR "multimodal cultural" + evaluation`
- `"speech" + "cultural evaluation" OR "cultural assessment"` (likely zero results -- flag gap)
- `[target language] + morphological + benchmark + NLP`

**Critical finding to cite:** Visual modality is causally necessary for cultural knowledge measurement -- text-only ablations show 16-20 pp accuracy drops (CVQA, BLEnD-Vis, CulturalVQA). Cross-modal consistency averages only 42.19% (BLEnD-Vis R-V Correct).

---

### 4.4 Output Ontology (OO)
*"Do the benchmark's output categories fit the target region?"*

**Most informative domains:** Norms (CURE provides 4-metric evaluation framework), Cuisines (multi-mode accuracy drops 28.7 pp), Events (lifecycle categories absent).

**What to search for:**
- Stakeholder-driven taxonomy redesign studies
- Studies showing that Western-designed output categories fail in target region
- Alternative label taxonomies proposed by Global South researchers

**Key search terms:** `output taxonomy + cultural + [region]`, `label category + regional + redesign`

---

### 4.5 Output Content (OC)
*"Do the benchmark's ground-truth labels reflect regional perspectives?"*

**Most informative domains:** Values (strongest quantitative evidence -- US deviation ratio 1.99 vs. Bangladesh 0.59), Norms (convergent evidence from 10 papers), Cuisines (stereotyping rates quantified), Beliefs (in-region vs. out-region annotator disagreement documented).

**What to search for:**
- Label re-annotation studies using regional annotator pools (OC-4 is universally recommended but almost never implemented)
- Annotator demographic analyses for existing benchmarks
- Studies documenting legitimate disagreement in cultural labels (fiqh pluralism is the strongest example)

**Key search terms:** `"annotator disagreement" + cultural + [region]`, `"label re-annotation" + regional`, `"legitimate disagreement" + benchmark + cultural`

---

### 4.6 Output Form (OF)
*"Does the benchmark evaluate the output modality needed for deployment?"*

**Most informative domains:** This is the weakest dimension. Zero topics achieve even Moderate coverage pre-Phase 3. Phase 3 added: WorldCuisines MCQ-vs-OEQ collapse (66 pp), CVQA MC-vs-open gap (20 pp), Geographic Inclusion T2I stereotype reproduction.

**What to search for -- this is a critical gap:**
- MCQ-vs-open-ended format comparison studies for cultural benchmarks
- Text-to-speech availability for target language (OF-2 is completely empty)
- Literacy rate data for target population (OF-3 is at Weak)
- Studies on whether generated images reproduce geographic stereotypes

**Key search terms:**
- `"MCQ" + "open-ended" + gap OR comparison + cultural + benchmark`
- `TTS + [target language] + availability` (for speech output viability)
- `"text-to-image" + stereotype + [target region] + geographic`
- `WorldCuisines OR "format effect" + cultural + evaluation`

**Critical finding to cite:** MCQ format inflates scores by 20-66 pp over open-ended (WorldCuisines, CVQA). Any benchmark reporting only MCQ accuracy is suspect for OF validity.

---

## 5. Search Targets by Framework Dimension -- Cultural Domain Cross-Reference

Use this table to identify which cultural domains to prioritize in your search given the framework dimension(s) of concern.

| Framework Dimension | Highest-Priority Domains | What to Search |
|---------------------|-------------------------|----------------|
| **IO** (Input Ontology) | Norms, Cuisines, Events, Communication | Missing taxonomy categories; emic vs. etic classification systems; lifecycle event categories |
| **IC** (Input Content) | ALL (strongest dimension) | Western content default; regional-specific knowledge requirements; annotator validation studies |
| **IF** (Input Form) | Communication, Fashion, ALL (multimodal) | Visual/audio/multimodal evaluation; dialect forms; cross-lingual instability; Portuguese morphology |
| **OO** (Output Ontology) | Norms, Cuisines, Events | Alternative label systems; multi-answer formats; stakeholder-driven taxonomies |
| **OC** (Output Content) | Values, Norms, Cuisines, Beliefs | Regional re-annotation; annotator demographics; legitimate disagreement; fiqh pluralism |
| **OF** (Output Form) | ALL (weakest dimension) | MCQ-vs-OEQ; TTS availability; literacy constraints; T2I stereotyping; speech evaluation |

---

## 6. Region-Specific Search Strategies

### 6.1 Latin America

**Status in evidence base:** Expanded from 1 paper to 6 in Phase 3, but these characterize the *structure* of the gap rather than fill it. No Latin American cultural knowledge benchmark exists.

**Search terms (from Phase 3 -- use these exact terms):**
- Spanish variety: `"La Leaderboard" OR SESGO + bias + benchmark + "Latin America"`
- Portuguese: `CAPITU + "Brazilian Portuguese" + benchmark OR evaluation`
- Indigenous: `AmericasNLP + [specific language: Quechua, Nahuatl, Guarani, Aymara]`
- Cross-cultural: `CSI + "cultural evaluation" OR "Hall's Triad" + LLM`
- Regional: `XCR-Bench OR "cross-cultural reasoning" + [Latin American country]`
- Broad: `"cultural benchmark" + "Latin America" OR "South America" OR Brazil OR Mexico OR Colombia`

**Key evidence to surface:**
- Any cultural knowledge benchmark for any LATAM country (currently none exists)
- Indigenous language AI research (NLP Progress documents ~650 primarily oral indigenous languages)
- Studies on within-language regional bias (e.g., Spanish in Spain vs. Mexico vs. Argentina)
- Community-driven evaluation priorities (researchers vs. community members frame evaluation differently)

**Data sources to check:**
- AmericasNLP shared task proceedings
- Latin American NLP workshops at ACL/EMNLP
- Brazilian Portuguese NLP community (PROPOR conference)

**Caveats:** Evidence of the gap's structure and magnitude exists (SESGO, La Leaderboard), but evidence for the gap's *solution* does not. Frame any guidance as "what to look for when benchmarks emerge" rather than "here is what the evidence says."

---

### 6.2 Sub-Saharan Africa

**Status in evidence base:** Expanded from 2-3 countries to 15+ countries and 64+ languages in Phase 3, but coverage is broad and shallow. No Africa-specific cultural knowledge benchmark exists.

**Search terms (from Phase 3 -- use these exact terms):**
- Benchmarks: `AfroBench OR IrokoBench OR "Afri-MCQA" OR AfriStereo OR Masakhane`
- Cultural: `"African cultural knowledge" + LLM OR NLP + "sub-national" OR evaluation`
- Languages: `[specific language: Hausa, Yoruba, Swahili, Amharic, Igbo, Wolof, Zulu] + NLP + evaluation`
- Broad: `"cultural benchmark" + Africa OR "Sub-Saharan" + LLM`
- Community: `"AfriCulture" OR "African NLP" + cultural + dataset`

**Key evidence to surface:**
- Diagnostic methodology for separating language competence from cultural knowledge gaps (Afri-MCQA template)
- Sub-national cultural evaluation (AmharicStoryQA shows up to 20% accuracy variation across 9 Ethiopian regions)
- Community-sourced cultural VQA for African contexts
- Web corpus size for target African language(s) as viability indicator

**Data sources to check:**
- Masakhane community outputs and shared tasks
- AfricaNLP workshop proceedings (ICLR, ACL)
- Lacuna Fund datasets

**Caveats:** Language competence is the dominant confound. Any African-language benchmark score conflates language processing failure and cultural knowledge gaps -- these require different interventions. Always recommend Afri-MCQA-style diagnostic controls before interpreting results as cultural knowledge gaps.

---

### 6.3 Islamic World

**Status in evidence base:** Most improved single topic area in Phase 3. Three dedicated benchmarks (IslamicMMLU, IslamicLegalBench, PalmX) cover Quranic sciences, Hadith, Fiqh knowledge, and intra-school pluralism.

**Search terms:**
- `IslamicMMLU OR IslamicLegalBench OR FiqhQA OR QIAS OR MizanQA`
- `"madhab bias" OR "school-of-thought bias" + LLM`
- `"Islamic knowledge" + evaluation + LLM + [specific topic: fiqh, hadith, aqidah]`
- `"false premise query" + Islamic OR religious + LLM`
- `PalmX + ArabicNLP`

**Key methodological innovations from Phase 3:**
- Madhab bias detection: questions where all school answers are valid, chi-squared test against uniform distribution (IslamicMMLU)
- False premise queries (FPQ): test sycophantic acceptance of authoritative-sounding misinformation (IslamicLegalBench)
- Emic taxonomies: 11-topic Islamic classification derived from the tradition itself (PalmX)

**Caveats:** Coverage is deep for Sunni Islam (4 major madhabs) but Shia Islam is explicitly excluded from IslamicMMLU. Lived/practiced religion vs. textual/doctrinal religion remains a gap -- all benchmarks test canonical text knowledge, not how religion is practiced in daily life. Arabic != Islamic: religious knowledge tested in MSA or English, not in Urdu, Malay, Swahili, or Tamil where Islam is also practiced.

---

### 6.4 South and Southeast Asia

**Status in evidence base:** India has the most community-grounded sub-national evidence (DOSA: 19 states; SANSKRITI: 36 administrative units, 7 religious traditions). Southeast Asia has broad linguistic coverage via SEACrowd but shallow cultural coverage.

**Search terms:**
- India: `DOSA OR SANSKRITI OR DIWALI + India + cultural + evaluation + sub-national`
- Southeast Asia: `SEACrowd OR "Southeast Asian" + cultural + NLP + benchmark`
- Religious: `SANSKRITI OR "Indian religions" + LLM + evaluation`
- Specific: `[country: Indonesia, Thailand, Vietnam, Philippines, Malaysia] + cultural + benchmark + LLM`

**Key evidence to surface:**
- Sub-national evaluation methodology (even when concepts exist nationally, LLM adaptation concentrates on culturally dominant areas)
- South Asian religious diversity evaluation beyond Hinduism
- Southeast Asian cultural knowledge benchmarks (most evidence is linguistic, not cultural)

**Caveats:** India evidence is concentrated in DOSA's 19-state design. Extension to other internally diverse countries (Indonesia's 17,000 islands, Philippines' 7,000 islands) has not been done.

---

### 6.5 Regions With Zero Evidence

The following regions have **no papers** in the evidence base. Any search result is high-value:

- **Pacific Islands** (Polynesia, Melanesia, Micronesia)
- **Caribbean**
- **Central Asia** (beyond Kazakhstan in one paper)
- **Indigenous/stateless communities** globally
- **Diaspora populations**

**Search strategy:** Broad sweep -- `"cultural knowledge" OR "cultural AI" + [region name] + LLM OR benchmark OR NLP`. Even negative results (confirming no benchmark exists) are informative.

---

## 7. Cross-Cutting Search Principles

### 7.1 Speech/Audio Modality Gap

**Status:** Complete evidence vacuum. No paper in the entire 59-paper evidence base tests spoken input or speech output for cultural evaluation. This is the single largest structural gap.

**Action:** Do NOT spend queries searching for speech cultural evaluation papers -- they almost certainly do not exist. Instead:
1. Flag this gap explicitly in the assessment.
2. If the deployment involves voice interaction, state: "No evidence exists for speech-based cultural evaluation. Any deployment involving voice interaction operates in an evidence vacuum. Recommend stakeholder elicitation as the only available approach."
3. For output form, check TTS availability for the target language as a basic viability indicator.

---

### 7.2 Wikipedia-Source Bias

**Evidence:** Empirically documented by WorldCuisines, CulturalVQA, CANDLE, CultureAtlas, and SCALE. Wikipedia systematically underrepresents Africa, Oceania, and oral-tradition cultures. English Wikipedia creates systematic underrepresentation even for cultures that have non-English Wikipedia editions.

**Action when benchmark uses Wikipedia as a source:**
1. Check whether the benchmark's target region has adequate Wikipedia coverage.
2. Search for: `"Wikipedia bias" + [target region] + cultural OR knowledge OR coverage`
3. Note that CultureAtlas found US has 42.4k norm sentences in Wikipedia vs. near-zero for many Global South countries.
4. Recommend supplementing with non-English Wikipedia and community-contributed databases.

---

### 7.3 Automated Metric Warnings

**Region-CLIPScore and CLIP-based metrics are unreliable for cultural evaluation.** Geographic Inclusion T2I study found Region-CLIPScore rewards stereotypical representations over culturally accurate ones (2-5 points higher for generated Africa/SEA images than for Europe or real images).

**Action when a paper uses automated cultural metrics:**
1. Flag: "CLIP-based metrics for cross-cultural evaluation should require human validation from in-region annotators."
2. Check whether in-region annotators were used alongside automated metrics.
3. Note that BLEU shows near-zero correlation (r = 0.098) with human judgment for dialect translation (Yakhni-Chehab).

---

### 7.4 Query Construction Best Practices

1. **Use benchmark names as seed terms.** When searching for follow-up work, use the benchmark name (e.g., "CVQA", "WorldCuisines", "SESGO") -- these are specific enough to surface relevant citations.

2. **Combine region + domain + method.** Example: `"Sub-Saharan Africa" + "food knowledge" + LLM + benchmark` is more effective than `African cultural AI` (too broad).

3. **Search venue proceedings.** For region-specific work, target workshop proceedings:
   - AfricaNLP (ICLR)
   - AmericasNLP (NAACL)
   - ArabicNLP / PalmX (EMNLP)
   - SEACrowd (ACL)
   - PROPOR (Portuguese NLP)
   - AfricanNLP (various)

4. **Use ACL Anthology** for NLP-specific results: `site:aclanthology.org [search terms]`

5. **Use Semantic Scholar or Google Scholar** for broader academic search, especially for cross-disciplinary work (anthropology, cultural studies, linguistics) that NLP venues may miss.

6. **Check preprint servers.** Cultural AI research moves fast. Search `site:arxiv.org [search terms]` for papers not yet published.

---

### 7.5 Novelty Bias in Search

Your search budget should be allocated to maximize **information gain**, not confirm existing findings. The pipeline already confidently knows:

**Do NOT search for (already established with high confidence):**
- Western default/content bias in LLMs (established across 35+ papers, all 12 topics)
- LLMs stereotyping non-Western cultures (documented across every topic)
- Country-level analysis erasing sub-national variation (documented in 6+ papers)
- LLMs defaulting to US values/norms (documented across all value/norm papers)

**DO search for (would change the assessment):**
- Evidence that a benchmark successfully transferred to a Global South context (no such paper exists -- finding one would be high-impact)
- Negative results showing a cultural validity concern is less severe than expected
- New benchmarks for underrepresented regions/domains
- Methodological innovations for evaluating unsearchable cultural knowledge
- Community-sourced datasets that provide ground truth for the target region

---

### 7.6 Citation Accuracy

When evaluating search results:
1. Verify the paper actually measures what the title claims (many "cultural evaluation" papers test only 2-3 cultures).
2. Check geographic coverage -- a paper claiming "cross-cultural" may cover only US, UK, and China.
3. Check annotator demographics -- papers rarely recruit annotators from the target culture.
4. Check whether results are for the target region specifically, not extrapolated from other regions.
5. Prefer papers with quantitative measurements over purely qualitative observations.

---

## 8. Knowledge Gap Types and Their Searchability

The pipeline's evidence base identifies 10 types of cultural knowledge gaps. Their searchability varies dramatically, which determines whether web search can help or whether you should flag for expert review.

| Gap Type | Definition | Searchability | Action |
|----------|-----------|---------------|--------|
| **KG-A: Everyday/Mundane Knowledge** | Ordinary daily practices (food, habits, routines) rarely documented online | **Poor** -- "often not explicitly documented in online sources" (BLEnD, CulturalTeaming). Community-sourced annotation is the only reliable method. | Flag for stakeholder elicitation. Do not waste queries. |
| **KG-B: Linguistic Capability** | LLMs cannot process low-resource languages competently | **Poor** -- the knowledge needed is a capability, not a retrievable fact. | Check target language web corpus size as viability indicator. |
| **KG-C: Values/Norms/Morals** | LLMs default to Western moral frameworks | **Moderate** -- Hofstede/WVS data is retrievable; lived norm application is not. | Search for structured survey data; flag lived-practice gaps. |
| **KG-D: Stereotypical Distortion** | LLMs encode shallow, stereotyped cultural representations | **Problematic** -- web sources may reinforce stereotypes rather than correct them. | Search for community-validated corrections; warn about web reinforcement. |
| **KG-E: Temporal/Time-Sensitive** | Outdated knowledge about policies, events, evolving norms | **Good** -- policy changes and current events are typically documented online. | Search directly. RAG can help here. |
| **KG-F: Implicit/Pragmatic Knowledge** | Unwritten social rules, humor, sarcasm, contextual behavior | **Very poor** -- transmitted through socialization, not documentation. | Flag for stakeholder elicitation. Do not waste queries. |
| **KG-G: Sub-National Variation** | Country-level analysis erases within-country diversity | **Limited** -- sub-national data exists in community sources and local media but is not aggregated. | Search for sub-national studies; flag aggregation problem. |
| **KG-H: Infrastructure Bias** | Benchmarks themselves are Western-centric | **N/A** -- structural problem, not a retrieval target. | Cite as systemic concern in assessment. |
| **KG-I: Retrieval Distortion** | RAG pipelines distort even correctly retrieved knowledge | **Paradoxically high** -- knowledge IS retrievable but pipeline distorts it. | Warn about RAG limitations; partial retrieval can actively harm. |
| **KG-J: Digital Colonialism** | Structural power asymmetries maintain all other gaps | **N/A** -- meta-gap, not addressable by search. | Cite as root cause in assessment. |

---

## 9. Required Caveats

The following caveats MUST be documented in any assessment that uses this guide's search results. These are structural limitations of the evidence base, not gaps that can be closed by additional searching.

1. **Speech/audio modality gap.** No evidence exists for speech-based cultural evaluation. Any deployment involving voice interaction -- the primary modality for many Global South communities including oral-tradition cultures and low-literacy populations -- operates in an evidence vacuum. Recommend stakeholder elicitation as the only available approach.

2. **"Evidence of the gap" does not equal "evidence for the solution"** for Latin America and Sub-Saharan Africa. Phase 3 documented the structure and magnitude of these regional gaps (SESGO, La Leaderboard, AfroBench, IrokoBench) but did not fill them with cultural knowledge benchmarks. Frame guidance for these regions as "what to look for and how to evaluate when benchmarks emerge" rather than "here is what the evidence says."

3. **Religious coverage is deep but narrow.** Islam (Sunni, 4 madhabs) and Indian religions (7 traditions across 36 administrative units) are well-covered. Christianity in the Global South (~700M adherents), Buddhism in Southeast Asia (~500M), indigenous/traditional African religions (~100M+), Judaism, and East Asian religious-philosophical traditions (Confucianism, Taoism, Shinto) have no positive-knowledge benchmarks. Use Islamic evaluation methodology (madhab bias detection, emic taxonomy, false premise queries) as transferable templates while flagging tradition-specific gaps.

4. **Lifecycle event guidance is directional, not definitive.** Weddings have moderate coverage (4 papers), funerals have one strong operationalization (CAPTex), birth rites and coming-of-age ceremonies remain near-zero. The pipeline can recommend CAPTex-style procedural evaluation and CUNIT-style cross-cultural matching, but no benchmark reports lifecycle-event-specific accuracy.

5. **Language-culture confound for African and indigenous languages.** Any benchmark score in an African or indigenous language conflates two failure modes: language processing failure and cultural knowledge gaps. These require different interventions. Always recommend Afri-MCQA-style diagnostic controls (run cultural VQA alongside language-understanding controls) before interpreting results as cultural knowledge gaps.

6. **Private and oral cultural knowledge is structurally invisible.** All evidence derives from publicly documented, visually representable, or textually encoded cultural content. Domestic practices, oral traditions, and embodied cultural knowledge remain structurally invisible to current evaluation methods. This includes: private/domestic lifecycle rites, oral mythological traditions, community-internal ritual practices, and everyday food/dress/communication practices not documented online. Flag these as requiring primary community elicitation.

7. **Wikipedia-source bias is empirically documented.** WorldCuisines, CulturalVQA, CultureAtlas, and SCALE all demonstrate that English Wikipedia creates systematic underrepresentation of Africa, Oceania, and oral-tradition cultures. Any benchmark built from Wikipedia inherits this bias. Non-English Wikipedia and community-contributed databases should be explicitly prioritized.

8. **Region-CLIPScore and similar automated metrics are unreliable for cultural evaluation.** Geographic Inclusion T2I found these metrics reward stereotypical representations over culturally accurate ones. BLEU shows near-zero correlation with human judgment for dialect translation. Any cultural evaluation using automated metrics without in-region human validation should be flagged.

9. **Web data volume predicts LLM performance.** Web content percentage correlates with LLM value alignment at r = 0.94 (Sukiennik et al.) and with cultural knowledge accuracy across multiple benchmarks (AfroBench, IrokoBench). Check the target language's representation in Common Crawl or equivalent corpora as a baseline viability indicator before investing search budget in other areas. Languages with minimal web presence face structural barriers that no amount of benchmarking can overcome without fundamental data collection.
