import pytest
from pydantic import ValidationError

from bayesian_auditing.scoring import Assessment, overall_score


def test_six_scores_have_equal_weight(assessment_dict):
    assert overall_score(Assessment.model_validate(assessment_dict)) == pytest.approx(25 / 6)


def test_unknown_dimension_prevents_overall_score(assessment_dict):
    assessment_dict["output_content"].update(score=None, information_gaps=["Reference answer unavailable"])
    assert overall_score(Assessment.model_validate(assessment_dict)) is None


@pytest.mark.parametrize("score", [0, 6, 3.5, True, "5"])
def test_invalid_ratings_are_rejected(assessment_dict, score):
    assessment_dict["input_ontology"]["score"] = score
    with pytest.raises(ValidationError):
        Assessment.model_validate(assessment_dict)


def test_numerical_score_requires_evidence(assessment_dict):
    assessment_dict["input_ontology"]["evidence"] = []
    with pytest.raises(ValidationError, match="supporting evidence"):
        Assessment.model_validate(assessment_dict)


def test_null_score_requires_explanation(assessment_dict):
    assessment_dict["input_ontology"]["score"] = None
    with pytest.raises(ValidationError, match="missing evidence"):
        Assessment.model_validate(assessment_dict)


def test_all_six_dimensions_are_required(assessment_dict):
    del assessment_dict["output_form"]
    with pytest.raises(ValidationError):
        Assessment.model_validate(assessment_dict)
