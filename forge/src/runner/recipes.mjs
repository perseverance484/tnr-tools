// Per-entity write recipes. Every path and input shape below was read at source
// (studie-tech/TheNinjaRPG@345d18ac, app/src/server/api/routers/*), not from the old bundle.
//
// All six creates are two-phase: create takes no payload (item.create takes {type}), inserts
// a placeholder row and returns the id in baseServerResponse.message; the record is not
// correct until update lands. Every update is {id, data: <EntityValidator>}. The get for
// read-back returns the DB row, which matches neither input shape, so the merge PICKS the
// validator's field set (45d) from live ∪ asserted and drops everything else (relations,
// server-owned columns).

export const RECIPES = Object.freeze({
  jutsu: {
    create: { path: "jutsu.create", input: () => undefined },      // jutsu.ts:391
    get: "jutsu.get", update: "jutsu.update", names: "jutsu.getAllNames",
    idKey: "id", nameKey: "name", placeholder: (id) => `New Jutsu - ${id}`, cacheEntity: "jutsu",
  },
  item: {
    create: { path: "item.create", input: (d) => ({ type: d.itemType ?? "CONSUMABLE" }) }, // item.ts:235-236
    get: "item.get", update: "item.update", names: "item.getAllNames",
    idKey: "id", nameKey: "name", placeholder: (id) => `New Item - ${id}`, cacheEntity: "item",
  },
  bloodline: {
    create: { path: "bloodline.create", input: () => undefined },  // bloodline.ts:144
    get: "bloodline.get", update: "bloodline.update", names: "bloodline.getAllNames",
    idKey: "id", nameKey: "name", placeholder: (id) => `New Bloodline - ${id}`, cacheEntity: "bloodline",
  },
  asset: {
    create: { path: "gameAsset.create", input: () => undefined },  // asset.ts:194
    get: "gameAsset.get", update: "gameAsset.update", names: "gameAsset.getAllNames",
    idKey: "id", nameKey: "name", placeholder: () => "Placeholder", cacheEntity: "asset",
    placeholderIsAnonymous: true, // every orphan is named "Placeholder": the snapshot diff is the only signal
  },
  quest: {
    create: { path: "quests.create", input: () => undefined },     // quests.ts:866
    get: "quests.get", update: "quests.update", names: "quests.getAllNames",
    idKey: "id", nameKey: "name", placeholder: (id) => `New Quest - ${id}`, cacheEntity: "quest",
  },
  ai: {
    create: { path: "profile.create", input: () => undefined },    // profile.ts:1138
    get: "profile.getAi", update: "profile.updateAi", names: "profile.getAllAiNames",
    idKey: "userId", nameKey: "username", placeholder: (id) => `New AI - ${id}`, cacheEntity: "ai",
  },
  aiProfile: {
    // update-only. targetId is the AI's userId. Rules live on a separate row reached through
    // profile.getAi().aiProfileId; ai.toggleAiProfile {aiId} creates that row when missing.
    get: "profile.getAi", names: "profile.getAllAiNames",
    idKey: "userId", nameKey: "username", cacheEntity: "ai",
    profileGet: "ai.getAiProfile", profileUpdate: "ai.updateAiProfile", profileToggle: "ai.toggleAiProfile",
  },
});

export function recipe(entity) {
  const r = RECIPES[entity];
  if (!r) throw new Error("no recipe for entity " + entity);
  return r;
}

/**
 * Build the update payload: pick the validator's fields from live ∪ asserted.
 * @param {string} entity
 * @param {object|null} live   the get() row (may be null if the read failed)
 * @param {object} data        asserted keys, refs resolved
 * @param {Set<string>|null} fields  45d field set for the entity; null for ai
 */
export function mergeForUpdate(entity, live, data, fields) {
  if (entity === "ai") return mergeAi(live, data);
  const src = { ...(live ?? {}), ...data };
  if (!fields) return src;
  const out = {};
  for (const k of fields) if (src[k] !== undefined) out[k] = src[k];
  return out;
}

// insertAiSchema = createInsertSchema(userData).omit({...}).extend({jutsus, items, ...}).
// profile.getAi returns the row with relation arrays jutsus: [{jutsuId, jutsu:{...}}] and
// items: [{itemId, quantity, ...}] (profile.ts:1121-1137; userJutsu at schema.ts:3010,
// userItem at :2802). updateAi (profile.ts:1529-1541) syncs by set difference against
// input.data.jutsus ?? [] and the ids inside input.data.items, so OMITTING them deletes the
// whole kit (law 70). The live kit is therefore always re-sent unless the manifest asserts it.
const AI_OMIT = new Set([
  // omitted from insertAiSchema at schema.ts:2578-2591
  "trainingStartedAt", "occupationSignupAt", "currentlyTraining", "deletionAt", "travelFinishAt",
  "questData", "occupation", "stealthActivatedAt", "stealthCooldownAt", "lastSensoryAt",
  "covertTrainingType", "covertTrainingStartedAt", "covertTrainingMinutes",
  // relation objects and routing keys that are not columns
  "rules", "includeDefaultRules",
]);
export function mergeAi(live, data) {
  const out = {};
  if (live) for (const [k, v] of Object.entries(live)) if (!AI_OMIT.has(k)) out[k] = v;
  if (live && Array.isArray(live.jutsus)) out.jutsus = live.jutsus.map((r) => (typeof r === "string" ? r : r.jutsuId ?? r.id)).filter(Boolean);
  if (live && Array.isArray(live.items)) {
    out.items = live.items.map((r) => (typeof r === "string" ? { ids: [r], number: 1 }
      : r && Array.isArray(r.ids) ? r
      : r ? { ids: [r.itemId ?? r.id].filter(Boolean), number: r.number ?? r.quantity ?? 1 } : null)).filter((x) => x && x.ids.length);
  }
  for (const [k, v] of Object.entries(data)) if (!["rules", "includeDefaultRules"].includes(k)) out[k] = v;
  if (Array.isArray(out.jutsus)) out.jutsus = out.jutsus.map((j) => (typeof j === "string" ? j : j && (j.jutsuId || j.id))).filter(Boolean);
  if (Array.isArray(out.items)) out.items = out.items.map((t) => (typeof t === "string" ? { ids: [t], number: 1 }
    : t && Array.isArray(t.ids) ? t : t ? { ids: [t.itemId || t.id].filter(Boolean), number: t.number ?? t.quantity ?? 1 } : null)).filter((x) => x && x.ids.length);
  out.isAi = true;
  if (out.userId == null && live && live.userId) out.userId = live.userId;
  return out;
}
