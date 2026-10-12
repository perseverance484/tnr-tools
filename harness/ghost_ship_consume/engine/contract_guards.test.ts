/** Active Consume candidate schemas and actual read-only occupation guards.
 * Rates 15/10 are approved. Consume rounds3/shieldRounds3, Crystal non-effect
 * fields, and all presentation placeholders are TEST CARRIERS, not balance freeze.
 * No persistence is attempted: the database proxy traps every write entry point.
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
  CONTRACT.flush({ scope: "schema-valid TEST carriers; timing, Crystal economy and presentation not approved", carriers: I.CARRIERS_PATH });
  GUARDS.flush({ scope: "actual pre-write eligibility paths with read-only stubs; no persistence/concurrency proof" });
});
const CONSUME_MSG = "ConsumeTag must be used together with a damage or pierce effect on the same action";
const diff = (before: any, after: any, path = ""): any[] => {
  if (Array.isArray(before) && Array.isArray(after) && before.length === after.length)
    return before.flatMap((v, i) => diff(v, after[i], `${path}/${i}`));
  if (before && after && typeof before === "object" && typeof after === "object" && !Array.isArray(before) && !Array.isArray(after))
    return [...new Set([...Object.keys(before), ...Object.keys(after)])].sort().flatMap((k) => diff(before[k], after[k], `${path}/${k}`));
  return before === after ? [] : [{ path, before, after }];
};

describe("CONTRACT — revised candidate records and source schema", () => {
  it("preserves the accepted Katana baseline with only the disclosed Consume delta", () => {
    const packet = I.itemCarriers();
    const spec = I.acceptedKatana();
    const cap = F.captured(spec.baseline.capture, spec.baseline.pointer).record;
    const rec = spec.record;
    const overrides = Object.entries(spec.provenance).filter(([, p]: any) => p.source === "override").map(([k]) => k).sort();
    const missing = Object.keys(cap).filter((k) => !(k in rec) && !spec.droppedFields.includes(k));
    const extra = Object.keys(rec).filter((k) => !(k in cap));
    const mismatch = Object.keys(rec).filter((k) => !overrides.includes(k) && JSON.stringify(rec[k]) !== JSON.stringify(cap[k]));
    const old = F.loadJson(I.HISTORICAL_KATANA_PATH).record;
    const actualDiff = diff(old, rec);
    const expectedDiff = [{ path: "/effects/2/power", before: 40, after: 15 }, { path: "/effects/2/rounds", before: 0, after: 3 }];
    const hashes = {
      katanaCapture: F.fileSha256(spec.baseline.capture),
      crystalCapture: F.fileSha256(packet.crystal.baseline.capture),
      historicalKatana: F.fileSha256(I.HISTORICAL_KATANA_PATH),
      designDelta: F.fileSha256(packet.designDelta.file),
    };
    CONTRACT.put("sourceProvenance", { engineCommit: packet.engineCommit, hashes, katanaBaseline: spec.baseline, crystalShapeDonor: packet.crystal.baseline });
    CONTRACT.put("historicalKatanaDiff", actualDiff);
    CONTRACT.put("carrierStatus", { status: packet.status, testTiming: packet.testTiming, crystalOpenPolicy: packet.crystal.openPolicy, crystalNonEffectWarning: packet.crystal.note, presentationPending: spec.presentationPending });
    expect(actualDiff).toEqual(expectedDiff);
    expect(actualDiff).toEqual(packet.historicalKatana.recordDiff);
    CONTRACT.check("all 65 non-override Katana fields equal Night's Testament; no missing or extra fields", mismatch.length === 0 && missing.length === 0 && extra.length === 0 && Object.keys(rec).length - overrides.length === 65, { mismatch, missing, extra, fields: Object.keys(rec).length });
    CONTRACT.check("the nine ruling/presentation overrides remain the exact accepted set", JSON.stringify(overrides) === JSON.stringify(["battleDescription", "canBeCrafted", "canBeImbued", "craftingExperience", "description", "effects", "hidden", "image", "name"]), overrides);
    CONTRACT.check("r4 Katana difference is only Consume power40->15 and TEST rounds0->3", JSON.stringify(actualDiff) === JSON.stringify(expectedDiff), actualDiff);
    CONTRACT.check("both capture, historical record and design delta SHA256 values match carrier provenance", hashes.katanaCapture === spec.baseline.captureSha256 && hashes.crystalCapture === packet.crystal.baseline.captureSha256 && hashes.historicalKatana === packet.historicalKatana.sha256 && hashes.designDelta === packet.designDelta.sha256, hashes);
    CONTRACT.check("timing is explicitly unapproved and the candidate keeps both test durations at 3", packet.testTiming.approved === false && packet.testTiming.consumeRounds === 3 && packet.testTiming.generatedShieldRounds === 3);
  });

  it("validates exactly Pierce50 Crystal + SELF immunity2r + active Consume15, and the complete Katana carrier", () => {
    const effects = I.parseItemEffects(I.KATANA_EFFECTS_INPUT());
    const full = I.validateItem(I.katanaRecord());
    CONTRACT.put("katanaValidation", { effectsAccepted: effects.success, effects: effects.success ? effects.data : null, fullAccepted: full.success, issues: I.issues(full), presentationPlaceholders: I.PRESENTATION_PLACEHOLDERS });
    expect(effects.success).toBe(true);
    expect(full.success).toBe(true);
    const e: any[] = effects.success ? effects.data : [];
    CONTRACT.check("exact three-effect Katana contract validates", e.length === 3 && e[0]?.type === "pierce" && e[0]?.power === 50 && e[0]?.powerPerLevel === 0 && JSON.stringify(e[0]?.elements) === JSON.stringify(["Crystal"]) && e[1]?.type === "immunity" && e[1]?.blocks === "buffprevent" && e[1]?.rounds === 2 && e[1]?.target === "SELF" && e[2]?.type === "consume" && e[2]?.power === 15 && e[2]?.target === "SELF" && e[2]?.calculation === "percentage" && e[2]?.rounds === 3 && e[2]?.shieldRounds === 3);
    CONTRACT.check("full ItemValidator accepts the Katana with explicit test timing and labelled presentation placeholders", full.success, I.issues(full));
    const k = I.katanaRecord();
    CONTRACT.check("Katana remains LEGENDARY WEAPON/SWORD, non-imbuable, hidden, drop-only and tradable", k.itemType === "WEAPON" && k.weaponType === "SWORD" && k.rarity === "LEGENDARY" && !k.canBeImbued && k.hidden && !k.canBeCrafted && k.craftingExperience === 0 && !k.inShop && k.canBeTraded);
  });

  it("validates a Consume10-only weapon Crystal full carrier at each labelled rarity", () => {
    const e = I.parseItemEffects(I.CRYSTAL_EFFECTS_INPUT());
    const candidates = ["RARE", "EPIC", "LEGENDARY"].map((rarity) => {
      const rec = I.crystalRecord(rarity);
      const r = I.validateItem(rec);
      return { rarity, success: r.success, issues: I.issues(r) };
    });
    CONTRACT.put("crystalValidation", { effectsAccepted: e.success, parsedEffects: e.success ? e.data : null, candidates, note: "rarities and all other Crystal non-effect fields are test inputs, not policy recommendations" });
    expect(e.success).toBe(true);
    expect(candidates.every((r) => r.success)).toBe(true);
    const tag: any = e.success ? e.data[0] : null;
    CONTRACT.check("single active Consume10 SELF percentage effect accepts with test duration3 and shield duration3", e.success && e.data.length === 1 && tag?.type === "consume" && tag?.power === 10 && tag?.target === "SELF" && tag?.calculation === "percentage" && tag?.rounds === 3 && tag?.shieldRounds === 3);
    CONTRACT.check("full ItemValidator accepts all three labelled Crystal rarity carriers without Damage/Pierce", candidates.every((r) => r.success), candidates);
    CONTRACT.check("Crystal remains CRYSTAL/WEAPON-only", I.crystalRecord().itemType === "CRYSTAL" && I.crystalRecord().crystalTargetTypes === "WEAPON");
  });

  it("instant-only negative control still requires a Damage/Pierce companion; defaults are not approval", () => {
    const instant = I.CRYSTAL_EFFECTS_INPUT().map((e) => ({ ...e, rounds: 0 }));
    const r = I.parseItemEffects(instant);
    const full = I.validateItem({ ...I.crystalRecord(), effects: instant });
    const activeAlone = I.parseItemEffects([{ type: "consume", power: 10 }]);
    const damageControl = I.parseItemEffects([...instant, { type: "damage", power: 1, calculation: "static" }]);
    const pierceControl = I.parseItemEffects([...instant, { type: "pierce", power: 1, calculation: "static" }]);
    const result = { instantEffects: I.issues(r), instantFullItem: I.issues(full), omittedTimingDefaults: activeAlone.success ? activeAlone.data : I.issues(activeAlone), damageControlAccepted: damageControl.success, pierceControlAccepted: pierceControl.success };
    CONTRACT.put("instantNegativeControl", result);
    expect(r.success).toBe(false);
    expect(full.success).toBe(false);
    CONTRACT.check("instant standalone Consume array rejected with exactly companion-tag issue", !r.success && I.issues(r).length === 1 && I.issues(r)[0].message === CONSUME_MSG, I.issues(r));
    CONTRACT.check("full instant Crystal rejects at effects for the same companion rule", !full.success && I.issues(full).some((i: any) => i.path.startsWith("effects") && i.message === CONSUME_MSG), I.issues(full));
    CONTRACT.check("source defaults active Consume to rounds3/shieldRounds3; recorded only as a schema control", activeAlone.success && (activeAlone.data[0] as any)?.rounds === 3 && (activeAlone.data[0] as any)?.shieldRounds === 3);
    CONTRACT.check("synthetic instant controls accept either companion; neither control is the Crystal candidate", damageControl.success && pierceControl.success);
  });

  it("canBeImbued:false remains the disabling field, not maxImbueNumber0", () => {
    const s = ItemValidatorRawSchema.shape;
    const zero = s.maxImbueNumber.safeParse(0);
    const one = s.maxImbueNumber.safeParse(1);
    const disabled = s.canBeImbued.safeParse(false);
    CONTRACT.check("maxImbueNumber0 rejects,1 accepts and canBeImbued:false accepts", !zero.success && one.success && disabled.success);
  });
});

describe("GUARDS — WEAPON restriction, recipient eligibility, duplicates, rank", () => {
  const USER = "user_crafter";
  const WRITE = "HARNESS_WRITE_TRAPPED";
  const mkUser = (over: Record<string, unknown> = {}) => ({
    userId: USER, status: "AWAKE", sector: 0, occupation: "CRAFTING",
    craftingExperience: CRAFTING_REQUIRED_EXP.MASTER, updatedAt: new Date(0), ...over,
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
    const crystal = I.crystalRecord("RARE");
    const sword = I.imbuableWeapon();
    const sword3 = I.imbuableWeapon({ maxImbueNumber: 3 });
    const cRow = rowFor(crystal);
    const sRow = rowFor(sword);
    const cases: Record<string, any> = {};
    cases.eligibleWeapon = await call(mkUser(), [sRow, cRow], { userItemId: sRow.id, userCrystalItemId: cRow.id });
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
    const skillCrystal = rowFor(I.crystalRecord("RARE", { requiredSkillId: "harness-crystal-skill" }));
    cases.requiredSkillAbsent = await call(mkUser(), [sRow, skillCrystal], { userItemId: sRow.id, userCrystalItemId: skillCrystal.id });
    cases.requiredSkillInactive = await call(mkUser({ userSkills: [{ skillId: "harness-crystal-skill", activated: false }] }), [sRow, skillCrystal], { userItemId: sRow.id, userCrystalItemId: skillCrystal.id });
    cases.requiredSkillActive = await call(mkUser({ userSkills: [{ skillId: "harness-crystal-skill", activated: true }] }), [sRow, skillCrystal], { userItemId: sRow.id, userCrystalItemId: skillCrystal.id });
    cases.equippedRecipient = await call(mkUser(), [{ ...sRow, equipped: "HAND_1" }, cRow], { userItemId: sRow.id, userCrystalItemId: cRow.id });
    for (const occ of [null, "GATHERING", "HUNTING"]) cases[`occupation_${occ}`] = await call(mkUser({ occupation: occ }), [sRow, cRow], { userItemId: sRow.id, userCrystalItemId: cRow.id });
    for (const rank of CRAFTING_RANKS) {
      for (const rarity of ["RARE", "EPIC", "LEGENDARY"]) {
        const c = I.crystalRecord(rarity);
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
    GUARDS.check("eligible imbuable WEAPON passes every tested pre-write eligibility guard and reaches the first (trapped) write; persistence/concurrency guards not exercised", cases.eligibleWeapon.outcome === "guards-passed-reached-write", cases.eligibleWeapon);
    expect(cases.maxImbuementsReached).toEqual(reject("You have reached the maximum number of crystals for this item (1)"));
    GUARDS.check("imbuement-slot limit: APPRENTICE (1 slot) on a maxImbueNumber-1 weapon that already holds a crystal is rejected", JSON.stringify(cases.maxImbuementsReached) === JSON.stringify(reject("You have reached the maximum number of crystals for this item (1)")), cases.maxImbuementsReached);
    const imbueMismatch = matrixMismatches(cases, IMBUE_MATRIX);
    expect(imbueMismatch).toEqual([]);
    GUARDS.check("imbueItem rank × rarity matrix: all 12 cells equal the source-derived expectation", imbueMismatch.length === 0, imbueMismatch);
    GUARDS.check("revised Katana carrier (canBeImbued:false, published state) rejected", cases.katanaNonImbuable.message === "This item cannot be imbued");
    GUARDS.check("while hidden, the Katana is invisible to imbueItem (fetchUserItems excludes hidden items)", cases.katanaWhileHidden.message === "Target item not found", cases.katanaWhileHidden);
    GUARDS.check("non-WEAPON recipient rejected by crystalTargetTypes", cases.armorRecipient.message === "This crystal can only be applied to WEAPON items");
    GUARDS.check("duplicate crystal ID rejected", String(cases.duplicateCrystal.message).includes("already has a"));
    GUARDS.check("non-CRAFTING occupations rejected (none/GATHERING/HUNTING)", ["occupation_null", "occupation_GATHERING", "occupation_HUNTING"].every((k) => cases[k].message === "You must have the Crafting occupation to imbue items"));
    GUARDS.check("equipped recipient rejected", cases.equippedRecipient.message === "You cannot imbue an equipped item");
    GUARDS.check("new source pre-write guard rejects a Crystal reserved for auction/trade", JSON.stringify(cases.crystalReservedForAuction) === JSON.stringify(reject("Cannot use a crystal reserved for auction or trade")), cases.crystalReservedForAuction);
    GUARDS.check("new source required-skill guard rejects absent or inactive skill (synthetic skill control)", [cases.requiredSkillAbsent, cases.requiredSkillInactive].every((r) => JSON.stringify(r) === JSON.stringify(reject("Activate the required skill to use this crystal"))), { absent: cases.requiredSkillAbsent, inactive: cases.requiredSkillInactive });
    GUARDS.check("new source required-skill guard permits the active skill and reaches trapped first write (control only)", JSON.stringify(cases.requiredSkillActive) === JSON.stringify(WRITE_REACHED), cases.requiredSkillActive);
  });

  it("craftItem occupation and rarity/rank guards (real procedure, read-only stub)", async () => {
    const crystal = { ...I.crystalRecord("RARE"), canBeCrafted: true, hidden: false, parentItemId: null, craftingRequirements: [{ requirementItemId: "filament", quantity: 12, requirementItem: { id: "filament" } }] };
    const cases: Record<string, any> = {};
    for (const occ of ["CRAFTING", "GATHERING", "HUNTING", null]) cases[`occupation_${occ}`] = await call(mkUser({ occupation: occ }), [], { itemId: crystal.id, quantity: 1 }, "craftItem", crystal);
    for (const rank of CRAFTING_RANKS) for (const rarity of ["RARE", "EPIC", "LEGENDARY"]) {
      cases[`rank_${rank}_${rarity}`] = await call(mkUser({ craftingExperience: CRAFTING_REQUIRED_EXP[rank] }), [], { itemId: crystal.id, quantity: 1 }, "craftItem", { ...crystal, rarity });
    }
    GUARDS.put("craftItemGuards", { note: "12 Filaments per Crystal used as the requirement carrier; inventory empty so eligible ranks stop at the material check", cases });
    expect(cases.occupation_GATHERING.message).toBe("You must have the Crafting occupation to craft items");
    GUARDS.check("craftItem requires current CRAFTING occupation", ["occupation_GATHERING", "occupation_HUNTING", "occupation_null"].every((k) => cases[k].message === "You must have the Crafting occupation to craft items"), cases);
    expect(cases.occupation_CRAFTING).toEqual(MATERIAL);
    const craftMismatch = matrixMismatches(cases, CRAFT_MATRIX);
    expect(craftMismatch).toEqual([]);
    GUARDS.check("craftItem rank × rarity matrix: all 12 cells equal the source-derived expectation", craftMismatch.length === 0, craftMismatch);
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
