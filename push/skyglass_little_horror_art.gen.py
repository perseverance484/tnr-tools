#!/usr/bin/env python3
"""The Little Horror's art pass (push/379, push/380; RUL-2026-10-31-085).

    python3 push/skyglass_little_horror_art.gen.py                    # 379: maw asset + Little Maw + species text
    python3 push/skyglass_little_horror_art.gen.py --unhide <379 bundle>   # 380: unhide the maw asset

379, phase 1: the maw animation (art/skyglass_boss_fx/exports/anim_maw_v1_x3.webp, 12 frames x 50 ms, 150 px frames)
as a HIDDEN ANIMATION gameAsset. Phase 2: Little Maw's damage effect uses it as appearAnimation (replacing Rallying
Echo's placeholder; its sound is kept, so the jutsu stays publishable), and the Little Horror species gets the refined
artDirection and rankConcepts (SKYGLASS_PETS.md; written for the engine's pet art prompt, libs/pets/appearance.ts:
four legs from rank 1, no spines or extra mouths, no named colours: the player's palette, trait and aura decide those).
Little Maw is published, so the edit does not unequip it from pets. 380 unhides the asset (battles load only unhidden
assets, law 16c). Do not hand-edit the outputs.
"""
import json, os, sys, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("a2", os.path.join(ROOT, "push", "skyglass_final_art2.gen.py"))
A2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(A2)
SPECIES_ID, MAW_ID = "eI2UFBlBTEhXpcHk5uBra", "GYy5K24tGkYIeGEJef3TW"
STRIP = "art/skyglass_boss_fx/exports/anim_maw_v1_x3.webp"
SRC = "sg379_anim_little_maw"
# Revised after the director's first adoption render (2026-10-31: a fluffy, big-eyed cute critter). The engine prompt
# defaults to "smooth species-specific fur" and calls it a "companion", so the text names the material explicitly:
# hairless, slick, wood-grained hide; crystal from rank 1; small eyes; a crooked grin. Never "small", "cute", "mascot".
ART_DIRECTION = ("Hairless: no fur, tufts or fluff anywhere. A lean, low four-legged creature built like a salamander "
                 "crossed with a hound, rebuilt from shipwreck rot. Its hide is slick, wet and glistening, with the grain "
                 "and seams of rotten hull planks, patched with barnacle crusts. A tail like a length of frayed, tarred "
                 "rope. Small glinting eyes, a mouth too wide for its head with crooked, uneven teeth. Flat clusters of "
                 "clouded crystal grow on its back like barnacles, in the palette's accent colour. Eerie, not cute.")
DESCRIPTION = ("The Core tried to remember the ship's mascot and rebuilt it from the wreck's rot: a hairless, dripping "
               "thing of soaked hull timber and frayed rope, crusted with clouded crystal, its grin too wide and crooked. "
               "It has decided you are its crew.")
RANKS = [
    "A lean, hairless rot creature low on four short legs, slick wood-grained hide, a crooked grin, flat crystal barnacles on its back",
    "Its legs lengthen and it stands steadier; the barnacles spread along its spine in a short line",
    "Adult size, low and sturdy; ship-plank grain shows through its hide and its rope-like tail is held up",
    "Its grin widens into a proper maw with crystal-tipped teeth; its claws look like tarred wood",
    "The barnacles fuse into one smooth crystal plate across its shoulders, one clean shape",
    "Seam lines painted across its body in the palette's accent colour, like caulking between hull planks",
    "The seam lines glow faintly in its aura colour and the crystal plate lights from within",
    "A guard of tarred rigging rope with a small crystal medallion, worn alongside any collar, scarf or charm it already has",
    "Head raised and one forepaw lifted as if standing watch on deck; the crystal plate polished clear",
    "The wreck's guardian: sleek and proud, its hide like lacquered hull timber, crystal catching the light, still grinning",
]


def build():
    effects = json.load(open(os.path.join(ROOT, "push/353_skyglass_little_maw_publish.json")))["items"][0]["data"]["effects"]
    assert effects[0]["type"] == "damage" and effects[0]["appearSfx"]
    effects[0]["appearAnimation"] = "@scene:" + SRC
    items = [A2.asset(SRC, "Little Maw bite", "ANIMATION", STRIP, "SkyglassBossFX", 12, 50),
             {"entity": "jutsu", "slot": "edit", "phase": 2, "targetId": MAW_ID, "name": "Little Maw: maw animation",
              "data": {"effects": effects, "injectableInBattle": False}},
             {"entity": "petSpecies", "slot": "edit", "phase": 2, "targetId": SPECIES_ID,
              "name": "Little Horror: refined art direction and rank concepts",
              "data": {"rarity": "LEGENDARY", "description": DESCRIPTION, "artDirection": ART_DIRECTION,
                       "rankConcepts": RANKS}}]
    m = {"_note": ("push/379: the Little Horror art pass (RUL-2026-10-31-085): the maw animation as a hidden asset, "
                   "Little Maw's appear animation, the species' refined art direction and rank concepts. Run 380 after. "
                   "Generated by push/skyglass_little_horror_art.gen.py; do not hand-edit."),
         "dedupNames": True, **A2.pack([STRIP]), "items": items}
    A2.write(379, "skyglass_little_horror_art", m)


def unhide(bundle):
    made = {e["srcId"]: e["id"] for e in json.load(open(bundle))["entries"]
            if e.get("entity") == "asset" and e.get("slot") == "create" and e.get("state") == "ok" and e.get("id")}
    c = A2.asset(SRC, "Little Maw bite", "ANIMATION", STRIP, "SkyglassBossFX", 12, 50)
    data = dict(c["data"], hidden=False)
    m = {"_note": f"push/380: unhides the Little Maw animation asset (from {os.path.basename(bundle)}).", "dedupNames": True,
         **A2.pack([STRIP]),
         "items": [{"entity": "asset", "slot": "edit", "targetId": made[SRC], "name": c["name"], "data": data}]}
    A2.write(380, "skyglass_little_horror_unhide", m)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--unhide"]:
        unhide(sys.argv[2])
    else:
        build()
