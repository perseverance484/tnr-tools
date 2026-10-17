/**
 * Ghost Ship / Skyglass active Consume — OFFLINE TEST CARRIERS.
 *
 * Approved rates (RUL-2026-10-11-005):
 *   Katana  = LEGENDARY WEAPON/SWORD, canBeImbued:false,
 *             pierce(power 50) + immunity(blocks buffprevent, rounds 2, SELF)
 *             + consume(power 15, percentage, SELF)
 *   Crystal = CRYSTAL, crystalTargetTypes WEAPON, consume(power 10, percentage) only.
 *
 * Both Consume durations are 3-round TEST INPUTS, not director-approved timing.
 * tools/build_item_carriers.py derives the new candidates. The frozen r4
 * Katana record and harness are unchanged. Katana keeps all RUL004 baseline
 * fields; its presentation uses placeholders. Crystal non-effect fields come
 * from the captured Flaming Sword shape donor and are NOT approved policy.
 */
import { ItemValidator, ItemValidatorRawSchema, getTagSchema } from "@/validators/combat";
import * as F from "./fixtures";

export const FLAMING_SWORD = {
  file: "harvests/inbox/tnr_results_1788235198666.json",
  pointer: "/captures/8/data/items/0/item",
};
export const flamingSword = () => F.captured(FLAMING_SWORD.file, FLAMING_SWORD.pointer);

/** Revised Katana effects with explicit, unapproved 3/3 test timing. */
export const KATANA_EFFECTS_INPUT = (): any[] => structuredClone(acceptedKatana().record.effects);
export const CRYSTAL_EFFECTS_INPUT = (): any[] => structuredClone(itemCarriers().crystal.record.effects);

/** The exact effects schema the item validator applies (ItemValidatorRawSchema.effects). */
export const itemEffectsSchema = ItemValidatorRawSchema.shape.effects;

export const parseItemEffects = (effects: unknown) => itemEffectsSchema.safeParse(effects);

/** Parse tags alone, for isolated schema controls only (not full item validity). */
export const parseTagsIndividually = (effects: any[]) =>
  effects.map((e) => getTagSchema(e.type).parse(e));

/** Full item validator (base + item + economy refinements). */
export const validateItem = (record: unknown) => ItemValidator.safeParse(record);

export const issues = (r: { success: boolean; error?: any }) =>
  r.success ? [] : r.error.issues.map((i: any) => ({ path: i.path.join("."), message: i.message }));

export const CARRIERS_PATH = "state/ghost_ship_skyglass_active_consume_carriers.json";
export const HISTORICAL_KATANA_PATH = "state/ghost_ship_skyglass_katana_record.json";
export const itemCarriers = () => F.loadJson(CARRIERS_PATH);
/** Legacy API name for consumers: this is a revised TEST CANDIDATE, not accepted timing. */
export const ACCEPTED_KATANA_PATH = CARRIERS_PATH;
export const acceptedKatana = () => itemCarriers().katana;
/** Presentation fields are pending acceptance; labelled placeholders fill them for validation/battle only. */
export const PRESENTATION_PLACEHOLDERS = {
  description: "harness placeholder (presentation pending)",
  battleDescription: "%user strikes %target (harness placeholder)",
  image: "",
};

/**
 * Revised Katana carrier: approved baseline/rate plus unapproved 3/3 timing,
 * effects in validator-parsed stored form,
 * presentation placeholders, and a harness row id. `overrides` exist only for
 * labelled control experiments (e.g. ALL-method aggregation).
 */
export const katanaRecord = (overrides: Record<string, unknown> = {}) => {
  const rec = structuredClone(acceptedKatana().record);
  const parsed = parseItemEffects(rec.effects);
  if (!parsed.success) throw new Error("Revised Katana carrier effects did not parse");
  return {
    ...rec,
    ...PRESENTATION_PLACEHOLDERS,
    id: "harness-skyglass-katana",
    effects: parsed.data,
    ...overrides,
  };
};

/**
 * Revised Crystal carrier. Active Consume alone is eligible for the new effects
 * schema; CONTRACT tests the full ItemValidator separately. Rarity and all other
 * non-effect fields are unapproved test inputs, not production defaults.
 */
export const crystalRecord = (rarity = "RARE", overrides: Record<string, unknown> = {}) => {
  const rec = structuredClone(itemCarriers().crystal.record);
  const parsed = parseItemEffects(rec.effects);
  if (!parsed.success) throw new Error("Revised Crystal carrier effects did not parse");
  return {
    ...rec,
    id: "harness-skyglass-crystal",
    rarity,
    effects: parsed.data,
    ...overrides,
  };
};

/** Imbuable WEAPON recipient: Flaming Sword carrier with canBeImbued flipped to true. */
export const imbuableWeapon = (overrides: Record<string, unknown> = {}) => ({
  ...flamingSword().record,
  id: "harness-imbuable-sword",
  name: "Flaming Sword (canBeImbued:true carrier)",
  canBeImbued: true,
  ...overrides,
});

export const userItemRow = (userId: string, item: any, extra: Record<string, unknown> = {}) => ({
  id: `ui-${item.id}-${userId}`,
  userId,
  itemId: item.id,
  quantity: 1,
  level: 1,
  experience: 0,
  equipped: "HAND_1",
  durability: 100,
  storedAtHome: false,
  craftingFinishedAt: null,
  isInAuction: false,
  activeVariantId: null,
  dropChancePerc: 0,
  createdAt: new Date(0),
  updatedAt: new Date(0),
  item,
  imbuements: [],
  ...extra,
});

export const imbuementRow = (userItemId: string, crystal: any) => ({
  id: `imb-${crystal.id}-${userItemId}`,
  userItemId,
  imbuementItemId: crystal.id,
  craftingFinishedAt: new Date(0),
  item: crystal,
});
