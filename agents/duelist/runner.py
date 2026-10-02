"""The duel loop: poll the game, let the agent decide for each live duel whose rival has moved, send the move.

Rules it keeps (RULES.md): one message per duel per tick, one acceptance per team per tick, 5 requests a second
per key. A poll is two reads (`clock`, `duels`) every `poll_s` seconds; each duel then costs one write per tick
at most. The SDK is synchronous, so every call runs in a thread and the model calls of several duels overlap.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from bazaar_sdk import Bazaar, BazaarError
from engine import Model

from .adapter import Snapshot, parse_duel
from .agent import DuelAgent, Move
from .model import Observation, Offer, Turn
from .prices import money
from .records import Records, duel_key


class Log:
    """Everything to one JSONL file: raw payloads (when they change), decisions, sends, errors."""

    def __init__(self, folder: Path):
        folder.mkdir(parents=True, exist_ok=True)
        self.path = folder / f"duels-{datetime.now():%Y%m%d-%H%M%S}.jsonl"
        self._seen: dict[str, str] = {}

    def write(self, event: str, **data: Any) -> None:
        with self.path.open("a") as f:
            f.write(json.dumps({"ts": round(time.time(), 2), "event": event, **data}, default=str) + "\n")

    def changed(self, key: str, payload: Any) -> bool:
        h = hashlib.sha1(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
        if self._seen.get(key) == h:
            return False
        self._seen[key] = h
        return True


def say(msg: str) -> None:
    print(f"{datetime.now():%H:%M:%S} {msg}", flush=True)


@dataclass
class Memory:
    """What we remember about one duel between polls."""
    agent: DuelAgent
    snap: Snapshot
    sent: list[Turn] = field(default_factory=list)       # our messages, with the decision behind each
    seen: list[Turn] = field(default_factory=list)       # their offers as we saw them change (no message list)
    decided_on: Any = None                               # the rival's state our last move answered
    sent_tick: int | None = None
    task: asyncio.Task | None = None
    pending: tuple[Move, Any] | None = None              # a move refused with wait_for_tick, for the next tick
    force: bool = False                                  # decide again even if the rival hasn't moved


def signature(snap: Snapshot) -> Any:
    """The rival's state: what a new move from us answers."""
    theirs = [t.model_dump() for t in (snap.messages or []) if not t.mine]
    return json.dumps([theirs, snap.rival_offer.model_dump() if snap.rival_offer else None], sort_keys=True)


class DuelRunner:
    def __init__(self, b: Bazaar, strategist: Model, negotiator: Model, *, dry_run: bool, log: Log,
                 decay: float | None, duel_ticks: int | None, poll_s: float, records: Records | None = None):
        self.b = b
        self.strategist, self.negotiator = strategist, negotiator
        self.dry_run = dry_run
        self.log = log
        self.overrides = {k: v for k, v in (("decay", decay), ("duel_ticks", duel_ticks)) if v is not None}
        self.session: dict[str, Any] = {}       # the current duel session's params from the schedule
        self.poll_s = poll_s
        self.team: set[str] = set()
        self.duels: dict[Any, Memory] = {}
        self.tick: int | None = None
        self.tick_seconds = 60.0
        self.accepted_tick: int | None = None   # one acceptance per team per tick
        self.spent_usd = 0.0
        self.records = records

    def record(self, key: Any, **fields: Any) -> None:
        """Into the duel's record; a failure here must never stop a duel."""
        if self.records is None:
            return
        try:
            self.records.save(key, **fields)
        except Exception as e:
            self.log.write("error", where="record", duel=key, error=repr(e))

    async def call(self, fn, *args, **kw):
        return await asyncio.to_thread(fn, *args, **kw)

    # The session's params

    async def refresh_session(self, now_hours: float | None = None) -> None:
        """The duel session in play (or the next one) from the schedule: its decay and ticks per duel."""
        try:
            sched = await self.call(self.b.schedule)
        except BazaarError as e:
            self.log.write("error", where="schedule", error=str(e))
            return
        now = sched.get("now_hours", now_hours) or 0
        sessions = [u for u in sched.get("upcoming", []) if u.get("action") == "duels"]
        started = [u for u in sessions if u.get("at_hours", 0) <= now + 0.02]
        nxt = started[-1] if started else (sessions[0] if sessions else None)
        if nxt and (not self.session or nxt.get("at_hours", 0) <= now + 0.02):
            if nxt.get("params") != self.session:
                self.session = dict(nxt.get("params") or {})
                self.log.write("session", at_hours=nxt.get("at_hours"), params=self.session)
                say(f"duel session: {self.session.get('name')} at hour {nxt.get('at_hours')}, "
                    f"{self.session.get('duel_ticks')} ticks, decay {self.session.get('decay')}, "
                    f"issues {self.session.get('issues', ['price'])}")

    def defaults(self) -> dict[str, Any]:
        return {"decay": self.session.get("decay"), "duel_ticks": self.session.get("duel_ticks"), **self.overrides}

    # Observations

    def observe(self, mem: Memory) -> Observation:
        snap = mem.snap
        if snap.messages is not None:
            turns = [t.model_copy() for t in snap.messages]
            ours = iter(mem.sent)
            for t in turns:                       # our decisions, in order, for the negotiator's transcript
                if t.mine and (sent := next(ours, None)) is not None:
                    t.decision = sent.decision
        else:
            turns = sorted([*mem.sent, *mem.seen], key=lambda t: (t.tick if t.tick is not None else -1, not t.mine))
        assert snap.view is not None
        return Observation(view=snap.view, turns=turns, rival_offer=snap.rival_offer, tick=self.tick,
                           ticks_left=snap.ticks_left)

    def update(self, raw: dict[str, Any]) -> Memory | None:
        snap = parse_duel(raw, team=self.team, tick=self.tick, defaults=self.defaults())
        key = snap.id
        if self.log.changed(f"duel:{key}", raw):
            self.log.write("duel", tick=self.tick, raw=raw, problems=snap.problems)
            self.record(key, payloads=[{"tick": self.tick, "raw": raw}], problems=snap.problems or None)
        mem = self.duels.get(key)
        if mem is None:
            if snap.view is None:
                if self.log.changed(f"unreadable:{key}", snap.problems):
                    say(f"duel {key}: can't read it ({'; '.join(snap.problems)}); see {self.log.path}")
                return None
            agent = DuelAgent(snap.view, self.strategist, self.negotiator)
            mem = self.duels[key] = Memory(agent=agent, snap=snap)
            v = snap.view
            say(f"duel {key} vs {v.rival or '?'}: {v.role.value}, limit {money(v.limit)}, issues {v.issues}, "
                f"{snap.ticks_left} ticks left" + (f" [{'; '.join(snap.problems)}]" if snap.problems else ""))
            self.log.write("new_duel", duel=key, view=v.model_dump(), strategist_system=agent.strategist_system,
                           negotiator_system=agent.negotiator_system)
            self.record(key, session=self.session, first_tick=self.tick, view=v.model_dump(),
                        models={"strategist": self.strategist.label, "negotiator": self.negotiator.label},
                        strategist_system=agent.strategist_system, negotiator_system=agent.negotiator_system)
        mem.snap = snap
        if snap.messages is None and snap.rival_offer is not None:
            last = next((t.offer for t in reversed(mem.seen)), None)
            if last != snap.rival_offer:
                text = str(raw.get("rival_text") or raw.get("rival_message") or "")
                mem.seen.append(Turn(mine=False, text=text, offer=snap.rival_offer, tick=self.tick))
        return mem

    # Deciding and sending

    def due(self, mem: Memory) -> bool:
        if mem.task is not None or mem.sent_tick == self.tick or not mem.snap.live:
            return False
        if mem.pending is not None or mem.force:
            return True
        return not mem.sent or signature(mem.snap) != mem.decided_on

    async def decide(self, mem: Memory) -> None:
        sig = signature(mem.snap)
        if mem.pending is not None:
            move, pending_sig = mem.pending
            mem.pending = None
            if pending_sig == sig:                # nothing changed: send what we decided last tick
                await self.send(mem, move, sig)
                return
        mem.force = False
        obs = self.observe(mem)
        start = time.perf_counter()
        timeout = max(8.0, self.tick_seconds - 5.0)
        try:
            move = await asyncio.wait_for(mem.agent.respond(obs), timeout)
        except TimeoutError:
            move = mem.agent.final(mem.agent.safe_move(obs, f"timeout after {timeout:.0f} s"), obs)
        except Exception as e:                    # never let one duel's bug stop the loop
            self.log.write("error", where="respond", duel=mem.snap.id, error=repr(e))
            move = mem.agent.final(mem.agent.safe_move(obs, f"error: {e!r}"), obs)
        took = time.perf_counter() - start
        cost = sum(c["cost_usd"] for c in move.meta.get("calls", []))
        self.spent_usd += cost
        self.log.write("decision", duel=mem.snap.id, tick=self.tick, took_s=round(took, 2), cost_usd=cost,
                       obs=obs.model_dump(), move=move.__dict__)
        self.record(mem.snap.id, decisions=[{"tick": self.tick, "took_s": round(took, 2), "cost_usd": cost,
                                             "obs": obs.model_dump(), "move": move.__dict__}])
        if signature(mem.snap) != sig and move.action == "accept":
            say(f"duel {mem.snap.id}: their offer changed while deciding; deciding again")
            mem.force = True
            return
        await self.send(mem, move, sig, took)

    async def send(self, mem: Memory, move: Move, sig: Any, took: float | None = None) -> None:
        did, v = mem.snap.id, mem.agent.view
        band = move.meta.get("band") or {}
        what = (f"offer {money(move.price)}" + (f" day {move.days}" if move.days is not None else "")
                if move.action == "offer" else
                f"accept {money(move.price) if move.price is not None else '?'}" if move.action == "accept" else
                "message")
        note = (f" band {band.get('worst')}..{band.get('best')}" if band else "") + \
               (f" FALLBACK({move.meta['fallback']})" if move.meta.get("fallback") else "") + \
               (" repaired" if move.meta.get("repaired") else "") + (f" {took:.1f}s" if took else "")
        if move.action == "accept" and self.accepted_tick == self.tick:
            mem.pending = (move, sig)             # one acceptance per team per tick: try next tick
            say(f"duel {did}: {what} waits for the next tick (another acceptance this tick)")
            return
        say(f"{'DRY ' if self.dry_run else ''}[tick {self.tick}] duel {did} ({v.role.value}, limit {v.limit}): "
            f"{what}{note} :: {move.text[:140]}")
        result: Any = "dry-run"
        if not self.dry_run:
            try:
                if move.action == "accept":
                    result = await self.call(self.b.duel_accept, did)
                else:
                    result = await self.call(self.b.duel_say, did, move.text, move.price, move.days)
            except BazaarError as e:
                self.log.write("send_error", duel=did, tick=self.tick, code=e.code, message=e.message,
                               extra=e.extra, move=move.__dict__)
                self.record(did, errors=[{"tick": self.tick, "code": e.code, "message": e.message,
                                          "move": move.__dict__}])
                if e.code == "wait_for_tick":
                    mem.pending = (move, sig)
                    return
                if e.code == "missing_days" and "days" not in v.issues:
                    v.issues.append("days")
                    mem.agent = DuelAgent(v, self.strategist, self.negotiator)
                    mem.force = True
                say(f"duel {did}: refused: {e.code}: {e.message}")
                return
        self.log.write("sent", duel=did, tick=self.tick, move=move.__dict__, result=result)
        self.record(did, sent=[{"tick": self.tick, "dry_run": self.dry_run, "move": move.__dict__, "result": result}])
        if move.action == "accept":
            self.accepted_tick = self.tick
        mem.sent.append(Turn(mine=True, text=move.text, accept=move.action == "accept", tick=self.tick,
                             offer=Offer(price=move.price, days=move.days) if move.action == "offer" else None,
                             decision=move.meta.get("decision")))
        mem.sent_tick = self.tick
        mem.decided_on = sig

    async def finish(self, gone: list[Any]) -> None:
        """Duels that left the live list: log how they ended."""
        try:
            done = {d.get("id", d.get("duel_id")): d for d in (await self.call(self.b.duels, True)).get("duels", [])}
        except BazaarError:
            done = {}
        for key in gone:
            mem = self.duels.pop(key)
            if mem.task is not None:
                mem.task.cancel()
            raw = done.get(key)
            self.log.write("finished", duel=key, raw=raw)
            self.record(key, last_seen_tick=self.tick, done=raw)   # if not in the done list yet, the sweep adds it
            say(f"duel {key} finished: " + (json.dumps({k: raw[k] for k in raw if k not in ('messages',)})[:300]
                                             if raw else "(not in the done list yet)"))

    async def sweep(self) -> None:
        """Every minute: finished duels we haven't recorded (also ones a restart missed), the feed's duel events,
        our duel points. Three reads; any failure is logged and skipped."""
        if self.records is None:
            return
        try:
            for raw in (await self.call(self.b.duels, True)).get("duels", []):
                key = duel_key(raw)
                if key is not None and key not in self.duels and not self.records.finished(key):
                    self.record(key, done=raw)
                    self.log.write("recorded", duel=key)
            self.records.add_feed((await self.call(self.b.feed, 200)).get("events", []))
            self.records.add_score(self.tick, (await self.call(self.b.me)).get("score") or {})
        except Exception as e:
            self.log.write("error", where="sweep", error=repr(e))

    # The loop

    async def run(self) -> None:
        me = await self.call(self.b.me)
        self.team = {str(me.get("id")), str(me.get("name"))}
        say(f"{me.get('name')} ({me.get('id')}): {'DRY RUN, ' if self.dry_run else ''}strategist "
            f"{self.strategist.label}, negotiator {self.negotiator.label}; log {self.log.path}")
        await self.refresh_session()
        await self.sweep()
        last_schedule = time.monotonic()
        while True:
            try:
                clock = await self.call(self.b.clock)
                if clock.get("tick") != self.tick:
                    self.tick = clock.get("tick")
                    self.tick_seconds = float(clock.get("tick_seconds") or self.tick_seconds)
                if time.monotonic() - last_schedule > 60:
                    await self.refresh_session(clock.get("t_hours"))
                    await self.sweep()
                    last_schedule = time.monotonic()
                if clock.get("doors") not in (None, "open") or clock.get("paused"):
                    await asyncio.sleep(max(self.poll_s, 10))
                    continue
                live = (await self.call(self.b.duels)).get("duels", [])
            except Exception as e:                # never let a bad read stop the loop
                self.log.write("error", where="poll", error=repr(e))
                say(f"poll failed: {e!r}")
                await asyncio.sleep(self.poll_s * 2)
                continue
            keys = set()
            for raw in live:
                try:
                    mem = self.update(raw)
                except Exception as e:            # one unreadable duel must not stop the others
                    self.log.write("error", where="update", raw=raw, error=repr(e))
                    say(f"duel payload failed: {e!r}")
                    if (k := duel_key(raw)) in self.duels:
                        keys.add(k)               # keep it; don't finish it on a parse error
                    continue
                if mem is None:
                    continue
                keys.add(mem.snap.id)
                if self.due(mem):
                    mem.task = asyncio.create_task(self._decide(mem))
            if gone := [k for k in self.duels if k not in keys and self.duels[k].task is None]:
                try:
                    await self.finish(gone)
                except Exception as e:
                    self.log.write("error", where="finish", error=repr(e))
            await asyncio.sleep(self.poll_s)

    async def _decide(self, mem: Memory) -> None:
        try:
            await self.decide(mem)
        except Exception as e:
            self.log.write("error", where="decide", duel=mem.snap.id, error=repr(e))
            say(f"duel {mem.snap.id}: error {e!r}")
        finally:
            mem.task = None
