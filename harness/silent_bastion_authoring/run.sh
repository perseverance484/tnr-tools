#!/usr/bin/env bash
# Silent Bastion complete authoring — offline native validation of the authored package.
#
#   harness/silent_bastion_authoring/run.sh           # generators --check, preflight, gates A, C, and C99 D/R/E on the compiled quest
#   harness/silent_bastion_authoring/run.sh ai        # one gate (ai|content)
#
# Package: state/silent_bastion_authoring/ (design → tools/compose.py → compiled/). Isolation matches
# harness/silent_bastion_condensed99/run.sh: git-archive export of the pinned engine, frozen lockfile
# without lifecycle scripts, socket-only throwaway MySQL (--network none), tests inside `unshare -rn`,
# placeholder environment, no credentials. No engine file is modified; nothing touches push/.
#
# Environment (optional): TNR_ENGINE_SRC, TNR_ENGINE_WORK (default .work/), TNR_OUT (default results/), TNR_KEEP_DB=1.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
P1="$REPO/harness/silent_bastion_phase1"
C99="$REPO/harness/silent_bastion_condensed99"
PKG="$REPO/state/silent_bastion_authoring"
PIN="0651b039a466516a8fe24fc13b56f60dea11b7eb"
UPSTREAM="https://github.com/studie-tech/TheNinjaRPG.git"
MYSQL_IMAGE="mysql:26.7.0@sha256:893418c8a7a34c60d2d961cc30ef136095da141478562ed2101ae3f5faba9c3f"
CONTAINER="tnr-sb-authoring-mysql"
GRAPH="harness/silent_bastion_condensed99/graphs/alt99_f4gate.json"
COMPILED="state/silent_bastion_authoring/compiled/quest.candidate.json"
WORK="${TNR_ENGINE_WORK:-$HERE/.work}"
OUT="${TNR_OUT:-$HERE/results}"
FILTER="${1:-}"
ENGINE="$WORK/engine"
APP="$ENGINE/app"
SUITE="tests/tnr_sb_authoring"
RUNTIME="tests/tnr_sb_compiled_runtime"
SOCKDIR="$WORK/mysqld"

mkdir -p "$WORK" "$OUT"

# 1. Pinned engine export + dependencies.
if [[ ! -f "$ENGINE/PIN" ]]; then
  SRC="${TNR_ENGINE_SRC:-$WORK/src}"
  [[ -d "$SRC/.git" ]] || git clone --filter=blob:none --no-checkout "$UPSTREAM" "$SRC"
  git -C "$SRC" cat-file -e "$PIN^{commit}"
  rm -rf "${ENGINE:?}" && mkdir -p "$ENGINE"
  git -C "$SRC" archive "$PIN" app | tar -x -C "$ENGINE"
  echo "$PIN" > "$ENGINE/PIN"
fi
[[ "$(cat "$ENGINE/PIN")" == "$PIN" ]] || { echo "engine export is not at $PIN" >&2; exit 2; }
[[ -d "$APP/node_modules" ]] || (cd "$APP" && bun install --frozen-lockfile --ignore-scripts)

# 2. Generators must be current (deterministic package).
set +e
GEN_STATUS=0
{
  python3 "$PKG/tools/extract_sources.py" --engine "$APP" --check
  python3 "$PKG/tools/gen_regulars.py" --check
  python3 "$PKG/tools/gen_script.py" --check
  python3 "$PKG/tools/compose.py" --check
  python3 "$C99/tools/derive_alternatives.py" --check
} > "$OUT/generators_check.log" 2>&1 || GEN_STATUS=1
grep -q "STALE" "$OUT/generators_check.log" && GEN_STATUS=1
cat "$OUT/generators_check.log"
# 2b. Repository validator on the composer's validation-only manifest: errors must be exactly the documented set.
python3 "$HERE/tools/check_validate.py" "$OUT"
VALIDATE_STATUS=$?
set -e

# 3. Install suites.
for S in "$SUITE" "$RUNTIME"; do rm -rf "${APP:?}/${S:?}" && mkdir -p "$APP/$S/lib"; done
cp "$P1/engine/lib/graph.ts" "$P1/engine/lib/driver.ts" "$P1/engine/lib/report.ts" "$C99/engine/lib/run99.ts" "$HERE/engine/lib/units.ts" "$APP/$SUITE/lib/"
cp "$HERE/engine/"*.test.ts "$APP/$SUITE/"
cp "$P1/engine/lib/graph.ts" "$P1/engine/lib/driver.ts" "$P1/engine/lib/report.ts" "$C99/engine/lib/run99.ts" "$APP/$RUNTIME/lib/"
cp "$C99/engine/c99_defect.test.ts" "$C99/engine/c99_runtime.test.ts" "$C99/engine/c99_edges.test.ts" "$APP/$RUNTIME/"

# 4. Throwaway MySQL, socket only.
if ! docker info >/dev/null 2>&1; then echo "docker daemon not reachable; start it (e.g. 'dockerd &') and rerun" >&2; exit 2; fi
mkdir -p "$SOCKDIR" && chmod 777 "$SOCKDIR"
if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
  rm -f "${SOCKDIR:?}"/*
  docker run -d --name "$CONTAINER" --network none -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -e MYSQL_DATABASE=tnr_test \
    -v "$SOCKDIR:/var/run/mysqld" "$MYSQL_IMAGE" >/dev/null
fi
cleanup() { [[ "${TNR_KEEP_DB:-0}" == "1" ]] || docker rm -f "$CONTAINER" >/dev/null 2>&1 || true; }
trap cleanup EXIT
for _ in $(seq 1 120); do
  docker exec "$CONTAINER" mysql -uroot --socket=/var/run/mysqld/mysqld.sock -e "SELECT 1" tnr_test >/dev/null 2>&1 && break
  sleep 2
done
docker exec "$CONTAINER" mysql -uroot --socket=/var/run/mysqld/mysqld.sock -e "SELECT 1" tnr_test >/dev/null

# 5. Socket-free environment (upstream test_build.yml fork-PR placeholders).
export TNR_REPO="$REPO" NODE_ENV=test
export NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_PUSHER_APP_KEY=test-key NEXT_PUBLIC_PUSHER_APP_CLUSTER=mt1
export PUSHER_APP_ID=test-app PUSHER_APP_SECRET=test-secret DATABASE_URL=http://127.0.0.1:1
export OPENAI_API_KEY=test-placeholder-not-a-real-key
export TEST_MYSQL_URL="mysql://root@localhost/tnr_test?socketPath=$SOCKDIR/mysqld.sock" TEST_MYSQL_ALLOW_DESTRUCTIVE=1

set +e
# 5a. Upstream preflight: the engine's own AI-decision and quest-run suites at the pin.
PREFLIGHT=(tests/libs/combat/ai_v2.test.ts tests/libs/combat/ai_v2_rules.test.ts tests/libs/combat/ai_v2_unreachable_target.test.ts
  tests/libs/combat/ai_v2_summon_fallback.test.ts tests/libs/combat/seal_stealth.test.ts tests/libs/questReset.test.ts
  tests/server/api/quests.pyramidConsequences.test.ts tests/server/api/quests.entryCharge.test.ts tests/server/api/quests.runState.test.ts)
PRE_STATUS=0
if [[ -z "$FILTER" ]]; then
  (cd "$APP" && unshare -rn bun test "${PREFLIGHT[@]}" --timeout 600000) > "$OUT/upstream_preflight.log" 2>&1
  PRE_STATUS=$?
  grep -E '^ *[0-9]+ (pass|fail)|^Ran ' "$OUT/upstream_preflight.log"
fi
# 5b. Gates A (AI) and C (content).
case "$FILTER" in "") GATES="a_ai c_content"; PAT="" ;; *ai*) GATES="a_ai"; PAT="/a_ai" ;; *content*) GATES="c_content"; PAT="/c_content" ;; *) GATES=""; PAT="" ;; esac
(cd "$APP" && TNR_OUT="$OUT" unshare -rn bun test "$SUITE$PAT" --timeout 900000) 2>&1 | grep -v '^\[Upstash Redis\]' > "$OUT/bun_test${FILTER:+_$FILTER}.log"
BUN_STATUS=${PIPESTATUS[0]}
grep -E '^ *[0-9]+ (pass|fail)|^Ran ' "$OUT/bun_test${FILTER:+_$FILTER}.log"
python3 "$P1/tools/check_evidence.py" "$OUT" $GATES
EVIDENCE_STATUS=$?
# 5c. The frozen C99 runtime gates D/R/E with the COMPILED candidate quest as the fixture.
RT_STATUS=0
if [[ -z "$FILTER" ]]; then
  mkdir -p "$OUT/compiled_runtime"
  (cd "$APP" && TNR_VARIANT=alt99_f4gate TNR_GRAPH="$GRAPH" TNR_COMPILED_QUEST="$COMPILED" TNR_OUT="$OUT/compiled_runtime" \
    unshare -rn bun test "$RUNTIME" --timeout 900000) 2>&1 | grep -v '^\[Upstash Redis\]' > "$OUT/compiled_runtime/bun_test.log"
  RT_STATUS=${PIPESTATUS[0]}
  grep -E '^ *[0-9]+ (pass|fail)|^Ran ' "$OUT/compiled_runtime/bun_test.log"
  python3 "$P1/tools/check_evidence.py" "$OUT/compiled_runtime" d_defect r_runtime e_edges || RT_STATUS=1
fi
set -e
STATUS=0
for s in "$GEN_STATUS" "$VALIDATE_STATUS" "$PRE_STATUS" "$BUN_STATUS" "$EVIDENCE_STATUS" "$RT_STATUS"; do [[ "$s" -ne 0 ]] && STATUS=1; done
echo "run.sh: generators=$GEN_STATUS validate=$VALIDATE_STATUS preflight=$PRE_STATUS bun=$BUN_STATUS evidence=$EVIDENCE_STATUS compiledRuntime=$RT_STATUS -> exit $STATUS"

# 6. Provenance.
python3 - "$OUT/provenance${FILTER:+_$FILTER}.json" "$APP" "$PIN" "$REPO" "$MYSQL_IMAGE" "$GEN_STATUS" "$VALIDATE_STATUS" "$PRE_STATUS" "$BUN_STATUS" "$EVIDENCE_STATUS" "$RT_STATUS" <<'PY'
import hashlib, json, os, subprocess, sys
out, app, pin, repo, image, gen, val, pre, bun, evid, rt = sys.argv[1:]
def sha(p):
    with open(p, "rb") as fh: return hashlib.sha256(fh.read()).hexdigest()
def run(*a):
    try: return subprocess.run(a, capture_output=True, text=True, check=True).stdout.strip()
    except Exception as e: return f"unavailable: {e}"
files = {}
for base in ("state/silent_bastion_authoring", "harness/silent_bastion_authoring/engine", "harness/silent_bastion_authoring/tools", "harness/silent_bastion_condensed99/engine",
             "harness/silent_bastion_phase1/engine/lib"):
    for root, dirs, fs in os.walk(os.path.join(repo, base)):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for f in sorted(fs):
            p = os.path.join(root, f); files[os.path.relpath(p, repo)] = sha(p)
for f in ("harness/silent_bastion_authoring/run.sh", "harness/silent_bastion_phase1/tools/check_evidence.py",
          "state/silent_bastion_approved_authoring_lock.json", "harness/silent_bastion_condensed99/graphs/alt99_f4gate.json",
          "skills/building-tnr-content/scripts/validate.py", "state/prompt_silent_bastion_complete_authoring.md", "state/silent_bastion_commander_roster.md", "state/silent_bastion_arakane_ai_profile.md"):
    files[f] = sha(os.path.join(repo, f))
src = ("src/libs/quest.ts", "src/libs/objectives.ts", "src/libs/combat/ai_v2.ts", "src/libs/combat/actions.ts", "src/libs/combat/util.ts",
       "src/validators/ai.ts", "src/validators/combat.ts", "src/validators/objectives.ts", "src/server/api/routers/ai.ts",
       "src/server/api/routers/combat.ts", "src/server/api/routers/quests.ts", "drizzle/constants.ts")
json.dump({
    "engine": {"repository": "studie-tech/TheNinjaRPG", "commit": pin, "export": "git archive <pin> app",
               "bunLockSha256": sha(os.path.join(app, "bun.lock")), "sourceSha256": {p: sha(os.path.join(app, p)) for p in src}},
    "database": {"image": image, "network": "--network none; unix socket only"},
    "runtime": {"bun": run("bun", "--version"), "node": run("node", "--version"), "python": sys.version.split()[0], "uname": run("uname", "-sr")},
    "isolation": {"network": "unshare -rn (no interfaces)", "env": "upstream test_build.yml fork-PR placeholders; no credentials", "liveGameRequests": 0},
    "fileSha256": files,
    "exitStatus": {"generators": int(gen), "validatePy": int(val), "upstreamPreflight": int(pre), "bunTest": int(bun), "evidenceCheck": int(evid), "compiledRuntime": int(rt)},
}, open(out, "w"), indent=1)
PY
exit "$STATUS"
