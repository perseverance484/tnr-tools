#!/usr/bin/env python3
"""Skyglass: the six Haul quests (The Trophy Hold, The Bone Store, The Snare Room, The Overgrown Stores, The Ore Vault,
The Bloom Cellar). All HIDDEN.

    python3 push/skyglass_haul.gen.py --copies <344 bundle> [--copies <bundle> ...] [--keymap <keys.json>]
        -> push/358_skyglass_haul.json   (6 quest creates; needs push/344's results for the guards' ids)

Run order: 344 (rebuilt) -> build 358 -> gates -> run 358. Not committed before 344 has run (L01: the guards' ids are
literal). Independent of push/356-357 (steeping).

Graph: state/skyglass_build/haul_spec.json `graphs` (the 6ad2a102 fit; the graphs are identical on
fable/skyglass-rule-cap, which changes only guard rule gates). Each choice node is a dialog; its options go to a
battle (win -> next node, loss -> `fail`), straight on (cut through), or to the `win_r<n>` ending for the haul
(leave). Endings pay the profession chests as plain reward_items at 100% (SKYGLASS_THE_HAUL.md "Payout"). Text:
SKYGLASS_TEXT.md section 3 (read verbatim; step lines, tags, alertness and pending lines, battle lines, rung endings,
hazard lines 3.8).

Rulings applied over the spec:
  * RUL-2026-10-31-073: the guards are NOT scaled (`opponent_scaled_to_user: false`; the spec says true). The Veteran
    tier is a fixed level-100 record.
  * RUL-2026-10-29-052 / RUL-2026-10-31-072 F11: the spec's `gate` (huntingRank / gatheringRank S RANK) is dropped;
    the generator refuses to emit any profession-rank field.
  * RUL-2026-10-31-067: guards resolve by AI key (push/skyglass_aikeys.py): one Veteran record per crew member; the
    spec's separate steps 4-5 and lookout copies map onto that crew member's Veteran (see HAUL_KEYS).
  * Chart-run shape (loot tables 5): isolated Battle Pyramid, the page is the entry item (spent at start), health and
    chakra carry, a lost/drawn/fled fight fails the run.
Reversible placeholders (not ruled; reported): questRank A (the Rare chart runs' rank; no rank gate is ruled for the
Haul, only the profession gate was removed), scene `hold` for hunter pages and `lower_hull` for gatherer pages (both
are the Haul's scenes, RUL-2026-10-30-061 item 7; the split is a proposal), maxAttempts/maxCompletes 100 (as the live
chart runs; F04 not addressed).

Do not hand-edit the output.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "push"))
import skyglass_text as T  # noqa: E402
import skyglass_aikeys as K  # noqa: E402

NUM = 358
PFX = "sg358_"
SPEC = os.path.join(ROOT, "state/skyglass_build/haul_spec.json")
BUNDLE_329 = os.path.join(ROOT, "harvests/inbox/tnr_results_1793424666625.json")  # push/329 results (the pages)
NAMES = os.path.join(ROOT, "answers/names_item.json")
EXP = "art/skyglass_event_icons/exports/"
SCENE = {"hunter": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJTdaBvI5IU29dZYJPoOKSh5vmlqatMub3EigH",  # hold
         "gatherer": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ0pHtoKgrYldRWJcD6vE10SjNsXHeA9pVMfQi"}  # lower_hull

# haul_spec record -> AI key (RUL-2026-10-31-067: one Veteran per crew member serves the Haul)
HAUL_KEYS = {
    "haul-h-wayfinder": "veteran:wayfinder",
    "haul-h-blade": "veteran:first-blade",
    "haul-h-veteran": "veteran:first-blade",
    "haul-h-warden": "veteran:deck-warden",
    "haul-h-lookout": "veteran:deck-warden",
    "haul-g-warden": "veteran:deck-warden",
    "haul-g-lookout": "veteran:deck-warden",
    "haul-g-sentinel": "veteran:skyglass-sentinel",
    "haul-g-veteran": "veteran:skyglass-sentinel",
    "haul-h-keeper": "veteran:arsenal-keeper",
    "haul-g-sealwright": "veteran:sealwright",
    "haul-trophy-warden": "oneoff:trophy-warden",
    "haul-stores-ward": "oneoff:stores-ward",
    "haul-g-charge": "copy:seal-charge-haul",
    "haul-g-canister": "copy:core-canister-haul",
}

# spec variant -> (329 srcId of the page, icon export (push/352), text: (table heading, after), (bullets from, to))
PAGES = {
    "trophy": ("sg329_page_trophy", "icon-ledger-page.webp", ("### 3.3", None), ("### 3.3", "### 3.4")),
    "bone": ("sg329_page_bone", "icon-ledger-page-bone-store.webp", ("### 3.4", None), ("### 3.4", "### 3.5")),
    "snare": ("sg329_page_snare", "icon-ledger-page-snare-room.webp", ("### 3.5", None), ("### 3.5", "### 3.6")),
    "overgrown": ("sg329_page_overgrown", "icon-stores-manifest.webp", ("### 3.6", None), ("### 3.6", "### 3.7")),
    "vault": ("sg329_page_vault", "icon-stores-manifest-ore-vault.webp",
              ("### 3.7", "**`quest:The Ore Vault.description`**"),
              ("**`quest:The Ore Vault.description`**", "**`quest:The Bloom Cellar.description`**")),
    "bloom": ("sg329_page_bloom", "icon-stores-manifest-bloom-cellar.webp",
              ("### 3.7", "**`quest:The Bloom Cellar.description`**"),
              ("**`quest:The Bloom Cellar.description`**", "### 3.8")),
}
SHARED = {"failDescription": "You are defeated.", "drawDescription": "The fight stalls, and the chart's way closes.",
          "fleeDescription": "You break away, and the way back closes behind you."}  # text doc section 2 shared lines
RANK_FIELDS = ("huntingRank", "gatheringRank", "medicalRank")


# ---------------------------------------------------------------------------------------------------------------
# text (SKYGLASS_TEXT.md section 3, verbatim)
# ---------------------------------------------------------------------------------------------------------------
BULLET = re.compile(r"^- \*\*([^*]+?):?\*\*(?:\s*\([^)]*\))?:?\s*`([^`]*)`\s*$")


def bullets(start, end):
    L = T.lines()
    i = next(i for i, l in enumerate(L) if l.startswith(start))
    j = next(j for j in range(i + 1, len(L)) if L[j].startswith(end))
    out = {}
    for l in L[i:j]:
        m = BULLET.match(l)
        if m:
            label = m.group(1).rstrip(":")
            assert label not in out, label
            out[label] = m.group(2)
    return out


def page_text(variant, prof):
    _, _, (head, after), (b0, b1) = PAGES[variant]
    rows = T.table(head, after)
    steps = {}
    for r in rows:
        n = int(r[0])
        steps[n] = {"line": r[1], "crate": r[2], "locker": None if r[3] == "—" else r[3],
                    "cut": None if r[4] == "—" else r[4]}
    assert sorted(steps) == [1, 2, 3, 4, 5], (variant, sorted(steps))
    b = bullets(b0, b1)
    need = ["Alertness 1-2", "Alertness 3+", "Crate battle", "Locker battle", "Locker battle, alertness 3+"]
    missing = [k for k in need if k not in b]
    assert not missing, (variant, missing)
    return steps, b


def shared_text():
    b = bullets("### 3.1", "### 3.2")
    rung_rows = T.table("### 3.1", "**Ending text by rung**")
    rungs = {}
    for r in rung_rows:
        lo, hi = (int(x) for x in r[0].split("-"))
        for n in range(lo, hi + 1):
            rungs[n] = {"hunter": r[1], "gatherer": r[2]}
    hz = bullets("### 3.8", "---")
    return {"leave": b["Leave option"],
            "pending": {"hunter": b["Pending line, hunters"], "gatherer": b["Pending line, gatherers"]},
            "fail": {"hunter": b["`fail.description`, hunters"], "gatherer": b["`fail.description`, gatherers"]},
            "rungs": rungs,
            "maxpools": {"hunter": hz_line("hunters"), "gatherer": hz_line("gatherers")},
            "success": T.block("quest:<page>.successDescription")}


def hz_line(who):
    L = T.lines()
    i = next(i for i, l in enumerate(L) if l.startswith("### 3.8"))
    for l in L[i:]:
        m = re.match(r"^- " + who + r": `([^`]*)`\s*$", l)
        if m:
            return m.group(1)
        if l.startswith("---"):
            break
    raise KeyError(f"3.8 {who} line")


# ---------------------------------------------------------------------------------------------------------------
def git(*a):
    return subprocess.check_output(["git", "-C", ROOT, *a], text=True).strip()


def image_pack(files):
    paths = [EXP + f for f in files]
    ref = git("log", "-1", "--format=%H", "HEAD", "--", *paths)
    if not ref:
        sys.exit("icon exports not committed")
    out = {}
    for p in paths:
        disk = open(os.path.join(ROOT, p), "rb").read()
        if subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{p}"]) != disk:
            sys.exit(f"{p}: working copy differs from {ref}")
        out[os.path.basename(p)] = {"path": p, "sha256": hashlib.sha256(disk).hexdigest(), "bytes": len(disk)}
    return {"ref": ref, "files": out}


def item_names():
    return {r[0]: r[1] for r in json.load(open(NAMES))["rows"]}


def band(alertness):
    return 0 if alertness == 0 else (1 if alertness <= 2 else 2)


def build_quest(variant, g, R, pages, names, S):
    prof = g["quest"]
    assert prof in ("hunter", "gatherer")
    page_src, icon, _, _ = PAGES[variant]
    page_id, page_name = pages[page_src]
    assert page_name == g["chart"], (variant, page_name, g["chart"])
    steps, B = page_text(variant, prof)
    scene = {"sceneBackground": SCENE[prof], "sceneCharacters": []}
    objs = []
    battles = {b["id"]: b for b in g["battles"]}
    used_battles = set()
    for n in g["nodes"]:
        st = steps[n["step"]]
        parts = [st["line"]]
        if band(n["alertness"]) == 1:
            parts.append(B["Alertness 1-2"])
        elif band(n["alertness"]) == 2:
            parts.append(B["Alertness 3+"])
        if n["pending"]:
            parts.append(S["pending"][prof])
        choices = []
        for o in n["options"]:
            c = o["choice"]
            if c == "leave":
                assert o["text"] == S["leave"], o
                choices.append({"text": S["leave"], "nextObjectiveId": o["next"]})
                continue
            text = st[c]
            if not text:
                raise SystemExit(f"{variant} step {n['step']}: the spec offers {c} but the text doc has no {c} tag")
            nxt = o["battle"] if o.get("fight") else o["next"]
            if o.get("fight"):
                used_battles.add(o["battle"])
            choices.append({"text": text, "nextObjectiveId": nxt})
        tg = [c["nextObjectiveId"] for c in choices]
        assert len(tg) == len(set(tg)), (n["id"], tg)
        objs.append({"id": n["id"], "task": "dialog", "description": "<br><br>".join(parts), **scene,
                     "nextObjectiveId": choices})
    assert used_battles == set(battles), (variant, set(battles) ^ used_battles)
    for b in g["battles"]:
        if b["kind"] == "crate":
            line = B["Crate battle"]
        else:
            line = B["Locker battle, alertness 3+"] if b["alertBand"] == 2 else B["Locker battle"]
        counts = {}
        for a in b["opponent_ai"]:
            key = HAUL_KEYS[a["ids"][0]]
            lit = R(key)
            counts[lit] = counts.get(lit, 0) + a["number"]
        debuffs = []
        for d in b["applyDebuffs"]:
            d = dict(d)
            if d["type"] == "decreasemaxpools":
                d["description"] = S["maxpools"][prof]  # text 3.8 split
            debuffs.append(d)
        o = {"id": b["id"], "task": "start_battle", "description": line, **scene,
             "opponentAIs": [{"ids": [i], "number": c, "quantity": 1} for i, c in counts.items()],
             "completionOutcome": "Win", "scaleGains": 1, "keepOriginalPools": False,
             "opponent_scaled_to_user": False,  # RUL-2026-10-31-073 (the spec's true is superseded)
             "nextObjectiveId": b["nextObjectiveId"], "failObjectiveId": b["failObjectiveId"], **SHARED}
        if debuffs:
            o["applyDebuffs"] = debuffs
        objs.append(o)
    for e in g["endings"]:
        if e["task"] == "fail_quest":
            objs.append({"id": e["id"], "task": "fail_quest", "description": S["fail"][prof], **scene})
            continue
        assert e["task"] == "win_quest"
        ri = []
        for r in e["reward_items"]:
            cid = r["ids"][0]
            if names.get(cid) != r["name"]:
                raise SystemExit(f"{variant} {e['id']}: chest {cid} is {names.get(cid)!r} in answers, not {r['name']!r}")
            if r["number"] != 100:
                raise SystemExit(f"{variant} {e['id']}: a chest at {r['number']}% (the fitted ladder pays at 100%)")
            ri.append({"ids": [cid], "number": 100, "quantity": r["quantity"]})
        objs.append({"id": e["id"], "task": "win_quest", "description": S["rungs"][e["rung"]][prof], **scene,
                     "reward_items": ri})
    ids = [o["id"] for o in objs]
    assert len(ids) == len(set(ids)) and ids[0] == g["start"], variant
    assert len(objs) == g["counts"]["objectives"] and len(objs) < 90, (variant, len(objs))  # RUL-2026-10-29-044 item 8
    page = g["page"]
    data = {"name": page, "description": T.block(f"quest:{page}.description"), "successDescription": S["success"],
            "image": "@img:" + icon, "questType": "battlepyramid", "questRank": "A", "hidden": True,
            "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True,
            "requiredLevel": 1, "maxLevel": 100, "maxAttempts": 100, "maxCompletes": 100,
            "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None,
            "startsAt": None, "endsAt": None,
            "content": {"objectives": objs, "sceneBackground": SCENE[prof], "sceneCharacters": [],
                        "entryItems": [{"ids": [page_id], "number": 1}], "isolated": True, "reward": {}}}
    blob = json.dumps(data)
    assert not any(f'"{f}"' in blob for f in RANK_FIELDS), f"{variant}: a profession rank gate (F11)"
    assert '"opponent_scaled_to_user": true' not in blob, variant
    return {"entity": "quest", "slot": "create", "srcId": PFX + variant, "phase": 1, "name": page, "data": data}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--copies", action="append", default=[], help="push/344 results bundle (repeatable)")
    ap.add_argument("--keymap", help="JSON {AI key: literal id} overriding the bundle lookup")
    a = ap.parse_args()
    if not a.copies and not a.keymap:
        ap.error("--copies <344 bundle> (or --keymap) is required: the guards' ids come from push/344")
    spec = json.load(open(SPEC))
    assert set(spec["records"]) == set(HAUL_KEYS), set(spec["records"]) ^ set(HAUL_KEYS)
    R = K.Resolver(a.copies, a.keymap)
    pages = {}
    for e in json.load(open(BUNDLE_329))["entries"]:
        if e.get("srcId") and e.get("state") == "ok" and e.get("id"):
            pages[e["srcId"]] = (e["id"], e["name"])
    names, S = item_names(), shared_text()
    assert S["fail"]["hunter"] and S["fail"]["gatherer"], S["fail"]
    items = [build_quest(v, spec["graphs"][v], R, pages, names, S) for v in PAGES]
    pack = image_pack([p[1] for p in PAGES.values()])
    m = {"_note": (
        f"push/{NUM}, HIDDEN. The six Haul quests (SKYGLASS_THE_HAUL.md; graphs from state/skyglass_build/haul_spec.json, "
        "6ad2a102 fit): isolated Battle Pyramids entered with their page (push/329 items), up to 5 steps of crate / "
        "locker / cut through / leave, endings pay Hunter's or Gatherer's Chests. Guards fixed at level 100, not "
        "scaled (RUL-2026-10-31-073); no profession rank gate (RUL-2026-10-29-052, F11). Guards by AI key from "
        f"{', '.join(R.bundles) or 'keymap'} (_aiKeys). Placeholders: questRank A, scenes hold/lower_hull. "
        "Generated by push/skyglass_haul.gen.py; do not hand-edit."),
        "dedupNames": True, "_aiKeys": R.used,
        "imgSizes": {k: v["bytes"] for k, v in pack["files"].items()}, "imagePack": pack, "items": items}
    path = os.path.join(ROOT, f"push/{NUM}_skyglass_haul.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{NUM}_skyglass_haul.json: {len(items)} quests, "
          f"{sum(len(i['data']['content']['objectives']) for i in items)} objectives")


if __name__ == "__main__":
    main()
