/**
 * Library probes: every Omen mark's primed-marker type is applied, seen by has_effect on the caster's next turn,
 * fires its blast, and does not lock another mark (two marks in one turn, both markers present together).
 *   TNR_SCRIPT=probe_library.ts run.sh [--out results/probe_library.json]
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, petFor, PLAYER_VARIANTS, playerQueryUser } from "./model";
import { assembleFloor, mulberry32, runFloor } from "./sim";
import { cast, cond, endTurn } from "./kitlib";
import { ANSWERS, buildLibrary, LIB, MARKER_TYPES, type MarkKey, PATTERNS } from "./library";
import { getBattleGrid } from "@/libs/combat/util";
import { getTargetTiles } from "@/libs/combat/targeting";

const args = process.argv.slice(2);
const outPath = args.includes("--out") ? args[args.indexOf("--out") + 1] : undefined;
const H = process.env.TNR_HARNESS!;
const baseline = loadJson(join(H, "data/baseline.json"));
const dmg = loadDmgConfig(H, "live");
const J = buildLibrary();
const blastFor = (k: MarkKey) => Object.keys(ANSWERS).find((id) => ANSWERS[id] === k)!;

const run = async (key: string, rules: any[], kit: string[], boss: [number, number], players: [number, number][], rounds: number, dodge = false, petCells?: [number, number][]) => {
  const ov: any = { jutsu: J, newEnemies: { boss: { base: "Deck Warden", username: `Boss ${key}`, jutsuIds: kit, rules, includeDefaultRules: false, effects: [] } } };
  const t = buildTemplates(baseline, ov);
  const rows = Object.fromEntries(Object.entries(t.enemies).map(([id, e]) => [id, enemyQueryUser(e)]));
  const rand = mulberry32(1);
  Math.random = rand;
  const v = { ...PLAYER_VARIANTS.average!, rules: [endTurn()] };
  const ps = players.map((_, i) => playerQueryUser(i, v as never, t.enemies["texZaFi42S3EvJZBwQ8cd"]!.row, t.jutsu));
  const pets = petCells ? ps.map((p) => petFor(p)) : undefined;
  if (pets) ps.forEach((p, i) => (p.activePetId = pets[i]!.id));
  const b = await assembleFloor({ players: ps, enemyRows: rows, floor: { kind: "floor", waves: [{ aiIds: ["boss"], delayRounds: 0 }] }, rand, initialBarriers: false, dmgConfig: dmg.config, mode: "quest", pets });
  if (pets) {
    // Pets stand still (end turn) on the given cells.
    for (const pet of b.usersState.filter((u: any) => u.petId)) {
      const i = ps.findIndex((p) => p.userId === pet.controllerId);
      [pet.longitude, pet.latitude] = petCells![i]!;
      const prof = (b.extraState.aiProfiles as any)[pet.aiProfileId];
      if (prof) {
        prof.rules = [endTurn()];
        prof.includeDefaultRules = false;
      }
    }
  }
  const unitName = (uid: string) => {
    const u: any = b.usersState.find((x) => x.userId === uid);
    return u ? (u.petId ? `pet@${u.longitude},${u.latitude}` : u.userId === bu.userId ? "boss" : `player@${u.longitude},${u.latitude}`) : uid;
  };
  const bu = b.usersState.find((u) => u.controllerId === "boss")!;
  [bu.longitude, bu.latitude] = boss;
  ps.forEach((p, i) => {
    const u = b.usersState.find((x) => x.userId === p.userId)!;
    [u.longitude, u.latitude] = players[i]!;
  });
  const res = runFloor(b, { playerIds: ps.map((p) => p.userId), maxRounds: rounds, detail: true, dodge });
  return res.steps.filter((s) => s.actorUid === bu.userId || (dodge && s.dodge)).map((s) => ({
    ...(s.actorUid !== bu.userId ? { player: true, to: s.actorTo } : {}),
    round: s.round, action: J[s.actionId ?? ""]?.name ?? s.actionId, rule: s.ruleIndex,
    bossEffects: (s.actorEffects ?? []).map((e) => `${e.type}:${e.power}:r${e.rounds}`),
    playersHit: Object.entries(s.hp).filter(([k, d]) => k !== bu.userId && d < 0).length,
    damage: Object.fromEntries(Object.entries(s.hp).filter(([k, d]) => k !== bu.userId && d < 0).map(([k, d]) => [unitName(k), Math.round(d)])),
    groundHexes: s.ground.length,
    newEffects: [...new Set(s.effects.map((e) => e.type))],
  }));
};

const out: any = { generatedBy: "engine/probe_library.ts", markerTypes: MARKER_TYPES, probes: [] as any[] };
// Players placed so every pattern holds one: ring (distance 1-2), rows 3/5, both scatter halves, the west fan, the diagonal cross.
// A CHARACTER blast with nobody on its hexes is not a valid cast (the marker then simply expires).
const boss: [number, number] = [8, 5];
const players: [number, number][] = [[7, 5], [6, 5], [3, 3], [8, 4], [5, 7]];
const MINOR: MarkKey[] = ["splash", "shortLine"];
for (const k of (Object.keys(MARKER_TYPES) as MarkKey[]).filter((x) => !MINOR.includes(x))) {
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
// Minor marks (caster-anchored, GROUND blasts): one player (and their modelled pet) two hexes west of a crew caster.
// "stays": both stand on the pattern (damage per hit). "steps off": the player dodges (harness one-hex steps off the
// marked hexes) and the pet stands off the pattern; the blast must still erupt on the empty tiles and hit nobody.
// A target-anchored build (AOE_CIRCLE_SPAWN / AOE_LINE_SHOOT on the target) hit the dodging player too: the blast
// re-aims at the target's current hex. A CHARACTER blast was not cast at all once everyone stepped off.
out.minor = [];
for (const k of MINOR) {
  const markId = LIB.mark[k];
  const blastId = blastFor(k);
  const rules = [cast("blast", blastId, "SELF", [cond.marker(1, MARKER_TYPES[k])]), endTurn("hold", [cond.marker(1, MARKER_TYPES[k])]), cast("mark", markId, "SELF", [cond.within(1, 3)]), endTurn()];
  for (const [label, dodge, pet] of [["stays (player and pet on the pattern)", false, [5, 5]], ["steps off (pet off the pattern)", true, [6, 1]]] as const) {
    const steps = await run(`${k} ${label}`, rules, [markId, blastId], boss, [[6, 5]], 3, dodge, [pet as [number, number]]);
    const blastStep: any = steps.find((s: any) => !s.player && s.action === J[blastId].name);
    out.minor.push({ mark: J[markId].name, blast: J[blastId].name, markerType: MARKER_TYPES[k], scenario: label, blastCast: !!blastStep, groundHexes: blastStep?.groundHexes ?? 0, damage: blastStep?.damage ?? {}, steps });
    console.log(`${k.padEnd(10)} ${label.padEnd(38)} blast ${blastStep ? `cast (${blastStep.groundHexes} ground hexes)` : "NOT cast"}, damage ${JSON.stringify(blastStep?.damage ?? {})}: ${steps.map((s: any) => (s.player ? `r${s.round}:dodge->${JSON.stringify(s.to)}` : `r${s.round}:${s.action}`)).join(" ")}`);
  }
}
// Boss pairs with the harness dodge on: once marked, does each blast still go off when players step off?
out.dodged = [];
for (const k of (Object.keys(MARKER_TYPES) as MarkKey[]).filter((x) => !MINOR.includes(x))) {
  const markId = LIB.mark[k];
  const blastId = blastFor(k);
  const steps = await run(`${k} dodged`, [cast("blast", blastId, "SELF", [cond.marker(1, MARKER_TYPES[k])]), cast("mark", markId, "SELF"), endTurn()], [markId, blastId], boss, players, 3, true);
  const blastStep: any = steps.find((s: any) => !s.player && s.action === J[blastId].name);
  out.dodged.push({ key: k, blast: J[blastId].name, blastCast: !!blastStep, playersHit: blastStep?.playersHit ?? 0, dodgeSteps: steps.filter((s: any) => s.player).length });
  console.log(`dodged ${k.padEnd(17)} blast ${blastStep ? `cast, hit ${blastStep.playersHit}` : "NOT cast"} after ${steps.filter((s: any) => s.player).length} dodge steps`);
}
// Geometry, from the engine's own grid and targeting (getBattleGrid + getTargetTiles, not the harness's offsets): the
// exact hexes each caster-anchored pattern covers from a throne in an even and in an odd column (rows 4 and 5), and a
// check that every ray is a chain of engine neighbours (grid.distance 1 from the previous hex, starting next to the caster).
{
  const grid = getBattleGrid(1, { width: 12, height: 10 } as never);
  const hexes = grid.toArray();
  const at = (c: number, r: number) => hexes.find((h: any) => h.col === c && h.row === r)!;
  const ids: [string, string][] = [["Eruption: Lines / Crownfall (Omen: Lines)", LIB.blast.lines], ["Binding: Seal Lines", LIB.blast.sealLines], ["Ship's Bell (Omen: Binding Ring)", LIB.sig.shipsBell], ["Eruption: Ring", LIB.blast.ring], ["Eruption: Splash", LIB.blast.splash], ["Eruption: Short Line", LIB.blast.shortLine]];
  out.geometry = [];
  for (const [c, r] of [[8, 4], [8, 5], [9, 4], [9, 5]] as const) {
    const a = at(c, r);
    for (const [label, id] of ids) {
      const tiles = getTargetTiles({ a, b: a, action: J[id], grid } as never).map((h: any) => [h.col, h.row]).sort((p: any, q: any) => p[0] - q[0] || p[1] - q[1]);
      out.geometry.push({ throne: [c, r], columnParity: c % 2 ? "odd" : "even", pattern: label, hexes: tiles });
      console.log(`geometry (${c},${r}) ${c % 2 ? "odd " : "even"} col  ${label.padEnd(42)} ${tiles.length} hexes: ${tiles.map((t: any) => `${t[0]},${t[1]}`).join(" ")}`);
    }
    // Ray chains for the exact single-parity fan and cross.
    const par = (c % 2 ? "odd" : "even") as "even" | "odd";
    for (const [name, offs, len] of [["fan W/NW/SW", PATTERNS.linesByColumnParity[par], 5], ["cross NW/NE/SW/SE", PATTERNS.sealLinesByColumnParity[par], 5]] as const) {
      const ok = [];
      for (let k = 0; k < offs.length; k += len) {
        const ray = offs.slice(k, k + len).map((o) => at(c + o.longitude, r + o.latitude)).filter(Boolean);
        ok.push(ray.every((h, i) => grid.distance(i === 0 ? a : ray[i - 1]!, h) === 1));
      }
      out.geometry.push({ throne: [c, r], rays: name, everyStepAdjacent: ok });
      console.log(`rays (${c},${r}) ${name}: every step an engine neighbour: ${ok.join(",")}`);
    }
  }
}
if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(resolve(outPath), `${JSON.stringify(out, null, 1)}\n`);
}
