# Saturday sessions: what to open, with which prompt, model and effort

Open one VS Code window on the repo folder (File → Open Folder → `claude-hackathon-team-5`) so the explorer, the Git
panel and every terminal live in the repo. Close Friday's sessions first: only ONE operator may exist.

## Lucas's machine (start all three at 08:45)

| # | Session | Model / effort | Writes to the game? |
|---|---|---|---|
| 1 | Operator | Opus 5.5, high | **Yes, the only one** |
| 2 | Strategy (Lucas talks here) | Opus 5.5 xhigh; Fable 5.1 max only for a one-off deep question | No |
| 3 | Builder | Opus 5.5, high | No (code + daemons) |

**1. Operator — first prompt:**
> You are Team 5's operator. Read intel/ORCHESTRATOR.md and intel/saturday-plan.md, then start. Run the plan's §2 decision
> tree before anything else; the trader and the analysts are stopped on purpose until then.

**2. Strategy — first prompt:**
> You are Team 5's strategy session. I'm Lucas; reply in the language I write in. Read intel/saturday-plan.md, intel/GAME.md
> and the top of team/lucas.md. You never write to the game or start/stop daemons. When we decide something, write it to
> intel/directives.md as `- HH:MM · decision with limits · why` (add GUARDRAIL when it changes a hard limit), and for
> anything urgent also SendMessage the operator session (find it with ListAgents). Challenge my reasoning; label claims
> [V]/[L]/[?]; run an independent verification agent before any directive that moves > 20 P or changes a rule.

**3. Builder — first prompt:**
> You are Team 5's builder. Read intel/saturday-plan.md §5 and §6b and CLAUDE.md. Build in this order, each with a test and
> a small commit, never touching game write endpoints: (1) before 09:00: operator PID lock, API spend preflight, the
> Market Test recorder (and the auto-clone broker if intel/directives.md says option A); (2) by 10:00: the
> intel/sellable.md generator (§6b); (3) during Duels I: the repricer daemon, the accept arbiter (with Aleks), keyless reads
> for read-only daemons, the SSE watcher, per-settlement attribution in metrics, analyst premise timestamps. Register every
> daemon in tools/daemons.sh. Log each step in team/lucas.md.

## Aleks's laptop
> You are Aleks's Claude Code for Team 5. Read PLAN.md "RIGHT NOW" (Aleks) and intel/saturday-plan.md §4D. Implement the
> duelist fixes with regression tests on docs/duels/ before Duels I; then the Duels II `days` prep. Keep team/aleks.md current.

## Dani's laptop
> You are Dani's Claude Code for Team 5. Read PLAN.md "RIGHT NOW" (Dani) and intel/saturday-plan.md §3 and §6b. Help me run
> the organisers' desk questions, then add a panel to dashboard/ that git-pulls every 60 s and shows intel/sellable.md with
> new lines highlighted. Keep team/dani.md current.

## API credits ($100 each; Friday used ~$2 in total)
Credits are not the constraint; correctness and attention are. Before 09:00 each of us checks the key's spend limit
(Console → Settings → Billing → Spend limits; Lucas's was $1 on Friday). Worth spending on:
- the duelist's Opus strategist for every Saturday duel (30 s ticks allow it): Aleks's key, ~$2-4;
- judge and strategist run on events (round start, bench result, new level) plus every 15 min: Lucas's key, ~$2/h;
- nothing else needs an LLM: page gaps, repricing, the broker and the arbiter are deterministic code.
