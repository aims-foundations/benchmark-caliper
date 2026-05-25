## Use Case
A US-based debate coaching platform is evaluating whether an LLM can assess the strength of arguments made by American high school students in competitive debate (Policy, LD, PF, Congressional). The system must score argument quality holistically — covering evidence credibility, logical structure, relevance/responsiveness, and persuasive effectiveness — and provide qualitative coaching feedback, with scoring norms adapted by debate format and circuit.

## Target Population
United States high school students competing in interscholastic debate across multiple formats (Policy, Lincoln-Douglas, Public Forum, Congressional). Sub-national variation is significant: students compete on local circuits (e.g., Texas lay PF) and national-circuit events (TOC bid tournaments). Coaching staff and judges define quality standards via NSDA norms and circuit-specific paradigms. Language is English; all input and output is text-based.

## Elicitation Responses

Q1 [IO]: FOLIO focuses on formal deductive reasoning — given a set of premises, is a conclusion true, false, or uncertain. Your deployment involves much richer argument types: empirical claims backed by evidence, value-laden claims, rhetorical moves like analogy or burden-shifting, and debate-specific structures like disadvantages, counterplans, or kritiks. Which of these categories does your system need to assess, and are any of them more central than pure deductive validity?
A1: All four categories are required — empirical claims with evidence, value-laden claims, rhetorical moves, and debate-specific structural moves (DAs, CPs, kritiks). Pure deductive validity is the least central; most arguments are inductive or evidentiary. The heaviest weight falls on evidence quality and claim warrants, followed by relevance and responsiveness to the opponent's case.

Q2 [OO]: FOLIO scores outputs as a three-way label (true / false / uncertain), which captures logical entailment but not argument quality. Your deployment requires holistic strength assessment — covering logical validity, evidence quality, relevance, and persuasive effectiveness. Should the system produce a single composite score, separate scores per dimension, qualitative feedback, or a ranking across competing arguments? And who defines what 'strong' means — coaches, judges, debate norms, or the platform itself?
A2: The system should produce separate sub-scores across logic, evidence, relevance, and persuasiveness, plus qualitative coaching feedback explaining weaknesses. A composite score alone is not actionable for student development. Pairwise comparison for rebuttal practice is also needed. "Strong" is defined by external community standards — NSDA norms, TOC circuit paradigms, and coaching staff rubrics — not a purely platform-internal standard.

Q3 [OC]: In competitive high school debate, what counts as a strong argument is shaped by community norms that vary across circuits — for example, policy debate judges in the national circuit may reward speed and technical flow, while LD or PF judges in local circuits may weight rhetoric and clarity more heavily. Should the system's quality judgments reflect a single universal standard, or adapt to the judging community and format (policy, LD, PF, congressional) your students compete in?
A3: Adaptation by format is a minimum requirement; circuit-level adaptation is a strong desideratum. Winning criteria differ substantially — a lay PF round in Texas rewards clarity and rhetoric, while a tech-heavy LD round at a TOC bid event rewards speed and technical flow. The system must accommodate PF, LD, and Policy across both local and national circuit contexts.

Q4 [IC]: Debate arguments frequently involve contested empirical claims where evidence quality is disputed and value claims where reasonable people disagree. Does your system need to evaluate the credibility and recency of cited evidence, or only assess the logical structure of the argument as stated — and how should it handle premises that are empirically false but internally consistent?
A4: Evidence credibility and recency must be evaluated, since card quality is central to competitive debate; cherry-picked, outdated, or miscontextualized evidence should be flagged. For empirically false but internally consistent arguments, the system should note the factual problem while scoring logical structure separately, giving students feedback on both dimensions independently.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | FOLIO's ontology covers only formal FOL deductive entailment, while the deployment requires inductive/evidentiary reasoning, value-laden claims, rhetorical moves, and debate-specific structures (DAs, CPs, kritiks) — nearly none of which appear in FOLIO's category set. |
| IC | HIGH | FOLIO uses logically constructed premise sets with no normatively charged, culturally embedded, or evidentially disputed content; the deployment centers on contested empirical claims, miscontextualized evidence, and value judgments that carry heavy construct-irrelevant variance risk when assessed by a benchmark with clean logical scenarios. |
| IF | LOWER | Both benchmark and deployment are text-only in standard American English; no modality or script mismatch exists. |
| OO | HIGH | FOLIO's three-way entailment label (true/false/uncertain) is categorically mismatched to the deployment's required output space — multi-dimensional sub-scores, qualitative coaching feedback, pairwise strength rankings, and format/circuit-conditioned quality norms cannot be approximated by an entailment label. |
| OC | HIGH | FOLIO's ground-truth labels are determined by formal FOL inference engines and expert logicians, whereas the deployment's correctness standard is set by a pluralistic, format-varying, circuit-varying human judging community; annotator-population mismatch is near-total. |
| OF | HIGH | FOLIO produces a single categorical label; the deployment requires multi-dimensional scores, free-text coaching rationales, and pairwise comparative outputs — a fundamental output-form mismatch that makes benchmark performance metrics largely uninformative for deployment validity. |

## Flagged Gaps

1. **Inductive and evidentiary reasoning coverage**: Web search should investigate whether any NLI or argument-quality benchmarks specifically cover inductive argument structures, evidence-quality assessment, or citation credibility tasks — FOLIO is exclusively deductive and will produce ceiling/floor effects irrelevant to deployment needs.

2. **Debate-specific argument ontologies**: The deployment references DAs, CPs, kritiks, and burden-shifting as first-class argument types. Downstream search should check whether any existing benchmarks (e.g., IBM Debater datasets, ArgMining corpora, or competitive debate-specific corpora) cover these structures and whether any include format-level labels (Policy vs. LD vs. PF).

3. **Circuit- and format-conditioned quality norms**: The deployment's definition of "strong argument" is explicitly pluralistic across lay vs. tech circuits and across formats. No benchmark is known to encode circuit paradigm variation; search should confirm whether any annotation schemes capture judge-style or format-conditioned rubrics (NSDA, TOC, local circuit).

4. **Evidence credibility and card-quality assessment**: The user requires flagging of cherry-picked, outdated, or miscontextualized evidence — a task closer to fact-checking or information retrieval quality assessment than to logical reasoning. Search should identify whether any benchmark evaluates source credibility, recency, or out-of-context quotation detection in argumentative text.

5. **Value-laden and normatively contested premises**: FOLIO explicitly avoids normatively ambiguous premises; the deployment requires handling claims where reasonable people disagree (e.g., "economic growth outweighs environmental protection"). Search should assess whether any argument-quality benchmarks include value-pluralism scenarios or moral/political reasoning tasks with annotator disagreement statistics.

6. **Pairwise argument comparison**: The deployment requires head-to-head rebuttal comparison, not standalone argument scoring. Search should determine whether existing benchmarks include comparative or contrastive argument ranking tasks, which would be structurally closer to the deployment's use case than FOLIO's binary premise-conclusion entailment format.