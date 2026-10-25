"""Encode complete benchmark rows with bounded, nonoverlapping BGE chunks."""

from __future__ import annotations

import numpy as np

from .onet import BGEEncoder, MAX_TOKENS
from .retrieval import _unit_vectors


def _check_cancelled(cancelled):
    if cancelled is not None and cancelled():
        raise InterruptedError("Benchmark encoding was cancelled")


class FullRowBGEEncoder(BGEEncoder):
    """Use every token of a row or query instead of truncating at 512 tokens.

    BGE produces a unit-normalized CLS vector for each chunk. The final vector
    is the L2-normalized, equally weighted mean of all chunk vectors. Only one
    tokenized text and at most ``batch_size`` chunks are held at a time; chunk
    vectors accumulate into one running sum per input text.

    The inherited loader supplies the same pinned tokenizer and BGE weights as
    O*NET retrieval. Step 3 keeps its existing encoder and behavior.
    """

    def _encode_chunks(self, chunks):
        import torch

        inputs = self._tokenizer.pad(chunks, padding=True, return_tensors="pt").to(self._model.device)
        with torch.inference_mode():
            output = self._model(**inputs)
            vectors = output.last_hidden_state[:, 0].float().cpu().numpy()
        return _unit_vectors(vectors, rows=len(chunks), dimensions=self.dimensions)

    def encode(self, texts: list[str], *, cancelled=None):
        _check_cancelled(cancelled)
        if not texts:
            return np.empty((0, self.dimensions), dtype=np.float32)
        self._load()
        special_tokens = self._tokenizer.num_special_tokens_to_add(pair=False)
        payload_size = MAX_TOKENS - special_tokens
        if payload_size < 1:
            raise ValueError("BGE special tokens leave no room for document content")
        cls_id, sep_id = self._tokenizer.cls_token_id, self._tokenizer.sep_token_id
        if special_tokens != 2 or cls_id is None or sep_id is None:
            raise ValueError("The pinned BGE tokenizer must wrap text with CLS and SEP")
        sums = np.zeros((len(texts), self.dimensions), dtype=np.float64)
        counts = np.zeros(len(texts), dtype=np.int64)
        pending, owners = [], []

        def flush():
            _check_cancelled(cancelled)
            vectors = self._encode_chunks(pending)
            _check_cancelled(cancelled)
            for owner, vector in zip(owners, vectors):
                sums[owner] += vector
                counts[owner] += 1
            pending.clear()
            owners.clear()

        for owner, text in enumerate(texts):
            _check_cancelled(cancelled)
            token_ids = self._tokenizer(
                text, add_special_tokens=False, truncation=False,
                return_attention_mask=False, return_token_type_ids=False, verbose=False,
            )["input_ids"]
            # Even an empty query/text has a well-defined special-token chunk.
            for start in range(0, max(1, len(token_ids)), payload_size):
                _check_cancelled(cancelled)
                # The pinned BGE model uses BERT single-sequence formatting.
                # Constructing it explicitly works with Transformers 4 and 5.
                ids = [cls_id, *token_ids[start:start + payload_size], sep_id]
                chunk = {"input_ids": ids, "attention_mask": [1] * len(ids),
                         "token_type_ids": [0] * len(ids)}
                if len(chunk["input_ids"]) > MAX_TOKENS:
                    raise ValueError("A BGE chunk exceeds the model's token limit")
                pending.append(chunk)
                owners.append(owner)
                if len(pending) == self.batch_size:
                    flush()
        if pending:
            flush()
        _check_cancelled(cancelled)
        return _unit_vectors(sums / counts[:, None], rows=len(texts), dimensions=self.dimensions)
