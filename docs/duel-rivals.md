# Duel rivals: who we play (Aleks, Sat 16:50)

For Aleks, the Duel Lab and Aleks's Builder, before Duels II (≈ 20:33, 68 duels, each rival team 4 times).
Data: our 68 records in `docs/duels/` (Friday practice 34, Duels I 34) and the rules. Labels: [V] read from the records
or rules, [L] inferred, [?] unknown.

## How rivals are identified
- **Each pair of consecutive duel ids is one rival team [V].** The rules say every team meets every other twice, once
  as seller and once as buyer, on the same scenario. Our 17 Duels I pairs (2296/2297 … 2584/2585) each have opposite
  roles and the same item.
  - In 9 pairs the same lines appear in both duels.
  - In 4 more, each role has its own line in a shared style (R2's "Hola.", R7, R14, R15).
  - In the other 4, one or both duels were silent.
- **Team names are hidden [V].** The alias changes per duel, and the public feed's `duel.closed` carries only the
  duel, status and item. The one exception is inferred: the silent pair 2414/2415 is most likely Team 11, whose duel
  agent never spoke in Duels I [L].
- **Wording identifies a team across sessions [V].** 7 Friday pairs use exactly the same lines as a Duels I pair, and
  1 more nearly the same, so the same bot ran on both days (table below).

## Scripted or LLM

| | Friday practice (17 teams) | Duels I (17 teams) |
|---|---|---|
| Scripted: fixed lines with the number swapped in, prices from a formula | 11 (some with only 1-2 messages) | **16** (12 sure, 4 likely: 1-3 messages each) |
| LLM-written text | **1** (pair 121/122) | **0** |
| Silent: no message, no accept | 5 | 1 (2414/2415) |

**Evidence for scripted:**
- **The same line repeats with only the number changed** [V]:
  - "N?" 30 times (2366/2367);
  - "I can do N. That is a fair deal for both of us." 21 times (2318/2319);
  - "Propongo este precio, creo que es justo para los dos." 13 times, with no number in the text at all (2506/2507).
- **Prices follow arithmetic, not judgement** [V]:
  - constant steps: 2460 +9 P every tick, 2461 −2 P every tick;
  - a fixed price forever (2366/2367);
  - an exact midpoint: 2530 moved to 97 = (82 + our 112) ÷ 2;
  - accelerating schedules that ignore our moves (2318/2319).
- **They never answer what we say** [V]: none of the 176 rival messages in Duels I names any number but its own price.

**The one LLM team** (Friday 121/122):
- unique sentences that react to us: "Thanks for moving to 112, though that step was a small one…", "a move of only four
  from you won't bridge this gap";
- a fallback line when the model fails: "I can do N. That is a fair deal for both of us."

In Duels I the same team (2318/2319) sent **only** that fallback line, 21 times, so its LLM path was off or failing all
session [L]. It may be back in Duels II. The style (an em dash, "Happy to hear your thoughts") fits Claude, the
hackathon's model, but the vendor can't be proven from text [?].

One oddity: the "N?" bot (2367) once sent "Quick one: Retiro or Malasaña for a coffee? My offer is 83." in the middle of
its repeats, then went back to "101?". It looks like a hand-written line to distract or test the other side's LLM. Ours
ignored it.

## Five behaviours and how to play them

| Cluster | Teams | How it behaves [V transcripts, L types] | Duels I for us | How to play |
|---|---|---|---|---|
| **A. Follower** | R1, R8, R14, R16, R17 | Its price comes to ours. R1 trails our offer by a shrinking %, and **drops when we concede** (2296: 101 → 97). R14 splits the difference. R16 ends on our exact number. R8 and R17 close within 1-2 messages | 10/10 deals, 26.2 P each, 3.0 rounds | Hold firm: every P we concede comes back as a lower offer. Open ambitious |
| **B. Clock** | R3, R4, R9, R12, R13, R15 | Concedes on its own schedule whatever we do: accelerating (R3), slowing (R4), constant (R9), bursts every ~3 ticks (R12), +1 P a tick (R13), a slow staircase (R15) | 11/12 deals, 12.1 P each, **7.6 rounds** | Our messages only add rounds; see the replay below. R15 is the exception: it closes only by accepting **our** offer |
| **C. Holder** | R5, R7 | R5 never moves and accepts our offer once it's inside its limit. R7 makes 3 moves of ~11 P, then sits silent and never accepts ours (it refused shares ≈ 0.46-0.61) | 3/4 deals, 6.9 P each | R7: take its number at the deadline and send nothing after its hold. R5: step towards its limit; no deal if the limits don't overlap (2367) |
| **D. Accept-only** | R2, R10, R11 | 0-2 messages, then accepts our offer with 2-3 ticks left | 6/6 deals, 10.5 P each, 1.0 round | Rounds = min(ours, theirs), so they stay at 1-2 however many offers we send: stepping down costs no decay. What they accept at the end is unknown |
| **E. Silent** | R6 (Team 11 [L]) | Never speaks or accepts | 0/2 | Silent walk; expect no deal |

## Team book (Duels I; R = rival team in duel order)

| R | Duels | First line (fingerprint) | Type | Scripted? | Friday | Duels I result |
|---|---|---|---|---|---|---|
| R1 | 2296/2297 | "Thank you for meeting me. I can do N P." (5-line cycle) | A, mirrors our offer | Yes | 227/228 | 97 in 6 rounds · 161 in 4 |
| R2 | 2314/2315 | "Hola. This one is in perfect condition. N P." / "Hola. I like it, and I can pay N P." | D | Likely | — | 68 · 72, 1 round each |
| R3 | 2318/2319 | "I can do N. That is a fair deal for both of us." | B, accelerating to a floor | Fallback only (LLM on Friday) | 121/122 | 85 · 91, 9 rounds each |
| R4 | 2356/2357 | "Propuesta justa para cerrar pronto y que ganemos los dos: N P." (4-line Spanish cycle) | B, slowing | Yes | 271/272 | 117 in 10 · 78 in 6 |
| R5 | 2366/2367 | "N?" | C, never moves | Yes | 277/278 | 110 in 5 · no deal (no overlap) |
| R6 | 2414/2415 | (silent) | E | — | silent pair | no deal ×2 |
| R7 | 2430/2431 | "N for ITEM. Every round costs us both: let's close it now." | C, 3 moves then holds | Yes | 181/182 | 184 · 134, took its number at the deadline |
| R8 | 2446/2447 | "Hello, and thank you for meeting me. I would propose N P for this one." | A, fast closer | Yes | 199/200 | 45 (took our opener) · 118 in 2 |
| R9 | 2460/2461 | "Happy to close quickly at N primas for ITEM." (then a 4-line cycle) | B, constant steps, a jump near the end (2461) | Yes | — | 198 in 10 · 150 in 12 |
| R10 | 2472/2473 | "N P y cerramos ahora." | D | Yes | — | 92 · 88, 1 round each |
| R11 | 2494/2495 | "Thank you, that's kind. I could do N P and close it today." | D | Likely | 113/114? | 74 in 2 · 107 (silent, took ours) |
| R12 | 2506/2507 | "Propongo este precio, creo que es justo para los dos." | B, bursts | Yes | — | 96 in 6 · 106 in 7 |
| R13 | 2522/2523 | "I can do N. Let's close it quickly." | B, +1 P/tick | Yes | 269/270 | 59 in 7 · no deal (silent in 2523) |
| R14 | 2530/2531 | "Hi there. N P from my side." / "Meeting you partway: N P." | A, splits the difference | Likely | — | 97 in 2 · 101 in 1 |
| R15 | 2534/2535 | "Puedo llegar a N primas. Dime si cerramos." / "Es una pieza que merece su precio: N primas." | B, slow; accepts ours at a rival share ≈ 0.27 | Yes | 175/176 | 167 · 176, 4 rounds each |
| R16 | 2540/2541 | "Hello! I can do N. Thank you for your time." (6-line cycle) | A, ends on our number | Yes | — | 90 in 7 · 87 in 6 |
| R17 | 2584/2585 | "We can do N P. Thank you for the talk." | A, opens inside our limit | Likely | — | 175 (took our opener) · 96 in 1 |

Friday teams with no Duels I match: 103/104 ("I can move a little: N."), 163/164, 257/258 ("Fair is fair: N P…"), and
the 5 silent pairs. They are among R2, R6, R9, R10, R12, R14, R16 and R17 with new wording [L].

## Tested: stay silent against clock bots
A clock bot's prices ignore ours, so its real offers can be replayed. The policy tested: after our opener, send nothing
and accept its best in-limit offer by 2 ticks left (rounds stay at 1).

| Team | Actual (P) | Silent (P) | Δ |
|---|---|---|---|
| R4 | 8.6 · 9.7 | 12.2 · 13.2 | **+7.1** |
| R9 | 14.0 · 9.5 | 23.5 · 20.7 | **+20.7** |
| R13 | 9.7 | 14.1 | **+4.4** |
| R3 | 6.3 · 3.4 | 8.5 · 0.9 | −0.3 |
| R12 | 4.8 · 3.9 | 6.6 · 0.0 | −2.1 |
| R15 | 29.7 · 33.6 | 0.0 · 9.4 | **−53.9** |
| All 12 | 133.2 | 109.0 | −24 |

- **As a rule for every rival it loses.** R15's own offers stay at or near our limit; it closes by accepting ours.
- **For R4, R9 and R13 it gains +32 P over 5 duels.** That's a per-team rule, and it needs the wording to survive into
  Duels II.
- **Not built.** Rival memory by wording is still off the build list (16:24). It is Aleks's call whether to add it
  as one strategist fact per fingerprint.

## Duels II watch list
1. **Days break unchanged bots [L].** A priced message without `days` is refused (`missing_days`). A scripted bot its
   team didn't update will look silent: no offers, so no deal, unless it accepts our offer.
2. **Wording may change** with the days update. A fingerprint match needs the first line with numbers, the item and
   the day removed.
3. **R3's LLM may come back.** Then it reacts to our words and numbers. Treat it as unknown, not as a clock.
4. **Each team plays us 4 times, 6 duels at once.** A fragile bot can go silent in one duel and not the other (R13 in
   2523, R11 in 2495).
