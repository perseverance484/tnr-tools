/**
 * Gate A2: actual Sealwright AI selection and full-combat comparison against the
 * accepted regular Captain (five captured moves, captured profile).
 *
 * Part 1 — selector matrix: one performAIaction decision per case on a battle
 * assembled by processUsersForBattle, with opponent effects injected through the
 * upstream test helper `makeEffect` (exact boundary powers are synthetic test
 * inputs; clearprevent is realised from a captured jutsu effect).
 * Part 2 — control and capacity: B16 lockout, 40+60 AP rounds, Clear GCD.
 * Part 3 — full fights: Captain vs three Sealwright rule variants (contract,
 * noClosing, lateClosing) over the same player fixtures, placements and seeds.
 * No parity tolerance is approved; this reports measurements only.
 */
import { afterAll, describe, expect, it } from "bun:test";
import { availableUserActions, performBattleAction } from "@/libs/combat/actions";
import { performAIaction } from "@/libs/combat/ai_v2";
import { calcApReduction, calcPoolCost, getBattleGrid } from "@/libs/combat/util";
import { BarrierTag } from "@/validators/combat";
import type { CompleteBattle, UserEffect } from "@/libs/combat/types";
import { makeEffect } from "../libs/combat/helpers/battleScenario";
import * as F from "./lib/fixtures";
import * as IB from "./lib/itembattle";
import * as S from "./lib/sim";
import { Evidence } from "./lib/report";

const A2 = new Evidence("A2");
afterAll(() => A2.flush({
  comparator: "regular Captain QY69h271Nx9uHrBeR6jwW, captured kit = accepted five moves, captured profile (includeDefaultRules:true), innate effect kept",
  sealwrightCarrier: "Captain numeric profile (level/stats/pools/regen/multipliers/preferences) without innate effect or items; contract seven jutsu at level 1",
  dmgConfig: "engine source defaults",
  migration: F.MIGRATION_0056,
}));

const SW = "sealwright";
const IDS = Object.fromEntries((F.contract().jutsus as any[]).map((j) => [j.code, j.liveJutsuId])) as Record<string, string>;
const NAME = Object.fromEntries(Object.entries(IDS).map(([k, v]) => [v, k]));
const ROSE = { file: "harvests/inbox/tnr_results_1791247737840.json", pointer: "/captures/52/data" }; // Rose Sanctuary (clearprevent 100/2r)

type Opp = { id: string; x: number; y: number; summonOf?: string; idg?: number; idgOpts?: Partial<UserEffect> & Record<string, unknown>; clearPrevent?: boolean };

const quietPlayer = (id: string) => {
  const pol = { id: `policy::${id}`, userId: id, includeDefaultRules: false, rules: [] };
  const u = F.playerQueryUser(id, "jonin-cap-durable", "striker", pol, S.joninCaps());
  u.jutsus = [];
  return u;
};

/** Assemble Sealwright (contract variant) at (sx, 4) against the given opponents. */
const selectorBattle = async (opps: Opp[], sw: { x: number; y?: number } = { x: 6 }, variant: "contract" | "noClosing" | "lateClosing" = "contract") => {
  const players = opps.filter((o) => !o.summonOf);
  const users = [...players.map((o) => quietPlayer(o.id)), F.sealwrightQueryUser(F.sealwrightProfile(variant))];
  const b = await S.assembleBattle({
    users,
    placements: [...players.map((o) => ({ userId: o.id, x: o.x, y: o.y })), { userId: SW, x: sw.x, y: sw.y ?? 4 }],
    leftSideUserIds: players.map((o) => o.id),
  });
  for (const o of opps.filter((x) => x.summonOf)) {
    // Summoned/cloned opponent as the engine's clone() constructs one: a copy of
    // its controller's battle state, isSummon/isAi true, controllerId = owner.
    const owner = b.usersState.find((u) => u.controllerId === o.summonOf)!;
    const s = structuredClone(owner);
    Object.assign(s, { userId: o.id, username: o.id, controllerId: owner.userId, isSummon: true, isAi: true, isOriginal: false, longitude: o.x, latitude: o.y, aiProfileId: "Default" });
    b.usersState.push(s);
  }
  const uidOf = (cid: string) => b.usersState.find((u) => u.controllerId === cid || u.userId === cid)!.userId;
  for (const o of opps) {
    const tid = uidOf(o.id);
    if (o.idg !== undefined) {
      b.usersEffects.push(makeEffect("increasedamagegiven", { power: o.idg, rounds: 3, calculation: "percentage", statTypes: ["Highest"] as never, generalTypes: [] }, {
        id: `idg-${o.id}`, creatorId: tid, targetId: tid, isNew: false, castThisRound: false, createdRound: 0, actionId: "harness-idg", fromType: "jutsu", targetType: "user", ...o.idgOpts,
      }));
    }
    if (o.clearPrevent) {
      const tag = F.captured(ROSE.file, ROSE.pointer).record.effects.find((e: any) => e.type === "clearprevent");
      b.usersEffects.push(makeEffect("clearprevent", { power: tag.power, rounds: tag.rounds, calculation: tag.calculation }, {
        id: `cp-${o.id}`, creatorId: tid, targetId: tid, isNew: false, castThisRound: false, createdRound: 0, actionId: "harness-clearprevent", fromType: "jutsu", targetType: "user",
      }));
    }
  }
  b.activeUserId = uidOf(SW);
  return { b, uidOf };
};

const decide = (b: CompleteBattle, swId: string) => {
  const grid = getBattleGrid(1, b);
  const before = structuredClone(b.usersEffects);
  const r = performAIaction(b, grid, swId);
  const after = r.nextBattle.usersEffects;
  const removed = before.filter((e) => e.type === "increasedamagegiven" || e.type === "clearprevent")
    .map((e) => ({ id: e.id, target: e.targetId, type: e.type, roundsBefore: e.rounds, roundsAfter: after.find((x) => x.id === e.id)?.rounds ?? null }));
  return { action: r.nextActionId ? NAME[r.nextActionId] ?? r.nextActionId : null, texts: r.nextActionEffects.map((e) => e.txt), effects: removed, battle: r.nextBattle };
};

describe("A2 Part 1 — B32/S31 selector matrix (contract rules)", () => {
  it("IDG 69 / 70 / 70.5 / 71 / 90 at hex distance 3 (path 4)", async () => {
    const out: Record<string, any> = {};
    for (const idg of [69, 70, 70.5, 71, 90]) {
      const { b, uidOf } = await selectorBattle([{ id: "user_p", x: 3, y: 4, idg }]);
      const d = decide(b, uidOf(SW));
      out[String(idg)] = { action: d.action, idgAfter: d.effects, texts: d.texts };
    }
    A2.put("thresholdMatrix", out);
    expect(out["69"].action).toBe("S31");
    expect(out["70"].action).toBe("S31");
    expect(out["70.5"].action).toBe("S31");
    expect(out["71"].action).toBe("B32");
    expect(out["90"].action).toBe("B32");
    A2.check("IDG 69/70/70.5 → S31 (routine), 71/90 → B32 (integer threshold 71, >=)", ["69", "70", "70.5"].every((k) => out[k].action === "S31") && ["71", "90"].every((k) => out[k].action === "B32"), Object.fromEntries(Object.entries(out).map(([k, v]: any) => [k, v.action])));
  });

  it("distance gate 6 is path length (hex distance + 1)", async () => {
    const out: Record<string, any> = {};
    for (const hex of [4, 5, 6]) {
      const { b, uidOf } = await selectorBattle([{ id: "user_p", x: 6 - hex, y: 4, idg: 90 }]);
      out[`hex${hex}`] = decide(b, uidOf(SW)).action;
    }
    A2.put("distanceGate", out);
    expect(out.hex5).toBe("B32");
    expect(out.hex6).not.toBe("B32");
    A2.check("IDG 90: B32 at hex 4/5 (path ≤6), not at hex 6 (path 7)", out.hex4 === "B32" && out.hex5 === "B32" && out.hex6 !== "B32", out);
  });

  it("B32 unavailable falls through (cooldown, AP, pools, Clear GCD after S31)", async () => {
    const out: Record<string, any> = {};
    const mk = () => selectorBattle([{ id: "user_p", x: 3, y: 4, idg: 90 }]);
    {
      const { b, uidOf } = await mk();
      const sw = b.usersState.find((u) => u.userId === uidOf(SW))!;
      sw.jutsus.find((j) => j.jutsuId === IDS.B32)!.lastUsedRound = b.round;
      out.cooldown = decide(b, sw.userId).action;
    }
    {
      const { b, uidOf } = await mk();
      b.usersState.find((u) => u.userId === uidOf(SW))!.actionPoints = 40;
      out.ap40 = decide(b, uidOf(SW)).action;
    }
    {
      const { b, uidOf } = await mk();
      const sw = b.usersState.find((u) => u.userId === uidOf(SW))!;
      const act = availableUserActions(b, sw.userId, true, true).find((a) => a.id === IDS.B32)!;
      out.b32PoolCost = calcPoolCost(act, b.usersEffects, sw);
      sw.curChakra = 0;
      sw.curStamina = 0;
      out.noPools = decide(b, sw.userId).action;
    }
    {
      // S31 cast in round r by a real action → the shared "clear" GCD locks B32.
      const { b, uidOf } = await mk();
      const sw = uidOf(SW);
      const grid = getBattleGrid(1, b);
      const s31 = availableUserActions(b, sw, true, true).find((a) => a.id === IDS.S31)!;
      performBattleAction({ battle: b, action: s31, grid, contextUserId: sw, actorId: sw, longitude: 3, latitude: 4 });
      const gcd: any[] = [];
      for (let k = 1; k <= 4; k++) {
        IB.nextRound(b);
        // Re-apply a fresh 90 IDG each round (S31 cleared the original).
        const tid = b.usersState.find((u) => u.controllerId === "user_p")!.userId;
        b.usersEffects.push(makeEffect("increasedamagegiven", { power: 90, rounds: 3, calculation: "percentage", statTypes: ["Highest"] as never, generalTypes: [] }, { id: `idg-r${k}`, creatorId: tid, targetId: tid, isNew: false, castThisRound: false, createdRound: b.round, actionId: "harness-idg", fromType: "jutsu", targetType: "user" }));
        const ids = availableUserActions(b, sw, true, true).map((a) => NAME[a.id]).filter(Boolean);
        gcd.push({ roundsAfterS31: k, available: ids });
      }
      out.clearGcdAfterS31 = gcd;
    }
    A2.put("b32Unavailable", out);
    expect(out.cooldown).toBe("S31");
    expect(out.ap40).not.toBe("B32");
    A2.check("B32 on cooldown → S31", out.cooldown === "S31", out.cooldown);
    A2.check("40 AP left → not B32 (60 AP)", out.ap40 !== "B32", out.ap40);
    A2.check("pools exhausted → recorded fall-through", true, { action: out.noPools, cost: out.b32PoolCost });
    A2.check("FINDING: S31 and B32 share the 'clear' GCD (3 rounds) — no same-round or back-to-back double Clear", out.clearGcdAfterS31[0].available.includes("B32") === false, out.clearGcdAfterS31);
  });

  it("closest-opponent targeting with summons and second opponents; ALL-method recipients", async () => {
    const out: Record<string, any> = {};
    {
      const { b, uidOf } = await selectorBattle([{ id: "user_p", x: 2, y: 4, idg: 90 }, { id: "summon_s", x: 4, y: 4, summonOf: "user_p" }]);
      out.lowIdgSummonCloser = decide(b, uidOf(SW));
    }
    {
      const { b, uidOf } = await selectorBattle([{ id: "user_p", x: 3, y: 4, idg: 60 }, { id: "summon_s", x: 4, y: 4, summonOf: "user_p", idg: 90 }]);
      out.buffedSummonCloser = decide(b, uidOf(SW));
    }
    {
      const { b, uidOf } = await selectorBattle([{ id: "user_p1", x: 3, y: 4, idg: 90 }, { id: "user_p2", x: 0, y: 1, idg: 60 }]);
      out.distantSecondOpponent = decide(b, uidOf(SW));
    }
    const brief = (d: any) => ({ action: d.action, idg: d.effects.filter((e: any) => e.type === "increasedamagegiven"), texts: d.texts });
    A2.put("targeting", Object.fromEntries(Object.entries(out).map(([k, v]) => [k, brief(v)])));
    expect(out.lowIdgSummonCloser.action).not.toBe("B32");
    expect(out.buffedSummonCloser.action).toBe("B32");
    A2.check("closest low-IDG summon suppresses B32 even when a farther player has IDG 90", out.lowIdgSummonCloser.action !== "B32", brief(out.lowIdgSummonCloser));
    A2.check("buffed closest summon triggers B32; ALL Clear also reaches the farther player", out.buffedSummonCloser.action === "B32", brief(out.buffedSummonCloser));
    A2.check("closest player IDG 90 triggers B32; distant second opponent (outside gate) recorded", out.distantSecondOpponent.action === "B32", brief(out.distantSecondOpponent));
  });

  it("blocked path lengthens the gate distance", async () => {
    const { b, uidOf } = await selectorBattle([{ id: "user_p", x: 1, y: 4, idg: 90 }]);
    for (const y of [1, 2, 3, 4, 5, 6, 7, 8]) {
      b.groundEffects.push({ ...BarrierTag.parse({ power: 2, staticAssetPath: "harness-wall" }), id: `wall-${y}`, creatorId: "ground", actionId: "initial", createdRound: 0, level: 0, longitude: 3, latitude: y, isNew: false, barrierAbsorb: 0, castThisRound: false } as never);
    }
    const d = decide(b, uidOf(SW));
    A2.put("blockedPath", { hexDistance: 5, wallColumn: 3, action: d.action, texts: d.texts });
    A2.check("wall between (hex 5) → path > 6 → no B32", d.action !== "B32", d.action);
    expect(d.action).not.toBe("B32");
  });

  it("new, inactive and protected IDG; Clear Prevent", async () => {
    const cases: Record<string, Partial<Opp>> = {
      newlyCastThisRound: { idgOpts: { isNew: true, castThisRound: true } },
      expiredRoundsZero: { idgOpts: { rounds: 0 } },
      protectedBloodlineSource: { idgOpts: { fromType: "bloodline" } },
      clearPrevent: { clearPrevent: true },
    };
    const out: Record<string, any> = {};
    for (const [k, extra] of Object.entries(cases)) {
      const { b, uidOf } = await selectorBattle([{ id: "user_p", x: 3, y: 4, idg: 90, ...extra }]);
      const d = decide(b, uidOf(SW));
      out[k] = { action: d.action, effects: d.effects, texts: d.texts };
    }
    A2.put("idgStatesAndClearPrevent", out);
    const removed = (k: string) => out[k].effects.find((e: any) => e.type === "increasedamagegiven")?.roundsAfter === 0;
    A2.check("expired (rounds 0) IDG still counts toward the threshold → B32 cast with nothing removable", out.expiredRoundsZero.action === "B32", out.expiredRoundsZero);
    A2.check("protected (bloodline-source) IDG triggers B32 but is not removed", out.protectedBloodlineSource.action === "B32" && !removed("protectedBloodlineSource"), out.protectedBloodlineSource);
    A2.check("Clear Prevent: B32 cast, IDG not removed", out.clearPrevent.action === "B32" && !removed("clearPrevent"), out.clearPrevent);
    A2.check("newly cast IDG: recorded selection and removal outcome", true, out.newlyCastThisRound);
    expect(out.clearPrevent.action).toBe("B32");
  });

  it("S31 is routine whenever ready and in range", async () => {
    const out: Record<string, any> = {};
    for (const [k, opp] of Object.entries({ noBuffs_hex3: { x: 3 }, idg50_hex3: { x: 3, idg: 50 }, noBuffs_hex4: { x: 2 } })) {
      const { b, uidOf } = await selectorBattle([{ id: "user_p", y: 4, ...opp } as Opp]);
      out[k] = decide(b, uidOf(SW)).action;
    }
    A2.put("s31Routine", out);
    expect(out.noBuffs_hex3).toBe("S31");
    A2.check("no buffs at hex 3 → S31 first", out.noBuffs_hex3 === "S31", out);
    A2.check("IDG 50 at hex 3 → S31 (not B32)", out.idg50_hex3 === "S31", out);
    A2.check("hex 4 (path 5) → S31 out of rule gate; next rule recorded", out.noBuffs_hex4 !== "S31", out.noBuffs_hex4);
  });
});

describe("A2 Part 2 — control duration and AP capacity", () => {
  it("B16 stun+seal lockout on a player", async () => {
    const { b, uidOf } = await selectorBattle([{ id: "user_p", x: 3, y: 4 }]);
    const sw = uidOf(SW);
    const p = uidOf("user_p");
    const grid = getBattleGrid(1, b);
    const b16 = availableUserActions(b, sw, true, true).find((a) => a.id === IDS.B16)!;
    const r = performBattleAction({ battle: b, action: b16, grid, contextUserId: sw, actorId: sw, longitude: 3, latitude: 4 });
    const timeline: any[] = [];
    for (let k = 0; k <= 3; k++) {
      const eff = r.newBattle.usersEffects.filter((e) => e.targetId === p && (e.type === "stun" || e.type === "seal")).map((e) => ({ type: e.type, rounds: e.rounds }));
      timeline.push({ round: r.newBattle.round, apReduction: calcApReduction(r.newBattle as never, p), effects: eff });
      IB.nextRound(r.newBattle);
    }
    A2.put("b16Control", { texts: r.actionEffects.map((e) => e.txt), timeline });
    A2.check("B16 applies stun and seal to the target (timeline recorded)", timeline[0].effects.length >= 2, timeline);
    expect(timeline[0].effects.length).toBeGreaterThanOrEqual(2);
  });
});

type Boss = { label: string; build: () => any; cid: string };
const BOSSES: Boss[] = [
  { label: "Captain", cid: "QY69h271Nx9uHrBeR6jwW", build: () => { const e = F.entityByName("The Captain"); return F.aiQueryUser(e, "accepted", F.capturedRules(e)); } },
  { label: "Sealwright:contract", cid: SW, build: () => F.sealwrightQueryUser(F.sealwrightProfile("contract")) },
  { label: "Sealwright:noClosing", cid: SW, build: () => F.sealwrightQueryUser(F.sealwrightProfile("noClosing")) },
  { label: "Sealwright:lateClosing", cid: SW, build: () => F.sealwrightQueryUser(F.sealwrightProfile("lateClosing")) },
];
const PLAYERS: [F.PlayerStatBand, keyof typeof F.PLAYER_KITS][] = [
  ["jonin-cap", "buffer"], ["jonin-cap", "striker"], ["jonin-half", "moderate"],
  ["jonin-cap-durable", "buffer"], ["jonin-cap-durable", "striker"], ["jonin-cap-durable", "moderate"],
];
const SEEDS = [1, 2, 3, 4, 5];
const PID = "user_p";

const fightMetrics = (r: S.FightResult, bossCid: string) => {
  const bossActs = r.log.filter((l) => l.actor === bossCid);
  const playerActs = r.log.filter((l) => l.actor === PID);
  const dmgTo = (l: S.ActionRecord, cid: string) => -Math.min(0, l.hpDelta[cid] ?? 0);
  const perRoundBossDmg: Record<number, number> = {};
  for (const l of r.log) perRoundBossDmg[l.round] = (perRoundBossDmg[l.round] ?? 0) + (l.actor === bossCid ? dmgTo(l, PID) : 0);
  const roundsWithBossAction = [...new Set(bossActs.map((l) => l.round))];
  const samples = r.perRound.filter((s) => s.users[PID] && s.users[bossCid]);
  const frac = (f: (s: S.RoundSample) => boolean) => (samples.length ? samples.filter(f).length / samples.length : 0);
  const clearIds = new Set([IDS.S31, IDS.B32]);
  const playerMax = r.final[PID]!.maxHealth;
  return {
    winner: r.winner,
    rounds: r.rounds,
    bossDamageToPlayer: bossActs.reduce((s, l) => s + dmgTo(l, PID), 0),
    playerDamageToBoss: playerActs.reduce((s, l) => s + dmgTo(l, bossCid), 0),
    spikeActionPctOfPlayerMaxHp: bossActs.reduce((m, l) => Math.max(m, dmgTo(l, PID)), 0) / playerMax,
    spikeRoundPctOfPlayerMaxHp: Math.max(0, ...Object.values(perRoundBossDmg)) / playerMax,
    lockoutRounds: samples.filter((s) => s.users[PID]!.stunned).length,
    sealedRounds: samples.filter((s) => s.users[PID]!.sealed).length,
    recoveryWindows: roundsWithBossAction.filter((rd) => (perRoundBossDmg[rd] ?? 0) === 0).length,
    playerMinChakraPct: Math.min(...samples.map((s) => s.users[PID]!.cp)) / r.final[PID]!.maxChakra,
    playerMinStaminaPct: Math.min(...samples.map((s) => s.users[PID]!.sp)) / r.final[PID]!.maxStamina,
    bossMinChakraPct: Math.min(...samples.map((s) => s.users[bossCid]!.cp)) / r.final[bossCid]!.maxChakra,
    bossMinStaminaPct: Math.min(...samples.map((s) => s.users[bossCid]!.sp)) / r.final[bossCid]!.maxStamina,
    playerBuffUptime: frac((s) => s.users[PID]!.idgRemovable > 0),
    bossDefenceUptime: frac((s) => s.users[bossCid]!.shieldHp > 0 || s.users[bossCid]!.absorb || s.users[bossCid]!.ddt),
    clearCasts: bossActs.filter((l) => l.actionId && clearIds.has(l.actionId)).length,
    b32Casts: bossActs.filter((l) => l.actionId === IDS.B32).length,
    clearsThatRemoved: bossActs.filter((l) => l.effectTexts.some((t) => t.includes("was cleared of all positive"))).length,
    bossExhausted: r.bossExhausted,
    bossIdleTimeouts: r.idleTimeouts[bossCid] ?? 0,
    bossActionCounts: bossActs.reduce<Record<string, number>>((m, l) => ((m[l.actionName ?? "(none)"] = (m[l.actionName ?? "(none)"] ?? 0) + 1), m), {}),
    bossApPerRound: roundsWithBossAction.length ? bossActs.reduce((s, l) => s + Math.max(0, l.apBefore - l.apAfter), 0) / roundsWithBossAction.length : 0,
    // AP spent on anything but "wait" (wait forfeits the remaining AP).
    bossActiveApPerRound: roundsWithBossAction.length ? bossActs.filter((l) => l.actionId !== "wait").reduce((s, l) => s + Math.max(0, l.apBefore - l.apAfter), 0) / roundsWithBossAction.length : 0,
    bossWaits: bossActs.filter((l) => l.actionId === "wait").length,
  };
};

const aggregate = (rows: ReturnType<typeof fightMetrics>[]) => {
  const num = Object.keys(rows[0]!).filter((k) => typeof (rows[0] as any)[k] === "number");
  const out: Record<string, any> = { fights: rows.length, bossWins: rows.filter((r) => r.winner === "boss").length, playerWins: rows.filter((r) => r.winner === "player").length, unresolved: rows.filter((r) => r.winner === "none").length, bossExhaustions: rows.filter((r) => r.bossExhausted).length };
  for (const k of num) {
    const v = rows.map((r) => (r as any)[k] as number);
    out[k] = { mean: v.reduce((a, b) => a + b, 0) / v.length, min: Math.min(...v), max: Math.max(...v) };
  }
  return out;
};

describe("A2 Part 3 — full combat comparison (same players, placements, seeds)", () => {
  it("Captain vs Sealwright variants", async () => {
    const table: Record<string, any> = {};
    const firstLogs: Record<string, any> = {};
    for (const [band, kitName] of PLAYERS) {
      for (const boss of BOSSES) {
        const rows = [];
        for (const seed of SEEDS) {
          const r = await S.withSeed(seed, async () => {
            const pl = F.playerQueryUser(PID, band, kitName, F.playerPolicy(PID, kitName), S.joninCaps());
            const bu = boss.build();
            const b = await S.assembleBattle({ users: [pl, bu], placements: [{ userId: PID, x: 2, y: 4 }, { userId: bu.userId, x: 8, y: 4 }], autoCombatUserIds: [PID] });
            return S.runFight(b, { playerIds: [PID], bossIds: [boss.cid], maxRounds: 40, seed });
          });
          rows.push(fightMetrics(r, boss.cid));
          if (seed === 1) firstLogs[`${band}/${kitName}|${boss.label}`] = r.log.filter((l) => l.actor === boss.cid).slice(0, 14).map((l) => `${l.round}:${l.actionName ?? "(none)"}:${Math.round(-(l.hpDelta[PID] ?? 0))}`);
        }
        table[`${band}/${kitName}|${boss.label}`] = aggregate(rows);
      }
    }
    A2.put("comparisonMatrix", table);
    A2.put("bossActionSamplesSeed1", firstLogs);
    const exh = Object.entries(table).filter(([, v]: any) => v.bossExhaustions > 0).map(([k]) => k);
    A2.check("no boss AI-exhaustion give-up in any comparison fight", exh.length === 0, exh);
    for (const [band, kitName] of PLAYERS) {
      const sw = table[`${band}/${kitName}|Sealwright:contract`];
      A2.check(`${band}/${kitName}: Sealwright casts Clears in combat (S31 routine)`, sw.clearCasts.mean > 0, sw.clearCasts);
    }
    expect(exh).toEqual([]);
  });
});
