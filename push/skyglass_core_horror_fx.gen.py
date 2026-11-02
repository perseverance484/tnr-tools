#!/usr/bin/env python3
"""Core Horror FX copies: Skyglass-only copies of three shared live jutsu, carrying AN04 / AN07-AN08 / AN09 (RUL-2026-11-01-092).

    python3 push/skyglass_core_horror_fx.gen.py --source <411 bundle>
        -> push/412_core_horror_fx_copies.json   (4 hidden ANIMATION gameAssets, phase 1; 3 hidden jutsu creates, phase 2)
    python3 push/skyglass_core_horror_fx.gen.py --swap <412 bundle>
        -> push/413_core_horror_fx_unhide.json   (4 asset unhides: battles load only unhidden assets, law 16c)
        -> push/414_core_horror_fx_swap.json     (5 Core Horror AI edits: old ids -> copies in kit and rules)

Why copies (push/README.md 373-378 "Not mapped"; director 2026-11-01: "Make the copies."): Second Wind, Venom Strike and
Sovereign Undertow are shared pool jutsu held by AIs across the game. Editing them would change their look everywhere
and sever every holder (law 18). The copies are the live records exactly as push/411 read them (effects, costs, range,
cooldown, flags), with a new name, Skyglass battle text, hidden: true (AIs use hidden jutsu), and the animations:
  * The Core Rebuilds (Second Wind): heal.appearAnimation = AN04 (enrage aura; an_v1 suggests static, but the heal is
    instant, so it plays once on cast).
  * Bilge Spit (Venom Strike): damage.appearAnimation = AN07 (the glob lands), poison.appearAnimation = AN08 (splash).
  * Undertow (Sovereign Undertow): redirection.appearAnimation = AN09 (water-drag streak).
Only the five Core Horror records swap (Core Horror, Faded, Veteran, Rot-Touched, Steeping Horror). The Captains keep
live Second Wind; the Second keeps live Sovereign Undertow; the Crown Stonebound keeps live Venom Strike. Swapping in a
NEW jutsu needs no unequip (the live jutsu are not edited). Battles load only unhidden assets (law 16c): 403 unhides the
four assets; run it before 404. (Separate manifests: validate.py's build-order lint misranks assets, RUL-2026-10-31-085 item 1.) Kits/rules: push/361 (Core Horror) and push/344 (the four copies), unchanged since.
Do not hand-edit the outputs.
"""
import argparse
import copy
import hashlib
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PFX = "sg412_"
FXD = "art/skyglass_boss_fx/exports/"
ASSETS = {  # srcId suffix -> (AN, export, asset name)
    "an04_core_enrage": ("AN04", FXD + "anim_fx_core_enrage_v1.webp", "Skyglass FX - The Core Rebuilds"),
    "an07_bile_glob": ("AN07", FXD + "anim_fx_bile_glob_v1.webp", "Skyglass FX - Bilge Spit glob"),
    "an08_bile_splash": ("AN08", FXD + "anim_fx_bile_splash_v1.webp", "Skyglass FX - Bilge Spit splash"),
    "an09_undertow": ("AN09", FXD + "anim_fx_undertow_v1.webp", "Skyglass FX - Undertow"),
}
S = lambda k: "@scene:" + PFX + k  # noqa: E731
# live id -> (copy srcId, name, description, battleDescription, {effect type: {field: value}})
COPIES = {
    "STu1VHNcfgeC3x-UiQDgt": ("core_rebuilds", "The Core Rebuilds",
        "The Core pours fresh skyglass into the Horror's wounds and seals them over.",
        "Skyglass floods the cracks in %user's body, and the wounds seal over with a low, rising hum.",
        {"heal": {"appearAnimation": S("an04_core_enrage")}}),
    "LiVOnYq6qHzjB0XkIIA2e": ("bilge_spit", "Bilge Spit",
        "A glob of black bilge that bursts on impact and rots health, chakra and stamina.",
        "%user heaves and spits a glob of black bilge at %target. It bursts on impact, and the rot soaks in.",
        {"damage": {"appearAnimation": S("an07_bile_glob")}, "poison": {"appearAnimation": S("an08_bile_splash")}}),
    "nOYLPmN3TXj6wEe_oE6HQ": ("undertow", "Undertow",
        "The deck turns to a rip tide beneath the target and drags them in.",
        "The planks under %target heave like a rip tide, and %user drags them in across the deck.",
        {"redirection": {"appearAnimation": S("an09_undertow")}}),
}
CREATE_KEYS = ["actionCostPerc", "battleUsageType", "bloodlineId", "chakraCost", "chakraCostReducePerLvl", "cooldown",
               "coordinateTargeting", "effects", "elementClassification", "extraBaseCost", "healthCost",
               "healthCostReducePerLvl", "image", "injectableInBattle", "jutsuRank", "jutsuType", "jutsuWeapon", "method",
               "methodSize", "range", "requiredLevel", "requiredRank", "staminaCost", "staminaCostReducePerLvl",
               "statClassification", "target", "villageId"]  # the push/342 create key set
HOLDERS = [  # (manifest, item selector, AI id or None to resolve from the 344 bundle)
    ("361_skyglass_crew_upgrade.json", ("targetId", "AQi-bHJ-5tHXtxrnc0P9E")),
    ("344_skyglass_copies_1.json", ("srcId", "sg344_faded-core-horror")),
    ("344_skyglass_copies_1.json", ("srcId", "sg344_veteran-core-horror")),
    ("344_skyglass_copies_1.json", ("srcId", "sg344_rot-core-horror")),
    ("344_skyglass_copies_1.json", ("srcId", "sg344_oneoff-steeping-horror")),
]
BUNDLE_344 = "harvests/inbox/tnr_results_1793484364363.json"


def jload(p):
    return json.load(open(os.path.join(ROOT, p)))


def git(*a):
    return subprocess.check_output(["git", "-C", ROOT, *a], text=True).strip()


def pack(paths):
    ref = git("log", "-1", "--format=%H", "HEAD", "--", *paths)
    files = {}
    for p in paths:
        disk = open(os.path.join(ROOT, p), "rb").read()
        if subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{p}"]) != disk:
            raise SystemExit(f"{p}: working copy differs from {ref}")
        files[os.path.basename(p)] = {"path": p, "sha256": hashlib.sha256(disk).hexdigest(), "bytes": len(disk)}
    return {"imgSizes": {k: v["bytes"] for k, v in files.items()}, "imagePack": {"ref": ref, "files": files}}


def write(n, slug, m):
    with open(os.path.join(ROOT, f"push/{n}_{slug}.json"), "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{n}_{slug}.json: {len(m['items'])} items")


def assets():
    an = {a["file"]: a for a in jload(FXD + "an_v1.json")["assets"]}
    out = []
    for k, (code, p, name) in ASSETS.items():
        a = an[p]
        assert a["an"] == code and a["type"] == "ANIMATION", a
        out.append({"entity": "asset", "slot": "create", "phase": 1, "srcId": PFX + k, "name": name, "data": {
            "name": name, "type": "ANIMATION", "image": "@img:" + os.path.basename(p), "folder": "SkyglassBossFX",
            "frames": a["frames"], "speed": a["speed"], "hidden": True, "onInitialBattleField": False,
            "licenseDetails": "TNR"}})
    return out


def source(bundle):
    b = json.load(open(bundle))
    got = {c["data"]["id"]: c["data"] for c in b.get("captures") or []
           if c.get("proc") == "jutsu.get" and c.get("ok") and isinstance(c.get("data"), dict)}
    missing = set(COPIES) - set(got)
    if missing:
        raise SystemExit(f"{os.path.basename(bundle)} lacks full jutsu.get captures of {sorted(missing)}: is it push/411's?")
    return got


def copies(bundle):
    live = source(bundle)
    out, log = [], []
    for lid, (src, name, desc, battle, change) in COPIES.items():
        rec = live[lid]
        data = {k: copy.deepcopy(rec[k]) for k in CREATE_KEYS if k in rec}
        data.update({"name": name, "description": desc, "battleDescription": battle, "hidden": True})
        for typ, fields in change.items():
            hit = [e for e in data["effects"] if e["type"] == typ]
            assert len(hit) == 1, (name, typ, [e["type"] for e in data["effects"]])
            for f, v in fields.items():
                log.append(f"{name} (copy of {rec['name']} {lid}): {typ}.{f} {hit[0].get(f, '')!r} -> {v}")
                hit[0][f] = v
        out.append({"entity": "jutsu", "slot": "create", "phase": 2, "srcId": PFX + src, "name": name, "data": data})
    return out, log


def holders():
    ids344 = {e["srcId"]: e["id"] for e in jload(BUNDLE_344)["entries"] if e.get("state") == "ok" and e.get("srcId")}
    out = []
    for mf, (key, val) in HOLDERS:
        it = next(i for i in jload("push/" + mf)["items"] if i.get(key) == val)
        aid = val if key == "targetId" else ids344[val]
        out.append((aid, it["data"].get("username") or it["name"].split(":")[0], it["data"]["jutsus"], it["data"]["rules"]))
    return out


def build_copies(bundle):
    items, log = copies(bundle)
    a = assets()
    m = {"_note": ("push/412 (RUL-2026-11-01-092), built from push/411's bundle " + os.path.basename(bundle) + ": the four "
                   "Core Horror FX animations (AN04, AN07, AN08, AN09) as hidden ANIMATION gameAssets (phase 1) and three "
                   "hidden Skyglass-only jutsu copies of shared live pool jutsu carrying them (phase 2, @scene refs in-job): "
                   "The Core Rebuilds (Second Wind), Bilge Spit (Venom Strike), Undertow (Sovereign Undertow). Everything "
                   "but name, text, hidden and the animation fields is the live record as read. Nothing holds the copies "
                   "until push/413. Generated by push/skyglass_core_horror_fx.gen.py; do not hand-edit."),
         "dedupNames": True, "_changes": log, **pack([ASSETS[k][1] for k in ASSETS]), "items": a + items}
    write(412, "core_horror_fx_copies", m)


def build_swap(bundle):
    b = json.load(open(bundle))
    ok = {e["srcId"]: e["id"] for e in b.get("entries") or []
          if e.get("slot") == "create" and e.get("state") == "ok" and e.get("id") and (e.get("srcId") or "").startswith(PFX)}
    need = {PFX + k for k in ASSETS} | {PFX + c[0] for c in COPIES.values()}
    if not need <= set(ok):
        raise SystemExit(f"{os.path.basename(bundle)} is not push/412's ok results: missing {sorted(need - set(ok))}")
    swap = {lid: ok[PFX + c[0]] for lid, c in COPIES.items()}
    unhide = [{"entity": "asset", "slot": "edit", "targetId": ok[PFX + k], "name": f"{name}: unhide", "data": {"hidden": False}}
              for k, (code, p, name) in ASSETS.items()]
    write(413, "core_horror_fx_unhide", {
        "_note": ("push/413 (RUL-2026-11-01-092), built from push/412's bundle " + os.path.basename(bundle) + " (literal "
                  "ids, L01): the four Core Horror FX assets unhidden (law 16c: battles load only unhidden assets). Run "
                  "before push/414. Generated by push/skyglass_core_horror_fx.gen.py --swap; do not hand-edit."),
        "items": unhide})
    items = []
    for aid, name, jutsus, rules in holders():
        assert all(l in jutsus for l in COPIES), (name, "kit lacks a source jutsu")
        js = [swap.get(j, j) for j in jutsus]
        rs = copy.deepcopy(rules)
        n = 0
        for r in rs:
            j = r["action"].get("jutsuId")
            if j in swap:
                r["action"]["jutsuId"] = swap[j]
                n += 1
        items.append({"entity": "ai", "slot": "edit", "targetId": aid,
                      "name": f"{name}: Core Horror FX copies ({n} rules re-pointed)", "data": {"jutsus": js, "rules": rs}})
    write(414, "core_horror_fx_swap", {
        "_note": ("push/414 (RUL-2026-11-01-092), built from push/412's bundle " + os.path.basename(bundle) + " (literal "
                  "ids, L01), after push/413: the five Core Horror records swap Second Wind, "
                  "Venom Strike and Sovereign Undertow for their copies, in the kit and in every rule that names them. "
                  "Kits and rules otherwise as push/361 / push/344. Generated by push/skyglass_core_horror_fx.gen.py "
                  "--swap; do not hand-edit."), "items": items})


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--source", help="push/411 results bundle")
    g.add_argument("--swap", help="push/412 results bundle")
    a = ap.parse_args()
    return build_copies(a.source) if a.source else build_swap(a.swap)


if __name__ == "__main__":
    main()
