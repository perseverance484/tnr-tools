/**
 * Boss-fight mechanic probes (SKYGLASS_BOSS_FIGHTS.md open questions; offline, engine-executed).
 * Each scenario is one plain QUEST battle: "average" player(s) vs one probe boss (Deck Warden row,
 * kit = the scenario's jutsu built with kitlib and validated by the live JutsuValidator / AiRule).
 *
 *   TNR_SCRIPT=probe_boss.ts run.sh [--only Q1,Q2] [--out results/probe_boss.json]
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, PLAYER_VARIANTS, playerQueryUser } from "./model";
import { assembleFloor, mulberry32, runFloor } from "./sim";
import { cast, cond, endTurn, jutsu, T, tag } from "./kitlib";

const args = process.argv.slice(2);
const opt = (k: string) => {
  const i = args.indexOf(`--${k}`);
  return i >= 0 ? args[i + 1] : undefined;
};
const only = opt("only")?.split(",");
const H = process.env.TNR_HARNESS!;
const baseline = loadJson(join(H, "data/baseline.json"));
const dmg = loadDmgConfig(H, "live");

const ALL_STATS = ["None", "Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu"];
const ALL_GENERALS = ["Highest", "Strength", "Intelligence", "Willpower", "Speed"];
const weakness = (mod: number, rounds: number) => tag("weakness", { target: "SELF", rounds, dmgModifier: mod, statTypes: ALL_STATS, generalTypes: ALL_GENERALS, power: 100 });
const recover = () => T.beat();

const j = {
  teleA: jutsu("probe-teleA", { name: "Chain mark A", description: "probe", battleDescription: "probe", target: "GROUND", method: "AOE_SPIRAL_SHOOT", range: 2, cooldown: 4, actionCostPerc: 60, effects: [T.visual("tg_heavy", 2), T.marker(10)] }),
  followB: jutsu("probe-followB", { name: "Chain follow-up B (pull 3)", description: "probe", battleDescription: "probe", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 4, actionCostPerc: 40, effects: [T.pull(3), T.marker(20)] }),
  detB: jutsu("probe-detB", { name: "Chain detonation on B", description: "probe", battleDescription: "probe", target: "GROUND", method: "AOE_SPIRAL_SHOOT", range: 2, cooldown: 2, actionCostPerc: 100, effects: [T.damage(60), recover()] }),
  exposeAfter: jutsu("probe-expose1", { name: "Weakness after cleanse", description: "probe", battleDescription: "probe", target: "SELF", method: "SINGLE", range: 0, cooldown: 3, actionCostPerc: 100, effects: [T.cleanseSelf(), weakness(3, 1)] }),
  exposeOnly: jutsu("probe-expose2", { name: "Weakness only (x3, 1 round)", description: "probe", battleDescription: "probe", target: "SELF", method: "SINGLE", range: 0, cooldown: 3, actionCostPerc: 100, effects: [weakness(3, 1)] }),
  ringTele: jutsu("probe-ringT", { name: "Ring telegraph (spiral r2, SELF)", description: "probe", battleDescription: "probe", target: "GROUND", method: "AOE_SPIRAL_SHOOT", range: 2, cooldown: 3, actionCostPerc: 100, effects: [T.visual("tg_control", 2), T.marker(5)] }),
  bell: jutsu("probe-bell", { name: "Bell: push 3 + stun 1 (spiral r2)", description: "probe", battleDescription: "probe", target: "GROUND", method: "AOE_SPIRAL_SHOOT", range: 2, cooldown: 2, actionCostPerc: 100, effects: [T.damage(40), T.push(3), T.stun(1)] }),
  hookPullRoot: jutsu("probe-hook1", { name: "Chain Hook: pull 3 then root 1", description: "probe", battleDescription: "probe", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 3, actionCostPerc: 60, effects: [T.damage(45), T.pull(3), T.root(1)] }),
  hookRootPull: jutsu("probe-hook2", { name: "Chain Hook: root 1 then pull 3", description: "probe", battleDescription: "probe", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 3, actionCostPerc: 60, effects: [T.damage(45), T.root(1), T.pull(3)] }),
  bellChar: jutsu("probe-bellC", { name: "Bell CHARACTER: push 3 + stun 1", description: "probe", battleDescription: "probe", target: "CHARACTER", method: "AOE_SPIRAL_SHOOT", range: 2, cooldown: 2, actionCostPerc: 100, effects: [T.damage(40), T.push(3), T.stun(1)] }),
  bellOU: jutsu("probe-bellO", { name: "Bell OTHER_USER: push 3 + stun 1", description: "probe", battleDescription: "probe", target: "OTHER_USER", method: "AOE_SPIRAL_SHOOT", range: 2, cooldown: 2, actionCostPerc: 100, effects: [T.damage(40), T.push(3), T.stun(1)] }),
  mawGround: jutsu("probe-mawG", { name: "EXCLUDE GROUND damage + stun", description: "probe", battleDescription: "probe", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 2, actionCostPerc: 100, coordinateTargeting: { origin: "BATTLEFIELD", selection: "EXCLUDE", coordinates: [{ longitude: 2, latitude: 2 }], randomCount: 1 }, effects: [T.damage(40), T.stun(1)] }),
  mawChar: jutsu("probe-mawC", { name: "EXCLUDE CHARACTER damage + stun", description: "probe", battleDescription: "probe", target: "CHARACTER", method: "COORDINATES", range: 0, cooldown: 2, actionCostPerc: 100, coordinateTargeting: { origin: "BATTLEFIELD", selection: "EXCLUDE", coordinates: [{ longitude: 2, latitude: 2 }], randomCount: 1 }, effects: [T.damage(40), T.stun(1)] }),
  wall: jutsu("probe-wall", { name: "Gunwale wall", description: "probe", battleDescription: "probe", target: "EMPTY_GROUND", method: "AOE_LARGE_WALL_SHOOT", range: 3, cooldown: 99, actionCostPerc: 60, donor: "i4lGrYY5HNN2Q2GPToKUS", effects: [tag("barrier", { power: 100, rounds: 4, curHealth: 3000, maxHealth: 3000, absorbPercentage: 50, staticAnimation: "cp_gunwale" })] }),
};

type Sc = { walls?: [number, number][]; key: string; question: string; kit: any[]; rules: any[]; boss: [number, number]; players: [number, number][]; rounds: number; playerRules?: "end" | "kit"; dodge?: boolean };
const S: Sc[] = [
  { key: "Q1chain", question: "two-marker chain: 60 AP mark A (visual + marker 10), then in the same turn a 40 AP follow-up on has_effect>=10 that pulls 3 and applies marker B (20); next turn detonation on has_effect>=30 (A+B) which applies a 1-round beat marker (increaserange, no actions); then a plain beat on the recover marker",
    kit: [j.teleA, j.followB, j.detB], rules: [cast("det on B", j.detB.id, "SELF", [cond.marker(30)]), cast("follow-up on A", j.followB.id, "RANDOM_OPPONENT", [cond.marker(10)]), endTurn("recover beat", [cond.marker(1, "increaserange")]), cast("mark A", j.teleA.id, "SELF"), endTurn()],
    boss: [6, 5], players: [[2, 5]], rounds: 6, playerRules: "end" },
  { key: "Q1f_uncond", question: "control: the 40 AP follow-up cast unconditionally at CLOSEST_OPPONENT", kit: [j.followB], rules: [cast("follow", j.followB.id, "CLOSEST_OPPONENT"), endTurn()], boss: [6, 5], players: [[2, 5]], rounds: 2, playerRules: "end" },
  { key: "Q1f_closest", question: "chain with the follow-up at CLOSEST_OPPONENT",
    kit: [j.teleA, j.followB, j.detB], rules: [cast("det on B", j.detB.id, "SELF", [cond.marker(30)]), cast("follow-up on A", j.followB.id, "CLOSEST_OPPONENT", [cond.marker(10)]), endTurn("recover beat", [cond.marker(1, "increaserange")]), cast("mark A", j.teleA.id, "SELF"), endTurn()],
    boss: [6, 5], players: [[2, 5]], rounds: 6, playerRules: "end" },
  { key: "Q1dbg_t1", question: "debug: follow-up gated has_effect >= 1",
    kit: [j.teleA, j.followB], rules: [cast("follow-up on A", j.followB.id, "CLOSEST_OPPONENT", [cond.marker(1)]), cast("mark A", j.teleA.id, "SELF"), endTurn()],
    boss: [6, 5], players: [[2, 5]], rounds: 3, playerRules: "end" },
  { key: "Q1dbg_nocond", question: "debug: follow-up ungated listed after mark A",
    kit: [j.teleA, j.followB], rules: [cast("mark A", j.teleA.id, "SELF"), cast("follow-up", j.followB.id, "CLOSEST_OPPONENT"), endTurn()],
    boss: [6, 5], players: [[2, 5]], rounds: 3, playerRules: "end" },
  { key: "Q6bell_char", question: "Bell as target CHARACTER (rule SELF): push + stun on players in the ring?", kit: [j.bellChar], rules: [cast("bell", j.bellChar.id, "SELF"), endTurn()], boss: [6, 5], players: [[5, 5], [6, 7]], rounds: 2, playerRules: "end" },
  { key: "Q6bell_ou", question: "Bell as target OTHER_USER (rule CLOSEST_OPPONENT)", kit: [j.bellOU], rules: [cast("bell", j.bellOU.id, "CLOSEST_OPPONENT"), endTurn()], boss: [6, 5], players: [[5, 5], [6, 7]], rounds: 2, playerRules: "end" },
  { key: "Q6maw_ground", question: "arena EXCLUDE as GROUND: does the stun land?", kit: [j.mawGround], rules: [cast("maw", j.mawGround.id, "SELF"), endTurn()], boss: [6, 5], players: [[5, 5], [2, 2]], rounds: 2, playerRules: "end" },
  { key: "Q6maw_char", question: "arena EXCLUDE as CHARACTER (rule SELF): stun lands? caster spared? safe hex spared?", kit: [j.mawChar], rules: [cast("maw", j.mawChar.id, "SELF"), endTurn()], boss: [6, 5], players: [[5, 5], [2, 2]], rounds: 2, playerRules: "end" },
  { key: "Q2weak_only", question: "weakness on SELF (x3, 1 round, every stat/general type): does the player's damage triple, and for how long?",
    kit: [j.exposeOnly], rules: [cast("expose", j.exposeOnly.id, "SELF", [cond.roundGt(1)]), endTurn()], boss: [6, 5], players: [[4, 5]], rounds: 6, playerRules: "kit" },
  { key: "Q2weak_cleanse", question: "same, with a cleanse on SELF listed before the weakness in the same jutsu (does the cleanse strip it?)",
    kit: [j.exposeAfter], rules: [cast("expose", j.exposeAfter.id, "SELF", [cond.roundGt(1)]), endTurn()], boss: [6, 5], players: [[4, 5]], rounds: 6, playerRules: "kit" },
  { key: "Q3ring_bell", question: "spiral radius-2 ring at SELF (telegraph, tg_control) then Ship's Bell (push 3 + stun 1) next turn; players at distance 1 and 2",
    kit: [j.ringTele, j.bell], rules: [cast("bell", j.bell.id, "SELF", [cond.marker(5)]), cast("ring", j.ringTele.id, "SELF"), endTurn()], boss: [6, 5], players: [[5, 5], [6, 7]], rounds: 3, playerRules: "end" },
  { key: "Q3ring_dodge", question: "same with the harness dodge on: do players step off the ring?",
    kit: [j.ringTele, j.bell], rules: [cast("bell", j.bell.id, "SELF", [cond.marker(5)]), cast("ring", j.ringTele.id, "SELF"), endTurn()], boss: [6, 5], players: [[5, 5], [6, 7]], rounds: 3, playerRules: "kit", dodge: true },
  { key: "Q4hook_pull_root", question: "Chain Hook rows damage, pull 3, root 1: does the same-cast root cancel the pull?",
    kit: [j.hookPullRoot], rules: [cast("hook", j.hookPullRoot.id, "CLOSEST_OPPONENT"), endTurn()], boss: [8, 5], players: [[3, 5]], rounds: 2, playerRules: "end" },
  { key: "Q4hook_root_pull", question: "control: root row before the pull row",
    kit: [j.hookRootPull], rules: [cast("hook", j.hookRootPull.id, "CLOSEST_OPPONENT"), endTurn()], boss: [8, 5], players: [[3, 5]], rounds: 2, playerRules: "end" },
  { key: "Q5barrier", question: "a barrier wall (3,000 HP) between the boss and a player using the normal auto-combat kit: does the player attack the barrier, walk around it, or stall?",
    kit: [j.wall], rules: [cast("wall", j.wall.id, "EMPTY_GROUND_CLOSEST_TO_OPPONENT"), endTurn()], boss: [9, 5], players: [[3, 5]], rounds: 5, playerRules: "kit" },
  { key: "Q5wall_full", question: "a full-height barrier line (3,000 HP each, col 6, rows 0-9) between a kit-using player and the boss: does the player attack the barrier?",
    kit: [j.wall], rules: [endTurn()], boss: [9, 5], players: [[3, 5]], rounds: 6, playerRules: "kit", walls: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((y) => [6, y] as [number, number]) },
  { key: "Q5wall_gap", question: "same line with a gap at row 0: walk around or attack?",
    kit: [j.wall], rules: [endTurn()], boss: [9, 5], players: [[3, 5]], rounds: 6, playerRules: "kit", walls: [1, 2, 3, 4, 5, 6, 7, 8, 9].map((y) => [6, y] as [number, number]) },
];

const out: any = { generatedBy: "engine/probe_boss.ts", dmgConfig: dmg.name, probes: [] as any[] };
for (const sc of S) {
  if (only && !only.includes(sc.key)) continue;
  const ov: any = {
    jutsu: Object.fromEntries(sc.kit.map((x) => [x.id, x])),
    newEnemies: { boss: { base: "Deck Warden", username: `Boss ${sc.key}`, jutsuIds: sc.kit.map((x) => x.id), rules: sc.rules, includeDefaultRules: false, effects: [] } },
  };
  const t = buildTemplates(baseline, ov);
  const rows = Object.fromEntries(Object.entries(t.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
  const v = { ...PLAYER_VARIANTS.average!, ...(sc.playerRules === "end" ? { rules: [endTurn()] } : {}) };
  const donor = t.enemies["texZaFi42S3EvJZBwQ8cd"]!.row;
  const rand = mulberry32(1);
  const orig = Math.random;
  Math.random = rand;
  try {
    const players = sc.players.map((_, i) => playerQueryUser(i, v as never, donor, t.jutsu));
    const b = await assembleFloor({ players, enemyRows: rows, floor: { kind: "floor", waves: [{ aiIds: ["boss"], delayRounds: 0 }] }, rand, initialBarriers: false, dmgConfig: dmg.config, mode: "quest" });
    const bu = b.usersState.find((u) => u.controllerId === "boss")!;
    [bu.longitude, bu.latitude] = sc.boss;
    players.forEach((p, i) => {
      const u = b.usersState.find((x) => x.userId === p.userId)!;
      [u.longitude, u.latitude] = sc.players[i]!;
    });
    for (const [x, y] of sc.walls ?? [])
      b.groundEffects.push({ ...j.wall.effects[0], id: `wall-${x}-${y}`, creatorId: bu.userId, actionId: j.wall.id, createdRound: 0, level: 1, longitude: x, latitude: y, isNew: false, castThisRound: false, barrierAbsorb: 0, rounds: 10 } as never);
    const res = runFloor(b, { playerIds: players.map((p) => p.userId), maxRounds: sc.rounds, detail: true, dodge: !!sc.dodge });
    const nameOf = (uid: string) => (uid === bu.userId ? "boss" : (players.findIndex((p) => p.userId === uid) >= 0 ? `p${players.findIndex((p) => p.userId === uid) + 1}` : uid.slice(0, 6)));
    const steps = res.steps.map((s) => ({
      round: s.round, actor: nameOf(s.actorUid), action: sc.kit.find((x) => x.id === s.actionId)?.name ?? t.jutsu[s.actionId ?? ""]?.name ?? s.actionId,
      rule: s.ruleIndex, dodge: s.dodge ?? false, from: s.actorFrom, to: s.actorTo,
      actorEffects: s.actorEffects?.map((e) => `${e.type}:${e.power}:r${e.rounds}`),
      hp: Object.fromEntries(Object.entries(s.hp).map(([k, d]) => [nameOf(k), Math.round(d)])),
      dealt: Math.round(s.dealt),
      newEffects: s.effects.map((e) => `${e.type}->${nameOf(e.target)}`),
      marks: (s.groundAfter ?? []).filter((g) => g.staticAnimation || g.type === "barrier").map((g) => `${g.type}${g.staticAnimation ? `:${g.staticAnimation}` : ""}@${g.x},${g.y}:r${g.rounds}${g.curHealth !== undefined ? `:hp${g.curHealth}` : ""}`),
    }));
    out.probes.push({ key: sc.key, question: sc.question, outcome: res.outcome, rounds: res.rounds, dodge: res.dodge, kit: sc.kit.map((x) => ({ name: x.name, method: x.method, range: x.range, cooldown: x.cooldown, actionCostPerc: x.actionCostPerc, effects: x.effects.map((e: any) => `${e.type}:${e.power}:r${e.rounds ?? 0}:${e.target}`) })), steps });
    console.log(`\n### ${sc.key}: ${sc.question}\n -> ${res.outcome} after ${res.rounds}; dodge ${JSON.stringify(res.dodge)}`);
    for (const s of steps)
      console.log(`  r${s.round} ${s.actor.padEnd(4)} ${String(s.action).slice(0, 34).padEnd(34)} rule ${s.rule}${s.dodge ? " DODGE" : ""} ${JSON.stringify(s.from)}->${JSON.stringify(s.to)} fx ${JSON.stringify(s.actorEffects)} hp ${JSON.stringify(s.hp)} new ${s.newEffects.join(",") || "-"} marks ${s.marks.length} ${s.marks.filter((m) => m.startsWith("barrier")).join(" ")}`);
  } finally {
    Math.random = orig;
  }
}
const outPath = opt("out");
if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(resolve(outPath), `${JSON.stringify(out, null, 1)}\n`);
  console.log(`wrote ${outPath}`);
}
