"""Duel monitor: read-only flags on our live duels, a review after each wave, and a watch on Aleks's duelist tests.

    source .env && python3 tools/duel_monitor.py --once            # one evaluation now
    source .env && python3 -u tools/duel_monitor.py --every 15     # loop: once per server tick, ~15 s into it
    python3 tools/duel_monitor.py --replay docs/duels [--write]    # offline, on recorded duels (no key, no network)

Live flags (each with a severity and one line): an in-limit rival offer standing with <= 2 ticks left (critical, duel
181); a deal closed outside our limit (critical); our side silent >= 4 ticks after a rival offer, or never opened
(high: the duelist may be down); both sides still >= 3 ticks with >= 3 left (medium: hold deadlock, duels 103/104); no
live duel while a scored session is running (high); a priced message refused with `missing_days` (high, read from
Aleks's records in docs/duels/ when they are on this machine). Critical and high go to Lucas and Dani through
tools/notify.py (deduped per duel and flag); everything is printed.

After each wave of our duels it prepends a section to intel/duel-review.md (newest first). The result model:
result = our surplus x (1 - decay)^rounds, rounds = min(our priced offers, theirs).

When the latest commit touching agents/duelist/, engine/ or tests/test_duelist.py by someone else changes, it runs
Aleks's tests and notifies on failure.

GET only (clock, schedule, feed, leaderboard, duels), at most one request a second. It never writes to the game,
never prints a key, never commits. Its own state lives in run/duel_monitor_state.json (gitignored).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "intel" / "duel-review.md"
STATE = ROOT / "run" / "duel_monitor_state.json"
RECORDS = ROOT / "docs" / "duels"
WATCH_PATHS = ("agents/duelist", "engine", "tests/test_duelist.py")
REVIEW_HEADER = (
    "# Duel review\n\n"
    "_Written by `tools/duel_monitor.py` after each wave of our duels, newest first. Advisory for Aleks (the duelist is "
    "his). Result = our surplus × (1 − decay)^rounds, rounds = min(our priced offers, theirs); \"spoke\" = the rival "
    "sent at least one price._\n")

CRITICAL, HIGH, MEDIUM = "critical", "high", "medium"
PRIORITY = {CRITICAL: 5, HIGH: 4, MEDIUM: 3}
TAGS = {CRITICAL: ["rotating_light", "crossed_swords"], HIGH: ["warning", "crossed_swords"], MEDIUM: ["crossed_swords"]}

# Thresholds, as the plan states them (intel/saturday-plan.md §4D).
ACCEPT_TICKS_LEFT = 2       # an in-limit standing offer with <= this many ticks left (including the current) must go
SILENT_TICKS = 4            # our side silent this long after a rival MOVE (a changed offer, not a repeat)
STANDBY = ("Only if Aleks confirms his duelist process is dead (never two duelists on the team key): start the cold "
           "standby on Lucas's Mac, `uv run python -m agents.duelist run`.")
OPEN_TICKS = 3              # no message from us this many ticks into a duel
HOLD_TICKS, HOLD_LEFT = 3, 3
NO_LIVE_TICKS = 2           # consecutive evaluated ticks without a live duel in a running session
# Duelist tests that go red from Saturday's records landing in docs/duels (data, not code): printed, never paged.
KNOWN_DATA_FAILURES = {"test_review_predicts_each_deals_result_from_our_reading"}

try:  # the notifier is another agent's file; without it, alerts are printed only
    sys.path.insert(0, str(ROOT))
    from tools.notify import notify as _notify
except Exception:  # noqa: BLE001
    _notify = None


def stamp() -> str:
    return time.strftime("%H:%M")


def emit(kind: str, msg: str) -> None:
    print(f"{stamp()} {kind}: {msg}", flush=True)


# ---------------------------------------------------------------------------------------------------- duel arithmetic

def sign(role: str | None) -> int:
    """+1 for a seller (a higher price is better for us), -1 for a buyer."""
    return 1 if str(role or "").lower().startswith("sell") else -1


def surplus(raw: dict, price: float | None) -> float | None:
    """Our surplus at `price`: price - cost for a seller, value - price for a buyer."""
    limit = raw.get("your_limit")
    if price is None or limit is None:
        return None
    return sign(raw.get("role")) * (price - limit)


def ticks_left(raw: dict, tick: int | None) -> int | None:
    """Ticks we can still move on, the current one included (1: the last), as Aleks's adapter and tools/arbiter.py
    count them: the payload's ticks_left, else deadline_tick - tick (the duel closes ON its deadline tick)."""
    left = raw.get("ticks_left", raw.get("remaining_ticks"))
    if isinstance(left, (int, float)) and not isinstance(left, bool):
        return max(int(left), 0)
    d = raw.get("deadline_tick", raw.get("deadline"))
    if not isinstance(d, (int, float)) or tick is None:
        return None
    return int(d) - int(tick)


def decay_of(raw: dict, default: float = 0.06) -> float:
    d = raw.get("decay_per_round", raw.get("decay"))
    return float(d) if isinstance(d, (int, float)) else default


def is_ours(m: dict) -> bool:
    return str(m.get("from", "")).lower() in ("you", "me", "us", "self")


def priced(m: dict) -> bool:
    return isinstance(m.get("price"), (int, float))


def messages(raw: dict) -> list[dict]:
    return [m for m in raw.get("messages") or [] if isinstance(m, dict)]


def offer_price(o: Any) -> float | None:
    if isinstance(o, dict):
        o = o.get("price")
    return float(o) if isinstance(o, (int, float)) and not isinstance(o, bool) else None


def move_ticks(msgs: list[dict]) -> list[int]:
    """Ticks at which either side changed its price, from the tick both sides have priced (repeating a price is not a
    move). Empty unless both sides have sent a price."""
    last: dict[bool, Any] = {True: None, False: None}
    first: dict[bool, int | None] = {True: None, False: None}
    out = []
    for m in msgs:
        if not priced(m) or not isinstance(m.get("tick"), int):
            continue
        side = is_ours(m)
        if first[side] is None:
            first[side] = m["tick"]
        if m["price"] != last[side]:
            last[side] = m["price"]
            out.append(m["tick"])
    if first[True] is None or first[False] is None:
        return []
    both = max(first[True], first[False])
    return [t for t in out if t >= both]


def is_live(raw: dict) -> bool:
    return str(raw.get("status", "live")).lower() == "live"


def rid(raw: dict) -> Any:
    return raw.get("duel", raw.get("id", raw.get("duel_id")))


# ---------------------------------------------------------------------------------------------------- flags

@dataclass
class Flag:
    duel: Any                 # a duel id, or "session:<name>" / "tests:<sha>"
    kind: str
    severity: str
    tick: int | None
    text: str

    @property
    def key(self) -> str:
        return f"{self.duel}|{self.kind}"

    def line(self) -> str:
        where = f"duel {self.duel}" if not str(self.duel).startswith(("session:", "tests:")) else str(self.duel)
        return f"[{self.severity.upper()}] {where} · {self.kind} · tick {self.tick}: {self.text}"


def live_flags(raw: dict, tick: int, *, first_seen: int | None = None, duel_ticks: int | None = None,
               errors: list[dict] | None = None, accepted: bool = False) -> list[Flag]:
    """Flags for one live duel as the game shows it at `tick`. `accepted`: Aleks's record shows an accept sent this
    tick or the last (it settles next tick, and the payload may not show it yet)."""
    if not is_live(raw):
        return []
    did, role, limit = rid(raw), raw.get("role"), raw.get("your_limit")
    left = ticks_left(raw, tick)
    msgs = messages(raw)
    ours = [m for m in msgs if is_ours(m) and priced(m)]
    theirs = [m for m in msgs if not is_ours(m) and priced(m)]
    rival = raw.get("rival") or "the rival"
    out: list[Flag] = []

    their = offer_price(raw.get("rival_offer"))
    s = surplus(raw, their)
    if (their is not None and s is not None and s > 0 and left is not None and left <= ACCEPT_TICKS_LEFT
            and not accepted):
        mine = offer_price(raw.get("your_offer"))
        out.append(Flag(did, "in_limit_not_accepted", CRITICAL, tick,
                        f"{rival}'s {their:g} stands inside our limit {limit} ({role}, +{s:g} P) with {left} tick(s) "
                        f"left and we haven't accepted (we're at {mine if mine is None else f'{mine:g}'}). "
                        f"Accept it now or it ends at 0."))

    # Silence after a rival MOVE. Since the rounds fix our duelist holds by sending nothing, so a rival repeating its
    # price every tick (278) gets no answer by design; a changed offer is what it decides on at once.
    last_ours = max((i for i, m in enumerate(msgs) if is_ours(m)), default=-1)
    seen = [m for i, m in enumerate(msgs) if i <= last_ours and not is_ours(m) and priced(m)]
    prev = (seen[-1]["price"], seen[-1].get("days")) if seen else None
    moves = []
    for i, m in enumerate(msgs):
        if i > last_ours and not is_ours(m) and priced(m) and (m["price"], m.get("days")) != prev:
            moves.append(m)
            prev = (m["price"], m.get("days"))
    if moves and isinstance(moves[0].get("tick"), int) and tick - moves[0]["tick"] >= SILENT_TICKS:
        t0 = moves[0]["tick"]
        out.append(Flag(did, "we_are_silent", HIGH, tick,
                        f"{rival} moved to {moves[-1]['price']:g} at tick {t0} and we haven't sent anything for "
                        f"{tick - t0} ticks ({left} left): the duelist may be down. {STANDBY}"))

    if not any(is_ours(m) for m in msgs):
        # The duel started at deadline - duel_ticks, or when we first saw it, whichever is later.
        starts = [first_seen]
        if duel_ticks and isinstance(raw.get("deadline_tick"), int):
            starts.append(raw["deadline_tick"] - duel_ticks)
        starts = [s_ for s_ in starts if s_ is not None]
        if starts and tick - max(starts) >= OPEN_TICKS:
            out.append(Flag(did, "never_opened", HIGH, tick,
                            f"we haven't sent a single message {tick - max(starts)} ticks into the duel ({left} left): "
                            f"the duelist may be down."))

    moves = move_ticks(msgs)
    if moves and left is not None and left >= HOLD_LEFT and tick - moves[-1] >= HOLD_TICKS:
        out.append(Flag(did, "hold_deadlock", MEDIUM, tick,
                        f"both sides still for {tick - moves[-1]} ticks (us {ours[-1]['price']:g}, {rival} "
                        f"{theirs[-1]['price']:g}, limit {limit}) with {left} left: force a move."))

    refused = [e for e in errors or [] if str(e.get("code", "")).lower() == "missing_days"]
    if refused:
        e = refused[-1]
        out.append(Flag(did, "missing_days", HIGH, tick,
                        f"a priced message was refused for missing `days` at tick {e.get('tick')} "
                        f"({len(refused)} so far): every priced message must carry days 0-10."))
    return out


def closed_flags(raw: dict) -> list[Flag]:
    """Flags for a finished duel: a deal outside our limit."""
    status = str(raw.get("status", "")).lower()
    price = offer_price(raw.get("price"))
    s = surplus(raw, price)
    if status == "deal" and s is not None and s < 0:
        return [Flag(rid(raw), "deal_outside_limit", CRITICAL, raw.get("deadline_tick"),
                     f"closed at {price:g} against our limit {raw.get('your_limit')} ({raw.get('role')}): "
                     f"{s:g} P. A guard failed: stop and check the duelist.")]
    return []


# ---------------------------------------------------------------------------------------------------- replay

def snapshots(rec: dict) -> list[tuple[int, dict]]:
    return [(p["tick"], p["raw"]) for p in rec.get("payloads") or [] if isinstance(p.get("tick"), int) and p.get("raw")]


def replay_record(rec: dict) -> list[Flag]:
    """Every flag the live monitor would have raised on this recorded duel, tick by tick (not deduped)."""
    snaps = snapshots(rec)
    final = rec.get("done") or {}
    if not snaps:
        return closed_flags(final) if final else []
    deadline = snaps[-1][1].get("deadline_tick")
    last_seen = rec.get("last_seen_tick")
    end = last_seen - 1 if isinstance(last_seen, int) else snaps[-1][0]   # it was live until it left the list
    if isinstance(deadline, int):
        end = min(end, deadline - 1)
    errors = rec.get("errors") or []
    first = snaps[0][0]
    out: list[Flag] = []
    for t in range(first, end + 1):
        state = [raw for (tk, raw) in snaps if tk <= t][-1]
        out += live_flags(state, t, first_seen=first, errors=[e for e in errors if (e.get("tick") or 0) <= t])
    if final:
        out += closed_flags(final)
    return out


def load_records(folder: Path) -> list[dict]:
    recs = []
    for p in folder.glob("duel-*.json"):
        try:
            recs.append(json.loads(p.read_text()))
        except (json.JSONDecodeError, OSError):
            continue
    return sorted(recs, key=lambda r: int(r.get("duel")) if str(r.get("duel")).isdigit() else 0)


def first_per_kind(flags: list[Flag]) -> list[Flag]:
    seen, out = set(), []
    for f in flags:
        if f.key not in seen:
            seen.add(f.key)
            out.append(f)
    return out


# ---------------------------------------------------------------------------------------------------- review

@dataclass
class DuelStats:
    duel: Any
    rival: str
    role: str
    limit: Any
    status: str
    price: float | None
    surplus: float | None
    result: float
    rounds: int
    decay: float
    spoke: bool                     # the rival sent at least one price
    behaviour: str
    rival_move: float               # how far the rival moved toward us, P
    our_move: float                 # how far we moved toward them, P
    missed: float | None            # value of the best in-limit rival offer we never accepted, no deal
    passed_over: float              # deals: value lost by not taking a better earlier rival offer
    latencies: list[int] = field(default_factory=list)   # ticks from a rival offer to our next message
    unanswered: int = 0
    decision_s: list[float] = field(default_factory=list)
    hold: int = 0                   # longest stretch (ticks) both sides sat still
    hold_flag: bool = False         # the live hold-deadlock flag would have fired


def analyse(raw: dict, rec: dict | None = None) -> DuelStats:
    msgs = messages(raw)
    role, d = raw.get("role") or "?", decay_of(raw)
    s_ = sign(role)
    ours = [m for m in msgs if is_ours(m) and priced(m)]
    theirs = [m for m in msgs if not is_ours(m) and priced(m)]
    status = str(raw.get("status", "")).lower()
    price = offer_price(raw.get("price"))
    sp = surplus(raw, price) if status == "deal" else None
    rounds = raw.get("rounds") if isinstance(raw.get("rounds"), int) else min(len(ours), len(theirs))
    result = raw.get("result")
    if not isinstance(result, (int, float)):
        result = sp * (1 - d) ** rounds if sp is not None else 0.0

    best_offer, ours_before, theirs_upto = None, 0, 0     # the best in-limit rival offer, valued if accepted then
    for m in msgs:
        if not priced(m):
            continue
        if is_ours(m):
            ours_before += 1
            continue
        theirs_upto += 1
        v = surplus(raw, m["price"])
        if v is not None and v > 0:
            val = v * (1 - d) ** min(ours_before, theirs_upto)
            best_offer = val if best_offer is None else max(best_offer, val)
    missed = best_offer if status != "deal" and best_offer is not None else None
    passed = max(0.0, (best_offer or 0) - result) if status == "deal" else 0.0

    lat, unanswered = [], 0
    for i, m in enumerate(msgs):
        if is_ours(m) or not priced(m) or not isinstance(m.get("tick"), int):
            continue
        nxt = next((x for x in msgs[i + 1:] if is_ours(x)), None)
        if nxt is not None and isinstance(nxt.get("tick"), int):
            lat.append(nxt["tick"] - m["tick"])
        elif status != "deal":
            unanswered += 1

    rival_move = s_ * (theirs[-1]["price"] - theirs[0]["price"]) if len(theirs) > 1 else 0.0
    our_move = -s_ * (ours[-1]["price"] - ours[0]["price"]) if len(ours) > 1 else 0.0
    if not theirs:
        behaviour = "accept-only (took our opener)" if status == "deal" else "silent"
    elif rival_move > 0:
        behaviour = "conceder"
    elif rival_move == 0:
        behaviour = "holder (never moved)"
    else:
        behaviour = "hardener (moved away)"

    # Holds: the longest stretch both sides sat still, and whether the live flag would have fired in one (still for
    # HOLD_TICKS with >= HOLD_LEFT ticks left). A no-deal is live until deadline - 1.
    hold, hold_flag = 0, False
    moves, end = move_ticks(msgs), raw.get("deadline_tick")
    if moves and isinstance(end, int):
        stop = end if status != "deal" else max(m["tick"] for m in msgs if isinstance(m.get("tick"), int)) + 1
        marks = sorted(set(moves)) + [stop]
        for a, b in zip(marks, marks[1:]):
            hold = max(hold, b - 1 - a)
            hold_flag = hold_flag or a + HOLD_TICKS <= min(b - 1, end - HOLD_LEFT)

    took = [x["took_s"] for x in (rec or {}).get("decisions") or [] if isinstance(x.get("took_s"), (int, float))]
    return DuelStats(duel=rid(raw), rival=str(raw.get("rival") or "?"), role=role, limit=raw.get("your_limit"),
                     status=status, price=price, surplus=sp, result=float(result), rounds=rounds, decay=d,
                     spoke=bool(theirs), behaviour=behaviour, rival_move=rival_move, our_move=our_move,
                     missed=missed, passed_over=passed, latencies=lat, unanswered=unanswered, decision_s=took,
                     hold=hold, hold_flag=hold_flag)


def summarise(stats: list[DuelStats]) -> dict[str, Any]:
    fin = [x for x in stats if x.status not in ("", "live")]
    deals = [x for x in fin if x.status == "deal"]
    spoke = [x for x in fin if x.spoke]
    engaged = [x for x in fin if x.spoke or x.status == "deal"]
    surplus_sum = sum(x.surplus or 0 for x in deals)
    result_sum = sum(x.result for x in deals)
    lat = [t for x in fin for t in x.latencies]
    took = [t for x in fin for t in x.decision_s]
    return {
        "finished": len(fin), "deals": len(deals),
        "spoke": len(spoke), "spoke_deals": sum(1 for x in spoke if x.status == "deal"),
        "engaged": len(engaged), "engaged_deals": sum(1 for x in engaged if x.status == "deal"),
        "silent": len(fin) - len(spoke), "accept_only": sum(1 for x in fin if not x.spoke and x.status == "deal"),
        "missed": [x for x in fin if x.missed is not None],
        "passed_over": [x for x in deals if x.passed_over >= 0.5],
        "holds": [x for x in fin if x.hold_flag and x.status != "deal"],
        "outside": [x for x in deals if (x.surplus or 0) < 0],
        "mean_rounds": sum(x.rounds for x in deals) / len(deals) if deals else None,
        "surplus": surplus_sum, "result": result_sum,
        "decay_lost": surplus_sum - result_sum,
        "decay_share": (surplus_sum - result_sum) / surplus_sum if surplus_sum > 0 else None,
        "lat_mean": sum(lat) / len(lat) if lat else None, "lat_max": max(lat) if lat else None,
        "lat_same": sum(1 for t in lat if t == 0), "lat_n": len(lat),
        "unanswered": sum(x.unanswered for x in fin),
        "took_mean": sum(took) / len(took) if took else None, "took_max": max(took) if took else None,
        "our_move": sum(x.our_move for x in fin), "rival_move": sum(x.rival_move for x in fin),
        "fin": fin, "deal_list": deals,
    }


def pct(a: float, b: float) -> str:
    return f"{100 * a / b:.0f}%" if b else "—"


def suggestions(sm: dict[str, Any]) -> list[str]:
    """1-3 concrete parameter suggestions for Aleks, most urgent first (the §4D fix order)."""
    out = []
    if sm["outside"]:
        out.append(f"Guard: {len(sm['outside'])} deal(s) closed outside our limit "
                   f"({', '.join(str(x.duel) for x in sm['outside'])}): block any accept/offer past the limit in code.")
    if sm["missed"]:
        lost = sum(x.missed for x in sm["missed"])
        out.append(f"Accept earlier: {len(sm['missed'])} deal(s) lost with the rival's offer inside our limit "
                   f"({', '.join(str(x.duel) for x in sm['missed'])}; ≈{lost:.1f} P after decay). In code, accept any "
                   f"in-limit standing offer at ticks_left ≤ {ACCEPT_TICKS_LEFT}.")
    if sm["holds"]:
        longest = max(x.hold for x in sm["holds"])
        out.append(f"Break holds: {len(sm['holds'])} no-deal duel(s) sat still up to {longest} ticks with time left "
                   f"({', '.join(str(x.duel) for x in sm['holds'])}). After {HOLD_TICKS} still ticks with ≥ {HOLD_LEFT} "
                   f"left, force a move (a concession step, or send their own price).")
    if sm["decay_share"] is not None and sm["decay_share"] > 0.10:
        out.append(f"Close in fewer exchanges: {sm['decay_lost']:.1f} P ({sm['decay_share']:.0%}) of deal value went to "
                   f"decay over {sm['mean_rounds']:.1f} rounds per deal. Accept when the gap to our last offer ≤ "
                   f"max(2 P, 2d/(1−d) × our surplus).")
    silent_lost = sm["silent"] - sm["accept_only"]
    if silent_lost and sm["accept_only"]:
        out.append(f"Silent rivals: {silent_lost} no-deal(s) with a silent rival while {sm['accept_only']} silent "
                   f"rival(s) took our opener: concede on a code schedule toward a floor (keep ≥ 30% of anchor-to-limit).")
    if sm["lat_mean"] is not None and sm["lat_mean"] >= 1:
        out.append(f"Answer faster: {sm['lat_mean']:.1f} ticks on average from a rival offer to our reply.")
    if sm["passed_over"] and len(out) < 3:
        lost = sum(x.passed_over for x in sm["passed_over"])
        out.append(f"Decay-aware accept: {len(sm['passed_over'])} deal(s) closed below an earlier in-limit rival offer "
                   f"(≈{lost:.1f} P).")
    return out[:3] or ["Nothing to change on this evidence."]


def behaviour_lines(fin: list[DuelStats]) -> list[str]:
    groups: dict[str, list[DuelStats]] = {}
    for x in fin:
        groups.setdefault(x.behaviour, []).append(x)
    rows = sorted(groups.items(), key=lambda kv: -sum(x.result for x in kv[1]) / len(kv[1]))
    out = []
    for name, xs in rows:
        deals = sum(1 for x in xs if x.status == "deal")
        mv = [x.rival_move for x in xs if x.spoke]
        extra = f", rival moved {sum(mv) / len(mv):.1f} P per duel" if mv else ""
        out.append(f"{name}: {len(xs)} duel(s), {deals} deal(s), mean result {sum(x.result for x in xs) / len(xs):.1f} P"
                   f"{extra}")
    return out


def render_block(sm: dict[str, Any], label: str) -> list[str]:
    fin = sm["fin"]
    L = [f"**{label}:** {sm['deals']} deals / {sm['finished']} finished ({pct(sm['deals'], sm['finished'])})"]
    L.append(f"- Rival engaged: spoke in {sm['spoke']} → {sm['spoke_deals']} deals ({pct(sm['spoke_deals'], sm['spoke'])}); "
             f"spoke or accepted {sm['engaged']} → {sm['engaged_deals']} ({pct(sm['engaged_deals'], sm['engaged'])}); "
             f"silent {sm['silent']} ({sm['accept_only']} took our opener, {sm['silent'] - sm['accept_only']} no deal).")
    if sm["missed"]:
        parts = []
        for x in sm["missed"]:
            parts.append(f"{x.duel} ({x.role}, limit {x.limit}, vs {x.rival}): ≈{x.missed:.1f} P left on the table")
        L.append(f"- In-limit offers not accepted: {len(sm['missed'])} — " + "; ".join(parts) + ".")
    else:
        L.append("- In-limit offers not accepted: 0.")
    if sm["passed_over"]:
        L.append(f"- Deals below an earlier in-limit rival offer: {len(sm['passed_over'])} "
                 f"(≈{sum(x.passed_over for x in sm['passed_over']):.1f} P: "
                 + ", ".join(f"{x.duel}" for x in sm["passed_over"]) + ").")
    if sm["deals"]:
        L.append(f"- Rounds and decay: {sm['mean_rounds']:.1f} rounds per deal; result {sm['result']:.1f} of "
                 f"{sm['surplus']:.1f} P surplus → {sm['decay_lost']:.1f} P ({sm['decay_share']:.0%}) lost to decay.")
    lat = (f"answered rival offers in {sm['lat_mean']:.1f} ticks on average (max {sm['lat_max']}; "
           f"{sm['lat_same']} of {sm['lat_n']} the same tick)" if sm["lat_n"] else "no rival offer to answer")
    took = (f"; decision {sm['took_mean']:.1f} s mean, {sm['took_max']:.1f} s max" if sm["took_mean"] is not None else "")
    L.append(f"- Latency: {lat}{took}" + (f"; {sm['unanswered']} rival offer(s) never answered" if sm["unanswered"] else "")
             + ".")
    L.append(f"- Concessions: we moved {sm['our_move']:.0f} P in total, rivals {sm['rival_move']:.0f} P.")
    if fin:
        b = behaviour_lines(fin)
        L.append("- Rival behaviours (best → worst by our mean result): " + " · ".join(b) + ".")
        best = max(fin, key=lambda x: x.result)
        worst = min(fin, key=lambda x: (x.result - (x.missed or 0), -(x.hold)))
        L.append(f"- Best duel: {best.duel} vs {best.rival} ({best.role}): {best.result:.1f} P in {best.rounds} round(s). "
                 f"Worst: {worst.duel} vs {worst.rival} ({worst.role}): {worst.status}"
                 + (f", {worst.missed:.1f} P in-limit left" if worst.missed else "")
                 + (f", both still {worst.hold} ticks" if worst.hold_flag else "") + ".")
    return L


def render_review(batch: list[DuelStats], session: list[DuelStats] | None, title: str,
                  pending: int = 0) -> str:
    sm = summarise(batch)
    L = [f"## {title}", ""]
    L += render_block(sm, "This wave" if session is not None else "All duels")
    if pending:
        L.append(f"- Not finished (no final payload): {pending}.")
    whole = sm
    if session is not None:
        whole = summarise(session)
        L += ["", *render_block(whole, "Session so far")]
    L += ["", "**For Aleks:**"] + [f"{i}. {s}" for i, s in enumerate(suggestions(whole), 1)]
    return "\n".join(L) + "\n"


def prepend_review(section: str, path: Path = REVIEW) -> None:
    body = path.read_text() if path.exists() else REVIEW_HEADER
    if not body.startswith("# Duel review"):
        body = REVIEW_HEADER + "\n" + body
    head, sep, rest = body.partition("\n## ")
    new = head.rstrip() + "\n\n" + section.rstrip() + "\n" + (("\n## " + rest) if sep else "")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(new)
    tmp.replace(path)


def replay_review(folder: Path, label: str | None = None) -> tuple[str, dict[str, Any]]:
    recs = load_records(folder)
    finals = [(r["done"], r) for r in recs if r.get("done")]
    stats = [analyse(raw, rec) for raw, rec in finals]
    pending = len(recs) - len(finals)
    sessions = sorted({str(raw.get("session")) for raw, _ in finals})
    title = (f"{time.strftime('%a %H:%M')} · replay of {label or folder.name} · {len(recs)} recorded duels"
             + (f" (game session {', '.join(sessions)})" if sessions else ""))
    return render_review(stats, None, title, pending=pending), summarise(stats)


# ---------------------------------------------------------------------------------------------------- test watch

def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True).stdout.strip()


def latest_foreign_commit(me: str, root: Path = ROOT) -> tuple[str, str, str] | None:
    """(sha, author, subject) of the newest commit touching the duelist or the engine by someone other than `me`."""
    out = git("log", "-50", "--format=%H%x09%an%x09%s", "--", *WATCH_PATHS, root=root)
    for line in out.splitlines():
        sha, author, subject = (line.split("\t", 2) + ["", ""])[:3]
        if author and author != me:
            return sha, author, subject
    return None


FAILED_RE = re.compile(r"^(?:FAILED|ERROR)\s+(\S+)", re.M)


def parse_failures(output: str) -> list[str]:
    return [m.split("::")[-1] if "::" in m else m for m in FAILED_RE.findall(output)]


def run_duelist_tests(sha: str | None = None, root: Path = ROOT) -> tuple[bool, list[str], str]:
    """Aleks's tests on a clean copy of commit `sha`, never on the shared working tree: Sat 09:44-09:46 it paged three
    false failures, from another session's half-done edit and a pull stuck mid-rebase. None: the working tree."""
    if shutil.which("uv"):
        cmd = ["uv", "run", "--project", str(root), "pytest", "-q", "-p", "no:cacheprovider", "tests/test_duelist.py"]
    else:
        cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_duelist.py"]
    with tempfile.TemporaryDirectory(prefix="duelist-tests-") as tmp:
        cwd = root
        if sha:
            arch = subprocess.run(["git", "-C", str(root), "archive", sha], capture_output=True)
            if arch.returncode != 0:
                return False, [], f"could not copy {sha[:7]}: {arch.stderr.decode(errors='replace')[:120]}"
            subprocess.run(["tar", "-x", "-C", tmp], input=arch.stdout, check=True)
            cwd = Path(tmp)
        try:
            p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=300)
        except (subprocess.TimeoutExpired, OSError, subprocess.CalledProcessError) as e:
            return False, [], f"could not run the tests: {e!r}"
    out = p.stdout + p.stderr
    tail = next((l for l in reversed(out.splitlines()) if l.strip()), "")
    return p.returncode == 0, parse_failures(out), tail


# ---------------------------------------------------------------------------------------------------- live

class ReadOnly:
    """The only game calls the monitor makes: GETs, at most one a second."""

    def __init__(self, b: Any, min_gap: float = 1.05):
        self.b, self.min_gap, self._last = b, min_gap, 0.0

    def _wait(self) -> None:
        gap = time.monotonic() - self._last
        if gap < self.min_gap:
            time.sleep(self.min_gap - gap)
        self._last = time.monotonic()

    def clock(self) -> dict:
        self._wait()
        return self.b.clock()

    def schedule(self) -> dict:
        self._wait()
        return self.b.schedule()

    def feed(self, limit: int = 200) -> dict:
        self._wait()
        return self.b.feed(limit)

    def leaderboard(self) -> dict:
        self._wait()
        return self.b.leaderboard()

    def duels(self, done: bool = False) -> dict:
        self._wait()
        return self.b.duels(done)


def load_env() -> None:
    """BAZAAR_KEY/BAZAAR_URL from the environment, else from .env (values never printed)."""
    if os.environ.get("BAZAAR_KEY"):
        return
    p = ROOT / ".env"
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        m = re.match(r"\s*(?:export\s+)?([A-Z_]+)\s*=\s*(.*)\s*$", line)
        if m and m.group(1) in ("BAZAAR_KEY", "BAZAAR_URL") and not os.environ.get(m.group(1)):
            words = shlex.split(m.group(2), comments=True)        # as the shell reads it: quotes, trailing comments
            if words:
                os.environ[m.group(1)] = words[0]


def local_record(did: Any) -> dict | None:
    p = RECORDS / f"duel-{did}.json"
    try:
        return json.loads(p.read_text()) if p.exists() else None
    except (json.JSONDecodeError, OSError):
        return None


class Monitor:
    def __init__(self, api: Any, *, notify: Callable[..., bool] | None = _notify, state_path: Path = STATE,
                 review_path: Path = REVIEW, me: str | None = None, test_watch: bool = True,
                 records: Callable[[Any], dict | None] = local_record, run_tests=run_duelist_tests,
                 foreign_commit=None, batch: int | None = None):
        self.api, self.notify_fn = api, notify
        self.state_path, self.review_path = state_path, review_path
        self.me = me if me is not None else git("config", "user.name")
        self.test_watch, self.records, self.run_tests = test_watch, records, run_tests
        self.foreign_commit = foreign_commit or (lambda: latest_foreign_commit(self.me))
        self.batch = batch
        self.state = self._load()
        self._sched_at = self._feed_at = self._tests_at = self._done_at = 0.0
        self._done: list[dict] | None = None
        self._live_ids: list[str] = []
        self.last_clock: dict = {}

    # state

    def _load(self) -> dict:
        try:
            return json.loads(self.state_path.read_text())
        except (OSError, json.JSONDecodeError):
            return {}

    def save(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=1, default=str))
        tmp.replace(self.state_path)

    # alerts

    def alert(self, flags: list[Flag]) -> list[Flag]:
        """Prints new flags; critical and high also go to Lucas and Dani. Deduped per (duel, flag). Returns the new."""
        sent = self.state.setdefault("notified", [])
        new = []
        for f in flags:
            if f.key in sent:
                continue
            sent.append(f.key)
            new.append(f)
            emit("DUEL " + f.severity.upper(), f.line())
            if f.severity == CRITICAL:                # Chief 17:40: Lucas gets CRITICAL only; Dani's phone is ACTs
                title = f"{f.severity.upper()} duel {f.duel}: {f.kind.replace('_', ' ')}" \
                    if not str(f.duel).startswith(("session:", "tests:")) else f"{f.severity.upper()} {f.kind.replace('_', ' ')}"
                self._notify("lucas", title, f.text, PRIORITY[f.severity], TAGS[f.severity])
        return new

    def _notify(self, channel: str, title: str, message: str, priority: int, tags: list[str]) -> bool:
        if self.notify_fn is None:
            print(f"notify[{channel}] (tools/notify.py unavailable) {title}: {message}", flush=True)
            return False
        try:
            return bool(self.notify_fn(channel, title, message, priority=priority, tags=tags))
        except Exception as e:  # noqa: BLE001
            print(f"notify[{channel}] failed: {e!r}", flush=True)
            return False

    # sessions

    def learn_sessions(self, sched: dict | None, feed: dict | None) -> None:
        """Duel sessions from the schedule (`upcoming` drops them once they fire) and the feed's duels.scheduled."""
        ss = self.state.setdefault("sessions", {})
        for u in (sched or {}).get("upcoming", []):
            if u.get("action") == "duels":
                p = u.get("params") or {}
                name = p.get("name") or u.get("note") or f"duels@{u.get('at_hours')}"
                ss.setdefault(name, {}).update(at_hours=u.get("at_hours"), params=p, note=u.get("note"))
        for e in (feed or {}).get("events", []):
            if e.get("type") == "duels.scheduled":
                p = e.get("payload") or {}
                name = p.get("name") or f"session {p.get('session')}"
                cur = ss.setdefault(name, {})
                cur.setdefault("params", {}).update({k: v for k, v in p.items() if v is not None})
                cur["start_tick"] = e.get("tick")

    def tick_at(self, at_hours: float) -> int | None:
        """The tick a schedule hour falls on, at the current pace: each tick advances tick_seconds of game time (30 s
        ticks: 120 a game hour; Friday's 60 s: 60). Measured Sat: ticks 159 → 175 took t_hours 2.65 → 2.7833."""
        c = self.last_clock or {}
        h, secs, now = c.get("t_hours"), c.get("tick_seconds"), c.get("tick")
        if not isinstance(h, (int, float)) or not isinstance(secs, (int, float)) or secs <= 0 or now is None:
            return None
        return int(now) + round((at_hours - h) * 3600 / secs)

    def current_session(self, tick: int) -> tuple[str, dict] | None:
        started = []
        for name, s in self.state.get("sessions", {}).items():
            start = s.get("start_tick")                  # from the feed's duels.scheduled: exact
            if start is None and isinstance(s.get("at_hours"), (int, float)):
                start = self.tick_at(s["at_hours"])
            if start is not None and start <= tick:
                started.append((start, name, {**s, "start_tick": start}))
        if not started:
            return None
        _, name, s = max(started, key=lambda x: x[0])
        return name, s

    def per_team(self, s: dict) -> int:
        p = s.get("params") or {}
        rounds = p.get("rounds") or 1
        if isinstance(p.get("duels"), int) and p["duels"] > 0:      # n(n-1)·rounds duels in all
            n = (1 + math.sqrt(1 + 4 * p["duels"] / rounds)) / 2
            return round(2 * p["duels"] / n)
        n = self.state.get("teams")
        if not n:
            try:
                n = len(self.api.leaderboard().get("teams", [])) or None
            except Exception:  # noqa: BLE001
                n = None
            self.state["teams"] = n
        return 2 * (n - 1) * rounds if n else 34

    def session_flag(self, tick: int, live: list[dict], done: list[dict]) -> list[Flag]:
        cur = self.current_session(tick)
        if cur is None:
            return []
        name, s = cur
        p = s.get("params") or {}
        key = f"session:{name}"
        if live:
            self.state.pop("no_live_since", None)
            self.state["notified"] = [k for k in self.state.get("notified", []) if not k.startswith(key + "|")]
            return []
        if "practice" in name.lower():
            return []
        per_team = self.per_team(s)
        dt, conc = p.get("duel_ticks") or 16, p.get("max_concurrent") or 3
        end = s["start_tick"] + math.ceil(per_team / conc) * dt + dt
        finished = sum(1 for d in done if (d.get("deadline_tick") or 0) > s["start_tick"])
        if not (s["start_tick"] + 1 < tick < end and finished < per_team):
            self.state.pop("no_live_since", None)
            return []
        since = self.state.setdefault("no_live_since", tick)
        if tick - since + 1 < NO_LIVE_TICKS:
            return []
        return [Flag(key, "no_live_duel", CRITICAL, tick,   # a possible duelist failover: Lucas (Chief 17:40)
                     f"{name} is running (started tick {s['start_tick']}, we've finished {finished} of ~{per_team}) "
                     f"but /api/duels shows no live duel for us since tick {since}: check the duelist and the key.")]

    # reviews

    def maybe_review(self, tick: int, live: list[dict], done: list[dict]) -> str | None:
        reviewed = set(map(str, self.state.setdefault("reviewed", [])))
        if not self.state.get("review_init"):                # don't review what finished before we started
            self.state["reviewed"] = sorted({str(rid(d)) for d in done})
            self.state["review_init"] = True
            return None
        fresh = [d for d in done if str(rid(d)) not in reviewed and str(d.get("status", "")).lower() != "live"]
        if not fresh:
            return None
        # A wave is done when no duel is live, when max_concurrent duels have finished, or when the oldest unreviewed
        # one has waited two duel lengths (deals close early and their slots refill, so waves blur).
        cur = self.current_session(tick)
        params = (cur[1].get("params") or {}) if cur else {}
        size = self.batch or params.get("max_concurrent") or 3
        waited = tick - min((d.get("deadline_tick") or tick) for d in fresh)
        if live and len(fresh) < size and waited < 2 * (params.get("duel_ticks") or 16):
            return None
        sess_no = max((d.get("session") or 0) for d in fresh)
        session = [d for d in done if (d.get("session") or 0) == sess_no and str(d.get("status", "")).lower() != "live"]
        an = lambda d: analyse(d, self.records(rid(d)))          # noqa: E731
        name = cur[0] if cur else f"session {sess_no}"
        title = (f"{time.strftime('%a %H:%M')} · {name} · tick {tick} · wave of {len(fresh)} "
                 f"(duels {', '.join(str(rid(d)) for d in sorted(fresh, key=lambda d: rid(d) or 0))})")
        section = render_review([an(d) for d in fresh], [an(d) for d in session], title)
        prepend_review(section, self.review_path)
        self.state["reviewed"] = sorted(reviewed | {str(rid(d)) for d in fresh})
        emit("DUEL REVIEW", f"wave of {len(fresh)} written to {self.review_path}")
        return section

    # test watch

    def check_tests(self) -> list[Flag]:
        c = self.foreign_commit()
        if c is None:
            return []
        sha, author, subject = c
        if self.state.get("tests_sha") == sha:
            return []
        self.state["tests_sha"] = sha
        ok, failed, tail = self.run_tests(sha)
        emit("DUELIST TESTS", f"{'pass' if ok else 'FAIL'} after {author} {sha[:7]} ({subject[:60]}): {tail[:120]}")
        if ok:
            return []
        if failed and set(failed) <= KNOWN_DATA_FAILURES:
            emit("DUELIST TESTS", f"only the known data-dependent failure ({', '.join(failed)}): not paged")
            return []
        names = ", ".join(failed[:8]) or tail[:200]
        return [Flag(f"tests:{sha[:7]}", "duelist_tests_failed", CRITICAL, None,   # tests red: Lucas (17:40)
                     f"tests/test_duelist.py fails after {author}'s {sha[:7]} \"{subject[:60]}\": {names}")]

    # one evaluation

    def cycle(self, clock: dict | None = None) -> list[Flag]:
        clock = self.last_clock = clock or self.api.clock()
        tick = clock.get("tick")
        flags: list[Flag] = []
        now = time.monotonic()
        if self.test_watch and now - self._tests_at > 60:
            self._tests_at = now
            flags += self.check_tests()
        open_ = clock.get("doors") in (None, "open") and not clock.get("paused")
        if open_ and tick is not None:
            sched = feed = None
            if now - self._sched_at > 300:
                self._sched_at = now
                sched = self.api.schedule()
            if now - self._feed_at > 120:
                self._feed_at = now
                feed = self.api.feed(200)
            if sched is not None or feed is not None:
                self.learn_sessions(sched, feed)
            live = [d for d in self.api.duels().get("duels", []) if is_live(d)]
            ids = sorted(str(rid(d)) for d in live)
            # The finished list only changes when a duel leaves the live list; read it then (or every 5 minutes, or
            # while nothing is live), not every tick.
            if self._done is None or ids != self._live_ids or not live or now - self._done_at > 300:
                self._done, self._done_at = self.api.duels(done=True).get("duels", []), now
            self._live_ids = ids
            done = self._done
            seen = self.state.setdefault("first_seen", {})
            cur = self.current_session(tick)
            dt = (cur[1].get("params") or {}).get("duel_ticks") if cur else None
            for raw in live:
                did = str(rid(raw))
                seen.setdefault(did, tick)
                rec = self.records(rid(raw)) or {}
                accepted = any((x.get("move") or {}).get("action") == "accept" and (x.get("tick") or 0) >= tick - 1
                               for x in rec.get("sent") or [])
                flags += live_flags(raw, tick, first_seen=seen[did], duel_ticks=dt, errors=rec.get("errors"),
                                    accepted=accepted)
            checked = set(map(str, self.state.setdefault("closed_checked", [])))
            for raw in done:
                if str(rid(raw)) not in checked:
                    flags += closed_flags(raw)
                    checked.add(str(rid(raw)))
            self.state["closed_checked"] = sorted(checked)
            flags += self.session_flag(tick, live, done)
            self.maybe_review(tick, live, done)
            self.state["last_tick"] = tick
        new = self.alert(flags)
        self.save()
        return new


def run_loop(m: Monitor, every: float) -> None:
    """Once per server tick, `every` seconds (or half a tick) into it, so the duelist has had time to act."""
    last = None
    while True:
        try:
            c = m.api.clock()
            ts = float(c.get("tick_seconds") or 30)
            nti = float(c.get("next_tick_in") or 1)
            if c.get("paused") or c.get("doors") not in (None, "open"):
                m.cycle(c)                        # test watch only; duels aren't read while closed
                time.sleep(max(60.0, every))
                continue
            offset = min(every, ts / 2)
            into = ts - nti
            if c.get("tick") != last:
                if into < offset:
                    time.sleep(offset - into)
                    c = m.api.clock()
                m.cycle(c)
                last = c.get("tick")
            time.sleep(max(1.0, min(every, nti + offset)))
        except KeyboardInterrupt:
            raise
        except Exception as e:  # noqa: BLE001  keep watching through a bad read
            emit("DUEL MONITOR ERROR", repr(e)[:200])
            time.sleep(max(every, 15))


def make_api() -> ReadOnly:
    load_env()
    sys.path.insert(0, str(ROOT / "bazaar-kit"))
    from bazaar_sdk import Bazaar  # noqa: E402
    key = os.environ.get("BAZAAR_KEY")
    if not key:
        sys.exit("BAZAAR_KEY is not set (source .env first)")
    return ReadOnly(Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), key,
                           wait_on_tick=False, retries=1))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--once", action="store_true", help="one evaluation against the live server")
    mode.add_argument("--every", type=float, metavar="S", help="loop: once per tick, S seconds (or half a tick) into it")
    mode.add_argument("--replay", type=Path, metavar="DIR", help="offline: replay recorded duels (docs/duels)")
    ap.add_argument("--write", action="store_true", help="replay: also prepend the review to intel/duel-review.md")
    ap.add_argument("--no-tests", action="store_true", help="skip the duelist test watch")
    ap.add_argument("--batch", type=int, help="review after this many finished duels (default: the session's max_concurrent)")
    ap.add_argument("--state", type=Path, default=STATE, help=f"monitor state file (default {STATE.relative_to(ROOT)})")
    a = ap.parse_args(argv)

    if a.replay:
        folder = a.replay if a.replay.is_absolute() else (Path.cwd() / a.replay)
        flags = []
        for rec in load_records(folder):
            flags += first_per_kind(replay_record(rec))
        print(f"# Flags the live monitor would have raised ({len(flags)}, first tick of each)\n")
        for f in sorted(flags, key=lambda f: ({CRITICAL: 0, HIGH: 1, MEDIUM: 2}[f.severity], f.tick or 0)):
            print("- " + f.line())
        section, _ = replay_review(folder, str(a.replay))
        print("\n# Review it would write\n")
        print(section)
        if a.write:
            prepend_review(section)
            print(f"(prepended to {REVIEW.relative_to(ROOT)})")
        return 0

    m = Monitor(make_api(), test_watch=not a.no_tests, batch=a.batch, state_path=a.state)
    if a.once:
        new = m.cycle()
        c = m.last_clock
        closed = c.get("paused") or c.get("doors") not in (None, "open")
        emit("DUEL MONITOR", f"tick {c.get('tick')}" + (" (doors closed or paused: duels not read)" if closed else "")
             + f": {len(new)} new flag(s)")
        return 0
    run_loop(m, a.every)
    return 0


if __name__ == "__main__":
    sys.exit(main())
