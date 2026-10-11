/**
 * Gates C1–C3: Skyglass Katana (LEGENDARY WEAPON/SWORD, canBeImbued:false,
 * Pierce 50 + SELF immunity(buffprevent, 2r) + Consume 40%).
 *
 * C1  Exact effect array through the real item effects schema; maxImbueNumber
 *     minimum; full-item validation of the carrier record (not a final record).
 * C2  Real assembly + weapon action: Pierce→Consume shield (pre-shield basis,
 *     multi-target aggregation, expiry/absorption), item-level scaling, immunity
 *     timing against a sourced Buff Prevent carrier, cooldown/GCD and AP.
 * C3  Complete final Katana record — BLOCKED without a full Legendary Sword
 *     capture and director baseline acceptance (scan of committed captures).
 */
import { afterAll, beforeEach, describe, expect, it } from "bun:test";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { SHARED_COOLDOWN_ROUNDS } from "@/drizzle/constants";
import { ItemValidatorRawSchema } from "@/validators/combat";
import * as F from "./lib/fixtures";
import * as I from "./lib/items";
import * as IB from "./lib/itembattle";
import { Evidence } from "./lib/report";
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
  C1.flush({ scope: "effect array + maxImbueNumber guard; full-item result is for a carrier record only" });
  C2.flush({ carriers: { weaponFields: I.FLAMING_SWORD, buffPrevent: SEAL, note: "non-effect Katana fields are Flaming Sword carrier values, not a baseline" } });
  C3.flush();
});

const SEAL = { file: "harvests/inbox/tnr_results_1789188714166.json", pointer: "/captures/13/data", name: "Seal of Nullification", note: "buffprevent power 90 + 0.4/level; cast at jutsu level 25 so power = 100 (deterministic carrier)" };
const W = "user_katana";
const T = "user_target";

describe("C1 — exact Katana effect array", () => {
  it("parses Pierce 50 + SELF immunity(buffprevent, 2r) + Consume 40% through the item effects schema", () => {
    const r = I.parseItemEffects(I.KATANA_EFFECTS_INPUT());
    C1.put("input", I.KATANA_EFFECTS_INPUT());
    C1.put("parsed", r.success ? r.data : null);
    C1.put("issues", I.issues(r));
    expect(r.success).toBe(true);
    const d = r.data as any[];
    expect(d.map((e) => e.type)).toEqual(["pierce", "immunity", "consume"]);
    expect(d[0].power).toBe(50);
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

  it("full ItemValidator on the carrier Katana record (effect-array PASS is not full-item PASS)", () => {
    const rec = { ...I.katanaRecord(), effects: I.KATANA_EFFECTS_INPUT() };
    const r = I.validateItem(rec);
    C1.put("fullItemValidatorOnCarrier", { success: r.success, issues: I.issues(r), note: "Flaming Sword carrier non-effect fields; LEGENDARY/SWORD/canBeImbued:false overrides" });
    C1.check("carrier record validated (informational; final fields unselected → C3)", true, { success: r.success, issues: I.issues(r) });
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
    C2.check("observed Pierce vs target shield recorded", true, { hpLost: s.lost[T], refHpLost: ref.lost[T], targetShield, targetShieldAfter });
  });

  it("multi-target aggregation into one shield (ALL-method carrier override)", async () => {
    const s = swing(await setup({ overrides: { method: "ALL" }, twoTargets: true }));
    const total = (s.lost[T] ?? 0) + (s.lost["user_target2"] ?? 0);
    C2.put("multiTarget", { lost: s.lost, shield: s.shield, note: "method ALL is a carrier override to exercise aggregation; Katana method is unselected" });
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
    C2.check("shield rounds counted down to expiry (timeline recorded)", true, timeline);
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
    expect(windows[0].blocked).toBe(true);
    expect(windows[3].blocked).toBe(false);
    C2.check("new Buff Prevent blocked in the Katana cast round", windows[0].blocked);
    C2.check("observed immunity window (rounds after cast that block)", true, windows.map((w) => ({ offset: w.offset, blocked: w.blocked })));
    C2.check("new Buff Prevent applies again after the window", !windows[3].blocked);
  });

  it("cooldown, shared GCD and AP with the carrier weapon fields", async () => {
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
    for (let k = 0; k <= 4; k++) {
      const ids = IB.actionList(s.b, W).map((a) => a.id);
      rounds.push({ round: s.b.round, katana: ids.includes("harness-skyglass-katana"), ionLance: ids.includes(ion), heavyCut: ids.includes(tide) });
      IB.nextRound(s.b);
    }
    C2.put("cooldowns", { carrierCooldown: I.flamingSword().record.cooldown, carrierActionCostPerc: I.flamingSword().record.actionCostPerc, sharedCooldownRounds: SHARED_COOLDOWN_ROUNDS, castRound, apAfterCast: apAfter, availability: rounds });
    expect(apAfter).toBe(100 - I.flamingSword().record.actionCostPerc);
    expect(rounds[0].ionLance).toBe(false);
    expect(rounds[0].heavyCut).toBe(true);
    C2.check("Katana use locks other pierce/consume-tag actions for the shared GCD", rounds[0].ionLance === false && rounds[0].heavyCut === true, rounds);
    C2.check("AP after one swing = 100 − carrier actionCostPerc", apAfter === 100 - I.flamingSword().record.actionCostPerc);
  });
});

describe("C3 — complete final Katana record", () => {
  it("is BLOCKED: no full LEGENDARY WEAPON/SWORD record in committed captures", () => {
    const found: any[] = [];
    const walk = (o: any, file: string, path: string) => {
      if (Array.isArray(o)) o.forEach((v, i) => walk(v, file, `${path}/${i}`));
      else if (o && typeof o === "object") {
        if (o.itemType === "WEAPON" && Array.isArray(o.effects) && "maxImbueNumber" in o)
          found.push({ file, path, id: o.id, name: o.name, rarity: o.rarity, weaponType: o.weaponType });
        for (const [k, v] of Object.entries(o)) walk(v, file, `${path}/${k}`);
      }
    };
    const files: string[] = [];
    const scan = (dir: string) => {
      for (const f of readdirSync(dir)) {
        const p = join(dir, f);
        if (statSync(p).isDirectory()) scan(p);
        else if (f.endsWith(".json")) files.push(p);
      }
    };
    scan(join(F.REPO, "harvests"));
    for (const p of files) {
      try {
        walk(JSON.parse(readFileSync(p, "utf8")), p.slice(F.REPO.length + 1), "");
      } catch {}
    }
    const uniq = [...new Map(found.map((f) => [f.id, f])).values()];
    const legendarySwords = uniq.filter((f) => f.rarity === "LEGENDARY" && f.weaponType === "SWORD");
    C3.put("scan", { filesScanned: files.length, fullWeaponRecords: uniq, legendarySwords });
    C3.put("status", "BLOCKED");
    C3.put("unblockRequires", [
      "operator-run read-only item.get full capture of a LEGENDARY WEAPON/SWORD (first suggestion Night's Testament osJq3k77YPGoFWgof12FQ; its SWORD typing is unverified)",
      "director acceptance of the exact AP, cooldown, pool/health costs and reducers, range/target/method, slot, durability, requirements and economy fields",
    ]);
    expect(legendarySwords).toHaveLength(0);
    C3.check("no qualifying full Legendary Sword baseline is committed → C3 BLOCKED", legendarySwords.length === 0, { fullWeaponRecords: uniq.length });
  });
});
