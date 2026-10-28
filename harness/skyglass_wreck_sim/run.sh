#!/usr/bin/env bash
# Skyglass Wreck offline dungeon simulator. Zero live requests: the engine runs from a
# git-archive export of a local game checkout, inside a socket-denied child process.
#
#   harness/skyglass_wreck_sim/run.sh [main.ts args...]
#   e.g. run.sh --variants geared,strong --runs 30 --out harness/skyglass_wreck_sim/results/baseline.json
#        run.sh --override harness/skyglass_wreck_sim/overrides/candidate_2waves.json --runs 30 --out ...
#        run.sh --probe-check
#
# Env:
#   TNR_ENGINE_SRC   local game clone (default /home/claude/studie-tech/theninjarpg); never modified
#   TNR_ENGINE_PIN   commit to export (default: the pin below)
#   TNR_ENGINE_WORK  scratch dir for the export (default $TMPDIR/tnr_skyglass_wreck_sim, outside the repo)
#   TNR_DEPENDENCIES_APP  optional existing install whose bun.lock/package.json match byte for byte;
#                    otherwise `bun install --frozen-lockfile --ignore-scripts` runs once (npm registry only)
#   TNR_NETWORK_ISOLATION  unshare (default) | seccomp
#   TNR_SCRIPT       engine script to run (default main.ts; trace_floor.ts traces one floor;
#                    calibrate.ts runs the solo-Captain player-strength calibration)
#   TNR_DMG_CONFIG   damage settings for trace_floor.ts (live | default | file)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PIN="${TNR_ENGINE_PIN:-c86f43f4e7ad468bc3673018423edca9fc48a1b1}"
SRC="${TNR_ENGINE_SRC:-/home/claude/studie-tech/theninjarpg}"
WORK="${TNR_ENGINE_WORK:-${TMPDIR:-/tmp}/tnr_skyglass_wreck_sim}"
BUN="${BUN:-$(command -v bun || echo /root/.bun/bin/bun)}"
ENGINE="$WORK/engine-$PIN"
APP="$ENGINE/app"
OFFLINE="$REPO/harness/ghost_ship_final/tools/offline_exec.py"

git -C "$SRC" cat-file -e "$PIN^{commit}"
if [[ ! -f "$ENGINE/PIN" ]]; then
  [[ ! -e "$ENGINE" ]] || { echo "unmarked export at $ENGINE; remove it" >&2; exit 2; }
  mkdir -p "$ENGINE"
  git -C "$SRC" archive "$PIN" app | tar -x -C "$ENGINE"
  printf '%s\n' "$PIN" > "$ENGINE/PIN"
fi
[[ "$(cat "$ENGINE/PIN")" == "$PIN" ]] || { echo "wrong engine pin" >&2; exit 2; }

if [[ ! -e "$APP/node_modules" ]]; then
  if [[ -n "${TNR_DEPENDENCIES_APP:-}" ]]; then
    cmp "$APP/bun.lock" "$TNR_DEPENDENCIES_APP/bun.lock"
    cmp "$APP/package.json" "$TNR_DEPENDENCIES_APP/package.json"
    ln -s "$(realpath "$TNR_DEPENDENCIES_APP/node_modules")" "$APP/node_modules"
  else
    (cd "$APP" && "$BUN" install --frozen-lockfile --ignore-scripts)
  fi
fi

# Observation-only rule probe (see tools/apply_probe.py); export copy only.
python3 "$HERE/tools/apply_probe.py" "$APP"
python3 "$HERE/tools/build_baseline.py" --check
python3 "$HERE/tools/build_crownhold_inputs.py" --check
# Per-invocation copy so concurrent runs never read each other's half-copied files.
RUNDIR="tnr_skyglass_wreck_sim_$$"
mkdir -p "$APP/$RUNDIR"
cp "$HERE"/engine/*.ts "$APP/$RUNDIR/"

# Resolve path arguments against the caller's cwd before changing into the app.
ARGS=()
prev=""
for a in "$@"; do
  if [[ "$prev" == "--override" || "$prev" == "--out" || ( "$prev" == "--dmg-config" && "$a" != "live" && "$a" != "default" ) || "$prev" == "--ladder" ]]; then a="$(realpath -m "$a")"; fi
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
  TNR_HARNESS="$HERE" TNR_REPO="$REPO" TNR_DMG_CONFIG="${TNR_DMG_CONFIG:-live}" \
  TNR_NETWORK_ISOLATION="${TNR_NETWORK_ISOLATION:-unshare}" \
  python3 "$OFFLINE" "$BUN" run "$RUNDIR/${TNR_SCRIPT:-main.ts}" "${ARGS[@]}"
