/**
 * Skyglass Wreck harness CLI.
 *
 *   bun run tnr_skyglass_wreck_sim/main.ts [--override file.json] [--variants a,b] [--runs 30]
 *       [--seed 1] [--max-wipes 3] [--max-rounds 150] [--floors 0,1] [--no-barriers]
 *       [--out results/name.json] [--probe-check]
 *
 * A run plays the dungeon as routers/dungeon.ts does: floors in order, each a fresh battle with
 * full pools (forceKeepPools; a won floor restores everyone, a wipe revives everyone); a wipe on a
 * "floor"/"boss" room returns the party to the tier's first floor (dungeonNextState). Waves inside
 * a floor share one battle (pools, effects and the round counter carry over).
 */
import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import {
  buildTemplates,
  loadDmgConfig,
  describePlayer,
  enemyQueryUser,
  loadJson,
  type Override,
  PLAYER_VARIANTS,
  type PlayerVariant,
  playerQueryUser,
  type Templates,
} from "./model";
import { assembleFloor, type FloorResult, mulberry32, runFloor, seedEntropy } from "./sim";

const args = process.argv.slice(2);
const opt = (k: string, d?: string) => {
  const i = args.indexOf(`--${k}`);
  return i >= 0 ? args[i + 1] : d;
};
const flag = (k: string) => args.includes(`--${k}`);
const HARNESS = process.env.TNR_HARNESS!;
const baseline = loadJson(join(HARNESS, "data/baseline.json"));
const ovPath = opt("override");
const override: Override = ovPath ? loadJson(resolve(ovPath)) : {};
const runs = Number(opt("runs", "30"));
const seed0 = Number(opt("seed", "1"));
const maxWipes = Number(opt("max-wipes", "3"));
const maxRounds = Number(opt("max-rounds", "150"));
const barriers = !flag("no-barriers");
/** Harness auto-player dodge of marked hexes (sim.ts DANGER_ANIMS); on unless --no-dodge. */
const dodgeOn = !flag("no-dodge");
const dmg = loadDmgConfig(HARNESS, opt("dmg-config", "live"));
const onlyFloors = opt("floors")?.split(",").map(Number);
const PACES = [10, 15, 20];
const AI_SECONDS = [0, 1.5];
const TRANSITION_SECONDS = 30;
const LIMIT = 3600;

const T: Templates = buildTemplates(baseline, override);
const variants: PlayerVariant[] = (opt("variants", "baseline,cap,geared,strong,elite") as string).split(",").map((n) => {
  const base = PLAYER_VARIANTS[n] ?? (override.players?.[n] ? { ...PLAYER_VARIANTS.cap!, name: n, note: "override-defined" } : undefined);
  if (!base) throw new Error(`unknown player variant ${n}`);
  return { ...base, ...(override.players?.[n] ?? {}), name: n } as PlayerVariant;
});
const donor = T.enemies["texZaFi42S3EvJZBwQ8cd"]?.row ?? Object.values(T.enemies)[0]!.row; // field-set donor only
const enemyRows = Object.fromEntries(Object.entries(T.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
const floors = onlyFloors ? onlyFloors.map((i) => T.floors[i]!) : T.floors;
const floorLabel = (i: number) => (onlyFloors ? onlyFloors[i]! : i); // original floor index

const BASIC: Record<string, string> = {
  move: "move", wait: "wait (end turn)", basicAttack: "basic attack", meditate: "meditate",
  basicHeal: "basic heal", flee: "flee", cleanse: "cleanse", clear: "clear",
};
const actionName = (id: string | null) =>
  id === null ? "(no action)" : (T.jutsu[id]?.name ?? BASIC[id] ?? id);
const IDLE = new Set(["move", "wait", null as unknown as string]);

/* ---------------- run model ---------------- */
type Attempt = { floor: number; res: FloorResult; seed: number };
const runDungeon = async (v: PlayerVariant, seed: number, probeOn = true) => {
  const rand = mulberry32(seed);
  seedEntropy(seed);
  const origRandom = Math.random;
  Math.random = rand;
  const g = globalThis as any;
  try {
    const players = [0, 1, 2].map((i) => playerQueryUser(i, v, donor, T.jutsu));
    const attempts: Attempt[] = [];
    let f = 0;
    let wipes = 0;
    let status: "cleared" | "max-wipes" | "ended" | "stalled" = "stalled";
    while (f < floors.length) {
      const battle = await assembleFloor({ players, enemyRows, floor: floors[f]!, rand, initialBarriers: barriers, dmgConfig: dmg.config });
      const res = runFloor(battle, { playerIds: players.map((p) => p.userId), maxRounds, dodge: dodgeOn });
      if (!probeOn) g.__TNR_RULE_PROBE__ = undefined;
      attempts.push({ floor: f, res, seed });
      if (res.outcome === "won") f++;
      else if (res.outcome === "wipe") {
        wipes++;
        if (wipes > maxWipes) {
          status = "max-wipes";
          break;
        }
        f = floors[f]!.kind === "mini-boss" ? f : 0; // dungeonNextState: tier start (one tier)
      } else {
        status = res.outcome === "ended" ? "ended" : "stalled";
        break;
      }
    }
    if (f >= floors.length) status = "cleared";
    return { seed, status, wipes, attempts };
  } finally {
    Math.random = origRandom;
  }
};

/* ---------------- aggregation helpers ---------------- */
const median = (xs: number[]) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m]! : (s[m - 1]! + s[m]!) / 2;
};
const pct = (xs: number[], p: number) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  return s[Math.min(s.length - 1, Math.floor(p * (s.length - 1) + 0.5))]!;
};
const r1 = (x: number | null) => (x === null ? null : Math.round(x * 10) / 10);
const inc = (o: Record<string, number>, k: string, n = 1) => {
  o[k] = (o[k] ?? 0) + n;
};

type EnemyAgg = {
  /** Per authored rule: how many appearances fired it never / exactly once / more than once. */
  ruleFireDist?: Record<string, { never: number; once: number; more: number }>;
  aiId: string; name: string; appearances: number; deaths: number; diedAfterRounds: number[];
  turns: number; actions: Record<string, number>; ruleFires: Record<string, number>;
  authoredRules: number; dealt: number; taken: number; healed: number;
  effectsApplied: Record<string, number>; idleActions: number; totalActions: number;
  /** Turns from the enemy's 3rd round in its wave on, and those with only move / end turn (acceptance: <= 25%). */
  idleAfterR2: number; actionsAfterR2: number;
  /** Appearances in which at least one signature rule fired (override.signatures). */
  signatureFired: number;
};
const signatures: Record<string, number[]> = (override as any).signatures ?? {};

const summarise = (v: PlayerVariant, results: Awaited<ReturnType<typeof runDungeon>>[]) => {
  const waveKey = (f: number, w: number) => `F${floorLabel(f) + 1}W${w}`;
  const waves: Record<string, any> = {};
  const enemies: Record<string, Record<string, EnemyAgg>> = {}; // waveKey -> aiId -> agg
  const enemyAll: Record<string, EnemyAgg> = {};
  const players: Record<string, any> = {};
  const floorsAgg: Record<string, any> = {};
  for (const run of results) {
    for (const at of run.attempts) {
      const res = at.res;
      const fk = `F${floorLabel(at.floor) + 1}`;
      const fa = (floorsAgg[fk] ??= { attempts: 0, won: 0, wipes: 0, rounds: [], humanTurns: [], aiTurns: [] });
      fa.attempts++;
      if (res.outcome === "won") fa.won++;
      if (res.outcome === "wipe") fa.wipes++;
      fa.rounds.push(res.rounds);
      fa.humanTurns.push(res.humanTurns);
      fa.aiTurns.push(res.aiTurns);
      const uidToWave = new Map<string, number>();
      for (const w of res.waves) {
        const k = waveKey(at.floor, w.wave);
        const wa = (waves[k] ??= { attempts: 0, cleared: 0, wipedHere: 0, rounds: [], humanTurns: [], aiTurns: [], hpLostPct: [], poolsEnd: { hp: [], cp: [], sp: [], alive: [] }, enemies: w.enemies.map((e) => e.name) });
        wa.attempts++;
        if (w.endRound !== null) {
          wa.cleared++;
          wa.rounds.push(w.endRound - w.startRound + 1);
          const pe = Object.values(w.poolsAtEnd ?? {});
          wa.poolsEnd.hp.push(pe.reduce((s, p) => s + p.hp, 0) / pe.length);
          wa.poolsEnd.cp.push(pe.reduce((s, p) => s + p.cp, 0) / pe.length);
          wa.poolsEnd.sp.push(pe.reduce((s, p) => s + p.sp, 0) / pe.length);
          wa.poolsEnd.alive.push(pe.filter((p) => p.alive).length);
        } else if (res.outcome === "wipe") wa.wipedHere++;
        wa.humanTurns.push(w.humanTurns);
        wa.aiTurns.push(w.aiTurns);
        wa.hpLostPct.push((100 * w.partyHpLost) / w.partyHpMax);
        for (const e of w.enemies) {
          uidToWave.set(e.uid, w.wave);
          for (const bucket of [((enemies[k] ??= {})), enemyAll]) {
            const ea = (bucket[e.aiId] ??= { aiId: e.aiId, name: e.name, appearances: 0, deaths: 0, diedAfterRounds: [], turns: 0, actions: {}, ruleFires: {}, authoredRules: 0, dealt: 0, taken: 0, healed: 0, effectsApplied: {}, idleActions: 0, totalActions: 0, idleAfterR2: 0, actionsAfterR2: 0, signatureFired: 0 });
            ea.appearances++;
            if (e.diedRound !== null) {
              ea.deaths++;
              ea.diedAfterRounds.push(e.diedRound - w.startRound + 1);
            }
          }
        }
      }
      // steps
      const seenTurn = new Set<string>();
      const waveStart = new Map(res.waves.map((w) => [w.wave, w.startRound]));
      const turnIdle: Record<string, { bucketKeys: string[]; idle: boolean; eas?: Set<EnemyAgg> }> = {};
      for (const s of res.steps) {
        const wk = waveKey(at.floor, s.wave);
        if (s.human) {
          const pa = (players[s.actor] ??= { actions: {}, dealt: 0, taken: 0, healed: 0, effectsApplied: {} });
          inc(pa.actions, actionName(s.actionId));
          pa.dealt += s.dealt;
          for (const e of s.effects) if (e.creator === s.actorUid) inc(pa.effectsApplied, e.type);
        } else {
          const tk = `${s.round}:${s.actorUid}`;
          for (const bucket of [enemies[wk] ?? {}, enemyAll]) {
            const ea = bucket[s.actor];
            if (!ea) continue;
            if (!seenTurn.has(tk)) ea.turns++;
            ea.totalActions++;
            ea.authoredRules = Math.max(ea.authoredRules, s.authoredRules);
            inc(ea.actions, actionName(s.actionId));
            if (IDLE.has(s.actionId as string)) ea.idleActions++;
            if (s.round - (waveStart.get(s.wave) ?? 1) >= 2) {
              // Per turn: a turn is idle when none of its actions is anything but move / end turn.
              const st = (turnIdle[tk] ??= { bucketKeys: [], idle: true });
              if (!IDLE.has(s.actionId as string)) st.idle = false;
              if (!st.bucketKeys.includes(bucket === enemyAll ? "all" : wk)) {
                st.bucketKeys.push(bucket === enemyAll ? "all" : wk);
                ea.actionsAfterR2++;
              }
              (st.eas ??= new Set()).add(ea);
            }
            const rk = s.ruleIndex === null ? "none" : s.ruleIndex < s.authoredRules ? String(s.ruleIndex) : "engine-fallback";
            inc(ea.ruleFires, rk);
            ea.dealt += s.dealt;
            for (const e of s.effects) if (e.creator === s.actorUid) inc(ea.effectsApplied, e.type);
          }
          seenTurn.add(tk);
        }
        // damage taken / healing per unit
        for (const [uid, d] of Object.entries(s.hp)) {
          const isPlayer = uid.startsWith("user_");
          if (isPlayer) {
            const pa = (players[uid] ??= { actions: {}, dealt: 0, taken: 0, healed: 0, effectsApplied: {} });
            if (d < 0) pa.taken -= d;
            else pa.healed += d;
          } else {
            const wv = uidToWave.get(uid);
            const aiId = res.waves.flatMap((w) => w.enemies).find((e) => e.uid === uid)?.aiId;
            if (wv === undefined || !aiId) continue;
            for (const bucket of [enemies[waveKey(at.floor, wv)] ?? {}, enemyAll]) {
              const ea = bucket[aiId];
              if (!ea) continue;
              if (d < 0) ea.taken -= d;
              else ea.healed += d;
            }
          }
        }
      }
      for (const st of Object.values(turnIdle)) if (st.idle) for (const ea of st.eas ?? []) ea.idleAfterR2++;
      // Per-appearance rule fire distribution (authored rules only).
      const firesByUid: Record<string, Record<string, number>> = {};
      let authoredOf: Record<string, number> = {};
      for (const st of res.steps) {
        if (st.human) continue;
        authoredOf[st.actorUid] = Math.max(authoredOf[st.actorUid] ?? 0, st.authoredRules);
        if (st.ruleIndex !== null && st.ruleIndex < st.authoredRules) inc((firesByUid[st.actorUid] ??= {}), String(st.ruleIndex));
      }
      for (const w of res.waves)
        for (const e of w.enemies) {
          const n = authoredOf[e.uid] ?? 0;
          for (const bucket of [enemies[waveKey(at.floor, w.wave)] ?? {}, enemyAll]) {
            const ea = bucket[e.aiId];
            if (!ea) continue;
            ea.ruleFireDist ??= {};
            if ((signatures[e.aiId] ?? []).some((i) => (firesByUid[e.uid]?.[String(i)] ?? 0) > 0)) ea.signatureFired++;
            for (let i = 0; i < n; i++) {
              const c = firesByUid[e.uid]?.[String(i)] ?? 0;
              const d = (ea.ruleFireDist[String(i)] ??= { never: 0, once: 0, more: 0 });
              if (c === 0) d.never++;
              else if (c === 1) d.once++;
              else d.more++;
            }
          }
        }
      for (const [uid, p] of Object.entries(res.players)) {
        const pa = (players[uid] ??= { actions: {}, dealt: 0, taken: 0, healed: 0, effectsApplied: {} });
        (pa.lowestHpPct ??= []).push((100 * Math.max(0, p.minHealth)) / p.maxHealth);
        pa.downs = (pa.downs ?? 0) + p.downs;
      }
    }
  }
  // finalise
  const enemyView = (e: EnemyAgg) => {
    const authored = [...Array(e.authoredRules).keys()].map(String);
    return {
      name: e.name, aiId: e.aiId, appearances: e.appearances, killedPct: r1((100 * e.deaths) / e.appearances),
      diedAfterRoundsMedian: median(e.diedAfterRounds), turnsPerAppearance: r1(e.turns / e.appearances),
      dealtPerAppearance: Math.round(e.dealt / e.appearances), takenPerAppearance: Math.round(e.taken / e.appearances),
      healedPerAppearance: Math.round(e.healed / e.appearances),
      idleOrMovePct: r1((100 * e.idleActions) / Math.max(1, e.totalActions)),
      idleTurnsAfterRound2Pct: r1((100 * e.idleAfterR2) / Math.max(1, e.actionsAfterR2)),
      signatureRules: signatures[e.aiId] ?? null,
      signatureFiredPct: signatures[e.aiId] ? r1((100 * e.signatureFired) / e.appearances) : null,
      actions: Object.fromEntries(Object.entries(e.actions).sort((a, b) => b[1] - a[1])),
      ruleFires: e.ruleFires, rulesNeverFired: authored.filter((i) => !e.ruleFires[i]), ruleFireDist: e.ruleFireDist ?? {},
      effectsApplied: e.effectsApplied,
    };
  };
  const waveTable = Object.entries(waves).map(([k, w]) => {
    const threats = Object.values(enemies[k] ?? {}).sort((a, b) => b.dealt - a.dealt);
    const totalDealt = threats.reduce((s, e) => s + e.dealt, 0) || 1;
    return {
      wave: k, enemies: w.enemies.join(" + "), attempts: w.attempts, cleared: w.cleared, wipedHere: w.wipedHere,
      roundsMedian: median(w.rounds), roundsMin: w.rounds.length ? Math.min(...w.rounds) : null,
      roundsMax: w.rounds.length ? Math.max(...w.rounds) : null, roundsP90: pct(w.rounds, 0.9),
      humanTurnsMedian: median(w.humanTurns), aiTurnsMedian: median(w.aiTurns),
      partyHpLostPctMedian: r1(median(w.hpLostPct)),
      poolsLeftMedianPct: { hp: r1((median(w.poolsEnd.hp) ?? 0) * 100), cp: r1((median(w.poolsEnd.cp) ?? 0) * 100), sp: r1((median(w.poolsEnd.sp) ?? 0) * 100), playersAlive: median(w.poolsEnd.alive) },
      threats: threats.map((e) => ({ name: e.name, dealtPerAppearance: Math.round(e.dealt / e.appearances), sharePct: r1((100 * e.dealt) / totalDealt) })),
    };
  });
  const waveTable2 = waveTable.map((w) => ({ ...w, enemyBehaviour: Object.values(enemies[w.wave] ?? {}).map(enemyView) }));
  const playerView = Object.fromEntries(Object.entries(players).map(([k, p]) => [k, {
    actions: Object.fromEntries(Object.entries(p.actions as Record<string, number>).sort((a, b) => b[1] - a[1])),
    dealtPerRun: Math.round(p.dealt / results.length), takenPerRun: Math.round(p.taken / results.length),
    healedPerRun: Math.round(p.healed / results.length), lowestHpPctMedianPerFloor: r1(median(p.lowestHpPct ?? [])),
    downsPerRun: r1((p.downs ?? 0) / results.length), effectsApplied: p.effectsApplied,
  }]));
  // time model
  const timeFor = (run: (typeof results)[number], pace: number, ai: number) => {
    let s = 0;
    for (const a of run.attempts) s += a.res.humanTurns * pace + a.res.aiTurns * ai + TRANSITION_SECONDS;
    return s;
  };
  const time: Record<string, any> = {};
  for (const pace of PACES)
    for (const ai of AI_SECONDS) {
      const ts = results.map((r) => timeFor(r, pace, ai));
      const clearedTs = results.filter((r) => r.status === "cleared").map((r) => timeFor(r, pace, ai));
      time[`player${pace}s_ai${ai}s`] = {
        minutesMedianAllRuns: r1((median(ts) ?? 0) / 60), minutesP10: r1((pct(ts, 0.1) ?? 0) / 60), minutesP90: r1((pct(ts, 0.9) ?? 0) / 60),
        minutesMedianClearedRuns: clearedTs.length ? r1((median(clearedTs) ?? 0) / 60) : null,
        clearedWithinLimitPct: r1((100 * results.filter((r) => r.status === "cleared" && timeFor(r, pace, ai) <= LIMIT).length) / results.length),
      };
    }
  const totalRounds = results.map((r) => r.attempts.reduce((s, a) => s + a.res.rounds, 0));
  const dodge = { threatened: 0, dodged: 0, failedRooted: 0, failedNoPath: 0, failedOther: 0, stepsTaken: 0 } as Record<string, number>;
  for (const r of results) for (const a of r.attempts) for (const [k, n] of Object.entries(a.res.dodge ?? {})) dodge[k] = (dodge[k] ?? 0) + (n as number);
  const dodgeView = { enabled: dodgeOn, ...dodge, dodgedPct: dodge.threatened ? r1((100 * dodge.dodged!) / dodge.threatened) : null };
  const cleanRuns = results.filter((r) => r.status === "cleared" && r.wipes === 0);
  return {
    variant: v.name, note: v.note, player: describePlayer(playerQueryUser(0, v, donor, T.jutsu)),
    runs: results.length,
    outcomes: Object.fromEntries(["cleared", "max-wipes", "ended", "stalled"].map((s) => [s, results.filter((r) => r.status === s).length])),
    runsWithAWipePct: r1((100 * results.filter((r) => r.wipes > 0).length) / results.length),
    wipesPerRunMedian: median(results.map((r) => r.wipes)),
    totalRoundsMedian: median(totalRounds), totalRoundsP10: pct(totalRounds, 0.1), totalRoundsP90: pct(totalRounds, 0.9),
    totalRoundsCleanClearMedian: median(cleanRuns.map((r) => r.attempts.reduce((s, a) => s + a.res.rounds, 0))),
    time,
    dodge: dodgeView,
    floors: Object.fromEntries(Object.entries(floorsAgg).map(([k, f]) => [k, { attempts: f.attempts, won: f.won, wipes: f.wipes, roundsMedian: median(f.rounds), humanTurnsMedian: median(f.humanTurns), aiTurnsMedian: median(f.aiTurns) }])),
    waves: waveTable2,
    enemiesOverall: Object.values(enemyAll).map(enemyView),
    players: playerView,
    runStatus: results.map((r) => ({ seed: r.seed, status: r.status, wipes: r.wipes, floorsAttempted: r.attempts.map((a) => `F${floorLabel(a.floor) + 1}:${a.res.outcome}:${a.res.rounds}`) })),
  };
};

/* ---------------- main ---------------- */
if (flag("probe-check")) {
  // The observation hook must not change outcomes: compare runs with the hook live vs. removed.
  const v = variants[0]!;
  for (const s of [seed0, seed0 + 1]) {
    const a = await runDungeon(v, s, true);
    const a2 = await runDungeon(v, s, true);
    const g = globalThis as any;
    const saved = g.__TNR_RULE_PROBE__;
    // Run with the hook permanently undefined by shadowing assignment.
    Object.defineProperty(g, "__TNR_RULE_PROBE__", { configurable: true, get: () => undefined, set: () => {} });
    const b = await runDungeon(v, s, false);
    delete g.__TNR_RULE_PROBE__;
    g.__TNR_RULE_PROBE__ = saved;
    const sig = (r: typeof a) => JSON.stringify(r.attempts.map((x) => [x.floor, x.res.outcome, x.res.rounds, x.res.steps.map((st) => [st.actor, st.actionId, st.ruleIndex === null ? 0 : 1, Object.values(st.hp).map((h) => Math.round(h)).sort((p, q) => p - q)])]));
    if (sig(a) !== sig(a2)) throw new Error(`determinism FAILED for seed ${s}: same seed, different outcome`);
    // With the hook removed ruleIndex is null everywhere; compare everything else.
    const sigNoRule = (r: typeof a) => sig(r).replace(/,[01],\[/g, ",[");
    if (sigNoRule(a) !== sigNoRule(b)) throw new Error(`probe-check FAILED for seed ${s}`);
    console.log(`probe-check seed ${s}: identical (${a.attempts.length} floor battles)`);
  }
  process.exit(0);
}

const out: any = {
  generatedBy: "harness/skyglass_wreck_sim/engine/main.ts",
  override: ovPath ? { path: ovPath, name: override.name, note: override.note } : null,
  settings: { dodge: dodgeOn, dmgConfig: dmg.name, dmgConfigValues: dmg.config ?? null, runs, seed0, maxWipes, maxRounds, initialBarriers: barriers, paces: PACES, aiSecondsPerTurn: AI_SECONDS, transitionSecondsPerFloorBattle: TRANSITION_SECONDS, limitSeconds: LIMIT },
  enemyNotes: Object.fromEntries(Object.entries(T.enemies).filter(([, e]) => e.notes.length).map(([id, e]) => [e.row.username ?? id, e.notes])),
  layout: floors.map((f, i) => ({ floor: floorLabel(i) + 1, kind: f.kind, waves: f.waves.map((w) => w.aiIds.map((id) => T.enemies[id]!.row.username)) })),
  variants: [] as any[],
};
const t0 = Date.now();
for (const v of variants) {
  const results = [];
  for (let i = 0; i < runs; i++) results.push(await runDungeon(v, seed0 + i));
  const s = summarise(v, results);
  out.variants.push(s);
  console.log(`\n=== ${v.name}: ${JSON.stringify(s.outcomes)} wipesRun%=${s.runsWithAWipePct} totalRounds med=${s.totalRoundsMedian} [${s.totalRoundsP10}-${s.totalRoundsP90}] (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
  for (const w of s.waves)
    console.log(`${w.wave.padEnd(6)} ${String(w.roundsMedian).padStart(5)} [${w.roundsMin}-${w.roundsMax}] clr ${w.cleared}/${w.attempts} wipe ${w.wipedHere} hpLost ${w.partyHpLostPctMedian}% left hp ${w.poolsLeftMedianPct.hp}% | ${w.enemies}`);
  console.log("time:", JSON.stringify(s.time));
  console.log("dodge:", JSON.stringify(s.dodge));
  for (const e of s.enemiesOverall)
    console.log(`  ${e.name.padEnd(18)} app ${String(e.appearances).padStart(3)} sig ${String(e.signatureFiredPct).padStart(5)}% idle>r2 ${String(e.idleTurnsAfterRound2Pct).padStart(5)}% dealt ${e.dealtPerAppearance} never ${e.rulesNeverFired.join(",")}`);
}
const outPath = opt("out");
if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(resolve(outPath), `${JSON.stringify(out, null, 1)}\n`);
  console.log(`wrote ${outPath}`);
}
