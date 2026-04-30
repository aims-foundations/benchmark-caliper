#!/usr/bin/env python3
"""create_expert_forms.py -- Create Google Forms for expert validation survey.

Creates one Google Form per expert with companion PDF links for each
assessment tuple. Forms follow the structure defined in
stage3_planning/expert_validation_survey_spec_v3.md.

Sections 1-3 (primary review) are fully implemented.
Section 4 (comparative) is a placeholder until comparative PDFs exist.

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


def build_context_page(data, drive_links, assessments_dir, tuple_num):
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
        _page_break(f"Tuple {tuple_num}: {benchmark} — {region}", description),
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
            "The 'What Else You Need' recommendations would help a practitioner "
            "plan supplementary evaluation."
        ),
        _text(
            "Any overall comments on the assessment's quality, framing, or "
            "usefulness?"
        ),
    ]


def build_dimension_page(dim_key, data, drive_links, assessments_dir, tuple_num):
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
        _page_break(f"Tuple {tuple_num} — {dim_label}", description),
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
            "What important considerations, if any, are missing or "
            "mischaracterized for this dimension? Please be specific about what "
            "was overlooked."
        ),
    ]


def build_usefulness_page(tuple_num):
    """Section 3: Usefulness & Actionability (one page)."""
    return [
        _page_break(
            f"Tuple {tuple_num} — Usefulness & Actionability",
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
            "The remediation recommendations are specific enough to act on."
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
    "Estimated time: 3–4 hours total (~45 min per primary tuple, "
    "~15–20 min per comparative assessment).\n\n"
    "Your responses are saved automatically as you progress."
)


def build_form_items(benchmarks, drive_links, assessments_dir):
    """Build all form items for one expert. Returns list of item dicts."""
    items = []
    tuple_num = 0

    for _bench_slug, tuple_dirs in benchmarks:
        for td in tuple_dirs:
            tuple_num += 1
            data = load_tuple_data(td)
            data["scoring"]["_tuple_dir"] = td

            items.extend(build_context_page(
                data, drive_links, assessments_dir, tuple_num,
            ))
            for dim_key in DIM_KEYS:
                items.extend(build_dimension_page(
                    dim_key, data, drive_links, assessments_dir, tuple_num,
                ))
            items.extend(build_usefulness_page(tuple_num))

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

    if args.dry_run:
        print("=== DRY RUN ===\n")
        for expert_id, benchmarks in experts.items():
            email = expert_emails.get(expert_id, "")
            total_tuples = sum(len(t) for _, t in benchmarks)
            items = build_form_items(benchmarks, drive_links, assessments_dir)
            pages = sum(1 for i in items if "pageBreakItem" in i)
            questions = len(items) - pages
            bench_names = [s.replace("_", " ") for s, _ in benchmarks]
            print(f"{expert_id} ({email}):")
            print(f"  Benchmarks: {', '.join(bench_names)}")
            print(f"  Tuples: {total_tuples}")
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

        form_id, responder_url = create_google_form(
            forms_service,
            "Benchmark Validity Assessment Review",
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
