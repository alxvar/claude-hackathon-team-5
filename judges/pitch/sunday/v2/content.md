# v2 content · 3 slides · 3 minutes (single source for every style variant)

Every number here is verified ([V] file). Do not add claims. English on the slides.

## Header facts (any slide that shows the result)
- Final: **#1 · 37.73**, 1.97 ahead of Team 10 (35.76) [V data/leaderboard.jsonl tick 2802]
- Saturday's close: **#3, 7.09 behind** Team 10 [V tick 1440]
- #1 at every snapshot from Sunday 12:35 to the close [V]

## Slide 1 · Q1 "How did you approach the challenge?" · 50 s
Title: **Adapt faster than the game changes**
Idea: two parts. (A) How we worked for three days: LEARN → DECIDE → ACT, over and over. (B) What made that possible: all the context connected in real time, so every decision was made on live numbers. Adaptation and reacting quickly were the key; you can't react quickly without real-time context.
- LEARN: rules, the organisers' changes, our own measurements → `GAME.md` (measured facts)
- DECIDE: humans + the Chief of staff → `directives.md`: **100 logged decisions, 24 guardrails** in 38 h [V intel/directives.md]
- ACT: the Operator and the Duelist trade; read-only watchers measure the result
- REAL-TIME CONTEXT (the base under all three): feed, scores, duels, market, rivals, news → **35,767 public events captured** [V team/aleks.md Sun 12:34], **42,791 data rows** [V data/*.jsonl], STATUS every 5 min, phone alerts
- ADAPTATION evidence (pick 2-3): the tick went **60 s → 30 s → 15 s** [V RULES]; we **redesigned overnight, twice** (Fri night: the Saturday plan; Sat night: the code-first duelist) [V team/lucas.md Sat 22:30-22:48, intel/saturday-plan.md]; result: **#3 at Saturday's close → #1** at the end.
- No "first idea: let the LLM negotiate" panel. No bottom sync strip.

## Slide 2 · Q2 + Q3 "What did you build? Why that way?" · 100 s (the main slide, show complexity simply)
Title: **Who decides, who acts, who checks**
Groups (one colour each):
- DECIDE: Lucas (goals + hard limits) · Aleks (wrote the duelist + hub) · Dani (the room, rivals, dashboard) → **Chief of staff** (Claude Code: makes the big calls, logs them with evidence, never writes to the game)
- ACT · two writer roles:
  - **Operator** (Claude Code, the only trade writer) + its bots: trader (taker) · book (maker) · dealer bots · page closers · counterparty policy
  - **Duelist**: code decides accept / hold / step / day, Claude Haiku 4.5 writes the words · guards · 8 s failover · **27 hot-reloaded tunables** [V docs/duelist-sunday-summary.md] · C → A safety switch · tested on a **5-world simulator** validated on Duels II [V intel/duel-lab.md]
- SENSE · CHECK (read-only): Market session (venue v10 at 0 % + Market Test recorder) · collector + status · reactor (live event stream) · Dani's dashboard + Neon hub · Analysts (scout + judge on the Claude API) · Duel Lab · verifier subagents + contrarian reviews
- HUMANS IN THE LOOP: **phone alerts (ntfy)** from the reactor and the opportunity finder to Lucas and Dani → they walk to the team in the room when a deal fits our market [V tools/notify.py, judges/demo.md]
- The game API at the bottom: writes = offers · accepts · threads · duels; reads = me · clock · board · event stream; one key, 5 req/s, 1 accept per tick.
- Arrows: solid = authority / a write to the game; dashed = data.
- Optional real screenshot: img/dashboard.png (Dani's live dashboard, 14:26).
Reveal: decide → act → sense/check + phones → the three decisions:
1. **Code decides, the LLM writes.** Price, day and accept are code; Haiku writes the words in ≈ 2 s vs 9.4 s when the LLM decided [V]. Guards in code. Because a 15 s tick doesn't wait.
2. **2 writers · 1 orchestrator · 14 watchers.** Two roles act, one Chief decides, fourteen read-only daemons sense; every hard limit is a written GUARDRAIL line [V tools/daemons.sh, directives].
3. **Redesigned every night, pressure-tested.** Each night we rebuilt on the day's data: Saturday night the duelist went code-first (**547 tests green**) and was checked on the simulator; Sunday 07:25 contrarian reviews of CHA, duels and market fixed the plan; verifier agents re-checked every claim; **163 tests** guard the bots [V team/lucas.md Sat 22:48, Sun 11:33; directives 07:25].

## Slide 3 · Q4 "What did you learn?" · 30 s (from the team's voice memo)
Title: **What we learned**
- **Technical · real-time shared context is everything.** Day one, three people and their agents worked in silos; by Sunday every agent saw every update as it happened. (Lucas, Aleks)
- **Negotiation · time can beat price.** A fast good deal beats a slow perfect one; and people still decide: alliances made in the room outweighed agent tactics. (Aleks, Lucas)
- **Marketplace · trust moves trades, not fees.** Zero commission wasn't enough; trust and returned favours brought trades to our market. Incentives can break. (Dani, Aleks)
Close: **Three humans set the limits. Claude ran the bazaar, and checked itself.**

## Timing (3:00)
Slide 1 0:00-0:50 · Slide 2 0:50-2:30 (4 reveal steps ≈ 25 s each) · Slide 3 2:30-3:00.
