"""Descriptive composition of the saved selection, without new model judgments."""

from collections import Counter
from html import escape
from urllib.parse import quote


def _formats(annotations, selected_ids):
    if annotations is None:
        return {"counts": [], "unknown_count": len(selected_ids), "basis": None}
    if (not isinstance(annotations, dict) or type(annotations.get("version")) is not int
            or annotations["version"] != 1 or not isinstance(annotations.get("formats"), list)
            or not isinstance(annotations.get("basis"), str) or not annotations["basis"].strip()):
        raise ValueError("Format annotations require version 1, a formats list, and a description of their basis.")
    assigned = set()
    counts = Counter()
    for group in annotations["formats"]:
        if (not isinstance(group, dict) or not isinstance(group.get("label"), str)
                or not group["label"].strip() or not isinstance(group.get("item_ids"), list)):
            raise ValueError("Each format annotation requires a label and a list of selected item IDs.")
        for item_id in group["item_ids"]:
            if not isinstance(item_id, str) or item_id not in selected_ids or item_id in assigned:
                raise ValueError("Format annotations must assign each selected item ID at most once.")
            assigned.add(item_id)
            counts[group["label"].strip()] += 1
    return {"counts": [{"label": label, "count": count} for label, count in counts.items()],
            "unknown_count": len(selected_ids) - len(assigned), "basis": annotations["basis"].strip()}


def summarize(snapshot: dict, annotations: dict | None = None) -> dict:
    """Count selected rows and describe their evidence without changing selection.

    Sources and tasks may overlap because a row can have several provenances or
    task matches. Question comparisons use only saved question_text, with
    whitespace normalized and all other characters preserved. Quota findings
    retain the recorded selection outcome rather than reinterpreting evidence.
    """
    selection = snapshot.get("selection") or {}
    compact = {item["item_id"]: item for item in selection.get("items", [])}
    selected_ids = list(dict.fromkeys(selection.get("selected_item_ids", list(compact))))
    selected_set = set(selected_ids)
    requirements = snapshot.get("requirements") or {}
    task_labels = {facet["facet_id"]: (facet.get("task") or {}).get("text") or facet["facet_id"]
                   for facet in requirements.get("task_facets", [])}
    # Retain only the fields used below, even when callers stream expanded rows.
    evidence = {}
    for item in (snapshot.get("screening") or {}).get("items", []):
        item_id = item["item_id"]
        if item_id in selected_set:
            evidence[item_id] = {
                "question_text": item.get("question_text"),
                "sources": item.get("sources") or [],
                "matched_facet_ids": ((item.get("assessment") or {}).get("task") or {}).get("matched_facet_ids", []),
            }
    source_counts = Counter()
    task_counts = Counter()
    questions = {}
    unknown_sources = 0
    available_questions = 0
    for item_id in selected_ids:
        item = evidence.get(item_id, {})
        sources = {source["benchmark"] for source in item.get("sources", [])
                   if isinstance(source.get("benchmark"), str) and source["benchmark"].strip()}
        source_counts.update(sources)
        unknown_sources += not sources
        facets = compact.get(item_id, {}).get("matched_facet_ids", item.get("matched_facet_ids", []))
        task_counts.update(set(facets))
        question = item.get("question_text")
        if isinstance(question, str) and question.strip():
            normalized = " ".join(question.split())
            questions.setdefault(normalized, []).append(item_id)
            available_questions += 1
    selected_count = len(selected_ids)
    quota_requirements = requirements.get("coverage_requirements", [])
    coverage = []
    for row in selection.get("quota_coverage", []):
        index = row["requirement_index"]
        label = ((quota_requirements[index].get("requirement") or {}).get("text")
                 if 0 <= index < len(quota_requirements) else None)
        coverage.append({"requirement_index": index, "label": label or f"Coverage requirement {index + 1}",
                         "minimum_items": row.get("minimum_items"), "selected_count": row.get("selected_count", 0),
                         "shortfall": row.get("shortfall")})
    for facet_id in sorted(task_counts.keys() - task_labels.keys()):
        task_labels[facet_id] = facet_id
    return {
        "selected_count": selected_count,
        "sources": [{"name": name, "count": count, "percentage": count / selected_count * 100}
                    for name, count in sorted(source_counts.items(), key=lambda pair: (-pair[1], pair[0]))],
        "unknown_source_count": unknown_sources,
        "tasks": [{"facet_id": facet_id, "label": label, "count": task_counts[facet_id]}
                  for facet_id, label in task_labels.items()],
        "coverage": coverage,
        "question_text": {"available_count": available_questions, "distinct_count": len(questions),
                          "missing_count": selected_count - available_questions,
                          "overlaps": [{"item_ids": ids} for ids in questions.values() if len(ids) > 1]},
        "formats": _formats(annotations, selected_set),
    }


def _table(headers, rows):
    def cell(value):
        return escape(str(value), quote=True)

    return ('<div class="table-wrap"><table><thead><tr>'
            + ''.join(f'<th scope="col">{cell(header)}</th>' for header in headers)
            + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{cell(value)}</td>' for value in row) + '</tr>' for row in rows)
            + '</tbody></table></div>')


def render_html(composition: dict) -> str:
    """Render the same descriptive summary used by the public gallery."""
    text = '<section id="selected-composition"><h2>Composition of the selected items</h2>'
    count = composition["selected_count"]
    if not count:
        return text + '<p>No selected items are available for a composition summary.</p></section>'
    text += (f'<p>This summary describes the {count} selected items. Combining source benchmarks and requested '
             'tasks does not require combining question formats.</p><h3>Source benchmarks</h3>')
    if composition["sources"]:
        text += _table(["Source benchmark", "Selected items", "Share of selected items"], [
            [row["name"], row["count"], f'{round(row["percentage"], 1):g}%'] for row in composition["sources"]])
    if composition["unknown_source_count"]:
        text += f'<p>Source information is unavailable for {composition["unknown_source_count"]} selected items.</p>'
    text += ('<p class="muted">Each item is counted once per source benchmark. A row with several source '
             'benchmarks contributes to each, so shares can add up to more than 100%.</p><h3>Requested tasks</h3>')
    if composition["tasks"]:
        text += _table(["Requested task", "Selected items"], [[row["label"], row["count"]] for row in composition["tasks"]])
        text += '<p class="muted">An item may match more than one requested task.</p>'
    else:
        text += '<p>No task matches are recorded for the selected items.</p>'
    text += '<h3>Coverage requirements</h3>'
    if composition["coverage"]:
        text += _table(["Requirement", "Selected items", "Minimum", "Shortfall"], [
            [row["label"], row["selected_count"],
             row["minimum_items"] if row["minimum_items"] is not None else "Unresolved",
             row["shortfall"] if row["shortfall"] is not None else "Unresolved"]
            for row in composition["coverage"]])
    else:
        text += '<p>No collection quota findings are recorded.</p>'
    formats = composition["formats"]
    text += '<h3>Question formats</h3>'
    if formats["counts"]:
        text += _table(["Reviewed format", "Selected items"], [[row["label"], row["count"]] for row in formats["counts"]])
    if formats["unknown_count"]:
        text += f'<p>Question format has not been reviewed for {formats["unknown_count"]} selected items.</p>'
    if formats["basis"]:
        text += f'<p class="muted">{escape(formats["basis"], quote=True)}</p>'
    questions = composition["question_text"]
    distinct_text = "distinct text remains" if questions["distinct_count"] == 1 else "distinct texts remain"
    text += ('<h3>Question text overlap</h3>'
             f'<p>{questions["available_count"]} selected items have saved question text. '
             f'After whitespace normalization, {questions["distinct_count"]} {distinct_text}. '
             'This comparison preserves letter case, punctuation, and wording. '
             'It does not determine whether differently worded questions test the same content.</p>')
    if questions["missing_count"]:
        text += f'<p>Question text is unavailable for {questions["missing_count"]} selected items, which are excluded from this comparison.</p>'
    if questions["overlaps"]:
        text += ('<p>The following rows share question text after whitespace normalization. '
                 'They remain separate under the existing whole row identity rule.</p><ul>')
        for group in questions["overlaps"]:
            links = [f'<a href="#selected-item-{quote(item_id, safe="")}">Item {escape(item_id[:12], quote=True)}</a>'
                     for item_id in group["item_ids"]]
            text += '<li>' + ', '.join(links) + '</li>'
        text += '</ul>'
    return text + '</section>'
