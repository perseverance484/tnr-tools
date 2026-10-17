#!/usr/bin/env python3
"""
push/93: repair Sentinel's failed final edit from push/90, renamed Guardian (RUL-2026-10-12-014).

    python3 push/93_ghost_ship_guardian_repair.gen.py           # write push/93 json
    python3 push/93_ghost_ship_guardian_repair.gen.py --check   # regenerate in memory, compare

What happened (harvests/inbox/tnr_results_1791779642866.json):
- push/90 item 29 renamed AI 3V_gdHYaclMB1gTyOPAbV to "Sentinel". The server refused it with
  Duplicate entry 'Sentinel' for key 'UserData.UserData_username_key': another live AI owns the name.
- updateAi syncs the kit before the userData update, so the new kit landed anyway.
- Name, statsMultiplier 5, avatar and rules did not land.
- The other 49 records completed.

What this emits, and nothing else:
1. The push/90 Sentinel edit, with:
   - username "Guardian";
   - the @img avatar resolved to the URL push/90 already uploaded;
   - every other key identical to push/90 item 29.
2. Both quest edits from push/90:
   - with @refs resolved through the run's idmap;
   - proved equal to the live after-capture before any change (0 differences);
   - then exactly the 8 objective lines that name the boss changed from "Sentinel" to "Guardian".

Inputs are pinned by SHA-256, so the build is deterministic. push/90 and its design state are
spent release history and are not edited. This file owns the rename.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "push/93_ghost_ship_guardian_repair.json"
REPORT = "state/ghost_ship_guardian_repair_report.json"
P90 = "push/90_ghost_ship_skyglass_release.json"
P90_SHA = "6b72054282be6a904f409333afcdf6b013e8d0c4654977d863d208d64804b0c7"
RESULTS = "harvests/inbox/tnr_results_1791779642866.json"

SENTINEL = "3V_gdHYaclMB1gTyOPAbV"
QUEST_IDS = ["6Ri-W5TtUrEMWpyYlnf_F", "HckXVOf-qk6ESU9t5rxLh"]
OLD_NAME, NEW_NAME = "Sentinel", "Guardian"
# The objective lines that name the boss, per quest (state/ghost_ship_retheme_patch.json objectiveText).
RENAMED_OBJECTIVES = ["d_guardian", "b_guardian", "r_dig", "d_claim_A"]
REF_RE = re.compile(r"^@(ai|item|scene|img):(.+)$")


def fail(msg: str) -> None:
    sys.exit(f"REFUSED: {msg}")


def load(rel: str, want_sha: str | None = None):
    raw = open(os.path.join(ROOT, rel), "rb").read()
    if want_sha and hashlib.sha256(raw).hexdigest() != want_sha:
        fail(f"{rel} sha256 {hashlib.sha256(raw).hexdigest()} != pinned {want_sha}")
    return json.loads(raw)


def resolve(o, idmap: dict, used: set):
    if isinstance(o, dict):
        return {k: resolve(v, idmap, used) for k, v in o.items()}
    if isinstance(o, list):
        return [resolve(v, idmap, used) for v in o]
    if isinstance(o, str):
        m = REF_RE.match(o)
        if m:
            if m.group(2) not in idmap:
                fail(f"{o} not in the push/90 run idmap")
            used.add(o)
            return idmap[m.group(2)]
    return o


def diffs(sent, live, path=""):
    """Forge-style asserted diff: every key sent must equal live."""
    if isinstance(sent, dict):
        if not isinstance(live, dict):
            return [path]
        return [d for k in sent for d in (diffs(sent[k], live[k], f"{path}/{k}") if k in live else [f"{path}/{k}"])]
    if isinstance(sent, list):
        if not isinstance(live, list) or len(sent) != len(live):
            return [path]
        return [d for i, (a, b) in enumerate(zip(sent, live)) for d in diffs(a, b, f"{path}/{i}")]
    return [] if sent == live else [path]


def build() -> tuple[dict, dict]:
    p90 = load(P90, P90_SHA)
    results = load(RESULTS)
    idmap = results["idmap"]
    after = {(c["proc"], json.dumps(c["input"], sort_keys=True)): c["data"]
             for c in results["captures"] if c["phase"] == "after" and c.get("data")}

    # The failure this repairs, exactly as recorded.
    ent = next((e for e in results["entries"] if e.get("id") == SENTINEL and e.get("entity") == "ai" and e.get("state") == "error"), None)
    if not ent or "Duplicate entry 'Sentinel'" not in json.dumps(ent):
        fail("results do not record the Sentinel duplicate-name failure this manifest repairs")
    items = p90["items"]
    src = [i for i, e in enumerate(items) if e["entity"] == "ai" and e.get("targetId") == SENTINEL and e["phase"] == 6]
    if src != [29]:
        fail(f"push/90 Sentinel final edit is at {src}, expected [29]")

    used: set = set()
    # 1. Sentinel -> Guardian.
    ai = copy.deepcopy(items[29])
    ai["data"] = resolve(ai["data"], idmap, used)
    if ai["data"]["username"] != OLD_NAME:
        fail("push/90 item 29 username is not Sentinel")
    ai["data"]["username"] = NEW_NAME
    # Everything but the name and the resolved avatar is push/90 item 29 verbatim, so the push/90 STATS
    # proof (harness/ghost_ship_final, multiplier 5 -> 1.3M / 400k) and rule parse carry over unchanged.
    changed = sorted(k for k in set(ai["data"]) | set(items[29]["data"]) if ai["data"].get(k) != items[29]["data"].get(k))
    if changed != ["avatar", "username"] or ai["data"]["statsMultiplier"] != 5:
        fail(f"Guardian payload departs from push/90 item 29 at {changed}")
    live_ai = after[("profile.getAi", json.dumps({"userId": SENTINEL}))]
    live_kit = sorted(uj["jutsuId"] for uj in live_ai["jutsus"])
    if live_kit != sorted(ai["data"]["jutsus"]):
        fail(f"live kit {live_kit} != push/90 kit; the partial-apply premise no longer holds")
    ai["name"] = "Guardian (was Ghostly Guardian; push/90 rename to Sentinel refused): rename, rules, avatar, multiplier 5, kit re-sent"

    # 2. Quests: resolve, prove equal to live, then rename exactly the boss lines.
    quests, renamed = [], []
    for qid in QUEST_IDS:
        src_q = [e for e in items if e["entity"] == "quest" and e.get("targetId") == qid]
        if len(src_q) != 1:
            fail(f"push/90 has {len(src_q)} edits of quest {qid}")
        q = copy.deepcopy(src_q[0])
        q["data"] = resolve(q["data"], idmap, used)
        live = after[("quests.get", json.dumps({"id": qid}))]
        d = diffs(q["data"], live)
        if d:
            fail(f"quest {qid}: resolved push/90 data differs from the live after-capture at {d[:5]}")
        by = {o["id"]: o for o in q["data"]["content"]["objectives"]}
        for oid in RENAMED_OBJECTIVES:
            text = by[oid]["description"]
            if len(re.findall(rf"\b{OLD_NAME}\b", text)) != 1:
                fail(f"{qid}/{oid}: expected exactly one '{OLD_NAME}' in {text!r}")
            by[oid]["description"] = re.sub(rf"\b{OLD_NAME}\b", NEW_NAME, text)
            renamed.append(f"{qid}/{oid}")
        left = re.findall(rf"\b{OLD_NAME}\b", json.dumps(q["data"]))
        if left:
            fail(f"quest {qid}: {len(left)} '{OLD_NAME}' left outside the enumerated lines")
        q["name"] = q["name"].replace(": Skyglass retheme + 83-node expansion", ": boss text Sentinel -> Guardian (re-sends the live push/90 quest)")
        quests.append(q)
    if len(renamed) != 8:
        fail(f"renamed {len(renamed)} lines, expected 8")

    reads = ([{"proc": "profile.getAi", "input": {"userId": SENTINEL}, "persist": "full"}]
             + [{"proc": "quests.get", "input": {"id": qid}, "persist": "full"} for qid in QUEST_IDS])
    return {
        "_note": ("Ghost Ship push/93: Guardian repair (RUL-2026-10-12-014). Generated by "
                  "push/93_ghost_ship_guardian_repair.gen.py; do not hand-edit. Re-sends push/90's failed Sentinel "
                  "final edit as \"Guardian\", and the two live quests with the 8 boss lines renamed. "
                  "No creates, no uploads; both quests stay hidden:true. Run by the operator only, Forge 0.5.2."),
        "dedupNames": True,
        "items": [ai] + quests,
        "capture": {"before": reads, "after": copy.deepcopy(reads)},
    }, {
        "schema": "tnr.repair_manifest_report", "ruling": "RUL-2026-10-12-014", "manifest": OUT,
        "push90": {"path": P90, "sha256": P90_SHA},
        "results": {"path": RESULTS, "sha256": hashlib.sha256(open(os.path.join(ROOT, RESULTS), "rb").read()).hexdigest()},
        "failure": ent["detail"],
        "resolvedRefs": {r: idmap[r.split(":", 1)[1]] for r in sorted(used)}, "renamedObjectives": renamed,
        "questsEqualLiveBeforeRename": True, "liveKitEqualsSentKit": True,
        "aiKeysChangedFromPush90": ["avatar (resolved @img)", "username"],
    }


def main() -> int:
    doc, report = build()
    text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    report["manifestSha256"] = hashlib.sha256(text.encode()).hexdigest()
    rtext = json.dumps(report, indent=1, ensure_ascii=False) + "\n"
    if "--check" in sys.argv[1:]:
        for rel, want in ((OUT, text), (REPORT, rtext)):
            path = os.path.join(ROOT, rel)
            if not os.path.exists(path) or open(path, encoding="utf-8").read() != want:
                print(f"STALE: {rel} differs from the generator", file=sys.stderr)
                return 1
        print(f"OK: {OUT} and {REPORT} reproduce ({len(doc['items'])} items, sha256 {report['manifestSha256']})")
        return 0
    for rel, t in ((OUT, text), (REPORT, rtext)):
        with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as fh:
            fh.write(t)
    print(f"wrote {OUT} + {REPORT}: {len(doc['items'])} items, refs resolved {len(report['resolvedRefs'])}, "
          f"lines renamed {len(report['renamedObjectives'])}, sha256 {report['manifestSha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
