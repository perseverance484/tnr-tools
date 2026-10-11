/**
 * Gates B1–B3: Skyglass Crystal (WEAPON-only CRYSTAL, Consume 20% only).
 *
 * B1  Consume-only array through the real item effects schema → expected rejection.
 * B2  Real battle assembly (processUsersForBattle) composing weapon + imbuement
 *     effects, then the weapon action through performBattleAction: shield size
 *     and basis, shielded/multi-target cases, stacking, no-damage recipient.
 *     The Crystal record is HYPOTHETICAL (it cannot pass B1); B2 proves
 *     post-composition runtime only, never production validity.
 * B3  Real occupation.imbueItem / craftItem procedures with read-only stubs
 *     (every write is trapped) for the guard paths; battle-side suppression of
 *     imbuements on canBeImbued:false items; rank/rarity tables from constants.
 */
import { afterAll, beforeEach, describe, expect, it } from "bun:test";
import {
  CRAFTING_MAX_IMBUED_ITEMS,
  CRAFTING_RANKS,
  CRAFTING_REQUIRED_EXP,
  CRAFTING_TIMES_MINS,
  ItemRarities,
} from "@/drizzle/constants";
import { occupationRouter } from "@/server/api/routers/occupation";
import { getCraftingRank, getEffectiveMaxImbuements } from "@/libs/crafting";
import { resetServerModuleStubs, stubProfile } from "../setup/serverModules";
import * as I from "./lib/items";
import * as IB from "./lib/itembattle";
import { Evidence } from "./lib/report";
import { mulberry32 } from "./lib/sim";

// Seed Math.random per test (initiative rolls, prevent/stun rolls) for reproducible evidence.
const realRandom = Math.random;
beforeEach(() => {
  Math.random = mulberry32(2101);
});
afterAll(() => {
  Math.random = realRandom;
});

const B1 = new Evidence("B1");
const B2 = new Evidence("B2");
const B3 = new Evidence("B3");
afterAll(() => {
  B1.flush({ productionStatus: "BLOCKED: Consume-only Crystal cannot pass the item validator at the pin" });
  B2.flush({ scope: "post-composition runtime with a hypothetical (validator-rejected) Crystal record" });
  B3.flush();
});

const CONSUME_MSG = "ConsumeTag must be used together with a damage or pierce effect on the same action";

describe("B1 — Consume-only Crystal through the real item effects schema", () => {
  it("rejects [consume 20%] with the companion-tag issue", () => {
    const r = I.parseItemEffects(I.CRYSTAL_EFFECTS_INPUT());
    const iss = I.issues(r);
    B1.put("crystalEffectsInput", I.CRYSTAL_EFFECTS_INPUT());
    B1.put("effectsSchemaResult", { success: r.success, issues: iss });
    expect(r.success).toBe(false);
    expect(iss.map((i: any) => i.message)).toEqual([CONSUME_MSG]);
    B1.check("Consume-only array rejected with exactly the companion issue", !r.success && iss.length === 1 && iss[0].message === CONSUME_MSG, iss);
  });

  it("the single consume tag is itself well-formed (rejection is the cross-tag rule)", () => {
    const [tag] = I.parseTagsIndividually(I.CRYSTAL_EFFECTS_INPUT());
    B1.put("consumeTagParsedAlone", tag);
    expect(tag.type).toBe("consume");
    expect(tag.power).toBe(20);
    expect(tag.shieldRounds).toBe(3);
    B1.check("consume tag parses alone; shieldRounds defaults to 3", tag.power === 20 && tag.shieldRounds === 3 && tag.target === "SELF");
  });

  it("controls: adding Damage or Pierce to the same array passes; Vamp/Wound share the rule", () => {
    const withDamage = I.parseItemEffects([...I.CRYSTAL_EFFECTS_INPUT(), { type: "damage", power: 1, calculation: "static" }]);
    const withPierce = I.parseItemEffects([...I.CRYSTAL_EFFECTS_INPUT(), { type: "pierce", power: 1, calculation: "static" }]);
    const vampOnly = I.parseItemEffects([{ type: "vamp", power: 20 }]);
    const woundOnly = I.parseItemEffects([{ type: "wound", power: 20, rounds: 2 }]);
    const res = {
      withDamage: withDamage.success, withPierce: withPierce.success,
      vampOnly: I.issues(vampOnly), woundOnly: I.issues(woundOnly),
    };
    B1.put("controls", res);
    expect(withDamage.success).toBe(true);
    expect(withPierce.success).toBe(true);
    expect(vampOnly.success).toBe(false);
    expect(woundOnly.success).toBe(false);
    B1.check("companion rule is generic across Consume/Vamp/Wound (any correction must stay context-scoped)", withDamage.success && withPierce.success && !vampOnly.success && !woundOnly.success, res);
  });

  it("the full ItemValidator on the hypothetical Crystal record reports the same issue", () => {
    const rec = { ...I.crystalRecord("RARE"), effects: I.CRYSTAL_EFFECTS_INPUT() };
    const r = I.validateItem(rec);
    const iss = I.issues(r);
    B1.put("fullItemValidatorOnCarrierCrystal", { success: r.success, issues: iss, carrierNote: "non-effect fields from Flaming Sword carrier; unselected" });
    expect(r.success).toBe(false);
    expect(iss.some((i: any) => i.message === CONSUME_MSG && i.path.startsWith("effects"))).toBe(true);
    B1.check("full validator also rejects at path effects", iss.some((i: any) => i.message === CONSUME_MSG));
  });
});

describe("B2 — weapon + Crystal composition and Consume 20% runtime", () => {
  const W = "user_wielder";
  const T1 = "user_target1";
  const T2 = "user_target2";

  const crystalOn = (weapon: any, crystals: any[]) => {
    const row = I.userItemRow(W, weapon);
    row.imbuements = crystals.map((c) => I.imbuementRow(row.id, c));
    return row;
  };
  const fight = async (weapon: any, crystals: any[], opts: { targetShield?: boolean; twoTargets?: boolean } = {}) => {
    const users = [IB.wielder(W, [crystalOn(weapon, crystals)]), IB.target(T1, opts.targetShield ? [{ record: (await import("./lib/fixtures")).poolJutsuById("05rH3kZNXbtFq9a9iRl-W").record }] : [])];
    const placements = [{ userId: W, x: 2, y: 4 }, { userId: T1, x: 4, y: 4 }];
    if (opts.twoTargets) {
      users.push(IB.target(T2));
      placements.push({ userId: T2, x: 4, y: 5 });
    }
    let b = await IB.build(users, placements);
    const composed = (b.extraState.items as any)[weapon.id].effects.map((e: any) => [e.type, e.power, e.shieldRounds ?? null]);
    if (opts.targetShield) {
      const r = IB.act(b, T1, "05rH3kZNXbtFq9a9iRl-W", { x: 4, y: 4 });
      if (!r.ok) throw new Error(`target shield cast failed: ${r.reason}`);
      b = r.battle;
      IB.nextRound(b); // shield active from the next round
    }
    const hp0 = { t1: IB.hp(b, T1), t2: opts.twoTargets ? IB.hp(b, T2) : 0 };
    const shield0 = IB.shieldsOn(b, T1).reduce((s, e: any) => s + (e.power ?? 0), 0);
    const r = IB.act(b, W, weapon.id, { x: 4, y: 4 });
    if (!r.ok) throw new Error(`weapon action failed: ${r.reason}`);
    b = r.battle;
    const lost = { t1: hp0.t1 - IB.hp(b, T1), t2: opts.twoTargets ? hp0.t2 - IB.hp(b, T2) : 0 };
    const shield = IB.shieldsOn(b, W).filter((e) => e.creatorId === IB.uid(b, W));
    return { b, composed, lost, shield0, shield: shield.map((e: any) => ({ power: e.power, rounds: e.rounds, isNew: e.isNew })), texts: r.effects.map((e) => e.txt) };
  };

  it("composes weapon effects + Crystal consume in battle assembly and generates a 20% shield", async () => {
    const res = await fight(I.imbuableWeapon(), [I.crystalRecord()]);
    B2.put("singleTarget", { composed: res.composed, lost: res.lost, shield: res.shield, texts: res.texts });
    const total = res.lost.t1;
    expect(res.composed.map((c: any) => c[0])).toEqual(["damage", "afterburn", "consume"]);
    expect(res.shield).toHaveLength(1);
    expect(res.shield[0]!.power).toBe(Math.floor(total * 0.2));
    expect(res.shield[0]!.rounds).toBe(3);
    B2.check("assembly composes [...weapon effects, consume20]", JSON.stringify(res.composed.map((c: any) => c[0])) === JSON.stringify(["damage", "afterburn", "consume"]), res.composed);
    B2.check("shield = floor(20% × damage) for 3 rounds", res.shield[0]?.power === Math.floor(total * 0.2) && res.shield[0]?.rounds === 3, { damage: total, shield: res.shield });
  });

  it("sizes the shield from pre-shield damage against a shielded target", async () => {
    const ref = await fight(I.imbuableWeapon(), [I.crystalRecord()]);
    const sh = await fight(I.imbuableWeapon(), [I.crystalRecord()], { targetShield: true });
    B2.put("shieldedTarget", { targetShieldBefore: sh.shield0, hpLost: sh.lost.t1, consumeShield: sh.shield, referenceHpLost: ref.lost.t1, referenceShield: ref.shield });
    expect(sh.shield0).toBeGreaterThan(0);
    expect(sh.lost.t1).toBeLessThan(ref.lost.t1);
    expect(sh.shield[0]!.power).toBe(ref.shield[0]!.power);
    B2.check("target shield absorbed damage but Consume shield unchanged (pre-shield basis)", sh.lost.t1 < ref.lost.t1 && sh.shield[0]?.power === ref.shield[0]?.power, { shieldedHpLost: sh.lost.t1, refHpLost: ref.lost.t1 });
  });

  it("aggregates multiple targets into one shield (ALL-method carrier override)", async () => {
    const res = await fight(I.imbuableWeapon({ method: "ALL" }), [I.crystalRecord()], { twoTargets: true });
    const total = res.lost.t1 + res.lost.t2;
    B2.put("multiTarget", { lost: res.lost, shield: res.shield, carrierNote: "method ALL override on carrier; Katana/Crystal recipients are not assumed ALL" });
    expect(res.lost.t1).toBeGreaterThan(0);
    expect(res.lost.t2).toBeGreaterThan(0);
    expect(res.shield).toHaveLength(1);
    expect(Math.abs(res.shield[0]!.power - Math.floor(total * 0.2))).toBeLessThanOrEqual(1);
    B2.check("one aggregated shield ≈ floor(20% × summed damage)", res.shield.length === 1 && Math.abs(res.shield[0]!.power - Math.floor(total * 0.2)) <= 1, { total, shield: res.shield });
  });

  it("does NOT stack a second SELF Consume on the same action (insertAction stack-key dedupe)", async () => {
    // insertAction realises SELF-target tags once per stack key
    // `${type}-${creatorId}-${targetId}-${fromType}`; the composed array is
    // [...weapon effects, ...imbuement effects], so the FIRST Consume wins.
    const weapon = I.imbuableWeapon({ effects: [...I.imbuableWeapon().effects, { type: "consume", power: 40, calculation: "percentage", target: "SELF", shieldRounds: 3, rounds: 0, powerPerLevel: 0 }] });
    const res = await fight(weapon, [I.crystalRecord()]);
    const twoCrystals = await fight(I.imbuableWeapon(), [I.crystalRecord(), { ...I.crystalRecord(), id: "harness-skyglass-crystal-2" }]);
    B2.put("stacking", {
      weaponConsume40PlusCrystal20: { lost: res.lost, shield: res.shield, observedRatio: res.shield[0] ? res.shield[0].power / res.lost.t1 : null, finding: "Crystal Consume dropped; weapon's own Consume 40 applies alone" },
      twoCrystalRecordsAtRuntime: { lost: twoCrystals.lost, shield: twoCrystals.shield, observedRatio: twoCrystals.shield[0] ? twoCrystals.shield[0].power / twoCrystals.lost.t1 : null, finding: "second Consume dropped; 20% only" },
      source: "app/src/libs/combat/actions.ts insertAction SELF branch (getEffectStackKey dedupe); tags.ts consume() additive ratio is only reachable across distinct stack keys",
    });
    expect(res.shield[0]!.power).toBe(Math.floor(res.lost.t1 * 0.4));
    expect(twoCrystals.shield[0]!.power).toBe(Math.floor(twoCrystals.lost.t1 * 0.2));
    B2.check("FINDING: weapon Consume40 + Crystal Consume20 on one action → 40% (Crystal Consume silently dropped)", res.shield[0]?.power === Math.floor(res.lost.t1 * 0.4));
    B2.check("FINDING: two Crystal Consume records on one weapon → 20% (no runtime stacking)", twoCrystals.shield[0]?.power === Math.floor(twoCrystals.lost.t1 * 0.2));
  });

  it("generates no shield on a recipient weapon without a cast-round Damage/Pierce", async () => {
    const afterburnOnly = I.imbuableWeapon({ id: "harness-afterburn-only", effects: I.imbuableWeapon().effects.filter((e: any) => e.type !== "damage") });
    const res = await fight(afterburnOnly, [I.crystalRecord()]);
    B2.put("noDamageRecipient", { composed: res.composed, lost: res.lost, shield: res.shield, texts: res.texts });
    expect(res.shield).toHaveLength(0);
    B2.check("no positive cast-round outgoing damage → no Consume shield", res.shield.length === 0, res);
  });
});

describe("B3 — WEAPON restriction, recipient eligibility, duplicates, rank", () => {
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

  it("imbueItem guard matrix (real procedure, read-only stub)", async () => {
    const crystal = I.crystalRecord("RARE");
    const sword = I.imbuableWeapon();
    const sword3 = I.imbuableWeapon({ maxImbueNumber: 3 });
    const cRow = rowFor(crystal);
    const sRow = rowFor(sword);
    const cases: Record<string, any> = {};
    cases.eligibleWeapon = await call(mkUser(), [sRow, cRow], { userItemId: sRow.id, userCrystalItemId: cRow.id });
    const katana = I.katanaRecord();
    const kRow = rowFor(katana);
    cases.katanaNonImbuable = await call(mkUser(), [kRow, cRow], { userItemId: kRow.id, userCrystalItemId: cRow.id });
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
    cases.equippedRecipient = await call(mkUser(), [{ ...sRow, equipped: "HAND_1" }, cRow], { userItemId: sRow.id, userCrystalItemId: cRow.id });
    for (const occ of [null, "GATHERING", "HUNTING"]) cases[`occupation_${occ}`] = await call(mkUser({ occupation: occ }), [sRow, cRow], { userItemId: sRow.id, userCrystalItemId: cRow.id });
    for (const rank of CRAFTING_RANKS) {
      for (const rarity of ["RARE", "EPIC", "LEGENDARY"]) {
        const c = I.crystalRecord(rarity);
        const cr = rowFor(c);
        cases[`rank_${rank}_${rarity}`] = await call(mkUser({ craftingExperience: CRAFTING_REQUIRED_EXP[rank] }), [sRow, cr], { userItemId: sRow.id, userCrystalItemId: cr.id });
      }
    }
    B3.put("imbueItemGuards", cases);
    expect(cases.eligibleWeapon.outcome).toBe("guards-passed-reached-write");
    expect(cases.katanaNonImbuable.message).toBe("This item cannot be imbued");
    expect(cases.capturedFlamingSwordNonImbuable.message).toBe("This item cannot be imbued");
    expect(cases.armorRecipient.message).toBe("This crystal can only be applied to WEAPON items");
    expect(cases.duplicateCrystal.message).toContain("already has a");
    expect(cases.notACrystal.message).toBe("Selected item is not a crystal");
    expect(cases.equippedRecipient.message).toBe("You cannot imbue an equipped item");
    expect(cases.occupation_GATHERING.message).toBe("You must have the Crafting occupation to imbue items");
    B3.check("eligible imbuable WEAPON passes every guard (stops at first trapped write)", cases.eligibleWeapon.outcome === "guards-passed-reached-write", cases.eligibleWeapon);
    B3.check("Katana carrier (canBeImbued:false) rejected", cases.katanaNonImbuable.message === "This item cannot be imbued");
    B3.check("non-WEAPON recipient rejected by crystalTargetTypes", cases.armorRecipient.message === "This crystal can only be applied to WEAPON items");
    B3.check("duplicate crystal ID rejected", String(cases.duplicateCrystal.message).includes("already has a"));
    B3.check("non-CRAFTING occupations rejected (none/GATHERING/HUNTING)", ["occupation_null", "occupation_GATHERING", "occupation_HUNTING"].every((k) => cases[k].message === "You must have the Crafting occupation to imbue items"));
    B3.check("equipped recipient rejected", cases.equippedRecipient.message === "You cannot imbue an equipped item");
  });

  it("craftItem occupation and rarity/rank guards (real procedure, read-only stub)", async () => {
    const crystal = { ...I.crystalRecord("RARE"), canBeCrafted: true, hidden: false, parentItemId: null, craftingRequirements: [{ requirementItemId: "filament", quantity: 12, requirementItem: { id: "filament" } }] };
    const cases: Record<string, any> = {};
    for (const occ of ["CRAFTING", "GATHERING", "HUNTING", null]) cases[`occupation_${occ}`] = await call(mkUser({ occupation: occ }), [], { itemId: crystal.id, quantity: 1 }, "craftItem", crystal);
    for (const rank of CRAFTING_RANKS) for (const rarity of ["RARE", "EPIC", "LEGENDARY"]) {
      cases[`rank_${rank}_${rarity}`] = await call(mkUser({ craftingExperience: CRAFTING_REQUIRED_EXP[rank] }), [], { itemId: crystal.id, quantity: 1 }, "craftItem", { ...crystal, rarity });
    }
    B3.put("craftItemGuards", { note: "12 Filaments per Crystal used as the requirement carrier; inventory empty so eligible ranks stop at the material check", cases });
    expect(cases.occupation_GATHERING.message).toBe("You must have the Crafting occupation to craft items");
    B3.check("craftItem requires current CRAFTING occupation", ["occupation_GATHERING", "occupation_HUNTING", "occupation_null"].every((k) => cases[k].message === "You must have the Crafting occupation to craft items"), cases);
  });

  it("rank/rarity/imbue-slot tables from the pinned constants", () => {
    const table = CRAFTING_RANKS.map((rank) => ({
      rank, minExperience: CRAFTING_REQUIRED_EXP[rank], maxImbuedPerItemRankLimit: CRAFTING_MAX_IMBUED_ITEMS[rank],
      effectiveMaxImbuementsForMaxImbueNumber1: getEffectiveMaxImbuements(rank, 1),
      minutes: Object.fromEntries(ItemRarities.map((r) => [r, CRAFTING_TIMES_MINS[rank][r]])),
    }));
    B3.put("rankRarityTable", table);
    expect(getCraftingRank(CRAFTING_REQUIRED_EXP.MASTER)).toBe("MASTER");
    B3.check("Novice has zero imbuement slots", CRAFTING_MAX_IMBUED_ITEMS.NOVICE === 0);
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
    B3.put("battleSuppression", { katanaEffects: k, flamingSwordEffects: f });
    expect(k).toEqual(["pierce", "immunity", "consume"]);
    expect(f).toEqual(["damage", "afterburn"]);
    B3.check("legacy crystal effects dropped for canBeImbued:false items at assembly", JSON.stringify(k) === JSON.stringify(["pierce", "immunity", "consume"]) && !f.includes("consume"), { k, f });
  });
});
