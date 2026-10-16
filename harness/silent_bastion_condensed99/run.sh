#!/usr/bin/env bash
# Silent Bastion condensed 99-node candidate — offline native recovery/reset proof.
#
#   harness/silent_bastion_condensed99/run.sh          # upstream preflight + gates S, D, R, E on every variant
#   harness/silent_bastion_condensed99/run.sh runtime  # only c99_runtime (also: static, defect, edges)
#   TNR_VARIANTS="candidate" harness/silent_bastion_condensed99/run.sh   # one variant only
#
# Variants: `candidate` = state/silent_bastion_condensed99_candidate.json (the director-selected
# design under test); `alt*` = graphs/<name>.json, content-only remediation options derived by
# tools/derive_alternatives.py. Evidence goes to results/<variant>/.
#
# Same isolation as harness/silent_bastion_phase1/run.sh (git-archive export of the pinned engine,
# frozen lockfile without lifecycle scripts, socket-only throwaway MySQL from the upstream CI image,
# tests inside `unshare -rn`, placeholder environment, no credentials). The fixture compiler is the
# Phase 1 one (harness/silent_bastion_phase1/engine/lib/graph.ts), pointed at the 99-node graph by
# TNR_GRAPH. No engine file is modified.
#
# Environment (optional): TNR_ENGINE_SRC (existing clone), TNR_ENGINE_WORK (default .work/),
# TNR_OUT (default results/), TNR_VARIANTS (space-separated), TNR_KEEP_DB=1.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
P1="$REPO/harness/silent_bastion_phase1"
PIN="13d40c4c1509ecf44262aba1b5120266011ea786"
UPSTREAM="https://github.com/studie-tech/TheNinjaRPG.git"
MYSQL_IMAGE="mysql:26.7.0@sha256:893418c8a7a34c60d2d961cc30ef136095da141478562ed2101ae3f5faba9c3f"
CONTAINER="tnr-sb-c99-mysql"
VARIANTS="${TNR_VARIANTS:-candidate alt99_f4gate alt99_alertgate alt95_bossgates}"
graph_for() { [[ "$1" == candidate ]] && echo "state/silent_bastion_condensed99_candidate.json" || echo "harness/silent_bastion_condensed99/graphs/$1.json"; }
WORK="${TNR_ENGINE_WORK:-$HERE/.work}"
OUT="${TNR_OUT:-$HERE/results}"
FILTER="${1:-}"
ENGINE="$WORK/engine"
APP="$ENGINE/app"
SUITE_DIR="tests/tnr_silent_bastion_c99"
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

# 3. Install the suite: Phase 1 compiler/driver/report + this harness's scenario and gates.
rm -rf "${APP:?}/$SUITE_DIR" && mkdir -p "$APP/$SUITE_DIR/lib"
cp "$P1/engine/lib/graph.ts" "$P1/engine/lib/driver.ts" "$P1/engine/lib/report.ts" "$APP/$SUITE_DIR/lib/"
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
export TNR_REPO="$REPO" NODE_ENV=test
export NEXT_PUBLIC_BASE_URL=http://localhost:3000 NEXT_PUBLIC_PUSHER_APP_KEY=test-key NEXT_PUBLIC_PUSHER_APP_CLUSTER=mt1
export PUSHER_APP_ID=test-app PUSHER_APP_SECRET=test-secret DATABASE_URL=http://127.0.0.1:1
export OPENAI_API_KEY=test-placeholder-not-a-real-key
export TEST_MYSQL_URL="mysql://root@localhost/tnr_test?socketPath=$SOCKDIR/mysqld.sock" TEST_MYSQL_ALLOW_DESTRUCTIVE=1

set +e
# 5a. Upstream preflight at the pin: the engine's own Pyramid/quest-run/reset suites.
PREFLIGHT=(tests/libs/quest.battleRetry.test.ts tests/libs/questRun.test.ts tests/libs/questReset.test.ts
  tests/server/api/quests.persistentBattle.test.ts tests/server/api/quests.isolation.test.ts
  tests/server/api/quests.runState.test.ts tests/server/api/combat.questEntry.test.ts
  tests/server/api/quests.entryCharge.test.ts tests/server/api/quests.pyramidConsequences.test.ts
  tests/server/api/quests.battleConsequences.test.ts)
PRE_STATUS=0
if [[ -z "$FILTER" ]]; then
  (cd "$APP" && unshare -rn bun test "${PREFLIGHT[@]}" --timeout 600000) > "$OUT/upstream_preflight.log" 2>&1
  PRE_STATUS=$?
  tail -5 "$OUT/upstream_preflight.log"
fi
# 5b. Remediation graphs must be current, then gates S, D, R, E per variant.
python3 "$HERE/tools/derive_alternatives.py" --check > "$OUT/derive_check.log" 2>&1
DERIVE_STATUS=$?
cat "$OUT/derive_check.log"
BUN_STATUS=0; EVIDENCE_STATUS=0
case "$FILTER" in
  "") GATES="s_static d_defect r_runtime e_edges" ;;
  *static*) GATES="s_static" ;; *defect*) GATES="d_defect" ;; *runtime*) GATES="r_runtime" ;; *edges*) GATES="e_edges" ;; *) GATES="" ;;
esac
for V in $VARIANTS; do
  mkdir -p "$OUT/$V"
  echo "=== variant $V ($(graph_for "$V")) ==="
  (cd "$APP" && TNR_VARIANT="$V" TNR_GRAPH="$(graph_for "$V")" TNR_OUT="$OUT/$V" unshare -rn bun test "$SUITE_DIR${FILTER:+/c99_}${FILTER}" --timeout 900000) 2>&1 \
    | grep -v '^\[Upstash Redis\]' > "$OUT/$V/bun_test${FILTER:+_$FILTER}.log"
  s=${PIPESTATUS[0]}; [[ "$s" -ne 0 ]] && BUN_STATUS=1
  grep -E '^ *[0-9]+ (pass|fail)|^Ran ' "$OUT/$V/bun_test${FILTER:+_$FILTER}.log"
  python3 "$P1/tools/check_evidence.py" "$OUT/$V" $GATES || EVIDENCE_STATUS=1
done
set -e
STATUS=0
for s in "$PRE_STATUS" "$DERIVE_STATUS" "$BUN_STATUS" "$EVIDENCE_STATUS"; do [[ "$s" -ne 0 ]] && STATUS=1; done
echo "run.sh: preflight=$PRE_STATUS derive=$DERIVE_STATUS bun=$BUN_STATUS evidence=$EVIDENCE_STATUS -> exit $STATUS"

# 6. Provenance.
python3 - "$OUT/provenance${FILTER:+_$FILTER}.json" "$APP" "$PIN" "$HERE" "$REPO" "$MYSQL_IMAGE" "$VARIANTS" "$PRE_STATUS" "$DERIVE_STATUS" "$BUN_STATUS" "$EVIDENCE_STATUS" <<'PY'
import hashlib, json, os, subprocess, sys
out, app, pin, here, repo, image, variants, pre, derive, bun, evid = sys.argv[1:]
def graph_for(v): return "state/silent_bastion_condensed99_candidate.json" if v == "candidate" else f"harness/silent_bastion_condensed99/graphs/{v}.json"
def sha(p):
    with open(p, "rb") as fh: return hashlib.sha256(fh.read()).hexdigest()
def run(*a):
    try: return subprocess.run(a, capture_output=True, text=True, check=True).stdout.strip()
    except Exception as e: return f"unavailable: {e}"
harness = {}
for sub in ("engine", "tools", "graphs"):
    for root, dirs, files in os.walk(os.path.join(here, sub)):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for f in sorted(files):
            p = os.path.join(root, f); harness[os.path.relpath(p, here)] = sha(p)
harness["run.sh"] = sha(os.path.join(here, "run.sh"))
p1 = os.path.join(repo, "harness/silent_bastion_phase1")
for f in ("engine/lib/graph.ts", "engine/lib/driver.ts", "engine/lib/report.ts", "tools/check_evidence.py"):
    harness[f"../silent_bastion_phase1/{f}"] = sha(os.path.join(p1, f))
json.dump({
    "engine": {"repository": "studie-tech/TheNinjaRPG", "commit": pin, "export": "git archive <pin> app",
               "bunLockSha256": sha(os.path.join(app, "bun.lock")), "packageJsonSha256": sha(os.path.join(app, "package.json")),
               "sourceSha256": {p: sha(os.path.join(app, p)) for p in ("src/libs/quest.ts", "src/libs/objectives.ts",
                   "src/validators/objectives.ts", "src/server/api/routers/quests.ts", "src/server/utils/questEntry.ts")}},
    "graphs": {v: {"path": graph_for(v), "sha256": sha(os.path.join(repo, graph_for(v)))} for v in variants.split()},
    "brief": {"path": "docs/handoffs/SILENT_BASTION_CONDENSED99_NATIVE_PROOF_BRIEF.md",
              "sha256": sha(os.path.join(repo, "docs/handoffs/SILENT_BASTION_CONDENSED99_NATIVE_PROOF_BRIEF.md"))},
    "database": {"image": image, "network": "--network none; unix socket only", "data": "throwaway, truncated per suite"},
    "runtime": {"bun": run("bun", "--version"), "node": run("node", "--version"), "python": sys.version.split()[0], "uname": run("uname", "-sr")},
    "isolation": {"network": "unshare -rn (no interfaces)", "env": "upstream test_build.yml fork-PR placeholders; no credentials",
                  "liveGameRequests": 0},
    "harnessFileSha256": harness,
    "exitStatus": {"upstreamPreflight": int(pre), "deriveCheck": int(derive), "bunTest": int(bun), "evidenceCheck": int(evid)},
}, open(out, "w"), indent=1)
PY
exit "$STATUS"
