"""Versioned, code-owned item classifier catalog. Context cannot redefine it."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path

CATALOG_VERSION = "caliper_generic_items_v1"
SPEC_SCHEMA_VERSION = "caliper_item_spec_v2"
LEGACY_SCHEMA_VERSION = "caliper_item_spec_legacy_v1"
LEGACY_CATALOG_VERSION = "caliper_induced_items_legacy_v1"
_CATALOG = json.loads(Path(__file__).with_name("catalog.json").read_text(encoding="utf-8"))
assert _CATALOG["version"] == CATALOG_VERSION


def get_catalog() -> list[dict]:
    """Detached rules; caller mutations cannot modify the catalog."""
    return deepcopy(_CATALOG["classifiers"])


def catalog_hash() -> str:
    return hashlib.sha256(json.dumps(_CATALOG, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def is_generic_spec(spec: dict) -> bool:
    return isinstance(spec, dict) and spec.get("fixed_catalog_version") == CATALOG_VERSION
