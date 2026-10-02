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

    # every settlement: who traded what
    sets = [e for e in feed if e["type"] == "settlement"]
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
    ours = [o for o in board["offers"] if o["team"] == me_id]
    L += [f"Our open offers: {len(ours)}: " + "; ".join(
        (f"sell {o['give']['assets'][0]['ref']} {o['want']['cash']}" if o["give"].get("assets") else f"bid {card(o)} {o['give']['cash']}")
        for o in ours), ""]

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
