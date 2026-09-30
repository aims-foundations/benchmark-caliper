"""Snapshot the original assessment and deterministic dataset evidence."""

from pathlib import Path

from .data import file_sha256, prepare_data
from .storage import read_json, write_json

PIPELINE_DIR = Path(__file__).resolve().parents[1]
REQUIRED_ASSESSMENT_FILES = (
    "scoring.json", "deployment_description.txt", "elicitation_summary.md",
    "dataset_analysis_report.md",
)


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
