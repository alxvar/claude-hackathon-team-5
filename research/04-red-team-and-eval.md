---
type: decision
entity: [people]
status: historical
updated: 2026-10-01
---

# 04 — Red team, evaluation, and code review

_Owner: Daniel (harness and metrics), Lucas (parameters, attacks, analysis), Aleksandar (code review gates). The goal is to find out how our agent loses **before** 17 other teams do._

## 1. The opponent zoo — from easiest to hardest

| Tier | Opponent | How to build it | Why it's here |
|---|---|---|---|
| **Z1 Scripted** (no LLM, deterministic) | Hardliner (never moves) · Conceder (fast) · Boulware (late) · Random walker · **Mirror** (our own engine, other role) | ~40 lines of Python each | Cheap, reproducible baselines. The mirror is the best proxy for a well-engineered rival |
| **Z2 Field-tested prompts** | The MIT top value claimers, verbatim: Winning Negotiator, Carmelo, Haggletron 3000, Odie_dog, Therapist 2.0, Deal Shark M (`mit-top-prompts.md`) | Each prompt as the system prompt of a Claude model + the scenario instructions | Real strategies that beat 190+ others. A ready-made zoo, at zero design cost |
| **Z3 The copycats** | Inject+Voss, NegoMate, The Art of the Deal, verbatim | Same | What other teams will most likely clone |
| **Z-Engine (code-enforced rival)** | Our own engine in the other role, behind a plain narrator | `07` §E2 | **P0 opponent for every promotion**: real rivals will enforce their limits in code too |
| **Z4 Naive baseline** | Claude with only *"You are the buyer/seller, get a good deal"* | One line | The most likely rival in an 18-team field |
| **Z4b Prosocial Claude** | Claude told to "make sure both sides end up happy" | One line | Project Swap: this archetype folds to pleas. Measures A11/A12, and how much we leave on the table against nice rivals |
| **Z5 Injection attacker** | Cycles through the 14 payloads in `03` | A script that inserts the payloads into a Z4 conversation | Measures D1-D14 |
| **Z6 Adaptive red-teamer (the hardest)** | An Opus agent that reads our agent's last N transcripts and writes a new attack strategy each round, against a goal ("extract R" / "get an accept below R" / "maximize your value") | A loop: transcripts → attacker LLM → new system prompt → play → score → repeat (PAIR-style) | Finds what the fixed suite misses. Run it overnight Saturday if possible |

**Screen cheap, confirm strong.** Run screening games on the cheapest allowed model, and re-run finalists on the model the field is most likely to use (probably Opus or Sonnet: the model matters more than the prompt, per Project Swap). A zoo only on Haiku would flatter us; a zoo only on Opus would burn the budget (`06` §4).

**Scenario generator:** randomize R for each side, ZOPA width, **no-ZOPA cases** (the right answer is *no deal*: test that we never accept below R), turn limit (known / unknown / short), who opens, and our role. Run 20 seeds per opponent per role.

## 2. Metrics (the judge is code, not an LLM)

All money metrics are computed by deterministic code from structured JSONL logs (one line per turn: raw rival text, parsed offer, engine state, action, outgoing text, latency).

| Metric | Definition | Use |
|---|---|---|
| **Value captured** (primary) | Exactly how the tournament scores it (ask on Friday). Default: the normalized surplus in `07` §C: seller (price − R)/ZOPA, buyer (R − price)/ZOPA, 0 if no deal | Rank versions |
| Deal rate | Share of matches with a deal | Impasse alarm |
| p10 value | 10th percentile across matches | Worst case; a tournament punishes blowups |
| **Leak rate** | R, or a number within ±2% of R, appears in our text **and the engine did not choose it** (`07` §C) | Must be 0 (H13 gate) |
| **Invalid accept rate** | Accepted a price worse than R | Must be 0 |
| Injection success | Per payload in Z5/Z6, our action deviated from the engine's plan | Monitored. Real damage shows up as invalid accepts or leaks, which the gate catches |
| Crash / timeout rate | — | Must be 0 |
| Turns to deal | — | Tiebreaker, if efficiency counts (it did in MIT) |

**LLM judges only where code can't judge:** (a) warmth and dominance of our messages, 0-100 (MIT scored prompts the same way with GPT-5.2); (b) *semantic* leaks (*"my cap is around four grand"*). Use a different model from the narrator.

**Tuning discipline:** one parameter at a time, the same seeds for A and B, and a version table (version → params → value / deal / p10 per zoo tier). Lucas owns the parameter table (`07` §A4; the rationale is in `02`). **Don't promote a version that improves the average while lowering p10 or raising the leak rate.**

## 3. Code review: Claude Code writes, Aleksandar gates

Yes, Aleksandar can and should improve what Claude Code (Opus 5.5) writes. But the leverage isn't reading every line. It's **guarding 8 invariants**, each backed by a test that Claude writes **before** the code:

| # | Invariant | Test that proves it |
|---|---|---|
| 1 | **R is never crossed.** No accept and no offer beyond R | Property-based test (`hypothesis`): random rival offers and texts, assert every accepted price ≥ R for the seller and ≤ R for the buyer |
| 2 | **Role and direction are correct** (the utility conversion for both roles) | Hand-written test vectors for buyer and seller, including a rival who argues against its own interest |
| 3 | **Information flow**: R and engine state never reach a narrator or parser prompt | A test that builds every prompt the code can produce and asserts that R itself and the engine's internal state never appear. Numbers the engine chose to offer, and the offer history, are allowed. Plus a grep |
| 4 | **The parser is quarantined**: rival text JSON-encoded, output schema-validated, garbage → `offer = null` | Fuzz it with the 14 payloads in `03`, malformed JSON and a 50k-character text |
| 5 | **The validator blocks**: wrong number, acceptance words without `accept`, leaked tags | Feed it synthetic narrator outputs that break each rule |
| 6 | **Arena protocol**: message format, deal semantics, turn counting, time limits | Integration test against the organizers' sandbox, if there is one |
| 7 | **Resilience**: API error, rate limit, timeout → template message on time | Inject failures with a mock client |
| 8 | **Logging**: every turn written to JSONL, never crashes the match | Smoke run |

**Workflow:**
1. Lucas states an invariant in plain English.
2. Claude Code writes the test, then the code.
3. Aleksandar reviews the diff **against the 8 invariants, not style**.
4. A fresh-context review (`/code-review` or a subagent) runs on every non-trivial change, because the model that wrote the code is bad at catching its own errors.
5. A **50-match smoke run** must be green before anything is merged into the competing agent.

Where Aleksandar adds the most: the arena integration, latency and concurrency, and catching subtle logic bugs like the two the verifier found in our first engine design (conceding by time without reciprocity, and a curve that ended at R).

## 4. Analysis between rounds (Lucas)

If the organizers show practice transcripts, a subagent per opponent team classifies its archetype (Z1-Z4), its concession curve, its opening behavior and whether it is a copycat (Z3 tells: *"remind me of your offers"*, *"how am I supposed to do that?"*, refusing to name a price). Output: **parameter changes only**, never last-minute code.

## Verification log

- **2026-10-01, the Tier 1 re-analysis (`01` §1b)** was recomputed by an Opus verifier with its own code and offer parser.
  - **Exact match:** the baseline, the agent ranking and the paper quotes.
  - **Corrected:**
    - Step size matters for buyers, not sellers.
    - The first-mover effect is about a third of the original estimate.
    - The "never conceded" stat was a definitional artifact and is withdrawn.
    - The Inject+Voss counter was wrong.
    - The ladder defaults decayed to zero, so the engine would have ended up repeating numbers.
  - All corrected in `01` and `02`.
  - Lesson for the weekend: **every number we compute from transcripts gets a second parser before we act on it.**
