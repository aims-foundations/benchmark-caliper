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


def _register_fonts():
    for base in FONT_PATHS:
        regular = Path(base) / "FreeSans.ttf"
        bold = Path(base) / "FreeSansBold.ttf"
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont("FreeSans", str(regular)))
            pdfmetrics.registerFont(TTFont("FreeSansBold", str(bold)))
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
        if "Verbatim Quote Registry" in line:
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
        if "Web Source Registry" in line:
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

def extract_citation_ids(text):
    """Extract all citation IDs from text. Handles:
    - [Q42], [Q24, Q25, Q26]
    - [WEB-9], [WEB-1, WEB-5]
    - [DATASET-D40], [DATASET-D40-D42] (range), [D23, D28]
    - [PREFIX-D1], [QUAERO-D11, QUAERO-D12] (org-mode prefixed)
    - [Limitation #1], [CRITICAL Concern 1]
    """
    ids = []
    seen = set()

    def _add(cid):
        if cid not in seen:
            seen.add(cid)
            ids.append(cid)

    # Paper quotes: [Q11] or [Q24, Q25, Q26]
    for m in re.finditer(r"\[(Q\d+(?:,\s*Q\d+)*)\]", text):
        for qid in re.findall(r"Q\d+", m.group(1)):
            _add(qid)

    # Web sources: [WEB-9] or [WEB-1, WEB-5]
    for m in re.finditer(r"\[(WEB-\d+(?:,\s*WEB-\d+)*)\]", text):
        for wid in re.findall(r"WEB-\d+", m.group(1)):
            _add(wid)

    # Dataset citations with DATASET- prefix: [DATASET-D40] or range [DATASET-D40-D42]
    for m in re.finditer(r"\[DATASET-(D\d+)[–\-](D?\d+)\]", text):
        start = int(re.search(r"\d+", m.group(1)).group())
        end_str = m.group(2)
        end = int(re.search(r"\d+", end_str).group())
        for i in range(start, end + 1):
            _add(f"D{i}")

    for m in re.finditer(r"\[DATASET-(D\d+(?:,\s*D\d+)*)\]", text):
        for did in re.findall(r"D\d+", m.group(1)):
            _add(did)

    # Standalone plain D refs: [D23, D28] (not inside DATASET- prefix)
    for m in re.finditer(r"\[(D\d+(?:,\s*D\d+)*)\]", text):
        for did in re.findall(r"D\d+", m.group(1)):
            _add(did)

    # Org-mode prefixed dataset citations: [QUAERO-D1], [QUAERO-D11, DIAMED-D9]
    for m in re.finditer(
        r"\[([A-Za-z][A-Za-z0-9_]*-D\d+(?:,\s*[A-Za-z][A-Za-z0-9_]*-D\d+)*)\]",
        text,
    ):
        for pid in re.findall(r"[A-Za-z][A-Za-z0-9_]*-D\d+", m.group(1)):
            _add(pid)

    # Limitations: [Limitation #1]
    for m in re.finditer(r"\[Limitation #(\d+)\]", text):
        _add(f"Limitation #{m.group(1)}")

    # CRITICAL Concerns: [CRITICAL Concern 1]
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
        if etype == "quote":
            content = f"“{escape(text1)}” ({escape(text2)})"
        elif etype == "web":
            if text2:
                content = f"{escape(text1)} ({escape(text2)})"
            else:
                content = escape(text1)
        elif etype == "dataset":
            content = f"{escape(text1)} — {escape(text2)}"
        elif etype in ("limitation", "critical"):
            content = escape(text1)
        else:
            content = escape(text1)
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
        f"<i>Benchmark: {escape(benchmark)} &nbsp;|&nbsp; "
        f"Context: {escape(region)}</i>",
        styles["Body"],
    ))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(
        width="100%", thickness=1.5, color=ACCENT,
        spaceAfter=10, spaceBefore=2,
    ))

    # === Definition ===
    story.append(Paragraph(
        f"Definition: {escape(DIM_DEFINITIONS[dim_key])}",
        styles["Body"],
    ))

    # === Justification ===
    justification = dim_data.get("justification", "")
    if justification:
        story.append(Paragraph("Justification", styles["SectionHead"]))
        story.append(Paragraph(escape(justification), styles["Body"]))
        story.append(Spacer(1, 4))
        _add_inline_evidence(story, justification, registries, content_width,
                             styles)

    # === Strengths ===
    strengths = dim_data.get("strengths", [])
    if strengths:
        story.append(Paragraph("Strengths", styles["SectionHead"]))
        for s in strengths:
            story.append(
                Paragraph(f"• {escape(s)}", styles["BulletItem"])
            )
            _add_inline_evidence(story, s, registries, content_width, styles,
                                 indent=18)

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

        # Responses with inline evidence
        story.append(
            Paragraph("Checklist responses:", styles["SubHead"])
        )
        evidence_map = dim_data.get("evidence_map", {})
        for item_id, response in checklist.items():
            story.append(Paragraph(
                f"<b>{escape(item_id)}</b>: {escape(response)}",
                styles["Body"],
            ))
            # Merge evidence_map IDs + inline text IDs, dedupe
            map_ids = evidence_map.get(item_id, [])
            text_ids = extract_citation_ids(response)
            all_ids = list(dict.fromkeys(map_ids + text_ids))
            _add_inline_evidence_from_ids(
                story, all_ids, registries, content_width, styles,
            )

    # === Information Gaps ===
    gaps = dim_data.get("information_gaps", [])
    if gaps:
        story.append(Paragraph("Information Gaps", styles["SectionHead"]))
        for gap in gaps:
            story.append(
                Paragraph(f"• {escape(gap)}", styles["GapText"])
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
                Paragraph(f"• {escape(item)}", styles["GapText"])
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
        for i, rem in enumerate(remediation_items, 1):
            story.append(Paragraph(
                f"<b>Gap {i}:</b> {escape(rem.get('gap', ''))}",
                styles["RemedGap"],
            ))
            story.append(Paragraph(
                f"<b>Recommendation:</b> {escape(rem.get('recommendation', ''))}",
                styles["RemedRec"],
            ))

    doc.build(story)


# === Summary PDF Builder ===

def build_summary_pdf(scoring, deployment_text, output_path, styles):
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
        story.append(Paragraph(escape(summary), styles["Body"]))
        story.append(Spacer(1, 8))

    # === Practical Guidance ===
    guidance = scoring.get("practical_guidance", {})
    if guidance:
        story.append(Paragraph("Practical Guidance", styles["SectionHead"]))

        measure = guidance.get("what_this_benchmark_measures", "")
        if measure:
            story.append(
                Paragraph("What This Benchmark Measures", styles["SubHead"])
            )
            story.append(Paragraph(escape(measure), styles["Body"]))
            story.append(Spacer(1, 4))

        depth = guidance.get("construct_depth", "")
        if depth:
            story.append(
                Paragraph("Construct Depth", styles["SubHead"])
            )
            story.append(Paragraph(escape(depth), styles["Body"]))
            story.append(Spacer(1, 4))

        supp = guidance.get("supplementation_needed", "")
        if supp:
            story.append(
                Paragraph("What Else You Need", styles["SubHead"])
            )
            story.append(Paragraph(escape(supp), styles["Body"]))
            story.append(Spacer(1, 4))

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
    build_summary_pdf(scoring, deploy_text, pdf_dir / "summary.pdf", styles)

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


if __name__ == "__main__":
    main()
