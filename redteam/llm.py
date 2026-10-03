"""Real models for the red team: the live setup (Opus 5.5 medium strategist, Sonnet 5.5 low negotiator, each with its
backup), a spend meter that counts cache tokens too and stops every call at a cap, and a cassette cache so a rerun of
an unchanged prompt costs nothing.

Only ANTHROPIC_API_KEY is read from the main repo's .env; the game keys stay out of this process.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import threading
import time
from pathlib import Path
from typing import Any

from dotenv import dotenv_values

from engine import LLMError, Reply
from engine.claude import PRICES, Claude

from . import SCRATCH

ENV = Path(__file__).resolve().parents[2] / "claude-hackathon-team-5" / ".env"
if not os.environ.get("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = dotenv_values(ENV).get("ANTHROPIC_API_KEY") or ""

CAP_USD = float(os.environ.get("REDTEAM_CAP_USD", "15"))     # all red-team runs together
METER = SCRATCH / "spend.json"
_lock = threading.Lock()


def spent() -> float:
    try:
        return json.loads(METER.read_text())["usd"]
    except (FileNotFoundError, KeyError, ValueError):
        return 0.0


def charge(model: str, usage: Any, stage: str) -> float:
    pin, pout = PRICES.get(model, (5.0, 25.0))
    u = {k: getattr(usage, k, 0) or 0 for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens",
                                                 "cache_read_input_tokens")}
    cost = (u["input_tokens"] * pin + u["output_tokens"] * pout + u["cache_creation_input_tokens"] * pin * 1.25
            + u["cache_read_input_tokens"] * pin * 0.1) / 1e6
    with _lock, (SCRATCH / "spend.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)            # several red-team processes share the meter
        try:
            data = json.loads(METER.read_text())
        except (FileNotFoundError, ValueError):
            data = {"usd": 0.0, "calls": []}
        data["usd"] += cost
        data["calls"].append({"t": round(time.time(), 1), "model": model, "stage": stage, "usd": round(cost, 5), **u})
        METER.write_text(json.dumps(data))
    return cost


def metered(c: Claude, stage: str) -> Claude:
    """Wrap the client's parse calls: refuse past the cap, charge every reply with its cache tokens."""
    for api in (c._client.messages, c._client.beta.messages):
        orig = api.parse

        async def parse(*a, _orig=orig, **k):
            if spent() >= CAP_USD:
                raise LLMError(f"red-team spend cap ${CAP_USD} reached")
            msg = await _orig(*a, **k)
            charge(k.get("model", c.model), msg.usage, stage)
            return msg
        api.parse = parse
    return c


class Cassette:
    """Replays a stored reply for the same model, schema, system and messages; else calls through and stores it."""

    def __init__(self, inner: Any, name: str):
        self.inner, self.label = inner, getattr(inner, "label", name)
        self.path = SCRATCH / "cassettes" / f"{name}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.store: dict[str, Any] = {}
        if self.path.exists():
            for line in self.path.read_text().splitlines():
                k, v = json.loads(line)
                self.store[k] = v
        self.hits = self.misses = 0

    async def parse(self, schema, system, messages) -> Reply:
        key = hashlib.sha256(json.dumps([self.label, schema.__name__, system, messages]).encode()).hexdigest()
        if key in self.store:
            self.hits += 1
            v = self.store[key]
            return Reply(schema.model_validate(v["parsed"]), v["latency_s"], 0, 0, 0.0, "cassette")
        self.misses += 1
        r = await self.inner.parse(schema, system, messages)
        self.store[key] = {"parsed": r.parsed.model_dump(), "latency_s": r.latency_s}
        with self.path.open("a") as f:
            f.write(json.dumps([key, self.store[key]]) + "\n")
        return r


def live_models(model: str = "claude-opus-5-5", effort: str = "medium", negotiator_model: str = "claude-sonnet-5-5",
                negotiator_effort: str = "low", cassette: str | None = None, failover: bool = True):
    """The live duelist's models (agents/duelist/__main__.models), metered; optionally behind a cassette."""
    from agents.duelist.__main__ import models
    a = argparse.Namespace(model=model, effort=effort, negotiator_model=negotiator_model,
                           negotiator_effort=negotiator_effort, thinking_off=False, no_failover=not failover)
    s, n = models(a)
    for m, stage in ((s, "strategist"), (n, "negotiator")):
        for c in (m.primary, m.backup) if hasattr(m, "primary") else (m,):
            metered(c, stage)
    if cassette:
        s, n = Cassette(s, f"{cassette}-strategist"), Cassette(n, f"{cassette}-negotiator")
    return s, n
