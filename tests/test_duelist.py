"""Offline tests: a fake model and a fake game, no network."""
import asyncio
import json
from pathlib import Path

from agents.duelist.adapter import parse_duel
from agents.duelist.agent import BandPlan, Decision, DuelAgent, ledger, make_band
from agents.duelist.model import DuelView, Observation, Offer, Role, Turn
from agents.duelist.runner import DuelRunner, Log
from engine import LLMError, Reply

SELLER = DuelView(duel_id=1, role=Role.SELLER, limit=40, item="a card", decay=0.06, duel_ticks=12)
BUYER = DuelView(duel_id=2, role=Role.BUYER, limit=60, item="a card", decay=0.06, duel_ticks=12)


class FakeModel:
    """Answers the strategist with `plan` and the negotiator with `decisions` in turn."""
    label = "fake"

    def __init__(self, plan, *decisions):
        self.plan, self.decisions, self.seen = plan, list(decisions), []

    async def parse(self, schema, system, messages):
        self.seen.append((schema.__name__, system, messages))
        if schema is BandPlan:
            if isinstance(self.plan, Exception):
                raise self.plan
            return Reply(self.plan, 0.1, 10, 10, 0.0, "fake")
        return Reply(self.decisions.pop(0), 0.1, 10, 10, 0.0, "fake")


def plan(target, best, worst, days=None):
    return BandPlan(read="They moved.", target=target, best=best, worst=worst, days=days, angle="Stress rarity.")


def obs(view, rival=None, turns=(), left=8):
    return Observation(view=view, turns=list(turns), rival_offer=Offer(price=rival) if rival else None, tick=5,
                       ticks_left=left)


def respond(view, o, fake):
    return asyncio.run(DuelAgent(view, fake).respond(o))


def test_offer_inside_the_band_goes_out_as_is():
    fake = FakeModel(plan(70, 72, 68), Decision(action="offer", price=70, message="70 P, it's rare."))
    move = respond(SELLER, obs(SELLER, rival=30), fake)
    assert (move.action, move.price, move.days) == ("offer", 70, None)
    assert "vetoes" not in move.meta


def test_band_never_crosses_the_limit_and_rounds_toward_us():
    band = make_band(SELLER, plan(41, 45, 30))
    assert band.worst == 40 and band.best == 45
    band = make_band(BUYER, BandPlan(read="", target=59, best=50, worst=70, days=None, angle=""))
    assert band.worst == 60 and band.best == 50


def test_offer_past_the_limit_is_repaired_inside_the_band():
    bad = Decision(action="offer", price=35, message="35 P.")
    move = respond(SELLER, obs(SELLER, rival=30), FakeModel(plan(50, 52, 45), bad, bad))
    assert move.action == "offer" and 45 <= move.price <= 52 and move.meta["repaired"]


def test_writing_an_amount_past_the_limit_is_vetoed():
    leaky = Decision(action="offer", price=50, message="I won't go down to 30 P, but 50 P works.")
    clean = Decision(action="offer", price=50, message="50 P is fair for a rare.")
    move = respond(SELLER, obs(SELLER, rival=30), FakeModel(plan(50, 52, 45), leaky, clean))
    assert move.text == clean.message and move.meta["vetoes"]


def test_accept_needs_their_offer_inside_the_band():
    ok = respond(SELLER, obs(SELLER, rival=48), FakeModel(plan(50, 52, 47),
                                                           Decision(action="accept", price=48, message="Done.")))
    assert (ok.action, ok.price) == ("accept", 48)
    low = Decision(action="accept", price=44, message="Done.")
    move = respond(SELLER, obs(SELLER, rival=44), FakeModel(plan(50, 52, 47), low, low))
    assert move.action == "offer" and move.price >= 47


def test_never_accepts_past_the_limit_whatever_the_plan():
    # The plan's worst is clamped to the limit, so an offer of 35 can't pass the band check either.
    take = Decision(action="accept", price=35, message="Fine.")
    move = respond(SELLER, obs(SELLER, rival=35), FakeModel(plan(36, 38, 30), take, take))
    assert move.action != "accept"


def test_offer_worse_than_their_standing_offer_is_vetoed():
    worse = Decision(action="offer", price=46, message="46 P.")
    better = Decision(action="accept", price=48, message="Done.")
    move = respond(SELLER, obs(SELLER, rival=48), FakeModel(plan(46, 50, 45), worse, better))
    assert move.action == "accept" and "standing offer" in move.meta["vetoes"][0]


def test_strategist_failure_restates_our_last_offer():
    turns = [Turn(mine=True, text="60 P.", offer=Offer(price=60), tick=1)]
    move = respond(SELLER, obs(SELLER, rival=30, turns=turns), FakeModel(LLMError("down")))
    assert (move.action, move.price) == ("offer", 60) and "strategist" in move.meta["fallback"]


def test_days_come_from_the_strategist():
    view = SELLER.model_copy(update={"issues": ["price", "days"], "days_weight": 2})
    move = respond(view, obs(view, rival=30), FakeModel(plan(60, 62, 58, days=7),
                                                         Decision(action="offer", price=60, message="60 P, day 7.")))
    assert (move.price, move.days) == (60, 7)


def test_negotiator_never_sees_the_limit_and_prompts_are_filled():
    fake = FakeModel(plan(70, 72, 68), Decision(action="offer", price=70, message="70 P."))
    view = SELLER.model_copy(update={"limit": 37})
    respond(view, obs(view, rival=30), fake)
    (_, s_system, s_msgs), (_, n_system, n_msgs) = fake.seen
    assert "37 P" in s_system and "$" not in s_system and "$" not in n_system
    assert "37" not in n_system + json.dumps(n_msgs)
    assert n_msgs[-1]["role"] == "user"


def test_ledger_states_ticks_decay_and_gap():
    turns = [Turn(mine=True, offer=Offer(price=70), tick=1), Turn(mine=False, offer=Offer(price=25), tick=1),
             Turn(mine=False, offer=Offer(price=30), tick=2)]
    text = ledger(obs(SELLER, rival=30, turns=turns, left=4))
    assert "They have moved 5 P from their first offer." in text
    assert "Ticks left in the duel, including this one: 4 of 12." in text
    assert "6%" in text and "Gap between your last offer (70 P) and their standing offer (30 P): 40 P." in text
    assert "last tick" in ledger(obs(SELLER, rival=30, turns=turns, left=1))


def test_adapter_reads_a_plausible_payload():
    raw = {"id": 9, "status": "open", "role": "seller", "your_limit": 40, "rival": "Lynx",
           "rival_offer": {"price": 30}, "deadline": 112, "scenario": {"item": "a mug"}, "mystery": 1,
           "messages": [{"from": "you", "text": "70 P", "price": 70, "tick": 101},
                        {"from": "Lynx", "text": "30", "offer": {"price": 30}, "tick": 102}]}
    s = parse_duel(raw, team={"t05", "Team 5"}, tick=105, defaults={"decay": 0.06, "duel_ticks": 12})
    assert s.live and s.view.role is Role.SELLER and s.view.limit == 40 and s.view.item == "a mug"
    assert s.rival_offer == Offer(price=30) and s.ticks_left == 8
    assert [(t.mine, t.offer.price) for t in s.messages] == [(True, 70), (False, 30)]
    assert s.view.extra == {"mystery": 1} and s.view.decay == 0.06 and not s.problems


def test_adapter_reports_what_it_cannot_read():
    s = parse_duel({"id": 3, "status": "live"}, team=set(), tick=1, defaults={})
    assert s.view is None and s.problems


class FakeBazaar:
    def __init__(self):
        self.said, self.accepted = [], []

    def duel_say(self, did, text, price=None, days=None):
        self.said.append((did, text, price, days))
        return {"ok": True}

    def duel_accept(self, did):
        self.accepted.append(did)
        return {"ok": True}


def test_runner_sends_one_move_per_tick_and_waits_for_their_reply(tmp_path: Path):
    b = FakeBazaar()
    fake = FakeModel(plan(70, 72, 68), Decision(action="offer", price=70, message="70 P."))
    r = DuelRunner(b, fake, fake, dry_run=False, log=Log(tmp_path), decay=None, duel_ticks=12, poll_s=1)
    r.tick = 101
    raw = {"id": 9, "role": "seller", "your_limit": 40, "deadline": 112, "rival_offer": None}
    mem = r.update(raw)
    assert r.due(mem)
    asyncio.run(r.decide(mem))
    assert b.said == [(9, "70 P.", 70, None)]
    assert not r.due(mem)                          # same tick
    r.tick = 102
    mem = r.update(raw)
    assert not r.due(mem)                          # they haven't moved
    mem = r.update({**raw, "rival_offer": {"price": 30}})
    assert r.due(mem)
    obs_ = r.observe(mem)
    assert [(t.mine, t.offer.price) for t in obs_.turns] == [(True, 70), (False, 30)]


def test_records_keep_the_whole_duel_and_review_reads_it(tmp_path: Path):
    from agents.duelist.records import Records, review, summary
    b = FakeBazaar()
    fake = FakeModel(plan(70, 72, 68), Decision(action="offer", price=70, message="70 P."))
    rec = Records(tmp_path / "duels")
    r = DuelRunner(b, fake, fake, dry_run=False, log=Log(tmp_path), decay=None, duel_ticks=12, poll_s=1,
                   records=rec)
    r.tick = 101
    raw = {"id": 9, "role": "seller", "your_limit": 40, "deadline": 112, "rival_offer": None, "rival": "Fox"}
    mem = r.update(raw)
    asyncio.run(r.decide(mem))
    r.tick = 102
    r.update({**raw, "rival_offer": {"price": 30}})
    rec.save(9, done={**raw, "status": "deal", "price": 55})
    d = rec.load(9)
    assert [p["tick"] for p in d["payloads"]] == [101, 102]
    assert len(d["decisions"]) == 1 and d["sent"][0]["move"]["price"] == 70
    assert d["view"]["limit"] == 40 and rec.finished(9)
    row = summary(d)
    assert (row["rival"], row["role"], row["our_first"], row["price"], row["surplus"]) == ("Fox", "seller", 70, 55, 15)
    assert "| 9 |" in review(rec)
    assert rec.add_feed([{"id": 1, "type": "duel.deal"}, {"id": 2, "type": "offer.listed"}]) == 1
    assert rec.add_feed([{"id": 1, "type": "duel.deal"}]) == 0
