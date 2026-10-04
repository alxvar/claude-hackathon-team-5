"""Secrets desk: the Bazaar's easter eggs, Radio Rastro's truth record and The Workshop, from public data only.

    python dashboard/secrets.py              # one pass: writes judges/secrets.md and prints a summary
    python dashboard/secrets.py --watch      # then keeps polling (every tick) and prints each new egg, badge,
                                             # news item and Workshop craft as it happens

Read-only and keyless: GET /api/feed, /api/news, /api/catalog, /api/levels (public reads, 60/s per address), plus the
dashboard's own feed cache (logs/dashboard/feed.jsonl) for history. It never writes to the game, never needs the team
key, and only Lucas's Operator ever talks to a dealer.

How it reads the eggs: a team's own words to a dealer are not in the public feed, but the dealer's answer is, and it
echoes the phrase that opened the egg ("¡Ay, cocido con sus tres vuelcos!", "Plaza Mayor, con caña. You know Madrid").
So each `egg.found` is matched with the dealer's reply to that team at that tick, and the reply is scanned for the
known trigger themes below. A reply that matches none is printed as is: that is a new egg to study.

Radio Rastro: each news item is checked against what the market then did (the dealer's buy prices for the rarity
before and after, a cash grant to us, the catalog's book prices and print runs, the egg log). The tally per source says
which one to trust. Eggs, badges, gifts and Workshop pulls never score (RULES.md "What never counts"); the cards and
packs they bring can be traded, and the story is the judges' to hear.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import statistics
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = "https://bazaar.causaprima.ai"
CACHE = ROOT / "logs" / "dashboard" / "feed.jsonl"
ME_CACHE = ROOT / "logs" / "dashboard" / "me.jsonl"
OUT = ROOT / "judges" / "secrets.md"
US = "t05"

# Trigger themes, read from the dealers' answers (Sat-Sun): theme, words to look for in the reply, what to say.
TRIGGERS = [
    ("oro de Moscú", ["oro de moscú", "moscow gold", "oro de moscu"], "ask Don Ernesto about 'el oro de Moscú'", "banco"),
    ("chulapa dorada", ["chulapa dorada", "golden chulapa"], "ask Abuela about 'la chulapa dorada'", "abuela"),
    ("estampita", ["lazarillo", "rinconete", "estampita", "old trick"], "tell Los Pícaros you know the 'timo de la estampita' (Lazarillo, Rinconete)", "picaros"),
    ("chotis", ["chotis", "baldosa", "one tile"], "tell Abuela the chotis is danced on one baldosa (verbena de la Paloma)", "abuela"),
    ("sile nole", ["sile", "nole", "me falta"], "'sile, nole, repe, me falta' (the old card-swapping chant)", "abuela"),
    ("cocido", ["cocido", "tres vuelcos", "rosquillas"], "tell Abuela about 'cocido madrileño con sus tres vuelcos' (rosquillas)", "abuela"),
    ("Plaza Mayor", ["plaza mayor", "calamares", "caña bien tirada", "con caña"], "tell El Chato 'Plaza Mayor, bocadillo de calamares, caña bien tirada'", "chato"),
    ("Carmen sends you", ["carmen sends", "abuela sent you", "me manda carmen"], "tell El Chato that Carmen (Abuela) sends you", "chato"),
]


def get(path, timeout=20):
    with urllib.request.urlopen(URL + path, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def load_events():
    """The dashboard's cache (full history) merged with the live feed's last 500 events, by id."""
    ev = {}
    if CACHE.exists():
        for line in CACHE.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
                ev[e["id"]] = e
            except (ValueError, KeyError):
                pass
    try:
        for e in get("/api/feed?limit=500").get("events", []):
            ev[e["id"]] = e
    except OSError as x:
        print(f"feed: {x}", file=sys.stderr)
    return sorted(ev.values(), key=lambda e: (e.get("tick") or 0, e["id"]))


def theme_of(text):
    low = (text or "").lower()
    return [name for name, words, _, _ in TRIGGERS if any(w in low for w in words)]


def hint_for(persona, themes):
    """The trigger to say to this dealer: the first theme of its own in the reply (Abuela's 'Sharp ear' reply also names
    Don Ernesto's 'oro de Moscú', but what opened it was 'la chulapa dorada')."""
    for name, _, say, who in TRIGGERS:
        if name in themes and who == persona:
            return say
    return next((say for name, _, say, _ in TRIGGERS if name in themes), "read the replies below")


# ------------------------------------------------------------------------------------------------ eggs
def eggs(events):
    msgs = collections.defaultdict(list)   # (team, persona) -> dealer replies
    for e in events:
        p = e.get("payload") or {}
        if e.get("type") == "thread.message" and p.get("kind") == "persona" and p.get("sender") == p.get("with"):
            msgs[(p.get("team"), p.get("with"))].append((e.get("tick") or 0, str(p.get("text") or "")))
    awards = collections.defaultdict(list)   # (tick, team) -> prizes in feed order
    for e in events:
        p = e.get("payload") or {}
        if e.get("type") == "badge.awarded":
            awards[(e.get("tick"), p.get("team"))].append(("badge", p.get("badge"), None))
        elif e.get("type") == "egg.given":
            got = (p.get("cards") or []) + (p.get("packs") or []) + ([f"{p['cash']} P"] if p.get("cash") else [])
            awards[(e.get("tick"), p.get("team"))].append(("gift", ", ".join(got), e.get("actor")))
    rows = []
    for e in events:
        if e.get("type") != "egg.found":
            continue
        p = e.get("payload") or {}
        t, per, k = p.get("team"), p.get("persona"), e.get("tick")
        pool = awards.get((k, t), [])
        hit = next((a for a in pool if a[0] == "gift" and a[2] == per), None) or next((a for a in pool if a[0] == "badge"), None)
        if hit:
            pool.remove(hit)
        what = (hit[0], hit[1]) if hit else ("?", "")
        reply = next((txt for tk, txt in reversed(msgs.get((t, per), [])) if tk <= k), "")
        rows.append({"tick": k, "team": t, "name": p.get("name"), "persona": per, "persona_name": p.get("persona_name"),
                     "kind": what[0], "prize": what[1], "themes": theme_of(reply), "reply": reply[:300]})
    return rows


# ------------------------------------------------------------------------------------------------ Radio Rastro
def dealer_buy_prices(events, persona, rarity, t0, t1, sets=None):
    out = []
    for e in events:
        if e.get("type") != "settlement" or not (t0 <= (e.get("tick") or 0) < t1):
            continue
        p = e.get("payload") or {}
        it = (p.get("items") or [{}])[0]
        if p.get("persona") == persona and it.get("to") == persona and it.get("rarity") == rarity \
                and (sets is None or it.get("set") in sets):
            out.append(p.get("price") or 0)
    return out


def verify(item, events, catalog, egg_rows, me_rows):
    """(verdict, evidence) for one news item: TRUE / FALSE / FLAVOUR / OPEN."""
    h = f"{item.get('headline', '')} {item.get('body', '')}".lower()
    k = item.get("tick") or 0
    hour = 240 if k >= 1445 else 120          # one game hour in ticks: 30 s on Saturday, 15 s on Sunday
    personas = {"abuela": "abuela", "chato": "chato", "pilar": "pilar", "pícaros": "picaros", "ernesto": "banco"}
    who = next((v for w, v in personas.items() if w in h), None)
    rar = next((r for r in ("uncommon", "common", "rare", "epic", "legendary") if r in h), None)
    sets = {"malasaña": "MAL", "lavapiés": "LAV", "latina": "LAT", "salamanca": "SAL", "retiro": "RET", "chamberí": "CHA"}
    st = {v for w, v in sets.items() if w in h} or None
    if "reprint" in h:
        return "FALSE", "print runs are fixed (RULES.md: commons 300 … legendaries 3)"
    if "double" in h or "worth" in h and "book" not in h and rar:
        book = (catalog.get("rarities") or {}).get(rar or "common", {}).get("book")
        return ("FALSE" if book in (10, 25, 70, 180, 450) else "OPEN"), f"catalog book for {rar or 'common'} still {book}"
    if "gives" in h and "legendary" in h:
        given = [r for r in egg_rows if r["persona"] == who and "legendary" in r["prize"]]
        return ("FALSE" if not given else "TRUE"), f"{len(given)} legendary handed out by {who} in the egg log"
    m = re.search(r"(\d+)\s*primas", h)
    if m and ("gives" in h or "bonus" in h or "pay" in h):
        n = int(m.group(1))
        jumps = [(a["tick"], b["tick"]) for a, b in zip(me_rows, me_rows[1:])
                 if a.get("cash") is not None and b.get("cash") is not None and b["tick"] > k and b["cash"] - a["cash"] == n]
        return ("TRUE" if jumps else "OPEN"), (f"our cash +{n} at tick {jumps[0][1]}" if jumps else f"no +{n} cash jump of ours yet")
    if who and rar and ("pays more" in h or "pays above" in h or "looking for" in h):
        before = dealer_buy_prices(events, who, rar, max(0, k - 6 * hour), k, st)
        during = dealer_buy_prices(events, who, rar, k, k + 2 * hour, st)
        if before and during:
            b, d = statistics.median(before), statistics.median(during)
            return ("TRUE" if d > b else "FALSE"), f"{who} paid median {b} before (n={len(before)}) vs {d} after (n={len(during)})"
        return "OPEN", f"too few {who} {rar} buys to tell (before {len(before)}, after {len(during)})"
    if who and rar and "stops buying" in h:
        after = dealer_buy_prices(events, who, rar, k, 10 ** 9)
        return ("FALSE" if after else "TRUE"), f"{who} bought {len(after)} {rar} card(s) afterwards"
    if who and ("gives" in h or "packs" in h):
        gifts = [e for e in events if e.get("type") in ("gift.given", "egg.given") and k <= (e.get("tick") or 0) < k + 2 * hour
                 and (who in str((e.get("payload") or {}).get("reason", "")).lower() or e.get("actor") == who)]
        return ("TRUE" if gifts else "OPEN"), f"{len(gifts)} gift(s) from {who} within two hours"
    if any(w in h for w in ("dealer", "pays", "buy", "sell", "cards", "pack", "primas", "price", "rastro closes")):
        return "OPEN", "a market claim this desk can't test yet"
    return "FLAVOUR", "Madrid colour (weather, football, metro, churros)"


def radio(events, catalog, egg_rows):
    news = get("/api/news").get("news", [])
    me_rows = []
    if ME_CACHE.exists():
        rows = {}
        for line in ME_CACHE.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
                if r.get("tick") is not None:
                    rows[r["tick"]] = r
            except ValueError:
                pass
        me_rows = [rows[t] for t in sorted(rows)]
    out = []
    for it in sorted(news, key=lambda x: x.get("tick") or 0):
        verdict, why = verify(it, events, catalog, egg_rows, me_rows)
        out.append({**it, "verdict": verdict, "why": why})
    tally = collections.defaultdict(collections.Counter)
    for it in out:
        tally[it.get("source_name") or it.get("source")][it["verdict"]] += 1
    return out, tally


# ------------------------------------------------------------------------------------------------ Workshop
def workshop(events, catalog):
    byname = {}
    for s in catalog.get("sets", []):
        for cd in s.get("cards", []):
            byname.setdefault((cd.get("name"), cd.get("rarity")), cd.get("id"))
    crafts = []
    for e in events:
        if e.get("type") == "taller.crafted":
            p = e.get("payload") or {}
            ref = byname.get((p.get("card"), p.get("to"))) or "?"
            crafts.append({"tick": e.get("tick"), "team": p.get("team"), "name": p.get("name"), "from": p.get("from"),
                           "to": p.get("to"), "ref": ref, "card": p.get("card")})
    return crafts


# ------------------------------------------------------------------------------------------------ report
def report(events):
    catalog = get("/api/catalog")
    levels = get("/api/levels").get("levels", [])
    hidden = [(s.get("id"), cd) for s in catalog.get("sets", []) for cd in s.get("cards", []) if cd.get("hidden")]
    egg_rows = eggs(events)
    news, tally = radio(events, catalog, egg_rows)
    crafts = workshop(events, catalog)
    now = max((e.get("tick") or 0) for e in events) if events else None
    L = [f"# Secrets desk (auto, {time.strftime('%a %H:%M')}, tick {now})", "",
         "_Public data only (feed, news, catalog, levels); `dashboard/secrets.py`. Eggs, badges, gifts and Workshop pulls "
         "never score (RULES.md); the cards and packs they bring can be traded. Only Lucas's Operator talks to dealers._", ""]

    L += ["## Hidden cards (catalog `hidden: true`)", ""]
    for sid, cd in hidden:
        owner = [r for r in egg_rows if cd.get("id") in r["prize"]]
        L.append(f"- **{cd.get('id')} {cd.get('name')}** ({cd.get('rarity')}, print run {cd.get('print_run')}, minted "
                 f"{cd.get('minted')}): \"{cd.get('flavour')}\"" + (f" → given to **{owner[0]['name']}** by "
                 f"{owner[0]['persona_name']} at tick {owner[0]['tick']}" if owner else ""))
    L.append("")

    L += ["## Easter eggs: the trigger behind each", "", "| Egg | Dealer | Trigger (from the dealer's reply) | Prize | Teams | Us |",
          "|---|---|---|---|---|---|"]
    groups = collections.OrderedDict()
    for r in egg_rows:
        groups.setdefault((r["persona"], r["persona_name"], r["prize"] if r["kind"] == "badge" else "gift"), []).append(r)
    for (per, pname, prize), rs in groups.items():
        prizes = sorted({r["prize"] for r in rs})
        teams = sorted({r["name"] for r in rs})
        us = any(r["team"] == US for r in rs)
        themes = collections.Counter(t for r in rs for t in r["themes"])
        hint = hint_for(per, [t for t, _ in themes.most_common()])
        L.append(f"| {prize} | {pname} | {hint} | {', '.join(prizes)} | {len(teams)}: {', '.join(teams)} | "
                 f"{'yes' if us else '**no**'} |")
    L.append("")
    unknown = [r for r in egg_rows if not r["themes"]]
    if unknown:
        L += ["Eggs whose reply matched no known trigger (study these):", ""]
        L += [f"- tick {r['tick']} {r['name']} → {r['persona_name']} ({r['prize']}): \"{r['reply'][:200]}\"" for r in unknown]
        L.append("")
    ours = {(r["persona_name"], r["prize"] if r["kind"] == "badge" else "gift") for r in egg_rows if r["team"] == US}
    missing = sorted({(r["persona_name"], r["prize"] if r["kind"] == "badge" else "gift") for r in egg_rows} - ours)
    L += ["**Ours:** " + (", ".join(f"{p} ({x})" for p, x in sorted(ours)) or "none"),
          "**Missing:** " + (", ".join(f"{p} ({x})" for p, x in missing) or "none"), ""]

    L += ["## Radio Rastro: which source tells the truth", "", "| Source | TRUE | FALSE | OPEN | FLAVOUR |", "|---|---|---|---|---|"]
    for src, c in tally.items():
        L.append(f"| {src} | {c['TRUE']} | {c['FALSE']} | {c['OPEN']} | {c['FLAVOUR']} |")
    L += ["", "| Tick | Source | Headline | Verdict | Evidence |", "|---|---|---|---|---|"]
    for it in news:
        L.append(f"| {it.get('tick')} | {it.get('source_name')} | {it.get('headline')} | **{it['verdict']}** | {it['why']} |")
    L.append("")

    by_set = collections.Counter(c["ref"][:3] for c in crafts)
    L += ["## The Workshop: three spares → one surprise", "",
          f"{len(crafts)} crafts so far; output by set: " + ", ".join(f"{s} {n}" for s, n in by_set.most_common())
          + ". The output is a random card of the next rarity from any released set (inputs from one set come out in "
            "another), so a craft is a lottery ticket for the set we build.", ""]
    L += [f"- tick {c['tick']} {c['name']}: {c['from']} → **{c['ref']}** {c['card']}" for c in crafts[-12:]]
    L.append("")
    lv = {l.get("id"): l for l in levels}
    for key in ("taller", "radio"):
        if key in lv:
            L.append(f"- **{lv[key].get('name')}**: «{lv[key].get('teaser')}» {lv[key].get('how')}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    return egg_rows, news, tally, crafts, missing


def watch(seen):
    """Print each new egg, badge, news item and craft as it lands (one poll per 15 s tick)."""
    print("watching (Ctrl+C to stop)…", flush=True)
    news_seen = {n.get("id") for n in get("/api/news").get("news", [])}
    while True:
        time.sleep(15)
        try:
            for e in get("/api/feed?limit=200").get("events", []):
                if e["id"] in seen:
                    continue
                seen.add(e["id"])
                p = e.get("payload") or {}
                if e.get("type") in ("egg.found", "egg.given", "badge.awarded", "taller.crafted"):
                    print(f"{time.strftime('%H:%M:%S')} tick {e.get('tick')} {e['type']}: "
                          f"{json.dumps(p, ensure_ascii=False)[:220]}", flush=True)
            for n in get("/api/news").get("news", []):
                if n.get("id") not in news_seen:
                    news_seen.add(n.get("id"))
                    print(f"{time.strftime('%H:%M:%S')} NEWS [{n.get('source_name')}] {n.get('headline')} — {n.get('body')}", flush=True)
        except OSError as x:
            print(f"{time.strftime('%H:%M:%S')} poll failed: {x}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", action="store_true", help="keep polling and print new eggs, badges, news and crafts")
    args = ap.parse_args()
    events = load_events()
    egg_rows, news, tally, crafts, missing = report(events)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(egg_rows)} eggs, {len(news)} news items, {len(crafts)} crafts")
    for src, c in tally.items():
        print(f"  {src}: TRUE {c['TRUE']} · FALSE {c['FALSE']} · OPEN {c['OPEN']} · FLAVOUR {c['FLAVOUR']}")
    print("  missing eggs for us:", ", ".join(f"{p} ({x})" for p, x in missing) or "none")
    if args.watch:
        watch({e["id"] for e in events})


if __name__ == "__main__":
    main()
