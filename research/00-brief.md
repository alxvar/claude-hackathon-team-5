---
type: brief
entity: [people]
status: active
updated: 2026-10-02
---

# Team 5 — one-page brief (Claude Code Hackathon Madrid, Oct 2-4)

_Aleksandar Varga · Daniel M. Díaz · Lucas Wiese. 18 teams. 1v1 buyer/seller negotiation agents, ranked by value captured, manipulation allowed. Sponsor: Causa Prima. $100 of Claude API credits each._

## Starting hypotheses (evidence in `01`; every one gets tested in `06`)

1. **Code decides the numbers, the LLM writes the words.** It is the sponsor's rule (*"LLMs inform; rules enforce"*), and in 2024 benchmarks it lifted deal rates a lot. **But it is untested against today's frontier models**, which negotiate well on their own. That is why H-ARCH is our first experiment.
2. **The model matters more than the prompt.** In Anthropic's Claude marketplace experiments, Opus beat Haiku on both sides, and "be aggressive" instructions did nothing. If we can choose the model, we take the strongest.
3. **The opening number is the most robust lever.** In the MIT competition data (~40k price negotiations), more extreme openings captured more value. Small concessions helped buyers (not sellers). "Always keep moving" comes from the winning prompts and is still a bet. Those are 2024-model results, correlational.
4. **Warm words, hard numbers.** Warmth avoids impasses but doesn't get better prices once a deal closes. Warm cues may make Claude rivals concede more (weak evidence). Our numbers stay immune to the same trick.
5. **If we write code, defenses live in code.** Our reservation value never enters any LLM context, and a validator blocks any number the engine didn't decide.

## How we'll find the best agent (`06`)

- **Layer A, the engine alone vs scripted rivals:** free, millions of games. It tunes the numbers.
- **Layer B, LLMs in the loop:** about 1,400 Sonnet-equivalent experiment games in our $300. That is one baseline plus ~6 variants of 200 paired games. It answers what Layer A can't (architecture, transfer to Claude, tone, attacks).
- **Layer C, real games against other teams**, if there's a sandbox. These outrank the simulations.
- **Rules:** paired comparisons; pick for robustness (p10, holdouts, beating our own engine); in Layer B we can only detect effects of ~7 pp or more.
- **Defense gate (H13, `06`):** 0 invalid accepts, 0 unsanctioned leaks and 0 crashes across all attack games, plus a pooled deal-rate check. Pass 1 on Saturday, pass 2 on Sunday.

## Friday 18:45-23:00: who does what

| Who | Owns | Tonight |
|---|---|---|
| **Lucas** | Strategy, parameters, prompts, attacks, reading results | Asks the questions below → applies `06` §1 · adapts metrics and personas to the real format |
| **Aleksandar** | Runtime. **The only one who merges into the competing agent** | **v0 by 23:00:** engine + regex parser + template messages, **no LLM** (`07` §A6), full match with logs |
| **Daniel** | The lab | Scenario generator, scripted opponent families, metrics and Layer A runner against a stub engine (`07` §B, §C, §E1). It works whatever the format |

**Budget rule:** the $300 is for agent runtime and simulations only. Claude Code stays on our personal plans.

## Questions for the organizers (Lucas asks)

1. Do we submit a prompt, code against an API, or a template? Which models are allowed?
2. **Protocol:** alternating free-text messages, structured offers, sealed bids, or one-shot? Repeated rounds against the same rival? Any third party?
3. **Scoring:** how is value computed, what does a no-deal score, and how are matches ranked (sum, average, wins, Elo)?
4. Both roles? One issue or several?
5. Private values: new each game? Do we know the rival's distribution?
6. Message cap known to both? Who opens? Time limit per message?
7. Is there a sandbox or practice rounds against other teams? Do we see transcripts?
8. Can we update the agent between rounds? What's forbidden?
9. Does Claude Code usage draw on the event credits?

## Milestones

| When | Milestone |
|---|---|
| Fri 23:00 | v0 plays a full match (H0) · the lab runs Layer A on a stub |
| Sat 12:00 | Engine candidate E1 · first defense-gate pass |
| Sat 22:30 | **v1 frozen** after the Layer B experiments |
| Sun 12:00 | **Feature freeze** · defense gate passed · robustness fixes only |
| Sun 15:30 | Build stops → tournament |

**Files:** `01` evidence · `02` offense · `03` defense · `04` red team, metrics, code review · `05` sponsor · `06` hypotheses and experiments · `07` spec kit · `mit-top-prompts` field-tested prompts.
