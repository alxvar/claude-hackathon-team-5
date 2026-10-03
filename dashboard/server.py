"""Read-only live dashboard for The Bazaar: every team's trades, offers and score, with insights.

    python dashboard/server.py              # then open http://127.0.0.1:8765
    python dashboard/server.py --port 9000  # another port
    python dashboard/server.py --no-key     # public data only (no score, assets or duels of ours)
    python dashboard/server.py --no-hub     # don't read the team hub even if HUB_READER_URL is set

http://127.0.0.1:8765/show is the judges' showcase (judges/dashboard-brief.md): the same data plus judges/show.json.

It never writes to the game. Public routes (feed, leaderboard, El Rastro board, venues, catalog, schedule, levels,
dealers) are read without the team key; only `me` and `duels` use it. About 5-8 requests per tick, spaced 0.4 s
apart, so the team's 5 requests/s stay free for the live bots. The key comes from BAZAAR_KEY, the repo's .env or
~/bazaar_key.txt, stays in this process and is never printed; the page is served on 127.0.0.1 only. History is
cached in logs/dashboard/ (gitignored), so charts survive a restart.

With HUB_READER_URL (env or .env; see hub/README.md) it also reads the team hub (read-only), at start and every few
rounds, and merges the events, leaderboard snapshots and /api/me rows it hasn't seen: the hub's collectors fill
the holes left while the dashboard was off. Without the URL or psycopg it runs as before.
"""
import argparse
import collections
import json
import math
import os
import re
import statistics
import subprocess
import sys
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402


def _run(*args, **kwargs):
    """subprocess.run without a console window on Windows. The dashboard runs under pythonw (start.bat), so every
    git call would otherwise open a terminal window for a split second."""
    if os.name == "nt":
        kwargs.setdefault("creationflags", subprocess.CREATE_NO_WINDOW)
    return subprocess.run(*args, **kwargs)

HERE = Path(__file__).resolve().parent
CACHE = ROOT / "logs" / "dashboard"
TEAMS_MD = ROOT / "intel" / "teams.md"
SHOW_JSON = ROOT / "judges" / "show.json"   # the judges' showcase (/show): story texts Dani edits
MULT_JSON = ROOT / "intel" / "multipliers.json"   # the Analyst's per-team set multiplier estimates (read-only here)
URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
GAP = 0.4          # seconds between two requests
EDGE = 3           # P of gain, after fees, that makes an offer an opportunity
RECENT = 30        # ticks that count as "recent" for momentum
HUB_EVERY = 5      # rounds between two reads of the hub (plus one at start)
TOP_NEVER = 4      # feeding rule (intel/saturday-plan.md): never sell to the top 4
FEED_GAP = 10      # ...and a card that can close the buyer's page goes only to teams this many points below us


def env_value(name):
    """A setting from the environment, else from the repo's .env. Never printed."""
    if os.environ.get(name):
        return os.environ[name].strip()
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith(name + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'") or None
    return None


def load_key():
    key = env_value("BAZAAR_KEY")
    if key:
        return key
    f = Path.home() / "bazaar_key.txt"
    return f.read_text(encoding="utf-8").strip() if f.exists() else None


def redact(text):
    """Strip credentials from a database error before showing it."""
    return re.sub(r"(postgres(?:ql)?://)[^@\s]+@", r"\1***@", str(text))


class Collector:
    """Polls the game once per tick and keeps everything it has seen, in memory and in logs/dashboard/."""

    def __init__(self, key, hub_url=None):
        self.pub = Bazaar(URL, "", retries=2)
        self.pub._headers = {}  # public routes: don't spend the team's quota
        self.team = Bazaar(URL, key, retries=2, wait_on_tick=False) if key else None
        self.hub_url = hub_url
        self.hub = {"on": bool(hub_url), "last": None, "added": 0, "gaps": 0}
        self.hub_since = None   # the hub's clock at our last read: next read asks for rows ingested after it
        self.lock = threading.Lock()
        self.events = {}
        self.lb_hist = {}
        self.me_hist = []
        self.latest = {}
        self.errors = collections.deque(maxlen=15)
        self.requests = 0
        self.updated = None
        self.feed_gap = False
        self.teams_every = 0
        self.teams_push = False
        self.teams_last = 0.0
        self.directives, self.directives_src = "", None   # intel/directives.md: the team's decisions and their why
        CACHE.mkdir(parents=True, exist_ok=True)
        self._load()

    def _jsonl(self, name):
        p = CACHE / name
        if not p.exists():
            return []
        out = []
        for line in p.read_text(encoding="utf-8").splitlines():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        return out

    def _append(self, name, rows):
        if rows:
            with (CACHE / name).open("a", encoding="utf-8") as f:
                for r in rows:
                    f.write(json.dumps(r) + "\n")

    def _load(self):
        self.events = {e["id"]: e for e in self._jsonl("feed.jsonl")}
        self.lb_hist = {s["tick"]: s for s in self._jsonl("leaderboard.jsonl")}
        me = {r["tick"]: r for r in self._jsonl("me.jsonl") if r.get("tick") is not None}  # rows from the hub can be out of order
        self.me_hist = [me[t] for t in sorted(me)]

    def _get(self, name, fn):
        try:
            r = fn()
            self.requests += 1
            with self.lock:
                self.latest[name] = r
            return r
        except BazaarError as e:
            self.requests += 1
            self.errors.appendleft(f"{time.strftime('%H:%M:%S')} {name}: {e.code} {e.message[:120]}")
        except Exception as e:  # keep polling through anything
            self.errors.appendleft(f"{time.strftime('%H:%M:%S')} {name}: {e!r}"[:200])
        finally:
            time.sleep(GAP)
        return None

    def _ingest_feed(self, feed):
        evs = feed.get("events", [])
        with self.lock:
            known = max(self.events) if self.events else None
            fresh = [e for e in evs if e["id"] not in self.events]
            if known is not None and evs and min(e["id"] for e in evs) > known + 1:
                self.feed_gap = True  # we were away long enough to miss events
            for e in fresh:
                self.events[e["id"]] = e
        self._append("feed.jsonl", sorted(fresh, key=lambda e: e["id"]))

    def _ingest_lb(self, lb):
        tick = lb.get("snapshot_tick")
        if tick is None or tick in self.lb_hist:
            return
        snap = {"tick": tick, "t": lb.get("t"),
                "teams": {t["team"]: {"name": t.get("name"), "score": t.get("score"), "negotiating": t.get("negotiating"),
                                      "market": t.get("market"), "deals": t.get("deals"),
                                      "pages": t.get("pages_complete")} for t in lb.get("teams", [])}}
        with self.lock:
            self.lb_hist[tick] = snap
        self._append("leaderboard.jsonl", [snap])

    def _ingest_me(self, me, tick):
        s = me.get("score") or {}
        row = {"tick": tick, "score": s.get("score"), "rank": s.get("rank"), "neg_points": s.get("neg_points"),
               "negotiating": s.get("negotiating"), "market": s.get("market"), "cash": me.get("cash"),
               "ladder_points": s.get("ladder_points"), "duel_points": s.get("duel_points")}
        with self.lock:
            if self.me_hist and self.me_hist[-1]["tick"] == tick:
                return
            self.me_hist.append(row)
        self._append("me.jsonl", [row])

    def hub_sync(self):
        """Read-only pass over the team hub: merge the events, leaderboard snapshots and our /api/me rows we lack.

        What it adds also goes to logs/dashboard/, so the local cache is the union and survives a restart offline.
        The first pass asks for every event we don't have; later passes only for rows ingested since the last one
        (with a 2-minute overlap for rows that were mid-insert)."""
        try:
            import psycopg
        except ImportError:
            self.hub["on"] = False
            self.errors.appendleft(f"{time.strftime('%H:%M:%S')} hub: psycopg is not installed (pip install psycopg[binary])")
            return
        try:
            with psycopg.connect(self.hub_url, connect_timeout=10, autocommit=True,
                                 application_name="dashboard-dani") as conn, conn.cursor() as cur:
                cur.execute("select now()")
                now = cur.fetchone()[0]
                with self.lock:
                    known_ids = list(self.events)
                    known_lb = list(self.lb_hist)
                    known_me = [r["tick"] for r in self.me_hist]
                cols = "select id, tick, t_hours, type, scope, actor, payload from hub.events"
                if self.hub_since is not None:
                    cur.execute(cols + " where ingested_at > %s - interval '2 minutes'", (self.hub_since,))
                elif known_ids:
                    cur.execute(cols + " where not (id = any(%s))", (known_ids,))
                else:
                    cur.execute(cols)
                events = [{"id": i, "tick": tk, "t": t, "type": ty, "scope": sc, "actor": ac, "payload": p}
                          for i, tk, t, ty, sc, ac, p in cur.fetchall()]
                cur.execute("""select s.snapshot_tick, l.t_hours, s.team, s.name, s.score, s.negotiating, s.market, s.deals,
                                      s.pages_complete
                               from hub.team_snapshots s left join hub.leaderboard l using (snapshot_tick)
                               where not (s.snapshot_tick = any(%s))""", (known_lb or [-1],))
                lb_rows = cur.fetchall()
                pages = []
                if self.hub_since is None:  # first pass: page counts for the snapshots we had (older caches lack them)
                    cur.execute("select snapshot_tick, team, pages_complete from hub.team_snapshots "
                                "where snapshot_tick = any(%s)", (known_lb or [-1],))
                    pages = cur.fetchall()
                cur.execute("""select distinct on (tick) tick, data from hub.me_snapshots
                               where not (tick = any(%s)) order by tick, source""", (known_me or [-1],))
                me_rows = cur.fetchall()
                cur.execute("select count(*) from hub.gaps")
                gaps = cur.fetchone()[0]
        except Exception as e:
            self.errors.appendleft(f"{time.strftime('%H:%M:%S')} hub: {redact(e)}"[:200])
            return
        snaps = {}
        for tick, t, team, name, score, neg, market, deals, pages_complete in lb_rows:
            s = snaps.setdefault(tick, {"tick": tick, "t": t, "teams": {}})
            s["teams"][team] = {"name": name, "score": score, "negotiating": neg, "market": market, "deals": deals,
                                "pages": pages_complete}
        me_keys = ("score", "rank", "neg_points", "negotiating", "market", "cash", "ladder_points", "duel_points")
        with self.lock:
            new_ev = [e for e in events if e["id"] not in self.events]
            for e in new_ev:
                self.events[e["id"]] = e
            new_lb = [s for k, s in sorted(snaps.items()) if k not in self.lb_hist]
            for s in new_lb:
                self.lb_hist[s["tick"]] = s
            for tick, team, pg in pages:
                row = (self.lb_hist.get(tick) or {}).get("teams", {}).get(team)
                if row is not None and row.get("pages") is None:
                    row["pages"] = pg
            have = {r["tick"] for r in self.me_hist}
            new_me = [{"tick": tick, **{k: (d or {}).get(k) for k in me_keys}} for tick, d in me_rows if tick not in have]
            if new_me:
                self.me_hist = sorted(self.me_hist + new_me, key=lambda r: r["tick"])
            self.hub_since = now
            self.feed_gap = False  # the hub's two collectors cover what we missed; their own holes are in hub.gaps
            self.hub.update(last=time.strftime("%H:%M:%S"), added=self.hub["added"] + len(new_ev), gaps=gaps)
        self._append("feed.jsonl", sorted(new_ev, key=lambda e: e["id"]))
        self._append("leaderboard.jsonl", new_lb)
        self._append("me.jsonl", new_me)

    def read_directives(self):
        """The team's decisions (intel/directives.md) as they are on GitHub. `git fetch` only moves the remote refs,
        never the working tree, so it can't disturb the sync hook or anyone's edits; the local copy is the fallback."""
        git = ["git", "-C", str(ROOT)]
        env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        try:
            _run(git + ["fetch", "-q", "origin", "main"], capture_output=True, timeout=30, env=env)
            r = _run(git + ["show", "origin/main:intel/directives.md"], capture_output=True, timeout=10, env=env)
            if r.returncode == 0 and r.stdout:
                self.directives = r.stdout.decode("utf-8", "replace")
                self.directives_src = f"GitHub, read {time.strftime('%H:%M')}"
                return
        except (OSError, subprocess.SubprocessError):
            pass
        f = ROOT / "intel" / "directives.md"
        if f.exists():
            self.directives, self.directives_src = f.read_text(encoding="utf-8"), "local copy"

    def write_teams(self):
        """Rewrite intel/teams.md and, with --push, commit and push that one file (retries on a busy git)."""
        try:
            text = Analysis(self).teams_md()
            TEAMS_MD.write_text(text, encoding="utf-8")
        except Exception as e:
            self.errors.appendleft(f"{time.strftime('%H:%M:%S')} teams.md: {e!r}"[:200])
            return
        if not self.teams_push:
            return
        git = ["git", "-C", str(ROOT)]
        rel = str(TEAMS_MD.relative_to(ROOT)).replace("\\", "/")
        # The same guards as tools/gitsync.py (which needs fcntl, so not on Windows): never pull over work in progress
        # (Sat 09:44-09:52 a pull --autostash over a half-done edit discarded other sessions' work 13 times).
        if (ROOT / "run" / "git-paused").exists():
            return
        gitdir = Path(_run(git + ["rev-parse", "--absolute-git-dir"], capture_output=True,
                                     text=True).stdout.strip())
        if any((gitdir / d).exists() for d in ("rebase-merge", "rebase-apply", "MERGE_HEAD")):
            self.errors.appendleft(f"{time.strftime('%H:%M:%S')} teams.md: a rebase/merge is under way, not pushed")
            return
        code = ("agents/", "tools/", "tests/", "engine/", "broker/", "dashboard/", "hub/", "bazaar-kit/",
                "pyproject.toml", "uv.lock")
        wip = [ln[3:] for ln in _run(git + ["status", "--porcelain"], capture_output=True,
                                               text=True).stdout.splitlines()
               if not ln.startswith("??") and ln[3:].strip('"').startswith(code)]
        for attempt in range(3):
            _run(git + ["add", "--", rel], capture_output=True)
            if _run(git + ["diff", "--cached", "--quiet", "--", rel]).returncode == 0:
                return
            c = _run(git + ["commit", "-q", "-m", f"intel: teams.md (Dani's dashboard, {time.strftime('%H:%M')})",
                                      "--", rel], capture_output=True, text=True)
            if c.returncode == 0:
                if wip:  # a code edit in the tree: keep the commit local, the next clean round pushes it
                    self.errors.appendleft(f"{time.strftime('%H:%M:%S')} teams.md: committed, not pushed "
                                           f"(work in progress in {', '.join(wip[:2])})")
                    return
                if _run(git + ["pull", "--rebase", "--autostash", "-q", "origin", "main"],
                                  capture_output=True).returncode != 0:
                    _run(git + ["rebase", "--abort"], capture_output=True)
                    self.errors.appendleft(f"{time.strftime('%H:%M:%S')} teams.md: pull conflicted (aborted), "
                                           "committed, not pushed")
                    return
                p = _run(git + ["push", "-q", "origin", "HEAD:main"], capture_output=True, text=True)
                if p.returncode == 0:
                    return
                self.errors.appendleft(f"{time.strftime('%H:%M:%S')} teams.md push: {p.stderr.strip()[:150]}")
                return
            time.sleep(5)  # git busy (index.lock): try again
        self.errors.appendleft(f"{time.strftime('%H:%M:%S')} teams.md: git busy, will retry next round")

    def run(self):
        n = 0
        while True:
            if self.hub["on"] and n % HUB_EVERY == 0:
                self.hub_sync()  # before the feed, so a restart's gap is filled before it is flagged
            clock = self._get("clock", self.pub.clock) or {}
            feed = self._get("feed", lambda: self.pub.feed(limit=500))
            if feed:
                self._ingest_feed(feed)
            lb_old = self.latest.get("leaderboard") or {}
            if n == 0 or clock.get("tick", 0) >= (lb_old.get("next_refresh_tick") or 0):
                lb = self._get("leaderboard", self.pub.leaderboard)
                if lb:
                    self._ingest_lb(lb)
            self._get("board", lambda: self.pub.board("rastro"))
            if self.team:
                me = self._get("me", self.team.me)
                if me:
                    self._ingest_me(me, clock.get("tick"))
                self._get("duels", self.team.duels)
                if n % 3 == 0:
                    self._get("duels_done", lambda: self.team.duels(done=True))
            if n % 10 == 0:
                for name, fn in (("catalog", self.pub.catalog), ("schedule", self.pub.schedule),
                                 ("levels", self.pub.levels), ("dealers", self.pub.dealers),
                                 ("venues", self.pub.venues)):
                    self._get(name, fn)
                self.read_directives()
            self.updated = time.time()
            if self.teams_every and time.time() - self.teams_last >= self.teams_every and self.team:
                self.teams_last = time.time()
                self.write_teams()
            n += 1
            wait = float(clock.get("next_tick_in") or 30) + 1.0
            if clock.get("paused"):
                wait = 60
            time.sleep(min(65.0, max(5.0, wait)))


# ---------------------------------------------------------------------------------------------- analysis

def cash_of(side):
    return (side or {}).get("cash") or 0


def refs_of(side):
    """Card refs on one side of an offer: concrete assets, or wanted types ("card:LAV-09")."""
    side = side or {}
    out = [a.get("ref") for a in side.get("assets", []) if isinstance(a, dict) and a.get("kind", "card") == "card"]
    out += [t.split(":", 1)[1] for t in side.get("types", []) if isinstance(t, str) and t.startswith("card:")]
    return [r for r in out if r]


def set_of(ref):
    return ref.split("-")[0] if ref and "-" in ref else "?"


def median(xs):
    return statistics.median(xs) if xs else None


class Analysis:
    def __init__(self, c: Collector):
        with c.lock:
            evs = list(c.events.values())
            # the hub stores Friday's backfilled settlements as id = −settlement number: drop one if the real event exists
            real = {(e.get("payload") or {}).get("settlement") for e in evs if e["id"] > 0 and e.get("type") == "settlement"}
            self.events = sorted((e for e in evs if e["id"] > 0 or e.get("type") != "settlement"
                                  or (e.get("payload") or {}).get("settlement") not in real),
                                 key=lambda e: (e.get("tick") or 0, e["id"]))
            self.lb_hist = [c.lb_hist[k] for k in sorted(c.lb_hist)]
            self.me_hist = list(c.me_hist)
            L = dict(c.latest)
        self.c = c
        self.clock = L.get("clock") or {}
        self.lb = L.get("leaderboard") or {}
        self.board = (L.get("board") or {}).get("offers", [])
        self.me = L.get("me") or {}
        self.cat = L.get("catalog") or {}
        self.sched = L.get("schedule") or {}
        self.levels = (L.get("levels") or {}).get("levels", [])
        self.dealers = (L.get("dealers") or {}).get("personas", [])
        self.venues = (L.get("venues") or {}).get("venues", [])
        self.duels = (L.get("duels") or {}).get("duels", [])
        self.duels_done = (L.get("duels_done") or {}).get("duels", [])
        self.us = self.me.get("id") or "t05"
        self.names = {t["team"]: t.get("name", t["team"]) for t in self.lb.get("teams", [])}
        for d in self.dealers:
            self.names.setdefault(d["id"], d.get("name", d["id"]))
        self.aff = self.me.get("affinity") or {}
        rar = self.cat.get("rarities") or {}
        self.book = {k: v.get("book") for k, v in rar.items()}
        self.cards = {}
        for st in self.cat.get("sets", []):
            for cd in st.get("cards", []):
                if isinstance(cd, dict) and cd.get("id"):
                    self.cards[cd["id"]] = {"name": cd.get("name"), "rarity": cd.get("rarity"), "set": st.get("id"),
                                            "page": cd.get("page"), "book": cd.get("book")}
        self.marg = (self.cat.get("values") or {}).get("copy_marginals") or [1.0]
        self.held = collections.Counter(a.get("ref") for a in self.me.get("assets", []) if a.get("kind") == "card")
        self.held_value = collections.defaultdict(list)
        for a in self.me.get("assets", []):
            if a.get("kind") == "card" and a.get("your_value") is not None:
                self.held_value[a["ref"]].append(a["your_value"])
        rastro = next((v for v in self.venues if v.get("venue") == "rastro"), {})
        self.fee_bps = rastro.get("fee_bps", 500)
        self.fee_card = rastro.get("fee_per_card", 1)

    def name(self, tid):
        return self.names.get(tid, tid or "?")

    def rarity(self, ref):
        return (self.cards.get(ref) or {}).get("rarity")

    def fee(self, price, ncards=1):
        return math.ceil(price * self.fee_bps / 10000) + self.fee_card * ncards

    def value_more(self, ref):
        """Our private value of one more copy of `ref` (book × our affinity × copy marginal). An estimate."""
        r, s = self.rarity(ref), set_of(ref)
        if not r or s not in self.aff or not self.book.get(r):
            return None
        k = min(self.held.get(ref, 0), len(self.marg) - 1)
        return round(self.book[r] * self.aff[s] * self.marg[k], 1)

    def value_held(self, ref):
        v = self.held_value.get(ref)
        return min(v) if v else None

    def token_bid(self, ref, price):
        """A bid under half the card's book price (Team 13's 2 P bids on RET commons): no sign the team collects it."""
        book = self.book.get(self.rarity(ref))
        return bool(book) and price < book / 2

    def feeding_block(self, p, us_score):
        """Why the feeding rule forbids selling team profile `p` a card that can close its page, or None if allowed."""
        if p["rank"] <= TOP_NEVER:
            return f"top {TOP_NEVER}"
        gap = (us_score or 0) - (p["score"] or 0)
        if gap < FEED_GAP:
            return f"only {gap:.1f} below us" if gap >= 0 else f"{-gap:.1f} above us"
        return None

    # -------------------------------------------------------------------------------------- the pass over the feed
    def scan(self):
        self.maker = {}
        self.trades = []
        self.holder = {}
        self.threads = {}
        self.packs = collections.Counter()
        self.gifts = collections.Counter()
        self.listings = collections.Counter()
        # team -> set -> distinct cards it bid for / listed for sale: a card relisted every few ticks counts once
        # (Team 12 relisted one spare MAL-02 ~23 times while buying 6 MAL cards, which read as "dumps MAL")
        self.bids = collections.defaultdict(lambda: collections.defaultdict(set))
        self.asks = collections.defaultdict(lambda: collections.defaultdict(set))
        self.news = []
        self.duel_events = []
        self.duel_closed = []
        for e in self.events:
            p, ty = e.get("payload") or {}, e.get("type", "")
            if ty == "offer.listed":
                o = p.get("offer") or {}
                who = e.get("actor") or o.get("maker")
                self.maker[o.get("id")] = who
                self.listings[who] += 1
                if cash_of(o.get("give")) and refs_of(o.get("want")):
                    each = cash_of(o.get("give")) / len(refs_of(o.get("want")))
                    for r in refs_of(o.get("want")):
                        if not self.token_bid(r, each):
                            self.bids[who][set_of(r)].add(r)
                elif refs_of(o.get("give")) and cash_of(o.get("want")):
                    for r in refs_of(o.get("give")):
                        self.asks[who][set_of(r)].add(r)
            elif ty == "settlement":
                items = [i for i in p.get("items", []) if i.get("kind") == "card" or i.get("ref")]
                kind = "dealer" if p.get("persona") else "team"
                self.trades.append({"tick": p.get("tick", e.get("tick")), "kind": kind, "dealer": p.get("persona"),
                                    "venue": p.get("venue"), "price": p.get("price") or 0, "fee": p.get("fee") or 0,
                                    "items": items, "parties": p.get("parties", [])})
                for i in items:
                    if i.get("id") is not None:
                        self.holder[i["id"]] = {"ref": i.get("ref"), "team": i.get("to"), "tick": p.get("tick"),
                                                "price": p.get("price"), "frm": i.get("frm")}
            elif ty == "thread.message" and p.get("kind") == "persona":
                th = self.threads.setdefault(p.get("thread"), {"team": p.get("team"), "dealer": p.get("with"),
                                                               "dealer_prices": [], "team_prices": [], "msgs": 0,
                                                               "side": None, "log": [], "item": None})
                th["msgs"] += 1
                o = p.get("offer") or {}
                mine = p.get("sender") == p.get("with")
                price = None
                if o:
                    gives, wants = cash_of(o.get("give")), cash_of(o.get("want"))
                    price = wants if mine and wants else gives if mine else gives if gives else wants
                    if mine:
                        th["side"] = "team buys" if wants else "team sells"
                    (th["dealer_prices"] if mine else th["team_prices"]).append(price)
                    th["item"] = th["item"] or ", ".join(refs_of(o.get("give")) + refs_of(o.get("want"))) or None
                th["log"].append({"tick": e.get("tick"), "dealer": mine, "text": (p.get("text") or "")[:400],
                                  "price": price, "final": bool(o.get("final")) if o else False})
            elif ty == "duel.closed":
                self.duel_closed.append(p)
            elif ty == "pack.opened":
                self.packs[p.get("team")] += 1
            elif ty == "gift.given":
                self.gifts[p.get("team")] += 1
            elif ty.startswith("duel"):
                self.duel_events.append(e)
            if ty.startswith(("level", "announcement", "schedule", "venue", "dealer")) or ty in ("set.released",):
                self.news.append({"tick": e.get("tick"), "type": ty, "text": json.dumps(p, ensure_ascii=False)[:220]})

    # -------------------------------------------------------------------------------------- per-team profiles
    def profiles(self):
        teams = sorted(self.lb.get("teams", []), key=lambda t: -(t.get("score") or 0))
        rank = {t["team"]: i + 1 for i, t in enumerate(teams)}
        hist = self.lb_hist
        then = None
        if hist:
            last = hist[-1]["tick"]
            older = [h for h in hist if h["tick"] <= last - RECENT]
            then = older[-1] if older else hist[0]
        our_rank = rank.get(self.us, 99)
        top_sets = {s for s, a in self.aff.items() if a >= 1.1}
        low_sets = {s for s, a in self.aff.items() if a < 1.0}
        out = []
        for t in teams:
            tid = t["team"]
            buys, sells, dbuys, dsells = (collections.Counter() for _ in range(4))
            team_trades = dealer_trades = 0
            volume = 0
            prices = []
            biggest = None
            for tr in self.trades:
                if tid not in tr["parties"]:
                    continue
                if tr["kind"] == "team":
                    team_trades += 1
                    volume += tr["price"]
                    prices.append(tr["price"])
                    if not biggest or tr["price"] > biggest["price"]:
                        biggest = tr
                else:
                    dealer_trades += 1
                for i in tr["items"]:
                    if i.get("kind", "card") != "card":
                        continue
                    s = i.get("set") or set_of(i.get("ref"))
                    if i.get("to") == tid:
                        (buys if tr["kind"] == "team" else dbuys)[s] += 1
                    elif i.get("frm") == tid:
                        (sells if tr["kind"] == "team" else dsells)[s] += 1
            interest = collections.Counter()
            for s, k in (buys + dbuys).items():
                interest[s] += 2 * k
            for s, k in self.bids[tid].items():
                interest[s] += len(k)
            dumping = collections.Counter()
            for s, k in (sells + dsells).items():
                dumping[s] += 2 * k
            for s, k in self.asks[tid].items():
                dumping[s] += len(k)
            net = {s: interest[s] - dumping[s] for s in set(interest) | set(dumping)}
            wants = [s for s, v in sorted(net.items(), key=lambda kv: -kv[1]) if v >= 2][:3]
            dumps = [s for s, v in sorted(net.items(), key=lambda kv: kv[1]) if v <= -2][:3]
            labels = []
            if wants:
                labels.append(f"Collects {'/'.join(wants)}")
            if team_trades >= 3:
                labels.append("Team trader")
            if dealer_trades >= 4 and dealer_trades >= 2 * team_trades:
                labels.append("Dealer grinder")
            if self.packs[tid] >= 3:
                labels.append("Pack opener")
            if self.listings[tid] >= 15:
                labels.append("Market maker")
            if team_trades + dealer_trades + self.listings[tid] < 3:
                labels.append("Quiet")
            relation = []
            if tid != self.us:
                comp = [s for s in wants if s in top_sets]
                buyer = [s for s in wants if s in low_sets]
                if comp:
                    relation.append(("rival", f"competes for {'/'.join(comp)}"))
                if buyer:
                    relation.append(("buyer", f"buys {'/'.join(buyer)} from us" +
                                     (" (below us: good)" if rank.get(tid, 0) > our_rank else " (above us)")))
                sup = [s for s in dumps if s in top_sets]
                if sup:
                    relation.append(("seller", f"sells {'/'.join(sup)}: source for us"))
            prev = (then or {}).get("teams", {}).get(tid, {}).get("score") if then else None
            out.append({
                "team": tid, "name": t.get("name"), "rank": rank[tid], "us": tid == self.us,
                "score": t.get("score"), "negotiating": t.get("negotiating"), "market": t.get("market"),
                "level": t.get("level"), "album": f"{t.get('album_filled')}/{t.get('album_slots')}",
                "pages": t.get("pages_complete"), "deals": t.get("deals"), "luck": t.get("luck"),
                "delta": round((t.get("score") or 0) - prev, 2) if prev is not None else None,
                "team_trades": team_trades, "dealer_trades": dealer_trades, "volume": volume,
                "avg_price": round(statistics.mean(prices), 1) if prices else None,
                "packs": self.packs[tid], "listings": self.listings[tid], "gifts": self.gifts[tid],
                "wants": wants, "dumps": dumps, "labels": labels, "relation": relation,
                "biggest": self.trade_text(biggest) if biggest else None,
            })
        self.rank = rank
        self.then = then
        return out

    def trade_text(self, tr):
        refs = ", ".join(i.get("ref", "?") for i in tr["items"]) or "cash"
        frm = tr["items"][0].get("frm") if tr["items"] else None
        to = tr["items"][0].get("to") if tr["items"] else None
        return f"{self.name(to)} bought {refs} from {self.name(frm)} for {tr['price']} P (tick {tr['tick']})"

    # -------------------------------------------------------------------------------------- the market
    def market(self):
        rows = []
        for o in self.board:
            if o.get("status") not in (None, "open"):
                continue
            team = self.maker.get(o.get("id"))
            give, want = o.get("give") or {}, o.get("want") or {}
            if cash_of(give) and refs_of(want):
                side, refs, price = "bid", refs_of(want), cash_of(give)
            elif refs_of(give) and cash_of(want):
                side, refs, price = "ask", refs_of(give), cash_of(want)
            else:
                side, refs, price = "swap", refs_of(give) + refs_of(want), cash_of(give) or cash_of(want)
            ref = refs[0] if refs else None
            row = {"id": o.get("id"), "team": team, "name": self.name(team) if team else "unknown",
                   "ours": team == self.us, "side": side, "ref": ref, "n": len(refs), "price": price,
                   "card": (self.cards.get(ref) or {}).get("name"), "rarity": self.rarity(ref), "set": set_of(ref),
                   "to": o.get("to"), "expires": o.get("expires_tick"), "created": o.get("created_tick"),
                   "value": None, "edge": None}
            if team != self.us and ref and len(refs) == 1:
                if side == "ask":
                    v = self.value_more(ref)
                    if v is not None:
                        row["value"], row["edge"] = v, round(v - price - self.fee(price), 1)
                elif side == "bid" and self.held.get(ref):
                    v = self.value_held(ref)
                    if v is not None:
                        row["value"], row["edge"] = v, round(price - v - self.fee(price), 1)
            rows.append(row)
        rows.sort(key=lambda r: (-(r["edge"] if r["edge"] is not None else -999), r["side"], r["ref"] or ""))
        return rows

    def prices(self):
        by_r = collections.defaultdict(list)
        by_rd = collections.defaultdict(list)
        last = {}
        for tr in self.trades:
            if len(tr["items"]) != 1:
                continue
            i = tr["items"][0]
            r = i.get("rarity") or self.rarity(i.get("ref"))
            (by_r if tr["kind"] == "team" else by_rd)[r].append(tr["price"])
            if tr["kind"] == "team":
                last[i.get("ref")] = tr["price"]
        order = ["common", "uncommon", "rare", "epic", "legendary"]
        rows = []
        for r in order:
            t, d = by_r.get(r, []), by_rd.get(r, [])
            if not t and not d:
                continue
            rows.append({"rarity": r, "book": self.book.get(r), "team_n": len(t), "team_median": median(t),
                         "team_min": min(t) if t else None, "team_max": max(t) if t else None,
                         "dealer_n": len(d), "dealer_median": median(d)})
        return rows, last

    def team_trades(self, prof):
        """Every settled trade between two teams (El Rastro and the teams' venues), newest first, from the feed we hold.

        A cash trade has one side giving cards and the other paying `price`; a swap moves cards both ways (plus any
        price). "Value created" is the venue's market-making signal: buyer's value − seller's value of the cards,
        estimated as book × (buyer's set multiplier − seller's), with ours exact (/api/me affinity) and the others from
        intel/multipliers.json (the Analyst's estimates [L]); None when a multiplier is unknown. Second copies are worth
        less to their holder, so it reads high on spares."""
        try:
            mult = json.loads(MULT_JSON.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            mult = {}

        def m_of(team, s):
            if team == self.us:
                return self.aff.get(s)
            return ((mult.get(team) or {}).get(s) or {}).get("m")

        byprof = {p["team"]: p for p in prof}
        vname = {v.get("venue"): v for v in self.venues}
        top4 = {p["team"] for p in prof if p["rank"] <= 4}
        opens = sorted(((e.get("tick") or 0), str((e.get("payload") or {}).get("day") or "").capitalize())
                       for e in self.events if e.get("type") == "day.opened")
        rows = []
        for tr in self.trades:
            if tr["kind"] != "team" or len(tr["parties"]) != 2:
                continue
            items = tr["items"]
            if not items:
                continue
            givers = {i.get("frm") for i in items}
            a, b = tr["parties"]
            swap = len(givers) > 1
            if swap:
                seller, buyer = a, b
            else:
                seller = items[0].get("frm")
                buyer = next((p for p in tr["parties"] if p != seller), None)
            created, known = 0.0, True
            for i in items:
                s, book = set_of(i.get("ref")), self.book.get(i.get("rarity")) or 0
                m_to, m_from = m_of(i.get("to"), s), m_of(i.get("frm"), s)
                if m_to is None or m_from is None:
                    known = False
                else:
                    created += book * (m_to - m_from)
            sets = sorted({set_of(i.get("ref")) for i in items})
            v = {} if tr["venue"] == "rastro" else (vname.get(tr["venue"]) or {})  # El Rastro is the house's
            day = next((d for t, d in reversed(opens) if t <= (tr["tick"] or 0)), "Fri")
            first = items[0]
            book = self.book.get(first.get("rarity"))
            bp, sp = byprof.get(buyer) or {}, byprof.get(seller) or {}
            rows.append({
                "tick": tr["tick"], "day": day, "venue": tr["venue"],
                "venue_name": "El Rastro" if tr["venue"] == "rastro" else (v.get("name") or tr["venue"]),
                "venue_owner": v.get("owner"), "on_ours": v.get("owner") == self.us,
                "kind": "swap" if swap else "cash",
                "seller": seller, "buyer": buyer, "seller_name": self.name(seller), "buyer_name": self.name(buyer),
                "seller_rank": sp.get("rank"), "buyer_rank": bp.get("rank"),
                "refs": [i.get("ref") for i in items],
                "items": [{"ref": i.get("ref"), "name": i.get("name"), "rarity": i.get("rarity"), "frm": i.get("frm"),
                           "to": i.get("to")} for i in items],
                "card": first.get("name"), "rarity": first.get("rarity"), "sets": sets,
                "price": tr["price"], "fee": tr["fee"],
                "vs_book": round(tr["price"] / book, 2) if book and not swap and len(items) == 1 and tr["price"] else None,
                "buyer_collects": any(s in (bp.get("wants") or []) for s in sets),
                "seller_dumps": any(s in (sp.get("dumps") or []) for s in sets),
                "created": round(created, 1) if known else None,
                "ours": self.us in tr["parties"], "top4": bool(top4 & set(tr["parties"])),
            })
        rows.sort(key=lambda r: -(r["tick"] or 0))

        venues = {}
        for r in rows:
            g = venues.setdefault(r["venue"], {"venue": r["venue"], "name": r["venue_name"], "owner": r["venue_owner"],
                                               "owner_name": self.name(r["venue_owner"]) if r["venue_owner"] else "the house",
                                               "ours": r["on_ours"], "trades": 0, "today": 0, "volume": 0, "fees": 0,
                                               "created": 0.0, "created_n": 0, "last": None})
            g["trades"] += 1
            g["today"] += r["day"] == rows[0]["day"]
            g["volume"] += r["price"] or 0
            g["fees"] += r["fee"] or 0
            if r["created"] is not None:
                g["created"] = round(g["created"] + r["created"], 1)
                g["created_n"] += 1
            g["last"] = max(g["last"] or 0, r["tick"] or 0)
        for g in venues.values():
            fee = (vname.get(g["venue"]) or {}).get("fee_bps")
            g["fee"] = "5 % + 1 P" if g["venue"] == "rastro" else (f"{fee / 100:g} %" if fee is not None else "—")

        teams = {}
        for r in rows:
            for tid, side in ((r["buyer"], "buy"), (r["seller"], "sell")):
                if not tid:
                    continue
                g = teams.setdefault(tid, {"team": tid, "name": self.name(tid), "rank": (byprof.get(tid) or {}).get("rank"),
                                           "us": tid == self.us, "buys": 0, "sells": 0, "swaps": 0, "spent": 0,
                                           "received": 0, "today": 0, "sets_bought": collections.Counter()})
                g["today"] += r["day"] == rows[0]["day"]
                if r["kind"] == "swap":
                    g["swaps"] += 1
                    continue
                if side == "buy":
                    g["buys"] += 1
                    g["spent"] += r["price"] or 0
                    g["sets_bought"].update(r["sets"])
                else:
                    g["sells"] += 1
                    g["received"] += r["price"] or 0
        team_rows = []
        for g in teams.values():
            g["sets_bought"] = ", ".join(f"{s} {n}" for s, n in g["sets_bought"].most_common(3))
            team_rows.append(g)
        team_rows.sort(key=lambda g: -(g["buys"] + g["sells"] + g["swaps"]))

        today = [r for r in rows if rows and r["day"] == rows[0]["day"]]
        return {"rows": rows, "venues": sorted(venues.values(), key=lambda g: -g["trades"]), "teams": team_rows,
                "summary": {"n": len(rows), "today": len(today), "day": rows[0]["day"] if rows else None,
                            "volume_today": sum(r["price"] or 0 for r in today),
                            "rastro_today": sum(1 for r in today if r["venue"] == "rastro"),
                            "swaps_today": sum(1 for r in today if r["kind"] == "swap"),
                            "ours_venue": sum(1 for r in rows if r["on_ours"]),
                            "ours_venue_created": round(sum(r["created"] or 0 for r in rows if r["on_ours"]), 1),
                            "last_tick": rows[0]["tick"] if rows else None, "now": self.clock.get("tick"),
                            "mult_updated": (mult.get("_meta") or {}).get("updated")}}

    def collection(self, prof):
        """Our cards (/api/me assets, with the game's your_value for each copy): every set's page (cards 01-10) and
        epics, and every duplicate with its extra copies, what one spare is worth to us (the lowest your_value: what a
        sale of one copy gives up), today's median team price for its rarity, our open asks on El Rastro, and the
        non-rival teams that collect the set or bid for the card now. Rival = live top 6 or within 3.0 of us, plus
        Teams 13 and 17 (Lucas's v10 rule)."""
        assets = [a for a in self.me.get("assets", []) if a.get("kind") == "card" and a.get("ref")]
        if not assets:
            return None
        us = next((p for p in prof if p["us"]), None)
        us_score = us["score"] if us else None
        rival = {p["team"] for p in prof if not p["us"] and (p["rank"] <= 6 or (us_score is not None and p["score"] is not None
                                                                              and abs(p["score"] - us_score) <= 3.0))}
        rival |= {"t13", "t17"}
        vals = collections.defaultdict(list)
        for a in assets:
            vals[a["ref"]].append(a.get("your_value"))
        opened = self._day_open()
        med = collections.defaultdict(list)
        last = {}
        for tr in self.trades:
            if tr["kind"] != "team" or len(tr["items"]) != 1 or not tr["price"]:
                continue
            i = tr["items"][0]
            if (tr["tick"] or 0) >= opened:
                med[i.get("rarity")].append(tr["price"])
            last[i.get("ref")] = (tr["price"], tr["tick"])
        bids, ours_ask = collections.defaultdict(list), collections.defaultdict(list)
        for o in self.board:
            who = self.maker.get(o.get("id"))
            if cash_of(o.get("give")) and refs_of(o.get("want")) and who and who != self.us:
                for r in refs_of(o.get("want")):
                    bids[r].append((who, round(cash_of(o.get("give")) / len(refs_of(o.get("want"))), 1)))
            elif refs_of(o.get("give")) and who == self.us:
                for r in refs_of(o.get("give")):
                    ours_ask[r].append(cash_of(o.get("want")))
        byprof = {p["team"]: p for p in prof}
        dups = []
        for ref, vs in vals.items():
            if len(vs) < 2:
                continue
            cd = self.cards.get(ref) or {}
            s = set_of(ref)
            known = sorted(v for v in vs if v is not None)
            buyers = [{"team": t, "name": self.name(t), "rank": (byprof.get(t) or {}).get("rank"), "why": f"bids {p} P"}
                      for t, p in bids.get(ref, []) if t not in rival]
            seen = {b["team"] for b in buyers}
            buyers += [{"team": p["team"], "name": p["name"], "rank": p["rank"], "why": f"collects {s}"}
                       for p in prof if not p["us"] and p["team"] not in rival and p["team"] not in seen and s in (p.get("wants") or [])]
            m = med.get(cd.get("rarity")) or []
            dups.append({"ref": ref, "name": cd.get("name"), "rarity": cd.get("rarity"), "set": s, "page": cd.get("page"),
                         "copies": len(vs), "extra": len(vs) - 1, "spare_value": known[0] if known else None,
                         "values": known, "book": cd.get("book"), "market": median(m) if m else None, "market_n": len(m),
                         "last": last.get(ref), "our_ask": sorted(ours_ask.get(ref, [])),
                         "bids": sorted((b for b in bids.get(ref, [])), key=lambda x: -x[1])[:4], "buyers": buyers[:6]})
        dups.sort(key=lambda r: (-(r["spare_value"] or 0), r["ref"]))
        sets = []
        for st in self.cat.get("sets", []):
            sid = st.get("id")
            page = [cd.get("id") for cd in st.get("cards", []) if isinstance(cd, dict) and cd.get("page")]
            extra = [cd.get("id") for cd in st.get("cards", []) if isinstance(cd, dict) and not cd.get("page")]
            if not st.get("released") and not any(set_of(r) == sid for r in vals):
                continue
            sets.append({"set": sid, "name": st.get("name"), "affinity": self.aff.get(sid),
                         "cards": [{"ref": r, "n": len(vals.get(r, [])), "rarity": (self.cards.get(r) or {}).get("rarity")}
                                   for r in page + extra],
                         "page_have": sum(1 for r in page if vals.get(r)), "page_size": len(page),
                         "complete": bool(page) and all(vals.get(r) for r in page)})
        return {"sets": sets, "dups": dups,
                "summary": {"copies": len(assets), "distinct": len(vals), "dup_refs": len(dups),
                            "extra": sum(d["extra"] for d in dups),
                            "spare_value": round(sum(d["spare_value"] or 0 for d in dups), 1),
                            "pages": sum(1 for s in sets if s["complete"])},
                "rivals": sorted(rival)}

    def _day_open(self):
        return max((e.get("tick") or 0 for e in self.events if e.get("type") == "day.opened"), default=0)

    def _nm(self, x):
        """A team or dealer name; dealers missing from the names map read 'Pilar', not 'pilar'."""
        n = self.name(x)
        return n if n != x else str(x or "?").capitalize()

    def _deal_text(self, tr, tid):
        """One settled deal, from team `tid`'s side: 'bought SAL-06 from Team 8 on El Rastro (28 P)'."""
        nm = self._nm
        items = tr["items"]
        refs = ", ".join(i.get("ref") or "?" for i in items)
        where = "El Rastro" if tr["venue"] == "rastro" else (tr["venue"] or "")
        if len({i.get("frm") for i in items}) > 1:
            other = next((p for p in tr["parties"] if p != tid), None)
            return f"swapped {refs} with {nm(other)}" + (f" on {where}" if where else "")
        frm, to = items[0].get("frm"), items[0].get("to")
        if to == tid:
            return f"bought {refs} from {nm(frm)}" + (f" on {where}" if where else "") + f" ({tr['price']} P)"
        if frm == tid:
            return f"sold {refs} to {nm(to)}" + (f" on {where}" if where else "") + f" ({tr['price']} P)"
        return f"{nm(frm)} → {nm(to)}: {refs} on its stall {where} ({tr['price']} P)"

    def market_pulse(self, prof):
        """The market since payday (the organisers' 400 P grant), or the last two hours: every settled deal with a team
        or a dealer, a timeline of the day in 40-tick buckets, who spends and on what, the biggest buys, the venue ads,
        and each venue's volume (GET /api/venues, all-time) next to its trades since payday (feed)."""
        tick = self.clock.get("tick") or 0
        payday = next((e.get("tick") for e in reversed(self.events) if e.get("type") == "announcement"
                       and "payday" in str((e.get("payload") or {}).get("text", "")).lower()), None)
        since = payday if payday is not None else max(0, tick - 240)
        opened = self._day_open()
        byprof = {p["team"]: p for p in prof}
        is_team = lambda x: bool(re.fullmatch(r"t\d{2}", str(x or "")))
        step = 40
        buckets = {}
        for tr in self.trades:
            t = tr["tick"] or 0
            if t < opened:
                continue
            b = opened + (t - opened) // step * step
            g = buckets.setdefault(b, {"tick": b, "team": 0, "dealer": 0, "volume": 0})
            g["team" if tr["kind"] == "team" else "dealer"] += 1
            g["volume"] += tr["price"] or 0
        win = [tr for tr in self.trades if (tr["tick"] or 0) >= since]
        acc, big = {}, []
        for tr in win:
            items = tr["items"]
            if not items or len({i.get("frm") for i in items}) > 1:
                continue
            frm, to, price = items[0].get("frm"), items[0].get("to"), tr["price"] or 0
            for tid, side in ((to, "buy"), (frm, "sell")):
                if not is_team(tid):
                    continue
                g = acc.setdefault(tid, {"team": tid, "name": self.name(tid), "rank": (byprof.get(tid) or {}).get("rank"),
                                         "us": tid == self.us, "spent": 0, "received": 0, "team_buys": 0, "team_sells": 0,
                                         "dealer_buys": 0, "dealer_sells": 0})
                kind = "team" if tr["kind"] == "team" else "dealer"
                if side == "buy":
                    g["spent"] += price
                    g[f"{kind}_buys"] += 1
                else:
                    g["received"] += price
                    g[f"{kind}_sells"] += 1
            big.append({"tick": tr["tick"], "kind": tr["kind"], "buyer": to, "seller": frm,
                        "text": f"{self._nm(to)} bought {', '.join(i.get('ref') or '?' for i in items)} "
                                f"({items[0].get('rarity') or items[0].get('kind') or ''}) from {self._nm(frm)}"
                                + (" on El Rastro" if tr["venue"] == "rastro" else f" on {tr['venue']}" if tr["venue"] else ""),
                        "price": price, "rarity": items[0].get("rarity"), "ours": self.us in tr["parties"]})
        big.sort(key=lambda r: -(r["price"] or 0))
        vown = {v.get("venue"): v.get("owner") for v in self.venues}
        ads = []
        for e in self.events:
            if e.get("type") != "venue.announcement" or (e.get("tick") or 0) < since:
                continue
            p = e.get("payload") or {}
            own = vown.get(p.get("venue"))
            ads.append({"tick": e.get("tick"), "venue": p.get("venue"), "name": p.get("name"), "owner": own,
                        "owner_name": self.name(own) if own else "?", "text": str(p.get("text") or "")[:240]})
        ads.reverse()
        since_v = collections.Counter(tr["venue"] for tr in win if tr["kind"] == "team")
        venues = []
        for v in self.venues:
            own = v.get("owner")
            venues.append({"venue": v.get("venue"), "name": v.get("name"), "owner": own,
                           "owner_name": "the house" if v.get("house") or v.get("venue") == "rastro" else self.name(own),
                           "rank": (byprof.get(own) or {}).get("rank"), "ours": own == self.us, "status": v.get("status"),
                           "fee_bps": v.get("fee_bps"), "mechanism": (v.get("rules") or {}).get("mechanism"),
                           "trades": v.get("trades") or 0, "volume": v.get("volume") or 0, "fees": v.get("fees") or 0,
                           "traders": v.get("traders") or 0, "since": since_v.get(v.get("venue"), 0),
                           "ads": sum(1 for a in ads if a["venue"] == v.get("venue"))})
        venues.sort(key=lambda r: -r["volume"])
        before = [tr for tr in self.trades if opened <= (tr["tick"] or 0) < since]
        rate = lambda xs, ticks: round(len(xs) / ticks * 20, 1) if ticks > 0 else None   # deals per 20 ticks (10 min)
        return {"payday": payday, "since": since, "now": tick, "opened": opened, "step": step,
                "timeline": [buckets[k] for k in sorted(buckets)],
                "summary": {"deals": len(win), "team": sum(1 for t in win if t["kind"] == "team"),
                            "dealer": sum(1 for t in win if t["kind"] != "team"),
                            "volume": sum(t["price"] or 0 for t in win),
                            "rares": sum(1 for t in win for i in t["items"] if i.get("rarity") in ("rare", "epic", "legendary")),
                            "rate_now": rate(win, tick - since), "rate_before": rate(before, since - opened)},
                "spenders": sorted(acc.values(), key=lambda g: -(g["spent"] + g["received"])),
                "big": big[:12], "ads": ads[:25], "venues": venues}

    def strategies(self, prof):
        """What each team is doing now (its deals and moves in the last game hour) and what lifted it today: its three
        biggest score jumps between leaderboard snapshots, each with that team's own deals in the window. A jump with no
        deal of its own came from duels, ladder re-grading or the field (the board is relative)."""
        tick = self.clock.get("tick") or 0
        tps = self.clock.get("tick_seconds") or 30
        hour = int(3600 / tps)
        recent = tick - hour
        opened = self._day_open()
        vown = {v.get("venue"): v.get("owner") for v in self.venues}
        sessions = []
        for e in self.events:
            p = e.get("payload") or {}
            if e.get("type") == "duels.scheduled":
                sessions.append([p.get("session"), p.get("name"), e.get("tick"), None])
            elif e.get("type") == "duels.finished":
                for s in sessions:
                    if s[0] == p.get("session"):
                        s[3] = e.get("tick")
        act = collections.defaultdict(lambda: collections.Counter())
        sets_bought = collections.defaultdict(collections.Counter)
        dealers = collections.defaultdict(set)
        for tr in self.trades:
            if (tr["tick"] or 0) < recent:
                continue
            items = tr["items"]
            if not items:
                continue
            if tr["kind"] == "team" and tr["venue"] in vown and vown[tr["venue"]] not in tr["parties"]:
                act[vown[tr["venue"]]]["on_stall"] += 1
            swap = len({i.get("frm") for i in items}) > 1
            for tid in tr["parties"]:
                c = act[tid]
                if swap:
                    c["swaps"] += 1
                elif items[0].get("to") == tid:
                    c["team_buys" if tr["kind"] == "team" else "dealer_buys"] += 1
                    sets_bought[tid].update(set_of(i.get("ref")) for i in items if i.get("ref"))
                else:
                    c["team_sells" if tr["kind"] == "team" else "dealer_sells"] += 1
                if tr["kind"] != "team":
                    dealers[tid].add(self._nm(tr["dealer"]))
        for e in self.events:
            if (e.get("tick") or 0) < recent:
                continue
            p, ty = e.get("payload") or {}, e.get("type")
            if ty == "pack.opened":
                act[p.get("team")]["packs"] += 1
            elif ty == "venue.announcement" and vown.get(p.get("venue")):
                act[vown[p.get("venue")]]["ads"] += 1
            elif ty == "taller.crafted":
                act[p.get("team")]["crafts"] += 1
            elif ty == "offer.listed":
                act[e.get("actor") or (p.get("offer") or {}).get("maker")]["listings"] += 1
            elif ty == "thread.opened" and p.get("kind") == "persona":
                act[p.get("team")]["dealer_talks"] += 1

        snaps = [h for h in self.lb_hist if h["tick"] >= opened] or self.lb_hist
        out = []
        for p in prof:
            tid, c = p["team"], act.get(p["team"], collections.Counter())
            now_parts = []
            if c["dealer_buys"] + c["dealer_sells"] >= 2:
                now_parts.append(f"dealer deals: {c['dealer_sells']} sells, {c['dealer_buys']} buys"
                                 f" ({', '.join(sorted(dealers[tid]))})")
            if c["on_stall"] or c["ads"] >= 2:
                now_parts.append(f"market-making: {c['on_stall']} trade(s) by others on its stall, {c['ads']} ad(s)")
            if c["team_buys"] >= 1:
                sb = ", ".join(s for s, _ in sets_bought[tid].most_common(2))
                now_parts.append(f"buying from teams: {c['team_buys']}" + (f" ({sb})" if sb else ""))
            if c["team_sells"] >= 1:
                now_parts.append(f"selling to teams: {c['team_sells']}")
            if c["swaps"]:
                now_parts.append(f"swaps: {c['swaps']}")
            if c["packs"]:
                now_parts.append(f"opened {c['packs']} pack(s)")
            if c["crafts"]:
                now_parts.append(f"{c['crafts']} Workshop craft(s)")
            if not now_parts:
                now_parts.append(f"no deal in the last hour ({c['listings']} listings, {c['dealer_talks']} dealer talks)"
                                 if c["listings"] or c["dealer_talks"] else "quiet in the last hour")
            moves = []
            for a, b in zip(snaps, snaps[1:]):
                ta, tb = a["teams"].get(tid), b["teams"].get(tid)
                if not ta or not tb or ta.get("score") is None or tb.get("score") is None:
                    continue
                dlt = round(tb["score"] - ta["score"], 2)
                if dlt < 0.5:
                    continue
                lo, hi = a["tick"] - 10, b["tick"]
                own = [self._deal_text(tr, tid) for tr in self.trades
                       if lo < (tr["tick"] or 0) <= hi and (tid in tr["parties"]
                       or (tr["kind"] == "team" and vown.get(tr["venue"]) == tid))]
                sess = [s[1] for s in sessions if s[2] is not None and s[2] <= hi and (s[3] is None or s[3] >= lo)]
                dn = round((tb.get("negotiating") or 0) - (ta.get("negotiating") or 0), 2)
                dm = round((tb.get("market") or 0) - (ta.get("market") or 0), 2)
                stall = any(tr["kind"] == "team" and vown.get(tr["venue"]) == tid and lo < (tr["tick"] or 0) <= hi
                            for tr in self.trades)
                if abs(dm) > abs(dn):
                    head = (f"market {dm:+.2f}: value created on its stall" if stall
                            else f"market {dm:+.2f}: a Market Test scored or value created was re-graded")
                else:
                    head = (f"negotiating {dn:+.2f}" + (f" during {', '.join(sess)}" if sess else ""))
                why = [head] + (own[:3] or ["no deal of its own in the window" + (" (duels)" if sess and abs(dn) >= abs(dm)
                                                                                  else " (the board is relative)")])
                if ta.get("pages") is not None and tb.get("pages") is not None and ta["pages"] < tb["pages"]:
                    why.insert(1, f"completed a page ({ta['pages']} → {tb['pages']})")
                moves.append({"from": a["tick"], "to": b["tick"], "delta": dlt, "neg": dn, "market": dm, "why": why})
            moves.sort(key=lambda m: -m["delta"])
            series = [h["teams"].get(tid, {}).get("score") for h in snaps]
            stride = max(1, len(series) // 60)
            out.append({"team": tid, "name": p["name"], "rank": p["rank"], "us": p["us"], "score": p["score"],
                        "delta": p.get("delta"), "negotiating": p.get("negotiating"), "market": p.get("market"),
                        "pages": p.get("pages"), "level": p.get("level"), "collects": p.get("wants") or [],
                        "dumps": p.get("dumps") or [], "stall": next((v for v, o in vown.items() if o == tid), None),
                        "now": now_parts, "activity": dict(c), "moves": moves[:3], "series": series[::stride]})
        return {"window_ticks": hour, "teams": out}

    def tape(self, n=40):
        out = []
        for tr in reversed(self.trades[-n:]):
            i = tr["items"][0] if tr["items"] else {}
            out.append({"tick": tr["tick"], "kind": tr["kind"], "venue": tr["venue"] or tr["dealer"],
                        "ref": ", ".join(x.get("ref", "?") for x in tr["items"]), "rarity": i.get("rarity"),
                        "buyer": self.name(i.get("to")), "seller": self.name(i.get("frm")), "price": tr["price"],
                        "ours": self.us in tr["parties"]})
        return out

    def holders(self):
        """Who holds the cards we want (from trades only: starting cards and pack pulls are invisible)."""
        wanted = {r for r in self.cards if set_of(r) in {s for s, a in self.aff.items() if a >= 1.1}}
        wanted |= {r for o in self.board if self.maker.get(o.get("id")) == self.us for r in refs_of(o.get("want"))}
        rows = collections.defaultdict(list)
        for aid, h in self.holder.items():
            if h["ref"] in wanted and h["team"] and h["team"] != self.us and h["team"].startswith("t"):
                rows[h["ref"]].append({"team": h["team"], "name": self.name(h["team"]), "tick": h["tick"],
                                       "price": h["price"], "from": self.name(h["frm"])})
        out = []
        for ref in sorted(rows, key=lambda r: -(self.value_more(r) or 0)):
            c = self.cards.get(ref) or {}
            out.append({"ref": ref, "card": c.get("name"), "rarity": c.get("rarity"), "value": self.value_more(ref),
                        "we_hold": self.held.get(ref, 0), "holders": rows[ref]})
        return out

    def abuela(self):
        per = collections.defaultdict(list)
        for th in self.threads.values():
            dp = th["dealer_prices"]
            if len(dp) < 1 or not dp[0]:
                continue
            first, lastp = dp[0], dp[-1]
            move = (first - lastp) / first if th["side"] == "team buys" else (lastp - first) / first
            per[(th["team"], th["dealer"])].append({"move": move, "msgs": th["msgs"], "side": th["side"]})
        rows = []
        for (tid, dealer), xs in per.items():
            rows.append({"team": tid, "name": self.name(tid), "dealer": dealer, "threads": len(xs),
                         "avg_move": round(100 * statistics.mean(x["move"] for x in xs), 1),
                         "best_move": round(100 * max(x["move"] for x in xs), 1),
                         "avg_msgs": round(statistics.mean(x["msgs"] for x in xs), 1), "us": tid == self.us})
        rows.sort(key=lambda r: -r["avg_move"])
        return rows

    def minutes_per_hour(self):
        """Wall minutes per game hour: ticks per game hour, measured on the feed's last 20 ticks, × the tick length.
        Friday (60 s ticks, 60 per hour) and Saturday (30 s, 120 per hour) both give 60: game hour = wall hour."""
        secs = self.clock.get("tick_seconds") or 60
        pts = [(e["tick"], e["t"]) for e in self.events
               if isinstance(e.get("t"), (int, float)) and isinstance(e.get("tick"), int)]
        if pts:
            win = [p for p in pts if p[0] >= pts[-1][0] - 20]
            (k0, t0), (k1, t1) = win[0], win[-1]
            if k1 - k0 >= 5 and t1 > t0:
                return (k1 - k0) / (t1 - t0) * secs / 60
        return 60

    def schedule(self):
        t_now, per_hour = self.clock.get("t_hours") or 0, self.minutes_per_hour()
        rows = []
        for e in (self.sched.get("upcoming") or [])[:10]:
            rows.append({"at": e.get("at_hours"), "eta_min": round((e.get("at_hours", 0) - t_now) * per_hour),
                         "action": e.get("action"), "note": e.get("note", ""),
                         "params": json.dumps(e.get("params") or {}, ensure_ascii=False)[:160]})
        return rows

    # -------------------------------------------------------------------------------------- insights
    def insights(self, prof, market):
        out = []

        def add(kind, text):
            out.append({"kind": kind, "text": text})

        byid = {p["team"]: p for p in prof}
        us = byid.get(self.us)
        if prof and us:
            lead = prof[0]
            if lead["team"] != self.us:
                add("info", f"We are #{us['rank']} with {us['score']:.1f}; {lead['name']} leads with {lead['score']:.1f} "
                            f"({lead['score'] - us['score']:+.1f}).")
            above = [p for p in prof if p["rank"] == us["rank"] - 1]
            if above:
                add("info", f"Next rung: {above[0]['name']} at {above[0]['score']:.1f} "
                            f"({above[0]['score'] - us['score']:.1f} above us).")
        movers = sorted([p for p in prof if p["delta"]], key=lambda p: -p["delta"])[:3]
        for p in movers:
            if p["delta"] >= 1:
                add("mover", f"{p['name']} {p['delta']:+.1f} in the last ~{RECENT} ticks"
                             + (f"; biggest team trade: {p['biggest']}" if p["biggest"] else "") + ".")
        sells = [r for r in market if r["side"] == "bid" and (r["edge"] or 0) >= EDGE]
        for r in sells[:5]:
            block = self.feeding_block(byid[r["team"]], us["score"]) if us and r["team"] in byid else None
            rule = ("" if not block else
                    f" Feeding rule: {r['name']} is in the top {TOP_NEVER}: only if the card can't close their page "
                    f"and our gain clearly beats theirs." if block.startswith("top") else
                    f" Feeding rule: {r['name']} is {block}: only if the card can't close their page.")
            add("sell", f"SELL: {r['name']} bids {r['price']} P for {r['ref']} (offer #{r['id']}); "
                        f"our copy is worth {r['value']} → +{r['edge']} after the fee if we accept." + rule)
        buys = [r for r in market if r["side"] == "ask" and (r["edge"] or 0) >= EDGE]
        for r in buys[:5]:
            add("buy", f"BUY: {r['name']} asks {r['price']} P for {r['ref']} (offer #{r['id']}); "
                       f"worth ~{r['value']} to us → +{r['edge']} after the fee.")
        ours = {r["ref"]: r for r in market if r["ours"] and r["side"] == "bid" and r["ref"]}
        rivals = collections.defaultdict(dict)
        for r in market:
            if r["side"] == "bid" and not r["ours"] and r["ref"] in ours:
                best = rivals[r["ref"]].get(r["name"])
                if not best or r["price"] > best["price"]:
                    rivals[r["ref"]][r["name"]] = r
        for ref, by in sorted(rivals.items(), key=lambda kv: -max(x["price"] for x in kv[1].values())):
            mine = ours[ref]
            xs = sorted(by.values(), key=lambda x: -x["price"])
            top = xs[0]
            who = ", ".join(f"{x['name']} {x['price']}" for x in xs)
            if top["price"] >= mine["price"]:
                add("rival", f"OUTBID on {ref}: {who} P vs our {mine['price']} (#{mine['id']}). Raise, or drop it.")
            else:
                add("rival", f"We lead on {ref} at {mine['price']} P (#{mine['id']}); also bidding: {who}.")
        rivals_by_set = collections.defaultdict(list)
        for p in prof:
            if p["us"]:
                continue
            for s in p["wants"]:
                if self.aff.get(s, 0) >= 1.1:
                    rivals_by_set[s].append(f"{p['name']} (#{p['rank']})")
        for s, who in rivals_by_set.items():
            add("rival", f"{len(who)} teams also collect {s} (worth {self.aff.get(s)}× to us): {', '.join(who)}. "
                         f"Expect competition for {s} cards; don't sell them {s}.")
        buyers = collections.defaultdict(list)
        for p in prof:
            for kind, text in p["relation"]:
                if kind == "buyer":
                    for s in p["wants"]:
                        if self.aff.get(s, 9) < 1.0:
                            buyers[s].append(f"{p['name']} (#{p['rank']})")
        for s, who in buyers.items():
            add("buyer", f"Who buys {s} (worth {self.aff.get(s)}× to us): {', '.join(who)}. Prefer teams below us.")
        ab = [r for r in self.abuela() if r["dealer"] == "abuela" and r["threads"] >= 2]
        if ab:
            best = ab[0]
            mine = next((r for r in ab if r["us"]), None)
            add("info", f"Best Abuela haggler: {best['name']}, {best['avg_move']}% off her first price on average"
                        + (f"; we get {mine['avg_move']}%." if mine else "."))
        if self.c.feed_gap:
            add("warn", "The feed had a gap (the dashboard was off for a while): counts before it are incomplete.")
        if self.c.hub.get("gaps"):
            add("warn", f"The hub recorded {self.c.hub['gaps']} feed gap(s) (both collectors were away): "
                        f"history there is incomplete.")
        return out

    # -------------------------------------------------------------------------------------- duels and conversations
    def duel_view(self):
        """Our duels (live and finished, from GET /api/duels with the team key): transcript, price paths, lessons.

        `result` is our surplus in P (price vs our limit) times (1 − decay) ** rounds; the rival's limit stays secret,
        so its offers only bound it: a rival buyer's value is at least its best bid, a seller's cost at most its best ask."""
        seen, out = set(), []
        for d in list(self.duels) + list(reversed(self.duels_done)):
            did = d.get("duel")
            if did in seen:
                continue
            seen.add(did)
            role, limit = d.get("role"), d.get("your_limit")
            msgs = [{"tick": m.get("tick"), "us": m.get("from") == "you", "who": "us" if m.get("from") == "you" else m.get("from"),
                     "text": (m.get("text") or "")[:500], "price": m.get("price"), "days": m.get("days")}
                    for m in (d.get("messages") or [])]
            ours = [m for m in msgs if m["us"] and m["price"] is not None]
            theirs = [m for m in msgs if not m["us"] and m["price"] is not None]
            better = (lambda a, b: a < b) if role == "buyer" else (lambda a, b: a > b)  # better for us
            rival_best = None
            for m in theirs:
                if rival_best is None or better(m["price"], rival_best):
                    rival_best = m["price"]
            within = rival_best is not None and limit is not None and (rival_best <= limit if role == "buyer" else rival_best >= limit)
            missed = d.get("status") == "no_deal" and within
            gain_missed = (limit - rival_best if role == "buyer" else rival_best - limit) if missed else None
            conc_us = abs(ours[-1]["price"] - ours[0]["price"]) if len(ours) > 1 else 0
            conc_them = abs(theirs[-1]["price"] - theirs[0]["price"]) if len(theirs) > 1 else 0
            out.append({"duel": did, "status": d.get("status"), "role": role, "item": d.get("item"), "rival": d.get("rival"),
                        "session": d.get("session"), "limit": limit, "price": d.get("price"), "rounds": d.get("rounds"),
                        "decay": d.get("decay_per_round"), "result": d.get("result"), "deadline": d.get("deadline_tick"),
                        "messages": msgs,
                        # a rival that never wrote but accepted our offer did have an agent: only no-deal silence counts
                        "rival_silent": not any(not m["us"] for m in msgs) and d.get("status") != "deal",
                        "rival_best": rival_best, "missed": missed, "gain_missed": gain_missed,
                        "our_first": ours[0]["price"] if ours else None, "their_first": theirs[0]["price"] if theirs else None,
                        "our_now": (d.get("your_offer") or {}).get("price"), "their_now": (d.get("rival_offer") or {}).get("price"),
                        "our_days": (d.get("your_offer") or {}).get("days"), "their_days": (d.get("rival_offer") or {}).get("days"),
                        "days_weight": d.get("your_days_weight"), "issues": d.get("issues"),
                        "conc_us": conc_us, "conc_them": conc_them,
                        "surplus": (limit - d["price"] if role == "buyer" else d["price"] - limit) if d.get("price") is not None and limit is not None else None})
        out.sort(key=lambda x: (x["status"] != "live", -(x["duel"] or 0)))
        decided = [x for x in out if x["status"] in ("deal", "no_deal")]
        talked = [x for x in decided if not x["rival_silent"]]
        deals = [x for x in decided if x["status"] == "deal"]
        closed = collections.Counter(p.get("status") for p in self.duel_closed)
        summary = {"live": sum(1 for x in out if x["status"] == "live"), "decided": len(decided), "deals": len(deals),
                   "silent": sum(1 for x in decided if x["rival_silent"]), "talked": len(talked),
                   "deal_rate_talked": round(len(deals) / len(talked), 2) if talked else None,
                   "missed": [x["duel"] for x in out if x["missed"]],
                   "missed_gain": sum(x["gain_missed"] or 0 for x in out if x["missed"]),
                   "points": round(sum(x["result"] or 0 for x in deals), 1),
                   "surplus": sum(x["surplus"] or 0 for x in deals),
                   "avg_rounds": round(statistics.mean(x["rounds"] or 0 for x in deals), 1) if deals else None,
                   "conc_us": sum(x["conc_us"] for x in deals), "conc_them": sum(x["conc_them"] for x in deals),
                   "field_deals": closed.get("deal", 0), "field_no_deals": closed.get("no_deal", 0)}
        lessons = []
        for x in out:
            if x["missed"]:
                lessons.append(f"Duel {x['duel']} ({x['role']}, limit {x['limit']}): {x['rival']} offered {x['rival_best']}, "
                               f"inside our limit, and the duel ended with no deal: +{x['gain_missed']} P left on the table. "
                               f"Accept an in-limit offer before the deadline.")
        if summary["silent"]:
            lessons.append(f"{summary['silent']} of {summary['decided']} finished duels had a silent rival (no agent running): "
                           f"no deal was possible there. Deal rate when the rival talked: "
                           f"{summary['deal_rate_talked'] if summary['deal_rate_talked'] is not None else '—'}.")
        if deals and summary["conc_us"] > summary["conc_them"]:
            lessons.append(f"In our deals we conceded {summary['conc_us']} P in total and the rivals {summary['conc_them']} P: "
                           f"we move more than they do.")
        elif deals:
            lessons.append(f"In our deals the rivals conceded {summary['conc_them']} P and we {summary['conc_us']} P: good.")
        if summary["field_deals"] + summary["field_no_deals"]:
            n = summary["field_deals"] + summary["field_no_deals"]
            lessons.append(f"Whole field (public feed): {summary['field_deals']} deals out of {n} closed duels "
                           f"({round(100 * summary['field_deals'] / n)}%).")
        return {"duels": out, "summary": summary, "lessons": lessons}

    def duel_monitor(self, view):
        """The current duel session live (Duels I/II/III), from data the dashboard already reads: no extra request.

        Session and field progress from the public feed (`duels.scheduled`, `duel.closed`: no team ids), our duels
        from GET /api/duels, `duel_points` from /api/me, negotiating per team from the leaderboard (it doesn't split
        duels out, so that column also moves with dealer and team trades). result = surplus × (1 − decay) ** rounds,
        so accepting the rival's standing offer now would score (limit − price, or price − limit) × (1 − decay) ** rounds."""
        sched = [e for e in self.duel_events if e.get("type") == "duels.scheduled"]
        if not sched:
            return None
        ev = sched[-1]
        sp, start, tick = ev.get("payload") or {}, ev.get("tick") or 0, self.clock.get("tick") or 0
        sess = sp.get("session")
        finished = any((e.get("payload") or {}).get("session") == sess for e in self.duel_events
                       if e.get("type") == "duels.finished")
        n_teams = len(self.lb_hist[-1]["teams"]) if self.lb_hist else 18
        total = sp.get("duels") or 0
        ours_total = round(total * 2 / n_teams) if n_teams else None  # each duel has two teams in it
        field = [p for p in self.duel_closed if p.get("session") == sess]
        field_deals = sum(1 for p in field if p.get("status") == "deal")
        mine = [x for x in view["duels"] if x.get("session") == sess]
        live = [x for x in mine if x["status"] == "live"]
        done = [x for x in mine if x["status"] in ("deal", "no_deal")]
        deals = [x for x in done if x["status"] == "deal"]
        talked = [x for x in done if not x["rival_silent"]]

        alerts, rows = [], []
        for x in sorted(live, key=lambda r: r["deadline"] or 0):
            role, limit, decay, rounds = x["role"], x["limit"], x["decay"] or 0, x["rounds"] or 0
            left = (x["deadline"] - tick) if x["deadline"] is not None else None
            pie = (1 - decay) ** rounds
            buyer = role == "buyer"
            their, our = x["their_now"], x["our_now"]
            in_limit = their is not None and limit is not None and (their <= limit if buyer else their >= limit)
            accept_now = round(((limit - their) if buyer else (their - limit)) * pie, 1) if in_limit else None
            ours_out = our is not None and limit is not None and (our > limit if buyer else our < limit)
            msgs = x["messages"]
            last_them = max((m["tick"] for m in msgs if not m["us"]), default=None)
            last_us = max((m["tick"] for m in msgs if m["us"]), default=None)
            we_quiet = last_them is not None and (last_us is None or last_us < last_them) and tick - last_them >= 4
            flags = []
            name = f"Duel {x['duel']} ({role}, {x['rival']})"
            if ours_out:
                flags.append("our offer outside our limit")
                alerts.append({"sev": "critical", "duel": x["duel"], "text": f"{name}: our standing offer {our} is outside our limit {limit}: a deal there loses points. Tell Aleks."})
            if in_limit and left is not None and left <= 2:
                flags.append("accept before the deadline")
                alerts.append({"sev": "critical", "duel": x["duel"], "text": f"{name}: the rival's {their} is inside our limit {limit} with {left} tick(s) left: accepting now scores +{accept_now} P; no deal scores 0 (duel 181)."})
            elif in_limit:
                flags.append("acceptable now")
                alerts.append({"sev": "watch", "duel": x["duel"], "text": f"{name}: the rival's {their} is inside our limit {limit}: accepting now would score +{accept_now} P; haggling on costs {round(decay * 100)}% of the pie per round."})
            if we_quiet:
                flags.append("we are silent")
                alerts.append({"sev": "critical" if left is not None and left <= 4 else "watch", "duel": x["duel"],
                               "text": f"{name}: the rival spoke at tick {last_them} and we haven't answered for {tick - last_them} ticks: is the duelist up? (Aleks)"})
            began = (x["deadline"] - sp["duel_ticks"]) if x["deadline"] is not None and sp.get("duel_ticks") else start
            if not any(not m["us"] for m in msgs) and tick - began >= 6:
                flags.append("rival silent")
            if rounds >= 6:
                flags.append(f"{rounds} rounds")
            rows.append({"duel": x["duel"], "rival": x["rival"], "role": role, "item": x["item"], "limit": limit,
                         "our_now": our, "their_now": their, "our_days": x["our_days"], "their_days": x["their_days"],
                         "days_weight": x["days_weight"],
                         "gap": abs(our - their) if our is not None and their is not None else None,
                         "rounds": rounds, "pie": round(100 * pie), "left": left, "accept_now": accept_now,
                         "flags": flags, "in_limit": in_limit})
        sev_order = {"critical": 0, "watch": 1}
        alerts.sort(key=lambda a: sev_order.get(a["sev"], 2))

        fin_rows = []
        for x in done:
            lost = round(x["surplus"] - x["result"], 1) if x["surplus"] is not None and x["result"] is not None else None
            fin_rows.append({"duel": x["duel"], "status": x["status"], "role": x["role"], "rival": x["rival"], "item": x["item"],
                             "limit": x["limit"], "price": x["price"], "surplus": x["surplus"], "rounds": x["rounds"],
                             "result": x["result"], "lost": lost, "missed": x["missed"], "gain_missed": x["gain_missed"],
                             "silent": x["rival_silent"]})
        for x in done:
            if x["missed"]:
                alerts.append({"sev": "missed", "duel": x["duel"], "text": f"Duel {x['duel']} ({x['role']}, {x['rival']}): the rival offered {x['rival_best']}, inside our limit {x['limit']}, and it ended with no deal: +{x['gain_missed']} P left on the table."})

        pts = [(r["tick"], r.get("duel_points")) for r in self.me_hist if (r.get("tick") or 0) >= start - 2]
        rate = len(done) / (tick - start) if tick > start and done else None
        remaining = (ours_total - len(done)) if ours_total else None
        eta_min = round(remaining / rate * (self.clock.get("tick_seconds") or 30) / 60) if rate and remaining is not None and not finished else None

        neg = []
        if self.lb_hist:  # snapshots sorted by tick
            base_snap = next((h for h in reversed(self.lb_hist) if h["tick"] <= start), self.lb_hist[0])
            base, a, b = base_snap["tick"], base_snap["teams"], self.lb_hist[-1]["teams"]
            for tid, v in b.items():
                if tid in a and v.get("negotiating") is not None and a[tid].get("negotiating") is not None:
                    neg.append({"team": tid, "name": v.get("name"), "us": tid == self.us, "from": a[tid]["negotiating"],
                                "now": v["negotiating"], "delta": round(v["negotiating"] - a[tid]["negotiating"], 2)})
            neg.sort(key=lambda r: -r["delta"])
            neg_span = [base, self.lb_hist[-1]["tick"]]
        else:
            neg_span = None

        return {"session": sess, "name": sp.get("name"), "decay": sp.get("decay"), "duel_ticks": sp.get("duel_ticks"),
                "rounds": sp.get("rounds"), "start": start, "tick": tick, "finished": finished,
                "field_total": total, "field_closed": len(field), "field_deals": field_deals,
                "ours_total": ours_total, "ours_done": len(done), "ours_live": len(live), "deals": len(deals),
                "talked": len(talked), "silent": sum(1 for x in done if x["rival_silent"]),
                "points": round(sum(x["result"] or 0 for x in deals), 1),
                "surplus": sum(x["surplus"] or 0 for x in deals),
                "decay_lost": round(sum(r["lost"] or 0 for r in fin_rows if r["status"] == "deal"), 1),
                "missed_gain": sum(x["gain_missed"] or 0 for x in done if x["missed"]),
                "avg_rounds": round(statistics.mean(x["rounds"] or 0 for x in deals), 1) if deals else None,
                "duel_points": pts[-1][1] if pts else None, "duel_points_start": pts[0][1] if pts else None,
                "duel_points_series": [p[1] for p in pts], "eta_min": eta_min,
                "alerts": alerts, "live": rows, "done": sorted(fin_rows, key=lambda r: -(r["duel"] or 0)),
                "neg": neg, "neg_span": neg_span, "sessions": self.duel_sessions(view, sess, tick)}

    def duel_sessions(self, view, current, tick):
        """Average points per duel, session by session: our result in P per finished duel (a no-deal counts 0) and per
        deal, and the `duel_points` /api/me gained over the session per finished duel (what the board sees)."""
        info = {}
        for e in self.duel_events:
            p = e.get("payload") or {}
            if e.get("type") == "duels.scheduled":
                info[p.get("session")] = {"name": p.get("name"), "start": e.get("tick"), "end": None, "decay": p.get("decay")}
            elif e.get("type") == "duels.finished" and p.get("session") in info:
                info[p["session"]]["end"] = e.get("tick")

        def dp_at(t):
            v = None
            for r in self.me_hist:   # sorted by tick
                if (r.get("tick") or 0) > t:
                    break
                if r.get("duel_points") is not None:
                    v = r["duel_points"]
            return v

        out = []
        for sid, s in sorted(info.items(), key=lambda kv: kv[1]["start"] or 0):
            done = [x for x in view["duels"] if x.get("session") == sid and x["status"] in ("deal", "no_deal")]
            if not done and sid != current:
                continue
            deals = [x for x in done if x["status"] == "deal"]
            res = round(sum(x["result"] or 0 for x in deals), 1)
            a, b = dp_at((s["start"] or 0) - 1), dp_at(s["end"] if s["end"] else tick)
            dp = round(b - a, 2) if a is not None and b is not None else None
            n = len(done)
            out.append({"session": sid, "name": s["name"], "current": sid == current, "finished": s["end"] is not None,
                        "decay": s["decay"], "done": n, "deals": len(deals), "result": res,
                        "per_duel": round(res / n, 1) if n else None,
                        "per_deal": round(res / len(deals), 1) if deals else None,
                        "dp": dp, "dp_per_duel": round(dp / n, 3) if dp is not None and n else None,
                        "rounds": round(statistics.mean(x["rounds"] or 0 for x in deals), 1) if deals else None})
        return out

    def conversations(self, n=60):
        """Public dealer conversations (every team's haggling, from the feed), newest first."""
        out = []
        for tid, th in self.threads.items():
            if not th["log"]:
                continue
            dp, tp = th["dealer_prices"], th["team_prices"]
            out.append({"thread": tid, "team": th["team"], "name": self.name(th["team"]), "dealer": th["dealer"],
                        "dealer_name": self.name(th["dealer"]), "side": th["side"], "item": th["item"],
                        "first": dp[0] if dp else None, "last": dp[-1] if dp else None, "team_first": tp[0] if tp else None,
                        "msgs": th["msgs"], "start": th["log"][0]["tick"], "end": th["log"][-1]["tick"],
                        "us": th["team"] == self.us, "log": th["log"][-40:]})
        out.sort(key=lambda x: -(x["end"] or 0))
        return out[:n]

    # -------------------------------------------------------------------------------------- why our score moved
    def our_trade_text(self, tr):
        i = tr["items"][0] if tr["items"] else {}
        refs = ", ".join(x.get("ref", "?") for x in tr["items"]) or "cash"
        if i.get("to") == self.us:
            return f"bought {refs} from {self.name(i.get('frm'))} for {tr['price']} P"
        return f"sold {refs} to {self.name(i.get('to'))} for {tr['price']} P"

    def story(self):
        """Per leaderboard interval: our score change = field drift (what idle teams did) + our own doing.

        The score is relative: teams that make no trade still move together when others gain. The median change
        of the teams that made no trade in the interval estimates that drift; the rest of our change is ours."""
        def neg_at(t):
            xs = [r for r in self.me_hist if r.get("tick") is not None and r["tick"] <= t and r.get("neg_points") is not None]
            return xs[-1]["neg_points"] if xs else None

        def rank_in(snap):
            order = sorted(snap["teams"], key=lambda k: -(snap["teams"][k].get("score") or 0))
            return order.index(self.us) + 1 if self.us in order else None

        def change(a, b, tid, key):
            x, y = a["teams"].get(tid, {}).get(key), b["teams"].get(tid, {}).get(key)
            return y - x if x is not None and y is not None else None

        venues = {v.get("venue") for v in self.venues if v.get("owner") == self.us}
        out = []
        for a, b in zip(self.lb_hist, self.lb_hist[1:]):
            ta, tb = a["tick"], b["tick"]
            active, ours, hosted = set(), [], []
            for tr in self.trades:
                if ta < (tr["tick"] or 0) <= tb:
                    active.update(tr["parties"])
                    if self.us in tr["parties"]:
                        ours.append(tr)
                    elif tr.get("venue") in venues:
                        hosted.append(tr)  # other teams trading on our venue: the value they create scores market for us
            idle_ids = [k for k in b["teams"] if k in a["teams"] and k not in active and k != self.us]
            idle = [d for k in idle_ids if (d := change(a, b, k, "score")) is not None]
            usa, usb = a["teams"].get(self.us, {}).get("score"), b["teams"].get(self.us, {}).get("score")
            if usa is None or usb is None:
                continue
            drift = median(idle) if idle else 0.0
            delta = usb - usa
            # the same split for each part of the score: what the idle teams got is drift, the rest is ours
            parts = {}
            for key in ("negotiating", "market"):
                d_us = change(a, b, self.us, key)
                d_idle = [d for k in idle_ids if (d := change(a, b, k, key)) is not None]
                parts[key] = round(d_us - (median(d_idle) if d_idle else 0.0), 2) if d_us is not None else None
            pa, pb = a["teams"].get(self.us, {}).get("pages"), b["teams"].get(self.us, {}).get("pages")
            pages_up = pb - pa if pa is not None and pb is not None else None
            na, nb = neg_at(ta), neg_at(tb)
            neg_delta = round(nb - na, 1) if na is not None and nb is not None else None
            causes = [self.our_trade_text(t) for t in ours]
            if pages_up:
                causes.append(f"page complete: {pb} complete page{'s' if pb != 1 else ''} now (the page bonus)")
            elif pages_up is None and (neg_delta or 0) >= 40:
                causes.append(f"likely a page complete (neg_points {neg_delta:+g})")
            causes += [f"on our venue {t.get('venue')}: {self.trade_text(t)} (value created on our venue scores "
                       f"market for us)" for t in hosted]
            if parts["market"] is not None and abs(parts["market"]) >= 0.5 and not hosted:
                causes.append(f"market {parts['market']:+.2f} vs the field (a Market Test or trades on our venue)")
            out.append({"from": ta, "to": tb, "score": usb, "rank_from": rank_in(a), "rank": rank_in(b),
                        "delta": round(delta, 2), "drift": round(drift, 2), "ours": round(delta - drift, 2),
                        "ours_neg": parts["negotiating"], "ours_market": parts["market"], "pages_up": pages_up,
                        "neg_points": nb, "neg_delta": neg_delta,
                        "trades": [self.our_trade_text(t) for t in ours], "causes": causes, "idle_teams": len(idle)})
        return out

    def directive_lines(self):
        """The team's decisions as dated lines (`- HH:MM · text` under `## Sat …` headings), newest first: today's from
        intel/directives.md as on GitHub, then Friday's archive."""
        fri = ROOT / "archive" / "fri" / "directives-fri.md"
        out = []
        for text, day in ((self.c.directives, "Sat"), (fri.read_text(encoding="utf-8") if fri.exists() else "", "Fri")):
            for ln in text.splitlines():
                if m := re.match(r"##\s+(\w{3})\b", ln):
                    day = m.group(1)
                elif m := re.match(r"-\s+(\d{1,2}:\d{2})\s+·\s+(.*)", ln):
                    t = re.sub(r"\*\*|`", "", m.group(2)).strip()
                    out.append({"day": day, "time": m.group(1), "text": t, "guardrail": "GUARDRAIL" in t})
        return out

    def moves(self, story):
        """The intervals that moved us most (our part after drift ≥ 1.5, or two places), newest first, each with its
        causes and the team decisions that name the same card or venue: the why behind the move."""
        lines = self.directive_lines()
        out = []
        for x in story:
            places = (x["rank_from"] - x["rank"]) if x.get("rank_from") and x.get("rank") else 0
            if abs(x["ours"]) < 1.5 and abs(places) < 2:
                continue
            keys = {k for c in x["causes"] for k in re.findall(r"\b(?:[A-Z]{3}-\d{2}|v\d{2})\b", c)}
            why = [ln for ln in lines if any(re.search(rf"\b{re.escape(k)}\b", ln["text"]) for k in keys)][:2]
            out.append({**{k: x.get(k) for k in ("from", "to", "rank_from", "rank", "score", "delta", "ours",
                                                 "ours_neg", "ours_market", "causes")}, "why": why})
        return out[::-1][:8]

    def decisions(self):
        """Today's newest team decisions (intel/directives.md)."""
        lines = self.directive_lines()
        return [ln for ln in lines if lines and ln["day"] == lines[0]["day"]][:10]

    # -------------------------------------------------------------------------------------- intel/teams.md
    def team_prices(self, tid, market):
        """Median price per rarity a team traded at with other teams, plus its open bids."""
        by = collections.defaultdict(list)
        for tr in self.trades:
            if tr["kind"] == "team" and tid in tr["parties"] and len(tr["items"]) == 1:
                i = tr["items"][0]
                by[i.get("rarity") or self.rarity(i.get("ref"))].append(tr["price"])
        for r in market:
            if r["team"] == tid and r["side"] == "bid" and r["rarity"]:
                by[r["rarity"]].append(r["price"])
        return {k: median(v) for k, v in by.items() if v}

    def teams_md(self):
        """Rival profiles for the analysts (they read the first 6000 characters, so keep it tight)."""
        self.scan()
        prof = self.profiles()
        market = self.market()
        byid = {p["team"]: p for p in prof}
        us = byid.get(self.us, {})
        our_rank = us.get("rank", 99)
        us_score = us.get("score") or 0
        first_tick = self.events[0].get("tick") if self.events else "?"
        ab = {r["team"]: r for r in self.abuela() if r["dealer"] == "abuela"}
        short = {"common": "c", "uncommon": "u", "rare": "r", "epic": "e", "legendary": "l"}
        L = [f"# Rival profiles (Dani's dashboard, auto {time.strftime('%a %H:%M')}, tick {self.clock.get('tick')})", "",
             f"_From the public feed since tick {first_tick}, the leaderboard and our /api/me. Inferred: starting cards "
             f"and pack pulls are invisible. Collects = sets it buys or bids for; dumps = sets it sells or asks for. "
             f"Prices = median of its team trades and open bids (c/u/r). Δ = score change over ~{RECENT} ticks._", "",
             "## Teams", ""]
        prices = {}
        for p in prof:
            tid = p["team"]
            tp = self.team_prices(tid, market)
            prices[tid] = tp
            if p["us"]:
                label = "US"
            elif p["rank"] <= TOP_NEVER:
                label = f"top {TOP_NEVER} (never feed)"
            elif p["wants"]:
                label = f"buyer for {'/'.join(p['wants'])}"
            elif p["dumps"]:
                label = f"seller of {'/'.join(p['dumps'])}"
            elif "Quiet" in p["labels"]:
                label = "inactive"
            else:
                label = "trader"
            bits = [f"#{p['rank']} {p['name']} {p['score']:.1f}"
                    + (f" (Δ {p['delta']:+.1f})" if p["delta"] is not None else ""), f"**{label}**"]
            if not p["us"] and p["rank"] > TOP_NEVER and self.feeding_block(p, us_score):
                bits.append(f"no page closers (not ≥ {FEED_GAP} below us)")
            if p["wants"]:
                bits.append("collects " + "/".join(p["wants"]))
            if p["dumps"]:
                bits.append("dumps " + "/".join(p["dumps"]))
            if tp:
                bits.append("prices " + " ".join(f"{short.get(k, k)} {v:g}" for k, v in sorted(tp.items(), key=lambda kv: list(short).index(kv[0]) if kv[0] in short else 9)))
            bits.append(f"{p['team_trades']} team / {p['dealer_trades']} dealer trades, {p['listings']} listings")
            if tid in ab:
                bits.append(f"Abuela −{ab[tid]['avg_move']:g}%")
            if p["biggest"] and p["biggest"].split(" bought ")[0] == p["name"]:
                bits.append("big: " + p["biggest"].split(" bought ", 1)[1])
            L.append("- " + " · ".join(bits))

        # who to sell what to: our cards, best counterparty that passes the feeding rule
        copies = collections.defaultdict(list)
        for a in self.me.get("assets", []):
            if a.get("kind") == "card" and a.get("your_value") is not None:
                copies[a["ref"]].append(a["your_value"])
        all_med = collections.defaultdict(list)
        for tr in self.trades:
            if tr["kind"] == "team" and len(tr["items"]) == 1:
                all_med[tr["items"][0].get("rarity")].append(tr["price"])
        rows = []
        for ref, vals in copies.items():
            v = min(vals)
            rar, st = self.rarity(ref), set_of(ref)
            cands = []
            for p in prof:
                # every candidate collects the set or bids for the card, i.e. it may lack it: treat it as a page closer
                if p["us"] or self.feeding_block(p, us_score):
                    continue
                bid = max((r["price"] for r in market if r["team"] == p["team"] and r["side"] == "bid" and r["ref"] == ref), default=None)
                if bid is None and st not in p["wants"]:
                    continue
                price = bid if bid is not None else (prices[p["team"]].get(rar) or median(all_med.get(rar, [])))
                if price is None:
                    continue
                gain = round(price - v - self.fee(price), 1)
                cands.append((bid is not None, gain, p, price))
            cands = [c for c in cands if c[1] >= EDGE]
            if not cands:
                continue
            cands.sort(key=lambda c: (c[0], c[1]), reverse=True)
            hasbid, gain, p, price = cands[0]
            also = ", ".join(f"{c[2]['name']} {c[3]:g}" for c in cands[1:4])
            rows.append((gain, f"| {ref} {rar[0] if rar else '?'} | {len(vals)} | {v:g} | {p['name']} (#{p['rank']}, "
                               f"{us_score - (p['score'] or 0):.1f} below) "
                               f"| {price:g}{' bid' if hasbid else ' est.'} | {gain:+g} | {also or '—'} |"))
        rows.sort(key=lambda r: -r[0])
        L += ["", f"## Who to sell what to (us #{our_rank}, {us_score:.1f}; never the top {TOP_NEVER}, "
                  f"only teams ≥ {FEED_GAP} points below us)", "",
              f"_Feeding rule: each buyer here collects the set or bids for the card, so the card may close its page; it goes "
              f"only to teams ≥ {FEED_GAP} points below us and never to the top {TOP_NEVER}. Our copies (cheapest value); "
              f"an open bid beats an estimate. Gain = price − our value − El Rastro fee (if we accept; 0 fee if they "
              f"accept our ask)._", "",
              "| Card | Copies | Our value | Best buyer | Price | Gain | Also |", "|---|---|---|---|---|---|---|"]
        L += [r[1] for r in rows] or ["| — | | | no buyer passes the feeding rule above our value + 3 yet | | | |"]
        text = "\n".join(L) + "\n"
        if len(text) > 5900:  # the analysts read 6000 characters: drop the tail of the team list first
            head, rest = text.split("\n## Who to sell", 1)
            sell = "\n## Who to sell" + rest
            keep = 5900 - len(sell) - 40
            text = head[:keep].rsplit("\n", 1)[0] + "\n- … (more teams on the dashboard)\n" + sell
        return text

    def build(self):
        self.scan()
        prof = self.profiles()
        market = self.market()
        story = self.story()
        price_rows, last_price = self.prices()
        s = self.me.get("score") or {}
        us = next((p for p in prof if p["us"]), None)
        for p in prof:
            p["feed_block"] = None if p["us"] or not us else self.feeding_block(p, us["score"])
        above = next((p for p in prof if us and p["rank"] == us["rank"] - 1), None)
        below = next((p for p in prof if us and p["rank"] == us["rank"] + 1), None)
        neighbours = [p["team"] for p in prof if us and abs(p["rank"] - us["rank"]) <= 2]
        duelview = self.duel_view()
        return {
            "duelview": duelview,
            "duelmon": self.duel_monitor(duelview),
            "conversations": self.conversations(),
            "story": story,
            "moves": self.moves(story),
            "decisions": self.decisions(),
            "decisions_src": self.c.directives_src,
            "neighbours": neighbours,
            "above": {"name": above["name"], "score": above["score"], "rank": above["rank"]} if above else None,
            "below": {"name": below["name"], "score": below["score"], "rank": below["rank"]} if below else None,
            "lb_score": us["score"] if us else None, "lb_rank": us["rank"] if us else None,
            "now": time.strftime("%H:%M:%S"),
            "updated": datetime.fromtimestamp(self.c.updated).strftime("%H:%M:%S") if self.c.updated else None,
            "requests": self.c.requests, "errors": list(self.c.errors), "has_key": self.c.team is not None,
            "events_cached": len(self.events),
            "hub": dict(self.c.hub),
            "clock": {k: self.clock.get(k) for k in ("tick", "t_hours", "tick_seconds", "paused", "next_tick_in",
                                                     "closes", "opens", "limits")},
            "us": self.us,
            "me": {"cash": self.me.get("cash"), "level": self.me.get("level"), "collection_value": self.me.get("collection_value"),
                   "affinity": self.aff, "unlocked": self.me.get("unlocked"),
                   "album": f"{(self.me.get('album') or {}).get('filled')}/{(self.me.get('album') or {}).get('slots')}",
                   "score": {k: s.get(k) for k in ("score", "rank", "negotiating", "market", "neg_points", "ladder_points",
                                                   "duel_points", "bench_efficiency", "deals", "pages_complete", "luck")}},
            "me_hist": self.me_hist[-500:],
            "lb_hist": [{"tick": h["tick"], "scores": {k: v.get("score") for k, v in h["teams"].items()}}
                        for h in self.lb_hist],
            "names": self.names,
            "teams": prof,
            "insights": self.insights(prof, market),
            "market": market,
            "prices": price_rows,
            "tape": self.tape(),
            "team_trades": self.team_trades(prof),
            "pulse": self.market_pulse(prof),
            "collection": self.collection(prof),
            "strategies": self.strategies(prof),
            "holders": self.holders(),
            "abuela": self.abuela(),
            "schedule": self.schedule(),
            "levels": self.levels,
            "dealers": [{"id": d["id"], "name": d.get("name"), "status": d.get("status"), "level": d.get("level"),
                         "line": d.get("line") or d.get("teaser"), "open_to_us": d["id"] in (self.me.get("unlocked") or [])}
                        for d in self.dealers],
            "venues": [{k: v.get(k) for k in ("venue", "name", "owner_name", "status", "fee_bps", "trades", "volume",
                                              "traders")} for v in self.venues],
            "duels": self.duels, "duels_done": self.duels_done[-40:],
            "duel_events": [{"tick": e.get("tick"), "type": e.get("type"),
                             "text": json.dumps(e.get("payload"), ensure_ascii=False)[:200]} for e in self.duel_events[-30:]],
            "news": self.news[-20:][::-1],
        }


# ---------------------------------------------------------------------------------------------- web

def last_seen(files, _cache={}):
    """When each file last changed on GitHub (`git log origin/main`, which read_directives keeps fetched): the "last
    seen" of the agent that writes it, for the showcase diagram. Local git only, no game request; cached 2 minutes."""
    out = {}
    for f in files:
        t, v = _cache.get(f, (0.0, None))
        if time.time() - t > 120:
            v = None
            for ref in ("origin/main", "HEAD"):
                try:
                    r = _run(["git", "-C", str(ROOT), "log", "-1", "--format=%cd", "--date=format:%a %H:%M",
                                        ref, "--", f], capture_output=True, text=True, timeout=5)
                except (OSError, subprocess.SubprocessError):
                    continue
                if r.returncode == 0 and r.stdout.strip():
                    v = r.stdout.strip()
                    break
            _cache[f] = (time.time(), v)
        out[f] = v
    return out


def show_data(c):
    """judges/show.json, read fresh on every call (Dani edits it during the day), plus each diagram node's last seen and
    our /api/me row at each tick the story names (/api/data only carries the last 500 rows)."""
    try:
        show = json.loads(SHOW_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return {"error": f"judges/show.json: {e}"[:300]}
    files = [n["file"] for col in (show.get("how") or {}).get("columns", []) for n in col.get("nodes", []) if n.get("file")]
    show["last_seen"] = last_seen(files)
    ticks = {(show.get("hero") or {}).get("since_tick"), (show.get("waterfall") or {}).get("start_tick"),
             (show.get("waterfall") or {}).get("end_tick")} - {None}
    with c.lock:
        rows = list(c.me_hist)
    show["me_at"] = {}
    for t in ticks:
        before = [r for r in rows if r.get("tick") is not None and r["tick"] <= t]
        show["me_at"][str(t)] = before[-1] if before else None
    return show


class Handler(BaseHTTPRequestHandler):
    collector: Collector = None
    _cache = (0.0, b"")

    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
        if self.path.split("?")[0] in ("/show", "/show.html"):
            return self._send(200, (HERE / "show.html").read_bytes(), "text/html; charset=utf-8")
        if self.path.startswith("/api/show"):
            return self._send(200, json.dumps(show_data(self.collector), ensure_ascii=False, default=str).encode(),
                              "application/json; charset=utf-8")
        if self.path.startswith("/api/data"):
            t, body = Handler._cache
            if time.time() - t > 3:
                try:
                    body = json.dumps(Analysis(self.collector).build(), default=str).encode()
                except Exception as e:  # show the error in the page instead of a blank screen
                    body = json.dumps({"fatal": repr(e)[:500]}).encode()
                Handler._cache = (time.time(), body)
            return self._send(200, body, "application/json")
        self._send(404, b"not found", "text/plain")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-key", action="store_true", help="public data only")
    ap.add_argument("--teams-every", type=int, default=600, help="seconds between intel/teams.md rewrites; 0 = off")
    ap.add_argument("--push", action="store_true", help="commit and push intel/teams.md after each rewrite")
    ap.add_argument("--no-hub", action="store_true", help="don't read the team hub even if HUB_READER_URL is set")
    args = ap.parse_args()
    key = None if args.no_key else load_key()
    hub_url = None if args.no_hub else env_value("HUB_READER_URL")
    c = Collector(key, hub_url)
    c.teams_every, c.teams_push = args.teams_every, args.push
    threading.Thread(target=c.run, daemon=True).start()
    Handler.collector = c
    ThreadingHTTPServer.allow_reuse_address = os.name != "nt"  # on Windows reuse lets a 2nd copy share the port
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    except OSError:
        print(f"Port {args.port} is busy: the dashboard is probably already running on http://127.0.0.1:{args.port}")
        return
    print(f"Bazaar dashboard on http://127.0.0.1:{args.port}  (team key: {'yes' if key else 'no'}; "
          f"hub: {'yes' if hub_url else 'no'}; read-only)", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
