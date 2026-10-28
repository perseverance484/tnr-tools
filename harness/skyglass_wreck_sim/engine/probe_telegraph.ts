/**
 * Telegraphed-boss probes (offline, engine-executed). Each scenario is one plain QUEST battle:
 * one "average" player who only ends its turn, vs one stationary probe boss (Deck Warden row,
 * kit = the scenario's jutsu, includeDefaultRules false, rule list ending in end_turn). Positions
 * are set after assembly so geometry is controlled; initial barriers are off.
 *
 *   TNR_SCRIPT=probe_telegraph.ts run.sh [--only T1,T2] [--out results/probe_telegraph.json]
 *
 * Synthetic jutsu are built on the captured Drowning Mire record (shape donor: GROUND,
 * AOE_CIRCLE_SPAWN) with only the fields named per scenario changed. Summon probes (T5) use the
 * push/272 Crownhold Proving Proctor (manifest data + the live stat readback in its results bundle)
 * with jutsu records taken from captures.
 */
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { Grid, rectangle } from "honeycomb-grid";
import { getBattleSpawnLocations } from "@/libs/combat/participants";
import { getDefaultBattleSizes } from "@/libs/combat/util";
import { TerrainHex } from "@/libs/hexgrid";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, PLAYER_VARIANTS, playerQueryUser, queryShell } from "./model";
import { assembleFloor, mulberry32, runFloor } from "./sim";

const args = process.argv.slice(2);
const opt = (k: string, d?: string) => {
  const i = args.indexOf(`--${k}`);
  return i >= 0 ? args[i + 1] : d;
};
const H = process.env.TNR_HARNESS!;
const REPO = process.env.TNR_REPO!;
const only = opt("only")?.split(",");

/* ---------- captured records ---------- */
const harvestFiles = readdirSync(join(REPO, "harvests/inbox")).filter((f) => f.endsWith(".json")).map((f) => `harvests/inbox/${f}`);
const cacheDocs = new Map<string, any>();
const doc = (f: string) => {
  if (!cacheDocs.has(f)) cacheDocs.set(f, JSON.parse(readFileSync(join(REPO, f), "utf8")));
  return cacheDocs.get(f);
};
const findRecord = (id: string, files: string[]) => {
  let best: any = null;
  let src = "";
  const walk = (x: any, f: string) => {
    if (Array.isArray(x)) x.forEach((v) => walk(v, f));
    else if (x && typeof x === "object") {
      if (x.id === id && "jutsuType" in x && "effects" in x && (!best || (x.updatedAt ?? "") > (best.updatedAt ?? ""))) {
        best = x;
        src = f;
      }
      Object.values(x).forEach((v) => walk(v, f));
    }
  };
  for (const f of files) walk(doc(f), f);
  if (!best) throw new Error(`jutsu ${id} not captured`);
  return { record: structuredClone(best), source: src };
};
const DONOR = findRecord("VmZzkyfPswbJLXvuB-mcV", ["harvests/inbox/tnr_results_1792732003454.json"]);
const dmgFx = DONOR.record.effects.find((e: any) => e.type === "damage");
const visFx = DONOR.record.effects.find((e: any) => e.type === "visual");
const pctFx = DONOR.record.effects.find((e: any) => e.type === "increasedamagetaken");

const fx = {
  visual: (rounds: number) => ({ ...structuredClone(visFx), rounds, staticAnimation: "harness-telegraph-mark" }),
  damage: (power: number) => ({ ...structuredClone(dmgFx), power, powerPerLevel: 0, rounds: 0, elements: ["None"], friendlyFire: "ENEMIES" }),
  pct: (type: string, power: number, rounds: number, target = "INHERIT") => ({ ...structuredClone(pctFx), type, power, powerPerLevel: 0, rounds, target }),
};
let seq = 0;
const jutsu = (name: string, over: Record<string, unknown>) => ({
  ...structuredClone(DONOR.record),
  id: `harness-tele-${++seq}`, name, elementClassification: "None", battleUsageType: "BOTH",
  cooldown: 0, actionCostPerc: 40, chakraCost: 0, staminaCost: 0, healthCost: 0,
  coordinateTargeting: null, methodSize: null, ...over,
});

/* ---------- geometry ---------- */
const size = getDefaultBattleSizes("QUEST" as never, 100)!;
const grid = new Grid(TerrainHex, rectangle({ width: size.width, height: size.height }));
const hexAt = (x: number, y: number) => grid.getHex({ col: x, row: y })!;
/** Column/row offsets of the hexes at exact hex distance r from (cx, cy). */
const ringOffsets = (cx: number, cy: number, r: number) =>
  grid.toArray().filter((h) => grid.distance(h, hexAt(cx, cy)) === r).map((h) => ({ longitude: h.col - cx, latitude: h.row - cy }));
const hexDist = (a: [number, number], b: [number, number]) => grid.distance(hexAt(a[0], a[1]), hexAt(b[0], b[1]));

/* ---------- Crownhold Proctor row (push/272 + live readback) ---------- */
const proctorRow = (baseRow: any, jutsuCatalog: Record<string, any>) => {
  const m = doc("archive/spent-manifests/push-2026-10-25/272_crownhold_ais.json");
  const item = m.items.find((i: any) => i.name === "Crownhold Proving Proctor");
  const res = doc("harvests/inbox/tnr_results_1792984876132.json").entries.find((e: any) => e.name === "Crownhold Proving Proctor");
  const id = res.id as string;
  const live: Record<string, number> = {};
  for (const f of res.asserted?.fail ?? []) {
    const mm = /live ([\d.]+)/.exec(f.d?.[0] ?? "");
    if (mm) live[f.k] = Number(mm[1]);
  }
  const d = item.data;
  const row = {
    ...structuredClone(baseRow), userId: id, username: d.username, level: d.level, rank: d.rank,
    poolsMultiplier: d.poolsMultiplier, statsMultiplier: d.statsMultiplier,
    maxHealth: 5050 * d.poolsMultiplier, curHealth: 5050 * d.poolsMultiplier,
    offence: live.offence ?? d.offence, defence: live.defence ?? d.defence, strength: live.strength ?? d.strength,
    intelligence: live.intelligence ?? d.intelligence, willpower: live.willpower ?? d.willpower, speed: live.speed ?? d.speed,
    effects: d.effects, items: [], aiProfileId: `profile-${id}`,
    jutsus: d.jutsus.map((jid: string, i: number) => ({
      id: `proctor-${i}`, userId: id, jutsuId: jid, level: 1, experience: 0, equipped: true, finishTraining: null,
      reskinId: null, activeReskin: null, jutsu: jutsuCatalog[jid] ?? findRecord(jid, harvestFiles).record,
    })),
  };
  const profile = { id: `profile-${id}`, userId: id, name: d.username, includeDefaultRules: d.includeDefaultRules, rules: d.rules };
  return { id, row: { ...row, ...queryShell(profile) }, rules: d.rules.length, statsFromReadback: Object.keys(live).length > 0 };
};

/* ---------- scenarios ---------- */
type Sc = {
  key: string; question: string; kit: any[]; rules: any[]; boss: [number, number]; player: [number, number];
  rounds: number; summonRows?: boolean;
};
const end = { conditions: [], action: { type: "end_turn", description: "" } };
const cast = (j: any, target: string, conditions: any[] = []) => ({ conditions, action: { type: "use_specific_jutsu", jutsuId: j.id, target, description: "" } });
const hasMarker = (type: string) => ({ type: "has_effect", effectType: type, threshold: 1, description: "" });

const T1a = jutsu("Telegraph: visual only", { target: "GROUND", method: "AOE_CIRCLE_SPAWN", range: 5, effects: [fx.visual(2)] });
const T1b = jutsu("Telegraph: visual + zero-impact increasepoolcost 1", { target: "GROUND", method: "AOE_CIRCLE_SPAWN", range: 5, effects: [fx.visual(2), fx.pct("increasepoolcost", 1, 2)] });
const T1c = jutsu("Telegraph: increasepoolcost 0 only", { target: "GROUND", method: "AOE_CIRCLE_SPAWN", range: 5, effects: [fx.pct("increasepoolcost", 0, 2)] });
// Marker note: decreasepoolcost is stored with a negative power (-1), so has_effect (sum >= threshold)
// never matches it; the self marker used below is increasepoolcost 1 (positive, ~1% pool cost).
const MARKER = "increasepoolcost";
const mk2 = (markerRounds: number) => ({
  tele: jutsu(`Telegraph + self marker r${markerRounds}`, { target: "GROUND", method: "AOE_CIRCLE_SPAWN", range: 5, cooldown: 3, actionCostPerc: 100, effects: [fx.visual(2), fx.pct(MARKER, 1, markerRounds, "SELF")] }),
  det: jutsu("Detonation (damage 60)", { target: "GROUND", method: "AOE_CIRCLE_SPAWN", range: 5, cooldown: 3, actionCostPerc: 100, effects: [fx.damage(60)] }),
});
const T2r1 = mk2(1);
const T2dec = { tele: jutsu("Telegraph + self marker decreasepoolcost r1", { target: "GROUND", method: "AOE_CIRCLE_SPAWN", range: 5, cooldown: 3, effects: [fx.visual(2), fx.pct("decreasepoolcost", 1, 1, "SELF")] }) };
const T2r2 = mk2(2);
const BOSS_EVEN: [number, number] = [6, 5];
const BOSS_ODD: [number, number] = [7, 5];
const ring2 = ringOffsets(BOSS_EVEN[0], BOSS_EVEN[1], 2);
const coordJ = (name: string, origin: string, selection: string, coords: any[], effects: any[], range: number) =>
  jutsu(name, { target: "GROUND", method: "COORDINATES", range, cooldown: 3, actionCostPerc: 100, coordinateTargeting: { origin, selection, coordinates: coords, randomCount: 1 }, effects });
const ringTele = (range: number) => coordJ(`Ring telegraph r${range}`, "CASTER", "ALL", ring2, [fx.visual(2), fx.pct(MARKER, 1, 1, "SELF")], range);
const ringDet = (range: number) => coordJ(`Ring detonation r${range}`, "CASTER", "ALL", ring2, [fx.damage(60)], range);
const SAFE = [{ longitude: 2, latitude: 2 }, { longitude: 2, latitude: 3 }, { longitude: 3, latitude: 2 }];
const excl = coordJ("Battlefield EXCLUDE 3 safe tiles", "BATTLEFIELD", "EXCLUDE", SAFE, [fx.damage(60)], 0);

const S: Sc[] = [
  { key: "T1a", question: "GROUND jutsu with only a visual tag (rounds 2): persistent ground mark? touches units? hurts caster?", kit: [T1a], rules: [cast(T1a, "CLOSEST_OPPONENT"), end], boss: BOSS_EVEN, player: [4, 5], rounds: 4 },
  { key: "T1b", question: "visual + zero-impact increasepoolcost 1 (rounds 2), cast on the player", kit: [T1b], rules: [cast(T1b, "CLOSEST_OPPONENT"), end], boss: BOSS_EVEN, player: [4, 5], rounds: 4 },
  { key: "T1c", question: "increasepoolcost power 0 only (rounds 2), cast on the player", kit: [T1c], rules: [cast(T1c, "CLOSEST_OPPONENT"), end], boss: BOSS_EVEN, player: [4, 5], rounds: 4 },
  { key: "T2dec", question: "control: SELF marker decreasepoolcost 1 (stored as -1) for 1 round; top rule has_effect decreasepoolcost >= 1 -> detonation", kit: [T2dec.tele, T2r1.det], rules: [cast(T2r1.det, "CLOSEST_OPPONENT", [hasMarker("decreasepoolcost")]), cast(T2dec.tele, "CLOSEST_OPPONENT"), end], boss: BOSS_EVEN, player: [4, 5], rounds: 6 },
  { key: "T2r1", question: "telegraph applies SELF marker increasepoolcost 1 for 1 round; top rule has_effect marker -> detonation", kit: [T2r1.tele, T2r1.det], rules: [cast(T2r1.det, "CLOSEST_OPPONENT", [hasMarker(MARKER)]), cast(T2r1.tele, "CLOSEST_OPPONENT"), end], boss: BOSS_EVEN, player: [4, 5], rounds: 6 },
  { key: "T2r2", question: "same with the marker lasting 2 rounds", kit: [T2r2.tele, T2r2.det], rules: [cast(T2r2.det, "CLOSEST_OPPONENT", [hasMarker(MARKER)]), cast(T2r2.tele, "CLOSEST_OPPONENT"), end], boss: BOSS_EVEN, player: [4, 5], rounds: 6 },
  ...([["SELF", 0], ["SELF", 5], ["CLOSEST_OPPONENT", 0], ["CLOSEST_OPPONENT", 5]] as const).map(([tgt, rng]) => {
    const tele = ringTele(rng);
    const det = ringDet(rng);
    return { key: `T3ring_${tgt}_r${rng}`, question: `COORDINATES CASTER/ALL radius-2 ring (offsets from an even column), rule target ${tgt}, jutsu range ${rng}; telegraph -> marker -> detonation`, kit: [tele, det], rules: [cast(det, tgt, [hasMarker(MARKER)]), cast(tele, tgt), end], boss: BOSS_EVEN, player: [BOSS_EVEN[0] + 2, BOSS_EVEN[1]] as [number, number], rounds: 5 };
  }),
  { key: "T3ring_odd", question: "same ring offsets with the caster on an odd column (offsets are column/row, not hex)", kit: [ringTele(5), ringDet(5)], rules: [], boss: BOSS_ODD, player: [BOSS_ODD[0] + 2, BOSS_ODD[1]], rounds: 5 },
  { key: "T3excl_unsafe", question: "BATTLEFIELD/EXCLUDE 3 safe tiles, player on an unsafe tile; is the caster hit?", kit: [excl], rules: [cast(excl, "SELF"), end], boss: BOSS_EVEN, player: [4, 5], rounds: 2 },
  { key: "T3excl_safe", question: "BATTLEFIELD/EXCLUDE 3 safe tiles, player on a safe tile (2,2)", kit: [excl], rules: [cast(excl, "SELF"), end], boss: BOSS_EVEN, player: [2, 2], rounds: 2 },
];
// The odd-column ring reuses the even-column offsets; rules reference its own two jutsu.
{
  const sc = S.find((s) => s.key === "T3ring_odd")!;
  sc.rules = [cast(sc.kit[1], "SELF", [hasMarker(MARKER)]), cast(sc.kit[0], "SELF"), end];
}

const baseline = loadJson(join(H, "data/baseline.json"));
const dmg = loadDmgConfig(H, "live");
const out: any = { generatedBy: "engine/probe_telegraph.ts", donor: `Drowning Mire (${DONOR.record.id}) from ${DONOR.source}`, dmgConfig: dmg.name, probes: [] as any[] };

const runScenario = async (sc: Sc, extra?: { rows: Record<string, any> }) => {
  const ov: any = {
    jutsu: Object.fromEntries(sc.kit.map((j) => [j.id, j])),
    newEnemies: { boss: { base: "Deck Warden", username: `Boss ${sc.key}`, jutsuIds: sc.kit.map((j) => j.id), rules: sc.rules, includeDefaultRules: false, effects: [] } },
  };
  const t = buildTemplates(baseline, ov);
  const rows: Record<string, any> = { ...Object.fromEntries(Object.entries(t.enemies).map(([id, e]) => [id, enemyQueryUser(e)])), ...(extra?.rows ?? {}) };
  const v = { ...PLAYER_VARIANTS.average!, rules: [end] };
  const donor = t.enemies["texZaFi42S3EvJZBwQ8cd"]!.row;
  const rand = mulberry32(1);
  const orig = Math.random;
  Math.random = rand;
  try {
    const player = playerQueryUser(0, v as never, donor, t.jutsu);
    const b = await assembleFloor({ players: [player], enemyRows: rows, floor: { kind: "floor", waves: [{ aiIds: ["boss"], delayRounds: 0 }] }, rand, initialBarriers: false, dmgConfig: dmg.config, mode: "quest" });
    const pu = b.usersState.find((u) => u.userId === player.userId)!;
    const bu = b.usersState.find((u) => u.controllerId === "boss")!;
    [pu.longitude, pu.latitude] = sc.player;
    [bu.longitude, bu.latitude] = sc.boss;
    const res = runFloor(b, { playerIds: [player.userId], maxRounds: sc.rounds, detail: true });
    const nameOf = (uid: string) => (uid === player.userId ? "player" : uid === bu.userId ? "boss" : `unit:${uid.slice(0, 5)}`);
    const steps = res.steps.map((s) => ({
      round: s.round, actor: nameOf(s.actorUid), action: (sc.kit.find((j) => j.id === s.actionId)?.name ?? s.actionId), rule: s.ruleIndex,
      actorEffects: s.actorEffects?.map((e) => `${e.type}:${e.power}:r${e.rounds}`),
      hp: Object.fromEntries(Object.entries(s.hp).map(([k, d]) => [nameOf(k), Math.round(d)])),
      newGround: s.ground.map((g) => `${g.type}@${g.x},${g.y}:r${g.rounds}`),
      newUserEffects: s.effects.map((e) => `${e.type}->${nameOf(e.target)}`),
      newUnits: s.newUnits?.map((n) => ({ name: n.name, at: [n.x, n.y], hp: n.hp, isSummon: n.isSummon })),
      groundAfter: (s.groundAfter ?? []).map((g) => `${g.type}@${g.x},${g.y}:r${g.rounds}${g.staticAnimation ? ":anim" : ""}`),
    }));
    return { key: sc.key, question: sc.question, positions: { boss: sc.boss, player: sc.player, hexDistance: hexDist(sc.boss, sc.player) }, outcome: res.outcome, rounds: res.rounds, kit: sc.kit.map((j) => ({ id: j.id, name: j.name, target: j.target, method: j.method, range: j.range, cooldown: j.cooldown, coordinateTargeting: j.coordinateTargeting, effects: j.effects.map((e: any) => ({ type: e.type, power: e.power, rounds: e.rounds, target: e.target, aiId: e.aiId, aiHp: e.aiHp })) })), steps };
  } finally {
    Math.random = orig;
  }
};

for (const sc of S) {
  if (only && !only.includes(sc.key)) continue;
  const r = await runScenario(sc);
  out.probes.push(r);
  console.log(`\n### ${sc.key}: ${sc.question}\n  boss ${JSON.stringify(sc.boss)} player ${JSON.stringify(sc.player)} (hex distance ${r.positions.hexDistance}) -> ${r.outcome} after ${r.rounds}`);
  for (const s of r.steps)
    if (s.action !== "wait" || Object.keys(s.hp).length || s.newGround.length)
      console.log(`  r${s.round} ${s.actor.padEnd(7)} ${String(s.action).padEnd(34)} rule ${s.rule} actorFx ${JSON.stringify(s.actorEffects)} hp ${JSON.stringify(s.hp)} newGround ${s.newGround.length ? s.newGround.join(" ") : "-"} userFx ${s.newUserEffects.join(",") || "-"}`);
}

/* T4: grid and wave spawn cells (engine functions). */
if (!only || only.includes("T4")) {
  const right = getBattleSpawnLocations(size.width, size.height, "right");
  const left = getBattleSpawnLocations(size.width, size.height, "left");
  out.grid = { battleType: "QUEST", levelAtLeast50: size, playerSpawnCells: left, enemySpawnCells: right };
  console.log(`\n### T4 grid ${size.width}x${size.height}; player (left) spawn cells ${left.length}: ${JSON.stringify(left)}\n  enemy (right) spawn cells ${right.length}: ${JSON.stringify(right)}`);
}

/* T5: summon an existing AI record (Crownhold Proving Proctor). */
if (!only || only.includes("T5")) {
  const t0 = buildTemplates(baseline, {});
  const donorRow = enemyQueryUser(t0.enemies["texZaFi42S3EvJZBwQ8cd"]!);
  const pr = proctorRow(donorRow, t0.jutsu);
  const hellHound = findRecord("kP_KMs7H9wQJwRHeaTGCZ", ["harvests/inbox/tnr_results_1792732003454.json"]).record;
  const sumFx = hellHound.effects.find((e: any) => e.type === "summon");
  const s1 = { ...structuredClone(hellHound), id: "harness-summon-one", name: "Recall one Proctor", cooldown: 3, effects: [{ ...structuredClone(sumFx), aiId: pr.id, aiHp: 6000, power: 100, powerPerLevel: 0, rounds: 3 }] };
  const s2 = { ...structuredClone(hellHound), id: "harness-summon-two", name: "Recall two Proctors (two summon tags)", cooldown: 3, effects: [{ ...structuredClone(sumFx), aiId: pr.id, aiHp: 6000, power: 100, powerPerLevel: 0, rounds: 3 }, { ...structuredClone(sumFx), aiId: pr.id, aiHp: 6000, power: 100, powerPerLevel: 0, rounds: 3 }] };
  for (const [key, j, rules] of [
    ["T5one", s1, [cast(s1, "EMPTY_GROUND_CLOSEST_TO_OPPONENT"), end]],
    ["T5two_tags", s2, [cast(s2, "EMPTY_GROUND_CLOSEST_TO_OPPONENT"), end]],
    ["T5recast", { ...s1, cooldown: 0 }, [cast({ ...s1, cooldown: 0 }, "EMPTY_GROUND_CLOSEST_TO_OPPONENT"), end]],
  ] as const) {
    const sc: Sc = { key, question: `summon the Crownhold Proving Proctor (${pr.id}): ${j.name}${key === "T5recast" ? " with cooldown 0 (recast while the first lives)" : ""}`, kit: [j], rules: rules as any[], boss: BOSS_EVEN, player: [3, 5], rounds: 5 };
    const r = await runScenario(sc, { rows: { [pr.id]: pr.row } });
    (r as any).proctor = { id: pr.id, rules: pr.rules, statsFromLiveReadback: pr.statsFromReadback };
    out.probes.push(r);
    console.log(`\n### ${key}: ${sc.question} -> ${r.outcome} after ${r.rounds}`);
    for (const s of r.steps)
      if (s.action !== "wait" || Object.keys(s.hp).length || s.newUnits?.length)
        console.log(`  r${s.round} ${s.actor.padEnd(10)} ${String(s.action).slice(0, 30).padEnd(30)} rule ${s.rule} hp ${JSON.stringify(s.hp)} ${s.newUnits?.length ? `NEW ${JSON.stringify(s.newUnits)}` : ""} summonsOnField ${s.groundAfter.filter((g) => g.startsWith("summon")).join(" ") || "-"}`);
  }
}

const outPath = opt("out");
if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(resolve(outPath), `${JSON.stringify(out, null, 1)}\n`);
  console.log(`wrote ${outPath}`);
}
