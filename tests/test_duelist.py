"""Offline tests: a fake model and a fake game, no network."""
import asyncio
import json
from pathlib import Path

from agents.duelist.adapter import parse_duel
from agents.duelist.agent import BandPlan, Decision, DuelAgent, Move, ledger, make_band, their_offers
from agents.duelist.days import read_days
from agents.duelist.model import DuelView, Observation, Offer, Role, Turn
from agents.duelist.records import Records, summary
from agents.duelist.runner import DuelRunner, Log
from engine import LLMError, Reply

DUELS = Path(__file__).resolve().parents[1] / "docs" / "duels"
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


def test_strategist_failure_concedes_toward_our_limit():
    turns = [Turn(mine=True, text="60 P.", offer=Offer(price=60), tick=1)]
    move = respond(SELLER, obs(SELLER, rival=30, turns=turns, left=8), FakeModel(LLMError("down")))
    assert move.action == "offer" and 40 <= move.price < 60 and "strategist" in move.meta["fallback"]
    move = respond(SELLER, obs(SELLER, rival=30, turns=turns, left=1), FakeModel(LLMError("down")))
    assert (move.action, move.price) == ("offer", 40)          # last tick: our limit, never past it


def test_fallback_accepts_their_offer_once_the_concession_meets_it():
    turns = [Turn(mine=True, text="50 P.", offer=Offer(price=50), tick=1)]
    move = respond(SELLER, obs(SELLER, rival=48, turns=turns, left=3), FakeModel(LLMError("down")))
    assert (move.action, move.price) == ("accept", 48)
    move = respond(SELLER, obs(SELLER, rival=35, turns=turns, left=1), FakeModel(LLMError("down")))
    assert move.action == "offer" and move.price == 40          # their 35 is past our limit: never accept it
    move = respond(BUYER, obs(BUYER, rival=55, turns=[Turn(mine=True, offer=Offer(price=40), tick=1)], left=1),
                   FakeModel(LLMError("down")))
    assert (move.action, move.price) == ("accept", 55)


def test_failover_uses_the_backup_and_skips_a_failing_primary():
    from engine.failover import Failover
    good = FakeModel(plan(70, 72, 68), Decision(action="offer", price=70, message="70 P."))
    bad = FakeModel(LLMError("overloaded"))
    m = Failover(bad, good, trip=1, cooldown_s=60)
    move = respond(SELLER, obs(SELLER, rival=30), m)
    assert (move.action, move.price) == ("offer", 70) and "fallback" not in move.meta
    assert len(bad.seen) == 1                                   # tripped: the negotiator call skipped it


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
    assert s.rival_offer == Offer(price=30) and s.ticks_left == 7
    assert [(t.mine, t.offer.price) for t in s.messages] == [(True, 70), (False, 30)]
    assert s.view.extra == {"mystery": 1} and s.view.decay == 0.06 and not s.problems


def test_adapter_reports_what_it_cannot_read():
    s = parse_duel({"id": 3, "status": "live"}, team=set(), tick=1, defaults={})
    assert s.view is None and s.problems


def recorded(duel: int, tick: int) -> dict:
    """The game's payload of one of Friday's practice duels, as we last saw it on or before `tick`."""
    d = json.loads((DUELS / f"duel-{duel}.json").read_text())
    return next(p["raw"] for p in reversed(d["payloads"]) if p["tick"] <= tick)


def test_ticks_left_counts_the_ticks_we_can_still_move_on():
    # Duel 114 opened on tick 144 in a 12-tick session; its deadline_tick is 156, the tick it closed on.
    raw = recorded(114, 144)
    left = lambda tick: parse_duel(raw, team=set(), tick=tick, defaults={}).ticks_left  # noqa: E731
    assert (left(144), left(155)) == (12, 1)


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


def test_the_sweep_saves_only_a_duel_that_is_over(tmp_path: Path):
    # Sat 09:13: the done list also listed six practice duels frozen as `live`; the sweep saved them as done, so
    # once over, their real result would never have been saved (`finished` was true).
    from agents.duelist.records import Records
    rec = Records(tmp_path / "duels")
    live = {"duel": 116, "session": 1, "status": "live", "role": "buyer", "your_limit": 140, "deadline_tick": 168}
    over = {**live, "status": "no_deal", "result": 0}
    b = FakeBazaar()
    b.done = [live]
    b.duels = lambda done=False: {"duels": b.done if done else []}
    b.feed = lambda limit=200: {"events": []}
    b.me = lambda: {"score": {}}
    r = DuelRunner(b, FakeModel(plan(67, 66, 68)), FakeModel(plan(67, 66, 68)), dry_run=False, log=Log(tmp_path),
                   decay=None, duel_ticks=None, poll_s=1, records=rec)
    asyncio.run(r.sweep())
    assert rec.load(116) is None
    rec.save(116, done=live)                            # a record from before this fix
    assert not rec.finished(116)
    b.done = [over]
    asyncio.run(r.sweep())
    assert rec.load(116)["done"]["status"] == "no_deal" and rec.finished(116)


def runner(b, model, tmp_path: Path, duel_ticks: int | None = None) -> DuelRunner:
    return DuelRunner(b, model, model, dry_run=False, log=Log(tmp_path), decay=None, duel_ticks=duel_ticks, poll_s=1)


def answered(r: DuelRunner, raw: dict, tick: int):
    """The runner first reading a duel on `tick`, as after a restart: our messages in the payload count as sent."""
    r.tick = tick
    return r.update(raw)


def test_with_no_duel_live_the_loop_polls_the_shared_key_less_often(tmp_path: Path):
    # Friday's runner read clock + duels every 2 s all night: 1 of the team key's 5 requests a second.
    r = runner(FakeBazaar(), FakeModel(plan(67, 66, 68)), tmp_path)
    r.poll_s, r.tick_seconds = 2, 30.0
    assert r.wait_s([]) == 10.0                         # Saturday: every 10 s while nothing is live
    r.tick_seconds = 15.0
    assert r.wait_s([]) == 5.0                          # Sunday: a third of a tick, seen early in its first tick
    raw = recorded(181, 141)
    assert r.wait_s([raw]) == 2                         # a duel is live: every poll_s
    answered(r, raw, 141)
    assert r.wait_s([]) == 2                            # gone from the list but not finished yet: every poll_s


def test_duel_181_accepts_their_offer_inside_our_limit_before_the_deadline(tmp_path: Path):
    # Fri: buyer, value 85. Their 73 stood from tick 141, we sat at 67, nobody moved again, and the duel closed
    # on tick 144 with no deal: 12 x 0.94^2 = 10.6 points lost.
    b = FakeBazaar()
    fake = FakeModel(plan(67, 66, 68))                 # no decisions: a negotiator call would fail
    r = runner(b, fake, tmp_path)
    raw = recorded(181, 141)
    mem = answered(r, raw, 141)
    assert mem.snap.ticks_left == 3 and not r.due(mem)  # we answered on 141
    r.tick = 142
    mem = r.update(raw)                                 # they haven't moved
    assert r.due(mem)
    asyncio.run(r.decide(mem))
    assert b.accepted == [181] and fake.seen == []      # code accepted 73 on 142, no model asked
    assert not r.due(mem)


def test_when_our_acceptance_must_wait_we_offer_their_price_if_that_adds_no_round(tmp_path: Path):
    # 181 on 142: we have sent 6 messages, they 2, so offering their 73 leaves rounds = min at 2.
    b = FakeBazaar()
    r = runner(b, FakeModel(plan(67, 66, 68)), tmp_path)
    raw = recorded(181, 141)
    answered(r, raw, 141)
    r.tick = 142
    mem = r.update(raw)
    r.accepted_tick = 142                               # another duel took the team's acceptance on 142
    asyncio.run(r.decide(mem))
    assert b.accepted == [] and b.said[-1][0] == 181 and b.said[-1][2] == 73 and not r.due(mem)
    r.tick = 143                                        # they didn't take it: our acceptance is free again
    mem = r.update(raw)
    assert r.due(mem)
    asyncio.run(r.decide(mem))
    assert b.accepted == [181]                          # 143: the last tick it can still land on


def test_when_their_price_would_add_a_round_our_acceptance_waits_a_tick(tmp_path: Path):
    # 200 on 157 (we sell at cost 68): their 87 then 102, our 104. Gap 2: code accepts 102. Offering 102
    # instead would make it 2 priced offers each, 2 rounds: 34 x 0.94^2 = 30.0 instead of 32.0.
    b = FakeBazaar()
    r = runner(b, FakeModel(plan(104, 105, 103)), tmp_path)
    mem = answered(r, recorded(200, 157), 157)
    assert r.closing(mem) == "small gap"
    r.accepted_tick = 157
    asyncio.run(r.decide(mem))
    assert b.accepted == b.said == [] and mem.pending and not r.due(mem)   # held, not retried on the same tick
    r.tick = 158
    mem = r.update(recorded(200, 157))
    assert r.due(mem)
    asyncio.run(r.decide(mem))
    assert b.accepted == [200]


def test_a_gap_smaller_than_one_more_round_is_closed_by_accepting(tmp_path: Path):
    # 199 on 156 (we buy, value 150): their 97 against our 96, surplus 53: one more round risks ~3 P, the gap
    # is 1. Friday's models accepted too; now code does it without asking them.
    b = FakeBazaar()
    fake = FakeModel(plan(96, 95, 97))
    r = runner(b, fake, tmp_path)
    mem = answered(r, recorded(199, 156), 156)
    assert r.due(mem) and r.closing(mem) == "small gap"
    asyncio.run(r.decide(mem))
    assert b.accepted == [199] and fake.seen == []
    # Had our 96 come after their 97, they'd get the tick to take it.
    raw = recorded(199, 156)
    r1 = runner(FakeBazaar(), fake, tmp_path)
    mem = answered(r1, {**raw, "messages": [*raw["messages"][:-2], raw["messages"][-1], raw["messages"][-2]]}, 156)
    assert r1.closing(mem) is None
    # 227 on 159 (we sell at cost 130): their 152 against our 156, surplus 22: a gap of 4 is worth more than
    # a round (~2.8 P), so the models keep it.
    r2 = runner(FakeBazaar(), fake, tmp_path)
    mem = answered(r2, recorded(227, 159), 159)
    assert r2.closing(mem) is None


def silent_duel_31(tmp_path: Path):
    """Duel 31 (12 ticks): we sell at cost 111, opened at 165 on tick 120; the rival never spoke; deadline 132."""
    b, fake = FakeBazaar(), FakeModel(plan(150, 155, 145))
    r = runner(b, fake, tmp_path, duel_ticks=12)
    raw = recorded(31, 120)
    answered(r, raw, 120)
    return r, b, fake, raw


def play(r: DuelRunner, b: FakeBazaar, raw: dict, tick: int) -> dict:
    """One tick: read the duel, decide if due, and put what we said into the payload as the game would."""
    r.tick = tick
    mem, sent = r.update(raw), len(b.said)
    if r.due(mem):
        asyncio.run(r.decide(mem))
    if len(b.said) > sent:
        _, text, price, days = b.said[-1]
        raw = {**raw, "messages": [*raw["messages"], {"tick": tick, "from": "you", "text": text, "price": price,
                                                      "days": days}],
               "your_offer": {"price": price, "tick": tick, "days": days}}
    return raw


def test_a_silent_rival_gets_our_offer_walked_down_to_a_floor_by_code(tmp_path: Path):
    r, b, fake, raw = silent_duel_31(tmp_path)
    for tick in range(121, 132):
        raw = play(r, b, raw, tick)
    steps = [(m["tick"], m["price"]) for m in raw["messages"][1:]]
    # From 6 ticks left (tick 126) to 2 left (130): 165 -> floor 111 + 0.3 x 54 = 127.2, rounded up to 128.
    assert steps == [(126, 158), (127, 150), (128, 143), (129, 135), (130, 128)]
    assert fake.seen == []                              # no model asked


def test_a_silent_rival_that_speaks_goes_back_to_the_models(tmp_path: Path):
    r, b, fake, raw = silent_duel_31(tmp_path)
    for tick in range(121, 128):
        raw = play(r, b, raw, tick)                     # 158 on 126, 150 on 127
    raw = {**raw, "rival_offer": {"price": 120},
           "messages": [*raw["messages"], {"tick": 128, "from": "Rival Sol", "text": "120.", "price": 120}]}
    r.tick = 128
    mem = r.update(raw)
    assert r.due(mem) and not r.silent_rival(mem)
    asyncio.run(r.decide(mem))
    assert fake.seen and fake.seen[0][0] == "BandPlan"  # the strategist plays it again


def test_a_silent_rival_in_a_days_duel_walks_on_price_and_keeps_our_day(tmp_path: Path):
    # Duel 31 as a days duel: our opener 165 on day 4, each day later costing us 2, so day 4 costs 8 and our
    # limit on it is 119: floor 119 + 0.3 x 46 = 132.8, rounded up to 133.
    b, fake = FakeBazaar(), FakeModel(plan(150, 155, 145, days=4))
    r = runner(b, fake, tmp_path, duel_ticks=12)
    raw = recorded(31, 120)
    raw = {**raw, "issues": ["price", "days"], "your_days_weight": 2, "days_meaning": "each day later costs you 2 P",
           "messages": [{**raw["messages"][0], "days": 4}], "your_offer": {**raw["your_offer"], "days": 4}}
    answered(r, raw, 120)
    for tick in range(121, 132):
        raw = play(r, b, raw, tick)
    steps = [(m["tick"], m["price"], m["days"]) for m in raw["messages"][1:]]
    assert steps == [(126, 159, 4), (127, 153, 4), (128, 146, 4), (129, 140, 4), (130, 133, 4)]
    assert fake.seen == []


def test_a_silent_rival_in_a_days_duel_we_cannot_read_stays_with_the_models(tmp_path: Path):
    r = runner(FakeBazaar(), FakeModel(plan(150, 155, 145, days=5)), tmp_path, duel_ticks=12)
    raw = {**recorded(31, 120), "issues": ["price", "days"], "your_days_weight": {"mystery": 1}}
    mem = answered(r, raw, 120)
    assert not r.silent_rival(mem)
    r.tick = 126
    assert not r.due(r.update(raw))                     # no schedule: the models decide in the last 3 ticks
    r.tick = 129
    assert r.due(r.update(raw))


def test_a_standoff_is_broken_after_three_still_ticks(tmp_path: Path):
    # Fri: duels 103/104 sat still from tick 146 to their deadline on 156, each side waiting for the other.
    r = runner(FakeBazaar(), FakeModel(plan(90, 92, 89)), tmp_path)
    raw = recorded(103, 146)
    answered(r, raw, 146)
    r.tick = 148
    assert not r.due(r.update(raw))
    r.tick = 149
    mem = r.update(raw)
    assert r.due(mem) and mem.snap.ticks_left == 7
    assert "Neither side has moved for 3 ticks" in ledger(r.observe(mem))


def test_offers_inside_our_limit_ending_together_are_accepted_one_per_tick_biggest_first(tmp_path: Path):
    # Duels I runs 3 at a time and a wave ends together; the team accepts one offer per tick.
    b = FakeBazaar()
    r = runner(b, FakeModel(plan(60, 58, 62)), tmp_path)
    raws = {did: {"duel": did, "status": "live", "role": "buyer", "your_limit": 100, "deadline_tick": 116,
                  "rival_offer": {"price": price},
                  "messages": [{"tick": 100, "from": "you", "text": "60 P.", "price": 60},
                               {"tick": 101, "from": "Rival", "text": "No.", "price": price}]}
            for did, price in ((1, 90), (2, 70), (3, 80))}
    for raw in raws.values():
        answered(r, raw, 111)
    assert r.closer() is None                           # 5 ticks left: all three can still wait
    order = []
    for tick in (112, 113, 114, 115):
        r.tick = tick
        for did, raw in raws.items():
            r.update({**raw, "status": "deal"} if did in b.accepted else raw)
        if (c := r.closer()) is not None:
            asyncio.run(r.decide(c[0]))
            order.append((tick, b.accepted[-1], c[1]))
    assert order == [(112, 2, "deadline"), (113, 3, "deadline"), (114, 1, "deadline")]   # surplus 30, 20, 10


def days_duel(*, weight=2, meaning="each day later costs you 2 P", rival=None, messages=(), deadline=116) -> dict:
    """A Duels II payload as RULES.md describes it (never seen yet): we buy at value 100, 8% per round."""
    return {"duel": 7, "session": 3, "status": "live", "role": "buyer", "your_limit": 100, "deadline_tick": deadline,
            "issues": ["price", "days"], "your_days_weight": weight, "days_meaning": meaning, "rival": "Rival Sol",
            "decay_per_round": 0.08, "rival_offer": rival, "messages": list(messages)}


OURS_ON_DAY_0 = [{"tick": 100, "from": "you", "text": "60 P, day 0.", "price": 60, "days": 0}]


def test_code_accepts_a_days_duel_on_the_whole_package_never_on_price_alone(tmp_path: Path):
    # 95 is inside our 100 on price, but day 5 costs us 10: the package is worth -5.
    r = runner(FakeBazaar(), FakeModel(plan(60, 58, 62)), tmp_path)
    answered(r, days_duel(rival={"price": 95, "days": 5}, messages=OURS_ON_DAY_0), 114)
    assert r.closer() is None
    # 70 on day 3 is worth 30 - 6 = 24: accepted by the deadline rule, no model asked.
    b, fake = FakeBazaar(), FakeModel(plan(60, 58, 62))
    r = runner(b, fake, tmp_path)
    mem = answered(r, days_duel(rival={"price": 70, "days": 3}, messages=OURS_ON_DAY_0), 114)
    assert r.closing(mem) == "deadline"
    asyncio.run(r.decide(mem))
    assert b.accepted == [7] and fake.seen == []
    # A weight we can't read: the models keep it.
    r = runner(FakeBazaar(), FakeModel(plan(60, 58, 62)), tmp_path)
    answered(r, days_duel(weight={"mystery": 1}, rival={"price": 70, "days": 3}, messages=OURS_ON_DAY_0), 114)
    assert r.closer() is None


def test_when_our_acceptance_must_wait_in_a_days_duel_we_offer_their_whole_package(tmp_path: Path):
    b = FakeBazaar()
    r = runner(b, FakeModel(plan(60, 58, 62)), tmp_path)
    mem = answered(r, days_duel(rival={"price": 70, "days": 3}, messages=OURS_ON_DAY_0), 114)
    r.accepted_tick = 114                               # another duel took the team's acceptance
    asyncio.run(r.decide(mem))
    assert b.accepted == [] and b.said[-1][2:] == (70, 3) and "day 3" in b.said[-1][1]


def test_a_small_gap_in_a_days_duel_counts_the_day(tmp_path: Path):
    def gap(their_day: int) -> str | None:
        msgs = [{"tick": 112, "from": "you", "text": "70 P, day 0.", "price": 70, "days": 0},
                {"tick": 113, "from": "Rival Sol", "text": "71.", "price": 71, "days": their_day}]
        r = runner(FakeBazaar(), FakeModel(plan(60, 58, 62)), tmp_path)
        return r.closing(answered(r, days_duel(deadline=130, rival={"price": 71, "days": their_day},
                                               messages=msgs), 114))
    assert gap(0) == "small gap"                        # 1 P apart on the same day
    assert gap(4) is None                               # 1 P apart on price, but day 4 costs us 8 more


def test_day_weights_are_read_as_a_number_a_list_or_a_dict():
    later = read_days(2, "each day later costs you 2 P")
    assert later.sure and later.best == 0 and later(3) == -6 and later(None) == -20
    assert read_days(2, "each day earlier costs you 2 P").best == 10
    assert read_days(2, "you prefer early delivery").best == 0
    assert read_days(2, "Days run from 0 (soonest) to 10 (latest); you lose your weight per day of delay").best == 0
    assert read_days(-1.5).best == 0 and read_days(-1.5)(2) == -3     # a negative weight per day: early is worth more
    guess = read_days(2)                                # positive, no words: which way is a guess
    assert not guess.sure and guess.best == 5 and guess(5) == -10 and guess(0) == guess(10) == -20
    assert read_days(0)(7) == 0
    assert read_days(list(range(11))).values == tuple(float(d - 10) for d in range(11))
    assert read_days({str(d): 10 - d for d in range(11)}).best == 0
    assert read_days({"per_day": 2, "prefers": "late"})(8) == -4
    assert read_days({"cost_per_day": 2, "prefers": "early"})(1) == -2
    assert read_days({"best_day": 3, "per_day": 1.5})(5) == -3
    assert read_days("2 P per day later").best == 10
    for unknown in ({"mystery": 1}, [1, 2], "soon", None, True):
        assert read_days(unknown) is None


def test_adapter_reads_a_days_payload_with_the_day_of_every_offer():
    raw = days_duel(rival={"id": 5, "price": 80, "days": 2, "tick": 101},
                    messages=[OURS_ON_DAY_0[0], {"tick": 101, "from": "Rival Sol", "text": "80, day 2.",
                                                 "offer": {"price": 80, "days": 2}}])
    s = parse_duel(raw, team=set(), tick=110, defaults={})
    assert s.view.has_days and s.view.days_meaning == "each day later costs you 2 P" and s.view.day_values.best == 0
    assert [t.offer for t in s.messages] == [Offer(price=60, days=0), Offer(price=80, days=2)]
    o = Observation(view=s.view, turns=s.messages, rival_offer=s.rival_offer, tick=110, ticks_left=s.ticks_left)
    assert their_offers(o) == [Offer(price=80, days=2)]   # the standing offer is not a second one


DAYS_BUYER = BUYER.model_copy(update={"limit": 100, "decay": 0.08, "issues": ["price", "days"], "days_weight": 2,
                                      "days_meaning": "each day later costs you 2 P"})


def test_the_limit_is_checked_on_the_whole_package():
    v = DAYS_BUYER
    assert make_band(v, plan(95, 85, 99), days=5) == make_band(v, plan(90, 85, 90), days=5)   # day 5: limit 90
    agent = DuelAgent(v, FakeModel(plan(60, 58, 62)))
    o = Observation(view=v, turns=[Turn(mine=True, offer=Offer(price=60, days=5), tick=1)], tick=2, ticks_left=8)
    move = agent.final(Move("offer", "95 P, day 5.", price=95, days=5), o)       # inside 100, but -5 with day 5
    assert move.action == "offer" and move.price <= 90 and move.days == 5 and move.meta["fallback"]
    move = agent.final(Move("offer", "70 P.", price=70), o)                      # no day: refused by the game
    assert move.days == 5 and move.meta["fallback"]
    bad = o.model_copy(update={"rival_offer": Offer(price=95, days=6)})
    assert agent.final(Move("accept", "Done.", price=95), bad).action != "accept"
    good = o.model_copy(update={"rival_offer": Offer(price=85, days=2)})
    assert agent.final(Move("accept", "Done.", price=85), good).action == "accept"


def test_the_strategist_sees_what_each_day_costs_and_the_negotiator_does_not():
    v = DAYS_BUYER
    fake = FakeModel(plan(80, 78, 85, days=1), Decision(action="offer", price=80, message="80 P, day 1."))
    turns = [Turn(mine=True, offer=Offer(price=60, days=0), tick=1), Turn(mine=False, offer=Offer(price=95, days=6),
                                                                          tick=2)]
    move = respond(v, Observation(view=v, turns=turns, rival_offer=Offer(price=95, days=6), tick=3, ticks_left=8),
                   fake)
    assert (move.action, move.price, move.days) == ("offer", 80, 1)
    (_, s_system, s_msgs), (_, n_system, n_msgs) = fake.seen
    assert "day 0: 0 P, day 1: 2 P, day 2: 4 P" in s_system and "best day (day 0)" in s_system
    assert "each day later costs you 2 P" in s_system
    prompt = s_msgs[0]["content"]
    assert "Their standing offer: 95 P (day 6) (past your limit, counting what the day costs you)." in prompt
    assert "your last offer, day 0: 0 P; their standing offer, day 6: 12 P" in prompt
    assert "100" not in n_system + json.dumps(n_msgs) and "day 1: 2 P" not in n_system


def test_decay_and_rounds_come_from_the_duel_itself():
    s = parse_duel(recorded(181, 141), team=set(), tick=141, defaults={"decay": 0.08})
    assert s.view.decay == 0.06 and s.rounds == 2       # decay_per_round, not the next session's 8%
    assert "decay_per_round" not in s.view.extra and "days_meaning" not in s.view.extra
    assert s.view.days_meaning is None                 # read into the view, null on price only


def test_session_params_come_from_the_feed_by_the_duels_own_session(tmp_path: Path):
    rec = Records(tmp_path / "duels")
    rec.add_feed([{"id": 1, "type": "duels.scheduled", "payload": {"session": 2, "name": "Duels I",
                                                                   "duel_ticks": 16, "decay": 0.06}}])
    r = DuelRunner(FakeBazaar(), FakeModel(plan(60, 58, 62)), FakeModel(plan(60, 58, 62)), dry_run=False,
                   log=Log(tmp_path), decay=None, duel_ticks=None, poll_s=1, records=rec)
    r.tick = 141
    mem = r.update({**recorded(181, 141), "session": 2})
    assert mem.agent.view.duel_ticks == 16 and rec.load(181)["session"]["name"] == "Duels I"
    r.learn_sessions([{"id": 2, "type": "duels.scheduled", "payload": {"session": 3, "name": "Duels II"}}])
    assert r.sessions[3]["name"] == "Duels II"


def test_review_predicts_each_deals_result_from_our_reading():
    recs = Records(DUELS)
    sessions = recs.sessions()
    deals = [row for row in (summary(r, sessions) for r in recs.all()) if row["status"] == "deal"]
    # Friday 11 deals, more as the records grow (Sat: the practice duels frozen overnight); price only so far
    assert len(deals) >= 11 and all(row["pred"] == row["points"] for row in deals)
    # A days deal: bought at 70 on day 3 after 2 rounds at 8%, each day later costing 2: (30 - 6) x 0.92^2.
    row = summary({"duel": 7, "view": DAYS_BUYER.model_dump(),
                   "done": {"status": "deal", "issues": ["price", "days"], "price": 70, "days": 3, "rounds": 2,
                            "decay_per_round": 0.08, "result": 20.3}})
    assert (row["day"], row["points"], row["pred"]) == (3, 20.3, 20.3)


def test_review_names_fridays_practice_from_the_feed():
    recs = Records(DUELS)
    row = summary(recs.load(181), recs.sessions())
    assert row["session"] == "Practice duels"            # the record itself says "Duels I"


def test_a_restart_waits_like_before_instead_of_resending(tmp_path: Path):
    # Duel 181, tick 137: a restart re-sent our standing 54 because a fresh process saw nothing sent.
    raw = recorded(181, 137)
    raw = {**raw, "messages": [m for m in raw["messages"] if m["tick"] < 137]}   # as read before we spoke on 137
    r = runner(FakeBazaar(), FakeModel(plan(54, 53, 55)), tmp_path, duel_ticks=12)   # 7 left: no silent step yet
    mem = answered(r, raw, 137)
    assert [t.offer.price for t in mem.sent] == [50, 50, 54] and not r.due(mem)


def test_a_message_we_did_not_send_is_flagged(tmp_path: Path, capsys):
    r = runner(FakeBazaar(), FakeModel(plan(67, 66, 68)), tmp_path)
    raw = recorded(181, 141)
    answered(r, {**raw, "messages": raw["messages"][:-1]}, 141)
    r.update(raw)                                        # our 67 on 141 came from somewhere else
    assert "another duelist" in capsys.readouterr().out


def test_ledger_counts_rounds_and_prices_one_more(tmp_path: Path):
    r = runner(FakeBazaar(), FakeModel(plan(67, 66, 68)), tmp_path)
    text = ledger(r.observe(answered(r, recorded(181, 141), 141)))
    assert "Their offers so far: 81 P, 73 P\n" in text                  # the standing offer is not a third one
    assert "Messages sent so far, priced or not: 6 by your side, 2 by theirs." in text
    assert "Rounds so far: 2, the smaller of the two sides' message counts" in text
    assert "adds no round by itself" in text and "worth about 11 P" in text   # 12 x 0.94^2
    text = ledger(r.observe(answered(r, recorded(200, 157), 157)))      # 87, our 104, their 102
    assert "Any message your side sends now adds a round" in text


def test_a_second_duelist_on_one_machine_refuses_to_start(tmp_path: Path):
    import pytest
    from agents.duelist.__main__ import ALREADY_RUNNING, single_instance
    held = single_instance(tmp_path)
    with pytest.raises(SystemExit) as e:
        single_instance(tmp_path)
    assert e.value.code == ALREADY_RUNNING
    held.close()
    single_instance(tmp_path).close()                   # free again once the first one is gone


def repeating(raw: dict, rival: str, price: int, ticks: range) -> dict:
    """`raw` with the rival repeating its standing `price` once on each of `ticks`, as Saturday's holders did."""
    return {**raw, "messages": [*raw["messages"], *({"tick": t, "from": rival, "text": f"{price}?", "price": price}
                                                    for t in ticks)]}


def test_duel_277_a_hold_sends_nothing(tmp_path: Path):
    # 277 (we sell, cost 119): Rival Plata sent 118 every tick. Our three no-price "holding" messages on 166-168
    # each raised the game's rounds by one (rounds = min(our messages, theirs), priced or not).
    b = FakeBazaar()
    fake = FakeModel(plan(173, 175, 171), Decision(action="message", price=None, message="I'm staying at 173 P."),
                     Decision(action="offer", price=173, message="173 P stands."))
    r = runner(b, fake, tmp_path)
    base = recorded(277, 165)                           # our 173 on 165 is the last word
    mem = answered(r, base, 165)
    for tick in (166, 167):
        r.tick = tick
        assert not r.due(r.update(repeating(base, "Rival Plata", 118, range(166, tick + 1))))   # a repeat
    r.tick = 168                                        # their offer unchanged since 163, our last word on 165
    mem = r.update(repeating(base, "Rival Plata", 118, range(166, 169)))
    assert r.due(mem)
    asyncio.run(r.decide(mem))                          # the model says "message": a hold
    assert b.said == [] and not r.due(mem)
    for tick, due in ((169, False), (170, False), (171, True)):     # asked again 3 ticks after the hold
        r.tick = tick
        mem = r.update(repeating(base, "Rival Plata", 118, range(166, tick + 1)))
        assert r.due(mem) is due, tick
    asyncio.run(r.decide(mem))                          # an offer at our standing 173: a hold too
    assert b.said == []


def test_duel_278_does_not_answer_a_repeated_offer_every_tick(tmp_path: Path):
    # 278 (we buy, value 116): Rival Oro sent 111, inside our limit, every tick and never moved. We answered every
    # tick (80, 82, 82, 84, 84, 85, ...), 10 rounds, then took 111 anyway: 5 x 0.94^10 = 2.7. Holding in silence
    # and taking it at the deadline keeps rounds at 1: 5 x 0.94 = 4.7.
    b = FakeBazaar()
    fake = FakeModel(plan(80, 78, 82), *[Decision(action="offer", price=80, message="80 P.")] * 6)
    r = runner(b, fake, tmp_path)
    base = recorded(278, 165)                           # their 111, then our opener 80, both on 165
    answered(r, base, 165)
    asked = []
    for tick in range(166, 177):
        r.tick = tick
        mem = r.update(repeating(base, "Rival Oro", 111, range(166, tick + 1)))
        if r.due(mem):
            calls = len(fake.seen)
            asyncio.run(r.decide(mem))
            asked += [tick] if len(fake.seen) > calls else []
        if b.accepted:
            break
    assert b.said == []                                 # never answered the repeats: our messages stay at 1
    assert asked == [168, 171, 174]                     # the hold breaker every 3 still ticks, then the deadline
    assert b.accepted == [278] and r.tick == 175        # code took 111 with 2 ticks left


def test_their_price_counts_every_message_as_a_round(tmp_path: Path):
    r = runner(FakeBazaar(), FakeModel(plan(80, 78, 82)), tmp_path)
    accept = Move("accept", "Agreed.", price=111)
    base = recorded(278, 165)                           # one message each: offering 111 adds no round
    assert r.their_price(answered(r, base, 165), accept).price == 111
    chat = {**base, "messages": [*base["messages"], {"tick": 165, "from": "Rival Oro", "text": "Well?", "price": None}]}
    r2 = runner(FakeBazaar(), FakeModel(plan(80, 78, 82)), tmp_path)
    assert r2.their_price(answered(r2, chat, 165), accept) is None   # their no-price message counts: 1 < 2


def test_a_plan_that_holds_sends_nothing_even_when_the_negotiator_drifts(tmp_path: Path):
    # Dani's 10:16 audit: the strategist holds (target = our standing 70) but the negotiator picks 68 from the
    # band; 68 would be sent and cost a round for 2 P (the 278 pattern). Code keeps our 70, so the runner holds.
    turns = [Turn(mine=True, offer=Offer(price=70), tick=1), Turn(mine=False, offer=Offer(price=30), tick=2)]
    drift = Decision(action="offer", price=68, message="68 P, final.")
    move = respond(SELLER, obs(SELLER, rival=30, turns=turns), FakeModel(plan(70, 72, 67), drift))
    assert (move.action, move.price, move.meta["rule"], move.meta["drafted"]) == ("offer", 70, "plan holds", 68)
    step = respond(SELLER, obs(SELLER, rival=30, turns=turns),
                   FakeModel(plan(58, 60, 56), Decision(action="offer", price=59, message="59 P.")))
    assert step.price == 59 and "rule" not in step.meta          # a planned step goes out as drafted
    take = respond(SELLER, obs(SELLER, rival=69, turns=turns),
                   FakeModel(plan(70, 72, 68), Decision(action="accept", price=69, message="Done.")))
    assert (take.action, take.price) == ("accept", 69)            # holding never blocks an accept


def mine(*prices, start=1):
    return [Turn(mine=True, offer=Offer(price=p), tick=start + i) for i, p in enumerate(prices)]


def theirs(price, tick, days=None):
    return Turn(mine=False, offer=Offer(price=price, days=days), tick=tick)


def drafted(view, turns, rival, target, left=8, days=None, action="offer"):
    """Our move when the strategist targets `target` and the negotiator drafts exactly that."""
    o = Observation(view=view, turns=turns, rival_offer=rival, tick=10, ticks_left=left)
    s = 1 if view.role is Role.SELLER else -1
    d = Decision(action=action, price=target if action == "offer" else rival.price, message=f"{target} P.")
    return respond(view, o, FakeModel(plan(target, target + 2 * s, target - 2 * s, days=days), d))


def test_277_a_step_of_a_point_or_two_is_held():
    # 277 (we sell, cost 119): our 175 against their 118, then 173, 160, 158, 156...: 11 rounds, 51% of the value.
    view = SELLER.model_copy(update={"limit": 119})
    turns = [*mine(175), theirs(118, 2)]
    small = drafted(view, turns, Offer(price=118), 173)       # gap 57: the least step worth a round is 3 P
    assert (small.price, small.meta["rule"], small.meta["drafted"]) == (175, "small step", 173)
    assert drafted(view, turns, Offer(price=118), 160).price == 160


def test_278_a_step_toward_a_holder_is_held():
    # 278 (we buy, value 116): our 82 against their 111, which they repeated every tick; we crept 82 → 84 → 85...
    view = BUYER.model_copy(update={"limit": 116})
    move = drafted(view, [*mine(82), theirs(111, 2)], Offer(price=111), 84)
    assert (move.price, move.meta["rule"]) == (82, "small step")


def test_a_fifth_offer_goes_out_normally():
    # Duels I: 71 P of our results came after our 4th offer, so there is no offer budget (§3.2).
    turns = [*mine(70), theirs(20, 1), *mine(64, 58, start=2), theirs(28, 3), *mine(52, start=4)]
    fifth = drafted(SELLER, turns, Offer(price=28), 46)       # their 28 stood when we sent 52
    assert fifth.price == 46 and "rule" not in fifth.meta
    assert drafted(SELLER, turns, Offer(price=28), 50).meta["rule"] == "small step"   # the 3 P floor stays


def test_the_round_rules_leave_accepts_openers_and_code_moves_alone(tmp_path: Path):
    turns = [*mine(70), theirs(42, 1), *mine(64, 58, 52, start=2)]          # four offers, their 42 unchanged
    take = drafted(SELLER, turns, Offer(price=42), 44, action="accept")
    assert (take.action, take.price) == ("accept", 42)
    assert drafted(SELLER, [], None, 70).price == 70                         # the opener
    o = Observation(view=SELLER, turns=turns, rival_offer=Offer(price=42), tick=10, ticks_left=6)
    assert DuelAgent(SELLER, FakeModel(plan(52, 54, 50))).close(o, "small gap").action == "accept"
    silent_obs = Observation(view=SELLER, turns=mine(70), tick=10, ticks_left=6)
    walk = DuelAgent(SELLER, FakeModel(plan(70, 72, 68))).silent_move(silent_obs)
    assert walk.action == "offer" and walk.price < 70 and walk.meta["rule"] == "silent rival"
    r = runner(FakeBazaar(), FakeModel(plan(80, 78, 82)), tmp_path)
    assert r.their_price(answered(r, recorded(278, 165), 165), Move("accept", "Agreed.", price=111)).price == 111


def test_a_day_only_concession_is_a_step_in_worth():
    view = SELLER.model_copy(update={"issues": ["price", "days"], "days_weight": 2,
                                     "days_meaning": "each day later costs you 2 P"})
    turns = [Turn(mine=True, offer=Offer(price=70, days=0), tick=1), theirs(30, 2, days=0)]
    rival = Offer(price=30, days=0)                           # gap 40 in worth: the least step is 3 P
    small = drafted(view, turns, rival, 70, days=1)           # day 1 costs us 2
    assert (small.price, small.days, small.meta["rule"]) == (70, 0, "small step")
    big = drafted(view, turns, rival, 70, days=3)             # day 3 costs us 6
    assert (big.price, big.days) == (70, 3)


def test_ledger_names_the_least_step_once_both_have_offered():
    assert "smallest step" not in ledger(obs(SELLER, turns=mine(70)))
    text = ledger(obs(SELLER, rival=30, turns=[*mine(70), theirs(30, 2)]))
    assert "- The smallest step worth sending now: 3 P (5% of the gap, at least 3 P)." in text
    assert "Offers your side has sent" not in text
    wide = ledger(obs(SELLER.model_copy(update={"limit": 100}), rival=100, turns=[*mine(300), theirs(100, 2)]))
    assert "- The smallest step worth sending now: 10 P (5% of the gap" in wide


# Duels II: the delivery day (docs/duels-1-review.md §3.1)

LATE_SELLER = SELLER.model_copy(update={"limit": 60, "issues": ["price", "days"], "days_weight": 1,
                                        "days_meaning": "each day later earns you 1 P"})
EARLY_BUYER = BUYER.model_copy(update={"limit": 100, "issues": ["price", "days"], "days_weight": -4})


def days_obs(view, ours, their, swings=(), left=10):
    turns = [Turn(mine=True, offer=Offer(price=ours[0], days=ours[1]), tick=1),
             Turn(mine=False, offer=Offer(price=their[0], days=their[1]), tick=2)]
    return Observation(view=view, turns=turns, rival_offer=Offer(price=their[0], days=their[1]), tick=3,
                       ticks_left=left, day_swings=list(swings))


def test_the_deck_example_seller_gives_the_day_buyer_holds_it():
    # The organisers' deck: the seller gains 1 per day later, the buyer loses 4 per day later.
    from agents.duelist.agent import day_read
    give = day_read(days_obs(LATE_SELLER, (95, 10), (70, 0)))     # a day-0 buyer: day 0 costs us 10
    assert (give.cost, give.level, give.call) == (10, "low", "give")
    text = ledger(days_obs(LATE_SELLER, (95, 10), (70, 0)))
    assert "- Their day: day 0. Against your best day (10) it costs you 10 P: it is on the other side from yours." in text
    assert "- If you give them day 0, ask at least 10 P more in price than your offer on day 10." in text
    assert "- By your day rules: give them day 0, with your price up by 10 P plus about 10 P more." in text
    hold = day_read(days_obs(EARLY_BUYER, (60, 0), (90, 10)))     # a day-10 seller: day 10 costs us 40
    assert (hold.cost, hold.level, hold.call) == (40, "high", "hold")
    assert "- By your day rules: hold your day 0; offer up to about 20 P in price to keep it." in \
        ledger(days_obs(EARLY_BUYER, (60, 0), (90, 10)))
    same = day_read(days_obs(EARLY_BUYER, (60, 0), (90, 0)))      # their day is ours
    assert (same.cost, same.call) == (0, "take")
    assert "ask at least" not in ledger(days_obs(EARLY_BUYER, (60, 0), (90, 0)))
    middle = day_read(days_obs(LATE_SELLER, (95, 10), (70, 4)))   # never settle on a middle day: give the end
    assert (middle.cost, middle.call, middle.give_day, middle.ask, middle.premium) == (6, "give", 0, 10, 10)


def test_the_day_weight_ranks_among_this_sessions_weights():
    from agents.duelist.agent import day_read, weight_level
    assert weight_level(20, [20]) == ("middle", None)             # too few seen: by size, 15 < 20 < 30
    assert weight_level(10, [10, 20, 40]) == ("low", 1)
    assert weight_level(20, [10, 20, 40]) == ("middle", 2)
    assert weight_level(40, [10, 20, 40]) == ("high", 3)
    assert weight_level(10, [5, 6, 7, 10]) == ("high", 4)         # a small weight can still be the session's largest
    r = day_read(days_obs(LATE_SELLER, (95, 10), (70, 0), swings=[2, 4, 5, 10]))
    assert (r.rank, r.seen, r.level, r.call) == (4, 4, "high", "hold")
    assert "rank 4 of 4 among the day weights seen this session (1 = the lowest)" in \
        ledger(days_obs(LATE_SELLER, (95, 10), (70, 0), swings=[2, 4, 5, 10]))
    r = day_read(days_obs(LATE_SELLER, (95, 10), (70, 0), swings=[10, 20, 30]))
    assert (r.rank, r.level, r.call) == (1, "low", "give")
    unsure = SELLER.model_copy(update={"issues": ["price", "days"], "days_weight": 2})
    assert day_read(days_obs(unsure, (70, 5), (50, 0))).call == "hold"   # a guessed direction never gives first


def test_a_day_swap_that_keeps_our_worth_is_sent():
    # We give a day-0 buyer its day at our 95 + 10: worth the same to us, so it is no concession.
    turns = [Turn(mine=True, offer=Offer(price=95, days=10), tick=1), theirs(70, 2, days=0)]
    swap = drafted(LATE_SELLER, turns, Offer(price=70, days=0), 105, days=0)
    assert (swap.price, swap.days) == (105, 0) and "rule" not in swap.meta


def test_the_runner_keeps_the_sessions_day_weights(tmp_path: Path):
    r = runner(FakeBazaar(), FakeModel(plan(70, 72, 68)), tmp_path)
    r.tick = 101
    base = {"role": "seller", "your_limit": 40, "deadline": 116, "rival_offer": None, "issues": ["price", "days"],
            "days_meaning": "each day later costs you w"}
    for did, (w, session) in enumerate(((1, 2), (3, 2), (2, 3)), 1):
        r.update({**base, "id": did, "your_days_weight": w, "session": session})
    assert sorted(r.observe(r.duels[1]).day_swings) == [10, 30]   # session 2 only
    assert r.observe(r.duels[3]).day_swings == [20]


def test_the_days_guide_and_the_negotiator_line():
    from agents.duelist.agent import brief
    s = brief(LATE_SELLER, strategist=True)["days_guide"]
    assert "Never settle on a middle day" in s and "at most 2 P" in s and "C/2" in s
    n = brief(LATE_SELLER, strategist=False)["days_negotiator"]
    assert "second package" in n and "only the price and day of your offer bind" in n


def test_the_opener_is_always_an_offer():
    talk = Decision(action="message", price=None, message="Tell me more about what you need.")
    move = respond(SELLER, obs(SELLER), FakeModel(plan(70, 72, 68), talk, talk))
    assert move.action == "offer" and move.price == 70 and "no offer standing" in move.meta["vetoes"][0]


def test_monitor_reads_a_duel_from_its_record():
    from agents.duelist.monitor import duel
    d = duel(Records(DUELS).load(278), 200, {})
    assert (d["status"], d["price"], d["result"], d["rounds"], d["messages"]) == ("deal", 111, 2.7, 10, [10, 11])
    last = d["events"][-1]
    assert (last["kind"], last["price"], last["rule"], last["sent"]) == ("accept", 111, "deadline", True)
    first_ours = next(e for e in d["events"] if e["kind"] == "message" and e["mine"])
    assert first_ours["decision"]["band"] == {"worst": 84, "target": 80, "best": 76} and first_ours["decision"]["read"]


def test_monitor_shows_holds_and_ends_a_duel_at_its_deadline():
    from agents.duelist.monitor import duel
    rec = {"duel": 9, "payloads": [{"tick": 98, "raw": {"duel": 9, "status": "live", "role": "buyer", "your_limit": 100,
                                                        "deadline_tick": 100, "rounds": 1, "decay_per_round": 0.06,
                                                        "rival_offer": {"price": 90},
                                                        "messages": [{"tick": 97, "from": "you", "price": 70},
                                                                     {"tick": 97, "from": "Rival", "price": 90}]}}],
           "decisions": [{"tick": 98, "hold": True, "move": {"action": "offer", "price": 70, "meta": {}}}]}
    live = duel(rec, 98, {})
    assert live["live"] and live["ticks_left"] == 2 and live["worth_now"] == 9.4      # 10 x 0.94
    assert [e["kind"] for e in live["events"]] == ["message", "message", "hold"]
    assert duel(rec, 100, {})["status"] == "ended"                                   # over, result not saved yet


def test_monitor_counts_every_duel_in_the_field_from_the_feed():
    from agents.duelist.monitor import field
    events = [json.loads(line) for line in (DUELS / "feed.jsonl").read_text().splitlines()]
    practice = next(s for s in field(events, {277, 278})["sessions"] if s["session"] == 1)
    assert (practice["name"], practice["total"], practice["closed"], practice["deals"]) == ("Practice duels", 306, 306, 124)
    assert practice["ours_closed"] == 2 and practice["finished"]


def test_monitor_knows_whether_the_duelist_runs(tmp_path: Path):
    import os
    from agents.duelist.monitor import duelist_status, next_session
    (tmp_path / "run.lock").write_text(f"pid {os.getpid()}\n")
    assert duelist_status(tmp_path)["running"]
    (tmp_path / "run.lock").write_text("pid 999999\n")
    assert not duelist_status(tmp_path)["running"]
    nxt = next_session({"upcoming": [{"action": "duels", "at_hours": 5.15, "params": {"name": "Duels I"}}]},
                       {"t_hours": 3.15, "tick": 219, "tick_seconds": 30})
    assert (nxt["name"], nxt["minutes"], nxt["tick"]) == ("Duels I", 120, 459)    # 120 ticks a game hour at 30 s
