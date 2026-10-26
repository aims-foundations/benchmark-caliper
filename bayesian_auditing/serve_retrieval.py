"""Supervise the private retrieval server and a temporary Cloudflare tunnel.

Run this command in a detached session for testing. Only the two values in the
private ``render.env`` file belong in Render; neither is printed to the log.
Restarting the tunnel changes its URL, so update Render after each restart.
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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--onet-dir", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, default=Path("results/retrieval-service"))
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--cloudflared", required=True, help="Path to the installed cloudflared binary")
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
        service_log = stack.enter_context((state_dir / "service.log").open("w"))
        tunnel_log = stack.enter_context((state_dir / "tunnel.log").open("w"))
        for handle in (service_log, tunnel_log):
            os.fchmod(handle.fileno(), 0o600)
        (state_dir / "render.env").unlink(missing_ok=True)
        status = {"state": "starting", "supervisor_pid": os.getpid(), "port": args.port,
                  "index": str(args.index.resolve())}

        def save_status():
            _write_private(state_dir / "status.json", json.dumps(status, indent=2) + "\n")

        def interrupt(_signum, _frame):
            raise KeyboardInterrupt

        previous_signals = {name: signal.signal(name, interrupt) for name in (signal.SIGTERM, signal.SIGINT)}
        children = []
        save_status()
        try:
            environment = {**os.environ, "RETRIEVAL_BENCHMARK_INDEX": str(args.index.resolve()),
                           "ITEM_REVIEW_ONET_DIR": str(args.onet_dir.resolve()),
                           "RETRIEVAL_SERVICE_TOKEN": token, "CUDA_VISIBLE_DEVICES": "",
                           **{key: "4" for key in ("RETRIEVAL_CPU_THREADS", "OMP_NUM_THREADS",
                                                   "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")}}
            service = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "bayesian_auditing.retrieval_service:app",
                 "--host", "127.0.0.1", "--port", str(args.port), "--no-access-log"],
                env=environment, stdin=subprocess.DEVNULL, stdout=service_log, stderr=subprocess.STDOUT,
            )
            children.append(service)
            status["service_pid"] = service.pid
            _wait_for_health(service, args.port, token)
            tunnel = subprocess.Popen(
                [args.cloudflared, "tunnel", "--no-autoupdate", "--protocol", "http2",
                 "--url", f"http://127.0.0.1:{args.port}"],
                stdin=subprocess.DEVNULL, stdout=tunnel_log, stderr=subprocess.STDOUT,
            )
            children.append(tunnel)
            status["tunnel_pid"] = tunnel.pid
            url = _wait_for_tunnel(tunnel, state_dir / "tunnel.log")
            _write_private(state_dir / "render.env",
                           f"ITEM_REVIEW_RETRIEVAL_URL={url}\nITEM_REVIEW_RETRIEVAL_TOKEN={token}\n")
            status.update(state="ready", url=url)
            save_status()
            print(f"Retrieval is ready. Private Render settings: {state_dir / 'render.env'}", flush=True)
            while all(child.poll() is None for child in children):
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
