/**
 * FINAL Katana15 / Crystal10 on the actual engine with the approved
 * RUL-2026-10-11-006 timing: Consume rounds=2 and generated shieldRounds=2.
 * Every other Katana mechanical field is the accepted baseline. Synthetic
 * controls below are explicitly identified. Consume overlap is director-deferred;
 * it is observed here, not corrected or restricted.
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
  E.flush({ sourcePin: "585534d7eb21d6f0dd678d5c3eb92662f611d39b", timing: "rounds=2/shieldRounds=2 approved (RUL-2026-10-11-006)", buffPreventCarrier: SEAL });
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
  expect(result.added[0]!.rounds).toBe(2);
  E.check(name, result.added.length === 1 && result.added[0]!.power === Math.floor(damage * ratio) && result.added[0]!.rounds === 2, { damage, ratio, added: result.added });
};

describe("active Consume through real weapon assembly and actions", () => {
  it("is absent on equip, applies to the granting Pierce hit, then converts different actions in this and a later round", async () => {
    let b = await setup();
    expect(activeConsume(b)).toHaveLength(0);
    const first = act(b, W, katana()); b = first.b;
    checkConversion("Katana granting hit converts 15%", first, 0.15);
    expect(activeConsume(b).map((e: any) => [e.power, e.rounds])).toEqual([[15, 2]]);
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
    const withOwn = I.imbuableWeapon({ effects: [...I.imbuableWeapon().effects, ...I.parseTagsIndividually([{ type: "consume", power: 15, rounds: 2, shieldRounds: 2, target: "SELF" }])] });
    const own = act(await setup({ rows: [crystalRow(withOwn)] }), W, withOwn.id);
    checkConversion("one action: own SELF Consume15 wins over appended Crystal10", own, 0.15);
    expect(activeConsume(own.b)).toHaveLength(1);
    const weapon = I.imbuableWeapon();
    const double = act(await setup({ rows: [crystalRow(weapon, [I.crystalRecord(), I.crystalRecord("RARE", { id: "distinct-crystal-control" })])] }), W, weapon.id);
    checkConversion("one action: two distinct Crystal records still realize one SELF Consume10", double, 0.1);
    expect(activeConsume(double.b)).toHaveLength(1);
    // Same sourced weapon fields in two hands. At 3/3 (historical fcd79e5) the
    // second weapon, usable at +3 after the shared GCD, overlapped the first buff
    // (10+10 -> 20%). At the approved 2/2 the first buff is gone by +3.
    const w2 = I.imbuableWeapon({ id: "second-weapon-control" });
    const row2 = { ...crystalRow(w2), equipped: "HAND_2" };
    let b = await setup({ rows: [crystalRow(weapon), row2] });
    b = act(b, W, weapon.id).b;
    const secondAvailable: boolean[] = [];
    for (let i = 0; i < SHARED_COOLDOWN_ROUNDS; i++) {
      advance(b);
      secondAvailable.push(IB.actionList(b, W).some((a) => a.id === w2.id));
    }
    const firstBuffAtSecondCast = activeConsume(b).map((e: any) => e.rounds);
    const second = act(b, W, w2.id); b = second.b;
    checkConversion("2/2: second Crystal weapon at the earliest shared-GCD release converts 10%, not 20%", second, 0.1);
    const durations = activeConsume(b).map((e: any) => e.rounds).sort();
    expect(secondAvailable).toEqual([false, false, true]);
    expect(firstBuffAtSecondCast).toEqual([]);
    expect(durations).toEqual([2]);
    E.put("dedupeAndOverlap", { sameActionOwn: own.added, sameActionDoubleCrystal: double.added, secondWeaponAvailableAtPlus1to3: secondAvailable, firstBuffAtSecondCast, secondCast: second.added, activeDurations: durations, control: "two imbuable Flaming Sword carriers, second in HAND_2; overlap is director-deferred and not corrected" });
    E.check("2/2 observation: the shared Consume GCD (3 rounds) outlasts the 2-round buff, so two Crystal weapons cannot overlap item Consume through separate casts", JSON.stringify(secondAvailable) === JSON.stringify([false, false, true]) && firstBuffAtSecondCast.length === 0 && JSON.stringify(durations) === JSON.stringify([2]));
  });

  it("2/2: buff covers the cast round and two more; final eligible hit at +2, first ineligible at +3; each shield expires independently", async () => {
    let b = act(await setup(), W, katana()).b;
    const start = b.round;
    const timeline: any[] = [];
    let lastEligible: any = null;
    for (let offset = 0; offset <= 3; offset++) {
      timeline.push({ offset, round: b.round, consume: activeConsume(b).map((e: any) => e.rounds), shields: shieldRows(b).map((e) => e.rounds) });
      if (offset === 2) { lastEligible = act(b, W, CUT); b = lastEligible.b; }
      if (offset < 3) advance(b);
    }
    // Buff: 2 in the cast round and +1, 1 at +2, gone at +3. Granting shield: same.
    expect(timeline.map((r) => r.round)).toEqual([0, 1, 2, 3].map((v) => start + v));
    expect(timeline.map((r) => r.consume)).toEqual([[2], [2], [1], []]);
    expect(timeline.map((r) => r.shields)).toEqual([[2], [2], [1], [2]]);
    checkConversion("final eligible hit: a different action at +2 (last active round) converts 15%", lastEligible, 0.15);
    const firstIneligible = act(b, W, QUICK); b = firstIneligible.b;
    expect(firstIneligible.lost[T]).toBeGreaterThan(0);
    expect(firstIneligible.added).toHaveLength(0);
    // The shield earned at +2 outlives the buff: 2 at +3, 1 at +4, gone at +5.
    const late: any[] = [{ offset: b.round - start, rounds: shieldRows(b).map((e) => e.rounds) }];
    for (let i = 0; i < 2; i++) { advance(b); late.push({ offset: b.round - start, rounds: shieldRows(b).map((e) => e.rounds) }); }
    expect(late).toEqual([{ offset: 3, rounds: [2] }, { offset: 4, rounds: [1] }, { offset: 5, rounds: [] }]);
    E.put("separateLifetimes2x2", { timeline, lastEligible: lastEligible.added, firstIneligible: { damage: firstIneligible.lost[T], added: firstIneligible.added }, lateShieldTimeline: late });
    E.check("buff present at offsets 0..2 (rounds 2,2,1) and gone at +3", JSON.stringify(timeline.map((r) => r.consume)) === JSON.stringify([[2], [2], [1], []]));
    E.check("granting-hit shield present at offsets 0..2 (rounds 2,2,1) and gone at +3", JSON.stringify(timeline.slice(0, 3).map((r) => r.shields)) === JSON.stringify([[2], [2], [1]]));
    E.check("first ineligible hit at +3 deals damage but earns no shield", firstIneligible.lost[T] > 0 && firstIneligible.added.length === 0, firstIneligible.lost[T]);
    E.check("shield earned at +2 survives the buff: rounds 2 at +3, 1 at +4, gone at +5", JSON.stringify(late) === JSON.stringify([{ offset: 3, rounds: [2] }, { offset: 4, rounds: [1] }, { offset: 5, rounds: [] }]), late);
  });

  it("2/2 Crystal on an imbued weapon follows the same buff and shield lifetimes", async () => {
    const weapon = I.imbuableWeapon();
    let b = await setup({ rows: [crystalRow(weapon)] });
    const first = act(b, W, weapon.id); b = first.b;
    checkConversion("Crystal granting hit converts 10% with a 2-round shield", first, 0.1);
    const life: any[] = [];
    for (let offset = 0; offset <= 3; offset++) {
      life.push({ offset, consume: activeConsume(b).map((e: any) => e.rounds), shields: shieldRows(b).map((e) => e.rounds) });
      if (offset < 3) advance(b);
    }
    expect(life.map((r) => r.consume)).toEqual([[2], [2], [1], []]);
    expect(life.map((r) => r.shields)).toEqual([[2], [2], [1], []]);
    E.put("crystalLifetimes2x2", life);
    E.check("Crystal buff and granting shield both present at offsets 0..2 and gone at +3", JSON.stringify(life.map((r) => [r.consume, r.shields])) === JSON.stringify([[[2], [2]], [[2], [2]], [[1], [1]], [[], []]]), life);
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
