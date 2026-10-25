"""Map retrieved O*NET passages to existing requirements without rewriting them.

Literal checks establish where added vocabulary came from. Human review is
still needed to assess whether the cited passage applies to the deployment.
"""

import json
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, ValidationError, model_validator

from .judge import DEFAULT_MAX_OUTPUT_TOKENS, DEFAULT_MODEL, DEFAULT_REASONING_EFFORT
from .requirements import Requirements, StrictModel, SupportedText, TaskFacet

MAPPING_VERSION = 1
MAX_REFINEMENTS = 3
PROMPT_PATH = Path(__file__).parent / "prompts" / "map_onet.md"


class OnetRecordMapping(StrictModel):
    record_id: str
    supporting_passage: str
    applicability: Literal["applicable", "partially_applicable", "not_applicable"]
    rationale: str
    search_terms: list[str]

    @model_validator(mode="after")
    def supported_vocabulary(self):
        if any(not value.strip() for value in (
            self.record_id, self.supporting_passage, self.rationale,
        )):
            raise ValueError("Record identifiers, passages, and rationales must contain text")
        if self.applicability == "not_applicable":
            if self.search_terms:
                raise ValueError("Rejected records cannot contribute search terms")
        elif not self.search_terms:
            raise ValueError("Adopted records must contribute supported search terms")
        if len(set(self.search_terms)) != len(self.search_terms):
            raise ValueError("Search terms must not repeat within a record")
        for term in self.search_terms:
            if not term.strip() or term not in self.supporting_passage:
                raise ValueError("Search terms must occur exactly in the supporting passage")
        return self


class OnetMapping(StrictModel):
    facet_id: str
    records: list[OnetRecordMapping]
    refinements: Annotated[list[SupportedText], Field(max_length=MAX_REFINEMENTS)]
    unresolved_details: list[str]

    @model_validator(mode="after")
    def valid_mapping(self):
        if not self.facet_id.strip():
            raise ValueError("A mapping must identify its existing task facet")
        record_ids = [record.record_id for record in self.records]
        if len(set(record_ids)) != len(record_ids):
            raise ValueError("A mapping must not repeat a record identifier")
        if any(refinement.text is None for refinement in self.refinements):
            raise ValueError("Search refinements must be supported statements")
        if any(not detail.strip() for detail in self.unresolved_details):
            raise ValueError("Unresolved details must contain text")
        if not self.records and not self.unresolved_details:
            raise ValueError("An empty mapping must explain why no records were selected")
        return self

    def validate_context(self, answers: dict[str, str], facet: TaskFacet,
                         candidates: list[dict]) -> None:
        """Check the existing facet, retrieved records, and original goal quotations."""
        if self.facet_id != facet.facet_id:
            raise ValueError("The mapping does not refer to the requested task facet.")
        texts = candidate_texts(candidates)
        for record in self.records:
            if record.record_id not in texts:
                raise ValueError("The mapping references an O*NET record outside the retrieved candidates.")
            if record.supporting_passage not in texts[record.record_id]:
                raise ValueError("An O*NET supporting passage does not occur exactly in its retrieved record.")
        for refinement in self.refinements:
            for reference in refinement.evidence:
                if (reference.answer_id not in answers
                        or reference.quote not in answers[reference.answer_id]):
                    raise ValueError("A search refinement quotation does not occur exactly in its original answer.")


def candidate_texts(candidates: list[dict]) -> dict[str, str]:
    """Use the local index's doc_id as the source identifier for model record_id."""
    texts = {}
    for candidate in candidates:
        record_id, text = candidate.get("doc_id"), candidate.get("text")
        if not isinstance(record_id, str) or not record_id.strip():
            raise ValueError("An O*NET candidate requires a nonempty doc_id.")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("An O*NET candidate requires nonempty searchable text.")
        if record_id in texts:
            raise ValueError("The retrieved O*NET candidates contain duplicate identifiers.")
        texts[record_id] = text
    return texts


def build_onet_query(requirements: Requirements, facet: TaskFacet) -> str:
    """Find work descriptions for this task; the mapper assesses deployment context.

    Shared answer formats and educational context belong in the mapping request,
    rather than diluting the task vocabulary used to retrieve O*NET candidates.
    """
    if facet not in requirements.task_facets:
        raise ValueError("The requested facet must match an extracted task facet.")
    return facet.task.text


class OnetMapper:
    """One structured Responses request per facet; invalid output is not retried."""

    def __init__(self, client, prompt: str | None = None, *, model=DEFAULT_MODEL,
                 reasoning_effort=DEFAULT_REASONING_EFFORT,
                 max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS):
        self.client = client
        self.prompt = PROMPT_PATH.read_text() if prompt is None else prompt
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.max_output_tokens = max_output_tokens

    def request_options(self, answers: dict[str, str], requirements: Requirements,
                        facet: TaskFacet, candidates: list[dict]) -> dict:
        requirements.validate_evidence(answers)
        if facet not in requirements.task_facets:
            raise ValueError("The requested facet must match an extracted task facet.")
        candidate_texts(candidates)
        return dict(
            model=self.model,
            instructions=self.prompt,
            input=json.dumps({
                "answers": answers,
                "requirements": requirements.model_dump(),
                "facet": facet.model_dump(),
                "candidates": candidates,
            }, ensure_ascii=False),
            reasoning={"effort": self.reasoning_effort},
            max_output_tokens=self.max_output_tokens,
            text={"format": {
                "type": "json_schema", "name": "onet_mapping",
                "schema": OnetMapping.model_json_schema(), "strict": True,
            }},
            store=False,
        )

    def __call__(self, answers: dict[str, str], requirements: Requirements,
                 facet: TaskFacet, candidates: list[dict]) -> dict:
        options = self.request_options(answers, requirements, facet, candidates)
        response = self.client.responses.create(**options)
        return self.assess_response(response, answers, facet, candidates)

    @staticmethod
    def assess_response(response, answers: dict[str, str], facet: TaskFacet,
                        candidates: list[dict]) -> dict:
        result = {
            "response_id": response.id, "response_model": response.model,
            "usage": response.usage.model_dump(mode="json") if response.usage else None,
        }
        if response.status != "completed":
            return {**result, "status": "error", "error": "The O*NET mapping response did not complete. No mapping was accepted."}
        if any(getattr(content, "type", None) == "refusal"
               for item in response.output for content in getattr(item, "content", [])):
            return {**result, "status": "error", "error": "The model declined to map O*NET records. No mapping was accepted."}
        try:
            mapping = OnetMapping.model_validate_json(response.output_text)
        except ValidationError:
            # Schema errors can contain arbitrary provider text; do not return it.
            return {**result, "status": "error", "error": "The O*NET mapping failed schema validation. Check required fields, applicability, and supported search terms."}
        try:
            mapping.validate_context(answers, facet, candidates)
        except ValueError as exc:
            return {**result, "status": "error", "error": str(exc)}
        return {**result, "status": "complete", "mapping": mapping.model_dump()}


class AsyncOnetMapper(OnetMapper):
    """The same mapping contract for cancellable website jobs."""

    async def __call__(self, answers: dict[str, str], requirements: Requirements,
                       facet: TaskFacet, candidates: list[dict]) -> dict:
        options = self.request_options(answers, requirements, facet, candidates)
        response = await self.client.responses.create(**options)
        return self.assess_response(response, answers, facet, candidates)
