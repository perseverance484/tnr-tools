#!/usr/bin/env bash
# Gate-enforcement self-test. Proves that a failed required evidence check
# makes execution fail at each layer, and that each failure is the intended
# one rather than a launch or infrastructure error.
#   1. tools/check_evidence.py rejects a synthetic evidence file with failed:1;
#   2. tools/check_evidence.py rejects a missing gate file;
#   3. `bun test` on selftest/negative_gate.test.ts exits nonzero, its log shows
#      exactly 1 pass / 1 fail with the requireClean test failing on
#      "deliberate failure", and it wrote NEG evidence with 2 checks, 1 failed;
#   4. tools/check_evidence.py rejects that NEG evidence;
#   5. `bun test` on selftest/negative_flush_only.test.ts (no requireClean, no
#      TNR_OUT) exits nonzero although its log shows 1 pass / 0 fail.
# Exit: 0 every layer enforced; 1 a layer did not fail as required;
#       2 infrastructure (missing tool, launch failure, missing artifact).
# Usage: selftest/run_negative.sh <engine-app-dir> <scratch-dir>
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
APP="$1"
TMP="$2"
rm -rf "$TMP" && mkdir -p "$TMP/synthetic" "$TMP/bun"
status=0
infra() { echo "negative self-test INFRASTRUCTURE: $1" >&2; status=2; }
result() { # <label> <enforced: 0|1>
  if [[ "$2" -eq 0 ]]; then echo "negative probe $1: enforced"; else echo "negative probe $1: NOT ENFORCED"; [[ $status -eq 0 ]] && status=1; fi
}

for tool in python3 bun; do command -v "$tool" >/dev/null || infra "$tool not found"; done
unshare -rn true 2>/dev/null || infra "unshare -rn unavailable"
[[ $status -eq 2 ]] && exit 2

printf '%s\n' '{"gate":"SYN","assertions":2,"failed":1,"checks":[{"name":"ok","pass":true},{"name":"bad","pass":false}],"data":{}}' > "$TMP/synthetic/syn.json"
out=$(python3 "$HERE/tools/check_evidence.py" "$TMP/synthetic" SYN); s=$?
[[ $s -eq 1 && "$out" == *"FAIL - 1 failed: bad"* ]]; result "synthetic failed:1 evidence (exit $s)" $?
out=$(python3 "$HERE/tools/check_evidence.py" "$TMP/synthetic" ABSENT); s=$?
[[ $s -eq 1 && "$out" == *"FAIL - missing"* ]]; result "missing gate file (exit $s)" $?

SUITE="$APP/tests/tnr_ghost_ship_stage2_selftest"
run_bun() { # <test file> <log> [TNR_OUT]
  rm -rf "$SUITE" && mkdir -p "$SUITE" && cp "$HERE/selftest/$1" "$SUITE/"
  local s
  if [[ -n "${3:-}" ]]; then
    (cd "$APP" && TNR_OUT="$3" unshare -rn bun test "tests/tnr_ghost_ship_stage2_selftest/$1" >"$2" 2>&1); s=$?
  else
    (cd "$APP" && env -u TNR_OUT unshare -rn bun test "tests/tnr_ghost_ship_stage2_selftest/$1" >"$2" 2>&1); s=$?
  fi
  rm -rf "$SUITE"
  return $s
}

run_bun negative_gate.test.ts "$TMP/bun.log" "$TMP/bun"; s=$?
if grep -q "(fail) evidence: no failed required checks (NEG)" "$TMP/bun.log" && grep -q '"deliberate failure"' "$TMP/bun.log" \
   && grep -Eq '^ *1 pass' "$TMP/bun.log" && grep -Eq '^ *1 fail' "$TMP/bun.log"; then
  [[ $s -ne 0 ]]; result "bun test with a failed Evidence.check (exit $s)" $?
else
  infra "negative_gate.test.ts did not run as intended (exit $s); see $TMP/bun.log"
fi
if python3 - "$TMP/bun/neg.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
bad = [c["name"] for c in d["checks"] if not c["pass"]]
sys.exit(0 if d["assertions"] == 2 and d["failed"] == 1 and bad == ["deliberate failure"] else 1)
PY
then
  out=$(python3 "$HERE/tools/check_evidence.py" "$TMP/bun" NEG); s=$?
  [[ $s -eq 1 && "$out" == *"deliberate failure"* ]]; result "evidence written by the failing bun run (exit $s)" $?
else
  infra "NEG evidence missing or not the expected 2 checks / 1 named failure"
fi

run_bun negative_flush_only.test.ts "$TMP/bun_flush.log"; s=$?
if grep -Eq '^ *1 pass' "$TMP/bun_flush.log" && grep -Eq '^ *0 fail' "$TMP/bun_flush.log"; then
  [[ $s -ne 0 ]]; result "flush-only failed check, no requireClean, no TNR_OUT (exit $s)" $?
else
  infra "negative_flush_only.test.ts did not run as intended (exit $s); see $TMP/bun_flush.log"
fi
exit $status
