"""From the game's duel JSON to what the agent sees.

The duel payload is not documented beyond `GET /api/duels` "role, your_limit, rival_offer, deadline" (the SDK
docstring) and `your_days_weight` (RULES.md). So every field is looked up under a few likely names, and what we
can't place goes to `DuelView.extra` for the strategist (never the negotiator) and into the log. Check the log of
the first practice duel and tighten the names here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .model import DuelView, Offer, Role, Turn

# `GET /api/duels` lists live duels only, so any other status counts as live.
DONE = {"deal", "done", "closed", "expired", "no_deal", "finished", "settled", "scored", "walked", "timeout",
        "timed_out", "agreed", "accepted", "failed", "cancelled", "canceled", "over", "ended", "complete", "completed"}
MESSAGE_KEYS = ("messages", "history", "transcript", "log", "turns")
# Keys we read; everything else of the top level goes to `extra`. Limits are listed so they never reach it twice.
KNOWN = {"id", "duel_id", "duel", "status", "state", "done", "closed", "role", "your_role", "side", "your_limit", "limit",
         "your_cost", "your_value", "cost", "value", "reservation", "rival_offer", "their_offer", "rival",
         "rival_alias", "opponent", "alias", "your_offer", "my_offer", "own_offer", "deadline", "deadline_tick",
         "ends_at_tick", "end_tick", "expires_tick", "ticks_left", "remaining_ticks", "issues",
         "your_days_weight", "days_weight", "decay", "duel_ticks", "item", "title", "name", "scenario",
         "description", "brief", "story", "context", "market", "market_range", "reference_price", "tick",
         "session", "practice", "result", "score", *MESSAGE_KEYS}


def first(d: dict[str, Any], *keys: str) -> Any:
    for k in keys:
        if isinstance(d, dict) and d.get(k) is not None:
            return d[k]
    return None


def as_number(x: Any) -> float | None:
    if isinstance(x, bool):
        return None
    if isinstance(x, int | float):
        return float(x)
    if isinstance(x, str):
        try:
            return float(x)
        except ValueError:
            return None
    if isinstance(x, dict):
        return as_number(first(x, "price", "cash", "amount", "value", "limit", "cost"))
    return None


def as_offer(x: Any) -> Offer | None:
    """An offer as the game may state it: a number, {"price", "days"}, or a message with an "offer" in it."""
    if x is None:
        return None
    if isinstance(x, dict) and isinstance(x.get("offer"), dict):
        x = x["offer"]
    price = as_number(x)
    if price is None:
        return None
    days = x.get("days") if isinstance(x, dict) else None
    return Offer(price=round(price), days=int(days) if isinstance(days, int | float) else None)


def as_role(x: Any) -> Role | None:
    x = str(x or "").lower()
    if x.startswith("sell") or x in ("s", "ask"):
        return Role.SELLER
    if x.startswith("buy") or x in ("b", "bid"):
        return Role.BUYER
    return None


@dataclass
class Snapshot:
    """One duel as the game showed it at one poll."""
    id: int | str
    live: bool
    status: str
    view: DuelView | None                 # None: we couldn't read our role or limit
    rival_offer: Offer | None
    our_offer: Offer | None
    tick: int | None
    deadline: Any
    ticks_left: int | None
    messages: list[Turn] | None           # None: the payload has no message list
    problems: list[str]
    raw: dict[str, Any]


def ticks_left(raw: dict[str, Any], tick: int | None, duel_ticks: int | None) -> tuple[int | None, Any]:
    """Ticks left including the current one, from `ticks_left` or from a deadline tick."""
    left = as_number(first(raw, "ticks_left", "remaining_ticks"))
    deadline = first(raw, "deadline", "deadline_tick", "ends_at_tick", "end_tick", "expires_tick")
    if left is not None:
        return max(int(left), 0), deadline
    d = as_number(deadline if not isinstance(deadline, dict) else first(deadline, "tick", "at_tick"))
    if d is None or tick is None:
        return None, deadline
    if d >= tick:
        return int(d - tick) + 1, deadline            # a tick number
    if duel_ticks and d <= duel_ticks:
        return int(d), deadline                       # already a count
    return None, deadline


def sender_is_us(m: dict[str, Any], role: Role, team: set[str], rival: str) -> bool | None:
    for k in ("mine", "yours", "from_me", "is_me", "own"):
        if isinstance(m.get(k), bool):
            return m[k]
    who = first(m, "from", "sender", "by", "author", "speaker", "side", "role", "team")
    if isinstance(who, dict):
        who = first(who, "id", "alias", "name", "role")
    if who is None:
        return None
    w = str(who).lower()
    if w in {"you", "me", "self", "us", "yours", "mine"} | {t.lower() for t in team}:
        return True
    if w in {"rival", "them", "opponent", "other"} or (rival and w == rival.lower()):
        return False
    r = as_role(w)
    return None if r is None else r is role


def read_messages(raw: dict[str, Any], role: Role, team: set[str], rival: str) -> tuple[list[Turn] | None, int]:
    """The message list, if the payload has one. Returns the turns and how many senders we couldn't place."""
    msgs = first(raw, *MESSAGE_KEYS)
    if not isinstance(msgs, list):
        return None, 0
    out, unknown = [], 0
    for m in msgs:
        if not isinstance(m, dict):
            continue
        mine = sender_is_us(m, role, team, rival)
        if mine is None:
            unknown += 1
            mine = False
        kind = str(first(m, "kind", "type", "action") or "").lower()
        out.append(Turn(mine=mine, text=str(first(m, "text", "message", "body") or ""),
                        offer=as_offer(first(m, "offer", "price")) if kind not in ("accept", "accepted") else None,
                        accept=kind in ("accept", "accepted") or m.get("accept") is True,
                        tick=int(m["tick"]) if isinstance(m.get("tick"), int) else None))
    return out, unknown


def parse_duel(raw: dict[str, Any], *, team: set[str], tick: int | None, defaults: dict[str, Any]) -> Snapshot:
    """`team`: our team's id and name, to recognise our own messages. `defaults`: the session's `decay` and
    `duel_ticks` from the schedule, used when the duel doesn't state them."""
    problems: list[str] = []
    did = first(raw, "id", "duel_id", "duel")
    status = str(first(raw, "status", "state") or "")
    live = status.lower() not in DONE and not raw.get("done") and not raw.get("closed")
    role = as_role(first(raw, "role", "your_role", "side"))
    limit = as_number(first(raw, "your_limit", "limit", "your_cost", "your_value", "reservation"))
    rival = first(raw, "rival", "rival_alias", "opponent", "alias")
    rival = str(first(rival, "alias", "name", "id") if isinstance(rival, dict) else rival or "")
    duel_ticks = as_number(first(raw, "duel_ticks")) or defaults.get("duel_ticks")
    left, deadline = ticks_left(raw, tick, int(duel_ticks) if duel_ticks else None)
    if left is None:
        problems.append(f"ticks left unknown (deadline={deadline!r})")
    view = None
    messages = None
    if role is None or limit is None:
        problems.append(f"can't read role ({first(raw, 'role', 'your_role', 'side')!r}) or limit")
    else:
        scenario = raw.get("scenario")
        sc = scenario if isinstance(scenario, dict) else {}
        item = first(raw, "item", "title", "name") or first(sc, "item", "title", "name")
        context = first(raw, "description", "brief", "story", "context") or first(sc, "description", "brief",
                                                                                  "story", "context")
        if isinstance(scenario, str) and not context:
            context = scenario
        market = first(raw, "market", "market_range", "reference_price") or first(sc, "market", "market_range",
                                                                                   "reference_price")
        issues = raw.get("issues") or ["price"]
        if not isinstance(issues, list):
            issues = [str(issues)]
        weight = first(raw, "your_days_weight", "days_weight")
        if weight is not None and "days" not in issues:
            issues = [*issues, "days"]
        view = DuelView(
            duel_id=did, role=role, limit=round(limit), item=str(item or ""), context=str(context or "")[:600],
            rival=rival, market=str(market) if market is not None else None, issues=[str(i) for i in issues],
            days_weight=weight, decay=as_number(raw.get("decay")) or defaults.get("decay"),
            duel_ticks=int(duel_ticks) if duel_ticks else None,
            extra={k: v for k, v in raw.items() if k not in KNOWN})
        messages, unknown = read_messages(raw, role, team, rival)
        if unknown:
            problems.append(f"{unknown} messages with an unknown sender (taken as theirs)")
    return Snapshot(id=did, live=live, status=status, view=view,
                    rival_offer=as_offer(first(raw, "rival_offer", "their_offer")),
                    our_offer=as_offer(first(raw, "your_offer", "my_offer", "own_offer")),
                    tick=tick, deadline=deadline, ticks_left=left, messages=messages, problems=problems, raw=raw)
