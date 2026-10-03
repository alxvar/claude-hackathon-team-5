# Scout (claude-sonnet-5-5, Sat 10:17)

## Top 3 actions now
1. **RET-07 (uncommon) from Abuela, cap 24. Operator's abuela_bot under `uv run`, reopens ~tick 259.**
   - Evidence: RET-08 closed at 22 (`neg_points` 0, ladder 0.048 → 0.051). RET-07 is worth 27.5 to us, so a deal ≤ 24 never loses. t15 bought RET-07 at 24 (tick 234) and is the only visible holder.
   - Effect: ladder about +0.003 and no `neg_points` cost. It leaves RET-01 as the only missing card, once the RET-06 deal at 30 (log 10:16) is confirmed in `/api/me`.
   - Confidence: high.
2. **RET-01 (common): public El Rastro bid at 20, from a team. Operator, `trade.py bid`, after action 1.**
   - Evidence: t13 bids 2 for RET-01 (offer 3856), so it lacks the card too. Holder and ask price: not in the data. The bonus scores only via a team trade [L], and 72.9 + 11 − 22 far exceeds the ~50 cap.
   - Effect: +50 predicted (flat 50 or 5×book), ~62 if 5×(p+f), ~38 if value ≤ 6×book. Log the result in GAME.md at once.
   - If unfilled in ~10 ticks, raise by +2 steps toward ~25 (value with bonus ≈ 84). Keep it short-lived: the feed shows addressed offers.
   - Confidence: med (cap form open, n=1).
3. **Check the level-3 unlock now: `GET /api/me` level, then `/api/schedule`. Operator, 2 min.**
   - Evidence: we have 3 negotiated Chato deals today (87, 86, 30). Level 2 opened early on Friday for 3 negotiated deals [V]. The metrics still show "level 2" and bid 3989 (30 for RET-06) as open.
   - Effect: opens the level-3 ladder. Tell the Chief before any level-3 dealer opens. Do not buy a pack.
   - Confidence: low-med (the level-3 rule is unpublished [L]).

## What the climbing teams are doing
- **Team 18 (#1, +14.6/15 min)** collects RET/LAT. It paid 49 P for RET-02 from t02 (tick 230), well above the 9-10 clearing price. It looks like a team pushing a page. RET page progress per team: not in the data.
- **Team 2 (#3, +9.6/15 min)** trades RET at both ends: sold RET-02 at 49 and RET-07 at 24 (ticks 230, 234), bought MAL-01 (tick 235). It also bids only 17-19 for RET-09/10 (offers 3983/3982). It is selling RET-type cards at a premium to a top-4 rival.
- **Team 3 (#9, +5.5/15 min)** has 1 team trade and 11 dealer trades, with an Abuela discount of −22.8%. It climbs on dealers and ladder, not on team trades.
- **Team 14 (#5, +4.9/15 min)** has 13 deals, collects LAV/LAT, and its median uncommon price is 40.

## Threats
- Team 18 (#1) and Team 2 (#3) both collect RET and could finish the RET page before us. Never sell them RET cards, and do not feed t18/t2/t12/t13 any card.
- t15 (#14) collects RET and holds RET-07. If it sees our bid it can raise the price. t13 bidding on RET commons (2 P) shows competition for RET-01.
- v10 at 0% lets other teams' trades score for the venue owner. Team 12's market 11.49 came from one 7 P trade on its own venue. We are fine on the stall (4.8), but do not route anything via v02/v03.
