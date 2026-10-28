"""Read JSON incrementally and replace completed records before retaining them.

Transforms receive actual object keys and integer array positions, so a key
containing a dot or the word ``item`` cannot masquerade as a candidate path.
The parser buffers one input chunk; callers decide which completed mappings to
keep in memory and which to replace with references to their stored payloads.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import json
import math

import ijson


CHUNK_BYTES = 64 * 1024
_MISSING = object()


@dataclass
class _Frame:
    value: dict | list
    path: tuple[str | int, ...]
    key: str | None = None


class _Builder:
    def __init__(self, transform):
        self.transform = transform
        self.stack: list[_Frame] = []
        self.value = _MISSING

    def _path(self):
        if not self.stack:
            return ()
        parent = self.stack[-1]
        return (*parent.path, len(parent.value) if isinstance(parent.value, list) else parent.key)

    def _attach(self, value):
        if not self.stack:
            if self.value is not _MISSING:
                raise ValueError("JSON must contain exactly one value.")
            self.value = value
            return
        parent = self.stack[-1]
        if isinstance(parent.value, list):
            parent.value.append(value)
        else:
            if parent.key is None:
                raise ValueError("A JSON object value requires a key.")
            parent.value[parent.key] = value
            parent.key = None

    def event(self, event, value):
        if event in {"start_map", "start_array"}:
            self.stack.append(_Frame({} if event == "start_map" else [], self._path()))
        elif event == "map_key":
            self.stack[-1].key = value
        elif event in {"end_map", "end_array"}:
            frame = self.stack.pop()
            value = frame.value
            if event == "end_map" and self.transform is not None:
                value = self.transform(frame.path, value)
                if not isinstance(value, dict):
                    raise TypeError("A JSON mapping transform must return a dictionary.")
            self._attach(value)
        else:
            # use_float=True can overflow arbitrary-size integer values in the
            # native parser. Decimal conversion retains Python json's int/float
            # distinction, including 1.0 and negative floating-point zero.
            if isinstance(value, Decimal):
                value = float(value)
                if not math.isfinite(value):
                    raise ValueError("JSON numbers must be finite.")
            self._attach(value)

    def finish(self):
        if self.stack or self.value is _MISSING:
            raise ValueError("Incomplete JSON document.")
        return self.value


def load(stream, *, transform=None):
    """Parse a binary stream with bounded reads, transforming completed maps."""
    builder = _Builder(transform)
    try:
        for event, value in ijson.basic_parse(stream, buf_size=CHUNK_BYTES, use_float=False):
            builder.event(event, value)
    except ijson.JSONError as exc:
        raise ValueError("Invalid JSON document.") from exc
    return builder.finish()


async def async_load(stream, *, transform=None):
    """Async equivalent of load; the reader must implement await read(n)."""
    builder = _Builder(transform)
    try:
        async for event, value in ijson.basic_parse_async(stream, buf_size=CHUNK_BYTES, use_float=False):
            builder.event(event, value)
    except ijson.JSONError as exc:
        raise ValueError("Invalid JSON document.") from exc
    return builder.finish()


class BinaryChunkReader:
    """Adapt response.aiter_bytes(chunk_size=CHUNK_BYTES) to bounded reads."""

    def __init__(self, chunks):
        self.chunks = aiter(chunks)
        self.pending = memoryview(b"")
        self.exhausted = False

    async def read(self, size=-1):
        if size < 0:
            raise ValueError("Unbounded reads are not supported.")
        if size == 0:
            return b""
        while not self.pending and not self.exhausted:
            try:
                chunk = await anext(self.chunks)
            except StopAsyncIteration:
                self.exhausted = True
                break
            if not isinstance(chunk, (bytes, bytearray, memoryview)):
                raise TypeError("The JSON stream must yield bytes.")
            self.pending = memoryview(chunk)
        length = min(size, CHUNK_BYTES, len(self.pending))
        result = self.pending[:length].tobytes()
        self.pending = self.pending[length:]
        return result


def iterencode(value, *, expand=None, ensure_ascii=False, sort_keys=False,
               separators=(",", ":"), allow_nan=False):
    """Emit JSON while expanding each stored mapping only when it is visited.

    Expansion receives the same (path, mapping) arguments as parsing transforms.
    The replacement root is not expanded again. Its children still pass through
    expansion, allowing callers to restrict references to known candidate paths.
    """
    encoder = json.JSONEncoder(ensure_ascii=ensure_ascii, allow_nan=allow_nan)
    item_separator, key_separator = separators
    active = set()

    def encode(item, path):
        original = item
        if isinstance(item, dict) and expand is not None:
            item = expand(path, item)
            if not isinstance(item, dict):
                raise TypeError("JSON mapping expansion must return a dictionary.")
        if not isinstance(item, (dict, list, tuple)):
            yield encoder.encode(item)
            return
        identities = {id(original), id(item)}
        if identities & active:
            raise ValueError("Circular reference detected.")
        active.update(identities)
        try:
            if isinstance(item, dict):
                yield "{"
                entries = sorted(item.items()) if sort_keys else item.items()
                for index, (key, nested) in enumerate(entries):
                    if not isinstance(key, str):
                        raise TypeError("JSON object keys must be strings.")
                    if index:
                        yield item_separator
                    yield encoder.encode(key)
                    yield key_separator
                    yield from encode(nested, (*path, key))
                yield "}"
            else:
                yield "["
                for index, nested in enumerate(item):
                    if index:
                        yield item_separator
                    yield from encode(nested, (*path, index))
                yield "]"
        finally:
            active.difference_update(identities)

    yield from encode(value, ())
