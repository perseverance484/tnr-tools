/**
 * Skyglass endgame Wreck boss floor (floor 5: 3 Deck Wardens, then The Captain + the Sealwright), SOLO level-100 player
 * with modelled pets, close-in vs kiting, old vs fixed Captain (RUL-2026-10-31-091; push/398-400).
 *
 *   TNR_SCRIPT=kite.ts run.sh --rules old|new --mode close|kite|poke [--runs 30] [--seed 1] [--pets 2]
 *       [--kite-range 5] [--kite-waves 2] [--uc-cooldown N] [--stunprevent on|off] [--captain-pools 9]
 *       [--variant average] [--max-rounds 150] [--no-dodge] [--out results/kite_<cell>.json]
 *
 * Inputs: overrides/kits_endgame.json (the generated endgame override, read unchanged). The fix is applied IN MEMORY
 * here, restating push/skyglass_captain_fix.gen.py (origin/main) on the harness copy dg-the-captain:
 *   --rules new: rule 13 (Stolen Form) deleted; the last rule (basic attack) gated player_within_range 0..1;
 *                move_towards_opponent CLOSEST_OPPONENT (no conditions) appended (20 rules); innate stunprevent 100 /
 *                99 rounds appended; Unbroken Command (0Y10JpChssDwFUxNRk6p3) cooldown 2 -> 99.
 *   --uc-cooldown / --stunprevent override the two non-rule parts separately (factor isolation).
 *   --captain-pools: the Captain's poolsMultiplier through the same scaleEditedAi aiEdit path (default 9 = the live
 *                record, push/361; the generated override still carries 7.5).
 * Pets: the engine spawns at most one active pet per owner (pets.ts addPetsToBattle). --pets 2 spawns the first through
 * the engine and adds a harness clone of that battle actor (same modelled companion, own id, nearest free cell to the
 * owner, shared pet profile). That second pet is NOT an engine path.
 * Modes: close = the existing auto-player (casts in range, closes in, dodges marks); kite / poke = sim.ts KiteOpts
 * strict / poke, applied in --kite-waves (default 2: the boss wave; wave 1 is played close-in), dodge still first.
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { nanoid } from "nanoid";
import { stillInBattle } from "@/libs/combat/actions";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, petFor, PLAYER_VARIANTS, playerQueryUser } from "./model";
import { assembleFloor, type FloorResult, mulberry32, runFloor, seedEntropy } from "./sim";
import { unmarkedReport } from "./fallback";

const args = process.argv.slice(2);
const opt = (k: string, d?: string) => (args.includes(`--${k}`) ? args[args.indexOf(`--${k}`) + 1] : d);
const H = process.env.TNR_HARNESS!;
const UC = "0Y10JpChssDwFUxNRk6p3";
const CAPTAIN = "dg-the-captain";
const STOLEN_FORM_RULE = 13;
const rulesSet = opt("rules", "old") as "old" | "new";
const mode = opt("mode", "close") as "close" | "kite" | "poke";
const runs = Number(opt("runs", "30"));
const seed0 = Number(opt("seed", "1"));
const petCount = Number(opt("pets", "2"));
const kiteRange = Number(opt("kite-range", "5"));
const kiteWaves = (opt("kite-waves", "2") as string).split(",").map(Number);
const ucCooldown = Number(opt("uc-cooldown", rulesSet === "new" ? "99" : "2"));
const stunprevent = (opt("stunprevent", rulesSet === "new" ? "on" : "off") as string) === "on";
const captainPools = Number(opt("captain-pools", "9"));
const variant = opt("variant", "average")!;
const maxRounds = Number(opt("max-rounds", "150"));
const dodge = !args.includes("--no-dodge");

/* ---- inputs (the generated override is read, never written) ---- */
const ov: any = loadJson(join(H, "overrides/kits_endgame.json"));
const cap = ov.newEnemies[CAPTAIN];
const changes: string[] = [];
cap.aiEdit = { ...(cap.aiEdit ?? {}), poolsMultiplier: captainPools };
changes.push(`dg-the-captain aiEdit.poolsMultiplier -> ${captainPools}`);
if (rulesSet === "new") {
  const rules = structuredClone(cap.rules);
  if (rules.length !== 20 || !String(rules[STOLEN_FORM_RULE].action.description).startsWith("Stolen Form")) throw new Error("captain rules: shape changed");
  if (rules[8].action.jutsuId !== UC || rules[19].action.jutsuId !== "basicAttack") throw new Error("captain rules: rule 8 / 19 changed");
  rules.splice(STOLEN_FORM_RULE, 1);
  rules[rules.length - 1].conditions = [{ type: "player_within_range", description: "", minRange: 0, maxRange: 1 }];
  rules.push({ conditions: [], action: { type: "move_towards_opponent", description: "Close on the nearest player (none in reach)", target: "CLOSEST_OPPONENT" } });
  if (rules.length !== 20) throw new Error("captain rules: not 20");
  cap.rules = rules;
  changes.push("rules: Stolen Form (13) cut; basic attack gated player_within_range 0..1; move_towards_opponent CLOSEST_OPPONENT appended");
}
if (stunprevent) {
  cap.effects = [...(cap.effects ?? []), {
    type: "stunprevent", power: 100, rounds: 99, target: "INHERIT", appearSfx: "", direction: "offence", calculation: "percentage",
    description: "Prevents being stunned", disappearSfx: "", powerPerLevel: 0, appearAnimation: "", staticAnimation: "",
    staticAssetPath: "", disappearAnimation: "",
  }];
  changes.push("effects: + stunprevent 100 / 99 rounds");
}
const baseline = loadJson(join(H, "data/baseline.json"));
const ucRecord = baseline.jutsuCatalog[UC]?.record;
if (!ucRecord || ucRecord.cooldown !== 2) throw new Error("Unbroken Command record: expected captured cooldown 2");
if (ucCooldown !== 2) {
  ov.jutsu = { ...ov.jutsu, [UC]: { ...structuredClone(ucRecord), cooldown: ucCooldown } };
  changes.push(`Unbroken Command cooldown 2 -> ${ucCooldown}`);
}
const t = buildTemplates(baseline, ov);
const v = { ...PLAYER_VARIANTS[variant]!, ...(ov.players?.[variant] ?? {}) };
const donor = t.enemies["texZaFi42S3EvJZBwQ8cd"]!.row;
const rows = Object.fromEntries(Object.entries(t.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
const dmg = loadDmgConfig(H, "live");
const floor = t.floors[4]!;
const capRules: any[] = t.enemies[CAPTAIN]!.profile.rules;
const BASIC: Record<string, string> = { move: "move", wait: "end turn", basicAttack: "basic attack", meditate: "meditate" };
const nameOf = (id: string | null) => (id === null ? "(none)" : (t.jutsu[id]?.name ?? BASIC[id] ?? id));

/** A second companion: a harness clone of the engine-spawned pet actor (the engine allows one per owner). */
const addClonePet = (battle: any, ownerId: string) => {
  const pet = battle.usersState.find((u: any) => u.petId && u.controllerId === ownerId);
  if (!pet) throw new Error("no engine pet to clone");
  const owner = battle.usersState.find((u: any) => u.userId === ownerId);
  const half = Math.floor(battle.width / 2);
  const cells: { x: number; y: number; d: number }[] = [];
  for (let x = 0; x <= half; x++)
    for (let y = 0; y < battle.height; y++) {
      if (battle.usersState.some((u: any) => u.longitude === x && u.latitude === y)) continue;
      cells.push({ x, y, d: Math.abs(x - owner.longitude) + Math.abs(y - owner.latitude) });
    }
  cells.sort((a, b) => a.d - b.d || a.x - b.x || a.y - b.y);
  const c = structuredClone(pet);
  c.userId = nanoid();
  c.petId = `${pet.petId}-harness2`;
  c.username = `${pet.username} (2)`;
  c.longitude = cells[0]!.x;
  c.latitude = cells[0]!.y;
  battle.usersState.push(c);
  battle.usersState.sort((a: any, b: any) => b.initiative - a.initiative);
};

type Row = {
  seed: number; outcome: FloorResult["outcome"]; wave1Rounds: number | null; wave2Rounds: number | null; wave2Reached: boolean;
  captainKilled: boolean; reachedPhase2: boolean; captainMinHpPct: number; ucCasts: number; maxHit: { dmg: number; by: string; action: string; round: number };
  death: { by: string; action: string; dmg: number; round: number; wave: number } | null; playerHpAtWave2Pct: number | null;
  captainTurns: number; captainIdleTurns: number; captainIdleTurnsPlayerFar: number; captainMoveSteps: number;
  ruleFires: Record<number, number>; backupFires: Record<string, number>; actions: Record<string, number>;
  markVsBlast: { ring: number; bell: number; rowsA: number; broadside: number }; stunOnCaptain: number; jabCastsW2: number;
  sealwrightDiedRoundInWave: number | null; captainMoveTurns: number;
  captainDecisions: number; captainDecisionsPlayerFar5: number; captainDecisionsPetAdjacentPlayerFar: number;
  kite?: FloorResult["kite"];
};

const out: Row[] = [];
for (let s = seed0; s < seed0 + runs; s++) {
  const rand = mulberry32(s);
  seedEntropy(s);
  Math.random = rand;
  const player = playerQueryUser(0, v, donor, t.jutsu);
  const pets = petCount > 0 ? [petFor(player)] : undefined;
  if (pets) player.activePetId = pets[0]!.id;
  const b0: any = await assembleFloor({ players: [player], enemyRows: rows, floor, rand, initialBarriers: true, dmgConfig: dmg.config, pets });
  for (let i = 1; i < petCount; i++) addClonePet(b0, player.userId);
  const php0 = b0.usersState.find((u: any) => u.userId === player.userId).curHealth as number;
  const pmax0 = b0.usersState.find((u: any) => u.userId === player.userId).maxHealth as number;
  let capUid: string | null = null;
  let decisions = 0, far5 = 0, petAdjFar = 0;
  const decisionFar = new Map<number, boolean>(); // round -> nearest player >= 2 at his first decision that round
  const r = runFloor(b0, {
    playerIds: [player.userId], maxRounds, dodge,
    ...(mode !== "close" ? { kite: { mode: mode === "kite" ? "strict" : "poke", range: kiteRange, waves: kiteWaves } } : {}),
    onAiDecision: (b, uid, grid) => {
      const u: any = b.usersState.find((x) => x.userId === uid);
      if (!u || u.controllerId !== CAPTAIN) return;
      capUid = uid;
      const hexes = grid.toArray();
      const at = (x: any) => hexes.find((h: any) => h.col === x.longitude && h.row === x.latitude);
      const here = at(u);
      const foes = b.usersState.filter((x: any) => x.direction !== u.direction && stillInBattle(x, b.usersEffects));
      const d = (x: any) => grid.distance(here, at(x));
      const dp = Math.min(99, ...foes.filter((x: any) => !x.isAi && !x.isSummon).map(d));
      const dAny = Math.min(99, ...foes.map(d));
      decisions++;
      if (dp >= 5) far5++;
      if (dAny <= 1 && dp >= 2) petAdjFar++;
      if (!decisionFar.has(b.round)) decisionFar.set(b.round, dp >= 2);
    },
  });
  const pid = player.userId;
  const w1 = r.waves[0], w2 = r.waves.find((w) => w.enemies.some((e) => e.aiId === CAPTAIN));
  const capE = w2?.enemies.find((e) => e.aiId === CAPTAIN);
  const capId = capE?.uid ?? capUid;
  // HP tracks from step deltas.
  let php = php0;
  let chp = capE?.maxHealth ?? 0;
  const cmax = capE?.maxHealth ?? 1;
  let cmin = chp;
  let p2 = false;
  let death: Row["death"] = null;
  let lastHit: Row["death"] = null;
  let maxHit: Row["maxHit"] = { dmg: 0, by: "", action: "", round: 0 };
  let hpAtW2: number | null = null;
  const ruleFires: Record<number, number> = {}, backupFires: Record<string, number> = {}, actions: Record<string, number> = {};
  const capTurnActs = new Map<number, string[]>();
  let ucCasts = 0, moveSteps = 0, stunOnCaptain = 0, jab = 0;
  const mv = { ring: 0, bell: 0, rowsA: 0, broadside: 0 };
  const unitName = (uid: string) => (b0.usersState.find((u: any) => u.userId === uid)?.username) ?? (w2?.enemies.find((e) => e.uid === uid)?.name) ?? (r.waves.flatMap((w) => w.enemies).find((e) => e.uid === uid)?.name) ?? uid;
  for (const st of r.steps) {
    if (hpAtW2 === null && w2 && st.wave === w2.wave) hpAtW2 = Math.round((100 * php) / pmax0);
    if (st.actorUid === capId) {
      if (chp < cmax / 2) p2 = true;
      const a = nameOf(st.actionId);
      actions[a] = (actions[a] ?? 0) + 1;
      if (st.actionId === UC) ucCasts++;
      if (st.actionId === "move") moveSteps++;
      if (st.ruleIndex !== null && st.ruleIndex < st.authoredRules) ruleFires[st.ruleIndex] = (ruleFires[st.ruleIndex] ?? 0) + 1;
      else backupFires[`${a} (engine-appended rule)`] = (backupFires[`${a} (engine-appended rule)`] ?? 0) + 1;
      if (st.actionId === "lib-omen-binding-ring") mv.ring++;
      if (st.actionId === "lib-ships-bell") mv.bell++;
      if (st.actionId === "lib-omen-rows-a") mv.rowsA++;
      if (st.actionId === "lib-broadside") mv.broadside++;
      const l = capTurnActs.get(st.round) ?? [];
      l.push(st.actionId ?? "null");
      capTurnActs.set(st.round, l);
    }
    if (st.human && st.wave === w2?.wave && st.actionId === "VT7oxj_fObWuQa3Rq_BbI") jab++;
    for (const e of st.effects) if (e.type === "stun" && e.target === capId) stunOnCaptain++;
    const dP = st.hp[pid] ?? 0;
    if (!st.human && dP < 0 && -dP > maxHit.dmg) maxHit = { dmg: -dP, by: unitName(st.actorUid), action: nameOf(st.actionId), round: st.round };
    const before = php;
    php += dP;
    if (capId) chp += st.hp[capId] ?? 0;
    cmin = Math.min(cmin, chp);
    void before;
    // The killing blow: the last step that took the player's HP (the battle ends on the step the solo player falls).
    if (dP < 0) lastHit = st.actorUid === pid
      ? { by: "own turn", action: `DoT tick or reflected damage (${nameOf(st.actionId)})`, dmg: -dP, round: st.round, wave: st.wave }
      : { by: unitName(st.actorUid), action: nameOf(st.actionId), dmg: -dP, round: st.round, wave: st.wave };
  }
  if (r.outcome === "wipe") death = lastHit;
  let idle = 0, idleFar = 0;
  for (const [round, acts] of capTurnActs) {
    if (acts.every((a) => a === "wait" || a === "null")) {
      idle++;
      if (decisionFar.get(round)) idleFar++;
    }
  }
  const row: Row = {
    seed: s, outcome: r.outcome,
    wave1Rounds: w1 ? (w1.endRound ?? r.rounds) - w1.startRound + 1 : null,
    wave2Rounds: w2 ? (w2.endRound ?? r.rounds) - w2.startRound + 1 : null, wave2Reached: !!w2,
    captainKilled: capE?.diedRound !== null && capE?.diedRound !== undefined, reachedPhase2: p2, captainMinHpPct: Math.round((100 * cmin) / cmax),
    ucCasts, maxHit, death, playerHpAtWave2Pct: hpAtW2,
    captainTurns: capTurnActs.size, captainIdleTurns: idle, captainIdleTurnsPlayerFar: idleFar, captainMoveSteps: moveSteps,
    ruleFires, backupFires, actions, markVsBlast: mv, stunOnCaptain, jabCastsW2: jab,
    sealwrightDiedRoundInWave: ((e) => (e && e.diedRound !== null && w2 ? e.diedRound - w2.startRound + 1 : null))(w2?.enemies.find((e) => e.aiId === "dg-sealwright")),
    captainMoveTurns: [...capTurnActs.values()].filter((a) => a.includes("move")).length,
    captainDecisions: decisions, captainDecisionsPlayerFar5: far5, captainDecisionsPetAdjacentPlayerFar: petAdjFar,
    ...(r.kite ? { kite: r.kite } : {}),
  };
  out.push(row);
  if (s === seed0) console.log(`player: HP ${php0}/${pmax0}; pets ${b0.usersState.filter((u: any) => u.petId).map((u: any) => `${u.username} HP ${u.maxHealth}`).join(", ")}`);
  console.log(`seed ${s}: ${r.outcome} w2 ${row.wave2Rounds} UC ${ucCasts} p2 ${p2} capMin ${row.captainMinHpPct}% maxHit ${maxHit.dmg} (${maxHit.action}) death ${death ? `${death.by}/${death.action} ${death.dmg} r${death.round}` : "-"} idle ${idle}/${capTurnActs.size} sealDied ${row.sealwrightDiedRoundInWave}${r.kite ? ` kite ${JSON.stringify(r.kite)}` : ""}`);
}

/* ---- aggregate ---- */
const med = (xs: number[]) => {
  const q = [...xs].sort((a, b) => a - b);
  return q.length ? q[Math.floor(q.length / 2)]! : null;
};
const p90 = (xs: number[]) => {
  const q = [...xs].sort((a, b) => a - b);
  return q.length ? q[Math.min(q.length - 1, Math.ceil(0.9 * q.length) - 1)]! : null;
};
const sum = (xs: number[]) => xs.reduce((a, b) => a + b, 0);
const reached = out.filter((x) => x.wave2Reached);
const w2r = reached.map((x) => x.wave2Rounds!);
const ruleTable = capRules.map((rule: any, k: number) => ({
  index: k, note: rule.action.description, fires: sum(out.map((x) => x.ruleFires[k] ?? 0)),
  firedInFightsPct: Math.round((100 * reached.filter((x) => (x.ruleFires[k] ?? 0) > 0).length) / Math.max(1, reached.length)),
}));
const backup: Record<string, number> = {};
for (const x of out) for (const [k, n] of Object.entries(x.backupFires)) backup[k] = (backup[k] ?? 0) + n;
const deaths: Record<string, number> = {};
for (const x of out) if (x.death) deaths[`${x.death.by} / ${x.death.action}`] = (deaths[`${x.death.by} / ${x.death.action}`] ?? 0) + 1;
const outcomes: Record<string, number> = {};
for (const x of out) outcomes[x.outcome] = (outcomes[x.outcome] ?? 0) + 1;
const agg = {
  runs, outcomes, winPct: Math.round((100 * (outcomes.won ?? 0)) / runs), wave2ReachedPct: Math.round((100 * reached.length) / runs),
  wave2RoundsMedian: med(w2r), wave2RoundsP90: p90(w2r), wave1RoundsMedian: med(out.flatMap((x) => (x.wave1Rounds === null ? [] : [x.wave1Rounds]))),
  playerHpAtWave2Median: med(reached.flatMap((x) => (x.playerHpAtWave2Pct === null ? [] : [x.playerHpAtWave2Pct]))),
  ucCastsMedian: med(reached.map((x) => x.ucCasts)), ucCastsMax: Math.max(0, ...reached.map((x) => x.ucCasts)), ucCastsMean: Math.round((10 * sum(reached.map((x) => x.ucCasts))) / Math.max(1, reached.length)) / 10,
  maxHitMedian: med(out.map((x) => x.maxHit.dmg)), maxHitMax: out.reduce((a, x) => (x.maxHit.dmg > a.dmg ? x.maxHit : a), { dmg: 0, by: "", action: "", round: 0 }),
  reachedPhase2Pct: Math.round((100 * reached.filter((x) => x.reachedPhase2).length) / Math.max(1, reached.length)),
  captainKilledPct: Math.round((100 * reached.filter((x) => x.captainKilled).length) / Math.max(1, reached.length)),
  captainMinHpMedian: med(reached.map((x) => x.captainMinHpPct)),
  captainTurns: sum(out.map((x) => x.captainTurns)), captainIdleTurns: sum(out.map((x) => x.captainIdleTurns)),
  captainIdleTurnsPlayerFar: sum(out.map((x) => x.captainIdleTurnsPlayerFar)), captainMoveSteps: sum(out.map((x) => x.captainMoveSteps)),
  sealwrightKilledPct: Math.round((100 * reached.filter((x) => x.sealwrightDiedRoundInWave !== null).length) / Math.max(1, reached.length)),
  sealwrightDiedRoundMedian: med(reached.flatMap((x) => (x.sealwrightDiedRoundInWave === null ? [] : [x.sealwrightDiedRoundInWave]))),
  captainMoveTurns: sum(out.map((x) => x.captainMoveTurns)),
  captainDecisions: sum(out.map((x) => x.captainDecisions)), captainDecisionsPlayerFar5: sum(out.map((x) => x.captainDecisionsPlayerFar5)),
  captainDecisionsPetAdjacentPlayerFar: sum(out.map((x) => x.captainDecisionsPetAdjacentPlayerFar)),
  deaths, markVsBlast: { ring: sum(out.map((x) => x.markVsBlast.ring)), bell: sum(out.map((x) => x.markVsBlast.bell)), rowsA: sum(out.map((x) => x.markVsBlast.rowsA)), broadside: sum(out.map((x) => x.markVsBlast.broadside)) },
  stunOnCaptain: sum(out.map((x) => x.stunOnCaptain)), jabCastsW2: sum(out.map((x) => x.jabCastsW2)),
  kite: mode === "close" ? null : Object.fromEntries(["retreatSteps", "approachSteps", "cornered", "pokes", "humanStepsInside", "humanSteps"].map((k) => [k, sum(out.map((x) => (x.kite as any)?.[k] ?? 0))])),
};
const res = {
  generatedBy: "engine/kite.ts", enginePin: process.env.TNR_ENGINE_PIN ?? "(run.sh default)",
  cell: { rules: rulesSet, mode, ucCooldown, stunprevent, captainPools, pets: petCount, kiteRange, kiteWaves, variant, dodge, seed0, runs, maxRounds },
  inMemoryChanges: changes, captainRules: capRules.map((r: any, i: number) => `${i} ${r.action.type} ${r.action.description} | ${JSON.stringify(r.conditions.map((c: any) => [c.type, c.value ?? c.threshold ?? `${c.minRange}-${c.maxRange}`]))}`),
  aggregate: agg, ruleTable, backupFires: backup, fallbackGuard: unmarkedReport(), perRun: out,
};
console.log(JSON.stringify({ cell: res.cell, aggregate: { ...agg } }, null, 1));
for (const x of ruleTable) console.log(`${String(x.index).padStart(2)} ${x.note.slice(0, 60).padEnd(60)} fires ${x.fires} (in ${x.firedInFightsPct}% of fights)`);
console.log("backup", JSON.stringify(backup));
const p = opt("out");
if (p) {
  mkdirSync(dirname(resolve(p)), { recursive: true });
  writeFileSync(resolve(p), `${JSON.stringify(res, null, 1)}\n`);
}
