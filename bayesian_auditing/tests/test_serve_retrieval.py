"""Launcher lifecycle and private credentials, without opening a tunnel."""

import json
import os
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
    state = SimpleNamespace(processes=[], health=[], handlers={}, state_dir=state_dir)
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
    monkeypatch.setattr(launcher.signal, "signal", lambda name, handler: state.handlers.update({name: handler}))
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
        assert service.command[service.command.index("--log-config") + 1] == str(runtime.state_dir / "log-config.json")
        assert token not in " ".join(service.command)
        environment = service.options["env"]
        assert environment["RETRIEVAL_SERVICE_TOKEN"] == token
        assert environment["CUDA_VISIBLE_DEVICES"] == ""
        assert environment["RETRIEVAL_CPU_THREADS"] == "4"
    assert all(call[2] == token for call in runtime.health)
    config = json.loads((runtime.state_dir / "log-config.json").read_text())
    assert config["root"]["level"] == "WARNING"
    assert set(config["loggers"]) == {"uvicorn", "bayesian_auditing"}
    assert all(entry["level"] == "INFO" for entry in config["loggers"].values())
    assert "%(asctime)s" in config["formatters"]["timestamped"]["format"]


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


@pytest.fixture
def existing_tunnel(runtime, monkeypatch):
    runtime.state_dir.mkdir()
    token = launcher._token(runtime.state_dir)
    url = "https://existing-test.trycloudflare.com"
    runtime.config = f"ITEM_REVIEW_RETRIEVAL_URL={url}\nITEM_REVIEW_RETRIEVAL_TOKEN={token}\n"
    (runtime.state_dir / "render.env").write_text(runtime.config)
    (runtime.state_dir / "status.json").write_text(json.dumps({
        "tunnel_pid": 555, "port": 8001, "url": url,
    }))
    (runtime.state_dir / "service.log").write_text("previous service log\n")
    (runtime.state_dir / "tunnel.log").write_text("previous tunnel log\n")
    identity = {
        "starttime": 12345,
        "uid": os.getuid(),
        "executable": Path("/fake/cloudflared"),
        "command": [os.fsencode(part) for part in launcher._tunnel_command("/fake/cloudflared", 8001)],
    }
    monkeypatch.setattr(launcher, "_process_identity", lambda pid: identity.copy() if pid == 555 else None)
    runtime.arguments += ["--reuse-tunnel", "555:12345"]
    runtime.identity = identity
    return runtime


def test_reuse_preserves_tunnel_settings_and_logs(existing_tunnel):
    state = existing_tunnel
    assert launcher.main(state.arguments) == 0
    service, = state.processes
    assert service.stopped
    assert (state.state_dir / "render.env").read_text() == state.config
    assert (state.state_dir / "tunnel.log").read_text() == "previous tunnel log\n"
    assert (state.state_dir / "service.log").read_text() == "previous service log\n"
    status = json.loads((state.state_dir / "status.json").read_text())
    assert status["tunnel_pid"] == 555
    assert status["tunnel_starttime"] == 12345
    assert status["tunnel_reused"] is True


@pytest.mark.parametrize("field,value", [
    ("starttime", 12346), ("uid", -1), ("executable", Path("/wrong/cloudflared")),
    ("command", [b"cloudflared", b"different", b"arguments"]),
])
def test_reuse_rejects_wrong_process_without_starting_service(existing_tunnel, field, value):
    state = existing_tunnel
    state.identity[field] = value
    previous_status = (state.state_dir / "status.json").read_text()
    with pytest.raises(SystemExit) as error:
        launcher.main(state.arguments)
    assert error.value.code == 2
    assert not state.processes
    assert (state.state_dir / "status.json").read_text() == previous_status
    assert (state.state_dir / "render.env").read_text() == state.config
    assert (state.state_dir / "tunnel.log").read_text() == "previous tunnel log\n"


def test_reuse_rejects_inconsistent_saved_settings(existing_tunnel):
    state = existing_tunnel
    path = state.state_dir / "render.env"
    path.write_text("different private settings")
    with pytest.raises(SystemExit):
        launcher.main(state.arguments)
    assert not state.processes
    assert path.read_text() == "different private settings"


def test_reuse_startup_failure_preserves_tunnel(existing_tunnel, monkeypatch):
    state = existing_tunnel

    def fail(*_args):
        raise RuntimeError("Index unavailable")

    monkeypatch.setattr(launcher, "_wait_for_health", fail)
    assert launcher.main(state.arguments) == 1
    assert len(state.processes) == 1
    assert state.processes[0].stopped
    assert (state.state_dir / "render.env").read_text() == state.config
    assert json.loads((state.state_dir / "status.json").read_text())["tunnel_pid"] == 555


def test_adopted_tunnel_detects_pid_reuse(existing_tunnel, monkeypatch):
    tunnel = launcher._ExistingTunnel(555, existing_tunnel.identity.copy())
    assert tunnel.poll() is None
    existing_tunnel.identity["starttime"] += 1
    assert tunnel.poll() == 0


def test_sighup_restarts_only_service(runtime, monkeypatch):
    calls = 0

    def request_then_stop(_seconds):
        nonlocal calls
        calls += 1
        if calls == 1:
            runtime.handlers[launcher.signal.SIGHUP](launcher.signal.SIGHUP, None)
        else:
            old_service, tunnel, new_service = runtime.processes
            assert old_service.stopped
            assert not tunnel.stopped
            assert not new_service.stopped
            assert json.loads((runtime.state_dir / "status.json").read_text())["state"] == "ready"
            raise KeyboardInterrupt

    monkeypatch.setattr(launcher.time, "sleep", request_then_stop)
    assert launcher.main(runtime.arguments) == 0
    assert len(runtime.processes) == 3
    assert len(runtime.health) == 2
    assert all(process.stopped for process in runtime.processes)


def test_failed_sighup_restart_keeps_tunnel_and_accepts_retry(runtime, monkeypatch):
    sleeps = 0
    starts = 0

    def health(*_args):
        nonlocal starts
        starts += 1
        if starts == 2:
            raise RuntimeError("Temporary startup failure")

    def retry_then_stop(_seconds):
        nonlocal sleeps
        sleeps += 1
        if sleeps == 2:
            assert runtime.processes[2].stopped
            assert not runtime.processes[1].stopped
            assert json.loads((runtime.state_dir / "status.json").read_text())["state"] == "failed"
        if sleeps < 3:
            runtime.handlers[launcher.signal.SIGHUP](launcher.signal.SIGHUP, None)
        else:
            assert not runtime.processes[1].stopped
            status = json.loads((runtime.state_dir / "status.json").read_text())
            assert status["state"] == "ready"
            assert "error" not in status
            raise KeyboardInterrupt

    monkeypatch.setattr(launcher, "_wait_for_health", health)
    monkeypatch.setattr(launcher.time, "sleep", retry_then_stop)
    assert launcher.main(runtime.arguments) == 0
    assert len(runtime.processes) == 4
    assert starts == 3
