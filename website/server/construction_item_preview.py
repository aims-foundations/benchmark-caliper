"""Small display previews derived from saved items, without changing their evidence."""

import json
import re


def _question(text):
    text = text.strip()
    if text.startswith("{"):
        try:
            value = json.loads(text)
        except (ValueError, TypeError):
            return None
        if not isinstance(value, dict):
            return None
        for key in ("question", "prompt"):
            if isinstance(value.get(key), str):
                return _question(value[key])
        return None

    # Explicit question headings distinguish the target from demonstrations.
    headings = list(re.finditer(r"(?im)^\s*(?:#{1,6}\s*)?(?:Question|Q)\s*:\s*", text))
    if headings:
        target = text[headings[-1].end():]
        completed_answer = re.search(r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?(?:Answer|A)[ \t]*:[ \t]*([^\n]*)", target)
        if len(headings) > 1 and completed_answer and completed_answer.group(1).strip():
            return None  # The final marked question may still be a demonstration.
        answer = re.search(r"(?im)^\s*(?:#{1,6}\s*)?(?:Answer|A|Rationale|Options)\s*:", target)
        if answer:
            target = target[:answer.start()]
        return target.strip() or None

    # Some few shot prompts separate complete demonstrations with Answer: lines,
    # then end with an empty Answer: for the unanswered target.
    answers = list(re.finditer(r"(?im)^\s*Answer\s*:[^\n]*", text))
    if answers and not answers[-1].group().split(":", 1)[1].strip() and not text[answers[-1].end():].strip():
        start = answers[-2].end() if len(answers) > 1 else 0
        target = text[start:answers[-1].start()].strip()
        if target and (len(answers) > 1 or not re.match(r"(?i)(?:you are|the following|instructions?\b)", target)):
            return target

    # A standalone question is safe to preview. Role instructions, unmarked
    # demonstrations, and serialized rows are represented by the saved decision.
    if ("?" in text and len(text) <= 2000
            and not re.match(r"(?i)(?:you are|your (?:task|role)|the following|instructions?\b|[\[{])", text)
            and not re.search(r"(?i)here are (?:some )?examples|answer the last question", text)):
        return text
    return None


def item_preview(record):
    """Return a short labeled preview; never infer or rewrite the tested task."""
    question = record.get("question_text")
    text = _question(question) if isinstance(question, str) else None
    kind = "question"
    if not text:
        text = ((record.get("assessment") or {}).get("task") or {}).get("decision")
        kind = "decision" if isinstance(text, str) and text.strip() else "unavailable"
    if kind == "unavailable":
        return {"question_preview": "Open the item content to inspect its question.", "preview_kind": kind}
    compact = " ".join(text.split())
    if len(compact) > 260:
        compact = compact[:257].rsplit(" ", 1)[0] + "…"
    return {"question_preview": compact, "preview_kind": kind}
