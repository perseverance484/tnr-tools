/**
 * Scenario runner: many seeded fights per (variant, fight), summarised.
 *
 *   run.sh main.ts --scenario scenarios/genin_hideout.json [--out results/x.json] [--seeds N] [--only variant,...]
 *
 * Scenario JSON (paths relative to the harness folder):
 *   library     record folders, merged in order (data/live/<date>, a manifest's records, ...)
 *   mode        "dungeon" (each fight is a floor: waves, full restore between floors) | "quest" (all enemies at once)
 *   seeds, maxRounds
 *   enemyOverrides  { aiId: EnemyOverride }   design knobs (level, aiEdit, rules, jutsu) applied to the read records
 *   fights      [{ name, waves: [{ aiIds, delayRounds }] }]
 *   players     { name: PlayerSpec }          reusable player builds
 *   variants    [{ name, party: [player names], policy: { dodge, dangerAnimations } }]
 */
import { writeFileSync } from "node:fs";
import { isAbsolute, join } from "node:path";
import { describeRow, enemyRow, loadJson, loadLibrary, playerRow, type PlayerSpec } from "./model";
import { assemble, runFight, seedRun, type FightResult, type Policy } from "./sim";

const arg = (k: string) => {
  const i = process.argv.indexOf(k);
  return i > 0 ? process.argv[i + 1] : undefined;
};
const H = process.env.TNR_HARNESS!;
const sc = loadJson(arg("--scenario")!);
const lib = loadLibrary(sc.library.map((d: string) => (isAbsolute(d) ? d : join(H, d))));
const seeds = Number(arg("--seeds") ?? sc.seeds ?? 20);
const only = arg("--only")?.split(",");
const rows: Record<string, any> = {};
for (const id of Object.keys(lib.ai)) rows[id] = enemyRow(lib, id, sc.enemyOverrides?.[id] ?? {});
// Player rows borrow the userData columns of a stored AI row (same table); every combat field is then set from the spec.
const donor = lib.ai[Object.keys(lib.ai).sort()[0]!];

const stats = (xs: number[]) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const q = (p: number) => s[Math.round(p * (s.length - 1))]!;
  return { median: q(0.5), p10: q(0.1), p90: q(0.9), mean: Math.round((xs.reduce((a, b) => a + b, 0) / xs.length) * 10) / 10 };
};
const r1 = (x: number) => Math.round(x * 10) / 10;

const summarise = (fight: any, partyNames: string[], runs: FightResult[]) => {
  const won = runs.filter((r) => r.outcome === "won");
  const hpLeft = (r: FightResult) => partyNames.map((n) => (r.final[n] ? r.final[n]!.hp / r.final[n]!.maxHp : 0));
  // Moves by enemy template: how often each fired, in which rounds, and what it did to the party.
  const moves: Record<string, Record<string, { uses: number; rounds: number[]; partyDamage: number[] }>> = {};
  for (const r of runs)
    for (const s of r.steps) {
      if (s.human || !s.actionId || s.actionId === "wait" || s.actionId === "move") continue;
      const who = s.actor.replace(/#\d+$/, "");
      const m = ((moves[who] ??= {})[s.action ?? s.actionId] ??= { uses: 0, rounds: [], partyDamage: [] });
      m.uses++;
      m.rounds.push(s.round);
      const dmg = -partyNames.reduce((t, n) => t + Math.min(0, s.hp[n] ?? 0), 0);
      if (dmg > 0) m.partyDamage.push(dmg);
    }
  const moveTable = Object.fromEntries(
    Object.entries(moves).map(([who, ms]) => [
      who,
      Object.fromEntries(
        Object.entries(ms).map(([name, m]) => [
          name,
          {
            perFight: r1(m.uses / runs.length),
            firstRound: stats(m.rounds)?.p10 ?? null,
            typicalRound: stats(m.rounds)?.median ?? null,
            hitPartyPct: Math.round((m.partyDamage.length / m.uses) * 100),
            damageWhenHit: stats(m.partyDamage.map(r1)),
          },
        ]),
      ),
    ]),
  );
  const playerMoves: Record<string, number> = {};
  let dodges = 0;
  for (const r of runs)
    for (const s of r.steps)
      if (s.human && s.actionId) {
        playerMoves[s.action ?? s.actionId] = (playerMoves[s.action ?? s.actionId] ?? 0) + 1;
        if (s.dodge) dodges++;
      }
  return {
    fight: fight.name,
    winRate: Math.round((won.length / runs.length) * 100),
    outcomes: Object.fromEntries(["won", "lost", "stalled"].map((o) => [o, runs.filter((r) => r.outcome === o).length])),
    roundsToWin: stats(won.map((r) => r.rounds)),
    roundsAll: stats(runs.map((r) => r.rounds)),
    partyHpLeftPctWhenWon: stats(won.map((r) => Math.round((hpLeft(r).reduce((a, b) => a + b, 0) / partyNames.length) * 100))),
    playersDownWhenWon: stats(won.map((r) => partyNames.filter((n) => !r.final[n]?.alive).length)),
    enemyMoves: moveTable,
    playerMovesPerFight: Object.fromEntries(Object.entries(playerMoves).map(([k, v]) => [k, r1(v / runs.length)])),
    dodgeStepsPerFight: r1(dodges / runs.length),
    issues: [...new Set(runs.flatMap((r) => [...r.steps.filter((s) => s.issue).map((s) => s.issue!), ...(r.failedReason ? [r.failedReason] : [])]))].slice(0, 5),
  };
};

const out: any = { scenario: arg("--scenario"), enginePin: process.env.TNR_ENGINE_PIN, seeds, mode: sc.mode, sources: {}, builds: {}, variants: [] };
for (const id of Object.keys(lib.ai)) out.sources[`ai/${id}`] = lib.sources[`ai/${id}`];
const sample: any = {};
for (const v of sc.variants) {
  if (only && !only.includes(v.name)) continue;
  const specs: PlayerSpec[] = v.party.map((n: string) => ({ ...sc.players[n], name: v.party.length > 1 ? `${sc.players[n].name} ${v.party.indexOf(n) + 1}` : sc.players[n].name }));
  // party member names must be unique for the per-player HP report
  specs.forEach((s, i) => (s.name = specs.filter((x) => x.name === s.name).length > 1 ? `${s.name}#${i + 1}` : s.name));
  const partyNames = specs.map((s) => s.name);
  out.builds[v.name] = specs.map((s, i) => describeRow(playerRow(lib, s, i, donor)));
  const fights: any[] = [];
  for (const fight of sc.fights) {
    const runs: FightResult[] = [];
    for (let seed = 1; seed <= seeds; seed++) {
      const rand = seedRun(seed * 7919 + fights.length);
      const players = specs.map((s, i) => playerRow(lib, s, i, donor));
      const battle = await assemble({ players, enemyRows: rows, waves: fight.waves, mode: sc.mode ?? "dungeon", runtime: lib.runtime, rand, totalFloors: sc.fights.length });
      runs.push(runFight(battle, { maxRounds: sc.maxRounds ?? 40, policy: v.policy as Policy }));
    }
    const s = summarise(fight, partyNames, runs);
    fights.push(s);
    sample[`${v.name}/${fight.name}`] = runs[0]!.steps.map((st) => `r${st.round} w${st.wave} ${st.actor}: ${st.action ?? "-"}${st.at ? ` @${st.at}` : ""}${st.dodge ? " (dodge)" : ""} ${JSON.stringify(st.hp)}`);
    console.error(`${v.name} | ${fight.name}: win ${s.winRate}%  rounds ${s.roundsToWin?.median ?? "-"} (p10 ${s.roundsToWin?.p10 ?? "-"}, p90 ${s.roundsToWin?.p90 ?? "-"})  HP left ${s.partyHpLeftPctWhenWon?.median ?? "-"}%`);
  }
  const clearAll = fights.reduce((p, f) => p * (f.winRate / 100), 1);
  out.variants.push({ name: v.name, party: partyNames, policy: v.policy ?? {}, fights, everyFloorFirstTry: Math.round(clearAll * 100) });
}
out.sampleFirstSeed = sample;
const o = arg("--out");
if (o) writeFileSync(o, JSON.stringify(out, null, 1));
console.log(JSON.stringify(out.variants.map((v: any) => ({ variant: v.name, everyFloorFirstTry: v.everyFloorFirstTry, fights: v.fights.map((f: any) => [f.fight, `${f.winRate}%`, f.roundsToWin?.median ?? null, f.partyHpLeftPctWhenWon?.median ?? null]) })), null, 1));
