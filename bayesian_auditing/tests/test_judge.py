import asyncio
import json

import httpx
from openai import AsyncOpenAI, OpenAI
import pytest

from bayesian_auditing.judge import AsyncJudge, DEFAULT_MODEL, Judge
from bayesian_auditing.scoring import DIMENSIONS


@pytest.mark.parametrize("mode", ["complete", "partial", "malformed", "incomplete", "refusal"])
@pytest.mark.parametrize("async_mode", [False, True])
def test_real_sdk_request_and_response_contract(assessment_dict, mode, async_mode):
    if mode == "partial":
        assessment_dict["output_content"].update(score=None, confidence="insufficient", information_gaps=["Reference missing"])
    captured = []

    def respond(request):
        captured.append(json.loads(request.content))
        content = {"type": "output_text", "text": json.dumps(assessment_dict), "annotations": []}
        if mode == "malformed":
            content["text"] = '{"input_ontology": 99}'
        if mode == "refusal":
            content = {"type": "refusal", "refusal": "Cannot assess this item"}
        return httpx.Response(200, json={
            "id": "resp_test", "object": "response", "created_at": 1, "model": DEFAULT_MODEL,
            "status": "incomplete" if mode == "incomplete" else "completed",
            "incomplete_details": {"reason": "max_output_tokens"} if mode == "incomplete" else None,
            "output": [{"type": "message", "id": "msg_test", "status": "completed", "role": "assistant", "content": [content]}],
            "usage": {"input_tokens": 100, "output_tokens": 90, "total_tokens": 190,
                      "input_tokens_details": {"cached_tokens": 10}, "output_tokens_details": {"reasoning_tokens": 30}},
        })

    if async_mode:
        async def assess():
            async with AsyncOpenAI(api_key="unit-test-placeholder", http_client=httpx.AsyncClient(transport=httpx.MockTransport(respond))) as client:
                return await AsyncJudge(client, "A text mathematics tutor", "Six-dimension rubric")({"item": {"content": "1 + 1"}})
        output = asyncio.run(assess())
    else:
        with OpenAI(api_key="unit-test-placeholder", http_client=httpx.Client(transport=httpx.MockTransport(respond))) as client:
            output = Judge(client, "A text mathematics tutor", "Six-dimension rubric")({"item": {"content": "1 + 1"}})
    request = captured[0]
    assert request["model"] == "gpt-6-luna"
    assert request["reasoning"] == {"effort": "high"}
    assert request["max_output_tokens"] == 25_000
    assert request["store"] is False
    assert request["text"]["format"]["strict"] is True
    assert set(request["text"]["format"]["schema"]["required"]) == set(DIMENSIONS)
    assert json.loads(request["input"])["deployment"] == "A text mathematics tutor"
    assert output["usage"]["output_tokens_details"]["reasoning_tokens"] == 30
    assert output["status"] == ("complete" if mode in {"complete", "partial"} else "error")
    if mode == "complete":
        assert output["overall_score"] == pytest.approx(25 / 6)
    if mode == "partial":
        assert output["overall_score"] == 4
        assert output["scored_dimensions"] == 5 and output["needs_review"]
