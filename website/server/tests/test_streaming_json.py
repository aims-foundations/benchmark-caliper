"""Bounded JSON parsing preserves complete evidence and numeric identities."""

import asyncio
from io import BytesIO
import json
import math

import pytest

from website.server.streaming_json import (
    BinaryChunkReader, CHUNK_BYTES, async_load, iterencode, load,
)


class BoundedReader(BytesIO):
    def read(self, size=-1):
        assert 0 <= size <= CHUNK_BYTES
        return super().read(size)


async def chunks(payload, size=17):
    yield b""
    for offset in range(0, len(payload), size):
        yield payload[offset:offset + size]


def parse(payload, asynchronous=False, transform=None):
    if asynchronous:
        return asyncio.run(async_load(BinaryChunkReader(chunks(payload)), transform=transform))
    return load(BoundedReader(payload), transform=transform)


@pytest.mark.parametrize("asynchronous", [False, True])
def test_preserves_nested_fields_unicode_and_exact_number_types(asynchronous):
    payload = ('{"row":{"text":"line\\n字 😀","empty":{},"array":[null,true,false,[],""]},'
               '"huge":123456789012345678901234567890123456789012345678901234567890,'
               '"integer":1,"float":1.0,"negative_zero":-0.0,"exponent":1e-250}').encode()
    result = parse(payload, asynchronous)
    assert result == json.loads(payload)
    assert type(result["huge"]) is int
    assert type(result["integer"]) is int
    assert type(result["float"]) is float
    assert math.copysign(1, result["negative_zero"]) == -1
    assert json.dumps(result, sort_keys=True) == json.dumps(json.loads(payload), sort_keys=True)


@pytest.mark.parametrize("asynchronous", [False, True])
def test_completed_candidates_are_transformed_before_document_is_retained(asynchronous):
    original = {"result": {"candidates": [{"item_id": "a", "evidence": {"item": {"text": "large"}}},
                                        {"item_id": "b", "evidence": {"item": {"text": "second"}}}]},
                "result.candidates.item": {"item_id": "spoof"},
                "item": [{"item_id": "unrelated"}]}
    observed = []

    def compact(path, value):
        observed.append(path)
        if len(path) == 3 and path[:2] == ("result", "candidates") and type(path[2]) is int:
            assert "text" in value["evidence"]["item"]
            return {"reference": value["item_id"]}
        return value

    result = parse(json.dumps(original).encode(), asynchronous, compact)
    assert result["result"]["candidates"] == [{"reference": "a"}, {"reference": "b"}]
    assert result["result.candidates.item"] == original["result.candidates.item"]
    assert result["item"] == original["item"]
    assert ("result", "candidates", 0, "evidence", "item") in observed
    assert observed[-1] == ()


def test_transform_runs_before_large_document_is_fully_read():
    payload = json.dumps({"candidates": [{"text": "x" * 40000} for _ in range(20)]}).encode()
    reader = BoundedReader(payload)
    offsets = []

    def compact(path, value):
        if len(path) == 2 and path[0] == "candidates":
            offsets.append(reader.tell())
            return {"bytes": len(value["text"])}
        return value

    assert load(reader, transform=compact) == {"candidates": [{"bytes": 40000}] * 20}
    assert offsets[0] < len(payload)
    assert offsets == sorted(offsets)


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("payload", [
    b"", b" ", b"{", b'{"key":', b'[1,2', b'{"a":1,}', b'{}{}', b'{} true',
    b'NaN', b'Infinity', b'1e9999', b'-1e9999', b'{"x":"\xff"}',
])
def test_invalid_incomplete_trailing_and_nonfinite_data_is_rejected(payload, asynchronous):
    with pytest.raises(ValueError):
        parse(payload, asynchronous)


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("payload", [b"null", b"true", b"1", b'"value"', b"[]", b"{}", b'{} \n\t'])
def test_single_json_values_and_trailing_whitespace(payload, asynchronous):
    assert parse(payload, asynchronous) == json.loads(payload)


def test_binary_reader_never_reads_ahead_for_zero_and_limits_oversized_chunks():
    async def check():
        requested = []

        async def source():
            requested.append(True)
            yield b"x" * (CHUNK_BYTES * 2 + 7)

        reader = BinaryChunkReader(source())
        assert await reader.read(0) == b""
        assert not requested
        with pytest.raises(ValueError, match="Unbounded"):
            await reader.read()
        assert await reader.read(CHUNK_BYTES * 10) == b"x" * CHUNK_BYTES
        assert await reader.read(3) == b"xxx"
        assert await reader.read(CHUNK_BYTES) == b"x" * CHUNK_BYTES
        assert await reader.read(CHUNK_BYTES) == b"xxxx"
        assert await reader.read(CHUNK_BYTES) == b""

    asyncio.run(check())


def test_streaming_encoder_expands_one_reference_at_a_time_without_recursion():
    references = [{"reference": str(index)} for index in range(4)]
    expansions = []

    def expand(path, value):
        if len(path) == 2 and path[0] == "candidates" and "reference" in value:
            expansions.append(value["reference"])
            return {**value, "text": "字 " * 20000, "score": -0.0}
        return value

    output = iterencode({"candidates": references}, expand=expand)
    assert not expansions
    pieces = []
    for piece in output:
        pieces.append(piece)
        if "字" in piece:
            # The following reference has not yet been fetched.
            assert len(expansions) == sum("字" in previous for previous in pieces)
    result = json.loads("".join(pieces))
    assert expansions == ["0", "1", "2", "3"]
    assert result == {"candidates": [{**value, "text": "字 " * 20000, "score": -0.0}
                                     for value in references]}


@pytest.mark.parametrize("ensure_ascii", [False, True])
@pytest.mark.parametrize("sort_keys", [False, True])
def test_streaming_encoding_matches_standard_json(ensure_ascii, sort_keys):
    value = {"unicode": "字 😀\n", "rows": [None, True, False, 10**100, -0.0, {"b": 1.0, "a": []}]}
    options = {"ensure_ascii": ensure_ascii, "sort_keys": sort_keys, "separators": (",", ":"), "allow_nan": False}
    assert "".join(iterencode(value, **options)) == json.dumps(value, **options)


def test_streaming_encoding_rejects_circular_references_and_invalid_values():
    value = {}
    value["self"] = value
    with pytest.raises(ValueError, match="Circular"):
        "".join(iterencode(value))
    with pytest.raises(ValueError):
        "".join(iterencode({"bad": float("inf")}))
    with pytest.raises(TypeError):
        "".join(iterencode({"bad": b"bytes"}))


def test_nested_references_expand_but_same_plain_mapping_is_allowed_twice():
    shared = {"text": "unchanged"}

    def expand(path, value):
        return {"child": {"reference": "inner"}} if value == {"reference": "outer"} else (
            {"text": "expanded"} if value == {"reference": "inner"} else value)

    result = json.loads("".join(iterencode([{"reference": "outer"}, shared, shared], expand=expand)))
    assert result == [{"child": {"text": "expanded"}}, shared, shared]


def test_encoder_expansion_paths_cannot_be_spoofed_by_original_row_keys():
    candidate = {"_candidate_ref": "stored"}
    payload = {"candidates": [candidate], "candidates.0": candidate,
               "evidence": {"item": {"_candidate_ref": "original column"}}}
    paths = []

    def expand(path, value):
        paths.append(path)
        return {"full": "record"} if path == ("candidates", 0) else value

    result = json.loads("".join(iterencode(payload, expand=expand)))
    assert result == {**payload, "candidates": [{"full": "record"}]}
    assert ("candidates.0",) in paths
    assert ("evidence", "item") in paths
