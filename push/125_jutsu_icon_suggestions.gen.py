#!/usr/bin/env python3
"""Generate push/125: the new Aerathiel, Vaporia and Blood-Enchanted Eyes jutsu icons, sent to the
content review desk (Forge suggest mode). Do not hand-edit the output.

Each item changes one field, `image` (injectableInBattle is re-sent at its captured value, law 20:
omitted means false), and carries its own rationale (RUL-2026-10-19-007).
Crimson Impact is held back: Ravena Bloodsilk equips it, and an approved edit would sever that
AI's combat link (laws 18, 60), so it needs an unequip -> edit -> re-equip run instead.

Inputs (all committed):
  - docs/design/bloodright/balance/kits_from_reference_captures.json  (jutsu ids)
  - art/jutsu_icons/{aerathiel,vaporia}/*.webp and art/style_refs/jutsu_icons/bee/*.webp
Then bind the pack:  node forge/tools/make_image_pack.mjs push/125_jutsu_icon_suggestions.json --map ... --ref <commit> --write
(the generator runs that step itself).

  python3 push/125_jutsu_icon_suggestions.gen.py [<image pack ref>]

Retry of a single item that failed in the 125 run (one manifest per retry, so the items already in
review are not suggested twice):
  python3 push/125_jutsu_icon_suggestions.gen.py <ref> --only "Particle Cannon" --out push/129_particle_cannon_icon_retry.json
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "push/125_jutsu_icon_suggestions.json"
KITS = json.loads((ROOT / "docs/design/bloodright/balance/kits_from_reference_captures.json").read_text())

AER, VAP, BEE = "art/jutsu_icons/aerathiel", "art/jutsu_icons/vaporia", "art/style_refs/jutsu_icons/bee"

# (kit slug, jutsu name, repo path, rationale)
ICONS = [
    ("aerathiel", "Windshear Decay", f"{AER}/Aerathiel_Windshear_Decay_jutsu_v1.webp",
     "New Aerathiel icon: razor wind slashes tearing through a cloud of crumbling dust, matching a technique whose wind cuts leave lasting decay on the target."),
    ("aerathiel", "Death's March", f"{AER}/Aerathiel_Deaths_March_jutsu_v1.webp",
     "New Aerathiel icon: rings of chakra rolling outward through shattered rock, matching the waves of chakra this area attack releases at its target."),
    ("aerathiel", "Atomic Shield", f"{AER}/Aerathiel_Atomic_Shield_jutsu_v1.webp",
     "New Aerathiel icon: a sphere of orbiting particles and dust fragments, matching the particle barrier the user raises to protect themselves."),
    ("aerathiel", "Decaying Touch", f"{AER}/Aerathiel_Decaying_Touch_jutsu_v1.webp",
     "New Aerathiel icon: an open palm glowing at the centre with the ground breaking into dust beneath it, matching a touch that destroys the target's body through dusty decay."),
    ("aerathiel", "Particle Cannon", f"{AER}/Aerathiel_Particle_Cannon_jutsu_v1.webp",
     "New Aerathiel icon: a concentrated beam firing out of a triangular particle formation, matching the bloodline's ultimate high-damage single-target strike."),
    ("vaporia", "Azure Dragon Palm", f"{VAP}/vaporia_azure_dragon_palm_jutsu_icon_v1.webp",
     "New Vaporia icon: a dragon formed from boiling water over embers, matching the jutsu's description of striking from the safety of your dragon."),
    ("vaporia", "Drowning Strike", f"{VAP}/vaporia_drowning_strike_jutsu_icon_v1.webp",
     "New Vaporia icon: a heavy downward surge of boiling water with heat at its base, matching a fist of boiling water driven into the target."),
    ("vaporia", "Liquid Ember Shell", f"{VAP}/vaporia_liquid_ember_shell_jutsu_icon_v1.webp",
     "New Vaporia icon: a shell of swirling water wrapped around molten fire and steam, matching the shell of molten fire and water that encases the user."),
    ("vaporia", "Scorch Break", f"{VAP}/vaporia_scorch_break_jutsu_icon_v1.webp",
     "New Vaporia icon: a line of fire splitting a wall of boiling water, showing the fire-and-water Boil style that this basic technique introduces."),
    ("vaporia", "Surfing Strike", f"{VAP}/vaporia_surfing_strike_jutsu_icon_v1.webp",
     "New Vaporia icon: a cresting wave of boiling water over a streak of heat, matching the gliding movements atop boiling water this jutsu describes."),
    ("blood_enchanted_eyes", "Ring of Spilled Blood", f"{BEE}/icon_bee_ring_of_spilled_blood_v2.webp",
     "New Blood-Enchanted Eyes icon: a spiral of spent blood, matching the spiral this jutsu throws across the ground to open and weaken what stands against the user."),
    ("blood_enchanted_eyes", "Crimson Tithe", f"{BEE}/icon_bee_crimson_tithe_v1.webp",
     "New Blood-Enchanted Eyes icon: a chalice taking in a stream of blood, matching the toll in blood that locks the victim in place."),
    ("blood_enchanted_eyes", "Sanguine Plague", f"{BEE}/icon_bee_sanguine_plague_v3.webp",
     "New Blood-Enchanted Eyes icon: a skull wreathed in diseased red smoke, matching the burning blood sickness this jutsu seeds in a rival."),
    ("blood_enchanted_eyes", "Reaper's Embrace", f"{BEE}/icon_bee_reapers_embrace_v1.webp",
     "New Blood-Enchanted Eyes icon: a reaper's scythe trailing blood, matching the jutsu's close-in drain that tears vitality from the target."),
    ("blood_enchanted_eyes", "Unholy Enhancement", f"{BEE}/icon_bee_unholy_enhancement_v2.webp",
     "New Blood-Enchanted Eyes icon: corrupted red veins spreading through darkness, matching the corrupted vitality the user awakens to amplify their strength."),
    ("blood_enchanted_eyes", "Hemocure", f"{BEE}/icon_bee_hemocure_v1.webp",
     "New Blood-Enchanted Eyes icon: a sphere of contained blood cradled by dark tendrils, matching the user commanding their blood to seal wounds and absorb incoming harm."),
    ("blood_enchanted_eyes", "Thousand Strike", f"{BEE}/icon_bee_thousand_strike_v1.webp",
     "New Blood-Enchanted Eyes icon: a rain of blood-red spikes, matching the relentless barrage that shatters the target's defences."),
]
HELD_BACK = {"Crimson Impact": "equipped by Ravena Bloodsilk (laws 18, 60)"}


def main():
    args = sys.argv[1:]
    only = args[args.index("--only") + 1] if "--only" in args else None
    out = ROOT / args[args.index("--out") + 1] if "--out" in args else OUT
    positional = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] not in ("--only", "--out"))]
    ids = {(slug, j["name"]): j["id"] for slug, k in KITS.items() for j in k["jutsu"]}
    injectable = {j["id"]: j.get("injectableInBattle") for k in KITS.values() for j in k["jutsu"]}
    items, img_sizes, maps = [], {}, []
    for slug, name, path, why in ICONS:
        if only and name != only:
            continue
        jid = ids.get((slug, name))
        if not jid:
            raise SystemExit(f"no captured jutsu {name} in {slug}")
        if not isinstance(injectable[jid], bool):
            raise SystemExit(f"{name}: captured injectableInBattle missing")
        logical = Path(path).name
        img_sizes[logical] = (ROOT / path).stat().st_size
        maps += ["--map", f"{logical}={path}"]
        items.append({"entity": "jutsu", "slot": "edit", "name": name, "targetId": jid,
                      "data": {"image": f"@img:{logical}", "injectableInBattle": injectable[jid]}, "suggestion": {"rationale": why}})
    manifest = {
        "_note": ("Jutsu icon refresh for Aerathiel (5), Vaporia (5) and Blood-Enchanted Eyes (7), sent to the content "
                  "review desk; nothing changes until a reviewer approves. Only `image` changes. Crimson Impact is held "
                  "back: " + HELD_BACK["Crimson Impact"] + ". Generated by push/125_jutsu_icon_suggestions.gen.py; "
                  "do not hand-edit. Operator-run only."),
        "mode": "suggest",
        "suggestion": {"category": "VISUAL", "title": "Jutsu icon refresh",
                       "rationale": "New jutsu icon from the director-approved bloodline icon set."},
        "imgSizes": img_sizes,
        "items": items,
    }
    if only:
        if not items:
            raise SystemExit(f"no icon item named {only}")
        manifest["_note"] = (f"Retry of {only} from push/125 (its upload failed: PUT 409 File already exists). Sent to the "
                             "content review desk; only `image` changes. Generated by push/125_jutsu_icon_suggestions.gen.py "
                             "--only; do not hand-edit. Operator-run only.")
    out.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    ref = positional[0] if positional else "HEAD"
    subprocess.run(["node", str(ROOT / "forge/tools/make_image_pack.mjs"), str(out), *maps, "--ref", ref, "--write"], check=True)


if __name__ == "__main__":
    main()
