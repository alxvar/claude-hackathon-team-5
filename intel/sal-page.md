# SAL page: can we finish it today? (Builder, Sat 11:05, tick ~300; independently verified)

_Scan of `data/feed.jsonl` (ticks 2-~300: settlements `frm`/`to`, pack.opened `best`, listings, bids, dealer threads),
El Rastro's live board (`data/board.json`, 10:45), `intel/teams.md` (Dani, 10:22) and our `/api/me` (10:42). Holders are
**visible** holders only: starting cards and non-best pack pulls are invisible (rares print 30; we see SAL-09 serials #1,
#4 and SAL-10 #2-#7). "Collects" (teams.md) means buys or bids for a set, not "won't sell". Ranks: leaderboard at tick
290 (we are **#4, 24.14**; top 4 = t18, t12, t02, us)._

## Where we stand [V, /api/me 10:42]

- Hold: SAL-01 ×2, SAL-02 ×2, SAL-03, SAL-05, SAL-08 (one copy). Missing: **SAL-04** (value 9), **SAL-06, SAL-07**
  (22.5), **SAL-09, SAL-10** (63, rares).
- **Cash 107 P.**
- **Our own v07 asks work against this page:** 4248 sells **SAL-08, our only copy**, to t03 at 27; 4253 (→ t06 at 9) and
  4322 (→ t03 at 40) offer **both** our SAL-01 copies. If the page is a goal, cancel 4248 and one of 4253/4322 (or drop
  them from `run/book.json`).

## Missing cards (visible holders)

| Card | Visible holders (rank; collects or dumps SAL) | Live asks | Recent prices | Cheapest realistic source |
|---|---|---|---|---|
| SAL-04 (c) | t08 #15 (listed it t285; dumps LAV), t04 #8 (listed t218; **dumps SAL**), t03 #10, t16 #14 (both collect SAL), t07 #17 (listed t159), t02 #3 **top 4** | none takeable (t08's are addressed to t14, t01) | Abuela sold at 10 (t127), 9 and 9 (t227) | **Abuela ~9-10** (≈ our value 9), or t04/t08 |
| SAL-06 (u) | Abuela (bought one back at 14, t132), t06 #12, t16 #14, t17 #9, t03 #10, t13 #6 (all collect SAL), t02 #3 **top 4** | none | Abuela 17-25; team trades 23 and 26 | **Abuela ~22-25** |
| SAL-07 (u) | t10 #7 (asks 29-34 since t127; latest 29 to t03 on v10), t02 #3 **top 4** (live ask), t03 #10 | **t02 at 25** (El Rastro 4355, expires t314): top 4 | Abuela sold 21-23 (t87, t99 ×2); her latest quotes 26 then 25 (t166-167); no Abuela sale since | **Abuela ~25** (stock unknown). Not t10 (29+); not t02: buying from a top-4 team pays them price − their value |
| SAL-09 (r) | t13 #6 (bought at 74, t65), t17 #9 (bought at 75, t109), both collect SAL | none | 74, 75 (the only two trades) | **No visible seller.** Bids seen: t03 74 to t17 (t216), t06 53, t08 23-62, t02 8, t15 7; none since t216 |
| SAL-10 (r) | **t01 #11** (two copies: live ask, and one bought at 72, t163), t16 #14 (bought from Chato at 90, t266), t13 #6 (bought at 70), t18 #1 **top 4** (bought at 80; collects RET/LAT, not SAL), t17 #9 (listed it at 125, t89/t94) | **t01 at 76** (El Rastro 4288, expires t306) | 70, 72, 80 (teams); **Chato 90** | t01 at 76 (+5 El Rastro fee as taker: 81). Bids: no cash bid since t195 (t12's was 34) |

## Rare sellers at ≤ 63

None visible. All six SAL rare trades ran **70-90** (teams 70, 72, 74, 75, 80; Chato 90). The only live rare ask is
t01's SAL-10 at 76 (t01 collects SAL and sells anyway; t17 also listed one, at 125). Current demand is not shown to
be high: no SAL-09 bid since t216, no SAL-10 cash bid since t195. A holder might take less than 70 if asked, but
nothing in the data says so.

## Cost of the page at today's prices [L]

SAL-04 ~10 + SAL-06 ~23 + SAL-07 ~25 + SAL-09 ≥ 75 + SAL-10 ≥ 76 = **≥ 209 P**; **≈ 214-219 P** with El Rastro's taker
fee on the rares (5 P each), against **107 P cash**. The cheap part (04, 06, 07 from Abuela, ~58 P, about our values of
54) takes us to 8/10; the two rares cost ~151 P at market, ~25 P above our values of 63 each before the page bonus.

**Is a SAL page buildable today with ≤ 170 P and rares from teams at ≤ 63? No** [L]: no rare has traded or is offered
at ≤ 63 (lowest trade 70, live ask 76), the page costs ≥ 209 P, and our cash is 107 P.
