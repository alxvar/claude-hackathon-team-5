"""The wave loop (Chief, Sat 22:00): after each closed wave of our duels, set it against the Duel Lab simulator and
propose a params diff for the duelist. It never applies anything itself: a human runs `approve`.

    python3 tools/duel_loop.py run [--wave latest|N|S.N] [--records docs/duels] [--params run/duel_params.json] [--dry]
    python3 tools/duel_loop.py approve [--proposal run/duel_loop_proposal.json] [--params ...] [--only A,B] [--by NAME]
    python3 tools/duel_loop.py revert [--params ...] [--by NAME]
    python3 tools/duel_loop.py watch [--every 60]
    python3 tools/duel_loop.py use SET --by NAME            # write one approved set (docs/duel_sets.json), whole
    python3 tools/duel_loop.py switch [--every 60] [--dry]  # the Duel Lab's one-way switch rule, on the duelist's machine

`run`, step by step:
1. The wave. Our duels of a session, in the order they started, cut into chunks of the session's `max_concurrent`
   (else the number that started together at the session's first tick: the first wave is always full). A wave is
   closed when every duel in it has the game's final payload; a short last chunk only once the session is over. Per
   duel: the result, the surplus (the game's result undone from the decay), what the rounds cost
   (surplus x (1 - (1 - d)^rounds)), the settled day against our best one, the rival's best in-limit offer when
   it beat what we got, and the share of the pie where our duel points (`scores.jsonl`) jumped for that deal alone.
2. The simulator (`tools/duel_sim_v2.py`, the Duel Lab's final: role-aware, price + delivery day; Chief 00:30):
   today's effective params (the constants in agents/duelist/, read from the source, plus the overrides in
   run/duel_params.json) mapped to a sim policy through its POLICY_KEYS, run with the session's ticks and decay in
   every role-aware world (RW), and the world closest to the wave named.
3. The proposal: one-parameter tweaks around today's values, paired against today's policy in that world. Only a
   tweak whose 95% CI is entirely above 0 and that passes `params.validate` and the CROSS checks is proposed;
   "no change proposed" is a valid outcome. Rule notes from the wave go next to it, never into the JSON.
Only a session at the setting the Duel Lab simulated proposes anything (TARGET: Duels III and the Final, 12 ticks at
10% decay; Chief 00:50): Duels III starts from the Duel Lab's file (docs/duels3-start.json), and a wave of another
setting (Duels II: 16 / 8%) still gets its summary and the simulator's comparison, never a proposal.
4. The Duel Lab's switch rule (`tools/duel_gates.py`, SUNDAY v2) on the session so far, shown with its counts: at
   least 12 closed duels with a rival that spoke and a deal rate below 0.60 → the pre-approved fallback set (C → A,
   A → today; docs/duel_sets.json), once, never back. `run` only reports it; `switch` applies it.

Sets (audit, Sun 01:00): `use SET` writes one approved set from docs/duel_sets.json as the WHOLE params file (every
set lists the same keys, so nothing of the previous set remains), with `_set` naming it; `switch` watches the
records on the duelist's machine and, when the rule fires, writes the fallback set the same way (once per set, never
back, never from a file that isn't an approved set; run/duel_switch.off or --dry stops it).

Writes intel/duel-loop.md (newest wave on top), run/duel_loop_proposal.json and, for `watch`, run/duel_loop_state.json.
`approve` and `revert` write the params file the duelist re-reads every tick (agents/duelist/params.py). No network,
no game calls. Stdlib only, so it runs with a bare `python3`.
"""
from __future__ import annotations

import argparse
import ast
import json
import math
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.duelist import params as pm  # noqa: E402  (stdlib only; never imports the agent itself)
from agents.duelist.days import DayValues, read_days  # noqa: E402
from tools import duel_monitor as dm  # noqa: E402
from tools import duel_gates as dg  # noqa: E402
from tools import duel_sim_v2 as sim  # noqa: E402

RECORDS = ROOT / "docs" / "duels"
DUELIST = ROOT / "agents" / "duelist"            # where the constants live (SPEC's modules)
OUT = ROOT / "intel" / "duel-loop.md"
PROPOSAL = ROOT / "run" / "duel_loop_proposal.json"
STATE = ROOT / "run" / "duel_loop_state.json"
OUT_HEADER = (
    "# Duel loop\n\n"
    "_Written by `tools/duel_loop.py` after each closed wave of our duels, newest first: the wave set against the Duel "
    "Lab simulator (`tools/duel_sim_v2.py`) and its live gates, and a params proposal for `run/duel_params.json`. Nothing here plays until a "
    "human runs the approve command. Score = share of the pie × (1 − decay)^rounds, i.e. duel points per duel._\n")

N_SIM = 4000                 # duels per world and per tweak: 0.1-0.2 s each, a CI of about ±0.006 on a level
SEED = 1                     # the same seed everywhere, so every comparison is paired (common random numbers)
ROUNDS_SCALE = 5.0           # world distance: a 5-round miss weighs like a 1.0 miss in deal rate or share
MISSED_MIN_P = 0.5           # an in-limit offer beat our result by more than this (the game rounds results to 0.1)
DECAY_SHARE_HIGH = 0.25      # rule note: rounds cost more than this share of the surplus...
ROUNDS_HIGH = 5.0            # ...or deals took this many rounds on average
LATENCY_P90_S = 10.0         # rule note: the runner's budget is max(8, tick - 5) s, 10 s at 15 s ticks
DAY_COST_HIGH_P = 15.0       # rule note: a deal settled on a day costing us this much against our best (GIVE_COST_P)
DEFAULT_SIZE = 3             # wave size when neither the session nor the records say
# The tweaks tried around today's values: (name, "+" or "x", amount). OPENER_SHARE only plays with --policy code.
TWEAKS = [("MAX_STEP_SHARE", "+", 0.03), ("MAX_STEP_SHARE", "+", -0.03),
          ("MIN_STEP_SHARE", "+", 0.03), ("MIN_STEP_SHARE", "+", -0.03),
          ("HOLD_TICKS", "+", 1), ("HOLD_TICKS", "+", -1),
          ("SILENT_KEEP", "+", 0.05), ("SILENT_KEEP", "+", -0.05),
          ("ACCEPT_BY", "+", 1), ("ACCEPT_BY", "+", -1),
          ("MIN_STEP_P", "+", 1), ("MIN_STEP_P", "+", -1),
          ("MONO_END_SHARE", "+", 0.1), ("MONO_END_SHARE", "+", -0.1),
          ("LATE_SWITCH_LEFT", "+", 1), ("LATE_SWITCH_LEFT", "+", -1)]
# What the simulator can't see, printed next to a proposal that moves a name that way. It never blocks a proposal.
CAVEATS = {
    ("ACCEPT_BY", "down"): "the sim never has an accept refused or late; below 2 no spare tick is left for an accept "
                           "the game refuses (runner.py), and the Duel Lab judged its gain not worth that risk "
                           "(intel/duel-lab.md §3, deadline accepts)",
    ("ACCEPT_BY", "up"): "accepting earlier lost in every exact replay of our transcripts (intel/duel-lab.md §0 #2)",
    ("HOLD_TICKS", "down"): "the sim forces a step when the hold breaks; the duelist asks the models again, which "
                            "costs a model call per duel and may still hold",
}
# Moves the simulator can't judge at all: shown with their simulated gain, never put in a proposal (Builder 22:40:
# ACCEPT_BY 1 leaves no spare tick for an accept the game refuses, a failure the sim doesn't have).
BLOCKED = {("ACCEPT_BY", "down")}


def stamp(fmt: str = "%a %H:%M") -> str:
    return time.strftime(fmt)


def write_atomic(path: Path, text: str) -> None:
    """tmp + rename in the same folder: a reader (the duelist's tick) sees the old file or the new one, never half."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    try:
        tmp.write_text(text)
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def read_jsonl(p: Path) -> list[dict]:
    out = []
    try:
        lines = p.read_text().splitlines()
    except OSError:
        return []
    for line in lines:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def num(x: Any) -> float | None:
    return float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else None


# ---------------------------------------------------------------------------------------------------- the duels

@dataclass
class Duel:
    """One of our duels as the loop reads it: the game's final payload first, our record around it."""
    id: Any
    session: Any
    start: int | None                # the tick it started: deadline - duel_ticks, else when we first saw it
    finished: bool
    status: str
    role: str
    rival: str
    limit: float | None
    decay: float
    rounds: int
    days_duel: bool = False          # the duel settles a delivery day too (Duels II on)
    price: float | None = None
    day: int | None = None
    result: float | None = None      # the game's result, in P: our surplus x (1 - d)^rounds
    surplus: float | None = None     # deals: our worth at the deal before decay, the day included
    decay_lost: float | None = None  # deals: what the rounds cost, surplus x (1 - (1 - d)^rounds)
    points: float | None = None      # our duel_points jump for this deal alone (share x decay), when one is found
    share: float | None = None       # points undone from the decay: our share of the pie
    dv: DayValues | None = None
    best_day: int | None = None
    day_cost: float | None = None    # deals: what the settled day cost us against our best day, P
    missed: dict | None = None       # the rival's best in-limit offer, when it beat what we got
    spoke: bool = False              # the rival sent at least one price
    behaviour: str = ""
    hold_flag: bool = False
    decisions: list = field(default_factory=list)

    @property
    def deal(self) -> bool:
        return self.status == "deal"


def sessions_of(folder: Path) -> tuple[dict[Any, dict], set]:
    """Each duel session's params from the feed's `duels.scheduled`, by number, and the numbers that finished."""
    events = read_jsonl(folder / "feed.jsonl")
    params = {e["payload"]["session"]: e["payload"] for e in events
              if e.get("type") == "duels.scheduled" and "session" in (e.get("payload") or {})}
    over = {(e.get("payload") or {}).get("session") for e in events if e.get("type") == "duels.finished"}
    return params, over - {None}


def closes_of(folder: Path) -> dict[Any, int]:
    """The tick each duel closed, from the feed's `duel.closed` (the tick its points land on)."""
    return {(e.get("payload") or {}).get("duel"): e["tick"] for e in read_jsonl(folder / "feed.jsonl")
            if e.get("type") == "duel.closed" and isinstance(e.get("tick"), int)}


def points_of(folder: Path, deals: dict[Any, int]) -> dict[Any, float]:
    """Each deal's duel points: the jump of our `duel_points` over a score interval that holds that deal alone
    (intel/duel-lab.md §1: the jump fits share x (1 - d)^rounds; matched to the feed's close tick, every share is
    <= 1). `deals`: duel -> close tick, for every deal of ours. Samples without a tick are skipped, so an interval
    spans them."""
    samples = [(s["tick"], num(s.get("duel_points"))) for s in read_jsonl(folder / "scores.jsonl")
               if isinstance(s.get("tick"), int) and num(s.get("duel_points")) is not None]
    out = {}
    for (t0, p0), (t1, p1) in zip(samples, samples[1:]):
        inside = [d for d, t in deals.items() if t0 < t <= t1]
        if len(inside) == 1:
            out[inside[0]] = round(p1 - p0, 4)
    return out


def day_values(raw: dict) -> DayValues | None:
    """Our value of each day, as the duelist reads it (`days.read_days`, the auto reading); None on price only."""
    if "days" not in (raw.get("issues") or []):
        return None
    weight = raw.get("your_days_weight", raw.get("days_weight"))
    return None if weight is None else read_days(weight, raw.get("days_meaning"), mode="auto")


def worth(raw: dict, dv: DayValues | None, price: float, day: Any) -> float | None:
    """What a deal at `price` on `day` is worth to us before decay (`guards.worth`): the price's margin over our
    limit plus the day's value in the game's terms (`dv.offset`: a seller's day bonus counts from day 0)."""
    limit = num(raw.get("your_limit"))
    if limit is None:
        return None
    day_value = 0.0 if dv is None else dv(day if isinstance(day, int) else None) + dv.offset
    return dm.sign(raw.get("role")) * (price - limit) + day_value


def best_missed(raw: dict, dv: DayValues | None, result: float, d: float) -> dict | None:
    """The rival's best in-limit offer, valued as if we had accepted it when it arrived (rounds then = the smaller of
    the two sides' message counts, priced or not), when it beat our result by more than MISSED_MIN_P (or the duel
    ended with no deal). None when no in-limit offer beat what we got."""
    ours = theirs = 0
    best = None
    for m in dm.messages(raw):
        if dm.is_ours(m):
            ours += 1
            continue
        theirs += 1
        if not dm.priced(m):
            continue
        w = worth(raw, dv, m["price"], m.get("days"))
        if w is None or w <= 0:
            continue
        value = w * (1 - d) ** min(ours, theirs)
        if best is None or value > best["value"]:
            best = {"tick": m.get("tick"), "price": m["price"], "day": m.get("days"), "value": round(value, 1)}
    if best is None:
        return None
    lost = best["value"] - (result if raw.get("status") == "deal" else 0.0)
    if raw.get("status") == "deal" and lost <= MISSED_MIN_P:
        return None
    return {**best, "lost": round(lost, 1)}


def read_duel(rec: dict, sessions: dict[Any, dict]) -> Duel:
    done = rec.get("done") or {}
    payloads = rec.get("payloads") or []
    raw = {**((payloads[-1].get("raw") or {}) if payloads else {}), **done}
    view = rec.get("view") or {}
    session = raw.get("session")
    sp = sessions.get(session) or {}
    ticks = sp.get("duel_ticks") or view.get("duel_ticks")
    deadline = raw.get("deadline_tick")
    start = (deadline - ticks if isinstance(deadline, int) and isinstance(ticks, int) else
             rec.get("first_tick") if isinstance(rec.get("first_tick"), int) else
             payloads[0].get("tick") if payloads else None)
    status = str(done.get("status", "")).lower()
    d = num(raw.get("decay_per_round")) or num(sp.get("decay")) or num(view.get("decay")) or 0.0
    msgs = dm.messages(raw)
    rounds = raw["rounds"] if isinstance(raw.get("rounds"), int) else min(
        sum(1 for m in msgs if dm.is_ours(m)), sum(1 for m in msgs if not dm.is_ours(m)))
    dv = day_values(raw)
    x = Duel(id=rec.get("duel", dm.rid(raw)), session=session, start=start, finished=status not in ("", "live"),
             status=status, role=str(raw.get("role") or view.get("role") or "?"), rival=str(raw.get("rival") or "?"),
             limit=num(raw.get("your_limit")), decay=d, rounds=rounds, dv=dv, decisions=rec.get("decisions") or [],
             days_duel="days" in (raw.get("issues") or view.get("issues") or []))
    if not x.finished:
        return x
    x.spoke = any(not dm.is_ours(m) and dm.priced(m) for m in msgs)
    try:
        st = dm.analyse(raw, rec)
        x.behaviour, x.hold_flag = st.behaviour, st.hold_flag
    except Exception:  # noqa: BLE001  a label only; an odd payload must not stop the wave
        pass
    keep = (1 - d) ** rounds
    x.result = num(done.get("result"))
    if x.deal:
        x.price, x.day = num(done.get("price")), done.get("days") if isinstance(done.get("days"), int) else None
        if x.result is not None and keep > 0:
            x.surplus = round(x.result / keep, 2)           # the game's own number: right whatever our day reading
        elif x.price is not None:
            x.surplus = worth(raw, dv, x.price, x.day)
            x.result = None if x.surplus is None else round(x.surplus * keep, 1)
        if x.surplus is not None:
            x.decay_lost = round(x.surplus * (1 - keep), 2)
        if dv is not None:
            x.best_day = dv.best
            x.day_cost = round(-dv(x.day), 2) + 0.0         # + 0.0: no "-0.0"
    x.missed = best_missed(raw, dv, x.result or 0.0, d)
    return x


@dataclass
class Wave:
    session: Any
    n: int                           # 1-based, within the session
    duels: list[Duel]
    closed: bool
    name: str = ""

    @property
    def id(self) -> str:
        return f"{self.session}.{self.n}"


def session_order(s: Any) -> tuple:
    """Sessions in game order: numbers numerically, anything else after them."""
    return (0, int(s), "") if str(s).isdigit() else (1, 0, str(s))


def wave_size(duels: list[Duel], sp: dict) -> int:
    """The session's max_concurrent, else how many of our duels started on its first tick (the first wave is full:
    6 for Duels II, 3 for Duels I in the records)."""
    if isinstance(sp.get("max_concurrent"), int) and sp["max_concurrent"] > 0:
        return sp["max_concurrent"]
    starts = [x.start for x in duels if x.start is not None]
    return sum(1 for s in starts if s == min(starts)) if starts else DEFAULT_SIZE


def make_waves(duels: list[Duel], sessions: dict[Any, dict], over: set, size: int | None = None) -> list[Wave]:
    """Our duels cut into waves, per session, in start order. The duel monitor cuts its waves live, on what finished
    between two reviews; offline the start order is what is stable, and a param change reaches the duels that start
    after it. A short last chunk closes only once the session is over (its `duels.finished`, or a later session in
    the records), since the duels still to start would join it."""
    out = []
    numbered = sorted({x.session for x in duels if x.session is not None}, key=session_order)
    for j, s in enumerate(numbered):
        xs = sorted((x for x in duels if x.session == s), key=lambda x: (x.start if x.start is not None else 1 << 30,
                                                                          str(x.id)))
        sp = sessions.get(s) or {}
        k = size or wave_size(xs, sp)
        ended = s in over or j < len(numbered) - 1
        for i in range(0, len(xs), k):
            chunk = xs[i:i + k]
            full = len(chunk) == k or ended
            out.append(Wave(s, i // k + 1, chunk, closed=full and all(x.finished for x in chunk),
                            name=sp.get("name") or f"session {s}"))
    return out


@dataclass
class Book:
    """Everything the loop reads from the records folder."""
    duels: list[Duel]
    waves: list[Wave]
    sessions: dict[Any, dict]


def load(folder: Path = RECORDS, size: int | None = None) -> Book:
    sessions, over = sessions_of(folder)
    records = dm.load_records(folder)
    for r in records:                             # a session the feed no longer holds: as our record saw it, when
        s = r.get("session") or {}                # it names its number (Friday's say "Duels I" for the practice)
        if s.get("session") is not None and s["session"] not in sessions:
            sessions[s["session"]] = s
    duels = [read_duel(r, sessions) for r in records]
    closes = closes_of(folder)
    pts = points_of(folder, {x.id: closes[x.id] for x in duels if x.deal and x.id in closes})
    for x in duels:
        if x.id in pts:
            x.points = pts[x.id]
            keep = (1 - x.decay) ** x.rounds
            x.share = round(x.points / keep, 3) if keep > 0 else None
    return Book(duels, make_waves(duels, sessions, over, size), sessions)


def pick(waves: list[Wave], which: str = "latest") -> Wave | None:
    """`latest`: the newest closed wave; `N`: wave N of the newest session with waves; `S.N`: wave N of session S."""
    if which == "latest":
        closed = [w for w in waves if w.closed]
        return closed[-1] if closed else None
    if "." in which:
        return next((w for w in waves if w.id == which), None)
    if not waves:
        return None
    last = waves[-1].session
    return next((w for w in waves if w.session == last and str(w.n) == which), None)


# ---------------------------------------------------------------------------------------------------- the summary

def p90(xs: list[float]) -> float | None:
    if not xs:
        return None
    s = sorted(xs)
    return s[max(math.ceil(0.9 * len(s)) - 1, 0)]


def latency(duels: list[Duel]) -> dict[str, Any]:
    """Our decisions: how long they took, who made them (a model call, code's rules, or the fallback when the models
    failed or ran out of time) and each model stage's latency."""
    took, stages = [], {}
    model = code = fallbacks = timeouts = holds = 0
    for x in duels:
        for dec in x.decisions:
            if num(dec.get("took_s")) is not None:
                took.append(dec["took_s"])
            meta = (dec.get("move") or {}).get("meta") or {}
            calls = meta.get("calls") or []
            for c in calls:
                if num(c.get("latency_s")) is not None:
                    stages.setdefault(c.get("stage") or "?", []).append(c["latency_s"])
            holds += bool(dec.get("hold"))
            if meta.get("fallback"):
                fallbacks += 1
                timeouts += str(meta["fallback"]).startswith("timeout")
            elif calls:
                model += 1
            else:
                code += 1
    return {"n": len(took), "mean": round(mean(took), 2) if took else None, "p90": p90(took),
            "max": max(took) if took else None, "model": model, "code": code, "fallbacks": fallbacks,
            "timeouts": timeouts, "holds": holds, "stages": {k: round(mean(v), 2) for k, v in stages.items()}}


def observe(duels: list[Duel]) -> dict[str, Any]:
    """The wave in the simulator's terms (deal rate, rounds per deal, share, score per duel) and in primas."""
    fin = [x for x in duels if x.finished]
    deals = [x for x in fin if x.deal]
    known = [x for x in deals if x.points is not None]
    surplus = sum(x.surplus or 0 for x in deals)
    lost = sum(x.decay_lost or 0 for x in deals)
    rate = len(deals) / len(fin) if fin else None
    if known and len(known) == len(deals):
        score, score_est = sum(x.points for x in known) / len(fin), False
    elif known:
        score, score_est = rate * mean(x.points for x in known), True     # the known deals stand for the rest
    else:
        score, score_est = (0.0 if fin and not deals else None), False
    days = [x for x in deals if x.day_cost is not None]
    return {
        "duels": len(fin), "deals": len(deals), "deal_rate": rate,
        "rounds": float(mean(x.rounds for x in deals)) if deals else None,
        "share": mean(x.share for x in known if x.share is not None) if known else None, "share_n": len(known),
        "score": score, "score_est": score_est,
        "result_p": sum(x.result or 0 for x in deals), "surplus_p": surplus, "decay_lost_p": lost,
        "decay_share": lost / surplus if surplus > 0 else None,
        "missed": [x for x in fin if x.missed], "missed_p": sum(x.missed["lost"] for x in fin if x.missed),
        "days_deals": len(days), "best_day_deals": sum(1 for x in days if x.day == x.best_day),
        "day_cost_p": sum(x.day_cost for x in days), "costly_days": [x for x in days if x.day_cost >= DAY_COST_HIGH_P],
        "silent_no_deal": [x for x in fin if not x.spoke and not x.deal],
        "holds_no_deal": [x for x in fin if x.hold_flag and not x.deal],
        "latency": latency(fin),
    }


def as_json(obs: dict[str, Any]) -> dict[str, Any]:
    """`observe`'s numbers, with its lists of duels as their ids."""
    return {k: [x.id for x in v] if isinstance(v, list) and v and isinstance(v[0], Duel) else
            [] if isinstance(v, list) else v for k, v in obs.items()}


# ---------------------------------------------------------------------------------------------------- the params

def module_defaults(src: Path = DUELIST) -> dict[str, Any]:
    """Today's value of every SPEC constant, read from the module's source (a top-level `NAME = <literal>`), so the
    loop needs neither the agent's dependencies nor its import. A module that doesn't exist (policy.py before the
    code policy lands) gives no defaults: those names stay at the simulator's own values."""
    out: dict[str, Any] = {}
    for module in sorted({s.module for s in pm.SPEC.values()}):
        try:
            tree = ast.parse((src / f"{module}.py").read_text())
        except (OSError, SyntaxError):
            continue
        for node in tree.body:
            target = (node.targets[0] if isinstance(node, ast.Assign) and len(node.targets) == 1 else
                      node.target if isinstance(node, ast.AnnAssign) and node.value is not None else None)
            if not isinstance(target, ast.Name) or pm.SPEC.get(target.id, None) is None:
                continue
            if pm.SPEC[target.id].module != module:
                continue
            try:
                value = ast.literal_eval(node.value)
            except ValueError:
                continue
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                out[target.id] = value
    return out


def read_params(path: Path) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    """(the file as JSON, its valid overrides, the errors). A missing file is no overrides; any error means the
    duelist ignores the whole file (`params.Params`), so the overrides are then {}."""
    try:
        raw = path.read_text()
    except FileNotFoundError:
        return {}, {}, []
    except OSError as e:
        return {}, {}, [f"unreadable: {e}"]
    try:
        data = json.loads(raw)
    except ValueError as e:
        return {}, {}, [f"broken JSON: {e}"]
    over, errors = pm.validate(data)
    return (data if isinstance(data, dict) else {}), ({} if errors else over), errors


def effective(defaults: dict[str, Any], over: dict[str, Any]) -> dict[str, Any]:
    """What the duelist plays: the defaults, with the overrides of names it has (as `Params.reload` does)."""
    return {**defaults, **{k: v for k, v in over.items() if k in defaults}}


def cross_errors(eff: dict[str, Any]) -> list[str]:
    return [f"{a} {eff[a]} > {b} {eff[b]}" for a, b in pm.CROSS if a in eff and b in eff and eff[a] > eff[b]]


def sim_policy(eff: dict[str, Any], *, days: bool, code: bool) -> dict[str, Any]:
    """The simulator's policy for the effective params: the live duelist as the Duel Lab models it
    (default_policy() + switch_any, the models' real closing steps end_emp, and the 6190 guards guard_worse +
    mono_end while GUARDS is on), each name in sim.POLICY_KEYS set from `eff`. --policy code: the code step
    (CODE_STEP_SHARE, END_STEP_SHARE) instead of the models'. OPEN_WAIT waits only in days duels."""
    pol = dict(sim.default_policy(), switch_any=True, end_emp=not code)
    for name, key in sim.POLICY_KEYS.items():
        if name in eff:
            pol[key] = eff[name]
    guards = bool(eff.get("GUARDS", 1))
    pol["guard_worse"], pol["mono_end"] = guards, (eff.get("MONO_END_SHARE") if guards else None)
    if code:
        pol["step"] = "code"
        for name, key in (("CODE_STEP_SHARE", "alpha"), ("END_STEP_SHARE", "end_alpha")):
            if name in eff:
                pol[key] = eff[name]
    if not days:
        pol["open_wait"] = 0
    return pol


# ---------------------------------------------------------------------------------------------------- the simulator

H = "H1"                     # the simulator's pie: the best day's (as the Duel Lab scores Duels II)
TARGET = (12, 0.10)          # (duel ticks, decay) the Duel Lab simulated its file for: Duels III and the Final


def predict(pol: dict, T: int, d: float, n: int = N_SIM, seed: int = SEED,
            worlds: dict | None = None) -> tuple[dict[str, dict], dict[str, list]]:
    """Every world's summary for `pol` at this session's ticks and decay, and the raw results (for pairing)."""
    worlds = sim.RW if worlds is None else worlds
    runs = {name: sim.evaluate(pol, P=P, n=n, seed=seed, T=T, d=d, H=H) for name, P in worlds.items()}
    return {name: sim.summary(r) for name, r in runs.items()}, runs


def distance(obs: dict, pred: dict) -> float | None:
    """How far a world's prediction sits from the wave: deal rate and share as they are, rounds over ROUNDS_SCALE.
    A term the wave can't give (no deal, no known pie) drops out."""
    terms = []
    if obs.get("deal_rate") is not None:
        terms.append(obs["deal_rate"] - pred["deal_rate"])
    if obs.get("rounds") is not None:
        terms.append((obs["rounds"] - pred["rounds"]) / ROUNDS_SCALE)
    if obs.get("share") is not None:
        terms.append(obs["share"] - pred["share"])
    return math.sqrt(sum(t * t for t in terms)) if terms else None


def closest(obs: dict, preds: dict[str, dict]) -> tuple[str, dict[str, float | None]]:
    dist = {name: distance(obs, p) for name, p in preds.items()}
    ranked = sorted(preds, key=lambda name: (dist[name] is None, dist[name] or 0.0))
    return ranked[0], dist


def tweaked(eff: dict[str, Any], name: str, op: str, amount: float) -> Any:
    v = eff[name] * amount if op == "x" else eff[name] + amount
    return int(round(v)) if pm.SPEC[name].kind is int else round(v, 4)


def candidate(base_over: dict, defaults: dict, change: dict[str, Any]) -> tuple[dict | None, str]:
    """The params file's overrides with `change` on top, if they pass `params.validate` and the CROSS checks; else
    None and why."""
    over, errors = pm.validate({**base_over, **change})
    if errors:
        return None, "; ".join(errors)
    if bad := cross_errors(effective(defaults, over)):
        return None, "; ".join(bad)
    return over, ""


def search(defaults: dict, base_over: dict, *, world: str, base_runs: list, T: int, d: float, days: bool,
           code: bool, n: int = N_SIM, seed: int = SEED) -> dict[str, Any]:
    """The TWEAKS in `world`, each paired against today's policy (`sim.paired`: mean and 95% CI of tweak - today,
    in duel points per duel). Kept: CI entirely above 0, and valid. The proposal: the best kept tweak per name,
    together when the set also passes the CI test and beats the best single one, else the best single one."""
    eff = effective(defaults, base_over)
    base_pol = sim_policy(eff, days=days, code=code)
    P = sim.RW[world]
    rows = []
    for name, op, amount in TWEAKS:
        row = {"name": name, "op": op, "amount": amount, "from": eff.get(name), "to": None,
               "mean": None, "ci": None, "kept": False, "why": ""}
        rows.append(row)
        if name not in eff:
            row["why"] = "no default in this checkout (its module is missing)"
            continue
        row["to"] = tweaked(eff, name, op, amount)
        over, why = candidate(base_over, defaults, {name: row["to"]})
        if over is None:
            row["why"] = f"invalid: {why}"
            continue
        pol = sim_policy(effective(defaults, over), days=days, code=code)
        if pol == base_pol:
            row["why"] = "not modelled here" + ("" if code else " (code-policy name; the models play)")
            continue
        m, ci = sim.paired(base_runs, sim.evaluate(pol, P=P, n=n, seed=seed, T=T, d=d, H=H))
        row["mean"], row["ci"] = round(m, 4), round(ci, 4)
        row["kept"] = m - ci > 0
        row["why"] = ("CI above 0" if row["kept"] else "worse (CI below 0)" if m + ci < 0 else
                      "no clear effect (CI spans 0)")
        way = "down" if row["to"] < row["from"] else "up"
        if row["kept"] and (name, way) in BLOCKED:
            row["kept"], row["why"] = False, "CI above 0, but blocked: " + CAVEATS.get((name, way), "the sim can't judge it")
    best: dict[str, dict] = {}
    for row in rows:
        if row["kept"] and (row["name"] not in best or row["mean"] > best[row["name"]]["mean"]):
            best[row["name"]] = row
    proposal, combined = {}, None
    if best:
        top = max(best.values(), key=lambda r: r["mean"])
        proposal = {top["name"]: top["to"]}
        if len(best) > 1:
            change = {r["name"]: r["to"] for r in best.values()}
            over, why = candidate(base_over, defaults, change)
            combined = {"params": change, "mean": None, "ci": None, "kept": False, "why": why and f"invalid: {why}"}
            if over is not None:
                pol = sim_policy(effective(defaults, over), days=days, code=code)
                m, ci = sim.paired(base_runs, sim.evaluate(pol, P=P, n=n, seed=seed, T=T, d=d, H=H))
                better = m - ci > 0 and m >= top["mean"]
                combined.update(mean=round(m, 4), ci=round(ci, 4), kept=better, why=(
                    "beats the best single tweak" if better else "not better than the best single tweak"))
                if better:
                    proposal = change
    return {"rows": rows, "combined": combined, "params": proposal}


def caveats(proposal: dict[str, Any], eff: dict[str, Any]) -> list[str]:
    """What the simulator can't see about a proposed change (CAVEATS), for whoever approves it."""
    out = []
    for name, value in proposal.items():
        way = "down" if name in eff and value < eff[name] else "up"
        if text := CAVEATS.get((name, way)):
            out.append(f"{name} {eff.get(name)} → {value}: {text}")
    return out


# ---------------------------------------------------------------------------------------------------- rule notes

def rule_notes(obs: dict, eff: dict[str, Any]) -> list[str]:
    """What the wave itself suggests, for a human to weigh. Never in the proposed JSON: only the simulator's
    supported changes go there."""
    v = lambda k: eff.get(k, "?")  # noqa: E731
    out = []
    if obs["missed"]:
        ids = ", ".join(str(x.id) for x in obs["missed"])
        out.append(f"In-limit offers missed in {len(obs['missed'])} duel(s) ({ids}; ≈{obs['missed_p']:.1f} P): "
                   f"consider ACCEPT_BY (now {v('ACCEPT_BY')}) or SMALL_GAP_P / SMALL_GAP_ROUNDS. The Duel Lab's "
                   "replays found every accept-earlier rule loses overall (intel/duel-lab.md §0 #2): read the "
                   "transcripts first.")
    if (obs["decay_share"] or 0) >= DECAY_SHARE_HIGH or (obs["rounds"] or 0) >= ROUNDS_HIGH:
        out.append(f"Rounds are expensive: {obs['decay_lost_p']:.1f} P of {obs['surplus_p']:.1f} P surplus "
                   f"({(obs['decay_share'] or 0):.0%}) went to decay, {obs['rounds']:.1f} rounds per deal: consider "
                   f"raising MIN_STEP_SHARE (now {v('MIN_STEP_SHARE')}) or MAX_STEP_SHARE (now "
                   f"{v('MAX_STEP_SHARE')}), so fewer, bigger steps close it.")
    lat = obs["latency"]
    if lat["fallbacks"]:
        out.append(f"{lat['fallbacks']} fallback move(s) ({lat['timeouts']} timeouts): the models missed the tick; "
                   "check the strategist's effort and the tick length.")
    if lat["p90"] is not None and lat["p90"] > LATENCY_P90_S:
        out.append(f"Decision p90 {lat['p90']:.1f} s is over {LATENCY_P90_S:.0f} s, the runner's budget at 15 s "
                   "ticks.")
    if obs["silent_no_deal"]:
        out.append(f"{len(obs['silent_no_deal'])} silent rival(s) ended with no deal "
                   f"({', '.join(str(x.id) for x in obs['silent_no_deal'])}): SILENT_KEEP (now {v('SILENT_KEEP')}).")
    if obs["holds_no_deal"]:
        out.append(f"{len(obs['holds_no_deal'])} no-deal(s) sat still with time left "
                   f"({', '.join(str(x.id) for x in obs['holds_no_deal'])}): HOLD_TICKS (now {v('HOLD_TICKS')}).")
    if costly := obs["costly_days"]:
        out.append(f"{len(costly)} deal(s) settled on a day costing us ≥ {DAY_COST_HIGH_P:.0f} P against our best "
                   f"({', '.join(f'{x.id}: {x.day_cost:.1f} P' for x in costly)}): GIVE_COST_P (now "
                   f"{v('GIVE_COST_P')}) and the day rules.")
    return out


# ---------------------------------------------------------------------------------------------------- the report

def f(x: Any, nd: int = 1, dash: str = "—") -> str:
    if x is None:
        return dash
    if isinstance(x, float):
        return f"{x:.{nd}f}"
    return str(x)


def duel_row(x: Duel) -> str:
    out = (f"deal {x.price:g}" + (f" day {x.day}" if x.day is not None else "") if x.deal and x.price is not None
           else x.status or "?")
    day = (f"day {x.day} vs best {x.best_day}: {x.day_cost:.1f} P" if x.day_cost is not None else "—")
    missed = (f"{x.missed['price']:g}" + (f" day {x.missed['day']}" if x.missed.get("day") is not None else "")
              + f" @{x.missed['tick']} ≈{x.missed['value']:.1f} P (−{x.missed['lost']:.1f})" if x.missed else "—")
    return (f"| {x.id} | {x.role} | {x.rival} | {out} | {x.rounds} | {f(x.result)} | {f(x.surplus)} | "
            f"{f(x.share, 2)} | {f(x.points, 3)} | {f(x.decay_lost)} | {day} | {missed} | {x.behaviour or '—'} |")


def sim_row(name: str, s: dict, dist: float | None = None, mark: str = "") -> str:
    est = " (est.)" if s.get("score_est") else ""
    share = f(s.get("share"), 3) + (f" (n {s['share_n']})" if s.get("share_n") is not None else "")
    return (f"| {mark}{name} | {f(s.get('deal_rate'), 2)} | {f(s.get('rounds'), 2)} | {share} | "
            f"{f(s.get('score'), 3)}{est} | {f(dist, 3)} |")


def render(wave: Wave, obs: dict, sess: dict, preds: dict, dist: dict, world: str, found: dict, notes: list[str],
           ctx: dict) -> str:
    ids = ", ".join(str(x.id) for x in wave.duels)
    L = [f"## {stamp()} · {wave.name} wave {wave.n} ({wave.id}) · duels {ids}", f"<!-- wave {wave.id} -->", ""]
    rate = f"{obs['deal_rate']:.0%}" if obs["deal_rate"] is not None else "—"
    lost = f" ({obs['decay_share']:.0%})" if obs["decay_share"] is not None else ""
    L.append(f"**Observed:** {obs['duels']} duels, {obs['deals']} deals ({rate}) · "
             f"{f(obs['rounds'])} rounds per deal · result {obs['result_p']:.1f} of {obs['surplus_p']:.1f} P surplus, "
             f"decay lost {obs['decay_lost_p']:.1f} P{lost} · "
             f"share {f(obs['share'], 3)} (pie known for {obs['share_n']} of {obs['deals']} deals) · "
             f"score/duel {f(obs['score'], 3)}{' (est.)' if obs['score_est'] else ''}")
    if obs["days_deals"]:
        L.append(f"- Days: {obs['best_day_deals']} of {obs['days_deals']} deals on our best day; the settled days cost "
                 f"us {obs['day_cost_p']:.1f} P against our best.")
    L.append(f"- In-limit offers missed: {len(obs['missed'])}"
             + (f" (≈{obs['missed_p']:.1f} P against what we got)" if obs["missed"] else "") + ".")
    lat = obs["latency"]
    stages = ", ".join(f"{k} {v:.1f} s" for k, v in sorted(lat["stages"].items()))
    L.append(f"- Latency: {lat['n']} decisions, took {f(lat['mean'])} s mean, p90 {f(lat['p90'])}, max "
             f"{f(lat['max'])}; {lat['model']} model / {lat['code']} code moves, {lat['fallbacks']} fallbacks "
             f"({lat['timeouts']} timeouts), {lat['holds']} holds" + (f"; stages: {stages}" if stages else "") + ".")
    L += ["", "| duel | role | rival | outcome | rounds | result P | surplus P | share | points | decay lost P | "
              "day (vs best, cost) | best in-limit offer missed | rival |", "|" + "---|" * 13]
    L += [duel_row(x) for x in wave.duels]
    L += ["", f"**Simulator vs observed** (T {ctx['T']}, d {ctx['d']}, n {ctx['n']} per world, policy "
              f"{ctx['policy']}; role-aware worlds, price + day):", "",
          "| | deal rate | rounds/deal | share | score/duel | distance |", "|---|---|---|---|---|---|",
          sim_row("observed (this wave)", obs), sim_row("observed (session so far)", sess)]
    L += [sim_row(name, p, dist[name], "**→** " if name == world else "") for name, p in preds.items()]
    L += ["", f"Closest world: **{world}**. Params played (sim mapping): "
              + ", ".join(f"{k} {v}" for k, v in sorted(ctx["eff"].items()) if k in sim.POLICY_KEYS)
              + (f"; overrides from the params file: {json.dumps(ctx['over'])}" if ctx["over"] else
                 "; no overrides (defaults)") + (f" **(params file ignored: {'; '.join(ctx['errors'])})**"
                                                 if ctx["errors"] else "") + ".", ""]
    L += [f"**Tweaks in {world}** (paired against today's params, Δ score/duel ± 95% CI):", "",
          "| tweak | Δ score/duel | verdict |", "|---|---|---|"]
    for r in found["rows"]:
        what = (f"{r['name']} {r['from']} → {r['to']}" if r["to"] is not None else
                f"{r['name']} {r['op']}{r['amount']}")
        delta = f"{r['mean']:+.4f} ± {r['ci']:.4f}" if r["mean"] is not None else "—"
        L.append(f"| {what} | {delta} | {'**kept**' if r['kept'] else r['why']} |")
    if (c := found["combined"]) is not None:
        delta = f"{c['mean']:+.4f} ± {c['ci']:.4f}" if c["mean"] is not None else "—"
        L.append(f"| together: {json.dumps(c['params'])} | {delta} | {'**kept**' if c['kept'] else c['why']} |")
    L.append("")
    g = ctx.get("gates") or {}
    if g:
        L += [f"**Switch rule** (`tools/duel_gates.py`, session so far): **{g.get('verdict', 'HOLD')}**: {g['reason']}"
              + (f" · evidence {json.dumps(g['evidence'])}" if g.get("evidence") else "")
              + (" · `tools/duel_loop.py switch` applies it" if g.get("verdict") == "SWITCH" else ""), ""]
    if notes:
        L += ["**Rule notes** (from the wave; not in the proposal):"] + [f"- {n}" for n in notes] + [""]
    if found["params"]:
        warn = caveats(found["params"], ctx["eff"])
        L += ["**Proposal:**", "", "```json", json.dumps({"wave": wave.id, "params": found["params"]}), "```", ""]
        L += [f"- Caveat: {c}" for c in warn] + ([""] if warn else [])
        L.append("Approve (on the duelist's machine; it plays from the next tick): "
                 "`python3 tools/duel_loop.py approve --by <name>` (or `--proposal intel/duel-loop.md` after a pull; "
                 "`--only NAME` for part of it). Undo: `python3 tools/duel_loop.py revert --by <name>`.")
    elif ctx.get("off_target"):
        t = ctx["off_target"]
        L += [f"**Proposal:** none for this session: it plays {ctx['T']} ticks at {ctx['d']:.0%} decay, not the "
              f"{t[0]} ticks at {t[1]:.0%} the Duel Lab simulated (Chief 00:50). Duels III starts from "
              "docs/duels3-start.json; proposals count from its first wave."]
    else:
        L += ["**Proposal:** no change proposed (no tweak's CI is entirely above 0)."]
    return "\n".join(L) + "\n"


def prepend(section: str, wave_id: str, path: Path = OUT) -> None:
    """Newest wave on top; a wave run again replaces its own section."""
    body = path.read_text() if path.exists() else OUT_HEADER
    if not body.startswith("# Duel loop"):
        body = OUT_HEADER + "\n" + body
    head, *sections = body.split("\n## ")
    keep = [s for s in sections if f"<!-- wave {wave_id} -->" not in s]
    write_atomic(path, head.rstrip() + "\n\n" + section.rstrip() + "\n" + "".join("\n## " + s for s in keep))


# ---------------------------------------------------------------------------------------------------- the live gates

def gate_duels(records: Path, session: Any) -> list[dict]:
    """The session's closed duels as tools/duel_gates.load reads them (the game's final payload), from `records`."""
    out = []
    for f in sorted(Path(records).glob("duel-*.json")):
        try:
            d = json.loads(f.read_text())
        except (OSError, ValueError):
            continue
        D = d.get("done") or ((d.get("payloads") or [{}])[-1].get("raw") if d.get("payloads") else None)
        if isinstance(D, dict) and D.get("session") == session and D.get("status") in ("deal", "no_deal"):
            out.append(D)
    return sorted(out, key=lambda D: D.get("deadline_tick") or 0)


def gate(records: Path, session: Any, eff: dict[str, Any] | None = None) -> dict[str, Any]:
    """tools/duel_gates.rule on the session so far: {"verdict": HOLD | SWITCH, "reason", "evidence", "diff": {}}."""
    try:
        verdict, reason, ev = dg.rule(gate_duels(records, session))
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as e:
        return {"verdict": "HOLD", "diff": {}, "reason": f"rule not evaluated ({e!r:.80})", "evidence": {}}
    return {"verdict": verdict, "diff": {}, "reason": reason, "evidence": ev}


# ---------------------------------------------------------------------------------------------------- run

def session_params(book: Book, wave: Wave) -> tuple[int, float]:
    sp = book.sessions.get(wave.session) or {}
    T = sp.get("duel_ticks") or 16
    d = num(sp.get("decay")) or (wave.duels[0].decay if wave.duels else 0.08)
    return int(T), float(d)


def run(*, records: Path = RECORDS, which: str = "latest", params_path: Path = pm.PATH, dry: bool = False,
        n: int = N_SIM, seed: int = SEED, policy: str = "llm", out: Path = OUT, proposal_path: Path = PROPOSAL,
        src: Path = DUELIST, size: int | None = None, quiet: bool = False,
        target: tuple[int, float] | None = TARGET) -> dict[str, Any] | None:
    """Steps 1-3 for one wave. Returns the proposal (also written unless `dry`), or None when there is no such
    closed wave."""
    book = load(records, size)
    wave = pick(book.waves, which)
    if wave is None or not wave.closed:
        if not quiet:
            live = wave and sum(1 for x in wave.duels if not x.finished)
            print(f"no closed wave {which}" + (f": wave {wave.id} still has {live} duel(s) live" if wave else ""))
        return None
    obs = observe(wave.duels)
    sess = observe([x for w in book.waves if w.session == wave.session and w.closed for x in w.duels])
    T, d = session_params(book, wave)
    defaults = module_defaults(src)
    _, over, errors = read_params(Path(params_path))
    eff = effective(defaults, over)
    code = policy == "code" and any(pm.SPEC[k].module == "policy" for k in defaults)
    if policy == "code" and not code and not quiet:
        print("warning: --policy code, but agents/duelist/policy.py has no constants here: simulating the models")
    days = any(x.days_duel for x in wave.duels)
    base = sim_policy(eff, days=days, code=code)
    preds, runs = predict(base, T, d, n, seed)
    world, dist = closest(obs, preds)
    found = search(defaults, over, world=world, base_runs=runs[world], T=T, d=d, days=days, code=code, n=n,
                   seed=seed)
    notes = rule_notes(obs, eff)
    gates = gate(records, wave.session, eff)
    off_target = target is not None and (T != target[0] or abs(d - target[1]) > 1e-9)
    if off_target:                                     # Chief 00:50: proposals only at the simulated setting
        found["params"], gates["diff"] = {}, {}
        gates["reason"] = f"{gates['reason']} (not proposed: this session is not at {target[0]} ticks / {target[1]:.0%})"
    ctx = {"T": T, "d": d, "n": n, "policy": "code" if code else "llm", "eff": eff, "over": over, "errors": errors,
           "gates": gates, "off_target": off_target and target}
    section = render(wave, obs, sess, preds, dist, world, found, notes, ctx)
    proposal = {
        "wave": wave.id, "label": f"{wave.name} wave {wave.n}", "made_at": stamp("%Y-%m-%dT%H:%M:%S"),
        "params": found["params"],
        "evidence": {
            "duels": [x.id for x in wave.duels], "T": T, "d": d, "n": n, "seed": seed, "policy": ctx["policy"],
            "observed": as_json(obs), "session_so_far": as_json(sess),
            "missed": {str(x.id): x.missed for x in obs["missed"]},
            "predicted": {k: {**v, "distance": dist[k]} for k, v in preds.items()}, "world": world,
            "base_params": eff, "base_overrides": over, "params_file_errors": errors, "sim_policy": base,
            "tweaks": found["rows"], "combined": found["combined"], "notes": notes, "gates": gates,
            "caveats": caveats(found["params"], eff),
        },
    }
    if not quiet:
        print(section)
    if not dry:
        prepend(section, wave.id, out)
        write_atomic(proposal_path, json.dumps(proposal, indent=1, default=str) + "\n")
        if not quiet:
            print(f"(written: {out}, {proposal_path})")
    return proposal


# ---------------------------------------------------------------------------------------------------- approve, revert

def me() -> str:
    try:
        name = subprocess.run(["git", "-C", str(ROOT), "config", "user.name"], capture_output=True, text=True,
                              timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        name = ""
    return name or os.environ.get("USER", "?")


def load_proposal(path: Path) -> dict[str, Any]:
    """The proposal JSON, or the newest wave's in intel/duel-loop.md (the file that travels by git: run/ doesn't).
    Only the newest section counts: when it proposed no change, an older wave's block is stale, never approved."""
    text = path.read_text()
    if path.suffix == ".md":
        newest = (text.split("\n## ") + [""])[1]
        m = re.search(r"```json\n(.*?)\n```", newest, re.S)
        if not m:
            raise ValueError(f"{path}: the newest wave proposed no change")
        text = m.group(1)
    data = json.loads(text)
    if not isinstance(data, dict) or not isinstance(data.get("params"), dict):
        raise ValueError(f"{path}: not a proposal (no params object)")
    return data


def was(name: str, existing: dict[str, Any], defaults: dict[str, Any]) -> str:
    """A name's value before a change: the file's override, else today's default."""
    return (str(existing[name]) if name in existing else f"default {defaults[name]}" if name in defaults else
            "unset")


def approve(*, proposal_path: Path = PROPOSAL, params_path: Path = pm.PATH, only: list[str] | None = None,
            by: str | None = None, src: Path = DUELIST, force: bool = False) -> int:
    """Merges the proposal into the params file, keeping its other keys. Refuses, writing nothing, on a broken file,
    a value `params.validate` rejects, or a CROSS violation. Writes atomically, with a `_note` (wave, time,
    approver). Returns the exit code."""
    try:
        prop = load_proposal(Path(proposal_path))
    except (OSError, ValueError) as e:
        print(f"refused: can't read the proposal: {e}")
        return 1
    chosen = dict(prop["params"])
    if only:
        unknown = [k for k in only if k not in chosen]
        if unknown:
            print(f"refused: {', '.join(unknown)} not in the proposal for wave {prop.get('wave')} "
                  f"(it proposes {', '.join(chosen) or 'nothing'})")
            return 1
        chosen = {k: chosen[k] for k in only}
    if not chosen:
        print(f"nothing to approve: the proposal for wave {prop.get('wave')} proposes no change")
        return 0
    path = Path(params_path)
    try:
        existing = json.loads(path.read_text()) if path.exists() else {}
    except (OSError, ValueError) as e:
        print(f"refused: {path} is unreadable or broken JSON ({e}); fix it or run revert first")
        return 1
    if not isinstance(existing, dict):
        print(f"refused: {path} is not a JSON object; run revert first")
        return 1
    defaults = module_defaults(src)
    base = prop.get("evidence", {}).get("base_overrides")
    now = {k: v for k, v in existing.items() if not k.startswith("_")}
    if base is not None and base != now:
        print(f"{'warning' if force else 'refused'}: the params file changed since the proposal was made (then "
              f"{json.dumps(base)}, now {json.dumps(now)}); its evidence was against another set (audit S2: a loop "
              f"run elsewhere could lower a value){'' if force else '. Re-run the loop here, or --force'}")
        if not force:
            return 1
    merged = {**existing, **chosen}
    over, errors = pm.validate(merged)
    if not errors:
        errors = cross_errors(effective(defaults, over))
    if errors:
        print("refused, nothing written:\n" + "\n".join(f"  - {e}" for e in errors))
        return 1
    who = by or me()
    merged["_note"] = (f"wave {prop.get('wave')} proposal ({', '.join(f'{k} {v}' for k, v in chosen.items())}), "
                       f"approved by {who} {stamp('%a %H:%M')}")
    write_atomic(path, json.dumps(merged, indent=1) + "\n")
    print(f"approved by {who}: {path}")
    for k, v in chosen.items():
        print(f"  {k}: {was(k, existing, defaults)} → {v}")
    if missing := [k for k in chosen if k not in defaults]:
        print(f"warning: {', '.join(missing)} has no constant in this checkout: the duelist ignores it")
    return 0


def revert(*, params_path: Path = pm.PATH, by: str | None = None, src: Path = DUELIST) -> int:
    """Deletes every override, so the defaults play from the next tick; leaves a `_note` saying who and when. A
    broken file is replaced too (the duelist was ignoring it)."""
    path = Path(params_path)
    try:
        existing = json.loads(path.read_text()) if path.exists() else {}
    except (OSError, ValueError):
        existing = None
    over = {k: v for k, v in existing.items() if not k.startswith("_")} if isinstance(existing, dict) else {}
    if isinstance(existing, dict) and not over:
        print(f"nothing to revert: no overrides in {path}; the defaults play")
        return 0
    who = by or me()
    write_atomic(path, json.dumps({"_note": f"reverted to defaults by {who} {stamp('%a %H:%M')}"}, indent=1) + "\n")
    defaults = module_defaults(src)
    print(f"reverted by {who}: {path}" + ("" if isinstance(existing, dict) else " (it was broken or not an object)"))
    for k, v in over.items():
        print(f"  {k}: {v} → {was(k, {}, defaults)}")
    return 0


# ---------------------------------------------------------------------------------------------------- watch

def watch_once(state_path: Path = STATE, **kw: Any) -> str | None:
    """One look: when the newest closed wave isn't the one last handled, steps 1-3 on it and one line back."""
    try:
        state = json.loads(Path(state_path).read_text())
    except (OSError, ValueError):
        state = {}
    book = load(kw.get("records", RECORDS), kw.get("size"))
    wave = pick(book.waves, "latest")
    if wave is None or wave.id == state.get("last_wave"):
        return None
    prop = run(**kw, quiet=True)
    if prop is None:
        return None
    ev = prop["evidence"]
    obs = ev["observed"]
    change = (", ".join(f"{k} {ev['base_params'].get(k, '?')} → {v}" for k, v in prop["params"].items())
              or "no change proposed")
    line = (f"{stamp('%H:%M')} wave {wave.id} ({obs['duels']} duels, {obs['deals']} deals, "
            f"{obs['rounds'] or 0:.1f} rounds/deal): closest world {ev['world']}; {change}")
    write_atomic(Path(state_path), json.dumps({"last_wave": wave.id, "at": stamp("%Y-%m-%dT%H:%M:%S"),
                                               "line": line}, indent=1) + "\n")
    return line


def watch(every: float, **kw: Any) -> None:
    while True:
        try:
            if line := watch_once(**kw):
                print(line, flush=True)
        except KeyboardInterrupt:
            raise
        except Exception as e:  # noqa: BLE001  keep watching through a bad record
            print(f"{stamp('%H:%M')} duel loop error: {e!r}"[:300], flush=True)
        time.sleep(every)


# ---------------------------------------------------------------------------------------------------- sets

SWITCH_STATE, SWITCH_OFF = ROOT / "run" / "duel_switch_state.json", ROOT / "run" / "duel_switch.off"


def use(name: str, *, sets_path: Path = pm.SETS, params_path: Path = pm.PATH, by: str | None = None,
        src: Path = DUELIST, why: str = "") -> int:
    """Writes the approved set `name` as the WHOLE params file (every set lists the same keys), validated and
    cross-checked, atomically, with `_set` and a `_note`. Refuses, writing nothing, on any error."""
    sets, _, _, errors = pm.load_sets(sets_path)
    if errors:
        print("refused: the sets file has errors:\n" + "\n".join(f"  - {e}" for e in errors))
        return 1
    if name not in sets:
        print(f"refused: no set {name!r} in {sets_path} (sets: {', '.join(sets)})")
        return 1
    if bad := cross_errors(effective(module_defaults(src), sets[name])):
        print("refused: " + "; ".join(bad))
        return 1
    path = Path(params_path)
    try:
        before = json.loads(path.read_text()) if path.exists() else {}
    except (OSError, ValueError):
        before = {}
    who = by or me()
    data = {"_set": name, "_note": f"set {name} from {Path(sets_path).name}, by {who} {stamp('%a %H:%M')}"
                                   + (f" ({why})" if why else ""), **sets[name]}
    write_atomic(path, json.dumps(data, indent=1) + "\n")
    print(f"set {name} written by {who}: {path} (was {before.get('_set') or ('custom' if before else 'no file')})")
    for k, v in sets[name].items():
        print(f"  {k}: {before.get(k, 'default')} → {v}")
    return 0


def switch_once(*, records: Path = RECORDS, sets_path: Path = pm.SETS, params_path: Path = pm.PATH,
                state_path: Path = SWITCH_STATE, off: Path = SWITCH_OFF, dry: bool = False,
                target: tuple[int, float] | None = TARGET, size: int | None = None, src: Path = DUELIST,
                log: Path = OUT) -> str | None:
    """One look, on the duelist's machine: on a newly closed wave of a session at `target`, the Duel Lab's rule on the
    session so far; when it says SWITCH and the params file plays an approved set with a fallback, that fallback is
    written whole (`use`), once per set, never back. A line when something happened, else None."""
    try:
        state = json.loads(Path(state_path).read_text())
    except (OSError, ValueError):
        state = {}
    book = load(records, size)
    wave = pick(book.waves, "latest")
    if wave is None or not wave.closed or wave.id == state.get("last_wave"):
        return None
    T, d = session_params(book, wave)
    state["last_wave"] = wave.id
    write_atomic(Path(state_path), json.dumps(state, indent=1) + "\n")
    if target is not None and (T != target[0] or abs(d - target[1]) > 1e-9):
        return None
    g = gate(records, wave.session)
    if g["verdict"] != "SWITCH":
        return f"{stamp('%H:%M')} wave {wave.id}: switch rule HOLD ({g['reason']})"
    try:
        now = json.loads(Path(params_path).read_text()).get("_set")
    except (OSError, ValueError, AttributeError):
        now = None
    _, _, fallback, errors = pm.load_sets(sets_path)
    if errors or now not in fallback:
        return (f"{stamp('%H:%M')} wave {wave.id}: switch rule SWITCH, but the params file plays "
                f"{now or 'no approved set'}: nothing written (a human decides)")
    if now in state.get("switched_from", []):
        return None                                   # once per set: never again, never back
    new = fallback[now]
    if dry or Path(off).exists():
        return f"{stamp('%H:%M')} wave {wave.id}: switch rule SWITCH {now} → {new} NOT applied ({'--dry' if dry else off})"
    if use(new, sets_path=sets_path, params_path=params_path, by="switch rule", src=src,
           why=f"wave {wave.id}: {g['reason']}") != 0:
        return f"{stamp('%H:%M')} wave {wave.id}: switch {now} → {new} refused (see above)"
    state.setdefault("switched_from", []).append(now)
    write_atomic(Path(state_path), json.dumps(state, indent=1) + "\n")
    line = f"{stamp('%H:%M')} wave {wave.id}: SWITCHED {now} → {new} ({g['reason']}; {json.dumps(g['evidence'])})"
    prepend(f"## Switch at wave {wave.id} <!-- wave switch-{wave.id} -->\n\n{line}\n", f"switch-{wave.id}", log)
    return line


def switch(every: float, **kw: Any) -> None:
    while True:
        try:
            if line := switch_once(**kw):
                print(line, flush=True)
        except KeyboardInterrupt:
            raise
        except Exception as e:  # noqa: BLE001
            print(f"{stamp('%H:%M')} switch error: {e!r}"[:300], flush=True)
        time.sleep(every)


# ---------------------------------------------------------------------------------------------------- main

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("run", "watch"):
        p = sub.add_parser(name)
        p.add_argument("--records", type=Path, default=RECORDS, help="the duel records folder (docs/duels)")
        p.add_argument("--params", type=Path, default=pm.PATH, help="the params file (run/duel_params.json)")
        p.add_argument("--n", type=int, default=N_SIM, help=f"simulated duels per world and tweak ({N_SIM})")
        p.add_argument("--seed", type=int, default=SEED)
        p.add_argument("--policy", choices=("llm", "code"), default="llm",
                       help="what plays our moves: the models (default) or policy.py's code policy")
        p.add_argument("--size", type=int, help="wave size (default: the session's max_concurrent)")
        if name == "run":
            p.add_argument("--wave", default="latest", help="latest (default), N (of the newest session) or S.N")
            p.add_argument("--dry", action="store_true", help="print only; write nothing")
        else:
            p.add_argument("--every", type=float, default=60.0, help="seconds between looks (60)")
            p.add_argument("--state", type=Path, default=STATE)
    p = sub.add_parser("approve")
    p.add_argument("--proposal", type=Path, default=PROPOSAL, help="the proposal (.json, or intel/duel-loop.md)")
    p.add_argument("--params", type=Path, default=pm.PATH)
    p.add_argument("--only", help="comma-separated names: approve only these")
    p.add_argument("--by", help="who approves (default: git user.name)")
    p.add_argument("--force", action="store_true", help="approve although the params file changed since the run")
    p = sub.add_parser("revert")
    p.add_argument("--params", type=Path, default=pm.PATH)
    p.add_argument("--by")
    p = sub.add_parser("use", help="write one approved set (docs/duel_sets.json) as the whole params file")
    p.add_argument("set")
    p.add_argument("--sets", type=Path, default=pm.SETS)
    p.add_argument("--params", type=Path, default=pm.PATH)
    p.add_argument("--by")
    p = sub.add_parser("switch", help="the Duel Lab's one-way switch rule, applied on the duelist's machine")
    p.add_argument("--records", type=Path, default=RECORDS)
    p.add_argument("--sets", type=Path, default=pm.SETS)
    p.add_argument("--params", type=Path, default=pm.PATH)
    p.add_argument("--every", type=float, default=60.0)
    p.add_argument("--dry", action="store_true", help="report, never write")
    a = ap.parse_args(argv)
    if a.cmd == "use":
        return use(a.set, sets_path=a.sets, params_path=a.params, by=a.by)
    if a.cmd == "switch":
        switch(a.every, records=a.records, sets_path=a.sets, params_path=a.params, dry=a.dry)
        return 0
    if a.cmd == "approve":
        only = [s.strip() for s in a.only.split(",") if s.strip()] if a.only else None
        return approve(proposal_path=a.proposal, params_path=a.params, only=only, by=a.by, force=a.force)
    if a.cmd == "revert":
        return revert(params_path=a.params, by=a.by)
    kw = dict(records=a.records, params_path=a.params, n=a.n, seed=a.seed, policy=a.policy, size=a.size)
    if a.cmd == "run":
        return 0 if run(which=a.wave, dry=a.dry, **kw) is not None else 1
    watch(a.every, state_path=a.state, **kw)
    return 0


if __name__ == "__main__":
    sys.exit(main())
