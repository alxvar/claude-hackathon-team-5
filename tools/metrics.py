"""Metrics: turns data/ into intel/metrics.md, a short factual brief every agent reads. Deterministic, no LLM.

    source .env && python3 tools/metrics.py      # rebuild once (the collector does it every 2 minutes)
"""
import collections
import json
import os
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data", ROOT / "intel" / "metrics.md"


def lines(path):
    if not path.exists():
        return []
    with path.open() as f:
        return [json.loads(x) for x in f if x.strip()]


def our_book(b, me_id, rar, mes, sets):
    """What the analysts can't see on the board: our copies and their values, our open offers (with `to`), what each of
    our deals did to neg_points, and how our dealer conversations went."""
    L = []
    try:
        held = collections.defaultdict(list)
        for a in b.me()["assets"]:
            held[a["ref"]].append(a.get("your_value") or 0)
        L += ["## Our holdings (card (rarity): value of each copy; a sale gives up the cheapest copy)", "",
              "; ".join(f"{r} ({rar.get(r, 'pack')}): {' / '.join(f'{v:g}' for v in sorted(vs))}" for r, vs in sorted(held.items())), ""]
        ours = [o for o in b.my_offers()["offers"] if o["maker"] == me_id and o["status"] == "open"]
        L += [f"## Our open offers ({len(ours)})", ""]
        for o in ours:
            g, w = o["give"], o["want"]
            what = (f"sell {', '.join(a['ref'] for a in g['assets'])} for {w.get('cash')}" if g.get("assets") else
                    f"bid {g.get('cash')} for {', '.join(w.get('cards') or [t.split(':', 1)[-1] for t in w.get('types', [])])}")
            L.append(f"- {o['id']}: {what} · to {o.get('to') or 'anyone'} · expires tick {o.get('expires_tick')}")
        L.append("")
    except Exception as e:
        L += [f"## Our holdings and offers: unavailable ({e!r})", ""]

    # each change of neg_points, next to our settlements since the previous change
    ourset = [e for e in sets if me_id in e["payload"].get("parties", [])]
    rows, prev, since = [], None, (mes[0].get("tick") if mes else 0)
    for m in mes:
        if prev is not None and m.get("neg_points") != prev.get("neg_points"):
            deals = [e["payload"] for e in ourset if (since or 0) < e["tick"] <= (m.get("tick") or 0)]
            what = "; ".join(
                f"{p.get('persona') or 'team'} {'buy' if p['items'][0]['to'] == me_id else 'sell'} "
                f"{', '.join(i['ref'] for i in p['items'])} at {p['price']} with {next(x for x in p['parties'] if x != me_id)}"
                for p in deals) or "no deal of ours in between"
            rows.append(f"- tick {m.get('tick')}: {m['neg_points'] - prev['neg_points']:+.1f} → {m['neg_points']} · {what}")
            since = m.get("tick")
        prev = m
    L += ["## What each of our deals did to neg_points (measured, last 12)", ""] + rows[-12:] + [""]

    try:
        th = [t for t in b.my_threads()["threads"] if t.get("kind") == "persona"][-8:]
        px = lambda o: max(o["give"].get("cash", 0), o["want"].get("cash", 0))
        L += ["## Our dealer conversations (last 8: dealer's first → last price, our last, outcome)", ""]
        for t in th:
            theirs = [m["offer"] for m in t["messages"] if m.get("offer") and m["sender"] == t["with"]]
            mine = [m["offer"] for m in t["messages"] if m.get("offer") and m["sender"] != t["with"]]
            side = "buy" if "buy" in (t.get("topic") or {}) else "sell"
            what = ((t.get("topic") or {}).get("buy") or {}).get("card") or ((t.get("topic") or {}).get("buy") or {}).get("pack") or t.get("item")
            L.append(f"- tick {t['created_tick']} {t['with']} {side} {what}: "
                     f"{px(theirs[0]) if theirs else '?'} → {px(theirs[-1]) if theirs else '?'}, ours {px(mine[-1]) if mine else '-'}"
                     f" · {t['status']}{' (' + t['closed_reason'] + ')' if t.get('closed_reason') else ''}")
        L.append("")
    except Exception as e:
        L += [f"## Our dealer conversations: unavailable ({e!r})", ""]
    return L


def write(b):
    OUT.parent.mkdir(exist_ok=True)
    feed, mes, lbs = lines(DATA / "feed.jsonl"), lines(DATA / "me.jsonl"), lines(DATA / "leaderboard.jsonl")
    board = json.loads((DATA / "board.json").read_text()) if (DATA / "board.json").exists() else {"offers": []}
    cat = b.catalog()
    rar = {c["id"]: c["rarity"] for s in cat["sets"] for c in s["cards"]}
    me_id = board.get("me", "t05")
    now_tick = feed[-1]["tick"] if feed else 0
    L = [f"# Metrics (auto, {time.strftime('%H:%M')}, game tick {now_tick})", ""]

    # leaderboard and how fast each team is moving
    if lbs:
        cur = lbs[-1]
        def at(minutes):
            old = [x for x in lbs if x["t"] <= cur["t"] - 60 * minutes]
            return {t["team"]: t["score"] for t in (old[-1] if old else lbs[0])["teams"]}
        d15, d60 = at(15), at(60)
        L += ["## Leaderboard (score, change over 15 min / 60 min)", ""]
        for i, t in enumerate(sorted(cur["teams"], key=lambda t: -(t["score"] or 0))[:10]):
            mark = " ← US" if t["team"] == me_id else ""
            L.append(f"{i + 1}. {t['name']} {t['score']:.1f} ({(t['score'] or 0) - d15.get(t['team'], 0):+.1f} / "
                     f"{(t['score'] or 0) - d60.get(t['team'], 0):+.1f}) deals {t['deals']}{mark}")
        us = next((i + 1 for i, t in enumerate(sorted(cur["teams"], key=lambda t: -(t["score"] or 0))) if t["team"] == me_id), None)
        L.append(f"Us: #{us}")
        L.append("")

    # our components over time
    if mes:
        m = mes[-1]
        old = [x for x in mes if x["t"] <= m["t"] - 900]
        o = old[-1] if old else mes[0]
        L += ["## Us", "", f"score {m['score']} · neg_points {m['neg_points']} (15 min ago {o['neg_points']}) · ladder "
              f"{m['ladder_points']} · duel {m['duel_points']} · cash {m['cash']} · level {m['level']} · deals {m['deals']}", ""]

    # every settlement once (the feed can repeat one under two event ids)
    uniq = {}
    for e in feed:
        if e["type"] == "settlement":
            uniq.setdefault(e["payload"].get("settlement", e["id"]), e)
    sets = sorted(uniq.values(), key=lambda e: e["tick"])

    L += our_book(b, me_id, rar, mes, sets)
    team_trades = [e for e in sets if not e["payload"].get("persona")]
    L += [f"## Trades between teams ({len(team_trades)} so far; last 12)", ""]
    for e in team_trades[-12:]:
        p = e["payload"]
        items = ", ".join(f"{i['ref']} ({rar.get(i['ref'], '?')}) {i['frm']}→{i['to']}" for i in p["items"])
        L.append(f"- tick {e['tick']}: {items} for {p['price']} P")
    buys = collections.defaultdict(lambda: collections.Counter())
    for e in team_trades:
        for i in e["payload"]["items"]:
            buys[i["to"]][i["ref"][:3]] += 1
    L += ["", "Who buys which set (team trades): " + "; ".join(
        f"{t}: {', '.join(f'{s}×{n}' for s, n in c.most_common())}" for t, c in sorted(buys.items())), ""]

    # dealer prices in the last ~60 ticks
    recent = [e for e in sets if e["payload"].get("persona") and e["tick"] >= now_tick - 60]
    by = collections.defaultdict(list)
    for e in recent:
        p = e["payload"]
        for i in p["items"]:
            kind = i["ref"] if i["kind"] == "pack" else rar.get(i["ref"], "?")
            side = "team buys" if i["frm"] == p["persona"] else "team sells"
            by[(p["persona"], kind, side)].append(p["price"] / max(1, len(p["items"])))
    L += ["## Dealer prices, last 60 ticks (median per item)", ""]
    L += [f"- {d} {k} ({s}): median {statistics.median(v):.0f} over {len(v)}" for (d, k, s), v in sorted(by.items())]
    L.append("")

    # El Rastro right now: bids and asks with the team behind them
    bids = [o for o in board["offers"] if o["give"].get("cash") and (o["want"].get("cards") or o["want"].get("types"))]
    asks = [o for o in board["offers"] if o["give"].get("assets") and o["want"].get("cash")]
    def card(o):
        w = o["want"]
        return (w.get("cards") or [t.split(":", 1)[-1] for t in w.get("types", [])] or ["?"])[0]
    L += ["## El Rastro now: top bids by price (team, card, price)", ""]
    for o in sorted(bids, key=lambda o: -o["give"]["cash"])[:15]:
        L.append(f"- {o['team']}{' (US)' if o['team'] == me_id else ''}: {card(o)} ({rar.get(card(o), '?')}) {o['give']['cash']} P · offer {o['id']}")
    ask_sum = collections.Counter((o["give"]["assets"][0]["ref"], o["want"]["cash"]) for o in asks if o["team"] != me_id)
    L += ["", "Asks by others (card, price: count): " + "; ".join(f"{r} {p}: {n}" for (r, p), n in ask_sum.most_common(15)), ""]

    # our duels (the judge grades the duelist too)
    try:
        done = b.duels(done=True).get("duels", [])
        live = b.duels().get("duels", [])
        L += [f"## Our duels: {len(live)} live, {len(done)} finished (last 10)", ""]
        for d in done[-10:]:
            keep = {k: v for k, v in d.items() if k not in ("messages", "transcript", "history", "offers")}
            L.append("- " + json.dumps(keep)[:260])
        L.append("")
    except Exception as e:
        L += [f"## Our duels: unavailable ({e!r})", ""]

    # announcements and levels
    ann = [e for e in feed if e["type"] in ("announcement", "level.announced", "level.activated") or "level" in e["type"]][-5:]
    if ann:
        L += ["## Latest announcements", ""] + [f"- tick {e['tick']} {e['type']}: {json.dumps(e['payload'])[:160]}" for e in ann] + [""]
    OUT.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "bazaar-kit"))
    from bazaar_sdk import Bazaar
    write(Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"]))
    print(OUT.read_text()[:3000])
