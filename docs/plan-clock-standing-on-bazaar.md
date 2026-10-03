# Plan: running Clock-Standing in The Bazaar

> **History.** Written on Friday evening, before the practice duels; the code and [duelist-runbook.md](duelist-runbook.md) have moved on since (decay is per round, not per tick; the delivery day is handled as described there). Background, not instructions.

As of Friday 2 October 2026, evening, after the rules were revealed ([bazaar-kit/RULES.md](../bazaar-kit/RULES.md)).

Background: [how-the-leading-model-works.md](how-the-leading-model-works.md) and [what-we-tried-so-far.md](what-we-tried-so-far.md). The code is in `~/Workspaces/personal/regateo`: the agent is `agents/ranged/v4` with config `clock-standing`, written against `agent-sdk`, and it calls models through `engine/src/regateo/llm`.

## 1. The short version

- **The Bazaar is much bigger than the game we prepared for.** We built a 1v1 price haggler. The Bazaar is a card-trading economy with five parts: dealers, team-to-team trades, our own market, duels and the judges.
- **The duels are almost exactly our game.** Each duel has one buyer and one seller, each with a secret limit, and no deal scores zero. Clock-Standing goes there first, with four adaptations: offers arrive as structured fields, the deal loses value with every round, later sessions add a second issue (delivery day), and replies must fit in a tick of 15 to 60 seconds.
- **The dealers are a different game.** A dealer concedes only after we move, so Clock-Standing's core rule ("hold until they move") would deadlock it. Dealers follow fixed rules, the same for every team, so a scripted prober plus an LLM for the wording beats our adaptive agent there.
- **Half the score isn't negotiation at all.** Market-making is 30% and the judges are 40%. Our regateo methodology is a strong story for the judges. A simple market broker is cheap points.

## 2. Where the points are and what we already have

| Score share | Part | Fit with regateo | Action |
|---|---|---|---|
| Negotiating 30 | **Duels**: share of each deal's value captured; a deal outside the limit loses points; the value shrinks every round | **Direct.** This is our game with a structured protocol | Adapt Clock-Standing (§4) |
| | **Dealer ladder**: share of the dealer's price range captured, best 3 negotiated deals per level, higher levels weigh more | Partial. Our guards and price checks carry over; our strategy doesn't | Separate dealer bot (§5) |
| | **Team trades**: value gained at our private values | Weak. Multi-card barter, not a single price | Later, if time allows |
| Market-making 30 | Market Test (a broker on synthetic books) and value created on our venue | None | Separate small track (§6) |
| Judges 40 | Ideas and craft | **Strong.** Benches, paired tests, red team, sandboxed builders, learnings | Demo story (§7) |

## 3. What changes from what we assumed

Regateo's open questions ([regateo docs/01 §5](../../regateo/docs/01-problem-and-constraints.md)), answered by the rules:

| We assumed or didn't know | The Bazaar | Effect on Clock-Standing |
|---|---|---|
| Free text, read by a referee | **Structured.** `price` (and `days`) travel next to the text; an accept is an API call on the rival's standing offer. "Words persuade, structure binds." | Read the rival's offer from the structured fields, not from the text. The "quote and accept" attack (−0.19 for us) no longer works: an accept can only take a real standing offer. The text-reading guards (`their_floor`, `closing_price`, the agreement-words veto) matter much less. |
| A message limit, known or hidden; no cost to talking | **The deal's value shrinks with every round**, and the duel has a `deadline` | The clock prompt's "with a known limit, holding costs nothing until the last two messages" is now wrong. Each round has a price, so concessions should come sooner and the near-deal closing rule should trigger earlier. |
| One issue: price | Later sessions: **price and delivery day (0–10)**, with a private weight per day (`your_days_weight`); a priced message without `days` is refused | New. The strategist must also choose a day, and the facts must say what each day is worth to us. The gain comes from logrolling: trade days the rival cares about for price. |
| Market range given (`market_low`, `market_high`) | Only our own limit (`your_limit`) is known for sure | Our prompts anchor the opening on the market range. Use whatever the duel gives; if nothing, derive it from the limit and the rival's first offer. Check in the practice round. |
| Per-message time limit unknown | One message per conversation per tick; ticks are 60 s Friday, 30 s Saturday, 15 s Sunday | Two model calls per turn (strategist, then negotiator, plus retries) must fit in a tick. Opus at high effort won't on Sunday. |
| Opponents on Qwen in our bench | Other teams' agents, most likely Claude | Our Qwen results may not carry over (regateo 07 §7.1). We never ran the Claude transfer check. |
| Prompt injection might be banned | Allowed; it changes words, never prices | Our agent already treats their text as evidence, not instructions. Structured offers make injection even weaker. |
| | A first practice session that doesn't score | Our live test and our chance to record the real payloads |

## 4. Duels: adapting Clock-Standing

### 4.1 Architecture

The agent lives outside the organisers' kit, and the model provider is kept apart from the agent:

```
bazaar-kit/
  bazaar_sdk.py          the organisers' SDK (unchanged; imported from here)
agents/
  duelist/               our duel agent (no provider SDK in it)
    model.py             what the agent sees: view, turns, offers
    adapter.py           duel JSON -> view and turns, read defensively
    agent.py             strategist + negotiator + guards (Clock-Standing)
    prompts/             strategist.md, negotiator.md
    runner.py            async loop: poll, decide, send; JSONL log
    __main__.py          probe | smoke | run; picks the provider
engine/
  __init__.py            Model (the interface agents use), Reply, LLMError
  claude.py              Claude via the Anthropic SDK (structured output)
tests/test_duelist.py    offline tests
```

- **Decided on 2 October: no imports from regateo.** What we need is copied into `agents/duelist/` (the agent, its prompts, the guards, the price reader) and `engine/` (the Anthropic client), and the §4.2 changes are built in rather than behind switches. We don't run simulations for now. How to run it: [duelist-runbook.md](duelist-runbook.md).
- **The SDK is synchronous** (urllib). Call it through `asyncio.to_thread` so that many duels can think in parallel. Model calls are the slow part; HTTP is not.
- **The request budget.** The limit is 5 requests per second per key, and the team shares one key. Read all live duels with one `GET /api/duels` per tick and send at most one message per duel. Don't poll a duel's thread on its own.

### 4.2 Changes to the agent (`ranged/v5`)

Each change is a param, off by default, so v5 with everything off is v4.

| # | Param | Change | Why |
|---|---|---|---|
| 1 | `structured_offers` | `their_offers`, `their_floor` and `closing_price` read the structured price from the opponent's moves. Text prices are ignored, except to note a mismatch. | Structure binds. The defensive text-reading made good offers look worse (doc "Where it still falls short"). |
| 2 | `decay` | The ledger says "Each further round shrinks the value of any deal by about X%" (with X once we know it). The v3 strategist prompt drops "holding costs nothing" and weighs every round's cost against the gain from holding. | No-deal is zero and delay now costs too. Our near-miss closing rule should fire earlier. |
| 3 | `days` | `BandPlan` gets `days: int` (0–10) and `days_reason`; the ledger lists our weight for each day and the days the rival has offered; the negotiator's `Decision` gets `days`; code checks 0 ≤ days ≤ 10 and that every priced move carries it. | Required by later sessions; refused otherwise (`missing_days`). |
| 4 | `deadline` | The deadline goes into `PrivateView.max_rounds` (or `time_limit_s`), so the clock facts say when the duel ends. | The clock was the change that won round 2. |
| 5 | (always) | The limit guard and `_final` work on the structured price; a deal outside the limit is still never sent. | "A deal outside it loses you points": our hard gate. |

Not changed: the strategist/negotiator split, the negotiator never seeing our limit, the band and the standing-offer veto.

What we don't know about days yet: how a day's weight turns into value and whether the limit applies to price only or to price plus days. Until the practice round tells us, the strategist gets the weights as given and code checks only the price against the limit.

### 4.3 Model and latency

The times below are guesses, not measurements.

| Option | Per turn (2 calls) | Fits a 15 s tick? |
|---|---|---|
| Opus 5.5, effort high (the only Claude profile in regateo today) | about 20–60 s | No |
| Opus 5.5, effort low | about 6–15 s | Barely |
| **Sonnet 5.5, thinking off, both stages** | about 3–6 s | **Yes** |
| Sonnet strategist, Haiku 4.5 negotiator (`strategist_model`) | about 2–4 s | Yes |

Start with **Sonnet 5.5 on both stages**. Add profiles `claude-sonnet-5-5.yaml` and `claude-haiku-4-5.yaml` to `regateo/engine/configs/models/`, and fix `claude-opus-5.yaml` to `claude-opus-5-5`. Measure the real latency in the practice session. If a turn would miss its tick, send `safe_move` (restate our last offer) rather than nothing, and log it.

### 4.4 Testing before it counts

1. **Unit tests on recorded payloads.** Turn real `GET /api/duels` responses into fixtures and test the adapter with `agent_sdk.testing.FakeLLM`. No network.
2. **A structured bench in regateo.** `gym` with `protocol: structured`, a per-round decay on the score, and the two-issue scenarios once we know the formula. Run `ranged/v5/bazaar` against `ranged/v4/clock-standing` and the baseline on Qwen overnight. The question: does v5 lose nothing where v4 was good, and gain under decay?
3. **The Claude pilot** we never ran (regateo 07 §3 step 4): 20 matches with our agent on Sonnet, to measure tokens, latency and whether the ranking holds.
4. **The practice session**, live, with full logging.

## 5. Dealers: a separate bot

Clock-Standing doesn't fit the dealers:

- A dealer **moves only when we move**, and repeating a price earns nothing. Clock-Standing holds when the other side doesn't move, so against a dealer both sides would wait.
- The score is **our share of the dealer's own price range**, and only a negotiated deal counts (not one at the opening price). Our best 3 deals per level count; a missing one counts as zero.
- Dealers follow **fixed rules, the same for every team**, with a secret limit per conversation. A fixed opponent is exactly where code that learns beats an adaptive LLM. Regateo's "strategy lives in the model" rule was about adaptive rivals and doesn't apply here.

The plan:

1. **A scripted prober**, starting from `starter_agent.py`: open low, raise by small, new amounts each tick, never repeat a price, take a `"final": true` offer if it is within our value, and close the thread when the dealer walks. Log every price path per dealer and topic.
2. **An LLM only for the words**, with a per-dealer style note (Abuela likes kindness; some treat the same words twice as spam). Haiku is enough. No prompt injection against dealers: it never changes prices and some dealers stop talking.
3. **Learn each dealer's curve** from the logs (opening price, step sizes, when `final` comes) and set our steps to get as close as we can to its limit before it walks.
4. **Three good deals per level, early**, since unlocking the next dealer needs negotiated deals with the one before it, and the head start is worth having.
5. **Flag bad faith**: when a dealer's words name a different price from its structured offer, `POST /api/flags`. A correct flag scores, a wrong one costs, so flag only clear mismatches.

Budget: we start with 400 P, and packs and cards cost money. Respect `persona_quota` and the hourly allotment; don't buy just to buy.

## 6. Market-making: a small separate track

Not our agent, but 30% of the score:

- At level 2, **open a `board` venue** (250 P refundable bond + 20 P) and run a broker. The free auto stall earns half the bench points by itself, so a broker only pays if it beats quote-crossing.
- `starter_broker.py` notes that bench traders shade their quotes away from hidden limits, and that most relax as their patience runs out. A broker that estimates each trader's limit and urgency from how its quote moves, then matches earlier, can beat the stall. This is a small statistics problem, and the kind of thing our gym is good at measuring offline against recorded `bench_offers`.
- The Market Test counts our best venue open during each session, so don't close it after a good session.

## 7. For the judges (40%)

Our method is the story: a negotiation gym with paired matches, holdout opponents, a red team, sandboxed AI builders, and a learnings record, which picked Clock-Standing out of five architectures. Show the dashboard, one duel transcript with the strategist's band next to it, and the before/after table for the Bazaar adaptations. Collect the material as we go: the logs from §4.1 are the raw input.

## 8. Timeline

| When | Duels | Dealers and market |
|---|---|---|
| **Fri, now to 23:00** | Read `GET /api/duels`, `/api/schedule` and `/api/levels`; save raw payloads. Write `duel_adapter.py` and `runner.py` around v4 as it is (structured protocol only). Add the Sonnet and Haiku profiles. If a practice duel runs tonight, play it live. | Run the prober against Abuela with full logging; get the first negotiated deals. |
| **Night 1** | `ranged/v5` with §4.2 changes 1, 2, 4. Structured + decay bench on Qwen: v5 against v4 and the baseline. Claude pilot (20 matches). | Fit Abuela's curve from the logs. |
| **Sat 09:00–12:00** | Read the night's results and transcripts. Switch the runner to v5 if it holds. Days support (change 3) once the practice round has shown the payload. | Level 2: open the venue, start the broker. Three good deals per unlocked dealer. |
| **Sat 12:00–23:00** | Run in the scoring duel sessions; read every lost or outside-limit duel. One fix at a time, each one checked on the bench. | Improve the broker on recorded books. |
| **Night 2** | Tune v5 on the two-issue bench; add our own v5 as an opponent. | |
| **Sun 09:00–12:00** | Freeze the duel agent by 12:00. Check latency at 15 s ticks. | |
| **Sun 12:00–15:00** | Run; prepare the demo. | |

## 9. Risks

| Risk | Mitigation |
|---|---|
| A turn misses its tick at 15 s | Sonnet or Haiku; a timeout around `respond` that sends `safe_move` |
| The decay rate or the days formula is unknown | Measure them in the practice session before tuning against them; until then, state only what the API gives us |
| Qwen gains don't carry over to Claude | The pilot (§4.4 step 3) before trusting any night result |
| One key, 5 requests a second, many duels at once | One `duels()` read per tick, one write per duel, the SDK's backoff on `rate_limited` |
| Too many conversations | The limit is 6 open conversations per team; check in the practice session whether duels count towards it, and keep the dealer bot to one thread when they do |
| A bug sends a deal past our limit | The `_final` guard on the structured price, and a unit test that tries every way past it |
| The home PC is unreachable | Duels and dealers run on the Claude API from a laptop; only the night bench needs the GPU |

## 10. Open questions for the practice session

1. The exact `GET /api/duels` payload: limit, rival offer, deadline (in rounds or ticks?), whose turn it is, and whether a market range or item is given.
2. How fast the deal's value shrinks per round, and whether a "round" is a message or an exchange.
3. How `your_days_weight` enters the value, and whether the limit applies to price alone.
4. Whether duels count towards the 6-conversation limit.
5. How long a session lasts and how many duels run in it at once (every team against every other, twice).
