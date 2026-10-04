# Contrarian review: v10 real trades, Market Test, denial and Club Castizo (Sun 06:55)

_A contrarian reviewer with no prior context; read-only, no game API calls, no keys. Scope: `intel/sunday-final.md` stages 3, 6 and 7, plus the club plan. Read: sunday-final, market-sunday §0-§7, market-test-audit, holdings-audit, club-pitch, the club page source (`club-castizo.html`, v3), adversary-t10, audit-why-we-lost, RULES, directives (top). Checked against `data/feed.jsonl`, `data/me.jsonl`, `data/leaderboard.jsonl` (tick 1440), `agents/trader/loop.py`, `tools/policy.py` and `bazaar-kit/bazaar_sdk.py`. Labels: **[V]** read from data or code · **[L]** inferred · **[?]** open. Points are Sunday round points; × 0.4 gives final points._

## Verdict

- **The core plan holds.** v10 hosts deals between other teams, both sides gain at their own values, quotes are addressed and agreed first, and there are no payments. That is what market-making is meant to reward, and the deck says so ("finds the missing card, swaps without cash, finishes pages"). **Keeping the stall is right**, for a stronger reason than the plan gives (#6).
- **Four fixes before 09:00:**
  1. Give RET-09 a fallback seller, and send it alone, not bundled with the reverse SAL-02 deal (#1).
  2. Stop the trader from accepting offers on rival venues (#2). The code allows it today, against stage 7.
  3. Take out the wording that reads like points-sharing ("lowest market score first", "club markets only"), and disclose the design to the desk instead of asking the Market Test question (#3).
  4. Invite open listings on v10 only after RET-09 has settled (#4).
- **No approved pair hands a rival a page close.** The buyers are t09 (#16), t07 (#17), t16 (#14) and t08 (#11) [V leaderboard 1440, holdings grids]. The leaks to rivals run through other channels: the trader daemon, open asks taken by fast rival bots, and the members' open-buy rule.
- **The WhatsApp texts don't leak the formula.** They do bundle a two-way deal between the same pair of teams, which looks like a round trip, and they anchor a price that doesn't affect our value created (VC) at all.
- **What the fixes are worth:** ≈ +2.5-4.5 Sunday points expected (≈ +1.0-1.8 final), most of it in #1 and #2.

## Issues ranked by expected Sunday points

| # | Issue | EV of the fix (Sunday pts) | Fix (owner, when) |
|---|---|---|---|
| 1 | RET-09 is a single point of failure: no fallback, a reciprocal pair, a price anchor that doesn't matter | **+1.0-1.8** | Hold row 6 as RET-09's fallback; send RET-09 alone; post SAL-02 ≥ 60 min later or drop it; close at any price (Lucas, Dani, 08:30) |
| 2 | The trader accepts offers on rival venues (v18 t18, v20 t03, v02 t12, v01 t06, v07 t10, …) [V code] | **+0.3-1.0** (denial; can decide #2) | Skip every offer whose venue owner is a rival, including offers addressed to us (Builder, before the 09:00 restart) |
| 3 | Fair-play optics: score-allocating rotation, "members-only" exclusivity, zero-gain accept rule, holdings posted in the group, a cash bonus still marked "fixed" in market-sunday §3 | **+0.4-0.8** (+ the judges' story) | Desk disclosure at 08:45; reword the page (v4) before it is shared; strictly positive gains in the bot rule; strike §3's bonus line (Chief, Lucas) |
| 4 | The open shelf on v10 is invited before any buffer exists; page-card dumps and fast rival bots | **+0.3-0.6** | No open-shelf invitations and the open-buy rule off until RET-09 settles; t07 posts addressed-only on v10; only rival-proof spares open (Market, Operator) |
| 5 | The 1-in-3 rotation sends VC to markets that never reach the top three, so it does nothing to cut t10/t06/t14 | **+0.2-0.5** | Host on the market whose matcher found the pair (all of ours on v10) (Lucas) |
| 6 | Market Test: the desk question can't change our decision and may help rivals if broadcast | **0 to +0.2** | Keep the stall. Drop the question, or ask it after the club disclosure |
| 7 | Members' open listings feed rival venues (t08 204 on v07; t07 94 on v02) | **+0.1-0.4** | One line to t08 and t04: "for spares with no agreed buyer, v10 is 0% and crosses every tick". Not to t07 (see #4) |

---

### 1. RET-09 is the plan's single point of failure (a, b, e)

**Facts:**
- RET-09 t07 → t09 carries v10's real trades: +156 of +231 matchmaker VC [V matches.md 06:44].
- Its estimate moved +68 → +134 → +156 across runs [V market-sunday §2].
- t09 is the team most likely to haggle: 16 counters of 121 [V §0.2]. Its highest live bids for rares are 56 [V holdings-audit].
- t07 is slow (median wait 20.5 ticks) [V §0.2].
- Without RET-09, the rest of the list scores 24-94% of full marks (market-sunday §6) [L].
- **P(row 1 slips past the first hour or fails) ≈ 25-35% [L].**

**Breaks found:**
1. **No fallback.** The only other traced spare RET-09 is t08's: one copy, and t08's RET page is incomplete, so selling it breaks nothing [V holdings grids]. Row 6 already sends that copy to t16 (+23.7). If row 6 fires first, t09 has no second source.
2. **Reciprocal pair.** RET-09 t07 → t09 and SAL-02 t09 → t07 go between the same two teams, in opposite directions, in the same hour, on the same third-party venue. The 08:30 texts even bundle them ("Dos cosas…").
   - RULES: deals where one team "keeps handing another the whole value … count for nothing until the organisers have looked".
   - A round trip is the shape any automatic filter would catch. SAL-02 adds only +6.5 VC; RET-09 is the whole day [L, P ≈ 3-5%, stake 7.5].
3. **The price anchor doesn't matter to us.** VC = buyer's value − seller's value; the price cancels out [L, market-test-audit §2]. Any price inside both values scores the same on v10.

**Fix:**
- **08:30:** send the RET-09 texts **alone**: split the "Dos cosas" messages, and say "~70-80 P, you two agree the price".
- **Commit t08 at 08:30 as well.** Lucas → t08: "There's a buyer for your spare RET-09 on v10 this morning: please hold it for half an hour." This also takes the copy out of reach of t10's v07 ad bot.
- **Hold row 6 until row 1 settles.** If row 1 has no listing by 09:20, or no fill by 09:40, re-route t08's copy to t09 on v10 (directive 21:40 had this pair at ≈ +134), and t16 drops out.
- **SAL-02:** post it no earlier than 60 minutes after RET-09 settles, or drop it. If t07 still wants SAL-02, look for another seller in the shared lists.

### 2. The trader daemon trades on rival venues [V code], against stage 7 (f)

**What the code does:**
- `agents/trader/loop.py` `gather()` reads "every open public board but our own venue's" (lines 129-153).
- `candidate()` only raises the bar to 15 P when the venue owner is top-4 (lines 359-360). For t03, t06, t13, t14 and t17 the bar stays at `--min-gain` (default 3).
- The rival check (`feeding_skip`, `policy.check`) looks at the **counterparty**, never at the **venue owner**.
- The 09:00 restart (`CASH_FLOOR=464`, ≈ 78 P to spend, plus the spare sells) will scan these boards: v18 (t18), v20 (t03), v02 (t12), v01 (t06), v07 (t10), v25 (t14), v24 (t13), v17 (t17) [V feed venue.opened].

**Why it matters:**
- Saturday's precedent: our single SAL-01 trade on v07 at tick 351 took t10's market from 7.50 to 11.84 on the board [V audit-why-we-lost §4.2].
- t18 and t03 have ≈ 0 VC, so any positive trade on v18 or v20 is pure gain for them. One +10 VC trade on v18 at M ≈ 40-60 ≈ +1.2-1.9 Sunday points for t18 [L]. That is about the whole #2 gap (0.46 final ≈ 1.15 Sunday points).

**Fix (≈ 5 lines, Builder, before 09:00):**
- In `candidate()`, after `owner` is known: `if owner in policy.rivals(teams) | policy.RIVALS | FIXED: skip "rival's venue"`, with `FIXED = {t10, t18, t12, t03, t06, t14, t13, t17}`. Apply it to offers addressed to us too, because those settle on the rival's venue.
- Reword stage 7 from "no trades on v07" to "**no trade of ours on any rival-owned venue**".
- Check that `book.py`, `swaps.py`, `opportunities.py` and the dealer bots post only on El Rastro or non-rival member venues. Their defaults are v15 or El Rastro [V directive 17:30, opportunities.md header].

### 3. Fair play: legit core, gray wording (c)

**What's clearly fine:**
- Matching, hosting, agreed and addressed deals, positive for both sides, at 0%, with no payments.
- Hosting is not feeding: Team 5 hands nobody any value.
- Seven other teams advertise matching too: t02, t03, t04, t06, t10, t12, t14 [V feed announcements].

**What could read as collusion to an organiser, or to a judge who is told about it:**

| Element | Why it looks bad | Fix |
|---|---|---|
| "Rotation: lowest market score first" (page, club-pitch §1-3) | Team 5 allocates venue score to members, weakest first. That is points-sharing in exchange for membership, and the deck says "friends count for nothing" | **The market whose matcher found the pair hosts it.** Ours go on v10. t02/t04 host what their own matchers find. No score-based order |
| Team 5's own trades "always on members' markets, lowest score first" | Same allocation | "On a 0% market the counterparty picks (not its own); never a rival's" |
| "Club markets only", "No club deal goes to the market of a team outside the club", "members" | Reads as an exclusive cartel | Call it the **Castizo matching desk**: open to any team that sends a list. We choose whom we contact; no exclusivity clause |
| Bot rule BUY: `your_value − price ≥ 0`; SELL: `price ≥ your_value` | Allows zero-gain deals where one side gets the "whole value", the exact RULES trigger | BUY: `price ≤ 0.9 × your_value`; SELL: `price ≥ your_value + 1`. Every deal visibly two-sided |
| "Paste the output in the group" (holdings list) | Broadcasts every member's exact holdings to six teams; one forward reaches t10. Contradicts club-pitch §2 ("never repost them in the group") | "Send it privately to Lucas or Dani" |
| market-sunday §3 still says "Incentive is fixed by the directive (Club Castizo, Sat 22:55): seller's bonus … cap 15 P per team per day" | Anyone reading §3 pays per-deal cash: paying for activity, the clearest fair-play own goal | Strike the line and mark it VOID (sunday-final: "no cash bonuses") |
| club-pitch §0/§1 says "≈ 50/50"; the page says "2 of 3"; club-pitch §3's venue plan differs from market-sunday §0.5 | Three versions of the rule; a member who compares them sees moving goalposts | One source: the page plus §0.5. Mark club-pitch §1 and §3 as superseded |

**Disclosure beats defence.** Use Lucas's desk minute at **08:45** (09:00 is CHA t+0 and the clock check) for this question:

> "Our free stall v10 will host card deals we match between other teams: each one agreed by both teams in a WhatsApp group, positive for both at their own values, addressed, 0% fee, no payments of any kind. Is that fine, including when the same few teams trade several times on it during the day?"

- A yes makes the design pre-approved and disarms t10's complaint (adversary-t10 §1.4 #7).
- A no costs nothing yet: nothing has been posted.
- It also gives the judges the "matching engine market" story, which is worth more there than a "club".

### 4. The open shelf before the buffer: negative VC and fast rival bots (b, f)

**Facts:**
- A stall crosses whatever is posted; it cannot refuse a fill.
- On Saturday, page-card or only-copy fills wiped 3 of the ~10 venues that had trades: ours (t10's SAL-07 at tick 398), t12's (two t07 dumps at 910), and t07's own [V market-sunday §0.7, audit §3].
- Two of the teams we pull toward v10 have dumped before: **t07** (club member and RET-09 seller) and **t06** (fell from #2 to #6 on a page-card sale).
- §0.7 invites heavy listers, including t06 and t13, to post open on v10.
- The page's optional open-buy rule makes members' bots buy any open v10 ask at ≤ 0.8 × value. Board makers are pseudonyms [V loop.py line 157 comment], so a member's bot can't tell a rival or a dumper from a club seller. A rival's spare sold to a member's bot gives that rival trade points.

**Fix:**
1. **No open-shelf invitations, and the open-buy rule off, until RET-09 has settled on v10.** The buffer absorbs a −10 to −20 dump [L, Saturday sizes]; a v10 with only +7 VC does not.
2. Ask t07 for **addressed, agreed offers only on v10**: no open spray there.
3. **Our own open spares only when rival-proof** [V holdings grids]:
   - LAV-03 is held by every rival. LAV-02 is held by t06, t13, t14 and t18; t03 is undecided.
   - **LAT-03** is lacked by t06 and t10; **LAT-04** by t13; **LAV-04** by t18. Post those addressed to a member buyer, or not at all.
   - Market-sunday §0.4 posts LAT-03/04 open at 6.
4. Every v10 fill gets logged with mm before → after within one tick (already in §5), with a hard stop on the open shelf after the first negative fill.

### 5. The rotation wastes denial (a, e)

- A VC unit raises M (the top-three mean) only on a venue that is in the top three.
- Members at the bottom of the rotation won't get there. So a third of club VC does nothing to t10's v07, t06's v01 or t14's v25 [L].
- The 01:10 directive's own figures: t10 keeps ≈ 83% at 50/50 and ≈ 69% at 2/3. All of our matches on v10 keeps it lower still [L].
- Fix #3's "the market whose matcher found the pair hosts it" gets both the clean optics and the denial.
- If Lucas keeps the 2-of-3 split for recruitment, rotate by **the two members with real activity** (adversary-t10's "pyramid": v21 and v06), not lowest score first. That way some member VC can still push v07 out of the top three.

### 6. Market Test: keep the stall; the desk question can't change it (d)

- **A decisive reason the plan omits [V feed]:** opening any venue **replaces the stall under a new id**: v08→v19, v09→v20, v12→v21, v14→v25 (`venue.closed … "replaced": true`). Our pending addresses would all be orphaned: every WhatsApp text, the club page, the members' bot rules and the open offers on v10. v10's real-trades VC probably would not follow either [?]. So even a desk "yes, any edge gets full points" cannot flip the decision. Add 270 P locked against CHA/MAL, a broker with no real-data edge, and 0 wins in 51 rival sessions [V audit §1a].
- **Information hazard:** if the desk broadcasts the answer, rivals with board brokers (t10, t06, t12, t03, t13) can tune for it, and we can't [L, small].
- **Cheap ways to beat the stall:** none found.
  - Every venue gets the same synthetic book: 10-12 traders, 16 ticks, one good [V bench files].
  - Every auto venue therefore scores the same efficiency.
  - A broker's only lever is timing, which the sims put at ≤ 15% wins and negative in the linear reading.
  - Do not touch the bench book with real orders. Venues can be suspended and the bond cut.
- **Fix:** drop the Market Test question, or ask it after the disclosure question as a RULES clarification: "When only one venue beats the stall's efficiency in a session, is its score capped at full?"

### 7. Members' open listings feed rival venues (f)

- On Saturday, t08 posted 204 listings on v07, and t07 posted 94 on t12's v02 [V audit §5.1].
- v02 built t12's VC (11 fills) before t07's dumps wiped it. t12 is 0.04 final behind us.
- **Fix:** one line in t08's and t04's messages: "For spares with no agreed buyer: v10 is 0% and crosses every tick." It's an invitation, with no boycott and no promise of flow.
- Leave t07's open spray where it is (#4).

---

## (a) The real-trades formula: what if it's wrong?

The fit, 7.5 × min(1, VC / top-3 mean), is strong on the cap structure:
- the leader is always at the cap;
- two venues are at the cap at once in 6 windows, never three;
- negative totals floor at 0.

Each attack, and what it changes:

| Attack | Status | Effect on the plan |
|---|---|---|
| Matchmaker units ≠ scoring units (+68…+156) | [?] | A page closer is ≥ 50 mm units even at a low t09 RET multiplier [L, from our SAL-06 closer at 82.1 value]. That is ≥ 3× Saturday's M ≤ 15 |
| Sunday's M is larger: 15 s ticks, +150 P, CHA page closers hosted on v07 or member markets | [L] | **P(RET-09 alone gives full marks all day) ≈ 0.6-0.75, not "likely full alone".** Keep 3-4 more positive pairs flowing; "no VC stop" stays |
| VC re-evaluated at current holdings: mm went −5.2 → +2.2 with no new v10 trade [V me.jsonl ticks 474 → 1445] | [?] | A buyer that later gets a second copy elsewhere shrinks VC. Low risk; another reason to keep stacking |
| VC carries over between rounds (Saturday's `round.started` shows `"reset": false` [V feed]) | [?] | Rivals' Saturday VC would count again; RET-09 still dominates. Ask nobody: it changes nothing we do |
| Top-4+ mean instead of top-3 | not excluded [L] | Same direction; a lower bar for us |

- **Case A (Saturday tail first, ≈ 15%):** firing RET-09 in the tail is right, and better than the plan says. Saturday's M is ≤ 15, so +68-156 on v10 would cut t06's +6.55 and t10's +7.5 Saturday real trades to roughly a quarter or less [L]. That is the biggest single denial move available against t06.

## (b) Pairs and texts

**Pairs:**
- No approved row gives a rival a page or big points [V].
- RET-09 closes t09's RET page, but t09 is ≈ 10.8 game points behind us [V club-pitch §2].
- Row 6 must wait (#1).

**Texts:**
- No formula, no top-three mean, no rivals named [V §0.5].
- To fix: the bundled two-way t07/t09 messages (#1); the "~76" anchor (#1); club-pitch §4 invites name all seven teams and markets, so one forward gives t10 the poaching list (send the roster only in the group opener, after joins); and the group holdings paste (#3).

## (e) Team 10's counters and our response

| t10 counter | P [L] | Response |
|---|---|---|
| v07 ad bot turns public needs (t09's RET-09 bids) into "list on v07" pairs; t08's copy goes to v07 first | 0.3 | Commit t08 at 08:30 (#1); first-tick posting; addressed offers can't be intercepted |
| Poaches members' flow: bids on v07 for their spares; their bots already spray v07 | 0.5 | Don't outbid. RET-09 on v10 makes v07 secondary. Invite t08 and t04 to v10 (#7) |
| Complains to the desk ("closed club, feeding") | 0.15 | Pre-empted by the 08:45 disclosure plus #3's wording |
| Negative-VC fills on v10 (itself or via t01) | 0.1 | Buffer first (#4); log every fill; a factual note to the desk if it happens twice; never retaliate |
| Copies the matching service with more cash | 0.3 | Our edge is speed plus private lists; members gain either way; never promise flow |
| Sells MAL-09/10 to t09 through the members' open-buy rule on v10 | 0.2 | The open-buy rule stays off at the open (#4); "no deal with t10 as a party" only binds us |

## (f) Anything else that lifts t10/t18/t12/t06/t03

- The trader on rival boards (#2) is the main one. It is the only channel that reaches **t18 and t03**, our closest #2-#5 rivals, through the market.
- Fast rival bots (t06, t13, t14) taking our non-rival-proof open spares, or a third party's spares (#4).
- Members' listings on v02 and v07 (#7).
- Out of scope, one line: the public CHA bids at the dealer price can be filled by rivals selling low-multiplier CHA copies, which is a trade gain for them. The fodder and CHA books should prefer dealer fills and member sellers.

_Verification: every [V] claim above was re-read from the cited file or code line in this pass. An independent verifier pass is noted in the handback._
