#!/usr/bin/env python3
"""Skyglass go-live, the quest half (push/383-385): every hidden Skyglass / Crownhold quest re-sent WHOLE, once, with
`hidden: false`, its scene backgrounds as gameAsset ids and the scene characters the server's publish rule needs.

    python3 push/skyglass_publish_quests.gen.py

Zero live requests: every record is read from the manifest that last wrote it, with its literal ids from that run's
results bundle (L01). The non-quest go-live edits (items, dungeons, jutsu, battle assets) are the parent session's
push/390+, not built here.

383  the six chart runs (push/354, 355) and the two Steeping quests (push/356)
384  the six Haul raids (push/358)
385  Crownhold (push/373's record), Wreck Sighted (push/374's record) and the four hunts (push/339's Buried Cache,
     Drowned Foundry and Captain's Watch; push/382's Quarantined Archive)

What changes, and nothing else (each manifest's `_diff` lists every changed path; any other difference aborts):
- `hidden: false` (publishing; the hunts' base was sent without it).
- every URL `sceneBackground` becomes its Ghost Ship scene asset id (`skyglass_update.gen.py` SCENE_ASSET). A quest
  scene renders only as a gameAsset id (theninjarpg@3314d122 layout/Logbook.tsx ~486-525 -> gameAsset.getSceneAssets;
  a URL shows the default background). Empty values stay empty (the client falls back to the quest-level scene).
- the publish rule (routers/quests.ts ~866-880: a non-hidden save needs content.sceneCharacters, or one on EVERY
  objective): a quest that has neither gets the blank scene character as its quest-level `content.sceneCharacters`
  (director 2026-10-31: "Just use a blank character for Crownhold except for if there is a boss intro scene, use the
  Crowned Captain's for his scene"). An objective's own characters override the quest-level ones (Logbook.tsx ~491-498),
  so the hunts' existing portraits still show.
- Crownhold only: the Crowned Captain's portrait on his eight boss-intro dialogs (the intro and "echoes" dialog of each
  of the four routes into his fight).

Assets used (both exist; getSceneAssets does not filter `hidden`, queries/asset.ts listGameAssetForGetSceneAssets, so
neither needs an unhide):
- BLANK `1YXbXYW2wz3GETVMb6DT6` "Blank Scene Character" (folder ghostship, 512x512, 1.1 KB): the repository's
  registered blank suppressor (skills/producing-tnr-art/scripts/shotlist.py SUPPRESSOR_ASSET_IDS), already used this
  way by the Ghost Ship quests.
- CC_PORTRAIT `4Cu4EBaWRsGm5J_Ld1hTt` "Crowned Captain Portrait": push/90 renamed it and set its image to
  art/ghost_ship_skyglass/scene_char_ghost_ship_crowned_captain_portrait_b.webp (728x728, 1:1 bust, an accepted
  SCENE_CHARACTER aspect), VERIFIED in tnr_results_1791779642866.json.

Do not hand-edit the outputs.
"""
import copy
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "push"))
INBOX = "harvests/inbox/"
NUM = {"charts": 383, "haul": 384, "crownhold": 385}
BLANK = "1YXbXYW2wz3GETVMb6DT6"
CC_PORTRAIT = "4Cu4EBaWRsGm5J_Ld1hTt"
CROWNHOLD_ID = "fqqpkcp_L4oOsC6yyodlk"
CC_INTRO = [f"d5.n.{r}" for r in ("boss.clean", "boss.clean.echoes", "boss.alert", "boss.alert.echoes")] + [
    f"d5.n.protocol.b5.n.boss.{r}.{s}" for r in ("medical", "combat") for s in ("intro", "echoes")]


def load(name):
    s = importlib.util.spec_from_file_location(name.replace(".", "_"), os.path.join(ROOT, "push", name))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def jload(path):
    return json.load(open(os.path.join(ROOT, path)))


U = load("skyglass_update.gen.py")
F2 = load("skyglass_final_art2.gen.py")
SCENE_ASSET = U.SCENE_ASSET
# URL (or @img ref) -> scene key, from the hunts' SCENE table that every Skyglass quest generator draws from
# (skyglass_charts uses it directly; skyglass_haul's hold / lower_hull URLs and skyglass_steeping's hold are the same).
URL2KEY = {v: k for k, v in U.G.SCENE.items()}
assert set(URL2KEY.values()) == set(SCENE_ASSET), set(URL2KEY.values()) ^ set(SCENE_ASSET)


def created_ids(bundle):
    """srcId -> (id, name) for every ok quest create in a results bundle."""
    b = jload(bundle)
    return {e["srcId"]: (e["id"], e["name"]) for e in b["entries"]
            if e.get("entity") == "quest" and e.get("slot") == "create" and e.get("state") == "ok" and e.get("id")}


def resolve_scene(o, ids):
    if isinstance(o, list):
        return [resolve_scene(x, ids) for x in o]
    if isinstance(o, dict):
        return {k: resolve_scene(v, ids) for k, v in o.items()}
    if isinstance(o, str) and o.startswith("@scene:"):
        return ids[o.split(":", 1)[1]]
    return o


def scene_ids(bundle):
    return {e["srcId"]: e["id"] for e in jload(bundle)["entries"]
            if e.get("entity") == "asset" and e.get("state") == "ok" and e.get("srcId") and e.get("id")}


def to_asset(v, where):
    if not v or v in SCENE_ASSET.values() or not (v.startswith("http") or v.startswith("@")):
        return v
    if v not in URL2KEY:
        raise SystemExit(f"{where}: sceneBackground {v!r} has no scene asset")
    return SCENE_ASSET[URL2KEY[v]]


def publishable(c):
    return bool(c.get("sceneCharacters")) or all(o.get("sceneCharacters") for o in c["objectives"])


def publish(name, base, intro=None):
    """The base record with only the go-live changes; returns (data, changed paths)."""
    data = copy.deepcopy(base)
    c = data["content"]
    c["sceneBackground"] = to_asset(c.get("sceneBackground"), name)
    for o in c["objectives"]:
        if "sceneBackground" in o:
            o["sceneBackground"] = to_asset(o["sceneBackground"], f"{name}/{o['id']}")
    for oid, chars in (intro or {}).items():
        o = next(x for x in c["objectives"] if x["id"] == oid)
        assert o["task"] == "dialog" and not o.get("sceneCharacters"), (name, oid)
        o["sceneCharacters"] = list(chars)
    if not publishable(c):
        assert not c.get("sceneCharacters"), name
        c["sceneCharacters"] = [BLANK]
    data["hidden"] = False
    assert publishable(c), name
    changed = F2.diff_paths(base, data)
    intro_paths = {f"content.objectives[{i}].sceneCharacters" for i in (intro or {})}
    bad = [p for p in changed if not (p == "hidden" or p == "content.sceneCharacters" or p in intro_paths
                                      or p.endswith("sceneBackground"))]
    assert not bad, f"{name}: changes more than the go-live fields: {bad}"
    for p in changed:  # a sceneBackground change is always URL -> its asset id
        if p.endswith("sceneBackground"):
            assert get(data, p) in SCENE_ASSET.values() and URL2KEY.get(get(base, p)), (name, p)
    return data, changed


def get(d, path):
    for part in re.findall(r"[^.\[\]]+|\[[^\]]+\]", path):
        if part.startswith("["):
            k = part[1:-1]
            d = next(x for x in d if x.get("id") == k) if isinstance(d[0], dict) and "id" in d[0] else d[int(k)]
        else:
            d = d.get(part)
    return d


def summary(changed):
    out = {}
    for p in changed:
        k = "objectives[*].sceneBackground" if p.endswith("sceneBackground") and "objectives" in p else p
        k = "objectives[<intro>].sceneCharacters" if "objectives" in k and k.endswith("sceneCharacters") else k
        out[k] = out.get(k, 0) + 1
    return out


def img_pack(src_manifest, items):
    """The creating manifest's imagePack, restricted to the @img refs these items still carry."""
    used = set(re.findall(r'"@img:([^"]+)"', json.dumps(items)))
    if not used:
        return {}
    m = jload(src_manifest)
    files = {k: v for k, v in m["imagePack"]["files"].items() if k in used}
    assert set(files) == used, used - set(files)
    return {"imgSizes": {k: v["bytes"] for k, v in files.items()}, "imagePack": {"ref": m["imagePack"]["ref"], "files": files}}


def edit(target, name, data):
    return {"entity": "quest", "slot": "edit", "targetId": target, "name": name, "data": data}


def from_creates(manifest, bundle):
    ids = created_ids(bundle)
    out = []
    for it in jload(manifest)["items"]:
        assert it["entity"] == "quest" and it["slot"] == "create", it.get("name")
        qid, qname = ids[it["srcId"]]
        assert qname == it["name"] == it["data"]["name"], (it["srcId"], qname)
        assert it["data"]["hidden"] is True
        out.append((qid, it["name"], it["data"], manifest))
    return out


def write(num, slug, note, entries, packs_from):
    items, diffs = [], {}
    for qid, name, base, src, intro in entries:
        data, changed = publish(name, base, intro)
        items.append(edit(qid, f"{name}: publish (hidden false, scene assets)", data))
        diffs[f"{name} ({qid})"] = {"base": src, "changed_paths": len(changed), "by_field": summary(changed),
                                    "blank_scene_character": data["content"]["sceneCharacters"] == [BLANK]}
    m = {"_note": note + " Generated by push/skyglass_publish_quests.gen.py; do not hand-edit.", "dedupNames": True}
    for src in packs_from:
        p = img_pack(src, [i for i, e in zip(items, entries) if e[3] == src])
        if p:
            if "imagePack" in m:
                m["imgSizes"].update(p["imgSizes"]); m["imagePack"]["files"].update(p["imagePack"]["files"])
                # one pin for the merged pack: keep the first ref if it holds every file byte for byte
                ref = m["imagePack"]["ref"]
                for f in m["imagePack"]["files"].values():
                    b = subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{f['path']}"])
                    assert hashlib.sha256(b).hexdigest() == f["sha256"], (ref, f["path"])
            else:
                m.update(copy.deepcopy(p))
    m["_diff"] = diffs
    m["items"] = items
    path = os.path.join(ROOT, "push", f"{num}_{slug}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"push/{num}_{slug}.json: {len(items)} quests")
    for k, v in diffs.items():
        print(f"  {k}: {v['changed_paths']} paths {v['by_field']}")


def crownhold_base():
    """push/373's Crownhold (the live record), @scene refs resolved from 373's bundle. Asserted equal to what
    skyglass_final_art2.gen.py scenes_manifest() builds today (any other base erases the scenes and heal top-ups)."""
    captured = {}
    orig = F2.write
    F2.write = lambda num, slug, m: captured.update(m=m)
    try:
        F2.scenes_manifest()
    finally:
        F2.write = orig
    sent = next(i for i in jload("push/373_crownhold_scenes.json")["items"] if i["entity"] == "quest")
    regen = next(i for i in captured["m"]["items"] if i["entity"] == "quest")
    assert regen == sent and sent["targetId"] == CROWNHOLD_ID, "push/373 no longer matches its generator"
    return resolve_scene(sent["data"], scene_ids(INBOX + "tnr_results_1793489703304.json"))


def wreck_sighted_base():
    sent = next(i for i in jload("push/374_skyglass_wreck_sighted_salvager.json")["items"] if i["entity"] == "quest")
    assert sent["targetId"] == F2.WRECK_SIGHTED_ID
    return sent["targetId"], resolve_scene(sent["data"], scene_ids(INBOX + "tnr_results_1793489718055.json"))


def hunts():
    """push/339's three verified hunts (tnr_results_1793490827321.json) and push/382's Archive (the same record with
    literal scene ids; 339's Archive failed). If 382 has not run, this send is the Archive's go-live."""
    ok = {e["id"] for e in jload(INBOX + "tnr_results_1793490827321.json")["entries"]
          if e.get("entity") == "quest" and e.get("state") == "ok"}
    scenes = scene_ids(INBOX + "tnr_results_1793490827321.json")
    out = []
    for it in jload("push/339_skyglass_go_live.json")["items"]:
        if it["entity"] == "quest" and it["targetId"] in ok:
            out.append((it["targetId"], it["name"], resolve_scene(it["data"], scenes), "push/339_skyglass_go_live.json"))
    for it in jload("push/382_skyglass_go_live_archive_retry.json")["items"]:
        out.append((it["targetId"], it["name"], it["data"], "push/382_skyglass_go_live_archive_retry.json"))
    assert sorted(q[0] for q in out) == sorted(U.QUEST_ID.values()), [q[1] for q in out]
    for q in out:
        assert "hidden" not in q[2] and "@scene:" not in json.dumps(q[2]), q[1]
    return out


def main():
    charts = (from_creates("push/354_skyglass_chart_runs_common.json", INBOX + "tnr_results_1793485965044.json")
              + from_creates("push/355_skyglass_chart_runs_epic.json", INBOX + "tnr_results_1793485978739.json")
              + from_creates("push/356_skyglass_steeping.json", INBOX + "tnr_results_1793486134536.json"))
    write(NUM["charts"], "skyglass_publish_chart_runs", (
        f"push/{NUM['charts']}, GO-LIVE (quests 1 of 3): the six chart runs (push/354, 355) and the two Steeping quests "
        "(push/356) re-sent whole from the creates (= live), with hidden false, every URL sceneBackground replaced by its "
        "scene asset id, and the blank scene character as quest-level sceneCharacters (the publish rule, routers/quests.ts "
        "~866-880). _diff lists every changed path."),
        [q + (None,) for q in charts], ["push/356_skyglass_steeping.json"])
    haul = from_creates("push/358_skyglass_haul.json", INBOX + "tnr_results_1793486527004.json")
    write(NUM["haul"], "skyglass_publish_haul", (
        f"push/{NUM['haul']}, GO-LIVE (quests 2 of 3): the six Haul raids (push/358) re-sent whole from the creates "
        "(= live), with hidden false, the hold / lower_hull URL scenes replaced by their scene asset ids, and the blank "
        "scene character as quest-level sceneCharacters. _diff lists every changed path."),
        [q + (None,) for q in haul], ["push/358_skyglass_haul.json"])
    ws_id, ws = wreck_sighted_base()
    third = [(CROWNHOLD_ID, "Crownhold", crownhold_base(), "push/373_crownhold_scenes.json",
              {oid: [CC_PORTRAIT] for oid in CC_INTRO}),
             (ws_id, "Wreck Sighted", ws, "push/374_skyglass_wreck_sighted_salvager.json", None)]
    third += [q + (None,) for q in hunts()]
    write(NUM["crownhold"], "skyglass_publish_crownhold_hunts", (
        f"push/{NUM['crownhold']}, GO-LIVE (quests 3 of 3): Crownhold (push/373's record: scenes SC01-SC06 and heal "
        "top-ups kept) with the blank scene character quest-level and the Crowned Captain's portrait on his eight "
        "boss-intro dialogs; Wreck Sighted (push/374's record, the salvager kept) with its cache_site URL scene as its "
        "asset id; the four hunts (push/339 / push/382 records) with the blank scene character quest-level. All with "
        "hidden false. _diff lists every changed path."),
        third, ["push/339_skyglass_go_live.json", "push/382_skyglass_go_live_archive_retry.json"])


if __name__ == "__main__":
    main()
