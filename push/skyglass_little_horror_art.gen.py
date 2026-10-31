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
# Matched to the creature in the approved jar icon (IC09, director 2026-10-31: "look like the thing from the jar"),
# colours left to the player's palette. The engine prompt defaults to fur and a "companion", so the material is named.
ART_DIRECTION = ("Hairless, no fur or tufts: a round-bodied, frog-like rot creature with a plump torso, a big round "
                 "head and four short stubby legs with soft paw pads, and a short tapering tail. Its hide is glossy and "
                 "tar-slick, streaked with thick dripping slime in the palette's accent colour. Clouded crystal is "
                 "crusted into its hide in small irregular barnacle clusters, sitting flush, never standing up as "
                 "spikes, posts or a row. Its eyes are always pale skyglass cyan with a bright pinpoint highlight, "
                 "whatever the palette. "
                 "Its signature: an enormous grin that splits its face nearly ear to ear, packed with jagged white "
                 "teeth. Creepy-cute, mischievous, a little unsettling.")
DESCRIPTION = ("The Core tried to remember the ship's mascot and rebuilt it from the wreck's rot: a round, tar-slick "
               "thing dripping slime, crusted with clouded crystal, its grin far too wide and far too full of teeth. "
               "It has decided you are its crew.")
RANKS = [
    "A round, tar-slick rot creature on stubby legs with a huge toothy grin and pale cyan eyes, slime dripping off it, a few flush crystal barnacles on its back",
    "A little longer in the legs and steadier on its feet; the crystal barnacles spread in an uneven patch over its back",
    "Full adult size, still round-bodied; the grin reaches nearly ear to ear and the slime streaks run thicker",
    "Its teeth turn jagged and crystal-tipped and its paw claws darken; the grin is now plainly a weapon",
    "The barnacle patch fuses into one smooth crystal plate lying flat across its back and shoulders",
    "Slime streaks settle into bold painted patterns across its hide in the palette's accent colour",
    "The slime patterns glow faintly in its aura colour and the crystal plate lights from within",
    "A collar of tarred rigging rope with a small crystal medallion, worn alongside any collar, scarf or charm it already has",
    "Sitting up proud with one paw raised, head high, the crystal plate polished clear, grin wide",
    "The wreck's guardian: glossy and commanding, its crystal plate catching the light, the same enormous grin and cyan eyes",
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


def species_only():
    """push/381: the species' text again (379 already ran): no standing crystal spikes, skyglass-cyan eyes."""
    item = {"entity": "petSpecies", "slot": "edit", "targetId": SPECIES_ID,
            "name": "Little Horror: flush crystal barnacles, skyglass-cyan eyes",
            "data": {"rarity": "LEGENDARY", "description": DESCRIPTION, "artDirection": ART_DIRECTION, "rankConcepts": RANKS}}
    A2.write(381, "skyglass_little_horror_text", {"_note": ("push/381: Little Horror art direction and rank concepts "
             "revised after the second adoption render (director 2026-10-31: the back spikes looked ridiculous; eyes "
             "skyglass blue). Generated by push/skyglass_little_horror_art.gen.py --species; do not hand-edit."),
             "items": [item]})


if __name__ == "__main__":
    if sys.argv[1:2] == ["--species"]:
        species_only()
    elif sys.argv[1:2] == ["--unhide"]:
        unhide(sys.argv[2])
    else:
        build()
