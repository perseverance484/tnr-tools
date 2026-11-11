#!/usr/bin/env python3
"""Offline end-to-end test of pilot.py: a fake transcript holding one poll batch (AngelSaber R3, a logged state) must
produce the planner's pick as actions + the next poll + the tick, in one batch. No live calls.
Run: python3 tests/test_pilot.py"""
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "angelsaber_r3.txt")
BID = "TESTPILOT"


def fake_transcript(path, battle, entries):
    now = dt.datetime.now(dt.timezone.utc)
    rows = []
    for k, (ep, inp, data) in enumerate((("combat.getBattle", {"battleId": BID}, battle),
                                         ("combat.getBattleEntries", {"battleId": BID, "limit": 200}, entries))):
        ts = (now + dt.timedelta(seconds=k)).isoformat().replace("+00:00", "Z")
        rows.append({"timestamp": ts, "message": {"content": [{"type": "tool_use", "id": f"u{k}",
                     "name": "mcp__Tnr__callEndpoint", "input": {"endpointName": ep, "input": inp}}]}})
        rows.append({"timestamp": ts, "message": {"content": [{"type": "tool_result", "tool_use_id": f"u{k}",
                     "content": [{"type": "text", "text": json.dumps(data)}]}]}})
    with open(path, "w") as f:
        f.write("\n".join(json.dumps(r) for r in rows) + "\n")


def main():
    battle, ents = [json.loads(l) for l in open(FIX).read().splitlines() if l.strip()]
    n = len(ents["*.battleRound"])
    ents["*.id"] = [f"e{n - i}" for i in range(n)]
    with tempfile.TemporaryDirectory() as d:
        tp = os.path.join(d, "t.jsonl")
        fake_transcript(tp, battle, ents)
        out = subprocess.run([sys.executable, os.path.join(HERE, "pilot.py")], capture_output=True, text=True,
                             env=dict(os.environ, TNR_TRANSCRIPT=tp, TNR_PILOT_LIVE=os.path.join(d, "live"))).stdout.splitlines()
    want = subprocess.run([sys.executable, os.path.join(HERE, "turn.py"), FIX, "--battle", BID + "_ref", "--top", "1",
                           "--no-engine"], capture_output=True, text=True).stdout
    want_ids = [a["actionId"] for a in json.loads(want.split("FIRE: ", 1)[1].splitlines()[0])]
    batch = [json.loads(l) for l in out[1:]]
    acts = [b["input"]["actionId"] for b in batch if b.get("call") == "combat.performAction"]
    vers = [b["input"]["version"] for b in batch if b.get("call") == "combat.performAction"]
    print(out[0])
    assert "MY TURN" in out[0], out
    assert acts == want_ids, (acts, want_ids)
    assert vers == list(range(battle["battle.version"], battle["battle.version"] + len(acts))), vers
    assert [b.get("call") or "bash" for b in batch[len(acts):]] == ["combat.getBattle", "combat.getBattleEntries", "bash"]
    print("ok: pilot batch = planner pick + poll + tick")


if __name__ == "__main__":
    main()
