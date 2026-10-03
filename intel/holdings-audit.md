# Holdings audit: what public data proves about each team's album

_Independent audit, Sun 00:45. Read-only, no keyed calls (two unkeyed GETs: `/api/leaderboard` and `/api/cards/308`).
Data: `data/feed.jsonl` + `data/hub/feed-lucas.jsonl` (27,162 public events, ticks 2-1445), `run/catalog.json` (00:23),
the tick-1440 leaderboard (`archive/2026-10-03-round2/leaderboard-232426.json`), `data/board.json`, and the saved
`/api/me` in `tests/fixtures/opportunities_friday.json` (for field names). The doors are shut until Sun 09:00, so these
holdings are still current. Scripts: session scratchpad (`recon.py`, `worlds.py`, `report.py`); method below._

## Short answer

- **Is 100 % exact possible from public data? No.** No public endpoint lists another team's cards. Three channels never
  reach the feed: starting hands, the contents of commons-only packs, and which copies the Workshop eats.
- **Near-exact is possible, though.** Join the feed (card ids), the leaderboard's per-team `album_filled` and `pages_complete`,
  and the catalog's `minted` per card. We can then name **588 of the 641 page cards the 18 teams hold (91.7 %)**.
  **10 teams resolve to a single album that fits every public number:** t01, t05, t07, t10, t12, t13, t15, t16, t17, t18.
  On our own album (t05) the reconstruction matches the truth card for card: 39 held and 11 lacking, 0 errors.
  The feed alone gives 82.5 %, and today's matchmaker gets 81.7 % (524 cards).
- **Starting albums are not shown anywhere, but they can be partly decoded.** Asset ids 1-270 are the starting deal:
  15 per team in team order (t01 = 1-15 … t18 = 256-270). Slots 1-11 are commons, 12-14 uncommons, slot 15 the rare.
  179 of the 270 slots have since surfaced in the feed. 91 never have, including all 15 of t11's.
- **Best path to exact holdings:** (a) a partner runs the one-liner in §3, and we check its output against the public
  leaderboard; (b) one keyed test of `GET /api/cards/{id}` (see Open items).

## 1. Team by team

**Method.** A card is "held" when its asset id's last public event leaves it with the team, or when a gift, egg or
Workshop event names the card. Public events: settlement `to`/`frm`, the team's own ask (`offer.listed` give.assets),
its offer to a dealer, or a pack's `best`.
I then list every album that fits the server's `album_filled` (distinct page cards 01-10 held; `album_slots` is
50 = 5 sets × 10, and it was 40 with 4 sets on Friday [Verified]) and `pages_complete`. Each album must also respect
supply: a card with `minted` = copies already traced (LAT-03, LAV-09, MAL-10, RET-09, RET-10) has no hidden copy left.
Albums are checked one team at a time; supply is not cross-checked between teams. Even so, the 56 hidden copies these
albums need never exceed any card's untraced supply.
A card that every fitting album contains counts as held. One that no fitting album can contain counts as proven lacking.

| Team | Rank | Album (server) | Pages (server) | Known held | % of album | Proven lacking | Undecided (held among them) | Status |
|---|---|---|---|---|---|---|---|---|
| t01 | 9 | 37/50 | 3 | 37 | 100% | 13 | 0 (0) | EXACT (unique) |
| t02 | 15 | 31/50 | 2 | 26 | 84% | 2 | 22 (5) | partial |
| t03 | 5 | 30/50 | 2 | 23 | 77% | 3 | 24 (7) | partial |
| t04 | 12 | 40/50 | 3 | 39 | 98% | 1 | 10 (1) | near |
| t05 (us) | 3 | 39/50 | 3 | 39 | 100% | 11 | 0 (0) | EXACT, **matches our real album** |
| t06 | 6 | 40/50 | 3 | 30 | 75% | 9 | 11 (10) | inconsistent by 1 card |
| t07 | 17 | 37/50 | 3 | 37 | 100% | 13 | 0 (0) | EXACT (unique) |
| t08 | 11 | 33/50 | 2 | 28 | 85% | 2 | 20 (5) | partial |
| t09 | 16 | 41/50 | 1 | 29 | 71% | 2 | 19 (12) | partial |
| t10 | 1 | 37/50 | 3 | 37 | 100% | 13 | 0 (0) | EXACT (unique) |
| t11 | 18 | 13/50 | 0 | 1 | 8% | 5 | 44 (12) | blind (inactive; hand never shown) |
| t12 | 4 | 40/50 | 3 | 40 | 100% | 10 | 0 (0) | EXACT (unique) |
| t13 | 10 | 32/50 | 3 | 32 | 100% | 18 | 0 (0) | EXACT (unique) |
| t14 | 7 | 41/50 | 4 | 40 | 98% | 8 | 2 (1) | inconsistent by 1 card |
| t15 | 13 | 42/50 | 4 | 42 | 100% | 8 | 0 (0) | EXACT (unique) |
| t16 | 14 | 34/50 | 2 | 34 | 100% | 16 | 0 (0) | EXACT (unique) |
| t17 | 8 | 37/50 | 3 | 37 | 100% | 13 | 0 (0) | EXACT (unique) |
| t18 | 2 | 37/50 | 3 | 37 | 100% | 13 | 0 (0) | EXACT (unique) |
| **All** | | 641 | | **588** | **91.7%** | 160 of 259 missing | | |

**Grids** (positions 01-10 of each page: `x` held, `-` proven lacking, `?` undecided):

| Team | LAV | MAL | LAT | SAL | RET | Evidence behind the known-held cards |
|---|---|---|---|---|---|---|
| t01 | `xxxxxxxxxx` | `xxxxxxxxxx` | `xxx-----x-` | `xxxxxxxxxx` | `x--x---x--` | settlement 16, ask 10, page arithmetic 9, Workshop 2 |
| t02 | `????????-?` | `xx??x?xx?x` | `xx-?x?????` | `?xxxxx?xx?` | `xxxxxxxxxx` | settlement 16, dealer offer 5, ask 5 |
| t03 | `x?x?xxxxxx` | `?x???????-` | `?xx??xxxx?` | `xx?xxxxxx?` | `????????--` | settlement 18, ask 4, dealer offer 1 |
| t04 | `xxxxxxxxxx` | `xxxxx??x?-` | `xxxxxxxxxx` | `x??x????x?` | `xxxxxxxxxx` | ask 21, settlement 10, page arithmetic 4, dealer offer 4 |
| t05 | `xxxxxxxxxx` | `xxxxxx-x--` | `--xx------` | `xxxxxxxxxx` | `xxxxxxxxxx` | settlement 16, ask 14, page arithmetic 6, gift, egg, dealer offer |
| t06 | `xxxxxxxxxx` | `????------` | `??-?????--` | `xxxxxxxxxx` | `xxxxxxxxxx` | ask 15, settlement 9, page arithmetic 3, gift/Workshop 3 |
| t07 | `xxxxxxxxxx` | `xx-xx-----` | `xxxxxxxxxx` | `--xx----x-` | `xxxxxxxxxx` | ask 19, settlement 12, page arithmetic 3, pack 2, dealer offer 1 |
| t08 | `???xx???-?` | `x?xx??x?xx` | `xxxxx?????` | `xxxxxxxxxx` | `??xxxx??x-` | ask 18, settlement 5, dealer offer 2, page arithmetic 1, Workshop 2 |
| t09 | `???x?x?xxx` | `???x?xxx?-` | `xxxxx??x??` | `?x??x?xxx?` | `xxxxxxxx-x` | settlement 17, ask 11, pack 1 |
| t10 | `xxxxxxxxxx` | `xxxxxxxxxx` | `-x-x------` | `xxxxx-----` | `xxxxxxxxxx` | ask 17, settlement 10, page arithmetic 6, Workshop 2, gift, egg |
| t11 | `????????-?` | `????????x-` | `??-???????` | `??????????` | `????????--` | leaderboard `rarest` (MAL-09) only |
| t12 | `xxxxx--x--` | `xxxxxxxxxx` | `xxxxxxxxxx` | `-xxxx-----` | `xxxxxxxxxx` | ask 17, settlement 15, page arithmetic 6, Workshop 2 |
| t13 | `xxxxxxxxxx` | `xxxxxxxxxx` | `--x-------` | `xxxxxxxxxx` | `---x------` | settlement 14, ask 10, dealer offer 5, page arithmetic 3 |
| t14 | `xxxxxxxxxx` | `??--------` | `xxxxxxxxxx` | `xxxxxxxxxx` | `xxxxxxxxxx` | settlement 28, ask 8, page arithmetic 3, Workshop 1 |
| t15 | `xxxxxxxxxx` | `xxxxxxxxxx` | `xxxxxxxxxx` | `--xx------` | `xxxxxxxxxx` | settlement 25, ask 12, page arithmetic 2, pack, dealer offer, start serial |
| t16 | `xx-xxx--x-` | `xxxxx-----` | `xxxxxxxxxx` | `xxxxxxxxxx` | `----x-xx--` | ask 24, settlement 8, page arithmetic 2 |
| t17 | `xxxxxxxxxx` | `xxxxxxxxxx` | `x---x--x--` | `xxxxxxxxxx` | `---x--xxx-` | settlement 17, ask 8, page arithmetic 7, dealer offer 2, Workshop 2, gift |
| t18 | `-xx-x-----` | `xx-xx-----` | `xxxxxxxxxx` | `xxxxxxxxxx` | `xxxxxxxxxx` | ask 15, settlement 14, page arithmetic 7, start serial 1 |

"Page arithmetic" means a card was not seen in the feed, but every album that fits `album_filled` + `pages_complete` +
supply contains it. Example: t13 shows 29 cards and the server counts 32 with 3 complete pages. The only way 3 unseen
cards make a third complete page is SAL-01/02/04, all of which fit t13's 4 hidden starting commons.
"Start serial" works because card serials rise with asset id inside the starting deal (55 cards checked, 0 exceptions).
That pins three hidden starting rares: t11 MAL-09 (the leaderboard's `rarest` for t11 agrees), t15 LAT-09 and t18 SAL-09.

**Undecided cards** (the team holds the number shown in brackets in the first table, among these):
t02 LAT-04 06 07 08 09 10, LAV-01 02 03 04 05 06 07 08 10, MAL-03 04 06 09, SAL-01 07 10 · t03 LAT-01 04 05 10,
LAV-02 04, MAL-01 03-09, RET-01-08, SAL-03 10 · t04 MAL-06 07 09, SAL-02 03 05 06 07 08 10 · t08 LAT-06-10,
LAV-01 02 03 06 07 08 10, MAL-02 05 06 08, RET-01 02 07 08 · t09 LAT-06 07 09 10, LAV-01 02 03 05 07, MAL-01 02 03 05
09, SAL-01 03 04 06 10 · t11 everything but MAL-09 and 5 proven gaps.

**The two inconsistent teams** (no album fits unless one card the feed shows as held is gone):
- **t14**: one of MAL-01 / MAL-02 is gone. Every repaired album still has LAV, LAT, SAL and RET complete.
- **t06**: one of LAT-01/02/04-08 or MAL-01-04 is gone. LAT-03 cannot be the card that completes t06's LAT page:
  all 20 minted copies are traced, and none is at t06.
- Both teams used the Workshop 4 times. My best guess is a craft that took a last copy, or a settlement that never
  reached the feed [Uncertain]. These two cases put the rate of silently vanished "held" cards at about 2 in 590.

**Live bids at close** (feed, not cancelled, expired or filled): t01 MAL-11 144; t06 SAL-12 450, MAL-09 31, MAL-02 2,
MAL-05 2; t09 MAL-09 56, MAL-10 56, SAL-06 24; t16 RET-11 103, MAL-11 63, RET-09 32, RET-10 32, LAV-10 28, RET-06 18.
All 7 that land on a decided page card land on a proven gap. The other 3 (t06 MAL-02, t09 MAL-09, t09 SAL-06) are undecided.

## 2. Which signals to trust, and where the matchmaker goes wrong

| Signal | What it proves | Measured reliability |
|---|---|---|
| Settlement (`items[].frm/to`, asset id) | The holder at that tick | 793 unique settlements, 0 contradictions once the backfilled duplicates are dropped [Verified]. Trade counts per venue equal the leaderboard's `trades` for every team venue, and El Rastro's Saturday count is 89 = 89 [Verified]. 333 of the 1,126 settlement numbers never appear publicly; they line up with grants, packs, gifts, crafts and unlocks [Likely] |
| Ask (`offer.listed` give.assets) | Holding when posted | 6,147 asset sightings, 0 contradictions [Verified]. Strongest live proof |
| Leaderboard `album_filled`, `pages_complete`, `rarest` (ref + serial) | Exact counts per team, refreshed every ~10 ticks | Server truth, but aggregate. `tools/collector.py` **drops them** from `data/leaderboard.jsonl` |
| Catalog `minted` per card | Total supply | Rules out hidden copies of 5 page cards |
| Gift / egg / Workshop (`gift.given`, `egg.given`, `taller.crafted` name→ref) | The team got that card | No asset id, so a later resale can't be linked. Of 69 resales I matched by heuristic, page arithmetic confirms 3 for t13 |
| Offer to a dealer (thread.message give.assets) | Weak: holding at that time | 9 of 2,359 were stale: the team had already sold the card |
| `pack.opened.best` | Only rare or better | All 61 neighbourhood packs and 11 of 17 welcome packs show nothing |
| Bid (want cards) | Lacked it **when posted** | 2,607 bids on 344 (team, card) pairs. 1.7 % came from a team the feed already showed holding the card (a lower bound). 55 % were under half book (bargain hunting). Bids outlive the need |

**Matchmaker (`intel/matches.md` at 00:23)**

- **Holdings:** 524 cards claimed, **0 proven wrong**, but it misses 77 cards that are proven held. The causes: it
  ignores `album_filled` and minted supply; it never parses `taller.crafted` (34 crafted cards) or `egg.given`; and it
  drops dealer-offer evidence when a later `gone` signal arrives.
- **Demand is where it fails.** Of its 20 matches, **6 send a card to a buyer that already holds it**:
  - #3 and #4: t15 MAL-09/MAL-10. t15 bought both from Pícaros at ticks 920 and 1037, and `pages_complete` = 4 is
    only possible with MAL complete.
  - #6: t01 RET-08 (from the Workshop, t1326).
  - #7: t08 SAL-03 (the "✓" comes from a Friday bid at t142; t08's SAL page is complete).
  - #9: t17 LAV-06 (from the Workshop, t929).
  - #10: t14 LAV-01 (held in every repaired album).

  Four buyers are undecided (#8, #14, #18, #19). Nine are confirmed gaps (#2, #5, #11, #12, #13, #15, #16, #17, #20).
  #1 is an epic.
- **"One or two cards from a page":** 11 of its 15 lines are pages that are already complete. Only t09 RET-09
  (a proven gap: all 14 copies are traced) and t03 SAL-03/SAL-10 are open; t14's two lines are complete in every repaired album.
- **The source of #3/#4:** `run/known_holdings.json` overrides the feed. Its t15 entry contradicts both the feed and the
  server, and its t05 entry is stale: we got MAL-06 from an egg at tick 1368.
- **Sellers:** "holds 2+" ignores the Workshop. t01 (4 crafts) and t08 (5 crafts) had their duplicates in #7, #11, #12
  and #19 last seen before a craft, so the spare may be gone.
- **Fixes, in order:**
  1. Have the collector keep `album_filled`/`pages_complete`/`rarest`, and run the page arithmetic before each match.
  2. Parse `taller.crafted` and `egg.given`.
  3. Let a known-holdings entry win only while Σhave = `album_filled` at the same snapshot.
  4. Expire bids once the bidder later receives the card.

## 3. How a partner team shares exact holdings

**Command** (their key stays in their environment; it prints no cash, no values, no key):

```bash
curl -s -H "X-Team-Key: $BAZAAR_KEY" https://bazaar.causaprima.ai/api/me | python3 -c 'import json,sys,collections as C;m=json.load(sys.stdin);n=C.Counter(a["ref"] for a in m["assets"] if a.get("kind")=="card");[print(p["set"],"%d/%d"%(p["have"],p["of"]),"HELD:"," ".join(r+("x%d"%n[r] if n[r]>1 else "") for r in sorted(n) if r.startswith(p["set"]+"-")) or "-","| MISSING:"," ".join(c for c in ["%s-%02d"%(p["set"],i) for i in range(1,11)] if c not in n) or "-") for p in m["album"]["pages"]]'
```

Output, tested on our saved Friday `/api/me`:
`MAL 4/10 HELD: MAL-02 MAL-04 MAL-06 MAL-07 | MISSING: MAL-01 MAL-03 MAL-05 MAL-08 MAL-09 MAL-10` (one line per page;
`x2` marks a spare).

- **Field names** [Verified on that fixture, a saved `/api/me` from Friday tick 159; current code still reads them]:
  `assets[].kind`, `assets[].ref`, `album.pages[].set/have/of`.
- [Uncertain] whether `album` changed shape since Friday. If it did, the command fails with a KeyError and prints
  nothing private.
- To hide spares, delete `+("x%d"%n[r] if n[r]>1 else "")`.

**Check before we trust it:**
- Σ`have` must equal their leaderboard `album_filled`, and the count of `have`=`of` pages must equal `pages_complete`,
  at the same snapshot.
- Every card the feed shows them holding must appear in HELD.
- t15's earlier report would have failed this check.

**Manual alternative:** send one line per set, e.g. `LAV 10/10 · MAL 8/10 missing MAL-09 MAL-10 · spares SAL-01x2`. We
apply the same leaderboard check, then add it to `run/known_holdings.json` (Lucas's file).

## Open items

1. **`GET /api/cards/{id}` needs a key.** Unkeyed, it returned `bad_key`, although the SDK lists it as public. The
   rules say each copy carries "a history of every hand it passed through". If it names the current holder, sweeping
   ids 1-~1,200 gives every team's exact holdings, including starting hands and pack pulls. One keyed test call settles
   it [Uncertain]. A full sweep uses the shared 5 req/s, so it needs the operator's slot.
2. The Workshop "keep one of each" rule vs. the t06/t14 anomaly [Uncertain].
3. Sunday: CHA makes `album_slots` 60. Re-run the arithmetic on each new snapshot.
