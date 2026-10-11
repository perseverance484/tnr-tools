#!/usr/bin/env bash
# Gate-enforcement self-test. Proves that a failed required evidence check
# makes execution fail at each layer. Exits 0 only when every probe failed as
# it must:
#   1. tools/check_evidence.py rejects a synthetic evidence file with failed:1;
#   2. tools/check_evidence.py rejects a missing gate file;
#   3. `bun test` on selftest/negative_gate.test.ts exits nonzero;
#   4. the evidence that run wrote is rejected by tools/check_evidence.py.
# Usage: selftest/run_negative.sh <engine-app-dir> <scratch-dir>
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
APP="$1"
TMP="$2"
rm -rf "$TMP" && mkdir -p "$TMP/synthetic" "$TMP/bun"
ok=0
expect_fail() { # <label> <status>
  if [[ "$2" -ne 0 ]]; then echo "negative probe $1: exit $2 (failed as required)"; else echo "negative probe $1: exit 0 (NOT ENFORCED)"; ok=1; fi
}

printf '%s\n' '{"gate":"SYN","assertions":2,"failed":1,"checks":[{"name":"ok","pass":true},{"name":"bad","pass":false}],"data":{}}' > "$TMP/synthetic/syn.json"
python3 "$HERE/tools/check_evidence.py" "$TMP/synthetic" SYN >/dev/null; expect_fail "synthetic failed:1 evidence" $?
python3 "$HERE/tools/check_evidence.py" "$TMP/synthetic" ABSENT >/dev/null; expect_fail "missing gate file" $?

SUITE="$APP/tests/tnr_ghost_ship_stage2_selftest"
rm -rf "$SUITE" && mkdir -p "$SUITE"
cp "$HERE/selftest/negative_gate.test.ts" "$SUITE/"
(cd "$APP" && TNR_OUT="$TMP/bun" unshare -rn bun test tests/tnr_ghost_ship_stage2_selftest >"$TMP/bun.log" 2>&1); expect_fail "bun test with a failed Evidence.check" $?
rm -rf "$SUITE"
python3 "$HERE/tools/check_evidence.py" "$TMP/bun" NEG >/dev/null; expect_fail "evidence written by the failing bun run" $?
exit $ok
