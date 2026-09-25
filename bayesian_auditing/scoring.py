"""The output contract and ranking arithmetic. No LLM or network calls here."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCORING_VERSION = 2
# Deliberately simple policy weights, not calibrated probabilities. Missing or
# uncertain evidence pulls a judgment toward the neutral ranking baseline.
CONFIDENCE_WEIGHTS = {"high": 1.0, "medium": 0.6, "low": 0.3, "insufficient": 0.0}
NEUTRAL_SCORE = 3.0
SCORING_POLICY = {
    "version": SCORING_VERSION,
    "neutral_score": NEUTRAL_SCORE,
    "confidence_weights": CONFIDENCE_WEIGHTS,
    "formula": "mean(3 + confidence_weight * (score - 3)); missing scores contribute 3",
}
DIMENSIONS = (
    "input_ontology", "input_content", "input_form",
    "output_ontology", "output_content", "output_form",
)


class DimensionScore(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    score: Annotated[int, Field(ge=1, le=5)] | None
    confidence: Literal["high", "medium", "low", "insufficient"]
    confidence_rationale: str
    justification: str
    evidence: list[str]
    information_gaps: list[str]

    @model_validator(mode="after")
    def check_evidence(self):
        if not self.justification.strip():
            raise ValueError("A justification is required")
        if not self.confidence_rationale.strip():
            raise ValueError("A confidence rationale is required")
        if any(not text.strip() for text in self.evidence + self.information_gaps):
            raise ValueError("Evidence and information gaps must be nonempty strings")
        if self.score is None and not self.information_gaps:
            raise ValueError("A null score must explain the missing evidence")
        if self.score is not None and not self.evidence:
            raise ValueError("A numerical score must identify supporting evidence")
        if (self.score is None) != (self.confidence == "insufficient"):
            raise ValueError("Only a null score must have insufficient confidence")
        return self


class Assessment(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    input_ontology: DimensionScore
    input_content: DimensionScore
    input_form: DimensionScore
    output_ontology: DimensionScore
    output_content: DimensionScore
    output_form: DimensionScore


def adjusted_score(dimension: DimensionScore) -> float:
    if dimension.score is None:
        return NEUTRAL_SCORE
    return NEUTRAL_SCORE + CONFIDENCE_WEIGHTS[dimension.confidence] * (dimension.score - NEUTRAL_SCORE)


def overall_score(assessment: Assessment) -> float:
    """All six dimensions contribute, including explicit neutral placeholders."""
    return sum(adjusted_score(getattr(assessment, name)) for name in DIMENSIONS) / len(DIMENSIONS)


def score_summary(assessment: Assessment) -> dict:
    dimensions = [getattr(assessment, name) for name in DIMENSIONS]
    known = [dimension.score for dimension in dimensions if dimension.score is not None]
    return {
        "overall_score": overall_score(assessment),
        "compatibility_score": sum(known) / len(known) if known else None,
        "scored_dimensions": len(known),
        "needs_review": any(d.confidence in {"low", "insufficient"} for d in dimensions),
    }
