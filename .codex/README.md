# Codex team-sync hooks

The installed hooks reuse `tools/team_sync.sh` with the same pull events as
`.claude/settings.json`:

- `SessionStart`: pull teammate updates (30-second timeout).
- `UserPromptSubmit`: pull before each prompt (30-second timeout).

The adapter resolves the project root from its own location and supplies
`CLAUDE_PROJECT_DIR` for the shared script. Pull output becomes session context.
The shared script's pause and work-in-progress checks still apply.

Start or resume Codex in this trusted repository, then use `/hooks` in the CLI
to review and trust these hooks. Codex skips new or changed hook definitions
until they are trusted. Hooks are enabled by default.

The matching `Stop` hook is pending explicit approval: it would run the shared
script's `push` mode after every turn with a 60-second timeout, automatically
committing changes and pushing to `origin` (`alxvar/claude-hackathon-team-5`,
branch `main`). Its adapter must send sync diagnostics to stderr and return
`{}` on stdout to satisfy Codex's Stop output contract.

Reference: [OpenAI hook documentation](https://learn.chatgpt.com/docs/hooks).
