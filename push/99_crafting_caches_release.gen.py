#!/usr/bin/env python3
"""
Build push/99: crafting caches release step B (RUL-2026-10-13-001..004, D10 (b)).

    python3 push/99_crafting_caches_release.gen.py           # write push/99 json
    python3 push/99_crafting_caches_release.gen.py --check   # rebuild in memory and compare

This generator never contacts the game. It reads committed captures only:

  base     push/98 results (harvests/inbox/tnr_results_1791903144042.json): fresh full reads of both live
           Ghost Ship quests and the three caches push/97 created hidden.
  checks   push/96 results (tnr_results_1791864463120.json): the quests must be unchanged since then.
           push/97 manifest and results (tnr_results_1791902993422.json): the cache ids and loot tables.

What it emits, in one manifest:
  phase 1  three item edits: hidden -> false (Medicine Inro, Shinobi Tool Pouch, Sage's Strongbox).
           Item edits fetch-merge, so only `hidden` is sent.
  phase 8  two quest edits (Gather, Hunt) shaped exactly like push/94's: content, description, hidden,
           image, name, successDescription, all taken from the live push/98 row. The only change is
           three reward lines appended to the restricted vault objective w_B2:
               Medicine Inro 15%, Shinobi Tool Pouch 15%, Sage's Strongbox 7.5%, quantity 1.
           `hidden` is carried as the LIVE value (false). Both quests are published, and push/94's own
           `hidden: true` must never be copied forward.

It refuses unless:
  - push/98 completed and every read succeeded;
  - each quest row equals its push/96 row, and the top-level key set is unchanged (upstream drift guard);
  - w_B2 exists exactly once per quest and still holds its four known lines;
  - each cache row is hidden, carries the push/97 name and loot table, and has exactly one effect;
  - the emitted quest content differs from the live content only at w_B2.reward_items, by the three lines,
    after omitting rewardMode / rewardPickCount / allyAIs, which hold server defaults (see SERVER_DEFAULTS_*).
Then it runs Forge check_manifest.mjs (must pass) and validate.py (the doctrine way). Every validate.py
line must fall in an allowed class; any other line refuses and needs a ruling.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "push", "99_crafting_caches_release.json")
P98 = os.path.join(ROOT, "harvests/inbox/tnr_results_1791903144042.json")
P96 = os.path.join(ROOT, "harvests/inbox/tnr_results_1791864463120.json")
P97_RESULTS = os.path.join(ROOT, "harvests/inbox/tnr_results_1791902993422.json")
P97 = os.path.join(ROOT, "push/97_crafting_caches_create.json")

QUESTS = {"6Ri-W5TtUrEMWpyYlnf_F": "Ghost Ship (Gather)", "HckXVOf-qk6ESU9t5rxLh": "Ghost Ship (Hunt)"}
VAULT = "w_B2"
# The vault's existing lines, per quest (push/90 shipped them; push/96 and push/98 confirm).
VAULT_BEFORE = {
    "6Ri-W5TtUrEMWpyYlnf_F": [("gb6vxdzWTYZR--7s-4kTX", 55, 1), ("SWQpaXB8csJWL3zZMTz4r", 25, 1),
                              ("c5dUPtXmCedfKssqiwbpt", 25, 1), ("c5dUPtXmCedfKssqiwbpt", 25, 1)],
    "HckXVOf-qk6ESU9t5rxLh": [("KwgjMOya2XT6uYsgXbsh6", 55, 1), ("M-0CPw9yBmmreLvJU6gav", 25, 1),
                              ("c5dUPtXmCedfKssqiwbpt", 25, 1), ("c5dUPtXmCedfKssqiwbpt", 25, 1)],
}
# RUL-2026-10-13-003: chance per vault clear, quantity 1.
CACHES = [
    ("crafting_cache_medicine_inro", "Medicine Inro", 15),
    ("crafting_cache_shinobi_tool_pouch", "Shinobi Tool Pouch", 15),
    ("crafting_cache_sages_strongbox", "Sage's Strongbox", 7.5),
]
QUEST_FIELDS = ["content", "description", "hidden", "image", "name", "successDescription"]  # push/94 shape

# Keys the live rows carry but Forge's pinned contract does not know (its pre-send validator refuses them).
# The server fills each with this default when it is absent, at both 641040531 and 922d61bb:
#   validators/rewards.ts questRewardModeFields: rewardMode .prefault("all"), rewardPickCount .prefault(1);
#   validators/objectives.ts allyAIsField .prefault([]).
# push/94 sent content without them, and its after-read came back with exactly these values, verdict match.
# So they are omitted ONLY when the live value equals the default. Any other value refuses.
SERVER_DEFAULTS_CONTENT = {"rewardMode": "all", "rewardPickCount": 1}
SERVER_DEFAULTS_OBJECTIVE = {"allyAIs": []}


def fail(msg: str) -> None:
    sys.exit("refusing: " + msg)


def load(path: str) -> dict:
    return json.load(open(path, encoding="utf-8"))


def canon(v) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"))


def reads(bundle: dict, label: str) -> dict:
    if bundle.get("outcome") != "success" or bundle.get("state") != "DONE":
        fail(f"{label} is {bundle.get('outcome')}/{bundle.get('state')}, not success/DONE")
    out = {}
    for c in bundle["captures"]:
        if c.get("proc") in ("quests.get", "item.get"):
            if not c.get("ok") or not isinstance(c.get("data"), dict) or c["data"].get("id") != c["input"]["id"]:
                fail(f"{label} read {c['proc']} {c['input']} did not return its record")
            out[c["input"]["id"]] = c["data"]
    return out


def diff_paths(a, b, path=""):
    if type(a) is not type(b):
        return [path or "/"]
    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            out += diff_paths(a.get(k), b.get(k), f"{path}/{k}") if (k in a and k in b) else [f"{path}/{k}"]
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [path]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff_paths(x, y, f"{path}/{i}")
        return out
    return [] if a == b else [path]


def build() -> dict:
    live = reads(load(P98), "push/98")
    before = reads(load(P96), "push/96")

    # Cache ids and loot tables come from push/97: its manifest and its verified results.
    r97 = load(P97_RESULTS)
    ids = {e["srcId"]: e["id"] for e in r97["entries"] if e.get("verdict") == "match" and e.get("state") == "ok"}
    sent = {it["srcId"]: it["data"] for it in load(P97)["items"]}
    lines_new = []
    for src, name, chance in CACHES:
        cid = ids.get(src)
        if not cid:
            fail(f"push/97 results do not record a verified create for {src}")
        row = live.get(cid)
        if not row or row.get("name") != name:
            fail(f"push/98 did not read {name} ({cid})")
        if row.get("hidden") is not True:
            fail(f"{name} is no longer hidden; step B assumes it is still hidden")
        if len(row.get("effects") or []) != 1:
            fail(f"{name} does not carry exactly one effect")
        if canon(row["effects"][0].get("reward_items")) != canon(sent[src]["effects"][0]["reward_items"]):
            fail(f"{name}'s live loot table differs from push/97")
        lines_new.append({"ids": [cid], "number": chance, "quantity": 1})

    items = []
    for src, name, _ in CACHES:
        items.append({"entity": "item", "slot": "edit", "phase": 1, "targetId": ids[src], "name": name,
                      "data": {"hidden": False}})

    for qid, qname in QUESTS.items():
        row, old = live.get(qid), before.get(qid)
        if not row or row.get("name") != qname:
            fail(f"push/98 did not read {qname}")
        if not old or sorted(row) != sorted(old):
            fail(f"{qname}: the top-level field set changed since push/96 (upstream contract drift?)")
        moved = diff_paths(old, row)
        if moved:
            fail(f"{qname} changed since push/96 at {moved[:8]}; re-review before step B")
        vault = [o for o in row["content"]["objectives"] if o.get("id") == VAULT]
        if len(vault) != 1:
            fail(f"{qname} has {len(vault)} {VAULT} objectives, expected 1")
        have = [(r["ids"][0], r["number"], r.get("quantity")) for r in vault[0]["reward_items"]]
        if have != VAULT_BEFORE[qid] or any(len(r["ids"]) != 1 for r in vault[0]["reward_items"]):
            fail(f"{qname} {VAULT} reward lines are {have}, not the known four")
        if any(r["ids"][0] in ids.values() for r in vault[0]["reward_items"]):
            fail(f"{qname} {VAULT} already carries a cache line")

        content = copy.deepcopy(row["content"])
        for k, dv in SERVER_DEFAULTS_CONTENT.items():
            if k in content:
                if content[k] != dv:
                    fail(f"{qname} content.{k} is {content[k]!r}, not the server default {dv!r}; omitting it would change it")
                del content[k]
        for o in content["objectives"]:
            for k, dv in SERVER_DEFAULTS_OBJECTIVE.items():
                if k in o:
                    if o[k] != dv:
                        fail(f"{qname} objective {o.get('id')} {k} is {o[k]!r}, not the server default {dv!r}")
                    del o[k]
        tgt = next(o for o in content["objectives"] if o.get("id") == VAULT)
        tgt["reward_items"] = tgt["reward_items"] + copy.deepcopy(lines_new)
        idx = next(i for i, o in enumerate(content["objectives"]) if o.get("id") == VAULT)
        stripped = copy.deepcopy(row["content"])
        for k in SERVER_DEFAULTS_CONTENT:
            stripped.pop(k, None)
        for o in stripped["objectives"]:
            for k in SERVER_DEFAULTS_OBJECTIVE:
                o.pop(k, None)
        changed = diff_paths(stripped, content)
        if changed != [f"/objectives/{idx}/reward_items"]:
            fail(f"{qname}: emitted content differs from live beyond {VAULT}.reward_items: {changed}")
        data = {k: copy.deepcopy(row[k]) for k in QUEST_FIELDS}
        data["content"] = content
        if data["hidden"] is not False:
            fail(f"{qname} is not live (hidden={data['hidden']}); step B was ruled for live quests")
        items.append({"entity": "quest", "slot": "edit", "phase": 8, "targetId": qid, "name": qname, "data": data})

    note = ("Crafting caches release step B (RUL-2026-10-13-001..004, D10 (b)). (1) Unhides the three caches "
            "push/97 created and verified: Medicine Inro " + ids["crafting_cache_medicine_inro"] + ", Shinobi Tool "
            "Pouch " + ids["crafting_cache_shinobi_tool_pouch"] + ", Sage's Strongbox " + ids["crafting_cache_sages_strongbox"]
            + ". (2) Adds them to the restricted vault (w_B2) of both LIVE Ghost Ship quests at 15% / 15% / 7.5%, "
            "quantity 1. Each quest is reproduced from the push/98 live read, push/94 field shape, hidden kept FALSE "
            "(live). The only content change is the three appended w_B2 lines. Generated by "
            "push/99_crafting_caches_release.gen.py; do not hand-edit.")
    return {"_note": note, "dedupNames": True, "items": items}


# Allowed validate.py diagnostic classes. Anything else refuses. These are the classes RUL-2026-10-12-015
# approved for push/94 on these same live quests. They are inherited from the live records; this edit
# introduces neither. Running push/99 needs its own release-specific ruling (decision D13).
ALLOWED = {
    # d_parley is the live riddle (two wrong answers -> duel); d_recon_test's wrong seals -> approved lockout.
    "approved_shared_menu_target": re.compile(
        r"^ERROR\s+\[quest:Ghost Ship \((Gather|Hunt)\)\]\.(d_parley|d_recon_test): two or more options in this menu share a target"),
    # b_K8qdNI651fTsRn9tfkk is gs_char_sealwright, created by push/90; the answers snapshot predates it.
    "stale_snapshot_scene_character": re.compile(
        r"^warn\s+lint Ghost Ship \((Gather|Hunt)\): T1 law 49: objective d_sealwright sceneCharacters 'b_K8qdNI651fTsRn9tfkk'"),
}


def gates(path: str) -> dict:
    f = subprocess.run(["node", os.path.join(ROOT, "forge/tools/check_manifest.mjs"), path],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if f.returncode != 0:
        sys.exit("forge check_manifest failed:\n" + f.stdout)
    v = subprocess.run([sys.executable, "../scripts/validate.py", os.path.abspath(path)],
                       cwd=os.path.join(ROOT, "skills/building-tnr-content/data"),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    counts, unknown = {}, []
    for line in v.stdout.splitlines():
        line = line.strip()
        if not re.match(r"^(ERROR|warn)\b", line):
            continue
        cls = next((k for k, rx in ALLOWED.items() if rx.match(line)), None)
        if cls:
            counts[cls] = counts.get(cls, 0) + 1
        else:
            unknown.append(line)
    if unknown:
        sys.exit(f"validate.py produced {len(unknown)} diagnostics outside the allowed classes:\n" + "\n".join(unknown))
    return counts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    text = json.dumps(build(), indent=1, ensure_ascii=False) + "\n"
    if a.check:
        if not os.path.exists(OUT) or open(OUT, encoding="utf-8").read() != text:
            print(f"{OUT} is stale; rerun without --check", file=sys.stderr)
            return 1
        print(f"push/99 current; gates: {gates(OUT)}")
        return 0
    tmp = OUT + ".tmp.json"
    open(tmp, "w", encoding="utf-8").write(text)
    try:
        counts = gates(tmp)
    except SystemExit:
        # Never leave a rejected manifest in push/: the builder picker lists every .json there.
        os.remove(tmp)
        raise
    os.replace(tmp, OUT)
    print(f"wrote push/99: 3 item unhides + 2 live quest edits; gates: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
