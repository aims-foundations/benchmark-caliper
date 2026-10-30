from website.server.construction_item_preview import item_preview


def preview(text, decision="Choose the appropriate treatment."):
    return item_preview({"question_text": text, "assessment": {"task": {"decision": decision}}})


def test_explicit_target_replaces_role_instructions_and_demonstrations():
    result = preview("You are a doctor.\n###Question: Example?\nA. One\n###Answer: A\n###Question: The actual case asks which treatment?\nA. Two\n###Answer:")
    assert result == {"preview_kind": "question", "question_preview": "The actual case asks which treatment? A. Two"}


def test_json_prompt_extracts_final_unanswered_block_without_showing_serialization():
    import json
    result = preview(json.dumps({"prompt": "The following are examples.\n\nFirst example?\nA. One\nAnswer: A\n\nThe actual case?\nA. Two\nAnswer:", "candidate_continuations": [" A"]}))
    assert result == {"preview_kind": "question", "question_preview": "The actual case? A. Two"}


def test_role_instructions_use_saved_decision_instead_of_guessing_question():
    assert preview("You are a clinician. Ask questions. How do you proceed?")["preview_kind"] == "decision"
    assert preview("You are a clinician. Ask questions. How do you proceed?")["question_preview"] == "Choose the appropriate treatment."


def test_answered_demonstration_is_not_mistaken_for_an_unmarked_target():
    assert preview("Question: First example?\nAnswer: A\nQuestion: Last example?\nAnswer: B\n\nUnmarked target question?")["preview_kind"] == "decision"


def test_unknown_or_malformed_content_never_shows_raw_json():
    assert preview('{"broken":', "")["preview_kind"] == "unavailable"
    assert preview('{"metadata": "unrelated question?"}')["preview_kind"] == "decision"


def test_short_standalone_question_is_preserved_and_original_record_unchanged():
    record = {"question_text": "Which test should be ordered?", "assessment": None}
    assert item_preview(record) == {"preview_kind": "question", "question_preview": "Which test should be ordered?"}
    assert record == {"question_text": "Which test should be ordered?", "assessment": None}
