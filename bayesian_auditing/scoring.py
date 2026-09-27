"""The output contract and ranking arithmetic. No LLM or network calls here."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCORING_VERSION = 5
SCORING_POLICY = {
    "version": SCORING_VERSION,
    "formula": "1 + sum(confidence * (score - 1) for scored dimensions) / 6; no scored dimensions yields null",
    "ranking_floor": 1,
    "compatibility_formula": "mean(available dimension scores); no scored dimensions yields null",
    "confidence_role": "discounts support above the ranking floor; never raises a dimension's contribution",
    "confidence_scale": "self-reported evidence support from 0 to 1; null when no score is defensible",
    "needs_review_rule": "any missing score or reported information gap",
    "missing_dimensions": "contribute 1 to ranking only; excluded from compatibility mean; coverage reported separately",
    "no_scored_dimensions": "unranked; retained with evidence gaps",
    "interpretation": "conservative ranking heuristic, not a calibrated probability or statistical lower bound",
}
DIMENSIONS = (
    "input_ontology", "input_content", "input_form",
    "output_ontology", "output_content", "output_form",
)


class DimensionScore(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    # Structured outputs follow schema order: establish the evidence and gaps
    # before generating the rating and its confidence judgment.
    evidence: list[str]
    information_gaps: list[str]
    justification: str
    score: Annotated[int, Field(ge=1, le=5)] | None
    confidence: Annotated[float, Field(ge=0, le=1)] | None
    confidence_rationale: str

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
        if (self.score is None) != (self.confidence is None):
            raise ValueError("Score and confidence must either both be null or both be numerical")
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
    """Discount support above 1, with all six dimensions equally represented.

    Missing dimensions contribute only the ranking floor, without imputing a
    compatibility score. Entirely unscorable assessments remain unranked.
    """
    known = [getattr(assessment, name) for name in DIMENSIONS
             if getattr(assessment, name).score is not None]
    return 1 + sum(d.confidence * (d.score - 1) for d in known) / len(DIMENSIONS) if known else None


def score_summary(assessment: Assessment) -> dict:
    dimensions = [getattr(assessment, name) for name in DIMENSIONS]
    known = [dimension.score for dimension in dimensions if dimension.score is not None]
    return {
        "overall_score": overall_score(assessment),
        "compatibility_score": sum(known) / len(known) if known else None,
        "scored_dimensions": len(known),
        "needs_review": any(d.score is None or d.information_gaps for d in dimensions),
    }
