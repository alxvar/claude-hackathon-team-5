# Sunday red team: the aggressive plan (independent strategist, Sun ≈ 01:30)

_Read-only red team with no prior context. Sources: `bazaar-kit/RULES.md`, `intel/chief-handoff.md`, `sunday-plan.md`, `cha-plan.md`,
`dealer-lab.md`, `dealer-lab-ladder.md` (§6 included), `duel-lab.md` (top), `market-sunday.md`, `score-model.md` §3-§4.10, `GAME.md`,
`directives.md` (through the lines labelled 02:30 / 01:35 / 01:15 / 00:50), `market-test-audit.md`, `audit-why-we-lost.md`,
`live-tuning.md`, `deny-list.md`. Live keyless reads at 00:15-01:20: `/api/clock`, `/api/schedule`, `/api/catalog`, `/api/leaderboard`.
Feed: `data/feed.jsonl` (to tick 1445). Code read: `agents/dealers/abuela_bot.py`, `chato_steady.py`, `bazaar-kit/bazaar_sdk.py`.
Labels: **[V]** measured or read · **[L]** inferred, fits the data · **[?]** open. Points are **Sunday round points** (out of 60;
final game = × 0.4) unless marked. An independent verifier audited this file (6 of 11 checks passed, 5 flagged); every flag is
applied below._

**Already adopted while this was written:** the clock correction (score-model §4.7, 01:45; sunday-plan and chief-handoff, 01:50),
the ladder-fodder pipeline (the directive labelled 02:30), the trader running sell-only and CHA bids capped at dealer prices
(01:35 / 6110b0e). The changes below are the ones still open.

## 0. The verdict and the changes that matter

**First place stays a long shot** (t10 needs to lose ≈ 16-18 Sunday points against us). **Second place is a four-way race with
t18, t12 and t03**: t12 sits 0.04 final points behind us (audit-why-we-lost §6), and t06 is close too. It goes to whoever fills the
four 0-cost or cash-neutral parts best: ladder, trade part, v10 VC and duels. The plans are good on CHA and duels. They still
leave 1-3 points on the table in the **first 20 minutes** and in the **ladder**, and they carry one live code risk.

| # | Change vs the current plans (still open) | Why | Sunday pts [L] |
|---|---|---|---|
| 1 | **Buy both CHA rares from the Pícaros from the first tick** (t+1), not at dealer-lab FAST-START's t+120 (30 min) after team bids | SAL-09 is minted 29/30 and SAL-11 9/9 after one day of Pícaros → Pilar loops [V catalog]; no team holds a CHA rare before dealers sell them; the CHA public bids are now capped at dealer prices anyway (6110b0e), so a 30-minute wait buys nothing | +0.5-2 (protects 2 L4 slots and the page) |
| 2 | **The "trick guard" is not in the code.** Run every Pícaros thread with `--offer-only`, and have the Builder add a card/rarity check before `b.accept` | `_haggle` and `chato_steady` accept the dealer's standing offer after a cash-only check [V code]; to a dealer, our `price` is a structured offer for the thread's item [V SDK] | avoids −1 to −3 |
| 3 | **Ladder fodder from T0, in parallel with CHA, and the silver pack opened BEFORE the rares** (the 02:30 directive says after the CHA buys and after the rares) | Pilar, Chato and Abuela/Pícaros are separate threads (≤ 6 open); the pack may draw a CHA rare (then we skip a 52 P buy) and drags every CHA team buy while sealed (≈ 10 np on the SAL close [V]) | +0.5-1 |
| 4 | **Gate the MAL close at 10:30 on the live trade-part test (live-tuning M5), not on cash (≥ 150 P left)** | the trade part caps at N (≈ 40-125 np); flags + the CHA closer + 2-3 CHA team buys likely fill it, after which MAL's net +20-28 np is worth ≈ 0 while costing ≈ 130 P | +0-2, and avoids wasting ≈ 130 P |
| 5 | **Harvest flags inside the rare threads, and put the egg line in the first PRICED message** (FAST-START's t+1 opens text-only threads and closes them) | 3 × +10 np at 0 P if the cap reset with round 3 [?]; a text-only thread costs a conversation and the bots' 10-tick reopen gap before the rare buy | +0-2.7 |

Smaller items: cancel SAL-11 20252 and the two LAV asks **before** the first tick; no club cash bonuses; never a big-VC trade
(page closer, rare) on a member's venue (it raises the VC normaliser); throttle keyed daemons during duel waves; idle cash has no
terminal value, so spend it by rule (§8); any Ernesto deal needs Lucas to lift the 00:50 GUARDRAIL.

## 1. Facts checked tonight that change the plan

### 1.1 The clock: game hour = wall hour at any tick length [V]
- Friday's ticks were 60 s: tick 96 → game 1.6 h (60 ticks per game hour). Saturday's were 30 s: ticks 160 → 1445 = 10.7 game hours
  (120 ticks per game hour). Each tick advances `tick_seconds` of game time, so **15 s ticks don't compress the schedule**. Sunday has
  240 ticks per game hour, and game time still runs at wall speed.
- So score-model §4.7's **B15 (Duels III 10:00, Final 11:30, close 12:00)** and **A15 (a 98-min tail)** were arithmetic errors. A15 would
  be 197 min, the same as A30. The handoff's "duelist live by 09:55" relaxes to **10:30** (corrected in score-model §4.7 at 01:45, and
  in sunday-plan and chief-handoff at 01:50).
- **Wall times below are the earliest possible.** Organiser pauses push everything later: Saturday took 14 wall hours for 10.7 game
  hours (a late open, then ticks 630 → 632 took 2 h 05 and ticks 1200 → 1209 took ≈ 47 min [V me.jsonl]). The doors close at 15:00
  whatever the game clock says: Saturday closed at 23:00 with its 14.65 and 15.0 benches never fired. **A late Final can be cut
  by the 15:00 close.**
- **Precedent [V feed]:** Friday closed paused at game 2.65 (tick 159). At Saturday's open, `day.opened` came at t 2.65 and
  **`round.started` round 2 at tick 160 (t 2.658)**, though the schedule had placed it later (GAME.md: "not 4.0"). The organisers
  re-anchor day-open events to the real opening. Tonight `/api/schedule` again pins `day_opens sun` at 16.65 = wall 09:00 and
  `end_round` at 22.65 = 15:00 [V]. A literal resume at 13.367 would push the Final to ≈ 17:17, past the 15:00 close.
- **Cases [L]:**
  - **Case J (≈ 80%):** round 3, the CHA release and the round-3 events fire at ≈ 09:00 (re-anchored or jumped; the wall times
    are the same). +150 at ≈ 09:03; Duels III ≈ 11:00-11:51 (68 duels, 17 waves × 12 ticks × 15 s); finale warning 13:48; dealers
    close and the Final starts ≈ 14:00 (≈ 14:27 end); freeze 15:00; benches at ≈ 09:21 / 11:21 / 13:21 (the stall gets half
    either way).
  - **Hybrid (inside J):** the round fires at the open but the clock stays near 13.37 with the rest of the schedule unshifted. Then
    Duels III would read 14:17 and the Final would fall after the close, so expect another re-anchor. Plan on the 11:00 timetable
    and re-read the schedule at every event.
  - **Case A (≈ 15%):** round 2 continues from 13.367 (a Saturday tail), and the organisers re-anchor or jump later in the morning.
  - **Other (≈ 5%):** organisers' surprises. **The case = `round` in `/api/clock` at the first tick** (directive 00:50). Recompute every
    wall time as `now + (at_hours − t_hours)`.

### 1.2 CHA rares are a race, not a queue [V catalog 01:00]
- Minted: **SAL-09 29/30**, SAL-10 20/30, **SAL-11 9/9** (sold out), RET-09 14/30, MAL-09 9/30, CHA-09/10 0/30.
- Saturday's flippers (t08, t10, t12, t14) drained SAL rares through Pícaros → Pilar loops within hours.
- Dealer allotments are per team per hour, but **print runs are global**. Every team and every flipper hits the Pícaros for CHA rares
  at 09:00.
- No team holds a CHA rare before buying one from a dealer. Team asks will open at ≥ 70-85, while the Pícaros close at 48-57.
- Rares at the Pícaros at **t+1, not t+30 min**: 0 neg, and two of our three heaviest ladder slots (L4, 0.089 each at full share).

### 1.3 The trick guard is a phrase, not code [V]
- `grep -i trick agents tools` finds only an egg line.
- `abuela_bot._haggle` and `chato_steady` accept the dealer's standing offer (`b.accept(o["id"])`) after comparing **cash only**
  (`her_price`).
- The Pícaros' main trick is structural: an uncommon at the rare ask in 41 Saturday threads, a rare at the epic ask in 8.
- With `--offer-only` **we** post the structured offer for the thread's item (SDK: "To a dealer, `price` is your structured offer
  for the thread's item") and the dealer accepts ours. **Every Pícaros run: `--offer-only`.** Builder, 08:30: a 5-line guard
  before each `b.accept`, so the offer's `give` card ref and rarity must equal the topic card.

### 1.4 The scoring parts and their references
| Part (per round) | Max | How [source] | Our Saturday | Sunday lever |
|---|---|---|---|---|
| Duels | 12 | share × 0.9^rounds, field-graded [V weight, L grading] | ≈ 6.9 (t10 ≥ 9.2) | latency + Duel Lab set |
| Team trades | 9 | 9 × min(1, T/N), T = neg_points; N ≈ 125 at Saturday's end, Sunday 40-125 [L] | ≈ 0.95 of cap | flags, CHA closer, CHA team buys |
| Ladder | 9 | 9 × min(1, L/M), L = Σ level × best-3 shares / 45 [V raw, L grading]; M ≈ 0.35-0.65 | capped at ≈ 0.37+ | **fodder pipeline** |
| Market Test | 22.5 | stall = 0.5 every session = 11.25 [V `bench_points` 0.5] | 11.25 | none (keep the stall) |
| Real trades (VC) | 7.5 | 7.5 × min(1, VC/top-3 mean) [L strong, market-test-audit §2] | 0 (−5.2, then +2.2 at the close) | v10 pairs, ≈ 40-50 net VC |

The deck's "Market Test 7.5 + real trades 22.5" was transcribed backwards; the slide and the data say 22.5 / 7.5 (market-test-audit §0).
A ceiling team scores ≈ 12 + 9 + 9 + 11.25 + 7.5 = 48.75. t10 made 45.99 on Saturday.

### 1.5 Packs, the Workshop and fodder [V]
- **The silver pack** (`sobre_plata`, asset 1013 per cha-plan; check `/api/me`): 2 commons, 2 uncommons and one rare (86%), epic (12%)
  or legendary (2%) [V catalog]. Pack drag cost ≈ 10 np on the SAL close [V]. Opened at the release, it removes the drag from every
  CHA team buy (the closer included), may draw CHA cards (5 slots), and **yields 2-3 ladder fodder cards**: duplicate uncommons/rares
  of LAV/RET/SAL are worth 25% to us, so any dealer price is ≥ their value.
- **Workshop:** `POST /api/taller` with 3 spare commons of one rarity (≥ 1 of each card kept) → 1 random uncommon. Our spares: LAV-02 ×2,
  LAV-03 ×1, LAV-04 ×1 [V, dealer-lab-ladder §6]. Not a scored deal; the card is fodder or a CHA card.
- **Dealer buy prices for fodder** (Saturday, all teams, ticks ≥ 160) [V feed]:
  - Pilar non-SAL/RET uncommons: 14-21, mostly 17-19, best 20-21 (n = 50); non-SAL/RET rares 50-56 (n = 4).
  - Chato uncommons: 11-16 (24 settlements, 25 cards; the one "26" is a 2-card settlement at 13 each); Chato rares 29 and 49.
  - Ernesto epics: settled 116-120 (n = 3); his finals ran up to 129 (dealer-lab-ladder §6).
  - Pícaros MAL rares: 57-61 (n = 5); Pícaros epics: 128-167 (n = 18).
- **Team uncommons on Saturday** [V feed]: LAT 10-25 (10, 13, 14, 14 at the bottom), MAL 14-28.

## 2. Stage by stage

EV = our expected Sunday round points from the stage under this plan [L]; "Δ" = vs the current plans.

| Stage | EV (range) | Δ | P cost | Window | Owner |
|---|---|---|---|---|---|
| A. Saturday tail (case A only) | +1-2 **Saturday** pts | 0 | 0 | 09:00 → re-anchor | Lucas, Dani, Market |
| B. Market Test | 11.25 fixed | 0 | 0 | all day | nobody (keep v10 open) |
| C. v10 real trades | 3-5 (1-7.5) | +0.5 | 0 | 09:00-14:45 | Lucas, Dani, Market |
| D. Dealer ladder (fresh) | **7-8.5** (4-9) | **+2-4** | ≈ 140 (in CHA) + fodder float ≈ 40 | 09:00-10:45, 11:55-13:45 | Operator |
| E. Team trades: CHA page, closer, flags | 7-9 (5-9) | +0.5-1 | ≈ 230-280 | 09:00 → closer ≈ 12:30 | Operator (book), Lucas/Dani for the closer |
| F. MAL page close | 0-2 (gated) | −0.5 | 0-130 | gate 10:30, buys 10:30-13:30 | Chief gate, Operator |
| G. FLIP / surplus → ladder | 0.5-2 | +1 | float 50-140, net ≈ 0 | after the M5 test, ≥ 10:30 | Operator (reactor), Chief go |
| H. Duels III + Final | 7.5 (6-9) | +0.5 | 0 | 11:00-11:51, 14:00-14:27 | Aleks |
| I. Denial | t10 −1 to −3.75 (via v07 flow) | — | 0 | all day | Lucas, Dani |

**Our Sunday ≈ 38-41** [L], against score-model §4.8 case B (36.4 at 00:30 with the ladder at 0.50; 34.7 in the current file
after the 01:05 ladder correction to 0.27). The gap is the fodder ladder (≈ 0.45 vs 0.27) and the flags.

### A. Saturday tail (case A only)
- **Points:** +1-2 Saturday pts from v10 VC (score-model §4.8: +2.0 mean) on top of the +2.2 mm flip [L].
- **First actions:**
  - 09:00:15: confirm `round` = 2.
  - Fire the club v10 pairs, buyers' open bids first: RET-09 t07/t08 → t09, SAL-05 t08 → t07, SAL-02 t09 → t07.
  - **No** dealer deals (the Saturday ladder is capped), no flags (Saturday's ≈ 3 are spent), no cash team trades (≈ 6 np of
    headroom left), no CHA prep beyond staging, and **don't open the pack** (CHA isn't released).
- **Failure modes:**
  - A negative-VC fill wipes the Saturday market part (3 venues lost theirs this way on Saturday).
  - **SAL-11 20252 fills into the capped Saturday trade part**: cancel it **before** the first tick.

### B. Market Test (bench)
- **Points:** 11.25 (stall = 0.5 per session) [V].
- **Action:** none. Keep v10 open all day; never close or replace it. No board venue: 51 board-venue sessions, 0 above the stall,
  5 below [V, market-test-audit §1a]; 270 P locked; broker-down risk.
- **Cheap upside:** ask the desk once (Dani, 09:00): "If one venue beats the stall's efficiency and nobody else does, does it get the
  full Market Test points?" Revisit only if yes **and** ≥ 270 P is idle after CHA, for the 13:21 session at most.

### C. v10 real trades (VC)
- **Points:** 3-5 expected, cap 7.5 at VC ≥ the top-3 mean.
- **Target:** ≈ 40-50 net VC by the close, front-loaded, **zero negative trades** (market-test-audit §3b). market-sunday's "170 at
  the close" overstates it 3-4×.
- **First actions (09:00-09:05):**
  1. RET-09 t07 or t08 → t09 (page finisher, est. +68 VC low). Resolve the seller conflict in person at 08:45: whoever holds a
     real spare. t09 posts the open bid on v10 first.
  2. Ask t15 (and t01 for MAL-11) to post their MAL bids on v10. t10's dump bots may fill them there: a rival seller is fine at
     VC ≥ 8 with its own gain ≤ 10 P (directive 17:40). Never message t10 (directive 17:45).
  3. SAL-05 t08 → t07; SAL-02 t09 → t07 (or as a swap).
  4. Ask t08 and t16 first to list on v10 (directive 01:35). The heavy open-offer bots are t13 (1,157 listings), t08 (1,098),
     t06 (870) and t16 (820) (audit-why-we-lost §6.1). Per 01:35, don't chase t06 or t13, but welcome their listings. It's an ad, not
     strategy: "v10: 0 %, crossed every tick, buyers for RET/LAT/SAL commons there."
- **Rules:**
  - Duplicates or set-dumpers → first-copy collectors only.
  - Page finishers only for teams > 5 below us.
  - **No cash bonuses** (organisers: "volume and friends count for nothing"; fair play: "feeding another team on purpose … count
    for nothing until the organisers have looked").
  - Our own spares go as **open asks on a non-rival member's venue** (directive 01:35: open asks fill 10× more than addressed
    ones). But **never a big-VC trade there** (a page closer, a rare, a CHA card): VC on a member's venue can lift it into the top 3,
    and the top-3 mean normalises our own VC. Big trades of ours go to El Rastro.
- **Failure modes:**
  - One wrong-direction trade (buyer values < seller) subtracts in full.
  - Pairs priced off matchmaker multipliers are [L]: require a live bid from the buyer as proof of want.
  - Early-Sunday snapshots overstate trading venues until the first bench (display quirk, audit §2).

### D. Dealer ladder (fresh round; best 3 per dealer; level/45 per full-share slot)
- **Points:** 7-8.5 if L ≈ 0.45 against M ≈ 0.5 (the Analyst's 0.27 gives ≈ 4.9).
- **Slot plan** (all 0 neg unless marked):

| Dealer (max/slot) | Slot 1 | Slot 2 | Slot 3 | Expected L |
|---|---|---|---|---|
| **Pícaros L4 (0.089)** | CHA-09 buy, open 42, +2, target 48-52, ≤ 54 (≤ 57 after one walk) | CHA-10, same | a spare LAV common sale at ≥ 5 (≈ 0.5 share) as a **placeholder**; upgrade after 11:55 with idle cash: CHA-11 buy at ≤ 140 (value 288, 0 neg, ≈ full share) | 0.19-0.22 |
| **Pilar L3 (0.067)** | fodder uncommon #1 at 19-20 (ask 30, −1/−2; take her number + 1) | fodder uncommon #2 | RET-11: ask 260, −6..−8, floor 198 (≈ 20% she reaches it); else a pack rare dup at 50-56 or fodder #3 | 0.10-0.15 |
| **Chato L2 (0.044)** | **sell** fodder uncommon at 15-16 (ask 32-40, −1/−2, 8-10 rounds; he mocks ±1 on buys only) | fodder #2 | a pack rare dup at ≈ 49 | 0.04-0.10 |
| **Abuela L1 (0.022)** | CHA-01 at 8-9 | CHA-02 | CHA-03 | 0.05 |
| **Ernesto L5 (0.111)** | only a pack epic we value ≤ 120 (LAT-11, a RET-11 dup), or the surplus loop (G). **Needs Lucas to lift the 00:50 GUARDRAIL "Ernesto: no deals"** | — | — | 0-0.1 |

- **Never Chato buys at list** (0 at 26, n = 18). Never above list. Never a dealer for the CHA page's last card.
- **Fodder** (approved by the directive labelled 02:30: team → dealer only, cards we hold 0 copies of, price + fee ≤ first-copy
  value, sell only above the dealer's opening, ≤ 3 per level). Sources, cheapest first:
  1. silver pack + Workshop (T0, free);
  2. Abuela gifts (warm lines; 18% of kind replies carry one);
  3. **maker bids at ≤ 12 P for LAT-06/07/08** on a 0 % member venue or El Rastro (first copies, value 12.5). Fills are unproven:
     only 1 of the 8 Saturday LAT-uncommon team trades went at ≤ 12 [V feed]. **Never** SAL/RET/LAV/CHA page cards.
- **Where this file differs from the 02:30 directive:** run fodder **in parallel from T0** (separate dealers and threads; it doesn't
  slow the CHA buys), and open the pack **before** the rares, not after.
- **First actions:**
  - 09:00:30 pack; 09:00:45 Workshop.
  - 09:01 three threads in parallel: Pícaros CHA-09, Abuela CHA-01..03, Pilar RET-11 (or fodder first if the pack gave an uncommon).
  - 09:02 fodder bids.
- **Failure modes:**
  - The Pícaros don't stock CHA rares → book bids 70 → 90 and Chato ≤ 77 → ≤ 100 (cha-plan).
  - Bait and switch → `--offer-only` (§1.3).
  - A low share from jumping to the dealer's number → small steps, take their number + 1.
  - A 4th deal at a full level only counts as an upgrade (best 3).
  - Abuela, the pack or the Workshop handing us the CHA **last** card → no pack, Workshop or Abuela thread once CHA is 9/10.

### E. Team trades: the CHA page and its closer, flags
- **Points:** 7-9 if T ≥ N (≈ 40-125).
- **T sources:**

| Source | np | P | When |
|---|---|---|---|
| **Flags on Pícaros lies** (words ≠ structured card/price, "stopped printing", "last one in Madrid"; never finality/deadline talk) | +10 each, ≈ 3 if the cap reset per round [?] | 0 | in the CHA rare threads, 09:01-09:30 |
| CHA closer (last card, from a team, as maker) | +50 (cap) | ≤ value − 50: 72 common / 96 uncommon / 168 rare | 10:30-12:30 |
| CHA team buys (CHA-04 ≤ 12, CHA-07/08 ≤ 30) | +4-16 each | ≈ 60 | 09:02 → |
| Fodder bids (LAT uncommons at 11-12) | +0.5-1.5 each | ≈ 36 (comes back from Pilar/Chato) | 09:02 → |

- **First actions:**
  - 09:01 flag check on every Pícaros message. First clean lie → `POST /api/flags`, then read `neg_points` 2 ticks later: +10 means
    the cap reset (keep going to 3 scored), 0 means stop, −10 means stop.
  - 09:02 one write to `run/book.json`: CHA-04 (9 → 12), CHA-07 (24 → 30), CHA-08 (flat 24), CHA-05 (flat 9, the designated closer),
    all El Rastro, `page_closer` and `last_card` on. **No CHA-09/10 team bids** unless the Pícaros have no CHA rare by 09:20. CHA-06
    goes to the book if no team fills it by 09:45 (Abuela 20-22 after that).
- **Closer rule:** whichever card a non-rival team actually holds once we're at 9/10. The book's `last_card` jump to value − 50 is
  automatic. Never a rival seller for the closer (+50 for us, and its gain feeds a rival).
- **Failure modes:**
  - No team ever sells the last card (the bonus is lost) → keep both CHA-05 and CHA-08 as team-only, and buy the other from Abuela
    at 12:30 (cha-plan step 4).
  - The 9/10 signal is public in the feed and a holder can hold out → the bid jumps straight to value − 50, so price doesn't matter.
  - Pack drag on the closer → the pack is open by 09:01.
  - A wrong flag → −10.

### F. MAL page close (gated, not scheduled)
- **Points:** +44 np (MAL-07 closer from t15 at ≈ 20: 17.5 + bonus 46.4 − 20) minus ≈ −16 to −24 np if MAL-09/10 come from the
  Pícaros (Saturday MAL rares 57-61 vs our value 49) [V prices] → **net ≈ +20-28 np**, worth something **only while T < N**.
- **Gate (10:30, Chief, on the Analyst's M5 test from live-tuning §1):** a positive team trade that still moves our board negotiating
  (field drift removed) means T < N → **go**. ≈ 0 means capped → **no-go**: MAL-09/10 stay unbought, MAL-08 is held
  (GUARDRAIL 00:50), and the cash goes to ladder upgrades.
- **Conflict:** t15 and t09 bid for MAL-09/10 themselves (page 8/10 for t15). Brokering those rares to t15 on v10 is worth VC to us
  at 0 P, and buying them ourselves competes with a club member. With the gate a no-go, broker them instead.
- **Failure modes:**
  - t15 won't sell MAL-07 → the close is impossible, and we hold two rares at a loss. So buy MAL-09/10 only **after** t15 confirms
    MAL-07 in person.
  - A dealer delivers the last card → the bonus is lost.

### G. FLIP arbitrage and "trade surplus → ladder"
- **Points:** +0.5-2.
- **Buyer-first flips** (reactor rule): dealer price ≤ list, a live non-rival team bid ≥ dealer + 30, our value ≤ the dealer price.
  - On Sunday: a 2nd CHA rare from the Pícaros (≈ 52) into a non-rival CHA bid ≥ 85: buy −24 np (2nd copy 28), sell +50 cap →
    **net ≈ +26 np, + an L4 slot**, and +33 P on a 0 % venue (+27 P as an El Rastro taker, after the 6 P fee). Same for epics into
    team bids ≥ 170.
  - Never against a complete page, never for a rival, never without the bid on the book.
- **Surplus → ladder** (live-tuning §3, Chief's go each time): once M5 says T ≥ N, small dealer losses are free up to the surplus.
  Candidates, best ladder per np:
  1. RET-11 → Pilar at 175-197 (L3 full share, −1 to −23);
  2. MAL rares Pícaros (57-61) → Pilar (50-56): L4 + L3, ≈ −10 np and −5 P each;
  3. MAL-11 Pícaros (≈ 140) → Pilar (≈ 140-160, 0 np) or Ernesto (settled 116-120, finals up to 129; L5): ≈ −14 to −24 np. The
     Ernesto leg needs Lucas to lift the 00:50 GUARDRAIL.
- **Failure modes:**
  - Surplus misread (M5 needs a clean window, n ≥ 2) → losses count in full.
  - The Pícaros bait and switch on epics (8 rare-for-epic offers on Saturday) → `--offer-only`.

### H. Duels III + Final
- **Points:** 7.5 expected (Saturday 6.9).
- **Actions (Aleks's lane):**
  - Duelist live by **10:30** (chief-handoff, sunday-plan).
  - Duel Lab set: v2 or SAFE, with its own gates. Opus `--effort low`; fix the failover budget (20 s > the runner's 10 s).
  - Smoke test: 4 concurrent duels at 15 s, p95 < 9 s.
  - Duelist audit S2 (timeout fallback) fixed before 11:00.
- **Our part:** at 10:45 throttle every keyed daemon that isn't book/trader (collector, opps, matchmaker, reactor, analysts' keyed
  reads) to ≤ 1 req/min until each wave ends. No new dealer threads in the waves (§4 has enough dealer time without them).
- **Failure modes:**
  - Latency: 29% of decisions were over 10 s in Duels II.
  - 429s from our own bots.
  - A params regression → the gates step back after 8 duels.

### I. Denying rivals
See §7. No denial buy is ≥ 0 for us (deny-list). The working denials are the v07 flow and never selling page cards, CHA cards or LAV
spares to rivals.

## 3. Ranking (where the next unit of effort goes)

1. **Ladder fodder pipeline + rares at t+1** (D): +2-4, cash-neutral, no dependency on other teams.
2. **Trade part to N** (E): flags first (free), then the CHA closer, then cheap team buys. Stop buying neg once M5 says capped.
3. **Duels** (H): the largest absolute part. Our marginal moves are latency and leaving the key free during waves.
4. **v10 VC** (C): free, up to 7.5, and the only lever that also cuts t10 (v07 flow).
5. **Idle cash → ladder upgrades** (G, CHA-11): only after 11:55 and only if L < M.
6. **MAL close** (F): gated; likely a no-go.
7. Market Test (B), Saturday tail (A), denial buys: nothing to do beyond the rules above.

## 4. Minute by minute, 08:45-10:30

Tick = 15 s. "T0" = the first tick with `round` = 3.

### Case J (round 3 at the open, ≈ 80%)
| Time | Who | Action |
|---|---|---|
| 08:30 | Builder | Trick guard in `abuela_bot._haggle` + `chato_steady` (offer `give` card ref and rarity == topic, else no accept); tests green; Operator restarts nothing yet |
| 08:30 | Aleks | Pull, full suite, Duel Lab set + duelist audit must-dos; smoke test at 15 s; live by 10:30 |
| 08:45 | Operator | Heartbeat, `git pull` (no stash), `tools/daemons.sh status`. **Cancel 20252 (SAL-11), 19979 (LAV-03 → t04), 19981 (LAV-04 → t01) now**; if refused while closed, at the first tick. Stage the `run/book.json` CHA entries (§2E) in a scratch file: commons, uncommons and the CHA-05/08 pair only. Stage the fodder bids: LAT-06/07/08 at 11, floor 12, El Rastro |
| 08:45 | Lucas, Dani | In the room: (1) RET-09 seller (t07 or t08) and buyer t09, buyer bids first; (2) t15: will it sell its spare MAL-07, and does it want MAL-09/10 bids on v10?; (3) SAL-05/SAL-02 → t07; (4) ask t08/t13/t16/t06 bots to default to v10 |
| 08:55 | Operator | `/api/clock` (still paused), `/api/schedule`. Tell the Chief: "case decided at 09:00:15 from `round`" |
| **09:00:00** | — | Doors open |
| 09:00:15 | Operator | Read `/api/clock` (round, t_hours, tick_seconds), `/api/catalog` (CHA `released`), `/api/me` (neg 0? ladder 0? cash 392), `/api/schedule` → wall times |
| 09:00:30 | Operator | **Open the silver pack**: `POST /api/packs/1013/open` (check the id in `/api/me`). Log the cards. A CHA card → drop its book entry; a dup uncommon or rare → fodder |
| 09:00:45 | Operator | **Workshop**: `POST /api/taller {"assets": [LAV-02 spare, LAV-02 spare, LAV-03 spare]}` → 1 uncommon (CHA → page; else fodder) |
| 09:01 | Operator | **Pícaros:** `chato_steady.py CHA-09 --dealer picaros --cap 54 --open 42 --step 2 --offer-only --cash-floor 0`. First message: the estampita line **with** 42 (never text-only). Flag rule on every message (§2E) |
| 09:01 | Operator | **Abuela:** `abuela_bot.py --dealer abuela --cards CHA-01,CHA-02,CHA-03 --max-buy 9 --deals 3 --offer-only --cash-floor 0` (cocido line in the first message) |
| 09:01 | Operator | **Pilar:** with a fodder uncommon from the pack or Workshop, sell it (ask 30, −1/−2, take ≥ 19). Otherwise RET-11 (ask 260, −6..−8, floor 198, walk once) |
| 09:02 | Operator | Book: one write adding the staged CHA entries (no rares) + the fodder bids (≤ 12 P incl. fee, maker, 0 % member venue or El Rastro). Check `expires_tick − created_tick` on the first post |
| 09:02 | Lucas, Dani, Market | v10 pairs live (§2C), buyers' bids first; the Market logs each fill's VC sign |
| 09:03 | Operator | +150 → `/api/me` cash ≈ 542 − spent |
| 09:06-09:10 | Operator | CHA-09 settles (expect 50-54): check the settlement card = CHA-09 and Δladder ≈ +0.06-0.08. Open **CHA-10** at once (after the bots' 10-tick reopen gap if it's the same dealer) |
| 09:10 | Operator | **Chato:** sell fodder uncommon #1 (ask 36, −2, floor 15; slow, 8-10 rounds). Never buy from Chato at list |
| 09:15 | Chief | Flags tally: did the first scored flag pay +10? Then the cap reset → keep going to 3 |
| 09:15-09:20 | Operator | CHA-10 settles. **No CHA rare stock or walks above 57 twice** → re-add the CHA-09/10 book bids (70 → 90) and run Chato ≤ 77 → ≤ 100 |
| 09:20 | Operator | Pícaros slot 3 placeholder: sell the LAV-04 spare at ≥ 5 (open 12, −1). It is our last LAV spare after the Workshop |
| 09:21 | — | Bench (stall), if re-anchored. Nothing to do |
| 09:25 | Operator | Abuela: 3 CHA commons done by ≈ 09:30. Pilar: 2nd fodder or RET-11 |
| 09:30 | Chief + Analyst | **Checkpoint 1:** CHA count (target 5-6/10), T so far (flags), L so far (target ≥ 0.25 by 09:45), cash, first VC fills, first round-3 snapshot (board every 10 ticks) |
| 09:30-10:00 | Operator | Pilar slot 2-3; Chato fodder #2; uncommon fallback: if CHA-06/07 are unfilled by teams at 09:45 → Abuela CHA-06 at 20-22 (an L1 upgrade only if better than a common's share) |
| 09:45 | Lucas, Dani | 2nd wave of v10 pairs; check each pair's first fill VC sign |
| 10:00 | Operator | Book steps bids (automatic; CHA/MAL buys only through run/cha_book.json / mal_book.json). The trader stays sell-only (`--cash-floor 9999`, directive 01:35). FLIP digest (reactor): any non-rival CHA rare bid ≥ 85 → the 2nd-copy flip on the Chief's go |
| 10:15 | Operator | CHA should be 8/10. Designate the closer: the card a non-rival actually holds. Its bid jumps to value − 50 by itself at 9/10 |
| 10:30 | Chief | **Checkpoint 2 (gates):** (a) MAL gate on M5; (b) surplus → ladder go/no-go; (c) dealer threads to wrap by 10:45; (d) daemon throttle plan for 10:45; (e) desk answers (§9) |

### Case A (Saturday tail, ≈ 15%)
| Time | Who | Action |
|---|---|---|
| 08:30-08:55 | all | As case J (the trick guard, the duelist, the cancels **before** the open, room pairs) |
| 09:00:15 | Operator | `round` = 2 → case A. Verify 20252/19979/19981 are gone. **Don't** open the pack, use the Workshop, open dealer threads, flag, or post CHA bids |
| 09:01 | Lucas, Dani, Market | v10 pairs (count for Saturday's VC; base mm +2.2). Strictly positive pairs only |
| 09:01-T0 | Operator | Idle on the game. Stage case J; watch `/api/clock` and `/api/schedule` every 5 min and the announcement feed |
| 10:17 / 10:38 | — | Hard bench / bench (stall), if the clock just runs on |
| T0 | Operator | Run case J from its 09:00:15 row, shifted to T0. If T0 is late (> 11:00), compress: rares → Abuela commons → book → fodder; skip Chato (slow); Pilar 2 slots max |
| T0 + 2 h | Aleks | Duels III per the re-read schedule |

## 5. After 10:30 (skeleton)

| Time (case J) | Action |
|---|---|
| 10:45 | Last dealer deals settle; throttle keyed daemons; book and trader keep running (team fills need no threads) |
| 11:00-11:51 | Duels III. Lucas and Dani keep v10 pairs moving (no key load). The closer can fill during the waves |
| 11:55 | **Checkpoint 3:** CHA closed? MAL gate final. Idle-cash rule (§8). Pícaros slot-3 upgrade (CHA-11 ≤ 140) if L < M and ≥ 150 P is idle |
| 12:00-13:40 | Ladder upgrades: Pilar/Chato fodder, the surplus moves on the Chief's go, buyer-first flips. CHA-08 from Abuela at 12:30 if both pair cards are still missing (cha-plan step 4) |
| 13:21 | Bench (stall) |
| 13:45 | All dealer deals settled (warning ≈ 13:48; dealers close ≈ 14:00) |
| 14:00-14:27 | Grand Final (throttle again) |
| 14:30-15:00 | Last v10 pairs only; no new cash commitments |

## 6. Holes, wrong assumptions and missing levers in the current plans

1. **Clock conversion** (score-model §4.7, chief-handoff, sunday-plan): 15 s ticks don't speed up game hours [V]. **Fixed at
   01:45-01:50.** Duels III ≈ 11:00 is the earliest; pauses push it later and the 15:00 close can cut the Final.
2. **CHA rares on a 30-60 min delay** (dealer-lab FAST-START "t+120": 30 min; cha-plan "~10:00"): supply is global and will be raced
   (SAL precedent) [V]. With CHA public bids now capped at dealer prices (6110b0e), waiting for teams buys nothing.
3. **"Trick guard mandatory" is not implemented** [V code]. Directive 00:25 assumes it exists.
4. **The ladder's L2/L3 gap was treated as structural** (score-model 01:05: "no spare rare/uncommon for L2/L3"). **Now approved as
   fodder** (the directive labelled 02:30). Our Saturday L3 slots came from exactly this kind of selling: MAL-07 19, MAL-06 19/20 (one
   from the Workshop), SAL-08 23 and MAL-09 56 to Pilar [V, score-model §2 table, STATUS dealer table]. Still open: start it at T0,
   not after the CHA buys.
5. **dealer-lab §4 item 4 "the silver pack stays unopened"** contradicts cha-plan ("open after the release"); the 02:30 directive
   says "after the CHA rares". Open it at T0 + 2 ticks, **before** the rares: a CHA rare from the pack saves a 52 P buy, while one
   drawn after we bought ours is a 2nd copy worth 28.
6. **The MAL close is gated on cash (≥ 150 P left), not on value.** Its net +20-28 np only counts while T < N. It also needs Pícaros
   MAL rares that sold at 57-61 on Saturday (≈ −16 to −24 np for the pair at our 0.7), and it competes with t15/t09 for the same
   rares. The gate should be M5 (§2F).
7. **The SAL-11 cancel at "the first tick"** (directive 00:50) can race t04's accept on that tick. Cancel at 08:45 if the server
   allows it while closed.
8. **dealer-lab FAST-START t+1, "open the Pícaros/Abuela thread with the egg line, no price, then close it":** it spends a
   conversation and the bots' 10-tick reopen gap, and Ernesto/Chato read text-only as spam. Put the line in the first priced message.
9. **The club:** cash bonuses (≤ 75 P) buy volume, not value, and invite a fair-play review. Big-VC trades of ours on members'
   venues lift the VC normaliser (small open spares are fine, directive 01:35). market-sunday's VC target (170) is 3-4× too high
   (audit §3b), which pushes toward risky pairs.
10. **Ernesto "no deals"** (GUARDRAIL 00:50): right for what we hold. But the L5 slot is ⅓ of the ladder reference. If the pack draws
    LAT-11 or a RET-11 dup, or the trade part shows surplus, **ask Lucas to lift the GUARDRAIL for that one deal**
    (dealer-lab-ladder §6 option 1; §2G here). Only Lucas changes a GUARDRAIL.
11. **Pilar targets:** RET-11 at ≥ 198 is a ≈ 20% shot (non-SAL epic precedent 140; SAL 179-199 in the fever). Don't let her three
    slots depend on it: fodder first, RET-11 as the upside. Below 198 only through surplus → ladder.
12. **Idle cash:** after CHA ≈ 250-280 P (RET-11 may add 198+), ≈ 200-250 P sits idle. "Only deals score, never cash you hold" [V].
    The plans keep a reserve with nothing to spend it on.
13. **Rate limit during duels:** 5 req/s per key is shared by the duelist and ≈ 10 daemons that poll per tick. A tick is now 15 s, so
    they poll 2× Saturday's rate. Throttle at 10:45 and 13:55.
14. **Abuela gifts, the pack and the Workshop can deliver the CHA last card:** none of them at 9/10.

## 7. Legal ways to slow Team 10 and the other rivals

| # | Lever | Hits | How (transactional messages only, no strategy) |
|---|---|---|---|
| 1 | **Pull flow off v07** | t10's VC (7.5 of its 10.6 lead) | Club members (t08: 204 v07 listings, t04: 55) list on v10. Ask the open-offer bots (t13, t08, t06, t16) to default to v10. t06 made 6 of v07's 11 fills as maker; an ad to t06 for v10 is neutral for t06 and moves VC from t10 to us. Never one offer of ours on v07 (we were maker on 4 of its 11 fills) |
| 2 | Rival-seller pairs on v10 | t10 gets ≤ 10 np, we get VC ≥ 8 | t10's MAL dumps (MAL-09/10/11) into t15/t01 bids posted **on v10**; no message to t10 |
| 3 | Never feed a rival's page | t12 (MAL-08), t03 (LAV-02/04), t06 (LAV-05/08), all rivals' CHA | Hold MAL-08 (GUARDRAIL 00:50). LAV spares go to the Workshop or the Pícaros, never to t03. No CHA dup ever to a rival; non-rivals only |
| 4 | Win the CHA rare race | everyone | Our 2 rares at t+1 (§1.2). No denial buys of extra copies (a 2nd copy is worth 28: −24 np) |
| 5 | Out-duel | t10, t18, t03 (duel-heavy) | Latency + params; keep the key free during waves |
| 6 | Denial only at ≥ 0 | t12/t18/t03 | The Analyst's 9/10 alerts; a denial buy only when its own np ≥ 0 (deny-list: none today) |
| 7 | Nothing to report | t01 ↔ t10 | The feed shows one t10 → t01 trade (MAL-07 at 14, on v10) [V]. No feeding pattern, so no desk report |
| 8 | Not doing | — | Engineering negative-VC trades on v07 (needs our offers on a rival venue and our own losses), wash trades, paid volume, key sharing |

## 8. Live decision rules (Operator acts; the Chief only on escalations)

- **M5 trade-part test** (Analyst, every 15 min from 09:30): Δ board negotiating per np on a clean window. Live (≈ 0.05-0.2 board/np)
  → keep buying np: closer, CHA team buys, MAL if gated in. ≈ 0 → **stop paying for np**; go fodder, surplus → ladder and flips.
- **Ladder test:** our L vs the Analyst's M estimate. L < M → idle cash goes to ladder (CHA-11 ≤ 140 at the Pícaros, fodder bids,
  the surplus loops). L ≥ M → stop dealer work except the CHA buys.
- **VC stop:** any v10 fill that lowers `mm_points` → pause that pair type at once.
- **Flags:** stop at the first 0 or −10.
- **Idle cash at 11:55:** cash − (closer max + 30 reserve) is spendable. Order: CHA-08/05 at once if still missing (ensures the close)
  → ladder upgrades if L < M → SAL-11-type team buys if T < N (from non-rivals, ≤ value − 15) → nothing.
- **Never:** a CHA last card from a dealer, pack or Workshop; a page-card sale; a rival venue; a dealer buy above list; Chato buys at
  list; a gold pack or legendary; a text-only message to Chato or Ernesto.

## 9. Desk questions (Dani, 09:00, one line each)
1. Does the flag cap (≈ 3 scored per team) reset with round 3?
2. Market Test: does one venue above the stall's efficiency get the full points for that session?
3. Do duel conversations count toward the 6 open conversations (Q6, still open)?
4. Round 2's final score: the live state at the round change, or the last snapshot? (Our mm went −5.2 → +2.2 at the close.)
