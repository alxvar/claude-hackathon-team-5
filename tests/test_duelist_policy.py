"""The code-first policy (agents/duelist/policy.py, --policy code): code decides accept / hold / step, one capped
model call writes the words, and a bad or late text becomes code's plain one."""
import asyncio

import pytest

from agents.duelist import agent as A, policy as P
from agents.duelist.agent import DuelAgent
from agents.duelist.model import DuelView, Observation, Offer, Role, Turn
from engine import LLMError, Reply

SELLER = DuelView(duel_id=1, role=Role.SELLER, limit=40, item="a card", decay=0.06, duel_ticks=12)
BUYER = DuelView(duel_id=2, role=Role.BUYER, limit=60, item="a card", decay=0.06, duel_ticks=12)


class Words:
    """A text model: answers with `text`, after `delay` seconds, or raises `error`."""
    label = "fake"

    def __init__(self, text="I can do that, as written.", delay=0.0, error=None):
        self.text, self.delay, self.error, self.seen = text, delay, error, []

    async def parse(self, schema, system, messages):
        self.seen.append((schema.__name__, system, messages))
        if self.delay:
            await asyncio.sleep(self.delay)
        if self.error:
            raise self.error
        return Reply(schema(message=self.text), 0.2, 10, 10, 0.0, "fake")


def obs(view, ours=(), theirs=(), left=8):
    turns = [Turn(mine=True, text="", offer=Offer(price=p), tick=i + 1) for i, p in enumerate(ours)]
    turns += [Turn(mine=False, text="Hmm.", offer=Offer(price=p), tick=i + 1) for i, p in enumerate(theirs)]
    turns.sort(key=lambda t: (t.tick, not t.mine))
    return Observation(view=view, turns=turns, rival_offer=Offer(price=theirs[-1]) if theirs else None, tick=9,
                       ticks_left=left)


def agent(view=SELLER, model=None):
    m = model or Words()
    return DuelAgent(view, m, m, policy="code"), m


def test_the_opener_sits_opener_share_of_the_limit_away_rounded_toward_us():
    a, _ = agent()
    assert P.code_move(a, obs(SELLER)).price == 70          # a seller: 40 + 0.73 x 40 = 69.2, up (per role, audit)
    b, _ = agent(BUYER)
    assert P.code_move(b, obs(BUYER)).price == 37           # a buyer: 60 - 0.37 x 60 = 37.8, down


def test_a_mid_duel_step_is_code_step_share_of_the_gap():
    a, _ = agent()
    m = P.code_move(a, obs(SELLER, ours=[80], theirs=[40]))   # worth 40 vs 0: gap 40, step 4.8
    assert (m.action, m.price, m.meta["rule"]) == ("offer", 76, "code step")


def test_a_step_below_min_step_is_held_and_a_big_share_is_cut(monkeypatch):
    a, _ = agent()
    m = P.code_move(a, obs(SELLER, ours=[52], theirs=[48]))   # gap 4: 0.6 < 3
    assert m.price == 52 and m.meta["rule"] == "code: small step"
    monkeypatch.setattr(P, "CODE_STEP_SHARE", 0.5)
    monkeypatch.setattr(A, "MAX_STEP_SHARE", 0.18)
    m = P.code_move(a, obs(SELLER, ours=[70], theirs=[50]))   # 50% cut to MAX_STEP_SHARE 18%: 3.6 off
    assert m.price == 67


def test_the_last_ticks_move_half_the_gap_and_take_an_offer_within_reach():
    a, _ = agent()
    assert P.code_move(a, obs(SELLER, ours=[70], theirs=[50], left=2)).price == 60
    m = P.code_move(a, obs(SELLER, ours=[50], theirs=[47], left=2))   # lands at 48.5: theirs within 2
    assert m.action == "accept" and m.price == 47


def test_their_offer_as_good_as_ours_is_accepted_and_the_limit_is_never_crossed():
    a, _ = agent()
    assert P.code_move(a, obs(SELLER, ours=[50], theirs=[55])).action == "accept"
    m = P.code_move(a, obs(SELLER, ours=[45], theirs=[30], left=2))   # theirs past our limit: our limit at most
    assert (m.action, m.price) == ("offer", 40)


def test_one_text_call_no_strategist_and_the_words_go_out():
    a, m = agent(model=Words("I can do 76 P."))
    move = asyncio.run(a.respond(obs(SELLER, ours=[80], theirs=[40])))
    assert (move.action, move.price, move.text) == ("offer", 76, "I can do 76 P.")
    assert [s for s, *_ in m.seen] == ["Words"] and [c["stage"] for c in move.meta["calls"]] == ["text"]


def test_a_hold_costs_no_model_call():
    a, m = agent()
    move = asyncio.run(a.respond(obs(SELLER, ours=[52], theirs=[48])))
    assert move.price == 52 and m.seen == []


@pytest.mark.parametrize("model,why", [
    (Words("It's a rare card: 76 P."), "rejected"),        # a claim
    (Words("Deal at 76 P?"), "rejected"),                  # agreement words on an offer
    (Words("I can do 76 P, not 30."), "rejected"),         # a number past our limit
    (Words(error=LLMError("down")), "model error"),
])
def test_bad_or_failed_words_become_plain_ones(model, why):
    a, _ = agent(model=model)
    move = asyncio.run(a.respond(obs(SELLER, ours=[80], theirs=[40])))
    assert move.text == "I can do 76 P." and why in move.meta["text"]


def test_a_slow_text_model_is_cut_at_the_budget(monkeypatch):
    monkeypatch.setattr(P, "TEXT_TIMEOUT_S", 0.05)
    a, _ = agent(model=Words("I can do 76 P.", delay=1.0))
    move = asyncio.run(a.respond(obs(SELLER, ours=[80], theirs=[40])))
    assert move.text == "I can do 76 P." and "timeout" in move.meta["text"]


def test_an_accept_gets_words_that_may_agree():
    a, m = agent(model=Words("Agreed, thank you."))
    move = asyncio.run(a.respond(obs(SELLER, ours=[50], theirs=[55])))
    assert (move.action, move.price, move.text) == ("accept", 55, "Agreed.")   # an accept posts no text: no call
    assert m.seen == []


def test_the_llm_policy_is_untouched():
    a = DuelAgent(SELLER, Words(), Words())
    assert a.policy == "llm" and "Words" not in a.strategist_system


DAYS_SELLER = DuelView(duel_id=6094, role=Role.SELLER, limit=34, item="a card", decay=0.08, duel_ticks=16,
                       issues=["price", "days"], days_weight=5.11,
                       days_meaning="each delivery day adds this much cash to your side")


def test_a_days_seller_opens_on_price_not_on_a_worth_that_carries_the_day_bonus():
    # Duel 6094 replay: worth-based, the opener came out at -2 P (day 10 adds 51.1 to a seller's worth)
    a, _ = agent(DAYS_SELLER)
    m = P.code_move(a, obs(DAYS_SELLER))
    assert m.days == 10 and m.price == 59                   # 34 + 0.73 x 34 = 58.8, up


def test_prices_never_go_below_the_floor_and_the_accept_ratio_is_tunable(monkeypatch):
    a, _ = agent(DAYS_SELLER)
    o = Observation(view=DAYS_SELLER, turns=[Turn(mine=True, text="", offer=Offer(price=5, days=10), tick=1),
                                            Turn(mine=False, text="", offer=Offer(price=0, days=0), tick=1)],
                    rival_offer=Offer(price=0, days=0), tick=9, ticks_left=2)
    m = P.code_move(a, o)
    assert m.action == "offer" and m.price >= P.MIN_PRICE
    b, _ = agent()
    assert P.code_move(b, obs(SELLER, ours=[80], theirs=[75])).action == "offer"   # 35 of 40: below 1.0
    monkeypatch.setattr(P, "ACCEPT_RATIO", 0.85)
    m = P.code_move(b, obs(SELLER, ours=[80], theirs=[75]))
    assert m.action == "accept" and "88%" in m.meta["rule"]


# Duel 6190 (Duels II wave 9, buyer, limit 143, each delivery day costs us 5 P): after the late switch to their day
# (116 on day 0 → 66 on day 10, worth 27 both), the model offered 88 on day 10, worth 5, as if the day were free;
# the rival (108 on day 10, worth -15) took it.
D6190 = DuelView(duel_id=6190, role=Role.BUYER, limit=143, item="a card", decay=0.08, duel_ticks=16,
                 issues=["price", "days"], days_weight=5.0, days_meaning="each delivery day costs you this much cash")


def obs_6190(left=3):
    ours = [(95, 0, 1367), (103, 0, 1368), (108, 0, 1369), (116, 0, 1378), (66, 10, 1379)]
    theirs = [(134, 10, 1366), (125, 10, 1367), (116, 10, 1368), (108, 10, 1379)]
    turns = [Turn(mine=True, text="", offer=Offer(price=p, days=d), tick=t) for p, d, t in ours]
    turns += [Turn(mine=False, text="", offer=Offer(price=p, days=d), tick=t) for p, d, t in theirs]
    turns.sort(key=lambda t: (t.tick, not t.mine))
    return Observation(view=D6190, turns=turns, rival_offer=Offer(price=108, days=10), tick=1380, ticks_left=left)


def test_6190_the_model_s_worth_5_package_is_floored_to_the_normal_step():
    from agents.duelist.guards import worth
    a = DuelAgent(D6190, Words(), Words())                    # the llm policy's last line
    m = a.final(A.Move("offer", "I can do 88 P, delivery on day 10.", price=88, days=10), obs_6190())
    assert (m.action, m.days, m.meta["rule"]) == ("offer", 10, "worth floor")
    assert m.price == 76 and worth(D6190, 76, 10) >= 27 - A.MONO_END_SHARE * 42      # 27 - 10.5 = 16.5
    assert m.text == "I can do 76 P, delivery on day 10."
    m = a.final(A.Move("offer", "x", price=78, days=10), obs_6190())                  # worth 15: also floored
    assert m.price == 76
    m = a.final(A.Move("offer", "I can do 74 P, delivery on day 10.", price=74, days=10), obs_6190())
    assert (m.price, m.meta.get("rule")) == (74, None)                                 # worth 19: inside the floor


def test_6190_the_code_policy_steps_in_worth_and_the_floor_holds_its_closing_step():
    b, _ = agent(D6190, Words("I can do 76 P, delivery on day 10."))
    move = asyncio.run(b.respond(obs_6190()))
    assert (move.action, move.price, move.days) == ("offer", 76, 10)


def test_never_offer_worse_than_their_standing_offer_accept_it_instead():
    a = DuelAgent(SELLER, Words(), Words())
    o = obs(SELLER, ours=[70], theirs=[60])
    m = a.final(A.Move("offer", "I can do 58 P.", price=58), o)                       # worse for us than their 60
    assert (m.action, m.price, m.meta["rule"]) == ("accept", 60, "theirs is as good as our offer")
    o = obs_6190()                                                                    # with days: whole packages
    m = DuelAgent(D6190, Words(), Words()).final(A.Move("offer", "x", price=130, days=10), o)
    assert m.action == "offer"                                                        # theirs is past our limit


def test_the_first_offer_follows_the_day_call():
    # their first offer names day 0, which costs us nothing: the call is "take", whatever the strategist planned
    a = DuelAgent(D6190, Words(), Words())
    o = Observation(view=D6190, turns=[Turn(mine=False, text="", offer=Offer(price=150, days=0), tick=1)],
                    rival_offer=Offer(price=150, days=0), tick=2, ticks_left=15)
    from agents.duelist.agent import BandPlan
    plan = BandPlan(read="-", target=50, best=45, worst=55, days=10, angle="-")    # planned on day 10
    p = a.first_day(plan, o)
    assert p.days == 0 and p.target == 100 and p.worst == 105                     # same worth on day 0: 50 P more
    assert a.first_day(p, o) is p                                                  # already on the call's day
    later = Observation(view=D6190, turns=[*o.turns, Turn(mine=True, text="", offer=Offer(price=95, days=0), tick=2)],
                        rival_offer=Offer(price=150, days=0), tick=3, ticks_left=14)
    assert a.first_day(plan, later) is plan                                        # only the first offer
    c, _ = agent(D6190)
    assert P.code_move(c, o).days == 0                                             # the code opener follows it too


def test_guards_off_switch(monkeypatch):
    monkeypatch.setattr(A, "GUARDS", 0)                               # {"GUARDS": 0} in run/duel_params.json
    a = DuelAgent(D6190, Words(), Words())
    m = a.final(A.Move("offer", "I can do 88 P, delivery on day 10.", price=88, days=10), obs_6190())
    assert (m.price, m.meta.get("rule")) == (88, None)



def test_a_give_is_worth_neutral_and_never_retreats_once_on_their_day():
    # audit S1: after a "give" call, the premium was re-added on every step and the offer ran away from the rival
    from agents.duelist.guards import worth
    view = D6190.model_copy(update={"role": Role.BUYER, "limit": 100, "days_weight": 1.2})
    a, _ = agent(view)
    seq = [Turn(mine=False, text="", offer=Offer(price=90, days=10), tick=1)]
    o = Observation(view=view, turns=seq, rival_offer=Offer(price=90, days=10), tick=2, ticks_left=10)
    first = P.code_move(a, o)
    prev = worth(view, first.price, first.days)
    theirs = 90
    for t in range(3, 8):                                             # the rival concedes; we must not retreat
        seq.append(Turn(mine=True, text="", offer=Offer(price=first.price, days=first.days), tick=t))
        theirs -= 2
        seq.append(Turn(mine=False, text="", offer=Offer(price=theirs, days=10), tick=t))
        o = Observation(view=view, turns=list(seq), rival_offer=Offer(price=theirs, days=10), tick=t + 1,
                        ticks_left=12 - t)
        m = P.code_move(a, o)
        if m.action != "offer":
            break
        assert worth(view, m.price, m.days) <= prev + 1e-9            # every move concedes or holds, never retreats
        prev, first = worth(view, m.price, m.days), m


def test_guards_leave_an_unreadable_day_alone_and_never_accept_from_a_past_limit_draft():
    unread = D6190.model_copy(update={"days_weight": "?", "days_meaning": None})
    a = DuelAgent(unread, Words(), Words())
    o = Observation(view=unread, turns=[Turn(mine=True, text="", offer=Offer(price=62, days=0), tick=1),
                                        Turn(mine=False, text="", offer=Offer(price=58, days=10), tick=1)],
                    rival_offer=Offer(price=58, days=10), tick=2, ticks_left=8)
    m = a.guarded(A.Move("offer", "x", price=61, days=0), o)
    assert m.action == "offer" and m.price == 61                       # no worth comparison on an unreadable day
    b = DuelAgent(SELLER, Words(), Words())
    m = b.guarded(A.Move("offer", "x", price=30), obs(SELLER, ours=[50], theirs=[41]))
    assert m.action == "offer"                                         # our draft is past the limit: no accept


def test_a_seller_may_name_its_own_price_below_the_nominal_limit_on_a_bonus_day():
    view = DuelView(duel_id=1, role=Role.SELLER, limit=73, item="a card", decay=0.08, duel_ticks=16,
                    issues=["price", "days"], days_weight=4.46, days_meaning="each delivery day adds this much cash to your side")
    a = DuelAgent(view, Words(), Words())
    o = Observation(view=view, turns=[Turn(mine=True, text="", offer=Offer(price=80, days=10), tick=1)],
                    rival_offer=None, tick=2, ticks_left=6)
    m = a.final(A.Move("offer", "I can do 70 P, delivery on day 10.", price=70, days=10), o)
    assert (m.action, m.price) == ("offer", 70)                       # worth +41.6: not "Let me think about that."
