#!/usr/bin/env bash
# Ghost Ship / Skyglass Stage 2 offline harness runner.
#
#   harness/ghost_ship_stage2/run.sh            # M0 + every engine gate
#   harness/ghost_ship_stage2/run.sh a2         # M0 + only files matching "a2"
#
# Exit status is nonzero when M0 fails, when `bun test` fails, when any
# required evidence file is missing or records a failed check
# (tools/check_evidence.py), or when the gate-enforcement self-test
# (selftest/run_negative.sh) finds a layer that does not fail on a failed check.
#
# Engine source: studie-tech/TheNinjaRPG at the pinned commit, exported with
# `git archive` into a disposable work directory (never the upstream working
# tree). Dependencies come from the pinned bun.lock with lifecycle scripts
# disabled. Tests run inside a network namespace with no interfaces
# (`unshare -rn`), with the upstream CI fork-PR placeholder environment values
# (no credentials) and no database (TEST_MYSQL_URL unset).
#
# Environment:
#   TNR_ENGINE_SRC   existing clone of studie-tech/TheNinjaRPG (else cloned)
#   TNR_ENGINE_WORK  work directory (default: harness/ghost_ship_stage2/.work)
#   TNR_OUT          results directory (default: harness/ghost_ship_stage2/results)
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PIN="cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93"
UPSTREAM="https://github.com/studie-tech/TheNinjaRPG.git"
WORK="${TNR_ENGINE_WORK:-$HERE/.work}"
OUT="${TNR_OUT:-$HERE/results}"
FILTER="${1:-}"
ENGINE="$WORK/engine"
APP="$ENGINE/app"
SUITE="$APP/tests/tnr_ghost_ship_stage2"

mkdir -p "$WORK" "$OUT"

# 1. Pinned engine export.
if [[ ! -f "$ENGINE/PIN" ]]; then
  SRC="${TNR_ENGINE_SRC:-$WORK/src}"
  if [[ ! -d "$SRC/.git" ]]; then
    git clone --filter=blob:none --no-checkout "$UPSTREAM" "$SRC"
  fi
  git -C "$SRC" cat-file -e "$PIN^{commit}"
  rm -rf "$ENGINE" && mkdir -p "$ENGINE"
  git -C "$SRC" archive "$PIN" app | tar -x -C "$ENGINE"
  echo "$PIN" > "$ENGINE/PIN"
fi
[[ "$(cat "$ENGINE/PIN")" == "$PIN" ]] || { echo "engine export is not at $PIN" >&2; exit 2; }

# 2. Dependencies from the pinned lockfile, no lifecycle scripts.
if [[ ! -d "$APP/node_modules" ]]; then
  (cd "$APP" && bun install --frozen-lockfile --ignore-scripts)
fi

# 3. Install the harness suite into the disposable export.
rm -rf "$SUITE" && mkdir -p "$SUITE"
cp -R "$HERE/engine/." "$SUITE/"

# 4. M0 (repository-only, stdlib Python).
python3 "$HERE/m0_verify.py" --out "$OUT/m0.json"

# 5. Engine gates, socket-free.
export TNR_REPO="$REPO" TNR_OUT="$OUT"
export NODE_ENV=test
export NEXT_PUBLIC_BASE_URL=http://localhost:3000
export NEXT_PUBLIC_PUSHER_APP_KEY=test-key NEXT_PUBLIC_PUSHER_APP_CLUSTER=mt1
export PUSHER_APP_ID=test-app PUSHER_APP_SECRET=test-secret
export DATABASE_URL=http://127.0.0.1:1
export OPENAI_API_KEY=test-placeholder-not-a-real-key
unset TEST_MYSQL_URL TEST_MYSQL_ALLOW_DESTRUCTIVE
set +e
(cd "$APP" && unshare -rn bun test "tests/tnr_ghost_ship_stage2${FILTER:+/}${FILTER}" --timeout 600000) 2>&1 | tee "$OUT/bun_test${FILTER:+_$FILTER}.log"
BUN_STATUS=${PIPESTATUS[0]}

# 5b. Every required evidence file must exist and be clean.
case "$FILTER" in
  "") GATES="m0 a1 a2 b1 b2 b3 c1 c2 c3" ;;
  a1*) GATES="m0 a1" ;;
  a2*) GATES="m0 a2" ;;
  b*) GATES="m0 b1 b2 b3" ;;
  c*) GATES="m0 c1 c2 c3" ;;
  *) GATES="m0" ;;
esac
python3 "$HERE/tools/check_evidence.py" "$OUT" $GATES
EVIDENCE_STATUS=$?

# 5c. Gate-enforcement self-test (negative probes must fail).
"$HERE/selftest/run_negative.sh" "$APP" "$WORK/selftest"
NEGATIVE_STATUS=$?
set -e
STATUS=0
for s in "$BUN_STATUS" "$EVIDENCE_STATUS" "$NEGATIVE_STATUS"; do [[ "$s" -ne 0 ]] && STATUS=1; done
echo "run.sh: bun=$BUN_STATUS evidence=$EVIDENCE_STATUS negativeSelftest=$NEGATIVE_STATUS -> exit $STATUS"

# 6. Provenance.
python3 - "$OUT/provenance${FILTER:+_$FILTER}.json" "$APP" "$PIN" "$HERE" "$BUN_STATUS" "$EVIDENCE_STATUS" "$NEGATIVE_STATUS" <<'PY'
import hashlib, json, os, subprocess, sys
out, app, pin, here, status, evidence_status, negative_status = sys.argv[1:]
def sha(p):
    with open(p, "rb") as fh: return hashlib.sha256(fh.read()).hexdigest()
def run(*a):
    try: return subprocess.run(a, capture_output=True, text=True, check=True).stdout.strip()
    except Exception as e: return f"unavailable: {e}"
harness = {}
for sub in ("engine", "selftest", "tools"):
    for root, dirs, files in os.walk(os.path.join(here, sub)):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for f in sorted(files):
            p = os.path.join(root, f); harness[os.path.relpath(p, here)] = sha(p)
harness["m0_verify.py"] = sha(os.path.join(here, "m0_verify.py"))
harness["run.sh"] = sha(os.path.join(here, "run.sh"))
json.dump({
    "engine": {"repository": "studie-tech/TheNinjaRPG", "commit": pin, "export": "git archive <pin> app",
               "bunLockSha256": sha(os.path.join(app, "bun.lock")),
               "packageJsonSha256": sha(os.path.join(app, "package.json"))},
    "runtime": {"bun": run("bun", "--version"), "node": run("node", "--version"),
                "python": sys.version.split()[0], "uname": run("uname", "-sr")},
    "isolation": {"network": "unshare -rn (no interfaces)", "database": "none (TEST_MYSQL_URL unset)",
                  "env": "upstream test_build.yml fork-PR placeholders; no credentials"},
    "harnessFileSha256": harness, "bunTestExitStatus": int(status),
    "evidenceCheckExitStatus": int(evidence_status), "negativeSelftestExitStatus": int(negative_status),
}, open(out, "w"), indent=1)
PY
exit "$STATUS"
