#!/usr/bin/env python3
"""Add an observation-only rule probe to the EXPORTED engine copy's ai_v2.ts.

performAIaction does not report which profile rule produced the action. This inserts one
optional global callback, invoked after a rule's action has already been performed, with the
rule's index. It changes no control flow, reads no randomness and writes no state.
`main.ts --probe-check` re-runs seeds with the hook absent and asserts identical outcomes.

Usage: apply_probe.py <exported app dir>. Idempotent; fails if anchors are missing.
Never run against the user's game checkout (refuses a path containing a .git directory).
"""
import os
import sys

app = sys.argv[1]
root = os.path.dirname(os.path.abspath(app))
if os.path.exists(os.path.join(app, ".git")) or os.path.exists(os.path.join(root, ".git")):
    raise SystemExit("refusing: target looks like a git checkout; use a git-archive export")
path = os.path.join(app, "src/libs/combat/ai_v2.ts")
src = open(path).read()
MARK = "/* TNR_SKYGLASS_RULE_PROBE */"
if MARK in src:
    print("probe already applied")
    sys.exit(0)
a1 = "    for (const rule of aiProfile?.rules ?? []) {\n"
b1 = f"    {MARK} let __probeRuleIdx = -1;\n    for (const rule of aiProfile?.rules ?? []) {{\n      __probeRuleIdx += 1;\n"
a2 = "        if (check.canAct && result) {\n"
b2 = (
    "        if (check.canAct && result) {\n"
    "          (globalThis as { __TNR_RULE_PROBE__?: (p: unknown) => void }).__TNR_RULE_PROBE__?.({\n"
    "            userId: user.userId, ruleIndex: __probeRuleIdx, actionId: nextAction.action.id,\n"
    "            ruleType: rule.action.type, totalRules: aiProfile?.rules.length ?? 0,\n"
    "          });\n"
)
for a in (a1, a2):
    if src.count(a) != 1:
        raise SystemExit(f"anchor not found exactly once: {a!r}")
src = src.replace(a1, b1).replace(a2, b2)
open(path, "w").write(src)
print("probe applied to", path)
