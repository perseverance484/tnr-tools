#!/usr/bin/env bash
# Offline PvP turn simulator on the pinned engine. Usage: harness/pvp_turn/run.sh REQUEST.json
# Env: TNR_ENGINE_APP = an exported, dependency-installed engine app (game commit in $APP/../PIN).
# Runs with socket syscalls denied (TNR_NETWORK_ISOLATION=seccomp|unshare, default seccomp).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
APP="${TNR_ENGINE_APP:?Set TNR_ENGINE_APP to the exported engine app dir}"
[[ -d "$APP/node_modules" ]] || { echo "engine app has no node_modules" >&2; exit 2; }
SUITE="$APP/tests/tnr_pvp_turn"
mkdir -p "$SUITE/lib"
cp "$HERE/engine/turn_sim.ts" "$SUITE/"
# lib = ghost_ship_final/engine/lib ported to the upstream engine layout (see engine/lib/*.ts headers)
for f in fixtures sim itembattle; do cp "$HERE/engine/lib/$f.ts" "$SUITE/lib/"; done
# test-helper location differs by engine version (tests/setup/combat.ts upstream; older pins: libs/combat/helpers)
if [[ -f "$APP/tests/setup/combat.ts" ]]; then
  echo 'export { makeEffect } from "../../setup/combat";' > "$SUITE/lib/helpers.ts"
else
  echo 'export { makeEffect } from "../../libs/combat/helpers/battleScenario";' > "$SUITE/lib/helpers.ts"
fi
REQ="$(realpath "$1")"
cd "$APP"
# only CI placeholders enter the child (same allowlist as harness/ghost_ship_final/tools/test_env.sh)
exec env -i PATH="$PATH" TNR_LIST_ACTIONS="${TNR_LIST_ACTIONS:-}" NODE_ENV=test NEXT_PUBLIC_NODE_ENV=test \
  NEXT_PUBLIC_BASE_URL=http://localhost:3000 \
  NEXT_PUBLIC_PUSHER_APP_KEY=test-key NEXT_PUBLIC_PUSHER_APP_CLUSTER=mt1 \
  PUSHER_APP_ID=test-app PUSHER_APP_SECRET=test-secret \
  DATABASE_URL=http://127.0.0.1:1 OPENAI_API_KEY=test-placeholder-not-a-real-key \
  TNR_REPO="$REPO" TNR_NETWORK_ISOLATION="${TNR_NETWORK_ISOLATION:-seccomp}" \
  python3 "$REPO/harness/ghost_ship_final/tools/offline_exec.py" bun "$SUITE/turn_sim.ts" "$REQ"
