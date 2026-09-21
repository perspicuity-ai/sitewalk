#!/bin/sh
# The single check command. Run locally as `make ci`.
set -eu

cd "$(dirname "$0")/.."

echo "== Perspicuity records =="
./scripts/check_records.sh

if [ -x scripts/check-project.sh ]; then
  echo
  echo "== project checks =="
  ./scripts/check-project.sh
else
  echo
  echo "error: scripts/check-project.sh is missing or not executable." >&2
  echo "       Nothing beyond the record check is running." >&2
  exit 1
fi

echo
echo "ci passed"
