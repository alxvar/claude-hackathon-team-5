"""Page arithmetic (holdings audit, Sun 00:45): what the public data proves about each team's album. Read-only.

The feed gives a lower bound of each team's page cards (matchmaker.counts). The keyless leaderboard gives the server's
exact `album_filled` (distinct page cards held) and `pages_complete`, and the catalog's `minted` rules out a hidden copy
of any card whose every copy is traced. An album fits a team when it holds every page card the feed shows, no card
without a hidden copy left, and matches both counts. A card in every fitting album is held, one in none is a proven gap,
the rest are undecided. No fitting album means a card the feed shows held is gone (a Workshop craft ate it): the team is
"inconsistent" and only the feed counts. The audit resolved 10 teams exactly this way, 0 errors on our own album.

Also here: named receipts (taller.crafted names the card, egg.given and gift.given give refs; none carries an asset id),
each team's Workshop crafts (each eats three cards of the `from` rarity), and the last public sighting of every copy,
for the seller-safety check (a "holds 2+" is only safe for copies seen after the seller's last craft of that rarity).
"""
from __future__ import annotations

from collections import defaultdict


def is_team(x) -> bool:
    return isinstance(x, str) and len(x) == 3 and x[0] == "t" and x[1:].isdigit()


def receipts(events, cards: dict) -> list[tuple[int, str, str, str]]:
    """[(tick, team, card, source)] for cards a team got without an asset id: a Workshop craft (the payload names the
    card and its rarity), an egg or a gift."""
    by_name = {(c["name"], c["rarity"]): ref for ref, c in cards.items()}
    out = []
    for e in events:
        p, typ = e.get("payload") if isinstance(e.get("payload"), dict) else {}, e.get("type")
        if typ == "taller.crafted":
            ref = by_name.get((p.get("card"), p.get("to")))
            if ref and is_team(p.get("team")):
                out.append((e["tick"], p["team"], ref, f"crafted it at the Workshop (tick {e['tick']})"))
        elif typ in ("egg.given", "gift.given"):
            for ref in p.get("cards") or []:
                if ref in cards and is_team(p.get("team")):
                    what = "an egg" if typ == "egg.given" else "a gift"
                    out.append((e["tick"], p["team"], ref, f"got it from {what} (tick {e['tick']})"))
    return out


def crafts(events) -> dict:
    """{team: [(tick, from rarity)]}: each craft eats three cards of that rarity, copies unknown."""
    out: dict = defaultdict(list)
    for e in events:
        p = e.get("payload") if isinstance(e.get("payload"), dict) else {}
        if e.get("type") == "taller.crafted" and is_team(p.get("team")):
            out[p["team"]].append((e["tick"], p.get("from")))
    return dict(out)


def last_craft(cr: dict, team: str, rarity: str):
    ticks = [t for t, frm in cr.get(team, ()) if frm == rarity]
    return max(ticks) if ticks else None


def trace(events, cards: dict | None = None) -> dict:
    """{asset id: (tick, holder, card)}: the latest public sighting of each copy (a settlement's receiver, the team's
    own ask, its offer to a dealer unless the copy has since left it, a pack's best pull). With `cards`, also {"anon": {team: [(card, tick, source)]}}
    under the key None: copies a team got without an asset id (a gift, an egg, a Workshop craft) that no later id has
    claimed. A copy first seen with a new id at a team (sold or listed) claims its oldest matching id-less copy: the
    lower bound the holdings audit used (0 errors on our own album)."""
    last: dict = {}
    anon: dict = defaultdict(list)

    def claim(team, ref, tick):
        for k, (r, t0, _) in enumerate(anon[team]):
            if r == ref and t0 <= tick:
                anon[team].pop(k)
                return

    def see(a, holder, tick, new=True):
        if isinstance(a, dict) and a.get("id") is not None and a.get("ref") and holder:
            if a["id"] not in last and new:
                claim(holder, a["ref"], tick)
            if a["id"] not in last or tick >= last[a["id"]][0]:
                last[a["id"]] = (tick, holder, a["ref"])
    rec = iter(receipts(events, cards)) if cards is not None else iter(())
    nxt = next(rec, None)
    for e in events:
        p, typ, tk = e.get("payload") if isinstance(e.get("payload"), dict) else {}, e.get("type"), e.get("tick") or 0
        while nxt is not None and nxt[0] < tk:
            anon[nxt[1]].append((nxt[2], nxt[0], nxt[3]))
            nxt = next(rec, None)
        if typ == "settlement":
            for i in p.get("items") or []:
                if i.get("kind") == "card":
                    if i.get("id") is not None and i["id"] not in last:
                        if is_team(i.get("frm")):
                            claim(i["frm"], i.get("ref"), tk)         # sold a copy never seen: an id-less one
                        last[i["id"]] = (tk, i.get("frm"), i.get("ref"))
                    see(i, i.get("to"), tk)
        elif typ == "offer.listed":
            o = p.get("offer") or {}
            maker = o.get("maker") if is_team(o.get("maker")) else e.get("actor")
            for a in (o.get("give") or {}).get("assets") or []:
                see(a, maker, tk)
        elif typ == "thread.message" and p.get("kind") == "persona" and p.get("sender") == p.get("team"):
            for a in ((p.get("offer") or {}).get("give") or {}).get("assets") or []:
                if not isinstance(a, dict) or a.get("id") not in last or last[a["id"]][1] == p.get("team"):
                    see(a, p.get("team"), tk)                  # a thread re-sends a copy it already sold: stale
        elif typ == "pack.opened":
            see(p.get("best"), p.get("team"), tk, new=False)       # a fresh copy, not an id-less one revealed
        elif typ in ("gift.given", "egg.given", "taller.crafted"):
            while nxt is not None and nxt[0] <= tk:
                anon[nxt[1]].append((nxt[2], nxt[0], nxt[3]))
                nxt = next(rec, None)
    while nxt is not None:
        anon[nxt[1]].append((nxt[2], nxt[0], nxt[3]))
        nxt = next(rec, None)
    if cards is not None:
        last[None] = {"anon": dict(anon)}
    return last


def copies(tr: dict) -> dict:
    """(team, card) → copies the trace puts at the team: copies with an id last seen there plus unclaimed id-less ones."""
    out: dict = defaultdict(int)
    for aid, v in tr.items():
        if aid is not None and is_team(v[1]):
            out[(v[1], v[2])] += 1
    for team, xs in ((tr.get(None) or {}).get("anon") or {}).items():
        for ref, _, _ in xs:
            out[(team, ref)] += 1
    return dict(out)


def copies_after(tr: dict, team: str, card: str, since=None) -> int:
    """Copies of `card` last seen at `team`, counting only sightings after tick `since` (None: all)."""
    return sum(1 for aid, v in tr.items() if aid is not None and v[1] == team and v[2] == card
               and (since is None or v[0] > since))


def exhausted(tr: dict, catalog: dict) -> set:
    """Cards whose every minted copy is traced: no team can hold a copy the feed hasn't shown."""
    seen: dict = defaultdict(set)
    for aid, v in tr.items():
        if aid is not None:
            seen[v[2]].add(aid)
    return {c["id"] for s in catalog.get("sets") or [] for c in s.get("cards") or []
            if isinstance(c.get("minted"), int) and c["minted"] > 0 and len(seen[c["id"]]) >= c["minted"]}


def released(catalog: dict, pg: dict) -> list:
    """The sets the album counts now (catalog `released`; a set without the flag counts)."""
    return [s["id"] for s in catalog.get("sets") or [] if s["id"] in pg and s.get("released", True)]


def solve(sets: list[tuple[str, int, int, int]], filled: int, complete: int) -> dict | None:
    """sets: [(set, k known held, u unknown, page size)]. → {set: sorted feasible counts of unknown cards held} over
    every album with Σ held = filled and #full pages = complete; None when no album fits."""
    def opts(k, u, size):
        return [(h, k + h, int(k + h == size)) for h in range(u + 1)]
    fwd = [{(0, 0)}]
    for _, k, u, size in sets:
        fwd.append({(a + f, b + c) for a, b in fwd[-1] for _, f, c in opts(k, u, size)})
    bwd = [{(0, 0)}]
    for _, k, u, size in reversed(sets):
        bwd.append({(a + f, b + c) for a, b in bwd[-1] for _, f, c in opts(k, u, size)})
    bwd.reverse()
    out = {}
    for i, (st, k, u, size) in enumerate(sets):
        ok = []
        for h, f, c in opts(k, u, size):
            if any((filled - a - f, complete - b - c) in bwd[i + 1] for a, b in fwd[i]):
                ok.append(h)
        if not ok:
            return None
        out[st] = ok
    return out


def team_album(team: str, n: dict, pg: dict, sets: list, row: dict, gone: set, lacking=frozenset()) -> dict:
    """One team's album from the feed (n: (team, card) → copies), its leaderboard row and the exhausted cards.
    → {status: exact | partial | repaired | inconsistent | unknown, why, held, gap, undecided,
       complete: {set: True/False/None}}"""
    filled, pc, slots = row.get("album_filled"), row.get("pages_complete"), row.get("album_slots")
    size = sum(len(pg[s]["cards"]) for s in sets)
    base = {"held": set(), "gap": set(), "undecided": set(), "complete": {}}
    if not isinstance(filled, int) or not isinstance(pc, int):
        return {**base, "status": "unknown", "why": "no album_filled/pages_complete"}
    if isinstance(slots, int) and slots != size:
        return {**base, "status": "unknown", "why": f"album_slots {slots} ≠ {size} page cards in the released sets"}
    known, unk, spec = {}, {}, []
    rarest = (row.get("rarest") or {}).get("ref")             # the server names the team's rarest copy
    for st in sets:
        cs = pg[st]["cards"]
        known[st] = [c for c in cs if n.get((team, c)) or c == rarest]
        unk[st] = [c for c in cs if c not in known[st] and c not in gone and c not in lacking]
        spec.append((st, len(known[st]), len(unk[st]), len(cs)))
    out = _read(sets, pg, known, unk, solve(spec, filled, pc))
    if out is not None:
        return {**base, **out}
    # No album fits: one card the feed shows held is gone (the audit's t06/t14: a craft ate it). Try each set with one
    # of its known cards back in the unknown pool; a card counts only where every repaired album agrees.
    reads = []
    for i, (st, k, u, size_) in enumerate(spec):
        if k:
            rel = spec[:i] + [(st, k - 1, u + 1, size_)] + spec[i + 1:]
            r = _read(sets, pg, known, unk, solve(rel, filled, pc), relaxed=st)
            if r is not None:
                reads.append(r)
    why = (f"no album fits: the feed shows {sum(len(v) for v in known.values())} page cards, the server counts "
           f"{filled} with {pc} complete pages (a card the feed shows held is gone)")
    if not reads:
        return {**base, "status": "inconsistent", "why": why}
    held = set.intersection(*(r["held"] for r in reads))
    gap = set.intersection(*(r["gap"] for r in reads))
    every = {c for st in sets for c in pg[st]["cards"]}
    comp = {st: (lambda v: v.pop() if len(v) == 1 else None)({r["complete"][st] for r in reads}) for st in sets}
    return {**base, "status": "repaired", "why": why + f"; {len(reads)} repaired album(s) agree on these",
            "held": held, "gap": gap, "undecided": every - held - gap, "complete": comp}


def _read(sets, pg, known, unk, sol, relaxed=None) -> dict | None:
    """held / gap / undecided / complete from solve()'s feasible counts. `relaxed`: the set whose known cards are all
    held but one (which one unknown), so solve() saw k − 1 known and that card back in the unknown pool."""
    if sol is None:
        return None
    out = {"status": "exact", "why": "", "held": set(), "gap": set(), "undecided": set(), "complete": {}}
    for st in sets:
        hs, cs, kn, un = sol[st], pg[st]["cards"], known[st], unk[st]
        r = st == relaxed
        k0, pool = (len(kn) - 1, len(un) + 1) if r else (len(kn), len(un))
        out["gap"] |= {c for c in cs if c not in kn and c not in un}
        if min(hs) == pool:
            out["held"] |= set(kn) | set(un)
        else:
            out["undecided" if r else "held"] |= set(kn)
            out["gap" if un and max(hs) == 0 else "undecided"] |= set(un)
        if (out["undecided"] & set(cs)) and out["status"] == "exact":
            out["status"] = "partial"
        full = [k0 + h == len(cs) for h in hs]
        out["complete"][st] = True if all(full) else False if not any(full) else None
    return out


def albums(n: dict, pg: dict, catalog: dict, lb: dict | None, gone: set, teams=None, lacking: dict | None = None) -> dict:
    """{team: team_album(...)} for every team on the leaderboard; {} without a leaderboard."""
    if not lb:
        return {}
    sets = released(catalog, pg)
    return {t: team_album(t, n, pg, sets, row, gone, (lacking or {}).get(t, frozenset()))
            for t, row in lb.items() if is_team(t) and (teams is None or t in teams)}


def status(alb: dict, team: str, card: str) -> str | None:
    """'held' | 'gap' | 'undecided' | None (no usable arithmetic for that team)."""
    a = (alb or {}).get(team)
    if not a or a["status"] not in ("exact", "partial", "repaired"):
        return None
    return "held" if card in a["held"] else "gap" if card in a["gap"] else "undecided" if card in a["undecided"] \
        else None
