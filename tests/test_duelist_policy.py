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
    assert P.code_move(a, obs(SELLER)).price == 57          # 40 + 0.42 x 40 = 56.8, up
    b, _ = agent(BUYER)
    assert P.code_move(b, obs(BUYER)).price == 34           # 60 - 25.2 = 34.8, down


def test_a_mid_duel_step_is_code_step_share_of_the_gap():
    a, _ = agent()
    m = P.code_move(a, obs(SELLER, ours=[70], theirs=[50]))   # worth 30 vs 10: gap 20, step 3
    assert (m.action, m.price, m.meta["rule"]) == ("offer", 67, "code step")


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
    a, m = agent(model=Words("I can do 67 P."))
    move = asyncio.run(a.respond(obs(SELLER, ours=[70], theirs=[50])))
    assert (move.action, move.price, move.text) == ("offer", 67, "I can do 67 P.")
    assert [s for s, *_ in m.seen] == ["Words"] and [c["stage"] for c in move.meta["calls"]] == ["text"]


def test_a_hold_costs_no_model_call():
    a, m = agent()
    move = asyncio.run(a.respond(obs(SELLER, ours=[52], theirs=[48])))
    assert move.price == 52 and m.seen == []


@pytest.mark.parametrize("model,why", [
    (Words("It's a rare card: 67 P."), "rejected"),        # a claim
    (Words("Deal at 67 P?"), "rejected"),                  # agreement words on an offer
    (Words("I can do 67 P, not 30."), "rejected"),         # a number past our limit
    (Words(error=LLMError("down")), "model error"),
])
def test_bad_or_failed_words_become_plain_ones(model, why):
    a, _ = agent(model=model)
    move = asyncio.run(a.respond(obs(SELLER, ours=[70], theirs=[50])))
    assert move.text == "I can do 67 P." and why in move.meta["text"]


def test_a_slow_text_model_is_cut_at_the_budget(monkeypatch):
    monkeypatch.setattr(P, "TEXT_TIMEOUT_S", 0.05)
    a, _ = agent(model=Words("I can do 67 P.", delay=1.0))
    move = asyncio.run(a.respond(obs(SELLER, ours=[70], theirs=[50])))
    assert move.text == "I can do 67 P." and "timeout" in move.meta["text"]


def test_an_accept_gets_words_that_may_agree():
    a, _ = agent(model=Words("Agreed, thank you."))
    move = asyncio.run(a.respond(obs(SELLER, ours=[50], theirs=[55])))
    assert (move.action, move.price, move.text) == ("accept", 55, "Agreed, thank you.")


def test_the_llm_policy_is_untouched():
    a = DuelAgent(SELLER, Words(), Words())
    assert a.policy == "llm" and "Words" not in a.strategist_system
