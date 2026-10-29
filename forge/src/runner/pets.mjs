// Pet species and PETS jutsu: the server-side rules a key-set check cannot see, read at
// studie-tech/TheNinjaRPG@2af4b32066c39e2868efae5dba6b339278701dca (RUL-2026-10-28-012).
//
//   validators/petSpecies.ts:20-95  PetSpeciesValidator: effects refuse barrier/move and (via
//                                   SuperRefinePassiveEffects) COORDINATES targets; defaults are
//                                   unique and fit PET_ABILITY_SLOTS_BY_RARITY[rarity].
//   routers/petSpecies.ts:38-154    create answers {success, message: <new id>}; update takes
//                                   {id, data} and re-saves the WHOLE parsed record, so an edit is
//                                   a fetch-merge like every other entity. Defaults must be
//                                   published, compatible PETS jutsu (isPetJutsuAllowed); a create
//                                   refuses species-locked defaults, an edit accepts only jutsu
//                                   locked to that species.
//   libs/pets/abilities.ts:33-95    isPetJutsuAllowed: what a pet can equip at all. The game SAVES
//                                   a PETS jutsu that fails it and then never lets a pet use it, so
//                                   a create cannot be told apart from a working one by its echo.
//   routers/jutsu.ts:1153-1157      requiredPetSpeciesId needs jutsuType PETS and a real species.
//
// `hidden` is deliberately NOT part of the jutsu rule below. isPetJutsuAllowed requires a published
// jutsu, and every create ships hidden (law 16b), so a freshly created signature jutsu is correct
// and unusable until the director publishes it. The species edit that names it as a default is the
// step that needs it published; that is checked against the manifest by lints.mjs and, live, by the
// server's own refusal.
//
// Species carry no `hidden` column. A create carries hidden:true for law 16b like every entity and
// it is stripped before the send (the server's zod object would drop it anyway); the species'
// own visibility switch is isActive, which a create must leave false.

export const PET_SLOTS = Object.freeze({ COMMON: 2, UNCOMMON: 3, RARE: 4, EPIC: 5, LEGENDARY: 6 });
export const PET_STRIPPED_OK = Object.freeze(["hidden"]);
const ACTIVE_EFFECTS = new Set(["damage", "elementaldamage", "heal", "shield", "increasestat", "decreasestat",
  "increasedamagegiven", "decreasedamagegiven", "increasedamagetaken", "decreasedamagetaken", "clear", "cleanse", "move"]);
const MASTERIES = ["requiredNinjutsuMastery", "requiredGenjutsuMastery", "requiredTaijutsuMastery",
  "requiredBukijutsuMastery", "requiredBloodlineMastery", "requiredSageMastery"];
const LINKS = ["bloodlineId", "bloodlineReskinId", "reskinParentJutsuId", "villageId", "requiredSkillId", "requiredBloodlineItemId"];
const NON_NEGATIVE = ["healthCost", "chakraCost", "staminaCost", "healthCostReducePerLvl", "chakraCostReducePerLvl",
  "staminaCostReducePerLvl", "range", "cooldown"];

/**
 * A species record as PetSpeciesValidator stores it (validators/petSpecies.ts:22-48): name and
 * description trimmed; artDirection trimmed, and blank or null is null; each rank concept trimmed
 * with null/undefined as "", trailing blank concepts dropped. Only keys present are touched, and it
 * is idempotent, so the asserted payload and the stored row compare under one rule (read-back and
 * lost-create matching alike). Anything else that differs is still a difference.
 */
export function normalizeSpecies(d) {
  if (!d || typeof d !== "object") return d;
  const out = { ...d };
  for (const k of ["name", "description"]) if (typeof out[k] === "string") out[k] = out[k].trim();
  if ("artDirection" in out) out.artDirection = typeof out.artDirection === "string" ? out.artDirection.trim() || null : out.artDirection ?? null;
  if (Array.isArray(out.rankConcepts)) {
    const kept = out.rankConcepts.map((c) => (typeof c === "string" ? c.trim() : c ?? ""));
    while (kept.length && !kept[kept.length - 1]) kept.pop();
    out.rankConcepts = kept;
  }
  return out;
}

/** Strip the keys a species has no column for, so they are never sent or diffed. */
export function petSpeciesPayload(d) {
  const out = { ...d };
  for (const k of PET_STRIPPED_OK) delete out[k];
  return out;
}

/** The PetSpeciesValidator refinements and the create-time visibility rule. `live` is the stored row. */
export function petSpeciesProblems(data, live, { preCreate = false } = {}) {
  const out = [];
  if ("hidden" in data && data.hidden !== true) out.push("hidden: species have no hidden column; a create carries hidden:true (law 16b) and isActive:false");
  if (preCreate && data.isActive !== false) out.push("isActive must be false on create: an active species is offered to players at once (publishing is a separate step)");
  const ids = data.defaultJutsuIds;
  if (ids !== undefined) {
    if (!Array.isArray(ids)) out.push("defaultJutsuIds must be an array");
    else {
      if (new Set(ids).size !== ids.length) out.push("defaultJutsuIds: choose each default pet jutsu only once");
      const rarity = data.rarity ?? live?.rarity;
      if (PET_SLOTS[rarity] !== undefined && ids.length > PET_SLOTS[rarity]) out.push(`defaultJutsuIds: ${ids.length} defaults exceed the ${PET_SLOTS[rarity]} jutsu slots of a ${rarity} species`);
    }
  }
  for (const [i, f] of (Array.isArray(data.effects) ? data.effects : []).entries()) {
    if (f && (f.type === "barrier" || f.type === "move")) out.push(`effects[${i}]: ${f.type} needs an empty-ground action; an innate skill cannot carry it`);
    if (f && f.target === "COORDINATES") out.push(`effects[${i}]: an innate skill cannot target COORDINATES`);
  }
  return out;
}

/**
 * isPetJutsuAllowed (minus `hidden`) over what is known of the record: the asserted keys, over the
 * live row when there is one. A key that is in neither is not judged here. Returns [] for a jutsu
 * that is not a pet jutsu.
 */
export function petJutsuProblems(data, live = null) {
  const j = { ...(live ?? {}), ...data };
  const out = [];
  if (j.requiredPetSpeciesId && j.jutsuType !== "PETS") out.push("requiredPetSpeciesId needs jutsuType PETS (the server refuses it otherwise)");
  if (j.jutsuType !== "PETS") return out;
  const bad = (m) => out.push("PETS jutsu a pet could never equip: " + m);
  if (j.injectableInBattle === true) bad("injectableInBattle must be false");
  if (j.battleUsageType === "PVP") bad("battleUsageType PVP");
  if (j.jutsuRank === "H") bad("H rank");
  for (const k of LINKS) if (j[k]) bad(`${k} must be empty`);
  if (j.jutsuWeapon !== undefined && j.jutsuWeapon !== "NONE") bad("jutsuWeapon must be NONE");
  if (j.elementClassification && j.elementClassification !== "None") bad("elementClassification must be None");
  for (const k of MASTERIES) if (j[k]) bad(`${k} must be empty`);
  for (const k of NON_NEGATIVE) if (j[k] !== undefined && !(Number.isFinite(Number(j[k])) && Number(j[k]) >= 0)) bad(`${k} must be a finite number >= 0`);
  if (j.actionCostPerc !== undefined && !(Number(j.actionCostPerc) >= 10 && Number(j.actionCostPerc) <= 100)) bad("actionCostPerc must be 10-100");
  if (Array.isArray(j.effects)) {
    if (!j.effects.length) bad("it has no effects");
    for (const [i, f] of j.effects.entries()) {
      if (!f || typeof f !== "object") continue;
      if (!ACTIVE_EFFECTS.has(f.type)) { bad(`effects[${i}] ${f.type} is not a pet effect`); continue; }
      const p = f.power ?? 1, ppl = f.powerPerLevel ?? 0;
      if (!(Number(p) >= 0) || !(Number(ppl) >= 0)) bad(`effects[${i}] power and powerPerLevel must be >= 0`);
      if (f.calculation === "percentage" && Number(p) > 100) bad(`effects[${i}] percentage power above 100`);
      if (Array.isArray(f.elements) && f.elements.some((e) => e !== "None")) bad(`effects[${i}] carries elements`);
    }
  }
  return out;
}
