/**
 * The Haul (engine/haul.ts), solo L100 S-rank professional + companion pet, offline and engine-driven.
 *
 *   TNR_SCRIPT=haul_main.ts run.sh [--params overrides/haul.params.json] [--quests hunter,gatherer] [--variant L100]
 *       [--seeds 40] [--seed 1] [--no-dodge] [--max-rounds 60]
 *       --paths all|CCL,CLLLC,...   evaluate paths as a shared prefix tree (every fight seeded by quest+seed+prefix)
 *       --fights [steps] [--alerts 0,1,3]  calibration: every crate/locker context from full HP
 *       --probe-hazards              each hazard alone vs none on a fixed fight (does it act as a starting debuff?)
 *       --repro quest@path@seed      run a path twice, compare actions/positions/HP (pets included)
 *       --spec-out file.json         quest state graphs + guard records + hazard tags (schema-checked)
 *       [--out results/haul_x.json]
 *
 * Each fight is a plain QUEST battle as initiateBattle builds a start_battle objective: opponent_scaled_to_user
 * (scaledRow), applyDebuffs via addQuestStartingEffects on the player; pools carry (cur HP/CP/SP written back,
 * status BATTLE: no regeneration), as in the charts harness. A lost / drawn / stalled fight fails the run.
 * Prefix tree: a path's fights are the fights of its prefixes, so every path (and every policy) is an exact
 * per-seed simulation; paths sharing a prefix share those fights (common random numbers).
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { addQuestStartingEffects } from "@/libs/combat/questEffects";
import { insertAiSchema } from "@/validators/aiInput";
import { questDebuffTypes, questStartingEffectsSchema } from "@/validators/combat";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, PLAYER_VARIANTS, petFor, playerQueryUser } from "./model";
import { assembleFloor, mulberry32, runFloor, seedEntropy } from "./sim";
import { auditTemplates, fixFallback, unmarkedReport } from "./fallback";
import { assertSpecRuleCap, overCapReport } from "./rulecap";
import { gateReport } from "./gates";
import { crownTemplates, DEFAULT_HUNT_PARAMS, DEFAULT_PARAMS, LIVE, NAME } from "./hunts";
import { buildCharts, type ChartParams, DEFAULT_CHART_EXTRA, scaledRow } from "./charts";
import { tag } from "./kitlib";
import {
  allPaths, buildGraph, copyId, DEFAULT_HAUL, fightFor, type FightDef, type HaulParams, hazardTag, optionsAt, pathFights, pathTiers,
  pathValue, questOf, startAlert, type Variant, variantKey, VALUE,
} from "./haul";
import { buildEndgame, CREW_TO_LIB } from "./hunts";
import { IDS } from "./kits";
import { LIB, MARKER_TYPES, type MarkKey } from "./library";
import { cast, cond, endTurn } from "./kitlib";

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
const chartParams = loadJson(join(HARNESS, "overrides/charts.params.json"));

const deepMerge = (a: any, b: any): any => {
  if (!b || typeof b !== "object" || Array.isArray(b)) return b ?? a;
  const o: any = { ...a };
  for (const [k, v] of Object.entries(b)) o[k] = v && typeof v === "object" && !Array.isArray(v) ? deepMerge(a?.[k] ?? {}, v) : v;
  return o;
};
const CP: ChartParams = deepMerge(deepMerge(deepMerge(DEFAULT_HUNT_PARAMS, huntParams), DEFAULT_CHART_EXTRA), chartParams);
const P: HaulParams = opt("params") ? deepMerge(DEFAULT_HAUL, loadJson(resolve(opt("params")!))) : DEFAULT_HAUL;
for (const [k, v] of args.filter((a) => a.startsWith("--set=")).map((a) => a.slice(6).split("="))) {
  // --set=copies.h-blade.stats=4 style quick overrides (numbers / JSON)
  const path = k!.split(".");
  let o: any = P;
  for (const p of path.slice(0, -1)) o = o[p];
  o[path[path.length - 1]!] = JSON.parse(v!);
}

/* ---------------- setup: the charts' records + the Haul copies ---------------- */
const built = buildCharts(CP, kitParams);
built.override.jutsu["nCQETf-HNnbRec1OSY2-R"] = coreRuptureV2;
const T = buildTemplates(baseline, built.override as never);
Object.assign(T.enemies, crownTemplates(T.enemies[LIVE.warden]!.row, T.jutsu, CP));
const sharedKits = (buildEndgame(kitParams, "endgame").override as any).newEnemies;
const SHARED_OF: Record<string, string> = { [LIVE.warden]: IDS.warden, [LIVE.wayfinder]: IDS.wayfinder, [LIVE.sentinel]: IDS.sentinel, [LIVE.blade]: IDS.blade };
const remap = (rules: any[]) => rules.map((r) => (r.action.jutsuId && CREW_TO_LIB[r.action.jutsuId] ? { ...r, action: { ...r.action, jutsuId: CREW_TO_LIB[r.action.jutsuId] } } : r));
const idgRows = (n: number) => Array.from({ length: n }, () => tag("increasedamagegiven", { power: 100, rounds: 99, calculation: "percentage", description: "Increased damage given" }));
const SET_PIECE_WHEN: Record<string, any[]> = { ring: [cond.within(0, 2)], sealLines: [cond.roundGt(1)], lines: [cond.roundGt(1)], rowsA: [cond.roundGt(1)] };
const COPY_META: Record<string, { id: string; name: string }> = {};
const COPY_NOTES: Record<string, string> = {};
for (const [k, c] of Object.entries(P.copies)) {
  const src = T.enemies[c.src];
  if (!src) throw new Error(`haul copy ${k}: source ${c.src} has no template`);
  const id = copyId(k);
  const row = structuredClone(src.row);
  Object.assign(row, { userId: id, username: c.name, poolsMultiplier: c.pools, statsMultiplier: c.stats, aiProfileId: `profile-${id}` });
  row.effects = [
    ...idgRows(c.rows),
    ...(c.taken ? [tag("increasedamagetaken", { power: c.taken, rounds: 99, calculation: "percentage", description: "Increased damage taken" })] : []),
    ...(c.givenDown ? [tag("decreasedamagegiven", { power: c.givenDown, rounds: 99, calculation: "percentage", description: "Decreased damage given" })] : []),
  ];
  const profile = { ...structuredClone(src.profile), id: `profile-${id}`, userId: id, name: c.name };
  let note = "source rules";
  if (c.rules === "shared" && SHARED_OF[c.src]) {
    profile.rules = remap(structuredClone(sharedKits[SHARED_OF[c.src]!].rules));
    profile.includeDefaultRules = false;
    note = `shared dungeon crew rules (${SHARED_OF[c.src]})`;
  }
  if (c.fuse) {
    // A set charge: stationary, bursts (live Core Rupture) on a player beside it, or when its fuse burns down.
    const rupture = "nCQETf-HNnbRec1OSY2-R";
    profile.rules = [
      cast(`Core Rupture: a player within ${c.fuse.adjacent}`, rupture, "CLOSEST_OPPONENT", [cond.within(0, c.fuse.adjacent)]),
      cast(`Core Rupture: the fuse (from round ${c.fuse.round})`, rupture, "CLOSEST_OPPONENT", [cond.roundGt(c.fuse.round - 1)]),
      endTurn("set into the growth (stationary)"),
    ];
    profile.includeDefaultRules = false;
    note = `set charge: stationary, Core Rupture adjacent (<= ${c.fuse.adjacent}) or fuse round ${c.fuse.round}`;
  }
  if (c.setPiece) {
    const mk = c.setPiece as MarkKey;
    const markId = LIB.mark[mk];
    const blastId = (LIB.blast as any)[mk] as string;
    const primed = cond.marker(1, MARKER_TYPES[mk]);
    profile.rules = [
      cast(`${mk}: blast (primed)`, blastId, "SELF", [primed]),
      endTurn(`${mk}: end turn after the mark`, [primed]),
      cast(`${mk}: mark`, markId, "SELF", SET_PIECE_WHEN[mk] ?? [cond.roundGt(1)]),
      ...profile.rules,
    ];
    for (const jid of [markId, blastId])
      if (!row.jutsus.some((uj: any) => uj.jutsuId === jid)) row.jutsus.push({ ...structuredClone(row.jutsus[0]), id: `${id}-${jid}`, jutsuId: jid, equipped: true, jutsu: structuredClone(T.jutsu[jid]) });
    note += ` + library set piece ${mk} (${markId} / ${blastId})`;
  }
  // RUL-2026-10-29-046: no fallback may cast a set piece unmarked (live-source rules: highest power -> basic attack).
  {
    const fx = fixFallback(profile, row.jutsus.map((uj: any) => uj.jutsuId));
    Object.assign(profile, fx.profile);
    if (fx.changes.length) note += `; fallback fix: ${fx.changes.join("; ")}`;
  }
  // Every rule's jutsu must be in the kit.
  for (const r of profile.rules) {
    const jid = r.action?.jutsuId;
    if (jid && jid !== "basicAttack" && !row.jutsus.some((uj: any) => uj.jutsuId === jid)) {
      if (!T.jutsu[jid]) throw new Error(`${k}: rule jutsu ${jid} unknown`);
      row.jutsus.push({ ...structuredClone(row.jutsus[0]), id: `${id}-${jid}`, jutsuId: jid, equipped: true, jutsu: structuredClone(T.jutsu[jid]) });
    }
  }
  row.jutsus = row.jutsus.map((uj: any) => ({ ...uj, userId: id }));
  T.enemies[id] = { row, profile, notes: [note] };
  NAME[id] = c.name;
  COPY_META[k] = { id, name: c.name };
  COPY_NOTES[k] = note;
}
const enemyRows: Record<string, any> = Object.fromEntries(Object.entries(T.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
// RUL-2026-10-28-026 item 2: the Crown Stonebound holds its own enemies-only copy of Erupting Ground (hunts.ts
// SKYGLASS_COPY); the shared live record is no longer patched here.
const donor = T.enemies[LIVE.warden]!.row;
{
  const auditPath = opt("audit-fallback");
  if (auditPath) {
    mkdirSync(dirname(resolve(auditPath)), { recursive: true });
    writeFileSync(resolve(auditPath), `${JSON.stringify(auditTemplates("haul", T.enemies, new Set(Object.values(COPY_META).map((m) => m.id))), null, 1)}\n`);
    console.log(`wrote ${auditPath}`);
    process.exit(0);
  }
}

const dodge = !flag("no-dodge");
const maxRounds = Number(opt("max-rounds", "60"));
const seeds = Number(opt("seeds", "40"));
const seed0 = Number(opt("seed", "1"));
const vk = opt("variant", "L100")!;
const VARIANTS: Record<string, any> = { L100: PLAYER_VARIANTS.average, L100noarmor: PLAYER_VARIANTS.noarmor };
const SEC_PER_TURN = 15;
const BASES = Object.keys(P.layouts);
const MODS = Object.keys(P.modifiers);
const parseVariants = (s: string): Variant[] => {
  if (s === "base") return BASES.map((l) => ({ layout: l, mod: null }));
  if (s === "mods") return BASES.flatMap((l) => MODS.map((m) => ({ layout: l, mod: m })));
  if (s === "all") return [...parseVariants("base"), ...parseVariants("mods")];
  return s.split(",").map((x) => {
    const [l, m] = x.split("+");
    if (!P.layouts[l!]) throw new Error(`layout ${l}?`);
    if (m && !P.modifiers[m]) throw new Error(`modifier ${m}?`);
    return { layout: l!, mod: m ?? null };
  });
};
const variants = parseVariants(opt("variants", "base")!);

const fnv = (s: string) => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619) >>> 0;
  return h || 1;
};

/* ---------------- one fight ---------------- */
type St = { seed: number; hp: number | null; cp: number; sp: number; rounds: number };
type LossDiag = { stunsOnPlayer: number; maxStepLossPct: number; lostTurns: number };
type FightOut = { won: boolean; outcome: string; rounds: number; hp: number; cp: number; sp: number; hpStart: number; dodge: any; sig?: string[]; diag: LossDiag };
let BASE_HP = 5050;
const runFight = async (st: St, f: FightDef, fseed: number, detail = false): Promise<FightOut> => {
  const orig = Math.random;
  const rand = mulberry32(fseed);
  seedEntropy(fseed);
  Math.random = rand;
  try {
    const player = playerQueryUser(0, VARIANTS[vk], donor, T.jutsu);
    BASE_HP = player.maxHealth;
    if (st.hp !== null) {
      player.curHealth = Math.round(st.hp);
      player.curChakra = Math.round(st.cp);
      player.curStamina = Math.round(st.sp);
      player.status = "BATTLE";
    }
    const pets = [petFor(player)];
    player.activePetId = pets[0]!.id;
    const ids = f.ids.map(copyId);
    const rows = { ...enemyRows, ...Object.fromEntries(ids.map((id) => [id, scaledRow(enemyRows[id], player.level)])) };
    const battle = await assembleFloor({ players: [player], enemyRows: rows, floor: { kind: "floor", waves: [{ aiIds: ids, delayRounds: 0 }] }, rand, initialBarriers: true, dmgConfig: dmg.config, mode: "quest", pets });
    const pu = battle.usersState.find((u) => u.userId === player.userId)!;
    if (f.debuffs.length) addQuestStartingEffects(pu, battle.usersEffects, f.debuffs as never, "quest-haul");
    const hpStart = pu.curHealth;
    const res = runFloor(battle, { playerIds: [player.userId], maxRounds, dodge, detail });
    const fin = res.final[player.userId]!;
    // Loss diagnostics: stuns landed on the player, the biggest single-step HP loss, player rounds with no action.
    let stuns = 0;
    let maxLoss = 0;
    const acted = new Set<number>();
    const rounds = new Set<number>();
    for (const s of res.steps) {
      for (const e of s.effects) if (e.type === "stun" && e.target === player.userId) stuns++;
      const d = s.hp[player.userId] ?? 0;
      if (d < 0) maxLoss = Math.max(maxLoss, -d);
      rounds.add(s.round);
      if (s.human && s.actionId) acted.add(s.round);
    }
    const sig = detail
      ? [`start ${battle.usersState.map((u) => `${u.username}@${u.longitude},${u.latitude}`).join(" ")}`, ...res.steps.map((s) => `r${s.round} ${s.actor} ${s.actionId} ${s.actorFrom} ${s.actorTo} ${JSON.stringify(s.hp)}`)]
      : undefined;
    return {
      won: res.outcome === "won", outcome: res.outcome, rounds: res.rounds, hp: Math.max(0, fin.hp), cp: fin.cp, sp: fin.sp, hpStart, dodge: res.dodge, sig,
      diag: { stunsOnPlayer: stuns, maxStepLossPct: (100 * maxLoss) / BASE_HP, lostTurns: [...rounds].filter((r) => !acted.has(r)).length },
    };
  } finally {
    Math.random = orig;
  }
};

/* ---------------- stats helpers ---------------- */
const median = (xs: number[]) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m]! : (s[m - 1]! + s[m]!) / 2;
};
const mean = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);
const r1 = (x: number | null) => (x === null ? null : Math.round(x * 10) / 10);
const r2 = (x: number | null) => (x === null ? null : Math.round(x * 100) / 100);
const hpPct = (hp: number) => (100 * hp) / BASE_HP;

type FightAgg = { key: string; label: string; reached: number; won: number; rounds: number[]; hpStart: number[]; hpEnd: number[]; outcomes: Record<string, number>; lossDiag: LossDiag[]; winStuns: number[] };
const newAgg = (f: FightDef): FightAgg => ({ key: f.key, label: f.label, reached: 0, won: 0, rounds: [], hpStart: [], hpEnd: [], outcomes: {}, lossDiag: [], winStuns: [] });
const addAgg = (a: FightAgg, r: FightOut) => {
  a.reached++;
  a.rounds.push(r.rounds);
  a.hpStart.push(hpPct(r.hpStart));
  a.outcomes[r.outcome] = (a.outcomes[r.outcome] ?? 0) + 1;
  if (r.won) {
    a.won++;
    a.hpEnd.push(hpPct(r.hp));
    a.winStuns.push(r.diag.stunsOnPlayer);
  } else a.lossDiag.push(r.diag);
};
const sumAgg = (a: FightAgg) => {
  const wonR = a.rounds.filter((_, i) => true);
  void wonR;
  const sorted = [...a.rounds].sort((x, y) => x - y);
  return {
    key: a.key, label: a.label, reached: a.reached, won: a.won, winPct: r1((100 * a.won) / Math.max(1, a.reached)),
    roundsMedian: median(a.rounds), roundsP90: sorted.length ? sorted[Math.floor(0.9 * (sorted.length - 1) + 0.5)] : null,
    hpStartMedian: r1(median(a.hpStart)), hpEndMedian: r1(median(a.hpEnd)), hpCostMedian: r1((median(a.hpStart) ?? 0) - (median(a.hpEnd) ?? 0)), outcomes: a.outcomes,
    losses: a.lossDiag.length,
    lossStunsMean: r1(mean(a.lossDiag.map((d) => d.stunsOnPlayer))), winStunsMean: r1(mean(a.winStuns)),
    lossMaxStepPctMedian: r1(median(a.lossDiag.map((d) => d.maxStepLossPct))),
    // "coin-flip" losses: 2+ stuns landed, or one step took 40%+ of base HP
    chainLosses: a.lossDiag.filter((d) => d.stunsOnPlayer >= 2 || d.maxStepLossPct >= 40).length,
  };
};

/* ---------------- exact prefix-tree path evaluation (named paths) ---------------- */
const evalPathsExact = async (v: Variant, targets: string[]) => {
  const legal = new Set(allPaths(P, v));
  for (const t of targets) if (!legal.has(t)) throw new Error(`${variantKey(v)}: path ${t} is not legal`);
  const prefixes = new Set<string>();
  for (const t of targets) for (let i = 0; i <= t.length; i++) prefixes.add(t.slice(0, i));
  const want = new Set(targets);
  const fights = new Map<string, FightAgg>();
  const paths: any[] = [];
  type Fail = { rounds: number; step: number };
  const visit = async (prefix: string, alert: number, pendingFrom: number | null, pop: St[], fails: Fail[]) => {
    const step = prefix.length + 1;
    const record = () => {
      const haul = pathValue(P, v, prefix);
      const n = pop.length + fails.length;
      const clearRounds = pop.map((s) => s.rounds);
      paths.push({
        path: prefix, tiers: pathTiers(P, v, prefix).join(""), haulM: r2(haul), seeds: n, clears: pop.length, clearPct: r1((100 * pop.length) / n), evM: r2((haul * pop.length) / n),
        minutesClearMedian: r1(((median(clearRounds) ?? 0) * SEC_PER_TURN) / 60), minutesAllMean: r1(((mean([...clearRounds, ...fails.map((f) => f.rounds)]) ?? 0) * SEC_PER_TURN) / 60),
        failsAtStep: fails.reduce((m: any, f) => ((m[f.step] = (m[f.step] ?? 0) + 1), m), {}),
      });
    };
    if (step > 5) return void (want.has(prefix) && record());
    for (const o of optionsAt(P, v, step, pendingFrom !== null)) {
      if (o === "leave") {
        if (want.has(prefix)) record();
        continue;
      }
      const np = prefix + o;
      if (!prefixes.has(np)) continue;
      if (o === "X") {
        await visit(np, alert, step, pop, fails);
        continue;
      }
      const f = fightFor(P, v, o, step, alert, pendingFrom);
      const agg = newAgg(f);
      fights.set(np, agg);
      const next: St[] = [];
      const nf = [...fails];
      for (const st of pop) {
        const r = await runFight(st, f, fnv(`${variantKey(v)}|${st.seed}|${np}`));
        addAgg(agg, r);
        if (r.won) next.push({ seed: st.seed, hp: r.hp, cp: r.cp, sp: r.sp, rounds: st.rounds + r.rounds });
        else nf.push({ rounds: st.rounds + r.rounds, step });
      }
      process.stderr.write(`  ${variantKey(v)} ${np.padEnd(5)} won ${agg.won}/${agg.reached} rnd ${median(agg.rounds)} hp ${r1(median(agg.hpStart))}->${r1(median(agg.hpEnd))}\n`);
      await visit(np, o === "L" ? alert + 1 : alert, null, next, nf);
    }
  };
  await visit("", startAlert(P, v), null, Array.from({ length: seeds }, (_, i) => ({ seed: seed0 + i, hp: null, cp: 0, sp: 0, rounds: 0 })), []);
  return { variant: variantKey(v), method: "exact prefix tree", paths, fights: Object.fromEntries([...fights.entries()].map(([k, a]) => [k, sumAgg(a)])) };
};

/* ---------------- state-merged exhaustive evaluation (every legal path) ---------------- */
/**
 * The fights depend on (step, alertness, pending cut) and the carried pools, not on the haul. Every state is evaluated
 * once with `seeds` particles: the survivors of all incoming fights, merged in equal shares (round-robin, then the
 * first `seeds`). A path's clear rate is the product of its fights' win rates at its states. Approximation: a path's
 * fights see the merged pool distribution of their state, not that path's own; checked against the exact tree.
 */
const evalPathsMerged = async (v: Variant) => {
  const stateKey = (s: number, a: number, p: number | null) => `${s}|${Math.min(a, 3)}|${p ?? "-"}`;
  const inbound = new Map<string, St[][]>();
  const push = (k: string, pop: St[]) => {
    if (!inbound.has(k)) inbound.set(k, []);
    inbound.get(k)!.push(pop);
  };
  const res = new Map<string, { agg: FightAgg; rounds: number | null }>(); // stateKey|kind
  push(stateKey(1, startAlert(P, v), null), Array.from({ length: seeds }, (_, i) => ({ seed: seed0 + i, hp: null, cp: 0, sp: 0, rounds: 0 })));
  for (let s = 1; s <= 5; s++) {
    for (const [k, lists] of [...inbound.entries()].filter(([k]) => k.startsWith(`${s}|`))) {
      const [, as, ps] = k.split("|");
      const a = Number(as);
      const p = ps === "-" ? null : Number(ps);
      const merged: St[] = [];
      for (let i = 0; merged.length < seeds && lists.some((l) => l.length > i); i++) for (const l of lists) if (l[i] && merged.length < seeds) merged.push(l[i]!);
      for (const o of optionsAt(P, v, s, p !== null)) {
        if (o === "leave") continue;
        if (o === "X") {
          if (s < 5) push(stateKey(s + 1, a, s), merged);
          continue;
        }
        const f = fightFor(P, v, o, s, a, p);
        const agg = newAgg(f);
        const next: St[] = [];
        for (const st of merged) {
          const r = await runFight(st, f, fnv(`${variantKey(v)}|${st.seed}|${k}|${o}`));
          addAgg(agg, r);
          if (r.won) next.push({ seed: st.seed, hp: r.hp, cp: r.cp, sp: r.sp, rounds: st.rounds + r.rounds });
        }
        res.set(`${k}|${o}`, { agg, rounds: median(agg.rounds.filter((_, i) => true)) });
        process.stderr.write(`  ${variantKey(v)} ${`${k}|${o}`.padEnd(10)} n ${merged.length} won ${agg.won}/${agg.reached} rnd ${median(agg.rounds)} hp ${r1(median(agg.hpStart))}->${r1(median(agg.hpEnd))}\n`);
        if (s < 5 && next.length) push(stateKey(s + 1, o === "L" ? a + 1 : a, null), next);
      }
    }
  }
  const paths = allPaths(P, v).filter((p) => p.length).map((path) => {
    let clear = 1;
    let rounds = 0;
    let roundsAll = 0;
    for (const f of pathFights(P, v, path)) {
      const r = res.get(`${stateKey(f.step, f.alert, f.pendingFrom)}|${f.kind}`);
      if (!r) return null;
      const w = r.agg.won / Math.max(1, r.agg.reached);
      roundsAll += clear * (r.rounds ?? 0);
      clear *= w;
      rounds += r.rounds ?? 0;
    }
    const haul = pathValue(P, v, path);
    return {
      path, tiers: pathTiers(P, v, path).join(""), lockers: [...path].filter((c) => c === "L").length, cuts: [...path].filter((c) => c === "X").length,
      haulM: r2(haul), clearPct: r1(100 * clear), evM: r2(haul * clear), minutesClear: r1((rounds * SEC_PER_TURN) / 60), minutesExpected: r1((roundsAll * SEC_PER_TURN) / 60),
    };
  }).filter(Boolean);
  return { variant: variantKey(v), method: "state-merged", seeds, paths, fights: Object.fromEntries([...res.entries()].map(([k, r]) => [k, sumAgg(r.agg)])) };
};

/* ---------------- modes ---------------- */
const writeOut = (o: any) => {
  const out = opt("out");
  if (!out) return;
  if (o && typeof o === "object" && !Array.isArray(o)) { o.fallbackGuard = unmarkedReport(); o.ruleCap = overCapReport(); o.gates = gateReport(); }
  mkdirSync(dirname(resolve(out)), { recursive: true });
  writeFileSync(resolve(out), `${JSON.stringify(o, null, 1)}\n`);
  console.log(`wrote ${out}`);
};
const settings = () => ({ dodge, maxRounds, seeds, seed0, variant: vk, variantNote: VARIANTS[vk].note, secondsPerTurn: SEC_PER_TURN, dmgConfig: dmg.name, params: P, copyRules: COPY_NOTES });

if (opt("revalue")) {
  // Recompute haul values / EVs of a results file with the current params (clear rates unchanged: haul-only edits).
  const d = loadJson(resolve(opt("revalue")!));
  for (const r of d.results) {
    const v = parseVariants(r.variant)[0]!;
    for (const p of r.paths) {
      const h = pathValue(P, v, p.path);
      p.haulM = r2(h);
      p.tiers = pathTiers(P, v, p.path).join("");
      p.evM = r2((h * p.clearPct) / 100);
    }
  }
  d.settings.params = P;
  d.revalued = "haul values recomputed with the current params (haul_main.ts --revalue); clear rates from the original run";
  writeOut(d);
  process.exit(0);
}

if (flag("list")) {
  for (const [k, c] of Object.entries(P.copies)) {
    const r = scaledRow(enemyRows[copyId(k)], 100);
    console.log(`${k.padEnd(14)} ${c.name.padEnd(18)} copy of ${(NAME[c.src] ?? c.src).padEnd(16)} sMult ${c.stats} pools ${c.pools} rows ${c.rows} -> HP ${r.maxHealth} off ${Math.round(r.offence)} | ${COPY_NOTES[k]} | rules ${T.enemies[copyId(k)]!.profile.rules.map((x: any) => x.action.description).join("; ").slice(0, 300)}`);
  }
  for (const v of parseVariants("all")) console.log(`${variantKey(v).padEnd(18)} legal paths ${allPaths(P, v).length}`);
  process.exit(0);
}

if (opt("spec-out")) {
  const RELS = new Set(["jutsus", "items", "aiProfile", "titles", "raidBuffs", "cookingJobs", "village", "bloodline", "sageMode", "anbuSquad", "clan", "loadout", "userSkills", "userQuests", "completedQuests", "bounties", "bountySignups", "queue"]);
  const records: any = {};
  for (const [k, c] of Object.entries(P.copies)) {
    const id = copyId(k);
    const e = T.enemies[id]!;
    const row = e.row;
    const check = insertAiSchema.safeParse({ ...Object.fromEntries(Object.entries(row).filter(([kk, val]) => !RELS.has(kk) && !(val && typeof (val as any).getTime === "function"))), jutsus: row.jutsus.map((uj: any) => uj.jutsuId) });
    const at100 = scaledRow(enemyRows[id], 100);
    const issues = check.success ? [] : check.error.issues.filter((i: any) => !/date/i.test(i.message));
    records[id] = {
      key: k, name: c.name, role: c.role, copyOf: { id: c.src, name: NAME[c.src] }, statsMultiplier: c.stats, poolsMultiplier: c.pools, damageRows: c.rows,
      innate: row.effects.map((x: any) => `${x.type} ${x.power}${x.calculation === "percentage" ? "%" : ""}`), opponent_scaled_to_user: true,
      atLevel100: { maxHealth: at100.maxHealth, offence: Math.round(at100.offence), defence: Math.round(at100.defence) },
      rulesNote: COPY_NOTES[k], jutsu: row.jutsus.map((uj: any) => ({ id: uj.jutsuId, name: uj.jutsu?.name })),
      rules: e.profile.rules.map((r: any) => ({ when: r.conditions, do: { type: r.action.type, jutsuId: r.action.jutsuId, target: r.action.target }, note: r.action.description })),
      insertAiSchema: issues.length ? issues.slice(0, 3).map((i: any) => `${i.path.join(".")}: ${i.message}`).join("; ") : "pass",
    };
  }
  const graphs: any = {};
  const counts: any = {};
  for (const v of parseVariants("all")) {
    const g = buildGraph(P, v, COPY_META);
    let bad = 0;
    for (const b of g.battles) if (!questStartingEffectsSchema(questDebuffTypes).safeParse(b.applyDebuffs).success) bad++;
    graphs[variantKey(v)] = { ...g, applyDebuffsSchemaFailures: bad };
    counts[variantKey(v)] = { ...g.counts, applyDebuffsSchemaFailures: bad };
    console.log(`${variantKey(v).padEnd(18)} ${JSON.stringify(g.counts)} schemaFail ${bad}`);
  }
  const spec = {
    generatedBy: "harness/skyglass_wreck_sim/engine/haul_main.ts --spec-out", engineRun: "c86f43f4 (harness pin); source checks cite theninjarpg@2af4b320",
    design: "docs/design/SKYGLASS_THE_HAUL.md (RUL-2026-10-29-037, -038)",
    note: "Placeholder ids (haul-*); the builder mints real ids. Each choice node is a dialog objective: its options route to a battle (start_battle; nextObjectiveId on a win, failObjectiveId 'fail'), straight to the next choice node (cut), or to the haul's win_quest ending (leave). Battles carry no rewards; endings pay the chests as reward_items (number = drop chance %), locker bonus chests as their own entries. All battles opponent_scaled_to_user; no givePools (pools carry). Modified quests (layout+modifier) are the steeping outputs.",
    params: P, records, counts, graphs,
  };
  mkdirSync(dirname(resolve(opt("spec-out")!)), { recursive: true });
  assertSpecRuleCap("haul_spec", spec);
  writeFileSync(resolve(opt("spec-out")!), `${JSON.stringify(spec)}\n`);
  console.log(`wrote ${opt("spec-out")}: record schema failures ${Object.values<any>(records).filter((r) => r.insertAiSchema !== "pass").map((r) => r.key).join(",") || "none"}`);
  process.exit(0);
}

const reproArg = opt("repro");
if (reproArg) {
  const [vs, path, sd] = reproArg.split("@") as [string, string, string];
  const v = parseVariants(vs)[0]!;
  const sigs: string[][] = [];
  for (let i = 0; i < 2; i++) {
    const sig: string[] = [];
    let st: St = { seed: Number(sd), hp: null, cp: 0, sp: 0, rounds: 0 };
    for (const fs of pathFights(P, v, path)) {
      const f = fightFor(P, v, fs.kind, fs.step, fs.alert, fs.pendingFrom);
      const r = await runFight(st, f, fnv(`${variantKey(v)}|${st.seed}|${path.slice(0, fs.step)}`), true);
      sig.push(`fight ${fs.step} ${f.key} ${r.outcome}`, ...r.sig!);
      if (!r.won) break;
      st = { ...st, hp: r.hp, cp: r.cp, sp: r.sp };
    }
    sigs.push(sig);
  }
  const n = Math.max(sigs[0]!.length, sigs[1]!.length);
  const diff = [...Array(n).keys()].find((i) => sigs[0]![i] !== sigs[1]![i]);
  const pet = sigs[0]!.filter((l) => l.startsWith("start")).map((l) => l.split(" ").find((x) => x.includes("companion@"))).join(" ");
  console.log(diff === undefined ? `REPRO OK ${reproArg}: ${n} lines identical (actions, positions, HP); pet start cells ${pet}` : `REPRO DIFF ${reproArg} at ${diff}:\n  ${sigs[0]![diff]}\n  ${sigs[1]![diff]}`);
  process.exit(diff === undefined ? 0 : 1);
}

if (flag("probe-hazards")) {
  // Each hazard alone on a fixed fight (the layout's step-3 crate, no other hazard) vs none, same seeds.
  const out: any[] = [];
  const rounds = Number(opt("hz-rounds", "2"));
  for (const v of variants) {
    const base = fightFor(P, v, (opt("hz-kind", "C") as "C" | "L"), Number(opt("hz-step", "3")), 0, null);
    const runSet = async (debuffs: any[]) => {
      const rs: FightOut[] = [];
      for (let i = 0; i < seeds; i++) rs.push(await runFight({ seed: seed0 + i, hp: null, cp: 0, sp: 0, rounds: 0 }, { ...base, debuffs }, fnv(`probe|${variantKey(v)}|${seed0 + i}`), true));
      return rs;
    };
    const none = await runSet([]);
    for (const key of ["none", ...P.layouts[v.layout]!.hazards]) {
      const rs = key === "none" ? none : await runSet([hazardTag(P, key, rounds)]);
      const same = rs.filter((r, i) => JSON.stringify(r.sig) === JSON.stringify(none[i]!.sig)).length;
      const cost = rs.map((r, i) => hpPct(none[i]!.hp) - hpPct(r.hp));
      const row = { variant: variantKey(v), hazard: key, engineType: key === "none" ? null : P.hazard[key]!.type, power: P.hazard[key]?.power, rounds, won: rs.filter((r) => r.won).length, n: rs.length, roundsMedian: median(rs.map((r) => r.rounds)), hpCostVsNoneMean: r1(mean(cost)), cpEndMean: r1(mean(rs.map((r) => r.cp))), identicalToNone: same };
      out.push(row);
      console.log(JSON.stringify(row));
    }
  }
  writeOut({ generatedBy: "haul_main.ts --probe-hazards", settings: settings(), probes: out });
  process.exit(0);
}

if (opt("solo")) {
  // Guard strength probe: each listed composition ("a+b") alone, no hazards, from full HP.
  const rows: any[] = [];
  for (const comp of opt("solo")!.split(",")) {
    const f: FightDef = { key: `solo:${comp}`, label: comp, ids: comp.split("+"), debuffs: [], hazards: [] };
    const agg = newAgg(f);
    for (let i = 0; i < seeds; i++) addAgg(agg, await runFight({ seed: seed0 + i, hp: null, cp: 0, sp: 0, rounds: 0 }, f, fnv(`solo|${seed0 + i}|${comp}`)));
    const row = sumAgg(agg);
    rows.push(row);
    console.log(`${comp.padEnd(48)} won ${row.won}/${row.reached} rnd ${row.roundsMedian} (p90 ${row.roundsP90}) cost ${row.hpCostMedian} chain ${row.chainLosses} stuns(win) ${row.winStunsMean}`);
  }
  writeOut({ generatedBy: "haul_main.ts --solo", settings: settings(), rows });
  process.exit(0);
}

if (flag("fights")) {
  const steps = opt("steps", "1,2,3,4,5")!.split(",").map(Number);
  const alerts = opt("alerts", "0,1,3")!.split(",").map(Number);
  const kinds = opt("kinds", "C,L")!.split(",") as ("C" | "L")[];
  const rows: any[] = [];
  for (const v of variants)
    for (const kind of kinds)
      for (const s of steps)
        for (const a0 of alerts) {
          const a = a0 + startAlert(P, v);
          if (a0 > s - 1 || (kind === "L" && !optionsAt(P, v, s, false).includes("L"))) continue;
          const f = fightFor(P, v, kind, s, a, flag("pending") && s > 1 ? s - 1 : null);
          const agg = newAgg(f);
          for (let i = 0; i < seeds; i++) addAgg(agg, await runFight({ seed: seed0 + i, hp: null, cp: 0, sp: 0, rounds: 0 }, f, fnv(`cal|${seed0 + i}|${f.key}`)));
          const row = sumAgg(agg);
          rows.push(row);
          console.log(`${f.key.padEnd(30)} won ${String(row.won).padStart(2)}/${row.reached} rnd ${row.roundsMedian} cost ${row.hpCostMedian} end ${row.hpEndMedian} chain ${row.chainLosses} | ${f.label}`);
        }
  writeOut({ generatedBy: "haul_main.ts --fights", settings: settings(), rows });
  process.exit(0);
}

const pathArg = opt("paths");
if (pathArg || flag("exhaustive")) {
  const results: any[] = [];
  for (const v of variants) {
    const t0 = performance.now();
    const r = pathArg ? await evalPathsExact(v, pathArg.split(",").filter((p) => allPaths(P, v).includes(p))) : await evalPathsMerged(v);
    results.push({ ...r, quest: questOf(P, v), wallMin: r1((performance.now() - t0) / 60000) });
    console.log(`\n=== ${variantKey(v)} ${r.method} dodge=${dodge} seeds=${seeds} (${((performance.now() - t0) / 60000).toFixed(1)} min wall)`);
    for (const p of [...r.paths].sort((a: any, b: any) => b.evM - a.evM).slice(0, Number(opt("top", "12"))))
      console.log(`  ${p.path.padEnd(5)} ${p.tiers.padEnd(5)} haul ${String(p.haulM).padStart(5)}M clear ${p.clearPct}% EV ${p.evM}M min ${p.minutesClearMedian ?? p.minutesClear}`);
  }
  writeOut({ generatedBy: `haul_main.ts ${pathArg ? "--paths" : "--exhaustive"}`, settings: settings(), values: VALUE, results });
  process.exit(0);
}
console.log("nothing to do: pass --exhaustive, --paths, --fights, --probe-hazards, --repro, --list or --spec-out");
