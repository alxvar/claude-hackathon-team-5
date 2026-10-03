"""Shared by the recorder, the broker and the replay: keyless reads, the tick clock, the broker key, key scrubbing."""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "bazaar-kit") not in sys.path:
    sys.path.insert(0, str(ROOT / "bazaar-kit"))

from bazaar_sdk import Bazaar, BazaarError, Broker, _Http  # noqa: E402,F401

URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
BENCH_DIR = ROOT / "data" / "bench"


class Public(_Http):
    """Keyless reads (60/s per address): they never touch the team key's shared 5/s, and never send an empty key
    (a wrong key counts toward the server's too_many_failures throttle)."""

    def __init__(self, url: str = URL, timeout: float = 10.0, retries: int = 2):
        super().__init__(url, {}, timeout, False, retries)

    def clock(self) -> dict:
        return self._call("GET", "/api/clock")

    def schedule(self) -> dict:
        return self._call("GET", "/api/schedule")

    def leaderboard(self) -> dict:
        return self._call("GET", "/api/leaderboard")

    def venues(self) -> dict:
        return self._call("GET", "/api/venues")


def scrub(x):
    """A copy of x without any field whose name contains 'key' (broker or team keys never reach a file or a log)."""
    if isinstance(x, dict):
        return {k: scrub(v) for k, v in x.items() if "key" not in str(k).lower()}
    if isinstance(x, list):
        return [scrub(v) for v in x]
    return x


def _key_fields(x, path=""):
    if isinstance(x, dict):
        for k, v in x.items():
            p = f"{path}.{k}" if path else str(k)
            if "broker_key" in str(k).lower() and isinstance(v, str) and v:
                yield p, v
            else:
                yield from _key_fields(v, p)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from _key_fields(v, f"{path}[{i}]")


def find_broker_key(team: Bazaar | None, me: dict | None = None) -> tuple[str | None, str, dict | None]:
    """(key, where it came from, the /api/me it read). Env BROKER_KEY (our own venue) wins; otherwise the free stall's
    key in /api/me (`starter_broker_key` per the SDK docstring; any *broker_key field is accepted). The key itself is
    never printed or written."""
    if os.environ.get("BROKER_KEY"):
        return os.environ["BROKER_KEY"], "env BROKER_KEY", me
    if me is None:
        if team is None:
            return None, "no BROKER_KEY and no BAZAAR_KEY to look one up", None
        me = team.me()
    for where, value in _key_fields(me):
        return value, f"/api/me field {where}", me
    return None, "no broker key in /api/me yet (the free stall only exists from game hour 3.0)", me


class TickClock:
    """The current tick at the cost of ~2 clock reads per tick: it re-reads only around the expected tick boundary
    (and every `max_age` s), so a book read just after a tick is labelled with the new tick."""

    def __init__(self, fetch, max_age: float = 10.0):
        self.fetch, self.max_age = fetch, max_age
        self.c: dict = {}
        self.read_at = self.boundary = 0.0

    def read(self) -> dict:
        now = time.monotonic()
        if not self.c or now - self.read_at > self.max_age or now >= self.boundary - 0.4:
            self.c = self.fetch()
            self.read_at = now
            paused = self.c.get("paused") or self.c.get("doors") == "closed"
            self.boundary = now + (30.0 if paused else max(0.0, float(self.c.get("next_tick_in") or 0.0)))
        return self.c
