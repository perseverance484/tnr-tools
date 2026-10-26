/**
 * Trace one floor battle action by action (design aid).
 *   TNR_SCRIPT=trace_floor.ts run.sh <floorIndex 0-4> [override.json | ""] [tier] [seed]
 * Prints, per round, each action with the rule index that produced it, HP changes and new effects.
 */
import { join } from "node:path";
import { buildTemplates, enemyQueryUser, loadJson, PLAYER_VARIANTS, playerQueryUser } from "./model";
import { assembleFloor, mulberry32, runFloor } from "./sim";

const H = process.env.TNR_HARNESS!;
const ov = process.argv[3] ? loadJson(process.argv[3]) : {};
const t = buildTemplates(loadJson(join(H, "data/baseline.json")), ov);
const v = { ...PLAYER_VARIANTS[process.argv[4] || "strong"]!, ...(ov.players?.[process.argv[4] ?? ""] ?? {}) };
const donor = t.enemies["texZaFi42S3EvJZBwQ8cd"]!.row;
const players = [0, 1, 2].map((i) => playerQueryUser(i, v, donor, t.jutsu));
const rows = Object.fromEntries(Object.entries(t.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
const rand = mulberry32(Number(process.argv[5] ?? 1));
Math.random = rand;
const b = await assembleFloor({ players, enemyRows: rows, floor: t.floors[Number(process.argv[2] ?? 0)]!, rand, initialBarriers: true });
const r = runFloor(b, { playerIds: players.map((p) => p.userId), maxRounds: 150 });
// Battle ids of spawned waves are minted at assembly; resolve names through the wave records.
const names = new Map<string, string>(players.map((p) => [p.userId, p.username]));
for (const w of r.waves) for (const e of w.enemies) names.set(e.uid, e.name);
const jname = (id: string | null) => (id && t.jutsu[id]?.name) || String(id);
console.log(`outcome ${r.outcome} after ${r.rounds} rounds`);
for (const w of r.waves) console.log(`wave ${w.wave}: rounds ${w.startRound}-${w.endRound ?? "?"} ${w.enemies.map((e) => `${e.name}(${e.maxHealth} HP, died r${e.diedRound ?? "-"})`).join(", ")}`);
let cur = -1;
for (const s of r.steps) {
  if (s.round !== cur) {
    cur = s.round;
    console.log(`--- round ${cur}`);
  }
  const hp = Object.entries(s.hp).map(([k, d]) => `${names.get(k) ?? k}:${Math.round(d)}`).join(" ");
  console.log(`  ${(names.get(s.actorUid) ?? s.actor).padEnd(17)} ${jname(s.actionId).slice(0, 26).padEnd(26)} rule ${s.ruleIndex ?? "-"}/${s.authoredRules} ${hp} ${s.effects.map((e) => e.type).join(",")}`);
}
