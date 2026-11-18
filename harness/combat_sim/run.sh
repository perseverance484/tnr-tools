#!/usr/bin/env bash
# TNR combat sim: runs real fights on the pinned game engine, offline. Zero live requests:
# the engine runs from a git-archive export of a local game checkout, inside a socket-denied child.
#
#   harness/combat_sim/run.sh <script> [args...]
#     run.sh main.ts --scenario harness/combat_sim/scenarios/genin_hideout.json --out results/genin.json
#     run.sh replay.ts --scenario harness/combat_sim/scenarios/isonade_replay.json --out results/replay.json
#     run.sh selftest.ts
#
# Env:
#   TNR_ENGINE_APP   an existing export's app dir whose PIN file matches ENGINE_PIN (skips export + install)
#   TNR_ENGINE_SRC   local game clone to export from (default /root/work/game); never modified
#   TNR_ENGINE_PIN   commit to export (default: ENGINE_PIN)
#   TNR_ENGINE_WORK  scratch dir for the export (default $TMPDIR/tnr_combat_sim, outside the repo)
#   TNR_NETWORK_ISOLATION  unshare (default) | seccomp
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PIN="${TNR_ENGINE_PIN:-$(cat "$HERE/ENGINE_PIN")}"
BUN="${BUN:-$(command -v bun || echo /root/.bun/bin/bun)}"
OFFLINE="$REPO/harness/ghost_ship_final/tools/offline_exec.py"
SCRIPT="${1:?usage: run.sh <main.ts|replay.ts|selftest.ts> [args...]}"; shift
[[ -f "$HERE/engine/$SCRIPT" ]] || { echo "no engine script $SCRIPT" >&2; exit 2; }

if [[ -n "${TNR_ENGINE_APP:-}" ]]; then
  APP="$(realpath "$TNR_ENGINE_APP")"
  [[ "$(cat "$APP/../PIN")" == "$PIN" ]] || { echo "TNR_ENGINE_APP is not at pin $PIN" >&2; exit 2; }
else
  SRC="${TNR_ENGINE_SRC:-/root/work/game}"
  WORK="${TNR_ENGINE_WORK:-${TMPDIR:-/tmp}/tnr_combat_sim}"
  ENGINE="$WORK/engine-$PIN"
  APP="$ENGINE/app"
  git -C "$SRC" cat-file -e "$PIN^{commit}"
  if [[ ! -f "$ENGINE/PIN" ]]; then
    [[ ! -e "$ENGINE" ]] || { echo "unmarked export at $ENGINE; remove it" >&2; exit 2; }
    mkdir -p "$ENGINE"
    git -C "$SRC" archive "$PIN" app | tar -x -C "$ENGINE"
    printf '%s\n' "$PIN" > "$ENGINE/PIN"
  fi
  [[ "$(cat "$ENGINE/PIN")" == "$PIN" ]] || { echo "wrong engine pin" >&2; exit 2; }
  [[ -e "$APP/node_modules" ]] || (cd "$APP" && "$BUN" install --frozen-lockfile --ignore-scripts)
fi

# Per-invocation copy so concurrent runs never read each other's half-copied files.
RUNDIR="tnr_combat_sim_$$"
mkdir -p "$APP/$RUNDIR"
cp "$HERE"/engine/*.ts "$APP/$RUNDIR/"

# Resolve path arguments against the caller's cwd before changing into the app.
ARGS=()
prev=""
for a in "$@"; do
  if [[ "$prev" == "--scenario" || "$prev" == "--out" || "$prev" == "--lib" ]]; then a="$(realpath -m "$a")"; fi
  ARGS+=("$a"); prev="$a"
done

cd "$APP"
trap 'rm -rf "$APP/$RUNDIR"' EXIT
env -i PATH="$PATH" NODE_ENV=test \
  NEXT_PUBLIC_BASE_URL=http://localhost:3000 \
  NEXT_PUBLIC_PUSHER_APP_KEY=test-key NEXT_PUBLIC_PUSHER_APP_CLUSTER=mt1 \
  PUSHER_APP_ID=test-app PUSHER_APP_SECRET=test-secret \
  DATABASE_URL=http://127.0.0.1:1 OPENAI_API_KEY=test-placeholder-not-a-real-key \
  UPSTASH_REDIS_REST_URL=http://127.0.0.1:1 UPSTASH_REDIS_REST_TOKEN=offline \
  TNR_HARNESS="$HERE" TNR_REPO="$REPO" TNR_ENGINE_PIN="$PIN" \
  TNR_NETWORK_ISOLATION="${TNR_NETWORK_ISOLATION:-unshare}" \
  python3 "$OFFLINE" "$BUN" run "$RUNDIR/$SCRIPT" "${ARGS[@]}"
