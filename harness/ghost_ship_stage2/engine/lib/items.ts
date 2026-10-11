/**
 * Ghost Ship / Skyglass Stage 2 harness — item fixtures for gates B and C.
 *
 * Approved effect contracts (RUL-2026-10-10-007, state/ghost_ship_skyglass_reward_decisions.md):
 *   Katana  = LEGENDARY WEAPON/SWORD, canBeImbued:false,
 *             pierce(power 50) + immunity(blocks buffprevent, rounds 2, SELF)
 *             + consume(power 40, percentage, SELF)
 *   Crystal = CRYSTAL, crystalTargetTypes WEAPON, consume(power 20, percentage) only.
 *
 * Katana: the accepted record in state/ghost_ship_skyglass_katana_record.json
 * (RUL-2026-10-11-004: Night's Testament baseline from push/85, Pierce element
 * Crystal, drop-only, tradable), built by tools/build_katana_record.py.
 * Crystal and imbuable-recipient fixtures still take their non-effect fields
 * from the captured Flaming Sword row (harvests/inbox/tnr_results_1788235198666.json
 * #/captures/8/data/items/0/item, EPIC SWORD) as a labelled TEST CARRIER; Crystal
 * economy fields remain unselected.
 */
import { ItemValidator, ItemValidatorRawSchema, getTagSchema } from "@/validators/combat";
import * as F from "./fixtures";

export const FLAMING_SWORD = {
  file: "harvests/inbox/tnr_results_1788235198666.json",
  pointer: "/captures/8/data/items/0/item",
};
export const flamingSword = () => F.captured(FLAMING_SWORD.file, FLAMING_SWORD.pointer);

/** The accepted Katana's three effects exactly as committed (pre-parse input form). */
export const KATANA_EFFECTS_INPUT = (): any[] => structuredClone(acceptedKatana().record.effects);
export const CRYSTAL_EFFECTS_INPUT = () => [
  { type: "consume", power: 20, calculation: "percentage", target: "SELF" },
];

/** The exact effects schema the item validator applies (ItemValidatorRawSchema.effects). */
export const itemEffectsSchema = ItemValidatorRawSchema.shape.effects;

export const parseItemEffects = (effects: unknown) => itemEffectsSchema.safeParse(effects);

/** Parse each tag alone (no cross-tag refinement) — used only to build hypothetical records. */
export const parseTagsIndividually = (effects: any[]) =>
  effects.map((e) => getTagSchema(e.type).parse(e));

/** Full item validator (base + item + economy refinements). */
export const validateItem = (record: unknown) => ItemValidator.safeParse(record);

export const issues = (r: { success: boolean; error?: any }) =>
  r.success ? [] : r.error.issues.map((i: any) => ({ path: i.path.join("."), message: i.message }));

/** Accepted Katana record (RUL-2026-10-11-004): Night's Testament baseline + ruling overrides. */
export const ACCEPTED_KATANA_PATH = "state/ghost_ship_skyglass_katana_record.json";
export const acceptedKatana = () => F.loadJson(ACCEPTED_KATANA_PATH);
/** Presentation fields are pending acceptance; labelled placeholders fill them for validation/battle only. */
export const PRESENTATION_PLACEHOLDERS = {
  description: "harness placeholder (presentation pending)",
  battleDescription: "%user strikes %target (harness placeholder)",
  image: "",
};

/**
 * Katana record used by C1–C3 and B3: the accepted record (all mechanics and
 * economy from the committed spec), effects in validator-parsed stored form,
 * presentation placeholders, and a harness row id. `overrides` exist only for
 * labelled control experiments (e.g. ALL-method aggregation).
 */
export const katanaRecord = (overrides: Record<string, unknown> = {}) => {
  const rec = structuredClone(acceptedKatana().record);
  const parsed = parseItemEffects(rec.effects);
  if (!parsed.success) throw new Error("Accepted Katana effects did not parse");
  return {
    ...rec,
    ...PRESENTATION_PLACEHOLDERS,
    id: "harness-skyglass-katana",
    effects: parsed.data,
    ...overrides,
  };
};

/**
 * Hypothetical Crystal record. Its effects array cannot pass the item validator
 * (gate B1); each tag is parsed alone so the record has the stored form it WOULD
 * have under a validator exception. Runtime use of it proves post-composition
 * behaviour only, not production validity.
 */
export const crystalRecord = (rarity = "RARE", overrides: Record<string, unknown> = {}) => {
  const fs = flamingSword().record;
  return {
    ...fs,
    id: "harness-skyglass-crystal",
    name: "Skyglass Crystal (harness hypothetical)",
    itemType: "CRYSTAL",
    weaponType: "NONE",
    slot: "ITEM",
    target: "SELF",
    method: "SINGLE",
    range: 0,
    rarity,
    canBeImbued: false,
    crystalTargetTypes: "WEAPON",
    effects: parseTagsIndividually(CRYSTAL_EFFECTS_INPUT()),
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
