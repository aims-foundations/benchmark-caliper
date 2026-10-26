"""Supervise the private retrieval server and a temporary Cloudflare tunnel.

Run this command in a detached session for testing. Only the two values in the
private ``render.env`` file belong in Render; neither is printed to the log.
Send SIGHUP to the supervisor to reload the retrieval server without changing
the tunnel URL. ``--reuse-tunnel PID:STARTTIME`` adopts an existing tunnel for
monitoring without stopping it when this launcher exits.
"""

from __future__ import annotations

import argparse
from contextlib import ExitStack
import fcntl
import json
import os
from pathlib import Path
import re
import secrets
import signal
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import ProxyHandler, Request, build_opener


def _write_private(path: Path, text: str):
    temporary = path.with_name(path.name + ".tmp")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        os.fchmod(handle.fileno(), 0o600)
        handle.write(text)
    temporary.replace(path)


def _token(state_dir: Path) -> str:
    path = state_dir / "service-token"
    if path.exists():
        token = path.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]{32,}", token):
            raise RuntimeError("The saved retrieval token is invalid; inspect the private state directory")
        path.chmod(0o600)
        return token
    token = secrets.token_urlsafe(48)
    _write_private(path, token + "\n")
    return token


def _wait_for_health(process, port: int, token: str, timeout=120):
    opener = build_opener(ProxyHandler({}))
    request = Request(f"http://127.0.0.1:{port}/healthz",
                      headers={"Authorization": f"Bearer {token}"})
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Retrieval server exited during startup; inspect service.log")
        try:
            with opener.open(request, timeout=min(5, max(0.1, deadline - time.monotonic()))) as response:
                if json.load(response).get("ready") is True:
                    return
        except (URLError, TimeoutError, ValueError):
            pass
        time.sleep(1)
    raise RuntimeError("Retrieval server did not become ready within 120 seconds; inspect service.log")


def _wait_for_tunnel(process, log_path: Path, timeout=120) -> str:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Cloudflare tunnel exited during startup; inspect tunnel.log")
        match = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com\b",
                          log_path.read_text(encoding="utf-8", errors="replace"))
        if match:
            return match.group(0)
        time.sleep(1)
    raise RuntimeError("Cloudflare did not provide a tunnel URL within 120 seconds; inspect tunnel.log")


def _stop(process):
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def _process_identity(pid: int):
    """Read Linux process identity without exposing command-line credentials."""
    process = Path(f"/proc/{pid}")
    try:
        fields = (process / "stat").read_text().rsplit(")", 1)[1].split()
        if fields[0] == "Z":
            return None
        return {
            "starttime": int(fields[19]),
            "uid": process.stat().st_uid,
            "executable": (process / "exe").resolve(strict=True),
            "command": (process / "cmdline").read_bytes().rstrip(b"\0").split(b"\0"),
        }
    except (OSError, IndexError, ValueError):
        return None


def _tunnel_identity(value: str):
    try:
        pid, starttime = map(int, value.split(":"))
        if pid <= 1 or starttime <= 0:
            raise ValueError
        return pid, starttime
    except ValueError:
        raise argparse.ArgumentTypeError("Use the existing tunnel's PID:STARTTIME from /proc/PID/stat") from None


def _tunnel_command(binary: str, port: int):
    return [binary, "tunnel", "--no-autoupdate", "--protocol", "http2",
            "--url", f"http://127.0.0.1:{port}"]


class _ExistingTunnel:
    """A borrowed process: monitor its pinned identity, never signal its PID."""

    def __init__(self, pid: int, identity: dict):
        self.pid = pid
        self.identity = identity

    def poll(self):
        return None if _process_identity(self.pid) == self.identity else 0


def _reuse_tunnel(args, state_dir: Path, token: str):
    pid, starttime = args.reuse_tunnel
    identity = _process_identity(pid)
    expected_command = [os.fsencode(part) for part in _tunnel_command(args.cloudflared, args.port)]
    if (identity is None or identity["starttime"] != starttime or identity["uid"] != os.getuid()
            or identity["executable"] != Path(args.cloudflared).resolve()
            or identity["command"] != expected_command):
        raise RuntimeError("Existing tunnel identity does not match; no processes were changed")
    try:
        status = json.loads((state_dir / "status.json").read_text())
        url = status["url"]
        config = (state_dir / "render.env").read_text()
    except (OSError, ValueError, KeyError):
        raise RuntimeError("Cannot verify the existing tunnel's private settings") from None
    if (status.get("tunnel_pid") != pid or status.get("port") != args.port
            or not isinstance(url, str)
            or not re.fullmatch(r"https://[a-z0-9-]+\.trycloudflare\.com", url)
            or config != f"ITEM_REVIEW_RETRIEVAL_URL={url}\nITEM_REVIEW_RETRIEVAL_TOKEN={token}\n"):
        raise RuntimeError("Existing tunnel settings do not match; no processes were changed")
    tunnel = _ExistingTunnel(pid, identity)
    if tunnel.poll() is not None:
        raise RuntimeError("Existing tunnel exited during validation")
    return tunnel, url


def _logging_config(state_dir: Path):
    path = state_dir / "log-config.json"
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"timestamped": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"}},
        "handlers": {"stderr": {"class": "logging.StreamHandler", "formatter": "timestamped",
                                 "stream": "ext://sys.stderr"}},
        "loggers": {
            "uvicorn": {"handlers": ["stderr"], "level": "INFO", "propagate": False},
            "bayesian_auditing": {"handlers": ["stderr"], "level": "INFO", "propagate": False},
        },
        "root": {"handlers": ["stderr"], "level": "WARNING"},
    }
    _write_private(path, json.dumps(config, indent=2) + "\n")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--onet-dir", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, default=Path("results/retrieval-service"))
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--cloudflared", required=True, help="Path to the installed cloudflared binary")
    parser.add_argument("--reuse-tunnel", type=_tunnel_identity, metavar="PID:STARTTIME",
                        help="Monitor this existing tunnel without replacing or stopping it")
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    for path in (args.index, args.onet_dir / "ONET_index.csv", args.onet_dir / "ONET_embeddings.npz"):
        if not path.is_file():
            parser.error(f"Required prepared file is missing: {path}")
    state_dir = args.state_dir.resolve()
    state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    state_dir.chmod(0o700)
    os.umask(0o077)

    with ExitStack() as stack:
        lock = stack.enter_context((state_dir / "launcher.lock").open("a"))
        os.fchmod(lock.fileno(), 0o600)
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error("A retrieval launcher already holds this state directory")
        token = _token(state_dir)
        tunnel, url = None, None
        if args.reuse_tunnel:
            try:
                tunnel, url = _reuse_tunnel(args, state_dir, token)
            except RuntimeError as error:
                parser.error(str(error))
        service_log = stack.enter_context((state_dir / "service.log").open("a"))
        # A new tunnel needs a fresh log so an old URL cannot be mistaken for its URL.
        tunnel_log = stack.enter_context((state_dir / "tunnel.log").open("a" if tunnel else "w"))
        for handle in (service_log, tunnel_log):
            os.fchmod(handle.fileno(), 0o600)
        if not tunnel:
            (state_dir / "render.env").unlink(missing_ok=True)
        log_config = _logging_config(state_dir)
        status = {"state": "starting", "supervisor_pid": os.getpid(), "port": args.port,
                  "index": str(args.index.resolve())}
        if tunnel:
            status.update(tunnel_pid=tunnel.pid, tunnel_starttime=args.reuse_tunnel[1],
                          tunnel_reused=True, url=url)

        def save_status():
            _write_private(state_dir / "status.json", json.dumps(status, indent=2) + "\n")

        def interrupt(_signum, _frame):
            raise KeyboardInterrupt

        restart_requested = False

        def request_restart(_signum, _frame):
            nonlocal restart_requested
            restart_requested = True

        previous_signals = {name: signal.signal(name, interrupt) for name in (signal.SIGTERM, signal.SIGINT)}
        previous_signals[signal.SIGHUP] = signal.signal(signal.SIGHUP, request_restart)
        children = []
        save_status()
        try:
            environment = {**os.environ, "RETRIEVAL_BENCHMARK_INDEX": str(args.index.resolve()),
                           "ITEM_REVIEW_ONET_DIR": str(args.onet_dir.resolve()),
                           "RETRIEVAL_SERVICE_TOKEN": token, "CUDA_VISIBLE_DEVICES": "",
                           **{key: "4" for key in ("RETRIEVAL_CPU_THREADS", "OMP_NUM_THREADS",
                                                   "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")}}
            def start_service():
                process = subprocess.Popen(
                    [sys.executable, "-m", "uvicorn", "bayesian_auditing.retrieval_service:app",
                     "--host", "127.0.0.1", "--port", str(args.port), "--no-access-log",
                     "--log-config", str(log_config)],
                    env=environment, stdin=subprocess.DEVNULL, stdout=service_log, stderr=subprocess.STDOUT,
                )
                children.append(process)
                status["service_pid"] = process.pid
                save_status()
                try:
                    _wait_for_health(process, args.port, token)
                except BaseException:
                    _stop(process)
                    raise
                return process

            service = start_service()
            if tunnel is None:
                tunnel = subprocess.Popen(
                    _tunnel_command(args.cloudflared, args.port),
                    stdin=subprocess.DEVNULL, stdout=tunnel_log, stderr=subprocess.STDOUT,
                )
                children.append(tunnel)
                status["tunnel_pid"] = tunnel.pid
                identity = _process_identity(tunnel.pid)
                if identity is not None:
                    status["tunnel_starttime"] = identity["starttime"]
                url = _wait_for_tunnel(tunnel, state_dir / "tunnel.log")
                _write_private(state_dir / "render.env",
                               f"ITEM_REVIEW_RETRIEVAL_URL={url}\nITEM_REVIEW_RETRIEVAL_TOKEN={token}\n")
            status.update(state="ready", url=url)
            save_status()
            print(f"Retrieval is ready. Private Render settings: {state_dir / 'render.env'}", flush=True)
            while tunnel.poll() is None and (service is None or service.poll() is None):
                if restart_requested:
                    restart_requested = False
                    status.update(state="restarting")
                    save_status()
                    if service is not None:
                        _stop(service)
                        service = None
                    try:
                        service = start_service()
                        status.update(state="ready")
                        status.pop("error", None)
                        print("Retrieval server restarted; tunnel unchanged.", flush=True)
                    except Exception as error:
                        # Retain the tunnel and accept another SIGHUP after a fix.
                        status.update(state="failed", error=str(error))
                        print(f"Retrieval restart failed: {error}", file=sys.stderr, flush=True)
                    save_status()
                time.sleep(1)
            raise RuntimeError("Retrieval server or tunnel exited; inspect service.log and tunnel.log")
        except KeyboardInterrupt:
            status["state"] = "stopped"
            return 0
        except Exception as error:
            status.update(state="failed", error=str(error))
            print(str(error), file=sys.stderr, flush=True)
            return 1
        finally:
            for name, previous in previous_signals.items():
                signal.signal(name, previous)
            for child in reversed(children):
                _stop(child)
            save_status()


if __name__ == "__main__":
    raise SystemExit(main())
