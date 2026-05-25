## Use Case
A US enterprise software company is evaluating whether an LLM can generate complete full-stack web application scaffolding — database schemas, API routes, frontend component stubs, and deployment configurations — from multi-page, semi-structured requirements documents. The target benchmark for this evaluation is HumanEval. Users are American software architects who will assess outputs against internal architecture conventions as well as functional completeness.

## Target Population
Geography: United States. Sub-national cohort: N/A (enterprise software teams, implicitly concentrated in tech-industry hubs). Language: English. Occupation: Software architects and senior engineers working primarily with FastAPI + PostgreSQL + React/Next.js and secondarily with Spring Boot + MySQL + Angular, deploying to Docker/Kubernetes on AWS.

## Elicitation Responses

Q1 [IO]: HumanEval covers standalone Python functions in isolation. Your task involves multi-file, multi-layer artifacts: database schemas (SQL/ORM), REST or GraphQL API route definitions, frontend component stubs (React, Vue, etc.), and deployment configs (Docker, Kubernetes, Terraform). Does your evaluation need to cover all of these artifact types, or are some layers more critical to validate than others? Are there specific technology stacks your architects work with most?
A1: All four layers must be covered since the value proposition is end-to-end scaffolding, but the database schema and API route layers are the most critical — they are hardest to refactor post-generation. Primary stack is FastAPI + PostgreSQL + React/Next.js; secondary stack is Spring Boot + MySQL + Angular. Deployment targets Docker + Kubernetes on AWS, with occasional Terraform use.

Q2 [OO]: HumanEval scores outputs by running unit tests against a single correct function — binary pass/fail. For your scaffolding task, what does 'correct' mean: syntactic validity, requirements satisfaction, architectural convention adherence? Do architects accept multiple valid designs or grade against a house style?
A2: Correctness is layered: outputs must parse/compile and pass linting, satisfy stated requirements (entities, endpoints, flows present), and conform to internal conventions (naming, folder structure, auth middleware patterns, error handling). Multiple valid designs are acceptable, but a codified internal architecture guide serves as the grading rubric. Evaluation is closer to rubric-based expert review than binary unit-test pass/fail.

Q3 [IF]: HumanEval inputs are concise, self-contained docstrings. How long and structured are your requirements documents, and does the LLM receive them whole or in chunks?
A3: Specs are typically 3–10 page Confluence documents or PRDs with consistent headings (business context, user stories, data entities, API expectations, non-functional requirements) but variable prose under each section. The full document is currently fed in a single prompt; section-by-section prompting has been explored for larger specs.

## Dimension Priority Weights

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| IO | HIGH | HumanEval's ontology covers only isolated single-function Python synthesis; the deployment requires multi-artifact, multi-language, multi-layer scaffolding across at minimum four structurally distinct output types, leaving most of the task's input category space completely unrepresented. |
| IC | HIGH | HumanEval instances are algorithm/interview-style problems with no enterprise conventions, framework-specific idioms, or business-logic complexity; the deployment's inputs embed compliance requirements, SLA constraints, and domain-specific data models that are categorically absent from the benchmark's item pool. |
| IF | HIGH | HumanEval inputs are short, self-contained docstrings; deployment inputs are 3–10 page semi-structured PRDs fed as long single-context prompts, representing a fundamentally different input distribution in length, structure, and information density. |
| OO | HIGH | HumanEval's output space is a single Python function evaluated by deterministic unit tests (binary correctness); the deployment's output space is a multi-file, multi-language artifact set graded by rubric against architectural conventions, making the scoring function categorically incompatible. |
| OC | HIGH | HumanEval ground-truth labels are unit-test pass/fail on algorithm problems; the deployment's "correct" labels require expert architectural judgment against an internal style guide, meaning HumanEval label correctness is entirely inapplicable to the deployment task. |
| OF | MODERATE | Both benchmark and deployment use text-in / code-out modality, which limits mismatch at the signal level; however, HumanEval outputs a single function file while the deployment expects multi-file project trees across several languages and frameworks, creating a structural output-form gap that is non-trivial but less severe than the ontology and content mismatches. |

## Flagged Gaps

1. **Multi-artifact / multi-language code generation benchmarks**: HumanEval has no coverage of SQL/ORM schema generation, REST/GraphQL API scaffolding, frontend component stubs, or infrastructure-as-code. Downstream search should identify benchmarks or evaluation suites that cover these artifact types — e.g., CoderEval, SWE-bench, DevEval, APIBench, or enterprise-focused scaffolding evaluations.

2. **Rubric-based architectural correctness metrics**: No standard unit-test metric captures adherence to naming conventions, folder structure, auth middleware patterns, or modular architecture. Search should investigate whether any rubric-based or LLM-as-judge evaluation frameworks have been validated for enterprise code quality assessment (e.g., CodeScore, custom judge-model approaches).

3. **Long-context, document-to-code generation**: HumanEval's docstring inputs bear no resemblance to 3–10 page PRDs. Downstream search should check whether any benchmark specifically tests code generation from long-form requirements documents or user stories at realistic enterprise spec length.

4. **FastAPI / Spring Boot ecosystem coverage**: No existing HumanEval problem exercises framework-specific patterns (FastAPI dependency injection, SQLAlchemy ORM, Pydantic schema validation, Spring Boot annotations). Search should determine whether framework-specific code generation benchmarks exist for these stacks.

5. **Multi-file project coherence**: HumanEval evaluates each function independently; end-to-end scaffolding requires cross-file consistency (schema entities matching API models matching frontend props). This coherence dimension has no analog in HumanEval and may not be covered by any existing benchmark — this is a concrete gap to flag for custom evaluation design.

6. **Deployment configuration correctness**: Docker Compose, Kubernetes manifests, and Terraform modules are entirely outside HumanEval's scope. Search should determine whether infrastructure-as-code generation quality has been benchmarked and how correctness is assessed (e.g., static analysis, policy-as-code tools like OPA or Checkov).