/**
 * Delayed ground damage probe (coordinator, 2026-10-28): can one GROUND jutsu warn this round and hit next round?
 * Each scenario: the boss casts a GROUND AOE_CIRCLE_SPAWN (the target hex and its ring) centred on player 1 once;
 * player 1 stands in it; player 2 starts outside and steps into the area on its next turn; both then wait.
 * Per step: HP changes, so we see when each type hits, and whom.
 *   TNR_SCRIPT=probe_ground.ts run.sh [--out results/probe_ground.json]
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, PLAYER_VARIANTS, playerQueryUser } from "./model";
import { assembleFloor, mulberry32, runFloor } from "./sim";
import { cast, endTurn, jutsu, rule, T, tag } from "./kitlib";

const args = process.argv.slice(2);
const outPath = args.includes("--out") ? args[args.indexOf("--out") + 1] : undefined;
const H = process.env.TNR_HARNESS!;
const baseline = loadJson(join(H, "data/baseline.json"));
const dmg = loadDmgConfig(H, "live");
const V: [string, any][] = [
  ["damage r0 (control)", T.damage(80)],
  ["elementaldamage r0", tag("elementaldamage", { power: 80, rounds: 0, friendlyFire: "ENEMIES" })],
  ["elementaldamage r2", tag("elementaldamage", { power: 80, rounds: 2, friendlyFire: "ENEMIES" })],
  ["damage r2", T.damage(80, { rounds: 2 })],
  ["poison r2", tag("poison", { power: 50, rounds: 2, friendlyFire: "ENEMIES" })],
  ["afterburn r2", tag("afterburn", { power: 50, rounds: 2, friendlyFire: "ENEMIES" })],
  ["drain r2", tag("drain", { power: 20, rounds: 2, friendlyFire: "ENEMIES", poolsAffected: ["Health"] })],
  ["drain r1", tag("drain", { power: 20, rounds: 1, friendlyFire: "ENEMIES", poolsAffected: ["Health"] })],
  ["drain r1, player 1 acts BEFORE the boss", tag("drain", { power: 20, rounds: 1, friendlyFire: "ENEMIES", poolsAffected: ["Health"] })],
  ["drain r1, player 1 steps out on its turn after the cast", tag("drain", { power: 20, rounds: 1, friendlyFire: "ENEMIES", poolsAffected: ["Health"] })],
];
const out: any = { generatedBy: "engine/probe_ground.ts", probes: [] as any[] };
for (const [label, fx] of V) {
  const j = jutsu("probe-ground", { name: `Ground ${label}`, description: "probe", battleDescription: "probe", target: "GROUND", method: "AOE_CIRCLE_SPAWN", range: 5, cooldown: 99, actionCostPerc: 100, effects: [fx] });
  const ov: any = { jutsu: { [j.id]: j }, newEnemies: { boss: { base: "Deck Warden", username: "Boss", jutsuIds: [j.id], rules: [cast("ground", j.id, "CLOSEST_OPPONENT"), endTurn()], includeDefaultRules: false, effects: [] } } };
  const t = buildTemplates(baseline, ov);
  const rows = Object.fromEntries(Object.entries(t.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
  const rand = mulberry32(1);
  Math.random = rand;
  const donor = t.enemies["texZaFi42S3EvJZBwQ8cd"]!.row;
  const stepOut = label.includes("steps out");
  const p1 = playerQueryUser(0, { ...PLAYER_VARIANTS.average!, rules: stepOut ? [rule("step out", [], { type: "move_towards_opponent", target: "COORDINATE", coordinates: { longitude: 5, latitude: 7 } }), endTurn()] : [endTurn()] } as never, donor, t.jutsu);
  const p2 = playerQueryUser(1, { ...PLAYER_VARIANTS.average!, rules: [rule("step in", [], { type: "move_towards_opponent", target: "COORDINATE", coordinates: { longitude: 4, latitude: 5 } }), endTurn()] } as never, donor, t.jutsu);
  const b = await assembleFloor({ players: [p1, p2], enemyRows: rows, floor: { kind: "floor", waves: [{ aiIds: ["boss"], delayRounds: 0 }] }, rand, initialBarriers: false, dmgConfig: dmg.config, mode: "quest" });
  const bu = b.usersState.find((u) => u.controllerId === "boss")!;
  const u1 = b.usersState.find((u) => u.userId === p1.userId)!;
  const u2 = b.usersState.find((u) => u.userId === p2.userId)!;
  [bu.longitude, bu.latitude] = [8, 5];
  [u1.longitude, u1.latitude] = [5, 5];
  [u2.longitude, u2.latitude] = [2, 5];
  // Boss acts first so player 2 steps in only after the cast.
  const before = label.includes("BEFORE");
  const order = before ? [u1.userId, bu.userId, u2.userId] : [bu.userId, u1.userId, u2.userId];
  b.usersState.sort((a, c) => order.indexOf(a.userId) - order.indexOf(c.userId));
  b.activeUserId = order[0]!;
  const res = runFloor(b, { playerIds: [p1.userId, p2.userId], maxRounds: 4, detail: true });
  const name = (uid: string) => (uid === p1.userId ? "p1(in at cast)" : uid === p2.userId ? "p2(steps in)" : uid === bu.userId ? "boss" : uid);
  const steps = res.steps.map((s) => ({
    round: s.round, actor: name(s.actorUid), action: s.actionId === j.id ? j.name : s.actionId, to: s.actorTo,
    hp: Object.fromEntries(Object.entries(s.hp).map(([k, d]) => [name(k), Math.round(d)])),
    newEffects: s.effects.map((e) => `${e.type}->${name(e.target)}`),
    ground: (s.groundAfter ?? []).filter((g) => g.type !== "visual").map((g) => `${g.type}@${g.x},${g.y}:r${g.rounds}`).slice(0, 2),
  }));
  out.probes.push({ label, steps });
  console.log(`\n### ${label}`);
  for (const s of steps) if (Object.keys(s.hp).length || s.action !== "wait" || s.newEffects.length) console.log(`  r${s.round} ${s.actor.padEnd(15)} ${String(s.action).slice(0, 26).padEnd(26)} -> ${JSON.stringify(s.to)} hp ${JSON.stringify(s.hp)} new ${s.newEffects.join(",") || "-"} ground ${s.ground.join(" ") || "-"}`);
}
if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(resolve(outPath), `${JSON.stringify(out, null, 1)}\n`);
}
