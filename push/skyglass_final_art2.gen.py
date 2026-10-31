#!/usr/bin/env python3
"""Skyglass final art, part 2 (push/373-378). Zero live requests: everything is read from repository files.

    python3 push/skyglass_final_art2.gen.py                       # writes 373, 374, 375, 376, 377
    python3 push/skyglass_final_art2.gen.py --unhide <376 bundle> # writes 378 (literal asset ids from 376's run)

373  Crownhold scene backgrounds SC01-SC06. Six SCENE_BACKGROUND gameAssets (hidden, law 16b) and Crownhold re-sent
     whole (quest edits do not fetch-merge) from the same source as push/365, the live record:
     skyglass_crownhold_rework.gen.py crownhold_record() (= push/349 + the heal top-ups). The generator asserts that
     record equals the committed 365 item byte for byte, then changes ONLY sceneBackground values and proves it (the
     `_diff_vs_365` block lists every changed path; any other difference aborts). A dialog's sceneBackground is read as a
     gameAsset id (theninjarpg@3314d122 layout/Logbook.tsx ~486-525, gameAsset.getSceneAssets, which does not filter
     hidden), so the scenes are assets referenced by @scene, not bare @img URLs.
374  The salvager PT01 on Wreck Sighted. One SCENE_CHARACTER gameAsset (hidden) and Wreck Sighted re-sent whole from
     push/348's create (skyglass_hoard.gen.py wreck_sighted(), asserted equal to the archived 348 record) with the
     salvager on both dialog nodes and as the quest's main scene character. The main entry is what lets the quest be
     published: the server refuses a non-hidden save unless content.sceneCharacters is set or EVERY objective has one
     (routers/quests.ts ~866-880), and w_done (win_quest) has none of its own. Stays hidden. push/339 (go-live) does not
     re-send Wreck Sighted, so it needs no change.
375  FX step 1, law 18/60: the library/exclusive jutsu that 376 edits are taken off every holder (AI edit: kit minus
     those jutsu, items re-sent; rules untouched). The Crowned Captain also loses Extermination Order here: push/372
     edited its image, and a save of a hidden jutsu unequips every holder (routers/jutsu.ts ~1117 ->
     queries/jutsu.ts:662 updateUserJutsuForUpdate), so his two exclusives have been severed since 372 ran.
376  FX step 2: the boss-FX gameAssets (hidden) and the jutsu edits that use them, in one job (assets phase 1, jutsu
     phase 2, @scene refs resolve in-job). Only effects change (and injectableInBattle:false, law 20).
377  FX step 3: every holder re-equipped (the same kit it had before 375; an added id inserts a fresh, equipped row,
     profile.ts updateUserContent / applyUserContentChanges).
378  FX step 4 (--unhide, built from 376's results bundle): the FX assets unhidden (law 16c: battles load only unhidden
     assets). Scene assets (373, 374) need no unhide: getSceneAssets does not filter hidden.

Not mapped (director decision, see push/README.md 373-378): AN04 (ch_enrage = The Core Rebuilds = live Second Wind,
pool S35), AN07/AN08 (ch_bile_spit = Bilge Spit = live Venom Strike, S29), AN09 (ch_undertow = Undertow = live
Sovereign Undertow, B03) are shared pool jutsu held across the game; AN05 (cc_hexweave) has no move in any built kit;
the Sentinel's Shell Wall (cp_gunwale's second user) is live Adamantine Fortress. Little Maw: no AN strip is a bite.

Exports are pinned by the newest commit that touched them (commit them first). Do not hand-edit the outputs.
"""
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "push"))
NUM = {"scenes": 373, "salvager": 374, "unequip": 375, "fx": 376, "reequip": 377, "unhide": 378}


def load(name):
    s = importlib.util.spec_from_file_location(name.replace(".", "_"), os.path.join(ROOT, "push", name))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def jload(path):
    return json.load(open(os.path.join(ROOT, path)))


def git(*a):
    return subprocess.check_output(["git", "-C", ROOT, *a], text=True).strip()


def pack(paths):
    """imagePack pinned at the newest commit touching the files; refuses an uncommitted or modified export."""
    paths = sorted(set(paths))
    ref = git("log", "-1", "--format=%H", "HEAD", "--", *paths)
    files = {}
    for p in paths:
        disk = open(os.path.join(ROOT, p), "rb").read()
        if subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{p}"]) != disk:
            sys.exit(f"{p}: working copy differs from {ref}; commit it first")
        files[os.path.basename(p)] = {"path": p, "sha256": hashlib.sha256(disk).hexdigest(), "bytes": len(disk)}
    return {"imgSizes": {k: v["bytes"] for k, v in files.items()}, "imagePack": {"ref": ref, "files": files}}


def asset(src, name, typ, path, folder, frames=1, speed=1):
    return {"entity": "asset", "slot": "create", "phase": 1, "srcId": src, "name": name, "data": {
        "name": name, "type": typ, "image": "@img:" + os.path.basename(path), "folder": folder, "frames": frames,
        "speed": speed, "hidden": True, "onInitialBattleField": False, "licenseDetails": "TNR"}}


def write(num, slug, m):
    path = os.path.join(ROOT, "push", f"{num}_{slug}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"push/{num}_{slug}.json: {len(m['items'])} items")


def diff_paths(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            p = f"{path}.{k}" if path else k
            if k not in a or k not in b:
                out.append(p)
            else:
                out += diff_paths(a[k], b[k], p)
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [path]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            ident = x.get("id") if isinstance(x, dict) and "id" in x else i
            out += diff_paths(x, y, f"{path}[{ident}]")
        return out
    return [] if a == b else [path]


# ===================================================================================================== 373
SC = "art/crownhold/scenes/exports/"
SCENES = {  # key -> (SC code, export, asset name); prompts docs/handoffs/SKYGLASS_ART_PROMPTS.md section 8
    "gate": ("SC01", SC + "scene_bg_crownhold_gate.webp", "Crownhold Scene - Gate"),
    "proving_hall": ("SC02", SC + "scene_bg_crownhold_proving_hall.webp", "Crownhold Scene - Proving Hall"),
    "vat_halls": ("SC03", SC + "scene_bg_crownhold_vat_halls.webp", "Crownhold Scene - Sealing-Jar Halls"),
    "signal_room": ("SC04", SC + "scene_bg_crownhold_signal_room.webp", "Crownhold Scene - Signal Room"),
    "planning_hall": ("SC05", SC + "scene_bg_crownhold_planning_hall.webp", "Crownhold Scene - Planning Hall"),
    "throne_room": ("SC06", SC + "scene_bg_crownhold_throne_room.webp", "Crownhold Scene - Throne Room"),
}
SCENE_PFX = f"sg{NUM['scenes']}_scene_"
GATE_NODES = {"d2.n.f1", "f_lost", "f.arakane"}  # SC01: the opening (the road ends at the gate) and both fail nodes
# High Command (division 4) split by the SC04/SC05 notes. Signal room: the Signaller (its bell-cord board) and the
# order-sealing shrine with its courier passage (terminal, puzzle, wrong answers, the Runner, the rites). Planning
# hall: the Tactician (the war-council table), the Honor Guard corridor and the Second's office (a folding map
# table) with its fights. PROPOSAL (the notes name only the Signaller and the Tactician).
SIGNAL_PREFIXES = ("d4.n.f1", "b4.n.f1", "d4.n.terminal", "d4.n.puzzle", "b4.n.f4", "d4.n.protocol")


def scene_key(nid):
    if nid in GATE_NODES:
        return "gate"
    div = nid[1] if nid[1].isdigit() else "5"  # d.aftermath and w.complete stand in the throne room
    if div == "4":
        return "signal_room" if nid.startswith(SIGNAL_PREFIXES) else "planning_hall"
    return {"2": "proving_hall", "3": "vat_halls", "5": "throne_room"}[div]


def scenes_manifest():
    CR = load("skyglass_crownhold_rework.gen.py")
    base = CR.crownhold_record([])
    live = jload("push/365_crownhold_heal_topups.json")["items"][0]
    assert base["targetId"] == live["targetId"] and base["data"] == live["data"], \
        "crownhold_record() no longer equals push/365 (the live record): regenerate 365 and investigate first"
    data = copy.deepcopy(base["data"])
    c = data["content"]
    count = {}
    for o in c["objectives"]:
        k = scene_key(o["id"])
        o["sceneBackground"] = "@scene:" + SCENE_PFX + k
        count[k] = count.get(k, 0) + 1
    c["sceneBackground"] = "@scene:" + SCENE_PFX + "gate"  # law 25: the travel popup shows the top-level scene
    changed = diff_paths(live["data"], data)
    bad = [p for p in changed if not p.endswith("sceneBackground")]
    assert not bad, f"373 changes more than sceneBackground: {bad}"
    assert len(changed) == len(c["objectives"]) + 1, len(changed)
    assert set(count) == set(SCENES), count
    quest = {"entity": "quest", "slot": "edit", "phase": 2, "targetId": live["targetId"],
             "name": "Crownhold: final scene backgrounds SC01-SC06", "data": data}
    assets = [asset(SCENE_PFX + k, name, "SCENE_BACKGROUND", p, "Crownhold") for k, (_, p, name) in SCENES.items()]
    m = {"_note": (
        f"push/{NUM['scenes']}: Crownhold's six final scene backgrounds (SC01-SC06, art/crownhold/scenes/exports). Six "
        "SCENE_BACKGROUND gameAssets created HIDDEN (law 16b; quest scenes load through gameAsset.getSceneAssets, which "
        "does not filter hidden), then Crownhold (fqqpkcp_L4oOsC6yyodlk, hidden) re-sent whole from the same source as "
        "push/365 (the live record: push/349 + heal top-ups) with ONLY sceneBackground changed (_diff_vs_365). Stays "
        "hidden. Generated by push/skyglass_final_art2.gen.py; do not hand-edit."),
        "dedupNames": True, **pack(p for _, p, _ in SCENES.values()),
        "_diff_vs_365": {"changed_paths": len(changed), "all_sceneBackground": True,
                         "objectives_per_scene": count, "top_level": "gate (was empty; law 25)"},
        "items": assets + [quest]}
    write(NUM["scenes"], "crownhold_scenes", m)
    return changed


# ===================================================================================================== 374
SALVAGER = "art/skyglass_scene_chars/exports/scene_char_skyglass_salvager.webp"
SALVAGER_SRC = f"sg{NUM['salvager']}_salvager"
WRECK_SIGHTED_ID = "v7kKhLXsX9aofQfc7BnGx"  # push/348 (tnr_results_1793459592295.json idmap sg348_wreck_sighted)
BUNDLE_348 = "harvests/inbox/tnr_results_1793459592295.json"
ARCHIVED_348 = "archive/spent-manifests/push-2026-10-31/348_skyglass_hoard_and_intro.json"


def salvager_manifest():
    H = load("skyglass_hoard.gen.py")
    ws = H.wreck_sighted()
    assert jload(BUNDLE_348)["idmap"][ws["srcId"]] == WRECK_SIGHTED_ID
    sent = next(i for i in jload(ARCHIVED_348)["items"] if i.get("srcId") == ws["srcId"])
    assert ws["data"] == sent["data"], "wreck_sighted() no longer equals push/348's create (the live record)"
    data = copy.deepcopy(sent["data"])
    ref = ["@scene:" + SALVAGER_SRC]
    dialogs = [o for o in data["content"]["objectives"] if o["task"] == "dialog"]
    assert [o["id"] for o in dialogs] == ["d_word", "d_chart"], dialogs
    for o in dialogs:
        o["sceneCharacters"] = list(ref)
    data["content"]["sceneCharacters"] = list(ref)
    assert data["hidden"] is True
    changed = diff_paths(sent["data"], data)
    assert all(p.endswith("sceneCharacters") for p in changed) and len(changed) == 3, changed
    w, h = Image.open(os.path.join(ROOT, SALVAGER)).size
    assert abs(w / h - 2 / 3) < 0.01, (w, h)  # 2:3 portrait (341 x 512)
    m = {"_note": (
        f"push/{NUM['salvager']}: the salvager (PT01) on Wreck Sighted ({WRECK_SIGHTED_ID}, hidden). One SCENE_CHARACTER "
        "gameAsset created HIDDEN, then the quest re-sent whole (quest edits do not fetch-merge) from push/348's create "
        "with the salvager on both dialog nodes and as the main scene character (the publish rule, routers/quests.ts "
        "~866-880: main characters, or every objective). Nothing else changes (_diff_vs_348); stays hidden. push/339 does "
        "not re-send this quest. Generated by push/skyglass_final_art2.gen.py; do not hand-edit."),
        "dedupNames": True, **pack([SALVAGER]),
        "_diff_vs_348": {"changed_paths": changed},
        "items": [asset(SALVAGER_SRC, "Skyglass Scene - The Salvager", "SCENE_CHARACTER", SALVAGER, "Skyglass"),
                  {"entity": "quest", "slot": "edit", "phase": 2, "targetId": WRECK_SIGHTED_ID,
                   "name": "Wreck Sighted: the salvager (PT01)", "data": data}]}
    write(NUM["salvager"], "skyglass_wreck_sighted_salvager", m)


# ===================================================================================================== 375-377
FXD = "art/skyglass_boss_fx/exports/"
FX_PFX = f"sg{NUM['fx']}_"
FX = {  # srcId suffix -> (AN, export, asset name, type); frames/speed from an_v1.json (150 px frames, director 2026-10-31)
    "an01_command_banner": ("AN01", FXD + "anim_fx_command_banner_v1.webp", "Skyglass FX - Ward of Command banner", "ANIMATION"),
    "an02_phase_shift": ("AN02", FXD + "anim_fx_phase_shift_v1.webp", "Skyglass FX - Phase Shift", "ANIMATION"),
    "an03_gunwale": ("AN03", FXD + "anim_fx_gunwale_barrier_v1.webp", "Skyglass FX - Gunwale barrier", "ANIMATION"),
    "an03_gunwale_tile": ("AN03", FXD + "tile_fx_gunwale_barrier_v1.webp", "Skyglass FX - Gunwale barrier (held)", "STATIC"),
    "an06_ember_tile": ("AN06", FXD + "tile_fx_spreading_fire_embers_v1.webp", "Skyglass FX - Spreading Fire embers (tile)", "STATIC"),
    "an06_ember_glint": ("AN06", FXD + "anim_fx_spreading_fire_glint_v1.webp", "Skyglass FX - Spreading Fire sparks", "ANIMATION"),
}
LIB_BUNDLE = "harvests/inbox/tnr_results_1793426982231.json"  # push/342, 41/41 VERIFIED
LAST_DIRECTIVE = "GHFMU_DDKvBBp5BEuTeah"
EXTERMINATION_ORDER = "EqZsaqser8c2-KpVCaXk_"
ARCHIVED_271 = "archive/spent-manifests/push-2026-10-25/271_crownhold_exclusives.json"
S = lambda k: "@scene:" + FX_PFX + k  # noqa: E731
# Jutsu edits: (library srcId or literal id, name, {effect type: {field: value}}). Placement follows the harness's
# symbolic slot (push/342 _placeholders) and an_v1.json's suggested use.
EDITS = [
    ("sg342_lib-ward-of-command", "Ward of Command", {"decreasedamagetaken": {"staticAnimation": S("an01_command_banner")}}),
    # an_v1: the strip rises and holds (appear), the held wall is the STATIC tile (staticAssetPath, drawn under the
    # characters). Replaces the harness's donor appear id and its "xAd94Cpuri" staticAssetPath (not an asset id).
    ("sg342_dg-raise-the-gunwale", "Raise the Gunwale", {"barrier": {"appearAnimation": S("an03_gunwale"),
                                                                     "staticAssetPath": S("an03_gunwale_tile")}}),
    *[(f"sg342_chart-embers-{i}", f"Spreading Fire {r}", {"visual": {"staticAssetPath": S("an06_ember_tile"),
                                                                     "staticAnimation": S("an06_ember_glint")}})
      for i, r in ((1, "I"), (2, "II"), (3, "III"))],
    # crowned_captain_spec.json editedJutsu / animations: cc_phase_shift on the Last Directive's finalstand (his 30%
    # phase). Its staticAnimation cc_last_directive has no art and stays empty.
    (LAST_DIRECTIVE, "The Last Directive", {"finalstand": {"appearAnimation": S("an02_phase_shift")}}),
]
# Records whose last committed AI payload may hold an edited jutsu (newest state of each holder; scanned below).
HOLDER_SOURCES = [
    ("push/361_skyglass_crew_upgrade.json", None),
    ("push/344_skyglass_copies_1.json", "harvests/inbox/tnr_results_1793484364363.json"),
    ("push/344_skyglass_copies_3.json", "harvests/inbox/tnr_results_1793484748665.json"),
    ("push/364_crownhold_captain_rework.json", None),
]
LATER_AI_SOURCES = ("push/372_skyglass_final_art.json",)  # later AI edits that do not touch kits (checked)


def library_ids():
    im = jload(LIB_BUNDLE)["idmap"]
    return {src: im[src] for src, _, _ in EDITS if src.startswith("sg342_")}


def live_effects():
    """Current effects of each edited jutsu: push/342 as committed (regenerated to match live after push/343; text
    only) and push/271 for the Last Directive (later sends: 329 description, 372 image)."""
    lib = {it["srcId"]: it["data"] for it in jload("push/342_skyglass_library.json")["items"]}
    ld = next(i for i in jload(ARCHIVED_271)["items"] if i["srcId"] == "last_directive")["data"]
    spec = jload("state/skyglass_build/crowned_captain_spec.json")["editedJutsu"][LAST_DIRECTIVE]["effects"]
    anim = ("appearAnimation", "staticAnimation", "disappearAnimation")
    strip = lambda es: [{k: v for k, v in e.items() if k not in anim} for e in es]  # noqa: E731
    assert [dict(sorted(e.items())) for e in strip(ld["effects"])] == [dict(sorted(e.items())) for e in strip(spec)]
    out = {src: copy.deepcopy(lib[src]["effects"]) for src, _, _ in EDITS if src.startswith("sg342_")}
    out[LAST_DIRECTIVE] = copy.deepcopy(ld["effects"])
    return out


def jutsu_edits():
    ids, eff = library_ids(), live_effects()
    items, log = [], []
    for src, name, change in EDITS:
        effects = eff[src]
        for typ, fields in change.items():
            hit = [e for e in effects if e["type"] == typ]
            assert len(hit) == 1, (name, typ)
            for f, v in fields.items():
                log.append(f"{name}: {typ}.{f} {hit[0].get(f, '')!r} -> {v}")
                hit[0][f] = v
        items.append({"entity": "jutsu", "slot": "edit", "phase": 2, "targetId": ids.get(src, src),
                      "name": f"{name}: boss FX", "data": {"effects": effects, "injectableInBattle": False}})
    return items, log


def fx_assets():
    an = {a["file"]: a for a in jload(FXD + "an_v1.json")["assets"]}
    out = []
    for k, (code, p, name, typ) in FX.items():
        a = an[p]
        assert a["an"] == code and a["type"] == typ, (p, a)
        im = Image.open(os.path.join(ROOT, p))
        frames = a["frames"]
        assert im.width == a["frame_px"] == 150 and im.height == 150 * frames, (p, im.size)
        out.append(asset(FX_PFX + k, name, typ, p, "SkyglassBossFX", frames, a["speed"] or 1))
    return out


def holders():
    """Every AI whose newest kit holds a jutsu 376 edits (or Extermination Order, severed by push/372)."""
    edited = set(library_ids().values()) | {LAST_DIRECTIVE}
    severed = {EXTERMINATION_ORDER}
    seen, out = set(), []
    for path, bundle in HOLDER_SOURCES:
        ents = {}
        if bundle:
            for e in jload(bundle)["entries"]:
                if e.get("entity") == "ai" and e.get("slot") == "create" and e.get("state") == "ok":
                    ents[e["srcId"]] = (e["id"], e["name"])
        for it in jload(path)["items"]:
            if it["entity"] != "ai":
                continue
            d = it["data"]
            off = [j for j in d["jutsus"] if j in edited or j in severed]
            if not off:
                continue
            if it["slot"] == "create":
                aid, name = ents[it["srcId"]]
                assert name == d["username"], (it["srcId"], name)
            else:
                aid, name = it["targetId"], it["name"].split(":")[0]
            assert aid not in seen, aid
            seen.add(aid)
            out.append({"id": aid, "name": name, "source": os.path.basename(path), "kit": list(d["jutsus"]),
                        "items": copy.deepcopy(d.get("items") or []), "off": off})
    for path in LATER_AI_SOURCES:  # nothing later re-sent a holder's kit
        for it in jload(path)["items"]:
            if it["entity"] == "ai" and it.get("targetId") in seen:
                assert "jutsus" not in it["data"], (path, it["targetId"])
    return out


def ai_edit(h, jutsus, label):
    return {"entity": "ai", "slot": "edit", "targetId": h["id"], "name": f"{h['name']}: {label}",
            "data": {"jutsus": jutsus, "items": h["items"]}}


def fx_manifests():
    hs = holders()
    table = [f"{h['name']} ({h['id']}, from {h['source']}): {len(h['kit'])} jutsu, off/on: {h['off']}" for h in hs]
    unequip = [ai_edit(h, [j for j in h["kit"] if j not in h["off"]], "boss-FX jutsu off (law 18/60)") for h in hs]
    reequip = [ai_edit(h, h["kit"], "boss-FX jutsu back on (law 18/60)") for h in hs]
    write(NUM["unequip"], "skyglass_fx_unequip", {
        "_note": (f"push/{NUM['unequip']}, FX step 1 of 4 (law 18/60: unequip -> edit -> re-equip). Takes the jutsu "
                  f"push/{NUM['fx']} edits (Ward of Command, Raise the Gunwale, Spreading Fire I-III, The Last "
                  "Directive) off every holder, and Extermination Order off the Crowned Captain (severed by push/372's "
                  "image edit). Kit otherwise unchanged; items re-sent; rules untouched. The Captain and the Sealwright "
                  "are the live crew the four live hunts fight until push/339: run 375 -> 376 -> 377 back to back. "
                  "Generated by push/skyglass_final_art2.gen.py; do not hand-edit."),
        "_holders": table, "items": unequip})
    edits, log = jutsu_edits()
    assets = fx_assets()
    write(NUM["fx"], "skyglass_fx", {
        "_note": (f"push/{NUM['fx']}, FX step 2 of 4 (after push/{NUM['unequip']}). Phase 1: the boss-FX gameAssets "
                  "(AN01, AN02, AN03 strip + held tile, AN06 tile + sparks; art/skyglass_boss_fx/exports, an_v1.json: "
                  "150 px frames, 50 ms) created HIDDEN (law 16b). Phase 2: the jutsu that use them, effects only "
                  "(@scene refs resolve in this job; injectableInBattle false, law 20): Ward of Command, Raise the "
                  "Gunwale, Spreading Fire I-III (push/342 library) and The Last Directive (push/271). The jutsu stay "
                  f"hidden. Then push/{NUM['reequip']}; push/{NUM['unhide']} (built from this run's bundle) unhides "
                  "the assets. Generated by push/skyglass_final_art2.gen.py; do not hand-edit."),
        "dedupNames": True, **pack(p for _, p, _, _ in FX.values()),
        "_changes": log, "items": assets + edits})
    write(NUM["reequip"], "skyglass_fx_reequip", {
        "_note": (f"push/{NUM['reequip']}, FX step 3 of 4 (after push/{NUM['fx']}). Every holder from push/"
                  f"{NUM['unequip']} gets its full kit back (the kit of its last verified send); the re-added jutsu "
                  "insert fresh, equipped rows. Items re-sent; rules untouched. Generated by "
                  "push/skyglass_final_art2.gen.py; do not hand-edit."),
        "_holders": table, "items": reequip})
    return hs


def unhide_manifest(bundle):
    b = json.load(open(bundle))
    if (b.get("journal") or {}).get("manifestNumber") != NUM["fx"]:
        raise SystemExit(f"{os.path.basename(bundle)} is not push/{NUM['fx']}'s results bundle")
    ok = {e["srcId"]: e["id"] for e in b["entries"]
          if e.get("entity") == "asset" and e.get("slot") == "create" and e.get("state") == "ok" and e.get("id")}
    items = []
    for c in fx_assets():
        aid = ok.get(c["srcId"])
        if not aid:
            raise SystemExit(f"{c['srcId']}: no ok create in {os.path.basename(bundle)}")
        data = dict(c["data"], hidden=False)
        data.pop("image")
        items.append({"entity": "asset", "slot": "edit", "targetId": aid, "name": c["name"], "data": data})
    write(NUM["unhide"], "skyglass_fx_unhide", {
        "_note": (f"push/{NUM['unhide']}, FX step 4 of 4 (built from push/{NUM['fx']}'s bundle "
                  f"{os.path.basename(bundle)}; literal ids): unhides the {len(items)} boss-FX assets (law 16c: battles "
                  "load only unhidden assets); create data re-sent with hidden false, image kept. Generated by "
                  "push/skyglass_final_art2.gen.py --unhide; do not hand-edit."), "items": items})


def main():
    a = sys.argv[1:]
    if a[:1] == ["--unhide"] and len(a) == 2:
        return unhide_manifest(a[1])
    if a:
        raise SystemExit(__doc__)
    changed = scenes_manifest()
    print(f"  373 vs 365: {len(changed)} changed paths, all sceneBackground")
    salvager_manifest()
    hs = fx_manifests()
    for h in hs:
        print(f"  holder {h['name']}: off {h['off']}")


if __name__ == "__main__":
    main()
