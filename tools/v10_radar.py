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
MULT_FILE = ROOT / "intel" / "multipliers.json"   # the Analyst's estimates: {team: {SET: {m, lo, hi, conf, why}}}
MIN_VC = 5.0          # est. value created for a buyer that hasn't shown it lacks the card
COPY = (1.0, 0.25, 0.10)   # what the 1st, 2nd, 3rd copy of a card is worth (catalog values.copy_marginals)
FEED_GAP = 10         # a page-closing card only to teams at least this far below us
SET_NAMES = {"SAL": "Salamanca", "LAT": "La Latina", "LAV": "Lavapiés", "MAL": "Malasaña", "RET": "El Retiro",
             "CHA": "Chamberí"}
HEADER = ("# v10 radar: buyers for the asks on our stall\n\n_Written by `tools/v10_radar.py`. Each line: an ask on v10, "
          "the likely buyer, why, and the DM sent to Lucas. Est. value created = book × (buyer's multiplier − "
          "seller's), multipliers from the hub's model [L]._\n\n")

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


def dm(team_name: str, card_name: str, card: str, price, set_id: str) -> str:
    return (f"Hi {team_name}! There's {card_name} ({card}) for {price} P on the market v10 (0% fee), in case you need "
            f"it for your {SET_NAMES.get(set_id, set_id)} page.")


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
        if not asks:
            return []
        teams = sorted(self.pub._call("GET", "/api/leaderboard").get("teams") or [], key=lambda t: -(t.get("score") or 0))
        for i, t in enumerate(teams):
            t["rank"] = i + 1
        top = {t["team"] for t in teams[:4]}
        ours = next((t.get("score") for t in teams if t["team"] == ME), None)
        events = self.events_fn()
        tick = self.pub._call("GET", "/api/clock").get("tick") or (events[-1]["tick"] if events else 0)
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
                              "card": [x.get("ref") for x in a["give"]["assets"]][0], **b})
        for f in found:
            key = f"{f['offer']}:{f['team']}"
            if self.dry or key in self.state["alerted"]:
                continue
            self.alert(f, tick)
            self.state["alerted"].append(key)
        if not self.dry:
            self.state["alerted"] = self.state["alerted"][-500:]
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            self.state_path.write_text(json.dumps(self.state))
        return found

    def alert(self, f: dict, tick) -> None:
        c = self.cards.get(f["card"], {})
        text = dm(f["name"], c.get("name", f["card"]), f["card"], f["price"], c.get("set", set_of(f["card"])))
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
            self.notifier("lucas", f"v10: DM {f['name']} about {f['card']} ({f['price']} P)",
                          f"{why}.\nDM to send:\n{text}", priority=4, tags=["handshake"])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry", action="store_true", help="print, send and write nothing")
    args = ap.parse_args(argv)
    pub = _Http(URL, {}, 15.0, False, 0)
    r = Radar(pub, dry=args.dry)
    while True:
        try:
            found = r.scan()
            print(f"{time.strftime('%H:%M:%S')} v10 radar: {len(found)} match(es)"
                  + "".join(f" · {f['card']} → {f['team']} (+{f['vc']:g})" for f in found[:3]), flush=True)
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
