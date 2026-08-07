"""Incremental-backfill bookkeeping.

A tiny JSON file (store/_catalog.json) mapping a dataset/partition key to the
last fully-fetched date (ISO-8601). Backfills consult it to skip work already on
disk and to resume after interruption. Atomic writes; coarse lock for parallel
backfills in one process.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

from .config import get_settings

_lock = threading.Lock()


def _path() -> Path:
    return get_settings().store_root / "_catalog.json"


def _load() -> dict:
    p = _path()
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def get_watermark(key: str) -> str | None:
    return _load().get(key)


def set_watermark(key: str, value: str) -> None:
    with _lock:
        data = _load()
        data[key] = value
        p = _path()
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
        tmp.replace(p)


def all_watermarks() -> dict:
    return _load()
