"""Rate a candidate against the deployment and apply the four-dimension gate.

Literal evidence checks establish traceability to the original item, not whether
an interpretation is correct. Collection selection and adaptive allocation are
separate stages; this module does not calculate an aggregate ranking score.
"""

import json
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, ValidationError, model_validator

from .judge import DEFAULT_MAX_OUTPUT_TOKENS, DEFAULT_MODEL, DEFAULT_REASONING_EFFORT
from .requirements import Requirements, StrictModel
from .scoring import DIMENSIONS


SCREENING_VERSION = 1
GATED_DIMENSIONS = ("input_ontology", "input_content", "input_form", "output_ontology")
PROMPT_PATH = Path(__file__).parent / "prompts" / "screen_item.md"


def _check_explanation(evidence, justification, information_gaps):
    if not justification.strip():
        raise ValueError("Every screening finding requires a justification.")
    if any(not value.strip() for value in [*evidence, *information_gaps]):
        raise ValueError("Evidence and information gaps must contain text.")


class TaskFinding(StrictModel):
    status: Literal["matched", "no_match", "unresolved"]
    decision: str | None
    matched_facet_ids: list[str]
    evidence: list[str]
    justification: str
    information_gaps: list[str]

    @model_validator(mode="after")
    def valid_task_finding(self):
        _check_explanation(self.evidence, self.justification, self.information_gaps)
        if self.decision is not None and (not self.decision.strip() or not self.evidence):
            raise ValueError("A described decision requires text and supporting item evidence.")
        if len(set(self.matched_facet_ids)) != len(self.matched_facet_ids):
            raise ValueError("Matched task identifiers must not repeat.")
        if any(not value.strip() for value in self.matched_facet_ids):
            raise ValueError("Matched task identifiers must contain text.")
        if self.status == "matched":
            if not self.matched_facet_ids:
                raise ValueError("A matched task must identify at least one extracted facet.")
        elif self.matched_facet_ids:
            raise ValueError("Only a matched task can claim extracted facet identifiers.")
        if self.status == "unresolved":
            if not self.information_gaps:
                raise ValueError("An unresolved task must explain the missing evidence.")
        elif self.decision is None or not self.evidence:
            raise ValueError("A resolved task requires its decision and supporting item evidence.")
        return self


class ScreeningRating(StrictModel):
    score: Annotated[int, Field(ge=1, le=5)] | None
    evidence: list[str]
    justification: str
    information_gaps: list[str]

    @model_validator(mode="after")
    def supported_rating(self):
        _check_explanation(self.evidence, self.justification, self.information_gaps)
        if self.score is None and not self.information_gaps:
            raise ValueError("An unknown rating must explain its information gap.")
        if self.score is not None and not self.evidence:
            raise ValueError("A numerical rating requires supporting item evidence.")
        return self


class ScreeningRatings(StrictModel):
    input_ontology: ScreeningRating
    input_content: ScreeningRating
    input_form: ScreeningRating
    output_ontology: ScreeningRating
    output_content: ScreeningRating
    output_form: ScreeningRating


class CoverageFinding(StrictModel):
    requirement_index: Annotated[int, Field(ge=0)]
    satisfied: bool | None
    evidence: list[str]
    justification: str
    information_gaps: list[str]

    @model_validator(mode="after")
    def supported_coverage(self):
        _check_explanation(self.evidence, self.justification, self.information_gaps)
        if self.satisfied is None and not self.information_gaps:
            raise ValueError("Unknown coverage must explain its information gap.")
        if self.satisfied is not None and not self.evidence:
            raise ValueError("A coverage conclusion requires supporting item evidence.")
        return self


def _item_strings(value):
    """Yield original string values, preserving raw JSON cells and whitespace."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from _item_strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _item_strings(nested)


class ScreeningAssessment(StrictModel):
    task: TaskFinding
    ratings: ScreeningRatings
    coverage: list[CoverageFinding]

    def validate_context(self, requirements: Requirements, item_row: dict) -> None:
        """Check facet/coverage references and literal excerpts of item values.

        Every evidence string must occur within one original string value in the
        row, including nested objects/lists. Field names, joined values, generated
        summaries, and deployment-only quotations are not item evidence. JSON
        stored inside a string cell is kept literal. Missing facts belong in
        information_gaps. These checks cannot establish semantic support.
        """
        facet_ids = {facet.facet_id for facet in requirements.task_facets}
        if not set(self.task.matched_facet_ids).issubset(facet_ids):
            raise ValueError("Screening references a task outside the extracted requirements.")
        indices = [finding.requirement_index for finding in self.coverage]
        if (len(indices) != len(requirements.coverage_requirements)
                or set(indices) != set(range(len(requirements.coverage_requirements)))):
            raise ValueError("Screening must assess each coverage requirement exactly once.")
        for finding in self.coverage:
            requirement = requirements.coverage_requirements[finding.requirement_index]
            if finding.satisfied is True:
                if self.task.status != "matched":
                    raise ValueError("Positive coverage requires a matched task.")
                if requirement.facet_ids and not set(requirement.facet_ids).intersection(self.task.matched_facet_ids):
                    raise ValueError("Positive coverage must apply to a matched task facet.")
        strings = list(_item_strings(item_row))
        findings = [self.task, *(getattr(self.ratings, name) for name in DIMENSIONS), *self.coverage]
        for finding in findings:
            for quote in finding.evidence:
                if not any(quote in original for original in strings):
                    raise ValueError("A screening evidence quotation does not occur exactly in the original item.")


def gate_for(assessment: ScreeningAssessment) -> dict:
    """Apply the task match and four independent thresholds without weighting."""
    failures, unresolved = [], []
    if assessment.task.status == "no_match":
        failures.append("The question does not request an extracted task.")
    elif assessment.task.status == "unresolved":
        unresolved.append("The question's match to an extracted task is unresolved.")
    for name in GATED_DIMENSIONS:
        score = getattr(assessment.ratings, name).score
        label = name.replace("_", " ").capitalize()
        if score is None:
            unresolved.append(f"{label} has no defensible rating.")
        elif score < 3:
            failures.append(f"{label} is {score}/5, below the required 3/5.")
    if failures:
        return {"status": "fail", "reasons": failures}
    if unresolved:
        return {"status": "unresolved", "reasons": unresolved}
    return {"status": "pass", "reasons": [
        "The question requests an extracted task and all four gated ratings are at least 3/5.",
    ]}


class ItemScreener:
    """One structured request per original item; invalid output is not retried."""

    def __init__(self, client, prompt: str | None = None, *, model=DEFAULT_MODEL,
                 reasoning_effort=DEFAULT_REASONING_EFFORT,
                 max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS):
        self.client = client
        self.prompt = PROMPT_PATH.read_text(encoding="utf-8") if prompt is None else prompt
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.max_output_tokens = max_output_tokens

    def request_options(self, answers: dict[str, str], requirements: Requirements, item_row: dict) -> dict:
        requirements.validate_evidence(answers)
        if not isinstance(item_row, dict):
            raise ValueError("Screening requires the complete original item row.")
        return dict(
            model=self.model,
            instructions=self.prompt,
            input=json.dumps({"answers": answers, "requirements": requirements.model_dump(),
                              "item": item_row}, ensure_ascii=False, allow_nan=False),
            reasoning={"effort": self.reasoning_effort},
            max_output_tokens=self.max_output_tokens,
            text={"format": {"type": "json_schema", "name": "item_screening",
                             "schema": ScreeningAssessment.model_json_schema(), "strict": True}},
            store=False,
        )

    def __call__(self, answers: dict[str, str], requirements: Requirements, item_row: dict) -> dict:
        response = self.client.responses.create(**self.request_options(answers, requirements, item_row))
        return self.assess_response(response, requirements, item_row)

    @staticmethod
    def assess_response(response, requirements: Requirements, item_row: dict) -> dict:
        result = {"response_id": response.id, "response_model": response.model,
                  "usage": response.usage.model_dump(mode="json") if response.usage else None}
        if response.status != "completed":
            return {**result, "status": "error", "error": "The screening response did not complete. No assessment was accepted."}
        if any(getattr(content, "type", None) == "refusal"
               for item in response.output for content in getattr(item, "content", [])):
            return {**result, "status": "error", "error": "The model declined to screen the item. No assessment was accepted."}
        try:
            assessment = ScreeningAssessment.model_validate_json(response.output_text)
        except ValidationError:
            return {**result, "status": "error", "error": "The screening failed schema validation. Check task findings, ratings, and coverage evidence."}
        try:
            assessment.validate_context(requirements, item_row)
        except ValueError as exc:
            return {**result, "status": "error", "error": str(exc)}
        return {**result, "status": "complete", "assessment": assessment.model_dump(),
                "gate": gate_for(assessment)}


class AsyncItemScreener(ItemScreener):
    """The same screening contract for cancellable website jobs."""

    async def __call__(self, answers: dict[str, str], requirements: Requirements, item_row: dict) -> dict:
        response = await self.client.responses.create(**self.request_options(answers, requirements, item_row))
        return self.assess_response(response, requirements, item_row)
