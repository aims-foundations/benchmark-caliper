"""Launcher lifecycle and private credentials, without opening a tunnel."""

import json
from pathlib import Path
import stat
from types import SimpleNamespace

import pytest

from bayesian_auditing import serve_retrieval as launcher


@pytest.fixture
def runtime(tmp_path, monkeypatch):
    index = tmp_path / "index.sqlite3"
    index.touch()
    for name in ("ONET_index.csv", "ONET_embeddings.npz"):
        (tmp_path / name).touch()
    state_dir = tmp_path / "state"
    state = SimpleNamespace(processes=[], health=[], state_dir=state_dir)
    state.arguments = ["--index", str(index), "--onet-dir", str(tmp_path),
                       "--state-dir", str(state_dir), "--cloudflared", "/fake/cloudflared"]

    class Process:
        def __init__(self, command, **options):
            self.command, self.options = command, options
            self.pid, self.stopped = 100 + len(state.processes), False
            state.processes.append(self)

        def poll(self):
            return 0 if self.stopped else None

        def terminate(self):
            self.stopped = True

        def wait(self, timeout):
            return 0

    def stop_loop(_seconds):
        raise KeyboardInterrupt

    monkeypatch.setattr(launcher.subprocess, "Popen", Process)
    monkeypatch.setattr(launcher, "_wait_for_health", lambda *args: state.health.append(args))
    monkeypatch.setattr(launcher, "_wait_for_tunnel", lambda *args: "https://example-test.trycloudflare.com")
    monkeypatch.setattr(launcher.time, "sleep", stop_loop)
    # Avoid changing the test process's global umask or signal handlers.
    monkeypatch.setattr(launcher.os, "umask", lambda value: None)
    monkeypatch.setattr(launcher.signal, "signal", lambda *args: None)
    return state


def test_credentials_are_reused_private_and_not_logged(runtime, capsys):
    assert launcher.main(runtime.arguments) == 0
    token = (runtime.state_dir / "service-token").read_text().strip()
    assert len(token) >= 32
    assert launcher.main(runtime.arguments) == 0
    assert (runtime.state_dir / "service-token").read_text().strip() == token
    assert stat.S_IMODE(runtime.state_dir.stat().st_mode) == 0o700
    for path in runtime.state_dir.iterdir():
        assert stat.S_IMODE(path.stat().st_mode) == 0o600
    output = capsys.readouterr()
    assert token not in output.out + output.err
    assert token not in (runtime.state_dir / "status.json").read_text()
    assert (runtime.state_dir / "render.env").read_text().splitlines() == [
        "ITEM_REVIEW_RETRIEVAL_URL=https://example-test.trycloudflare.com",
        f"ITEM_REVIEW_RETRIEVAL_TOKEN={token}",
    ]
    assert all(process.stopped for process in runtime.processes)
    assert json.loads((runtime.state_dir / "status.json").read_text())["state"] == "stopped"
    for service in runtime.processes[::2]:
        assert "127.0.0.1" in service.command
        assert "--no-access-log" in service.command
        assert token not in " ".join(service.command)
        environment = service.options["env"]
        assert environment["RETRIEVAL_SERVICE_TOKEN"] == token
        assert environment["CUDA_VISIBLE_DEVICES"] == ""
        assert environment["RETRIEVAL_CPU_THREADS"] == "4"
    assert all(call[2] == token for call in runtime.health)


def test_startup_failure_stops_server_without_creating_tunnel(runtime, monkeypatch):
    def fail(*_args):
        raise RuntimeError("Retrieval server could not load the prepared index")

    monkeypatch.setattr(launcher, "_wait_for_health", fail)
    assert launcher.main(runtime.arguments) == 1
    service, = runtime.processes
    assert service.stopped
    assert not (runtime.state_dir / "render.env").exists()
    assert json.loads((runtime.state_dir / "status.json").read_text())["state"] == "failed"


def test_duplicate_launcher_does_not_overwrite_files(runtime):
    runtime.state_dir.mkdir()
    config = runtime.state_dir / "render.env"
    config.write_text("existing configuration")
    with (runtime.state_dir / "launcher.lock").open("a") as lock:
        launcher.fcntl.flock(lock.fileno(), launcher.fcntl.LOCK_EX | launcher.fcntl.LOCK_NB)
        with pytest.raises(SystemExit) as error:
            launcher.main(runtime.arguments)
    assert error.value.code == 2
    assert not runtime.processes
    assert config.read_text() == "existing configuration"


def test_stop_kills_a_child_that_does_not_terminate():
    calls = []

    class StuckProcess:
        def poll(self):
            return None

        def terminate(self):
            calls.append("terminate")

        def wait(self, timeout):
            calls.append(("wait", timeout))
            if timeout == 20:
                raise launcher.subprocess.TimeoutExpired("server", timeout)

        def kill(self):
            calls.append("kill")

    launcher._stop(StuckProcess())
    assert calls == ["terminate", ("wait", 20), "kill", ("wait", 5)]
