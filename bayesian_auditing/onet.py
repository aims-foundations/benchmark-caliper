"""Search the supplied O*NET reference table using BGE, BM25, and rank fusion.

Retrieval proposes reference records; the separate mapping step decides which
passages apply to the user's task. No benchmark questions are searched here.
"""

from __future__ import annotations

from copy import deepcopy
import csv
import hashlib
from pathlib import Path
import re


DEFAULT_MATERIALS_DIR = Path(__file__).resolve().parents[1] / "materials"
MODEL_ID = "BAAI/bge-small-en-v1.5"
MODEL_REVISION = "5c38ec7c405ec4b44b94cc5a9bb96e735b38267a"
QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "
MAX_TOKENS = 512
RRF_K = 60
BM25_K1 = 1.5
BM25_B = 0.75
BM25_EPSILON = 0.25
DEFAULT_DENSE_K = 50
DEFAULT_BM25_K = 50
DEFAULT_LIMIT = 20
CSV_FIELDS = ("doc_id", "kind", "name", "text", "occupation_id")


def _check_cancelled(cancelled):
    if cancelled is not None and cancelled():
        raise InterruptedError("O*NET retrieval was cancelled")


def _tokens(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text.casefold())


def _unit_vectors(values, rows: int, dimensions: int | None = None):
    import numpy as np

    vectors = np.asarray(values, dtype=np.float32)
    if vectors.ndim != 2 or vectors.shape[0] != rows or not vectors.shape[1]:
        raise ValueError("O*NET embeddings must have one nonempty vector per record")
    if dimensions is not None and vectors.shape[1] != dimensions:
        raise ValueError("O*NET query and reference embedding dimensions differ")
    if not np.isfinite(vectors).all():
        raise ValueError("O*NET embeddings must contain only finite values")
    norms = np.linalg.norm(vectors.astype(np.float64), axis=1, keepdims=True)
    if (norms <= 0).any():
        raise ValueError("O*NET embeddings must have nonzero norms")
    return vectors, norms


class BGEEncoder:
    """Lazy local encoder following BGE's documented CLS/L2 encoding.

    ``encode`` does not add instructions. The index prefixes search queries,
    while document compatibility checks encode the original CSV text directly.
    Hugging Face downloads the pinned model once and then uses its local cache.
    """

    dimensions = 384

    def __init__(self, *, device: str | None = None, batch_size: int = 8):
        if batch_size < 1:
            raise ValueError("batch_size must be positive")
        self.device = device
        self.batch_size = batch_size
        self._model = None
        self._tokenizer = None

    def _load(self):
        if self._model is not None:
            return
        try:
            import torch
            from transformers import AutoModel, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError(
                "Local O*NET retrieval requires torch and transformers. "
                "Install bayesian_auditing/requirements-retrieval.txt."
            ) from exc
        self.device = self.device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._tokenizer = AutoTokenizer.from_pretrained(
            MODEL_ID, revision=MODEL_REVISION, padding_side="right",
            truncation_side="right", trust_remote_code=False,
        )
        self._model = AutoModel.from_pretrained(
            MODEL_ID, revision=MODEL_REVISION, trust_remote_code=False,
            use_safetensors=True, torch_dtype=torch.float32,
        ).to(self.device).eval()

    def encode(self, texts: list[str], *, cancelled=None):
        import numpy as np

        _check_cancelled(cancelled)
        if not texts:
            return np.empty((0, self.dimensions), dtype=np.float32)
        self._load()
        import torch
        import torch.nn.functional as functional

        batches = []
        for start in range(0, len(texts), self.batch_size):
            _check_cancelled(cancelled)
            inputs = self._tokenizer(
                texts[start:start + self.batch_size], padding=True, truncation=True,
                max_length=MAX_TOKENS, return_tensors="pt",
            ).to(self._model.device)
            with torch.inference_mode():
                output = self._model(**inputs)
                pooled = output.last_hidden_state[:, 0]
                vectors = functional.normalize(pooled.float(), p=2, dim=1)
            batches.append(vectors.cpu().numpy())
        _check_cancelled(cancelled)
        return np.concatenate(batches)


class OnetIndex:
    """Read the prepared reference files and retrieve a bounded candidate list.

    An injected encoder supplies ``encode(list[str]) -> array[n, dimensions]``.
    Before the first dense search, eight evenly spaced records (or all records
    in a smaller corpus) are re-encoded to check compatibility with saved vectors.
    A mismatch fails explicitly; incompatible vectors are never silently used.
    ``cancelled`` is an optional zero-argument predicate.
    """

    def __init__(self, materials_dir=DEFAULT_MATERIALS_DIR, encoder=None, cancelled=None):
        import numpy as np
        try:
            from rank_bm25 import BM25Okapi
        except ImportError as exc:
            raise RuntimeError(
                "Local O*NET retrieval requires rank-bm25. "
                "Install bayesian_auditing/requirements-retrieval.txt."
            ) from exc

        _check_cancelled(cancelled)
        directory = Path(materials_dir)
        table_path = directory / "ONET_index.csv"
        vectors_path = directory / "ONET_embeddings.npz"
        with table_path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != list(CSV_FIELDS):
                raise ValueError("O*NET CSV must contain doc_id, kind, name, text, occupation_id")
            records = []
            for row in reader:
                _check_cancelled(cancelled)
                if None in row or any(row[field] is None for field in CSV_FIELDS):
                    raise ValueError("O*NET CSV contains a malformed row")
                if any(not row[field].strip() for field in CSV_FIELDS[:-1]):
                    raise ValueError("O*NET records require nonempty IDs, kinds, names, and text")
                records.append(row)
        if not records:
            raise ValueError("O*NET index must contain at least one record")
        ids = [record["doc_id"] for record in records]
        if len(set(ids)) != len(ids):
            raise ValueError("O*NET record IDs must be unique")

        with np.load(vectors_path, allow_pickle=False) as saved:
            if set(saved.files) != {"vectors", "doc_ids"}:
                raise ValueError("O*NET NPZ must contain vectors and doc_ids")
            saved_ids = saved["doc_ids"]
            if saved_ids.ndim != 1 or saved_ids.dtype.kind not in {"U", "S"}:
                raise ValueError("O*NET embedding IDs must be a one-dimensional string array")
            if saved_ids.astype(str).tolist() != ids:
                raise ValueError("O*NET embedding IDs must match the CSV IDs in the same order")
            vectors, norms = _unit_vectors(saved["vectors"], len(records))
        if not np.allclose(norms, 1.0, rtol=1e-5, atol=1e-5):
            raise ValueError("Saved O*NET embeddings must be L2-normalized")

        self._records = records
        self._vectors = vectors
        self._encoder = encoder if encoder is not None else BGEEncoder()
        tokenized = [_tokens(record["text"]) for record in records]
        if not any(tokenized):
            raise ValueError("O*NET records must contain searchable words")
        self._token_sets = [set(tokens) for tokens in tokenized]
        self._bm25 = BM25Okapi(tokenized, k1=BM25_K1, b=BM25_B, epsilon=BM25_EPSILON)
        self._policy = {
            "version": 1,
            "method": "bge_bm25_rrf",
            "scope": "Supplied healthcare-focused O*NET catalog; broader domains may need broader coverage",
            "record_count": len(records),
            "files": {
                path.name: {"sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                for path in (table_path, vectors_path)
            },
            "embedding": {
                "model": MODEL_ID if encoder is None else "custom",
                "revision": MODEL_REVISION if encoder is None else None,
                "dimensions": vectors.shape[1], "max_tokens": MAX_TOKENS,
                "pooling": "cls", "normalization": "l2", "truncation": "right",
                "similarity": "dot_product", "query_instruction": QUERY_INSTRUCTION,
                "document_instruction": None, "indexed_content": "CSV text field",
                "compatibility": {"status": "not_checked"},
            },
            "bm25": {
                "implementation": "rank-bm25 BM25Okapi", "k1": BM25_K1,
                "b": BM25_B, "epsilon": BM25_EPSILON,
                "tokenization": "Unicode word tokens after casefold; no stemming or stopword removal",
                "unmatched_records": "Excluded from keyword ranking",
            },
            "fusion": {"method": "reciprocal_rank_fusion", "k": RRF_K,
                       "ranks_start_at": 1, "tie_break": "doc_id ascending"},
            "candidate_limits": {"dense_k": DEFAULT_DENSE_K, "bm25_k": DEFAULT_BM25_K,
                                 "limit": DEFAULT_LIMIT},
        }
        _check_cancelled(cancelled)

    @property
    def policy(self) -> dict:
        return deepcopy(self._policy)

    def _encode(self, texts, cancelled):
        _check_cancelled(cancelled)
        if isinstance(self._encoder, BGEEncoder):
            values = self._encoder.encode(texts, cancelled=cancelled)
        else:
            values = self._encoder.encode(texts)
        _check_cancelled(cancelled)
        vectors, norms = _unit_vectors(values, len(texts), self._vectors.shape[1])
        return (vectors / norms).astype("float32")

    def _verify_embeddings(self, cancelled):
        import numpy as np

        if self._policy["embedding"]["compatibility"]["status"] == "passed":
            return
        indices = np.linspace(0, len(self._records) - 1, min(8, len(self._records)), dtype=int)
        encoded = self._encode([self._records[i]["text"] for i in indices], cancelled)
        similarities = np.sum(encoded * self._vectors[indices], axis=1)
        minimum = float(similarities.min())
        if minimum < 0.9999:
            raise ValueError(
                "Supplied O*NET embeddings do not match the configured encoder. "
                "Rebuild document vectors from the CSV with the pinned BGE settings before searching."
            )
        self._policy["embedding"]["compatibility"] = {
            "status": "passed", "sample_record_ids": [self._records[i]["doc_id"] for i in indices],
            "minimum_cosine": minimum, "required_minimum_cosine": 0.9999,
        }

    def search(self, query: str, *, dense_k=DEFAULT_DENSE_K, bm25_k=DEFAULT_BM25_K,
               limit=DEFAULT_LIMIT, cancelled=None) -> list[dict]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("O*NET search query must be nonempty text")
        for name, value in (("dense_k", dense_k), ("bm25_k", bm25_k), ("limit", limit)):
            if type(value) is not int or value < (1 if name == "limit" else 0):
                raise ValueError(f"{name} must be a {'positive' if name == 'limit' else 'nonnegative'} integer")
        if not dense_k and not bm25_k:
            raise ValueError("At least one O*NET retrieval method must be enabled")
        _check_cancelled(cancelled)
        dense_ranks, bm25_ranks = {}, {}

        def ordered(scores, indices, count):
            return sorted(indices, key=lambda i: (-float(scores[i]), self._records[i]["doc_id"]))[:count]

        if dense_k:
            self._verify_embeddings(cancelled)
            vector = self._encode([QUERY_INSTRUCTION + query], cancelled)[0]
            scores = self._vectors @ vector
            dense_ranks = {i: rank for rank, i in enumerate(ordered(scores, range(len(scores)), dense_k), 1)}
        if bm25_k:
            tokens = _tokens(query)
            query_tokens = set(tokens)
            scores = self._bm25.get_scores(tokens)
            matching = [i for i, words in enumerate(self._token_sets) if query_tokens.intersection(words)]
            bm25_ranks = {i: rank for rank, i in enumerate(ordered(scores, matching, bm25_k), 1)}

        _check_cancelled(cancelled)
        candidates = []
        for i in dense_ranks.keys() | bm25_ranks.keys():
            score = sum(1.0 / (RRF_K + ranks[i]) for ranks in (dense_ranks, bm25_ranks) if i in ranks)
            candidates.append({**self._records[i], "dense_rank": dense_ranks.get(i),
                               "bm25_rank": bm25_ranks.get(i), "rrf_score": score})
        self._policy["candidate_limits"] = {"dense_k": dense_k, "bm25_k": bm25_k, "limit": limit}
        return sorted(candidates, key=lambda candidate: (-candidate["rrf_score"], candidate["doc_id"]))[:limit]
