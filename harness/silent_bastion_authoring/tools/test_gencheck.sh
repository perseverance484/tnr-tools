#!/usr/bin/env bash
# Negative tests for run_generator_checks (review F2): a failure or STALE report in the first, middle
# or last of five checks must fail the gate; five passing checks must pass it. No game, no repo writes.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=gencheck.sh
source "$HERE/gencheck.sh"
OK="echo current"; FAIL="python3 -c 'raise SystemExit(\"compose: script ids differ from graph\")'"; STALE="echo 'compiled/: STALE [x]'"
fails=0
expect() { # expect <want-status> <label> CMD...
  local want=$1 label=$2; shift 2
  run_generator_checks "$@" >/dev/null 2>&1; local got=$?
  if [[ $got -eq $want ]]; then echo "ok   $label (status $got)"; else echo "FAIL $label (want $want, got $got)"; fails=$((fails + 1)); fi
}
expect 0 "all five current"            "$OK" "$OK" "$OK" "$OK" "$OK"
expect 1 "first check exits nonzero"   "$FAIL" "$OK" "$OK" "$OK" "$OK"
expect 1 "middle check exits nonzero"  "$OK" "$OK" "$FAIL" "$OK" "$OK"
expect 1 "last check exits nonzero"    "$OK" "$OK" "$OK" "$OK" "$FAIL"
expect 1 "first check reports STALE"   "$STALE" "$OK" "$OK" "$OK" "$OK"
expect 1 "middle check reports STALE"  "$OK" "$OK" "$STALE" "$OK" "$OK"
expect 1 "last check reports STALE"    "$OK" "$OK" "$OK" "$OK" "$STALE"
# Every command still runs after an early failure (full log).
log="$(run_generator_checks "$FAIL" "echo second-ran" "echo third-ran" 2>&1)"
if grep -q second-ran <<<"$log" && grep -q third-ran <<<"$log"; then echo "ok   later checks still run after a failure"; else echo "FAIL later checks skipped"; fails=$((fails + 1)); fi
echo "test_gencheck: $fails failed"
exit $((fails > 0))
