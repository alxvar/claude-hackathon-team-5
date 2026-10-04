# agents/ · the processes that act in the game

| Folder | What | Writes to the game? |
|---|---|---|
| `duelist/` | The duel agent. On Sunday: code decides accept / hold / step / delivery day, Claude Haiku 4.5 writes the words, guards, 8 s failover, hot-reloaded params. **The Sunday version is branch `duelist-loop` @ f57a002 (tag `sunday-final-duelist`)**; main holds the earlier version. How it was tested: `docs/duelist-sunday-summary.md` | yes (duels) |
| `trader/` | `loop.py` (taker: accepts other teams' offers), `book.py` (maker book), `swaps.py` (card-for-card), `trade.py` (one manual trade) | yes, started by the Operator |
| `dealers/` | `abuela_bot.py`, `chato_steady.py`: negotiated dealer deals with a trick guard and cash floors; `narrator.py` writes their text | yes, started by the Operator |
| `analyst/` | `analyst.py --role scout|judge|strategist`: the analysts on the Claude API; outputs in `intel/scout.md`, `judge.md`, `strategy.md` | no |
| `negotiator/` | A general negotiator agent, built and tested but never wired into the live game | no |

Rules for every writer: one owner per job, limits in `intel/directives.md`, counterparty rules in `tools/policy.py`. See the root `README.md` for the architecture.
