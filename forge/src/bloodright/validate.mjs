import CONTRACT from "./contract.json" with { type: "json" };
export { CONTRACT };
export const isBloodrightEntity = e => e === "skillTree" || e === "skillTreeFolder";
export const bloodrightFields = e => new Set(e === "skillTree" ? CONTRACT.skillFields : CONTRACT.folderFields);
const obj = v => v && typeof v === "object" && !Array.isArray(v);
const str = v => typeof v === "string";
const int = (v, min, max = Number.MAX_SAFE_INTEGER) => Number.isSafeInteger(v) && v >= min && v <= max;

// Narrow import surface, intentionally stricter than the general AllTags server union.
// Image may be omitted before create: the server placeholder supplies it, then fetch/merge
// preserves it. Existing edits are checked again against the complete merged row.
export function bloodrightProblems(entity, data, live = null, { preCreate = false } = {}) {
  if (!obj(data)) return ["data must be an object"];
  const out = [];
  const fields = bloodrightFields(entity);
  for (const k of Object.keys(data)) if (!fields.has(k)) out.push(`unknown key ${k} for ${entity}`);
  const d = { ...live, ...data };
  const check = (ok, message) => { if (!ok) out.push(message); };
  check(str(d.name) && !!d.name.trim() && d.name.length <= 191, "name must contain 1..191 characters");
  check(d.image === undefined || str(d.image) && d.image.length <= (entity === "skillTree" ? 191 : 512), "invalid image");
  check(d.description === undefined || str(d.description) || entity === "skillTreeFolder" && d.description === null, "description must be text");
  check(d.hidden === undefined || typeof d.hidden === "boolean", "hidden must be boolean");
  if (entity === "skillTreeFolder") {
    check(d.order === undefined || Number.isSafeInteger(d.order), "folder order must be an integer");
    return out;
  }
  check(d.pathType === "BLOODRIGHT" && str(d.bloodlineId) && !!d.bloodlineId && !d.bloodlineId.startsWith("@"), "requires a literal bloodlineId and pathType BLOODRIGHT");
  check(d.skillType === "DEFAULT", "Bloodright skillType must be DEFAULT");
  check(["SELF", "ENEMIES", "ALLIES"].includes(d.target), "invalid skill target");
  check(int(d.tier, 1, 10), "tier must be 1..10");
  check(int(d.costSkillPoints, 1), "costSkillPoints must be a positive integer");
  check(int(d.seichiSilverCost, 0, 2147483647), "explicit seichiSilverCost must be 0..2147483647");
  check(Array.isArray(d.requiredSkillIds) && d.requiredSkillIds.every(v => str(v) && !!v) && new Set(d.requiredSkillIds).size === d.requiredSkillIds.length, "invalid prerequisite IDs");
  check(d.folderId == null || str(d.folderId) && !!d.folderId, "invalid folderId");
  check(Array.isArray(d.effects), "effects must be an array");
  for (const [i, e] of (Array.isArray(d.effects) ? d.effects : []).entries()) {
    const where = `effects[${i}]`;
    if (!obj(e)) { out.push(`${where} must be an object`); continue; }
    for (const k of Object.keys(e)) if (!CONTRACT.effectFields.includes(k)) out.push(`${where}: unknown key ${k}`);
    check(["increasepotency", "decreasepotency"].includes(e.type), `${where}: only audited potency effects supported`);
    check(Number.isFinite(e.power) && e.power >= 0, `${where}: power must be nonnegative`);
    check(Number.isFinite(e.powerPerLevel) && e.powerPerLevel >= 0 && e.powerPerLevel <= 1, `${where}: powerPerLevel must be 0..1`);
    check(int(e.rounds, 1, 100), `${where}: explicit rounds must be 1..100`);
    check(["static", "percentage"].includes(e.calculation), `${where}: invalid calculation`);
    check(["SELF", "INHERIT"].includes(e.target), `${where}: invalid target`);
    check(e.direction === "offence", `${where}: direction must be offence`);
    check(e.friendlyFire === undefined || ["ALL", "FRIENDLY", "ENEMIES"].includes(e.friendlyFire), `${where}: invalid friendlyFire`);
    check(CONTRACT.tags.includes(e.affectedTag), `${where}: choose one supported affectedTag`);
    check(Array.isArray(e.affectedElements) && e.affectedElements.length > 0 && e.affectedElements.every(v => CONTRACT.elements.includes(v)), `${where}: resolve affectedElements explicitly`);
    for (const k of ["description", "staticAssetPath", "staticAnimation", "appearAnimation", "disappearAnimation", "appearSfx", "disappearSfx"]) check(str(e[k]), `${where}: ${k} must be text`);
    check(e.timeTracker === undefined, `${where}: runtime timeTracker is not importable`);
  }
  if (!preCreate && live) check(str(d.image) && !!d.image, "skill image must be preserved or supplied");
  return out;
}

export function writableSnapshot(entity, row) {
  const out = {};
  for (const key of bloodrightFields(entity)) if (row[key] !== undefined) out[key] = row[key];
  // The folder API accepts a string and writes empty descriptions as null.
  if (entity === "skillTreeFolder" && out.description == null) out.description = "";
  return out;
}
