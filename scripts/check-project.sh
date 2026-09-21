#!/bin/sh
# Project-specific checks.
#
# Everything that must be true before a commit belongs here: the test suite, the linter, the
# build, link checks, the site's own rules. `make ci` runs this after the record check, so a
# failure here fails the build.
#
# It is deliberately empty at setup. That is a gap, not a pass: until there is code, this script
# establishes nothing, and a green check that establishes nothing is worse than no check.
set -eu

cd "$(dirname "$0")/.."

echo "note: no project checks are defined yet."
echo "      Replace this script with the real ones as soon as there is code to check."
