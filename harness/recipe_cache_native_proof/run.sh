#!/usr/bin/env bash
# Silent Bastion one-of-two reward cache — native offline proof.
#
#   harness/recipe_cache_native_proof/run.sh            # preflight + gates S, F + alt99_f4gate regression
#   harness/recipe_cache_native_proof/run.sh flow       # one gate (static|flow)
#
# Brief: docs/handoffs/RECIPE_ALIGNED_CACHE_NATIVE_OFFLINE_PROOF_BRIEF_20261016.md
# Same isolation as harness/silent_bastion_condensed99/run.sh: git-archive export of the pinned
# engine, frozen lockfile without lifecycle scripts, socket-only throwaway MySQL from the upstream
# CI image (--network none), tests inside `unshare -rn`, placeholder environment, no credentials.
# No engine file is modified. Synthetic cache/ingredient items only.
#
# Environment (optional): TNR_ENGINE_SRC, TNR_ENGINE_WORK (default .work/), TNR_OUT (default
# results/), TNR_KEEP_DB=1.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
P1="$REPO/harness/silent_bastion_phase1"
C99="$REPO/harness/silent_bastion_condensed99"
PIN="0651b039a466516a8fe24fc13b56f60dea11b7eb"
UPSTREAM="https://github.com/studie-tech/TheNinjaRPG.git"
MYSQL_IMAGE="mysql:26.7.0@sha256:893418c8a7a34c60d2d961cc30ef136095da141478562ed2101ae3f5faba9c3f"
CONTAINER="tnr-rc-proof-mysql"
GRAPH="harness/silent_bastion_condensed99/graphs/alt99_f4gate.json"
WORK="${TNR_ENGINE_WORK:-$HERE/.work}"
OUT="${TNR_OUT:-$HERE/results}"
FILTER="${1:-}"
ENGINE="$WORK/engine"
APP="$ENGINE/app"
SUITE="tests/tnr_recipe_cache_proof"
REGR="tests/tnr_c99_regression"
SOCKDIR="$WORK/mysqld"

mkdir -p "$WORK" "$OUT"

# 1. Pinned engine export.
if [[ ! -f "$ENGINE/PIN" ]]; then
  SRC="${TNR_ENGINE_SRC:-$WORK/src}"
  [[ -d "$SRC/.git" ]] || git clone --filter=blob:none --no-checkout "$UPSTREAM" "$SRC"
  git -C "$SRC" cat-file -e "$PIN^{commit}"
  rm -rf "$ENGINE" && mkdir -p "$ENGINE"
  git -C "$SRC" archive "$PIN" app | tar -x -C "$ENGINE"
  echo "$PIN" > "$ENGINE/PIN"
fi
[[ "$(cat "$ENGINE/PIN")" == "$PIN" ]] || { echo "engine export is not at $PIN" >&2; exit 2; }

# 2. Dependencies from the pinned lockfile, no lifecycle scripts.
[[ -d "$APP/node_modules" ]] || (cd "$APP" && bun install --frozen-lockfile --ignore-scripts)

# 3. Install the suites: shared fixture libs + this proof's gates; the C99 gates as regression.
for S in "$SUITE" "$REGR"; do rm -rf "${APP:?}/$S" && mkdir -p "$APP/$S/lib"; done
cp "$P1/engine/lib/graph.ts" "$P1/engine/lib/driver.ts" "$P1/engine/lib/report.ts" "$C99/engine/lib/run99.ts" "$APP/$SUITE/lib/"
cp -R "$HERE/engine/." "$APP/$SUITE/"
cp "$P1/engine/lib/graph.ts" "$P1/engine/lib/driver.ts" "$P1/engine/lib/report.ts" "$APP/$REGR/lib/"
cp -R "$C99/engine/." "$APP/$REGR/"

# 4. Throwaway MySQL, socket only.
if ! docker info >/dev/null 2>&1; then
  echo "docker daemon not reachable; start it (e.g. 'dockerd &') and rerun" >&2; exit 2
fi
mkdir -p "$SOCKDIR" && chmod 777 "$SOCKDIR"
if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
  rm -f "$SOCKDIR"/*
  docker run -d --name "$CONTAINER" --network none \
    -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -e MYSQL_DATABASE=tnr_test \
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
export TNR_REPO="$REPO" TNR_GRAPH="$GRAPH" NODE_ENV=test
export NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_PUSHER_APP_KEY=test-key NEXT_PUBLIC_PUSHER_APP_CLUSTER=mt1
export PUSHER_APP_ID=test-app PUSHER_APP_SECRET=test-secret DATABASE_URL=http://127.0.0.1:1
export OPENAI_API_KEY=test-placeholder-not-a-real-key
export TEST_MYSQL_URL="mysql://root@localhost/tnr_test?socketPath=$SOCKDIR/mysqld.sock" TEST_MYSQL_ALLOW_DESTRUCTIVE=1

set +e
# 5a. Upstream preflight at the pin: reward choice, weighted cache, Pyramid/run/entry suites.
PREFLIGHT=(tests/libs/rewardChoice.test.ts tests/validators/rewardChoice.test.ts tests/server/api/quests.rewardChoiceSql.test.ts
  tests/libs/weightedCache.test.ts tests/server/api/item.weightedCache.sql.test.ts
  tests/server/api/quests.pyramidConsequences.test.ts tests/server/api/quests.entryCharge.test.ts
  tests/server/api/quests.runState.test.ts tests/server/api/quests.isolation.test.ts tests/libs/questReset.test.ts
  tests/libs/questRun.test.ts tests/server/api/quests.persistentBattle.test.ts)
PRE_STATUS=0
if [[ -z "$FILTER" ]]; then
  (cd "$APP" && unshare -rn bun test "${PREFLIGHT[@]}" --timeout 600000) > "$OUT/upstream_preflight.log" 2>&1
  PRE_STATUS=$?
  grep -E '^ *[0-9]+ (pass|fail)|^Ran ' "$OUT/upstream_preflight.log"
fi
# 5b. This proof's gates.
case "$FILTER" in
  "") GATES="s_static f_flow" ;; *static*) GATES="s_static" ;; *flow*) GATES="f_flow" ;; *) GATES="" ;;
esac
(cd "$APP" && TNR_OUT="$OUT" unshare -rn bun test "$SUITE${FILTER:+/rc_}${FILTER}" --timeout 900000) 2>&1 \
  | grep -v '^\[Upstash Redis\]' > "$OUT/bun_test${FILTER:+_$FILTER}.log"
BUN_STATUS=${PIPESTATUS[0]}
grep -E '^ *[0-9]+ (pass|fail)|^Ran ' "$OUT/bun_test${FILTER:+_$FILTER}.log"
python3 "$P1/tools/check_evidence.py" "$OUT" $GATES
EVIDENCE_STATUS=$?
# 5c. Regression: the frozen C99 gates on alt99_f4gate at this pin (source-drift check).
REGR_STATUS=0
if [[ -z "$FILTER" ]]; then
  mkdir -p "$OUT/c99_regression_alt99_f4gate"
  (cd "$APP" && TNR_VARIANT=alt99_f4gate TNR_OUT="$OUT/c99_regression_alt99_f4gate" unshare -rn bun test "$REGR" --timeout 900000) 2>&1 \
    | grep -v '^\[Upstash Redis\]' > "$OUT/c99_regression_alt99_f4gate/bun_test.log"
  REGR_STATUS=${PIPESTATUS[0]}
  grep -E '^ *[0-9]+ (pass|fail)|^Ran ' "$OUT/c99_regression_alt99_f4gate/bun_test.log"
  python3 "$P1/tools/check_evidence.py" "$OUT/c99_regression_alt99_f4gate" s_static d_defect r_runtime e_edges || REGR_STATUS=1
fi
set -e
STATUS=0
for s in "$PRE_STATUS" "$BUN_STATUS" "$EVIDENCE_STATUS" "$REGR_STATUS"; do [[ "$s" -ne 0 ]] && STATUS=1; done
echo "run.sh: preflight=$PRE_STATUS bun=$BUN_STATUS evidence=$EVIDENCE_STATUS regression=$REGR_STATUS -> exit $STATUS"

# 6. Provenance.
python3 - "$OUT/provenance${FILTER:+_$FILTER}.json" "$APP" "$PIN" "$HERE" "$REPO" "$MYSQL_IMAGE" "$GRAPH" "$PRE_STATUS" "$BUN_STATUS" "$EVIDENCE_STATUS" "$REGR_STATUS" <<'PY'
import hashlib, json, os, subprocess, sys
out, app, pin, here, repo, image, graph, pre, bun, evid, regr = sys.argv[1:]
def sha(p):
    with open(p, "rb") as fh: return hashlib.sha256(fh.read()).hexdigest()
def run(*a):
    try: return subprocess.run(a, capture_output=True, text=True, check=True).stdout.strip()
    except Exception as e: return f"unavailable: {e}"
files = {}
for base in ("harness/recipe_cache_native_proof/engine", "harness/silent_bastion_condensed99/engine", "harness/silent_bastion_phase1/engine/lib"):
    for root, dirs, fs in os.walk(os.path.join(repo, base)):
        dirs[:] = sorted(dirs)
        for f in sorted(fs):
            p = os.path.join(root, f); files[os.path.relpath(p, repo)] = sha(p)
for f in ("harness/recipe_cache_native_proof/run.sh", "harness/silent_bastion_phase1/tools/check_evidence.py"):
    files[f] = sha(os.path.join(repo, f))
src = ("src/libs/quest.ts", "src/libs/rewardChoice.ts", "src/libs/weightedCache.ts", "src/validators/weightedCache.ts",
       "src/validators/rewards.ts", "src/validators/combat.ts", "src/validators/objectives.ts",
       "src/server/api/routers/quests.ts", "src/server/api/routers/item.ts", "src/server/utils/questEntry.ts", "src/layout/RewardChoice.tsx")
json.dump({
    "engine": {"repository": "studie-tech/TheNinjaRPG", "commit": pin, "export": "git archive <pin> app",
               "bunLockSha256": sha(os.path.join(app, "bun.lock")), "sourceSha256": {p: sha(os.path.join(app, p)) for p in src}},
    "graph": {"path": graph, "sha256": sha(os.path.join(repo, graph))},
    "brief": {"path": "docs/handoffs/RECIPE_ALIGNED_CACHE_NATIVE_OFFLINE_PROOF_BRIEF_20261016.md",
              "sha256": sha(os.path.join(repo, "docs/handoffs/RECIPE_ALIGNED_CACHE_NATIVE_OFFLINE_PROOF_BRIEF_20261016.md"))},
    "database": {"image": image, "network": "--network none; unix socket only"},
    "runtime": {"bun": run("bun", "--version"), "node": run("node", "--version"), "uname": run("uname", "-sr")},
    "isolation": {"network": "unshare -rn (no interfaces)", "env": "upstream test_build.yml fork-PR placeholders; no credentials", "liveGameRequests": 0},
    "harnessFileSha256": files,
    "exitStatus": {"upstreamPreflight": int(pre), "bunTest": int(bun), "evidenceCheck": int(evid), "c99Regression": int(regr)},
}, open(out, "w"), indent=1)
PY
exit "$STATUS"
