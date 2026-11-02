/**
 * The Mother of Echoes: proofs of the five risky mechanics (offline, engine-executed; zero live requests).
 *   TNR_SCRIPT=moe_probe.ts run.sh [--only P1a,P3] [--out /abs/results/moe_probe.json]
 * Each probe is a minimal QUEST battle on the real encounter records (engine/moe_lib.ts) or a one-purpose probe record,
 * stepped through the engine's own loop (alignBattle -> performAIaction / performBattleAction). Verdicts are printed and
 * written with the raw step logs.
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { performAIaction } from "@/libs/combat/ai_v2";
import { availableUserActions, actionPointsAfterAction, performBattleAction, stillInBattle } from "@/libs/combat/actions";
import { alignBattle, getBattleGrid } from "@/libs/combat/util";
import { jutsu, tag, T } from "./kitlib";
import { C, R, type Cell } from "./cclib";
import { loadDmgConfig, PLAYER_VARIANTS } from "./model";
import { assembleFloor, mulberry32, seedEntropy, tickClock } from "./sim";
import {
  AI, aiRecords, buildPlayer, buildRecords, CYCLES, JID, MK, moeParams, nextComboAction, playerJutsuCatalog, playerModel, rowOf, setDmgConfig, setGearOverride, validateAll,
} from "./moe_lib";

const args = process.argv.slice(2);
const opt = (k: string) => { const i = args.indexOf(`--${k}`); return i >= 0 ? args[i + 1] : undefined; };
const only = opt("only")?.split(",");
const H = process.env.TNR_HARNESS!;
const dmg = loadDmgConfig(H, "live");
setDmgConfig(dmg.config);
const PRAW = opt("params") ? JSON.parse(require("node:fs").readFileSync(opt("params")!, "utf8")) : {};
if (PRAW.gear) setGearOverride(PRAW.gear);
const P = moeParams(opt("params") ? JSON.parse(require("node:fs").readFileSync(opt("params")!, "utf8")) : {});
const RECS = buildRecords(P);
const CAT = playerJutsuCatalog();
const out: any = { generatedBy: "engine/moe_probe.ts", engine: "theninjarpg 3314d122 (git archive, offline)", probes: {} as Record<string, any> };

type Scripted = { id: string; at: Cell } | null;
/** One battle: player (model + optional rule override) vs the given AI rows; returns a step log. */
const stepper = async (o: {
  seed?: number; rows: Record<string, any>; targets: string[]; positions?: Record<string, Cell>; playerAt?: Cell; model?: string | ReturnType<typeof playerModel>; playerRules?: any[];
  pets?: number; rounds: number; script?: (b: any, round: number, puid: string) => Scripted; onStep?: (b: any, s: any) => void; mutate?: (b: any, round: number) => void;
}) => {
  const seed = o.seed ?? 1;
  const rand = mulberry32(seed);
  const orig = Math.random;
  Math.random = rand;
  seedEntropy(seed);
  try {
    const m = typeof o.model === "object" ? structuredClone(o.model) : playerModel(o.model ?? "elite");
    if (o.playerRules) m.variant = { ...m.variant, rules: o.playerRules };
    m.pets = o.pets ?? 0;
    const player = buildPlayer(m, CAT);
    let b: any = await assembleFloor({ players: [player], enemyRows: o.rows, floor: { kind: "boss", waves: [{ aiIds: o.targets, delayRounds: 0 }] }, rand, initialBarriers: false, dmgConfig: dmg.config, mode: "quest" });
    for (const [id, r] of Object.entries(RECS)) if (!b.extraState.jutsus[id]) b.extraState.jutsus[id] = r;
    const puid = player.userId;
    const pu = () => b.usersState.find((u: any) => u.userId === puid);
    if (o.playerAt) [pu().longitude, pu().latitude] = o.playerAt;
    for (const [aid, c] of Object.entries(o.positions ?? {})) { const u = b.usersState.find((x: any) => x.controllerId === aid); if (u) [u.longitude, u.latitude] = c; }
    const grid = getBattleGrid(1, b);
    const ar: number[] = [];
    const steps: any[] = [];
    const nm = (id?: string) => (id ? (b.extraState.jutsus[id]?.name ?? id) : "none");
    for (let i = 0; i < o.rounds * 40; i++) {
      const pre = alignBattle(b, ar, puid);
      if (!ar.includes(pre.actionRound)) ar.push(pre.actionRound);
      if (b.round > o.rounds) break;
      o.mutate?.(b, b.round);
      tickClock(1000);
      const actor = pre.actor;
      const hp0 = new Map(b.usersState.map((u: any) => [u.userId, u.curHealth]));
      const fx0 = new Set(b.usersEffects.map((e: any) => e.id));
      let actionId: string | undefined;
      const sc = actor.userId === puid && o.script ? o.script(b, b.round, puid) : null;
      if (sc) {
        const action = availableUserActions(b, puid, true, true).find((a: any) => a.id === sc.id);
        if (action && actionPointsAfterAction(actor, b, action).canAct) {
          try { b = performBattleAction({ battle: structuredClone(b), action, grid, contextUserId: puid, actorId: puid, longitude: sc.at[0], latitude: sc.at[1] }).newBattle; actionId = sc.id; }
          catch (e: any) { actionId = `FAILED ${sc.id}: ${String(e.message ?? e).slice(0, 60)}`; const r = performAIaction(b, grid, actor.userId); b = r.nextBattle; }
        } else { actionId = `UNAVAILABLE ${sc.id}`; const r = performAIaction(b, grid, actor.userId); b = r.nextBattle; }
      } else {
        const r = performAIaction(b, grid, actor.userId);
        b = r.nextBattle;
        actionId = r.nextActionId;
      }
      alignBattle(b, ar, puid);
      if (!actionId && actor.isAutoCombat) b.roundStartAt = new Date(Date.now() - 61_000);
      const s = {
        round: pre.actionRound, actor: actor.userId === puid ? "player" : actor.username, actorUid: actor.userId, action: nm(actionId), actionId,
        hp: Object.fromEntries(b.usersState.filter((u: any) => Math.round(u.curHealth - (hp0.get(u.userId) ?? u.curHealth)) !== 0).map((u: any) => [u.userId === puid ? "player" : u.username, Math.round(u.curHealth - (hp0.get(u.userId) ?? 0))])),
        newFx: b.usersEffects.filter((e: any) => !fx0.has(e.id)).map((e: any) => `${e.type}:${e.power}:r${e.rounds}->${e.targetId === puid ? "player" : b.usersState.find((u: any) => u.userId === e.targetId)?.username}`),
      };
      o.onStep?.(b, s);
      steps.push(s);
      const side = (dir: string) => b.usersState.some((u: any) => u.direction === dir && !u.isSummon && stillInBattle(u, b.usersEffects));
      if (!stillInBattle(pu(), b.usersEffects) || !side("right")) break;
    }
    return { steps, b, puid };
  } finally {
    Math.random = orig;
  }
};
const recs = aiRecords(P);
const recOf = (id: string) => recs.find((r) => r.id === id)!;
const rowsFor = (ids: string[], edit: Record<string, (a: any) => any> = {}) => Object.fromEntries(ids.map((id) => {
  const a = structuredClone(recOf(id));
  const e = edit[id] ? edit[id]!(a) : a;
  return [id, rowOf(e, RECS, P)];
}));
const passive = [R.end()];
const fxOf = (b: any, uid: string) => b.usersEffects.filter((e: any) => e.targetId === uid).map((e: any) => `${e.type}:${e.power}:r${e.rounds}${e.castThisRound ? "*" : ""}`);
const log = (k: string, lines: string[]) => { console.log(`\n### ${k}`); for (const l of lines) console.log("  " + l); };
const want = (k: string) => !only || only.includes(k);

/* ---------------------------------------------------------------- P0: static validation */
{
  const issues = validateAll(P);
  out.probes.P0 = { issues, records: Object.keys(RECS).length, ais: recs.length };
  log("P0 static validation", [issues.length ? issues.join("\n  ") : `all ${Object.keys(RECS).length} jutsu (JutsuValidator) and ${recs.length} AI records / rules (AiRule, insertAiSchema, <=20 rules, unconditional last rule) valid`]);
}

/* ---------------------------------------------------------------- P1a: marker lifetimes (rounds semantics, L3) */
if (want("P1a")) {
  const types = ["increaserange", "fleeprevent", "robprevent", "onehitkillprevent", "sealprevent", "disarm"];
  const probeJ = jutsu("moe-probe-markers", { name: "Probe: six markers, rounds 0..5", description: "probe", battleDescription: "probe", target: "SELF", method: "SINGLE", range: 0, cooldown: 99, actionCostPerc: 40,
    effects: types.map((t, i) => tag(t, { power: ["increaserange"].includes(t) ? 1 : 100, rounds: i, target: "SELF", ...(t === "increaserange" ? { actionsAffected: [], calculation: "static" } : {}) })) });
  RECS[probeJ.id] = probeJ;
  // A boss that casts it on round 1, then on every later turn checks has_effect for each type (rules record which match).
  const rules = [R.jutsu(probeJ.id, "SELF", [{ type: "specific_round", value: 1, description: "" }]), ...types.map((t) => R.end([C.has(t)])), R.end()];
  const rows = rowsFor([AI.sayo2, AI.porter, AI.hana, AI.tomo], { [AI.sayo2]: (a) => ({ ...a, jutsus: [...a.jutsus, probeJ.id], rules, effects: [] }) });
  const lines: string[] = [];
  const g = globalThis as any;
  const matched: any[] = [];
  g.__TNR_RULE_PROBE__ = (p: any) => matched.push(p);
  const { steps } = await stepper({ rows, targets: [AI.sayo2], positions: { [AI.sayo2]: [9, 5] }, playerAt: [2, 5], playerRules: passive, rounds: 7,
    onStep: (b, s) => { if (s.actor !== "player") { const u = b.usersState.find((x: any) => x.controllerId === AI.sayo2); lines.push(`r${s.round} boss ${s.action.padEnd(28)} rule#${matched.at(-1)?.ruleIndex ?? "?"} fx after: ${fxOf(b, u.userId).join(" ")}`); } } });
  g.__TNR_RULE_PROBE__ = undefined;
  // rule index 0 = cast; 1..6 = has_effect type[i] (rounds i); the first matching end-turn rule shows the longest-lived marker still counted.
  out.probes.P1a = { types: types.map((t, i) => `${t} rounds ${i}`), lines, steps };
  log("P1a marker lifetimes: cast at r1 with rounds 0..5 (rule k+1 = has_effect of the marker with rounds k)", lines);
}

/* ---------------------------------------------------------------- P1b: Recast by use_combo_action (Act II record) */
if (want("P1b")) {
  for (const variant of ["passive player", "player stuns her (stunprevent off)"]) {
    const stun = variant.includes("stuns");
    const rows = rowsFor([AI.sayo2, AI.porter, AI.hana, AI.tomo], stun ? { [AI.sayo2]: (a) => ({ ...a, effects: a.effects.filter((e: any) => e.type !== "stunprevent") }) } : {});
    const seq: string[] = [];
    const usedTrail: string[] = [];
    const { steps } = await stepper({ rows, targets: [AI.sayo2], positions: { [AI.sayo2]: [8, 5] }, playerAt: [3, 5], rounds: 60,
      playerRules: stun ? [R.jutsu("VT7oxj_fObWuQa3Rq_BbI", "CLOSEST_OPPONENT", [C.near(4)]), { conditions: [C.far(4)], action: { type: "move_towards_opponent", target: "CLOSEST_OPPONENT", description: "" } }, R.end()] : passive,
      mutate: (b) => { const pu = b.usersState.find((u: any) => !u.isAi && !u.petId); if (pu) pu.curHealth = pu.maxHealth; },
      onStep: (b, s) => { if (s.actor?.startsWith("Sayo")) { seq.push(`r${s.round}:${s.action}${s.actionId?.startsWith("moe-etching") || s.actionId?.startsWith("moe-recast") ? "(" + s.actionId.slice(-1).toUpperCase() + ")" : ""}`); const u = b.usersState.find((x: any) => x.controllerId === AI.sayo2); usedTrail.push(...[]); if (s.action === "End Turn" || s.actionId === "wait") usedTrail.push(`r${s.round} used tail: ${(u.usedActions ?? []).slice(-3).map((a: any) => a.id).join(",")}`); } } });
    // Verify order: for each cycle, the detonation order equals the etching order, and no detonation precedes its etching.
    const acts = seq.map((x) => x.split(":")[1]!);
    const cycles: { etch: string[]; det: string[] }[] = [];
    let cur = { etch: [] as string[], det: [] as string[] };
    for (const a of acts) {
      const m = a.match(/\(([A-E])\)$/);
      if (a.startsWith("Etching")) { if (cur.det.length) { cycles.push(cur); cur = { etch: [], det: [] }; } cur.etch.push(m![1]!); }
      else if (a.startsWith("Recast")) cur.det.push(m![1]!);
      else if (a.startsWith("The Glass Falls Quiet")) { cycles.push(cur); cur = { etch: [], det: [] }; }
    }
    if (cur.etch.length || cur.det.length) cycles.push(cur);
    const verdict = cycles.map((c, i) => ({ cycle: i + 1, etched: c.etch.join(""), detonated: c.det.join(""), designed: CYCLES[i]?.join("") ?? "-", inOrder: c.det.join("") === c.etch.join("").slice(0, c.det.length) }));
    out.probes[`P1b ${variant}`] = { sequence: seq, cycles: verdict, waitTrail: usedTrail.slice(0, 12), steps: steps.length };
    log(`P1b Recast via use_combo_action, ${variant}`, [...verdict.map((v) => JSON.stringify(v)), `sequence: ${seq.join(" ")}`.slice(0, 1500), ...usedTrail.slice(0, 6)]);
  }
}

/* ---------------------------------------------------------------- P1c: weakness x3 during recast */
if (want("P1c")) {
  const lines: string[] = [];
  const rows = rowsFor([AI.sayo2, AI.porter, AI.hana, AI.tomo]);
  const hits: { round: number; recastWindow: boolean; dmg: number }[] = [];
  await stepper({ rows, targets: [AI.sayo2], positions: { [AI.sayo2]: [5, 5] }, playerAt: [4, 5], rounds: 12,
    playerRules: [R.jutsu("basicAttack", "CLOSEST_OPPONENT", []), R.end()],
    mutate: (b) => { const pu = b.usersState.find((u: any) => !u.isAi && !u.petId); if (pu) { pu.curHealth = pu.maxHealth; pu.basicActions = []; } const s = b.usersState.find((u: any) => u.controllerId === AI.sayo2); if (s) s.curHealth = s.maxHealth; },
    onStep: (b, s) => { if (s.actor === "player" && s.actionId === "basicAttack") { const u = b.usersState.find((x: any) => x.controllerId === AI.sayo2); const weak = b.usersEffects.some((e: any) => e.targetId === u.userId && e.type === "weakness"); hits.push({ round: s.round, recastWindow: weak, dmg: -(s.hp[u.username] ?? 0) }); } } });
  const avg = (w: boolean) => { const xs = hits.filter((h) => h.recastWindow === w).map((h) => h.dmg); return xs.length ? Math.round(xs.reduce((a, c) => a + c, 0) / xs.length) : null; };
  out.probes.P1c = { hits, meanOutside: avg(false), meanInWindow: avg(true) };
  log("P1c weakness during recast (player basic attack on Sayo; her HP reset each step)", [JSON.stringify(hits), `mean outside ${avg(false)} vs in window ${avg(true)}`]);
}

/* ---------------------------------------------------------------- P2: Cradle */
if (want("P2")) {
  const lines: string[] = [];
  const rows = rowsFor([AI.sayo1, AI.silence, AI.feeler, AI.likeness]);
  const hits: { round: number; cradle: boolean; dmg: number }[] = [];
  let clearTried = 0;
  await stepper({ rows, targets: [AI.sayo1, AI.silence], positions: { [AI.sayo1]: [5, 5], [AI.silence]: [11, 4] }, playerAt: [4, 5], rounds: 12,
    playerRules: [R.jutsu("basicAttack", "CLOSEST_OPPONENT", []), R.end()],
    script: (b, round) => { if (round === 4 && clearTried++ === 0) { const s = b.usersState.find((u: any) => u.controllerId === AI.sayo1); return { id: "clear", at: [s.longitude, s.latitude] }; } return null; },
    mutate: (b, round) => {
      const pu = b.usersState.find((u: any) => !u.isAi && !u.petId); if (pu) { pu.curHealth = pu.maxHealth; pu.basicActions = []; }
      const sy = b.usersState.find((u: any) => u.controllerId === AI.sayo1); if (sy) { sy.curHealth = sy.maxHealth; [sy.longitude, sy.latitude] = [5, 5]; }
      if (round === 7) for (const f of b.usersState.filter((u: any) => u.isSummon && u.username?.startsWith("A Feeler"))) if (f.curHealth > 0) { f.curHealth = 0; lines.push("-- round 7: feeler killed --"); }
    },
    onStep: (b, s) => {
      const sy = b.usersState.find((x: any) => x.controllerId === AI.sayo1); const si = b.usersState.find((x: any) => x.controllerId === AI.silence);
      const cr = b.usersEffects.some((e: any) => e.targetId === sy.userId && e.type === "decreasedamagetaken" && e.power === -P.pw.cradleDR || (e.targetId === sy.userId && e.type === "decreasedamagetaken" && Math.abs(e.power) === P.pw.cradleDR));
      if (s.actor === "player" && s.actionId === "basicAttack") hits.push({ round: s.round, cradle: cr, dmg: -(s.hp[sy.username] ?? 0) });
      if (s.actor?.startsWith("A Feeler") || s.action === "clear" || s.actor === "player") lines.push(`r${s.round} ${String(s.actor).padEnd(22)} ${String(s.action).padEnd(14)} hp ${JSON.stringify(s.hp)} | Sayo: ${fxOf(b, sy.userId).filter((x: string) => /^(decreasedamagetaken|clearprevent)/.test(x)).join(" ")} | Silence: ${fxOf(b, si.userId).filter((x: string) => /^(decreasedamagetaken|clearprevent)/.test(x)).join(" ")}`);
    } });
  const avg = (w: boolean) => { const xs = hits.filter((h) => h.cradle === w).map((h) => h.dmg); return xs.length ? Math.round(xs.reduce((a, c) => a + c, 0) / xs.length) : null; };
  out.probes.P2 = { hits, meanWithCradle: avg(true), meanWithout: avg(false), lines };
  log("P2 Cradle (feeler -> HIGHEST_MAX_HEALTH_ALLY; player Clear on Sayo at round 4; feeler killed at round 7)", [...lines, JSON.stringify(hits), `mean basic-attack damage on Sayo: with Cradle ${avg(true)}, without ${avg(false)}`]);
}

/* ---------------------------------------------------------------- P3: healprevent vs sustain */
if (want("P3")) {
  const hp = jutsu("moe-probe-healprevent", { name: "Probe: healprevent 6 rounds", description: "probe", battleDescription: "probe", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 99, actionCostPerc: 40, effects: [tag("healprevent", { power: 100, rounds: 6 })] });
  const hit = jutsu("moe-probe-hit", { name: "Probe: hit", description: "probe", battleDescription: "probe", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 0, actionCostPerc: 60, effects: [T.damage(40)] });
  RECS[hp.id] = hp; RECS[hit.id] = hit;
  const cases: { label: string; script?: string; gear?: number; siphon?: number }[] = [
    { label: "gear lifesteal 25% (row from round 0), basic attacks", gear: 25 },
    { label: "Eclipse Drain lifesteal 35% cast AFTER the prevent", script: "ou7VyChQ-SFCm8T8yGS7I" },
    { label: "Black Crow vamp 40%", script: "c-yTyBUJil8MzlAIHApUG" },
    { label: "innate siphon 25% (shields from damage taken)", siphon: 25 },
    { label: "Inner Flame absorb 20% cast AFTER the prevent", script: "kUcL8K94TW3iCkRcoik_7" },
    { label: "Rejuvenating-style heal: basic heal action", script: "basicHeal" },
  ];
  const resP3: any[] = [];
  for (const withPrevent of [false, true]) for (const cs of cases) {
    const rules = [...(withPrevent ? [R.jutsu(hp.id, "CLOSEST_OPPONENT", [{ type: "specific_round", value: 1, description: "" }])] : []), R.jutsu(hit.id, "CLOSEST_OPPONENT", []), R.end()];
    const rows = rowsFor([AI.saint], { [AI.saint]: (a) => ({ ...a, jutsus: [...a.jutsus, hp.id, hit.id], rules, effects: [] }) });
    const m = playerModel("elite", { lifesteal: cs.gear ?? 0, siphon: cs.siphon ?? 0 });
    // Round 1: the player only ends its turn (the boss lays healprevent after it). From round 2: the case's action once, then basic attacks.
    const prules = [R.jutsu("basicAttack", "CLOSEST_OPPONENT", [{ type: "round_greater_than", value: 1, description: "" }]), R.end()];
    let gained = 0, shields = 0, used = false; const hitNet: number[] = [];
    const lines: string[] = [];
    await stepper({ rows, targets: [AI.saint], positions: { [AI.saint]: [5, 5] }, playerAt: [4, 5], rounds: 5, model: m, playerRules: prules, seed: 3,
      script: (b, round) => { if (round >= 2 && cs.script && !used) { used = true; const sy = b.usersState.find((u: any) => u.controllerId === AI.saint); return { id: cs.script, at: cs.script.startsWith("c-") ? [sy.longitude, sy.latitude] : [4, 5] }; } return null; },
      mutate: (b, round) => { const pu = b.usersState.find((u: any) => !u.isAi && !u.petId); if (pu && round === 1 && !pu.__half) { pu.curHealth = Math.round(pu.maxHealth / 2); pu.__half = true; } const sy = b.usersState.find((u: any) => u.controllerId === AI.saint); if (sy) sy.curHealth = sy.maxHealth; },
      onStep: (b, s) => { const pd = s.hp.player ?? 0; if (pd > 0) gained += pd; if (s.actionId === hit.id && s.round >= 3) hitNet.push(pd); const pu = b.usersState.find((u: any) => !u.isAi && !u.petId); const sh = b.usersEffects.filter((e: any) => e.type === "shield" && e.targetId === pu?.userId); shields = Math.max(shields, sh.reduce((a: number, e: any) => a + (e.health ?? e.power ?? 0), 0)); lines.push(`r${s.round} ${s.actor.slice(0, 12)} ${s.action.slice(0, 26)} hp ${JSON.stringify(s.hp)} ${s.newFx.join(",")}`); } });
    resP3.push({ healprevent: withPrevent, case: cs.label, hpGained: gained, maxShield: Math.round(shields), netOnBossHitsFromR3: hitNet, lines });
  }
  // gear/siphon need the model flags: re-run handled by playerModel options above via stepper's model? (applied through buildPlayer)
  out.probes.P3 = resP3;
  log("P3 healprevent vs sustain (player at 50% HP; HP regained on any step over 5 rounds; max shield)", resP3.map((r) => `${r.healprevent ? "PREVENT" : "control"} | ${r.case.padEnd(52)} | +${r.hpGained} HP | shield ${r.maxShield} | net HP on boss hits r3+: ${r.netOnBossHitsFromR3.join(",")}`));
}

/* ---------------------------------------------------------------- P4: Hush pools */
if (want("P4")) {
  const lines: string[] = [];
  const rows = rowsFor([AI.silence, AI.feeler], { [AI.silence]: (a) => ({ ...a, rules: [R.jutsu(JID.hush[1]!, "SELF", [{ type: "round_greater_than", value: 3, description: "" }]), R.jutsu(JID.hush[0]!, "SELF", []), R.jutsu(JID.hushUnbridled, "SELF", [{ type: "round_greater_than", value: 6, description: "" }]), R.end()] }) });
  let healTry = 0;
  const { steps } = await stepper({ rows, targets: [AI.silence], positions: { [AI.silence]: [11, 4] }, playerAt: [3, 5], rounds: 9, playerRules: passive,
    script: (b, round, puid) => {
      // Round 2: the player walks onto the nearest pool; afterwards it stands still and tries to basic-heal on round 4.
      const pu = b.usersState.find((u: any) => u.userId === puid);
      const pools = b.groundEffects.filter((g: any) => g.type === "healprevent");
      if (round === 2 && pools.length) { const t = pools.map((g: any) => [g.longitude, g.latitude] as Cell).sort((a: Cell, c: Cell) => Math.abs(a[0] - pu.longitude) + Math.abs(a[1] - pu.latitude) - Math.abs(c[0] - pu.longitude) - Math.abs(c[1] - pu.latitude))[0]; if (t && !(t[0] === pu.longitude && t[1] === pu.latitude)) return { id: "replacementTechnique", at: t }; }
      if (round === 4 && healTry++ === 0) return { id: "basicHeal", at: [pu.longitude, pu.latitude] };
      return null;
    },
    onStep: (b, s) => {
      const ge = b.groundEffects.filter((g: any) => g.type !== "visual");
      const byType: Record<string, number> = {};
      for (const g of ge) byType[`${g.type}:r${g.rounds}`] = (byType[`${g.type}:r${g.rounds}`] ?? 0) + 1;
      const pu = b.usersState.find((u: any) => !u.isAi && !u.petId);
      const onPool = ge.some((g: any) => g.longitude === pu.longitude && g.latitude === pu.latitude);
      lines.push(`r${s.round} ${String(s.actor).padEnd(12)} ${String(s.action).padEnd(26)} p@${pu.longitude},${pu.latitude}${onPool ? " ON POOL" : ""} hp ${JSON.stringify(s.hp)} new ${s.newFx.join(",") || "-"} | ground ${JSON.stringify(byType)}`);
    } });
  out.probes.P4 = { lines, steps };
  log("P4 Hush pools (RANDOM seeding, drain + healprevent ground, cadence, Unbridled pools)", lines);
}

/* ---------------------------------------------------------------- P5: kill order */
if (want("P5")) {
  for (const first of ["sayo", "silence"] as const) {
    const lines: string[] = [];
    const rows = rowsFor([AI.sayo1, AI.silence, AI.feeler, AI.likeness]);
    const killId = first === "sayo" ? AI.sayo1 : AI.silence;
    const { steps } = await stepper({ rows, targets: [AI.sayo1, AI.silence], positions: { [AI.sayo1]: [8, 6], [AI.silence]: [11, 4] }, playerAt: [2, 5], rounds: 10, playerRules: passive,
      mutate: (b, round) => { const pu = b.usersState.find((u: any) => !u.isAi && !u.petId); if (pu) pu.curHealth = pu.maxHealth; if (round === 3) { const u = b.usersState.find((x: any) => x.controllerId === killId); if (u && u.curHealth > 0) { u.curHealth = 0; lines.push(`-- round 3: ${u.username} set to 0 HP (killed) --`); } } },
      onStep: (b, s) => { if (s.actor !== "player") lines.push(`r${s.round} ${String(s.actor).padEnd(24)} ${String(s.action).padEnd(28)} ${s.newFx.filter((x: string) => !x.startsWith("visual")).join(",")}`); } });
    out.probes[`P5 ${first} first`] = { lines, steps: steps.length };
    log(`P5 kill order: ${first} killed at round 3`, lines);
  }
}

/* ---------------------------------------------------------------- P6: cleanseprevent while channelling */
if (want("P6")) {
  const lines: string[] = [];
  const rows = rowsFor([AI.saint], { [AI.saint]: (a) => ({ ...a, rules: [R.jutsu(JID.quiet, "CLOSEST_OPPONENT", [C.near(5)]), R.end()] }) });
  await stepper({ rows, targets: [AI.saint], positions: { [AI.saint]: [6, 5] }, playerAt: [4, 5], rounds: 6, playerRules: passive,
    script: (_b, round, puid) => (round >= 2 ? { id: "cleanse", at: [4, 5] } : null),
    mutate: (b) => { const pu = b.usersState.find((u: any) => !u.isAi && !u.petId); if (pu) { pu.curHealth = pu.maxHealth; pu.basicActions = []; } },
    onStep: (b, s) => { const pu = b.usersState.find((u: any) => !u.isAi && !u.petId); lines.push(`r${s.round} ${String(s.actor).padEnd(26)} ${String(s.action).padEnd(26)} player fx: ${fxOf(b, pu.userId).filter((x: string) => /increasedamagetaken|decreaseheal|cleanseprevent/.test(x)).join(" ")}`); } });
  out.probes.P6 = { lines };
  log("P6 The Quiet: cleanse attempts every player turn from round 2 (cleanse cooldown reset each step)", lines);
}

/* ---------------------------------------------------------------- P7: damage calibration (not a proof) */
if (want("P7")) {
  const res: any = {};
  const atk = [...(opt("first") ? [opt("first")!] : []), "c-yTyBUJil8MzlAIHApUG", "mYCbcdDwDzJBul52HiwhC", "nS-iidYFYqWE9Z-UkC84y", "V_VY284CMTuqYqOOX5sa7", "VT7oxj_fObWuQa3Rq_BbI", "basicAttack"];
  const avgKit = ["PQdSt0IDdYFoR44tC3Hvo", "mYCbcdDwDzJBul52HiwhC", "rBcwIiHjKOF07Yoq4wVqU", "nS-iidYFYqWE9Z-UkC84y", "basicAttack"];
  const models: Record<string, any> = {
    elite: playerModel("elite"), average: playerModel("average"),
    elite_nosustain: playerModel("elite", { lifesteal: 0, siphon: 0 }),
    elite_avgkit: (() => { const m = playerModel("elite", { lifesteal: 0, siphon: 0 }); m.variant = { ...m.variant, jutsuIds: PLAYER_VARIANTS.average!.jutsuIds, elements: ["Fire", "Wind"] }; return m; })(),
  };
  const bosses = (opt("bosses") ?? "sayo1,silence,sayo2,saint").split(",").map((k) => (AI as any)[k]);
  for (const mname of (opt("models") ?? "elite,average").split(",")) for (const boss of bosses) {
    const model = models[mname];
    const kit = mname === "elite" || mname === "elite_nosustain" ? atk : avgKit;
    const extra = boss === AI.sayo1 || boss === AI.silence ? [AI.feeler, AI.likeness] : boss === AI.sayo2 ? [AI.porter, AI.hana, AI.tomo] : [];
    const rows = rowsFor([boss, ...extra], { [boss]: (a) => ({ ...a, rules: [R.jutsu(JID.lancet, "CLOSEST_OPPONENT", []), R.end()] }) });
    const dmgBy: Record<string, number[]> = {};
    const taken: number[] = [];
    await stepper({ rows, targets: [boss], positions: { [boss]: [5, 5] }, playerAt: [4, 5], rounds: 4, model, playerRules: [...kit.map((j) => R.jutsu(j, "CLOSEST_OPPONENT", [])), R.end()],
      mutate: (b) => { for (const u of b.usersState) { u.curHealth = u.maxHealth; if (!u.isAi) for (const uj of u.jutsus ?? []) uj.lastUsedRound = -100; } },
      onStep: (b, s) => { const bu = b.usersState.find((u: any) => u.controllerId === boss); if (s.actor === "player" && s.hp[bu.username]) (dmgBy[s.action] ??= []).push(-s.hp[bu.username]); if (s.actionId === JID.lancet) taken.push(-(s.hp.player ?? 0)); } });
    res[`${mname} vs ${boss}`] = { playerHits: Object.fromEntries(Object.entries(dmgBy).map(([k, v]) => [k, Math.round(v.reduce((a, c) => a + c, 0) / v.length)])), lancetOnPlayer: taken };
  }
  out.probes.P7 = res;
  log("P7 damage calibration (mean hit by jutsu, boss HP reset each step; Glass Lancet power " + P.pw.lancet + " on the player)", Object.entries(res).map(([k, v]: any) => `${k}: ${JSON.stringify(v.playerHits)} | lancet on player ${JSON.stringify(v.lancetOnPlayer)}`));
}

const outPath = opt("out");
if (outPath) { mkdirSync(dirname(resolve(outPath)), { recursive: true }); writeFileSync(resolve(outPath), `${JSON.stringify(out, null, 1)}\n`); console.log(`wrote ${outPath}`); }
