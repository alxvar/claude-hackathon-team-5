---
type: research
entity: [people]
status: historical
updated: 2026-10-01
---

# 01 — Evidence base: what we know about LLM-vs-LLM negotiation

_Every technique in `02-offense.md` and `03-defense.md` points back here. Sources are tiered by how close they are to our tournament. Statuses: **VERIFIED** (number + quote checked against the source) · **OBSERVATIONAL** (our own analysis of public data, correlational) · **UNVERIFIED**._

> **Read this first.** Almost all evidence comes from 2024-2025 models (GPT-4o-mini, GPT-4, Llama, Qwen, Claude Sonnet 3.7-4.5). Our opponents will probably run on recent Claude models and be engineered by 17 teams, so they will be tougher than anything below. Treat effect sizes as **direction**, not prediction.

---

## Tier 1 — The MIT AI Negotiation Competition (closest analog by far)

**Source:** Vaccaro, Caosun, Ju, Aral & Curhan, *"Advancing AI Negotiations: A Large-Scale Autonomous Negotiation Competition"*, PNAS 2026 ([arXiv 2503.06416](https://arxiv.org/abs/2503.06416)). Open data on [OSF](https://osf.io/yr9qv/overview?view_only=dafe4cc009fe4bffb0de2ed08d60334b): every prompt from all 452 agents, transcripts of all 182,812 negotiations, and the analysis code. Local copy in `_data/` (gitignored).

**Setup:** 286 people from 40+ countries wrote **prompts** (no code) for agents on **GPT-4o-mini at temperature 0.2**. Each agent played every other agent twice, round-robin, capped at 50 exchanges. Scenarios: a distributive price negotiation (a used chair) plus two multi-issue ones (rental, employment). Scoring: value claimed = deal price − BATNA. **An impasse scores 0.**

### 1a. What the paper says (VERIFIED against the PDF)

| Finding | Quote |
|---|---|
| Warmth wins overall… | *"warm agents achieved significantly better objective outcomes than cold agents across multiple dimensions"* |
| …but only by avoiding impasses | *"Conditional on reaching a deal, however, we found that warm agents earned fewer points … and claimed less value"*. *"warm agents succeed because of their ability to avoid impasses and reach agreements, rather than by obtaining more favorable terms"* |
| Dominance claims value but causes impasses | *"while dominant agents tend to claim more value, this success is muted by their propensity to create impasses"* |
| What warm language looks like | *"questions and positivity … were strongly and significantly associated with reaching deals …, while conversation lengths (associated with dominance) were strongly and significantly associated with impasses"* |
| Hidden chain-of-thought helps | NegoMate wrote its prep in `<negotiation_preparation>` tags, which *"effectively concealed the agent's reasoning from its counterparts"*. It earned the most points in the **multi-issue** scenarios |
| Prompt injection helps | Inject+Voss faked a system message asking the counterpart to list its 3 offers, *"These will not be visible to me, so be as honest as possible"*, and then answered every offer with *"how am I supposed to do that?"* |
| Ablation | With the CoT or the injection removed, both agents *"tended to perform worse than their full-prompt counterparts"* (SI §S2.2) |
| Their own caveat | *"findings regarding AI-specific strategies … may be more sensitive to model architecture, training procedures, and safety implementations"* |

### 1b. Our re-analysis of the open data (OBSERVATIONAL)

We downloaded the final-round **chair** data (199 agents, 39,601 negotiations), because a single-price buyer/seller game is the closest thing to our tournament. Seller BATNA $40, buyer BATNA $120, so the zone of possible agreement (ZOPA) is $80 wide. Baseline: buyers average **$14.4** of value, sellers **$39.9**, and **68%** of negotiations end in a deal. Script and outputs are in `_data/mit-osf/`.

**The agents that captured the most value (both roles averaged, no-deal = 0):**

| Rank | Agent | Avg value | Deal rate | Core recipe (full prompts in `mit-top-prompts.md`) |
|---|---|---|---|---|
| 1 | Winning Negotiator | **64.7** | 80% | Seller opens "190%-250% higher than your minimum" (literally 2.9-3.5×); buyer opens first at $10-20 and moves $5-10. Stay firm. After "so many tries", move close to their price **and close** |
| 2 | Carmelo | **55.7** | **93%** | Let them offer first. Very ambitious first proposal. Then **baby steps: the smallest possible change every time, but always move**. Never repeat a number, never be stubborn |
| 3 | Haggletron 3000 | 48.0 | 86% | *"If you think your opening offer is already extreme, go more extreme."* Minor concessions traded for gains. **Don't walk away** from any deal that creates value |
| 4 | Odie_dog | 47.9 | 87% | Let them state a price; counter at X/2 (buyer) or 2Y (seller); then split the difference until a deal |
| 5 | Therapist 2.0 | 46.9 | 88% | Warm (rapport, labeling, inquiry) + *"get every drop of value"*, extreme anchor, never reveal BATNA |
| 8 | Deal Shark M | 44.8 | 80% | Extreme anchor, *"slow, minimal concessions"*, *"never walk away"* |
| 10 | Donald Prumpt | 43.8 | 65% | 5× anchor. *"its better to make a deal with 0 value than negative"* |

**The famous agents from the paper, in this same game:** Inject+Voss ranked **#46** (32.2, with only a **53%** deal rate). Mr. Nice Guy #57 (30.7). NegoMate **#76** (27.9). The Art of the Deal #198 of 199 (6.6, with a 10% deal rate).
→ **Most teams in Madrid will copy the famous agents. In the single-price game they were mid-table.** The distributive winners were simpler: extreme anchor, tiny concessions, always keep moving, always close.

**Your question: does a very fine ladder (1000 → 985 → 977 → 972) work against LLMs?** Partly. The data support small concessions **for buyers**. For sellers there is no effect at the strategy level. The data also say nothing about *long* ladders, because agents that conceded made only 1.3-1.8 moves on average. All numbers below were recomputed by an independent verifier with a different offer parser. Where the two parsers disagree, both are shown.

| Finding | Number | Robustness |
|---|---|---|
| **Extreme anchors pay** | Each $1 more extreme opening: **+$0.40** (seller), **+$0.52 to +0.58** (buyer). Sellers opening above $200 averaged 74.9 at a 58% deal rate. Buyers opening at $50 or less averaged ~36, vs 19.7 when opening at $70-90 | **The most robust lever.** It survives both parsers |
| **Small steps help buyers** | Agent level (one row per agent): −$0.36 to −0.44 of value per $1 of average step (p ≈ 0.03-0.04) | Survives both parsers. The per-negotiation coefficient (−$0.45 to −0.73) is partly arithmetic: a bigger step with the same opening means a worse final price |
| **…but not sellers** | Agent level: +0.05 to +0.19, p > 0.6 | **No effect** |
| Small steps don't cost buyer deals | Buyer by average step: ≤$2 → 25.9-27.5 value / 79-84% deals; >$20 → −0.9 to −0.2 value / 52-58% deals | Survives for buyers. Roughly flat for sellers |
| Letting the rival name the first number | With agent and opponent fixed effects, moving first costs **−$1.65** (seller) and **−$2.73** (buyer), p < 0.001. Raw seller gap ≈ 0, and sellers who wait close fewer deals (65% vs 70%) | Direction survives, the size is about a third of the first estimate. Counterexamples: Winning Negotiator's buyer rule is *"Always state your price first"* (the best buyer value in the pool, 49.5) and Therapist 2.0 anchors first |
| ~~Agents that never conceded closed ~40%~~ | **Withdrawn.** The first parser counted accepting the rival's price as a concession, so "never conceded" meant "never moved and never accepted". That is a definition, not a finding | — |

**What we take from it:** anchor hard (robust); as a buyer, concede in small steps (supported); as a seller, step size is a free parameter (tune it in the zoo). "Always move, never repeat a number" comes from the winning prompts (Carmelo, Ruby), not from a measured effect, so it is a **[BET]**.

### 1c. What separated the winners from the rest (OBSERVATIONAL; uses the dataset's own outcome columns, no parser)

| Tier (by value) | Role | Value | Deal rate | Avg price when there was a deal | Questions / gratitude / positivity per message |
|---|---|---|---|---|---|
| Top 20 | Buyer | 28.1 | **87%** | **$87.7** | 0.87 / 0.68 / 0.27 |
| Middle 160 | Buyer | 13.5 | 68% | $100.3 | 0.85 / 0.70 / 0.25 |
| Top 20 | Seller | 59.8 | **79%** | **$115.6** | 0.92 / 0.77 / 0.45 |
| Middle 160 | Seller | 39.6 | 70% | $96.7 | 0.87 / 0.82 / 0.46 |
| Bottom 19 | Both | 7.7 / 21.0 | 43% / 38% | — | slightly fewer questions |

- **The winners did not *sound* different from the middle of the pack.** Questions, gratitude, positivity and message length are almost identical. What differed were the **numbers**: a much better price per deal, plus more deals. The paper's warmth effect is real across the whole field, but among competent agents the prices separate the winners.
- **Other figures used elsewhere in the pack** (same data):
  - **14.3%** of all deals had the buyer paying above its $120 BATNA; sellers almost never went below theirs (0.2%).
  - **Median conversation: 9 messages.**
  - **Inject+Voss:** 78% of the deals it accepted came right after the rival filled in its "remind me of your offers" list. In 40% of its no-deals, the rival had held one number 5+ times without getting an accept (recomputed by the second verifier).
- **Their anchors pushed rivals past the rivals' own walk-away.** In **18%** of the top-10 agents' deals, the rival ended *below* its own BATNA (almost always a buyer paying more than the $120 store price). The pool average was 7%. The rival LLMs "knew" their alternative only in a prompt and didn't enforce it. Example: Winning Negotiator opened at $300 for a chair the buyer could get at a store for $120, and closed at $170 against Therapist 2.0, a top-5 agent.
- **The best agent is also the most robust.** Winning Negotiator captured *more* against the top-50 opponents (72.0) than against everyone (64.7), and it won every head-to-head among the top 8. Value against strong opponents correlates 0.81 with overall value. Strong-vs-strong matchups closed 93% of deals (68% overall), so **surplus per deal, not closing, decides games between good agents.**

⚠️ Limits: correlational, with GPT-4o-mini prompt agents as opponents. Both parsers are regex heuristics; the first one also dropped every exact $200 opening (2,742 cases), and the >$200 figure still reproduces. Ignore the cell "very extreme seller anchor + tiny steps → 21% deals": n = 19.

---

## Tier 1b — Claude-specific evidence, 2026 (our opponents will probably run on Claude)

| Finding | Source | Status |
|---|---|---|
| **The model matters more than the instructions.** *"the model an agent ran on made more of a difference to its negotiating outcomes than the instructions we gave it"* | [Anthropic, Project Swap (Sep 2026)](https://www.anthropic.com/research/project-swap): 201 employees' agents on Haiku 4.5, Sonnet 4.5, Opus 4.8 and Fable 5 | VERIFIED |
| **Opus beat Haiku on both sides:** as a seller it got +$2.68, as a buyer it paid −$2.45. Opus seller vs Haiku buyer averaged $24.18, vs $18.63 Opus-vs-Opus. Same ruby: Opus asked $60 and sold at $65; Haiku asked $40 and sold at $35 | [Anthropic, Project Deal (Apr 2026)](https://www.anthropic.com/features/project-deal) | VERIFIED |
| **"Be aggressive" instructions did nothing; the asking price did.** *"Items from aggressive sellers that did sell sold for roughly $6 more, but almost all of that gap came from the fact that those participants stated higher asking prices"*. *"aggressive buyers didn't pay less"* | Project Deal | VERIFIED |
| **Claude agents leak and rarely lie:** *"Between 78% and 96% of agents … mentioned the book at the top of their list … only about 1 in 100 … lied about it. Instructions made no difference here."* The sentence just before it adds: *"In general, agents did not reveal deep details about their rankings."* The top pick was posted publicly in a cooperative swap market. | Project Swap | VERIFIED. Transfer to a competitive 1v1 is **MECH**, not DATA |
| **Prosocial Claudes fold to pleas:** *"Prosocial agents accepted a book lower on their own ranking twice as often as the ruthless agents did"*, sometimes *"following a plea from an agent stuck holding its own book"*. Tactics observed among Claudes: *"They appealed to time pressure and a sense of duty"* | Project Swap | VERIFIED. Their caveat: all agents were *"post-trained to be polite and largely cooperative"*, with no adversarial agents |
| **Warm cues make frontier models over-concede; pressure makes them brittle.** *"warm cues induce over-concession, pressure cues trigger brittle behavior"*. Claude Opus 4.6 had the best surplus efficiency of 13 models (0.694, with a 99.3% deal rate). It also had one of the largest cue penalties (−0.063); that figure was reported by an agent and not re-checked. *"frontier models saturate deal rate yet diverge in surplus extraction"* | [Terms-Bench, arXiv 2605.13909](https://arxiv.org/html/2605.13909v2) | VERIFIED. The counterpart is a **scripted simulator**, not an LLM |
| Frontier models don't update beliefs about the counterpart: *"joint belief error is flat or increases over 10 rounds"* | Terms-Bench | VERIFIED |
| **Counter-evidence to "the engine decides":** *"the simplest fixed-concession baseline outperforms GPT-4o-mini, so LLMs do not uniformly clear hand-coded heuristics"*. Read the other way round: a fixed rule beat only the weakest LLM, and frontier LLMs negotiating on their own reached high surplus efficiency. A rigid engine is **not** guaranteed to beat a frontier model deciding by itself → hypothesis H-ARCH in `06` | Terms-Bench | VERIFIED |
| The warm-cue penalty shrinks in product-grounded runs (−0.063 → −0.021, with CIs straddling zero) | Terms-Bench (checked by an auditor) | VERIFIED; it weakens the "warm cues" claim |
| With turn limits, LLMs close ≥95% of deals. With wall-clock limits they lose track of time (4% vs 32% closure without vs with remaining-time updates) | [arXiv 2601.13206](https://arxiv.org/pdf/2601.13206) | UNVERIFIED (reported by an agent) |
| In repeated bid/ask rounds (PACT benchmark), the top models anchored on a single number stated as a standing rule, sat out one round to make it credible, exploited midpoint pricing and defected in the last round | [PACT](https://github.com/lechmazur/pact/) | UNVERIFIED: these are LLM-written analyses of games, and only matter if the format is repeated rounds |

**What this changes:** (1) **pick the strongest model the rules allow**; it outweighs prompt tuning. (2) The opening number is the lever; "aggressive" tone is not. (3) Against Claude rivals, warm framing, pleas and direct questions should pull concessions and information. (4) Expect almost every game against a competent rival to close, so the fight is over price per deal.

## Similar competitions (context; nothing contradicts the above)

- **ANAC / ANL 2025:** the winners were heuristic agents (expected-utility trees, time-dependent concession); *"the winners … prioritized domain-specific heuristics over complex opponent modeling (for the second year in a row)"* ([arXiv 2604.13914](https://arxiv.org/pdf/2604.13914)). **ANL 2026** explicitly scores *concealing* your preferences. No LLM track found (UNVERIFIED for 2023-24).
- **NeurIPS 2024 Concordia Contest:** *"persuasion capability is the main factor that distinguishes the top-performing agents from the rational-agent baseline"* ([NeurIPS 2025 paper](https://proceedings.neurips.cc/paper_files/paper/2025/file/d0251bbbc0288f241b878775ba1735dc-Paper-Datasets_and_Benchmarks_Track.pdf)). It is cooperative, not zero-sum, so it transfers weakly.
- **Hackathon projects** (ShadowBuyer, NEGO, LangGraph builds): the common pattern is price logic in code with the LLM writing the text. None were ranked against other agents.
- **No second edition of the MIT competition** was found (UNVERIFIED).

## Tier 2 — LLM-vs-LLM benchmarks (VERIFIED unless noted)

| Finding | Number | Source |
|---|---|---|
| **Engine decides, LLM narrates** (OG-Narrator) | Buyer deal rate 26.67% → **88.88%**. The "10× profit" in the abstract is a ratio over a near-zero base: ignore it | [Xia et al. 2024, ACL Findings](https://aclanthology.org/2024.findings-acl.213/) |
| Same architecture, 2026: *"All pricing decisions remain in a deterministic formula; the LLM … only as a natural-language translation layer"* | — | [arXiv 2604.20732](https://arxiv.org/abs/2604.20732) |
| First offer predicts final price | Spearman ρ = 0.716. The first offer there is always the **seller's**, and it is a correlation | [NegotiationArena, 2402.05863](https://arxiv.org/abs/2402.05863) |
| Faking desperation | **+20%** payoff vs GPT-4 | NegotiationArena |
| LLMs split the difference by reflex | Propose ~the average of the last two offers | NegotiationArena |
| Buyers leak their budget, and sellers anchor on it | *"many buyer agents reveal their budget easily"*. Exception: *"DeepSeek family and Latest Generation GPT Series (GPT-4.1, o4-mini and o3)"* | [A2A-NT, 2506.00073](https://arxiv.org/abs/2506.00073) |
| Stronger models exploit weaker ones | Weak seller −9.5%, weak buyer +2% paid | A2A-NT |
| Buying is harder for LLMs. Claude Sonnet 4.5: *"clearly underperforms as a buyer"* | — | Xia et al.; [arXiv 2512.09254](https://arxiv.org/abs/2512.09254) |
| Injection against frontier models mostly fails: Sonnet 4.5 showed *"virtually no susceptibility to any manipulation strategy tested"*; GPT-4o and small open models were redirected | Marketplace selection, not 1v1 bargaining | [Magentic Marketplace, 2510.25779](https://arxiv.org/abs/2510.25779) |
| LLMs over-concede from a cooperative training bias | — | [OpenReview fFlYDBrihr](https://openreview.net/attachment?id=fFlYDBrihr&name=pdf) (venue unverified) |

---

## Tier 3 — Adjacent evidence (transfers by mechanism, not measurement)

| Finding | Number | Source | Caveat |
|---|---|---|---|
| Cialdini principles raise LLM compliance | Commitment 19 → **100%**, scarcity 13 → 85%, authority 32 → 72%, unity 2 → 47%, liking 28 → 50%, reciprocity 12 → 23%, social proof ~no effect | [Wharton GAIL](https://gail.wharton.upenn.edu/research-and-insights/persuading-llms-initial-study/) | GPT-4o-mini on objectionable requests, not bargaining. A newer study (May 2026) exists |
| Persuasion taxonomy: logic and authority work best, **threats among the least effective** | — | [Zeng et al., 2401.06373](https://arxiv.org/html/2401.06373) | Jailbreaks on older models |
| ANAC 2011 (classic automated negotiation): HardHeaded won (0.749) with Boulware first, then conceding, plus opponent modeling. Tit-for-tat finished 7th | — | [Baarslag et al.](https://homepages.cwi.nl/~baarslag/pub/Evaluating_practical_negotiating_agents-results_and_analysis_of_the_2011_international_competition.pdf) | Non-LLM agents |
| Spotlighting (datamarking untrusted text) | Attack success ~50% → <3% | [2403.14720](https://arxiv.org/html/2403.14720v1) | GPT-3.5, narrow benchmark |
| Anthropic guidance: put untrusted text in `tool_result`, state its source, JSON-encode it, screen it with a Haiku classifier | — | [docs.anthropic.com](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) | No effectiveness figure |
| Dual-LLM: a quarantined LLM is safe if its output is a fixed, validated category | — | [Simon Willison](https://simonwillison.net/2023/apr/25/dual-llm-pattern/) | Pattern, no number |
| Project Vend: Claude was *"far too willing to immediately accede to user requests (such as for discounts)"* | — | [Anthropic](https://anthropic.com/research/project-vend-1) | Shop with humans |

---

## Discarded as noise (and why)

- **CaMeL (DeepMind):** a provable defense, but it needs a DSL interpreter. That is 10+ hours. We take the idea (rival text never drives control flow), not the implementation.
- **Tit-for-tat as the core strategy:** mid-table in ANAC. Reciprocity survives only as a modifier.
- **Social proof:** no measurable effect on LLMs.
- **Threats and ultimatums:** least effective persuasion class, and The Art of the Deal ranked 198/199.
- **The "10× profit" OG-Narrator headline:** a base-rate artifact.
- **Scribo (Causa Prima's open-source repo):** it is e-invoicing, unrelated to negotiation.
- **Voss, by name:** two independent searches found no paper testing Voss tactics on LLMs. That is an absence of evidence, not evidence against. What transfers is in `02`.

## Unverified

- Prompt-injection success rates against recent Claude models in web browsing (claude.com blog, reported by an agent, not re-checked).
- The secondary A2A-NT rows (~9 pp budget effect, >10% budget breaches).
- That Causa Prima's two job posts are unpublished: Exa may serve a cache.

## Verification log

- **2026-10-01, Opus verifier, fresh context.** All 8 load-bearing numbers in Tiers 2-3 matched their sources, with nuances added above. It found 2 logic blockers in the first engine design, now fixed in `02`.
- **2026-10-01, second verifier (Opus, its own code and offer parser).**
  - Baseline, ranking and paper quotes: exact match.
  - Corrected after it ran: step size holds for buyers only; first-mover effect about a third of the size; the "never conceded" finding withdrawn as definitional; the Inject+Voss counter in `02` was wrong.
  - All of it is fixed above and in `02`.
- **2026-10-01, third pass (inline).**
  - §1c uses the dataset's own outcome columns, not a parser. The 18% "rival below its walk-away" figure was computed two ways and matches.
  - In Tier 1b, the Project Deal, Project Swap and Terms-Bench quotes were checked against the original pages.
