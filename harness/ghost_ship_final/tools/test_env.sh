#!/usr/bin/env bash
# Only CI placeholders and explicit harness paths enter an offline test child.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
exec env -i PATH="$PATH" NODE_ENV=test \
  NEXT_PUBLIC_BASE_URL=http://localhost:3000 \
  NEXT_PUBLIC_PUSHER_APP_KEY=test-key NEXT_PUBLIC_PUSHER_APP_CLUSTER=mt1 \
  PUSHER_APP_ID=test-app PUSHER_APP_SECRET=test-secret \
  DATABASE_URL=http://127.0.0.1:1 OPENAI_API_KEY=test-placeholder-not-a-real-key \
  TNR_REPO="$REPO" TNR_OUT="${TNR_OUT:-$HERE/results}" \
  TNR_NETWORK_ISOLATION="${TNR_NETWORK_ISOLATION:-unshare}" \
  python3 "$HERE/tools/offline_exec.py" "$@"
