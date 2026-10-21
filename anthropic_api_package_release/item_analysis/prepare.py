"""Freeze assessment evidence or explicit deployment requirements with items."""

from copy import deepcopy
from pathlib import Path
from itertools import islice
import re

from .data import file_sha256, prepare_data, read_items
from .storage import read_json, write_json

PIPELINE_DIR = Path(__file__).resolve().parents[1]
REQUIRED_ASSESSMENT_FILES = (
    "scoring.json", "deployment_description.txt", "elicitation_summary.md",
    "dataset_analysis_report.md",
)

DIRECT_CONTEXT_FIELDS = (
    "benchmark", "deployment", "task_requirements", "answer_requirements", "validity_concerns",
)


def attach_direct_context(directory: Path, context: dict, *, deployment: str | None = None,
                          confirmed_source: bool = False) -> dict:
    """Freeze explicit requirements after ``prepare_data``, without an assessment.

    The caller validates access and confirms the source. ``deployment`` may be a
    canonical rendering of the raw context fields; both forms are retained.
    This must precede specification creation and cannot replace frozen evidence.
    """
    directory = Path(directory)
    if not isinstance(context, dict) or set(context) - set(DIRECT_CONTEXT_FIELDS):
        raise ValueError("Direct context must contain only the supported requirement fields")
    for field in DIRECT_CONTEXT_FIELDS[:-1]:
        if not isinstance(context.get(field), str) or not context[field].strip():
            raise ValueError(f"Direct context requires nonempty {field}")
    if "validity_concerns" in context and not isinstance(context["validity_concerns"], str):
        raise ValueError("validity_concerns must be text when supplied")
    frozen = deepcopy(context)
    deployment = frozen["deployment"] if deployment is None else deployment
    if not isinstance(deployment, str) or not deployment.strip():
        raise ValueError("Direct deployment must be nonempty text")
    if any((directory / name).exists() for name in (
        "evidence.json", "direct_context.json", "classifier_spec.json", "specification.json", "run.json",
    )):
        raise ValueError("Direct context requires a fresh prepared dataset; evidence is already frozen")
    dataset = read_json(directory / "dataset.json")
    normalized = lambda name: re.sub(r"[^a-z0-9]", "", name.lower())
    if not confirmed_source and normalized(dataset["benchmark"]) != normalized(frozen["benchmark"]):
        raise ValueError("The prepared dataset does not match the direct benchmark context")
    # Verify the item/profile files before attaching new evidence.
    for filename, key in (("items.jsonl", "items_sha256"), ("profile.json", "profile_sha256")):
        if file_sha256(directory / filename) != dataset[key]:
            raise ValueError(f"Prepared {filename} changed before attaching direct context")
    requirements = {field: frozen[field] for field in DIRECT_CONTEXT_FIELDS[2:]
                    if frozen.get(field, "").strip()}
    documents = {
        "deployment_description.txt": deployment,
        "framework.yaml": (PIPELINE_DIR / "framework.yaml").read_text(encoding="utf-8"),
        **{f"direct_context.json#/{field}": value for field, value in frozen.items() if value.strip()},
    }
    registry, roles, gaps = build_sources(directory, documents)
    evidence = {
        "benchmark": frozen["benchmark"], "deployment": deployment,
        "analysis_basis": "deployment_requirements", "assessment_status": "not_run",
        "requirements": requirements, "direct_context": frozen, "registry": registry,
        "source_roles": roles, "evidence_gaps": gaps,
    }
    write_json(directory / "direct_context.json", frozen)
    write_json(directory / "evidence.json", evidence)
    dataset.update({
        "source_benchmark": dataset["benchmark"], "benchmark": frozen["benchmark"],
        "analysis_basis": "deployment_requirements", "assessment_status": "not_run",
        "direct_context_sha256": file_sha256(directory / "direct_context.json"),
        "evidence_sha256": file_sha256(directory / "evidence.json"),
    })
    write_json(directory / "dataset.json", dataset)
    return dataset


def evidence_registry(scoring: dict, documents: dict) -> dict:
    """Provide resolvable source IDs for generated classifier citations."""
    registry = dict(documents)

    def visit(value, pointer):
        if isinstance(value, dict):
            for key, child in value.items():
                escaped = str(key).replace("~", "~0").replace("/", "~1")
                visit(child, f"{pointer}/{escaped}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{pointer}/{index}")
        elif value is not None:
            registry[f"scoring.json#{pointer}"] = value

    visit(scoring, "")
    return registry


# Explicit artifacts emitted by the pipeline, plus documented supplemental
# evidence files. Names retain their exact registry identity and full contents.
OPTIONAL_SOURCE_ROLES = {
    "elicitation_questions.json": "elicitation_question",
    "elicitation_answers.json": "deployment_requirement",
    "benchmark.yaml": "benchmark_evidence",
    "paper_summary.md": "benchmark_evidence",
    "metadata.md": "benchmark_evidence",
    "quote_registry.md": "benchmark_evidence",
    "output_taxonomy.json": "benchmark_evidence",
    "output_taxonomy.md": "benchmark_evidence",
    "scoring_documentation.md": "benchmark_evidence",
    "annotation_documentation.md": "benchmark_evidence",
    "region.yaml": "domain_evidence",
    "region_scaffold.yaml": "domain_evidence",
    "traces/5_web_search.jsonl": "domain_evidence",
    "domain_evidence.md": "domain_evidence",
    "domain_standards.md": "domain_evidence",
    "stakeholder_evidence.md": "stakeholder_evidence",
    "stakeholder_judgments.json": "stakeholder_evidence",
}


def source_role(source_id: str) -> str:
    # This model-written report mixes observations and prior concerns. Treat
    # it conservatively as hypotheses; direct items/profile/docs ground facts.
    if source_id.startswith("scoring.json") or source_id == "dataset_analysis_report.md":
        return "prior_assessment"
    if source_id == "direct_context.json#/validity_concerns":
        return "prior_hypothesis"
    if source_id in ("deployment_description.txt", "elicitation_summary.md") or source_id.startswith("direct_context.json#/"):
        return "deployment_requirement"
    if source_id == "framework.yaml":
        return "rubric"
    if source_id == "profile.json":
        return "dataset_profile"
    if source_id.startswith("items.jsonl#/"):
        return "example_item"
    return OPTIONAL_SOURCE_ROLES.get(source_id, "benchmark_evidence")


def build_sources(directory: Path, documents: dict, *, scoring: dict | None = None,
                  assessment_dir: Path | None = None) -> tuple[dict, dict, list[str]]:
    """Snapshot source contents, roles and explicit availability gaps.

    Optional source_registry.json accepts exact IDs mapped to {content, role};
    it allows supplied standards/quotes without fabricating evidence or IDs.
    It may not replace the pipeline's already registered sources.
    """
    documents = deepcopy(documents)
    if assessment_dir is not None:
        for filename in OPTIONAL_SOURCE_ROLES:
            path = Path(assessment_dir) / filename
            if path.is_file():
                content = path.read_text(encoding="utf-8")
                if content.strip():
                    documents.setdefault(filename, content)
        # Paper-scoped metadata and quoted documentation are used only when the
        # assessment path has the pipeline's actual assessments/name/slug shape.
        assessment_dir = Path(assessment_dir).resolve()
        if assessment_dir.parent.parent.name == "assessments":
            paper_dir = assessment_dir.parent.parent.parent / "papers" / assessment_dir.parent.name
            for filename in ("metadata.md", "quote_registry.md", "paper_summary.md"):
                path = paper_dir / filename
                if path.is_file() and filename not in documents:
                    documents[f"papers/{assessment_dir.parent.name}/{filename}"] = path.read_text(encoding="utf-8")
    registry = evidence_registry(scoring or {}, documents)
    registry["profile.json"] = read_json(directory / "profile.json")
    for index, item in enumerate(islice(read_items(directory / "items.jsonl"), 8)):
        registry[f"items.jsonl#/{index}"] = item
    roles = {key: source_role(key) for key in registry}
    if assessment_dir is not None and (assessment_dir / "source_registry.json").is_file():
        supplemental = read_json(assessment_dir / "source_registry.json")
        if not isinstance(supplemental, dict):
            raise ValueError("source_registry.json must map exact source IDs to content and role")
        allowed = set(OPTIONAL_SOURCE_ROLES.values()) | {"deployment_requirement", "prior_hypothesis", "prior_assessment", "rubric"}
        for key, entry in supplemental.items():
            if key in registry:
                raise ValueError(f"Supplemental registry cannot replace existing source {key}")
            if (not isinstance(entry, dict) or set(entry) != {"content", "role"}
                    or entry["role"] not in allowed or entry["content"] in (None, "", [], {})):
                raise ValueError(f"Supplemental source {key} requires nonempty content and a supported role")
            registry[key] = entry["content"]
            roles[key] = entry["role"]
    gaps = []
    if not any(roles.get(key) == "benchmark_evidence" and key != "dataset_analysis_report.md" for key in registry):
        gaps.append("No benchmark taxonomy, scoring, or annotation documentation was supplied beyond the dataset analysis report.")
    if "domain_evidence" not in roles.values():
        gaps.append("No domain standards or domain evidence were supplied.")
    if "stakeholder_evidence" not in roles.values():
        gaps.append("No documented stakeholder judgments or disagreements were supplied.")
    return registry, roles, gaps


def prepare(assessment_dir: Path, items_path: Path, output_dir: Path, *, benchmark=None,
            seed=42, source_repo="aims-foundations/measurement-db", source_revision=None,
            source_table=None) -> dict:
    # Fail before preparing data if a required upstream artifact is absent.
    documents = {name: (assessment_dir / name).read_text(encoding="utf-8")
                 for name in REQUIRED_ASSESSMENT_FILES}
    scoring = read_json(assessment_dir / "scoring.json")
    actual_benchmark = scoring.get("benchmark")
    if not isinstance(actual_benchmark, str) or not actual_benchmark.strip():
        raise ValueError("scoring.json must identify the benchmark")
    if benchmark is not None and benchmark != actual_benchmark:
        raise ValueError("Requested benchmark does not match the original assessment")
    for name, text in documents.items():
        if not text.strip():
            raise ValueError(f"Assessment artifact is empty: {name}")
    if not isinstance(scoring.get("dimensions"), dict):
        raise ValueError("scoring.json must contain the original dimension assessments")
    documents["framework.yaml"] = (PIPELINE_DIR / "framework.yaml").read_text(encoding="utf-8")
    evidence = {
        "benchmark": actual_benchmark, "assessment_dir": str(assessment_dir.resolve()),
        "deployment": documents["deployment_description.txt"], "scoring": scoring,
        "elicitation_summary": documents["elicitation_summary.md"],
        "dataset_analysis_report": documents["dataset_analysis_report.md"],
    }
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("Prepare requires an empty output directory")
    dataset = prepare_data(items_path, output_dir, benchmark=actual_benchmark, seed=seed,
                           source_repo=source_repo, source_revision=source_revision,
                           source_table=source_table)
    registry, roles, gaps = build_sources(output_dir, documents, scoring=scoring, assessment_dir=assessment_dir)
    evidence.update(registry=registry, source_roles=roles, evidence_gaps=gaps)
    write_json(output_dir / "evidence.json", evidence)
    dataset["evidence_sha256"] = file_sha256(output_dir / "evidence.json")
    write_json(output_dir / "dataset.json", dataset)
    return dataset
