"""Authenticated retrieval on a separate server, with no local-build fallback.

Only task queries and the inventory fingerprint cross this boundary. Provider
keys remain in the website process; retrieved evidence retains its original
policy, full rows, and source locations for subsequent screening and export.
"""

from __future__ import annotations

import asyncio
from contextlib import suppress
from dataclasses import dataclass, field
import ipaddress
import math
import os
import re
from urllib.parse import urlsplit

import httpx

from bayesian_auditing.benchmark_data import row_fingerprint, row_search_text
from bayesian_auditing.benchmark_index import DEFAULT_BM25_K, DEFAULT_DENSE_K, INDEX_VERSION
from bayesian_auditing.data import fingerprint
from bayesian_auditing.onet import CSV_FIELDS, DEFAULT_LIMIT, MODEL_ID, MODEL_REVISION


POLL_SECONDS = 2
REQUEST_TIMEOUT_SECONDS = 20
SEARCH_TIMEOUT_SECONDS = 3600


class RemoteRetrievalError(RuntimeError):
    """An actionable message safe to show without server addresses or secrets."""


@dataclass(frozen=True)
class RemoteRetrieval:
    url: str = field(repr=False)
    token: str = field(repr=False)

    @classmethod
    def from_environment(cls) -> RemoteRetrieval | None:
        url = os.environ.get("ITEM_REVIEW_RETRIEVAL_URL", "").strip()
        token = os.environ.get("ITEM_REVIEW_RETRIEVAL_TOKEN", "").strip()
        if not url and not token:
            return None
        if not url or not token:
            raise RemoteRetrievalError(
                "Remote retrieval requires both its service URL and authentication token. "
                "Please contact the site maintainer."
            )
        try:
            parsed = urlsplit(url)
            host = parsed.hostname
            loopback = host == "localhost"
            if host and not loopback:
                with suppress(ValueError):
                    loopback = ipaddress.ip_address(host).is_loopback
            valid = (host and not parsed.username and not parsed.password
                     and not parsed.query and not parsed.fragment
                     and (parsed.scheme == "https" or (parsed.scheme == "http" and loopback)))
            parsed.port  # Reject malformed ports before building an HTTP client.
        except ValueError:
            valid = False
        if not valid or any(character.isspace() for character in url):
            raise RemoteRetrievalError(
                "Remote retrieval requires an HTTPS service address. "
                "Please contact the site maintainer."
            )
        return cls(url.rstrip("/"), token)

    async def search(self, kind: str, query: str, *, inventory: dict | None = None) -> dict:
        if kind not in {"onet", "benchmark"} or (kind == "benchmark" and inventory is None):
            raise ValueError("A benchmark search requires its pinned inventory")
        payload = {"kind": kind, "query": query}
        if kind == "benchmark":
            payload["inventory_hash"] = fingerprint(inventory)
        # Never follow a redirect with the shared credential to another host.
        async with httpx.AsyncClient(
            base_url=self.url + "/", headers={"Authorization": f"Bearer {self.token}"},
            timeout=REQUEST_TIMEOUT_SECONDS, follow_redirects=False,
        ) as client:
            try:
                return await asyncio.wait_for(
                    self._search(client, payload, inventory), timeout=SEARCH_TIMEOUT_SECONDS,
                )
            except (TimeoutError, httpx.TimeoutException):
                raise RemoteRetrievalError(
                    "Remote retrieval timed out. Check that the retrieval server is available, then retry."
                ) from None
            except httpx.HTTPError:
                raise RemoteRetrievalError(
                    "Could not reach the retrieval server. Check its connection, then retry."
                ) from None

    async def _search(self, client, payload, inventory):
        job_id = None
        submission = asyncio.create_task(client.post("v1/searches", json=payload))
        try:
            try:
                response = await asyncio.shield(submission)
            except asyncio.CancelledError:
                # A cancelled POST may already have started a search. Finish its
                # bounded response so the finally block can cancel that job too.
                with suppress(Exception):
                    submitted = self._response(await submission)
                    job_id = self._job_id(submitted)
                raise
            submitted = self._response(response)
            job_id = self._job_id(submitted)
            while True:
                state = self._response(await client.get(f"v1/searches/{job_id}"))
                status = state.get("status")
                if status == "completed":
                    result = state.get("result")
                    _validate_result(result, payload["kind"], inventory)
                    return result
                if status in {"failed", "cancelled"}:
                    # The remote error may contain a path, query, or credential.
                    raise RemoteRetrievalError(
                        "The retrieval server could not complete this search. "
                        "The site maintainer should check its index and dataset access, then retry."
                    )
                if status not in {"queued", "running"}:
                    raise _invalid_response()
                await asyncio.sleep(POLL_SECONDS)
        finally:
            if job_id is not None:
                # Release completed query/results as well as cancelling work.
                # A network failure here must not overwrite the original error.
                with suppress(httpx.HTTPError):
                    await client.delete(f"v1/searches/{job_id}")

    @staticmethod
    def _job_id(response):
        value = response.get("job_id")
        if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value):
            raise _invalid_response()
        return value

    @staticmethod
    def _response(response):
        if response.status_code in {401, 403}:
            raise RemoteRetrievalError(
                "The retrieval server rejected authentication. "
                "The site maintainer should check the shared retrieval token."
            )
        if response.status_code == 409:
            raise RemoteRetrievalError(
                "The retrieval index does not match this website's pinned item bank. "
                "The site maintainer should align their inventory revisions."
            )
        if response.status_code == 429:
            raise RemoteRetrievalError("The retrieval server is busy. Please retry shortly.")
        if not 200 <= response.status_code < 300:
            raise RemoteRetrievalError(
                "The retrieval server is unavailable. Check that its service is running, then retry."
            )
        try:
            value = response.json()
        except ValueError:
            raise _invalid_response() from None
        if not isinstance(value, dict):
            raise _invalid_response()
        return value


def _invalid_response():
    return RemoteRetrievalError(
        "The retrieval server returned incomplete or incompatible evidence. "
        "The site maintainer should check that both services use matching code and data."
    )


def _validate_result(result, kind, inventory):
    """Reject truncated rows or mismatched provenance instead of weakening queues."""
    try:
        if not isinstance(result, dict) or not isinstance(result["candidates"], list):
            raise ValueError
        policy, candidates = result["policy"], result["candidates"]
        if (not isinstance(policy, dict) or policy["method"] != "bge_bm25_rrf"
                or policy["embedding"]["model"] != MODEL_ID
                or policy["embedding"]["revision"] != MODEL_REVISION):
            raise ValueError
        if kind == "onet":
            if len(candidates) > DEFAULT_LIMIT or policy["candidate_limits"]["limit"] != DEFAULT_LIMIT:
                raise ValueError
            seen = set()
            for candidate in candidates:
                if any(not isinstance(candidate[name], str) for name in CSV_FIELDS):
                    raise ValueError
                if any(not candidate[name].strip() for name in CSV_FIELDS[:-1]):
                    raise ValueError
                if candidate["doc_id"] in seen:
                    raise ValueError
                seen.add(candidate["doc_id"])
            return

        stats = result["stats"]
        if (result["inventory_hash"] != fingerprint(inventory) or policy["version"] != INDEX_VERSION
                or policy["candidate_limits"] != {"dense_k": DEFAULT_DENSE_K, "bm25_k": DEFAULT_BM25_K}
                or stats["source_rows"] != sum(table["row_count"] for table in inventory["tables"])
                or type(stats["indexed_items"]) is not int
                or not 0 <= stats["indexed_items"] <= stats["source_rows"]):
            raise ValueError
        locations = {(table["branch"], table["commit"], table["benchmark"], table["items_path"]): table["row_count"]
                     for table in inventory["tables"]}
        seen, dense_ranks, bm25_ranks = set(), [], []
        for rank, candidate in enumerate(candidates, 1):
            row, item_id = candidate["evidence"]["item"], candidate["item_id"]
            if (item_id in seen or item_id != row_fingerprint(row) or candidate["evidence_hash"] != item_id
                    or candidate["rank"] != rank or candidate["search_text"] != row_search_text(row)
                    or not isinstance(candidate["question_text"], str) or not candidate["sources"]
                    or not math.isfinite(candidate["rrf_score"])):
                raise ValueError
            seen.add(item_id)
            for source in candidate["sources"]:
                location = tuple(source[name] for name in ("branch", "commit", "benchmark", "items_path"))
                if (source["repo"] != inventory["repo"] or location not in locations
                        or type(source["row"]) is not int or not 1 <= source["row"] <= locations[location]
                        or source.get("item_id") != row.get("item_id")):
                    raise ValueError
            for method, ranks in (("dense", dense_ranks), ("bm25", bm25_ranks)):
                method_rank = candidate[f"{method}_rank"]
                if method_rank is not None:
                    if type(method_rank) is not int or method_rank < 1 or not math.isfinite(candidate[f"{method}_score"]):
                        raise ValueError
                    ranks.append(method_rank)
            if candidate["dense_rank"] is None and candidate["bm25_rank"] is None:
                raise ValueError
        # Dense retrieval always returns this many items; losing even one
        # candidate in transport must fail instead of reducing task coverage.
        if (sorted(dense_ranks) != list(range(1, min(DEFAULT_DENSE_K, stats["indexed_items"]) + 1))
                or len(bm25_ranks) > DEFAULT_BM25_K or sorted(bm25_ranks) != list(range(1, len(bm25_ranks) + 1))):
            raise ValueError
    except (KeyError, TypeError, ValueError, OverflowError):
        raise _invalid_response() from None
