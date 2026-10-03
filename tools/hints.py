"""Dealer-hint miner (Chief, Sat 18:30): easter eggs hide in what dealers say to EVERY team. Read-only.

Sat [V]: Pilar told many teams "ask Carmen at El Rastro about the golden chulapa"; Carmen, asked, fired egg.found and
said "ask him about the Moscow gold"; Don Ernesto (banco), told "El oro de Moscú", gave Team 2 LAT-13 (a hidden
legendary, print run 1) at tick 1021.

Every tick this reads new events in data/feed.jsonl (the collector's) and:
- every persona (non-team) thread.message whose text matches a hint pattern (EN/ES: story, legend, secret, hidden,
  only one, ask her/him about, knows, golden/dorad*, oro, treasure, vault, password, phrase, saint, a quoted phrase…)
  becomes a hit, de-duplicated per (dealer, text without numbers): first/last tick, count, teams;
- every egg.found / egg.given / taller.crafted / persona.updated / persona.open_to_all / set.released is a hit;
- every 10 min, /api/catalog: a new card with hidden=true, or a changed `minted` on an epic or legendary, is a hit;
- intel/news.md lines matching the patterns are hits.
Each new hit prints one `HINT …` line (the Builder relays it to the Chief) and is appended to intel/hints.md.

    python3 -u tools/hints.py                 # daemon (tools/daemons.sh start hints)
    python3 tools/hints.py --backfill --dry   # every hit in the whole feed, printed only
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
FEED, NEWS = ROOT / "data" / "feed.jsonl", ROOT / "intel" / "news.md"
OUT, STATE = ROOT / "intel" / "hints.md", ROOT / "run" / "hints_state.json"
URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
CATALOG_EVERY_S = 600
EVENT_TYPES = ("egg.found", "egg.given", "taller.crafted", "persona.updated", "persona.open_to_all", "set.released")

HINT = re.compile(   # strong patterns only: flavour words (grandchildren, saint, story, secret) alone are noise
    r"(only (ever )?one\b|there was only ever|solo se imprimi|sólo se imprimi|una sola (vez|copia|carta)|"
    r"\bask (her|him|them|me)? ?(about|for)\b|pregúnt\w*( a [\w ]{2,20})? (por|sobre)\b|preguntad\w* (por|sobre)\b|"
    r"knows? (the story|where|more)\b|conoce la historia|sabe (dónde|más)\b|él sabrá|ella sabrá|he will know|"
    r"he'll know|keeps something|guarda algo|\blegend\w*|leyenda\w*|\bhidden\b|escondid\w*|\bvault\b|bóveda|"
    r"password|contraseña|santo y seña|easter|golden \w*chulapa|chulapa dorada|dorad[ao]s? |oro de mosc\w*|"
    r"moscow gold|gold of mosc\w*|el oro\b|carmen (sends|speaks|talks)|sends you|me manda|te manda)", re.I)
KEEPER = "banco"   # Don Ernesto keeps the golden chulapa: every line of his to a team that found an egg is a hit
NOISE = re.compile(r"(not a legend|no secrets?|hardly a treasure|not a treasure|is a story|a story, not)", re.I)
QUOTED = re.compile(r"\b(say|tell (him|her|them)|dile|díle|diga|di|pronounce|whisper)\b[^.]{0,20}[\"“«]([^\"”»]{3,60})[\"”»]", re.I)
NUM = re.compile(r"\d+|\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
                 r"sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|"
                 r"diez|once|doce|trece|catorce|quince|dieciséis|diecisiete|dieciocho|diecinueve|veinte|treinta|"
                 r"cuarenta|cincuenta|sesenta|setenta|ochenta|noventa|cien\w*)\b", re.I)


def is_team(x) -> bool:
    return isinstance(x, str) and len(x) == 3 and x[0] == "t" and x[1:].isdigit()


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", NUM.sub("#", text or "").lower()).strip()[:200]


def scan_events(events, seen: dict | None = None) -> tuple[list[dict], dict]:
    """New hits from feed events. `seen`: {(dealer, norm text): hit} to de-duplicate across runs (it also keeps the
    teams that found an egg, under "eggs")."""
    seen = {} if seen is None else seen
    eggs = set(seen.get("eggs", {}).get("teams", []))
    new = []
    for e in events:
        p = e.get("payload") if isinstance(e.get("payload"), dict) else {}
        if e.get("type") == "egg.found" and p.get("team"):
            eggs.add(p["team"])
        if e.get("type") == "thread.message":
            sender, text = p.get("sender"), p.get("text") or ""
            if not sender or is_team(sender) or not text:
                continue
            keeper = sender == KEEPER and p.get("team") in eggs
            if not keeper and not HINT.search(text) and not QUOTED.search(text):
                continue
            if NOISE.search(text) and not re.search(r"chulapa|oro|moscow|ask (her|him)|pregúnt", text, re.I):
                continue
            key = f"{sender}|{norm(text)}"
            hit = seen.get(key)
            if hit:
                hit["last"], hit["count"] = e.get("tick"), hit["count"] + 1
                if p.get("team") not in hit["teams"]:
                    hit["teams"].append(p.get("team"))
                continue
            hit = {"kind": "message", "dealer": sender, "first": e.get("tick"), "last": e.get("tick"), "count": 1,
                   "teams": [p.get("team")], "text": text[:400]}
            seen[key] = hit
            new.append(hit)
        elif e.get("type") in EVENT_TYPES:
            key = f"{e['type']}|{e.get('id')}"
            if key in seen:
                continue
            hit = {"kind": e["type"], "dealer": p.get("persona") or e.get("actor"), "first": e.get("tick"),
                   "last": e.get("tick"), "count": 1, "teams": [p.get("team")] if p.get("team") else [],
                   "text": p.get("text") or json.dumps(p)[:300]}
            seen[key] = hit
            new.append(hit)
    seen["eggs"] = {"kind": "_eggs", "teams": sorted(eggs)}
    return new, seen


def scan_catalog(catalog: dict, before: dict) -> tuple[list[dict], dict]:
    """New hidden cards, and minted changes on epics and legendaries, against the last snapshot."""
    now, new = {}, []
    for s in catalog.get("sets") or []:
        for c in s.get("cards") or []:
            cid = c.get("id")
            now[cid] = {"hidden": bool(c.get("hidden")), "minted": c.get("minted"), "rarity": c.get("rarity"),
                        "name": c.get("name"), "print_run": c.get("print_run")}
            old = before.get(cid)
            if before and old is None:
                new.append({"kind": "catalog.new_card", "card": cid, **now[cid]})
            elif old and now[cid]["hidden"] and not old.get("hidden"):
                new.append({"kind": "catalog.hidden", "card": cid, **now[cid]})
            elif old and c.get("rarity") in ("epic", "legendary") and old.get("minted") != c.get("minted"):
                new.append({"kind": "catalog.minted", "card": cid, "was": old.get("minted"), **now[cid]})
    return new, now


def scan_news(text: str, seen: set) -> list[dict]:
    out = []
    for line in text.splitlines():
        if line.startswith("- ") and HINT.search(line) and line not in seen:
            seen.add(line)
            out.append({"kind": "news", "text": line[2:400]})
    return out


def line(h: dict) -> str:
    if h["kind"].startswith("catalog"):
        return f"HINT {h['kind']} {h['card']} ({h.get('name')}, {h.get('rarity')}, print run {h.get('print_run')}): " \
               f"hidden={h.get('hidden')} minted={h.get('minted')}" + (f" (was {h['was']})" if "was" in h else "")
    if h["kind"] == "news":
        return f"HINT news {h['text'][:300]}"
    return (f"HINT {h['kind']} tick {h['first']}{'-' + str(h['last']) if h['last'] != h['first'] else ''} · "
            f"{h.get('dealer')} → {', '.join(t for t in h['teams'] if t) or '?'} · {h['text'][:300]}")


class Miner:
    def __init__(self, pub=None, *, feed=FEED, news=NEWS, out=OUT, state=STATE, log=print, dry=False):
        self.pub, self.feed, self.news, self.out, self.state_path, self.log, self.dry = pub, feed, news, out, state, log, dry
        try:
            st = json.loads(Path(state).read_text())
        except (OSError, ValueError):
            st = {}
        self.pos, self.seen = st.get("pos", 0), st.get("seen", {})
        self.catalog, self.news_seen = st.get("catalog", {}), set(st.get("news_seen", []))
        self._cat_at = 0.0
        if "eggs" not in self.seen and self.pos:      # state from before the egg list: seed it from the whole feed
            teams = set()
            try:
                with Path(feed).open() as f:
                    for raw in f:
                        if '"egg.found"' in raw:
                            try:
                                teams.add((json.loads(raw).get("payload") or {}).get("team"))
                            except ValueError:
                                continue
            except OSError:
                pass
            self.seen["eggs"] = {"kind": "_eggs", "teams": sorted(t for t in teams if t)}

    def read_new(self) -> list:
        """Events appended to the feed since the last read (complete lines only; a truncated feed restarts)."""
        events = []
        try:
            path = Path(self.feed)
            if self.pos > path.stat().st_size:
                self.pos = 0
            with path.open("rb") as f:
                f.seek(self.pos)
                while True:
                    raw = f.readline()
                    if not raw or not raw.endswith(b"\n"):
                        break                          # end, or a half-written last line: next run
                    self.pos += len(raw)
                    try:
                        events.append(json.loads(raw))
                    except ValueError:
                        continue
        except OSError:
            pass
        return events

    def run_once(self) -> list[dict]:
        hits, self.seen = scan_events(self.read_new(), self.seen)
        try:
            hits += scan_news(Path(self.news).read_text(), self.news_seen)
        except OSError:
            pass
        if self.pub is not None and time.time() - self._cat_at >= CATALOG_EVERY_S:
            self._cat_at = time.time()
            try:
                new, self.catalog = scan_catalog(self.pub._call("GET", "/api/catalog"), self.catalog)
                hits += new
            except Exception as e:  # noqa: BLE001
                self.log(f"hints: catalog unavailable ({e!r})"[:200])
        for h in hits:
            self.log(line(h))
        if hits and not self.dry:
            new_file = not Path(self.out).exists()
            Path(self.out).parent.mkdir(parents=True, exist_ok=True)
            with Path(self.out).open("a") as f:
                if new_file:
                    f.write("# Dealer hints and hidden cards (tools/hints.py)\n\n_Every persona line with a hint pattern "
                            "(de-duplicated per dealer and text), egg/workshop/persona events, hidden or newly minted "
                            "epic/legendary cards. Newest at the bottom._\n\n")
                for h in hits:
                    f.write(f"- {time.strftime('%a %H:%M')} · {line(h)[5:]}\n")
        if not self.dry:
            Path(self.state_path).parent.mkdir(parents=True, exist_ok=True)
            Path(self.state_path).write_text(json.dumps({"pos": self.pos, "seen": self.seen, "catalog": self.catalog,
                                                         "news_seen": sorted(self.news_seen)[-2000:]}))
        return hits


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], allow_abbrev=False)
    ap.add_argument("--backfill", action="store_true", help="from the start of the feed (ignore the saved position)")
    ap.add_argument("--dry", action="store_true", help="print only: no file, no state")
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args(argv)
    from bazaar_sdk import _Http
    m = Miner(_Http(URL, {}, 15.0, False, 0), dry=args.dry)
    if args.backfill:
        m.pos, m.seen = 0, {}
    while True:
        try:
            m.run_once()
        except Exception as e:  # noqa: BLE001  a watcher keeps watching
            print(time.strftime("%H:%M:%S"), "hints error:", repr(e)[:200], flush=True)
        if args.once or args.dry:
            return
        time.sleep(20)


if __name__ == "__main__":
    main()
