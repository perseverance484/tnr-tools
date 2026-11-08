#!/usr/bin/env python3
"""Ship the Dragon King's Impact v6l animation (approved by dauntless 2026-11-08) through the content review desk.

    python3 push/dragon_king_impact.gen.py [--draft]
        -> push/<A>_dragon_king_impact_assets.json   8 HIDDEN ANIMATION gameAssets (imagePack pinned, law 16b) and a
                                                     READ-ONLY jutsu.get capture of Dragon King's Impact (before).
                                                     Uploads images, so it runs in the browser Forge, not mcp_run.
    python3 push/dragon_king_impact.gen.py --from <A results bundle>
        -> push/<B>_dragon_king_impact_unhide.json   the 8 assets unhidden by literal id (law 16c: battles load only
                                                     unhidden assets). Unused by anything until the ticket is applied.
        -> push/<C>_dragon_king_impact_suggest.json  mode "suggest": ONE review desk ticket (category ANIMATION) on the
                                                     live jutsu FytS2iqFInf1go6WhOvUU. Nothing changes in the game
                                                     until a reviewer approves it on the desk.

The ticket changes art fields only, built from A's fresh capture of the live record:
  effects[0] damage: appearAnimation stock fire (XznC_jJ3WI-UdHFFQ_0fD) -> "" (a damage appear is drawn twice,
             so the explosion rides the visual slices); appearSfx moves to the c0 slice (same moment, and a visible
             save needs one effect with both appearAnimation and appearSfx, routers/jutsu.ts:1151).
  effects[1] increasedamagegiven (SELF, 2 rounds): staticAnimation stock fire -> smoulder loop.
  + 7 zero-impact `visual` tags (target COORDINATES, power 2, rounds 1; a COORDINATES tag is stamped only on its own
    tiles, util.ts getActionAffectedTiles, so the damage still hits the target alone):
      CASTER (0,-2) (0,-1) (0,0): cast_n2 cast_n1 cast_c0 (rise in flame, 19 frames)
      TARGET (0,-2) (0,-1) (0,0) (0,1): n2 n1 c0 p1 (dive, impact, fireball with the face glimpse, smoke; 36 frames)
    Offsets are column/row (longitude/latitude added to the origin's col/row, targeting.ts:64-69). All slices sit
    in the origin's own column, so the odd-q half-row shift never tears them.
Effects [2] afterburn and [3] wound are untouched. The build stops if the live effects differ from what this
generator expects (--accept-drift to build anyway, listing the drift).
Do not hand-edit the outputs.
"""
import argparse
import copy
import hashlib
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = {"assets": 533, "unhide": 534, "suggest": 535}  # check push/ for the next free numbers before committing
SLUG = {"assets": "dragon_king_impact_assets", "unhide": "dragon_king_impact_unhide",
        "suggest": "dragon_king_impact_suggest"}
PFX = "dki533_"
META = "art/dragon_king_impact/exports/dki_v6l.json"
JUTSU = "FytS2iqFInf1go6WhOvUU"
STOCK_FIRE = "XznC_jJ3WI-UdHFFQ_0fD"
HIT_SFX = "9-b8hbTXA019dgn8yyr3j"
FOLDER = "DragonKingImpact"

ASSETS = {  # strip id -> asset name
    "cast_n2": "Dragon King's Impact - rise, 2 rows above caster",
    "cast_n1": "Dragon King's Impact - rise, 1 row above caster",
    "cast_c0": "Dragon King's Impact - rise, caster hex",
    "n2": "Dragon King's Impact - dive, 2 rows above target",
    "n1": "Dragon King's Impact - dive, 1 row above target",
    "c0": "Dragon King's Impact - impact, target hex",
    "p1": "Dragon King's Impact - impact, 1 row below target",
    "smoulder": "Dragon King's Impact - scorched caster loop",
}
# visual tags in draw order: (strip, origin, col, row, carries the hit sound)
SLICES = [
    ("cast_n2", "CASTER", 0, -2, False),
    ("cast_n1", "CASTER", 0, -1, False),
    ("cast_c0", "CASTER", 0, 0, False),
    ("n2", "TARGET", 0, -2, False),
    ("n1", "TARGET", 0, -1, False),
    ("c0", "TARGET", 0, 0, True),
    ("p1", "TARGET", 0, 1, False),
]
TITLE = "New Dragon King's Impact animation"
RATIONALE = (
    "Replaces the stock orange fire on Dragon King's Impact with its own animation: the caster rises in flame, a fire "
    "dragon dives from the sky onto the target and bursts into a rolling fireball where you catch a glimpse of its "
    "face, and the caster smoulders while the damage buff lasts. Only art changes: the stock fire comes off the hit "
    "and the buff, seven art-only visual slices carry the clip (the hit sound moves onto the impact slice), and "
    "damage, targeting and numbers are untouched.")


def jload(p):
    return json.load(open(os.path.join(ROOT, p)))


def git(*a):
    return subprocess.check_output(["git", "-C", ROOT, *a], text=True).strip()


def write(key, m):
    path = os.path.join(ROOT, "push", f"{NUM[key]}_{SLUG[key]}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"push/{NUM[key]}_{SLUG[key]}.json: {len(m['items'])} items")


def pack(paths, draft):
    ref = "DRAFT-not-committed" if draft else git("log", "-1", "--format=%H", "HEAD", "--", *paths)
    files = {}
    for p in paths:
        disk = open(os.path.join(ROOT, p), "rb").read()
        if not draft and subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{p}"]) != disk:
            raise SystemExit(f"{p}: working copy differs from {ref}")
        files[os.path.basename(p)] = {"path": p, "sha256": hashlib.sha256(disk).hexdigest(), "bytes": len(disk)}
    return {"imgSizes": {k: v["bytes"] for k, v in files.items()}, "imagePack": {"ref": ref, "files": files}}


def build_assets(draft):
    meta = {a["id"]: a for a in jload(META)["assets"]}
    assert set(meta) == set(ASSETS), sorted(set(meta) ^ set(ASSETS))
    items = []
    for sid, name in ASSETS.items():
        a = meta[sid]
        assert a["type"] == "ANIMATION" and a["frame_px"] == 112 and a["speed"] in (60, 80), a
        assert a["bytes"] < 450_000, a
        items.append({"entity": "asset", "slot": "create", "phase": 1, "srcId": PFX + sid, "name": name, "data": {
            "name": name, "type": "ANIMATION", "image": "@img:" + os.path.basename(a["file"]), "folder": FOLDER,
            "frames": a["frames"], "speed": a["speed"], "hidden": True, "onInitialBattleField": False,
            "licenseDetails": "TNR"}})
    write("assets", {
        "_note": (f"push/{NUM['assets']}, step 1 of 3 (any day): the Dragon King's Impact v6l strips "
                  "(art/dragon_king_impact/exports, dki_v6l.json: 112 px frames, 60 ms, 80 ms for the smoulder loop) as "
                  "HIDDEN ANIMATION gameAssets (law 16b), plus a READ-ONLY jutsu.get capture of Dragon King's Impact "
                  f"({JUTSU}) so the ticket is built from the live record. Nothing else changes. Uploads images: run it "
                  f"in the browser Forge. Keep the results bundle: push/{NUM['unhide']} and {NUM['suggest']} are built "
                  "from it (--from). Generated by push/dragon_king_impact.gen.py; do not hand-edit."),
        "dedupNames": True, **pack([meta[s]["file"] for s in ASSETS], draft),
        "capture": {"before": [{"proc": "jutsu.get", "input": {"id": JUTSU}, "persist": "full"}], "after": []},
        "items": items})


def expected_effects():
    """The live effects as read on 2026-11-08 (art fields are what the ticket changes)."""
    return [("damage", "INHERIT", STOCK_FIRE, ""), ("increasedamagegiven", "SELF", "", STOCK_FIRE),
            ("afterburn", "SELF", "", ""), ("wound", "INHERIT", "", "")]


def visual(aid, sid, origin, col, row, sfx):
    where = {(-2): "2 rows above", (-1): "1 row above", 0: "on", 1: "1 row below"}[row]
    return {"type": "visual", "power": 2, "rounds": 1, "target": "COORDINATES", "direction": "offence",
            "calculation": "static", "powerPerLevel": 0,
            "description": f"Dragon King's Impact: {sid} slice {where} the {origin.lower()} (art only)",
            "appearAnimation": aid, "appearSfx": HIT_SFX if sfx else "", "staticAnimation": "", "staticAssetPath": "",
            "disappearAnimation": "", "disappearSfx": "",
            "coordinateTargeting": {"origin": origin, "selection": "ALL",
                                    "coordinates": [{"longitude": col, "latitude": row}]}}


def build_from(bundle, accept_drift):
    b = json.load(open(bundle))
    ok = {e["srcId"]: e["id"] for e in b.get("entries") or []
          if e.get("slot") == "create" and e.get("state") == "ok" and e.get("id") and (e.get("srcId") or "").startswith(PFX)}
    need = {PFX + s for s in ASSETS}
    if not need <= set(ok):
        raise SystemExit(f"{os.path.basename(bundle)} is not push/{NUM['assets']}'s ok results: missing {sorted(need - set(ok))}")
    live = {c["data"]["id"]: c["data"] for c in b.get("captures") or []
            if c.get("proc") == "jutsu.get" and c.get("ok") and isinstance(c.get("data"), dict)}
    if JUTSU not in live:
        raise SystemExit(f"{os.path.basename(bundle)} lacks the jutsu.get capture of {JUTSU}")
    aid = {s: ok[PFX + s] for s in ASSETS}
    rec = live[JUTSU]
    effs = copy.deepcopy(rec["effects"])
    drift = []
    exp = expected_effects()
    shape = [(e["type"], e.get("target"), e.get("appearAnimation", ""), e.get("staticAnimation", "")) for e in effs]
    if shape != exp:
        drift.append(f"live effects {shape} differ from the expected {exp}")
    if effs and effs[0].get("appearSfx") != HIT_SFX:
        drift.append(f"damage appearSfx is {effs[0].get('appearSfx')!r}, expected {HIT_SFX}")
    if any(e["type"] == "visual" for e in effs):
        drift.append("the live record already has visual tags")
    if drift and not accept_drift:
        raise SystemExit("drift (pass --accept-drift to build from the live record anyway):\n  " + "\n  ".join(drift))
    assert rec.get("hidden") is False and rec.get("injectableInBattle") is False, "expected a visible, non-injectable jutsu"
    changes = []
    d = effs[0]
    assert d["type"] == "damage"
    changes.append(f"effects[0] damage.appearAnimation {d['appearAnimation']!r} -> '' ; appearSfx {d['appearSfx']!r} -> '' "
                   "(moves to the c0 slice)")
    d["appearAnimation"], d["appearSfx"] = "", ""
    s = effs[1]
    assert s["type"] == "increasedamagegiven" and s.get("target") == "SELF"
    changes.append(f"effects[1] increasedamagegiven.staticAnimation {s['staticAnimation']!r} -> {aid['smoulder']} "
                   "(scorched caster loop)")
    s["staticAnimation"] = aid["smoulder"]
    for sid, origin, col, row, sfx in SLICES:
        effs.append(visual(aid[sid], sid, origin, col, row, sfx))
        changes.append(f"+ visual {origin} ({col},{row}) appearAnimation {aid[sid]} ({ASSETS[sid]})"
                       + (f", appearSfx {HIT_SFX}" if sfx else ""))
    # nothing but art fields changes on the original four effects
    art = {"appearAnimation", "appearSfx", "staticAnimation"}
    for i, (a, c) in enumerate(zip(rec["effects"], effs)):
        diff = {k for k in set(a) | set(c) if a.get(k) != c.get(k)}
        assert diff <= art, (i, diff)
    # a visible save needs one effect with both appearAnimation and appearSfx (routers/jutsu.ts:1151)
    assert any(e.get("appearAnimation") and e.get("appearSfx") for e in effs)
    pre = "Generated by push/dragon_king_impact.gen.py --from " + os.path.basename(bundle) + "; do not hand-edit."
    write("unhide", {
        "_note": (f"push/{NUM['unhide']}, step 2 of 3 (literal ids from push/{NUM['assets']}'s bundle): the "
                  f"{len(aid)} Dragon King's Impact animation assets unhidden (law 16c). No record uses them until "
                  f"push/{NUM['suggest']}'s ticket is approved. " + pre),
        "items": [{"entity": "asset", "slot": "edit", "targetId": aid[s], "name": f"{n}: unhide", "data": {"hidden": False}}
                  for s, n in ASSETS.items()]})
    write("suggest", {
        "_note": (f"push/{NUM['suggest']}, step 3 of 3 (after push/{NUM['unhide']}): ONE review desk ticket on the live "
                  f"jutsu Dragon King's Impact ({JUTSU}). Suggest mode: nothing changes until a reviewer approves it. "
                  f"Built from push/{NUM['assets']}'s live capture; only the art fields in _changes differ. " + pre),
        "mode": "suggest",
        "suggestion": {"category": "ANIMATION", "title": TITLE, "rationale": RATIONALE},
        "_changes": changes, "_drift": drift,
        "items": [{"entity": "jutsu", "slot": "edit", "phase": 1, "targetId": JUTSU, "name": "Dragon King's Impact",
                   "data": {"effects": effs}, "suggestion": {"rationale": RATIONALE}}]})
    for line in drift:
        print("CHECK:", line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="bundle", help=f"push/{NUM['assets']} results bundle")
    ap.add_argument("--accept-drift", action="store_true")
    ap.add_argument("--draft", action="store_true", help="skip the commit pin (preview only; never run a draft)")
    a = ap.parse_args()
    if a.bundle:
        build_from(a.bundle, a.accept_drift)
    else:
        build_assets(a.draft)


if __name__ == "__main__":
    main()
