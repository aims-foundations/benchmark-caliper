"""PDF helpers for the website backend.

Step 1 (metadata extraction) only needs pages 1-2. Sending the full PDF to
Haiku wastes input tokens — a 30-page paper costs ~10x more in input tokens
than just the title-page + abstract pages. We trim before the API call.
"""

from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader, PdfWriter


def first_pages(pdf_bytes: bytes, n_pages: int = 2) -> bytes:
    """Return a new PDF containing only the first `n_pages` pages.

    If the source has fewer pages, returns whatever is available. Raises
    ValueError if the PDF is encrypted or unreadable.
    """
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
    except Exception as e:
        raise ValueError(f"could not read PDF: {e}") from e

    if reader.is_encrypted:
        raise ValueError("encrypted PDFs are not supported")

    writer = PdfWriter()
    for page in reader.pages[:n_pages]:
        writer.add_page(page)

    out = BytesIO()
    writer.write(out)
    return out.getvalue()


def page_count(pdf_bytes: bytes) -> int:
    """Number of pages, or 0 if the PDF is unreadable."""
    try:
        return len(PdfReader(BytesIO(pdf_bytes)).pages)
    except Exception:
        return 0


def split_pages(pdf_bytes: bytes) -> list[bytes]:
    """Split a PDF into a list of single-page PDFs (one bytes blob per page).

    Each entry is a complete, standalone PDF containing exactly one page.
    Used by Step 3a so each page can be sent to Haiku in parallel.

    Raises ValueError on encrypted or unreadable input.
    """
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
    except Exception as e:
        raise ValueError(f"could not read PDF: {e}") from e

    if reader.is_encrypted:
        raise ValueError("encrypted PDFs are not supported")

    out: list[bytes] = []
    for page in reader.pages:
        writer = PdfWriter()
        writer.add_page(page)
        buf = BytesIO()
        writer.write(buf)
        out.append(buf.getvalue())
    return out
