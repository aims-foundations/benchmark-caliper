"""Preparation CLI options and worker lifecycle, without models or GPUs."""

import json
import signal
import sys
from types import SimpleNamespace

import pytest

from bayesian_auditing import prepare_benchmark_index as cli
from bayesian_auditing.benchmark_data import row_fingerprint


@pytest.fixture
def runtime(tmp_path, monkeypatch):
    inventory = {"branches": {"main": "pinned"}, "tables": [{"row_count": 7}]}
    inventory_path = tmp_path / "inventory.json"
    inventory_path.write_text(json.dumps(inventory))
    state = SimpleNamespace(single=[], parallel=[], indexes=[], calls=[], threads=[], signals={})
    monkeypatch.setitem(sys.modules, "torch", SimpleNamespace(set_num_threads=state.threads.append))
    monkeypatch.setattr(cli, "get_token", lambda: None)
    monkeypatch.setattr(cli.os, "umask", lambda value: None)
    monkeypatch.setattr(cli.signal, "signal", lambda name, handler: state.signals.__setitem__(name, handler))

    class SingleEncoder:
        def __init__(self, **options):
            self.options = options
            state.single.append(self)

    class ParallelEncoder:
        def __init__(self, devices, **options):
            self.devices, self.options, self.closed = devices, options, 0
            state.parallel.append(self)

        def close(self):
            self.closed += 1

    class Index:
        def __init__(self, cache_dir, cache_hit):
            self.path = cache_dir / "test.sqlite3"
            self.path.write_bytes(b"fake index")
            self.stats = {"cache_hit": cache_hit}
            self.closed = 0
            state.indexes.append(self)

        def search(self, query, *, cancelled):
            assert query == cli.SMOKE_QUERY
            assert not cancelled()
            row = {"item_id": "original", "content": "A complete original row."}
            return [{"item_id": row_fingerprint(row), "evidence": {"item": row},
                     "dense_rank": 1, "bm25_rank": 1, "sources": [{"benchmark": "test"}]}]

        def close(self):
            self.closed += 1

    def prepare(rows, cache_dir, inventory, encoder, **options):
        state.calls.append((rows, inventory, encoder, options))
        if "progress" in options:
            options["progress"]({"stage": "indexing", "completed": 7, "total": 7})
        return Index(cache_dir, cache_hit=len(state.calls) > 1)

    monkeypatch.setattr(cli, "FullRowBGEEncoder", SingleEncoder)
    monkeypatch.setattr(cli, "ParallelFullRowBGEEncoder", ParallelEncoder)
    monkeypatch.setattr(cli, "prepare_benchmark_index", prepare)
    state.prepare, state.Index = prepare, Index
    state.cache = tmp_path / "cache"
    state.arguments = ["--inventory", str(inventory_path), "--cache-dir", str(state.cache)]
    state.status = lambda: json.loads((state.cache / "preparation-status.json").read_text())
    return state


def test_parallel_options_status_verification_and_cleanup(runtime):
    cli.main(runtime.arguments + ["--devices", "cuda:0", "cuda:2", "--batch-size", "23", "--cpu-threads", "3"])
    assert not runtime.single
    encoder, = runtime.parallel
    assert encoder.devices == ["cuda:0", "cuda:2"]
    assert encoder.options == {"batch_size": 23, "cpu_threads": 3}
    assert encoder.closed == 1
    assert runtime.threads == [3]
    assert [index.closed for index in runtime.indexes] == [1, 1]
    assert len(runtime.calls) == 2
    assert all(call[2] is encoder and call[3]["resume"] for call in runtime.calls)
    with pytest.raises(AssertionError, match="unexpectedly consumed"):
        runtime.calls[1][0](0)
    status = runtime.status()
    assert status["status"] == "completed"
    assert status["devices"] == ["cuda:0", "cuda:2"]
    assert status["encoding_workers"] == 2
    assert status["source_rows"] == 7
    assert status["cache_reuse_verified"] is True
    assert status["smoke_search"]["candidates"] == 1


@pytest.mark.parametrize("arguments, device", [([], None), (["--device", "cpu"], "cpu")])
def test_single_device_path_is_preserved(runtime, arguments, device):
    cli.main(runtime.arguments + arguments)
    encoder, = runtime.single
    assert encoder.options == {"device": device, "batch_size": 64}
    assert not runtime.parallel
    assert runtime.status()["devices"] == [device or "auto"]
    assert runtime.status()["encoding_workers"] == 1


@pytest.mark.parametrize("devices", [
    ["--devices"], ["--devices", ""], ["--devices", "cuda:0", "cuda:0"],
    ["--devices", "cpu"], ["--devices", "cuda"], ["--devices", "cuda:-1"],
    ["--devices", "cuda:00"], ["--device", "cuda:0", "--devices", "cuda:1"],
])
def test_invalid_device_choices_fail_before_starting_workers(runtime, devices):
    with pytest.raises(SystemExit) as error:
        cli.main(runtime.arguments + devices)
    assert error.value.code == 2
    assert not runtime.parallel and not runtime.single and not runtime.threads
    assert not runtime.cache.exists()


@pytest.mark.parametrize("phase", ["build", "verify", "reuse", "index_close"])
def test_parallel_workers_close_when_preparation_fails(runtime, monkeypatch, phase):
    def fail(*args, **kwargs):
        raise RuntimeError("fixture failure")

    def prepare(*args, **kwargs):
        if phase == "build" or (phase == "reuse" and runtime.calls):
            fail()
        index = runtime.prepare(*args, **kwargs)
        if phase == "verify":
            index.search = fail
        elif phase == "index_close":
            index.close = fail
        return index

    monkeypatch.setattr(cli, "prepare_benchmark_index", prepare)
    with pytest.raises(RuntimeError, match="fixture failure"):
        cli.main(runtime.arguments + ["--devices", "cuda:0", "cuda:1"])
    assert runtime.parallel[0].closed == 1
    assert runtime.status()["status"] == "failed"
    if phase == "verify":
        assert runtime.indexes[0].closed == 1


def test_signal_cancellation_closes_parallel_workers_and_records_interruption(runtime, monkeypatch):
    def prepare(*args, **options):
        runtime.signals[signal.SIGTERM](signal.SIGTERM, None)
        assert options["cancelled"]()
        raise InterruptedError("cancelled fixture")

    monkeypatch.setattr(cli, "prepare_benchmark_index", prepare)
    with pytest.raises(InterruptedError, match="cancelled fixture"):
        cli.main(runtime.arguments + ["--devices", "cuda:0", "cuda:1"])
    assert runtime.parallel[0].closed == 1
    assert runtime.status()["status"] == "interrupted"


def test_row_iteration_and_candidate_loading_keep_the_pinned_inventory(runtime, monkeypatch):
    row_calls, load_calls = [], []
    monkeypatch.setattr(cli, "iter_benchmark_items", lambda data, **options: row_calls.append((data, options)))
    monkeypatch.setattr(cli, "fetch_benchmark_rows", lambda data, requests, **options: load_calls.append((data, requests, options)))
    cli.main(runtime.arguments + ["--devices", "cuda:0", "cuda:1"])
    rows, inventory, _, options = runtime.calls[0]
    rows(5)
    options["row_loader"]([{"item_id": "requested"}])
    assert row_calls == [(inventory, {"token": None, "streaming": True, "skip_rows": 5})]
    assert load_calls == [(inventory, [{"item_id": "requested"}], {"token": None, "cancelled": None})]
