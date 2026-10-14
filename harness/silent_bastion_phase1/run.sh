#!/usr/bin/env bash
# Silent Bastion Phase 1 — offline native progression proof.
#
#   harness/silent_bastion_phase1/run.sh            # upstream preflight + gates S, R, E
#   harness/silent_bastion_phase1/run.sh edges      # only p1_edges (also: static, runtime)
#
# Engine: studie-tech/TheNinjaRPG at PIN, exported with `git archive` into a disposable work
# directory (the upstream working tree is never touched; no engine file is modified).
# Dependencies: pinned bun.lock, lifecycle scripts disabled.
# Database: a throwaway MySQL from the upstream CI's own image (test_build.yml: mysql:26.7.0),
# started with `--network none` and reachable ONLY through a unix socket in the work directory.
# Tests: `unshare -rn` (a network namespace with no interfaces), upstream CI fork-PR placeholder
# environment values, no credentials. Zero live-game requests are possible from inside the run.
#
# Environment (optional): TNR_ENGINE_SRC (existing clone), TNR_ENGINE_WORK (default .work/),
# TNR_OUT (default results/), TNR_KEEP_DB=1 (leave the MySQL container running).
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PIN="c82dc7f8ee76cb9ac498c0689f71b6f13bfe69dd"
UPSTREAM="https://github.com/studie-tech/TheNinjaRPG.git"
MYSQL_IMAGE="mysql:26.7.0@sha256:893418c8a7a34c60d2d961cc30ef136095da141478562ed2101ae3f5faba9c3f"
CONTAINER="tnr-sb-phase1-mysql"
WORK="${TNR_ENGINE_WORK:-$HERE/.work}"
OUT="${TNR_OUT:-$HERE/results}"
FILTER="${1:-}"
ENGINE="$WORK/engine"
APP="$ENGINE/app"
SUITE_DIR="tests/tnr_silent_bastion_phase1"
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

# 3. Install the suite into the disposable export.
rm -rf "${APP:?}/$SUITE_DIR" && mkdir -p "$APP/$SUITE_DIR"
cp -R "$HERE/engine/." "$APP/$SUITE_DIR/"

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
export TNR_REPO="$REPO" TNR_OUT="$OUT" NODE_ENV=test
export NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_PUSHER_APP_KEY=test-key NEXT_PUBLIC_PUSHER_APP_CLUSTER=mt1
export PUSHER_APP_ID=test-app PUSHER_APP_SECRET=test-secret DATABASE_URL=http://127.0.0.1:1
export OPENAI_API_KEY=test-placeholder-not-a-real-key
export TEST_MYSQL_URL="mysql://root@localhost/tnr_test?socketPath=$SOCKDIR/mysqld.sock" TEST_MYSQL_ALLOW_DESTRUCTIVE=1

set +e
# 5a. Upstream preflight at the pin: the engine's own Pyramid/quest-run suites in this environment.
PREFLIGHT=(tests/libs/quest.battleRetry.test.ts tests/libs/questRun.test.ts tests/server/api/quests.persistentBattle.test.ts
  tests/server/api/quests.isolation.test.ts tests/server/api/quests.runState.test.ts tests/server/api/combat.questEntry.test.ts
  tests/server/api/quests.pyramidConsequences.test.ts tests/server/api/quests.battleConsequences.test.ts)
PRE_STATUS=0
if [[ -z "$FILTER" ]]; then
  (cd "$APP" && unshare -rn bun test "${PREFLIGHT[@]}" --timeout 600000) > "$OUT/upstream_preflight.log" 2>&1
  PRE_STATUS=$?
  tail -5 "$OUT/upstream_preflight.log"
fi
# 5b. Gates S, R, E.
(cd "$APP" && unshare -rn bun test "$SUITE_DIR${FILTER:+/p1_}${FILTER}" --timeout 900000) 2>&1 \
  | grep -v '^\[Upstash Redis\]' | tee "$OUT/bun_test${FILTER:+_$FILTER}.log"
BUN_STATUS=${PIPESTATUS[0]}
case "$FILTER" in
  "") GATES="s_static r_runtime e_edges" ;;
  *static*) GATES="s_static" ;; *runtime*) GATES="r_runtime" ;; *edges*) GATES="e_edges" ;; *) GATES="" ;;
esac
python3 "$HERE/tools/check_evidence.py" "$OUT" $GATES
EVIDENCE_STATUS=$?
set -e
STATUS=0
for s in "$PRE_STATUS" "$BUN_STATUS" "$EVIDENCE_STATUS"; do [[ "$s" -ne 0 ]] && STATUS=1; done
echo "run.sh: preflight=$PRE_STATUS bun=$BUN_STATUS evidence=$EVIDENCE_STATUS -> exit $STATUS"

# 6. Provenance.
python3 - "$OUT/provenance${FILTER:+_$FILTER}.json" "$APP" "$PIN" "$HERE" "$REPO" "$MYSQL_IMAGE" "$PRE_STATUS" "$BUN_STATUS" "$EVIDENCE_STATUS" <<'PY'
import hashlib, json, os, subprocess, sys
out, app, pin, here, repo, image, pre, bun, evid = sys.argv[1:]
def sha(p):
    with open(p, "rb") as fh: return hashlib.sha256(fh.read()).hexdigest()
def run(*a):
    try: return subprocess.run(a, capture_output=True, text=True, check=True).stdout.strip()
    except Exception as e: return f"unavailable: {e}"
harness = {}
for sub in ("engine", "tools"):
    for root, dirs, files in os.walk(os.path.join(here, sub)):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for f in sorted(files):
            p = os.path.join(root, f); harness[os.path.relpath(p, here)] = sha(p)
harness["run.sh"] = sha(os.path.join(here, "run.sh"))
json.dump({
    "engine": {"repository": "studie-tech/TheNinjaRPG", "commit": pin, "export": "git archive <pin> app",
               "bunLockSha256": sha(os.path.join(app, "bun.lock")), "packageJsonSha256": sha(os.path.join(app, "package.json"))},
    "designGraph": {"path": "state/silent_bastion_phase1_graph.json", "sha256": sha(os.path.join(repo, "state/silent_bastion_phase1_graph.json"))},
    "database": {"image": image, "network": "--network none; unix socket only", "data": "throwaway, truncated per suite"},
    "runtime": {"bun": run("bun", "--version"), "node": run("node", "--version"), "python": sys.version.split()[0], "uname": run("uname", "-sr")},
    "isolation": {"network": "unshare -rn (no interfaces)", "env": "upstream test_build.yml fork-PR placeholders; no credentials",
                  "liveGameRequests": 0},
    "harnessFileSha256": harness,
    "exitStatus": {"upstreamPreflight": int(pre), "bunTest": int(bun), "evidenceCheck": int(evid)},
}, open(out, "w"), indent=1)
PY
exit "$STATUS"
