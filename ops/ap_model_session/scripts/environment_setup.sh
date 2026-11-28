#!/bin/bash
# tnr-tools environment setup: put the tnr-relay agent where Claude Code loads it at session start.
mkdir -p ~/.claude/agents
SRC=""
for d in "$PWD" /home/user/tnr-tools "$HOME/tnr-tools" "$PWD/tnr-tools"; do
  if [ -f "$d/.claude/agents/tnr-relay.md" ]; then SRC="$d/.claude/agents/tnr-relay.md"; break; fi
done
if [ -n "$SRC" ]; then
  cp "$SRC" ~/.claude/agents/tnr-relay.md && echo "tnr-relay copied from $SRC"
else
  curl -fsSL https://raw.githubusercontent.com/perseverance484/tnr-tools/main/.claude/agents/tnr-relay.md -o ~/.claude/agents/tnr-relay.md \
    && echo "tnr-relay fetched from main" || echo "WARNING: tnr-relay.md not found and not fetched"
fi
ls -l ~/.claude/agents/tnr-relay.md
