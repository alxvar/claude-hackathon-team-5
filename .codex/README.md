# Codex team-sync hooks

The installed hooks reuse `tools/team_sync.sh` with the same events as
`.claude/settings.json`:

- `SessionStart`: pull teammate updates (30-second timeout).
- `UserPromptSubmit`: pull before each prompt (30-second timeout).
- `Stop`: commit and push when a turn finishes (60-second timeout).

The adapter resolves the project root from its own location and supplies
`CLAUDE_PROJECT_DIR` for the shared script. Pull output becomes session context;
push diagnostics go to stderr and the Stop hook returns `{}` on stdout.
The shared script's pause and work-in-progress checks still apply.

Start or resume Codex in this trusted repository, then use `/hooks` in the CLI
to review and trust these hooks. Codex skips new or changed hook definitions
until they are trusted. Hooks are enabled by default.

`AGENTS.md` points Codex to `CLAUDE.md`, so both agents use the same project
instructions. Edit `CLAUDE.md` to update those shared instructions.

Reference: [OpenAI hook documentation](https://learn.chatgpt.com/docs/hooks).
