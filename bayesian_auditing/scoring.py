"""The output contract and ranking arithmetic. No LLM or network calls here."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCORING_VERSION = 1
DIMENSIONS = (
    "input_ontology", "input_content", "input_form",
    "output_ontology", "output_content", "output_form",
)


class DimensionScore(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    score: Annotated[int, Field(ge=1, le=5)] | None
    justification: str
    evidence: list[str]
    information_gaps: list[str]

    @model_validator(mode="after")
    def check_evidence(self):
        if not self.justification.strip():
            raise ValueError("A justification is required")
        if any(not text.strip() for text in self.evidence + self.information_gaps):
            raise ValueError("Evidence and information gaps must be nonempty strings")
        if self.score is None and not self.information_gaps:
            raise ValueError("A null score must explain the missing evidence")
        if self.score is not None and not self.evidence:
            raise ValueError("A numerical score must identify supporting evidence")
        return self


class Assessment(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    input_ontology: DimensionScore
    input_content: DimensionScore
    input_form: DimensionScore
    output_ontology: DimensionScore
    output_content: DimensionScore
    output_form: DimensionScore


def overall_score(assessment: Assessment) -> float | None:
    scores = [getattr(assessment, name).score for name in DIMENSIONS]
    if any(score is None for score in scores):
        return None
    return sum(scores) / len(scores)
