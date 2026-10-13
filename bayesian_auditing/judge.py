"""One OpenAI Responses request per item, with a strict six-dimension schema."""

import json
from pathlib import Path

from .scoring import Assessment, score_summary

DEFAULT_MODEL = "gpt-6-luna"
DEFAULT_REASONING_EFFORT = "high"
# This ceiling includes both internal reasoning and the structured assessment.
DEFAULT_MAX_OUTPUT_TOKENS = 25_000
PROMPT_PATH = Path(__file__).parent / "prompts" / "assess_item.md"


def request_input(deployment: str, evidence: dict) -> str:
    return json.dumps({"deployment": deployment, "item_evidence": evidence}, ensure_ascii=False)


class Judge:
    def __init__(self, client, deployment: str, prompt: str, *, model=DEFAULT_MODEL,
                 reasoning_effort=DEFAULT_REASONING_EFFORT,
                 max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS):
        self.client = client
        self.deployment = deployment
        self.prompt = prompt
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.max_output_tokens = max_output_tokens

    def request_options(self, evidence: dict) -> dict:
        return dict(
            model=self.model,
            instructions=self.prompt,
            input=request_input(self.deployment, evidence),
            reasoning={"effort": self.reasoning_effort},
            max_output_tokens=self.max_output_tokens,
            text={"format": {
                "type": "json_schema", "name": "validity_assessment",
                "schema": Assessment.model_json_schema(), "strict": True,
            }},
            store=False,
        )

    def __call__(self, evidence: dict) -> dict:
        return self.assess_response(self.client.responses.create(**self.request_options(evidence)))

    @staticmethod
    def assess_response(response) -> dict:
        result = {
            "response_id": response.id, "response_model": response.model,
            "usage": response.usage.model_dump(mode="json") if response.usage else None,
            "raw_output": response.output_text,
        }
        if response.status != "completed":
            return {**result, "status": "error", "error": f"Response {response.status}: {response.incomplete_details}"}
        try:
            assessment = Assessment.model_validate_json(response.output_text)
        except ValueError as exc:
            return {**result, "status": "error", "error": f"Invalid assessment or refusal: {exc}"}
        return {
            **result, "status": "complete", "assessment": assessment.model_dump(),
            **score_summary(assessment),
        }


class AsyncJudge(Judge):
    """The same request and scoring contract for cancellable website jobs."""

    async def __call__(self, evidence: dict) -> dict:
        response = await self.client.responses.create(**self.request_options(evidence))
        return self.assess_response(response)
