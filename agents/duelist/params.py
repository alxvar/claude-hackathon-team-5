"""Hot-reloaded tuning parameters (Chief, Sat 22:00, for the Duel Lab's tuner between waves): run/duel_params.json
holds overrides of the duelist's code constants, re-read every tick, so a tuned value takes effect on the next tick
with no restart.

    {"_note": "wave 3 proposal, approved by Aleks 09:12", "MAX_STEP_SHARE": 0.15, "HOLD_TICKS": 5}

- Defaults are today's constants, read from the modules at start: a key absent from the file (or no file) means the
  default, so deleting a line or the file reverts it.
- Every key is bounds-checked (SPEC) and the set is cross-checked (MIN_STEP_SHARE <= MAX_STEP_SHARE, ...). A file
  with any bad key, a bad value or broken JSON changes NOTHING: the last good set stays and the error is logged, so a
  half-written tuning never plays.
- Every change is logged (old → new) by the runner, to the console and the JSONL log, and each new duel's record
  carries the effective set.
- Keys starting with "_" are notes. The constants are module globals read at call time, so setting them on the module
  is all a change needs (the strategist's prompt text names some of them: a new value reaches the prompt of duels that
  start after it).

The duelist runs on Aleks's machine: the file is the one under that checkout's run/ (or --params / DUEL_PARAMS).
`tools/duel_loop.py approve` writes it; nothing else does.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PATH = Path(os.environ.get("DUEL_PARAMS") or ROOT / "run" / "duel_params.json")


@dataclass(frozen=True)
class Spec:
    module: str                  # "agent", "runner" or "policy": where the constant lives
    lo: float
    hi: float
    kind: type = float
    sim: str | None = None       # the Duel Lab simulator's policy key, when it models it (tools/duel_sim.py)
    what: str = ""


SPEC: dict[str, Spec] = {
    # concessions (agent.py)
    "MIN_STEP_P": Spec("agent", 0, 15, float, "smin", "a concession smaller than this (P, in worth) is held"),
    "MIN_STEP_SHARE": Spec("agent", 0, 0.30, float, "smin_share", "...or smaller than this share of the gap"),
    "MAX_STEP_SHARE": Spec("agent", 0.05, 0.60, float, "cap_share", "a mid-duel concession is cut to this share of the gap"),
    "CLOSING_TICKS": Spec("agent", 1, 6, int, "end_ticks", "the last ticks: no hold, no cut"),
    # the silent rival (agent.py)
    "SILENT_FROM": Spec("agent", 0.2, 0.9, float, None, "the silent walk starts with this share of the ticks left"),
    "SILENT_KEEP": Spec("agent", 0.0, 0.6, float, "walk_floor", "share of the opener's distance never conceded"),
    "SILENT_BY": Spec("agent", 1, 5, int, None, "the walk reaches its floor with this many ticks left"),
    # the delivery day (agent.py)
    "LATE_SWITCH_LEFT": Spec("agent", 0, 8, int, None, "ticks left from which code offers their day once"),
    "GUARDS": Spec("agent", 0, 1, int, None, "1: the 6190 guards on (accept-instead, worth floor, first-offer day)"),
    "MONO_END_SHARE": Spec("agent", 0.1, 1.0, float, None, "worth floor in the last ticks: at most this share of the gap"),
    "DAY_SAME_SIDE_P": Spec("agent", 0, 10, float, None, "their day costs us at most this: take it"),
    "GIVE_COST_P": Spec("agent", 0, 40, float, None, "their day costing at most this is cheap to give"),
    "SWING_LOW_P": Spec("agent", 0, 60, float, None, "a 10-day swing up to this is a low weight"),
    "SWING_HIGH_P": Spec("agent", 0, 100, float, None, "from this, a high one"),
    "RANK_SAMPLES": Spec("agent", 2, 12, int, None, "weights seen before ours is ranked"),
    "RANK_LOW": Spec("agent", 0.1, 0.9, float, None, "ranked below this share: low"),
    "RANK_HIGH": Spec("agent", 0.1, 0.95, float, None, "ranked from this share: high"),
    # when to decide and accept (runner.py)
    "DECIDE_LEFT": Spec("runner", 1, 6, int, None, "ticks left from which we decide every tick"),
    "ACCEPT_BY": Spec("runner", 1, 4, int, "deadline_acc", "an offer inside our limit is accepted by this many ticks left"),
    "OPEN_WAIT": Spec("runner", 0, 4, int, "wait_first", "a days duel waits this many ticks for their first offer"),
    "HOLD_TICKS": Spec("runner", 2, 8, int, "hold_break", "both sides still this long: decide again"),
    "SMALL_GAP_P": Spec("runner", 0, 10, float, None, "accept when the gap is at most this (P)..."),
    "SMALL_GAP_ROUNDS": Spec("runner", 0, 4, float, None, "...or at most this many rounds of decay on the surplus"),
    # the code-first policy (policy.py, --policy code)
    "OPENER_SHARE": Spec("policy", 0.05, 1.5, float, "u_scale", "our opener's distance from our limit, as a share of it"),
    "CODE_STEP_SHARE": Spec("policy", 0.03, 0.6, float, "alpha", "a mid-duel concession: this share of the gap"),
    "END_STEP_SHARE": Spec("policy", 0.1, 1.0, float, "end_alpha", "in the last CLOSING_TICKS: this share"),
    "ACCEPT_NEAR_P": Spec("policy", 0, 10, float, None, "their offer within this of our step's landing: take it"),
    "ACCEPT_RATIO": Spec("policy", 0.5, 1.0, float, "acc_ratio", "take their offer at this share of ours (1.0: off)"),
    "TEXT_TIMEOUT_S": Spec("policy", 0.5, 8.0, float, None, "the text model's budget; then code's plain text"),
}
CROSS = [("MIN_STEP_SHARE", "MAX_STEP_SHARE"), ("SWING_LOW_P", "SWING_HIGH_P"), ("RANK_LOW", "RANK_HIGH"),
         ("ACCEPT_BY", "DECIDE_LEFT"), ("CODE_STEP_SHARE", "END_STEP_SHARE")]   # (a, b): a <= b


def validate(data: Any) -> tuple[dict[str, Any], list[str]]:
    """(the overrides, the errors) of a parsed params file; any error means the file is not applied."""
    if not isinstance(data, dict):
        return {}, ["the file must be a JSON object"]
    out, errors = {}, []
    for k, v in data.items():
        if k.startswith("_"):
            continue
        spec = SPEC.get(k)
        if spec is None:
            errors.append(f"{k}: unknown parameter")
            continue
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            errors.append(f"{k}: {v!r} is not a number")
            continue
        if spec.kind is int and float(v) != int(v):
            errors.append(f"{k}: {v!r} must be a whole number")
            continue
        if not spec.lo <= v <= spec.hi:
            errors.append(f"{k}: {v!r} outside [{spec.lo:g}, {spec.hi:g}]")
            continue
        out[k] = spec.kind(v)
    return out, errors


class Params:
    """The effective values: defaults read from the modules, overridden by the file. `reload()` once per tick."""

    def __init__(self, modules: dict[str, ModuleType], path: Path | None = None):
        self.modules, self.path = modules, Path(path or PATH)
        self.defaults = {k: getattr(modules[s.module], k) for k, s in SPEC.items() if s.module in modules}
        self.current = dict(self.defaults)
        self._stamp: Any = None
        self.last_error: list[str] = []

    def _read(self) -> tuple[dict[str, Any] | None, list[str]]:
        try:
            raw = self.path.read_text()
        except FileNotFoundError:
            return {}, []
        except OSError as e:
            return None, [f"unreadable: {e}"]
        try:
            data = json.loads(raw)
        except ValueError as e:
            return None, [f"broken JSON: {e}"]
        over, errors = validate(data)
        return (None, errors) if errors else (over, [])

    def reload(self) -> dict[str, Any]:
        """{"changed": {name: [old, new]}, "errors": [...]} when the file changed since the last read, else {}."""
        try:
            st = self.path.stat()
            stamp = (st.st_mtime_ns, st.st_size)
        except FileNotFoundError:
            stamp = None
        except OSError:
            stamp = "?"
        if stamp == self._stamp:
            return {}
        self._stamp = stamp
        over, errors = self._read()
        if over is None:
            self.last_error = errors
            return {"changed": {}, "errors": errors}
        want = {**self.defaults, **{k: v for k, v in over.items() if k in self.defaults}}
        bad = [f"{a} {want[a]} > {b} {want[b]}" for a, b in CROSS if a in want and b in want and want[a] > want[b]]
        if bad:
            self.last_error = bad
            return {"changed": {}, "errors": bad}
        changed = {k: [self.current[k], v] for k, v in want.items() if self.current.get(k) != v}
        for k, (_, v) in changed.items():
            setattr(self.modules[SPEC[k].module], k, v)
            self.current[k] = v
        self.last_error = []
        return {"changed": changed, "errors": []}

    def overrides(self) -> dict[str, Any]:
        """The values that differ from today's defaults."""
        return {k: v for k, v in self.current.items() if v != self.defaults.get(k)}


def modules() -> dict[str, ModuleType]:
    from . import agent, policy, runner
    return {"agent": agent, "runner": runner, "policy": policy}
