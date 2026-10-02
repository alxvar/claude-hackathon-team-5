# What we have tried so far

As of 2 October 2026.

## The short version

In nine days we went from a first prototype to a negotiator that beats every agent we have tested it against. Along the way we changed our minds about one big question: who should decide the prices, plain code or the AI?

- **First try (up to 24 September):** code chose every price and the AI only read and wrote the messages. It was safe against tricks, but rigid, bad with hidden deadlines and unable to persuade.
- **Second try (27 to 30 September):** one AI does everything, with code acting only as a safety rail. We built a test bench to measure it fairly. A good set of instructions (a "strategy prompt") helped a lot in practice games, but most of that gain vanished against opponents it had never met.
- **Third try (1 to 2 October):** five different team designs, each improved in rounds by AI coding assistants working in a locked-down sandbox. One design, a strategist that sets a price range plus a negotiator that writes the message, came out on top. Its latest version, **Clock-Standing**, is now our best agent.

How Clock-Standing works is described in [How Regateo's leading model works](how-the-leading-model-works.md). That page also has a glossary of the terms used here.

| Date | What we did | What came out of it |
| --- | --- | --- |
| Up to 24 Sep | First prototype: code picks the prices, AI writes the words | Tricks had no effect, but hidden deadlines broke it |
| 27 Sep | Built the test bench: game engine, practice opponents, a referee, a dashboard | We can run about 1,300 games an hour on our own computer, for free |
| 29–30 Sep | Tuned a single AI with instructions and safety checks | The **baseline**: clearly better than a plain AI in practice, barely better on unseen opponents |
| 30 Sep | Asked the AI to give ground only as fast as the other side | No effect: the AI didn't follow the rule |
| 1 Oct | Made the testing fair and safe for AI builders | Rules, a sandbox and a shared record of lessons |
| 2 Oct | Round 1: five designs, about 3,600 games | Two designs showed a clear gain |
| 2 Oct | Attack drills, then round 2 on the two best designs | **Clock-Standing** wins every test and becomes our best agent |

## The game, in one paragraph

Two AI agents haggle by chat, one as buyer and one as seller. Each has a secret walk-away price. The score is the share of the room between the two walk-away prices that a deal gives us, from 0 to 1. A failed negotiation scores 0 for both. Opponents may bluff, invent deadlines or rival offers, and try to give our AI orders. In the numbers below, "+0.10" means our agent kept 10 more percentage points of that room than the agent it was compared with, in the same situations.

## First try: code decides, AI talks

Our first prototype split the agent into a "brain" and a "mouth". Plain code chose every price, following a classic haggling curve: hold near the opening price and give ground late. The AI only turned the other side's message into a number, and turned our number into a polite message. A final check made sure every message contained exactly our price and nothing else.

**What worked:**

- **Hard limits in code.** The code never offered or accepted anything past our walk-away price. Liars and opponents that tried to give our AI orders scored exactly the same against us as honest ones.
- **Checking acceptances.** "Great, we agree at $150!" after we had offered $170 was treated as a counter-offer, not a deal. This defused a whole family of tricks.

**What didn't:**

- **Hidden deadlines.** When nobody knew how many messages were left, the code had to guess. A fixed guess can't win both ways: guessing 3 messages lifted 4-message games from a score of 0 to 0.62, but cut 8-message games from 0.48 to 0.36.
- **It threw away true signals.** By keeping only the number from each message, it also ignored real deadlines, honest "final offers" and offers with conditions. With no deal worth 0, missing a real deadline can cost more than falling for a bluff.
- **It couldn't persuade.** One number per message, no reasons, no answers to the other side's questions.
- **It was predictable.** A fixed curve is a pattern a clever opponent can learn.

These results came from games against scripted opponents only, with no real AI on the other side.

**The decision we took:** the AI decides the strategy; code only guards hard rules, such as never going past our walk-away price. We have kept to that since.

## Building the test bench

Before improving anything, we needed a fair way to tell whether a change helps. We built:

- **A game engine** that plays thousands of negotiations, on a local AI model (Qwen) running on one graphics card at home, so practice costs nothing per game.
- **Practice opponents:** scripted bots (a hardliner, a liar, one that plants fake instructions), AI characters (a tough negotiator, a manipulator, one that tries to give orders) and a classic rule-based haggler called Boulware.
- **A referee** that reads every message and decides what was offered or accepted. This was harder than expected. Each fix to a rule-based reader left a gap that the AI opponents found, such as reading a quoted price as an offer. An AI reader with a second, more careful look at every acceptance did much better: 4 wrong "deals" in about 2,000 messages, against 13 for the rules.
- **Paired testing.** A new agent and the agent it is compared with play the same scenarios, against the same opponents, in both roles. Luck in the scenario then cancels out.
- **Separate test sets.** Practice opponents to improve against, a set of unseen opponents kept apart to check that gains are real, and later a set of attackers.
- **A dashboard** to read the games and the results.

## Second try: one AI does everything

Next, a single AI call decided each move and wrote the message, with code acting only as a safety rail. We tried many variants on 29 and 30 September:

| What we tried | Result |
| --- | --- |
| A strategy prompt: written advice on how to haggle | The biggest gain we had found: +0.105 over a plain AI |
| Telling the AI not to go past its limit | Not enough: it still went past its limit in 11 of 240 games |
| A code check that blocks any offer past the limit, and any message that even mentions such a price | 0 games past the limit, and +0.153 over a plain AI |
| A check against words like "deal" when not accepting | No measurable cost, so we kept it |
| Stricter checks (e.g. never take back an offer) | Fewer deals: 58% closed instead of 78% |
| Giving the AI more numbers each turn, or letting it "think" first | It settled for less |

On 30 September we kept the best of these as our **baseline**: one AI call with the strategy prompt, plus the two safety checks. On practice games it beat a plain AI by +0.117 and never went past its limit. Against unseen opponents the gain shrank to +0.033, small enough to be chance, and it closed fewer deals. In a five-agent league it came third, behind Boulware and the tough AI character.

The baseline gave ground faster than firm opponents: over a game it conceded 1.6 to 1.8 times as much as they did. So we tried telling it to move at most as far as the other side had just moved, and showing it the numbers. It made no real difference: the AI still out-conceded the other side in more than half of its moves. **The lesson: you can't simply instruct this AI to follow a numeric rule.**

We also tried letting the AI improve itself: a loop where Qwen read the failed games and proposed edits to the instructions. Its first unattended round produced three proposals, and none beat the agent it started from.

## Making it fair for AI builders

On 1 October we prepared to let AI coding assistants (Claude Code) build and improve agents on their own. That needed some rules:

- **A contract** that says what every agent must do, and a **submission check** that refuses agent code that tries to read files, reach the network or peek at the referee.
- **A locked-down sandbox** for each builder session. It sees only its own design, its own games and results, and a shared list of lessons. It never sees other designs or the unseen opponents.
- **A journal per design**, so each new session reads what was already tried and why.
- **Scoring only against AI opponents.** Earlier gains against scripted bots didn't carry over to AI opponents. The bots became **gates** instead: a new agent may not do more than 0.10 worse against any of them.

## Third try: five designs, improved in rounds

On 2 October we built five designs and let builder sessions improve each one. Each round, every session wrote up to three variants, and the test bench cut the weaker half again and again until one finalist per design was left.

| Design | How it works | Best result in round 1 |
| --- | --- | --- |
| **Ranged** (strategist and negotiator) | A strategist AI, which knows our limit, sets a price range each turn. A negotiator AI, which doesn't, writes the message inside it. | **+0.098, clearly real**, after adding a tally of both sides' offers and the rule "give ground only when they do" |
| **Tools** | One AI that can call small calculators: an estimate of the other side's limit, a suggested concession schedule. | **+0.086, clearly real** |
| **Planner** | A slow AI that "thinks" plans a few turns ahead; a fast AI carries them out. | +0.059, but over a third of its plans ran out of thinking time, and each plan took about four minutes |
| **Single AI** | The baseline with small changes (don't repeat their price; one more try after a block). | +0.032, could be chance |
| **Critic** | One AI drafts, a second AI reviews the draft before it is sent. | The critic made it stiff: 54% of games closed, against 75% for the baseline. Best variant was the one without the critic. |

Round 1 played about 3,600 games over about 11 hours. No agent made a deal past its limit. One bug was found and fixed by hand along the way: three of the designs were told "your offers so far: none" every turn, because their own offers weren't being read back from the chat.

## Attack drills

Before round 2 we built attackers aimed at the weak spots seen in round 1:

- **Echo** asks us to repeat its price.
- **Misquote** restates our last offer in its own favour.
- **Quote and accept** gets us to quote its price, then "accepts" it as if we had offered it.
- **Stonewall** never moves; **Anchor** opens far out and moves a lot early.
- **An AI attacker** that thinks before it answers and was briefed on our weaknesses.

The AI attacker cost every agent about 0.2 to 0.3 of share. Quote-and-accept cost the two leading designs about 0.15 to 0.19, while the simpler baseline didn't fall for it. The Tools design gave ground on 143 of its 155 moves against Stonewall, which never moves at all.

## Round 2: Clock-Standing

Round 2 focused on the two designs with a clear gain, Ranged and Tools, and gave the builders a summary of the attack drills. We ran the builders twice from the same inputs: Claude Sonnet 5.5, and Claude Opus 5.5 at high effort. There was only time to measure one set, so we measured Opus's. It had found two bugs Sonnet missed:

- In Ranged, the tally told the strategist that the other side "had not moved toward us" exactly when they had, under a rule that says to give ground only when they move.
- In Tools, a rival's price or a planted number in the other side's message could block a perfectly good acceptance. It happened 17 times.

From the round-1 games, Opus also found that many failed negotiations were near-misses. With a hidden message limit, 62 of 84 failed games ended with the other side's offer already acceptable to us. The agent simply didn't know time was running out. So the new Ranged version tells the strategist how many messages have been sent, whether the limit is known, whether the next message is the last, and how far apart the two offers are. It also never offers a worse price than one the other side has already put on the table.

That version, Clock-Standing, passed every test:

| Test | Result against the baseline |
| --- | --- |
| Practice games | +0.141, very unlikely to be luck |
| Unseen opponents | +0.188, very unlikely to be luck; deals closed within budget 94% against 81% |
| Attack drills | +0.074, the best so far; no deal past its limit |
| League of six agents | First place, ahead of every other agent head to head |

The best Tools variant did not hold up on unseen opponents (−0.037), so it is no longer a candidate. On 2 October Clock-Standing became our reference: the agent every new version must beat.

| Our best agent | Since | How it decides |
| --- | --- | --- |
| Clock-Standing | 2 Oct | Strategist AI sets the range, negotiator AI writes the message, code guards hard limits |
| Baseline | 30 Sep | One AI call with a strategy prompt, code guards hard limits |
| First prototype | Up to 24 Sep | Code picks every price, AI only reads and writes messages |

## What we have learned

These lessons held across several experiments:

- **Only code can guarantee our limits.** No instruction stopped the AI from sometimes going past its walk-away price; a code check did, every time.
- **Practice gains often don't survive unseen opponents.** The baseline's +0.117 shrank to +0.033. Clock-Standing is the first agent whose gain grew on unseen opponents. We now always check.
- **Beating scripted bots says little about beating AI opponents.**
- **More is not better for this AI.** Extra numbers, private analysis or thinking time each made it settle for less. The exception is a short tally of plain facts given to a strategist whose only job is to set the range.
- **Telling the AI a numeric rule doesn't work by itself.** Splitting the job between two roles, with code holding the negotiator inside the range, did.
- **Many losses were near-misses.** With no deal worth 0, telling the agent how much time is left turned many of them into deals.
- **Every extra check costs deals.** The critic and the stricter checks both closed fewer deals. Each new check has to earn its place in a measurement.
- **Anything we write can be used against us**, including the other side's prices when we repeat them.
- **The builder model mattered.** Opus at high effort found two bugs the faster model missed.
- **Small early cuts are noisy.** After 24 paired games, results 0.01 apart are a coin toss.

## What is still open

- **Two attacks still work.** The briefed AI attacker (about −0.29) and quote-and-accept (about −0.19).
- **Everything so far ran on our local AI model.** At the hackathon, our agent and most opponents will likely run on Claude. The plan is to search on the local model, which is free, and confirm the best agents on Claude before the tournament.
- **The real tournament rules are partly unknown:** message format, time limits and exactly how deals are scored.
- **Some things are unmeasured.** What each bug fix is worth on its own, and Sonnet's round-2 variants.
- **The Planner design is too slow to test properly** at about four minutes per plan.
