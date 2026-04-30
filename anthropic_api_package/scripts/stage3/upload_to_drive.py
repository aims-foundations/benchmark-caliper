#!/usr/bin/env python3
"""upload_to_drive.py -- Upload expert review PDFs to Google Drive.

Uploads all PDFs from assessments/{expert}/{tuple}/pdfs/ into a nested
Google Drive folder structure, sets anyone-with-link sharing, and writes
a link mapping JSON for the form generator.

Usage:
    python3 scripts/stage3/upload_to_drive.py
    python3 scripts/stage3/upload_to_drive.py --force
    python3 scripts/stage3/upload_to_drive.py --tuple assessments/expert_.../slug/
"""

import argparse
import json
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

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

ROOT_FOLDER_NAME = "validity-expert-review"

PDF_KEYS = ["summary", "io", "ic", "if", "oo", "oc", "of"]


# === Auth ===

def get_credentials(secrets_dir):
    """Load or refresh OAuth credentials."""
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
        print(f"Token saved to {token_path}")

    return creds


# === Drive helpers ===

def find_or_create_folder(service, name, parent_id=None):
    """Find an existing folder by name under parent, or create it."""
    q = (
        f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder'"
        f" and trashed = false"
    )
    if parent_id:
        q += f" and '{parent_id}' in parents"

    results = service.files().list(
        q=q, fields="files(id, name)", pageSize=1,
    ).execute()
    files = results.get("files", [])

    if files:
        return files[0]["id"]

    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        metadata["parents"] = [parent_id]

    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def upload_file(service, local_path, parent_id):
    """Upload a PDF file to a Drive folder, return file ID."""
    metadata = {
        "name": local_path.name,
        "parents": [parent_id],
    }
    media = MediaFileUpload(str(local_path), mimetype="application/pdf")
    f = service.files().create(
        body=metadata, media_body=media, fields="id",
    ).execute()
    return f["id"]


def set_anyone_with_link(service, file_id):
    """Set anyone-with-link viewer permission on a file."""
    service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
        fields="id",
    ).execute()


def get_web_view_link(service, file_id):
    """Get the webViewLink for a file."""
    f = service.files().get(fileId=file_id, fields="webViewLink").execute()
    return f["webViewLink"]


# === Tuple discovery (matches generate_expert_pdfs.py) ===

def discover_tuples(assessments_dir):
    """Find all assessment tuple directories that have a pdfs/ subdirectory."""
    assessments_dir = Path(assessments_dir)
    tuples = []
    for expert_dir in sorted(assessments_dir.glob("expert_*")):
        if not expert_dir.is_dir():
            continue
        for slug_dir in sorted(expert_dir.iterdir()):
            if slug_dir.is_dir() and (slug_dir / "pdfs").is_dir():
                tuples.append(slug_dir)
    return tuples


def tuple_key(tuple_dir, assessments_dir):
    """Relative path key for the link map: expert_dir/slug."""
    return str(tuple_dir.relative_to(assessments_dir))


# === Main upload logic ===

def upload_tuple(service, tuple_dir, assessments_dir, folder_cache,
                 link_map, force):
    """Upload all PDFs for one tuple. Returns count of files uploaded."""
    tkey = tuple_key(tuple_dir, assessments_dir)
    pdfs_dir = tuple_dir / "pdfs"

    # === Folder hierarchy: root / expert_dir / tuple_slug ===
    expert_dir_name = tuple_dir.parent.name
    tuple_slug = tuple_dir.name

    if "root" not in folder_cache:
        folder_cache["root"] = find_or_create_folder(service, ROOT_FOLDER_NAME)
    root_id = folder_cache["root"]

    expert_cache_key = f"expert:{expert_dir_name}"
    if expert_cache_key not in folder_cache:
        folder_cache[expert_cache_key] = find_or_create_folder(
            service, expert_dir_name, root_id,
        )
    expert_folder_id = folder_cache[expert_cache_key]

    tuple_cache_key = f"tuple:{expert_dir_name}/{tuple_slug}"
    if tuple_cache_key not in folder_cache:
        folder_cache[tuple_cache_key] = find_or_create_folder(
            service, tuple_slug, expert_folder_id,
        )
    tuple_folder_id = folder_cache[tuple_cache_key]

    # === Upload each PDF ===
    existing = link_map.get(tkey, {})
    uploaded = 0

    for key in PDF_KEYS:
        pdf_path = pdfs_dir / f"{key}.pdf"
        if not pdf_path.exists():
            continue

        if key in existing and not force:
            continue

        file_id = upload_file(service, pdf_path, tuple_folder_id)
        set_anyone_with_link(service, file_id)
        link = get_web_view_link(service, file_id)

        if tkey not in link_map:
            link_map[tkey] = {}
        link_map[tkey][key] = link
        uploaded += 1

    return uploaded


def main():
    p = argparse.ArgumentParser(
        description="Upload expert review PDFs to Google Drive",
    )
    p.add_argument(
        "--assessments-dir", default="assessments",
        help="Path to assessments directory (default: assessments/)",
    )
    p.add_argument(
        "--secrets-dir", default=".secrets",
        help="Path to secrets directory with credentials.json/token.json",
    )
    p.add_argument(
        "--tuple", default=None,
        help="Process a single tuple directory instead of all",
    )
    p.add_argument(
        "--force", action="store_true",
        help="Re-upload files even if already in link map",
    )
    args = p.parse_args()

    # === Load existing link map ===
    secrets_dir = Path(args.secrets_dir)
    link_map_path = secrets_dir / "drive_links.json"
    if link_map_path.exists():
        link_map = json.loads(link_map_path.read_text())
        print(f"Loaded existing link map ({len(link_map)} tuples)")
    else:
        link_map = {}

    # === Auth ===
    creds = get_credentials(args.secrets_dir)
    service = build("drive", "v3", credentials=creds)
    print("Authenticated to Google Drive")

    # === Discover tuples ===
    assessments_dir = Path(args.assessments_dir)
    if args.tuple:
        td = Path(args.tuple)
        if not (td / "pdfs").is_dir():
            print(f"ERROR: {td / 'pdfs'} not found", file=sys.stderr)
            sys.exit(1)
        tuples = [td]
    else:
        tuples = discover_tuples(assessments_dir)
        if not tuples:
            print(f"No tuples with pdfs/ found in {assessments_dir}")
            sys.exit(1)

    # === Count work ===
    skip_count = 0
    work_tuples = []
    for td in tuples:
        tkey = tuple_key(td, assessments_dir)
        existing = link_map.get(tkey, {})
        pdfs_present = [k for k in PDF_KEYS if (td / "pdfs" / f"{k}.pdf").exists()]
        needs_upload = [k for k in pdfs_present if k not in existing or args.force]
        if needs_upload:
            work_tuples.append(td)
        else:
            skip_count += 1

    if skip_count > 0:
        print(f"Skipping {skip_count} tuples (already uploaded, use --force to re-upload)")
    print(f"Uploading PDFs for {len(work_tuples)} tuples")

    if not work_tuples:
        print("Nothing to upload")
        return

    # === Upload ===
    folder_cache = {}
    total_uploaded = 0

    for td in tqdm(work_tuples, desc="Uploading"):
        n = upload_tuple(
            service, td, assessments_dir, folder_cache, link_map, args.force,
        )
        total_uploaded += n
        # Save incrementally after each tuple (crash-safe)
        link_map_path.write_text(json.dumps(link_map, indent=2) + "\n")

    print(f"Done: {total_uploaded} files uploaded across {len(work_tuples)} tuples")
    print(f"Link map saved to {link_map_path}")


if __name__ == "__main__":
    main()
