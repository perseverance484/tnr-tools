/** FINAL 2/2 Skyglass item records (RUL-2026-10-11-006): complete-record schema
 * validation and actual read-only occupation guards. Katana15 / Crystal10, both
 * Consume rounds2 / shieldRounds2; Crystal LEGENDARY, tradable, not craftable,
 * no recipe. Unapproved Crystal carrier fields and presentation placeholders are
 * labelled. No persistence is attempted: the database proxy traps every write.
 */
import { afterAll, beforeEach, describe, expect, it } from "bun:test";
import { ItemValidatorRawSchema } from "@/validators/combat";
import { CRAFTING_MAX_IMBUED_ITEMS, CRAFTING_RANKS, CRAFTING_REQUIRED_EXP, CRAFTING_TIMES_MINS, ItemRarities } from "@/drizzle/constants";
import { occupationRouter } from "@/server/api/routers/occupation";
import { getCraftingRank, getEffectiveMaxImbuements } from "@/libs/crafting";
import { resetServerModuleStubs, stubProfile } from "../setup/serverModules";
import * as F from "./lib/fixtures";
import * as I from "./lib/items";
import * as IB from "./lib/itembattle";
import { Evidence, requireClean } from "./lib/report";
import { mulberry32 } from "./lib/sim";

const CONTRACT = new Evidence("CONTRACT");
const GUARDS = new Evidence("GUARDS");
const realRandom = Math.random;
beforeEach(() => { Math.random = mulberry32(1510); });
afterAll(() => {
  Math.random = realRandom;
  CONTRACT.flush({ scope: "final 2/2 candidate records (RUL006); Crystal unapproved carrier fields and presentation pending", records: I.RECORDS_PATH });
  GUARDS.flush({ scope: "actual pre-write eligibility paths with read-only stubs; no persistence, CAS/concurrency, committed craft/imbue or executed trade" });
});
const CONSUME_MSG = "ConsumeTag must be used together with a damage or pierce effect on the same action";
const diff = (before: any, after: any, path = ""): any[] => {
  if (Array.isArray(before) && Array.isArray(after) && before.length === after.length)
    return before.flatMap((v, i) => diff(v, after[i], `${path}/${i}`));
  if (before && after && typeof before === "object" && typeof after === "object" && !Array.isArray(before) && !Array.isArray(after))
    return [...new Set([...Object.keys(before), ...Object.keys(after)])].sort().flatMap((k) => diff(before[k], after[k], `${path}/${k}`));
  return before === after ? [] : [{ path, before, after }];
};
const consumeOk = (t: any, power: number) => t?.type === "consume" && t?.power === power && t?.target === "SELF" && t?.calculation === "percentage" && t?.rounds === 2 && t?.shieldRounds === 2;

describe("CONTRACT — final 2/2 candidate records and source schema", () => {
  it("derives the Katana from Night's Testament with only the disclosed r4 and 3/3 deltas", () => {
    const packet = I.finalRecords();
    const spec = I.acceptedKatana();
    const cap = F.captured(spec.baseline.capture, spec.baseline.pointer).record;
    const rec = spec.record;
    const overrides = Object.entries(spec.provenance).filter(([, p]: any) => p.source === "override").map(([k]) => k).sort();
    const missing = Object.keys(cap).filter((k) => !(k in rec) && !spec.droppedFields.includes(k));
    const extra = Object.keys(rec).filter((k) => !(k in cap));
    const mismatch = Object.keys(rec).filter((k) => !overrides.includes(k) && JSON.stringify(rec[k]) !== JSON.stringify(cap[k]));
    const r4Diff = diff(F.loadJson(I.HISTORICAL_KATANA_PATH).record, rec);
    const c33Diff = diff(F.loadJson(I.HISTORICAL_3X3_PATH).katana.record, rec);
    const wantR4 = [{ path: "/effects/2/power", before: 40, after: 15 }, { path: "/effects/2/rounds", before: 0, after: 2 }, { path: "/effects/2/shieldRounds", before: 3, after: 2 }];
    const want33 = [{ path: "/effects/2/rounds", before: 3, after: 2 }, { path: "/effects/2/shieldRounds", before: 3, after: 2 }];
    const hashes = {
      katanaCapture: F.fileSha256(spec.baseline.capture),
      crystalCapture: F.fileSha256(packet.crystal.baseline.capture),
      r4Katana: F.fileSha256(I.HISTORICAL_KATANA_PATH),
      carriers3x3: F.fileSha256(I.HISTORICAL_3X3_PATH),
      contract: F.fileSha256(I.CONTRACT_PATH),
    };
    CONTRACT.put("sourceProvenance", { engineCommit: packet.engineCommit, designCommit: packet.designCommit, hashes, katanaBaseline: spec.baseline, crystalShapeDonor: packet.crystal.baseline });
    CONTRACT.put("katanaDiffs", { fromR4: r4Diff, from3x3: c33Diff });
    CONTRACT.put("recordStatus", { status: packet.status, timing: packet.timing, consumeOverlap: packet.consumeOverlap, presentationPending: spec.presentationPending });
    expect(r4Diff).toEqual(wantR4);
    expect(c33Diff).toEqual(want33);
    CONTRACT.check("all 65 non-override Katana fields equal Night's Testament; no missing or extra fields", mismatch.length === 0 && missing.length === 0 && extra.length === 0 && Object.keys(rec).length - overrides.length === 65, { mismatch, missing, extra, fields: Object.keys(rec).length });
    CONTRACT.check("the nine ruling/presentation overrides remain the exact accepted set", JSON.stringify(overrides) === JSON.stringify(["battleDescription", "canBeCrafted", "canBeImbued", "craftingExperience", "description", "effects", "hidden", "image", "name"]), overrides);
    CONTRACT.check("r4 Katana → final differs only in Consume power 40→15, rounds 0→2, shieldRounds 3→2", JSON.stringify(r4Diff) === JSON.stringify(wantR4), r4Diff);
    CONTRACT.check("3/3 carrier → final Katana differs only in Consume rounds 3→2 and shieldRounds 3→2", JSON.stringify(c33Diff) === JSON.stringify(want33), c33Diff);
    CONTRACT.check("capture, historical record, 3/3 packet and contract SHA256 values match record provenance", hashes.katanaCapture === spec.baseline.captureSha256 && hashes.crystalCapture === packet.crystal.baseline.captureSha256 && hashes.r4Katana === packet.historical.r4Katana.sha256 && hashes.carriers3x3 === packet.historical.activeConsume3x3.sha256 && hashes.contract === packet.contract.sha256, hashes);
    CONTRACT.check("timing is the approved RUL006 2/2 and the historical diffs recorded in the packet match", packet.timing.approved === true && packet.timing.consumeRounds === 2 && packet.timing.generatedShieldRounds === 2 && JSON.stringify(packet.historical.r4Katana.katanaDiff) === JSON.stringify(r4Diff) && JSON.stringify(packet.historical.activeConsume3x3.katanaDiff) === JSON.stringify(c33Diff));
  });

  it("validates exactly Pierce50 Crystal + SELF immunity2r + Consume15 2/2, and the complete Katana record", () => {
    const effects = I.parseItemEffects(I.KATANA_EFFECTS_INPUT());
    const full = I.validateItem(I.katanaRecord());
    CONTRACT.put("katanaValidation", { effectsAccepted: effects.success, effects: effects.success ? effects.data : null, fullAccepted: full.success, issues: I.issues(full), presentationPlaceholders: I.PRESENTATION_PLACEHOLDERS });
    expect(effects.success).toBe(true);
    expect(full.success).toBe(true);
    const e: any[] = effects.success ? effects.data : [];
    CONTRACT.check("exact three-effect Katana contract validates with Consume15 rounds2/shieldRounds2", e.length === 3 && e[0]?.type === "pierce" && e[0]?.power === 50 && e[0]?.powerPerLevel === 0 && JSON.stringify(e[0]?.elements) === JSON.stringify(["Crystal"]) && e[1]?.type === "immunity" && e[1]?.blocks === "buffprevent" && e[1]?.rounds === 2 && e[1]?.target === "SELF" && consumeOk(e[2], 15));
    CONTRACT.check("full ItemValidator accepts the complete Katana with labelled presentation placeholders", full.success, I.issues(full));
    const k = I.katanaRecord();
    CONTRACT.check("Katana remains LEGENDARY WEAPON/SWORD, non-imbuable, hidden, drop-only and tradable; AP40 CD6 range4 40/40/0", k.itemType === "WEAPON" && k.weaponType === "SWORD" && k.rarity === "LEGENDARY" && !k.canBeImbued && k.hidden && !k.canBeCrafted && k.craftingExperience === 0 && !k.inShop && k.canBeTraded && k.actionCostPerc === 40 && k.cooldown === 6 && k.range === 4 && k.chakraCost === 40 && k.staminaCost === 40 && k.healthCost === 0);
  });

  it("validates the complete final Crystal: LEGENDARY, tradable, not craftable, no recipe, exactly one Consume10 2/2", () => {
    const packet = I.finalRecords();
    const contract = F.loadJson(I.CONTRACT_PATH).crystal;
    const e = I.parseItemEffects(I.CRYSTAL_EFFECTS_INPUT());
    const rec = I.crystalRecord();
    const full = I.validateItem(rec);
    const out: any = full.success ? full.data : null;
    const stored = packet.crystal.record;
    const unapproved = packet.crystal.unapprovedCarrierFields;
    CONTRACT.put("crystalValidation", { effectsAccepted: e.success, parsedEffects: e.success ? e.data : null, fullAccepted: full.success, issues: I.issues(full), validatorOutputEconomy: out ? { canBeTraded: out.canBeTraded, canBeCrafted: out.canBeCrafted, craftingRequirements: out.craftingRequirements, craftingExperience: out.craftingExperience, auctionMinPrice: out.auctionMinPrice ?? null, auctionMaxPrice: out.auctionMaxPrice ?? null } : null, unapprovedCarrierFields: unapproved, diffFrom3x3: packet.historical.activeConsume3x3.crystalDiff });
    expect(e.success).toBe(true);
    expect(full.success).toBe(true);
    CONTRACT.check("Crystal effects are exactly one Consume10 rounds2/shieldRounds2 (no Damage/Pierce filler)", e.success && e.data.length === 1 && consumeOk(e.data[0], 10));
    CONTRACT.check("full ItemValidator accepts the complete LEGENDARY Crystal with labelled presentation placeholders", full.success, I.issues(full));
    CONTRACT.check("decided Crystal fields equal the RUL006 contract (CRYSTAL, WEAPON-only, LEGENDARY, canBeTraded true, canBeCrafted false)", stored.itemType === contract.itemType && stored.crystalTargetTypes === contract.crystalTargetTypes && stored.rarity === contract.rarity && stored.canBeTraded === contract.canBeTraded && stored.canBeCrafted === contract.canBeCrafted && consumeOk(stored.effects[0], contract.consume.power) && stored.effects.length === contract.effectCount);
    CONTRACT.check("no recipe remains operative: craftingRequirements [] and craftingExperience 0, preserved by the validator", JSON.stringify(stored.craftingRequirements) === "[]" && stored.craftingExperience === 0 && out && JSON.stringify(out.craftingRequirements) === "[]" && out.canBeCrafted === false && out.craftingExperience === 0, out && { craftingRequirements: out.craftingRequirements, craftingExperience: out.craftingExperience });
    CONTRACT.check("trade flag is record/schema evidence only: stored and validator output canBeTraded true; no auction price bounds set", stored.canBeTraded === true && out?.canBeTraded === true && (out?.auctionMinPrice ?? null) === null && (out?.auctionMaxPrice ?? null) === null);
    CONTRACT.check("Crystal is created hidden and not sold in shops (acquisition is the 3% Reliquary drop)", stored.hidden === true && stored.inShop === false);
    CONTRACT.check("every undecided carrier field is disclosed in the packet with its recorded value", Object.entries(unapproved).every(([k, v]) => JSON.stringify(stored[k]) === JSON.stringify(v)) && Object.keys(unapproved).length === 14, Object.keys(unapproved));
  });

  it("instant-only negative control still requires a Damage/Pierce companion", () => {
    const instant = I.CRYSTAL_EFFECTS_INPUT().map((e) => ({ ...e, rounds: 0 }));
    const r = I.parseItemEffects(instant);
    const full = I.validateItem({ ...I.crystalRecord(), effects: instant });
    const damageControl = I.parseItemEffects([...instant, { type: "damage", power: 1, calculation: "static" }]);
    CONTRACT.put("instantNegativeControl", { instantEffects: I.issues(r), instantFullItem: I.issues(full), damageControlAccepted: damageControl.success });
    expect(r.success).toBe(false);
    CONTRACT.check("instant standalone Consume array rejected with exactly the companion-tag issue", !r.success && I.issues(r).length === 1 && I.issues(r)[0].message === CONSUME_MSG, I.issues(r));
    CONTRACT.check("full instant Crystal rejects at effects for the same rule; a damage control is accepted", !full.success && I.issues(full).some((i: any) => i.path.startsWith("effects") && i.message === CONSUME_MSG) && damageControl.success);
  });

  it("canBeImbued:false remains the disabling field, not maxImbueNumber0", () => {
    const s = ItemValidatorRawSchema.shape;
    CONTRACT.check("maxImbueNumber0 rejects, 1 accepts and canBeImbued:false accepts", !s.maxImbueNumber.safeParse(0).success && s.maxImbueNumber.safeParse(1).success && s.canBeImbued.safeParse(false).success);
  });
});

describe("GUARDS — WEAPON restriction, recipient eligibility, duplicates, rank", () => {
  const USER = "user_crafter";
  const WRITE = "HARNESS_WRITE_TRAPPED";
  const mkUser = (over: Record<string, unknown> = {}) => ({
    userId: USER, status: "AWAKE", sector: 0, occupation: "CRAFTING",
    craftingExperience: CRAFTING_REQUIRED_EXP.FORGEMASTER, updatedAt: new Date(0),
    // Read-only profile fields the craft path reads after its guards (quest tracking).
    userQuests: [], completedQuests: [], ...over,
  });
  const readOnlyClient = (rows: any[], item?: any) =>
    new Proxy({}, {
      get(_t, prop) {
        if (prop === "query") {
          return {
            userItem: { findMany: async () => rows },
            item: { findFirst: async () => item },
            userQueue: { findMany: async () => [] },
          };
        }
        throw new Error(`${WRITE}:${String(prop)}`);
      },
    });
  const call = async (user: any, rows: any[], input: any, proc: "imbueItem" | "craftItem" = "imbueItem", item?: any) => {
    stubProfile("fetchUpdatedUser", (async () => ({ user })) as never);
    const caller = occupationRouter.createCaller({ drizzle: readOnlyClient(rows, item), userId: USER } as never);
    try {
      const res: any = await (caller as any)[proc](input);
      return { outcome: "response", message: res?.message ?? null, success: res?.success ?? null };
    } catch (e: any) {
      const msg = String(e?.message ?? e);
      return msg.includes(WRITE) ? { outcome: "guards-passed-reached-write", message: msg.split(":").slice(1).join(":") } : { outcome: "error", message: msg };
    } finally {
      resetServerModuleStubs();
    }
  };
  const rowFor = (item: any, extra: Record<string, unknown> = {}) => ({ ...I.userItemRow(USER, item, { equipped: "NONE" }), ...extra });
  const WRITE_REACHED = { outcome: "guards-passed-reached-write", message: "update" };
  const reject = (message: string) => ({ outcome: "response", message, success: false });
  /**
   * Expected imbueItem outcome per crafting rank × crystal rarity, on an eligible
   * imbuable WEAPON with maxImbueNumber 1 and no imbuements. Source (pin
   * 585534d7, occupation.ts imbueItem): the slot guard runs first
   * (getEffectiveMaxImbuements: NOVICE 0 slots); then CRAFTING_TIMES_MINS[rank][rarity]
   * === 0 rejects. The engine's rejection text names the wrong rank
   * ("Apprentice" for EPIC, "Master" otherwise); recorded verbatim.
   */
  const IMBUE_MATRIX: Record<string, Record<string, object>> = {
    NOVICE: { RARE: reject("You have reached the maximum number of crystals for this item (0)"), EPIC: reject("You have reached the maximum number of crystals for this item (0)"), LEGENDARY: reject("You have reached the maximum number of crystals for this item (0)") },
    APPRENTICE: { RARE: WRITE_REACHED, EPIC: reject("You need to be at least Apprentice rank to imbue EPIC crystals"), LEGENDARY: reject("You need to be at least Master rank to imbue LEGENDARY crystals") },
    MASTER: { RARE: WRITE_REACHED, EPIC: WRITE_REACHED, LEGENDARY: reject("You need to be at least Master rank to imbue LEGENDARY crystals") },
    FORGEMASTER: { RARE: WRITE_REACHED, EPIC: WRITE_REACHED, LEGENDARY: WRITE_REACHED },
  };
  /** Expected craftItem outcome per rank × rarity (empty inventory: eligible ranks stop at the 12-Filament material check). */
  const MATERIAL = reject("You need 12 Unknown item (you have 0)");
  const CRAFT_MATRIX: Record<string, Record<string, object>> = {
    NOVICE: { RARE: reject("You need to be at least Apprentice rank to craft RARE items"), EPIC: reject("You need to be at least Master rank to craft EPIC items"), LEGENDARY: reject("You need to be at least Forgemaster rank to craft LEGENDARY items") },
    APPRENTICE: { RARE: MATERIAL, EPIC: reject("You need to be at least Master rank to craft EPIC items"), LEGENDARY: reject("You need to be at least Forgemaster rank to craft LEGENDARY items") },
    MASTER: { RARE: MATERIAL, EPIC: MATERIAL, LEGENDARY: reject("You need to be at least Forgemaster rank to craft LEGENDARY items") },
    FORGEMASTER: { RARE: MATERIAL, EPIC: MATERIAL, LEGENDARY: MATERIAL },
  };
  const matrixMismatches = (cases: Record<string, any>, want: Record<string, Record<string, object>>) =>
    Object.entries(want).flatMap(([rank, row]) => Object.entries(row).filter(([rarity, w]) => JSON.stringify(cases[`rank_${rank}_${rarity}`]) !== JSON.stringify(w)).map(([rarity]) => ({ cell: `${rank}/${rarity}`, got: cases[`rank_${rank}_${rarity}`], want: row[rarity] })));

  it("imbueItem guard matrix (real procedure, read-only stub)", async () => {
    // Final LEGENDARY Crystal in its published state (records are created hidden;
    // the as-created hidden state is exercised separately below).
    const crystal = I.crystalRecord("LEGENDARY", { hidden: false });
    const sword = I.imbuableWeapon();
    const sword3 = I.imbuableWeapon({ maxImbueNumber: 3 });
    const cRow = rowFor(crystal);
    const sRow = rowFor(sword);
    const cases: Record<string, any> = {};
    cases.eligibleWeapon = await call(mkUser(), [sRow, cRow], { userItemId: sRow.id, userCrystalItemId: cRow.id });
    const hiddenCrystal = rowFor(I.crystalRecord());
    cases.finalCrystalAsCreatedHidden = await call(mkUser(), [sRow, hiddenCrystal], { userItemId: sRow.id, userCrystalItemId: hiddenCrystal.id });
    // The accepted record is created hidden; fetchUserItems drops hidden items, so the
    // canBeImbued guard is exercised on the published state, and the hidden state separately.
    const kRow = rowFor(I.katanaRecord({ hidden: false }));
    cases.katanaNonImbuable = await call(mkUser(), [kRow, cRow], { userItemId: kRow.id, userCrystalItemId: cRow.id });
    const kHidden = rowFor(I.katanaRecord());
    cases.katanaWhileHidden = await call(mkUser(), [kHidden, cRow], { userItemId: kHidden.id, userCrystalItemId: cRow.id });
    const fsRow = rowFor(I.flamingSword().record);
    cases.capturedFlamingSwordNonImbuable = await call(mkUser(), [fsRow, cRow], { userItemId: fsRow.id, userCrystalItemId: cRow.id });
    const armor = { ...I.imbuableWeapon(), id: "harness-armor", itemType: "ARMOR", slot: "CHEST" };
    const aRow = rowFor(armor);
    cases.armorRecipient = await call(mkUser(), [aRow, cRow], { userItemId: aRow.id, userCrystalItemId: cRow.id });
    const s3Row = rowFor(sword3);
    const dupRow = { ...s3Row, imbuements: [I.imbuementRow(s3Row.id, crystal)] };
    cases.duplicateCrystal = await call(mkUser({ craftingExperience: CRAFTING_REQUIRED_EXP.FORGEMASTER }), [dupRow, cRow], { userItemId: s3Row.id, userCrystalItemId: cRow.id });
    cases.maxImbuementsReached = await call(mkUser({ craftingExperience: CRAFTING_REQUIRED_EXP.APPRENTICE }), [{ ...sRow, imbuements: [I.imbuementRow(sRow.id, { ...crystal, id: "other-crystal" })] }, cRow], { userItemId: sRow.id, userCrystalItemId: cRow.id });
    const notCrystal = rowFor({ ...crystal, id: "harness-not-crystal", itemType: "MATERIAL" });
    cases.notACrystal = await call(mkUser(), [sRow, notCrystal], { userItemId: sRow.id, userCrystalItemId: notCrystal.id });
    cases.crystalReservedForAuction = await call(mkUser(), [sRow, { ...cRow, isInAuction: true }], { userItemId: sRow.id, userCrystalItemId: cRow.id });
    const skillCrystal = rowFor(I.crystalRecord("LEGENDARY", { hidden: false, requiredSkillId: "harness-crystal-skill" }));
    cases.requiredSkillAbsent = await call(mkUser(), [sRow, skillCrystal], { userItemId: sRow.id, userCrystalItemId: skillCrystal.id });
    cases.requiredSkillInactive = await call(mkUser({ userSkills: [{ skillId: "harness-crystal-skill", activated: false }] }), [sRow, skillCrystal], { userItemId: sRow.id, userCrystalItemId: skillCrystal.id });
    cases.requiredSkillActive = await call(mkUser({ userSkills: [{ skillId: "harness-crystal-skill", activated: true }] }), [sRow, skillCrystal], { userItemId: sRow.id, userCrystalItemId: skillCrystal.id });
    cases.equippedRecipient = await call(mkUser(), [{ ...sRow, equipped: "HAND_1" }, cRow], { userItemId: sRow.id, userCrystalItemId: cRow.id });
    for (const occ of [null, "GATHERING", "HUNTING"]) cases[`occupation_${occ}`] = await call(mkUser({ occupation: occ }), [sRow, cRow], { userItemId: sRow.id, userCrystalItemId: cRow.id });
    for (const rank of CRAFTING_RANKS) {
      for (const rarity of ["RARE", "EPIC", "LEGENDARY"]) {
        const c = I.crystalRecord(rarity, { hidden: false });
        const cr = rowFor(c);
        cases[`rank_${rank}_${rarity}`] = await call(mkUser({ craftingExperience: CRAFTING_REQUIRED_EXP[rank] }), [sRow, cr], { userItemId: sRow.id, userCrystalItemId: cr.id });
      }
    }
    GUARDS.put("imbueItemGuards", cases);
    expect(cases.eligibleWeapon.outcome).toBe("guards-passed-reached-write");
    expect(cases.katanaNonImbuable.message).toBe("This item cannot be imbued");
    expect(cases.capturedFlamingSwordNonImbuable.message).toBe("This item cannot be imbued");
    expect(cases.armorRecipient.message).toBe("This crystal can only be applied to WEAPON items");
    expect(cases.duplicateCrystal.message).toContain("already has a");
    expect(cases.notACrystal.message).toBe("Selected item is not a crystal");
    expect(cases.equippedRecipient.message).toBe("You cannot imbue an equipped item");
    expect(cases.occupation_GATHERING.message).toBe("You must have the Crafting occupation to imbue items");
    GUARDS.check("final LEGENDARY Crystal (published state) on an eligible imbuable WEAPON at FORGEMASTER passes every tested pre-write guard and reaches the first (trapped) write; persistence/concurrency not exercised", cases.eligibleWeapon.outcome === "guards-passed-reached-write", cases.eligibleWeapon);
    GUARDS.check("final Crystal as created (hidden:true) is invisible to imbueItem (fetchUserItems excludes hidden items)", JSON.stringify(cases.finalCrystalAsCreatedHidden) === JSON.stringify(reject("Crystal not found")), cases.finalCrystalAsCreatedHidden);
    GUARDS.check("native rank gate for the final LEGENDARY Crystal: only FORGEMASTER reaches the write", ["NOVICE", "APPRENTICE", "MASTER"].every((r) => cases[`rank_${r}_LEGENDARY`].outcome === "response") && cases.rank_FORGEMASTER_LEGENDARY.outcome === "guards-passed-reached-write");
    expect(cases.maxImbuementsReached).toEqual(reject("You have reached the maximum number of crystals for this item (1)"));
    GUARDS.check("imbuement-slot limit: APPRENTICE (1 slot) on a maxImbueNumber-1 weapon that already holds a crystal is rejected", JSON.stringify(cases.maxImbuementsReached) === JSON.stringify(reject("You have reached the maximum number of crystals for this item (1)")), cases.maxImbuementsReached);
    const imbueMismatch = matrixMismatches(cases, IMBUE_MATRIX);
    expect(imbueMismatch).toEqual([]);
    GUARDS.check("imbueItem rank × rarity matrix: all 12 cells equal the source-derived expectation", imbueMismatch.length === 0, imbueMismatch);
    GUARDS.check("final Katana (canBeImbued:false, published state) rejects the final Crystal", cases.katanaNonImbuable.message === "This item cannot be imbued");
    GUARDS.check("while hidden, the Katana is invisible to imbueItem (fetchUserItems excludes hidden items)", cases.katanaWhileHidden.message === "Target item not found", cases.katanaWhileHidden);
    GUARDS.check("non-WEAPON recipient rejected by crystalTargetTypes", cases.armorRecipient.message === "This crystal can only be applied to WEAPON items");
    GUARDS.check("duplicate crystal ID rejected", String(cases.duplicateCrystal.message).includes("already has a"));
    GUARDS.check("non-CRAFTING occupations rejected (none/GATHERING/HUNTING)", ["occupation_null", "occupation_GATHERING", "occupation_HUNTING"].every((k) => cases[k].message === "You must have the Crafting occupation to imbue items"));
    GUARDS.check("equipped recipient rejected", cases.equippedRecipient.message === "You cannot imbue an equipped item");
    GUARDS.check("new source pre-write guard rejects a Crystal reserved for auction/trade", JSON.stringify(cases.crystalReservedForAuction) === JSON.stringify(reject("Cannot use a crystal reserved for auction or trade")), cases.crystalReservedForAuction);
    GUARDS.check("new source required-skill guard rejects absent or inactive skill (synthetic skill control)", [cases.requiredSkillAbsent, cases.requiredSkillInactive].every((r) => JSON.stringify(r) === JSON.stringify(reject("Activate the required skill to use this crystal"))), { absent: cases.requiredSkillAbsent, inactive: cases.requiredSkillInactive });
    GUARDS.check("new source required-skill guard permits the active skill and reaches trapped first write (control only)", JSON.stringify(cases.requiredSkillActive) === JSON.stringify(WRITE_REACHED), cases.requiredSkillActive);
  });

  it("final Crystal canBeCrafted:false rejects crafting even for FORGEMASTER with a full 12-Filament stack (real procedure)", async () => {
    // Controls supply the superseded 12-Filament recipe and enough materials, so the
    // only difference between the rejected final record and the write-reaching control
    // is the canBeCrafted flag. The recipe is NOT part of the final record.
    const filament = { id: "harness-filament", name: "Skyglass Filament (harness carrier)", itemType: "MATERIAL", rarity: "COMMON", hidden: false, stackSize: 100 };
    const filamentRow = rowFor(filament, { quantity: 12 });
    const recipe = [{ requirementItemId: filament.id, quantity: 12, requirementItem: { id: filament.id, name: filament.name } }];
    const finalPublished = { ...I.crystalRecord("LEGENDARY", { hidden: false }), parentItemId: null };
    const cases: Record<string, any> = {};
    cases.finalAsCreatedHidden = await call(mkUser(), [filamentRow], { itemId: finalPublished.id, quantity: 1 }, "craftItem", { ...I.crystalRecord(), parentItemId: null, craftingRequirements: [] });
    cases.finalPublishedNoRecipe = await call(mkUser(), [filamentRow], { itemId: finalPublished.id, quantity: 1 }, "craftItem", { ...finalPublished, craftingRequirements: [] });
    cases.finalPublishedWithRestoredRecipeAndMaterials = await call(mkUser(), [filamentRow], { itemId: finalPublished.id, quantity: 1 }, "craftItem", { ...finalPublished, craftingRequirements: recipe });
    cases.controlCraftableWithRecipeAndMaterials = await call(mkUser(), [filamentRow], { itemId: finalPublished.id, quantity: 1 }, "craftItem", { ...finalPublished, canBeCrafted: true, craftingRequirements: recipe });
    cases.controlCraftableNoRecipe = await call(mkUser(), [filamentRow], { itemId: finalPublished.id, quantity: 1 }, "craftItem", { ...finalPublished, canBeCrafted: true, craftingRequirements: [] });
    for (const occ of ["GATHERING", "HUNTING", null]) cases[`occupation_${occ}`] = await call(mkUser({ occupation: occ }), [filamentRow], { itemId: finalPublished.id, quantity: 1 }, "craftItem", { ...finalPublished, canBeCrafted: true, craftingRequirements: recipe });
    GUARDS.put("craftItemGuards", { note: "harness Filament carrier and restored-recipe controls; neither is part of the final record", cases });
    const notCraftable = reject("This item is not craftable");
    // craftItem's first write is a DB transaction (imbueItem's is an update).
    const CRAFT_WRITE_REACHED = { outcome: "guards-passed-reached-write", message: "transaction" };
    expect(cases.finalPublishedNoRecipe).toEqual(notCraftable);
    expect(cases.finalPublishedWithRestoredRecipeAndMaterials).toEqual(notCraftable);
    expect(cases.controlCraftableWithRecipeAndMaterials).toEqual(CRAFT_WRITE_REACHED);
    GUARDS.check("final Crystal (published, no recipe) is rejected: \"This item is not craftable\"", JSON.stringify(cases.finalPublishedNoRecipe) === JSON.stringify(notCraftable), cases.finalPublishedNoRecipe);
    GUARDS.check("even with the old recipe restored and 12 Filaments held, a FORGEMASTER cannot craft the final Crystal", JSON.stringify(cases.finalPublishedWithRestoredRecipeAndMaterials) === JSON.stringify(notCraftable), cases.finalPublishedWithRestoredRecipeAndMaterials);
    GUARDS.check("control: the same inputs with canBeCrafted:true pass every pre-write guard and reach the trapped write, so the flag alone blocks crafting", JSON.stringify(cases.controlCraftableWithRecipeAndMaterials) === JSON.stringify(CRAFT_WRITE_REACHED), cases.controlCraftableWithRecipeAndMaterials);
    GUARDS.check("as created (hidden:true) the final Crystal is rejected as hidden before the craftable check", JSON.stringify(cases.finalAsCreatedHidden) === JSON.stringify(reject("This item is hidden and cannot be crafted")), cases.finalAsCreatedHidden);
    GUARDS.check("control: a craftable record with no requirements is rejected for missing requirements", JSON.stringify(cases.controlCraftableNoRecipe) === JSON.stringify(reject("This item cannot be crafted (no requirements defined)")), cases.controlCraftableNoRecipe);
    GUARDS.check("craftItem requires the CRAFTING occupation (GATHERING/HUNTING/none)", ["occupation_GATHERING", "occupation_HUNTING", "occupation_null"].every((k) => cases[k].message === "You must have the Crafting occupation to craft items"), cases);
  });

  it("native craft rank × rarity control (restored-recipe carrier, empty inventory)", async () => {
    const carrier = { ...I.crystalRecord("RARE", { hidden: false }), canBeCrafted: true, parentItemId: null, craftingRequirements: [{ requirementItemId: "filament", quantity: 12, requirementItem: { id: "filament" } }] };
    const cases: Record<string, any> = {};
    for (const rank of CRAFTING_RANKS) for (const rarity of ["RARE", "EPIC", "LEGENDARY"]) {
      cases[`rank_${rank}_${rarity}`] = await call(mkUser({ craftingExperience: CRAFTING_REQUIRED_EXP[rank] }), [], { itemId: carrier.id, quantity: 1 }, "craftItem", { ...carrier, rarity });
    }
    GUARDS.put("craftRankMatrixControl", { note: "native engine behaviour with a craftable carrier; the final Crystal is not craftable", cases });
    const craftMismatch = matrixMismatches(cases, CRAFT_MATRIX);
    expect(craftMismatch).toEqual([]);
    GUARDS.check("native craftItem rank × rarity control: all 12 cells equal the source-derived expectation", craftMismatch.length === 0, craftMismatch);
  });

  it("rank/rarity/imbue-slot tables from the pinned constants", () => {
    const table = CRAFTING_RANKS.map((rank) => ({
      rank, minExperience: CRAFTING_REQUIRED_EXP[rank], maxImbuedPerItemRankLimit: CRAFTING_MAX_IMBUED_ITEMS[rank],
      effectiveMaxImbuementsForMaxImbueNumber1: getEffectiveMaxImbuements(rank, 1),
      minutes: Object.fromEntries(ItemRarities.map((r) => [r, CRAFTING_TIMES_MINS[rank][r]])),
    }));
    GUARDS.put("rankRarityTable", table);
    expect(getCraftingRank(CRAFTING_REQUIRED_EXP.MASTER)).toBe("MASTER");
    GUARDS.check("Novice has zero imbuement slots", CRAFTING_MAX_IMBUED_ITEMS.NOVICE === 0);
    const imbueGate = Object.fromEntries(CRAFTING_RANKS.map((rank) => [rank, Object.fromEntries(["RARE", "EPIC", "LEGENDARY"].map((r) => [r, getEffectiveMaxImbuements(rank, 1) > 0 && (CRAFTING_TIMES_MINS as any)[rank][r] > 0]))]));
    const expectedGate = Object.fromEntries(Object.entries(IMBUE_MATRIX).map(([rank, row]) => [rank, Object.fromEntries(Object.entries(row).map(([r, w]) => [r, (w as any).outcome === "guards-passed-reached-write"]))]));
    GUARDS.check("imbue eligibility derived from the pinned constants equals the expected matrix", JSON.stringify(imbueGate) === JSON.stringify(expectedGate), { imbueGate, expectedGate });
  });

  it("battle assembly suppresses imbuements on canBeImbued:false recipients", async () => {
    const W = "user_legacy";
    const katana = I.katanaRecord();
    const row = I.userItemRow(W, katana);
    row.imbuements = [I.imbuementRow(row.id, I.crystalRecord())];
    const fs = I.flamingSword().record;
    const row2 = I.userItemRow(W, fs, { equipped: "HAND_2" });
    row2.imbuements = [I.imbuementRow(row2.id, { ...I.crystalRecord(), id: "legacy-crystal-2" })];
    const b = await IB.build([IB.wielder(W, [row, row2]), IB.target("user_t")], [{ userId: W, x: 2, y: 4 }, { userId: "user_t", x: 4, y: 4 }]);
    const k = (b.extraState.items as any)[katana.id].effects.map((e: any) => e.type);
    const f = (b.extraState.items as any)[fs.id].effects.map((e: any) => e.type);
    GUARDS.put("battleSuppression", { katanaEffects: k, flamingSwordEffects: f });
    expect(k).toEqual(["pierce", "immunity", "consume"]);
    expect(f).toEqual(["damage", "afterburn"]);
    GUARDS.check("legacy crystal effects dropped for canBeImbued:false items at assembly", JSON.stringify(k) === JSON.stringify(["pierce", "immunity", "consume"]) && !f.includes("consume"), { k, f });
  });
});


requireClean(CONTRACT, GUARDS);
