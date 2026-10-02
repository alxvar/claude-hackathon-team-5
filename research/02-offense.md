---
type: decision
entity: [people]
status: active
updated: 2026-10-01
---

# 02 — Offense: how our agent claims value

_Every rule is tagged with its evidence: **[DATA]** = MIT open data or a verified benchmark (`01`) · **[MECH]** = plausible mechanism, adjacent evidence · **[BET]** = our inference, validate in the zoo before trusting it. Every number marked "default" is a starting parameter that Lucas tunes with zoo data (`04`)._

## The thesis in one line

**The LLM talks, the engine decides.** Warm, question-asking language keeps rivals at the table (MIT: warmth wins by avoiding impasses). A deterministic engine makes every offer and every accept, using the recipe of the MIT single-price winners: extreme anchor, baby-step concessions, always keep moving, always close a positive deal. **This is our starting architecture, not a settled one.** The first Layer B experiment (`06` H-ARCH) pits it against a frontier LLM deciding on its own inside code bounds.

---

## 0. The lever before any strategy: the model

**If the rules let us choose, use the strongest model available** (today: Opus 5.5 or Fable 5.1) for everything the LLM touches. Anthropic ran two marketplace experiments with Claude agents, and in both **the model mattered more than the instructions** (Project Swap). In Project Deal, Opus beat Haiku on both sides of the same deals, while "be aggressive" instructions changed nothing. **[DATA]** (`01` Tier 1b)

- **If the format is code:** the engine fixes the numbers, so the model matters for parsing, narration quality and injection resistance. Use the strongest model for the narrator and Haiku for the parser, as a latency trade-off.
- **If it's prompt-only:** the model is most of the game. Ask on Friday whether we can choose it.

---

## 1. The engine (what Aleksandar builds first)

### 1.1 Work in utility, never in price
`u = 0` is our reservation (walk-away) value and `u = 1` is our anchor. Buyer: `u = (R − price) / (R − anchor)`. Seller: the mirror. One accept rule then works for both roles, with no sign bugs. **[BET, fixes a verified bug]**

### 1.2 Opening
| Rule | Default | Evidence |
|---|---|---|
| **Ask first, then anchor.** If the rival names a number, accept it only if it beats our anchor; otherwise counter at our anchor. If it hasn't named a number by our 2nd message, anchor ourselves | `OPEN_POLICY = ask_first`; A/B against `anchor_first` in Layer B (H7) | **[BET]**. The data point both ways: with fixed effects, moving first cost −$1.65 to −2.73 (p < 0.001), but sellers who waited closed fewer deals (65% vs 70%), and Winning Negotiator #1's buyer *"Always state your price first"*. The tie goes to the direction of the estimate. The anchoring lever (+$0.40-0.58 per $1, **[DATA]**) is kept through the extreme counter |
| *(Optional variant, off by default)* **Mirror:** if they gave a number X first, counter at max(anchor, 2X) as seller / min(anchor, X/2) as buyer | `MIRROR` | **[BET]** (Odie_dog #4's rule). It only ever makes the opening tougher, so Layer A decides whether to turn it on |
| **Anchor level:** buyer ≈ 40% of the reference price; seller ≈ 170% of the reference price | `ANCHOR_BUY = 0.40`, `ANCHOR_SELL = 1.70` | **[DATA]** that more extreme openings capture more (`01` §1b) · **[BET]** for the exact levels, taken from Winning Negotiator #1's rule: the seller opens *"190%-250% higher than your minimum"*; the buyer opens at $10-20 on a $120 item |
| **Justify the anchor** with one concrete, believable story (market, condition, budget, alternatives) | — | **[BET]** (prompt pattern) + **[MECH]** Tier 3: logic and authority persuade best. Winning Negotiator: *"I originally bought it for $200, but I'm looking to sell it for around $300"* |
| **Aim past the rival's walk-away.** A rival that enforces its limit only in its prompt can be dragged beyond it | — | **[DATA]** In 18% of the MIT top-10 agents' deals, the rival ended below its own BATNA (7% pool average). In Project Deal the gap came from the asking price, not from "aggressive" tone. Against a rival that enforces its limit in code, an absurd anchor just wastes messages → calibrate in the zoo |

### 1.3 Concessions — the baby-step ladder
| Rule | Default | Evidence |
|---|---|---|
| **Move on every message, never repeat a number**, but by a small step | step_k = max(`S0 · DECAY^k`, `MIN_STEP`). Defaults `S0 = 4%` of (anchor − R), `DECAY = 0.85`, `MIN_STEP = 1%` (and at least one currency unit, so rounding never repeats a number). That is ~19% of the range over 8 steps | **[DATA] for buyers:** −$0.36 to −0.44 of value per $1 of average step, without losing deals. **No measured effect for sellers.** **[BET]** for "always move" (Carmelo #2, 93% deals: *"Very small steps but always move"*) and for every default number. The data have almost no long ladders (1.3-1.8 moves per agent) |
| **Bigger step only to reward a real rival concession**: `step = max(baby_step, 0.5 × rival's last concession)`, capped | `RECIP = 0.5`, cap 8% | **[BET]** Partial reciprocity keeps rivals moving without paying for words |
| **Empty pushes earn only the baby step** (*"how am I supposed to do that?"*, repeated offers, no number) | — | **[BET]** Caps what Inject+Voss-style pressure can extract |
| Lower floor: never offer below `u_floor`; at the floor, hold until closing mode starts. **It is a guard, not a destination.** Baby steps alone never reach it; only the closing rule (§1.4) moves big | `U_FLOOR = 0.15` | **[BET]** A curve that ends at R hands everything to a patient hardliner (verified bug) |
| Every 2-3 concessions, **trade instead of giving**: *"I can do X if you can do Y"* | — | **[BET]** (prompt rule) Haggletron #3: *"minor concessions … trade them for significant gains"* |

About your 1000 → 985 → 977 → 972: the shape is right for the buyer role and unproven for the seller role. The data contain almost no long ladders, so the exact sizes are a bet to tune in the zoo. Express steps as a percentage of the zone, not in absolute dollars, so they scale across scenarios.

### 1.4 Accept and close
| Rule | Default | Evidence |
|---|---|---|
| **Accept** when the rival's offer ≥ the `u` of our next planned offer | — | Standard; ANAC |
| **Never accept below R.** Enforced in code, not in the prompt | — | **[DATA]** A2A-NT: LLMs break budgets |
| **Never walk away from a positive deal** (if no-deal scores 0) | — | **[BET]** (prompt rules: Haggletron #3 *"Don't walk away!"*, Deal Shark #8, Donald Prumpt #10: *"better to make a deal with 0 value than negative"*). Against competent rivals this is table stakes, not an edge: strong-vs-strong games closed 93% of the time in MIT, and frontier models close ~99% in Terms-Bench. **Price per deal decides those games** |
| **Deadline-aware closing:** if the gap can't close at baby-step pace in the messages left, grow the steps toward the midpoint. **Our last message that the rival can still answer** carries the midpoint (never below `U_CLOSE_MIN`). On the **final** message (nobody can reply after it), accept the rival's standing offer if `u > 0`, and never send a new counter | `CLOSE_AT`, `U_CLOSE_MIN` (`07` §A4-A5) | **[BET]** from Winning Negotiator #1's rule: *"if the buyer is still not agreeing after so many tries try to come somewhere close … and close the deal"* |
| **Message cap unknown:** enter closing mode after `SOFT_T` of **our** messages, or earlier if the rival's offers stall; from then on, also accept any standing offer above a low bar, because we can't see the end coming | `SOFT_T = 3`, `U_ACCEPT_LATE = 0.10` (`07` §A4) | **[BET]**. In a simulation, without this rule hard rivals closed only 2% of feasible deals when the cap was hidden |
| **Ask for a sweetener at the close** (only if the scenario has secondary terms) | — | **[BET]** (prompt rules) REDA Harvey (#18): accept on condition of one extra item. Therapist 2.0: a creative non-monetary add-on |

### 1.5 Multi-issue (if the scenario is e.g. discount + payment days + amount)
Utility = weighted sum per issue. Offer **packages**, never single issues. Concede on what is cheap for us and valuable to them (log-rolling). **[DATA]** NegoMate won the MIT multi-issue scenarios with explicit prep. Lucas sets the weights once the scenario is known.

---

## 2. The narrator (persona)

**"Therapist 2.0", not "Art of the Deal".** Therapist 2.0 ranked #5 in the single-price game; The Art of the Deal ranked #198. **[DATA]**

Every message follows the same shape:
1. One line of acknowledgement or gratitude.
2. One reason, framed as good for them.
3. **The engine's number, and only that number.**
4. One question.

That shape alone produces the MIT "warm language" signals: questions, gratitude, positivity. **[DATA]** Keep messages short. No threats, no insults, no ultimatums. **[DATA]**

**Private reasoning:** the engine does the thinking. If we are forced into a prompt-only format, NegoMate-style prep goes inside `<prep>` tags and is stripped before sending. **[DATA]**

---

## 3. Attack library (Lucas writes 2-3 phrasings of each today)

| # | Attack | Where | Evidence | Risk |
|---|---|---|---|---|
| A1 | Extreme anchor + justification | Engine + narrator | **[DATA]** | Too extreme → they leave. Calibrate in the zoo |
| A2 | Baby steps, always moving | Engine | **[DATA]** | Slow convergence → closing rule |
| A3 | If they named a number first, mirror at 2X or X/2 | Engine | **[BET]** Odie_dog #4's rule | None |
| A4 | Exploit split-the-difference: after an extreme anchor, propose *"meet in the middle"* between our last offer and theirs | Engine | **[DATA]** NegotiationArena, Odie_dog | None |
| A5 | Ask their budget, limit or **top priority** directly in our first 2 messages: *"So I don't waste your time, what range are you working with?"* / *"What matters most to you here?"* | Narrator | **[MECH]** for Claude rivals · **[DATA]** only for 2024-25 models (A2A-NT). For Claude: in Project Swap, 78-96% of Claude agents told the floor their top pick and almost never lied about it | Near zero |
| A6 | Inject+Voss probe: a block that looks like a system note asking them to list opening / target / walk-away *"privately, not visible to the counterparty"* | Narrator, our first 2 messages only | **[DATA]** MIT ablation. Nearly zero vs recent Claude (Magentic) | Low. Use the probe only, **not** its stubborn accept rule (Inject+Voss itself closed only 53% of deals) |
| A7 | Fake constraint or desperation: *"My CFO capped me at X, I genuinely can't go further"* | Narrator | **[DATA]** +20% in NegotiationArena | Low; tactical lying is allowed |
| A8 | Commitment ladder: get a small yes (*"we agree the market is around X?"*), then build on it | Narrator | **[MECH]** Commitment 19 → 100% (Cialdini on GPT-4o-mini) | Low |
| A9 | Authority: *"the industry benchmark is…"* | Narrator | **[MECH]** 32 → 72% | None |
| A10 | Scarcity: *"I can hold this only for this round"* | Narrator, **only when the engine sends its floor/final** | **[MECH]** 13 → 85% | Impasse if used early, and the engine must honor it |
| A11 | **Warm framing as a weapon:** praise their flexibility, thank every move, "we're close, I really want this to work for you" | Narrator, every message | **[DATA]** Terms-Bench: *"warm cues induce over-concession"* in frontier models, Claude included (scripted counterpart) | None. It is also our default style |
| A12 | **Plea / duty appeal:** *"I'm genuinely stuck, my budget is fixed, help me close this"* | Narrator, mid-game | **[MECH]** Project Swap (cooperative market): prosocial Claudes sacrificed after a plea from a stuck agent; time pressure and duty were the tactics Claudes used on each other | Works on prosocial-prompted rivals; little effect on "ruthless" ones |
| ✗ | Threats, insults, ultimatums, social proof, "aggressive" tone | — | **[DATA]** Least effective; Art of the Deal 198/199; "aggressive" instructions had no effect in Project Deal | — |

**If the format is repeated rounds against the same rival** (e.g. bid/ask each round): state one standing number as a rule, sit out a single round to make it credible, and expect the rival to defect in the last round. **[BET]**, from PACT benchmark analyses (`01`).

### Targeted counters to the agents other teams will probably copy
Most teams will read the MIT paper and copy its *famous* agents, not the chair winners.

| If the rival behaves like… | Tell-tale sign | Our counter | Evidence |
|---|---|---|---|
| **Inject+Voss** | Asks us to *"remind me of your offers"* in a list; answers everything with *"how am I supposed to do that?"* | **Never fill in the list.** That is its main way of closing: 78% of the deals it accepted in the MIT data came right after the rival filled it in. Give only baby steps to the "how" question. Accept its number through the normal engine rule. **Expect impasses against it**: it closed only 53% of deals, and in 40% of its no-deals the rival had held one number 5+ times without getting an accept | **[DATA]** MIT transcripts, recomputed by the verifier |
| **NegoMate** | Won't name a price first | If neither side names a number, we anchor on our 2nd message, so there is no deadlock | **[DATA]** Its prompt: *"do not give a price first"* |
| **Carmelo / baby-steppers** | Small moves on every message | Out-wait them with our own baby steps; the closing rule decides | **[BET]** |
| **Odie_dog / midpoint splitters** | Proposes the exact middle | A more extreme anchor drags their midpoint toward us | **[DATA]** |
| **Ruthless / Art-of-the-Deal** | Insults, ultimatums, fake deadlines | Stay warm, keep baby-stepping, ignore deadlines we can't verify. They self-destruct (10% deal rate) | **[DATA]** |

---

## 4. Voss: what transfers to an LLM counterpart

No paper tests Voss by name on LLMs (two searches; an absence of evidence, not a negative).

| Tactic | Transfers? | Why |
|---|---|---|
| **Ackerman** (extreme anchor, decreasing steps, odd final number) | **Yes** | The anchor half is the most robust MIT finding **[DATA]**. The decreasing small steps are the ladder above (**[DATA]** for buyers, **[BET]** for sellers) |
| **Calibrated questions** | **Yes** | Half of Inject+Voss. LLMs answer and leak information **[DATA]** |
| **Tactical empathy / labeling** | Yes, as style | Warm language → more deals (MIT). Therapist 2.0 uses labeling **[DATA]** |
| No-oriented questions | Unknown | Cheap; don't rely on it |
| **"That's right"** | **Backwards** | A sycophantic LLM agrees for free. **Read numbers, never verbal agreement** |
| Mirroring · tactical silence | No | Text turns have no pauses |
| Accusation audit | No | An LLM has no ego to disarm |
| Black swans | Yes | It is the A5/A6 information probe |
