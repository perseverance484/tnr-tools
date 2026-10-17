/**
 * Crowned Captain active support (RUL-2026-10-11-007/008) on engine 585534d7.
 *
 * Approved constants: Second Wind on native health_below:40 (strictly below 40%
 * of effective max HP); Stolen Form when the selected opponent's summed IDG >= 71;
 * Rebounding Form in the regular rotation. The concrete candidate under test
 * (state/ghost_ship_skyglass_crowned_support_behavior.md) prepends
 *   1. S35 Second Wind   health_below 40 → SELF
 *   2. B07 Stolen Form   target_has_effect IDG >= 71 (CLOSEST_OPPONENT) + distance_lower_than 5 → same target
 *   3. Rebounding Form   no condition → SELF
 * to the prior candidate-remapped chain (includeDefaultRules unchanged). Order and
 * selector are the implementation candidate; measured balance is reported, not
 * accepted. The regular Captain is not touched. Selector effects are injected with
 * the upstream makeEffect helper; boundary HP/IDG values are synthetic inputs.
 */
import { afterAll, describe, expect, it } from "bun:test";
import { availableUserActions } from "@/libs/combat/actions";
import { performAIaction } from "@/libs/combat/ai_v2";
import { getBattleGrid, getEffectiveMaxPool } from "@/libs/combat/util";
import { AiRule } from "@/validators/ai";
import type { CompleteBattle, UserEffect } from "@/libs/combat/types";
import { makeEffect } from "../libs/combat/helpers/battleScenario";
import * as F from "./lib/fixtures";
import * as IB from "./lib/itembattle";
import * as S from "./lib/sim";
import { Evidence, requireClean } from "./lib/report";

const E = new Evidence("CROWNED");
afterAll(() => E.flush({
  sourcePin: "585534d7eb21d6f0dd678d5c3eb92662f611d39b",
  behaviour: "state/ghost_ship_skyglass_crowned_support_behavior.md",
  approved: "S35 health_below 40 (strict); B07 summed IDG >= 71; regular Reflect (RUL007/008)",
  candidate: "order Heal → Copy (CLOSEST_OPPONENT, distance_lower_than 5) → Reflect → prior remapped chain; not a final balance acceptance",
  dmgConfig: "engine source defaults",
}));

const CROWNED = F.entityByName("Crowned Captain");
const BOSS = CROWNED.aiId as string;
const S35 = "STu1VHNcfgeC3x-UiQDgt";
const B07 = "VuFuBtE7h5B1nnA2J1lFZ";
const REFLECT = "T3glZGcSd-jS8G-NB43GR";
const S31 = "1OhP0StX4VTsosWtCxhsG";
const SUPPORT = new Set([S35, B07, REFLECT]);
const CATACLYSM = "I66lzvVHf8v4thxR6tEJn";

const supportRules = () => [
  { conditions: [{ type: "health_below", value: 40, description: "" }], action: { type: "use_specific_jutsu", jutsuId: S35, target: "SELF", description: "" } },
  {
    conditions: [
      { type: "target_has_effect", effectType: "increasedamagegiven", target: "CLOSEST_OPPONENT", threshold: 71, description: "" },
      { type: "distance_lower_than", value: 5, target: "CLOSEST_OPPONENT", description: "" },
    ],
    action: { type: "use_specific_jutsu", jutsuId: B07, target: "CLOSEST_OPPONENT", description: "" },
  },
  { conditions: [], action: { type: "use_specific_jutsu", jutsuId: REFLECT, target: "SELF", description: "" } },
];
type Variant = "captured" | "dormant" | "support";
const profileFor = (v: Variant) => {
  if (v === "captured") return F.capturedRules(CROWNED);
  const base = F.remappedRules(CROWNED).profile;
  if (v === "dormant") return base;
  return { ...base, id: `${base.id}::support`, rules: [...supportRules(), ...base.rules] };
};
const bossFor = (v: Variant) => F.aiQueryUser(CROWNED, v === "captured" ? "captured" : "accepted", profileFor(v));

const quietPlayer = (id: string) => {
  const u = F.playerQueryUser(id, "jonin-cap-durable", "striker", { id: `policy::${id}`, userId: id, includeDefaultRules: false, rules: [] }, S.joninCaps());
  u.jutsus = [];
  return u;
};
const fx = (type: string, tag: Record<string, unknown>, meta: Record<string, unknown>) =>
  makeEffect(type as never, tag as never, { isNew: false, castThisRound: false, createdRound: 0, targetType: "user", fromType: "jutsu", ...meta } as never);

type Opp = { id: string; x: number; summonOf?: string; effects?: { type: string; tag: Record<string, unknown>; meta?: Record<string, unknown> }[] };
/** Crowned (support candidate unless stated) at (6,4) against the given opponents on row 4. */
const selector = async (opps: Opp[], opts: { variant?: Variant; hpPct?: number; bossEffects?: { type: string; tag: Record<string, unknown>; meta?: Record<string, unknown> }[] } = {}) => {
  const players = opps.filter((o) => !o.summonOf);
  const b = await S.assembleBattle({
    users: [...players.map((o) => quietPlayer(o.id)), bossFor(opts.variant ?? "support")],
    placements: [...players.map((o) => ({ userId: o.id, x: o.x, y: 4 })), { userId: BOSS, x: 6, y: 4 }],
    leftSideUserIds: players.map((o) => o.id),
  });
  for (const o of opps.filter((x) => x.summonOf)) {
    const owner = b.usersState.find((u) => u.controllerId === o.summonOf)!;
    const s = structuredClone(owner);
    Object.assign(s, { userId: o.id, username: o.id, controllerId: owner.userId, isSummon: true, isAi: true, isOriginal: false, longitude: o.x, latitude: 4, aiProfileId: "Default" });
    b.usersState.push(s);
  }
  const uid = (cid: string) => b.usersState.find((u) => u.controllerId === cid || u.userId === cid)!.userId;
  for (const o of opps) for (const [i, e] of (o.effects ?? []).entries()) {
    const t = uid(o.id);
    b.usersEffects.push(fx(e.type, e.tag, { id: `${e.type}-${o.id}-${i}`, creatorId: t, targetId: t, actionId: `harness-${e.type}`, ...e.meta }));
  }
  const boss = b.usersState.find((u) => u.controllerId === BOSS)!;
  for (const [i, e] of (opts.bossEffects ?? []).entries()) {
    b.usersEffects.push(fx(e.type, e.tag, { id: `boss-${e.type}-${i}`, creatorId: boss.userId, targetId: boss.userId, actionId: `harness-boss-${e.type}`, ...e.meta }));
  }
  if (opts.hpPct !== undefined) boss.curHealth = (getEffectiveMaxPool(boss, b.usersEffects, "Health") * opts.hpPct) / 100;
  b.activeUserId = boss.userId;
  return { b, boss, uid };
};
const decide = (b: CompleteBattle, bossId: string) => {
  const r = performAIaction(b, getBattleGrid(1, b), bossId);
  return { action: r.nextActionId ?? null, texts: r.nextActionEffects.map((e) => e.txt), battle: r.nextBattle };
};
const nameOf = (id: string | null) => ({ [S35]: "S35", [B07]: "B07", [REFLECT]: "Reflect", [S31]: "S31" } as Record<string, string>)[id ?? ""] ?? id;
const idg = (power: number, meta: Record<string, unknown> = {}, rounds = 3) => ({ type: "increasedamagegiven", tag: { power, rounds, calculation: "percentage", statTypes: ["Highest"], generalTypes: [] }, meta });
const copiedOnto = (b: CompleteBattle, bossId: string) =>
  b.usersEffects.filter((e) => e.targetId === bossId && e.creatorId === bossId && e.fromEffectId).map((e) => ({ type: e.type, power: e.power, rounds: e.rounds }));

describe("CROWNED — rule candidate and records", () => {
  it("support rules parse with the engine AiRule schema; techniques are the preserved captured records", () => {
    const parsed = supportRules().map((r) => AiRule.safeParse(r));
    const cap = F.capturedAi(CROWNED).record;
    const rec = (id: string) => cap.jutsus.find((uj: any) => uj.jutsuId === id)!.jutsu;
    const summary = [S35, B07, REFLECT].map((id) => { const j = rec(id); return { id, name: j.name, target: j.target, method: j.method, range: j.range, ap: j.actionCostPerc, cooldown: j.cooldown, costs: [j.chakraCost, j.staminaCost, j.healthCost], effects: j.effects.map((x: any) => [x.type, x.power, x.rounds, x.calculation]) }; });
    const accepted = bossFor("support").jutsus.map((uj: any) => uj.jutsuId);
    const base = F.remappedRules(CROWNED).profile;
    const support = profileFor("support");
    E.put("candidateRules", { support: supportRules(), parsed: parsed.map((p) => p.success), records: summary, acceptedKit: accepted, includeDefaultRules: support.includeDefaultRules, priorChainLength: base.rules.length });
    expect(parsed.every((p) => p.success)).toBe(true);
    E.check("all three support rules parse with the pinned AiRule schema (integer health value 40, IDG threshold 71)", parsed.every((p) => p.success));
    E.check("preserved records: S35 heal15% SELF AP40 CD6; B07 copy100 r3 range4 AP60 CD6; Reflect35 r2 SELF AP40 CD4 (fractional 0.05 pool costs kept)", JSON.stringify(summary.map((s) => [s.ap, s.cooldown, s.range, s.effects])) === JSON.stringify([[40, 6, 0, [["heal", 15, 0, "percentage"]]], [60, 6, 4, [["copy", 100, 3, "percentage"]]], [40, 4, 0, [["reflect", 35, 2, "percentage"]]]]) && summary[2]!.costs[0] === 0.05 && summary[2]!.costs[1] === 0.05, summary);
    E.check("all eleven accepted members kept and all three support techniques equipped", accepted.length === 11 && [S35, B07, REFLECT].every((id) => accepted.includes(id)), accepted);
    E.check("support profile = three support rules + the unchanged prior remapped chain and includeDefaultRules", support.rules.length === base.rules.length + 3 && JSON.stringify(support.rules.slice(3)) === JSON.stringify(base.rules) && support.includeDefaultRules === base.includeDefaultRules);
  });
});

describe("CROWNED — Second Wind at the strict 40% boundary", () => {
  it("39.9% and 20% heal; exactly 40% and 40.1% do not; heal is 15% of base max HP", async () => {
    const out: Record<string, any> = {};
    for (const pct of [39.9, 40, 40.1, 20]) {
      const { b, boss } = await selector([{ id: "user_p", x: 0 }], { hpPct: pct });
      const effMax = getEffectiveMaxPool(boss, b.usersEffects, "Health");
      const ratio = (boss.curHealth / effMax) * 100;
      const before = boss.curHealth;
      const d = decide(b, boss.userId);
      const after = d.battle.usersState.find((u) => u.userId === boss.userId)!.curHealth;
      out[String(pct)] = { action: nameOf(d.action), engineRatio: ratio, effectiveMax: effMax, baseMax: boss.maxHealth, healed: after - before };
    }
    E.put("healBoundary", out);
    expect(out["40"].engineRatio).toBe(40);
    expect(out["39.9"].action).toBe("S35");
    expect(out["40"].action).not.toBe("S35");
    E.check("exactly 40% (engine ratio === 40) does not heal; 40.1% does not heal", out["40"].engineRatio === 40 && out["40"].action !== "S35" && out["40.1"].action !== "S35", out);
    E.check("39.9% and 20% heal (strictly below 40)", out["39.9"].action === "S35" && out["20"].action === "S35", out);
    E.check("heal amount = 15% of base maxHealth (effective max equals base max for this profile)", [out["39.9"], out["20"]].every((r) => Math.abs(r.healed - 0.15 * r.baseMax) < 1e-6) && out["20"].effectiveMax === out["20"].baseMax, { at399: out["39.9"].healed, at20: out["20"].healed, baseMax: out["20"].baseMax });
  });

  it("cooldown, AP and Heal Prevent fall-through", async () => {
    const out: Record<string, any> = {};
    {
      const { b, boss } = await selector([{ id: "user_p", x: 0 }], { hpPct: 20 });
      boss.jutsus.find((j) => j.jutsuId === S35)!.lastUsedRound = b.round;
      out.onCooldown = nameOf(decide(b, boss.userId).action);
    }
    {
      const { b, boss } = await selector([{ id: "user_p", x: 0 }], { hpPct: 20 });
      boss.actionPoints = 30;
      out.ap30 = nameOf(decide(b, boss.userId).action);
    }
    {
      const { b, boss } = await selector([{ id: "user_p", x: 0 }], { hpPct: 20, bossEffects: [{ type: "healprevent", tag: { power: 100, rounds: 3, calculation: "static" } }] });
      const before = boss.curHealth;
      const d = decide(b, boss.userId);
      out.healPrevent = { action: nameOf(d.action), healed: d.battle.usersState.find((u) => u.userId === boss.userId)!.curHealth - before, texts: d.texts };
    }
    {
      // Heal then Reflect in the same round: 40 + 40 AP leaves 20, below any 60-AP attack.
      const { b, boss } = await selector([{ id: "user_p", x: 4 }], { hpPct: 20 });
      const seq: any[] = [];
      let cur = b;
      for (let i = 0; i < 3; i++) {
        const me = cur.usersState.find((u) => u.userId === boss.userId)!;
        if (cur.round !== b.round) break;
        const ap = me.actionPoints;
        const d = decide(cur, boss.userId);
        seq.push({ action: nameOf(d.action), apBefore: ap });
        cur = d.battle;
        if (!d.action || d.action === "wait") break;
      }
      out.sameRoundSequence = seq;
    }
    E.put("healFallthrough", out);
    expect(out.onCooldown).not.toBe("S35");
    E.check("S35 on cooldown at 20% HP falls through to the next rule", out.onCooldown !== "S35", out.onCooldown);
    E.check("30 AP left (S35 costs 40) falls through", out.ap30 !== "S35", out.ap30);
    E.check("Heal Prevent: the AI still selects S35 but no HP is restored (wasted action)", out.healPrevent.action === "S35" && out.healPrevent.healed === 0, out.healPrevent);
    E.check("low HP, no high IDG: Heal (40 AP) then Reflect (40 AP) in the same round", out.sameRoundSequence[0]?.action === "S35" && out.sameRoundSequence[1]?.action === "Reflect" && out.sameRoundSequence[1]?.apBefore === 60, out.sameRoundSequence);
  });
});

describe("CROWNED — Stolen Form trigger, copied effects and selector", () => {
  it("IDG 30/70/70.5 do not trigger; 71/90 trigger (inclusive integer threshold)", async () => {
    const out: Record<string, any> = {};
    for (const p of [30, 70, 70.5, 71, 90]) {
      const { b, boss } = await selector([{ id: "user_p", x: 3, effects: [idg(p)] }]);
      out[String(p)] = nameOf(decide(b, boss.userId).action);
    }
    E.put("copyThreshold", out);
    expect(out["71"]).toBe("B07");
    expect(out["70.5"]).not.toBe("B07");
    E.check("Copy at 71 and 90; not at 30, 70, 70.5", out["71"] === "B07" && out["90"] === "B07" && ["30", "70", "70.5"].every((k) => out[k] !== "B07"), out);
    E.check("below threshold the Reflect rule is next (no inherited condition)", ["30", "70", "70.5"].every((k) => out[k] === "Reflect"), out);
  });

  it("separates the trigger from what is actually copied", async () => {
    const out: Record<string, any> = {};
    const run = async (label: string, opp: Opp, bossEffects: any[] = []) => {
      const { b, boss, uid } = await selector([opp], { bossEffects });
      const targetBefore = b.usersEffects.filter((e) => e.targetId === uid(opp.id)).map((e) => ({ id: e.id, type: e.type, power: e.power, rounds: e.rounds, fromType: e.fromType }));
      const d = decide(b, boss.userId);
      // Every pre-existing opponent effect is still present (Copy does not remove). Powers are
      // recorded after the action too: effect processing stores DDT with a negative sign.
      const after = targetBefore.map((t) => d.battle.usersEffects.find((e) => e.id === t.id));
      const targetKept = after.every((e) => !!e);
      out[label] = { action: nameOf(d.action), sources: targetBefore, sourcesAfter: after.map((e) => e && { id: e.id, power: e.power, rounds: e.rounds }), copied: copiedOnto(d.battle, boss.userId), texts: d.texts, targetKept };
    };
    await run("broad", { id: "user_p", x: 3, effects: [idg(90), { type: "decreasedamagetaken", tag: { power: 40, rounds: 3, calculation: "percentage" } }, { type: "increasestat", tag: { power: 20, rounds: 3, calculation: "percentage", statTypes: ["Highest"], generalTypes: [] } }] });
    await run("summed40plus35", { id: "user_p", x: 3, effects: [idg(40), idg(35)] });
    await run("expiredRounds0", { id: "user_p", x: 3, effects: [idg(90, {}, 0)] });
    await run("protectedBloodline", { id: "user_p", x: 3, effects: [idg(90, { fromType: "bloodline" })] });
    await run("itemSource", { id: "user_p", x: 3, effects: [idg(90, { fromType: "item" })] });
    await run("buffPreventOnCaster", { id: "user_p", x: 3, effects: [idg(90)] }, [{ type: "buffprevent", tag: { power: 100, rounds: 3, calculation: "static" } }]);
    // Four active copied clones (fromEffectId) already held by the Captain fill COPY_MAX_TAGS.
    const held = ["increasedamagegiven", "decreasedamagetaken", "absorb", "shield"].map((t) => ({ type: t, tag: { power: 10, rounds: 3, calculation: t === "shield" ? "static" : "percentage" }, meta: { fromEffectId: `prior-${t}` } }));
    await run("copyBudgetFull", { id: "user_p", x: 3, effects: [idg(90), { type: "increaseheal", tag: { power: 30, rounds: 3 } }] }, held);
    E.put("copyOutcomes", out);
    expect(out.broad.copied.map((c: any) => c.type).sort()).toEqual(["decreasedamagetaken", "increasedamagegiven", "increasestat"]);
    E.check("Copy is broad: IDG, DDT and increasestat all cloned onto the Captain (rounds 3), and the opponent keeps them", JSON.stringify(out.broad.copied.map((c: any) => c.type).sort()) === JSON.stringify(["decreasedamagetaken", "increasedamagegiven", "increasestat"]) && out.broad.copied.every((c: any) => c.rounds === 3) && out.broad.targetKept, out.broad);
    E.check("summed IDG 40+35 = 75 triggers; one IDG (the strongest, 40) is copied, not the 75 sum", out.summed40plus35.action === "B07" && JSON.stringify(out.summed40plus35.copied) === JSON.stringify([{ type: "increasedamagegiven", power: 40, rounds: 3 }]), out.summed40plus35);
    E.check("fixture validity: the expired source IDG really has rounds 0; protected/item sources carry their fromType", out.expiredRounds0.sources[0]?.rounds === 0 && out.protectedBloodline.sources[0]?.fromType === "bloodline" && out.itemSource.sources[0]?.fromType === "item", { expired: out.expiredRounds0.sources, bloodline: out.protectedBloodline.sources, item: out.itemSource.sources });
    for (const k of ["expiredRounds0", "protectedBloodline", "itemSource"]) {
      E.check(`${k}: raw IDG 90 triggers B07 but nothing is copied (empty Copy)`, out[k].action === "B07" && out[k].copied.length === 0 && out[k].texts.some((t: string) => t.includes("finds no copyable effects")), out[k]);
    }
    E.check("Buff Prevent on the Captain: B07 cast, copy prevented, nothing copied", out.buffPreventOnCaster.action === "B07" && out.buffPreventOnCaster.copied.length === 0 && out.buffPreventOnCaster.texts.some((t: string) => t.includes("cannot copy effects")), out.buffPreventOnCaster);
    E.check("copy budget (4 active copied types) full: B07 cast, nothing new copied", out.copyBudgetFull.action === "B07" && out.copyBudgetFull.texts.some((t: string) => t.includes("already holding the maximum")) && out.copyBudgetFull.copied.length === 4, out.copyBudgetFull);
  });

  it("closest-opponent selector, summons, path distance and precedence over S31", async () => {
    const out: Record<string, any> = {};
    {
      const { b, boss } = await selector([{ id: "user_p", x: 3, effects: [idg(90)] }, { id: "summon_s", x: 4, summonOf: "user_p" }]);
      out.lowIdgSummonCloser = nameOf(decide(b, boss.userId).action);
    }
    {
      const { b, boss } = await selector([{ id: "user_p", x: 3 }, { id: "summon_s", x: 4, summonOf: "user_p", effects: [idg(90)] }]);
      const d = decide(b, boss.userId);
      out.buffedSummonCloser = { action: nameOf(d.action), copied: copiedOnto(d.battle, boss.userId).map((c) => c.type) };
    }
    for (const hex of [3, 4, 5]) {
      const { b, boss } = await selector([{ id: "user_p", x: 6 - hex, effects: [idg(90)] }]);
      out[`hex${hex}_path${hex + 1}`] = nameOf(decide(b, boss.userId).action);
    }
    for (const v of ["support", "dormant"] as const) {
      const { b, boss } = await selector([{ id: "user_p", x: 5, effects: [idg(90)] }], { variant: v });
      out[`adjacent_${v}`] = nameOf(decide(b, boss.userId).action);
    }
    E.put("copySelector", out);
    E.check("closest low-IDG summon blocks Copy even though a farther player has IDG 90", out.lowIdgSummonCloser !== "B07", out.lowIdgSummonCloser);
    E.check("buffed closest summon triggers Copy and is the copy source", out.buffedSummonCloser.action === "B07" && out.buffedSummonCloser.copied.includes("increasedamagegiven"), out.buffedSummonCloser);
    E.check("distance_lower_than 5 is path ≤ 5: Copy at hex 3 and 4 (path 4, 5), not at hex 5 (path 6)", out.hex3_path4 === "B07" && out.hex4_path5 === "B07" && out.hex5_path6 !== "B07", out);
    E.check("adjacent IDG 90 opponent: support candidate copies before Clear; the prior dormant chain uses S31", out.adjacent_support === "B07" && out.adjacent_dormant === "S31", { support: out.adjacent_support, dormant: out.adjacent_dormant });
  });
});

describe("CROWNED — regular Reflect", () => {
  it("activates at full HP near and far, returns damage without reducing it, expires, and respects cooldown and Buff Prevent", async () => {
    const out: Record<string, any> = {};
    for (const [label, x] of [["far_hex6", 0], ["near_hex2", 4]] as const) {
      const { b, boss } = await selector([{ id: "user_p", x }]);
      out[label] = nameOf(decide(b, boss.userId).action);
    }
    // Reflected damage vs a control without Reflect: the player hits the Captain the round after.
    const strike = async (withReflect: boolean, bossEffects: any[] = []) => {
      const pl = F.playerQueryUser("user_p", "jonin-cap", "striker", F.playerPolicy("user_p", "striker"), S.joninCaps());
      let b = await S.assembleBattle({ users: [pl, bossFor("support")], placements: [{ userId: "user_p", x: 4, y: 4 }, { userId: BOSS, x: 6, y: 4 }] });
      const boss = b.usersState.find((u) => u.controllerId === BOSS)!;
      for (const [i, e] of bossEffects.entries()) b.usersEffects.push(fx(e.type, e.tag, { id: `bp-${i}`, creatorId: boss.userId, targetId: boss.userId, actionId: "harness-bp" }));
      if (withReflect) { const r = IB.act(b, BOSS, REFLECT, { x: 6, y: 4 }); if (!r.ok) throw new Error(r.reason); b = r.battle; }
      IB.nextRound(b);
      const pHp = IB.hp(b, "user_p");
      const bHp = IB.hp(b, BOSS);
      const reflectRounds = IB.effectsOn(b, BOSS, "reflect").map((e: any) => e.rounds);
      const hit = IB.act(b, "user_p", CATACLYSM, { x: 6, y: 4 });
      if (!hit.ok) throw new Error(hit.reason);
      return { b: hit.battle, bossLost: bHp - IB.hp(hit.battle, BOSS), playerLost: pHp - IB.hp(hit.battle, "user_p"), reflectRounds, texts: hit.effects.map((e) => e.txt) };
    };
    const control = await strike(false);
    const reflected = await strike(true);
    const prevented = await strike(true, [{ type: "buffprevent", tag: { power: 100, rounds: 3, calculation: "static" } }]);
    out.control = { bossLost: control.bossLost, playerLost: control.playerLost };
    out.reflected = { bossLost: reflected.bossLost, playerLost: reflected.playerLost, reflectRounds: reflected.reflectRounds, texts: reflected.texts.filter((t) => t.includes("reflect")) };
    out.prevented = { bossLost: prevented.bossLost, playerLost: prevented.playerLost, texts: prevented.texts.filter((t) => t.includes("reflect") || t.includes("cannot be buffed")) };
    // Expiry and cooldown on the support Captain after a cast.
    {
      const { b, boss } = await selector([{ id: "user_p", x: 0 }]);
      const r = IB.act(b, BOSS, REFLECT, { x: 6, y: 4 });
      if (!r.ok) throw new Error(r.reason);
      const life: any[] = [];
      for (let k = 0; k <= 4; k++) {
        life.push({ offset: k, reflect: IB.effectsOn(r.battle, BOSS, "reflect").filter(IB.active).map((e: any) => e.rounds), available: availableUserActions(r.battle, boss.userId, true, true).some((a) => a.id === REFLECT) });
        IB.nextRound(r.battle);
      }
      out.lifetime = life;
    }
    E.put("reflect", out);
    expect(out.far_hex6).toBe("Reflect");
    expect(reflected.playerLost).toBeGreaterThan(0);
    E.check("Reflect is cast at full HP from far (hex 6) and near (hex 2): no inherited health or distance gate", out.far_hex6 === "Reflect" && out.near_hex2 === "Reflect", { far: out.far_hex6, near: out.near_hex2 });
    E.check("active Reflect returns damage to the attacker (reflect text, player HP lost)", reflected.playerLost > 0 && out.reflected.texts.length > 0, out.reflected);
    E.check("Reflect is not damage reduction: the Captain loses the same HP as without Reflect", reflected.bossLost === control.bossLost && control.playerLost === 0, { control: out.control, reflected: out.reflected });
    E.check("Buff Prevent on the Captain before the cast stops the return", prevented.playerLost === 0, out.prevented);
    E.check("Reflect lifetime: active rounds 2 then 1 after the cast round, gone by +3", JSON.stringify(out.lifetime.slice(1, 4).map((l: any) => l.reflect)) === JSON.stringify([[2], [1], []]) || JSON.stringify(out.lifetime.slice(0, 4).map((l: any) => l.reflect)) === JSON.stringify([[2], [2], [1], []]), out.lifetime);
    E.check("cooldown 4: Reflect unavailable at +1..+3 and available at +4", JSON.stringify(out.lifetime.map((l: any) => l.available)) === JSON.stringify([false, false, false, false, true]), out.lifetime);
  });
});

describe("CROWNED — fight comparison (captured / dormant / support)", () => {
  const PID = "user_p";
  const PLAYERS: [F.PlayerStatBand, keyof typeof F.PLAYER_KITS][] = [
    ["jonin-cap", "buffer"], ["jonin-cap", "striker"], ["jonin-half", "moderate"],
    ["jonin-cap-durable", "buffer"], ["jonin-cap-durable", "striker"], ["jonin-cap-durable", "moderate"],
  ];
  const SEEDS = [1, 2, 3];
  const reflectDamage = (texts: string[]) => texts.reduce((s, t) => { const m = t.match(new RegExp(`^${PID} takes ([0-9.]+) reflect damage`)); return s + (m ? Number(m[1]) : 0); }, 0);
  const fight = async (v: Variant, band: F.PlayerStatBand, kit: keyof typeof F.PLAYER_KITS, seed: number, startPct?: number) =>
    S.withSeed(seed, async () => {
      const pl = F.playerQueryUser(PID, band, kit, F.playerPolicy(PID, kit), S.joninCaps());
      const b = await S.assembleBattle({ users: [pl, bossFor(v)], placements: [{ userId: PID, x: 2, y: 4 }, { userId: BOSS, x: 8, y: 4 }], autoCombatUserIds: [PID] });
      if (startPct !== undefined) { const boss = b.usersState.find((u) => u.controllerId === BOSS)!; boss.curHealth = boss.maxHealth * startPct / 100; }
      return S.runFight(b, { playerIds: [PID], bossIds: [BOSS], maxRounds: 40, seed });
    });
  const metrics = (r: S.FightResult) => {
    const boss = r.log.filter((l) => l.actor === BOSS);
    const loss = (d: Record<string, number>, c: string) => -Math.min(0, d[c] ?? 0);
    const supportCasts = boss.filter((l) => l.actionId && SUPPORT.has(l.actionId));
    const offensive = boss.filter((l) => l.actionId && !SUPPORT.has(l.actionId) && l.actionId !== "wait" && l.actionId !== "move");
    const rounds = [...new Set(boss.map((l) => l.round))].length || 1;
    return {
      winner: r.winner, rounds: r.rounds,
      bossDamageToPlayer: r.log.reduce((s, l) => s + loss(l.hpDeltaStep, PID), 0) + loss(r.residualHpDelta, PID),
      playerDamageToBoss: r.log.reduce((s, l) => s + loss(l.hpDeltaStep, BOSS), 0) + loss(r.residualHpDelta, BOSS),
      bossHpLeftPct: r.final[BOSS]!.curHealth / r.final[BOSS]!.maxHealth,
      heals: boss.filter((l) => l.actionId === S35).length,
      hpHealed: boss.filter((l) => l.actionId === S35).reduce((s, l) => s + Math.max(0, l.hpDelta[BOSS] ?? 0), 0),
      copies: boss.filter((l) => l.actionId === B07).length,
      effectsCopied: boss.filter((l) => l.actionId === B07).reduce((s, l) => { const m = l.effectTexts.join(" ").match(/copies (\d+) positive effect/); return s + (m ? Number(m[1]) : 0); }, 0),
      reflectCasts: boss.filter((l) => l.actionId === REFLECT).length,
      reflectDamage: r.log.filter((l) => l.actor === PID).reduce((s, l) => s + reflectDamage(l.effectTexts), 0),
      supportApPerRound: supportCasts.reduce((s, l) => s + Math.max(0, l.apBefore - l.apAfter), 0) / rounds,
      offensiveActionsPerRound: offensive.length / rounds,
      offensiveApPerRound: offensive.reduce((s, l) => s + Math.max(0, l.apBefore - l.apAfter), 0) / rounds,
    };
  };
  const mean = (rows: any[], k: string) => rows.reduce((s, r) => s + r[k], 0) / rows.length;
  const summarise = (rows: any[]) => ({
    bossWins: rows.filter((r) => r.winner === "boss").length, playerWins: rows.filter((r) => r.winner === "player").length,
    ...Object.fromEntries(["rounds", "bossDamageToPlayer", "playerDamageToBoss", "bossHpLeftPct", "heals", "hpHealed", "copies", "effectsCopied", "reflectCasts", "reflectDamage", "supportApPerRound", "offensiveActionsPerRound", "offensiveApPerRound"].map((k) => [k, mean(rows, k)])),
  });

  it("measures support activation against the same players, placements and seeds", async () => {
    const table: Record<string, any> = {};
    for (const [band, kit] of PLAYERS) for (const v of ["captured", "dormant", "support"] as Variant[]) {
      const rows = [];
      for (const seed of SEEDS) rows.push(metrics(await fight(v, band, kit, seed)));
      table[`${band}/${kit}|${v}`] = summarise(rows);
    }
    // Forced heal opportunity: the Captain starts at 45% HP (labelled synthetic start).
    for (const [band, kit] of [["jonin-cap-durable", "striker"], ["jonin-cap-durable", "buffer"]] as const) for (const v of ["dormant", "support"] as Variant[]) {
      const rows = [];
      for (const seed of SEEDS) rows.push(metrics(await fight(v, band, kit, seed, 45)));
      table[`start45%:${band}/${kit}|${v}`] = summarise(rows);
    }
    E.put("comparison", table);
    const keys = (v: Variant) => Object.keys(table).filter((k) => k.endsWith(`|${v}`) && !k.startsWith("start45"));
    const dormantSupportUses = [...keys("captured"), ...keys("dormant")].reduce((s, k) => s + table[k].heals + table[k].copies + table[k].reflectCasts, 0);
    const supportReflects = keys("support").reduce((s, k) => s + table[k].reflectCasts, 0);
    const bufferCopies = keys("support").filter((k) => k.includes("buffer")).reduce((s, k) => s + table[k].copies, 0);
    const forcedHeals = table["start45%:jonin-cap-durable/striker|support"].heals + table["start45%:jonin-cap-durable/buffer|support"].heals;
    E.check("captured and prior remap-only rules keep all three support techniques dormant (control)", dormantSupportUses === 0, dormantSupportUses);
    E.check("support candidate casts Reflect in every matchup", keys("support").every((k) => table[k].reflectCasts > 0), Object.fromEntries(keys("support").map((k) => [k, table[k].reflectCasts])));
    E.check("support candidate copies against IDG buffers (copy count > 0 vs buffer fixtures)", bufferCopies > 0, bufferCopies);
    E.check("forced 45% start: support candidate heals in-fight (heals > 0) and restores HP", forcedHeals > 0 && table["start45%:jonin-cap-durable/striker|support"].hpHealed + table["start45%:jonin-cap-durable/buffer|support"].hpHealed > 0, { forcedHeals });
    E.check("no fight ends unresolved within 40 rounds", Object.values(table).every((t: any) => t.bossWins + t.playerWins === SEEDS.length), Object.fromEntries(Object.entries(table).map(([k, t]: any) => [k, [t.bossWins, t.playerWins]])));
    expect(supportReflects).toBeGreaterThan(0);
  });
});

requireClean(E);
