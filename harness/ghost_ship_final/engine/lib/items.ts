/**
 * Ghost Ship / Skyglass FINAL 2/2 item candidates (RUL-2026-10-11-006).
 *
 *   Katana  = LEGENDARY WEAPON/SWORD, canBeImbued:false, Night's Testament baseline,
 *             pierce(50, Crystal) + immunity(buffprevent, rounds 2, SELF)
 *             + consume(15%, SELF, rounds 2, shieldRounds 2)
 *   Crystal = CRYSTAL, WEAPON-only, LEGENDARY, canBeTraded:true, canBeCrafted:false,
 *             no recipe, exactly consume(10%, SELF, rounds 2, shieldRounds 2).
 *
 * tools/build_final_items.py derives both records. Crystal fields no ruling
 * decides are labelled unapproved carrier values in the record packet;
 * presentation fields are pending and filled with labelled placeholders here.
 * The r4 Katana record and the 3/3 carrier packet are historical and unchanged.
 */
import { ItemValidator, ItemValidatorRawSchema, getTagSchema } from "@/validators/combat";
import * as F from "./fixtures";

export const FLAMING_SWORD = {
  file: "harvests/inbox/tnr_results_1788235198666.json",
  pointer: "/captures/8/data/items/0/item",
};
export const flamingSword = () => F.captured(FLAMING_SWORD.file, FLAMING_SWORD.pointer);

/** Final Katana / Crystal effect arrays (approved 2/2 timing). */
export const KATANA_EFFECTS_INPUT = (): any[] => structuredClone(acceptedKatana().record.effects);
export const CRYSTAL_EFFECTS_INPUT = (): any[] => structuredClone(finalRecords().crystal.record.effects);

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

export const RECORDS_PATH = "state/ghost_ship_skyglass_final_item_records.json";
export const CONTRACT_PATH = "state/ghost_ship_skyglass_final_item_contract.json";
export const HISTORICAL_KATANA_PATH = "state/ghost_ship_skyglass_katana_record.json";
export const HISTORICAL_3X3_PATH = "state/ghost_ship_skyglass_active_consume_carriers.json";
export const finalRecords = () => F.loadJson(RECORDS_PATH);
export const acceptedKatana = () => finalRecords().katana;
/** Presentation fields are pending acceptance; labelled placeholders fill them for validation/battle only. */
export const PRESENTATION_PLACEHOLDERS = {
  description: "harness placeholder (presentation pending)",
  battleDescription: "%user strikes %target (harness placeholder)",
  image: "",
};

/**
 * Final Katana candidate: approved baseline, rate and 2/2 timing,
 * effects in validator-parsed stored form,
 * presentation placeholders, and a harness row id. `overrides` exist only for
 * labelled control experiments (e.g. ALL-method aggregation).
 */
export const katanaRecord = (overrides: Record<string, unknown> = {}) => {
  const rec = structuredClone(acceptedKatana().record);
  const parsed = parseItemEffects(rec.effects);
  if (!parsed.success) throw new Error("Final Katana effects did not parse");
  return {
    ...rec,
    ...PRESENTATION_PLACEHOLDERS,
    id: "harness-skyglass-katana",
    effects: parsed.data,
    ...overrides,
  };
};

/**
 * Final Crystal candidate (LEGENDARY by RUL006). `rarity` other than LEGENDARY is
 * only for labelled native rank-matrix controls. Unapproved carrier fields stay
 * as recorded in the packet; presentation uses labelled placeholders.
 */
export const crystalRecord = (rarity = "LEGENDARY", overrides: Record<string, unknown> = {}) => {
  const rec = structuredClone(finalRecords().crystal.record);
  const parsed = parseItemEffects(rec.effects);
  if (!parsed.success) throw new Error("Final Crystal effects did not parse");
  return {
    ...rec,
    ...PRESENTATION_PLACEHOLDERS,
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
