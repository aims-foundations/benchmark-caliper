"""Portable review documents derived from one goal-pipeline export snapshot.

The JSON is the complete record. HTML and CSV are views of that record, with
selected IDs joined to their screening evidence rather than copied by position.
This module performs no model calls, network access, or source-data mutations.
"""

import csv
from html import escape
from io import TextIOWrapper
import json
import re
from tempfile import SpooledTemporaryFile
import unicodedata
from zipfile import ZIP_DEFLATED, ZipFile

from website.server import construction_composition, streaming_json


DIMENSIONS = (
    ("input_ontology", "Input ontology"), ("input_content", "Input content"),
    ("input_form", "Input form"), ("output_ontology", "Output ontology"),
    ("output_content", "Output content"), ("output_form", "Output form"),
)
ANSWERS = (
    ("task", "What will the AI system do?"), ("users", "Who will use it?"),
    ("inputs", "What inputs will it receive?"), ("outputs", "What should its responses look like?"),
    ("success", "What counts as a successful response?"),
    ("constraints", "What constraints or failures matter?"),
)
STOP_REASONS = {
    "candidate_limit": "The total candidate limit was reached.",
    "queues_exhausted": "No unseen candidates remain in the saved retrieval queues.",
    "cost_limit": "The additional screening cost ceiling was reached, or cannot cover the next reserved call.",
}
STAGES = {
    "requirements": "Step 2: Requirements extraction", "grounding": "Step 3: O*NET grounding",
    "retrieval": "Step 4: Benchmark retrieval", "screening": "Step 5: Initial screening",
    "selection": "Step 6: Collection selection", "adaptive": "Step 7: Adaptive screening",
}
STYLE = """
:root { color-scheme: light; font: 16px/1.6 system-ui, sans-serif; color: #243346; background: #eef2f5; }
* { box-sizing: border-box; } body { margin: 0; } main { max-width: 1100px; margin: auto; padding: 3rem 2rem; }
header { border-top: 5px solid #27665e; padding-top: 1rem; } h1 { line-height: 1.15; font-size: 2.3rem; }
h2 { margin-top: 2.4rem; color: #17483f; } h3, h4 { margin-bottom: .5rem; }
p, ul, dl { margin-top: .5rem; } .eyebrow, .muted { color: #536579; }
.eyebrow { text-transform: uppercase; letter-spacing: .08em; font-size: .8rem; font-weight: 700; }
.card, .notice { background: #fff; border: 1px solid #d6dfe5; border-radius: .6rem; padding: 1.2rem; margin: 1rem 0; }
.notice { background: #fff6e4; border-left: 5px solid #a76b10; } .success { background: #eaf5f1; border-left-color: #27665e; }
.preserve, blockquote { white-space: pre-wrap; overflow-wrap: anywhere; }
blockquote { border-left: 3px solid #abc5bd; padding-left: 1rem; margin-left: 0; color: #425b55; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: .9rem; }
th, td { padding: .65rem; text-align: left; vertical-align: top; border-bottom: 1px solid #d6dfe5; overflow-wrap: anywhere; }
th { background: #e6eeeb; } .table-wrap { overflow-x: auto; }
dt { font-weight: 700; } dd { margin: 0 0 .5rem; } code { overflow-wrap: anywhere; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; font-size: .8rem; background: #f3f5f7; padding: 1rem; }
details { border-top: 1px solid #d6dfe5; padding: .8rem 0; } summary { cursor: pointer; font-weight: 600; }
footer { margin-top: 3rem; border-top: 1px solid #d6dfe5; padding-top: 1rem; }
@media (max-width: 650px) { main { padding: 1.5rem 1rem; } h1 { font-size: 1.8rem; } }
@media print {
  :root { font-size: 11pt; background: white; color: black; } main { max-width: none; padding: 0; }
  .card, .notice { border-radius: 0; } h2, h3, h4, summary { break-after: avoid; }
  tr, blockquote { break-inside: avoid; } .table-wrap { overflow: visible; }
  details > * { display: block !important; } details::details-content { content-visibility: visible; }
  pre { font-size: 8pt; } header { border-top-width: 2px; }
}
"""


def _text(value, fallback="Unknown") -> str:
    return fallback if value is None else str(value)


def _html(value, fallback="Unknown") -> str:
    return escape(_text(value, fallback), quote=True)


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)


def _details(label, value) -> str:
    return f"<details><summary>{_html(label)}</summary><pre>{_html(_json(value))}</pre></details>"


def _list(values) -> str:
    return "<ul>" + "".join(f'<li class="preserve">{_html(value)}</li>' for value in values) + "</ul>"


def _table(headers, rows) -> str:
    return ('<div class="table-wrap"><table><thead><tr>'
            + "".join(f'<th scope="col">{_html(header)}</th>' for header in headers)
            + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{_html(cell)}</td>" for cell in row) + "</tr>" for row in rows)
            + "</tbody></table></div>")


def _supported(value) -> str:
    value = value or {}
    text = f'<p class="preserve">{_html(value.get("text"), "Unspecified in the original answers.")}</p>'
    for reference in value.get("evidence", []):
        text += (f'<blockquote>{_html(reference.get("quote"))}'
                 f'<br><small>Source answer: {_html(reference.get("answer_id"))}</small></blockquote>')
    return text


def _finding(value) -> str:
    value = value or {}
    text = f'<p class="preserve">{_html(value.get("justification"), "No explanation recorded.")}</p>'
    if value.get("evidence"):
        text += "<h5>Model-provided item evidence</h5>" + _list(value["evidence"])
    if value.get("information_gaps"):
        text += "<h5>Information gaps</h5>" + _list(value["information_gaps"])
    return text


def _task_names(snapshot) -> dict:
    return {facet["facet_id"]: _text((facet.get("task") or {}).get("text"), facet["facet_id"])
            for facet in (snapshot.get("requirements") or {}).get("task_facets", [])}


def _selected(snapshot) -> list[tuple[dict, dict]]:
    selection = snapshot.get("selection") or {}
    compact = {item["item_id"]: item for item in selection.get("items", [])}
    evidence = {item["item_id"]: item for item in (snapshot.get("screening") or {}).get("items", [])}
    # The recorded ID order is the collection order. Never zip unrelated lists.
    identifiers = selection.get("selected_item_ids", list(compact))
    return [(compact.get(key, {"item_id": key}), evidence.get(key, {})) for key in identifiers]


def _preview(item, *, limit=None) -> str:
    value = item.get("question_text") or item.get("search_text")
    if not value:
        evidence = item.get("evidence") or {}
        value = _json(evidence["item"]) if "item" in evidence else "No item text is recorded."
    return value if limit is None or len(value) <= limit else value[:limit] + "…"


def _sources(item) -> str:
    values = []
    for source in item.get("sources", []):
        # Include every provenance field, including full pinned commit and row.
        values.append("; ".join(f"{key}: {_text(value)}" for key, value in source.items()))
    return "\n".join(values)


def package_filename(snapshot: dict) -> str:
    """Return an ASCII attachment name; never interpolate user text as a path."""
    metadata = snapshot.get("metadata") or {}

    def slug(value, limit):
        ascii_text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
        return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")[:limit].rstrip("-")

    name = slug(metadata.get("run_name") or "benchmark-results", 64) or "benchmark-results"
    date_match = re.match(r"\d{4}-\d{2}-\d{2}", str(metadata.get("created_at", "")))
    date = date_match[0] if date_match else "undated"
    run_id = slug(snapshot.get("run_id", "run"), 12) or "run"
    partial = "-partial" if metadata.get("result_state") == "partial" else ""
    return f"{name}_{date}_{run_id}{partial}.zip"


def _summary(snapshot) -> str:
    metadata = snapshot.get("metadata") or {}
    selection = snapshot.get("selection")
    adaptive = snapshot.get("adaptive") or {}
    state = metadata.get("result_state", "partial")
    labels = {"partial": "Partial result", "stage_complete": "Stage complete", "frozen": "Collection frozen"}
    title = metadata.get("run_name") or "Benchmark construction results"
    text = (f'<header><p class="eyebrow">Benchmark construction record</p><h1>{_html(title)}</h1>'
            f'<p>{_html(STAGES.get(snapshot.get("mode"), snapshot.get("mode")))}. {_html(labels.get(state, state))}</p>'
            f'<p class="muted">Run <code>{_html(snapshot.get("run_id"))}</code><br>'
            f'Created {_html(metadata.get("created_at"))}. Exported {_html(metadata.get("exported_at"))}</p></header>')
    if state == "partial":
        text += ('<div class="notice"><strong>Partial result. The current stage is unfinished.</strong>'
                 '<p>Completed evidence and any last accepted collection are included. '
                 'Pending work has not produced a frozen collection.</p></div>')
    elif state == "stage_complete":
        text += ('<div class="notice"><strong>This stage is complete.</strong>'
                 '<p>The full automated construction pipeline has not produced a frozen collection in this run.</p></div>')
    if selection and not selection.get("fully_satisfied"):
        text += ('<div class="notice"><strong>Coverage remains incomplete.</strong>'
                 '<p>Unmet or unresolved requirements remain in this collection. Stopping does not lower the original requirements.</p>'
                 + _list(selection.get("gaps") or ["Some coverage requirements remain unmet or unresolved."]) + "</div>")
    elif state == "frozen":
        text += '<div class="notice success"><strong>The automated collection is frozen.</strong></div>'
    if snapshot.get("message"):
        text += f'<p class="preserve">{_html(snapshot["message"])}</p>'
    if selection:
        text += (f'<p><strong>Selected items:</strong> {_html(selection.get("selected_count", len(_selected(snapshot))))}'
                 f' / {_html(selection.get("limit", 30))} total. <strong>Eligible items:</strong> {_html(selection.get("eligible_count"))}'
                 f'. <strong>Total quality Q:</strong> {_html(selection.get("total_quality"))}</p>'
                 '<p class="muted">Q is the mean of the four gated ratings for each item; total Q sums these item scores.</p>')
    else:
        text += '<p><strong>No benchmark collection has been selected at this stage.</strong></p>'
    if adaptive.get("stop_reason"):
        reason = adaptive["stop_reason"]
        text += f'<p><strong>Stopping reason:</strong> {_html(STOP_REASONS.get(reason, reason))}</p>'
    text += '<p class="muted">This is an automated benchmark-construction record. Target-system performance and separate human validation are not included.</p>'
    return text


def _coverage(snapshot) -> str:
    selection = snapshot.get("selection") or {}
    requirements = snapshot.get("requirements") or {}
    names = _task_names(snapshot)
    text = "<section><h2>Task and quota coverage</h2>"
    if not selection:
        return text + "<p>Collection coverage has not been calculated at this stage.</p></section>"
    text += _table(["Required task", "Minimum", "Eligible", "Selected", "Shortfall"], [
        [names.get(row["facet_id"], row["facet_id"]), row.get("minimum"), row.get("eligible_count"),
         row.get("selected_count"), row.get("shortfall")] for row in selection.get("task_coverage", [])])
    quotas = requirements.get("coverage_requirements", [])
    unresolved = selection.get("unresolved_requirement_indices", [])
    quota_rows = []
    for row in selection.get("quota_coverage", []):
        index = row["requirement_index"]
        description = quotas[index]["requirement"]["text"] if 0 <= index < len(quotas) else f"Coverage requirement {index + 1}"
        status = "Unresolved" if row.get("minimum_items") is None or index in unresolved else "Unmet" if row.get("shortfall") else "Satisfied"
        quota_rows.append([description, _text(row.get("minimum_items"), "Unresolved"), row.get("eligible_count"),
                           row.get("selected_count"), _text(row.get("shortfall"), "Unresolved"), status])
    text += (_table(["Coverage requirement", "Minimum", "Eligible", "Selected", "Shortfall", "Status"], quota_rows)
             if quota_rows else "<p>No explicit collection quotas were recorded.</p>")
    return text + "</section>"


def _selected_item(compact, item, index, snapshot) -> str:
    names = _task_names(snapshot)
    key = compact["item_id"]
    text = f'<article class="card" id="selected-item-{_html(key)}"><h3>Selected item {index + 1}</h3><p class="muted">Item ID: <code>{_html(key)}</code></p>'
    if not item:
        return text + '<p class="notice">The saved screening evidence for this item is unavailable. Consult results.json for the recorded selection.</p></article>'
    assessment = item.get("assessment") or {}
    task = assessment.get("task") or {}
    matched = compact.get("matched_facet_ids", task.get("matched_facet_ids", []))
    text += (f'<p class="preserve">{_html(_preview(item))}</p>'
             f'<p><strong>Quality Q:</strong> {_html(compact.get("quality_score"))} / 5. '
             f'<strong>Screening gate:</strong> {_html((item.get("gate") or {}).get("status"))}</p>'
             f'<p><strong>Matched tasks:</strong> {_html("; ".join(names.get(facet, facet) for facet in matched), "None")}</p>'
             f'<p class="preserve"><strong>Sources:</strong> {_html(_sources(item), "None recorded")}</p>'
             '<h4>Six screening ratings</h4>')
    ratings = assessment.get("ratings") or {}
    text += _table(["Dimension", "Score / 5"], [[label, _text((ratings.get(key) or {}).get("score"))] for key, label in DIMENSIONS])
    text += '<details><summary>Task interpretation, ratings, and supporting evidence</summary><h4>Task actually tested</h4>'
    text += f'<p class="preserve">{_html(task.get("decision"), "Unresolved")}</p>' + _finding(task)
    if item.get("gate"):
        text += "<h4>Screening gate reasons</h4>" + _list(item["gate"].get("reasons", []))
    for key, label in DIMENSIONS:
        text += f"<h4>{label}</h4>" + _finding(ratings.get(key))
    text += "</details>"
    quotas = (snapshot.get("requirements") or {}).get("coverage_requirements", [])
    if assessment.get("coverage"):
        text += '<details><summary>Item coverage findings</summary>'
        for finding in assessment["coverage"]:
            index = finding["requirement_index"]
            description = quotas[index]["requirement"]["text"] if 0 <= index < len(quotas) else f"Requirement {index + 1}"
            satisfied = finding.get("satisfied")
            label = "Unresolved" if satisfied is None else "Satisfied" if satisfied else "Not satisfied"
            text += f"<h4>{_html(description)}. {label}</h4>" + _finding(finding)
        text += "</details>"
    text += _details("Complete original item row", (item.get("evidence") or {}).get("item", item.get("evidence")))
    text += _details("Source provenance and acquisition", {key: item.get(key) for key in (
        "sources", "evidence_hash", "acquisition", "rank", "screened_run_id", "usage")})
    return text + "</article>"


def _requirements(snapshot) -> str:
    text = "<section><h2>Goal and extracted requirements</h2>"
    requirements = snapshot.get("requirements")
    if requirements:
        for key, label in (("workflow", "Workflow"), ("primary_user", "Primary user"),
                           ("input_types", "Input types"), ("output_types", "Output types"), ("authority", "Authority")):
            text += f"<h3>{label}</h3>" + _supported(requirements.get(key))
        for index, facet in enumerate(requirements.get("task_facets", [])):
            text += f'<article class="card"><h3>Task {index + 1}. {_html(facet["facet_id"])}</h3>'
            text += _supported(facet.get("task"))
            text += "<h4>Required input evidence</h4>" + _supported(facet.get("required_input_evidence"))
            text += "<h4>Required output behavior</h4>" + _supported(facet.get("required_output_behavior"))
            text += f'<p><strong>Essential:</strong> {_html(facet.get("essential"))}</p></article>'
        text += "<h3>Explicit coverage requirements</h3>"
        for index, quota in enumerate(requirements.get("coverage_requirements", [])):
            text += f"<h4>Requirement {index + 1}</h4>" + _supported(quota.get("requirement"))
            text += f'<p>Minimum items: {_html(quota.get("minimum_items"), "Unspecified")}</p>'
        if not requirements.get("coverage_requirements"):
            text += "<p>No explicit coverage requirements were extracted.</p>"
        text += "<h3>Unresolved details</h3>"
        text += _list(requirements["unresolved_details"]) if requirements.get("unresolved_details") else "<p>No unresolved details were reported by extraction.</p>"
    else:
        text += "<p>No validated requirements are available in this snapshot.</p>"
    text += "<h3>Original deployment answers</h3>"
    for index, (key, label) in enumerate(ANSWERS):
        text += f'<h4>Answer {index + 1}. {label}</h4><p class="preserve">{_html((snapshot.get("deployment") or {}).get(key) or "No answer supplied.")}</p>'
    return text + "</section>"


def _history(snapshot) -> str:
    text = "<section><h2>Construction history</h2>"
    screening = snapshot.get("screening") or {}
    allocation = screening.get("allocation") or {}
    items = screening.get("items", [])
    if screening:
        text += (f'<p><strong>Initial allocation:</strong> {_html(allocation.get("allocated"))} of '
                 f'{_html(allocation.get("budget"))} candidates. <strong>All saved screening assessments:</strong> '
                 f'{sum(item.get("status") == "complete" for item in items)} valid, '
                 f'{sum(item.get("status") == "error" for item in items)} errors.</p>')
        text += _details("Initial screening allocation", allocation)
    adaptive = snapshot.get("adaptive") or {}
    names = _task_names(snapshot)
    for batch in adaptive.get("batches", []):
        title = "Initial screening" if batch.get("kind") == "initial" else f'Adaptive batch {batch.get("number")}'
        text += (f'<details><summary>{_html(title)}. {len(batch.get("item_ids", []))} candidates. '
                 f'{_html(batch.get("status"))}</summary>')
        if batch.get("facet_id"):
            text += f'<p>Task: {_html(names.get(batch["facet_id"], batch["facet_id"]))}</p>'
        if batch.get("status") == "committed":
            retained = sum(outcome.get("retained") is True for outcome in batch.get("outcomes", []))
            text += f'<p>{retained} newly screened items retained after this batch; {len(batch.get("selected_item_ids", []))} items in the resulting collection.</p>'
        else:
            text += "<p>Pending batch outcomes have not updated the queue statistics.</p>"
        if batch.get("unresolved_item_ids"):
            text += f'<p>{len(batch["unresolved_item_ids"])} acquired candidates lack valid assessments and are excluded from the batch outcomes.</p>'
        text += f'<pre>{_html(_json(batch))}</pre></details>'
    if adaptive:
        text += _details("Queue statistics and decisions", adaptive.get("queue_statistics"))
    text += "<h3>Usage and cost scope</h3>"
    if snapshot.get("stage_usage"):
        text += "<p>Recorded usage by run preserves earlier stages and repeated or resumed runs. Missing usage is shown as unknown; this table does not estimate an overall pipeline dollar cost.</p>"
        text += _table(["Stage", "Run ID", "Status", "Input tokens", "Output tokens", "Total tokens"], [
            [STAGES.get(run.get("mode"), run.get("mode")), run.get("run_id"), run.get("status"),
             (run.get("usage") or {}).get("input_tokens"), (run.get("usage") or {}).get("output_tokens"),
             (run.get("usage") or {}).get("total_tokens")] for run in snapshot["stage_usage"]])
        text += _details("Complete recorded stage usage", snapshot["stage_usage"])
    text += "<p>Top-level token usage covers the current run only. It is not the total for all pipeline stages or previous runs.</p>"
    text += _details("Current run token usage", snapshot.get("usage"))
    if adaptive:
        cost = adaptive.get("cost") or {}
        text += ("<p>Adaptive cost estimates cover Step 7 calls and retries only. Earlier stages are excluded. "
                 "Estimates and reservations are not a final provider invoice.</p>"
                 f'<p>Estimated spent (USD): {_html(cost.get("spent_usd"), "Not priced")}. '
                 f'Reserved (USD): {_html(cost.get("reserved_usd"), "Not priced")}</p>')
        if cost.get("unknown_attempts"):
            text += f'<p class="notice">Usage is unknown for {_html(cost["unknown_attempts"])} attempts; those attempts may still incur charges.</p>'
        text += _details("Adaptive settings, cost policy, and call attempts", {
            key: adaptive.get(key) for key in ("policy", "settings", "cost", "attempts")})
    if snapshot.get("extraction"):
        text += _details("Extraction model, prompt, schema, and evidence", snapshot["extraction"])
    if snapshot.get("grounding"):
        text += _details("O*NET records, mappings, passages, and applicability", snapshot["grounding"])
    if snapshot.get("retrieval"):
        text += _details("Retrieval queries, scope, policy, and statistics", {
            key: value for key, value in snapshot["retrieval"].items() if key not in {"rankings", "queues"}})
        text += "<p>Complete retrieval candidates and queues, including rejected and unselected evidence, are retained in results.json.</p>"
    if screening:
        text += _details("Screening model, prompt, schema, and policy", {key: screening.get(key) for key in ("model", "policy")})
    if snapshot.get("selection"):
        text += _details("Selection policy, exclusions, and solver result", {key: snapshot["selection"].get(key) for key in (
            "policy", "excluded_counts", "solver", "preserved_coverage")})
    text += _details("Run metadata", {key: snapshot.get(key) for key in (
        "run_id", "source_run_id", "selection_run_id", "mode", "status", "model", "reasoning_effort", "metadata")})
    return text + "</section>"


def _report(snapshot, *, expand=None, composition_annotations=None):
    title = (snapshot.get("metadata") or {}).get("run_name") or "Benchmark construction results"
    yield ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1">'
           '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'">'
           f'<title>{_html(title)}</title><style>{STYLE}</style></head><body><main>')
    yield _summary(snapshot)
    selected = _selected(snapshot)
    # Expand only selected records, one at a time. The summary retains question
    # text and small metadata rather than whole source rows or retrieval data.
    composition_snapshot = {**snapshot, "screening": {"items": (
        expand(item) if expand and item else item for _, item in selected if item
    )}}
    yield construction_composition.render_html(construction_composition.summarize(
        composition_snapshot, composition_annotations))
    yield _coverage(snapshot)
    yield "<section><h2>Selected benchmark items</h2>"
    if not selected:
        yield "<p>No selected items are recorded in this snapshot. Review the current stage and coverage findings above.</p>"
    for index, (compact, item) in enumerate(selected):
        # Only this selected record needs its original row for the report.
        # Rankings and unselected evidence remain compact while it is rendered.
        yield _selected_item(compact, expand(item) if expand else item, index, snapshot)
    yield "</section>"
    yield _requirements(snapshot)
    yield _history(snapshot)
    yield ('<footer><p>This report opens without the website or an internet connection. '
           'Use your browser’s print command to save a PDF. Expand evidence sections before printing if needed.</p>'
           '<p>The package also contains selected_items.csv for spreadsheet review and results.json for the complete record. '
           'The CSV question preview is limited to 1,000 characters; original fields remain complete in results.json. '
           'Text that could be interpreted as a spreadsheet formula is prefixed with an apostrophe in the CSV.</p></footer>'
           '</main></body></html>')


def _csv_safe(value) -> str:
    text = _text(value, "")
    # Quoting CSV cells alone does not prevent spreadsheet formula evaluation.
    if text.startswith(("\t", "\r", "\n")) or text.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def _write_csv(stream, snapshot, *, expand=None) -> None:
    writer = csv.writer(stream)
    writer.writerow(["item_id", "question_preview", "matched_tasks", "sources", "quality_score",
                     "screening_gate", *(key for key, _ in DIMENSIONS), "reviewer_notes"])
    names = _task_names(snapshot)
    for compact, item in _selected(snapshot):
        if expand is not None:
            item = expand(item)
        assessment = item.get("assessment") or {}
        facets = compact.get("matched_facet_ids", (assessment.get("task") or {}).get("matched_facet_ids", []))
        ratings = assessment.get("ratings") or {}
        row = [compact["item_id"], _preview(item, limit=1000), "; ".join(names.get(key, key) for key in facets),
               _sources(item), compact.get("quality_score"), (item.get("gate") or {}).get("status"),
               *((ratings.get(key) or {}).get("score") for key, _ in DIMENSIONS), ""]
        writer.writerow([_csv_safe(value) for value in row])


def build_results_package(snapshot: dict, *, expand=None):
    """Build a ZIP in bounded-memory temporary storage; caller owns its handle."""
    def expand_candidate(path, record):
        # Original source rows may themselves contain a field named
        # _candidate_ref. Only stored pipeline records are references.
        ranking = (len(path) == 5 and path[:2] == ("retrieval", "rankings")
                   and isinstance(path[2], int) and path[3] == "candidates"
                   and isinstance(path[4], int))
        screening = (len(path) == 3 and path[:2] == ("screening", "items")
                     and isinstance(path[2], int))
        return expand(record) if expand is not None and (ranking or screening) else record

    output = SpooledTemporaryFile(max_size=8 * 1024 * 1024, mode="w+b")
    try:
        with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
            with archive.open("report.html", "w", force_zip64=True) as stream:
                for chunk in _report(snapshot, expand=expand):
                    stream.write(chunk.encode("utf-8"))
            with archive.open("selected_items.csv", "w", force_zip64=True) as raw:
                with TextIOWrapper(raw, encoding="utf-8-sig", newline="") as stream:
                    _write_csv(stream, snapshot, expand=expand)
            with archive.open("results.json", "w", force_zip64=True) as raw:
                with TextIOWrapper(raw, encoding="utf-8") as stream:
                    # Read each stored candidate as the encoder visits it. The
                    # complete expanded result never occupies memory at once.
                    for chunk in streaming_json.iterencode(snapshot, expand=expand_candidate):
                        stream.write(chunk)
        output.seek(0)
        return output
    except BaseException:
        output.close()
        raise
