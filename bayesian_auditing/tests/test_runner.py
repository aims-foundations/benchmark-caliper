import json

from openai import OpenAIError
import pytest

from bayesian_auditing import runner
from bayesian_auditing.judge import DEFAULT_MODEL
from bayesian_auditing.scoring import Assessment, score_summary


def fake_judge(assessment_dict, calls):
    def assess(evidence):
        calls.append(evidence)
        assessment = Assessment.model_validate(assessment_dict)
        return {"status": "complete", **score_summary(assessment),
                "assessment": assessment.model_dump(),
                "usage": {"input_tokens": 10, "output_tokens": 20,
                          "output_tokens_details": {"reasoning_tokens": 5}}}
    return assess


def test_whole_inventory_deduplicates_and_preserves_sources(corpus, assessment_dict, tmp_path):
    calls = []
    output = tmp_path / "results"
    summary = runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL,
                         judge=fake_judge(assessment_dict, calls))
    assert len(calls) == 3  # Exact duplicate across branches is assessed once.
    assert summary["source_rows_seen"] == 4
    assert summary["complete"] == 3
    assert summary["full_inventory_scored"] is True
    assert summary["usage_all_attempts"]["output_tokens"] == 60  # Already includes reasoning.
    ranks = json.loads((output / "ranked_items.json").read_text())
    assert len(ranks) == 3
    assert sorted(len(row["sources"]) for row in ranks) == [1, 1, 2]


def test_resume_after_interruption_and_partial_append(corpus, assessment_dict, tmp_path):
    output = tmp_path / "results"
    calls = []
    working = fake_judge(assessment_dict, calls)

    def interrupt(evidence):
        if calls:
            raise KeyboardInterrupt()
        return working(evidence)

    with pytest.raises(KeyboardInterrupt):
        runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL, judge=interrupt)
    assert json.loads((output / "summary.json").read_text())["state"] == "interrupted"
    with (output / "assessments.jsonl").open("ab") as log:
        log.write(b'{"status":')
    summary = runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL,
                         resume=True, judge=working)
    assert len(calls) == 3
    assert summary["complete"] == 3
    assert len(list(runner.records(output / "assessments.jsonl"))) == 4
    runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL, resume=True, judge=working)
    assert len(calls) == 3


def test_resume_refuses_changed_configuration(corpus, tmp_path):
    output = tmp_path / "results"
    runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL, dry_run=True)
    with pytest.raises(ValueError, match="settings"):
        runner.run(corpus[0], "different deployment", "rubric", output, model=DEFAULT_MODEL, dry_run=True, resume=True)


def test_dry_run_has_no_scores_and_marks_limited_scope(corpus, tmp_path):
    output = tmp_path / "preview"
    summary = runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL,
                         dry_run=True, limit_per_table=1)
    assert summary["source_rows_seen"] == 2
    assert summary["previews"] == 1
    assert not summary["full_inventory_scored"]
    assert not summary["full_inventory_traversed"]
    assert json.loads((output / "ranked_items.json").read_text()) == []
    record = next(runner.records(output / "assessments.jsonl"))
    assert json.loads(record["request_input"])["item_evidence"] == record["evidence"]


def test_api_failure_stops_and_is_retried_on_resume(corpus, assessment_dict, tmp_path):
    output = tmp_path / "results"

    def fail(_):
        raise OpenAIError("API unavailable")

    with pytest.raises(OpenAIError):
        runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL, judge=fail)
    summary = json.loads((output / "summary.json").read_text())
    assert summary["errors"] == 1
    assert summary["configured_scope_traversed"] is False
    calls = []
    summary = runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL,
                         resume=True, judge=fake_judge(assessment_dict, calls))
    assert summary["errors"] == 0
    assert summary["complete"] == 3


def test_partial_assessments_are_ranked_and_resume_without_rebilling(corpus, tmp_path, assessment_dict):
    assessment_dict["output_content"].update(score=None, confidence="insufficient", information_gaps=["Missing reference"])
    calls = []
    output = tmp_path / "results"
    summary = runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL,
                         judge=fake_judge(assessment_dict, calls))
    assert summary["complete"] == summary["needs_review"] == 3
    assert summary["full_inventory_traversed"] is True
    assert summary["full_inventory_scored"] is True
    ranked = json.loads((output / "ranked_items.json").read_text())
    assert len(ranked) == 3
    assert all(r["overall_score"] == 4 and r["scored_dimensions"] == 5 and r["needs_review"] for r in ranked)
    runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL,
               judge=fake_judge(assessment_dict, calls), resume=True)
    assert len(calls) == 3


def test_data_failure_is_reported_in_summary(corpus, tmp_path, monkeypatch):
    def broken(*_):
        raise OSError("Item table unavailable")

    monkeypatch.setattr(runner, "iter_items", broken)
    output = tmp_path / "results"
    with pytest.raises(OSError):
        runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL, dry_run=True)
    summary = json.loads((output / "summary.json").read_text())
    assert summary["fatal_error"] == "Item table unavailable"
    assert summary["full_inventory_traversed"] is False


def test_log_corruption_is_not_silently_dropped(tmp_path):
    path = tmp_path / "assessments.jsonl"
    path.write_text('not json\n')
    with pytest.raises(ValueError, match="Invalid assessment log"):
        list(runner.records(path, repair_tail=True))


def test_top_k_ranks_scores_and_can_expand_on_resume(corpus, assessment_dict, tmp_path):
    calls = []
    output = tmp_path / "results"
    assess = fake_judge(assessment_dict, calls)

    def varied_scores(evidence):
        grading = evidence["item"]["grading_criterion"]
        score = 3 if grading is None else (5 if grading["reference_answer"] == "2" else 1)
        for dimension in assessment_dict.values():
            dimension["score"] = score
        return assess(evidence)

    runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL,
               top_k=2, judge=varied_scores)
    ranked = json.loads((output / "ranked_items.json").read_text())
    assert [r["overall_score"] for r in ranked] == [5, 3]
    assert len(ranked[0]["sources"]) == 2
    runner.run(corpus[0], "deployment", "rubric", output, model=DEFAULT_MODEL,
               top_k=3, judge=varied_scores, resume=True)
    assert len(calls) == 3
    ranked = json.loads((output / "ranked_items.json").read_text())
    assert [r["overall_score"] for r in ranked] == [5, 3, 1]
