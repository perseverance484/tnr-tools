#!/usr/bin/env python3
"""Token figures for the gate run, from <live>/tokens.jsonl.
Usage: python3 token_report.py <repo_root>/state/player/dauntless/live
The plan's count (PROOF.md, RUL-2026-11-13-156): 0.1 x cache read + 1.25 x cache written + fresh input + 5 x output,
in fresh Haiku input tokens. Assumes "in" is fresh input and "cached"/"written" are cache read/write, as player/relay.py logs them;
check one line by hand against the relay's transcript before relying on it."""
import json, os, sys
live = sys.argv[1]
rows = [json.loads(l) for l in open(os.path.join(live, "tokens.jsonl")) if l.strip()]
def plan(r): return 0.1 * (r.get("cached") or 0) + 1.25 * (r.get("written") or 0) + (r.get("in") or 0) + 5 * (r.get("out") or 0)
hooked = [r for r in rows if r.get("hooks")]
fight = [r for r in rows if r.get("battle")]
tot = sum(plan(r) for r in rows); calls = sum(r.get("calls") or 0 for r in rows)
late = os.path.join(live, "hook", "late")
print(json.dumps({
  "batches": len(rows), "batches_with_hooks": len(hooked), "game_calls_carried": calls,
  "plan_count_total": round(tot), "plan_count_per_batch": round(tot / len(rows)) if rows else None,
  "plan_count_per_call": round(tot / calls) if calls else None,
  "plan_count_per_fight_batch": round(sum(plan(r) for r in fight) / len(fight)) if fight else None,
  "max_context": max((r.get("context") or 0) for r in rows) if rows else None,
  "files_in_hook_late": len(os.listdir(late)) if os.path.isdir(late) else 0,
  "proof_reference": "PROOF.md: 4,200-4,400 a batch (one-message form), estimate 97-98% under the pre-hook live relay",
}, indent=1))
