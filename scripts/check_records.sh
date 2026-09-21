#!/bin/sh
# Mechanical check of the project's Perspicuity records.
#
# The checker ships with the Perspicuity skill rather than with the project, so it is looked up
# at run time. When it is absent the check is skipped loudly rather than silently passing: a
# skipped check and a passing check must not look the same.
#
# Usage: check_records.sh [project-root]
# With no argument the project root is this script's parent directory.
#
# The full dashboard is useful interactively and noise in CI, so this prints the summary and the
# mechanical findings, and dumps everything only when something fails.
set -eu

if [ "$#" -ge 1 ]; then
  ROOT="$(cd "$1" && pwd)"
else
  ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi

# The skill can be installed in more than one place, and the installation layout has changed
# between skill versions. Probe in order and take the first that carries the checker, so a
# renamed install directory shows up as a skip rather than as an unexplained pass.
if [ -n "${PERSPICUITY_CHECKER:-}" ]; then
  CHECKER="$PERSPICUITY_CHECKER"
else
  CHECKER=""
  for candidate in \
    "$HOME/.dsh/skills/perspicuity/scripts" \
    "$HOME/.codex/skills/perspicuity/scripts" \
    "$HOME/.claude/skills/perspicuity/scripts"
  do
    if [ -d "$candidate/perspicuity_dashboard" ]; then
      CHECKER="$candidate"
      break
    fi
  done
  CHECKER="${CHECKER:-$HOME/.dsh/skills/perspicuity/scripts}"
fi

if [ ! -d "$CHECKER/perspicuity_dashboard" ]; then
  echo "note: the Perspicuity checker was not found at $CHECKER."
  echo "      skipping the mechanical record check. Set PERSPICUITY_CHECKER to the"
  echo "      skill's scripts directory to enable it. This is a skip, not a pass."
  exit 0
fi

cd "$ROOT"

output="$(PYTHONPATH="$CHECKER" python3 -m perspicuity_dashboard.work --root . --source . --check 2>&1)" && status=0 || status=$?

printf '%s\n' "$output" | sed -n '/^markdown_files:/p'
printf '%s\n' "$output" | sed -n '/^## Mechanical checks/,$p'

if [ "$status" -ne 0 ]; then
  echo
  echo "--- full dashboard output follows ---" >&2
  printf '%s\n' "$output" >&2
  exit "$status"
fi
