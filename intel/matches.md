# v10 matchmaker: page finishers and first copies

_Written by `tools/matchmaker.py` at 15:41 (tick 2802). Read-only. Holdings: the feed's copies (gifts, eggs and Workshop crafts included) plus the page arithmetic on the leaderboard's album_filled/pages_complete and minted supply (`tools/album.py`; 0 conflicts with intel/holdings-audit.md). ✓ = a proven gap, a bid since Saturday, or a want-list; "undecided" = the buyer may hold it. Giver: a true duplicate or a set it dumps (held back when its page is complete and under two copies are seen after its last craft); receiver: no copy, collects the set; both gain > 0 at the price (conservative multipliers). Want-lists: `intel/wants.md`. Never a page-closer for a rival or a team < 6 below us; a rival on either side gains <= 10 P at our price. Venue: a club deal (both sides in the club) alternates v10 / a member's market (least used, then lowest market score, never either side's own; page-closers on v10); every other deal on v10._

## Matches (best first)

| # | Buyer | Card | Seller | Venue | Price | Value created | Closer | Rival | Why |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Team 16 | RET-01 Barca del Estanque | Team 1 | v10 | ~9 | +7.1 (low +7.1) |  |  | bid ✓ · gap proven · seller holds 2 · also t08 · spare unverified: 1 seen after its common craft at tick 2575 |
| 2 | Team 16 | RET-04 Paseo de Coches | Team 1 | v10 | ~9 | +7.1 (low +7.1) |  |  | bid ✓ · gap proven · seller holds 2 · also t08 · spare unverified: 1 seen after its common craft at tick 2575 |
| 3 | Team 16 | RET-06 La Rosaleda | Team 8 | v10 | ~22 | +4.9 (low +4.9) |  |  | bid ✓ · gap proven · seller dumps RET |
| 4 | Team 16 | RET-02 La Castañera | Team 8 | v10 | ~9 | +2 (low +2) |  |  | bid ✓ · gap proven · seller dumps RET |
| 5 | Team 16 | RET-03 El Titiritero | Team 8 | v10 | ~9 | +2 (low +2) |  |  | bid ✓ · gap proven · seller dumps RET |

## Ready DMs

**1. RET-01 · Team 1 → Team 16 at ~9 P on v10**
- To Team 1: "Hi Team 1! Could you post your Barca del Estanque (RET-01) on v10 as an ask addressed to Team 16, at ~9 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 1 can post Barca del Estanque (RET-01) on v10 as an ask addressed to Team 16, at ~9 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**2. RET-04 · Team 1 → Team 16 at ~9 P on v10**
- To Team 1: "Hi Team 1! Could you post your Paseo de Coches (RET-04) on v10 as an ask addressed to Team 16, at ~9 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 1 can post Paseo de Coches (RET-04) on v10 as an ask addressed to Team 16, at ~9 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**3. RET-06 · Team 8 → Team 16 at ~22 P on v10**
- To Team 8: "Hi Team 8! Could you post your La Rosaleda (RET-06) on v10 as an ask addressed to Team 16, at ~22 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 8 can post La Rosaleda (RET-06) on v10 as an ask addressed to Team 16, at ~22 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**4. RET-02 · Team 8 → Team 16 at ~9 P on v10**
- To Team 8: "Hi Team 8! Could you post your La Castañera (RET-02) on v10 as an ask addressed to Team 16, at ~9 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 8 can post La Castañera (RET-02) on v10 as an ask addressed to Team 16, at ~9 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**5. RET-03 · Team 8 → Team 16 at ~9 P on v10**
- To Team 8: "Hi Team 8! Could you post your El Titiritero (RET-03) on v10 as an ask addressed to Team 16, at ~9 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 8 can post El Titiritero (RET-03) on v10 as an ask addressed to Team 16, at ~9 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

## Teams one or two cards from a page

- Team 17 RET 8/10 · missing RET-07 (undecided), RET-08 (undecided) · rival · **may be complete**
- Team 1 RET 8/10 · missing RET-07, RET-09

## Held back (never suggested)

- RET-01 for Team 16: seller safety: Team 18's RET page is complete and only 1 copy of it seen after its last common craft (tick 2216)
- RET-01 for Team 16: seller safety: Team 12's RET page is complete and only 1 copy of it seen after its last common craft (tick 1114)
- RET-04 for Team 16: seller safety: Team 18's RET page is complete and only 0 copies of it seen after its last common craft (tick 2216)
- CHA-03 for Team 15: seller safety: Team 1's CHA page is complete and only 0 copies of it seen after its last common craft (tick 2575)
- CHA-03 for Team 4: seller safety: Team 1's CHA page is complete and only 0 copies of it seen after its last common craft (tick 2575)
- CHA-03 for Team 9: seller safety: Team 1's CHA page is complete and only 0 copies of it seen after its last common craft (tick 2575)
- CHA-03 for Team 7: seller safety: Team 1's CHA page is complete and only 0 copies of it seen after its last common craft (tick 2575)
- CHA-03 for Team 13: seller safety: Team 1's CHA page is complete and only 0 copies of it seen after its last common craft (tick 2575)
- CHA-03 for Team 3: seller safety: Team 1's CHA page is complete and only 0 copies of it seen after its last common craft (tick 2575)

## Holdings (page arithmetic)

| Team | Status | Held | Proven gaps | Undecided |
|---|---|---|---|---|
| Team 1 | exact | 51/51 | 9 | 0 |
| Team 2 | partial | 38/42 | 1 | 21 |
| Team 3 | exact | 43/43 | 17 | 0 |
| Team 4 | exact | 45/45 | 15 | 0 |
| Team 6 | repaired | 40/47 | 12 | 8 |
| Team 7 | repaired | 30/39 | 20 | 10 |
| Team 8 | exact | 49/49 | 11 | 0 |
| Team 9 | partial | 42/47 | 6 | 12 |
| Team 10 | exact | 41/41 | 19 | 0 |
| Team 11 | partial | 1/13 | 12 | 47 |
| Team 12 | exact | 45/45 | 15 | 0 |
| Team 13 | repaired | 30/36 | 23 | 7 |
| Team 14 | partial | 43/44 | 7 | 10 |
| Team 15 | exact | 43/43 | 17 | 0 |
| Team 16 | exact | 44/44 | 16 | 0 |
| Team 17 | partial | 37/44 | 8 | 15 |
| Team 18 | partial | 46/47 | 2 | 12 |

- run/known_holdings.json entry for Team 5 ignored: the feed shows MAL-07, MAL-10 held.

- run/known_holdings.json entry for Team 15 ignored: the feed shows MAL-09, MAL-10 held.
