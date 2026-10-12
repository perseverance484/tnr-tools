#!/usr/bin/env bash
# Final 2/2 item records + Crowned Captain support (RUL-2026-10-11-006/007/008).
# Versioned successor; never modifies the frozen r4 or 3/3 active-Consume harnesses.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PIN=585534d7eb21d6f0dd678d5c3eb92662f611d39b
WORK="${TNR_ENGINE_WORK:-$HERE/.work}"
OUT="${TNR_OUT:-$HERE/results}"
ENGINE="$WORK/engine"
APP="$ENGINE/app"
SUITE="$APP/tests/tnr_ghost_ship_final"
export TNR_OUT="$OUT"
mkdir -p "$WORK" "$OUT"
# Never leave a previous clean result available after a failed early preflight.
case "$(realpath "$OUT")/" in
  "$REPO/harness/ghost_ship_stage2/"*|"$REPO/harness/ghost_ship_consume/"*) echo "refusing historical output path" >&2; exit 2 ;;
esac
rm -f "$OUT"/{m0,contract,guards,active,crowned,provenance}.json "$OUT/bun_test.log" "$OUT/negative_selftest.log"
SRC="${TNR_ENGINE_SRC:?Set TNR_ENGINE_SRC to an existing upstream clone}"
git -C "$SRC" cat-file -e "$PIN^{commit}"
if [[ ! -f "$ENGINE/PIN" ]]; then
  [[ ! -e "$ENGINE" ]] || { echo "unmarked export exists; choose a fresh work directory" >&2; exit 2; }
  mkdir -p "$ENGINE"
  git -C "$SRC" archive "$PIN" app | tar -x -C "$ENGINE"
  printf '%s\n' "$PIN" > "$ENGINE/PIN"
fi
[[ "$(cat "$ENGINE/PIN")" == "$PIN" ]] || { echo "wrong engine pin" >&2; exit 2; }
python3 "$HERE/tools/verify_export.py" "$SRC" "$PIN" "$ENGINE"

# Reuse only an install backed by byte-identical dependency manifests. No install/network.
DEPS="${TNR_DEPENDENCIES_APP:?Set TNR_DEPENDENCIES_APP to the approved installed app export}"
cmp "$APP/bun.lock" "$DEPS/bun.lock"
cmp "$APP/package.json" "$DEPS/package.json"
[[ -d "$DEPS/node_modules" ]] || { echo "missing dependencies" >&2; exit 2; }
if [[ ! -d "$APP/node_modules" ]]; then
  ln -s "$(realpath "$DEPS/node_modules")" "$APP/node_modules"
fi
[[ "$(realpath "$APP/node_modules")" == "$(realpath "$DEPS/node_modules")" ]] || {
  echo "engine node_modules does not resolve to the declared approved install" >&2; exit 2;
}

# Isolation is tested before importing any engine module. Missing infrastructure is fatal.
"$HERE/tools/test_env.sh" python3 -c 'import errno,socket
for family in (socket.AF_INET,socket.AF_INET6,socket.AF_UNIX):
 try: socket.socket(family,socket.SOCK_STREAM)
 except OSError as e: assert e.errno==errno.EPERM
 else: raise AssertionError("socket creation allowed")
print("offline socket-denial preflight: PASS")'

rm -rf "$SUITE"
mkdir -p "$SUITE"
cp -R "$HERE/engine/." "$SUITE/"
python3 "$HERE/tools/build_final_items.py" --check
python3 "$REPO/harness/ghost_ship_consume/tools/build_item_carriers.py" --check
python3 "$REPO/harness/ghost_ship_stage2/m0_verify.py" --out "$OUT/m0.json"
rm -f "$OUT/contract.json" "$OUT/guards.json" "$OUT/active.json" "$OUT/crowned.json"
set +e
(cd "$APP" && "$HERE/tools/test_env.sh" bun test ./tests/tnr_ghost_ship_final/ --timeout 600000) >"$OUT/bun_test.log" 2>&1
BUN_STATUS=$?
cat "$OUT/bun_test.log"
python3 "$HERE/tools/check_evidence.py" "$OUT" M0 CONTRACT GUARDS ACTIVE CROWNED
EVIDENCE_STATUS=$?
"$HERE/tools/test_env.sh" bash "$HERE/selftest/run_negative.sh" "$APP" "$WORK/selftest" >"$OUT/negative_selftest.log" 2>&1
NEGATIVE_STATUS=$?
cat "$OUT/negative_selftest.log"
python3 "$HERE/tools/verify_export.py" "$SRC" "$PIN" "$ENGINE"
SOURCE_STATUS=$?
set -e
python3 "$HERE/tools/provenance.py" "$OUT" "$APP" "$BUN_STATUS" "$EVIDENCE_STATUS" "$NEGATIVE_STATUS" "$SOURCE_STATUS"
STATUS=0
for s in "$BUN_STATUS" "$EVIDENCE_STATUS" "$NEGATIVE_STATUS" "$SOURCE_STATUS"; do
  [[ "$s" -ne 0 ]] && STATUS=1
done
echo "run.sh: bun=$BUN_STATUS evidence=$EVIDENCE_STATUS negativeSelftest=$NEGATIVE_STATUS source=$SOURCE_STATUS -> exit $STATUS"
exit "$STATUS"
