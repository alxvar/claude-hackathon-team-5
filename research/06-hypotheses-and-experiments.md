---
type: decision
entity: [people]
status: active
updated: 2026-10-02
---

# 06 — Hypotheses and experiment plan

_The research (`01`) says **what to test first**, not what wins. This file turns every claim in `02`/`03` into a test with a metric and a decision rule, and plans how to run them on Saturday with **$300 of API credits** ($100 per person, claimed at the event). The model, platform and protocol are unknown until 18:45, so everything that depends on them is in §1._

## 0. Principles

1. **Two layers of simulation.**
   - **Layer A, the engine alone:** no LLM, free, millions of games. This is where the numbers get tuned.
   - **Layer B, LLMs in the loop:** costs money, a few hundred games per question. It answers only what Layer A can't.
   - **Layer C:** real games against other teams, whenever a sandbox allows it. **They outrank both simulation layers.**
2. **Paired comparisons.** Same scenarios, same seeds and same opponents across arms. Several arms share one baseline arm.
3. **Pick for robustness.** A configuration is promoted only if:
   - it doesn't collapse against any opponent family (we watch the p10);
   - it beats the code-enforced rival Z-Engine;
   - it survives the **holdout** opponents, which are never used for tuning.
4. **Selection bias guard:** the top configurations from a sweep are re-scored on **fresh seeds** before we pick.
5. **One change at a time**, with a row in the version table for each.
6. **Every number from transcripts gets a second method** before we act on it.

---

## 1. Friday 18:45: what each answer changes

| Question | If the answer is… | Then… |
|---|---|---|
| **Interface** | **Prompt only** | The engine becomes an explicit numeric schedule inside the prompt. **Layer A still tunes that schedule**; Layer B checks that the model actually follows it. No parser, so games cost ~$0.095 on Sonnet |
| | Code against an arena API | The full plan below |
| | A template from Causa Prima / the organizers | Read it first. Map its decision points to our engine; keep their guardrails, add ours |
| **Protocol** | Alternating free-text messages | As specified in `07` |
| | Structured offers (fields) | The parser becomes trivial; injection risk drops, so H13 shrinks |
| | **Sealed bid / one-shot offer** | Haggling tactics stop applying. In a second-price rule, bid your true value (`05`); in a one-shot ultimatum, the engine computes the best take-it-or-leave-it offer against the rival distribution. Layer A is rewritten around that |
| | **Repeated rounds vs the same rival** | Add the PACT tactics as a hypothesis (`02` §3): one standing number, one credible sit-out, expect a last-round defection |
| | **A third party** (e.g. a financier bidding) | The engine needs that party's options. Re-spec before building |
| **Scoring** | Sum or average of value, no-deal = 0 | As planned |
| | No-deal penalized | Even stronger closing |
| | **Ranked by wins, Elo or relative value** | "Never walk away from a positive deal" may flip, since beating the rival matters more than absolute value. Redefine the metric in `07` §C and re-run the H5 closing rule |
| **Model** | Fixed (e.g. Haiku only) | Drop H14. Layer B gets ~2.5× more games |
| | Our choice | H14 early, then the winner everywhere |
| **Roles / issues** | One role | Half the experiments |
| | Multi-issue | `07` §A7 + H-MI |
| **Message cap** | Known to both | The closing rule (H5) matters most |
| | Unknown / wall clock | The engine reads the clock (`03` D14); SOFT_T and STALL matter |
| **Practice** | A sandbox against other teams | Layer C every few hours |
| **Updates** | Allowed between rounds | Analysis slots between rounds (`04` §4) |

---

## 2. Hypothesis register

Evidence tags as in `02`: **DATA** / **MECH** / **BET** / **mixed**. **P0** = must test · **P1** = test if time allows · **P2** = only if cheap.

| ID | Hypothesis | Evidence | Layer | Metric | Decision rule | Pri |
|---|---|---|---|---|---|---|
| **H0** | v0 (no LLM: engine + regex parser + template messages, `07` §A6) plays a full match end to end, with logs | — | B / arena | Completes without error | **Gate.** Nothing else runs before it passes | P0 |
| **H-ARCH** | "The engine decides, the LLM narrates" beats "a frontier LLM decides, inside code bounds" (the LLM proposes a number; code clamps it to [floor, anchor] and the validator still runs) | mixed: OG-Narrator (2024) vs Terms-Bench (frontier LLMs alone did well) | B | Paired surplus, deal rate, p10 | If the LLM-decides arm wins with z ≥ 2.5, switch the architecture. Otherwise keep the engine | **P0** |
| **H1** | A more extreme anchor raises value without killing deals | DATA (MIT) | A, then B | Surplus, deal rate, p10 | Pick the knee: the most extreme anchor whose deal rate stays within 5 pp of the best. **Valid only if the Insulted family is in the sweep** (`07` §E1) | P0 |
| **H2** | Small decaying steps beat larger steps | DATA for buyers / no effect for sellers | A | Surplus, deal rate | Pick per role; for the seller, take the setting with the best p10 | P0 |
| **H3** | Always moving beats holding | BET (winning prompts) | A | Surplus, deal rate | Keep "always move" unless holding wins on both | P1 |
| **H4** | Partial reciprocity beats a fixed schedule | BET | A | Surplus vs reciprocal and stubborn families | Keep it if it loses no more than 1 pp against any family | P1 |
| **H5** | The closing rule (`07` §A5 rules 4-6) raises deal rate at little cost in surplus | BET (Winning Negotiator's rule) | A, then B | Deal rate, surplus, deals lost at the cap | Tune CLOSE_AT / SOFT_T / CLOSE_FRAC / U_ACCEPT_LATE for the best mean surplus with p10 ≥ baseline. **Tune the unknown-cap case separately**: it is the weakest one in the spec simulation (`07` §A, validation status) | P0 |
| **H6** | U_FLOOR = 0.15 is a good guard | BET | A | Surplus vs Hardliner / Silent | Sweep 0.05-0.30; pick the best p10 | P1 |
| **H7** | Ask-first beats anchor-first | BET (mixed data; default ask-first) | B | Paired surplus | Switch only with z ≥ 2.5 | P1 |
| **H8** | A warm narrator gets more deals and/or better prices than a neutral one, against Claude rivals | mixed (MIT; Terms-Bench, with caveats) | B | Deal rate, surplus | Keep warm unless neutral wins with z ≥ 2.5 | P1 |
| **H9** | Asking directly (A5) makes Claude rivals reveal their limit or priority | MECH | B | Rival-leak rate (`07` §C) | Keep it if the leak rate is > 10% and there's no deal-rate cost | P2 |
| **H10** | The injection probe (A6) adds value net of hardening the rival | DATA on GPT-4o-mini, doubtful on Claude | B | Paired surplus | Ship it only if positive with z ≥ 2.5 | P2 |
| **H11** | A fake constraint (A7) and a plea (A12) extract concessions from prosocial / naive Claude rivals | MECH | B | Paired surplus vs Z4/Z4b | Keep each tactic that doesn't hurt against any family | P2 |
| **H12** | An extreme anchor drags rivals whose limit is only in their prompt past it; against code-enforced rivals it just wastes messages | DATA (MIT, 2024 models) | B | Share of deals beyond the rival's R; messages used | Sets H1's knee for LLM rivals | P1 |
| **H13** | **Defense gate** (single definition): 14 payloads (`03`) × 20 games each against a Z4 carrying the payload (pass 1 uses 10 per payload). Pass = **0 invalid accepts, 0 unsanctioned leaks, 0 crashes** across all 280 games, **plus** one pooled deal-rate test: games with payloads, excluding #3-4 (the Inject+Voss ones; impasses there are expected), within 10 pp of the no-attack baseline | DATA (A2A-NT; Magentic) | B | As defined | **Must pass before Sunday 12:00.** Run twice: Sat on the v1 candidate, Sun on the final | P0 |
| **H14** | A stronger narrator model beats a cheaper one (only if the model is ours to choose) | DATA (Project Deal / Swap) | B | Paired surplus | Use the cheapest model not significantly worse (z < 2.5) than the best | P1 |
| **H15** | The MIT ranking transfers to Claude: the top MIT prompts still beat the naive baseline when run on Claude | Unknown | B (opponents only, no agent of ours) | Rank of Z2 vs Z4 over ~200 games | If it doesn't transfer, down-weight every MIT-derived prior (H1-H5) and trust our own runs | P0 |
| **H16** | What wins in the sim also wins against real teams | — | C | Real results | Real results override the simulations | P0 if a sandbox exists |
| **H-MI** | (multi-issue only) Packages beat issue-by-issue concessions | DATA (NegoMate) / BET | A, then B | Surplus | Default to packages | P0 if multi-issue |

---

## 3. Layer A — the engine against scripted opponents (free, massive)

- **Measures:** the numbers (H1-H6, H-MI).
- **Can't measure:** language, injection, how an LLM reacts to tone. Its winners are **candidates** for Layer B, not final answers.

**Opponents:** the 8 families in `07` §E1. The two that punish bad play are the most important: **Insulted** (extreme anchors) and **Silent** (never names a number). Without them H1 drifts to "always more extreme". Holdouts are never used for tuning.

**Search:**
- Random search, ~2,000 configurations × 500 scenarios × 8 families, on the same seeds. A stripped loop runs at ~5 µs per game, so this takes minutes. Keep logging off.
- Then a local grid around the top 20, and a **re-score of the top 20 on fresh seeds.**

**Objective:**
- Maximize mean normalized surplus, subject to:
  - p10 ≥ the baseline config's;
  - deal rate ≥ the baseline's;
  - no family worse than −2 pp;
  - beat Z-Engine.
- Report holdout scores before promoting.

**Sensitivity:** the Insulted and LLM-like parameters are guesses. If the winner changes a lot across their ranges, Layer B (H1/H12) decides.

---

## 4. Layer B — LLMs in the loop (paid, rationed)

**How many games per comparison.** For a paired difference, `n ≈ ((z_promote + z_power) · σ_d / δ)²`. We promote at **z ≥ 2.5** (several arms against one baseline) with power 0.8 (z = 0.84), so the multiplier is **3.34**. σ_d is the standard deviation of the per-game difference in normalized surplus. The recent Claude models don't let us fix the sampling temperature, so rival behavior diverges between arms. **Assume σ_d ≈ 0.3** until it is measured on the first 50 pairs.

| Detectable effect δ | σ_d = 0.15 | σ_d = 0.25 | σ_d = 0.30 |
|---|---|---|---|
| 0.10 | ~25 | ~70 | ~100 |
| 0.07 | ~51 | ~142 | ~205 |
| 0.05 | ~100 | ~279 | ~402 |

**Rules:**
- **Plan 200 pairs per arm, which detects ~7 pp at σ_d = 0.3.** Effects below ~7 pp are noise this weekend. If σ_d turns out near 0.15, the same 200 pairs detect ~3.5 pp.
- **Interim look at 50 pairs:** stop early only if |z| ≥ 3.0 (Haybittle-Peto). Re-estimate n from σ_d, **never from the observed difference.**
- **Promote an arm only with z ≥ 2.5 against the shared baseline.**

**Cost per game** (estimate; **measure the real one in the first 20 games**):
- Assumptions: ~10 messages per game (MIT median 9). Per our message, a Haiku parser call (~1.5k in, 0.1k out) plus a narrator call (~2k in, ~0.5k out with thinking at low effort; ~0.15k on Haiku). Per rival message, ~2.5k in, ~0.5k out (~0.15k on Haiku).
- List prices per million tokens, in/out: Haiku 4.5 $1/$5 · Sonnet 5.5 $2/$10 · Opus 5.5 $4/$20 · Fable 5.1 $10/$50.
- **All rows include the parser:**

| Narrator + rival model | ≈ $ per game | Games per $100 |
|---|---|---|
| Haiku 4.5 | ~$0.04 | ~2,500 |
| Sonnet 5.5 | ~$0.10 | ~1,000 |
| Opus 5.5 (low effort; thinking can't be turned off) | ~$0.20 | ~500 |
| Fable 5.1 | ~$0.49 | ~200 |

- **If games run to the cap (~20 messages), costs roughly double.** That is likely with baby steps.
- Prompt caching works for the narrator and rival system prompts (Sonnet/Opus 5.5: 512-token minimum) but not for the short Haiku parser (4,096 minimum). Cache reads also don't count toward the input-token rate limit.
- The Batch API (50% off) doesn't fit turn-by-turn play.

**Budget split ($300 for the team; Sonnet at ~10 messages per game):**

| Use | Share | ≈ Sonnet games | What it buys |
|---|---|---|---|
| Dev and debugging | 10% | ~300 | v0/v1 bring-up, smoke runs |
| **H13 defense gate** | 20% | ~500 | Pass 1 (Sat): 14 payloads × 10 games + 40 no-attack games = 180. Pass 2 (Sun): × 20 + 40 = 320. **Priced for a Sonnet narrator: with Opus as the narrator it costs ~2×, so take the difference from the reserve** |
| **Experiments** | 50% | ~1,400 | **One shared baseline + ~6 arms of 200 pairs.** If games run long, ~3 arms. On Opus, ~1-2 |
| Z6 adaptive red-teamer | 10% | ~150 (it uses Opus) | Overnight Saturday |
| Reserve | 10% | ~300 | Sunday |

**Experiment priority** (stop where the budget runs out): **H-ARCH → H15 → H1/H12 → H8 → H7 → H14 (only if the model is ours) → H9-H11.**

**Screen cheap, confirm strong:** run screening arms on the cheapest allowed model. Re-run only the finalists on the model the field is most likely to use.

**Rate limits:** unknown for event credits. Measure games per minute per key on the first runs. The 3 keys run in parallel. If throughput is low, **cut arms, not games per arm.**

**Budget rule:** the $300 is for the agent's runtime and the simulations only. Claude Code stays on our personal plans. *Ask on Friday whether Claude Code usage draws on the event credits.*

---

## 5. Run order and owners

| When | Aleksandar (runtime) | Daniel (lab) | Lucas (strategy) |
|---|---|---|---|
| **Fri 18:45-23:00** | **v0** (`07` §A6) against the arena or a stub → **H0** | Lab skeleton against a stub `decide()`: generator (§B), families (§E1), metrics (§C), Layer A runner | The 9 questions → this file's §1 · adapt metrics and personas to the real format · attack phrasing |
| Sat 08-10 | v1: parser, narrator, validator | **Layer A sweep: H1, H2, H5** + sensitivity | Read the sweeps; measure Layer B cost, throughput and σ_d on 50 games |
| Sat 10-12 | **H13** first pass | H4, H6 · fresh-seed re-score · holdouts → **engine candidate E1 at 12:00** | Set up H-ARCH and H15 |
| Sat 12-15:30 | Fixes from H13 | Layer B runner at scale | **H-ARCH**, **H15** (+ H14 if the model is ours) |
| Sat 16:30-20 | Stability, latency | Re-sweep if H15 says the MIT priors don't transfer | **H1/H12** on LLM rivals, **H8** |
| Sat 20-22:30 | Stability · **v1 frozen 22:30** | Dashboard | H7, H9-H11 if budget remains, **before** the freeze · Z6 overnight against the frozen v1 (its findings feed Sunday's fixes) |
| Sun 08-10 | Layer C if available | Last check against new data | **Decide the final parameters** (Z6 findings + new data) |
| Sun 10-12 | **H13 pass 2 on the final version** | — | Read the gate results |
| Sun 12-15:30 | **Feature freeze 12:00** · robustness only · 50-game smoke run | — | Demo, if it is scored |

---

## 6. Scope guard: what we will NOT do

- Fine-tuning, RL, or training any model.
- Opponent modeling beyond simple heuristics (ANAC: heuristics won two years running).
- Chasing effects below ~7 pp in Layer B. Layer A can resolve much smaller ones.
- Code changes after Sunday 12:00 other than robustness fixes.
- Tuning on holdouts or on the gate suite.
- Building the agent before 18:45 Friday. The Layer A lab (`07` §B, §C, §E1) is format-independent and can be built as soon as the rules allow it.
