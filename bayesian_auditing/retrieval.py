"""Local Qwen question retrieval, followed separately by the existing item judge.

Question and query embeddings use the same encoding: right truncation at 8192
tokens, last-token pooling, and L2 normalization. Retrieval is a single dot
product. Literal matches against the full, untruncated question sort first.
"""

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Iterable


MODEL_ID = "Qwen/Qwen3-Embedding-0.6B"
MODEL_REVISION = "97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3"
MAX_TOKENS = 8192
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "benchmark-caliper" / "question-embeddings"
RETRIEVAL_POLICY = {
    "version": 1,
    "method": "qwen3_embedding",
    "model": MODEL_ID,
    "model_revision": MODEL_REVISION,
    "max_tokens": MAX_TOKENS,
    "truncation": "right",
    "pooling": "last_token",
    "normalization": "l2",
    "similarity": "dot_product",
    "query_instruction": None,
    "indexed_content": "Question content only; grading, reference answers, and benchmark metadata are not embedded",
    "exact_match": "Literal equality of full question text and query, before truncation; exact matches sort first",
    "tie_break": "exact_match descending, similarity descending, evidence_hash ascending",
    "interpretation": "Cosine similarity retrieves a shortlist; the GPT-6 Luna judge separately assesses six validity dimensions",
}


def _fingerprint(value: object) -> str:
    serialized = json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def question_text(evidence: dict) -> str:
    """Extract question content while retaining its literal text for exact matches.

    Ordinary string content is used unchanged. For structured content, join text
    values in their source order, excluding answer/metadata fields and assistant
    messages. The original structure always remains in the evidence for judging.
    """
    content = (evidence.get("item") or {}).get("content")
    excluded = {"answer", "answers", "reference_answer", "reference_answers", "correct_answer",
                "solution", "solutions", "grading_criterion", "verifier", "metadata", "role",
                "type", "id", "item_id", "benchmark_id", "url", "image_url", "asset_manifest"}

    def values(value):
        if isinstance(value, str):
            yield value
        elif isinstance(value, dict):
            if value.get("role") in {"assistant", "tool"}:
                return
            for key, nested in value.items():
                if str(key).casefold() not in excluded:
                    yield from values(nested)
        elif isinstance(value, (list, tuple)):
            for nested in value:
                yield from values(nested)

    return "\n".join(values(content))


def _unit_vectors(values, *, rows: int, dimensions: int | None = None):
    import numpy as np

    vectors = np.asarray(values, dtype=np.float32)
    if vectors.ndim != 2 or vectors.shape[0] != rows or vectors.shape[1] == 0:
        raise ValueError("Encoder must return one nonempty vector per text")
    if dimensions is not None and vectors.shape[1] != dimensions:
        raise ValueError("Embedding dimensions do not match the document index")
    if not np.isfinite(vectors).all():
        raise ValueError("Embeddings must contain only finite values")
    # Use float64 for norms to avoid overflow/underflow, then store float32.
    norms = np.linalg.norm(vectors.astype(np.float64), axis=1, keepdims=True)
    if not np.isfinite(norms).all() or (norms <= 0).any():
        raise ValueError("Embeddings must have a finite, nonzero L2 norm")
    normalized = (vectors / norms).astype(np.float32)
    if not np.allclose(np.linalg.norm(normalized, axis=1), 1.0, rtol=1e-5, atol=1e-6):
        raise ValueError("Could not produce unit-normalized embeddings")
    return normalized


class QwenEncoder:
    """Lazy local Transformers encoder using Qwen's documented pooling method.

    No instruction prefix is added, so identical question/query text follows the
    same encoding path. A CUDA device is used when available; otherwise CPU.
    """

    dimensions = 1024

    def __init__(self, *, device: str | None = None, batch_size: int = 2):
        if batch_size <= 0:
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
                "Local Qwen retrieval requires torch and transformers. "
                "Install bayesian_auditing/requirements-retrieval.txt."
            ) from exc
        self.device = self.device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._tokenizer = AutoTokenizer.from_pretrained(
            MODEL_ID, revision=MODEL_REVISION, padding_side="left", truncation_side="right",
            trust_remote_code=False,
        )
        self._model = AutoModel.from_pretrained(
            MODEL_ID, revision=MODEL_REVISION, trust_remote_code=False,
            torch_dtype=torch.float16 if self.device.startswith("cuda") else torch.float32,
            attn_implementation="sdpa",
        ).to(self.device).eval()

    def encode(self, texts: list[str]):
        import numpy as np

        if not texts:
            return np.empty((0, self.dimensions), dtype=np.float32)
        self._load()
        import torch
        import torch.nn.functional as functional

        batches = []
        for start in range(0, len(texts), self.batch_size):
            inputs = self._tokenizer(
                texts[start:start + self.batch_size], padding=True, truncation=True,
                max_length=MAX_TOKENS, return_tensors="pt",
            ).to(self._model.device)
            with torch.inference_mode():
                output = self._model(**inputs)
                # Left padding ensures the last position is the last real token.
                pooled = output.last_hidden_state[:, -1]
                vectors = functional.normalize(pooled.float(), p=2, dim=1)
            batches.append(vectors.cpu().numpy())
        return np.concatenate(batches)


class _VectorCache:
    def __init__(self, directory: Path, policy: dict):
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        directory.chmod(0o700)
        self.connection = sqlite3.connect(directory / "vectors.sqlite3", timeout=30)
        self.connection.execute("CREATE TABLE IF NOT EXISTS vectors (key TEXT PRIMARY KEY, dimensions INTEGER NOT NULL, vector BLOB NOT NULL)")
        self.connection.commit()
        self.policy = policy

    def key(self, text: str) -> str:
        # Hash full text before tokenization/truncation: different tails cannot
        # accidentally share cache identity or become literal exact matches.
        return _fingerprint({"policy": self.policy, "text": text})

    def get(self, text: str, dimensions: int | None):
        import numpy as np

        record = self.connection.execute(
            "SELECT dimensions, vector FROM vectors WHERE key = ?", (self.key(text),)
        ).fetchone()
        if record is None:
            return None
        try:
            vector = np.frombuffer(record[1], dtype="<f4").reshape(1, record[0])
            return _unit_vectors(vector, rows=1, dimensions=dimensions)[0]
        except (ValueError, TypeError):
            self.connection.execute("DELETE FROM vectors WHERE key = ?", (self.key(text),))
            self.connection.commit()
            return None

    def put(self, text: str, vector):
        self.connection.execute(
            "INSERT OR REPLACE INTO vectors (key, dimensions, vector) VALUES (?, ?, ?)",
            (self.key(text), len(vector), vector.astype("<f4").tobytes()),
        )

    def close(self):
        self.connection.close()


class ItemIndex:
    """Index full-evidence records, sharing vectors for identical question text.

    ``encoder`` may provide ``encode(list[str]) -> array[n, dimensions]`` for
    tests/local integrations. Custom encoders use a separate cache namespace.
    Construction ``cancelled`` is a zero-argument predicate, used only while
    building. ``progress`` receives stage, completed, total, and cache_hits.
    """

    def __init__(self, items: Iterable[dict], cache_dir=None, encoder=None,
                 cancelled=None, progress=None):
        import numpy as np

        def check_cancelled():
            if cancelled is not None and cancelled():
                raise InterruptedError("Question retrieval was cancelled")

        check_cancelled()
        self._encoder = encoder if encoder is not None else QwenEncoder()
        by_hash = {}
        source_maps = defaultdict(dict)
        self.source_rows_seen = 0
        for item in items:
            check_cancelled()
            self.source_rows_seen += 1
            evidence = item["evidence"]
            key = item.get("evidence_hash") or _fingerprint(evidence)
            if key not in by_hash:
                by_hash[key] = {"evidence_hash": key, "evidence": deepcopy(evidence)}
            elif by_hash[key]["evidence"] != evidence:
                raise ValueError(f"Conflicting evidence for evidence_hash {key}")
            sources = item.get("sources", [])
            if "source" in item:
                sources = [*sources, item["source"]]
            for source in sources:
                source_maps[key][_fingerprint(source)] = deepcopy(source)
        self.items = [
            {**by_hash[key], "sources": [source_maps[key][source_key]
                                       for source_key in sorted(source_maps[key])]}
            for key in sorted(by_hash)
        ]
        self.total = len(self.items)
        self.source_references = sum(len(item["sources"]) for item in self.items)
        self._questions = [question_text(item["evidence"]) for item in self.items]
        self._searchable = [i for i, text in enumerate(self._questions) if text.strip()]
        self.indexed_items = len(self._searchable)
        self.contentless_items = self.total - self.indexed_items
        unique_questions = list(dict.fromkeys(self._questions[i] for i in self._searchable))
        self.unique_questions = len(unique_questions)
        self.cache_hits = 0
        self.embedded_questions = 0
        self._vectors = np.empty((0, 0), dtype=np.float32)
        if not unique_questions:
            return
        policy = deepcopy(RETRIEVAL_POLICY)
        if encoder is not None and not isinstance(encoder, QwenEncoder):
            policy["encoder"] = getattr(encoder, "cache_namespace", f"{type(encoder).__module__}.{type(encoder).__qualname__}")
        cache = _VectorCache(Path(cache_dir) if cache_dir is not None else DEFAULT_CACHE_DIR, policy)
        dimensions = getattr(self._encoder, "dimensions", None)
        vectors_by_text = {}
        pending = []

        def report_progress():
            if progress is not None:
                progress({"stage": "embedding", "completed": len(vectors_by_text),
                          "total": self.unique_questions, "cache_hits": self.cache_hits})

        try:
            for text in unique_questions:
                check_cancelled()
                vector = cache.get(text, dimensions)
                if vector is None:
                    pending.append(text)
                else:
                    dimensions = len(vector)
                    vectors_by_text[text] = vector
                    self.cache_hits += 1
            report_progress()
            # Bound activation memory and allow cancellation between model calls.
            for start in range(0, len(pending), 2):
                check_cancelled()
                texts = pending[start:start + 2]
                vectors = _unit_vectors(self._encoder.encode(texts), rows=len(texts), dimensions=dimensions)
                dimensions = vectors.shape[1]
                check_cancelled()
                for text, vector in zip(texts, vectors):
                    vectors_by_text[text] = vector
                    cache.put(text, vector)
                cache.connection.commit()
                self.embedded_questions += len(texts)
                report_progress()
        finally:
            cache.close()
        self._vectors = np.stack([vectors_by_text[self._questions[i]] for i in self._searchable])

    def search(self, query: str, top_k: int | None = 20, *, cancelled=None) -> list[dict]:
        """Return exact matches first, then a single normalized dot-product score.

        Full question text, not its truncated prefix, determines literal equality.
        Blank queries and corpora without question text return no candidates.
        Query vectors are computed afresh and are never added to the disk cache.
        An optional cancellation predicate belongs only to this search.
        """
        import numpy as np

        def check_cancelled():
            if cancelled is not None and cancelled():
                raise InterruptedError("Question retrieval was cancelled")

        if not isinstance(query, str):
            raise ValueError("query must be text")
        if top_k is not None and (isinstance(top_k, bool) or not isinstance(top_k, int) or top_k <= 0):
            raise ValueError("top_k must be a positive integer or None")
        check_cancelled()
        if not query.strip() or not self._searchable:
            return []
        query_vector = _unit_vectors(self._encoder.encode([query]), rows=1, dimensions=self._vectors.shape[1])[0]
        check_cancelled()
        similarities = self._vectors @ query_vector
        # Unit float32 vectors can exceed ±1 by a few ULPs. Clipping protects
        # that numeric boundary without adding any ranking component.
        similarities = np.clip(similarities, -1.0, 1.0)
        exact = [self._questions[document] == query for document in self._searchable]
        order = sorted(range(len(self._searchable)), key=lambda row: (
            not exact[row], -float(similarities[row]),
            self.items[self._searchable[row]]["evidence_hash"],
        ))
        if top_k is not None:
            order = order[:top_k]
        return [
            {**self.items[self._searchable[row]], "retrieval_rank": rank,
             "retrieval_score": float(similarities[row]), "exact_match": exact[row]}
            for rank, row in enumerate(order, 1)
        ]
