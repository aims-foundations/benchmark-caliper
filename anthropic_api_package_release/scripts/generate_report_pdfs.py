#!/usr/bin/env python3
"""generate_expert_pdfs.py -- Generate section PDFs for expert validation survey.

Produces 7 PDFs per assessment tuple: 1 summary + 6 dimension sections.
Each dimension PDF includes inline evidence tables after every cited paragraph,
with full repetition of shared citations and full expansion of citation ranges.

Usage:
    python3 scripts/stage3/generate_expert_pdfs.py
    python3 scripts/stage3/generate_expert_pdfs.py --tuple assessments/expert_.../slug/
"""

import argparse
import json
import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(it, **kw):
        return it


# === Constants ===

DIM_LABELS = {
    "input_ontology": "Input Ontology",
    "input_content": "Input Content",
    "input_form": "Input Form",
    "output_ontology": "Output Ontology",
    "output_content": "Output Content",
    "output_form": "Output Form",
}

DIM_ABBREVS = {
    "input_ontology": "IO", "input_content": "IC", "input_form": "IF",
    "output_ontology": "OO", "output_content": "OC", "output_form": "OF",
}

DIM_DEFINITIONS = {
    "input_ontology": "Whether the benchmark's test case categories cover the query types expected in deployment.",
    "input_content": "Whether individual datapoint content is culturally and contextually appropriate for the target region.",
    "input_form": "Whether the input signal encoding (text, audio, image parameters) matches deployment conditions.",
    "output_ontology": "Whether the benchmark's output categories and scoring criteria reflect regionally valid decision boundaries.",
    "output_content": "Whether ground-truth labels align with the judgments of regional stakeholders.",
    "output_form": "Whether the expected output modality matches regional deployment needs and accessibility.",
}

SCORE_LABELS = {
    1: "Serious concern", 2: "Significant gaps", 3: "Moderate gaps",
    4: "Minor gaps", 5: "Strong alignment",
}

CHECKLIST_DEFINITIONS = {
    "IO": [
        ("IO-1", "Identify test case categories required for regional deployment"),
        ("IO-2", "Check if taxonomy omits regionally relevant categories"),
        ("IO-3", "Check if taxonomy includes irrelevant categories"),
        ("IO-4", "Document category gaps harming content validity"),
    ],
    "IC": [
        ("IC-1", "Do inputs require region-specific cultural/geographic/dialectal knowledge?"),
        ("IC-2", "Does culturally sensitive content align with target culture?"),
        ("IC-3", "Flag inputs assuming Western-specific knowledge"),
        ("IC-4", "Regional annotator recruitment for culturally sensitive instances"),
        ("IC-5", "Document content issues harming content validity"),
    ],
    "IF": [
        ("IF-1", "Compare signal distributions between source and target"),
        ("IF-2", "Check if regional infrastructure supports data capture specs"),
        ("IF-3", "Identify domain-specific form differences"),
        ("IF-4", "Document form mismatches harming external validity"),
    ],
    "OO": [
        ("OO-1", "Review output label categories for regional relevance"),
        ("OO-2", "Identify missing regionally specific categories"),
        ("OO-3", "Flag categories encoding non-regional values"),
        ("OO-4", "Consider stakeholder-driven taxonomy redesign"),
        ("OO-5", "Document taxonomy issues harming structural/content validity"),
    ],
    "OC": [
        ("OC-1", "Do ground-truth labels reflect regional stakeholder perspectives?"),
        ("OC-2", "Assess potential annotator-regional population disagreement"),
        ("OC-3", "Review annotator demographics from documentation"),
        ("OC-4", "Consider label re-annotation by regional annotators"),
        ("OC-5", "Review aggregation methods for minority perspective erasure"),
        ("OC-6", "Document label issues harming convergent/external validity"),
    ],
    "OF": [
        ("OF-1", "Does output modality match regional deployment needs?"),
        ("OF-2", "Assess text-to-speech availability for speech output"),
        ("OF-3", "Consider literacy rates and accessibility requirements"),
        ("OF-4", "Document form mismatches harming external validity"),
    ],
}

# === Font Registration ===

FONT_PATHS = [
    "/usr/share/fonts/truetype/freefont",  # Linux / Docker
    "/usr/local/share/fonts/freefont",
]

NOTO_FONT_DIR = "/usr/share/fonts/truetype/noto"

# === Unicode block → Noto font name for non-Latin script rendering ===
_SCRIPT_RANGES = [
    (0x0900, 0x097F, "NotoSansDevanagari"),
    (0x0980, 0x09FF, "NotoSansBengali"),
    (0x0A00, 0x0A7F, "NotoSansGurmukhi"),
    (0x0A80, 0x0AFF, "NotoSansGujarati"),
    (0x0B00, 0x0B7F, "NotoSansOriya"),
    (0x0B80, 0x0BFF, "NotoSansTamil"),
    (0x0C00, 0x0C7F, "NotoSansTelugu"),
    (0x0C80, 0x0CFF, "NotoSansKannada"),
    (0x0D00, 0x0D7F, "NotoSansMalayalam"),
    (0x0D80, 0x0DFF, "NotoSansSinhala"),
    (0x0600, 0x06FF, "NotoSansArabic"),
    (0x0590, 0x05FF, "NotoSansHebrew"),
    (0x0E00, 0x0E7F, "NotoSansThai"),
    (0x1000, 0x109F, "NotoSansMyanmar"),
    (0x0E80, 0x0EFF, "NotoSansLao"),
    (0x1780, 0x17FF, "NotoSansKhmer"),
    (0x1200, 0x137F, "NotoSansEthiopic"),
    (0x1380, 0x139F, "NotoSansEthiopic"),
    (0x2D80, 0x2DDF, "NotoSansEthiopic"),
    (0xAB00, 0xAB2F, "NotoSansEthiopic"),
    (0x3040, 0x309F, "NotoSansJP"),   # Hiragana
    (0x30A0, 0x30FF, "NotoSansJP"),   # Katakana
    (0x4E00, 0x9FFF, "NotoSansJP"),   # CJK Unified Ideographs
    (0x3400, 0x4DBF, "NotoSansJP"),   # CJK Extension A
    (0x3000, 0x303F, "NotoSansJP"),   # CJK Symbols and Punctuation
    (0xFF00, 0xFFEF, "NotoSansJP"),   # Fullwidth Forms
]

_noto_registered = set()


def _register_noto_fonts():
    noto_dir = Path(NOTO_FONT_DIR)
    if not noto_dir.exists():
        return
    needed = {stem for _, _, stem in _SCRIPT_RANGES}
    for stem in sorted(needed):
        regular = noto_dir / f"{stem}-Regular.ttf"
        if not regular.exists():
            continue
        try:
            pdfmetrics.registerFont(TTFont(stem, str(regular)))
            # Map all style variants to Regular so <b>/<i> inside Noto
            # spans don't crash — most script fonts only ship Regular
            pdfmetrics.registerFontFamily(
                stem, normal=stem, bold=stem, italic=stem, boldItalic=stem,
            )
            _noto_registered.add(stem)
        except Exception:
            pass


def _register_fonts():
    for base in FONT_PATHS:
        regular = Path(base) / "FreeSans.ttf"
        bold = Path(base) / "FreeSansBold.ttf"
        oblique = Path(base) / "FreeSansOblique.ttf"
        bold_oblique = Path(base) / "FreeSansBoldOblique.ttf"
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont("FreeSans", str(regular)))
            pdfmetrics.registerFont(TTFont("FreeSansBold", str(bold)))
            if oblique.exists():
                pdfmetrics.registerFont(TTFont("FreeSansOblique", str(oblique)))
            if bold_oblique.exists():
                pdfmetrics.registerFont(TTFont("FreeSansBoldOblique", str(bold_oblique)))
            pdfmetrics.registerFontFamily(
                "FreeSans",
                normal="FreeSans",
                bold="FreeSansBold",
                italic="FreeSansOblique",
                boldItalic="FreeSansBoldOblique",
            )
            _register_noto_fonts()
            return
    print(
        "WARNING: FreeSans fonts not found. PDF generation will use Helvetica "
        "(no Devanagari/non-Latin support).",
        file=sys.stderr,
    )
    global FONT_REGULAR, FONT_BOLD
    FONT_REGULAR = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"


FONT_REGULAR = "FreeSans"
FONT_BOLD = "FreeSansBold"

# === Colors ===

DARK = HexColor("#1a1a2e")
ACCENT = HexColor("#2d6a9f")
SCORE_BG = HexColor("#fef3c7")
EVIDENCE_BG = HexColor("#f0f4f8")
HEADER_BG = HexColor("#e8eef4")
WHITE = HexColor("#ffffff")
GRAY_BORDER = HexColor("#cbd5e1")
RED_TEXT = HexColor("#b91c1c")
LIGHT_GRAY = HexColor("#f8fafc")

# === Styles ===


def _build_styles():
    styles = getSampleStyleSheet()
    add = styles.add

    add(ParagraphStyle(
        "DimTitle", fontName=FONT_BOLD, fontSize=16, textColor=DARK,
        spaceAfter=4, spaceBefore=0,
    ))
    add(ParagraphStyle(
        "ScoreLine", fontName=FONT_BOLD, fontSize=12, textColor=ACCENT,
        spaceAfter=8,
    ))
    add(ParagraphStyle(
        "SectionHead", fontName=FONT_BOLD, fontSize=11, textColor=ACCENT,
        spaceBefore=14, spaceAfter=6,
    ))
    add(ParagraphStyle(
        "SubHead", fontName=FONT_BOLD, fontSize=10, textColor=DARK,
        spaceBefore=10, spaceAfter=4,
    ))
    add(ParagraphStyle(
        "Body", fontName=FONT_REGULAR, fontSize=9, textColor=DARK,
        leading=13, spaceAfter=4,
    ))
    add(ParagraphStyle(
        "BodyBold", fontName=FONT_BOLD, fontSize=9, textColor=DARK,
        leading=13, spaceAfter=4,
    ))
    add(ParagraphStyle(
        "BulletItem", fontName=FONT_REGULAR, fontSize=9, textColor=DARK,
        leading=13, spaceAfter=3, leftIndent=18, bulletIndent=6,
        bulletFontName=FONT_REGULAR, bulletFontSize=9,
    ))
    add(ParagraphStyle(
        "EvidenceCell", fontName=FONT_REGULAR, fontSize=7.5, textColor=DARK,
        leading=10,
    ))
    add(ParagraphStyle(
        "EvidenceID", fontName=FONT_BOLD, fontSize=7.5, textColor=ACCENT,
        leading=10,
    ))
    add(ParagraphStyle(
        "GapText", fontName=FONT_REGULAR, fontSize=8.5,
        textColor=HexColor("#4a5568"), leading=12, spaceAfter=2,
        leftIndent=18, bulletIndent=6,
        bulletFontName=FONT_REGULAR, bulletFontSize=8.5,
    ))
    add(ParagraphStyle(
        "RemedGap", fontName=FONT_BOLD, fontSize=9, textColor=RED_TEXT,
        leading=12, spaceAfter=2, leftIndent=12,
    ))
    add(ParagraphStyle(
        "RemedRec", fontName=FONT_REGULAR, fontSize=9, textColor=DARK,
        leading=12, spaceAfter=8, leftIndent=12,
    ))
    add(ParagraphStyle(
        "ChecklistDef", fontName=FONT_REGULAR, fontSize=8,
        textColor=HexColor("#4a5568"), leading=11,
    ))
    add(ParagraphStyle(
        "SummaryTitle", fontName=FONT_BOLD, fontSize=18, textColor=DARK,
        spaceAfter=6, spaceBefore=0,
    ))
    add(ParagraphStyle(
        "SummarySubtitle", fontName=FONT_BOLD, fontSize=11,
        textColor=HexColor("#4a5568"), spaceAfter=4,
    ))
    add(ParagraphStyle(
        "ScoreTableCell", fontName=FONT_REGULAR, fontSize=9, textColor=DARK,
        leading=12,
    ))
    add(ParagraphStyle(
        "ScoreTableBold", fontName=FONT_BOLD, fontSize=9, textColor=DARK,
        leading=12,
    ))
    return styles


# === XML Escaping ===

def escape(text):
    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


# === Registry Parsing ===

def parse_quote_registry(composed_text):
    """Parse Verbatim Quote Registry table from composed_prompt.md."""
    registry = {}
    in_table = False
    for line in composed_text.splitlines():
        if "Verbatim Quote Registry" in line and line.lstrip().startswith("#"):
            in_table = True
            continue
        if in_table and line.startswith("|"):
            if "---" in line:
                continue
            cols = [c.strip() for c in line.split("|")]
            cols = [c for c in cols if c]
            if len(cols) >= 4 and cols[0].startswith("Q") and cols[0][1:].isdigit():
                qid = cols[0]
                page = cols[1]
                text = cols[3] if len(cols) >= 4 else ""
                if text.startswith('"') and text.endswith('"'):
                    text = text[1:-1]
                registry[qid] = {"text": text, "page": page}
        elif in_table and line.strip() and not line.startswith("|"):
            if re.match(r"^#{1,4}\s+", line):
                break
    return registry


def parse_web_registry(composed_text):
    """Parse Web Source Registry table from composed_prompt.md (ID -> URL)."""
    registry = {}
    in_table = False
    for line in composed_text.splitlines():
        if "Web Source Registry" in line and line.lstrip().startswith("#"):
            in_table = True
            continue
        if in_table and line.startswith("|"):
            if "---" in line:
                continue
            cols = [c.strip() for c in line.split("|")]
            cols = [c for c in cols if c]
            if len(cols) >= 2 and cols[0].startswith("WEB-"):
                registry[cols[0]] = {"url": cols[1], "desc": ""}
        elif in_table and line.strip() and not line.startswith("|"):
            if re.match(r"^#{1,4}\s+", line):
                break
    return registry


def parse_web_descriptions(scoring):
    """Extract web source descriptions from scoring.json evidence_web_sources fields.

    Entries look like: "[WEB-9] UPSC Current Affairs ranges 0-27 questions..."
    Returns {WEB-9: "UPSC Current Affairs ranges..."}.
    """
    descs = {}
    for dim_data in scoring.get("dimensions", {}).values():
        for entry in dim_data.get("evidence_web_sources", []):
            m = re.match(r"\[(WEB-\d+)\]\s*(.*)", entry)
            if m:
                descs[m.group(1)] = m.group(2).strip()
    return descs


def merge_web_registries(url_registry, descriptions):
    """Merge URL registry (from composed_prompt) with descriptions (from scoring)."""
    merged = dict(url_registry)
    for wid, desc in descriptions.items():
        if wid in merged:
            merged[wid]["desc"] = desc
        else:
            merged[wid] = {"url": "", "desc": desc}
    return merged


def parse_dataset_registry(report_text):
    """Parse dataset citation registry from dataset_analysis_report.md.

    Handles two formats:
    - Table format (single-dataset, e.g. MILU): | D1 | Dataset | # | Label | Excerpt | Interp | Dim |
    - Bullet format (org-mode, e.g. DrBenchmark): - **PREFIX-D1**: dataset | # | label | "excerpt" | interp | dim
    """
    if not report_text:
        return {}

    registry = {}

    # === Try table format first ===
    in_table = False
    for line in report_text.splitlines():
        if "Datapoint Citations Registry" in line or "Cited Datapoints" in line:
            in_table = True
            continue
        if in_table and line.startswith("|"):
            if "---" in line:
                continue
            cols = [c.strip() for c in line.split("|")]
            cols = [c for c in cols if c]
            if len(cols) >= 6 and re.match(r"D\d+$", cols[0]):
                did = cols[0]
                excerpt = cols[4] if len(cols) >= 5 else ""
                interp = cols[5] if len(cols) >= 6 else ""
                if excerpt.startswith('"') and excerpt.endswith('"'):
                    excerpt = excerpt[1:-1]
                registry[did] = {"excerpt": excerpt, "interp": interp}
        elif in_table and line.strip() and not line.startswith("|"):
            if re.match(r"^#{1,4}\s+", line):
                break

    if registry:
        return registry

    # === Try bullet format (org-mode, dynamically-prefixed IDs) ===
    for line in report_text.splitlines():
        m = re.match(
            r"-\s+\*\*([A-Za-z][A-Za-z0-9_]*-D\d+)\*\*:\s*(.*)", line
        )
        if m:
            cid = m.group(1)
            rest = m.group(2)
            parts = [p.strip() for p in rest.split("|")]
            excerpt = ""
            interp = ""
            if len(parts) >= 4:
                raw_excerpt = parts[3]
                if raw_excerpt.startswith('"') and raw_excerpt.endswith('"'):
                    raw_excerpt = raw_excerpt[1:-1]
                excerpt = raw_excerpt
            if len(parts) >= 5:
                interp = parts[4]
            registry[cid] = {"excerpt": excerpt, "interp": interp}

    return registry


def parse_limitations(report_text):
    """Parse Limitations section from dataset_analysis_report.md."""
    if not report_text:
        return {}
    registry = {}
    in_section = False
    lim_num = 0
    for line in report_text.splitlines():
        if re.match(r"^#{1,4}\s+Limitations?\b", line):
            in_section = True
            continue
        if in_section:
            if re.match(r"^#{1,4}\s+", line):
                break
            m = re.match(r"^\d+\.\s+(.*)", line.strip())
            if m:
                lim_num += 1
                registry[f"Limitation #{lim_num}"] = m.group(1).strip()
            elif line.strip().startswith("- "):
                lim_num += 1
                registry[f"Limitation #{lim_num}"] = line.strip()[2:].strip()
    return registry


def parse_critical_concerns(report_text):
    """Parse CRITICAL Concern entries from dataset_analysis_report.md."""
    if not report_text:
        return {}
    registry = {}
    current_id = None
    for line in report_text.splitlines():
        m = re.match(r"^#{1,5}\s+CRITICAL Concern\s+(\d+)", line)
        if m:
            current_id = f"CRITICAL Concern {m.group(1)}"
            continue
        if current_id and "**Observation:**" in line:
            obs = line.split("**Observation:**", 1)[1].strip()
            registry[current_id] = obs
            current_id = None
    return registry


def load_registries(tuple_dir, scoring):
    """Load all evidence registries for a single assessment tuple."""
    composed_path = tuple_dir / "composed_prompt.md"
    da_path = tuple_dir / "dataset_analysis_report.md"

    composed_text = composed_path.read_text(encoding="utf-8") if composed_path.exists() else ""
    da_text = da_path.read_text(encoding="utf-8") if da_path.exists() else ""

    quote_reg = parse_quote_registry(composed_text)
    web_urls = parse_web_registry(composed_text)
    web_descs = parse_web_descriptions(scoring)
    web_reg = merge_web_registries(web_urls, web_descs)
    dataset_reg = parse_dataset_registry(da_text)
    limitation_reg = parse_limitations(da_text)
    critical_reg = parse_critical_concerns(da_text)

    return {
        "quote": quote_reg,
        "web": web_reg,
        "dataset": dataset_reg,
        "limitation": limitation_reg,
        "critical": critical_reg,
    }


# === Citation Extraction ===

def normalize_citations(text):
    """Convert parenthetical citations to bracket form and slashes to commas.

    Clean parenthetical patterns:
      (DATASET-D14/D15/D29) → [DATASET-D14, D15, D29]
      (DATASET-D13)         → [DATASET-D13]
      (DATASET-D1, D2, D3)  → [DATASET-D1, D2, D3]
      (elicitation Q2)      → [elicitation Q2]

    Slash-separated DATASET refs inside brackets:
      [DATASET-D14/D15/D29] → [DATASET-D14, D15, D29]
    """
    def _slash_to_comma(m):
        parts = m.group(1).split("/")
        return "[" + ", ".join(parts) + "]"

    # Slash-separated in parens or brackets
    text = re.sub(r"\(DATASET-(D\d+(?:/D?\d+)+)\)", _slash_to_comma, text)
    text = re.sub(r"\[DATASET-(D\d+(?:/D?\d+)+)\]", _slash_to_comma, text)

    # Parenthetical DATASET refs
    text = re.sub(
        r"\(DATASET-(D\d+(?:,\s*D\d+)*)\)", r"[DATASET-\1]", text)

    # Parenthetical plain D refs (only when all items are D-refs)
    text = re.sub(r"\((D\d+(?:,\s*D\d+)+)\)", r"[\1]", text)

    # Parenthetical elicitation refs
    text = re.sub(r"\((elicitation\s+Q\d+)\)", r"[\1]", text)

    return text


def colorize_citations(escaped_text):
    """Wrap citation references in blue font tags for PDF rendering.

    Colors any bracket group [...] that contains at least one citation token.
    """
    color = "#2d6a9f"

    def _blue_if_citation(m):
        inner = m.group(0)
        if re.search(r"Q\d+|WEB-\d+|D\d+|Limitation #\d+|CRITICAL Concern \d+",
                      inner):
            return f'<font color="{color}">{inner}</font>'
        return inner

    escaped_text = re.sub(r"\[[^\]]+\]", _blue_if_citation, escaped_text)

    # Standalone citation tokens outside brackets (e.g. "only DATASET-D3 on")
    def _blue_if_not_wrapped(m):
        pre = escaped_text[:m.start()]
        if pre.count("<font") > pre.count("</font>"):
            return m.group(0)
        return f'<font color="{color}">{m.group(0)}</font>'

    escaped_text = re.sub(r"DATASET-D\d+", _blue_if_not_wrapped, escaped_text)
    return escaped_text


def _char_to_noto_font(ch):
    cp = ord(ch)
    for start, end, font in _SCRIPT_RANGES:
        if start <= cp <= end and font in _noto_registered:
            return font
    return None


def wrap_scripts(text):
    """Wrap non-Latin characters in <font face="NotoSansXXX"> tags.

    Scans character-by-character, skipping XML tags and entities, grouping
    consecutive same-script characters into single font spans.
    """
    if not _noto_registered:
        return text

    result = []
    i = 0
    n = len(text)
    cur_font = None
    cur_run = []

    def _flush():
        nonlocal cur_font, cur_run
        if cur_font and cur_run:
            result.append(
                f'<font face="{cur_font}">{"".join(cur_run)}</font>')
            cur_run = []
            cur_font = None

    while i < n:
        ch = text[i]

        if ch == '<':
            _flush()
            end = text.find('>', i)
            if end == -1:
                result.append(text[i:])
                break
            result.append(text[i:end + 1])
            i = end + 1
            continue

        if ch == '&':
            _flush()
            end = text.find(';', i)
            if end != -1 and end - i < 10:
                result.append(text[i:end + 1])
                i = end + 1
            else:
                result.append(ch)
                i += 1
            continue

        font = _char_to_noto_font(ch)

        if font is None:
            _flush()
            result.append(ch)
        elif font == cur_font:
            cur_run.append(ch)
        else:
            _flush()
            cur_font = font
            cur_run = [ch]

        i += 1

    _flush()
    return "".join(result)


def render_text(text):
    """Normalize citations, escape XML, colorize, wrap non-Latin scripts."""
    return wrap_scripts(colorize_citations(escape(normalize_citations(text))))


def extract_citation_ids(text):
    """Extract citation IDs using token-level scanning.

    Finds Q, WEB, D, and DATASET-D tokens anywhere in the text regardless
    of surrounding delimiters (brackets, parens, explanatory text). Handles
    ranges like Q60–Q66 and D40–D42.
    """
    text = normalize_citations(text)

    ids = []
    seen = set()

    def _add(cid):
        if cid not in seen:
            seen.add(cid)
            ids.append(cid)

    # === Q ranges first (Q60–Q66, Q43-Q45) — expand before individual scan ===
    for m in re.finditer(r"Q(\d+)[–\-]Q(\d+)", text):
        for i in range(int(m.group(1)), int(m.group(2)) + 1):
            _add(f"Q{i}")

    # === Individual Q refs (word-boundary guard to skip e.g. "FAQ1") ===
    for m in re.finditer(r"(?<![A-Za-z])(Q\d+)", text):
        _add(m.group(1))

    # === WEB- refs ===
    for m in re.finditer(r"(WEB-\d+)", text):
        _add(m.group(1))

    # === DATASET-D refs (extract the D-number) ===
    for m in re.finditer(r"DATASET-(D\d+)", text):
        _add(m.group(1))

    # === D ranges (D40–D42, D1-D22) ===
    for m in re.finditer(r"(?<![A-Za-z])D(\d+)[–\-]D?(\d+)", text):
        for i in range(int(m.group(1)), int(m.group(2)) + 1):
            _add(f"D{i}")

    # === Standalone D refs (not part of DATASET- or other word) ===
    for m in re.finditer(r"(?<![A-Za-z\-])(D\d+)", text):
        _add(m.group(1))

    # === Org-mode prefixed (QUAERO-D1, DIAMED-D9, but not DATASET-D) ===
    for m in re.finditer(r"([A-Za-z][A-Za-z0-9_]*-D\d+)", text):
        if not m.group(1).startswith("DATASET"):
            _add(m.group(1))

    # === Limitation / CRITICAL Concern (still require brackets) ===
    for m in re.finditer(r"\[Limitation #(\d+)\]", text):
        _add(f"Limitation #{m.group(1)}")
    for m in re.finditer(r"\[CRITICAL Concern (\d+)\]", text):
        _add(f"CRITICAL Concern {m.group(1)}")

    return ids


# === Evidence Lookup & Table ===

def lookup_evidence(citation_ids, registries):
    """Look up evidence entries for a list of citation IDs.

    Returns list of (type, id, text1, text2) tuples.
    """
    entries = []
    seen = set()
    for cid in citation_ids:
        if cid in seen:
            continue
        seen.add(cid)

        if cid.startswith("Q") and cid[1:].isdigit():
            e = registries["quote"].get(cid)
            if e:
                entries.append(("quote", cid, e["text"], f"p.{e['page']}"))
        elif cid.startswith("WEB-"):
            e = registries["web"].get(cid)
            if e:
                desc = e.get("desc", "")
                url = e.get("url", "")
                display = desc if desc else url
                entries.append(("web", cid, display, url if desc else ""))
        elif cid.startswith("Limitation"):
            e = registries["limitation"].get(cid)
            if e:
                entries.append(("limitation", cid, e, ""))
        elif cid.startswith("CRITICAL Concern"):
            e = registries["critical"].get(cid)
            if e:
                entries.append(("critical", cid, e, ""))
        elif re.match(r"D\d+$", cid):
            e = registries["dataset"].get(cid)
            if e:
                entries.append(("dataset", cid, e["excerpt"], e["interp"]))
        elif re.match(r"[A-Za-z][A-Za-z0-9_]*-D\d+$", cid):
            e = registries["dataset"].get(cid)
            if e:
                entries.append(("dataset", cid, e["excerpt"], e["interp"]))
        else:
            pass

    # === Sort by type group then numeric ID ===
    type_order = {"quote": 0, "dataset": 1, "web": 2, "limitation": 3, "critical": 4}
    def _sort_key(entry):
        etype, eid = entry[0], entry[1]
        m = re.search(r"(\d+)$", eid)
        num = int(m.group(1)) if m else 0
        return (type_order.get(etype, 99), num)
    entries.sort(key=_sort_key)

    return entries


def make_evidence_table(entries, available_width, styles):
    """Create a formatted evidence table from lookup entries."""
    if not entries:
        return None

    id_col_width = 0.85 * inch
    evidence_col_width = available_width - id_col_width - 0.1 * inch

    rows = [
        [
            Paragraph("<b>ID</b>", styles["EvidenceID"]),
            Paragraph("<b>Evidence</b>", styles["EvidenceCell"]),
        ]
    ]

    for etype, eid, text1, text2 in entries:
        eid_p = Paragraph(f"<b>{escape(eid)}</b>", styles["EvidenceID"])
        e1 = wrap_scripts(escape(text1))
        e2 = wrap_scripts(escape(text2)) if text2 else ""
        if etype == "quote":
            content = f"“{e1}” ({e2})"
        elif etype == "web":
            content = f"{e1} ({e2})" if text2 else e1
        elif etype == "dataset":
            content = f"{e1} — {e2}"
        elif etype in ("limitation", "critical"):
            content = e1
        else:
            content = e1
        rows.append([eid_p, Paragraph(content, styles["EvidenceCell"])])

    t = Table(rows, colWidths=[id_col_width, evidence_col_width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("BACKGROUND", (0, 1), (-1, -1), EVIDENCE_BG),
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def _add_inline_evidence(story, text, registries, content_width, styles,
                         indent=0):
    """Extract citations from text and append an evidence table to story."""
    cids = extract_citation_ids(text)
    entries = lookup_evidence(cids, registries)
    tbl = make_evidence_table(entries, content_width - indent, styles)
    if tbl:
        if indent > 0:
            wrapper = Table([[tbl]], colWidths=[content_width - indent])
            wrapper.setStyle(TableStyle([
                ("LEFTPADDING", (0, 0), (-1, -1), indent),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(wrapper)
        else:
            story.append(tbl)
            story.append(Spacer(1, 6))


def _add_inline_evidence_from_ids(story, citation_ids, registries,
                                  content_width, styles, indent=0):
    """Like _add_inline_evidence but from pre-extracted citation IDs."""
    entries = lookup_evidence(citation_ids, registries)
    tbl = make_evidence_table(entries, content_width - indent, styles)
    if tbl:
        if indent > 0:
            wrapper = Table([[tbl]], colWidths=[content_width - indent])
            wrapper.setStyle(TableStyle([
                ("LEFTPADDING", (0, 0), (-1, -1), indent),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(wrapper)
        else:
            story.append(tbl)
            story.append(Spacer(1, 6))


# === Dimension PDF Builder ===

def build_dimension_pdf(dim_key, scoring, registries, output_path, styles):
    """Build a single dimension PDF with inline evidence tables."""
    dim_data = scoring["dimensions"][dim_key]
    benchmark = scoring.get("benchmark", "unknown").upper()
    region = scoring.get("region", "unknown")
    label = DIM_LABELS[dim_key]
    abbrev = DIM_ABBREVS[dim_key]
    score = dim_data.get("score", "N/A")
    confidence = dim_data.get("confidence", "N/A")
    rating = SCORE_LABELS.get(int(score), "") if isinstance(score, (int, float)) else ""

    doc = SimpleDocTemplate(
        str(output_path), pagesize=letter,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
    )
    content_width = letter[0] - 1.5 * inch
    story = []

    # === Header ===
    story.append(Paragraph(f"{label} ({abbrev})", styles["DimTitle"]))
    story.append(Paragraph(
        f"Score: {score}/5 — {rating} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"Confidence: {confidence}",
        styles["ScoreLine"],
    ))
    story.append(Paragraph(
        f"<i><b>Benchmark:</b> {escape(benchmark)} &nbsp;|&nbsp; "
        f"<b>Context:</b> {escape(region)}</i>",
        styles["Body"],
    ))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(
        width="100%", thickness=1.5, color=ACCENT,
        spaceAfter=10, spaceBefore=2,
    ))

    # === Definition ===
    story.append(Paragraph(
        f"<b>{escape(label)} definition:</b> {escape(DIM_DEFINITIONS[dim_key])}",
        styles["Body"],
    ))
    story.append(Spacer(1, 4))

    # === Evidence preamble ===
    story.append(Paragraph(
        "Each section below is followed by an evidence table. Three types of "
        "evidence are cited: "
        "<b>[QN]</b> — verbatim quotes extracted from the benchmark paper; "
        "<b>[WEB-N]</b> — web sources consulted during assessment; "
        "<b>[DN]</b> / <b>[DATASET-DN]</b> — sampled datapoints from the "
        "benchmark dataset, with an interpretation note.",
        styles["GapText"],
    ))
    story.append(Spacer(1, 4))

    # === Justification ===
    justification = dim_data.get("justification", "")
    if justification:
        story.append(Paragraph("Justification", styles["SectionHead"]))
        story.append(Paragraph(render_text(justification), styles["Body"]))
        story.append(Spacer(1, 4))
        _add_inline_evidence(story, justification, registries, content_width,
                             styles)

    # === Strengths ===
    strengths = dim_data.get("strengths", [])
    if strengths:
        story.append(Paragraph("Strengths", styles["SectionHead"]))
        all_strength_ids = []
        for s in strengths:
            story.append(
                Paragraph(f"• {render_text(s)}", styles["BulletItem"])
            )
            all_strength_ids.extend(extract_citation_ids(s))
        all_strength_ids = list(dict.fromkeys(all_strength_ids))
        _add_inline_evidence_from_ids(
            story, all_strength_ids, registries, content_width, styles,
        )

    # === Checklist ===
    checklist = dim_data.get("checklist_responses", {})
    if checklist:
        story.append(Paragraph("Checklist", styles["SectionHead"]))

        # Definitions table
        defs = CHECKLIST_DEFINITIONS.get(abbrev, [])
        if defs:
            story.append(
                Paragraph("Checklist item definitions:", styles["SubHead"])
            )
            def_rows = [
                [
                    Paragraph("<b>ID</b>", styles["EvidenceID"]),
                    Paragraph(
                        "<b>Assessment Question</b>",
                        styles["ChecklistDef"],
                    ),
                ]
            ]
            for cid, cdef in defs:
                def_rows.append([
                    Paragraph(f"<b>{cid}</b>", styles["EvidenceID"]),
                    Paragraph(escape(cdef), styles["ChecklistDef"]),
                ])
            def_table = Table(
                def_rows,
                colWidths=[0.5 * inch, content_width - 0.6 * inch],
            )
            def_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GRAY),
                ("GRID", (0, 0), (-1, -1), 0.5, GRAY_BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(def_table)
            story.append(Spacer(1, 10))

        # Responses with consolidated evidence table
        story.append(
            Paragraph("Checklist responses:", styles["SubHead"])
        )
        evidence_map = dim_data.get("evidence_map", {})
        all_checklist_ids = []
        for item_id, response in checklist.items():
            story.append(Paragraph(
                f"<b>{escape(item_id)}</b>: {render_text(response)}",
                styles["Body"],
            ))
            map_ids = evidence_map.get(item_id, [])
            text_ids = extract_citation_ids(response)
            all_checklist_ids.extend(map_ids + text_ids)
        all_checklist_ids = list(dict.fromkeys(all_checklist_ids))
        _add_inline_evidence_from_ids(
            story, all_checklist_ids, registries, content_width, styles,
        )

    # === Information Gaps ===
    gaps = dim_data.get("information_gaps", [])
    if gaps:
        story.append(Paragraph("Information Gaps", styles["SectionHead"]))
        for gap in gaps:
            story.append(
                Paragraph(f"• {render_text(gap)}", styles["GapText"])
            )
        story.append(Spacer(1, 4))

    # === Requires Expert Verification ===
    expert_items = dim_data.get("requires_expert_verification", [])
    if expert_items:
        story.append(
            Paragraph("Requires Expert Verification", styles["SectionHead"])
        )
        for item in expert_items:
            story.append(
                Paragraph(f"• {render_text(item)}", styles["GapText"])
            )
        story.append(Spacer(1, 4))

    # === Remediation ===
    remediation_items = [
        r for r in scoring.get("remediation_suggestions", [])
        if isinstance(r, dict) and r.get("dimension") == dim_key
    ]
    if remediation_items:
        story.append(HRFlowable(
            width="100%", thickness=0.75, color=GRAY_BORDER,
            spaceAfter=6, spaceBefore=8,
        ))
        story.append(Paragraph("Remediation", styles["SectionHead"]))
        all_remed_ids = []
        for i, rem in enumerate(remediation_items, 1):
            gap = rem.get("gap", "")
            rec = rem.get("recommendation", "")
            story.append(Paragraph(
                f"<b>Gap {i}:</b> {render_text(gap)}",
                styles["RemedGap"],
            ))
            story.append(Paragraph(
                f"<b>Recommendation:</b> {render_text(rec)}",
                styles["RemedRec"],
            ))
            all_remed_ids.extend(extract_citation_ids(gap))
            all_remed_ids.extend(extract_citation_ids(rec))
        all_remed_ids = list(dict.fromkeys(all_remed_ids))
        _add_inline_evidence_from_ids(
            story, all_remed_ids, registries, content_width, styles,
        )

    doc.build(story)


# === Summary PDF Builder ===

def build_summary_pdf(scoring, deployment_text, output_path, styles,
                      registries=None):
    """Build the summary PDF: deployment context, scores, guidance."""
    benchmark = scoring.get("benchmark", "unknown")
    region = scoring.get("region", "unknown")
    risk = scoring.get("risk_assessment", "N/A").upper()

    doc = SimpleDocTemplate(
        str(output_path), pagesize=letter,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
    )
    content_width = letter[0] - 1.5 * inch
    story = []

    # === Title ===
    story.append(Paragraph(
        f"Validity Analysis: {escape(benchmark.upper())}",
        styles["SummaryTitle"],
    ))
    story.append(Paragraph(
        f"Target context: {escape(region)}",
        styles["SummarySubtitle"],
    ))
    story.append(Paragraph(
        f"Overall risk: <b>{escape(risk)}</b>",
        styles["Body"],
    ))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(
        width="100%", thickness=1.5, color=ACCENT,
        spaceAfter=12, spaceBefore=2,
    ))

    # === Deployment Context ===
    if deployment_text:
        story.append(Paragraph("Deployment Context", styles["SectionHead"]))
        for line in deployment_text.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            low = line.lower()
            if low.startswith("use case and domain:"):
                story.append(Paragraph(
                    f"<b>Use case:</b> {escape(line.split(':', 1)[1].strip())}",
                    styles["Body"],
                ))
            elif low.startswith("target population:"):
                story.append(Paragraph(
                    f"<b>Target population:</b> {escape(line.split(':', 1)[1].strip())}",
                    styles["Body"],
                ))
            else:
                story.append(Paragraph(escape(line), styles["Body"]))
        story.append(Spacer(1, 8))

    # === Scores Table ===
    story.append(Paragraph("Dimension Scores", styles["SectionHead"]))
    dims = scoring.get("dimensions", {})
    highest = scoring.get("highest_concern_dimensions", [])
    strongest = scoring.get("strongest_dimensions", [])

    header = [
        Paragraph("<b>Dimension</b>", styles["ScoreTableBold"]),
        Paragraph("<b>Score</b>", styles["ScoreTableBold"]),
        Paragraph("<b>Rating</b>", styles["ScoreTableBold"]),
        Paragraph("<b>Confidence</b>", styles["ScoreTableBold"]),
    ]
    rows = [header]
    total, count = 0, 0

    for key, label in DIM_LABELS.items():
        dd = dims.get(key, {})
        sc = dd.get("score", "N/A")
        conf = dd.get("confidence", "N/A")
        rating = SCORE_LABELS.get(int(sc), "") if isinstance(sc, (int, float)) else ""
        flag = ""
        if key in highest:
            flag = " ⚠"
        elif key in strongest:
            flag = " ✓"
        rows.append([
            Paragraph(f"{escape(label)}{flag}", styles["ScoreTableCell"]),
            Paragraph(str(sc), styles["ScoreTableCell"]),
            Paragraph(rating, styles["ScoreTableCell"]),
            Paragraph(str(conf), styles["ScoreTableCell"]),
        ])
        if isinstance(sc, (int, float)):
            total += sc
            count += 1

    if count > 0:
        rows.append([
            Paragraph("<b>Average</b>", styles["ScoreTableBold"]),
            Paragraph(f"<b>{total / count:.1f}</b>", styles["ScoreTableBold"]),
            Paragraph("", styles["ScoreTableCell"]),
            Paragraph("", styles["ScoreTableCell"]),
        ])

    col_widths = [
        content_width * 0.35,
        content_width * 0.12,
        content_width * 0.30,
        content_width * 0.23,
    ]
    scores_tbl = Table(rows, colWidths=col_widths)
    scores_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(scores_tbl)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "⚠ = highest concern &nbsp;&nbsp; ✓ = strongest dimension",
        styles["GapText"],
    ))
    story.append(Spacer(1, 10))

    # === Dimension Key ===
    story.append(Paragraph("Dimension Key", styles["SectionHead"]))
    key_header = [
        Paragraph("<b>Abbr.</b>", styles["ScoreTableBold"]),
        Paragraph("<b>Dimension</b>", styles["ScoreTableBold"]),
        Paragraph("<b>Definition</b>", styles["ScoreTableBold"]),
    ]
    key_rows = [key_header]
    for key, label in DIM_LABELS.items():
        key_rows.append([
            Paragraph(DIM_ABBREVS[key], styles["ScoreTableCell"]),
            Paragraph(label, styles["ScoreTableCell"]),
            Paragraph(DIM_DEFINITIONS[key], styles["ChecklistDef"]),
        ])
    key_tbl = Table(
        key_rows,
        colWidths=[0.5 * inch, 1.2 * inch, content_width - 1.8 * inch],
    )
    key_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GRAY),
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(key_tbl)
    story.append(Spacer(1, 10))

    # === Overall Summary ===
    summary = scoring.get("overall_summary", "")
    if summary:
        story.append(Paragraph("Overall Summary", styles["SectionHead"]))
        story.append(Paragraph(render_text(summary), styles["Body"]))
        story.append(Spacer(1, 4))
        if registries:
            _add_inline_evidence(story, summary, registries, content_width,
                                 styles)
        story.append(Spacer(1, 4))

    # === Practical Guidance ===
    guidance = scoring.get("practical_guidance", {})
    if guidance:
        story.append(Paragraph("Practical Guidance", styles["SectionHead"]))
        all_guidance_ids = []

        measure = guidance.get("what_this_benchmark_measures", "")
        if measure:
            story.append(
                Paragraph("What This Benchmark Measures", styles["SubHead"])
            )
            story.append(Paragraph(render_text(measure), styles["Body"]))
            story.append(Spacer(1, 4))
            all_guidance_ids.extend(extract_citation_ids(measure))

        depth = guidance.get("construct_depth", "")
        if depth:
            story.append(
                Paragraph("Construct Depth", styles["SubHead"])
            )
            story.append(Paragraph(render_text(depth), styles["Body"]))
            story.append(Spacer(1, 4))
            all_guidance_ids.extend(extract_citation_ids(depth))

        supp = guidance.get("supplementation_needed", "")
        if supp:
            story.append(
                Paragraph("What Else You Need", styles["SubHead"])
            )
            story.append(Paragraph(render_text(supp), styles["Body"]))
            story.append(Spacer(1, 4))
            all_guidance_ids.extend(extract_citation_ids(supp))

        if registries:
            all_guidance_ids = list(dict.fromkeys(all_guidance_ids))
            _add_inline_evidence_from_ids(
                story, all_guidance_ids, registries, content_width, styles,
            )

    doc.build(story)


# === Main ===

DIM_FILE_KEYS = {
    "input_ontology": "io",
    "input_content": "ic",
    "input_form": "if",
    "output_ontology": "oo",
    "output_content": "oc",
    "output_form": "of",
}


def process_tuple(tuple_dir, styles):
    """Generate all 7 PDFs for a single assessment tuple."""
    tuple_dir = Path(tuple_dir)
    scoring_path = tuple_dir / "scoring.json"
    if not scoring_path.exists():
        print(f"  SKIP {tuple_dir.name}: no scoring.json")
        return 0

    scoring = json.loads(scoring_path.read_text(encoding="utf-8"))
    registries = load_registries(tuple_dir, scoring)

    deploy_path = tuple_dir / "deployment_description.txt"
    deploy_text = (
        deploy_path.read_text(encoding="utf-8") if deploy_path.exists() else ""
    )

    pdf_dir = tuple_dir / "pdfs"
    pdf_dir.mkdir(exist_ok=True)

    # Summary PDF
    build_summary_pdf(scoring, deploy_text, pdf_dir / "summary.pdf", styles,
                      registries=registries)

    # Dimension PDFs
    for dim_key, file_key in DIM_FILE_KEYS.items():
        if dim_key in scoring.get("dimensions", {}):
            build_dimension_pdf(
                dim_key, scoring, registries,
                pdf_dir / f"{file_key}.pdf", styles,
            )

    n_pdfs = 1 + sum(
        1 for dk in DIM_FILE_KEYS if dk in scoring.get("dimensions", {})
    )
    return n_pdfs


def discover_tuples(assessments_dir):
    """Find all assessment tuple directories that have scoring.json."""
    assessments_dir = Path(assessments_dir)
    tuples = []
    for expert_dir in sorted(assessments_dir.glob("expert_*")):
        if not expert_dir.is_dir():
            continue
        for slug_dir in sorted(expert_dir.iterdir()):
            if slug_dir.is_dir() and (slug_dir / "scoring.json").exists():
                tuples.append(slug_dir)
    return tuples


# === Per-expert concatenation in form ordering ===

COMPARATOR_MAP = {
    "milu_the_indicmmlu_benchmark": "mmlu",
    "milu": "mmlu",
    "drbenchmark": "blurb",
    "ltzglue": "glue",
    "mrbench": "mathdial",
    "crisisltlsum": "cnn_dailymail",
    "wximpactbench": "crisisbench",
    "arabicmmlu": "mmlu",
    "laila": "asap_pp",
    "toxigen": "civil_comments",
    "afridoc_mt_document_level_mt_corpus_for_african_languages": "flores200",
    "injongo_a_multicultural_intent_detection_and_slot_filling_dataset_for_16_african_languages": "massive",
    "hope": "swda",
    "mentalclouds": "samsum",
}
COMPARATOR_BENCHMARKS = set(COMPARATOR_MAP.values())

DIM_PDF_ORDER = ["io", "ic", "if", "oo", "oc", "of"]


def discover_experts(assessments_dir):
    """Returns {expert_id: {benchmark_slug: [tuple_dir, ...]}}."""
    assessments_dir = Path(assessments_dir)
    experts = {}
    for d in sorted(assessments_dir.glob("expert_*__*")):
        if not d.is_dir():
            continue
        parts = d.name.split("__", 1)
        if len(parts) != 2:
            continue
        eid, bench = parts
        if eid not in experts:
            experts[eid] = {}
        tuples = sorted(
            [t for t in d.iterdir() if t.is_dir() and (t / "scoring.json").exists()]
        )
        if tuples:
            experts[eid][bench] = tuples
    return experts


def concat_expert_pdfs(expert_id, benchmarks, assessments_dir, concat_dir):
    """Merge all PDFs for one expert into a single file in form order.

    Order: for each regional benchmark (sorted), for each tuple (sorted):
      summary → io → ic → if → oo → oc → of
    Then comparative PDFs for that benchmark's pairs (if any).
    """
    from pypdf import PdfWriter

    writer = PdfWriter()
    pdf_paths = []

    for bench in sorted(benchmarks):
        if bench in COMPARATOR_BENCHMARKS:
            continue

        # === Regional tuples: summary + 6 dimensions ===
        for td in benchmarks[bench]:
            pdf_dir = td / "pdfs"
            for name in ["summary"] + DIM_PDF_ORDER:
                p = pdf_dir / f"{name}.pdf"
                if p.exists():
                    pdf_paths.append(p)

        # === Comparative PDFs for this benchmark's pairs ===
        comp_slug = COMPARATOR_MAP.get(bench)
        if comp_slug and comp_slug in benchmarks:
            comp_dirs = {d.name: d for d in benchmarks[comp_slug]}
            for td in benchmarks[bench]:
                if td.name in comp_dirs:
                    p = comp_dirs[td.name] / "pdfs" / "comparative.pdf"
                    if p.exists():
                        pdf_paths.append(p)

    if not pdf_paths:
        print(f"  SKIP {expert_id}: no PDFs found")
        return

    for p in pdf_paths:
        writer.append(str(p))

    concat_dir = Path(concat_dir)
    concat_dir.mkdir(parents=True, exist_ok=True)
    out_path = concat_dir / f"{expert_id}_all.pdf"
    with open(out_path, "wb") as f:
        writer.write(f)
    print(f"  {expert_id}: {len(pdf_paths)} PDFs → {out_path}")


def main():
    p = argparse.ArgumentParser(
        description="Generate expert review PDFs for assessment tuples",
    )
    p.add_argument(
        "--assessments-dir", default="assessments",
        help="Path to assessments directory (default: assessments/)",
    )
    p.add_argument(
        "--tuple", default=None,
        help="Process a single tuple directory instead of all",
    )
    p.add_argument(
        "--concat-dir", default=None,
        help="Directory for per-expert concatenated PDFs (outside assessments/)",
    )
    args = p.parse_args()

    _register_fonts()
    styles = _build_styles()

    if args.tuple:
        td = Path(args.tuple)
        if not td.exists():
            print(f"ERROR: {td} not found", file=sys.stderr)
            sys.exit(1)
        print(f"Processing: {td}")
        n = process_tuple(td, styles)
        print(f"  Generated {n} PDFs in {td / 'pdfs'}")
    else:
        tuples = discover_tuples(args.assessments_dir)
        if not tuples:
            print(f"No tuples with scoring.json found in {args.assessments_dir}")
            sys.exit(1)
        print(f"Found {len(tuples)} assessment tuples")
        total = 0
        for td in tqdm(tuples, desc="Generating PDFs"):
            n = process_tuple(td, styles)
            total += n
        print(f"Done: {total} PDFs generated across {len(tuples)} tuples")

    if args.concat_dir:
        experts = discover_experts(args.assessments_dir)
        print(f"\nConcatenating PDFs for {len(experts)} experts:")
        for eid, benchmarks in sorted(experts.items()):
            concat_expert_pdfs(eid, benchmarks, args.assessments_dir, args.concat_dir)


if __name__ == "__main__":
    main()
