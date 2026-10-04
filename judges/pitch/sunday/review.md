# What makes a good pitch: organisers' decks, reviewed (Sun 4 Oct)

Sources: S = `Sunday.pdf`, K = `Kickoff.pdf`, P = `Payday.pdf`, plus `bazaar-kit/RULES.md`. pN = slide N.

## Criteria (verbatim + source)

- **Weight:** "Judges 40 | Your ideas and your craft" (RULES.md l.120; also K p9, P p5, S p8 "THE JUDGES: 40 POINTS"). Judges are 40 of 100. (The "40 % of the server score is still to play" on S p1 is Sunday's round weight, not the judges.)
- **Rubric:** "Ideas and craft. They read your submission. Tell them what you built, why, and what you'd do with one more day." (S p8). No sub-weights are published [?].
- **The four questions** (S p10, "WHAT MAKES A GOOD PITCH"):
  1. "How did you approach the challenge? Your first idea, and what changed it."
  2. "What did you build? Your agent, your market, your tools. Show it, don't list it."
  3. "Why did you build it that way? The decision you'd defend in front of the judges."
  4. "What did you learn? Technically, and about negotiation and marketplaces." (bold on the slide)

## Format

- **Duration:** "Presentations, in ranking order · top 3 teams: 5 min · all others: 3 min" (S p9). A top-3 finish earns 5 minutes.
- **Order:** "in ranking order". The direction isn't stated, and the ranking is presumably the 15:00 server board [?].
- **Not stated:** Q&A, who presents, whether a demo is allowed [?]. "Show it, don't list it" favours showing. All the decks are in English.

## Submission (what, where, when)

- **Where:** "Link at the bottom of the game board: Submit your project" (S p8), and "/submit closes at 16:00" (S p9). That probably means bazaar.causaprima.ai/submit [?].
- **How:** "Pick your team, enter your team key tk-…".
- **What:** "Add your code, your Claude artifacts, how your agent works, and later your slides." The format (link or upload) isn't given [?], and there's no mention of a video.
- **When:** "Save early, edit until 16:00." (S p8)

## What they asked us to show

- What we built, why, and **what we'd do with one more day** (S p8). The four questions above (S p10). Claude artifacts and how the agent works (S p8).
- Signals of what they value:
  - "Scores come only from value created. Never from activity." (K p3)
  - Team 12's bug write-up "with ticks, settlement ids and numbers … exactly the kind of work we hoped for" (S p7): evidence-grade rigour impresses them.

## Timeline (S p2, S p9)

| Time | What |
|---|---|
| ≈11:15 | Duels III |
| ≈14:15 | Grand Final: the dealers close, only team trades remain, the last duel wave |
| 15:00 | The market stops, scores freeze |
| 15–16 | Prepare the pitch and upload; /submit closes at 16:00 |
| 16–17 | Pitches, in ranking order |
| 17–17:30 | Jury deliberations |
| 17:30 | Winners; 18:00 photo and networking |

## Implications for our deck

- **Build 5 minutes with a 3-minute core.** If we're top 3 at 15:00 we get 5 minutes. Mark the skippable slides.
- **Use the four questions as the spine:** approach → build → why → learn. "First idea → what changed it" = our hypothesis → challenge → change pairs.
- **Show, don't list.** The architecture goes on one visual, with a dashboard or screenshot instead of bullets.
- **Name one decision "we'd defend".** Candidate: the code-first duelist, with the LLM only writing text [verify]. Split the learnings into technical, then negotiation/marketplace.
- **Add "one more day".** It's in the rubric (S p8) but not on the S p10 list.
- **Frame impact as value created, with evidence:** ticks, ids, [V]/[L]. Never trade counts or volume.
- **The submission is read too.** Upload code, Claude artifacts and the agent explainer before 15:00, and the slides by 16:00. Final numbers exist only after 15:00, so leave placeholders. Never put the `tk-` key in the slides or the repo.

## How our deck answers each point

| Criterion | Slide | Evidence |
|---|---|---|
| Q1 first idea → what changed it | 3 · Five beliefs our data broke (+ 6 · the loop) | 5 belief → breaker → change rows, each breaker tagged V (RET-09 −10, 9.2 s, 50.0 → 52.2, CHA-11 +1.48 both sides, 0 fills by 10:45) |
| Q2 what we built (shown, not listed) | 2 · Architecture A (control room); B and C are alternative views | every box exists in the repo (verifier pass 13:36); writers vs readers vs checkers drawn as lanes |
| Q3 the decision we'd defend | 2 + 3 · "the Chief never writes; code decides, the LLM talks" | latency 9.2 s → Haiku ≈ 2 s (docs/duelist-sunday-summary.md); Duels III 57/68 |
| Q4 learned: technical | 7 · column 1 | code-first, decide/write/check split, beliefs as bugs (round-cap lap) |
| Q4 learned: negotiation and markets | 7 · column 2 (+ 4 · impact map) | relative scoring (CHA-11), losses count / gains clip, a market needs a first trade (+4.08 over stall-only) |
| One more day | 7 · column 3 | merge the Sunday duelist + per-opponent day weights; run the staged broker; verifier gate on every directive |
| Built around the Bazaar (organisers' feed, 13:44: "lending, escrow, auctions, ZK, a market with more than two sides? Describe it in your /submit story and tell us at the desk") | 5 · Around the Bazaar + `submit-story.md` | club matchmaker (tools/matchmaker.py, intel/club-pitch.md), demand model + Neon hub, Market Test recorder + sim, live reactor, judges' showcase. **Also tell the desk in person.** |
| Result / strategy | 1 · race, 4 · impact map | #6 at Friday's final → #1 since 12:35; points by part of the system, V/L tagged |
| Submission items | upload | code (main + `duelist-loop`), Claude artifacts (this folder, intel/), how the agent works (arch A + docs/duelist-sunday-summary.md), slides (deck.html, or a PDF export) by 16:00; never the `tk-` key |
