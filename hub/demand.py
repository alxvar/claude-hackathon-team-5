"""Demand model v0: what every card is worth to every team, from public behaviour alone. No LLM.

    uv run python -m hub.demand --once          # one run: read the hub, write team_mult / team_card_value /
                                                #   opportunities / evidence (replaces the previous run's rows)
    uv run python -m hub.demand --every 120     # keep running (incremental: only new events are fetched)
    uv run python -m hub.demand --once --dry-run --selftest   # print, write nothing; check the model on our team

What we know (RULES.md, GAME.md, /api/catalog): one more copy of card X is worth to team T
    book(X) × m_T(set) × copy marginal (1, 0.25, 0.10 for the 1st, 2nd, 3rd copy)
    + page bonus 0.25 × page book (265) × m_T(set) if X is the last card T misses on that page.
Every team's six multipliers are the same six numbers (ours) in its own order: 720 possible orders per team.

Unknowns: the order (exact Bayesian posterior over the 720) and the holdings (tracked from settlements and listings;
starting hands and most pack pulls are invisible, so "lacks X" is a probability).

Evidence → likelihood of each multiplier for that card's set (noisy: teams aren't fully rational):
    a team bought X at cost c   → value ≥ c   (team trade: strong; dealer: weak, teams buy from dealers for the ladder)
    a team sold X for r         → value of its copy ≤ r (often a duplicate, so weaker)
    a team bid / asked p, unfilled, or bid p to a dealer → the same, weaker
    a team keeps buying / dumping a set → that multiplier is high / low (small weight)
Our own team is the check: `--selftest` scores the posterior for our true order from our public behaviour only.

Outputs (hub tables): team_mult (posterior per team × set), team_card_value (E[value], q25, q75, P(lacks),
P(completes page)), opportunities (sell / buy / match with a price that maximises expected gain), evidence.
"""
import argparse
import itertools
import json
import math
import os
import sys
import time
import urllib.request
from collections import defaultdict
from dataclasses import dataclass, field

from psycopg.types.json import Jsonb

from hub.db import connect, redact

MULTS_DEFAULT = (1.6, 1.3, 1.1, 0.9, 0.7, 0.5)
COPY_DEFAULT = (1.0, 0.25, 0.10)
PAGE_BONUS_DEFAULT = 0.25

PARAMS = {
    "tau_abs": 2.0,       # price noise: τ = tau_abs + tau_rel × price
    "tau_rel": 0.15,
    "eps": {"team_buy": 0.10, "team_sell": 0.15, "dealer_buy": 0.35, "dealer_sell": 0.30,
            "bid": 0.35, "ask": 0.40, "dealer_bid": 0.45},
    "q_first_buy": 0.75,          # a buyer lacked the card (no earlier signal)
    "q_first_buy_signal": 0.95,   # ... after it bid for it or asked a dealer for it
    "q_complete": 0.10,           # a first copy also completes the buyer's page
    "q_only_copy_sell": 0.40,     # a seller gave up its only copy
    "beta_flow": 0.6,             # weight of buy/dump counts per set
    "lack_half_life_h": 2.0,      # a "lacks X" signal fades to the prior with this half-life (game hours)
    "lack_signal_p": 0.92,
    "lack_prior_new_set": 0.85,   # sets released in the last 3 game hours
    "margin": 3,                  # never sell below our value + margin / buy above our value − margin
    "cap": 50,                    # per-trade gain cap [L, GAME.md]
    "outside": {"common": 10, "uncommon": 24, "rare": 90},   # what a dealer realistically charges (GAME.md)
    "outside_leak": 0.25,         # chance a team pays above the dealer's price anyway (page closers, convenience)
    "feeding_gap": 10, "top_n": 4,
}
EVENT_TYPES = ("settlement", "offer.listed", "thread.opened", "gift.given", "pack.opened", "thread.message")


def phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def rastro_fee(price: float, n_cards: int = 1) -> int:
    return math.ceil(0.05 * price) + n_cards


def is_team(x) -> bool:
    return isinstance(x, str) and len(x) >= 2 and x[0] == "t" and x[1:].isdigit()


# ---------------------------------------------------------------------------------------------------------- catalog

@dataclass
class Catalog:
    cards: dict                     # ref → {set, rarity, book, page}
    sets: list                      # set ids, fixed order
    mults: tuple = MULTS_DEFAULT
    copy: tuple = COPY_DEFAULT
    page_bonus: float = PAGE_BONUS_DEFAULT
    released: dict = field(default_factory=dict)   # set → bool

    @property
    def page_book(self) -> dict:
        out = defaultdict(float)
        for c in self.cards.values():
            if c["page"]:
                out[c["set"]] += c["book"]
        return out

    def page_cards(self, s: str) -> list:
        return [r for r, c in self.cards.items() if c["set"] == s and c["page"]]

    def copy_marginal(self, n_held: int) -> float:
        return self.copy[min(n_held, len(self.copy) - 1)]

    @classmethod
    def from_catalog_json(cls, cat: dict, mults=MULTS_DEFAULT) -> "Catalog":
        cards, sets, released = {}, [], {}
        for s in cat.get("sets") or []:
            sets.append(s["id"])
            released[s["id"]] = bool(s.get("released"))
            for c in s.get("cards") or []:
                if c.get("hidden"):
                    continue
                cards[c["id"]] = {"set": s["id"], "rarity": c["rarity"], "book": c["book"], "page": bool(c.get("page"))}
        v = cat.get("values") or {}
        return cls(cards, sets, tuple(sorted(mults, reverse=True)), tuple(v.get("copy_marginals") or COPY_DEFAULT),
                   float(v.get("page_bonus") or PAGE_BONUS_DEFAULT), released)


# ---------------------------------------------------------------------------------------------------------- evidence

@dataclass
class Obs:
    team: str
    card: str
    kind: str          # team_buy | team_sell | dealer_buy | dealer_sell | bid | ask | dealer_bid
    price: float       # buyer's cost (incl. fee it paid) or seller's net
    tick: int
    q: float           # P(first copy) for buy-side, P(only copy) for sell-side
    direction: str     # "ge": value ≥ price · "le": value ≤ price
    detail: dict = field(default_factory=dict)


@dataclass
class World:
    """Everything the model reads from the event stream, built incrementally."""
    obs: list = field(default_factory=list)
    owner: dict = field(default_factory=dict)        # asset id → team (or None once a dealer has it)
    asset_ref: dict = field(default_factory=dict)    # asset id → card ref
    seen_refs: dict = field(default_factory=lambda: defaultdict(set))       # team → refs seen held (no asset id)
    lack_signal: dict = field(default_factory=dict)  # (team, ref) → game hours of its latest "lacks" signal
    flow: dict = field(default_factory=lambda: defaultdict(float))          # (team, set) → net buys − dumps
    flow_keys: set = field(default_factory=set)
    best_bid: dict = field(default_factory=dict)     # (team, ref, kind) → (price, tick, t)
    best_ask: dict = field(default_factory=dict)     # (team, ref) → (price, tick, t, asset id)
    sold_assets: set = field(default_factory=set)    # (team, asset id) sold in a settlement
    max_id: int = 0                                  # newest positive event id ingested (the incremental cursor)
    seen_ids: set = field(default_factory=set)
    seen_settlements: set = field(default_factory=set)
    now_t: float = 0.0
    now_tick: int = 0

    counts: dict = field(default_factory=lambda: defaultdict(lambda: defaultdict(int)))   # team → ref → copies

    def set_owner(self, aid: int, team, ref=None):
        """Move asset `aid` to `team` (None = a dealer); keep per-team counts in step."""
        old, old_ref = self.owner.get(aid), self.asset_ref.get(aid)
        if old is not None and old_ref is not None:
            self.counts[old][old_ref] -= 1
        if ref is not None:
            self.asset_ref[aid] = ref
        self.owner[aid] = team if is_team(team) else None
        new_ref = self.asset_ref.get(aid)
        if self.owner[aid] is not None and new_ref is not None:
            self.counts[self.owner[aid]][new_ref] += 1

    def learn_ref(self, aid: int, ref: str):
        if aid in self.asset_ref:
            return
        self.asset_ref[aid] = ref
        if self.owner.get(aid) is not None:
            self.counts[self.owner[aid]][ref] += 1

    def held(self, team: str) -> dict:
        n = {r: c for r, c in self.counts.get(team, {}).items() if c > 0}
        for r in self.seen_refs.get(team, ()):
            n[r] = max(n.get(r, 0), 1)
        return n

    def _flow(self, team, ref, cat, sign, key):
        c = cat.cards.get(ref)
        if c and (team, ref, key) not in self.flow_keys:
            self.flow_keys.add((team, ref, key))
            self.flow[(team, c["set"])] += sign

    @staticmethod
    def order(e: dict) -> tuple:
        """Game order. Backfilled settlements carry id = −settlement number (Lucas's Friday file had them as -1):
        they go after the real events of their tick, in settlement order."""
        i = e["id"]
        return (e.get("tick") or 0, 0, i) if i > 0 else (e.get("tick") or 0, 1, -i)

    def ingest(self, events: list, cat: Catalog, p=PARAMS):
        """Apply events once each. Holdings depend on order, so a batch must not contain events older than ones
        already applied: the caller rebuilds the World when that happens (see Reader.late_arrivals)."""
        for e in sorted(events, key=self.order):
            if e["id"] in self.seen_ids:
                continue
            self.seen_ids.add(e["id"])
            if e["id"] > self.max_id:
                self.max_id = e["id"]
            pl = e.get("payload") or {}
            if e["type"] == "settlement":
                sid = pl.get("settlement")
                if sid is not None and sid in self.seen_settlements:
                    continue      # the same settlement under a real id and a backfilled one
                self.seen_settlements.add(sid)
            tick, t = e.get("tick") or 0, e.get("t") or e.get("t_hours") or 0.0
            self.now_tick, self.now_t = max(self.now_tick, tick), max(self.now_t, t)
            typ = e["type"]
            if typ == "settlement" and pl.get("kind") == "trade":
                self._settlement(pl, tick, t, cat, p)
            elif typ == "offer.listed":
                self._listing(pl.get("offer") or {}, tick, t, cat)
            elif typ == "thread.message":
                o = pl.get("offer") or {}
                if is_team(pl.get("sender")) and o and o.get("maker") == pl.get("sender"):
                    self._listing(o, tick, t, cat, dealer=True)
            elif typ == "thread.opened" and is_team(pl.get("team")):
                topic = pl.get("topic") or {}
                buy, sell = topic.get("buy") or {}, topic.get("sell") or {}
                if isinstance(buy, dict) and buy.get("card") in cat.cards:
                    self.lack_signal[(pl["team"], buy["card"])] = t
                    self._flow(pl["team"], buy["card"], cat, +1, "want")
                for a in (sell.get("assets") or []) if isinstance(sell, dict) else []:
                    if isinstance(a, int):
                        self.set_owner(a, pl["team"])
                        if a in self.asset_ref:
                            self._flow(pl["team"], self.asset_ref[a], cat, -1, "dump")
            elif typ == "gift.given" and is_team(pl.get("team")):
                for r in pl.get("cards") or []:
                    self.seen_refs[pl["team"]].add(r)
            elif typ == "pack.opened" and is_team(pl.get("team")):
                b = pl.get("best") or {}
                if isinstance(b, dict) and b.get("ref"):
                    if isinstance(b.get("id"), int):
                        self.set_owner(b["id"], pl["team"], b["ref"])
                    else:
                        self.seen_refs[pl["team"]].add(b["ref"])

    def _settlement(self, pl, tick, t, cat, p):
        items = [i for i in pl.get("items") or [] if i.get("kind") == "card" and i.get("ref") in cat.cards]
        parties = pl.get("parties") or []
        taker = parties[1] if len(parties) > 1 else None
        dealer = pl.get("persona")
        price, fee = float(pl.get("price") or 0), float(pl.get("fee") or 0)
        for i in items:
            if isinstance(i.get("id"), int):
                self.learn_ref(i["id"], i["ref"])
        dirs = {(i.get("frm"), i.get("to")) for i in items}
        one_way = len(dirs) == 1 and items and price > 0
        if one_way:
            seller, buyer = next(iter(dirs))
            total_book = sum(cat.cards[i["ref"]]["book"] for i in items) or 1
            for i in items:
                share = cat.cards[i["ref"]]["book"] / total_book
                ref = i["ref"]
                if is_team(buyer):
                    cost = share * (price + (fee if buyer == taker else 0))
                    if self.held(buyer).get(ref, 0) >= 1:
                        q = 0.1
                    elif (buyer, ref) in self.lack_signal:
                        q = p["q_first_buy_signal"]
                    else:
                        q = p["q_first_buy"]
                    kind = "dealer_buy" if dealer else "team_buy"
                    self.obs.append(Obs(buyer, ref, kind, cost, tick, q, "ge",
                                        {"price": price, "fee": fee if buyer == taker else 0, "from": seller}))
                    self._flow(buyer, ref, cat, +1, "buy")
                if is_team(seller):
                    net = share * (price - (fee if seller == taker else 0))
                    n_held = self.held(seller).get(ref, 0)
                    q = 0.1 if n_held >= 2 else p["q_only_copy_sell"]
                    kind = "dealer_sell" if dealer else "team_sell"
                    self.obs.append(Obs(seller, ref, kind, net, tick, q, "le",
                                        {"price": price, "fee": fee if seller == taker else 0, "to": buyer}))
                    self._flow(seller, ref, cat, -1, "sell")
                    if isinstance(i.get("id"), int):
                        self.sold_assets.add((seller, i["id"]))
        for i in items:   # ownership moves whatever the trade's shape (swaps included)
            to = i.get("to")
            if isinstance(i.get("id"), int):
                self.set_owner(i["id"], to, i["ref"])
            if is_team(to):
                self.lack_signal.pop((to, i["ref"]), None)

    def _listing(self, o, tick, t, cat, dealer=False):
        maker = o.get("maker")
        if not is_team(maker):
            return
        give, want = o.get("give") or {}, o.get("want") or {}
        wanted = [x.split(":", 1)[1] for x in want.get("types") or [] if isinstance(x, str) and x.startswith("card:")]
        wanted += [r for r in want.get("cards") or [] if isinstance(r, str)]
        wanted = [r for r in wanted if r in cat.cards]
        gave = [a for a in give.get("assets") or [] if isinstance(a, dict) and a.get("ref") in cat.cards]
        for a in gave:
            if isinstance(a.get("id"), int) and self.owner.get(a["id"]) != maker:
                self.set_owner(a["id"], maker, a["ref"])
        for r in wanted:
            self.lack_signal[(maker, r)] = t
            self._flow(maker, r, cat, +1, "want")
        if wanted and not gave and len(wanted) == 1 and (give.get("cash") or 0) > 0:
            kind = "dealer_bid" if dealer else "bid"
            key = (maker, wanted[0], kind)
            if give["cash"] > self.best_bid.get(key, (0,))[0]:
                self.best_bid[key] = (float(give["cash"]), tick, t)
        if gave and not wanted and len(gave) == 1 and (want.get("cash") or 0) > 0 and not dealer:
            key = (maker, gave[0]["ref"])
            if key not in self.best_ask or want["cash"] < self.best_ask[key][0]:
                self.best_ask[key] = (float(want["cash"]), tick, t, gave[0].get("id"))
            self._flow(maker, gave[0]["ref"], cat, -1, "dump")

    def all_obs(self, p=PARAMS) -> list:
        """Trades, plus each team's best standing bid / ask per card (asks whose card later sold are dropped)."""
        out = list(self.obs)
        for (team, ref, kind), (price, tick, _t) in self.best_bid.items():
            out.append(Obs(team, ref, kind, price, tick, p["q_first_buy_signal"], "ge", {"listed": True}))
        for (team, ref), (price, tick, _t, aid) in self.best_ask.items():
            if (team, aid) in self.sold_assets:
                continue
            out.append(Obs(team, ref, "ask", price, tick, p["q_only_copy_sell"], "le", {"listed": True}))
        return out


# ---------------------------------------------------------------------------------------------------------- posterior

def obs_loglik(o: Obs, cat: Catalog, p=PARAMS) -> list:
    """log P(observation | the card's set has multiplier m), for each m in cat.mults."""
    c = cat.cards[o.card]
    b = c["book"]
    bonus_rate = cat.page_bonus * cat.page_book[c["set"]] if c["page"] else 0.0
    eps = p["eps"][o.kind]
    tau = p["tau_abs"] + p["tau_rel"] * abs(o.price)
    out = []
    for m in cat.mults:
        v1, v2 = b * m, cat.copy[1] * b * m
        if o.direction == "ge":
            first = (1 - p["q_complete"]) * phi((v1 - o.price) / tau) + \
                p["q_complete"] * phi((v1 + bonus_rate * m - o.price) / tau)
            like = o.q * first + (1 - o.q) * phi((v2 - o.price) / tau)
        else:
            like = o.q * phi((o.price - v1) / tau) + (1 - o.q) * phi((o.price - v2) / tau)
        out.append(math.log(eps + (1 - eps) * like))
    return out


def set_scores(world: World, cat: Catalog, teams: list, p=PARAMS, exclude_private_for=None) -> dict:
    """team → set → [log-likelihood per multiplier]; also returns per-observation shifts for the evidence table."""
    k = len(cat.mults)
    mean_m = sum(cat.mults) / k
    S = {t: {s: [0.0] * k for s in cat.sets} for t in teams}
    n_obs = defaultdict(int)
    ev = []
    for o in world.all_obs(p):
        if o.team not in S:
            continue
        ll = obs_loglik(o, cat, p)
        s = cat.cards[o.card]["set"]
        row = S[o.team][s]
        for i in range(k):
            row[i] += ll[i]
        n_obs[(o.team, s)] += 1
        mx = max(ll)
        w = [math.exp(x - mx) for x in ll]
        shift = sum(m * wi for m, wi in zip(cat.mults, w)) / sum(w) - mean_m
        ev.append((o, s, shift))
    for (team, s), net in world.flow.items():
        if team in S and s in S[team]:
            z = math.tanh(net / 3.0)
            for i, m in enumerate(cat.mults):
                S[team][s][i] += p["beta_flow"] * z * (m - mean_m)
    return S, n_obs, ev


PERMS = {}


def perms(k: int) -> list:
    if k not in PERMS:
        PERMS[k] = list(itertools.permutations(range(k)))
    return PERMS[k]


def posterior(S_team: dict, cat: Catalog) -> tuple:
    """Exact posterior over the k! orders. Returns (marginals set → [P(m_i)], log-weights per order)."""
    k = len(cat.mults)
    sets = cat.sets[:k]
    logw = [sum(S_team[s][perm[j]] for j, s in enumerate(sets)) for perm in perms(k)]
    mx = max(logw)
    w = [math.exp(x - mx) for x in logw]
    z = sum(w)
    marg = {s: [0.0] * k for s in sets}
    for perm, wi in zip(perms(k), w):
        for j, s in enumerate(sets):
            marg[s][perm[j]] += wi / z
    return marg, logw


def truth_rank(logw: list, cat: Catalog, affinity: dict) -> tuple:
    """Rank (1 = best) and posterior probability of the true order, for the self-test."""
    k = len(cat.mults)
    idx = {m: i for i, m in enumerate(cat.mults)}
    true = tuple(idx[round(affinity[s], 2)] for s in cat.sets[:k])
    order = perms(k)
    pos = order.index(true)
    mx = max(logw)
    z = sum(math.exp(x - mx) for x in logw)
    rank = 1 + sum(1 for x in logw if x > logw[pos])
    return rank, math.exp(logw[pos] - mx) / z


# ---------------------------------------------------------------------------------------------------------- values

def lack_prob(world: World, team: str, ref: str, cat: Catalog, prior: dict, p=PARAMS) -> float:
    if world.held(team).get(ref, 0) >= 1:
        return 0.03
    base = prior.get(cat.cards[ref]["set"], 0.6)
    t = world.lack_signal.get((team, ref))
    if t is None:
        return base
    w = 0.5 ** (max(0.0, world.now_t - t) / p["lack_half_life_h"])
    return w * p["lack_signal_p"] + (1 - w) * base


def team_priors(cat: Catalog, snap: dict, released_at: dict, now_t: float, p=PARAMS) -> dict:
    """Per set, P(team lacks a given page card) before any card-specific signal."""
    filled, slots = (snap or {}).get("album_filled"), (snap or {}).get("album_slots")
    base = 1 - filled / slots if filled is not None and slots else 0.6
    out = {}
    for s in cat.sets:
        r = released_at.get(s)
        out[s] = p["lack_prior_new_set"] if r is not None and now_t - r < 3 else min(0.95, max(0.05, base))
    return out


def value_dist(cat: Catalog, ref: str, marg: list, n_held: int, p_lack: float, p_complete: float) -> list:
    """Discrete distribution [(value, prob)] of one more copy of `ref` to a team."""
    c = cat.cards[ref]
    b = c["book"]
    bonus_rate = cat.page_bonus * cat.page_book[c["set"]] if c["page"] else 0.0
    out = []
    for m, pm in zip(cat.mults, marg):
        if pm < 1e-9:
            continue
        if n_held >= 1:
            out.append((cat.copy_marginal(n_held) * b * m, pm))
            continue
        out.append((b * m + bonus_rate * m, pm * p_lack * p_complete))
        out.append((b * m, pm * p_lack * (1 - p_complete)))
        out.append((cat.copy[1] * b * m, pm * (1 - p_lack)))
    return [(v, w) for v, w in out if w > 0]


def loss_dist(cat: Catalog, ref: str, marg: list, n_held: int) -> list:
    """What giving up one copy costs a holder (its cheapest copy), as [(value, prob)]."""
    c = cat.cards[ref]
    b = c["book"]
    out = []
    for m, pm in zip(cat.mults, marg):
        if pm < 1e-9:
            continue
        if n_held >= 2:
            out.append((cat.copy_marginal(n_held - 1) * b * m, pm))
        else:
            out.append((b * m, pm))
    return out


def expect(dist: list) -> float:
    z = sum(w for _, w in dist) or 1.0
    return sum(v * w for v, w in dist) / z


def quantile(dist: list, q: float) -> float:
    z = sum(w for _, w in dist) or 1.0
    acc = 0.0
    for v, w in sorted(dist):
        acc += w / z
        if acc >= q - 1e-12:
            return v
    return max(v for v, _ in dist) if dist else 0.0


def p_at_least(dist: list, x: float) -> float:
    z = sum(w for _, w in dist) or 1.0
    return sum(w for v, w in dist if v >= x) / z


# ---------------------------------------------------------------------------------------------------------- pricing

def best_ask(our_loss: float, buyer_dist: list, rarity: str, p=PARAMS, max_price=500) -> tuple:
    """Our ask (we are maker; the buyer accepts and pays the fee). Maximises (price − our loss) × P(fill)."""
    outside = p["outside"].get(rarity)
    best = (None, 0.0, 0.0)
    lo = int(math.ceil(our_loss + p["margin"]))
    for price in range(max(1, lo), max_price + 1):
        cost = price + rastro_fee(price)
        pf = p_at_least(buyer_dist, cost)
        if outside is not None and cost > outside:
            pf *= p["outside_leak"]
        if pf <= 0:
            break
        eg = (price - our_loss) * pf
        if eg > best[1]:
            best = (price, eg, pf)
    return best


def best_bid(our_value: float, seller_loss: list, p=PARAMS) -> tuple:
    """Our bid (we are maker; the seller accepts and pays the fee). Maximises min(cap, value − price) × P(fill)."""
    best = (None, 0.0, 0.0)
    hi = int(math.floor(our_value - p["margin"]))
    for price in range(1, max(1, hi) + 1):
        pf = p_at_least([(-v, w) for v, w in seller_loss], -(price - rastro_fee(price)))
        eg = min(p["cap"], our_value - price) * pf
        if eg > best[1] + 1e-9:
            best = (price, eg, pf)
    return best


# ---------------------------------------------------------------------------------------------------------- run

@dataclass
class Us:
    team: str
    affinity: dict
    assets: list          # [{id, ref, your_value}]
    album: dict           # set → {have, of, complete}
    score: float = None
    rank: int = None

    def count(self) -> dict:
        n = defaultdict(int)
        for a in self.assets:
            n[a["ref"]] += 1
        return n

    def value_more(self, cat: Catalog, ref: str) -> float:
        """Our value of one more copy (book × m × marginal, + the page bonus if it is our last missing page card)."""
        c = cat.cards[ref]
        n = self.count()
        m = self.affinity.get(c["set"], 1.0)
        v = cat.copy_marginal(n.get(ref, 0)) * c["book"] * m
        if c["page"] and n.get(ref, 0) == 0:
            missing = [r for r in cat.page_cards(c["set"]) if n.get(r, 0) == 0]
            if missing == [ref]:
                v += cat.page_bonus * cat.page_book[c["set"]] * m
        return v

    def loss(self, ref: str) -> float:
        vals = [a.get("your_value") or 0 for a in self.assets if a["ref"] == ref]
        return min(vals) if vals else 0.0


def feeding(team: str, snap: dict, us: Us, p_complete: float, p=PARAMS) -> str:
    s = snap.get(team) or {}
    rank, score = s.get("rank"), s.get("score")
    if p_complete >= 0.3 and (rank is not None and rank <= p["top_n"] or
                              score is not None and us.score is not None and score > us.score - p["feeding_gap"]):
        return "page_closer_to_rival"
    if rank is not None and rank <= p["top_n"]:
        return "top4"
    return "ok"


def compute(world: World, cat: Catalog, us: Us, snaps: dict, released_at: dict, p=PARAMS, build=("RET", "CHA")):
    teams = sorted(set(snaps) | {o.team for o in world.obs} | {us.team})
    S, n_obs, ev = set_scores(world, cat, teams, p)
    k = len(cat.mults)
    marg, selftest = {}, None
    for t in teams:
        mg, logw = posterior(S[t], cat)
        if t == us.team:
            rank, ptrue = truth_rank(logw, cat, us.affinity)
            selftest = {"rank_of_truth": rank, "of": len(logw), "p_truth": ptrue,
                        "p_true_mult": {s: mg[s][cat.mults.index(round(us.affinity[s], 2))] for s in cat.sets[:k]}}
            mg = {s: [1.0 if abs(m - us.affinity[s]) < 1e-6 else 0.0 for m in cat.mults] for s in cat.sets[:k]}
        marg[t] = mg

    mult_rows = []
    for t in teams:
        for s in cat.sets[:k]:
            pm = marg[t][s]
            i = max(range(k), key=lambda j: pm[j])
            mult_rows.append((t, s, sum(m * x for m, x in zip(cat.mults, pm)),
                              {f"{m:.1f}": round(x, 4) for m, x in zip(cat.mults, pm)}, cat.mults[i], pm[i],
                              n_obs.get((t, s), 0)))

    values, lacks, comps, dists = [], {}, {}, {}
    for t in teams:
        if t == us.team:
            continue
        prior = team_priors(cat, snaps.get(t), released_at, world.now_t, p)
        held = world.held(t)
        lk = {r: lack_prob(world, t, r, cat, prior, p) for r in cat.cards}
        lacks[t] = lk
        for r, c in cat.cards.items():
            if c["page"]:
                pc = 1.0
                for y in cat.page_cards(c["set"]):
                    if y != r:
                        pc *= (1 - lk[y])
            else:
                pc = 0.0
            comps[(t, r)] = pc
            d = value_dist(cat, r, marg[t][c["set"]], held.get(r, 0), lk[r], pc)
            dists[(t, r)] = d
            values.append((t, r, c["set"], c["rarity"], expect(d), quantile(d, 0.25), quantile(d, 0.75), lk[r],
                           pc * lk[r], held.get(r, 0)))

    opps = []
    ours = us.count()
    complete_sets = {s for s, a in us.album.items() if a.get("complete")}
    # SELL: our copies, to the team where the expected gain is highest.
    for ref, n in ours.items():
        c = cat.cards.get(ref)
        if not c:
            continue
        if n == 1 and (c["set"] in build or c["set"] in complete_sets) and c["page"]:
            continue
        loss = us.loss(ref)
        cands = []
        for t in teams:
            if t == us.team:
                continue
            price, eg, pf = best_ask(loss, dists[(t, ref)], c["rarity"], p)
            if price is None or eg < 1.0:
                continue
            pcomp = comps[(t, ref)] * lacks[t][ref]
            cands.append({"kind": "sell", "card": ref, "seller": us.team, "buyer": t, "price": price,
                          "our_value": loss, "their_value": expect(dists[(t, ref)]), "p_fill": pf, "exp_gain": eg,
                          "p_completes": pcomp, "feeding": feeding(t, snaps, us, pcomp, p),
                          "why": f"{t} m≈{sum(m * x for m, x in zip(cat.mults, marg[t][c['set']])):.2f} on "
                                 f"{c['set']}, lacks {lacks[t][ref]:.0%}"})
        cands.sort(key=lambda o: -o["exp_gain"])
        opps.extend(cands[:3])
    # BUY: cards worth more to us than to a known holder.
    for t in teams:
        if t == us.team:
            continue
        for ref, n in world.held(t).items():
            if ref not in cat.cards:
                continue
            our_v = us.value_more(cat, ref)
            if our_v < 8:
                continue
            c = cat.cards[ref]
            ld = loss_dist(cat, ref, marg[t][c["set"]], n)
            price, eg, pf = best_bid(our_v, ld, p)
            if price is None or eg < 3.0:
                continue
            opps.append({"kind": "buy", "card": ref, "seller": t, "buyer": us.team, "price": price, "our_value": our_v,
                         "their_value": expect(ld), "p_fill": pf, "exp_gain": eg, "p_completes": None,
                         "feeding": "ok", "why": f"{t} holds {n} (known); its loss E={expect(ld):.1f}"})
    # MATCH: a known holder with little use for X and a team that wants it (for our venue).
    for a in teams:
        if a == us.team:
            continue
        for ref, n in world.held(a).items():
            if ref not in cat.cards:
                continue
            c = cat.cards[ref]
            la = expect(loss_dist(cat, ref, marg[a][c["set"]], n))
            best = None
            for b in teams:
                if b in (a, us.team):
                    continue
                vb = expect(dists[(b, ref)])
                if best is None or vb > best[1]:
                    best = (b, vb)
            if best and best[1] - la >= 10:
                b, vb = best
                pcomp = comps[(b, ref)] * lacks[b][ref]
                flag = "ok" if feeding(a, snaps, us, 0, p) == "ok" and feeding(b, snaps, us, pcomp, p) == "ok" \
                    else "involves_rival"
                opps.append({"kind": "match", "card": ref, "seller": a, "buyer": b, "price": round((la + vb) / 2),
                             "our_value": None, "their_value": vb, "p_fill": None, "exp_gain": vb - la,
                             "p_completes": pcomp, "feeding": flag,
                             "why": f"{a} loses ≈{la:.1f}, {b} gains ≈{vb:.1f}"})
    opps.sort(key=lambda o: -o["exp_gain"])
    return {"teams": teams, "marg": marg, "mult_rows": mult_rows, "values": values, "opps": opps[:150],
            "evidence": ev, "selftest": selftest}


# ---------------------------------------------------------------------------------------------------------- I/O

def fetch_me():
    """Our team's /api/me (one keyed GET per run). None without BAZAAR_KEY."""
    key = os.environ.get("BAZAAR_KEY")
    if not key:
        return None
    url = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai").rstrip("/") + "/api/me"
    req = urllib.request.Request(url, headers={"X-Team-Key": key, "User-Agent": "team5-hub-demand"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def load_us(me: dict, snaps: dict) -> Us:
    if me:
        album = {pg["set"]: pg for pg in (me.get("album") or {}).get("pages") or []}
        s = me.get("score") or {}
        return Us(me["id"], me.get("affinity") or {}, me.get("assets") or [], album, s.get("score"), s.get("rank"))
    team = os.environ.get("HUB_TEAM", "t05")
    aff = {"CHA": 1.6, "LAV": 1.3, "RET": 1.1, "SAL": 0.9, "MAL": 0.7, "LAT": 0.5}   # GAME.md
    sn = snaps.get(team) or {}
    return Us(team, aff, [], {}, sn.get("score"), sn.get("rank"))


class Reader:
    """Incremental reads from the hub (only new events are fetched after the first run)."""

    def __init__(self):
        self.conn = None

    def c(self):
        if self.conn is None or self.conn.closed:
            self.conn = connect("writer")
        return self.conn

    def catalog(self) -> Catalog:
        with self.c().cursor() as cur:
            cur.execute("select data from hub.state where kind = 'catalog'")
            row = cur.fetchone()
        if not row:
            raise SystemExit("no catalog in the hub yet: run the collector once")
        return Catalog.from_catalog_json(row[0])

    RELEVANT = """type = any(%s) and (type <> 'thread.message' or (payload->>'sender' like 't%%'
                                                                   and jsonb_typeof(payload->'offer') = 'object'))"""

    def events(self, after_id=None) -> list:
        """Relevant events; all of them (negative backfill ids included) when after_id is None."""
        where = self.RELEVANT + ("" if after_id is None else " and id > %s")
        args = [list(EVENT_TYPES)] + ([] if after_id is None else [after_id])
        with self.c().cursor() as cur:
            cur.execute(f"select id, tick, t_hours, type, payload from hub.events where {where}", args)
            return [{"id": i, "tick": tk, "t": th, "type": ty, "payload": pl} for i, tk, th, ty, pl in cur.fetchall()]

    def late_arrivals(self, world: "World") -> int:
        """Relevant events at or below the World's cursor that it has not applied: an import or a collector catching
        up after an outage. Any of them means the World must be rebuilt (holdings depend on order)."""
        with self.c().cursor() as cur:
            cur.execute(f"select count(*) from hub.events where {self.RELEVANT} and id <= %s",
                        (list(EVENT_TYPES), world.max_id))
            return cur.fetchone()[0] - len(world.seen_ids)

    def snapshots(self) -> dict:
        with self.c().cursor() as cur:
            cur.execute("""select team, rank, score, album_filled, album_slots, pages_complete
                           from hub.v_team_latest""")
            return {t: {"rank": r, "score": s, "album_filled": f, "album_slots": sl, "pages_complete": pc}
                    for t, r, s, f, sl, pc in cur.fetchall()}

    def released_at(self, cat: Catalog) -> dict:
        """Game hour of each set's release, from every schedule version we stored (past items drop off the live
        schedule). Sets out from the start are absent."""
        with self.c().cursor() as cur:
            cur.execute("select data from hub.state_history where kind = 'schedule' order by fetched_at")
            rows = cur.fetchall()
        out = {}
        for (d,) in rows:
            for item in (d or {}).get("upcoming") or []:
                if isinstance(item, dict) and item.get("action") == "set_release":
                    s = (item.get("params") or {}).get("set")
                    if s and item.get("at_hours") is not None:
                        out[s] = float(item["at_hours"])
        return out

    def write(self, out: dict, cat: Catalog, world: World, params: dict, events_used: int, us: Us):
        c = self.c()
        with c.transaction(), c.cursor() as cur:
            cur.execute("""insert into hub.model_runs (tick, events_used, params, summary) values (%s, %s, %s, %s)
                           returning run_id""",
                        (world.now_tick, events_used, Jsonb(params),
                         Jsonb({"selftest": out["selftest"], "teams": len(out["teams"]), "obs": len(out["evidence"]),
                                "opps": len(out["opps"]), "us": us.team})))
            run = cur.fetchone()[0]
            for t in ("team_mult", "team_card_value", "opportunities", "evidence"):
                cur.execute(f"delete from hub.{t}")
            cur.executemany("""insert into hub.team_mult (team, set, e_mult, p_mult, top, p_top, n_obs, run_id)
                               values (%s, %s, %s, %s, %s, %s, %s, %s)""",
                            [(t, s, e, Jsonb(pm), top, pt, n, run) for t, s, e, pm, top, pt, n in out["mult_rows"]])
            cur.executemany("""insert into hub.team_card_value (team, card, set, rarity, e_value, q25, q75, p_lacks,
                               p_completes, known_copies, run_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            [v + (run,) for v in out["values"]])
            cur.executemany("""insert into hub.opportunities (run_id, kind, card, seller, buyer, price, our_value,
                               their_value, p_fill, exp_gain, p_completes, feeding, why)
                               values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            [(run, o["kind"], o["card"], o["seller"], o["buyer"], o["price"], o["our_value"],
                              o["their_value"], o["p_fill"], o["exp_gain"], o["p_completes"], o["feeding"], o["why"])
                             for o in out["opps"]])
            cur.executemany("""insert into hub.evidence (run_id, team, set, card, kind, price, tick, shift, detail)
                               values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            [(run, o.team, s, o.card, o.kind, o.price, o.tick, sh, Jsonb(o.detail))
                             for o, s, sh in out["evidence"]])
        return run


def print_summary(out: dict, cat: Catalog, us: Us):
    st = out["selftest"]
    if st:
        print(f"self-test on {us.team}: true order ranks {st['rank_of_truth']}/{st['of']} (P={st['p_truth']:.3f}); "
              "P(true multiplier): " + ", ".join(f"{s} {v:.2f}" for s, v in st["p_true_mult"].items()))
    print("team multipliers (most likely, P):")
    by_team = defaultdict(list)
    for t, s, e, pm, top, pt, n in out["mult_rows"]:
        by_team[t].append(f"{s} {top:.1f}({pt:.0%},n{n})")
    for t in sorted(by_team, key=lambda x: int(x[1:]) if x[1:].isdigit() else 0):
        print(f"  {t}: " + " ".join(by_team[t]))
    print("top opportunities:")
    for o in out["opps"][:15]:
        print(f"  {o['kind']:5} {o['card']:7} {o['seller'] or '':>4} → {o['buyer'] or '':4} at {o['price']} · "
              f"E[gain] {o['exp_gain']:.1f} · {o['feeding']} · {o['why']}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--every", type=int, default=0, help="seconds between runs")
    ap.add_argument("--dry-run", action="store_true", help="compute and print; write nothing")
    ap.add_argument("--selftest", action="store_true", help="print the summary and the self-test")
    a = ap.parse_args(argv)
    reader, world, cat = Reader(), None, None
    while True:
        t0 = time.time()
        try:
            if cat is None:
                cat = reader.catalog()
            if world is not None and reader.late_arrivals(world) != 0:
                print(time.strftime("%H:%M:%S"), "late or backfilled events in the hub: rebuilding", flush=True)
                world = None
            if world is None:
                world = World()
                evs = reader.events()
            else:
                evs = reader.events(world.max_id)
            world.ingest(evs, cat)
            snaps = reader.snapshots()
            try:
                me = fetch_me()
            except Exception as e:
                print("me: unavailable,", type(e).__name__, flush=True)
                me = None
            us = load_us(me, snaps)
            out = compute(world, cat, us, snaps, reader.released_at(cat))
            if a.selftest or a.dry_run:
                print_summary(out, cat, us)
            if not a.dry_run:
                run = reader.write(out, cat, world, PARAMS, world.max_id, us)
                st = out["selftest"] or {}
                print(time.strftime("%H:%M:%S"), f"run {run} · tick {world.now_tick} · +{len(evs)} events · "
                      f"{len(out['evidence'])} obs · {len(out['opps'])} opps · self-test rank "
                      f"{st.get('rank_of_truth')}/{st.get('of')} · {time.time() - t0:.1f}s", flush=True)
        except Exception as e:
            print(time.strftime("%H:%M:%S"), "error:", type(e).__name__, redact(e)[:200], flush=True)
            reader.conn = None
            if a.once:
                raise
        if a.once or not a.every:
            return
        time.sleep(max(5, a.every - (time.time() - t0)))


if __name__ == "__main__":
    sys.exit(main())
