"""What the relays' batches cost, by the plan's count (live/tokens.jsonl; `python3 -m player.brain tokens`).

The plan's count (RUL-2026-11-13-156; docs/reviews/evidence/ai_player_hook_relay/PROOF.md, "What was run"): a tenth
of what was read from the cache, one and a quarter of what was written to it, the fresh input as it is and five
times the output, in fresh input tokens of the relay's model.

None of it is the cost of the session that starts the relays: that session's tokens are not in the file.
"""
import json
import os


def plan_count(row):
    """One row of tokens.jsonl by the plan's count. A row's `in` is the batch's whole input, what was read from
    the cache and written to it included (relay._usage), so the fresh part is what is left of it. Adding `in`
    itself counts the conversation twice: AP run 2's report did, and said 27,514 a batch where this says 4,930.
    A row that does not say what was cached counts its whole input as fresh, which is the most it can have been."""
    cached, written = row.get("cached") or 0, row.get("written") or 0
    fresh = max((row.get("in") or 0) - cached - written, 0)
    return 0.1 * cached + 1.25 * written + fresh + 5 * (row.get("out") or 0)


def _each(rows, of=plan_count):
    return round(sum(map(of, rows)) / len(rows)) if rows else None


def report(live):
    """The whole log: what a batch cost, in a fight and out of one, what that was made of, and how large the
    relays' conversations were."""
    try:
        with open(os.path.join(live, "tokens.jsonl"), encoding="utf8") as f:
            rows = [json.loads(line) for line in f if line.strip()]
    except (OSError, ValueError):
        rows = []
    if not rows:
        return {"batches": 0}
    total, calls = sum(map(plan_count, rows)), sum(r.get("calls") or 0 for r in rows)
    part = lambda key, weight: _each(rows, lambda r: weight * (r.get(key) or 0))
    return {"batches": len(rows), "batches_with_hooks": len([r for r in rows if r.get("hooks")]),
            "calls_carried": calls, "plan_total": round(total), "plan_per_batch": _each(rows),
            "plan_per_call": round(total / calls) if calls else None,
            "plan_per_fight_batch": _each([r for r in rows if r.get("battle")]),
            "plan_per_other_batch": _each([r for r in rows if not r.get("battle")]),
            "of_a_batch": {"read_from_cache": part("cached", 0.1), "written_to_cache": part("written", 1.25),
                           "output": part("out", 5)},
            "context_mean": part("context", 1), "context_max": max(r.get("context") or 0 for r in rows),
            "rows_without_cache_figures": len([r for r in rows if r.get("cached") is None])}
