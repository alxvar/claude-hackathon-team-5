# Contrarian review: CHA page, MAL close, ladder fodder, cash (Sun 07:15)

_Contrarian reviewer, no prior context. Read-only, no game calls, no keys. Scope: `intel/sunday-final.md` stages 1, 4 and 5 and the
cash plan, **as armed at 07:04**: `run/sunday/t0.sh` (pid 92570), `run/book.sunday.json`, `run/floors.env`, directive 07:05.
Read: sunday-final, dealer-lab (§2, FAST-START), dealer-lab-ladder (§1, §5-6), cha-plan, run/cha_book.json, mal_book.json,
book_cha_entries.json, score-model §4.6-4.13, live-tuning, directives (top), sunday-redteam, adversary-t10, contra-ops,
contra-market (skimmed), RULES, GAME.md. Checked against `data/feed.jsonl` (Fri-Sat, to tick 1445), `run/sunday/simple_buy.py`,
`run/sunday/t0.sh`, `agents/trader/loop.py`, `agents/trader/book.py`, `tools/opportunities.py`, `tools/policy.py`.
Labels: **[V]** read from data or code · **[L]** inferred · **[?]** open. Points are Sunday round points (× 0.4 = final).
Updated 07:35 after an independent verification pass (feed stats, code and arithmetic re-run; corrections applied) and after
directive 07:25 adopted most fixes._

## Status at 07:35: adopted, and still open

**Adopted (directive 07:25, t0.sh re-armed at 07:14:32 as pid 15531 on the new file [V lsof]):**
- #1 per-thread caps 57 → 60 → 62, reopening only after a logged walk;
- #2 closers on El Rastro;
- #4 LAV asks dropped, the Workshop at C, LAV-04 → the Pícaros;
- #5 MAL out of the chain;
- #6 floors at 110;
- #7 Abuela commons from C+5;
- #8 the sink order;
- #9 the t10/t01 watcher;
- #10 simple_buy retries and the last-card guard; CHA-09/10 public only at C+60.

**Still open (review of the new t0.sh / simple_buy.py):**
1. **The Chato fallback fires on anything that isn't a logged walk** [V t0.sh lines 77-81]:
   - A Pícaros run that ends by deadline counts, and so does a trick-guard stall. simple_buy waits on a bait-and-switch offer
     until it expires. The Pícaros bait and switch in ≈ 15-22% of offers [L dealer-lab-ladder].
   - Both send the rare to Chato ≤ 100: no L4 slot (Chato's rare finals are 77-93 [V feed, n = 31]).
   - A run that offered the Pícaros' price, where the deal hasn't settled within 15 s (an organiser pause), also goes to Chato.
     That can buy a **2nd copy at ≈ 77-93, worth 28: ≈ −50 to −65 np** counted in full.
   - **Fix:** if the log shows `offer_their_price`, poll `held` for 2 min before doing anything else. Go to Chato only on
     `closed_reason` `sold_out` or `persona_quota`, or when the thread can't be opened. On a deadline or a trick stall, reopen
     at the Pícaros at the same cap.
2. **The last-card guard runs only at start** [V simple_buy.py:50-53].
   - A public fill of another CHA card mid-thread can make this card the last one, and the dealer deal then closes the page
     without the bonus.
   - **Fix:** re-read `/api/me/value` just before `offer_their_price` and walk if it is above base + 1.
3. **The closer still has no seller (#3).** 07:25 covers the venue but not the relay.
   - sunday-final still says "pre-agreed", which can't happen at 08:30: nobody holds CHA before C.
   - Either ask one non-rival member at 08:30 to buy CHA-05/08 at Abuela at C and hold them, or accept the 09:15 feed search.
     The search sees only dealer buyers, because pack pulls are hidden.
4. **t15's MAL-07** should stay unlisted until we bid (#5, g). An ask addressed to us is still visible in the feed, and t10
   needs MAL-07.
5. **Docs:** sunday-final stage 1 still says "10 public bids … 54". t0 posts 8, plus CHA-09/10 only at C+60 if a rare is
   missing. Doc only.

## Verdict per stage

| Stage | Verdict | Why |
|---|---|---|
| **1 CHA page** | **GO, with 4 changes** (#1, #2, #3, #7) | The rare chain is stricter than the Pícaros' measured finals. The closer has no seller at 09:00 and no venue rule. The Abuela window can't finish the page before Duels III |
| **4 MAL close** | **NO-GO at 09:00. Re-decide at ≈ 12:00 on M5** (#5) | At ≤ 49 it can't fill: 0 of 8 Saturday Pícaros MAL rare finals and sales were below 57. In the chain it only blocks the Pícaros. Relaxed, it's worth ≈ +17-28 np, and only while our trade part is live |
| **5 Fodder** | **GO, re-allocate the LAV spares** (#4) | Most of the value is one Pícaros common sale (an L4 slot nobody has scheduled), plus the pack and the Workshop. The LAT bids are lottery tickets. Two staged LAV asks eat the Workshop's inputs |
| **Cash** | **No overspend path. The risk runs the other way** (#6, #8) | The trader and opps floors count our open CHA bids twice, so both stay inert all morning. ≈ 300 P will sit idle at 15:00 |

Combined, the fixes are worth ≈ +2-5 Sunday points (≈ +1-2 final) [L; the ranges overlap and are not additive].

## Issues ranked by expected points (EV midpoint, weighted by evidence: #1 rests on [V] data; #2's size hinges on a [?])

| # | Issue | EV of the fix | Fix (owner, when) |
|---|---|---|---|
| 1 | The Pícaros chain stops at cap 57 after two threads; Saturday finals sit mostly at 55-60 | +0.4-1.0 | Per rare: thread 1 ≤ 57, thread 2 ≤ 60, thread 3 ≤ 62 (always < list 63). Reopen only after a logged walk (Operator, before the 08:45 re-arm; band change = Chief) |
| 2 | Our page closers routed to a member market (MAL-07 on v26 since 06:43; the CHA closer would follow the club rule) | +0.2-1.5 | Every closer of ours goes on El Rastro, addressed, with the seller's fee added to our price (Chief, now) |
| 3 | The CHA closer has no seller at C and lands ≈ 12:45-13:45 | +0.3-0.8 | 08:30 relay with one non-rival club member: it buys CHA-05 and CHA-08 from Abuela at C and sells both to us by addressed El Rastro bids at cost + 5-8 (Lucas/Dani, 08:30) |
| 4 | Pícaros L4 slot 3 is unscheduled; 4 LAV spares are booked for 7 uses | +0.3-0.7 | Drop both staged LAV asks. LAV-04 → Pícaros right after the CHA rares. LAV-02, LAV-02, LAV-03 → Workshop at C (Operator, before 08:45) |
| 5 | The MAL legs in t0.sh can't fill at ≤ 49 and hold the Pícaros 10-28 min | +0.2-0.8 | Delete the MAL loop from the chain. At ≈ 12:00, if M5 is live: relaxed MAL (Pícaros ≤ 60, t15's MAL-07 confirmed first, closer on El Rastro), with a GUARDRAIL line. Else drop it and its 126 P (Chief) |
| 6 | Trader/opps floors 464 double-count our open bids | +0.2-0.6 | Floor = planned spend not already in open bids + 50 ≈ 80-122 at R+10; 0 at 13:30 (Operator) |
| 7 | Abuela window 10:00-10:40 is too short for 6 cards | +0.2-0.5 | Commons CHA-01..03 at Abuela from C+5, in parallel with the Pícaros. Uncommons and CHA-04 stay public until C+45, then Abuela (Operator) |
| 8 | ≈ 300 P strands at 15:00 | +0.1-0.5 | 12:00 sink order: floors → relaxed MAL if live → ladder upgrades ≤ value → non-rival asks ≤ value − 10 (Chief) |
| 9 | Public CHA bids pay a duplicate holder almost as much as us, and t10 can fill them | +0.1-0.4 | Cancel the public bid for any CHA card the feed shows t10/t01 holding; pull all public CHA bids once M5 says capped (Operator) |
| 10 | Small: unguarded simple_buy calls, no last-card guard, public rare bids during the chain, a no-CHA-stock fallback | protective | §10 |

---

### 1. The CHA rare chain is stricter than the Pícaros' finals (a, b)

**Facts.**
- Saturday Pícaros **finals** on rare buy threads (non-MAL, n = 23) [V feed]:

  | Final ≤ | 54 | 57 | 60 | 62 |
  |---|---|---|---|---|
  | Share of finals | 17% | 52% | 96% | 100% |

  - Settled non-MAL rare buys (n = 47): 32% at ≤ 54, 68% at ≤ 57, 89% at ≤ 62.
  - Finals are close to binding: teams beat a dealer's final in 7 of 183 deals [V dealer-lab-ladder §0.4].
- The 07:04 t0.sh ran `B 42 54`, then, if the card wasn't held, `B 42 57`, then the next card [V].
  - P(per rare) ≈ 0.52-0.78 (the low end assumes a card's final carries over between threads).
  - **P(both rares) ≈ 0.3-0.6.**
  - So about half the time a CHA rare would still have been missing at ≈ 09:30, with nothing saying what comes next.
  - Chato's rare finals run 77-93 (n = 31) [V feed]: at or above list 77, so a Chato rare carries no ladder slot.
- The walk buys little share:
  - The same price of 54 gave shares of ≈ 0.79 (SAL-09, +0.070) and ≈ 0.71 (SAL-10, +0.063). The ladder moves are [V
    dealer-lab]; the shares are derived as Δ / 0.089 [L].
  - So the range is per conversation [L]: a final taken near its own limit keeps most of the share.
  - Every price ≤ 62 is below list 63 (the ladder counts it) and below our value of 112 (0 np).
- Print runs are global, 30 per CHA rare. SAL-09 hit 29/30 in one day [V redteam §1.2]. A slow chain risks the card itself, not just
  the share.

**Fix (Operator before the 08:45 re-arm; the cap change is outside the live-tuning band, so the Chief signs):**
- Per rare: thread 1 accepts ≤ 57, thread 2 ≤ 60, thread 3 ≤ 62 (thread 3 only before 10:00). Walk only on a final above that
  thread's cap. Never above 62.
- **Reopen only if the previous run logged `walk` or `deadline`**, never after `offer_their_price`.
  - A deal waiting to settle during an organiser pause reads as "not held".
  - The reopen would then buy a 2nd copy at ≤ 57, worth 28: −29 np counted in full [L, edge case].

### 2. Our page closers must settle on El Rastro, not on a member market (c, g)

- At 06:43 MAL-07 moved to an addressed bid on **v26** (Team 2's market), under the club rule "member trades settle on member
  markets" [V lucas.md]. The CHA closer has no venue in sunday-final, so the same rule would send it to a member market.
- How real trades score: 7.5 × min(1, VC / M), where M is the mean of the top three venues [L strong, market-test-audit §2].
  - A page closer is ≥ 50 mm units [L, contra-market].
  - Ours for CHA would be ≈ +100 (122 to us, minus the seller's ≤ 16) **if VC counts the page bonus [?]**.
  - Saturday's M was ≤ ≈ 15. v10's Sunday target is 40-50.
- One such trade makes the host market the top VC venue and lifts M past v10.
  - Example: v26 at 100, v10 at 45, v07 at 40 → M = 62 → v10 earns 0.73 of its 7.5, **−2.0**.
  - It also cuts v07, but we race for #2-#5, not #1.
- **Fix:**
  - Every trade of ours that closes a page goes on **El Rastro**. It has no owner, so it adds no VC to anyone.
  - The seller pays 5% + 1 P (2-3 P at these prices) [V GAME.md]: add that to our price.
  - Revert the 06:43 line in dealer-lab FAST-START and tell t15.
  - This matches sunday-redteam §2C: "big trades of ours go to El Rastro".

### 3. The CHA closer has no seller at C and lands too late (a, c)

**Facts.**
- Nobody holds a CHA card at C: minted 0.
  - The feed names dealer buyers by team.
  - `pack.opened` shows only `best` [V feed], so a pulled common or uncommon is invisible.
  - So contra-ops' 09:15 search ("which non-rival pulled CHA-05/08") can only find dealer buyers.
- As armed, the pair (CHA-05/08) waits for team fills, then CHA-08 from Abuela at 12:30 (cha-plan step 4), then the closer.
  - That lands ≈ 12:45-13:45.
  - The dealer warning is at 13:48 and the Final's T−5 freeze at 13:55.
  - Saturday paused for 47 min and for 2 h 05 [V redteam §1.1].

**Fix (Lucas or Dani, one WhatsApp at 08:30): a relay with one club member that says Chamberí is a low set for it.**
- At C it buys CHA-05 (≈ 9) and CHA-08 (≈ 21) from Abuela, out of its own allotment.
- It holds both off-market: no listing, and no fill of our public bids.
- It accepts two addressed El Rastro bids from us when we signal: the non-last card at cost + 5, the last at cost + 8.
- The page closes ≈ 10:30-10:45, and no Abuela thread runs at 8/10 or 9/10, so no gift or dealer can deliver the last card.
- **Don't pay "up to 72".** Any price ≤ 72 scores the same +50 for us. A 72 P common hands the seller up to +50 np and looks
  like feeding (RULES, fair play).
- Keep the public CHA-05/08 bids at 9/22 anyway.
  - A public fill of the last card at the dealer price still scores +50 for us.
  - Nobody can flip into it: the seller nets 7 or 19 after the fee.
  - sunday-final's "never public" should read "**never above the dealer price**".
- [?] If the per-trade cap is 5 × book (GAME.md, still open), an uncommon closer scores up to 124, not 50. Where the relay
  makes it just as easy, let CHA-08 be the last card.
- If organisers ban alliances (directive 18:40 contingency), drop the relay and fall back to the 09:15 feed search.

### 4. Fodder: Pícaros L4 slot 3 is unscheduled, and the LAV spares are over-booked (e)

- **Spares and uses.**
  - We hold 4 spares: LAV-02 ×2, LAV-03, LAV-04 [V dealer-lab-ladder §6.2].
  - They are booked for 7 uses:
    - the Workshop (3);
    - a Pícaros sale (dealer-lab §2 #3);
    - an Abuela sale (§2 #8);
    - two addressed asks still staged in `run/book.sunday.json`: LAV-03 → t04 at 6 and LAV-04 → t01 at 9 [V]. t01 is t10's
      reported ally.
- **The slot.**
  - A Pícaros common sale at 5 fills an L4 slot. SAL-04 at 5 gave +0.043 [V], half a full L4 slot.
  - No file schedules it: it isn't in t0.sh, contra-ops' timetable or sunday-final stage 5.
  - If the MAL legs fail (#5), L4 slot 3 stays **empty and counts 0** (RULES).
- **Fix (one edit of `run/book.sunday.json` before 08:45):**
  - Drop both LAV asks (cancel 19979/19981).
  - LAV-04 → the Pícaros right after the CHA rares: `dealer_sell.py`, offer-only, open ≈ 12, −1, floor 5.
  - LAV-02, LAV-02, LAV-03 → the Workshop at C+1 min. Every CHA card is missing then, so the luck gate holds. Send the
    resulting uncommon to Pilar.
  - No Abuela LAV sale.
  - If a CHA rare ends up coming from Chato (no L4 slot), sell a second LAV spare to the Pícaros instead of the Workshop.
- **LAT bids** (≤ 12 on v15 as maker, 0%):
  - The fee math holds: +0.5 np at our value of 12.5.
  - Supply is thin: 1 of 8 Saturday LAT-uncommon team trades went at ≤ 12 [V redteam §2D].
  - The likeliest seller is t10, which dumps LAT [L adversary]. Its gain would be ≤ ≈ 9, inside the 10 P rule.
  - Expect 0-1 fills.
- **The sale floors come from Saturday's openings** (Pilar 16, Chato 13: directive 00:44 and dealer-lab). `dealer_sell.py`
  takes `--floor` as an argument, so the Operator types it.
  - The dealers were patched 7 times over the weekend (`persona.updated` [V feed]).
  - Pilar opens at 22 for SAL/RET.
  - Pass the dealer's first bid in that thread + 1.
- **Pack duplicates of reserved refs** are blocked by ref in `policy.py` [V]: MAL-01..06 and 08, SAL-01..05 and 07..10, RET-11.
  Sell those by hand, by asset id, and only a 2nd copy.
- **Dealer resale is harmless.**
  - A rival buying our fodder back from Chato pays list: no ladder, 0 np, and no team-trade close.
  - Pilar and the Pícaros don't sell singles of what they buy [V menus].

### 5. MAL: the binding limit is the price, not the 150 P gate (d)

- **The dealer legs can't fill.**
  - Pícaros MAL rare finals on Saturday: 57, 60, 63. MAL rares the Pícaros sold: 57, 59, 60, 61, 61 [V feed].
  - Pícaros rare finals ≤ 49, all sets: 1 of 26.
  - So MAL-09/10 at ≤ 49 (our value) fill with P ≈ 0-5% each.
- **They still cost time.**
  - t0.sh runs MAL-09 and MAL-10, two threads each with a 420 s deadline, as soon as cash ≥ 373 (always true) [V].
  - That holds the only Pícaros thread for ≈ 10-28 min, ahead of the rare's third attempt (#1) and the L4 sale (#4).
- **The stage's EV is overstated twice.**
  - MAL ×0.7 makes the bonus 46.4, so MAL-07 as the last card is worth 63.9. It scores 63.9 − price: **+44 at 20, +34 at 30,
    not +50**. mal_book's "≈ 34 at a 1.0 multiplier" doesn't apply to us.
  - "Past our cap it lowers t18/t12/t03" is **[L], not [V]**. score-model §4.13 labels the trade side [L] with no clean test.
    It also needs us inside the trade top 3, and the reference to be a top-3 mean.
- **Fix:**
  - Delete the MAL loop from t0.sh's chain, and put the CHA third attempt and the LAV-04 sale in its place.
  - At ≈ 12:00, after Duels III and after the CHA closer:
    - **If M5 shows our trade part still live, run a relaxed MAL.** t15 confirms in writing that it holds MAL-07. MAL-09/10 at
      the Pícaros ≤ 60: −11 np each, still below list, so they count as L4 upgrades. MAL-07 last, on El Rastro, at ≤ 25.
      Net ≈ +17-28 np (+17 at the caps: 63.9 − 25 − 22) ≈ +1.5-2.5 points. It buys above our value, so it needs a
      GUARDRAIL line from Lucas.
    - **If M5 says capped,** no MAL, and the 126 P leave every floor.
- **(g) t15's MAL-07.**
  - The plan asks t15 to post an ask addressed to us (market-sunday; contra-ops 08:30 "sellers post now").
  - Addressed offers are public in the feed [V GAME.md], and t10 needs MAL-07 for its own MAL close [L adversary §1.3 row 7].
  - Ask t15 to hold MAL-07 unlisted and sell it to no one else until we post our bid.

### 6. Trader and opps floors count our CHA bids twice (f)

- How the floors work:
  - The trader skips a buy when cash − bid_cash − cost < floor [V loop.py:391].
  - opps nets all our open bids against its floor too [V opportunities.py:25].
  - Both floors are 464 = CHA 288 + MAL 126 + 50 [V lucas.md 00:40, run/floors.env]. The CHA 288 is mostly the open bids
    themselves (199, rising to 219 at the caps), plus 30-36 of LAT bids.
- Neither one can buy:
  - At R+10: 542 − ≈ 230 − 464 < 0.
  - At contra-ops' 09:30 floor of ≈ 300: ≈ 430 − ≈ 150 − 300 < 0.
- **Fix:**
  - Set the floor to the planned spend **not already in open bids**, + 50. That is the unposted closer premium (≈ 30 with the
    relay, ≤ 72 without), so TRADER/OPPS_FLOOR ≈ 80-122 at R+10. It was set to 110 at 07:14.
  - Add 126 only if the relaxed MAL goes live at 12:00. Set 0 at 13:30.
  - Every trader buy stays ≥ 0 np: max ratio 0.8, CHA-*/MAL-* excluded. The trader stays held until `run/trader_ok` exists
    (rival-venue skip).

### 7. The Abuela window, 10:00-10:40, is too short (a)

- Directive 07:05 (5) runs Abuela from C+60 to D3−20, one thread at a time: 40 min for up to 6 cards.
- Abuela needs 4-7 rounds per card (≈ 3-5 min at 15 s ticks), plus reopens.
  - On Saturday, uncommon threads ended at ≤ 22 in 24% of cases and common threads at ≤ 9 in 33% [V feed]. Those numbers
    include impatient teams; among settled deals it was 44% and 65%.
  - Expect 1-3 cards to slip past Duels III.
- **Fix:**
  - Commons CHA-01..03 at Abuela from **C+5**, in parallel with the Pícaros. It's a different dealer, and ≤ 4 dealer threads
    are open. These three fill the L1 slots, and a team fill of a common is worth only +7.
  - Uncommons and CHA-04 stay public until C+45, then go to Abuela.
  - Everything but the relay pair is in hand by ≈ 10:30.
- **Optional (Chief + Aleks):** ops-contention's own figures allow **one** simple_buy thread inside Duels III.
  - Load: 0.15 req/s. "CHA release inside Duels III, 2 dealer threads: 0-6 429s an hour, duelist 0-1.6."
  - Never abuela_bot there: its plan() makes 50 reads at 4/s.

### 8. ≈ 300 P will strand at 15:00 (f)

- **Spend ≈ 250:** rares 110-120, 4 commons 36, 3 uncommons 66, closer ≤ 30 with the relay.
- **Income:** fodder sales 35-55, LAV 5, and RET-11 at 198 (≈ 20% chance).
- **End cash ≈ 300-350 P** (≈ 200 if the relaxed MAL runs). "Only deals score, never cash you hold" [V Payday deck].
- **Fix (Chief, 12:00). Spend idle cash in this order, never on a trade that books a loss:**
  1. Floors per #6, down to 0 at 13:30.
  2. The relaxed MAL, if M5 is live.
  3. Ladder upgrades below list and ≤ our value. Example: CHA-11 at the Pícaros ≤ 150 (worth 288 to us) if an L4 slot is weak
     and the card isn't minted out.
  4. Non-rival first-copy asks at ≤ value − 10 (bargains.py lines).
- **No overspend path found:**
  - book.py clamps bids to cash, and a pulled duplicate only gets a bid at duplicate value: floor = min(entry floor, value of
    one more copy − min gain) [V book.py].
  - simple_buy checks cash before it opens a thread.
  - The server refuses offers above cash.
  - The worst case on paper is ≈ 560 > 542: a rare as the last card at 168, plus full MAL, fodder and rebates. It can't happen:
    MAL dies at its price cap and rebates are off ("no cash bonuses", 01:10).

### 9. Public CHA bids pay the filler about as much as us, and can't exclude t10 (b, g)

- **Who gains.**
  - A duplicate CHA uncommon sold into our 22: we gain +18, the seller ≈ +13-16 (22 − 3 fee − its duplicate value of 3-6).
  - Once our trade part is capped (M5), the filler still gains points and we don't.
  - Stage 7 says "no deal with t10 as a party". A public bid can't enforce that, and t10 is the likeliest low-CHA seller [L
    adversary §1.3 note].
- **Who fills [L].**
  - After the El Rastro fee (taker pays [V GAME.md]), a seller nets 7 on commons at 9, 19 on uncommons at 22, and 50 on rares
    at 54.
  - Only duplicate holders and teams with CHA at ×0.5-0.7 will sell.
  - Commons and uncommons can fill: Saturday team bids had a median of 4 and 14, so 9/22 may be the top of the book early.
  - Rares at 54 will mostly lose to collectors bidding 70-90.
- **Fix:**
  - When the feed shows t10 or t01 buying CHA-xx from a dealer, cancel our public bid for that card and buy it at Abuela.
  - When M5 says capped, pull every remaining public CHA bid except the pair, and finish at Abuela (0 np + L1).

### 10. Small and cheap
- `simple_buy.py` still leaves `open_thread`, `close_thread` and `me()` unguarded [V; the run/sunday copy matches the
  scratchpad copy].
  - A 429 on the walk-close crashes the run with the Pícaros thread still open.
  - The reopen then fails on "one thread per dealer".
  - Fix: wrap the three calls in try/except with one retry.
- simple_buy has no last-card guard; abuela_bot and chato_steady do.
  - Fix: exit with "last card" when `/api/me/value` for the card is above its base value (16/40/112).
- The public CHA-09/10 bids are live while the chain runs. If both fill in the same tick we get a 2nd copy: book.py cancels one
  tick after the card lands [V].
  - Fix: drop CHA-09/10 from `book.sunday.json`, and post them only if a rare is still missing at 10:00.
- The Pícaros may stock no CHA rares at all [?].
  - On Saturday, Chato sold RET rares from 46 ticks after the release; the Pícaros sold their first only after they opened
    [V feed].
  - Fallback: Chato at ≤ 100 (0 np, no ladder). The public rare cap then follows Chato's price (≤ 75), not 54.

## The seven questions, one line each

- **(a)** As armed, CHA can't close before Duels III: the rares land ≈ 09:30 (if #1 is fixed), Abuela runs 10:00-10:40, and the
  pair comes after 12:30. With #3 and #7 the page closes ≈ 10:30-10:45. The 6-conversation cap doesn't bind (≤ 4 dealer threads
  open); one thread per dealer does, which is why the Pícaros queue matters (#4, #5).
- **(b)** The 9/22 bids can fill from duplicate holders; 54 for rares will barely fill. On stock, Abuela's 8 deals per hour are
  enough. The Pícaros' hourly rare stock is [?], so contra-ops' 10:00 rerun stands, and the global print run of 30 argues for
  buying early (#1).
- **(c)** Nobody holds CHA at C, so the realistic non-rival seller is a relay (#3). The pack and the Workshop run while all ten
  CHA cards are missing, so neither can deliver the last card. Abuela gifts matter only at 9/10, and #3 removes those threads.
- **(d)** No. The claim is [L] for trades, and at ≤ 49 the dealer legs don't fill anyway (#5).
- **(e)** LAT supply is thin. The fee math holds. Floors should come from each thread's first bid. Dealer resale is harmless. The
  LAV allocation is broken (#4).
- **(f)** There is no overspend path. The floors double-count, leaving the trader and opps inert (#6), and ≈ 300 P strands (#8).
- **(g)** t10 can fill our public CHA and LAT bids (small, #9). t15's visible MAL-07 can feed t10's MAL close (#5). A closer on a
  member market cuts v07 a little and v10 more (#2). LAV-04 → t01 helps t10's ally (#4).

## Checked and sound
- The pack opens first at C with the ≥ 2-missing gate, and MISS counts CHA-01..10 [V t0.sh]. The chain's "held" reopen check
  fixes the old exit-code problem: simple_buy exits 0 on a walk [V].
- The public caps 54/22/9 can't be flipped at a profit [V fee rule]:
  - commons (Abuela 8 → 9) net −1;
  - uncommons (Abuela 20 → 22) net −1;
  - rares (Pícaros 48 → 54) net ≤ +2.
- CHA values 16/40/112 and the 106 bonus [V GAME.md]. The worst-case CHA spend fits in 542. The live-tuning caps were fixed at
  07:05.

## Limits
- No live reads: the catalog, the Pícaros' CHA stock and the Sunday dealer versions are unchecked. Saturday's dealer data may not
  hold on Sunday.
- Whether VC includes the page bonus is [?], and the size of #2 depends on it.
- The EVs are judgment-weighted ranges, not a simulation.
