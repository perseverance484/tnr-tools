/**
 * Scenario runner: many seeded fights per (variant, fight), summarised.
 *
 *   run.sh main.ts --scenario scenarios/genin_hideout.json [--out results/x.json] [--seeds N] [--only "variant|variant"]
 *
 * Scenario JSON (paths relative to the harness folder):
 *   library     record folders, merged in order (data/live/<date>, a manifest's records, ...)
 *   mode        "dungeon" (each fight is a floor: waves, full restore between floors) | "quest" (all enemies at once)
 *   seeds, maxRounds
 *   enemyOverrides  { aiId: EnemyOverride }   design knobs (level, aiEdit, rules, jutsu) applied to the read records
 *   fights      [{ name, waves: [{ aiIds, delayRounds }] }]
 *   players     { name: PlayerSpec }          reusable player builds
 *   variants    [{ name, party: [player names], policy: { dodge, dangerAnimations } }]
 *   _assumptions  free-text build assumptions, copied into the results
 *
 * Enemy move metrics (per enemy template, per move):
 *   usesPerFight          mean uses per fight
 *   usedInRunsPct         share of fights in which it was used at least once
 *   firstUseRound         per fight, the round of its first use; {median,p10,p90} over the fights that used it
 *   useRound              {median,p10,p90} over every use
 *   partyDamagePerUse     the engine's own "X takes N damage" lines on party members in the move's action effects,
 *                         summed per use (uses that hit nobody count as 0); excludes later ticks and expiry
 *   netPartyHpLossPerUse  party HP lost over the whole step (expiry, ticks and heals included), per use that lost any
 *   hitPartyPct           share of uses whose own effects damaged a party member
 */
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { isAbsolute, join } from "node:path";
import { describeRow, enemyRow, loadJson, loadLibrary, playerRow, type PlayerSpec } from "./model";
import { damageLines } from "./replay_check";
import { assemble, runFight, seedRun, type FightResult, type Policy } from "./sim";

const arg = (k: string) => {
  const i = process.argv.indexOf(k);
  return i > 0 ? process.argv[i + 1] : undefined;
};
const H = process.env.TNR_HARNESS!;
const sc = loadJson(arg("--scenario")!);
const lib = loadLibrary(sc.library.map((d: string) => (isAbsolute(d) ? d : join(H, d))));
const seeds = Number(arg("--seeds") ?? sc.seeds ?? 20);
// --only "name|name": variant names may contain commas, so the separator is "|"; an unknown name is an error.
const only = arg("--only")?.split("|");
const unknownOnly = (only ?? []).filter((n) => !sc.variants.some((v: any) => v.name === n));
if (unknownOnly.length) throw new Error(`--only: no variant named ${unknownOnly.map((n) => JSON.stringify(n)).join(", ")}`);
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
  const party = new Set(partyNames);
  type M = { uses: number; rounds: number[]; firstUse: number[]; runsUsed: number; dealt: number[]; netLoss: number[]; hits: number };
  const moves: Record<string, Record<string, M>> = {};
  for (const r of runs) {
    const seen = new Set<M>();
    for (const s of r.steps) {
      if (s.human || !s.actionId || s.actionId === "wait" || s.actionId === "move" || s.actionId === "unknown") continue;
      const who = s.actor.replace(/#\d+$/, "");
      const m = ((moves[who] ??= {})[s.action ?? s.actionId] ??= { uses: 0, rounds: [], firstUse: [], runsUsed: 0, dealt: [], netLoss: [], hits: 0 });
      m.uses++;
      m.rounds.push(s.round);
      if (!seen.has(m)) {
        seen.add(m);
        m.runsUsed++;
        m.firstUse.push(s.round);
      }
      const dealt = damageLines(s.actionTexts).filter((d) => party.has(d.who) && !/ heal/.test(d.kind)).reduce((t, d) => t + d.cents, 0) / 100;
      m.dealt.push(dealt);
      if (dealt > 0) m.hits++;
      const net = -partyNames.reduce((t, n) => t + Math.min(0, s.hp[n] ?? 0), 0);
      if (net > 0) m.netLoss.push(net);
    }
  }
  const moveTable = Object.fromEntries(
    Object.entries(moves).map(([who, ms]) => [
      who,
      Object.fromEntries(
        Object.entries(ms).map(([name, m]) => [
          name,
          {
            usesPerFight: r1(m.uses / runs.length),
            usedInRunsPct: Math.round((m.runsUsed / runs.length) * 100),
            firstUseRound: stats(m.firstUse),
            useRound: stats(m.rounds),
            hitPartyPct: Math.round((m.hits / m.uses) * 100),
            partyDamagePerUse: stats(m.dealt.map(r1)),
            netPartyHpLossPerUse: stats(m.netLoss.map(r1)),
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
  const settlements: Record<string, number> = {};
  for (const r of runs) for (const p of Object.values(r.participants)) settlements[p.outcome] = (settlements[p.outcome] ?? 0) + 1;
  return {
    fight: fight.name,
    winRate: Math.round((won.length / runs.length) * 100),
    outcomes: Object.fromEntries(["won", "lost", "stalled"].map((o) => [o, runs.filter((r) => r.outcome === o).length])),
    wonSeeds: runs.map((r, i) => (r.outcome === "won" ? i + 1 : null)).filter((x) => x !== null),
    participantSettlements: settlements,
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

const scenarioPath = arg("--scenario")!;
const out: any = {
  invocation: { script: "main.ts", args: process.argv.slice(2).map((a) => a.replace(/^.*\/harness\/combat_sim\//, "")) },
  scenario: scenarioPath.replace(/^.*\/harness\/combat_sim\//, ""),
  scenarioSha256: createHash("sha256").update(readFileSync(scenarioPath)).digest("hex"),
  harnessCode: process.env.TNR_HARNESS_CODE ?? null,
  enginePin: process.env.TNR_ENGINE_PIN,
  seeds, maxRounds: sc.maxRounds ?? 40, mode: sc.mode,
  seedFormula: "fight k (0-based), seed s (1..seeds): seedRun(s * 7919 + k)",
  assumptions: sc._assumptions ?? null,
  sources: {}, builds: {}, variants: [],
};
for (const id of Object.keys(lib.ai)) out.sources[`ai/${id}`] = lib.sources[`ai/${id}`];
const traces: any = {};
for (const v of sc.variants) {
  if (only && !only.includes(v.name)) continue;
  const specs: PlayerSpec[] = v.party.map((n: string) => ({ ...sc.players[n], name: v.party.length > 1 ? `${sc.players[n].name} ${v.party.indexOf(n) + 1}` : sc.players[n].name }));
  // party member names must be unique for the per-player HP report
  specs.forEach((s, i) => (s.name = specs.filter((x) => x.name === s.name).length > 1 ? `${s.name}#${i + 1}` : s.name));
  const partyNames = specs.map((s) => s.name);
  out.builds[v.name] = specs.map((s, i) => describeRow(playerRow(lib, s, i, donor)));
  const fights: any[] = [];
  const wonBySeed: boolean[][] = [];
  for (const [k, fight] of sc.fights.entries()) {
    const runs: FightResult[] = [];
    for (let seed = 1; seed <= seeds; seed++) {
      seedRun(seed * 7919 + k);
      const players = specs.map((s, i) => playerRow(lib, s, i, donor));
      const battle = await assemble({ players, enemyRows: rows, waves: fight.waves, mode: sc.mode ?? "dungeon", runtime: lib.runtime, totalFloors: sc.fights.length });
      runs.push(runFight(battle, { maxRounds: sc.maxRounds ?? 40, policy: v.policy as Policy }));
    }
    wonBySeed.push(runs.map((r) => r.outcome === "won"));
    const s = summarise(fight, partyNames, runs);
    fights.push(s);
    traces[`${v.name}/${fight.name}`] = {
      seed: 1,
      outcome: runs[0]!.outcome,
      participants: runs[0]!.participants,
      opening: runs[0]!.opening,
      steps: runs[0]!.steps.map((st) => `r${st.round} w${st.wave} ${st.actor}: ${st.idle ? "(timed out)" : st.action ?? "-"}${st.at ? ` @${st.at}` : ""}${st.dodge ? " (dodge)" : ""} ${JSON.stringify(st.hp)}`),
    };
    console.error(`${v.name} | ${fight.name}: win ${s.winRate}%  rounds ${s.roundsToWin?.median ?? "-"} (p10 ${s.roundsToWin?.p10 ?? "-"}, p90 ${s.roundsToWin?.p90 ?? "-"})  HP left ${s.partyHpLeftPctWhenWon?.median ?? "-"}%`);
  }
  // Floors restore fully between fights, so each floor is run on its own. A seed index "clears the whole hideout"
  // when the floor run with that index was won on every floor.
  const wholeRun = Array.from({ length: seeds }, (_, i) => wonBySeed.every((f) => f[i]));
  out.variants.push({
    name: v.name, party: partyNames, policy: v.policy ?? {}, fights,
    wholeHideout: { seedIndicesClearingEveryFloor: wholeRun.filter(Boolean).length, of: seeds, productOfFloorWinRatesPct: Math.round(fights.reduce((p, f) => p * (f.winRate / 100), 1) * 100) },
  });
}
out.tracesFirstSeed = traces;
const o = arg("--out");
if (o) writeFileSync(o, JSON.stringify(out, null, 1));
console.log(JSON.stringify(out.variants.map((v: any) => ({ variant: v.name, wholeHideout: v.wholeHideout, fights: v.fights.map((f: any) => [f.fight, `${f.winRate}%`, f.roundsToWin?.median ?? null, f.partyHpLeftPctWhenWon?.median ?? null]) })), null, 1));
