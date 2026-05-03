#!/usr/bin/env python3
"""generate_comparative_pdfs.py -- Side-by-side comparison PDFs for expert validation.

Produces 1 comparative PDF per benchmark pair: regional benchmark vs.
global standard, showing deployment context, scores comparison table,
per-dimension justification excerpts, and overall risk ratings.

Usage:
    python3 scripts/stage3/generate_comparative_pdfs.py
    python3 scripts/stage3/generate_comparative_pdfs.py \
        --regional assessments/expert_.../slug \
        --comparator assessments/expert_.../slug
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
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether,
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

# === Regional → comparator benchmark slug mapping ===
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
}


# === Font Registration ===

FONT_PATHS = [
    "/usr/share/fonts/truetype/freefont",
    "/usr/local/share/fonts/freefont",
]

FONT_REGULAR = "FreeSans"
FONT_BOLD = "FreeSansBold"


def _register_fonts():
    global FONT_REGULAR, FONT_BOLD
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
            return
    print(
        "WARNING: FreeSans fonts not found. Using Helvetica (no Devanagari).",
        file=sys.stderr,
    )
    FONT_REGULAR = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"


# === Colors ===

DARK = HexColor("#1a1a2e")
ACCENT = HexColor("#2d6a9f")
SCORE_BG = HexColor("#fef3c7")
HEADER_BG = HexColor("#e8eef4")
WHITE = HexColor("#ffffff")
GRAY_BORDER = HexColor("#cbd5e1")
LIGHT_GRAY = HexColor("#f8fafc")
REGIONAL_BG = HexColor("#e8f5e9")
COMPARATOR_BG = HexColor("#e3f2fd")
DELTA_POS = HexColor("#2e7d32")
DELTA_NEG = HexColor("#c62828")
DELTA_ZERO = HexColor("#616161")


# === Styles ===

def _build_styles():
    styles = getSampleStyleSheet()
    add = styles.add

    add(ParagraphStyle(
        "CompTitle", fontName=FONT_BOLD, fontSize=16, textColor=DARK,
        spaceAfter=4, spaceBefore=0,
    ))
    add(ParagraphStyle(
        "CompSubtitle", fontName=FONT_BOLD, fontSize=11,
        textColor=HexColor("#4a5568"), spaceAfter=4,
    ))
    add(ParagraphStyle(
        "SectionHead", fontName=FONT_BOLD, fontSize=11, textColor=ACCENT,
        spaceBefore=14, spaceAfter=6,
    ))
    add(ParagraphStyle(
        "DimHead", fontName=FONT_BOLD, fontSize=10, textColor=DARK,
        spaceBefore=8, spaceAfter=4,
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
        "Excerpt", fontName=FONT_REGULAR, fontSize=8.5,
        textColor=HexColor("#37474f"), leading=12, spaceAfter=2,
        leftIndent=12,
    ))
    add(ParagraphStyle(
        "CellText", fontName=FONT_REGULAR, fontSize=9, textColor=DARK,
        leading=12,
    ))
    add(ParagraphStyle(
        "CellBold", fontName=FONT_BOLD, fontSize=9, textColor=DARK,
        leading=12,
    ))
    add(ParagraphStyle(
        "CellCenter", fontName=FONT_REGULAR, fontSize=9, textColor=DARK,
        leading=12, alignment=TA_CENTER,
    ))
    add(ParagraphStyle(
        "CellCenterBold", fontName=FONT_BOLD, fontSize=9, textColor=DARK,
        leading=12, alignment=TA_CENTER,
    ))
    add(ParagraphStyle(
        "DimDef", fontName=FONT_REGULAR, fontSize=8,
        textColor=HexColor("#4a5568"), leading=11, spaceAfter=6,
    ))
    add(ParagraphStyle(
        "ExcerptLabel", fontName=FONT_BOLD, fontSize=8.5,
        textColor=ACCENT, leading=12, spaceAfter=2,
    ))
    return styles


# === Helpers ===

def escape(text):
    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def truncate_excerpt(text, max_chars=350):
    """Truncate to max_chars at the nearest sentence boundary."""
    if not text or len(text) <= max_chars:
        return text or ""
    cut = text[:max_chars]
    # Try to cut at sentence end
    for end in (". ", ".\n", ".\t"):
        last = cut.rfind(end)
        if last > max_chars * 0.5:
            return cut[:last + 1]
    return cut.rstrip() + " ..."


def _entry_id(entry):
    """Extract citation ID from an evidence entry string.

    Handles '[Q1] ...', '[WEB-3] ...', and 'DATASET-D5: ...' formats.
    """
    m = re.match(r"\[([^\]]+)\]", entry)
    if m:
        return m.group(1)
    m = re.match(r"(DATASET-D\d+)", entry)
    if m:
        return m.group(1)
    return None


def _cited_evidence(justification, evidence_entries):
    """Filter evidence entries to only those whose ID is cited in the text."""
    if not justification:
        return []
    cited = []
    for entry in evidence_entries:
        eid = _entry_id(entry)
        if not eid:
            continue
        # For DATASET-D5 entries, also match bare D5 in the justification
        patterns = [re.escape(eid) + r"(?!\d)"]
        if eid.startswith("DATASET-"):
            bare = eid.replace("DATASET-", "")
            patterns.append(re.escape(bare) + r"(?!\d)")
        if any(re.search(p, justification) for p in patterns):
            cited.append(entry)
    return cited


def colorize_citations(escaped_text):
    """Wrap citation references in blue font tags."""
    color = "#2d6a9f"

    def _blue_if_citation(m):
        inner = m.group(0)
        if re.search(r"Q\d+|WEB-\d+|D\d+|DATASET", inner):
            return f'<font color="{color}">{inner}</font>'
        return inner

    escaped_text = re.sub(r"\[[^\]]+\]", _blue_if_citation, escaped_text)

    def _blue_if_not_wrapped(m):
        pre = escaped_text[:m.start()]
        if pre.count("<font") > pre.count("</font>"):
            return m.group(0)
        return f'<font color="{color}">{m.group(0)}</font>'

    escaped_text = re.sub(r"DATASET-D\d+", _blue_if_not_wrapped, escaped_text)

    # Bare citation tokens outside brackets (e.g. "partition: D8, D9")
    def _blue_bare(m):
        pre = escaped_text[:m.start()]
        if pre.count("<font") > pre.count("</font>"):
            return m.group(0)
        return f'<font color="{color}">{m.group(0)}</font>'

    escaped_text = re.sub(r"(?<![A-Za-z])D\d+(?!\d)", _blue_bare, escaped_text)
    escaped_text = re.sub(r"(?<![A-Za-z])Q\d+(?!\d)", _blue_bare, escaped_text)
    escaped_text = re.sub(r"WEB-\d+(?!\d)", _blue_bare, escaped_text)
    return escaped_text


def _compute_avg(scoring):
    dims = scoring.get("dimensions", {})
    total, count = 0, 0
    for key in DIM_LABELS:
        sc = dims.get(key, {}).get("score")
        if isinstance(sc, (int, float)):
            total += sc
            count += 1
    return total / count if count > 0 else 0


def _delta_str(regional_score, comparator_score):
    """Format score delta as +N, -N, or 0."""
    if not isinstance(regional_score, (int, float)) or not isinstance(comparator_score, (int, float)):
        return "—"
    d = round(regional_score - comparator_score, 1)
    if d == int(d):
        d = int(d)
    if d > 0:
        return f"+{d}"
    elif d < 0:
        return str(d)
    return "0"


# === Pair Discovery ===

def discover_pairs(assessments_dir):
    """Find all regional→comparator tuple pairs by expert_id + slug matching.

    Returns list of (regional_tuple_dir, comparator_tuple_dir) pairs.
    """
    assessments_dir = Path(assessments_dir)
    pairs = []

    # === Group benchmark dirs by expert_id ===
    expert_benchmarks = {}
    for d in sorted(assessments_dir.iterdir()):
        if not d.is_dir() or not d.name.startswith("expert_"):
            continue
        parts = d.name.split("__", 1)
        if len(parts) != 2:
            continue
        expert_id, bench_slug = parts
        if expert_id not in expert_benchmarks:
            expert_benchmarks[expert_id] = {}
        expert_benchmarks[expert_id][bench_slug] = d

    # === Match regional → comparator by slug ===
    for expert_id, benchmarks in expert_benchmarks.items():
        for regional_bench, comparator_bench in COMPARATOR_MAP.items():
            if regional_bench not in benchmarks or comparator_bench not in benchmarks:
                continue
            regional_dir = benchmarks[regional_bench]
            comparator_dir = benchmarks[comparator_bench]

            # Find shared slugs (same deployment context)
            for slug_dir in sorted(comparator_dir.iterdir()):
                if not slug_dir.is_dir():
                    continue
                if not (slug_dir / "scoring.json").exists():
                    continue
                regional_slug = regional_dir / slug_dir.name
                if regional_slug.is_dir() and (regional_slug / "scoring.json").exists():
                    pairs.append((regional_slug, slug_dir))

    return pairs


# === PDF Builder ===

def build_comparative_pdf(regional_dir, comparator_dir, output_path, styles):
    """Build the side-by-side comparison PDF for one benchmark pair."""
    regional_scoring = json.loads(
        (regional_dir / "scoring.json").read_text(encoding="utf-8"))
    comparator_scoring = json.loads(
        (comparator_dir / "scoring.json").read_text(encoding="utf-8"))

    deploy_path = regional_dir / "deployment_description.txt"
    deploy_text = deploy_path.read_text(encoding="utf-8") if deploy_path.exists() else ""

    regional_name = regional_scoring.get("benchmark", "Regional").upper()
    comparator_name = comparator_scoring.get("benchmark", "Global").upper()
    region = regional_scoring.get("region", comparator_scoring.get("region", ""))

    regional_risk = regional_scoring.get("risk_assessment", "N/A").upper()
    comparator_risk = comparator_scoring.get("risk_assessment", "N/A").upper()

    regional_avg = _compute_avg(regional_scoring)
    comparator_avg = _compute_avg(comparator_scoring)

    doc = SimpleDocTemplate(
        str(output_path), pagesize=letter,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
    )
    content_width = letter[0] - 1.5 * inch
    story = []

    # =========================================================
    # PAGE 1: Title + Deployment Context + Scores Comparison
    # =========================================================

    # === Title ===
    story.append(Paragraph(
        f"Comparative Assessment: {escape(regional_name)} vs. {escape(comparator_name)}",
        styles["CompTitle"],
    ))
    story.append(Paragraph(
        f"Deployment context: {escape(region)}",
        styles["CompSubtitle"],
    ))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(
        width="100%", thickness=1.5, color=ACCENT,
        spaceAfter=10, spaceBefore=2,
    ))

    # === Deployment Context ===
    if deploy_text:
        story.append(Paragraph("Deployment Context", styles["SectionHead"]))
        for line in deploy_text.strip().splitlines():
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

    # === Risk Ratings ===
    story.append(Paragraph("Overall Risk Ratings", styles["SectionHead"]))
    risk_data = [
        [Paragraph("<b>Benchmark</b>", styles["CellBold"]),
         Paragraph("<b>Risk</b>", styles["CellBold"]),
         Paragraph("<b>Avg. Score</b>", styles["CellBold"])],
        [Paragraph(escape(regional_name), styles["CellText"]),
         Paragraph(escape(regional_risk), styles["CellText"]),
         Paragraph(f"{regional_avg:.1f} / 5", styles["CellText"])],
        [Paragraph(escape(comparator_name), styles["CellText"]),
         Paragraph(escape(comparator_risk), styles["CellText"]),
         Paragraph(f"{comparator_avg:.1f} / 5", styles["CellText"])],
    ]
    risk_tbl = Table(risk_data, colWidths=[
        content_width * 0.40, content_width * 0.30, content_width * 0.30,
    ])
    risk_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("BACKGROUND", (0, 1), (-1, 1), REGIONAL_BG),
        ("BACKGROUND", (0, 2), (-1, 2), COMPARATOR_BG),
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(risk_tbl)
    story.append(Spacer(1, 12))

    # === Scores Comparison Table ===
    story.append(Paragraph("Dimension Scores Comparison", styles["SectionHead"]))

    header = [
        Paragraph("<b>Dimension</b>", styles["CellBold"]),
        Paragraph(f"<b>{escape(regional_name)}</b>", styles["CellBold"]),
        Paragraph("<b>Rating</b>", styles["CellBold"]),
        Paragraph(f"<b>{escape(comparator_name)}</b>", styles["CellBold"]),
        Paragraph("<b>Rating</b>", styles["CellBold"]),
        Paragraph("<b>Δ</b>", styles["CellCenterBold"]),
    ]
    rows = [header]

    regional_dims = regional_scoring.get("dimensions", {})
    comparator_dims = comparator_scoring.get("dimensions", {})

    for dim_key, dim_label in DIM_LABELS.items():
        r_score = regional_dims.get(dim_key, {}).get("score", "N/A")
        c_score = comparator_dims.get(dim_key, {}).get("score", "N/A")
        r_rating = SCORE_LABELS.get(int(r_score), "") if isinstance(r_score, (int, float)) else ""
        c_rating = SCORE_LABELS.get(int(c_score), "") if isinstance(c_score, (int, float)) else ""
        delta = _delta_str(r_score, c_score)

        rows.append([
            Paragraph(f"{escape(dim_label)} ({DIM_ABBREVS[dim_key]})", styles["CellText"]),
            Paragraph(f"{r_score}/5", styles["CellCenter"]),
            Paragraph(r_rating, styles["CellText"]),
            Paragraph(f"{c_score}/5", styles["CellCenter"]),
            Paragraph(c_rating, styles["CellText"]),
            Paragraph(delta, styles["CellCenter"]),
        ])

    # Average row
    avg_delta = _delta_str(regional_avg, comparator_avg)
    rows.append([
        Paragraph("<b>Average</b>", styles["CellBold"]),
        Paragraph(f"<b>{regional_avg:.1f}</b>", styles["CellCenterBold"]),
        Paragraph("", styles["CellText"]),
        Paragraph(f"<b>{comparator_avg:.1f}</b>", styles["CellCenterBold"]),
        Paragraph("", styles["CellText"]),
        Paragraph(f"<b>{avg_delta}</b>", styles["CellCenterBold"]),
    ])

    col_widths = [
        content_width * 0.25,
        content_width * 0.10,
        content_width * 0.22,
        content_width * 0.10,
        content_width * 0.22,
        content_width * 0.11,
    ]
    scores_tbl = Table(rows, colWidths=col_widths)

    # === Color code the delta column ===
    tbl_style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        # Alternate row shading
        ("BACKGROUND", (0, -1), (-1, -1), LIGHT_GRAY),
    ]
    for i, dim_key in enumerate(DIM_LABELS, start=1):
        r_sc = regional_dims.get(dim_key, {}).get("score")
        c_sc = comparator_dims.get(dim_key, {}).get("score")
        if isinstance(r_sc, (int, float)) and isinstance(c_sc, (int, float)):
            if r_sc > c_sc:
                tbl_style_cmds.append(("TEXTCOLOR", (5, i), (5, i), DELTA_POS))
            elif r_sc < c_sc:
                tbl_style_cmds.append(("TEXTCOLOR", (5, i), (5, i), DELTA_NEG))
            else:
                tbl_style_cmds.append(("TEXTCOLOR", (5, i), (5, i), DELTA_ZERO))

    scores_tbl.setStyle(TableStyle(tbl_style_cmds))
    story.append(scores_tbl)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        f"Δ = {escape(regional_name)} score − {escape(comparator_name)} score. "
        "Positive = regional benchmark scores higher.",
        styles["DimDef"],
    ))

    # =========================================================
    # Overall Summaries (before per-dimension detail)
    # =========================================================

    story.append(Spacer(1, 6))
    story.append(HRFlowable(
        width="100%", thickness=1, color=ACCENT,
        spaceAfter=6, spaceBefore=6,
    ))
    story.append(Paragraph("Overall Summaries", styles["SectionHead"]))

    r_summary = regional_scoring.get("overall_summary", "")
    c_summary = comparator_scoring.get("overall_summary", "")

    if r_summary:
        story.append(Paragraph(
            f"<b>{escape(regional_name)}</b> (risk: {escape(regional_risk)})",
            styles["ExcerptLabel"],
        ))
        story.append(Paragraph(
            colorize_citations(escape(r_summary)),
            styles["Excerpt"],
        ))
        story.append(Spacer(1, 6))

    if c_summary:
        story.append(Paragraph(
            f"<b>{escape(comparator_name)}</b> (risk: {escape(comparator_risk)})",
            styles["ExcerptLabel"],
        ))
        story.append(Paragraph(
            colorize_citations(escape(c_summary)),
            styles["Excerpt"],
        ))

    # =========================================================
    # Per-Dimension Justification + Evidence Comparison
    # =========================================================

    half_width = content_width * 0.50
    section_header = [
        Spacer(1, 6),
        HRFlowable(
            width="100%", thickness=1, color=ACCENT,
            spaceAfter=6, spaceBefore=6,
        ),
        Paragraph(
            "Per-Dimension Justification Comparison", styles["SectionHead"],
        ),
        Paragraph(
            "Each benchmark's full assessment justification and cited evidence, "
            "shown side by side.",
            styles["DimDef"],
        ),
    ]
    first_dim = True

    for dim_key, dim_label in DIM_LABELS.items():
        r_dim = regional_dims.get(dim_key, {})
        c_dim = comparator_dims.get(dim_key, {})

        r_score = r_dim.get("score", "N/A")
        c_score = c_dim.get("score", "N/A")
        r_conf = r_dim.get("confidence", "N/A")
        c_conf = c_dim.get("confidence", "N/A")
        r_just = r_dim.get("justification", "")
        c_just = c_dim.get("justification", "")

        abbrev = DIM_ABBREVS[dim_key]
        definition = DIM_DEFINITIONS[dim_key]

        block = []

        # === Dimension header ===
        block.append(Paragraph(
            f"{escape(dim_label)} ({abbrev})",
            styles["DimHead"],
        ))
        block.append(Paragraph(escape(definition), styles["DimDef"]))

        # === Side-by-side justification table ===
        excerpt_rows = [
            [Paragraph(
                f"<b>{escape(regional_name)}</b> — {r_score}/5 "
                f"({SCORE_LABELS.get(int(r_score), '')}) "
                f"[{r_conf} confidence]" if isinstance(r_score, (int, float)) else
                f"<b>{escape(regional_name)}</b> �� {r_score}",
                styles["CellBold"]),
             Paragraph(
                f"<b>{escape(comparator_name)}</b> — {c_score}/5 "
                f"({SCORE_LABELS.get(int(c_score), '')}) "
                f"[{c_conf} confidence]" if isinstance(c_score, (int, float)) else
                f"<b>{escape(comparator_name)}</b> — {c_score}",
                styles["CellBold"])],
            [Paragraph(colorize_citations(escape(r_just)) if r_just else "<i>No justification available</i>",
                        styles["Excerpt"]),
             Paragraph(colorize_citations(escape(c_just)) if c_just else "<i>No justification available</i>",
                        styles["Excerpt"])],
        ]

        excerpt_tbl = Table(excerpt_rows, colWidths=[half_width, half_width])
        excerpt_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), REGIONAL_BG),
            ("BACKGROUND", (1, 0), (1, 0), COMPARATOR_BG),
            ("BACKGROUND", (0, 1), (0, 1), HexColor("#f1f8e9")),
            ("BACKGROUND", (1, 1), (1, 1), HexColor("#e8f4fd")),
            ("GRID", (0, 0), (-1, -1), 0.5, GRAY_BORDER),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        block.append(excerpt_tbl)

        # === Side-by-side evidence table (only justification-cited entries) ===
        r_all_ev = (r_dim.get("evidence_quotes", [])
                    + r_dim.get("evidence_web_sources", [])
                    + r_dim.get("evidence_dataset", []))
        c_all_ev = (c_dim.get("evidence_quotes", [])
                    + c_dim.get("evidence_web_sources", [])
                    + c_dim.get("evidence_dataset", []))
        r_ev = _cited_evidence(r_just, r_all_ev)
        c_ev = _cited_evidence(c_just, c_all_ev)

        if r_ev or c_ev:
            n_rows = max(len(r_ev), len(c_ev))
            ev_rows = [
                [Paragraph(f"<b>{escape(regional_name)} evidence</b>",
                           styles["CellBold"]),
                 Paragraph(f"<b>{escape(comparator_name)} evidence</b>",
                           styles["CellBold"])],
            ]
            for i in range(n_rows):
                r_cell = colorize_citations(escape(r_ev[i])) if i < len(r_ev) else ""
                c_cell = colorize_citations(escape(c_ev[i])) if i < len(c_ev) else ""
                ev_rows.append([
                    Paragraph(r_cell, styles["Excerpt"]),
                    Paragraph(c_cell, styles["Excerpt"]),
                ])

            ev_tbl = Table(ev_rows, colWidths=[half_width, half_width])
            ev_style = [
                ("BACKGROUND", (0, 0), (0, 0), REGIONAL_BG),
                ("BACKGROUND", (1, 0), (1, 0), COMPARATOR_BG),
                ("GRID", (0, 0), (-1, -1), 0.5, GRAY_BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]
            for i in range(1, n_rows + 1):
                ev_style.append(("BACKGROUND", (0, i), (0, i), HexColor("#f1f8e9")))
                ev_style.append(("BACKGROUND", (1, i), (1, i), HexColor("#e8f4fd")))
            ev_tbl.setStyle(TableStyle(ev_style))
            block.append(Spacer(1, 4))
            block.append(ev_tbl)

        block.append(Spacer(1, 10))
        # Keep section header with first dim header to prevent orphaning
        if first_dim:
            story.append(KeepTogether(section_header + block[:3]))
            first_dim = False
        else:
            story.append(KeepTogether(block[:3]))
        for flowable in block[3:]:
            story.append(flowable)

    doc.build(story)


# === Main ===

def process_pair(regional_dir, comparator_dir, styles):
    """Generate comparative PDF for one pair. Returns 1 on success, 0 on skip."""
    regional_dir = Path(regional_dir)
    comparator_dir = Path(comparator_dir)

    for d, label in [(regional_dir, "regional"), (comparator_dir, "comparator")]:
        if not (d / "scoring.json").exists():
            print(f"  SKIP: {label} {d.name} has no scoring.json")
            return 0

    pdf_dir = comparator_dir / "pdfs"
    pdf_dir.mkdir(exist_ok=True)
    output_path = pdf_dir / "comparative.pdf"

    build_comparative_pdf(regional_dir, comparator_dir, output_path, styles)
    return 1


def main():
    p = argparse.ArgumentParser(
        description="Generate comparative PDFs for expert validation survey",
    )
    p.add_argument(
        "--assessments-dir", default="assessments",
        help="Path to assessments directory (default: assessments/)",
    )
    p.add_argument(
        "--regional", default=None,
        help="Regional tuple directory (single-pair mode)",
    )
    p.add_argument(
        "--comparator", default=None,
        help="Comparator tuple directory (single-pair mode)",
    )
    args = p.parse_args()

    _register_fonts()
    styles = _build_styles()

    # === Single-pair mode ===
    if args.regional and args.comparator:
        r = Path(args.regional)
        c = Path(args.comparator)
        if not r.exists() or not c.exists():
            print(f"ERROR: directory not found", file=sys.stderr)
            sys.exit(1)
        print(f"Processing: {r.name} vs {c.name}")
        n = process_pair(r, c, styles)
        if n:
            print(f"  Generated comparative.pdf in {c / 'pdfs'}")
        return

    # === Batch mode: auto-discover all pairs ===
    pairs = discover_pairs(args.assessments_dir)
    if not pairs:
        print(f"No comparative pairs found in {args.assessments_dir}")
        sys.exit(1)

    print(f"Found {len(pairs)} comparative pairs")
    total = 0
    for regional_dir, comparator_dir in tqdm(pairs, desc="Generating comparative PDFs"):
        expert_bench = comparator_dir.parent.name
        slug = comparator_dir.name
        print(f"  {expert_bench}/{slug}")
        n = process_pair(regional_dir, comparator_dir, styles)
        total += n

    print(f"Done: {total} comparative PDFs generated")


if __name__ == "__main__":
    main()
