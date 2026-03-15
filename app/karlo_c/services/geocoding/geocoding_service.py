from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
from threading import Lock
from time import time
from typing import Any
import json

import requests


BASE_DIR = Path(__file__).resolve().parent
CACHE_FILE = BASE_DIR / "geocode_cache.json"
CACHE_TTL_SECONDS = 60 * 60 * 24 * 7
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 10
USER_AGENT = "KarLo/1.0 (location-reminder app)"

_cache_lock = Lock()
_rate_limit_lock = Lock()
_rate_limit_buckets: dict[str, deque[float]] = defaultdict(deque)


def _load_cache() -> dict[str, dict[str, Any]]:
    if not CACHE_FILE.exists():
        return {}

    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_cache(cache: dict[str, dict[str, Any]]) -> None:
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=True, indent=2), encoding="utf-8")


def _cache_get(key: str) -> list[dict[str, Any]] | None:
    with _cache_lock:
        cache = _load_cache()
        payload = cache.get(key)
        if not payload:
            return None

        if time() - payload.get("timestamp", 0) > CACHE_TTL_SECONDS:
            cache.pop(key, None)
            _save_cache(cache)
            return None

        return payload.get("results", [])


def _cache_set(key: str, results: list[dict[str, Any]]) -> None:
    with _cache_lock:
        cache = _load_cache()
        cache[key] = {
            "timestamp": time(),
            "results": results,
        }
        _save_cache(cache)


def _enforce_rate_limit(client_key: str) -> None:
    now = time()
    with _rate_limit_lock:
        bucket = _rate_limit_buckets[client_key]
        while bucket and now - bucket[0] > RATE_LIMIT_WINDOW_SECONDS:
            bucket.popleft()

        if len(bucket) >= RATE_LIMIT_MAX_REQUESTS:
            raise ValueError("Geocoding rate limit exceeded. Please wait a moment and try again.")

        bucket.append(now)


def search_places(query: str, client_key: str) -> list[dict[str, Any]]:
    normalized = query.strip().lower()
    if not normalized:
        return []

    cache_key = f"search::{normalized}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    _enforce_rate_limit(client_key)

    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={
            "q": normalized,
            "format": "jsonv2",
            "addressdetails": 1,
            "limit": 5,
        },
        headers={"User-Agent": USER_AGENT},
        timeout=10,
    )
    response.raise_for_status()

    raw_results = response.json()
    results = [
        {
            "display_name": item.get("display_name"),
            "lat": float(item.get("lat")),
            "lon": float(item.get("lon")),
        }
        for item in raw_results
    ]
    _cache_set(cache_key, results)
    return results


def reverse_geocode(latitude: float, longitude: float, client_key: str) -> dict[str, Any]:
    cache_key = f"reverse::{latitude:.5f}:{longitude:.5f}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached[0] if cached else {}

    _enforce_rate_limit(client_key)

    response = requests.get(
        "https://nominatim.openstreetmap.org/reverse",
        params={
            "lat": latitude,
            "lon": longitude,
            "format": "jsonv2",
        },
        headers={"User-Agent": USER_AGENT},
        timeout=10,
    )
    response.raise_for_status()

    payload = response.json()
    result = {
        "display_name": payload.get("display_name"),
        "lat": latitude,
        "lon": longitude,
    }
    _cache_set(cache_key, [result])
    return result