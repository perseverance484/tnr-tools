#!/usr/bin/env python3
"""The Mother of Echoes (the Skyglass uber, RUL-2026-11-01-093..096, -097, -099..103): build manifests from the
offline-tested spec on fable/mother-of-echoes-sim.

    python3 push/mother_of_echoes.gen.py
        -> push/440_mother_of_echoes_jutsu.json        (HIDDEN creates: every new jutsu that names no AI)
    python3 push/mother_of_echoes.gen.py --step templates --bundles <440 bundle>
        -> push/461_mother_of_echoes_templates.json    (HIDDEN creates: the 5 summon-template AIs)
    python3 push/mother_of_echoes.gen.py --step summons --bundles <440> <461>
        -> push/462_mother_of_echoes_summons.json      (HIDDEN creates: the 6 summon jutsu, aiId literal)
    python3 push/mother_of_echoes.gen.py --step bosses --bundles <440> <461> <462>
        -> push/463_mother_of_echoes_bosses.json       (HIDDEN creates: the 4 boss AIs, inArena false)
    python3 push/mother_of_echoes.gen.py --step quest --bundles <440, 461-463> --economy <417>
        -> push/464_mother_of_echoes_quest.json        (the HIDDEN battle pyramid, one repeatable quest)

The final push (2026-11-04; docs/design/MOTHER_OF_ECHOES_ART.md; law 16b/16c, law 18) is TWO jobs. It supersedes the
old --step publish (465), which is gone:
    python3 push/mother_of_echoes.gen.py --step final --bundles <440, 461-463> --economy <417>
        -> push/466_mother_of_echoes_final.json        (JOB 1, phases 10, 30-50: hidden art assets, law 18
                                                         unequip, the 53 jutsu with art, the 9 AIs re-equipped with
                                                         avatars; everything that fights stays hidden)
    python3 push/mother_of_echoes.gen.py --step golive --bundles <440, 461-464> --economy <417> --from <466 bundle>
        -> push/467_mother_of_echoes_go_live.json      (JOB 2: the FX unhidden, then the quest published with its art)
Job 2 needs job 1's bundle for one reason: the FX unhide is an edit, Forge sends an edit's targetId as written (no
@ref resolution there), and lint L13 refuses creating them visible. 466 and 467 take every jutsu/AI record from the
spec at SPEC_REF, so a re-tune (pass 6) is the one-line SPEC_REF bump plus a rebuild of 466.

Every step after 440 needs literal ids from earlier results bundles (law 17, ID provenance law): AI equip arrays and
rule jutsuIds, summon aiIds and quest opponentAIs / entry items / rewards. `--bundles` takes any number of results
bundles; ids are read from their `entries` (create, state ok) and `idmap`, only for this generator's srcIds, and every
id a step needs must be present or the step refuses. `--economy` is push/417's results bundle (the four shards, the
Heartglass and The Remainder tokens).

Source of truth: harness/skyglass_wreck_sim/mother_of_echoes_spec.json at SPEC_REF (pinned below and in every
manifest's _note). The spec is read with `git show`, so fetch fable/mother-of-echoes-sim first. Records are taken as
the harness ran them (theninjarpg@3314d122 JutsuValidator / AiRule / insertAiSchema valid); this generator only
(1) drops harness-only keys, (2) maps art names to live asset ids or placeholders, (3) maps harness ids (moe-*) to
srcIds or literal ids, (4) refuses repeated display names (the game has unique name indexes on jutsu and AI usernames).

Do not hand-edit the outputs.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC_REF = "780907a7dd281717cc08b443919a9982618676d2"  # fable/mother-of-echoes-sim: pass 6 calibrated to the live log (2026-11-05), ground Recasts; the last spec with only director-approved changes
SPEC_PATH = "harness/skyglass_wreck_sim/mother_of_echoes_spec.json"
PFX = "sg440_"
ECON = "sg417_"
# 441 was taken by a concurrent session (push/441_dusk_dawn_variants.json); later steps use 461-465.
N = {"jutsu": 440, "templates": 461, "summons": 462, "bosses": 463, "quest": 464, "publish": 465}
SLUG = {"jutsu": "mother_of_echoes_jutsu", "templates": "mother_of_echoes_templates",
        "summons": "mother_of_echoes_summons", "bosses": "mother_of_echoes_bosses",
        "quest": "mother_of_echoes_quest", "publish": "mother_of_echoes_publish"}

PLACEHOLDER = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"  # engine default (45e)
CORE_CHAMBER = "81DATu13hATfbkPuLT54E"  # scene asset reconstruction_chamber (push/339), placeholder scene
BLANK = "1YXbXYW2wz3GETVMb6DT6"  # Blank Scene Character (push/383-385 publish rule)
STOLEN_FORM = "VuFuBtE7h5B1nnA2J1lFZ"  # live, reused as-is (34 holders; never edited)
HEAVY_ARMOR = "h-V9uiuxbL7lAWkO6nZWt"  # AI Heavy Armor (live item)
ENGINE_ACTIONS = {"basicAttack", "wait"}  # built-in action ids a rule may name (no record)

# Live Skyglass danger-language art (push/431, RUL-2026-11-02-101): field -> asset id. Marks ride the
# increaseregeneration carrier; pool art sits on the lasting effect (no disappear animation).
APPEAR, VANISH = "bJy2IjRKmAVYEoXUYmXv5", "k8J4ic-KEz9ewEq1gAszr"
TG = {
    "tg_heavy": {"staticAssetPath": "dGCN9ZaoyXwDK9E3ZuWgU", "staticAnimation": "dL1vh_PNbZQ9m6nYwGnFa",
                 "appearAnimation": APPEAR, "disappearAnimation": VANISH},
    "tg_control": {"staticAssetPath": "M2oqurvH5jYkuCeDafnFK", "staticAnimation": "ZZ2YrtIAxfnlHAzOHXSgl",
                   "appearAnimation": APPEAR, "disappearAnimation": VANISH},
    "tg_safe": {"staticAssetPath": "-hIV18piGe0EcC0u6eN8d", "staticAnimation": "v9nA0cPU5NXxBXoONhdLH",
                "appearAnimation": APPEAR, "disappearAnimation": VANISH},
    "tg_linger": {"staticAssetPath": "PoG_KDERWlvyj7MsKSDW2", "staticAnimation": "qlGYJizxxxdd794Jea6lB",
                  "appearAnimation": APPEAR, "disappearAnimation": ""},
}
# tg_etch has no live art yet: the Etching marks borrow the violet control tile so they stay readable (RUL-101 item 3).
TG_STANDIN = {"tg_etch": "tg_control"}  # used by the 440-464 creates only; the art pass (481) maps tg_etch to 466's assets

# ---------------------------------------------------------------------------------------------------------------
# Art pass (466-467; docs/design/MOTHER_OF_ECHOES_ART.md). Files are pinned by the newest commit touching them.
# ---------------------------------------------------------------------------------------------------------------
N.update({"final": 466, "golive": 477, "tune": 476, "art2": 478, "art2_unhide": 479})  # 465 (the bare publish) superseded; 467 became the test-art job (push/mother_of_echoes_test_art.gen.py), so the go-live is 477
SLUG.update({"final": "mother_of_echoes_final", "golive": "mother_of_echoes_go_live", "tune": "mother_of_echoes_tune",
             "art2": "mother_of_echoes_custom_art", "art2_unhide": "mother_of_echoes_custom_art_unhide"})
ART = "art/mother_of_echoes/exports/"
FXDIR = "art/mother_of_echoes_fx/exports/"
FX_META = "art/mother_of_echoes_fx/exports/moe_fx_v1.json"
AID = "sg466_"
# Code-built FX: asset key -> (file, display name). Frames, speed and type come from FX_META.
FX = {
    "etch_tile": ("tile_moe_etch_v3.webp", "Mother of Echoes FX - Etching mark"),
    "etch_glint": ("anim_moe_etch_glint_v1.webp", "Mother of Echoes FX - Etching glint"),
    "recast": ("anim_moe_recast_v1.webp", "Mother of Echoes FX - Recast"),
    "guard_open": ("anim_moe_guard_open_v2.webp", "Mother of Echoes FX - Guard open"),
    "quiet": ("anim_moe_quiet_v1.webp", "Mother of Echoes FX - The Quiet"),
    "lancet": ("anim_moe_lancet_v2.webp", "Mother of Echoes FX - Glass Lancet"),
    "feeler": ("anim_moe_feeler_v2.webp", "Mother of Echoes FX - The Listening"),
    "lull": ("anim_moe_lull_v3.webp", "Mother of Echoes FX - The Glass Falls Quiet"),
    "still": ("anim_moe_still_dark_v2.webp", "Mother of Echoes FX - Nothing Moves"),
    "breath": ("anim_moe_breath_draw_v1.webp", "Mother of Echoes FX - Breathless Pull"),
    "lucid": ("anim_moe_lucid_aura_v1.webp", "Mother of Echoes FX - Lucid"),
    "likeness": ("anim_moe_likeness_ring_v2.webp", "Mother of Echoes FX - Your Likeness"),
    "worn": ("anim_moe_worn_ash_v2.webp", "Mother of Echoes FX - Raise the Worn"),
    "cradle": ("anim_moe_cradle_v2.webp", "Mother of Echoes FX - Cradle"),
    "flood": ("anim_moe_flood_mask_v1.webp", "Mother of Echoes FX - The Names Flood In"),
}
SCENES = {  # key -> (file, name, quest nodes). "content" is the quest-level sceneBackground.
    "heart": ("scene_moe_heart.webp", "Mother of Echoes Scene - The Heart of the Mother Glass",
              ("content", "d_intro1", "d_intro2", "d_open", "b_act1", "f_lost")),
    "stilling": ("scene_moe_stilling.webp", "Mother of Echoes Scene - The Stilling", ("d_act2", "b_act2")),
    "impression": ("scene_moe_impression.webp", "Mother of Echoes Scene - A Good Impression",
                   ("d_act3", "b_act3", "w_clear")),
}
ERUPTION, CRYSTAL_SHARD = "Z9j8J7ZmAjiaxH2S4nDy8", "TAu9k8ifgteP6HBofoKn7"  # live Skyglass Blast strips (reuse live)
# Custom set (push/478, director 2026-11-05: no borrowed animations; art3 brief, same day: "a high end boss fight ...
# pull out all the stops"). Every slot that borrowed a live Skyglass or library strip gets a Mother of Echoes strip
# keeping the event's danger grammar, and the material follows the story: Act I Heartglass (crystal, framed facets),
# Act II the turn (the Remainder's black cracks and smoke creeping into the Heartglass), Act III the Remainder (thorned
# dark shards, teal-cyan vein light). docs/design/MOTHER_OF_ECHOES_ART.md. Asset key -> (file, display name); srcId
# AID2 + key. FX2: art/mother_of_echoes_fx/build_fx.py CUSTOM (moe_fx_v1.json); FX3: build_fx_a3.py (moe_fx_a3.json).
AID2 = "sg478_"
PRACTICE_QUEST = "YDmKO6fp2vBRnTf7fHWQZ"  # push/469 run: harvests/inbox/tnr_results_1793840873454.json (VERIFIED)
FX2 = {
    "control_glint": ("anim_moe_control_glint_v1.webp", "Mother of Echoes FX - Hush lock loop"),
    "control_appear": ("anim_moe_control_appear_v1.webp", "Mother of Echoes FX - Hush lock arrives"),
    "linger_tile": ("tile_moe_linger_v1.webp", "Mother of Echoes FX - Seeping pool"),
    "linger_glint": ("anim_moe_linger_glint_v1.webp", "Mother of Echoes FX - Seeping pool loop"),
    "linger_appear": ("anim_moe_linger_appear_v1.webp", "Mother of Echoes FX - Seeping pool arrives"),
    "safe_tile": ("tile_moe_safe_v1.webp", "Mother of Echoes FX - Safe pane"),
    "safe_glint": ("anim_moe_safe_glint_v1.webp", "Mother of Echoes FX - Safe pane loop"),
    "safe_appear": ("anim_moe_safe_appear_v1.webp", "Mother of Echoes FX - Safe pane arrives"),
    "etch_appear": ("anim_moe_etch_appear_v1.webp", "Mother of Echoes FX - Etching cut"),
    "grasp": ("anim_moe_grasp_v1.webp", "Mother of Echoes FX - Grasp"),
    "echo_strike": ("anim_moe_echo_strike_v1.webp", "Mother of Echoes FX - Echo strike"),
    "pull": ("anim_moe_pull_v1.webp", "Mother of Echoes FX - Pull"),
    "shove": ("anim_moe_shove_v1.webp", "Mother of Echoes FX - Shove"),
    "mend": ("anim_moe_mend_v1.webp", "Mother of Echoes FX - Worn Mending"),
}
FX3_META = "art/mother_of_echoes_fx/exports/moe_fx_a3.json"
ROMAN = {"i": "I", "ii": "II", "iii": "III"}
FX3 = {
    **{f"heavy_tile_{a}": (f"tile_moe_heavy_{a}_a3.webp", f"Mother of Echoes FX - Heavy mark (Act {r})")
       for a, r in ROMAN.items()},
    **{f"heavy_glint_{a}": (f"anim_moe_heavy_glint_{a}_a3.webp", f"Mother of Echoes FX - Heavy mark loop (Act {r})")
       for a, r in ROMAN.items()},
    **{f"heavy_appear_{a}": (f"anim_moe_heavy_appear_{a}_a3.webp", f"Mother of Echoes FX - Heavy mark arrives (Act {r})")
       for a, r in ROMAN.items()},
    "control_dark": ("tile_moe_control_dark_a3.webp", "Mother of Echoes FX - Hush lock mark (the Silence)"),
    "linger_dark": ("tile_moe_linger_dark_a3.webp", "Mother of Echoes FX - Seeping pool (the Remainder)"),
    "refraction": ("anim_moe_refraction_a3.webp", "Mother of Echoes FX - Refraction Breaks (Heartglass)"),
    "recast": ("anim_moe_recast_a3.webp", "Mother of Echoes FX - Recast (the turn)"),
    **{f"enrage_w{k}": (f"anim_moe_enrage_w{k}_a3.webp", f"Mother of Echoes FX - The Glass Remembers, wave {k + 1}")
       for k in range(4)},
    **{f"shatterfall_w{k}": (f"anim_moe_shatterfall_w{k}_a3.webp", f"Mother of Echoes FX - Shatterfall, wave {k + 1}")
       for k in range(5)},
    **{f"glassfall_w{k}": (f"anim_moe_glassfall_w{k}_a3.webp", f"Mother of Echoes FX - Glassfall, wave {k + 1}")
       for k in range(3)},
    **{f"flood_w{k}": (f"anim_moe_flood_w{k}_a3.webp", f"Mother of Echoes FX - The Names Flood In, wave {k + 1}")
       for k in range(4)},
    **{f"rise_{k}": (f"anim_moe_rise_{k}_a3.webp", f"Mother of Echoes FX - {n} rises") for k, n in
       (("feeler", "A feeler"), ("likeness", "Your likeness"), ("worn", "The Worn"))},
    **{f"aura_{k}": (f"anim_moe_aura_{k}_a3.webp", f"Mother of Echoes FX - {n} aura") for k, n in
       (("sayo1", "Sayo"), ("silence", "The Silence"), ("sayo2", "The Glasswright"), ("saint", "The Saint"))},
    **{f"flourish_{k}": (f"anim_moe_flourish_{k}_a3.webp", f"Mother of Echoes FX - {n} rises to fight") for k, n in
       (("sayo1", "Sayo"), ("silence", "The Silence"), ("sayo2", "The Glasswright"), ("saint", "The Saint"))},
}
# Drawn for the per-boss act buffs the sim designs (director 2026-11-05: a real thematic positive-power buff per boss,
# not a 1-power carrier). Created and unhidden with the set; wired when the buff tags land (coordinated via main).
FX3_UNWIRED = {k for k in FX3 if k.startswith(("aura_", "flourish_"))}
# Boss entrances (art4; director after the live test, 2026-11-05: "Boss intro animation was a bit underwhelming but the
# aura was cool"): art/mother_of_echoes_fx/build_fx_a4.py. One 30-frame signature entrance per form on the full clip
# square, held beat, inside her own clip (v2, below). They replace the art3 flourishes.
# Wiring is by slot name, so the spec decides the carrier: an effect whose appearAnimation is "moe_entrance" gets her
# form's entrance (and a staticAnimation "moe_aura" her approved art3 aura). Today no boss jutsu carries "moe_entrance" (the art3 flourishes and auras were created
# and unhidden by push/489 and 496 but never wired): the carrier is the sim's once-per-act buff (ENTRANCE_NOTE).
FX4_META = "art/mother_of_echoes_fx/exports/moe_fx_final.json"  # every asset the final tuning job creates
FORMS = (("sayo1", "Sayo"), ("silence", "The Silence"), ("sayo2", "The Glasswright"), ("saint", "The Saint"))
# v2 (director 2026-11-05: the first entrances were "far too large and gaudy ... they clip"): small, inside her clip, the
# bible's held beat, no ground ring. The v1 strips (_a4) and their rings were retired before upload.
FX4 = {f"entrance_{k}": (f"anim_moe_entrance_{k}_a5.webp", f"Mother of Echoes FX - {n} enters") for k, n in FORMS}
# The final tuning job's art (director 2026-11-05: the Refraction line is the bar; omens / payoffs / lingering ground;
# no sickly green, colours per enemy; the floor as a stage; MOTHER_OF_ECHOES_ART.md "Art direction"):
FX4.update({f"rbreak_{s_}{c}": (f"anim_moe_rbreak_{s_}{c}_a6.webp", f"Mother of Echoes FX - Refraction breaks, {s_.upper()} {c}")
            for s_, cols in (("l", range(0, 9)), ("r", range(3, 12))) for c in cols})
FX4.update({f"rmark_{s_}{c}": (f"anim_moe_rmark_{s_}{c}_a6.webp", f"Mother of Echoes FX - Refraction runs in, {s_.upper()} {c}")
            for s_, cols in (("l", range(0, 9)), ("r", range(3, 12))) for c in cols})
FX4.update({
    "lancet6": ("anim_moe_lancet_a6.webp", "Mother of Echoes FX - Glass Lancet (held star)"),
    "sweep6": ("anim_moe_doorward_sweep_a6.webp", "Mother of Echoes FX - Doorward Sweep"),
    "quiet6": ("anim_moe_quiet_a6.webp", "Mother of Echoes FX - The Quiet (ink lids)"),
    "floor_i": ("tile_moe_floor_i_a8.webp", "Mother of Echoes floor - crazed Heartglass"),
    "floor_ii": ("tile_moe_recast_floor_a8.webp", "Mother of Echoes floor - shattered etch"),
    "floor_iii": ("tile_moe_floor_iii_a8.webp", "Mother of Echoes floor - blackened obsidian"),
    "floor_silence": ("tile_moe_floor_silence_a8.webp", "Mother of Echoes floor - ink and frost"),
    "floor_mended": ("tile_moe_mended_floor_a8.webp", "Mother of Echoes floor - nothing is mended"),
    "absence_rise": ("anim_moe_absence_rise_a7.webp", "Mother of Echoes FX - An Absence arrives"),
    "absence_idle": ("anim_moe_absence_idle_a7.webp", "Mother of Echoes FX - An Absence waits"),
    "absence_burst": ("anim_moe_absence_burst_a9.webp", "Mother of Echoes FX - An Absence erupts"),
    "absence_splat": ("anim_moe_absence_splat_a9.webp", "Mother of Echoes FX - An Absence splatters"),
})
# Lingering ground by owner (no bile anywhere): the payoff's settle carries the arrival, so the floor has no appear and
# no loop (stacking rules 1-2). The Hush family is the Silence's whatever boss casts it.
FLOOR_BY_ACT = {"i": "floor_i", "ii": "floor_ii", "iii": "floor_iii"}
FLOOR_BY_NAME = (("No One Is Mended", "floor_mended"), ("The Hush", "floor_silence"), ("Hush ", "floor_silence"),
                 ("An Absence", "floor_silence"), ("Recast:", "floor_ii"))
# Refraction lines (fixed rows: L = columns 0-8 from the left wall, R = 3-11 from the right): the mark's arrival and the
# break as the sliced Refraction line, one visual tag per (side, column).
REFRACTION_SLICES = {"Refraction": "rmark", "Far Refraction": "rmark", "Facet": "rmark",
                     "Refraction Breaks": "rbreak", "Far Refraction Breaks": "rbreak", "Facet Breaks": "rbreak",
                     "Lucid Refraction": "rbreak"}
FORM = {"Sayo, Mother of Echoes": "sayo1", "The Silence": "silence", "Sayo, Glasswright of the Stilling": "sayo2",
        "Sayo, Saint of Stillness": "saint"}
ENTRANCE_NOTE = ("the entrance plays when its carrier is cast, every time: it needs a once-per-act cast (a first rule "
                 "gated on the buff's own absence), which is the sim's act buff (director 2026-11-05)")
# Dialog portraits (director 2026-11-05): SCENE_CHARACTER 2:3 crops of the approved avatars, Sayo only. Act I Sayo in
# the three opening scenes (not the Silence), her act forms for the interludes. key -> (file, name, dialog nodes).
SCENE_CHARS = {
    "sc_sayo": ("scene_moe_sayo_a3.webp", "Mother of Echoes Scene Character - Sayo",
                ("d_intro1", "d_intro2", "d_open")),
    "sc_stilling": ("scene_moe_sayo_stilling_a3.webp", "Mother of Echoes Scene Character - Sayo, Glasswright",
                    ("d_act2",)),
    "sc_saint": ("scene_moe_saint_a3.webp", "Mother of Echoes Scene Character - Sayo, Saint of Stillness",
                 ("d_act3",)),
}
# Which act's material a boss (or its summon) fights in. The Silence is the Remainder's own material.
BOSS_ACT = {"Sayo, Mother of Echoes": "i", "Your Likeness": "i", "Sayo, Glasswright of the Stilling": "ii",
            "The Gate Porter (Worn)": "ii", "Sister Hana (Worn)": "ii", "Cadet Tomo (Worn)": "ii",
            "The Silence": "iii", "A Feeler of the Deep": "iii", "Sayo, Saint of Stillness": "iii"}
TG3 = {  # telegraph name -> per-field key (FX2 or FX3) by act. No disappearAnimation on any ground mark: a ground tag's
    # disappear clip is re-spawned on whoever stands on it at every effect pass (process.ts:1667-1684,
    # docs/design/COMBAT_ANIMATION_ENGINE.md section 5.3), so a vanish would pop repeatedly on a player in a mark or on
    # the safe hex. The mark simply goes when it expires.
    "tg_heavy": lambda act: {"staticAssetPath": f"heavy_tile_{act}", "staticAnimation": f"heavy_glint_{act}",
                             "appearAnimation": f"heavy_appear_{act}", "disappearAnimation": None},
    "tg_control": lambda act: {"staticAssetPath": "control_dark", "staticAnimation": "control_glint",
                               "appearAnimation": "control_appear", "disappearAnimation": None},
    "tg_safe": lambda act: {"staticAssetPath": "safe_tile", "staticAnimation": "safe_glint",
                            "appearAnimation": "safe_appear", "disappearAnimation": None},
    "tg_linger": lambda act: {"staticAssetPath": "linger_dark" if act == "iii" else "linger_tile",
                              "staticAnimation": "linger_glint", "appearAnimation": "linger_appear",
                              "disappearAnimation": None},
}
SLOT3 = {"moe_refraction": "refraction", "moe_recast": "recast", "moe_feeler": "rise_feeler",
         "moe_likeness": "rise_likeness", "moe_worn": "rise_worn"}
# Mosaics (director 2026-11-05, approved): the signature payoffs play as a wave. The hit's own appear is blanked and one
# zero-impact visual tag per band (target COORDINATES, the cast's own origin, a subset of its tiles) carries a strip
# whose frames are led by band * WAVE_LEAD blank frames. A visual tag is stamped only on its own tiles
# (actions.ts:1063-1071, util.ts getActionAffectedTiles), has no server duplicate (process.ts:432), no occupant copy
# (process.ts:399), no gameplay handler, and power 2 is never hidden (combatEffects.ts:183-187).
MOSAIC = {  # art slot -> (FX3 key prefix, band count, band(longitude, latitude))
    "moe_enrage": ("enrage_w", 4, lambda lon, lat: lon // 3),  # 12 columns, swept in 4 bands
    "moe_flood": ("flood_w", 4, lambda lon, lat: min(3, int(4 * max(abs(lon - 5.5) / 6, abs(lat - 4.5) / 5)))),
    "moe_shatterfall": ("shatterfall_w", 5, lambda lon, lat: abs(lon) - 1),  # CASTER cone, near rank first
    "moe_glassfall": ("glassfall_w", 3, lambda lon, lat: lon // 4),
}
# Recasts are not mosaicked: they are CHARACTER casts (a hit lands only on an occupied etched hex), so a band of visual
# tags over the etching would draw a payoff where no one is hit and change a no-target cast into a landed one.
# Sound (director 2026-11-05): existing in-game SFX only, one per cast. The client plays appearSfx once per NEW effect
# record (combatEffects.ts:35-41, :106), so a sound on a 100-tile tag plays 100 times. Single-target and CHARACTER casts
# carry it on their art-bearing hit (one record per target); ground casts on a one-tile visual at the caster.
SFX = {"lightning": "eJCEtS5_P_pW_VPc6ttRh", "sword_clash": "PFY2oXpwIpNwUOx327WCm", "earth": "XBlRonNjvwAZx1_HFpHdM",
       "sword": "muq1tu3xvolOsUHm-NqBr", "wind": "oDdj-mBmiWTswFi_NkOqc", "smoke": "16vlpusdcPY8Ki3zE4qOs",
       "punch": "874ccOJkc8HPAzQgmzgQ8", "heal": "4iG_WpgEmPGUzHn8z129r"}
SFX_BY_NAME = [  # (name or prefix, sound): first match wins
    ("Refraction Breaks", "lightning"), ("Far Refraction Breaks", "lightning"), ("Facet Breaks", "lightning"),
    ("Lucid Refraction", "lightning"), ("Lucid", "lightning"), ("Recast:", "sword_clash"),
    ("Glassfall:", "earth"), ("Shatterfall Gives Way", "earth"), ("The Glass Remembers", "earth"),
    ("The Names Flood In", "earth"), ("Glass Lancet", "sword"), ("Breathless Pull", "wind"),
    ("Refraction", "wind"), ("Far Refraction", "wind"), ("Facet", "wind"), ("Etching:", "wind"),
    ("Shatterfall", "wind"), ("Every Name in the Glass", "wind"), ("The Held Breath", "wind"), ("Stillness", "wind"),
    ("The Long Hush", "wind"), ("The Silence Turns", "wind"), ("The Glass Turns", "wind"),
    ("The Hush", "smoke"), ("Hush Where They Refused", "smoke"), ("No One Is Mended", "smoke"),
    ("Nothing Moves", "smoke"), ("The Quiet", "smoke"), ("The Glass Falls Quiet", "smoke"), ("Cradle", "smoke"),
    ("The Listening", "smoke"), ("Your Likeness", "smoke"), ("Raise ", "smoke"),
    ("Grasp", "punch"), ("Doorward Sweep", "punch"), ("Cadet's Tether", "punch"), ("Your Own Strike", "punch"),
    ("Worn Mending", "heal"),
]
VISUAL = {"staticAssetPath": "", "staticAnimation": "", "appearAnimation": "", "disappearAnimation": "",
          "appearSfx": "", "disappearSfx": "", "rounds": 1, "power": 2, "powerPerLevel": 0, "direction": "offence",
          "target": "COORDINATES", "calculation": "static", "type": "visual"}
# Library strips the spec names by literal id -> FX2 key, by (id, effect type, detail).
LIB2 = {("dBatQkc1Ts2ask5ZN-A3p", "pierce"): lambda name, e: "grasp" if name == "Grasp" else "echo_strike",
        ("FZNt0vFGXlOZeagmPneqc", "redirection"): lambda name, e: "shove" if e.get("direction") == "push" else "pull",
        ("I9aYhT5wMB", "heal"): lambda name, e: "mend",
        ("bJy2IjRKmAVYEoXUYmXv5", "visual"): lambda name, e: "control_appear",
        ("k8J4ic-KEz9ewEq1gAszr", "visual"): lambda name, e: None}  # a visual never plays its disappear (dead wiring)

# Art slot -> asset key (466) or live id. tg_etch and moe_hush_floor fill all four fields; moe_lull moves (below).
SLOT_FX = {"moe_recast": "recast", "moe_guard_open": "guard_open", "moe_quiet": "quiet", "moe_lancet": "lancet",
           "moe_feeler": "feeler", "moe_stillness": "still", "moe_breathless": "breath", "moe_lucid": "lucid",
           "moe_likeness": "likeness", "moe_worn": "worn", "moe_cradle": "cradle",
           "moe_flood": "flood"}
SLOT_LIVE = {"moe_refraction": ERUPTION, "moe_enrage": ERUPTION,
             "moe_shatterfall": CRYSTAL_SHARD, "moe_glassfall": CRYSTAL_SHARD}
SLOT_PENDING = {}  # every slot is drawn. moe_flood: the director's glass-mask keyframes (ME28b, drawn for the 50 px
# CDN rendition) replace the ME28 faces, which failed the art QA (2026-11-04) and are not shipped.
# The lull rides the jutsu's fleeprevent (SELF, 2 rounds) as its staticAnimation, not the visual (the server drops
# visual ground effects at the next action, RUL-2026-11-02-101). The visual keeps its live appear/vanish.
LULL_MOVE = ("visual", "fleeprevent")
FAMILY_FILES = {f: f"{ART}icon-jutsu-moe-{f}.webp" for f in
                ("lancet", "refraction", "etching", "glassfall", "hush", "echoes")}
FAMILY = {  # the art list's family table (ME21-ME26), by jutsu name
    "lancet": ["Glass Lancet", "The Glass Remembers", "Lucid"],
    "refraction": ["Refraction", "Far Refraction", "Facet", "Refraction Breaks", "Far Refraction Breaks",
                   "Facet Breaks", "Lucid Refraction", "Every Name in the Glass", "The Names Flood In"],
    "etching": ["Etching: Rime", "Etching: Ember", "Etching: Seam", "Etching: Heart", "Etching: Hail",
                "Recast: Rime", "Recast: Ember", "Recast: Seam", "Recast: Heart", "Recast: Hail",
                "The Glass Turns"],  # pass 6 follow-the-player mark (Act II Sayo's etching family)
    "glassfall": ["Shatterfall", "Shatterfall Gives Way", "Glassfall: First Pane", "Glassfall: Second Pane",
                  "Glassfall: Last Pane", "Glassfall: Opening Pane", "Glassfall: Heart Recast"],
    "hush": ["The Hush", "The Hush, Unbridled", "The Hush Rises", "Hush Where They Refused", "No One Is Mended",
             "The Quiet", "The Long Hush", "The Glass Falls Quiet", "Stillness", "Nothing Moves", "The Held Breath",
             "Breathless Pull", "The Listening", "The Listening, Unbridled", "Cradle", "Grasp",
             "The Silence Turns"],  # pass 6 follow-the-player mark (the Silence's hush family)
    "echoes": ["Your Likeness", "Your Own Strike", "Raise the Gate Porter", "Raise Sister Hana", "Raise Cadet Tomo",
               "Doorward Sweep", "Worn Mending", "Cadet's Tether"],
}
# The Silence rim-lit proposal (art QA 2026-11-04; art/mother_of_echoes/rim_silence.py). Set True once the director
# approves it; the original stays wired until then.
SILENCE_RIM = False
AVATARS = {  # harness AI id -> export (RUL-2026-11-03-111; Act I is the approved v2)
    "moe-ai-sayo": "avatar_moe_sayo_v2.webp",
    "moe-ai-silence": "avatar_moe_silence_rim.webp" if SILENCE_RIM else "avatar_moe_silence.webp",
    "moe-ai-sayo-stilling": "avatar_moe_sayo_stilling.webp", "moe-ai-saint": "avatar_moe_saint.webp",
    "moe-ai-feeler": "avatar_moe_feeler.webp", "moe-ai-likeness": "avatar_moe_likeness.webp",
    "moe-ai-worn-porter": "avatar_moe_worn_porter.webp", "moe-ai-worn-hana": "avatar_moe_worn_hana.webp",
    "moe-ai-worn-tomo": "avatar_moe_worn_tomo.webp",
}
AVATARS_OPTIONAL = {"moe-ai-absence": "avatar_moe_absence_a7.webp"}  # An Absence (the sim's anti-camping summon, 2026-11-05)
QUEST_ICON = ART + "icon-quest-mother-of-echoes.webp"
SHARD_ICONS = {k: f"{ART}icon-shard-{k}.webp" for k in ("keel", "crown", "tide", "ledger")}
TOKEN_ICONS = {"heartglass": ART + "icon-variant-token-heartglass.webp",
               "remainder": ART + "icon-variant-token-remainder.webp"}
VARIANT_ICONS = {  # NOT icon-variant-heartglass-v2 (not the approved image) nor the 417 original
    "heartglass": "art/skyglass_variant_skins/exports/icon-variant-heartglass-approved.webp",
    "remainder": "art/skyglass_variant_skins/exports/icon-variant-the-remainder.webp",
}
PASS6_NEW = ("The Silence Turns", "The Glass Turns")  # jutsu pass 6 adds (no live record before push/476)
ART_FIELDS = ("staticAssetPath", "staticAnimation", "appearAnimation", "disappearAnimation")
LIVE_ID = re.compile(r"^[A-Za-z0-9_-]{10,21}$")
DROP_KEYS = {"id", "createdAt", "updatedAt"}


# Rewards (RUL-2026-11-01-095 item 2 as amended by RUL-2026-11-02-100, -104 (no Salvage) and -105 (no first-clear
# mechanics, no title; every clear rolls both tradeable tokens)): pick ids by name from verified bundles.
CROWNS_HOARD = "WrnHlt3h6ZDjFaJk3i41O"   # harvests/inbox/tnr_results_1793491854510.json (unhide, verified)
SKYGLASS_COFFER = "THo7rfzP-S82_43aN8fs3"  # harvests/inbox/tnr_results_1793491854510.json
SKYGLASS_TOKEN = "nzCW7A-_AuYMzBs2wClnM"   # harvests/inbox/tnr_results_1793424666625.json
PICK = [(CROWNS_HOARD, 1), (SKYGLASS_COFFER, 5), (SKYGLASS_TOKEN, 3)]  # RUL-2026-11-04-114
TOKEN_PCT = {"heartglass": 25, "remainder": 25}  # approved RUL-2026-11-03-110
REWARD_EXP = 1000      # RUL-2026-11-03-110
REWARD_MONEY = 50000   # RUL-2026-11-03-110

Q_NAME = "The Mother of Echoes"


def die(msg):
    sys.exit(f"mother_of_echoes.gen.py: {msg}")


# ---------------------------------------------------------------------------------------------------------------
# Spec
# ---------------------------------------------------------------------------------------------------------------
# Dev-only dry run (never for a committed manifest): MOE_SPEC_FILE=<spec.json> MOE_OUT_DIR=<dir outside push/> builds
# from an unpinned spec file into a scratch directory, to prove a step against a spec before its SHA is pinned.
DRY_SPEC = os.environ.get("MOE_SPEC_FILE")
DRY_OUT = os.environ.get("MOE_OUT_DIR")


# The director-approved jutsu text pass (2026-11-05; docs/design/MOTHER_OF_ECHOES_JUTSU_TEXT.md): description, and
# battleDescription where rewritten, by jutsu name. Applied over the spec's text in every jutsu record built here.
JUTSU_TEXT = json.load(open(os.path.join(ROOT, "push", "mother_of_echoes_text.json")))["jutsu"]


def load_spec():
    if DRY_SPEC:
        if not DRY_OUT or os.path.abspath(DRY_OUT).startswith(os.path.join(ROOT, "push")):
            die("MOE_SPEC_FILE needs MOE_OUT_DIR outside push/ (dry runs never write a committed manifest)")
        spec = json.load(open(DRY_SPEC))
        if not str(spec.get("validation", "")).startswith("valid"):
            die(f"{DRY_SPEC} does not validate: {spec.get('validation')}")
        return spec
    if not re.fullmatch(r"[0-9a-f]{40}", SPEC_REF):
        die("SPEC_REF is not pinned to a fable/mother-of-echoes-sim commit")
    try:
        raw = subprocess.check_output(["git", "-C", ROOT, "show", f"{SPEC_REF}:{SPEC_PATH}"], stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        die(f"cannot read {SPEC_PATH} at {SPEC_REF}; run: git fetch origin fable/mother-of-echoes-sim")
    spec = json.loads(raw)
    if not str(spec.get("validation", "")).startswith("valid"):
        die(f"the spec at {SPEC_REF} does not validate: {spec.get('validation')}")
    return spec


def sid(hid):
    """Harness id -> srcId (moe-glass-lancet -> sg440_glass_lancet; moe-ai-sayo -> sg440_ai_sayo)."""
    if not hid.startswith("moe-"):
        die(f"not a harness id: {hid}")
    return PFX + hid[4:].replace("-", "_")


def unique_names(rows, key):
    """The game keeps jutsu names and AI usernames unique (theninjarpg@3314d122 drizzle/schema.ts Jutsu_name_key,
    UserData_username_key). Names come from the spec only (RUL-2026-11-02-105: proper names, no numbered
    placeholders), so a repeated name refuses the build instead of being suffixed."""
    out, seen = {}, {}
    for r in rows:
        name = key(r)
        if name in seen:
            die(f"name {name!r} is used by both {seen[name]} and {r['id']}; name them in the spec (FINAL_TEXT)")
        seen[name] = r["id"]
        out[r["id"]] = name
    return out


# Stacking pass (docs/design/MOTHER_OF_ECHOES_ART.md "Stacking pass", 2026-11-05): visual-only budget rules, opt-in per
# build (Build(stack=True)) so the jobs that already ran regenerate unchanged. Static loops draw OVER every fighter
# (COMBAT_ANIMATION_ENGINE.md 3.2) and never stop for the effect's life; the tile under the fighters carries the
# telegraph. A pool or a mark field bigger than its cap keeps its tile and its arrival, and loses its loop.
STACK_RULES = {"pool_loop_max": 10, "mark_loop_max": 30}
LIB_BUFF_PLACEHOLDERS = {"FZNt0vFGXlOZeagmPneqc", "VMft99LeB_qQggEw_GrKi"}  # library shove / shield strips on the boss buffs
BUFF_TYPES = ("absorb", "shield", "reflect", "lifesteal")


class Build:
    def __init__(self, spec, fx=None, art=False, fx2=None, stack=False, final=False):
        self.spec = spec
        self.fx = fx      # 466 asset ids by FX key (jutsu_art step only)
        self.fx2 = fx2    # push/478 custom set: FX2 key -> asset ref (None: the live borrowed strips)
        self.final_art = art  # art pass: real images instead of the engine default
        self.final = final    # the final tuning job's art (FX4 set, floors by owner, slices); implies the stacking rules
        self.stack = stack or final
        self.jutsu = {j["id"]: j for j in spec["jutsu"]}
        self.ais = {a["id"]: a for a in spec["ais"]}
        self.jname = unique_names(spec["jutsu"], lambda j: j["record"]["name"])
        self.aname = unique_names(spec["ais"], lambda a: a["username"])
        self.notes = []
        summon = {jid for jid, j in self.jutsu.items() if any(e.get("aiId") for e in j["record"]["effects"])}
        self.summon_jutsu = [jid for jid in self.jutsu if jid in summon]
        self.plain_jutsu = [jid for jid in self.jutsu if jid not in summon]
        self.templates = [a["id"] for a in spec["ais"] if a["summonTemplate"]]
        self.family = {n: f for f, names in FAMILY.items() for n in names}
        if art:
            names = set(self.jname.values())
            optional = set(PASS6_NEW)  # absent from pre-pass-6 specs
            if names != set(self.family) - (optional - names):
                die(f"family table vs spec jutsu: missing {sorted(names - set(self.family))}, "
                    f"stale {sorted(set(self.family) - names)}")
            AVATARS.update({k: v for k, v in AVATARS_OPTIONAL.items() if k in self.ais})
            if set(AVATARS) != set(self.ais):
                die(f"avatar table vs spec AIs: {sorted(set(AVATARS) ^ set(self.ais))}")
        self.bosses = [a["id"] for a in spec["ais"] if not a["summonTemplate"]]
        self.holders = {}  # jutsu name -> the AI usernames holding it
        for a in spec["ais"]:
            for j in a["create"]["jutsus"]:
                if j in self.jname:
                    self.holders.setdefault(self.jname[j], set()).add(a["username"])

    # ---- jutsu -----------------------------------------------------------------------------------------------
    def art(self, label, eff):
        if self.fx is not None:
            return self.art_final(label, eff)
        e = dict(eff)
        for f in ART_FIELDS:
            v = e.get(f) or ""
            if v in TG_STANDIN:
                e[f] = TG[TG_STANDIN[v]][f]
                self.notes.append(f"{label}: effects[{e['type']}] art {v} (no live art yet; the {TG_STANDIN[v]} tile stands in)")
            elif v in TG:
                e[f] = TG[v][f]
            elif v.startswith("moe_"):
                e[f] = ""
                self.notes.append(f"{label}: effects[{e['type']}] art {v} (art pending; left empty)")
            elif v and not LIVE_ID.match(v):
                die(f"{label}: unknown art name {v!r} in {f}")
        return e

    def art_final(self, label, eff):
        """Art pass: every slot name resolves to a 466 asset, a live id, or (P2 not drawn) empty."""
        if self.fx2 is not None:
            return self.art_custom(label, eff)
        e = dict(eff)
        etch = {"staticAssetPath": self.fx["etch_tile"], "staticAnimation": self.fx["etch_glint"],
                "appearAnimation": APPEAR, "disappearAnimation": VANISH}
        for f in ART_FIELDS:
            v = e.get(f) or ""
            if v == "tg_etch":
                e[f] = etch[f]
            elif v in TG:
                e[f] = TG[v][f]
            elif v == "moe_hush_floor":
                e[f] = TG["tg_linger"][f]
            elif v in SLOT_FX:
                e[f] = self.fx[SLOT_FX[v]]
            elif v in SLOT_LIVE:
                e[f] = SLOT_LIVE[v]
            elif v in SLOT_PENDING:
                e[f] = ""
                self.notes.append(f"{label}: effects[{e['type']}].{f} {v}: {SLOT_PENDING[v]}")
            elif v == "moe_lull":
                e[f] = ""  # moved to the fleeprevent effect (jutsu_data)
            elif v.startswith(("moe_", "tg_")) or (v and not LIVE_ID.match(v)):
                die(f"{label}: art name {v!r} in {f} has no mapping in the art pass")
        return e

    def form_of(self, label):
        forms = {FORM.get(u, "?") for u in self.holders.get(label, ())}
        if len(forms) != 1 or "?" in forms:
            die(f"{label}: held by {sorted(self.holders.get(label, ()))}; an entrance needs one boss form (FORM)")
        return forms.pop()

    def floor_of(self, label):
        for prefix, key in FLOOR_BY_NAME:
            if label == prefix or label.startswith(prefix):
                return key
        return FLOOR_BY_ACT[self.act_of(label)]

    def refraction_slices(self, label, rec, d):
        """The sliced Refraction line: blank the per-hex arrival / payoff and add one visual tag per (row side, column)."""
        kind = REFRACTION_SLICES[label]
        slot = "tg_heavy" if kind == "rmark" else "moe_refraction"
        for src, e in zip(rec["effects"], d["effects"]):
            if src.get("appearAnimation") == slot and src.get("target") != "COORDINATES":
                e["appearAnimation"] = ""
        rows = {}
        for c in rec["coordinateTargeting"]["coordinates"]:
            rows.setdefault(c["latitude"], []).append(c["longitude"])
        tags = {}
        for lat, cols in rows.items():
            side = "l" if sorted(cols) == list(range(0, 9)) else "r" if sorted(cols) == list(range(3, 12)) else None
            if side is None:
                die(f"{label}: row {lat} is not a 9-hex wall line ({sorted(cols)}); the Refraction slices need one")
            for c in cols:
                tags.setdefault((side, c), []).append({"longitude": c, "latitude": lat})
        return [{**VISUAL, "appearAnimation": self.fx2[f"{kind}_{side}{c}"],
                 "coordinateTargeting": {"origin": "BATTLEFIELD", "selection": "ALL", "coordinates": coords},
                 "description": f"{label}: the line, {side.upper()} column {c} (art only)"}
                for (side, c), coords in sorted(tags.items())]

    def act_of(self, label):
        """The act material a jutsu fights in: every AI holding it must share one act (BOSS_ACT)."""
        acts = {BOSS_ACT.get(u, "?") for u in self.holders.get(label, ())}
        if len(acts) != 1 or "?" in acts:
            die(f"{label}: held by {sorted(self.holders.get(label, ()))}; no single act material (BOSS_ACT)")
        return acts.pop()

    def art_custom(self, label, eff):
        """push/478: as art_final, but every borrowed live strip resolves to the custom set (FX2, FX3 by act). A
        MOSAIC slot is blanked here; jutsu_data adds its band visuals."""
        e = dict(eff)
        etch = {"staticAssetPath": self.fx["etch_tile"], "staticAnimation": self.fx["etch_glint"],
                "appearAnimation": self.fx2["etch_appear"], "disappearAnimation": ""}
        for f in ART_FIELDS:
            v = e.get(f) or ""
            tg = "tg_linger" if v == "moe_hush_floor" else v
            if v == "tg_etch":
                e[f] = etch[f]
            elif self.final and tg == "tg_linger":
                e[f] = self.fx2[self.floor_of(label)] if f == "staticAssetPath" else ""
            elif self.final and v == "moe_lancet":
                e[f] = self.fx2["lancet6"]
            elif self.final and v == "moe_quiet":
                e[f] = self.fx2["quiet6"]
            elif self.final and label == "Doorward Sweep" and e["type"] == "pierce" and v:
                e[f] = self.fx2["sweep6"]
            elif self.final and v in ("moe_absence_rise", "moe_absence_idle"):
                e[f] = self.fx2[v[4:]]
            elif self.final and v == "moe_absence_burst":
                e[f] = ""   # the burst rides one centre visual (jutsu_data), not every hex of the cast
            elif self.final and v == "tg_absence":
                e[f] = {"staticAssetPath": self.fx2["floor_silence"], "appearAnimation": self.fx2["absence_splat"]}.get(f, "")
            elif tg in TG3:
                k = TG3[tg](self.act_of(label))[f]
                e[f] = self.fx2[k] if k else ""
            elif v in MOSAIC:
                e[f] = ""
            elif v == "moe_entrance":
                e[f] = self.fx2[f"entrance_{self.form_of(label)}"]
            elif v == "moe_aura":
                e[f] = self.fx2[f"aura_{self.form_of(label)}"]
            elif v in SLOT3:
                e[f] = self.fx2[SLOT3[v]]
            elif v in SLOT_FX:
                e[f] = self.fx[SLOT_FX[v]]
            elif self.stack and v in LIB_BUFF_PLACEHOLDERS and e["type"] in BUFF_TYPES:
                e[f] = ""  # another event's strip restacking on the boss every cast: blanked (stacking pass rule 5)
            elif (v, e["type"]) in LIB2:
                k = LIB2[(v, e["type"])](label, e)
                e[f] = self.fx2[k] if k else ""
            elif v == "moe_lull":
                e[f] = ""  # moved to the fleeprevent effect (jutsu_data)
            elif v in SLOT_PENDING:
                e[f] = ""
            elif v.startswith(("moe_", "tg_")):
                die(f"{label}: art name {v!r} in {f} has no mapping in the custom set")
            elif v and LIVE_ID.match(v):
                die(f"{label}: effects[{e['type']}].{f} still borrows live strip {v} (no custom mapping)")
            elif v:
                die(f"{label}: unknown art {v!r} in {f}")
        return e

    def hexes(self, rec, e):
        """How many hexes an effect's art lands on (the cast's own pattern, a RANDOM pick, or its own COORDINATES)."""
        if e.get("target") == "SELF":
            return 1
        ct = e.get("coordinateTargeting") if e.get("target") == "COORDINATES" else rec.get("coordinateTargeting")
        if ct:
            return ct.get("randomCount", len(ct["coordinates"])) if ct.get("selection") == "RANDOM" else len(ct["coordinates"])
        return {"AOE_CIRCLE_SPAWN": 7, "AOE_SPIRAL_SHOOT": 36}.get(rec.get("method"), 1)

    def stack_rules(self, label, rec, d):
        pools = {self.fx2.get(k) for k in ("linger_tile", "linger_dark")}
        marks = {self.fx2.get(k) for k in self.fx2 if k.startswith(("heavy_tile", "control_"))} | {self.fx.get("etch_tile")}
        for src, e in zip(rec["effects"], d["effects"]):
            n = self.hexes(rec, src)
            if e.get("staticAssetPath") in pools and n > STACK_RULES["pool_loop_max"] and e.get("staticAnimation"):
                e["staticAnimation"] = ""
                self.notes.append(f"{label}: pool on {n} hexes keeps its tile, loses its loop (stacking rule 1)")
            elif e.get("staticAssetPath") in marks and n > STACK_RULES["mark_loop_max"] and e.get("staticAnimation"):
                e["staticAnimation"] = ""
                self.notes.append(f"{label}: mark field of {n} hexes keeps its tile, loses its loop (stacking rule 2)")

    def mosaic(self, label, rec):
        """The band visuals for a MOSAIC slot: one visual tag per band, the cast's own origin, its tiles split by band."""
        slots = [e.get("appearAnimation") for e in rec["effects"] if e.get("appearAnimation") in MOSAIC]
        if not slots:
            return []
        if len(slots) != 1 or rec.get("method") != "COORDINATES" or rec.get("target") != "GROUND":
            die(f"{label}: a mosaic needs one {sorted(MOSAIC)} slot on a GROUND COORDINATES cast")
        prefix, n, band = MOSAIC[slots[0]]
        ct = rec["coordinateTargeting"]
        if ct["selection"] != "ALL":
            die(f"{label}: a mosaic splits an ALL pattern, got {ct['selection']}")
        bands = [[] for _ in range(n)]
        for c in ct["coordinates"]:
            k = band(c["longitude"], c["latitude"])
            if not 0 <= k < n:
                die(f"{label}: tile {c} falls outside the {n} bands")
            bands[k].append({"longitude": c["longitude"], "latitude": c["latitude"]})
        out = []
        for k, coords in enumerate(bands):
            if not coords:
                continue
            out.append({**VISUAL, "appearAnimation": self.fx2[f"{prefix}{k}"],
                        "coordinateTargeting": {"origin": ct["origin"], "selection": "ALL", "coordinates": coords},
                        "description": f"{label}: wave {k + 1} of {n} (art only)"})
        return out

    def jutsu_data(self, jid, ids=None):
        rec = self.jutsu[jid]["record"]
        name = self.jname[jid]
        d = {k: v for k, v in rec.items() if k not in DROP_KEYS and v is not None}
        d["name"] = name
        d["hidden"] = True
        d.update(JUTSU_TEXT.get(name, {}))  # approved text pass (push/mother_of_echoes_text.json)
        if self.final_art:
            d["image"] = "@img:" + os.path.basename(FAMILY_FILES[self.family[name]])
        else:
            d["image"] = PLACEHOLDER
            self.notes.append(f"jutsu {sid(jid)}: {name} (engine default image)")
        d["effects"] = [self.art(name, e) for e in rec["effects"]]
        if self.fx2 is not None and self.stack:
            self.stack_rules(name, rec, d)
        if self.fx2 is not None:
            d["effects"] += self.mosaic(name, rec)
        if self.final and name in REFRACTION_SLICES:
            d["effects"] += self.refraction_slices(name, rec, d)
        if self.final and any(e.get("appearAnimation") == "moe_absence_burst" for e in rec["effects"]):
            d["effects"].append({**VISUAL, "appearAnimation": self.fx2["absence_burst"],
                                 "coordinateTargeting": {"origin": "CASTER", "selection": "ALL",
                                                         "coordinates": [{"longitude": 0, "latitude": 0}]},
                                 "description": f"{name}: the burst (art only)"})
        if self.fx is not None and any(e.get("staticAnimation") == "moe_lull" for e in rec["effects"]):
            src = [e["type"] for e in rec["effects"] if e.get("staticAnimation") == "moe_lull"]
            dst = [i for i, e in enumerate(d["effects"]) if e["type"] == LULL_MOVE[1]]
            if src != [LULL_MOVE[0]] or len(dst) != 1:
                die(f"{name}: moe_lull expects one {LULL_MOVE[0]} and one {LULL_MOVE[1]} effect, got {src} / {dst}")
            d["effects"][dst[0]]["staticAnimation"] = self.fx["lull"]
        for e in d["effects"]:
            if e.get("aiId"):
                if ids is None:
                    die(f"{jid} names an AI; it is built by --step summons")
                e["aiId"] = ids[sid(e["aiId"])]
        return d

    def jutsu_entry(self, jid, ids=None):
        return {"entity": "jutsu", "slot": "create", "srcId": sid(jid), "phase": 1, "name": self.jname[jid],
                "data": self.jutsu_data(jid, ids)}

    # ---- AI --------------------------------------------------------------------------------------------------
    def lit(self, hid, ids):
        if hid == STOLEN_FORM or hid in ENGINE_ACTIONS:
            return hid
        k = sid(hid)
        if k not in ids:
            die(f"no created id for {hid} ({k}) in the bundles given")
        return ids[k]

    def ai_entry(self, aid, ids):
        a = self.ais[aid]
        d = json.loads(json.dumps(a["create"]))
        d["username"] = self.aname[aid]
        d["avatar"] = "@img:" + AVATARS[aid] if self.final_art else PLACEHOLDER
        d["inArena"] = False
        d["hidden"] = True
        d["jutsus"] = [self.lit(j, ids) for j in d["jutsus"]]
        for r in d["rules"]:
            act = r["action"]
            if act.get("jutsuId"):
                act["jutsuId"] = self.lit(act["jutsuId"], ids)
            if act.get("comboIds"):
                act["comboIds"] = [self.lit(j, ids) for j in act["comboIds"]]
        left = sorted(set(re.findall(r'"(moe-[a-z0-9-]+)"', json.dumps(d))))
        if left:
            die(f"{aid}: unresolved harness ids {left}")
        for it in d["items"]:
            if it["ids"] != [HEAVY_ARMOR]:
                die(f"{aid}: unexpected item {it}")
        if not self.final_art:
            self.notes.append(f"ai {sid(aid)}: {d['username']} (engine default image as avatar)")
        return {"entity": "ai", "slot": "create", "srcId": sid(aid), "phase": 1, "name": d["username"], "data": d}


# ---------------------------------------------------------------------------------------------------------------
# Bundles
# ---------------------------------------------------------------------------------------------------------------
def created(paths, prefix):
    got = {}
    for p in paths or []:
        b = json.load(open(p))
        for e in b.get("entries") or []:
            s = e.get("srcId") or ""
            if e.get("slot") == "create" and e.get("state") == "ok" and e.get("id") and s.startswith(prefix):
                got[s] = e["id"]
        for k, v in (b.get("idmap") or {}).items():
            if k.startswith(prefix):
                got.setdefault(k, v)
    return got


def need(ids, keys, what):
    miss = sorted(k for k in keys if k not in ids)
    if miss:
        die(f"{what}: the bundles given lack {miss}")


# ---------------------------------------------------------------------------------------------------------------
# Quest (444) and publish (445)
# ---------------------------------------------------------------------------------------------------------------
Q_DESC = ("The four shards are her invitation. Carry one of each (Keel, Crown, Tide and Ledger) to the Mother Glass "
          "under Crownhold; all four are spent when the fight begins.\n\n"
          "Three battles, one after another. Health, chakra and stamina carry from each battle to the next, with no "
          "refills. Lose any battle and the attempt ends; the shards are not returned.\n\n"
          "Watch the floor. Every mark she draws is a warning, and every warning comes due.\n\n"
          "If you still have a reward to choose from an earlier attempt, claim it before you start.")
Q_SUCCESS = "The Mother Glass cracks from the root to the crown. Choose your reward."
LOSS = {"failDescription": "The glass goes quiet around you. The shards are spent.",
        "drawDescription": "The glass goes quiet around you. The shards are spent.",
        "fleeDescription": "You back out of the hall. The shards stay in the glass."}
F_LOST = "The glass keeps what it was given. Find four more shards and come back."


# RUL-2026-11-03-111: the Silence rides in Sayo's shadow; it stands up off the floor at the start and folds back
# into her for Act III. These override the spec's dialog text (ids: d_open = n0, d_act3 = n4); 465 carries them live.
DIALOG_OVERRIDES = {
    "d_open": ("She studies you the way she studied them. \"There is room in the glass for one more.\"<br><br>She "
               "turns to the wall, as if choosing a place for you. Her shadow does not turn with her. It stays where it "
               "was. Then it stands up off the floor."),
    "d_act3": ("Every pane in the hall turns toward you. The dark at the edge of the light folds itself small and slides "
               "back across the floor into Sayo's shadow. Her eyes close. When she speaks again, nothing moves her lips. "
               "\"Hold still. You will make for a good impression.\""),
}


# The opening build-up (director, 2026-11-05: "the opening scene is exactly 1 dialog with no exposition ... Could use a
# little build up"; Sayo's villain reveal: she stilled everyone and put them in the glass). Two scenes before d_open.
INTRO = [
    ("d_intro1", "The four shards fit together in your hands, and the seams vanish. They were never broken. They were an "
                 "invitation.<br><br>They pull you down, past where Crownhold's stair ends, into a hall of glass. Every "
                 "pane holds a face. The Deck Warden. The Captain, twice: once bareheaded, once crowned. The guards you cut down. "
                 "Their eyes are open, and "
                 "none of them blink.", "Go deeper"),
    ("d_intro2", "She hangs in the air before the Mother Glass, her fan open behind her like a halo.<br><br>\"Lovely, "
                 "aren't they? Every one of them held still for me.\" She smiles at the faces. \"The ship, the castle, "
                 "all of it. I never lost them. I kept them.\" She inclines her head, as if you had asked. \"Sayo. I grew the "
                 "glass.\"<br><br>\"And you have been cutting them out of my glass, "
                 "one by one. How interesting.\"", "You did this"),
]


def quest_data(b, ids, econ, scenes=None, chars=None):
    """scenes: SCENES key -> 466 asset id (the publish); None keeps the CORE_CHAMBER placeholder (464). chars:
    SCENE_CHARS key -> 478 asset id (the dialog portraits); None keeps every node's sceneCharacters empty."""
    q = b.spec["quest"]
    obj = {o["n"]: o for o in q["objectives"]}
    sc = {"sceneBackground": CORE_CHAMBER, "sceneCharacters": []}

    def battle(oid, n, nxt):
        o = obj[n]
        return {"id": oid, "task": "start_battle", "description": o["title"], **sc,
                "opponentAIs": [{"ids": [ids[sid(a)]], "number": 1, "quantity": 1} for a in o["opponents"]],
                "completionOutcome": "Win", "scaleGains": 1, "keepOriginalPools": False,
                "opponent_scaled_to_user": False, "nextObjectiveId": nxt, "failObjectiveId": "f_lost", **LOSS}

    def dialog(oid, n, nxt, label):
        return {"id": oid, "task": "dialog", "description": DIALOG_OVERRIDES.get(oid, obj[n]["text"]), **sc,
                "nextObjectiveId": [{"text": label, "nextObjectiveId": nxt}]}

    win = {"id": "w_clear", "task": "win_quest", "description": obj[6]["text"], **sc, "reward_exp": REWARD_EXP}
    if REWARD_MONEY:
        win["reward_money"] = REWARD_MONEY
    win["reward_items"] = [{"ids": [econ[ECON + k]], "number": pct, "quantity": 1} for k, pct in TOKEN_PCT.items()]
    intro = [{"id": oid, "task": "dialog", "description": text, **sc,
              "nextObjectiveId": [{"text": label, "nextObjectiveId": (INTRO[i + 1][0] if i + 1 < len(INTRO) else "d_open")}]}
             for i, (oid, text, label) in enumerate(INTRO)]
    objs = [*intro, dialog("d_open", 0, "b_act1", "Step into the hall"),
            battle("b_act1", 1, "d_act2"), dialog("d_act2", 2, "b_act2", "Hold your ground"),
            battle("b_act2", 3, "d_act3"), dialog("d_act3", 4, "b_act3", "Do not hold still"),
            battle("b_act3", 5, "w_clear"), win,
            {"id": "f_lost", "task": "fail_quest", "description": F_LOST, **sc}]
    entry = [{"ids": [econ[ECON + k]], "number": 1} for k in ("keel", "crown", "tide", "ledger")]
    content_bg = CORE_CHAMBER
    if scenes is not None:
        node = {n: scenes[k] for k, (_, _, nodes) in SCENES.items() for n in nodes}
        got = {o["id"] for o in objs}
        if set(node) - {"content"} != got:
            die(f"scene table vs quest nodes: {sorted((set(node) - {'content'}) ^ got)}")
        for o in objs:
            o["sceneBackground"] = node[o["id"]]
        content_bg = node["content"]
    if chars is not None:
        node = {n: chars[k] for k, (_, _, nodes) in SCENE_CHARS.items() for n in nodes}
        got = {o["id"] for o in objs if o["task"] == "dialog"}
        if set(node) - got:
            die(f"scene-character nodes not in the quest's dialogs: {sorted(set(node) - got)}")
        for o in objs:
            if o["id"] in node:
                o["sceneCharacters"] = [node[o["id"]]]
    return {"name": Q_NAME, "description": Q_DESC, "successDescription": Q_SUCCESS,
            "image": PLACEHOLDER if scenes is None else "@img:" + os.path.basename(QUEST_ICON),
            "questType": "battlepyramid", "questRank": "S", "hidden": True,
            "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "requiredLevel": 1,
            "maxLevel": 100, "maxAttempts": 100, "maxCompletes": 100,
            "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None,
            "startsAt": None, "endsAt": None,
            "content": {"objectives": objs, "sceneBackground": content_bg, "sceneCharacters": [BLANK],
                        "entryItems": entry, "isolated": True, "rewardMode": "choose", "rewardPickCount": 1,
                        "reward": {"reward_items": [{"ids": [i], "number": 100, "quantity": n} for i, n in PICK]}}}


# ---------------------------------------------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------------------------------------------
def pack(paths):
    """imagePack pinned to the newest commit touching the files; the working copy must equal that commit."""
    paths = sorted(set(paths))
    ref = subprocess.check_output(["git", "-C", ROOT, "log", "-1", "--format=%H", "HEAD", "--", *paths], text=True).strip()
    if not ref:
        die(f"not committed: {paths}")
    files = {}
    for p in paths:
        disk = open(os.path.join(ROOT, p), "rb").read()
        try:
            same = subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{p}"], stderr=subprocess.DEVNULL) == disk
        except subprocess.CalledProcessError:
            same = False
        if not same:
            die(f"{p}: working copy differs from {ref} (commit it first)")
        name = os.path.basename(p)
        if name in files:
            die(f"two files named {name}")
        files[name] = {"path": p, "sha256": hashlib.sha256(disk).hexdigest(), "bytes": len(disk)}
    return {"imgSizes": {k: v["bytes"] for k, v in files.items()}, "imagePack": {"ref": ref, "files": files}}


def img_paths(items, pool):
    """The files behind every @img ref in items, looked up by basename in pool."""
    by = {os.path.basename(p): p for p in pool}
    used = set(re.findall(r'"@img:([^"]+)"', json.dumps(items)))
    if used - set(by):
        die(f"@img refs without a file: {sorted(used - set(by))}")
    return [by[u] for u in used]


def write(step, note, items, notes=None, extra=None):
    m = {"_note": f"{note} Spec: fable/mother-of-echoes-sim@{SPEC_REF}:{SPEC_PATH}. "
                  "Generated by push/mother_of_echoes.gen.py; do not hand-edit.",
         "dedupNames": True}
    if extra:
        m.update(extra)
    if notes:
        m["_placeholders"] = sorted(set(notes))
    m["items"] = items
    path = os.path.join(DRY_OUT or os.path.join(ROOT, "push"), f"{N[step]}_{SLUG[step]}.json")
    if DRY_SPEC:
        m["_note"] = "DRY RUN from an unpinned spec file; not for the builder. " + m["_note"]
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{os.path.relpath(path, ROOT)}: {len(items)} items")


# ---------------------------------------------------------------------------------------------------------------
# Art pass
# ---------------------------------------------------------------------------------------------------------------
def fx_meta():
    meta = {os.path.basename(a["file"]): a for a in json.load(open(os.path.join(ROOT, FX_META)))["assets"]}
    files = {f for f, _ in FX.values()} | {f for f, _ in FX2.values()}
    if files - set(meta):  # moe_fx_v1.json also lists the first custom heavy and payoff strips the art3 set retired
        die(f"FX table vs {FX_META}: {sorted(files - set(meta))}")
    return meta


def asset_ids(path):
    """466's created asset ids by FX/SCENES key; refuses an incomplete bundle."""
    got = created([path] if path else [], AID)
    need(got, [AID + k for k in (*FX, *SCENES)], "--from (push/466 results)")
    return {k: got[AID + k] for k in (*FX, *SCENES)}


def asset_row(name, typ, frames, speed, hidden):
    return {"name": name, "type": typ, "folder": "MotherOfEchoes", "frames": frames, "speed": speed,
            "hidden": hidden, "onInitialBattleField": False, "licenseDetails": "TNR"}


def assets_items():
    meta = fx_meta()
    items, paths = [], []
    for k, (f, name) in FX.items():
        a = meta[f]
        typ = a["type"]
        frames, speed = (1, 1) if typ == "STATIC" else (a["frames"], a["speed"])
        if typ not in ("STATIC", "ANIMATION") or (typ == "ANIMATION" and speed != 50):
            die(f"{f}: unexpected {typ} speed {speed}")
        items.append({"entity": "asset", "slot": "create", "srcId": AID + k, "name": name,
                      "data": {**asset_row(name, typ, frames, speed, True), "image": "@img:" + f}})
        paths.append(FXDIR + f)
    for k, (f, name, _) in SCENES.items():
        items.append({"entity": "asset", "slot": "create", "srcId": AID + k, "name": name,
                      "data": {**asset_row(name, "SCENE_BACKGROUND", 1, 1, True), "image": "@img:" + f}})
        paths.append(ART + f)
    return items, paths


def unhide_items(aids):
    meta = fx_meta()
    items = []
    for k, (f, name) in FX.items():
        typ = meta[f]["type"]
        frames, speed = (1, 1) if typ == "STATIC" else (meta[f]["frames"], meta[f]["speed"])
        items.append({"entity": "asset", "slot": "edit", "targetId": aids[k], "name": f"{name}: unhide",
                      "data": asset_row(name, typ, frames, speed, False)})
    return items


def item_art_items(econ_path):
    spec_ = importlib.util.spec_from_file_location("uber_econ", os.path.join(ROOT, "push/skyglass_uber_economy.gen.py"))
    E = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(E)
    got = created([econ_path] if econ_path else [], ECON)
    keys = [ECON + k for k in SHARD_ICONS] + [ECON + k for k in TOKEN_ICONS] + [ECON + "var_" + k for k in TOKEN_ICONS]
    need(got, keys, "--economy (push/417)")
    names = {k: n for k, n, *_ in E.SHARDS}
    items = [{"entity": "item", "slot": "edit", "targetId": got[ECON + k], "name": f"{names[k]}: icon",
              "data": {"image": "@img:" + os.path.basename(p)}} for k, p in SHARD_ICONS.items()]
    for key, v, base, bid, story, vdesc, _img in E.TOKENS:
        trade = key in E.TRADEABLE_TOKENS
        desc = E.TOKEN_TMPL.format(story=story, v=v, base=base) + (E.TRADE_NOTE if trade else "")
        items.append({"entity": "item", "slot": "edit", "targetId": got[ECON + key],
                      "name": f"{v} (token): icon and text",
                      "data": {"image": "@img:" + os.path.basename(TOKEN_ICONS[key]), "description": desc}})
        items.append({"entity": "itemVariant", "slot": "edit", "targetId": got[ECON + "var_" + key],
                      "name": f"{v} (variant): final image and text",
                      "data": {"itemId": bid, "image": "@img:" + os.path.basename(VARIANT_ICONS[key]),
                               "description": vdesc}})
    return items, [*SHARD_ICONS.values(), *TOKEN_ICONS.values(), *VARIANT_ICONS.values()]


def unequip_items(b, ids):
    need(ids, [sid(j) for j in b.jutsu] + [sid(a) for a in b.ais], "unequip")
    moe = {ids[sid(j)] for j in b.jutsu}
    items = []
    for aid in [*b.templates, *b.bosses]:
        full = b.ai_entry(aid, ids)["data"]
        items.append({"entity": "ai", "slot": "edit", "targetId": ids[sid(aid)],
                      "name": f"{full['username']}: moe jutsu off (law 18)",
                      "data": {"jutsus": [j for j in full["jutsus"] if j not in moe], "items": full["items"]}})
    return items


def jutsu_art_items(spec, ids, fx):
    b = Build(spec, fx=fx, art=True)
    need(ids, [sid(j) for j in b.jutsu] + [sid(t) for t in b.templates], "jutsu_art")
    items = []
    for jid in [*b.plain_jutsu, *b.summon_jutsu]:
        d = b.jutsu_data(jid, ids if jid in b.summon_jutsu else None)
        items.append({"entity": "jutsu", "slot": "edit", "targetId": ids[sid(jid)], "name": f"{d['name']}: art",
                      "data": d})
    return items, [FAMILY_FILES[b.family[i["data"]["name"]]] for i in items], b.notes


def reequip_items(spec, ids):
    b = Build(spec, art=True)
    need(ids, [sid(j) for j in b.jutsu] + [sid(a) for a in b.ais], "reequip")
    items = []
    for aid in [*b.templates, *b.bosses]:
        e = b.ai_entry(aid, ids)
        items.append({"entity": "ai", "slot": "edit", "targetId": ids[sid(aid)],
                      "name": f"{e['name']}: avatar and kit back (law 18)", "data": e["data"]})
    return items, [ART + f for f in AVATARS.values()], b.notes


def phased(groups):
    """[(phase, items)] -> one item list; Forge runs by phase, then manifest order (manifest.mjs planOrder)."""
    out = []
    for ph, items in groups:
        for it in items:
            out.append({**it, "phase": ph})
    return out


def step_final(spec, ids, econ_path):
    fx = {k: "@scene:" + AID + k for k in FX}  # in-job refs: resolved in data at send time (refs.mjs)
    a_items, a_paths = assets_items()
    b = Build(spec)
    u_items = unequip_items(b, ids)
    j_items, j_paths, j_notes = jutsu_art_items(spec, ids, fx)
    r_items, r_paths, r_notes = reequip_items(spec, ids)
    # Item art (phase 20 in the first master build) ran standalone as push/468 (built by item_art_items, c0509237).
    items = phased([(10, a_items), (30, u_items), (40, j_items), (50, r_items)])
    write("final", (
        f"push/{N['final']}, JOB 1 of 2 of the Mother of Echoes final push (docs/design/MOTHER_OF_ECHOES_ART.md; "
        f"zero live requests to build). Phase 10: {len(a_items)} HIDDEN gameAssets (law 16b, folder MotherOfEchoes): "
        f"the {len(FX)} code-built FX and the {len(SCENES)} act scenes. (No phase 20: the shard, token and variant art "
        "ran standalone as push/468.) Phase 30: law 18 step 1, every "
        f"moe jutsu off its {len(u_items)} AIs (saving a hidden jutsu sets equipped false on its holders, "
        "queries/jutsu.ts:662; an unchanged kit inserts nothing, routers/profile.ts computeUserContentChanges). Phase "
        f"40: all {len(j_items)} moe jutsu re-sent from the spec with family icons and FX (FX by in-job @scene refs, "
        "resolved at send; the lull on The Glass Falls Quiet's fleeprevent). Phase 50: law 18 step 3, the "
        f"{len(r_items)} AIs re-sent whole with avatars, re-equipping every moe jutsu; rules re-sent. Everything that "
        "fights stays HIDDEN and the quest stays hidden: a pause anywhere strands nothing a player can reach (resume "
        f"from the paused job). Keep the results bundle: push/{N['golive']} (job 2) is built from it."),
        items, j_notes + r_notes, extra=pack(a_paths + j_paths + r_paths))


def step_tune(spec, ids, bundle):
    """push/476: the pass-6 tuning on the live hidden records (one job, literal 466 asset ids, no new art files).
    Phase 10 creates the jutsu the spec has but no bundle id covers (pass 6's follow-the-player marks); phase 20 is law
    18 step 1 (moe jutsu off the 9 AIs); phase 30 re-sends every existing moe jutsu from the spec with the 466 art;
    phase 40 re-sends the 9 AIs whole (avatars, kits incl. the new jutsu by in-job @jutsu refs, rules, rows, DR)."""
    fx = asset_ids(bundle)
    b = Build(spec, fx=fx, art=True)
    new = [j for j in b.jutsu if sid(j) not in ids]
    if any(j in b.summon_jutsu for j in new):
        die(f"new summon jutsu {new}: a summon names a template AI; build it in its own step")
    allids = {**ids, **{sid(j): "@jutsu:" + sid(j) for j in new}}
    need(allids, [sid(j) for j in b.jutsu] + [sid(a) for a in b.ais], "tune")
    c_items = []
    for j in new:
        e = b.jutsu_entry(j)
        e.pop("phase", None)
        c_items.append(e)
    u_items = unequip_items(b, allids)
    j_items = []
    for jid in [*b.plain_jutsu, *b.summon_jutsu]:
        if jid in new:
            continue
        d = b.jutsu_data(jid, ids if jid in b.summon_jutsu else None)
        j_items.append({"entity": "jutsu", "slot": "edit", "targetId": ids[sid(jid)], "name": f"{d['name']}: tuning",
                        "data": d})
    r_items = []
    for aid in [*b.templates, *b.bosses]:
        e = b.ai_entry(aid, allids)
        r_items.append({"entity": "ai", "slot": "edit", "targetId": ids[sid(aid)],
                        "name": f"{e['name']}: tuning, kit back (law 18)", "data": e["data"]})
    paths = [FAMILY_FILES[b.family[i["data"]["name"]]] for i in c_items + j_items] + [ART + f for f in AVATARS.values()]
    items = phased([(10, c_items), (20, u_items), (30, j_items), (40, r_items)])
    write("tune", (
        f"push/{N['tune']}: the Mother of Echoes pass-6 tuning (spec at fable/mother-of-echoes-sim {SPEC_REF[:8]}) on the "
        f"live HIDDEN records, art as push/{N['final']} (literal asset ids from its results bundle; no new art files). "
        f"Phase 10: {len(c_items)} new HIDDEN jutsu ({', '.join(b.jname[j] for j in new) or 'none'}). Phase 20: law 18 "
        f"step 1, every moe jutsu off its {len(u_items)} AIs. Phase 30: the {len(j_items)} existing moe jutsu re-sent "
        f"from the spec. Phase 40: the {len(r_items)} AIs re-sent whole (avatars, kits incl. the new jutsu by in-job "
        "@jutsu refs, rules, damage rows, damage reduction), re-equipping every moe jutsu. Everything stays hidden; a "
        "pause strands nothing a player can reach (resume the paused job). The practice quest (push/469) and the real "
        "quest point at the same boss ids, so both pick this up."),
        items, b.notes, extra=pack(paths))


# Tags whose handler flips their power negative when cast on a character (tags.ts: decreaseStats :847,
# decreaseMastery :892, decreaseDamageGiven :977, decreaseDamageTaken :1062, decreaseHealGiven :1173, decreasepoolcost
# :1816). The client hides any record with power <= 0 (combatEffects.ts:183-187, :215), so art on them never shows on a
# character, and a pool's fromGround copy shares the ground effect's id (process.ts:398-411), so an occupant hides the
# pool's art too (COMBAT_ANIMATION_ENGINE.md section 5.1). Art moves to a positive sibling tag of the same cast.
NEGATIVE_TAGS = {"decreasedamagetaken", "decreasedamagegiven", "decreasestat", "decreasemastery", "decreaseheal",
                 "decreasepoolcost"}
ART_CARRIERS = ("increasedamagetaken", "healprevent", "clearprevent")


def move_off_negative(d):
    """Move art fields off negative-power tags onto the first art-free positive sibling; returns the moves made."""
    moves = []
    for e in d["effects"]:
        if e["type"] not in NEGATIVE_TAGS or not any(e.get(f) for f in ART_FIELDS):
            continue
        dst = next((x for c in ART_CARRIERS for x in d["effects"]
                    if x["type"] == c and not any(x.get(f) for f in ART_FIELDS)), None)
        if dst is None:
            die(f"{d['name']}: art on {e['type']} (hidden when cast) and no positive sibling to carry it")
        for f in ART_FIELDS:
            dst[f], e[f] = e.get(f) or "", ""
        moves.append(f"{d['name']}: {e['type']} -> {dst['type']}")
    return moves


def fx2_rows(only4=False):
    """The push/478 asset rows: FX2 (moe_fx_v1.json), FX3 (moe_fx_a3.json), then the scene characters. only4: the
    art4 entrance rows alone (FX4, moe_fx_a4.json), for the final tuning job."""
    if set(FX2) & set(FX3) or set(FX4) & (set(FX2) | set(FX3)) or (set(FX2) | set(FX3) | set(FX4)) & set(SCENE_CHARS):
        die("FX2 / FX3 / SCENE_CHARS keys overlap")
    meta = fx_meta()
    a3 = json.load(open(os.path.join(ROOT, FX3_META)))
    meta3 = {os.path.basename(a["file"]): a for a in a3["assets"]}
    if {f for f, _ in FX3.values()} != set(meta3):
        die(f"FX3 table vs {FX3_META}: {sorted({f for f, _ in FX3.values()} ^ set(meta3))}")
    sc3 = {os.path.basename(a["file"]) for a in a3["scene_characters"]}
    if {f for f, _, _ in SCENE_CHARS.values()} != sc3:
        die(f"SCENE_CHARS vs {FX3_META}: {sorted({f for f, _, _ in SCENE_CHARS.values()} ^ sc3)}")
    meta4 = {os.path.basename(a["file"]): a for a in json.load(open(os.path.join(ROOT, FX4_META)))["assets"]}
    if {f for f, _ in FX4.values()} != set(meta4):
        die(f"FX4 table vs {FX4_META}: {sorted({f for f, _ in FX4.values()} ^ set(meta4))}")
    rows = []
    tables = ((FX4, meta4, FXDIR),) if only4 else ((FX2, meta, FXDIR), (FX3, meta3, FXDIR))
    for table, m, d in tables:
        for k, (f, name) in table.items():
            a = m[f]
            typ = a["type"]
            frames, speed = (1, 1) if typ == "STATIC" else (a["frames"], a["speed"])
            if typ not in ("STATIC", "ANIMATION") or (typ == "ANIMATION" and speed != 50):
                die(f"{f}: unexpected {typ} speed {speed}")
            rows.append((k, f, name, typ, frames, speed, d + f))
    if only4:
        return rows
    for k, (f, name, _) in SCENE_CHARS.items():
        rows.append((k, f, name, "SCENE_CHARACTER", 1, 1, ART + f))
    return rows


AID4 = "sg498_"


def custom_fx_refs(art2_bundle, art4_bundle=None):
    """The custom set as the final tuning job needs it: FX2, FX3 and the portraits by literal id from the push/478 run
    (it ran inside the push/489 master: harvests/inbox/tnr_results_1793931586141.json), FX4 by literal id from an art4
    bundle, or by in-job @scene ref when the same job creates them (fx4_create_items, phase before the jutsu)."""
    got = created([art2_bundle], AID2)
    keys2 = [k for k, *_ in fx2_rows()]
    need(got, [AID2 + k for k in keys2 if k not in FX2], "--art2-from (push/478 results)")
    refs = {k: got[AID2 + k] for k in keys2 if AID2 + k in got}
    if art4_bundle:
        g4 = created([art4_bundle], AID4)
        need(g4, [AID4 + k for k in FX4], "--art4-from")
        refs.update({k: g4[AID4 + k] for k in FX4})
    else:
        refs.update({k: "@scene:" + AID4 + k for k in FX4})
    return refs


def fx4_create_items():
    """The art4 entrance assets, created HIDDEN (law 16b); a later job unhides them (law 16c, art4_unhide_items)."""
    items, paths = [], []
    for k, f, name, typ, frames, speed, path in fx2_rows(only4=True):
        items.append({"entity": "asset", "slot": "create", "srcId": AID4 + k, "name": name,
                      "data": {**asset_row(name, typ, frames, speed, True), "image": "@img:" + f}})
        paths.append(path)
    return items, paths


def art4_unhide_items(art4_bundle):
    g4 = created([art4_bundle], AID4)
    need(g4, [AID4 + k for k in FX4], "art4 unhide")
    return [{"entity": "asset", "slot": "edit", "targetId": g4[AID4 + k], "name": f"{name}: unhide",
             "data": asset_row(name, typ, frames, speed, False)} for k, f, name, typ, frames, speed, _ in fx2_rows(True)]


def sfx_for(name):
    for k, v in SFX_BY_NAME:
        if name == k or name.startswith(k):
            return v
    return None


def add_sfx(d, rec):
    """One existing sound per cast (director 2026-11-05). A single-target or CHARACTER cast makes one record per hit
    character, so its art-bearing hit carries the sound; a ground cast stamps every tile, so a one-tile visual at the
    caster carries it. Returns where it went."""
    key = sfx_for(d["name"])
    if key is None:
        die(f"{d['name']}: no sound (SFX_BY_NAME)")
    if rec.get("method") == "SINGLE" or rec.get("target") == "CHARACTER":
        host = next((e for e in d["effects"] if e["type"] not in NEGATIVE_TAGS and e["type"] != "visual"
                     and any(e.get(f) for f in ART_FIELDS)), None)
        if host is None:
            die(f"{d['name']}: no art-bearing positive hit to carry the sound")
        host["appearSfx"] = SFX[key]
        return f"{key} on {host['type']}"
    d["effects"].append({**VISUAL, "appearSfx": SFX[key],
                         "coordinateTargeting": {"origin": "CASTER", "selection": "ALL",
                                                 "coordinates": [{"longitude": 0, "latitude": 0}]},
                         "description": f"{d['name']}: sound (art only)"})
    return f"{key} on a caster visual"


def step_art2(spec, ids, bundle):
    """push/478: the custom set (no borrowed animations; director 2026-11-05) with the art3 material arc, mosaics, one
    sound per cast and the dialog portraits. Phase 10 creates the assets HIDDEN (law 16b); phase 20 is law 18 step 1
    (moe jutsu off the 9 AIs); phase 30 re-sends every moe jutsu from the spec with the custom set by in-job @scene refs
    and the 466 art by literal ids; phase 40 re-sends the 9 AIs whole (re-equip). Tuning is whatever SPEC_REF holds, so
    a SPEC_REF bump rebuilds this with no art change."""
    fx = asset_ids(bundle)
    rows = fx2_rows()
    fx2 = {k: "@scene:" + AID2 + k for k, *_ in rows}
    b = Build(spec, fx=fx, art=True, fx2=fx2)
    need(ids, [sid(j) for j in b.jutsu] + [sid(a) for a in b.ais], "art2 (the 476 bundle holds the pass-6 jutsu ids)")
    u_items = unequip_items(b, ids)
    j_items, moved, sounds, waves = [], [], {}, []
    for jid in [*b.plain_jutsu, *b.summon_jutsu]:
        d = b.jutsu_data(jid, ids if jid in b.summon_jutsu else None)
        moved += move_off_negative(d)
        nwave = sum(1 for e in d["effects"] if e["type"] == "visual" and e.get("target") == "COORDINATES")
        if nwave:
            waves.append(f"{d['name']} ({nwave})")
        sounds.setdefault(add_sfx(d, b.jutsu[jid]["record"]).split(" on ")[0], []).append(d["name"])
        j_items.append({"entity": "jutsu", "slot": "edit", "targetId": ids[sid(jid)], "name": f"{d['name']}: custom art",
                        "data": d})
    r_items = []
    for aid in [*b.templates, *b.bosses]:
        e = b.ai_entry(aid, ids)
        r_items.append({"entity": "ai", "slot": "edit", "targetId": ids[sid(aid)],
                        "name": f"{e['name']}: kit back (law 18)", "data": e["data"]})
    used = {v for i in j_items for e in i["data"]["effects"] for f in ART_FIELDS for v in [e.get(f) or ""]}
    unused3 = sorted(k for k in FX3 if fx2[k] not in used and k not in FX3_UNWIRED)
    if unused3:
        die(f"art3 assets no jutsu uses: {unused3}")
    a_items, paths = [], []
    for k, f, name, typ, frames, speed, path in rows:
        if k in FX2 and fx2[k] not in used:
            continue  # an FX2 fallback no slot needs this spec
        a_items.append({"entity": "asset", "slot": "create", "srcId": AID2 + k, "name": name,
                        "data": {**asset_row(name, typ, frames, speed, True), "image": "@img:" + f}})
        paths.append(path)
    paths += [FAMILY_FILES[b.family[i["data"]["name"]]] for i in j_items] + [ART + f for f in AVATARS.values()]
    items = phased([(10, a_items), (20, u_items), (30, j_items), (40, r_items)])
    nsc = len(SCENE_CHARS)
    write("art2", (
        f"push/{N['art2']}: the Mother of Echoes custom animation set (director 2026-11-05: no borrowed animations; "
        "art3: \"a high end boss fight ... pull out all the stops\"; docs/design/MOTHER_OF_ECHOES_ART.md). Phase 10: "
        f"{len(a_items)} HIDDEN gameAssets (law 16b): the act-material danger grammar (heavy marks in Heartglass, the "
        "turn and the Remainder; the Silence's dark lock and pools), the custom payoffs and their wave strips, the "
        f"summon rises, {len(FX3_UNWIRED)} boss aura and act-start strips held for the sim's act buffs (not wired yet), "
        f"and {nsc} SCENE_CHARACTER dialog portraits (Sayo only; used by the quest edits, push/{N['art2_unhide']} and "
        f"push/{N['golive']}). Phase 20: law 18 step 1, every moe jutsu off its {len(u_items)} AIs. Phase 30: all "
        f"{len(j_items)} moe jutsu re-sent from the spec at {SPEC_REF[:8]} (tuning unchanged) with the custom set by "
        "in-job @scene refs and the push/466 art by literal ids. Art on tags that go negative when cast moved to a "
        f"positive sibling ({len(moved)}: {'; '.join(moved)}; COMBAT_ANIMATION_ENGINE.md 5.1); no ground mark carries "
        "a disappear clip (5.3). Mosaics: the hit's own appear is blanked and zero-impact visual tags (power 2, target "
        f"COORDINATES, a subset of the cast's tiles, no gameplay handler) play the wave by band: {'; '.join(waves)}. "
        "One existing in-game sound per cast (an art-bearing single hit, or a one-tile visual at the caster): "
        f"{'; '.join(f'{k}: {len(v)}' for k, v in sorted(sounds.items()))}. The visual tags change no numbers; the sim "
        "confirms identical clear rates on a fixed-seed rerun. Phase 40: the "
        f"{len(r_items)} AIs re-sent whole, re-equipping every moe jutsu. Everything stays hidden. The new FX play only "
        f"after push/{N['art2_unhide']} unhides them (built from this job's results bundle; an unhide cannot run "
        "in-job: Forge sends an edit's targetId as written and lint L13 refuses hidden:false creates)."),
        items, b.notes, extra=pack(paths))


def scene_char_ids(bundle):
    got = created([bundle], AID2)
    need(got, [AID2 + k for k in SCENE_CHARS], "--art2-from (push/478 results)")
    return {k: got[AID2 + k] for k in SCENE_CHARS}


def step_art2_unhide(bundle, b, ids, econ, scenes_bundle):
    """push/479: unhide the 478 FX (law 16c) and re-send the practice quest whole with the dialog portraits."""
    got = created([bundle], AID2)
    rows = [r for r in fx2_rows() if r[3] != "SCENE_CHARACTER" and AID2 + r[0] in got]
    missing = sorted(k for k in FX3 if AID2 + k not in got)
    if missing:
        die(f"--from (push/478 results) lacks {missing}")
    items = [{"entity": "asset", "slot": "edit", "targetId": got[AID2 + k], "name": f"{name}: unhide",
              "data": asset_row(name, typ, frames, speed, False)} for k, f, name, typ, frames, speed, _ in rows]
    _s = importlib.util.spec_from_file_location("moe_practice", os.path.join(ROOT, "push",
                                                                             "mother_of_echoes_practice.gen.py"))
    P = importlib.util.module_from_spec(_s)
    _s.loader.exec_module(P)
    d = P.practice_data(b, ids, econ, asset_ids(scenes_bundle), chars=scene_char_ids(bundle))
    q = [{"entity": "quest", "slot": "edit", "targetId": PRACTICE_QUEST, "name": f"{P.NAME}: dialog portraits",
          "data": d}]
    write("art2_unhide", (
        f"push/{N['art2_unhide']} (after push/{N['art2']}; literal asset ids from its results bundle). Phase 10: the "
        f"{len(items)} custom Mother of Echoes FX assets unhidden (law 16c: battles load only unhidden assets; the "
        "scene characters need none, gameAsset.getSceneAssets does not filter hidden). Phase 20: the practice quest "
        f"(push/469, {PRACTICE_QUEST}) re-sent whole (quest edits do not fetch-merge) with Sayo's dialog portraits "
        "(Act I Sayo in d_intro1, d_intro2 and d_open; the Glasswright in d_act2; the Saint in d_act3), the opening "
        "build-up, its icon and the act scenes; still hidden."),
        phased([(10, items), (20, q)]), extra=pack([QUEST_ICON]))


def step_golive(b, ids, econ, bundle, art2_bundle):
    aids = asset_ids(bundle)
    u_items = unhide_items(aids)
    d = quest_data(b, ids, econ, aids, chars=scene_char_ids(art2_bundle))
    d["hidden"] = False
    q = [{"entity": "quest", "slot": "edit", "targetId": ids[PFX + "quest"], "name": f"{Q_NAME}: publish", "data": d}]
    write("golive", (
        f"push/{N['golive']}, JOB 2 of 2 (after push/{N['final']}; literal asset ids from its results bundle). Phase 10: "
        f"the {len(u_items)} FX assets unhidden (law 16c: battles load only unhidden assets). Phase 20: the quest "
        "re-sent whole with hidden false, its icon (ME13) and the three act scenes (heart: content, d_open, b_act1, "
        "f_lost; stilling: d_act2, b_act2; impression: d_act3, b_act3, w_clear) and Sayo's dialog portraits from "
        f"push/{N['art2']} (Act I Sayo in d_intro1, d_intro2, d_open; the Glasswright in d_act2; the Saint in d_act3). Why a second job: an unhide is an edit "
        "and Forge sends an edit's targetId as written (runner.mjs _fill: item.entityId ?? item.targetId; refs.mjs "
        "resolves @refs in data only), and lint L13 refuses a create with hidden:false, so the FX cannot be created "
        "or unhidden visible inside job 1. Publishing here, after the unhide, means the fight never goes live with "
        "invisible marks."), phased([(10, u_items), (20, q)]), extra=pack([QUEST_ICON]))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--step", choices=["jutsu", "templates", "summons", "bosses", "quest", "final", "golive", "tune",
                                               "art2", "art2_unhide"],
                    default="jutsu")
    ap.add_argument("--bundles", nargs="*", default=[], help="results bundles of 440 and 461-464 (any order)")
    ap.add_argument("--economy", help="push/417 results bundle (the shards, Heartglass and The Remainder tokens)")
    ap.add_argument("--from", dest="frm", help="push/466 (job 1) results bundle: the art assets' ids (golive, tune, "
                    "art2); push/478's for art2_unhide")
    ap.add_argument("--art2-from", dest="art2", help="push/478 results bundle: the dialog portraits (golive)")
    ap.add_argument("--scenes", help="push/466 results bundle: the act scenes (art2_unhide's practice-quest edit)")
    a = ap.parse_args()
    spec = load_spec()
    b = Build(spec)
    ids = created(a.bundles, PFX)
    if a.step == "final":
        return step_final(spec, ids, a.economy)
    if a.step == "tune":
        if not a.frm:
            die("--step tune needs --from <push/466 results bundle> (the art asset ids)")
        return step_tune(spec, ids, a.frm)
    if a.step in ("art2", "art2_unhide"):
        if not a.frm:
            die(f"--step {a.step} needs --from <push/466 results bundle> (art2) or <push/478 results bundle> (art2_unhide)")
        if a.step == "art2":
            return step_art2(spec, ids, a.frm)
        econ = created([a.economy] if a.economy else [], ECON)
        need(econ, [ECON + k for k in ("keel", "crown", "tide", "ledger", *TOKEN_PCT)], "--economy (push/417)")
        need(ids, [sid(t) for t in b.bosses], "art2_unhide")
        if not a.scenes:
            die("--step art2_unhide needs --scenes <push/466 results bundle> (the practice quest's act scenes)")
        return step_art2_unhide(a.frm, Build(spec, art=True), ids, econ, a.scenes)
    if a.step == "golive":
        econ = created([a.economy] if a.economy else [], ECON)
        need(econ, [ECON + k for k in ("keel", "crown", "tide", "ledger", *TOKEN_PCT)], "--economy (push/417)")
        need(ids, [sid(t) for t in b.bosses] + [PFX + "quest"], "golive")
        if not a.art2:
            die("--step golive needs --art2-from <push/478 results bundle> (the dialog portraits)")
        return step_golive(b, ids, econ, a.frm, a.art2)

    if a.step == "jutsu":
        items = [b.jutsu_entry(j) for j in b.plain_jutsu]
        write("jutsu", (
            f"push/440 (RUL-2026-11-02-103 part 2), all HIDDEN: the {len(items)} new Mother of Echoes jutsu that name no "
            f"AI (the {len(b.summon_jutsu)} summon jutsu come in push/442 with literal aiIds; Stolen Form "
            f"{STOLEN_FORM} is reused live, not created). No earlier ids needed. Telegraph marks ride the "
            "increaseregeneration carrier with the live Skyglass tiles (push/431); pool art on the lasting effect."),
            items, b.notes)
    elif a.step == "templates":
        need(ids, [sid(j) for j in b.plain_jutsu], "templates")
        items = [b.ai_entry(t, ids) for t in b.templates]
        write("templates", f"push/441 (from push/440's bundle; literal ids, law 17): the {len(items)} summon-template "
              "AIs, plain AI rows (the engine marks the summoned unit). No hidden column on AI records (law 16b); "
              "inArena false, referenced only by push/442's summon jutsu.", items, b.notes)
    elif a.step == "summons":
        need(ids, [sid(t) for t in b.templates], "summons")
        items = [b.jutsu_entry(j, ids) for j in b.summon_jutsu]
        write("summons", f"push/442 (from push/441's bundle; literal aiIds, law 17), all HIDDEN: the {len(items)} "
              "summon jutsu.", items, b.notes)
    elif a.step == "bosses":
        need(ids, [sid(j) for j in b.plain_jutsu + b.summon_jutsu], "bosses")
        items = [b.ai_entry(t, ids) for t in b.bosses]
        write("bosses", f"push/443 (from push/440 and 442's bundles; literal ids, law 17): the {len(items)} boss AIs "
              f"with AI Heavy Armor ({HEAVY_ARMOR}), inArena false. Fresh creates, equipped once (law 18: any later "
              "edit to an equipped moe jutsu is unequip, edit, re-equip).", items, b.notes)
    elif a.step == "quest":
        econ = created([a.economy] if a.economy else [], ECON)
        need(econ, [ECON + k for k in ("keel", "crown", "tide", "ledger", *TOKEN_PCT)], "--economy (push/417)")
        need(ids, [sid(t) for t in b.bosses], a.step)
        d = quest_data(b, ids, econ)
        write("quest", "push/444 (literal ids from push/417 and 440-443, law 17): the HIDDEN battle pyramid, one "
              "repeatable quest (RUL-2026-11-02-105: no first-clear mechanics, no title). Every clear rolls the "
              "Heartglass and The Remainder tokens (both tradeable) and a pick of one reward.",
              [{"entity": "quest", "slot": "create", "srcId": PFX + "quest", "phase": 1, "name": Q_NAME, "data": d}],
              [f"quest {PFX}quest: image and every node's scene {CORE_CHAMBER}"])

if __name__ == "__main__":
    main()
