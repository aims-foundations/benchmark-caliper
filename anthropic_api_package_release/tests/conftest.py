"""Session-wide test setup: generate a tiny dummy PDF for the pipeline to chew on."""

from __future__ import annotations

import sys
from pathlib import Path

# Make api_package importable (run_pipeline, client, prompts, personas).
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
DUMMY_PDF = FIXTURES / "dummy.pdf"


def _generate_dummy_pdf(path: Path, pages: int = 2) -> None:
    """Emit a minimal N-page PDF using pypdf (no external tools needed)."""
    from pypdf import PdfWriter
    from pypdf.generic import RectangleObject

    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=72, height=72)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        writer.write(f)


@pytest.fixture(scope="session", autouse=True)
def _ensure_dummy_pdf():
    if not DUMMY_PDF.exists():
        _generate_dummy_pdf(DUMMY_PDF, pages=2)
    yield DUMMY_PDF
