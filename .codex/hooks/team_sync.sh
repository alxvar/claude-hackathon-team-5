#!/usr/bin/env bash
# Resolve the project independently of Codex's current subdirectory.
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)" || exit 0
export CLAUDE_PROJECT_DIR="$project_dir"

case "${1:-}" in
  pull)
    # SessionStart and UserPromptSubmit accept plain-text context.
    exec bash "$project_dir/tools/team_sync.sh" pull
    ;;
  *)
    echo "Usage: team_sync.sh pull" >&2
    exit 1
    ;;
esac
