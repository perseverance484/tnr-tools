#!/usr/bin/env bash
# TNR combat sim: runs real fights on the pinned game engine, offline. Zero live requests and no
# package installs: the engine runs from a git-archive export of a local game checkout, inside a
# socket-denied child, with dependencies that were provisioned beforehand (see README "Setup").
#
#   harness/combat_sim/run.sh <script> [args...]
#     run.sh main.ts --scenario harness/combat_sim/scenarios/genin_hideout.json --out results/genin.json
#     run.sh replay.ts --scenario harness/combat_sim/scenarios/isonade_replay.json --out results/replay.json
#     run.sh selftest.ts
#
# The engine commit is always the committed ENGINE_PIN. Before every run the export's source tree is
# checked file by file against `git ls-tree <pin> app` in the game clone; any changed, missing or extra
# file (outside node_modules and this launcher's own run folders) stops the run.
#
# Env:
#   TNR_ENGINE_APP   an existing export's app dir (skips the export step; still verified against the pin)
#   TNR_ENGINE_SRC   local game clone holding the pin (default /root/work/game); never modified
#   TNR_ENGINE_PIN   optional; must equal ENGINE_PIN if set (a different pin means editing ENGINE_PIN in a commit)
#   TNR_ENGINE_WORK  scratch dir for a new export (default $TMPDIR/tnr_combat_sim, outside the repo)
#   TNR_NETWORK_ISOLATION  unshare (default) | seccomp
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PIN="$(tr -d '[:space:]' < "$HERE/ENGINE_PIN")"
[[ "$PIN" =~ ^[0-9a-f]{40}$ ]] || { echo "ENGINE_PIN is not a full commit sha" >&2; exit 2; }
if [[ -n "${TNR_ENGINE_PIN:-}" && "$TNR_ENGINE_PIN" != "$PIN" ]]; then
  echo "TNR_ENGINE_PIN=$TNR_ENGINE_PIN conflicts with the committed ENGINE_PIN $PIN; change ENGINE_PIN in a commit instead" >&2
  exit 2
fi
BUN="${BUN:-$(command -v bun || echo /root/.bun/bin/bun)}"
OFFLINE="$REPO/harness/ghost_ship_final/tools/offline_exec.py"
SCRIPT="${1:?usage: run.sh <main.ts|replay.ts|selftest.ts> [args...]}"; shift
[[ -f "$HERE/engine/$SCRIPT" ]] || { echo "no engine script $SCRIPT" >&2; exit 2; }
SRC="${TNR_ENGINE_SRC:-/root/work/game}"
git -C "$SRC" cat-file -e "$PIN^{commit}" 2>/dev/null || { echo "game clone $SRC does not hold pin $PIN" >&2; exit 2; }

if [[ -n "${TNR_ENGINE_APP:-}" ]]; then
  APP="$(realpath "$TNR_ENGINE_APP")"
else
  WORK="${TNR_ENGINE_WORK:-${TMPDIR:-/tmp}/tnr_combat_sim}"
  ENGINE="$WORK/engine-$PIN"
  APP="$ENGINE/app"
  if [[ ! -e "$ENGINE" ]]; then
    mkdir -p "$ENGINE"
    git -C "$SRC" archive "$PIN" app | tar -x -C "$ENGINE"
  fi
fi
[[ -d "$APP" ]] || { echo "no engine export at $APP" >&2; exit 2; }

# Verify the export's source against the pinned tree (blob hashes, exact file set).
python3 "$HERE/tools/verify_export.py" "$SRC" "$PIN" "$APP"

# Dependencies are provisioned outside this harness; never install here.
if [[ ! -d "$APP/node_modules" ]]; then
  echo "no node_modules in $APP: provision the engine's dependencies first (README, Setup); run.sh never installs" >&2
  exit 3
fi

# Hash of the harness engine code this run uses, recorded in results.
CODE="$(cd "$HERE" && sha256sum engine/*.ts | sha256sum | cut -c1-64)"

# Per-invocation copy so concurrent runs never read each other's half-copied files.
RUNDIR="tnr_combat_sim_$$"
mkdir -p "$APP/$RUNDIR"
trap 'rm -rf "$APP/$RUNDIR"' EXIT
cp "$HERE"/engine/*.ts "$APP/$RUNDIR/"

# Resolve path arguments against the caller's cwd before changing into the app.
ARGS=()
prev=""
for a in "$@"; do
  if [[ "$prev" == "--scenario" || "$prev" == "--out" || "$prev" == "--lib" || "$prev" == "--traces" ]]; then a="$(realpath -m "$a")"; fi
  ARGS+=("$a"); prev="$a"
done

cd "$APP"
env -i PATH="$PATH" NODE_ENV=test \
  NEXT_PUBLIC_BASE_URL=http://localhost:3000 \
  NEXT_PUBLIC_PUSHER_APP_KEY=test-key NEXT_PUBLIC_PUSHER_APP_CLUSTER=mt1 \
  PUSHER_APP_ID=test-app PUSHER_APP_SECRET=test-secret \
  DATABASE_URL=http://127.0.0.1:1 OPENAI_API_KEY=test-placeholder-not-a-real-key \
  UPSTASH_REDIS_REST_URL=http://127.0.0.1:1 UPSTASH_REDIS_REST_TOKEN=offline \
  TNR_HARNESS="$HERE" TNR_REPO="$REPO" TNR_ENGINE_PIN="$PIN" TNR_HARNESS_CODE="$CODE" \
  TNR_NETWORK_ISOLATION="${TNR_NETWORK_ISOLATION:-unshare}" \
  python3 "$OFFLINE" "$BUN" run --preload "./$RUNDIR/entropy_plugin.ts" "$RUNDIR/$SCRIPT" "${ARGS[@]}"
