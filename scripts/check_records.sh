#!/bin/sh
# Mechanical check of the project's Perspicuity records.
#
# The checker ships with the Perspicuity skill rather than with the project, so it is looked up
# at run time from a list of known locations. Set PERSPICUITY_CHECKER to override.
#
# When the checker is absent the check is skipped LOUDLY and exits 0, saying that it skipped.
# A skipped check and a passing check must not look the same. Set
# ELIGIBILITY_RECORDS_REQUIRED=1 to make a missing checker a hard failure instead.
#
# Usage: check_records.sh [project-root]
# With no argument the project root is this script's parent directory.
set -eu

if [ "$#" -ge 1 ]; then
  ROOT="$(cd "$1" && pwd)"
else
  ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi

find_checker() {
  if [ -n "${PERSPICUITY_CHECKER:-}" ]; then
    printf '%s\n' "$PERSPICUITY_CHECKER"
    return 0
  fi
  for candidate in \
    "$HOME/.dsh/skills/perspicuity/scripts" \
    "$HOME/.codex/skills/perspicuity/scripts" \
    "$HOME/.claude/skills/perspicuity/scripts"
  do
    if [ -d "$candidate/perspicuity_dashboard" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

if ! CHECKER="$(find_checker)"; then
  echo "note: the Perspicuity checker was not found in any known location."
  echo "      Looked in PERSPICUITY_CHECKER, ~/.dsh/skills/perspicuity/scripts,"
  echo "      ~/.codex/skills/perspicuity/scripts, ~/.claude/skills/perspicuity/scripts."
  if [ "${ELIGIBILITY_RECORDS_REQUIRED:-0}" = "1" ]; then
    echo "error: ELIGIBILITY_RECORDS_REQUIRED=1 and the checker is missing." >&2
    exit 1
  fi
  echo "      SKIPPED, not passed. Set PERSPICUITY_CHECKER to the skill's scripts"
  echo "      directory to enable it."
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
