# SAL page: can we finish it today? (Builder, Sat 10:45, tick ~300)

_Scan of `data/feed.jsonl` (ticks 2-~300: settlements `frm`/`to`, pack.opened `best`, listings, bids, dealer threads),
the live boards (El Rastro + every open venue, keyless GET at 10:40), `intel/teams.md` (Dani, 10:22) and our
`/api/me` (10:42). Holders are inferred: starting cards and non-best pack pulls are invisible, so a team can hold a copy
we don't see. Ranks: leaderboard snapshot ~10:40 (we are **#4, 24.14**; top 4 = t18, t12, t02, us)._

## Where we stand [V, /api/me 10:42]

- Hold: SAL-01 ×2, SAL-02 ×2, SAL-03, SAL-05, SAL-08 (one copy). Missing: **SAL-04** (value 9), **SAL-06, SAL-07**
  (22.5), **SAL-09, SAL-10** (63, rares).
- **Cash 107 P.**
- **Our own v07 asks work against this page:** 4248 sells **SAL-08, our only copy**, to t03 at 27; 4253 (→ t06 at 9) and
  4322 (→ t03 at 40) offer **both** our SAL-01 copies. If the page is a goal, cancel 4248 and one of 4253/4322 (or
  drop them from `run/book.json`).

## Missing cards

| Card | Likely holders (rank; collects or dumps SAL) | Live asks | Recent prices | Cheapest realistic source |
|---|---|---|---|---|
| SAL-04 (c) | t08 #15 (listed it t285; dumps LAV), t04 #8 (listed t218; **dumps SAL**), t03 #10 (collects), t16 #14 (collects), t07 #17 (listed t159), t02 #3 **top 4** | none seen | Abuela sold at 9-10 (t127, t227 ×2) | **Abuela ~9-10** (dealer buy ≈ our value 9: ~0 score), or t04/t08 |
| SAL-06 (u) | Abuela (bought one back t132), t06 #12, t16 #14, t17 #9, t03 #10, t13 #6 (all collect SAL), t02 #3 **top 4** | none | Abuela 17-25; team trades 23-26 | **Abuela ~22-25** |
| SAL-07 (u) | t10 #7 (listed it t284; **dumps SAL**), t02 #3 **top 4** (live ask), t03 #10 (collects) | **t02 at 25** (El Rastro 4355, expires t314): top 4 | Abuela 21-23 (t87, t99 ×2) | **Abuela ~21-23**, or ask **t10** (dumper). Not t02: buying from a top-4 team pays them price − their value |
| SAL-09 (r) | **t13 #6** (bought at 74, t65; collects SAL), **t17 #9** (bought at 75, t109; collects SAL) | none | 74, 75 (the only two trades) | **No seller in sight.** Both holders collect SAL; 5 teams bid for it (t02, t03, t06, t08, t15) |
| SAL-10 (r) | **t01 #11** (live ask), t16 #14 (bought from Chato at 90, t266; collects), t13 #6 (bought at 70; collects), t18 #1 **top 4** (bought at 80; collects RET/LAT, not SAL), t17 #9 (listed t94) | **t01 at 76** (El Rastro 4288, expires t306) | 70, 72, 80 ×2 (teams); **Chato 90** | t01 at 76 (+5 El Rastro fee as taker: 81); 6 teams bid for it |

## Rare sellers at ≤ 60

None found. All six SAL rare trades ran **70-90** (teams 70-80, Chato 90). The only live rare ask is t01's SAL-10 at 76.
The one holder that doesn't collect SAL is t18 (#1, top 4): buying from it would feed the leader. Every other holder
collects SAL, and demand is high (5 bidders on SAL-09, 6 on SAL-10).

## Cost of the page at today's prices [L]

SAL-04 ~10 + SAL-06 ~23 + SAL-07 ~22 + SAL-09 ≥ 75 + SAL-10 ≥ 76 (81 with fee) ≈ **207-215 P**, against **107 P cash**.
The cheap part (04, 06, 07 from Abuela, ~55 P, roughly at our values) takes us to 8/10; the two rares cost ~150 P
at market, ~25 P above our values of 63 each before the page bonus.

**Is a SAL page buildable today with ≤ 170 P and rares from teams at ≤ 63? No** [L]: no rare has traded or is offered
at ≤ 63, the market is 70-90 with 5-6 bidders per rare, and our cash is 107 P.
