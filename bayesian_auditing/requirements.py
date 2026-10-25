"""Step 2: extract requirements and check their references to the six answers.

The schema and literal-quotation checks establish traceability. Whether the
quoted text supports an interpretation still requires human review.
"""

import json
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from .judge import DEFAULT_MAX_OUTPUT_TOKENS, DEFAULT_MODEL, DEFAULT_REASONING_EFFORT

EXTRACTION_VERSION = 1
PROMPT_PATH = Path(__file__).parent / "prompts" / "extract_requirements.md"
AnswerId = Literal["task", "users", "inputs", "outputs", "success", "constraints"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class EvidenceRef(StrictModel):
    answer_id: AnswerId
    quote: str

    @model_validator(mode="after")
    def nonempty_quote(self):
        if not self.quote.strip():
            raise ValueError("An evidence quotation must contain text")
        return self


class SupportedText(StrictModel):
    text: str | None
    evidence: list[EvidenceRef]

    @model_validator(mode="after")
    def supported_or_unknown(self):
        if self.text is None:
            if self.evidence:
                raise ValueError("Unknown information must have no evidence")
        elif not self.text.strip() or not self.evidence:
            raise ValueError("Known information requires nonempty text and evidence")
        return self


class TaskFacet(StrictModel):
    facet_id: str
    task: SupportedText
    required_input_evidence: SupportedText
    required_output_behavior: SupportedText
    essential: bool | None

    @model_validator(mode="after")
    def stated_task(self):
        if not self.facet_id.strip():
            raise ValueError("A task facet requires a nonempty identifier")
        if self.task.text is None:
            raise ValueError("A task facet must identify a supported task")
        return self


class CoverageRequirement(StrictModel):
    facet_ids: list[str]
    minimum_items: Annotated[int, Field(ge=1)] | None
    requirement: SupportedText

    @model_validator(mode="after")
    def stated_requirement(self):
        if self.requirement.text is None:
            raise ValueError("A coverage requirement must have supporting evidence")
        if len(set(self.facet_ids)) != len(self.facet_ids):
            raise ValueError("A coverage requirement must not repeat a facet identifier")
        return self


class Requirements(StrictModel):
    workflow: SupportedText
    primary_user: SupportedText
    input_types: SupportedText
    output_types: SupportedText
    authority: SupportedText
    task_facets: list[TaskFacet]
    coverage_requirements: list[CoverageRequirement]
    unresolved_details: list[str]

    @model_validator(mode="after")
    def valid_facet_references(self):
        facet_ids = [facet.facet_id for facet in self.task_facets]
        if len(set(facet_ids)) != len(facet_ids):
            raise ValueError("Task facet identifiers must be unique")
        for requirement in self.coverage_requirements:
            if not set(requirement.facet_ids).issubset(facet_ids):
                raise ValueError("A coverage requirement references an unknown task facet")
        if any(not detail.strip() for detail in self.unresolved_details):
            raise ValueError("Unresolved details must contain text")
        return self

    def validate_evidence(self, answers: dict[str, str]) -> None:
        """Require every quotation to occur verbatim in its named source answer."""
        supported = [self.workflow, self.primary_user, self.input_types,
                     self.output_types, self.authority]
        for facet in self.task_facets:
            supported.extend((facet.task, facet.required_input_evidence,
                              facet.required_output_behavior))
        supported.extend(requirement.requirement for requirement in self.coverage_requirements)
        for value in supported:
            for reference in value.evidence:
                if reference.answer_id not in answers:
                    raise ValueError(f"The source answer '{reference.answer_id}' is missing.")
                if reference.quote not in answers[reference.answer_id]:
                    raise ValueError(
                        f"An evidence quotation does not occur exactly in the '{reference.answer_id}' answer."
                    )


class RequirementExtractor:
    """One structured Responses request; invalid output is returned as an error."""

    def __init__(self, client, prompt: str | None = None, *, model=DEFAULT_MODEL,
                 reasoning_effort=DEFAULT_REASONING_EFFORT,
                 max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS):
        self.client = client
        self.prompt = PROMPT_PATH.read_text() if prompt is None else prompt
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.max_output_tokens = max_output_tokens

    def request_options(self, answers: dict[str, str]) -> dict:
        return dict(
            model=self.model,
            instructions=self.prompt,
            input=json.dumps({"answers": answers}, ensure_ascii=False),
            reasoning={"effort": self.reasoning_effort},
            max_output_tokens=self.max_output_tokens,
            text={"format": {
                "type": "json_schema", "name": "deployment_requirements",
                "schema": Requirements.model_json_schema(), "strict": True,
            }},
            store=False,
        )

    def __call__(self, answers: dict[str, str]) -> dict:
        response = self.client.responses.create(**self.request_options(answers))
        return self.assess_response(response, answers)

    @staticmethod
    def assess_response(response, answers: dict[str, str]) -> dict:
        result = {
            "response_id": response.id, "response_model": response.model,
            "usage": response.usage.model_dump(mode="json") if response.usage else None,
        }
        if response.status != "completed":
            return {**result, "status": "error", "error": "The extraction response did not complete. No requirements were accepted."}
        if any(getattr(content, "type", None) == "refusal"
               for item in response.output for content in getattr(item, "content", [])):
            return {**result, "status": "error", "error": "The model declined to extract requirements. No requirements were accepted."}
        try:
            requirements = Requirements.model_validate_json(response.output_text)
        except ValidationError:
            # Pydantic errors can include arbitrary model output. Keep them out of
            # the public result, along with raw output and provider refusal text.
            return {**result, "status": "error", "error": "The extraction failed schema validation. Check required fields, evidence, and facet references."}
        try:
            requirements.validate_evidence(answers)
        except ValueError as exc:
            return {**result, "status": "error", "error": str(exc)}
        return {**result, "status": "complete", "requirements": requirements.model_dump()}


class AsyncRequirementExtractor(RequirementExtractor):
    """The same extraction contract for cancellable website jobs."""

    async def __call__(self, answers: dict[str, str]) -> dict:
        response = await self.client.responses.create(**self.request_options(answers))
        return self.assess_response(response, answers)
