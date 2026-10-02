# Dani — judges, organisers, notes

**Now:** Live dashboard running (`python dashboard/server.py` → http://127.0.0.1:8765, read-only). Then the organisers' desk (2 questions) and the room (LAV-09 holder, buyers for SAL/LAT).

**Touches:** this file only.

## Log (newest on top: `time · what · result · next`)

- Fri 22:05 · **correction for judge 21:55:** offers #984-988 (bids SAL-07 18, SAL-08 18, MAL-07 14, MAL-09 38, MAL-10 38) ARE ours: the feed's `offer.listed` at tick 69 has actor `t05`. The collector started after tick 69, so it shows their owner as "?" · Team 17 bids 78 for MAL-09/10 and 26 for MAL-07, so our MAL bids neither fill nor block: cancel them, or keep them on purpose · next: Lucas decides

- Fri 21:55 · `dashboard/` live, read-only (public routes without the key, ~5-8 requests per tick): score over time, each team's inferred strategy, El Rastro board with the real team behind 52 of 55 offers, edges at our values, rival bids, who last bought the cards we want · first reads: **rival bids beat ours on MAL-09 (Team 17 78, Team 12 70, Team 8 67 vs our 38), MAL-10 (Team 17 78), MAL-07 (Team 17 26, Team 8 24 vs 14), SAL-07/08 (Team 8 19 vs 18)**; MAL is worth 0.7× to us, so a MAL rare at ~78 is a sale for us, not a buy. Buyers of our low sets: LAT → Teams 18, 8, 14, 15; SAL → Teams 18, 8, 3; MAL → Teams 8, 12, 17, 15 · next: anyone can run it; I keep it on to build history

- Fri 21:45 · read the public feed (no key) · **Team 10 outbid us on LAV-09: 90 P (offer #1114, tick 76) vs our 85 (#910).** Also: the feed's `offer.listed` events carry the real maker team id, so 65 of the 77 "anonymous" El Rastro offers can be matched to a team (feed → offer id → actor) · next: Lucas decides on LAV-09; I'm building a read-only dashboard on this

- Fri 21:25 · checked the 5 questions against RULES.md · Q2 already answered (a deal at the dealer's opening price doesn't count, line 35); the other 4 sharpened (duel pie decay formula, early-unlock count, level 2 timing, judging format, whether pack prices count in neg_points) · next: organisers' desk

