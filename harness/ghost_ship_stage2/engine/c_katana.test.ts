/**
 * Gates C1–C3: Skyglass Katana (LEGENDARY WEAPON/SWORD, canBeImbued:false,
 * Pierce 50 + SELF immunity(buffprevent, 2r) + Consume 40%).
 *
 * C1  Exact effect array through the real item effects schema; maxImbueNumber
 *     minimum; full-item validation of the accepted record.
 * C2  Real assembly + weapon action: Pierce→Consume shield (pre-shield basis,
 *     multi-target aggregation, expiry/absorption), item-level scaling, immunity
 *     timing against a sourced Buff Prevent carrier, cooldown/GCD and AP — all on
 *     the accepted record (RUL-2026-10-11-004, Night's Testament baseline).
 * C3  Complete final Katana record: every field equals the captured Night's
 *     Testament row except the ruling-cited overrides; full ItemValidator;
 *     contract invariants; presentation fields reported as pending.
 */
import { afterAll, beforeEach, describe, expect, it } from "bun:test";
import { SHARED_COOLDOWN_ROUNDS } from "@/drizzle/constants";
import { ItemValidatorRawSchema } from "@/validators/combat";
import * as F from "./lib/fixtures";
import * as I from "./lib/items";
import * as IB from "./lib/itembattle";
import { Evidence, requireClean } from "./lib/report";
import { mulberry32 } from "./lib/sim";

// Seed Math.random per test (initiative rolls, prevent/stun rolls) for reproducible evidence.
const realRandom = Math.random;
beforeEach(() => {
  Math.random = mulberry32(3101);
});
afterAll(() => {
  Math.random = realRandom;
});

const C1 = new Evidence("C1");
const C2 = new Evidence("C2");
const C3 = new Evidence("C3");
afterAll(() => {
  C1.flush({ scope: "accepted effect array + maxImbueNumber guard + full ItemValidator on the accepted record" });
  C2.flush({ katanaRecord: I.ACCEPTED_KATANA_PATH, carriers: { buffPrevent: SEAL }, note: "Katana fields are the accepted RUL-2026-10-11-004 record; presentation placeholders only" });
  C3.flush();
});

const SEAL = { file: "harvests/inbox/tnr_results_1789188714166.json", pointer: "/captures/13/data", name: "Seal of Nullification", note: "buffprevent power 90 + 0.4/level; cast at jutsu level 25 so power = 100 (deterministic carrier)" };
const W = "user_katana";
const T = "user_target";

describe("C1 — exact Katana effect array", () => {
  it("parses the accepted Pierce 50 (Crystal) + SELF immunity(buffprevent, 2r) + Consume 40% through the item effects schema", () => {
    const r = I.parseItemEffects(I.KATANA_EFFECTS_INPUT());
    C1.put("input", I.KATANA_EFFECTS_INPUT());
    C1.put("parsed", r.success ? r.data : null);
    C1.put("issues", I.issues(r));
    expect(r.success).toBe(true);
    const d = r.data as any[];
    expect(d.map((e) => e.type)).toEqual(["pierce", "immunity", "consume"]);
    expect(d[0].power).toBe(50);
    expect(d[0].elements).toEqual(["Crystal"]);
    expect(d[1]).toMatchObject({ blocks: "buffprevent", rounds: 2, target: "SELF" });
    expect(d[2]).toMatchObject({ power: 40, calculation: "percentage", target: "SELF", shieldRounds: 3, rounds: 0 });
    C1.check("exact three-effect array accepted (Pierce satisfies Consume's companion rule)", r.success && d.length === 3);
    C1.check("consume shieldRounds source default = 3; consume rounds normalised to 0", d[2].shieldRounds === 3 && d[2].rounds === 0);
  });

  it("maxImbueNumber minimum is 1; canBeImbued:false is the disabling field", () => {
    const s = ItemValidatorRawSchema.shape;
    const zero = s.maxImbueNumber.safeParse(0);
    const one = s.maxImbueNumber.safeParse(1);
    const cbi = s.canBeImbued.safeParse(false);
    C1.put("maxImbueNumber", { zero: I.issues(zero), oneAccepted: one.success, canBeImbuedFalseAccepted: cbi.success });
    expect(zero.success).toBe(false);
    expect(one.success).toBe(true);
    C1.check("maxImbueNumber 0 rejected, 1 accepted", !zero.success && one.success);
  });

  it("full ItemValidator accepts the accepted Katana record", () => {
    const rec = { ...I.katanaRecord(), effects: I.KATANA_EFFECTS_INPUT() };
    const r = I.validateItem(rec);
    C1.put("fullItemValidatorOnAccepted", { success: r.success, issues: I.issues(r), note: "presentation fields are labelled placeholders" });
    expect(r.success).toBe(true);
    C1.check("accepted record passes ItemValidator (base + item + economy refinements)", r.success, I.issues(r));
  });
});

describe("C2 — Pierce→Consume, immunity timing, cooldowns", () => {
  const katanaRow = (overrides: Record<string, unknown> = {}, extra: Record<string, unknown> = {}) =>
    I.userItemRow(W, I.katanaRecord(overrides), extra);
  const setup = async (opts: { overrides?: Record<string, unknown>; itemLevel?: number; targetJutsu?: any[]; twoTargets?: boolean; wielderJutsu?: string[]; wielderElement?: string } = {}) => {
    const w = IB.wielder(W, [katanaRow(opts.overrides, { level: opts.itemLevel ?? 1 })], opts.wielderJutsu ?? []);
    if (opts.wielderElement) w.primaryElement = opts.wielderElement;
    const users = [w, IB.target(T, opts.targetJutsu ?? [])];
    const placements = [{ userId: W, x: 2, y: 4 }, { userId: T, x: 4, y: 4 }];
    if (opts.twoTargets) {
      users.push(IB.target("user_target2"));
      placements.push({ userId: "user_target2", x: 4, y: 5 });
    }
    return IB.build(users, placements);
  };
  const swing = (b: any, at = { x: 4, y: 4 }) => {
    const hp0 = Object.fromEntries(b.usersState.map((u: any) => [u.controllerId, u.curHealth]));
    const r = IB.act(b, W, "harness-skyglass-katana", at);
    if (!r.ok) throw new Error(r.reason);
    const lost = Object.fromEntries(r.battle.usersState.map((u: any) => [u.controllerId, hp0[u.controllerId] - u.curHealth]));
    const shield = IB.shieldsOn(r.battle, W).filter((e: any) => e.creatorId === IB.uid(r.battle, W)).map((e: any) => ({ power: e.power, rounds: e.rounds }));
    const immunity = IB.effectsOn(r.battle, W, "immunity").map((e: any) => ({ blocks: e.blocks, rounds: e.rounds, castThisRound: e.castThisRound }));
    return { b: r.battle, lost, shield, immunity, texts: r.effects.map((e) => e.txt) };
  };

  it("single target: Pierce damage converts 40% into a 3-round self shield", async () => {
    const b = await setup();
    const s = swing(b);
    C2.put("singleTarget", { lost: s.lost, shield: s.shield, immunity: s.immunity, texts: s.texts });
    expect(s.lost[T]).toBeGreaterThan(0);
    expect(s.shield).toEqual([{ power: Math.floor(s.lost[T] * 0.4), rounds: 3 }]);
    expect(s.immunity).toEqual([{ blocks: "buffprevent", rounds: 2, castThisRound: true }]);
    C2.check("shield = floor(40% × Pierce damage), 3 rounds", s.shield[0]?.power === Math.floor(s.lost[T] * 0.4) && s.shield[0]?.rounds === 3, s);
    C2.check("SELF immunity(buffprevent) realised for 2 rounds on the wielder", s.immunity.length === 1 && s.immunity[0]!.rounds === 2);
  });

  it("shielded target: Pierce ignores the target shield; Consume basis is pre-shield damage", async () => {
    const lb = F.poolJutsuById("05rH3kZNXbtFq9a9iRl-W").record;
    const ref = swing(await setup());
    let b = await setup({ targetJutsu: [{ record: lb }] });
    const c = IB.act(b, T, lb.id, { x: 4, y: 4 });
    if (!c.ok) throw new Error(c.reason);
    b = c.battle;
    IB.nextRound(b);
    const targetShield = IB.shieldsOn(b, T).reduce((s: number, e: any) => s + e.power, 0);
    const s = swing(b);
    const targetShieldAfter = IB.shieldsOn(s.b, T).reduce((x: number, e: any) => x + e.power, 0);
    C2.put("shieldedTarget", { targetShieldBefore: targetShield, targetShieldAfter, hpLost: s.lost[T], consumeShield: s.shield, referenceHpLost: ref.lost[T], referenceShield: ref.shield });
    expect(targetShield).toBeGreaterThan(0);
    expect(s.shield[0]!.power).toBe(ref.shield[0]!.power);
    C2.check("Consume shield equals unshielded reference (pre-shield basis)", s.shield[0]?.power === ref.shield[0]?.power, { s: s.shield, ref: ref.shield });
    C2.check("Pierce ignores the target shield: HP loss equals the unshielded reference and the target shield is consumed", s.lost[T] === ref.lost[T] && targetShieldAfter < targetShield, { hpLost: s.lost[T], refHpLost: ref.lost[T], targetShield, targetShieldAfter });
  });

  it("multi-target aggregation into one shield (ALL-method control override)", async () => {
    const s = swing(await setup({ overrides: { method: "ALL" }, twoTargets: true }));
    const total = (s.lost[T] ?? 0) + (s.lost["user_target2"] ?? 0);
    C2.put("multiTarget", { lost: s.lost, shield: s.shield, note: "method ALL is a control override to exercise aggregation; the accepted Katana is SINGLE" });
    expect(s.lost["user_target2"]).toBeGreaterThan(0);
    expect(s.shield).toHaveLength(1);
    expect(Math.abs(s.shield[0]!.power - Math.floor(total * 0.4))).toBeLessThanOrEqual(1);
    C2.check("one aggregated shield ≈ floor(40% × summed damage)", s.shield.length === 1 && Math.abs(s.shield[0]!.power - Math.floor(total * 0.4)) <= 1, { total, shield: s.shield });
  });

  it("shield expiry and later absorption across rounds", async () => {
    const arc = F.poolJutsuById("I66lzvVHf8v4thxR6tEJn").record; // Cataclysm Fist 70, range 5, non-elemental
    const s = swing(await setup({ targetJutsu: [{ record: arc }] }));
    const b = s.b;
    const timeline: any[] = [{ round: b.round, shield: IB.shieldsOn(b, W).map((e: any) => ({ power: e.power, rounds: e.rounds })) }];
    IB.nextRound(b);
    const hpW0 = IB.hp(b, W);
    const shieldBefore = IB.shieldsOn(b, W).reduce((x: number, e: any) => x + e.power, 0);
    const hit = IB.act(b, T, arc.id, { x: 2, y: 4 });
    if (!hit.ok) throw new Error(hit.reason);
    const shieldAfterHit = IB.shieldsOn(hit.battle, W).reduce((x: number, e: any) => x + e.power, 0);
    const absorption = { round: hit.battle.round, wielderHpLost: hpW0 - IB.hp(hit.battle, W), shieldBefore, shieldAfterHit };
    for (let i = 0; i < 4; i++) {
      timeline.push({ round: hit.battle.round, shield: IB.shieldsOn(hit.battle, W).map((e: any) => ({ power: e.power, rounds: e.rounds, active: IB.active(e) })) });
      IB.nextRound(hit.battle);
    }
    C2.put("expiryAndAbsorption", { absorption, timeline });
    expect(shieldAfterHit).toBeLessThan(shieldBefore);
    C2.check("Consume shield absorbs subsequent incoming damage", shieldAfterHit < shieldBefore, absorption);
    // Exact expiry: cast round r (rounds 3), r+1 (3), r+2 (2), r+3 (1) present; gone from r+4.
    const shape = timeline.map((t: any) => ({ round: t.round, rounds: t.shield.map((x: any) => x.rounds) }));
    const r0 = timeline[0].round;
    const want = [{ round: r0, rounds: [3] }, { round: r0 + 1, rounds: [3] }, { round: r0 + 2, rounds: [2] }, { round: r0 + 3, rounds: [1] }, { round: r0 + 4, rounds: [] }];
    expect(shape).toEqual(want);
    C2.check("Consume shield present in the cast round and the next three rounds (rounds 3,3,2,1), gone from round +4", JSON.stringify(shape) === JSON.stringify(want), shape);
    C2.check("absorption leaves wielder HP unchanged", absorption.wielderHpLost === 0, absorption);
  });

  it("player item level does not scale Pierce when powerPerLevel is 0; item level path is live", async () => {
    const lvl1 = swing(await setup({ itemLevel: 1 }));
    const lvl50 = swing(await setup({ itemLevel: 50 }));
    const pplEffects = I.KATANA_EFFECTS_INPUT().map((e: any) => (e.type === "pierce" ? { ...e, powerPerLevel: 0.5 } : e));
    const parsedPpl = I.parseItemEffects(pplEffects);
    const ppl1 = swing(await setup({ overrides: { effects: parsedPpl.success ? parsedPpl.data : [] }, itemLevel: 1 }));
    const ppl50 = swing(await setup({ overrides: { effects: parsedPpl.success ? parsedPpl.data : [] }, itemLevel: 50 }));
    C2.put("itemLevelScaling", { ppl0: { level1: lvl1.lost[T], level50: lvl50.lost[T] }, ppl05Carrier: { level1: ppl1.lost[T], level50: ppl50.lost[T] }, source: "actions.ts userItemToAction: players use item level, AI uses character level" });
    expect(lvl1.lost[T]).toBe(lvl50.lost[T]);
    expect(ppl50.lost[T]).toBeGreaterThan(ppl1.lost[T]);
    C2.check("approved Katana (powerPerLevel 0): identical damage at item level 1 and 50", lvl1.lost[T] === lvl50.lost[T]);
    C2.check("control: powerPerLevel>0 carrier scales with player item level", ppl50.lost[T] > ppl1.lost[T]);
  });

  const sealRecord = () => F.captured(SEAL.file, SEAL.pointer).record;
  const castSeal = (b: any) => {
    const t = b.usersState.find((u: any) => u.controllerId === T);
    t.actionPoints = 100;
    for (const j of t.jutsus) j.lastUsedRound = -100;
    const r = IB.act(b, T, sealRecord().id, { x: 2, y: 4 });
    if (!r.ok) throw new Error(`seal cast failed: ${r.reason}`);
    const bp = IB.effectsOn(r.battle, W, "buffprevent").map((e: any) => ({ rounds: e.rounds, power: e.power, isNew: e.isNew, active: IB.active(e) }));
    return { b: r.battle, texts: r.effects.map((e) => e.txt), bp };
  };

  it("immunity: existing Buff Prevent is not cleared; new applications blocked only inside the window", async () => {
    // (a) Existing Buff Prevent survives the Katana cast.
    let b = await setup({ targetJutsu: [{ record: sealRecord(), level: 25 }] });
    const pre = castSeal(b);
    b = pre.b;
    IB.nextRound(b);
    const existingBefore = IB.effectsOn(b, W, "buffprevent").filter(IB.active).length;
    const s = swing(b);
    const existingAfter = IB.effectsOn(s.b, W, "buffprevent").filter(IB.active).map((e: any) => ({ rounds: e.rounds, power: e.power }));
    C2.put("immunityExisting", { existingBefore, existingAfterCast: existingAfter, castRoundTexts: pre.texts });
    expect(existingBefore).toBeGreaterThan(0);
    expect(existingAfter.length).toBe(existingBefore);
    C2.check("pre-existing Buff Prevent is not removed by the Katana's immunity", existingAfter.length === existingBefore && existingBefore > 0);

    // (b) Fresh Buff Prevent attempts in the cast round and each following round.
    const windows: any[] = [];
    for (let offset = 0; offset <= 3; offset++) {
      let bb = await setup({ targetJutsu: [{ record: sealRecord(), level: 25 }] });
      const castRound = bb.round;
      bb = swing(bb).b;
      for (let k = 0; k < offset; k++) IB.nextRound(bb);
      const imm = IB.effectsOn(bb, W, "immunity").map((e: any) => ({ rounds: e.rounds, castThisRound: e.castThisRound }));
      const r = castSeal(bb);
      const blocked = r.texts.some((t) => t.includes("immunity blocked"));
      windows.push({ katanaCastRound: castRound, attemptRound: r.b.round, offset, immunityBeforeAttempt: imm, blocked, buffPreventAfter: r.bp, texts: r.texts });
    }
    C2.put("immunityWindow", windows);
    const blockedPattern = windows.map((w) => w.blocked);
    const landedAfter = windows[3].buffPreventAfter.filter((e: any) => e.active && e.power === 100);
    expect(blockedPattern).toEqual([true, true, true, false]);
    expect(landedAfter.length).toBe(1);
    C2.check("immunity window: new Buff Prevent blocked at offsets 0/1/2, not at 3 ([true,true,true,false])", JSON.stringify(blockedPattern) === JSON.stringify([true, true, true, false]), windows.map((w) => ({ offset: w.offset, blocked: w.blocked })));
    C2.check("blocked attempts leave no Buff Prevent on the wielder", windows.slice(0, 3).every((w) => w.buffPreventAfter.length === 0), windows.slice(0, 3).map((w) => w.buffPreventAfter));
    C2.check("after the window (offset 3) the new Buff Prevent is applied and active (power 100)", landedAfter.length === 1, windows[3].buffPreventAfter);
  });

  it("cooldown, shared GCD and AP with the accepted fields", async () => {
    // Players need a matching element for elemental jutsu; the wielder is given
    // primaryElement Lightning (labelled fixture input) so Ion Lance is usable.
    const ion = "xGVqWSX93hXZgfmlKZODp"; // Ion Lance: pierce 60, Lightning (shares the pierce GCD tag)
    const tide = "Vo8N1luCT0p48y7JzKe84"; // Heavy Cut: damage 45, non-elemental (no shared tag)
    const b = await setup({ wielderJutsu: [ion, tide], wielderElement: "Lightning" });
    const castRound = b.round;
    const s = swing(b);
    const wu = s.b.usersState.find((u: any) => u.controllerId === W)!;
    const apAfter = wu.actionPoints;
    const rounds: any[] = [];
    for (let k = 0; k <= 6; k++) {
      const ids = IB.actionList(s.b, W).map((a) => a.id);
      rounds.push({ round: s.b.round, katana: ids.includes("harness-skyglass-katana"), ionLance: ids.includes(ion), heavyCut: ids.includes(tide) });
      IB.nextRound(s.b);
    }
    const K = I.acceptedKatana().record;
    C2.put("cooldowns", { cooldown: K.cooldown, actionCostPerc: K.actionCostPerc, sharedCooldownRounds: SHARED_COOLDOWN_ROUNDS, castRound, apAfterCast: apAfter, availability: rounds });
    const ionPattern = rounds.map((r) => r.ionLance);
    const katanaPattern = rounds.map((r) => r.katana);
    const wantIon = rounds.map((_, k) => k >= SHARED_COOLDOWN_ROUNDS);
    const wantKatana = rounds.map((_, k) => k >= K.cooldown);
    expect(apAfter).toBe(100 - K.actionCostPerc);
    expect(katanaPattern).toEqual(wantKatana);
    expect(ionPattern).toEqual(wantIon);
    expect(rounds.every((r) => r.heavyCut)).toBe(true);
    C2.check(`shared GCD: Ion Lance (pierce tag) locked for exactly ${SHARED_COOLDOWN_ROUNDS} rounds (cast round and the next two) and released from round +${SHARED_COOLDOWN_ROUNDS}`, JSON.stringify(ionPattern) === JSON.stringify(wantIon), rounds);
    C2.check("Heavy Cut (no shared tag) available in every round", rounds.every((r) => r.heavyCut), rounds);
    C2.check("AP after one swing = 100 − actionCostPerc (40)", apAfter === 100 - K.actionCostPerc);
    C2.check("Katana unavailable in the cast round and the next five, available again exactly cooldown (6) rounds after the swing", JSON.stringify(katanaPattern) === JSON.stringify(wantKatana), rounds);
  });
});

describe("C3 — complete final Katana record", () => {
  it("equals Night's Testament except ruling-cited overrides, validates, and keeps the contract", () => {
    const spec = I.acceptedKatana();
    const cap = F.captured(spec.baseline.capture, spec.baseline.pointer).record;
    const rec = spec.record;
    const overrides = Object.entries(spec.provenance).filter(([, p]: any) => p.source === "override").map(([k]) => k).sort();
    const fromBaseline = Object.keys(rec).filter((k) => !overrides.includes(k));
    const mismatched = fromBaseline.filter((k) => JSON.stringify(rec[k]) !== JSON.stringify(cap[k]));
    const missing = Object.keys(cap).filter((k) => !(k in rec) && !spec.droppedFields.includes(k));
    const full = I.validateItem({ ...rec, ...I.PRESENTATION_PLACEHOLDERS, effects: rec.effects });
    const e = rec.effects;
    const contract = {
      legendarySword: rec.itemType === "WEAPON" && rec.rarity === "LEGENDARY" && rec.weaponType === "SWORD",
      notImbuable: rec.canBeImbued === false && rec.maxImbueNumber >= 1,
      exactlyThreeEffects: e.map((x: any) => x.type).join(",") === "pierce,immunity,consume",
      pierce50Crystal: e[0].power === 50 && e[0].powerPerLevel === 0 && JSON.stringify(e[0].elements) === JSON.stringify(["Crystal"]),
      selfImmunityBuffPrevent2: e[1].blocks === "buffprevent" && e[1].rounds === 2 && e[1].target === "SELF",
      consume40Self: e[2].power === 40 && e[2].calculation === "percentage" && e[2].target === "SELF",
      dropOnly: rec.canBeCrafted === false && rec.craftingExperience === 0 && rec.inShop === false,
      tradable: rec.canBeTraded === true,
      createdHidden: rec.hidden === true,
    };
    const accepted = Object.fromEntries(["actionCostPerc", "cooldown", "range", "target", "method", "chakraCost", "staminaCost", "healthCost", "chakraCostReducePerLvl", "staminaCostReducePerLvl", "healthCostReducePerLvl", "slot", "maxDurability", "maxEquips", "requiredLevel", "battleUsageType", "cost", "repsCost", "seichiSilverCost", "inShop", "canBeTraded", "canBeCrafted", "canBeImbued", "maxImbueNumber", "stackSize", "xpToLevel"].map((k) => [k, rec[k]]));
    C3.put("baseline", spec.baseline);
    C3.put("overrides", Object.fromEntries(overrides.map((k) => [k, spec.provenance[k].why])));
    C3.put("acceptedFields", accepted);
    C3.put("presentationPending", spec.presentationPending);
    C3.put("fullItemValidator", { success: full.success, issues: I.issues(full) });
    C3.put("contract", contract);
    C3.put("status", "PASS (mechanics/economy); presentation fields pending separate acceptance");
    expect(mismatched).toEqual([]);
    expect(missing).toEqual([]);
    expect(full.success).toBe(true);
    C3.check("every non-override field equals the captured Night's Testament row", mismatched.length === 0 && missing.length === 0, { mismatched, missing });
    C3.check("overrides are exactly the ruling-cited set", JSON.stringify(overrides) === JSON.stringify(["battleDescription", "canBeCrafted", "canBeImbued", "craftingExperience", "description", "effects", "hidden", "image", "name"]), overrides);
    C3.check("complete record passes ItemValidator", full.success, I.issues(full));
    for (const [k, v] of Object.entries(contract)) C3.check(`contract: ${k}`, v as boolean);
  });
});

requireClean(C1, C2, C3);
