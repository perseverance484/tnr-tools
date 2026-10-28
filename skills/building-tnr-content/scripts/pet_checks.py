"""Pet species and PETS jutsu checks for validate.py (RUL-2026-10-28-012).

Field sets, enums, required keys and the PET_* constants are read from the generated contracts
(45d petSpecies, 45g, 45e), extracted from studie-tech/TheNinjaRPG@2af4b32066c39e2868efae5dba6b339278701dca.
The rules below that no schema expresses are read at that pin and cited per rule:

  validators/petSpecies.ts:20-95   PetSpeciesValidator refinements: innate effects refuse barrier and
                                   move, SuperRefinePassiveEffects refuses COORDINATES, defaults are
                                   unique and fit PET_ABILITY_SLOTS_BY_RARITY[rarity]
  validators/pets.ts:110-157       aiRules actions limited to PET_AI_ACTION_TYPES, a highest-power
                                   action's effect to PET_AI_EFFECT_TYPES
  routers/petSpecies.ts:56-67,113-125  defaults must be published, compatible PETS jutsu; a create
                                   refuses species-locked ones, an edit accepts only its own
  libs/pets/abilities.ts:33-95,231-238  isPetJutsuAllowed / isAllowedEffect: what a pet can equip.
                                   The game SAVES a PETS jutsu that fails it and never lets a pet use
                                   it, so a failure here is an error even though the push would echo ok
  routers/jutsu.ts:1153-1157       requiredPetSpeciesId needs jutsuType PETS and an existing species
  validators/combat.ts:867-893,1547-1559  reward_pets: item noncombatconsumereward only, at most
                                   PET_MAX_CONSUME_PETS per item, standard rewardMode, and the item
                                   must prevent battle usage

Forge mirrors the same rules in forge/src/runner/pets.mjs and lints.mjs; the activeEffects list and
the mastery/link keys are hand-held in both places because they live in libs/, not in a validator.
"""
import re

ID_LEN = 21
REF = re.compile(r"^@(jutsu|petSpecies):[A-Za-z0-9_\-]+$")
PET_JUTSU_EFFECTS = ("damage", "elementaldamage", "heal", "shield", "increasestat", "decreasestat",
                     "increasedamagegiven", "decreasedamagegiven", "increasedamagetaken",
                     "decreasedamagetaken", "clear", "cleanse", "move")
MASTERIES = ("requiredNinjutsuMastery", "requiredGenjutsuMastery", "requiredTaijutsuMastery",
             "requiredBukijutsuMastery", "requiredBloodlineMastery", "requiredSageMastery")
LINKS = ("bloodlineId", "bloodlineReskinId", "reskinParentJutsuId", "villageId", "requiredSkillId",
         "requiredBloodlineItemId")
NON_NEGATIVE = ("healthCost", "chakraCost", "staminaCost", "healthCostReducePerLvl",
                "chakraCostReducePerLvl", "staminaCostReducePerLvl", "range", "cooldown")


def _const(consts, name):
    e = (consts or {}).get(name) or {}
    return e.get("value")


def _record(consts, name):
    """`{ COMMON: 2, ... }` Record constants are kept as raw text in 45e."""
    raw = ((consts or {}).get(name) or {}).get("raw") or ""
    return {k: int(v) for k, v in re.findall(r"([A-Z_]+)\s*:\s*(\d+)", raw)}


def _id_ok(v):
    return isinstance(v, str) and (len(v) == ID_LEN or bool(REF.match(v)))


def check_species(entry, items, fields, checks, consts, rep, where):
    data = entry.get("data") or {}
    slot = entry.get("slot")
    create = slot == "create"
    if not fields:
        rep.err(where, "45d has no petSpecies entity: regenerate the contracts at the pin before building species")
        return
    if consts is None:
        rep.err(where, "45e_DATA_constants.json not loaded: the pet species checks need its PET_* constants")
        return
    for k in data:
        if k not in fields and k != "hidden":
            rep.err(where, f"unknown key '{k}' for petSpecies (the server drops it silently). Valid: {', '.join(sorted(fields))}")
    if "hidden" in data and data["hidden"] is not True:
        rep.err(where, "petSpecies has no hidden column: a create carries hidden:true (law 16b, stripped) and isActive:false")
    if create:
        for k in (checks.get("required_on_create") or {}).get("fields", {}).get("petSpecies", []):
            if k not in data:
                rep.err(where, f"petSpecies create missing required '{k}'")
        if data.get("isActive") is not False:
            rep.err(where, "isActive must be false on create: an active species is offered to players at once. "
                           "Activating it is a publishing step for the director")
    for k, allowed in ((checks.get("enums") or {}).get("fields", {}).get("petSpecies") or {}).items():
        v = data.get(k)
        if v is not None and v not in allowed:
            rep.err(where, f"{k}={v!r} not in {allowed}")
    for k in ("name", "description", "artDirection"):
        v, spec = data.get(k), fields.get(k) or {}
        if v is None:
            continue
        if not isinstance(v, str):
            rep.err(where, f"{k} must be a string")
            continue
        if spec.get("min") and len(v.strip()) < spec["min"]:
            rep.err(where, f"{k} is empty")
        if spec.get("max") and len(v.strip()) > spec["max"]:
            rep.err(where, f"{k} is {len(v.strip())} characters; the limit is {spec['max']}")
    rc = data.get("rankConcepts")
    if rc is not None:
        ranks = len(re.findall(r"\brank\s*:", (consts.get("PET_RANKS") or {}).get("raw") or ""))
        if not isinstance(rc, list) or not all(isinstance(x, str) and len(x) <= 1000 for x in rc):
            rep.err(where, "rankConcepts is a list of strings of at most 1000 characters")
        elif ranks and len(rc) > ranks:
            rep.err(where, f"rankConcepts has {len(rc)} entries; there are {ranks} pet ranks")
    ids = data.get("defaultJutsuIds")
    if ids is not None:
        slots = _record(consts, "PET_ABILITY_SLOTS_BY_RARITY")
        if not isinstance(ids, list):
            rep.err(where, "defaultJutsuIds must be a list")
        else:
            if len(set(ids)) != len(ids):
                rep.err(where, "defaultJutsuIds: choose each default pet jutsu only once")
            r = data.get("rarity")
            if r in slots and len(ids) > slots[r]:
                rep.err(where, f"defaultJutsuIds: {len(ids)} defaults exceed the {slots[r]} slots of a {r} species")
            elif r is None and ids:
                rep.note(where, "defaultJutsuIds checked against the live rarity's slots by the server and Forge (rarity not in this edit)")
            for v in ids:
                if not _id_ok(v):
                    rep.err(where, f"defaultJutsuIds entry {v!r} is neither a {ID_LEN}-char id nor an @jutsu ref")
            if ids and slot != "create":
                rep.note(where, "every default must be a PUBLISHED PETS jutsu (hidden:false) when this runs; "
                                "the server refuses the save otherwise")
            _defaults_in_manifest(entry, ids, items, rep, where)
    for i, f in enumerate(data.get("effects") or []):
        if not isinstance(f, dict):
            continue
        if f.get("type") in ("barrier", "move"):
            rep.err(f"{where}.effects[{i}]", f"{f['type']} needs an empty-ground action; an innate skill cannot carry it")
        if f.get("target") == "COORDINATES":
            rep.err(f"{where}.effects[{i}]", "an innate skill cannot target COORDINATES")
    acts = _const(consts, "PET_AI_ACTION_TYPES") or []
    effs = _const(consts, "PET_AI_EFFECT_TYPES") or []
    for i, r in enumerate(data.get("aiRules") or []):
        a = (r or {}).get("action") if isinstance(r, dict) else None
        if not isinstance(a, dict):
            continue
        if acts and a.get("type") not in acts:
            rep.err(f"{where}.aiRules[{i}]", f"pet AI action {a.get('type')!r} not in {acts}")
        if a.get("type") == "use_highest_power_action" and effs and a.get("effect") not in effs:
            rep.err(f"{where}.aiRules[{i}]", f"highest-power effect {a.get('effect')!r} not available to pets ({effs})")


def _defaults_in_manifest(entry, ids, items, rep, where):
    by_src = {e.get("srcId"): e for e in items if e.get("entity") == "jutsu" and e.get("srcId")}
    for ref in ids:
        if not (isinstance(ref, str) and ref.startswith("@jutsu:")):
            continue
        j = by_src.get(ref[7:])
        if not j:
            continue
        if j.get("slot") == "create":
            rep.err(where, f"default {ref} is created hidden in this manifest; the server refuses unpublished "
                           "defaults. Publish it, then set the defaults in a later manifest")
        lock = (j.get("data") or {}).get("requiredPetSpeciesId")
        if lock and entry.get("slot") == "create":
            rep.err(where, f"default {ref} is species-locked; a species create accepts only unlocked PETS jutsu")
        # a ref names a species by srcId, the edit by literal id: only two literal ids compare offline
        if lock and entry.get("slot") != "create" and not str(lock).startswith("@") and lock != entry.get("targetId"):
            rep.err(where, f"default {ref} is locked to another species ({lock})")


def check_jutsu(entry, rep, where):
    """isPetJutsuAllowed over the asserted keys (minus `hidden`). Keys an edit does not carry are the
    live record's; a create fills the rest from jutsu.create's placeholder (jutsuType AI, effects [],
    weapon NONE, element None), so a create must carry jutsuType PETS and its effects."""
    d = entry.get("data") or {}
    lock = d.get("requiredPetSpeciesId")
    create = entry.get("slot") == "create"
    if lock is not None and lock != "" and not _id_ok(lock):
        rep.err(where, f"requiredPetSpeciesId {lock!r} is neither a {ID_LEN}-char species id nor an @petSpecies ref")
    if lock and "jutsuType" in d and d["jutsuType"] != "PETS":
        rep.err(where, "requiredPetSpeciesId needs jutsuType PETS (routers/jutsu.ts refuses the save)")
    if lock and create and d.get("jutsuType") != "PETS":
        rep.err(where, "a species-locked jutsu create must carry jutsuType PETS")
    if d.get("jutsuType") != "PETS":
        return
    bad = lambda m: rep.err(where, "PETS jutsu a pet could never equip (isPetJutsuAllowed): " + m)
    if d.get("injectableInBattle") is True:
        bad("injectableInBattle must be false")
    if d.get("battleUsageType") == "PVP":
        bad("battleUsageType PVP")
    if d.get("jutsuRank") == "H":
        bad("H rank")
    for k in LINKS + MASTERIES:
        if d.get(k):
            bad(f"{k} must be empty")
    if "jutsuWeapon" in d and d["jutsuWeapon"] != "NONE":
        bad("jutsuWeapon must be NONE")
    if d.get("elementClassification") not in (None, "", "None"):
        bad("elementClassification must be None")
    for k in NON_NEGATIVE:
        v = d.get(k)
        if v is not None and not (isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0):
            bad(f"{k} must be a number >= 0")
    ap = d.get("actionCostPerc")
    if ap is not None and not (isinstance(ap, (int, float)) and 10 <= ap <= 100):
        bad("actionCostPerc must be 10-100")
    effects = d.get("effects")
    if create and not effects:
        bad("it has no effects (the placeholder's are empty)")
    for i, f in enumerate(effects or []):
        if not isinstance(f, dict):
            continue
        if f.get("type") not in PET_JUTSU_EFFECTS:
            bad(f"effects[{i}] {f.get('type')!r} is not a pet effect ({', '.join(PET_JUTSU_EFFECTS)})")
            continue
        for k in ("power", "powerPerLevel"):
            v = f.get(k)
            if isinstance(v, (int, float)) and v < 0:
                bad(f"effects[{i}].{k} must be >= 0")
        if f.get("calculation") == "percentage" and isinstance(f.get("power"), (int, float)) and f["power"] > 100:
            bad(f"effects[{i}] percentage power above 100")
        if any(e != "None" for e in f.get("elements") or []):
            bad(f"effects[{i}] carries elements")
    if create and d.get("hidden") is True:
        rep.note(where, "PETS jutsu ships hidden: no pet can equip it, and no species can take it as a "
                        "default, until the director publishes it")


def check_rewards(entry, consts, rep, where):
    """reward_pets / reward_pet_experience on items and quests."""
    d = entry.get("data") or {}
    ent = entry.get("entity")
    if ent == "quest":
        content = d.get("content") or {}
        for node in [content.get("reward") or {}] + list(content.get("objectives") or []):
            if isinstance(node, dict) and "reward_pets" in node:
                rep.err(where, "reward_pets is not a quest reward (QuestReward/ObjectiveReward lack it); "
                               "grant a pet by rewarding an item whose noncombatconsumereward carries it")
            v = node.get("reward_pet_experience") if isinstance(node, dict) else None
            if v is not None and not (isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0):
                rep.err(where, "reward_pet_experience must be a number >= 0")
        return
    if ent != "item":
        return
    cap = _const(consts, "PET_MAX_CONSUME_PETS") or 1
    pets = 0
    for i, f in enumerate(d.get("effects") or []):
        if not isinstance(f, dict) or f.get("type") != "noncombatconsumereward":
            continue
        rp = f.get("reward_pets") or []
        pets += len(rp) if isinstance(rp, list) else 0
        for v in rp if isinstance(rp, list) else []:
            if not _id_ok(v):
                rep.err(f"{where}.effects[{i}]", f"reward_pets entry {v!r} is neither a {ID_LEN}-char species id nor an @petSpecies ref")
        if rp and f.get("rewardMode") == "weightedCache":
            rep.err(f"{where}.effects[{i}]", "pet grants require standard rewards (rewardMode weightedCache refuses reward_pets)")
        v = f.get("reward_pet_experience")
        if v is not None and not (isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0):
            rep.err(f"{where}.effects[{i}]", "reward_pet_experience must be a number >= 0")
    if pets > cap:
        rep.err(where, f"an item may grant at most {cap} companion ({pets} in reward_pets)")
    if pets:
        if d.get("preventBattleUsage") is False or (entry.get("slot") == "create" and d.get("preventBattleUsage") is not True):
            rep.err(where, "companion rewards must prevent battle usage: set preventBattleUsage true")
        elif "preventBattleUsage" not in d:
            rep.note(where, "reward_pets needs preventBattleUsage true on the live item (not asserted in this edit)")
