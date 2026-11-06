#!/usr/bin/env python3
"""Skyglass story pass (RUL-2026-11-05-117; docs/design/SKYGLASS_STORY_AUDIT.md): the live-record edits. Zero live requests.

    python3 push/skyglass_story_pass.gen.py
        -> push/483_skyglass_story_crownhold.json   Crownhold quest text + Replicant Zero renamed The First Impression
        -> push/484_skyglass_story_runs.json        The Quarantined Archive and The Fall quest text
        -> push/485_skyglass_story_shards.json      the four Invitation shards' story lines

The text is owned elsewhere and only carried here:
- Crownhold: push/crownhold.gen.py (OVERRIDE, STORY_PASS, PROSE). Each node's new text is taken from its quest()
  output; the build stops unless exactly the story-pass nodes differ from the live record and every other node matches.
- The Quarantined Archive: state/skyglass_hunts/hunts.py. The Fall: docs/design/SKYGLASS_TEXT.md section 2.4. Each
  replacement must occur once in the live record, and its new text must be present in the owner.
- Shards: push/skyglass_uber_economy.gen.py (SHARDS, THUMBPRINT, shard_desc); the drop and invitation lines must be
  unchanged from the live text.

Live records: Crownhold and The Fall from push/420 (tnr_results_1793718972517.json, VERIFIED), the Archive from push/385
(tnr_results_1793492929044.json, VERIFIED), the shards from push/417 (tnr_results_1793716872408.json; 419 only unhid
them, 468 only changed their icons). No later manifest in push/ edits these records. Quests are re-sent whole (quest
edits do not fetch-merge); live Battle Pyramids abandon any open run on a content change, so run outside event hours.

Do not hand-edit the output.
"""
import copy
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULING = "RUL-2026-11-05-117"


def load(name, path):
    s = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def jload(path):
    return json.load(open(os.path.join(ROOT, path)))


def die(msg):
    raise SystemExit("skyglass_story_pass: " + msg)


def live_item(manifest, target):
    hits = [i for i in jload(manifest)["items"] if i.get("targetId") == target]
    if len(hits) != 1:
        die(f"{target} not found once in {manifest}")
    return copy.deepcopy(hits[0])


def choices(o):
    return [c.get("text") for c in o.get("nextObjectiveId", []) if isinstance(c, dict)]


def write(num, slug, note, items, diff):
    m = {"_note": note, "dedupNames": True, "_diff": diff, "items": items}
    p = os.path.join(ROOT, "push", f"{num}_{slug}.json")
    with open(p, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{num}_{slug}.json: {len(items)} items")


# ---------------------------------------------------------------------------------------------------------------
# 483 Crownhold
# ---------------------------------------------------------------------------------------------------------------
CROWNHOLD = "fqqpkcp_L4oOsC6yyodlk"
REPLICANT_ZERO_AI = "vjEFUJ9mb1zNTuQf4lfXv"  # state/crownhold/ids.json @ai:D3.BOSS (push/272, VERIFIED)
CROWNHOLD_NODES = {  # audit R2, R5, R6 (+ D2), R7, R8, R9, R13a, R13c; D3 the First Impression
    "d3.n.f1", "d3.n.f2", "d3.n.f3", "d3.n.terminal", "d3.n.boss.clean", "d3.n.boss.alert", "b3.n.boss.clean",
    "b3.n.boss.alert", "b3.n.boss.medical", "b3.n.boss.combat", "d4.n.f1", "d4.n.f3", "d5.n.f3", "d5.n.boss.clean",
    "d5.n.boss.alert", "d.aftermath"}


def crownhold():
    cg = load("crownhold_gen", "push/crownhold.gen.py")
    gen = {o["id"]: o for o in cg.quest()["data"]["content"]["objectives"]}
    q = live_item("push/420_skyglass_uber_shard_drops.json", CROWNHOLD)
    objs = q["data"]["content"]["objectives"]
    if {o["id"] for o in objs} != set(gen):
        die("Crownhold: live and generated node sets differ")
    changed = []
    for o in objs:
        g = gen[o["id"]]
        if choices(g) != choices(o) or any(g.get(f) != o.get(f) for f in ("failDescription", "drawDescription",
                                                                           "fleeDescription")):
            die(f"Crownhold {o['id']}: choices or battle lines differ from the generator")
        if g["description"] != o["description"]:
            changed.append(o["id"])
            o["description"] = g["description"]
    if set(changed) != CROWNHOLD_NODES:
        die(f"Crownhold: changed nodes {sorted(set(changed) ^ CROWNHOLD_NODES)} differ from the story pass")
    if "Replicant" in json.dumps(q):
        die("Crownhold: Replicant Zero still named")
    q["name"] = f"Crownhold: story pass ({RULING})"
    rename = {"entity": "ai", "slot": "edit", "targetId": REPLICANT_ZERO_AI,
              "name": f"Replicant Zero -> {cg.FIRST_IMPRESSION} (username only)",
              "data": {"username": cg.FIRST_IMPRESSION}}
    diff = {"Crownhold": [f"content.objectives[{n}].description" for n in changed],
            "AI vjEFUJ9mb1zNTuQf4lfXv": ["username: Replicant Zero -> The First Impression"]}
    write(483, "skyglass_story_crownhold", (
        f"push/483, Skyglass story pass 1 of 3 ({RULING}; docs/design/SKYGLASS_STORY_AUDIT.md). Item 1: the Crownhold "
        "AI Replicant Zero renamed The First Impression (username only; Forge fetch-merges the live kit; updateAi "
        "rescales stats on the write, law 71; a bare multi-word title like The Second, RUL-2026-10-26-003; if the name "
        "is refused as taken, law 66, stop and report: the fix is a new name). Item 2: Crownhold (live, PUBLISHED) "
        "re-sent whole from push/420 with 16 node descriptions from push/crownhold.gen.py: the aftermath no longer "
        "frees the echoes and the glass rings beneath the throne; the register's same night and three unmarked names; "
        "the Glasswright brought back the First Impression; the siege ring on High Command's maps; the Silence came up "
        "out of the mountain; the Crowned Captain's crack of doubt; glass hall and drill scroll. Nothing else changes "
        "(_diff). A content edit abandons open runs: run outside event hours. Generated by "
        "push/skyglass_story_pass.gen.py; do not hand-edit."), [rename, q], diff)


# ---------------------------------------------------------------------------------------------------------------
# 484 The Quarantined Archive and The Fall
# ---------------------------------------------------------------------------------------------------------------
ARCHIVE, FALL = "-bZ_ZoI6yrUJ_LKT9R5zm", "H9YInJtnzKCOEMv-sNgzP"
ARCHIVE_IMG = ("@img:icon-chart-quarantined-archive.webp",  # push/385 run idmap (tnr_results_1793492929044.json)
               "https://ui0arpl8sm.ufs.sh/f/pDUTNFUKXRIPMj5umfUsn.webp")
GLASSWRIGHT_REPORT = ("<br><br>The last report is addressed to no officer, only to 'the Glasswright', and it was never "
                      "sent. It asks one thing: who are they holding still for?")
RUNS = [  # (target, manifest, owner file, [(node, field, old, new)])
    (ARCHIVE, "push/385_skyglass_publish_crownhold_hunts.json", "state/skyglass_hunts/hunts.py", [
        ("d_records", "description", "'Refused. None is relieved.'", "'Refused. None is relieved.'" + GLASSWRIGHT_REPORT),
        ("d_entry", "choice", "Read the suppressed incident reports", "Read the buried reports"),
    ]),
    (FALL, "push/420_skyglass_uber_shard_drops.json", "docs/design/SKYGLASS_TEXT.md", [
        ("w_press", "description", "\"It was done a long time ago.\"", "\"We were called home. I only held the heading.\""),
    ]),
]


def runs():
    items, diff = [], {}
    for target, manifest, owner, edits in RUNS:
        q = live_item(manifest, target)
        objs = {o["id"]: o for o in q["data"]["content"]["objectives"]}
        own = open(os.path.join(ROOT, owner)).read()
        base = q["data"]["name"]
        for node, field, old, new in edits:
            if new.replace("\"", "") not in own.replace("\\\"", "").replace("\"", ""):
                die(f"{base} {node}: the owner {owner} does not carry the new text")
            o = objs[node]
            if field == "choice":
                hit = [c for c in o["nextObjectiveId"] if c.get("text") == old]
                if len(hit) != 1:
                    die(f"{base} {node}: choice {old!r} not found once")
                hit[0]["text"] = new
            else:
                if o[field].count(old) != 1:
                    die(f"{base} {node}: {old!r} not found once")
                o[field] = o[field].replace(old, new)
            diff.setdefault(base, []).append(f"content.objectives[{node}].{field}")
        s = json.dumps(q)
        if ARCHIVE_IMG[0] in s:
            q = json.loads(s.replace(ARCHIVE_IMG[0], ARCHIVE_IMG[1]))
        if "@img:" in json.dumps(q):
            die(f"{base}: an unresolved @img reference")
        q["name"] = f"{base}: story pass ({RULING})"
        items.append(q)
    write(484, "skyglass_story_runs", (
        f"push/484, Skyglass story pass 2 of 3 ({RULING}). The Quarantined Archive (live record push/385; its quest icon "
        "sent as the literal URL push/385 resolved) gains the unsent report to the Glasswright on d_records, and its "
        "d_entry choice reads 'Read the buried reports'; The Fall (live record push/420) closes on the Captain's \"We "
        "were called home. I only held the heading.\" Both re-sent whole; nothing else changes (_diff). Live, PUBLISHED "
        "chart runs: a content edit abandons open runs, so run outside event hours. Generated by "
        "push/skyglass_story_pass.gen.py; do not hand-edit."), items, diff)


# ---------------------------------------------------------------------------------------------------------------
# 485 Shards
# ---------------------------------------------------------------------------------------------------------------
SHARD_IDS = {"keel": "uKnlqlfyE_k1QjLuaVml_", "crown": "4UNvgWIDGD9QpNVtLr1aM", "tide": "KHGZAfQFosLQJ29AN2ymC",
             "ledger": "cGrmhfe88ACBvFk2XqvSu"}  # push/417 run idmap (tnr_results_1793716872408.json)


def shards():
    ue = load("uber_economy", "push/skyglass_uber_economy.gen.py")
    live = {i["srcId"]: i["data"]["description"] for i in jload("push/417_skyglass_uber_economy.json")["items"]
            if i.get("entity") == "item" and i.get("srcId", "").startswith(ue.PFX)}
    items, diff = [], {}
    for key, name, story, drop in ue.SHARDS:
        new, old = ue.shard_desc(story, drop), live[ue.PFX + key]
        if new.split("</i>", 1)[1] != old.split("</i>", 1)[1]:
            die(f"{name}: the drop or invitation lines changed")
        items.append({"entity": "item", "slot": "edit", "targetId": SHARD_IDS[key],
                      "name": f"{name}: story line ({RULING})", "data": {"description": new}})
        diff[name] = ["description (story line)"]
    write(485, "skyglass_story_shards", (
        f"push/485, Skyglass story pass 3 of 3 ({RULING}). Description-only edits on the four live Invitation shards "
        "(push/417): each story line gains the Glasswright's thumbprint, and the Shard of the Tide's line now covers "
        "both run families it drops from (the reliquary's echoes and the night of the fall). Drop and invitation lines "
        "unchanged. Generated by push/skyglass_story_pass.gen.py; do not hand-edit."), items, diff)


if __name__ == "__main__":
    crownhold()
    runs()
    shards()
