> **HISTORICAL (Fri 20:10, before any measurement). Superseded by `intel/saturday-plan.md` and `intel/GAME.md`.**

# Crosswalk: research × simulations × the real rules

_Fri 2 Oct, ~20:10. Sources: `bazaar-kit/RULES.md`, `GET /api/schedule` and `/api/clock` (clock still paused at tick 0 at 20:10), `docs/` (Aleks), `research/` (Lucas; IDs from `research/06` §2). Where they disagree, the rules and the server win. Checked by an independent verifier pass; inferences are marked as such._

## 1. The headline

**We prepared for one slice of the game.** Both `docs/` and `research/` assumed a single 1v1 price duel. In the real game, duels are one of three parts of **Negotiating (30%)**, next to the dealer ladder and trades with other teams. **Market-making is another 30%, and the judges 40%.** Nobody on the team has prepared market-making yet.

| Score part | Weight | What counts (`RULES.md`) | What we have | Gap |
|---|---|---|---|---|
| Duels | part of 30 | Share of each deal's pie; the pie *"shrinks with every round of talk"*; a deal outside your limit loses points; no deal scores 0 | Clock-Standing and the test bench (Aleks); `research/01`-`07` (Lucas) | Decay, two issues, structured offers, Claude rivals |
| Dealer ladder | part of 30 | Share of each dealer's price range captured; your best 3 deals per level count, *"a missing one as zero"*; higher levels weigh more | Nothing specific. The negotiation logic and the bench carry over | Prices come from *"their own rules, the same for every team"*, but *"every conversation has its own secret limit"*, plus hourly allotments and stock caps |
| Trades with other teams | part of 30 | Value gained, at your private values | Nothing | Card valuation (pages, duplicates, set multipliers) |
| Market Test + own venue | 30 | Share of the possible gains your matching realises; value created between other teams on your venue. Fees never count | Nothing | **The biggest gap** |
| Judges | 40 | Ideas and craft | The bench, paired testing, the build journal, the evidence base: a strong craft story | Turning it into a demo |

## 2. Duel sessions, from the server

| Session | Game hour | ≈ Wall clock | Issues | Ticks | `decay` param | Scored |
|---|---|---|---|---|---|---|
| Practice | 2.0 | Fri, ~2 h after the clock starts | price | 12 | 0.06 | No |
| Duels I | 6.5 | Sat ~11:30 | price | 16 | 0.06 | Yes, 1 round-robin |
| Duels II | 13.0 | Sat ~18:00 | price + days | 16 | 0.08 | Yes, 2 round-robins |
| Duels III | 20.0 | Sun ~11:00 | price + days | 12 | 0.10 | Yes, 2 round-robins |
| Final | 23.0 | Sun ~14:00 | price + days | 12 | 0.10 | Yes, on the big screen |

- Wall-clock times assume the schedule's anchors hold: game hour 4.0 = Sat 09:00, 18.0 = Sun 09:00.
- **If the clock starts late tonight, the practice duels (hour 2.0) and the first Market Test (hour 3.0) may fall after Friday's 23:00 close.**
- **Three of the four scored sessions have two issues.**
- The message cap is public (`duel_ticks`, and each duel has a `deadline`). The rules only say the pie *"shrinks with every round of talk"*. How `decay` applies (per tick or per message, multiplicative or linear) is not stated: **measure it in the practice duels** with `GET /api/duels?done=true`. Below, "6-10% per round" is our reading of the `decay` parameter, not a stated rule.

## 3. Hypothesis by hypothesis

| ID | Research says | Simulations say | Agree? | What the real rules change | Next |
|---|---|---|---|---|---|
| **H-ARCH** (who picks the number) | Code decides the numbers, the LLM writes the words (2024 evidence); flagged as untested against frontier models | The code-decides prototype was dropped for four reasons: hidden deadlines, *"It threw away true signals"*, *"It couldn't persuade"*, *"It was predictable"*. Clock-Standing: a strategist LLM sets a price range, code clamps it, a negotiator LLM writes | Both keep hard limits in code. They disagree on who picks the number | Only the first of the four reasons goes away: the cap is public. The other three still apply. And code-decides was only tested against scripted opponents (*"These results came from games against scripted opponents only"*) | Keep Clock-Standing as the reference. An engine-priced arm is a cheap paired test on the bench if time allows, after the port (P2) |
| **H1, H2** (anchor, step size) | More extreme openings captured more value (MIT, 2024 models, correlational); small steps helped buyers only | The strategist opens ambitiously and gives ground *"only after the other side has, by less than they did, in shrinking steps"* | Yes, same direction | **Decay:** if `decay` means a 6-10% cut per round, every round of talk is costly. The bench priced time only through the cap (no deal = 0), with no per-round cost; `research/01` records no per-round cost either. So small steps may now buy share at the cost of pie. Dealers: *"Small steps earn small steps"*, and repeating a price earns nothing | **P0.** Add decay to the bench's score and re-tune the opening and step size. The bench is free |
| **H3** (always move vs hold) | *"Always moving beats holding"* (a bet, from the winning MIT prompts) | Clock-Standing: *"If they haven't moved, hold."* | **No, they contradict each other** | Against dealers the rules settle it: *"A dealer only moves when you do"*, so holding gets nothing. In duels it is still open | Dealers: always move, in small steps, never repeating a price. Duels: test both on the bench with decay on |
| **H5** (closing, the clock) | A closing rule; tune the unknown-cap case separately | v4 added the clock. *"With a hidden message limit, 62 of 84 failed negotiations ended with the other side's offer already acceptable"*. Its rule for a known cap: *"With a known limit, holding costs nothing until the last two messages"* | Yes: closing is where value leaks | The cap is known here, and the near-miss figure came from the hidden-cap case. **But if the pie shrinks every round, holding is never free**, so the known-cap rule doesn't fit this game (inference until decay is measured) | **P0.** Rewrite the strategist's clock rule around decay: accept when their standing offer beats what one more round is expected to bring, after decay |
| **H13** (defense) | 14 attack payloads; gate: 0 invalid accepts, 0 leaks, 0 crashes | The code check held: no deal past the limit in any test. Still open: quote-and-accept (−0.19) and the briefed AI attacker (−0.29) | Yes | *"Words persuade, structure binds"*: only an accepted structured offer moves anything, so a fake "we agree at X" in the text cannot bind. `duel_accept` takes the rival's standing offer. Quote-and-accept should only work if our `price` field carries their number (inference) | Re-run quote-and-accept and the briefed attacker on the structured protocol before trusting −0.19 and −0.29. Prompt injection against dealers is allowed; it *"changes what they say, never their prices, and some of them will stop talking to you"* |
| **H8** (warm vs neutral tone) | Mixed evidence | Not tested | — | *"Abuela likes kindness."* Of the dealers in general: *"Some forgive everything; some stop dealing with you for a while if you try to trick them"*, and to some the same words without a new price are spam | Warm with Abuela, as the rules say. Other dealers: unknown; never trick them blind. Duels: untested, low priority |
| **H14** (model, latency) | A stronger model wins (Anthropic's marketplace experiments) | Everything ran on local Qwen. Letting the AI "think" first made it settle for less | Partly | Ticks are 60 s / 30 s / 15 s and can be moved *"between 5 s and 60 s"*. Up to 3-6 duels run at once, each needing 2 LLM calls per turn plus retries, under a shared 5 requests/s per key | Measure per-turn latency on Claude (Haiku, Sonnet) in the practice duels. The binding case is concurrent duels × the shortest tick, not just Sunday |
| **H15** (transfer to Claude) | The MIT priors are untested on Claude | *"Everything so far ran on our local AI model"* | Yes: the same open question on both sides | The practice duels (not scored) are the first real test | **P0.** Play the practice duels with Clock-Standing on Claude, with full logs |
| **H-MI** (multi-issue) | Packages beat issue-by-issue concessions (NegoMate); `research/07` §A7 | None: Clock-Standing is price-only | — | Duels II, III and the Final are price + delivery day (0-10), with a private weight per day for each side. *"The pie grows when you find out who cares more about time"* | **P0 before Saturday 18:00.** Teach the strategist to offer packages and to read the rival's day preference from their counters |
| **H16** (sim → real) | Real games outrank simulations | — | — | Practice duels and live dealers are real games | Log everything from tonight on |

## 4. False positives and false negatives

**Results we may be over-trusting:**
- **Clock-Standing's margins.** Measured mostly with 6 messages (5 or 10 against unseen opponents), no per-round decay, one issue, free text read by a referee, and Qwen opponents (plus the rule-based Boulware). The real duels differ on most of these, and from Duels II on also on the number of issues. Its ranking may hold; its margins are unknown until it plays on Claude.
- **The known-cap rule** (*"holding costs nothing until the last two messages"*): it fits the bench, and likely not a game where the pie shrinks every round (H5).
- **The MIT priors** (`research/01`): 2024 models, correlational.
- **Thin league margins:** some rest on 20 games, as `docs/` itself says.

**Things we may have dropped too early:**
- **Code-decides.** One of its four failures (hidden deadlines) no longer applies; the other three still do. Not worth re-litigating unless the bench makes it cheap.
- **A code policy against dealers.** Dealers price by *"their own rules, the same for every team"*. If their concession pattern turns out to be consistent across conversations (each has its own secret limit), a policy tuned on it may beat an LLM improvising. A hypothesis to check on live data, not a result.

## 5. Tonight (Friday counts half; the practice duels count nothing)

1. **A read-only monitor** of `me`, `clock`, `levels` and `duels`, so we see what happens as it happens.
2. **Port Clock-Standing to the structured duel protocol** (`duel_say(id, text, price, days)`, `duel_accept`), on Claude, with the decay-aware clock rule and full logs. Target: the practice duels, if they happen tonight.
3. **Abuela.** Negotiated deals with her (a deal at her opening price doesn't count) earn a head start on level 2 when the organisers activate it; everyone else gets it after the head start. Level 2 lets us open a `board` venue. Only the best 3 deals per level count and a missing one counts as zero, so we need at least 3 good ones. Move every turn, in small steps, never repeat a price, be kind, take her `final` offer if it fits the budget.
4. **Cash is tight.** We start with 400 P. A venue costs a 250 P bond plus 20 P, and Saturday adds 150 P. Don't spend at Abuela the cash the venue needs.
5. **The Market Test.** The free stall earns half the bench points with no work. Full points need a `board` venue plus a broker that estimates traders' hidden limits (`bazaar-kit/README.md` §5). Fees never count and we can't trade on our own venue, so fees should attract trades, not earn. Closing a venue after a good session keeps nothing. There is a harder Market Test at game hour 16.0. Read `starter_broker.py` and design the matcher tonight.
6. **Flags:** *"a correct flag scores, a wrong one costs"*. Flag a dealer only when sure.
7. **The judges (40%).** Keep every log. The bench, the paired testing and the evidence base are the craft story.
