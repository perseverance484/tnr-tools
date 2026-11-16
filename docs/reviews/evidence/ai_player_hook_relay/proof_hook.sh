#!/bin/sh
# One of the relay's hooks, for the proof: it fails on one of its runs, as told, and is the relay's own hook on
# the others.   proof_hook.sh WHICH NTH HOW COUNT
#   WHICH  bash, pre, post or fail: the hook it stands for (python3 -m player.hook WHICH)
#   NTH    the run of it that fails (0: none)
#   HOW    exit1: it ends with 1 and a line on standard error; sleep: it does nothing for 40 seconds;
#          look: it never fails, and writes down how large its input was and how that began (COUNT.seen)
#   COUNT  a file that keeps count of its runs
n=$(( $(cat "$4" 2>/dev/null || echo 0) + 1 ))
echo "$n" > "$4"
if [ "$n" = "$2" ]; then
  case "$3" in
    exit1) echo "the proof's hook fails here (run $n of $1)" >&2; exit 1 ;;
    sleep) sleep 40; exit 0 ;;
  esac
fi
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 1
if [ "$3" = look ]; then
  given=$(mktemp) && cat > "$given"
  python3 - "$given" "$4.seen" "$n" <<'PY'
import json, sys
text = open(sys.argv[1], encoding="utf8").read()
try:
    inp = json.loads(text)
    seen = {k: (v if len(json.dumps(v)) < 300 else json.dumps(v)[:300] + f" ... ({len(json.dumps(v))} characters)")
            for k, v in inp.items()}
except ValueError:
    seen = text[:300]
with open(sys.argv[2], "a", encoding="utf8") as f:
    f.write(json.dumps({"run": int(sys.argv[3]), "characters": len(text), "input": seen}) + "\n")
PY
  python3 -m player.hook "$1" < "$given"; code=$?
  rm -f "$given"
  exit $code
fi
exec python3 -m player.hook "$1"
