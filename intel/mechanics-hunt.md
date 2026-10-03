# Mechanics hunt: Sunday levers we don't use yet (Sun 01:05, read-only)

_Independent pass over `bazaar-kit/RULES.md`, `README.md`, `bazaar_sdk.py`, `intel/GAME.md`, `hints.md`, `eggs.md`,
`directives.md` (21:10 line read with the 00:35 correction: **Market Test 22.5 + real trades 7.5**), `score-model.md` §1-§4,
`data/feed.jsonl` (27,169 events, ticks 2-1445), plus the code in `tools/`, `agents/`, `broker/`. Keyless public reads at 01:05
(`/api/schedule`, `/api/levels`, `/api/venues`, `/api/catalog`, `/api/clock`); no keyed call, no write.
Labels: **[V]** read or measured · **[L]** fits the data, not proven · **[?]** open. "Sunday pts" = Sunday round points (×0.4 = final points)._

## 0. Ranked by EV (new levers only)

| # | Lever | Mechanic (source) | Sunday EV | Cost | Risk | Used now? |
|---|---|---|---|---|---|---|
| 1 | **Don't stop at the cap: every part is graded against the field's top, so value past our cap lowers rivals** | Relative scoring (GAME.md:4); VC = top-3 mean (market-test-audit §2) [V rescaling]; trade part N and ladder M field-relative [L] | Relative, not ours: **t18 / t12 / t03 −0.3 to −0.8 each** per +30 np or +0.1 ladder past our cap; **t10 / t06 / t14 −0.7 to −2** per +45 VC past the 40-50 target | idle cash (no terminal value), 0 P for VC and fodder | a negative trade still subtracts; needs us in the top 3 of that part | **VC: partly** (Lucas 01:10 club split). **Trades and ladder: no** (red team §8 stop rules) |
| 2 | **Probe `GET /api/cards/{id}` with the key, then sweep the ~1,190 asset ids** | SDK:168-170 "provenance chain"; RULES:19 "a history of every hand" | +0.3 to +1.0 if it names holders (CHA sourcing after pack buys, v10 pairs) [?] | 1 keyed GET to test; sweep ≈ 5 min at 4 req/s | shared 5 req/s: never during duel waves | **No** (holdings-audit open item 1) |
| 3 | **The server takes listings and cancels while closed** | RULES:107 "offers stay open"; feed ids 73274 → 73299 [V] | +0.1 to +0.5 (no first-tick race on bid 20252; staged bids first in the 09:00 queue) | operator minutes | staged offers show in the feed overnight | **No** (directives say "at the first tick") |
| 4 | **N-for-1 and cash-topped swaps** | RULES:62, 144 (≤ 50 items a side); `swaps.py:199-202` posts 1:1 cash-free swaps only | +0.1 to +0.4 | Builder change | as today's swaps | **No** |
| 5 | **Team threads for private terms (closer, club pairs)** | RULES:64-65; SDK:192-203 (`open_thread("t03", venue=...)`) | 0 to +0.5 [?] | one test thread | if public, nothing gained | **No** (0 team threads in the feed) |
| 6 | **Re-topic a dealer thread instead of walk + reopen** | SDK:209-220 (`say(..., topic=...)`) | 0 to +0.3 [?] | one test on Abuela | spam or cool-off | **No** |

Everything else examined is either already in the plan (§2) or dropped (§3).

## 1. The levers

### 1.1 Past the cap, value still counts against rivals [VC: V · trades, ladder: L]
- **Mechanic.** Each part is scored as `min(1, ours / field reference)`. The reference for real trades is the **mean of the top three
  venues** (market-test-audit §2: "the top venue is always at the cap exactly", two venues at the cap at once in 6 windows,
  never three). RULES:83 uses the same "mean of the top three" for the Market Test. When our number is in the top three, raising
  it raises the reference by Δ/3 and shrinks every rival below the reference by the same factor.
- **Evidence that it moves rivals.**
  - [V] VC: at tick 556 one t06 trade on v01 cut every other VC venue's market gap by about 29% at once (t14 11.86 → 10.60,
    t12 → 10.52, t10 → 12.06; score-model:30). 15 such common-factor moves are logged (score-model §3h).
  - [L] Trades: at snapshot 350 every idle team rose together when t02, then a top trader, lost ~15 np (score-model:256).
  - [L] Ladder: our negotiating sat flat at 21.88 over snapshots 850-890 while our ladder rose +0.064 and the field drifted
    −0.1 to −0.2 per snapshot (score-model:286).
- **What the plan does now.**
  - VC: Lucas's 01:10 directive already uses this ("concentrating VC on v10 raises the top-3 mean that v07 is scored against").
    But the 00:35 directive still caps the target at 40-50 net VC because "above the top-3 mean earns nothing", and
    market-test-audit §3b and red team §C repeat it.
  - Trades: the red team's M5 rule says "≈ 0 → stop paying for np", and the MAL gate goes no-go when capped (§8, §2F).
  - Ladder: the red team stops dealer work at L ≥ M (§8).
  - Flags: they stop at the first 0.
- **The change.**
  1. VC: drop the 40-50 ceiling. Keep firing safe pairs (collector buys, page finishers) all day.
  2. Trades: once M5 reads "capped", still spend idle cash (it has no terminal value) on positive-np team buys from non-rivals,
     and the MAL close.
  3. Ladder: keep doing zero-neg ladder upgrades past M.
- **Size [L; Saturday's references assumed for Sunday].**
  - Trades, N ≈ 100, +30 np past our cap, we're top 3: N → 110.
    - A rival at 0.8 N: 7.2 → 6.55 (−0.65).
    - A rival at N: 9 → 8.18 (−0.82).
    - A rival above 1.1 N: 0.
  - Ladder, M ≈ 0.5, +0.1 past our cap: M → 0.533. Rivals near the reference lose 0.45-0.56.
  - VC: t10 ≈ 21, t06 ≈ 14 (Saturday, M ≤ 15; market-test-audit §3b).
    - v10 at 45: t10's real trades 7.5 → 5.9.
    - v10 at 90: 3.8 (**−2.1 more**). t06 loses ≈ 1.4 more.
    - t18, t12 and t03 have stall-only markets (7.5 / 7.25 / 6.08 at tick 1440), so VC denial doesn't touch them. The trade and
      ladder parts do.
  - Bonus: VC above the reference is insurance. One negative pair later can't drop us below the cap.
- **Game totals at tick 1440** (0.5·Fri + Sat, from `data/leaderboard.jsonl`): t10 56.37 · t18 46.89 · **us 45.73** · t12 45.63
  · t03 44.51 · t06 43.14 · t14 41.51. The trade and ladder parts are where t18, t12 and t03 can be pushed down. VC pushes down
  t10, t06 and t14.
- **Fair play.** Only value creation, with no transfer to anyone, so it is clean.
- **Risks.**
  - [?] The trade and ladder references may be a max or a median instead of a top-3 mean. Then the effect is larger (max) or zero.
  - The effect is zero whenever we're outside the top 3 of that part, but then we're under the cap and the value counts for
    us directly. Either way more positive value is never worse.

### 1.2 Keyed probe of `GET /api/cards/{id}` [?]
- **Mechanic.** SDK:168-170 lists `card(asset_id)` ("one card or pack instance with its provenance chain") in the public block,
  but unkeyed it returns `bad_key` (holdings-audit:181). RULES:19 says every copy carries "a history of every hand it passed
  through".
- **Why it scores.** The feed misses pack pulls (`pack.opened` shows only `best`, rare+), gifts and Workshop outputs by asset id.
  333 of 1,126 settlement numbers never appear publicly, and the matchmaker sent 6 of 20 pairs to buyers that already held the
  card (holdings-audit §2).
  - Sunday makes this worse. The 09:00 grant is **cash only** ([V] `/api/schedule`: `grant_all` 16.7 `{"cash": 150}`, no pack),
    so CHA cards enter only through dealer sales (public) and **packs teams buy (private)**.
  - A holder map finds who pulled CHA cards, who can sell the closer, and which v10 buyers truly lack a card.
- **Cost.**
  - Operator: one keyed GET on an asset we own; check whether the chain names teams.
  - Sweep: ids 1 → ~1,190 (max id in the feed 1186) ≈ 5 min at 4 req/s, **before 09:00** (key idle).
  - Re-sweep only new ids every 30 min, never during duel waves.
- **Not used.** No file in `tools/`, `agents/` or `broker/` calls `/api/cards`.

### 1.3 Writes are accepted while the doors are closed [V]
- **Evidence.**
  - After `day.closed` (feed id 73274, tick 1445), the server accepted our own bid 20252 (id 73278, SAL-11 115 → t04 on v15).
  - It also accepted t09's 10 listings and 8 cancels (ids 73279-73299) and fee notices for v05 and v07.
  - RULES:107: "offers stay open; the clock stops".
- **Uses.**
  1. **Bid 20252 is still live** (no cancel in the feed or the hub feed). The 00:21 GUARDRAIL cancels it "at the first tick",
     which races t04's accept on that same tick (red team §6.7).
     - It can be cancelled now.
     - Or, under §1.1, Lucas may let it fill: +47 np at 115 P, if the CHA + MAL cash (cha-plan: 242-282 + MAL) still fits in 542.
     - Lucas's call either way.
  2. **Stage the 09:00 maker bids now** (fodder LAT-06/07/08 ≤ 12, our spare asks on member venues). The club partners can do the
     same for their v10 pair bids. Staged bids sit first in the book when the bots wake at tick 1446, and they don't use the first
     tick's 12-listing budget. RULES:109 counts listings per tick, and the closed tick 1445 has its own budget [L].
  3. [?] **Test whether an accept made while closed queues for tick 1446.** Do it once, on an ask we'd take anyway. If it works,
     we get the best first-tick ask before any bot.
- **Hygiene [L].** `expires_param` uses the live `tick_seconds`, which is 30 while paused (`/api/clock`). A bid staged now gets
  half its intended wall life at 15 s, so pass `tick_seconds=15` for staged offers.
- **Side fact for Dani's desk list [V].** The venue bond comes back **10 ticks** after closing: `venue.closing` → `refund_at_tick`
  for v03 753 → 763, v22 776 → 786, v23 808 → 818, v04 1313 → 1323.

### 1.4 N-for-1 and cash-topped swaps [L]
- **Mechanic.** An offer can carry cash and up to 50 assets on each side (RULES:144). `swaps.py:199-202` only posts 1 asset for 1
  card, addressed and cash-free.
- **Why now.** Nobody holds CHA at 09:00 (§1.2). The first team-held CHA commons and uncommons come from teams that buy packs or
  dealer cards, and a lone LAV dup worth 3.2 to us rarely matches a CHA card's value to them. A swap of "dup + up to 10 P"
  or "2 dups → 1 card" clears where 1:1 doesn't.
  - Our side: CHA common 16, uncommon 40 (first copy).
  - Each fill is +6 to +30 np at ≤ value − 10, and it saves a dealer thread.
- **Risk.** Same rules as today's swaps (policy.py rivals, never a page card). Keep each trade's gain under the 50 cap (GAME.md:29).

### 1.5 Team threads for private terms [?]
- **Mechanic.** RULES:64-65 and SDK:192-203 allow a thread with another team on a venue, with structured offers inside it; the
  accepting side pays that venue's fee.
- **Evidence.** All 1,637 `thread.opened` and 11,262 `thread.message` events in the public feed are dealer threads. Team threads
  are either private or unused.
  - If they're private: a CHA closer or a club pair can be agreed and accepted in-game without the `offer.listed` leak (GAME.md:56-58:
    addressed offers show in full in the feed), so nobody can see us at 9/10 and hold out.
  - Club pairs can also open their own thread on venue `v10`, which keeps the VC ours.
- **Test.** One thread with a club member, then watch the public feed for 2 ticks.

### 1.6 Re-topic a dealer thread [?]
- **Mechanic.** `say()` takes `topic` (SDK:209-220). Our bots only set topics at `open_thread` (`abuela_bot.py:271`,
  `chato_steady.py:82`).
- **Why it might pay.** If a new topic draws a fresh secret limit (RULES:46 "every conversation has its own secret limit"), it's a
  re-roll without the bots' 10-tick reopen gap or a new conversation against the hourly `persona_quota`.
- **Risk.** Spam or cool-off; Abuela forgives, Ernesto doesn't. One test on Abuela only.

## 2. Already used or planned (checked, with where)

| Mechanic | Where | Note from this pass |
|---|---|---|
| Card-for-card swaps, want-cards bids | `agents/trader/swaps.py`, `book.py`, `run/cha_book.json` | 1:1 only (§1.4) |
| Workshop | GAME.md:113; directive 00:44 fodder; red team §1.5 | 3 uncommons → rare also exists (t01 tick 1361) |
| Flags | GAME.md:116-130; red team §E (test the cap reset) | The Trickster badge does **not** stop the tricks [V]: after their badge t10 got 5 bait-and-switch offers and 3 false-fact lines in 34 Pícaros messages; flag material survives the egg |
| Gifts (kindness) | dealer-lab-ladder §2; `narrator.py`, `chato_steady.py` kindness lines | — |
| Eggs | `intel/eggs.md`; dealer-lab §3 | The Chato pack line ("Plaza Mayor, con caña") is still unclaimed by us. No CHA hidden card in `/api/catalog` (12 cards) [V], so there is no CHA egg card to hunt |
| Page close via a team closer; pack drag | GAME.md:34-39; score-model §3e; cha-plan | — |
| Ladder slots, fodder, walk and reopen, offer-only | score-model §4.5/§4.12; dealer-lab-ladder §3; GAME.md:18 | — |
| Expiry conversion | `book.py:77-79`, `opportunities.py:66` | Staged offers: see §1.3 hygiene |
| Events stream, keyless reads | `tools/reactor.py` (keyless SSE), `broker/common.py`, `opportunities.py` | — |
| News and dealer patches | `tools/news.py` | True items led patches: Chato MAL rares (403 → chato v2 at 463), Abuela uncommons (943 → abuela v2 at 979), Salamanca fever (850 → 939) [V] |
| Market Test | market-test-audit.md (keep the stall) | — |
| Broker announcements | `run/v10_announce2.py` | 1 per 20 ticks (GAME.md:147) |
| VC normaliser on v10 | directive 01:10 (club split) | Extend to trades and ladder (§1.1) |

## 3. Checked and dropped

| Idea | Why not |
|---|---|
| Board venue / second venue for the Market Test | Opening replaces the stall (RULES:72). 0 of 51 board sessions beat the stall (market-test-audit §1a). Every `bench.started` lists one venue per team. The bond is only locked 10 ticks (§1.3), but replacing v10 risks its real-trades record (RULES:81) |
| Don Ernesto L5 | No neg-safe deal from our holdings: he buys epics at 113-129 (our RET-11 is 198), and gold packs and legendaries are far above value (dealer-lab-ladder §6) |
| Master bonus (`master_bonus` 0.1) | Needs the legendary: every *-12 minted 0/3 [V catalog]; Ernesto finals 729+ |
| Flags on duel messages | Duel payloads carry no message ids (`docs/duels/*.json`), and an LLM's number slip isn't the engine's bad faith (−10 [V]) |
| Flags on Abuela/Chato/Pilar text | No engine tricks there (score-model §3c); a wrong flag costs −10 |
| Accepting a dealer offer addressed to another team | Would be a bug exploit: fair-play-dubious |
| Bids beyond our cash, relying on failed settlements | Unknown cash reservation; it fails counterparties on purpose: dubious |
| Reporting a rival to the desk | Feed scan of team-pair trades: no one-sided pattern involving t10/t18/t12/t03; t07 ↔ t15's 0-price trades are swaps |
| Club cash bonuses | Dropped by Lucas at 01:10 ("no cash bonuses (fair play)"). Penalties are a % of the round (RULES:123) |
| t09's silver pack at 130 (open ask) | Our EV of a silver pack ≈ 72 (dealer-lab-ladder §6.2), so ≈ −58 np |
| Abuela packs as a CHA source | sobre_barrio EV to us ≈ 17 vs 19-26 P; her CHA commons at 8-9 are better and fill the same L1 slots |
| LAT page | ≈ 224 P to complete vs ≈ 166 of value incl. the 33 bonus |
| CHA bids posted before the release | Server acceptance of unreleased cards is [?]; it shows our CHA prices all night for a few ticks of queue |
| Pilar egg | Nobody found it; no reply hints at a trigger beyond chulapa lore; eggs never score |

## 4. Feed event types (`data/feed.jsonl`, 27,169 events, ticks 2-1445) [V]

| Type | n | | Type | n | | Type | n |
|---|---|---|---|---|---|---|---|
| thread.message | 11,262 | | gift.given | 48 | | announcement | 14 |
| offer.listed | 8,197 | | thread.closed | 42 | | schedule.fired | 13 |
| offer.cancelled | 3,056 | | taller.crafted | 34 | | news.posted | 11 |
| thread.opened | 1,637 | | venue.fee_announced | 29 | | venue.closed | 8 |
| duel.closed | 1,224 | | egg.found | 27 | | persona.updated | 7 |
| settlement | 819 | | venue.opened | 26 | | level.announced / level.activated / bench.started / egg.given | 6 each |
| venue.announcement | 429 | | venue.fee_changed | 25 | | persona.open_to_all, venue.closing | 4 each |
| pack.opened | 109 | | badge.awarded | 21 | | duels.scheduled, duels.finished | 3 each |
| level.unlocked | 72 | | clock.changed | 15 | | day.closed 2 · day.opened, set.released, round.ended, round.started 1 each | |

- **Settlements.** 632 dealer, 145 El Rastro, 42 on team venues. **One broker `match` all weekend** (t12's v02, tick 234).
- **Threads.** All are dealer threads (§1.5).

## 5. Read live at 01:05 (keyless) [V]

- **Schedule** (`/api/schedule`, `now_hours` 13.367, paused, round 2):
  - hard Market Test 14.65, bench 15.0
  - CHA release + round 3 + Sunday open at 16.65 (wall 09:00)
  - allowance 16.7 (cash 150 only)
  - benches 17.0 / 19.0 / 21.0
  - Duels III 18.65 (2 rounds, 12 ticks, decay 0.10, max 4)
  - all five stalls close + Grand Final 21.65
  - scores freeze 22.65 (15:00)
- **Levels:** nothing new announced for Sunday.
- **Venues:** `/api/venues` shows trades, pairs, traders and volume per venue, but **no `value_created`**. Rivals' VC is not public;
  the reference stays an estimate.
- **Catalog:** CHA-01..12, all minted 0. CHA-09/10 rares and CHA-11 epic have print runs of 30 / 30 / 9.
