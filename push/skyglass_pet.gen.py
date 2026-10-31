#!/usr/bin/env python3
"""The Skyglass pet: the Little Horror species, its signature jutsu Little Maw and The Little Horror's Jar (push/346),
and the species' default loadout (push/347). All HIDDEN, engine-default placeholder art (RUL-2026-10-30-059; nothing
is published until the art lands, RUL-2026-10-31-066 item 4). Kit and numbers: RUL-2026-10-31-068,
docs/design/SKYGLASS_PETS.md "Little Horror".

    python3 push/skyglass_pet.gen.py                              # push/346: species -> jutsu -> jar (3 creates)
    python3 push/skyglass_pet.gen.py --defaults <346 bundle>      # push/347: species defaults = [Little Maw]
    python3 push/skyglass_pet.gen.py --defaults <346 bundle> --out <path>   # write elsewhere (stand-in tests)

Templates (RUL-2026-10-31-068): the push/345 capture harvests/inbox/tnr_results_1793460185610.json.
  - Innate effects are shaped exactly like the live legendary species' rows: Dragon's `afterburn` 25% row (target
    INHERIT, skillTarget ENEMIES, rounds 30, percentage) for Rot Bite, the Kitsune's `increasedamagegiven` 30% row
    (target INHERIT, skillTarget SELF) for Hungry. Both rows are copied from the capture and only type/power/
    description (and poison's own fields) change.
  - Little Maw is the Yamabiko's Rallying Echo record (a live PETS jutsu) with the director's numbers.

Engine (theninjarpg@3314d122):
  - validators/petSpecies.ts: PetSpeciesEffect = AllTags & {skillTarget?}; isActive required; defaults <= slots.
  - libs/combat/pets.ts ~146-180: an ENEMIES innate is realized on EVERY living enemy at battle start with the
    companion as caster (not on each hit); a SELF innate on the owner and the companion. Both enter already active.
  - validators/combat.ts ~805-815 PoisonTag: type "poison", calculation percentage only, poolsAffected (default
    Health/Chakra/Stamina), **rounds 1-10**. A 30-round row (the Dragon template) is refused, so Rot Bite carries
    rounds 10, the schema maximum (RUL-2026-10-31-068 records this). libs/combat/tags.ts ~2256-2313: the poisoned
    target takes power% of the chakra + stamina it spends on each action as damage.
  - validators/combat.ts ~970-993 NonCombatConsumeRewardTag.reward_pets (species ids, standard rewardMode); ~1679-1689
    at most PET_MAX_CONSUME_PETS per item and the item must set preventBattleUsage.
  - routers/petSpecies.ts: defaults must be PUBLISHED PETS jutsu; a create refuses species-locked defaults, so the
    defaults are push/347, after the director publishes Little Maw.
  - Forge resolves `@petSpecies:<srcId>` minted earlier in the same job (forge/src/runner/refs.mjs), so the jutsu's
    requiredPetSpeciesId and the jar's reward_pets ride in this manifest.

Do not hand-edit the outputs.
"""
import copy
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(name):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), os.path.join(ROOT, "push", name))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


IT = _load("skyglass_items.gen.py")
T = IT.T
PLACEHOLDER = IT.PLACEHOLDER

NUM, DEFAULTS_NUM = 346, 347
PFX = "sg346_"  # srcIds are unique across every Forge job
SPECIES_SRC, JUTSU_SRC, JAR_SRC = PFX + "little_horror", PFX + "little_maw", PFX + "little_horror_jar"
SPECIES, JUTSU, JAR = "Little Horror", "Little Maw", "The Little Horror's Jar"
CAPTURE_345 = "harvests/inbox/tnr_results_1793460185610.json"
PETS_DOC = os.path.join(ROOT, "docs/design/SKYGLASS_PETS.md")

DESCRIPTION = ("The Core tried to remember the ship's mascot. This is what came back: a small, damp thing with one tooth "
               "too many, and it has decided you are its crew.")
MAW_DESCRIPTION = ("The Little Horror opens a mouth far too big for its body and bites, leaving the target easier to "
                   "hurt for a round.")
MAW_BATTLE = "%user opens a maw far too big for its body and bites down on %target."
POISON_ROUNDS_MAX = 10  # PoisonTag.rounds .max(10) at 3314d122


# ---------------------------------------------------------------------------------------------------------------
# The 345 capture: templates and the name check
# ---------------------------------------------------------------------------------------------------------------
def capture():
    caps = json.load(open(os.path.join(ROOT, CAPTURE_345)))["captures"]
    species = next(c for c in caps if c["proc"] == "petSpecies.getAll")["data"]
    jutsu = [j for c in caps if c["proc"] == "jutsu.getAll" for j in c["data"]]
    assert len(species) == 69 and len(jutsu) == 4, (len(species), len(jutsu))
    return species, jutsu


SPECIES_CAP, JUTSU_CAP = capture()
assert SPECIES not in {s["name"] for s in SPECIES_CAP}, "species names are unique and a create cannot be deleted"
assert JUTSU not in {j["name"] for j in JUTSU_CAP}


def live_species(name):
    return next(s for s in SPECIES_CAP if s["name"] == name)


def live_row(species, etype, power):
    rows = [e for e in live_species(species)["effects"] if e["type"] == etype and e["power"] == power]
    assert len(rows) == 1, (species, etype, power)
    return copy.deepcopy(rows[0])


# ---------------------------------------------------------------------------------------------------------------
# Species
# ---------------------------------------------------------------------------------------------------------------
def pets_doc_kit():
    """artDirection and the 10 rankConcepts, verbatim from SKYGLASS_PETS.md's Little Horror kit."""
    L = open(PETS_DOC, encoding="utf-8").read().split("\n")
    i = L.index("### Little Horror")
    kit = []
    for l in L[i + 1:]:
        if l.startswith("#"):
            break
        kit.append(l)
    art = [l for l in kit if l.startswith("- Art direction: ")]
    assert len(art) == 1
    concepts = []
    for l in kit:
        m = re.match(r"^\s+(\d+)\. [A-Za-z]+: `(.+)`$", l)
        if m:
            assert int(m.group(1)) == len(concepts) + 1
            concepts.append(m.group(2))
    assert len(concepts) == 10, len(concepts)
    return art[0][len("- Art direction: "):], concepts


def rot_bite():
    # RUL-2026-10-31-070: enemies deal 10% less damage for the whole battle. Built on the Dragon's live
    # increasedamagetaken 30% row (target SELF, skillTarget ENEMIES, rounds 30, percentage): the same enemy-facing
    # innate shape, as decreasedamagegiven 10%. (Poison was dropped: it only bites on chakra/stamina spent, and most AI
    # jutsu cost little against their pools; a flat pool-cost rise was dropped too, since poison ignores static costs.)
    e = live_row("Dragon", "increasedamagetaken", 30)
    e.update({"type": "decreasedamagegiven", "power": 10, "description": "Decrease damage given by target"})
    e.pop("poolsAffected", None)
    assert e["skillTarget"] == "ENEMIES" and e["calculation"] == "percentage" and e["rounds"] == 30
    return e


def hungry():
    # The Kitsune's increasedamagegiven 30% row (target INHERIT, skillTarget SELF), at 20%.
    e = live_row("Kitsune", "increasedamagegiven", 30)
    e.update({"power": 20, "description": "Increase damage given by target"})  # IncreaseDamageGivenTag's own
    assert e["rounds"] == 30 and e["skillTarget"] == "SELF" and e["calculation"] == "percentage"
    return e


def species():
    art, concepts = pets_doc_kit()
    return {"entity": "petSpecies", "slot": "create", "srcId": SPECIES_SRC, "name": SPECIES, "data": {
        "name": SPECIES, "description": DESCRIPTION, "artDirection": art, "rankConcepts": concepts,
        "rarity": "LEGENDARY", "role": "ASSAULT", "preferredDamageElement": None,
        "isActive": False,  # reward-only; activation is never needed for a jar grant
        "hidden": True,     # law 16b; species have no hidden column, Forge strips it
        "defaultJutsuIds": [], "aiRules": [], "includeDefaultRules": True,
        "effects": [rot_bite(), hungry()]}}


# ---------------------------------------------------------------------------------------------------------------
# Signature jutsu
# ---------------------------------------------------------------------------------------------------------------
JUTSU_DROP = ("id", "createdAt", "updatedAt", "bloodline")  # read-only columns and the join


def resolve_refs(x):
    return x  # effects carry no @refs


def little_maw():
    rally = copy.deepcopy(next(j for j in JUTSU_CAP if j["name"] == "Rallying Echo"))
    data = {k: v for k, v in rally.items() if k not in JUTSU_DROP}
    dmg = copy.deepcopy(rally["effects"][0])
    assert dmg["type"] == "damage" and dmg["generalTypes"] == ["Highest"] and "statTypes" not in dmg
    dmg.update({"power": 50, "calculation": "formula", "description": "Deals damage to target"})
    if not PUBLISHABLE:
        dmg.update({"appearAnimation": "", "appearSfx": ""})  # as push/346 created it: maw strip not uploaded
    taken = {"type": "increasedamagetaken", "power": 10, "rounds": 1, "target": "INHERIT", "direction": "offence",
             "calculation": "percentage", "description": "Increase damage taken of target", "powerPerLevel": 0,
             "appearSfx": "", "disappearSfx": "", "appearAnimation": "", "staticAnimation": "", "staticAssetPath": "",
             "disappearAnimation": ""}
    data.update({"name": JUTSU, "description": MAW_DESCRIPTION, "battleDescription": MAW_BATTLE,
                 "requiredPetSpeciesId": "@petSpecies:" + SPECIES_SRC, "jutsuRank": "D",
                 "requiredRank": "STUDENT", "requiredLevel": 1, "target": "OPPONENT", "method": "SINGLE",
                 "range": 4, "cooldown": 5, "actionCostPerc": 60, "healthCost": 0, "chakraCost": 0, "staminaCost": 0,
                 "image": PLACEHOLDER, "hidden": True, "effects": [dmg, taken]})
    assert data["jutsuType"] == "PETS" and data["jutsuWeapon"] == "NONE" and data["elementClassification"] == "None"
    return {"entity": "jutsu", "slot": "create", "srcId": JUTSU_SRC, "name": JUTSU, "data": data}


# ---------------------------------------------------------------------------------------------------------------
# The jar
# ---------------------------------------------------------------------------------------------------------------
def jar():
    eff = IT.fixed("The Little Horror's Jar: binds the Little Horror to you as a pet")
    eff["reward_pets"] = ["@petSpecies:" + SPECIES_SRC]
    assert "rewardMode" not in eff  # standard rewards (a weightedCache refuses pet grants)
    e = IT.create(JAR_SRC, JAR, T.block(f"item:{JAR}.description"), "LEGENDARY", "CONSUMABLE", False, [eff],
                  battle="Companion jar")
    d = e["data"]
    assert d["preventBattleUsage"] is True and d["canBeTraded"] is False and d["hidden"] is True
    assert d["image"] == PLACEHOLDER
    return e


# ---------------------------------------------------------------------------------------------------------------
# 347: defaults, from 346's results
# ---------------------------------------------------------------------------------------------------------------
def defaults_edit(bundle):
    idmap = json.load(open(bundle)).get("idmap") or {}
    missing = [s for s in (SPECIES_SRC, JUTSU_SRC) if not idmap.get(s)]
    if missing:
        raise SystemExit(f"{', '.join(missing)} missing from {os.path.basename(bundle)}'s idmap: is it push/{NUM}'s results?")
    return {"entity": "petSpecies", "slot": "edit", "targetId": idmap[SPECIES_SRC],
            "name": f"{SPECIES}: default loadout = {JUTSU}",
            "data": {"rarity": "LEGENDARY", "defaultJutsuIds": [idmap[JUTSU_SRC]]}}


# ---------------------------------------------------------------------------------------------------------------
def placeholders(items):
    out = IT.placeholders(items)
    out.append(f"jutsu {JUTSU_SRC}: {JUTSU} damage appearAnimation empty (the Core Horror's maw strip is not uploaded)")
    out.append(f"petSpecies {SPECIES_SRC}: {SPECIES} has no art yet (artDirection/rankConcepts drive generation)")
    return out


def write(path, note, items, extra=None):
    m = {"_note": note + " Generated by push/skyglass_pet.gen.py; do not hand-edit.", "dedupNames": True}
    if extra:
        m.update(extra)
    m["items"] = items
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    shown = os.path.relpath(path, ROOT) if os.path.abspath(path).startswith(ROOT + os.sep) else path
    print(f"{shown}: {len(items)} items")


PUBLISH_NUM = 353
# The server publishes a jutsu only if one effect has both appearAnimation and appearSfx (push/353 first run refused:
# "At least one effect must have both appearAnimation and appearSfx defined"). Until the maw strip is uploaded, Little
# Maw's damage keeps Rallying Echo's live animation and sound (copied from the 345 capture; placeholder, swapped by the
# visual-asset push). push/346 itself ran with both empty.
PUBLISHABLE = False


def main():
    a = sys.argv[1:]
    if a[:1] == ["--publish"] and len(a) == 2:
        # Director 2026-10-31: publish Little Maw by a Forge edit (hidden false) so push/347 can set it as a default
        # (the server refuses an unpublished default). The species and Jar stay hidden; nobody can learn or use the
        # jutsu without the species (requiredPetSpeciesId).
        idmap = json.load(open(a[1])).get("idmap") or {}
        jid = idmap[PFX + "little_maw"]
        global PUBLISHABLE
        PUBLISHABLE = True
        effects = resolve_refs(little_maw()["data"]["effects"])
        assert effects[0]["type"] == "damage" and effects[0]["appearAnimation"] and effects[0]["appearSfx"]
        item = {"entity": "jutsu", "slot": "edit", "targetId": jid, "name": JUTSU,
                "data": {"hidden": False, "injectableInBattle": False,  # law 20: sent explicitly, as 346 created it
                         "effects": effects}}
        return write(os.path.join(ROOT, f"push/{PUBLISH_NUM}_skyglass_little_maw_publish.json"), (
            f"push/{PUBLISH_NUM} (after push/{NUM}, from {os.path.basename(a[1])}): publishes {JUTSU} ({jid}) so "
            f"push/{DEFAULTS_NUM} can set it as the Little Horror's default. Species and Jar stay hidden."), [item])
    if a[:1] == ["--defaults"] and len(a) in (2, 4):
        bundle = a[1]
        out = os.path.join(ROOT, f"push/{DEFAULTS_NUM}_skyglass_pet_defaults.json")
        if len(a) == 4:
            if a[2] != "--out":
                raise SystemExit(__doc__)
            out = a[3]
        return write(out, (
            f"push/{DEFAULTS_NUM} (after push/{NUM}, from its results bundle {os.path.basename(bundle)}; literal ids, "
            f"L01). RUN ONLY AFTER the director has PUBLISHED {JUTSU} (hidden:false): the server refuses an unpublished "
            f"default. Sets the {SPECIES}'s default loadout to [{JUTSU}]. The species stays isActive:false."),
            [defaults_edit(bundle)])
    if a:
        raise SystemExit(__doc__)
    body = [species(), little_maw(), jar()]
    write(os.path.join(ROOT, f"push/{NUM}_skyglass_pet.json"), (
        f"push/{NUM}, HIDDEN, placeholder art (list in _placeholders). RUL-2026-10-31-068. Three creates in build order: "
        f"the {SPECIES} species (Legendary Assault, isActive:false, innates Rot Bite = enemies deal 10% less damage "
        f"(30 rounds) and Hungry = +20% damage given), its signature PETS jutsu {JUTSU} (requiredPetSpeciesId -> the species; "
        f"D rank, 60 AP, damage 50 + 10% damage taken for 1 round), and {JAR} (untradeable Legendary consumable granting "
        f"the species). After it runs: record the three ids; the director publishes {JUTSU}; then build push/"
        f"{DEFAULTS_NUM} with --defaults. The jar's id goes to the Wreck drops builder."),
        body, {"_placeholders": placeholders(body)})


if __name__ == "__main__":
    main()
