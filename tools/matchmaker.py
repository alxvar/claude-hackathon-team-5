"""Page-finisher matchmaker for v10 (Chief, Sat 21:25). Read-only: it never trades and never sends a message.

The organisers' deck: a market scores when two OTHER teams gain on it, and the best trade in the game is the last card
of a page ("take want-lists and match them with teams holding duplicates"). Every run this:
1. estimates each team's page cards (01-10) from the feed: card ids received, listed or offered to a dealer, minus
   those sent, plus pack pulls and gifts (opportunities.read_signals: the latest hold/lack/gone per team and card).
   A lower bound: on our own album (Sat 21:25) it had no false card and ~80% recall (LAV 7 of 10 seen, SAL 8, RET 8),
   so a "9/10" team may already be complete. A bid or dealer ask for the missing card ("bid") confirms it;
2. for each missing card of a team at 8/10 or 9/10, finds a giver: a true duplicate (2+ distinct copies seen) or the
   only copy of a set it dumps (intel/teams.md; never the only copy of a page the feed shows complete);
3. reads want-lists from intel/wants.md (Lucas, from WhatsApp: `- t07 RET-05 40` = team, card, max price in P; the
   price is optional) and matches them the same way; a bid in the feed is a want too. run/known_holdings.json
   (Chief 21:50: what a team told Lucas, {team: {"complete": [sets], "missing": [cards]}}) beats the feed: such a
   team holds every other page card of those sets and buys only the cards it said it misses;
4. writes intel/matches.md: buyer, card, seller, a price, value created, page-closer and rival flags, and a ready DM
   for each side (transactional only, never why; the giver's DM always says "Only if it's a spare for you, keep one
   copy.").
Hard rule (Chief 21:40, after one swap wiped Team 7's value created): the giver shows a true duplicate or dumps the
set; the receiver shows no copy and collects the set (collectors, a buy or bid in the feed, or a want-list); both
sides gain > 0 at the price with the conservative multipliers (seller's high, buyer's low), else no match. Never a
page-closer for a rival (policy.rivals: top 6 or within 3 of us; Teams 13/17) or for a team < policy.PAGE_CLOSER_GAP
below us (+50 ≈ +4.7 board could lift it past us). A rival on either side only at a price that keeps its gain <=
RIVAL_GAIN_MAX; both sides rivals: never. Each giver's copies go to one buyer each, best match first.
Rank: page-closers first, then est. value created.

Value: a card is worth book × m × copy weight (1st copy 1.0, 2nd 0.25, 3rd 0.10) to a team, and the last card of a
page adds the page bonus 25% × page book × m. m: the Analyst's intel/multipliers.json (V/L) or the hub's, else 1.0
[L]. Price (fair_price): a team trade scores at most +50 per side, so any price in [max(seller, buyer − 50),
min(buyer, seller + 50)] gives both sides their full gain; inside that window, the market's clearing price for the
rarity (GAME.md), else the midpoint.

    python3 tools/matchmaker.py --once --dry   # print, write nothing
    python3 -u tools/matchmaker.py             # every 5 min (tools/daemons.sh start matchmaker)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
sys.path.insert(0, str(ROOT / "tools"))
import opportunities as op  # noqa: E402
import policy  # noqa: E402
import v10_radar as vr  # noqa: E402
import known as known_mod  # noqa: E402
from collectors import Collectors, from_feed, parse_teams_md  # noqa: E402

URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
ME = "t05"
OUT, WANTS = ROOT / "intel" / "matches.md", ROOT / "intel" / "wants.md"
FEED, LEADERBOARD = ROOT / "data" / "feed.jsonl", ROOT / "data" / "leaderboard.jsonl"
TEAMS_MD, CATALOG_CACHE = ROOT / "intel" / "teams.md", ROOT / "run" / "catalog.json"
KNOWN = known_mod.KNOWN   # run/known_holdings.json: Lucas's facts from the teams themselves (tools/known.py)
EVERY_S = 300
NEAR = 8                   # flag a team with at least this many cards of a page seen
PAGE_BONUS = 0.25          # catalog values.page_bonus
CAP = 50                   # a team trade scores at most +50 per side (GAME.md [V] for the buyer; the seller [L])
RIVAL_GAIN_MAX = 10.0      # a rival on either side: its gain at our suggested price stays <= this (Chief 17:50)
TABLE_LINES, DM_LINES = 20, 8
_CARD = re.compile(r"\b[A-Z]{3}-\d{2}\b")
_TEAM = re.compile(r"\b(?:t|team\s*)(\d{1,2})\b", re.I)
_NUM = re.compile(r"(?<![\w-])(\d+(?:\.\d+)?)\s*(?:P\b|primas?\b|pesetas?\b)?", re.I)
WANTS_HEADER = ("# Want-lists (Lucas, from WhatsApp)\n\nOne line per want: `- t07 RET-05 40` = team, card, max price in P "
                "(the price is optional; `Team 7` works too). `tools/matchmaker.py` re-reads this file every run and "
                "matches each want with a team holding a spare (intel/matches.md). Delete a line once it's done.\n\n")


class _Order:
    """read_signals takes game hours; the matchmaker only needs the order of events."""

    def of(self, e):
        return e.get("t")

    def at(self, tick):
        return None


def load_catalog(cache: Path = CATALOG_CACHE) -> dict:
    """The public catalog (no key); the last copy on disk when the server doesn't answer."""
    try:
        with urllib.request.urlopen(URL.rstrip("/") + "/api/catalog", timeout=15) as r:
            cat = json.load(r)
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(cat))
        return cat
    except Exception:  # noqa: BLE001
        try:
            return json.loads(cache.read_text())
        except (OSError, ValueError):
            return {}


def load_teams(path: Path = LEADERBOARD) -> tuple[list, int | None]:
    """(teams, tick) from the collector's last leaderboard line."""
    try:
        lines = path.read_text().strip().splitlines()
        d = json.loads(lines[-1])
        return d.get("teams") or [], d.get("tick")
    except (OSError, ValueError, IndexError):
        return [], None


def pages(catalog: dict) -> dict:
    """{set: {"cards": [page card ids], "book": page book}}: the page cards are 01-10 (catalog `page`)."""
    out = {}
    for s in catalog.get("sets") or []:
        ids = [c for c in s.get("cards") or [] if c.get("page", int(c["id"].split("-")[1]) <= 10)]
        if ids:
            out[s["id"]] = {"cards": [c["id"] for c in ids], "book": sum(c.get("book") or 0 for c in ids)}
    return out


def counts(events, cards: dict) -> tuple[dict, dict, dict]:
    """((team, card) → copies seen, (team, card) → latest signal, (team, set) → profile). Copies: the distinct asset
    ids v10_radar.holdings sees, or 1 when the latest signal is a hold the ids miss (a gift, a pack pull, an offer to a
    dealer); 0 after a sale."""
    held = vr.holdings(events)
    last, prof = op.read_signals(events, [], ME, _Order(), 0, cards, now_h=0)
    n = {k: len(v) for k, v in held.items() if v}
    for k, sig in last.items():
        if sig["kind"] == "hold":
            n[k] = max(n.get(k, 0), 1)
    return {k: v for k, v in n.items() if v and k[0] and str(k[0]).startswith("t")}, last, prof


def progress(n: dict, pg: dict) -> dict:
    """(team, set) → page cards seen."""
    out: dict = {}
    for (team, card), k in n.items():
        st = card.split("-")[0]
        if k and st in pg and card in pg[st]["cards"]:
            out.setdefault((team, st), set()).add(card)
    return out


def load_known(path: Path | None = None) -> dict:
    """run/known_holdings.json (tools/known.py)."""
    return known_mod.load(path or KNOWN)


def apply_known(n: dict, known: dict, pg: dict) -> dict:
    return known_mod.apply(n, known, {st: p["cards"] for st, p in pg.items()})


def parse_wants(text: str) -> list[dict]:
    """[{team, card, max}] from intel/wants.md lines (`- t07 RET-05 40`, `| Team 7 | RET-05 | 40 |`)."""
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith(("-", "*", "|")) or line.startswith("|--") or line.startswith("| --"):
            continue
        cards, team = _CARD.findall(line), _TEAM.search(line)
        if not cards or not team:
            continue
        rest = _TEAM.sub(" ", _CARD.sub(" ", line))
        nums = [float(x) for x in _NUM.findall(rest)]
        for c in cards:
            out.append({"team": f"t{int(team.group(1)):02d}", "card": c, "max": nums[-1] if nums else None})
    return out


def load_wants(path: Path = WANTS) -> list[dict]:
    try:
        return parse_wants(path.read_text())
    except OSError:
        return []


def fair_price(lo: float, hi: float, clearing: float | None = None) -> int:
    """A price both sides take: any price in [max(lo, hi − CAP), min(hi, lo + CAP)] gives each side its full gain
    (neither side's +50 cap wastes any of it); when hi − lo > 2 × CAP both sides cap anywhere in [lo + CAP, hi − CAP].
    Inside that window, the market's clearing price for the rarity (GAME.md: a price teams already pay), else the
    midpoint; always strictly between the seller's value and the buyer's when there is room."""
    a, b = max(lo, hi - CAP), min(hi, lo + CAP)
    a, b = min(a, b), max(a, b)
    p = round(min(max(clearing if clearing is not None else (lo + hi) / 2, a), b))
    if hi - lo >= 2:
        p = min(max(p, math.floor(lo) + 1), math.ceil(hi) - 1)
    return max(1, p)


def _m(mult: dict, team: str, st: str) -> tuple:
    return vr._triple((mult.get(team) or {}).get(st, 1.0))


def value(book, m, n_copy, closer=False, page_book=0) -> float:
    """What the n-th copy of a card is worth to a team (+ the page bonus when it completes the page)."""
    return book * m * vr.copy_weight(n_copy) + (PAGE_BONUS * page_book * m if closer else 0.0)


def sellers_for(card: str, buyer: str, *, n: dict, prog: dict, pg: dict, dumps: dict) -> list[tuple[str, int, str]]:
    """[(team, copies, why)] that can give `card` (Chief 21:40, hard rule): a true duplicate (2+ distinct copies seen),
    or the only copy of a set it dumps (intel/teams.md) unless the feed shows that page complete."""
    st = card.split("-")[0]
    out = []
    for (team, c), k in n.items():
        if c != card or team in (buyer, ME):
            continue
        if k >= 2:
            out.append((team, k, f"holds {k}"))
        elif st in dumps.get(team, ()) and len(prog.get((team, st), ())) < len(pg[st]["cards"]):
            out.append((team, k, f"dumps {st}"))
    return out


def candidates(*, n, last, prog, pg, wants, cards, known=None) -> dict:
    """(buyer, card) → {sources, max}: the missing cards of teams at NEAR+ of a page, want-lists, bids and known
    wants, each only where the buyer shows no copy of the card (Chief 21:40, hard rule). A team in run/
    known_holdings.json buys only the cards it said it misses (Chief 21:50)."""
    out: dict = {}
    known = known or {}

    def add(team, card, source, mx=None):
        if team == ME or not op.is_team(team) or card not in cards or n.get((team, card)):
            return
        if team in known and card not in known[team]["missing"]:
            return
        c = out.setdefault((team, card), {"sources": [], "max": None})
        if source not in c["sources"]:
            c["sources"].append(source)
        if mx is not None:
            c["max"] = mx
    for (team, st), have in prog.items():
        if len(have) >= NEAR and len(have) < len(pg[st]["cards"]):
            for card in pg[st]["cards"]:
                if card not in have:
                    add(team, card, f"page {len(have)}/{len(pg[st]['cards'])}")
    for w in wants:
        add(w["team"], w["card"], "want-list", w["max"])
    for (team, card), sig in last.items():
        if sig["kind"] == "lack":
            add(team, card, "bid")
    for team, k in known.items():
        for card in sorted(k["missing"]):
            add(team, card, "known want")
    return out


def collects(team: str, st: str, *, coll: Collectors, prof: dict, wanted: bool = False) -> tuple[bool, str]:
    """The receiver collects the set: teams.md, a feed bid or dealer ask (collectors), a buy of the set (read_signals),
    or Lucas's want-list; never a set teams.md says it dumps."""
    ok, why = coll.allows(team, st)
    if "dumps" in why:
        return False, why
    if ok:
        return True, why
    if (prof.get((team, st)) or {}).get("collects"):
        return True, f"{team} bought or bid for {st} (feed)"
    if wanted:
        return True, f"{team} asked for it (want-list)"
    return False, why


def matches(*, events, catalog, teams, wants=(), mult=None, coll: Collectors | None = None, known=None,
            me=ME) -> tuple[list, list, dict, dict]:
    """(matches ranked best first, held back, progress, names). Hard rule (Chief 21:40): the giver shows a true
    duplicate or dumps the set; the receiver shows no copy and collects the set; both sides gain > 0 at the price at
    the conservative multipliers (the seller's high, the buyer's low), else no match."""
    mult = mult or {}
    cards = vr.card_index(catalog)
    pg = pages(catalog)
    known = known or {}
    n, last, prof = counts(events, cards)
    n = apply_known(n, known, pg)
    coll = coll or Collectors({}, from_feed(events))
    dumps = {t: p.get("dumps", set()) for t, p in coll.teams.items()}
    prog = progress(n, pg)
    riv = policy.rivals(teams, me) | set(policy.RIVALS)
    names = {t["team"]: t.get("name", t["team"]) for t in teams}
    cand = candidates(n=n, last=last, prog=prog, pg=pg, wants=list(wants), cards=cards, known=known)
    out, held_back, groups = [], [], []
    for (buyer, card), c in cand.items():
        st, book = cards[card]["set"], cards[card]["book"]
        if st not in pg:
            continue
        wanted = "want-list" in c["sources"] or "known want" in c["sources"]
        ok, _ = collects(buyer, st, coll=coll, prof=prof, wanted=wanted)
        if not ok:
            continue
        have = prog.get((buyer, st), set())
        closer = card in pg[st]["cards"] and len(have) == len(pg[st]["cards"]) - 1
        sig = last.get((buyer, card))
        confirmed = wanted or bool(sig and sig["kind"] == "lack")
        if closer and buyer in riv:
            held_back.append({"buyer": buyer, "card": card, "why": "page-closer for a rival"})
            continue
        g = policy.gap(buyer, teams, me)
        if closer and (g is None or g < policy.PAGE_CLOSER_GAP):
            held_back.append({"buyer": buyer, "card": card,
                              "why": f"page-closer for a team {g if g is None else round(g, 1)} below us "
                                     f"(< {policy.PAGE_CLOSER_GAP})"})
            continue
        m_b, lo_b, _ = _m(mult, buyer, st)
        hi = value(book, m_b, 1, closer, pg[st]["book"])
        hi_cons = value(book, lo_b, 1, closer, pg[st]["book"])
        rows = []
        for seller, k, why in sellers_for(card, buyer, n=n, prog=prog, pg=pg, dumps=dumps):
            if seller in riv and buyer in riv:
                continue
            m_s, _, hi_s = _m(mult, seller, st)
            lo, lo_cons = value(book, m_s, k), value(book, hi_s, k)
            clearing = vr.CLEARING_SET.get((st, cards[card]["rarity"]), vr.CLEARING.get(cards[card]["rarity"]))
            price, note = fair_price(lo_cons, hi_cons, clearing), ""
            if c["max"] is not None and c["max"] < price:
                price, note = max(1, int(c["max"])), f"at their max {c['max']:g}"
            if seller in riv:          # a rival seller gains at most RIVAL_GAIN_MAX
                price = min(price, int(lo + RIVAL_GAIN_MAX))
            if buyer in riv:           # a rival buyer gains at most RIVAL_GAIN_MAX
                price = max(price, int(round(hi - RIVAL_GAIN_MAX)))
                if c["max"] is not None and price > c["max"]:
                    continue
            seller_gain, buyer_gain = round(price - lo_cons, 1), round(hi_cons - price, 1)
            if seller_gain <= 0 or buyer_gain <= 0:
                continue
            rows.append({"buyer": buyer, "buyer_name": names.get(buyer, buyer), "card": card, "card_name":
                         cards[card]["name"], "set": st, "seller": seller, "seller_name": names.get(seller, seller),
                         "seller_why": why, "spare": k - 1 if k >= 2 else 1, "price": price, "vc": round(hi - lo, 1),
                         "vc_low": round(hi_cons - lo_cons, 1), "seller_gain": seller_gain, "buyer_gain": buyer_gain,
                         "seller_value": round(lo, 1), "buyer_value": round(hi, 1), "closer": closer,
                         "confirmed": confirmed, "have": len(have), "page_size": len(pg[st]["cards"]),
                         "sources": c["sources"], "max": c["max"], "rival_buyer": buyer in riv,
                         "rival_seller": seller in riv, "note": note,
                         "bid": sig.get("src") if sig and sig["kind"] == "lack" else None})
        if rows:
            rows.sort(key=lambda r: (r["rival_seller"], -r["vc"], -r["spare"]))
            groups.append(rows)
    left: dict = {}                    # (seller, card) → copies it can still give: its spares, or a dumper's one
    for rows in sorted(groups, key=lambda g: rank(g[0])):
        for r in rows:
            k = (r["seller"], r["card"])
            left.setdefault(k, r["spare"])
            if left[k] > 0:
                left[k] -= 1
                r["also"] = [x["seller"] for x in rows if x is not r]
                r["dm_seller"], r["dm_buyer"] = dm_seller(r), dm_buyer(r)
                out.append(r)
                break
    out.sort(key=rank)
    return out, held_back, prog, names


def rank(r: dict) -> tuple:
    """Page-closers first (Chief 21:25), then value created (Chief 21:40); a rival on either side last among equals."""
    return not r["closer"], -r["vc"], r["rival_buyer"] or r["rival_seller"]


SPARE_LINE = "Only if it's a spare for you, keep one copy."   # Chief 21:40: in every DM to the side that gives a card


def dm_seller(r: dict) -> str:
    """Transactional only (Lucas 17:20): what, where, price, thanks. Never why."""
    return (f"Hi {r['seller_name']}! Could you post your {r['card_name']} ({r['card']}) on v10 as an open ask at "
            f"~{r['price']} P? There's a buyer for it. {SPARE_LINE} Thanks!")


def dm_buyer(r: dict) -> str:
    return (f"Hi {r['buyer_name']}! {r['card_name']} ({r['card']}) can be on v10 soon: post an open bid there at "
            f"~{r['price']} P and it crosses. Thanks!")


def _flags(r: dict) -> str:
    out = []
    if r["rival_buyer"]:
        out.append("buyer")
    if r["rival_seller"]:
        out.append("seller")
    return "rival " + "+".join(out) if out else ""


def render(rows, held_back, prog, names, pg, *, tick=None, now=None, me=ME, riv=frozenset()) -> str:
    stamp = time.strftime("%H:%M", time.localtime(now or time.time()))
    lines = [
        "# v10 matchmaker: page finishers and first copies\n",
        f"_Written by `tools/matchmaker.py` at {stamp} (tick {tick}). Read-only. Holdings are a feed lower bound "
        "(~80% recall on our own album): a missing card may already be held unless the team bid for it or put it on "
        "a want-list (✓). Giver: a true duplicate or a set it dumps; receiver: no copy, collects the set; both gain > 0 "
        "at the price (conservative multipliers). Want-lists: `intel/wants.md`. "
        "Never a page-closer for a rival or a team < "
        f"{policy.PAGE_CLOSER_GAP} below us; a rival on either side gains <= {RIVAL_GAIN_MAX:g} P at our price._\n",
        "## Matches (best first)\n",
    ]
    if rows:
        lines += ["| # | Buyer | Card | Seller | Price | Value created | Closer | Rival | Why |",
                  "|---|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(rows[:TABLE_LINES], 1):
            why = " · ".join(r["sources"]) + (" ✓" if r["confirmed"] else "")
            why += f" · seller {r['seller_why']}" + (f" · also {', '.join(r['also'][:3])}" if r["also"] else "")
            why += f" · {r['note']}" if r["note"] else ""
            lines.append(f"| {i} | {r['buyer_name']} | {r['card']} {r['card_name']} | {r['seller_name']} | "
                         f"~{r['price']} | {r['vc']:+g} (low {r['vc_low']:+g}) | "
                         f"{'**page ' + str(r['have'] + 1) + '/' + str(r['page_size']) + '**' if r['closer'] else ''} | "
                         f"{_flags(r)} | {why} |")
        lines.append("\n## Ready DMs\n")
        for i, r in enumerate(rows[:DM_LINES], 1):
            lines += [f"**{i}. {r['card']} · {r['seller_name']} → {r['buyer_name']} at ~{r['price']} P**",
                      f"- To {r['seller_name']}: \"{r['dm_seller']}\"",
                      f"- To {r['buyer_name']}: \"{r['dm_buyer']}\"\n"]
    else:
        lines.append("No match yet.\n")
    lines.append("## Teams one or two cards from a page (feed lower bound)\n")
    near = sorted(((len(h), team, st) for (team, st), h in prog.items()
                   if st in pg and NEAR <= len(h) < len(pg[st]["cards"]) and team != me), reverse=True)
    for k, team, st in near:
        miss = [c for c in pg[st]["cards"] if c not in prog[(team, st)]]
        lines.append(f"- {names.get(team, team)} {st} {k}/{len(pg[st]['cards'])} · missing {', '.join(miss)}"
                     + (" · rival" if team in riv else ""))
    if not near:
        lines.append("None seen.")
    if held_back:
        lines.append("\n## Held back (never suggested)\n")
        for h in held_back[:15]:
            lines.append(f"- {h['card']} for {names.get(h['buyer'], h['buyer'])}: {h['why']}")
    return "\n".join(lines) + "\n"


def run_once(*, dry=False, out: Path = OUT, wants_path: Path = WANTS, now=None) -> list:
    catalog = load_catalog()
    teams, tick = load_teams()
    events = vr.load_events(FEED)
    try:
        coll = Collectors(parse_teams_md(TEAMS_MD.read_text()), from_feed(events))
    except OSError:
        coll = Collectors({}, from_feed(events))
    try:
        hub = vr.hub_mult()
    except SystemExit:         # hub.db exits when HUB_READER_URL is unset: run without the hub's model
        hub = {}
    mult = vr.load_mult(hub)
    if not wants_path.exists() and not dry:
        wants_path.write_text(WANTS_HEADER)
    rows, held_back, prog, names = matches(events=events, catalog=catalog, teams=teams, wants=load_wants(wants_path),
                                           mult=mult, coll=coll, known=load_known())
    riv = policy.rivals(teams) | set(policy.RIVALS)
    text = render(rows, held_back, prog, names, pages(catalog), tick=tick, now=now, riv=riv)
    if dry:
        print(text)
    else:
        tmp = out.with_suffix(".tmp")
        tmp.write_text(text)
        tmp.replace(out)
    return rows


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], allow_abbrev=False)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry", action="store_true", help="print, write nothing")
    ap.add_argument("--every", type=int, default=EVERY_S)
    args = ap.parse_args(argv)
    while True:
        try:
            rows = run_once(dry=args.dry)
            closers = sum(r["closer"] for r in rows)
            print(f"{time.strftime('%H:%M:%S')} matchmaker: {len(rows)} match(es), {closers} page-closer(s)"
                  + "".join(f" · {r['card']} {r['seller']}→{r['buyer']} ~{r['price']} ({r['vc']:+g})" for r in rows[:3]),
                  flush=True)
        except Exception as e:  # noqa: BLE001  a watcher keeps watching
            print(time.strftime("%H:%M:%S"), "matchmaker error:", repr(e)[:200], flush=True)
        if args.once or args.dry:
            return
        time.sleep(args.every)


if __name__ == "__main__":
    main()
