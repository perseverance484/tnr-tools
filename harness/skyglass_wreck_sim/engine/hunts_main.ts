/**
 * Skyglass treasure hunts, solo, end to end (offline, engine-driven).
 *
 *   TNR_SCRIPT=hunts_main.ts run.sh [--params hunts.params.json] [--paths foundry,watch_000,...|all]
 *       [--seeds 40] [--seed 1] [--no-dodge] [--max-rounds 60] [--out results/hunts_x.json]
 *       [--trace path@fight@seed]   (prints one fight action by action)
 *
 * A hunt is an isolated Battle Pyramid: each start_battle objective is a plain QUEST battle (one player vs the fight's
 * AIs, opponent_scaled_to_user false, keepOriginalPools false, no givePools), and the player's HP/CP/SP after a won
 * fight are what the next fight starts with (libs/combat/database.ts writes result.cur* unclamped; nothing regenerates
 * inside an isolated run). A lost, drawn or stalled fight fails the hunt (RUL-2026-10-25-010). Quest debuffs (ALARM,
 * TERM) are added to the player through the engine's own addQuestStartingEffects, as initiateBattle does.
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { addQuestStartingEffects } from "@/libs/combat/questEffects";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, PLAYER_VARIANTS, playerQueryUser } from "./model";
import { assembleFloor, mulberry32, runFloor, seedEntropy } from "./sim";
import { buildHunts, buildPaths, DEFAULT_HUNT_PARAMS, type HuntParams, LIVE, NAME, type Path } from "./hunts";
import { DEFAULT_PARAMS } from "./kits";
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

const mergeParams = (base: HuntParams, p: any): HuntParams => ({ ...base, ...p, stats: { ...base.stats, ...(p.stats ?? {}) }, pow: { ...base.pow, ...(p.pow ?? {}) } });
export const loadParams = (path?: string): HuntParams => (path ? mergeParams(DEFAULT_HUNT_PARAMS, loadJson(resolve(path))) : DEFAULT_HUNT_PARAMS);
const kitParamsFile = loadJson(join(HARNESS, "overrides/kits_endgame.params.json"));
const kitParams = { ...DEFAULT_PARAMS, ...kitParamsFile, pow: { ...DEFAULT_PARAMS.pow, ...(kitParamsFile.pow ?? {}) } };
let HP = loadParams(opt("params"));
const coreRuptureV2 = loadJson(join(HARNESS, "overrides/director_6wave_tuned.json")).jutsu["nCQETf-HNnbRec1OSY2-R"];
let built: ReturnType<typeof buildHunts>;
let T: ReturnType<typeof buildTemplates>;
let enemyRows: Record<string, any>;
let donor: any;
const MARKS = new Set<string>();
const BLASTS = new Set<string>();
let PATHS: Record<string, Path> = buildPaths();
const setup = (params: HuntParams) => {
  HP = params;
  PATHS = buildPaths(HP.compose ?? {});
  built = buildHunts(HP, kitParams);
  // Core Rupture v2: the live record as edited by push/316-317 (as build_kits.ts does).
  built.override.jutsu["nCQETf-HNnbRec1OSY2-R"] = coreRuptureV2;
  T = buildTemplates(baseline, built.override as never);
  enemyRows = Object.fromEntries(Object.entries(T.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
  donor = T.enemies[LIVE.warden]!.row;
  MARKS.clear();
  BLASTS.clear();
  for (const id of Object.values(LIB.mark)) MARKS.add(id);
  for (const id of [...Object.values(LIB.blast), ...Object.values(LIB.sig)]) BLASTS.add(id);
  // The shared Wreck set pieces (Captain, Core Horror) count too.
  for (const id of Object.keys(T.jutsu)) {
    const j = T.jutsu[id];
    if (!id.startsWith("dg-")) continue;
    if (j.description?.startsWith("Telegraph:")) MARKS.add(id);
    else if (j.effects?.some((e: any) => e.type === "damage") && (j.method === "COORDINATES" || j.target === "CHARACTER" || (j.target === "GROUND" && j.method !== "SINGLE"))) BLASTS.add(id);
  }
};
setup(HP);
const variant = PLAYER_VARIANTS[opt("variant", "average")!]!;
const dodge = !flag("no-dodge");
const maxRounds = Number(opt("max-rounds", "60"));
const seeds = Number(opt("seeds", "40"));
const seed0 = Number(opt("seed", "1"));
const pathArg = opt("paths", "all")!;
const paths = pathArg === "all" ? Object.keys(buildPaths()) : pathArg.split(",");

const isWindow = (id: string | null) => id === LIB.loweredGuard || id === LIB.sig.quench;
const IDLE = new Set(["move", "wait", null as unknown as string]);
const jname = (id: string | null) => (id === null ? "(none)" : (T.jutsu[id]?.name ?? id));

type FightRec = {
  label: string; boss: boolean; outcome: string; rounds: number; hpStart: number; hpEnd: number; maxHp: number; cpEnd: number; spEnd: number;
  enemies: Record<string, { marks: number; blasts: number; blastHits: number; windows: number; turnsAfterR2: number; idleAfterR2: number; sig: boolean; dealt: number }>;
  playerTurns: number; playerIdleTurns: number; dodge: Record<string, number>; playerDealt: number;
};

/** A path key "fight:Name+Name" is one ad-hoc fight at full pools (debugging). */
const pathOf = (key: string) => {
  if (!key.startsWith("fight:")) return PATHS[key]!;
  const ids = key.slice(6).split("+").map((n) => Object.keys(NAME).find((id) => NAME[id] === n.replaceAll("_", " "))!);
  return { hunt: "ad hoc", fights: [{ label: key, ids, boss: true }] } as Path;
};
const runPath = async (pathKey: string, seed: number, trace?: number) => {
  const path = pathOf(pathKey);
  const rand = mulberry32(seed);
  seedEntropy(seed);
  const orig = Math.random;
  Math.random = rand;
  try {
    const player = playerQueryUser(0, variant, donor, T.jutsu);
    const fights: FightRec[] = [];
    let status = "won";
    for (let fi = 0; fi < path.fights.length; fi++) {
      const f = path.fights[fi]!;
      const hpStart = player.curHealth;
      const battle = await assembleFloor({ players: [player], enemyRows, floor: { kind: "floor", waves: [{ aiIds: f.ids, delayRounds: 0 }] }, rand, initialBarriers: true, dmgConfig: dmg.config, mode: "quest" });
      const pu = battle.usersState.find((u) => u.userId === player.userId)!;
      if (f.debuffs?.length) addQuestStartingEffects(pu, battle.usersEffects, f.debuffs as never, `quest-${pathKey}`);
      const res = runFloor(battle, { playerIds: [player.userId], maxRounds, dodge, detail: trace === fi });
      if (trace === fi) printTrace(res, battle, player.userId);
      const fin = res.final[player.userId]!;
      const enemies: FightRec["enemies"] = {};
      const turnSeen = new Map<string, boolean>();
      const ensure = (aid: string) => (enemies[NAME[aid] ?? "(clone or summon)"] ??= { marks: 0, blasts: 0, blastHits: 0, windows: 0, turnsAfterR2: 0, idleAfterR2: 0, sig: false, dealt: 0 });
      for (const aid of f.ids) ensure(aid);
      const sigs = (built.override.signatures as any) ?? {};
      let playerTurns = 0;
      let playerIdle = 0;
      const pTurn = new Map<number, boolean>();
      let playerDealt = 0;
      for (const s of res.steps) {
        if (s.human) {
          playerDealt += s.dealt;
          if (!pTurn.has(s.round)) pTurn.set(s.round, true);
          if (!s.dodge && !IDLE.has(s.actionId as string)) pTurn.set(s.round, false);
          continue;
        }
        const e = ensure(s.actor);
        e.dealt += s.dealt;
        if (s.actionId && MARKS.has(s.actionId)) e.marks++;
        if (s.actionId && BLASTS.has(s.actionId)) {
          e.blasts++;
          if ((s.hp[player.userId] ?? 0) < 0 || s.effects.some((x) => x.target === player.userId && x.creator === s.actorUid)) e.blastHits++;
        }
        if (isWindow(s.actionId)) e.windows++;
        if (s.ruleIndex !== null && (sigs[s.actor] ?? []).includes(s.ruleIndex)) e.sig = true;
        if (s.round >= 3) {
          const k = `${s.actorUid}:${s.round}`;
          if (!turnSeen.has(k)) {
            turnSeen.set(k, true);
            e.turnsAfterR2++;
            e.idleAfterR2++;
          }
          if (!IDLE.has(s.actionId as string) && turnSeen.get(k)) {
            turnSeen.set(k, false);
            e.idleAfterR2--;
          }
        }
      }
      for (const v of pTurn.values()) {
        playerTurns++;
        if (v) playerIdle++;
      }
      fights.push({ label: f.label, boss: !!f.boss, outcome: res.outcome, rounds: res.rounds, hpStart, hpEnd: Math.max(0, fin.hp), maxHp: fin.maxHp, cpEnd: fin.cp, spEnd: fin.sp, enemies, playerTurns, playerIdleTurns: playerIdle, dodge: res.dodge as any, playerDealt });
      if (res.outcome !== "won") {
        status = `lost at fight ${fi + 1} (${res.outcome})`;
        break;
      }
      // Pools carry into the next fight (isolated pyramid; no givePools).
      player.curHealth = Math.round(fin.hp);
      player.curChakra = Math.round(fin.cp);
      player.curStamina = Math.round(fin.sp);
      // Between pyramid fights the account stays in status BATTLE (database.ts userPatch for isolated runs), so
      // processUsersForBattle adds no timed regeneration (restored = 0) and only clamps cur to max.
      player.status = "BATTLE";
    }
    return { seed, status, won: status === "won", fights };
  } finally {
    Math.random = orig;
  }
};

const printTrace = (res: any, battle: any, pid: string) => {
  console.log(`--- trace: ${res.outcome} in ${res.rounds} rounds`);
  for (const s of res.steps) {
    const who = s.human ? "PLAYER" : (NAME[s.actor] ?? s.actor);
    const hp = Object.entries(s.hp).map(([u, d]: any) => `${u === pid ? "P" : u.slice(0, 6)}${d > 0 ? "+" : ""}${Math.round(d)}`).join(" ");
    const g = (s.groundAfter ?? []).filter((x: any) => x.staticAnimation && ((x.rounds ?? 0) > 0)).map((x: any) => `${x.staticAnimation}@${x.x},${x.y}`);
    console.log(`r${s.round} ${who.padEnd(17)} ${jname(s.actionId).padEnd(26)} rule ${String(s.ruleIndex ?? (s.dodge ? "dodge" : "-")).padEnd(5)} ${s.actorFrom?.join(",")}->${s.actorTo?.join(",")} | ${hp} | fx ${s.effects.map((e: any) => `${e.type}>${e.target === pid ? "P" : e.target.slice(0, 6)}`).join(",")} | ground ${g.length} ${g.slice(0, 6).join(" ")}${(s.newUnits ?? []).length ? ` | new ${JSON.stringify(s.newUnits)}` : ""}`);
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
const BASE_HP = 5050;

const summarise = (key: string, runs: Awaited<ReturnType<typeof runPath>>[]) => {
  const path = pathOf(key);
  const fights = path.fights.map((f, i) => {
    const recs = runs.map((r) => r.fights[i]).filter(Boolean) as FightRec[];
    const won = recs.filter((x) => x.outcome === "won");
    const enemyNames = [...new Set(recs.flatMap((x) => Object.keys(x.enemies)))];
    const enemies = Object.fromEntries(enemyNames.map((n) => {
      const es = recs.map((x) => x.enemies[n]).filter(Boolean);
      const sum = (k: keyof (typeof es)[number]) => es.reduce((s, e) => s + (e[k] as number), 0);
      return [n, {
        appearances: es.length,
        markFiredPct: r1((100 * es.filter((e) => e.marks > 0).length) / Math.max(1, es.length)),
        marksPerFight: r1(sum("marks") / Math.max(1, es.length)), blastsPerFight: r1(sum("blasts") / Math.max(1, es.length)),
        blastHitPct: sum("blasts") ? r1((100 * sum("blastHits")) / sum("blasts")) : null,
        windowsPerFight: r1(sum("windows") / Math.max(1, es.length)),
        signatureFiredPct: r1((100 * es.filter((e) => e.sig).length) / Math.max(1, es.length)),
        idleTurnsAfterR2Pct: sum("turnsAfterR2") ? r1((100 * sum("idleAfterR2")) / sum("turnsAfterR2")) : null,
        dealtPerFight: Math.round(sum("dealt") / Math.max(1, es.length)),
      }];
    }));
    const dodgeSum: Record<string, number> = {};
    for (const x of recs) for (const [k, v] of Object.entries(x.dodge ?? {})) dodgeSum[k] = (dodgeSum[k] ?? 0) + (v as number);
    return {
      fight: i + 1, label: f.label, boss: !!f.boss, reached: recs.length, won: won.length, lost: recs.length - won.length,
      winPctOfReached: r1((100 * won.length) / Math.max(1, recs.length)),
      roundsMedian: median(won.map((x) => x.rounds)), roundsP10: pctl(won.map((x) => x.rounds), 0.1), roundsP90: pctl(won.map((x) => x.rounds), 0.9),
      hpStartPctMedian: r1(median(recs.map((x) => (100 * x.hpStart) / BASE_HP))),
      hpEndPctMedian: r1(median(won.map((x) => (100 * x.hpEnd) / BASE_HP))), hpEndPctP10: r1(pctl(won.map((x) => (100 * x.hpEnd) / BASE_HP), 0.1)),
      hpLostPctMedian: r1(median(recs.map((x) => (100 * (x.hpStart - x.hpEnd)) / BASE_HP))),
      cpEndPctMedian: r1(median(won.map((x) => (100 * x.cpEnd) / BASE_HP))), spEndPctMedian: r1(median(won.map((x) => (100 * x.spEnd) / BASE_HP))),
      playerIdleTurnsPct: r1((100 * recs.reduce((s, x) => s + x.playerIdleTurns, 0)) / Math.max(1, recs.reduce((s, x) => s + x.playerTurns, 0))),
      dodge: dodgeSum, enemies,
    };
  });
  const wins = runs.filter((r) => r.won);
  return {
    path: key, hunt: path.hunt, runs: runs.length, wins: wins.length, winPct: r1((100 * wins.length) / runs.length),
    endHpPctMedian: r1(median(wins.map((r) => (100 * r.fights[r.fights.length - 1]!.hpEnd) / BASE_HP))),
    endHpPctP10: r1(pctl(wins.map((r) => (100 * r.fights[r.fights.length - 1]!.hpEnd) / BASE_HP), 0.1)),
    totalRoundsMedian: median(wins.map((r) => r.fights.reduce((s, f) => s + f.rounds, 0))),
    lossesAt: Object.fromEntries(path.fights.map((_, i) => [i + 1, runs.filter((r) => !r.won && r.fights.length === i + 1).length])),
    fights,
    perSeed: runs.map((r) => ({ seed: r.seed, status: r.status, hp: r.fights.map((f) => Math.round((100 * f.hpEnd) / BASE_HP)), rounds: r.fights.map((f) => f.rounds) })),
  };
};

const traceArg = opt("trace");
if (traceArg) {
  const [p, fi, s] = traceArg.split("@");
  const r = await runPath(p!, Number(s ?? 1), Number(fi ?? 0));
  console.log(r.status);
  for (const f of r.fights) console.log(JSON.stringify({ label: f.label, outcome: f.outcome, rounds: f.rounds, hp: [f.hpStart, f.hpEnd], cp: f.cpEnd, sp: f.spEnd, dodge: f.dodge }), JSON.stringify(f.enemies));
  process.exit(0);
}

const sweepArg = opt("sweep");
if (sweepArg) {
  const base = HP;
  const cases: { name: string; params?: any; paths: string[]; seeds?: number }[] = loadJson(resolve(sweepArg));
  const rows: any[] = [];
  for (const c of cases) {
    setup(mergeParams(base, c.params ?? {}));
    for (const key of c.paths) {
      const runs = [];
      for (let i = 0; i < (c.seeds ?? seeds); i++) runs.push(await runPath(key, seed0 + i));
      const s = summarise(key, runs);
      const line = `${c.name.padEnd(24)} ${key.padEnd(34)} win ${String(s.wins).padStart(2)}/${s.runs} endHP ${s.endHpPctMedian}% p10 ${s.endHpPctP10} | ` +
        s.fights.map((f) => `F${f.fight} ${f.won}/${f.reached} r${f.roundsMedian} ${f.hpStartPctMedian}->${f.hpEndPctMedian}`).join(" | ");
      console.log(line);
      rows.push({ case: c.name, ...s, perSeed: undefined });
    }
  }
  const o = opt("out");
  if (o) writeFileSync(resolve(o), `${JSON.stringify(rows, null, 1)}\n`);
  process.exit(0);
}

const out: any = { generatedBy: "harness/skyglass_wreck_sim/engine/hunts_main.ts", settings: { dodge, maxRounds, seeds, seed0, variant: variant.name, dmgConfig: dmg.name, params: HP }, results: [] as any[] };
const t0 = Date.now();
for (const key of paths) {
  const runs = [];
  for (let i = 0; i < seeds; i++) runs.push(await runPath(key, seed0 + i));
  const s = summarise(key, runs);
  out.results.push(s);
  console.log(`\n=== ${key} (${s.hunt}) dodge=${dodge}: win ${s.wins}/${s.runs} end HP ${s.endHpPctMedian}% [p10 ${s.endHpPctP10}] losses ${JSON.stringify(s.lossesAt)} (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
  for (const f of s.fights) {
    console.log(`  F${f.fight} ${f.label.padEnd(52)} won ${f.won}/${f.reached} rnd ${f.roundsMedian} [${f.roundsP10}-${f.roundsP90}] HP ${f.hpStartPctMedian}->${f.hpEndPctMedian}% (p10 ${f.hpEndPctP10}) cp ${f.cpEndPctMedian} sp ${f.spEndPctMedian} pIdle ${f.playerIdleTurnsPct}%`);
    for (const [n, e] of Object.entries<any>(f.enemies)) console.log(`      ${n.padEnd(18)} mark% ${e.markFiredPct} marks ${e.marksPerFight} blasts ${e.blastsPerFight} hit% ${e.blastHitPct} win ${e.windowsPerFight} sig% ${e.signatureFiredPct} idle>r2 ${e.idleTurnsAfterR2Pct}% dealt ${e.dealtPerFight}`);
  }
}
const outPath = opt("out");
if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(resolve(outPath), `${JSON.stringify(out, null, 1)}\n`);
  console.log(`wrote ${outPath}`);
}
