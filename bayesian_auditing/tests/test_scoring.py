import pytest
from pydantic import ValidationError

from bayesian_auditing.scoring import Assessment, overall_score, score_summary


def test_full_confidence_preserves_equal_weight_compatibility_mean(assessment_dict):
    for dimension in assessment_dict.values():
        dimension["confidence"] = 1
    assert overall_score(Assessment.model_validate(assessment_dict)) == pytest.approx(25 / 6)


def test_unknown_dimension_keeps_supported_scores(assessment_dict):
    assessment_dict["output_content"].update(score=None, confidence=None, information_gaps=["Reference answer unavailable"])
    result = score_summary(Assessment.model_validate(assessment_dict))
    assert result == {"overall_score": pytest.approx(3.48), "compatibility_score": 4.2,
                      "scored_dimensions": 5, "needs_review": True}


@pytest.mark.parametrize("score", [1, 3, 5])
@pytest.mark.parametrize("confidence", [0, 0.17, 0.72, 0.93, 1])
def test_confidence_does_not_change_compatibility(assessment_dict, score, confidence):
    for dimension in assessment_dict.values():
        dimension.update(score=score, confidence=confidence)
    result = score_summary(Assessment.model_validate(assessment_dict))
    assert 1 <= result["overall_score"] <= score
    if confidence == 0:
        assert result["overall_score"] == 1
    if confidence == 1:
        assert result["overall_score"] == score
    assert result["compatibility_score"] == score
    assert not result["needs_review"]
    assert Assessment.model_validate(assessment_dict).input_ontology.confidence == confidence


def test_all_unknown_has_no_overall_score(assessment_dict):
    for dimension in assessment_dict.values():
        dimension.update(score=None, confidence=None, evidence=[], information_gaps=["Evidence absent"])
    result = score_summary(Assessment.model_validate(assessment_dict))
    assert result == {"overall_score": None, "compatibility_score": None,
                      "scored_dimensions": 0, "needs_review": True}


def test_supported_four_outranks_weak_five(assessment_dict):
    for dimension in assessment_dict.values():
        dimension.update(score=5, confidence=0.2)
    weak_five = overall_score(Assessment.model_validate(assessment_dict))
    for dimension in assessment_dict.values():
        dimension.update(score=4, confidence=0.9)
    supported_four = overall_score(Assessment.model_validate(assessment_dict))
    assert weak_five == pytest.approx(1.8)
    assert supported_four == pytest.approx(3.7)
    assert supported_four > weak_five


def test_one_known_dimension_retains_raw_mean_but_has_limited_ranking_support(assessment_dict):
    for dimension in assessment_dict.values():
        dimension.update(score=None, confidence=None, evidence=[], information_gaps=["Evidence absent"])
    assessment_dict["input_form"].update(score=5, confidence=0.93, evidence=["Text input matches."], information_gaps=[])
    assert score_summary(Assessment.model_validate(assessment_dict)) == {
        "overall_score": pytest.approx(1.62), "compatibility_score": 5, "scored_dimensions": 1, "needs_review": True,
    }


def test_uncertain_mismatches_are_not_removed_from_the_average(assessment_dict):
    for index, dimension in enumerate(assessment_dict.values()):
        dimension.update(score=5 if index % 2 else 1, confidence=0.9 if index % 2 else 0.1)
    result = score_summary(Assessment.model_validate(assessment_dict))
    assert result["overall_score"] == pytest.approx(2.8)
    assert result["compatibility_score"] == 3
    for dimension in assessment_dict.values():
        if dimension["score"] == 1:
            dimension["confidence"] = 0
    assert overall_score(Assessment.model_validate(assessment_dict)) == pytest.approx(2.8)


@pytest.mark.parametrize("score", [1, 2, 3, 4, 5])
def test_lower_confidence_or_missing_evidence_never_improves_rank(assessment_dict, score):
    dimension = assessment_dict["input_ontology"]
    dimension.update(score=score, confidence=1)
    supported = overall_score(Assessment.model_validate(assessment_dict))
    dimension["confidence"] = 0.2
    uncertain = overall_score(Assessment.model_validate(assessment_dict))
    dimension.update(score=None, confidence=None, evidence=[], information_gaps=["Evidence absent"])
    missing = overall_score(Assessment.model_validate(assessment_dict))
    assert 1 <= missing <= uncertain <= supported <= 5


def test_uniformly_low_confidence_reduces_ranking_support(assessment_dict):
    for dimension in assessment_dict.values():
        dimension.update(score=5, confidence=0.1)
    assert overall_score(Assessment.model_validate(assessment_dict)) == pytest.approx(1.4)
    for dimension in assessment_dict.values():
        dimension["confidence"] = 0.9
    assert overall_score(Assessment.model_validate(assessment_dict)) == pytest.approx(4.6)


@pytest.mark.parametrize("update", [
    {"confidence": "high"}, {"confidence": "insufficient"}, {"confidence": "0.7"},
    {"confidence": -0.1}, {"confidence": 1.1}, {"confidence": True},
    {"confidence": float("nan")}, {"confidence": float("inf")},
    {"confidence": None}, {"confidence_rationale": " "},
    {"score": None, "confidence": 0.1, "information_gaps": ["Missing"]},
])
def test_inconsistent_confidence_is_rejected(assessment_dict, update):
    assessment_dict["input_ontology"].update(update)
    with pytest.raises(ValidationError):
        Assessment.model_validate(assessment_dict)


def test_reported_gaps_flag_review_even_with_high_numerical_confidence(assessment_dict):
    assessment_dict["output_content"].update(confidence=0.93, information_gaps=["Reference provenance not documented"])
    result = score_summary(Assessment.model_validate(assessment_dict))
    assert result["needs_review"]
    assert result["overall_score"] == pytest.approx(3.945)
    assert result["compatibility_score"] == pytest.approx(25 / 6)


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
