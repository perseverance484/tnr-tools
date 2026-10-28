/**
 * Skyglass charts, solo + companion pet, end to end (offline, engine-driven). See engine/charts.ts.
 *
 *   TNR_SCRIPT=charts_main.ts run.sh [--params overrides/charts.params.json] [--runs lowtide,nightwatch,...|all]
 *       [--variants L100,L100noarmor,L50,L50kit] [--seeds 40] [--seed 1] [--no-dodge] [--no-twist] [--max-rounds 60]
 *       [--out results/charts_x.json] [--trace run@fight@seed@variant] [--sweep cases.json]
 *
 * Each fight is a plain QUEST battle built as initiateBattle builds a start_battle objective:
 * - opponent_scaled_to_user: targets take the player's level and scaleUserStats(.., "ai") (charts.ts scaledRow);
 * - allyAIs: NPC allies after the player, on the left (sim.ts assembleFloor allyIds);
 * - applyDebuffs: addQuestStartingEffects on the player; givePools: player pools := % of effective max, after both.
 * Pools carry between fights as in the hunts (database.ts writes cur pools back; status BATTLE adds no regeneration).
 * Any lost/drawn/stalled base fight fails the run. The press-on room is fought only after a base clear; losing it keeps
 * the base ending (RUL-2026-10-28-022).
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { addQuestStartingEffects } from "@/libs/combat/questEffects";
import { getEffectiveMaxPool } from "@/libs/combat/util";
import { buildTemplates, enemyQueryUser, KITSUNE_SET, loadDmgConfig, loadJson, PLAYER_VARIANTS, petFor, playerQueryUser } from "./model";
import { assembleFloor, mulberry32, runFloor, seedEntropy } from "./sim";
import { crownTemplates, DEFAULT_HUNT_PARAMS, DEFAULT_PARAMS, LIVE, NAME } from "./hunts";
import { buildCharts, buildRuns, C, COMMON_CREW, COPY, type ChartParams, DEFAULT_CHART_EXTRA, type Run, scaledRow } from "./charts";
import { LIB } from "./library";

const args = process.argv.slice(2);
const opt = (k: string, d?: string) => {
  const i = args.indexOf(`--${k}`);
  return i >= 0 ? args[i + 1] : d;
};
const flag = (k: string) => args.includes(`--${k}`);
const HARNESS = process.env.TNR_HARNESS!;
const baseline = loadJson(join(HARNESS, "data/baseline.json"));
const dmg = loadDmgConfig(HARNESS, "live");
const kitParams = { ...DEFAULT_PARAMS, ...loadJson(join(HARNESS, "overrides/kits_endgame.params.json")) } as any;
const coreRuptureV2 = loadJson(join(HARNESS, "overrides/director_6wave_tuned.json")).jutsu["nCQETf-HNnbRec1OSY2-R"];
const huntParams = loadJson(join(HARNESS, "overrides/hunts.params.json"));

const deepMerge = (a: any, b: any): any => {
  if (!b || typeof b !== "object" || Array.isArray(b)) return b ?? a;
  const o: any = { ...a };
  for (const [k, v] of Object.entries(b)) o[k] = v && typeof v === "object" && !Array.isArray(v) ? deepMerge(a?.[k] ?? {}, v) : v;
  return o;
};
const BASE: ChartParams = deepMerge(deepMerge(DEFAULT_HUNT_PARAMS, huntParams), DEFAULT_CHART_EXTRA);
let P: ChartParams = opt("params") ? deepMerge(BASE, loadJson(resolve(opt("params")!))) : BASE;

/* Player variants: the hunts' endgame build with and without the Kitsune set, and the level-50 build with and without it. */
const VARIANTS: Record<string, any> = {
  L100: PLAYER_VARIANTS.average,
  L100noarmor: PLAYER_VARIANTS.noarmor,
  L50: PLAYER_VARIANTS.lvl50,
  L50kit: { ...PLAYER_VARIANTS.lvl50, name: "lvl50kit", note: "lvl50 + the full Kitsune set (requiredLevel 1)", gearItemIds: KITSUNE_SET },
};

let T: ReturnType<typeof buildTemplates>;
let enemyRows: Record<string, any>;
let donor: any;
let built: ReturnType<typeof buildCharts>;
let RUNS: Record<string, Run>;
const MARKS = new Set<string>(Object.values(LIB.mark));
const BLASTS = new Set<string>([...Object.values(LIB.blast), ...Object.values(LIB.sig)]);
const setup = (params: ChartParams, twist: boolean) => {
  P = params;
  built = buildCharts(P, kitParams);
  built.override.jutsu["nCQETf-HNnbRec1OSY2-R"] = coreRuptureV2;
  T = buildTemplates(baseline, built.override as never);
  Object.assign(T.enemies, crownTemplates(T.enemies[LIVE.warden]!.row, T.jutsu, P));
  enemyRows = Object.fromEntries(Object.entries(T.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
  // RUL-2026-10-28-021 item 3: Crown Stonebound's live Erupting Ground hits enemies only (a push/319 live edit).
  for (const row of Object.values(enemyRows))
    for (const uj of row.jutsus ?? [])
      if (uj.jutsu?.name === "Erupting Ground") uj.jutsu.effects = uj.jutsu.effects.map((e: any) => (["damage", "pierce"].includes(e.type) ? { ...e, friendlyFire: "ENEMIES" } : e));
  donor = T.enemies[LIVE.warden]!.row;
  RUNS = buildRuns(P, twist);
};
const twistOn = !flag("no-twist");
setup(P, twistOn);

const dodge = !flag("no-dodge");
const maxRounds = Number(opt("max-rounds", "60"));
const seeds = Number(opt("seeds", "40"));
const seed0 = Number(opt("seed", "1"));
const variantArg = opt("variants", "L100")!.split(",");
const runArg = opt("runs", "all")!;
const IDLE = new Set(["move", "wait", null as unknown as string]);
const jname = (id: string | null) => (id === null ? "(none)" : (T.jutsu[id]?.name ?? id));

type FightRec = {
  label: string; pressOn: boolean; outcome: string; rounds: number; hpStart: number; hpEnd: number; cpEnd: number;
  playerTurns: number; playerIdle: number; dodge: Record<string, number>;
  enemies: Record<string, { marks: number; blasts: number; blastHits: number; dealt: number; diedRound: number | null; gaveUp: boolean }>;
  emberHits: number; emberDmg: number;
};

const playerFor = (vk: string) => {
  const v = VARIANTS[vk]!;
  const player = playerQueryUser(0, v, donor, T.jutsu);
  const pets = [petFor(player)];
  player.activePetId = pets[0]!.id;
  return { player, pets, baseHp: player.maxHealth as number };
};

/** --repro: every step's actor, action, positions and HP deltas, to compare two same-seed runs. */
let reproSig: string[] | null = null;
const runOne = async (runKey: string, vk: string, seed: number, trace?: number) => {
  const run = RUNS[runKey]!;
  const rand = mulberry32(seed);
  seedEntropy(seed);
  const orig = Math.random;
  Math.random = rand;
  try {
    const { player, pets, baseHp } = playerFor(vk);
    const fights: FightRec[] = [];
    let base = true;
    let pressOn: boolean | null = null;
    for (let fi = 0; fi < run.fights.length; fi++) {
      const f = run.fights[fi]!;
      if (f.pressOn && !base) break;
      const hpStart = player.curHealth;
      const rows = f.scaled ? { ...enemyRows, ...Object.fromEntries(f.ids.map((id) => [id, scaledRow(enemyRows[id], player.level)])) } : enemyRows;
      const battle = await assembleFloor({ players: [player], enemyRows: rows, floor: { kind: "floor", waves: [{ aiIds: f.ids, delayRounds: 0 }] }, rand, initialBarriers: true, dmgConfig: dmg.config, mode: "quest", pets, allyIds: f.allies });
      const pu = battle.usersState.find((u) => u.userId === player.userId)!;
      if (f.debuffs?.length) addQuestStartingEffects(pu, battle.usersEffects, f.debuffs as never, `quest-${runKey}`);
      if (f.givePools !== undefined) {
        pu.curHealth = (getEffectiveMaxPool(pu, battle.usersEffects, "Health") * f.givePools) / 100;
        pu.curChakra = (getEffectiveMaxPool(pu, battle.usersEffects, "Chakra") * f.givePools) / 100;
        pu.curStamina = (getEffectiveMaxPool(pu, battle.usersEffects, "Stamina") * f.givePools) / 100;
      }
      const hpAtStart = pu.curHealth;
      const res = runFloor(battle, { playerIds: [player.userId], maxRounds, dodge, detail: trace === fi || !!reproSig });
      if (reproSig) {
        reproSig.push(`fight ${fi} start ${battle.usersState.map((u) => `${u.username}@${u.longitude},${u.latitude}`).join(" ")}`);
        for (const s of res.steps) reproSig.push(`${fi} r${s.round} ${s.actor} ${s.actionId} ${s.actorFrom} ${s.actorTo} ${JSON.stringify(s.hp)}`);
      }
      if (trace === fi) printTrace(res, player.userId);
      const fin = res.final[player.userId]!;
      const enemies: FightRec["enemies"] = {};
      const enemyUid = new Map<string, string>();
      for (const w of res.waves) for (const e of w.enemies) enemyUid.set(e.uid, e.aiId);
      const ensure = (aid: string) => (enemies[NAME[aid] ? `${NAME[aid]}${aid.startsWith("chart-lingering") ? "" : ""}` : "(summon/clone)"] ??= { marks: 0, blasts: 0, blastHits: 0, dealt: 0, diedRound: null, gaveUp: false });
      for (const aid of f.ids) ensure(aid);
      for (const w of res.waves) for (const e of w.enemies) if (e.diedRound !== null) ensure(e.aiId).diedRound = e.diedRound;
      let playerTurns = 0;
      let playerIdle = 0;
      const pTurn = new Map<number, boolean>();
      let emberHits = 0;
      let emberDmg = 0;
      for (const s of res.steps) {
        if (s.human) {
          if (!pTurn.has(s.round)) pTurn.set(s.round, true);
          if (!s.dodge && !IDLE.has(s.actionId as string)) pTurn.set(s.round, false);
        }
        if (s.actor === player.userId && !s.human) continue; // pet
        if (!s.human && s.actor !== player.userId && !(f.allies ?? []).includes(s.actor)) {
          const e = ensure(s.actor);
          e.dealt += s.dealt;
          if (s.actionId && MARKS.has(s.actionId)) e.marks++;
          if (s.actionId && BLASTS.has(s.actionId)) {
            e.blasts++;
            if ((s.hp[player.userId] ?? 0) < 0) e.blastHits++;
          }
          if (s.actionId === null && s.hp[s.actorUid] && s.hp[s.actorUid]! < 0 && !(s.dealtBy && Object.keys(s.dealtBy).length)) e.gaveUp = true;
        }
        // Ember damage: HP loss on a player's own step while the Burning Deck is in the fight (drain fires on the occupant's action).
        if (s.human && (s.hp[player.userId] ?? 0) < 0 && f.ids.includes(C.deck)) {
          emberHits++;
          emberDmg -= s.hp[player.userId]!;
        }
      }
      for (const v of pTurn.values()) {
        playerTurns++;
        if (v) playerIdle++;
      }
      fights.push({ label: f.label, pressOn: !!f.pressOn, outcome: res.outcome, rounds: res.rounds, hpStart: (100 * hpAtStart) / baseHp, hpEnd: (100 * Math.max(0, fin.hp)) / baseHp, cpEnd: (100 * fin.cp) / fin.maxCp, playerTurns, playerIdle, dodge: res.dodge as any, enemies, emberHits, emberDmg: (100 * emberDmg) / baseHp });
      void hpStart;
      const won = res.outcome === "won";
      if (f.pressOn) {
        pressOn = won;
        break;
      }
      if (!won) {
        base = false;
        break;
      }
      player.curHealth = Math.round(fin.hp);
      player.curChakra = Math.round(fin.cp);
      player.curStamina = Math.round(fin.sp);
      player.status = "BATTLE";
    }
    return { seed, base, pressOn, fights };
  } finally {
    Math.random = orig;
  }
};

const printTrace = (res: any, pid: string) => {
  console.log(`--- trace: ${res.outcome} in ${res.rounds} rounds`);
  for (const s of res.steps) {
    const who = s.human ? "PLAYER" : s.actor === pid ? "PET" : (NAME[s.actor] ?? s.actor);
    const hp = Object.entries(s.hp).map(([u, d]: any) => `${u === pid ? "P" : u.slice(0, 6)}${d > 0 ? "+" : ""}${Math.round(d)}`).join(" ");
    const g = (s.groundAfter ?? []).filter((x: any) => x.staticAnimation && (x.rounds ?? 0) > 0);
    const gs = Object.entries(g.reduce((m: any, x: any) => ((m[x.staticAnimation] = (m[x.staticAnimation] ?? 0) + 1), m), {})).map(([k, v]) => `${k}x${v}`).join(" ");
    console.log(`r${s.round} ${who.padEnd(17)} ${jname(s.actionId).padEnd(28)} rule ${String(s.ruleIndex ?? (s.dodge ? "dodge" : "-")).padEnd(5)} ${s.actorFrom?.join(",")}->${s.actorTo?.join(",")} | ${hp} | fx ${s.effects.map((e: any) => `${e.type}>${e.target === pid ? "P" : e.target.slice(0, 6)}`).join(",")} | ground ${gs}${(s.newUnits ?? []).length ? ` | new ${s.newUnits.map((u: any) => u.name).join(",")}` : ""}`);
  }
};

/* ---------------- aggregation ---------------- */
const median = (xs: number[]) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m]! : (s[m - 1]! + s[m]!) / 2;
};
const pctl = (xs: number[], p: number) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  return s[Math.min(s.length - 1, Math.floor(p * (s.length - 1) + 0.5))]!;
};
const r1 = (x: number | null) => (x === null ? null : Math.round(x * 10) / 10);
const SEC_PER_TURN = 15;

const summarise = (key: string, vk: string, runs: Awaited<ReturnType<typeof runOne>>[]) => {
  const run = RUNS[key]!;
  const baseWins = runs.filter((r) => r.base);
  const pressReached = runs.filter((r) => r.pressOn !== null);
  const pressWins = runs.filter((r) => r.pressOn === true);
  const nBase = run.fights.filter((f) => !f.pressOn).length;
  const baseRounds = baseWins.map((r) => r.fights.slice(0, nBase).reduce((s, f) => s + f.rounds, 0));
  const fights = run.fights.map((f, i) => {
    const recs = runs.map((r) => r.fights[i]).filter(Boolean) as FightRec[];
    const won = recs.filter((x) => x.outcome === "won");
    const enemyNames = [...new Set(recs.flatMap((x) => Object.keys(x.enemies)))];
    const dsum: Record<string, number> = {};
    for (const x of recs) for (const [k, v] of Object.entries(x.dodge ?? {})) dsum[k] = (dsum[k] ?? 0) + (v as number);
    return {
      fight: i + 1, label: f.label, pressOn: !!f.pressOn, reached: recs.length, won: won.length,
      roundsMedian: median(won.map((x) => x.rounds)), roundsP90: pctl(won.map((x) => x.rounds), 0.9),
      hpStartMedian: r1(median(recs.map((x) => x.hpStart))), hpEndMedian: r1(median(won.map((x) => x.hpEnd))), hpEndP10: r1(pctl(won.map((x) => x.hpEnd), 0.1)),
      hpCostMedian: r1(median(won.map((x) => x.hpStart - x.hpEnd))),
      playerIdlePct: r1((100 * recs.reduce((s, x) => s + x.playerIdle, 0)) / Math.max(1, recs.reduce((s, x) => s + x.playerTurns, 0))),
      emberHitsMedian: median(recs.map((x) => x.emberHits)), emberDmgMedian: r1(median(recs.map((x) => x.emberDmg))),
      outcomes: recs.reduce((m: any, x) => ((m[x.outcome] = (m[x.outcome] ?? 0) + 1), m), {}),
      dodge: dsum,
      enemies: Object.fromEntries(enemyNames.map((n) => {
        const es = recs.map((x) => x.enemies[n]).filter(Boolean);
        const sum = (k: "marks" | "blasts" | "blastHits" | "dealt") => es.reduce((s, e) => s + e[k], 0);
        return [n, { marksPerFight: r1(sum("marks") / Math.max(1, es.length)), blastsPerFight: r1(sum("blasts") / Math.max(1, es.length)), blastHitPct: sum("blasts") ? r1((100 * sum("blastHits")) / sum("blasts")) : null, dealtPerFight: Math.round(sum("dealt") / Math.max(1, es.length)), diedMedianRound: median(es.filter((e) => e.diedRound !== null).map((e) => e.diedRound!)) }];
      })),
    };
  });
  return {
    run: key, chart: run.chart, variant: vk, dodge, twist: twistOn, runs: runs.length,
    baseClear: baseWins.length, baseClearPct: r1((100 * baseWins.length) / runs.length),
    pressOnWon: pressWins.length, pressOnReached: pressReached.length, pressOnPctOfReached: pressReached.length ? r1((100 * pressWins.length) / pressReached.length) : null,
    pressOnPctOfAll: r1((100 * pressWins.length) / runs.length),
    baseRoundsMedian: median(baseRounds), baseMinutesMedian: r1(((median(baseRounds) ?? 0) * SEC_PER_TURN) / 60),
    lossesAt: Object.fromEntries(run.fights.map((_, i) => [i + 1, runs.filter((r) => r.fights.length === i + 1 && r.fights[i]!.outcome !== "won").length])),
    fights,
    perSeed: runs.map((r) => ({ seed: r.seed, base: r.base, pressOn: r.pressOn, hp: r.fights.map((f) => Math.round(f.hpEnd)), rounds: r.fights.map((f) => f.rounds) })),
  };
};

const runKeys = (key: string, vk: string) => {
  if (key !== "all") return key.split(",");
  const L50 = vk.startsWith("L50");
  return L50 ? ["lowtide", "nightwatch"] : Object.keys(RUNS);
};

/**
 * Ember probe (The Fall twist): does `drain` ember ground do nothing on the cast and hit the occupant on its next action?
 * The Burning Deck lays band I (rows 0-1) at round 1 and band II (rows 2-3) at round 3. Four players' rules:
 *   A stands on row 1 and waits; B stands on row 1 and walks off to row 8 on its turn; C stands on row 8 (clear) and
 *   waits; D starts on row 8 and walks onto row 2 at round 2 (before band II lands at round 3), then waits.
 * One player per scenario (separate battles), pet off, no other enemies. Per step: HP change of the player.
 */
if (flag("probe-embers")) {
  const { rule } = await import("./kitlib");
  const scen: [string, [number, number], any[]][] = [
    ["A: on row 1, waits", [3, 1], [rule("wait", [], { type: "end_turn" })]],
    ["B: on row 1, walks off to row 8", [3, 1], [rule("walk off", [], { type: "move_towards_opponent", target: "COORDINATE", coordinates: { longitude: 3, latitude: 8 } }), rule("wait", [], { type: "end_turn" })]],
    ["C: on row 8 (clear), waits", [3, 8], [rule("wait", [], { type: "end_turn" })]],
    ["D: row 8, walks onto row 2 in round 2", [3, 8], [rule("walk in", [{ type: "round_greater_than", value: 1, description: "" }], { type: "move_towards_opponent", target: "COORDINATE", coordinates: { longitude: 3, latitude: 2 } }), rule("wait", [], { type: "end_turn" })]],
  ];
  const probes: any[] = [];
  for (const [label, pos, rules] of scen) {
    const rand = mulberry32(1);
    seedEntropy(1);
    Math.random = rand;
    const player = playerQueryUser(0, { ...VARIANTS.L100, rules }, donor, T.jutsu);
    const battle = await assembleFloor({ players: [player], enemyRows, floor: { kind: "floor", waves: [{ aiIds: [C.deck], delayRounds: 0 }] }, rand, initialBarriers: false, dmgConfig: dmg.config, mode: "quest" });
    const pu = battle.usersState.find((u) => u.userId === player.userId)!;
    const du = battle.usersState.find((u) => u.controllerId === C.deck)!;
    [pu.longitude, pu.latitude] = pos;
    [du.longitude, du.latitude] = [10, 9];
    battle.usersState.sort((a, c) => (a.userId === du.userId ? -1 : c.userId === du.userId ? 1 : 0));
    battle.activeUserId = du.userId;
    const res = runFloor(battle, { playerIds: [player.userId], maxRounds: 5, detail: true, dodge: false });
    const steps = res.steps.map((s) => ({
      round: s.round, actor: s.human ? "player" : "Burning Deck", action: jname(s.actionId), at: s.actorFrom, to: s.actorTo,
      playerHp: Math.round(s.hp[player.userId] ?? 0),
      embersAfter: (s.groundAfter ?? []).filter((g: any) => g.type === "drain").length,
      playerOnEmberAtStart: (s.groundAfter ?? []).some((g: any) => g.type === "drain" && s.actorFrom && g.x === s.actorFrom[0] && g.y === s.actorFrom[1]),
    }));
    probes.push({ label, maxHp: pu.maxHealth, steps });
    console.log(`\n### ${label} (max HP ${pu.maxHealth}; drain ${P.ember.power}% = ${Math.floor((P.ember.power / 100) * pu.maxHealth)} per tick)`);
    for (const s of steps) console.log(`  r${s.round} ${s.actor.padEnd(13)} ${s.action.padEnd(22)} ${JSON.stringify(s.at)}->${JSON.stringify(s.to)} playerHP ${s.playerHp} drainTiles ${s.embersAfter}`);
  }
  const o = opt("out");
  if (o) writeFileSync(resolve(o), `${JSON.stringify({ generatedBy: "charts_main.ts --probe-embers", ember: P.ember, probes }, null, 1)}\n`);
  process.exit(0);
}

const reproArg = opt("repro");
if (reproArg) {
  // run@variant@seed, all fights, twice; identical signatures (positions included) or the first difference.
  const [k, vk, sd] = reproArg.split("@");
  const sigs: string[][] = [];
  for (let i = 0; i < 2; i++) {
    reproSig = [];
    await runOne(k!, vk ?? "L100", Number(sd ?? 1));
    sigs.push(reproSig);
  }
  reproSig = null;
  const n = Math.max(sigs[0]!.length, sigs[1]!.length);
  const diff = [...Array(n).keys()].find((i) => sigs[0]![i] !== sigs[1]![i]);
  console.log(diff === undefined ? `REPRO OK ${reproArg}: ${n} steps identical (positions, actions, HP)` : `REPRO DIFF ${reproArg} at ${diff}:\n  ${sigs[0]![diff]}\n  ${sigs[1]![diff]}`);
  process.exit(diff === undefined ? 0 : 1);
}

const traceArg = opt("trace");
if (traceArg) {
  const [k, fi, s, vk] = traceArg.split("@");
  const r = await runOne(k!, vk ?? "L100", Number(s ?? 1), Number(fi ?? 0));
  console.log(`base ${r.base} pressOn ${r.pressOn}`);
  for (const f of r.fights) console.log(JSON.stringify({ label: f.label, outcome: f.outcome, rounds: f.rounds, hp: [r1(f.hpStart), r1(f.hpEnd)], embers: [f.emberHits, r1(f.emberDmg)], dodge: f.dodge }), JSON.stringify(f.enemies));
  process.exit(0);
}

if (flag("scaled-stats")) {
  for (const lvl of [50, 100])
    for (const id of [...COMMON_CREW.map((x) => COPY[x]!), C.steep]) {
      const r = scaledRow(enemyRows[id], lvl);
      console.log(`L${lvl} ${NAME[id]?.padEnd(18)} lvl ${r.level} HP ${r.maxHealth} off ${Math.round(r.offence)} def ${Math.round(r.defence)} str ${Math.round(r.strength)} int ${Math.round(r.intelligence)} wil ${Math.round(r.willpower)} spd ${Math.round(r.speed)} | unscaled HP ${enemyRows[id].maxHealth} off ${Math.round(enemyRows[id].offence)} | rows ${enemyRows[id].effects.length}`);
    }
  for (const vk of Object.keys(VARIANTS)) {
    const { player } = playerFor(vk);
    console.log(`${vk}: lvl ${player.level} HP ${player.maxHealth} off ${Math.round(player.offence)} def ${Math.round(player.defence)} gen ${Math.round(player.strength)} kit ${player.jutsus.length}`);
  }
  process.exit(0);
}

const sweepArg = opt("sweep");
if (sweepArg) {
  const cases: { name: string; params?: any; runs: string[]; variants?: string[]; seeds?: number; twist?: boolean }[] = loadJson(resolve(sweepArg));
  const rows: any[] = [];
  for (const c of cases) {
    setup(deepMerge(BASE, c.params ?? {}), c.twist ?? twistOn);
    for (const vk of c.variants ?? variantArg)
      for (const key of c.runs) {
        const runs = [];
        for (let i = 0; i < (c.seeds ?? seeds); i++) runs.push(await runOne(key, vk, seed0 + i));
        const s = summarise(key, vk, runs);
        console.log(`${c.name.padEnd(22)} ${vk.padEnd(11)} ${key.padEnd(11)} base ${String(s.baseClear).padStart(2)}/${s.runs} press ${s.pressOnWon}/${s.pressOnReached} min ${s.baseMinutesMedian} | ` + s.fights.map((f) => `F${f.fight} ${f.won}/${f.reached} r${f.roundsMedian} ${f.hpStartMedian}->${f.hpEndMedian}`).join(" | "));
        rows.push({ case: c.name, ...s, perSeed: undefined });
      }
  }
  const o = opt("out");
  if (o) writeFileSync(resolve(o), `${JSON.stringify(rows, null, 1)}\n`);
  process.exit(0);
}

const out: any = { generatedBy: "harness/skyglass_wreck_sim/engine/charts_main.ts", settings: { dodge, twist: twistOn, maxRounds, seeds, seed0, dmgConfig: dmg.name, params: P, secondsPerTurn: SEC_PER_TURN, variants: Object.fromEntries(variantArg.map((v) => [v, VARIANTS[v].note])) }, newRecords: built.newRecords, results: [] as any[] };
for (const vk of variantArg)
  for (const key of runKeys(runArg, vk)) {
    const runs = [];
    for (let i = 0; i < seeds; i++) runs.push(await runOne(key, vk, seed0 + i));
    const s = summarise(key, vk, runs);
    out.results.push(s);
    console.log(`\n=== ${vk} ${key} (${s.chart}) dodge=${dodge} twist=${twistOn}: base ${s.baseClear}/${s.runs} press-on ${s.pressOnWon}/${s.pressOnReached} (${s.pressOnPctOfAll}% of all) base ${s.baseRoundsMedian} rounds = ${s.baseMinutesMedian} min; losses ${JSON.stringify(s.lossesAt)}`);
    for (const f of s.fights) {
      console.log(`  F${f.fight} ${f.label.padEnd(64)} won ${f.won}/${f.reached} rnd ${f.roundsMedian} (p90 ${f.roundsP90}) HP ${f.hpStartMedian}->${f.hpEndMedian} (p10 ${f.hpEndP10}) cost ${f.hpCostMedian} idle ${f.playerIdlePct}%${f.emberHitsMedian ? ` embers ${f.emberHitsMedian} hits/${f.emberDmgMedian}%` : ""} ${JSON.stringify(f.outcomes)}`);
      for (const [n, e] of Object.entries<any>(f.enemies)) if (e.marksPerFight || e.blastsPerFight) console.log(`      ${n.padEnd(18)} marks ${e.marksPerFight} blasts ${e.blastsPerFight} hit% ${e.blastHitPct} dealt ${e.dealtPerFight} died r${e.diedMedianRound}`);
    }
  }
const outPath = opt("out");
if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(resolve(outPath), `${JSON.stringify(out, null, 1)}\n`);
  console.log(`wrote ${outPath}`);
}
