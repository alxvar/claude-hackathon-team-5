"""Egg-trigger catalog (Chief, Sat 22:30): which words make which dealer give what. Read-only; tools/hints.py runs it
every EGGS_EVERY_S and writes intel/eggs.md.

Team messages to dealers are private in the feed (text null), but a dealer's reply echoes the trigger (Chato 1363:
"Plaza Mayor, con caña — you know Madrid. Here, for your trouble" → a sobre_barrio pack to t10; Abuela 1364:
"cocido con sus tres vuelcos" → MAL-06 to t10). So, from data/feed.jsonl:
1. every reward event (egg.found, egg.given, badge.awarded; Abuela's routine gift.given apart) with the dealer replies
   to that team over the preceding ECHO_TICKS ticks, and the Madrid references in them: the trigger;
2. every dealer reply that names a Madrid reference (MADRID), with the team and what followed within FOLLOW_TICKS
   (a gift, an egg, a badge, or the dealer's price against its previous one in the thread);
3. a castizo script per dealer for the Operator (SCRIPTS: one trigger per message), marked with what the feed has
   confirmed and whether we already have it.

    python3 tools/eggs.py            # write intel/eggs.md once (tools/daemons.sh hints runs it every 10 min)
"""
from __future__ import annotations

import json
import re
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEED, OUT = ROOT / "data" / "feed.jsonl", ROOT / "intel" / "eggs.md"
ME = "t05"
DEALERS = ("abuela", "chato", "pilar", "picaros", "banco")
NAMES = {"abuela": "Abuela Carmen", "chato": "El Chato", "pilar": "Doña Pilar", "picaros": "Los Pícaros",
         "banco": "Don Ernesto"}
REWARDS = ("egg.found", "egg.given", "badge.awarded")
ECHO_TICKS, FOLLOW_TICKS = 5, 3
EGGS_EVERY_S = 600
# Madrid references a dealer may echo (accents stripped, lower case). "caña" only with Plaza Mayor or "con/una".
MADRID = re.compile(r"\b(chotis|baldosa|cocido|tres vuelcos|plaza mayor|con cana|una cana|calamares|bocata|vermut|"
                    r"rosquillas|tontas y listas|chulap[ao]\w*|verbena|san isidro|la paloma|organill\w*|barquill\w*|"
                    r"cascorro|quevedo|monipodio|lazarillo|rinconete|cortadillo|estampita|corte de los milagros|"
                    r"perra gorda|sile,? nole|me falta|mi santo|zarzuela|manton|moscu|moscow|oro de|dama de serrano|"
                    r"doce de octubre|12 de octubre|cibeles|puerta del sol|kilometro cero|churros|gallinejas|"
                    r"entresijos|gatos?\b|madrilen\w*|castiz\w*|you know madrid)")
# One trigger per message, in a thread we'd open anyway (Operator). Evidence fills in from the feed.
SCRIPTS = {   # dealer → [(the reward kind it confirms, what, the line)]
    "abuela": [("badge Castizo", "the Castizo badge", "¡Carmen! El chotis se baila en una sola baldosa, como Dios manda."),
               ("card", "a card (egg.given)", "Y el domingo, un cocido madrileño con sus tres vuelcos, ¿eh? Como el de "
                                               "su madre."),
               ("badge Sharp ear", "Sharp ear (→ Ernesto)", "Carmen, ¿y la chulapa dorada? Cuénteme la historia.")],
    "chato": [("pack", "a pack (egg.given sobre_barrio)", "Un bocata de calamares en la Plaza Mayor, con una caña: eso "
                                                          "es Madrid.")],
    "picaros": [("badge Trickster tricked", "Trickster tricked", "A mí no, que me sé el timo de la estampita: Lazarillo, "
                                                                 "Rinconete y Monipodio.")],
    "banco": [("card", "LAT-13 legendary (minted out since 1021)", "Don Ernesto, el oro de Moscú.")],
    "pilar": [("", "none seen yet", "Doña Pilar, felicidades por el Pilar, el doce de octubre.")],
}


def norm(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text or "") if unicodedata.category(c) != "Mn").lower()


def refs(text: str) -> list[str]:
    return sorted({m.group(1) for m in MADRID.finditer(norm(text))})


def load(path: Path = FEED) -> list[dict]:
    out = []
    try:
        with Path(path).open() as f:
            for raw in f:
                try:
                    out.append(json.loads(raw))
                except ValueError:
                    continue
    except OSError:
        pass
    return sorted((e for e in out if isinstance(e.get("tick"), int)), key=lambda e: (e["tick"], e.get("id") or 0))


def _price(p: dict) -> float | None:
    o = p.get("offer") or {}
    want, give = o.get("want") or {}, o.get("give") or {}
    return want.get("cash") or give.get("cash") or None


def _item(e: dict) -> str | None:
    """What a reward event gave: "badge X", "card X", "pack X", or None for a bare egg.found."""
    p = e["payload"]
    if e["type"] == "badge.awarded":
        return f"badge {p.get('badge')}"
    if e["type"] in ("egg.given", "gift.given"):
        got = [f"card {c}" for c in p.get("cards") or []] + [f"pack {k}" for k in p.get("packs") or []]
        return ", ".join(got + ([f"{p['cash']} P"] if p.get("cash") else [])) or None
    return None


def kind_of(item: str | None) -> str:
    """The table's reward class: the badge's name, "card", "pack", or "egg found" alone."""
    if not item:
        return "egg found"
    return item if item.startswith("badge") else item.split()[0]


def build(events: list[dict]) -> dict:
    """{"rewards": [...], "refs": [...], "gifts": {team: n}}. A reward is one (team, tick, dealer): the egg.found
    names the dealer, and the egg.given or badge of the same team and tick is what it gave (the feed lists them
    together: Abuela 1368, egg.found + egg.given MAL-06 for "cocido con sus tres vuelcos")."""
    replies: dict = defaultdict(list)                  # team → dealer replies, in order
    for e in events:
        p = e.get("payload") or {}
        if e.get("type") == "thread.message" and p.get("sender") in DEALERS and p.get("team"):
            replies[p["team"]].append(e)
    found_at: dict = defaultdict(list)                 # (team, tick) → dealers whose egg was found
    for e in events:
        p = e.get("payload") or {}
        if e.get("type") == "egg.found" and p.get("team"):
            found_at[(p["team"], e["tick"])].append(p.get("persona"))
    groups: dict = {}
    gifts, by_team = defaultdict(int), defaultdict(list)
    for e in events:
        p = e.get("payload") or {}
        if e.get("type") == "gift.given":
            gifts[p.get("team")] += 1
            by_team[p.get("team")].append(e)
            continue
        if e.get("type") not in REWARDS or not p.get("team"):
            continue
        by_team[p["team"]].append(e)
        dealer = p.get("persona") if e["type"] == "egg.found" else next(iter(found_at.get((p["team"], e["tick"])) or []), None)
        g = groups.setdefault((p["team"], e["tick"], dealer), {"tick": e["tick"], "team": p["team"], "dealer": dealer,
                                                               "items": []})
        if (item := _item(e)) and item not in g["items"]:
            g["items"].append(item)
    rewards = []
    for g in groups.values():
        cands = [m for m in replies[g["team"]] if g["tick"] - ECHO_TICKS <= m["tick"] <= g["tick"]
                 and (g["dealer"] is None or m["payload"]["sender"] == g["dealer"])]
        keyed = [m for m in cands if refs(m["payload"].get("text") or "")]
        hit = [m for m in keyed if m["tick"] == keyed[-1]["tick"]] if keyed else cands[-1:]
        dealer = g["dealer"] or (hit[-1]["payload"]["sender"] if hit else None)
        words = sorted({w for m in hit for w in refs(m["payload"].get("text") or "")})
        rewards.append({**g, "dealer": dealer, "kinds": [kind_of(i) for i in g["items"]] or ["egg found"],
                        "reward": "; ".join(g["items"]) or "egg found", "words": words,
                        "echo": [(m["tick"], m["payload"]["sender"], (m["payload"].get("text") or "")[:300])
                                 for m in hit[-2:]]})
    rewards.sort(key=lambda r: (r["tick"], r["team"]))
    found = []
    for team, ms in replies.items():
        last_price: dict = {}
        for m in ms:
            p = m["payload"]
            price, prev = _price(p), last_price.get(p.get("thread"))
            if price is not None:
                last_price[p.get("thread")] = price
            words = refs(p.get("text") or "")
            if not words:
                continue
            after = [r["reward"] for r in rewards if r["team"] == team and r["dealer"] == p["sender"]
                     and m["tick"] <= r["tick"] <= m["tick"] + FOLLOW_TICKS]
            after += [_item(r) or "gift" for r in by_team[team] if r["type"] == "gift.given"
                      and m["tick"] <= r["tick"] <= m["tick"] + FOLLOW_TICKS and p["sender"] == "abuela"]
            if price is not None and prev is not None and price != prev:
                after.append(f"price {prev:g} → {price:g}")
            found.append({"tick": m["tick"], "team": team, "dealer": p["sender"], "words": words,
                          "text": (p.get("text") or "")[:260], "after": after})
    found.sort(key=lambda x: (x["tick"], x["team"]))
    return {"rewards": rewards, "refs": found, "gifts": dict(gifts)}


def table(rewards: list[dict]) -> list[dict]:
    """The trigger → reward → dealer rows: one per (dealer, reward kind), with the teams, the words and an echo."""
    rows: dict = {}
    for r in rewards:
        for kind in r["kinds"]:
            row = rows.setdefault((r["dealer"], kind), {"dealer": r["dealer"], "kind": kind, "teams": [],
                                                        "words": defaultdict(int), "first": r["tick"], "echo": None,
                                                        "rewards": set()})
            if r["team"] not in row["teams"]:
                row["teams"].append(r["team"])
            for w in r["words"]:
                row["words"][w] += 1
            row["rewards"].add(r["reward"])
            if r["echo"]:
                row["echo"] = r["echo"][-1]            # the latest echo: the freshest wording
    return sorted(rows.values(), key=lambda x: (DEALERS.index(x["dealer"]) if x["dealer"] in DEALERS else 9,
                                                x["first"]))


def render(cat: dict, *, me: str = ME, now=None) -> str:
    rows = table(cat["rewards"])
    L = ["# Easter eggs: trigger → reward → dealer (castizo catalog)\n",
         f"_Written by `tools/eggs.py` at {time.strftime('%H:%M', time.localtime(now or time.time()))} (every 10 min, "
         "from data/feed.jsonl). Teams' words to dealers are private; the dealer's reply in the "
         f"{ECHO_TICKS} ticks before a reward echoes the trigger. **We** = Team 5. Abuela's routine gifts (kindness, "
         "meeting in the middle) are counted apart._\n",
         "## Trigger → reward → dealer\n", "| dealer | reward | trigger words (echoed) | teams | we | first tick | the echo |",
         "|---|---|---|---|---|---|---|"]
    for r in rows:
        words = ", ".join(w for w, _ in sorted(r["words"].items(), key=lambda x: -x[1])[:6]) or "(none echoed)"
        echo = r["echo"][2].replace("\n", " ").replace("|", "/")[:170] if r["echo"] else ""
        got = r["kind"] if r["kind"].startswith(("badge", "egg")) else "; ".join(sorted(r["rewards"]))[:60]
        L.append(f"| {NAMES.get(r['dealer'], r['dealer'])} | {got} | {words} | {', '.join(r['teams'])} | "
                 f"{'yes' if me in r['teams'] else '**no**'} | {r['first']} | {echo} |")
    L += ["", f"Abuela's routine gifts (gift.given): {sum(cat['gifts'].values())} to "
              f"{len(cat['gifts'])} teams" + (f", {cat['gifts'].get(me, 0)} to us" if cat["gifts"] else "") + ".", ""]
    L += ["## Castizo script per dealer (Sunday 09:00; one trigger per message, in a thread we open anyway)\n"]
    ours = {r["kind"] for r in rows if me in r["teams"] and r["kind"].startswith("badge")}   # a badge is the team's
    for d, lines in SCRIPTS.items():
        L.append(f"**{NAMES[d]}**")
        for kind, what, text in lines:
            got = next((r for r in rows if r["dealer"] == d and r["kind"] == kind), None)
            have = got is not None and (me in got["teams"] or kind in ours)
            status = (f"confirmed for {', '.join(got['teams'])}; " + ("we have it" if have else "**we don't**")
                      if got else "not confirmed in the feed")
            L.append(f"- {what}: \"{text}\" · {status}")
        L.append("")
    L += ["## Every dealer reply naming Madrid (newest first)\n", "| tick | team | dealer | words | what followed | reply |",
          "|---|---|---|---|---|---|"]
    for x in reversed(cat["refs"][-80:]):
        L.append(f"| {x['tick']} | {x['team']} | {x['dealer']} | {', '.join(x['words'])} | "
                 f"{'; '.join(x['after']) or '-'} | {x['text'].replace(chr(10), ' ').replace('|', '/')[:160]} |")
    return "\n".join(L) + "\n"


def write(feed: Path = FEED, out: Path = OUT) -> dict:
    cat = build(load(feed))
    tmp = Path(out).with_suffix(".tmp")
    tmp.write_text(render(cat))
    tmp.replace(out)
    return cat


if __name__ == "__main__":
    c = write()
    print(f"eggs: {len(c['rewards'])} rewards, {len(c['refs'])} Madrid replies → {OUT}")
