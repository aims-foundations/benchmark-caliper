import json
from pathlib import Path
from types import SimpleNamespace

import pyarrow as pa
import pyarrow.parquet as pq
import pytest
import yaml

from website.server import item_analysis_databank as bank


REVISION = "a" * 40
PROCESSED_REPO = "aims-foundations/measurement-db-pp"
OLD_REPO = "aims-foundations/measurement-db"


def entry(slug="mmlu", **changes):
    return {"id": f"databank:{REVISION}:{slug}", "benchmark": slug,
            "title": "MMLU" if slug == "mmlu" else slug, "aliases": [],
            "repo": bank.REPO, "revision": REVISION, "source_revision": REVISION,
            "paper_urls": ["https://arxiv.org/abs/2009.03300"], "source_urls": [],
            "identifiers": ["arxiv:2009.03300"], "version": None,
            "available": True, "unavailable_reason": None, "item_count": 2,
            "requires_confirmation": True, **changes}


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    monkeypatch.setattr(bank, "_catalogs", {})
    monkeypatch.setattr(bank, "_latest", None)
    monkeypatch.setattr(bank, "_refreshing", False)
    monkeypatch.setattr(bank, "_refresh_failed", False)
    monkeypatch.setattr(bank, "_last_refresh", 0)
    monkeypatch.setattr(bank, "_cache_dir", lambda: tmp_path / "cache")
    monkeypatch.setattr(bank, "BUNDLED_CATALOG", tmp_path / "catalog.json")
    monkeypatch.setattr(bank, "_schedule_refresh", lambda: None)
    monkeypatch.setattr(bank, "get_token", lambda: "private-test-token")


def publish(entries):
    catalog = {"version": 2, "repo": bank.REPO, "revision": REVISION, "entries": entries}
    bank.BUNDLED_CATALOG.write_text(json.dumps(catalog))
    return catalog


def assessment(name="mmlu", **identity):
    return {"benchmark": name, "benchmark_name": name, "benchmark_identity": identity}


@pytest.mark.parametrize(("value", "expected"), [
    ("https://arxiv.org/pdf/2009.03300v3.pdf", "arxiv:2009.03300"),
    ("arXiv:2009.03300v2", "arxiv:2009.03300"),
    ("https://doi.org/10.1000/ABC.Def", "doi:10.1000/abc.def"),
    ("doi:10.1000/ABC.Def", "doi:10.1000/abc.def"),
    ("https://github.com/Hendrycks/test.git/tree/main?x=1", "github:hendrycks/test"),
    ("https://huggingface.co/datasets/OpenAI/gsm8k/tree/main", "hf:openai/gsm8k"),
    ("https://[bad", None),
    ("[", None),
])
def test_canonical_identifiers(value, expected):
    assert bank.canonical_identifier(value) == expected


def test_search_exact_identifier_alias_fuzzy_and_required_confirmation():
    publish([entry(), entry("mmlupro", title="MMLU-Pro"),
             entry("renamed", title="Unrelated renamed title", aliases=["MMLU Classic"],
                   identifiers=["doi:10.1000/example"], paper_urls=[]),
             entry("other", title="Unrelated", identifiers=[], paper_urls=[])])
    matches = bank.search_candidates(assessment("Measuring Massive Multitask Language Understanding",
                                              paper_urls=["https://arxiv.org/pdf/2009.03300v2.pdf"]))
    assert matches["candidates"][0]["match_type"] == "identifier"
    assert matches["requires_confirmation"]
    assert all(c["requires_confirmation"] for c in matches["candidates"])
    assert "suggested_source_id" not in matches
    assert bank.search_candidates(assessment("MMLU Classic"))["candidates"][0]["benchmark"] == "renamed"
    fuzzy = bank.search_candidates(assessment("mmlupro"))["candidates"]
    assert fuzzy[0]["benchmark"] == "mmlupro"
    assert next(c for c in fuzzy if c["benchmark"] == "mmlu")["conflicts"]
    assert all(c["benchmark"] != "other" for c in matches["candidates"])


def test_explicit_version_conflict_and_search_without_automatic_match():
    publish([entry(version="v1"), entry("mathdial", title="MathDial", identifiers=[], paper_urls=[])])
    result = bank.search_candidates(assessment(version="v2"))
    assert "Release differs" in result["candidates"][0]["conflicts"][0]
    assert bank.search_candidates(assessment("unknown zzzz"))["candidates"] == []
    manual = bank.search_candidates(assessment("unknown zzzz"), "mathdial")
    assert manual["candidates"][0]["benchmark"] == "mathdial"
    assert manual["candidates"][0]["conflicts"]
    assert manual["candidates"][0]["match_type"] == "search"
    assert bank.search_candidates(assessment(), "  ")["candidates"][0]["benchmark"] == "mmlu"


def test_search_does_not_use_deployment_as_identity():
    publish([entry()])
    context = assessment("a wholly separate benchmark")
    context["deployment"] = "MMLU https://arxiv.org/abs/2009.03300"
    assert bank.search_candidates(context)["candidates"] == []


def test_documented_language_and_paper_mismatch_are_explained():
    publish([entry(languages=["English"])])
    result = bank.search_candidates(assessment(languages=["hi"], paper_urls=["https://arxiv.org/abs/2401.12345"]))
    conflicts = result["candidates"][0]["conflicts"]
    assert any("language differs" in value for value in conflicts)
    assert any("paper identifier differs" in value for value in conflicts)
    matched = bank.search_candidates(assessment(languages=["en-US"], paper_urls=["https://arxiv.org/pdf/2009.03300v2.pdf"]))
    assert not matched["candidates"][0]["conflicts"]
    assert bank.search_candidates(assessment(), "https://[bad")["candidates"] == []


def test_missing_access_and_refresh_failure_remain_visible(monkeypatch):
    publish([entry()])
    monkeypatch.setattr(bank, "get_token", lambda: None)
    monkeypatch.setattr(bank, "_refresh_failed", True)
    result = bank.search_candidates(assessment())
    assert result["status"] == "cached"
    assert not result["candidates"][0]["available"]
    assert "access" in result["candidates"][0]["unavailable_reason"]
    assert "token" not in json.dumps(result)


def test_no_catalog_returns_safe_unavailable():
    result = bank.search_candidates(assessment())
    assert result["status"] == "unavailable"
    assert not result["candidates"]


def test_revision_bound_resolve_retains_previous_catalog(tmp_path):
    original = entry()
    publish([original])
    assert bank.resolve_candidate(original["id"])["source_revision"] == REVISION
    new = "b" * 40
    bank._catalogs[new] = {"version": 2, "repo": bank.REPO, "revision": new, "entries": []}
    bank._latest = new
    assert bank.resolve_candidate(original["id"])["id"] == original["id"]
    with pytest.raises(bank.DataBankError, match="expired"):
        bank.resolve_candidate(f"databank:{'c' * 40}:mmlu")
    with pytest.raises(bank.DataBankError, match="invalid"):
        bank.resolve_candidate(f"databank:{REVISION}:../../private")


def test_old_repository_cache_and_saved_selection_cannot_be_reused():
    old_revision = "d" * 40
    old = entry("old-only", id=f"databank:{old_revision}:old-only", repo=OLD_REPO,
                revision=old_revision, source_revision=old_revision)
    cached = {"version": 2, "repo": OLD_REPO, "revision": old_revision, "entries": [old]}
    bank._cache_dir().mkdir()
    for filename in ("latest.json", f"{old_revision}.json"):
        (bank._cache_dir() / filename).write_text(json.dumps(cached))
    current = publish([entry()])
    result = bank.search_candidates(assessment())
    assert result["repo"] == PROCESSED_REPO and result["revision"] == REVISION
    assert bank._load_catalog() == current
    assert old_revision not in bank._catalogs
    assert bank.resolve_candidate(entry()["id"])["repo"] == PROCESSED_REPO
    with pytest.raises(bank.DataBankError, match="expired"):
        bank.resolve_candidate(old["id"])


def test_old_repository_cache_is_not_used_when_no_processed_catalog_exists():
    old = {"version": 2, "repo": OLD_REPO, "revision": REVISION, "entries": [entry(repo=OLD_REPO)]}
    bank._cache_dir().mkdir()
    (bank._cache_dir() / "latest.json").write_text(json.dumps(old))
    bank.BUNDLED_CATALOG.write_text(json.dumps(old))
    assert bank.search_candidates(assessment())["status"] == "unavailable"
    assert not bank._catalogs
    with pytest.raises(bank.DataBankError, match="expired"):
        bank.resolve_candidate(entry()["id"])


def test_old_public_only_catalog_at_same_repo_and_revision_is_replaced_by_expanded_bundle():
    public_only = {"version": 1, "repo": PROCESSED_REPO, "revision": REVISION,
                   "entries": [entry(release="public")]}
    bank._cache_dir().mkdir()
    for filename in ("latest.json", f"{REVISION}.json"):
        (bank._cache_dir() / filename).write_text(json.dumps(public_only))
    expanded = publish([entry(release="public"), entry("mathdial", title="MathDial", release="private", identifiers=[])])
    result = bank.search_candidates(assessment("MathDial"))
    assert result["revision"] == REVISION
    assert result["candidates"][0]["benchmark"] == "mathdial"
    assert result["candidates"][0]["available"] and result["candidates"][0]["release"] == "private"
    assert bank._load_catalog() == expanded
    assert not bank._valid_catalog(public_only)
    assert bank._valid_catalog(expanded)
    assert bank.resolve_candidate(f"databank:{REVISION}:mathdial")["release"] == "private"

    class Api:
        def list_repo_refs(self, *args, **kwargs):
            return SimpleNamespace(branches=[SimpleNamespace(name="main", target_commit=REVISION)])

        def list_repo_tree(self, *args, **kwargs):
            pytest.fail("A matching expanded catalog is already available at this revision")

    assert bank.refresh_catalog(api=Api(), skip_if_unchanged=True) == expanded


def test_legacy_catalog_cannot_restore_a_revision_selection_without_an_expanded_catalog():
    bank._cache_dir().mkdir()
    (bank._cache_dir() / f"{REVISION}.json").write_text(json.dumps({
        "version": 1, "repo": PROCESSED_REPO, "revision": REVISION, "entries": [entry()],
    }))
    with pytest.raises(bank.DataBankError, match="expired"):
        bank.resolve_candidate(entry()["id"])


def test_background_failure_preserves_existing_catalog(monkeypatch):
    publish([entry()])
    bank._load_catalog()
    monkeypatch.setattr(bank, "refresh_catalog", lambda **kwargs: (_ for _ in ()).throw(RuntimeError("private-test-token")))
    bank._refresh_worker()
    assert bank.search_candidates(assessment())["status"] == "cached"
    assert bank.resolve_candidate(entry()["id"])["benchmark"] == "mmlu"
    assert not bank._refreshing


def discovery_fixture(tmp_path, monkeypatch, *, release="public", granularity="item", modality=None, footer=None):
    metadata = tmp_path / "metadata.yaml"
    metadata.write_text(yaml.safe_dump({"benchmark": {"name": "MMLU", "release": release,
        "granularity": granularity, "modality": ["text"] if modality is None else modality,
        "paper_url": "https://arxiv.org/abs/2009.03300", "version": "v1", "testing_condition": "Original test release"}}))
    characterization = tmp_path / "characterization.yaml"
    characterization.write_text(yaml.safe_dump({"tables": {"items": {"rows": 2}}}))
    benchmarks = tmp_path / "benchmarks.parquet"
    pq.write_table(pa.Table.from_pylist([{"benchmark_id": "mmlu", "name": "MMLU", "release": release}]), benchmarks)
    paths = {"mmlu/metadata.yaml": metadata, "mmlu/characterization.yaml": characterization,
             "mmlu/formatted_tables/benchmarks.parquet": benchmarks}
    requests = []

    def download(path, revision, token):
        requests.append(path)
        assert revision == REVISION
        assert not path.endswith("items.parquet")
        return paths[path]

    monkeypatch.setattr(bank, "_metadata_file", download)
    monkeypatch.setattr(bank, "_inspect_footer", lambda *args: footer or {
        "item_count": 2, "columns": ["item_id", "benchmark_id", "content"], "uncompressed_bytes": 1000})

    class Api:
        def list_repo_refs(self, *args, **kwargs):
            return SimpleNamespace(branches=[SimpleNamespace(name="main", target_commit=REVISION)])

        def list_repo_tree(self, *args, **kwargs):
            path = kwargs.get("path_in_repo")
            if not path:
                return [SimpleNamespace(path="mmlu")]
            if path == "mmlu":
                return [SimpleNamespace(path=name, size=file.stat().st_size) for name, file in paths.items()
                        if name.count("/") == 1] + [SimpleNamespace(path="mmlu/formatted_tables")]
            return [SimpleNamespace(path="mmlu/formatted_tables/benchmarks.parquet", size=1000),
                    SimpleNamespace(path="mmlu/formatted_tables/items.parquet", size=500,
                                    lfs=SimpleNamespace(sha256="c" * 64))]

    return Api(), requests


def test_refresh_uses_repository_metadata_and_footers_not_item_rows(tmp_path, monkeypatch):
    api, requests = discovery_fixture(tmp_path, monkeypatch)
    result = bank.refresh_catalog(api=api)
    candidate = result["entries"][0]
    assert result["revision"] == REVISION
    assert result["version"] == 2
    assert candidate["available"]
    assert candidate["item_count"] == 2
    assert candidate["sha256"] == "c" * 64
    assert candidate["benchmark_ids"] == ["mmlu"]
    assert candidate["testing_scope"] == "Original test release"
    assert all(not path.endswith("items.parquet") for path in requests)
    assert "private-test-token" not in json.dumps(result)


def test_private_release_is_eligible_and_keeps_original_metadata_label(tmp_path, monkeypatch):
    api, _ = discovery_fixture(tmp_path, monkeypatch, release="private")
    candidate = bank._build_entry("mmlu", REVISION, api, "private-test-token")
    assert candidate["available"] and candidate["release"] == "private"
    publish([candidate])
    match = bank.search_candidates(assessment())["candidates"][0]
    assert match["available"] and match["release"] == "private"


def processed_discovery_fixture(tmp_path, monkeypatch, *, rows=None, declared=None,
                                formatted=False, root_benchmark=True):
    """The processed bank may publish only paired root Parquet tables."""
    default_row = {
        "benchmark_id": "db5b91e17168483fbd3c3dbb733d0018", "name": "Massive Multitask Language Understanding",
        "aliases": ["MMLU"], "release": "public", "granularity": "item", "modality": ["text"],
        "paper_url": "https://arxiv.org/abs/2009.03300", "dataset_source": "https://github.com/hendrycks/test",
        "version": "v1", "split": "test", "testing_condition": "Original 57-subject test release",
        "benchmark_features": json.dumps({"language": "English"}),
    }
    paths = {}
    if root_benchmark:
        benchmark_path = tmp_path / "root-benchmarks.parquet"
        pq.write_table(pa.Table.from_pylist(rows if rows is not None else [default_row]), benchmark_path)
        paths["mmlu/benchmarks.parquet"] = benchmark_path
    if declared is not None:
        metadata = tmp_path / "processed-metadata.yaml"
        metadata.write_text(yaml.safe_dump({"benchmark": declared}))
        paths["mmlu/metadata.yaml"] = metadata
    if formatted:
        legacy = tmp_path / "legacy-benchmarks.parquet"
        pq.write_table(pa.Table.from_pylist([{**default_row, "benchmark_id": "mmlu", "name": "Old formatted table", "paper_url": "https://arxiv.org/abs/9999.99999"}]), legacy)
        paths["mmlu/formatted_tables/benchmarks.parquet"] = legacy
    requests, footer_requests, api_calls = [], [], []

    def metadata_file(path, revision, token):
        assert revision == REVISION and token == "private-test-token"
        assert not path.endswith("items.parquet")
        requests.append(path)
        return paths[path]

    def footer(path, revision, token):
        footer_requests.append((path, revision))
        assert token == "private-test-token"
        return {"item_count": 14042 if path == "mmlu/items.parquet" else 2,
                "columns": ["item_id", "benchmark_id", "content"], "uncompressed_bytes": 1000}

    class Api:
        def list_repo_refs(self, repo_id, **kwargs):
            assert repo_id == PROCESSED_REPO and kwargs["repo_type"] == "dataset"
            return SimpleNamespace(branches=[SimpleNamespace(name="main", target_commit=REVISION)])

        def list_repo_tree(self, repo_id, **kwargs):
            assert repo_id == PROCESSED_REPO
            assert kwargs["repo_type"] == "dataset" and kwargs["revision"] == REVISION
            parent = kwargs.get("path_in_repo")
            api_calls.append(parent)
            if parent is None:
                return [SimpleNamespace(path="mmlu")]
            found = [SimpleNamespace(path=name, size=path.stat().st_size) for name, path in paths.items() if str(Path(name).parent) == parent]
            if parent == "mmlu":
                found.append(SimpleNamespace(path="mmlu/items.parquet", size=500, lfs=SimpleNamespace(sha256="c" * 64)))
                if formatted:
                    found.append(SimpleNamespace(path="mmlu/formatted_tables"))
            elif parent == "mmlu/formatted_tables":
                found.append(SimpleNamespace(path="mmlu/formatted_tables/items.parquet", size=600, lfs=SimpleNamespace(sha256="e" * 64)))
            return found

    monkeypatch.setattr(bank, "_metadata_file", metadata_file)
    monkeypatch.setattr(bank, "_inspect_footer", footer)
    return Api(), requests, footer_requests, api_calls, default_row


def test_processed_root_tables_without_yaml_provide_mmlu_identity_and_matching(tmp_path, monkeypatch):
    api, requests, footer_requests, _, row = processed_discovery_fixture(tmp_path, monkeypatch)
    catalog = bank.refresh_catalog(api=api)
    assert bank.REPO == catalog["repo"] == PROCESSED_REPO
    candidate = catalog["entries"][0]
    assert candidate["available"] and candidate["release"] == "public"
    assert candidate["benchmark_ids"] == [row["benchmark_id"]]
    assert candidate["title"] == row["name"] and "MMLU" in candidate["aliases"]
    assert candidate["item_count"] == 14042 and candidate["table_path"] == "mmlu/items.parquet"
    assert candidate["version"] == "v1" and candidate["split"] == "test"
    assert candidate["testing_scope"] == row["testing_condition"] and candidate["languages"] == ["English"]
    assert candidate["paper_urls"] == [row["paper_url"]]
    assert candidate["source_urls"] == [row["dataset_source"]]
    assert candidate["metadata_url"] == f"https://huggingface.co/datasets/{PROCESSED_REPO}/blob/{REVISION}/mmlu/benchmarks.parquet"
    assert candidate["source_url"] == f"https://huggingface.co/datasets/{PROCESSED_REPO}/blob/{REVISION}/mmlu/items.parquet"
    assert requests == ["mmlu/benchmarks.parquet"]
    assert footer_requests == [("mmlu/items.parquet", REVISION)]
    publish([candidate])
    named = bank.search_candidates(assessment("MMLU"))["candidates"][0]
    assert named["id"] == candidate["id"] and named["match_type"] == "exact_name"
    for identity in ({"paper_urls": ["https://arxiv.org/pdf/2009.03300v2.pdf"]},
                     {"source_urls": ["https://github.com/hendrycks/test/tree/master"]}):
        matched = bank.search_candidates(assessment("Different display name", **identity))["candidates"][0]
        assert matched["id"] == candidate["id"] and matched["match_type"] == "identifier"
        assert matched["requires_confirmation"]


@pytest.mark.parametrize("release", ["private", "restricted", None, ""])
def test_table_only_nonpublic_or_missing_release_remains_eligible(tmp_path, monkeypatch, release):
    row = {"benchmark_id": "mmlu", "name": "MMLU", "granularity": "item", "modality": ["text"]}
    if release is not None:
        row["release"] = release
    api, requests, footer_requests, _, _ = processed_discovery_fixture(tmp_path, monkeypatch, rows=[row])
    candidate = bank._build_entry("mmlu", REVISION, api, "private-test-token")
    assert candidate["available"] and candidate["release"] == release
    assert requests == ["mmlu/benchmarks.parquet"] and footer_requests == [("mmlu/items.parquet", REVISION)]


@pytest.mark.parametrize("rows", [
    [{"benchmark_id": "mmlu", "release": "public"}, {"benchmark_id": "12345", "release": "private"}],
    [{"benchmark_id": "mmlu", "release": "public"}, {"benchmark_id": "12345"}],
])
def test_mixed_release_rows_are_eligible_when_identity_and_item_schema_are_valid(tmp_path, monkeypatch, rows):
    rows = [{"granularity": "item", "modality": ["text"], **row} for row in rows]
    api, _, footer_requests, _, _ = processed_discovery_fixture(tmp_path, monkeypatch, rows=rows,
                                                               declared={"release": "public"})
    candidate = bank._build_entry("mmlu", REVISION, api, "private-test-token")
    assert candidate["available"] and set(candidate["benchmark_ids"]) == {"mmlu", "12345"}
    assert footer_requests == [("mmlu/items.parquet", REVISION)]


def test_private_yaml_does_not_block_an_otherwise_eligible_root_table(tmp_path, monkeypatch):
    api, _, footer_requests, _, _ = processed_discovery_fixture(tmp_path, monkeypatch, declared={"release": "private"})
    candidate = bank._build_entry("mmlu", REVISION, api, "private-test-token")
    assert candidate["available"] and candidate["release"] == "private"
    assert footer_requests == [("mmlu/items.parquet", REVISION)]


def test_root_item_table_uses_root_identity_instead_of_formatted_metadata(tmp_path, monkeypatch):
    api, requests, footer_requests, _, row = processed_discovery_fixture(tmp_path, monkeypatch, formatted=True)
    candidate = bank._build_entry("mmlu", REVISION, api, "private-test-token")
    assert candidate["available"] and candidate["table_path"] == "mmlu/items.parquet"
    assert candidate["benchmark_ids"] == [row["benchmark_id"]]
    assert candidate["sha256"] == "c" * 64 and candidate["item_count"] == 14042
    assert candidate["paper_urls"] == [row["paper_url"]]
    assert requests == ["mmlu/benchmarks.parquet"] and footer_requests == [("mmlu/items.parquet", REVISION)]


def test_root_items_without_identity_stay_visible_but_cannot_borrow_formatted_metadata(tmp_path, monkeypatch):
    api, requests, footer_requests, _, _ = processed_discovery_fixture(tmp_path, monkeypatch, formatted=True, root_benchmark=False)
    candidate = bank._build_entry("mmlu", REVISION, api, "private-test-token")
    assert candidate is not None and not candidate["available"]
    assert candidate["table_path"] == "mmlu/items.parquet" and candidate["benchmark_ids"] == []
    assert "identity mapping" in candidate["unavailable_reason"]
    assert not requests and footer_requests == [("mmlu/items.parquet", REVISION)]
    publish([candidate])
    match = bank.search_candidates(assessment())["candidates"][0]
    assert match["id"] == candidate["id"] and not match["available"]


def test_same_revision_refresh_avoids_corpus_scan():
    catalog = publish([entry()])

    class Api:
        def list_repo_refs(self, *args, **kwargs):
            return SimpleNamespace(branches=[SimpleNamespace(name="main", target_commit=REVISION)])

        def list_repo_tree(self, *args, **kwargs):
            pytest.fail("Unchanged main should not scan metadata again")

    assert bank.refresh_catalog(api=Api(), skip_if_unchanged=True) == catalog


def test_source_links_only_allow_http_and_https():
    assert bank._safe_urls(["javascript:alert(1)", "https://[bad", "https://user:secret@host.test/x",
                            "https://arxiv.org/abs/2009.03300"]) == ["https://arxiv.org/abs/2009.03300"]


@pytest.mark.parametrize(("changes", "reason"), [
    ({"granularity": "aggregate"}, "not verified as individual"),
    ({"modality": ["text", "image"]}, "requires other media"),
    ({"footer": {"item_count": 2, "columns": ["item_id"], "uncompressed_bytes": 10}}, "lacks required"),
    ({"footer": {"item_count": 50_001, "columns": ["item_id", "benchmark_id", "content"], "uncompressed_bytes": 10}}, "50,000"),
    ({"footer": {"item_count": 2, "columns": ["item_id", "benchmark_id", "content"], "uncompressed_bytes": bank.MAX_UNCOMPRESSED_BYTES + 1}}, "96 MiB"),
])
def test_unsupported_candidates_visible_with_reason(tmp_path, monkeypatch, changes, reason):
    api, _ = discovery_fixture(tmp_path, monkeypatch, **changes)
    candidate = bank._build_entry("mmlu", REVISION, api, "private-test-token")
    assert not candidate["available"]
    assert reason in candidate["unavailable_reason"]


def prepared_fixture(tmp_path, monkeypatch, *, benchmark_id="mmlu"):
    path = tmp_path / "source.parquet"
    pq.write_table(pa.Table.from_pylist([
        {"item_id": "one", "benchmark_id": benchmark_id, "content": "Question one", "reference_answer": "One"},
        {"item_id": "two", "benchmark_id": benchmark_id, "content": "Question two", "reference_answer": "Two"},
    ]), path)
    with pq.ParquetFile(path) as parquet:
        columns = parquet.schema_arrow.names
    candidate = entry(table_path="mmlu/items.parquet", table_bytes=path.stat().st_size,
                      sha256=bank.data.file_sha256(path), benchmark_ids=["mmlu"], columns=columns,
                      testing_scope="Test split", version="v1")
    publish([candidate])
    calls = []

    def download(**kwargs):
        calls.append(kwargs)
        return str(path)

    monkeypatch.setattr(bank, "hf_hub_download", download)
    return candidate, calls


def test_prepare_preserves_full_population_and_pinned_identity(tmp_path, monkeypatch):
    candidate, calls = prepared_fixture(tmp_path, monkeypatch)
    output = tmp_path / "run"
    dataset = bank.prepare_candidate(output, candidate)
    assert dataset["item_count"] == 2
    assert dataset["source"]["revision"] == REVISION
    assert dataset["source"]["repo"] == PROCESSED_REPO
    assert dataset["source"]["identity_validation"] == "repository_metadata_mapping"
    assert "path" not in dataset["source"]
    assert len(list(bank.data.read_items(output / "items.jsonl"))) == 2
    assert not (output / "evidence.json").exists()
    assert not (output / "classifier_spec.json").exists()
    assert calls[0]["revision"] == REVISION
    assert calls[0]["repo_id"] == PROCESSED_REPO
    assert calls[0]["repo_type"] == "dataset"
    assert calls[0]["filename"] == candidate["table_path"]


def test_prepare_accepts_eligible_nonpublic_snapshot_with_pinned_repository_and_revision(tmp_path, monkeypatch):
    candidate, calls = prepared_fixture(tmp_path, monkeypatch)
    candidate["release"] = "private"
    publish([candidate])
    selected = bank.search_candidates(assessment())["candidates"][0]
    assert selected["available"] and selected["release"] == "private"
    dataset = bank.prepare_candidate(tmp_path / "run", selected)
    assert dataset["item_count"] == 2
    assert dataset["source"]["repo"] == PROCESSED_REPO and dataset["source"]["revision"] == REVISION
    assert dataset["source"]["identity_validation"] == "repository_metadata_mapping"
    assert calls[0]["repo_id"] == PROCESSED_REPO and calls[0]["revision"] == REVISION
    assert calls[0]["filename"] == candidate["table_path"]


def test_prepare_rejects_wrong_identity_before_preparing(tmp_path, monkeypatch):
    candidate, _ = prepared_fixture(tmp_path, monkeypatch, benchmark_id="a-different-benchmark")
    with pytest.raises(bank.DataBankError, match="validation"):
        bank.prepare_candidate(tmp_path / "run", candidate)
    assert not (tmp_path / "run" / "items.jsonl").exists()


def test_prepare_rejects_changed_confirmation_and_can_stop(tmp_path, monkeypatch):
    candidate, calls = prepared_fixture(tmp_path, monkeypatch)
    with pytest.raises(bank.DataBankError, match="metadata changed"):
        bank.prepare_candidate(tmp_path / "run", {**candidate, "item_count": 1})
    with pytest.raises(InterruptedError):
        bank.prepare_candidate(tmp_path / "run", candidate, stopped=lambda: True)
    assert not calls


@pytest.mark.parametrize("missing", [None, "", "   "])
def test_prepare_rejects_any_item_without_mapped_identity(tmp_path, monkeypatch, missing):
    candidate, _ = prepared_fixture(tmp_path, monkeypatch)
    source = tmp_path / "source.parquet"
    rows = pq.read_table(source).to_pylist()
    rows[1]["benchmark_id"] = missing
    pq.write_table(pa.Table.from_pylist(rows), source)
    candidate.update(sha256=bank.data.file_sha256(source), table_bytes=source.stat().st_size)
    publish([candidate])
    with pytest.raises(bank.DataBankError, match="validation"):
        bank.prepare_candidate(tmp_path / "run", candidate)
    assert not (tmp_path / "run" / "items.jsonl").exists()


def test_prepare_rejects_changed_hash(tmp_path, monkeypatch):
    candidate, _ = prepared_fixture(tmp_path, monkeypatch)
    changed = {**candidate, "sha256": "0" * 64}
    publish([changed])
    with pytest.raises(bank.DataBankError, match="validation"):
        bank.prepare_candidate(tmp_path / "run", changed)
    assert not (tmp_path / "run" / "items.jsonl").exists()
