"""Tick-decay policy, whole-package authorization, deadlines and cache warm-up; offline only."""
import asyncio
import json
import time
from types import SimpleNamespace

import pytest

from agents.duelist.agent import BandPlan, Decision, DuelAgent, ledger, tick_prefix
from agents.duelist.model import DuelView, Observation, Offer, Role, Turn
from agents.duelist.runner import DuelRunner, Log
from engine import CACHE_PREFIX_END, Reply
from engine.claude import Claude
from engine.failover import Failover


def view(role=Role.SELLER, days=False, limit=40):
    return DuelView(duel_id=1, role=role, limit=limit, decay=0.1, duel_ticks=12,
                    issues=["price", "days"] if days else ["price"],
                    days_weight=2 if days else None,
                    days_meaning="each delivery day costs you this much cash" if days else None)


def plan(target=100, worst=90, best=110, days=None, **kw):
    return BandPlan(target=target, worst=worst, best=best, days=days, read="Their offer moved.",
                    angle="State the price plainly.", **kw)


def obs(v, price=None, day=None, tick=10):
    return Observation(view=v, tick=tick, ticks_left=8,
                       rival_offer=Offer(price=price, days=day) if price is not None else None)


class Model:
    label = "fake"

    def __init__(self, answer, delay=0):
        self.answer, self.delay, self.calls = answer, delay, 0

    async def parse(self, schema, system, messages):
        self.calls += 1
        await asyncio.sleep(self.delay)
        return Reply(self.answer, self.delay, 10, 10, 0, "fake")


@pytest.mark.parametrize("role,limit,p,prices", [
    (Role.SELLER, 40, plan(), [89, 90, 100, 111]),
    (Role.BUYER, 140, plan(80, 90, 70), [91, 90, 80, 69]),
])
def test_cached_band_accepts_boundaries_and_better_than_best_without_models(role, limit, p, prices):
    v = view(role, limit=limit)
    m = Model(None)
    a = DuelAgent(v, m, tick_decay=True)
    a.cache_plan(p, obs(v))
    assert a.accept_cached(obs(v, prices[0], tick=11)) is None
    for price in prices[1:]:
        move = asyncio.run(a.respond(obs(v, price, tick=11)))
        assert (move.action, move.price) == ("accept", price)
    assert m.calls == 0
    assert a.accept_cached(obs(v, prices[1], tick=12)) is None
    changed = v.model_copy(update={"limit": limit + 1})
    assert a.accept_cached(obs(changed, prices[1], tick=11)) is None


def test_day_packages_use_worth_and_require_a_readable_valid_day():
    v = view(days=True)
    a = DuelAgent(v, Model(None), tick_decay=True)
    a.cache_plan(plan(days=0), obs(v))             # minimum worth: 90 - 40 = 50
    assert a.accept_cached(obs(v, 95, 5, tick=11)) is None  # worth 45, despite price inside band
    assert a.accept_cached(obs(v, 100, 5, tick=11)).action == "accept"  # worth 50
    for day in (None, -1, 11):
        assert a.accept_cached(obs(v, 100, day, tick=11)) is None
    unknown = v.model_copy(update={"days_meaning": None})
    a = DuelAgent(unknown, Model(None), tick_decay=True)
    a.cache_plan(plan(days=5), obs(unknown))
    assert a.accept_cached(obs(unknown, 110, 5, tick=11)) is None


def test_break_even_counts_silence_and_failure_risk():
    v = view()
    a = DuelAgent(v, Model(None), tick_decay=True)
    a.cache_plan(plan(next_tick_surplus=44), obs(v))
    assert a.accept_cached(obs(v, 80, tick=11)).meta["rule"] == "tick break-even"  # 40 >= .9 * 44
    a.cache_plan(plan(next_tick_surplus=45), obs(v))
    assert a.accept_cached(obs(v, 80, tick=11)) is None
    a.cache_plan(plan(next_tick_surplus=45, next_tick_deal_probability=0.9), obs(v))
    assert a.accept_cached(obs(v, 80, tick=11)) is not None
    assert a.accept_cached(obs(v, 39, tick=11)) is None
    text = ledger(obs(v, 80), tick_decay=True)
    assert "including silence" in text and "11.1%" in text and "costs nothing" not in text


def test_fresh_band_skips_negotiator():
    v = view()
    strategist, negotiator = Model(plan()), Model(None)
    a = DuelAgent(v, strategist, negotiator, tick_decay=True)
    assert asyncio.run(a.respond(obs(v, 95))).action == "accept"
    assert strategist.calls == 1 and negotiator.calls == 0


def test_four_concurrent_days_duels_finish_with_validated_targets_when_writer_hangs():
    async def run():
        agents = [DuelAgent(view(days=True), Model(plan(days=0), 0.01), Model(None, 10),
                    tick_decay=True, strategy_timeout_s=0.1, negotiation_timeout_s=0.03) for _ in range(4)]
        start = time.monotonic()
        moves = await asyncio.gather(*(a.respond(obs(a.view, 20, 0)) for a in agents))
        return time.monotonic() - start, moves
    elapsed, moves = asyncio.run(run())
    assert elapsed < 0.3
    assert all((m.action, m.price, m.days) == ("offer", 100, 0) and "TimeoutError" in m.meta["fallback"]
               for m in moves)


def test_runner_rechecks_each_tick_and_interrupts_model_for_an_authorized_offer(tmp_path):
    async def run():
        b = SimpleNamespace(duel_accept=lambda did: {"ok": True})
        r = DuelRunner(b, Model(None, 10), Model(None, 10), dry_run=False, log=Log(tmp_path),
                       decay=None, duel_ticks=12, poll_s=1, tick_decay=True)
        r.tick = 10
        raw = {"duel": 1, "role": "seller", "your_limit": 40, "status": "live", "deadline_tick": 18,
               "decay_per_round": 0.1, "rival_offer": {"price": 20}}
        mem = r.update(raw)
        mem.agent.cache_plan(plan(), r.observe(mem))
        mem.task = asyncio.create_task(r._decide(mem))
        await asyncio.sleep(0.01)
        r.update({**raw, "rival_offer": {"price": 95}})
        await r.interrupt_for_offer(mem)
        assert mem.task is None and r.due(mem)
        await r.decide(mem)
        assert mem.sent[-1].accept and mem.sent_tick == 10
        assert r.strategist.calls == 1 and r.negotiator.calls == 0
    asyncio.run(run())


def test_runner_whole_budget_shrinks_when_late_and_cancels_strategy(tmp_path):
    async def run():
        r = DuelRunner(SimpleNamespace(duel_say=lambda *a: {"ok": True}), Model(None, 10), Model(None, 10),
                       dry_run=False, log=Log(tmp_path), decay=None, duel_ticks=12, poll_s=1,
                       tick_decay=True, decision_timeout_s=0.05)
        r.tick, r.tick_seconds = 10, 15
        mem = r.update({"duel": 1, "role": "seller", "your_limit": 40, "status": "live",
                        "deadline_tick": 18})
        start = time.monotonic()
        await r.decide(mem)
        assert time.monotonic() - start < 0.3 and mem.sent
        r.tick_deadline = time.monotonic() + 1.02
        assert 0 <= r.decision_budget() <= 0.02
        r.tick_deadline = time.monotonic() + 0.5
        assert r.decision_budget() == 0
    asyncio.run(run())


def test_failover_gets_a_backup_inside_budget_and_never_launches_one_after_cancellation():
    async def run():
        primary, backup = Model(None, 10), Model(plan())
        f = Failover(primary, backup, timeout_s=0.01)
        assert (await f.parse(BandPlan, "", [])).parsed.target == 100
        assert backup.calls == 1
        f.timeout_s = 10
        with pytest.raises(TimeoutError):
            await asyncio.wait_for(f.parse(BandPlan, "", []), 0.01)
        assert backup.calls == 1 and f.failures == 2
    asyncio.run(run())


def test_warmup_matches_live_prefix_schema_and_effort_and_logs_cache_usage(monkeypatch):
    requests = []
    usage = SimpleNamespace(input_tokens=2, output_tokens=1, cache_creation_input_tokens=600,
                            cache_read_input_tokens=0)
    msg = SimpleNamespace(usage=usage, model="claude-opus-5-5", stop_reason="end_turn", parsed_output=plan())
    class API:
        async def create(self, **kw):
            requests.append(kw)
            return msg
        async def parse(self, **kw):
            requests.append(kw)
            return msg
    api = API()
    monkeypatch.setattr("engine.claude.anthropic.AsyncAnthropic",
                        lambda **kw: SimpleNamespace(messages=api, beta=SimpleNamespace(messages=api)))
    async def run():
        c = Claude()
        prefix = tick_prefix("strategist")
        warmed = await c.warmup(BandPlan, prefix)
        reply = await c.parse(BandPlan, prefix + CACHE_PREFIX_END + "private limit: 40", [])
        assert warmed["cached"] and reply.cache_creation_input_tokens == 600
    asyncio.run(run())
    warm, live = requests
    assert warm["system"][0] == live["system"][0]
    assert warm["max_tokens"] == 1 and warm["output_config"]["effort"] == live["output_config"]["effort"] == "low"
    assert warm["output_config"]["format"]["type"] == "json_schema"
    assert live["output_format"] is BandPlan
    assert "private limit" not in json.dumps(warm)
