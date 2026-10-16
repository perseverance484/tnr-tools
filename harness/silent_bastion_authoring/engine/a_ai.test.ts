/**
 * Gate A — the 4 commander translations and 16 regular AIs against the pinned engine's own AI
 * schema, rule cap, write schema and decision engine (performAIaction / alignBattle). Pure, no DB.
 * Real captured jutsu records; exclusive / Countermand / seed weapons as labelled candidates.
 */
import { describe, it } from "bun:test";
import { AI_PROFILE_MAX_RULES } from "@/drizzle/constants";
import { insertAiSchema } from "@/drizzle/schema";
import { getTagSchema, JutsuValidator } from "@/validators/combat";
import { Evidence, requireClean } from "./lib/report";
import {
  AI, aiTurn, allUnits, commanders, compileRules, HUMAN, itemRecord, jutsuId, jutsuRecord, playRounds, regulars, scene, sources, type Unit,
} from "./lib/units";

const ev = new Evidence("a_ai");
const c = (n: string, p: boolean, d?: unknown) => ev.check(n, p, d);
const byKey = (k: string) => allUnits().find((u) => u.key === k)!;
const MOA = byKey("master_of_arms"), RZ = byKey("replicant_zero"), GM = byKey("grand_marshal"), AR = byKey("arakane");
const fx = (type: string, power = 100, rounds = 3) => ({ type, power, rounds }) as never;
const first = (u: Unit, s: Parameters<typeof scene>[1]) => aiTurn(u, scene(u, s)).acts;

describe("A1 static: every unit's rules, kit and write record", () => {
  for (const u of allUnits()) {
    it(u.key, () => {
      const rules = compileRules(u);
      c(`${u.key}: ${rules.length} rules ≤ server cap ${AI_PROFILE_MAX_RULES}`, rules.length <= AI_PROFILE_MAX_RULES, rules.length);
      const last = rules[rules.length - 1]!;
      c(`${u.key}: last rule is an unconditional end_turn (includeDefaultRules:false)`, last.conditions.length === 0 && last.action.type === "end_turn");
      const thresholds = rules.flatMap((r) => r.conditions).filter((x) => x.type === "has_effect" || x.type === "target_has_effect") as { threshold: number }[];
      c(`${u.key}: every has_effect/target_has_effect threshold ≥ 1 (law R50)`, thresholds.every((t) => t.threshold >= 1), thresholds);
      const kitIds = new Set(u.kit.map(jutsuId));
      const used = new Set(rules.map((r) => ("jutsuId" in r.action ? r.action.jutsuId : undefined)).filter(Boolean) as string[]);
      c(`${u.key}: every jutsu rule targets an equipped kit jutsu`, [...used].every((id) => kitIds.has(id)), [...used].filter((id) => !kitIds.has(id)));
      const unusedKit = u.kit.filter((k) => !used.has(jutsuId(k)));
      ev.put(`${u.key}.kitWithoutRule`, unusedKit);
      // Exact gate law: SINGLE OTHER_USER jutsu/item gated at range+1 (or tighter); none on SELF; ALL optional.
      const gateIssues: string[] = [];
      u.rules.forEach((r, i) => {
        if (r.do[0] !== "jutsu" && r.do[0] !== "item") return;
        const rec = r.do[0] === "jutsu" ? jutsuRecord(r.do[1]!) : itemRecord(r.do[1]!);
        const gates = r.if.filter((x) => x[0] === "dist<=").map((x) => Number(x[1]));
        const method = rec.method as string, target = rec.target as string, range = Number(rec.range);
        if (target === "SELF" || target === "EMPTY_GROUND") return;
        if (method === "ALL") { if (gates.length) gateIssues.push(`#${i + 1} ${r.do[1]} ALL-method carries a ≤${gates[0]} gate (safe, narrows use)`); return; }
        if (!gates.length) gateIssues.push(`#${i + 1} ${r.do[1]} UNGATED ranged action (range ${range})`);
        else if (Math.min(...gates) > range + 1) gateIssues.push(`#${i + 1} ${r.do[1]} gate ${Math.min(...gates)} > range+1=${range + 1} (can fire out of range)`);
      });
      const unsafe = gateIssues.filter((g) => g.includes("UNGATED") || g.includes("out of range"));
      ev.put(`${u.key}.gateNotes`, gateIssues);
      c(`${u.key}: no ranged action can fire out of range (gate ≤ range+1, law 40)`, unsafe.length === 0, unsafe);
      const cand = u.candidate as Record<string, unknown> & { ratio: Record<string, number>; element: string; preferredStat: string; generals: string[] };
      const record = {
        userId: `sb-${u.key}`, offence: 10, defence: 10, ninjutsuMastery: 10, genjutsuMastery: 10, taijutsuMastery: 10, bukijutsuMastery: 10, bloodlineMastery: 10, sageMastery: 10,
        username: u.name, avatar: "https://example.invalid/avatar.png", gender: "Unknown", isAi: true, isSummon: false,
        level: cand.level, rank: cand.rank, regeneration: cand.regeneration, statsMultiplier: cand.statsMultiplier, poolsMultiplier: cand.poolsMultiplier,
        primaryElement: cand.element === "None" ? "" : cand.element, secondaryElement: "", preferredStat: cand.preferredStat,
        preferredGeneral1: cand.generals[0], preferredGeneral2: cand.generals[1],
        ninjutsuOffence: 10, ninjutsuDefence: 10, genjutsuOffence: 10, genjutsuDefence: 10, taijutsuOffence: 10, taijutsuDefence: 10,
        bukijutsuOffence: 10, bukijutsuDefence: 10, strength: 10, intelligence: 10, willpower: 10, speed: 10,
        ...Object.fromEntries(Object.entries(cand.ratio).map(([k, v]) => [k, Math.max(10, v * 10_000)])),
        jutsus: u.kit.map(jutsuId), items: u.items.map((k) => ({ ids: [k.startsWith("X:") ? `x` : k], number: 0 })),
        effects: u.innate.map((x) => getTagSchema(x.type as never).parse({ type: x.type, power: x.power, rounds: x.rounds, target: "SELF", description: "innate" })),
      };
      const parsed = insertAiSchema.safeParse(record);
      c(`${u.key}: candidate AI record passes insertAiSchema (incl. innate passive effects)`, parsed.success, parsed.success ? undefined : parsed.error.issues.slice(0, 5));
    });
  }
});

describe("A2 static: exclusives, seed weapons, source drift", () => {
  it("candidate exclusive jutsu and Countermand pass the engine validators", () => {
    for (const code of ["X:LAST_DIRECTIVE", "X:EXTERMINATION_ORDER"]) {
      const rec = jutsuRecord(code);
      const p = JutsuValidator.safeParse({ ...rec, description: "candidate", requiredRank: "STUDENT", jutsuRank: "S", battleDescription: "%user", image: "https://example.invalid/i.png" });
      c(`${code} passes JutsuValidator`, p.success, p.success ? undefined : p.error.issues.slice(0, 5));
    }
  });
  it("captured records vs the pool registry summaries", () => {
    const drift: Record<string, string[]> = {};
    for (const [code, j] of Object.entries(sources.jutsu)) {
      const s = j.poolSummary as { range?: number; cooldown?: number; ap?: number; effects?: string[] } | null;
      if (!s) continue;
      const r = j.record;
      const d: string[] = [];
      if (s.cooldown !== r.cooldown) d.push(`cooldown pool ${s.cooldown} vs record ${r.cooldown}`);
      if (s.ap !== r.actionCostPerc) d.push(`AP pool ${s.ap} vs record ${r.actionCostPerc}`);
      if (typeof s.range === "number" && s.range !== r.range && r.target !== "SELF") d.push(`range pool ${s.range} vs record ${r.range}`);
      const recFx = r.effects.map((e) => `${e.type} ${e.power}${Number(e.rounds) > 0 ? `/${e.rounds}r` : ""}`).join("; ");
      if ((s.effects ?? []).join("; ") !== recFx) d.push(`effects pool [${(s.effects ?? []).join("; ")}] vs record [${recFx}]`);
      if (d.length) drift[code] = d;
    }
    ev.put("poolVsCaptureDrift", drift);
    ev.finding("SRC1", "Captured jutsu records differ from the 32b pool registry summary (record wins for implementation; pool doc needs a refresh)", Object.keys(drift).length > 0, Object.keys(drift));
    c("drift report produced", true);
  });
});

describe("A3 Master of Arms — roster §2 priorities", () => {
  it("priority order", () => {
    c("MoA: at 59% HP Sovereign Ascendance comes first", first(MOA, { hpPct: 59, dist: 4 })[0] === "B10", first(MOA, { hpPct: 59, dist: 4 }));
    c("MoA: at 60% HP it does not", first(MOA, { hpPct: 60, dist: 4 })[0] !== "B10");
    c("MoA: player IDG 71 → Nullifying Wave", first(MOA, { dist: 4, playerEffects: [fx("increasedamagegiven", 71)] })[0] === "B32");
    c("MoA: player IDG 70 → no Clear", first(MOA, { dist: 4, playerEffects: [fx("increasedamagegiven", 70)] })[0] !== "B32");
    c("MoA: player shield → Piercing Judgment", first(MOA, { dist: 4, playerEffects: [fx("shield", 100)] })[0] === "B33");
    const combo = first(MOA, { dist: 4 });
    c("MoA: open → Tempo Fracture then Fighter's Poise (full 100 AP)", combo.join() === "B08,B37", combo);
    const fetters = first(MOA, { dist: 6, cooldowns: { B08: 1 } });
    c("MoA: Tempo Fracture on cooldown → Sovereign Fetters", fetters[0] === "B16", fetters);
    const det = first(MOA, { dist: 4, cooldowns: { B08: 1, B16: 1 }, playerEffects: [fx("increasedamagetaken", 35)] });
    c("MoA: target with IDT ≥35 (Tempest Cleave applied) → Cataclysm Detonation follow-up", det[0] === "B14", det);
  });
  it("Tempest Cleave (AOE_CIRCLE_SPAWN, friendlyFire ALL): self-hit by distance", () => {
    const res: Record<number, { cast: boolean; selfHit: string[] }> = {};
    for (const dist of [2, 3, 4, 5]) {
      const u = { ...MOA, rules: [{ if: [["dist<=", 5]], do: ["jutsu", "TC", "CLOSEST_OPPONENT"], src: "probe" }, { if: [], do: ["end"], src: "end" }] } as Unit;
      const { battle, acts } = aiTurn(u, scene(u, { dist }));
      const self = battle.usersEffects.filter((e) => e.targetId === AI && e.creatorId === AI && ["afterburn", "increasedamagetaken", "damage"].includes(e.type)).map((e) => e.type);
      const hpLoss = 100_000 - (battle.usersState.find((x) => x.userId === AI)!.curHealth);
      res[dist] = { cast: acts[0] === "TC", selfHit: [...new Set(self)].concat(hpLoss > 0 ? [`hp-${hpLoss}`] : []) };
    }
    ev.put("tempestCleaveSelfHit", res);
    const safe = Object.entries(res).filter(([, v]) => v.cast && v.selfHit.length === 0).map(([k]) => Number(k));
    ev.put("tempestCleaveSafeMinDistance", safe.length ? Math.min(...safe) : null);
    c("Tempest Cleave cast at path distances 3–5", [3, 4, 5].every((d) => res[d]!.cast), res);
    ev.finding("TC1", "Tempest Cleave (existing EVENT jutsu, AOE_CIRCLE_SPAWN, friendlyFire ALL) hits Master of Arms himself at short range", Object.values(res).some((v) => v.selfHit.length > 0), res);
  });
  it("never gives up across 8 router-faithful rounds at range 3 and 8", () => {
    for (const dist of [3, 8]) {
      const { log } = playRounds(MOA, scene(MOA, { dist, round: 1 }), 8);
      c(`MoA dist ${dist}: no exhaustion give-up over 8 rounds`, !log.some((l) => l.acts.includes("GAVE_UP")), log);
      ev.put(`MoA.rounds.dist${dist}`, log.map((l) => `${l.round}:${l.acts.join("+")}`));
    }
  });
});

describe("A4 Replicant Zero — roster §3 priorities", () => {
  it("opening, clone once, sustain", () => {
    const open = first(RZ, { round: 1, dist: 4 });
    c("RZ round 1: Compression Barrier then Hexweave", open.join() === "B22,B13", open);
    const r2 = aiTurn(RZ, scene(RZ, { round: 2, dist: 4, cooldowns: { B22: 1, B13: 1 } }));
    const clones = r2.battle.usersState.filter((x) => x.userId !== AI && x.userId !== HUMAN).length;
    c("RZ round 2: Split Image cast and a clone is on the field", r2.acts[0] === "B06" && clones >= 1, { acts: r2.acts, clones });
    const r8 = first(RZ, { round: 8, dist: 4, cooldowns: { B13: 1 } });
    c("RZ round 8 (clone off cooldown): no second Split Image", !r8.includes("B06"), r8);
    c("RZ: player IDG ≥71 → Stolen Form", first(RZ, { round: 4, dist: 4, playerEffects: [fx("increasedamagegiven", 80)] })[0] === "B07");
    c("RZ: below 65% → Bulwark Charge", first(RZ, { round: 4, dist: 4, hpPct: 60 })[0] === "B23");
    c("RZ: below 40% with Bulwark on cooldown → Second Wind", first(RZ, { round: 4, dist: 4, hpPct: 35, cooldowns: { B23: 1 } })[0] === "S35");
    const cycle = first(RZ, { round: 4, dist: 5, cooldowns: { B13: 1 } });
    c("RZ: Hexweave on cooldown → Feast of Marrow", cycle[0] === "B15", cycle);
  });
  it("never gives up across 8 rounds", () => {
    const { log, others } = playRounds(RZ, scene(RZ, { dist: 4, round: 1 }), 8);
    c("RZ: no exhaustion give-up over 8 rounds", !log.some((l) => l.acts.includes("GAVE_UP")), log);
    ev.put("RZ.rounds", log.map((l) => `${l.round}:${l.acts.join("+")}`));
    ev.put("RZ.cloneTurns", others.map((o) => `${o.round}:${o.actor}:${o.act}`));
    c("RZ: exactly one Split Image over 8 rounds", log.flatMap((l) => l.acts).filter((a) => a === "B06").length === 1, log);
  });
});

describe("A5 The Grand Marshal — roster §4 priorities (candidate kit)", () => {
  it("suppression, clears, anti-kite, execute, martial law", () => {
    c("GM: opening Sovereign Ruin", first(GM, { dist: 4 })[0] === "B12");
    c("GM: Ruin on cooldown → Malediction", first(GM, { dist: 4, cooldowns: { B12: 1 } })[0] === "B11");
    c("GM: close high-IDG target → Unraveling Strike", first(GM, { dist: 3, cooldowns: { B12: 1, B11: 1 }, playerEffects: [fx("increasedamagegiven", 80)] })[0] === "S31");
    c("GM: far high-IDG target → Nullifying Wave", first(GM, { dist: 6, cooldowns: { B12: 1, B11: 1 }, playerEffects: [fx("increasedamagegiven", 80)] })[0] === "B32");
    c("GM: kiting at 5 → Sovereign Undertow", first(GM, { dist: 5, cooldowns: { B12: 1, B11: 1 } })[0] === "B03");
    c("GM: stunned target → Cataclysm Detonation", first(GM, { dist: 3, cooldowns: { B12: 1, B11: 1, B30: 1, B17: 1 }, playerEffects: [fx("stun", 100, 2)] })[0] === "B14");
    const ml = first(GM, { dist: 3, hpPct: 50, cooldowns: { B12: 1, B11: 1, B30: 1, B17: 1, B14: 1 } });
    c("GM below 55%: Martial Law Bulwark Charge in the rotation", ml.includes("B23"), ml);
  });
  it("never gives up; documents stacked suppression for the director", () => {
    const { battle, log } = playRounds(GM, scene(GM, { dist: 4, round: 1 }), 8);
    c("GM: no exhaustion give-up over 8 rounds", !log.some((l) => l.acts.includes("GAVE_UP")), log);
    ev.put("GM.rounds", log.map((l) => `${l.round}:${l.acts.join("+")}`));
    const ddg = battle.usersEffects.filter((e) => e.targetId === HUMAN && e.type === "decreasedamagegiven");
    ev.put("GM.playerDDGStackAfter8", ddg.map((e) => ({ power: e.power, rounds: e.rounds })));
  });
});

describe("A6 Supreme Commander Arakane — 20-rule profile", () => {
  it("rule-by-rule behaviour", () => {
    c("AR rule 3: round 1 opens with Apex Hunger", first(AR, { round: 1, dist: 4 })[0] === "B18");
    const kite = first(AR, { round: 3, dist: 9 });
    c("AR rule 4: kiting target ≥7 early → Veilstep", kite[0] === "B09", kite);
    const st = first(AR, { round: 3, dist: 5, aiEffects: [fx("stealth", 100, 1)] });
    c("AR rule 5: stealthed in range → Countermand item, then weapons only (no jutsu while stealthed)", st[0] === "X:COUNTERMAND" && !st.some((a) => AR.kit.includes(a)), st);
    c("AR rule 6: own Afterburn → Purging Stance", first(AR, { round: 3, dist: 4, aiEffects: [fx("afterburn", 30, 2)] })[0] === "S34");
    c("AR rule 7: target shield → Zephyr Lance", first(AR, { round: 3, dist: 4, playerEffects: [fx("shield", 100)] })[0] === "EA04");
    const copy = first(AR, { round: 3, dist: 4, playerEffects: [fx("increasedamagegiven", 80)] });
    c("AR rules 8–9: high IDG → Stolen Form then Countermand (60+40 AP)", copy.join() === "B07,X:COUNTERMAND", copy);
    // validate.py lint L18 says Clear is "excluded from item union"; check the engine actually applies it from the item.
    const cm = aiTurn(AR, scene(AR, { round: 3, dist: 5, aiEffects: [fx("stealth", 100, 1)], playerEffects: [fx("increasedamagegiven", 80, 3), fx("decreasedamagetaken", 30, 3)] }));
    const left = cm.battle.usersEffects.filter((e) => e.targetId === HUMAN && ["increasedamagegiven", "decreasedamagetaken"].includes(e.type));
    ev.put("AR.countermandClearResult", { acts: cm.acts, playerBuffsLeft: left.map((e) => ({ type: e.type, rounds: e.rounds })) });
    c("Countermand (item) Clear strips the player's positive effects in combat (resolves validate.py L18 against the engine)", cm.acts[0] === "X:COUNTERMAND" && left.length === 0, { acts: cm.acts, left: left.map((e) => e.type) });
    const std = first(AR, { round: 3, dist: 4 });
    c("AR rules 10+17: Hexweave then a 40 AP weapon", std[0] === "B13" && std.length === 2, std);
    const close = first(AR, { round: 3, dist: 3, aiEffects: [fx("stealth", 100, 1)], cooldowns: { "X:COUNTERMAND": 1, "SEED:Solar Bow": 1 } });
    c("AR rule 18: stealthed at 3 with Countermand/Solar Bow on cooldown → Crossbow", close[0] === "SEED:Crossbow", close);
    c("AR rule 1: HP 29% → The Last Directive", first(AR, { round: 6, dist: 4, hpPct: 29 })[0] === "X:LAST_DIRECTIVE");
    c("AR rule 1 boundary: HP exactly 30% does NOT trigger (health_below strict)", first(AR, { round: 6, dist: 4, hpPct: 30 })[0] !== "X:LAST_DIRECTIVE");
    const fs = first(AR, { round: 6, dist: 4, hpPct: 25, cooldowns: { "X:LAST_DIRECTIVE": 1 }, aiEffects: [fx("finalstand", 100, 3)] });
    c("AR rule 2: active Final Stand in range → Extermination Order", fs[0] === "X:EXTERMINATION_ORDER", fs);
    const noFs = first(AR, { round: 6, dist: 4, hpPct: 25, cooldowns: { "X:LAST_DIRECTIVE": 1 } });
    c("AR rule 2: no Final Stand → never Extermination Order", !noFs.includes("X:EXTERMINATION_ORDER"), noFs);
  });
  it("Final Stand expiry through the router's own alignBattle → performAIaction order", () => {
    // As first drafted (cooldown 2): reproduce the hazard.
    const b = scene(AR, { round: 6, dist: 4, hpPct: 25 });
    const xo = jutsuId("X:EXTERMINATION_ORDER");
    (b.extraState.jutsus as Record<string, { cooldown: number }>)[xo]!.cooldown = 2;
    b.usersState.find((x) => x.userId === AI)!.jutsus.find((j) => j.jutsuId === xo)!.originalCooldown = 2;
    const { decisions } = playRounds(AR, b, 9);
    ev.put("AR.finalPhaseDecisions", decisions);
    const ultimates = decisions.filter((d) => d.act === "X:EXTERMINATION_ORDER");
    const stale = ultimates.filter((d) => !d.finalStand.active);
    c("AR: The Last Directive cast once in the final phase", decisions.filter((d) => d.act === "X:LAST_DIRECTIVE").length === 1, decisions);
    c("AR: Extermination Order cast while Final Stand is active", ultimates.some((d) => d.finalStand.active), decisions);
    ev.finding("AR1", "Extermination Order is chosen at a decision where Final Stand has already reached 0 rounds: routers/combat.ts runs alignBattle (lowers rounds to 0, no pruning) then performAIaction, and has_effect sums raw power without isEffectActive — 'only while Final Stand is active' is not guaranteed by the authored rule 2",
      stale.length > 0, stale);
    const stale0 = first(AR, { round: 9, dist: 4, hpPct: 20, cooldowns: { "X:LAST_DIRECTIVE": 1 }, aiEffects: [fx("finalstand", 100, 0)] });
    ev.put("AR.staleZeroRoundFinalStandChoice", stale0);
  });
  it("AR1 content-only probe: does an Extermination Order cooldown keep the expired-Final-Stand decision unreachable?", () => {
    const xo = jutsuId("X:EXTERMINATION_ORDER");
    const table: Record<string, { casts: number; activeCasts: number; staleCasts: number }> = {};
    for (const cd of [2, 3, 4, 5, 6, 7]) for (const dist of [4, 7, 9]) {
      const b = scene(AR, { round: 6, dist, hpPct: 25 });
      (b.extraState.jutsus as Record<string, { cooldown: number }>)[xo]!.cooldown = cd;
      b.usersState.find((x) => x.userId === AI)!.jutsus.find((j) => j.jutsuId === xo)!.originalCooldown = cd;
      const { decisions } = playRounds(AR, b, 10);
      const casts = decisions.filter((d) => d.act === "X:EXTERMINATION_ORDER");
      table[`cd${cd}.dist${dist}`] = { casts: casts.length, activeCasts: casts.filter((d) => d.finalStand.active).length, staleCasts: casts.filter((d) => !d.finalStand.active).length };
    }
    ev.put("AR1.cooldownProbe", table);
    const safeCds = [2, 3, 4, 5, 6, 7].filter((cd) => [4, 7, 9].every((d) => table[`cd${cd}.dist${d}`]!.staleCasts === 0 && table[`cd${cd}.dist${d}`]!.activeCasts > 0));
    ev.put("AR1.cooldownsWithNoStaleCastInProbe", safeCds);
    const candidateCd = Number(jutsuRecord("X:EXTERMINATION_ORDER").cooldown);
    c(`AR1 mitigation: candidate Extermination Order cooldown ${candidateCd} never casts on an expired Final Stand and still casts while active in every probe`, safeCds.includes(candidateCd), { candidateCd, safeCds });
    c("AR1 probe ran for cooldowns 2–7 at start distances 4/7/9", Object.keys(table).length === 18);
  });
  it("never gives up: kiting, stealth and close range over 8 rounds", () => {
    for (const dist of [3, 9]) {
      const { log } = playRounds(AR, scene(AR, { dist, round: 1 }), 8);
      c(`AR dist ${dist}: no exhaustion give-up over 8 rounds`, !log.some((l) => l.acts.includes("GAVE_UP")), log);
      ev.put(`AR.rounds.dist${dist}`, log.map((l) => `${l.round}:${l.acts.join("+")}`));
    }
  });
});

describe("A7 regulars — every regular acts and never gives up", () => {
  for (const u of regulars.units) {
    it(u.key, () => {
      const close = first(u, { dist: 4 });
      c(`${u.key}: at range 4 the first action is an equipped kit jutsu`, !!close[0] && u.kit.includes(close[0]), close);
      const far = first(u, { dist: 9 });
      c(`${u.key}: at range 9 it closes in (move) or self-buffs, never gives up`, far.includes("move") && !far.includes("GAVE_UP"), far);
      const { log } = playRounds(u, scene(u, { dist: 6, round: 1 }), 6);
      c(`${u.key}: no exhaustion give-up over 6 rounds`, !log.some((l) => l.acts.includes("GAVE_UP")), log);
      ev.put(`${u.key}.rounds`, log.map((l) => `${l.round}:${l.acts.join("+")}`));
    });
  }
});

requireClean(ev);
