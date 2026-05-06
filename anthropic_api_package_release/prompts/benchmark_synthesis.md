Synthesize a benchmark YAML from a paper summary, using 1-2 reference examples
as style and schema guides.

The user message contains:
- The full paper summary from the extraction step (narrative + verbatim quote registry).
- 1-2 selected reference YAMLs from `benchmarks/examples/`. These are **format,
  style, and depth guides — do NOT copy their content verbatim.**

## Required fields (top level)

- `name` — short identifier (lowercase, no spaces)
- `full_name` — full benchmark title from the paper
- `year` — publication year
- `domain` — what the benchmark evaluates
- `porting_strategy` — one of: `ground_up`, `adapted`, `mixed`, `translation`,
  `parallel`, `regional_exams`, `none`
- `languages` — list of language codes
- `primary_region` — geographic or cultural region the benchmark targets

## The 6 validity dimensions

Both the `documentation_excerpts` narrative and the per-quote `dimension` tags
below use these six dimensions (2×3 grid: Input/Output × Ontology/Content/Form).
Use the definitions below so that the tagging and narrative you produce here
align with the definitions the downstream Opus scorer will use. The "Cues" line
under each is an operational addendum for this step only — concrete signals that
commonly mark a quote as belonging to that dimension.

- **input_ontology** — The input data ontology consists of the set of test case categories represented by the benchmark, which should cover the query types that evaluated systems are expected to encounter during deployment (e.g., factual questions, creative writing help, or restaurant recommendations for NLP dialogue systems; pick-and-place tasks, point navigation, or planning for robotics). A misalignment in this taxonomy — whether through the omission of necessary categories (construct underrepresentation) or the inclusion of irrelevant ones (construct-irrelevant variance) — harms the content validity of the benchmark.
  Cues: task types, subtask breakdown, coverage, stated gaps in the taxonomy.

- **input_content** — Whereas the ontology defines the types of input queries, the content of dataset inputs refers to the explicit instances specified by individual datapoints — an LLM prompt, an image, a database entry, etc. Even when the test case taxonomy provides good coverage, implementation-level details of individual datapoints can introduce construct-irrelevant variance, violating content validity.
  Cues: data sources, collection methodology, cultural grounding of the instances.

- **input_form** — The form of dataset inputs determines the encoding of the input signal — e.g., text vs. audio for natural language, or camera parameters such as focal length and resolution for visual data. Since machine learning systems are sensitive to signal distributions, a mismatch between the benchmark's input representation and the real-world signals that deployed models would encounter violates the external validity of the evaluation.
  Cues: modality, length, language, format, infrastructure assumptions (e.g. written vs spoken, script, SMS-length constraints).

- **output_ontology** — A benchmark's output ontology determines the space of outputs an AI system is expected to produce and the decision rules by which those outputs are organized and scored — i.e., the benchmark's criteria. For categorical outputs, the mapping is direct (e.g., safe/unsafe, or object class labels). For free-form outputs, the scoring function must first interpret what the output means before mapping it to a score — and this interpretive step is where validity violations most readily arise, since decision rules can differ across cultural contexts. For instance, an LLM recommending "red wine" for a dinner party may score highly for helpfulness in a Western context but poorly where alcohol consumption is prohibited. A misaligned output taxonomy thus violates structural validity (the construct's structure is misrepresented), content validity (through missing or irrelevant categories), and risks violating external validity (benchmark performance is less likely to generalize to regional settings).
  Cues: label set, ground-truth schema, taxonomy of correct-answer types.

- **output_content** — Whereas taxonomic alignment addresses whether abstract decision boundaries reflect regional values, label correctness concerns whether the labels for particular datapoints correlate with the judgments of regional stakeholders. Disagreement between regional and original annotators violates both convergent validity (the labels fail to correlate with regional perspectives on the construct) and external validity (the original judgments do not generalize to the target context).
  Cues: annotation process, annotator demographics, inter-annotator agreement, label provenance.

- **output_form** — The form of dataset outputs pertains to the representation of output signals models are expected to produce. If a benchmark does not evaluate models on the output forms encountered during real-world deployment, this violates the external validity of the evaluation.
  Cues: output modality, evaluation metric definition, scoring methodology.

## Required section: `documentation_excerpts`

Interpretive narrative organized by the 6 validity dimensions, referencing quotes
by registry IDs (e.g., `[Q3]`, `[Q14]`). Structure with these exact headers:

1. **Input Ontology**
2. **Input Content**
3. **Input Form**
4. **Output Ontology**
5. **Output Content**
6. **Output Form**

Under each header, write the interpretive narrative for that dimension anchored
to the definition above. Propagate "NOT DOCUMENTED" notes from the paper summary
where a dimension has no supporting quotes.

## Required section: `verbatim_quotes`

Tag ALL Quote Registry entries with their validity dimension. Do NOT include the
quote text — it will be filled in programmatically from the registry. Output only
`id`, `page`, and `dimension`:

```yaml
verbatim_quotes:
  - id: Q1
    page: 20
    dimension: input_ontology
```

Rules:
- Propagate ALL quotes — do not drop any.
- Tag each quote with the most relevant validity dimension using the definitions above. A quote's *extraction category* (`task_taxonomy`, `evaluation_metrics`, etc. from the registry) is a hint, not a mapping — e.g. a `task_taxonomy` quote about output label types belongs to `output_ontology`, not `input_ontology`.

## Required section: `coverage_strengths`

**Only include this section if an elicitation summary is provided in the user
message.** If no elicitation summary is present, omit the section entirely.

Cross-reference the elicitation summary against the benchmark documentation to
identify where the benchmark's coverage aligns well with the user's deployment
priorities. For each HIGH-priority dimension and each cultural topic priority,
note where the benchmark documents relevant coverage.

```yaml
coverage_strengths:
  - user_priority: "French biomedical NLP"
    benchmark_coverage: "12 datasets spanning NER, STS, classification in French clinical text [Q5]"
    dimension: input_content
  - user_priority: "drug labeling terminology"
    benchmark_coverage: "QUAERO dataset drawn from EMEA drug labels with UMLS entity annotation [Q12]"
    dimension: input_ontology
```

Each entry should reference at least one quote ID grounding the strength in
the paper's documentation.

## Required section: `coverage_gap_analysis`

**Only include this section if an elicitation summary is provided in the user
message.** If no elicitation summary is present, omit the section entirely.

Cross-reference the elicitation summary against the benchmark documentation to
identify where the user's priorities and the benchmark's actual coverage diverge.
For each HIGH-priority dimension and each cultural topic priority from the
elicitation summary, assess whether the benchmark documents relevant content.

```yaml
coverage_gap_analysis:
  - user_priority: "sub-national variation in Nigeria"
    benchmark_coverage: "Country-level only — no state or ethnic group breakdown"
    gap_type: "partial"
    web_search_target: "Sub-national cultural variation benchmarks Nigeria Yoruba Igbo Hausa"
  - user_priority: "regional cuisines"
    benchmark_coverage: "NOT DOCUMENTED — no food-related tasks"
    gap_type: "full"
    web_search_target: "Nigerian cuisine cultural knowledge AI evaluation"
```

Gap types:
- **full**: The benchmark is silent on this priority. Web search should look for
  supplementary evidence or alternative benchmarks.
- **partial**: The benchmark addresses this but at insufficient depth or the wrong
  granularity for the user's context.
- **none**: The benchmark covers this priority well. No web search needed.

The `web_search_target` field provides a suggested search query for the web
search step. Only populate for `full` and `partial` gaps.

## Schema enforcement

This schema is enforced by downstream scripts (`verify_quotes.py`,
`compose_prompt.py`). Treat it as a hard requirement, not a suggestion. Use the
reference YAMLs to match tone, field depth, and narrative density; use the
schema to guarantee downstream compatibility.

## Output

Output ONLY the YAML document. Wrap it in a ```yaml fenced block so it can be
extracted cleanly.
