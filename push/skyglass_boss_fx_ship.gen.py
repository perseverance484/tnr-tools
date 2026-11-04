#!/usr/bin/env python3
"""Ship the Skyglass boss set-piece animations (boss_fx.py strips, 2026-10-28) onto the live moves they were drawn for.

    python3 push/skyglass_boss_fx_ship.gen.py
        -> push/470_skyglass_boss_fx_assets.json   11 hidden ANIMATION gameAssets (phase 1, imagePack pinned) and
                                                    READ-ONLY jutsu.get captures of the 14 edited jutsu (before)
    python3 push/skyglass_boss_fx_ship.gen.py --from <470 results bundle>
        -> push/471_skyglass_boss_fx_unhide.json    11 asset unhides by literal id (law 16c)
        -> push/472_skyglass_boss_fx_unequip.json   AI edits: the edited jutsu off every holder (law 18/60)
        -> push/473_skyglass_boss_fx.json           14 jutsu edits: art fields only + injectableInBattle false (law 20)
        -> push/474_skyglass_boss_fx_reequip.json   AI edits: each holder's exact current kit back on
        -> push/475_skyglass_boss_fx_master.json    471-474 in one run (push/master_manifest.gen.py, phases 0/10/20/30)

Strips: art/skyglass_boss_fx/deliver_boss.py -> exports/anim_<id>_v1_x3d.webp (150 px frames, 50 ms, alpha 0/255;
the AN-set convention of push/376, exports/an_v1.json). Mapping (design ids in push/342 and push/363 `_placeholders`;
docs/design/SKYGLASS_ART_AUDIT.md H2; RUL-2026-10-30-061 item 10: the violet Binding blast reuses chain_wrap;
RUL-2026-10-28-028 item 6: every burst window uses the one window strip, anim_exposed): see SLOTS. The arena-wide set
pieces (Command Absolute, Broadside) take the field variants (director 2026-10-28, boss_fx.py field_variants).
RUL-2026-11-03-112: the window strip plays once (appearAnimation); Maw of the Deep's arena hit (maw_field) is held back
for a composite Maw, so its damage appearAnimation stays empty; Splintered Grasp is skipped.

Not edited: Splintered Grasp is the live pool jutsu Heavy Strike (S01, pUrUJX8Jml7fUIBXKsPwv), held by AIs across the
game; editing it would change its look everywhere and sever holders the repository cannot see. Skipped: no copy, no
upload (RUL-2026-11-03-112 item 4).

Edits are built from 470's fresh captures (the live records), changing only the named art fields; each capture is
compared with the repository's expectation (push/342 / 344 part 2 / 363 creates and edits, the 2026-10-25 capture for
Keelbind and Final Command) and the build stops on any drift (--accept-drift to build anyway, listing the drift).

Holders: push/skyglass_mark_fix.gen.py holders() (every AI whose newest RUN kit send holds an edited jutsu, mapped
from the committed results bundles to the committed manifests; rules are not sent; items re-sent per law 70), with
this generator's own outputs excluded. Keelbind and Final Command are legacy Ghost Ship records: the push/81-84
census holders (state/ghost_ship_legacy_jutsu_consumer_audit.json) are cross-checked and any not found is listed.
Do not hand-edit the outputs.
"""
import argparse
import copy
import glob
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = {"assets": 470, "unhide": 471, "unequip": 472, "edit": 473, "reequip": 474, "master": 475}
SLUG = {"assets": "skyglass_boss_fx_assets", "unhide": "skyglass_boss_fx_unhide", "unequip": "skyglass_boss_fx_unequip",
        "edit": "skyglass_boss_fx", "reequip": "skyglass_boss_fx_reequip", "master": "skyglass_boss_fx_master"}
PFX = "sg470_"
FXD = "art/skyglass_boss_fx/exports/"
META = FXD + "boss_v1_x3d.json"
INJECTABLE = False  # law 20, as push/431

# strip id -> asset name
ASSETS = {
    "ships_bell": "Skyglass FX - Ship's Bell",
    "broadside_field": "Skyglass FX - Broadside",
    "command_absolute_field": "Skyglass FX - Command Absolute",
    "crownfall": "Skyglass FX - Crownfall",
    "quench": "Skyglass FX - Quench",
    "exposed": "Skyglass FX - Exposed window",
    "recall": "Skyglass FX - Recall",
    "crown_aura": "Skyglass FX - The Crown's Will",
    "crimson_strike": "Skyglass FX - Final Command",
    "chain_wrap": "Skyglass FX - Chain wrap",
}
# The window strip plays ONCE, as the window opens (RUL-2026-11-03-112 item 2; the design placeholders had a
# staticAnimation loop, which covered the boss's portrait for the window round).
WINDOW_FIELD = "appearAnimation"

# live jutsu id -> (name, source, [(effect index, effect type, effect target, field, strip, design id)])
SLOTS = {
    "4mu7BPrMKOHXmvp5WKMmw": ("Ship's Bell", "342", [(0, "damage", "INHERIT", "appearAnimation", "ships_bell", "cp_bell_toll")]),
    "CxGrWF_wJepsT6W4MNkuq": ("Broadside", "342", [(0, "damage", "INHERIT", "appearAnimation", "broadside_field", "cp_broadside")]),
    "fXqcnsFlK-1w7rweBanZY": ("Command Absolute", "342", [(0, "damage", "INHERIT", "appearAnimation", "command_absolute_field", "cc_command_absolute")]),
    "ee4hRc-GiwDJkqCcnMDaX": ("Crownfall", "342", [(0, "damage", "INHERIT", "appearAnimation", "crownfall", "cc_crownfall")]),
    # damage [0] appearAnimation (ch_maw) stays empty: maw_field HELD BACK for a composite Maw (RUL-2026-11-03-112 item 3)
    "_hxcJFYdxVOsjs0ryzrFq": ("Maw of the Deep", "342", [(2, "weakness", "SELF", WINDOW_FIELD, "exposed", "ch_exposed")]),
    "5x2F8btsK8Gvfr0o3WtiE": ("Quench", "342", [(0, "damage", "INHERIT", "appearAnimation", "quench", "fw_quench"),
                                                (1, "weakness", "SELF", WINDOW_FIELD, "exposed", "fw_cracked")]),
    "sOooIuNeKScLskCCtgBMY": ("Lowered Guard", "342", [(0, "weakness", "SELF", WINDOW_FIELD, "exposed", "lg_lowered")]),
    "F6uu9fki0KdceKzxLVvKi": ("Binding: Seal Cross", "342", [(0, "damage", "INHERIT", "appearAnimation", "chain_wrap", "dt_control")]),
    "kjtW0Yjc3-QfJzrvrLyUT": ("Chain Hook", "342", [(0, "damage", "INHERIT", "appearAnimation", "chain_wrap", "chain-hook-hit")]),
    "bcbOllIWqHEopmQGHKDED": ("Stonebound Summons", "344-2", [(0, "summon", "INHERIT", "appearAnimation", "recall", "cc_recall")]),
    "ag8guPcS5Lkw_YwK3YyFG": ("Recall", "363", [(0, "summon", "INHERIT", "appearAnimation", "recall", "cc_recall")]),
    "UTLj47puRAwSnFwiSKCuN": ("The Crown's Will", "363", [(0, "increasedamagegiven", "INHERIT", "staticAnimation", "crown_aura", "cc_crown_aura")]),
    "PdD44PGaNv4MN5fOALhAF": ("Keelbind", "capture", [(0, "damage", "INHERIT", "appearAnimation", "chain_wrap", "Keelbind")]),
    "X2P22h8ApDmTZHjWpNO87": ("Final Command", "capture", [(0, "damage", "INHERIT", "appearAnimation", "crimson_strike", "cp_final_command")]),
}
NOT_SHIPPED = {"pUrUJX8Jml7fUIBXKsPwv": "Heavy Strike (Splintered Grasp; shared pool S01): skipped, no copy, no upload (RUL-2026-11-03-112 item 4)",
              "_hxcJFYdxVOsjs0ryzrFq": "Maw of the Deep damage[0].appearAnimation: left empty, maw_field held back (RUL-2026-11-03-112 item 3)"}
HELD = {"maw_field"}  # delivered by deliver_boss.py but not uploaded (RUL-2026-11-03-112 item 3)
LIB, LIB_BUNDLE = "push/342_skyglass_library.json", "harvests/inbox/tnr_results_1793426982231.json"
CC, CC_BUNDLE = "push/363_crownhold_captain_jutsu.json", "harvests/inbox/tnr_results_1793486035765.json"
SUMMON = "push/344_skyglass_copies_2.json"
CAPTURE = "harvests/inbox/tnr_results_1792900120886.json"  # newest committed record of Keelbind / Final Command
CENSUS = "state/ghost_ship_legacy_jutsu_consumer_audit.json"
ART_KEYS = ("appearAnimation", "staticAnimation", "staticAssetPath", "disappearAnimation")


def jload(p):
    return json.load(open(os.path.join(ROOT, p)))


def git(*a):
    return subprocess.check_output(["git", "-C", ROOT, *a], text=True).strip()


def mark_fix():
    spec = importlib.util.spec_from_file_location("mark_fix", os.path.join(ROOT, "push/skyglass_mark_fix.gen.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    base = mod.manifests
    own = tuple(f"{NUM[k]}_{SLUG[k]}" for k in NUM)
    mod.manifests = lambda: [(p, d) for p, d in base() if not os.path.basename(p).startswith(own)]
    return mod


def write(key, m):
    path = os.path.join(ROOT, "push", f"{NUM[key]}_{SLUG[key]}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"push/{NUM[key]}_{SLUG[key]}.json: {len(m['items'])} items")


def pack(paths):
    ref = git("log", "-1", "--format=%H", "HEAD", "--", *paths)
    files = {}
    for p in paths:
        disk = open(os.path.join(ROOT, p), "rb").read()
        if subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{p}"]) != disk:
            raise SystemExit(f"{p}: working copy differs from {ref}")
        files[os.path.basename(p)] = {"path": p, "sha256": hashlib.sha256(disk).hexdigest(), "bytes": len(disk)}
    return {"imgSizes": {k: v["bytes"] for k, v in files.items()}, "imagePack": {"ref": ref, "files": files}}


# ------------------------------------------------------------------------------------------------ 470
def build_assets():
    meta = {a["id"]: a for a in jload(META)["assets"]}
    assert set(meta) == set(ASSETS) | HELD and not HELD & set(ASSETS), sorted(set(meta) ^ (set(ASSETS) | HELD))
    used = {s for _, _, slots in SLOTS.values() for *_, s, _ in slots}
    assert used == set(ASSETS), sorted(used ^ set(ASSETS))
    items = []
    for sid, name in ASSETS.items():
        a = meta[sid]
        assert a["type"] == "ANIMATION" and a["speed"] == 50 and a["frame_px"] == 150, a
        items.append({"entity": "asset", "slot": "create", "phase": 1, "srcId": PFX + sid, "name": name, "data": {
            "name": name, "type": "ANIMATION", "image": "@img:" + os.path.basename(a["file"]), "folder": "SkyglassBossFX",
            "frames": a["frames"], "speed": a["speed"], "hidden": True, "onInitialBattleField": False,
            "licenseDetails": "TNR"}})
    reads = [{"proc": "jutsu.get", "input": {"id": jid}, "persist": "full"} for jid in SLOTS]
    write("assets", {
        "_note": (f"push/{NUM['assets']}, step 1 (assets; any day): the {len(items)} Skyglass boss set-piece animations "
                  "(art/skyglass_boss_fx/exports/*_v1_x3d.webp, boss_v1_x3d.json: 150 px frames, 50 ms) as HIDDEN "
                  f"ANIMATION gameAssets (law 16b), plus READ-ONLY jutsu.get captures of the {len(reads)} jutsu that will "
                  f"carry them, so push/{NUM['edit']} is built from the live records. Nothing else changes. Keep the "
                  f"results bundle: push/{NUM['unhide']}-{NUM['master']} are built from it (--from). Generated by "
                  "push/skyglass_boss_fx_ship.gen.py; do not hand-edit."),
        "dedupNames": True, **pack([meta[s]["file"] for s in ASSETS]),
        "capture": {"before": reads, "after": []}, "items": items})


# ------------------------------------------------------------------------------------------------ 471-475
def expected():
    """Repository expectation of each edited jutsu's effects (what 470's captures should show)."""
    exp = {}
    lib, lb = jload(LIB), jload(LIB_BUNDLE)
    for it in lib["items"]:
        jid = lb["idmap"].get(it.get("srcId"))
        if jid in SLOTS:
            exp[jid] = copy.deepcopy(it["data"]["effects"])
    cc, cb = jload(CC), jload(CC_BUNDLE)
    for it in cc["items"]:
        jid = cb["idmap"].get(it["srcId"])
        if jid in SLOTS:
            exp[jid] = copy.deepcopy(it["data"]["effects"])
    for it in jload(SUMMON)["items"]:
        if it.get("targetId") in SLOTS and "effects" in it["data"]:
            exp[it["targetId"]] = copy.deepcopy(it["data"]["effects"])
    cap = {}

    def walk(o):
        if isinstance(o, dict):
            if o.get("id") in SLOTS and isinstance(o.get("effects"), list) and o.get("name"):
                cap[o["id"]] = o["effects"]
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(jload(CAPTURE))
    for jid, (_, src, _) in SLOTS.items():
        if src == "capture":
            exp[jid] = copy.deepcopy(cap[jid])
    assert set(exp) == set(SLOTS), sorted(set(SLOTS) - set(exp))
    return exp


def norm(effects):
    return json.dumps(effects, sort_keys=True)


def build_from(bundle, accept_drift):
    b = json.load(open(bundle))
    ok = {e["srcId"]: e["id"] for e in b.get("entries") or []
          if e.get("slot") == "create" and e.get("state") == "ok" and e.get("id") and (e.get("srcId") or "").startswith(PFX)}
    need = {PFX + s for s in ASSETS}
    if not need <= set(ok):
        raise SystemExit(f"{os.path.basename(bundle)} is not push/{NUM['assets']}'s ok results: missing {sorted(need - set(ok))}")
    live = {c["data"]["id"]: c["data"] for c in b.get("captures") or []
            if c.get("proc") == "jutsu.get" and c.get("ok") and isinstance(c.get("data"), dict)}
    if set(SLOTS) - set(live):
        raise SystemExit(f"{os.path.basename(bundle)} lacks jutsu.get captures of {sorted(set(SLOTS) - set(live))}")
    aid = {s: ok[PFX + s] for s in ASSETS}
    exp = expected()
    edits, changes, drift = [], [], []
    for jid, (name, src, slots) in SLOTS.items():
        rec = live[jid]
        effs = copy.deepcopy(rec["effects"])
        if norm(effs) != norm(exp[jid]):
            drift.append(f"{name} ({jid}): live effects differ from the repository's {src} record")
        assert rec.get("hidden") is True, (name, "is not hidden: a visible save needs appearAnimation+appearSfx and does not unequip")
        for idx, typ, tgt, field, sid, design in slots:
            e = effs[idx]
            assert e["type"] == typ and e.get("target") == tgt, (name, idx, e["type"], e.get("target"))
            assert e["type"] != "visual", (name, idx, "art on a visual vanishes at the next action (RUL-2026-11-02-101)")
            assert not e.get(field) or e[field] == aid[sid], (name, idx, field, e.get(field), "already has art")
            changes.append(f"{name}: effects[{idx}] {typ} (target {tgt}).{field} {e.get(field, '')!r} -> {aid[sid]} "
                           f"({ASSETS[sid]}, anim_{sid}_v1_x3d; design id {design})")
            e[field] = aid[sid]
        # nothing but the named art fields changes
        for i, (a, c) in enumerate(zip(rec["effects"], effs)):
            diff = {k for k in set(a) | set(c) if a.get(k) != c.get(k)}
            assert diff <= set(ART_KEYS), (name, i, diff)
        edits.append({"entity": "jutsu", "slot": "edit", "targetId": jid, "name": f"{name}: boss set-piece animation",
                      "data": {"effects": effs, "injectableInBattle": INJECTABLE}})
    if drift and not accept_drift:
        raise SystemExit("drift (pass --accept-drift to build from the live records anyway):\n  " + "\n  ".join(drift))
    mf = mark_fix()
    hs = mf.holders(set(SLOTS))
    # An items list re-sent from an old manifest can carry an in-job ref (push/90's "@item:skyglass_katana"). Resolve
    # it to the literal id from the newest committed bundle's idmap: Forge's own idmap is browser storage, which the
    # quota fix clears, and validate.py flags an unresolvable ref.
    idmap = {}
    for _, _, bb in mf.bundles():
        idmap.update(bb.get("idmap") or {})

    def resolve(o):
        if isinstance(o, str) and o.startswith("@") and ":" in o:
            key = o.split(":", 1)[1]
            if key not in idmap:
                raise SystemExit(f"unresolvable ref {o} in a holder's items")
            return idmap[key]
        if isinstance(o, list):
            return [resolve(v) for v in o]
        if isinstance(o, dict):
            return {k: resolve(v) for k, v in o.items()}
        return o
    for h in hs:
        h["items"] = resolve(h["items"])
    names = {j: n for j, (n, _, _) in SLOTS.items()}
    found = {h["id"] for h in hs}
    census = jload(CENSUS)
    legacy = [f"{h['username']} ({h['aiId']}) held {names[h['jutsuId']]} in the push/81-84 census and has no committed "
              "run kit send holding it" for h in census["ghostShipHolders"] + census["otherHolders"]
              if h["jutsuId"] in ("PdD44PGaNv4MN5fOALhAF", "X2P22h8ApDmTZHjWpNO87") and h["aiId"] not in found]
    table = [f"{h['name']} ({h['id']}): kit {h['kitFrom']}, items {h['itemsFrom']}; off/on: {[names[j] for j in h['off']]}"
             for h in hs]
    held = {j for h in hs for j in h["off"]}
    unheld = sorted(names[j] for j in SLOTS if j not in held)
    pre = "Generated by push/skyglass_boss_fx_ship.gen.py --from " + os.path.basename(bundle) + "; do not hand-edit."
    write("unhide", {
        "_note": (f"push/{NUM['unhide']} (literal ids from push/{NUM['assets']}'s bundle, L01): the {len(aid)} boss "
                  "set-piece animation assets unhidden (law 16c: battles load only unhidden assets). " + pre),
        "items": [{"entity": "asset", "slot": "edit", "targetId": aid[s], "name": f"{n}: unhide", "data": {"hidden": False}}
                  for s, n in ASSETS.items()]})
    write("unequip", {
        "_note": (f"push/{NUM['unequip']}, law 18/60 step 1 of 3: every jutsu push/{NUM['edit']} edits comes off every "
                  "holder (the jutsu are hidden: a hidden save unequips every holder, routers/jutsu.ts:1117-1118). Kit "
                  "otherwise unchanged; items re-sent (law 70); rules untouched. MONDAY TO THURSDAY ONLY. " + pre),
        "_holders": table, "_notHeld": unheld, "_legacyNotFound": legacy,
        "items": [mf.ai_edit(h, [j for j in h["kit"] if j not in h["off"]], "boss FX jutsu off (law 18/60)") for h in hs]})
    write("edit", {
        "_note": (f"push/{NUM['edit']}, step 2 of 3 (after push/{NUM['unequip']}): the boss set-piece animations onto "
                  "their moves. Built from push/" + str(NUM["assets"]) + "'s live captures; only the art fields in "
                  "_changes differ (plus injectableInBattle false, law 20, as push/431). The jutsu stay hidden. " + pre),
        "_changes": changes, "_drift": drift, "_notShipped": NOT_SHIPPED, "items": edits})
    write("reequip", {
        "_note": (f"push/{NUM['reequip']}, step 3 of 3 (after push/{NUM['edit']}): every holder from push/{NUM['unequip']} "
                  "gets its exact current kit back (the newest run send carrying jutsus) and its items; rules "
                  "untouched. " + pre),
        "_holders": table, "items": [mf.ai_edit(h, h["kit"], "boss FX jutsu back on (law 18/60)") for h in hs]})
    srcs = [f"push/{NUM[k]}_{SLUG[k]}.json:{base}" for k, base in (("unhide", 0), ("unequip", 10), ("edit", 20), ("reequip", 30))]
    subprocess.run([sys.executable, os.path.join(ROOT, "push/master_manifest.gen.py"),
                    f"push/{NUM['master']}_{SLUG['master']}.json", *srcs], check=True, cwd=ROOT)
    print(f"{len(hs)} holders; edited jutsu not held by any AI: {unheld}")
    for line in legacy + drift:
        print("CHECK:", line)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--from", dest="bundle", help=f"push/{NUM['assets']} results bundle")
    ap.add_argument("--accept-drift", action="store_true")
    a = ap.parse_args()
    return build_from(a.bundle, a.accept_drift) if a.bundle else build_assets()


if __name__ == "__main__":
    main()
