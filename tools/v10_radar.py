"""v10 radar: find the team that should buy each ask on our stall, and hand Lucas a ready DM (Chief, Sat 11:55).

Value created on our stall v10 (buyer's value − seller's value, when two OTHER teams trade there) scores market
points for us; one good trade ≈ +5 board, a bad one (−10.2) cost us. Every tick this reads v10's public board and,
for each ask (cards for cash), ranks the likely buyers with the bots' buyer model:
- collects the set (tools/collectors.py: teams.md "collects", feed bids ≥ half book, dealer asks; "dumps" vetoes);
- lacks that card (opportunities.read_signals: a bid or dealer ask for it not followed by getting one);
- creates value: est. value created = book × (m_buyer × c_buyer − m_seller × c_seller), m from the Analyst's
  intel/multipliers.json where its confidence is V or L, else the hub's demand model (hub.team_mult), else 1.0 [L] and c the copy weight (values rules: 1st copy 1.0, 2nd 0.25, 3rd 0.10): the seller
  gives up its last copy, the buyer gains its next. Copies are counted from the feed (settlements, pack pulls,
  listings), so they are lower bounds: starting cards are invisible [L]. Analyst, Sat 12:05: a high-multiplier team
  selling a duplicate to a lower-multiplier collector creates value (v14 +4.36, v17 +2.76 [V]).
Never the top 4, never the seller or us, and never a team within 10 points of us for a card that may close its page
(it lacks at most one other card of the set). The conservative estimate (buyer's low multiplier, seller's high) must be above 0. A strong match pages Lucas once per (ask, buyer) with a ready WhatsApp DM
and is logged to intel/v10-radar.md. Read-only: it never trades.

Partner suggestions (Chief 15:45): every 30 min, for each partner (Teams 10, 15, 3), the cards it holds 2+ copies of
(feed) and the best buyer for each (the same buyer model, top 5 excluded, est. value created > +5 copy-weighted, no
page-closer to a team within 10 points of us); at most 3 lines per partner, written to intel/v10-suggestions.md and
sent to Lucas as a ready message per partner ("Suggestions for v10: your <card> (you hold 2) -> Team Y at ~P; ...").

Addressed offers (Chief 12:55): the public board hides offers on v10 made `to` one team, which are the trades that
score for us (Team 10 → t03 LAV-04 at 13, → t17 MAL-02 at 6). So it also reads offer.listed events on v10 from
data/feed.jsonl, keeps the open ones (not cancelled, not expired, no settlement of its card since), and for each one
addressed to another team pages Lucas once with a DM to that team ("Team 10 has an offer for you on v10: ..."), when
the estimated value created (midpoint) is above 0; otherwise it only logs it.

    python3 -u tools/v10_radar.py            # every tick (tools/daemons.sh start radar)
    python3 tools/v10_radar.py --once --dry  # print, send and write nothing
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
sys.path.insert(0, str(ROOT / "tools"))
from bazaar_sdk import _Http  # noqa: E402
from collectors import CachedCollectors, set_of  # noqa: E402
import opportunities as op  # noqa: E402

URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
VENUE, ME = "v10", "t05"
OUT, STATE, FEED = ROOT / "intel" / "v10-radar.md", ROOT / "run" / "v10_radar_state.json", ROOT / "data" / "feed.jsonl"
SUGGEST_OUT, SUGGEST_EVERY_S = ROOT / "intel" / "v10-suggestions.md", 1800
PARTNER_TEAMS = ("t10", "t15", "t03")
SUGGEST_VC, SUGGEST_LINES, SUGGEST_TOP = 5.0, 3, 5
CLEARING = {"common": 9, "uncommon": 24.5, "rare": 70}   # GAME.md clearing prices: the price to suggest
CLEARING_SET = {("LAT", "common"): 7.5, ("LAT", "uncommon"): 21.5, ("MAL", "uncommon"): 26}   # GAME.md, per set
DESK = ("dani", "lucas")   # Dani is the human deal desk (Lucas, Sat 16:10): every "message a team" alert goes to both
MULT_FILE = ROOT / "intel" / "multipliers.json"   # the Analyst's estimates: {team: {SET: {m, lo, hi, conf, why}}}
MIN_VC = 5.0          # est. value created for a buyer that hasn't shown it lacks the card
COPY = (1.0, 0.25, 0.10)   # what the 1st, 2nd, 3rd copy of a card is worth (catalog values.copy_marginals)
FEED_GAP = 6          # a page-closing card only to teams at least this far below us (policy.PAGE_CLOSER_GAP)
SET_NAMES = {"SAL": "Salamanca", "LAT": "La Latina", "LAV": "Lavapiés", "MAL": "Malasaña", "RET": "El Retiro",
             "CHA": "Chamberí"}
HEADER = ("# v10 radar: buyers for the asks on our stall\n\n_Written by `tools/v10_radar.py`. Each line: an ask on v10, "
          "the likely buyer, why, and the DM sent to Lucas. Est. value created = book × (buyer's multiplier × "
          "copy weight − seller's), multipliers from intel/multipliers.json (the Analyst, conf V/L), else the hub's "
          "model [L]._\n\n")

try:
    from notify import notify as _notify
except Exception:  # noqa: BLE001
    _notify = None


def hub_mult() -> dict:
    """{team: {set: e_mult}} from the hub's latest model run; {} when the hub isn't reachable."""
    try:
        sys.path.insert(0, str(ROOT))
        from hub.db import connect
        with connect("reader") as c:
            cur = c.cursor()
            cur.execute("select team, set, e_mult from hub.team_mult where run_id = (select max(run_id) from hub.team_mult)")
            out: dict = {}
            for team, s, e in cur.fetchall():
                out.setdefault(team, {})[s] = float(e)
            return out
    except Exception:  # noqa: BLE001
        return {}


def _triple(v) -> tuple:
    return tuple(v) if isinstance(v, (tuple, list)) else (float(v), float(v), float(v))


def load_mult(hub: dict, path: Path = MULT_FILE) -> dict:
    """{team: {set: (m, lo, hi)}}: the Analyst's estimates where conf is V or L (intel/multipliers.json), else the hub's
    (m = lo = hi)."""
    out = {t: {s: _triple(v) for s, v in sets.items()} for t, sets in (hub or {}).items()}
    try:
        data = json.loads(Path(path).read_text())
    except (OSError, ValueError):
        data = {}
    for team, sets in data.items():
        if team.startswith("_") or not isinstance(sets, dict):
            continue
        for st, v in sets.items():
            if isinstance(v, dict) and v.get("conf") in ("V", "L") and isinstance(v.get("m"), (int, float)):
                out.setdefault(team, {})[st] = (float(v["m"]), float(v.get("lo", v["m"])), float(v.get("hi", v["m"])))
    return out


def load_events(path: Path = FEED) -> list:
    events = []
    try:
        with path.open() as f:
            for line in f:
                try:
                    events.append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        pass
    return sorted((e for e in events if isinstance(e.get("tick"), int) and e.get("id") is not None),
                  key=lambda e: (e["tick"], e["id"]))


def card_index(catalog: dict) -> dict:
    return {c["id"]: {"set": s["id"], "rarity": c["rarity"], "book": c["book"], "name": c.get("name", c["id"])}
            for s in catalog.get("sets", []) for c in s.get("cards", [])}


def sellers(events) -> dict:
    """offer id → the team that listed it (the board shows a pseudonym; the feed names the maker)."""
    out = {}
    for e in events:
        if e.get("type") == "offer.listed":
            o = (e.get("payload") or {}).get("offer") or {}
            if o.get("id") is not None:
                out[o["id"]] = o.get("maker") if op.is_team(o.get("maker")) else e.get("actor")
    return out


def holdings(events) -> dict:
    """(team, card) → asset ids it holds as far as the feed shows (received or listed, not sent): a lower bound."""
    held: dict = {}
    for e in events:
        p = e.get("payload") if isinstance(e.get("payload"), dict) else {}
        if e.get("type") == "settlement":
            for i in p.get("items") or []:
                if i.get("kind") == "card" and i.get("id") is not None:
                    held.setdefault((i.get("to"), i.get("ref")), set()).add(i["id"])
                    held.get((i.get("frm"), i.get("ref")), set()).discard(i["id"])
        elif e.get("type") == "pack.opened" and (p.get("best") or {}).get("id") is not None:
            b = p["best"]
            held.setdefault((p.get("team"), b.get("ref")), set()).add(b["id"])
        elif e.get("type") == "offer.listed":
            o = p.get("offer") or {}
            maker = o.get("maker") if op.is_team(o.get("maker")) else e.get("actor")
            for a in (o.get("give") or {}).get("assets") or []:
                if isinstance(a, dict) and a.get("id") is not None and a.get("ref"):
                    held.setdefault((maker, a["ref"]), set()).add(a["id"])
    return held


def copy_weight(n_after: int) -> float:
    """Weight of the n-th copy (1-based)."""
    return COPY[min(max(n_after, 1), len(COPY)) - 1]


def buyers_for(ask: dict, *, seller, teams, top, ours, last, prof, mult, collectors, cards, held=None) -> list[dict]:
    """Ranked likely buyers for one ask: [{team, rank, m_buyer, m_seller, vc, lacks, why}]."""
    refs = [a.get("ref") for a in (ask.get("give") or {}).get("assets") or [] if isinstance(a, dict)]
    if len(refs) != 1 or refs[0] not in cards:
        return []
    card = refs[0]
    c = cards[card]
    st, book = c["set"], c["book"]
    m_s, _, hi_s = _triple((mult.get(seller) or {}).get(st, 1.0)) if seller else (1.0, 1.0, 1.0)
    held = held or {}
    c_s = copy_weight(len(held.get((seller, card), ())) or 1)      # the seller gives up its last copy
    out = []
    for t in teams:
        team = t["team"]
        if team in (ME, seller) or team in top:
            continue
        ok, why = collectors.allows(team, st)
        p = prof.get((team, st), {})
        if not ok and not p.get("collects"):
            continue
        if "dumps" in why:
            continue
        sig = last.get((team, card))
        n_b = len(held.get((team, card), ()))
        if sig and sig["kind"] == "hold":
            n_b = max(n_b, 1)
        lacks = bool(sig and sig["kind"] == "lack") and n_b == 0
        m_b, lo_b, _ = _triple((mult.get(team) or {}).get(st, 1.0))
        c_b = copy_weight(n_b + 1)                      # the buyer gains its next copy
        vc = round(book * (m_b * c_b - m_s * c_s), 1)
        vc_low = round(book * (lo_b * c_b - hi_s * c_s), 1)   # conservative: buyer at lo, seller at hi (Analyst)
        if vc_low <= 0 or (not lacks and vc < MIN_VC):
            continue
        others = [k for k, x in last.items() if k[0] == team and k[1] != card and x["kind"] == "lack"
                  and cards.get(k[1], {}).get("set") == st]
        gap = None if t.get("score") is None or ours is None else ours - t["score"]
        if len(others) <= 1 and (gap is None or gap < FEED_GAP):
            continue                                   # may close its page and it's within 10 points of us
        out.append({"team": team, "name": t.get("name", team), "rank": t.get("rank"), "m_buyer": round(m_b, 2),
                    "m_seller": round(m_s, 2), "c_buyer": c_b, "c_seller": c_s, "vc": vc, "vc_low": vc_low,
                    "lacks": lacks,
                    "why": why if ok else "bought or bid for the set"})
    out.sort(key=lambda b: (not b["lacks"], -b["vc"]))
    return out


def value_created(book, m_b, m_s, c_b, c_s) -> tuple[float, float]:
    """(est., conservative) value created when the buyer (m_b, its next copy c_b) gets a card from the seller."""
    (mb, lob, _), (ms, _, his) = _triple(m_b), _triple(m_s)
    return round(book * (mb * c_b - ms * c_s), 1), round(book * (lob * c_b - his * c_s), 1)


def open_addressed(events, tick) -> list[dict]:
    """Offers on v10 made `to` one team that are still open as far as the feed shows: listed, not cancelled, not
    expired, and no settlement of their card (an ask) or between the two teams on v10 (a bid) since they were listed."""
    listed = {}
    for e in events:
        p = e.get("payload") if isinstance(e.get("payload"), dict) else {}
        if e.get("type") == "offer.listed":
            o = p.get("offer") or {}
            if o.get("venue") == VENUE and o.get("to") and o.get("id") is not None:
                maker = o.get("maker") if op.is_team(o.get("maker")) else e.get("actor")
                listed[o["id"]] = {**o, "maker": maker, "_assets": {a.get("id") for a in (o.get("give") or {}).get(
                    "assets") or [] if isinstance(a, dict)}}
        elif e.get("type") == "offer.cancelled":
            listed.pop(p.get("offer"), None)
        elif e.get("type") == "settlement":
            moved = {i.get("id") for i in p.get("items") or []}
            parties = set(p.get("parties") or [])
            for oid, o in list(listed.items()):
                if e.get("tick", 0) >= (o.get("created_tick") or 0) and (
                        o["_assets"] & moved or (p.get("venue") == VENUE and {o["maker"], o["to"]} <= parties)):
                    listed.pop(oid)
    return [o for o in listed.values() if (o.get("expires_tick") or 0) > tick and o["to"] != ME and o["maker"] != ME]


def addressed_match(o: dict, *, teams, mult, cards, held) -> dict | None:
    """One addressed offer as a radar row: who buys, who sells, the card, the estimated value created."""
    give, want = o.get("give") or {}, o.get("want") or {}
    assets = [a for a in give.get("assets") or [] if isinstance(a, dict)]
    if len(assets) == 1 and want.get("cash") and not give.get("cash"):
        card, price, buyer, seller = assets[0].get("ref"), want["cash"], o["to"], o["maker"]       # an ask to them
    else:
        wanted = list(want.get("cards") or []) + [t[5:] for t in want.get("types") or [] if t.startswith("card:")]
        wanted += [a.get("ref") for a in want.get("assets") or [] if isinstance(a, dict)]
        if len(wanted) != 1 or not give.get("cash"):
            return None
        card, price, buyer, seller = wanted[0], give["cash"], o["maker"], o["to"]                 # a bid to them
    c = cards.get(card)
    if not c:
        return None
    st = c["set"]
    m_b, m_s = (mult.get(buyer) or {}).get(st, 1.0), (mult.get(seller) or {}).get(st, 1.0)
    c_b = copy_weight(len(held.get((buyer, card), ())) + 1)
    c_s = copy_weight(len(held.get((seller, card), ())) or 1)
    vc, vc_low = value_created(c["book"], m_b, m_s, c_b, c_s)
    names = {t["team"]: t.get("name", t["team"]) for t in teams}
    rank = {t["team"]: t.get("rank") for t in teams}
    return {"offer": o["id"], "addressed": True, "maker": o["maker"], "maker_name": names.get(o["maker"], o["maker"]),
            "team": o["to"], "name": names.get(o["to"], o["to"]), "rank": rank.get(o["to"]), "card": card,
            "price": price, "side": "ask" if buyer == o["to"] else "bid", "seller": seller, "vc": vc, "vc_low": vc_low,
            "m_buyer": round(_triple(m_b)[0], 2), "m_seller": round(_triple(m_s)[0], 2), "c_buyer": c_b, "c_seller": c_s,
            "expires_tick": o.get("expires_tick")}


def suggestions(partner: str, *, teams, held, mult, cards, last, prof, collectors, ours) -> list[dict]:
    """Up to SUGGEST_LINES {card, n, buyer, name, price, vc} for one partner: its 2+ copy cards, each with its best
    buyer outside the top SUGGEST_TOP (buyers_for), est. value created > SUGGEST_VC."""
    top = {t["team"] for t in teams[:SUGGEST_TOP]} | {"t13", "t17"}   # policy: rivals' gains vs ours unknown
    out = []
    for (team, card), ids in held.items():
        if team != partner or len(ids) < 2 or card not in cards:
            continue
        ask = {"give": {"assets": [{"ref": card}]}}
        ranked = [b for b in buyers_for(ask, seller=partner, teams=teams, top=top, ours=ours, last=last, prof=prof,
                                        mult=mult, collectors=collectors, cards=cards, held=held)
                  if b["vc"] > SUGGEST_VC]
        rarity, st = cards[card]["rarity"], cards[card]["set"]
        if ranked and rarity in CLEARING:              # epics and legendaries: no clearing price, no suggestion
            b = ranked[0]
            worth = cards[card]["book"] * b["m_buyer"] * b["c_buyer"]   # never suggest above the buyer's value
            price = max(1, round(min(CLEARING_SET.get((st, rarity), CLEARING[rarity]), worth)))
            out.append({"card": card, "n": len(ids), "buyer": b["team"], "name": b["name"], "vc": b["vc"],
                        "price": price})
    out.sort(key=lambda x: -x["vc"])
    return out[:SUGGEST_LINES]


# Ready-to-send texts are transactional only (Lucas, Sat 17:20): what, offer id, price, thanks. Never why: no value
# created, multipliers, collections or page status; rivals learn from it.

def suggestion_text(lines: list[dict], cards: dict) -> str:
    return "Suggestions for v10: " + "; ".join(
        f"your {cards.get(x['card'], {}).get('name', x['card'])} ({x['card']}) → {x['name']} at ~{x['price']} P"
        for x in lines) + ". Thanks!"


def dm_addressed(f: dict, card_name: str) -> str:
    if f["side"] == "ask":
        return (f"Hi {f['name']}! {f['maker_name']} has an offer for you on v10: {card_name} ({f['card']}) for "
                f"{f['price']} P, offer {f['offer']}. Thanks!")
    return (f"Hi {f['name']}! {f['maker_name']} offers you {f['price']} P for your {card_name} ({f['card']}) on v10, "
            f"offer {f['offer']}. Thanks!")


def dm(team_name: str, card_name: str, card: str, price, set_id: str = "", offer=None) -> str:
    return f"Hi {team_name}! {card_name} ({card}) is on v10 for {price} P{f', offer {offer}' if offer else ''}. Thanks!"


class Radar:
    def __init__(self, pub, *, events_fn=load_events, mult_fn=hub_mult, collectors=None, notifier=_notify,
                 out: Path = OUT, state: Path = STATE, log=print, dry=False, mult_file: Path = MULT_FILE):
        self.pub, self.events_fn, self.mult_fn, self.notifier = pub, events_fn, mult_fn, notifier
        self.collectors = collectors or CachedCollectors()
        self.out, self.state_path, self.log, self.dry, self.mult_file = out, state, log, dry, mult_file
        self._hub: dict = {}
        try:
            self.state = json.loads(state.read_text())
        except (OSError, ValueError):
            self.state = {"alerted": []}
        self.cards, self._cat_at, self.mult, self._mult_at = {}, 0.0, {}, 0.0
        self._suggest_at = 0.0
        self._clock: dict = {}

    def scan(self) -> list[dict]:
        now = time.time()
        if not self.cards or now - self._cat_at > 600:
            self.cards, self._cat_at = card_index(self.pub._call("GET", "/api/catalog")), now
        if now - self._mult_at > 600:
            self._hub, self._mult_at = self.mult_fn() or self._hub, now
        self.mult = load_mult(self._hub, self.mult_file)    # the Analyst's file is re-read every scan
        board = self.pub._call("GET", f"/api/venues/{VENUE}/offers").get("offers") or []
        asks = [o for o in board if (o.get("give") or {}).get("assets") and (o.get("want") or {}).get("cash")
                and not (o.get("give") or {}).get("cash") and not o.get("to")]
        events = self.events_fn()
        self._clock = self.pub._call("GET", "/api/clock") or {}
        tick = self._clock.get("tick") or (events[-1]["tick"] if events else 0)
        direct = open_addressed(events, tick)
        if not asks and not direct:
            return []
        teams = sorted(self.pub._call("GET", "/api/leaderboard").get("teams") or [], key=lambda t: -(t.get("score") or 0))
        for i, t in enumerate(teams):
            t["rank"] = i + 1
        top = {t["team"] for t in teams[:5]} | {"t13", "t17"}   # policy: top 5; rivals' gains vs ours unknown
        ours = next((t.get("score") for t in teams if t["team"] == ME), None)
        last, prof = op.read_signals(events, [], ME, op.GameTime(events), tick, self.cards)
        who = sellers(events)
        held = holdings(events)
        col = self.collectors.get()
        found = []
        for a in asks:
            seller = who.get(a["id"])
            ranked = buyers_for(a, seller=seller, teams=teams, top=top, ours=ours, last=last, prof=prof, mult=self.mult,
                                collectors=col, cards=self.cards, held=held)
            for b in ranked[:2]:
                found.append({"offer": a["id"], "seller": seller, "price": (a.get("want") or {}).get("cash"),
                              "card": [x.get("ref") for x in a["give"]["assets"]][0],
                              "expires_tick": a.get("expires_tick"), **b})
        for o in direct:
            m = addressed_match(o, teams=teams, mult=self.mult, cards=self.cards, held=held)
            if m:
                found.append(m)
        for f in found:
            key = f"{f['offer']}:{f['team']}"
            if self.dry or key in self.state["alerted"]:
                continue
            (self.alert_addressed if f.get("addressed") else self.alert)(f, tick)
            self.state["alerted"].append(key)
        if not self.dry:
            self.state["alerted"] = self.state["alerted"][-500:]
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            self.state_path.write_text(json.dumps(self.state))
        return found

    def until(self, expires_tick, tick) -> str:
        """'~HH:MM' wall time an offer expires (the clock's tick length); '?' when unknown."""
        secs = float(self._clock.get("tick_seconds") or 30)
        if expires_tick is None or tick is None:
            return "?"
        return "~" + time.strftime("%H:%M", time.localtime(time.time() + max(0, expires_tick - tick) * secs))

    def desk(self, title: str, body: str, **kw) -> None:
        for who in DESK:
            self.notifier(who, title, body, **kw)

    def alert(self, f: dict, tick) -> None:
        c = self.cards.get(f["card"], {})
        text = dm(f["name"], c.get("name", f["card"]), f["card"], f["price"], offer=f["offer"])
        why = (f"{'lacks it' if f['lacks'] else 'collects ' + c.get('set', '')}, multiplier {f['m_buyer']} × copy "
               f"{f['c_buyer']:g} vs seller {f['seller'] or '?'} {f['m_seller']} × copy {f['c_seller']:g}: est. value "
               f"created +{f['vc']:g} (at least +{f['vc_low']:g}) on v10")
        self.log(f"v10 radar: offer {f['offer']} {f['card']} at {f['price']} → {f['team']} (#{f['rank']}) · {why}")
        if not self.out.exists():
            self.out.parent.mkdir(parents=True, exist_ok=True)
            self.out.write_text(HEADER)
        with self.out.open("a") as fh:
            fh.write(f"- {time.strftime('%a %H:%M')} · tick {tick} · offer {f['offer']} · {f['card']} at {f['price']} P "
                     f"(seller {f['seller'] or '?'}) → **{f['name']}** (#{f['rank']}) · {why} · DM: \"{text}\"\n")
        if self.notifier:
            self.desk(f"v10: DM {f['name']} about {f['card']} ({f['price']} P)",
                      f"Offer {f['offer']} on v10, valid until {self.until(f.get('expires_tick'), tick)}.\n{why}.\n"
                      f"DM to send:\n{text}", priority=4, tags=["handshake"])


    def suggest(self, out: Path = None) -> dict:
        """{partner: lines}; written to intel/v10-suggestions.md and sent to Lucas, one message per partner."""
        out = out or SUGGEST_OUT
        if not self.cards:
            self.cards = card_index(self.pub._call("GET", "/api/catalog"))
        if not self._hub:                             # the first run after a start: the hub model too, not 1.0
            self._hub, self._mult_at = self.mult_fn() or {}, time.time()
        self.mult = load_mult(self._hub, self.mult_file)
        teams = sorted(self.pub._call("GET", "/api/leaderboard").get("teams") or [], key=lambda t: -(t.get("score") or 0))
        names = {t["team"]: t.get("name", t["team"]) for t in teams}
        ours = next((t.get("score") for t in teams if t["team"] == ME), None)
        events = self.events_fn()
        tick = events[-1]["tick"] if events else 0
        last, prof = op.read_signals(events, [], ME, op.GameTime(events), tick, self.cards)
        held, col = holdings(events), self.collectors.get()
        found = {p: suggestions(p, teams=teams, held=held, mult=self.mult, cards=self.cards, last=last, prof=prof,
                                collectors=col, ours=ours) for p in PARTNER_TEAMS}
        L = [f"# v10 partner suggestions ({time.strftime('%a %H:%M')}, tick {tick})", "",
             "_Written every 30 min by `tools/v10_radar.py`: for Teams 10, 15 and 3, the cards each holds 2+ copies of "
             "(feed, a lower bound) and the best buyer outside the top 5 (est. value created > +5, copy-weighted; no "
             "page-closer to a team within 10 points of us). Est. [L]. Price: the rarity's clearing price._", ""]
        for p in PARTNER_TEAMS:
            lines = found[p]
            L.append(f"## {names.get(p, p)} ({p})")
            if not lines:
                L += ["", "No pair clears +5 now.", ""]
                continue
            L += [""] + [f"- {x['card']} (holds {x['n']}) → {x['name']} ({x['buyer']}) at ~{x['price']} P · est. value "
                         f"created +{x['vc']:g}" for x in lines]
            text = suggestion_text(lines, self.cards)
            L += ["", f"Message: \"{text}\"", ""]
            sent = self.state.setdefault("suggested", {})
            if self.notifier and not self.dry and sent.get(p) != text:   # only when it changed
                until = time.strftime("%H:%M", time.localtime(time.time() + SUGGEST_EVERY_S))
                self.desk(f"v10 suggestions for {names.get(p, p)}",
                          f"For {names.get(p, p)} (no offer yet: they list it on v10). Valid until ~{until} (next "
                          f"refresh).\n{text}", priority=3, tags=["handshake"])
                sent[p] = text
        if not self.dry:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text("\n".join(L) + "\n")
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            self.state_path.write_text(json.dumps(self.state))
        return found

    def alert_addressed(self, f: dict, tick) -> None:
        c = self.cards.get(f["card"], {})
        text = dm_addressed(f, c.get("name", f["card"]))
        left = (f.get("expires_tick") or tick) - tick
        why = (f"{f['maker_name']} → {f['name']} (#{f['rank']}), {f['side']} {f['card']} at {f['price']} P, {left} ticks "
               f"left; buyer {f['m_buyer']} × copy {f['c_buyer']:g} vs seller {f['m_seller']} × copy {f['c_seller']:g}: "
               f"est. value created {f['vc']:+g} (at least {f['vc_low']:+g}) on v10")
        paged = f["vc"] > 0 and self.notifier is not None
        self.log(f"v10 radar: addressed offer {f['offer']} · {why} · {'paged' if paged else 'not paged (est. ≤ 0)'}")
        if not self.out.exists():
            self.out.parent.mkdir(parents=True, exist_ok=True)
            self.out.write_text(HEADER)
        with self.out.open("a") as fh:
            fh.write(f"- {time.strftime('%a %H:%M')} · tick {tick} · addressed offer {f['offer']} · {why} · "
                     f"{'DM' if paged else 'not paged, DM'}: \"{text}\"\n")
        if paged:
            self.desk(f"v10: {f['maker_name']} has an offer for {f['name']} ({f['card']} {f['price']} P)",
                      f"Offer {f['offer']} on v10, valid until {self.until(f.get('expires_tick'), tick)}.\n{why}.\n"
                      f"DM {f['name']} to accept:\n{text}", priority=5, tags=["handshake"])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry", action="store_true", help="print, send and write nothing")
    args = ap.parse_args(argv)
    pub = _Http(URL, {}, 15.0, False, 0)
    r = Radar(pub, dry=args.dry)
    while True:
        try:
            if time.time() - r._suggest_at >= SUGGEST_EVERY_S:
                r._suggest_at = time.time()
                sug = r.suggest()
                print(f"{time.strftime('%H:%M:%S')} v10 suggestions: "
                      + ", ".join(f"{p} {len(x)}" for p, x in sug.items()), flush=True)
            found = r.scan()
            print(f"{time.strftime('%H:%M:%S')} v10 radar: {len(found)} match(es)"
                  + "".join(f" · {'addressed ' if f.get('addressed') else ''}{f['card']} → {f['team']} ({f['vc']:+g})"
                            for f in found[:5]), flush=True)
            c = pub._call("GET", "/api/clock")
            wait = 30.0 if c.get("paused") or c.get("doors") not in (None, "open") else float(c.get("next_tick_in", 10))
        except Exception as e:  # noqa: BLE001  a watcher keeps watching
            print(time.strftime("%H:%M:%S"), "v10 radar error:", repr(e)[:200], flush=True)
            wait = 15.0
        if args.once:
            return
        time.sleep(max(2.0, wait + 1.0))


if __name__ == "__main__":
    main()
