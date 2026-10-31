#!/usr/bin/env python3
"""Generate push/342: the Skyglass set-piece library and the event's other new AI jutsu, all HIDDEN (jutsu creates only).

    python3 push/skyglass_library.gen.py

Records (state/skyglass_build/, harness provenance in state/skyglass_build/README.md):
  - the 36 records of library_spec.json (12 marks, 9 shared blasts, 6 bespoke signatures, Lowered Guard, 6 crew
    additions, Steady the Helm, and the Archive's enemies-only copy of Erupting Ground);
  - Raise the Gunwale (build_spec.json wreckNewJutsu, the Captain's phase-2 barrier; also used by the Fall's Captain copy);
  - Called to the Archive (hunts_spec.json, the Sealwright's summon of the Crown Stonebound at 40% power, hunts.params
    echoPower 40, RUL-2026-10-30-060 item 7);
  - Spreading Fire I-III (charts_spec.json newJutsu, the Fall's ember bands, RUL-2026-10-30-060 item 7).

Text: SKYGLASS_TEXT.md section 6.4 (names approved by RUL-2026-10-31-064 item 4; marks and blasts take the section's
shared descriptions), 6.3 (Steady the Helm) and the Spreading Fire lines. Where the text doc keeps a harness line
("kept", the crew additions "otherwise kept"), the harness record's text is used unchanged. Two records have no text in
SKYGLASS_TEXT.md (Raise the Gunwale, Called to the Archive): they are created with EMPTY description and battle text, a
reversible placeholder, and listed in the manifest's `_text_gaps` for the director.

Art (RUL-2026-10-30-059, -061 items 6 and 10): every jutsu image is the engine default (AI-only jutsu keep it). The
harness's symbolic animation names resolve to the live push/320 danger-language assets (state/skyglass_fx/asset_ids.json):
tg_* marks -> the tile (staticAssetPath) + its glint (staticAnimation); dt_heavy / dt_linger -> Skyglass Blast - Eruption.
Every other symbolic name (the 15 boss strips not yet uploaded, and the strips that need art) is left empty and listed
in `_placeholders` for the visual-asset push. Effect descriptions the harness left as "placeholder" take the engine's own
tag description (theninjarpg@3314d122 validators/combat.ts).

Literal ids: AI jutsu arrays need literal ids (law 17), so the AI copies are push/343, built from THIS manifest's results
bundle (python3 push/skyglass_copies.gen.py --library <342 bundle>). Do not hand-edit the output.
"""
import copy
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "state/skyglass_build")
NUM = 342
PFX = "sg342_"  # srcIds are unique across Forge jobs
DEFAULT_JUTSU_IMAGE = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"
GAME = "/home/claude/studie-tech/theninjarpg"
GAME_PIN = "3314d122"

import importlib.util
_spec = importlib.util.spec_from_file_location("skyglass_text", os.path.join(ROOT, "push/skyglass_text.py"))
T = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(T)


def spec(name):
    return json.load(open(os.path.join(BUILD, name)))


FX = json.load(open(os.path.join(ROOT, "state/skyglass_fx/asset_ids.json")))["assets"]
MARK_FX = {  # harness token -> (tile staticAssetPath, glint staticAnimation)
    "tg_heavy": (FX["Skyglass Mark - Heavy (tile)"], FX["Skyglass Mark - Heavy (glint)"]),
    "tg_control": (FX["Skyglass Mark - Binding (tile)"], FX["Skyglass Mark - Binding (glint)"]),
    "tg_linger": (FX["Skyglass Mark - Lingering Pool (tile)"], FX["Skyglass Mark - Lingering Pool (bubbles)"]),
    "tg_safe": (FX["Skyglass Mark - Safe (tile)"], FX["Skyglass Mark - Safe (floating emblem)"]),
}
BLAST_FX = {"dt_heavy": FX["Skyglass Blast - Eruption"], "dt_linger": FX["Skyglass Blast - Eruption"]}
# The harness's symbolic animation names are lowercase words joined by '_' or '-' (tg_heavy, cp_gunwale, mark-sigil);
# live values from the shape donors are real ids (mixed case and digits) or the engine's built-in "hit".
SYMBOLIC = re.compile(r"^[a-z]+(?:[_-][a-z]+)+$")


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


# ---------------------------------------------------------------- text (SKYGLASS_TEXT.md, verbatim)
def _code(cell):
    m = re.search(r"`([^`]*)`", cell)
    return m.group(1) if m else cell


def _para(prefix):
    hits = [l for l in T.lines() if l.startswith(prefix)]
    assert len(hits) == 1, prefix
    return hits[0]


def text_tables():
    lib = {}
    for row in T.table("### 6.4 Library jutsu"):
        rid = re.search(r"\(`([^`]+)`\)", row[0]).group(1)
        name = re.sub(r"\s*\(kept\)$", "", row[2])
        lib[rid] = {"name": name, "battleDescription": _code(row[3])}
    mark_desc = re.search(r"`description` for every mark: `([^`]+)`", " ".join(
        l for l in T.lines() if "`description` for every mark" in l or "For every shared blast" in l)).group(1)
    blast_desc = re.search(r"For every shared blast: `([^`]+)`", " ".join(
        l for l in T.lines() if "For every shared blast" in l)).group(1)
    sig = {}
    for row in T.table("Bespoke signatures"):
        sig[row[0]] = None if row[2] == "kept" else _code(row[2])
    L = T.lines()
    i = next(i for i, l in enumerate(L) if l.startswith("Fixes to crew additions"))
    ward = re.search(r"Proposed: `([^`]+)`", " ".join(L[i:i + 3])).group(1)
    echo_name = re.search(r"\*\*(Echo of Erupting Ground)\*\*", " ".join(T.lines())).group(1)
    embers_desc = re.search(r"`description` \(all three\): `([^`]+)`", _para("- `description` (all three)")).group(1)
    eb = _para("- `battleDescription`: I ")
    embers_battle = [re.search(rf"{n} `([^`]+)`", eb).group(1) for n in ("I", "II", "III")]
    helm = {"description": T.block("jutsu:Steady the Helm.description"),
            "battleDescription": T.block("jutsu:Steady the Helm.battleDescription")}
    return dict(lib=lib, mark=mark_desc, blast=blast_desc, sig=sig, ward=ward, echo=echo_name,
                embers=(embers_desc, embers_battle), helm=helm)


TX = text_tables()


# ---------------------------------------------------------------- records
def fx(effects, placeholders, where):
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
            if f == "appearAnimation" and v in BLAST_FX:
                e[f] = BLAST_FX[v]
            elif v and SYMBOLIC.match(v):
                placeholders.append(f"{where}: effects[{e['type']}].{f} = {v} (art pending; left empty)")
                e[f] = ""
        if e.get("description") in ("placeholder", "<p>placeholder</p>"):
            e["description"] = TAG_DESC[e["type"]]
        out.append(e)
    return out


KEEP = ("name", "description", "battleDescription", "jutsuType", "jutsuRank", "requiredRank", "requiredLevel",
        "jutsuWeapon", "target", "method", "range", "coordinateTargeting", "methodSize", "cooldown", "actionCostPerc",
        "healthCost", "chakraCost", "staminaCost", "healthCostReducePerLvl", "chakraCostReducePerLvl",
        "staminaCostReducePerLvl", "battleUsageType", "elementClassification", "statClassification", "extraBaseCost",
        "effects")


def jutsu(src, rec, name, desc, battle, placeholders, gaps=None):
    data = {k: copy.deepcopy(rec[k]) for k in KEEP if k in rec}
    data.update({"name": name, "description": desc, "battleDescription": battle, "jutsuType": "AI",
                 "hidden": True, "injectableInBattle": False, "bloodlineId": "", "villageId": "",
                 "image": DEFAULT_JUTSU_IMAGE})
    data["effects"] = fx(rec["effects"], placeholders, name)
    e = {"entity": "jutsu", "slot": "create", "srcId": PFX + src, "name": name, "data": data}
    if gaps is not None:
        gaps.append(f"jutsu {PFX + src} {name}: description and battleDescription not in SKYGLASS_TEXT.md; created EMPTY")
    return e


COOLDOWN_FLOOR = 3  # Forge refuses a jutsu with cooldown < 3 (forge/src/runner/lints.mjs L16; validate.py L16)


def cooldown_floor(L, rid, rec, notes):
    """Raise a harness cooldown of 2 to Forge's floor of 3 where that changes nothing in battle.

    A blast or signature fires only on the turn after its own mark (rule `has_effect <marker> >= 1`, marker 1 round)
    and every mark it answers has cooldown >= 3, so with readiness `roundsPassed >= cooldown` (theninjarpg@3314d122
    libs/combat/actions.ts ~331) a cooldown-3 blast is always ready when its marker is up; the marker tags
    (increasecooldown etc. with no actionsAffected) change no jutsu cooldown (actions.ts ~451-480). Ward of Command
    (2 rounds, cooldown 2, recast unconditionally: continuous) becomes 3 rounds / cooldown 3, which keeps it continuous.
    """
    rec = copy.deepcopy(rec)
    if rec["cooldown"] >= COOLDOWN_FLOOR:
        return rec
    recs = {r["id"]: r for r in L["records"]}
    r = recs[rid]
    if r.get("answersMark"):
        assert recs[r["answersMark"]]["record"]["cooldown"] >= COOLDOWN_FLOOR, rid
        notes.append(f"{rec['name']}: cooldown {rec['cooldown']} -> {COOLDOWN_FLOOR} (answers {r['answersMark']}, "
                     f"cooldown {recs[r['answersMark']]['record']['cooldown']}: no change in battle)")
    elif rid == "lib-ward-of-command":
        assert all(e["rounds"] == rec["cooldown"] for e in rec["effects"]), rec["effects"]
        for e in rec["effects"]:
            e["rounds"] = COOLDOWN_FLOOR
        notes.append(f"{rec['name']}: cooldown and rounds {rec['cooldown']} -> {COOLDOWN_FLOOR} (recast unconditionally: "
                     "still continuous)")
    else:
        raise SystemExit(f"{rid}: cooldown {rec['cooldown']} below Forge's floor and no equivalence argument")
    rec["cooldown"] = COOLDOWN_FLOOR
    return rec


def library(placeholders, gaps, notes):
    L = spec("library_spec.json")
    out = []
    for r in L["records"]:
        rid, rec, g = r["id"], r["record"], r["group"]
        if rid in TX["lib"]:
            name, battle = TX["lib"][rid]["name"], TX["lib"][rid]["battleDescription"]
            desc = TX["mark"] if g == "mark" else TX["blast"] if g == "shared blast" else rec["description"]
        elif g == "signature":
            name, desc = rec["name"], rec["description"]
            battle = TX["sig"][rec["name"]] if TX["sig"].get(rec["name"]) else rec["battleDescription"]
            assert rec["name"] in TX["sig"], rec["name"]
        elif rid == "lib-steady-the-helm":
            name, desc, battle = rec["name"], TX["helm"]["description"], TX["helm"]["battleDescription"]
        elif rid == "lib-ward-of-command":
            name, desc, battle = rec["name"], TX["ward"], rec["battleDescription"]
        elif g == "crew addition":
            name, desc, battle = rec["name"], rec["description"], rec["battleDescription"]
        elif rid == "hunt-stonebound-erupting-ground":
            name, desc, battle = TX["echo"], rec["description"], rec["battleDescription"]
        else:
            raise SystemExit(f"unclassified library record {rid}")
        out.append(jutsu(rid, cooldown_floor(L, rid, rec, notes), name, desc, battle, placeholders))
    assert len(out) == L["counts"]["total"] == 36
    return out


def extras(placeholders, gaps):
    out = []
    gun = next(j for j in spec("build_spec.json")["wreckNewJutsu"] if j["id"] == "dg-raise-the-gunwale")["record"]
    out.append(jutsu("dg-raise-the-gunwale", gun, gun["name"], "", "", placeholders, gaps))
    hs = spec("hunts_spec.json")
    call = next(j for j in hs["jutsu"] if j["id"] == "hunt-called-to-the-archive")["record"]
    call = copy.deepcopy(call)
    summon = next(e for e in call["effects"] if e["type"] == "summon")
    hp = spec("hunts.params.json")  # final pass (hunts_spec.json itself predates it: echoPower 60 there)
    summon["power"], summon["aiHp"] = hp["echoPower"], hp["echoHp"]
    assert (summon["power"], summon["aiHp"]) == (40, 15000), summon  # hunts.params final pass, RUL-2026-10-30-060 item 7
    out.append(jutsu("hunt-called-to-the-archive", call, call["name"], "", "", placeholders, gaps))
    desc, battles = TX["embers"]
    for i, (k, v) in enumerate(sorted(spec("charts_spec.json")["newJutsu"].items())):
        rec = v["record"]
        assert rec["name"] == f"Spreading Fire {'I' * (i + 1)}", rec["name"]
        out.append(jutsu(k, rec, rec["name"], desc, battles[i], placeholders))
    return out


def all_jutsu():
    placeholders, gaps, notes = [], [], []
    items = library(placeholders, gaps, notes) + extras(placeholders, gaps)
    assert all(e["data"]["cooldown"] >= COOLDOWN_FLOOR for e in items)
    names = [e["name"] for e in items]
    assert len(names) == len(set(n.lower() for n in names)), "duplicate jutsu names"
    return items, placeholders, gaps, notes


def harness_ids():
    """harness placeholder id -> srcId, for push/343 (rule and kit remapping)."""
    items, _, _, _ = all_jutsu()
    return {e["srcId"][len(PFX):]: e["srcId"] for e in items}


def main():
    items, placeholders, gaps, notes = all_jutsu()
    m = {"_note": (
        f"push/{NUM} (RUL-2026-10-30-059: hidden, engine-default images). The Skyglass set-piece library (36: marks, shared "
        "blasts, bespoke signatures, Lowered Guard, crew additions, Steady the Helm, Echo of Erupting Ground) plus Raise the "
        "Gunwale, Called to the Archive (Crown Stonebound at 40%) and Spreading Fire I-III: 41 AI jutsu creates, all hidden. "
        "Names and battle text: SKYGLASS_TEXT.md section 6.3/6.4 (RUL-2026-10-31-064 item 4). Nothing holds these yet; the AI "
        "copies that use them are push/343, built from this run's results bundle (literal ids, law 17). Generated by "
        "push/skyglass_library.gen.py; do not hand-edit."),
        "dedupNames": True, "_placeholders": placeholders, "_text_gaps": gaps, "_cooldown_floor": notes, "items": items}
    path = os.path.join(ROOT, f"push/{NUM}_skyglass_library.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{NUM}_skyglass_library.json: {len(items)} jutsu creates; {len(placeholders)} animation placeholders; "
          f"{len(gaps)} text gaps")


if __name__ == "__main__":
    main()
