/**
 * Ghost Ship / Skyglass Stage 2 harness — item fixtures for gates B and C.
 *
 * Approved effect contracts (RUL-2026-10-10-007, state/ghost_ship_skyglass_reward_decisions.md):
 *   Katana  = LEGENDARY WEAPON/SWORD, canBeImbued:false,
 *             pierce(power 50) + immunity(blocks buffprevent, rounds 2, SELF)
 *             + consume(power 40, percentage, SELF)
 *   Crystal = CRYSTAL, crystalTargetTypes WEAPON, consume(power 20, percentage) only.
 *
 * Every NON-effect field (AP, costs, cooldown, range, slot, economy, …) is
 * unselected by the director. Records here take those fields from the captured
 * Flaming Sword row (harvests/inbox/tnr_results_1788235198666.json
 * #/captures/8/data/items/0/item, EPIC SWORD, 2026-09-01) as a labelled TEST
 * CARRIER only. Effect stat/general classification on the Katana Pierce is
 * likewise carried from Flaming Sword's own damage effect (statTypes/generalTypes
 * ["Highest"]). These are not recommendations for the final Katana.
 */
import { ItemValidator, ItemValidatorRawSchema, getTagSchema } from "@/validators/combat";
import * as F from "./fixtures";

export const FLAMING_SWORD = {
  file: "harvests/inbox/tnr_results_1788235198666.json",
  pointer: "/captures/8/data/items/0/item",
};
export const flamingSword = () => F.captured(FLAMING_SWORD.file, FLAMING_SWORD.pointer);

export const KATANA_EFFECTS_INPUT = () => {
  const fs = flamingSword().record;
  const dmg = fs.effects.find((e: any) => e.type === "damage");
  return [
    {
      type: "pierce",
      power: 50,
      powerPerLevel: 0,
      rounds: 0,
      calculation: "formula",
      target: "INHERIT",
      statTypes: dmg.statTypes, // carrier: Flaming Sword damage effect
      generalTypes: dmg.generalTypes, // carrier: Flaming Sword damage effect
    },
    { type: "immunity", blocks: "buffprevent", rounds: 2, target: "SELF" },
    { type: "consume", power: 40, calculation: "percentage", target: "SELF" },
  ];
};
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

/** Katana record on the Flaming Sword carrier. Effects are the validator-parsed form. */
export const katanaRecord = (overrides: Record<string, unknown> = {}) => {
  const fs = flamingSword().record;
  const parsed = parseItemEffects(KATANA_EFFECTS_INPUT());
  if (!parsed.success) throw new Error("Katana effects did not parse");
  return {
    ...fs,
    id: "harness-skyglass-katana",
    name: "Skyglass Katana (harness carrier)",
    rarity: "LEGENDARY",
    itemType: "WEAPON",
    weaponType: "SWORD",
    canBeImbued: false,
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
