# Deny-list (Analyst, Sun 00:30; read-only; final Saturday snapshot 1440)

> **CORRECTION, Sun 11:52 (Chief, from Team 3 to Lucas):** t03 already holds SAL-03; its Saturday SAL-03 sale (settlement 1008, tick 1130) was
> a spare. My SAL-03 alerts (09:53, 11:17, 11:50) were wrong. Rule from now on: **feed holdings are a lower bound (they miss starting
> albums and spares). A team that sold or listed a card may still hold another copy. Only a rival's OWN live bid proves it lacks a card.**
> The denial watch now alerts only on that evidence. Today's claims checked against the closes: t18 CHA-01, t12 LAV-07, t06 CHA-05 and
> t10 SAL-08 were right (each closed with that card). t03 SAL-03 was wrong. t18 RET-07 and t12 LAT-08 are unknown, likely held (each sold one).

**Verdict: no denial buy is ≥ 0 for our score at today's asks. Drop the 35-50 P denial reserve and put it into CHA or v10.**
The cheap "denial" is (1) never selling our spares or page cards to a rival, and (2) pulling trades off t10's v07 onto v10
(score-model §4.9: P(#1) 1.7% → ≈ 7%).

**Method and limits [L]:** holdings come from the feed (`tools/v10_radar.holdings`), a LOWER bound that misses starting albums.
t12 and t06 each show 3 complete pages on the board but far fewer cards in the feed, so a "missing" card may already be held.
A rival's own live bid for a card is the only strong evidence that it lacks it. Rival points removed by one denied page close
≈ 9 × 50/N Sunday points (N ≈ 40-100 → 4.5-11), and only if our buy is the last copy it can reach. Every set below has 5-8 other
holders. Our value of a copy: first copy = book × our multiplier; an extra copy = 0.25 (2nd) or 0.10 (3rd+) of that.
Script: scratchpad `deny.py`.

## Rivals, near pages (feed ≥ 8/10, or a live bid)

| Rival | Set (feed) | Card it lacks | Holders (feed) | Live asks | Our value of a copy | Denial buy ≥ 0 for us? |
|---|---|---|---|---|---|---|
| t12 | LAT 9/10 | LAT-08 | 8 teams (t06, t07, t15, t18, t14, t03, t04, t17) | t06 at 30 (Rastro) | 12.5 | **No** (30 > 12.5) |
| t12 | MAL 8/10 | MAL-03, MAL-08 | MAL-03: 8 teams; MAL-08: 6 incl. **us** | MAL-03: t06 at 12 | MAL-03 1.8 · MAL-08 is OUR page card | **No.** Never sell MAL-08 to t12 |
| t12 | LAV 6/10 | live bid LAV-08 at 14 (v11) | 8 teams incl. us | — | LAV-08 is our page card | Never sell |
| t18 | RET 9/10 | RET-07 | 8 teams incl. us | t16 at 45 | 6.9 | **No.** t18 sold its own RET-07 to Pilar (tick 1426): it isn't chasing RET |
| t03 | LAV 8/10 | LAV-02, LAV-04 | many; **we hold spares** (LAV-02 ×3, LAV-04 ×2) | t04 LAV-02 at 10; t08 LAV-04 at 10; ours at 6 are addressed to t04/t01 | 1.3 | **No buy.** Free denial: never sell LAV-02/03/04 spares to t03 (it still has t04/t08 at 10) |
| t03 | SAL 8/10 | SAL-03, SAL-10 | SAL-10: we hold (page card) | — | page card | Never sell |
| t06 | LAV 8/10 | LAV-05, LAV-08 | we hold both (page cards) | — | page cards | Never sell |
| t06 | MAL 4/10 | live bids MAL-02 2, MAL-05 2, MAL-09 31 | — | — | — | far from a page |
| t10 | RET | closed (snapshot 1040) | — | — | — | — |
| t10 | LAV 7/10 | LAV-01/03/07 | many | — | — | far |

## CHA (released at round 3; everyone starts at 0/10)
The scarce cards are the rares CHA-09/10 (print run 30). An extra copy is worth 0.25 × 112 = 28 to us, so a ≥ 0 denial buy
needs a price ≤ 28: impossible (dealers ≈ 48-63, teams ≈ 65-86). No CHA denial; the rule is: never sell a CHA card to a rival.

## Market denial (the one that works) [L]
t10's Saturday lead is 7.5 points of v07 value created. The VC part is field-normalised (score-model §3h), so every pair that
trades on v10 instead of v07 lowers t10's share and raises ours: a double swing for 0 P (rebates ≤ 80 P per the sunday-plan).
