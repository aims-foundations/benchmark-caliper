#!/usr/bin/env python3
"""One-off fix: update old ASAP_PLUS_PLUS items (243-253) with correct text,
then delete the duplicate ASAP++ items (254-264) from the MENA expert form.

Usage (user-run only):
    python3 scripts/stage3/fix_mena_duplicates.py --secrets-dir .secrets
    python3 scripts/stage3/fix_mena_duplicates.py --secrets-dir .secrets --dry-run
"""

import argparse
import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

FORM_ID = "1e9SohjNM8d7EkHgDLVk9OEFEDC04dNkxP5vXQsQsgYw"

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/forms.body",
]

COMP_LINK = "https://drive.google.com/file/d/1bX15w26oQ87ZFPhXdyj-UYE7TaPxq2ed/view?usp=drivesdk"
PAPER_URL = "https://aclanthology.org/L18-1187/"

NEW_DESCRIPTION = (
    "The pipeline assessed two benchmarks for the same deployment "
    "context: LAILA (a benchmark proposed by you) and "
    f"ASAP++ ({PAPER_URL}) (a benchmark we selected for comparison). Both "
    "were evaluated across the same six validity dimensions. The "
    "comparative PDF below presents excerpts from each benchmark's "
    "individual assessment for this context — please review it "
    "before answering the questions.\n\n"
    "LAILA: 2.2/5 avg | ASAP++: 1.0/5 avg\n"
    "Context: Arab High-School Arabic Essay Feedback (Qatar Primary)\n\n"
    f"▶ Open the Comparative PDF: {COMP_LINK}"
)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--secrets-dir", default=".secrets")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    creds = Credentials.from_authorized_user_file(
        str(Path(args.secrets_dir) / "token.json"), SCOPES)
    svc = build("forms", "v1", credentials=creds)

    form = svc.forms().get(formId=FORM_ID).execute()
    items = form.get("items", [])
    print(f"Total items: {len(items)}")

    # === Verify expected state ===
    old_page = items[243]
    new_page = items[254]
    assert "ASAP_PLUS_PLUS" in old_page.get("title", ""), \
        f"Expected ASAP_PLUS_PLUS at [243], got: {old_page.get('title')}"
    assert "ASAP++" in new_page.get("title", ""), \
        f"Expected ASAP++ at [254], got: {new_page.get('title')}"

    # === Build update requests for old items (243-253) ===
    old_titles = {
        243: "Comparative 2: LAILA vs. ASAP++",
        244: "The pipeline scored LAILA at an average of 2.2/5 and "
             "ASAP++ at 1.0/5 for this deployment context. Does this "
             "relative ordering match your expert judgment?",
        245: "For Input Ontology (IO), the pipeline scored LAILA at 2/5 and "
             "ASAP++ at 1/5. Does this relative ordering match your judgment?",
        246: "For Input Content (IC), the pipeline scored LAILA at 2/5 and "
             "ASAP++ at 1/5. Does this relative ordering match your judgment?",
        247: "For Input Form (IF), the pipeline scored LAILA at 4/5 and "
             "ASAP++ at 1/5. Does this relative ordering match your judgment?",
        248: "For Output Ontology (OO), the pipeline scored LAILA at 1/5 and "
             "ASAP++ at 1/5. Does this relative ordering match your judgment?",
        249: "For Output Content (OC), the pipeline scored LAILA at 3/5 and "
             "ASAP++ at 1/5. Does this relative ordering match your judgment?",
        250: "For Output Form (OF), the pipeline scored LAILA at 1/5 and "
             "ASAP++ at 1/5. Does this relative ordering match your judgment?",
    }

    requests = []

    # Update page break title + description (must include pageBreakItem)
    requests.append({
        "updateItem": {
            "item": {
                "itemId": items[243]["itemId"],
                "title": old_titles[243],
                "description": NEW_DESCRIPTION,
                "pageBreakItem": {},
            },
            "location": {"index": 243},
            "updateMask": "title,description",
        },
    })

    # Update question titles (244-250) — must include questionItem
    for idx in range(244, 251):
        requests.append({
            "updateItem": {
                "item": {
                    "itemId": items[idx]["itemId"],
                    "title": old_titles[idx],
                    "questionItem": items[idx]["questionItem"],
                },
                "location": {"index": idx},
                "updateMask": "title",
            },
        })
    # Items 251-253 don't need title changes

    # === Delete new duplicate items (254-264) ===
    # Must delete in reverse order so indices don't shift
    for idx in range(264, 253, -1):
        requests.append({
            "deleteItem": {
                "location": {"index": idx},
            },
        })

    # === Report ===
    print(f"\nUpdates: 8 items (243-250)")
    print(f"Deletes: 11 items (254-264)")
    print(f"Total requests: {len(requests)}")

    for r in requests:
        if "updateItem" in r:
            idx = r["updateItem"]["location"]["index"]
            old = items[idx].get("title", "")
            new = r["updateItem"]["item"].get("title", "")
            if old != new:
                print(f"\n  UPDATE [{idx}]:")
                print(f"    old: {old}")
                print(f"    new: {new}")
            mask = r["updateItem"].get("updateMask", "")
            if "description" in mask:
                print(f"    + new description (comparative intro)")
        elif "deleteItem" in r:
            idx = r["deleteItem"]["location"]["index"]
            print(f"  DELETE [{idx}]: {items[idx].get('title', '')}")

    if args.dry_run:
        print("\n[DRY RUN] No changes applied.")
        return

    print()
    resp = input("Apply? [y/N] ")
    if resp.lower() != "y":
        print("Aborted.")
        return

    svc.forms().batchUpdate(
        formId=FORM_ID, body={"requests": requests},
    ).execute()
    print(f"\nDone. Form now has {len(items) - 11} items.")


if __name__ == "__main__":
    main()
