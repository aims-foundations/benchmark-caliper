"""Freeze assessment evidence or explicit deployment requirements with items."""

from copy import deepcopy
from pathlib import Path
import re

from .data import file_sha256, prepare_data
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
    registry = {
        "deployment_description.txt": deployment,
        "framework.yaml": (PIPELINE_DIR / "framework.yaml").read_text(encoding="utf-8"),
        **{f"direct_context.json#/{field}": value for field, value in frozen.items() if value.strip()},
    }
    evidence = {
        "benchmark": frozen["benchmark"], "deployment": deployment,
        "analysis_basis": "deployment_requirements", "assessment_status": "not_run",
        "requirements": requirements, "direct_context": frozen, "registry": registry,
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
    registry = evidence_registry(scoring, {k: v for k, v in documents.items() if k != "scoring.json"})
    evidence = {
        "benchmark": actual_benchmark, "assessment_dir": str(assessment_dir.resolve()),
        "deployment": documents["deployment_description.txt"], "scoring": scoring,
        "elicitation_summary": documents["elicitation_summary.md"],
        "dataset_analysis_report": documents["dataset_analysis_report.md"],
        "registry": registry,
    }
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("Prepare requires an empty output directory")
    dataset = prepare_data(items_path, output_dir, benchmark=actual_benchmark, seed=seed,
                           source_repo=source_repo, source_revision=source_revision,
                           source_table=source_table)
    write_json(output_dir / "evidence.json", evidence)
    dataset["evidence_sha256"] = file_sha256(output_dir / "evidence.json")
    write_json(output_dir / "dataset.json", dataset)
    return dataset
