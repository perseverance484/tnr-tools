/**
 * Library probes: every Omen mark's primed-marker type is applied, seen by has_effect on the caster's next turn,
 * fires its blast, and does not lock another mark (two marks in one turn, both markers present together).
 *   TNR_SCRIPT=probe_library.ts run.sh [--out results/probe_library.json]
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, PLAYER_VARIANTS, playerQueryUser } from "./model";
import { assembleFloor, mulberry32, runFloor } from "./sim";
import { cast, cond, endTurn } from "./kitlib";
import { ANSWERS, buildLibrary, LIB, MARKER_TYPES, type MarkKey } from "./library";

const args = process.argv.slice(2);
const outPath = args.includes("--out") ? args[args.indexOf("--out") + 1] : undefined;
const H = process.env.TNR_HARNESS!;
const baseline = loadJson(join(H, "data/baseline.json"));
const dmg = loadDmgConfig(H, "live");
const J = buildLibrary();
const blastFor = (k: MarkKey) => Object.keys(ANSWERS).find((id) => ANSWERS[id] === k)!;

const run = async (key: string, rules: any[], kit: string[], boss: [number, number], players: [number, number][], rounds: number) => {
  const ov: any = { jutsu: J, newEnemies: { boss: { base: "Deck Warden", username: `Boss ${key}`, jutsuIds: kit, rules, includeDefaultRules: false, effects: [] } } };
  const t = buildTemplates(baseline, ov);
  const rows = Object.fromEntries(Object.entries(t.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
  const rand = mulberry32(1);
  Math.random = rand;
  const v = { ...PLAYER_VARIANTS.average!, rules: [endTurn()] };
  const ps = players.map((_, i) => playerQueryUser(i, v as never, t.enemies["texZaFi42S3EvJZBwQ8cd"]!.row, t.jutsu));
  const b = await assembleFloor({ players: ps, enemyRows: rows, floor: { kind: "floor", waves: [{ aiIds: ["boss"], delayRounds: 0 }] }, rand, initialBarriers: false, dmgConfig: dmg.config, mode: "quest" });
  const bu = b.usersState.find((u) => u.controllerId === "boss")!;
  [bu.longitude, bu.latitude] = boss;
  ps.forEach((p, i) => {
    const u = b.usersState.find((x) => x.userId === p.userId)!;
    [u.longitude, u.latitude] = players[i]!;
  });
  const res = runFloor(b, { playerIds: ps.map((p) => p.userId), maxRounds: rounds, detail: true });
  return res.steps.filter((s) => s.actorUid === bu.userId).map((s) => ({
    round: s.round, action: J[s.actionId ?? ""]?.name ?? s.actionId, rule: s.ruleIndex,
    bossEffects: (s.actorEffects ?? []).map((e) => `${e.type}:${e.power}:r${e.rounds}`),
    playersHit: Object.entries(s.hp).filter(([k, d]) => k !== bu.userId && d < 0).length,
    newEffects: [...new Set(s.effects.map((e) => e.type))],
  }));
};

const out: any = { generatedBy: "engine/probe_library.ts", markerTypes: MARKER_TYPES, probes: [] as any[] };
// Players placed so every pattern holds one: ring (distance 1-2), rows 3/5, both scatter halves, the west fan, the diagonal cross.
// A CHARACTER blast with nobody on its hexes is not a valid cast (the marker then simply expires).
const boss: [number, number] = [8, 5];
const players: [number, number][] = [[7, 5], [6, 5], [3, 3], [8, 4], [5, 7]];
for (const k of Object.keys(MARKER_TYPES) as MarkKey[]) {
  const markId = LIB.mark[k];
  const blastId = blastFor(k);
  const steps = await run(k, [cast("blast", blastId, "SELF", [cond.marker(1, MARKER_TYPES[k])]), cast("mark", markId, "SELF"), endTurn()], [markId, blastId], boss, players, 3);
  const ok = steps.some((s) => s.action === J[markId].name) && steps.some((s) => s.action === J[blastId].name && s.bossEffects.some((e) => e.startsWith(`${MARKER_TYPES[k]}:`)));
  out.probes.push({ mark: J[markId].name, key: k, markerType: MARKER_TYPES[k], blast: J[blastId].name, firedInOrder: ok, steps });
  console.log(`${k.padEnd(17)} ${MARKER_TYPES[k].padEnd(18)} ${ok ? "OK " : "FAIL"} ${steps.map((s) => `r${s.round}:${s.action}${s.playersHit ? `(hit ${s.playersHit})` : ""}`).join(" ")}`);
}
// Coexistence: two different marks in one turn (40 + 40 AP), then both markers on the boss together.
{
  const a = "ring" as MarkKey;
  const c = "scatterA" as MarkKey;
  const rules = [cast("blast scatter", blastFor(c), "SELF", [cond.marker(1, MARKER_TYPES[c])]), cast("blast ring", blastFor(a), "SELF", [cond.marker(1, MARKER_TYPES[a])]), cast("mark ring", LIB.mark[a], "SELF"), cast("mark scatter", LIB.mark[c], "SELF"), endTurn()];
  const steps = await run("coexist", rules, [LIB.mark[a], LIB.mark[c], blastFor(a), blastFor(c)], boss, players, 3);
  out.coexistence = steps;
  console.log(`coexist: ${steps.map((s) => `r${s.round}:${s.action} [${s.bossEffects.filter((e) => /cooldown|robprevent/.test(e)).join(",")}]`).join(" | ")}`);
}
if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(resolve(outPath), `${JSON.stringify(out, null, 1)}\n`);
}
