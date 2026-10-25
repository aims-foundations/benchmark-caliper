"""Full-row coverage and bounded chunk aggregation, without loading BGE weights."""

import numpy as np
import pytest

from bayesian_auditing.benchmark_encoding import FullRowBGEEncoder
from bayesian_auditing.onet import MAX_TOKENS


class Tokenizer:
    """One whitespace-separated integer is one payload token."""

    cls_token_id = -1
    sep_token_id = -2

    def __call__(self, text, **options):
        assert options["add_special_tokens"] is False
        assert options["truncation"] is False
        return {"input_ids": [int(value) for value in text.split()]}

    def num_special_tokens_to_add(self, pair=False):
        assert not pair
        return 2



class Encoder(FullRowBGEEncoder):
    dimensions = 2

    def __init__(self, batch_size=2):
        super().__init__(batch_size=batch_size)
        self._model = object()
        self._tokenizer = Tokenizer()
        self.batches = []

    def _encode_chunks(self, chunks):
        self.batches.append([list(chunk["input_ids"]) for chunk in chunks])
        # A tail token contributes an independent direction, as a mocked CLS.
        return np.asarray([[0, 1] if 9999 in chunk["input_ids"] else [1, 0]
                           for chunk in chunks], dtype=np.float32)


def test_all_tokens_including_long_tail_contribute_to_final_vector():
    encoder = Encoder()
    payload = list(range(1, 1100)) + [9999]
    vector = encoder.encode([" ".join(map(str, payload))])[0]
    chunks = [chunk for batch in encoder.batches for chunk in batch]
    assert [token for chunk in chunks for token in chunk[1:-1]] == payload
    assert [len(chunk) for chunk in chunks] == [512, 512, 82]
    assert all(chunk[0] == -1 and chunk[-1] == -2 for chunk in chunks)
    assert [len(batch) for batch in encoder.batches] == [2, 1]
    assert vector == pytest.approx(np.array([2, 1]) / np.sqrt(5))
    assert vector[1] > 0  # A truncating encoder would never see the tail token.


def test_chunks_from_different_rows_do_not_mix_their_means():
    encoder = Encoder(batch_size=3)
    vectors = encoder.encode(["1 " * 511 + "9999", "9999", "3"])
    assert [len(batch) for batch in encoder.batches] == [3, 1]
    assert vectors[0] == pytest.approx([1 / np.sqrt(2), 1 / np.sqrt(2)])
    assert vectors[1] == pytest.approx([0, 1])
    assert vectors[2] == pytest.approx([1, 0])
    assert vectors.dtype == np.float32


def test_exact_payload_boundary_uses_one_chunk_without_losing_special_tokens():
    encoder = Encoder()
    encoder.encode(["1 " * (MAX_TOKENS - 2)])
    assert len(encoder.batches) == 1 and len(encoder.batches[0]) == 1
    assert len(encoder.batches[0][0]) == MAX_TOKENS


def test_many_chunks_remain_bounded_and_empty_input_is_supported():
    encoder = Encoder(batch_size=3)
    encoder.encode(["1 " * 10000, ""])
    assert all(len(batch) <= 3 for batch in encoder.batches)
    assert encoder.batches[-1][-1] == [-1, -2]
    assert encoder.encode([]).shape == (0, 2)


def test_cancellation_between_chunks_does_not_return_partial_embedding():
    encoder = Encoder(batch_size=1)
    with pytest.raises(InterruptedError, match="cancelled"):
        encoder.encode(["1 " * 1500], cancelled=lambda: bool(encoder.batches))
    assert len(encoder.batches) == 1


def test_invalid_special_token_configuration_fails():
    encoder = Encoder()
    encoder._tokenizer.num_special_tokens_to_add = lambda pair: MAX_TOKENS
    with pytest.raises(ValueError, match="no room"):
        encoder.encode(["1"])
