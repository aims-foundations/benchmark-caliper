import pytest
from pydantic import ValidationError

from bayesian_auditing.scoring import Assessment, overall_score, score_summary


def test_six_scores_have_equal_weight(assessment_dict):
    assert overall_score(Assessment.model_validate(assessment_dict)) == pytest.approx(25 / 6)


def test_unknown_dimension_keeps_supported_scores(assessment_dict):
    assessment_dict["output_content"].update(score=None, confidence="insufficient", information_gaps=["Reference answer unavailable"])
    result = score_summary(Assessment.model_validate(assessment_dict))
    assert result == {"overall_score": 4, "compatibility_score": 4.2,
                      "scored_dimensions": 5, "needs_review": True}


@pytest.mark.parametrize("score,expected", [(5, 3.6), (1, 2.4)])
def test_uncertainty_shrinks_both_good_and_bad_judgments(assessment_dict, score, expected):
    for dimension in assessment_dict.values():
        dimension.update(score=score, confidence="low")
    result = score_summary(Assessment.model_validate(assessment_dict))
    assert result["overall_score"] == pytest.approx(expected)
    assert result["compatibility_score"] == score
    assert result["needs_review"]


def test_all_unknown_is_explicit_baseline_not_observed_compatibility(assessment_dict):
    for dimension in assessment_dict.values():
        dimension.update(score=None, confidence="insufficient", evidence=[], information_gaps=["Evidence absent"])
    result = score_summary(Assessment.model_validate(assessment_dict))
    assert result == {"overall_score": 3, "compatibility_score": None,
                      "scored_dimensions": 0, "needs_review": True}


def test_confidence_can_change_ranking(assessment_dict):
    for dimension in assessment_dict.values():
        dimension.update(score=5, confidence="low")
    weak_five = overall_score(Assessment.model_validate(assessment_dict))
    for dimension in assessment_dict.values():
        dimension.update(score=4, confidence="high")
    supported_four = overall_score(Assessment.model_validate(assessment_dict))
    assert supported_four > weak_five


@pytest.mark.parametrize("update", [
    {"confidence": "certain"}, {"confidence": 0.9}, {"confidence_rationale": " "},
    {"confidence": "insufficient"},
    {"score": None, "confidence": "high", "information_gaps": ["Missing"]},
])
def test_inconsistent_confidence_is_rejected(assessment_dict, update):
    assessment_dict["input_ontology"].update(update)
    with pytest.raises(ValidationError):
        Assessment.model_validate(assessment_dict)


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
