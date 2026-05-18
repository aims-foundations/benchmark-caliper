"""Read-only access to pipeline ICL assets.

The website reuses the existing `anthropic_api_package_release/benchmarks/examples`
and `regions/base` directories as in-context-learning seeds for synthesis
steps. We never modify these files — they are the same versioned references
the CLI pipeline uses.
"""

from __future__ import annotations

from pathlib import Path

_PACKAGE_ROOT = (
    Path(__file__).resolve().parent.parent.parent / "anthropic_api_package_release"
)
BENCHMARK_EXAMPLES_DIR = _PACKAGE_ROOT / "benchmarks" / "examples"
REGION_TEMPLATES_DIR = _PACKAGE_ROOT / "regions" / "base"
FRAMEWORK_PATH = _PACKAGE_ROOT / "framework.yaml"


def load_framework() -> str:
    """Read the validity-framework YAML (6 dimensions + scoring rubric)
    that Opus uses as scoring criteria."""
    return FRAMEWORK_PATH.read_text()


def list_benchmark_examples() -> list[str]:
    """Return the basenames of available benchmark example YAMLs, sorted."""
    if not BENCHMARK_EXAMPLES_DIR.exists():
        return []
    return sorted(p.name for p in BENCHMARK_EXAMPLES_DIR.glob("*.yaml"))


def load_benchmark_example(name: str) -> str:
    """Read one example YAML by basename. Raises FileNotFoundError if
    the name does not match an existing file (defensive against the
    LLM hallucinating a filename)."""
    if "/" in name or ".." in name or not name.endswith(".yaml"):
        raise FileNotFoundError(f"invalid example name: {name!r}")
    path = BENCHMARK_EXAMPLES_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"benchmark example not found: {name}")
    return path.read_text()


def benchmark_manifest() -> str:
    """Compact one-line-per-file manifest for the example-selection step."""
    names = list_benchmark_examples()
    return "\n".join(f"- {n}" for n in names)


def list_region_templates() -> list[str]:
    """Return the basenames of available region template YAMLs, sorted."""
    if not REGION_TEMPLATES_DIR.exists():
        return []
    return sorted(p.name for p in REGION_TEMPLATES_DIR.glob("*.yaml"))


def load_region_template(name: str) -> str:
    """Read one region template YAML by basename."""
    if "/" in name or ".." in name or not name.endswith(".yaml"):
        raise FileNotFoundError(f"invalid template name: {name!r}")
    path = REGION_TEMPLATES_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"region template not found: {name}")
    return path.read_text()


def region_manifest() -> str:
    """Compact manifest for the region-template-selection step."""
    names = list_region_templates()
    return "\n".join(f"- {n}" for n in names)
