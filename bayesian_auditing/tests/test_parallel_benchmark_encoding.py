"""Exercise real spawn/IPC/lifecycle behavior without loading CUDA or models."""

import multiprocessing
import os
from pathlib import Path
import sys
from threading import Event, Timer
import time
from types import SimpleNamespace

import numpy as np
import pytest

from bayesian_auditing import parallel_benchmark_encoding as module
from bayesian_auditing.benchmark_index import _policy


class FakeEncoder:
    def __init__(self, *, device, batch_size):
        if device == "init-fail":
            raise ValueError("fixture initialization failure")
        self.batch_size = batch_size

    def encode(self, texts):
        if texts and texts[0] == "raise":
            raise ValueError("fixture encoding failure")
        if texts and texts[0] == "die":
            os._exit(23)
        if texts and texts[0] == "wait":
            time.sleep(30)
        vectors = np.zeros((len(texts), 384), dtype=np.float32)
        for index, text in enumerate(texts):
            if text.startswith("delay:"):
                _, seconds, value = text.split(":")
                time.sleep(float(seconds))
            else:
                value = text
            vectors[index, :4] = [float(value), os.getpid(), len(texts), self.batch_size]
        if texts and texts[0] == "99":
            return vectors.astype(np.float64)
        return vectors


def fake_worker(connection, device, batch_size, cpu_threads):
    # Monkeypatch inside the spawned child: parent monkeypatches are not
    # inherited with spawn. The production worker's actual protocol still runs.
    sys.modules["torch"] = SimpleNamespace(set_num_threads=lambda threads: None)
    module.FullRowBGEEncoder = FakeEncoder
    module._encoder_worker(connection, device, batch_size, cpu_threads)


def graceful_marker_worker(connection, device, batch_size, cpu_threads):
    try:
        fake_worker(connection, device, batch_size, cpu_threads)
    finally:
        # SIGTERM skips this Python cleanup, so a marker proves normal exit.
        Path(device.removeprefix("marker:")).write_text("worker cleanup completed")


@pytest.fixture
def encoder(monkeypatch):
    monkeypatch.setattr(module, "_encoder_worker", fake_worker)
    pool = module.ParallelFullRowBGEEncoder(["cpu:0", "cpu:1", "cpu:2"], batch_size=7)
    yield pool
    pool.close()


def live_pids():
    return {process.pid for process in multiprocessing.active_children()}


def test_lazy_start_then_ordered_unchanged_batches_and_persistent_workers(encoder):
    assert encoder._workers == [] and encoder.max_parallel_batches == 3
    assert encoder.encode_batches([]) == []
    assert encoder._workers == []
    batches = [["delay:0.2:1", "2"], ["3"], ["4", "5", "6"]]
    outputs = encoder.encode_batches(batches)
    assert [output[:, 0].tolist() for output in outputs] == [[1, 2], [3], [4, 5, 6]]
    assert [output[:, 2].tolist() for output in outputs] == [[2, 2], [1], [3, 3, 3]]
    assert all(output.dtype == np.float32 for output in outputs)
    assert all((output[:, 3] == 7).all() for output in outputs)
    pids = [int(output[0, 1]) for output in outputs]
    assert len(set(pids)) == 3 and os.getpid() not in pids
    again = encoder.encode_batches([["7"], ["8"], ["9"]])
    assert [int(output[0, 1]) for output in again] == pids
    assert encoder.encode(["10"])[0, 1] == pids[0]


def test_window_bound_is_enforced_before_starting_workers(encoder):
    with pytest.raises(ValueError, match="more batches than workers"):
        encoder.encode_batches([["1"]] * 4)
    assert encoder._workers == []
    assert encoder.encode(["2"])[0, 0] == 2


def test_parallel_policy_matches_existing_single_gpu_checkpoint(encoder):
    assert _policy(encoder) == _policy(None)
    assert encoder._workers == []


def test_cuda_worker_selects_its_device_before_constructing_encoder(monkeypatch):
    selected = []
    sent = []
    monkeypatch.setitem(sys.modules, "torch", SimpleNamespace(
        set_num_threads=lambda count: None,
        cuda=SimpleNamespace(set_device=lambda device: selected.append(device)),
    ))

    class DeviceEncoder(FakeEncoder):
        def __init__(self, *, device, batch_size):
            assert selected == [device]
            super().__init__(device=device, batch_size=batch_size)

    class Connection:
        def send(self, value):
            sent.append(value)

        def recv(self):
            raise EOFError

        def close(self):
            pass

    monkeypatch.setattr(module, "FullRowBGEEncoder", DeviceEncoder)
    module._encoder_worker(Connection(), "cuda:2", 64, 4)
    assert selected == ["cuda:2"] and sent == [("ready", None)]


@pytest.mark.parametrize("bad", [[], [""], ["cpu:0", "cpu:0"], [None]])
def test_invalid_device_lists_fail_before_start(bad):
    with pytest.raises(ValueError, match="device names"):
        module.ParallelFullRowBGEEncoder(bad)


def test_empty_single_batch_has_original_shape_and_dtype(encoder):
    output = encoder.encode([])
    assert output.shape == (0, 384) and output.dtype == np.float32


@pytest.mark.parametrize("command,error", [("raise", "fixture encoding failure"), ("die", "disconnected|exited"),
                                          ("99", "invalid float32 vectors")])
def test_worker_errors_hard_exits_and_bad_results_close_every_worker(encoder, command, error):
    encoder.encode(["0"])
    pids = {worker.process.pid for worker in encoder._workers}
    with pytest.raises(RuntimeError, match=error):
        encoder.encode_batches([["wait"], [command], ["1"]])
    assert encoder._workers == []
    assert not pids & live_pids()
    with pytest.raises(RuntimeError, match="closed"):
        encoder.encode(["1"])


def test_startup_failure_closes_other_started_workers(monkeypatch):
    monkeypatch.setattr(module, "_encoder_worker", fake_worker)
    before = live_pids()
    encoder = module.ParallelFullRowBGEEncoder(["cpu:0", "init-fail", "cpu:2"])
    with pytest.raises(RuntimeError, match="fixture initialization failure"):
        encoder.encode(["1"])
    assert encoder._workers == [] and live_pids() == before


def test_cancellation_terminates_active_workers_without_waiting_for_encoding(encoder):
    encoder.encode(["0"])
    pids = {worker.process.pid for worker in encoder._workers}
    stopped = Event()
    timer = Timer(0.2, stopped.set)
    timer.start()
    started = time.monotonic()
    try:
        with pytest.raises(InterruptedError, match="cancelled"):
            encoder.encode_batches([["wait"], ["wait"]], cancelled=stopped.is_set)
    finally:
        timer.cancel()
    assert time.monotonic() - started < 5
    assert not pids & live_pids()
    assert encoder._workers == []


def test_preexisting_cancellation_starts_no_workers(encoder):
    with pytest.raises(InterruptedError, match="cancelled"):
        encoder.encode(["1"], cancelled=lambda: True)
    assert encoder._workers == []


def test_close_and_context_exit_are_idempotent_and_leave_no_workers(encoder):
    with encoder:
        encoder.encode(["1"])
        pids = {worker.process.pid for worker in encoder._workers}
    encoder.close()
    assert not pids & live_pids()
    assert encoder._workers == []
    with pytest.raises(RuntimeError, match="closed"):
        encoder.encode_batches([])


def test_idle_close_lets_each_worker_run_its_cleanup(monkeypatch, tmp_path):
    monkeypatch.setattr(module, "_encoder_worker", graceful_marker_worker)
    markers = [tmp_path / "worker-0.txt", tmp_path / "worker-1.txt"]
    with module.ParallelFullRowBGEEncoder([f"marker:{path}" for path in markers]) as encoder:
        encoder.encode_batches([["1"], ["2"]])
        assert all(not path.exists() for path in markers)
    assert [path.read_text() for path in markers] == ["worker cleanup completed"] * 2
