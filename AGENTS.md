# Shared project instructions

Read and follow `CLAUDE.md` before working in this repository. It is the shared
source of project instructions for Codex and Claude Code; follow its referenced
plans and role-specific instructions when they apply to the task.

Codex's team-sync hooks in `.codex/hooks.json` mirror `.claude/settings.json` and
reuse `tools/team_sync.sh`: pull on session start and before each user prompt,
then commit and push when a turn finishes, with the shared script's pause and
work-in-progress checks.
