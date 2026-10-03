"""Offline tests for hub/demand.py: the posterior recovers a known order from rational trades, holdings follow
settlements, and the pricing rules respect the margin, the dealer's price and the per-trade cap."""
import random

import pytest

from hub import demand as d

SETS = ["LAV", "MAL", "LAT", "SAL", "RET", "CHA"]
RARITY = ["common"] * 5 + ["uncommon"] * 3 + ["rare"] * 2 + ["epic", "legendary"]
BOOK = {"common": 10, "uncommon": 25, "rare": 70, "epic": 180, "legendary": 450}


def catalog():
    sets = []
    for s in SETS:
        cards = [{"id": f"{s}-{i + 1:02d}", "rarity": r, "book": BOOK[r], "page": r in ("common", "uncommon", "rare")}
                 for i, r in enumerate(RARITY)]
        sets.append({"id": s, "released": True, "cards": cards})
    return d.Catalog.from_catalog_json({"sets": sets, "values": {"copy_marginals": [1, 0.25, 0.1], "page_bonus": 0.25}})


def settlement(eid, ref, aid, frm, to, price, fee=0, persona=None, tick=1):
    parties = [frm, to]
    return {"id": eid, "tick": tick, "t": tick / 60, "type": "settlement",
            "payload": {"kind": "trade", "parties": parties, "persona": persona, "price": price, "fee": fee,
                        "items": [{"id": aid, "kind": "card", "ref": ref, "frm": frm, "to": to}]}}


def test_catalog_page_book_and_marginals():
    cat = catalog()
    assert cat.page_book["LAV"] == 265
    assert cat.copy_marginal(0) == 1 and cat.copy_marginal(1) == 0.25 and cat.copy_marginal(5) == 0.1
    assert len(cat.page_cards("RET")) == 10


MARKET = {"common": 9, "uncommon": 24, "rare": 70}


def rational_team(truth, seed, n=120):
    """A team trading at market prices (±20 %): buys a first copy when it is worth the price to it, sells a copy
    (its only one 40 % of the time) when the price beats what it loses."""
    cat = catalog()
    rng = random.Random(seed)
    events, eid, aid = [], 1, 1000
    for _ in range(n):
        ref = rng.choice([r for r, c in cat.cards.items() if c["page"] and c["set"] in ("LAV", "MAL", "LAT", "SAL")])
        c = cat.cards[ref]
        price = max(1, round(MARKET[c["rarity"]] * rng.uniform(0.8, 1.2)))
        v1 = c["book"] * truth[c["set"]]
        if rng.random() < 0.5:
            if v1 >= price + d.rastro_fee(price):
                events.append(settlement(eid, ref, aid, "t02", "t09", price, fee=d.rastro_fee(price)))
        else:
            loss = v1 if rng.random() < 0.4 else 0.25 * v1
            if price >= loss:
                events.append(settlement(eid, ref, aid, "t09", "t02", price, fee=d.rastro_fee(price)))
        eid, aid = eid + 1, aid + 1
    return cat, events


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_posterior_recovers_a_rational_team(seed):
    truth = dict(zip(SETS, [0.5, 1.6, 0.9, 1.3, 0.7, 1.1]))
    cat, events = rational_team(truth, seed)
    w = d.World()
    w.ingest(events, cat)
    S, n, _ = d.set_scores(w, cat, ["t09"])
    marg, logw = d.posterior(S["t09"], cat)
    rank, p_truth = d.truth_rank(logw, cat, truth)
    e = {s: sum(m * x for m, x in zip(cat.mults, marg[s])) for s in ("LAV", "MAL", "LAT", "SAL")}
    assert rank <= 36, rank                                      # top 5 % of 720
    ranked = sorted(e, key=e.get)
    assert set(ranked[:2]) == {"LAV", "LAT"} and set(ranked[2:]) == {"SAL", "MAL"}, e   # low pair vs high pair


def test_buy_prices_alone_only_bound_from_below():
    """Paying well under value says little: five cheap buys of different commons must not pin a multiplier."""
    cat = catalog()
    w = d.World()
    w.ingest([settlement(i, f"LAV-0{i}", 100 + i, "t02", "t09", 2) for i in range(1, 6)], cat)
    S, _, _ = d.set_scores(w, cat, ["t09"], {**d.PARAMS, "beta_flow": 0.0})
    marg, _ = d.posterior(S["t09"], cat)
    assert max(marg["LAV"]) < 0.35


def test_repeat_buys_of_one_card_mean_a_high_value():
    """A second and third copy are worth 25 % / 10 %: paying 4 for each again only makes sense with a high m."""
    cat = catalog()
    w = d.World()
    w.ingest([settlement(i, "LAV-01", 100 + i, "t02", "t09", 4) for i in range(1, 6)], cat)
    S, _, _ = d.set_scores(w, cat, ["t09"], {**d.PARAMS, "beta_flow": 0.0})
    marg, _ = d.posterior(S["t09"], cat)
    assert marg["LAV"][0] == max(marg["LAV"])


def test_holdings_follow_settlements_and_dealers():
    cat = catalog()
    w = d.World()
    w.ingest([settlement(1, "LAV-01", 7, "t01", "t02", 9, fee=2),
              settlement(2, "LAV-01", 8, "t03", "t02", 9, fee=2),
              settlement(3, "LAV-01", 7, "t02", "abuela", 5, persona="abuela")], cat)
    assert w.held("t02") == {"LAV-01": 1}
    assert w.held("t01") == {}
    kinds = [(o.team, o.kind) for o in w.obs]
    assert ("t02", "team_buy") in kinds and ("t02", "dealer_sell") in kinds and ("t01", "team_sell") in kinds


def test_taker_pays_the_fee_in_the_observation():
    cat = catalog()
    w = d.World()
    w.ingest([settlement(1, "MAL-06", 7, "t01", "t02", 20, fee=2)], cat)   # parties [maker t01, taker t02]
    buy = next(o for o in w.obs if o.kind == "team_buy")
    sell = next(o for o in w.obs if o.kind == "team_sell")
    assert buy.price == 22 and sell.price == 20


def test_bids_keep_the_highest_price_and_mark_lacks():
    cat = catalog()
    w = d.World()
    for i, price in enumerate((5, 12, 8)):
        w.ingest([{"id": 10 + i, "tick": 1, "t": 0.1, "type": "offer.listed", "payload": {"offer": {
            "id": 100 + i, "maker": "t04", "give": {"cash": price, "assets": []},
            "want": {"cash": 0, "types": ["card:SAL-09"], "assets": []}}}}], cat)
    assert w.best_bid[("t04", "SAL-09", "bid")][0] == 12
    assert ("t04", "SAL-09") in w.lack_signal


def test_best_ask_respects_margin_and_outside_option():
    p = dict(d.PARAMS)
    rich = [(200.0, 1.0)]                       # the buyer would pay anything
    price, eg, pf = d.best_ask(3.0, rich, "common", p)
    assert price >= 3 + p["margin"]
    capped = d.best_ask(3.0, rich, "common", {**p, "outside_leak": 0.0})
    assert capped[0] + d.rastro_fee(capped[0]) <= p["outside"]["common"]
    assert d.best_ask(50.0, [(10.0, 1.0)], "rare", p)[0] is None   # nobody pays above its value


def test_best_bid_raises_the_price_when_the_cap_binds():
    p = dict(d.PARAMS)
    seller = [(10.0, 0.5), (40.0, 0.5)]          # the holder loses 10 or 40 by selling
    price, eg, pf = d.best_bid(120.0, seller, p)
    assert pf == pytest.approx(1.0)             # value − price stays ≥ cap, so paying more is free
    assert 120 - price >= p["cap"] - 1e-9
    low = d.best_bid(30.0, seller, p)
    assert low[0] <= 30 - p["margin"]


def test_value_dist_duplicates_and_page_closer():
    cat = catalog()
    marg = [0, 1, 0, 0, 0, 0]                   # m = 1.3 for sure
    dup = d.value_dist(cat, "LAV-01", marg, n_held=1, p_lack=0.0, p_complete=0.0)
    assert d.expect(dup) == pytest.approx(0.25 * 10 * 1.3)
    closer = d.value_dist(cat, "LAV-01", marg, n_held=0, p_lack=1.0, p_complete=1.0)
    assert d.expect(closer) == pytest.approx(10 * 1.3 + 0.25 * 265 * 1.3)


def test_compute_runs_end_to_end_and_flags_rivals():
    cat = catalog()
    w = d.World()
    w.ingest([settlement(1, "LAT-03", 7, "t01", "t02", 9, fee=2),
              {"id": 2, "tick": 2, "t": 0.1, "type": "offer.listed", "payload": {"offer": {
                  "id": 5, "maker": "t03", "give": {"cash": 30, "assets": []},
                  "want": {"cash": 0, "types": ["card:LAT-09"], "assets": []}}}}], cat)
    us = d.Us("t05", dict(zip(SETS, [1.3, 0.7, 0.5, 0.9, 1.1, 1.6])),
              [{"id": 1, "ref": "LAT-09", "your_value": 35.0}, {"id": 2, "ref": "LAT-09", "your_value": 3.5}],
              {}, score=20.0, rank=5)
    snaps = {"t02": {"rank": 1, "score": 30.0, "album_filled": 20, "album_slots": 40},
             "t03": {"rank": 12, "score": 8.0, "album_filled": 20, "album_slots": 40}}
    out = d.compute(w, cat, us, snaps, {})
    assert out["selftest"]["of"] == 720
    sells = [o for o in out["opps"] if o["kind"] == "sell" and o["card"] == "LAT-09"]
    assert sells and all(o["price"] >= 3.5 + d.PARAMS["margin"] for o in sells)
    assert any(o["buyer"] == "t03" for o in sells)
