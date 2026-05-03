#!/usr/bin/env python3
"""create_expert_forms.py -- Create Google Forms for expert validation survey.

Creates one Google Form per expert with companion PDF links for each
assessment tuple. Forms follow the structure defined in
stage3_planning/expert_validation_survey_spec_v3.md.

Sections 1-3 (primary review) + Section 4 (comparative) are fully implemented.

Usage (user-run only — CC must not execute this script):
    python3 scripts/stage3/create_expert_forms.py
    python3 scripts/stage3/create_expert_forms.py --expert expert_a59b4f572c38
    python3 scripts/stage3/create_expert_forms.py --dry-run
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(it, **kw):
        return it


# === Constants ===

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/forms.body",
]

DIM_KEYS = [
    "input_ontology", "input_content", "input_form",
    "output_ontology", "output_content", "output_form",
]

DIM_LABELS = {
    "input_ontology": "Input Ontology (IO)",
    "input_content": "Input Content (IC)",
    "input_form": "Input Form (IF)",
    "output_ontology": "Output Ontology (OO)",
    "output_content": "Output Content (OC)",
    "output_form": "Output Form (OF)",
}

DIM_ABBREVS = {
    "input_ontology": "io", "input_content": "ic", "input_form": "if",
    "output_ontology": "oo", "output_content": "oc", "output_form": "of",
}

SCORE_LABELS = {
    1: "Serious concern", 2: "Significant gaps", 3: "Moderate gaps",
    4: "Minor gaps", 5: "Strong alignment",
}

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
}
COMPARATOR_BENCHMARKS = set(COMPARATOR_MAP.values())

EXPECTED_REGIONAL_BENCHMARKS = 2
EXPECTED_TUPLES_PER_BENCHMARK = 2
EXPECTED_COMPARATIVE_PAIRS = 2
DIM_PDF_NAMES = ["summary", "io", "ic", "if", "oo", "oc", "of"]


def validate_expert_completeness(expert_id, benchmarks, drive_links,
                                 assessments_dir):
    """Fail hard if any expected PDFs or comparatives are missing.

    Every expert must have exactly 2 regional benchmarks × 2 tuples = 4
    primary assessments, each with 7 drive-linked PDFs (summary + 6 dims),
    plus 2 comparative pairs each with a comparative PDF.
    """
    errors = []
    assessments_dir = Path(assessments_dir)

    regional = [(s, t) for s, t in benchmarks if s not in COMPARATOR_BENCHMARKS]

    if len(regional) != EXPECTED_REGIONAL_BENCHMARKS:
        errors.append(
            f"expected {EXPECTED_REGIONAL_BENCHMARKS} regional benchmarks, "
            f"found {len(regional)}: {[s for s, _ in regional]}"
        )

    for bench_slug, tuple_dirs in regional:
        if len(tuple_dirs) != EXPECTED_TUPLES_PER_BENCHMARK:
            errors.append(
                f"benchmark '{bench_slug}': expected "
                f"{EXPECTED_TUPLES_PER_BENCHMARK} tuples, "
                f"found {len(tuple_dirs)}"
            )

        if bench_slug not in COMPARATOR_MAP:
            errors.append(
                f"benchmark '{bench_slug}' has no entry in COMPARATOR_MAP "
                f"— comparative section will be silently skipped"
            )

        for td in tuple_dirs:
            tkey = str(td.relative_to(assessments_dir))
            links = drive_links.get(tkey, {})
            for pdf_name in DIM_PDF_NAMES:
                if pdf_name not in links:
                    errors.append(
                        f"missing drive link '{pdf_name}' for {tkey}"
                    )

    pairs = _find_comparative_pairs(benchmarks, assessments_dir)
    if len(pairs) != EXPECTED_COMPARATIVE_PAIRS:
        errors.append(
            f"expected {EXPECTED_COMPARATIVE_PAIRS} comparative pairs, "
            f"found {len(pairs)}"
        )

    for regional_dir, comp_dir in pairs:
        tkey = str(comp_dir.relative_to(assessments_dir))
        links = drive_links.get(tkey, {})
        if "comparative" not in links:
            errors.append(f"missing drive link 'comparative' for {tkey}")

    if errors:
        print(f"\nFATAL: {expert_id} is incomplete:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print(
            "\nFix the issues above before creating the form. "
            "This check exists to prevent deploying incomplete surveys.",
            file=sys.stderr,
        )
        sys.exit(1)

def _ordering_options(proposed, comparison):
    return [
        {"value": f"{proposed} should score higher than {comparison}"},
        {"value": "Relative ordering is about right"},
        {"value": f"{comparison} should score higher than {proposed}"},
        {"value": "Scores should be approximately equal"},
        {"value": "Cannot assess"},
    ]

LIKERT_OPTIONS = [
    {"value": "1 — Strongly disagree"},
    {"value": "2 — Disagree"},
    {"value": "3 — Neutral"},
    {"value": "4 — Agree"},
    {"value": "5 — Strongly agree"},
]

RISK_AGREEMENT_OPTIONS = [
    {"value": "Too conservative (risk is lower)"},
    {"value": "About right"},
    {"value": "Too lenient (risk is higher)"},
    {"value": "Cannot assess"},
]

CONFIDENCE_OPTIONS = [
    {"value": "Overconfident"},
    {"value": "About right"},
    {"value": "Underconfident"},
    {"value": "Cannot assess"},
]

NOVEL_INSIGHTS_OPTIONS = [
    {"value": "Yes — several new concerns"},
    {"value": "Yes — one or two"},
    {"value": "No — but it confirmed my existing concerns"},
    {"value": "No — it missed concerns I already knew about"},
]

VALUE_OPTIONS = [
    {"value": "Comparable to expert review"},
    {"value": "Useful complement to expert review"},
    {"value": "Starting point that needs substantial revision"},
    {"value": "Not useful"},
]


# === Auth ===

def get_credentials(secrets_dir):
    secrets_dir = Path(secrets_dir)
    token_path = secrets_dir / "token.json"
    creds_path = secrets_dir / "credentials.json"

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not creds_path.exists():
                print(f"ERROR: {creds_path} not found", file=sys.stderr)
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(
                str(creds_path), SCOPES,
            )
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())

    return creds


# === Data Loading ===

def load_tuple_data(tuple_dir):
    td = Path(tuple_dir)
    scoring = json.loads((td / "scoring.json").read_text())
    elicitation_qs = json.loads((td / "elicitation_questions.json").read_text())
    elicitation_as = json.loads((td / "elicitation_answers.json").read_text())
    deployment_desc = (td / "deployment_description.txt").read_text().strip()
    return {
        "scoring": scoring,
        "elicitation_questions": elicitation_qs,
        "elicitation_answers": elicitation_as,
        "deployment_description": deployment_desc,
    }


def load_drive_links(secrets_dir):
    link_path = Path(secrets_dir) / "drive_links.json"
    if not link_path.exists():
        return {}
    return json.loads(link_path.read_text())


# === Expert Discovery ===

def discover_experts(assessments_dir):
    """Returns {expert_id: [(benchmark_slug, [tuple_dir, ...]), ...]}."""
    assessments_dir = Path(assessments_dir)
    expert_benchmarks = defaultdict(lambda: defaultdict(list))

    for expert_bench_dir in sorted(assessments_dir.glob("expert_*")):
        if not expert_bench_dir.is_dir():
            continue
        parts = expert_bench_dir.name.split("__", 1)
        if len(parts) != 2:
            continue
        expert_id, benchmark_slug = parts

        for slug_dir in sorted(expert_bench_dir.iterdir()):
            if slug_dir.is_dir() and (slug_dir / "scoring.json").exists():
                expert_benchmarks[expert_id][benchmark_slug].append(slug_dir)

    result = {}
    for expert_id in sorted(expert_benchmarks):
        benchmarks = []
        for bench_slug in sorted(expert_benchmarks[expert_id]):
            tuples = sorted(expert_benchmarks[expert_id][bench_slug])
            benchmarks.append((bench_slug, tuples))
        result[expert_id] = benchmarks
    return result


def tuple_key(tuple_dir, assessments_dir):
    return str(Path(tuple_dir).relative_to(assessments_dir))


# === Item Builders ===

def _page_break(title, description=""):
    return {"title": title, "description": description, "pageBreakItem": {}}


def _likert(title, required=True):
    return {
        "title": title,
        "questionItem": {
            "question": {
                "required": required,
                "choiceQuestion": {
                    "type": "RADIO",
                    "options": list(LIKERT_OPTIONS),
                },
            },
        },
    }


def _mcq(title, options, required=True):
    return {
        "title": title,
        "questionItem": {
            "question": {
                "required": required,
                "choiceQuestion": {
                    "type": "RADIO",
                    "options": list(options),
                },
            },
        },
    }


def _text(title, required=False):
    return {
        "title": title,
        "questionItem": {
            "question": {
                "required": required,
                "textQuestion": {"paragraph": True},
            },
        },
    }


# === Section Builders ===

def _format_benchmark_name(scoring):
    return scoring["benchmark"].upper()


def _format_elicitation_qa(data):
    lines = []
    for q in data["elicitation_questions"]:
        qid = q["id"]
        dim = q.get("dimension", "")
        answer = data["elicitation_answers"].get(qid, "(no response)")
        lines.append(f'{qid} ({dim}): "{q["question"]}"')
        lines.append(f'  → "{answer}"\n')
    return "\n".join(lines)


def build_context_page(data, drive_links, assessments_dir, assess_num):
    """Section 1: Deployment Context + Overall Assessment (one page)."""
    scoring = data["scoring"]
    benchmark = _format_benchmark_name(scoring)
    region = scoring["region"]
    risk = scoring["risk_assessment"].upper()

    tkey = tuple_key(data["scoring"]["_tuple_dir"], assessments_dir)
    links = drive_links.get(tkey, {})
    summary_link = links.get("summary", "(link not available)")

    qa_text = _format_elicitation_qa(data)
    description = (
        f"{data['deployment_description']}\n\n"
        f"Your elicitation responses:\n\n{qa_text}\n"
        f"▶ Open the Summary PDF before answering: {summary_link}"
    )

    return [
        _page_break(f"Assessment {assess_num}: {benchmark} — {region}", description),
        _mcq(
            f"The pipeline assigned an overall risk rating of {risk} for using "
            f"{benchmark} in this deployment context. How does this compare to "
            f"your expert judgment?",
            RISK_AGREEMENT_OPTIONS,
        ),
        _likert(
            "The overall summary paragraph accurately synthesizes the findings "
            "across all six dimensions."
        ),
        _likert(
            "The overall summary captures the most important validity concerns "
            "for this deployment context."
        ),
        _likert(
            "The 'Construct Depth' description accurately characterizes what "
            "this benchmark measures and does not measure."
        ),
        _likert(
            "The 'What Else You Need' recommendations would help a practitioner "
            "plan supplementary evaluation."
        ),
        _text(
            "Any overall comments on the assessment's quality, framing, or "
            "usefulness?"
        ),
    ]


def build_dimension_page(dim_key, data, drive_links, assessments_dir, assess_num):
    """Section 2: One dimension review page."""
    scoring = data["scoring"]
    dim_data = scoring["dimensions"][dim_key]
    dim_label = DIM_LABELS[dim_key]
    score = dim_data["score"]
    rating = SCORE_LABELS.get(int(score), "")
    confidence = dim_data.get("confidence", "N/A")

    tkey = tuple_key(scoring["_tuple_dir"], assessments_dir)
    links = drive_links.get(tkey, {})
    pdf_link = links.get(DIM_ABBREVS[dim_key], "(link not available)")

    description = (
        f"Score: {score}/5 ({rating}) | Confidence: {confidence}\n\n"
        f"▶ Open the {dim_label} PDF before answering: {pdf_link}"
    )

    return [
        _page_break(f"Assessment {assess_num} — {dim_label}", description),
        _likert(
            f"The score of {score}/5 ({rating}) for {dim_label} is appropriate "
            f"for this deployment context."
        ),
        _likert(
            "The justification adequately explains why this score was assigned."
        ),
        _likert(
            "The arguments for this dimension are well-supported by the cited "
            "evidence."
        ),
        _likert(
            "The checklist responses and information gaps capture the most "
            "important validity concerns for this dimension."
        ),
        _mcq(
            f"The pipeline assigned {confidence} confidence for this dimension. "
            f"How does this compare to your judgment of the evidence strength?",
            CONFIDENCE_OPTIONS,
        ),
        _text(
            "What important validity considerations, if any, are missing or "
            "mischaracterized for this dimension? For example, were any "
            "strengths overstated or weaknesses omitted (or vice versa)?"
        ),
    ]


def build_usefulness_page(assess_num):
    """Section 3: Usefulness & Actionability (one page)."""
    return [
        _page_break(
            f"Assessment {assess_num} — Usefulness & Actionability",
            "Based on your review of the full assessment, please evaluate its "
            "overall usefulness.",
        ),
        _mcq(
            "Did the assessment surface validity concerns you hadn't previously "
            "considered?",
            NOVEL_INSIGHTS_OPTIONS,
        ),
        _text(
            "Which concerns were new or surprising to you? "
            '(If you answered "Yes" above)'
        ),
        _likert(
            "I would trust this assessment to inform a real deployment decision "
            "about this benchmark."
        ),
        _likert(
            "This assessment could help evaluation/benchmark design decisions "
            "for the deployment use case and target population of interest."
        ),
        _likert(
            "The remediation recommendations are reasonable."
        ),
        _likert(
            "The remediation recommendations are actionable."
        ),
        _mcq(
            "How would you characterize this assessment's value relative to a "
            "manual expert review?",
            VALUE_OPTIONS,
        ),
        _text(
            "Are there specific refinements or additions that would make this "
            "assessment more useful for practitioners in your domain?"
        ),
    ]


def _compute_avg(scoring):
    dims = scoring.get("dimensions", {})
    total, count = 0, 0
    for key in DIM_KEYS:
        sc = dims.get(key, {}).get("score")
        if isinstance(sc, (int, float)):
            total += sc
            count += 1
    return round(total / count, 1) if count else 0


def _get_paper_url(tuple_dir):
    """Read paper_url from a tuple's benchmark.yaml, if available."""
    bm_path = tuple_dir / "benchmark.yaml"
    if bm_path.exists():
        bm = yaml.safe_load(bm_path.read_text())
        return (bm or {}).get("paper_url", "")
    return ""


def build_comparative_page(regional_dir, comparator_dir, drive_links,
                           assessments_dir, pair_num):
    """Section 4: Comparative assessment for one benchmark pair."""
    r_scoring = json.loads((regional_dir / "scoring.json").read_text())
    c_scoring = json.loads((comparator_dir / "scoring.json").read_text())

    r_name = r_scoring["benchmark"].upper()
    c_name = c_scoring["benchmark"].upper()
    r_avg = _compute_avg(r_scoring)
    c_avg = _compute_avg(c_scoring)
    region = r_scoring.get("region", "")

    tkey = tuple_key(comparator_dir, assessments_dir)
    links = drive_links.get(tkey, {})
    comp_link = links.get("comparative", "(link not available)")

    c_paper_url = _get_paper_url(comparator_dir)
    c_ref = f" ({c_paper_url})" if c_paper_url else ""

    description = (
        f"The pipeline assessed two benchmarks for the same deployment "
        f"context: {r_name} (a benchmark proposed by you) and "
        f"{c_name}{c_ref} (a benchmark we selected for comparison). Both "
        f"were evaluated across the same six validity dimensions. The "
        f"comparative PDF below presents excerpts from each benchmark's "
        f"individual assessment for this context — please review it "
        f"before answering the questions.\n\n"
        f"{r_name}: {r_avg}/5 avg | {c_name}: {c_avg}/5 avg\n"
        f"Context: {region}\n\n"
        f"▶ Open the Comparative PDF: {comp_link}"
    )

    ordering = _ordering_options(r_name, c_name)

    items = [
        _page_break(
            f"Comparative {pair_num}: {r_name} vs. {c_name}",
            description,
        ),
        _mcq(
            f"The pipeline scored {r_name} at an average of {r_avg}/5 and "
            f"{c_name} at {c_avg}/5 for this deployment context. Does this "
            f"relative ordering match your expert judgment?",
            ordering,
        ),
    ]

    r_dims = r_scoring.get("dimensions", {})
    c_dims = c_scoring.get("dimensions", {})
    for dim_key in DIM_KEYS:
        dim_label = DIM_LABELS[dim_key]
        r_sc = r_dims.get(dim_key, {}).get("score", "N/A")
        c_sc = c_dims.get(dim_key, {}).get("score", "N/A")
        items.append(_mcq(
            f"For {dim_label}, the pipeline scored {r_name} at {r_sc}/5 and "
            f"{c_name} at {c_sc}/5. Does this relative ordering match your "
            f"judgment?",
            ordering,
        ))

    items.append(_likert(
        "The pipeline's justifications convincingly explain why the two "
        "benchmarks received different scores."
    ))
    items.append(_likert(
        "The scoring leaves room to grow: a benchmark designed to address "
        "the gaps identified in both assessments could reasonably achieve a "
        "higher score for this deployment context."
    ))
    items.append(_text(
        "Are there important differences between these two benchmarks (for "
        "this deployment context) that the pipeline failed to capture?"
    ))

    return items


def build_closing_page():
    return [
        _page_break(
            "Thank You",
            "Thank you for completing this review. Your expert feedback is "
            "invaluable for validating and improving this automated assessment "
            "pipeline.\n\n"
            "If you have any remaining comments or feedback about the overall "
            "experience, please share them below.",
        ),
        _text("Any final comments or feedback?"),
    ]


# === Form Assembly ===

WELCOME_DESCRIPTION = (
    "Thank you for participating in this expert validation study.\n\n"
    "You will review automated validity assessments for benchmark datasets "
    "in specific deployment contexts. For each assessment, you will:\n\n"
    "1. Read a companion PDF with the detailed analysis\n"
    "2. Answer questions about the assessment's accuracy and completeness\n\n"
    "Each section includes a link to the relevant PDF — please open it "
    "before answering the questions.\n\n"
    "Estimated time: 3 - 4.5 hours (~45 mins - 1 hr per "
    "[benchmark, use case, target population] example you provided "
    "(4 total) and 15-20 mins per comparative assessment).\n\n"
    "Please be as transparent as possible with your answers. This will "
    "help us accurately frame any contributions or uses of the pipeline "
    "in the paper, as well as help us improve the pipeline for future "
    "iterations.\n\n"
    "IMPORTANT: The total PDF materials are quite long due to the "
    "inclusion of detailed evidence tables. You should aim to fully "
    "digest the main text of each document, but you do not need to "
    "exhaustively read the evidence tables — they are provided as a "
    "reference to help you assess your answers to the questions in "
    "this form.\n\n"
    "Your responses are saved automatically as you progress (requires "
    "being signed into your Google account; drafts are tied to your "
    "browser and device)."
)


def _find_comparative_pairs(benchmarks, assessments_dir):
    """Find (regional_tuple_dir, comparator_tuple_dir) pairs for Section 4.

    Matches regional benchmarks to their comparators using COMPARATOR_MAP,
    pairing tuples that share the same deployment slug.
    """
    bench_dict = {slug: dirs for slug, dirs in benchmarks}
    pairs = []
    for regional_bench, comparator_bench in COMPARATOR_MAP.items():
        if regional_bench not in bench_dict or comparator_bench not in bench_dict:
            continue
        comp_dirs = {d.name: d for d in bench_dict[comparator_bench]}
        for rd in bench_dict[regional_bench]:
            if rd.name in comp_dirs:
                pairs.append((rd, comp_dirs[rd.name]))
    return pairs


def build_form_items(benchmarks, drive_links, assessments_dir):
    """Build all form items for one expert. Returns list of item dicts."""
    items = []
    assess_num = 0

    bench_dict = {slug: dirs for slug, dirs in benchmarks}
    pair_num = 0

    for bench_slug, tuple_dirs in benchmarks:
        if bench_slug in COMPARATOR_BENCHMARKS:
            continue

        # === Sections 1-3: regional tuples for this benchmark ===
        for td in tuple_dirs:
            assess_num += 1
            data = load_tuple_data(td)
            data["scoring"]["_tuple_dir"] = td

            items.extend(build_context_page(
                data, drive_links, assessments_dir, assess_num,
            ))
            for dim_key in DIM_KEYS:
                items.extend(build_dimension_page(
                    dim_key, data, drive_links, assessments_dir, assess_num,
                ))
            items.extend(build_usefulness_page(assess_num))

        # === Section 4: comparative pair for this benchmark (if exists) ===
        comparator_slug = COMPARATOR_MAP.get(bench_slug)
        if comparator_slug and comparator_slug in bench_dict:
            comp_dirs = {d.name: d for d in bench_dict[comparator_slug]}
            for td in tuple_dirs:
                if td.name in comp_dirs:
                    pair_num += 1
                    items.extend(build_comparative_page(
                        td, comp_dirs[td.name], drive_links,
                        assessments_dir, pair_num,
                    ))

    items.extend(build_closing_page())
    return items


def create_google_form(forms_service, title, description, items):
    """Create a form and populate it via batchUpdate."""
    form = forms_service.forms().create(body={
        "info": {"title": title},
    }).execute()
    form_id = form["formId"]

    requests = [
        {
            "updateFormInfo": {
                "info": {"description": description},
                "updateMask": "description",
            },
        },
        {
            "updateSettings": {
                "settings": {"emailCollectionType": "VERIFIED"},
                "updateMask": "emailCollectionType",
            },
        },
    ]
    for idx, item in enumerate(items):
        requests.append({
            "createItem": {
                "item": item,
                "location": {"index": idx},
            },
        })

    forms_service.forms().batchUpdate(
        formId=form_id, body={"requests": requests},
    ).execute()

    return form_id, form["responderUri"]


def _find_insert_index(existing_items, insert_before_title):
    """Find the index of the first item whose title starts with the given prefix."""
    for i, item in enumerate(existing_items):
        title = item.get("title", "")
        if title.startswith(insert_before_title):
            return i
    return None


def patch_form_add_items(forms_service, form_id, new_items, existing_items,
                         insert_before_title=None):
    """Insert items into an existing form at a specific position.

    If insert_before_title is given, finds the first item whose title
    starts with that string and inserts before it. Falls back to
    inserting before the closing page (last 2 items).
    """
    insert_idx = None
    if insert_before_title:
        insert_idx = _find_insert_index(existing_items, insert_before_title)

    if insert_idx is None:
        insert_idx = max(0, len(existing_items) - 2)

    requests = []
    for offset, item in enumerate(new_items):
        requests.append({
            "createItem": {
                "item": item,
                "location": {"index": insert_idx + offset},
            },
        })

    forms_service.forms().batchUpdate(
        formId=form_id, body={"requests": requests},
    ).execute()

    return len(new_items)


def _print_text_diff(live, expected):
    """Print a compact side-by-side diff of two text strings."""
    import difflib
    live_lines = live.splitlines(keepends=True)
    expected_lines = expected.splitlines(keepends=True)
    diff = difflib.unified_diff(
        live_lines, expected_lines,
        fromfile="live", tofile="expected", lineterm="",
    )
    for line in diff:
        print(f"  {line}")


# === Main ===

def main():
    p = argparse.ArgumentParser(
        description="Create Google Forms for expert validation survey",
    )
    p.add_argument(
        "--assessments-dir", default="assessments",
        help="Path to assessments directory (default: assessments/)",
    )
    p.add_argument(
        "--secrets-dir", default=".secrets",
        help="Path to secrets directory",
    )
    p.add_argument(
        "--expert", default=None,
        help="Create form for a single expert ID",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be created without calling the API",
    )
    p.add_argument(
        "--patch", action="store_true",
        help="Add missing comparative sections to an existing form "
             "(requires --expert and an entry in form_urls.json)",
    )
    p.add_argument(
        "--sync-text", action="store_true",
        help="Diff live form text against expected text and update any "
             "discrepancies (titles, descriptions). Use with --dry-run "
             "to preview changes without applying them.",
    )
    args = p.parse_args()

    assessments_dir = Path(args.assessments_dir)
    drive_links = load_drive_links(args.secrets_dir)
    if not drive_links and not args.dry_run:
        print("WARNING: No drive links found — PDF links will be missing.")
        print("Run upload_to_drive.py first, then re-run this script.")
        resp = input("Continue anyway? [y/N] ")
        if resp.lower() != "y":
            sys.exit(0)

    experts = discover_experts(assessments_dir)
    if args.expert:
        if args.expert not in experts:
            print(f"ERROR: {args.expert} not found", file=sys.stderr)
            sys.exit(1)
        experts = {args.expert: experts[args.expert]}

    expert_map_path = Path(args.secrets_dir) / "expert_map.json"
    expert_emails = {}
    if expert_map_path.exists():
        expert_emails = json.loads(expert_map_path.read_text())

    form_urls_path = Path(args.secrets_dir) / "form_urls.json"
    form_urls = {}
    if form_urls_path.exists():
        form_urls = json.loads(form_urls_path.read_text())

    if not args.patch and not args.sync_text:
        for expert_id, benchmarks in experts.items():
            validate_expert_completeness(
                expert_id, benchmarks, drive_links, assessments_dir)

    # === Sync-text mode: diff and update live form text ===
    if args.sync_text:
        if not args.expert:
            print("ERROR: --sync-text requires --expert", file=sys.stderr)
            sys.exit(1)
        expert_id = args.expert
        if expert_id not in form_urls:
            print(f"ERROR: {expert_id} has no existing form in "
                  f"form_urls.json", file=sys.stderr)
            sys.exit(1)

        benchmarks = experts[expert_id]
        form_info = form_urls[expert_id]
        form_id = form_info["form_id"]

        expected_items = build_form_items(
            benchmarks, drive_links, assessments_dir)

        creds = get_credentials(args.secrets_dir)
        forms_service = build("forms", "v1", credentials=creds)
        form = forms_service.forms().get(formId=form_id).execute()
        live_items = form.get("items", [])

        # === Also check welcome page description ===
        live_desc = form.get("info", {}).get("description", "")
        update_requests = []
        if live_desc != WELCOME_DESCRIPTION:
            print("DIFF [Welcome page description]:")
            _print_text_diff(live_desc, WELCOME_DESCRIPTION)
            update_requests.append({
                "updateFormInfo": {
                    "info": {"description": WELCOME_DESCRIPTION},
                    "updateMask": "description",
                },
            })

        # === Match live items to expected items by index ===
        if len(live_items) != len(expected_items):
            print(f"\nWARNING: item count mismatch — live={len(live_items)}, "
                  f"expected={len(expected_items)}. Matching by index up to "
                  f"min({len(live_items)}, {len(expected_items)}).")

        n = min(len(live_items), len(expected_items))
        for i in range(n):
            live = live_items[i]
            want = expected_items[i]
            item_id = live["itemId"]
            live_title = live.get("title", "")
            want_title = want.get("title", "")
            live_description = live.get("description", "")
            want_description = want.get("description", "")

            title_diff = live_title != want_title
            desc_diff = live_description != want_description

            if not title_diff and not desc_diff:
                continue

            label = live_title or want_title or f"item[{i}]"
            update_mask_parts = []
            update_item = {"itemId": item_id}

            # Preserve item type to avoid API error
            if "pageBreakItem" in live:
                update_item["pageBreakItem"] = {}
            elif "questionItem" in live:
                update_item["questionItem"] = live["questionItem"]

            if title_diff:
                print(f"\nDIFF [{label}] title:")
                _print_text_diff(live_title, want_title)
                update_item["title"] = want_title
                update_mask_parts.append("title")

            if desc_diff:
                print(f"\nDIFF [{label}] description:")
                _print_text_diff(live_description, want_description)
                update_item["description"] = want_description
                update_mask_parts.append("description")

            update_requests.append({
                "updateItem": {
                    "item": update_item,
                    "location": {"index": i},
                    "updateMask": ",".join(update_mask_parts),
                },
            })

        if not update_requests:
            print("No text discrepancies found — form is up to date.")
            return

        print(f"\n{len(update_requests)} update(s) needed.")

        if args.dry_run:
            print("[DRY RUN] No changes applied.")
            return

        resp = input("Apply updates? [y/N] ")
        if resp.lower() != "y":
            print("Aborted.")
            return

        forms_service.forms().batchUpdate(
            formId=form_id, body={"requests": update_requests},
        ).execute()
        print(f"Updated {len(update_requests)} item(s) in form {form_id}.")
        return

    # === Patch mode: add missing comparatives to existing form ===
    if args.patch:
        if not args.expert:
            print("ERROR: --patch requires --expert", file=sys.stderr)
            sys.exit(1)
        expert_id = args.expert
        if expert_id not in form_urls:
            print(f"ERROR: {expert_id} has no existing form in "
                  f"form_urls.json", file=sys.stderr)
            sys.exit(1)

        benchmarks = experts[expert_id]
        form_info = form_urls[expert_id]
        form_id = form_info["form_id"]

        all_pairs = _find_comparative_pairs(benchmarks, assessments_dir)

        # Build the expected item sequence to figure out which assessment
        # number follows each comparative (for insertion positioning).
        expected_items = build_form_items(
            benchmarks, drive_links, assessments_dir)
        # Map each comparative title -> the title of the next page break
        # (i.e., where the comparative should appear *before* in the form).
        comp_insert_before = {}
        for i, it in enumerate(expected_items):
            title = it.get("title", "")
            if not title.startswith("Comparative "):
                continue
            for j in range(i + 1, len(expected_items)):
                nxt = expected_items[j]
                if "pageBreakItem" in nxt:
                    comp_insert_before[title] = nxt.get("title", "")
                    break

        creds = get_credentials(args.secrets_dir)
        forms_service = build("forms", "v1", credentials=creds)
        form = forms_service.forms().get(formId=form_id).execute()
        existing_items = form.get("items", [])
        existing_comp_titles = {
            it["title"]
            for it in existing_items
            if it.get("title", "").startswith("Comparative ")
        }

        total_added = 0
        for pair_num, (regional_dir, comp_dir) in enumerate(all_pairs, 1):
            r_scoring = json.loads(
                (regional_dir / "scoring.json").read_text())
            c_scoring = json.loads(
                (comp_dir / "scoring.json").read_text())
            r_name = r_scoring["benchmark"].upper()
            c_name = c_scoring["benchmark"].upper()
            title = f"Comparative {pair_num}: {r_name} vs. {c_name}"

            if title in existing_comp_titles:
                print(f"  Already in form: {title}")
                continue

            insert_before = comp_insert_before.get(title)
            print(f"  Will add: {title}")
            if insert_before:
                print(f"    Insert before: '{insert_before}'")
            else:
                print(f"    Insert before: closing page (fallback)")

            new_items = build_comparative_page(
                regional_dir, comp_dir, drive_links,
                assessments_dir, pair_num,
            )

            if args.dry_run:
                print(f"    [DRY RUN] {len(new_items)} items")
                continue

            # Re-fetch form after each patch since indices shift
            if total_added > 0:
                form = forms_service.forms().get(formId=form_id).execute()
                existing_items = form.get("items", [])

            n = patch_form_add_items(
                forms_service, form_id, new_items, existing_items,
                insert_before_title=insert_before,
            )
            total_added += n

        if total_added == 0 and not args.dry_run:
            print("No missing comparative sections — form is up to date.")
        elif not args.dry_run:
            print(f"\nPatched: added {total_added} items to form {form_id}")
            print(f"  URL: {form_info.get('url', 'N/A')}")
        return

    if args.dry_run:
        print("=== DRY RUN ===\n")
        for expert_id, benchmarks in experts.items():
            email = expert_emails.get(expert_id, "")
            regional = [(s, t) for s, t in benchmarks
                        if s not in COMPARATOR_BENCHMARKS]
            n_tuples = sum(len(t) for _, t in regional)
            items = build_form_items(benchmarks, drive_links, assessments_dir)
            pages = sum(1 for i in items if "pageBreakItem" in i)
            questions = len(items) - pages
            pairs = _find_comparative_pairs(benchmarks, assessments_dir)
            bench_names = [s.replace("_", " ") for s, _ in regional]
            print(f"{expert_id} ({email}):")
            print(f"  Regional benchmarks: {', '.join(bench_names)}")
            print(f"  Regional tuples: {n_tuples}")
            print(f"  Comparative pairs: {len(pairs)}")
            print(f"  Pages: {pages + 1} (incl. welcome)")
            print(f"  Questions: {questions}")
            print()
        return

    creds = get_credentials(args.secrets_dir)
    forms_service = build("forms", "v1", credentials=creds)
    print("Authenticated to Google Forms\n")

    for expert_id, benchmarks in tqdm(list(experts.items()), desc="Creating forms"):
        if expert_id in form_urls:
            print(f"  Skipping {expert_id} (already exists: "
                  f"{form_urls[expert_id]['url']})")
            continue

        email = expert_emails.get(expert_id, "")
        total_tuples = sum(len(t) for _, t in benchmarks)
        bench_names = [s.replace("_", " ") for s, _ in benchmarks]
        print(f"\n  {expert_id} ({email}): {total_tuples} tuples")

        items = build_form_items(benchmarks, drive_links, assessments_dir)

        title = f"Benchmark Validity Assessment Stage 3 ({email or expert_id})"
        form_id, responder_url = create_google_form(
            forms_service,
            title,
            WELCOME_DESCRIPTION,
            items,
        )

        form_urls[expert_id] = {
            "form_id": form_id,
            "url": responder_url,
            "email": email,
            "tuples": total_tuples,
            "benchmarks": bench_names,
        }
        form_urls_path.write_text(json.dumps(form_urls, indent=2) + "\n")
        print(f"  Created: {responder_url}")

    print(f"\nDone. Form URLs saved to {form_urls_path}")
    for eid, info in form_urls.items():
        print(f"  {eid} ({info.get('email', '')}): {info['url']}")


if __name__ == "__main__":
    main()
