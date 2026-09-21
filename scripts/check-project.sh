#!/bin/sh
# Project-specific checks.
#
# Everything that must be true before a commit belongs here: the test suite, the linter, the
# build, link checks. `make ci` runs this after the record check, so a failure here fails the
# build.
#
# THIS STUB DELIBERATELY FAILS. It used to print a note and exit 0, which meant a project could
# have failing tests and a green `make ci` at the same time. A check that establishes nothing is
# worse than no check, because it is believed. Replace the body with the real checks.
set -eu

cd "$(dirname "$0")/.."

echo "error: no project checks are defined." >&2
echo "       scripts/check-project.sh is still the template stub, so 'make ci' would" >&2
echo "       report success without verifying anything." >&2
echo "" >&2
echo "       Replace the body with the real checks -- at minimum the test suite -- and" >&2
echo "       run 'make ci' again. If there is genuinely nothing to check yet, make this" >&2
echo "       script say so and exit 0 deliberately, in a sentence a reader can judge." >&2
exit 1
