#!/usr/bin/env python3
"""The Flooded Stores: build manifest for the Isonade fight and the looting crew (records only).

Reads the two harness specs, exactly as engine-tested:
  isonade_spec.json  (isonade.ts --write-spec)       Isonade, the Grasping Arm, 18 jutsu
  stores_spec.json   (stores_main.ts --spec-out)     6 crew AI records, 10 jutsu (fs-* only)
and the nine animation strips in ../art/isonade_anims.

Writes manifests/1_strips_and_jutsu.json .. 4_ais.json. NOT pushed and not cleared to push: every stage needs the
director's go.

Stages (law 17: AI jutsus arrays and summon aiIds must be literal ids, so each stage after the first is regenerated
with --bundle=<results bundle> from the stages before it, whose idmap gives srcId -> created id):
  1  asset + jutsu creates   the 9 animation strips (@img: uploads) and every new jutsu except the two summons
  2  AI creates              the two summoned bodies (Grasping Arm, Deckhand from the Hold)
  3  jutsu creates           the two summon jutsu (they name the summoned AI)
  4  AI creates              Isonade and the five crew

Every create is hidden. Ids are the harness placeholders behind a prefix (srcId fsb_<id>).
Usage: python3 flooded_stores_build.gen.py [--bundle=<results.json> ...]   (needs the game checkout for tag descriptions)
"""
import copy
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the strips sit beside the build in the project files (../art/isonade_anims) and in the repo at art/isonade_anims
ART = next(d for d in (os.path.join(HERE, "..", "art", "isonade_anims"), os.path.join(os.environ.get("TNR_REPO", "/home/user/tnr-tools"), "art", "isonade_anims")) if os.path.isdir(d))
REPO = os.environ.get("TNR_REPO", "/home/user/tnr-tools")
GAME = os.environ.get("TNR_ENGINE_SRC", "/root/isowork/game/tnr")
GAME_PIN = "3314d122c93e036618483d18229a793ad7ad21fd"
PFX = "fsb_"
sys.path.insert(0, os.path.join(REPO, "skills/building-tnr-content/scripts"))
os.chdir(os.path.join(REPO, "skills/building-tnr-content/data"))
from factory import Factory  # noqa: E402

F = Factory()
BUNDLES = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--bundle=")]
# --hosted=<uploaded.json>: the strips already sit on the director's UploadThing (state/isonade_upload, the
# isonade-uploadthing workflow), so stage 1 creates point at those URLs and runs over the connector (mcp_run refuses
# @img uploads). Each URL is checked against the strip's sha256 before it is used.
HOSTED = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--hosted=")), None)
ISO = json.load(open(os.path.join(HERE, "isonade_spec.json")))
STO = json.load(open(os.path.join(HERE, "stores_spec.json")))

# Shared Skyglass marks (state/skyglass_fx/asset_ids.json): harness token -> (tile, glint), as push/skyglass_library.gen.py.
FX = json.load(open(os.path.join(REPO, "state/skyglass_fx/asset_ids.json")))["assets"]
MARK_FX = {
    "tg_heavy": (FX["Skyglass Mark - Heavy (tile)"], FX["Skyglass Mark - Heavy (glint)"]),
    "tg_safe": (FX["Skyglass Mark - Safe (tile)"], FX["Skyglass Mark - Safe (floating emblem)"]),
}
# anim_fx_undertow_v1 is live already: the AN09 undertow strip created by Forge job 412 (srcId sg412_an09_undertow).
LIVE_ANIM = {"anim_fx_undertow_v1": "3vKPSGqmwtJn1by7Uk1Ii"}

# The nine new strips (frames from art/isonade_anims/README.md; every strip 128 px frames, 50 ms).
STRIPS = {
    "anim_isonade_body_water_v1": ("Isonade - Body Water (loop)", 32),
    "anim_isonade_slam_v1": ("Isonade - Slam (hit)", 14),
    "anim_isonade_brine_v1": ("Isonade - Brine Pool (loop)", 24),
    "anim_isonade_arm_burst_v1": ("Isonade - Arm Burst (appear)", 16),
    "anim_isonade_arm_lash_v1": ("Isonade - Arm Lash (hit)", 10),
    "anim_isonade_surge_v1": ("Isonade - Black Water (hit)", 24),
    "anim_isonade_eye_v1": ("Isonade - Open Eye (loop)", 16),
    "anim_isonade_bite_v1": ("Isonade - Bite of the Ship (appear)", 20),
    "anim_isonade_rot_drip_v1": ("Isonade - Rot Drip (loop)", 24),
}
FOLDER = "SkyglassIsonade"

# Jutsu names must be unique in the live catalog (a duplicate saves as a blank shell), and the harness
# reuses "Slam" / "Black Water" for its mark and strike halves. Library precedent: "Omen: X" marks the
# telegraph, the strike carries the plain name. PLACEHOLDER names: the director's call.
NAMES = {
    "iso-slam-mark-a": "Isonade Omen: Slam I", "iso-slam-a": "Isonade Slam I", "iso-slam-a-bitten": "Isonade Slam I, Bitten",
    "iso-slam-mark-b": "Isonade Omen: Slam II", "iso-slam-b": "Isonade Slam II", "iso-slam-b-bitten": "Isonade Slam II, Bitten",
    "iso-slam-mark-c": "Isonade Omen: Slam III", "iso-slam-c": "Isonade Slam III", "iso-slam-c-bitten": "Isonade Slam III, Bitten",
    "iso-black-water-mark-75": "Isonade Omen: Black Water I", "iso-black-water-mark-50": "Isonade Omen: Black Water II",
    "iso-black-water-mark-25": "Isonade Omen: Black Water III", "iso-black-water": "Isonade Black Water",
    "iso-undertow": "Isonade Undertow", "iso-grasping-arm-rises": "Grasping Arm Rises", "iso-it-rises": "It Rises",
}
# AI usernames are unique across all players and AIs: the summoned copy cannot share "Looting Deckhand".
USERNAMES = {"fs-looting-deckhand-hold": "Deckhand from the Hold"}

# Donor avatars the harness carries as @img refs, with their hosted URLs (harvests/inbox idmaps, e.g. tnr_results_1794615376220).
PLACEHOLDER_AVATARS = {"avatar_crownhold_arakane.webp": "https://ui0arpl8sm.ufs.sh/f/fGSVwTtK8TwnOeZ7wXphI.webp"}
SUMMONED = ["iso-grasping-arm", "fs-looting-deckhand-hold"]
SUMMON_JUTSU = ["iso-grasping-arm-rises", "fs-up-from-the-hold"]
AI_KEYS = ["username", "avatar", "avatarFacing", "gender", "level", "rank", "regeneration", "isSummon", "hidden",
           "inArena", "includeDefaultRules", "poolsMultiplier", "statsMultiplier", "preferredGeneral1",
           "preferredGeneral2", "primaryElement", "secondaryElement", "strength", "speed", "intelligence",
           "willpower", "offence", "defence", "ninjutsuMastery", "genjutsuMastery", "taijutsuMastery",
           "bukijutsuMastery", "bloodlineMastery", "sageMastery", "effects", "items", "jutsus", "rules"]
JUTSU_DROP = {"id", "createdAt", "updatedAt"}


def tag_defaults():
    src = subprocess.check_output(["git", "-C", GAME, "show", f"{GAME_PIN}:app/src/validators/combat.ts"], text=True)
    out = {}
    for m in re.finditer(r"export const (\w+)Tag = z\.object\(\{(.*?)\n\}\);", src, re.S):
        t = re.search(r'type: z\.literal\("(\w+)"\)', m.group(2))
        d = re.search(r'description: msg\(\s*"([^"]*)"', m.group(2))
        if t and d:
            out[t.group(1)] = d.group(1)
    return out


TAG_DESC = tag_defaults()
notes = []


def sid(i):
    return PFX + i


def ref(kind, i):
    return f"@{kind}:{sid(i)}"


def fx(effects, where):
    out = []
    for e in effects:
        e = copy.deepcopy(e)
        sa = e.get("staticAnimation", "")
        if sa in MARK_FX:
            tile, glint = MARK_FX[sa]
            e["staticAnimation"] = glint
            if not e.get("staticAssetPath"):
                e["staticAssetPath"] = tile
        for f in ("staticAnimation", "appearAnimation", "disappearAnimation"):
            v = e.get(f, "")
            if v in STRIPS:
                e[f] = ref("scene", v)
            elif v in LIVE_ANIM:
                e[f] = LIVE_ANIM[v]
            elif v and re.fullmatch(r"[a-z]+(?:[_-][a-z]+)+", v):
                notes.append(f"{where}: {e['type']}.{f} = {v} has no art yet; left empty")
                e[f] = ""
        if e.get("type") == "summon" and e.get("aiId"):
            e["aiId"] = ref("ai", e["aiId"])
        if e.get("description") in ("placeholder", "<p>placeholder</p>", ""):
            e["description"] = TAG_DESC.get(e["type"], e.get("description") or e["type"])
        out.append(e)
    return out


def jutsu_entry(jid, rec, phase):
    nullable = set(F.checks["nullable"]["fields"].get("jutsu", []))
    data = {k: v for k, v in rec.items() if k not in JUTSU_DROP and (v is not None or k in nullable)}
    data["name"] = NAMES.get(jid, rec["name"])
    data["hidden"] = True
    data["effects"] = fx(rec["effects"], jid)
    # factory's law-4 check (formula damage needs generalTypes) is stale at game pin 3314d122: the damage formula
    # reads the caster's highestGenerals and generalTypes is display-only (libs/combat/tags.ts getAffected), and
    # 134 live Skyglass damage effects already ship statTypes ["None"] with no generalTypes. Effects that trip only
    # that check are attached after construction, unchanged from the engine-tested spec; validate.py still sees them.
    effs = data.pop("effects")
    try:
        F._effects("jutsu", effs)
    except Exception as err:  # noqa: BLE001
        if "generalTypes" not in str(err):
            raise
        notes.append(f"{jid}: formula damage with statTypes [None] and no generalTypes (law 4 check skipped; stale at the pin)")
    e = F.entry("jutsu", "create", name=data["name"], srcId=sid(jid), data=data)
    e["data"]["effects"] = effs
    e["phase"] = phase
    return e


def rule(r):
    conds = [F.condition(c["type"], **{k: v for k, v in c.items() if k not in ("type", "description")}) for c in r["conditions"]]
    a = {k: v for k, v in r["action"].items() if k not in ("type",)}
    if a.get("jutsuId"):
        a["jutsuId"] = ref("jutsu", a["jutsuId"])
    if not a.get("description"):
        a.pop("description", None)
    return {"conditions": conds, "action": F.action(r["action"]["type"], **a)}


def ai_entry(aid, row, rules, include_default, phase):
    data = {k: copy.deepcopy(row[k]) for k in AI_KEYS if k in row}
    data["username"] = USERNAMES.get(aid, row["username"])
    if str(data.get("avatar", "")).startswith("@img:"):
        fn = data["avatar"][5:]
        assert fn in PLACEHOLDER_AVATARS, fn
        data["avatar"] = PLACEHOLDER_AVATARS[fn]
        notes.append(f"{aid}: avatar is a placeholder ({fn}, the donor's hosted image) until the director's art lands")
    data["hidden"] = True
    data.setdefault("inArena", False)
    data["includeDefaultRules"] = include_default
    data["items"] = []
    data["effects"] = fx(row.get("effects", []), aid)
    data["jutsus"] = [ref("jutsu", j) for j in row["jutsus"]]
    data["rules"] = [rule(r) for r in rules]
    assert len(data["rules"]) <= 20, aid
    return {"entity": "ai", "slot": "create", "srcId": sid(aid), "name": data["username"], "phase": phase, "data": data}


# ---------------------------------------------------------------- records
jutsu = {**ISO["newJutsu"], **{k: v["record"] for k, v in STO["newJutsu"].items() if k.startswith("fs-")}}
ais = {k: (v, v["rules"], v.get("includeDefaultRules", False)) for k, v in ISO["ais"].items()}
for k, v in STO["newAIs"].items():
    if k.startswith("fs-"):
        ais[k] = (v["fullRow"], v["fullProfile"]["rules"], v["fullProfile"].get("includeDefaultRules", False))
bad = [k for k, v in STO["newAIs"].items() if k.startswith("fs-") and v["insertAiSchema"] != "pass"]
bad += [k for k, v in STO["newJutsu"].items() if k.startswith("fs-") and v["JutsuValidator"] != "pass"]
assert not bad, f"harness schema failures: {bad}"

items = []
imgSizes = {}
for name, (title, frames) in STRIPS.items():
    fn = f"{name}.webp"
    p = os.path.join(ART, fn)
    assert os.path.exists(p), p
    imgSizes[fn] = os.path.getsize(p)
    image = f"@img:{fn}"
    if HOSTED:
        import hashlib
        u = json.load(open(HOSTED))["files"][sid(name)]
        assert u["file"] == fn and u["sha256"] == hashlib.sha256(open(p, "rb").read()).hexdigest(), ("upload does not match strip", fn)
        assert u["url"].startswith("https://bbenpyo9uu.ufs.sh/f/"), u["url"]
        image = u["url"]
    items.append({"entity": "asset", "slot": "create", "srcId": sid(name), "name": title, "phase": 10, "data": {
        "name": title, "type": "ANIMATION", "folder": FOLDER, "frames": frames, "speed": 50, "hidden": True,
        "onInitialBattleField": False, "licenseDetails": "TNR", "image": image}})
for jid, rec in jutsu.items():
    if jid not in SUMMON_JUTSU:
        items.append(jutsu_entry(jid, rec, 20))
for aid in SUMMONED:
    items.append(ai_entry(aid, *ais[aid], 30))
for jid in SUMMON_JUTSU:
    items.append(jutsu_entry(jid, jutsu[jid], 40))
for aid in ais:
    if aid not in SUMMONED:
        items.append(ai_entry(aid, *ais[aid], 50))

# every @jutsu/@ai/@scene ref must be created earlier in the sequence
made, order_problems = set(), []
for it in items:
    for r in re.findall(r'"@(jutsu|ai|scene):([^"]+)"', json.dumps(it["data"])):
        if r[1] not in made:
            order_problems.append(f"{it['srcId']} needs {r[1]} before it")
    made.add(it["srcId"])
assert not order_problems, order_problems

# Law 17: an AI's jutsus array (and a summon's aiId) must carry LITERAL ids; refs are stripped server-side and
# validate.py refuses them. So the build runs in four stages, each regenerated from the previous stages' results
# bundles (--bundle, repeatable): their idmap supplies srcId -> created id. A stage whose refs are still open is
# written anyway (marked NOT READY) so it can be read and validated for everything else.
idmap = {}
for b in BUNDLES:
    idmap.update(json.load(open(b)).get("idmap") or {})


def resolve(o):
    if isinstance(o, dict):
        return {k: resolve(v) for k, v in o.items()}
    if isinstance(o, list):
        return [resolve(v) for v in o]
    if isinstance(o, str):
        m = re.fullmatch(r"@(jutsu|ai|scene):(.+)", o)
        if m and m.group(2) in idmap:
            return idmap[m.group(2)]
        if o.startswith("@img:") and o[5:] in idmap:
            return idmap[o[5:]]
    return o


STAGES = [
    ("1_strips_and_jutsu", (10, 20), "the nine Isonade strips (@img: uploads) and 26 jutsu; their @scene refs resolve inside this run"),
    ("2_summoned_ais", (30,), "the Grasping Arm and the Deckhand from the Hold (needs stage 1's bundle for literal jutsu ids)"),
    ("3_summon_jutsu", (40,), "Grasping Arm Rises and Up from the Hold (need stage 2's bundle for the summoned AI ids)"),
    ("4_ais", (50,), "Isonade and the five crew (need stages 1 and 3 bundles for literal jutsu ids)"),
]
from collections import Counter  # noqa: E402
for fname, phases, what in STAGES:
    st = [resolve(it) for it in items if it["phase"] in phases]
    open_refs = sorted(set(re.findall(r'"(@(?:jutsu|ai):[^"]+)"', json.dumps(st))))
    man = {
        "_note": (f"The Flooded Stores build, stage {fname[0]} of 4: {what}. Generated by flooded_stores_build.gen.py from the "
                  "engine-tested harness specs; do not hand-edit. NOT cleared to push: every stage needs the director's go. "
                  "All creates hidden. Isonade and the Grasping Arm carry placeholder avatars until the director's art lands. "
                  + (f"NOT READY: {len(open_refs)} refs wait on earlier stages' results bundles." if open_refs else "Refs resolved.")),
        "dedupNames": True,
        "items": st,
    }
    if any(it["entity"] == "asset" for it in st) and not HOSTED:
        man["imgSizes"] = imgSizes
    out = os.path.join(HERE, "manifests", f"{fname}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(man, open(out, "w"), indent=1, ensure_ascii=False)
    open(out, "a").write("\n")
    print(f"wrote {out}: {dict(Counter(i['entity'] for i in st))}; open refs {len(open_refs)}")
for n in sorted(set(notes)):
    print("  note:", n)
