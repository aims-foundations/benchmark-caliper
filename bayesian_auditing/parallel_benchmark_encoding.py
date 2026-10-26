"""Run unchanged full-row BGE batches on persistent, explicitly assigned GPUs.

The parent owns source iteration and SQLite. Workers receive only ordered text
batches and return vectors; they never open the item bank or its checkpoint.
"""

from __future__ import annotations

from dataclasses import dataclass
import multiprocessing
from multiprocessing.connection import Connection, wait

import numpy as np

from .benchmark_encoding import FullRowBGEEncoder, _check_cancelled


def _encoder_worker(connection: Connection, device: str, batch_size: int, cpu_threads: int) -> None:
    """Initialize CUDA inside a spawned process, never in the parent process."""
    try:
        import torch

        torch.set_num_threads(cpu_threads)
        if device.startswith("cuda"):
            torch.cuda.set_device(device)
        encoder = FullRowBGEEncoder(device=device, batch_size=batch_size)
        connection.send(("ready", None))
        while True:
            texts = connection.recv()
            if texts is None:
                break
            connection.send(("result", encoder.encode(texts)))
    except EOFError:
        pass  # The parent closed its end during shutdown.
    except BaseException as error:
        try:
            connection.send(("error", f"{type(error).__name__}: {error}"))
        except (BrokenPipeError, EOFError, OSError):
            pass
    finally:
        connection.close()


@dataclass
class _Worker:
    device: str
    process: multiprocessing.Process
    connection: Connection


class ParallelFullRowBGEEncoder(FullRowBGEEncoder):
    """Keep one unchanged encoder per device, with one active batch per worker.

    Callers retain each single-encoder batch boundary. Results follow the input
    batch order even when workers finish out of order. Cancellation or failure
    closes the pool, so no orphan computation continues past a failed window.
    The instance is used by one caller at a time, like the SQLite index builder.
    """

    def __init__(self, devices: list[str], batch_size: int = 64, cpu_threads: int = 4):
        if (not devices or any(not isinstance(device, str) or not device.strip() for device in devices)
                or len(set(devices)) != len(devices)):
            raise ValueError("Encoding devices must be nonempty, unique device names")
        if type(cpu_threads) is not int or cpu_threads < 1:
            raise ValueError("CPU threads per encoding worker must be a positive integer")
        super().__init__(device=devices[0], batch_size=batch_size)
        self.devices = tuple(devices)
        self.cpu_threads = cpu_threads
        self._workers: list[_Worker] = []
        self._closed = False
        self._active = False

    @property
    def max_parallel_batches(self) -> int:
        return len(self.devices)

    def _receive(self, indices, expected: str, cancelled, row_counts=None) -> dict:
        pending = set(indices)
        results = {}
        connections = {self._workers[index].connection: index for index in pending}
        while pending:
            _check_cancelled(cancelled)
            for index in pending:
                worker = self._workers[index]
                if not worker.process.is_alive() and not worker.connection.poll():
                    raise RuntimeError(f"BGE worker on {worker.device} exited without returning its batch")
            for connection in wait([self._workers[index].connection for index in pending], timeout=0.05):
                index = connections[connection]
                worker = self._workers[index]
                try:
                    message = connection.recv()
                except (EOFError, OSError) as error:
                    raise RuntimeError(f"BGE worker on {worker.device} disconnected") from error
                if not isinstance(message, tuple) or len(message) != 2:
                    raise RuntimeError(f"BGE worker on {worker.device} returned an invalid response")
                kind, value = message
                if kind == "error":
                    raise RuntimeError(f"BGE worker on {worker.device} failed: {value}")
                if kind != expected:
                    raise RuntimeError(f"BGE worker on {worker.device} returned an unexpected response")
                if row_counts is not None and (
                    not isinstance(value, np.ndarray) or value.dtype != np.float32
                    or value.shape != (row_counts[index], self.dimensions) or not np.isfinite(value).all()
                ):
                    raise RuntimeError("A BGE worker returned invalid float32 vectors")
                results[index] = value
                pending.remove(index)
        _check_cancelled(cancelled)
        return results

    def _start(self, cancelled) -> None:
        if self._closed:
            raise RuntimeError("The parallel BGE encoder is closed")
        if self._workers:
            return
        context = multiprocessing.get_context("spawn")
        for device in self.devices:
            _check_cancelled(cancelled)
            parent, child = context.Pipe()
            process = context.Process(
                target=_encoder_worker, args=(child, device, self.batch_size, self.cpu_threads),
                name=f"benchmark-bge-{device}", daemon=True,
            )
            try:
                process.start()
            except BaseException:
                parent.close()
                process.close()
                raise
            finally:
                child.close()
            self._workers.append(_Worker(device, process, parent))
        self._receive(range(len(self._workers)), "ready", cancelled)

    def encode_batches(self, batches: list[list[str]], *, cancelled=None) -> list[np.ndarray]:
        """Encode a bounded window without repartitioning any original batch."""
        if self._closed:
            raise RuntimeError("The parallel BGE encoder is closed")
        if len(batches) > self.max_parallel_batches:
            raise ValueError("An encoding window cannot contain more batches than workers")
        if not batches:
            _check_cancelled(cancelled)
            return []
        self._active = True
        try:
            _check_cancelled(cancelled)
            self._start(cancelled)
            for index, texts in enumerate(batches):
                _check_cancelled(cancelled)
                worker = self._workers[index]
                try:
                    worker.connection.send(texts)
                except (BrokenPipeError, EOFError, OSError) as error:
                    raise RuntimeError(f"Could not send a batch to BGE worker on {worker.device}") from error
            results = self._receive(range(len(batches)), "result", cancelled, [len(texts) for texts in batches])
            return [results[index] for index in range(len(batches))]
        except BaseException:
            self.close()
            raise
        finally:
            self._active = False

    def encode(self, texts: list[str], *, cancelled=None):
        # Smoke-query encoding uses the first persistent worker. Document
        # batches use encode_batches so every worker receives its own work.
        return self.encode_batches([texts], cancelled=cancelled)[0]

    def close(self) -> None:
        """Let idle workers release resources; terminate active or stuck calls."""
        if self._closed:
            return
        self._closed = True
        workers, self._workers = self._workers, []
        for worker in workers:
            if worker.process.is_alive():
                if self._active:
                    worker.process.terminate()
                else:
                    try:
                        worker.connection.send(None)
                    except (EOFError, OSError):
                        worker.process.terminate()
            worker.connection.close()
        for worker in workers:
            worker.process.join(timeout=2)
            if worker.process.is_alive():
                worker.process.terminate()
        for worker in workers:
            worker.process.join(timeout=2)
            if worker.process.is_alive():
                worker.process.kill()
        for worker in workers:
            worker.process.join(timeout=2)
            if not worker.process.is_alive():
                worker.process.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
