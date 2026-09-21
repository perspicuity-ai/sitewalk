#!/bin/sh
# Project-specific checks.
#
# Everything that must be true before a commit belongs here. `make ci` runs this after the
# record check, so a failure here fails the build.
#
# This script must be able to fail. A check that cannot fail establishes nothing, and a green
# `make ci` that verified nothing is worse than no check at all, because it is believed. The
# suite below runs with the network unavailable: `tests/fakes.py` replaces `socket.socket` and
# `socket.getaddrinfo` with functions that raise, so an accidental request fails the suite
# rather than passing on a connected machine.
#
# Two pipeline traps are avoided below, because both were hit here while writing this:
#   * `cmd | tail` reports tail's status, not cmd's, so a failing suite would vanish. The suite
#     writes to a file and the status is read from that command instead.
#   * `cmd || true` would hide a failure outright.
set -eu

cd "$(dirname "$0")/.."

echo "== byte-compile the package =="
python3 -m compileall -q sitewalk
echo "   ok: sitewalk/ compiles"

echo
echo "== the test suite, with no network =="
suite_log="$(mktemp)"
trap 'rm -f "$suite_log"' EXIT
if ! python3 -m unittest discover -s tests -t . >"$suite_log" 2>&1; then
  echo "error: the test suite failed. Full output:" >&2
  cat "$suite_log" >&2
  exit 1
fi
tail -n 3 "$suite_log"

echo
echo "== the tool answers for itself =="
# A smoke check through the real entry point, on fixtures, with no network. It proves the
# package runs as `python3 -m sitewalk` rather than only as an imported library, and that the
# exit codes a CI gate depends on are the ones the command line actually produces.
if ! python3 -m sitewalk --dir tests/fixtures/bare-site >/dev/null 2>&1; then
  echo "error: 'python3 -m sitewalk --dir tests/fixtures/bare-site' did not exit 0" >&2
  exit 1
fi
if python3 -m sitewalk --dir tests/fixtures/bare-site --strict >/dev/null 2>&1; then
  echo "error: --strict exited 0 on a fixture that carries an error finding" >&2
  exit 1
fi
echo "   ok: runs as a module, and --strict gates"

echo
echo "== the claim boundary is still in the output =="
# The product's central constraint, checked mechanically rather than trusted. If a later change
# drops the boundary from the report, this fails and says which phrase went missing.
output="$(python3 -m sitewalk --dir tests/fixtures/bare-site 2>/dev/null)"
for phrase in "does not execute JavaScript" "not measured here"; do
  case "$output" in
    *"$phrase"*) ;;
    *)
      echo "error: the report no longer states '$phrase'" >&2
      exit 1
      ;;
  esac
done
echo "   ok: the report states the no-JavaScript limit and what it does not measure"

echo
echo "project checks passed"
