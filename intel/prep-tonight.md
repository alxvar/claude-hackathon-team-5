# Prep for Saturday — Lucas's open requests (Sat 01:00). The operator session works through these in order.

Status: [ ] open · [~] in progress · [x] done

1. [x] Fact-check `intel/saturday-plan.md` (agent running), apply fixes, commit.
2. [x] Explain the game to Lucas in plain Spanish with examples (chat).
3. [~] Explain the market-making venue decision in plain terms, then ask Lucas: open a venue (270 P) and lower the cash floor?
4. [x] Dani: automated, exact page-gap analysis — which team has a card we need, which team needs a spare we hold, whether it
   is far enough below us; real-time alert path (Lucas's local session tells Lucas, who tells Dani in the room; his
   dashboard pulls the file); exact pitch scripts (what to say so they sell to us / buy from us). Spec in the plan + builder task.
5. [x] Stage-by-stage strategy for Sat and Sun (RET, benches, Duels I/II/III/Final, new dealers, CHA, faster ticks,
   dealer close at hour 23): add a timeline section to the plan.
6. [x] Confirm the plan maximises throughput and real-time learning (calls, offers, listings, event-driven analysts).
7. [x] Aleks: a precise Saturday brief in the repo (PLAN.md "RIGHT NOW"): duelist fixes with acceptance tests, Duels II
   prep, Sunday model, accept arbiter, cold standby, API spend check.
8. [x] Sessions tomorrow: how many, exact first prompts, model and effort for each; how to use the $100 API credits each.
9. [x] Repo cleanup + update so it is 100% accurate: inventory every file (current / historical / wrong / noise), fix
   Lucas-owned files, flag teammates' files for them.

Done so far: plan fact-checked and fixed (§1-§4E), stage table §2b, Dani's page-gap desk §6b, PLAN.md RIGHT NOW (Sat),
intel/saturday-sessions.md (prompts, models, credits). Waiting: Lucas's answer on the venue (A/B) and the cash floor;
the repo audit (item 9).

## From Lucas's questions (Sat 01:45) — plan updates to make after the Q&A
10. [ ] Judges' traceability: auto-archive data/ + logs/ + leaderboard + our score components at every round close (archive/<day>/, committed); a decision timeline; round-close snapshots.
11. [ ] Anti-deception rules: decisions only on our private values and live structured offers; never buy to flip unless the buyer's bid is live, high and confirmed in person; keep bids for page-critical cards short and addressed (our bids reveal our needs); duelist clamps prices in code.
12. [ ] Dani's pitches in natural Spanish (and English), 1-2 lines, telling the other team what THEY gain and the one action to take.
13. [ ] Spares as inventory: count our duplicates; page-completer flips only with a live high bid confirmed by Dani.
14. [ ] Duels quality loop: Lucas's builder reviews Aleks's diff; after each wave a duel review (deal rate, in-limit offers not accepted, rounds, latency); parameter changes between Duels I and II.
15. [ ] Market-making owner + learning loop: builder session owns it; record → score → replay variants offline → deploy the best before the next bench (every 2 h).
16. [ ] Experiment lane: offline experiments run in parallel (sims, replays); online experiments go through the operator with a loss budget per test; results into GAME.md. Saturday list: cap, ladder, reset, Abuela welcome price, market variants, duel variants.
