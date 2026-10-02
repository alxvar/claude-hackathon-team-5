# Saturday plan (Team 5) — written Sat 00:45 from 10 agent reports + 4 independent verifications

Labels: **[V]** verified on raw data or rules · **[L]** likely · **[?]** open (ask the desk). Sources are in
`archive/fri/` (raw data), `intel/GAME.md` (facts) and the agent reports summarised here.

---

## 1. The game on one page

Score = **Negotiating 30 + Market-making 30 + Judges 40.** Each day is a round; the game part averages
(0.5·Fri + Sat + Sun) / 2.5, so **Friday is 20%, Saturday 40%, Sunday 40%** [V]. Sunday's 6 hours weigh as much
as Saturday's 14. Scores are **relative**: the leader is pinned at 30.0 Negotiating, and a team that does nothing
falls 0.4-1.5 per snapshot when others gain [V]. The 5 teams with zero team trades finished 13th-18th [V].

Four different games run in parallel on one key. Each has its own scoring and its own best play:

| Game | What scores | Best play |
|---|---|---|
| **Team trades** (El Rastro) | Δ(our whole collection value, incl. unopened packs and page bonus) − price − fee if we accept; capped at ~50 per trade [V cap exists, form ?] | Volume as maker; page-completing trades; never feed climbers |
| **Dealers / ladder** (Abuela, Chato, 3 more coming) | Ladder: share of the dealer's price range, best 3 deals per level, higher levels weigh more. `neg_points`: min(0, ΔV − price): a dealer deal never adds, only subtracts [V] | Patience to the `final`, only at ≤ our value, never first prices, never packs |
| **Duels** (I 11:30, II 18:00, III Sun, Final Sun) | Surplus × (1 − decay)^rounds, rounds = min(our priced offers, theirs); no deal 0; outside limit negative [V] | Anchor, close inside limit fast, never let an in-limit offer expire |
| **Market-making** (benches every 2 h) | Share of the possible gains our venue's matching realises; the free stall earns half; full = mean of top 3; + value created between other teams on our venue [V rules] | Record first, decide on evidence; a broken broker scores 0 |

1 `neg_point` ≈ **0.16 board points** on Friday [V, ticks 110-155]. Our +50 page trade moved us #10 → #5.

### Measured formulas (use them before every trade)
- **Team trade** [V]: score = min(cap, ΔV − p − f_taker). ΔV includes the page bonus and the drag on unopened packs.
  `parties` = [maker, taker]; only the taker pays the fee (5% + 1 P per card) [V].
- **Dealer deal** [V]: score = min(0, ΔV − p). Gains are clipped to 0, losses count in full.
- **Cap** [V that it exists]: our page-completing buy (value 99.1, paid 8 + 2) scored exactly +50.0. Four forms
  still fit: flat 50 · gain ≤ 5×book · gain ≤ 5×(p+f) · value ≤ 6×book. **The RET finish is the test** (§4B).
- **Open your packs first.** An unopened pack shifts every trade's score by 1-4 points [V].

---

## 2. 09:00 decision tree (operator, first 10 minutes)

| Check | API field | If A | If B |
|---|---|---|---|
| Clock | `/api/clock` `t_hours`, `round` | **≥4.0 / 2 = jump**: RET + 150 P at 09:00-09:03, bench 10:00, Duels I 11:30 | **2.65 / 1 = resume**: bench 3.0 at ~09:21 (round 1's ONLY bench, on the free stall), RET + grant ~10:21, every event +81 min |
| Schedule | `/api/schedule` `upcoming` | 3.0 bench gone or re-timed | 3.0 bench still listed |
| Reset | `/api/me` `neg_points`, `ladder_points` right after the `round` event fires (not at 09:00 under resume) | ~0 = **reset**: ladder is cheap points again, every trade from zero, move first | 67.8 / 0.064 = **carry**: the LAV page keeps counting |

Evidence so far favours **resume**: the big screen's "Coming up" reads *Market Test in 21m, New round in 1h 21m* at the
paused game clock 2:39 [V screen], i.e. ~09:21 and ~10:21 if nothing is re-anchored. No organiser statement either way.

**The trader (`loop.py`) and the analysts are stopped overnight on purpose** (they would start on Friday's premises with
an unopened grant pack). The operator starts them only after: clock checked → grant pack opened → reset checked.

**This plan supersedes every `intel/directives.md` block written before Sat 00:45 where they conflict:**
cap test = a RET common at p ≈ 12 (not an uncommon at ≥20); RET rares from Chato with the 80-84 protocol (not "up to 90");
cash floor per §4B (GUARDRAIL pending Lucas's word).

---

## 3. Questions for the organisers' desk (Dani, 09:00 sharp, answers into `team/dani.md`)

1. Saturday clock: resume at 2.65 or jump to 4.0? Does the 3.0 Market Test run, and in which round?
2. Do `neg_points`, ladder and duel points reset each round?
3. Is there a per-trade cap on `neg_points`? Our page-completing buy scored exactly +50.0 where ~89 was implied.
4. Ladder: what defines a dealer's "price range" (opening, list price, or the conversation's secret limit)? Our three
   El Chato deals never moved `ladder_points`.
5. Market: split between bench and venue value; how points scale between the stall (half) and the top-3 mean; does
   closing a venue bring the stall back; does the bench charge fees.
6. Does a duel accept use the team's 1 accept per tick? Do duels count in the 6 open conversations?
7. Judging: format, time, length, criteria; do judges read the repo?
8. Levels 3-5: when, and the unlock rule. Does Abuela's "welcome price" (17 on a team's first deal) reset each day?

---

## 4. Playbooks

### 4A. Team trades — the main engine (uncapped count, ~0.16 board per point)
- **Be the maker.** A fill on our offer uses THEIR accept and THEY pay the fee. Keep **20-30 live offers** (limit 30;
  12 new per tick). Friday we had ≤8; Team 6 listed 112, Team 8 81 [V].
- **Price at the bid level.** Clearing prices all Friday [V]: common 9 (LAT 7.5), uncommon 24.5 (MAL 26, SAL 24.5,
  LAT 21.5), rare 70 (53-80). Only 5% of asks and 9% of bids filled; filled bids took a median 4 ticks. Reprice any
  offer unfilled for 10 minutes.
- **Sell page-completers at the buyer's page price** (biggest new lever). A team one card from a page values that
  card with its bonus (ours read 99.1 for a common). Our spares are worth 2-3 to us: second LAV-02, LAV-03, LAV-04,
  second SAL-02, second LAT-04. Price ≈ 45-50 (about half the buyer's implied gain), addressed `to` the team. Known gaps
  [L, field report]: t14 (LAV, missing one of 01/02/07/08), t04 (LAV-09: we can't), t02 (SAL-09), t08 (SAL rares),
  t18 (LAT-09/10), t17 (MAL-09). No API shows other teams' albums (only `album_filled`, `pages_complete`): the best
  signal that a team lacks card X is that it **bids for X or asks a dealer for X**. `intel/sellable.md` (builder,
  §5) turns that into one line per opportunity for Dani.
- **Feeding rule.** Before any sale read the buyer's progress in that set (feed + `intel/teams.md`). A page-completing
  card (second-to-last or last) goes only to a team **≥ 10 points below us** and never to the top 4: at a 45-50 price
  the buyer books up to the cap while we book less. Friday's SAL-06 → t17 let them finish SAL (+6.25 board) and pass
  us [V].
- **Accept (taker) only** for: a page-completing card, or an ask below our value − 3 − fee.

### 4B. Pages — the recipe that worked (+40 net, #10 → #5)
1. Build every card but the last at ≤ our value (dealer buys score 0, never more than value).
2. Leave the **cheapest common** for last; buy it **from a team**. Check `value?card` before each step.
3. **RET page (Saturday)**: values common 11, uncommon 27.5, rare 77; bonus 72.9.
   - Commons: Abuela after rounds (~8-9) or teams at ≤ 8.
   - Uncommons: Abuela after 5-7 rounds (~21). Chato's 28-29 is above 27.5 (−1 each).
   - Rares: from teams at ≤ 74, else Chato at ~80-84 (−3 to −7 each, a dealer loss counts in full).
   - Cost ≈ 5×9 + 3×22 + 2×82 ≈ 275 P. Expected net ≈ +35 to +45 if the cap holds.
   - **Order: rares first** (scarce: 30 copies each, and teams with a high RET multiplier value them ~112 and will
     outbid us), uncommons next, commons last. If a rare is still missing at 15:00, stop and sell the RET cards we hold
     to RET collectors at their page price instead of finishing.
   - **Cap test with the last card:** a RET common at price ≈ 12 (p + f ≈ 14). Measured score 50 → flat/5×book;
     ≈ 70 → 5×(p+f); ≈ 46 → value ≤ 6×book. Log it in GAME.md immediately; it sets every later price.
4. **CHA page (Sunday, 18.0)**: values common 16, uncommon 40, rare 112 > dealer prices, so no dealer losses even on
   rares. Also buy CHA cards from teams below value (each scores value − price). Dealers close at hour 23.
5. **Cash**: cash scores nothing at the end. **GUARDRAIL needed (Lucas):** Saturday floor 200 → 100 for page buys,
   Sunday → 0 by 14:00. Fund pages by selling low-multiplier cards (MAL 0.7, LAT 0.5, SAL 0.9) as maker.

### 4C. Dealers and the ladder
- **Never** a first price, never a pack (Team 8's silver pack: −5.65 board, #3 → #9) [V]. Open free packs at once.
- **Chato protocol** [V, verifier 2]:
  - Buy uncommon: open 13-20, exactly +1 per round; he holds 33 for 2-3 rounds, then −1/round; final 28-29.
    Bid one under his standing offer (28 vs 29 accepted).
  - Buy rare: open 55-60, constant +2 to +4 (never +1: final 91-93; never jumps); bid just under his standing
    offer; expect 80-84 after 8-10 rounds (Team 4: 82 vs his 84).
  - Sell uncommon: open ≥ 39, step −2/−3, never go to 13 yourself; final 15-16 after 6-8 rounds.
- **Abuela** [V]: opens uncommon 29, pack 30, common 12; more rounds = lower (uncommon 21 after 5-7 rounds, pack 19
  after 8). First deal with each team was a fixed welcome price (17 pack/uncommon, 7 common).
- **Ladder** [?]: Abuela deals moved ours; our 3 Chato deals did not, and no variable explains which Chato deals
  count (desk Q4). Until answered: no Chato deal for the ladder alone; only when we need the card at ≤ value.
- **Levels 3-5**: early access needs 3 negotiated deals with the previous dealer (Chato: `early_min_deals` 3) [V].
  Three RET uncommons from Chato at 28 (−0.5 each) is the cheap way to qualify when level 3 is announced.

### 4D. Duels (Aleks) — fix before Duels I
Practice [V]: 11 deals / 24 finished; 9/12 closed when the rival spoke; ~14% of value lost to decay.
**Must-fix before 11:30** (≈1-1.5 h, with regression tests on `docs/duels/`):
1. Deadline trigger: decide when `ticks_left ≤ 3`; at ≤ 2, accept any standing offer inside our limit (in code, no LLM).
   Duel 181 must accept 73 by tick 143.
2. Decay-aware accept: accept an in-limit offer when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
3. Hold breaker: both sides still for 3 ticks with ≥ 3 left → force a decision (duels 103/104 deadlocked 10 ticks).
4. Silent rival: concede on a code schedule toward a floor (keep ≥ 30% of anchor-to-limit). Silence costs no decay;
   two "silent" rivals accepted our opener (accept-only bots).
5. Fix the prompt: decay is per exchange, not per tick (`agent.py:148,178`). Read session params from the payload.
6. **Close by sending the rival's own standing price** (and day) from `ticks_left ≤ 4`: then THEY accept and spend
   their accept, which avoids collisions when 6 duels end on the same tick.
- **Single point of failure**: Aleks's laptop on mains power with `caffeinate`; a stopped copy of the duelist on Lucas's
  machine as cold standby (never both running: one key). Check the spend limit on Aleks's API key before 11:00.
- **Duels II (18:00, `days`)**: payload shape never seen; test number/list/dict; compute day value in code; always send
  full packages; concede cheap days for price; ≤ 3 exchanges at 8% decay.
- **Sunday (15 s ticks)**: Sonnet strategist (Opus max was 14.2 s vs a 10 s budget).

### 4E. Market-making — record first, decide on evidence
- The free stall already ≈ the starter broker (half points). Our sim says even a perfect-information broker beats it
  by only +1.0-1.6 pp [L, model]; the real generator may differ. **That edge is not small in points**: the scale runs
  from the stall (half) to the top-3 mean (full), so +1.6 pp can be most of the other half. A board venue with its
  broker down scores **0**.
- **Decision for Lucas (cash + 270 P):** Option A (pre-mortem): build an `auto`-clone broker (no LLM: cross best bid /
  best ask every tick, as the stall does) + one improvement, supervised by `daemons.sh`; open a `board` venue at fee 0
  as soon as it reproduces the stall's matches on a recorded bench (replay equality). Downside bounded to "= stall"
  except downtime; it is the only way to capture any edge. Funds: the bond is refundable; sell low-multiplier cards.
  Option B: the gate below. **Recommendation: A**, because B's four conditions are unlikely to all hold before 15:00.
- **Before the first bench**: a read-only recorder of `bench_offers` (needs `starter_broker_key` from `/api/me` once
  the stall exists) + our `bench_efficiency` and every team's `market` after each session.
- **~14:15 gate** (Lucas): open a `board` venue at fee 0, between sessions, only if (a) broker v1 ≥ stall + 2 pp on the
  calibrated sim and replays, never < stall − 1 pp; (b) the leaderboard shows a rival board venue above the stall
  teams; (c) cash after RET allows 270 P; (d) supervised host. Otherwise reconsider Sunday 09:00 after the grant: the
  two Sunday benches carry all of round 3's bench score (each ≈ 4× a Saturday bench) [V].

---

## 5. Throughput and infrastructure

**Before 09:00 build only three things** (a builder eating 09:00-11:30, the only accept window before Duels I, is a
pre-mortem failure): the operator PID lock, the API spend preflight, and the market recorder (+ the `auto`-clone broker
if Lucas picks option A). Everything else is built during Duels I, when our bots hold accepts anyway.

| Fix | Why | Owner |
|---|---|---|
| `intel/sellable.md` generator: cross teams' bids and dealer threads (what they lack) with our spares and the feeding rule → one line per opportunity with price, buyer, pitch text; the watcher alerts Dani on a new line | Turns the room into targeted page-completion sales | builder, by 10:00 |
| Repricer daemon (no LLM) that owns our maker book within the hard limits: keeps 20-30 offers live, reprices after 10 min unfilled | The operator's context can fill or its Monitor expire; standing still = falling | builder |
| Read-only daemons (collector, watcher, metrics, dashboard) on **keyless** public routes | Keyless reads get 60/s per IP; the team key's 5/s is shared and we hit 429s at 21:50 and 21:54 | builder session |
| Watcher on `/api/events/stream` (SSE) | Instant reaction, fewer requests | builder |
| **Accept arbiter**: bots hold accepts only during SCORED duel sessions, and only on ticks where a live duel has an in-limit rival offer or `ticks_left ≤ 3`, read **directly from `/api/duels`** (git sync takes 2-8 ticks, too slow); include dealer `final` accepts | Today's rule freezes all accepts during any live duel (~3.3 h Saturday) | builder + Aleks |
| `metrics.md` attribution per settlement (not per score change) | Friday merged LAT-08 and LAV-05 into one window | builder |
| Operator PID lock; strategy session has no write path to the game | Two sessions operated at once on Friday | builder |
| Spend preflight for every API key + alert on the first analyst error | The $1 cap stopped the analysts 21:59-22:16 | builder |
| Analysts: timestamp the facts each recommendation rests on; run judge/strategist on events (round, new level, bench result) + a slow timer; scout only if it adds beyond metrics | Stale premises cost −11.8 (judge 21:55) and produced 6 wrong recommendations | builder |

---

## 6. Team and sessions

**Lucas** — decides, is the human channel, owns the story. Talks only to the strategy session. His leverage is what
agents can't do: the desk, other teams' humans, spotting what doesn't add up, the judges' pitch.

**Lucas's machine — three sessions, one role each, all started fresh at 08:45** in a VS Code window opened on the repo
folder (explorer + Git panel + terminals all in the repo):
1. **Operator** (unattended, Opus high): the only process that writes to the game. Runbook `intel/ORCHESTRATOR.md`.
   Liveness: if `team/lucas.md` gets no operator line for 15 minutes, push Lucas. Planned fresh restart (with handoff)
   during Duels I, when trading is quiet.
2. **Strategy** (Lucas talks here): reads everything, writes decisions to `intel/directives.md`, and for urgent ones
   also `SendMessage` to the operator (same machine: wakes it at once) [V docs].
3. **Builder**: §5 fixes, then the market recorder → sim → broker v1. Commits code, never trades.

**Aleks** — owns the duelist end to end (§4D fixes before 11:30, Duels II prep before 18:00), reviews the accept
arbiter. His Claude reads `intel/directives.md`, `intel/saturday-plan.md` and `team/lucas.md` on every prompt (the
team_sync hook) and writes `team/aleks.md` + `docs/duels/want_accept.json`.

**Dani** — three jobs with clear outputs, none of them in our critical path:
1. **Desk (09:00)**: the §3 questions, answers in `team/dani.md` within minutes; the strategy session turns them into
   directives.
2. **Page-completion broker in the room.** The operator publishes `intel/sellable.md` (our spares and asks, approved
   buyers, floor prices) and `intel/wanted.md` (cards we need, max prices). Dani uses her dashboard to find teams one
   card from a page and pitches with a concrete offer: *"You need LAV-02 to finish Lavapiés. It's on El Rastro
   addressed to you at 40; accept it and your page is done."* For buying: *"We pay 12 for RET-0x right now, bid is
   up."* She never improvises prices; she only points teams at offers that already exist.
3. **Judges' story (40%)**: get the judging format from the desk by 09:30; `docs/demo.md` skeleton; a screenshot of the
   dashboard and leaderboard at each round close; the decision timeline (from `team/*.md`, `LOG.md`,
   `intel/directives.md`). **Lucas and Dani draft the pitch during Duels I (11:30-13:05)** and rehearse during Duels II:
   those are the windows when the bots hold accepts and Lucas is least needed.

**Sync** [V docs]: same machine → `SendMessage` (instant) + files; across machines → git (hooks pull on every prompt,
the watcher emits teammate pushes within a minute). No tool shares another session's context: everything that
matters goes into a file.

---

## 7. Quality guardrails (the process that would have prevented Friday's losses)
1. **One deal per measurement window** for our own accepts and dealer deals (maker fills can't be timed: attribute them
   per settlement instead). Predict each trade's score with the §1 formula, log predicted vs measured.
2. **A new finding must explain every earlier measurement**, or it isn't a finding.
3. **Manual test before automating** any lever; no bot ever accepts a dealer's first price.
4. **One fact store**: `intel/GAME.md`, each fact labelled [V]/[L]/[?] with its source.
5. **Independent verification** (fresh agent) before any directive that moves > 20 P or changes a rule.
6. **Stale premises die**: a recommendation whose facts are older than the latest measurement is dropped.

---

## 8. Judges (40%) — gaps to close by Sunday
`docs/demo.md` and a clean "what we measured" table (LOG.md findings are out of order); an architecture diagram
(collector → metrics → analysts → directives → operator; human vs agent steps); a cost ledger; round-close snapshots;
a duel post-mortem; the market-making story. Raw Friday data is archived in `archive/fri/`.
