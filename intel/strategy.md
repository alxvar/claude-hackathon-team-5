# Strategist (claude-opus-5-5, Sat 22:07)

## How the points really work
- **Board = Negotiating 30 + Market 30 (Market Test 7.5 + real trades 22.5) + Judges 40.** All game parts are relative to the field. Judges' scoring is not in the data.
- **Us now:** 30.85 board = negotiating 23.35 + market 7.5 (log 21:53). Our market is bench only: real trades are 0 since the tick-398 wipe.
- **Real trades is the field's weakest component.** The best market shows +5.0 of 22.5. One positive-VC trade between two teams on v10 gave us +4.99 (tick 311). The directive's model is 5.0 × min(1, VC / top-3 mean) [L].
  - So one brokered page-close on v10 ≈ +5 board, about what +100 `neg_points` would give at 0.05/pt.
  - The risk is symmetric: a dump on v10 (card to a lower multiplier) subtracts (−5.2 at tick 398).
- **Team trades:** +0.05 board per `neg_point` [V 17:46]. Capped at 50 per trade. 173 team trades in the whole field. Ours are flat at 119.1 since tick 988.
- **Ladder and flags are spent this round:** ladder flat for the board at 0.373 → 0.437; flags capped at about 3 scored (net +20). Dealer gains clip to 0.
- **Duels are our only rising part:** duel points 13.93 → 26.43 since 21:17.
- **Round timing [L, schedule]:** Round 3 and the CHA release are at game hour **16.65**, but Sunday opens at **13.368**.
  - Precedent: round 2 fired at tick 160, not at doors-open.
  - So Sunday's first 3.28 game hours are still **round 2**, including the hard bench (14.65) and the bench at 15.0.
  - The schedule is inconsistent: Bazaar closes at 19.368, yet benches and finale are listed at 21.0-21.65. Wall times are not in the data.
- **Gap to t10 is 7.9.** It is only closable through real trades (+5) plus a page close (+50 neg ≈ +2.5) plus duels.

## Our winning strategy
- **Be the market that finishes OTHER teams' pages, and finish our own CHA page in round 3.**
  - t10 wins on epic flips and its own venue, and both sit near the same 5.0 ceiling. Copying it caps us at a tie.
  - Brokered page-closes on v10 use the one component nobody has filled. They cost us 0 P (rebate ≤ 80, paid via a card we lack worth ≥ the amount).
  - They need humans: bot team chat got 0 of 4 replies.
- **Only collector-bound moves on v10** (matchmaker rule: giver dumps or holds 2+, receiver collects). Net VC must stay positive.
- **CHA (1.6×, bonus 106):** buy every card at ≤ value (dealers score 0; low-CHA teams sell below value and score positive). Close with a team trade after 16.65.
- **Stop doing:**
  - bot-to-bot chat pings;
  - dealer threads tonight;
  - flags until round 3;
  - DENY buys (the last target was stale);
  - +2 sells of single copies: cancel 18963 (MAL-03) and 18965 (MAL-08), which are Sunday MAL page progress.

## Levers nobody is using yet
1. **Page-close brokerage on our venue.**
   - Evidence: best market +5.0 of 22.5; no v10 trade between others since the 21:30 rebate; all 46 Friday trades went via El Rastro.
   - First match: RET-09 t08 → t09 (t08 dumps RET and asks 84; t09 is 9/10 on RET; VC ≈ +134).
   - Exploit: Lucas and Dani go in person, not by ads.
2. **Round boundary at 16.65.**
   - Evidence: `/api/schedule`. The directives and the organisers' deck assume "Sunday = new round".
   - Exploit: the Sunday morning is round 2 territory. Run the v10 desk and RET-11 there; hold the MAL/CHA closers for after 16.65.
3. **Cap-form test for free.**
   - If the CHA page's last card is a **rare bought from a team**, value = 112 + 106 = 218. At any price ≤ 168 the gain is above 50.
   - A flat-50 cap still gives 50, the same as a common closer. A 5×book cap gives up to 350.
   - Nobody has tested it (both observed caps were commons).
4. **Fresh-round reset of flags and ladder.** Round 2 zeroed both. If flags reset, 3 correct flags = +30 neg in round 3. CHA dealer buys made with −2/−3 steps fill ladder slots at no extra cost.
5. **RET-11 to a non-rival RET collector above 198** scores positive `neg_points`; Pilar at the same price scores 0. The last epic print sold at 216 (t06 → t12). Never sell to t12 or t10.

## Plan, anchored to the schedule
| When | Who | Move | Impact |
|---|---|---|---|
| Now → 13.368 (Sat close) | Lucas + Dani in person | RET-09 t08 → t09 relisted on v10 at 84-100, 10 P rebate; then MAL-09/10 to t15/t09 from a MAL dumper (not t10) | ≈ +5 board [L] |
| Now | Operator | Cancel 18963 and 18965. Swap a LAV-02 spare (1.3) for t04's MAL-06 on El Rastro, maker, only if LAV-02 is not t04's last LAV card (matches.md) | ≈ +16 neg ≈ +0.8 |
| To tick 1371 | Operator | Leave SAL-11 18977 to expiry; floor back to 350 after | 0 to +47 neg |
| 13.0 bench | Market | Stall, no action | — |
| After Sat close | Dani at the desk | Ask: (a) does round 3 start at 16.65; (b) what earns the full 22.5; (c) do flags/ladder reset; (d) do packs pull CHA if opened after release | Settles hypotheses 1, 2, 4, 6 |
| After Sat close | Lucas + Dani | Pitch draft: measured-facts table (cap, pack drag, flags, ladder, round timing) | Judges 40 |
| Sun 13.368 | Operator | Read `/api/clock`, `/api/schedule`, `neg_points` (119.1 = still round 2). Bots on | — |
| 13.368 → 16.65 | Lucas + Dani + matchmaker | v10 desk with every team in the room; two-way duplicate swaps (+15 common / +37 uncommon VC); RET-11 ≥ 199 to a non-rival collector | Round-2 market + neg |
| 14.65, 15.0 benches | Market | Stall (round 2) | — |
| Before 16.65 | Operator + Builder | Pre-stage CHA dealer threads and maker bids addressed to low-CHA teams; cash 392 + 150 | Speed in a short round |
| 16.65 | Operator | Open the silver pack first (drag), then buy CHA at ≤ value with −2/−3 steps. Leave 1 rare + 1 common. Last card = team rare if one is offered, else Chato rare at ≤ 112 then a team common | +50 to +148 neg, cap test |
| After 16.65 | Operator | MAL close per directive (t15 MAL-07 closer), only if CHA is under budget. First unmistakable Pícaros false fact → one flag | +36 neg [L]; +10 if flags reset |
| After 16.65 | Lucas + Dani | First positive-VC v10 match of round 3 | ≈ +5 in round 3 [L] |
| 18.65 Duels III | Aleks | Duelist; bots maker-only | Duel points |
| Before 21.65 | Operator | All dealer buys done (stalls close) | — |

## Hypotheses to test
1. **Round 3 starts at 16.65, not Sunday doors-open.**
   - Test: desk question, plus `neg_points` at 09:00.
   - Decides: 119.1 is held until the round event, then 0.
2. **Real trades saturate at 5.0 per market.**
   - Test: a second positive-VC trade on v10.
   - Decides: market component rises above about 12.5, or stays.
3. **Cap is 5×book, not flat 50.**
   - Test: a CHA rare closer from a team at ≤ 168.
   - Decides: Δ`neg_points` = 50 or above 50.
4. **Flag cap resets per round.**
   - Test: one flag after 16.65 on a words-vs-structure mismatch.
   - Decides: +10, or 0.
5. **Ladder moves the board in a fresh round.**
   - Test: the first below-list CHA dealer buy.
   - Decides: whether `negotiating` moves at the next board refresh, with no other deal in the window.
6. **A pack opened after the release can pull CHA.**
   - Test: watch others' `pack.opened` best card after 16.65 (free).
   - Decides: a CHA card shows up, or never does.
