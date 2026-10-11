/**
 * Revised 15% Katana / 10% Crystal on the actual engine.
 * Consume rounds=3 and shieldRounds=3 are SOURCE-DEFAULT TEST CARRIERS,
 * not director-approved durations. Every other Katana mechanical field is the
 * accepted baseline. Synthetic controls below are explicitly identified.
 */
import { afterAll, beforeEach, describe, expect, it } from "bun:test";
import { SHARED_COOLDOWN_ROUNDS } from "@/drizzle/constants";
import { ActionNotPossibleError, availableUserActions } from "@/libs/combat/actions";
import { calcPoolCost } from "@/libs/combat/util";
import * as F from "./lib/fixtures";
import * as I from "./lib/items";
import * as IB from "./lib/itembattle";
import { Evidence, requireClean } from "./lib/report";
import { mulberry32 } from "./lib/sim";
import { registerProcessorProbes } from "./lib/consume_probes";

const E = new Evidence("ACTIVE");
const W = "user_wielder", T = "user_target";
const CUT = "Vo8N1luCT0p48y7JzKe84", QUICK = "FeYnH7BBw_usnc1K-TM-J";
const ION = "xGVqWSX93hXZgfmlKZODp", LIGHT = "05rH3kZNXbtFq9a9iRl-W";
const CLEAR = "JWZYiHKPNwYziWEFjw4Fn";
const SEAL = { file: "harvests/inbox/tnr_results_1789188714166.json", pointer: "/captures/13/data" };
const seal = () => F.captured(SEAL.file, SEAL.pointer).record;
const realRandom = Math.random;
beforeEach(() => { Math.random = mulberry32(151003); });
afterAll(() => {
  Math.random = realRandom;
  E.flush({ sourcePin: "585534d7eb21d6f0dd678d5c3eb92662f611d39b", durationScope: "rounds=3/shieldRounds=3 are source-default test carriers; final timing unselected", buffPreventCarrier: SEAL });
});

const who = (b: any, cid = W) => b.usersState.find((u: any) => u.controllerId === cid)!;
const activeConsume = (b: any, cid = W) => IB.effectsOn(b, cid, "consume").filter(IB.active);
const shieldRows = (b: any, cid = W) => IB.shieldsOn(b, cid).map((e: any) => ({ power: e.power, rounds: e.rounds }));
const crystalRow = (weapon: any, crystals = [I.crystalRecord()]) => {
  const row = I.userItemRow(W, weapon);
  row.imbuements = crystals.map((c) => I.imbuementRow(row.id, c));
  return row;
};
const setup = async (opts: { weapon?: any; rows?: any[]; targets?: { record: any; level?: number }[]; x?: number; twoTargets?: boolean; lightning?: boolean } = {}) => {
  const w = IB.wielder(W, opts.rows ?? [I.userItemRow(W, opts.weapon ?? I.katanaRecord())], [CUT, QUICK, ION]);
  if (opts.lightning) w.primaryElement = "Lightning";
  const users = [w, IB.target(T, opts.targets ?? [])];
  const placements = [{ userId: W, x: 2, y: 4 }, { userId: T, x: opts.x ?? 4, y: 4 }];
  if (opts.twoTargets) { users.push(IB.target("user_target2")); placements.push({ userId: "user_target2", x: 4, y: 5 }); }
  return IB.build(users, placements);
};
const act = (b: any, cid: string, id: string, at = { x: 4, y: 4 }) => {
  const hp = Object.fromEntries(b.usersState.map((u: any) => [u.controllerId, u.curHealth]));
  const oldShields = new Set(IB.shieldsOn(b, W).map((e) => e.id));
  const r = IB.act(b, cid, id, at);
  if (!r.ok) throw new Error(`${id}: ${r.reason}`);
  const lost = Object.fromEntries(r.battle.usersState.map((u: any) => [u.controllerId, hp[u.controllerId] - u.curHealth]));
  const added = IB.shieldsOn(r.battle, W).filter((e) => !oldShields.has(e.id)).map((e: any) => ({ power: e.power, rounds: e.rounds }));
  return { b: r.battle, lost, added, texts: r.effects.map((e) => e.txt) };
};
const advance = (b: any) => { const r = b.round; IB.nextRound(b); expect(b.round).toBe(r + 1); };
const katana = () => I.katanaRecord().id;
const checkConversion = (name: string, result: ReturnType<typeof act>, ratio: number, targetIds = [T]) => {
  const damage = targetIds.reduce((v, id) => v + result.lost[id], 0);
  expect(damage).toBeGreaterThan(0);
  expect(result.added).toHaveLength(1);
  expect(result.added[0]!.power).toBe(Math.floor(damage * ratio));
  expect(result.added[0]!.rounds).toBe(3);
  E.check(name, result.added.length === 1 && result.added[0]!.power === Math.floor(damage * ratio) && result.added[0]!.rounds === 3, { damage, ratio, added: result.added });
};

describe("active Consume through real weapon assembly and actions", () => {
  it("is absent on equip, applies to the granting Pierce hit, then converts different actions in this and a later round", async () => {
    let b = await setup();
    expect(activeConsume(b)).toHaveLength(0);
    const first = act(b, W, katana()); b = first.b;
    checkConversion("Katana granting hit converts 15%", first, 0.15);
    expect(activeConsume(b).map((e: any) => [e.power, e.rounds])).toEqual([[15, 3]]);
    const other = act(b, W, CUT); b = other.b;
    checkConversion("different action in the granting round converts 15%", other, 0.15);
    advance(b);
    const later = act(b, W, QUICK); b = later.b;
    checkConversion("different action in the next round converts 15%", later, 0.15);
    expect(IB.shieldsOn(b, W)).toHaveLength(3);
    E.put("activationAndLaterActions", { onEquipConsume: 0, first: first.added, sameRound: other.added, laterRound: later.added, finalShields: shieldRows(b) });
    E.check("weapon Consume activates on use, not merely equipping; earned shields stack", activeConsume(b).length === 1 && IB.shieldsOn(b, W).length === 3);
  });

  it("Crystal10 composes through battle assembly and can grant an active buff on a weapon without a damage tag", async () => {
    const weapon = I.imbuableWeapon();
    const b = await setup({ rows: [crystalRow(weapon)] });
    const composed = (b.extraState.items as any)[weapon.id].effects.map((e: any) => e.type);
    expect(composed).toEqual(["damage", "afterburn", "consume"]);
    const first = act(b, W, weapon.id);
    checkConversion("Crystal granting weapon hit converts 10%", first, 0.1);
    const empty = I.imbuableWeapon({ id: "active-no-hit-carrier", effects: [] });
    const noHit = act(await setup({ rows: [crystalRow(empty)] }), W, empty.id);
    expect(noHit.lost[T]).toBe(0);
    expect(noHit.added).toHaveLength(0);
    expect(activeConsume(noHit.b)).toHaveLength(1);
    const follow = act(noHit.b, W, CUT);
    checkConversion("no-hit recipient grants active Consume that converts a later action", follow, 0.1);
    E.put("crystalComposition", { composed, noHit: { damage: noHit.lost[T], newShields: noHit.added, activePower: activeConsume(noHit.b).map((e: any) => e.power) }, later: follow.added });
    E.check("active Crystal on a no-damage weapon is not inert after activation", noHit.added.length === 0 && follow.added.length === 1);
  });

  it("uses pre-shield damage for Crystal and Pierce and aggregates an ALL-method control", async () => {
    const weapon = I.imbuableWeapon();
    const ref = act(await setup({ rows: [crystalRow(weapon)] }), W, weapon.id);
    let b = await setup({ rows: [crystalRow(weapon)], targets: [{ record: F.poolJutsuById(LIGHT).record }] });
    b = act(b, T, LIGHT).b; advance(b);
    const shieldBefore = shieldRows(b, T);
    const sh = act(b, W, weapon.id);
    expect(shieldBefore.length).toBeGreaterThan(0);
    expect(sh.lost[T]).toBeLessThan(ref.lost[T]);
    expect(sh.added).toEqual(ref.added);
    E.check("Crystal conversion uses pre-shield damage", sh.lost[T] < ref.lost[T] && JSON.stringify(sh.added) === JSON.stringify(ref.added), { shieldBefore, referenceDamage: ref.lost[T], shieldedDamage: sh.lost[T], added: sh.added });
    const kRef = act(await setup(), W, katana());
    let kb = await setup({ targets: [{ record: F.poolJutsuById(LIGHT).record }] });
    kb = act(kb, T, LIGHT).b; advance(kb);
    const pierced = act(kb, W, katana());
    expect(pierced.lost[T]).toBe(kRef.lost[T]);
    expect(pierced.added).toEqual(kRef.added);
    expect(IB.shieldsOn(pierced.b, T)).toHaveLength(0);
    E.check("Katana Pierce destroys the target shield without reducing conversion", pierced.lost[T] === kRef.lost[T] && JSON.stringify(pierced.added) === JSON.stringify(kRef.added));
    const multi = act(await setup({ weapon: I.katanaRecord({ method: "ALL" }), twoTargets: true }), W, katana());
    checkConversion("ALL-method control aggregates two targets once", multi, 0.15, [T, "user_target2"]);
  });

  it("distinguishes same-action SELF dedupe from overlapping active item buffs", async () => {
    const withOwn = I.imbuableWeapon({ effects: [...I.imbuableWeapon().effects, ...I.parseTagsIndividually([{ type: "consume", power: 15, rounds: 3, shieldRounds: 3, target: "SELF" }])] });
    const own = act(await setup({ rows: [crystalRow(withOwn)] }), W, withOwn.id);
    checkConversion("one action: own SELF Consume15 wins over appended Crystal10", own, 0.15);
    expect(activeConsume(own.b)).toHaveLength(1);
    const weapon = I.imbuableWeapon();
    const double = act(await setup({ rows: [crystalRow(weapon, [I.crystalRecord(), I.crystalRecord("RARE", { id: "distinct-crystal-control" })])] }), W, weapon.id);
    checkConversion("one action: two distinct Crystal records still realize one SELF Consume10", double, 0.1);
    expect(activeConsume(double.b)).toHaveLength(1);
    // Same sourced weapon fields in two hands. Shared GCD lasts 3 rounds; the
    // unused second weapon can be used at +3 while the first buff has 1 round.
    const w2 = I.imbuableWeapon({ id: "second-weapon-control" });
    const row2 = { ...crystalRow(w2), equipped: "HAND_2" };
    let b = await setup({ rows: [crystalRow(weapon), row2] });
    b = act(b, W, weapon.id).b;
    for (let i = 0; i < SHARED_COOLDOWN_ROUNDS; i++) advance(b);
    const overlap = act(b, W, w2.id); b = overlap.b;
    checkConversion("separate casts: overlapping item Consume10 buffs convert 20%", overlap, 0.2);
    const durations = activeConsume(b).map((e: any) => e.rounds).sort();
    expect(durations).toEqual([1, 3]);
    E.put("dedupeAndOverlap", { sameActionOwn: own.added, sameActionDoubleCrystal: double.added, separateCast: overlap.added, activeDurations: durations, control: "two imbuable Flaming Sword carriers, second in HAND_2; captured cooldown4 unchanged" });
    E.check("reapplication adds independently timed active buffs rather than refreshing the first", JSON.stringify(durations) === JSON.stringify([1, 3]));
  });

  it("expires conversion independently of each earned shield; late shields survive the buff", async () => {
    let b = act(await setup(), W, katana()).b;
    const start = b.round;
    const timeline: any[] = [];
    for (let offset = 0; offset <= 4; offset++) {
      timeline.push({ offset, round: b.round, consume: activeConsume(b).map((e: any) => e.rounds), shields: shieldRows(b) });
      if (offset === 3) b = act(b, W, CUT).b;
      if (offset < 4) advance(b);
    }
    expect(timeline.map((r) => r.consume)).toEqual([[3], [3], [2], [1], []]);
    expect(timeline.map((r) => r.round)).toEqual([0, 1, 2, 3, 4].map((v) => start + v));
    expect(shieldRows(b).map((e) => e.rounds)).toEqual([3]);
    const after = act(b, W, QUICK); b = after.b;
    expect(after.lost[T]).toBeGreaterThan(0);
    expect(after.added).toHaveLength(0);
    const lateShieldTimeline = [{ offset: b.round - start, rounds: shieldRows(b).map((e) => e.rounds) }];
    for (let i = 0; i < 3; i++) { advance(b); lateShieldTimeline.push({ offset: b.round - start, rounds: shieldRows(b).map((e) => e.rounds) }); }
    expect(lateShieldTimeline).toEqual([{ offset: 4, rounds: [3] }, { offset: 5, rounds: [2] }, { offset: 6, rounds: [1] }, { offset: 7, rounds: [] }]);
    expect(IB.shieldsOn(b, W)).toHaveLength(0);
    E.put("separateLifetimes", { timeline, lateShieldTimeline, postExpiryDamage: after.lost[T], postExpiryAdded: after.added, finalRound: b.round, finalShields: shieldRows(b) });
    E.check("buff expires at +4; shield earned at +3 survives until +7; no conversion after buff expiry", activeConsume(b).length === 0 && after.added.length === 0 && IB.shieldsOn(b, W).length === 0);
  });
});

describe("removal, prevention and unchanged weapon action fields", () => {
  it("Clear removes active item Consume and stops subsequent conversion", async () => {
    let b = act(await setup({ targets: [{ record: F.poolJutsuById(CLEAR).record }] }), W, katana()).b;
    expect(activeConsume(b)).toHaveLength(1);
    const cleared = act(b, T, CLEAR, { x: 2, y: 4 }); b = cleared.b;
    expect(activeConsume(b)).toHaveLength(0);
    const follow = act(b, W, CUT);
    expect(follow.lost[T]).toBeGreaterThan(0);
    expect(follow.added).toHaveLength(0);
    E.check("Clear removes item-source active Consume; later hit grants no shield", activeConsume(follow.b).length === 0 && follow.added.length === 0, { clearTexts: cleared.texts, laterDamage: follow.lost[T] });
  });

  const castSeal = (b: any) => act(b, T, seal().id, { x: 2, y: 4 });
  it("preserves existing Buff Prevent and measures Consume under it; Katana immunity blocks only new applications inside its exact window", async () => {
    let b = await setup({ targets: [{ record: seal(), level: 25 }] });
    b = castSeal(b).b; advance(b);
    expect(IB.effectsOn(b, W, "buffprevent").filter(IB.active)).toHaveLength(1);
    const under = act(b, W, katana());
    expect(IB.effectsOn(under.b, W, "buffprevent").filter(IB.active)).toHaveLength(1);
    expect(activeConsume(under.b)).toHaveLength(1);
    checkConversion("source observation: existing Buff Prevent does not block Consume conversion", under, 0.15);
    const windows: any[] = [];
    for (let offset = 0; offset <= 3; offset++) {
      let q = act(await setup({ targets: [{ record: seal(), level: 25 }] }), W, katana()).b;
      for (let k = 0; k < offset; k++) advance(q);
      const r = castSeal(q);
      windows.push({ offset, blocked: r.texts.some((s) => s.includes("immunity blocked")), prevents: IB.effectsOn(r.b, W, "buffprevent").filter(IB.active).map((e: any) => e.power), consume: activeConsume(r.b).map((e: any) => ({ power: e.power, rounds: e.rounds })) });
    }
    expect(windows.map((w) => w.blocked)).toEqual([true, true, true, false]);
    expect(windows.map((w) => w.prevents)).toEqual([[], [], [], [100]]);
    E.put("buffPreventAndImmunity", { underExistingPrevent: { consume: activeConsume(under.b).map((e: any) => e.power), added: under.added }, windows });
    E.check("unchanged immunity blocks new Buff Prevent in cast round/+1/+2; power100 applies at +3", JSON.stringify(windows.map((w) => w.prevents)) === JSON.stringify([[], [], [], [100]]));
  });

  it("keeps accepted AP40, costs40/40/0, range4 OTHER_USER and cooldown6/shared-GCD3", async () => {
    let b = await setup({ lightning: true });
    const actor = who(b);
    const action = availableUserActions(b, actor.userId, true, true).find((a) => a.id === katana())!;
    const costs = calcPoolCost(action, b.usersEffects, actor);
    expect(costs).toMatchObject({ hpCost: 0, cpCost: 40, spCost: 40 });
    const before = { hp: actor.curHealth, cp: actor.curChakra, sp: actor.curStamina };
    b = act(b, W, katana()).b;
    const after = who(b);
    expect(after.actionPoints).toBe(60);
    expect([before.hp - after.curHealth, before.cp - after.curChakra, before.sp - after.curStamina]).toEqual([0, 40, 40]);
    const availability = [];
    for (let i = 0; i <= 6; i++) {
      const ids = IB.actionList(b, W).map((a) => a.id);
      availability.push({ offset: i, katana: ids.includes(katana()), ion: ids.includes(ION), cut: ids.includes(CUT) });
      if (i < 6) advance(b);
    }
    expect(availability.map((v) => v.katana)).toEqual([false, false, false, false, false, false, true]);
    expect(availability.map((v) => v.ion)).toEqual([false, false, false, true, true, true, true]);
    expect(availability.every((v) => v.cut)).toBe(true);
    const edge = act(await setup({ x: 6 }), W, katana(), { x: 6, y: 4 });
    expect(edge.lost[T]).toBeGreaterThan(0);
    const invalid: any[] = [];
    for (const [name, x, click] of [["beyond range", 7, 7], ["self target", 4, 2]] as const) {
      const q = await setup({ x });
      const beforeState = { hp: who(q).curHealth, cp: who(q).curChakra, sp: who(q).curStamina, ap: who(q).actionPoints, targetHp: who(q, T).curHealth };
      let rejected = false;
      try { const r = IB.act(q, W, katana(), { x: click, y: 4 }); rejected = !r.ok; } catch (e) { if (!(e instanceof ActionNotPossibleError)) throw e; rejected = true; }
      const afterState = { hp: who(q).curHealth, cp: who(q).curChakra, sp: who(q).curStamina, ap: who(q).actionPoints, targetHp: who(q, T).curHealth };
      expect(rejected).toBe(true);
      expect(afterState).toEqual(beforeState);
      invalid.push({ name, rejected, unchanged: JSON.stringify(beforeState) === JSON.stringify(afterState) });
    }
    E.put("acceptedActionFields", { costs, apAfter: 60, availability, range4Damage: edge.lost[T], invalid });
    E.check("accepted action costs/availability/targeting execute unchanged", invalid.every((v) => v.rejected && v.unchanged) && availability[6]!.katana && availability[3]!.ion);
  });
});

registerProcessorProbes(E);
requireClean(E);
