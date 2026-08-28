#!/usr/bin/env python3
"""
profile_derive.py - turn a mission capture into a ratification table.

The fifty AWAITING_RULING slots in 48_DATA_mission_profiles.json are not opinions waiting to
be invented; the live game already answers most of them. This reads the capture and reports,
per rank, what the existing missions actually do, so the ratification is a review of measured
behaviour rather than a blank form.

It proposes and never writes. Nothing here edits the profile: it prints a table and, with
--json, emits the same table as data. Balance and gating are supplied by dauntless, and a tool that
quietly filled fifty of them would be a tool that decided the mission family's difficulty.

What "proposal" means per field, and it differs by field on purpose:

  unanimous     every live mission of that rank agrees. The proposal is that value, and the
                confidence is real.
  dominant      one value holds a clear majority. Proposed, with the spread shown, because a
                majority is evidence and not a verdict.
  split         no value holds. NO proposal is made. A mean of a bimodal field is a number
                that describes none of the population, and printing one invites ratifying it.
  empty         the rank has no live missions to learn from. B and S have five and four
                records, so a thin rank is expected and is flagged rather than smoothed.

Graph shape is counted from `content.objectives` rather than from any stored field, since
objective_count, battle_nodes and enemies_per_battle only exist as facts about the graph.

    python3 profile_derive.py capture_missions_2026-08-26.json [--json out.json] [--selftest]
"""
from __future__ import annotations

import argparse
import collections
import json
import sys

BATTLE_TASKS = ("start_battle", "defeat_opponents")
QUEST_FIELDS = ("requiredLevel", "maxLevel", "maxAttempts", "maxCompletes",
                "retryDelay", "attemptDelay")
RANKS = ("D", "C", "B", "A", "S")
DOMINANT_SHARE = 0.6


def unwrap(payload, family: str = "mission") -> list:
    """Accept a builder results bundle, a bare family list, or a raw getAll envelope.

    The builder returns capture reads in its results bundle, so the shapes worth handling are
    the bundle's and the raw tRPC envelope's. Both are unwrapped rather than reshaped by hand,
    since a hand-reshaped capture is one where a filter can be introduced without a trace.
    """
    if isinstance(payload, dict):
        # Builder results bundle: capture reads keyed or listed by procedure.
        caps = payload.get("capture") or payload.get("captures")
        if caps is not None:
            rows = []
            entries = caps if isinstance(caps, list) else [
                dict(v, proc=k) if isinstance(v, dict) else v
                for k, v in (caps.items() if isinstance(caps, dict) else [])
            ]
            for c in entries:
                if not isinstance(c, dict):
                    continue
                if c.get("proc") and "quests.getAll" not in str(c.get("proc")):
                    continue
                inp = c.get("input") or {}
                if inp.get("questType") and inp["questType"] != family:
                    continue
                # v4.23 bundles put the response under `data`; `resp`/`response`/`result`
                # were assumed shapes and none of them is what the builder actually emits.
                rows += unwrap(c.get("resp") or c.get("response") or c.get("result")
                               or c.get("data") or {}, family)
            if rows:
                return rows
        if "families" in payload:
            return payload["families"].get(family, [])
        if "result" in payload and isinstance(payload["result"], dict):
            return unwrap(payload["result"], family)
        if "data" in payload:
            # `data` is the row array on a getAll result, but an intermediate wrapper in a
            # batch envelope (result.data.json.data). Recurse rather than assume the depth.
            if isinstance(payload["data"], list):
                return payload["data"]
            return unwrap(payload["data"], family)
        if "json" in payload:
            return unwrap(payload["json"], family)
    if isinstance(payload, list):
        # A batch envelope arrives as a list of numbered results.
        if payload and isinstance(payload[0], dict) and "result" in payload[0]:
            rows = []
            for part in payload:
                rows += unwrap(part, family)
            return rows
        return payload
    return []


def shape_of(quest: dict) -> dict:
    content = quest.get("content") or {}
    objectives = content.get("objectives") or []
    battles = [o for o in objectives if o.get("task") in BATTLE_TASKS]
    heads = []
    for o in battles:
        for spawn in (o.get("opponentAIs") or []):
            n = spawn.get("number")
            if isinstance(n, int):
                heads.append(n)
    return {
        "objective_count": len(objectives),
        "battle_nodes": len(battles),
        "enemies_per_battle": heads,
    }


def summarise(values: list) -> dict:
    """One field, one rank. Classification is the output; a bare mean is not."""
    present = [v for v in values if v is not None]
    if not present:
        return {"verdict": "empty", "n": 0}
    counts = collections.Counter(
        json.dumps(v, sort_keys=True) if isinstance(v, (list, dict)) else v for v in present
    )
    top, hits = counts.most_common(1)[0]
    share = hits / len(present)
    spread = {str(k): c for k, c in counts.most_common()}
    if len(counts) == 1:
        return {"verdict": "unanimous", "propose": top, "n": len(present), "spread": spread}
    if share >= DOMINANT_SHARE:
        return {"verdict": "dominant", "propose": top, "share": round(share, 2),
                "n": len(present), "spread": spread}
    numeric = [v for v in present if isinstance(v, (int, float))]
    out = {"verdict": "split", "n": len(present), "spread": spread}
    if numeric:
        # Range only. A mean across a split field is a value nothing in the population has.
        out["observed_range"] = [min(numeric), max(numeric)]
    return out


def derive(quests: list) -> dict:
    by_rank = collections.defaultdict(list)
    for q in quests:
        by_rank[q.get("questRank")].append(q)

    out = {"_source": {"records": len(quests),
                       "by_rank": {r: len(by_rank.get(r, [])) for r in RANKS}},
           "ranks": {}}

    for rank in RANKS:
        rows = by_rank.get(rank, [])
        block = {"n": len(rows), "quest": {}, "shape": {}}
        for field in QUEST_FIELDS:
            block["quest"][field] = summarise([q.get(field) for q in rows])

        shapes = [shape_of(q) for q in rows]
        block["shape"]["objective_count"] = summarise([s["objective_count"] for s in shapes])
        block["shape"]["battle_nodes"] = summarise([s["battle_nodes"] for s in shapes])
        heads = [n for s in shapes for n in s["enemies_per_battle"]]
        block["shape"]["enemies_per_battle"] = summarise(heads)
        # enemy_level_band cannot come from the quest at all: the quest holds AI ids, and the
        # levels live on the AI records. Named so it is not mistaken for an oversight.
        block["shape"]["enemy_level_band"] = {
            "verdict": "not_in_this_capture",
            "note": ("levels live on the AI records, not the quest. A profile.getAi capture of "
                     "the ids in opponentAIs answers it."),
            "ai_ids": sorted({i for q in rows for o in (q.get("content") or {}).get("objectives", [])
                              for spawn in (o.get("opponentAIs") or [])
                              for i in (spawn.get("ids") or [])}),
        }
        out["ranks"][rank] = block
    return out


def render(result: dict) -> str:
    lines = []
    src = result["_source"]
    lines.append(f"{src['records']} missions: " +
                 ", ".join(f"{r} {n}" for r, n in src["by_rank"].items()))
    for rank in RANKS:
        block = result["ranks"][rank]
        lines.append(f"\n--- {rank} (n={block['n']})")
        for group in ("quest", "shape"):
            for field, s in block[group].items():
                verdict = s["verdict"]
                if verdict in ("unanimous", "dominant"):
                    extra = f"  [{verdict}" + (f" {int(s['share']*100)}%]" if "share" in s else "]")
                    lines.append(f"  {field:20} {str(s['propose']):>12}{extra}")
                elif verdict == "split":
                    rng = s.get("observed_range")
                    lines.append(f"  {field:20} {'SPLIT':>12}  {s['spread']}"
                                 + (f"  range {rng}" if rng else ""))
                elif verdict == "empty":
                    lines.append(f"  {field:20} {'no data':>12}  [rank has no live missions]")
                else:
                    lines.append(f"  {field:20} {'n/a':>12}  {s.get('note', '')}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- selftest

FIXTURE = {"families": {"mission": [
    {"questRank": "D", "requiredLevel": 1, "maxLevel": 10, "maxAttempts": 3,
     "maxCompletes": 1, "retryDelay": "daily", "attemptDelay": "none",
     "content": {"objectives": [
         {"id": "a", "task": "dialog"},
         {"id": "b", "task": "defeat_opponents",
          "opponentAIs": [{"ids": ["ai1"], "number": 2}]}]}},
    {"questRank": "D", "requiredLevel": 1, "maxLevel": 10, "maxAttempts": 3,
     "maxCompletes": 1, "retryDelay": "daily", "attemptDelay": "none",
     "content": {"objectives": [
         {"id": "a", "task": "dialog"},
         {"id": "b", "task": "defeat_opponents",
          "opponentAIs": [{"ids": ["ai2"], "number": 2}]}]}},
    {"questRank": "D", "requiredLevel": 1, "maxLevel": 10, "maxAttempts": 3,
     "maxCompletes": 1, "retryDelay": "weekly", "attemptDelay": "none",
     "content": {"objectives": [{"id": "a", "task": "dialog"}]}},
    {"questRank": "C", "requiredLevel": 5, "maxLevel": 40, "maxAttempts": 1,
     "maxCompletes": 99, "retryDelay": "daily", "attemptDelay": "none",
     "content": {"objectives": [{"id": "a", "task": "dialog"}]}},
    {"questRank": "C", "requiredLevel": 30, "maxLevel": 40, "maxAttempts": 5,
     "maxCompletes": 99, "retryDelay": "daily", "attemptDelay": "none",
     "content": {"objectives": [{"id": "a", "task": "dialog"}]}},
]}}


def selftest() -> int:
    checks, failures = [], []

    def want(cond, label):
        checks.append(label)
        if not cond:
            failures.append(label)

    r = derive(unwrap(FIXTURE))
    d, c, s = r["ranks"]["D"], r["ranks"]["C"], r["ranks"]["S"]

    want(r["_source"]["records"] == 5, "every record counted")
    want(d["n"] == 3 and c["n"] == 2, "records bucketed by rank")

    want(d["quest"]["maxAttempts"]["verdict"] == "unanimous",
         "a field every record agrees on is unanimous")
    want(d["quest"]["maxAttempts"]["propose"] == 3, "unanimous field proposes that value")

    want(d["quest"]["retryDelay"]["verdict"] == "dominant",
         "2 of 3 clears the dominant threshold")
    want(d["quest"]["retryDelay"]["propose"] == "daily", "dominant proposes the majority value")
    want(d["quest"]["retryDelay"]["spread"] == {"daily": 2, "weekly": 1},
         "the spread is shown so a majority is not mistaken for consensus")

    want(c["quest"]["requiredLevel"]["verdict"] == "split", "a 1-1 tie is split, not dominant")
    want("propose" not in c["quest"]["requiredLevel"],
         "a split field proposes NOTHING rather than averaging")
    want(c["quest"]["requiredLevel"]["observed_range"] == [5, 30],
         "a split numeric field reports its range instead of a mean")

    want(s["quest"]["maxAttempts"]["verdict"] == "empty", "a rank with no records is empty")
    want(s["n"] == 0, "empty rank reported with n=0 rather than omitted")

    want(d["shape"]["objective_count"]["verdict"] == "dominant"
         and d["shape"]["objective_count"]["propose"] == 2,
         "objective count measured from the graph, not from a stored field")
    want(d["shape"]["battle_nodes"]["spread"] == {"1": 2, "0": 1},
         "battle nodes counted per record")
    want(d["shape"]["enemies_per_battle"]["propose"] == 2,
         "headcount read out of opponentAIs number")

    # Input shapes. The builder returns capture reads in its results bundle, and a bundle
    # carrying another family must not leak into the mission population.
    rows = FIXTURE["families"]["mission"]
    want(len(unwrap({"capture": [{"proc": "quests.getAll",
                                  "input": {"questType": "mission"},
                                  "resp": {"json": {"data": rows}}}]})) == 5,
         "builder results bundle unwraps")
    want(len(unwrap([{"result": {"data": {"json": {"data": rows}}}}])) == 5,
         "raw tRPC batch envelope unwraps at any depth")
    want(len(unwrap({"capture": [{"proc": "quests.getAll",
                                  "input": {"questType": "story"},
                                  "resp": {"json": {"data": rows}}}]})) == 0,
         "a read of another quest family does not leak into the mission set")

    band = d["shape"]["enemy_level_band"]
    want(band["verdict"] == "not_in_this_capture",
         "enemy level is named as absent rather than silently missing")
    want(band["ai_ids"] == ["ai1", "ai2"],
         "the AI ids needing a second capture are listed")

    for label in failures:
        print(f"  FAIL  {label}")
    print(f"\n{len(checks) - len(failures)} passed, {len(failures)} failed")
    return len(failures)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("capture", nargs="?")
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.capture:
        ap.error("a capture file is required")

    with open(args.capture) as fh:
        quests = unwrap(json.load(fh))
    if not quests:
        print("no mission records found in that capture")
        return 1

    result = derive(quests)
    print(render(result))
    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(result, fh, indent=1)
        print(f"\nwrote {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
