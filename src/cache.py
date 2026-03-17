from __future__ import annotations

import hashlib
import json
import logging
import threading
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class CacheBackend(ABC):
    """Abstract interface every cache backend must implement."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]: ...

    @abstractmethod
    def set(self, key: str, value: Any) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...


class NoCache(CacheBackend):
    """Pass-through — nothing is ever stored."""

    def get(self, key: str) -> None:
        return None

    def set(self, key: str, value: Any) -> None:
        pass

    def delete(self, key: str) -> None:
        pass

    def clear(self) -> None:
        pass

    def __repr__(self) -> str:
        return "NoCache()"


class MemoryCache(CacheBackend):
    """
    Thread-safe, in-process TTL cache.

    Parameters
    ----------
    ttl : int
        Seconds before an entry expires (default 60).
    max_size : int
        Maximum entries; oldest is evicted when exceeded (default 512).
    """

    def __init__(self, ttl: int = 60, max_size: int = 512):
        self._ttl = ttl
        self._max_size = max_size
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, expires_at = entry
            if time.monotonic() > expires_at:
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            if len(self._store) >= self._max_size:
                del self._store[next(iter(self._store))]
            self._store[key] = (value, time.monotonic() + self._ttl)

    def delete(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._store)

    def __repr__(self) -> str:
        return f"MemoryCache(ttl={self._ttl}, max_size={self._max_size}, size={self.size})"


class FileCache(CacheBackend):
    """
    Disk-based TTL cache.  Each entry is one JSON file + one metadata file.

    Parameters
    ----------
    ttl : int
        Seconds before an entry expires (default 300).
    directory : str | Path
        Cache directory, created automatically (default ``/tmp/opta_sdapi_cache``).
    """

    def __init__(self, ttl: int = 300, directory: str | Path = "/tmp/opta_sdapi_cache"):
        self._ttl = ttl
        self._dir = Path(directory)
        self._dir.mkdir(parents=True, exist_ok=True)

    def _hash(self, key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()

    def _data_path(self, key: str) -> Path:
        return self._dir / f"{self._hash(key)}.json"

    def _meta_path(self, key: str) -> Path:
        return self._dir / f"{self._hash(key)}.meta"

    def get(self, key: str) -> Optional[Any]:
        meta, data = self._meta_path(key), self._data_path(key)
        if not meta.exists() or not data.exists():
            return None
        try:
            if time.time() > float(meta.read_text()):
                self.delete(key)
                return None
            return json.loads(data.read_text(encoding="utf-8"))
        except (ValueError, OSError, json.JSONDecodeError):
            return None

    def set(self, key: str, value: Any) -> None:
        try:
            payload = json.dumps(value, ensure_ascii=False)
        except (TypeError, ValueError):
            logger.debug("FileCache: skipping non-serialisable value for key %.80s", key)
            return
        try:
            self._data_path(key).write_text(payload, encoding="utf-8")
            self._meta_path(key).write_text(str(time.time() + self._ttl))
        except OSError as exc:
            logger.warning("FileCache: write failed: %s", exc)

    def delete(self, key: str) -> None:
        for p in (self._data_path(key), self._meta_path(key)):
            p.unlink(missing_ok=True)

    def clear(self) -> None:
        for p in list(self._dir.glob("*.json")) + list(self._dir.glob("*.meta")):
            p.unlink(missing_ok=True)

    def __repr__(self) -> str:
        return f"FileCache(ttl={self._ttl}, directory={str(self._dir)!r})"